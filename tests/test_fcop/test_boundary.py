"""tests/test_fcop/test_boundary.py —— ADR-0020 4 条规则的回归测试。

按 TASK-20260509-005 R1 §A2..A4。
"""

from __future__ import annotations

import pytest

from fcop import (
    AgentLayer,
    BoundaryViolation,
    BoundaryViolationError,
    Capability,
    TeamConfig,
)
from fcop.core.boundary import (
    BOUNDARY_RULES,
    CAPABILITY_VOCAB,
    LAYER_DEFAULTS,
    RULE_EXPLICIT_OVERRIDES_LAYER,
    RULE_NO_ADMIN_PROGRAMMATIC_CREATE,
    RULE_NO_GOVERNANCE_FISSION,
    RULE_NO_WORKER_REVIEWS_GOVERNANCE,
    RULE_UNKNOWN_CAPABILITY,
    lookup_capability,
    validate_action,
)
from fcop.core.jsonschema_validator import load_bundled_schema


# ── 词表 / 默认 ─────────────────────────────────────────────────────


def test_capability_vocab_aligns_with_schema():
    """A2：CAPABILITY_VOCAB 必须与 boundary.schema.json 词表完全相符。"""
    schema = load_bundled_schema("boundary.schema.json")
    schema_enum = set(schema["$defs"]["capabilityToken"]["enum"])
    assert CAPABILITY_VOCAB == schema_enum, (
        f"vocab drifted: {CAPABILITY_VOCAB ^ schema_enum}"
    )


def test_capability_vocab_is_exactly_ten():
    assert len(CAPABILITY_VOCAB) == 10


def test_boundary_rules_are_exactly_four():
    """RULE_UNKNOWN_CAPABILITY 是 advisory，不计入 4 条 normative 规则。"""
    assert len(BOUNDARY_RULES) == 4
    assert RULE_UNKNOWN_CAPABILITY not in BOUNDARY_RULES


def test_layer_defaults_align_with_adr_table():
    """A2：3 个 layer 的默认 bundle 必须与 ADR-0020 §decision 表一致。"""
    worker_can, worker_cannot = LAYER_DEFAULTS[AgentLayer.WORKER]
    assert "file_io" in worker_can
    assert "task_io" in worker_can
    assert set(worker_cannot) == {"approve_release", "escalate", "spawn_agent"}

    gov_can, gov_cannot = LAYER_DEFAULTS[AgentLayer.GOVERNANCE]
    assert set(gov_can) >= {"file_io", "task_io", "review_decision"}
    assert set(gov_cannot) == {"modify_code", "spawn_agent"}

    admin_can, admin_cannot = LAYER_DEFAULTS[AgentLayer.ADMIN]
    assert set(admin_can) >= {"file_io", "task_io", "review_decision", "escalate", "override"}
    assert admin_cannot == ()


def test_layer_default_tokens_subset_of_vocab():
    """所有 layer 默认提到的 token 都必须在 v1.0 词表内。"""
    for layer, (can, cannot) in LAYER_DEFAULTS.items():
        for token in (*can, *cannot):
            assert token in CAPABILITY_VOCAB, (
                f"layer {layer.value} mentions {token!r} which is not in vocab"
            )


# ── lookup_capability ────────────────────────────────────────────────


def _config_with_role_meta(meta: dict[str, dict]) -> TeamConfig:
    """造一个 solo TeamConfig，把 meta 塞进 ``_role_labels``。"""
    return TeamConfig(
        mode="solo",
        team="solo",
        leader="ME",
        roles=tuple(meta.keys()) or ("ME",),
        lang="zh",
        version=1,
        extra={"_role_labels": meta},
    )


class TestLookupCapability:
    def test_falls_back_to_worker_default(self):
        cfg = _config_with_role_meta({})
        cap = lookup_capability("ME", cfg)
        assert cap.layer is AgentLayer.WORKER
        assert "file_io" in cap.can
        assert "approve_release" in cap.cannot
        assert cap.is_explicit is False

    def test_explicit_layer_governance(self):
        cfg = _config_with_role_meta({"PM": {"layer": "governance"}})
        cap = lookup_capability("PM", cfg)
        assert cap.layer is AgentLayer.GOVERNANCE
        assert "review_decision" in cap.can
        assert "modify_code" in cap.cannot
        assert cap.is_explicit is True

    def test_explicit_can_extends_default(self):
        cfg = _config_with_role_meta(
            {"DEV": {"layer": "worker", "can": ["modify_code"]}}
        )
        cap = lookup_capability("DEV", cfg)
        assert "file_io" in cap.can  # default 仍在
        assert "modify_code" in cap.can  # 显式新增

    def test_explicit_cannot_extends_default(self):
        cfg = _config_with_role_meta(
            {"DEV": {"layer": "worker", "cannot": ["modify_code"]}}
        )
        cap = lookup_capability("DEV", cfg)
        assert "modify_code" in cap.cannot
        # default cannot 也在
        assert "approve_release" in cap.cannot

    def test_admin_layer_in_config_rejected(self):
        """A3 + 决议 4：fcop.json 显式 layer='admin' → 立即 raise。"""
        cfg = _config_with_role_meta({"BAD": {"layer": "admin"}})
        with pytest.raises(BoundaryViolationError) as exc_info:
            lookup_capability("BAD", cfg)
        assert exc_info.value.violations[0].rule_id == RULE_NO_ADMIN_PROGRAMMATIC_CREATE

    def test_unknown_layer_value_raises(self):
        cfg = _config_with_role_meta({"X": {"layer": "wizard"}})
        with pytest.raises(ValueError, match="unknown layer"):
            lookup_capability("X", cfg)

    def test_can_accepts_string_or_list(self):
        cfg = _config_with_role_meta({"X": {"can": "modify_code"}})
        cap = lookup_capability("X", cfg)
        assert "modify_code" in cap.can

    def test_can_dedups_when_user_repeats_default(self):
        cfg = _config_with_role_meta({"X": {"can": ["file_io", "file_io"]}})
        cap = lookup_capability("X", cfg)
        assert cap.can.count("file_io") == 1


