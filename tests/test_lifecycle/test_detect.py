"""Tests for fcop.lifecycle.detect — topology classification."""

from __future__ import annotations

from pathlib import Path

import pytest

from fcop.lifecycle.detect import (
    DEFAULT_V2_DIRS,
    Topology,
    detect_topology,
    find_workspace_root,
)
from fcop.lifecycle.state import (
    LIFECYCLE_DIRNAME,
    STAGE_NAMES,
    ensure_lifecycle_dirs,
)


def _make_v2_workspace(tmp_path: Path, *, subdirs: tuple[str, ...] = DEFAULT_V2_DIRS) -> Path:
    ws = tmp_path / "fcop"
    ws.mkdir(parents=True)
    for sub in subdirs:
        (ws / sub).mkdir()
    return ws


def _make_v3_workspace(tmp_path: Path, *, complete: bool = True) -> Path:
    ws = tmp_path / "fcop"
    if complete:
        ensure_lifecycle_dirs(ws)
    else:
        (ws / LIFECYCLE_DIRNAME).mkdir(parents=True)
        # Create only some of the stage subdirs to trigger
        # "incomplete v3" reporting.
        (ws / LIFECYCLE_DIRNAME / STAGE_NAMES[0]).mkdir()
    return ws


class TestFindWorkspaceRoot:
    def test_prefers_fcop_over_docs_agents(self, tmp_path: Path) -> None:
        (tmp_path / "fcop" / "tasks").mkdir(parents=True)
        (tmp_path / "docs" / "agents" / "tasks").mkdir(parents=True)
        ws = find_workspace_root(tmp_path)
        assert ws.name == "fcop"

    def test_falls_back_to_docs_agents_when_no_fcop(self, tmp_path: Path) -> None:
        (tmp_path / "docs" / "agents" / "tasks").mkdir(parents=True)
        ws = find_workspace_root(tmp_path)
        assert ws.relative_to(tmp_path).as_posix() == "docs/agents"

    def test_empty_project_returns_v1_default(self, tmp_path: Path) -> None:
        ws = find_workspace_root(tmp_path)
        assert ws == tmp_path / "fcop"


class TestDetectEmpty:
    def test_empty_root(self, tmp_path: Path) -> None:
        report = detect_topology(tmp_path)
        assert report.topology == Topology.EMPTY
        assert report.v2_dirs_present == ()
        assert report.v3_lifecycle_present is False
        assert report.notes  # non-empty observation

    def test_empty_fcop_dir_only(self, tmp_path: Path) -> None:
        (tmp_path / "fcop").mkdir()
        report = detect_topology(tmp_path)
        assert report.topology == Topology.EMPTY


class TestDetectV2:
    def test_canonical_v2_layout(self, tmp_path: Path) -> None:
        _make_v2_workspace(tmp_path)
        report = detect_topology(tmp_path)
        assert report.topology == Topology.V2
        assert set(report.v2_dirs_present) == set(DEFAULT_V2_DIRS)

    def test_partial_v2_layout_still_detected(self, tmp_path: Path) -> None:
        # Only tasks/ exists — still v2.
        _make_v2_workspace(tmp_path, subdirs=("tasks",))
        report = detect_topology(tmp_path)
        assert report.topology == Topology.V2
        assert report.v2_dirs_present == ("tasks",)

    def test_legacy_docs_agents_layout(self, tmp_path: Path) -> None:
        (tmp_path / "docs" / "agents" / "tasks").mkdir(parents=True)
        (tmp_path / "docs" / "agents" / "log").mkdir(parents=True)
        report = detect_topology(tmp_path)
        assert report.topology == Topology.V2
        assert report.workspace_root.relative_to(tmp_path).as_posix() == "docs/agents"


class TestDetectV3:
    def test_complete_v3_layout(self, tmp_path: Path) -> None:
        _make_v3_workspace(tmp_path, complete=True)
        report = detect_topology(tmp_path)
        assert report.topology == Topology.V3
        assert report.v3_lifecycle_present is True
        assert report.v3_lifecycle_complete is True
        assert report.notes == ()  # no concerns

    def test_incomplete_v3_layout_still_v3(self, tmp_path: Path) -> None:
        _make_v3_workspace(tmp_path, complete=False)
        report = detect_topology(tmp_path)
        assert report.topology == Topology.V3
        assert report.v3_lifecycle_complete is False
        # Should surface a repair hint in notes.
        assert any("missing one or more" in n for n in report.notes)


class TestDetectMixed:
    def test_both_v2_and_v3_marks_mixed(self, tmp_path: Path) -> None:
        ws = _make_v2_workspace(tmp_path)
        ensure_lifecycle_dirs(ws)
        report = detect_topology(tmp_path)
        assert report.topology == Topology.MIXED
        assert report.v3_lifecycle_present is True
        assert set(report.v2_dirs_present) == set(DEFAULT_V2_DIRS)
        # MIXED MUST surface an explicit diagnostic in notes.
        assert any("half-migrated" in n for n in report.notes)


class TestExplicitWorkspace:
    def test_explicit_workspace_bypasses_auto_detect(self, tmp_path: Path) -> None:
        # Auto-detect would pick fcop/ first, but we pass docs/agents/ explicitly.
        (tmp_path / "fcop" / "tasks").mkdir(parents=True)
        (tmp_path / "docs" / "agents" / "tasks").mkdir(parents=True)
        report = detect_topology(
            tmp_path,
            workspace_root=tmp_path / "docs" / "agents",
        )
        assert report.topology == Topology.V2
        assert report.workspace_root.relative_to(tmp_path).as_posix() == "docs/agents"


class TestNeverRaises:
    @pytest.mark.parametrize(
        "factory",
        [
            lambda tp: None,  # bare empty path
            lambda tp: (tp / "fcop").mkdir(),
            lambda tp: _make_v2_workspace(tp),
            lambda tp: _make_v3_workspace(tp),
        ],
    )
    def test_no_exceptions_across_shapes(self, tmp_path: Path, factory) -> None:  # type: ignore[no-untyped-def]
        factory(tmp_path)
        # Must complete without raising for any input shape.
        report = detect_topology(tmp_path)
        assert isinstance(report.topology, Topology)
