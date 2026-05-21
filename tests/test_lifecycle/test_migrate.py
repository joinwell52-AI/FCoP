"""Tests for fcop.lifecycle.migrate — v2 → v3 migration engine."""

from __future__ import annotations

from pathlib import Path

import pytest

from fcop.lifecycle.detect import Topology, detect_topology
from fcop.lifecycle.events import read_events
from fcop.lifecycle.migrate import (
    apply,
    plan,
    render_summary,
)
from fcop.lifecycle.state import LIFECYCLE_DIRNAME, Stage

# ── fixtures / helpers ──


def _seed_v2_project(
    tmp_path: Path,
    *,
    open_tasks: int = 0,
    archived_tasks: int = 0,
    archived_reports: int = 0,
    archived_issues: int = 0,
) -> Path:
    """Build a synthetic v2 project layout under ``tmp_path``."""
    ws = tmp_path / "fcop"
    (ws / "tasks").mkdir(parents=True)
    (ws / "log" / "tasks").mkdir(parents=True)
    (ws / "log" / "reports").mkdir(parents=True)
    (ws / "log" / "issues").mkdir(parents=True)
    (ws / "reports").mkdir(parents=True)
    (ws / "issues").mkdir(parents=True)
    (ws / "shared").mkdir(parents=True)

    def _write(p: Path, kind: str) -> None:
        p.write_text(
            f"---\nprotocol: fcop\nversion: 2\ntype: {kind}\n---\nbody\n",
            encoding="utf-8",
        )

    for i in range(open_tasks):
        _write(ws / "tasks" / f"TASK-2026-{i:03d}.md", "TASK")
    for i in range(archived_tasks):
        _write(ws / "log" / "tasks" / f"TASK-old-{i:03d}.md", "TASK")
    for i in range(archived_reports):
        _write(ws / "log" / "reports" / f"REPORT-{i:03d}.md", "REPORT")
    for i in range(archived_issues):
        _write(ws / "log" / "issues" / f"ISSUE-{i:03d}.md", "ISSUE")

    return tmp_path


class TestPlan:
    def test_empty_project_is_noop(self, tmp_path: Path) -> None:
        p = plan(tmp_path)
        assert p.topology_before.topology == Topology.EMPTY
        assert p.is_noop
        assert p.moves == []

    def test_already_v3_is_noop(self, tmp_path: Path) -> None:
        from fcop.lifecycle.state import ensure_lifecycle_dirs

        ensure_lifecycle_dirs(tmp_path / "fcop")
        p = plan(tmp_path)
        assert p.topology_before.topology == Topology.V3
        assert p.is_noop

    def test_mixed_topology_is_planned_noop(self, tmp_path: Path) -> None:
        from fcop.lifecycle.state import ensure_lifecycle_dirs

        _seed_v2_project(tmp_path, open_tasks=1)
        ensure_lifecycle_dirs(tmp_path / "fcop")
        p = plan(tmp_path)
        assert p.topology_before.topology == Topology.MIXED
        assert p.is_noop  # planner refuses to move anything in MIXED
        assert any("MIXED" in note for note in p.notes)

    def test_v2_project_yields_correct_moves(self, tmp_path: Path) -> None:
        _seed_v2_project(
            tmp_path,
            open_tasks=2,
            archived_tasks=3,
            archived_reports=1,
            archived_issues=1,
        )
        p = plan(tmp_path)
        assert p.topology_before.topology == Topology.V2
        assert len(p.moves) == 2 + 3 + 1 + 1

        by_stage: dict[str | None, int] = {}
        for m in p.moves:
            key = m.target_stage.value if m.target_stage else None
            by_stage[key] = by_stage.get(key, 0) + 1
        assert by_stage[Stage.INBOX.value] == 2
        assert by_stage[Stage.ARCHIVE.value] == 3
        assert by_stage[None] == 2  # reports + issues

    def test_plan_destinations_are_correct(self, tmp_path: Path) -> None:
        _seed_v2_project(tmp_path, open_tasks=1, archived_tasks=1)
        p = plan(tmp_path)
        dests = {m.destination.relative_to(tmp_path).as_posix() for m in p.moves}
        assert any(d.startswith("fcop/_lifecycle/inbox/") for d in dests)
        assert any(d.startswith("fcop/_lifecycle/archive/") for d in dests)

    def test_log_will_be_removed_when_fully_drained(self, tmp_path: Path) -> None:
        _seed_v2_project(
            tmp_path,
            archived_tasks=1,
            archived_reports=1,
            archived_issues=1,
        )
        p = plan(tmp_path)
        assert p.empty_log_will_be_removed is True

    def test_log_not_removed_with_unexpected_children(self, tmp_path: Path) -> None:
        _seed_v2_project(tmp_path, archived_tasks=1)
        # Drop an unexpected stray under log/ that the migrator
        # does not know how to move.
        stray = tmp_path / "fcop" / "log" / "weird.txt"
        stray.write_text("not a TASK", encoding="utf-8")
        p = plan(tmp_path)
        assert p.empty_log_will_be_removed is False
        assert any("unexpected children" in n for n in p.notes)


