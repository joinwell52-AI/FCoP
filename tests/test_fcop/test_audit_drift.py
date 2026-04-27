"""Tests for :meth:`fcop.Project.audit_drift` (since 0.7.1).

The method backs the :func:`fcop_check` MCP tool and the new drift
section in :func:`fcop_report`. Surfaces two independent classes of
ledger violation:

1. **Working-tree drift** (Rule 0.a.1 / ISSUE-20260427-001): files
   touched outside ``docs/agents/{tasks,reports,issues,log}/`` that
   bypass the four-step task→do→report→archive cycle.
2. **session_id ↔ role conflicts** (Rule 1 / ISSUE-20260427-004): a
   ``session_id`` that signed files under more than one role code,
   the canonical evidence of sub-agent role impersonation.

Both audits are detection-only — they exist to make evidence loud,
not to block writes.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from fcop import DriftReport, Project, SessionRoleConflict


def _init_solo(tmp_path: Path) -> Project:
    project = Project(tmp_path)
    project.init_solo(role_code="ME", lang="en")
    return project


def _git_init(repo: Path) -> bool:
    try:
        subprocess.run(
            ["git", "init", "-q"],
            cwd=str(repo),
            check=True,
            timeout=15,
            capture_output=True,
        )
        # Configure local identity so commit operations don't fail
        # if the test happens to run them later.
        for key, value in (
            ("user.email", "test@example.invalid"),
            ("user.name", "fcop test"),
        ):
            subprocess.run(
                ["git", "config", "--local", key, value],
                cwd=str(repo),
                check=True,
                timeout=15,
                capture_output=True,
            )
    except (FileNotFoundError, subprocess.SubprocessError):
        return False
    return True


class TestAuditDriftEmpty:
    def test_uninitialized_project_returns_empty_report(
        self, tmp_path: Path
    ) -> None:
        project = Project(tmp_path)
        report = project.audit_drift()

        assert isinstance(report, DriftReport)
        assert report.entries == ()
        assert report.session_role_conflicts == ()

    def test_freshly_initialized_solo_no_drift(self, tmp_path: Path) -> None:
        project = _init_solo(tmp_path)

        report = project.audit_drift()

        # A solo init under a non-git tree should not crash and should
        # not produce session_id conflicts (no session_id frontmatter
        # was written by ``init_solo``).
        assert report.session_role_conflicts == ()


class TestWorkingTreeDrift:
    def test_drift_outside_ledger_is_reported(self, tmp_path: Path) -> None:
        if not _git_init(tmp_path):
            return  # no git available — covered separately

        project = _init_solo(tmp_path)
        # Stand up an untracked file that is NOT inside the FCoP
        # ledger — exactly the Rule 0.a.1 violation pattern.
        rogue = tmp_path / "rogue_note.md"
        rogue.write_text("not in any task chain", encoding="utf-8")

        report = project.audit_drift()

        assert report.git_available is True
        rogue_paths = [e.path for e in report.entries]
        assert any(
            "rogue_note.md" in p for p in rogue_paths
        ), f"expected rogue_note.md in drift entries, got {rogue_paths}"
        for entry in report.entries:
            assert entry.in_ledger is False, (
                "audit_drift must filter out ledger-internal files"
            )

    def test_files_inside_ledger_are_not_drift(self, tmp_path: Path) -> None:
        if not _git_init(tmp_path):
            return

        project = _init_solo(tmp_path)
        # Drop a file *inside* the issues directory — this is the
        # FCoP-blessed write path, even though the file is untracked
        # by git.
        ledger_file = (
            project.issues_dir / "ISSUE-20260427-099-ME.md"
        )
        ledger_file.parent.mkdir(parents=True, exist_ok=True)
        ledger_file.write_text(
            "---\nprotocol: fcop\nversion: 1\nreporter: ME\n"
            "severity: low\nstatus: open\nsummary: test\n"
            "created_at: 2026-04-27T00:00:00\n---\n\nbody\n",
            encoding="utf-8",
        )

        report = project.audit_drift()

        # The file is untracked by git, but lives in the ledger so
        # audit_drift must NOT report it.
        for entry in report.entries:
            assert "ISSUE-20260427-099-ME.md" not in entry.path, (
                f"ledger file was incorrectly flagged as drift: {entry}"
            )


class TestSessionRoleConflicts:
    def test_single_role_per_session_no_conflict(
        self, tmp_path: Path
    ) -> None:
        project = _init_solo(tmp_path)

        # Two files, same session_id, same role — happy path.
        for seq, name in (
            (1, "TASK-20260427-001-ADMIN-to-ME.md"),
            (2, "TASK-20260427-002-ADMIN-to-ME.md"),
        ):
            (project.tasks_dir / name).write_text(
                _task_body(sender="ADMIN", session="sess-A"),
                encoding="utf-8",
            )
            del seq

        report = project.audit_drift()

        assert report.session_role_conflicts == ()

    def test_two_roles_share_one_session_id_is_a_conflict(
        self, tmp_path: Path
    ) -> None:
        project = _init_solo(tmp_path)

        # Same session_id signing two different sender roles — the
        # canonical sub-agent impersonation pattern.
        (project.tasks_dir / "TASK-20260427-010-PLANNER-to-ME.md").write_text(
            _task_body(sender="PLANNER", session="sess-X"),
            encoding="utf-8",
        )
        project.reports_dir.mkdir(parents=True, exist_ok=True)
        (project.reports_dir / "REPORT-20260427-011-CODE_EXPERT-to-ME.md").write_text(
            _report_body(reporter="CODE_EXPERT", session="sess-X"),
            encoding="utf-8",
        )

        report = project.audit_drift()

        assert len(report.session_role_conflicts) == 1
        conflict = report.session_role_conflicts[0]
        assert isinstance(conflict, SessionRoleConflict)
        assert conflict.session_id == "sess-X"
        assert set(conflict.roles) == {"PLANNER", "CODE_EXPERT"}
        assert len(conflict.files) == 2


def _task_body(*, sender: str, session: str) -> str:
    return (
        "---\n"
        "protocol: fcop\n"
        "version: 1\n"
        "kind: task\n"
        f"task_id: TASK-20260427-{sender}\n"
        f"sender: {sender}\n"
        "recipient: ME\n"
        "priority: P2\n"
        f"session_id: {session}\n"
        "---\n\nbody\n"
    )


def _report_body(*, reporter: str, session: str) -> str:
    return (
        "---\n"
        "protocol: fcop\n"
        "version: 1\n"
        "kind: report\n"
        "task_id: TASK-20260427-XXX\n"
        f"reporter: {reporter}\n"
        "recipient: ME\n"
        "status: done\n"
        "priority: P2\n"
        f"session_id: {session}\n"
        "---\n\nbody\n"
    )
