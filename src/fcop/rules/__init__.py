"""Stateless accessors for the packaged FCoP protocol rule documents.

These functions return plain strings so callers can feed them directly
into LLM system prompts or rule engines without any fcop-specific
framework. The underlying data lives in ``fcop/rules/_data/`` inside
the wheel and is loaded on demand via :mod:`importlib.resources`.

See adr/ADR-0001-library-api.md ("无状态模块：`fcop.rules`") for the
contract.

The loader uses :mod:`importlib.resources` so the library works both
from an installed wheel and from an editable checkout without caring
about cwd. Content is cached after the first read to keep LLM-prompt
assembly cheap.
"""

from __future__ import annotations

import re
from functools import cache
from importlib import resources
from typing import Literal

from fcop.errors import FcopError

__all__ = [
    "get_rules",
    "get_protocol_commentary",
    "get_letter",
    "get_rules_version",
    "get_protocol_version",
]


# ── Data file names (must match files under fcop/rules/_data/) ────────

_RULES_FILENAME = "fcop-rules.mdc"
_PROTOCOL_FILENAME = "fcop-protocol.mdc"
_LETTER_FILENAMES: dict[str, str] = {
    "zh": "letter-to-admin.zh.md",
    "en": "letter-to-admin.en.md",
}

# Frontmatter key that pins the semver of the rules document. Kept in
# sync with the _data/fcop-rules.mdc header — bumped when the .mdc
# changes semantically, independent of :data:`fcop.__version__`.
_RULES_VERSION_KEY = "fcop_rules_version"

# Frontmatter key that pins the semver of the protocol commentary.
# The two are independent: rules can bump without touching the
# commentary and vice versa, so each carries its own version field.
_PROTOCOL_VERSION_KEY = "fcop_protocol_version"


# ── Public API ───────────────────────────────────────────────────────


def get_rules() -> str:
    """Return the content of ``fcop-rules.mdc`` (the protocol rules).

    Suitable for injecting into LLM system prompts so any compliant
    agent — MCP-hosted or otherwise — understands the protocol. The
    frontmatter is retained so downstream tooling that cares about
    ``fcop_rules_version`` can parse it in place.
    """
    return _load_text(_RULES_FILENAME)


def get_protocol_commentary() -> str:
    """Return the content of ``fcop-protocol.mdc``.

    This is the "how to apply the rules" commentary — less normative
    than :func:`get_rules` but useful context for agents bootstrapping
    into the protocol.
    """
    return _load_text(_PROTOCOL_FILENAME)


def get_letter(lang: Literal["zh", "en"] = "zh") -> str:
    """Return the Letter-to-ADMIN user manual in the requested language.

    Raises:
        ValueError: ``lang`` is not a supported language code.
    """
    if lang not in _LETTER_FILENAMES:
        raise ValueError(
            f"unsupported letter language {lang!r}; "
            f"expected one of {sorted(_LETTER_FILENAMES)}"
        )
    return _load_text(_LETTER_FILENAMES[lang])


def get_rules_version() -> str:
    """Return the semver of the shipped rules document, e.g. ``"1.4.0"``.

    This is independent of :data:`fcop.__version__`: the library and the
    rules document version each independently so agents can detect
    "same library, new rules" and refresh their system prompt without a
    reinstall.

    Raises:
        FcopError: the bundled rules file lacks a parseable
            ``fcop_rules_version:`` field. This indicates a packaging
            bug (the .mdc was trimmed or corrupted during build) and
            should surface loudly.
    """
    text = get_rules()
    version = _extract_frontmatter_version(text, _RULES_VERSION_KEY)
    if version is None:
        raise FcopError(
            f"{_RULES_FILENAME!r} is missing a parseable "
            f"{_RULES_VERSION_KEY!r} frontmatter field"
        )
    return version


def get_protocol_version() -> str:
    """Return the semver of the shipped protocol commentary, e.g. ``"1.3.0"``.

    Symmetric to :func:`get_rules_version`: the rules document
    (`fcop-rules.mdc`) and the protocol commentary
    (`fcop-protocol.mdc`) version independently so a wording-only
    edit to the commentary doesn't force a rules bump and vice versa.

    Used by :class:`fcop.Project.deploy_protocol_rules` (and the MCP
    layer's ``fcop_report`` / ``redeploy_rules``) to detect when a
    project's local copy of the commentary has drifted from the
    bundled wheel and an explicit redeploy is needed.

    Raises:
        FcopError: the bundled commentary file lacks a parseable
            ``fcop_protocol_version:`` field. Indicates a packaging
            bug — surfaces loudly rather than silently substituting
            a placeholder.
    """
    text = get_protocol_commentary()
    version = _extract_frontmatter_version(text, _PROTOCOL_VERSION_KEY)
    if version is None:
        raise FcopError(
            f"{_PROTOCOL_FILENAME!r} is missing a parseable "
            f"{_PROTOCOL_VERSION_KEY!r} frontmatter field"
        )
    return version


# ── Internal helpers ─────────────────────────────────────────────────


@cache
def _load_text(name: str) -> str:
    """Read a packaged data file as UTF-8 text.

    Cached on first call so repeated LLM-prompt assembly doesn't keep
    hitting the wheel's zipfile reader. The cache key is the filename,
    which is stable for the lifetime of an installed version.
    """
    # files() returns a Traversable anchored at the package root; we
    # join the data subpackage then the filename. This works whether
    # the package is installed from a wheel, an sdist, or in editable
    # mode from the source tree.
    data_dir = resources.files("fcop.rules").joinpath("_data")
    return data_dir.joinpath(name).read_text(encoding="utf-8")


def _extract_frontmatter_version(text: str, key: str) -> str | None:
    """Pull a ``key: <semver>`` line out of a .mdc frontmatter block.

    Uses a line-scoped regex rather than a full YAML parse: the
    frontmatter is tiny, every key is unique on its own line, and
    avoiding a YAML round-trip here keeps the public version getters
    trivially cheap. Quoting is tolerated because YAML permits it and
    hand-edited files sometimes arrive that way.

    Returns ``None`` when the field is absent so the caller can
    decide how to surface the packaging error with a key-specific
    message.
    """
    pattern = re.compile(
        r"^" + re.escape(key) + r"\s*:\s*['\"]?([^'\"\s]+)['\"]?\s*$",
        re.MULTILINE,
    )
    match = pattern.search(text)
    return match.group(1) if match else None
