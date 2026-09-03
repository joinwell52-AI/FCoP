"""C4 relation behavior probes."""

from __future__ import annotations

import pytest

from .driver import V4ConformanceDriver


@pytest.mark.parametrize(
    ("test_id", "clause", "action"),
    [
        ("C4-N01", "F4.5.1-F4.5.2", "create"),
        ("C4-N02", "F4.5.3-F4.5.4", "branches"),
        ("C4-R01", "F4.5.2", "create"),
        ("C4-R02", "F4.5.3", "branches"),
    ],
    ids=["C4-N01", "C4-N02", "C4-R01", "C4-R02"],
)
def test_c4_contract(
    v4_driver: V4ConformanceDriver, test_id: str, clause: str, action: str
) -> None:
    if action == "branches":
        v4_driver.list_branches(test_id=test_id, clause=clause)
    else:
        v4_driver.create_task(test_id=test_id, clause=clause)
