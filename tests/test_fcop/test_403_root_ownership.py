"""4.0.3 customer-root ownership: real operations, not filename probes."""

from __future__ import annotations

import io
import json
from pathlib import Path

import pytest

from fcop import Project
from fcop.cli._main import main
from fcop.errors import FcopError

HOST_ACTIONS = (
    "redeploy", "inspect_profile", "status", "adopt", "plan", "apply",
    "verify_deployment", "rollback", "inspect_failure", "rollback_partial",
    "measure_context",
)
USER_FILES = {
    "AGENTS.md": b"Customer instructions\r\nnot owned by FCoP\xff",
    "CLAUDE.md": b"Customer Claude instructions\n",
    ".cursor/rules/customer.mdc": b"Customer Cursor settings\r\n",
    "GEMINI.md": b"Customer future Host\n",
    "README.md": b"Customer application README\n",
    "other/user.bin": bytes(range(256)),
}


def snapshot(root: Path) -> dict[str, bytes | None]:
    return {
        p.relative_to(root).as_posix(): p.read_bytes() if p.is_file() else None
        for p in root.rglob("*")
    }


def customer(root: Path, occupied: bool) -> dict[str, bytes | None]:
    root.mkdir(parents=True, exist_ok=True)
    if occupied:
        for relative, raw in USER_FILES.items():
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
    return snapshot(root)


def assert_customer_unchanged(root: Path, before: dict[str, bytes | None]) -> None:
    after = snapshot(root)
    assert {p: raw for p, raw in after.items() if p != "fcop" and not p.startswith("fcop/")} == before


@pytest.mark.parametrize("occupied", [False, True])
@pytest.mark.parametrize("initializer", ["project", "cli"])
def test_real_init_work_reads_and_reopen_preserve_root(tmp_path, occupied, initializer):
    root = tmp_path / "customer root"
    before = customer(root, occupied)
    if initializer == "cli":
        output = io.StringIO()
        assert main(["init", "--root", str(root), "--json"], stdout=output) == 0
        workspace = json.loads(output.getvalue())["data"]
    else:
        workspace = Project(root).create_workspace(protocol_version="4.0")
    project = Project(root)
    task = project.create_task(
        workspace_id=workspace["workspace_id"], operation_id="root-preservation",
        sender="ME", recipient="ME", subject="Customer boundary", body="Work",
    )
    project.transition(task_id=task["task_id"], from_stage="inbox", to_stage="active", actor="ME", tool="claim_task")
    state = project.inspect_state(task_id=task["task_id"])
    report = project.write_report(
        workspace_id=workspace["workspace_id"], subject_ref=task["task_id"],
        sender="ME", recipient="ME", attempt_id=state["current_attempt_id"],
        report_kind="final", result="done", body="Actual evidence",
    )
    project.transition(task_id=task["task_id"], from_stage="active", to_stage="review", actor="ME", tool="submit_task", report_ref=report["report_id"])
    project.write_review(
        workspace_id=workspace["workspace_id"], subject_ref=task["task_id"],
        sender="ME", recipient="ME", review_kind="assessment", decision="needs_human",
        body="Await acceptance", references=[report["report_id"]],
    )
    for command in ("status", "validate", "doctor"):
        output = io.StringIO()
        assert main([command, "--root", str(root), "--json"], stdout=output) == 0
        assert json.loads(output.getvalue())["status"] == "ok"
    unchanged = snapshot(root)
    reopened = Project(root)
    assert reopened.inspect_state(task_id=task["task_id"])["stage"] == "review"
    assert snapshot(root) == unchanged
    assert_customer_unchanged(root, before)


@pytest.mark.parametrize("action", HOST_ACTIONS)
@pytest.mark.parametrize("occupied", [False, True])
def test_retired_host_actions_are_structured_zero_write(tmp_path, action, occupied):
    customer(tmp_path, occupied)
    project = Project(tmp_path)
    project.create_workspace(protocol_version="4.0")
    before = snapshot(tmp_path)
    with pytest.raises(FcopError) as caught:
        project.rule_distribution(action=action, request={
            "host_profile_path": str(tmp_path / "missing-profile.json"),
            "target_paths": ["AGENTS.md", "CLAUDE.md"], "force": True,
            "adoption_receipt_ref": {"path": "missing", "sha256": "0" * 64},
        })
    assert caught.value.code == "toolkit:OPERATION_NOT_IMPLEMENTED"
    assert caught.value.operation_ref == action
    assert snapshot(tmp_path) == before
    assert not (tmp_path / "fcop/internal/rule-distribution").exists()


@pytest.mark.parametrize("assembly", ["sequential", "parallel"])
@pytest.mark.parametrize("language", ["en", "zh"])
def test_guidance_without_any_host_files(tmp_path, assembly, language):
    project = Project(tmp_path)
    project.create_workspace(protocol_version="4.0")
    before = snapshot(tmp_path)
    for uri in ("fcop://rules", "fcop://protocol", f"fcop://guidance/{assembly}/{language}"):
        result = project.rule_distribution(action="read_resource", request={"resource_uri": uri})
        assert result["content"] and len(result["sha256"]) == 64
    assert snapshot(tmp_path) == before
    assert set(p.name for p in tmp_path.iterdir()) == {"fcop"}
