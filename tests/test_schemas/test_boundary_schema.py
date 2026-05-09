"""boundary.schema.json —— 抽象 6（Boundary & Capability）回归。

ADR-0020 / TASK-004 R1 §A3。
"""

from __future__ import annotations

import pytest

V10_VOCAB = {
    "file_io",
    "task_io",
    "modify_code",
    "review_decision",
    "approve_release",
    "escalate",
    "spawn_agent",
    "override",
    "archive",
    "mark_done",
}


def test_capability_token_def_exists(schemas):
    """capabilityToken 是其他 schema 的 cross-ref 锚点；必须存在且
    enum 长度 = 10。"""
    s = schemas["boundary.schema.json"]
    cap = s["$defs"]["capabilityToken"]
    assert cap["type"] == "string"
    assert set(cap["enum"]) == V10_VOCAB


def test_legal_full_registry(validator_for):
    """完整 vocabulary registry 文档（所有字段满足）。"""
    v = validator_for("boundary.schema.json")
    rec = {
        "vocabulary_version": "1.0.0",
        "tokens": sorted(V10_VOCAB),
        "rules": [
            {"id": "NO_ADMIN_PROGRAMMATIC_CREATE", "rule": "..."},
            {"id": "NO_GOVERNANCE_FISSION", "rule": "..."},
            {"id": "NO_WORKER_REVIEWS_GOVERNANCE", "rule": "..."},
            {"id": "EXPLICIT_OVERRIDES_LAYER", "rule": "..."},
        ],
    }
    assert list(v.iter_errors(rec)) == []


def test_tokens_must_be_exactly_10(validator_for):
    """tokens 数组长度被 minItems=maxItems=10 锁住。"""
    v = validator_for("boundary.schema.json")
    rec = {
        "vocabulary_version": "1.0.0",
        "tokens": ["file_io", "task_io"],  # 2 个 < 10
        "rules": [
            {"id": "NO_ADMIN_PROGRAMMATIC_CREATE", "rule": "x"},
            {"id": "NO_GOVERNANCE_FISSION", "rule": "x"},
            {"id": "NO_WORKER_REVIEWS_GOVERNANCE", "rule": "x"},
            {"id": "EXPLICIT_OVERRIDES_LAYER", "rule": "x"},
        ],
    }
    errs = list(v.iter_errors(rec))
    assert errs, "tokens length != 10 must be rejected"


def test_unknown_rule_id_rejected(validator_for):
    """boundaryRule.id 是 closed enum；新规则要新发 ADR + bump MINOR。"""
    v = validator_for("boundary.schema.json")
    rec = {
        "vocabulary_version": "1.0.0",
        "tokens": sorted(V10_VOCAB),
        "rules": [
            {"id": "NO_ADMIN_PROGRAMMATIC_CREATE", "rule": "x"},
            {"id": "NO_GOVERNANCE_FISSION", "rule": "x"},
            {"id": "NO_WORKER_REVIEWS_GOVERNANCE", "rule": "x"},
            {"id": "MAKE_COFFEE_FOR_ME", "rule": "x"},  # 非法
        ],
    }
    errs = list(v.iter_errors(rec))
    assert errs, "unknown rule id must be rejected"


@pytest.mark.parametrize(
    "tok,legal",
    [
        ("file_io", True),
        ("task_io", True),
        ("modify_code", True),
        ("override", True),
        ("hack_the_planet", False),
        ("FILE_IO", False),  # 大小写敏感
        ("", False),
    ],
)
def test_capability_token_per_value(validator_for, tok, legal):
    """通过 boundary.schema.json 的 $defs.capabilityToken 单独校验
    一个 token；用 generic agent.can 的 wrapper 间接调一下。"""
    from jsonschema import Draft202012Validator

    from fcop.core.jsonschema_validator import SCHEMA_REGISTRY

    cap_only = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$ref": "https://fcop.dev/schemas/boundary/v1.0.json#/$defs/capabilityToken",
    }
    v = Draft202012Validator(cap_only, registry=SCHEMA_REGISTRY)
    errs = list(v.iter_errors(tok))
    if legal:
        assert errs == [], f"{tok!r} should be a legal capability token"
    else:
        assert errs, f"{tok!r} should be rejected"
