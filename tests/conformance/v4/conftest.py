"""Fixtures for isolated FCoP 4.0 behavioral conformance tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from .driver import V4ConformanceDriver
from .fixtures import WorkspaceFixture


@pytest.fixture
def workspace(tmp_path: Path) -> WorkspaceFixture:
    return WorkspaceFixture(tmp_path).create()


@pytest.fixture
def empty_workspace(tmp_path: Path) -> WorkspaceFixture:
    return WorkspaceFixture(tmp_path)


@pytest.fixture
def v4_driver(workspace: WorkspaceFixture) -> V4ConformanceDriver:
    return V4ConformanceDriver(workspace.root)
