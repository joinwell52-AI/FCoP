"""C7 durable create idempotency behavior probes."""

from __future__ import annotations

import pytest

from .driver import V4ConformanceDriver


@pytest.mark.parametrize(
    ("test_id", "clause"),
    [
        ("C7-N01", "F4.8.1-F4.8.5"),
        ("C7-R01", "F4.8.3-F4.8.4"),
        ("C7-CREATE-01", "F4.8.1-F4.8.5; F4.9.8"),
    ],
    ids=["C7-N01", "C7-R01", "C7-CREATE-01"],
)
def test_c7_contract(
    v4_driver: V4ConformanceDriver, test_id: str, clause: str
) -> None:
    v4_driver.create_task(test_id=test_id, clause=clause)


def test_c7_x01(v4_driver: V4ConformanceDriver) -> None:
    v4_driver.race_same_create(test_id="C7-X01", clause="F4.8.2-F4.8.5")


def test_at_01(v4_driver: V4ConformanceDriver) -> None:
    v4_driver.race_same_create(test_id="AT-01", clause="F4.8; F4.9.5")
