"""tests/test_fcop/test_project_events.py —— TASK-007 R2 端到端测试。

覆盖 Project.subscribe_events / poll_once / _emit_event +
TASK-005 BOUNDARY_VIOLATED + TASK-006 stub-replacement 集成。
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from fcop import (
    Event,
    EventSubscription,
    EventType,
    Failure,
    FailureType,
    Project,
    RecoveryAction,
)
from fcop.errors import BoundaryViolationError


# ── helpers ──────────────────────────────────────────────────────────


def _init_project(tmp_path: Path) -> Project:
    p = Project(tmp_path)
    p.init(team="dev-team", lang="zh")
    return p


def _failure(
    *,
    ftype: FailureType = FailureType.TIMEOUT,
    agent: str = "ME",
    task_id: str | None = "TASK-20260509-007-ADMIN-to-ME",
) -> Failure:
    return Failure(
        failure_type=ftype,
        subject_agent_code=agent,
        detected_at=datetime(2026, 5, 9, 10, 0, tzinfo=timezone.utc),
        subject_task_id=task_id,
        evidence="超时；最后日志 line=42",
    )


# ── subscribe_events ────────────────────────────────────────────────


class TestSubscribeEvents:
    def test_subscribe_returns_subscription(self, tmp_path: Path):
        project = _init_project(tmp_path)
        sub = project.subscribe_events(callback=lambda e: None)
        assert isinstance(sub, EventSubscription)
        assert sub.active is True

    def test_subscribe_with_no_types_means_all(self, tmp_path: Path):
        project = _init_project(tmp_path)
        sub = project.subscribe_events(callback=lambda e: None)
        assert sub.types is None

    def test_subscribe_normalizes_string_types(self, tmp_path: Path):
        project = _init_project(tmp_path)
        sub = project.subscribe_events(
            types=["TASK_CREATED", "REPORT_FILED"],
            callback=lambda e: None,
        )
        assert sub.types == (EventType.TASK_CREATED, EventType.REPORT_FILED)

    def test_subscribe_unknown_type_rejected(self, tmp_path: Path):
        project = _init_project(tmp_path)
        with pytest.raises(ValueError, match="unknown EventType"):
            project.subscribe_events(types=["NOT_A_REAL_EVENT"])

    def test_unsubscribe_idempotent(self, tmp_path: Path):
        project = _init_project(tmp_path)
        sub = project.subscribe_events(callback=lambda e: None)
        sub.unsubscribe()
        sub.unsubscribe()  # 再调一次不抛错
        assert sub.active is False

    def test_callback_receives_events(self, tmp_path: Path):
        project = _init_project(tmp_path)
        received: list[Event] = []
        project.subscribe_events(callback=received.append)
        # 触发一个 in-process 同步事件（FAILURE_DETECTED）
        project.report_failure(_failure())
        assert len(received) == 1
        assert received[0].event_type == EventType.FAILURE_DETECTED

    def test_type_filter_excludes_other_events(self, tmp_path: Path):
        project = _init_project(tmp_path)
        received: list[Event] = []
        project.subscribe_events(
            types=[EventType.RECOVERY_INITIATED],
            callback=received.append,
        )
        project.report_failure(_failure())  # 发 FAILURE_DETECTED，应被过滤
        assert received == []

    def test_unsubscribe_stops_callback(self, tmp_path: Path):
        project = _init_project(tmp_path)
        received: list[Event] = []
        sub = project.subscribe_events(callback=received.append)
        project.report_failure(_failure())
        sub.unsubscribe()
        project.report_failure(_failure(agent="DEV"))
        assert len(received) == 1


# ── poll_once：文件类事件派生 ────────────────────────────────────────


class TestPollOnce:
    def test_first_poll_emits_no_events_when_empty(self, tmp_path: Path):
        project = _init_project(tmp_path)
        events = project.poll_once()
        # init 写了 fcop.json + workspace 结构；首次 poll 视为基线
        # 事件来自当前已存在文件（task/report/review 都没；ROLE 只在
        # 变化时才 emit），所以应是空
        assert events == []

    def test_poll_emits_task_created_after_write(self, tmp_path: Path):
        project = _init_project(tmp_path)
        project.poll_once()  # 基线
        project.write_task(
            sender="ADMIN",
            recipient="ME",
            priority="P1",
            subject="smoke",
            body="x",
        )
        events = project.poll_once()
        types = [e.event_type for e in events]
        assert EventType.TASK_CREATED in types

    def test_poll_emits_report_filed(self, tmp_path: Path):
        project = _init_project(tmp_path)
        task = project.write_task(
            sender="ADMIN",
            recipient="ME",
            priority="P1",
            subject="x",
            body="x",
        )
        project.poll_once()  # 基线含 task
        project.write_report(
            task_id=task.task_id,
            reporter="ME",
            recipient="ADMIN",
            body="ok",
            status="done",
        )
        events = project.poll_once()
        types = [e.event_type for e in events]
        assert EventType.REPORT_FILED in types

    def test_poll_dedup_across_runs(self, tmp_path: Path):
        project = _init_project(tmp_path)
        project.write_task(
            sender="ADMIN", recipient="ME", priority="P1",
            subject="x", body="x",
        )
        first = project.poll_once()
        second = project.poll_once()
        assert any(e.event_type == EventType.TASK_CREATED for e in first)
        assert second == []

    def test_poll_callback_invoked_in_order(self, tmp_path: Path):
        project = _init_project(tmp_path)
        received: list[EventType] = []
        project.subscribe_events(callback=lambda e: received.append(e.event_type))
        project.write_task(
            sender="ADMIN", recipient="ME", priority="P1",
            subject="x", body="x",
        )
        events = project.poll_once()
        assert [e.event_type for e in events] == received


# ── BOUNDARY_VIOLATED 集成（接 TASK-005）────────────────────────────


class TestBoundaryEventIntegration:
    def test_boundary_violation_emits_event(self, tmp_path: Path):
        project = _init_project(tmp_path)
        received: list[Event] = []
        project.subscribe_events(
            types=[EventType.BOUNDARY_VIOLATED],
            callback=received.append,
        )
        # 触发 governance 试图 spawn agent —— 违规
        with pytest.raises(BoundaryViolationError):
            project.assert_boundary("LEADER", "spawn_agent")
        # 注意：默认 layer 配置下 LEADER 是 governance，spawn_agent
        # 不在 governance 默认 can 列表 → 会触发 NO_GOVERNANCE_FISSION
        # 或缺权违规
        assert len(received) >= 1
        ev = received[0]
        assert ev.event_type == EventType.BOUNDARY_VIOLATED
        assert ev.subject.get("actor") == "LEADER"
        assert ev.subject.get("attempted_action") == "spawn_agent"


# ── FAILURE / RECOVERY 事件集成（接 TASK-006）──────────────────────


class TestFailureRecoveryEvents:
    def test_report_failure_emits_failure_detected(self, tmp_path: Path):
        project = _init_project(tmp_path)
        received: list[Event] = []
        project.subscribe_events(callback=received.append)
        project.report_failure(_failure())
        types = [e.event_type for e in received]
        assert EventType.FAILURE_DETECTED in types

    def test_apply_recovery_emits_initiated_then_completed(self, tmp_path: Path):
        project = _init_project(tmp_path)
        received: list[Event] = []
        project.subscribe_events(callback=received.append)
        f = _failure()
        project.apply_recovery(
            f,
            action=RecoveryAction.RETRY,
            task_path=tmp_path / "TASK-x.md",
        )
        types = [e.event_type for e in received]
        assert EventType.RECOVERY_INITIATED in types
        assert EventType.RECOVERY_COMPLETED in types
        # 顺序：INITIATED 先于 COMPLETED
        idx_init = types.index(EventType.RECOVERY_INITIATED)
        idx_done = types.index(EventType.RECOVERY_COMPLETED)
        assert idx_init < idx_done

    def test_failure_event_subject_has_failure_type(self, tmp_path: Path):
        project = _init_project(tmp_path)
        received: list[Event] = []
        project.subscribe_events(
            types=[EventType.FAILURE_DETECTED], callback=received.append
        )
        project.report_failure(_failure(ftype=FailureType.DEADLOCK))
        assert len(received) == 1
        assert received[0].subject.get("failure_type") == "DEADLOCK"
        assert received[0].subject.get("actor") == "ME"


# ── SESSION_LOST 集成 ──────────────────────────────────────────────


class TestSessionLostEvent:
    def test_invalid_session_id_emits_session_lost(self, tmp_path: Path):
        project = _init_project(tmp_path)
        received: list[Event] = []
        project.subscribe_events(
            types=[EventType.SESSION_LOST], callback=received.append
        )
        result = project.recover_session(":bad", "resume", task_path=tmp_path / "x.md")
        assert result.outcome == "session_not_found"
        assert len(received) == 1
        assert received[0].subject.get("session_id") == ":bad"


# ── ROLE_SWITCHED 集成 ──────────────────────────────────────────────


class TestRoleSwitchEvent:
    def test_fcop_json_change_emits_role_switched(self, tmp_path: Path):
        import json

        project = _init_project(tmp_path)
        project.poll_once()  # 基线
        # 改 fcop.json（实际位置 = Project.config_path）
        config = project.config_path
        data = json.loads(config.read_text(encoding="utf-8"))
        data["leader"] = "NEWLEADER"
        data["roles"] = list(data.get("roles", [])) + ["NEWLEADER"]
        config.write_text(json.dumps(data), encoding="utf-8")
        events = project.poll_once()
        types = [e.event_type for e in events]
        assert EventType.ROLE_SWITCHED in types


# ── 兼容性：TASK-006 既有测试不破坏 ────────────────────────────────


class TestBackCompatWithStub:
    def test_emit_event_stub_calls_still_populated(self, tmp_path: Path):
        """TASK-006 测试通过 _emit_event_stub_calls 观察 stub；本任务
        替换 stub 实现为真实 emitter，但 _emit_event_stub_calls 仍是
        每次调用的 (type_str, subject) 元组列表（向后兼容契约）。"""
        project = _init_project(tmp_path)
        f = _failure()
        project.report_failure(f)
        log = project._emit_event_stub_calls
        assert len(log) == 1
        assert log[0] == ("FAILURE_DETECTED", f)
