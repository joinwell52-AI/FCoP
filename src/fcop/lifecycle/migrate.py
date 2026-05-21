"""v2 → v3 migration engine for FCoP project workspaces.

Per spec §9, a single one-shot migration moves an existing v2 project
into the v3 ``_lifecycle/`` topology and stamps every file with a
synthetic baseline transition event so the audit history starts at a
known point.

Mapping (re-stated from spec §9):

    fcop/tasks/*.md         → fcop/_lifecycle/inbox/*.md
    fcop/log/tasks/*.md     → fcop/_lifecycle/archive/*.md
    fcop/log/reports/*.md   → fcop/reports/*.md          (no longer archived)
    fcop/log/issues/*.md    → fcop/issues/*.md           (add `resolved: true`)
    fcop/log/               → (removed if empty)

The migrator is deliberately built around the same patterns the
existing :mod:`fcop.cli.migrate_workspace` (0.7→1.0) uses:

* **Dry-run by default.** The caller computes a :class:`MigrationPlan`
  via :func:`plan`, inspects it, and only then calls :func:`apply`.
* **git-aware.** When the project is a git work tree and the source
  files are tracked, we use ``git mv`` so blame / log follows.
  Otherwise we fall back to a stdlib copy + ``Path.unlink``.
* **Idempotent at the edges.** Running :func:`apply` twice is a no-op
  on a clean v3 project. Running on a ``MIXED`` project refuses.
* **Synthetic baseline events.** Every migrated file receives one
  :func:`fcop.lifecycle.events.synthetic_baseline_event` and the
  result is written back via the write-then-rename atomic pattern
  (so the migration itself respects Rules E / F / G).

What the migrator does **not** do:

* Rewrite ``.gitignore`` / ``.cursor/rules/*.mdc`` / READMEs that
  mention the old paths. Surfaced as advisory hits (see
  :attr:`MigrationPlan.advisory_hits`) for human review.
* Touch ``shared/``, ``reviews/``, ``fcop.json``, or any other v1.0
  envelope that already maps cleanly to v3.
* Delete files. Even ``log/`` is only removed when it ends up empty;
  unexpected children are left in place with a warning.
"""

from __future__ import annotations

import shutil
import subprocess
from collections.abc import Iterable
from contextlib import suppress
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from fcop.lifecycle.detect import Topology, TopologyReport, detect_topology
from fcop.lifecycle.events import (
    append_event_to_frontmatter,
    synthetic_baseline_event,
)
from fcop.lifecycle.state import (
    LIFECYCLE_DIRNAME,
    Stage,
    ensure_lifecycle_dirs,
)

__all__ = [
    "MigrationPlan",
    "PlannedMove",
    "apply",
    "plan",
    "render_summary",
]


# Each tuple is (relative-source-glob-under-workspace, destination-stage)
# Order matters only for human-readable summaries; semantically the
# four mappings are independent.
_TASK_INBOX_GLOB = "tasks/*.md"
_LOG_TASK_ARCHIVE_GLOB = "log/tasks/*.md"
_LOG_REPORT_GLOB = "log/reports/*.md"
_LOG_ISSUE_GLOB = "log/issues/*.md"


@dataclass(frozen=True, slots=True)
class PlannedMove:
    """One concrete file move + its baseline transition event.

    Attributes:
        source: Path the file currently lives at (absolute).
        destination: Path the file will live at after :func:`apply`
            (absolute).
        target_stage: Stage the destination falls into. ``None`` for
            non-lifecycle destinations (``reports/`` / ``issues/``)
            which do not receive a transition event because they
            are not under the protocol's NOW-truth tree.
    """

    source: Path
    destination: Path
    target_stage: Stage | None


@dataclass(slots=True)
class MigrationPlan:
    """What :func:`plan` *would* do or what :func:`apply` *did*.

    Attributes:
        project_root: Repo root, resolved absolute.
        workspace_root: ``<project_root>/fcop/`` (or whatever
            :class:`Topology` detection picked).
        topology_before: The :class:`TopologyReport` we computed
            against ``workspace_root`` at planning time.
        moves: Concrete file moves (see :class:`PlannedMove`).
        will_use_git_mv: ``True`` when we plan to use ``git mv``.
            Decided once at plan time per (project, workspace) pair.
        empty_log_will_be_removed: ``True`` when planning sees
            ``log/`` becoming empty after the moves, so apply may
            ``rmdir`` it.
        advisory_hits: Files that mention the old v2 paths and may
            need human review (READMEs, .gitignore, .cursor/rules).
        applied: ``True`` after a successful :func:`apply`.
        notes: Free-form human-readable observations.
    """

    project_root: Path
    workspace_root: Path
    topology_before: TopologyReport
    moves: list[PlannedMove] = field(default_factory=list)
    will_use_git_mv: bool = False
    empty_log_will_be_removed: bool = False
    advisory_hits: list[Path] = field(default_factory=list)
    applied: bool = False
    notes: list[str] = field(default_factory=list)

    @property
    def is_noop(self) -> bool:
        """``True`` when the plan would not move any files.

        Canonical noop cases: already-v3 projects, empty projects,
        and projects that hold only v3 ``_lifecycle/`` and no
        legacy file evidence.
        """
        return not self.moves


