"""The :class:`Project` facade — the main entry point of the fcop library.

A :class:`Project` represents one FCoP-managed directory on disk. It is
the only public class that performs side effects; every method that
creates, modifies, archives, or reads files goes through a ``Project``
instance.

See adr/ADR-0001-library-api.md for the full API contract and invariants.

Implementation status: D3 in progress. Identity / path properties,
``is_initialized``, ``config``, and ``status`` are implemented. Task /
report / issue CRUD, ``init*``, and deployment still raise
:class:`NotImplementedError` — they land in D3-c2 and D4.
"""

from __future__ import annotations

import contextlib
import datetime as _dt
import os
import pathlib
from collections.abc import Sequence
from typing import TYPE_CHECKING, Literal

import yaml

from fcop.core.config import load_team_config, save_team_config
from fcop.core.filename import (
    ISSUE_FILENAME_RE,
    REPORT_FILENAME_RE,
    TASK_FILENAME_RE,
    build_issue_filename,
    build_report_filename,
    build_task_filename,
    next_sequence,
    parse_issue_filename,
    parse_report_filename,
    parse_task_filename,
    today_iso,
)
from fcop.core.frontmatter import (
    FRONTMATTER_DELIMITER,
    assemble_task_file,
    parse_frontmatter_raw,
    parse_task_frontmatter,
    split_frontmatter,
)
from fcop.core.schema import (
    PROTOCOL_NAME,
    PROTOCOL_VERSION,
    is_valid_role_code,
    normalize_priority,
    normalize_severity,
    validate_role_code,
)
from fcop.errors import (
    ProjectAlreadyInitializedError,
    ProtocolViolation,
    TaskNotFoundError,
    ValidationError,
)
from fcop.models import (
    Issue,
    Priority,
    ProjectStatus,
    RecentActivityEntry,
    Report,
    Severity,
    Task,
    TaskFrontmatter,
    TeamConfig,
    ValidationIssue,
)
from fcop.teams import get_team_info

if TYPE_CHECKING:
    from fcop.models import DeploymentReport

__all__ = ["Project"]


