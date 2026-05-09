"""tests/test_fcop/test_core_events.py —— TASK-007 R1 测试 ≥ 12 用例。

覆盖 EventType / Event 模型 + scan_workspace + compute_diff 纯函数行为。
不依赖 :class:`fcop.Project`——验证 ADR-0018 §design-details "core
模块独立可被 host adapter 复用"。
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from fcop import Event, EventSource, EventSourceKind, EventType
from fcop.core.events import (
    WATCHER_ID,
    FileSnapshot,
    WatcherState,
    compute_diff,
    make_event,
    make_event_id,
    scan_workspace,
)
from fcop.core.jsonschema_validator import load_bundled_schema


# ── EventType / Event 词表对齐 ──────────────────────────────────────


class TestEventTypeAlignment:
    def test_event_type_has_12_values(self):
        assert len(EventType) == 12

    def test_event_type_aligns_with_schema(self):
        """EventType 必须与 event.schema.json 词表完全相符。"""
        schema = load_bundled_schema("event.schema.json")
        schema_enum = set(schema["$defs"]["eventType"]["enum"])
        py_enum = {e.value for e in EventType}
        assert py_enum == schema_enum, (
            f"drifted: {py_enum ^ schema_enum}"
        )

    def test_event_source_kind_aligns_with_schema(self):
        schema = load_bundled_schema("event.schema.json")
        schema_enum = set(schema["properties"]["source"]["properties"]["kind"]["enum"])
        py_enum = {k.value for k in EventSourceKind}
        assert py_enum == schema_enum


# ── make_event / make_event_id ──────────────────────────────────────


class TestMakeEvent:
    def test_event_id_deterministic(self):
        eid1 = make_event_id(EventType.TASK_CREATED, {"task_id": "TASK-foo"})
        eid2 = make_event_id(EventType.TASK_CREATED, {"task_id": "TASK-foo"})
        assert eid1 == eid2
        assert eid1.startswith("TASK_CREATED:")

    def test_event_id_subject_order_independent(self):
        eid1 = make_event_id(
            EventType.REPORT_FILED, {"task_id": "T1", "report_id": "R1"}
        )
        eid2 = make_event_id(
            EventType.REPORT_FILED, {"report_id": "R1", "task_id": "T1"}
        )
        assert eid1 == eid2

    def test_event_id_differs_by_subject(self):
        eid1 = make_event_id(EventType.TASK_CREATED, {"task_id": "TASK-foo"})
        eid2 = make_event_id(EventType.TASK_CREATED, {"task_id": "TASK-bar"})
        assert eid1 != eid2

    def test_make_event_default_occurred_at_is_utc(self):
        ev = make_event(
            EventType.TASK_CREATED,
            subject={"task_id": "TASK-foo"},
            source=EventSource(kind=EventSourceKind.FILE, path="x.md"),
        )
        assert isinstance(ev, Event)
        assert ev.occurred_at.tzinfo is not None
        assert ev.event_type == EventType.TASK_CREATED


# ── scan_workspace ──────────────────────────────────────────────────


def _make_workspace(tmp_path: Path) -> tuple[Path, Path]:
    """Build minimal FCoP workspace skeleton for scan_workspace tests."""
    project_root = tmp_path / "proj"
    workspace = project_root / "docs" / "agents"
    for sub in ("tasks", "reports", "reviews", "issues",
                "log/tasks", "log/reports", "log/reviews"):
        (workspace / sub).mkdir(parents=True, exist_ok=True)
    (project_root / "fcop.json").write_text(
        json.dumps({"team": "x", "roles": ["ME", "ADMIN"], "leader": "ADMIN"}),
        encoding="utf-8",
    )
    return project_root, workspace


def _write_task(
    workspace: Path,
    *,
    name: str = "TASK-20260509-001-ADMIN-to-ME.md",
    status: str | None = None,
    archived: bool = False,
) -> Path:
    fm_lines = ["---", "protocol: fcop", "version: 1", "type: TASK",
                "sender: ADMIN", "recipient: ME", "priority: P1",
                "subject: smoke"]
    if status:
        fm_lines.append(f"status: {status}")
    fm_lines.append("---")
    body = "\n".join(fm_lines) + "\n\nbody\n"
    target = workspace / ("log/tasks" if archived else "tasks") / name
    target.write_text(body, encoding="utf-8")
    return target


def _write_report(
    workspace: Path,
    *,
    name: str = "REPORT-20260509-001-ME-to-ADMIN.md",
    status: str = "done",
    ref_task: str = "TASK-20260509-001",
    archived: bool = False,
) -> Path:
    fm = "\n".join([
        "---", "protocol: fcop", "version: 1", "type: REPORT",
        "sender: ME", "recipient: ADMIN", f"ref_task: {ref_task}",
        f"status: {status}", "---",
    ])
    target = workspace / ("log/reports" if archived else "reports") / name
    target.write_text(fm + "\n\nbody\n", encoding="utf-8")
    return target


def _write_review(
    workspace: Path,
    *,
    name: str = "REVIEW-20260509-001-ME-on-task-001.md",
    decision: str = "approved",
) -> Path:
    fm = "\n".join([
        "---", "protocol: fcop", "version: 1", "type: REVIEW",
        "sender: ME", "reviewer_role: ME",
        "subject_type: task", "subject_ref: TASK-20260509-001",
        f"decision: {decision}", "---",
    ])
    target = workspace / "reviews" / name
    target.write_text(fm + "\n\nbody\n", encoding="utf-8")
    return target


class TestScanWorkspace:
    def test_empty_workspace(self, tmp_path: Path):
        project_root, workspace = _make_workspace(tmp_path)
        state = scan_workspace(workspace, project_root=project_root)
        # 仅含 fcop.json
        assert "fcop.json" in state.files
        assert state.files["fcop.json"].kind == "config"

    def test_scans_task_with_metadata(self, tmp_path: Path):
        project_root, workspace = _make_workspace(tmp_path)
        _write_task(workspace, status="accepted")
        state = scan_workspace(workspace, project_root=project_root)
        relpaths = list(state.files)
        task_paths = [p for p in relpaths if "TASK-" in p]
        assert len(task_paths) == 1
        snap = state.files[task_paths[0]]
        assert snap.kind == "task"
        assert snap.is_archived is False
        assert snap.status == "accepted"
        assert snap.sender == "ADMIN"
        assert snap.recipient == "ME"

    def test_scans_archived_task(self, tmp_path: Path):
        project_root, workspace = _make_workspace(tmp_path)
        _write_task(workspace, archived=True)
        state = scan_workspace(workspace, project_root=project_root)
        archived_snaps = [s for s in state.files.values() if s.kind == "task"]
        assert len(archived_snaps) == 1
        assert archived_snaps[0].is_archived is True

    def test_scans_report_with_ref_task(self, tmp_path: Path):
        project_root, workspace = _make_workspace(tmp_path)
        _write_report(workspace, status="blocked", ref_task="TASK-20260509-099")
        state = scan_workspace(workspace, project_root=project_root)
        report_snaps = [s for s in state.files.values() if s.kind == "report"]
        assert len(report_snaps) == 1
        assert report_snaps[0].status == "blocked"
        assert report_snaps[0].ref_task == "TASK-20260509-099"

    def test_scans_review_with_decision(self, tmp_path: Path):
        project_root, workspace = _make_workspace(tmp_path)
        _write_review(workspace, decision="needs_changes")
        state = scan_workspace(workspace, project_root=project_root)
        review_snaps = [s for s in state.files.values() if s.kind == "review"]
        assert len(review_snaps) == 1
        assert review_snaps[0].decision == "needs_changes"

    def test_scans_config_blob_hash(self, tmp_path: Path):
        project_root, _ws = _make_workspace(tmp_path)
        state = scan_workspace(_ws, project_root=project_root)
        config = state.files["fcop.json"]
        assert config.config_blob_hash is not None
        assert len(config.config_blob_hash) == 16

    def test_ignores_non_envelope_files(self, tmp_path: Path):
        project_root, workspace = _make_workspace(tmp_path)
        (workspace / "tasks" / "README.md").write_text("# readme", encoding="utf-8")
        (workspace / "tasks" / "random.txt").write_text("noise", encoding="utf-8")
        state = scan_workspace(workspace, project_root=project_root)
        kinds = [s.kind for s in state.files.values()]
        assert "other" not in kinds
        # 仅 fcop.json
        assert len(state.files) == 1


# ── compute_diff ────────────────────────────────────────────────────


class TestComputeDiff:
    def test_first_scan_emits_created_for_existing_tasks(self, tmp_path: Path):
        project_root, workspace = _make_workspace(tmp_path)
        _write_task(workspace)
        curr = scan_workspace(workspace, project_root=project_root)
        events = compute_diff(prev=None, curr=curr)
        types = [e.event_type for e in events]
        assert EventType.TASK_CREATED in types

    def test_no_diff_when_state_unchanged(self, tmp_path: Path):
        project_root, workspace = _make_workspace(tmp_path)
        _write_task(workspace)
        s1 = scan_workspace(workspace, project_root=project_root)
        s2 = scan_workspace(workspace, project_root=project_root)
        events = compute_diff(prev=s1, curr=s2)
        assert events == []

    def test_dedup_task_created_across_polls(self, tmp_path: Path):
        """A9：同一文件重复 poll 不重复触发 TASK_CREATED。"""
        project_root, workspace = _make_workspace(tmp_path)
        _write_task(workspace)
        s1 = scan_workspace(workspace, project_root=project_root)
        # 首次 poll：会发 TASK_CREATED
        events_first = compute_diff(prev=None, curr=s1)
        assert any(e.event_type == EventType.TASK_CREATED for e in events_first)
        # 第二次 poll：state 一致，不发
        s2 = scan_workspace(workspace, project_root=project_root)
        events_second = compute_diff(prev=s1, curr=s2)
        assert events_second == []

    def test_report_filed_emits_with_task_id(self, tmp_path: Path):
        project_root, workspace = _make_workspace(tmp_path)
        s1 = scan_workspace(workspace, project_root=project_root)
        _write_report(workspace, ref_task="TASK-20260509-007")
        s2 = scan_workspace(workspace, project_root=project_root)
        events = compute_diff(prev=s1, curr=s2)
        filed = [e for e in events if e.event_type == EventType.REPORT_FILED]
        assert len(filed) == 1
        assert filed[0].subject.get("task_id") == "TASK-20260509-007"

    def test_blocked_status_emits_task_blocked(self, tmp_path: Path):
        project_root, workspace = _make_workspace(tmp_path)
        s1 = scan_workspace(workspace, project_root=project_root)
        _write_report(workspace, status="blocked", ref_task="TASK-20260509-007")
        s2 = scan_workspace(workspace, project_root=project_root)
        events = compute_diff(prev=s1, curr=s2)
        types = [e.event_type for e in events]
        assert EventType.TASK_BLOCKED in types
        assert EventType.REPORT_FILED in types

    def test_review_decided_emits(self, tmp_path: Path):
        project_root, workspace = _make_workspace(tmp_path)
        s1 = scan_workspace(workspace, project_root=project_root)
        _write_review(workspace, decision="approved")
        s2 = scan_workspace(workspace, project_root=project_root)
        events = compute_diff(prev=s1, curr=s2)
        decided = [e for e in events if e.event_type == EventType.REVIEW_DECIDED]
        assert len(decided) == 1
        assert decided[0].subject.get("decision") == "approved"

    def test_role_switched_emits_on_config_change(self, tmp_path: Path):
        project_root, workspace = _make_workspace(tmp_path)
        s1 = scan_workspace(workspace, project_root=project_root)
        # 修改 fcop.json
        (project_root / "fcop.json").write_text(
            json.dumps({"team": "x", "roles": ["ME", "ADMIN", "PM"], "leader": "PM"}),
            encoding="utf-8",
        )
        s2 = scan_workspace(workspace, project_root=project_root)
        events = compute_diff(prev=s1, curr=s2)
        switched = [e for e in events if e.event_type == EventType.ROLE_SWITCHED]
        assert len(switched) == 1
        assert switched[0].subject.get("from") != switched[0].subject.get("to")

    def test_task_completed_when_archived(self, tmp_path: Path):
        project_root, workspace = _make_workspace(tmp_path)
        _write_task(workspace)
        s1 = scan_workspace(workspace, project_root=project_root)
        # 模拟归档：把 task 移到 log/
        original_path = next(
            (workspace / "tasks").iterdir()
        )
        original_path.replace(workspace / "log" / "tasks" / original_path.name)
        s2 = scan_workspace(workspace, project_root=project_root)
        events = compute_diff(prev=s1, curr=s2)
        completed = [e for e in events if e.event_type == EventType.TASK_COMPLETED]
        assert len(completed) == 1

    def test_events_sorted_stable(self, tmp_path: Path):
        project_root, workspace = _make_workspace(tmp_path)
        s1 = scan_workspace(workspace, project_root=project_root)
        # 写多个文件以触发多个事件
        _write_task(workspace, name="TASK-20260509-001-ADMIN-to-ME.md")
        _write_report(workspace, ref_task="TASK-20260509-002")
        _write_review(workspace)
        s2 = scan_workspace(workspace, project_root=project_root)
        events = compute_diff(prev=s1, curr=s2)
        # 确保排序稳定
        events_again = compute_diff(prev=s1, curr=s2)
        assert [e.event_id for e in events] == [e.event_id for e in events_again]
