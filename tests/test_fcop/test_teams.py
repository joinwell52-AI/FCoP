"""Tests for :mod:`fcop.teams` — bundled preset team registry.

These tests pin the 0.6.0 preset team catalogue: changing a role list
or leader in the bundled ``index.json`` will fail here, forcing the
author to either update the test *and* CHANGELOG (legitimate change)
or back out (accidental change). The presets are public API in the
sense that ``Project.init(team=X)`` promises to produce the roles
listed here.
"""

from __future__ import annotations

from importlib import resources

import pytest

from fcop.errors import TeamNotFoundError
from fcop.teams import (
    TeamInfo,
    TeamTemplate,
    get_available_teams,
    get_team_info,
    get_template,
)


class TestRegistry:
    def test_get_available_teams_is_sorted(self) -> None:
        teams = get_available_teams()
        names = [t.name for t in teams]
        assert names == sorted(names)
        # Bundled presets — guardrail for accidental removal. 0.6.4
        # added `solo` so a single-AI project also gets a three-layer
        # template bundle.
        assert set(names) == {
            "solo",
            "dev-team",
            "media-team",
            "mvp-team",
            "qa-team",
        }

    def test_every_entry_is_a_frozen_team_info(self) -> None:
        for info in get_available_teams():
            assert isinstance(info, TeamInfo)
            # Frozen dataclass — mutation is a contract violation.
            with pytest.raises(Exception):  # noqa: B017, PT011
                info.leader = "HACKED"  # type: ignore[misc]

    @pytest.mark.parametrize(
        ("team", "leader", "role_set"),
        [
            # Aligned with _data/teams/index.json v0.6 (ported from
            # plugin 0.5.x data). If you update a preset's roles /
            # leader, bump CHANGELOG and update this parametrize row.
            ("dev-team", "PM", {"PM", "DEV", "QA", "OPS"}),
            (
                "media-team",
                "PUBLISHER",
                {"PUBLISHER", "COLLECTOR", "WRITER", "EDITOR"},
            ),
            (
                "mvp-team",
                "MARKETER",
                {"MARKETER", "RESEARCHER", "DESIGNER", "BUILDER"},
            ),
            (
                "qa-team",
                "LEAD-QA",
                {"LEAD-QA", "TESTER", "AUTO-TESTER", "PERF-TESTER"},
            ),
        ],
    )
    def test_preset_shape(
        self, team: str, leader: str, role_set: set[str]
    ) -> None:
        info = get_team_info(team)
        assert info.name == team
        assert info.leader == leader
        assert set(info.roles) == role_set
        # Leader must be in the roles list; if not, something has gone
        # wrong in the registry definition.
        assert info.leader in info.roles

    def test_unknown_team_raises(self) -> None:
        with pytest.raises(TeamNotFoundError) as excinfo:
            get_team_info("nonexistent")
        # Error carries the query so callers can echo back.
        assert excinfo.value.team == "nonexistent"
        # Message lists the available options to help users self-correct.
        assert "dev-team" in str(excinfo.value)


class TestGetTemplate:
    @pytest.mark.parametrize("team", ["dev-team", "qa-team", "media-team", "mvp-team"])
    def test_zh_bundle_is_complete(self, team: str) -> None:
        tmpl = get_template(team, "zh")
        assert isinstance(tmpl, TeamTemplate)
        assert tmpl.name == team
        assert tmpl.lang == "zh"
        # Layer 1 + 2 are always present.
        assert tmpl.readme
        assert tmpl.team_roles
        assert tmpl.operating_rules
        # Every role from get_team_info must have its own bio.
        info = get_team_info(team)
        assert set(tmpl.roles) == set(info.roles)
        for role, body in tmpl.roles.items():
            assert body, f"role {role} in {team} has empty template"

    def test_en_differs_from_zh(self) -> None:
        zh = get_template("dev-team", "zh")
        en = get_template("dev-team", "en")
        assert en.lang == "en"
        # Same team name, same roster, different text.
        assert en.name == zh.name
        assert set(en.roles) == set(zh.roles)
        assert en.readme != zh.readme

    def test_unknown_team(self) -> None:
        with pytest.raises(TeamNotFoundError):
            get_template("nonexistent")

    def test_unknown_lang(self) -> None:
        with pytest.raises(ValueError, match="unsupported lang"):
            get_template("dev-team", "fr")  # type: ignore[arg-type]


class TestPackagedTeamData:
    """Guard against regressions in pyproject.toml force-include — if
    the team tree stops shipping, imports still work but every
    get_template call would break at runtime.
    """

    def test_index_json_is_packaged(self) -> None:
        data_dir = resources.files("fcop.teams").joinpath("_data")
        assert data_dir.joinpath("index.json").is_file()

    @pytest.mark.parametrize("team", ["dev-team", "media-team", "mvp-team", "qa-team"])
    def test_team_dir_is_packaged(self, team: str) -> None:
        team_dir = (
            resources.files("fcop.teams").joinpath("_data").joinpath(team)
        )
        # Smoke: every team ships at least its Chinese README.
        assert team_dir.joinpath("README.md").is_file()
