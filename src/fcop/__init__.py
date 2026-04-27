"""fcop — Python library for the File-based Coordination Protocol.

FCoP (File-based Coordination Protocol) is a lightweight protocol that
lets multiple AI agents collaborate through a shared filesystem. This
package is a pure-Python SDK for creating, reading, validating, and
archiving FCoP artifacts (tasks, reports, issues).

Quick start::

    from fcop import Project, Priority

    project = Project("./myproject")
    if not project.is_initialized():
        project.init(team="dev-team", lang="zh")

    task = project.write_task(
        sender="ADMIN",
        recipient="PM",
        priority=Priority.P1,
        subject="登录模块偶发 500",
        body="麻烦排一下最近的报错，看能否复现。",
    )
    print(task.filename)

The full public API is documented in
adr/ADR-0001-library-api.md. Anything imported below is stable within
the current minor version; anything NOT exported here (notably
:mod:`fcop.core`) is internal and may change without notice.

Design principles:
    * **Zero MCP coupling** — this package has no MCP/fastmcp imports.
    * **Zero LLM coupling** — no OpenAI / Anthropic / Gemini SDKs.
    * **Zero global state** — configuration flows through ``Project``
      constructor arguments, not environment variables.
    * **Structured returns** — every method returns dataclasses, never
      pre-formatted strings.

For the MCP server that wraps this library, install the companion
``fcop-mcp`` package.
"""

from __future__ import annotations

from fcop import rules, teams
from fcop._version import __version__
from fcop.errors import (
    ConfigError,
    FcopError,
    ProjectAlreadyInitializedError,
    ProjectNotFoundError,
    ProtocolViolation,
    RoleNotFoundError,
    TaskNotFoundError,
    TeamNotFoundError,
    ValidationError,
)
from fcop.models import (
    DeploymentReport,
    DriftEntry,
    DriftReport,
    Issue,
    Priority,
    ProjectStatus,
    RecentActivityEntry,
    Report,
    RoleOccupancy,
    SessionRoleConflict,
    Severity,
    Task,
    TaskFrontmatter,
    TeamConfig,
    ValidationIssue,
)
from fcop.project import Project

__all__ = [
    # Version
    "__version__",
    # Main facade
    "Project",
    # Data models
    "Task",
    "TaskFrontmatter",
    "Report",
    "Issue",
    "TeamConfig",
    "ProjectStatus",
    "RecentActivityEntry",
    "RoleOccupancy",
    "DriftEntry",
    "DriftReport",
    "SessionRoleConflict",
    "ValidationIssue",
    "DeploymentReport",
    "Priority",
    "Severity",
    # Exceptions
    "FcopError",
    "ProtocolViolation",
    "ValidationError",
    "ProjectNotFoundError",
    "ProjectAlreadyInitializedError",
    "TaskNotFoundError",
    "TeamNotFoundError",
    "RoleNotFoundError",
    "ConfigError",
    # Sub-modules
    "teams",
    "rules",
]
