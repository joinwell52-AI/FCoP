"""C2 four-envelope and append-only fact behavior probes."""

from __future__ import annotations

import pytest

from .driver import V4ConformanceDriver


@pytest.mark.parametrize(
    ("test_id", "clause", "action"),
    [
        ("C2-N01", "F4.3.1-F4.3.2", "report"),
        ("C2-R01", "F4.3.1-F4.3.2", "review"),
        ("C2-R02", "F4.3.3; F4.3.5", "review"),
    ],
    ids=["C2-N01", "C2-R01", "C2-R02"],
)
def test_c2_contract(
    v4_driver: V4ConformanceDriver, test_id: str, clause: str, action: str
) -> None:
    if action == "report":
        v4_driver.write_report(test_id=test_id, clause=clause)
    else:
        v4_driver.write_review(test_id=test_id, clause=clause)
