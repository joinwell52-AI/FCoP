"""Tests for the ``fcop migrate --to-v3`` CLI subcommand glue."""

from __future__ import annotations

import io
from pathlib import Path

from fcop.cli import migrate_v3
from fcop.cli._main import main as fcop_main


def _seed_v2(tmp_path: Path) -> Path:
    ws = tmp_path / "fcop"
    (ws / "tasks").mkdir(parents=True)
    (ws / "log" / "tasks").mkdir(parents=True)
    (ws / "tasks" / "TASK-x.md").write_text(
        "---\nprotocol: fcop\nversion: 2\ntype: TASK\n---\nbody\n",
        encoding="utf-8",
    )
    return tmp_path


class TestStandaloneRunner:
    def test_dry_run_returns_zero_and_does_not_move(self, tmp_path: Path) -> None:
        _seed_v2(tmp_path)
        out = io.StringIO()
        rc = migrate_v3.run(
            ["--to-v3", "--project-root", str(tmp_path)],
            stdout=out,
        )
        assert rc == 0
        text = out.getvalue()
        assert "dry-run" in text
        # Source file must still be in place.
        assert (tmp_path / "fcop" / "tasks" / "TASK-x.md").exists()

    def test_apply_moves_files(self, tmp_path: Path) -> None:
        _seed_v2(tmp_path)
        out = io.StringIO()
        rc = migrate_v3.run(
            ["--to-v3", "--apply", "--project-root", str(tmp_path)],
            stdout=out,
        )
        assert rc == 0
        assert "applied" in out.getvalue()
        assert not (tmp_path / "fcop" / "tasks" / "TASK-x.md").exists()
        assert (tmp_path / "fcop" / "_lifecycle" / "inbox" / "TASK-x.md").exists()

    def test_apply_on_mixed_returns_2(self, tmp_path: Path) -> None:
        from fcop.lifecycle.state import ensure_lifecycle_dirs

        _seed_v2(tmp_path)
        ensure_lifecycle_dirs(tmp_path / "fcop")
        out = io.StringIO()
        rc = migrate_v3.run(
            ["--to-v3", "--apply", "--project-root", str(tmp_path)],
            stdout=out,
        )
        assert rc == 2
        assert "MIXED" in out.getvalue()

    def test_explicit_workspace_arg(self, tmp_path: Path) -> None:
        # Put the v2 layout under docs/agents/ instead of fcop/ and
        # tell the CLI to use that workspace explicitly.
        ws = tmp_path / "docs" / "agents"
        (ws / "tasks").mkdir(parents=True)
        (ws / "tasks" / "TASK-x.md").write_text(
            "---\nprotocol: fcop\nversion: 2\n---\n",
            encoding="utf-8",
        )
        out = io.StringIO()
        rc = migrate_v3.run(
            [
                "--to-v3",
                "--apply",
                "--project-root",
                str(tmp_path),
                "--workspace",
                "docs/agents",
            ],
            stdout=out,
        )
        assert rc == 0
        assert (
            tmp_path / "docs" / "agents" / "_lifecycle" / "inbox" / "TASK-x.md"
        ).exists()


class TestTopLevelMainIntegration:
    """`fcop migrate --to-v3 ...` through the top-level entry point."""

    def test_dry_run_through_main(self, tmp_path: Path) -> None:
        _seed_v2(tmp_path)
        out = io.StringIO()
        rc = fcop_main(
            ["migrate", "--to-v3", "--project-root", str(tmp_path)],
            stdout=out,
        )
        assert rc == 0
        assert "dry-run" in out.getvalue()

    def test_to_v3_is_required(self, tmp_path: Path) -> None:
        # Missing --to-v3 must cause argparse to error (SystemExit).
        import pytest

        with pytest.raises(SystemExit):
            fcop_main(
                ["migrate", "--project-root", str(tmp_path)],
            )

    def test_migrate_workspace_still_works(self, tmp_path: Path) -> None:
        """Adding `migrate` must not break the existing `migrate-workspace`."""
        # Bare migrate-workspace dry-run on an empty tree should
        # exit cleanly with a "source does not exist" note.
        out = io.StringIO()
        rc = fcop_main(
            ["migrate-workspace", "--project-root", str(tmp_path)],
            stdout=out,
        )
        assert rc == 0
        assert "migrate-workspace" in out.getvalue()
