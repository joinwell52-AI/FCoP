#!/usr/bin/env python3
"""
Inventory drift audit — RULES-release-file-inventory §2 vs git ls-files.

Implements `audit.inventory_drift()` slot promised by
`fcop/shared/RULES-release-file-inventory.md` §4. Detects three drift
classes (per §4 spec):

    1. listed-but-missing : path declared in RULES §2 but not in
       `git ls-files`  → file deleted, RULES forgot to update.
    2. tracked-but-unlisted : `git ls-files` hit not declared in
       RULES §2  → new file slipped in without release-discipline.
    3. path-drift : path renamed (only fuzzy-detectable; we report
       basename matches across categories as candidates).

Exit codes:
    0  = no drift
    1  = drift detected (any class)

Bilingual output: every line carries `zh:` + `en:` (per ADMIN red line 3).

Usage:
    py -3.10 scripts/inventory_drift.py
    py -3.10 scripts/inventory_drift.py --json
    py -3.10 scripts/inventory_drift.py --strict   # fail on class 2 too
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
INVENTORY = REPO_ROOT / "fcop" / "shared" / "RULES-release-file-inventory.md"


# ---------------------------------------------------------------------------
# Scope: which directories are RULES §2 expected to govern?
# ---------------------------------------------------------------------------

# Roots that the inventory governs; everything outside is ignored by class-2
# (tracked-but-unlisted) so we don't drown ADMIN in false positives.
GOVERNED_ROOTS = (
    "src/fcop/_version.py",
    "src/fcop/rules/_data/",
    "mcp/src/fcop_mcp/_version.py",
    ".cursor/rules/",
    "AGENTS.md",
    "CLAUDE.md",
    "README.md",
    "README.zh.md",
    "mcp/README.md",
    "docs/index.html",
    "essays/README.md",
    "CITATION.cff",
    "CHANGELOG.md",
    "adr/",
    "docs/MIGRATION-",
    ".github/workflows/",
    "fcop/shared/TEAM-",
)

# Paths that may live under a governed root but are intentionally NOT release
# inventory items (helpers, data, samples). Substring match.
EXEMPT_SUBSTRINGS = (
    "src/fcop/rules/_data/teams/",  # team templates listed via glob in §I
    "adr/templates/",
    "adr/_assets/",
    ".github/workflows/test-",  # test-*.yml allowed by §J wildcard
    # F.5 hardcoded assertions point at specific test files but the test
    # files themselves are not "release artifacts"; skip the test corpus.
    "tests/",
)

# Glob patterns declared in §I (team templates) — recognised by their
# enclosing directory rather than per-file enumeration.
GLOB_GOVERNED = (
    re.compile(r"^src/fcop/rules/_data/teams/[^/]+/.+\.(md|en\.md)$"),
)


# ---------------------------------------------------------------------------
# Parse RULES §2 for declared file paths
# ---------------------------------------------------------------------------

# Bullet patterns: "- `path/to/file.md`" with possible bold and trailing
# annotation. We extract every backtick-quoted thing that looks like a path.
_BULLET_PATH_RE = re.compile(r"`([^`]+)`")

# Section boundary: the inventory's path enumeration lives strictly under
# "## 2. 文件清单 12 类 ..." up until "## 3. 改动义务 ...".
_SEC2_RE = re.compile(
    r"^## 2\. 文件清单 12 类.*?(?=^## 3\.)", re.M | re.S
)


_PATH_EXTS = (
    ".md", ".mdc", ".cff", ".html", ".yml", ".yaml",
    ".py", ".json", ".toml", ".txt", ".png",
)


def _looks_like_path(token: str) -> bool:
    """Heuristic: does this backtick-quoted token look like a repo path?"""
    # Strip any trailing line-number ref like `:779` so paths still match.
    base = re.sub(r":\d+$", "", token)
    has_slash = "/" in base
    has_known_ext = any(base.endswith(ext) for ext in _PATH_EXTS)
    if not (has_slash or has_known_ext):
        return False
    # If only `/` but no extension and no trailing `/`, likely an org/repo or
    # URL fragment (e.g. `joinwell52-AI/FCoP-backup`). Require an extension or
    # trailing slash to count as a repo path.
    if has_slash and not has_known_ext and not base.endswith("/"):
        return False
    # Filter out command snippets / regex / English prose fragments.
    bad_chars = " \n\t|()<>"
    if any(c in base for c in bad_chars):
        return False
    # Drop URL-like tokens (http://, https://, fcop://, etc.).
    if "://" in base:
        return False
    # Drop non-path-looking globs we explicitly handle elsewhere.
    if "{" in base and "}" in base:
        # Brace-expansion glob like `src/.../{dev-team,...}/*.{md,en.md}`
        return False
    # Drop wildcards — they belong to GLOB_GOVERNED, not per-file enumeration.
    if "*" in base or "?" in base:
        return False
    return True


def _expand_brace_glob(token: str) -> list[str]:
    """Light-touch brace expansion for §B's `{zh,en}.md` style entries.

    We keep this conservative: only expand the simplest 2-element brace,
    no nested braces, no commas inside braces."""
    m = re.match(r"^(.*?)\{([^{}]+)\}(.*)$", token)
    if not m:
        return [token]
    head, inner, tail = m.group(1), m.group(2), m.group(3)
    parts = [p.strip() for p in inner.split(",") if p.strip()]
    out: list[str] = []
    for p in parts:
        out.extend(_expand_brace_glob(f"{head}{p}{tail}"))
    return out


def parse_inventory_paths(text: str) -> set[str]:
    """Return the set of repo-relative paths declared in §2."""
    m = _SEC2_RE.search(text)
    section = m.group(0) if m else text
    paths: set[str] = set()
    for token in _BULLET_PATH_RE.findall(section):
        token = token.strip()
        # Skip non-path tokens (`every release`, `rg`, etc.)
        if not _looks_like_path(token):
            # Try brace-expand and re-test pieces
            for piece in _expand_brace_glob(token):
                piece = piece.strip()
                if _looks_like_path(piece):
                    paths.add(piece)
            continue
        for piece in _expand_brace_glob(token):
            piece = piece.strip()
            if piece:
                paths.add(piece)
    # Filter to repo-relative (drop absolute / scheme-y / template anchors).
    cleaned: set[str] = set()
    for p in paths:
        if p.startswith(("/", "http", "fcop://")):
            continue
        # Strip line-number ref like `path:779` — those are citations, not separate files.
        p = re.sub(r":\d+$", "", p)
        # Drop trailing punctuation accidentally captured.
        p = p.rstrip(".,;:")
        # Reject obvious prose remnants.
        if p in {"X.Y.Z", "vX.Y.Z 摘要", "fcop", "fcop-mcp"}:
            continue
        cleaned.add(p)
    return cleaned


# ---------------------------------------------------------------------------
# git ls-files with scope filter
# ---------------------------------------------------------------------------

def list_tracked_files() -> set[str]:
    out = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=REPO_ROOT, capture_output=True, check=True,
    )
    raw = out.stdout.decode("utf-8", errors="replace")
    return {line.strip() for line in raw.split("\0") if line.strip()}


def is_governed(path: str) -> bool:
    """Is this tracked path one that release-inventory §2 should mention?"""
    for ex in EXEMPT_SUBSTRINGS:
        if ex in path:
            return False
    for pat in GLOB_GOVERNED:
        if pat.match(path):
            return False  # covered by glob — not per-file enumerated
    for root in GOVERNED_ROOTS:
        if path == root or path.startswith(root):
            return True
    return False


def adr_glob_covers(path: str) -> bool:
    # Anything tracked under `adr/` counts as ADR-bucket content (ADRs,
    # ADR-adjacent NOTEs, semantic-execution-chain diagrams + assets, etc.).
    return path.startswith("adr/")


def workflow_glob_covers(path: str) -> bool:
    return bool(re.match(r"^\.github/workflows/.+\.yml$", path))


def migration_glob_covers(path: str) -> bool:
    # Allow zh/en bilingual variants too: MIGRATION-3.0.md, MIGRATION-3.0.zh.md
    return bool(re.match(r"^docs/MIGRATION-[\d.]+(\.(zh|en))?\.md$", path))


def cursor_rules_glob_covers(path: str) -> bool:
    return bool(re.match(r"^\.cursor/rules/.+\.mdc$", path))


def is_glob_covered(path: str) -> bool:
    return (
        adr_glob_covers(path)
        or workflow_glob_covers(path)
        or migration_glob_covers(path)
        or cursor_rules_glob_covers(path)
    )


# ---------------------------------------------------------------------------
# Drift detection
# ---------------------------------------------------------------------------

@dataclass
class DriftReport:
    listed_missing: list[str] = field(default_factory=list)
    tracked_unlisted: list[str] = field(default_factory=list)
    path_drift_candidates: list[tuple[str, str]] = field(default_factory=list)

    @property
    def has_any(self) -> bool:
        return bool(
            self.listed_missing
            or self.tracked_unlisted
            or self.path_drift_candidates
        )

    @property
    def has_strict(self) -> bool:
        return bool(self.listed_missing or self.tracked_unlisted)


def detect_drift(declared: set[str], tracked: set[str]) -> DriftReport:
    rep = DriftReport()

    # ---------- Resolve basename-only inventory entries ---------------------
    # When inventory mentions only a basename (e.g. `_version.py`,
    # `letter-to-admin.zh.md`), accept any unique tracked file whose basename
    # matches AND lives under a governed root. This mirrors how a human reader
    # would interpret the inventory.
    tracked_by_basename: dict[str, list[str]] = {}
    for t in tracked:
        tracked_by_basename.setdefault(Path(t).name, []).append(t)

    resolved_basename_paths: set[str] = set()
    unresolved_basenames: set[str] = set()
    for p in declared:
        if "/" in p or p.endswith("/"):
            continue  # full paths handled in Class 1 below
        candidates = [
            t for t in tracked_by_basename.get(p, []) if is_governed(t)
        ]
        if not candidates:
            candidates = tracked_by_basename.get(p, [])
        if candidates:
            resolved_basename_paths.update(candidates)
        else:
            unresolved_basenames.add(p)

    declared_full = {p for p in declared if "/" in p or p.endswith("/")}

    # ---------- Class 1: listed but not tracked -----------------------------
    def _is_template(p: str) -> bool:
        if "{" in p and "}" in p:
            return True
        if "X.Y.Z" in p or "X_Y_Z" in p:
            return True
        if "X.Y" in p:  # e.g. MIGRATION-X.Y.md
            return True
        if "date-seq" in p:
            return True
        # Uppercase placeholder filename like ROLE.md / TEAM.md (template stub).
        name = p.rsplit("/", 1)[-1]
        stem = name.rsplit(".", 1)[0]
        if stem.isupper() and stem.isalpha() and len(stem) >= 3:
            return True
        return False

    for p in sorted(declared_full - tracked):
        if p.endswith("/"):
            anything = any(t.startswith(p) for t in tracked)
            if not anything:
                rep.listed_missing.append(p)
            continue
        if _is_template(p):
            continue
        rep.listed_missing.append(p)

    for p in sorted(unresolved_basenames):
        if _is_template(p):
            continue
        rep.listed_missing.append(p)

    # ---------- Class 2: tracked, governed, not enumerated ------------------
    declared_norm = set(declared) | resolved_basename_paths
    for t in sorted(tracked):
        if not is_governed(t):
            continue
        if t in declared_norm:
            continue
        if is_glob_covered(t):
            continue
        rep.tracked_unlisted.append(t)

    # ---------- Class 3: light fuzzy rename detection -----------------------
    for missing in rep.listed_missing:
        bn = Path(missing).name
        for t in tracked:
            if Path(t).name == bn and t != missing:
                rep.path_drift_candidates.append((missing, t))
                break

    return rep


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def render_text(rep: DriftReport) -> str:
    lines: list[str] = []
    lines.append("=" * 72)
    lines.append("FCoP Inventory Drift Audit — RULES §2 vs git ls-files")
    lines.append("=" * 72)

    if not rep.has_any:
        lines.append("[OK] 无漂移 / no drift detected")
        lines.append("    zh: RULES-release-file-inventory §2 与 git ls-files 完全对齐")
        lines.append("    en: RULES inventory §2 is fully aligned with tracked files")
        return "\n".join(lines)

    if rep.listed_missing:
        lines.append(f"[FAIL] Class 1 · 清单有、仓库无 (n={len(rep.listed_missing)})")
        lines.append("       zh: 清单声明的文件已不在 git ls-files 中")
        lines.append("       en: paths declared in inventory are absent from tracked tree")
        for p in rep.listed_missing:
            lines.append(f"       - {p}")

    if rep.tracked_unlisted:
        lines.append(f"[FAIL] Class 2 · 仓库有、清单无 (n={len(rep.tracked_unlisted)})")
        lines.append("       zh: 仓库已追踪但清单未列入(governed root 内)")
        lines.append("       en: tracked under governed root but not enumerated in inventory")
        for p in rep.tracked_unlisted:
            lines.append(f"       - {p}")

    if rep.path_drift_candidates:
        lines.append(f"[WARN] Class 3 · 路径漂移候选 (n={len(rep.path_drift_candidates)})")
        lines.append("       zh: 同名文件在仓库另一路径 — 可能是重命名而清单未跟上")
        lines.append("       en: same basename found at a different path — possible rename")
        for old, new in rep.path_drift_candidates:
            lines.append(f"       - inventory says: {old}")
            lines.append(f"         tracked at:    {new}")

    lines.append("-" * 72)
    lines.append(
        f"Summary: missing={len(rep.listed_missing)} "
        f"unlisted={len(rep.tracked_unlisted)} "
        f"renamed?={len(rep.path_drift_candidates)}"
    )
    return "\n".join(lines)


def render_json(rep: DriftReport) -> str:
    return json.dumps(
        {
            "listed_missing": rep.listed_missing,
            "tracked_unlisted": rep.tracked_unlisted,
            "path_drift_candidates": [
                {"inventory_says": a, "tracked_at": b}
                for a, b in rep.path_drift_candidates
            ],
        },
        ensure_ascii=False, indent=2,
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    # Force UTF-8 stdout on Windows consoles so bilingual output isn't garbled.
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception:
        pass
    ap = argparse.ArgumentParser(
        description="Audit RULES-release-file-inventory §2 against git ls-files",
    )
    ap.add_argument("--json", action="store_true", help="emit JSON only")
    ap.add_argument(
        "--strict", action="store_true",
        help="fail (exit 1) on Class 1 OR Class 2 drift (default: same)",
    )
    ap.add_argument(
        "--lenient", action="store_true",
        help="warn-only on Class 2 (tracked-but-unlisted); fail only on Class 1",
    )
    args = ap.parse_args()

    if not INVENTORY.exists():
        print(f"::error::inventory not found: {INVENTORY}", file=sys.stderr)
        return 1

    text = INVENTORY.read_text(encoding="utf-8")
    declared = parse_inventory_paths(text)
    tracked = list_tracked_files()
    rep = detect_drift(declared, tracked)

    if args.json:
        print(render_json(rep))
    else:
        print(render_text(rep))

    if args.lenient:
        return 1 if rep.listed_missing else 0
    return 1 if rep.has_strict else 0


if __name__ == "__main__":
    sys.exit(main())
