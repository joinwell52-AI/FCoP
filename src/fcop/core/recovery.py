"""Recovery primitives — reference impl of 5 类 RecoveryAction.

Per ADR-0019 §design-details + TASK-006 §决议 3：v1.0 把 5 类 Recovery
落到 reference-impl 函数。这些函数都**纯**——不依赖 :class:`Project`
facade，只接 plain Path / TeamConfig / 字符串入参，便于在
:meth:`fcop.Project.apply_recovery` 之外被 host adapter 直接复用。

5 类的实现策略（per TASK-006 §决议 3）：

================  ============================================================
RetryAction       v1.0 行为
================  ============================================================
``RETRY``         返回 :class:`RetryPlan`（task_path + delay + attempt_count）
``RESUME``        返回 :class:`ResumePayload`（task + last_report + metadata）
``ROLLBACK``      返回 :class:`RollbackPlan`（commit_hash + files），**不**跑 git
``ABORT``         调 caller 提供的 ``write_report_fn`` 写一份 status: aborted
``ESCALATE``      调 caller 提供的 ``write_issue_fn`` 写一份 ISSUE 给 leader
================  ============================================================

ABORT / ESCALATE 不直接 import :class:`fcop.Project` 是为了避免循环依赖
——project.py 通过 partial 包好 write_report / write_issue 再传进来。

DRIFT 自动检测、git revert 实际执行、infinite-retry 防护这三件事
**永远不在本模块**——per ADR-0019 §open-questions 1/3。
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Protocol

from fcop.models import (
    Failure,
    Recovery,
    RecoveryAction,
    ResumePayload,
    RetryPlan,
    RollbackPlan,
)

__all__ = [
    "make_retry_plan",
    "make_resume_payload",
    "make_rollback_plan",
    "make_abort_artifact",
    "make_escalate_artifact",
    "parse_session_id",
    "ParsedSessionId",
]


@dataclass(frozen=True, slots=True)
class ParsedSessionId:
    """:func:`parse_session_id` 的返回 —— 两种 session_id 形状归一。

    Attributes:
        raw: 原始入参字符串。
        task_id: 解析出的 task_id（如 ``TASK-20260509-006-ADMIN-to-ME``）。
            v1.0 ADR-0019 §session-recovery-hook 形状必填；0.7.x 形状下
            为 None（caller 需扫文件查 task）。
        agent_code: 解析出的 agent code（如 ``ME``）。两种形状都填。
        scheme: 形状标识 —— ``"task_colon_agent"`` 或 ``"sess_dated"``。
    """

    raw: str
    agent_code: str
    scheme: str
    task_id: str | None = None


def parse_session_id(session_id: str) -> ParsedSessionId:
    """解析两种 session_id 形状（per TASK-006 §决议 5）。

    形状 A（per ADR-0019）::

        TASK-20260509-006-ADMIN-to-ME:ME
        ^─────── task_id ────────────^ ^─ agent_code

    形状 B（0.7.x 历史）::

        sess-20260427-me-072
              ^date^  ^^^^^─ agent_code (lowercase) + 序号

    Args:
        session_id: 入参。

    Returns:
        ParsedSessionId —— ``scheme`` 字段标识用了哪种解析。

    Raises:
        ValueError: 两种形状都不匹配。
    """

    if not session_id or not isinstance(session_id, str):
        raise ValueError(f"session_id 必须是非空字符串：{session_id!r}")

    if ":" in session_id:
        task_id, _, agent = session_id.rpartition(":")
        if not task_id or not agent:
            raise ValueError(
                f"task-colon-agent 形状要求两侧非空：{session_id!r}"
            )
        return ParsedSessionId(
            raw=session_id,
            task_id=task_id,
            agent_code=agent,
            scheme="task_colon_agent",
        )

    if session_id.startswith("sess-"):
        rest = session_id[len("sess-") :]
        parts = rest.split("-")
        if len(parts) >= 3:
            agent = parts[1].upper() if parts[1] else ""
            if agent:
                return ParsedSessionId(
                    raw=session_id,
                    task_id=None,
                    agent_code=agent,
                    scheme="sess_dated",
                )

    raise ValueError(
        f"session_id {session_id!r} 既不匹配 'TASK-...:agent' 也不匹配"
        " 'sess-YYYYMMDD-agent-NNN' 形状"
    )


def make_retry_plan(
    failure: Failure,
    *,
    task_path: Path,
    suggested_delay_seconds: int = 0,
    attempt_count: int = 1,
) -> RetryPlan:
    """生成 RETRY recovery 的 plan。

    v1.0 不实际重试——caller 拿这个 plan 自己决定何时何处把 task 喂回
    给 agent。``attempt_count`` / ``suggested_delay_seconds`` 是 caller
    自报，本函数不做 backoff 算法。

    Args:
        failure: 触发 retry 的 failure（仅用于结构对齐，本函数暂不用其
            字段；保留入参以便 v1.x 加 retry_count 守门时不破坏签名）。
        task_path: 要重试的 TASK 文件绝对路径。
        suggested_delay_seconds: 建议在重试前等待的秒数；默认 0。
        attempt_count: 已尝试次数；默认 1（首次重试）。

    Returns:
        :class:`fcop.models.RetryPlan`
    """

    if attempt_count < 1:
        raise ValueError(f"attempt_count 必须 >= 1：{attempt_count}")
    if suggested_delay_seconds < 0:
        raise ValueError(
            f"suggested_delay_seconds 必须 >= 0：{suggested_delay_seconds}"
        )
    return RetryPlan(
        task_path=task_path,
        suggested_delay_seconds=suggested_delay_seconds,
        attempt_count=attempt_count,
    )


def make_resume_payload(
    *,
    session_id: str,
    task_path: Path,
    last_report_path: Path | None,
    extra_metadata: dict[str, object] | None = None,
) -> ResumePayload:
    """生成 RESUME recovery 的 payload（只读）。

    Caller（host adapter / LLM driver）拿这个 payload 自己重建 agent
    context。v1.0 不持久化 LLM context / tool history——推 v1.x。

    Args:
        session_id: 已解析过的 session_id 字符串（caller 自己 parse）。
        task_path: TASK 文件绝对路径。
        last_report_path: 最近一份 REPORT 的绝对路径；首次 retry 时为 None。
        extra_metadata: 扩展键值对，会与默认 metadata 合并；默认空。

    Returns:
        :class:`fcop.models.ResumePayload`
    """

    parsed = parse_session_id(session_id)
    metadata: dict[str, object] = {
        "task_id": parsed.task_id,
        "agent_code": parsed.agent_code,
        "scheme": parsed.scheme,
    }
    if extra_metadata:
        metadata.update(extra_metadata)
    return ResumePayload(
        task_path=task_path,
        last_report_path=last_report_path,
        session_id=session_id,
        metadata=metadata,
    )


def make_rollback_plan(
    *,
    target_commit_hash: str | None,
    affected_files: list[str] | tuple[str, ...],
) -> RollbackPlan:
    """生成 ROLLBACK recovery 的 plan（v1.0 **不**实际跑 git revert）。

    per TASK-006 §决议 3：reference impl 不引入 git 依赖。caller / host
    adapter / human 拿这个 plan 自己决定是否执行 ``git revert``。

    返回值的 ``executed`` 字段**永远是 False**，让 caller 显式确认
    "我看到了，我自己跑"。

    Args:
        target_commit_hash: 建议 revert 到的 commit hash；caller 用 git
            log 自己找出，本函数不查 git。``None`` 表示找不到合适 commit。
        affected_files: 该 TASK 工作期间修改过的文件清单（相对 project root
            的字符串路径）。caller 可基于此打 diff 预览。

    Returns:
        :class:`fcop.models.RollbackPlan`，``executed=False``。
    """

    return RollbackPlan(
        target_commit_hash=target_commit_hash,
        affected_files=tuple(affected_files),
        executed=False,
    )


class _WriteReportFn(Protocol):
    """Type protocol for the abort write-report callback."""

    def __call__(
        self,
        *,
        sender: str,
        recipient: str,
        ref_task: str,
        body: str,
        status: str,
    ) -> object: ...


class _WriteIssueFn(Protocol):
    """Type protocol for the escalate write-issue callback."""

    def __call__(
        self,
        *,
        sender: str,
        recipient: str,
        title: str,
        severity: str,
        body: str,
    ) -> object: ...


def make_abort_artifact(
    failure: Failure,
    *,
    write_report_fn: _WriteReportFn,
    ref_task: str,
    sender: str,
    recipient: str,
    body: str | None = None,
) -> Path:
    """ABORT recovery：写一份 ``status: aborted`` 的 REPORT。

    v1.0 唯一会**实际写盘**的 recovery 之一（另一个是 ESCALATE）。
    本函数不直接 import :class:`fcop.Project` 以避免循环依赖——caller
    传入 ``write_report_fn``（通常是
    ``functools.partial(project.write_report, ...)``，但也可以是测试
    fake）。

    Args:
        failure: 触发 abort 的 failure；用其 evidence + failure_type
            渲染默认 body。
        write_report_fn: 写 report 的回调；签名见 :class:`_WriteReportFn`。
        ref_task: 要 abort 的 TASK 文件路径（绝对或相对 project root，
            按 caller 约定）。
        sender: REPORT 的 sender 角色码（通常 = failure.subject_agent_code）。
        recipient: REPORT 的 recipient 角色码（通常 = TASK.sender）。
        body: 自定义 body；None 时用 failure 字段渲染默认。

    Returns:
        写出的 REPORT 文件路径。
    """

    if body is None:
        body = (
            f"# Aborted by recovery\n\n"
            f"- failure_type: `{failure.failure_type.value}`\n"
            f"- subject_agent: `{failure.subject_agent_code}`\n"
            f"- detected_at: {failure.detected_at.isoformat()}\n"
        )
        if failure.evidence:
            body += f"\n## Evidence\n\n{failure.evidence}\n"

    report = write_report_fn(
        sender=sender,
        recipient=recipient,
        ref_task=ref_task,
        body=body,
        status="aborted",
    )
    path = getattr(report, "path", None)
    if not isinstance(path, Path):
        raise TypeError(
            "write_report_fn 必须返回带 .path: Path 属性的对象，"
            f"实得 {type(report).__name__}"
        )
    return path


def make_escalate_artifact(
    failure: Failure,
    *,
    write_issue_fn: _WriteIssueFn,
    sender: str,
    leader_recipient: str,
    title: str | None = None,
    severity: str = "high",
) -> Path:
    """ESCALATE recovery：写一份 ISSUE 给 leader。

    per ADR-0019 §open-question 4：v1.0 默认升级到 ``leader``（来自
    ``fcop.json``）；caller 自己查 leader 角色码并传 ``leader_recipient``。

    Args:
        failure: 触发 escalate 的 failure。
        write_issue_fn: 写 issue 的回调；签名见 :class:`_WriteIssueFn`。
        sender: ISSUE 的 sender。
        leader_recipient: leader 角色码（caller 从 TeamConfig 查）。
        title: 自定义 title；None 时用 failure 渲染。
        severity: ISSUE 严重度；默认 ``"high"``。

    Returns:
        写出的 ISSUE 文件路径。
    """

    if title is None:
        title = (
            f"Escalation: {failure.failure_type.value} on "
            f"{failure.subject_agent_code}"
        )
    body = (
        f"# Auto-escalated by recovery\n\n"
        f"- failure_type: `{failure.failure_type.value}`\n"
        f"- subject_agent: `{failure.subject_agent_code}`\n"
    )
    if failure.subject_task_id:
        body += f"- subject_task_id: `{failure.subject_task_id}`\n"
    body += f"- detected_at: {failure.detected_at.isoformat()}\n"
    if failure.evidence:
        body += f"\n## Evidence\n\n{failure.evidence}\n"

    issue = write_issue_fn(
        sender=sender,
        recipient=leader_recipient,
        title=title,
        severity=severity,
        body=body,
    )
    path = getattr(issue, "path", None)
    if not isinstance(path, Path):
        raise TypeError(
            "write_issue_fn 必须返回带 .path: Path 属性的对象，"
            f"实得 {type(issue).__name__}"
        )
    return path


def build_recovery_record(
    failure: Failure,
    action: RecoveryAction,
    *,
    initiated_at: datetime | None = None,
    outcome: str = "in_progress",
) -> Recovery:
    """构造 :class:`fcop.models.Recovery` 内存记录。

    工厂函数；显式给个不带 timezone 误差的 default。

    Args:
        failure: 触发 recovery 的 failure。
        action: 5 类 RecoveryAction 之一。
        initiated_at: 时间戳；None 时用 ``datetime.now(UTC)``。
        outcome: ``"in_progress"`` / ``"succeeded"`` / ``"failed"``。

    Returns:
        :class:`fcop.models.Recovery`
    """

    return Recovery(
        recovery_action=action,
        trigger_failure=failure,
        initiated_at=initiated_at or datetime.now(timezone.utc),
        outcome=outcome,
    )


# Re-export the Callable types for static analysis convenience.
WriteReportFn = Callable[..., object]
WriteIssueFn = Callable[..., object]
