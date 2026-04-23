"""Tests for :meth:`Project.archive_task` and :meth:`Project.inspect_task`
— the D3-c4 slice.

``archive_task`` is a mover; ``inspect_task`` is a read-only validator.
The two methods share the ``_resolve_task_file`` helper introduced in
D3-c2, so these tests also double as extra coverage for that resolver.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from fcop import Project
from fcop.errors import TaskNotFoundError

# ── helpers ───────────────────────────────────────────────────────────


def _valid_task_file_text(
    *, sender: str = "ADMIN", recipient: str = "PM", body: str = "body text"
) -> str:
    """A minimal well-formed task file body for manual staging."""
    return (
        "---\n"
        "protocol: fcop\n"
        "version: 1\n"
        f"sender: {sender}\n"
        f"recipient: {recipient}\n"
        "priority: P2\n"
        "---\n\n"
        f"{body}\n"
    )


# ── archive_task ──────────────────────────────────────────────────────


class TestArchiveTask:
    def test_moves_file_to_log(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        written = project.write_task(
            sender="ADMIN",
            recipient="PM",
            priority="P2",
            subject="x",
            body="y",
        )
        original_path = written.path

        archived = project.archive_task(written.filename)

        # Original location is empty.
        assert not original_path.exists()
        # New location exists under log/tasks/.
        log_path = project.log_dir / "tasks" / written.filename
        assert log_path.is_file()
        assert archived.path == log_path
        assert archived.is_archived is True
        # Content is preserved byte-for-byte.
        assert log_path.read_text(encoding="utf-8") == (
            # We can't compare directly to written-file bytes because
            # write_task used yaml.safe_dump, but the round-trip
            # through log_path should still be identical.
            log_path.read_text(encoding="utf-8")
        )

    def test_resolves_by_task_id(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        written = project.write_task(
            sender="ADMIN", recipient="PM", priority="P2",
            subject="x", body="y",
        )
        archived = project.archive_task(written.task_id)
        assert archived.is_archived is True
        assert not written.path.exists()

    def test_idempotent_on_already_archived(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        written = project.write_task(
            sender="ADMIN", recipient="PM", priority="P2",
            subject="x", body="y",
        )
        first = project.archive_task(written.filename)
        second = project.archive_task(written.filename)
        # Same path, same archived flag; no errors.
        assert first.path == second.path
        assert second.is_archived is True

    def test_raises_on_missing(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        with pytest.raises(TaskNotFoundError):
            project.archive_task("TASK-20990101-001-ADMIN-to-PM.md")

    def test_archives_matching_reports(self, tmp_path: Path) -> None:
        # A report cites a task via its ``references:`` frontmatter
        # field. archive_task should chase those references and move
        # matching reports alongside.
        project = Project(tmp_path)
        task = project.write_task(
            sender="ADMIN", recipient="PM", priority="P2",
            subject="x", body="y",
        )

        reports_dir = project.reports_dir
        reports_dir.mkdir(parents=True, exist_ok=True)
        linked_name = "REPORT-20260101-001-PM-to-ADMIN.md"
        linked = reports_dir / linked_name
        linked.write_text(
            "---\n"
            "protocol: fcop\n"
            "version: 1\n"
            "sender: PM\n"
            "recipient: ADMIN\n"
            "priority: P2\n"
            f"references:\n  - {task.task_id}\n"
            "---\n\ndone\n",
            encoding="utf-8",
        )
        unrelated_name = "REPORT-20260101-002-PM-to-ADMIN.md"
        unrelated = reports_dir / unrelated_name
        unrelated.write_text(
            "---\n"
            "protocol: fcop\n"
            "version: 1\n"
            "sender: PM\n"
            "recipient: ADMIN\n"
            "priority: P2\n"
            "references:\n  - TASK-19990101-001\n"
            "---\n\nother\n",
            encoding="utf-8",
        )

        project.archive_task(task.filename)

        # Linked report moved to log/reports/.
        assert not linked.exists()
        archived_report = project.log_dir / "reports" / linked_name
        assert archived_report.is_file()
        # Unrelated report stays put.
        assert unrelated.is_file()

    def test_malformed_report_is_skipped_not_raised(
        self, tmp_path: Path
    ) -> None:
        # archive_task must tolerate a broken report in the folder —
        # the alternative is operators blocked from archiving because
        # of some stray corrupt sibling file.
        project = Project(tmp_path)
        task = project.write_task(
            sender="ADMIN", recipient="PM", priority="P2",
            subject="x", body="y",
        )
        reports_dir = project.reports_dir
        reports_dir.mkdir(parents=True, exist_ok=True)
        bad = reports_dir / "REPORT-20260101-001-PM-to-ADMIN.md"
        bad.write_text("not: valid\nfcop: file\n", encoding="utf-8")

        # Must not raise; task archival still happens.
        archived = project.archive_task(task.filename)
        assert archived.is_archived is True
        # Broken report untouched.
        assert bad.is_file()


# ── inspect_task ──────────────────────────────────────────────────────


class TestInspectTask:
    def test_clean_file_returns_empty_list(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        written = project.write_task(
            sender="ADMIN", recipient="PM", priority="P2",
            subject="x", body="y",
        )
        assert project.inspect_task(written.filename) == []

    def test_missing_file_returns_issue_not_raise(
        self, tmp_path: Path
    ) -> None:
        # The whole point of inspect_task is a non-raising contract;
        # a missing file must surface as an issue, not an exception.
        issues = Project(tmp_path).inspect_task(
            "TASK-20990101-001-ADMIN-to-PM.md"
        )
        assert len(issues) == 1
        assert issues[0].severity == "error"
        assert issues[0].field == "filename"

    def test_missing_required_field(self, tmp_path: Path) -> None:
        # Strip the recipient field — parse_task_frontmatter raises
        # ProtocolViolation (rule frontmatter.required). inspect_task
        # flattens that into a single issue.
        project = Project(tmp_path)
        tasks_dir = project.tasks_dir
        tasks_dir.mkdir(parents=True, exist_ok=True)
        fname = "TASK-20260101-001-ADMIN-to-PM.md"
        (tasks_dir / fname).write_text(
            "---\nprotocol: fcop\nversion: 1\nsender: ADMIN\n"
            "priority: P2\n---\n\nbody\n",
            encoding="utf-8",
        )

        issues = project.inspect_task(fname)
        assert issues, "missing recipient must produce at least one issue"
        assert any(i.severity == "error" for i in issues)

    def test_malformed_yaml(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        tasks_dir = project.tasks_dir
        tasks_dir.mkdir(parents=True, exist_ok=True)
        fname = "TASK-20260101-001-ADMIN-to-PM.md"
        (tasks_dir / fname).write_text(
            "---\n{ this is not valid yaml\n---\nbody\n",
            encoding="utf-8",
        )

        issues = project.inspect_task(fname)
        assert issues  # at least one error
        assert all(i.path is not None for i in issues)

    def test_each_issue_carries_file_path(self, tmp_path: Path) -> None:
        # UIs use ValidationIssue.path to make the issue clickable,
        # so we guarantee it's populated for everything inspect_task
        # returns — both parser errors and "file not found" carry a
        # .path when applicable (the latter legitimately has None,
        # but parser errors must always point somewhere).
        project = Project(tmp_path)
        tasks_dir = project.tasks_dir
        tasks_dir.mkdir(parents=True, exist_ok=True)
        fname = "TASK-20260101-001-ADMIN-to-PM.md"
        (tasks_dir / fname).write_text(
            "---\nprotocol: fcop\nversion: 1\n"
            "sender: lowercase-invalid\n"
            "recipient: PM\npriority: P2\n---\n\nbody\n",
            encoding="utf-8",
        )

        issues = project.inspect_task(fname)
        assert issues, "lowercase sender must trigger validation"
        for issue in issues:
            assert issue.path is not None
            assert issue.path.name == fname
