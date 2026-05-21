"""Atomic write-then-rename (per FCoP 3.0 spec §2.4).

The physical implementation of "an event *is* the transition,
witnessed in writing". This module performs the only operation that
genuinely matters for an FCoP transition:

1. read source file
2. append the event to ``transitions:`` (in memory)
3. write to a temp file inside the destination directory
4. fsync the temp file
5. ``os.rename(tmp, destination)`` — the POSIX atomic commit point
6. unlink source if its path differs from the destination

Before step 5: state = source location, event not written.
After  step 5: state = destination location, event written.
**There is no observable intermediate state.**

This module is intentionally minimal — it owns one verb (``commit``)
and one observation type (:class:`AtomicCommitResult`). All policy
(which transitions are legal, who can fire them, what the source
file looks like) lives elsewhere. By the time control reaches
:func:`commit`, the caller has already passed
:func:`fcop.lifecycle.transitions.validate_transition`.
"""

from __future__ import annotations

import os
import uuid
from dataclasses import dataclass
from pathlib import Path

from fcop.lifecycle.events import (
    TransitionEvent,
    append_event_to_frontmatter,
)
from fcop.lifecycle.state import Stage, stage_dir, stage_of_path
from fcop.lifecycle.transitions import (
    IllegalTransitionError,
    validate_transition,
)

__all__ = [
    "AtomicCommitResult",
    "CrossDeviceError",
    "commit",
    "create",
]


class CrossDeviceError(OSError):
    """Raised when source and destination live on different mount points.

    The rename + the write-then-rename pattern both require same-mount
    POSIX semantics (spec §1.1, §2.5). Cross-mount transitions break
    atomicity and FCoP refuses to silently degrade.

    The OS itself surfaces this as ``OSError(errno=EXDEV)``; this
    subclass is what we raise after pre-checking, so callers can
    catch the protocol-level intent without scraping errno values.
    """


@dataclass(frozen=True, slots=True)
class AtomicCommitResult:
    """Outcome of a successful :func:`commit` call.

    Attributes:
        source_path: The original path of the file. ``None`` when the
            commit was a creation (``from_stage is None``).
        destination_path: Where the file lives now. Always present.
        event: The :class:`TransitionEvent` that was witnessed and
            written. Returned so audit code can hash / log it without
            re-reading the file.
        used_rename: ``True`` for normal transitions (rename was the
            commit point). ``False`` only for the creation case, where
            there is no source — the destination is fsync'd-and-renamed
            from a temp file inside the same destination directory.
    """

    source_path: Path | None
    destination_path: Path
    event: TransitionEvent
    used_rename: bool = True


def _same_mount(a: Path, b: Path) -> bool:
    """Compare ``st_dev`` of two existing parent directories.

    The check fires on the *parent* of each path because the path
    itself may not yet exist (destination temp file). ``a`` is
    expected to exist; ``b`` is expected to have an existing parent.
    """
    return os.stat(a).st_dev == os.stat(b.parent).st_dev


def _temp_name(stem: str) -> str:
    """Build a ``.fcop-<stem>-<uuid>.tmp`` name to dodge collisions.

    Leading dot keeps the temp out of casual ``ls`` output on POSIX;
    UUID makes concurrent transitions on the same file safe.
    """
    return f".fcop-{stem}-{uuid.uuid4().hex}.tmp"


