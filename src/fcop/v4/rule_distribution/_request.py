"""Bounded data-only input validation, independent of retired Host deployment."""

from collections.abc import Mapping
from typing import Any

from ._errors import reject


def safe_request(value: Any, action: str, depth: int = 0) -> None:
    if depth > 32:
        reject("RULE_SELECTION_INVALID", action, "Request nesting exceeds the bounded input shape")
    if callable(value):
        reject("RULE_HOST_UNAVAILABLE", action, "Caller executable logic is forbidden")
    if isinstance(value, Mapping):
        for key, item in value.items():
            if not isinstance(key, str) or any(
                term in key for term in ("evaluator", "resolver", "probe", "trusted_profiles", "caller_judge")
            ):
                reject("RULE_HOST_UNAVAILABLE", action, "Caller judging or discovery fields are forbidden")
            safe_request(item, action, depth + 1)
    elif isinstance(value, (list, tuple)):
        for item in value:
            safe_request(item, action, depth + 1)
