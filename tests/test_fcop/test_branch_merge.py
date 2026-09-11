"""4.0.1 atomic merge acceptance, including real processes and crash recovery."""

from __future__ import annotations

import json
import multiprocessing
import os
from pathlib import Path
from typing import Any

import pytest

from fcop import Project
from fcop.errors import FcopError
from tests.conformance.v4.fixtures import snapshot_tree
from tests.test_fcop.test_v4_convergence import _family, _project


def _worker(root: str, barrier: Any, output: Any, action: str, req: dict[str, Any]) -> None:
    project = _project(Path(root))
    barrier.wait(timeout=25)
    try:
        output.put(("ok", getattr(project, action)(**req)))
    except FcopError as exc:
        output.put(("error", exc.code))


def _race(root: Path, operations: list[tuple[str, dict[str, Any]]]) -> list[tuple[str, Any]]:
    context = multiprocessing.get_context("spawn")
    barrier, output = context.Barrier(len(operations)), context.Queue()
    workers = [
        context.Process(target=_worker, args=(str(root), barrier, output, action, req))
        for action, req in operations
    ]
    for worker in workers:
        worker.start()
    try:
        return [output.get(timeout=35) for _ in workers]
    finally:
        for worker in workers:
            worker.join(5)
            if worker.is_alive():
                worker.kill()
                worker.join()
            assert worker.exitcode == 0


def test_concurrent_branch_creation_reuses_core_operation(tmp_path: Path) -> None:
    from tests.conformance.v4.fixtures import ATTEMPT_A, WorkspaceFixture

    workspace = WorkspaceFixture(tmp_path).create()
    workspace.task("TASK-ROOT", stage="active", attempt_id=ATTEMPT_A)
    req = dict(
        workspace_id=workspace.workspace_id,
        operation_id="branch-once",
        sender="ME",
        recipient="ME",
        subject="Branch",
        body="Parallel",
        branch_of="TASK-ROOT",
    )
    results = _race(tmp_path, [("create_task", req), ("create_task", req)])
    assert all(status == "ok" for status, _ in results)
    assert len({result["task_id"] for _, result in results}) == 1
    assert sum(not result["existing"] for _, result in results) == 1
    family = Project(tmp_path).inspect_family(root_task_id="TASK-ROOT")
    assert len(family["branches"]) == 1 and family["family_digest"] is None


def request(root: Path) -> dict[str, Any]:
    workspace, entries, digest = _family(root)
    return dict(
        workspace_id=workspace.workspace_id,
        root_task_id="TASK-ROOT",
        expected_family_digest=digest,
        branch_report_heads={r["branch_task_id"]: r["report_id"] for r in entries},
        conclusion="Both results accepted",
        conflict_resolution="No conflicts",
        operation_id="merge-once",
        sender="ME",
        recipient="ME",
    )


def legacy(req: dict[str, Any]) -> dict[str, Any]:
    return dict(
        workspace_id=req["workspace_id"],
        sender=req["sender"],
        recipient=req["recipient"],
        subject_ref=req["root_task_id"],
        review_kind="convergence",
        decision="approved",
        family_digest=req["expected_family_digest"],
        references=list(req["branch_report_heads"].values()),
        body="## Merge conclusion\n\nBoth results accepted\n\n## Conflict resolution\n\nNo conflicts\n",
    )


def test_inspect_readonly_precise_and_stable(tmp_path: Path) -> None:
    req = request(tmp_path)
    before = snapshot_tree(tmp_path)
    family = _project(tmp_path).inspect_family(root_task_id="TASK-ROOT")
    assert snapshot_tree(tmp_path) == before
    assert family["family_digest"] == req["expected_family_digest"]
    assert family["merge_ready"] and family["reasons"] == []
    assert [b["task_id"] for b in family["branches"]] == ["TASK-A", "TASK-B"]
    assert {b["task_id"]: b["report_head"]["report_id"] for b in family["branches"]} == req[
        "branch_report_heads"
    ]


@pytest.mark.parametrize(
    "stage,code", [("inbox", "ATTEMPT_MISMATCH"), ("active", "REPORT_REQUIRED")]
)
def test_partial_digest_is_null(tmp_path: Path, stage: str, code: str) -> None:
    from tests.conformance.v4.fixtures import ATTEMPT_A, WorkspaceFixture

    fixture = WorkspaceFixture(tmp_path).create()
    fixture.task("TASK-ROOT", stage="active", attempt_id=ATTEMPT_A)
    fixture.task(
        "TASK-B",
        stage=stage,
        branch_of="TASK-ROOT",
        **({"attempt_id": ATTEMPT_A} if stage == "active" else {}),
    )
    before = snapshot_tree(tmp_path)
    result = _project(tmp_path).inspect_family(root_task_id="TASK-ROOT")
    assert result["family_digest"] is None and result["merge_ready"] is False
    assert code in {r["code"] for r in result["reasons"]}
    assert "BRANCH_NOT_TERMINAL" in {r["code"] for r in result["reasons"]}
    assert snapshot_tree(tmp_path) == before


