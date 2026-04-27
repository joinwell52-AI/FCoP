"""Tests for the per-MCP-process role lock (since fcop-mcp 0.7.1).

The lock is the soft mitigation for ISSUE-20260427-004: a parent
agent that is bound to one role must not flip to a different role
mid-session, and a sub-agent claiming a role its parent was not
assigned is exactly the impersonation we want to surface.

Contract:
- The first ``write_task`` / ``write_report`` / ``write_issue`` of a
  given MCP-server lifetime locks the sender role.
- Subsequent writes under a *different* sender role are still
  *allowed* (the lock is intentionally soft — blocking would just
  hide the impersonation), but produce a Rule 1 warning string and
  drop ``.fcop/proposals/role-switch-{ts}.md`` for ADMIN review.
- Reserved senders (``ADMIN``, ``SYSTEM``) bypass the lock — they
  represent the human / framework rather than an AI seat.
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any

from fcop_mcp.server import mcp


def _text(result: object) -> str:
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
    return _text(asyncio.run(mcp.call_tool(name, kwargs)))


def _init_team(project_dir: Path) -> None:
    _call("set_project_dir", path=str(project_dir))
    _call(
        "create_custom_team",
        roles="PLANNER,CODE_EXPERT,QA",
        leader="PLANNER",
        lang="en",
        team_name="role-lock-test",
    )


class TestRoleLock:
    def test_first_write_locks_role_no_warning(
        self, project_dir: Path
    ) -> None:
        _init_team(project_dir)

        out = _call(
            "write_task",
            sender="PLANNER",
            recipient="CODE_EXPERT",
            subject="initial",
            body="first write",
        )

        assert "Task created" in out
        assert "Rule 1 warning" not in out

    def test_second_write_same_role_no_warning(
        self, project_dir: Path
    ) -> None:
        _init_team(project_dir)

        _call(
            "write_task",
            sender="PLANNER",
            recipient="CODE_EXPERT",
            subject="first",
            body="lock the role",
        )
        out = _call(
            "write_task",
            sender="PLANNER",
            recipient="QA",
            subject="second",
            body="same role, no warning",
        )

        assert "Rule 1 warning" not in out

    def test_role_switch_emits_warning(self, project_dir: Path) -> None:
        _init_team(project_dir)

        _call(
            "write_task",
            sender="PLANNER",
            recipient="CODE_EXPERT",
            subject="planner first",
            body="lock to PLANNER",
        )
        out = _call(
            "write_task",
            sender="CODE_EXPERT",
            recipient="QA",
            subject="impersonation",
            body="trying to flip role",
        )

        assert "Task created" in out, "soft lock must let the write land"
        assert "Rule 1 warning" in out
        assert "PLANNER" in out and "CODE_EXPERT" in out

        proposals = project_dir / ".fcop" / "proposals"
        assert proposals.exists()
        evidence = sorted(proposals.glob("role-switch-*.md"))
        assert evidence, (
            "role switch must drop .fcop/proposals/role-switch-*.md "
            "evidence for fcop_check() to surface later"
        )
        body = evidence[0].read_text(encoding="utf-8")
        assert "PLANNER" in body and "CODE_EXPERT" in body
        assert "Rule 1" in body

    def test_admin_sender_bypasses_lock(self, project_dir: Path) -> None:
        _init_team(project_dir)

        _call(
            "write_task",
            sender="PLANNER",
            recipient="CODE_EXPERT",
            subject="planner write",
            body="lock to PLANNER",
        )
        # ADMIN is the human channel — it must always be allowed
        # without producing the Rule 1 warning.
        out = _call(
            "write_task",
            sender="ADMIN",
            recipient="PLANNER",
            subject="admin instruction",
            body="ADMIN dispatches",
        )

        assert "Rule 1 warning" not in out

    def test_role_switch_via_write_report_also_warns(
        self, project_dir: Path
    ) -> None:
        _init_team(project_dir)

        _call(
            "write_task",
            sender="PLANNER",
            recipient="CODE_EXPERT",
            subject="initial task",
            body="lock to PLANNER",
        )
        out = _call(
            "write_report",
            task_id="TASK-20260427-001",
            reporter="CODE_EXPERT",
            recipient="PLANNER",
            body="report under a different role",
            status="done",
        )

        assert "Rule 1 warning" in out
