"""Drift tests for the canonical "have an agent install fcop-mcp" prompt.

Background. 0.6.4 standardised the install instructions across **four**
surfaces so every customer sees the same text regardless of where they
land:

1. ``src/fcop/rules/_data/agent-install-prompt.{zh,en}.md`` — source of
   truth, packaged into the wheel.
2. ``fcop.rules.get_install_prompt(lang)`` — programmatic accessor.
3. ``fcop://prompt/install`` + ``fcop://prompt/install/en`` — MCP
   resources, exposed to any MCP client (Cursor, Claude Code CLI…).
4. ``mcp/README.md`` — visible on GitHub *and* PyPI; embeds the EN
   prompt verbatim so a customer reading PyPI never has to leave the
   page to copy it.

Plus the root-level ``README.md`` and ``README.zh.md`` link to (1).

Without a test, surfaces (1) and (4) drift the moment one is edited
without the other. This module pins the relationship: the prompt
block extracted from ``mcp/README.md`` must equal the one returned by
``fcop.rules.get_install_prompt("en")``, both of which must equal the
content of the bundled markdown file.

We also assert the **non-negotiable safety clauses** are present in
both languages — the "preserve existing mcpServers" warning, the
"wait 30 seconds to 1 minute" cooldown, and the "do not auto-init"
instruction — so a future copy edit can't silently drop them.
"""

from __future__ import annotations

import pathlib
import re

import pytest

from fcop.rules import get_install_prompt

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
MCP_README = REPO_ROOT / "mcp" / "README.md"
ROOT_README_EN = REPO_ROOT / "README.md"
ROOT_README_ZH = REPO_ROOT / "README.zh.md"


def _extract_first_fenced_block(
    text: str, opening_fence: str = "```text"
) -> str:
    """Return the body of the first fenced code block in ``text``.

    Strict by default: opens on ``opening_fence`` and closes on the
    next ```` ``` ````. Designed for the install-prompt snippet,
    which we want bit-for-bit identity rather than fuzzy matching.
    """
    pattern = re.compile(
        r"^" + re.escape(opening_fence) + r"\s*\n(.*?)^```\s*$",
        re.DOTALL | re.MULTILINE,
    )
    match = pattern.search(text)
    if match is None:
        raise AssertionError(
            f"could not find a fenced block opening with {opening_fence!r}"
        )
    return match.group(1).rstrip()


def _extract_canonical_prompt_body(prompt_md: str) -> str:
    """Pull the actual instruction body out of an
    ``agent-install-prompt.{zh,en}.md`` file.

    The markdown wrapper carries headings + an explanatory blockquote;
    only the unlabelled fenced block between "Copy the block below"
    and the next horizontal rule is the canonical text. We extract
    that and compare it against what the README inlines.
    """
    pattern = re.compile(r"^```\s*\n(.*?)^```\s*$", re.DOTALL | re.MULTILINE)
    match = pattern.search(prompt_md)
    if match is None:
        raise AssertionError(
            "agent-install-prompt markdown is missing its fenced block"
        )
    return match.group(1).rstrip()


class TestPromptIsStandardized:
    """The four-surface contract: same text everywhere."""

    def test_get_install_prompt_returns_zh_file_verbatim(self) -> None:
        on_disk = (
            REPO_ROOT
            / "src/fcop/rules/_data/agent-install-prompt.zh.md"
        ).read_text(encoding="utf-8")
        assert get_install_prompt("zh") == on_disk

    def test_get_install_prompt_returns_en_file_verbatim(self) -> None:
        on_disk = (
            REPO_ROOT
            / "src/fcop/rules/_data/agent-install-prompt.en.md"
        ).read_text(encoding="utf-8")
        assert get_install_prompt("en") == on_disk

    def test_mcp_readme_inlines_canonical_en_prompt(self) -> None:
        # mcp/README.md is the PyPI-visible page. It embeds the EN
        # prompt inside a ```text fenced block so a copy-paste from
        # PyPI matches the canonical text byte-for-byte.
        readme = MCP_README.read_text(encoding="utf-8")
        embedded = _extract_first_fenced_block(readme, "```text")

        canonical = _extract_canonical_prompt_body(get_install_prompt("en"))
        assert embedded == canonical, (
            "mcp/README.md TL;DR install prompt has drifted from "
            "src/fcop/rules/_data/agent-install-prompt.en.md. "
            "Update both — the README is just a copy of the .md."
        )

    def test_root_readme_links_to_install_prompt_files(self) -> None:
        text = ROOT_README_EN.read_text(encoding="utf-8")
        assert "agent-install-prompt.en.md" in text
        assert "agent-install-prompt.zh.md" in text
        assert "fcop://prompt/install" in text

    def test_root_readme_zh_links_to_install_prompt_files(self) -> None:
        text = ROOT_README_ZH.read_text(encoding="utf-8")
        assert "agent-install-prompt.zh.md" in text
        assert "agent-install-prompt.en.md" in text
        assert "fcop://prompt/install" in text


class TestPromptSafetyClausesPresent:
    """The non-negotiable safety clauses must survive copy edits."""

    @pytest.mark.parametrize("lang", ["zh", "en"])
    def test_prompt_demands_preserving_existing_mcp_servers(
        self, lang: str
    ) -> None:
        text = get_install_prompt(lang)  # type: ignore[arg-type]
        # ZH uses 保留 / 不要覆盖; EN uses Preserve / do not overwrite.
        # Either canonical phrase counts.
        if lang == "zh":
            assert "保留" in text and "覆盖" in text, (
                "ZH prompt must explicitly tell the agent to preserve "
                "existing mcpServers — drop this and the agent may wipe "
                "the user's other MCP servers"
            )
        else:
            assert "Preserve" in text or "preserve" in text
            assert "overwrite" in text.lower()

    @pytest.mark.parametrize("lang", ["zh", "en"])
    def test_prompt_warns_about_first_launch_cooldown(
        self, lang: str
    ) -> None:
        text = get_install_prompt(lang)  # type: ignore[arg-type]
        # Both languages mention "30 seconds to 1 minute" / "30 秒
        # 到 1 分钟" — pin the numerals so a translation drift can't
        # silently drop the cooldown.
        assert "30" in text and "1" in text, (
            f"{lang} prompt must mention the 30-second-to-1-minute "
            "first-launch cooldown — without it customers reconnect "
            "early and the install looks broken"
        )

    @pytest.mark.parametrize("lang", ["zh", "en"])
    def test_prompt_forbids_auto_init_after_install(
        self, lang: str
    ) -> None:
        text = get_install_prompt(lang)  # type: ignore[arg-type]
        # ZH uses "不要" 自动初始化 / "选择题"; EN uses "Do not" auto-
        # init / "ADMIN's choice". Cross-check both anchors so a
        # future paraphrase has to keep the intent.
        if lang == "zh":
            assert "不要" in text and "初始化" in text
            assert "ADMIN" in text
        else:
            assert "Do not" in text or "do not" in text
            assert "auto-init" in text.lower() or "init" in text.lower()
            assert "ADMIN" in text