class TestApply:
    def test_refuses_mixed(self, tmp_path: Path) -> None:
        from fcop.lifecycle.state import ensure_lifecycle_dirs

        _seed_v2_project(tmp_path, open_tasks=1)
        ensure_lifecycle_dirs(tmp_path / "fcop")
        p = plan(tmp_path)
        with pytest.raises(RuntimeError, match="MIXED"):
            apply(p)

    def test_noop_apply_is_safe(self, tmp_path: Path) -> None:
        p = plan(tmp_path)
        result = apply(p)
        assert result.applied is True

    def test_v2_to_v3_full_migration(self, tmp_path: Path) -> None:
        _seed_v2_project(
            tmp_path,
            open_tasks=2,
            archived_tasks=2,
            archived_reports=1,
            archived_issues=1,
        )
        p = plan(tmp_path)
        apply(p)

        ws = tmp_path / "fcop"
        # Source files all gone.
        assert list((ws / "tasks").glob("*.md")) == []
        assert not (ws / "log").exists()  # removed because empty

        # Destination files all present.
        inbox = ws / LIFECYCLE_DIRNAME / "inbox"
        archive = ws / LIFECYCLE_DIRNAME / "archive"
        assert len(list(inbox.glob("*.md"))) == 2
        assert len(list(archive.glob("*.md"))) == 2

        # Reports and issues moved to v3 locations.
        assert len(list((ws / "reports").glob("*.md"))) == 1
        assert len(list((ws / "issues").glob("*.md"))) == 1

    def test_baseline_event_stamped_on_lifecycle_files(self, tmp_path: Path) -> None:
        _seed_v2_project(tmp_path, open_tasks=1, archived_tasks=1)
        p = plan(tmp_path)
        apply(p)

        inbox_file = next(
            (tmp_path / "fcop" / LIFECYCLE_DIRNAME / "inbox").glob("*.md")
        )
        events = read_events(inbox_file.read_text(encoding="utf-8"))
        assert len(events) == 1
        assert events[0].tool == "fcop_migrate_v3"
        assert events[0].by == "migration"
        assert events[0].from_stage is None
        assert events[0].to_stage == Stage.INBOX

    def test_no_event_stamped_on_reports(self, tmp_path: Path) -> None:
        _seed_v2_project(tmp_path, archived_reports=1)
        p = plan(tmp_path)
        apply(p)

        report_file = next((tmp_path / "fcop" / "reports").glob("*.md"))
        events = read_events(report_file.read_text(encoding="utf-8"))
        # Reports are not under _lifecycle/; they receive no transition event.
        assert events == []

    def test_idempotent_second_apply_is_noop(self, tmp_path: Path) -> None:
        _seed_v2_project(tmp_path, open_tasks=1, archived_tasks=1)
        apply(plan(tmp_path))
        # Second run sees V3 and refuses to do anything.
        second = plan(tmp_path)
        assert second.topology_before.topology == Topology.V3
        assert second.is_noop
        apply(second)  # must not raise

    def test_post_migration_topology_is_v3(self, tmp_path: Path) -> None:
        _seed_v2_project(tmp_path, open_tasks=1)
        apply(plan(tmp_path))
        report = detect_topology(tmp_path)
        assert report.topology == Topology.V3
        assert report.v3_lifecycle_complete is True


class TestRenderSummary:
    def test_dry_run_includes_hint(self, tmp_path: Path) -> None:
        _seed_v2_project(tmp_path, open_tasks=1)
        out = render_summary(plan(tmp_path), applied=False)
        assert "dry-run" in out
        assert "--apply to execute" in out

    def test_applied_omits_hint(self, tmp_path: Path) -> None:
        _seed_v2_project(tmp_path, open_tasks=1)
        p = plan(tmp_path)
        apply(p)
        out = render_summary(p, applied=True)
        assert "applied" in out
        assert "--apply to execute" not in out

    def test_summary_lists_per_stage_counts(self, tmp_path: Path) -> None:
        _seed_v2_project(tmp_path, open_tasks=2, archived_tasks=3)
        out = render_summary(plan(tmp_path), applied=False)
        assert "inbox" in out
        assert "archive" in out

    def test_noop_summary_is_terse(self, tmp_path: Path) -> None:
        out = render_summary(plan(tmp_path), applied=False)
        assert "no-op" in out
