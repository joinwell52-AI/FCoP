"""FCoP YAML frontmatter parser and serializer.

FCoP task / report / issue files are UTF-8 Markdown with a YAML
frontmatter block at the top::

    ---
    protocol: fcop
    version: 1
    sender: ADMIN
    recipient: PM
    priority: P1
    ---

    # body in markdown...

This module is the boundary between raw text and the structured
:class:`TaskFrontmatter` dataclass. Parsing is lenient about historical
spellings — :data:`fcop.core.schema.PROTOCOL_ALIASES` and
:data:`fcop.core.schema.PRIORITY_ALIASES` are honored — but strict
about required fields (missing ``sender`` / ``recipient`` is a
protocol violation).

Pure module: no filesystem I/O. Callers read/write the file; this
module handles the text ↔ dataclass conversion.

See adr/ADR-0001-library-api.md ("frontmatter.py ← YAML 头解析/写回")
for the rationale.
"""

from __future__ import annotations

import yaml

from fcop.core.schema import (
    PROTOCOL_NAME,
    PROTOCOL_VERSION,
    normalize_priority,
    normalize_protocol_name,
    validate_role_code,
)
from fcop.errors import ProtocolViolation, ValidationError
from fcop.models import Priority, TaskFrontmatter, ValidationIssue

__all__ = [
    "FRONTMATTER_DELIMITER",
    "DEFAULT_PRIORITY",
    "split_frontmatter",
    "parse_frontmatter_raw",
    "parse_task_frontmatter",
    "serialize_task_frontmatter",
    "assemble_task_file",
    "parse_review_frontmatter",
    "serialize_review_frontmatter",
    "assemble_review_file",
]


FRONTMATTER_DELIMITER: str = "---"
"""The three-dash fence that brackets the YAML block."""

DEFAULT_PRIORITY: Priority = Priority.P2
"""Priority assumed when a frontmatter omits the ``priority:`` field."""


# The public TaskFrontmatter fields that are handled by name; anything
# else in the YAML mapping goes into :attr:`TaskFrontmatter.extra`.
_KNOWN_KEYS: frozenset[str] = frozenset(
    {
        "protocol",
        "version",
        "sender",
        "recipient",
        "priority",
        "thread_key",
        "parent",
        "subject",
        "references",
    }
)


# ── Splitter ─────────────────────────────────────────────────────────


def split_frontmatter(text: str) -> tuple[str, str]:
    """Split a markdown document into ``(yaml_block, body)``.

    The returned ``yaml_block`` is the YAML content without the fence
    lines. If the document does not begin with a ``---`` fence on its
    own line, returns ``("", text)`` so the caller can decide whether
    missing frontmatter is an error.

    CRLF line endings (common from Windows editors) are normalized to
    LF before splitting so the regex-free scanner below stays simple.
    """
    normalized = text.replace("\r\n", "\n")
    if not normalized.startswith(FRONTMATTER_DELIMITER):
        return "", text

    first_nl = normalized.find("\n")
    if first_nl < 0:
        return "", text
    if normalized[:first_nl].strip() != FRONTMATTER_DELIMITER:
        return "", text

    rest = normalized[first_nl + 1 :]
    closing = _find_closing_delimiter(rest)
    if closing < 0:
        return "", text

    yaml_block = rest[:closing]
    after = rest[closing:]
    body_nl = after.find("\n")
    body = after[body_nl + 1 :] if body_nl >= 0 else ""
    return yaml_block, body


def _find_closing_delimiter(text: str) -> int:
    """Return the byte offset of the next standalone ``---`` line in ``text``.

    A standalone line is one where the trimmed content equals ``---``
    exactly. Returns ``-1`` if no such line exists.
    """
    idx = 0
    while idx < len(text):
        nl = text.find("\n", idx)
        line_end = nl if nl >= 0 else len(text)
        if text[idx:line_end].strip() == FRONTMATTER_DELIMITER:
            return idx
        if nl < 0:
            return -1
        idx = nl + 1
    return -1


# ── Raw parse ────────────────────────────────────────────────────────


