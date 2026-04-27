"""Thin FastMCP server that exposes :class:`fcop.Project` over MCP.

Overall design (see adr/ADR-0002 and adr/ADR-0003):

* **fcop (library)** is the brain: business logic, validation, dataclasses.
* **fcop_mcp.server (this file)** is the telephone: maps each inbound MCP
  tool call to one :class:`fcop.Project` method call, formats the
  result as a human-readable string, and sends it back.

Everything FastMCP-specific — environment-variable discovery, stdio
transport wiring, per-session project pinning — lives in this module
only. The library never imports ``fastmcp`` and has no notion of
"current project"; every operation is explicit on a ``Project(path)``
instance.

Tool inventory for 0.6.0 mirrors the 22 tools shipped in
``fcop 0.5.4`` (legacy 0.5.x plugin / MCP 壳). Names and
argument shapes are locked by ADR-0003 — any addition goes through a
new tool, never a rename or removal. D7-a seeds the scaffolding plus
two worked examples (``set_project_dir``, ``drop_suggestion``);
D7-b / D7-c / D7-d populate the remaining twenty tools and ten
resources.
"""

from __future__ import annotations

import json
import os
import re
import sys
import threading
from collections.abc import Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

import fcop
from fastmcp import FastMCP
from fcop import Issue, Project, Report, Task, ValidationIssue

# ─── Project path resolution ─────────────────────────────────────────

# Markers that 0.5.x used to auto-detect an FCoP project root during
# the upward walk from cwd. Kept verbatim so users upgrading from
# 0.5.x to 0.6.x see the same resolution behaviour.
_AUTO_MARKERS: tuple[tuple[str, str], ...] = (
    ("docs/agents/fcop.json", "fcop.json"),
    (".cursor/rules/fcop-rules.mdc", ".cursor rule file"),
    ("docs/agents/tasks", "tasks dir"),
)

_STATE_LOCK = threading.Lock()
_SESSION_PROJECT_PATH: Path | None = None
_SESSION_PROJECT_SOURCE: str = "uninitialized"
_LEGACY_ENV_WARNED: bool = False

# Per-MCP-process role lock (since 0.7.1, ISSUE-20260427-004).
#
# The MCP server is one process per Cursor chat session. The first
# write_task / write_report / write_issue caller "claims" a sender
# role; subsequent calls with a *different* sender role are flagged
# as a Rule 1 violation (parent agent shouldn't switch roles
# mid-session, and a sub-agent claiming a different role is exactly
# the impersonation pattern Rule 1 1.8.0 forbids).
#
# This is a soft lock — the call is *allowed* to land (Rule 0.b
# admits proposer/reviewer flips, and reserved roles like ADMIN /
# SYSTEM are write-throughs), but the violation is recorded under
# ``.fcop/proposals/role-switch-{ts}.md`` so ADMIN sees evidence on
# the next ``fcop_check()``. We deliberately do NOT block writes:
# blocking just hides the impersonation; recording surfaces it.
_ROLE_LOCK: dict[str, str] = {}  # project_path → first sender role
_RESERVED_SENDERS: frozenset[str] = frozenset({"ADMIN", "SYSTEM"})


def _home_dirs() -> set[Path]:
    """Return the set of paths the resolver refuses to treat as a project.

    Binding the MCP session to a user's home / profile directory leads
    to disasters like writing ``docs/agents/tasks/`` underneath
    ``~/.cursor`` or ``C:\\Users\\<name>``. We refuse every ancestor of
    the home we can identify, so even a misconfigured ``cwd`` just
    falls through to the explicit "set a project dir" error message.
    """
    candidates: set[Path] = set()
    home = os.environ.get("HOME") or os.environ.get("USERPROFILE")
    if home:
        with _ignore_errors():
            candidates.add(Path(home).resolve())
    for var in ("APPDATA", "LOCALAPPDATA"):
        value = os.environ.get(var)
        if value:
            with _ignore_errors():
                candidates.add(Path(value).resolve())
    # Parents of each candidate home (typically ``C:\Users`` or ``/home``)
    # are also out of bounds — the presence of a ``.cursor`` marker in
    # ``C:\Users\<you>`` used to trick the 0.4.1 resolver into binding
    # the entire user profile as a project.
    for p in list(candidates):
        candidates.add(p.parent)
    return candidates


class _ignore_errors:  # noqa: N801 — context manager, not a class users see
    """Swallow exceptions from ``Path.resolve()`` on weird filesystems."""

    def __enter__(self) -> None:
        return None

    def __exit__(self, exc_type: object, exc: object, tb: object) -> bool:
        return True  # suppress


def _resolve_project_dir() -> tuple[Path, str]:
    """Return ``(project_dir, source)`` using 0.5.4's resolution cascade.

    Order matters; changing it would silently shift which directory a
    Cursor session bound to. Per ADR-0003 the cascade is locked for
    the 0.6.x series.

    1. Session pin set by ``set_project_dir`` tool.
    2. ``FCOP_PROJECT_DIR`` environment variable.
    3. ``CODEFLOW_PROJECT_DIR`` env (deprecated; prints one warning).
    4. Upward walk from cwd, looking for any known marker file.
    5. cwd itself as a last-resort fallback (with a "no markers" tag so
       ``unbound_report`` can explain it to ADMIN).
    """
    global _LEGACY_ENV_WARNED

    with _STATE_LOCK:
        pinned = _SESSION_PROJECT_PATH
    if pinned is not None:
        return pinned, "session:set_project_dir"

    explicit = os.environ.get("FCOP_PROJECT_DIR")
    if explicit:
        return Path(explicit).expanduser().resolve(), "env:FCOP_PROJECT_DIR"

    legacy = os.environ.get("CODEFLOW_PROJECT_DIR")
    if legacy:
        if not _LEGACY_ENV_WARNED:
            sys.stderr.write(
                "[fcop-mcp] WARNING: CODEFLOW_PROJECT_DIR is deprecated; "
                "rename it to FCOP_PROJECT_DIR in your MCP client config.\n"
            )
            _LEGACY_ENV_WARNED = True
        return Path(legacy).expanduser().resolve(), "env:CODEFLOW_PROJECT_DIR (deprecated)"

    try:
        cwd = Path.cwd().resolve()
    except OSError:
        cwd = Path(".").resolve()

    unsafe = _home_dirs()
    for candidate in (cwd, *cwd.parents):
        if candidate in unsafe:
            continue
        for marker, _label in _AUTO_MARKERS:
            if (candidate / marker).exists():
                return candidate, f"auto:{marker}"

    if cwd in unsafe:
        return (
            cwd,
            'cwd fallback (home dir — unsafe; call set_project_dir("<your project>") '
            "or set FCOP_PROJECT_DIR)",
        )
    return cwd, "cwd fallback (no markers; consider setting FCOP_PROJECT_DIR)"


def _get_project() -> tuple[Project, str]:
    """Resolve the current project path and return a fresh :class:`Project`.

    Constructing a new ``Project`` per call is cheap — it only stores
    a resolved path — and keeps the library free of hidden global
    state. The ``source`` string is returned alongside so tools like
    ``unbound_report`` can explain *why* the resolver picked this path.
    """
    path, source = _resolve_project_dir()
    return Project(path), source


# ─── FastMCP instance ────────────────────────────────────────────────

mcp = FastMCP("fcop")


# ─── Tools ───────────────────────────────────────────────────────────


@mcp.tool
def set_project_dir(path: str) -> str:
    """Pin the project root for this MCP session.

    Useful when the MCP process was spawned with the wrong working
    directory — typical symptom: ``unbound_report`` shows a project
    path like ``C:\\Users\\<you>`` instead of the workspace you
    actually opened in Cursor. Calling this tool once re-binds every
    subsequent tool call to the given directory, **without** editing
    ``mcp.json`` or restarting Cursor.

    Safe to call while UNBOUND — re-pointing at a directory is not a
    role-claim and writes nothing. It only mutates in-process state.

    Args:
        path: absolute path to the project root (the directory that
            should contain ``docs/agents/`` and ``.cursor/rules/``).
            The directory must exist; it does not need to be an
            already-initialized FCoP project.

    Returns:
        Bilingual confirmation with the resolved absolute path and
        whether ``docs/agents/fcop.json`` is present.
    """
    if not path or not isinstance(path, str):
        return (
            "错误：path 不能为空，需要传入绝对路径 / "
            "error: path must be a non-empty absolute path string"
        )
    try:
        resolved = Path(path).expanduser().resolve()
    except (OSError, RuntimeError) as exc:
        return f"错误：路径无法解析 / error resolving path: {exc}"
    if not resolved.exists():
        return (
            f"错误：路径不存在 / error: path does not exist: {resolved}\n"
            "请先创建目录，或传入一个已存在的绝对路径。\n"
            "Create the directory first, or pass an existing absolute path."
        )
    if not resolved.is_dir():
        return f"错误：路径不是目录 / error: path is not a directory: {resolved}"

    global _SESSION_PROJECT_PATH, _SESSION_PROJECT_SOURCE
    with _STATE_LOCK:
        _SESSION_PROJECT_PATH = resolved
        _SESSION_PROJECT_SOURCE = "session:set_project_dir"

    project = Project(resolved)
    cfg_present = project.config_path.exists()
    rules_present = (resolved / ".cursor" / "rules" / "fcop-rules.mdc").exists()

    return (
        f"已绑定项目根 / project root bound: `{resolved}`\n"
        f"- docs/agents/fcop.json present: {'yes' if cfg_present else 'no'}\n"
        f"- .cursor/rules/fcop-rules.mdc present: "
        f"{'yes' if rules_present else 'no'}\n\n"
        f"下一步 / next: 调用 `unbound_report()` 查看绑定后状态；"
        f"未初始化的话再调 `init_solo` / `init_project` / "
        f"`create_custom_team`。\n"
        f"Call `unbound_report()` to view post-bind state; if not yet "
        f"initialized, call `init_solo` / `init_project` / "
        f"`create_custom_team`."
    )


# ─── Formatting helpers ──────────────────────────────────────────────
#
# MCP tools return plain strings that Cursor / Claude Desktop render
# into the agent's context window. The library, on the other hand,
# returns structured dataclasses. Everything between "dataclass" and
# "user-readable text" lives here so individual tools stay trivial.
#
# Per ADR-0003: these helpers may be refined freely — no stability
# commitment on exact formatting — but they must keep the same
# *fields* present in the output so downstream scripts that grep
# the output don't silently break.


def _format_error(exc: Exception) -> str:
    """Render an exception as a bilingual user-facing string."""
    name = exc.__class__.__name__
    return f"错误 / error ({name}): {exc}"


def _format_task_line(task: Task) -> str:
    """One-line summary of a Task, matching 0.5.4's list_tasks format."""
    priority = task.frontmatter.priority.value
    recipient = task.frontmatter.recipient
    sender = task.frontmatter.sender
    subject = task.frontmatter.subject or "(no subject)"
    status = " [archived]" if task.is_archived else ""
    return (
        f"  - {task.filename}  [{priority}]  {sender}→{recipient}{status}\n"
        f"      {subject}"
    )


def _format_task_full(task: Task) -> str:
    """Full task content: metadata header + body."""
    fm = task.frontmatter
    refs = ", ".join(fm.references) if fm.references else "(none)"
    lines = [
        f"# {task.filename}",
        "",
        f"- task_id: {task.task_id}",
        f"- sender: {fm.sender}",
        f"- recipient: {fm.recipient}",
        f"- priority: {fm.priority.value}",
        f"- thread_key: {fm.thread_key or '(none)'}",
        f"- subject: {fm.subject or '(none)'}",
        f"- references: {refs}",
        f"- archived: {task.is_archived}",
        "",
        "---",
        "",
        task.body,
    ]
    return "\n".join(lines)


