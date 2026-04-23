"""Stateless accessors for bundled team templates.

This module exposes read-only metadata and template content for the
preset teams packaged with fcop (``dev-team``, ``media-team``,
``mvp-team``, ``qa-team``, etc.). The underlying data lives in
``fcop/teams/_data/`` inside the wheel and is loaded on demand via
:mod:`importlib.resources`.

See adr/ADR-0001-library-api.md ("无状态模块：`fcop.teams`") for the
contract.

Implementation status: stubbed. Data files have not been migrated yet
— that happens in D5 per the ADR-0001 timeline.
"""

from __future__ import annotations

from dataclasses import dataclass

__all__ = [
    "TeamInfo",
    "TeamTemplate",
    "get_available_teams",
    "get_team_info",
    "get_template",
]


@dataclass(frozen=True, slots=True)
class TeamInfo:
    """Metadata for one bundled team."""

    name: str
    display_name: str
    leader: str
    roles: tuple[str, ...]
    description_zh: str
    description_en: str


@dataclass(frozen=True, slots=True)
class TeamTemplate:
    """The four-layer documentation bundle for one team, one language."""

    name: str
    lang: str
    readme: str
    team_roles: str
    operating_rules: str
    roles: dict[str, str]


def get_available_teams() -> list[TeamInfo]:
    """Return metadata for every bundled preset team."""
    raise NotImplementedError


def get_team_info(team: str) -> TeamInfo:
    """Return metadata for one bundled team.

    Raises:
        TeamNotFoundError: ``team`` is not bundled.
    """
    raise NotImplementedError


def get_template(team: str, lang: str = "zh") -> TeamTemplate:
    """Fetch the full four-layer documentation for a bundled team."""
    raise NotImplementedError