@pytest.mark.parametrize(
    "change,code",
    [
        ({"expected_family_digest": None}, "FAMILY_CONVERGENCE_MISMATCH"),
        ({"expected_family_digest": "0" * 64}, "FAMILY_CONVERGENCE_MISMATCH"),
        ({"branch_report_heads": {"TASK-A": "REPORT-A"}}, "FAMILY_CONVERGENCE_MISMATCH"),
        (
            {"branch_report_heads": {"TASK-A": "REPORT-old", "TASK-B": "REPORT-B"}},
            "FAMILY_CONVERGENCE_MISMATCH",
        ),
        (
            {"branch_report_heads": {"TASK-A": "REPORT-B", "TASK-B": "REPORT-A"}},
            "FAMILY_CONVERGENCE_MISMATCH",
        ),
        ({"conclusion": ""}, "INVALID_ENVELOPE"),
    ],
)
def test_rejected_request_is_zero_write(tmp_path: Path, change: dict[str, Any], code: str) -> None:
    req = request(tmp_path)
    before = snapshot_tree(tmp_path)
    with pytest.raises(FcopError) as exc:
        _project(tmp_path).merge_branches(**{**req, **change})
    assert exc.value.code == code
    assert snapshot_tree(tmp_path) == before


def test_idempotency_conflict_and_legacy_unification(tmp_path: Path) -> None:
    req = request(tmp_path)
    project = _project(tmp_path)
    first = project.merge_branches(**req)
    assert first["existing"] is False
    assert first["old_family_digest"] == first["new_family_digest"] == req["expected_family_digest"]
    assert project.inspect_state(task_id="TASK-ROOT")["stage"] == "done"
    before = snapshot_tree(tmp_path)
    replay = Project(tmp_path).merge_branches(**req)
    assert replay["existing"] and replay["review_id"] == first["review_id"]
    assert snapshot_tree(tmp_path) == before
    with pytest.raises(FcopError) as exc:
        project.merge_branches(**{**req, "conclusion": "Different"})
    assert exc.value.code == "OPERATION_ID_CONFLICT"
    assert snapshot_tree(tmp_path) == before
    with pytest.raises(FcopError) as exc:
        project.merge_branches(**{**req, "operation_id": "other", "conclusion": "Different"})
    assert exc.value.code == "FAMILY_CONVERGENCE_MISMATCH"
    assert snapshot_tree(tmp_path) == before
    assert project.write_review(**legacy(req))["review_id"] == first["review_id"]
    assert project.merge_branches(**{**req, "operation_id": "alias"})["existing"]
    assert len(project.inspect_family(root_task_id="TASK-ROOT")["convergence_reviews"]) == 1


@pytest.mark.parametrize(
    "mode", ["same-operation", "different-operation", "legacy", "different-content"]
)
def test_real_cross_process_merge(tmp_path: Path, mode: str) -> None:
    req = request(tmp_path)
    second = {**req, "operation_id": "other"} if mode != "same-operation" else req
    if mode == "different-content":
        second["conclusion"] = "Competing decision"
    action = ("write_review", legacy(req)) if mode == "legacy" else ("merge_branches", second)
    results = _race(tmp_path, [("merge_branches", req), action])
    successes = [result for status, result in results if status == "ok"]
    assert len({r["review_id"] for r in successes}) == 1
    assert sum(not r["existing"] for r in successes) == 1
    if mode == "different-content":
        assert [r for status, r in results if status == "error"] == ["FAMILY_CONVERGENCE_MISMATCH"]
    else:
        assert len(successes) == 2
    assert (
        len(_project(tmp_path).inspect_family(root_task_id="TASK-ROOT")["convergence_reviews"]) == 1
    )


def _crash(root: str, req: dict[str, Any], stage: str) -> None:
    project = Project(root)
    creation = project._v4_creation

    def kill(operation: str, boundary: str) -> None:
        if operation == "merge_branches" and boundary == stage:
            os._exit(71)

    creation._trigger_fault = kill
    project.merge_branches(**req)


