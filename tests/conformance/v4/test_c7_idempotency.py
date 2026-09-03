"""C7 durable create idempotency and real process races."""

from __future__ import annotations

from pathlib import Path

from .driver import (
    V4ConformanceDriver, capture_error, error_code, result_field,
    run_concurrent_operations,
)
from .fixtures import ATTEMPT_A, WorkspaceFixture, read_frontmatter, snapshot_tree
from .scenarios import create_request, transition_request


def _worker_value(item: dict[str, object], name: str) -> object:
    assert item["status"] == "returned", item
    returned = item["returned"]
    assert isinstance(returned, dict), item
    assert name in returned, item
    return returned[name]


def test_c7_n01(workspace: WorkspaceFixture, v4_driver: V4ConformanceDriver) -> None:
    # Arrange: one normalized create request with durable public operation_id.
    kwargs = create_request("operation-c7-n01", body="same\r\nbody\r\n", references=["Z", "A", "A"])

    # Act: send semantically identical normalized requests twice.
    first = v4_driver.create_task(test_id="C7-N01", clause="F4.8.1-F4.8.5", **kwargs)
    first_snapshot = snapshot_tree(workspace.root)
    second = v4_driver.create_task(test_id="C7-N01", clause="F4.8.1-F4.8.5", **kwargs)

    # Assert: second is Existing with identical durable identity and no extra bytes/event.
    assert result_field(second, "existing") is True
    for field in ("task_id", "path", "digest"):
        assert result_field(first, field) == result_field(second, field)
    assert snapshot_tree(workspace.root) == first_snapshot
    assert len(workspace.task_paths(result_field(first, "task_id"))) == 1


def test_c7_r01(workspace: WorkspaceFixture, v4_driver: V4ConformanceDriver) -> None:
    # Arrange: reserve one operation key with request digest A.
    first = v4_driver.create_task(
        test_id="C7-R01", clause="F4.8.3-F4.8.4",
        **create_request("operation-c7-conflict", body="A\n")
    )
    before = snapshot_tree(workspace.root)

    # Act: reuse the same key with semantic body B.
    exc = capture_error(
        lambda: v4_driver.create_task(
            test_id="C7-R01", clause="F4.8.3-F4.8.4",
            **create_request("operation-c7-conflict", body="B\n")
        )
    )

    # Assert: conflict code and original TASK/operation fact remain byte-identical.
    assert first is not None
    assert error_code(exc) == "OPERATION_ID_CONFLICT"
    assert snapshot_tree(workspace.root) == before


def test_c7_x01(workspace: WorkspaceFixture) -> None:
    # Arrange: two commands carry the same operation_id and the same normalized request.
    kwargs = {
        "test_id": "C7-X01", "clause": "F4.8.2-F4.8.5",
        **create_request("operation-c7-race", subject="same", body="same\n"),
    }
    commands = [{"action": "create_task", "kwargs": kwargs} for _ in range(2)]

    # Act: race two spawned processes, then query again from a fresh spawned process.
    raced = run_concurrent_operations(workspace.root, commands)
    restarted = run_concurrent_operations(
        workspace.root, [{"action": "create_task", "kwargs": kwargs}]
    )[0]

    # Assert: all calls converge on one task/path/digest and exactly one TASK exists.
    assert all(item.get("code") != "V4_NOT_IMPLEMENTED" for item in [*raced, restarted]), (
        f"[C7-X01] F4.8.2-F4.8.5 production operation missing: {[*raced, restarted]}"
    )
    task_ids = {_worker_value(item, "task_id") for item in [*raced, restarted]}
    digests = {_worker_value(item, "digest") for item in [*raced, restarted]}
    paths = {_worker_value(item, "path") for item in [*raced, restarted]}
    assert len(task_ids) == len(digests) == len(paths) == 1
    assert len(workspace.task_paths(str(next(iter(task_ids))))) == 1
    assert _worker_value(restarted, "existing") is True


def test_c7_create_01(workspace: WorkspaceFixture, v4_driver: V4ConformanceDriver) -> None:
    # Arrange: one create key and a TASK that will later take ordinary T2.
    kwargs = create_request("operation-c7-boundary")

    # Act: replay create, then call T2 twice without a public operation_id.
    first = v4_driver.create_task(test_id="C7-CREATE-01", clause="F4.8; F4.9.8", **kwargs)
    second = v4_driver.create_task(test_id="C7-CREATE-01", clause="F4.8; F4.9.8", **kwargs)
    task_id = result_field(first, "task_id")
    claimed = v4_driver.transition(
        test_id="C7-CREATE-01", clause="F4.8; F4.9.8",
        **transition_request(task_id, "inbox", "active", tool="claim_task")
    )
    before_retry = snapshot_tree(workspace.root)
    exc = capture_error(
        lambda: v4_driver.transition(
            test_id="C7-CREATE-01", clause="F4.8; F4.9.8",
            **transition_request(task_id, "inbox", "active", tool="claim_task")
        )
    )

    # Assert: create is Existing; arbitrary T2 replay is not public idempotency.
    assert claimed is not None
    assert result_field(second, "existing") is True
    assert result_field(second, "task_id") == task_id
    assert error_code(exc) == "INVALID_TRANSITION"
    assert snapshot_tree(workspace.root) == before_retry


def test_at_01(workspace: WorkspaceFixture) -> None:
    # Arrange: active Root and two same-key Branch create commands.
    workspace.task("TASK-AT-01-ROOT", stage="active", attempt_id=ATTEMPT_A)
    same = {
        "test_id": "AT-01", "clause": "F4.8; F4.9.5",
        **create_request("operation-at-01", branch_of="TASK-AT-01-ROOT", body="same\n"),
    }

    # Act: race same digest; then submit the same key with a different digest.
    results = run_concurrent_operations(
        workspace.root,
        [{"action": "create_task", "kwargs": same}, {"action": "create_task", "kwargs": same}],
    )
    driver = V4ConformanceDriver(workspace.root)
    before_conflict = snapshot_tree(workspace.root)
    exc = capture_error(
        lambda: driver.create_task(
            test_id="AT-01", clause="F4.8; F4.9.5",
            **create_request("operation-at-01", branch_of="TASK-AT-01-ROOT", body="different\n")
        )
    )

    # Assert: same digest converges; different digest conflicts without second Branch.
    assert all(item.get("code") != "V4_NOT_IMPLEMENTED" for item in results), (
        f"[AT-01] F4.8/F4.9.5 production operation missing: {results}"
    )
    task_ids = {_worker_value(item, "task_id") for item in results}
    assert len(task_ids) == 1
    branch_id = str(next(iter(task_ids)))
    assert read_frontmatter(workspace.task_paths(branch_id)[0])["branch_of"] == "TASK-AT-01-ROOT"
    assert error_code(exc) == "OPERATION_ID_CONFLICT"
    assert snapshot_tree(workspace.root) == before_conflict
