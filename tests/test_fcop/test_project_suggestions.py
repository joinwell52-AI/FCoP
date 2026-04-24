"""Tests for :meth:`fcop.Project.drop_suggestion` — D5-c4.

``drop_suggestion`` is intentionally the simplest write-side tool in
the library: it's a pressure valve for protocol-level disagreement.
These tests pin:

    * File layout — ``<project>/.fcop/proposals/<timestamp>.md``.
    * Content shape — the ``# Suggestion @ <ts>`` header, optional
      ``**Context**:`` line, then the body verbatim (after stripping).
    * Idempotency-ish guarantee — two calls in the same second get
      distinct files (``-2``, ``-3`` suffix) rather than one
      clobbering the other.
    * Input validation — empty / whitespace-only ``content`` raises.
    * Does *not* require an initialized project: any agent can drop
      a suggestion even in a half-set-up workspace.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from fcop import Project

# ``YYYYMMDD-HHMMSS`` plus optional ``-N`` duplicate-counter, plus ``.md``.
_FILENAME_RE = re.compile(r"^\d{8}-\d{6}(-\d+)?\.md$")


class TestHappyPath:
    def test_creates_proposals_dir_and_returns_path(
        self, tmp_path: Path
    ) -> None:
        project = Project(tmp_path)
        path = project.drop_suggestion(content="Rule 5 is too strict.")
        assert path.is_absolute()
        assert path.is_file()
        # Lives under .fcop/proposals/ inside the project.
        assert path.parent == tmp_path / ".fcop" / "proposals"
        assert _FILENAME_RE.match(path.name), (
            f"unexpected filename shape: {path.name!r}"
        )

    def test_header_and_body_shape(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        path = project.drop_suggestion(
            content="Rule 5 needs an exception for cross-team reports.",
        )
        text = path.read_text(encoding="utf-8")
        # Opens with the timestamped suggestion header.
        assert text.startswith("# Suggestion @ "), text[:40]
        # Body is preserved verbatim somewhere after the header.
        assert "cross-team reports" in text
        # File ends with a newline — makes cat/diff/git happy.
        assert text.endswith("\n")

    def test_context_included_when_provided(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        path = project.drop_suggestion(
            content="Change X.",
            context="TASK-20260423-001-ADMIN-to-PM.md",
        )
        text = path.read_text(encoding="utf-8")
        assert "**Context**: TASK-20260423-001-ADMIN-to-PM.md" in text

    def test_context_omitted_when_blank(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        path = project.drop_suggestion(content="Change X.", context="   ")
        text = path.read_text(encoding="utf-8")
        # No **Context**: line when the caller passes only whitespace.
        assert "**Context**:" not in text

    def test_does_not_require_initialized_project(
        self, tmp_path: Path
    ) -> None:
        # No Project.init() call — this works anyway so agents mid-
        # setup can always file a complaint.
        project = Project(tmp_path)
        assert not project.is_initialized()
        path = project.drop_suggestion(content="Init UX is confusing.")
        assert path.is_file()


class TestUniqueness:
    def test_two_calls_same_second_produce_different_files(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        # Freeze the timestamp so both calls attempt the same stem;
        # the helper must fall back to ``<stem>-2.md`` instead of
        # clobbering the first. We patch `datetime` inside
        # fcop.project's namespace (the module imports the whole
        # `datetime` submodule as `_dt`, so patching on that handle
        # is equivalent to patching globally for the function under
        # test without touching other modules' copies).
        import datetime as real_dt

        frozen_moment = real_dt.datetime(2026, 4, 23, 18, 5, 12)

        class FrozenDatetime(real_dt.datetime):
            @classmethod
            def now(cls, tz: real_dt.tzinfo | None = None) -> real_dt.datetime:  # type: ignore[override]
                return frozen_moment

        monkeypatch.setattr("fcop.project._dt.datetime", FrozenDatetime)

        project = Project(tmp_path)
        first = project.drop_suggestion(content="one")
        second = project.drop_suggestion(content="two")
        third = project.drop_suggestion(content="three")

        assert first != second != third
        assert {p.name for p in (first, second, third)} == {
            "20260423-180512.md",
            "20260423-180512-2.md",
            "20260423-180512-3.md",
        }
        # And each file still has its own body — nothing was lost.
        assert "one" in first.read_text(encoding="utf-8")
        assert "two" in second.read_text(encoding="utf-8")
        assert "three" in third.read_text(encoding="utf-8")


class TestInputValidation:
    @pytest.mark.parametrize("bad", ["", "   ", "\n\n", "\t"])
    def test_empty_content_rejected(self, tmp_path: Path, bad: str) -> None:
        project = Project(tmp_path)
        with pytest.raises(ValueError, match="non-empty content"):
            project.drop_suggestion(content=bad)
        # No file created — the proposals dir doesn't even exist.
        assert not (tmp_path / ".fcop" / "proposals").exists()

    def test_content_stripped_in_body(self, tmp_path: Path) -> None:
        # Leading/trailing whitespace on `content` is stripped in the
        # body, but internal whitespace is preserved. This matches how
        # `context` is handled — fair on both knobs.
        project = Project(tmp_path)
        path = project.drop_suggestion(content="   hello\nworld   ")
        text = path.read_text(encoding="utf-8")
        assert "hello\nworld" in text
        # But the leading spaces are NOT in the file (header separator
        # is \n\n, body follows, then trailing \n).
        body_start = text.index("\n\n") + 2
        # Find the body line that starts with "hello" — no leading
        # whitespace should precede it.
        assert text[body_start:body_start + 5] == "hello"
