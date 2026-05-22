"""Tests for Project.write_task + archive_task on v3 projects (PR-3b).

Asserts:

* write_task on a v3 project lands the file in _lifecycle/inbox/
  with a create_task transition event stamped in frontmatter.
* archive_task on a v3 project walks the file through the legal
  chain inbox → active → done → archive (or shorter, depending on
  start stage) and the final file holds the complete audit trace.
* v2 behaviour is unchanged on v2 projects.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from fcop import Priority, Project
from fcop.lifecycle.events import read_events
from fcop.lifecycle.migrate import apply as migrate_apply
from fcop.lifecycle.migrate import plan as migrate_plan
from fcop.lifecycle.state import LIFECYCLE_DIRNAME, Stage


def _seed_v2_legacy(tmp_path: Path) -> Project:
    """Build a legacy v2 project (pre-FCoP-3.0).

    Since FCoP 3.0.2, ``Project.init()`` defaults to v3 topology, so
    constructing a v2-shaped project means writing the directory tree
    by hand: the five v2 buckets (``tasks/`` ``reports/`` ``issues/``
    ``shared/`` ``log/``) plus a minimal ``fcop.json``. Used by the
    "v2 behaviour unchanged" regression tests.
    """
    workspace = tmp_path / "fcop"
    workspace.mkdir(parents=True, exist_ok=True)
    for sub in ("tasks", "reports", "issues", "shared", "log"):
        (workspace / sub).mkdir(parents=True, exist_ok=True)
    (workspace / "fcop.json").write_text(
        '{"version": "2.0.0", "mode": "team", "team": "dev-team",'
        ' "team_name": "dev-team", "leader": "PM",'
        ' "roles": [{"code": "PM", "label": "PM"},'
        ' {"code": "DEV", "label": "DEV"}]}',
        encoding="utf-8",
    )
    return Project(tmp_path)


def _seed_v3_initialized(tmp_path: Path) -> Project:
    """Build a v3 project that's also been ``init()``-ed.

    init() always creates the v2 layout (per Q2=b: no automatic
    migration in init). The migrate engine refuses to act on a
    completely empty v2 skeleton ("nothing to move"), so we seed
    one real task file before migrating — that gives plan() real
    moves to compute and apply() real work to do, which in turn
    triggers the post-migration v2-skeleton cleanup that produces
    a pure v3 topology.

    After migration the seed task lives at
    ``_lifecycle/archive/`` (PR-2's synthetic baseline event puts
    pre-existing tasks straight into archive). New tasks created
    via write_task land in inbox/ as expected.
    """
    from fcop.lifecycle.state import ensure_lifecycle_dirs

    p = Project(tmp_path)
    p.init(team="dev-team", lang="en")
    # Drop a single seed file so migrate has something to move.
    seed = p.tasks_dir / "TASK-20260101-001-PM-to-DEV.md"
    seed.write_text(
        "---\nprotocol: fcop\nversion: 2.0.0\n"
        "sender: PM\nrecipient: DEV\npriority: P2\n"
        "subject: seed\n---\nseed body\n",
        encoding="utf-8",
    )
    # plan() takes the *project root* (not workspace); detect_topology
    # walks down to find the workspace internally.
    plan = migrate_plan(tmp_path)
    migrate_apply(plan)
    # Defensive: ensure all 5 lifecycle dirs exist even if the
    # seed task only triggered creation of archive/.
    ensure_lifecycle_dirs(p.workspace_dir)
    return Project(tmp_path)


class TestWriteTaskOnV3:
    def test_lands_in_inbox(self, tmp_path: Path) -> None:
        p = _seed_v3_initialized(tmp_path)
        task = p.write_task(
            sender="PM",
            recipient="DEV",
            priority=Priority.P1,
            subject="test",
            body="body",
        )
        assert task.path.parent.name == "inbox"
        assert task.path.parent.parent.name == LIFECYCLE_DIRNAME

    def test_stamps_creation_event(self, tmp_path: Path) -> None:
        p = _seed_v3_initialized(tmp_path)
        task = p.write_task(
            sender="PM",
            recipient="DEV",
            priority=Priority.P1,
            subject="test",
            body="body",
        )
        events = read_events(task.path.read_text(encoding="utf-8"))
        assert len(events) == 1
        assert events[0].tool == "create_task"
        assert events[0].from_stage is None
        assert events[0].to_stage == Stage.INBOX
        assert events[0].by == "PM"

    def test_v2_write_task_unchanged(self, tmp_path: Path) -> None:
        """v2 projects must not get a transitions: field stamped."""
        # FCoP 3.0.2+: init() now defaults to v3 topology, so we have to
        # build a v2 project by hand to keep this regression alive.
        p = _seed_v2_legacy(tmp_path)
        assert p.is_v3 is False

        task = p.write_task(
            sender="PM",
            recipient="DEV",
            priority=Priority.P1,
            subject="test",
            body="body",
        )
        # v2 file does not get a transition event.
        events = read_events(task.path.read_text(encoding="utf-8"))
        assert events == []


class TestArchiveTaskOnV3:
    def test_inbox_to_archive_full_chain(self, tmp_path: Path) -> None:
        p = _seed_v3_initialized(tmp_path)
        task = p.write_task(
            sender="PM",
            recipient="DEV",
            priority=Priority.P1,
            subject="test",
            body="body",
        )
        archived = p.archive_task(task.filename)
        assert archived.is_archived is True
        assert archived.path.parent.name == "archive"

        events = read_events(archived.path.read_text(encoding="utf-8"))
        # 1 create + 3 chain transitions = 4 events.
        assert len(events) == 4
        assert [e.to_stage for e in events] == [
            Stage.INBOX,
            Stage.ACTIVE,
            Stage.DONE,
            Stage.ARCHIVE,
        ]
        assert [e.tool for e in events] == [
            "create_task",
            "claim_task",
            "finish_task",
            "archive_task",
        ]

    def test_idempotent_on_already_archived(self, tmp_path: Path) -> None:
        p = _seed_v3_initialized(tmp_path)
        task = p.write_task(
            sender="PM",
            recipient="DEV",
            priority=Priority.P1,
            subject="test",
            body="body",
        )
        first = p.archive_task(task.filename)
        second = p.archive_task(task.filename)
        # Second call must find the archived file and return it unchanged.
        assert first.path == second.path
        events_after_second = read_events(second.path.read_text(encoding="utf-8"))
        # Still 4 events — no extra appends on a no-op archive.
        assert len(events_after_second) == 4

    def test_resolve_task_file_scans_all_v3_buckets(self, tmp_path: Path) -> None:
        """Once archived, resolve_task_file must still find the task."""
        p = _seed_v3_initialized(tmp_path)
        task = p.write_task(
            sender="PM",
            recipient="DEV",
            priority=Priority.P1,
            subject="test",
            body="body",
        )
        p.archive_task(task.filename)
        # Resolve by task_id.
        source, archived = p._resolve_task_file(task.task_id)
        assert source is not None
        assert archived is True
        assert source.parent.name == "archive"


class TestV2BehaviourUnchanged:
    def test_archive_task_on_v2_still_uses_log_tasks(self, tmp_path: Path) -> None:
        # FCoP 3.0.2+: init() defaults to v3 — see _seed_v2_legacy comment.
        p = _seed_v2_legacy(tmp_path)
        assert p.is_v3 is False

        task = p.write_task(
            sender="PM",
            recipient="DEV",
            priority=Priority.P1,
            subject="test",
            body="body",
        )
        archived = p.archive_task(task.filename)
        # Classic v2 destination — log/tasks/, NOT _lifecycle/archive/.
        assert archived.path.parent.name == "tasks"
        assert archived.path.parent.parent.name == "log"


class TestErrorPaths:
    def test_archive_unknown_task_raises(self, tmp_path: Path) -> None:
        from fcop import TaskNotFoundError

        p = _seed_v3_initialized(tmp_path)
        with pytest.raises(TaskNotFoundError):
            p.archive_task("TASK-99999999-001")
