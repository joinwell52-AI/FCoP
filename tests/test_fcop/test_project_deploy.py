"""Tests for :meth:`fcop.Project.deploy_role_templates` — D5-c3.

The deployment writes the bundled :class:`TeamTemplate` for a team
(both zh and en) into ``docs/agents/shared/``. These tests pin:

    * Layout — which files land where, named correctly.
    * Defaults — team/lang fall back to ``fcop.json`` when not given.
    * force=True — existing files are archived rather than overwritten
      silently; archive layout preserves relative paths.
    * force=False — existing files are skipped, not touched.
    * Report shape — ``DeploymentReport`` carries every path we promised.
    * Error paths — unknown team / unsupported lang / uninitialized project.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from fcop import Project
from fcop.errors import ConfigError, TeamNotFoundError

# ── Shared fixtures ──────────────────────────────────────────────────


@pytest.fixture
def fresh_project(tmp_path: Path) -> Project:
    """An initialized dev-team project at tmp_path."""
    project = Project(tmp_path)
    project.init(team="dev-team", lang="zh")
    return project


# ── Layout + content ─────────────────────────────────────────────────


class TestDeploymentLayout:
    def test_creates_expected_tree(self, fresh_project: Project) -> None:
        report = fresh_project.deploy_role_templates()
        shared = fresh_project.shared_dir

        # Top-level layer-0/1/2 files, both languages.
        expected_top = {
            "TEAM-README.md",
            "TEAM-README.en.md",
            "TEAM-ROLES.md",
            "TEAM-ROLES.en.md",
            "TEAM-OPERATING-RULES.md",
            "TEAM-OPERATING-RULES.en.md",
        }
        actual_top = {p.name for p in shared.iterdir() if p.is_file()}
        assert expected_top.issubset(actual_top)

        # roles/ subdir holds one pair per role.
        roles_dir = shared / "roles"
        assert roles_dir.is_dir()
        info_roles = {"DEV", "OPS", "PM", "QA"}
        for role in info_roles:
            assert (roles_dir / f"{role}.md").is_file()
            assert (roles_dir / f"{role}.en.md").is_file()

        # Every deployed path is absolute + exists + non-empty.
        for path in report.deployed:
            assert path.is_absolute()
            assert path.is_file()
            assert path.stat().st_size > 0

    def test_content_matches_bundled(self, fresh_project: Project) -> None:
        # The deployed TEAM-README.md must be byte-equal to the bundled
        # zh readme — otherwise we're silently mangling content.
        from fcop.teams import get_template

        fresh_project.deploy_role_templates()

        shared = fresh_project.shared_dir
        on_disk_zh = (shared / "TEAM-README.md").read_text(encoding="utf-8")
        bundled_zh = get_template("dev-team", "zh").readme
        assert on_disk_zh == bundled_zh

        on_disk_en = (shared / "TEAM-README.en.md").read_text(encoding="utf-8")
        bundled_en = get_template("dev-team", "en").readme
        assert on_disk_en == bundled_en


# ── Default resolution from config ───────────────────────────────────


class TestDefaults:
    def test_reads_team_from_config(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        project.init(team="qa-team", lang="zh")
        report = project.deploy_role_templates()
        # qa-team roles: LEAD-QA / TESTER / AUTO-TESTER / PERF-TESTER.
        names = {p.name for p in report.deployed}
        assert "LEAD-QA.md" in names
        assert "AUTO-TESTER.md" in names

    def test_explicit_team_overrides_config(
        self, fresh_project: Project
    ) -> None:
        # Project was initialized as dev-team but we deploy qa-team.
        report = fresh_project.deploy_role_templates(team="qa-team")
        names = {p.name for p in report.deployed}
        # qa-team markers present.
        assert "LEAD-QA.md" in names
        # dev-team-specific role absent.
        assert "DEV.md" not in names

    def test_uninitialized_project_requires_explicit_args(
        self, tmp_path: Path
    ) -> None:
        # No fcop.json → ConfigError when team must be read from config.
        project = Project(tmp_path)
        with pytest.raises(ConfigError):
            project.deploy_role_templates()

    def test_uninitialized_project_with_explicit_args_works(
        self, tmp_path: Path
    ) -> None:
        # Explicit team + lang should bypass the config read entirely,
        # so uninitialized projects can still stage templates.
        project = Project(tmp_path)
        report = project.deploy_role_templates(team="dev-team", lang="zh")
        assert len(report.deployed) > 0


# ── Force / skip semantics ───────────────────────────────────────────


class TestForceAndSkip:
    def test_force_archives_existing_file(
        self, fresh_project: Project
    ) -> None:
        shared = fresh_project.shared_dir
        shared.mkdir(parents=True, exist_ok=True)
        (shared / "roles").mkdir(parents=True, exist_ok=True)

        # Plant a stale file that the redeploy will conflict with.
        stale = shared / "TEAM-README.md"
        stale.write_text("# stale content", encoding="utf-8")

        report = fresh_project.deploy_role_templates(force=True)

        # The new file is on disk with bundled content.
        assert stale.read_text(encoding="utf-8") != "# stale content"
        # And the old file is preserved under .fcop/migrations/<ts>/shared/.
        assert report.migration_dir is not None
        archived = report.migration_dir / "TEAM-README.md"
        assert archived.is_file()
        assert archived.read_text(encoding="utf-8") == "# stale content"
        # And it shows up in report.archived.
        assert archived in report.archived

    def test_skip_preserves_existing_file(
        self, fresh_project: Project
    ) -> None:
        shared = fresh_project.shared_dir
        shared.mkdir(parents=True, exist_ok=True)

        # Plant a stale file first.
        stale = shared / "TEAM-README.md"
        stale.write_text("# user-authored content", encoding="utf-8")

        report = fresh_project.deploy_role_templates(force=False)

        # The stale file is untouched.
        assert stale.read_text(encoding="utf-8") == "# user-authored content"
        # And it's recorded as skipped, NOT deployed.
        assert stale in report.skipped
        assert stale not in report.deployed
        # No migration dir since nothing was archived.
        assert report.migration_dir is None

    def test_fresh_project_has_no_skips_or_archives(
        self, fresh_project: Project
    ) -> None:
        # init() creates empty directories; no pre-existing files means
        # a clean deploy: all deployed, nothing skipped or archived.
        report = fresh_project.deploy_role_templates()
        assert report.skipped == ()
        assert report.archived == ()
        assert report.migration_dir is None
        assert len(report.deployed) >= 14  # 6 top-level + 8 per-role


# ── Error paths ──────────────────────────────────────────────────────


class TestErrors:
    def test_unknown_team_raises(self, fresh_project: Project) -> None:
        with pytest.raises(TeamNotFoundError):
            fresh_project.deploy_role_templates(team="nonexistent")

    def test_unsupported_lang_raises(self, fresh_project: Project) -> None:
        with pytest.raises(ValueError, match="unsupported lang"):
            fresh_project.deploy_role_templates(lang="fr")  # type: ignore[arg-type]

    def test_report_tuple_types(self, fresh_project: Project) -> None:
        # The frozen-dataclass contract: deployed/skipped/archived are
        # *tuples*, not lists — callers rely on them being hashable /
        # unchanged across subsequent deploy calls.
        report = fresh_project.deploy_role_templates()
        assert isinstance(report.deployed, tuple)
        assert isinstance(report.skipped, tuple)
        assert isinstance(report.archived, tuple)
