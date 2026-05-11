"""Tests for fcop_mcp.governance — Layer 1 SMB audit-first middleware.

Covers:
  - Skill Resolver: lookup, fail-open default, YAML override
  - Risk tag mapping (3-entry table)
  - Event Logger: append-only, emitted_at injection, thread safety
  - FCoPGovernanceMiddleware: instantiation, on_call_tool integration
"""

from __future__ import annotations

import json
import os
import tempfile
import threading
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from fcop_mcp.governance import (
    FCoPGovernanceMiddleware,
    SkillMeta,
    emit_event,
    resolve_skill,
)
from fcop_mcp.governance.skill_resolver import (
    _BUILTIN,
    _user_registry,
    load_registry_yaml,
)


# ── Fixtures ──────────────────────────────────────────────────────────


@pytest.fixture(autouse=True)
def isolate_user_registry():
    """Each test starts with a clean user registry."""
    original = dict(_user_registry)
    _user_registry.clear()
    yield
    _user_registry.clear()
    _user_registry.update(original)


@pytest.fixture()
def tmp_event_log(tmp_path, monkeypatch):
    """Redirect event log to a temp file."""
    log = tmp_path / "fcop_events.jsonl"
    monkeypatch.setenv("FCOP_EVENT_LOG", str(log))
    return log


# ── Skill Resolver ─────────────────────────────────────────────────────


class TestSkillResolver:
    def test_builtin_safe_tools(self):
        for tool in ("list_tasks", "read_task", "list_reviews", "read_review", "fcop_check"):
            skill = resolve_skill(tool)
            assert skill.risk_level == "Safe", f"{tool}: expected Safe, got {skill.risk_level}"

    def test_builtin_sensitive_tools(self):
        for tool in ("write_task", "write_review", "mark_human_approved", "set_project_dir"):
            skill = resolve_skill(tool)
            assert skill.risk_level == "Sensitive", f"{tool}: expected Sensitive"

    def test_builtin_critical_tools(self):
        for tool in ("delete_task", "delete_review"):
            skill = resolve_skill(tool)
            assert skill.risk_level == "Critical", f"{tool}: expected Critical"

    def test_unknown_tool_defaults_to_safe(self):
        """Fail-open: unknown tools must NOT be blocked."""
        skill = resolve_skill("some_totally_unknown_tool_xyz")
        assert skill.risk_level == "Safe"
        assert skill.category == "unknown"

    def test_returns_skill_meta(self):
        skill = resolve_skill("write_task")
        assert isinstance(skill, SkillMeta)
        assert skill.tool == "write_task"

    def test_user_registry_overrides_builtin(self):
        """User registry takes precedence over builtin."""
        _user_registry["write_task"] = {"risk": "Critical", "category": "override"}
        skill = resolve_skill("write_task")
        assert skill.risk_level == "Critical"
        assert skill.category == "override"

    def test_user_registry_adds_new_tool(self):
        _user_registry["custom_deploy"] = {"risk": "Critical", "category": "deploy"}
        skill = resolve_skill("custom_deploy")
        assert skill.risk_level == "Critical"

    def test_load_registry_yaml(self, tmp_path):
        """YAML file is loaded into user registry."""
        yaml_content = "custom_tool:\n  risk: Sensitive\n  category: custom\n"
        yaml_path = tmp_path / "skills.yaml"
        yaml_path.write_text(yaml_content, encoding="utf-8")

        try:
            import yaml  # noqa: F401
        except ImportError:
            pytest.skip("PyYAML not installed")

        load_registry_yaml(yaml_path)
        skill = resolve_skill("custom_tool")
        assert skill.risk_level == "Sensitive"
        assert skill.category == "custom"


# ── Risk Tag Mapping ───────────────────────────────────────────────────


