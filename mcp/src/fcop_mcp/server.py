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
``fcop 0.5.4`` (née ``codeflow-plugin/src/fcop/server.py``). Names and
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


def _parse_roles_list(roles: str) -> list[str]:
    """Split a comma-separated role-code string into normalized uppercase codes."""
    return [r.strip().upper() for r in roles.split(",") if r.strip()]


def _parse_refs_list(references: str) -> tuple[str, ...]:
    """Split a comma-separated references string into a tuple."""
    if not references:
        return ()
    return tuple(r.strip() for r in references.split(",") if r.strip())


# ─── init_* tools ────────────────────────────────────────────────────


@mcp.tool
def init_project(team: str = "dev-team", lang: str = "zh") -> str:
    """Initialize an FCoP project with a bundled preset team.

    Creates ``docs/agents/`` (tasks / reports / issues / shared / log),
    writes ``docs/agents/fcop.json``, drops the bundled protocol rules
    into ``.cursor/rules/``, and deploys the team's three-layer role
    documentation. Idempotent when the project is already initialized
    (re-running returns the existing status without clobbering files);
    use ``force`` from the library API if you need overwrite behaviour.

    Args:
        team: Team template ID. One of ``dev-team`` / ``media-team`` /
            ``mvp-team`` / ``qa-team``. Default: ``dev-team``.
        lang: Output language. ``zh`` or ``en``. Default: ``zh``.

    Returns:
        Post-init summary with roster, leader, and directory layout.
    """
    try:
        project, _source = _get_project()
        status = project.init(team=team, lang=lang)
    except fcop.ProjectAlreadyInitializedError as exc:
        return f"项目已初始化 / already initialized: {exc}"
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
        "",
        "下一步 / next: unbound_report 查看状态后，"
        "由 ADMIN 通过『你是 <ROLE>』语句为本会话分配角色。",
    ]
    return "\n".join(lines)


@mcp.tool
def init_solo(role_code: str = "ME", role_label: str = "", lang: str = "zh") -> str:
    """Initialize an FCoP project in **Solo mode** (one AI, no dispatch).

    Solo mode is for projects where a single agent works directly with
    ADMIN. Rule 0.b still applies: the agent uses files to split itself
    into *proposer* and *reviewer*, even though there is no second role.

    Args:
        role_code: The single role code (uppercase letters / digits /
            underscore, must start with a letter; ``ADMIN`` and
            ``SYSTEM`` are reserved). Default: ``ME``.
        role_label: Display label (e.g. ``"我自己"``). Currently
            recorded in ``extra`` for future use; the library does not
            yet consume it. Safe to omit.
        lang: Output language, ``zh`` or ``en``.
    """
    try:
        project, _source = _get_project()
        status = project.init_solo(role_code=role_code, lang=lang)
    except fcop.ProjectAlreadyInitializedError as exc:
        return f"项目已初始化 / already initialized: {exc}"
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
        f"Directories: tasks/, reports/, issues/, shared/, log/"
    )


