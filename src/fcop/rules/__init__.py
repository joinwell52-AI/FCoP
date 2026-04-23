"""Stateless accessors for the packaged FCoP protocol rule documents.

These functions return plain strings so callers can feed them directly
into LLM system prompts or rule engines without any fcop-specific
framework. The underlying data lives in ``fcop/rules/_data/`` inside
the wheel and is loaded on demand via :mod:`importlib.resources`.

See adr/ADR-0001-library-api.md ("无状态模块：`fcop.rules`") for the
contract.

Implementation status: stubbed. Data files have not been migrated yet
— that happens in D5 per the ADR-0001 timeline.
"""

from __future__ import annotations

from typing import Literal

__all__ = [
    "get_rules",
    "get_protocol_commentary",
    "get_letter",
    "get_rules_version",
]


def get_rules() -> str:
    """Return the content of ``fcop-rules.mdc`` (the 9 core rules).

    Suitable for injecting into LLM system prompts so any compliant
    agent — MCP-hosted or otherwise — understands the protocol.
    """
    raise NotImplementedError


def get_protocol_commentary() -> str:
    """Return the content of ``fcop-protocol.mdc``.

    This is the "how to apply the rules" commentary — less normative
    than :func:`get_rules` but useful context for agents bootstrapping
    into the protocol.
    """
    raise NotImplementedError


def get_letter(lang: Literal["zh", "en"] = "zh") -> str:
    """Return the Letter-to-ADMIN user manual in the requested language."""
    raise NotImplementedError


def get_rules_version() -> str:
    """Return the semver of the shipped rules document, e.g. ``"1.4.0"``.

    This is independent of :data:`fcop.__version__`: the library and the
    rules document version each independently.
    """
    raise NotImplementedError
