"""Explicit foreground WebSocket transport for the same MCP server.

Frames contain standard MCP JSON-RPC messages. No room protocol, evaluator,
workspace discovery, auto-connect or alternate business dispatcher is added.
"""

from __future__ import annotations

import json
from typing import Any
from urllib.parse import urlparse

import anyio
from fastmcp import FastMCP
from mcp.shared.message import SessionMessage
from mcp.types import JSONRPCMessage


def _connector() -> Any:
    try:
        from websockets.asyncio.client import connect
    except ImportError as exc:
        raise RuntimeError("Explicit Relay requires: pip install 'fcop-mcp[relay]'") from exc
    return connect


async def run_relay(mcp: FastMCP, url: str) -> None:
    """Run only when explicitly requested; endpoint never comes from workspace data."""
    endpoint = urlparse(url)
    if endpoint.scheme != "wss" and not (
        endpoint.scheme == "ws" and endpoint.hostname in {"localhost", "127.0.0.1", "::1"}
    ):
        raise ValueError("Relay requires wss://, or ws:// on loopback for local testing")
    connect = _connector()
    incoming_send, incoming_read = anyio.create_memory_object_stream[SessionMessage | Exception](1)
    outgoing_send, outgoing_read = anyio.create_memory_object_stream[SessionMessage](1)
    async with connect(url) as socket, anyio.create_task_group() as group:
        async def receive() -> None:
            try:
                async for raw in socket:
                    message = JSONRPCMessage.model_validate(json.loads(raw))
                    await incoming_send.send(SessionMessage(message))
            finally:
                await incoming_send.aclose()

        async def send() -> None:
            async with outgoing_read:
                async for message in outgoing_read:
                    await socket.send(message.message.model_dump_json(by_alias=True, exclude_none=True))

        group.start_soon(receive)
        group.start_soon(send)
        try:
            async with mcp._lifespan_manager():
                await mcp._mcp_server.run(
                    incoming_read, outgoing_send,
                    mcp._mcp_server.create_initialization_options(),
                )
        finally:
            group.cancel_scope.cancel()
