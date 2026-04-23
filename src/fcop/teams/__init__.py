"""Stateless accessors for bundled team templates.

This module exposes read-only metadata and template content for the
preset teams packaged with fcop (``dev-team``, ``media-team``,
``mvp-team``, ``qa-team``). The underlying template *text* (role bios,
operating rules) still lives in ``fcop/_data/`` and will be migrated in
D5 per ADR-0001; at this stage we expose **metadata only** so
:meth:`fcop.Project.init` can wire up ``fcop.json`` + the directory
tree end-to-end. :func:`get_template` continues to raise
:class:`NotImplementedError` until the data migration lands.

Public contract (stable within 0.6.x):
    * :func:`get_available_teams` — list all bundled presets.
    * :func:`get_team_info` — fetch one preset by slug.
    * :func:`get_template` — fetch the four-layer doc bundle (D5).

See adr/ADR-0001-library-api.md ("无状态模块：`fcop.teams`") for the
rationale behind keeping this module stateless.
"""

from __future__ import annotations

from dataclasses import dataclass

from fcop.errors import TeamNotFoundError

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


# ── Bundled presets ───────────────────────────────────────────────────
#
# These definitions are the canonical source-of-truth for what "preset
# team X" means. The role lists and leader assignments are stable
# across minor releases — adding or removing roles is a semver-minor
# at minimum since it changes what init(team=X) produces.
#
# The role codes and leaders mirror the 0.5.x TEAM_TEMPLATES dict in
# codeflow-plugin's server.py so projects migrating from 0.5.x keep
# working without surprise. Translations are included verbatim from
# the same source.

_BUNDLED_TEAMS: dict[str, TeamInfo] = {
    "dev-team": TeamInfo(
        name="dev-team",
        display_name="软件开发团队",
        leader="PM",
        roles=("PM", "DEV", "QA", "OPS"),
        description_zh="四人软件开发小组：项目经理、开发、测试、运维。",
        description_en=(
            "Four-role software development squad: "
            "PM, Developer, QA, Operations."
        ),
    ),
    "media-team": TeamInfo(
        name="media-team",
        display_name="自媒体团队",
        leader="PUBLISHER",
        roles=("PUBLISHER", "COLLECTOR", "WRITER"),
        description_zh="自媒体三人组：审核发行、素材采集、拟题提纲。",
        description_en=(
            "Three-role content media team: "
            "Publisher, Content Collector, Content Writer."
        ),
    ),
    "mvp-team": TeamInfo(
        name="mvp-team",
        display_name="MVP 验证团队",
        leader="PM",
        roles=("PM", "BUILDER", "SELLER"),
        description_zh="MVP 验证三人组：项目经理、实现者、销售验证。",
        description_en=(
            "Three-role MVP validation team: "
            "Project Manager, Builder, Seller."
        ),
    ),
    "qa-team": TeamInfo(
        name="qa-team",
        display_name="质量保证团队",
        leader="LEAD-QA",
        roles=("LEAD-QA", "TESTER", "AUTO-TESTER", "PERF-TESTER"),
        description_zh="四人 QA 团队：测试负责人、功能、自动化、性能。",
        description_en=(
            "Four-role QA team: "
            "QA Lead, Functional Tester, Automation Tester, "
            "Performance Tester."
        ),
    ),
}


def get_available_teams() -> list[TeamInfo]:
    """Return metadata for every bundled preset team.

    Order is deterministic: sorted by team slug so UIs that render
    these as a picker get a stable presentation.
    """
    return [_BUNDLED_TEAMS[name] for name in sorted(_BUNDLED_TEAMS)]


def get_team_info(team: str) -> TeamInfo:
    """Return metadata for one bundled team.

    Raises:
        TeamNotFoundError: ``team`` is not bundled. The error's
            ``.team`` attribute carries the requested slug so callers
            can echo it back without reparsing.
    """
    try:
        return _BUNDLED_TEAMS[team]
    except KeyError as exc:
        available = ", ".join(sorted(_BUNDLED_TEAMS))
        raise TeamNotFoundError(
            f"team {team!r} is not bundled; available: {available}",
            team=team,
        ) from exc


def get_template(team: str, lang: str = "zh") -> TeamTemplate:  # noqa: ARG001
    """Fetch the full four-layer documentation for a bundled team.

    Raises:
        NotImplementedError: template text migration is scheduled for
            D5 (see ADR-0001). :func:`get_team_info` is available in
            the meantime for metadata-only consumers.
    """
    raise NotImplementedError(
        "team template text is not yet migrated; see ADR-0001 D5 timeline."
    )
