"""Fixtures for isolated FCoP 4.0 conformance probes."""

from __future__ import annotations

from pathlib import Path

import pytest

from .driver import V4ConformanceDriver


@pytest.fixture
def v4_driver(tmp_path: Path) -> V4ConformanceDriver:
    """Return a driver rooted only in pytest's disposable directory."""
    return V4ConformanceDriver(tmp_path)
