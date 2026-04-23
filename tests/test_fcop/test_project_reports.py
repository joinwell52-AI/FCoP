"""Tests for :class:`fcop.Project` report CRUD — the D4-c1 surface.

Goals:
    * ``write_report`` creates a well-formed report file that cites
      the original task via ``references`` and stores ``status`` at
      the top level of its frontmatter.
    * Rule 5 is enforced: only the task's recipient may report.
    * ``write_report`` refuses to touch disk if the referenced task
      doesn't exist — no stub reports left behind.
    * Round-trips through ``write_report`` → ``read_report`` preserve
      the full report shape (reporter, recipient, status, body,
      task_id).
    * ``list_reports`` filters by reporter / parent task and orders
      newest-first via the embedded date+sequence tuple.
    * Malformed report files are silently skipped by ``list_reports``
      (matching the ``list_tasks`` contract).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from fcop import Project
from fcop.errors import ProtocolViolation, TaskNotFoundError
from fcop.models import Report


def _seed_task(project: Project, **overrides: object):
    """Write a default task and return it. Overrides layer onto defaults."""
    kwargs = {
        "sender": "ADMIN",
        "recipient": "PM",
        "priority": "P1",
        "subject": "Plan 0.6",
        "body": "Please plan the release.",
    }
    kwargs.update(overrides)
    return project.write_task(**kwargs)  # type: ignore[arg-type]


# ── write_report ──────────────────────────────────────────────────────


class TestWriteReport:
    def test_creates_file_with_references(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        task = _seed_task(project)

        report = project.write_report(
            task_id=task.task_id,
            reporter="PM",
            recipient="ADMIN",
            body="Release plan attached.",
            status="done",
        )

        assert isinstance(report, Report)
        assert report.task_id == task.task_id
        assert report.reporter == "PM"
        assert report.recipient == "ADMIN"
        assert report.status == "done"
        assert report.path.is_file()
        assert report.path == (
            tmp_path / "docs" / "agents" / "reports" / report.filename
        )
        assert report.filename.startswith("REPORT-")
        assert report.filename.endswith("-PM-to-ADMIN.md")
        assert report.is_archived is False

    def test_frontmatter_has_status_and_references(
        self, tmp_path: Path
    ) -> None:
        project = Project(tmp_path)
        task = _seed_task(project)
        report = project.write_report(
            task_id=task.task_id,
            reporter="PM",
            recipient="ADMIN",
            body="All green.",
            status="done",
        )

        text = report.path.read_text(encoding="utf-8")
        assert text.startswith("---\n")
        assert "protocol: fcop\n" in text
        assert "sender: PM\n" in text
        assert "recipient: ADMIN\n" in text
        # `status` and `references` both live in the frontmatter.
        assert "status: done\n" in text
        assert "references:" in text
        assert task.task_id in text
        # Body preserved verbatim after closing fence.
        assert text.rstrip().endswith("All green.")

    def test_sequence_increments_per_day(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        task = _seed_task(project)

        first = project.write_report(
            task_id=task.task_id,
            reporter="PM",
            recipient="ADMIN",
            body="One",
        )
        second = project.write_report(
            task_id=task.task_id,
            reporter="PM",
            recipient="ADMIN",
            body="Two",
        )
        # Filenames differ because the sequence number advances,
        # not because of the body / status.
        assert first.filename != second.filename

    def test_accepts_priority_alias(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        task = _seed_task(project)

        report = project.write_report(
            task_id=task.task_id,
            reporter="PM",
            recipient="ADMIN",
            body="x",
            priority="urgent",  # alias → P0
        )

        assert "priority: P0\n" in report.path.read_text(encoding="utf-8")

    def test_status_blocked_and_in_progress_accepted(
        self, tmp_path: Path
    ) -> None:
        project = Project(tmp_path)
        task = _seed_task(project)

        blocked = project.write_report(
            task_id=task.task_id,
            reporter="PM",
            recipient="ADMIN",
            body="stuck",
            status="blocked",
        )
        in_prog = project.write_report(
            task_id=task.task_id,
            reporter="PM",
            recipient="ADMIN",
            body="ongoing",
            status="in_progress",
        )
        assert blocked.status == "blocked"
        assert in_prog.status == "in_progress"

    def test_status_must_be_valid(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        task = _seed_task(project)

        with pytest.raises(ProtocolViolation, match="status"):
            project.write_report(
                task_id=task.task_id,
                reporter="PM",
                recipient="ADMIN",
                body="x",
                status="wtf",  # type: ignore[arg-type]
            )
        # No file should have been created on rejection.
        reports_dir = tmp_path / "docs" / "agents" / "reports"
        if reports_dir.exists():
            assert not any(reports_dir.iterdir())

    def test_rejects_missing_task(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        with pytest.raises(TaskNotFoundError):
            project.write_report(
                task_id="TASK-20260101-999",
                reporter="PM",
                recipient="ADMIN",
                body="dangling",
            )
        # Reports directory must not have been populated.
        reports_dir = tmp_path / "docs" / "agents" / "reports"
        if reports_dir.exists():
            assert not any(reports_dir.iterdir())

    def test_rejects_wrong_reporter_rule5(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        task = _seed_task(project, sender="ADMIN", recipient="PM")

        # DEV is not the task's recipient → protocol violation (Rule 5).
        with pytest.raises(ProtocolViolation, match="recipient"):
            project.write_report(
                task_id=task.task_id,
                reporter="DEV",
                recipient="ADMIN",
                body="not allowed",
            )

    def test_report_references_archived_task(self, tmp_path: Path) -> None:
        # Closing the task first should still allow the recipient to
        # file a late report — the task is resolvable by id from the
        # log/tasks directory.
        project = Project(tmp_path)
        task = _seed_task(project)
        project.archive_task(task.task_id)

        report = project.write_report(
            task_id=task.task_id,
            reporter="PM",
            recipient="ADMIN",
            body="late but logged",
        )
        assert report.task_id == task.task_id


# ── read_report ───────────────────────────────────────────────────────


class TestReadReport:
    def test_round_trip_by_filename(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        task = _seed_task(project)
        written = project.write_report(
            task_id=task.task_id,
            reporter="PM",
            recipient="ADMIN",
            body="Round-trip me.",
            status="done",
        )

        loaded = project.read_report(written.filename)
        assert loaded.filename == written.filename
        assert loaded.task_id == written.task_id
        assert loaded.reporter == written.reporter
        assert loaded.recipient == written.recipient
        assert loaded.status == written.status
        # Body preserves content verbatim (a single leading newline is
        # introduced by assemble_task_file and carried as-is — matches
        # the task round-trip contract).
        assert "Round-trip me." in loaded.body

    def test_round_trip_by_id(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        task = _seed_task(project)
        written = project.write_report(
            task_id=task.task_id,
            reporter="PM",
            recipient="ADMIN",
            body="x",
        )
        # REPORT-YYYYMMDD-NNN prefix is enough to resolve.
        rid = written.filename.rsplit("-PM-to-ADMIN.md", 1)[0]
        loaded = project.read_report(rid)
        assert loaded.filename == written.filename

    def test_reads_archived_report(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        task = _seed_task(project)
        written = project.write_report(
            task_id=task.task_id,
            reporter="PM",
            recipient="ADMIN",
            body="pre-archive",
        )
        # Archiving the parent task should move this report with it.
        project.archive_task(task.task_id)

        loaded = project.read_report(written.filename)
        assert loaded.is_archived is True
        assert "pre-archive" in loaded.body

    def test_missing_raises(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        with pytest.raises(TaskNotFoundError):
            project.read_report("REPORT-20260101-001")


# ── list_reports ──────────────────────────────────────────────────────


class TestListReports:
    def test_empty_project(self, tmp_path: Path) -> None:
        assert Project(tmp_path).list_reports() == []

    def test_sorted_newest_first(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        task = _seed_task(project)
        first = project.write_report(
            task_id=task.task_id,
            reporter="PM",
            recipient="ADMIN",
            body="1",
        )
        second = project.write_report(
            task_id=task.task_id,
            reporter="PM",
            recipient="ADMIN",
            body="2",
        )

        listing = project.list_reports()
        # Same day → sorted by sequence descending, so the later write
        # (higher seq) comes first.
        assert [r.filename for r in listing] == [
            second.filename,
            first.filename,
        ]

    def test_filter_by_reporter(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        # Two separate tasks — one recipient per reporter — so Rule 5
        # is satisfied for each report below.
        task_pm = project.write_task(
            sender="ADMIN",
            recipient="PM",
            priority="P2",
            subject="s",
            body="b",
        )
        task_dev = project.write_task(
            sender="ADMIN",
            recipient="DEV",
            priority="P2",
            subject="s",
            body="b",
        )
        r_pm = project.write_report(
            task_id=task_pm.task_id,
            reporter="PM",
            recipient="ADMIN",
            body="pm",
        )
        project.write_report(
            task_id=task_dev.task_id,
            reporter="DEV",
            recipient="ADMIN",
            body="dev",
        )

        only_pm = project.list_reports(reporter="PM")
        assert [r.filename for r in only_pm] == [r_pm.filename]

    def test_filter_by_task_id(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        task_a = _seed_task(project)
        task_b = project.write_task(
            sender="ADMIN",
            recipient="PM",
            priority="P3",
            subject="b",
            body="b",
        )
        r_a = project.write_report(
            task_id=task_a.task_id,
            reporter="PM",
            recipient="ADMIN",
            body="a",
        )
        project.write_report(
            task_id=task_b.task_id,
            reporter="PM",
            recipient="ADMIN",
            body="b",
        )

        only_a = project.list_reports(task_id=task_a.task_id)
        assert [r.filename for r in only_a] == [r_a.filename]

    def test_archived_status_scope(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        task = _seed_task(project)
        live = project.write_report(
            task_id=task.task_id,
            reporter="PM",
            recipient="ADMIN",
            body="live",
        )
        # Archive parent → report moves with it.
        project.archive_task(task.task_id)

        # Default scope "open" → no reports remain in reports_dir.
        assert project.list_reports() == []
        # Explicit scope hits the log.
        archived = project.list_reports(status="archived")
        assert [r.filename for r in archived] == [live.filename]
        # "all" merges both.
        all_reports = project.list_reports(status="all")
        assert [r.filename for r in all_reports] == [live.filename]

    def test_limit_and_offset(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        task = _seed_task(project)
        filenames = [
            project.write_report(
                task_id=task.task_id,
                reporter="PM",
                recipient="ADMIN",
                body=str(i),
            ).filename
            for i in range(3)
        ]
        # Newest-first: reversed order from creation.
        expected = list(reversed(filenames))

        page = project.list_reports(limit=2)
        assert [r.filename for r in page] == expected[:2]

        page2 = project.list_reports(limit=2, offset=2)
        assert [r.filename for r in page2] == expected[2:]

    def test_skips_malformed_file(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        task = _seed_task(project)
        good = project.write_report(
            task_id=task.task_id,
            reporter="PM",
            recipient="ADMIN",
            body="ok",
        )

        # Drop a malformed file alongside the good one. list_reports
        # must ignore it rather than crashing the whole enumeration.
        bad = project.reports_dir / "REPORT-20260423-999-PM-to-ADMIN.md"
        bad.write_text("not a yaml header\n", encoding="utf-8")

        listing = project.list_reports()
        assert [r.filename for r in listing] == [good.filename]
