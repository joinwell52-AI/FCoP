"""Tests for :meth:`fcop.Project.role_occupancy`.

The method drives the "Role occupancy" section of `fcop_report()`'s
UNBOUND output (since ``fcop_protocol_version: 1.5.0`` / fcop-mcp
0.7.0). Backs the protocol's UNBOUND step 4: an agent compares the
assigned role's occupancy state against `last_session_id` *before*
transitioning to BOUND so two sessions can never both be "ME".

See ISSUE-20260427-002-ME for the bug class this method exists to
defend against.
"""

from __future__ import annotations

from pathlib import Path

from fcop import Project


def _init_solo(tmp_path: Path) -> Project:
    project = Project(tmp_path)
    project.init_solo(role_code="ME", lang="en")
    return project


def _init_team(tmp_path: Path) -> Project:
    project = Project(tmp_path)
    project.init(team="dev-team", lang="en", deploy_rules=False)
    return project


class TestRoleOccupancyBasics:
    def test_uninitialized_project_returns_empty_tuple(
        self, tmp_path: Path
    ) -> None:
        project = Project(tmp_path)
        assert project.role_occupancy() == ()

    def test_freshly_initialized_solo_has_unused_status(
        self, tmp_path: Path
    ) -> None:
        project = _init_solo(tmp_path)
        occupancy = project.role_occupancy()
        assert len(occupancy) == 1
        me = occupancy[0]
        assert me.role == "ME"
        assert me.status == "UNUSED"
        assert me.open_tasks == 0
        assert me.open_reports == 0
        assert me.open_issues == 0
        assert me.archived_tasks == 0
        assert me.last_seen_at is None
        assert me.last_session_id is None

    def test_team_init_lists_all_roles_in_config_order(
        self, tmp_path: Path
    ) -> None:
        project = _init_team(tmp_path)
        occupancy = project.role_occupancy()
        # dev-team has 4 roles; preserve their order from fcop.json.
        config_roles = list(project.config.roles)
        observed_roles = [o.role for o in occupancy]
        assert observed_roles == config_roles


class TestRoleOccupancyActiveStatus:
    def test_open_task_marks_both_endpoints_active(
        self, tmp_path: Path
    ) -> None:
        # ADMIN is reserved (never an agent), so the only role that
        # gets ACTIVE here is the recipient PM.
        project = _init_team(tmp_path)
        project.write_task(
            sender="ADMIN", recipient="PM", priority="P2",
            subject="x", body="y",
        )
        occupancy = {o.role: o for o in project.role_occupancy()}
        assert occupancy["PM"].status == "ACTIVE"
        assert occupancy["PM"].open_tasks == 1
        assert occupancy["DEV"].status == "UNUSED"

    def test_archived_task_demotes_to_archived_status(
        self, tmp_path: Path
    ) -> None:
        project = _init_team(tmp_path)
        task = project.write_task(
            sender="ADMIN", recipient="PM", priority="P2",
            subject="x", body="y",
        )
        project.archive_task(task.task_id)
        occupancy = {o.role: o for o in project.role_occupancy()}
        # No active files → ACTIVE drops to ARCHIVED, but counts move
        # into ``archived_tasks``. Previous state must be visible.
        assert occupancy["PM"].status == "ARCHIVED"
        assert occupancy["PM"].open_tasks == 0
        assert occupancy["PM"].archived_tasks == 1


class TestRoleOccupancySessionAttribution:
    def test_last_session_id_picked_from_frontmatter(
        self, tmp_path: Path
    ) -> None:
        # Manually plant a task with a session_id frontmatter field
        # so role_occupancy can pick it up. In production code this
        # is written by `init_solo` / `write_task` flows that include
        # the field on the writer side; here we simulate the on-disk
        # ledger directly to keep the test minimal.
        project = _init_solo(tmp_path)
        task_path = (
            project.tasks_dir / "TASK-20260427-001-ADMIN-to-ME.md"
        )
        task_path.write_text(
            "---\n"
            "protocol: fcop\n"
            "version: 0.6\n"
            "sender: ADMIN\n"
            "recipient: ME\n"
            "priority: P2\n"
            "subject: hello\n"
            "session_id: sess-test-abc\n"
            "---\n"
            "\nbody\n",
            encoding="utf-8",
        )
        occupancy = project.role_occupancy()
        me = next(o for o in occupancy if o.role == "ME")
        assert me.status == "ACTIVE"
        assert me.last_session_id == "sess-test-abc"
        assert me.last_seen_at is not None


class TestRoleOccupancyGhostRoles:
    def test_role_in_ledger_but_not_in_fcop_json_is_surfaced(
        self, tmp_path: Path
    ) -> None:
        # If the team config changes (e.g. an old role was removed)
        # but on-disk files still mention the old role code, ADMIN
        # should still see those rows so they can spot the
        # cross-version mess. Reserved roles (ADMIN, SYSTEM) are not
        # ghost-listed because they cannot be agent-bound anyway.
        project = _init_solo(tmp_path)
        ghost_path = (
            project.tasks_dir / "TASK-20260427-001-ME-to-OLDROLE.md"
        )
        ghost_path.write_text(
            "---\n"
            "protocol: fcop\n"
            "version: 0.6\n"
            "sender: ME\n"
            "recipient: OLDROLE\n"
            "priority: P2\n"
            "subject: stale\n"
            "---\n"
            "\nbody\n",
            encoding="utf-8",
        )
        occupancy = {o.role: o for o in project.role_occupancy()}
        # ME (declared) and OLDROLE (ghost) both show up.
        assert "ME" in occupancy
        assert "OLDROLE" in occupancy
        assert occupancy["OLDROLE"].open_tasks == 1
        # ADMIN never shown — it is a reserved sender, not a role.
        assert "ADMIN" not in occupancy
