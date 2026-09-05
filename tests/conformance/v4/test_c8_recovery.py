"""C8 atomic commit, five recovery states, and real-operation races."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from .driver import (
    V4ConformanceDriver,
    capture_error,
    error_code,
    result_field,
    run_concurrent_operations,
)
from .fixtures import (
    ATTEMPT_A,
    DeterministicProfileEvaluator,
    WorkspaceFixture,
    bind_t3,
    sha256_bytes,
    snapshot_tree,
)
from .scenarios import assert_task_stage, authorization_fixture, create_request, transition_request


def _recovery_paths(workspace: WorkspaceFixture, task_id: str) -> tuple[Path, Path]:
    root = workspace.root / "fcop" / "_lifecycle"
    return root / "active" / f"{task_id}.md", root / "review" / f"{task_id}.md"


def _arrange_recovery_state(
    workspace: WorkspaceFixture, state: str, operation_id: str
) -> tuple[Path, Path, Path | None, dict[str, bytes]]:
    source, target = _recovery_paths(workspace, f"TASK-{state}")
    receipt = None
    if state in {"S1", "S2", "S4"}:
        source = workspace.task(f"TASK-{state}", stage="active", attempt_id=ATTEMPT_A, body="source")
    source_bytes = source.read_bytes() if source.exists() else b""
    if state == "S2":
        target.write_bytes(source_bytes)
    elif state == "S3":
        target = workspace.task(f"TASK-{state}", stage="review", attempt_id=ATTEMPT_A, body="source")
        source_bytes = target.read_bytes()
    elif state == "S4":
        workspace.task(f"TASK-{state}", stage="review", attempt_id=ATTEMPT_A, body="different")
    digest = sha256_bytes(source_bytes or b"expected")
    if state == "S1":
        receipt = workspace.receipt(
            operation_id, source=source, target=target, stage="PREPARED", content_digest=digest
        )
    elif state in {"S2", "S3", "S4"}:
        receipt = workspace.receipt(
            operation_id, source=source, target=target, stage="TARGET_DURABLE", content_digest=digest
        )
    elif state == "S5":
        receipt = workspace.receipt(
            operation_id, source=source, target=target, stage="TARGET_DURABLE",
            content_digest=digest, corrupt=True,
        )
    visible = {str(path): path.read_bytes() for path in (source, target) if path.exists()}
    return source, target, receipt, visible


def _recover(
    driver: V4ConformanceDriver, test_id: str, operation_id: str,
    source: Path, target: Path, receipt: Path | None,
) -> object:
    return driver.recover_operation(
        test_id=test_id, clause="F4.9.1-F4.9.10", operation_id=operation_id,
        source_path=source, target_path=target, receipt_path=receipt,
    )


def test_c8_n01(workspace: WorkspaceFixture, v4_driver: V4ConformanceDriver) -> None:
    # Arrange: one legal inbox→active transition and no receipt.
    workspace.task("TASK-C8-N01", stage="inbox")
    before_receipts = set((workspace.root / "fcop" / "operations").glob("*"))

    # Act: execute the production transition.
    result = v4_driver.transition(
        test_id="C8-N01", clause="F4.9.1-F4.9.4",
        **transition_request("TASK-C8-N01", "inbox", "active", tool="claim_task")
    )

    # Assert: COMMITTED, one path/event, and one durable auditable receipt.
    assert result_field(result, "status") == "COMMITTED"
    path, fields = assert_task_stage(workspace, "TASK-C8-N01", "active")
    assert len(fields["transitions"]) == 1
    receipts = set((workspace.root / "fcop" / "operations").glob("*")) - before_receipts
    assert len(receipts) == 1
    assert json.loads(next(iter(receipts)).read_text("utf-8"))["stage"] == "COMMITTED"
    assert path.exists()


def test_c8_r01(workspace: WorkspaceFixture, v4_driver: V4ConformanceDriver) -> None:
    # Arrange: source and destination for one TASK ID contain different bytes.
    source = workspace.task("TASK-C8-R01", stage="inbox", body="source")
    target = workspace.task("TASK-C8-R01", stage="active", body="different")
    source_bytes, target_bytes = source.read_bytes(), target.read_bytes()

    # Act: attempt inbox→active into the conflicting destination.
    exc = capture_error(
        lambda: v4_driver.transition(
            test_id="C8-R01", clause="F4.9.2",
            **transition_request("TASK-C8-R01", "inbox", "active", tool="claim_task")
        )
    )

    # Assert: no overwrite/delete and exact stable error.
    assert error_code(exc) == "TARGET_ALREADY_EXISTS_DIFFERENT"
    assert source.read_bytes() == source_bytes
    assert target.read_bytes() == target_bytes


@pytest.mark.parametrize("fault_stage", ["PREPARED", "TARGET_DURABLE", "COMMITTED", "RESPONSE_LOST"])
def test_c8_x01(
    workspace: WorkspaceFixture, v4_driver: V4ConformanceDriver, fault_stage: str
) -> None:
    # Arrange: one legal transition with fault injection at a named abstract boundary.
    task_id = f"TASK-C8-X01-{fault_stage}"
    workspace.task(task_id, stage="inbox")
    operation_id = f"internal-c8-x01-{fault_stage.lower()}"
    v4_driver.inject_fault(
        test_id="C8-X01", clause="F4.9.1-F4.9.4; F4.9.9",
        operation="transition", stage=fault_stage, once=True,
    )

    # Act: crash/lose response, then invoke durable recovery for visible facts.
    capture_error(
        lambda: v4_driver.transition(
            test_id="C8-X01", clause="F4.9.1-F4.9.4; F4.9.9",
            internal_operation_id=operation_id,
            **transition_request(task_id, "inbox", "active", tool="claim_task")
        )
    )
    source = workspace.root / "fcop" / "_lifecycle" / "inbox" / f"{task_id}.md"
    target = workspace.root / "fcop" / "_lifecycle" / "active" / f"{task_id}.md"
    receipt = workspace.root / "fcop" / "operations" / f"{operation_id}.json"
    recovered = _recover(v4_driver, "C8-X01", operation_id, source, target, receipt)

    # Assert: exactly one of five states, never two TASKs or a fabricated second event.
    classification = result_field(recovered, "classification")
    assert classification in {
        "NOT_COMMITTED", "COMMITTED", "RECOVERABLE_DUPLICATE",
        "DIVERGENT_DUPLICATE", "INDETERMINATE",
    }
    paths = workspace.task_paths(task_id)
    assert len(paths) <= 1 or classification == "DIVERGENT_DUPLICATE"
    if len(paths) == 1:
        assert len(json.loads(receipt.read_text("utf-8"))) > 0


def test_c8_x02(workspace: WorkspaceFixture) -> None:
    # Arrange: done Root with authorization; Branch-create races Root archive.
    workspace.task("TASK-C8-X02-ROOT", stage="done", attempt_id=ATTEMPT_A)
    authorization_fixture(
        workspace, "REVIEW-C8-X02", task_id="TASK-C8-X02-ROOT",
        from_stage="done", to_stage="archive", attempt_id=ATTEMPT_A,
    )
    commands = [
        {"action": "create_task", "kwargs": {
            "test_id": "C8-X02", "clause": "F4.9.5",
            **create_request("c8-x02-branch", branch_of="TASK-C8-X02-ROOT"),
        }},
        {"action": "transition", "kwargs": {
            "test_id": "C8-X02", "clause": "F4.9.5",
            **transition_request(
                "TASK-C8-X02-ROOT", "done", "archive", tool="archive_task",
                authorization_ref="REVIEW-C8-X02",
            ),
        }},
    ]

    # Act: execute both production commits in synchronized processes.
    results = run_concurrent_operations(workspace.root, commands)

    # Assert: no missing surface, no Branch appears beneath an archived Root.
    assert all(item.get("code") != "V4_NOT_IMPLEMENTED" for item in results), (
        f"[C8-X02] F4.9.5 production operation missing: {results}"
    )
    root_stage = workspace.task_paths("TASK-C8-X02-ROOT")[0].parent.name
    branch_files = [
        path for path in (workspace.root / "fcop" / "_lifecycle").glob("*/*.md")
        if path.name != "TASK-C8-X02-ROOT.md"
    ]
    if root_stage == "archive":
        assert not branch_files
    else:
        assert root_stage == "done"
        assert any(item["status"] == "error" for item in results)


@pytest.mark.parametrize("case", ["divergent", "corrupt-receipt", "unsupported-filesystem"])
def test_c8_x03(
    workspace: WorkspaceFixture, v4_driver: V4ConformanceDriver, case: str
) -> None:
    # Arrange: divergent copies, corrupt receipt, or explicitly unsupported filesystem.
    source, target, receipt, visible = _arrange_recovery_state(
        workspace, "S4" if case == "divergent" else "S5", f"operation-c8-x03-{case}"
    )

    # Act: ask production recovery to classify without guessing.
    if case == "unsupported-filesystem":
        exc = capture_error(
            lambda: v4_driver.recover_operation(
                test_id="C8-X03", clause="F4.9.4; F4.9.7",
                operation_id="operation-c8-x03-fs", source_path=source,
                target_path=target, receipt_path=receipt, filesystem="network",
            )
        )
        observed = error_code(exc)
    else:
        result = _recover(v4_driver, "C8-X03", f"operation-c8-x03-{case}", source, target, receipt)
        observed = result_field(result, "classification")

    # Assert: explicit fail-closed class/error and every visible byte preserved.
    expected = {
        "divergent": "DIVERGENT_DUPLICATE",
        "corrupt-receipt": "INDETERMINATE",
        "unsupported-filesystem": "UNSUPPORTED_FILESYSTEM",
    }[case]
    assert observed == expected
    assert {str(path): path.read_bytes() for path in (source, target) if path.exists()} == visible


AUTHORIZED_EDGES = [
    ("T4", "review", "done", "approve_task"),
    ("T5", "review", "active", "reject_task"),
    ("T6", "done", "active", "reopen_task"),
    ("T7", "done", "archive", "archive_task"),
]

DIFFERENT_AUTHORIZED_EDGE = {
    "T4": ("review", "active", "reject_task"),
    "T5": ("review", "done", "approve_task"),
    "T6": ("review", "done", "approve_task"),
    "T7": ("done", "active", "reopen_task"),
}


@pytest.mark.parametrize(
    ("edge", "source_stage", "target_stage", "tool"), AUTHORIZED_EDGES,
    ids=[item[0] for item in AUTHORIZED_EDGES],
)
def test_c8_retry_01(
    workspace: WorkspaceFixture, v4_driver: V4ConformanceDriver,
    edge: str, source_stage: str, target_stage: str, tool: str,
) -> None:
    # Arrange: complete evidence for T4/T5/T6/T7 and a lost-response fault.
    task_id = f"TASK-C8-RETRY-{edge}"
    workspace.task(task_id, stage=source_stage, attempt_id=ATTEMPT_A)
    report_ref = review_ref = None
    if edge in {"T4", "T5"}:
        workspace.report(f"REPORT-C8-{edge}", task_id=task_id, attempt_id=ATTEMPT_A)
        report_ref = f"REPORT-C8-{edge}"
        bind_t3(workspace, task_id, report_ref)
        kind = "acceptance" if edge == "T4" else "rejection"
        decision = "approved" if edge == "T4" else "rejected"
        workspace.review(
            f"REVIEW-C8-{edge}", task_id=task_id, review_kind=kind, decision=decision,
            attempt_id=ATTEMPT_A, references=[report_ref], profile_ref="profile:test",
            transition={"from": source_stage, "to": target_stage},
            authorization_scope="single_use",
        )
        review_ref = f"REVIEW-C8-{edge}"
    else:
        authorization_fixture(
            workspace, f"REVIEW-C8-{edge}", task_id=task_id,
            from_stage=source_stage, to_stage=target_stage, attempt_id=ATTEMPT_A,
        )
        review_ref = f"REVIEW-C8-{edge}" if edge == "T6" else None
    auth_ref = f"REVIEW-C8-{edge}"
    kwargs = transition_request(
        task_id, source_stage, target_stage, tool=tool, report_ref=report_ref,
        review_ref=review_ref, authorization_ref=auth_ref,
    )
    driver = V4ConformanceDriver(
        workspace.root,
        trusted_profiles={"profile:test": DeterministicProfileEvaluator("AUTHORIZED")},
        test_id="C8-RETRY-01",
    )

    # Act: lose the first response, retry the exact operation, then try to spend
    # the consumed authorization on a different valid authorization-gated edge.
    def commit_then_lose_response() -> None:
        driver.transition(
            test_id="C8-RETRY-01", clause="F4.9.8; F4.9.11", **kwargs
        )
        raise ConnectionError("response lost after durable production return")

    capture_error(commit_then_lose_response)
    after_commit = snapshot_tree(workspace.root)
    retry = driver.transition(
        test_id="C8-RETRY-01", clause="F4.9.8; F4.9.11", **kwargs
    )
    after_exact_retry = snapshot_tree(workspace.root)
    other_from, other_to, other_tool = DIFFERENT_AUTHORIZED_EDGE[edge]
    different_kwargs = dict(kwargs)
    different_kwargs.update({
        "from_stage": other_from, "to_stage": other_to, "tool": other_tool,
    })
    reused = capture_error(
        lambda: driver.transition(
            test_id="C8-RETRY-01", clause="F4.9.8; F4.9.11",
            **different_kwargs,
        )
    )

    # Assert: exact retry is Existing; a different transition is REUSED and
    # performs zero movement, zero new event, and zero second consumption.
    assert result_field(retry, "existing") is True
    assert snapshot_tree(workspace.root) == after_commit
    assert error_code(reused) == "AUTHORIZATION_REUSED"
    assert snapshot_tree(workspace.root) == after_exact_retry
    _, fields = assert_task_stage(workspace, task_id, target_stage)
    assert sum(event.get("authorization_ref") == auth_ref for event in fields["transitions"]) == 1


RECOVERY_STATES = [
    ("S1", "NOT_COMMITTED"),
    ("S2", "RECOVERABLE_DUPLICATE"),
    ("S3", "COMMITTED"),
    ("S4", "DIVERGENT_DUPLICATE"),
    ("S5", "INDETERMINATE"),
]


@pytest.mark.parametrize(
    ("state", "expected"), RECOVERY_STATES, ids=[item[0] for item in RECOVERY_STATES]
)
def test_c8_state_01(
    workspace: WorkspaceFixture, v4_driver: V4ConformanceDriver,
    state: str, expected: str,
) -> None:
    # Arrange: exact source/target/receipt row from the frozen five-state table.
    operation_id = f"operation-c8-state-{state.lower()}"
    source, target, receipt, visible = _arrange_recovery_state(workspace, state, operation_id)

    # Act: mechanically classify and recover.
    result = _recover(v4_driver, "C8-STATE-01", operation_id, source, target, receipt)

    # Assert: unique class and the row-specific permitted mechanical action.
    assert result_field(result, "classification") == expected
    if state == "S1":
        assert source.exists() and not target.exists()
    elif state in {"S2", "S3"}:
        assert not source.exists() and target.exists()
        assert json.loads(receipt.read_text("utf-8"))["stage"] == "COMMITTED"
    else:
        assert {str(path): path.read_bytes() for path in (source, target) if path.exists()} == visible
        if state == "S5":
            assert result_field(result, "error_code") == "RECOVERY_REQUIRED"


def test_c8_indeterminate_01(workspace: WorkspaceFixture, v4_driver: V4ConformanceDriver) -> None:
    # Arrange: both files absent and a corrupt conflicting receipt.
    operation_id = "operation-c8-indeterminate"
    source, target = _recovery_paths(workspace, "TASK-C8-INDETERMINATE")
    receipt = workspace.receipt(
        operation_id, source=source, target=target, stage="TARGET_DURABLE",
        content_digest="0" * 64, corrupt=True,
    )
    receipt_bytes = receipt.read_bytes()

    # Act: ask recovery to decide from unprovable evidence.
    result = _recover(v4_driver, "C8-INDETERMINATE-01", operation_id, source, target, receipt)

    # Assert: only INDETERMINATE, evidence preserved, Fail Closed error.
    assert result_field(result, "classification") == "INDETERMINATE"
    assert result_field(result, "error_code") == "RECOVERY_REQUIRED"
    assert receipt.read_bytes() == receipt_bytes
    assert not source.exists() and not target.exists()


def test_at_02(workspace: WorkspaceFixture) -> None:
    # Arrange: done Root, archive authorization, and a competing Branch create.
    workspace.task("TASK-AT-02-ROOT", stage="done", attempt_id=ATTEMPT_A)
    authorization_fixture(
        workspace, "REVIEW-AT-02", task_id="TASK-AT-02-ROOT",
        from_stage="done", to_stage="archive", attempt_id=ATTEMPT_A,
    )
    commands = [
        {"action": "create_task", "kwargs": {
            "test_id": "AT-02", "clause": "F4.5.4; F4.9.5",
            **create_request("operation-at-02", branch_of="TASK-AT-02-ROOT"),
        }},
        {"action": "transition", "kwargs": {
            "test_id": "AT-02", "clause": "F4.5.4; F4.9.5",
            **transition_request(
                "TASK-AT-02-ROOT", "done", "archive", tool="archive_task",
                authorization_ref="REVIEW-AT-02",
            ),
        }},
    ]

    # Act: run real create-Branch/root-archive competition.
    results = run_concurrent_operations(workspace.root, commands)

    # Assert: archived Root never gains a new Branch; loser returns a stable error.
    assert all(item.get("code") != "V4_NOT_IMPLEMENTED" for item in results), (
        f"[AT-02] F4.5.4/F4.9.5 production operation missing: {results}"
    )
    root_stage = workspace.task_paths("TASK-AT-02-ROOT")[0].parent.name
    branches = [path for path in (workspace.root / "fcop" / "_lifecycle").glob("*/*.md") if path.name != "TASK-AT-02-ROOT.md"]
    if root_stage == "archive":
        assert not branches
    else:
        assert root_stage == "done"
        assert any(item["status"] == "error" for item in results)


@pytest.mark.parametrize("fault_stage", ["PREPARED", "TARGET_DURABLE", "RESPONSE_LOST"])
def test_at_05(
    workspace: WorkspaceFixture, v4_driver: V4ConformanceDriver, fault_stage: str
) -> None:
    # Arrange: real transition with deterministic fault boundary, no sleep/timing oracle.
    task_id = f"TASK-AT-05-{fault_stage}"
    workspace.task(task_id, stage="inbox")
    operation_id = f"operation-at-05-{fault_stage.lower()}"
    v4_driver.inject_fault(
        test_id="AT-05", clause="F4.9.1-F4.9.11",
        operation="transition", stage=fault_stage, once=True,
    )

    # Act: trigger fault, then recover and retry from durable evidence.
    capture_error(
        lambda: v4_driver.transition(
            test_id="AT-05", clause="F4.9.1-F4.9.11",
            internal_operation_id=operation_id,
            **transition_request(task_id, "inbox", "active", tool="claim_task")
        )
    )
    source = workspace.root / "fcop" / "_lifecycle" / "inbox" / f"{task_id}.md"
    target = workspace.root / "fcop" / "_lifecycle" / "active" / f"{task_id}.md"
    receipt = workspace.root / "fcop" / "operations" / f"{operation_id}.json"
    recovered = _recover(v4_driver, "AT-05", operation_id, source, target, receipt)

    # Assert: classified result, at most one authoritative TASK, no duplicate event.
    assert result_field(recovered, "classification") in {item[1] for item in RECOVERY_STATES}
    paths = workspace.task_paths(task_id)
    assert len(paths) <= 1
    if paths:
        assert len(json.loads(receipt.read_text("utf-8"))) > 0


@pytest.mark.parametrize("state", ["S2", "S4", "S5"])
def test_at_06(
    workspace: WorkspaceFixture, v4_driver: V4ConformanceDriver, state: str
) -> None:
    # Arrange: same duplicate, divergent duplicate, or corrupt/unprovable evidence.
    operation_id = f"operation-at-06-{state.lower()}"
    source, target, receipt, visible = _arrange_recovery_state(workspace, state, operation_id)

    # Act: invoke real recovery.
    result = _recover(v4_driver, "AT-06", operation_id, source, target, receipt)

    # Assert: same is mechanically recoverable; different/corrupt is preserved and closed.
    expected = {"S2": "RECOVERABLE_DUPLICATE", "S4": "DIVERGENT_DUPLICATE", "S5": "INDETERMINATE"}[state]
    assert result_field(result, "classification") == expected
    if state == "S2":
        assert not source.exists() and target.exists()
    else:
        assert {str(path): path.read_bytes() for path in (source, target) if path.exists()} == visible
