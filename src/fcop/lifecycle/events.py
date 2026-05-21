"""Event layer — the PAST trace (per FCoP 3.0 spec §2).

This module owns the ``transitions:`` array inside an FCoP file's
YAML frontmatter. Every lifecycle ``mv`` MUST append exactly one
event here (Rule E), events are append-only (Rule F), and the array
is **audit-only** — current state is never derived from it (Rule G).

Public surface:

* :class:`TransitionEvent` — one event as an immutable dataclass
* :func:`event_to_mapping` / :func:`event_from_mapping` — round-trip
  between :class:`TransitionEvent` and the plain ``dict`` that lands
  in YAML
* :func:`append_event_to_frontmatter` — given a file's raw text,
  return new text with one event appended to ``transitions:``. Does
  no I/O; the caller drives the write (typically through
  :mod:`fcop.lifecycle.atomic`).
* :func:`read_events` — parse ``transitions:`` out of a file's text,
  for audit/replay use only (never to compute current state).
* :func:`synthetic_baseline_event` — produce the synthetic event the
  v2→v3 migrator stamps onto pre-existing files (per spec §9).

Implementation note: this module uses :mod:`yaml` to round-trip the
frontmatter, the same dependency the rest of fcop already pulls in.
We deliberately do **not** introduce a streaming YAML editor — for
typical FCoP files (frontmatter ≪ 50 lines) the simplicity of full
parse + dump outweighs the cost.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Final

import yaml

from fcop.lifecycle.state import Stage

__all__ = [
    "FRONTMATTER_FENCE",
    "MIGRATION_TOOL_NAME",
    "TransitionEvent",
    "append_event_to_frontmatter",
    "event_from_mapping",
    "event_to_mapping",
    "read_events",
    "synthetic_baseline_event",
]


FRONTMATTER_FENCE: Final[str] = "---"
"""Fence string used by the YAML frontmatter block on disk."""

MIGRATION_TOOL_NAME: Final[str] = "fcop_migrate_v3"
"""Reserved ``tool`` value for the v2→v3 baseline event (spec §9)."""


@dataclass(frozen=True, slots=True)
class TransitionEvent:
    """One witnessed lifecycle transition (per spec §2.2).

    The dataclass is frozen because :class:`TransitionEvent` instances
    represent points in the append-only PAST trace — once constructed,
    nothing about them ever changes.

    Attributes:
        at: ISO-8601 timestamp with timezone. Always timezone-aware.
        from_stage: Source stage, or ``None`` for creation events.
        to_stage: Destination stage.
        by: Actor identifier (agent role code or persistent agent ID).
        tool: The L1 tool that fired this transition (Rule C).
        note: Optional free-form annotation. ``None`` means no note.
        supersedes: Optional reference to an earlier event ID this
            event corrects (per Rule F — corrections are appends,
            never edits).
    """

    at: datetime
    from_stage: Stage | None
    to_stage: Stage
    by: str
    tool: str
    note: str | None = None
    supersedes: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)
    """Forward-compatible bag for unknown optional fields.

    The :func:`event_from_mapping` reader preserves any key it does
    not recognise here so MINOR-version field additions in the
    on-disk schema round-trip cleanly through older readers (per
    spec §10 versioning rules).
    """


def event_to_mapping(event: TransitionEvent) -> dict[str, Any]:
    """Convert an event into the plain dict that lands in YAML.

    The returned mapping preserves insertion order so YAML output is
    deterministic field-by-field: ``at``, ``from``, ``to``, ``by``,
    ``tool``, then optional ``note`` / ``supersedes`` / extras.

    Note: the YAML key for the source stage is ``from`` (a Python
    reserved word), which is why the dataclass attribute is named
    ``from_stage`` while the on-disk key is plain ``from``.
    """
    out: dict[str, Any] = {
        "at": event.at.isoformat(),
        "from": event.from_stage.value if event.from_stage is not None else None,
        "to": event.to_stage.value,
        "by": event.by,
        "tool": event.tool,
    }
    if event.note is not None:
        out["note"] = event.note
    if event.supersedes is not None:
        out["supersedes"] = event.supersedes
    for key, value in event.extra.items():
        # We let extras win for keys not already set, but never
        # overwrite the 5 required fields above — that would let
        # an unknown extra silently corrupt schema-defined fields.
        out.setdefault(key, value)
    return out


_REQUIRED_KEYS: Final[frozenset[str]] = frozenset({"at", "from", "to", "by", "tool"})
_KNOWN_OPTIONAL_KEYS: Final[frozenset[str]] = frozenset({"note", "supersedes"})


def event_from_mapping(mapping: dict[str, Any]) -> TransitionEvent:
    """Parse one event from a YAML-derived mapping.

    Lenient about timestamp format: accepts the canonical ISO-8601
    string we write, anything :meth:`datetime.fromisoformat` understands,
    and an already-parsed :class:`datetime`. A naive datetime is
    treated as UTC.

    Raises:
        ValueError: if any of the 5 required keys is missing, or if
            ``to`` / ``from`` carry a stage name we don't recognise.
    """
    missing = _REQUIRED_KEYS - mapping.keys()
    if missing:
        raise ValueError(
            f"transition event missing required key(s): {sorted(missing)}"
        )

    at_raw = mapping["at"]
    at_dt = (
        at_raw
        if isinstance(at_raw, datetime)
        else datetime.fromisoformat(str(at_raw))
    )
    if at_dt.tzinfo is None:
        at_dt = at_dt.replace(tzinfo=timezone.utc)

    from_raw = mapping["from"]
    from_stage = None if from_raw is None else Stage.from_dirname(str(from_raw))
    to_stage = Stage.from_dirname(str(mapping["to"]))

    extras = {
        k: v
        for k, v in mapping.items()
        if k not in _REQUIRED_KEYS and k not in _KNOWN_OPTIONAL_KEYS
    }

    return TransitionEvent(
        at=at_dt,
        from_stage=from_stage,
        to_stage=to_stage,
        by=str(mapping["by"]),
        tool=str(mapping["tool"]),
        note=None if mapping.get("note") is None else str(mapping["note"]),
        supersedes=(
            None
            if mapping.get("supersedes") is None
            else str(mapping["supersedes"])
        ),
        extra=extras,
    )


def _split_frontmatter(
    text: str,
) -> tuple[dict[str, Any] | None, str, str]:
    """Split a file's text into ``(fm_dict, body, newline_style)``.

    Returns ``(None, original_text, newline)`` when the file has no
    fenced frontmatter block at all — distinct from an empty-but-
    fenced block (``---\\n---``) which legitimately yields an empty
    mapping. ``newline_style`` is ``"\\r\\n"`` for CRLF files,
    ``"\\n"`` otherwise; the writer re-uses it so we don't churn
    line endings on Windows checkouts.
    """
    newline = "\r\n" if "\r\n" in text and "\n" not in text.replace("\r\n", "") else "\n"
    lines = text.splitlines()
    if not lines or lines[0].strip() != FRONTMATTER_FENCE:
        return None, text, newline

    # Find the closing fence.
    end_idx: int | None = None
    for i in range(1, len(lines)):
        if lines[i].strip() == FRONTMATTER_FENCE:
            end_idx = i
            break
    if end_idx is None:
        # Malformed — opening fence with no closer. Treat as no frontmatter.
        return None, text, newline

    fm_block = "\n".join(lines[1:end_idx])
    body_lines = lines[end_idx + 1 :]
    body = newline.join(body_lines)
    # Preserve trailing newline behaviour of the original file.
    if body and not body.endswith(newline) and text.endswith(("\n", "\r\n")):
        body += newline

    parsed = yaml.safe_load(fm_block)
    if parsed is None:
        # Empty frontmatter block (``---\n---``) is structurally valid;
        # treat it as an empty mapping so callers can still seed fields.
        fm: dict[str, Any] = {}
    elif isinstance(parsed, dict):
        fm = parsed
    else:
        raise ValueError(
            "frontmatter is not a YAML mapping; cannot append transition event"
        )
    return fm, body, newline


def _join_frontmatter(fm: dict[str, Any], body: str, newline: str) -> str:
    """Inverse of :func:`_split_frontmatter`."""
    dumped = yaml.safe_dump(
        fm,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
    )
    # yaml.safe_dump always uses \n internally; normalise to file style.
    if newline != "\n":
        dumped = dumped.replace("\n", newline)
    return f"{FRONTMATTER_FENCE}{newline}{dumped}{FRONTMATTER_FENCE}{newline}{body}"


def append_event_to_frontmatter(text: str, event: TransitionEvent) -> str:
    """Return ``text`` with ``event`` appended to the ``transitions:`` array.

    Pure function — does no I/O. The caller is responsible for the
    atomic write (typically via :mod:`fcop.lifecycle.atomic`).

    Behaviour:

    * If the file has no frontmatter block, raises ``ValueError`` —
      v3 protocol files MUST carry frontmatter (spec §2.1).
    * If ``transitions:`` is missing, it is created as a new list.
    * If ``transitions:`` exists but is not a list, raises
      ``ValueError`` — this is a malformed file.
    * The event mapping is appended at the end; per Rule F we never
      mutate earlier entries.

    Raises:
        ValueError: malformed frontmatter, or transitions is not a list.
    """
    fm, body, newline = _split_frontmatter(text)
    if fm is None:
        raise ValueError(
            "file has no YAML frontmatter; cannot append transition event "
            "(spec §2.1 requires frontmatter on every _lifecycle/ file)"
        )

    transitions = fm.get("transitions", [])
    if not isinstance(transitions, list):
        raise ValueError(
            f"frontmatter 'transitions' is not a list "
            f"(found {type(transitions).__name__}); refusing to append"
        )

    transitions.append(event_to_mapping(event))
    fm["transitions"] = transitions
    return _join_frontmatter(fm, body, newline)


def read_events(text: str) -> list[TransitionEvent]:
    """Return the parsed ``transitions:`` array from a file's text.

    For audit and consistency checking **only** (Rule G). Callers
    MUST NOT use this to determine current state — current state is
    the file's directory (Rule A); always go through
    :func:`fcop.lifecycle.state.stage_of_path` for that.

    Returns an empty list when the file has no ``transitions:`` field,
    which is the canonical answer for legal historical artefacts that
    pre-date the v3 event layer (spec §9).
    """
    fm, _body, _newline = _split_frontmatter(text)
    raw = fm.get("transitions") if fm else None
    if not isinstance(raw, list):
        return []
    return [
        event_from_mapping(item)
        for item in raw
        if isinstance(item, dict)
    ]


def synthetic_baseline_event(
    file_path: Path,
    current_stage: Stage,
    *,
    by: str = "migration",
) -> TransitionEvent:
    """Build the synthetic event the v2→v3 migrator stamps on a file.

    Per spec §9, every file moved by ``fcop migrate --to-v3`` receives
    one event with:

    * ``at`` = the file's mtime (as a timezone-aware UTC datetime)
    * ``from`` = ``None``
    * ``to``   = the current stage
    * ``by``   = ``"migration"`` (override via the ``by`` kwarg)
    * ``tool`` = ``"fcop_migrate_v3"``

    The function reads the file's mtime via :func:`Path.stat`; if the
    file does not yet exist on disk (test harnesses, dry runs), the
    current wall-clock time is used instead.
    """
    try:
        mtime = file_path.stat().st_mtime
        at_dt = datetime.fromtimestamp(mtime, tz=timezone.utc)
    except FileNotFoundError:
        at_dt = datetime.now(timezone.utc)

    return TransitionEvent(
        at=at_dt,
        from_stage=None,
        to_stage=current_stage,
        by=by,
        tool=MIGRATION_TOOL_NAME,
    )
