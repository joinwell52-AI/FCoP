"""FCoP filename grammar — parse, build, and allocate sequence numbers.

The FCoP protocol encodes routing metadata (sender, recipient, date,
ordering) directly in the filename so files are self-describing on disk
without any index. This module is the single source of truth for that
grammar.

Grammars (all fullmatch, ASCII, uppercase role codes):

- **Task**: ``TASK-{YYYYMMDD}-{NNN}-{SENDER}-to-{RECIPIENT}[.SLOT].md``
- **Report**: ``REPORT-{YYYYMMDD}-{NNN}-{REPORTER}-to-{RECIPIENT}.md``
- **Issue**: ``ISSUE-{YYYYMMDD}-{NNN}-{REPORTER}.md``

Where ``{NNN}`` is a 3-digit zero-padded per-day sequence (001..999) and
``{SLOT}`` is an optional dot-separated role qualifier on task
recipients (e.g. ``to-DEV.BACKEND``). Role codes inside a filename
follow the rules in :mod:`fcop.core.schema` — the regex groups are
written so that ``LEAD-QA-to-AUTO-TESTER.md`` parses cleanly despite
the internal hyphens colliding visually with the ``-to-`` separator.

This module is pure: no filesystem I/O. Callers that need directory
scans (for :func:`next_sequence`) pass an iterable of filenames.

See adr/ADR-0001-library-api.md ("filename.py ← 文件名解析/构造") for
the rationale.
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date as _date
from typing import Literal

from fcop.models import ValidationIssue

__all__ = [
    # Constants
    "TASK_FILENAME_PREFIX",
    "REPORT_FILENAME_PREFIX",
    "ISSUE_FILENAME_PREFIX",
    "TASK_FILENAME_RE",
    "REPORT_FILENAME_RE",
    "ISSUE_FILENAME_RE",
    "DATE_RE",
    "MAX_SEQUENCE",
    # Structural types
    "TaskFilename",
    "ReportFilename",
    "IssueFilename",
    "FilenameKind",
    # Parse / build
    "parse_task_filename",
    "parse_report_filename",
    "parse_issue_filename",
    "build_task_filename",
    "build_report_filename",
    "build_issue_filename",
    # Validators & helpers
    "validate_date",
    "validate_sequence",
    "next_sequence",
    "today_iso",
]


# ── Constants ────────────────────────────────────────────────────────

TASK_FILENAME_PREFIX: str = "TASK"
REPORT_FILENAME_PREFIX: str = "REPORT"
ISSUE_FILENAME_PREFIX: str = "ISSUE"

MAX_SEQUENCE: int = 999
"""Largest per-day sequence number the 3-digit field can encode."""

FilenameKind = Literal["task", "report", "issue"]


# The role-code subpattern here must match :data:`fcop.core.schema.ROLE_CODE_RE`
# exactly (minus the anchors). Duplicated on purpose so the regex is
# self-contained; a unit test pins them to the same shape.
_ROLE = r"[A-Z][A-Z0-9_]*(?:-[A-Z0-9_]+)*"

DATE_RE: re.Pattern[str] = re.compile(r"^\d{8}$")
"""Lexical shape of the ``YYYYMMDD`` date field.

