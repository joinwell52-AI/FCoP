"""Shared pytest fixtures for the fcop test suite.

Keep this file tiny on purpose: the tests in ``tests/test_fcop/`` are
primarily unit tests against pure functions in ``fcop.core.*``. Fixtures
that build on-disk FCoP projects live closer to the integration tests
once those exist.
"""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture()
def tmp_project(tmp_path: Path) -> Path:
    """An empty directory that looks like a fresh project root.

    Tests that need a ``Project(path=...)`` should call the ``Project``
    constructor on this path. Nothing is pre-created inside it; each
    test decides what it needs.
    """
    return tmp_path