class Project:
    """Represents an FCoP-managed project rooted at a filesystem path.

    Constructing a :class:`Project` does **not** touch the filesystem.
    Use :meth:`is_initialized` to check whether the project has been set
    up, and :meth:`init` (or :meth:`init_solo` / :meth:`init_custom`) to
    create the directory structure and configuration.

    Args:
        path: Absolute or relative path to the project root. When the
              project is initialized, this directory will contain
              ``docs/agents/`` with the FCoP layout inside.
        strict: If ``True`` (the default), every operation validates
                against FCoP rules and raises
                :class:`~fcop.errors.ProtocolViolation` on any breach.
                If ``False``, best-effort mode — useful for migration
                tools that need to read malformed legacy files.

    Thread safety:
        A :class:`Project` instance maintains no mutable state other
        than a per-call config cache. Multiple instances for different
        paths are independent and safe to use concurrently. Concurrent
        writers to the *same* path rely on filesystem ``rename()``
        atomicity; the :meth:`write_task` method retries on sequence
        number collisions.
    """

    def __init__(
        self,
        path: str | os.PathLike[str],
        *,
        strict: bool = True,
    ) -> None:
        self._path = pathlib.Path(path).resolve()
        self._strict = strict

    # ── Identity ──────────────────────────────────────────────────────

    @property
    def path(self) -> pathlib.Path:
        """Absolute, resolved path to the project root."""
        return self._path

    @property
    def tasks_dir(self) -> pathlib.Path:
        """``<project>/docs/agents/tasks/``."""
        return self._path / "docs" / "agents" / "tasks"

    @property
    def reports_dir(self) -> pathlib.Path:
        """``<project>/docs/agents/reports/``."""
        return self._path / "docs" / "agents" / "reports"

    @property
    def issues_dir(self) -> pathlib.Path:
        """``<project>/docs/agents/issues/``."""
        return self._path / "docs" / "agents" / "issues"

    @property
    def shared_dir(self) -> pathlib.Path:
        """``<project>/docs/agents/shared/``."""
        return self._path / "docs" / "agents" / "shared"

    @property
    def log_dir(self) -> pathlib.Path:
        """``<project>/docs/agents/log/`` (archive root)."""
        return self._path / "docs" / "agents" / "log"

    @property
    def config_path(self) -> pathlib.Path:
        """``<project>/docs/agents/fcop.json``.

        The presence of this file is the canonical signal that a project
        has been initialized — see :meth:`is_initialized`.
        """
        return self._path / "docs" / "agents" / "fcop.json"

    @property
    def _migrations_dir(self) -> pathlib.Path:
        """``<project>/.fcop/migrations/`` — destination for archived
        conflicts during ``init(force=True)`` and template redeploys.

        Private because the exact ``.fcop/`` layout is an internal
        implementation detail that may change between minor releases.
        """
        return self._path / ".fcop" / "migrations"

    @property
    def _suggestions_dir(self) -> pathlib.Path:
        """``<project>/.fcop/suggestions/`` — inbox for out-of-band
        notes AI roles drop for ADMIN. Private for the same reason
        as :attr:`_migrations_dir`.
        """
        return self._path / ".fcop" / "suggestions"

    # ── Lifecycle ─────────────────────────────────────────────────────

    def is_initialized(self) -> bool:
        """``True`` if ``docs/agents/fcop.json`` exists under the root.

        This is a pure filesystem probe — it does not validate the
        contents of ``fcop.json``. Use :attr:`config` to actually parse
        the configuration (which will raise :class:`ConfigError` if the
        file is present but malformed).
        """
        return self.config_path.is_file()

    def init(
        self,
        *,
        team: str = "dev-team",
        lang: str = "zh",
        force: bool = False,
    ) -> ProjectStatus:
        """Initialize this directory as an FCoP project with a preset team.

        Creates the ``docs/agents/{tasks,reports,issues,shared,log}/``
        tree and writes ``fcop.json``. Role template deployment,
        Cursor rule installation, and the welcome task are handled by
        separate methods (:meth:`deploy_role_templates` + future work)
        so ``init`` stays focused on the one invariant that
        :meth:`is_initialized` probes for.

        Args:
            team: Name of a bundled preset team. See
                  :func:`fcop.teams.get_available_teams` for the list.
            lang: ``"zh"`` or ``"en"`` — informational only at this
                  point; influences nothing that ``init`` writes
                  today, but is persisted into ``fcop.json`` so later
                  template deployment picks it up.
            force: If ``True``, allow overwriting an existing
                   ``fcop.json``; the old file is archived to
                   ``.fcop/migrations/<timestamp>/`` before the new
                   one lands. Destructive — defaults to ``False``.

        Returns:
            A :class:`ProjectStatus` snapshot of the freshly initialized
            project.

        Raises:
            ProjectAlreadyInitializedError: ``fcop.json`` exists and
                ``force=False``.
            TeamNotFoundError: ``team`` is not in the bundled registry.
        """
        info = get_team_info(team)
        cfg = TeamConfig(
            mode="preset",
            team=info.name,
            leader=info.leader,
            roles=info.roles,
            lang=lang,
            version=PROTOCOL_VERSION,
            extra={
                "display_name": info.display_name,
                "created_at": _now_iso(),
            },
        )
        self._apply_init(cfg, force=force)
        return self.status()

    def init_solo(
        self,
        *,
        role_code: str = "ME",
        lang: str = "zh",
        force: bool = False,
    ) -> ProjectStatus:
        """Initialize in Solo mode (single role interfacing with ADMIN).

        Solo mode is for individual users who want FCoP's file
        discipline without a multi-agent team. Exactly one role is
        registered (default ``"ME"``); it doubles as the leader.

        Args:
            role_code: The one role that writes in this project.
                Must match the role grammar (uppercase, ASCII,
                optionally hyphenated). ``ADMIN`` / ``SYSTEM`` are
                rejected because solo mode is about AI authorship —
                ADMIN is already implied as the human counterpart.
            lang: Persisted into ``fcop.json`` for later template
                deployment; ignored by ``init_solo`` itself.
            force: Same semantics as :meth:`init`.

        Raises:
            ValidationError: ``role_code`` fails
                :func:`fcop.core.schema.validate_role_code`
                (strict — reserved roles rejected).
            ProjectAlreadyInitializedError: see :meth:`init`.
        """
        issues = validate_role_code(role_code, field="role_code")
        errors = [i for i in issues if i.severity == "error"]
        if errors:
            raise ValidationError(
                f"invalid role_code {role_code!r} for solo mode",
                issues=errors,
            )

        cfg = TeamConfig(
            mode="solo",
            team="solo",
            leader=role_code,
            roles=(role_code,),
            lang=lang,
            version=PROTOCOL_VERSION,
            extra={"created_at": _now_iso()},
        )
        self._apply_init(cfg, force=force)
        return self.status()

    def init_custom(
        self,
        *,
        team_name: str,
        roles: Sequence[str],
        leader: str,
        lang: str = "zh",
        force: bool = False,
    ) -> ProjectStatus:
        """Initialize with a user-defined role set.

        Equivalent to the legacy ``create_custom_team()`` tool. Call
        :meth:`validate_team` first to surface any naming or
        structural issues without writing files — the checks here are
        identical, they just raise :class:`ValidationError` on failure
        instead of returning a list.

        Args:
            team_name: Human-readable team slug written into
                ``fcop.json`` (``"my-custom-squad"``). Free-form
                string; only non-emptiness is enforced.
            roles: Ordered sequence of role codes registered on this
                team. Must include ``leader``.
            leader: Role code of the team's leader — the one recipient
                ``ADMIN``-addressed tasks default to.
            lang: Persisted for later template deployment.
            force: Same semantics as :meth:`init`.

        Raises:
            ValidationError: the team config is invalid. The raised
                exception's ``.issues`` list mirrors what
                :meth:`validate_team` returns.
        """
        issues = Project.validate_team(roles=roles, leader=leader)
        errors = [i for i in issues if i.severity == "error"]
        if errors:
            raise ValidationError(
                "invalid custom team config",
                issues=errors,
            )
        if not team_name.strip():
            raise ValidationError(
                "team_name must not be empty",
                issues=[
                    ValidationIssue(
                        severity="error",
                        field="team_name",
                        message="team_name must be a non-empty string",
                    )
                ],
            )

        cfg = TeamConfig(
            mode="custom",
            team=team_name,
            leader=leader,
            roles=tuple(roles),
            lang=lang,
            version=PROTOCOL_VERSION,
            extra={"created_at": _now_iso()},
        )
        self._apply_init(cfg, force=force)
        return self.status()

    @staticmethod
    def validate_team(
        *,
        roles: Sequence[str],
        leader: str,
    ) -> list[ValidationIssue]:
        """Dry-run validation of a custom team config.

        Does not touch the filesystem. Checks:

        * ``roles`` is non-empty.
        * Each role code matches
          :data:`fcop.core.schema.ROLE_CODE_RE` and is not reserved
          (``ADMIN`` / ``SYSTEM`` cannot be assigned to AI roles).
        * Authority words like ``BOSS`` produce a stylistic
          ``warning`` issue (non-fatal — callers can elect to proceed).
        * ``roles`` has no duplicates.
        * ``leader`` appears in ``roles``.

        Returns:
            A list of :class:`ValidationIssue` — empty when the config
            is clean. Callers render the list to the user; callers
            that prefer exceptions can filter to ``severity=="error"``
            and raise themselves.
        """
        issues: list[ValidationIssue] = []

        if not roles:
            issues.append(
                ValidationIssue(
                    severity="error",
                    field="roles",
                    message="roles must be a non-empty sequence",
                )
            )
            return issues

        seen: set[str] = set()
        for i, code in enumerate(roles):
            field = f"roles[{i}]"
            issues.extend(validate_role_code(code, field=field))
            if code in seen:
                issues.append(
                    ValidationIssue(
                        severity="error",
                        field=field,
                        message=f"duplicate role code {code!r}",
                    )
                )
            else:
                seen.add(code)

        if not is_valid_role_code(leader):
            issues.append(
                ValidationIssue(
                    severity="error",
                    field="leader",
                    message=(
                        f"leader {leader!r} is not a valid role code "
                        "(must be uppercase ASCII, optionally hyphenated)"
                    ),
                )
            )
        elif leader not in seen:
            issues.append(
                ValidationIssue(
                    severity="error",
                    field="leader",
                    message=(
                        f"leader {leader!r} must appear in the roles list"
                    ),
                )
            )

        return issues

    def _apply_init(self, cfg: TeamConfig, *, force: bool) -> None:
        """Shared I/O for ``init`` / ``init_solo`` / ``init_custom``.

        Order of operations:

        1. Check for pre-existing ``fcop.json``. If present and
           ``force=False``, refuse.
        2. Create the canonical directory tree even in the force path;
           this is idempotent (``mkdir(parents=True, exist_ok=True)``).
        3. If forcing, archive the old ``fcop.json`` into
           ``.fcop/migrations/<timestamp>/`` *before* the atomic swap —
           losing the old config silently would be a data hazard.
        4. Atomic write of the new config (``save_team_config``
           uses tmp-then-replace internally).

        Private because the exact sequencing is an implementation
        detail; callers use the high-level ``init*`` methods.
        """
        config_path = self.config_path
        already = config_path.is_file()
        if already and not force:
            raise ProjectAlreadyInitializedError(
                f"fcop.json already exists at {config_path}; "
                "pass force=True to overwrite (the old file will be "
                "archived under .fcop/migrations/)."
            )

        for directory in (
            self.tasks_dir,
            self.reports_dir,
            self.issues_dir,
            self.shared_dir,
            self.log_dir,
        ):
            directory.mkdir(parents=True, exist_ok=True)

        if already and force:
            timestamp = _now_iso().replace(":", "").replace("-", "")
            migration_dir = self._migrations_dir / timestamp
            migration_dir.mkdir(parents=True, exist_ok=True)
            archive_path = migration_dir / "fcop.json"
            config_path.replace(archive_path)

        save_team_config(cfg, config_path)

    # ── Config ────────────────────────────────────────────────────────

    @property
    def config(self) -> TeamConfig:
        """Read-only snapshot of ``docs/agents/fcop.json``.

        Re-read from disk on each access so external mutations are
        visible. This property has no caching guarantees; if you need
        to repeatedly inspect the config, capture it into a local.

        Raises:
            ConfigError: ``fcop.json`` is missing, unreadable, not valid
                JSON, or fails structural validation. The raised error's
                ``.path`` attribute points at ``config_path``.
        """
        return load_team_config(self.config_path)

    # ── Status ────────────────────────────────────────────────────────

    def status(self) -> ProjectStatus:
        """Return counts and recent activity for this project.

        Safe to call on an uninitialized project: in that case every
        count is ``0``, ``config`` is ``None``, and ``recent_activity``
        is empty. Never raises for a missing directory — only for
        invalid ``fcop.json`` contents (via :attr:`config`).
        """
        initialized = self.is_initialized()
        cfg: TeamConfig | None = self.config if initialized else None

        tasks_open = _count_matching(self.tasks_dir, TASK_FILENAME_RE)
        reports_count = _count_matching(self.reports_dir, REPORT_FILENAME_RE)
        issues_count = _count_matching(self.issues_dir, ISSUE_FILENAME_RE)
        tasks_archived = _count_matching(
            self.log_dir / "tasks", TASK_FILENAME_RE
        )

        recent = _collect_recent_activity(
            tasks_dir=self.tasks_dir,
            reports_dir=self.reports_dir,
            issues_dir=self.issues_dir,
            limit=_RECENT_ACTIVITY_LIMIT,
        )

        return ProjectStatus(
            path=self._path,
            is_initialized=initialized,
            config=cfg,
            tasks_open=tasks_open,
            tasks_archived=tasks_archived,
            reports_count=reports_count,
            issues_count=issues_count,
            recent_activity=recent,
        )

    # ── Tasks ─────────────────────────────────────────────────────────

    def write_task(
        self,
        *,
        sender: str,
        recipient: str,
        priority: Priority | str,
        subject: str,
        body: str,
        references: Sequence[str] = (),
        thread_key: str | None = None,
        slot: str | None = None,
    ) -> Task:
        """Create a new task file.

        Filename is auto-generated as
        ``TASK-YYYYMMDD-NNN-{sender}-to-{recipient}.md``. ``NNN`` is
        today's existing task count + 1. On concurrent-write
        collisions the sequence is retried up to :data:`_MAX_WRITE_RETRIES`
        times before giving up with a :class:`RuntimeError`.

        Args:
            sender: Role code of the sending agent (uppercase, ASCII,
                hyphen-friendly). ``ADMIN`` and ``SYSTEM`` are accepted.
            recipient: Role code of the receiving agent.
            priority: Either a :class:`Priority` enum or a string alias
                accepted by :func:`normalize_priority` (``"P0".."P3"``
                or legacy words like ``"urgent"`` / ``"normal"``).
            subject: Short one-line summary written into the ``subject:``
                frontmatter field. Required by the 0.6 grammar.
            body: Markdown body of the task; any leading blank lines
                are normalized away so the output stays idempotent.
            references: Zero or more task/report IDs this task depends
                on. Written as ``references: [...]`` in the frontmatter.
            thread_key: Optional thread grouping key — ties a sequence
                of back-and-forth tasks together.
            slot: Optional recipient qualifier (``.BACKEND`` → recipient
                becomes ``DEV.BACKEND`` in the filename). Role grammar
                applies to the slot too.

        Raises:
            ValueError: filename components don't match the grammar
                (e.g. sender contains lowercase letters), or ``priority``
                is an unrecognized alias.
            OverflowError: today's 999-sequence space is exhausted.
            RuntimeError: failed to reserve a sequence after
                :data:`_MAX_WRITE_RETRIES` collisions with concurrent
                writers. Practical only under pathological races.
        """
        tasks_dir = self.tasks_dir
        tasks_dir.mkdir(parents=True, exist_ok=True)

        priority_enum = normalize_priority(priority)
        date = today_iso()

        fm = TaskFrontmatter(
            protocol=PROTOCOL_NAME,
            version=PROTOCOL_VERSION,
            sender=sender,
            recipient=recipient,
            priority=priority_enum,
            thread_key=thread_key,
            subject=subject or None,
            references=tuple(references),
        )
        text = assemble_task_file(fm, body)
        payload = text.encode("utf-8")

        for _ in range(_MAX_WRITE_RETRIES):
            existing = (
                entry.name for entry in tasks_dir.iterdir() if entry.is_file()
            )
            sequence = next_sequence(existing, date=date, kind="task")
            filename = build_task_filename(
                date=date,
                sequence=sequence,
                sender=sender,
                recipient=recipient,
                slot=slot,
            )
            target = tasks_dir / filename

            try:
                # O_EXCL makes the reservation atomic: if a concurrent
                # writer won the same sequence we fail here and retry.
                fd = os.open(
                    os.fspath(target),
                    os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                )
            except FileExistsError:
                continue

            try:
                with os.fdopen(fd, "wb") as handle:
                    handle.write(payload)
            except BaseException:
                # Writer crashed after reserving — clean up the empty
                # placeholder so we don't poison the sequence slot.
                with contextlib.suppress(OSError):
                    target.unlink()
                raise

            parsed = parse_task_filename(filename)
            assert parsed is not None, (
                f"built filename {filename!r} failed to round-trip through "
                "parse_task_filename — this is a bug in core.filename."
            )
            mtime = _dt.datetime.fromtimestamp(target.stat().st_mtime)
            return Task(
                path=target,
                filename=filename,
                task_id=parsed.task_id,
                date=parsed.date,
                sequence=parsed.sequence,
                frontmatter=fm,
                body=body,
                is_archived=False,
                mtime=mtime,
            )

        raise RuntimeError(
            f"failed to reserve a task sequence after {_MAX_WRITE_RETRIES} "
            "retries — concurrent writers are colliding faster than we can "
            "pick an unused slot"
        )

    def list_tasks(
        self,
        *,
        sender: str | None = None,
        recipient: str | None = None,
        status: Literal["open", "archived", "all"] = "open",
        date: str | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> list[Task]:
        """List tasks, optionally filtered by sender / recipient / date.

        Args:
            sender: Exact-match role code filter. ``None`` means any.
            recipient: Exact-match role code filter. ``None`` means any.
            status: ``"open"`` scans :attr:`tasks_dir`, ``"archived"``
                scans ``log/tasks/``, ``"all"`` scans both.
            date: ``YYYYMMDD`` filter. ``None`` means any date.
            limit: Max results; ``None`` means unlimited.
            offset: Skip this many results from the front (applied
                after sorting). Combine with ``limit`` for pagination.

        Returns:
            Tasks sorted by ``(date, sequence)`` descending — newest
            first. Unreadable files (malformed frontmatter, corrupt
            YAML) are silently skipped; use :meth:`inspect_task` if
            you need to surface their problems.
        """
        directories: list[tuple[pathlib.Path, bool]] = []
        if status in ("open", "all"):
            directories.append((self.tasks_dir, False))
        if status in ("archived", "all"):
            directories.append((self.log_dir / "tasks", True))

        tasks: list[Task] = []
        for directory, archived in directories:
            if not directory.is_dir():
                continue
            for entry in directory.iterdir():
                task = _try_load_task(entry, is_archived=archived)
                if task is None:
                    continue
                if date is not None and task.date != date:
                    continue
                if sender is not None and task.sender != sender:
                    continue
                if recipient is not None and task.recipient != recipient:
                    continue
                tasks.append(task)

        tasks.sort(key=lambda t: (t.date, t.sequence), reverse=True)

        end = None if limit is None else offset + max(0, limit)
        return tasks[offset:end]

    def read_task(self, filename_or_id: str) -> Task:
        """Load one task by full filename or by task id (``TASK-YYYYMMDD-NNN``).

        Args:
            filename_or_id: Either a full filename (``TASK-...md``) or a
                task id prefix (``TASK-20260423-001``). Ids are resolved
                by scanning :attr:`tasks_dir` first, then ``log/tasks/``
                so open tasks win over archived ones.

        Raises:
            TaskNotFoundError: nothing matches.
            ValidationError | ProtocolViolation: file exists but its
                frontmatter is malformed. Use :meth:`inspect_task` for a
                non-raising variant.
        """
        target, archived = self._resolve_task_file(filename_or_id)
        if target is None:
            raise TaskNotFoundError(
                f"no task matches {filename_or_id!r}",
                query=filename_or_id,
            )
        return _load_task_strict(target, is_archived=archived)

    def _resolve_task_file(
        self, filename_or_id: str
    ) -> tuple[pathlib.Path | None, bool]:
        """Resolve a user-supplied task handle to an on-disk path.

        Accepts three shapes:

        * A full filename matching :data:`TASK_FILENAME_RE`
          (``TASK-20260423-001-ADMIN-to-PM.md``). Direct lookup.
        * A task id (``TASK-20260423-001``). Scan both dirs for the
          first file whose filename starts with that id.
        * Anything else — returns ``(None, False)``.

        The open :attr:`tasks_dir` is scanned before ``log/tasks/`` so
        a live task takes precedence over a same-id archived one; that
        matches how ADMIN thinks about it ("the task I'm working on").

        Returns:
            ``(path, is_archived)``. ``path`` is ``None`` when no
            match is found; ``is_archived`` is meaningless in that case.
        """
        if TASK_FILENAME_RE.fullmatch(filename_or_id):
            for directory, archived in (
                (self.tasks_dir, False),
                (self.log_dir / "tasks", True),
            ):
                candidate = directory / filename_or_id
                if candidate.is_file():
                    return candidate, archived
            return None, False

        prefix = filename_or_id
        for directory, archived in (
            (self.tasks_dir, False),
            (self.log_dir / "tasks", True),
        ):
            if not directory.is_dir():
                continue
            for entry in directory.iterdir():
                if not entry.is_file():
                    continue
                parsed = parse_task_filename(entry.name)
                if parsed is None:
                    continue
                if parsed.task_id == prefix or entry.name.startswith(
                    prefix + "-"
                ):
                    return entry, archived
        return None, False

    def archive_task(self, filename_or_id: str) -> Task:
        """Move a task (and any matching report) to ``log/``.

        Archiving is the manual "this conversation is closed" marker.
        The file is physically relocated from ``docs/agents/tasks/`` to
        ``docs/agents/log/tasks/``; any report whose filename starts
        with the same ``TASK-...-NNN`` identifier is also moved to
        ``docs/agents/log/reports/`` so the full thread lives together.

        Idempotent — archiving an already-archived task returns the
        same :class:`Task` without touching the filesystem. That makes
        the method safe to call from cleanup scripts without
        pre-checking.

        Args:
            filename_or_id: Full filename or task id, same shapes
                accepted by :meth:`read_task`.

        Returns:
            The archived :class:`Task` with ``is_archived == True`` and
            an updated ``path``.

        Raises:
            TaskNotFoundError: no matching file in either the open or
                archived directories.
            ValidationError | ProtocolViolation: file exists but its
                frontmatter is malformed; archiving a corrupt file
                would hide the problem, so we surface it up-front.
        """
        source, archived = self._resolve_task_file(filename_or_id)
        if source is None:
            raise TaskNotFoundError(
                f"cannot archive: no task matches {filename_or_id!r}",
                query=filename_or_id,
            )

        if archived:
            return _load_task_strict(source, is_archived=True)

        log_tasks_dir = self.log_dir / "tasks"
        log_tasks_dir.mkdir(parents=True, exist_ok=True)
        destination = log_tasks_dir / source.name
        # os.replace is atomic on same-filesystem moves, which is the
        # only case we can reach here — tasks_dir and log_dir are both
        # under self._path.
        source.replace(destination)

        # Move matching reports alongside. A report is "matching" when
        # its filename starts with the task id that precedes the
        # sender/recipient segment of the task filename.
        parsed = parse_task_filename(source.name)
        if parsed is not None:
            self._archive_related_reports(task_id=parsed.task_id)

        return _load_task_strict(destination, is_archived=True)

    def _archive_related_reports(self, *, task_id: str) -> None:
        """Move every report whose filename embeds *task_id* to the log.

        Report filenames don't include the task id as a prefix — they
        carry their own ``REPORT-YYYYMMDD-NNN-`` slug — so matching is
        done on the ``references`` frontmatter field instead. We load
        each report, check whether it cites *task_id*, and move the
        ones that do.

        Silent if there's nothing to move; reports are optional.
        """
        open_reports = self.reports_dir
        if not open_reports.is_dir():
            return
        log_reports = self.log_dir / "reports"

        for entry in open_reports.iterdir():
            if not entry.is_file():
                continue
            if entry.suffix.lower() not in _FCOP_SUFFIXES:
                continue
            if not REPORT_FILENAME_RE.match(entry.name):
                continue

            try:
                text = entry.read_text(encoding="utf-8")
            except OSError:
                continue
            # Reports share the YAML-frontmatter shape with tasks, so
            # we reuse the task parser to read references / extras.
            # A malformed report here just gets skipped; surfacing its
            # breakage is inspect_report's job, not archive_task's.
            try:
                fm, _ = parse_task_frontmatter(text)
            except Exception:
                continue

            references = fm.references
            if task_id not in references:
                continue

            log_reports.mkdir(parents=True, exist_ok=True)
            entry.replace(log_reports / entry.name)

    def inspect_task(self, filename_or_id: str) -> list[ValidationIssue]:
        """Validate a task file against the FCoP schema.

        Unlike :meth:`read_task`, this method never raises on parser
        errors — every problem is converted into a
        :class:`ValidationIssue` and returned in the list. An empty
        list means the file is schema-valid.

        Useful for UIs that want to display warnings and errors side-
        by-side, or for migration tooling that needs to tolerate a
        batch of broken files.

        Args:
            filename_or_id: Same resolution rules as :meth:`read_task`.
                If nothing matches, a single ``"error"`` issue is
                returned with ``field == "filename"`` — we do not
                raise :class:`TaskNotFoundError` here because that
                would defeat the "non-raising" contract.

        Returns:
            Possibly empty list of issues, ordered: filesystem / I/O
            issues first, then frontmatter issues.
        """
        source, _ = self._resolve_task_file(filename_or_id)
        if source is None:
            return [
                ValidationIssue(
                    severity="error",
                    field="filename",
                    message=f"no task matches {filename_or_id!r}",
                )
            ]

        issues: list[ValidationIssue] = []
        try:
            text = source.read_text(encoding="utf-8")
        except OSError as exc:
            issues.append(
                ValidationIssue(
                    severity="error",
                    field="filename",
                    message=f"cannot read {source.name}: {exc}",
                    path=source,
                )
            )
            return issues

        try:
            parse_task_frontmatter(text)
        except ValidationError as exc:
            # ValidationError carries a .issues list already — annotate
            # each with the file path so agents can jump to it.
            issues.extend(
                ValidationIssue(
                    severity=i.severity,
                    field=i.field,
                    message=i.message,
                    path=source,
                )
                for i in exc.issues
            )
        except Exception as exc:
            # ProtocolViolation and unexpected YAML errors both land
            # here; flatten to a single issue so callers get something
            # actionable. We deliberately catch broad to honor the
            # "never raises" docstring contract.
            issues.append(
                ValidationIssue(
                    severity="error",
                    field="frontmatter",
                    message=str(exc),
                    path=source,
                )
            )

        return issues

    # ── Reports ───────────────────────────────────────────────────────

    def write_report(
        self,
        *,
        task_id: str,
        reporter: str,
        recipient: str,
        body: str,
        status: Literal["done", "blocked", "in_progress"] = "done",
        priority: Priority | str = "P2",
    ) -> Report:
        """Create a report responding to an existing task.

        Reports live in ``docs/agents/reports/`` and cite their parent
        task via the ``references:`` frontmatter field. A custom
        top-level ``status:`` field captures the report outcome
        (``done`` / ``blocked`` / ``in_progress``).

        Args:
            task_id: Id of the task this report answers. The task must
                exist — open or archived — and its recipient must match
                ``reporter`` (Rule 5: only the addressee can report).
            reporter: Role code of the reporting agent.
            recipient: Role code receiving the report. Typically the
                original task's sender, so the thread loops back.
            body: Markdown body of the report.
            status: ``done`` / ``blocked`` / ``in_progress``. Written
                as a top-level YAML field and echoed in
                :attr:`Report.status`.
            priority: Report priority, same normalization rules as
                :meth:`write_task`. Defaults to ``P2``.

        Raises:
            TaskNotFoundError: ``task_id`` has no matching task file.
            ProtocolViolation: ``reporter`` is not the original task's
                recipient (Rule 5), or ``status`` is not a valid
                report status.
            ValueError: ``priority`` is an unrecognized alias.
        """
        if status not in _VALID_REPORT_STATUSES:
            raise ProtocolViolation(
                f"status must be one of {sorted(_VALID_REPORT_STATUSES)}; "
                f"got {status!r}",
                rule="report.status",
            )

        task_path, task_archived = self._resolve_task_file(task_id)
        if task_path is None:
            raise TaskNotFoundError(
                f"cannot write report: no task matches {task_id!r}",
                query=task_id,
            )
        # Strict load — we need the frontmatter to enforce Rule 5.
        task = _load_task_strict(task_path, is_archived=task_archived)
        if task.recipient != reporter:
            raise ProtocolViolation(
                f"reporter {reporter!r} is not the recipient of task "
                f"{task_id!r} (its recipient is {task.recipient!r}); "
                "only the task's addressee may report on it",
                rule="Rule 5",
            )

        reports_dir = self.reports_dir
        reports_dir.mkdir(parents=True, exist_ok=True)

        priority_enum = normalize_priority(priority)
        date = today_iso()

        fm = TaskFrontmatter(
            protocol=PROTOCOL_NAME,
            version=PROTOCOL_VERSION,
            sender=reporter,
            recipient=recipient,
            priority=priority_enum,
            references=(task.task_id,),
            extra={"status": status},
        )
        text = assemble_task_file(fm, body)
        payload = text.encode("utf-8")

        for _ in range(_MAX_WRITE_RETRIES):
            existing = (
                entry.name
                for entry in reports_dir.iterdir()
                if entry.is_file()
            )
            sequence = next_sequence(existing, date=date, kind="report")
            filename = build_report_filename(
                date=date,
                sequence=sequence,
                reporter=reporter,
                recipient=recipient,
            )
            target = reports_dir / filename

            try:
                fd = os.open(
                    os.fspath(target),
                    os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                )
            except FileExistsError:
                continue

            try:
                with os.fdopen(fd, "wb") as handle:
                    handle.write(payload)
            except BaseException:
                with contextlib.suppress(OSError):
                    target.unlink()
                raise

            mtime = _dt.datetime.fromtimestamp(target.stat().st_mtime)
            return Report(
                path=target,
                filename=filename,
                task_id=task.task_id,
                reporter=reporter,
                recipient=recipient,
                status=status,
                body=body,
                is_archived=False,
                mtime=mtime,
            )

        raise RuntimeError(
            f"failed to reserve a report sequence after "
            f"{_MAX_WRITE_RETRIES} retries"
        )

    def list_reports(
        self,
        *,
        reporter: str | None = None,
        task_id: str | None = None,
        status: Literal["open", "archived", "all"] = "open",
        limit: int | None = None,
        offset: int = 0,
    ) -> list[Report]:
        """List reports, optionally filtered by reporter or parent task.

        Args:
            reporter: Exact-match filter on the report's sender.
            task_id: If provided, only reports that cite this task in
                their ``references:`` list are returned.
            status: ``"open"`` (default, scans ``reports_dir``),
                ``"archived"`` (scans ``log/reports/``), or ``"all"``.
            limit / offset: Pagination window, applied after sorting.

        Returns:
            Reports sorted by filename (which embeds date + sequence)
            descending — newest first. Malformed files are silently
            skipped, matching :meth:`list_tasks`'s contract.
        """
        directories: list[tuple[pathlib.Path, bool]] = []
        if status in ("open", "all"):
            directories.append((self.reports_dir, False))
        if status in ("archived", "all"):
            directories.append((self.log_dir / "reports", True))

        reports: list[Report] = []
        for directory, archived in directories:
            if not directory.is_dir():
                continue
            for entry in directory.iterdir():
                report = _try_load_report(entry, is_archived=archived)
                if report is None:
                    continue
                if reporter is not None and report.reporter != reporter:
                    continue
                if task_id is not None and report.task_id != task_id:
                    continue
                reports.append(report)

        # Date+sequence ordering matches list_tasks; parse once for
        # the sort key so we don't re-parse filenames per comparison.
        def _sort_key(r: Report) -> tuple[str, int]:
            parsed = parse_report_filename(r.filename)
            if parsed is None:  # defense in depth; shouldn't happen
                return ("", 0)
            return (parsed.date, parsed.sequence)

        reports.sort(key=_sort_key, reverse=True)

        end = None if limit is None else offset + max(0, limit)
        return reports[offset:end]

    def read_report(self, filename_or_id: str) -> Report:
        """Load one report by filename or report id (``REPORT-YYYYMMDD-NNN``).

        Resolution is parallel to :meth:`read_task`: full filename or
        id prefix, open directory first then archive.

        Raises:
            TaskNotFoundError: no match. (We reuse this error type
                because there isn't a dedicated ``ReportNotFoundError``
                in the 0.6 exception hierarchy — the search space and
                user intent are analogous.)
            ValidationError | ProtocolViolation: file exists but is
                malformed. Use inspect for a non-raising variant.
        """
        target, archived = self._resolve_report_file(filename_or_id)
        if target is None:
            raise TaskNotFoundError(
                f"no report matches {filename_or_id!r}",
                query=filename_or_id,
            )
        return _load_report_strict(target, is_archived=archived)

    def _resolve_report_file(
        self, filename_or_id: str
    ) -> tuple[pathlib.Path | None, bool]:
        """Resolve a user handle to a report path, parallel to
        :meth:`_resolve_task_file`.

        Accepts a full filename, or a ``REPORT-YYYYMMDD-NNN`` id prefix.
        Live reports in ``reports_dir`` take precedence over archived
        duplicates with the same id.
        """
        if REPORT_FILENAME_RE.fullmatch(filename_or_id):
            for directory, archived in (
                (self.reports_dir, False),
                (self.log_dir / "reports", True),
            ):
                candidate = directory / filename_or_id
                if candidate.is_file():
                    return candidate, archived
            return None, False

        prefix = filename_or_id
        for directory, archived in (
            (self.reports_dir, False),
            (self.log_dir / "reports", True),
        ):
            if not directory.is_dir():
                continue
            for entry in directory.iterdir():
                if not entry.is_file():
                    continue
                parsed = parse_report_filename(entry.name)
                if parsed is None:
                    continue
                if parsed.report_id == prefix or entry.name.startswith(
                    prefix + "-"
                ):
                    return entry, archived
        return None, False

    # ── Issues ────────────────────────────────────────────────────────

    def write_issue(
        self,
        *,
        reporter: str,
        summary: str,
        body: str,
        severity: Severity | str = "medium",
    ) -> Issue:
        """Create an issue broadcast.

        Issues don't follow the sender → recipient pattern; any
        registered role can write one, and they are addressed to
        *whoever can fix them*. The filename therefore carries only
        the reporter; frontmatter carries ``summary`` and
        ``severity`` as top-level fields.

        Args:
            reporter: Role code of the agent raising the issue. Must
                pass :func:`validate_role_code` (reserved codes like
                ``ADMIN`` / ``SYSTEM`` are permitted — a human or the
                protocol itself can raise an issue).
            summary: Short one-line description. Becomes the ``summary:``
                frontmatter field; must be non-empty after stripping.
            body: Markdown body describing the issue in detail.
            severity: ``low`` / ``medium`` / ``high`` / ``critical``
                (plus the aliases :func:`normalize_severity` accepts).
                Defaults to ``medium``.

        Raises:
            ValidationError: ``reporter`` fails role-code grammar.
            ValueError: ``summary`` is empty or ``severity`` is not a
                recognized value.
        """
        cleaned_summary = summary.strip()
        if not cleaned_summary:
            raise ValueError(
                "issue summary must be non-empty after stripping whitespace"
            )

        role_issues = validate_role_code(
            reporter, field="reporter", allow_reserved=True
        )
        role_errors = [i for i in role_issues if i.severity == "error"]
        if role_errors:
            raise ValidationError(
                f"invalid reporter role code {reporter!r}",
                issues=role_errors,
            )

        severity_enum = normalize_severity(severity)

        issues_dir = self.issues_dir
        issues_dir.mkdir(parents=True, exist_ok=True)

        date = today_iso()
        frontmatter_data: dict[str, object] = {
            "protocol": PROTOCOL_NAME,
            "version": PROTOCOL_VERSION,
            "reporter": reporter,
            "severity": severity_enum.value,
            "summary": cleaned_summary,
        }
        text = _assemble_issue_file(frontmatter_data, body)
        payload = text.encode("utf-8")

        for _ in range(_MAX_WRITE_RETRIES):
            existing = (
                entry.name
                for entry in issues_dir.iterdir()
                if entry.is_file()
            )
            sequence = next_sequence(existing, date=date, kind="issue")
            filename = build_issue_filename(
                date=date, sequence=sequence, reporter=reporter
            )
            target = issues_dir / filename

            try:
                fd = os.open(
                    os.fspath(target),
                    os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                )
            except FileExistsError:
                continue

            try:
                with os.fdopen(fd, "wb") as handle:
                    handle.write(payload)
            except BaseException:
                with contextlib.suppress(OSError):
                    target.unlink()
                raise

            mtime = _dt.datetime.fromtimestamp(target.stat().st_mtime)
            return Issue(
                path=target,
                filename=filename,
                issue_id=f"ISSUE-{date}-{sequence:03d}",
                summary=cleaned_summary,
                severity=severity_enum,
                reporter=reporter,
                body=body,
                mtime=mtime,
            )

        raise RuntimeError(
            f"failed to reserve an issue sequence after "
            f"{_MAX_WRITE_RETRIES} retries"
        )

    def list_issues(
        self,
        *,
        reporter: str | None = None,
        severity: Severity | str | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> list[Issue]:
        """List issues, optionally filtered.

        Args:
            reporter: Exact-match filter on the issue's ``reporter``.
            severity: Exact-match filter; string aliases are normalized
                via :func:`normalize_severity`.
            limit / offset: Pagination window, applied after sorting.

        Returns:
            Issues sorted by date + sequence descending (newest first).
            Malformed files are silently skipped — matches the
            :meth:`list_tasks` / :meth:`list_reports` contract.
        """
        severity_enum: Severity | None = None
        if severity is not None:
            severity_enum = normalize_severity(severity)

        issues: list[Issue] = []
        directory = self.issues_dir
        if directory.is_dir():
            for entry in directory.iterdir():
                issue = _try_load_issue(entry)
                if issue is None:
                    continue
                if reporter is not None and issue.reporter != reporter:
                    continue
                if (
                    severity_enum is not None
                    and issue.severity is not severity_enum
                ):
                    continue
                issues.append(issue)

        def _sort_key(i: Issue) -> tuple[str, int]:
            parsed = parse_issue_filename(i.filename)
            if parsed is None:
                return ("", 0)
            return (parsed.date, parsed.sequence)

        issues.sort(key=_sort_key, reverse=True)

        end = None if limit is None else offset + max(0, limit)
        return issues[offset:end]

    def read_issue(self, filename_or_id: str) -> Issue:
        """Load one issue by filename or issue id.

        Accepts a full filename (``ISSUE-YYYYMMDD-NNN-REPORTER.md``) or
        an id prefix (``ISSUE-YYYYMMDD-NNN``). Unlike tasks and reports,
        issues are never archived, so there is only one location to
        search.

        Raises:
            TaskNotFoundError: no match. The ``Task`` prefix is
                retained here because the 0.6 exception hierarchy does
                not include a dedicated ``IssueNotFoundError`` — the
                semantic meaning is the same.
            ValidationError | ProtocolViolation: malformed frontmatter.
        """
        target = self._resolve_issue_file(filename_or_id)
        if target is None:
            raise TaskNotFoundError(
                f"no issue matches {filename_or_id!r}",
                query=filename_or_id,
            )
        return _load_issue_strict(target)

    def _resolve_issue_file(
        self, filename_or_id: str
    ) -> pathlib.Path | None:
        """Resolve a user handle to an on-disk issue path, or ``None``.

        Accepts full filename or ``ISSUE-YYYYMMDD-NNN`` prefix. Issues
        live only in ``issues_dir`` — there is no archive equivalent,
        so resolution is a single-directory scan.
        """
        directory = self.issues_dir
        if not directory.is_dir():
            return None

        if ISSUE_FILENAME_RE.fullmatch(filename_or_id):
            candidate = directory / filename_or_id
            return candidate if candidate.is_file() else None

        prefix = filename_or_id
        for entry in directory.iterdir():
            if not entry.is_file():
                continue
            parsed = parse_issue_filename(entry.name)
            if parsed is None:
                continue
            if parsed.issue_id == prefix or entry.name.startswith(
                prefix + "-"
            ):
                return entry
        return None

    # ── Templates ─────────────────────────────────────────────────────

    def deploy_role_templates(
        self,
        *,
        team: str | None = None,
        lang: str | None = None,
        force: bool = True,
    ) -> DeploymentReport:
        """Deploy three-layer team templates into ``docs/agents/shared/``.

        Layer 1 (``TEAM-README.md`` + ``TEAM-ROLES.md`` +
        ``TEAM-OPERATING-RULES.md``) + layer 2 (``roles/<code>.md``).

        Args:
            team: Override the team from ``self.config``. If ``None``,
                  uses the project's configured team.
            lang: Override the language. If ``None``, uses
                  ``self.config.lang``.
            force: If ``True`` (the default), the aggressive migration
                   strategy archives conflicting files to
                   ``.fcop/migrations/<timestamp>/`` before overwriting.
                   If ``False``, existing files are skipped.

        Returns:
            A :class:`DeploymentReport` detailing what was deployed,
            what was skipped, and what was archived.
        """
        raise NotImplementedError

    # ── Suggestions ───────────────────────────────────────────────────

    def drop_suggestion(
        self,
        *,
        content: str,
        context: str = "",
    ) -> pathlib.Path:
        """Append a proposal under ``.fcop/proposals/``.

        Used by agents to log ideas that don't fit the task/report/issue
        channels. Returns the path of the written file.
        """
        raise NotImplementedError


# ── module-level helpers ──────────────────────────────────────────────

# Cap for :meth:`Project.status` recent-activity output. Intentionally
# small so callers don't pay for a full directory scan on every status
# call; tweak via a future kwarg when a real use case shows up.
_RECENT_ACTIVITY_LIMIT = 10

# How many times :meth:`Project.write_task` retries on sequence-number
# collisions before bailing out. Ten is generous: the lock window is a
# single ``os.open(O_EXCL)``, so collisions are extremely unlikely
# outside of intentional stress tests.
_MAX_WRITE_RETRIES = 10

# File suffixes that the FCoP grammar allows. ``.md`` is canonical;
# legacy 0.5.x projects sometimes carry ``.fcop``. Anything else is
# ignored entirely when counting.
_FCOP_SUFFIXES = frozenset({".md", ".fcop"})

# Report status values. Kept here instead of in :mod:`fcop.core.schema`
# because reports don't yet have a dedicated ReportFrontmatter model —
# the status rides in ``TaskFrontmatter.extra["status"]`` for 0.6 and
# will migrate when we split report parsing into its own module.
_VALID_REPORT_STATUSES: frozenset[str] = frozenset(
    {"done", "blocked", "in_progress"}
)


def _now_iso() -> str:
    """Return the current local time as an ISO-8601 string.

    Local time (not UTC) matches the operator's wall clock — FCoP
    files are authored interactively and a human reading
    ``created_at`` cares about "when did I create this on my laptop",
    not a UTC offset. Seconds-level precision is sufficient; we don't
    include microseconds because the value is informational only.
    """
    return _dt.datetime.now().replace(microsecond=0).isoformat()


def _try_load_task(
    path: pathlib.Path, *, is_archived: bool
) -> Task | None:
    """Best-effort load of one task file; return ``None`` on any problem.

    Used by :meth:`Project.list_tasks` where a single corrupt file must
    not break the enumeration. Strict loading lives in
    :func:`_load_task_strict`.
    """
    if not path.is_file():
        return None
    if path.suffix.lower() not in _FCOP_SUFFIXES:
        return None
    parsed = parse_task_filename(path.name)
    if parsed is None:
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    try:
        fm, body = parse_task_frontmatter(text)
    except Exception:
        # Covers ValidationError, ProtocolViolation, and any unexpected
        # parser bug — list_tasks is advertised as lenient.
        return None
    try:
        mtime = _dt.datetime.fromtimestamp(path.stat().st_mtime)
    except OSError:
        return None
    return Task(
        path=path,
        filename=path.name,
        task_id=parsed.task_id,
        date=parsed.date,
        sequence=parsed.sequence,
        frontmatter=fm,
        body=body,
        is_archived=is_archived,
        mtime=mtime,
    )


def _load_task_strict(
    path: pathlib.Path, *, is_archived: bool
) -> Task:
    """Strict load for :meth:`Project.read_task` — propagates errors.

    Callers who want a boolean-ish result should use
    :func:`_try_load_task` instead.
    """
    text = path.read_text(encoding="utf-8")
    fm, body = parse_task_frontmatter(text)
    parsed = parse_task_filename(path.name)
    assert parsed is not None, (
        f"_resolve_task_file returned {path.name!r} but it does not match "
        "TASK_FILENAME_RE — this is a bug in the resolver."
    )
    mtime = _dt.datetime.fromtimestamp(path.stat().st_mtime)
    return Task(
        path=path,
        filename=path.name,
        task_id=parsed.task_id,
        date=parsed.date,
        sequence=parsed.sequence,
        frontmatter=fm,
        body=body,
        is_archived=is_archived,
        mtime=mtime,
    )


def _extract_report_status(
    fm: TaskFrontmatter,
) -> Literal["done", "blocked", "in_progress"]:
    """Pull and validate the ``status`` field from a report's frontmatter.

    Reports store their status as a top-level YAML key that ends up in
    :attr:`TaskFrontmatter.extra` (since 0.6 reuses ``TaskFrontmatter``
    for both tasks and reports). A missing status is treated as
    ``"done"`` so older reports that predate the field still load.

    Raises:
        ProtocolViolation: the field exists but its value is not one
            of ``done`` / ``blocked`` / ``in_progress``. We intentionally
            accept a missing field but reject a malformed one — the
            former is a version-skew story, the latter is a bug.
    """
    raw = fm.extra.get("status", "done")
    if not isinstance(raw, str) or raw not in _VALID_REPORT_STATUSES:
        raise ProtocolViolation(
            f"report status must be one of {sorted(_VALID_REPORT_STATUSES)}; "
            f"got {raw!r}",
            rule="report.status",
        )
    return raw  # type: ignore[return-value]


def _try_load_report(
    path: pathlib.Path, *, is_archived: bool
) -> Report | None:
    """Best-effort report load; return ``None`` on any problem.

    Mirrors :func:`_try_load_task` — used by
    :meth:`Project.list_reports` where one bad file must not break
    the enumeration.
    """
    if not path.is_file():
        return None
    if path.suffix.lower() not in _FCOP_SUFFIXES:
        return None
    parsed = parse_report_filename(path.name)
    if parsed is None:
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    try:
        fm, body = parse_task_frontmatter(text)
    except Exception:
        return None
    # A report without a `references:` entry is protocol-ambiguous:
    # we don't know which task it replies to. Skip rather than guess.
    if not fm.references:
        return None
    try:
        status = _extract_report_status(fm)
    except ProtocolViolation:
        return None
    try:
        mtime = _dt.datetime.fromtimestamp(path.stat().st_mtime)
    except OSError:
        return None
    return Report(
        path=path,
        filename=path.name,
        task_id=fm.references[0],
        reporter=fm.sender,
        recipient=fm.recipient,
        status=status,
        body=body,
        is_archived=is_archived,
        mtime=mtime,
    )


def _load_report_strict(
    path: pathlib.Path, *, is_archived: bool
) -> Report:
    """Strict report load for :meth:`Project.read_report`.

    Unlike :func:`_try_load_report`, missing/invalid pieces raise.
    Used where the caller asked for a specific file and silent
    skipping would hide the problem.
    """
    text = path.read_text(encoding="utf-8")
    fm, body = parse_task_frontmatter(text)
    parsed = parse_report_filename(path.name)
    assert parsed is not None, (
        f"_resolve_report_file returned {path.name!r} but it does not match "
        "REPORT_FILENAME_RE — this is a bug in the resolver."
    )
    if not fm.references:
        raise ProtocolViolation(
            f"report {path.name} has no `references:` — cannot identify "
            "the task it responds to",
            rule="report.references",
        )
    status = _extract_report_status(fm)
    mtime = _dt.datetime.fromtimestamp(path.stat().st_mtime)
    return Report(
        path=path,
        filename=path.name,
        task_id=fm.references[0],
        reporter=fm.sender,
        recipient=fm.recipient,
        status=status,
        body=body,
        is_archived=is_archived,
        mtime=mtime,
    )


def _assemble_issue_file(
    frontmatter_data: dict[str, object], body: str
) -> str:
    """Serialize an issue frontmatter + body into a complete file text.

    Issues don't use :class:`TaskFrontmatter` — they have no recipient
    and carry ``summary`` / ``severity`` instead of ``priority``. We
    write the YAML directly rather than shoe-horning issue fields into
    the task dataclass. Field order is deterministic (identity fields
    first, then reporter, severity, summary) so round-tripping produces
    minimal diffs.
    """
    ordered: dict[str, object] = {}
    # Keep a canonical order — mirrors serialize_task_frontmatter's
    # "protocol/version first" discipline.
    for key in ("protocol", "version", "reporter", "severity", "summary"):
        if key in frontmatter_data:
            ordered[key] = frontmatter_data[key]
    for key in sorted(frontmatter_data):
        if key not in ordered:
            ordered[key] = frontmatter_data[key]

    yaml_text = yaml.safe_dump(
        ordered,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
    )
    fm_text = (
        f"{FRONTMATTER_DELIMITER}\n{yaml_text}{FRONTMATTER_DELIMITER}\n"
    )
    if not body:
        return fm_text
    return f"{fm_text}\n{body.lstrip(chr(10))}"


def _parse_issue_frontmatter(
    text: str,
) -> tuple[str, Severity, str, str]:
    """Parse issue frontmatter, returning ``(reporter, severity, summary, body)``.

    Unlike :func:`parse_task_frontmatter`, this accepts a much smaller
    schema: no sender / recipient / priority, but ``reporter``,
    ``severity``, and ``summary`` are mandatory. Historical
    ``protocol`` / ``version`` are still validated.

    Raises:
        ProtocolViolation: required field missing or wrong protocol.
        ValidationError: malformed YAML or bad role code / severity.
    """
    raw = parse_frontmatter_raw(text)
    _, body = split_frontmatter(text)

    for required in ("protocol", "version", "reporter", "severity", "summary"):
        if required not in raw or raw[required] in (None, ""):
            raise ProtocolViolation(
                f"missing required issue frontmatter field: {required}",
                rule="issue.frontmatter.required",
            )

    reporter = str(raw["reporter"]).strip()
    role_issues = validate_role_code(
        reporter, field="reporter", allow_reserved=True
    )
    role_errors = [i for i in role_issues if i.severity == "error"]
    if role_errors:
        raise ValidationError(
            f"invalid reporter role code {reporter!r}",
            issues=role_errors,
        )

    severity_enum = normalize_severity(str(raw["severity"]))
    summary = str(raw["summary"]).strip()
    if not summary:
        raise ProtocolViolation(
            "issue summary must be non-empty",
            rule="issue.frontmatter.required",
        )

    return reporter, severity_enum, summary, body


def _try_load_issue(path: pathlib.Path) -> Issue | None:
    """Best-effort issue load; ``None`` on any problem.

    Companion to :func:`_try_load_task` / :func:`_try_load_report` for
    the :meth:`Project.list_issues` enumeration.
    """
    if not path.is_file():
        return None
    if path.suffix.lower() not in _FCOP_SUFFIXES:
        return None
    parsed = parse_issue_filename(path.name)
    if parsed is None:
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    try:
        reporter, severity_enum, summary, body = _parse_issue_frontmatter(text)
    except Exception:
        return None
    try:
        mtime = _dt.datetime.fromtimestamp(path.stat().st_mtime)
    except OSError:
        return None
    return Issue(
        path=path,
        filename=path.name,
        issue_id=parsed.issue_id,
        summary=summary,
        severity=severity_enum,
        reporter=reporter,
        body=body,
        mtime=mtime,
    )


def _load_issue_strict(path: pathlib.Path) -> Issue:
    """Strict issue load for :meth:`Project.read_issue`."""
    text = path.read_text(encoding="utf-8")
    reporter, severity_enum, summary, body = _parse_issue_frontmatter(text)
    parsed = parse_issue_filename(path.name)
    assert parsed is not None, (
        f"_resolve_issue_file returned {path.name!r} but it does not match "
        "ISSUE_FILENAME_RE — this is a bug in the resolver."
    )
    mtime = _dt.datetime.fromtimestamp(path.stat().st_mtime)
    return Issue(
        path=path,
        filename=path.name,
        issue_id=parsed.issue_id,
        summary=summary,
        severity=severity_enum,
        reporter=reporter,
        body=body,
        mtime=mtime,
    )


def _count_matching(directory: pathlib.Path, pattern) -> int:  # type: ignore[no-untyped-def]
    """Count files in *directory* whose name matches *pattern*.

    Missing directories are treated as empty — ``status()`` must be
    safe to call on uninitialized projects. We do a shallow scan only;
    archives live under a separate ``log/`` path, not nested.
    """
    if not directory.is_dir():
        return 0
    total = 0
    for entry in directory.iterdir():
        if not entry.is_file():
            continue
        if entry.suffix.lower() not in _FCOP_SUFFIXES:
            continue
        if pattern.match(entry.name):
            total += 1
    return total


def _collect_recent_activity(
    *,
    tasks_dir: pathlib.Path,
    reports_dir: pathlib.Path,
    issues_dir: pathlib.Path,
    limit: int,
) -> tuple[RecentActivityEntry, ...]:
    """Return the newest *limit* entries across tasks/reports/issues.

    Entries are ordered by filesystem mtime, descending. "Newest" is a
    UX hint, not a correctness claim — an external tool that rewrites
    files can perturb the order harmlessly.
    """
    candidates: list[RecentActivityEntry] = []
    for kind, directory, pattern in (
        ("task", tasks_dir, TASK_FILENAME_RE),
        ("report", reports_dir, REPORT_FILENAME_RE),
        ("issue", issues_dir, ISSUE_FILENAME_RE),
    ):
        if not directory.is_dir():
            continue
        for entry in directory.iterdir():
            if not entry.is_file():
                continue
            if entry.suffix.lower() not in _FCOP_SUFFIXES:
                continue
            if not pattern.match(entry.name):
                continue
            try:
                mtime = _dt.datetime.fromtimestamp(entry.stat().st_mtime)
            except OSError:
                continue
            candidates.append(
                RecentActivityEntry(
                    kind=kind,  # type: ignore[arg-type]
                    filename=entry.name,
                    mtime=mtime,
                    summary="",
                )
            )

    candidates.sort(key=lambda e: e.mtime, reverse=True)
    return tuple(candidates[:limit])
