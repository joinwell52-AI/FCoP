"""Public read-only data structures returned by the fcop library.

All models are :func:`dataclasses.dataclass(frozen=True, slots=True)` so
they are hashable, immutable, and have a tiny memory footprint. They are
the public contract of the library — changing any field name, type, or
default in a non-additive way is a breaking change per semver.

See adr/ADR-0001-library-api.md ("数据结构") for the full contract.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Literal

__all__ = [
    "Priority",
    "Severity",
    "ReviewDecision",
    "ReviewSubjectType",
    "AgentLayer",
    "FailureType",
    "RecoveryAction",
    "SessionRecoveryAction",
    "TaskFrontmatter",
    "Task",
    "Report",
    "Issue",
    "Review",
    "Capability",
    "BoundaryViolation",
    "Failure",
    "Recovery",
    "RetryPlan",
    "ResumePayload",
    "RollbackPlan",
    "RecoveryOutcome",
    "SessionRecoveryResult",
    "FailureReceipt",
    "TeamConfig",
    "ProjectStatus",
    "RecentActivityEntry",
    "RoleOccupancy",
    "DriftEntry",
    "DriftReport",
    "SessionRoleConflict",
    "ValidationIssue",
    "DeploymentReport",
]


# ── Enums ─────────────────────────────────────────────────────────────


class Priority(str, Enum):
    """Task priority band. Matches the four P-levels in fcop-rules.mdc."""

    P0 = "P0"
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"


class Severity(str, Enum):
    """Issue severity band."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ReviewDecision(str, Enum):
    """REVIEW 决议四值枚举（v1.0 frozen，per ADR-0017）。

    - APPROVED：通过
    - REJECTED：驳回（subject 整体不可用）
    - NEEDS_CHANGES：要求修改（必须配合非空 required_changes 列出条目）
    - ABSTAINED：弃权 / 不在职责范围内

    刻意**不含** ``needs_human``——人类介入语义推迟到 v1.2，按 ADR-0017
    §explicit-deferrals。任何想偷塞 ``needs_human`` 的 PR 会被 schema
    层（review.schema.json#/$defs/decisionEnum）和本 enum 双重拒。
    """

    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_CHANGES = "needs_changes"
    ABSTAINED = "abstained"


class AgentLayer(str, Enum):
    """Agent 的三层 capability bundle 简写（v1.0 frozen，per ADR-0020）。

    - WORKER：默认；只能动 file_io / task_io / modify_code 等
    - GOVERNANCE：can review_decision；不能 modify_code，不能 spawn_agent
    - ADMIN：人类操作员；不能由 ``fcop.json.roles`` 显式声明
      （per ADR-0020 §决议 4 + rule ``NO_ADMIN_PROGRAMMATIC_CREATE``）

    显式 ``can`` / ``cannot`` 字段覆盖 layer 默认（rule
    ``EXPLICIT_OVERRIDES_LAYER``）。
    """

    WORKER = "worker"
    GOVERNANCE = "governance"
    ADMIN = "admin"


class FailureType(str, Enum):
    """Runtime 失败类型四值枚举（v1.0 frozen，per ADR-0019）。

    POSIX 类比：FCoP 之于 Failure = Unix 之于 errno。本 enum 的值与
    ``failure.schema.json#/$defs/failureType/enum`` 必须一致——
    test_failure_record_schema_compat 在 CI 守门。

    扩展失败类型必须发新 ADR + bump MINOR（schema 同步加值）。

    - TIMEOUT：agent 在约定时间内未交付（如超过 TASK.timeout_at）
    - CRASH：reference impl / host adapter 异常退出（如 OOM、SIGKILL）
    - DEADLOCK：多 agent 互相等待（如 A 等 B 的 REVIEW，B 等 A 的 REPORT）
    - DRIFT：agent 输出与 TASK 约定不符（越界、答非所问）
    """

    TIMEOUT = "TIMEOUT"
    CRASH = "CRASH"
    DEADLOCK = "DEADLOCK"
    DRIFT = "DRIFT"