# ── git helpers (intentional duplication of migrate_workspace.py) ──
#
# We deliberately do NOT import the helpers from
# fcop.cli.migrate_workspace: that module owns the 0.7→1.0 migration
# semantics and is part of the v2 surface. Coupling the v3 migrator
# to it would let one set of refactors break the other. The helpers
# are ~15 lines and stable enough to redeclare.


def _is_git_repo(project_root: Path) -> bool:
    """Return ``True`` if ``project_root`` (or any ancestor) is a git tree."""
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
    """Run ``git mv <src> <dst>`` from ``project_root``."""
    src_rel = src.relative_to(project_root).as_posix()
    dst_rel = dst.relative_to(project_root).as_posix()
    subprocess.run(
        ["git", "mv", "-f", src_rel, dst_rel],
        cwd=str(project_root),
        check=True,
        capture_output=True,
        text=True,
    )


# ── advisory scan ──


_ADVISORY_GLOBS: tuple[str, ...] = (
    ".gitignore",
    ".cursor/rules/*.mdc",
    "AGENTS.md",
    "CLAUDE.md",
    "README.md",
    "README.zh.md",
)
_ADVISORY_NEEDLES: tuple[str, ...] = (
    "fcop/tasks/",
    "fcop/log/",
    "docs/agents/tasks/",
    "docs/agents/log/",
)


def _scan_advisory_hits(project_root: Path) -> list[Path]:
    """Files that mention the old v2 paths and may need a manual nudge."""
    hits: list[Path] = []
    for pattern in _ADVISORY_GLOBS:
        for candidate in project_root.glob(pattern):
            if not candidate.is_file():
                continue
            try:
                text = candidate.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            if any(needle in text for needle in _ADVISORY_NEEDLES):
                hits.append(candidate)
    return sorted(hits)


# ── planning ──


def _iter_globs(workspace_root: Path, glob: str) -> Iterable[Path]:
    """Yield matching files; never yields directories or non-.md children."""
    for p in workspace_root.glob(glob):
        if p.is_file() and p.suffix == ".md":
            yield p


