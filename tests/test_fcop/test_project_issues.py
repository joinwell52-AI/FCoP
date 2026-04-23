"""Tests for :class:`fcop.Project` issue CRUD — the D4-c2 surface.

Goals:
    * ``write_issue`` creates a well-formed issue file with the
      broadcast shape: no recipient, ``summary`` and ``severity`` as
      first-class frontmatter fields.
    * Severity aliases (``critical`` → ``Severity.CRITICAL``,
      ``"P0"``-equivalent values) are normalized on write.
    * Summary must be non-empty; reporters must pass role grammar.
    * Round-trips through ``write_issue`` → ``read_issue`` preserve
      every field.
    * ``list_issues`` filters by reporter / severity and orders newest
      first via date + sequence.
    * Malformed files are silently skipped by ``list_issues``.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from fcop import Project
from fcop.errors import TaskNotFoundError, ValidationError
from fcop.models import Issue, Severity

# ── write_issue ───────────────────────────────────────────────────────


class TestWriteIssue:
    def test_creates_file(self, tmp_path: Path) -> None:
        issue = Project(tmp_path).write_issue(
            reporter="DEV",
            summary="DB connection timeouts",
            body="Timing out against MySQL around 3AM CST.",
            severity="high",
        )
        assert isinstance(issue, Issue)
        assert issue.reporter == "DEV"
        assert issue.summary == "DB connection timeouts"
        assert issue.severity is Severity.HIGH
        assert issue.path.is_file()
        assert issue.path == (
            tmp_path / "docs" / "agents" / "issues" / issue.filename
        )
        assert issue.filename.startswith("ISSUE-")
        assert issue.filename.endswith("-DEV.md")

    def test_frontmatter_fields(self, tmp_path: Path) -> None:
        issue = Project(tmp_path).write_issue(
            reporter="QA",
            summary="Login regression on Safari 17",
            body="Repro: open /login, tab to submit, ERR.",
            severity="critical",
        )
        text = issue.path.read_text(encoding="utf-8")
        assert text.startswith("---\n")
        assert "protocol: fcop\n" in text
        assert "version: 1\n" in text
        assert "reporter: QA\n" in text
        assert "severity: critical\n" in text
        assert "summary: Login regression on Safari 17\n" in text
        # Issues carry no recipient / priority fields.
        assert "recipient:" not in text
        assert "priority:" not in text
        # Body is preserved.
        assert text.rstrip().endswith("Repro: open /login, tab to submit, ERR.")

    def test_default_severity_medium(self, tmp_path: Path) -> None:
        issue = Project(tmp_path).write_issue(
            reporter="DEV",
            summary="Minor typo",
            body="missing comma",
        )
        assert issue.severity is Severity.MEDIUM
        assert "severity: medium\n" in issue.path.read_text(encoding="utf-8")

    def test_severity_alias_accepted(self, tmp_path: Path) -> None:
        # normalize_severity accepts `crit` / `med` as aliases.
        issue = Project(tmp_path).write_issue(
            reporter="DEV",
            summary="Outage",
            body="prod down",
            severity="crit",  # alias → Severity.CRITICAL
        )
        assert issue.severity is Severity.CRITICAL
        assert "severity: critical\n" in issue.path.read_text(encoding="utf-8")

    def test_sequence_increments_per_day(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        first = project.write_issue(
            reporter="DEV", summary="one", body="x"
        )
        second = project.write_issue(
            reporter="DEV", summary="two", body="y"
        )
        assert first.filename != second.filename

    def test_rejects_empty_summary(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError, match="summary"):
            Project(tmp_path).write_issue(
                reporter="DEV", summary="   ", body="body"
            )

    def test_rejects_bad_reporter(self, tmp_path: Path) -> None:
        with pytest.raises(ValidationError):
            Project(tmp_path).write_issue(
                reporter="lowercase-bad",
                summary="x",
                body="y",
            )

    def test_rejects_unknown_severity(self, tmp_path: Path) -> None:
        # normalize_severity raises ValueError on unknown aliases.
        with pytest.raises(ValueError):
            Project(tmp_path).write_issue(
                reporter="DEV",
                summary="x",
                body="y",
                severity="catastrophic",
            )


# ── read_issue ────────────────────────────────────────────────────────


class TestReadIssue:
    def test_round_trip_by_filename(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        written = project.write_issue(
            reporter="DEV",
            summary="round-trip",
            body="body text",
            severity="low",
        )
        loaded = project.read_issue(written.filename)
        assert loaded.filename == written.filename
        assert loaded.reporter == "DEV"
        assert loaded.severity is Severity.LOW
        assert loaded.summary == "round-trip"
        assert "body text" in loaded.body

    def test_round_trip_by_id(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        written = project.write_issue(
            reporter="DEV", summary="x", body="y"
        )
        # ISSUE-YYYYMMDD-NNN prefix is enough.
        iid = written.filename.rsplit("-DEV.md", 1)[0]
        loaded = project.read_issue(iid)
        assert loaded.filename == written.filename

    def test_missing_raises(self, tmp_path: Path) -> None:
        with pytest.raises(TaskNotFoundError):
            Project(tmp_path).read_issue("ISSUE-20260101-001")


# ── list_issues ───────────────────────────────────────────────────────


class TestListIssues:
    def test_empty_project(self, tmp_path: Path) -> None:
        assert Project(tmp_path).list_issues() == []

    def test_sorted_newest_first(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        first = project.write_issue(
            reporter="DEV", summary="1", body="a"
        )
        second = project.write_issue(
            reporter="DEV", summary="2", body="b"
        )
        # Same day → sorted by sequence descending.
        listing = project.list_issues()
        assert [i.filename for i in listing] == [
            second.filename,
            first.filename,
        ]

    def test_filter_by_reporter(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        dev = project.write_issue(reporter="DEV", summary="d", body="x")
        project.write_issue(reporter="QA", summary="q", body="y")

        only_dev = project.list_issues(reporter="DEV")
        assert [i.filename for i in only_dev] == [dev.filename]

    def test_filter_by_severity(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        low = project.write_issue(
            reporter="DEV", summary="low", body="x", severity="low"
        )
        project.write_issue(
            reporter="DEV", summary="high", body="y", severity="high"
        )

        only_low = project.list_issues(severity="low")
        assert [i.filename for i in only_low] == [low.filename]
        # Severity aliases should also work on the filter side.
        also_low = project.list_issues(severity=Severity.LOW)
        assert [i.filename for i in also_low] == [low.filename]

    def test_limit_and_offset(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        filenames = [
            project.write_issue(
                reporter="DEV", summary=str(i), body="b"
            ).filename
            for i in range(3)
        ]
        expected = list(reversed(filenames))

        page = project.list_issues(limit=2)
        assert [i.filename for i in page] == expected[:2]

        page2 = project.list_issues(limit=2, offset=2)
        assert [i.filename for i in page2] == expected[2:]

    def test_skips_malformed_file(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        good = project.write_issue(
            reporter="DEV", summary="ok", body="body"
        )

        bad = project.issues_dir / "ISSUE-20260423-999-DEV.md"
        bad.write_text("not a yaml header\n", encoding="utf-8")

        listing = project.list_issues()
        assert [i.filename for i in listing] == [good.filename]
