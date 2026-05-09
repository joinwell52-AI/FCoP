"""failure.schema.json —— 抽象 5（Failure & Recovery）回归。

ADR-0019 / TASK-004 R1 §A3。
"""

from __future__ import annotations

import pytest

V10_FAILURES = {"TIMEOUT", "CRASH", "DEADLOCK", "DRIFT"}
V10_RECOVERIES = {"RETRY", "RESUME", "ROLLBACK", "ABORT", "ESCALATE"}


def test_vocab_frozen(schemas):
    s = schemas["failure.schema.json"]
    assert set(s["$defs"]["failureType"]["enum"]) == V10_FAILURES
    assert set(s["$defs"]["recoveryAction"]["enum"]) == V10_RECOVERIES


def test_legal_failure_record(validator_for):
    v = validator_for("failure.schema.json")
    rec = {
        "kind": "failure",
        "failure_type": "TIMEOUT",
        "subject": {"task_id": "TASK-20260601-001-PM-to-DEV", "agent_code": "DEV"},
        "detected_at": "2026-06-01T10:00:00Z",
        "evidence": {"last_seen_at": "2026-06-01T09:50:00Z"},
        "suggested_recovery": "RETRY",
    }
    assert list(v.iter_errors(rec)) == []


def test_legal_recovery_record(validator_for):
    v = validator_for("failure.schema.json")
    rec = {
        "kind": "recovery",
        "recovery_action": "RESUME",
        "subject": {"task_id": "TASK-20260601-001-PM-to-DEV"},
        "initiated_at": "2026-06-01T10:01:00Z",
        "outcome": "in_progress",
        "trigger_failure_id": "fail-001",
    }
    assert list(v.iter_errors(rec)) == []


def test_legal_session_recovery_call(validator_for):
    v = validator_for("failure.schema.json")
    rec = {
        "kind": "session_recovery_call",
        "session_id": "TASK-20260601-001:DEV",
        "action": "resume",
    }
    assert list(v.iter_errors(rec)) == []


def test_unknown_failure_type_rejected(validator_for):
    v = validator_for("failure.schema.json")
    rec = {
        "kind": "failure",
        "failure_type": "MELTDOWN",
        "subject": {"task_id": "x"},
        "detected_at": "2026-06-01T10:00:00Z",
    }
    errs = list(v.iter_errors(rec))
    assert errs


def test_session_recovery_action_limited_to_three(validator_for):
    """ADR-0019 §session-recovery-hook：仅暴露 resume/rollback/abort。"""
    v = validator_for("failure.schema.json")
    rec = {
        "kind": "session_recovery_call",
        "session_id": "TASK-001:DEV",
        "action": "RETRY",  # 不在 hook 暴露的 3 类内
    }
    errs = list(v.iter_errors(rec))
    assert errs


def test_missing_kind_rejected(validator_for):
    """oneOf discriminator 字段 'kind' 缺失 → 三个分支都不命中 → 拒。"""
    v = validator_for("failure.schema.json")
    rec = {
        "failure_type": "TIMEOUT",
        "subject": {"task_id": "x"},
        "detected_at": "2026-06-01T10:00:00Z",
    }
    errs = list(v.iter_errors(rec))
    assert errs


@pytest.mark.parametrize("ft", sorted(V10_FAILURES))
def test_each_failure_type(validator_for, ft):
    v = validator_for("failure.schema.json")
    rec = {
        "kind": "failure",
        "failure_type": ft,
        "subject": {"task_id": "x"},
        "detected_at": "2026-06-01T10:00:00Z",
    }
    assert list(v.iter_errors(rec)) == []


@pytest.mark.parametrize("ra", sorted(V10_RECOVERIES))
def test_each_recovery_action(validator_for, ra):
    v = validator_for("failure.schema.json")
    rec = {
        "kind": "recovery",
        "recovery_action": ra,
        "subject": {"task_id": "x"},
        "initiated_at": "2026-06-01T10:00:00Z",
    }
    assert list(v.iter_errors(rec)) == []
