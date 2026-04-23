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

import datetime as _dt
import os
import pathlib
from collections.abc import Sequence
from typing import TYPE_CHECKING, Literal

from fcop.core.config import load_team_config
from fcop.core.filename import (
    ISSUE_FILENAME_RE,
    REPORT_FILENAME_RE,
    TASK_FILENAME_RE,
)
from fcop.models import ProjectStatus, RecentActivityEntry

if TYPE_CHECKING:
    from fcop.models import (
        DeploymentReport,
        Issue,
        Priority,
        Report,
        Severity,
        Task,
        TeamConfig,
        ValidationIssue,
    )

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
        """Initialize this directory as an FCoP project.

        Creates the ``docs/agents/{tasks,reports,issues,shared,log}/``
        tree, writes ``fcop.json``, deploys the Cursor rule files
        (``.cursor/rules/fcop-rules.mdc`` + ``fcop-protocol.mdc``),
        deploys the chosen team's four-layer templates into
        ``docs/agents/shared/``, and writes a welcome task.

        Args:
            team: Name of a bundled preset team. See
                  :func:`fcop.teams.get_available_teams`.
            lang: ``"zh"`` or ``"en"``; drives template language and
                  letter-to-admin selection.
            force: If ``True``, overwrite an existing initialization.
                   Conflicting files are archived to
                   ``.fcop/migrations/<timestamp>/``.

        Returns:
            A :class:`ProjectStatus` snapshot of the freshly initialized
            project.

        Raises:
            ProjectAlreadyInitializedError: ``fcop.json`` already exists
                and ``force=False``.
            TeamNotFoundError: ``team`` is not a bundled preset.
        """
        raise NotImplementedError

    def init_solo(
        self,
        *,
        role_code: str = "ME",
        lang: str = "zh",
        force: bool = False,
    ) -> ProjectStatus:
        """Initialize in Solo mode (single role, directly interfacing with ADMIN).

        Solo mode is meant for individual users who want FCoP's file
        discipline without a multi-agent team. Only one role is
        registered (default ``"ME"``).
        """
        raise NotImplementedError

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

        Equivalent to the legacy ``create_custom_team()`` tool. Use
        :meth:`validate_team` first to surface any naming or structural
        issues without writing files.

        Raises:
            ValidationError: the team config is invalid. The raised
                exception's ``.issues`` list mirrors what
                :meth:`validate_team` returns.
        """
        raise NotImplementedError

    @staticmethod
    def validate_team(
        *,
        roles: Sequence[str],
        leader: str,
    ) -> list[ValidationIssue]:
        """Dry-run validation of a custom team config.

        Does not touch the filesystem. Returns a list of issues; an
        empty list means the config is valid.
        """
        raise NotImplementedError

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
    ) -> Task:
        """Create a new task file.

        Filename is auto-generated as
        ``TASK-YYYYMMDD-NNN-{sender}-to-{recipient}.md``. ``NNN`` is
        today's existing task count + 1. On concurrent-write
        collisions the sequence is retried up to 10 times before
        giving up with a :class:`RuntimeError`.

        Raises:
            ProtocolViolation: the sender → recipient edge is not
                allowed by the role chain (Rule 4).
            ValidationError: ``priority``/``subject``/``body`` is
                missing or malformed.
        """
        raise NotImplementedError

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

        ``date`` is a ``YYYYMMDD`` string.

        Results are sorted by ``(date desc, sequence desc)`` i.e.
        newest first.
        """
        raise NotImplementedError

    def read_task(self, filename_or_id: str) -> Task:
        """Load one task by full filename or by task id (``TASK-YYYYMMDD-NNN``).

        Raises:
            TaskNotFoundError: no file matches.
        """
        raise NotImplementedError

    def archive_task(self, filename_or_id: str) -> Task:
        """Move a task (and any matching report) to ``log/``.

        Returns the archived :class:`Task` with ``is_archived == True``
        and updated ``path``.
        """
        raise NotImplementedError

    def inspect_task(self, filename_or_id: str) -> list[ValidationIssue]:
        """Validate a task file against the FCoP schema.

        Empty list means the file is valid. Otherwise every problem is
        reported as a :class:`ValidationIssue` — unlike writers, this
        method does **not** raise on errors.
        """
        raise NotImplementedError

    # ── Reports ───────────────────────────────────────────────────────

    def write_report(
        self,
        *,
        task_id: str,
        reporter: str,
        recipient: str,
        body: str,
        status: Literal["done", "blocked", "in_progress"] = "done",
    ) -> Report:
        """Create a report responding to an existing task.

        Raises:
            TaskNotFoundError: ``task_id`` has no matching task file.
            ProtocolViolation: ``reporter`` is not the original task's
                recipient (Rule 5).
        """
        raise NotImplementedError

    def list_reports(
        self,
        *,
        reporter: str | None = None,
        task_id: str | None = None,
        limit: int | None = None,
    ) -> list[Report]:
        """List reports, optionally filtered."""
        raise NotImplementedError

    def read_report(self, filename_or_id: str) -> Report:
        """Load one report by filename or report id."""
        raise NotImplementedError

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
        registered role can write one.
        """
        raise NotImplementedError

    def list_issues(self, *, limit: int | None = None) -> list[Issue]:
        """List all issues, newest first."""
        raise NotImplementedError

    def read_issue(self, filename_or_id: str) -> Issue:
        """Load one issue by filename or issue id."""
        raise NotImplementedError

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

# File suffixes that the FCoP grammar allows. ``.md`` is canonical;
# legacy 0.5.x projects sometimes carry ``.fcop``. Anything else is
# ignored entirely when counting.
_FCOP_SUFFIXES = frozenset({".md", ".fcop"})


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
