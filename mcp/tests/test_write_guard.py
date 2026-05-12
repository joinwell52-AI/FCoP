"""Tests for fcop-mcp write-side binding guard (D1 + D2 + S1–S3, TASK-001/002).

Scenarios covered:
  TC-01  Call write-side tool with no binding → WriteRefused (D1)
  TC-02  Call write-side tool bound to USER HOME via set_project_dir → WriteRefused (D2)
  TC-03  Call write-side tool bound to drive root → WriteRefused (D2)
  TC-04  Call write-side tool bound to legal project dir → succeeds (requires fcop.json)
  TC-05  _is_protected_path() deny-list logic
  TC-06  Integration: replicates PM #50 incident (cwd = home, no binding)
  TC-07  binding_required tag present on all write-side tools
  TC-08  fcop_report() shows protected-path warning when path is home dir
  TC-09  S1: write-side (non-init) tool refuses when fcop.json missing
  TC-10  S1: init tools exempt from fcop.json check
  TC-11  S2: HOME subdirectory is allowed (only exact HOME refused)
  TC-12  S3: parametrize — all write-side tools share consistent guard behaviour
"""

from __future__ import annotations

import os
import sys
import threading
from pathlib import Path
from unittest.mock import patch

import pytest

import fcop_mcp.server as srv


# ─── helpers ─────────────────────────────────────────────────────────────────


def _reset_session() -> None:
    """Reset global session state between tests."""
    with srv._STATE_LOCK:
        srv._SESSION_PROJECT_PATH = None
        srv._SESSION_PROJECT_SOURCE = "uninitialized"


def _home_path() -> Path:
    home = os.environ.get("USERPROFILE") or os.environ.get("HOME") or "~"
    return Path(home).expanduser().resolve()


# ─── TC-01: no explicit binding → cwd fallback → WriteRefused ────────────────


def test_tc01_no_binding_cwd_fallback_raises_write_refused(tmp_path: Path) -> None:
    """write-side tools must refuse when only cwd fallback is available."""
    _reset_session()
    # Use tmp_path as cwd — it has no fcop marker files, so the resolver falls
    # back to "cwd fallback (no markers; ...)" which is a cwd fallback → D1 fires.
    env_patch = {k: v for k, v in os.environ.items()
                 if k not in ("FCOP_PROJECT_DIR", "CODEFLOW_PROJECT_DIR")}
    with patch.dict(os.environ, env_patch, clear=True):
        with patch.object(Path, "cwd", return_value=tmp_path):
            with pytest.raises(ValueError, match="WriteRefused"):
                srv._assert_writable_project("write_task")


def test_tc01_home_cwd_fallback_raises_write_refused() -> None:
    """cwd = home dir → WriteRefused even without explicit deny-list hit."""
    _reset_session()
    home = _home_path()
    env_patch = {k: v for k, v in os.environ.items()
                 if k not in ("FCOP_PROJECT_DIR", "CODEFLOW_PROJECT_DIR")}
    with patch.dict(os.environ, env_patch, clear=True):
        with patch.object(Path, "cwd", return_value=home):
            with pytest.raises(ValueError, match="WriteRefused"):
                srv._assert_writable_project("redeploy_rules")


# ─── TC-02: bound to USER HOME via set_project_dir → WriteRefused (D2) ───────


def test_tc02_explicit_bind_to_home_refused(tmp_path: Path) -> None:
    """Binding explicitly to USER HOME must be rejected (D2 deny-list)."""
    _reset_session()
    home = _home_path()
    with srv._STATE_LOCK:
        srv._SESSION_PROJECT_PATH = home
        srv._SESSION_PROJECT_SOURCE = "session:set_project_dir"
    try:
        with pytest.raises(ValueError, match="WriteRefused"):
            srv._assert_writable_project("redeploy_rules")
    finally:
        _reset_session()


# ─── TC-03: bound to drive root → WriteRefused (D2) ─────────────────────────


@pytest.mark.skipif(sys.platform != "win32", reason="Windows drive root test")
def test_tc03_explicit_bind_to_drive_root_refused() -> None:
    """Binding to a drive root (C:\\) must be rejected on Windows."""
    _reset_session()
    drive_root = Path("C:/").resolve()
    with srv._STATE_LOCK:
        srv._SESSION_PROJECT_PATH = drive_root
        srv._SESSION_PROJECT_SOURCE = "session:set_project_dir"
    try:
        with pytest.raises(ValueError, match="WriteRefused"):
            srv._assert_writable_project("init_project")
    finally:
        _reset_session()


