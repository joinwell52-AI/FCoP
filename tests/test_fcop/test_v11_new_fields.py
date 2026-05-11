"""tests/test_fcop/test_v11_new_fields.py — v1.1 新字段冒烟测试。

覆盖 ADR-0024（Task.risk_level）、ADR-0027（Skill/SkillTool）
以及相关 schema/model 的基本验证。
"""

from __future__ import annotations

import pytest

from fcop import Project, RiskLevel, Skill, SkillTool
from fcop.core.jsonschema_validator import load_bundled_schema
from fcop.core.schema import normalize_risk_level
from fcop.models import TaskFrontmatter

# ── RiskLevel enum ──────────────────────────────────────────────────


def test_risk_level_enum_values():
    values = {r.value for r in RiskLevel}
    assert values == {"low", "medium", "high", "irreversible"}


def test_normalize_risk_level_none_gives_medium():
    assert normalize_risk_level(None) is RiskLevel.MEDIUM


def test_normalize_risk_level_string():
    assert normalize_risk_level("low") is RiskLevel.LOW
    assert normalize_risk_level("high") is RiskLevel.HIGH
    assert normalize_risk_level("irreversible") is RiskLevel.IRREVERSIBLE


def test_normalize_risk_level_enum_passthrough():
    assert normalize_risk_level(RiskLevel.HIGH) is RiskLevel.HIGH


def test_normalize_risk_level_bad_value():
    with pytest.raises(ValueError, match="risk_level"):
        normalize_risk_level("extreme")


# ── TaskFrontmatter.risk_level ──────────────────────────────────────


def test_task_frontmatter_default_risk_level():
    fm = TaskFrontmatter(
        protocol="fcop", version=1, sender="PM", recipient="DEV",
        priority="P2",  # type: ignore[arg-type]
    )
    assert fm.risk_level is RiskLevel.MEDIUM


def test_task_frontmatter_explicit_risk_level():
    fm = TaskFrontmatter(
        protocol="fcop", version=1, sender="PM", recipient="DEV",
        priority="P0",  # type: ignore[arg-type]
        risk_level=RiskLevel.HIGH,
    )
    assert fm.risk_level is RiskLevel.HIGH


# ── write_task risk_level parameter ────────────────────────────────


def test_write_task_default_risk_level(tmp_project):
    proj = Project(tmp_project)
    proj.init_solo(role_code="ME")
    task = proj.write_task(
        sender="ME", recipient="ME",
        priority="P2", subject="test task", body="body",
    )
    assert task.frontmatter.risk_level is RiskLevel.MEDIUM


def test_write_task_explicit_risk_level(tmp_project):
    proj = Project(tmp_project)
    proj.init_solo(role_code="ME")
    task = proj.write_task(
        sender="ME", recipient="ME",
        priority="P1", subject="high risk task", body="body",
        risk_level="high",
    )
    assert task.frontmatter.risk_level is RiskLevel.HIGH


def test_write_task_irreversible(tmp_project):
    proj = Project(tmp_project)
    proj.init_solo(role_code="ME")
    task = proj.write_task(
        sender="ME", recipient="ME",
        priority="P0", subject="drop table", body="body",
        risk_level=RiskLevel.IRREVERSIBLE,
    )
    assert task.frontmatter.risk_level is RiskLevel.IRREVERSIBLE


# ── ipc-envelope schema risk_level ─────────────────────────────────


def test_ipc_envelope_schema_has_risk_level():
    schema = load_bundled_schema("ipc-envelope.schema.json")
    task_def = schema["$defs"]["task"]
    assert "risk_level" in task_def["properties"], (
        "ipc-envelope.schema.json task def must have risk_level property (ADR-0024)."
    )
    enum = task_def["properties"]["risk_level"]["enum"]
    assert set(enum) == {"low", "medium", "high", "irreversible"}


# ── Skill / SkillTool dataclasses ──────────────────────────────────


def test_skill_tool_defaults():
    t = SkillTool(name="git.status")
    assert t.risk_level is RiskLevel.LOW
    assert t.irreversible is False
    assert t.cost_sensitive is False
    assert t.description is None


def test_skill_tool_custom():
    t = SkillTool(
        name="db.exec",
        risk_level=RiskLevel.IRREVERSIBLE,
        irreversible=True,
        cost_sensitive=False,
        description="Execute raw SQL",
    )
    assert t.risk_level is RiskLevel.IRREVERSIBLE
    assert t.irreversible is True


def test_skill_defaults():
    s = Skill(id="git-tools")
    assert s.label is None
    assert s.uri is None
    assert s.tools == ()


def test_skill_with_tools():
    tools = (
        SkillTool(name="git.status", risk_level=RiskLevel.LOW),
        SkillTool(name="git.push_force", risk_level=RiskLevel.HIGH, irreversible=True),
    )
    s = Skill(
        id="git-tools",
        label="Git Operations",
        uri="mcp://local/git",
        tools=tools,
    )
    assert len(s.tools) == 2
    assert s.tools[1].name == "git.push_force"
    assert s.tools[1].irreversible is True


# ── skill.schema.json ───────────────────────────────────────────────


def test_skill_schema_exists():
    schema = load_bundled_schema("skill.schema.json")
    assert schema["title"] == "FCoP Skill"
    assert "tools" in schema["properties"]
    assert "skillTool" in schema["$defs"]


def test_skill_schema_tool_risk_level_enum():
    schema = load_bundled_schema("skill.schema.json")
    tool_def = schema["$defs"]["skillTool"]
    # risk_level is a $ref → riskLevel; verify the riskLevel def exists
    assert "$ref" in tool_def["properties"]["risk_level"]
    assert "riskLevel" in schema["$defs"]
    assert set(schema["$defs"]["riskLevel"]["enum"]) == {"low", "medium", "high", "irreversible"}
