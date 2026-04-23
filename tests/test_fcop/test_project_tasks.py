"""Tests for :class:`fcop.Project` task CRUD — the D3-c2 surface.

Goals:
    * ``write_task`` creates well-formed files and returns a Task model
      with the on-disk state, assigning the next sequence for today.
    * Repeated writes on the same day increment the sequence.
    * Round-trips through write → read yield equivalent frontmatter and
      body, so the protocol grammar is self-consistent.
    * ``list_tasks`` filters correctly and orders newest-first.
    * ``read_task`` accepts both full filenames and TASK-ids.
    * Malformed files don't break ``list_tasks``.
"""

from __future__ import annotations

import time
from pathlib import Path

import pytest

from fcop import Project
from fcop.errors import TaskNotFoundError
from fcop.models import Priority, Task

# ── write_task ────────────────────────────────────────────────────────


class TestWriteTask:
    def test_creates_file_with_today_sequence(self, tmp_path: Path) -> None:
        task = Project(tmp_path).write_task(
            sender="ADMIN",
            recipient="PM",
            priority="P1",
            subject="Kick off the release",
            body="Please plan the 0.6 release.",
        )

        assert isinstance(task, Task)
        assert task.sequence == 1  # first task of the day
        assert task.path.is_file()
        assert task.path == tmp_path / "docs" / "agents" / "tasks" / task.filename
        assert task.filename.startswith("TASK-")
        assert task.filename.endswith("-ADMIN-to-PM.md")
        assert task.is_archived is False

    def test_frontmatter_contains_core_fields(self, tmp_path: Path) -> None:
        task = Project(tmp_path).write_task(
            sender="ADMIN",
            recipient="PM",
            priority=Priority.P0,
            subject="Urgent review",
            body="Details below.",
            references=("TASK-20260101-002", "TASK-20260101-003"),
            thread_key="release-0.6",
        )

        text = task.path.read_text(encoding="utf-8")
        assert text.startswith("---\n")
        assert "protocol: fcop\n" in text
        assert "version: 1\n" in text
        assert "sender: ADMIN\n" in text
        assert "recipient: PM\n" in text
        assert "priority: P0\n" in text
        assert "subject: Urgent review\n" in text
        assert "thread_key: release-0.6\n" in text
        # References should be emitted as a YAML block/flow list.
        assert "references:" in text
        # Body is preserved verbatim after the closing fence.
        assert text.rstrip().endswith("Details below.")

    def test_priority_alias_accepted(self, tmp_path: Path) -> None:
        # "urgent" → P0 per fcop.core.schema.PRIORITY_ALIASES; write_task
        # should normalize on our behalf so callers never see the raw
        # string in their output.
        task = Project(tmp_path).write_task(
            sender="ADMIN",
            recipient="PM",
            priority="urgent",
            subject="x",
            body="y",
        )
        assert task.priority is Priority.P0
        assert "priority: P0\n" in task.path.read_text(encoding="utf-8")

    def test_priority_unknown_raises(self, tmp_path: Path) -> None:
        # Unknown aliases must fail loudly — silently downgrading would
        # mask typos in AI-authored code.
        with pytest.raises(ValueError, match="unknown priority"):
            Project(tmp_path).write_task(
                sender="ADMIN",
                recipient="PM",
                priority="whatever",
                subject="x",
                body="y",
            )

    def test_sequence_increments_across_writes(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        first = project.write_task(
            sender="ADMIN", recipient="PM", priority="P2",
            subject="a", body="a",
        )
        second = project.write_task(
            sender="ADMIN", recipient="PM", priority="P2",
            subject="b", body="b",
        )
        third = project.write_task(
            sender="PM", recipient="DEV", priority="P2",
            subject="c", body="c",
        )
        assert first.sequence == 1
        assert second.sequence == 2
        assert third.sequence == 3  # sequence is per-day, not per-sender

    def test_creates_tasks_dir_if_missing(self, tmp_path: Path) -> None:
        assert not (tmp_path / "docs").exists()
        task = Project(tmp_path).write_task(
            sender="ADMIN", recipient="PM", priority="P2",
            subject="x", body="y",
        )
        assert task.path.parent.is_dir()

    def test_slot_appears_in_filename(self, tmp_path: Path) -> None:
        # Slot lets writers target a sub-role like DEV.BACKEND without
        # inventing a whole new role code.
        task = Project(tmp_path).write_task(
            sender="PM", recipient="DEV", slot="BACKEND",
            priority="P2", subject="x", body="y",
        )
        assert ".BACKEND.md" in task.filename

    def test_invalid_role_code_raises(self, tmp_path: Path) -> None:
        # Lowercase sender should blow up in build_task_filename.
        with pytest.raises(ValueError, match="filename"):
            Project(tmp_path).write_task(
                sender="admin",  # lowercase → rejected by grammar
                recipient="PM", priority="P2",
                subject="x", body="y",
            )

    def test_file_is_placed_atomically(self, tmp_path: Path) -> None:
        # After write_task returns, there should be no .tmp or .part
        # leftovers in the tasks directory — writes are either committed
        # under the final filename or not present at all.
        project = Project(tmp_path)
        task = project.write_task(
            sender="ADMIN", recipient="PM", priority="P2",
            subject="x", body="y",
        )
        entries = list(task.path.parent.iterdir())
        assert entries == [task.path]


# ── round-trip ────────────────────────────────────────────────────────


class TestRoundTrip:
    """Write a task, then read it back — the frontmatter and body must
    be semantically identical. This is the canary that tells us the
    filename grammar and YAML serialization stay in sync."""

    def test_read_after_write_recovers_fields(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        written = project.write_task(
            sender="ADMIN", recipient="PM", priority="P1",
            subject="Round-trip",
            body="Some body content.",
            references=("TASK-20260101-009",),
            thread_key="thr-1",
        )

        loaded = project.read_task(written.filename)

        assert loaded.sender == "ADMIN"
        assert loaded.recipient == "PM"
        assert loaded.priority is Priority.P1
        assert loaded.subject == "Round-trip"
        assert loaded.frontmatter.thread_key == "thr-1"
        assert loaded.frontmatter.references == ("TASK-20260101-009",)
        assert "Some body content." in loaded.body
        assert loaded.is_archived is False

    def test_read_by_task_id(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        written = project.write_task(
            sender="ADMIN", recipient="PM", priority="P2",
            subject="x", body="y",
        )
        loaded = project.read_task(written.task_id)
        assert loaded.filename == written.filename

    def test_read_archived_task(self, tmp_path: Path) -> None:
        # Manually place a file under log/tasks/ and confirm read_task
        # finds it and flags it archived. (archive_task itself lands
        # in a later slice — we pre-stage the file here.)
        log_tasks = tmp_path / "docs" / "agents" / "log" / "tasks"
        log_tasks.mkdir(parents=True)
        fname = "TASK-20250101-001-ADMIN-to-PM.md"
        body = (
            "---\n"
            "protocol: fcop\n"
            "version: 1\n"
            "sender: ADMIN\n"
            "recipient: PM\n"
            "priority: P2\n"
            "---\n\n"
            "body\n"
        )
        (log_tasks / fname).write_text(body, encoding="utf-8")

        loaded = Project(tmp_path).read_task(fname)
        assert loaded.is_archived is True

    def test_read_missing_raises(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        with pytest.raises(TaskNotFoundError) as excinfo:
            project.read_task("TASK-20991231-001-ADMIN-to-PM.md")
        assert excinfo.value.query == "TASK-20991231-001-ADMIN-to-PM.md"

    def test_read_by_unmatched_id(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        project.write_task(
            sender="ADMIN", recipient="PM", priority="P2",
            subject="x", body="y",
        )
        with pytest.raises(TaskNotFoundError):
            project.read_task("TASK-19990101-001")  # id that doesn't exist


# ── list_tasks ────────────────────────────────────────────────────────


class TestListTasks:
    def test_empty(self, tmp_path: Path) -> None:
        assert Project(tmp_path).list_tasks() == []

    def test_newest_first(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        t1 = project.write_task(
            sender="ADMIN", recipient="PM", priority="P2",
            subject="one", body="b",
        )
        t2 = project.write_task(
            sender="ADMIN", recipient="PM", priority="P2",
            subject="two", body="b",
        )
        tasks = project.list_tasks()
        # Same-day write order: higher sequence appears first.
        assert [t.filename for t in tasks] == [t2.filename, t1.filename]

    def test_filter_by_sender(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        project.write_task(
            sender="ADMIN", recipient="PM", priority="P2",
            subject="x", body="y",
        )
        project.write_task(
            sender="PM", recipient="DEV", priority="P2",
            subject="x", body="y",
        )
        pm_sent = project.list_tasks(sender="PM")
        assert len(pm_sent) == 1
        assert pm_sent[0].sender == "PM"

    def test_filter_by_recipient(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        project.write_task(
            sender="ADMIN", recipient="PM", priority="P2",
            subject="x", body="y",
        )
        project.write_task(
            sender="ADMIN", recipient="DEV", priority="P2",
            subject="x", body="y",
        )
        dev_inbox = project.list_tasks(recipient="DEV")
        assert len(dev_inbox) == 1
        assert dev_inbox[0].recipient == "DEV"

    def test_status_archived_excluded_by_default(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        project.write_task(
            sender="ADMIN", recipient="PM", priority="P2",
            subject="open", body="b",
        )

        log_tasks = tmp_path / "docs" / "agents" / "log" / "tasks"
        log_tasks.mkdir(parents=True)
        (log_tasks / "TASK-20250101-001-ADMIN-to-PM.md").write_text(
            "---\nprotocol: fcop\nversion: 1\nsender: ADMIN\n"
            "recipient: PM\npriority: P2\n---\n\narchived\n",
            encoding="utf-8",
        )

        open_only = project.list_tasks(status="open")
        all_tasks = project.list_tasks(status="all")
        archived_only = project.list_tasks(status="archived")

        assert len(open_only) == 1
        assert open_only[0].is_archived is False
        assert len(archived_only) == 1
        assert archived_only[0].is_archived is True
        assert len(all_tasks) == 2

    def test_filter_by_date(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        project.write_task(
            sender="ADMIN", recipient="PM", priority="P2",
            subject="x", body="y",
        )
        today = project.list_tasks()[0].date

        # Stage a file dated yesterday by hand.
        tasks_dir = project.tasks_dir
        stale = tasks_dir / "TASK-20250101-001-ADMIN-to-PM.md"
        stale.write_text(
            "---\nprotocol: fcop\nversion: 1\nsender: ADMIN\n"
            "recipient: PM\npriority: P2\n---\n\nold\n",
            encoding="utf-8",
        )

        today_only = project.list_tasks(date=today)
        assert len(today_only) == 1
        yesterday_only = project.list_tasks(date="20250101")
        assert len(yesterday_only) == 1
        assert yesterday_only[0].filename == stale.name

    def test_limit_and_offset(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        for _ in range(5):
            project.write_task(
                sender="ADMIN", recipient="PM", priority="P2",
                subject="x", body="y",
            )
        assert len(project.list_tasks(limit=2)) == 2
        window = project.list_tasks(limit=2, offset=1)
        assert len(window) == 2
        # offset=1 + limit=2 = entries 2 and 3 from newest-first.
        full = project.list_tasks()
        assert window == full[1:3]

    def test_malformed_file_is_skipped(self, tmp_path: Path) -> None:
        # A wrecked YAML block should not take down list_tasks — agents
        # rely on it to get an overview even when the project is partly
        # broken.
        project = Project(tmp_path)
        project.write_task(
            sender="ADMIN", recipient="PM", priority="P2",
            subject="x", body="y",
        )
        broken = project.tasks_dir / "TASK-20260101-050-ADMIN-to-PM.md"
        broken.write_text(
            "---\nnot: valid\nfrontmatter: here\n---\nbody\n",
            encoding="utf-8",
        )
        tasks = project.list_tasks()
        assert len(tasks) == 1  # only the good one survives
        assert tasks[0].sender == "ADMIN"


# ── atomicity (shallow) ───────────────────────────────────────────────


class TestConcurrencyGuards:
    """Shallow race-condition guards — true concurrency testing belongs
    in an integration suite, but we can smoke-test the O_EXCL reservation
    path by pre-creating the file the writer would have chosen."""

    def test_existing_file_forces_retry(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        tasks_dir = project.tasks_dir
        tasks_dir.mkdir(parents=True, exist_ok=True)

        # Pre-reserve seq 001 manually (as a competing writer might).
        today = time.strftime("%Y%m%d")
        squatter = tasks_dir / f"TASK-{today}-001-PM-to-DEV.md"
        squatter.write_text(
            "---\nprotocol: fcop\nversion: 1\nsender: PM\n"
            "recipient: DEV\npriority: P2\n---\n\nprior\n",
            encoding="utf-8",
        )

        task = project.write_task(
            sender="ADMIN", recipient="PM", priority="P2",
            subject="x", body="y",
        )
        # next_sequence should detect seq 001 is taken and pick 002.
        assert task.sequence == 2
        # The squatter file is untouched.
        assert squatter.read_text(encoding="utf-8").endswith("prior\n")