Calendar validity (e.g. no February 30th) is checked separately in
:func:`validate_date`.
"""

TASK_FILENAME_RE: re.Pattern[str] = re.compile(
    r"^TASK-(\d{8})-(\d{3})-(" + _ROLE + r")-to-(" + _ROLE + r")(?:\.(" + _ROLE + r"))?\.md$"
)

REPORT_FILENAME_RE: re.Pattern[str] = re.compile(
    r"^REPORT-(\d{8})-(\d{3})-(" + _ROLE + r")-to-(" + _ROLE + r")\.md$"
)

ISSUE_FILENAME_RE: re.Pattern[str] = re.compile(
    r"^ISSUE-(\d{8})-(\d{3})-(" + _ROLE + r")\.md$"
)


# ── Structural types ─────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class TaskFilename:
    """Parsed components of a task filename.

    Internal to :mod:`fcop.core`. Public callers receive the richer
    :class:`fcop.models.Task` instead. The two are deliberately distinct:
    this one carries only on-disk-derivable fields.
    """

    date: str
    sequence: int
    sender: str
    recipient: str
    slot: str | None = None

    @property
    def task_id(self) -> str:
        """Canonical task identifier, e.g. ``TASK-20260423-017``."""
        return f"{TASK_FILENAME_PREFIX}-{self.date}-{self.sequence:03d}"

    def render(self) -> str:
        """Render back to the on-disk filename."""
        recipient = f"{self.recipient}.{self.slot}" if self.slot else self.recipient
        return f"{self.task_id}-{self.sender}-to-{recipient}.md"


@dataclass(frozen=True, slots=True)
class ReportFilename:
    """Parsed components of a report filename."""

    date: str
    sequence: int
    reporter: str
    recipient: str

    @property
    def report_id(self) -> str:
        """Canonical report identifier, e.g. ``REPORT-20260423-004``."""
        return f"{REPORT_FILENAME_PREFIX}-{self.date}-{self.sequence:03d}"

    def render(self) -> str:
        return f"{self.report_id}-{self.reporter}-to-{self.recipient}.md"


@dataclass(frozen=True, slots=True)
class IssueFilename:
    """Parsed components of an issue filename.

    Issues are broadcasts with no recipient — the shape differs from
    tasks and reports by that single field.
    """

    date: str
    sequence: int
    reporter: str

    @property
    def issue_id(self) -> str:
        """Canonical issue identifier, e.g. ``ISSUE-20260423-002``."""
        return f"{ISSUE_FILENAME_PREFIX}-{self.date}-{self.sequence:03d}"

    def render(self) -> str:
        return f"{self.issue_id}-{self.reporter}.md"


# ── Parsers ──────────────────────────────────────────────────────────


def parse_task_filename(name: str) -> TaskFilename | None:
    """Parse a task filename into its components, or ``None`` if it doesn't match.

    Accepts only the basename (no directory prefix). Sequence is returned
    as :class:`int` (``"017" → 17``), losing the zero-padding; use
    :meth:`TaskFilename.render` to recover the canonical spelling.
    """
    m = TASK_FILENAME_RE.fullmatch(name)
    if not m:
        return None
    date, seq, sender, recipient, slot = m.groups()
    return TaskFilename(
        date=date,
        sequence=int(seq),
        sender=sender,
        recipient=recipient,
        slot=slot,
    )


def parse_report_filename(name: str) -> ReportFilename | None:
    """Parse a report filename into its components, or ``None`` if it doesn't match."""
    m = REPORT_FILENAME_RE.fullmatch(name)
    if not m:
        return None
    date, seq, reporter, recipient = m.groups()
    return ReportFilename(
        date=date,
        sequence=int(seq),
        reporter=reporter,
        recipient=recipient,
    )


def parse_issue_filename(name: str) -> IssueFilename | None:
    """Parse an issue filename into its components, or ``None`` if it doesn't match."""
    m = ISSUE_FILENAME_RE.fullmatch(name)
    if not m:
        return None
    date, seq, reporter = m.groups()
    return IssueFilename(date=date, sequence=int(seq), reporter=reporter)


# ── Builders ─────────────────────────────────────────────────────────


def build_task_filename(
    *,
    date: str,
    sequence: int,
    sender: str,
    recipient: str,
    slot: str | None = None,
) -> str:
    """Build a canonical task filename from components.

    Validates each argument and raises :class:`ValueError` on anything
    the grammar forbids. Use :func:`parse_task_filename` to round-trip.
    """
    _check_components(
        date=date,
        sequence=sequence,
        role_fields={"sender": sender, "recipient": recipient}
        | ({"slot": slot} if slot is not None else {}),
    )
    return TaskFilename(
        date=date,
        sequence=sequence,
        sender=sender,
        recipient=recipient,
        slot=slot,
    ).render()


def build_report_filename(
    *,
    date: str,
    sequence: int,
    reporter: str,
    recipient: str,
) -> str:
    """Build a canonical report filename from components."""
    _check_components(
        date=date,
        sequence=sequence,
        role_fields={"reporter": reporter, "recipient": recipient},
    )
    return ReportFilename(
        date=date,
        sequence=sequence,
        reporter=reporter,
        recipient=recipient,
    ).render()


def build_issue_filename(
    *,
    date: str,
    sequence: int,
    reporter: str,
) -> str:
    """Build a canonical issue filename from components."""
    _check_components(
        date=date,
        sequence=sequence,
        role_fields={"reporter": reporter},
    )
    return IssueFilename(date=date, sequence=sequence, reporter=reporter).render()


# ── Validators ───────────────────────────────────────────────────────


