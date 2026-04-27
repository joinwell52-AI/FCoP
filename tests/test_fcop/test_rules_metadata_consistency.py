"""Metadata-consistency tests for the bundled rules / protocol files.

These tests prevent **ISSUE-20260427-007** — the third "multi-line
edit, one edit dropped" bug in the 0.7.x cycle. The release of
``fcop-rules.mdc`` for 1.8.0 shipped with body content correctly
updated to 1.8.0 (Rule 1 sub-agent clause, Rule 5 AMEND removal,
Rule 0.a.1 clarification) **but** the frontmatter still said
``fcop_rules_version: 1.7.0``. ``fcop_report()`` therefore reported
"rules: 1.7.0" while the rules ALREADY behaved as 1.8.0.

Both `.mdc` files in ``src/fcop/rules/_data/`` carry their version
in two places that humans must update together:

1. **Frontmatter**: ``fcop_rules_version: X.Y.Z`` /
   ``fcop_protocol_version: X.Y.Z``.
2. **Body changelog heading**: ``**X.Y.Z changes / X.Y.Z 变更**:``
   for ``fcop-rules.mdc`` or ``- **vX.Y** (YYYY-MM-DD)`` for
   ``fcop-protocol.mdc``.

The two MUST agree. If a maintainer remembers to add the new
changelog block but forgets to bump the frontmatter (or vice versa),
this test fails the build before the wheel is built.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
RULES_FILE = REPO_ROOT / "src" / "fcop" / "rules" / "_data" / "fcop-rules.mdc"
PROTOCOL_FILE = REPO_ROOT / "src" / "fcop" / "rules" / "_data" / "fcop-protocol.mdc"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _frontmatter_version(text: str, key: str) -> tuple[int, int, int]:
    match = re.search(rf"^{re.escape(key)}:\s*(\d+)\.(\d+)\.(\d+)\s*$", text, re.MULTILINE)
    assert match is not None, f"frontmatter `{key}: X.Y.Z` not found"
    return int(match.group(1)), int(match.group(2)), int(match.group(3))


def _max_changelog_version(text: str, pattern: re.Pattern[str]) -> tuple[int, int, int]:
    versions: list[tuple[int, int, int]] = []
    for match in pattern.finditer(text):
        groups = match.groups()
        if len(groups) == 3:
            versions.append((int(groups[0]), int(groups[1]), int(groups[2])))
        else:
            versions.append((int(groups[0]), int(groups[1]), 0))
    assert versions, (
        f"no changelog entry found with pattern {pattern.pattern!r}; the body "
        "must list each version that ships, otherwise this test cannot detect "
        "metadata drift"
    )
    return max(versions)


def test_fcop_rules_frontmatter_matches_body_changelog() -> None:
    """``fcop-rules.mdc`` frontmatter must equal the highest body changelog.

    Body convention: ``**1.8.0 changes / 1.8.0 变更**:`` lines.
    """
    text = _read(RULES_FILE)
    frontmatter = _frontmatter_version(text, "fcop_rules_version")
    body_pattern = re.compile(r"\*\*(\d+)\.(\d+)\.(\d+) changes")
    latest_body = _max_changelog_version(text, body_pattern)

    assert frontmatter == latest_body, (
        f"fcop-rules.mdc frontmatter `fcop_rules_version: "
        f"{'.'.join(str(n) for n in frontmatter)}` does not match the "
        f"latest body changelog "
        f"`**{'.'.join(str(n) for n in latest_body)} changes ...**`. "
        "This is the ISSUE-20260427-007 metadata-drift bug — bump them "
        "together in the same commit. Either the frontmatter is stale "
        "(forgot to bump after adding new rules content) or the body is "
        "stale (added the version field but never wrote what changed)."
    )


def test_fcop_protocol_frontmatter_matches_body_changelog() -> None:
    """``fcop-protocol.mdc`` frontmatter must equal the highest body
    changelog entry.

    Body convention: ``- **vX.Y** (YYYY-MM-DD) — ...`` lines under the
    "Protocol Version Log" section.
    """
    text = _read(PROTOCOL_FILE)
    frontmatter = _frontmatter_version(text, "fcop_protocol_version")
    body_pattern = re.compile(r"^-\s+\*\*v(\d+)\.(\d+)\*\*", re.MULTILINE)
    latest_body = _max_changelog_version(text, body_pattern)

    assert frontmatter[:2] == latest_body[:2], (
        f"fcop-protocol.mdc frontmatter `fcop_protocol_version: "
        f"{'.'.join(str(n) for n in frontmatter)}` (minor "
        f"{frontmatter[0]}.{frontmatter[1]}) does not match the latest "
        f"body changelog `- **v{latest_body[0]}.{latest_body[1]}**`. "
        "ISSUE-20260427-007 again — bump frontmatter and body together."
    )


def test_no_stale_rules_version_anywhere_in_data() -> None:
    """Belt-and-braces: catch frontmatter / body **at the same time**.

    If somebody copy-pastes the file structure for a new bundled rule
    document and forgets to bump versions, this test surfaces it.
    Currently bounded to the `_data` directory because that is the
    only authoritative source of bundled rules.
    """
    rules_text = _read(RULES_FILE)
    protocol_text = _read(PROTOCOL_FILE)

    rules_frontmatter = _frontmatter_version(rules_text, "fcop_rules_version")
    protocol_frontmatter = _frontmatter_version(protocol_text, "fcop_protocol_version")

    rules_body_pattern = re.compile(r"\*\*(\d+)\.(\d+)\.(\d+) changes")
    protocol_body_pattern = re.compile(r"^-\s+\*\*v(\d+)\.(\d+)\*\*", re.MULTILINE)

    rules_body = _max_changelog_version(rules_text, rules_body_pattern)
    protocol_body = _max_changelog_version(protocol_text, protocol_body_pattern)

    assert rules_frontmatter == rules_body, "fcop-rules.mdc frontmatter ↔ body drift"
    assert protocol_frontmatter[:2] == protocol_body[:2], (
        "fcop-protocol.mdc frontmatter ↔ body drift"
    )