class RecoveryAction(str, Enum):
    """Runtime 恢复动作五值枚举（v1.0 frozen，per ADR-0019）。

    每个 Failure 必须配对至少一个 Recovery；具体 mapping 由 host
    adapter 决定，FCoP 协议层不强制 enforce。Project.apply_recovery
    把这 5 类映射到 reference impl 函数（per TASK-006 §决议 3）。

    - RETRY：同一 agent 重做同一 TASK（v1.0 仅返回 RetryPlan，不实际重试）
    - RESUME：加载 session state 从中断点继续（v1.0 仅返回 ResumePayload）
    - ROLLBACK：回到 TASK 创建前文件状态（v1.0 仅返回 RollbackPlan，不
      实际跑 git revert——per TASK-006 §决议 3）
    - ABORT：终止 TASK，写 REPORT status: aborted
    - ESCALATE：升级到 leader 写 ISSUE
    """

    RETRY = "RETRY"
    RESUME = "RESUME"
    ROLLBACK = "ROLLBACK"
    ABORT = "ABORT"
    ESCALATE = "ESCALATE"


class SessionRecoveryAction(str, Enum):
    """``Project.recover_session`` 仅暴露的 3 类 action（v1.0 frozen）。

    per ADR-0019 §session-recovery-hook + failure.schema.json
    sessionRecoveryAction enum：仅 ``resume`` / ``rollback`` / ``abort``
    是 session 级动作。RETRY 是 task 级、ESCALATE 跨 session，它们走
    :meth:`fcop.Project.apply_recovery` 而非 ``recover_session``。

    任何想偷塞 RETRY / ESCALATE 进 recover_session 的 PR 会被本 enum +
    schema enum 双层拒。
    """

    RESUME = "resume"
    ROLLBACK = "rollback"
    ABORT = "abort"


class ReviewSubjectType(str, Enum):
    """REVIEW 评审对象的四类型枚举（v1.0 frozen，per ADR-0017）。

    - TASK：评审某个 TASK envelope（典型：governance 层批准/驳回）
    - REPORT：评审某个 REPORT envelope（典型：成果验收）
    - ROLE_SWITCH：评审一次角色切换决策
    - CODE_CHANGE：评审一段代码改动（commit / PR / patch hash）
    """

    TASK = "task"
    REPORT = "report"
    ROLE_SWITCH = "role_switch"
    CODE_CHANGE = "code_change"


# ── Task ──────────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class TaskFrontmatter:
    """Parsed YAML frontmatter of a TASK-*.md file.

    Unknown keys are preserved in :attr:`extra` so forward-compatible
    additions to the protocol don't silently drop data.
    """

    protocol: str
    version: int
    sender: str
    recipient: str
    priority: Priority
    thread_key: str | None = None
    subject: str | None = None
    references: tuple[str, ...] = ()
    extra: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class Task:
    """A task file on disk.

    Properties :attr:`sender`, :attr:`recipient`, :attr:`priority`,
    :attr:`subject` are convenience accessors forwarding to
    :attr:`frontmatter`.
    """

    path: Path
    filename: str
    task_id: str
    date: str
    sequence: int
    frontmatter: TaskFrontmatter
    body: str
    is_archived: bool
    mtime: datetime

    @property
    def sender(self) -> str:
        return self.frontmatter.sender

    @property
    def recipient(self) -> str:
        return self.frontmatter.recipient

    @property
    def priority(self) -> Priority:
        return self.frontmatter.priority

    @property
    def subject(self) -> str | None:
        return self.frontmatter.subject


# ── Report ────────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class Report:
    """A report file responding to a task."""

    path: Path
    filename: str
    task_id: str
    reporter: str
    recipient: str
    status: Literal["done", "blocked", "in_progress"]
    body: str
    is_archived: bool
    mtime: datetime


# ── Issue ─────────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class Issue:
    """An issue file.

    Issues are broadcasts that don't follow the A-to-B task chain:
    they describe a problem observed by any role, addressed to whoever
    can fix it.
    """

    path: Path
    filename: str
    issue_id: str
    summary: str
    severity: Severity
    reporter: str
    body: str
    mtime: datetime


