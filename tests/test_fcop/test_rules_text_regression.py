"""Regression tests for the bundled FCoP rule texts.

Catches the kinds of "protocol drift" bugs that ISSUE-20260427-005
exposed: ``fcop-rules.mdc`` Rule 5 used to mention ``AMEND-*`` and
``-v2`` filenames, but the library's parsers never recognised those
prefixes — so anything written under those names was a "ghost file"
from the toolchain's point of view.

The rules-text files are protocol surface, not internal docs. Their
shape changing without the version frontmatter changing too is the
exact failure mode this regression battery prevents.
"""

from __future__ import annotations

import re
from importlib import resources


def _read_rule_data(filename: str) -> str:
    with resources.files("fcop.rules._data").joinpath(filename).open(
        "r", encoding="utf-8"
    ) as f:
        return f.read()


def _parse_frontmatter_version(text: str, key: str) -> tuple[int, int, int] | None:
    """Extract ``X.Y.Z`` from ``key: X.Y.Z`` in frontmatter."""
    m = re.search(rf"^{re.escape(key)}:\s*(\d+)\.(\d+)\.(\d+)\s*$", text, re.MULTILINE)
    if m:
        return int(m.group(1)), int(m.group(2)), int(m.group(3))
    return None


class TestRulesVersion:
    def test_rules_version_is_180_or_later(self) -> None:
        text = _read_rule_data("fcop-rules.mdc")
        # Accept any X.Y.Z >= 1.8.0 (rules went 3.0.0 in fcop 2.0.0).
        ver = _parse_frontmatter_version(text, "fcop_rules_version")
        assert ver is not None, "fcop-rules.mdc must declare fcop_rules_version: X.Y.Z"
        assert ver >= (1, 8, 0), (
            f"fcop-rules.mdc fcop_rules_version {'.'.join(str(n) for n in ver)} "
            "must be >= 1.8.0 since 0.7.1"
        )

    def test_protocol_version_is_160_or_later(self) -> None:
        text = _read_rule_data("fcop-protocol.mdc")
        # Accept any X.Y.Z >= 1.6.0 (protocol went 3.x in fcop 2.0.0).
        ver = _parse_frontmatter_version(text, "fcop_protocol_version")
        assert ver is not None, "fcop-protocol.mdc must declare fcop_protocol_version: X.Y.Z"
        assert ver >= (1, 6, 0), (
            f"fcop-protocol.mdc fcop_protocol_version {'.'.join(str(n) for n in ver)} "
            "must be >= 1.6.0 since 0.7.1"
        )


class TestRule5DropsAmendV2:
    """ISSUE-20260427-005 regression: Rule 5 must no longer suggest
    creating ``AMEND-*`` or ``*-v2.md`` files.

    The library's filename parsers only recognise ``TASK-`` /
    ``REPORT-`` / ``ISSUE-`` prefixes; promoting alternative
    correction prefixes in the rule text writes ghost files into the
    ledger.
    """

    def test_rules_does_not_recommend_amend_prefix(self) -> None:
        text = _read_rule_data("fcop-rules.mdc")
        # The body of Rule 5 (delimited by the next "## Rule 6" or
        # "## Rule" heading) is what we audit. A historical mention
        # in a changelog footnote is acceptable; an active
        # recommendation is not.
        rule5_start = text.find("## Rule 5")
        rule5_end = text.find("## Rule 6", rule5_start)
        assert rule5_start != -1, "Rule 5 heading missing"
        if rule5_end == -1:
            rule5_end = len(text)
        rule5_body = text[rule5_start:rule5_end]

        # The new copy explicitly forbids these patterns; an old copy
        # would *recommend* them. Detect the forbidden recommendation
        # by checking that "do not invent" / "不要" appears whenever
        # AMEND / v2 are mentioned.
        if "AMEND-" in rule5_body or "-v2" in rule5_body:
            assert (
                "不要" in rule5_body
                or "do not" in rule5_body.lower()
                or "must not" in rule5_body.lower()
            ), (
                "Rule 5 still mentions AMEND-* / -v2 patterns but no "
                "longer marks them as forbidden. ISSUE-20260427-005 "
                "regression — these prefixes are not parsed by fcop "
                "and must not be promoted."
            )

    def test_rules_recommends_sequential_filename_for_corrections(
        self,
    ) -> None:
        text = _read_rule_data("fcop-rules.mdc")
        rule5_start = text.find("## Rule 5")
        rule5_end = text.find("## Rule 6", rule5_start)
        if rule5_end == -1:
            rule5_end = len(text)
        rule5_body = text[rule5_start:rule5_end]

        # The 1.8.0 copy points at "next sequence number / 下一序号".
        assert (
            "下一序号" in rule5_body
            or "next sequence" in rule5_body.lower()
        ), (
            "Rule 5 must point users at sequential filenames as the "
            "canonical correction path (since 1.8.0 / 0.7.1)."
        )


class TestRule1MentionsSubAgent:
    """ISSUE-20260427-004 regression: Rule 1 must explicitly forbid
    sub-agents from claiming roles their parent session was not
    assigned.
    """

    def test_rule1_mentions_sub_agent_inheritance(self) -> None:
        text = _read_rule_data("fcop-rules.mdc")
        # Look for either the Chinese or English clause we landed in
        # 1.8.0.
        assert (
            "sub-agent" in text.lower() or "子 agent" in text
        ), (
            "Rule 1 must mention sub-agent identity inheritance "
            "(since 1.8.0). ISSUE-20260427-004 regression."
        )


class TestRule0a1AllPaths:
    """ISSUE-20260427-001 regression: Rule 0.a.1 must clarify that the
    four-step cycle binds *every* write path, not only MCP tools.
    """

    def test_rule0a1_calls_out_non_mcp_paths(self) -> None:
        text = _read_rule_data("fcop-rules.mdc")
        # Either the Chinese or English copy needs the clarification.
        zh_match = "所有写入路径" in text or "适用所有写入路径" in text
        en_match = (
            "every write path" in text.lower()
            or "binds every write path" in text.lower()
        )
        assert zh_match or en_match, (
            "Rule 0.a.1 must spell out that the four-step cycle "
            "applies to shell / git / IDE writes, not just MCP "
            "tools (since 1.8.0). ISSUE-20260427-001 regression."
        )
