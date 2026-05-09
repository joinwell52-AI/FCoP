"""``fcop migrate-workspace`` subcommand — 0.7.x → 1.0 layout migration.

Implements ADR-0022 §"自动迁移工具": move ``docs/agents/`` to ``fcop/``
(or any ``--target`` directory) while preserving git history, then
write a ``MIGRATED_FROM_DOCS_AGENTS.md`` breadcrumb so the move is
discoverable + reversible.

Design constraints (per ADR-0022):

* **Dry-run by default.** Users must opt in with ``--apply``.
* **git-aware.** When the project is a git repo *and* the source tree
  is git-tracked, use ``git mv`` so history follows. Otherwise fall
  back to ``shutil.move`` and emit a warning.
* **Idempotent.** Running ``--apply`` twice is a no-op (and reports it
  as such; exit code 0).
* **Conservative.** We only move the ``docs/agents/`` subtree itself
  and leave ``docs/`` alone (it may contain unrelated user docs). We
  do **not** rewrite ``.gitignore`` or ``.cursor/rules/*.mdc`` — instead
  we surface a list of files that mention ``docs/agents/`` and suggest
  the user review them by hand. Auto-rewriting carries a risk of
  damaging unrelated prose; the trade-off is documented in ADR-0022
  §"Design Details" item 3.
* **Pure stdlib.** No new runtime deps. ``git`` is invoked via
  ``subprocess`` only when present + applicable.

The subcommand is intentionally narrow: it is a one-shot migration
tool, not a general workspace-management CLI. The expected workflow is

    fcop migrate-workspace             # see what would happen
    fcop migrate-workspace --apply     # do it (single commit recommended)
    git status                         # review
    git commit -m "fcop: migrate to v1.0 workspace layout"

"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import IO

# Default 0.7.x source location and v1.0 default target. Both are
# repo-root-relative. ADR-0022 calls these out explicitly.
LEGACY_WORKSPACE_RELPATH = Path("docs") / "agents"
DEFAULT_TARGET_RELPATH = Path("fcop")

# Files that frequently reference the old ``docs/agents/`` path. These
# are surfaced as "advisory" hits — never auto-rewritten — because
# they may also contain user prose where the literal string is wanted.
_ADVISORY_HINT_GLOBS = (
    ".gitignore",
    ".cursor/rules/*.mdc",
    "AGENTS.md",
    "CLAUDE.md",
    "README.md",
    "README.zh.md",
)

# A short list of subdirectories we expect to find inside a healthy
# 0.7.x workspace; used purely to make the dry-run summary readable.
_KNOWN_SUBDIRS = (
    "tasks",
    "reports",
    "issues",
    "shared",
    "log",
    "reviews",  # v1.0 ADR-0017 — created lazily on first write_review
)


# ── Result types ──────────────────────────────────────────────────────


@dataclass(slots=True)
class MigrationPlan:
    """What ``migrate-workspace`` *would* do (dry run) or *did* do.

    Returned by :func:`run` so callers (tests, future MCP tool wrapper)
    can introspect the outcome without re-parsing stdout.

    Attributes:
        project_root: Resolved absolute path to the project root.
        source: Resolved absolute path to ``docs/agents/`` (or
            whatever ``--source`` pointed to).
        target: Resolved absolute path to the destination (default
            ``<root>/fcop``).
        already_migrated: ``True`` when ``target`` exists and ``source``
            does not — the canonical "nothing to do" idempotent state.
        source_missing: ``True`` when neither ``source`` nor ``target``
            exists; this usually means the project isn't initialised
            yet and the migration is a no-op.
        conflict: ``True`` when **both** ``source`` and ``target``
            exist. Aborts ``--apply`` (per ADR-0022 §"启动时 detect
            行为" — both-exist is an error in v1.0).
        will_use_git_mv: ``True`` when we plan to invoke ``git mv``
            (project is a git repo and the source tree is tracked).
        moved_entries: Top-level entries inside ``source`` that will
            move (or did move when ``apply=True``).
        advisory_hits: Files outside the workspace that mention the
            literal string ``docs/agents`` and *might* need a manual
            update post-migration.
        breadcrumb_path: Where the ``MIGRATED_FROM_DOCS_AGENTS.md``
            sentinel was (or would be) written.
        applied: ``True`` when ``--apply`` was requested **and** the
            move completed successfully.
        notes: Free-form lines printed in the human-readable summary.
    """

    project_root: Path
    source: Path
    target: Path
    already_migrated: bool = False
    source_missing: bool = False
    conflict: bool = False
    will_use_git_mv: bool = False
    moved_entries: list[str] = field(default_factory=list)
    advisory_hits: list[Path] = field(default_factory=list)
    breadcrumb_path: Path | None = None
    applied: bool = False
    notes: list[str] = field(default_factory=list)


# ── git helpers ───────────────────────────────────────────────────────


def _is_git_repo(project_root: Path) -> bool:
    """Return ``True`` if ``project_root`` (or any ancestor) is a git
    work tree.

    We intentionally shell out to ``git`` rather than poking ``.git/``
    directly because the latter would miss worktrees and submodules.
    A missing ``git`` binary, an unrelated ``CalledProcessError``, or
    a non-zero exit all map to ``False`` — degrade silently.
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=str(project_root),
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
    except (FileNotFoundError, OSError, subprocess.TimeoutExpired):
        return False
    return result.returncode == 0 and result.stdout.strip() == "true"


def _is_path_tracked(project_root: Path, path: Path) -> bool:
    """``True`` if at least one file under ``path`` is git-tracked."""
    try:
        rel = path.relative_to(project_root)
    except ValueError:
        return False
    try:
        result = subprocess.run(
            ["git", "ls-files", "--", str(rel).replace("\\", "/")],
            cwd=str(project_root),
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
    except (FileNotFoundError, OSError, subprocess.TimeoutExpired):
        return False
    return result.returncode == 0 and result.stdout.strip() != ""


def _git_mv(project_root: Path, src: Path, dst: Path) -> None:
    """Run ``git mv <src> <dst>`` so history follows.

    Caller has already ensured we're in a git repo and ``src`` is
    tracked. We escalate the subprocess CalledProcessError unchanged
    so the human-readable summary surfaces git's own error message
    (typically "fatal: not under version control" or similar).
    """
    src_rel = src.relative_to(project_root).as_posix()
    dst_rel = dst.relative_to(project_root).as_posix()
    subprocess.run(
        ["git", "mv", src_rel, dst_rel],
        cwd=str(project_root),
        check=True,
        capture_output=True,
        text=True,
    )


# ── advisory scan ─────────────────────────────────────────────────────


def _scan_advisory_hits(project_root: Path) -> list[Path]:
    """Return files in :data:`_ADVISORY_HINT_GLOBS` that mention the
    literal ``docs/agents``.

    These are surfaced for the user to review by hand — we never
    rewrite them automatically. The intent is to remind users that
    rule files and README references may need updating, without the
    risk of corrupting unrelated prose.
    """
    hits: list[Path] = []
    for pattern in _ADVISORY_HINT_GLOBS:
        for candidate in project_root.glob(pattern):
            if not candidate.is_file():
                continue
            try:
                text = candidate.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            if "docs/agents" in text:
                hits.append(candidate)
    return sorted(hits)


# ── breadcrumb ────────────────────────────────────────────────────────


_BREADCRUMB_TEMPLATE = """\
# Migrated from `docs/agents/`

This directory was moved here by `fcop migrate-workspace` on
**{stamp}** (per ADR-0022).

- **Old path**: `{old}`
- **New path**: `{new}`
- **fcop CLI version**: `{version}`

If you need to roll back, the inverse `git mv` plus the safety
backup of this file should be sufficient. See ADR-0022
§"Backwards Compatibility" for the long-term escape hatch:
`Project(workspace_dir="docs/agents/")` remains legal forever.
"""


def _write_breadcrumb(target: Path, project_root: Path) -> Path:
    """Write the ``MIGRATED_FROM_DOCS_AGENTS.md`` sentinel inside
    ``target`` and return its path."""
    from fcop._version import __version__  # local: avoid cycle at import time

    breadcrumb = target / "MIGRATED_FROM_DOCS_AGENTS.md"
    breadcrumb.write_text(
        _BREADCRUMB_TEMPLATE.format(
            stamp=datetime.now(timezone.utc).isoformat(timespec="seconds"),
            old=LEGACY_WORKSPACE_RELPATH.as_posix(),
            new=target.relative_to(project_root).as_posix(),
            version=__version__,
        ),
        encoding="utf-8",
    )
    return breadcrumb


# ── core ──────────────────────────────────────────────────────────────


def plan(
    project_root: Path,
    *,
    source: Path | None = None,
    target: Path | None = None,
) -> MigrationPlan:
    """Build a :class:`MigrationPlan` without touching the filesystem.

    Pure inspection. Used both by ``--dry-run`` (default) and by
    ``--apply`` to compute the work it's about to do.
    """
    project_root = project_root.resolve()
    src = (source or (project_root / LEGACY_WORKSPACE_RELPATH)).resolve()
    dst = (target or (project_root / DEFAULT_TARGET_RELPATH)).resolve()

    p = MigrationPlan(project_root=project_root, source=src, target=dst)

    src_exists = src.exists()
    dst_exists = dst.exists()

    if not src_exists and dst_exists:
        p.already_migrated = True
        p.notes.append(
            f"target {dst.relative_to(project_root).as_posix()} exists; "
            f"source {src.relative_to(project_root).as_posix()} does not. "
            "Nothing to migrate."
        )
        return p

    if not src_exists and not dst_exists:
        p.source_missing = True
        p.notes.append(
            f"neither {src.relative_to(project_root).as_posix()} nor "
            f"{dst.relative_to(project_root).as_posix()} exists. "
            "Project not initialised? Nothing to migrate."
        )
        return p

    if src_exists and dst_exists:
        p.conflict = True
        p.notes.append(
            f"BOTH {src.relative_to(project_root).as_posix()} and "
            f"{dst.relative_to(project_root).as_posix()} exist. "
            "Refusing to merge automatically — please remove one or "
            "merge by hand. (See ADR-0022 §'启动时 detect 行为'.)"
        )
        return p

    # Only source exists — this is the canonical case.
    p.moved_entries = sorted(
        entry.name
        for entry in src.iterdir()
        if entry.name != "MIGRATED_FROM_DOCS_AGENTS.md"
    )
    p.will_use_git_mv = _is_git_repo(project_root) and _is_path_tracked(
        project_root, src
    )
    p.advisory_hits = _scan_advisory_hits(project_root)
    p.breadcrumb_path = dst / "MIGRATED_FROM_DOCS_AGENTS.md"

    expected = set(_KNOWN_SUBDIRS)
    seen = set(p.moved_entries)
    surprise = sorted(seen - expected - {"fcop.json", ".keep"})
    if surprise:
        p.notes.append(
            "Note: the following entries are not part of the standard "
            "FCoP layout but will move along with everything else: "
            + ", ".join(surprise)
        )

    return p


def apply(p: MigrationPlan) -> MigrationPlan:
    """Execute the move described by ``p``.

    Mutates ``p`` (sets ``applied=True`` on success) and returns it
    for fluent use. Raises if the underlying move fails — callers
    should wrap in try/except.
    """
    if p.already_migrated or p.source_missing:
        # Idempotent: no-op cases don't touch disk and report success.
        p.applied = True
        return p

    if p.conflict:
        raise RuntimeError(
            "Refusing to apply: both source and target exist "
            f"({p.source} and {p.target}). Please resolve manually."
        )

    p.target.parent.mkdir(parents=True, exist_ok=True)

    if p.will_use_git_mv:
        try:
            _git_mv(p.project_root, p.source, p.target)
        except subprocess.CalledProcessError as exc:
            stderr = exc.stderr or ""
            p.notes.append(
                "git mv failed; falling back to shutil.move. "
                f"git stderr: {stderr.strip()}"
            )
            shutil.move(str(p.source), str(p.target))
            p.will_use_git_mv = False
    else:
        shutil.move(str(p.source), str(p.target))

    p.breadcrumb_path = _write_breadcrumb(p.target, p.project_root)
    p.applied = True
    return p


# ── presentation ──────────────────────────────────────────────────────


def render_summary(p: MigrationPlan, *, applied: bool) -> str:
    """Format ``p`` as a human-readable multi-line string for stdout."""
    lines: list[str] = []
    head = "[applied]" if applied else "[dry-run]"
    lines.append(f"{head} fcop migrate-workspace")
    lines.append(f"  project root : {p.project_root}")
    lines.append(f"  source       : {p.source.relative_to(p.project_root).as_posix()}")
    lines.append(f"  target       : {p.target.relative_to(p.project_root).as_posix()}")

    if p.already_migrated:
        lines.append("  status       : already migrated (no-op)")
    elif p.source_missing:
        lines.append("  status       : source does not exist (no-op)")
    elif p.conflict:
        lines.append("  status       : ABORT — both source and target exist")
    else:
        lines.append(
            "  strategy     : "
            + ("git mv (history preserved)" if p.will_use_git_mv else "shutil.move")
        )
        lines.append(
            f"  entries      : {len(p.moved_entries)} top-level "
            "(" + ", ".join(p.moved_entries) + ")"
            if p.moved_entries
            else "  entries      : 0 (empty workspace)"
        )
        if p.breadcrumb_path is not None:
            lines.append(
                "  breadcrumb   : "
                + p.breadcrumb_path.relative_to(p.project_root).as_posix()
            )
        if p.advisory_hits:
            lines.append("  advisory     : files referencing 'docs/agents' (review by hand):")
            for hit in p.advisory_hits:
                try:
                    rel = hit.relative_to(p.project_root).as_posix()
                except ValueError:
                    rel = str(hit)
                lines.append(f"                 - {rel}")

    for note in p.notes:
        lines.append(f"  note         : {note}")

    if not applied and not (p.already_migrated or p.source_missing or p.conflict):
        lines.append("")
        lines.append("Run again with --apply to execute the migration.")

    return "\n".join(lines) + "\n"


# ── argparse glue ─────────────────────────────────────────────────────


def add_subparser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    """Register the ``migrate-workspace`` subparser on the dispatcher."""
    p = subparsers.add_parser(
        "migrate-workspace",
        help="Migrate FCoP workspace from docs/agents/ to fcop/ (ADR-0022).",
        description=(
            "Move docs/agents/ → fcop/ in this project, preserving git "
            "history when possible. Dry-run by default; pass --apply "
            "to execute."
        ),
    )
    p.add_argument(
        "--apply",
        action="store_true",
        help="Actually perform the move. Without this flag the command is a dry-run.",
    )
    p.add_argument(
        "--target",
        type=Path,
        default=None,
        help="Target directory (relative to project root or absolute). Default: fcop/.",
    )
    p.add_argument(
        "--source",
        type=Path,
        default=None,
        help="Source directory (relative to project root or absolute). Default: docs/agents/.",
    )
    p.add_argument(
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="Project root. Default: current working directory.",
    )
    p.set_defaults(func=_dispatch)


def _dispatch(args: argparse.Namespace, *, stdout: IO[str] | None = None) -> int:
    """argparse callback: run plan(), optionally apply(), print summary."""
    out = stdout or sys.stdout

    project_root = Path(args.project_root).resolve()

    def _resolve(p: Path | None) -> Path | None:
        if p is None:
            return None
        return p if p.is_absolute() else (project_root / p).resolve()

    p = plan(
        project_root,
        source=_resolve(args.source),
        target=_resolve(args.target),
    )

    if args.apply:
        if p.conflict:
            out.write(render_summary(p, applied=False))
            return 2
        try:
            apply(p)
        except Exception as exc:  # noqa: BLE001 - surface any move failure
            out.write(render_summary(p, applied=False))
            out.write(f"ERROR: {exc}\n")
            return 1

    out.write(render_summary(p, applied=args.apply and p.applied))
    return 0


def run(argv: list[str] | None = None, *, stdout: IO[str] | None = None) -> int:
    """Standalone entry point — used by tests so they can drive the
    subcommand without going through the top-level ``fcop`` parser.
    """
    parser = argparse.ArgumentParser(prog="fcop migrate-workspace")
    sub = parser.add_subparsers(dest="cmd", required=True)
    add_subparser(sub)
    args = parser.parse_args(["migrate-workspace", *(argv or [])])
    return _dispatch(args, stdout=stdout)
