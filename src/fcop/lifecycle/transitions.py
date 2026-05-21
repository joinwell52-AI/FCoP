"""Allowed-transitions table (per FCoP 3.0 spec §1.3).

Encodes the 7 legal ``(from_stage, to_stage)`` pairs and the L1 tool
that owns each one. Everything not in this table is rejected.

This module is **declarative**: it does not perform transitions, it
only describes which transitions are legal and which tool authorises
each one. The actual file move + event append lives in
:mod:`fcop.lifecycle.atomic` and :mod:`fcop.lifecycle.events`.

The 7 transitions (re-stated verbatim from spec §1.3):

    ─────────────  ────────────  ──────────────────────────────
    From           To            Tool
    ─────────────  ────────────  ──────────────────────────────
    (creation)     inbox         create_task
    inbox          active        claim_task
    active         review        submit_task
    active         done          finish_task(skip_review=true)
    review         done          approve_task
    review         active        reject_task
    done           archive       archive_task
    ─────────────  ────────────  ──────────────────────────────

Anything else MUST raise :class:`IllegalTransitionError`. This is
Rule C: *transitions are governed by explicit tool invocation only*
— neither file fields nor role inference may decide which transition
fires, only the tool the caller chose.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from fcop.lifecycle.state import Stage

__all__ = [
    "ALLOWED_TRANSITIONS",
    "IllegalTransitionError",
    "TransitionSpec",
    "is_allowed",
    "tool_for",
    "validate_transition",
]


@dataclass(frozen=True, slots=True)
class TransitionSpec:
    """One row of the allowed-transitions table.

    Attributes:
        from_stage: Source stage, or ``None`` to denote creation
            (the file did not exist on disk before this transition).
        to_stage: Destination stage. Always a real :class:`Stage`.
        tool: Canonical L1 tool name that owns this transition.
            This is the **only** identifier authorised to fire it
            (Rule C).
    """

    from_stage: Stage | None
    to_stage: Stage
    tool: str


# Module-level frozen registry. Tuples (not list) so accidental
# mutation at runtime is impossible — Rule A/B/C all depend on this
# table being immutable.
ALLOWED_TRANSITIONS: Final[tuple[TransitionSpec, ...]] = (
    TransitionSpec(None, Stage.INBOX, "create_task"),
    TransitionSpec(Stage.INBOX, Stage.ACTIVE, "claim_task"),
    TransitionSpec(Stage.ACTIVE, Stage.REVIEW, "submit_task"),
    TransitionSpec(Stage.ACTIVE, Stage.DONE, "finish_task"),
    TransitionSpec(Stage.REVIEW, Stage.DONE, "approve_task"),
    TransitionSpec(Stage.REVIEW, Stage.ACTIVE, "reject_task"),
    TransitionSpec(Stage.DONE, Stage.ARCHIVE, "archive_task"),
)
"""All transitions FCoP 3.0 permits. Anything else MUST be rejected."""


class IllegalTransitionError(Exception):
    """Raised when a caller attempts a transition not in the allowed table.

    This is the protocol-level expression of Rule C. The error
    deliberately does **not** subclass :class:`fcop.errors.FcopError`
    — :mod:`fcop.lifecycle` is designed to be importable standalone
    by minimal hosts that don't want the full ``fcop`` facade. When
    integrating with the wider library, callers should adapt this
    to :class:`fcop.errors.ProtocolViolation` at the boundary.

    Attributes:
        from_stage: The stage the caller tried to leave (or ``None``
            for an unsupported creation target).
        to_stage: The stage the caller tried to enter.
        tool: The tool name the caller invoked, when known.
    """

    def __init__(
        self,
        from_stage: Stage | None,
        to_stage: Stage,
        *,
        tool: str | None = None,
    ) -> None:
        self.from_stage = from_stage
        self.to_stage = to_stage
        self.tool = tool
        origin = "(creation)" if from_stage is None else from_stage.value
        via = f" via tool {tool!r}" if tool else ""
        super().__init__(
            f"Illegal FCoP transition {origin} → {to_stage.value}{via}; "
            f"not in the spec §1.3 allowed-transitions table."
        )


def is_allowed(from_stage: Stage | None, to_stage: Stage) -> bool:
    """Return ``True`` iff ``(from_stage, to_stage)`` is in the table.

    Does not consider the tool — use :func:`validate_transition` when
    you also want to check that the caller's tool matches.
    """
    return any(
        spec.from_stage == from_stage and spec.to_stage == to_stage
        for spec in ALLOWED_TRANSITIONS
    )


def tool_for(from_stage: Stage | None, to_stage: Stage) -> str | None:
    """Return the canonical L1 tool for a given transition, or ``None``.

    Useful for error messages ("you can't move active→archive directly;
    the tool for active→done is ``finish_task``").
    """
    for spec in ALLOWED_TRANSITIONS:
        if spec.from_stage == from_stage and spec.to_stage == to_stage:
            return spec.tool
    return None


def validate_transition(
    from_stage: Stage | None,
    to_stage: Stage,
    *,
    tool: str | None = None,
) -> TransitionSpec:
    """Look up the spec and verify the caller's tool matches.

    Args:
        from_stage: Source stage, or ``None`` for creation.
        to_stage: Destination stage.
        tool: When given, MUST equal the canonical tool for the
            transition; otherwise :class:`IllegalTransitionError`.
            When ``None``, only the ``(from, to)`` pair is checked.

    Returns:
        The matching :class:`TransitionSpec`.

    Raises:
        IllegalTransitionError: If the pair is not in the table, or
            if ``tool`` is given and does not match the canonical one.
    """
    for spec in ALLOWED_TRANSITIONS:
        if spec.from_stage == from_stage and spec.to_stage == to_stage:
            if tool is not None and tool != spec.tool:
                raise IllegalTransitionError(from_stage, to_stage, tool=tool)
            return spec
    raise IllegalTransitionError(from_stage, to_stage, tool=tool)
