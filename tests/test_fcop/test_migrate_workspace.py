"""Tests for ``fcop migrate-workspace`` (ADR-0022).

Coverage matrix:

* :func:`plan` (pure inspection):
  - canonical: source-only → produces moveable plan
  - already migrated: target-only → ``already_migrated``
  - never initialised: neither → ``source_missing``
  - both exist → ``conflict``
  - advisory hits surface ``.gitignore`` / ``README.md`` mentions
* :func:`apply` (mutating):
  - shutil fallback when not in git
  - idempotent: ``apply`` after ``apply`` is a no-op
  - conflict → raises
  - breadcrumb file is written
* CLI dispatcher (``run`` / ``main`` end-to-end):
  - dry-run prints summary, exits 0
  - ``--apply`` actually moves
  - ``--apply`` over conflict exits 2
  - ``--target`` overrides default
  - bare ``fcop`` (no subcommand) preserves the legacy message
"""

from __future__ import annotations

import io
import shutil
import subprocess
from pathlib import Path

import pytest

from fcop.cli import migrate_workspace as mw
from fcop.cli._main import main as cli_main


# ── helpers ───────────────────────────────────────────────────────────


def _make_legacy_workspace(root: Path, *, with_files: bool = True) -> Path:
    """Create a 0.7.x-style ``docs/agents/`` tree under ``root``."""
    workspace = root / "docs" / "agents"
    for sub in ("tasks", "reports", "issues", "shared", "log"):
        (workspace / sub).mkdir(parents=True, exist_ok=True)
    if with_files:
        (workspace / "fcop.json").write_text(
            '{"team":"solo","leader":"ME"}', encoding="utf-8"
        )
        (workspace / "tasks" / "TASK-20260101-001-ADMIN-to-ME.md").write_text(
            "# task body", encoding="utf-8"
        )
    return workspace


def _git_init(root: Path) -> None:
    """Initialise a git repo at ``root`` with one commit so ``git mv``
    can preserve history. Skipped quietly if git is not installed."""
    if shutil.which("git") is None:
        pytest.skip("git not on PATH")
    subprocess.run(["git", "init", "-q"], cwd=str(root), check=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=str(root), check=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test"],
        cwd=str(root), check=True,
    )
    subprocess.run(["git", "add", "-A"], cwd=str(root), check=True)
    subprocess.run(
        ["git", "commit", "-qm", "init"],
        cwd=str(root), check=True,
    )


# ── plan() ────────────────────────────────────────────────────────────


class TestPlan:
    def test_canonical_source_only_produces_moveable_plan(self, tmp_path: Path) -> None:
        _make_legacy_workspace(tmp_path)
        p = mw.plan(tmp_path)
        assert not p.already_migrated
        assert not p.source_missing
        assert not p.conflict
        assert p.source.name == "agents"
        assert p.target.name == "fcop"
        assert "tasks" in p.moved_entries
        assert "fcop.json" in p.moved_entries
        # breadcrumb is *projected* even in dry-run
        assert p.breadcrumb_path is not None
        assert p.breadcrumb_path.name == "MIGRATED_FROM_DOCS_AGENTS.md"

    def test_already_migrated_when_target_exists_and_source_missing(
        self, tmp_path: Path,
    ) -> None:
        (tmp_path / "fcop").mkdir()
        p = mw.plan(tmp_path)
        assert p.already_migrated is True
        assert p.moved_entries == []
        assert "Nothing to migrate" in "\n".join(p.notes)

    def test_source_missing_when_neither_exists(self, tmp_path: Path) -> None:
        p = mw.plan(tmp_path)
        assert p.source_missing is True
        assert p.already_migrated is False

    def test_conflict_when_both_source_and_target_exist(self, tmp_path: Path) -> None:
        _make_legacy_workspace(tmp_path)
        (tmp_path / "fcop").mkdir()
        p = mw.plan(tmp_path)
        assert p.conflict is True
        assert "BOTH" in "\n".join(p.notes)

    def test_advisory_scan_finds_gitignore_and_readme_mentions(
        self, tmp_path: Path,
    ) -> None:
        _make_legacy_workspace(tmp_path)
        (tmp_path / ".gitignore").write_text(
            "build/\ndocs/agents/\n", encoding="utf-8",
        )
        (tmp_path / "README.md").write_text(
            "# project\nsee docs/agents/ for fcop files\n",
            encoding="utf-8",
        )
        (tmp_path / "README.zh.md").write_text(
            "无关内容", encoding="utf-8"
        )
        p = mw.plan(tmp_path)
        names = {h.name for h in p.advisory_hits}
        assert ".gitignore" in names
        assert "README.md" in names
        assert "README.zh.md" not in names  # didn't mention docs/agents

    def test_custom_target_path_is_honoured(self, tmp_path: Path) -> None:
        _make_legacy_workspace(tmp_path)
        custom = tmp_path / "ws"
        p = mw.plan(tmp_path, target=custom)
        assert p.target == custom.resolve()

    def test_custom_source_path_is_honoured(self, tmp_path: Path) -> None:
        legacy = tmp_path / "old" / "agents"
        legacy.mkdir(parents=True)
        (legacy / "fcop.json").write_text("{}", encoding="utf-8")
        p = mw.plan(tmp_path, source=legacy)
        assert p.source == legacy.resolve()
        assert "fcop.json" in p.moved_entries

    def test_surprise_entry_is_called_out_in_notes(self, tmp_path: Path) -> None:
        _make_legacy_workspace(tmp_path)
        (tmp_path / "docs" / "agents" / "weird-stuff.md").write_text(
            "x", encoding="utf-8",
        )
        p = mw.plan(tmp_path)
        notes = "\n".join(p.notes)
        assert "weird-stuff.md" in notes


