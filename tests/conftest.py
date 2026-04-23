"""Shared pytest fixtures for the fcop test suite.

Keep this file tiny on purpose: the tests in ``tests/test_fcop/`` are
primarily unit tests against pure functions in ``fcop.core.*``. Fixtures
that build on-disk FCoP projects live closer to the integration tests
once those exist.
"""

from __future__ import annotations

from pathlib import Path

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register custom CLI flags used by the test suite.

    ``--snapshot-update`` is consumed by
    :mod:`tests.test_fcop.test_public_surface` to regenerate the stored
    snapshot of the library's public API surface. See
    adr/ADR-0003-stability-charter.md for policy.
    """
    parser.addoption(
        "--snapshot-update",
        action="store_true",
        default=False,
        help="Regenerate API-surface snapshots instead of asserting against them.",
    )


@pytest.fixture()
def tmp_project(tmp_path: Path) -> Path:
    """An empty directory that looks like a fresh project root.

    Tests that need a ``Project(path=...)`` should call the ``Project``
    constructor on this path. Nothing is pre-created inside it; each
    test decides what it needs.
    """
    return tmp_path