def _format_report_line(report: Report) -> str:
    """One-line summary of a Report, matching 0.5.4's list_reports format."""
    archived = " [archived]" if report.is_archived else ""
    return (
        f"  - {report.filename}  "
        f"task={report.task_id}  {report.reporter}→{report.recipient}  "
        f"status={report.status}{archived}"
    )


def _format_report_full(report: Report) -> str:
    lines = [
        f"# {report.filename}",
        "",
        f"- task_id: {report.task_id}",
        f"- reporter: {report.reporter}",
        f"- recipient: {report.recipient}",
        f"- status: {report.status}",
        f"- archived: {report.is_archived}",
        "",
        "---",
        "",
        report.body,
    ]
    return "\n".join(lines)


def _format_issue_line(issue: Issue) -> str:
    return (
        f"  - {issue.filename}  [{issue.severity.value}]  "
        f"{issue.reporter}: {issue.summary}"
    )


def _format_validation_issues(issues: Sequence[ValidationIssue]) -> str:
    if not issues:
        return "PASS — no violations detected."
    errors = [i for i in issues if i.severity == "error"]
    warnings = [i for i in issues if i.severity == "warning"]
    lines: list[str] = []
    if errors:
        lines.append(f"FAIL — {len(errors)} error(s):")
        for v in errors:
            prefix = f"{v.field}: " if v.field else ""
            lines.append(f"  - {prefix}{v.message}")
    if warnings:
        lines.append(f"WARN — {len(warnings)} warning(s):")
        for v in warnings:
            prefix = f"{v.field}: " if v.field else ""
            lines.append(f"  - {prefix}{v.message}")
    return "\n".join(lines)


def _record_role_switch(
    project: Project, *, claimed_role: str, locked_role: str, kind: str
) -> None:
    """Drop a `.fcop/proposals/role-switch-{ts}.md` describing the violation.

    Used by :func:`_check_role_lock` when a write_* tool is called
    under a role that disagrees with the lock established by the
    first write of this MCP-server lifetime. Failure is silent (best
    effort) — the user-visible warning in the tool's return value is
    the primary signal; this file is the durable evidence ADMIN finds
    later via :func:`fcop_check` / git history.
    """
    proposals = project.path / ".fcop" / "proposals"
    try:
        proposals.mkdir(parents=True, exist_ok=True)
    except OSError:
        return
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    target = proposals / f"role-switch-{ts}.md"
    body = (
        f"# Rule 1 role-switch evidence ({kind})\n\n"
        f"- timestamp: {ts}\n"
        f"- locked role (first write of this MCP session): `{locked_role}`\n"
        f"- claimed role (this write): `{claimed_role}`\n"
        f"- tool: `{kind}`\n\n"
        "This MCP-server process previously wrote a file under the\n"
        f"role `{locked_role}` and is now being asked to write under\n"
        f"`{claimed_role}`. Per Rule 1 (sub-agents inherit the\n"
        "caller's seat, since rules 1.8.0) one MCP session = one\n"
        "role binding for life. The current write was *allowed* to\n"
        "land — fcop-mcp records evidence rather than blocking, so\n"
        "the impersonation cannot be hidden by working around the\n"
        "block. ADMIN will see this conflict surfaced by\n"
        "`fcop_check()` and decide handoff / co-review / distinct\n"
        "role per Rule 1.\n"
    )
    try:
        target.write_text(body, encoding="utf-8")
    except OSError:
        return


def _check_role_lock(project: Project, sender: str, kind: str) -> str:
    """Apply the per-MCP-process role lock from ISSUE-20260427-004.

    Returns a non-empty warning string when a violation was recorded
    (the caller appends it to the tool's normal return value), and
    the empty string on the happy path. Reserved senders (``ADMIN``,
    ``SYSTEM``) and the very first write of a project never produce a
    warning.
    """
    sender_norm = (sender or "").strip().upper()
    if not sender_norm or sender_norm in _RESERVED_SENDERS:
        return ""
    project_key = str(project.path)
    with _STATE_LOCK:
        locked = _ROLE_LOCK.get(project_key)
        if locked is None:
            _ROLE_LOCK[project_key] = sender_norm
            return ""
        if locked == sender_norm:
            return ""
    _record_role_switch(
        project,
        claimed_role=sender_norm,
        locked_role=locked,
        kind=kind,
    )
    return (
        "\n\n[Rule 1 warning] this MCP session previously wrote as "
        f"`{locked}` but is now writing as `{sender_norm}`. The write "
        "landed; evidence dropped at `.fcop/proposals/role-switch-*.md`. "
        "Run `fcop_check()` to confirm, then decide handoff / co-review "
        "/ distinct-role per Rule 1."
    )


def _parse_roles_list(roles: str) -> list[str]:
    """Split a comma-separated role-code string into normalized uppercase codes."""
    return [r.strip().upper() for r in roles.split(",") if r.strip()]


def _parse_refs_list(references: str) -> tuple[str, ...]:
    """Split a comma-separated references string into a tuple."""
    if not references:
        return ()
    return tuple(r.strip() for r in references.split(",") if r.strip())


def _letter_handover_block(lang: str) -> str:
    """Compose the post-init "give the letter to ADMIN" block.

    Why this exists. 0.6.3 deposited ``LETTER-TO-ADMIN.md`` to disk
    (well, was *supposed* to — see the 0.6.4 fix) but never surfaced
    it in the chat. ADMIN had to know to go look for it. In practice
    nobody did, so the manual was effectively invisible. 0.6.4
    splices the letter's intro slice (title + 0.6.4 summary +
    identity diagram) into the post-init reply, plus an explicit
    instruction telling the agent to forward this block verbatim to
    ADMIN before doing anything else.

    The slice is bounded — pasting the entire 500-line letter into
    every init reply would torch the chat context. Agents needing
    the full text read it from ``docs/agents/LETTER-TO-ADMIN.md``
    on disk or from the ``fcop://letter/zh|en`` MCP resource
    (already exposed). Both endpoints are advertised inside the
    handover block so the next step is obvious.

    The Chinese / English copy track each other and use a fenced
    region with a leading marker line so a follow-up parser (or a
    test) can locate the block without regex acrobatics.
    """
    normalized: Literal["zh", "en"] = "en" if lang == "en" else "zh"
    try:
        intro = fcop.rules.get_letter_intro(normalized)
    except (ValueError, fcop.FcopError):
        # Defensive: a packaging failure here should not break init.
        # The disk-side letter is still landed by Project.init_*; the
        # agent can always read it from there.
        intro = ""

    if normalized == "en":
        header = (
            "─────────────────────────────────────────────────\n"
            "📨 Letter to ADMIN — please read it to ADMIN now\n"
            "─────────────────────────────────────────────────\n"
            "\n"
            "Agent: paste the block below to ADMIN VERBATIM (do not "
            "summarise, do not skip the 0.6.4 summary). After ADMIN "
            "has read it, ask whether they want the full manual.\n"
            "\n"
            "Full manual lives in two places:\n"
            "  • on disk: docs/agents/LETTER-TO-ADMIN.md\n"
            "  • MCP resource: fcop://letter/en\n"
            "\n"
            "──────── BEGIN LETTER (intro slice) ────────\n"
        )
        footer = (
            "\n──────── END LETTER (intro slice) ────────\n"
            "\n"
            "(The full letter continues with: the three entry "
            "points table, day-to-day operations, common mistakes, "
            "and the resource catalogue. Ask ADMIN whether to read "
            "those sections too.)"
        )
    else:
        header = (
            "─────────────────────────────────────────────────\n"
            "📨 给 ADMIN 的一封信 —— 请现在念给 ADMIN 听\n"
            "─────────────────────────────────────────────────\n"
            "\n"
            "Agent：把下面这一整段**原样**贴给 ADMIN（不要省略，"
            "尤其是 0.6.4 摘要那一段）。念完后问 ADMIN 是否需要继续"
            "看完整版。\n"
            "\n"
            "完整说明书有两处可读：\n"
            "  • 本地文件：docs/agents/LETTER-TO-ADMIN.md\n"
            "  • MCP 资源：fcop://letter/zh\n"
            "\n"
            "──────── 信件开始（前导段） ────────\n"
        )
        footer = (
            "\n──────── 信件结束（前导段） ────────\n"
            "\n"
            "（完整信件还有：三种起手方式表、日常操作要点、常见"
            "错误、资源目录。读完上面这段后，问 ADMIN 是否需要"
            "继续读完整版。）"
        )
    return header + intro + footer


# ─── init_* tools ────────────────────────────────────────────────────


@mcp.tool
def init_project(
    team: str = "dev-team",
    lang: str = "zh",
    force: bool = False,
) -> str:
    """Initialize an FCoP project with a bundled preset team.

    Creates ``docs/agents/`` (tasks / reports / issues / shared / log),
    writes ``docs/agents/fcop.json``, deposits ``LETTER-TO-ADMIN.md``
    under ``docs/agents/``, creates the ``workspace/`` cage with a
    starter README (per Rule 7.5), deploys the team's three-layer
    docs to ``docs/agents/shared/`` (TEAM-README / TEAM-ROLES /
    TEAM-OPERATING-RULES + ``roles/{ROLE}.md``, both zh and en),
    and (per ADR-0006) deploys the bundled protocol rules to **four**
    locations so any agent host sees them:
    ``.cursor/rules/fcop-rules.mdc``,
    ``.cursor/rules/fcop-protocol.mdc``, ``AGENTS.md``, and
    ``CLAUDE.md``. Existing copies are archived to
    ``.fcop/migrations/<timestamp>/`` before being overwritten.

    Args:
        team: Team template ID. One of ``dev-team`` / ``media-team`` /
            ``mvp-team`` / ``qa-team``. Default: ``dev-team``.
            (Solo mode is a separate entry point — call ``init_solo``
            instead so the config carries ``mode="solo"``.)
        lang: Output language. ``zh`` or ``en``. Default: ``zh``.
        force: When ``True``, overwrite an already-initialized project.
            The previous ``fcop.json``, letter, workspace README, and
            ``shared/`` documents are archived under
            ``.fcop/migrations/<timestamp>/`` before the new content
            lands — nothing is lost silently. Use this when ADMIN
            wants to switch teams (e.g. solo → dev-team) without
            manually wiping the project. Default: ``False``.

    Returns:
        Post-init summary with roster, leader, and directory layout.
    """
    try:
        project, _source = _get_project()
        status = project.init(
            team=team, lang=lang, deploy_rules=True, force=force
        )
    except fcop.ProjectAlreadyInitializedError as exc:
        return (
            f"项目已初始化 / already initialized: {exc}\n"
            "如需切换团队 / to switch teams, "
            "rerun with force=True (旧文件会归档到 .fcop/migrations/)."
        )
    except fcop.FcopError as exc:
        return _format_error(exc)

    cfg = status.config
    assert cfg is not None, "init must produce a config"
    lines = [
        f"Project initialized: {cfg.team} (lang={cfg.lang})",
        f"Path: {status.path}",
        f"Roles: {', '.join(cfg.roles)}",
        f"Leader: {cfg.leader}",
        "Directories: tasks/, reports/, issues/, shared/, log/",
        "Rules deployed: .cursor/rules/*.mdc, AGENTS.md, CLAUDE.md",
        "Letter deposited: docs/agents/LETTER-TO-ADMIN.md",
        "",
        "下一步 / next: fcop_report 查看状态后，"
        "由 ADMIN 通过『你是 <ROLE>』语句为本会话分配角色。",
        "",
        _letter_handover_block(cfg.lang),
    ]
    return "\n".join(lines)