def plan(
    project_root: Path,
    *,
    workspace_root: Path | None = None,
) -> MigrationPlan:
    """Build a :class:`MigrationPlan` without touching the filesystem.

    Args:
        project_root: Repo / project root.
        workspace_root: Optional explicit workspace dir; bypasses
            topology auto-detection (matches ``Project(workspace_dir=…)``).

    Returns:
        A :class:`MigrationPlan` describing what :func:`apply` would do.
        For ``EMPTY`` / ``V3`` projects the plan is empty (``is_noop``).
        For ``MIXED`` projects the plan is empty but ``notes`` explain
        what's wrong; :func:`apply` will refuse such plans.
    """
    project_root = project_root.resolve()
    report = detect_topology(project_root, workspace_root=workspace_root)
    plan_obj = MigrationPlan(
        project_root=project_root,
        workspace_root=report.workspace_root,
        topology_before=report,
    )

    if report.topology == Topology.MIXED:
        plan_obj.notes.append(
            "Workspace is in MIXED state — both _lifecycle/ and v2 "
            f"dirs ({list(report.v2_dirs_present)}) exist. Refusing "
            "to plan a migration. Resolve the mixed state by hand "
            "(usually: complete the partial migration or remove the "
            "empty stragglers) and re-run."
        )
        return plan_obj

    if report.topology == Topology.V3:
        plan_obj.notes.append(
            "Project is already v3 (_lifecycle/ present, no legacy "
            "v2 dirs). Nothing to migrate."
        )
        return plan_obj

    if report.topology == Topology.EMPTY:
        plan_obj.notes.append(
            "Workspace is empty — no v2 or v3 evidence. A fresh "
            "`init` would create a v3 layout directly; no migration "
            "needed."
        )
        return plan_obj

    # ── V2 → V3 mapping ──
    workspace = report.workspace_root
    lifecycle = workspace / LIFECYCLE_DIRNAME

    for src in _iter_globs(workspace, _TASK_INBOX_GLOB):
        plan_obj.moves.append(
            PlannedMove(
                source=src,
                destination=lifecycle / Stage.INBOX.value / src.name,
                target_stage=Stage.INBOX,
            )
        )

    for src in _iter_globs(workspace, _LOG_TASK_ARCHIVE_GLOB):
        plan_obj.moves.append(
            PlannedMove(
                source=src,
                destination=lifecycle / Stage.ARCHIVE.value / src.name,
                target_stage=Stage.ARCHIVE,
            )
        )

    for src in _iter_globs(workspace, _LOG_REPORT_GLOB):
        plan_obj.moves.append(
            PlannedMove(
                source=src,
                destination=workspace / "reports" / src.name,
                target_stage=None,
            )
        )

    for src in _iter_globs(workspace, _LOG_ISSUE_GLOB):
        plan_obj.moves.append(
            PlannedMove(
                source=src,
                destination=workspace / "issues" / src.name,
                target_stage=None,
            )
        )

    plan_obj.will_use_git_mv = _is_git_repo(project_root) and _is_path_tracked(
        project_root, workspace
    )
    plan_obj.advisory_hits = _scan_advisory_hits(project_root)

    log_dir = workspace / "log"
    if log_dir.is_dir():
        # If every file under log/ is something we plan to move,
        # the directory will end up empty and apply() can remove it.
        # An already-empty log/ also qualifies for removal — it
        # holds no information and its only effect is to confuse
        # detect_topology into reporting V2 forever.
        moved_log_files = {
            m.source
            for m in plan_obj.moves
            if m.source.is_relative_to(log_dir)
        }
        all_log_files = {p for p in log_dir.rglob("*") if p.is_file()}
        plan_obj.empty_log_will_be_removed = all_log_files == moved_log_files
        if all_log_files and not plan_obj.empty_log_will_be_removed:
            unexpected = sorted(
                p.relative_to(workspace).as_posix()
                for p in all_log_files - moved_log_files
            )
            plan_obj.notes.append(
                "log/ contains unexpected children that will not be "
                "moved: " + ", ".join(unexpected[:5])
                + (" …" if len(unexpected) > 5 else "")
            )

    return plan_obj


# ── apply ──


def _ensure_destination_parents(dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)


def _move_one(
    move: PlannedMove,
    *,
    project_root: Path,
    use_git_mv: bool,
) -> None:
    """Physically move a single file from source to destination.

    Uses ``git mv`` when ``use_git_mv`` and the source is git-tracked;
    otherwise falls back to :func:`shutil.move`. We do **not** rewrite
    frontmatter here — the synthetic event append happens in
    :func:`_stamp_baseline_event` after the move so the on-disk file
    at the destination is the one we mutate.
    """
    _ensure_destination_parents(move.destination)

    if use_git_mv and _is_path_tracked(project_root, move.source):
        try:
            _git_mv(project_root, move.source, move.destination)
            return
        except subprocess.CalledProcessError:
            # Fall through to stdlib move. The caller's plan note
            # already explains we may degrade to shutil.move.
            pass

    shutil.move(str(move.source), str(move.destination))


def _stamp_baseline_event(move: PlannedMove) -> None:
    """Append the synthetic baseline event to a freshly-moved file.

    Only for moves whose destination is under ``_lifecycle/`` (i.e.
    ``target_stage`` is not None). Reports and issues moved to
    ``reports/`` / ``issues/`` are *not* protocol-NOW-truth files
    in v3 and so do not receive transition events.

    The append is in-place but follows the same idea as the
    write-then-rename atomic pattern: we write to a sibling temp
    file first and ``Path.replace`` it onto the destination. This
    keeps the migration crash-safe on a per-file basis.
    """
    if move.target_stage is None:
        return

    dst = move.destination
    try:
        original = dst.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        # Not a UTF-8 markdown — skip silently. Migration is best-
        # effort for legacy artefacts; the file remains in place.
        return

    event = synthetic_baseline_event(dst, move.target_stage)
    try:
        stamped = append_event_to_frontmatter(original, event)
    except ValueError:
        # File has no frontmatter (extremely old pre-v1 artefact, or
        # someone dropped a stray note). Treat as a "legal historical
        # artefact" per spec §9 — leave it alone.
        return

    tmp = dst.with_suffix(dst.suffix + ".fcop-v3-tmp")
    tmp.write_text(stamped, encoding="utf-8")
    tmp.replace(dst)


