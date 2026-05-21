"""Tests for fcop.lifecycle.events — Rules E / F / G."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from fcop.lifecycle.events import (
    MIGRATION_TOOL_NAME,
    TransitionEvent,
    append_event_to_frontmatter,
    event_from_mapping,
    event_to_mapping,
    read_events,
    synthetic_baseline_event,
)
from fcop.lifecycle.state import Stage


def _make_event(
    *,
    from_stage: Stage | None = Stage.INBOX,
    to_stage: Stage = Stage.ACTIVE,
    by: str = "DEV-01",
    tool: str = "claim_task",
    note: str | None = None,
) -> TransitionEvent:
    return TransitionEvent(
        at=datetime(2026, 5, 21, 10, 15, 0, tzinfo=timezone.utc),
        from_stage=from_stage,
        to_stage=to_stage,
        by=by,
        tool=tool,
        note=note,
    )


class TestEventMappingRoundtrip:
    def test_to_mapping_required_keys(self) -> None:
        m = event_to_mapping(_make_event())
        assert m["at"] == "2026-05-21T10:15:00+00:00"
        assert m["from"] == "inbox"
        assert m["to"] == "active"
        assert m["by"] == "DEV-01"
        assert m["tool"] == "claim_task"

    def test_to_mapping_skips_none_optional(self) -> None:
        m = event_to_mapping(_make_event())
        assert "note" not in m
        assert "supersedes" not in m

    def test_to_mapping_creation_event(self) -> None:
        m = event_to_mapping(
            _make_event(from_stage=None, to_stage=Stage.INBOX, tool="create_task")
        )
        assert m["from"] is None

    def test_from_mapping_roundtrip(self) -> None:
        original = _make_event(note="claimed by dev")
        m = event_to_mapping(original)
        parsed = event_from_mapping(m)
        assert parsed == original

    def test_from_mapping_rejects_missing_required(self) -> None:
        with pytest.raises(ValueError, match="missing required key"):
            event_from_mapping({"at": "2026-05-21T10:00:00+00:00", "to": "inbox"})

    def test_from_mapping_naive_datetime_becomes_utc(self) -> None:
        m = {
            "at": datetime(2026, 5, 21, 10, 0),
            "from": None,
            "to": "inbox",
            "by": "PM",
            "tool": "create_task",
        }
        parsed = event_from_mapping(m)
        assert parsed.at.tzinfo is not None

    def test_from_mapping_preserves_extra_fields(self) -> None:
        m = {
            "at": "2026-05-21T10:00:00+00:00",
            "from": None,
            "to": "inbox",
            "by": "PM",
            "tool": "create_task",
            "future_field": "value",
        }
        parsed = event_from_mapping(m)
        assert parsed.extra == {"future_field": "value"}


class TestAppendEventToFrontmatter:
    def test_append_to_existing_transitions_array(self) -> None:
        original = (
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
            "body line\n"
        )
        new_text = append_event_to_frontmatter(original, _make_event())
        events = read_events(new_text)
        assert len(events) == 2
        assert events[0].to_stage == Stage.INBOX
        assert events[1].to_stage == Stage.ACTIVE
        assert events[1].tool == "claim_task"

    def test_append_creates_transitions_when_missing(self) -> None:
        original = (
            "---\n"
            "protocol: fcop\n"
            "version: 3\n"
            "---\n"
            "body\n"
        )
        new_text = append_event_to_frontmatter(original, _make_event())
        events = read_events(new_text)
        assert len(events) == 1

    def test_append_preserves_body(self) -> None:
        body = "## Heading\n\nSome body content with `code`.\n"
        original = f"---\nprotocol: fcop\nversion: 3\n---\n{body}"
        new_text = append_event_to_frontmatter(original, _make_event())
        assert body in new_text

    def test_append_to_file_without_frontmatter_raises(self) -> None:
        with pytest.raises(ValueError, match="no YAML frontmatter"):
            append_event_to_frontmatter("just a body\n", _make_event())

    def test_append_when_transitions_not_list_raises(self) -> None:
        original = (
            "---\n"
            "protocol: fcop\n"
            "transitions: 'not a list'\n"
            "---\n"
            "body\n"
        )
        with pytest.raises(ValueError, match="not a list"):
            append_event_to_frontmatter(original, _make_event())

    def test_appended_event_at_end_rule_f(self) -> None:
        """Rule F: appends go at the end; earlier events never move."""
        original = (
            "---\n"
            "transitions:\n"
            "  - at: '2026-05-21T10:00:00+00:00'\n"
            "    from: null\n"
            "    to: inbox\n"
            "    by: PM\n"
            "    tool: create_task\n"
            "---\n"
            "body\n"
        )
        new_text = append_event_to_frontmatter(original, _make_event())
        events = read_events(new_text)
        # The PM creation event must still be index 0 — never reordered.
        assert events[0].by == "PM"
        assert events[0].tool == "create_task"


class TestReadEvents:
    def test_empty_when_no_frontmatter(self) -> None:
        assert read_events("just body\n") == []

    def test_empty_when_no_transitions_key(self) -> None:
        text = "---\nprotocol: fcop\n---\nbody\n"
        assert read_events(text) == []

    def test_audit_only_use_rule_g(self) -> None:
        """read_events MUST NOT be used to compute current state.

        We assert this by example: the events claim the file is
        currently DONE, but Rule A says path is truth. read_events
        just returns the history — judging current state from it is
        the caller's mistake (which Rule G forbids).
        """
        text = (
            "---\n"
            "transitions:\n"
            "  - at: '2026-05-21T10:00:00+00:00'\n"
            "    from: null\n"
            "    to: inbox\n"
            "    by: PM\n"
            "    tool: create_task\n"
            "  - at: '2026-05-21T11:00:00+00:00'\n"
            "    from: inbox\n"
            "    to: active\n"
            "    by: DEV\n"
            "    tool: claim_task\n"
            "  - at: '2026-05-21T12:00:00+00:00'\n"
            "    from: active\n"
            "    to: done\n"
            "    by: DEV\n"
            "    tool: finish_task\n"
            "---\n"
        )
        events = read_events(text)
        assert len(events) == 3
        # Note we do NOT assert "current state is done". That would
        # be Rule G violation. The file's path (which lives outside
        # this text) is the only authority on current state.


class TestSyntheticBaselineEvent:
    def test_uses_file_mtime_when_present(self, tmp_path: Path) -> None:
        f = tmp_path / "TASK-x.md"
        f.write_text("body", encoding="utf-8")
        event = synthetic_baseline_event(f, Stage.INBOX)
        assert event.tool == MIGRATION_TOOL_NAME
        assert event.by == "migration"
        assert event.from_stage is None
        assert event.to_stage == Stage.INBOX
        # The mtime is set by the write_text call → tzinfo present.
        assert event.at.tzinfo is not None

    def test_falls_back_to_now_when_file_missing(self, tmp_path: Path) -> None:
        ghost = tmp_path / "does-not-exist.md"
        event = synthetic_baseline_event(ghost, Stage.ARCHIVE)
        assert event.tool == MIGRATION_TOOL_NAME
        assert event.to_stage == Stage.ARCHIVE
