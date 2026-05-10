"""tests/test_fcop/test_review_v11_features.py — v1.1 新功能正式验证。

per ADR-0025 + ADR-0026:
- ``decision: needs_human`` 枚举值（v1.1 正式落地）
- ``human_approval`` 子对象
- ``Project.mark_human_approved`` API
- ``Review.human_approval`` dataclass 字段

这个文件替代 test_review_no_v12_features.py（旧文件已改名为 test_review_no_v12_features_RETIRED）。
"""

from __future__ import annotations

import pytest

from fcop import Project, Review, ReviewDecision
from fcop.core.jsonschema_validator import load_bundled_schema


def test_review_decision_enum_has_needs_human():
    """v1.1 起 ReviewDecision 必须包含 needs_human（per ADR-0025）。"""
    values = {d.value for d in ReviewDecision}
    assert "needs_human" in values, (
        "ReviewDecision must include 'needs_human' in v1.1 — per ADR-0025."
    )


def test_review_decision_enum_is_exactly_five():
    """v1.1 ReviewDecision 共 5 个值（4 个 v1.0 值 + needs_human）。"""
    values = {d.value for d in ReviewDecision}
    assert values == {"approved", "rejected", "needs_changes", "abstained", "needs_human"}


def test_schema_decision_enum_has_needs_human():
    """review.schema.json 的 decisionEnum 必须包含 needs_human。"""
    schema = load_bundled_schema("review.schema.json")
    enum = set(schema["$defs"]["decisionEnum"]["enum"])
    assert "needs_human" in enum


def test_schema_has_human_approval_field():
    """review.schema.json 的 properties 必须包含 human_approval（per ADR-0026）。"""
    schema = load_bundled_schema("review.schema.json")
    assert "human_approval" in schema.get("properties", {}), (
        "review.schema.json must have human_approval property per ADR-0026."
    )
    assert "humanApproval" in schema.get("$defs", {}), (
        "review.schema.json must define humanApproval $def per ADR-0026."
    )


def test_project_has_mark_human_approved():
    """Project.mark_human_approved 必须存在（per ADR-0026）。"""
    assert hasattr(Project, "mark_human_approved"), (
        "Project.mark_human_approved is a v1.1 API per ADR-0026."
    )


def test_review_dataclass_has_human_approval_field():
    """Review dataclass 必须有 human_approval 字段（per ADR-0026）。"""
    field_names = {f for f in Review.__dataclass_fields__}
    assert "human_approval" in field_names, (
        "Review must have human_approval field per ADR-0026."
    )


def test_write_review_with_needs_human(tmp_project):
    """write_review 接受 decision='needs_human'（per ADR-0025）。"""
    proj = Project(tmp_project)
    proj.init_solo(role_code="ME")
    r = proj.write_review(
        reviewer_role="ADMIN",
        subject_type="task",
        subject_ref="some-task-ref",
        decision="needs_human",
        rationale="escalating to human — risk level too high",
        subject_short="some-task",
    )
    assert r.decision is ReviewDecision.NEEDS_HUMAN
    assert r.human_approval is None  # 尚未经人工审批


@pytest.mark.parametrize(
    "bad_alias",
    ["NEEDS_HUMAN", "needs-human", "need_human", "needshuman"],
)
def test_write_review_rejects_bad_aliases(tmp_project, bad_alias):
    """只接受精确的小写 'needs_human'；其他格式应该被拒。"""
    from fcop.errors import ValidationError

    proj = Project(tmp_project)
    proj.init_solo(role_code="ME")
    with pytest.raises(ValidationError, match="decision"):
        proj.write_review(
            reviewer_role="ADMIN",
            subject_type="task",
            subject_ref="x",
            decision=bad_alias,
        )


def test_mark_human_approved_round_trip(tmp_project):
    """mark_human_approved 完整闭环：写入 needs_human REVIEW 然后人工批准。"""
    from fcop import HumanApprovalDecision

    proj = Project(tmp_project)
    proj.init_solo(role_code="ME")

    r = proj.write_review(
        reviewer_role="ADMIN",
        subject_type="task",
        subject_ref="some-task",
        decision="needs_human",
        rationale="escalate",
        subject_short="some-task",
    )
    assert r.decision is ReviewDecision.NEEDS_HUMAN
    assert r.human_approval is None

    updated = proj.mark_human_approved(
        r.review_id,
        approver="ADMIN",
        decision="approve",
        channel="cli",
        comment="LGTM, approved via CLI",
    )
    assert updated.decision is ReviewDecision.NEEDS_HUMAN  # 原决议保留
    assert updated.human_approval is not None
    assert updated.human_approval.approver == "ADMIN"
    assert updated.human_approval.decision is HumanApprovalDecision.APPROVE
    assert updated.human_approval.channel.value == "cli"
    assert updated.human_approval.comment == "LGTM, approved via CLI"


def test_mark_human_approved_rejects_non_needs_human_review(tmp_project):
    """mark_human_approved 应该拒绝 decision != needs_human 的 REVIEW。"""
    from fcop.errors import ValidationError

    proj = Project(tmp_project)
    proj.init_solo(role_code="ME")

    r = proj.write_review(
        reviewer_role="ADMIN",
        subject_type="task",
        subject_ref="some-task",
        decision="approved",
        subject_short="some-task",
    )
    with pytest.raises(ValidationError, match="needs_human"):
        proj.mark_human_approved(
            r.review_id,
            approver="ADMIN",
            decision="approve",
            channel="cli",
        )