# ── Review ────────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class Review:
    """A REVIEW envelope file on disk（v1.0 引入，per ADR-0017）。

    REVIEW 是 FCoP v1.0 落地的第七个核心抽象（Audit）的唯一文件载体。
    它**不**承载人类批准语义——任何 ``human_approval`` 子对象、
    ``mark_human_approved`` API 都被推迟到 v1.2，本 dataclass 也刻意
    不含相关字段（schema 层 + dataclass 层双锁）。

    Attributes:
        path: 绝对路径。
        filename: 文件名（``REVIEW-YYYYMMDD-NNN-{reviewer}-on-{subject_short}.md``）。
        review_id: 文件名 stem 的稳定 id；与 frontmatter ``review_id``
            字段同值。
        date: ``YYYYMMDD``。
        sequence: 当日序号 1..999。
        subject_type: 评审对象类型枚举。
        subject_ref: 对象引用——TASK/REPORT 是路径，CODE_CHANGE 是 hash。
        reviewer_role: 评审者角色 code（必须通过 role-code 校验，允许
            reserved 如 ADMIN）。
        reviewer_agent: 可选；标识具体 session / agent 实例。
        decision: 四值决议枚举。
        rationale: 可选自由文本理由。
        required_changes: ``decision == NEEDS_CHANGES`` 时必须非空；
            其他决议下应为空 tuple。
        decided_at: 决议时间（解析为 datetime；YAML 自动 ISO parse）。
        body: REVIEW Markdown body（rationale 与 required_changes 已在
            frontmatter，body 是补充论证 / 上下文）。
        is_archived: 是否在 ``log/reviews/`` 下。
        mtime: 文件 mtime。
    """

    path: Path
    filename: str
    review_id: str
    date: str
    sequence: int
    subject_type: ReviewSubjectType
    subject_ref: str
    reviewer_role: str
    reviewer_agent: str | None
    decision: ReviewDecision
    rationale: str | None
    required_changes: tuple[str, ...]
    decided_at: datetime
    body: str
    is_archived: bool
    mtime: datetime


# ── Boundary / Capability ────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class Capability:
    """一个 role code 的 capability 视图（v1.0，per ADR-0020）。

    `lookup_capability(role_code, config)` 的返回值。把 fcop.json 里
    显式声明的 layer/can/cannot 与 layer 默认 bundle 合并后得到。

    Attributes:
        code: role code（已通过 role-code 校验）。
        layer: ``AgentLayer`` 枚举。``ADMIN`` 仅能由 reserved sender
            （人类）使用，不能由 fcop.json.roles 显式声明——若声明了，
            ``lookup_capability`` 会 raise ``BoundaryViolationError``。
        can: 显式允许的 capability token tuple（已与 layer 默认 union）。
        cannot: 显式禁止的 capability token tuple（已与 layer 默认
            union；优先级高于 can —— rule ``EXPLICIT_OVERRIDES_LAYER``）。
        is_explicit: 该 role 在 fcop.json 是否显式声明了 layer/can/cannot
            字段。``False`` 意味着完全继承 layer default（fallback worker）；
            用于 ``fcop_report()`` 的"capability 缺字段"警告。
    """

    code: str
    layer: AgentLayer
    can: tuple[str, ...]
    cannot: tuple[str, ...]
    is_explicit: bool


@dataclass(frozen=True, slots=True)
class BoundaryViolation:
    """一条 boundary 规则被触发的记录（v1.0，per ADR-0020）。

    由 `core.boundary.validate_action` 产生；当
    `Project.assert_boundary` 收集到 ≥1 条时打包成
    :class:`fcop.errors.BoundaryViolationError` raise 出去。

    Attributes:
        rule_id: ADR-0020 §决议 5 表里的规则 id 之一，或扩展常量
            ``UNKNOWN_CAPABILITY``（severity == warning）。
        actor: 主语角色 code。
        action: capability token；可能是 v1.0 词表外的字符串
            （UNKNOWN_CAPABILITY 时）。
        target: 宾语角色 code，或 ``None``（如 spawn_agent 类无对象动作）。
        message: 人类可读的违规说明。
        severity: ``"error"`` 表示阻塞操作；``"warning"`` 仅 advisory
            （目前唯一来源是 UNKNOWN_CAPABILITY）。
    """

    rule_id: str
    actor: str
    action: str
    target: str | None
    message: str
    severity: Literal["error", "warning"] = "error"


