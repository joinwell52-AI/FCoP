"""Test fixtures for the ``fcop-mcp`` contract + smoke tests.

These fixtures keep the ``fcop-mcp`` test suite isolated from a
developer's real FCoP projects. Every test runs inside an ephemeral
``tmp_path`` directory and the ``FCOP_PROJECT_DIR`` / legacy
``CODEFLOW_PROJECT_DIR`` env vars are scrubbed before the fixture
body runs so project resolution can't accidentally escape the sandbox.

The ``mcp_server`` fixture is session-scoped because ``FastMCP``
instances are expensive to construct and tool handlers are themselves
stateless — all mutable state lives in the target project directory.
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from pathlib import Path

import pytest

# ``--snapshot-update`` is registered in the repo-root ``tests/conftest.py``
# so this package does not redefine it (pytest refuses duplicate options).


@pytest.fixture
def clean_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Scrub every env var that fcop-mcp's project resolver consults.

    Prevents a developer's shell from leaking into the test run.
    """
    for var in (
        "FCOP_PROJECT_DIR",
        "CODEFLOW_PROJECT_DIR",
        "FCOP_ROOM_KEY",
        "FCOP_RELAY_WS_URL",
    ):
        monkeypatch.delenv(var, raising=False)


@pytest.fixture
def reset_session_project() -> Iterator[None]:
    """Reset the per-session pinned project between tests.

    ``set_project_dir`` stores the choice in module-level state
    (``_SESSION_PROJECT_PATH``). Without this fixture, the first test
    that pins a path would leak into every subsequent test.

    The 0.7.1 ``_ROLE_LOCK`` (per-MCP-process role lock from
    ISSUE-20260427-004) lives in the same module — clear it here too
    so a write_task in one test doesn't accidentally lock the role
    for the next test's write_task.
    """
    from fcop_mcp import server as srv

    with srv._STATE_LOCK:
        prev_path = srv._SESSION_PROJECT_PATH
        prev_source = srv._SESSION_PROJECT_SOURCE
        prev_role_lock = dict(srv._ROLE_LOCK)
        srv._SESSION_PROJECT_PATH = None
        srv._SESSION_PROJECT_SOURCE = "uninitialized"
        srv._ROLE_LOCK.clear()
    try:
        yield
    finally:
        with srv._STATE_LOCK:
            srv._SESSION_PROJECT_PATH = prev_path
            srv._SESSION_PROJECT_SOURCE = prev_source
            srv._ROLE_LOCK.clear()
            srv._ROLE_LOCK.update(prev_role_lock)


@pytest.fixture
def project_dir(tmp_path: Path, clean_env: None, reset_session_project: None) -> Path:
    """An empty temp dir ready to be initialized as an FCoP project."""
    return tmp_path


@pytest.fixture
def initialized_project(project_dir: Path) -> Path:
    """A temp dir that has already run ``init_project`` for ``dev-team``."""
    import asyncio

    from fcop_mcp.server import mcp

    async def _init() -> None:
        await mcp.call_tool("set_project_dir", {"path": str(project_dir)})
        await mcp.call_tool("init_project", {"team": "dev-team", "lang": "zh"})

    asyncio.run(_init())
    return project_dir


@pytest.fixture(scope="session")
def mcp_server() -> object:
    """Return the shared FastMCP instance so tests can list & dispatch."""
    os.environ.pop("FCOP_PROJECT_DIR", None)
    os.environ.pop("CODEFLOW_PROJECT_DIR", None)
    from fcop_mcp.server import mcp

    return mcp
