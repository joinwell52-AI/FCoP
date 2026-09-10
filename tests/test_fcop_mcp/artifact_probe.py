"""Run with an isolated installed wheel interpreter: python -I -B <file> base|relay."""

from __future__ import annotations

import asyncio
import builtins
import json
import os
import sys
import tempfile
from importlib.metadata import requires, version
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import TextResourceContents
from pydantic import AnyUrl


async def base() -> None:
    import fcop_mcp

    import fcop

    for module in (fcop, fcop_mcp):
        assert module.__file__ is not None
        assert Path(module.__file__).resolve().is_relative_to(Path(sys.prefix).resolve())
        print("INSTALLED", module.__file__, flush=True)
    with tempfile.TemporaryDirectory(prefix="wp4b-wheel-") as temporary:
        env = dict(os.environ, FCOP_PROJECT_DIR=temporary,
                   FCOP_RELAY_WS_URL="wss://must-not-activate.invalid")
        env.pop("PYTHONPATH", None)
        launcher = (
            "import sys,runpy,socket\n"
            "def audit(event,args):\n"
            "    if event != 'socket.connect': return\n"
            "    caller=sys._getframe(1).f_code\n"
            "    if caller.co_filename == socket.__file__ and caller.co_name == '_fallback_socketpair': return\n"
            "    raise RuntimeError('Unexpected base network connection')\n"
            "sys.addaudithook(audit)\n"
            "runpy.run_module('fcop_mcp',run_name='__main__')\n"
        )
        parameters = StdioServerParameters(
            command=sys.executable, args=["-I", "-B", "-c", launcher], env=env,
        )
        async with stdio_client(parameters) as streams, ClientSession(*streams) as session:
            await session.initialize()
            assert len((await session.list_tools()).tools) == 46
            assert len((await session.list_resources()).resources) == 12
            assert len((await session.list_resource_templates()).resourceTemplates) == 4
            initialized = await session.call_tool("init_solo", {
                "role_code": "ME", "protocol_version": "4.0", "profiles": [],
            })
            assert not initialized.isError and initialized.structuredContent
            root = Path(temporary)
            before = {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file()}
            for uri in ("fcop://rules", "fcop://protocol", "fcop://team", "fcop://guidance/sequential/en", "fcop://guidance/parallel/zh"):
                semantic = fcop.Project(root).rule_distribution(action="read_resource", request={"resource_uri": uri})
                resource = (await session.read_resource(AnyUrl(uri))).contents[0]
                assert resource.mimeType == semantic["mime_type"]
                assert isinstance(resource, TextResourceContents)
                text = resource.text
                if uri == "fcop://rules":
                    assert json.loads(text.split("```json\n", 1)[1].split("```", 1)[0]) == semantic["content"]
                elif uri == "fcop://protocol":
                    assert all(f"- {key}: {semantic['content'][key]}\n" in text for key in ("path", "revision", "sha256"))
                elif uri == "fcop://team":
                    assert json.loads(text) == semantic["content"]
                else:
                    assert text == semantic["content"]
            assert {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file()} == before
            request = dict(workspace_id=initialized.structuredContent["workspace_id"],
                           operation_id="installed-wheel-request", sender="ME", recipient="ME",
                           subject="Installed wheel smoke", body="Real stdio operation")
            first = await session.call_tool("create_task", request)
            assert not first.isError and first.structuredContent
            second = await session.call_tool("create_task", request)
            assert not second.isError and second.structuredContent
            assert second.structuredContent["existing"] is True
            assert second.structuredContent["task_id"] == first.structuredContent["task_id"]
            spec = await session.read_resource(AnyUrl("fcop://spec/en"))
            assert "workspace protocol: v4" in str(spec.contents)
            rejected = await session.call_tool("finish_task", {
                "task_id": first.structuredContent["task_id"],
            })
            assert rejected.isError and rejected.structuredContent
            assert rejected.structuredContent["code"] == "LEGACY_TRANSITION_NOT_ALLOWED"
    print("REAL_STDIO: 46/12/4; create/retry/spec/structured-error PASS", flush=True)
    print("WP4C5_PACKAGED_RESOURCE_PROJECT_STDIO_PARITY_ZERO_WRITE: 5/5", flush=True)
    print("RESOLVED", {name: version(name) for name in ("fcop", "fcop-mcp", "fastmcp", "mcp", "websockets")})
    print("DIRECT_REQUIREMENTS", requires("fcop-mcp"))


async def relay() -> None:
    from fcop_mcp.relay import run_relay
    from fcop_mcp.server import mcp
    from websockets.asyncio.server import serve

    completed = asyncio.Event()
    async def peer(socket: Any) -> None:
        await socket.send(json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize",
            "params": {"protocolVersion": "2025-11-25", "capabilities": {},
                       "clientInfo": {"name": "installed-wheel", "version": "1"}}}))
        response = json.loads(await socket.recv())
        assert response["id"] == 1 and "result" in response
        await socket.send(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}))
        await socket.send(json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}))
        assert len(json.loads(await socket.recv())["result"]["tools"]) == 46
        completed.set()
    async with serve(peer, "127.0.0.1", 0) as endpoint:
        port = next(iter(endpoint.sockets)).getsockname()[1]
        await asyncio.wait_for(run_relay(mcp, f"ws://127.0.0.1:{port}"), 30)
    assert completed.is_set()
    print("INSTALLED_RELAY_INITIALIZE_AND_TOOL_LIST: PASS", flush=True)

    # Fault injection only: never uninstall or alter upstream dependencies.
    from fcop_mcp.relay import _connector

    original_import = builtins.__import__
    def unavailable(name: str, *args: Any, **kwargs: Any) -> Any:
        if name.startswith("websockets"):
            raise ImportError("controlled missing Relay dependency")
        return original_import(name, *args, **kwargs)
    builtins.__import__ = unavailable
    try:
        try:
            _connector()
        except RuntimeError as error:
            assert "fcop-mcp[relay]" in str(error)
        else:
            raise AssertionError("Missing Relay dependency must be diagnosed")
    finally:
        builtins.__import__ = original_import
    print("RELAY_MISSING_DEPENDENCY_DIAGNOSTIC: PASS", flush=True)


if __name__ == "__main__":
    asyncio.run(base() if sys.argv[1] == "base" else relay())
