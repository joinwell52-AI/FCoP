"""Production MCP integration: version boundaries, REPORT graphs and transport."""

from __future__ import annotations

import asyncio
import hashlib
import json
import subprocess
from importlib import import_module
from pathlib import Path
from typing import Any
from uuid import uuid4

import pytest
import yaml
from fastmcp import Client
from fastmcp.exceptions import ResourceError
from fcop_mcp import server
from fcop_mcp.disposition import RESOURCES, TEMPLATES, TOOLS
from fcop_mcp.routing import WorkspaceRouter

from fcop import Project


def call(mcp: Any, name: str, args: dict[str, Any]) -> Any:
    async def invoke() -> Any:
        async with Client(mcp) as client:
            return await client.call_tool(name, args, raise_on_error=False)
    return asyncio.run(invoke())


def facts(root: Path) -> dict[str, bytes]:
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file()}


def app_at(root: Path) -> Any:
    return import_module("examples.v4.application").Application(root)


def trusted(root: Path) -> Any:
    example = import_module("examples.v4.application")
    return server.create_server(root, trusted_profiles={example.PROFILE: example.evaluator})


@pytest.mark.parametrize("shape,code", [("unique", None), ("multiple", "REPORT_HEAD_AMBIGUOUS"),
                                         ("cycle", "REPORT_REQUIRED"), ("replaced", None)])
def test_mcp_query_consumers(tmp_path: Path, shape: str, code: str | None) -> None:
    app = app_at(tmp_path)
    task = app.task("MCP REPORT head")
    attempt = app.project.inspect_state(task_id=task)["current_attempt_id"]
    req = dict(workspace_id=app.workspace_id, sender="ME", recipient="ME", subject_ref=task,
               body="Evidence", attempt_id=attempt, result="done")
    first = app.project.write_report(**req, report_kind="final")
    second = None
    if shape != "unique":
        second = app.project.write_report(**req, report_kind="replacement", references=[first["report_id"]])
        path = Path(first["path"] if shape == "cycle" else second["path"])
        if shape != "replaced":
            _, front, body = path.read_text(encoding="utf-8").split("---", 2)
            fields = yaml.safe_load(front)
            fields.update(report_kind="replacement" if shape == "cycle" else "final",
                          references=[second["report_id"]] if shape == "cycle" else [])
            path.write_bytes(("---\n" + yaml.safe_dump(fields) + "---" + body).encode())
    before = facts(tmp_path)
    mcp = trusted(tmp_path)
    for name, args in [("list_reports", dict(task_id=task, attempt_id=attempt, head_only=True)),
                       ("read_report", dict(filename=first["report_id"]))]:
        result = call(mcp, name, args)
        assert result.is_error is (code is not None), result
        if code:
            assert result.structured_content["code"] == code
        else:
            row = result.structured_content["items"][0] if name == "list_reports" else result.structured_content
            assert row["head_ref"] == (second or first)["report_id"]
            assert row["is_head"] is (name == "list_reports" or shape == "unique")
        assert facts(tmp_path) == before


def test_mcp_empty_explicit_head(tmp_path: Path) -> None:
    app = app_at(tmp_path)
    task = app.task("No REPORT")
    result = call(trusted(tmp_path), "list_reports", dict(task_id=task, head_only=True,
                  attempt_id=app.project.inspect_state(task_id=task)["current_attempt_id"]))
    assert result.is_error and result.structured_content["code"] == "REPORT_REQUIRED"


@pytest.mark.parametrize("manifest", [b'{"protocol_version":"9.0"}', b'{}', b'bad', b'\xff',
    b'{"protocol_version":"4.0","protocol_version":"3.0"}',
    b'{"protocol_version":"3.0","protocol_version":"4.0"}'])
def test_unknown_version_zero_write(tmp_path: Path, manifest: bytes) -> None:
    folder = tmp_path / "fcop"
    folder.mkdir()
    (folder / "fcop.json").write_bytes(manifest)
    before = facts(tmp_path)
    result = call(server.create_server(tmp_path), "create_task",
                  dict(sender="ME", recipient="ME", subject="Reject", body="No writes"))
    assert result.is_error
    expected = "UNSUPPORTED_PROTOCOL" if manifest == b'{"protocol_version":"9.0"}' else "UNSUPPORTED_WORKSPACE_VERSION"
    assert result.structured_content["code"] == expected
    assert facts(tmp_path) == before


