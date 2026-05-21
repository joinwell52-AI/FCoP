"""Tests for fcop.lifecycle.state — Rule A and the 5-bucket topology."""

from __future__ import annotations

from pathlib import Path

import pytest

from fcop.lifecycle.state import (
    LIFECYCLE_DIRNAME,
    STAGE_NAMES,
    Stage,
    ensure_lifecycle_dirs,
    lifecycle_root,
    same_mount,
    stage_dir,
    stage_of_path,
)


class TestStageEnum:
    def test_five_stages_in_canonical_order(self) -> None:
        assert STAGE_NAMES == ("inbox", "active", "review", "done", "archive")

    def test_stage_str_equality(self) -> None:
        # The str mixin makes Stage.INBOX == "inbox" — important for
        # ergonomic comparisons against on-disk directory names.
        assert Stage.INBOX == "inbox"
        assert Stage.ACTIVE == "active"

    def test_from_dirname_roundtrip(self) -> None:
        for name in STAGE_NAMES:
            assert Stage.from_dirname(name).value == name

    def test_from_dirname_rejects_unknown(self) -> None:
        with pytest.raises(ValueError, match="not a valid FCoP lifecycle stage"):
            Stage.from_dirname("pending")


class TestPathHelpers:
    def test_lifecycle_root(self, tmp_path: Path) -> None:
        assert lifecycle_root(tmp_path) == tmp_path / LIFECYCLE_DIRNAME

    def test_stage_dir(self, tmp_path: Path) -> None:
        assert stage_dir(tmp_path, Stage.ACTIVE) == (
            tmp_path / LIFECYCLE_DIRNAME / "active"
        )

    def test_ensure_lifecycle_dirs_creates_five_subdirs(self, tmp_path: Path) -> None:
        root = ensure_lifecycle_dirs(tmp_path)
        assert root.is_dir()
        for name in STAGE_NAMES:
            assert (root / name).is_dir()

    def test_ensure_lifecycle_dirs_is_idempotent(self, tmp_path: Path) -> None:
        ensure_lifecycle_dirs(tmp_path)
        # Drop a sentinel; a second call must not nuke it.
        sentinel = tmp_path / LIFECYCLE_DIRNAME / "active" / "keep.txt"
        sentinel.write_text("keep", encoding="utf-8")
        ensure_lifecycle_dirs(tmp_path)
        assert sentinel.read_text(encoding="utf-8") == "keep"


class TestStageOfPath:
    """Rule A: the file's enclosing directory is the only state source.

    These tests deliberately do *not* read file contents — they
    construct paths and assert what stage_of_path returns, which is
    the entire point of Rule A.
    """

    def test_file_in_inbox(self, tmp_path: Path) -> None:
        ensure_lifecycle_dirs(tmp_path)
        f = tmp_path / LIFECYCLE_DIRNAME / "inbox" / "TASK-x.md"
        f.write_text("placeholder", encoding="utf-8")
        assert stage_of_path(f, project_root=tmp_path) == Stage.INBOX

    def test_file_in_active(self, tmp_path: Path) -> None:
        ensure_lifecycle_dirs(tmp_path)
        f = tmp_path / LIFECYCLE_DIRNAME / "active" / "TASK-x.md"
        f.write_text("placeholder", encoding="utf-8")
        assert stage_of_path(f, project_root=tmp_path) == Stage.ACTIVE

    def test_file_outside_lifecycle_returns_none(self, tmp_path: Path) -> None:
        ensure_lifecycle_dirs(tmp_path)
        f = tmp_path / "elsewhere.md"
        f.write_text("placeholder", encoding="utf-8")
        assert stage_of_path(f, project_root=tmp_path) is None

    def test_file_under_unknown_lifecycle_subdir_returns_none(
        self, tmp_path: Path
    ) -> None:
        # Someone created _lifecycle/staging/ by mistake. Rule A says
        # only the 5 canonical buckets count.
        weird = tmp_path / LIFECYCLE_DIRNAME / "staging"
        weird.mkdir(parents=True)
        f = weird / "TASK-x.md"
        f.write_text("placeholder", encoding="utf-8")
        assert stage_of_path(f, project_root=tmp_path) is None

    def test_no_project_root_walks_up(self, tmp_path: Path) -> None:
        ensure_lifecycle_dirs(tmp_path)
        f = tmp_path / LIFECYCLE_DIRNAME / "review" / "TASK-x.md"
        f.write_text("placeholder", encoding="utf-8")
        # No project_root argument — function must still resolve via
        # walking parents up.
        assert stage_of_path(f) == Stage.REVIEW

    def test_does_not_read_file(self, tmp_path: Path) -> None:
        """Even if the frontmatter claims a different status, Rule A wins."""
        ensure_lifecycle_dirs(tmp_path)
        f = tmp_path / LIFECYCLE_DIRNAME / "done" / "TASK-x.md"
        f.write_text(
            "---\nstatus: pending\nclaimed_by: lying\n---\nbody",
            encoding="utf-8",
        )
        # frontmatter says "pending"; the path says "done"; Rule A → done.
        assert stage_of_path(f, project_root=tmp_path) == Stage.DONE


class TestSameMount:
    def test_freshly_created_lifecycle_is_single_mount(self, tmp_path: Path) -> None:
        ensure_lifecycle_dirs(tmp_path)
        assert same_mount(tmp_path) is True

    def test_returns_false_when_dirs_missing(self, tmp_path: Path) -> None:
        # No subdirs created → can't verify → False.
        assert same_mount(tmp_path) is False
