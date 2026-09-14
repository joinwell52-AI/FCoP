"""Real stdio v4 bootstrap/resources and legacy-only redeployment."""

from __future__ import annotations

import asyncio
import sys

import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from tests.test_fcop.test_403_root_ownership import (
    assert_customer_unchanged,
    customer,
    snapshot,
)


@pytest.mark.parametrize("initializer", ["init_solo", "init_project"])
@pytest.mark.parametrize("occupied", [False, True])
def test_stdio_bootstrap_and_resources_without_host_dependency(tmp_path, initializer, occupied):
    before = customer(tmp_path, occupied)
    launcher = (
        "from fcop_mcp.adapter import create_server; "
        f"create_server({str(tmp_path)!r}).run(transport='stdio')"
    )
    params = StdioServerParameters(command=sys.executable, args=["-I", "-B", "-c", launcher])

    async def run():
        async with stdio_client(params) as streams, ClientSession(*streams) as session:
            await session.initialize()
            assert len((await session.list_tools()).tools) == 49
            assert len((await session.list_resources()).resources) == 12
            assert len((await session.list_resource_templates()).resourceTemplates) == 4
            args = {"protocol_version": "4.0"}
            args.update({"role_code": "ME"} if initializer == "init_solo" else {"team": "dev-team"})
            created = await session.call_tool(initializer, args)
            assert not created.isError and created.structuredContent["workspace_id"]
            stable = snapshot(tmp_path)
            for uri in ("fcop://rules", "fcop://protocol", *(
                f"fcop://guidance/{assembly}/{lang}"
                for assembly in ("sequential", "parallel") for lang in ("en", "zh")
            )):
                result = await session.read_resource(uri)
                assert result.contents and result.contents[0].text
            rejected = await session.call_tool("redeploy_rules", {"force": True, "archive": True})
            assert rejected.isError
            assert rejected.structuredContent["code"] == "toolkit:OPERATION_NOT_IMPLEMENTED"
            assert snapshot(tmp_path) == stable
    asyncio.run(run())
    assert_customer_unchanged(tmp_path, before)
