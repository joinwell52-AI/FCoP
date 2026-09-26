"""4.0.5 default MCP contract and pure-Core boundary checks."""
from __future__ import annotations

import asyncio
import json
from pathlib import Path

from fcop_mcp.registry import create_server, export_manifest

from fcop import Project

SNAPSHOT = Path(__file__).parents[2] / "test_fcop_mcp" / "snapshots" / "canonical_tools_405.json"


def test_default_tool_contract_matches_manifest_snapshot(tmp_path: Path) -> None:
    manifest = export_manifest()
    expected = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    assert manifest == expected
    server = create_server(tmp_path)
    tools = asyncio.run(server.list_tools())
    assert len(tools) == 25
    assert {tool.name for tool in tools} == {item["name"] for item in manifest}
    for tool in tools:
        entry = next(item for item in manifest if item["name"] == tool.name)
        assert tool.description == entry["description"]
        assert tool.parameters == entry["inputSchema"]
    assert not {"write_task", "fcop_report", "set_project_dir", "fcop_audit"} & {tool.name for tool in tools}


def test_default_workspace_has_no_host_rules_or_profile_precondition(tmp_path: Path) -> None:
    server = create_server(tmp_path)
    result = asyncio.run(server.call_tool("init_workspace", {})).structured_content
    assert result["protocol_version"] == "4.0"
    assert result["profiles"] == []
    assert Project(tmp_path).is_initialized()
    for name in ("AGENTS.md", "CLAUDE.md", ".cursor"):
        assert not (tmp_path / name).exists()
    inspected = asyncio.run(server.call_tool("inspect_workspace", {})).structured_content
    validated = asyncio.run(server.call_tool("validate_workspace", {})).structured_content
    assert inspected["workspace_id"] == result["workspace_id"]
    assert validated["valid"] is True


def test_rule_resources_are_core_backed_without_host_projection(tmp_path: Path) -> None:
    server = create_server(tmp_path)
    asyncio.run(server.call_tool("init_workspace", {}))
    resources = asyncio.run(server.list_resources())
    assert {str(item.uri) for item in resources} == {
        "fcop://rules", "fcop://protocol",
        "fcop://guidance/sequential/en", "fcop://guidance/sequential/zh",
        "fcop://guidance/parallel/en", "fcop://guidance/parallel/zh",
    }
    uri = "fcop://guidance/sequential/en"
    core = Project(tmp_path).rule_distribution(
        action="read_resource", request={"resource_uri": uri}
    )
    mcp = asyncio.run(server.read_resource(uri)).contents[0].content
    assert mcp == core["content"]
    assert not any((tmp_path / name).exists() for name in ("AGENTS.md", "CLAUDE.md", ".cursor"))


def test_base_initialization_does_not_import_profile_or_builtin_team(tmp_path: Path, monkeypatch) -> None:
    import builtins

    original_import = builtins.__import__

    def no_profile(name, *args, **kwargs):
        if name.startswith(("fcop.profiles", "fcop.teams")):
            raise AssertionError(f"Base imported optional Profile: {name}")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", no_profile)
    server = create_server(tmp_path)
    result = asyncio.run(server.call_tool("init_workspace", {})).structured_content
    assert result["profiles"] == []


def test_canonical_manifest_takes_precedence_over_legacy_host_directory(tmp_path: Path) -> None:
    server = create_server(tmp_path)
    asyncio.run(server.call_tool("init_workspace", {}))
    (tmp_path / "docs" / "agents").mkdir(parents=True)
    from fcop.observation import workspace_status

    status = workspace_status(tmp_path)
    assert status["topology"] == "v4"


def test_mcp_create_and_read_have_core_fact_parity(tmp_path: Path) -> None:
    server = create_server(tmp_path)
    workspace = asyncio.run(server.call_tool("init_workspace", {})).structured_content
    request = dict(workspace_id=workspace["workspace_id"], operation_id="op-parity-1",
                   sender="ALPHA", recipient="BETA", subject="Parity", body="Evidence")
    via_mcp = asyncio.run(server.call_tool("create_task", request)).structured_content
    via_core = Project(tmp_path).create_task(**request, priority="P2", references=[])
    assert via_core["existing"] is True
    assert (via_mcp["task_id"], via_mcp["digest"]) == (via_core["task_id"], via_core["digest"])
    read_mcp = asyncio.run(server.call_tool("read_task", {"task_id": via_mcp["task_id"]})).structured_content
    read_core = Project(tmp_path).read_task(task_id=via_mcp["task_id"])
    assert read_mcp == read_core


