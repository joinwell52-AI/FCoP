"""agent.schema.json —— 抽象 1（Agent）回归测试。

ADR-0020 §design-details / TASK-004 R1 §A3。
"""

from __future__ import annotations


def test_legal_minimal_agent(validator_for):
    """code + label 是仅有的必填字段。"""
    v = validator_for("agent.schema.json")
    assert list(v.iter_errors({"code": "DEV", "label": "Developer"})) == []


def test_legal_full_agent(validator_for):
    """完整 worker，含显式 can/cannot —— 跨文件 $ref 必须解析成功。"""
    v = validator_for("agent.schema.json")
    rec = {
        "code": "DEV",
        "label": "开发者",
        "layer": "worker",
        "can": ["file_io", "task_io", "modify_code"],
        "cannot": ["spawn_agent", "approve_release"],
        "session_id": "TASK-20260601-001:DEV",
    }
    assert list(v.iter_errors(rec)) == []


def test_missing_required_label(validator_for):
    """缺 label 必须报错（required 列表里）。"""
    v = validator_for("agent.schema.json")
    errs = list(v.iter_errors({"code": "DEV"}))
    assert errs, "missing label must surface as a validation error"
    assert any("label" in e.message for e in errs)


def test_lowercase_code_rejected(validator_for):
    """code 必须匹配 ^[A-Z][A-Z0-9]{0,15}$。"""
    v = validator_for("agent.schema.json")
    errs = list(v.iter_errors({"code": "dev", "label": "x"}))
    assert errs, "lowercase role code must be rejected"


def test_admin_layer_is_legal_in_schema_only(validator_for):
    """schema 层面 admin 是合法 enum 值；运行时拒（per ADR-0020 B1）由
    boundary 模块在 TASK-005 实现。本测试只盯 schema 边界。"""
    v = validator_for("agent.schema.json")
    rec = {"code": "ADMIN", "label": "human operator", "layer": "admin"}
    assert list(v.iter_errors(rec)) == []


def test_unknown_capability_via_cross_ref_rejected(validator_for):
    """can 中含 boundary 词表外的 token 应被 cross-$ref 拒。"""
    v = validator_for("agent.schema.json")
    errs = list(v.iter_errors({"code": "DEV", "label": "x", "can": ["fly"]}))
    assert errs, "unknown capability token must be rejected via cross-ref"
