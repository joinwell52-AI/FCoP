"""Real resource calls and in-process Relay frames preserve Project ownership."""

from __future__ import annotations

import asyncio
import inspect
import json
from collections.abc import AsyncIterator, Mapping
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

import pytest
from fastmcp import Client
from fastmcp.exceptions import ResourceError
from fcop_mcp import resources, server

from fcop import Project
from fcop.rules import get_protocol_commentary, get_rules


def facts(root: Path) -> dict[str, bytes]:
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file()}


def workspace(root: Path, version: str) -> None:
    if version == "4.0":
        Project(root).create_workspace(protocol_version="4.0", encoding="fcop-filesystem/4.0", profiles=[])
    else:
        (root / "fcop").mkdir()
        (root / "fcop/fcop.json").write_bytes(b'{"protocol":"fcop","protocol_version":"3.0"}\n')


@pytest.mark.parametrize("version", ["3.0", "4.0"])
@pytest.mark.parametrize("uri", ["fcop://protocol", "fcop://rules", "fcop://team", "fcop://guidance/sequential/en"])
def test_project_direct_and_real_relay_bytes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, version: str, uri: str) -> None:
    from fcop_mcp import relay

    workspace(tmp_path, version)
    before = facts(tmp_path)
    project = Project(tmp_path).rule_distribution(action="read_resource", request={"resource_uri": uri})
    mcp = server.create_server(tmp_path)
    direct = asyncio.run(mcp.read_resource(uri)).contents[0]
    assert isinstance(direct.content, str)
    direct_text = direct.content
    assert direct.mime_type == project["mime_type"]
    if version == "3.0" and uri != "fcop://team":
        expected = get_protocol_commentary() if uri == "fcop://protocol" else get_rules()
        assert direct.content.encode() == expected.encode()
    elif uri == "fcop://protocol":
        obj = project["content"]
        expected = ("# FCoP specification identity\n\n"
                    f"- path: {obj['path']}\n- revision: {obj['revision']}\n- sha256: {obj['sha256']}\n")
        assert direct.content == expected and "\r" not in direct.content
    elif uri == "fcop://rules":
        expected = ("# FCoP rule package Manifest\n\n```json\n" +
                    json.dumps(project["content"], ensure_ascii=False, sort_keys=True, indent=2) + "\n```\n")
        assert direct.content == expected
        assert json.loads(direct.content.split("```json\n", 1)[1].split("```", 1)[0]) == project["content"]
        assert len(project["content"]["artifacts"]) == 18
        assert all(len(record) == 11 for record in project["content"]["artifacts"])
    elif uri == "fcop://team":
        assert json.loads(direct.content) == project["content"]
    else:
        assert direct.content == project["content"]

    async def exercise() -> None:
        async with Client(mcp) as client:
            content = (await client.read_resource(uri))[0]
            assert content.text == direct.content and content.mimeType == direct.mime_type
        inbound: asyncio.Queue[str | None] = asyncio.Queue()
        outbound: asyncio.Queue[dict[str, Any]] = asyncio.Queue()

        class Socket:
            def __aiter__(self) -> Socket:
                return self

            async def __anext__(self) -> str:
                value = await inbound.get()
                if value is None:
                    raise StopAsyncIteration
                return value

            async def send(self, value: str) -> None:
                await outbound.put(json.loads(value))

        @asynccontextmanager
        async def connect(url: str) -> AsyncIterator[Socket]:
            assert url == "wss://explicit.inprocess.invalid"
            yield Socket()

        monkeypatch.setattr(relay, "_connector", lambda: connect)
        runner = asyncio.create_task(relay.run_relay(mcp, "wss://explicit.inprocess.invalid"))

        async def request(message: dict[str, Any]) -> dict[str, Any]:
            await inbound.put(json.dumps({"jsonrpc": "2.0", **message}))
            while True:
                response = await asyncio.wait_for(outbound.get(), 10)
                if response.get("id") == message["id"]:
                    return response

        try:
            init = await request({"id": 1, "method": "initialize", "params": {
                "protocolVersion": "2025-11-25", "capabilities": {},
                "clientInfo": {"name": "wp4c5-memory-relay", "version": "1"}}})
            assert "result" in init
            await inbound.put(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}))
            result = await request({"id": 2, "method": "resources/read", "params": {"uri": uri}})
            content = result["result"]["contents"][0]
            assert content["text"].encode() == direct_text.encode()
            assert content["mimeType"] == direct.mime_type and content["uri"] == uri
        finally:
            await inbound.put(None)
            await asyncio.wait_for(runner, 10)

    asyncio.run(exercise())
    assert facts(tmp_path) == before


