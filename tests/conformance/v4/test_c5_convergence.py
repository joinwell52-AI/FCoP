"""C5 attempts, evidence heads, convergence, and family races."""

from __future__ import annotations

import pytest

from .driver import V4ConformanceDriver


@pytest.mark.parametrize(
    ("test_id", "clause", "action"),
    [
        ("C5-N01", "F4.6.1-F4.6.2", "report"),
        ("C5-N02", "F4.6.5-F4.6.8", "family"),
        ("C5-R01", "F4.3.4; F4.6.2", "report"),
        ("C5-R02", "F4.6.1-F4.6.2", "report"),
        ("C5-R03", "F4.6.6-F4.6.8", "family"),
        ("C5-X01", "F4.6.8; F4.9.5", "family"),
        ("C5-BRANCH-01", "F4.6.5", "family"),
        ("C5-ARCHIVED-01", "F4.6.6-F4.6.8", "family"),
        ("C5-FAMILY-DIGEST-01", "F4.6.6", "family"),
    ],
    ids=[
        "C5-N01", "C5-N02", "C5-R01", "C5-R02", "C5-R03", "C5-X01",
        "C5-BRANCH-01", "C5-ARCHIVED-01", "C5-FAMILY-DIGEST-01",
    ],
)
def test_c5_contract(
    v4_driver: V4ConformanceDriver, test_id: str, clause: str, action: str
) -> None:
    if action == "report":
        v4_driver.write_report(test_id=test_id, clause=clause)
    else:
        v4_driver.require_family(test_id=test_id, clause=clause)


def test_c5_family_race_01(v4_driver: V4ConformanceDriver) -> None:
    v4_driver.parallel_surface_probe(
        "list_branches",
        test_id="C5-FAMILY-RACE-01",
        clause="F4.5.4; F4.9.5",
        expected="family-linearized Root transition versus Branch create",
    )


def test_c5_report_race_01(v4_driver: V4ConformanceDriver) -> None:
    v4_driver.parallel_surface_probe(
        "write_report",
        required_parameters=("attempt_id", "report_kind", "references"),
        test_id="C5-REPORT-RACE-01",
        clause="F4.6.6-F4.6.8; F4.9.5",
        expected="family-linearized REPORT replacement versus convergence",
    )


def test_at_03(v4_driver: V4ConformanceDriver) -> None:
    v4_driver.parallel_surface_probe(
        "write_report",
        required_parameters=("attempt_id", "report_kind", "references"),
        test_id="AT-03",
        clause="F4.6.2-F4.6.3",
        expected="REPORT durable before Branch T3/T4 under synchronized processes",
    )


def test_at_04(v4_driver: V4ConformanceDriver) -> None:
    v4_driver.parallel_surface_probe(
        "write_review",
        required_parameters=("review_kind", "family_digest", "references"),
        test_id="AT-04",
        clause="F4.6.5-F4.6.8",
        expected="one canonical family snapshot for convergence versus Root archive",
    )
