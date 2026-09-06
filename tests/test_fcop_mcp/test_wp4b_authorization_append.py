"""Real MCP transport exercises the public validated authorization append path."""

from __future__ import annotations

import asyncio
from importlib import import_module
from pathlib import Path
from typing import Any

import pytest
from fastmcp import Client
from fcop_mcp.server import create_server


@pytest.mark.parametrize("verdict", ["AUTHORIZED", "DENIED", "UNKNOWN", "EMPTY", "REJECT"])
def test_mcp_validated_append(tmp_path: Path, verdict: str, monkeypatch: pytest.MonkeyPatch) -> None:
    helpers = import_module("tests.test_fcop.test_v4_authorization_append")
    app, request, move = helpers.fixture(tmp_path)
    calls: list[dict[str, Any]] = []
    def evaluator(**fields: Any) -> str:
        calls.append(fields)
        return verdict
    registry = {} if verdict == "EMPTY" else {request["profile_ref"]: evaluator}
    mcp = create_server(tmp_path, trusted_profiles=registry)
    if verdict == "REJECT":
        request["decision"] = "reject"
    # Spy at the production internal method reached by public Project binding;
    # do not substitute evaluator decisions or manufacture a successful result.
    creation = import_module("fcop.v4.creation")
    original = creation._Creation.mark_human_approved
    invocations: list[Any] = []
    def record(self: Any, **kwargs: Any) -> Any:
        invocations.append(kwargs)
        return original(self, **kwargs)
    monkeypatch.setattr(creation._Creation, "mark_human_approved", record)
    before = helpers.files(tmp_path)
    async def run() -> Any:
        async with Client(mcp) as client:
            return await client.call_tool("mark_human_approved", request, raise_on_error=False)
    result = asyncio.run(run())
    assert len(invocations) == 1
    assert len(calls) == (0 if verdict in {"EMPTY", "REJECT"} else 1)
    if verdict == "AUTHORIZED":
        assert not result.is_error
        after = helpers.files(tmp_path)
        assert len(after) == len(before) + 1
        assert all(after[k] == v for k, v in before.items())
        review = app.project.inspect_state(envelope_path=Path(result.structured_content["path"]).relative_to(tmp_path).as_posix())
        assert review["review_kind"] == "authorization"
        assert review["decision"] == "authorize"
        assert app.project.inspect_state(task_id=move["task_id"])["stage"] == "done"
    else:
        assert result.is_error
        assert result.structured_content["code"] == (
            "AUTHORIZATION_PROFILE_UNAVAILABLE" if verdict == "EMPTY" else "AUTHORIZATION_INVALID"
        )
        assert helpers.files(tmp_path) == before