def test_rebind_version_and_registry_immutable(tmp_path: Path) -> None:
    v3, v4 = tmp_path / "v3", tmp_path / "v4"
    Project(v3).init_solo(role_code="ME")
    app_at(v4)
    router = WorkspaceRouter(v3)
    assert router.route().declared_protocol == "v3"
    assert router.bind(v4).declared_protocol == "v4"
    assert router.bind(v3).declared_protocol == "v3"
    mcp = server.create_server(v3)
    result = call(mcp, "set_project_dir", {"path": str(v4)})
    assert not result.is_error
    assert call(mcp, "finish_task", {"task_id": "TASK-missing"}).structured_content["code"] == "LEGACY_TRANSITION_NOT_ALLOWED"
    result = call(mcp, "set_project_dir", {"path": str(v3)})
    assert not result.is_error
    result = call(mcp, "reopen_task", dict(task_id="TASK-any", review_ref="REVIEW-any",
                  authorization_ref="REVIEW-auth", profile_ref="profile:test", actor="ADMIN"))
    assert result.structured_content["code"] == "UNSUPPORTED_WORKSPACE_VERSION"


@pytest.mark.parametrize("declared", ["v3", "v4"])
def test_all_static_resources_and_disposition(tmp_path: Path, declared: str) -> None:
    if declared == "v3":
        Project(tmp_path).init_solo(role_code="ME")
    else:
        app_at(tmp_path)
    mcp = server.create_server(tmp_path)
    assert {t.name for t in asyncio.run(mcp.list_tools())} == set(TOOLS) | {"create_branch", "inspect_family", "merge_branches"}
    assert {str(r.uri) for r in asyncio.run(mcp.list_resources())} == set(RESOURCES)
    assert {t.uri_template for t in asyncio.run(mcp.list_resource_templates())} == set(TEMPLATES)
    before = facts(tmp_path)
    for uri, policy in RESOURCES.items():
        if declared == "v4" and policy in {"RULES_PENDING_WP4C", "GUIDANCE"}:
            with pytest.raises(ResourceError, match="V4_GUIDANCE_UNAVAILABLE"):
                asyncio.run(mcp.read_resource(uri))
        else:
            result = asyncio.run(mcp.read_resource(uri))
            text = str(result.contents[0].content)
            assert text
            if policy == "VERSIONED_SPEC":
                assert "workspace protocol: " + declared in text
                assert "Source payload SHA-256:" in text
    assert facts(tmp_path) == before


def test_spec_payload_git_parity() -> None:
    from importlib.resources import files

    registry = json.loads(files("fcop_mcp").joinpath("_specs.json").read_text(encoding="utf-8"))
    assert set(registry) == {"v3/en", "v3/zh", "v4/en", "v4/zh"}
    root = Path(__file__).resolve().parents[2]
    for entry in registry.values():
        # The current root spec is unchanged; this also works in CI's shallow checkout.
        source = subprocess.check_output(["git", "show", "HEAD:" + entry["source_path"]], cwd=root)
        assert source == entry["content"].encode("utf-8")
        assert hashlib.sha256(source).hexdigest() == entry["sha256"]