@mcp.tool
def init_solo(
    role_code: str = "ME",
    role_label: str = "",
    lang: str = "zh",
    force: bool = False,
) -> str:
    """Initialize an FCoP project in **Solo mode** (one AI, no dispatch).

    Solo mode is for projects where a single agent works directly with
    ADMIN. Rule 0.b still applies: the agent uses files to split itself
    into *proposer* and *reviewer*, even though there is no second role.

    Beyond ``fcop.json`` and the canonical directories, this also
    deposits ``docs/agents/LETTER-TO-ADMIN.md`` (the user manual),
    creates the ``workspace/`` cage with a starter README (per Rule
    7.5), deploys the bundled solo three-layer docs (TEAM-README /
    TEAM-ROLES / TEAM-OPERATING-RULES + ``roles/ME.md``, both zh and
    en) to ``docs/agents/shared/``, and (per ADR-0006) drops the
    bundled protocol rules into ``.cursor/rules/*.mdc`` +
    ``AGENTS.md`` + ``CLAUDE.md``. Existing copies are archived under
    ``.fcop/migrations/<timestamp>/`` before being overwritten.

    Args:
        role_code: The single role code (uppercase letters / digits /
            underscore, must start with a letter; ``ADMIN`` and
            ``SYSTEM`` are reserved). Default: ``ME``.
        role_label: Display label (e.g. ``"我自己"``). Currently
            recorded in ``extra`` for future use; the library does not
            yet consume it. Safe to omit.
        lang: Output language, ``zh`` or ``en``.
        force: When ``True``, overwrite an already-initialized project.
            All previous artifacts (config, letter, workspace README,
            ``shared/`` docs, protocol rule files) are archived under
            ``.fcop/migrations/<timestamp>/`` before the new content
            lands. Use this when ADMIN wants to switch from team mode
            back to solo, or re-init solo with a different
            ``role_code``. Default: ``False``.
    """
    try:
        project, _source = _get_project()
        status = project.init_solo(
            role_code=role_code, lang=lang, deploy_rules=True, force=force
        )
    except fcop.ProjectAlreadyInitializedError as exc:
        return (
            f"项目已初始化 / already initialized: {exc}\n"
            "如需重置或切到 solo / to reset or switch to solo, "
            "rerun with force=True (旧文件会归档到 .fcop/migrations/)."
        )
    except fcop.FcopError as exc:
        return _format_error(exc)

    cfg = status.config
    assert cfg is not None
    label = role_label.strip() or cfg.leader
    return (
        f"Solo-mode project initialized.\n"
        f"Path: {status.path}\n"
        f"Role: {cfg.leader} ({label})\n"
        f"Lang: {cfg.lang}\n"
        f"Directories: tasks/, reports/, issues/, shared/, log/\n"
        f"Rules deployed: .cursor/rules/*.mdc, AGENTS.md, CLAUDE.md\n"
        f"Letter deposited: docs/agents/LETTER-TO-ADMIN.md\n"
        f"\n"
        f"{_letter_handover_block(cfg.lang)}"
    )


@mcp.tool
def create_custom_team(
    team_name: str,
    roles: str,
    leader: str,
    lang: str = "zh",
    force: bool = False,
) -> str:
    """Create an FCoP project with a custom roster of roles.

    Role codes can be anything — they become part of task filenames,
    e.g. ``TASK-20260423-001-BOSS-to-CODER.md``. Use ``validate_team_config``
    first to catch illegal role codes without writing anything.

    Custom teams have **no bundled three-layer docs**, so
    ``docs/agents/shared/`` is left empty (apart from the project's
    own ``shared/README.md``). The recommended next step is to read
    the closest preset (``fcop://teams/<closest-preset>`` — see the
    ``teams/_data/README.md`` "Custom teams" section) and hand-author
    your own ``TEAM-README.md`` / ``TEAM-ROLES.md`` /
    ``TEAM-OPERATING-RULES.md`` + ``roles/{ROLE}.md`` based on it.

    The other init artifacts are deposited as usual:
    ``docs/agents/fcop.json``, ``LETTER-TO-ADMIN.md``,
    ``workspace/README.md``, plus the protocol rule files at
    ``.cursor/rules/*.mdc`` + ``AGENTS.md`` + ``CLAUDE.md`` (existing
    copies archived under ``.fcop/migrations/``).

    Args:
        team_name: Display name for the team (e.g. ``"My Design Studio"``).
        roles: Comma-separated role codes (e.g. ``"BOSS,CODER,TESTER"``).
        leader: Leader role code; must appear in ``roles``.
        lang: Output language, ``zh`` or ``en``.
        force: When ``True``, overwrite an already-initialized project.
            Existing config / letter / workspace README / ``shared/``
            files are archived under ``.fcop/migrations/<timestamp>/``
            before the new ones land. Default: ``False``.
    """
    role_list = _parse_roles_list(roles)
    try:
        project, _source = _get_project()
        status = project.init_custom(
            team_name=team_name,
            roles=role_list,
            leader=leader.strip().upper(),
            lang=lang,
            deploy_rules=True,
            force=force,
        )
    except fcop.ProjectAlreadyInitializedError as exc:
        return (
            f"项目已初始化 / already initialized: {exc}\n"
            "如需重置 / to reset, "
            "rerun with force=True (旧文件会归档到 .fcop/migrations/)."
        )
    except fcop.FcopError as exc:
        return _format_error(exc)

    cfg = status.config
    assert cfg is not None
    return (
        f"Custom team created: {team_name}\n"
        f"Path: {status.path}\n"
        f"Roles: {', '.join(cfg.roles)}\n"
        f"Leader: {cfg.leader}\n"
        f"Lang: {cfg.lang}\n"
        f"Rules deployed: .cursor/rules/*.mdc, AGENTS.md, CLAUDE.md\n"
        f"Letter deposited: docs/agents/LETTER-TO-ADMIN.md\n"
        f"\n"
        f"{_letter_handover_block(cfg.lang)}"
    )


@mcp.tool
def validate_team_config(roles: str, leader: str) -> str:
    """Dry-run validation for a custom team config.

    Use **before** ``create_custom_team`` to catch illegal role codes
    (Chinese characters, dashes, reserved names, duplicates) without
    writing anything to disk.

    Args:
        roles: Comma-separated role codes.
        leader: Leader role code; must be one of ``roles``.

    Returns:
        ``"OK"`` if valid, else a bulleted list of violations.
    """
    role_list = _parse_roles_list(roles)
    leader_up = leader.strip().upper()
    issues = Project.validate_team(roles=role_list, leader=leader_up)
    if not issues:
        return f"OK — {len(role_list)} role(s), leader={leader_up}"
    return _format_validation_issues(issues)


# ─── Task CRUD tools ─────────────────────────────────────────────────


@mcp.tool
def write_task(
    sender: str,
    recipient: str,
    subject: str,
    body: str,
    priority: str = "P2",
    thread_key: str = "",
    references: str = "",
) -> str:
    """Create a new task file under ``docs/agents/tasks/``.

    The library assigns a filename of the form
    ``TASK-YYYYMMDD-NNN-{SENDER}-to-{RECIPIENT}.md`` and writes a
    FCoP-v1.1-compliant YAML frontmatter + markdown body.

    Args:
        sender: Sender role code (uppercase).
        recipient: Recipient role code (uppercase). May use the
            slot form ``ROLE.D1`` for per-slot targeting or ``TEAM``
            for broadcast.
        subject: One-line subject written to the ``subject:``
            frontmatter field.
        body: Task body in Markdown.
        priority: FCoP priority. Accepts ``P0`` / ``P1`` / ``P2`` /
            ``P3`` (canonical) or the legacy aliases
            ``urgent`` / ``high`` / ``normal`` / ``low``. Default:
            ``P2``.
        thread_key: Optional thread identifier for linking this task
            to an ongoing conversation.
        references: Comma-separated task filenames this task refers
            back to (for ``references:`` frontmatter field).

    Returns:
        The filename of the created task on success; error string
        on failure.
    """
    try:
        project, _source = _get_project()
        task = project.write_task(
            sender=sender,
            recipient=recipient,
            priority=priority,
            subject=subject,
            body=body,
            references=_parse_refs_list(references),
            thread_key=thread_key or None,
        )
    except fcop.FcopError as exc:
        return _format_error(exc)
    except ValueError as exc:
        return _format_error(exc)

    warning = _check_role_lock(project, sender, "write_task")
    return f"Task created: {task.filename}\nPath: {task.path}{warning}"


@mcp.tool
def read_task(filename: str) -> str:
    """Read the full content of a task file.

    Args:
        filename: Task filename (e.g. ``TASK-20260423-001-PM-to-DEV.md``)
            or plain task ID (e.g. ``TASK-20260423-001``). Both open
            and archived tasks are searched.
    """
    try:
        project, _source = _get_project()
        task = project.read_task(filename)
    except fcop.TaskNotFoundError as exc:
        return f"File not found: {filename} ({exc})"
    except fcop.FcopError as exc:
        return _format_error(exc)

    return _format_task_full(task)


@mcp.tool
def list_tasks(
    sender: str = "",
    recipient: str = "",
    status: str = "open",
    date: str = "",
    limit: int = 0,
    offset: int = 0,
) -> str:
    """List tasks, optionally filtered.

    Args:
        sender: Filter by sender role code (case-insensitive).
        recipient: Filter by recipient role code. Matches ``to-ROLE``,
            ``to-ROLE.SLOT``, and ``to-TEAM`` broadcasts.
        status: ``open`` (default), ``archived``, or ``all``.
        date: Filter by YYYYMMDD date stamp.
        limit: Maximum number of rows to return (0 = no limit).
        offset: Number of rows to skip before returning.
    """
    status_val = status.strip().lower() or "open"
    if status_val not in ("open", "archived", "all"):
        return f"错误：status 必须为 open/archived/all，收到 '{status}'"

    try:
        project, _source = _get_project()
        tasks = project.list_tasks(
            sender=sender or None,
            recipient=recipient or None,
            status=status_val,  # type: ignore[arg-type]
            date=date or None,
            limit=limit or None,
            offset=offset,
        )
    except fcop.FcopError as exc:
        return _format_error(exc)

    if not tasks:
        detail = []
        if sender:
            detail.append(f"sender={sender}")
        if recipient:
            detail.append(f"to-{recipient}")
        if date:
            detail.append(f"date={date}")
        suffix = f" ({', '.join(detail)})" if detail else ""
        return f"No tasks found{suffix}."

    header = f"Total: {len(tasks)} task(s)"
    return header + "\n" + "\n".join(_format_task_line(task) for task in tasks)


@mcp.tool
def inspect_task(filename: str) -> str:
    """Validate a task file against FCoP grammar.

    Catches deterministic violations that raw ``read_file + regex``
    agents often miss: filename says ``to-DEV`` but frontmatter says
    ``recipient: QA``, ``protocol`` field mistyped, required field
    missing, and so on.

    Args:
        filename: Task filename or ID (same forms as ``read_task``).

    Returns:
        ``"PASS"`` if the file is fully FCoP-compliant, else a bulleted
        list of violations with field names and suggestions.
    """
    try:
        project, _source = _get_project()
        issues = project.inspect_task(filename)
    except fcop.TaskNotFoundError as exc:
        return f"File not found: {filename} ({exc})"
    except fcop.FcopError as exc:
        return _format_error(exc)

    result = _format_validation_issues(issues)
    return f"{filename}\n{result}"


