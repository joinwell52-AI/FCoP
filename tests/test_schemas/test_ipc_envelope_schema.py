"""ipc-envelope.schema.json —— 抽象 3（IPC）回归。

ADR-0017 + 0.7.x 基线 / TASK-004 R1 §A3。
"""

from __future__ import annotations


def test_legal_task_envelope(validator_for):
    v = validator_for("ipc-envelope.schema.json")
    rec = {
        "protocol": "fcop",
        "version": 1,
        "type": "TASK",
        "sender": "PM",
        "recipient": "DEV",
        "subject": "实现登录页",
        "priority": "P1",
    }
    assert list(v.iter_errors(rec)) == []


def test_legal_report_envelope(validator_for):
    v = validator_for("ipc-envelope.schema.json")
    rec = {
        "protocol": "fcop",
        "version": 1,
        "type": "REPORT",
        "sender": "DEV",
        "recipient": "PM",
        "ref_task": "fcop/tasks/TASK-20260601-001-PM-to-DEV.md",
        "status": "done",
    }
    assert list(v.iter_errors(rec)) == []


def test_legal_issue_envelope(validator_for):
    v = validator_for("ipc-envelope.schema.json")
    rec = {
        "protocol": "fcop",
        "version": 1,
        "type": "ISSUE",
        "sender": "QA",
        "subject": "建议加 e2e 测试",
    }
    assert list(v.iter_errors(rec)) == []


def test_legal_review_envelope(validator_for):
    """REVIEW 是 v1.0 新增；走 cross-$ref 到 review.schema.json。"""
    v = validator_for("ipc-envelope.schema.json")
    rec = {
        "protocol": "fcop",
        "version": 1,
        "type": "REVIEW",
        "sender": "ADMIN",
        "subject_type": "task",
        "subject_ref": "fcop/tasks/TASK-20260601-001-PM-to-DEV.md",
        "decision": "approved",
    }
    assert list(v.iter_errors(rec)) == []


def test_protocol_must_be_literal_fcop(validator_for):
    v = validator_for("ipc-envelope.schema.json")
    rec = {
        "protocol": "agent_bridge",  # 旧别名（normalize 后 OK，但 schema 严格 const='fcop'）
        "version": 1,
        "type": "TASK",
        "sender": "PM",
        "recipient": "DEV",
        "subject": "x",
    }
    errs = list(v.iter_errors(rec))
    assert errs, "protocol must be the literal 'fcop' on disk"


def test_unknown_envelope_type_rejected(validator_for):
    v = validator_for("ipc-envelope.schema.json")
    rec = {
        "protocol": "fcop",
        "version": 1,
        "type": "BROADCAST",  # 不在 4 类内
        "sender": "PM",
        "subject": "x",
    }
    errs = list(v.iter_errors(rec))
    assert errs


def test_extra_keys_at_root_are_allowed(validator_for):
    """envelope root additionalProperties: true（保 0.7.x 兼容）。"""
    v = validator_for("ipc-envelope.schema.json")
    rec = {
        "protocol": "fcop",
        "version": 1,
        "type": "TASK",
        "sender": "PM",
        "recipient": "DEV",
        "subject": "x",
        "thread_key": "auth-flow",  # 0.7.x 字段
        "custom_legacy_key": "anything",
    }
    assert list(v.iter_errors(rec)) == []


def test_task_missing_recipient_rejected(validator_for):
    v = validator_for("ipc-envelope.schema.json")
    rec = {
        "protocol": "fcop",
        "version": 1,
        "type": "TASK",
        "sender": "PM",
        "subject": "x",
    }
    errs = list(v.iter_errors(rec))
    assert errs, "TASK without recipient must be rejected"