@pytest.mark.parametrize("stage", ["PREPARED", "TARGET_DURABLE", "COMMITTED", "RESPONSE_LOST"])
def test_process_death_and_restart(tmp_path: Path, stage: str) -> None:
    req = request(tmp_path)
    process = multiprocessing.get_context("spawn").Process(
        target=_crash, args=(str(tmp_path), req, stage)
    )
    process.start()
    process.join(30)
    if process.is_alive():
        process.kill()
        process.join()
        pytest.fail("Crash probe timed out")
    assert process.exitcode == 71
    receipt = json.loads(next((tmp_path / "fcop/operations").glob("merge-*.json")).read_text())
    result = Project(tmp_path).merge_branches(**req)
    assert result["existing"] and result["review_id"] == receipt["review_id"]
    assert len(list((tmp_path / "fcop/reviews").glob("REVIEW-*.md"))) == 1
    before = snapshot_tree(tmp_path)
    assert Project(tmp_path).merge_branches(**req)["review_id"] == result["review_id"]
    assert snapshot_tree(tmp_path) == before


def test_corrupt_receipt_and_missing_review_fail_closed(tmp_path: Path) -> None:
    req = request(tmp_path)
    result = Project(tmp_path).merge_branches(**req)
    Path(result["path"]).unlink()
    before = snapshot_tree(tmp_path)
    with pytest.raises(FcopError) as exc:
        Project(tmp_path).merge_branches(**req)
    assert exc.value.code == "RECOVERY_REQUIRED"
    assert snapshot_tree(tmp_path) == before


def test_nonterminal_branch_zero_side_effect(tmp_path: Path) -> None:
    req = request(tmp_path)
    path = tmp_path / "fcop/_lifecycle/done/TASK-A.md"
    path.replace(tmp_path / "fcop/_lifecycle/review/TASK-A.md")
    before = snapshot_tree(tmp_path)
    family = Project(tmp_path).inspect_family(root_task_id="TASK-ROOT")
    assert not family["merge_ready"]
    with pytest.raises(FcopError) as exc:
        Project(tmp_path).merge_branches(**req)
    assert exc.value.code in {"BRANCH_NOT_TERMINAL", "STATE_AMBIGUOUS"}
    assert snapshot_tree(tmp_path) == before


@pytest.mark.parametrize("damage", ["hash", "alias", "copy"])
def test_receipt_damage_is_not_repaired_by_guessing(tmp_path: Path, damage: str) -> None:
    req = request(tmp_path)
    Project(tmp_path).merge_branches(**req)
    path = next((tmp_path / "fcop/operations").glob("merge-*.json"))
    value = json.loads(path.read_text(encoding="utf-8"))
    if damage == "copy":
        path.with_name("merge-copy.json").write_bytes(path.read_bytes())
    else:
        if damage == "hash":
            value["content_digest"] = "0" * 64
        else:
            value["operations"].append(value["operations"][0])
        path.write_bytes((json.dumps(value) + "\n").encode())
    before = snapshot_tree(tmp_path)
    with pytest.raises(FcopError) as exc:
        Project(tmp_path).merge_branches(**req)
    assert exc.value.code == "RECOVERY_REQUIRED"
    assert snapshot_tree(tmp_path) == before


def test_historical_single_equivalent_review_is_preserved(tmp_path: Path) -> None:
    from fcop.v4.encoding import envelope_bytes, publish

    req = request(tmp_path)
    project = Project(tmp_path)
    # Simulate an existing 4.0.0 append, with no operation receipt.
    fields = project._v4_creation._common("REVIEW", "ME", "ME")
    fields.update({k: v for k, v in legacy(req).items() if k != "body"})
    path = tmp_path / "fcop/reviews" / (fields["review_id"] + ".md")
    publish(path, envelope_bytes(fields, legacy(req)["body"]))
    original = path.read_bytes()
    result = project.merge_branches(**req)
    assert result["existing"] and result["review_id"] == fields["review_id"]
    assert path.read_bytes() == original
    assert len(list(path.parent.glob("REVIEW-*.md"))) == 1
    assert Project(tmp_path).merge_branches(**req)["review_id"] == fields["review_id"]


def test_actual_replacement_report_invalidates_old_head(tmp_path: Path) -> None:
    from tests.conformance.v4.fixtures import ATTEMPT_A

    req = request(tmp_path)
    project = _project(tmp_path)
    project.write_report(
        workspace_id=req["workspace_id"],
        sender="ME",
        recipient="ME",
        subject_ref="TASK-A",
        attempt_id=ATTEMPT_A,
        report_kind="replacement",
        references=["REPORT-A"],
        result="done",
        body="Revised result",
    )
    current = project.inspect_family(root_task_id="TASK-ROOT")["family_digest"]
    assert current != req["expected_family_digest"]
    before = snapshot_tree(tmp_path)
    for digest in (req["expected_family_digest"], current):
        with pytest.raises(FcopError) as exc:
            project.merge_branches(**{**req, "expected_family_digest": digest})
        assert exc.value.code == "FAMILY_CONVERGENCE_MISMATCH"
        assert snapshot_tree(tmp_path) == before