def parse_frontmatter_raw(text: str) -> dict[str, object]:
    """Return the raw YAML mapping from a markdown document.

    Returns an empty dict when the document has no frontmatter or the
    YAML block is empty / contains only comments. Lifts YAML parse
    errors and non-mapping top levels into :class:`ValidationError`.
    """
    yaml_block, _ = split_frontmatter(text)
    if not yaml_block.strip():
        return {}

    try:
        parsed = yaml.safe_load(yaml_block)
    except yaml.YAMLError as exc:
        raise ValidationError(
            "malformed YAML frontmatter",
            issues=[
                ValidationIssue(
                    severity="error",
                    field="<frontmatter>",
                    message=str(exc),
                )
            ],
        ) from exc

    if parsed is None:
        return {}
    if not isinstance(parsed, dict):
        raise ValidationError(
            "frontmatter must be a YAML mapping",
            issues=[
                ValidationIssue(
                    severity="error",
                    field="<frontmatter>",
                    message=(
                        f"expected a mapping at the top level, "
                        f"got {type(parsed).__name__}"
                    ),
                )
            ],
        )
    # Normalize keys to str so downstream lookups are uniform.
    return {str(k): v for k, v in parsed.items()}


# ── Task frontmatter ─────────────────────────────────────────────────


def parse_task_frontmatter(text: str) -> tuple[TaskFrontmatter, str]:
    """Parse and validate a TASK-*.md document into ``(TaskFrontmatter, body)``.

    Accepts historical aliases for ``protocol`` and ``priority``; the
    returned dataclass always holds canonical values. Unknown keys are
    preserved in :attr:`TaskFrontmatter.extra` for forward
    compatibility.

    Raises:
        ProtocolViolation: a required field is missing or ``protocol`` /
            ``version`` don't identify FCoP v1.
        ValidationError: malformed YAML, bad role code, unknown priority,
            malformed references list, etc.
    """
    raw = parse_frontmatter_raw(text)
    _, body = split_frontmatter(text)

    # protocol — required, canonical after alias lookup.
    if "protocol" not in raw:
        raise ProtocolViolation(
            "missing required frontmatter field: protocol",
            rule="frontmatter.required",
        )
    proto_raw = str(raw["protocol"]).strip()
    if not proto_raw:
        raise ProtocolViolation(
            "missing required frontmatter field: protocol",
            rule="frontmatter.required",
        )
    canonical = normalize_protocol_name(proto_raw)
    if canonical is None:
        raise ProtocolViolation(
            f"unknown protocol value {proto_raw!r}; "
            f"expected 'fcop' or a known alias",
            rule="frontmatter.protocol",
        )

    # version — required, integer, must be the one this lib speaks.
    if "version" not in raw:
        raise ProtocolViolation(
            "missing required frontmatter field: version",
            rule="frontmatter.required",
        )
    version = _coerce_version(raw["version"])
    if version != PROTOCOL_VERSION:
        raise ProtocolViolation(
            f"unsupported FCoP version {version}; "
            f"this library speaks v{PROTOCOL_VERSION}",
            rule="frontmatter.version",
        )

    # sender / recipient — required and must pass role-code grammar.
    sender = _required_role(raw, key="sender")
    recipient = _required_role(raw, key="recipient")

    # allow_reserved=True so ADMIN (human operator) and SYSTEM (internal
    # protocol messages) can legitimately appear as sender / recipient
    # in task files. The "reserved" rule is about who can be *assigned*
    # a role in fcop.json, not about who can appear in a message header.
    role_issues: list[ValidationIssue] = []
    role_issues.extend(validate_role_code(sender, field="sender", allow_reserved=True))
    role_issues.extend(
        validate_role_code(recipient, field="recipient", allow_reserved=True)
    )
    role_errors = [i for i in role_issues if i.severity == "error"]
    if role_errors:
        raise ValidationError(
            "invalid role code in frontmatter",
            issues=role_errors,
        )

    # priority — optional, defaults to P2.
    priority = _parse_priority(raw.get("priority"))

    # optional scalars
    thread_key = _optional_string(raw, "thread_key")
    parent = _optional_string(raw, "parent")
    subject = _optional_string(raw, "subject")
    references = _parse_references(raw.get("references"))

    extra = {k: v for k, v in raw.items() if k not in _KNOWN_KEYS}

    fm = TaskFrontmatter(
        protocol=PROTOCOL_NAME,
        version=PROTOCOL_VERSION,
        sender=sender,
        recipient=recipient,
        priority=priority,
        thread_key=thread_key,
        parent=parent,
        subject=subject,
        references=references,
        extra=extra,
    )
    return fm, body


