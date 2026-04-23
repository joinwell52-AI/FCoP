"""FCoP protocol constants and pure validators.

Everything in this module is stateless: no filesystem I/O, no network,
no global mutables. Higher-level code in ``fcop.core.*`` composes these
primitives into on-disk operations.

Values defined here are normative to FCoP protocol v1 and track the
rules document ``fcop-rules.mdc`` v1.4.0. If the rules document changes
at the same major version, this module must track it.

See adr/ADR-0001-library-api.md ("schema.py ← 协议规则常量") for the
rationale.
"""

from __future__ import annotations

import re

from fcop.models import Priority, Severity, ValidationIssue

__all__ = [
    # Protocol identity
    "PROTOCOL_NAME",
    "PROTOCOL_VERSION",
    "PROTOCOL_ALIASES",
    # Role codes
    "ROLE_CODE_RE",
    "RESERVED_ROLE_CODES",
    "AUTHORITY_WORDS",
    # Frontmatter
    "REQUIRED_TASK_FRONTMATTER_KEYS",
    "OPTIONAL_TASK_FRONTMATTER_KEYS",
    # Priority / Severity aliases
    "PRIORITY_ALIASES",
    "SEVERITY_ALIASES",
    # Validators
    "is_valid_role_code",
    "validate_role_code",
    "suggest_role_code",
    "normalize_protocol_name",
    "normalize_priority",
    "normalize_severity",
]


# ── Protocol identity ────────────────────────────────────────────────

PROTOCOL_NAME: str = "fcop"
"""Canonical value for the ``protocol:`` frontmatter field.

Lowercase per machine-identifier convention (cf. ``http`` / ``ssh`` /
``grpc``). The brand name ``FCoP`` is reserved for documentation, titles
and external communications; the two spellings divide labor.
"""

PROTOCOL_VERSION: int = 1
"""Canonical value for the ``version:`` frontmatter field.

Bumped only on **breaking** changes to the on-disk format.
"""

PROTOCOL_ALIASES: frozenset[str] = frozenset(
    {
        "fcop",
        "agent_bridge",
        "agent-bridge",
        "file-coordination",
        "file_coordination",
    }
)
"""Values accepted in the ``protocol:`` field that normalize to
:data:`PROTOCOL_NAME`.

Historical aliases are kept forever so old files authored before a
rename event don't silently become invalid.
"""


# ── Role codes ────────────────────────────────────────────────────────

ROLE_CODE_RE: re.Pattern[str] = re.compile(r"^[A-Z][A-Z0-9_]*(-[A-Z0-9_]+)*$")
"""Matches canonical role codes.

An uppercase ASCII letter, followed by zero or more uppercase / digit /
underscore characters, optionally followed by hyphen-separated
subsegments (each of which itself starts with an uppercase / digit /
underscore). This allows canonical forms like ``PM``, ``DEV_01``,
``LEAD-QA``, ``AUTO-TESTER`` while rejecting leading digits, lowercase,
leading / trailing / consecutive hyphens, and non-ASCII characters.
"""

RESERVED_ROLE_CODES: frozenset[str] = frozenset({"ADMIN", "SYSTEM"})
"""Role codes reserved by FCoP itself.

``ADMIN`` denotes the human operator and cannot be assigned to an AI.
``SYSTEM`` is reserved for protocol-internal messages.
"""

AUTHORITY_WORDS: frozenset[str] = frozenset(
    {
        "BOSS",
        "CHIEF",
        "MASTER",
        "OWNER",
        "CEO",
        "KING",
        "GOD",
        "COMMANDER",
        "DICTATOR",
        "LORD",
    }
)
"""Regex-legal but stylistically discouraged role codes.

:func:`validate_role_code` emits a ``"warning"``-severity
:class:`ValidationIssue` (not an error) for members of this set. The
rationale lives in fcop-rules.mdc — roles should describe function, not
authority.
"""


# ── Frontmatter ───────────────────────────────────────────────────────

REQUIRED_TASK_FRONTMATTER_KEYS: frozenset[str] = frozenset(
    {"protocol", "version", "sender", "recipient"}
)
"""Keys that every TASK-*.md file must carry in its YAML frontmatter."""

OPTIONAL_TASK_FRONTMATTER_KEYS: frozenset[str] = frozenset(
    {"priority", "thread_key", "subject", "references", "type"}
)
"""Keys that TASK-*.md files may carry.

Any additional keys beyond these two sets are preserved in
:attr:`TaskFrontmatter.extra` for forward compatibility, but validators
may emit ``"info"``-severity issues describing them.
"""


# ── Priority / Severity aliases ──────────────────────────────────────

PRIORITY_ALIASES: dict[str, Priority] = {
    # Canonical, case-insensitive
    "p0": Priority.P0,
    "p1": Priority.P1,
    "p2": Priority.P2,
    "p3": Priority.P3,
    # Legacy word-style aliases encountered in pre-0.6 files
    "urgent": Priority.P0,
    "critical": Priority.P0,
    "high": Priority.P1,
    "normal": Priority.P2,
    "medium": Priority.P2,
    "low": Priority.P3,
}
"""Case-insensitive mapping of accepted priority strings to :class:`Priority`.

Exposed so UI code can enumerate accepted inputs and migration tools
can normalize legacy files.
"""

SEVERITY_ALIASES: dict[str, Severity] = {
    "low": Severity.LOW,
    "medium": Severity.MEDIUM,
    "med": Severity.MEDIUM,
    "high": Severity.HIGH,
    "critical": Severity.CRITICAL,
    "crit": Severity.CRITICAL,
}
"""Case-insensitive mapping of accepted severity strings to :class:`Severity`."""