def test_stdio_explicit_no_relay(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import socket

    from fcop_mcp.__main__ import main

    seen: list[str] = []
    def stdio(**kwargs: Any) -> None:
        assert kwargs["show_banner"] is False
        seen.append(kwargs["transport"])
    def network(*args: Any, **kwargs: Any) -> Any:
        raise AssertionError("Base stdio must not connect")
    monkeypatch.setattr(server.mcp, "run", stdio)
    monkeypatch.setattr(socket, "create_connection", network)
    monkeypatch.setenv("FCOP_RELAY_WS_URL", "wss://must-not-be-used.invalid")
    monkeypatch.setenv("FCOP_ROOM_KEY", "must-not-activate")
    assert main([]) == 0 and seen == ["stdio"]


def test_explicit_relay_real_mcp() -> None:
    from fcop_mcp.relay import run_relay
    from websockets.asyncio.server import serve

    async def probe() -> None:
        completed = asyncio.Event()
        async def relay_peer(socket: Any) -> None:
            await socket.send(json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                "params": {"protocolVersion": "2025-11-25", "capabilities": {},
                           "clientInfo": {"name": "wp4b-relay-test", "version": "1"}}}))
            init = json.loads(await socket.recv())
            assert init["id"] == 1 and "result" in init
            await socket.send(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}))
            await socket.send(json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}))
            tools = json.loads(await socket.recv())
            assert len(tools["result"]["tools"]) == 49
            completed.set()
        async with serve(relay_peer, "127.0.0.1", 0) as endpoint:
            port = next(iter(endpoint.sockets)).getsockname()[1]
            await asyncio.wait_for(run_relay(server.mcp, f"ws://127.0.0.1:{port}"), 20)
        assert completed.is_set()
    asyncio.run(probe())


@pytest.mark.parametrize("pair", [("4.0.0", "3.2.5"), ("3.2.5", "4.0.0"), ("bad", "3.2.5")])
def test_package_pair_fail_closed(monkeypatch: pytest.MonkeyPatch, pair: tuple[str, str]) -> None:
    from fcop_mcp import routing

    monkeypatch.setattr(routing, "version", lambda name: pair[0 if name == "fcop" else 1])
    with pytest.raises(RuntimeError, match="MCP_PACKAGE_INCOMPATIBLE"):
        server.create_server("unused")


