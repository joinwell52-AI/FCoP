"""CLI v1 real command/readonly contracts; no MCP-work aliases."""
from __future__ import annotations

import io
import json
import subprocess
import sys
from pathlib import Path

import pytest

from fcop import Project
from fcop.cli._main import main
from tests.conformance.v4.fixtures import snapshot_tree

COMMANDS = ("init", "status", "inspect", "validate", "tools", "doctor", "version", "spec")
OBSERVE = tuple(c for c in COMMANDS if c != "init")


def call(*args):
    out = io.StringIO()
    code = main([*map(str, args), "--json"], stdout=out)
    data = json.loads(out.getvalue())
    assert set(data) == {"schema_version", "command", "status", "data", "errors", "warnings"}
    assert data["schema_version"] == 1
    return code, data


def v4(root):
    project = Project(root)
    workspace = project.create_workspace()
    task = project.create_task(workspace_id=workspace["workspace_id"], operation_id="cli-fixture",
                               sender="ME", recipient="ME", subject="CLI fixture", body="Read only")
    return project, task["task_id"]


@pytest.mark.parametrize("command", (*COMMANDS, "migrate", "migrate-workspace"))
def test_help(command, capsys):
    with pytest.raises(SystemExit) as result:
        main([command, "--help"])
    assert result.value.code == 0
    assert "usage:" in capsys.readouterr().out


def test_exact_top_level_surface(capsys):
    with pytest.raises(SystemExit) as result:
        main(["--help"])
    assert result.value.code == 0
    text = capsys.readouterr().out
    assert "CLI = Setup + Observe + Diagnose" in text
    import argparse

    from fcop.cli._main import _build_parser

    action = next(a for a in _build_parser()._actions if isinstance(a, argparse._SubParsersAction))
    assert set(action.choices) == {*COMMANDS, "migrate", "migrate-workspace"}
    assert main([]) == 1
    captured = capsys.readouterr()
    assert not captured.out and "fcop-mcp" in captured.err


@pytest.mark.parametrize("command", OBSERVE)
@pytest.mark.parametrize("kind", ["empty", "v3", "v4", "invalid"])
@pytest.mark.parametrize("json_output", [False, True])
def test_readonly_matrix(tmp_path, command, kind, json_output):
    root = tmp_path / "space 中文 root"
    root.mkdir()
    task_id = "TASK-missing"
    if kind == "v4":
        _, task_id = v4(root)
    if kind == "v3":
        Project(root).init_solo(role_code="ME")
    if kind == "invalid":
        (root / "fcop").mkdir()
        (root / "fcop/fcop.json").write_bytes(b'{"version":3,"version":4}')
    args = [command]
    if command in {"status", "inspect", "validate", "doctor"}:
        args += ["--root", str(root)]
    if command == "inspect":
        args += [task_id]
    if json_output:
        args += ["--json"]
    before = snapshot_tree(root)
    output = io.StringIO()
    code = main(args, stdout=output)
    assert snapshot_tree(root) == before
    assert code in {0, 2, 3}  # never an internal crash
    if json_output:
        data = json.loads(output.getvalue())
        assert data["command"] == command
    else:
        assert output.getvalue().startswith(f"FCoP {command}: ")
    if kind == "v4":
        from fcop.cli._observe import _mcp
        assert code == (3 if command == "tools" and not _mcp()["installed"] else 0)
    if kind == "invalid" and command in {"status", "inspect", "validate", "doctor"}:
        assert code == 2
    if kind == "empty" and command in {"inspect", "validate"}:
        assert code == 3


def test_init_core_only_and_existing(tmp_path):
    root = tmp_path / "新 workspace"
    code, result = call("init", "--root", root)
    assert code == 0 and result["data"]["workspace_id"]
    assert Project(root).is_initialized()
    assert not list(root.rglob("TASK-*.md"))
    assert not (root / "AGENTS.md").exists()
    assert not (root / ".cursor").exists()
    before = snapshot_tree(root)
    assert call("init", "--root", root)[0] == 2
    assert snapshot_tree(root) == before


@pytest.mark.parametrize("raw", [b'{', b'{"protocol_version":"9.9"}', b'\xff',
                                 b'{"version":3,"version":3}'])
def test_invalid_classification_no_write(tmp_path, raw):
    (tmp_path / "fcop").mkdir()
    (tmp_path / "fcop/fcop.json").write_bytes(raw)
    before = snapshot_tree(tmp_path)
    for command in ("status", "validate", "doctor"):
        assert call(command, "--root", tmp_path)[0] in {2, 3}
        assert snapshot_tree(tmp_path) == before


