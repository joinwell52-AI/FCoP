"""Compare independent declarations, catalog, CLI and actual stdio registration."""
from __future__ import annotations

import asyncio
import io
import json
import os
import subprocess
import sys
from pathlib import Path

from fcop_mcp.catalog import get_tool_catalog
from fcop_mcp.disposition import TOOLS
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from fcop.cli._main import main


def test_catalog_does_not_import_runtime_and_returns_fresh_rows(tmp_path: Path) -> None:
    script = (
        "import sys; from fcop_mcp.catalog import get_tool_catalog; "
        "get_tool_catalog(); assert 'fastmcp' not in sys.modules; assert 'fcop_mcp.server' not in sys.modules"
    )
    subprocess.run([sys.executable, "-I", "-c", script], cwd=tmp_path, check=True, timeout=60)
    first = get_tool_catalog()
    first[0]["name"] = "tampered"
    assert "tampered" not in {row["name"] for row in get_tool_catalog()}
    assert get_tool_catalog("create_branch") == [{"name": "create_branch", "disposition": TOOLS["create_branch"]}]


def test_catalog_cli_stdio_registry_equality(tmp_path: Path) -> None:
    output = io.StringIO()
    assert main(["tools", "--json"], stdout=output) == 0
    cli = json.loads(output.getvalue())["data"]
    authoritative = set(TOOLS)
    assert {r["name"] for r in cli["tools"]} == authoritative
    assert {r["name"] for r in get_tool_catalog()} == authoritative
    assert cli["total"] == len(authoritative)
    environment = dict(os.environ)
    environment.pop("PYTHONPATH", None)

    async def verify() -> None:
        params = StdioServerParameters(command=sys.executable, args=["-I", "-m", "fcop_mcp"],
                                        cwd=str(tmp_path), env=environment)
        async with stdio_client(params) as streams, ClientSession(*streams) as session:
            await session.initialize()
            assert {t.name for t in (await session.list_tools()).tools} == authoritative

    asyncio.run(verify())
