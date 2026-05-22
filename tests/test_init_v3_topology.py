"""FCoP 3.0 init topology compliance tests.

Covers TASK-20260522-004: every fresh ``init_*`` MUST land the v3
``_lifecycle/{inbox,active,review,done,archive}/`` topology plus the
retained v2 buckets ``reports/`` ``issues/`` ``shared/``, and MUST NOT
re-create the superseded v2 buckets ``tasks/`` and ``log/`` (per
spec §1.1 / §6).

These tests exist because 3.0.0 / 3.0.1 ``Project._apply_init`` only
created the v2 five-bucket layout — every v3 fresh-init project was
silently non-compliant with the spec it shipped with. Fixed in 3.0.2.
"""

from __future__ import annotations

from pathlib import Path

from fcop import Project

V3_BUCKETS = ("inbox", "active", "review", "done", "archive")
V3_RETAINED = ("reports", "issues", "shared")
V2_SUPERSEDED = ("tasks", "log")


def _assert_v3_topology(project: Project) -> None:
    """Assert ``project`` has the canonical v3 layout on disk."""
    workspace = project._workspace_root  # noqa: SLF001 — test-only.
    lifecycle = workspace / "_lifecycle"
    assert lifecycle.is_dir(), f"missing {lifecycle}"
    for bucket in V3_BUCKETS:
        assert (lifecycle / bucket).is_dir(), (
            f"v3 bucket missing: _lifecycle/{bucket}/"
        )
    for retained in V3_RETAINED:
        assert (workspace / retained).is_dir(), (
            f"retained v2 bucket missing: {retained}/"
        )
    for superseded in V2_SUPERSEDED:
        assert not (workspace / superseded).exists(), (
            f"superseded v2 bucket should not be created: {superseded}/"
        )


# ── init_solo ─────────────────────────────────────────────────────────


def test_init_solo_creates_lifecycle(tmp_path: Path) -> None:
    project = Project(tmp_path)
    project.init_solo(role_code="ME")
    _assert_v3_topology(project)


def test_init_solo_marks_project_v3(tmp_path: Path) -> None:
    project = Project(tmp_path)
    project.init_solo(role_code="ME")
    assert project.is_v3 is True


# ── init_project (preset team) ────────────────────────────────────────


def test_init_project_creates_lifecycle(tmp_path: Path) -> None:
    project = Project(tmp_path)
    project.init(team="dev-team")
    _assert_v3_topology(project)


def test_init_project_marks_project_v3(tmp_path: Path) -> None:
    project = Project(tmp_path)
    project.init(team="dev-team")
    assert project.is_v3 is True


# ── init_custom ───────────────────────────────────────────────────────


def _init_custom(project: Project) -> None:
    project.init_custom(
        team_name="custom-team",
        roles=["PM", "DEV"],
        leader="PM",
    )


def test_init_custom_team_creates_lifecycle(tmp_path: Path) -> None:
    project = Project(tmp_path)
    _init_custom(project)
    _assert_v3_topology(project)


def test_init_custom_marks_project_v3(tmp_path: Path) -> None:
    project = Project(tmp_path)
    _init_custom(project)
    assert project.is_v3 is True


# ── tasks_dir resolution after v3 init ────────────────────────────────


def test_tasks_dir_resolves_to_lifecycle_inbox_after_init(
    tmp_path: Path,
) -> None:
    """``project.tasks_dir`` must follow the v3 contract: a fresh
    ``init_*`` makes it resolve to ``_lifecycle/inbox/``, never the
    deprecated ``tasks/``."""
    project = Project(tmp_path)
    project.init_solo(role_code="ME")
    expected = project._workspace_root / "_lifecycle" / "inbox"  # noqa: SLF001
    assert project.tasks_dir == expected
    assert project.tasks_dir.is_dir()
