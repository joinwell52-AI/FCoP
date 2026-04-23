"""Tests for :class:`fcop.Project` identity, ``is_initialized``,
``config``, and ``status`` — the D3-c1 surface.

Goals:
    * ``Project(path)`` is side-effect free; the path properties resolve
      to the canonical FCoP layout without touching the disk.
    * ``is_initialized`` is a pure probe for ``fcop.json``.
    * ``config`` parses both 0.6 and legacy 0.5.x ``fcop.json`` shapes
      and raises :class:`ConfigError` on malformed input.
    * ``status`` is safe on empty directories, counts task / report /
      issue files correctly, ignores junk, and orders recent activity
      by mtime descending.

These are integration-style tests against a real ``tmp_path`` — the
pure unit tests for the underlying ``core.config`` parser live
alongside in :mod:`test_core_config`.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import pytest

from fcop import Project
from fcop.errors import ConfigError
from fcop.models import ProjectStatus, TeamConfig

# ── identity / path properties ────────────────────────────────────────


class TestIdentity:
    """Constructing a Project must not touch the filesystem.

    Every path property is a pure string concatenation off ``self._path``
    so callers can inspect intended paths before any init happens.
    """

    def test_construction_is_side_effect_free(self, tmp_path: Path) -> None:
        sub = tmp_path / "nonexistent"
        project = Project(sub)
        assert project.path == sub.resolve()
        assert not sub.exists()

    def test_path_is_resolved(self, tmp_path: Path) -> None:
        # A relative path should be resolved eagerly so later operations
        # aren't sensitive to os.chdir() between calls.
        project = Project(tmp_path / "a" / ".." / "b")
        assert project.path == (tmp_path / "b").resolve()

    def test_canonical_layout(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        root = project.path

        assert project.tasks_dir == root / "docs" / "agents" / "tasks"
        assert project.reports_dir == root / "docs" / "agents" / "reports"
        assert project.issues_dir == root / "docs" / "agents" / "issues"
        assert project.shared_dir == root / "docs" / "agents" / "shared"
        assert project.log_dir == root / "docs" / "agents" / "log"
        assert project.config_path == root / "docs" / "agents" / "fcop.json"


# ── is_initialized ────────────────────────────────────────────────────


class TestIsInitialized:
    """The sole initialization signal is the presence of ``fcop.json``.

    We deliberately *don't* parse it as part of the probe so
    ``is_initialized()`` stays cheap and never raises.
    """

    def test_false_on_empty_root(self, tmp_path: Path) -> None:
        assert Project(tmp_path).is_initialized() is False

    def test_true_when_fcop_json_present(self, tmp_path: Path) -> None:
        cfg_path = tmp_path / "docs" / "agents" / "fcop.json"
        cfg_path.parent.mkdir(parents=True)
        cfg_path.write_text("{}", encoding="utf-8")
        assert Project(tmp_path).is_initialized() is True

    def test_malformed_json_does_not_raise(self, tmp_path: Path) -> None:
        # Sensible agents should be able to *ask* whether init is needed
        # without handling ConfigError just to get a boolean.
        cfg_path = tmp_path / "docs" / "agents" / "fcop.json"
        cfg_path.parent.mkdir(parents=True)
        cfg_path.write_text("not json", encoding="utf-8")
        assert Project(tmp_path).is_initialized() is True

    def test_directory_at_config_path_is_not_init(self, tmp_path: Path) -> None:
        # A directory accidentally named fcop.json shouldn't be mistaken
        # for an initialized project — use is_file() specifically.
        dir_at_cfg = tmp_path / "docs" / "agents" / "fcop.json"
        dir_at_cfg.mkdir(parents=True)
        assert Project(tmp_path).is_initialized() is False


# ── config loading ────────────────────────────────────────────────────


def _write_config(root: Path, payload: dict[str, object]) -> Path:
    """Helper: write *payload* as docs/agents/fcop.json under *root*."""
    path = root / "docs" / "agents" / "fcop.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return path


class TestConfigLoading:
    """``Project.config`` must accept both the 0.6 native shape and the
    legacy 0.5.x shape without information loss."""

    def test_native_preset_shape(self, tmp_path: Path) -> None:
        _write_config(
            tmp_path,
            {
                "mode": "preset",
                "team": "dev-team",
                "leader": "PM",
                "roles": ["PM", "DEV", "QA", "OPS"],
                "lang": "zh",
                "version": 1,
            },
        )
        cfg = Project(tmp_path).config
        assert isinstance(cfg, TeamConfig)
        assert cfg.mode == "preset"
        assert cfg.leader == "PM"
        assert cfg.roles == ("PM", "DEV", "QA", "OPS")
        assert cfg.lang == "zh"
        assert cfg.version == 1
        assert cfg.is_solo is False

    def test_legacy_team_mode_is_normalized_to_preset(
        self, tmp_path: Path
    ) -> None:
        # 0.5.x server.py wrote "mode": "team"; "mode": "preset" is the
        # 0.6 canonical name. Parsing must accept both.
        _write_config(
            tmp_path,
            {
                "mode": "team",
                "team": "dev-team",
                "leader": "PM",
                "roles": [
                    {"code": "PM", "label": "项目经理"},
                    {"code": "DEV", "label": "开发"},
                    {"code": "QA", "label": "测试"},
                    {"code": "OPS", "label": "运维"},
                ],
                "lang": "zh",
            },
        )
        cfg = Project(tmp_path).config
        assert cfg.mode == "preset"
        assert cfg.roles == ("PM", "DEV", "QA", "OPS")
        # Labels from the legacy dict shape should survive in extra so
        # downstream tools can still render them to users.
        assert "_role_labels" in cfg.extra

    def test_solo_mode(self, tmp_path: Path) -> None:
        _write_config(
            tmp_path,
            {
                "mode": "solo",
                "team": "solo",
                "leader": "ME",
                "roles": ["ME"],
                "lang": "en",
            },
        )
        cfg = Project(tmp_path).config
        assert cfg.is_solo is True
        assert cfg.roles == ("ME",)

    def test_missing_file_raises_config_error(self, tmp_path: Path) -> None:
        with pytest.raises(ConfigError) as excinfo:
            _ = Project(tmp_path).config
        # The error should carry the offending path so agents can report
        # it without reimplementing the layout logic.
        assert excinfo.value.path == (
            tmp_path / "docs" / "agents" / "fcop.json"
        )

    def test_malformed_json_raises(self, tmp_path: Path) -> None:
        cfg_path = tmp_path / "docs" / "agents" / "fcop.json"
        cfg_path.parent.mkdir(parents=True)
        cfg_path.write_text("{ not valid", encoding="utf-8")
        with pytest.raises(ConfigError):
            _ = Project(tmp_path).config

    def test_leader_not_in_roles_raises(self, tmp_path: Path) -> None:
        _write_config(
            tmp_path,
            {
                "mode": "preset",
                "team": "dev-team",
                "leader": "MISSING",
                "roles": ["PM", "DEV"],
                "lang": "zh",
            },
        )
        with pytest.raises(ConfigError, match="not listed"):
            _ = Project(tmp_path).config

    def test_invalid_role_code_raises(self, tmp_path: Path) -> None:
        _write_config(
            tmp_path,
            {
                "mode": "preset",
                "team": "dev-team",
                "leader": "pm",  # lowercase — invalid per ROLE_CODE_RE
                "roles": ["pm"],
                "lang": "zh",
            },
        )
        with pytest.raises(ConfigError, match="valid role code"):
            _ = Project(tmp_path).config

    def test_config_is_re_read_on_each_access(self, tmp_path: Path) -> None:
        # The docstring promises no caching; mutate on disk and confirm.
        _write_config(
            tmp_path,
            {
                "mode": "preset",
                "team": "dev-team",
                "leader": "PM",
                "roles": ["PM", "DEV"],
                "lang": "zh",
            },
        )
        project = Project(tmp_path)
        assert project.config.leader == "PM"

        _write_config(
            tmp_path,
            {
                "mode": "preset",
                "team": "dev-team",
                "leader": "DEV",
                "roles": ["PM", "DEV"],
                "lang": "zh",
            },
        )
        assert project.config.leader == "DEV"


# ── status ────────────────────────────────────────────────────────────


def _write(path: Path, content: str = "x") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


class TestStatus:
    """``status()`` should behave on every combination of:
    uninitialized / initialized × empty / populated directories,
    and must ignore files that don't match FCoP filename grammar.
    """

    def test_empty_uninitialized_project(self, tmp_path: Path) -> None:
        status = Project(tmp_path).status()
        assert isinstance(status, ProjectStatus)
        assert status.is_initialized is False
        assert status.config is None
        assert status.tasks_open == 0
        assert status.tasks_archived == 0
        assert status.reports_count == 0
        assert status.issues_count == 0
        assert status.recent_activity == ()
        assert status.path == tmp_path.resolve()

    def test_counts_tasks_reports_and_issues(self, tmp_path: Path) -> None:
        tasks = tmp_path / "docs" / "agents" / "tasks"
        reports = tmp_path / "docs" / "agents" / "reports"
        issues = tmp_path / "docs" / "agents" / "issues"

        _write(tasks / "TASK-20260101-001-ADMIN-to-PM.md")
        _write(tasks / "TASK-20260101-002-PM-to-DEV.md")
        _write(reports / "REPORT-20260101-001-DEV-to-PM.md")
        _write(issues / "ISSUE-20260101-001-QA.md")

        # Non-matching junk must be ignored — drafts, backups, READMEs,
        # subdirectories, and files with wrong prefixes.
        _write(tasks / "DRAFT-whatever.md")
        _write(tasks / "TASK-20260101-001-ADMIN-to-PM.md.bak")
        _write(tasks / "README.md")
        (tasks / "subdir").mkdir()

        status = Project(tmp_path).status()
        assert status.tasks_open == 2
        assert status.reports_count == 1
        assert status.issues_count == 1

    def test_archived_tasks_counted_separately(self, tmp_path: Path) -> None:
        log_tasks = tmp_path / "docs" / "agents" / "log" / "tasks"
        _write(log_tasks / "TASK-20251230-001-ADMIN-to-PM.md")
        _write(log_tasks / "TASK-20251231-001-PM-to-DEV.md")

        status = Project(tmp_path).status()
        assert status.tasks_open == 0
        assert status.tasks_archived == 2

    def test_recent_activity_sorted_newest_first(self, tmp_path: Path) -> None:
        tasks = tmp_path / "docs" / "agents" / "tasks"
        reports = tmp_path / "docs" / "agents" / "reports"
        issues = tmp_path / "docs" / "agents" / "issues"

        # Write in one order, then perturb mtimes so ordering isn't just
        # iteration order.
        t1 = tasks / "TASK-20260101-001-ADMIN-to-PM.md"
        t2 = tasks / "TASK-20260101-002-PM-to-DEV.md"
        r1 = reports / "REPORT-20260101-001-DEV-to-PM.md"
        i1 = issues / "ISSUE-20260101-001-QA.md"
        for path in (t1, t2, r1, i1):
            _write(path)

        now = time.time()
        for path, offset in (
            (t1, -300),  # oldest
            (r1, -200),
            (t2, -100),
            (i1, 0),  # newest
        ):
            import os as _os

            _os.utime(path, (now + offset, now + offset))

        entries = Project(tmp_path).status().recent_activity
        names = [e.filename for e in entries]
        assert names == [i1.name, t2.name, r1.name, t1.name]
        assert [e.kind for e in entries] == ["issue", "task", "report", "task"]

    def test_initialized_status_populates_config(self, tmp_path: Path) -> None:
        _write_config(
            tmp_path,
            {
                "mode": "preset",
                "team": "dev-team",
                "leader": "PM",
                "roles": ["PM", "DEV"],
                "lang": "zh",
            },
        )
        status = Project(tmp_path).status()
        assert status.is_initialized is True
        assert status.config is not None
        assert status.config.leader == "PM"