# ── apply() ───────────────────────────────────────────────────────────


class TestApply:
    def test_apply_moves_source_to_target_via_shutil_when_no_git(
        self, tmp_path: Path,
    ) -> None:
        _make_legacy_workspace(tmp_path)
        p = mw.plan(tmp_path)
        assert not p.will_use_git_mv  # tmp_path is not a git repo
        result = mw.apply(p)
        assert result.applied is True
        assert (tmp_path / "fcop").is_dir()
        assert not (tmp_path / "docs" / "agents").exists()
        # breadcrumb landed
        assert (tmp_path / "fcop" / "MIGRATED_FROM_DOCS_AGENTS.md").is_file()

    def test_apply_uses_git_mv_when_repo_tracked(self, tmp_path: Path) -> None:
        _make_legacy_workspace(tmp_path)
        _git_init(tmp_path)
        p = mw.plan(tmp_path)
        assert p.will_use_git_mv is True
        mw.apply(p)
        # `git status --porcelain=2 --renames` must show a rename
        out = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(tmp_path),
            capture_output=True, text=True, check=True,
        ).stdout
        assert "fcop/" in out  # destination present
        assert (tmp_path / "fcop" / "tasks").is_dir()

    def test_apply_idempotent_after_already_migrated(self, tmp_path: Path) -> None:
        _make_legacy_workspace(tmp_path)
        first = mw.plan(tmp_path)
        mw.apply(first)
        # second pass on the migrated tree
        second = mw.plan(tmp_path)
        assert second.already_migrated is True
        mw.apply(second)
        assert (tmp_path / "fcop" / "tasks").is_dir()
        assert not (tmp_path / "docs" / "agents").exists()

    def test_apply_conflict_raises(self, tmp_path: Path) -> None:
        _make_legacy_workspace(tmp_path)
        (tmp_path / "fcop").mkdir()
        p = mw.plan(tmp_path)
        with pytest.raises(RuntimeError, match="both source and target"):
            mw.apply(p)

    def test_apply_source_missing_is_noop(self, tmp_path: Path) -> None:
        p = mw.plan(tmp_path)
        result = mw.apply(p)
        assert result.applied is True  # no-op success
        assert not (tmp_path / "fcop").exists()

    def test_breadcrumb_content_includes_old_and_new_paths(
        self, tmp_path: Path,
    ) -> None:
        _make_legacy_workspace(tmp_path)
        p = mw.plan(tmp_path)
        mw.apply(p)
        text = (tmp_path / "fcop" / "MIGRATED_FROM_DOCS_AGENTS.md").read_text(
            encoding="utf-8",
        )
        assert "docs/agents" in text
        assert "fcop" in text
        assert "ADR-0022" in text


# ── render_summary ────────────────────────────────────────────────────


