"""C3 exact lifecycle and gate behavior probes."""

from __future__ import annotations

import pytest

from .driver import V4ConformanceDriver, V4_EDGES, actual_v3_edges


def test_c3_n01(v4_driver: V4ConformanceDriver) -> None:
    assert actual_v3_edges() == V4_EDGES, "[C3-N01] F4.4.1-F4.4.3 exact seven-edge table"


def test_c3_n02(v4_driver: V4ConformanceDriver) -> None:
    v4_driver.transition("done", "active", test_id="C3-N02", clause="F4.4.2; F4.6.1")


def test_c3_r01(v4_driver: V4ConformanceDriver) -> None:
    v4_driver.transition(
        "inbox", "archive", test_id="C3-R01", clause="F4.4.2-F4.4.3", should_exist=False
    )


def test_c3_r02(v4_driver: V4ConformanceDriver) -> None:
    v4_driver.transition(
        "active", "done", test_id="C3-R02", clause="F4.4.4", should_exist=False
    )


def test_c3_r03(v4_driver: V4ConformanceDriver) -> None:
    v4_driver.inspect_state(test_id="C3-R03", clause="F4.4.6; F4.11.2")


def test_c3_x01(v4_driver: V4ConformanceDriver) -> None:
    v4_driver.inject_fault(test_id="C3-X01", clause="F4.4.6; F4.9.4")


def test_c3_gate_01(v4_driver: V4ConformanceDriver) -> None:
    assert actual_v3_edges() == V4_EDGES, "[C3-GATE-01] F4.4.2/F4.4.7 T1-T7 gate matrix"
