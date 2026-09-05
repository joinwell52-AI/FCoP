"""Explicit Project method policies and native-function version wrappers."""

from __future__ import annotations

import inspect
from collections.abc import Callable
from functools import wraps
from types import MappingProxyType
from typing import Any

from fcop.errors import V4ProtocolError, _V4Code

# Every public method is classified, including the safe staticmethod. Adding a
# method requires a conscious policy choice, never an automatic catch-all.
_METHOD_POLICIES = MappingProxyType({
    "validate_team": "COMMON_SAFE",
    "create_workspace": "V4_HANDLER",
    "create_task": "V4_HANDLER",
    "derive_workspace": "V4_HANDLER",
    "inspect_state": "V4_HANDLER",
    "is_initialized": "V4_HANDLER",
    "write_task": "V4_HANDLER",
    "read_task": "V4_HANDLER",
    "write_report": "V4_HANDLER",
    "write_issue": "V4_HANDLER",
    "write_review": "V4_HANDLER",
    "mark_human_approved": "V4_HANDLER",
    "transition": "V4_HANDLER",  # structured rejection only in WP3A
    "family_digest": "V4_HANDLER",
    "finish_task": "LEGACY_ONLY",
    "archive_to_history": "LEGACY_ONLY",
    "init": "V4_MUTATION_REJECTED",
    "init_solo": "V4_MUTATION_REJECTED",
    "init_custom": "V4_MUTATION_REJECTED",
    "deploy_role_templates": "V4_MUTATION_REJECTED",
    "deploy_protocol_rules": "V4_MUTATION_REJECTED",
    "audit": "V4_MUTATION_REJECTED",  # can emit an inspection artifact
    "archive_task": "V4_MUTATION_REJECTED",
    "archive_review": "V4_MUTATION_REJECTED",
    "report_failure": "V4_MUTATION_REJECTED",
    "apply_recovery": "V4_MUTATION_REJECTED",
    "recover_session": "V4_MUTATION_REJECTED",
    "subscribe_events": "V4_MUTATION_REJECTED",
    "poll_once": "V4_MUTATION_REJECTED",
    "drop_suggestion": "V4_MUTATION_REJECTED",
    "status": "V4_READ_UNAVAILABLE",
    "role_occupancy": "V4_READ_UNAVAILABLE",
    "audit_drift": "V4_READ_UNAVAILABLE",
    "list_tasks": "V4_READ_UNAVAILABLE",
    "list_history": "V4_READ_UNAVAILABLE",
    "read_history_task": "V4_READ_UNAVAILABLE",
    "inspect_task": "V4_READ_UNAVAILABLE",
    "list_reports": "V4_READ_UNAVAILABLE",
    "read_report": "V4_READ_UNAVAILABLE",
    "list_issues": "V4_READ_UNAVAILABLE",
    "read_issue": "V4_READ_UNAVAILABLE",
    "list_reviews": "V4_READ_UNAVAILABLE",
    "read_review": "V4_READ_UNAVAILABLE",
    "boundary_violations": "V4_READ_UNAVAILABLE",
    "assert_boundary": "V4_READ_UNAVAILABLE",
})


def _versioned(legacy: Callable[..., Any], policy: str) -> Callable[..., Any]:
    # Ordinary functions restore class-level reflection, method binding and
    # unittest.mock autospec. __wrapped__ retains the unchanged v3 signature.
    @wraps(legacy)
    def invoke(instance: Any, *args: Any, **kwargs: Any) -> Any:
        creation = instance.__dict__.get("_v4_creation")
        if creation is None:
            return legacy(instance, *args, **kwargs)
        try:
            if creation.invalid:
                if legacy.__name__ == "is_initialized":
                    return legacy(instance, *args, **kwargs)
                return creation._invalid_declaration(*args, **kwargs)
            handler = creation.handler(legacy.__name__) if policy == "V4_HANDLER" else None
            if handler is not None:
                return handler(*args, **kwargs)
            raise V4ProtocolError(
                _V4Code.LEGACY_TRANSITION_NOT_ALLOWED
                if policy == "LEGACY_ONLY" else _V4Code.OPERATION_NOT_IMPLEMENTED,
                f"{legacy.__name__} is not available in the WP3A creation plane",
            )
        except V4ProtocolError as exc:
            if exc.operation_ref is None:
                exc.operation_ref = kwargs.get("operation_id") or legacy.__name__
            if exc.subject_ref is None:
                exc.subject_ref = (
                    kwargs.get("subject_ref") or kwargs.get("task_id")
                    or kwargs.get("workspace_id") or creation.manifest.get("workspace_id")
                )
            raise

    return invoke


def version_boundary(cls: type) -> type:
    """Install only explicitly classified version-sensitive method wrappers."""
    methods = {
        name: value for name, value in vars(cls).items()
        if not name.startswith("_") and (
            inspect.isfunction(value) or isinstance(value, (classmethod, staticmethod))
        )
    }
    if set(methods) != set(_METHOD_POLICIES):
        raise TypeError("Project public methods require explicit version policy classification")
    for name, value in methods.items():
        if _METHOD_POLICIES[name] != "COMMON_SAFE":
            if not inspect.isfunction(value):
                raise TypeError("Version-sensitive methods must be instance functions")
            setattr(cls, name, _versioned(value, _METHOD_POLICIES[name]))
    return cls


def bind_v4_methods(instance: Any, facade: type) -> None:
    """Bind supported v4 signatures without changing class or legacy surfaces.

    Only called at trusted initialization and successful workspace creation.
    Subclass overrides retain normal Python semantics, including super calls.
    """
    creation = instance.__dict__.get("_v4_creation")
    if creation is None or creation.invalid:
        return
    for name, policy in _METHOD_POLICIES.items():
        if policy != "V4_HANDLER":
            continue
        wrapper = vars(facade)[name]
        if inspect.getattr_static(type(instance), name) is not wrapper:
            continue
        handler = creation.handler(name)
        if handler is not None:
            instance.__dict__[name] = _bound_v4(instance, wrapper, handler)


def _bound_v4(
    instance: Any, wrapper: Callable[..., Any], handler: Callable[..., Any]
) -> Callable[..., Any]:
    @wraps(handler)
    def invoke(*args: Any, **kwargs: Any) -> Any:
        return wrapper(instance, *args, **kwargs)

    return invoke
