"""WP3E recovery, fault-boundary, and cold-export production evidence."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from fcop import Project
from fcop.errors import V4ProtocolError
from tests.conformance.v4.fixtures import (
    ATTEMPT_A,
    WorkspaceFixture,
    read_frontmatter,
    sha256_bytes,
    snapshot_tree,
)
from tests.conformance.v4.scenarios import transition_request


@pytest.fixture
def workspace(tmp_path: Path) -> WorkspaceFixture:
    return WorkspaceFixture(tmp_path).create(profiles=[])


def _paths(workspace: WorkspaceFixture, task_id: str) -> tuple[Path, Path]:
    lifecycle = workspace.root / "fcop/_lifecycle"
    return lifecycle / "active" / f"{task_id}.md", lifecycle / "review" / f"{task_id}.md"


def _compact_state(
    workspace: WorkspaceFixture, state: str, operation_id: str
) -> tuple[Path, Path, Path]:
    task_id = f"TASK-UNIT-{state}"
    source, target = _paths(workspace, task_id)
    if state in {"S1", "S2", "S4"}:
        source = workspace.task(task_id, stage="active", attempt_id=ATTEMPT_A, body="source")
    source_bytes = source.read_bytes() if source.exists() else b""
    if state == "S2":
        target.write_bytes(source_bytes)
    elif state == "S3":
        target = workspace.task(task_id, stage="review", attempt_id=ATTEMPT_A, body="source")
        source_bytes = target.read_bytes()
    elif state == "S4":
        workspace.task(task_id, stage="review", attempt_id=ATTEMPT_A, body="different")
    receipt = workspace.receipt(
        operation_id,
        source=source,
        target=target,
        stage="PREPARED" if state == "S1" else "TARGET_DURABLE",
        content_digest=sha256_bytes(source_bytes or b"expected"),
        corrupt=state == "S5",
    )
    return source, target, receipt


@pytest.mark.parametrize(
    ("state", "classification"),
    [
        ("S1", "NOT_COMMITTED"),
        ("S2", "RECOVERABLE_DUPLICATE"),
        ("S3", "COMMITTED"),
        ("S4", "DIVERGENT_DUPLICATE"),
        ("S5", "INDETERMINATE"),
    ],
)
def test_public_recovery_five_state_table(
    workspace: WorkspaceFixture, state: str, classification: str
) -> None:
    operation_id = f"operation-unit-{state.lower()}"
    source, target, receipt = _compact_state(workspace, state, operation_id)
    before = snapshot_tree(workspace.root)
    result = Project(workspace.root).recover_operation(
        operation_id=operation_id,
        source_path=source,
        target_path=target,
        receipt_path=receipt,
    )
    assert result["classification"] == classification
    if state == "S1":
        assert source.exists() and not target.exists()
    elif state in {"S2", "S3"}:
        assert not source.exists() and target.exists()
        assert json.loads(receipt.read_text("utf-8"))["stage"] == "COMMITTED"
    else:
        assert snapshot_tree(workspace.root) == before
        repeated = Project(workspace.root).recover_operation(
            operation_id=operation_id,
            source_path=source,
            target_path=target,
            receipt_path=receipt,
        )
        assert repeated["classification"] == classification
        assert snapshot_tree(workspace.root) == before


def test_full_lifecycle_receipt_uses_same_classifier(workspace: WorkspaceFixture) -> None:
    task_id = "TASK-UNIT-FULL"
    source = workspace.task(task_id, stage="inbox")
    source_bytes = source.read_bytes()
    request = transition_request(task_id, "inbox", "active", tool="claim_task")
    committed = Project(workspace.root).transition(**request)
    target = Path(committed["path"])
    receipt = workspace.root / committed["receipt_ref"]
    value = json.loads(receipt.read_text("utf-8"))
    source.write_bytes(source_bytes)
    value["stage"] = "TARGET_DURABLE"
    receipt.write_text(
        json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    result = Project(workspace.root).recover_operation(
        operation_id=value["operation_id"],
        source_path=source,
        target_path=target,
        receipt_path=receipt,
    )
    assert result["classification"] == "RECOVERABLE_DUPLICATE"
    assert not source.exists() and target.exists()
    assert len(read_frontmatter(target)["transitions"]) == 1


@pytest.mark.parametrize("case", ["different-task", "illegal-edge", "receipt-outside", "op-mismatch"])
def test_recovery_rejects_unbound_evidence(
    workspace: WorkspaceFixture, case: str
) -> None:
    operation_id = "operation-unit-invalid"
    source, target, receipt = _compact_state(workspace, "S1", operation_id)
    if case == "different-task":
        target = target.with_name("TASK-OTHER.md")
    elif case == "illegal-edge":
        target = workspace.root / "fcop/_lifecycle/archive" / source.name
    elif case == "receipt-outside":
        receipt = workspace.root / "fcop/fcop.json"
    elif case == "op-mismatch":
        operation_id = "operation-unit-other"
    before = snapshot_tree(workspace.root)
    try:
        result = Project(workspace.root).recover_operation(
            operation_id=operation_id,
            source_path=source,
            target_path=target,
            receipt_path=receipt,
        )
    except V4ProtocolError as exc:
        assert exc.code == "RECOVERY_REQUIRED"
    else:
        assert result["classification"] == "INDETERMINATE"
        assert result["error_code"] == "RECOVERY_REQUIRED"
    assert snapshot_tree(workspace.root) == before


def test_recovery_rejects_traversal_and_network_without_writes(
    workspace: WorkspaceFixture,
) -> None:
    source, target, receipt = _compact_state(workspace, "S1", "operation-unit-boundary")
    before = snapshot_tree(workspace.root)
    with pytest.raises(V4ProtocolError) as traversal:
        Project(workspace.root).recover_operation(
            operation_id="operation-unit-boundary",
            source_path="../outside.md",
            target_path=target,
            receipt_path=receipt,
        )
    assert traversal.value.code == "RECOVERY_REQUIRED"
    with pytest.raises(V4ProtocolError) as network:
        Project(workspace.root).recover_operation(
            operation_id="operation-unit-boundary",
            source_path=source,
            target_path=target,
            receipt_path=receipt,
            filesystem="network",
        )
    assert network.value.code == "UNSUPPORTED_FILESYSTEM"
    assert snapshot_tree(workspace.root) == before


def test_recovery_rejects_symlink_escape(workspace: WorkspaceFixture, tmp_path: Path) -> None:
    outside = tmp_path.parent / f"{tmp_path.name}-outside-recovery-task.md"
    outside.write_text("outside", encoding="utf-8")
    source = workspace.root / "fcop/_lifecycle/active/TASK-LINK.md"
    target = workspace.root / "fcop/_lifecycle/review/TASK-LINK.md"
    try:
        source.symlink_to(outside)
    except OSError:
        pytest.skip("native symlink creation is unavailable")
    before = outside.read_bytes()
    with pytest.raises(V4ProtocolError) as caught:
        Project(workspace.root).recover_operation(
            operation_id="operation-unit-link",
            source_path=source,
            target_path=target,
        )
    assert caught.value.code == "RECOVERY_REQUIRED"
    assert outside.read_bytes() == before


@pytest.mark.parametrize("stage", ["PREPARED", "TARGET_DURABLE", "COMMITTED", "RESPONSE_LOST"])
def test_transition_faults_land_only_named_durable_states(
    workspace: WorkspaceFixture, stage: str
) -> None:
    task_id = f"TASK-UNIT-FAULT-{stage}"
    source = workspace.task(task_id, stage="inbox")
    target = workspace.root / "fcop/_lifecycle/active" / source.name
    operation_id = f"internal-unit-{stage.lower()}"
    project = Project(workspace.root)
    project.inject_fault(operation="transition", stage=stage, once=True)
    with pytest.raises(V4ProtocolError) as caught:
        project.transition(
            **transition_request(task_id, "inbox", "active", tool="claim_task"),
            internal_operation_id=operation_id,
        )
    assert caught.value.code == "RECOVERY_REQUIRED"
    receipt = workspace.root / "fcop/operations" / f"{operation_id}.json"
    recovered = project.recover_operation(
        operation_id=operation_id,
        source_path=source,
        target_path=target,
        receipt_path=receipt,
    )
    assert recovered["classification"] in {
        "NOT_COMMITTED",
        "RECOVERABLE_DUPLICATE",
        "COMMITTED",
    }
    visible = [path for path in (source, target) if path.exists()]
    assert len(visible) == 1
    assert len(read_frontmatter(visible[0])["transitions"]) <= 1


def test_fault_plan_is_once_in_memory_and_internal_id_is_not_public(
    workspace: WorkspaceFixture,
) -> None:
    archived = workspace.task("TASK-UNIT-COLD-ONCE", stage="archive", attempt_id=ATTEMPT_A)
    project = Project(workspace.root)
    project.inject_fault(operation="export_archive", stage="PREPARED", once=True)
    with pytest.raises(V4ProtocolError):
        project.export_archive(task_id="TASK-UNIT-COLD-ONCE")
    assert project.export_archive(task_id="TASK-UNIT-COLD-ONCE")["existing"] is False
    assert archived.exists()
    assert not list((workspace.root / "fcop").rglob("*fault*"))

    inbox = workspace.task("TASK-UNIT-NO-REPLAY-KEY", stage="inbox")
    request = transition_request(
        "TASK-UNIT-NO-REPLAY-KEY", "inbox", "active", tool="claim_task"
    )
    with pytest.raises(V4ProtocolError) as caught:
        Project(workspace.root).transition(
            **request, internal_operation_id="internal-unit-forbidden"
        )
    assert caught.value.code == "INVALID_ENVELOPE" and inbox.exists()


def test_cold_export_is_non_authoritative_and_idempotent(
    workspace: WorkspaceFixture,
) -> None:
    task_id = "TASK-UNIT-COLD"
    archived = workspace.task(task_id, stage="archive", attempt_id=ATTEMPT_A)
    before = archived.read_bytes()
    project = Project(workspace.root)
    state_before = project.inspect_state(task_id=task_id)
    first = project.export_archive(task_id=task_id)
    second = project.export_archive(task_id=task_id)
    cold = Path(first["path"])
    assert first["existing"] is False and second["existing"] is True
    assert archived.read_bytes() == before == cold.read_bytes()
    assert "_lifecycle" not in cold.relative_to(workspace.root / "fcop/cold").parts
    assert project.inspect_state(task_id=task_id) == state_before
    assert read_frontmatter(archived)["transitions"] == read_frontmatter(cold)["transitions"]


def test_cold_export_conflict_and_target_durable_fault_preserve_archive(
    workspace: WorkspaceFixture,
) -> None:
    task_id = "TASK-UNIT-COLD-CONFLICT"
    archived = workspace.task(task_id, stage="archive", attempt_id=ATTEMPT_A)
    original = archived.read_bytes()
    cold = workspace.root / "fcop/cold" / archived.name
    cold.write_bytes(b"different")
    with pytest.raises(V4ProtocolError) as conflict:
        Project(workspace.root).export_archive(task_id=task_id)
    assert conflict.value.code == "TARGET_ALREADY_EXISTS_DIFFERENT"
    assert cold.read_bytes() == b"different" and archived.read_bytes() == original
    cold.unlink()
    project = Project(workspace.root)
    project.inject_fault(operation="export_archive", stage="TARGET_DURABLE", once=True)
    with pytest.raises(V4ProtocolError):
        project.export_archive(task_id=task_id)
    assert cold.read_bytes() == original and archived.read_bytes() == original
    assert Project(workspace.root).inspect_state(task_id=task_id)["stage"] == "archive"


def test_new_public_methods_fail_closed_on_v3(tmp_path: Path) -> None:
    project = Project(tmp_path)
    project.init_solo(role_code="ME")
    calls = [
        lambda: project.inject_fault(operation="transition", stage="PREPARED"),
        lambda: project.export_archive(task_id="TASK-V3"),
        lambda: project.recover_operation(
            operation_id="operation-v3",
            source_path="fcop/_lifecycle/inbox/TASK-V3.md",
            target_path="fcop/_lifecycle/active/TASK-V3.md",
        ),
    ]
    for call in calls:
        with pytest.raises(V4ProtocolError) as caught:
            call()
        assert caught.value.code == "UNSUPPORTED_WORKSPACE_VERSION"