@mcp.tool
def archive_task(task_id: str, lang: str = "") -> str:
    """Archive a completed task (move under ``docs/agents/log/``).

    The report file tied to this task, if any, is moved alongside so
    the archived pair stays together.

    Args:
        task_id: Task ID (e.g. ``TASK-20260423-001``) or full filename.
        lang: Kept for 0.5.4 parity; currently unused because the
            library does not need locale for this operation.
    """
    del lang  # accepted for 0.5.x API compatibility, not used here
    try:
        project, _source = _get_project()
        task = project.archive_task(task_id)
    except fcop.TaskNotFoundError as exc:
        return f"File not found: {task_id} ({exc})"
    except fcop.FcopError as exc:
        return _format_error(exc)

    return f"Archived: {task.filename}\nNew path: {task.path}"


# ─── Report CRUD tools ───────────────────────────────────────────────


@mcp.tool
def write_report(
    task_id: str,
    reporter: str,
    recipient: str,
    body: str,
    status: str = "done",
    priority: str = "P2",
) -> str:
    """Write a completion report for a task.

    Creates ``REPORT-<task_id>-{REPORTER}-to-{RECIPIENT}.md`` under
    ``docs/agents/reports/``. The ``task_id`` is the canonical reference
    back to the source task.

    Args:
        task_id: Source task ID (e.g. ``TASK-20260423-001``).
        reporter: Reporter role code (uppercase).
        recipient: Recipient role code (typically the PM).
        body: Report body in Markdown.
        status: ``done`` / ``in_progress`` / ``blocked``.
        priority: FCoP priority; accepts ``P0``–``P3`` and aliases.
    """
    status_val = status.strip().lower() or "done"
    if status_val not in ("done", "in_progress", "blocked"):
        return f"错误：status 必须为 done/in_progress/blocked，收到 '{status}'"

    try:
        project, _source = _get_project()
        report = project.write_report(
            task_id=task_id,
            reporter=reporter,
            recipient=recipient,
            body=body,
            status=status_val,  # type: ignore[arg-type]
            priority=priority,
        )
    except fcop.FcopError as exc:
        return _format_error(exc)
    except ValueError as exc:
        return _format_error(exc)

    warning = _check_role_lock(project, reporter, "write_report")
    return f"Report created: {report.filename}\nPath: {report.path}{warning}"


@mcp.tool
def list_reports(
    reporter: str = "",
    task_id: str = "",
    status: str = "open",
    limit: int = 0,
    offset: int = 0,
) -> str:
    """List reports, optionally filtered.

    Args:
        reporter: Filter by reporter role code (case-insensitive).
        task_id: Filter by source task ID.
        status: ``open`` (default), ``archived``, or ``all``.
        limit: Maximum number of rows (0 = no limit).
        offset: Number of rows to skip.
    """
    status_val = status.strip().lower() or "open"
    if status_val not in ("open", "archived", "all"):
        return f"错误：status 必须为 open/archived/all，收到 '{status}'"

    try:
        project, _source = _get_project()
        reports = project.list_reports(
            reporter=reporter or None,
            task_id=task_id or None,
            status=status_val,  # type: ignore[arg-type]
            limit=limit or None,
            offset=offset,
        )
    except fcop.FcopError as exc:
        return _format_error(exc)

    if not reports:
        return "No reports found."
    return f"Total: {len(reports)} report(s)\n" + "\n".join(
        _format_report_line(r) for r in reports
    )


@mcp.tool
def read_report(filename: str) -> str:
    """Read the full content of a report file.

    Args:
        filename: Report filename or the ``task_id`` the report was
            filed against.
    """
    try:
        project, _source = _get_project()
        report = project.read_report(filename)
    except fcop.FcopError as exc:
        return _format_error(exc)

    return _format_report_full(report)


# ─── Issue tools ─────────────────────────────────────────────────────


@mcp.tool
def write_issue(
    reporter: str,
    summary: str,
    body: str,
    severity: str = "medium",
) -> str:
    """File an issue under ``docs/agents/issues/``.

    Args:
        reporter: Reporter role code (uppercase).
        summary: One-line summary written into the filename and
            frontmatter.
        body: Detailed issue body in Markdown.
        severity: ``critical`` / ``high`` / ``medium`` / ``low``.
            Aliases: ``P0`` → critical, ``P1`` → high, ``P2`` →
            medium, ``P3`` → low.
    """
    try:
        project, _source = _get_project()
        issue = project.write_issue(
            reporter=reporter,
            summary=summary,
            body=body,
            severity=severity,
        )
    except fcop.FcopError as exc:
        return _format_error(exc)
    except ValueError as exc:
        return _format_error(exc)

    warning = _check_role_lock(project, reporter, "write_issue")
    return f"Issue created: {issue.filename}\nPath: {issue.path}{warning}"


@mcp.tool
def list_issues(
    reporter: str = "",
    severity: str = "",
    limit: int = 0,
    offset: int = 0,
    lang: str = "",
) -> str:
    """List issues, optionally filtered.

    Args:
        reporter: Filter by reporter role code (case-insensitive).
        severity: Filter by severity (``critical`` / ``high`` /
            ``medium`` / ``low``). Empty = all.
        limit: Maximum number of rows (0 = no limit).
        offset: Number of rows to skip.
        lang: Kept for 0.5.4 parity; currently unused.
    """
    del lang  # accepted for 0.5.x API compatibility, not used here
    try:
        project, _source = _get_project()
        issues = project.list_issues(
            reporter=reporter or None,
            severity=severity or None,
            limit=limit or None,
            offset=offset,
        )
    except fcop.FcopError as exc:
        return _format_error(exc)

    if not issues:
        return "No issues found."
    return f"Total: {len(issues)} issue(s)\n" + "\n".join(
        _format_issue_line(i) for i in issues
    )


# ─── Safety-fuse tools ───────────────────────────────────────────────


# ─── Team / deploy / workspace tools ─────────────────────────────────


@mcp.tool
def get_available_teams(lang: str = "zh") -> str:
    """List bundled preset teams and their role rosters.

    Useful before ``init_project`` to pick a template that fits the
    work. Each team ships with its own three-layer documentation
    (``TEAM-README.md`` + ``TEAM-ROLES.md`` + ``TEAM-OPERATING-RULES.md``)
    that gets deployed into ``docs/agents/shared/`` during ``init_project``.

    Args:
        lang: Output language hint. Currently only affects display
            prose; the roster data is language-independent.

    Returns:
        A block of markdown listing every bundled team with its ID,
        roster, and leader.
    """
    teams = fcop.teams.get_available_teams()
    if not teams:
        return "No bundled teams. This is probably a packaging bug."

    is_en = lang.lower().startswith("en")
    header = (
        f"Available preset teams ({len(teams)}):"
        if is_en
        else f"可用预设团队 {len(teams)} 个："
    )
    lines = [header]
    for info in teams:
        lines.append(
            f"  - {info.name} — "
            f"roles: {', '.join(info.roles)}; "
            f"leader: {info.leader}"
        )
    return "\n".join(lines)


@mcp.tool
def get_team_status(lang: str = "") -> str:
    """Return a concise status snapshot of the current project.

    Shows whether the project is initialized, which team / roster is
    loaded, how many open tasks / reports / issues are on disk, and
    the five most recent activity entries (sorted newest first).

    Args:
        lang: Output language (``zh`` / ``en``). Empty = auto-detect
            from ``docs/agents/fcop.json``.
    """
    try:
        project, source = _get_project()
        status = project.status()
    except fcop.FcopError as exc:
        return _format_error(exc)

    if not status.is_initialized:
        return (
            f"Project NOT initialized.\n"
            f"Path: {status.path} (source: {source})\n"
            "Call `init_solo`, `init_project`, or `create_custom_team` first."
        )

    cfg = status.config
    assert cfg is not None
    effective_lang = lang.strip() or cfg.lang

    lines = [
        f"Project: {status.path} (source: {source})",
        f"Team: {cfg.team}  Leader: {cfg.leader}  Lang: {effective_lang}",
        f"Roles: {', '.join(cfg.roles)}",
        "",
        f"Tasks: {status.tasks_open} open, {status.tasks_archived} archived",
        f"Reports: {status.reports_count}",
        f"Issues: {status.issues_count}",
    ]
    if status.recent_activity:
        lines.append("")
        lines.append("Recent activity (newest first):")
        for entry in status.recent_activity[:5]:
            lines.append(
                f"  - [{entry.kind}] {entry.filename}  — {entry.summary}"
            )
    return "\n".join(lines)


@mcp.tool
def deploy_role_templates(
    team: str = "",
    lang: str = "",
    force: bool = True,
) -> str:
    """Deploy the three-layer team documentation into ``shared/``.

    Writes ``TEAM-README.md`` (bilingual), ``TEAM-ROLES.md``,
    ``TEAM-OPERATING-RULES.md``, and per-role bios under
    ``docs/agents/shared/`` (both ``zh`` and ``en`` variants).

    When ``force=True`` (default) existing files are archived under
    ``.fcop/migrations/<timestamp>/shared/`` before being overwritten,
    so the action is safely reversible. When ``force=False`` existing
    files are left untouched and reported as skipped.

    Args:
        team: Team ID to deploy. Empty = use the current project's
            ``fcop.json`` team.
        lang: Language variant to emphasize. Empty = use project
            language from ``fcop.json``.
        force: Overwrite existing files (after archiving) vs skip.

    Returns:
        A summary listing deployed / skipped / archived paths, and
        the migration directory (when ``force=True`` archived anything).
    """
    try:
        project, _source = _get_project()
        report = project.deploy_role_templates(
            team=team or None,
            lang=(lang or None),  # type: ignore[arg-type]
            force=force,
        )
    except fcop.FcopError as exc:
        return _format_error(exc)

    lines = [
        f"Deployed: {len(report.deployed)} file(s)",
        f"Skipped: {len(report.skipped)} file(s) (already existed and force=False)",
        f"Archived: {len(report.archived)} file(s) (moved before overwrite)",
    ]
    if report.migration_dir:
        lines.append(f"Migration dir: {report.migration_dir}")
    if report.deployed:
        lines.append("")
        lines.append("Deployed paths:")
        for p in report.deployed[:10]:
            lines.append(f"  - {p}")
        if len(report.deployed) > 10:
            lines.append(f"  ... and {len(report.deployed) - 10} more")
    return "\n".join(lines)


_SLUG_RE = re.compile(r"^[a-z][a-z0-9-]*$")
_SLUG_MAX_LEN = 40


def _validate_slug(slug: str) -> str:
    """Return an error message (or empty string) for a workspace slug."""
    if not slug:
        return "错误 / error: slug 不能为空 / slug must not be empty."
    if len(slug) > _SLUG_MAX_LEN:
        return (
            f"错误 / error: slug 超过 {_SLUG_MAX_LEN} 字符 "
            f"/ slug exceeds {_SLUG_MAX_LEN} chars: {slug!r}"
        )
    if not _SLUG_RE.match(slug):
        suggested = re.sub(r"[^a-z0-9-]+", "-", slug.lower()).strip("-")
        hint = (
            f" Suggested fix: {suggested!r}"
            if suggested and _SLUG_RE.match(suggested) and len(suggested) <= _SLUG_MAX_LEN
            else ""
        )
        return (
            f"错误 / error: slug 必须匹配 ^[a-z][a-z0-9-]*$ 且 ≤ {_SLUG_MAX_LEN} 字符; "
            f"got {slug!r}." + hint
        )
    return ""


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _recent_task_mentions_slug(project: Project, slug: str) -> bool:
    """Return True iff any open ``TASK-*.md`` references the slug.

    Used by :func:`new_workspace` to decide whether to attach a
    ``Rule 0.a.1`` "you forgot Step 1 (write_task)" reminder. We check
    three places where ADMIN's task could legitimately mention the slug:

    * frontmatter ``subject`` (one-liner goal)
    * frontmatter ``references`` (e.g. ``workspace/<slug>``)
    * body text (anywhere)

    Substring match is intentional — slugs are short, hyphenated, and
    rarely appear in unrelated prose; a real task that scopes this
    workspace will almost always name the slug somewhere.

    Errors (broken frontmatter, IO) are swallowed: this is a soft
    tripwire, never a blocker.
    """
    if not slug:
        return False
    needle = slug.lower()
    try:
        tasks = project.list_tasks(status="open", limit=200)
    except Exception:
        return False
    for task in tasks:
        haystack_parts: list[str] = []
        if task.subject:
            haystack_parts.append(task.subject)
        haystack_parts.append(task.body or "")
        haystack_parts.extend(task.frontmatter.references)
        if any(needle in part.lower() for part in haystack_parts):
            return True
    return False


