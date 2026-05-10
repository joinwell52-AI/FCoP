"""tests/test_fcop/test_project_failure.py —— TASK-006 R2 端到端测试。

覆盖 Project.report_failure / apply_recovery / recover_session
与 _emit_event_stub。
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from fcop import (
    Failure,
    FailureReceipt,
    FailureType,
    Project,
    RecoveryAction,
    RecoveryOutcome,
    ResumePayload,
    RetryPlan,
    RollbackPlan,
    SessionRecoveryAction,
    SessionRecoveryResult,
)

# ── helpers ──────────────────────────────────────────────────────────


def _init_project(tmp_path: Path) -> Project:
    project = Project(tmp_path)
    project.init(team="dev-team", lang="zh")
    return project


def _failure(
    *,
    ftype: FailureType = FailureType.TIMEOUT,
    agent: str = "ME",
    task_id: str | None = "TASK-20260509-006-ADMIN-to-ME",
    suggested: RecoveryAction | None = None,
    detected: datetime | None = None,
) -> Failure:
    return Failure(
        failure_type=ftype,
        subject_agent_code=agent,
        detected_at=detected or datetime(2026, 5, 9, 10, 0, tzinfo=timezone.utc),
        subject_task_id=task_id,
        evidence="超时；最后日志 line=42",
        suggested_recovery=suggested,
    )


# ── report_failure ───────────────────────────────────────────────────


class TestReportFailure:
    def test_returns_receipt(self, tmp_path: Path):
        project = _init_project(tmp_path)
        f = _failure()
        receipt = project.report_failure(f)
        assert isinstance(receipt, FailureReceipt)
        assert receipt.failure == f
        assert receipt.event_emitted is True
        assert receipt.accepted_at.tzinfo is not None

    def test_emits_stub_event(self, tmp_path: Path):
        project = _init_project(tmp_path)
        f = _failure()
        project.report_failure(f)
        log = project._emit_event_stub_calls
        assert log == [("FAILURE_DETECTED", f)]

    def test_multiple_failures_appended(self, tmp_path: Path):
        project = _init_project(tmp_path)
        f1 = _failure(ftype=FailureType.TIMEOUT, agent="ME")
        f2 = _failure(ftype=FailureType.CRASH, agent="DEV")
        project.report_failure(f1)
        project.report_failure(f2)
        log = project._emit_event_stub_calls
        assert len(log) == 2
        assert log[0][1] == f1
        assert log[1][1] == f2

    def test_non_failure_rejected(self, tmp_path: Path):
        project = _init_project(tmp_path)
        with pytest.raises(TypeError, match="must be a Failure"):
            project.report_failure("not a failure")  # type: ignore[arg-type]


# ── apply_recovery RETRY / RESUME / ROLLBACK (read-only) ────────────


class TestApplyRecoveryReadOnly:
    def test_retry_returns_plan(self, tmp_path: Path):
        project = _init_project(tmp_path)
        f = _failure(suggested=RecoveryAction.RETRY)
        outcome = project.apply_recovery(
            f, task_path=tmp_path / "TASK-foo.md"
        )
        assert isinstance(outcome, RecoveryOutcome)
        assert isinstance(outcome.plan, RetryPlan)
        assert outcome.recovery.recovery_action == RecoveryAction.RETRY
        assert outcome.artifact_path is None

    def test_resume_returns_payload(self, tmp_path: Path):
        project = _init_project(tmp_path)
        f = _failure()
        outcome = project.apply_recovery(
            f,
            action=RecoveryAction.RESUME,
            task_path=tmp_path / "TASK-foo.md",
            last_report_path=tmp_path / "REPORT-foo.md",
        )
        assert isinstance(outcome.plan, ResumePayload)
        assert outcome.plan.last_report_path == tmp_path / "REPORT-foo.md"
        assert outcome.recovery.recovery_action == RecoveryAction.RESUME

    def test_rollback_returns_plan_executed_false(self, tmp_path: Path):
        project = _init_project(tmp_path)
        f = _failure()
        outcome = project.apply_recovery(
            f,
            action="ROLLBACK",
            rollback_target_commit="abc1234",
            rollback_affected_files=["src/foo.py"],
        )
        assert isinstance(outcome.plan, RollbackPlan)
        assert outcome.plan.executed is False
        assert outcome.plan.target_commit_hash == "abc1234"
        assert outcome.plan.affected_files == ("src/foo.py",)

    def test_action_string_lowercase_rejected(self, tmp_path: Path):
        """RecoveryAction enum values are UPPERCASE; lowercase 'retry'
        is invalid (vs SessionRecoveryAction which is lowercase).

        实际实现 _coerce_recovery_action 调 .upper()，所以小写也会被接受。
        本测试守门：未知字符串必须挂。"""
        project = _init_project(tmp_path)
        with pytest.raises(ValueError, match="unknown RecoveryAction"):
            project.apply_recovery(_failure(), action="lol_unknown")

    def test_no_action_no_suggestion_raises(self, tmp_path: Path):
        project = _init_project(tmp_path)
        f = _failure(suggested=None)  # 没建议
        with pytest.raises(ValueError, match="action= is required"):
            project.apply_recovery(f, task_path=tmp_path / "x.md")

    def test_retry_without_task_path_raises(self, tmp_path: Path):
        project = _init_project(tmp_path)
        with pytest.raises(ValueError, match="task_path"):
            project.apply_recovery(_failure(), action=RecoveryAction.RETRY)


# ── apply_recovery ABORT (writes REPORT) ────────────────────────────


class TestApplyRecoveryAbort:
    def test_abort_writes_report_with_status_aborted(self, tmp_path: Path):
        project = _init_project(tmp_path)
        # 先建一个 TASK 让 ABORT 有目标
        task = project.write_task(
            sender="ADMIN",
            recipient="ME",
            priority="P1",
            subject="待 abort 的 task",
            body="will be aborted",
        )

        f = _failure(
            ftype=FailureType.TIMEOUT,
            agent="ME",
            task_id=task.task_id,
        )

        outcome = project.apply_recovery(f, action=RecoveryAction.ABORT)
        assert outcome.recovery.recovery_action == RecoveryAction.ABORT
        assert isinstance(outcome.artifact_path, Path)
        assert outcome.artifact_path.exists()
        # 校验 REPORT 文件的 status
        text = outcome.artifact_path.read_text(encoding="utf-8")
        assert "status: aborted" in text or 'status: "aborted"' in text

    def test_abort_without_task_id_raises(self, tmp_path: Path):
        project = _init_project(tmp_path)
        f = _failure(task_id=None)
        with pytest.raises(ValueError, match="ABORT.*subject_task_id"):
            project.apply_recovery(f, action=RecoveryAction.ABORT)


# ── apply_recovery ESCALATE (writes ISSUE) ──────────────────────────


class TestApplyRecoveryEscalate:
    def test_escalate_writes_issue(self, tmp_path: Path):
        project = _init_project(tmp_path)
        f = _failure(ftype=FailureType.DEADLOCK, agent="ME")
        outcome = project.apply_recovery(
            f,
            action=RecoveryAction.ESCALATE,
            leader_recipient="ADMIN",
        )
        assert outcome.recovery.recovery_action == RecoveryAction.ESCALATE
        assert isinstance(outcome.artifact_path, Path)
        assert outcome.artifact_path.exists()
        text = outcome.artifact_path.read_text(encoding="utf-8")
        assert "DEADLOCK" in text
        assert "ME" in text

    def test_escalate_without_leader_raises(self, tmp_path: Path):
        project = _init_project(tmp_path)
        with pytest.raises(ValueError, match="ESCALATE.*leader_recipient"):
            project.apply_recovery(_failure(), action=RecoveryAction.ESCALATE)


# ── recover_session ─────────────────────────────────────────────────


class TestRecoverSession:
    def test_resume_succeeds(self, tmp_path: Path):
        project = _init_project(tmp_path)
        result = project.recover_session(
            "TASK-20260509-006-ADMIN-to-ME:ME",
            "resume",
            task_path=tmp_path / "TASK-foo.md",
        )
        assert isinstance(result, SessionRecoveryResult)
        assert result.outcome == "succeeded"
        assert result.action == SessionRecoveryAction.RESUME
        assert isinstance(result.payload, ResumePayload)

    def test_rollback_succeeds(self, tmp_path: Path):
        project = _init_project(tmp_path)
        result = project.recover_session(
            "sess-20260427-me-072",
            SessionRecoveryAction.ROLLBACK,
            rollback_target_commit="deadbeef",
            rollback_affected_files=["a.py", "b.py"],
        )
        assert result.outcome == "succeeded"
        assert isinstance(result.payload, RollbackPlan)
        assert result.payload.executed is False

    def test_abort_writes_report(self, tmp_path: Path):
        project = _init_project(tmp_path)
        # 先建 TASK
        task = project.write_task(
            sender="ADMIN",
            recipient="ME",
            priority="P1",
            subject="待 session abort",
            body="x",
        )
        result = project.recover_session(
            f"{task.task_id}:ME",
            "abort",
            ref_task=task.task_id,
            recipient="ADMIN",
        )
        assert result.outcome == "succeeded"
        assert isinstance(result.payload, Path)
        assert result.payload.exists()

    def test_invalid_session_id_returns_not_found(self, tmp_path: Path):
        project = _init_project(tmp_path)
        result = project.recover_session(
            ":bad",
            "resume",
            task_path=tmp_path / "x.md",
        )
        assert result.outcome == "session_not_found"
        assert result.payload is None
        assert result.error and "task-colon-agent" in result.error

    def test_retry_action_rejected(self, tmp_path: Path):
        """Critical invariant: RETRY 不是 session-level action（per
        TASK-006 §决议 4 + ADR-0019 §session-recovery-hook）。"""
        project = _init_project(tmp_path)
        with pytest.raises(ValueError, match="not session-level"):
            project.recover_session(
                "TASK-foo:ME",
                "retry",  # ← 应被拒
                task_path=tmp_path / "x.md",
            )

    def test_escalate_action_rejected(self, tmp_path: Path):
        """同上：ESCALATE 跨 session，不能在 recover_session 里调。"""
        project = _init_project(tmp_path)
        with pytest.raises(ValueError, match="not session-level"):
            project.recover_session(
                "TASK-foo:ME",
                "escalate",
                task_path=tmp_path / "x.md",
            )

    def test_unknown_action_rejected(self, tmp_path: Path):
        project = _init_project(tmp_path)
        with pytest.raises(ValueError, match="unknown SessionRecoveryAction"):
            project.recover_session("TASK-foo:ME", "purge")

    def test_abort_without_ref_task_raises(self, tmp_path: Path):
        project = _init_project(tmp_path)
        with pytest.raises(ValueError, match="abort action requires ref_task"):
            project.recover_session("TASK-foo:ME", "abort", recipient="ADMIN")
