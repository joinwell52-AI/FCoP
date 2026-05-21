"""Tests for Project's FCoP 3.0 dual-topology awareness (PR-3a).

Asserts that the Project facade exposes the new v3 properties
(topology / is_v3 / lifecycle_root / inbox_dir / active_dir /
review_dir / done_dir / archive_dir) and that the tasks_dir
compatibility shim returns the correct physical directory on
both v2 and v3 projects.

These tests do NOT exercise write paths — that's PR-3b's territory.
PR-3a is a pure property-level contract.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from fcop import Project
from fcop.lifecycle.state import ensure_lifecycle_dirs


def _seed_v2(tmp_path: Path) -> Path:
    """Build a minimal v2 workspace under tmp_path/fcop/."""
    ws = tmp_path / "fcop"
    (ws / "tasks").mkdir(parents=True)
    (ws / "log" / "tasks").mkdir(parents=True)
    (ws / "reports").mkdir(parents=True)
    (ws / "issues").mkdir(parents=True)
    return tmp_path


def _seed_v3(tmp_path: Path) -> Path:
    """Build a v3 workspace under tmp_path/fcop/."""
    ensure_lifecycle_dirs(tmp_path / "fcop")
    return tmp_path


class TestTopologyProperty:
    def test_empty_project_reports_empty(self, tmp_path: Path) -> None:
        p = Project(tmp_path)
        assert p.topology == "empty"
        assert p.is_v3 is False

    def test_v2_project_reports_v2(self, tmp_path: Path) -> None:
        _seed_v2(tmp_path)
        p = Project(tmp_path)
        assert p.topology == "v2"
        assert p.is_v3 is False

    def test_v3_project_reports_v3(self, tmp_path: Path) -> None:
        _seed_v3(tmp_path)
        p = Project(tmp_path)
        assert p.topology == "v3"
        assert p.is_v3 is True

    def test_mixed_project_reports_mixed_and_not_v3(self, tmp_path: Path) -> None:
        _seed_v2(tmp_path)
        ensure_lifecycle_dirs(tmp_path / "fcop")
        p = Project(tmp_path)
        assert p.topology == "mixed"
        # is_v3 MUST be False in MIXED — we never enforce v3 semantics
        # over an ambiguous tree.
        assert p.is_v3 is False

    def test_topology_report_exposes_notes(self, tmp_path: Path) -> None:
        _seed_v3(tmp_path, )  # complete v3 — no notes expected
        p = Project(tmp_path)
        assert p.topology_report.topology.value == "v3"
        assert p.topology_report.notes == ()


class TestLifecycleProperties:
    def test_lifecycle_root_path(self, tmp_path: Path) -> None:
        p = Project(tmp_path)
        # Always resolvable even on empty projects.
        assert p.lifecycle_root == p.workspace_dir / "_lifecycle"

    @pytest.mark.parametrize(
        ("name", "stage"),
        [
            ("inbox_dir", "inbox"),
            ("active_dir", "active"),
            ("review_dir", "review"),
            ("done_dir", "done"),
            ("archive_dir", "archive"),
        ],
    )
    def test_five_stage_dirs(self, tmp_path: Path, name: str, stage: str) -> None:
        p = Project(tmp_path)
        assert getattr(p, name) == p.workspace_dir / "_lifecycle" / stage


class TestTasksDirCompatibilityShim:
    """Q1 = a · tasks_dir transparently retargets on v3 projects.

    CodeFlow and any other v2-era caller continues to read
    project.tasks_dir; the right physical directory is returned.
    """

    def test_v2_tasks_dir_unchanged(self, tmp_path: Path) -> None:
        _seed_v2(tmp_path)
        p = Project(tmp_path)
        assert p.tasks_dir == p.workspace_dir / "tasks"
        assert p.tasks_dir.is_dir()  # the seed actually created it

    def test_v3_tasks_dir_redirects_to_inbox(self, tmp_path: Path) -> None:
        _seed_v3(tmp_path)
        p = Project(tmp_path)
        # The shim: tasks_dir on a v3 project points to inbox_dir.
        assert p.tasks_dir == p.inbox_dir
        assert p.tasks_dir == p.workspace_dir / "_lifecycle" / "inbox"

    def test_v3_tasks_dir_does_not_raise(self, tmp_path: Path) -> None:
        """Even before _lifecycle/inbox/ physically exists, the
        path must be resolvable (callers may construct the path
        first and create the directory second)."""
        # Workspace doesn't even exist yet.
        p = Project(tmp_path)
        # Empty topology → tasks_dir still returns the v2 path
        # (no v3 evidence on disk).
        assert p.tasks_dir == p.workspace_dir / "tasks"

    def test_mixed_tasks_dir_falls_back_to_v2(self, tmp_path: Path) -> None:
        """MIXED is NOT is_v3 — the shim must return the v2 path
        so legacy reads still hit the real (mixed) tree."""
        _seed_v2(tmp_path)
        ensure_lifecycle_dirs(tmp_path / "fcop")
        p = Project(tmp_path)
        assert p.tasks_dir == p.workspace_dir / "tasks"


class TestBackwardCompatibility:
    """The PR-3a change MUST NOT alter behaviour on v2 projects."""

    def test_v2_reports_dir_unchanged(self, tmp_path: Path) -> None:
        _seed_v2(tmp_path)
        p = Project(tmp_path)
        assert p.reports_dir == p.workspace_dir / "reports"

    def test_v2_issues_dir_unchanged(self, tmp_path: Path) -> None:
        _seed_v2(tmp_path)
        p = Project(tmp_path)
        assert p.issues_dir == p.workspace_dir / "issues"

    def test_v2_log_dir_unchanged(self, tmp_path: Path) -> None:
        _seed_v2(tmp_path)
        p = Project(tmp_path)
        assert p.log_dir == p.workspace_dir / "log"

    def test_v2_workspace_layout_still_v1(self, tmp_path: Path) -> None:
        _seed_v2(tmp_path)
        p = Project(tmp_path)
        # PR-3a does not touch workspace_layout — that's the v1 vs
        # legacy (docs/agents) discriminator from ADR-0022.
        assert p.workspace_layout == "v1"

    def test_v3_workspace_layout_still_v1(self, tmp_path: Path) -> None:
        """Same workspace_layout, different topology. They're
        independent axes:
          - workspace_layout = "v1" / "legacy" / "explicit"
          - topology         = "empty" / "v2" / "v3" / "mixed"
        """
        _seed_v3(tmp_path)
        p = Project(tmp_path)
        assert p.workspace_layout == "v1"
        assert p.topology == "v3"