_RULE_0A1_TRIPWIRE_BLOCK = (
    "⚠️  FCoP Rule 0.a.1 check: no open TASK-*.md mentions slug `{slug}`.\n"
    "    FCoP Rule 0.a.1 检查：当前没有任何开放 TASK-*.md 提及 slug `{slug}`。\n"
    "\n"
    "If you just got a request from ADMIN, Step 1 is **write_task** —\n"
    "BEFORE editing any file. The 4-step cycle has no \"simple = skip\" exception.\n"
    "如果你刚收到 ADMIN 的需求，第 1 步应当是 **write_task** ——\n"
    "在动手写任何文件之前。4 步循环没有「简单任务可跳过」这种例外。\n"
    "\n"
    "  write_task(\n"
    "      sender=\"ADMIN\", recipient=\"<your role>\", priority=\"P2\",\n"
    "      subject=\"<one-line goal>\",\n"
    "      body=\"<rephrase the request + scope + acceptance criteria>\",\n"
    "  )\n"
    "\n"
    "Then drop artifacts into workspace/{slug}/, then write_report when done.\n"
    "随后把产物落到 workspace/{slug}/，完成时再调 write_report 收尾。\n"
    "\n"
    "(Workspace was created — this is a reminder, not a block.\n"
    "笼子已建好——这是提醒，不阻断创建。)\n"
    "---\n"
)


@mcp.tool
def new_workspace(slug: str, title: str = "", description: str = "") -> str:
    """Create a workspace subdirectory under ``workspace/<slug>/``.

    ``workspace/<slug>/`` is FCoP's soft convention for the actual
    artifacts of a piece of work — code, scripts, data. Keeping those
    out of the project root prevents yesterday's mini-game from
    colliding with today's report generator.

    Idempotent: calling twice with the same slug updates the title /
    description but never wipes files you already dropped in the
    folder.

    Args:
        slug: Short lowercase-hyphen name matching ``^[a-z][a-z0-9-]*$``
            and ≤ 40 chars. Examples: ``csdn-search``, ``mini-game``,
            ``weekly-report-2026w17``.
        title: Optional human-readable title (any language).
        description: Optional one-paragraph description, written into
            the per-slug README.
    """
    slug_norm = (slug or "").strip()
    err = _validate_slug(slug_norm)
    if err:
        return err

    project, _source = _get_project()
    workspace_dir = project.path / "workspace"
    workspace_dir.mkdir(parents=True, exist_ok=True)
    workspace_readme = workspace_dir / "README.md"
    if not workspace_readme.exists():
        workspace_readme.write_text(
            "# workspace/\n\n"
            "Per-slug workspaces. One subdirectory per piece of work.\n"
            "Use `new_workspace(slug=...)` to create them; do not write "
            "business code into the project root.\n",
            encoding="utf-8",
        )

    target = workspace_dir / slug_norm
    is_new = not target.exists()
    target.mkdir(parents=True, exist_ok=True)

    marker = target / ".workspace.json"
    now = _iso_now()
    created_at = now
    if marker.exists():
        try:
            prev = json.loads(marker.read_text(encoding="utf-8"))
            if isinstance(prev, dict) and prev.get("created_at"):
                created_at = str(prev["created_at"])
        except (json.JSONDecodeError, OSError):
            pass

    meta = {
        "slug": slug_norm,
        "title": title.strip(),
        "description": description.strip(),
        "created_at": created_at,
        "updated_at": now,
    }
    marker.write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    readme = target / "README.md"
    if not readme.exists():
        body_lines = [
            f"# {title.strip() or slug_norm}",
            "",
            f"Slug: `{slug_norm}`",
            f"Created: {created_at}",
        ]
        if description.strip():
            body_lines.extend(["", description.strip()])
        body_lines.extend(
            [
                "",
                "---",
                "",
                "这里放这个任务/模块的实际产物（代码、脚本、数据）。",
                "不要把业务代码写到项目根目录。",
                "",
                "Place actual work artifacts (code, scripts, data) here.",
                "Do not write business code into the project root.",
            ]
        )
        readme.write_text("\n".join(body_lines) + "\n", encoding="utf-8")

    try:
        rel = target.relative_to(project.path).as_posix()
    except ValueError:
        rel = str(target)

    verb = "Created" if is_new else "Updated"
    base = (
        f"{verb} workspace: `{rel}/`\n"
        f"  slug: {slug_norm}\n"
        f"  title: {title.strip() or '(none)'}\n"
        f"  created_at: {created_at}\n\n"
        f"{verb} workspace at `{rel}/`. Put code / scripts / data here; "
        "do not write to the project root."
    )
    if not _recent_task_mentions_slug(project, slug_norm):
        return _RULE_0A1_TRIPWIRE_BLOCK.format(slug=slug_norm) + base
    return base


@mcp.tool
def list_workspaces(lang: str = "") -> str:
    """List all ``workspace/<slug>/`` subdirectories with their metadata.

    Picks up both workspaces created by ``new_workspace`` (they have
    a ``.workspace.json`` marker) and directories created by hand
    (shown with just the slug). Use for the at-a-glance "what's
    inside this project" view.

    Args:
        lang: Output language (``zh``/``en``). Empty = auto-detect
            from project config.
    """
    try:
        project, _source = _get_project()
    except fcop.FcopError as exc:
        return _format_error(exc)

    effective_lang = lang.strip()
    if not effective_lang:
        try:
            cfg = project.config
            effective_lang = cfg.lang
        except fcop.FcopError:
            effective_lang = "zh"
    is_en = effective_lang.lower().startswith("en")

    workspace_dir = project.path / "workspace"
    if not workspace_dir.exists():
        return (
            "No `workspace/` directory yet.\n"
            'Call `new_workspace(slug="<your-slug>")` to create the first one.'
            if is_en
            else "项目里还没有 `workspace/` 目录。\n"
            '调 `new_workspace(slug="<你的-slug>")` 开第一个。'
        )

    entries: list[dict[str, str]] = []
    for child in sorted(workspace_dir.iterdir()):
        if not child.is_dir() or child.name.startswith("."):
            continue
        marker = child / ".workspace.json"
        meta: dict[str, str] = {"slug": child.name}
        if marker.exists():
            try:
                loaded = json.loads(marker.read_text(encoding="utf-8"))
                if isinstance(loaded, dict):
                    for k in ("title", "description", "created_at"):
                        if k in loaded:
                            meta[k] = str(loaded[k])
            except (json.JSONDecodeError, OSError):
                pass
        entries.append(meta)

    if not entries:
        return (
            "`workspace/` exists but has no slug subdirectories yet."
            if is_en
            else "`workspace/` 存在但还没有任何子目录。"
        )

    lines = [
        f"`workspace/` has {len(entries)} slug(s):"
        if is_en
        else f"workspace/ 下有 {len(entries)} 个笼子："
    ]
    for entry in entries:
        slug = entry.get("slug", "?")
        title = entry.get("title") or ("(no title)" if is_en else "(无标题)")
        created = entry.get("created_at") or "?"
        lines.append(f"  - {slug}  —  {title}  (created: {created})")
    return "\n".join(lines)


# ─── Safety-fuse tools ───────────────────────────────────────────────


@mcp.tool
def drop_suggestion(content: str, context: str = "") -> str:
    """Pressure valve for agents who disagree with the current FCoP protocol.

    Writes a timestamped markdown file under ``.fcop/proposals/`` that
    ADMIN can review later. **This is the ONLY sanctioned way for an
    agent to push back on the rule files** (``fcop-rules.mdc`` /
    ``fcop-protocol.mdc``). Agents MUST NOT edit the rule files
    themselves; those are ADMIN's source of truth.

    Works before ``init_project`` / ``init_solo`` too — suggestions
    just land under the project root even if the project is not yet
    fully initialized.

    Args:
        content: the suggestion body (plain text or markdown).
        context: optional short context line (e.g. "triggered while
            doing X"). Rendered as a separate block in the proposal
            file.

    Returns:
        Bilingual confirmation with the absolute path of the created
        file so ADMIN can open it directly.
    """
    try:
        project, _source = _get_project()
        proposal_path = project.drop_suggestion(content=content, context=context)
    except ValueError as exc:
        return f"错误：内容不能为空 / error: {exc}"
    except fcop.FcopError as exc:
        return f"错误：{exc} / error: {exc}"

    return (
        f"建议已记录 / suggestion recorded: `{proposal_path}`\n\n"
        "ADMIN 会稍后审阅。感谢反馈。\n"
        "ADMIN will review this later. Thanks for the feedback."
    )


# ─── Protocol meta tools ─────────────────────────────────────────────


# ── Rule version drift detection (ADR-0006) ──────────────────────────


_LOCAL_RULES_PATH = Path(".cursor") / "rules" / "fcop-rules.mdc"
_LOCAL_PROTOCOL_PATH = Path(".cursor") / "rules" / "fcop-protocol.mdc"


def _read_local_frontmatter_version(file_path: Path, key: str) -> str | None:
    """Pull a ``key: <semver>`` line out of a local .mdc's frontmatter.

    Mirrors the same regex shape ``fcop.rules._extract_frontmatter_version``
    uses, but kept private here so we don't import a module-private
    helper across the package boundary. Returns ``None`` for missing
    files, missing fields, or unparseable content — every failure mode
    collapses into "no local version detected", which the caller
    surfaces as a "couldn't read" hint rather than a hard error.
    """
    try:
        text = file_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    pattern = re.compile(
        r"^" + re.escape(key) + r"\s*:\s*['\"]?([^'\"\s]+)['\"]?\s*$",
        re.MULTILINE,
    )
    match = pattern.search(text)
    return match.group(1) if match else None


def _semver_tuple(version: str | None) -> tuple[int, int, int] | None:
    """Best-effort semver parse for comparison only.

    Returns ``None`` for ``None`` or for strings that don't start with
    ``X.Y.Z`` integers — pre-release suffixes (``-rc1``, ``+build``)
    are ignored so a 1.5.0-rc1 is treated as 1.5.0 for drift purposes.
    """
    if version is None:
        return None
    match = re.match(r"^\s*(\d+)\.(\d+)\.(\d+)", version)
    if not match:
        return None
    return (int(match.group(1)), int(match.group(2)), int(match.group(3)))