@mcp.tool
def create_custom_team(
    team_name: str,
    roles: str,
    leader: str,
    lang: str = "zh",
) -> str:
    """Create an FCoP project with a custom roster of roles.

    Role codes can be anything — they become part of task filenames,
    e.g. ``TASK-20260423-001-BOSS-to-CODER.md``. Use ``validate_team_config``
    first to catch illegal role codes without writing anything.

    Args:
        team_name: Display name for the team (e.g. ``"My Design Studio"``).
        roles: Comma-separated role codes (e.g. ``"BOSS,CODER,TESTER"``).
        leader: Leader role code; must appear in ``roles``.
        lang: Output language, ``zh`` or ``en``.
    """
    role_list = _parse_roles_list(roles)
    try:
        project, _source = _get_project()
        status = project.init_custom(
            team_name=team_name,
            roles=role_list,
            leader=leader.strip().upper(),
            lang=lang,
        )
    except fcop.ProjectAlreadyInitializedError as exc:
        return f"项目已初始化 / already initialized: {exc}"
    except fcop.FcopError as exc:
        return _format_error(exc)

    cfg = status.config
    assert cfg is not None
    return (
        f"Custom team created: {team_name}\n"
        f"Path: {status.path}\n"
        f"Roles: {', '.join(cfg.roles)}\n"
        f"Leader: {cfg.leader}\n"
        f"Lang: {cfg.lang}"
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

    return f"Task created: {task.filename}\nPath: {task.path}"


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

    return f"Report created: {report.filename}\nPath: {report.path}"


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

    return f"Issue created: {issue.filename}\nPath: {issue.path}"


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
    return (
        f"{verb} workspace: `{rel}/`\n"
        f"  slug: {slug_norm}\n"
        f"  title: {title.strip() or '(none)'}\n"
        f"  created_at: {created_at}\n\n"
        f"{verb} workspace at `{rel}/`. Put code / scripts / data here; "
        "do not write to the project root."
    )


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


@mcp.tool
def unbound_report(lang: str = "zh") -> str:
    """**FCoP v1.1 Rule 0 — first tool call of every new session.**

    Returns one of two reports:

    1. **Initialization report** when ``docs/agents/fcop.json`` is
       missing. Lists the detected project path + resolution source
       and the available init modes (Solo / preset teams / custom).
       Does NOT ask for a role assignment — there's no team yet.

    2. **UNBOUND report** when the project is initialized but this
       session has no role. Shows project state and a role-assignment
       template for ADMIN to fill in.

    While UNBOUND (or uninitialized) the agent MUST NOT read task
    bodies, write any files (except via the explicit init tools), or
    claim a role from context clues.

    Args:
        lang: Output language, ``zh`` or ``en``. Default: ``zh``.
    """
    is_en = lang.lower().startswith("en")
    try:
        project, source = _get_project()
        status = project.status()
    except fcop.FcopError as exc:
        return _format_error(exc)

    project_path = str(status.path)
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
                "Available init modes:\n"
                f"{roster}\n"
                "  - solo (one role, direct ADMIN ↔ AI, no dispatch)\n"
                "  - custom (your own roles)\n\n"
                "ADMIN, pick ONE:\n"
                "  - init_project(team=\"dev-team\", lang=\"en\")\n"
                "  - init_solo(role_code=\"ME\", lang=\"en\")\n"
                '  - create_custom_team(team_name="...", roles="A,B,C", '
                'leader="A", lang="en")\n\n'
                "STOP HERE. Do not claim a role; do not write any file "
                "other than via the init tools above."
            )
        return (
            "=== FCoP 初始化汇报 ===\n"
            f"项目路径 / path: {project_path}\n"
            f"来源 / source: {source}\n"
            "状态 / status: 未初始化（docs/agents/fcop.json 不存在）\n\n"
            "可选初始化方式：\n"
            f"{roster}\n"
            "  - solo（一个角色，直接对 ADMIN，不做派发）\n"
            "  - 自定义（你自己的角色列表）\n\n"
            "ADMIN 请从下面三选一：\n"
            "  - init_project(team=\"dev-team\", lang=\"zh\")\n"
            "  - init_solo(role_code=\"ME\", lang=\"zh\")\n"
            '  - create_custom_team(team_name="...", roles="A,B,C", '
            'leader="A", lang="zh")\n\n'
            "本会话到此为止。不要自认角色；除上述 init 工具外不要写任何文件。"
        )

    cfg = status.config
    assert cfg is not None
    recent = status.recent_activity[:3]
    activity_lines = "\n".join(
        f"  - [{e.kind}] {e.filename} — {e.summary}" for e in recent
    ) or "  (none yet)"

    if is_en:
        return (
            "=== FCoP UNBOUND Report ===\n"
            f"Project: {project_path}  (source: {source})\n"
            f"Team: {cfg.team}  Leader: {cfg.leader}  Lang: {cfg.lang}\n"
            f"Roles: {', '.join(cfg.roles)}\n\n"
            f"Tasks: {status.tasks_open} open, {status.tasks_archived} archived\n"
            f"Reports: {status.reports_count}  Issues: {status.issues_count}\n\n"
            "Recent activity:\n"
            f"{activity_lines}\n\n"
            "ADMIN: assign a role with the literal sentence:\n"
            '  "You are <ROLE> on <team>, thread <thread_key> (optional)"\n\n'
            "Until then this session MUST NOT:\n"
            "  - read task bodies (metadata only)\n"
            "  - write any file\n"
            "  - claim a role from context\n"
            "  - dispatch follow-up tasks"
        )
    return (
        "=== FCoP UNBOUND 报告 ===\n"
        f"项目 / project: {project_path}  (来源: {source})\n"
        f"团队 / team: {cfg.team}  负责人 / leader: {cfg.leader}  lang: {cfg.lang}\n"
        f"角色 / roles: {', '.join(cfg.roles)}\n\n"
        f"任务 tasks: {status.tasks_open} 进行中, {status.tasks_archived} 已归档\n"
        f"报告 reports: {status.reports_count}  问题 issues: {status.issues_count}\n\n"
        "最近活动 / recent activity:\n"
        f"{activity_lines}\n\n"
        "ADMIN 请用这句话给本会话分配角色：\n"
        "  「你是 <ROLE>，在 <team>，线程 <thread_key>（可选）」\n\n"
        "在此之前，本会话禁止：\n"
        "  - 读取任务正文（只看元数据）\n"
        "  - 写入任何文件\n"
        "  - 从上下文自认角色\n"
        "  - 派发后续任务"
    )


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