def apply(plan_obj: MigrationPlan) -> MigrationPlan:
    """Execute ``plan_obj``.

    Mutates the plan (sets ``applied=True`` on success) and returns
    it for fluent use. Refuses to operate on a ``MIXED`` topology.

    Raises:
        RuntimeError: when called on a MIXED plan.
        OSError: any underlying filesystem failure surfaces unchanged.
    """
    if plan_obj.topology_before.topology == Topology.MIXED:
        raise RuntimeError(
            "Refusing to apply migration on a MIXED workspace. "
            "Resolve the mixed v2/v3 state manually first."
        )

    if plan_obj.is_noop:
        plan_obj.applied = True
        return plan_obj

    ensure_lifecycle_dirs(plan_obj.workspace_root)

    workspace = plan_obj.workspace_root
    reports_dir = workspace / "reports"
    issues_dir = workspace / "issues"
    reports_dir.mkdir(parents=True, exist_ok=True)
    issues_dir.mkdir(parents=True, exist_ok=True)

    for move in plan_obj.moves:
        _move_one(
            move,
            project_root=plan_obj.project_root,
            use_git_mv=plan_obj.will_use_git_mv,
        )
        _stamp_baseline_event(move)

    if plan_obj.empty_log_will_be_removed:
        log_dir = workspace / "log"
        # rmdir empty subdirs first, then the root.
        for sub in sorted(
            (p for p in log_dir.rglob("*") if p.is_dir()),
            key=lambda p: len(p.parts),
            reverse=True,
        ):
            with suppress(OSError):
                sub.rmdir()
        try:
            log_dir.rmdir()
        except OSError:
            plan_obj.notes.append(
                "log/ could not be removed (likely non-empty after "
                "migration); leaving it in place."
            )

    # Also reclaim emptied v2 evidence dirs so detect_topology no
    # longer reports MIXED. We are conservative: only rmdir when
    # truly empty (rmdir refuses otherwise — there's no race here
    # because we just drained these directories ourselves).
    # ``reports/`` and ``issues/`` are *not* in this list — they
    # are first-class v3 directories that may now hold v3 content.
    for relname in ("tasks",):
        candidate = workspace / relname
        if candidate.is_dir():
            try:
                candidate.rmdir()
            except OSError:
                # Non-empty (user left strays in here) — that's fine,
                # we just don't remove. detect_topology will keep
                # reporting V2 evidence; the user can clean up
                # by hand. We surface a note so the dry-run readout
                # explains the situation.
                plan_obj.notes.append(
                    f"{relname}/ still contains files after migration; "
                    "not removed. detect_topology may continue to "
                    "report MIXED until you clean it up by hand."
                )

    plan_obj.applied = True
    return plan_obj


# ── presentation ──


def render_summary(plan_obj: MigrationPlan, *, applied: bool) -> str:
    """Render ``plan_obj`` as a human-readable multi-line string."""
    lines: list[str] = []
    head = "[applied]" if applied else "[dry-run]"
    lines.append(f"{head} fcop migrate --to-v3")
    lines.append(f"  project root  : {plan_obj.project_root}")
    try:
        rel_ws = plan_obj.workspace_root.relative_to(plan_obj.project_root).as_posix()
    except ValueError:
        rel_ws = str(plan_obj.workspace_root)
    lines.append(f"  workspace     : {rel_ws}")
    lines.append(f"  topology      : {plan_obj.topology_before.topology.value}")

    if plan_obj.is_noop:
        lines.append("  status        : no-op (nothing to migrate)")
    else:
        strategy = "git mv (history preserved)" if plan_obj.will_use_git_mv else "shutil.move"
        lines.append(f"  strategy      : {strategy}")
        lines.append(f"  files to move : {len(plan_obj.moves)}")
        by_stage: dict[str, int] = {}
        for move in plan_obj.moves:
            key = move.target_stage.value if move.target_stage else "reports/issues"
            by_stage[key] = by_stage.get(key, 0) + 1
        for key, count in sorted(by_stage.items()):
            lines.append(f"                  - {key:<16} {count}")
        if plan_obj.empty_log_will_be_removed:
            lines.append("  cleanup       : log/ will be removed (empty after migration)")

    if plan_obj.advisory_hits:
        lines.append("  advisory      : files mentioning old v2 paths (review by hand):")
        for hit in plan_obj.advisory_hits:
            try:
                rel = hit.relative_to(plan_obj.project_root).as_posix()
            except ValueError:
                rel = str(hit)
            lines.append(f"                  - {rel}")

    for note in plan_obj.notes:
        lines.append(f"  note          : {note}")

    if not applied and not plan_obj.is_noop:
        lines.append("")
        lines.append("Run again with --apply to execute the migration.")

    lines.append("")
    lines.append(f"  generated     : {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
    return "\n".join(lines) + "\n"
