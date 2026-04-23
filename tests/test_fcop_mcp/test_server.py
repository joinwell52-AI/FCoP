"""End-to-end smoke tests for every registered ``fcop-mcp`` tool and resource.

Purpose
-------
The :mod:`test_tool_surface` snapshot guards the **shape** of the contract
(tool name, param name, required-ness). This module guards the **behavior**:
when Cursor actually invokes each tool, does a sensible thing happen?

Testing strategy
~~~~~~~~~~~~~~~~
* Each test runs inside ``tmp_path`` and pins the session project via
  ``set_project_dir`` so the MCP layer's path-resolution cascade can be
  verified end-to-end.
* Tests exercise tools via ``mcp.call_tool(...)`` — the exact code path
  Cursor / Claude Desktop hit — instead of calling the decorated
  functions directly. This keeps us honest about JSON-schema coercion.
* We assert on *substrings* rather than full-string matches, because
  ADR-0003 §"Return Shape" only commits to keeping the same fields,
  not identical prose. Byte-level matching would break on every
  wording tweak.
* Negative paths (uninitialized project, invalid inputs) are covered
  alongside happy paths so that error copy also stays consistent.

Fixtures live in ``conftest.py``:

    clean_env              wipe FCOP_* / CODEFLOW_* env vars
    reset_session_project  wipe module-level session pin between tests
    project_dir            empty tmp dir (no init)
    initialized_project    tmp dir already initialized with dev-team
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Any

import pytest
from fcop_mcp.server import mcp

# ─── Shared helpers ──────────────────────────────────────────────────


def _text(result: object) -> str:
    """Extract the first text payload from a FastMCP tool or resource result.

    FastMCP's result shape differs slightly between ``call_tool`` and
    ``read_resource`` across versions, so we probe the most common
    attribute paths and fall back to ``repr``.
    """
    for attr in ("content", "contents"):
        items = getattr(result, attr, None)
        if items:
            first = items[0] if isinstance(items, list) else items
            for a in ("text", "content", "body"):
                txt = getattr(first, a, None)
                if isinstance(txt, str):
                    return txt
    return repr(result)


def _call(name: str, **kwargs: Any) -> str:
    """Invoke an MCP tool by name and return its textual result."""
    result = asyncio.run(mcp.call_tool(name, kwargs))
    return _text(result)


def _read(uri: str) -> str:
    """Read an MCP resource by URI and return its textual content."""
    result = asyncio.run(mcp.read_resource(uri))
    return _text(result)


# ─── Path resolution ─────────────────────────────────────────────────


class TestProjectPath:
    """Coverage for ``set_project_dir`` and the ``_get_project`` cascade.

    The 0.5.4 contract says project resolution follows this priority:
    session pin → FCOP_PROJECT_DIR → CODEFLOW_PROJECT_DIR → auto
    markers → cwd. The session pin is the only one we drive from a
    tool; the others are covered by fcop library tests.
    """

    def test_set_project_dir_happy_path(self, project_dir: Path) -> None:
        out = _call("set_project_dir", path=str(project_dir))
        assert "project root bound" in out or "已绑定" in out
        assert str(project_dir) in out

    def test_set_project_dir_rejects_missing_path(
        self, project_dir: Path
    ) -> None:
        bogus = project_dir / "does-not-exist"
        out = _call("set_project_dir", path=str(bogus))
        assert "不存在" in out or "does not exist" in out

    def test_set_project_dir_rejects_file(
        self, project_dir: Path
    ) -> None:
        f = project_dir / "a.txt"
        f.write_text("hi", encoding="utf-8")
        out = _call("set_project_dir", path=str(f))
        assert "not a directory" in out or "不是目录" in out


# ─── Initialization ──────────────────────────────────────────────────


class TestInit:
    def test_init_project_dev_team(self, project_dir: Path) -> None:
        _call("set_project_dir", path=str(project_dir))
        out = _call("init_project", team="dev-team", lang="zh")
        assert "dev-team" in out
        assert (project_dir / "docs" / "agents" / "fcop.json").exists()

    def test_init_project_unknown_team(self, project_dir: Path) -> None:
        _call("set_project_dir", path=str(project_dir))
        out = _call("init_project", team="no-such-team", lang="zh")
        assert "no-such-team" in out.lower() or "not found" in out.lower() or \
               "未知" in out or "错误" in out or "error" in out.lower()

    def test_init_solo(self, project_dir: Path) -> None:
        _call("set_project_dir", path=str(project_dir))
        out = _call("init_solo", role_code="ME", role_label="", lang="zh")
        cfg = project_dir / "docs" / "agents" / "fcop.json"
        assert cfg.exists()
        data = json.loads(cfg.read_text(encoding="utf-8"))
        assert "ME" in data["roles"]
        assert "ME" in out or "solo" in out.lower() or "已初始化" in out

    def test_create_custom_team(self, project_dir: Path) -> None:
        _call("set_project_dir", path=str(project_dir))
        out = _call(
            "create_custom_team",
            roles="PM,DEV,QA",
            leader="PM",
            lang="zh",
            team_name="my-team",
        )
        assert "PM" in out and "DEV" in out
        cfg = project_dir / "docs" / "agents" / "fcop.json"
        assert cfg.exists()
        data = json.loads(cfg.read_text(encoding="utf-8"))
        assert data["team"] == "my-team"
        assert data["leader"] == "PM"

    def test_validate_team_config_ok(self, project_dir: Path) -> None:
        _call("set_project_dir", path=str(project_dir))
        out = _call("validate_team_config", roles="PM,DEV", leader="PM")
        # success returns a passing message; library raises on real failure
        assert "PM" in out

    def test_validate_team_config_bad_leader(
        self, project_dir: Path
    ) -> None:
        _call("set_project_dir", path=str(project_dir))
        out = _call("validate_team_config", roles="PM,DEV", leader="BOSS")
        assert "BOSS" in out or "leader" in out.lower() or "错误" in out


# ─── Task CRUD ───────────────────────────────────────────────────────


class TestTasks:
    def test_full_task_lifecycle(self, initialized_project: Path) -> None:
        create = _call(
            "write_task",
            sender="PM",
            recipient="DEV",
            subject="First task",
            body="Body of the first task.",
            priority="P2",
        )
        assert "TASK-" in create
        # Pull the filename out of the response.
        filename = next(
            (tok for tok in create.split() if tok.startswith("TASK-")),
            "",
        )
        assert filename, f"could not parse task filename from: {create!r}"

        listing = _call("list_tasks")
        assert filename in listing
        assert "Total:" in listing or "共" in listing

        detail = _call("read_task", filename=filename)
        assert "First task" in detail
        assert "Body of the first task" in detail

        inspection = _call("inspect_task", filename=filename)
        # A freshly written task from the library must pass inspection.
        assert "PASS" in inspection

        parts = filename.split("-")
        task_id = f"{parts[0]}-{parts[1]}-{parts[2]}"
        archived = _call("archive_task", task_id=task_id)
        assert "Archived" in archived or "已归档" in archived

        # After archival, default listing (status=open) should not show it.
        listing_after = _call("list_tasks")
        assert filename not in listing_after or "No tasks" in listing_after

    def test_read_task_not_found(self, initialized_project: Path) -> None:
        out = _call("read_task", filename="TASK-20260101-999-PM-to-DEV.md")
        assert "not found" in out.lower() or "未找到" in out

    def test_list_tasks_invalid_status(
        self, initialized_project: Path
    ) -> None:
        out = _call("list_tasks", status="garbage")
        assert "garbage" in out

    def test_write_task_requires_initialized_project(
        self, project_dir: Path
    ) -> None:
        _call("set_project_dir", path=str(project_dir))
        out = _call(
            "write_task",
            sender="PM",
            recipient="DEV",
            subject="Should fail",
            body="project not initialized",
        )
        assert "init" in out.lower() or "初始化" in out


# ─── Report & Issue CRUD ─────────────────────────────────────────────


class TestReportsAndIssues:
    def test_report_lifecycle(self, initialized_project: Path) -> None:
        task_out = _call(
            "write_task",
            sender="PM",
            recipient="DEV",
            subject="Task for report",
            body="to be reported on",
        )
        task_filename = next(
            tok for tok in task_out.split() if tok.startswith("TASK-")
        )
        parts = task_filename.split("-")
        task_id = f"{parts[0]}-{parts[1]}-{parts[2]}"

        rep = _call(
            "write_report",
            task_id=task_id,
            reporter="DEV",
            recipient="PM",
            body="Report body",
            status="done",
        )
        assert "REPORT-" in rep
        rep_filename = next(
            tok for tok in rep.split() if tok.startswith("REPORT-")
        )

        listing = _call("list_reports")
        assert rep_filename in listing

        detail = _call("read_report", filename=rep_filename)
        assert "Report body" in detail

    def test_write_report_bad_status(
        self, initialized_project: Path
    ) -> None:
        out = _call(
            "write_report",
            task_id="TASK-20260101-001",
            reporter="DEV",
            recipient="PM",
            body="x",
            status="weird",
        )
        assert "weird" in out

    def test_issue_lifecycle(self, initialized_project: Path) -> None:
        out = _call(
            "write_issue",
            reporter="QA",
            summary="login broken",
            body="steps: ...",
            severity="high",
        )
        assert "ISSUE-" in out or "Issue" in out

        listing = _call("list_issues")
        assert "login broken" in listing or "Total:" in listing


# ─── Team / Deploy / Workspace tools ─────────────────────────────────


class TestTeamAndWorkspace:
    def test_get_available_teams(self, project_dir: Path) -> None:
        out = _call("get_available_teams", lang="zh")
        assert "dev-team" in out
        assert "leader" in out.lower() or "队长" in out or "lead" in out.lower()

    def test_get_team_status_uninitialized(
        self, project_dir: Path
    ) -> None:
        _call("set_project_dir", path=str(project_dir))
        out = _call("get_team_status", lang="zh")
        assert "NOT initialized" in out or "未初始化" in out

    def test_get_team_status_initialized(
        self, initialized_project: Path
    ) -> None:
        out = _call("get_team_status", lang="zh")
        assert "dev-team" in out
        assert "PM" in out

    def test_deploy_role_templates(
        self, initialized_project: Path
    ) -> None:
        out = _call("deploy_role_templates", team="", lang="", force=True)
        assert "Deployed" in out
        shared = initialized_project / "docs" / "agents" / "shared"
        assert shared.exists()
        assert any(shared.iterdir())

    def test_new_workspace_and_list(
        self, initialized_project: Path
    ) -> None:
        out = _call("new_workspace", slug="feature-a", title="Feature A")
        assert "feature-a" in out
        ws_dir = initialized_project / "workspace" / "feature-a"
        assert ws_dir.exists()

        listing = _call("list_workspaces")
        assert "feature-a" in listing

    def test_new_workspace_bad_slug(
        self, initialized_project: Path
    ) -> None:
        out = _call("new_workspace", slug="Bad Slug!!")
        assert "slug" in out.lower() or "错误" in out

    def test_list_workspaces_none(
        self, initialized_project: Path
    ) -> None:
        out = _call("list_workspaces")
        assert "workspace" in out.lower() or "没有" in out or "no " in out.lower()


# ─── Safety-fuse + Meta tools ────────────────────────────────────────


class TestSafetyAndMeta:
    def test_drop_suggestion(self, project_dir: Path) -> None:
        _call("set_project_dir", path=str(project_dir))
        out = _call(
            "drop_suggestion",
            content="I think we should pause.",
            context="TASK-20260423-001",
        )
        assert "suggestion" in out.lower() or "建议" in out or ".fcop" in out
        proposals = project_dir / ".fcop" / "proposals"
        assert proposals.exists()
        files = list(proposals.iterdir())
        assert len(files) == 1

    def test_unbound_report_uninitialized(
        self, project_dir: Path
    ) -> None:
        _call("set_project_dir", path=str(project_dir))
        out = _call("unbound_report", lang="zh")
        # Uninitialized project emits the init-required variant.
        assert "init" in out.lower() or "初始化" in out or "FCoP" in out

    def test_unbound_report_initialized(
        self, initialized_project: Path
    ) -> None:
        out = _call("unbound_report", lang="zh")
        assert "UNBOUND" in out or "dev-team" in out

    def test_upgrade_fcop_is_dry(self, project_dir: Path) -> None:
        out = _call("upgrade_fcop", lang="zh")
        # Must NEVER attempt to run pip — always returns instructions.
        assert "pip" in out.lower() or "uvx" in out.lower() or \
               "pipx" in out.lower() or "fcop-mcp" in out
        assert "upgrade" in out.lower() or "升级" in out


# ─── Resources ───────────────────────────────────────────────────────


class TestResources:
    """Every fcop:// resource should return non-empty content.

    ADR-0003 §Commitment #2 extends to resources too: URI stays,
    mime type stays, content is expected to be non-empty.
    """

    @pytest.mark.parametrize(
        "uri",
        [
            "fcop://rules",
            "fcop://protocol",
            "fcop://letter/zh",
            "fcop://letter/en",
            "fcop://teams",
        ],
    )
    def test_static_resource_non_empty(self, uri: str) -> None:
        body = _read(uri)
        assert body, f"{uri} returned empty content"
        assert len(body) > 50, f"{uri} suspiciously short: {body!r}"

    def test_status_resource_uninitialized(
        self, project_dir: Path
    ) -> None:
        _call("set_project_dir", path=str(project_dir))
        body = _read("fcop://status")
        assert "NOT initialized" in body or "未初始化" in body

    def test_status_resource_initialized(
        self, initialized_project: Path
    ) -> None:
        body = _read("fcop://status")
        assert "dev-team" in body

    def test_config_resource(self, initialized_project: Path) -> None:
        body = _read("fcop://config")
        data = json.loads(body)
        assert data["team"] == "dev-team"
        assert "PM" in data["roles"]

    def test_teams_index_is_json(self) -> None:
        body = _read("fcop://teams")
        data = json.loads(body)
        team_names = {t["name"] for t in data["teams"]}
        assert "dev-team" in team_names

    def test_team_readme_template(self) -> None:
        body = _read("fcop://teams/dev-team")
        assert "dev-team" in body
        assert len(body) > 200

    def test_team_role_zh_template(self) -> None:
        body = _read("fcop://teams/dev-team/PM")
        assert "PM" in body
        assert len(body) > 100

    def test_team_role_en_template(self) -> None:
        body = _read("fcop://teams/dev-team/PM/en")
        assert "PM" in body
        assert len(body) > 100
