"""tests/test_fcop/test_core_recovery.py —— TASK-006 R1 测试 ≥ 12 用例。

覆盖：
- parse_session_id 两种形状 + 错误形状
- make_retry_plan / make_resume_payload / make_rollback_plan 行为 + 边界
- make_abort_artifact / make_escalate_artifact 通过 fake callback 验证
- build_recovery_record 工厂

不依赖 :class:`fcop.Project` —— 验证 ADR-0019 §design-details 第 5 点
"core/recovery.py 是 reference impl，可被 host adapter 直接复用"。
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from fcop import (
    Failure,
    FailureType,
    Recovery,
    RecoveryAction,
    ResumePayload,
    RetryPlan,
    RollbackPlan,
)
from fcop.core.recovery import (
    ParsedSessionId,
    build_recovery_record,
    make_abort_artifact,
    make_escalate_artifact,
    make_resume_payload,
    make_retry_plan,
    make_rollback_plan,
    parse_session_id,
)


# ── helpers ──────────────────────────────────────────────────────────


def _failure(
    *,
    ftype: FailureType = FailureType.TIMEOUT,
    agent: str = "ME",
    task_id: str | None = "TASK-20260509-006-ADMIN-to-ME",
    suggested: RecoveryAction | None = None,
) -> Failure:
    return Failure(
        failure_type=ftype,
        subject_agent_code=agent,
        detected_at=datetime(2026, 5, 9, 10, 0, 0, tzinfo=timezone.utc),
        subject_task_id=task_id,
        evidence="超过 timeout_at；最后日志 line=42",
        suggested_recovery=suggested,
    )


# ── parse_session_id ─────────────────────────────────────────────────


class TestParseSessionId:
    def test_task_colon_agent_form(self):
        result = parse_session_id("TASK-20260509-006-ADMIN-to-ME:ME")
        assert isinstance(result, ParsedSessionId)
        assert result.scheme == "task_colon_agent"
        assert result.task_id == "TASK-20260509-006-ADMIN-to-ME"
        assert result.agent_code == "ME"
        assert result.raw == "TASK-20260509-006-ADMIN-to-ME:ME"

    def test_sess_dated_form(self):
        result = parse_session_id("sess-20260427-me-072")
        assert result.scheme == "sess_dated"
        assert result.task_id is None
        assert result.agent_code == "ME"  # uppercased

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="非空字符串"):
            parse_session_id("")

    def test_non_string_raises(self):
        with pytest.raises(ValueError, match="非空字符串"):
            parse_session_id(None)  # type: ignore[arg-type]

    def test_bare_agent_no_prefix_raises(self):
        with pytest.raises(ValueError, match="既不匹配"):
            parse_session_id("just-some-string")

    def test_colon_with_empty_left_raises(self):
        with pytest.raises(ValueError, match="task-colon-agent"):
            parse_session_id(":ME")

    def test_colon_with_empty_right_raises(self):
        with pytest.raises(ValueError, match="task-colon-agent"):
            parse_session_id("TASK-foo:")


# ── make_retry_plan ──────────────────────────────────────────────────


class TestMakeRetryPlan:
    def test_default(self, tmp_path: Path):
        f = _failure(suggested=RecoveryAction.RETRY)
        task = tmp_path / "TASK-foo.md"
        plan = make_retry_plan(f, task_path=task)
        assert isinstance(plan, RetryPlan)
        assert plan.task_path == task
        assert plan.suggested_delay_seconds == 0
        assert plan.attempt_count == 1

    def test_with_backoff(self, tmp_path: Path):
        f = _failure()
        plan = make_retry_plan(
            f,
            task_path=tmp_path / "x.md",
            suggested_delay_seconds=30,
            attempt_count=3,
        )
        assert plan.suggested_delay_seconds == 30
        assert plan.attempt_count == 3

    def test_attempt_count_zero_rejected(self, tmp_path: Path):
        with pytest.raises(ValueError, match="attempt_count 必须 >= 1"):
            make_retry_plan(_failure(), task_path=tmp_path / "x.md", attempt_count=0)

    def test_negative_delay_rejected(self, tmp_path: Path):
        with pytest.raises(ValueError, match="suggested_delay_seconds"):
            make_retry_plan(
                _failure(),
                task_path=tmp_path / "x.md",
                suggested_delay_seconds=-1,
            )


# ── make_resume_payload ──────────────────────────────────────────────


class TestMakeResumePayload:
    def test_with_last_report(self, tmp_path: Path):
        task = tmp_path / "TASK-foo.md"
        report = tmp_path / "REPORT-foo.md"
        payload = make_resume_payload(
            session_id="TASK-20260509-006-ADMIN-to-ME:ME",
            task_path=task,
            last_report_path=report,
        )
        assert isinstance(payload, ResumePayload)
        assert payload.task_path == task
        assert payload.last_report_path == report
        assert payload.session_id == "TASK-20260509-006-ADMIN-to-ME:ME"
        assert payload.metadata["agent_code"] == "ME"
        assert payload.metadata["scheme"] == "task_colon_agent"

    def test_without_last_report(self, tmp_path: Path):
        payload = make_resume_payload(
            session_id="sess-20260427-me-072",
            task_path=tmp_path / "x.md",
            last_report_path=None,
        )
        assert payload.last_report_path is None
        assert payload.metadata["scheme"] == "sess_dated"
        assert payload.metadata["task_id"] is None

    def test_extra_metadata_merged(self, tmp_path: Path):
        payload = make_resume_payload(
            session_id="TASK-foo:ME",
            task_path=tmp_path / "x.md",
            last_report_path=None,
            extra_metadata={"custom": "value", "scheme": "OVERRIDDEN"},
        )
        assert payload.metadata["custom"] == "value"
        assert payload.metadata["scheme"] == "OVERRIDDEN"


# ── make_rollback_plan ──────────────────────────────────────────────


class TestMakeRollbackPlan:
    def test_with_commit(self):
        plan = make_rollback_plan(
            target_commit_hash="abc1234",
            affected_files=["src/foo.py", "tests/test_foo.py"],
        )
        assert isinstance(plan, RollbackPlan)
        assert plan.target_commit_hash == "abc1234"
        assert plan.affected_files == ("src/foo.py", "tests/test_foo.py")
        assert plan.executed is False

    def test_no_commit_found(self):
        plan = make_rollback_plan(
            target_commit_hash=None,
            affected_files=(),
        )
        assert plan.target_commit_hash is None
        assert plan.affected_files == ()
        assert plan.executed is False

    def test_executed_always_false_v1_0(self):
        """关键 invariant：v1.0 ROLLBACK plan.executed 永远 False（per
        TASK-006 §决议 3）。如果未来某 commit 把 executed 默认改成 True，
        本测试会立刻挂——这是设计意图。"""
        plan = make_rollback_plan(
            target_commit_hash="ffffffff",
            affected_files=["a.py"],
        )
        assert plan.executed is False, (
            "v1.0 ROLLBACK 必须是 plan-only；要改成实际执行需先发新 ADR"
        )


# ── make_abort_artifact ──────────────────────────────────────────────


class TestMakeAbortArtifact:
    def test_writes_via_callback(self, tmp_path: Path):
        captured = {}
        fake_path = tmp_path / "REPORT-aborted.md"

        def fake_write_report(**kwargs):
            captured.update(kwargs)

            class _R:
                path = fake_path

            return _R()

        f = _failure()
        result = make_abort_artifact(
            f,
            write_report_fn=fake_write_report,
            ref_task="fcop/tasks/TASK-foo.md",
            sender="ME",
            recipient="ADMIN",
        )
        assert result == fake_path
        assert captured["sender"] == "ME"
        assert captured["recipient"] == "ADMIN"
        assert captured["status"] == "aborted"
        assert captured["ref_task"] == "fcop/tasks/TASK-foo.md"
        assert "TIMEOUT" in captured["body"]
        assert "ME" in captured["body"]
        assert "Evidence" in captured["body"]

    def test_custom_body(self, tmp_path: Path):
        captured = {}

        def fake_write_report(**kwargs):
            captured.update(kwargs)

            class _R:
                path = tmp_path / "x.md"

            return _R()

        make_abort_artifact(
            _failure(),
            write_report_fn=fake_write_report,
            ref_task="x.md",
            sender="ME",
            recipient="ADMIN",
            body="自定义 body 内容",
        )
        assert captured["body"] == "自定义 body 内容"

    def test_callback_returning_no_path_rejected(self, tmp_path: Path):
        def bad_write_report(**kwargs):
            return object()  # no .path attribute

        with pytest.raises(TypeError, match="必须返回带 .path"):
            make_abort_artifact(
                _failure(),
                write_report_fn=bad_write_report,
                ref_task="x.md",
                sender="ME",
                recipient="ADMIN",
            )


# ── make_escalate_artifact ──────────────────────────────────────────


class TestMakeEscalateArtifact:
    def test_writes_via_callback(self, tmp_path: Path):
        captured = {}
        fake_path = tmp_path / "ISSUE-escalation.md"

        def fake_write_issue(**kwargs):
            captured.update(kwargs)

            class _I:
                path = fake_path

            return _I()

        f = _failure(ftype=FailureType.DEADLOCK)
        result = make_escalate_artifact(
            f,
            write_issue_fn=fake_write_issue,
            sender="ME",
            leader_recipient="LEADER",
        )
        assert result == fake_path
        assert captured["sender"] == "ME"
        assert captured["recipient"] == "LEADER"
        assert captured["severity"] == "high"
        assert "Escalation: DEADLOCK on ME" == captured["title"]
        assert "DEADLOCK" in captured["body"]
        assert "Evidence" in captured["body"]

    def test_custom_title_and_severity(self, tmp_path: Path):
        captured = {}

        def fake_write_issue(**kwargs):
            captured.update(kwargs)

            class _I:
                path = tmp_path / "x.md"

            return _I()

        make_escalate_artifact(
            _failure(),
            write_issue_fn=fake_write_issue,
            sender="ME",
            leader_recipient="LEADER",
            title="自定义标题",
            severity="critical",
        )
        assert captured["title"] == "自定义标题"
        assert captured["severity"] == "critical"


# ── build_recovery_record ───────────────────────────────────────────


class TestBuildRecoveryRecord:
    def test_default_outcome(self):
        f = _failure()
        rec = build_recovery_record(f, RecoveryAction.RETRY)
        assert isinstance(rec, Recovery)
        assert rec.recovery_action == RecoveryAction.RETRY
        assert rec.trigger_failure == f
        assert rec.outcome == "in_progress"
        assert rec.initiated_at.tzinfo is not None

    def test_custom_outcome_and_time(self):
        f = _failure()
        ts = datetime(2026, 1, 1, tzinfo=timezone.utc)
        rec = build_recovery_record(
            f,
            RecoveryAction.ABORT,
            initiated_at=ts,
            outcome="succeeded",
        )
        assert rec.initiated_at == ts
        assert rec.outcome == "succeeded"
