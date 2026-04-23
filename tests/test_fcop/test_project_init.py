"""Tests for :class:`fcop.Project` initialization — the D3-c3 surface.

Covers:
    * Preset-team init (``Project.init``) — writes fcop.json + tree.
    * Solo init (``Project.init_solo``).
    * Custom init (``Project.init_custom``) and the ``validate_team``
      pre-flight.
    * ``force=True`` archiving to ``.fcop/migrations/``.
    * Round-trip init → Project.config without information loss.

Bundled team metadata is covered separately in :mod:`test_teams`; here
we stick to the integration surface on :class:`Project`.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from fcop import Project
from fcop.core.config import load_team_config
from fcop.errors import (
    ProjectAlreadyInitializedError,
    TeamNotFoundError,
    ValidationError,
)
from fcop.models import TeamConfig

# ── init (preset) ─────────────────────────────────────────────────────


class TestInitPreset:
    def test_writes_fcop_json_and_tree(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        status = project.init(team="dev-team")

        # fcop.json landed in the canonical location.
        assert project.config_path.is_file()
        assert project.is_initialized() is True

        # Canonical tree is present.
        for directory in (
            project.tasks_dir,
            project.reports_dir,
            project.issues_dir,
            project.shared_dir,
            project.log_dir,
        ):
            assert directory.is_dir()

        # Returned status reflects the fresh init.
        assert status.is_initialized is True
        assert status.config is not None
        assert status.config.mode == "preset"
        assert status.config.team == "dev-team"
        assert status.config.leader == "PM"
        assert status.config.roles == ("PM", "DEV", "QA", "OPS")
        assert status.tasks_open == 0

    def test_default_team_is_dev_team(self, tmp_path: Path) -> None:
        # Unexpected default changes would break downstream tooling,
        # so we pin it here.
        status = Project(tmp_path).init()
        assert status.config is not None
        assert status.config.team == "dev-team"

    def test_unknown_team_raises(self, tmp_path: Path) -> None:
        with pytest.raises(TeamNotFoundError) as excinfo:
            Project(tmp_path).init(team="mystery-team")
        assert excinfo.value.team == "mystery-team"

    def test_refuses_to_overwrite_without_force(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        project.init(team="dev-team")
        with pytest.raises(ProjectAlreadyInitializedError):
            project.init(team="media-team")

    def test_force_archives_old_config(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        project.init(team="dev-team", lang="zh")

        # Different team the second time so we can distinguish on disk.
        project.init(team="media-team", lang="en", force=True)

        reloaded = project.config
        assert reloaded.team == "media-team"
        assert reloaded.leader == "PUBLISHER"
        assert reloaded.lang == "en"

        # The old config should have landed under .fcop/migrations/.
        migrations = tmp_path / ".fcop" / "migrations"
        assert migrations.is_dir()
        archived = list(migrations.rglob("fcop.json"))
        assert len(archived) == 1

        # The archived file should still carry the old team.
        archived_cfg = load_team_config(archived[0])
        assert archived_cfg.team == "dev-team"

    def test_lang_is_persisted(self, tmp_path: Path) -> None:
        status = Project(tmp_path).init(team="dev-team", lang="en")
        assert status.config is not None
        assert status.config.lang == "en"


# ── init_solo ─────────────────────────────────────────────────────────


class TestInitSolo:
    def test_default_me_role(self, tmp_path: Path) -> None:
        status = Project(tmp_path).init_solo()
        assert status.config is not None
        assert status.config.mode == "solo"
        assert status.config.is_solo is True
        assert status.config.leader == "ME"
        assert status.config.roles == ("ME",)

    def test_custom_solo_role(self, tmp_path: Path) -> None:
        status = Project(tmp_path).init_solo(role_code="CODER")
        assert status.config is not None
        assert status.config.leader == "CODER"
        assert status.config.roles == ("CODER",)

    def test_rejects_admin(self, tmp_path: Path) -> None:
        # ADMIN is reserved for the human operator; letting an AI
        # claim it would undermine Rule 2.
        with pytest.raises(ValidationError) as excinfo:
            Project(tmp_path).init_solo(role_code="ADMIN")
        # .issues carries the structured details the UI can render.
        assert any("reserved" in i.message for i in excinfo.value.issues)

    def test_rejects_bad_grammar(self, tmp_path: Path) -> None:
        with pytest.raises(ValidationError):
            Project(tmp_path).init_solo(role_code="lowercase")

    def test_force_reinit(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        project.init_solo(role_code="ME")
        project.init_solo(role_code="CODER", force=True)
        assert project.config.roles == ("CODER",)


# ── init_custom ───────────────────────────────────────────────────────


class TestInitCustom:
    def test_valid_custom_team(self, tmp_path: Path) -> None:
        status = Project(tmp_path).init_custom(
            team_name="my-squad",
            roles=["LEAD", "BUILDER", "CRITIC"],
            leader="LEAD",
        )
        assert status.config is not None
        assert status.config.mode == "custom"
        assert status.config.team == "my-squad"
        assert status.config.roles == ("LEAD", "BUILDER", "CRITIC")
        assert status.config.leader == "LEAD"

    def test_hyphenated_roles_accepted(self, tmp_path: Path) -> None:
        # Hyphenated codes like LEAD-QA are part of the grammar; a
        # custom init should handle them end-to-end.
        status = Project(tmp_path).init_custom(
            team_name="qa-squad",
            roles=["LEAD-QA", "AUTO-TESTER"],
            leader="LEAD-QA",
        )
        assert status.config is not None
        assert status.config.roles == ("LEAD-QA", "AUTO-TESTER")

    def test_leader_not_in_roles_raises(self, tmp_path: Path) -> None:
        with pytest.raises(ValidationError) as excinfo:
            Project(tmp_path).init_custom(
                team_name="x",
                roles=["A", "B"],
                leader="C",
            )
        assert any(i.field == "leader" for i in excinfo.value.issues)

    def test_empty_team_name_raises(self, tmp_path: Path) -> None:
        with pytest.raises(ValidationError):
            Project(tmp_path).init_custom(
                team_name="   ",
                roles=["PM"],
                leader="PM",
            )

    def test_duplicate_roles_raises(self, tmp_path: Path) -> None:
        with pytest.raises(ValidationError) as excinfo:
            Project(tmp_path).init_custom(
                team_name="x",
                roles=["PM", "PM", "DEV"],
                leader="PM",
            )
        assert any("duplicate" in i.message for i in excinfo.value.issues)


# ── validate_team (pure, no filesystem) ───────────────────────────────


class TestValidateTeam:
    def test_clean_team(self) -> None:
        issues = Project.validate_team(
            roles=["PM", "DEV", "QA"], leader="PM"
        )
        assert issues == []

    def test_empty_roles(self) -> None:
        issues = Project.validate_team(roles=[], leader="PM")
        assert len(issues) == 1
        assert issues[0].field == "roles"

    def test_duplicate_roles(self) -> None:
        issues = Project.validate_team(
            roles=["PM", "DEV", "PM"], leader="PM"
        )
        assert any("duplicate" in i.message for i in issues)

    def test_reserved_admin_rejected(self) -> None:
        # ADMIN in a custom team's roster means "assign an AI to ADMIN",
        # which is exactly what we forbid.
        issues = Project.validate_team(
            roles=["PM", "ADMIN"], leader="PM"
        )
        assert any(
            i.severity == "error" and "reserved" in i.message for i in issues
        )

    def test_authority_word_warning(self) -> None:
        # BOSS is stylistically discouraged but not fatal.
        issues = Project.validate_team(
            roles=["BOSS", "DEV"], leader="BOSS"
        )
        warnings = [i for i in issues if i.severity == "warning"]
        assert warnings, "BOSS should raise a stylistic warning"

    def test_leader_not_in_roles(self) -> None:
        issues = Project.validate_team(
            roles=["PM", "DEV"], leader="QA"
        )
        assert any(i.field == "leader" for i in issues)

    def test_invalid_leader_grammar(self) -> None:
        issues = Project.validate_team(
            roles=["pm"], leader="pm"
        )
        # Expect at least one error about the role grammar.
        assert any(i.severity == "error" for i in issues)


# ── round-trip: init → config ─────────────────────────────────────────


class TestRoundTrip:
    """Whatever init writes must be readable by Project.config without
    loss. Captures the implicit contract that save_team_config and
    load_team_config are mirror images of each other."""

    def test_preset_round_trip(self, tmp_path: Path) -> None:
        Project(tmp_path).init(team="dev-team", lang="zh")
        cfg = Project(tmp_path).config
        assert isinstance(cfg, TeamConfig)
        assert cfg.mode == "preset"
        assert cfg.team == "dev-team"
        assert cfg.leader == "PM"
        # created_at should have been stashed in extra.
        assert "created_at" in cfg.extra

    def test_solo_round_trip(self, tmp_path: Path) -> None:
        Project(tmp_path).init_solo(role_code="CODER")
        cfg = Project(tmp_path).config
        assert cfg.mode == "solo"
        assert cfg.is_solo is True
        assert cfg.roles == ("CODER",)

    def test_custom_round_trip(self, tmp_path: Path) -> None:
        Project(tmp_path).init_custom(
            team_name="my-squad",
            roles=["LEAD", "BUILDER"],
            leader="LEAD",
        )
        cfg = Project(tmp_path).config
        assert cfg.mode == "custom"
        assert cfg.team == "my-squad"
        assert cfg.roles == ("LEAD", "BUILDER")