def _format_versions_block(project_path: Path, *, is_en: bool) -> str:
    """Render the ``[Versions]`` section + optional drift warning.

    Always shows: fcop-mcp, fcop, rules (project-local | packaged),
    protocol (project-local | packaged). Appends a one-paragraph
    warning when the local rules or protocol version is older than
    the packaged one — that's the ADMIN-facing prompt to call
    ``redeploy_rules()``. Newer-than-packaged is rendered as a neutral
    note (could happen when ADMIN has manually edited or a downgrade
    is in progress); we don't push an action because there's no safe
    automated remedy.
    """
    from fcop_mcp._version import __version__ as mcp_version

    pkg_rules = fcop.rules.get_rules_version()
    pkg_protocol = fcop.rules.get_protocol_version()
    local_rules = _read_local_frontmatter_version(
        project_path / _LOCAL_RULES_PATH, "fcop_rules_version"
    )
    local_protocol = _read_local_frontmatter_version(
        project_path / _LOCAL_PROTOCOL_PATH, "fcop_protocol_version"
    )

    def render_pair(local: str | None, packaged: str) -> str:
        if local is None:
            return f"(not deployed) | packaged {packaged}" if is_en \
                else f"（项目本地未部署）| 包内 {packaged}"
        local_t = _semver_tuple(local)
        packaged_t = _semver_tuple(packaged)
        if local_t is None or packaged_t is None or local_t == packaged_t:
            mark = "✓" if local == packaged else "?"
            return (
                f"local {local} | packaged {packaged} {mark}"
                if is_en
                else f"项目本地 {local} | 包内 {packaged} {mark}"
            )
        if local_t < packaged_t:
            return (
                f"local {local} | packaged {packaged} (OUTDATED)"
                if is_en
                else f"项目本地 {local} | 包内 {packaged} (本地偏旧)"
            )
        return (
            f"local {local} | packaged {packaged} (newer than package)"
            if is_en
            else f"项目本地 {local} | 包内 {packaged} (本地比包还新)"
        )

    rules_line = render_pair(local_rules, pkg_rules)
    protocol_line = render_pair(local_protocol, pkg_protocol)

    if is_en:
        body = (
            "[Versions]\n"
            f"  fcop-mcp:  {mcp_version}\n"
            f"  fcop:      {fcop.__version__}\n"
            f"  rules:     {rules_line}\n"
            f"  protocol:  {protocol_line}"
        )
    else:
        body = (
            "[版本 / Versions]\n"
            f"  fcop-mcp:  {mcp_version}\n"
            f"  fcop:      {fcop.__version__}\n"
            f"  rules:     {rules_line}\n"
            f"  protocol:  {protocol_line}"
        )

    drift_lines: list[str] = []
    rules_drift = (
        _semver_tuple(local_rules) is not None
        and _semver_tuple(pkg_rules) is not None
        and _semver_tuple(local_rules) < _semver_tuple(pkg_rules)  # type: ignore[operator]
    )
    protocol_drift = (
        _semver_tuple(local_protocol) is not None
        and _semver_tuple(pkg_protocol) is not None
        and _semver_tuple(local_protocol) < _semver_tuple(pkg_protocol)  # type: ignore[operator]
    )
    if rules_drift or protocol_drift:
        if is_en:
            drift_lines.append(
                "\n  ⚠ Project-local protocol files are older than the "
                "installed package."
            )
            drift_lines.append(
                "    ADMIN, please run `redeploy_rules()` to refresh "
                ".cursor/rules/*.mdc + AGENTS.md + CLAUDE.md."
            )
            drift_lines.append(
                "    Old files are archived to "
                ".fcop/migrations/<timestamp>/rules/. Agents must NOT "
                "invoke redeploy_rules themselves."
            )
        else:
            drift_lines.append(
                "\n  ⚠ 项目本地协议规则文件比已安装包旧。"
            )
            drift_lines.append(
                "    ADMIN 请调用 `redeploy_rules()` 升级 "
                ".cursor/rules/*.mdc + AGENTS.md + CLAUDE.md。"
            )
            drift_lines.append(
                "    旧文件会归档到 .fcop/migrations/<时间戳>/rules/。"
                "Agent 不得自行调用 redeploy_rules。"
            )

    return body + ("\n" + "\n".join(drift_lines) if drift_lines else "")


def _compose_session_report(lang: str) -> str:
    """Build the `fcop_report` / `unbound_report` body.

    Centralised so the new ``fcop_report`` tool and the deprecated
    ``unbound_report`` alias can both call it without code drift. The
    output structure mirrors the legacy ``unbound_report`` (two
    branches: not-initialized vs initialized-no-role) and inserts a
    ``[Versions]`` block on each branch, with an ADR-0006 drift
    warning when the project-local rules or protocol version is
    older than the wheel-bundled one.
    """
    is_en = lang.lower().startswith("en")
    try:
        project, source = _get_project()
        status = project.status()
    except fcop.FcopError as exc:
        return _format_error(exc)

    project_path = str(status.path)
    versions_block = _format_versions_block(status.path, is_en=is_en)

    if not status.is_initialized:
        teams = fcop.teams.get_available_teams()
        roster = "\n".join(
            f"  - {info.name} — roles: {', '.join(info.roles)}, leader: {info.leader}"
            for info in teams
        )
        if is_en:
            return (
                "=== FCoP Initialization Report ===\n"
                f"Project path: {project_path}\n"
                f"Source: {source}\n"
                "Status: NOT initialized (docs/agents/fcop.json missing)\n\n"
                f"{versions_block}\n\n"
                "Available init modes:\n"
                f"{roster}\n"
                "  - solo (one role, direct ADMIN ↔ AI, no dispatch)\n"
                "  - custom (your own roles)\n\n"
                "ADMIN, pick ONE — the agent MUST NOT default this:\n"
                "  - init_project(team=\"dev-team\", lang=\"en\")\n"
                "  - init_solo(role_code=\"ME\", lang=\"en\")\n"
                '  - create_custom_team(team_name="...", roles="A,B,C", '
                'leader="A", lang="en")\n\n'
                "If you (ADMIN) are unsure, ask the agent to read you the "
                "manual first: it lives at MCP resource `fcop://letter/en` "
                "(or after init at `docs/agents/LETTER-TO-ADMIN.md`).\n\n"
                "STOP HERE. Do not claim a role; do not write any file "
                "other than via the init tools above; do not pick an init "
                "mode on ADMIN's behalf."
            )
        return (
            "=== FCoP 初始化汇报 ===\n"
            f"项目路径 / path: {project_path}\n"
            f"来源 / source: {source}\n"
            "状态 / status: 未初始化（docs/agents/fcop.json 不存在）\n\n"
            f"{versions_block}\n\n"
            "可选初始化方式：\n"
            f"{roster}\n"
            "  - solo（一个角色，直接对 ADMIN，不做派发）\n"
            "  - 自定义（你自己的角色列表）\n\n"
            "ADMIN 请从下面三选一 —— Agent 不允许替 ADMIN 默认：\n"
            "  - init_project(team=\"dev-team\", lang=\"zh\")\n"
            "  - init_solo(role_code=\"ME\", lang=\"zh\")\n"
            '  - create_custom_team(team_name="...", roles="A,B,C", '
            'leader="A", lang="zh")\n\n'
            "如果 ADMIN 拿不准选哪个，请先让 Agent 读说明书给你听："
            "MCP 资源 `fcop://letter/zh`（或初始化后 "
            "`docs/agents/LETTER-TO-ADMIN.md`）。\n\n"
            "本会话到此为止。不要自认角色；除上述 init 工具外不要写任何文件；"
            "也不要替 ADMIN 选初始化模式。"
        )

    cfg = status.config
    assert cfg is not None
    recent = status.recent_activity[:3]
    activity_lines = "\n".join(
        f"  - [{e.kind}] {e.filename} — {e.summary}" for e in recent
    ) or "  (none yet)"
    occupancy_lines = _format_role_occupancy(project, is_en=is_en)
    drift_lines = _format_drift_summary(project, is_en=is_en)

    if is_en:
        return (
            "=== FCoP UNBOUND Report ===\n"
            f"Project: {project_path}  (source: {source})\n"
            f"Team: {cfg.team}  Leader: {cfg.leader}  Lang: {cfg.lang}\n"
            f"Roles: {', '.join(cfg.roles)}\n\n"
            f"{versions_block}\n\n"
            f"Tasks: {status.tasks_open} open, {status.tasks_archived} archived\n"
            f"Reports: {status.reports_count}  Issues: {status.issues_count}\n\n"
            "Recent activity:\n"
            f"{activity_lines}\n\n"
            "Role occupancy (from on-disk ledger):\n"
            f"{occupancy_lines}\n\n"
            "Drift audit (Rule 0.a.1 + Rule 1, since 0.7.1):\n"
            f"{drift_lines}\n\n"
            "ADMIN: assign a role with the literal sentence:\n"
            '  "You are <ROLE> on <team>, thread <thread_key> (optional)"\n\n'
            "Until then this session MUST NOT:\n"
            "  - read task bodies (metadata only)\n"
            "  - write any file\n"
            "  - claim a role from context\n"
            "  - dispatch follow-up tasks\n\n"
            "Before transitioning to BOUND, cross-check the assigned role against\n"
            "the 'Role occupancy' table above (Rule 1 + protocol 1.5.0):\n"
            "  - UNUSED / ARCHIVED  → safe to BOUND\n"
            "  - ACTIVE, same session_id  → resume / safe to BOUND\n"
            "  - ACTIVE, different session_id  → STOP. Refuse under Rule 8,\n"
            "    drop a note in .fcop/proposals/double-bind-{ts}.md, and\n"
            "    return three options to ADMIN: handoff / co-review / distinct\n"
            "    role. Do NOT 'temporarily' share the role code.\n\n"
            "Once ADMIN binds you to a role, EVERY incoming request runs through\n"
            "the Rule 0.a.1 four-step cycle — there is no 'simple = skip' exception:\n"
            "  Step 1  write_task(sender=\"ADMIN\", recipient=\"<your role>\", ...)\n"
            "          ← BEFORE editing any file\n"
            "  Step 2  do the work (new_workspace + edit files in workspace/<slug>/)\n"
            "  Step 3  write_report(task_id=\"TASK-...\", reporter=\"<your role>\", ...)\n"
            "          ← BEFORE telling ADMIN \"done\" in chat\n"
            "  Step 4  archive_task(\"TASK-...\")  (after ADMIN accepts)\n"
            "Skipping Step 1 or Step 3 violates Rule 0.a.1."
        )
    return (
        "=== FCoP UNBOUND 报告 ===\n"
        f"项目 / project: {project_path}  (来源: {source})\n"
        f"团队 / team: {cfg.team}  负责人 / leader: {cfg.leader}  lang: {cfg.lang}\n"
        f"角色 / roles: {', '.join(cfg.roles)}\n\n"
        f"{versions_block}\n\n"
        f"任务 tasks: {status.tasks_open} 进行中, {status.tasks_archived} 已归档\n"
        f"报告 reports: {status.reports_count}  问题 issues: {status.issues_count}\n\n"
        "最近活动 / recent activity:\n"
        f"{activity_lines}\n\n"
        "角色占用（来自磁盘账本） / role occupancy:\n"
        f"{occupancy_lines}\n\n"
        "漂移审计 / drift audit（Rule 0.a.1 + Rule 1，自 0.7.1 起）：\n"
        f"{drift_lines}\n\n"
        "ADMIN 请用这句话给本会话分配角色：\n"
        "  「你是 <ROLE>，在 <team>，线程 <thread_key>（可选）」\n\n"
        "在此之前，本会话禁止：\n"
        "  - 读取任务正文（只看元数据）\n"
        "  - 写入任何文件\n"
        "  - 从上下文自认角色\n"
        "  - 派发后续任务\n\n"
        "转 BOUND 之前，请把指派的角色码与上面的「角色占用」表对照\n"
        "（Rule 1 + 协议 1.5.0）：\n"
        "  - UNUSED / ARCHIVED  → 可安全 BOUND\n"
        "  - ACTIVE 且 session_id 与本会话一致 → 同一 agent 重连，可 BOUND\n"
        "  - ACTIVE 但 session_id 不一致 → 停。按 Rule 8 拒绝绑定，向\n"
        "    .fcop/proposals/double-bind-{时间戳}.md 落一份冲突说明，\n"
        "    把三选一交还 ADMIN：交班 / 协审 / 改派一个未占用角色码。\n"
        "    不要「临时顶一下」——本协议里没有这种合法状态。\n\n"
        "ADMIN 把你绑定到角色之后，**每一条**新需求都要走 Rule 0.a.1 4 步循环——\n"
        "没有「简单任务可跳过」这种例外：\n"
        "  第 1 步  write_task(sender=\"ADMIN\", recipient=\"<你的角色>\", ...)\n"
        "           ← 在动手写任何文件之前\n"
        "  第 2 步  做事（new_workspace + 在 workspace/<slug>/ 下落产物）\n"
        "  第 3 步  write_report(task_id=\"TASK-...\", reporter=\"<你的角色>\", ...)\n"
        "           ← 在聊天里说「做完了」之前\n"
        "  第 4 步  archive_task(\"TASK-...\")（ADMIN 验收后）\n"
        "跳过第 1 步或第 3 步即违反 Rule 0.a.1。"
    )


