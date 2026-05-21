"""Tests for fcop.lifecycle.transitions — Rule C and the 7-row table."""

from __future__ import annotations

import pytest

from fcop.lifecycle.state import Stage
from fcop.lifecycle.transitions import (
    ALLOWED_TRANSITIONS,
    IllegalTransitionError,
    is_allowed,
    tool_for,
    validate_transition,
)


class TestAllowedTable:
    def test_exactly_seven_rows(self) -> None:
        # Spec §1.3 mandates exactly 7 legal transitions.
        assert len(ALLOWED_TRANSITIONS) == 7

    def test_canonical_rows(self) -> None:
        rows = {(s.from_stage, s.to_stage, s.tool) for s in ALLOWED_TRANSITIONS}
        assert rows == {
            (None, Stage.INBOX, "create_task"),
            (Stage.INBOX, Stage.ACTIVE, "claim_task"),
            (Stage.ACTIVE, Stage.REVIEW, "submit_task"),
            (Stage.ACTIVE, Stage.DONE, "finish_task"),
            (Stage.REVIEW, Stage.DONE, "approve_task"),
            (Stage.REVIEW, Stage.ACTIVE, "reject_task"),
            (Stage.DONE, Stage.ARCHIVE, "archive_task"),
        }

    def test_table_is_immutable(self) -> None:
        # Should be a tuple, not a list — Rule C protection.
        assert isinstance(ALLOWED_TRANSITIONS, tuple)


class TestIsAllowed:
    @pytest.mark.parametrize(
        ("frm", "to"),
        [
            (None, Stage.INBOX),
            (Stage.INBOX, Stage.ACTIVE),
            (Stage.ACTIVE, Stage.REVIEW),
            (Stage.ACTIVE, Stage.DONE),
            (Stage.REVIEW, Stage.DONE),
            (Stage.REVIEW, Stage.ACTIVE),
            (Stage.DONE, Stage.ARCHIVE),
        ],
    )
    def test_legal_pairs(self, frm: Stage | None, to: Stage) -> None:
        assert is_allowed(frm, to) is True

    @pytest.mark.parametrize(
        ("frm", "to"),
        [
            # Inbox → Done (skipping active) — illegal.
            (Stage.INBOX, Stage.DONE),
            # Active → Archive (skipping done) — illegal.
            (Stage.ACTIVE, Stage.ARCHIVE),
            # Archive → anywhere — illegal (archive is terminal).
            (Stage.ARCHIVE, Stage.INBOX),
            (Stage.ARCHIVE, Stage.DONE),
            # Same-stage self-loop — illegal.
            (Stage.ACTIVE, Stage.ACTIVE),
            # Re-creation — only None → INBOX is legal.
            (None, Stage.ACTIVE),
            (None, Stage.DONE),
        ],
    )
    def test_illegal_pairs(self, frm: Stage | None, to: Stage) -> None:
        assert is_allowed(frm, to) is False


class TestToolFor:
    def test_known_pair_returns_tool(self) -> None:
        assert tool_for(Stage.REVIEW, Stage.DONE) == "approve_task"

    def test_unknown_pair_returns_none(self) -> None:
        assert tool_for(Stage.ARCHIVE, Stage.INBOX) is None


class TestValidateTransition:
    def test_legal_pair_no_tool(self) -> None:
        spec = validate_transition(Stage.INBOX, Stage.ACTIVE)
        assert spec.tool == "claim_task"

    def test_legal_pair_with_correct_tool(self) -> None:
        spec = validate_transition(
            Stage.INBOX, Stage.ACTIVE, tool="claim_task"
        )
        assert spec.from_stage == Stage.INBOX

    def test_legal_pair_with_wrong_tool_raises(self) -> None:
        with pytest.raises(IllegalTransitionError) as excinfo:
            validate_transition(
                Stage.INBOX, Stage.ACTIVE, tool="finish_task"
            )
        assert excinfo.value.tool == "finish_task"
        assert excinfo.value.from_stage == Stage.INBOX
        assert excinfo.value.to_stage == Stage.ACTIVE

    def test_illegal_pair_raises(self) -> None:
        with pytest.raises(IllegalTransitionError) as excinfo:
            validate_transition(Stage.INBOX, Stage.DONE)
        assert excinfo.value.from_stage == Stage.INBOX
        assert excinfo.value.to_stage == Stage.DONE

    def test_error_message_mentions_origin_and_destination(self) -> None:
        with pytest.raises(IllegalTransitionError, match="inbox → done"):
            validate_transition(Stage.INBOX, Stage.DONE)

    def test_error_message_for_creation(self) -> None:
        with pytest.raises(IllegalTransitionError, match=r"\(creation\) → active"):
            validate_transition(None, Stage.ACTIVE, tool="create_task")