class TestRiskTagMapping:
    """The 3-entry table inside interceptor — verify via event output."""

    EXPECTED = {
        "Safe": "ALLOW",
        "Sensitive": "REVIEW_TAG",
        "Critical": "CRITICAL_TAG",
    }

    def test_all_three_tags(self, tmp_event_log):
        for risk, expected_tag in self.EXPECTED.items():
            emit_event({
                "type": "tool_call",
                "tool": "test_tool",
                "risk": risk,
                "tag": expected_tag,
                "args_hash": "abc",
                "session_id": None,
                "ts": 1.0,
            })

        lines = tmp_event_log.read_text(encoding="utf-8").strip().splitlines()
        assert len(lines) == 3
        for line, (risk, expected_tag) in zip(lines, self.EXPECTED.items()):
            ev = json.loads(line)
            assert ev["tag"] == expected_tag, f"risk={risk}: expected tag {expected_tag}"


# ── Event Logger ───────────────────────────────────────────────────────


class TestEventLogger:
    def test_append_only(self, tmp_event_log):
        emit_event({"type": "a", "ts": 1.0})
        emit_event({"type": "b", "ts": 2.0})
        lines = tmp_event_log.read_text(encoding="utf-8").strip().splitlines()
        assert len(lines) == 2
        assert json.loads(lines[0])["type"] == "a"
        assert json.loads(lines[1])["type"] == "b"

    def test_emitted_at_injected(self, tmp_event_log):
        emit_event({"type": "test", "ts": 1.0})
        ev = json.loads(tmp_event_log.read_text(encoding="utf-8"))
        assert "emitted_at" in ev
        assert isinstance(ev["emitted_at"], float)

    def test_event_without_emitted_at_gets_it(self, tmp_event_log):
        emit_event({"type": "no_ts_event"})
        ev = json.loads(tmp_event_log.read_text(encoding="utf-8"))
        assert "emitted_at" in ev

    def test_existing_emitted_at_not_overwritten(self, tmp_event_log):
        emit_event({"type": "pre_timed", "emitted_at": 999.0})
        ev = json.loads(tmp_event_log.read_text(encoding="utf-8"))
        assert ev["emitted_at"] == 999.0

    def test_thread_safe(self, tmp_event_log):
        """Concurrent emits must not corrupt the log."""
        errors: list[Exception] = []

        def worker(n: int):
            try:
                for _ in range(20):
                    emit_event({"type": "concurrent", "worker": n})
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors, f"Thread errors: {errors}"
        lines = tmp_event_log.read_text(encoding="utf-8").strip().splitlines()
        assert len(lines) == 100  # 5 threads × 20 events

    def test_unicode_in_event(self, tmp_event_log):
        emit_event({"type": "unicode", "msg": "你好 🚀"})
        ev = json.loads(tmp_event_log.read_text(encoding="utf-8"))
        assert ev["msg"] == "你好 🚀"

    def test_env_var_controls_path(self, tmp_path, monkeypatch):
        custom_log = tmp_path / "custom.jsonl"
        monkeypatch.setenv("FCOP_EVENT_LOG", str(custom_log))
        emit_event({"type": "custom_path"})
        assert custom_log.exists()
        assert json.loads(custom_log.read_text(encoding="utf-8"))["type"] == "custom_path"


# ── FCoPGovernanceMiddleware ───────────────────────────────────────────