def test_mcp_entire_lifecycle_and_four_envelopes(tmp_path: Path) -> None:
    from datetime import datetime, timezone

    example = import_module("examples.v4.application")
    mcp = trusted(tmp_path)
    def ok(name: str, **args: Any) -> dict[str, Any]:
        result = call(mcp, name, args)
        assert not result.is_error, (name, result)
        return dict(result.structured_content)

    manifest = ok("init_solo", role_code="ME", protocol_version="4.0", profiles=[example.PROFILE])
    workspace = manifest["workspace_id"]
    request = dict(sender="ME", recipient="ME", subject="All lifecycle edges", body="Work",
                   workspace_id=workspace, operation_id=uuid4().hex)
    created = ok("create_task", **request)
    task = created["task_id"]
    assert ok("write_task", **request)["task_id"] == task
    assert ok("create_task", **request)["existing"] is True
    ok("claim_task", task_id=task, actor="ME")
    project: Any = Project(tmp_path, trusted_profiles={example.PROFILE: example.evaluator})

    def review(kind: str, decision: str, source: str, target: str, refs: list[str]) -> str:
        attempt = project.inspect_state(task_id=task)["current_attempt_id"]
        return str(ok("write_review", reviewer_role="ME", subject_type="task", subject_ref=task,
            decision=decision, body="Evidence", workspace_id=workspace, recipient="ME",
            review_kind=kind, attempt_id=attempt, transition={"from": source, "to": target},
            profile_ref=example.PROFILE, issuer_proof="demo-only", references=refs,
            issued_at=datetime.now(timezone.utc).isoformat(), authorization_scope="single_use",
            operation_kind="lifecycle_transition")["review_id"])

    issue = ok("write_issue", reporter="ME", recipient="ME", summary="Observation", body="Issue",
               severity="medium", subject_ref=task, workspace_id=workspace)
    assert issue["issue_id"].startswith("ISSUE-")
    report = ok("write_report", task_id=task, reporter="ME", recipient="ME", body="Complete",
                workspace_id=workspace, attempt_id=project.inspect_state(task_id=task)["current_attempt_id"])["report_id"]
    before = facts(tmp_path)
    for name in ("finish_task", "archive_to_history", "bulk_archive_to_history", "list_history", "read_history_task"):
        tool = next(t for t in asyncio.run(mcp.list_tools()) if t.name == name)
        args = {key: (task if "task" in key or key == "filename" else "2026-01-01")
                for key in tool.parameters.get("required", [])}
        result = call(mcp, name, args)
        assert result.is_error and result.structured_content["code"] == "LEGACY_TRANSITION_NOT_ALLOWED"
        assert facts(tmp_path) == before
    ok("submit_task", task_id=task, actor="ME", report_ref=report)
    rejection = review("rejection", "rejected", "review", "active", [report])
    previous_attempt = project.inspect_state(task_id=task)["current_attempt_id"]
    ok("reject_task", task_id=task, actor="ME", report_ref=report, review_ref=rejection,
       authorization_ref=rejection, profile_ref=example.PROFILE)
    assert project.inspect_state(task_id=task)["current_attempt_id"] != previous_attempt
    report = ok("write_report", task_id=task, reporter="ME", recipient="ME", body="Revised",
                workspace_id=workspace, attempt_id=project.inspect_state(task_id=task)["current_attempt_id"])["report_id"]
    ok("submit_task", task_id=task, actor="ME", report_ref=report)
    acceptance = review("acceptance", "approved", "review", "done", [report])
    ok("approve_task", task_id=task, actor="ME", report_ref=report, review_ref=acceptance,
       authorization_ref=acceptance, profile_ref=example.PROFILE)
    reopen = review("reopen", "approved", "done", "active", [])
    authorization = review("authorization", "authorize", "done", "active", [reopen])
    args = dict(task_id=task, actor="ME", review_ref=reopen,
                authorization_ref=authorization, profile_ref=example.PROFILE)
    ok("reopen_task", **args)
    # Discarded successful response + fresh server models transport response loss.
    before = facts(tmp_path)
    retry = call(trusted(tmp_path), "reopen_task", args)
    assert not retry.is_error and retry.structured_content["existing"] is True
    assert facts(tmp_path) == before
    report = ok("write_report", task_id=task, reporter="ME", recipient="ME", body="Final round",
                workspace_id=workspace, attempt_id=project.inspect_state(task_id=task)["current_attempt_id"])["report_id"]
    ok("submit_task", task_id=task, actor="ME", report_ref=report)
    acceptance = review("acceptance", "approved", "review", "done", [report])
    ok("approve_task", task_id=task, actor="ME", report_ref=report, review_ref=acceptance,
       authorization_ref=acceptance, profile_ref=example.PROFILE)
    archive = review("authorization", "authorize", "done", "archive", [])
    ok("archive_task", task_id=task, actor="ME", authorization_ref=archive, profile_ref=example.PROFILE)
    assert project.inspect_state(task_id=task)["stage"] == "archive"
    tools = {e["tool"] for e in project.read_task(task)["transitions"]}
    assert tools == {"create_task", "claim_task", "submit_task", "reject_task", "approve_task", "reopen_task", "archive_task"}


def test_v4_query_filters_are_real_projections(tmp_path: Path) -> None:
    app = app_at(tmp_path)
    root = app.task("Root")
    branch = app.task("Branch", branch_of=root)
    child = app.project.create_task(workspace_id=app.workspace_id, operation_id="query-child",
        sender="ME", recipient="ME", subject="Child", body="work", parent=root,
        references=[branch])["task_id"]
    first = app.review(root, "assessment", "needs_human")
    second = app.review(root, "assessment", "approved", references=[first])
    before = facts(tmp_path)
    mcp = trusted(tmp_path)
    for filters, expected in [({"branch_of": root}, [branch]), ({"parent": root}, [child]),
        ({"references": [branch]}, [child]),
        ({"stage": "inbox"}, [child]), ({"branch_of": child}, [])]:
        result = call(mcp, "list_tasks", filters)
        assert not result.is_error
        assert sorted(row["task_id"] for row in result.structured_content["items"]) == expected, filters
    result = call(mcp, "list_reviews", dict(review_kind="assessment", subject_ref=root, references=[first]))
    assert not result.is_error
    assert [row["review_id"] for row in result.structured_content["items"]] == [second]
    assert facts(tmp_path) == before
