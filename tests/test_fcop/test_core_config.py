"""Unit tests for :mod:`fcop.core.config` — the pure configuration
parser. Integration with :class:`fcop.Project` is covered in
:mod:`test_project_identity`; here we focus on the parser's behavior
in isolation, especially the structural validation error paths that
are inconvenient to exercise through the full Project API.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from fcop.core.config import load_team_config, parse_team_config
from fcop.errors import ConfigError

# ── parse_team_config: happy paths ────────────────────────────────────


class TestParseHappyPaths:
    def test_minimal_preset(self) -> None:
        cfg = parse_team_config(
            {
                "mode": "preset",
                "team": "dev-team",
                "leader": "PM",
                "roles": ["PM", "DEV"],
                "lang": "zh",
            }
        )
        assert cfg.mode == "preset"
        assert cfg.version == 1  # default from PROTOCOL_VERSION
        assert cfg.extra == {}

    def test_solo_with_me_role(self) -> None:
        cfg = parse_team_config(
            {
                "mode": "solo",
                "team": "solo",
                "leader": "ME",
                "roles": ["ME"],
                "lang": "en",
            }
        )
        assert cfg.is_solo is True

    def test_custom_with_hyphenated_roles(self) -> None:
        # Hyphenated role codes are explicitly part of the grammar; a
        # custom team should be able to use them end-to-end.
        cfg = parse_team_config(
            {
                "mode": "custom",
                "team": "ops-squad",
                "leader": "LEAD-OPS",
                "roles": ["LEAD-OPS", "DB-ADMIN"],
                "lang": "zh",
            }
        )
        assert cfg.roles == ("LEAD-OPS", "DB-ADMIN")
        assert cfg.leader == "LEAD-OPS"

    def test_unknown_top_level_keys_go_to_extra(self) -> None:
        cfg = parse_team_config(
            {
                "mode": "preset",
                "team": "dev-team",
                "leader": "PM",
                "roles": ["PM"],
                "lang": "zh",
                "created_at": "2026-01-01T00:00:00Z",
                "custom_key": {"nested": True},
            }
        )
        assert cfg.extra == {
            "created_at": "2026-01-01T00:00:00Z",
            "custom_key": {"nested": True},
        }


# ── parse_team_config: legacy compatibility ───────────────────────────


class TestLegacyCompat:
    def test_team_mode_alias_maps_to_preset(self) -> None:
        cfg = parse_team_config(
            {
                "mode": "team",
                "team": "dev-team",
                "leader": "PM",
                "roles": ["PM"],
                "lang": "zh",
            }
        )
        assert cfg.mode == "preset"

    def test_role_dicts_are_flattened_and_labels_preserved(self) -> None:
        cfg = parse_team_config(
            {
                "mode": "preset",
                "team": "media-team",
                "leader": "PUBLISHER",
                "roles": [
                    {"code": "PUBLISHER", "label_zh": "审核发行"},
                    {"code": "WRITER", "label_zh": "拟题提纲"},
                ],
                "lang": "zh",
            }
        )
        assert cfg.roles == ("PUBLISHER", "WRITER")
        labels = cfg.extra["_role_labels"]
        assert labels == {
            "PUBLISHER": {"label_zh": "审核发行"},
            "WRITER": {"label_zh": "拟题提纲"},
        }


# ── parse_team_config: error paths ────────────────────────────────────


class TestParseErrors:
    """Every invalid shape raises ConfigError with a path attribute."""

    def test_non_dict_top_level(self) -> None:
        with pytest.raises(ConfigError, match="top-level must be a JSON object"):
            parse_team_config(["not", "a", "dict"])

    def test_missing_mode(self) -> None:
        with pytest.raises(ConfigError, match="'mode'"):
            parse_team_config({"team": "x", "leader": "PM", "roles": ["PM"]})

    def test_unknown_mode(self) -> None:
        with pytest.raises(ConfigError, match="must be one of"):
            parse_team_config(
                {
                    "mode": "invalid-mode",
                    "team": "x",
                    "leader": "PM",
                    "roles": ["PM"],
                }
            )

    def test_missing_team(self) -> None:
        with pytest.raises(ConfigError, match="'team'"):
            parse_team_config(
                {"mode": "preset", "leader": "PM", "roles": ["PM"]}
            )

    def test_empty_team_string(self) -> None:
        with pytest.raises(ConfigError, match="'team'"):
            parse_team_config(
                {"mode": "preset", "team": "  ", "leader": "PM", "roles": ["PM"]}
            )

    def test_empty_roles_list(self) -> None:
        with pytest.raises(ConfigError, match="non-empty list"):
            parse_team_config(
                {"mode": "preset", "team": "x", "leader": "PM", "roles": []}
            )

    def test_role_entry_wrong_type(self) -> None:
        with pytest.raises(ConfigError, match=r"roles\[0\]"):
            parse_team_config(
                {
                    "mode": "preset",
                    "team": "x",
                    "leader": "PM",
                    "roles": [123],
                }
            )

    def test_role_dict_without_code(self) -> None:
        with pytest.raises(ConfigError, match=r"roles\[0\].code"):
            parse_team_config(
                {
                    "mode": "preset",
                    "team": "x",
                    "leader": "PM",
                    "roles": [{"label": "orphan"}],
                }
            )

    def test_duplicate_role_code(self) -> None:
        with pytest.raises(ConfigError, match="duplicate"):
            parse_team_config(
                {
                    "mode": "preset",
                    "team": "x",
                    "leader": "PM",
                    "roles": ["PM", "PM"],
                }
            )

    def test_version_must_be_int(self) -> None:
        with pytest.raises(ConfigError, match="'version'"):
            parse_team_config(
                {
                    "mode": "preset",
                    "team": "x",
                    "leader": "PM",
                    "roles": ["PM"],
                    "version": "1",
                }
            )

    def test_version_bool_rejected(self) -> None:
        # isinstance(True, int) is True in Python; guard explicitly.
        with pytest.raises(ConfigError, match="'version'"):
            parse_team_config(
                {
                    "mode": "preset",
                    "team": "x",
                    "leader": "PM",
                    "roles": ["PM"],
                    "version": True,
                }
            )

    def test_negative_version_rejected(self) -> None:
        with pytest.raises(ConfigError, match=">= 1"):
            parse_team_config(
                {
                    "mode": "preset",
                    "team": "x",
                    "leader": "PM",
                    "roles": ["PM"],
                    "version": 0,
                }
            )


# ── load_team_config: filesystem boundary ─────────────────────────────


class TestLoadTeamConfig:
    def test_file_not_found(self, tmp_path: Path) -> None:
        with pytest.raises(ConfigError, match="not found"):
            load_team_config(tmp_path / "missing.json")

    def test_invalid_json(self, tmp_path: Path) -> None:
        path = tmp_path / "fcop.json"
        path.write_text("{ not json", encoding="utf-8")
        with pytest.raises(ConfigError, match="valid JSON"):
            load_team_config(path)

    def test_valid_json_is_parsed(self, tmp_path: Path) -> None:
        path = tmp_path / "fcop.json"
        path.write_text(
            '{"mode": "solo", "team": "solo", "leader": "ME", "roles": ["ME"], "lang": "en"}',
            encoding="utf-8",
        )
        cfg = load_team_config(path)
        assert cfg.is_solo is True
