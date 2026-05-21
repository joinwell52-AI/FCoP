"""State layer — the NOW truth (per FCoP 3.0 spec §1).

This module encodes the 5-bucket lifecycle topology and the rule that
**file path is the only source of current state** (Rule A). Nothing in
this module reads file contents; the directory a file lives in *is*
the state.

Public surface (re-exported by :mod:`fcop.lifecycle`):

* :class:`Stage` — the 5 lifecycle stages as an ``Enum``
* :data:`LIFECYCLE_DIRNAME` — the conventional root directory name
  (``"_lifecycle"``) under any FCoP project root
* :func:`stage_dir` — resolve ``<root>/<LIFECYCLE_DIRNAME>/<stage>/``
* :func:`stage_of_path` — inverse: given a path inside a lifecycle root,
  return the :class:`Stage` it currently lives in (Rule A)
* :func:`ensure_lifecycle_dirs` — create the 5 subdirs if missing
* :func:`same_mount` — verify all 5 subdirs share a single mount point
  (per spec §1.1 "all on the same filesystem")

The module deliberately does **no** I/O beyond ``mkdir`` and ``stat``.
File moves and event appends live in
:mod:`fcop.lifecycle.atomic` and :mod:`fcop.lifecycle.events`.
"""

from __future__ import annotations

import os
from enum import Enum
from pathlib import Path

__all__ = [
    "LIFECYCLE_DIRNAME",
    "STAGE_NAMES",
    "Stage",
    "ensure_lifecycle_dirs",
    "lifecycle_root",
    "same_mount",
    "stage_dir",
    "stage_of_path",
]


LIFECYCLE_DIRNAME = "_lifecycle"
"""The conventional name of the lifecycle root inside an FCoP project.

Per spec §1.1, a v3 project's lifecycle root lives at
``<project_root>/<LIFECYCLE_DIRNAME>/``. The five stage subdirectories
``inbox/``, ``active/``, ``review/``, ``done/``, ``archive/`` live
directly beneath it. All five MUST share a single mount point — see
:func:`same_mount`.
"""


class Stage(str, Enum):
    """The 5 lifecycle stages (per spec §1.2).

    The ``str`` mixin lets ``Stage.INBOX == "inbox"`` evaluate true,
    which keeps the API ergonomic when comparing against on-disk
    directory names without forcing every caller to ``.value`` first.

    Definitions are frozen by ADR-0035 and re-stated here verbatim:

    * :attr:`INBOX`   — created
    * :attr:`ACTIVE`  — claimed
    * :attr:`REVIEW`  — pending confirmation
    * :attr:`DONE`    — completed
    * :attr:`ARCHIVE` — closed

    Implementations MUST NOT attach extra semantics to these names.
    """

    INBOX = "inbox"
    ACTIVE = "active"
    REVIEW = "review"
    DONE = "done"
    ARCHIVE = "archive"

    @classmethod
    def from_dirname(cls, name: str) -> Stage:
        """Parse a directory name into a :class:`Stage`.

        Raises:
            ValueError: if ``name`` is not one of the five stage names.
        """
        try:
            return cls(name)
        except ValueError as exc:
            raise ValueError(
                f"{name!r} is not a valid FCoP lifecycle stage; "
                f"expected one of {STAGE_NAMES}"
            ) from exc


STAGE_NAMES: tuple[str, ...] = tuple(s.value for s in Stage)
"""All 5 stage names in canonical (inbox → archive) order."""


def lifecycle_root(project_root: Path) -> Path:
    """Return ``<project_root>/<LIFECYCLE_DIRNAME>/``.

    The path is returned unresolved (no ``.resolve()``) so callers can
    decide whether they want a symlink-following or symlink-preserving
    view. ``project_root`` is taken as-is.
    """
    return project_root / LIFECYCLE_DIRNAME


def stage_dir(project_root: Path, stage: Stage) -> Path:
    """Return ``<project_root>/<LIFECYCLE_DIRNAME>/<stage>/``.

    Pure path arithmetic — does not create the directory; use
    :func:`ensure_lifecycle_dirs` for that.
    """
    return lifecycle_root(project_root) / stage.value


def ensure_lifecycle_dirs(project_root: Path) -> Path:
    """Create the lifecycle root and all 5 stage subdirs if missing.

    Idempotent. Returns the lifecycle root path. The function does
    *not* assert single-mount; call :func:`same_mount` separately
    when you need that guarantee (it is a deployment property, not a
    construction-time one).
    """
    root = lifecycle_root(project_root)
    root.mkdir(parents=True, exist_ok=True)
    for stage in Stage:
        (root / stage.value).mkdir(parents=True, exist_ok=True)
    return root


def stage_of_path(path: Path, *, project_root: Path | None = None) -> Stage | None:
    """Return the :class:`Stage` that ``path`` currently lives in.

    This is the in-code expression of **Rule A: file path is the only
    source of current state**. The function inspects only ``path``;
    it never opens the file or reads its contents.

    Args:
        path: A file path. It does not need to exist on disk — this
            function works purely on the path string.
        project_root: Optional project root for tighter validation.
            When given, the path MUST live under
            ``<project_root>/<LIFECYCLE_DIRNAME>/``; otherwise the
            function returns ``None``. When ``None``, the function
            simply walks up parents and returns the first match.

    Returns:
        The :class:`Stage` matching the enclosing directory name, or
        ``None`` if ``path`` is not inside any recognised lifecycle
        bucket. ``None`` is the canonical "this file is not under
        FCoP state management" answer; callers should treat it as
        non-error.
    """
    if project_root is not None:
        root = lifecycle_root(project_root)
        try:
            rel_parts = path.resolve().relative_to(root.resolve()).parts
        except ValueError:
            return None
        if not rel_parts:
            return None
        candidate = rel_parts[0]
        try:
            return Stage.from_dirname(candidate)
        except ValueError:
            return None

    for parent in path.parents:
        # Walk up. The first directory matching LIFECYCLE_DIRNAME
        # establishes the root; the path component *right under* it
        # is the stage.
        if parent.name == LIFECYCLE_DIRNAME:
            try:
                rel = path.relative_to(parent)
            except ValueError:
                return None
            head = rel.parts[0] if rel.parts else ""
            try:
                return Stage.from_dirname(head)
            except ValueError:
                return None
    return None


def same_mount(project_root: Path) -> bool:
    """Return ``True`` iff all 5 stage subdirs share a single mount.

    Per spec §1.1, atomic transitions rely on POSIX ``rename()`` being
    same-mount. This check is the deployment-time assertion of that
    invariant.

    Implementation: compares ``stat().st_dev`` across all 5 stage
    directories. Returns ``True`` when they are all equal **and** all
    directories exist. Returns ``False`` if any subdir is missing
    (because then the invariant is trivially unverifiable) or if the
    devices disagree.

    On Windows ``st_dev`` is the volume serial; on POSIX it's the
    device number. Both behave correctly for the "same mount" check.
    """
    root = lifecycle_root(project_root)
    devs: set[int] = set()
    for stage in Stage:
        sub = root / stage.value
        try:
            devs.add(os.stat(sub).st_dev)
        except FileNotFoundError:
            return False
    return len(devs) == 1
