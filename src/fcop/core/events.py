"""Event model — polling watcher reference impl.

Per ADR-0018 + TASK-007 §决议 3：v1.0 把事件抽象实现为基于
filesystem state diff 的 polling watcher。**caller 必须显式调
:meth:`Project.poll_once`** —— 本模块不引入任何后台线程 / asyncio
（per TASK-007 §决议 7，是 host adapter 的责任）。

设计核心 3 件事：

1. :class:`WatcherState` —— 缓存上次扫描看到的文件 + 其 mtime + 关键
   frontmatter 字段（status / leader / decision），支持下次比对
2. :func:`scan_workspace` —— 把当前 fcop 工作目录扫成 :class:`WatcherState`
3. :func:`compute_diff` —— 比 prev / curr 两个 state 派生出 :class:`Event`
   列表

12 类 EventType 中 8 类（TASK_CREATED / TASK_ACCEPTED / TASK_BLOCKED /
TASK_COMPLETED / REPORT_FILED / REVIEW_DECIDED / ROLE_SWITCHED + 部
分 BOUNDARY_VIOLATED）由本模块从 polling 派生；剩下 4-5 类
（FAILURE_DETECTED / RECOVERY_INITIATED / RECOVERY_COMPLETED /
SESSION_LOST / 同步 BOUNDARY_VIOLATED）由 :class:`fcop.Project`
内部代码同步触发（per TASK-007 §决议 5）。
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping

from fcop.core.filename import (
    parse_report_filename,
    parse_review_filename,
    parse_task_filename,
)
from fcop.core.frontmatter import parse_frontmatter_raw
from fcop.models import (
    Event,
    EventSource,
    EventSourceKind,
    EventType,
)

__all__ = [
    "WATCHER_ID",
    "WatcherState",
    "FileSnapshot",
    "scan_workspace",
    "compute_diff",
    "make_event",
    "make_event_id",
]

WATCHER_ID = "polling-watcher@v1.0"


@dataclass(frozen=True, slots=True)
class FileSnapshot:
    """单个文件在某次扫描时的快照。

    Attributes:
        relpath: 相对 workspace 根的 POSIX 风格路径（用于跨平台稳定
            的 dict key）。
        mtime: 文件 mtime（POSIX timestamp）。
        kind: ``"task"`` / ``"report"`` / ``"review"`` / ``"config"``
            / ``"other"`` 之一；polling 只关心前 4 类。
        is_archived: 是否在 ``log/`` 子树中。
        status: 从 frontmatter 解析的 ``status`` 字段（小写规范化），
            非 envelope 文件时为 None。
        decision: REVIEW 文件的 decision 字段；其他类型 None。
        sender: envelope 的 sender 字段，便于事件 subject 回填。
        recipient: envelope 的 recipient 字段。
        ref_task: REPORT 的 ``ref_task`` / ``references[0]`` /
            ``related_task`` 字段（任一）的最佳猜测，用于 TASK_BLOCKED /
            TASK_ACCEPTED 派生。
        config_blob_hash: ``kind=config`` 时的 fcop.json 关键字段哈希
            （roles + leader），用于 ROLE_SWITCHED 检测。
    """

    relpath: str
    mtime: float
    kind: str
    is_archived: bool = False
    status: str | None = None
    decision: str | None = None
    sender: str | None = None
    recipient: str | None = None
    ref_task: str | None = None
    config_blob_hash: str | None = None


@dataclass(frozen=True, slots=True)
class WatcherState:
    """一次扫描的完整快照（多个文件）。

    Attributes:
        files: relpath → :class:`FileSnapshot` 的映射。
        scanned_at: 扫描完成的 UTC 时间戳。
    """

    files: dict[str, FileSnapshot] = field(default_factory=dict)
    scanned_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


def make_event_id(event_type: EventType, subject: Mapping[str, object]) -> str:
    """Build a deterministic ``event_id``.

    格式：``"<type>:<sha1(subject_repr)[:12]>"``。同一 type + 同一
    subject 永远生成同一 id —— 这是 polling 去重的依据。

    Args:
        event_type: 事件类型枚举。
        subject: 事件 subject dict。会用 sorted-key repr 哈希以保稳定。

    Returns:
        ``str`` event id。
    """

    canonical = "&".join(f"{k}={subject[k]}" for k in sorted(subject))
    digest = hashlib.sha1(
        f"{event_type.value}|{canonical}".encode("utf-8")
    ).hexdigest()
    return f"{event_type.value}:{digest[:12]}"


def make_event(
    event_type: EventType,
    *,
    subject: Mapping[str, object],
    source: EventSource,
    occurred_at: datetime | None = None,
    metadata: Mapping[str, object] | None = None,
) -> Event:
    """构造 :class:`fcop.models.Event` 的工厂。

    自动生成 event_id（per :func:`make_event_id`）+ 默认 occurred_at
    = ``datetime.now(UTC)`` + 复制 subject/metadata 进 plain dict。
    """

    subj_dict = dict(subject)
    return Event(
        event_id=make_event_id(event_type, subj_dict),
        event_type=event_type,
        occurred_at=occurred_at or datetime.now(timezone.utc),
        subject=subj_dict,
        source=source,
        metadata=dict(metadata or {}),
    )


# ── workspace scanning ──────────────────────────────────────────────


def _classify_filename(name: str) -> str:
    if parse_task_filename(name) is not None:
        return "task"
    if parse_report_filename(name) is not None:
        return "report"
    if parse_review_filename(name) is not None:
        return "review"
    if name == "fcop.json":
        return "config"
    return "other"


def _read_envelope_meta(
    path: Path, kind: str
) -> tuple[str | None, str | None, str | None, str | None, str | None]:
    """Return ``(status, decision, sender, recipient, ref_task)`` from frontmatter.

    Best-effort —— 解析失败全部返回 None；不抛异常。``ref_task`` 仅
    REPORT 类型有意义；TASK / REVIEW 时返回 None。
    """

    try:
        text = path.read_text(encoding="utf-8")
        fm = parse_frontmatter_raw(text)
    except Exception:
        return None, None, None, None, None

    status = fm.get("status")
    if isinstance(status, str):
        status = status.strip().lower() or None
    else:
        status = None

    decision: str | None = None
    if kind == "review":
        d = fm.get("decision")
        if isinstance(d, str):
            decision = d.strip().lower() or None

    sender = fm.get("sender") or fm.get("from")
    sender = str(sender).strip() if sender else None

    recipient = fm.get("recipient") or fm.get("to")
    recipient = str(recipient).strip() if recipient else None

    ref_task: str | None = None
    if kind == "report":
        ref = fm.get("ref_task") or fm.get("related_task")
        if not ref:
            references = fm.get("references")
            if isinstance(references, list) and references:
                ref = references[0]
        if ref:
            ref_str = str(ref).strip()
            # 只取 task_id 段（去掉路径前缀和 .md 后缀）
            tail = Path(ref_str).name
            if tail.endswith(".md"):
                tail = tail[:-3]
            # 0.7.x 有时直接传 task_id（无路径无后缀），保留之
            ref_task = tail or ref_str

    return status, decision, sender, recipient, ref_task


def _read_config_hash(path: Path) -> str | None:
    """Hash the role-relevant slice of fcop.json for ROLE_SWITCHED detection."""

    try:
        import json

        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None

    relevant = {
        "roles": data.get("roles"),
        "leader": data.get("leader"),
    }
    blob = repr(sorted(relevant.items()))
    return hashlib.sha1(blob.encode("utf-8")).hexdigest()[:16]


def scan_workspace(workspace_dir: Path, *, project_root: Path) -> WatcherState:
    """Walk the FCoP workspace and snapshot every relevant file.

    扫描范围（v1.0）：

    - ``<workspace>/tasks/`` + ``<workspace>/log/tasks/``
    - ``<workspace>/reports/`` + ``<workspace>/log/reports/``
    - ``<workspace>/reviews/`` + ``<workspace>/log/reviews/``
    - ``<workspace>/issues/``（issues 不参与 v1.0 events 但顺手扫）
    - ``<project_root>/fcop.json``

    Args:
        workspace_dir: ``Project.workspace_dir`` —— 通常
            ``<project>/docs/agents/``。
        project_root: ``Project._path`` —— fcop.json 所在目录。

    Returns:
        :class:`WatcherState`。文件不存在时返回空 state（不抛错）。
    """

    snapshots: dict[str, FileSnapshot] = {}

    def _scan_dir(directory: Path, *, archived: bool) -> None:
        if not directory.is_dir():
            return
        for entry in directory.iterdir():
            if not entry.is_file():
                continue
            kind = _classify_filename(entry.name)
            if kind == "other":
                continue
            try:
                mtime = entry.stat().st_mtime
            except OSError:
                continue
            relpath = entry.relative_to(project_root).as_posix()
            status, decision, sender, recipient, ref_task = (
                _read_envelope_meta(entry, kind)
                if kind in {"task", "report", "review"}
                else (None, None, None, None, None)
            )
            snapshots[relpath] = FileSnapshot(
                relpath=relpath,
                mtime=mtime,
                kind=kind,
                is_archived=archived,
                status=status,
                decision=decision,
                sender=sender,
                recipient=recipient,
                ref_task=ref_task,
            )

    for sub in ("tasks", "reports", "reviews", "issues"):
        _scan_dir(workspace_dir / sub, archived=False)
    log_root = workspace_dir / "log"
    for sub in ("tasks", "reports", "reviews"):
        _scan_dir(log_root / sub, archived=True)

    config = project_root / "fcop.json"
    if config.is_file():
        try:
            mtime = config.stat().st_mtime
        except OSError:
            mtime = 0.0
        snapshots["fcop.json"] = FileSnapshot(
            relpath="fcop.json",
            mtime=mtime,
            kind="config",
            config_blob_hash=_read_config_hash(config),
        )

    return WatcherState(files=snapshots)


# ── diff → events ────────────────────────────────────────────────────


def _file_source(snap: FileSnapshot) -> EventSource:
    return EventSource(
        kind=EventSourceKind.FILE,
        path=snap.relpath,
        watcher=WATCHER_ID,
    )


def _derived_source(relpath: str) -> EventSource:
    return EventSource(
        kind=EventSourceKind.DERIVED,
        path=relpath,
        watcher=WATCHER_ID,
    )


def _task_id_from_relpath(relpath: str) -> str:
    """Strip dir + .md to get TASK-... id."""
    name = Path(relpath).name
    return name[:-3] if name.endswith(".md") else name


def compute_diff(
    prev: WatcherState | None,
    curr: WatcherState,
    *,
    occurred_at: datetime | None = None,
) -> list[Event]:
    """Compute the ordered :class:`Event` list between two snapshots.

    本函数是**纯函数** —— 完全由 prev / curr 决定输出，不读 filesystem。
    这让 diff 行为可以被任意构造的 :class:`WatcherState` 测试，无需
    创建真实文件。

    去重契约（per TASK-007 §决议 6）：

    - ``_CREATED`` / ``_FILED`` 仅在 path 在 curr 但不在 prev 时触发
    - ``_ACCEPTED`` / ``_BLOCKED`` 仅在 status 字段从 X → Y 切换时触发
    - ``_COMPLETED`` 仅在 task 从 open → archived 移动时触发
    - ``_DECIDED`` 仅在 review 文件首次出现时触发（v1.0 不追踪修改）
    - ``ROLE_SWITCHED`` 仅在 fcop.json 的 config_blob_hash 变化时触发

    ``prev=None`` 视为"首次扫描" —— 此时**只发** TASK_CREATED /
    REPORT_FILED / REVIEW_DECIDED 类事件（已存在的 task/report 视为
    新 caller 接手时应感知到的状态）。如果 caller 不希望首次扫描发
    一堆事件，应先调一次 :func:`scan_workspace` + 丢掉结果再 subscribe。

    Args:
        prev: 上一次 :class:`WatcherState`；``None`` 视为空 state。
        curr: 这一次 :class:`WatcherState`。
        occurred_at: 显式时间戳；默认 ``curr.scanned_at``。

    Returns:
        按 (event_type 字典序, relpath 字典序) 稳定排序的事件列表。
    """

    when = occurred_at or curr.scanned_at
    prev_files = prev.files if prev else {}
    events: list[Event] = []

    # ── pass 1: 新增文件类事件 ────────────────────────────────────
    for relpath, snap in curr.files.items():
        if relpath in prev_files:
            continue

        if snap.kind == "task":
            if snap.is_archived:
                # 极端：第一次看到的 task 已在 log/ → 当 COMPLETED
                events.append(
                    make_event(
                        EventType.TASK_COMPLETED,
                        subject={"task_id": _task_id_from_relpath(relpath)},
                        source=_derived_source(relpath),
                        occurred_at=when,
                    )
                )
            else:
                events.append(
                    make_event(
                        EventType.TASK_CREATED,
                        subject={
                            "task_id": _task_id_from_relpath(relpath),
                            **({"sender": snap.sender} if snap.sender else {}),
                            **(
                                {"recipient": snap.recipient}
                                if snap.recipient else {}
                            ),
                        },
                        source=_file_source(snap),
                        occurred_at=when,
                    )
                )

        elif snap.kind == "report":
            # REPORT_FILED 总是发；额外按 status 派生 TASK_BLOCKED
            ref_task = _extract_ref_task_id_from_snap(snap)
            subject_filed: dict[str, object] = {
                "report_id": _task_id_from_relpath(relpath),
            }
            if ref_task:
                subject_filed["task_id"] = ref_task
            events.append(
                make_event(
                    EventType.REPORT_FILED,
                    subject=subject_filed,
                    source=_file_source(snap),
                    occurred_at=when,
                )
            )
            if snap.status == "blocked" and ref_task:
                events.append(
                    make_event(
                        EventType.TASK_BLOCKED,
                        subject={
                            "task_id": ref_task,
                            "reason": "report status=blocked",
                        },
                        source=_derived_source(relpath),
                        occurred_at=when,
                    )
                )
            if snap.status in {"accepted", "in_progress"} and ref_task:
                events.append(
                    make_event(
                        EventType.TASK_ACCEPTED,
                        subject={"task_id": ref_task},
                        source=_derived_source(relpath),
                        occurred_at=when,
                    )
                )

        elif snap.kind == "review":
            subj: dict[str, object] = {
                "review_id": _task_id_from_relpath(relpath),
            }
            if snap.decision:
                subj["decision"] = snap.decision
            events.append(
                make_event(
                    EventType.REVIEW_DECIDED,
                    subject=subj,
                    source=_file_source(snap),
                    occurred_at=when,
                )
            )

    # ── pass 2: 已有文件的状态/位置变化 ────────────────────────────
    for relpath, snap in curr.files.items():
        prev_snap = prev_files.get(relpath)
        if prev_snap is None:
            continue

        # status 字段从 X → Y
        if (
            snap.kind == "report"
            and snap.status != prev_snap.status
            and snap.status is not None
        ):
            ref_task = _extract_ref_task_id_from_snap(snap)
            if snap.status == "blocked" and ref_task:
                events.append(
                    make_event(
                        EventType.TASK_BLOCKED,
                        subject={
                            "task_id": ref_task,
                            "reason": "report status changed to blocked",
                        },
                        source=_derived_source(relpath),
                        occurred_at=when,
                    )
                )
            elif snap.status in {"accepted", "in_progress"} and ref_task:
                events.append(
                    make_event(
                        EventType.TASK_ACCEPTED,
                        subject={"task_id": ref_task},
                        source=_derived_source(relpath),
                        occurred_at=when,
                    )
                )

        # config 文件 ROLE_SWITCHED
        if (
            snap.kind == "config"
            and snap.config_blob_hash != prev_snap.config_blob_hash
        ):
            events.append(
                make_event(
                    EventType.ROLE_SWITCHED,
                    subject={
                        "from": prev_snap.config_blob_hash or "UNKNOWN",
                        "to": snap.config_blob_hash or "UNKNOWN",
                        "reason": "fcop.json roles/leader changed",
                    },
                    source=_file_source(snap),
                    occurred_at=when,
                )
            )

    # ── pass 3: TASK_COMPLETED ── 文件从 open → archived 移动 ─────
    for relpath, prev_snap in prev_files.items():
        if prev_snap.kind != "task" or prev_snap.is_archived:
            continue
        if relpath in curr.files:
            continue
        # path 不见了 —— 找 log/ 下同名是否出现
        archived_name = Path(relpath).name
        for curr_relpath, curr_snap in curr.files.items():
            if (
                curr_snap.kind == "task"
                and curr_snap.is_archived
                and Path(curr_relpath).name == archived_name
                and curr_relpath not in prev_files
            ):
                events.append(
                    make_event(
                        EventType.TASK_COMPLETED,
                        subject={
                            "task_id": _task_id_from_relpath(curr_relpath),
                        },
                        source=_derived_source(curr_relpath),
                        occurred_at=when,
                    )
                )
                break

    # 去重：同 event_id 仅保留首次出现（pass 1 优先于 pass 3 的派生）
    seen_ids: set[str] = set()
    deduped: list[Event] = []
    for ev in events:
        if ev.event_id in seen_ids:
            continue
        seen_ids.add(ev.event_id)
        deduped.append(ev)

    return sorted(deduped, key=lambda e: (e.event_type.value, e.event_id))


def _extract_ref_task_id_from_snap(snap: FileSnapshot) -> str | None:
    """REPORT snapshot → 它指向的 TASK id（best-effort）。"""
    return snap.ref_task
