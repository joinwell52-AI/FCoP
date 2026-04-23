"""Tests for :mod:`fcop.teams` — bundled preset team registry.

These tests pin the 0.6.0 preset team catalogue: changing a role list
or leader in ``_BUNDLED_TEAMS`` will fail here, forcing the author to
either update the test *and* CHANGELOG (legitimate change) or back out
(accidental change). The presets are public API in the sense that
``Project.init(team=X)`` promises to produce the roles listed here.
"""

from __future__ import annotations

import pytest

from fcop.errors import TeamNotFoundError
from fcop.teams import (
    TeamInfo,
    get_available_teams,
    get_team_info,
    get_template,
)


class TestRegistry:
    def test_get_available_teams_is_sorted(self) -> None:
        teams = get_available_teams()
        names = [t.name for t in teams]
        assert names == sorted(names)
        # The four bundled presets — guardrail for accidental removal.
        assert set(names) == {"dev-team", "media-team", "mvp-team", "qa-team"}

    def test_every_entry_is_a_frozen_team_info(self) -> None:
        for info in get_available_teams():
            assert isinstance(info, TeamInfo)
            # Frozen dataclass — mutation is a contract violation.
            with pytest.raises(Exception):  # noqa: B017, PT011
                info.leader = "HACKED"  # type: ignore[misc]

    @pytest.mark.parametrize(
        ("team", "leader", "role_set"),
        [
            ("dev-team", "PM", {"PM", "DEV", "QA", "OPS"}),
            ("media-team", "PUBLISHER", {"PUBLISHER", "COLLECTOR", "WRITER"}),
            ("mvp-team", "PM", {"PM", "BUILDER", "SELLER"}),
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


class TestTemplateStubbed:
    def test_get_template_raises_not_implemented(self) -> None:
        # Template text migration is D5 per ADR-0001; explicitly
        # verify the stub so the commit that flips it on also flips
        # this test.
        with pytest.raises(NotImplementedError):
            get_template("dev-team")
