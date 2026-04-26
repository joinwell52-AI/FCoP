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
    get_letter_intro,
    get_protocol_commentary,
    get_protocol_version,
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


class TestGetLetterIntro:
    """Pin the intro slice that the MCP layer splices into the
    post-init handover. This slice is what ADMIN actually *sees*
    after running ``init_*`` — drift here is a UX regression, not a
    cosmetic one, so we assert structural invariants rather than
    exact bytes."""

    def test_zh_starts_with_letter_title(self) -> None:
        intro = get_letter_intro("zh")
        assert intro.startswith("# FCoP 致 ADMIN 的一封信"), (
            "intro slice must keep the H1 title — that's the cue "
            "the agent uses when forwarding the block to ADMIN"
        )

    def test_zh_includes_064_summary_block(self) -> None:
        intro = get_letter_intro("zh")
        assert "0.6.4 摘要" in intro, (
            "0.6.4 introduced the workflow hard-constraint and the "
            "init-deposit fix; the intro must surface that summary"
        )

    def test_zh_is_strict_prefix_of_full_letter(self) -> None:
        # No paraphrasing is allowed — the slice must be a verbatim
        # prefix so the agent can paste it without divergence from
        # the on-disk LETTER-TO-ADMIN.md.
        intro = get_letter_intro("zh")
        full = get_letter("zh")
        assert full.startswith(intro.rstrip())

    def test_zh_is_substantially_shorter_than_full_letter(self) -> None:
        intro = get_letter_intro("zh")
        full = get_letter("zh")
        # Intro is meant to be ~50 lines; the full letter is ~500.
        # The exact ratio drifts as 0.6.x ships, so we only pin the
        # qualitative invariant: the intro is at most a quarter of
        # the full letter.
        assert len(intro) * 4 < len(full), (
            "intro slice must stay short enough to splice into the "
            "init reply without drowning the chat — currently "
            f"{len(intro)} chars vs full {len(full)} chars"
        )

    def test_en_starts_with_letter_title(self) -> None:
        intro = get_letter_intro("en")
        # The EN letter title is "A Letter from FCoP to ADMIN — User
        # Manual". We pin only the substring that's stable across
        # wording revisions ("FCoP" + "ADMIN") so a future title
        # tweak doesn't break the test, but a missing H1 still does.
        first_line = intro.splitlines()[0] if intro else ""
        assert first_line.startswith("# "), (
            f"EN intro must lead with an H1; got: {first_line!r}"
        )
        assert "FCoP" in first_line and "ADMIN" in first_line, (
            f"EN intro H1 must reference FCoP and ADMIN; got: {first_line!r}"
        )

    def test_en_is_strict_prefix_of_full_letter(self) -> None:
        intro = get_letter_intro("en")
        full = get_letter("en")
        assert full.startswith(intro.rstrip())

    def test_unknown_language_raises(self) -> None:
        with pytest.raises(ValueError, match="unsupported letter language"):
            get_letter_intro("fr")  # type: ignore[arg-type]


class TestGetRulesVersion:
    def test_semver_shape(self) -> None:
        version = get_rules_version()
        # Should match a "x.y.z" (or "x.y.z-tag") pattern.
        assert re.fullmatch(r"\d+\.\d+\.\d+(-[\w.]+)?", version), (
            f"unexpected rules version shape: {version!r}"
        )


class TestGetProtocolVersion:
    """Symmetric to :class:`TestGetRulesVersion`.

    The rules document and the protocol commentary version
    independently — :func:`get_protocol_version` is the second
    half of that pair, added in 0.6.3 (ADR-0006). It feeds
    :meth:`Project.deploy_protocol_rules` and the MCP layer's
    ``redeploy_rules`` so agents can detect a stale on-disk copy.
    """

    def test_semver_shape(self) -> None:
        version = get_protocol_version()
        assert re.fullmatch(r"\d+\.\d+\.\d+(-[\w.]+)?", version), (
            f"unexpected protocol version shape: {version!r}"
        )

    def test_independent_of_rules_version(self) -> None:
        # Both must parse, but they're separate strings — confirms we
        # didn't accidentally wire get_protocol_version through the
        # rules-document loader.
        rules_v = get_rules_version()
        protocol_v = get_protocol_version()
        # Even if they happen to coincide today, the *sources* are
        # different files; assert by re-loading both and checking the
        # commentary file actually carries fcop_protocol_version.
        commentary_text = get_protocol_commentary()
        assert "fcop_protocol_version:" in commentary_text
        assert protocol_v in commentary_text
        # Sanity: neither is empty.
        assert rules_v and protocol_v

    def test_malformed_frontmatter_raises(self, monkeypatch) -> None:  # type: ignore[no-untyped-def]
        # Same failure-mode contract as the rules version: when the
        # bundled commentary lacks a parseable version line, surface
        # FcopError loudly with a key-specific message.
        from fcop import rules as rules_mod

        monkeypatch.setattr(
            rules_mod,
            "get_protocol_commentary",
            lambda: "---\nno version here\n---\n# empty\n",
        )
        with pytest.raises(FcopError, match="fcop_protocol_version"):
            rules_mod.get_protocol_version()


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
