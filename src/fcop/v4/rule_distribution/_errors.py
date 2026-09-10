"""Private Toolkit failures, independent of the frozen Base error registry."""

from typing import Any, NoReturn

from fcop.errors import FcopError

_CODES = frozenset({
    "RULE_MANIFEST_INVALID", "RULE_ARTIFACT_MISMATCH", "RULE_SELECTION_INVALID",
    "RULE_HOST_UNAVAILABLE", "RULE_PROJECTION_LIMIT", "RULE_OWNERSHIP_CONFLICT",
    "RULE_ADOPTION_REQUIRED", "RULE_DEPLOYMENT_RECOVERY_REQUIRED",
})


class _DistributionError(FcopError):
    def __init__(self, code: str, operation: str, reason: str) -> None:
        if code not in _CODES:
            raise ValueError("Unknown private distribution error")
        self.code = f"toolkit:{code}"
        self.operation = operation
        self.subject_ref = "fcop:rule-distribution"
        self.details: dict[str, Any] = {"reason": reason}
        super().__init__(f"{self.code}: {reason}")


def reject(code: str, operation: str, reason: str) -> NoReturn:
    # Reasons are implementation literals, never file bodies or caller paths.
    raise _DistributionError(code, operation, reason)
