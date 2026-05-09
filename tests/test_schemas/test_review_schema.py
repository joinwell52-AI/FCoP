"""review.schema.json —— 抽象 7（Audit / REVIEW）回归。

ADR-0017（最小面） / TASK-004 R1 §A3。

特别重要：本测试**显式拒**收 v1.2 推迟值（needs_human）—— 防止被偷塞。
"""

from __future__ import annotations

import pytest


def _legal_review():
    return {
        "protocol": "fcop",
        "version": 1,
        "type": "REVIEW",
        "review_id": "REVIEW-20260601-001-ADMIN-on-task-001",
        "subject_type": "task",
        "subject_ref": "fcop/tasks/TASK-20260601-001-PM-to-DEV.md",
        "reviewer_role": "ADMIN",
        "decision": "approved",
        "decided_at": "2026-06-01T10:00:00Z",
    }


def test_decision_enum_is_exactly_four(schemas):
    """4 值 enum FROZEN for v1.0；新增 needs_human 等只能在 v1.2+ 走 ADR。"""
    s = schemas["review.schema.json"]
    enum = set(s["$defs"]["decisionEnum"]["enum"])
    assert enum == {"approved", "rejected", "needs_changes", "abstained"}


def test_subject_type_enum_is_exactly_four(schemas):
    s = schemas["review.schema.json"]
    enum = set(s["$defs"]["subjectType"]["enum"])
    assert enum == {"task", "report", "role_switch", "code_change"}


def test_legal_minimal_approved(validator_for):
    v = validator_for("review.schema.json")
    assert list(v.iter_errors(_legal_review())) == []


def test_legal_needs_changes_with_required_changes(validator_for):
    v = validator_for("review.schema.json")
    rec = _legal_review()
    rec["decision"] = "needs_changes"
    rec["required_changes"] = ["加单元测试", "修两处 typo"]
    rec["rationale"] = "v1 缺关键测试"
    assert list(v.iter_errors(rec)) == []


def test_needs_changes_with_empty_required_changes_rejected(validator_for):
    """ADR-0017 if/then 条件：needs_changes 必须非空 required_changes。"""
    v = validator_for("review.schema.json")
    rec = _legal_review()
    rec["decision"] = "needs_changes"
    rec["required_changes"] = []
    errs = list(v.iter_errors(rec))
    assert errs, "needs_changes + empty required_changes must be rejected"


def test_needs_changes_without_required_changes_rejected(validator_for):
    """完全不写 required_changes 与写空数组同等违规。"""
    v = validator_for("review.schema.json")
    rec = _legal_review()
    rec["decision"] = "needs_changes"
    # 故意不设 required_changes
    errs = list(v.iter_errors(rec))
    assert errs


def test_needs_human_rejected_at_schema_level(validator_for):
    """**最关键的防御测试**：v1.2 推迟的 'needs_human' 在 v1.0
    schema 层面就拒——防止下游 PR 偷塞它。"""
    v = validator_for("review.schema.json")
    rec = _legal_review()
    rec["decision"] = "needs_human"
    errs = list(v.iter_errors(rec))
    assert errs, "decision='needs_human' MUST be rejected by v1.0 schema"


def test_human_approval_subobject_is_not_required(schemas):
    """human_approval 子对象在 v1.0 不是 required；schema 层面不强制
    存在（v1.2 加进来时 properties 里加 + 不进 required 列表 = additive）。"""
    s = schemas["review.schema.json"]
    assert "human_approval" not in s.get("required", [])
    assert "human_approval" not in s.get("properties", {})


def test_review_id_must_match_filename_pattern(validator_for):
    """review_id 与文件名 stem 一致，pattern 严格。"""
    v = validator_for("review.schema.json")
    rec = _legal_review()
    rec["review_id"] = "review-20260601-001-admin-on-task-001"  # 小写非法
    errs = list(v.iter_errors(rec))
    assert errs


@pytest.mark.parametrize("d", ["approved", "rejected", "abstained"])
def test_each_decision_minimal(validator_for, d):
    """approved / rejected / abstained 都可以无 required_changes 通过。"""
    v = validator_for("review.schema.json")
    rec = _legal_review()
    rec["decision"] = d
    assert list(v.iter_errors(rec)) == []


def test_missing_decided_at_rejected(validator_for):
    v = validator_for("review.schema.json")
    rec = _legal_review()
    del rec["decided_at"]
    errs = list(v.iter_errors(rec))
    assert errs
