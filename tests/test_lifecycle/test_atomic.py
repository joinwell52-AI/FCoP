"""Tests for fcop.lifecycle.atomic — the write-then-rename commit point."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from fcop.lifecycle.atomic import (
    AtomicCommitResult,
    commit,
    create,
)
from fcop.lifecycle.events import TransitionEvent, read_events
from fcop.lifecycle.state import (
    LIFECYCLE_DIRNAME,
    Stage,
    ensure_lifecycle_dirs,
    stage_of_path,
)
from fcop.lifecycle.transitions import IllegalTransitionError


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _seed_inbox_file(project_root: Path, name: str = "TASK-x.md") -> Path:
    """Drop a v3-shaped file into inbox/ with one creation event."""
    ensure_lifecycle_dirs(project_root)
    f = project_root / LIFECYCLE_DIRNAME / "inbox" / name
    f.write_text(
        "---\n"
        "protocol: fcop\n"
        "version: 3\n"
        "type: TASK\n"
        "transitions:\n"
        "  - at: '2026-05-21T10:00:00+00:00'\n"
        "    from: null\n"
        "    to: inbox\n"
        "    by: PM\n"
        "    tool: create_task\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    return f


class TestCreate:
    def test_creates_file_in_inbox(self, tmp_path: Path) -> None:
        ensure_lifecycle_dirs(tmp_path)
        event = TransitionEvent(
            at=_now(),
            from_stage=None,
            to_stage=Stage.INBOX,
            by="PM",
            tool="create_task",
        )
        result = create(
            "TASK-20260521-001-PM-to-DEV.md",
            "---\nprotocol: fcop\nversion: 3\n---\nbody\n",
            event,
            project_root=tmp_path,
        )
        assert isinstance(result, AtomicCommitResult)
        assert result.source_path is None
        assert result.destination_path.parent.name == "inbox"
        assert result.destination_path.exists()

    def test_appends_creation_event_to_frontmatter(self, tmp_path: Path) -> None:
        ensure_lifecycle_dirs(tmp_path)
        event = TransitionEvent(
            at=_now(),
            from_stage=None,
            to_stage=Stage.INBOX,
            by="PM",
            tool="create_task",
        )
        result = create(
            "TASK-x.md",
            "---\nprotocol: fcop\n---\nbody\n",
            event,
            project_root=tmp_path,
        )
        events = read_events(result.destination_path.read_text(encoding="utf-8"))
        assert len(events) == 1
        assert events[0].tool == "create_task"

    def test_refuses_filename_with_separator(self, tmp_path: Path) -> None:
        ensure_lifecycle_dirs(tmp_path)
        event = TransitionEvent(
            at=_now(),
            from_stage=None,
            to_stage=Stage.INBOX,
            by="PM",
            tool="create_task",
        )
        with pytest.raises(ValueError, match="path separators"):
            create(
                "subdir/TASK-x.md",
                "---\n---\nbody\n",
                event,
                project_root=tmp_path,
            )

    def test_refuses_when_event_has_from_stage(self, tmp_path: Path) -> None:
        ensure_lifecycle_dirs(tmp_path)
        bad_event = TransitionEvent(
            at=_now(),
            from_stage=Stage.INBOX,  # creation cannot have a from_stage
            to_stage=Stage.INBOX,
            by="PM",
            tool="create_task",
        )
        with pytest.raises(IllegalTransitionError):
            create("TASK-x.md", "---\n---\nbody\n", bad_event, project_root=tmp_path)

    def test_refuses_when_target_exists(self, tmp_path: Path) -> None:
        ensure_lifecycle_dirs(tmp_path)
        event = TransitionEvent(
            at=_now(),
            from_stage=None,
            to_stage=Stage.INBOX,
            by="PM",
            tool="create_task",
        )
        create("TASK-x.md", "---\n---\n", event, project_root=tmp_path)
        with pytest.raises(FileExistsError):
            create("TASK-x.md", "---\n---\n", event, project_root=tmp_path)


class TestCommit:
    def test_inbox_to_active(self, tmp_path: Path) -> None:
        f = _seed_inbox_file(tmp_path)
        event = TransitionEvent(
            at=_now(),
            from_stage=Stage.INBOX,
            to_stage=Stage.ACTIVE,
            by="DEV",
            tool="claim_task",
        )
        result = commit(f, Stage.ACTIVE, event, project_root=tmp_path)
        assert not f.exists()  # source removed
        assert result.destination_path.exists()
        assert (
            stage_of_path(result.destination_path, project_root=tmp_path)
            == Stage.ACTIVE
        )

    def test_event_witnessed_in_destination_file(self, tmp_path: Path) -> None:
        f = _seed_inbox_file(tmp_path)
        event = TransitionEvent(
            at=_now(),
            from_stage=Stage.INBOX,
            to_stage=Stage.ACTIVE,
            by="DEV",
            tool="claim_task",
        )
        result = commit(f, Stage.ACTIVE, event, project_root=tmp_path)
        events = read_events(result.destination_path.read_text(encoding="utf-8"))
        # Creation event + claim event = 2.
        assert len(events) == 2
        assert events[-1].tool == "claim_task"
        assert events[-1].by == "DEV"

    def test_no_intermediate_temp_lingers(self, tmp_path: Path) -> None:
        """After a successful commit, no .fcop-*.tmp must remain."""
        f = _seed_inbox_file(tmp_path)
        event = TransitionEvent(
            at=_now(),
            from_stage=Stage.INBOX,
            to_stage=Stage.ACTIVE,
            by="DEV",
            tool="claim_task",
        )
        commit(f, Stage.ACTIVE, event, project_root=tmp_path)
        root = tmp_path / LIFECYCLE_DIRNAME
        leaked = [p for p in root.rglob(".fcop-*.tmp")]
        assert leaked == []

    def test_refuses_skipping_stage(self, tmp_path: Path) -> None:
        """inbox → done is not in the allowed table."""
        f = _seed_inbox_file(tmp_path)
        bad = TransitionEvent(
            at=_now(),
            from_stage=Stage.INBOX,
            to_stage=Stage.DONE,
            by="DEV",
            tool="finish_task",
        )
        with pytest.raises(IllegalTransitionError):
            commit(f, Stage.DONE, bad, project_root=tmp_path)
        # File must remain in inbox after the rejected attempt.
        assert f.exists()

    def test_refuses_wrong_tool(self, tmp_path: Path) -> None:
        f = _seed_inbox_file(tmp_path)
        wrong_tool = TransitionEvent(
            at=_now(),
            from_stage=Stage.INBOX,
            to_stage=Stage.ACTIVE,
            by="DEV",
            tool="finish_task",  # legitimate tool but wrong for this pair
        )
        with pytest.raises(IllegalTransitionError):
            commit(f, Stage.ACTIVE, wrong_tool, project_root=tmp_path)
        assert f.exists()

    def test_refuses_event_to_stage_mismatch(self, tmp_path: Path) -> None:
        f = _seed_inbox_file(tmp_path)
        # event says ACTIVE but caller passes REVIEW — mismatch.
        event = TransitionEvent(
            at=_now(),
            from_stage=Stage.INBOX,
            to_stage=Stage.ACTIVE,
            by="DEV",
            tool="claim_task",
        )
        with pytest.raises(IllegalTransitionError):
            commit(f, Stage.REVIEW, event, project_root=tmp_path)

    def test_refuses_event_from_stage_mismatch(self, tmp_path: Path) -> None:
        f = _seed_inbox_file(tmp_path)
        # Source file is in inbox/, but event claims it came from active/.
        event = TransitionEvent(
            at=_now(),
            from_stage=Stage.ACTIVE,
            to_stage=Stage.REVIEW,
            by="DEV",
            tool="submit_task",
        )
        with pytest.raises(IllegalTransitionError):
            commit(f, Stage.REVIEW, event, project_root=tmp_path)

    def test_full_happy_path_chain(self, tmp_path: Path) -> None:
        """End-to-end: inbox → active → review → done → archive."""
        f = _seed_inbox_file(tmp_path, name="TASK-chain.md")

        chain: list[tuple[Stage, Stage, str, str]] = [
            (Stage.INBOX, Stage.ACTIVE, "claim_task", "DEV"),
            (Stage.ACTIVE, Stage.REVIEW, "submit_task", "DEV"),
            (Stage.REVIEW, Stage.DONE, "approve_task", "REVIEWER"),
            (Stage.DONE, Stage.ARCHIVE, "archive_task", "ADMIN"),
        ]

        current = f
        for frm, to, tool, by in chain:
            event = TransitionEvent(
                at=_now(),
                from_stage=frm,
                to_stage=to,
                by=by,
                tool=tool,
            )
            result = commit(current, to, event, project_root=tmp_path)
            current = result.destination_path
            assert stage_of_path(current, project_root=tmp_path) == to

        # Final file holds all 5 events (creation + 4 transitions).
        events = read_events(current.read_text(encoding="utf-8"))
        assert len(events) == 5
        assert [e.to_stage for e in events] == [
            Stage.INBOX,
            Stage.ACTIVE,
            Stage.REVIEW,
            Stage.DONE,
            Stage.ARCHIVE,
        ]

    def test_source_file_missing_raises(self, tmp_path: Path) -> None:
        ensure_lifecycle_dirs(tmp_path)
        ghost = tmp_path / LIFECYCLE_DIRNAME / "inbox" / "ghost.md"
        event = TransitionEvent(
            at=_now(),
            from_stage=Stage.INBOX,
            to_stage=Stage.ACTIVE,
            by="DEV",
            tool="claim_task",
        )
        with pytest.raises(FileNotFoundError):
            commit(ghost, Stage.ACTIVE, event, project_root=tmp_path)