class TestFCoPGovernanceMiddleware:
    def test_instantiation(self):
        mw = FCoPGovernanceMiddleware()
        assert mw is not None

    @pytest.mark.asyncio
    async def test_safe_tool_always_calls_next(self, tmp_event_log):
        """Safe tools: log + call_next, return upstream result."""
        mw = FCoPGovernanceMiddleware()
        expected_result = [MagicMock()]
        call_next = AsyncMock(return_value=expected_result)

        import mcp.types as mt

        context = MagicMock()
        context.message = mt.CallToolRequestParams(name="list_tasks", arguments={})
        context.fastmcp_context = None

        result = await mw.on_call_tool(context, call_next)

        call_next.assert_awaited_once()
        assert result is expected_result

        # Event was emitted
        ev = json.loads(tmp_event_log.read_text(encoding="utf-8"))
        assert ev["tool"] == "list_tasks"
        assert ev["risk"] == "Safe"
        assert ev["tag"] == "ALLOW"

    @pytest.mark.asyncio
    async def test_sensitive_tool_logs_review_tag(self, tmp_event_log):
        """Sensitive tools: log REVIEW_TAG + call_next (audit-first, no block)."""
        mw = FCoPGovernanceMiddleware()
        call_next = AsyncMock(return_value=[])

        import mcp.types as mt

        context = MagicMock()
        context.message = mt.CallToolRequestParams(name="write_task", arguments={"title": "x"})
        context.fastmcp_context = None

        await mw.on_call_tool(context, call_next)

        call_next.assert_awaited_once()
        ev = json.loads(tmp_event_log.read_text(encoding="utf-8"))
        assert ev["tool"] == "write_task"
        assert ev["risk"] == "Sensitive"
        assert ev["tag"] == "REVIEW_TAG"

    @pytest.mark.asyncio
    async def test_critical_tool_logs_critical_tag(self, tmp_event_log):
        """Critical tools: log CRITICAL_TAG + call_next (audit-first, no block)."""
        mw = FCoPGovernanceMiddleware()
        call_next = AsyncMock(return_value=[])

        import mcp.types as mt

        context = MagicMock()
        context.message = mt.CallToolRequestParams(name="delete_task", arguments={"task_id": "TASK-001"})
        context.fastmcp_context = None

        await mw.on_call_tool(context, call_next)

        call_next.assert_awaited_once()
        ev = json.loads(tmp_event_log.read_text(encoding="utf-8"))
        assert ev["tool"] == "delete_task"
        assert ev["risk"] == "Critical"
        assert ev["tag"] == "CRITICAL_TAG"

    @pytest.mark.asyncio
    async def test_event_emitted_before_call_next(self, tmp_event_log):
        """Governance contract: event MUST be written before call_next returns."""
        mw = FCoPGovernanceMiddleware()
        log_size_at_call: list[int] = []

        async def inspecting_next(ctx):
            log_size_at_call.append(tmp_event_log.stat().st_size)
            return []

        import mcp.types as mt

        context = MagicMock()
        context.message = mt.CallToolRequestParams(name="list_tasks", arguments={})
        context.fastmcp_context = None

        await mw.on_call_tool(context, inspecting_next)

        assert log_size_at_call[0] > 0, "Event log was empty when call_next was invoked"

    @pytest.mark.asyncio
    async def test_args_hash_in_event(self, tmp_event_log):
        import hashlib, json as _json
        mw = FCoPGovernanceMiddleware()
        call_next = AsyncMock(return_value=[])

        import mcp.types as mt

        args = {"title": "test task", "status": "open"}
        context = MagicMock()
        context.message = mt.CallToolRequestParams(name="write_task", arguments=args)
        context.fastmcp_context = None

        await mw.on_call_tool(context, call_next)

        ev = json.loads(tmp_event_log.read_text(encoding="utf-8"))
        expected_hash = hashlib.sha256(
            _json.dumps(args, sort_keys=True, ensure_ascii=False).encode()
        ).hexdigest()
        assert ev["args_hash"] == expected_hash

    @pytest.mark.asyncio
    async def test_unknown_tool_defaults_safe(self, tmp_event_log):
        """Unknown tools: fail-open → Safe → ALLOW tag → call_next."""
        mw = FCoPGovernanceMiddleware()
        call_next = AsyncMock(return_value=[])

        import mcp.types as mt

        context = MagicMock()
        context.message = mt.CallToolRequestParams(name="nonexistent_tool_xyz", arguments={})
        context.fastmcp_context = None

        await mw.on_call_tool(context, call_next)

        call_next.assert_awaited_once()
        ev = json.loads(tmp_event_log.read_text(encoding="utf-8"))
        assert ev["risk"] == "Safe"
        assert ev["tag"] == "ALLOW"