# ── Failure & Recovery ───────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class Failure:
    """一次 runtime 失败的内存记录（v1.0，per ADR-0019）。

    与 :class:`Review` 不同，Failure 不是 IPC envelope —— **不写盘**
    （per TASK-006 §决议 1）。它是 ``Project.report_failure`` 的入参
    与 ``apply_recovery`` 的依据；持久化由 caller 自己的日志系统负责。

    Attributes:
        failure_type: 4 类失败枚举之一。
        subject_task_id: 失败发生在哪个 task 上下文（可选——CRASH 类
            可能没具体 task，留 None）。
        subject_agent_code: 哪个 agent 失败（必填——失败必有主体）。
        detected_at: 检测到失败的时间戳。
        evidence: 自由文本证据（last seen log、stack trace 摘要、
            partial output 等）。
        suggested_recovery: 建议的恢复动作枚举；可选（reporter 不一定
            知道最佳恢复路径）。
    """

    failure_type: FailureType
    subject_agent_code: str
    detected_at: datetime
    subject_task_id: str | None = None
    evidence: str = ""
    suggested_recovery: RecoveryAction | None = None


@dataclass(frozen=True, slots=True)
class Recovery:
    """一次 recovery 尝试的内存记录（v1.0，per ADR-0019）。

    由 :meth:`fcop.Project.apply_recovery` 内部构造；记录"针对哪个
    failure 应用了哪个 recovery action"。同样不写盘。

    Attributes:
        recovery_action: 5 类恢复动作枚举之一。
        trigger_failure: 触发本次恢复的 :class:`Failure` 实例。
        initiated_at: 恢复发起时间。
        outcome: 自由 enum 字符串（``"in_progress"`` / ``"succeeded"``
            / ``"failed"``）；v1.0 不冻 outcome 词表。
    """

    recovery_action: RecoveryAction
    trigger_failure: Failure
    initiated_at: datetime
    outcome: str = "in_progress"


@dataclass(frozen=True, slots=True)
class RetryPlan:
    """RETRY recovery 的返回 plan（v1.0 不实际重试，仅给 plan）。

    Attributes:
        task_path: 要重试的 TASK 文件绝对路径（caller 用它重新喂给 agent）。
        suggested_delay_seconds: 建议在重试前等待的秒数（exponential
            backoff 启发；v1.0 默认 0）。
        attempt_count: 已尝试次数（v1.0 reporter 自报；本字段不强制
            防 infinite retry——per ADR-0019 §open-question 3）。
    """

    task_path: Path
    suggested_delay_seconds: int = 0
    attempt_count: int = 1


@dataclass(frozen=True, slots=True)
class ResumePayload:
    """RESUME recovery 的返回 payload（只读）。

    Caller（host adapter / LLM driver）拿到这个 payload 自己重建
    agent context。v1.0 不持久化 LLM context / tool history（推 v1.x）。

    Attributes:
        task_path: TASK 文件绝对路径。
        last_report_path: 最近一份 REPORT 的绝对路径；可能为 None
            （首次 retry 时还没 REPORT）。
        session_id: 解析后的 session_id 字符串（与入参一致）。
        metadata: 自由 dict —— v1.0 兜底 placeholder for future
            session schema fields；目前包含 ``{"task_id": ...,
            "agent_code": ...}``。
    """

    task_path: Path
    last_report_path: Path | None
    session_id: str
    metadata: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class RollbackPlan:
    """ROLLBACK recovery 的返回 plan（v1.0 **不实际跑 git revert**）。

    per TASK-006 §决议 3：v1.0 仅返回需要 revert 的信息，由 host
    adapter / human 决定是否执行。这避免了 reference impl 引入 git
    依赖 + 防止脚本误删工作。

    Attributes:
        target_commit_hash: 建议 revert 到的 commit hash；v1.0 best-effort
            （从 git log 找 TASK 创建前的 commit），失败时 None。
        affected_files: 该 TASK 工作期间修改过的文件清单（路径相对
            project root）。caller 可基于此打预览 diff。
        executed: **永远是 False**，标识 v1.0 plan-only 语义。
    """

    target_commit_hash: str | None
    affected_files: tuple[str, ...]
    executed: bool = False


