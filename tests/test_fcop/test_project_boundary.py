"""tests/test_fcop/test_project_boundary.py —— Project boundary 端到端。

按 TASK-20260509-005 R2 §A6..A8。
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from fcop import (
    BoundaryViolationError,
    Project,
)
from fcop.core.boundary import (
    RULE_NO_GOVERNANCE_FISSION,
    RULE_NO_WORKER_REVIEWS_GOVERNANCE,
)


def _make_project_with_roles(tmp_project: Path, roles_meta: dict) -> Project:
    """Init solo 然后改 fcop.json 把 roles 改成 dict-form 携带 layer/can/cannot。"""
    proj = Project(tmp_project)
    proj.init_solo(role_code="ME")
    cfg_path = proj.config_path
    raw = json.loads(cfg_path.read_text(encoding="utf-8"))
    # 把 string 角色升级为 dict-form
    new_roles = []
    for code in raw["roles"]:
        entry = {"code": code, **roles_meta[code]} if code in roles_meta else code
        new_roles.append(entry)
    # 加任何在 roles_meta 但不在原 roles 的额外角色
    existing_codes = set(raw["roles"])
    for code, meta in roles_meta.items():
        if code not in existing_codes:
            raw["roles"].append(code)
            new_roles.append({"code": code, **meta})
    raw["roles"] = new_roles
    cfg_path.write_text(
        json.dumps(raw, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return Project(tmp_project)


class TestBoundaryViolations:
    def test_returns_empty_for_legal_action(self, tmp_project):
        proj = _make_project_with_roles(tmp_project, {})
        v = proj.boundary_violations("ME", "file_io")
        assert v == []

    def test_returns_warning_for_unknown_action(self, tmp_project):
        proj = _make_project_with_roles(tmp_project, {})
        v = proj.boundary_violations("ME", "fly_to_moon")
        assert len(v) == 1
        assert v[0].severity == "warning"

    def test_governance_spawn_agent_violations(self, tmp_project):
        proj = _make_project_with_roles(
            tmp_project,
            {"PM": {"layer": "governance"}},
        )
        v = proj.boundary_violations("PM", "spawn_agent")
        rules = {x.rule_id for x in v}
        assert RULE_NO_GOVERNANCE_FISSION in rules

    def test_worker_reviews_governance_violations(self, tmp_project):
        proj = _make_project_with_roles(
            tmp_project,
            {
                "DEV": {"layer": "worker"},
                "PM": {"layer": "governance"},
            },
        )
        v = proj.boundary_violations(
            "DEV", "review_decision", target_role="PM"
        )
        rules = {x.rule_id for x in v}
        assert RULE_NO_WORKER_REVIEWS_GOVERNANCE in rules


class TestAssertBoundary:
    def test_silent_on_legal(self, tmp_project):
        proj = _make_project_with_roles(tmp_project, {})
        proj.assert_boundary("ME", "file_io")  # no raise

    def test_raises_on_violation(self, tmp_project):
        proj = _make_project_with_roles(
            tmp_project,
            {
                "DEV": {"layer": "worker"},
                "PM": {"layer": "governance"},
            },
        )
        with pytest.raises(BoundaryViolationError) as exc_info:
            proj.assert_boundary(
                "DEV", "review_decision", target_role="PM"
            )
        assert any(
            v.rule_id == RULE_NO_WORKER_REVIEWS_GOVERNANCE
            for v in exc_info.value.violations
        )

    def test_warning_does_not_raise(self, tmp_project):
        """UNKNOWN_CAPABILITY 只是 warning，assert_boundary 不应 raise。"""
        proj = _make_project_with_roles(tmp_project, {})
        proj.assert_boundary("ME", "fly_to_moon")  # no raise


class TestReviewBoundaryEnforce:
    """A8：write_review 接进 boundary 强制。"""

    def test_worker_review_governance_subject_blocked(self, tmp_project):
        proj = _make_project_with_roles(
            tmp_project,
            {
                "DEV": {"layer": "worker"},
                "PM": {"layer": "governance"},
            },
        )
        # 先放一个 PM 派给 DEV 的 TASK 文件
        task_dir = proj.tasks_dir
        task_dir.mkdir(parents=True, exist_ok=True)
        task_path = task_dir / "TASK-20260601-001-PM-to-DEV.md"
        task_path.write_text(
            "---\nprotocol: fcop\nversion: 1\ntype: TASK\nsender: PM\n"
            "recipient: DEV\nsubject: x\n---\n\nbody\n",
            encoding="utf-8",
        )

        # DEV (worker) 尝试 review_decision 一个 PM-sender 的 TASK →
        # boundary 阻断
        with pytest.raises(BoundaryViolationError) as exc_info:
            proj.write_review(
                reviewer_role="DEV",
                subject_type="task",
                subject_ref=str(task_path),
                decision="approved",
            )
        assert any(
            v.rule_id == RULE_NO_WORKER_REVIEWS_GOVERNANCE
            for v in exc_info.value.violations
        )
        # 文件不应被创建
        assert not any(proj.reviews_dir.glob("REVIEW-*.md")) if proj.reviews_dir.exists() else True

    def test_governance_review_worker_subject_allowed(self, tmp_project):
        proj = _make_project_with_roles(
            tmp_project,
            {
                "DEV": {"layer": "worker"},
                "PM": {"layer": "governance"},
            },
        )
        task_dir = proj.tasks_dir
        task_dir.mkdir(parents=True, exist_ok=True)
        task_path = task_dir / "TASK-20260601-001-DEV-to-PM.md"
        task_path.write_text(
            "---\nprotocol: fcop\nversion: 1\ntype: TASK\nsender: DEV\n"
            "recipient: PM\nsubject: x\n---\n\nbody\n",
            encoding="utf-8",
        )

        r = proj.write_review(
            reviewer_role="PM",
            subject_type="task",
            subject_ref=str(task_path),
            decision="approved",
        )
        assert r.decision.value == "approved"

    def test_code_change_subject_skips_target_check(self, tmp_project):
        """code_change 不指向 envelope 文件 → target_role 推不出 →
        NO_WORKER_REVIEWS_GOVERNANCE 不触发，review 应正常写入。"""
        proj = _make_project_with_roles(
            tmp_project,
            {"DEV": {"layer": "worker"}},
        )
        r = proj.write_review(
            reviewer_role="DEV",
            subject_type="code_change",
            subject_ref="commit:abc123",
            decision="approved",
        )
        assert r.subject_type.value == "code_change"

    def test_admin_layer_in_config_blocks_lookup(self, tmp_project):
        """A3 重申：fcop.json 显式 layer='admin' 一定 raise。"""
        proj = _make_project_with_roles(
            tmp_project,
            {"BAD": {"layer": "admin"}},
        )
        with pytest.raises(BoundaryViolationError):
            proj.boundary_violations("BAD", "file_io")
