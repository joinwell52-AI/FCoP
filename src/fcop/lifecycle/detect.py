"""Topology detection for FCoP project roots.

A project on disk can be in one of four shapes:

* ``EMPTY``  — neither a v2 ``tasks/`` tree nor a v3 ``_lifecycle/``
  tree is present. A fresh ``init`` would create a v3 layout by
  default.
* ``V2``     — has ``tasks/`` / ``log/`` / ``reports/`` / ``issues/``
  but no ``_lifecycle/``. The pre-3.0 layout, fully understood by
  the existing :class:`fcop.Project` facade.
* ``V3``     — has ``_lifecycle/`` (with all 5 stage subdirs) and no
  competing v2 ``tasks/`` directory. The post-3.0 layout, handled
  by :mod:`fcop.lifecycle`.
* ``MIXED``  — both ``_lifecycle/`` and a v2 ``tasks/`` exist
  simultaneously. This is an error condition: it usually means a
  half-finished migration. Callers should refuse to operate (or
  ask the user to resolve it manually) rather than guess which
  is authoritative.

This module is **pure inspection**: nothing here writes, moves, or
creates files. It is safe to call against any path.

The detector understands both the v1.0 default workspace layout
(``<root>/fcop/...``) and the 0.7.x legacy layout
(``<root>/docs/agents/...``) — both are valid v2 shapes, and v3
inherits the same workspace-root convention.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from fcop.lifecycle.state import (
    LIFECYCLE_DIRNAME,
    STAGE_NAMES,
)

__all__ = [
    "DEFAULT_V2_DIRS",
    "Topology",
    "TopologyReport",
    "detect_topology",
    "find_workspace_root",
]


# v2 directory names we consider authoritative signals. The presence
# of any one of these *under the workspace root* (alongside no
# _lifecycle/) is enough to call the layout V2.
#
# Important: ``reports/`` and ``issues/`` are deliberately NOT in
# this list, even though v2 projects create them. They are also
# first-class v3 directories (spec §1.1) and a clean v3 project
# will keep them populated. Including them would make every v3
# project look MIXED forever. The unambiguous v2-only signals are
# ``tasks/`` (replaced by ``_lifecycle/inbox/``) and ``log/``
# (replaced by ``_lifecycle/archive/`` + flat ``reports/`` /
# ``issues/``).
DEFAULT_V2_DIRS: tuple[str, ...] = ("tasks", "log")
"""v2-only subdirectory names whose presence marks a project as v2."""


# Workspace root candidates, in priority order. find_workspace_root
# tries each and returns the first one that contains *some* v2 or v3
# evidence; falls back to the v1.0 default when nothing is found.
_WORKSPACE_CANDIDATES: tuple[str, ...] = ("fcop", "docs/agents")


class Topology(str, Enum):
    """The four possible shapes a project root may be in.

    The ``str`` mixin keeps comparisons against plain string literals
    ergonomic (``topology == "v3"`` works) for code that does not
    want to import the enum.
    """

    EMPTY = "empty"
    V2 = "v2"
    V3 = "v3"
    MIXED = "mixed"


@dataclass(frozen=True, slots=True)
class TopologyReport:
    """The structured result of :func:`detect_topology`.

    Attributes:
        topology: The :class:`Topology` value.
        workspace_root: The directory we inspected. For a v1.0
            project this is ``<project_root>/fcop/``; for 0.7.x
            legacy projects it is ``<project_root>/docs/agents/``.
            For ``EMPTY`` projects, the v1.0 default is returned so
            callers know where ``init`` would land things.
        v2_dirs_present: The subset of :data:`DEFAULT_V2_DIRS` that
            actually exist under the workspace root. Empty when the
            layout is ``V3`` or ``EMPTY``.
        v3_lifecycle_present: Whether ``<workspace_root>/_lifecycle/``
            exists.
        v3_lifecycle_complete: Whether ``_lifecycle/`` exists *and*
            holds all 5 stage subdirs. A ``True`` here is the
            stronger v3-conformance signal.
        notes: Free-form human-readable observations the migrator's
            dry-run pretty-printer can surface to the user.
    """

    topology: Topology
    workspace_root: Path
    v2_dirs_present: tuple[str, ...] = ()
    v3_lifecycle_present: bool = False
    v3_lifecycle_complete: bool = False
    notes: tuple[str, ...] = ()


def _v2_dirs_in(workspace_root: Path) -> tuple[str, ...]:
    """Return the v2 directory names that actually exist under root."""
    return tuple(
        name for name in DEFAULT_V2_DIRS if (workspace_root / name).is_dir()
    )


def _v3_status(workspace_root: Path) -> tuple[bool, bool]:
    """Return ``(present, complete)`` for the ``_lifecycle/`` subtree.

    * ``present``  — ``_lifecycle/`` directory exists.
    * ``complete`` — all 5 stage subdirs also exist.
    """
    lifecycle = workspace_root / LIFECYCLE_DIRNAME
    if not lifecycle.is_dir():
        return False, False
    complete = all((lifecycle / s).is_dir() for s in STAGE_NAMES)
    return True, complete


def find_workspace_root(project_root: Path) -> Path:
    """Return the directory we treat as the FCoP workspace.

    Walks ``_WORKSPACE_CANDIDATES`` in order; returns the first one
    that contains either ``_lifecycle/`` or any of the v2 evidence
    directories. When neither yields a signal, falls back to the
    v1.0 default (``<project_root>/fcop/``) so a subsequent
    ``init`` lands files in the canonical place.
    """
    for rel in _WORKSPACE_CANDIDATES:
        candidate = project_root / rel
        if not candidate.is_dir():
            continue
        if (candidate / LIFECYCLE_DIRNAME).is_dir():
            return candidate
        if _v2_dirs_in(candidate):
            return candidate
    return project_root / _WORKSPACE_CANDIDATES[0]


def detect_topology(
    project_root: Path,
    *,
    workspace_root: Path | None = None,
) -> TopologyReport:
    """Classify the project at ``project_root`` into one of four shapes.

    Args:
        project_root: The repository / project root. We search under
            it for a workspace directory.
        workspace_root: Optional explicit workspace path. When given,
            ``find_workspace_root`` is bypassed — useful for tests
            and for non-standard layouts that ``Project(workspace_dir=…)``
            already supports.

    Returns:
        A :class:`TopologyReport` summarising what was found.

    The detector intentionally never raises. ``MIXED`` is surfaced
    as a value, not an exception, because the caller usually wants
    to render it as a user-facing diagnostic (the migrator's dry-run
    output, an MCP audit response, etc.) rather than crash.
    """
    workspace = workspace_root or find_workspace_root(project_root)

    v2_dirs = _v2_dirs_in(workspace)
    v3_present, v3_complete = _v3_status(workspace)

    notes: list[str] = []

    if v3_present and v2_dirs:
        notes.append(
            f"both _lifecycle/ and v2 dirs {list(v2_dirs)} present under "
            f"{workspace.name}/; this is a half-migrated state — refuse "
            "to operate until the v2 dirs are emptied or removed."
        )
        return TopologyReport(
            topology=Topology.MIXED,
            workspace_root=workspace,
            v2_dirs_present=v2_dirs,
            v3_lifecycle_present=True,
            v3_lifecycle_complete=v3_complete,
            notes=tuple(notes),
        )

    if v3_present:
        if not v3_complete:
            notes.append(
                "_lifecycle/ exists but is missing one or more of the 5 "
                f"stage subdirs ({list(STAGE_NAMES)}); run "
                "`fcop.lifecycle.ensure_lifecycle_dirs` to repair."
            )
        return TopologyReport(
            topology=Topology.V3,
            workspace_root=workspace,
            v3_lifecycle_present=True,
            v3_lifecycle_complete=v3_complete,
            notes=tuple(notes),
        )

    if v2_dirs:
        return TopologyReport(
            topology=Topology.V2,
            workspace_root=workspace,
            v2_dirs_present=v2_dirs,
            notes=tuple(notes),
        )

    notes.append(
        f"neither v2 tasks/log/reports/issues nor v3 _lifecycle/ found "
        f"under {workspace.relative_to(project_root) if workspace.is_relative_to(project_root) else workspace}/; "
        "treating as an empty project."
    )
    return TopologyReport(
        topology=Topology.EMPTY,
        workspace_root=workspace,
        notes=tuple(notes),
    )
