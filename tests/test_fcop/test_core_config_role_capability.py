"""tests/test_fcop/test_core_config_role_capability.py —— A9：dict-form
roles 的 layer / can / cannot 字段 round-trip 单测。

按 TASK-20260509-005 R2 §A9。
"""

from __future__ import annotations

from pathlib import Path

import pytest

from fcop.core.config import (
    load_team_config,
    parse_team_config,
    save_team_config,
    serialize_team_config,
)
from fcop.errors import ConfigError


def _legal_dict_form_config() -> dict:
    return {
        "mode": "preset",
        "team": "dev-team",
        "leader": "PM",
        "lang": "zh",
        "version": 1,
        "roles": [
            {"code": "PM", "label": "项目经理", "layer": "governance"},
            {"code": "DEV", "label": "开发", "layer": "worker", "can": ["modify_code"]},
            {"code": "QA", "layer": "worker", "cannot": ["modify_code"]},
        ],
    }


class TestParseRoleCapability:
    def test_layer_can_cannot_preserved_in_role_labels(self):
        cfg = parse_team_config(_legal_dict_form_config())
        labels = cfg.extra["_role_labels"]
        assert labels["PM"]["layer"] == "governance"
        assert labels["DEV"]["can"] == ["modify_code"]
        assert labels["QA"]["cannot"] == ["modify_code"]
        # 既有 label 字段不丢
        assert labels["PM"]["label"] == "项目经理"

    def test_role_codes_extracted_correctly(self):
        cfg = parse_team_config(_legal_dict_form_config())
        assert cfg.roles == ("PM", "DEV", "QA")

    def test_layer_must_be_string(self):
        raw = _legal_dict_form_config()
        raw["roles"][0]["layer"] = 42
        with pytest.raises(ConfigError, match="layer"):
            parse_team_config(raw)

    def test_can_must_be_list_of_strings(self):
        raw = _legal_dict_form_config()
        raw["roles"][1]["can"] = "modify_code"  # 不是 list
        with pytest.raises(ConfigError, match="can"):
            parse_team_config(raw)

    def test_cannot_must_be_list_of_strings(self):
        raw = _legal_dict_form_config()
        raw["roles"][2]["cannot"] = [123]
        with pytest.raises(ConfigError, match="cannot"):
            parse_team_config(raw)

    def test_can_null_is_legal(self):
        raw = _legal_dict_form_config()
        raw["roles"][1]["can"] = None
        cfg = parse_team_config(raw)
        # null 被保留进 _role_labels（lookup_capability 会 normalize 为 ()）
        assert cfg.extra["_role_labels"]["DEV"].get("can") is None


class TestRoundTrip:
    def test_serialize_load_round_trip(self, tmp_path: Path):
        cfg = parse_team_config(_legal_dict_form_config())
        target = tmp_path / "fcop.json"
        save_team_config(cfg, target)
        # 再 load 一次
        cfg2 = load_team_config(target)
        assert cfg2.roles == cfg.roles
        assert cfg2.extra["_role_labels"] == cfg.extra["_role_labels"]

    def test_serialize_writes_role_labels_under_extra(self, tmp_path: Path):
        cfg = parse_team_config(_legal_dict_form_config())
        text = serialize_team_config(cfg)
        # _role_labels 字段必须出现在 serialize 输出（否则 round-trip 丢数据）
        assert "_role_labels" in text
        # layer / can / cannot 三个字符串都能在 serialize 输出中找到
        assert "governance" in text
        assert "modify_code" in text


class TestStringFormStillWorks:
    """保 0.7.x backward compat：纯 string roles 仍可用，无 _role_labels。"""

    def test_string_form_no_labels(self):
        raw = {
            "mode": "preset",
            "team": "dev-team",
            "leader": "PM",
            "lang": "zh",
            "version": 1,
            "roles": ["PM", "DEV", "QA"],
        }
        cfg = parse_team_config(raw)
        assert cfg.roles == ("PM", "DEV", "QA")
        assert "_role_labels" not in cfg.extra
