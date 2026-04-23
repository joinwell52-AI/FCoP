"""Tests for :mod:`fcop.rules` — the D5-c1 surface.

The rules module is a thin wrapper over :mod:`importlib.resources`:
it reads bundled ``.mdc`` / ``.md`` files and returns them as strings.
Tests here check:

    * All four public accessors return non-empty text.
    * Text is valid UTF-8 with actual markdown (fence line, at least
      one Chinese or English heading).
    * ``get_rules_version`` returns a semver-shaped string parsed from
      the rules frontmatter.
    * ``get_letter`` rejects unsupported languages.
    * Results are cached — the second call returns the same object.
    * Bundled data is actually packaged; the file shows up via
      :mod:`importlib.resources`.
"""

from __future__ import annotations

import re
from importlib import resources

import pytest

from fcop.errors import FcopError
from fcop.rules import (
    get_letter,
    get_protocol_commentary,
    get_rules,
    get_rules_version,
)

# ── Happy paths ──────────────────────────────────────────────────────


class TestGetRules:
    def test_returns_non_empty_text(self) -> None:
        text = get_rules()
        assert isinstance(text, str)
        assert len(text) > 500  # real document, not a stub

    def test_has_frontmatter_and_title(self) -> None:
        text = get_rules()
        assert text.startswith("---")
        # Version field is in the frontmatter.
        assert "fcop_rules_version:" in text
        # The H1 heading appears somewhere in the first 2 KB.
        assert "# FCoP Rules" in text[:2048]

    def test_cached(self) -> None:
        # Two calls return the exact same object — the lru_cache on
        # _load_text is doing its job. This matters for LLM-prompt
        # assembly where get_rules() might be called hundreds of
        # times per session.
        assert get_rules() is get_rules()


class TestGetProtocolCommentary:
    def test_returns_non_empty_text(self) -> None:
        text = get_protocol_commentary()
        assert isinstance(text, str)
        assert len(text) > 500


class TestGetLetter:
    def test_default_is_chinese(self) -> None:
        text = get_letter()
        # Heuristic: the Chinese letter contains at least one CJK char.
        assert re.search(r"[\u4e00-\u9fff]", text)

    def test_english(self) -> None:
        text = get_letter("en")
        # The EN letter should contain plain ASCII letters and no CJK
        # in its heading. (Body may cite CJK names, but the opening
        # should be English.)
        assert text.lstrip().startswith(("# ", "---"))
        # Sanity: EN and ZH are different files → different strings.
        assert text != get_letter("zh")

    def test_unknown_language_raises(self) -> None:
        with pytest.raises(ValueError, match="unsupported letter language"):
            get_letter("fr")  # type: ignore[arg-type]


class TestGetRulesVersion:
    def test_semver_shape(self) -> None:
        version = get_rules_version()
        # Should match a "x.y.z" (or "x.y.z-tag") pattern.
        assert re.fullmatch(r"\d+\.\d+\.\d+(-[\w.]+)?", version), (
            f"unexpected rules version shape: {version!r}"
        )


# ── Packaging sanity ─────────────────────────────────────────────────


class TestPackagedData:
    """Verify the data files actually ship with the package.

    Catches the regression where someone removes the
    `force-include` block in pyproject.toml — our wheels would build
    green, import would succeed, but every getter would raise
    FileNotFoundError at runtime.
    """

    @pytest.mark.parametrize(
        "name",
        [
            "fcop-rules.mdc",
            "fcop-protocol.mdc",
            "letter-to-admin.zh.md",
            "letter-to-admin.en.md",
        ],
    )
    def test_data_file_is_traversable(self, name: str) -> None:
        data_dir = resources.files("fcop.rules").joinpath("_data")
        candidate = data_dir.joinpath(name)
        assert candidate.is_file(), (
            f"{name} is not shipped in the fcop.rules._data package; "
            f"check pyproject.toml [tool.hatch.build.targets.wheel.force-include]"
        )

    def test_malformed_frontmatter_raises(self, monkeypatch) -> None:  # type: ignore[no-untyped-def]
        # Confirm the failure mode of get_rules_version when the
        # frontmatter field has been stripped: swap in a version of
        # get_rules that returns text missing the key, and assert we
        # get a clear FcopError rather than an obscure TypeError.
        from fcop import rules as rules_mod

        monkeypatch.setattr(
            rules_mod,
            "get_rules",
            lambda: "---\nno version here\n---\n# empty\n",
        )
        with pytest.raises(FcopError, match="fcop_rules_version"):
            rules_mod.get_rules_version()