def test_mcp_round_trip_to_review_and_core_inspection(tmp_path: Path) -> None:
    server = create_server(tmp_path)

    def call(name: str, **request):
        return asyncio.run(server.call_tool(name, request)).structured_content

    workspace = call("init_workspace")
    task = call("create_task", workspace_id=workspace["workspace_id"],
                operation_id="op-roundtrip-1", sender="ALPHA", recipient="BETA",
                subject="Round trip", body="Work")
    claimed = call("claim_task", task_id=task["task_id"], actor="BETA")
    report = call("write_report", workspace_id=workspace["workspace_id"],
                  sender="BETA", recipient="ALPHA", subject_ref=task["task_id"],
                  attempt_id=claimed["attempt_id"], body="Delivered", result="done")
    submitted = call("submit_task", task_id=task["task_id"], actor="BETA",
                     report_ref=report["report_id"])
    assert submitted["to_stage"] == "review"
    inspected = call("inspect_task", task_id=task["task_id"])
    assert inspected["stage"] == "review"
    assert inspected == Project(tmp_path).inspect_state(task_id=task["task_id"])
    assert call("validate_workspace")["valid"] is True


def test_mcp_authorized_round_trip_to_archive(tmp_path: Path) -> None:
    evaluator_calls = []

    def evaluator(*, profile_ref, issuer, proof):
        evaluator_calls.append((profile_ref, issuer, proof))
        return "AUTHORIZED"

    server = create_server(tmp_path, trusted_profiles={"profile:test": evaluator})

    def call(name: str, **request):
        return asyncio.run(server.call_tool(name, request)).structured_content

    workspace = call("init_workspace", profile="profile:test")
    task = call("create_task", workspace_id=workspace["workspace_id"],
                operation_id="op-approved-1", sender="ALPHA", recipient="BETA",
                subject="Authorized round trip", body="Work")
    task_id = task["task_id"]
    attempt = call("claim_task", task_id=task_id, actor="BETA")["attempt_id"]
    report = call("write_report", workspace_id=workspace["workspace_id"], sender="BETA",
                  recipient="ALPHA", subject_ref=task_id, attempt_id=attempt,
                  body="Delivered", result="done")
    report_id = report["report_id"]
    assert call("submit_task", task_id=task_id, actor="BETA", report_ref=report_id)["to_stage"] == "review"
    common = dict(workspace_id=workspace["workspace_id"], sender="ALPHA", recipient="BETA",
                  subject_ref=task_id, attempt_id=attempt, body="Approved",
                  profile_ref="profile:test", issued_at="2026-09-03T00:03:00+08:00",
                  expires_at="2099-01-01T00:00:00+00:00", authorization_scope="single_use",
                  operation_kind="lifecycle_transition",
                  issuer_proof={"scheme": "test-proof", "value": "valid"})
    acceptance = call("write_review", **common, review_kind="acceptance", decision="approved",
                      references=[report_id], transition={"from": "review", "to": "done"})
    review_id = acceptance["review_id"]
    approved = call("approve_task", task_id=task_id, actor="ALPHA", report_ref=report_id,
                    review_ref=review_id, authorization_ref=review_id,
                    profile_ref="profile:test")
    assert approved.get("to_stage") == "done", approved
    archive_review = call("write_review", **common, review_kind="authorization",
                          decision="authorize", references=[review_id],
                          transition={"from": "done", "to": "archive"})
    archived = call("archive_task", task_id=task_id, actor="ALPHA",
                    authorization_ref=archive_review["review_id"], profile_ref="profile:test")
    assert archived.get("to_stage") == "archive", archived
    assert len(evaluator_calls) >= 2


def test_validation_reports_corrupt_protocol_fact_without_repair(tmp_path: Path) -> None:
    server = create_server(tmp_path)
    asyncio.run(server.call_tool("init_workspace", {}))
    corrupt = tmp_path / "fcop" / "reports" / "REPORT-corrupt.md"
    corrupt.write_text("invalid", encoding="utf-8")
    before = corrupt.read_bytes()
    result = asyncio.run(server.call_tool("validate_workspace", {})).structured_content
    assert result["valid"] is False
    assert result["errors"]
    assert corrupt.read_bytes() == before


def test_unknown_operation_is_reported_without_guessing_recovery(tmp_path: Path) -> None:
    server = create_server(tmp_path)
    asyncio.run(server.call_tool("init_workspace", {}))
    unknown = tmp_path / "fcop" / "operations" / "unknown.json"
    unknown.write_text("{}", encoding="utf-8")
    before = unknown.read_bytes()
    observed = asyncio.run(server.call_tool("inspect_workspace", {})).structured_content
    assert observed["consistent"] is False
    assert any(item["state"] == "UNKNOWN" for item in observed["operations"])
    assert unknown.read_bytes() == before


def test_default_server_root_is_immutable_and_offline(tmp_path: Path, monkeypatch) -> None:
    import socket

    original_connect = socket.socket.connect

    def blocked(sock, address):
        if isinstance(address, tuple) and address[0] in {"127.0.0.1", "::1"}:
            return original_connect(sock, address)
        raise AssertionError(f"external network operation attempted: {address}")

    monkeypatch.setattr("socket.socket.connect", blocked)
    server = create_server(tmp_path)
    assert len(asyncio.run(server.list_tools())) == 25
    assert "set_project_dir" not in {tool.name for tool in asyncio.run(server.list_tools())}