# ─── TC-04: bound to valid project dir → succeeds ────────────────────────────


def test_tc04_valid_project_dir_allowed(tmp_path: Path) -> None:
    """Explicitly binding to a safe project directory with fcop.json must be accepted."""
    _reset_session()
    project_dir = tmp_path / "my_project"
    project_dir.mkdir()
    # Create fcop.json so S1 check passes
    (project_dir / "fcop").mkdir()
    (project_dir / "fcop" / "fcop.json").write_text('{"mode":"solo"}')
    with srv._STATE_LOCK:
        srv._SESSION_PROJECT_PATH = project_dir
        srv._SESSION_PROJECT_SOURCE = "session:set_project_dir"
    try:
        path, source = srv._assert_writable_project("write_task")
        assert path == project_dir
        assert "set_project_dir" in source
    finally:
        _reset_session()


# ─── TC-05: _is_protected_path() deny-list ───────────────────────────────────


def test_tc05_home_is_protected() -> None:
    assert srv._is_protected_path(_home_path()) is True


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific")
def test_tc05_drive_root_is_protected() -> None:
    assert srv._is_protected_path(Path("C:/").resolve()) is True


@pytest.mark.skipif(sys.platform == "win32", reason="Unix-specific")
def test_tc05_unix_root_is_protected() -> None:
    assert srv._is_protected_path(Path("/")) is True


@pytest.mark.skipif(sys.platform == "win32", reason="Unix-specific")
def test_tc05_unix_etc_is_protected() -> None:
    assert srv._is_protected_path(Path("/etc")) is True


def test_tc05_random_tmp_not_protected(tmp_path: Path) -> None:
    project = tmp_path / "project"
    project.mkdir()
    assert srv._is_protected_path(project) is False


# ─── TC-06: Integration — PM #50 incident replay ─────────────────────────────


def test_tc06_pm50_incident_replay() -> None:
    """Replicate the PM #50 incident: MCP cwd=home, no binding → redeploy_rules must fail."""
    _reset_session()
    home = _home_path()
    env_patch = {k: v for k, v in os.environ.items()
                 if k not in ("FCOP_PROJECT_DIR", "CODEFLOW_PROJECT_DIR")}
    with patch.dict(os.environ, env_patch, clear=True):
        with patch.object(Path, "cwd", return_value=home):
            # In the old code, redeploy_rules would silently write to home.
            # With D1 guard, it must raise WriteRefused.
            with pytest.raises(ValueError, match="WriteRefused"):
                srv._assert_writable_project("redeploy_rules")


# ─── TC-07: binding_required tag on all write-side tools ─────────────────────


@pytest.mark.asyncio
async def test_tc07_write_side_tools_have_binding_required_tag() -> None:
    """All write-side tools must carry the 'binding_required' tag (D4)."""
    expected_write_side = {
        "init_project", "init_solo", "create_custom_team",
        "write_task", "archive_task", "write_report", "write_issue", "write_review",
        "mark_human_approved", "deploy_role_templates", "new_workspace",
        "drop_suggestion", "fcop_audit", "redeploy_rules", "fcop_create_alert",
    }
    tools = await srv.mcp.list_tools()
    tools_with_tag: set[str] = {
        t.name for t in tools if t.tags and "binding_required" in t.tags
    }
    missing = expected_write_side - tools_with_tag
    assert not missing, f"Missing 'binding_required' tag on: {sorted(missing)}"


# ─── TC-08: fcop_report() warns when project_path is protected ───────────────


def test_tc08_fcop_report_warns_protected_path() -> None:
    """fcop_report() must include a warning when project resolves to home dir (D3)."""
    _reset_session()
    home = _home_path()
    env_patch = {k: v for k, v in os.environ.items()
                 if k not in ("FCOP_PROJECT_DIR", "CODEFLOW_PROJECT_DIR")}
    with patch.dict(os.environ, env_patch, clear=True):
        with patch.object(Path, "cwd", return_value=home):
            # _compose_session_report is read-only (no guard), so it must run
            # but produce a warning in the output.
            report = srv._compose_session_report("zh")
    assert "警告" in report or "WARNING" in report, (
        "fcop_report() should warn about protected project path"
    )


