"""C1 workspace identity behavior probes."""

from __future__ import annotations

import pytest

from .driver import V4ConformanceDriver


@pytest.mark.parametrize(
    ("test_id", "clause", "action"),
    [
        ("C1-N01", "F4.2.1-F4.2.3", "create"),
        ("C1-R01", "F4.2.2", "create"),
        ("C1-FORK-01", "F4.2.4", "derive"),
        ("C1-OFFLINE-01", "F4.2.6", "create"),
    ],
    ids=["C1-N01", "C1-R01", "C1-FORK-01", "C1-OFFLINE-01"],
)
def test_c1_contract(
    v4_driver: V4ConformanceDriver, test_id: str, clause: str, action: str
) -> None:
    if action == "derive":
        v4_driver.derive_workspace(test_id=test_id, clause=clause)
    else:
        v4_driver.create_workspace(test_id=test_id, clause=clause)
