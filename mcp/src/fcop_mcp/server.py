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

import os
import sys
import threading
from pathlib import Path

import fcop
from fastmcp import FastMCP
from fcop import Project

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
