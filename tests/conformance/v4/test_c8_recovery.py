"""C8 atomicity, recovery-state, and cross-layer race probes."""

from __future__ import annotations

import pytest

from .driver import V4ConformanceDriver


@pytest.mark.parametrize(
    ("test_id", "clause", "action"),
    [
        ("C8-N01", "F4.9.1-F4.9.4", "recover"),
        ("C8-R01", "F4.9.2", "recover"),
        ("C8-X01", "F4.9.1-F4.9.4; F4.9.9", "fault"),
        ("C8-X02", "F4.9.5", "recover"),
        ("C8-X03", "F4.9.4; F4.9.7", "recover"),
        ("C8-RETRY-01", "F4.9.8; F4.9.11", "recover"),
        ("C8-STATE-01", "F4.9.1; F4.9.9-F4.9.10", "recover"),
        ("C8-INDETERMINATE-01", "F4.9.1; F4.9.4; F4.9.9", "recover"),
    ],
    ids=[
        "C8-N01", "C8-R01", "C8-X01", "C8-X02", "C8-X03",
        "C8-RETRY-01", "C8-STATE-01", "C8-INDETERMINATE-01",
    ],
)
def test_c8_contract(
    v4_driver: V4ConformanceDriver, test_id: str, clause: str, action: str
) -> None:
    if action == "fault":
        v4_driver.inject_fault(test_id=test_id, clause=clause)
    else:
        v4_driver.require_recovery(test_id=test_id, clause=clause)


def test_at_02(v4_driver: V4ConformanceDriver) -> None:
    v4_driver.parallel_surface_probe(
        "list_branches",
        test_id="AT-02",
        clause="F4.5.4; F4.9.5",
        expected="linearized create-Branch versus Root archive",
    )


def test_at_05(v4_driver: V4ConformanceDriver) -> None:
    v4_driver.parallel_surface_probe(
        "recover_operation",
        test_id="AT-05",
        clause="F4.9.1-F4.9.11",
        expected="stable recovery across crash/response-loss commit boundaries",
    )


def test_at_06(v4_driver: V4ConformanceDriver) -> None:
    v4_driver.recover_operation(test_id="AT-06", clause="F4.9.2-F4.9.4")