@dataclass(frozen=True, slots=True)
class RecoveryOutcome:
    """``Project.apply_recovery`` 的返回值。

    包装 :class:`Recovery` record + 5 类 recovery 各自的 plan/payload
    + 写盘类 recovery（ABORT/ESCALATE）实际生成的文件路径。

    Attributes:
        recovery: 内存记录。
        plan: 5 类的具体 plan/payload；类型与 recovery_action 对应：
            - RETRY → :class:`RetryPlan`
            - RESUME → :class:`ResumePayload`
            - ROLLBACK → :class:`RollbackPlan`
            - ABORT / ESCALATE → 写出的文件路径 :class:`pathlib.Path`
              （ABORT 写 REPORT，ESCALATE 写 ISSUE）
        artifact_path: ``ABORT`` / ``ESCALATE`` 写出的文件路径；其他
            recovery 时为 None。冗余于 plan 但便于 caller 直接拿到。
    """

    recovery: Recovery
    plan: object
    artifact_path: Path | None = None


@dataclass(frozen=True, slots=True)
class SessionRecoveryResult:
    """``Project.recover_session`` 的返回值。

    Attributes:
        session_id: 入参回显（解析后的）。
        action: 实际执行的 SessionRecoveryAction。
        outcome: ``"succeeded"`` / ``"session_not_found"`` /
            ``"failed"`` 之一。
        payload: action 对应的具体 payload；resume → ResumePayload，
            rollback → RollbackPlan，abort → 写出的 REPORT 路径。
            ``outcome != "succeeded"`` 时为 None。
        error: outcome 非 succeeded 时的人类可读说明。
    """

    session_id: str
    action: SessionRecoveryAction
    outcome: str
    payload: object | None = None
    error: str | None = None


@dataclass(frozen=True, slots=True)
class FailureReceipt:
    """``Project.report_failure`` 的返回值（acknowledge）。

    v1.0 不写盘，所以只返回一个收据告诉 caller "已收到、stub 事件
    已 emit"。TASK-007 接事件后会换成真实 event_id。

    Attributes:
        failure: 入参回显。
        accepted_at: 收到时间（与 failure.detected_at 不同——前者是
            report 时刻）。
        event_emitted: bool，stub 事件是否被调（v1.0 总是 True；
            TASK-007 接事件后可能因订阅者抛错变 False）。
    """

    failure: Failure
    accepted_at: datetime
    event_emitted: bool = True


# ── Project configuration ────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class TeamConfig:
    """In-memory representation of ``docs/agents/fcop.json``."""

    mode: Literal["solo", "preset", "custom"]
    team: str
    leader: str
    roles: tuple[str, ...]
    lang: str
    version: int
    extra: dict[str, object] = field(default_factory=dict)

    @property
    def is_solo(self) -> bool:
        return self.mode == "solo"


# ── Status ────────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class RecentActivityEntry:
    """A single row in :attr:`ProjectStatus.recent_activity`."""

    kind: Literal["task", "report", "issue"]
    filename: str
    mtime: datetime
    summary: str


@dataclass(frozen=True, slots=True)
class ProjectStatus:
    """A snapshot of project-wide counts and the most recent activity."""

    path: Path
    is_initialized: bool
    config: TeamConfig | None
    tasks_open: int
    tasks_archived: int
    reports_count: int
    issues_count: int
    recent_activity: tuple[RecentActivityEntry, ...]


@dataclass(frozen=True, slots=True)
class RoleOccupancy:
    """Per-role occupancy snapshot derived from the on-disk ledger.

    Returned by :meth:`fcop.Project.role_occupancy`. Backs the
    "Role occupancy" section of `fcop_report()`'s UNBOUND output and
    is the canonical data source agents consult before transitioning
    from UNBOUND to BOUND (Rule 1 + ``fcop_protocol_version: 1.5.0``
    UNBOUND step 4).

    A role's status is computed from filename parses only — bodies are
    never read, so this method is safe to call from an UNBOUND session.

    Attributes:
        role: The role code as it appears in :class:`TeamConfig.roles`.
        open_tasks: ``TASK-*.md`` files in ``tasks/`` where ``role`` is
            sender or recipient.
        open_reports: ``REPORT-*.md`` files in ``reports/`` where
            ``role`` is reporter or recipient.
        open_issues: ``ISSUE-*.md`` files in ``issues/`` where ``role``
            is the reporter.
        archived_tasks: ``TASK-*.md`` files in ``log/tasks/`` involving
            ``role`` (sender or recipient).
        last_session_id: ``session_id`` frontmatter value of the most
            recently modified file involving the role, if any. May be
            ``None`` if the field was never written by an older fcop
            version, or if no files mention the role.
        last_seen_at: ``mtime`` of the most recently modified file
            involving the role.
        status: ``"UNUSED"`` (no files anywhere), ``"ARCHIVED"`` (only
            archived files), or ``"ACTIVE"`` (at least one open file).
    """

    role: str
    open_tasks: int
    open_reports: int
    open_issues: int
    archived_tasks: int
    last_session_id: str | None
    last_seen_at: datetime | None
    status: Literal["UNUSED", "ARCHIVED", "ACTIVE"]