# ── Validators (pure) ────────────────────────────────────────────────


def is_valid_role_code(code: str) -> bool:
    """Return ``True`` iff ``code`` is a well-formed, non-reserved role code.

    This is the cheap, boolean check. For structured error output use
    :func:`validate_role_code`.
    """
    if not code or code in RESERVED_ROLE_CODES:
        return False
    return bool(ROLE_CODE_RE.fullmatch(code))


def validate_role_code(
    code: str,
    *,
    field: str = "role",
    allow_reserved: bool = False,
) -> list[ValidationIssue]:
    """Return a list of issues describing what's wrong with ``code``.

    Empty list ⇒ valid. An ``"error"``-severity issue means the caller
    must not accept the code. A ``"warning"`` means the code is legal
    but stylistically discouraged (see :data:`AUTHORITY_WORDS`).

    Args:
        code: The role code to validate.
        field: Field name embedded in each returned issue so downstream
               aggregators can tell sender from recipient failures.
        allow_reserved: If True, ``ADMIN`` / ``SYSTEM`` pass as legal.
               Used when validating fields that legitimately carry
               those codes (e.g. the ``sender`` of a task written by
               the human operator). Default False — strict — which is
               what team-config registration wants.
    """
    issues: list[ValidationIssue] = []

    if not code:
        issues.append(
            ValidationIssue(
                severity="error",
                field=field,
                message="role code must not be empty",
            )
        )
        return issues

    if not ROLE_CODE_RE.fullmatch(code):
        issues.append(
            ValidationIssue(
                severity="error",
                field=field,
                message=(
                    f"role code {code!r} must start with an uppercase ASCII "
                    f"letter and contain only A-Z, 0-9, _, or internal hyphens "
                    f"(no leading, trailing, or consecutive hyphens)"
                ),
            )
        )
        return issues

    if code in RESERVED_ROLE_CODES and not allow_reserved:
        issues.append(
            ValidationIssue(
                severity="error",
                field=field,
                message=(
                    f"role code {code!r} is reserved by FCoP "
                    f"({'human operator' if code == 'ADMIN' else 'internal use'})"
                ),
            )
        )
        return issues

    if code in AUTHORITY_WORDS:
        issues.append(
            ValidationIssue(
                severity="warning",
                field=field,
                message=(
                    f"role code {code!r} is an authority word; prefer "
                    f"function-specific names like MANAGER / CODER / QA"
                ),
            )
        )

    return issues


def suggest_role_code(bad: str) -> str:
    """Best-effort repair of a malformed role code.

    Pure transformation: uppercases, keeps ASCII alnum / underscore /
    hyphen, folds dots and whitespace to underscores, collapses
    consecutive separators, strips leading / trailing separators, and
    prefixes a digit-starting result with ``R`` (for "role").

    Returns either an empty string (the input is hopeless) or a string
    that passes :data:`ROLE_CODE_RE`. Callers must **never** apply this
    silently — always surface the suggestion for human confirmation.
    """
    if not bad:
        return ""

    cleaned: list[str] = []
    for ch in bad:
        if ch.isascii() and (ch.isalnum() or ch in "_-"):
            cleaned.append(ch)
        elif ch in ". \t":
            cleaned.append("_")
        # else: drop non-ASCII and other punctuation

    out = "".join(cleaned).upper()
    while "__" in out:
        out = out.replace("__", "_")
    while "--" in out:
        out = out.replace("--", "-")
    out = out.strip("_-")

    if not out:
        return ""
    if out[0].isdigit():
        out = "R" + out

    return out if ROLE_CODE_RE.fullmatch(out) else ""


def normalize_protocol_name(raw: str) -> str | None:
    """Map a ``protocol:`` field value to its canonical form.

    Returns :data:`PROTOCOL_NAME` if ``raw`` (case-insensitive, trimmed)
    is in :data:`PROTOCOL_ALIASES`; returns ``None`` for unknown values.
    """
    if not raw:
        return None
    if raw.strip().lower() in PROTOCOL_ALIASES:
        return PROTOCOL_NAME
    return None


def normalize_priority(raw: str | Priority) -> Priority:
    """Coerce a user-supplied priority to :class:`Priority`.

    Accepts an existing :class:`Priority` (passed through), the canonical
    spelling (``"P0"`` / ``"P1"`` / ``"P2"`` / ``"P3"``, case-insensitive),
    or a legacy word alias (``"urgent"`` / ``"high"`` / ``"normal"`` /
    ``"low"`` / etc. — see :data:`PRIORITY_ALIASES`).

    Raises:
        ValueError: ``raw`` is not a recognized priority.
    """
    if isinstance(raw, Priority):
        return raw
    key = str(raw).strip().lower()
    if key in PRIORITY_ALIASES:
        return PRIORITY_ALIASES[key]
    raise ValueError(
        f"unknown priority {raw!r}; expected one of "
        f"{sorted(p.value for p in Priority)} "
        f"(or legacy aliases {sorted(PRIORITY_ALIASES)})"
    )


def normalize_severity(raw: str | Severity) -> Severity:
    """Coerce a user-supplied severity to :class:`Severity`.

    Same contract as :func:`normalize_priority` but targeting
    :class:`Severity`.

    Raises:
        ValueError: ``raw`` is not a recognized severity.
    """
    if isinstance(raw, Severity):
        return raw
    key = str(raw).strip().lower()
    if key in SEVERITY_ALIASES:
        return SEVERITY_ALIASES[key]
    raise ValueError(
        f"unknown severity {raw!r}; expected one of "
        f"{sorted(s.value for s in Severity)} "
        f"(or aliases {sorted(SEVERITY_ALIASES)})"
    )
