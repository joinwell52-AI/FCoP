"""Inject or replace the Rule 0.a.1 workflow section in bundled role charters.

Since fcop@3.2.5 the canonical cycle is::

    task → execute/dispatch → report → await acceptance / archive when authorised

—not the legacy ``task → do → report → archive`` four-step contract where
executors were taught to call ``archive_task`` as Step 4.

Authoritative block text lives in::

    src/fcop/templates/roles/_COMMON-FCOP-3.2.5.md

The script **replaces** an existing hard-constraint section when it finds
the canonical anchor (``工作流硬约束`` / ``Workflow hard constraint`` /
solo ``核心工作流`` / ``Core workflow (hard constraint``).  Idempotent
re-runs overwrite with the latest common block.

Run from the repo root::

    py -3.12 scripts/inject_workflow_constraint.py
"""

from __future__ import annotations

import pathlib
import re
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
ROLES_GLOB = "src/fcop/teams/_data/*/roles/*.md"
COMMON_PATH = REPO_ROOT / "src/fcop/templates/roles/_COMMON-FCOP-3.2.5.md"

TEAM_ZH_ANCHOR = "## 工作流硬约束"
TEAM_EN_ANCHOR = "## Workflow hard constraint"
SOLO_ZH_ANCHOR = "## 核心工作流（硬约束 / 不允许例外）"
SOLO_EN_ANCHOR = "## Core workflow (hard constraint / no exceptions)"

_BLOCK_RE = re.compile(
    r"<!-- BEGIN_(?P<key>TEAM_ZH|TEAM_EN|SOLO_ZH|SOLO_EN) -->\n"
    r"(?P<body>.*?)\n<!-- END_\1 -->",
    re.DOTALL,
)
_FRONTMATTER_RE = re.compile(r"^---\r?\n(?P<body>.*?)\r?\n---\r?\n", re.DOTALL)
_ROLE_FIELD_RE = re.compile(r"^role:\s*(\S+)\s*$", re.MULTILINE)
_H1_RE = re.compile(r"^# .+$", re.MULTILINE)
_NEXT_H2_RE = re.compile(r"\n## (?!#)", re.MULTILINE)


def _load_blocks() -> dict[str, str]:
    text = COMMON_PATH.read_text(encoding="utf-8")
    blocks: dict[str, str] = {}
    for match in _BLOCK_RE.finditer(text):
        blocks[match.group("key")] = match.group("body").rstrip() + "\n"
    missing = {"TEAM_ZH", "TEAM_EN", "SOLO_ZH", "SOLO_EN"} - blocks.keys()
    if missing:
        raise RuntimeError(f"{COMMON_PATH} missing blocks: {sorted(missing)}")
    return blocks


def _is_english(path: pathlib.Path) -> bool:
    return path.name.endswith(".en.md")


def _is_solo(path: pathlib.Path) -> bool:
    return "solo" in path.parts


def _role_from_path(path: pathlib.Path) -> str:
    name = path.name
    if name.endswith(".en.md"):
        return name[: -len(".en.md")]
    return path.stem


def _extract_role(text: str, path: pathlib.Path) -> str | None:
    match = _FRONTMATTER_RE.match(text)
    if match:
        role_match = _ROLE_FIELD_RE.search(match.group("body"))
        if role_match:
            return role_match.group(1)
    # Fallback: filename stem (PM.md / AUTO-TESTER.en.md)
    return _role_from_path(path)


def _section_bounds(text: str, anchor: str) -> tuple[int, int] | None:
    start = text.find(anchor)
    if start < 0:
        return None
    tail = text[start + len(anchor) :]
    next_h2 = _NEXT_H2_RE.search(tail)
    end = start + len(anchor) + next_h2.start() if next_h2 else len(text)
    return start, end


def _pick_block(path: pathlib.Path, blocks: dict[str, str]) -> tuple[str, str]:
    is_en = _is_english(path)
    if _is_solo(path):
        key = "SOLO_EN" if is_en else "SOLO_ZH"
        anchor = SOLO_EN_ANCHOR if is_en else SOLO_ZH_ANCHOR
    else:
        key = "TEAM_EN" if is_en else "TEAM_ZH"
        anchor = TEAM_ZH_ANCHOR if not is_en else TEAM_EN_ANCHOR
    return anchor, blocks[key]


def _inject(path: pathlib.Path, blocks: dict[str, str]) -> str:
    text = path.read_text(encoding="utf-8")
    anchor, template = _pick_block(path, blocks)
    role = _extract_role(text, path)
    if not role:
        return "skipped-no-role"

    block = template.replace("{role}", role)
    bounds = _section_bounds(text, anchor)

    if bounds is not None:
        start, end = bounds
        new_text = text[:start] + block.rstrip() + "\n" + text[end:]
        action = "replaced"
    else:
        h1_match = _H1_RE.search(text)
        if h1_match is None:
            return "skipped-no-h1"
        insert_at = h1_match.end()
        new_text = text[:insert_at] + "\n\n" + block.rstrip() + "\n" + text[insert_at:]
        action = "injected"

    path.write_text(new_text, encoding="utf-8", newline="\n")
    return action


def main() -> int:
    if not COMMON_PATH.is_file():
        print(f"missing common inject file: {COMMON_PATH}")
        return 1

    blocks = _load_blocks()
    files = sorted(REPO_ROOT.glob(ROLES_GLOB))
    if not files:
        print(f"no role files matched glob {ROLES_GLOB!r} under {REPO_ROOT}")
        return 1

    counts: dict[str, int] = {}
    for path in files:
        action = _inject(path, blocks)
        counts[action] = counts.get(action, 0) + 1
        rel = path.relative_to(REPO_ROOT)
        print(f"  {action:20s}  {rel}")

    print()
    print("Summary:")
    for action, count in sorted(counts.items()):
        print(f"  {action:20s}  {count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