# ── Audit ─────────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class DriftEntry:
    """One file in the working tree that drifted outside the FCoP ledger.

    Surfaces uncommitted / unstaged changes that were *not* produced
    via the four-step task→do→report→archive cycle. Drift is detected
    by parsing ``git status --porcelain`` and removing anything under
    ``docs/agents/{tasks,reports,issues,log}/``.

    Attributes:
        path: Path relative to the project root.
        status: Two-character porcelain code (``"M "``, ``"??"``, etc.).
            Kept verbatim so callers can re-format if needed.
        in_ledger: ``True`` only when the file lives under one of the
            FCoP ledger directories above. Always ``False`` for the
            entries returned in :attr:`DriftReport.entries`; included
            on the dataclass so test fixtures and consumers can
            inspect ledger files when scanning a wider set.
    """

    path: str
    status: str
    in_ledger: bool


@dataclass(frozen=True, slots=True)
class SessionRoleConflict:
    """One ``session_id`` that produced files under multiple role codes.

    Returned by :meth:`fcop.Project.audit_drift` (within
    :class:`DriftReport.session_role_conflicts`). The presence of any
    entry is direct evidence of Rule 1 sub-agent role impersonation
    (since 1.8.0): one session = one role binding, period.

    Attributes:
        session_id: The shared frontmatter field that ties files
            together.
        roles: All distinct role codes the session signed files under
            (sorted).
        files: All ledger files where this conflict shows up (sorted
            by path).
    """

    session_id: str
    roles: tuple[str, ...]
    files: tuple[Path, ...]


@dataclass(frozen=True, slots=True)
class DriftReport:
    """Result of :meth:`fcop.Project.audit_drift`.

    Two independent audits live in this report:

    1. **Working-tree drift**: files that ``git`` thinks are dirty
       (``modified`` / ``untracked`` / ``deleted``) and that do *not*
       sit under the FCoP ledger directories. These are the canonical
       Rule 0.a.1 violations — work performed without the four-step
       cycle.
    2. **Session/role conflicts**: ``session_id`` values that appear
       under more than one role code. These are the canonical Rule 1
       sub-agent impersonation evidence (since 1.8.0).

    Attributes:
        entries: One :class:`DriftEntry` per drifting file.
        session_role_conflicts: One :class:`SessionRoleConflict` per
            conflicting session.
        git_available: ``False`` when ``git`` could not be invoked
            (no git binary, not a git repo). The audit falls back to
            an empty :attr:`entries` and a warning printed by the
            caller; :attr:`session_role_conflicts` still works because
            it does not depend on git.
    """

    entries: tuple[DriftEntry, ...]
    session_role_conflicts: tuple[SessionRoleConflict, ...]
    git_available: bool


# ── Validation ────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    """A single problem found by ``inspect_task`` or ``validate_team``.

    ``severity == "error"`` means "rejected, won't write/accept";
    ``"warning"`` means "accepted but discouraged"; ``"info"`` is purely
    diagnostic.
    """

    severity: Literal["error", "warning", "info"]
    field: str
    message: str
    path: Path | None = None


# ── Deployment ────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class DeploymentReport:
    """Result of ``Project.deploy_role_templates()``.

    When ``force=True`` and conflicting files exist, they are moved to
    ``.fcop/migrations/<timestamp>/`` rather than overwritten silently.
    :attr:`migration_dir` points to that archive, or ``None`` if no
    archiving happened.
    """

    deployed: tuple[Path, ...]
    skipped: tuple[Path, ...]
    archived: tuple[Path, ...]
    migration_dir: Path | None