# ─── TC-09: S1 — non-init tool refuses when fcop.json missing ────────────────


def test_tc09_s1_refuses_when_no_fcop_json(tmp_path: Path) -> None:
    """S1: non-init write-side tools must refuse if fcop.json is absent."""
    _reset_session()
    project_dir = tmp_path / "empty_project"
    project_dir.mkdir()
    with srv._STATE_LOCK:
        srv._SESSION_PROJECT_PATH = project_dir
        srv._SESSION_PROJECT_SOURCE = "session:set_project_dir"
    try:
        with pytest.raises(ValueError, match="WriteRefused"):
            srv._assert_writable_project("write_task")
    finally:
        _reset_session()


# ─── TC-10: S1 — init tools exempt from fcop.json check ─────────────────────


@pytest.mark.parametrize("init_tool", ["init_project", "init_solo", "create_custom_team"])
def test_tc10_s1_init_tools_skip_fcop_check(tmp_path: Path, init_tool: str) -> None:
    """S1: init tools are exempt from the fcop.json existence check (they create it)."""
    _reset_session()
    project_dir = tmp_path / "new_project"
    project_dir.mkdir()
    # No fcop.json — init tools must still pass S1
    with srv._STATE_LOCK:
        srv._SESSION_PROJECT_PATH = project_dir
        srv._SESSION_PROJECT_SOURCE = "session:set_project_dir"
    try:
        path, source = srv._assert_writable_project(init_tool)
        assert path == project_dir
    finally:
        _reset_session()


# ─── TC-11: S2 — HOME subdirectory is allowed ────────────────────────────────


def test_tc11_s2_home_subdir_allowed(tmp_path: Path) -> None:
    """S2: only the EXACT home dir is refused; a subdirectory is a legal project."""
    _reset_session()
    # Simulate a project inside the home directory (e.g. ~/my-project)
    home = Path.home().resolve()
    project_under_home = home / "my-project"

    # We don't create it on disk; just verify _is_protected_path accepts it.
    assert not srv._is_protected_path(project_under_home), (
        f"HOME subdirectory {project_under_home} should NOT be protected "
        f"(only exact HOME={home} is refused)"
    )


def test_tc11_s2_exact_home_refused() -> None:
    """S2: the exact home directory must be refused."""
    home = Path.home().resolve()
    assert srv._is_protected_path(home), (
        f"Exact HOME={home} must be in the protected set"
    )


# ─── TC-12: S3 — all write-side tools share consistent guard (parametrize) ───


_ALL_WRITE_SIDE = [
    "init_project", "init_solo", "create_custom_team",
    "write_task", "archive_task", "write_report", "write_issue", "write_review",
    "mark_human_approved", "deploy_role_templates", "new_workspace",
    "drop_suggestion", "fcop_audit", "redeploy_rules", "fcop_create_alert",
]


@pytest.mark.parametrize("tool_name", _ALL_WRITE_SIDE)
def test_tc12_s3_all_tools_refuse_cwd_fallback(tmp_path: Path, tool_name: str) -> None:
    """S3: every write-side tool must refuse when there is no explicit binding."""
    _reset_session()
    env_patch = {k: v for k, v in os.environ.items()
                 if k not in ("FCOP_PROJECT_DIR", "CODEFLOW_PROJECT_DIR")}
    with patch.dict(os.environ, env_patch, clear=True):
        with patch.object(Path, "cwd", return_value=tmp_path):
            with pytest.raises(ValueError, match="WriteRefused"):
                srv._assert_writable_project(tool_name)


@pytest.mark.parametrize("tool_name", _ALL_WRITE_SIDE)
def test_tc12_s3_all_tools_refuse_home_binding(tool_name: str) -> None:
    """S3: every write-side tool must refuse when bound to exact USER HOME."""
    _reset_session()
    home = _home_path()
    with srv._STATE_LOCK:
        srv._SESSION_PROJECT_PATH = home
        srv._SESSION_PROJECT_SOURCE = "session:set_project_dir"
    try:
        with pytest.raises(ValueError, match="WriteRefused"):
            srv._assert_writable_project(tool_name)
    finally:
        _reset_session()