def test_v4_inspection_exact_state_and_null_family(tmp_path):
    project, task = v4(tmp_path)
    project.transition(task_id=task, from_stage="inbox", to_stage="active", tool="claim_task", actor="ME")
    identity = json.loads(project.config_path.read_bytes())["workspace_id"]
    project.create_task(workspace_id=identity, operation_id="incomplete-branch", branch_of=task,
                        sender="ME", recipient="ME", subject="Pending", body="Pending")
    code, result = call("inspect", task, "--root", tmp_path)
    assert code == 0
    assert result["data"]["stage"] == "active"
    assert result["data"]["family"]["family_digest"] is None
    assert not result["data"]["family"]["merge_ready"]
    path = Path(project.inspect_state(task_id=task)["path"])
    code, by_path = call("inspect", "--path", path, "--root", tmp_path)
    assert code == 0 and by_path["data"] == result["data"]
    path.write_bytes(path.read_bytes().replace(task.encode(), b"TASK-wrong-id"))
    before = snapshot_tree(tmp_path)
    code, invalid = call("validate", "--root", tmp_path)
    assert code == 2 and invalid["data"]["valid"] is False
    assert invalid["data"]["errors"]
    assert snapshot_tree(tmp_path) == before


def test_readonly_real_process_json(tmp_path):
    _, task = v4(tmp_path)
    before = snapshot_tree(tmp_path)
    result = subprocess.run([sys.executable, "-m", "fcop.cli._main", "inspect", task,
                             "--root", str(tmp_path), "--json"], capture_output=True, text=True,
                            encoding="utf-8", timeout=60)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["data"]["task_id"] == task
    assert "\x1b" not in result.stdout
    assert snapshot_tree(tmp_path) == before


@pytest.mark.parametrize("command", COMMANDS)
def test_invalid_flags_do_not_write(tmp_path, command, capsys):
    before = snapshot_tree(tmp_path)
    with pytest.raises(SystemExit) as result:
        main([command, "--repair"])
    assert result.value.code == 2
    assert capsys.readouterr().out == ""
    assert snapshot_tree(tmp_path) == before


def test_unknown_tool_internal_error_and_missing_optional(monkeypatch):
    from fcop.cli import _observe
    assert call("tools", "not-a-tool")[0] == (2 if _observe._mcp()["installed"] else 3)
    monkeypatch.setattr(_observe, "_mcp", lambda: {"installed": False, "version": None})
    code, result = call("tools")
    assert code == 3 and result["data"]["message"] == "fcop-mcp: not installed"
    monkeypatch.setattr(_observe, "_run", lambda _: (_ for _ in ()).throw(RuntimeError("failure")))
    code, result = call("version")
    assert code == 1 and result["errors"][0]["code"] == "RuntimeError"


def test_path_escape_and_partial_init_rejected(tmp_path):
    v4(tmp_path)
    assert call("inspect", "--root", tmp_path, "--path", "../outside.md")[0] == 2
    partial = tmp_path / "partial"
    (partial / "fcop").mkdir(parents=True)
    before = snapshot_tree(partial)
    assert call("status", "--root", partial)[0] == 2
    assert call("init", "--root", partial)[0] == 2
    assert snapshot_tree(partial) == before


def test_inspect_current_report_head_and_relations(tmp_path):
    project, task = v4(tmp_path)
    project.transition(task_id=task, from_stage="inbox", to_stage="active", tool="claim_task", actor="ME")
    state = project.inspect_state(task_id=task)
    identity = json.loads(project.config_path.read_bytes())["workspace_id"]
    first = project.write_report(workspace_id=identity, sender="ME", recipient="ME", subject_ref=task,
                                 body="Evidence", attempt_id=state["current_attempt_id"],
                                 report_kind="final", result="done")
    replacement = project.write_report(workspace_id=identity, sender="ME", recipient="ME", subject_ref=task,
                                       body="Updated evidence", attempt_id=state["current_attempt_id"],
                                       report_kind="replacement", result="done", references=[first["report_id"]])
    before = snapshot_tree(tmp_path)
    code, result = call("inspect", task, "--root", tmp_path)
    assert code == 0 and result["data"]["report_head"]["report_id"] == replacement["report_id"]
    assert call("validate", "--root", tmp_path)[0] == 0
    assert snapshot_tree(tmp_path) == before


def test_valid_legacy_task_inspect_and_validate(tmp_path):
    project = Project(tmp_path)
    project.init_solo(role_code="ME")
    task = project.write_task(sender="ADMIN", recipient="ME", priority="P2", subject="Legacy", body="Read")
    before = snapshot_tree(tmp_path)
    assert call("inspect", task.path.name, "--root", tmp_path)[0] == 0
    assert call("validate", "--root", tmp_path)[0] == 0
    assert snapshot_tree(tmp_path) == before