def _format_drift_summary(
    project: fcop.Project, *, is_en: bool
) -> str:
    """Render the audit_drift summary as a multi-line block.

    Surfaces (a) working-tree files outside the FCoP ledger and
    (b) `session_id ↔ role` cross-role conflicts. Used by both
    `fcop_report()` (initialized branch, post 0.7.1) and the new
    `fcop_check()` tool. Stays compact — the full evidence list is
    available via `fcop_check()` itself.
    """
    try:
        report = project.audit_drift()
    except Exception as exc:  # noqa: BLE001 — best-effort audit
        if is_en:
            return f"  (audit_drift failed: {exc!r})"
        return f"  （audit_drift 失败：{exc!r}）"

    lines: list[str] = []
    if not report.git_available:
        lines.append(
            "  (git not available — drift check skipped)"
            if is_en
            else "  （未检测到 git，跳过 drift 检查）"
        )
    else:
        if report.entries:
            head = (
                f"  {len(report.entries)} drift file(s) outside FCoP ledger:"
                if is_en
                else f"  {len(report.entries)} 份文件在 FCoP 账本外漂移："
            )
            lines.append(head)
            for entry in report.entries[:8]:
                lines.append(f"    [{entry.status}] {entry.path}")
            remaining = len(report.entries) - 8
            if remaining > 0:
                lines.append(
                    f"    ... and {remaining} more (run fcop_check for the full list)"
                    if is_en
                    else f"    ……另有 {remaining} 份（调 fcop_check 看完整列表）"
                )
        else:
            lines.append(
                "  No working-tree drift outside the FCoP ledger."
                if is_en
                else "  工作树无漂移文件，全部修改都在 FCoP 账本内。"
            )

    if report.session_role_conflicts:
        head = (
            f"  ⚠ {len(report.session_role_conflicts)} session_id used under multiple roles:"
            if is_en
            else f"  ⚠ {len(report.session_role_conflicts)} 个 session_id 跨多个角色署名："
        )
        lines.append(head)
        for conflict in report.session_role_conflicts[:5]:
            lines.append(
                f"    {conflict.session_id} → roles: {', '.join(conflict.roles)} "
                f"({len(conflict.files)} files)"
            )
    else:
        lines.append(
            "  No session_id ↔ role conflicts detected."
            if is_en
            else "  未发现 session_id 跨角色冲突。"
        )

    return "\n".join(lines)


def _format_role_occupancy(project: fcop.Project, *, is_en: bool) -> str:
    """Render :meth:`fcop.Project.role_occupancy` as a fixed-width table.

    Backs the "Role occupancy" section of `fcop_report()` UNBOUND
    output (since fcop-mcp 0.7.0 / `fcop_protocol_version: 1.5.0`).
    Each line carries one role's status, counts, and the most recent
    `session_id` seen on disk so an UNBOUND agent can detect the
    double-bind scenario described in ISSUE-20260427-002 before
    transitioning to BOUND.
    """
    occupancies = project.role_occupancy()
    if not occupancies:
        return "  (no roles declared)" if is_en else "  （未声明任何角色）"

    lines: list[str] = []
    for occ in occupancies:
        sid = occ.last_session_id or ("none" if is_en else "无")
        when = (
            occ.last_seen_at.strftime("%Y-%m-%dT%H:%M")
            if occ.last_seen_at is not None
            else "—"
        )
        lines.append(
            f"  {occ.role:<10} {occ.status:<8} "
            f"tasks={occ.open_tasks} open / {occ.archived_tasks} archived  "
            f"reports={occ.open_reports}  issues={occ.open_issues}  "
            f"last: {sid} @ {when}"
        )
    return "\n".join(lines)


@mcp.tool
def fcop_report(lang: str = "zh") -> str:
    """**FCoP Rule 0 — first tool call of every new session, also the
    general project-status report.**

    Returns one of two reports plus a versions block + optional drift
    warning (ADR-0006):

    1. **Initialization report** when ``docs/agents/fcop.json`` is
       missing. Lists the detected project path + resolution source
       and the available init modes (Solo / preset teams / custom).
       Does NOT ask for a role assignment — there's no team yet.

    2. **UNBOUND report** when the project is initialized but this
       session has no role. Shows project state and a role-assignment
       template for ADMIN to fill in.

    In both cases the ``[Versions]`` block reports installed
    ``fcop-mcp`` / ``fcop`` versions plus the project-local vs
    packaged versions of the protocol rules. When the project's
    ``.cursor/rules/*.mdc`` is older than the wheel-bundled copy a
    drift warning is appended prompting ADMIN to run
    ``redeploy_rules()``. Agents must NOT invoke redeploy themselves.

    While UNBOUND (or uninitialized) the agent MUST NOT read task
    bodies, write any files (except via the explicit init tools), or
    claim a role from context clues.

    .. note::
        This tool replaced ``unbound_report`` in 0.6.3. The deprecated
        alias was removed in 0.7.0; existing system prompts and
        ``LETTER-TO-ADMIN.md`` references that still reference
        ``unbound_report`` must switch to ``fcop_report``.

    Args:
        lang: Output language, ``zh`` or ``en``. Default: ``zh``.
    """
    return _compose_session_report(lang)


@mcp.tool
def fcop_check(lang: str = "zh") -> str:
    """**FCoP audit.** Cross-reference git working tree + frontmatter
    against the FCoP ledger.

    Two independent post-hoc audits, both new in 0.7.1
    (``fcop_protocol_version: 1.6.0``):

    1. **Rule 0.a.1 drift** — files in ``git status --porcelain``
       that live outside ``docs/agents/{tasks,reports,issues,log}/``
       are by definition work performed without the
       task→do→report→archive cycle.
    2. **Rule 1 sub-agent role impersonation** — any ``session_id``
       that signed files under more than one role code. One session =
       one role binding for life; cross-role usage is direct evidence
       that a sub-agent self-claimed a role its parent session was
       not assigned.

    This tool is **detection, not prevention**. It surfaces the
    evidence; the protocol-mandated response is for ADMIN to file an
    ISSUE-* and decide handoff / co-review / distinct-role per
    Rule 1, just as for the ``role_occupancy`` table in
    ``fcop_report()``.

    Decomposes to filesystem operations:
    - ``git status --porcelain -z`` from the project root.
    - Walk every ``TASK-*.md`` / ``REPORT-*.md`` / ``ISSUE-*.md`` in
      ``docs/agents/{tasks,reports,issues}`` + ``docs/agents/log/*``.
    - Read frontmatter only; never task bodies.

    Args:
        lang: Output language, ``zh`` or ``en``. Default: ``zh``.
    """
    is_en = lang.lower().startswith("en")
    try:
        project, source = _get_project()
    except fcop.FcopError as exc:
        return _format_error(exc)

    if not project.is_initialized():
        return (
            "fcop_check requires an initialised project (docs/agents/fcop.json missing). "
            "Run init_project / init_solo / create_custom_team first."
            if is_en
            else "fcop_check 需要已初始化的项目（docs/agents/fcop.json 不存在）。"
            "请先用 init_project / init_solo / create_custom_team 初始化。"
        )

    try:
        report = project.audit_drift()
    except Exception as exc:  # noqa: BLE001
        return _format_error(exc)

    project_path = str(project.path)
    lines: list[str] = []
    if is_en:
        lines.append("=== FCoP Check (audit_drift) ===")
        lines.append(f"Project: {project_path}  (source: {source})")
        if not report.git_available:
            lines.append("git: NOT available (drift section skipped)")
        else:
            lines.append(
                f"git: OK — {len(report.entries)} drift file(s) outside FCoP ledger"
            )
        lines.append("")
        lines.append("--- Working-tree drift (Rule 0.a.1) ---")
        if not report.entries:
            lines.append("(none — every uncommitted change is inside the ledger)")
        else:
            for entry in report.entries:
                lines.append(f"  [{entry.status}] {entry.path}")
        lines.append("")
        lines.append("--- session_id ↔ role conflicts (Rule 1) ---")
        if not report.session_role_conflicts:
            lines.append("(none — every session signs files under exactly one role)")
        else:
            for conflict in report.session_role_conflicts:
                lines.append(
                    f"  {conflict.session_id}  →  roles: {', '.join(conflict.roles)}"
                )
                for fp in conflict.files:
                    try:
                        rel = fp.relative_to(project.path)
                    except ValueError:
                        rel = fp
                    lines.append(f"      {rel}")
        lines.append("")
        lines.append(
            "Detection only — file an ISSUE-*.md in docs/agents/issues/ and "
            "ask ADMIN to decide handoff / co-review / distinct-role per Rule 1."
        )
    else:
        lines.append("=== FCoP Check（audit_drift） ===")
        lines.append(f"项目 / project: {project_path}  （来源: {source}）")
        if not report.git_available:
            lines.append("git: 不可用（漂移段已跳过）")
        else:
            lines.append(
                f"git: OK —— FCoP 账本外漂移 {len(report.entries)} 份"
            )
        lines.append("")
        lines.append("--- 工作树漂移（Rule 0.a.1） ---")
        if not report.entries:
            lines.append("（无 —— 所有未提交修改都在 FCoP 账本内）")
        else:
            for entry in report.entries:
                lines.append(f"  [{entry.status}] {entry.path}")
        lines.append("")
        lines.append("--- session_id ↔ role 冲突（Rule 1） ---")
        if not report.session_role_conflicts:
            lines.append("（无 —— 每个 session 都只在一个角色名下署名）")
        else:
            for conflict in report.session_role_conflicts:
                lines.append(
                    f"  {conflict.session_id}  →  涉及角色: {', '.join(conflict.roles)}"
                )
                for fp in conflict.files:
                    try:
                        rel = fp.relative_to(project.path)
                    except ValueError:
                        rel = fp
                    lines.append(f"      {rel}")
        lines.append("")
        lines.append(
            "本工具只做检测，不阻塞写入。请把异常落成 docs/agents/issues/ISSUE-*.md，"
            "请 ADMIN 按 Rule 1 三选一裁决：交班 / 协审 / 改派。"
        )

    return "\n".join(lines)