def test_adapter_uses_one_project_read_no_source_algorithms(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    workspace(tmp_path, "4.0")
    mcp = server.create_server(tmp_path)
    calls: list[tuple[str, Mapping[str, Any]]] = []
    original = Project.rule_distribution

    def recorded(self: Project, *, action: str, request: Mapping[str, Any]) -> Mapping[str, Any]:
        calls.append((action, request))
        return original(self, action=action, request=request)

    # Spy forwards to the actual version-bound Project implementation.
    monkeypatch.setattr(Project, "rule_distribution", recorded)
    for uri in ("fcop://protocol", "fcop://rules", "fcop://team", "fcop://guidance/parallel/zh"):
        calls.clear()
        assert asyncio.run(mcp.read_resource(uri)).contents[0].content
        assert calls == [("read_resource", {"resource_uri": uri})]
    for fn in (resources._distribution, resources._render):
        source = inspect.getsource(fn)
        for forbidden in ("read_bytes", "read_text", "get_rules", "get_protocol_commentary", "hashlib", "load(", "route("):
            assert forbidden not in source


@pytest.mark.parametrize("raw", [b'{}', b'bad', b'\xff', b'{"protocol_version":"9.0"}',
                                  b'{"protocol_version":"4.0","protocol_version":"3.0"}'])
def test_resource_unknown_version_zero_write(tmp_path: Path, raw: bytes) -> None:
    (tmp_path / "fcop").mkdir()
    (tmp_path / "fcop/fcop.json").write_bytes(raw)
    before = facts(tmp_path)
    mcp = server.create_server(tmp_path)
    for uri in ("fcop://protocol", "fcop://rules", "fcop://team", "fcop://guidance/sequential/en"):
        with pytest.raises(ResourceError):
            asyncio.run(mcp.read_resource(uri))
        assert facts(tmp_path) == before


def test_old_uri_mime_preserved_and_additive_surface(tmp_path: Path) -> None:
    workspace(tmp_path, "4.0")
    mcp = server.create_server(tmp_path)
    static = {str(r.uri): r.mime_type for r in asyncio.run(mcp.list_resources())}
    templates = {r.uri_template: r.mime_type for r in asyncio.run(mcp.list_resource_templates())}
    historical = json.loads((Path(__file__).parent / "snapshots/tool_surface.json").read_bytes())
    for r in historical["resources"]["static"]:
        assert static[r["uri"]] == r["mime_type"]
    for r in historical["resources"]["templates"]:
        assert templates[r["uri_template"]] == r["mime_type"]
    assert len(asyncio.run(mcp.list_tools())) == 46
    assert len(static) == 12 and static["fcop://team"] == "application/json"
    assert len(templates) == 4 and templates["fcop://guidance/{assembly}/{language}"] == "text/markdown"


@pytest.mark.parametrize("suffix", ["?network=true", "?profile_evaluator=AUTHORIZED", "?deploy=true", "?language=en&language=zh", "#adopt"])
def test_mcp_template_cannot_discard_unaccepted_fields(tmp_path: Path, suffix: str) -> None:
    workspace(tmp_path, "4.0")
    mcp = server.create_server(tmp_path)
    before = facts(tmp_path)
    with pytest.raises(ResourceError, match="RULE_SELECTION_INVALID"):
        asyncio.run(mcp.read_resource("fcop://guidance/sequential/en" + suffix))
    assert facts(tmp_path) == before


@pytest.mark.parametrize("field", ["deploy", "adoption_receipt_ref", "profile_evaluator", "network"])
def test_mcp_resource_rpc_extra_fields_rejected(tmp_path: Path, field: str) -> None:
    from mcp import types
    from mcp.shared.exceptions import McpError

    workspace(tmp_path, "4.0")
    mcp = server.create_server(tmp_path)
    before = facts(tmp_path)

    async def exercise() -> None:
        async with Client(mcp) as client:
            params = types.ReadResourceRequestParams.model_validate({"uri": "fcop://guidance/sequential/en", field: True})
            request = types.ClientRequest(types.ReadResourceRequest(params=params))
            with pytest.raises(McpError, match="RULE_SELECTION_INVALID"):
                await client.session.send_request(request, types.ReadResourceResult)

    asyncio.run(exercise())
    assert facts(tmp_path) == before