# ── validate_action 4 规则 ─────────────────────────────────────────


def _cap(layer: AgentLayer, *, can=(), cannot=(), code="X") -> Capability:
    """Quick 构造 Capability for tests。"""
    return Capability(
        code=code,
        layer=layer,
        can=can or (),
        cannot=cannot or (),
        is_explicit=True,
    )


class TestValidateAction:
    """A4：每条规则 ≥ 2 用例（合法 + 违规）。"""

    # NO_GOVERNANCE_FISSION
    def test_governance_spawn_agent_blocked(self):
        actor = _cap(AgentLayer.GOVERNANCE, code="PM")
        v = validate_action(actor, "spawn_agent")
        rules = {x.rule_id for x in v}
        assert RULE_NO_GOVERNANCE_FISSION in rules

    def test_worker_spawn_agent_blocked_via_default_cannot(self):
        """worker.cannot 默认含 spawn_agent → 触发 EXPLICIT_OVERRIDES_LAYER。"""
        actor = _cap(AgentLayer.WORKER, cannot=("spawn_agent",), code="DEV")
        v = validate_action(actor, "spawn_agent")
        rules = {x.rule_id for x in v}
        assert RULE_EXPLICIT_OVERRIDES_LAYER in rules
        # 但不触发 NO_GOVERNANCE_FISSION（actor 是 worker 不是 governance）
        assert RULE_NO_GOVERNANCE_FISSION not in rules

    def test_admin_spawn_agent_allowed(self):
        actor = _cap(AgentLayer.ADMIN, code="ADMIN")
        v = validate_action(actor, "spawn_agent")
        # admin 没有任何 cannot，且不是 governance，spawn_agent 在词表内 → 0 violations
        assert v == []

    # NO_WORKER_REVIEWS_GOVERNANCE
    def test_worker_reviews_governance_blocked(self):
        worker = _cap(AgentLayer.WORKER, code="DEV")
        gov = _cap(AgentLayer.GOVERNANCE, code="PM")
        v = validate_action(worker, "review_decision", target=gov)
        rules = {x.rule_id for x in v}
        assert RULE_NO_WORKER_REVIEWS_GOVERNANCE in rules

    def test_worker_reviews_worker_allowed(self):
        actor = _cap(AgentLayer.WORKER, can=("review_decision",), code="QA")
        target = _cap(AgentLayer.WORKER, code="DEV")
        v = validate_action(actor, "review_decision", target=target)
        rules = {x.rule_id for x in v}
        assert RULE_NO_WORKER_REVIEWS_GOVERNANCE not in rules

    def test_governance_reviews_worker_allowed(self):
        gov = _cap(AgentLayer.GOVERNANCE, code="PM")
        worker = _cap(AgentLayer.WORKER, code="DEV")
        v = validate_action(gov, "review_decision", target=worker)
        assert v == []

    def test_governance_reviews_governance_allowed(self):
        gov1 = _cap(AgentLayer.GOVERNANCE, code="PM")
        gov2 = _cap(AgentLayer.GOVERNANCE, code="LEAD")
        v = validate_action(gov1, "review_decision", target=gov2)
        rules = {x.rule_id for x in v}
        # NO_WORKER_REVIEWS_GOVERNANCE 不应触发（actor 不是 worker）
        assert RULE_NO_WORKER_REVIEWS_GOVERNANCE not in rules

    # EXPLICIT_OVERRIDES_LAYER
    def test_explicit_cannot_blocks_action_layer_allows(self):
        actor = _cap(
            AgentLayer.GOVERNANCE,
            can=("review_decision", "approve_release"),
            cannot=("approve_release",),
            code="PM",
        )
        v = validate_action(actor, "approve_release")
        rules = {x.rule_id for x in v}
        assert RULE_EXPLICIT_OVERRIDES_LAYER in rules

    def test_explicit_cannot_takes_priority_over_can(self):
        actor = _cap(
            AgentLayer.WORKER,
            can=("modify_code",),
            cannot=("modify_code",),
            code="DEV",
        )
        v = validate_action(actor, "modify_code")
        rules = {x.rule_id for x in v}
        assert RULE_EXPLICIT_OVERRIDES_LAYER in rules

    # UNKNOWN_CAPABILITY (warning only)
    def test_unknown_action_emits_warning_not_error(self):
        actor = _cap(AgentLayer.WORKER, code="DEV")
        v = validate_action(actor, "fly_to_moon")
        assert len(v) == 1
        assert v[0].rule_id == RULE_UNKNOWN_CAPABILITY
        assert v[0].severity == "warning"

    def test_known_action_no_unknown_warning(self):
        actor = _cap(AgentLayer.WORKER, code="DEV")
        v = validate_action(actor, "file_io")
        rules = {x.rule_id for x in v}
        assert RULE_UNKNOWN_CAPABILITY not in rules


def test_violation_is_frozen_and_slotted():
    v = BoundaryViolation(
        rule_id="X",
        actor="A",
        action="b",
        target=None,
        message="m",
    )
    with pytest.raises((AttributeError, TypeError)):
        v.actor = "B"  # type: ignore[misc]
