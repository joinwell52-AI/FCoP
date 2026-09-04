"""One version boundary, preserving native bound methods for legacy projects."""

from __future__ import annotations

import inspect
from collections.abc import Callable
from functools import wraps
from typing import Any, cast

from fcop.errors import V4ProtocolError, _V4Code


class _VersionedMethod:
    """Dispatch class and instance calls identically, without request sniffing."""

    def __init__(self, legacy: Callable[..., Any]) -> None:
        self.legacy = legacy
        self.__name__ = legacy.__name__
        self.__doc__ = legacy.__doc__
        self.__signature__ = inspect.signature(legacy)

    def __get__(self, instance: Any, owner: type | None = None) -> Callable[..., Any]:
        if instance is None:
            return self
        creation = instance.__dict__.get("_v4_creation")
        if creation is None:
            return cast(Callable[..., Any], self.legacy.__get__(instance, owner))
        handler = creation.handler(self.__name__)
        if handler is not None:

            @wraps(handler)
            def invoke(*args: Any, **kwargs: Any) -> Any:
                try:
                    return handler(*args, **kwargs)
                except V4ProtocolError as exc:
                    if exc.operation_ref is None:
                        exc.operation_ref = kwargs.get("operation_id") or self.__name__
                    if exc.subject_ref is None:
                        exc.subject_ref = (
                            kwargs.get("subject_ref")
                            or kwargs.get("task_id")
                            or kwargs.get("workspace_id")
                            or creation.manifest.get("workspace_id")
                        )
                    raise

            return invoke

        def unavailable(*args: Any, **kwargs: Any) -> Any:
            code = (
                _V4Code.LEGACY_TRANSITION_NOT_ALLOWED
                if self.__name__ in {"finish_task", "archive_to_history"}
                else _V4Code.OPERATION_NOT_IMPLEMENTED
            )
            raise V4ProtocolError(
                code,
                f"{self.__name__} is not available in the WP3A creation plane",
                operation_ref=self.__name__,
                subject_ref=kwargs.get("task_id"),
            )

        return unavailable

    def __call__(self, instance: Any, *args: Any, **kwargs: Any) -> Any:
        return self.__get__(instance, type(instance))(*args, **kwargs)


def version_boundary(cls: type) -> type:
    """Keep legacy functions intact behind a single Project descriptor layer."""
    for name, value in list(vars(cls).items()):
        if not name.startswith("_") and inspect.isfunction(value):
            setattr(cls, name, _VersionedMethod(value))
    return cls
