"""tests/test_fcop/test_review_no_v12_features.py —— v1.2 偷塞防御。

按 TASK-20260509-004 §决议 6。

ADR-0017 明确 v1.0 REVIEW **不能**包含：
- ``decision: needs_human`` 枚举值
- ``human_approval`` 子对象
- ``Project.mark_human_approved`` API
- admin-layer manual_file_edit 守卫

任何 PR 想满足下游需求偷塞这些（绕过 charter ADR）会被这套测试拦下。
"""

from __future__ import annotations

import pytest

from fcop import Project, ReviewDecision
from fcop.core.jsonschema_validator import load_bundled_schema


def test_review_decision_enum_has_no_needs_human():
    values = {d.value for d in ReviewDecision}
    assert "needs_human" not in values, (
        "ReviewDecision must NOT include 'needs_human' in v1.0 — "
        "it is deferred to v1.2 per ADR-0017."
    )


def test_review_decision_enum_is_exactly_four():
    values = {d.value for d in ReviewDecision}
    assert values == {"approved", "rejected", "needs_changes", "abstained"}


def test_schema_decision_enum_has_no_needs_human():
    schema = load_bundled_schema("review.schema.json")
    enum = set(schema["$defs"]["decisionEnum"]["enum"])
    assert "needs_human" not in enum
    assert enum == {"approved", "rejected", "needs_changes", "abstained"}


def test_schema_has_no_human_approval_field():
    schema = load_bundled_schema("review.schema.json")
    assert "human_approval" not in schema.get("properties", {})
    assert "human_approval" not in schema.get("required", [])


def test_project_has_no_mark_human_approved():
    """``Project.mark_human_approved`` 是 v1.2 计划方法，v1.0 不应该出现。"""
    assert not hasattr(Project, "mark_human_approved"), (
        "Project.mark_human_approved is a v1.2-deferred API; "
        "if you're adding it, that requires a fresh ADR superseding ADR-0017."
    )


def test_review_dataclass_has_no_human_approval_field():
    from fcop import Review

    field_names = {f for f in Review.__dataclass_fields__}
    assert "human_approval" not in field_names
    assert "approved_by_human" not in field_names
    assert "human_approver" not in field_names


@pytest.mark.parametrize(
    "needs_human_alias",
    ["needs_human", "NEEDS_HUMAN", "needs-human"],
)
def test_write_review_rejects_needs_human_aliases(tmp_project, needs_human_alias):
    """无论以何种大小写传 needs_human，都必须被拒。"""
    from fcop.errors import ValidationError

    proj = Project(tmp_project)
    proj.init_solo(role_code="ME")
    with pytest.raises(ValidationError, match="decision"):
        proj.write_review(
            reviewer_role="ADMIN",
            subject_type="task",
            subject_ref="x",
            decision=needs_human_alias,
        )
