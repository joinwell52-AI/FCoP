"""Real stdio 49-tool family flow with caller-supplied semantic decisions."""

from __future__ import annotations

import asyncio
import importlib.util
import json
import os
import sys
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from fcop import Project
from tests.conformance.v4.fixtures import snapshot_tree


def test_all_46_existing_tool_signatures_unchanged() -> None:
    from tests.test_fcop_mcp.test_tool_surface import _collect_surface

    frozen = json.loads(
        (Path(__file__).parent / "snapshots/tool_surface_4_0_0.json").read_text(encoding="utf-8")
    )
    current = _collect_surface()
    assert isinstance(current["tools"], list)
    old = {row["name"]: row for row in frozen["tools"]}
    new = {row["name"]: row for row in current["tools"]}
    assert len(old) == 46 and len(new) == 49
    assert {name: new[name] for name in old} == old
    assert new.keys() - old.keys() == {"create_branch", "inspect_family", "merge_branches"}
    assert current["resources"] == frozen["resources"]


def test_real_stdio_branch_merge_and_restart(tmp_path: Path) -> None:
    helper_path = Path(__file__).resolve().parents[1] / "stable/third-party/python-only/app.py"
    spec = importlib.util.spec_from_file_location("branch_demo", helper_path)
    assert spec and spec.loader
    demo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(demo)
    workspace = Project(tmp_path).create_workspace(protocol_version="4.0", profiles=[demo.PROFILE])
    app = demo.Application(tmp_path, workspace["workspace_id"])
    root_id = app.start("root")
    launcher = (
        "from pathlib import Path\n"
        "from fcop_mcp.adapter import create_server\n"
        f"create_server(Path({str(tmp_path)!r})).run(transport='stdio')\n"
    )
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    parameters = StdioServerParameters(command=sys.executable, args=["-I", "-c", launcher], env=env)

    async def flow() -> tuple[dict[str, Any], str]:
        async with stdio_client(parameters) as streams, ClientSession(*streams) as session:
            await session.initialize()
            tools = (await session.list_tools()).tools
            assert len(tools) == 49
            assert {"create_branch", "inspect_family", "merge_branches", "reopen_task"} <= {
                t.name for t in tools
            }
            assert len((await session.list_resources()).resources) == 12
            assert len((await session.list_resource_templates()).resourceTemplates) == 4
            requests = [
                dict(
                    root_task_id=root_id,
                    workspace_id=workspace["workspace_id"],
                    operation_id=f"branch-{i}",
                    sender="ME",
                    recipient="ME",
                    subject=f"Branch {i}",
                    body="Parallel work",
                )
                for i in range(2)
            ]
            results = await asyncio.gather(
                *(session.call_tool("create_branch", req) for req in requests)
            )
            branches = []
            for result in results:
                assert not result.isError and result.structuredContent
                assert result.structuredContent["family_digest"] is None
                assert result.structuredContent["merge_ready"] is False
                branches.append(result.structuredContent["branch_task_id"])
            assert len(set(branches)) == 2
            retried = await session.call_tool("create_branch", requests[0])
            assert retried.structuredContent is not None
            assert not retried.isError and retried.structuredContent["existing"]
            heads = {}
            for task_id in branches:
                app.move(task_id, "inbox", "active", "claim_task")
                heads[task_id] = app.complete(task_id)
            app.complete(root_id)
            before = snapshot_tree(tmp_path)
            inspected = await session.call_tool("inspect_family", {"root_task_id": root_id})
            assert inspected.structuredContent is not None
            assert not inspected.isError and inspected.structuredContent["merge_ready"]
            assert snapshot_tree(tmp_path) == before
            family = inspected.structuredContent
            req = dict(
                root_task_id=root_id,
                workspace_id=workspace["workspace_id"],
                expected_family_digest=family["family_digest"],
                branch_report_heads=heads,
                conclusion="Combine both branches",
                conflict_resolution="No unresolved conflict",
                operation_id="stdio-merge",
                sender="ME",
                recipient="ME",
            )
            bad = await session.call_tool(
                "merge_branches", {**req, "expected_family_digest": "0" * 64}
            )
            assert bad.structuredContent is not None
            assert bad.isError and bad.structuredContent["code"] == "FAMILY_CONVERGENCE_MISMATCH"
            assert snapshot_tree(tmp_path) == before
            result = await session.call_tool("merge_branches", req)
            assert result.structuredContent is not None
            assert not result.isError and not result.structuredContent["existing"]
            review_id = result.structuredContent["review_id"]
            assert app.p.inspect_state(task_id=root_id)["stage"] == "done"
            return req, review_id

    req, review_id = asyncio.run(flow())
    before = snapshot_tree(tmp_path)

    async def restarted() -> None:
        async with stdio_client(parameters) as streams, ClientSession(*streams) as session:
            await session.initialize()
            replay = await session.call_tool("merge_branches", req)
            assert replay.structuredContent is not None
            assert not replay.isError and replay.structuredContent["existing"]
            assert replay.structuredContent["review_id"] == review_id
            conflict = await session.call_tool("merge_branches", {**req, "conclusion": "Different"})
            assert conflict.structuredContent is not None
            assert (
                conflict.isError and conflict.structuredContent["code"] == "OPERATION_ID_CONFLICT"
            )

    asyncio.run(restarted())
    assert snapshot_tree(tmp_path) == before