def serialize_task_frontmatter(fm: TaskFrontmatter) -> str:
    """Render a :class:`TaskFrontmatter` back to a YAML block with fences.

    Field order is deterministic: ``protocol`` first, then ``version``,
    ``sender``, ``recipient``, ``priority``, optional ``thread_key`` /
    ``subject`` / ``references`` (only when populated), then ``extra``
    keys alphabetically. This stable ordering means round-tripping a
    file through parse→serialize yields a minimal diff.

    Output includes the leading and trailing ``---\\n`` fences and ends
    with a newline so callers can concatenate a body directly.
    """
    data: dict[str, object] = {
        "protocol": fm.protocol,
        "version": fm.version,
        "sender": fm.sender,
        "recipient": fm.recipient,
        "priority": fm.priority.value,
    }
    if fm.thread_key:
        data["thread_key"] = fm.thread_key
    if fm.parent:
        data["parent"] = fm.parent
    if fm.subject:
        data["subject"] = fm.subject
    if fm.references:
        data["references"] = list(fm.references)
    for key in sorted(fm.extra):
        data[key] = fm.extra[key]

    yaml_text = yaml.safe_dump(
        data,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
    )
    return f"{FRONTMATTER_DELIMITER}\n{yaml_text}{FRONTMATTER_DELIMITER}\n"


# ── Review frontmatter ───────────────────────────────────────────────


# REVIEW frontmatter 字段集（与 review.schema.json 对齐）。本模块按字典
# 维护（不引入 ReviewFrontmatter dataclass）——REVIEW 的字段相对扁平，
# Project.write_review 直接构造 dict 比包一层 dataclass 更直接。
_REVIEW_REQUIRED_KEYS: frozenset[str] = frozenset(
    {
        "protocol",
        "version",
        "type",
        "sender",
        "review_id",
        "subject_type",
        "subject_ref",
        "reviewer_role",
        "decision",
        "decided_at",
    }
)

_REVIEW_OPTIONAL_KEYS: frozenset[str] = frozenset(
    {
        "reviewer_agent",
        "rationale",
        "required_changes",
        "session_id",
    }
)

_REVIEW_FIELD_ORDER: tuple[str, ...] = (
    "protocol",
    "version",
    "type",
    "sender",
    "review_id",
    "subject_type",
    "subject_ref",
    "reviewer_role",
    "reviewer_agent",
    "decision",
    "rationale",
    "required_changes",
    "decided_at",
    "session_id",
)


def parse_review_frontmatter(text: str) -> tuple[dict[str, object], str]:
    """Parse a REVIEW-*.md document into ``(frontmatter_dict, body)``.

    与 :func:`parse_task_frontmatter` 不同，本函数返回**原生 dict**而
    非 dataclass —— REVIEW 的字段集小且扁平，调用方（``Project.read_review``）
    直接组装 :class:`fcop.models.Review`。

    本函数只做最小的协议层校验（protocol/version 存在且匹配），结构
    校验交给 :mod:`fcop.core.jsonschema_validator` 统一兜底。

    Raises:
        ProtocolViolation: ``protocol`` 字段缺失或非 fcop 别名；
            ``version`` 字段缺失或不等于本库 PROTOCOL_VERSION。
        ValidationError: YAML 本身畸形。
    """
    raw = parse_frontmatter_raw(text)
    _, body = split_frontmatter(text)

    if "protocol" not in raw:
        raise ProtocolViolation(
            "missing required frontmatter field: protocol",
            rule="frontmatter.required",
        )
    proto_raw = str(raw["protocol"]).strip()
    canonical = normalize_protocol_name(proto_raw)
    if canonical is None:
        raise ProtocolViolation(
            f"unknown protocol value {proto_raw!r}; expected 'fcop'",
            rule="frontmatter.protocol",
        )

    if "version" not in raw:
        raise ProtocolViolation(
            "missing required frontmatter field: version",
            rule="frontmatter.required",
        )
    version = _coerce_version(raw["version"])
    if version != PROTOCOL_VERSION:
        raise ProtocolViolation(
            f"unsupported FCoP version {version}; "
            f"this library speaks v{PROTOCOL_VERSION}",
            rule="frontmatter.version",
        )

    out = dict(raw)
    out["protocol"] = canonical
    out["version"] = version
    out.setdefault("type", "REVIEW")
    return out, body