def commit(
    source_path: Path,
    to_stage: Stage,
    event: TransitionEvent,
    *,
    project_root: Path,
) -> AtomicCommitResult:
    """Atomically move ``source_path`` to ``to_stage`` and witness it.

    The single operation that physically enacts an FCoP 3.0 lifecycle
    transition. By the time control reaches this function:

    * The caller has decided which stage the file should land in.
    * The caller has built a fully-populated :class:`TransitionEvent`
      whose ``to_stage`` and ``tool`` match the intent.
    * :func:`validate_transition` will run here as a final safety
      check — if the event's ``(from, to, tool)`` is not in the
      spec §1.3 table, the function raises and disk is untouched.

    Args:
        source_path: The file as it currently lives on disk. The
            function infers ``from_stage`` from its enclosing
            lifecycle directory (Rule A).
        to_stage: The destination stage. MUST equal ``event.to_stage``.
        event: The witness event. Its ``to_stage`` MUST equal
            ``to_stage``; its ``from_stage`` MUST equal the inferred
            source stage; its ``tool`` MUST be the canonical L1 tool
            for the transition. Any mismatch raises
            :class:`IllegalTransitionError` before any I/O.
        project_root: The FCoP project root. Used to compute the
            destination directory and to verify single-mount.

    Returns:
        :class:`AtomicCommitResult` describing where the file lives now.

    Raises:
        IllegalTransitionError: event/argument inconsistency, or the
            transition is not in the allowed table.
        CrossDeviceError: source and destination are on different
            mount points; atomicity cannot be guaranteed.
        FileNotFoundError: ``source_path`` does not exist.
        OSError: any other underlying filesystem failure.
    """
    if event.to_stage != to_stage:
        raise IllegalTransitionError(
            event.from_stage,
            to_stage,
            tool=event.tool,
        )

    inferred_from = stage_of_path(source_path, project_root=project_root)
    if inferred_from != event.from_stage:
        raise IllegalTransitionError(
            inferred_from,
            to_stage,
            tool=event.tool,
        )

    spec = validate_transition(inferred_from, to_stage, tool=event.tool)
    _ = spec  # validated for side effect; identity is enough

    if not source_path.exists():
        raise FileNotFoundError(str(source_path))

    dst_dir = stage_dir(project_root, to_stage)
    dst_dir.mkdir(parents=True, exist_ok=True)
    destination = dst_dir / source_path.name

    if not _same_mount(source_path, destination):
        raise CrossDeviceError(
            f"source ({source_path}) and destination ({destination}) "
            f"are on different mount points; FCoP 3.0 requires "
            f"_lifecycle/ subdirs to share a single mount (spec §1.1)."
        )

    original_text = source_path.read_text(encoding="utf-8")
    new_text = append_event_to_frontmatter(original_text, event)

    tmp_path = dst_dir / _temp_name(source_path.stem)
    fd = os.open(tmp_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as fh:
            fh.write(new_text)
            fh.flush()
            os.fsync(fh.fileno())
    except BaseException:
        tmp_path.unlink(missing_ok=True)
        raise

    try:
        os.replace(tmp_path, destination)
    except BaseException:
        tmp_path.unlink(missing_ok=True)
        raise

    if source_path.resolve() != destination.resolve():
        source_path.unlink(missing_ok=True)

    return AtomicCommitResult(
        source_path=source_path,
        destination_path=destination,
        event=event,
    )


def create(
    filename: str,
    initial_text: str,
    event: TransitionEvent,
    *,
    project_root: Path,
) -> AtomicCommitResult:
    """Atomically create a brand-new file in ``inbox/`` (or whichever
    stage ``event.to_stage`` names).

    The creation analogue of :func:`commit`. Used when the file does
    not exist on disk yet — the only legal creation target in spec
    §1.3 is ``inbox`` via ``create_task``, but we keep this generic
    in case future MINOR versions add other creation paths.

    Behaviour:

    * Writes the file's full text (frontmatter + body) to a temp file
      inside the destination directory.
    * Appends ``event`` to that text's ``transitions:`` array first.
    * fsync, then ``os.rename`` to the canonical name.

    Args:
        filename: Just the file name (e.g. ``"TASK-20260521-001-PM-to-DEV.md"``);
            must not contain path separators.
        initial_text: Full file contents *before* the creation event is
            appended. Must already include valid frontmatter (spec §2.1).
        event: The creation event. ``event.from_stage`` MUST be ``None``.
        project_root: The FCoP project root.

    Returns:
        :class:`AtomicCommitResult` with ``source_path=None`` and
        ``used_rename=False``.

    Raises:
        IllegalTransitionError: ``event.from_stage`` is not ``None``,
            or the transition is not in the allowed table.
        FileExistsError: a file with ``filename`` already exists in
            the destination directory.
    """
    if "/" in filename or "\\" in filename:
        raise ValueError(f"filename must not contain path separators: {filename!r}")

    if event.from_stage is not None:
        raise IllegalTransitionError(
            event.from_stage,
            event.to_stage,
            tool=event.tool,
        )

    validate_transition(None, event.to_stage, tool=event.tool)

    dst_dir = stage_dir(project_root, event.to_stage)
    dst_dir.mkdir(parents=True, exist_ok=True)
    destination = dst_dir / filename
    if destination.exists():
        raise FileExistsError(str(destination))

    text_with_event = append_event_to_frontmatter(initial_text, event)

    tmp_path = dst_dir / _temp_name(Path(filename).stem)
    fd = os.open(tmp_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as fh:
            fh.write(text_with_event)
            fh.flush()
            os.fsync(fh.fileno())
    except BaseException:
        tmp_path.unlink(missing_ok=True)
        raise

    try:
        os.replace(tmp_path, destination)
    except BaseException:
        tmp_path.unlink(missing_ok=True)
        raise

    return AtomicCommitResult(
        source_path=None,
        destination_path=destination,
        event=event,
        used_rename=False,
    )