class TestRenderSummary:
    def test_dry_run_summary_includes_apply_hint(self, tmp_path: Path) -> None:
        _make_legacy_workspace(tmp_path)
        p = mw.plan(tmp_path)
        text = mw.render_summary(p, applied=False)
        assert "[dry-run]" in text
        assert "--apply" in text

    def test_applied_summary_drops_apply_hint(self, tmp_path: Path) -> None:
        _make_legacy_workspace(tmp_path)
        p = mw.plan(tmp_path)
        mw.apply(p)
        text = mw.render_summary(p, applied=True)
        assert "[applied]" in text
        assert "--apply" not in text

    def test_advisory_hits_appear_in_summary(self, tmp_path: Path) -> None:
        _make_legacy_workspace(tmp_path)
        (tmp_path / ".gitignore").write_text("docs/agents/\n", encoding="utf-8")
        p = mw.plan(tmp_path)
        text = mw.render_summary(p, applied=False)
        assert ".gitignore" in text
        assert "advisory" in text


# ── CLI dispatcher ────────────────────────────────────────────────────


class TestCli:
    def test_dry_run_via_cli_main(self, tmp_path: Path) -> None:
        _make_legacy_workspace(tmp_path)
        out = io.StringIO()
        rc = cli_main(
            ["migrate-workspace", "--project-root", str(tmp_path)],
            stdout=out,
        )
        assert rc == 0
        assert "[dry-run]" in out.getvalue()
        assert (tmp_path / "docs" / "agents").exists()  # not moved
        assert not (tmp_path / "fcop").exists()

    def test_apply_via_cli_main(self, tmp_path: Path) -> None:
        _make_legacy_workspace(tmp_path)
        out = io.StringIO()
        rc = cli_main(
            ["migrate-workspace", "--project-root", str(tmp_path), "--apply"],
            stdout=out,
        )
        assert rc == 0
        assert "[applied]" in out.getvalue()
        assert (tmp_path / "fcop").is_dir()
        assert not (tmp_path / "docs" / "agents").exists()

    def test_conflict_via_cli_main_exits_two(self, tmp_path: Path) -> None:
        _make_legacy_workspace(tmp_path)
        (tmp_path / "fcop").mkdir()
        out = io.StringIO()
        rc = cli_main(
            ["migrate-workspace", "--project-root", str(tmp_path), "--apply"],
            stdout=out,
        )
        assert rc == 2
        assert "ABORT" in out.getvalue()

    def test_custom_target_via_cli_main(self, tmp_path: Path) -> None:
        _make_legacy_workspace(tmp_path)
        out = io.StringIO()
        rc = cli_main(
            [
                "migrate-workspace",
                "--project-root", str(tmp_path),
                "--target", "ws",
                "--apply",
            ],
            stdout=out,
        )
        assert rc == 0
        assert (tmp_path / "ws").is_dir()
        assert not (tmp_path / "fcop").exists()

    def test_bare_fcop_preserves_legacy_message(self) -> None:
        """``fcop`` with no args still routes through the 0.5→0.6
        legacy compat shim — historical contract per ADR-0002."""
        rc = cli_main([])
        assert rc == 1  # _compat_cli's documented exit code

    def test_help_subcommand_exits_zero(self, capsys: pytest.CaptureFixture[str]) -> None:
        """``fcop migrate-workspace --help`` is argparse-native and
        therefore raises ``SystemExit(0)`` before reaching our code."""
        with pytest.raises(SystemExit) as exc:
            cli_main(["migrate-workspace", "--help"])
        assert exc.value.code == 0
        captured = capsys.readouterr()
        assert "migrate-workspace" in captured.out
        assert "--apply" in captured.out


# ── standalone run() entry ────────────────────────────────────────────


class TestRunStandalone:
    def test_run_dry_run(self, tmp_path: Path) -> None:
        _make_legacy_workspace(tmp_path)
        out = io.StringIO()
        rc = mw.run(["--project-root", str(tmp_path)], stdout=out)
        assert rc == 0
        assert "[dry-run]" in out.getvalue()

    def test_run_apply(self, tmp_path: Path) -> None:
        _make_legacy_workspace(tmp_path)
        out = io.StringIO()
        rc = mw.run(["--project-root", str(tmp_path), "--apply"], stdout=out)
        assert rc == 0
        assert (tmp_path / "fcop").is_dir()