@mcp.tool
def redeploy_rules(force: bool = True, archive: bool = True, lang: str = "zh") -> str:
    """**ADMIN-only.** Re-deploy bundled FCoP protocol rules to the project.

    Writes the wheel-bundled :file:`fcop-rules.mdc` /
    :file:`fcop-protocol.mdc` to **four** locations so any agent host
    the project runs under sees the same rules:

    .. code-block:: text

        <root>/.cursor/rules/fcop-rules.mdc       # Cursor IDE
        <root>/.cursor/rules/fcop-protocol.mdc    # Cursor IDE
        <root>/AGENTS.md                          # Codex / Cursor / Devin / generic
        <root>/CLAUDE.md                          # Claude Code CLI

    Run this **after** ``pip install -U fcop-mcp`` (or ``-U fcop``)
    to refresh on-disk copies to the newly packaged versions.
    ``fcop_report()`` shows when this is needed via the version
    drift warning.

    Per ADR-0006, agents must NOT invoke this tool themselves —
    only ADMIN does, explicitly.

    Args:
        force: When ``True`` (default) overwrite existing copies.
            ``False`` skips files that already exist (no-op for an
            up-to-date project).
        archive: When ``True`` (default) and ``force=True``, the
            existing copy is moved to
            :file:`.fcop/migrations/<timestamp>/rules/<rel>` before
            being overwritten so ADMIN can diff or roll back.
            ``False`` skips archiving (destructive — only safe when
            the project has no local edits).
        lang: Output language, ``zh`` or ``en``.
    """
    is_en = lang.lower().startswith("en")
    try:
        project, _source = _get_project()
        report = project.deploy_protocol_rules(force=force, archive=archive)
    except fcop.FcopError as exc:
        return _format_error(exc)

    deployed_count = len(report.deployed)
    skipped_count = len(report.skipped)
    archived_count = len(report.archived)

    if is_en:
        lines = [
            "=== FCoP Rule Redeployment ===",
            f"Project: {project.path}",
            f"Rules version (packaged):     {fcop.rules.get_rules_version()}",
            f"Protocol version (packaged):  {fcop.rules.get_protocol_version()}",
            "",
            f"Deployed: {deployed_count}",
        ]
        for path in report.deployed:
            lines.append(f"  + {path.relative_to(project.path)}")
        if skipped_count:
            lines.append(f"\nSkipped (already exist, force=False): {skipped_count}")
            for path in report.skipped:
                lines.append(f"  - {path.relative_to(project.path)}")
        if archived_count:
            lines.append(f"\nArchived: {archived_count}")
            archive_root = report.migration_dir
            if archive_root is not None:
                lines.append(f"  Migration dir: {archive_root.relative_to(project.path)}")
        lines.append(
            "\nAgent hosts will pick up the new rules on next session restart "
            "(Cursor: reload window; Claude Code: restart CLI; Codex: restart task)."
        )
        return "\n".join(lines)

    lines = [
        "=== FCoP 协议规则重新部署 ===",
        f"项目 / project: {project.path}",
        f"包内 rules 版本:    {fcop.rules.get_rules_version()}",
        f"包内 protocol 版本: {fcop.rules.get_protocol_version()}",
        "",
        f"已部署 / deployed: {deployed_count}",
    ]
    for path in report.deployed:
        lines.append(f"  + {path.relative_to(project.path)}")
    if skipped_count:
        lines.append(f"\n已跳过（force=False 且文件已存在）: {skipped_count}")
        for path in report.skipped:
            lines.append(f"  - {path.relative_to(project.path)}")
    if archived_count:
        lines.append(f"\n已归档 / archived: {archived_count}")
        archive_root = report.migration_dir
        if archive_root is not None:
            lines.append(
                f"  归档目录 / migration dir: "
                f"{archive_root.relative_to(project.path)}"
            )
    lines.append(
        "\nAgent host 重启后才会读到新规则（Cursor: 重载窗口；"
        "Claude Code: 重启 CLI；Codex: 重启任务）。"
    )
    return "\n".join(lines)


@mcp.tool
def check_update(lang: str = "zh") -> str:
    """Compare the installed fcop-mcp version to the latest on PyPI.

    Prints the local version, the latest PyPI version (if reachable),
    and a one-line verdict. Does NOT install anything — call
    ``upgrade_fcop`` afterwards for that.

    Args:
        lang: Output language, ``zh`` or ``en``.
    """
    import urllib.error
    import urllib.request

    from fcop_mcp._version import __version__ as local_version

    is_en = lang.lower().startswith("en")
    url = "https://pypi.org/pypi/fcop-mcp/json"
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:  # noqa: S310
            payload = json.loads(resp.read().decode("utf-8"))
        latest = str(payload.get("info", {}).get("version", "")) or "(unknown)"
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return (
            f"Could not reach PyPI: {exc}\n"
            f"Local fcop-mcp version: {local_version}"
            if is_en
            else f"无法访问 PyPI: {exc}\n本地 fcop-mcp 版本: {local_version}"
        )

    fcop_local = fcop.__version__
    if local_version == latest:
        verdict = (
            f"Up to date: fcop-mcp=={local_version} (fcop library=={fcop_local})"
            if is_en
            else f"已是最新: fcop-mcp=={local_version} (fcop 库=={fcop_local})"
        )
    else:
        verdict = (
            f"Update available: {local_version} → {latest}\n"
            f"Library stays at: fcop=={fcop_local}\n"
            "Run `upgrade_fcop` for install hints."
            if is_en
            else f"有可升级版本: {local_version} → {latest}\n"
            f"底层库版本: fcop=={fcop_local}\n"
            "调用 `upgrade_fcop` 查看具体升级命令。"
        )
    return verdict


@mcp.tool
def upgrade_fcop(lang: str = "zh") -> str:
    """Return the install-method-specific command to upgrade fcop-mcp.

    Does NOT run pip — MCP servers cannot safely upgrade themselves
    mid-process, and different install methods (``pip`` in a venv,
    ``pipx``, ``uvx``) need different commands. This tool prints the
    right incantation for the user to run in their own shell.

    Args:
        lang: Output language, ``zh`` or ``en``.
    """
    from fcop_mcp._version import __version__ as local_version

    is_en = lang.lower().startswith("en")
    env_hint = ""
    if "uvx" in (os.environ.get("PATH", "") or "").lower():
        env_hint = "Detected 'uvx' on PATH — likely a uvx install.\n"
    if is_en:
        return (
            f"Current version: fcop-mcp=={local_version}\n"
            f"Underlying library: fcop=={fcop.__version__}\n\n"
            f"{env_hint}"
            "Upgrade commands (run in YOUR shell, outside the MCP process):\n"
            "  uvx:   (automatic on next MCP restart — no action needed)\n"
            "  pipx:  pipx upgrade fcop-mcp\n"
            "  pip:   pip install --upgrade fcop-mcp\n\n"
            "After the upgrade, restart your MCP client (Cursor / Claude "
            "Desktop) so it reloads the new process."
        )
    return (
        f"当前版本: fcop-mcp=={local_version}\n"
        f"底层库: fcop=={fcop.__version__}\n\n"
        f"{env_hint}"
        "升级命令（在你自己的终端里跑，不是在 MCP 里）：\n"
        "  uvx:   下次 MCP 重启自动生效，无需操作\n"
        "  pipx:  pipx upgrade fcop-mcp\n"
        "  pip:   pip install --upgrade fcop-mcp\n\n"
        "升级完重启 MCP 客户端（Cursor / Claude Desktop），让它重新加载进程。"
    )


# ─── MCP resources ───────────────────────────────────────────────────
#
# Resources expose read-only content via `fcop://...` URIs. Cursor and
# other clients typically attach these to the context window on
# demand. The shapes below are locked by ADR-0003: URI template, MIME
# type, and the fact that each returns a text document are
# additive-only for the 0.6.x series.


@mcp.resource("fcop://status", mime_type="text/markdown")
def resource_status() -> str:
    """Project status snapshot (same data as :func:`get_team_status`)."""
    return get_team_status()


@mcp.resource("fcop://config", mime_type="application/json")
def resource_config() -> str:
    """Raw contents of ``docs/agents/fcop.json`` when the project is initialized."""
    try:
        project, _source = _get_project()
        cfg_path = project.config_path
        if not cfg_path.exists():
            return json.dumps({"initialized": False, "path": str(project.path)})
        return cfg_path.read_text(encoding="utf-8")
    except fcop.FcopError as exc:
        return json.dumps({"error": str(exc)})


@mcp.resource("fcop://rules", mime_type="text/markdown")
def resource_rules() -> str:
    """FCoP protocol rules (``fcop-rules.mdc``)."""
    return fcop.rules.get_rules()


@mcp.resource("fcop://protocol", mime_type="text/markdown")
def resource_protocol() -> str:
    """FCoP protocol commentary (``fcop-protocol.mdc``)."""
    return fcop.rules.get_protocol_commentary()


@mcp.resource("fcop://letter/zh", mime_type="text/markdown")
def resource_letter_zh() -> str:
    """Chinese Letter-to-ADMIN user manual."""
    return fcop.rules.get_letter("zh")


@mcp.resource("fcop://letter/en", mime_type="text/markdown")
def resource_letter_en() -> str:
    """English Letter-to-ADMIN user manual."""
    return fcop.rules.get_letter("en")


@mcp.resource("fcop://prompt/install", mime_type="text/markdown")
def resource_install_prompt_zh() -> str:
    """Canonical "have an agent install fcop-mcp" prompt (Chinese).

    Same text as the bundled ``agent-install-prompt.zh.md`` and the
    ``mcp/README.md`` § "Have an agent install fcop-mcp for you"
    section. ADMIN copies this and gives it to a fresh shell-capable
    agent. The prompt body explicitly forbids agents from
    auto-initialising a project after install — initialisation is
    ADMIN's three-way choice (solo / preset team / custom).
    """
    return fcop.rules.get_install_prompt("zh")


@mcp.resource("fcop://prompt/install/en", mime_type="text/markdown")
def resource_install_prompt_en() -> str:
    """Canonical "have an agent install fcop-mcp" prompt (English).

    English variant of ``fcop://prompt/install``. Same content as
    the bundled ``agent-install-prompt.en.md``.
    """
    return fcop.rules.get_install_prompt("en")


@mcp.resource("fcop://teams", mime_type="application/json")
def resource_teams_index() -> str:
    """JSON index of all bundled teams with name / roles / leader."""
    teams = fcop.teams.get_available_teams()
    data = [
        {"name": t.name, "roles": list(t.roles), "leader": t.leader}
        for t in teams
    ]
    return json.dumps({"teams": data}, ensure_ascii=False, indent=2)


@mcp.resource("fcop://teams/{team}", mime_type="text/markdown")
def resource_team_readme(team: str) -> str:
    """Team-level README (Chinese variant)."""
    try:
        template = fcop.teams.get_template(team, "zh")
    except fcop.TeamNotFoundError as exc:
        return f"# Team not found: {team}\n\n{exc}"
    return template.readme


@mcp.resource("fcop://teams/{team}/{role}", mime_type="text/markdown")
def resource_team_role_zh(team: str, role: str) -> str:
    """Role-level bio for one team member (Chinese variant)."""
    try:
        template = fcop.teams.get_template(team, "zh")
    except fcop.TeamNotFoundError as exc:
        return f"# Team not found: {team}\n\n{exc}"
    role_up = role.upper()
    text = template.roles.get(role_up)
    if text is None:
        known = ", ".join(sorted(template.roles)) or "(none)"
        return (
            f"# Role not found: {role_up} in team {team}\n\n"
            f"Known roles: {known}"
        )
    return text


@mcp.resource("fcop://teams/{team}/{role}/en", mime_type="text/markdown")
def resource_team_role_en(team: str, role: str) -> str:
    """Role-level bio for one team member (English variant)."""
    try:
        template = fcop.teams.get_template(team, "en")
    except fcop.TeamNotFoundError as exc:
        return f"# Team not found: {team}\n\n{exc}"
    role_up = role.upper()
    text = template.roles.get(role_up)
    if text is None:
        known = ", ".join(sorted(template.roles)) or "(none)"
        return (
            f"# Role not found: {role_up} in team {team}\n\n"
            f"Known roles: {known}"
        )
    return text