def validate_date(value: str, *, field: str = "date") -> list[ValidationIssue]:
    """Check that ``value`` is a real ``YYYYMMDD`` calendar date.

    Returns an empty list when valid. Rejects both lexically bad values
    (``"2026-04-23"`` with dashes, ``"20260"`` too short) and lexically
    fine but impossible dates (``"20260230"``).
    """
    if not value or not DATE_RE.fullmatch(value):
        return [
            ValidationIssue(
                severity="error",
                field=field,
                message=(
                    f"date {value!r} must be 8 digits in YYYYMMDD form "
                    f"(e.g. '20260423')"
                ),
            )
        ]
    try:
        _date(int(value[0:4]), int(value[4:6]), int(value[6:8]))
    except ValueError:
        return [
            ValidationIssue(
                severity="error",
                field=field,
                message=f"date {value!r} is not a real calendar date",
            )
        ]
    return []


def validate_sequence(value: int, *, field: str = "sequence") -> list[ValidationIssue]:
    """Check that ``value`` fits the 3-digit per-day sequence field.

    Zero is rejected so the first task of a day is ``001``, not ``000``.
    """
    if not isinstance(value, int) or isinstance(value, bool):
        return [
            ValidationIssue(
                severity="error",
                field=field,
                message=f"sequence must be int, got {type(value).__name__}",
            )
        ]
    if value < 1 or value > MAX_SEQUENCE:
        return [
            ValidationIssue(
                severity="error",
                field=field,
                message=(
                    f"sequence {value!r} out of range; "
                    f"must be 1..{MAX_SEQUENCE} (3 digits, zero-padded)"
                ),
            )
        ]
    return []


# ── Helpers ──────────────────────────────────────────────────────────


def today_iso() -> str:
    """Return today's date in the ``YYYYMMDD`` format used in filenames.

    Always UTC-insensitive — FCoP uses the system local date because
    files are authored from wherever the operator is.
    """
    return _date.today().strftime("%Y%m%d")


def next_sequence(
    existing: Iterable[str],
    *,
    date: str,
    kind: FilenameKind,
) -> int:
    """Compute the next unused sequence for ``date`` from an iterable of names.

    ``existing`` may contain names of any of the three kinds; only names
    that parse as ``kind`` and whose ``date`` matches are considered.
    Non-matching entries are silently ignored, so callers can pass a raw
    ``os.listdir()`` without pre-filtering.

    Raises:
        ValueError: ``date`` is not a valid ``YYYYMMDD`` string.
        OverflowError: all ``MAX_SEQUENCE`` slots are taken for that day.
    """
    if validate_date(date):
        raise ValueError(f"invalid date {date!r}; expected YYYYMMDD")

    parser: dict[FilenameKind, object] = {
        "task": parse_task_filename,
        "report": parse_report_filename,
        "issue": parse_issue_filename,
    }
    parse = parser[kind]

    used: set[int] = set()
    for name in existing:
        parsed = parse(name)  # type: ignore[operator]
        if parsed is None:
            continue
        if parsed.date != date:
            continue
        used.add(parsed.sequence)

    for candidate in range(1, MAX_SEQUENCE + 1):
        if candidate not in used:
            return candidate

    raise OverflowError(
        f"all {MAX_SEQUENCE} {kind} sequence slots are exhausted for {date}"
    )


# ── Internal helpers ─────────────────────────────────────────────────


def _check_components(
    *,
    date: str,
    sequence: int,
    role_fields: dict[str, str],
) -> None:
    """Raise :class:`ValueError` if any component is grammar-illegal.

    Internal to the builders — consolidates the shared preconditions so
    each public ``build_*_filename`` stays declarative.
    """
    issues: list[ValidationIssue] = []
    issues.extend(validate_date(date))
    issues.extend(validate_sequence(sequence))

    for field_name, value in role_fields.items():
        if not value:
            issues.append(
                ValidationIssue(
                    severity="error",
                    field=field_name,
                    message=f"{field_name} must not be empty",
                )
            )
            continue
        # Re-use the role code regex from schema.py here rather than
        # importing validate_role_code, so builder errors are about the
        # filename segment — not the semantic notion of a role.
        from fcop.core.schema import ROLE_CODE_RE

        if not ROLE_CODE_RE.fullmatch(value):
            issues.append(
                ValidationIssue(
                    severity="error",
                    field=field_name,
                    message=(
                        f"{field_name} {value!r} is not a legal filename "
                        f"segment (must match role-code grammar)"
                    ),
                )
            )

    errors = [i for i in issues if i.severity == "error"]
    if errors:
        details = "; ".join(f"{i.field}: {i.message}" for i in errors)
        raise ValueError(f"cannot build filename — {details}")
