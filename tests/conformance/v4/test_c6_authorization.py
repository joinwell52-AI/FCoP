"""C6 durable authorization and trust-boundary behavior probes."""

from __future__ import annotations

import pytest

from .driver import V4ConformanceDriver


@pytest.mark.parametrize(
    ("test_id", "clause"),
    [
        ("C6-N01", "F4.7.1-F4.7.5"),
        ("C6-R01", "F4.7.3-F4.7.5"),
        ("C6-R02", "F4.7.3"),
        ("C6-X01", "F4.7.3; F4.9.11"),
        ("C6-PROFILE-01", "F4.2.3; F4.7.4; F4.7.7"),
        ("C6-SPOOF-01", "F4.7.4-F4.7.6"),
        ("C6-DIGEST-01", "F4.4.5; F4.7.3; F4.7.5"),
    ],
    ids=[
        "C6-N01", "C6-R01", "C6-R02", "C6-X01", "C6-PROFILE-01",
        "C6-SPOOF-01", "C6-DIGEST-01",
    ],
)
def test_c6_contract(
    v4_driver: V4ConformanceDriver, test_id: str, clause: str
) -> None:
    v4_driver.require_authorization(test_id=test_id, clause=clause)
