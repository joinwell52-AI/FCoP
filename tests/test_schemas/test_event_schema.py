"""event.schema.json —— 抽象 4（Event Model）回归。

ADR-0018 + ADR-0019 / TASK-004 R1 §A3。
"""

from __future__ import annotations

import pytest

V10_EVENTS = {
    "TASK_CREATED",
    "TASK_ACCEPTED",
    "TASK_BLOCKED",
    "TASK_COMPLETED",
    "REPORT_FILED",
    "REVIEW_DECIDED",
    "BOUNDARY_VIOLATED",
    "ROLE_SWITCHED",
    "FAILURE_DETECTED",
    "RECOVERY_INITIATED",
    "RECOVERY_COMPLETED",
    "SESSION_LOST",
}


def test_event_type_vocab_matches_spec(schemas):
    """event.schema.json 必须列 12 个事件，与 ADR-0018+0019 一致。"""
    s = schemas["event.schema.json"]
    enum = set(s["$defs"]["eventType"]["enum"])
    assert enum == V10_EVENTS, f"vocab drifted: {enum ^ V10_EVENTS}"


def test_legal_task_created_event(validator_for):
    v = validator_for("event.schema.json")
    rec = {
        "event_id": "evt-001",
        "event_type": "TASK_CREATED",
        "occurred_at": "2026-06-01T10:00:00Z",
        "subject": {"task_id": "TASK-20260601-001-PM-to-DEV"},
        "source": {"kind": "file", "path": "fcop/tasks/TASK-20260601-001-PM-to-DEV.md"},
    }
    assert list(v.iter_errors(rec)) == []


def test_legal_review_decided_with_cross_ref(validator_for):
    """REVIEW_DECIDED 的 subject.decision 走 cross-$ref 到 review.schema.json。"""
    v = validator_for("event.schema.json")
    rec = {
        "event_id": "evt-002",
        "event_type": "REVIEW_DECIDED",
        "occurred_at": "2026-06-01T10:01:00Z",
        "subject": {
            "review_id": "REVIEW-20260601-001-ADMIN-on-task-001",
            "decision": "approved",
        },
        "source": {"kind": "file", "path": "fcop/reviews/REVIEW-20260601-001-ADMIN-on-task-001.md"},
    }
    assert list(v.iter_errors(rec)) == []


def test_unknown_event_type_rejected(validator_for):
    v = validator_for("event.schema.json")
    rec = {
        "event_id": "evt-003",
        "event_type": "ALIEN_LANDED",  # 不在 12 内
        "occurred_at": "2026-06-01T10:02:00Z",
        "subject": {},
        "source": {"kind": "derived"},
    }
    errs = list(v.iter_errors(rec))
    assert errs, "unknown event_type must be rejected"


def test_missing_required_field_rejected(validator_for):
    v = validator_for("event.schema.json")
    rec = {
        "event_id": "evt-004",
        # 缺 event_type
        "occurred_at": "2026-06-01T10:03:00Z",
        "subject": {},
        "source": {"kind": "file", "path": "x"},
    }
    errs = list(v.iter_errors(rec))
    assert errs


def test_invalid_source_kind_rejected(validator_for):
    v = validator_for("event.schema.json")
    rec = {
        "event_id": "evt-005",
        "event_type": "TASK_CREATED",
        "occurred_at": "2026-06-01T10:04:00Z",
        "subject": {"task_id": "x"},
        "source": {"kind": "telepathy"},  # source.kind enum 限定
    }
    errs = list(v.iter_errors(rec))
    assert errs, "unknown source.kind must be rejected"


@pytest.mark.parametrize("ev", sorted(V10_EVENTS))
def test_each_event_type_alone_validates(validator_for, ev):
    v = validator_for("event.schema.json")
    rec = {
        "event_id": f"evt-{ev}",
        "event_type": ev,
        "occurred_at": "2026-06-01T10:00:00Z",
        "subject": {},
        "source": {"kind": "derived"},
    }
    errs = list(v.iter_errors(rec))
    assert errs == [], f"{ev} should validate as a bare event"
