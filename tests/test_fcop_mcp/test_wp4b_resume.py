"""WP4B.0/.1 production-entry contracts; independent of frozen Conformance."""

from __future__ import annotations

import asyncio
import json
from importlib import import_module
from pathlib import Path
from typing import Any

import pytest
from fastmcp.exceptions import ResourceError
from fcop_mcp import server

ROOT = Path(__file__).resolve().parents[2]


def test_wp4b_surface_adds_only_reopen() -> None:
    historical = json.loads(
        (ROOT / "tests/test_fcop_mcp/snapshots/tool_surface.json").read_text(encoding="utf-8")
    )
    names = {row["name"] for row in historical["tools"]}
    observed = {tool.name for tool in asyncio.run(server.mcp.list_tools())}
    assert len(names) == 45
    assert observed == names | {"reopen_task"}
    assert len(observed) == 46
    assert "close_issue" not in observed
    assert "transition" not in observed


def test_wp4b_reopen_exact_six_parameters() -> None:
    tools = {tool.name: tool for tool in asyncio.run(server.mcp.list_tools())}
    schema = tools["reopen_task"].parameters
    assert set(schema["properties"]) == {
        "task_id", "review_ref", "authorization_ref", "profile_ref", "actor", "lang",
    }
    assert set(schema["required"]) == {
        "task_id", "review_ref", "authorization_ref", "profile_ref", "actor",
    }
    assert all(value["type"] == "string" for value in schema["properties"].values())


@pytest.mark.parametrize(
    "uri",
    ["fcop://teams/dev-team", "fcop://teams/dev-team/PM", "fcop://teams/dev-team/PM/en"],
)
def test_wp4b_profile_reads_have_no_workspace_effect(tmp_path: Path, uri: str) -> None:
    # Server construction is the trusted initialization boundary, not a tool argument.
    mcp = server.create_server(tmp_path, trusted_profiles={})
    before = sorted(tmp_path.rglob("*"))
    result = asyncio.run(mcp.read_resource(uri))
    assert result.contents and result.contents[0].content
    assert sorted(tmp_path.rglob("*")) == before
    assert not (tmp_path / "fcop/fcop.json").exists()


@pytest.mark.parametrize(
    "uri",
    ["fcop://teams/unknown-team", "fcop://teams/dev-team/UNKNOWN", "fcop://teams/../PM"],
)
def test_wp4b_profile_unknown_or_path_fails(tmp_path: Path, uri: str) -> None:
    mcp = server.create_server(tmp_path, trusted_profiles={})
    with pytest.raises(ResourceError):
        asyncio.run(mcp.read_resource(uri))
    assert not list(tmp_path.rglob("*"))


def test_wp4b_relay_direct_dependency_is_optional() -> None:
    # Python 3.10 has no tomllib; inspect the simple declarative dependency block.
    text = (ROOT / "mcp/pyproject.toml").read_text(encoding="utf-8")
    base = text.split("\ndependencies = [", 1)[1].split("]", 1)[0]
    extras = text.split("[project.optional-dependencies]", 1)[1]
    assert "websockets" not in base
    assert "relay = [" in extras
    assert "websockets" in extras.split("relay = [", 1)[1].split("]", 1)[0]


def _reopen_fixture(root: Path) -> tuple[Any, dict[str, Any], Any, Any, Any]:
    # Exercise the shipped untyped example as an integration fixture, not as
    # part of the MCP package's strict static source set.
    example = import_module("examples.v4.application")
    app = example.Application(root)
    task = app.task("MCP T6 work")
    report = app.complete(task)
    attempt = app.project.inspect_state(task_id=task)["current_attempt_id"]
    review = app.review(task, "reopen", "approved", attempt_id=attempt)
    authorization = app.authorization(task, "done", "active", refs=[review])
    request = dict(task_id=task, review_ref=review, authorization_ref=authorization,
                   profile_ref=example.PROFILE, actor="ME")
    return app, request, attempt, report, example.evaluator


def _invoke(mcp: Any, name: str, args: dict[str, Any]) -> Any:
    from fastmcp import Client

    async def call() -> Any:
        async with Client(mcp) as client:
            return await client.call_tool(name, args, raise_on_error=False)

    return asyncio.run(call())


def _files(root: Path) -> dict[str, bytes]:
    return {p.relative_to(root).as_posix(): p.read_bytes()
            for p in root.rglob("*") if p.is_file()}


def test_wp4b_t6_real_commit_and_exact_retry(tmp_path: Path) -> None:
    app, args, old_attempt, report, evaluator = _reopen_fixture(tmp_path)
    mcp = server.create_server(tmp_path, trusted_profiles={args["profile_ref"]: evaluator})
    result = _invoke(mcp, "reopen_task", args)
    assert not result.is_error, result
    state = app.project.inspect_state(task_id=args["task_id"])
    assert state["stage"] == "active"
    assert state["current_attempt_id"] != old_attempt
    assert state["last_transition"]["tool"] == "reopen_task"
    assert state["last_transition"]["authorization_ref"] == args["authorization_ref"]
    before = _files(tmp_path)
    retry = _invoke(mcp, "reopen_task", {**args, "lang": "en"})
    assert not retry.is_error, retry
    assert retry.structured_content["existing"] is True
    assert _files(tmp_path) == before
    from fcop.errors import V4ProtocolError

    with pytest.raises(V4ProtocolError) as caught:
        app.move(args["task_id"], "active", "review", "submit_task", report_ref=report)
    assert caught.value.code == "ATTEMPT_MISMATCH"
    assert _files(tmp_path) == before


@pytest.mark.parametrize("verdict", ["EMPTY", "DENIED", "UNKNOWN"])
def test_wp4b_t6_trusted_profile_denials_are_structured(tmp_path: Path, verdict: str) -> None:
    app, args, attempt, _, _ = _reopen_fixture(tmp_path)
    registry = {} if verdict == "EMPTY" else {args["profile_ref"]: lambda **_: verdict}
    mcp = server.create_server(tmp_path, trusted_profiles=registry)
    # Neither reading the role document nor an ADMIN actor creates authority.
    asyncio.run(mcp.read_resource("fcop://teams/dev-team/PM"))
    before = _files(tmp_path)
    result = _invoke(mcp, "reopen_task", {**args, "actor": "ADMIN"})
    assert result.is_error
    assert result.structured_content["code"] == (
        "AUTHORIZATION_PROFILE_UNAVAILABLE" if verdict == "EMPTY" else "AUTHORIZATION_INVALID"
    )
    assert result.structured_content["operation_ref"]
    assert result.structured_content["subject_ref"] == args["task_id"]
    assert _files(tmp_path) == before
    assert app.project.inspect_state(task_id=args["task_id"])["current_attempt_id"] == attempt


@pytest.mark.parametrize("field", ["from_stage", "to_stage", "tool", "operation_id",
                                   "internal_operation_id", "attempt_id", "report_ref",
                                   "family_digest", "profile_evaluator"])
def test_wp4b_t6_rejects_unapproved_inputs(tmp_path: Path, field: str) -> None:
    _, args, _, _, evaluator = _reopen_fixture(tmp_path)
    mcp = server.create_server(tmp_path, trusted_profiles={args["profile_ref"]: evaluator})
    before = _files(tmp_path)
    result = _invoke(mcp, "reopen_task", {**args, field: "caller-controlled"})
    assert result.is_error
    assert _files(tmp_path) == before
