"""Meta-tests proving names, parameters, and ``None`` stubs stay red."""

from __future__ import annotations

from pathlib import Path

import pytest

from .driver import V4ConformanceDriver, result_field


class EmptyStubProject:
    def create_task(self, **kwargs: object) -> None:
        return None

    def transition(self, **kwargs: object) -> None:
        return None

    def recover_operation(self, **kwargs: object) -> None:
        return None


@pytest.mark.parametrize("action", ["create_task", "transition", "recover_operation"])
def test_empty_stub_cannot_satisfy_behavior(tmp_path: Path, action: str) -> None:
    driver = V4ConformanceDriver(tmp_path)
    driver.project = EmptyStubProject()  # type: ignore[assignment]
    result = getattr(driver, action)(test_id="STUB-GUARD", clause="meta", marker="x")
    with pytest.raises(AssertionError, match="returned None"):
        result_field(result, "status")
