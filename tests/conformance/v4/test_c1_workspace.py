"""C1 workspace identity behavioral conformance."""

from __future__ import annotations

import json

from .driver import V4ConformanceDriver, capture_error, error_code, result_field
from .fixtures import WORKSPACE_A, WORKSPACE_B, WorkspaceFixture, read_frontmatter, snapshot_tree


def _create_kwargs(workspace_id: str, operation_id: str = "c1-create") -> dict[str, object]:
    return {
        "workspace_id": workspace_id, "operation_id": operation_id,
        "operation_kind": "create_task", "sender": "ME", "recipient": "ME",
        "priority": "P2", "subject": "identity probe", "body": "body\n",
        "parent": None, "branch_of": None, "references": [],
    }


def test_c1_n01(empty_workspace: WorkspaceFixture) -> None:
    # Arrange: an empty directory with no manifest.
    driver = V4ConformanceDriver(empty_workspace.root)

    # Act: create an actual 4.0 workspace and then create a matching TASK.
    created = driver.create_workspace(
        test_id="C1-N01", clause="F4.2.1-F4.2.3",
        protocol_version="4.0", encoding="fcop-filesystem/4.0", profiles=[],
    )
    manifest = json.loads(empty_workspace.manifest_path.read_text(encoding="utf-8"))
    task = driver.create_task(
        test_id="C1-N01", clause="F4.2.1-F4.2.3", **_create_kwargs(manifest["workspace_id"])
    )

    # Assert: creation is not a stub and both declaration and envelope bind the same ID.
    assert created is not None
    assert manifest["protocol"] == "fcop"
    assert manifest["protocol_version"] == "4.0"
    assert manifest["encoding"] == {"name": "fcop-filesystem", "version": "4.0"}
    assert manifest["profiles"] == []
    task_id = result_field(task, "task_id")
    task_path = empty_workspace.task_paths(task_id)[0]
    assert read_frontmatter(task_path)["workspace_id"] == manifest["workspace_id"]


def test_c1_r01(workspace: WorkspaceFixture, v4_driver: V4ConformanceDriver) -> None:
    # Arrange: workspace A and a create request that explicitly claims workspace B.
    before = snapshot_tree(workspace.root)

    # Act: submit the mismatched envelope request.
    exc = capture_error(
        lambda: v4_driver.create_task(
            test_id="C1-R01", clause="F4.2.2", **_create_kwargs(WORKSPACE_B, "c1-mismatch")
        )
    )

    # Assert: stable error and byte-for-byte zero writes.
    assert error_code(exc) == "WORKSPACE_ID_MISMATCH"
    assert snapshot_tree(workspace.root) == before


def test_c1_fork_01(workspace: WorkspaceFixture) -> None:
    # Arrange: one writable source workspace and two empty destinations.
    destination = workspace.root.parent / "derived"
    mirror = workspace.root.parent / "mirror"
    driver = V4ConformanceDriver(workspace.root)

    # Act: request an independent writable derive, then forced ID retention.
    result = driver.derive_workspace(
        test_id="C1-FORK-01", clause="F4.2.4", destination=destination,
        mode="independent-writable", retain_workspace_id=False,
    )
    retained = None
    retained_error = None
    try:
        retained = driver.derive_workspace(
            test_id="C1-FORK-01", clause="F4.2.4", destination=mirror,
            mode="independent-writable", retain_workspace_id=True,
        )
    except Exception as exc:
        retained_error = exc

    # Assert: writable derive has a new ID; retained-ID output is explicitly read-only.
    derived_manifest = json.loads((destination / "fcop" / "fcop.json").read_text("utf-8"))
    assert result is not None
    assert derived_manifest["workspace_id"] != WORKSPACE_A
    if retained_error is not None:
        assert error_code(retained_error) == "WORKSPACE_ID_CLONE_CONFLICT"
        assert not mirror.exists() or not any(mirror.rglob("TASK-*.md"))
    else:
        assert result_field(retained, "read_only") is True
        assert json.loads((mirror / "fcop" / "fcop.json").read_text("utf-8"))["workspace_id"] == WORKSPACE_A


def test_c1_offline_01(workspace: WorkspaceFixture, v4_driver: V4ConformanceDriver) -> None:
    # Arrange: one isolated workspace; no registry or second copy exists.
    assert not (workspace.root / "fcop" / "registry.json").exists()

    # Act: perform a local matching create without network uniqueness proof.
    result = v4_driver.create_task(
        test_id="C1-OFFLINE-01", clause="F4.2.6", **_create_kwargs(WORKSPACE_A, "offline-create")
    )

    # Assert: local work succeeds and does not invent a clone-conflict artifact.
    task_id = result_field(result, "task_id")
    assert len(workspace.task_paths(task_id)) == 1
    assert "clone_conflict" not in "\n".join(snapshot_tree(workspace.root)).lower()