def serialize_review_frontmatter(fm: dict[str, object]) -> str:
    """Render a REVIEW frontmatter dict to a YAML block with fences.

    Field order is deterministic per :data:`_REVIEW_FIELD_ORDER`，未知
    字段（向前兼容）追加在后并按字母排序。
    """
    ordered: dict[str, object] = {}
    for key in _REVIEW_FIELD_ORDER:
        if key in fm and fm[key] is not None:
            ordered[key] = fm[key]
    for key in sorted(fm):
        if key not in ordered and fm[key] is not None:
            ordered[key] = fm[key]

    yaml_text = yaml.safe_dump(
        ordered,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
    )
    return f"{FRONTMATTER_DELIMITER}\n{yaml_text}{FRONTMATTER_DELIMITER}\n"


def assemble_review_file(fm: dict[str, object], body: str) -> str:
    """Combine a REVIEW frontmatter dict and body into the full file text."""
    fm_text = serialize_review_frontmatter(fm)
    if not body:
        return fm_text
    body_stripped = body.lstrip("\n")
    return f"{fm_text}\n{body_stripped}"


def assemble_task_file(fm: TaskFrontmatter, body: str) -> str:
    """Combine a frontmatter dataclass and a markdown body into the full file text.

    Ensures exactly one blank line separates the closing ``---`` and
    the body so the output is idempotent when parsed again.
    """
    fm_text = serialize_task_frontmatter(fm)
    if not body:
        return fm_text
    # Strip leading blank lines from body; we always insert one.
    body_stripped = body.lstrip("\n")
    return f"{fm_text}\n{body_stripped}"


# ── Internal helpers ─────────────────────────────────────────────────


def _required_role(raw: dict[str, object], *, key: str) -> str:
    """Pull a required role-code field out of ``raw`` or raise."""
    if key not in raw:
        raise ProtocolViolation(
            f"missing required frontmatter field: {key}",
            rule="frontmatter.required",
        )
    value = str(raw[key]).strip()
    if not value:
        raise ProtocolViolation(
            f"missing required frontmatter field: {key}",
            rule="frontmatter.required",
        )
    return value


def _coerce_version(raw: object) -> int:
    """Map the historically-lenient shapes of ``version:`` to a plain int.

    Accepts ``1``, ``"1"``, ``"1.0"``, and ``1.0``. Anything else raises
    :class:`ValidationError` so callers see a structured issue rather
    than a bare :class:`TypeError`.
    """
    if isinstance(raw, bool):
        raise ValidationError(
            "version field must be an integer",
            issues=[
                ValidationIssue(
                    severity="error",
                    field="version",
                    message="got bool, expected integer",
                )
            ],
        )
    if isinstance(raw, int):
        return raw
    if isinstance(raw, float) and raw.is_integer():
        return int(raw)
    if isinstance(raw, str):
        s = raw.strip().strip('"').strip("'")
        if s in ("1", "1.0"):
            return 1
        if s.isdigit():
            return int(s)

    raise ValidationError(
        f"version field {raw!r} is not an integer",
        issues=[
            ValidationIssue(
                severity="error",
                field="version",
                message=f"expected integer, got {raw!r} ({type(raw).__name__})",
            )
        ],
    )


def _parse_priority(raw: object) -> Priority:
    """Normalize an optional ``priority:`` value, falling back to the default."""
    if raw is None or raw == "":
        return DEFAULT_PRIORITY
    try:
        return normalize_priority(str(raw))
    except ValueError as exc:
        raise ValidationError(
            str(exc),
            issues=[
                ValidationIssue(
                    severity="error",
                    field="priority",
                    message=str(exc),
                )
            ],
        ) from exc


def _optional_string(raw: dict[str, object], key: str) -> str | None:
    """Return a stripped string from ``raw[key]`` or ``None`` if absent/blank."""
    if key not in raw or raw[key] is None:
        return None
    value = str(raw[key]).strip()
    return value or None


def _parse_references(raw: object) -> tuple[str, ...]:
    """Normalize ``references:`` to a tuple of non-empty strings.

    Accepts:
        - missing / ``None`` → ``()``
        - a single string → ``(string,)`` (common shorthand in old files)
        - a list or tuple → each element str()-ified and stripped
    """
    if raw is None:
        return ()
    if isinstance(raw, str):
        stripped = raw.strip()
        return (stripped,) if stripped else ()
    if isinstance(raw, (list, tuple)):
        out: list[str] = []
        for item in raw:
            s = str(item).strip()
            if s:
                out.append(s)
        return tuple(out)
    raise ValidationError(
        "references field must be a list or string",
        issues=[
            ValidationIssue(
                severity="error",
                field="references",
                message=f"expected list or string, got {type(raw).__name__}",
            )
        ],
    )
