"""Exception hierarchy for the fcop library.

All exceptions raised by public API methods inherit from :class:`FcopError`.
Callers can catch this base class to handle any library-raised error, or
catch specific subclasses for fine-grained behavior.

See adr/ADR-0001-library-api.md ("异常体系") for the full contract.
"""

from __future__ import annotations

from enum import Enum as _Enum
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


class _V4Code(str, _Enum):
    """Frozen Base codes plus one explicitly namespaced Toolkit extension."""

    WORKSPACE_ID_MISMATCH = "WORKSPACE_ID_MISMATCH"
    WORKSPACE_ID_CLONE_CONFLICT = "WORKSPACE_ID_CLONE_CONFLICT"
    UNSUPPORTED_PROTOCOL = "UNSUPPORTED_PROTOCOL"
    UNSUPPORTED_WORKSPACE_VERSION = "UNSUPPORTED_WORKSPACE_VERSION"
    UNSUPPORTED_ENCODING = "UNSUPPORTED_ENCODING"
    INVALID_ENVELOPE = "INVALID_ENVELOPE"
    RELATION_INVALID = "RELATION_INVALID"
    REFERENCE_UNRESOLVED = "REFERENCE_UNRESOLVED"
    BRANCH_DEPTH_EXCEEDED = "BRANCH_DEPTH_EXCEEDED"
    ROOT_NOT_ACTIVE = "ROOT_NOT_ACTIVE"
    REPORT_REQUIRED = "REPORT_REQUIRED"
    REPORT_HEAD_AMBIGUOUS = "REPORT_HEAD_AMBIGUOUS"
    ATTEMPT_MISMATCH = "ATTEMPT_MISMATCH"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    FAMILY_CONVERGENCE_REQUIRED = "FAMILY_CONVERGENCE_REQUIRED"
    FAMILY_CONVERGENCE_MISMATCH = "FAMILY_CONVERGENCE_MISMATCH"
    EVIDENCE_DIGEST_MISMATCH = "EVIDENCE_DIGEST_MISMATCH"
    AUTHORIZATION_REQUIRED = "AUTHORIZATION_REQUIRED"
    AUTHORIZATION_INVALID = "AUTHORIZATION_INVALID"
    AUTHORIZATION_EXPIRED = "AUTHORIZATION_EXPIRED"
    AUTHORIZATION_REUSED = "AUTHORIZATION_REUSED"
    AUTHORIZATION_PROFILE_UNAVAILABLE = "AUTHORIZATION_PROFILE_UNAVAILABLE"
    OPERATION_ID_CONFLICT = "OPERATION_ID_CONFLICT"
    INVALID_TRANSITION = "INVALID_TRANSITION"
    BRANCH_NOT_TERMINAL = "BRANCH_NOT_TERMINAL"
    LEGACY_TRANSITION_NOT_ALLOWED = "LEGACY_TRANSITION_NOT_ALLOWED"
    TARGET_ALREADY_EXISTS_DIFFERENT = "TARGET_ALREADY_EXISTS_DIFFERENT"
    STATE_AMBIGUOUS = "STATE_AMBIGUOUS"
    RECOVERY_REQUIRED = "RECOVERY_REQUIRED"
    LOCK_RECOVERY_REQUIRED = "LOCK_RECOVERY_REQUIRED"
    UNSUPPORTED_FILESYSTEM = "UNSUPPORTED_FILESYSTEM"
    OPERATION_NOT_IMPLEMENTED = "toolkit:OPERATION_NOT_IMPLEMENTED"


class V4ProtocolError(FcopError):
    """Machine-readable 4.0 failure; no changes to the legacy hierarchy."""

    def __init__(
        self, code: _V4Code, message: str, *, operation_ref: str | None = None,
        subject_ref: str | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code.value
        self.operation_ref = operation_ref
        self.subject_ref = subject_ref


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
