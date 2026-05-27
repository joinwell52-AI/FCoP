"""UTF-8 / mojibake guards for bundled FCoP rule files (release gate).

Regression context: fcop 3.2.3 PyPI wheel shipped garbled fcop-protocol.mdc
(UTF-8 corruption during release sync). These checks fail the release if
bundled rules look corrupted before upload.
"""
from __future__ import annotations

import zipfile
from pathlib import Path

# Substrings observed in the bad 3.2.3 wheel (not valid protocol prose).
MOJIBAKE_SUBSTRINGS: tuple[str, ...] = (
    "鍗忚",       # garbled fragment of 协议
    "涓枃",       # common mis-decoded CJK run
    "鍗忚幙",     # garbled 协议层
    "\ufffd",     # Unicode replacement character
)

PROTOCOL_FILE = "fcop-protocol.mdc"
RULES_FILE = "fcop-rules.mdc"

PROTOCOL_GOOD_MARKERS: tuple[str, ...] = (
    "协议解释",
    "Protocol Commentary",
    "## Core Principle",
    "fcop_protocol_version",
)

RULES_GOOD_MARKERS: tuple[str, ...] = (
    "FCoP Rules",
    "fcop_rules_version",
    "Rule 0",
    "_lifecycle/",
)


def _collect_encoding_issues(text: str, good_markers: tuple[str, ...], label: str) -> list[str]:
    issues: list[str] = []
    for bad in MOJIBAKE_SUBSTRINGS:
        if bad in text:
            issues.append(f"{label}: mojibake marker {bad!r}")
    if not any(m in text for m in good_markers):
        issues.append(
            f"{label}: missing expected markers (need one of {good_markers!r})"
        )
    if label.endswith(PROTOCOL_FILE):
        cjk = sum(1 for c in text if "\u4e00" <= c <= "\u9fff")
        if cjk < 500:
            issues.append(
                f"{label}: too few CJK characters ({cjk}; garbled wheel often drops readable zh)"
            )
    return issues


def validate_rule_file(path: Path) -> list[str]:
    """Return issue strings; empty list means OK."""
    if not path.exists():
        return [f"{path.name}: file missing at {path}"]
    text = path.read_text(encoding="utf-8")
    name = path.name
    if name == PROTOCOL_FILE:
        return _collect_encoding_issues(text, PROTOCOL_GOOD_MARKERS, name)
    if name == RULES_FILE:
        return _collect_encoding_issues(text, RULES_GOOD_MARKERS, name)
    return []


def validate_bundled_rules(rules_data_dir: Path) -> list[str]:
    issues: list[str] = []
    for fname in (PROTOCOL_FILE, RULES_FILE):
        issues.extend(validate_rule_file(rules_data_dir / fname))
    return issues


def validate_wheel_rules(whl_path: Path) -> list[str]:
    """Inspect fcop-protocol.mdc / fcop-rules.mdc inside a built wheel."""
    issues: list[str] = []
    if not whl_path.exists():
        return [f"wheel not found: {whl_path}"]
    with zipfile.ZipFile(whl_path) as zf:
        for fname in (PROTOCOL_FILE, RULES_FILE):
            members = [n for n in zf.namelist() if n.endswith(f"rules/_data/{fname}")]
            if not members:
                issues.append(f"wheel: no rules/_data/{fname}")
                continue
            text = zf.read(members[0]).decode("utf-8")
            markers = PROTOCOL_GOOD_MARKERS if fname == PROTOCOL_FILE else RULES_GOOD_MARKERS
            issues.extend(_collect_encoding_issues(text, markers, f"wheel:{fname}"))
    return issues
