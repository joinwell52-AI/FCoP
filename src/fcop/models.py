"""Public read-only data structures returned by the fcop library.

All models are :func:`dataclasses.dataclass(frozen=True, slots=True)` so
they are hashable, immutable, and have a tiny memory footprint. They are
the public contract of the library — changing any field name, type, or
default in a non-additive way is a breaking change per semver.

See adr/ADR-0001-library-api.md ("数据结构") for the full contract.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Literal

__all__ = [
    "Priority",
    "Severity",
    "TaskFrontmatter",
    "Task",
    "Report",
    "Issue",
    "TeamConfig",
    "ProjectStatus",
    "RecentActivityEntry",
    "ValidationIssue",
    "DeploymentReport",
]


# ── Enums ─────────────────────────────────────────────────────────────


class Priority(str, Enum):
    """Task priority band. Matches the four P-levels in fcop-rules.mdc."""

    P0 = "P0"
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"


class Severity(str, Enum):
    """Issue severity band."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ── Task ──────────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class TaskFrontmatter:
    """Parsed YAML frontmatter of a TASK-*.md file.

    Unknown keys are preserved in :attr:`extra` so forward-compatible
    additions to the protocol don't silently drop data.
    """

    protocol: str
    version: int
    sender: str
    recipient: str
    priority: Priority
    thread_key: str | None = None
    subject: str | None = None
    references: tuple[str, ...] = ()
    extra: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class Task:
    """A task file on disk.

    Properties :attr:`sender`, :attr:`recipient`, :attr:`priority`,
    :attr:`subject` are convenience accessors forwarding to
    :attr:`frontmatter`.
    """

    path: Path
    filename: str
    task_id: str
    date: str
    sequence: int
    frontmatter: TaskFrontmatter
    body: str
    is_archived: bool
    mtime: datetime

    @property
    def sender(self) -> str:
        return self.frontmatter.sender

    @property
    def recipient(self) -> str:
        return self.frontmatter.recipient

    @property
    def priority(self) -> Priority:
        return self.frontmatter.priority

    @property
    def subject(self) -> str | None:
        return self.frontmatter.subject


# ── Report ────────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class Report:
    """A report file responding to a task."""

    path: Path
    filename: str
    task_id: str
    reporter: str
    recipient: str
    status: Literal["done", "blocked", "in_progress"]
    body: str
    is_archived: bool
    mtime: datetime


# ── Issue ─────────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class Issue:
    """An issue file.

    Issues are broadcasts that don't follow the A-to-B task chain:
    they describe a problem observed by any role, addressed to whoever
    can fix it.
    """

    path: Path
    filename: str
    issue_id: str
    summary: str
    severity: Severity
    reporter: str
    body: str
    mtime: datetime


# ── Project configuration ────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class TeamConfig:
    """In-memory representation of ``docs/agents/fcop.json``."""

    mode: Literal["solo", "preset", "custom"]
    team: str
    leader: str
    roles: tuple[str, ...]
    lang: str
    version: int
    extra: dict[str, object] = field(default_factory=dict)

    @property
    def is_solo(self) -> bool:
        return self.mode == "solo"


# ── Status ────────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class RecentActivityEntry:
    """A single row in :attr:`ProjectStatus.recent_activity`."""

    kind: Literal["task", "report", "issue"]
    filename: str
    mtime: datetime
    summary: str


@dataclass(frozen=True, slots=True)
class ProjectStatus:
    """A snapshot of project-wide counts and the most recent activity."""

    path: Path
    is_initialized: bool
    config: TeamConfig | None
    tasks_open: int
    tasks_archived: int
    reports_count: int
    issues_count: int
    recent_activity: tuple[RecentActivityEntry, ...]


# ── Validation ────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    """A single problem found by ``inspect_task`` or ``validate_team``.

    ``severity == "error"`` means "rejected, won't write/accept";
    ``"warning"`` means "accepted but discouraged"; ``"info"`` is purely
    diagnostic.
    """

    severity: Literal["error", "warning", "info"]
    field: str
    message: str
    path: Path | None = None


# ── Deployment ────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class DeploymentReport:
    """Result of ``Project.deploy_role_templates()``.

    When ``force=True`` and conflicting files exist, they are moved to
    ``.fcop/migrations/<timestamp>/`` rather than overwritten silently.
    :attr:`migration_dir` points to that archive, or ``None`` if no
    archiving happened.
    """

    deployed: tuple[Path, ...]
    skipped: tuple[Path, ...]
    archived: tuple[Path, ...]
    migration_dir: Path | None
