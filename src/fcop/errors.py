"""Exception hierarchy for the fcop library.

All exceptions raised by public API methods inherit from :class:`FcopError`.
Callers can catch this base class to handle any library-raised error, or
catch specific subclasses for fine-grained behavior.

See adr/ADR-0001-library-api.md ("异常体系") for the full contract.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fcop.models import BoundaryViolation, ValidationIssue

__all__ = [
    "FcopError",
    "ProtocolViolation",
    "BoundaryViolationError",
    "ValidationError",
    "ProjectNotFoundError",
    "ProjectAlreadyInitializedError",
    "TaskNotFoundError",
    "TeamNotFoundError",
    "RoleNotFoundError",
    "ConfigError",
]


class FcopError(Exception):
    """Base class for all errors raised by the fcop library.

    Catch this to handle any fcop-originated failure uniformly.
    """


class ProtocolViolation(FcopError):  # noqa: N818 — "Violation" names the
    # *domain concept* (FCoP protocol rules) precisely; renaming to
    # ProtocolViolationError would add an -Error suffix on top of FcopError's
    # and say less. This is a deliberate deviation from the PEP-8 style guide.
    """A requested operation would violate an FCoP protocol rule.

    Attributes:
        rule: The rule identifier that was violated, e.g. ``"Rule 4.1"``.
              Corresponds to the numbered rules in ``fcop-rules.mdc``.
    """

    def __init__(self, message: str, *, rule: str) -> None:
        super().__init__(message)
        self.rule = rule


class BoundaryViolationError(FcopError):  # noqa: N818 — same rationale as
    # ProtocolViolation: the domain term is "boundary violation"; an extra
    # -Error suffix on top of FcopError says less. The class name is
    # `...Error` (not `...Violation`) here only to avoid a collision with
    # the :class:`fcop.models.BoundaryViolation` value object — they
    # describe two facets of the same event (one is a record, the other
    # is the raisable form).
    """A requested operation would violate one or more boundary rules.

    Per ADR-0020 (Agent Boundary & Capability) + TASK-20260509-005.
    Raised from :meth:`fcop.Project.assert_boundary` and from
    :meth:`fcop.Project.write_review` when the reviewer's layer + the
    subject's layer trip rule ``NO_WORKER_REVIEWS_GOVERNANCE`` (or any
    other rule listed in :data:`fcop.core.boundary.BOUNDARY_RULES`).

    Attributes:
        violations: One :class:`fcop.models.BoundaryViolation` record
            per rule that was tripped. Always ``len >= 1`` — if the call
            site has nothing to report, it should not raise this class.
    """

    def __init__(
        self, message: str, *, violations: list[BoundaryViolation]
    ) -> None:
        super().__init__(message)
        self.violations = violations


class ValidationError(FcopError):
    """User input or an on-disk file failed validation.

    Attributes:
        issues: A list of :class:`ValidationIssue` records pinpointing
                every problem. At least one issue is guaranteed to be
                severity ``"error"``.
    """

    def __init__(self, message: str, *, issues: list[ValidationIssue]) -> None:
        super().__init__(message)
        self.issues = issues


class ProjectNotFoundError(FcopError):
    """The given path does not contain a valid FCoP project structure.

    Attributes:
        path: The path that was probed.
    """

    def __init__(self, message: str, *, path: Path) -> None:
        super().__init__(message)
        self.path = path


class ProjectAlreadyInitializedError(FcopError):
    """``Project.init()`` was called on an already-initialized project.

    Pass ``force=True`` to overwrite in place (destructive).
    """


class TaskNotFoundError(FcopError):
    """No task file matches the given filename or task id.

    Attributes:
        query: The filename, task id, or partial string that was searched.
    """

    def __init__(self, message: str, *, query: str) -> None:
        super().__init__(message)
        self.query = query


class TeamNotFoundError(FcopError):
    """The requested team is not bundled and not in the project config.

    Attributes:
        team: The requested team slug, e.g. ``"mystery-team"``.
    """

    def __init__(self, message: str, *, team: str) -> None:
        super().__init__(message)
        self.team = team


class RoleNotFoundError(FcopError):
    """The requested role code is not registered in the project config.

    Attributes:
        role: The requested role code, e.g. ``"QA"``.
    """

    def __init__(self, message: str, *, role: str) -> None:
        super().__init__(message)
        self.role = role


class ConfigError(FcopError):
    """``docs/agents/fcop.json`` is missing, malformed, or inconsistent.

    Attributes:
        path: The offending config file path.
    """

    def __init__(self, message: str, *, path: Path) -> None:
        super().__init__(message)
        self.path = path
