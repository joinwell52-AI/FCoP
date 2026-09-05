"""WP3C trusted authorization, T4-T6, retry, and race proofs."""

from __future__ import annotations

import json
import multiprocessing
from pathlib import Path
from queue import Empty
from typing import Any

import pytest

from fcop import Project
from fcop.errors import V4ProtocolError
from tests.conformance.v4.fixtures import (
    ATTEMPT_A,
    ISSUER_PROOF,
    DeterministicProfileEvaluator,
    WorkspaceFixture,
    _frontmatter,
    bind_t3,
    read_frontmatter,
    snapshot_tree,
)
from tests.conformance.v4.scenarios import (
    authorization_fixture,
    report_request,
    transition_request,
)


class _Allow:
    def __call__(self, *, profile_ref: str, issuer: str, proof: Any) -> str:
        assert profile_ref == "profile:test"
        assert issuer == "ME"
        assert proof == ISSUER_PROOF
        return "AUTHORIZED"


def _arrange(root: Path, edge: str) -> tuple[WorkspaceFixture, dict[str, Any], bytes]:
    workspace = WorkspaceFixture(root).create()
    task_id = f"TASK-WP3C-{edge}"
    source, target, tool = {
        "T4": ("review", "done", "approve_task"),
        "T5": ("review", "active", "reject_task"),
        "T6": ("done", "active", "reopen_task"),
    }[edge]
    workspace.task(task_id, stage=source, attempt_id=ATTEMPT_A)
    report_ref = None
    if edge in {"T4", "T5"}:
        report_ref = f"REPORT-WP3C-{edge}"
        workspace.report(report_ref, task_id=task_id, attempt_id=ATTEMPT_A)
        bind_t3(workspace, task_id, report_ref)
        kind, decision = (
            ("acceptance", "approved") if edge == "T4" else ("rejection", "rejected")
        )
        workspace.review(
            f"REVIEW-WP3C-{edge}",
            task_id=task_id,
            review_kind=kind,
            decision=decision,
            attempt_id=ATTEMPT_A,
            references=[report_ref],
            profile_ref="profile:test",
            transition={"from": source, "to": target},
            authorization_scope="single_use",
        )
    else:
        authorization_fixture(
            workspace,
            "REVIEW-WP3C-T6",
            task_id=task_id,
            from_stage=source,
            to_stage=target,
            attempt_id=ATTEMPT_A,
        )
    request = transition_request(
        task_id,
        source,
        target,
        tool=tool,
        report_ref=report_ref,
        review_ref=f"REVIEW-WP3C-{edge}",
        authorization_ref=f"REVIEW-WP3C-{edge}",
    )
    return workspace, request, workspace.task_paths(task_id)[0].read_bytes()


def _project(root: Path, evaluator: Any | None = None) -> Project:
    return Project(root, trusted_profiles={"profile:test": evaluator or _Allow()})


@pytest.mark.parametrize("edge", ["T4", "T5", "T6"])
def test_authorized_edges_commit_exact_evidence_and_attempts(
    tmp_path: Path, edge: str
) -> None:
    workspace, request, _ = _arrange(tmp_path, edge)
    result = _project(tmp_path).transition(**request)
    task = read_frontmatter(workspace.task_paths(request["task_id"])[0])
    event = task["transitions"][-1]
    assert result["existing"] is False
    assert event["authorization_ref"] == request["authorization_ref"]
    assert len(event["authorization_digest"]) == 64
    assert len(event["evidence_ref"]) == (2 if edge in {"T4", "T5"} else 1)
    assert len(event["evidence_ref"]) == len(event["evidence_digest"])
    if edge == "T4":
        assert result["attempt_id"] == ATTEMPT_A
        assert "attempt_id" not in event
    else:
        assert result["attempt_id"] != ATTEMPT_A
        assert event["attempt_id"] == result["attempt_id"]


@pytest.mark.parametrize("result", ["DENIED", "UNKNOWN", "OTHER"])
def test_only_exact_authorized_result_passes(tmp_path: Path, result: str) -> None:
    workspace, request, _ = _arrange(tmp_path, "T4")

    def evaluator(**kwargs: Any) -> str:
        assert kwargs == {
            "profile_ref": "profile:test", "issuer": "ME", "proof": ISSUER_PROOF,
        }
        return result

    before = snapshot_tree(workspace.root)
    with pytest.raises(V4ProtocolError) as caught:
        _project(tmp_path, evaluator).transition(**request)
    assert caught.value.code == "AUTHORIZATION_INVALID"
    assert snapshot_tree(workspace.root) == before


def test_evaluator_exception_fails_closed(tmp_path: Path) -> None:
    workspace, request, _ = _arrange(tmp_path, "T4")

    def evaluator(**kwargs: Any) -> str:
        del kwargs
        raise RuntimeError("profile unavailable")

    before = snapshot_tree(workspace.root)
    with pytest.raises(V4ProtocolError) as caught:
        _project(tmp_path, evaluator).transition(**request)
    assert caught.value.code == "AUTHORIZATION_INVALID"
    assert snapshot_tree(workspace.root) == before


def test_registry_is_copied_at_initialization(tmp_path: Path) -> None:
    workspace, request, _ = _arrange(tmp_path, "T4")
    denied = DeterministicProfileEvaluator("DENIED")
    registry = {"profile:test": denied}
    project = Project(tmp_path, trusted_profiles=registry)
    registry["profile:test"] = DeterministicProfileEvaluator("AUTHORIZED")
    before = snapshot_tree(workspace.root)
    with pytest.raises(V4ProtocolError) as caught:
        project.transition(**request)
    assert caught.value.code == "AUTHORIZATION_INVALID"
    assert len(denied.calls) == 1
    assert snapshot_tree(workspace.root) == before


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("subject_ref", "TASK-OTHER"),
        ("attempt_id", "urn:uuid:bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"),
        ("transition", {"from": "review", "to": "active"}),
        ("operation_kind", "workspace_admin"),
        ("authorization_scope", "reusable"),
        ("profile_ref", "profile:other"),
        ("decision", "rejected"),
        ("review_kind", "assessment"),
    ],
)
def test_authorization_binding_failures_are_zero_write(
    tmp_path: Path, field: str, value: Any
) -> None:
    workspace, request, _ = _arrange(tmp_path, "T4")
    review = workspace.envelope_paths("REVIEW-WP3C-T4")[0]
    fields = read_frontmatter(review)
    fields[field] = value
    review.write_bytes(_frontmatter(fields, "fixture review"))
    before = snapshot_tree(workspace.root)
    with pytest.raises(V4ProtocolError) as caught:
        _project(tmp_path).transition(**request)
    assert caught.value.code == "AUTHORIZATION_INVALID"
    assert snapshot_tree(workspace.root) == before


def test_t5_old_attempt_report_cannot_satisfy_new_round(tmp_path: Path) -> None:
    workspace, request, _ = _arrange(tmp_path, "T5")
    result = _project(tmp_path).transition(**request)
    before = snapshot_tree(workspace.root)
    with pytest.raises(V4ProtocolError) as caught:
        _project(tmp_path).transition(
            **transition_request(
                request["task_id"], "active", "review", tool="submit_task",
                report_ref="REPORT-WP3C-T5",
            )
        )
    assert caught.value.code == "ATTEMPT_MISMATCH"
    assert result["attempt_id"] != ATTEMPT_A
    assert snapshot_tree(workspace.root) == before


@pytest.mark.parametrize("edge", ["T4", "T5", "T6"])
@pytest.mark.parametrize("state", ["PREPARED", "TARGET_DURABLE", "COMMITTED", "RESPONSE_LOST"])
def test_authorized_receipt_recovery_is_exact_and_single_use(
    tmp_path: Path, edge: str, state: str
) -> None:
    workspace, request, source_bytes = _arrange(tmp_path, edge)
    first = _project(tmp_path).transition(**request)
    receipt_path = workspace.root / first["receipt_ref"]
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert receipt["source_attempt_id"] == ATTEMPT_A
    assert receipt["target_attempt_id"] == first["attempt_id"]
    source = workspace.root / receipt["source_path"]
    target = workspace.root / receipt["target_path"]
    if state == "PREPARED":
        source.write_bytes(source_bytes)
        target.unlink()
        receipt["stage"] = "PREPARED"
    elif state == "TARGET_DURABLE":
        source.write_bytes(source_bytes)
        receipt["stage"] = "TARGET_DURABLE"
    receipt_path.write_text(
        json.dumps(receipt, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    result = _project(tmp_path).transition(**request)
    fields = read_frontmatter(workspace.task_paths(request["task_id"])[0])
    assert result["existing"] is True
    assert len([event for event in fields["transitions"] if event.get("authorization_ref")]) == 1
    assert not source.exists() and target.exists()
    assert json.loads(receipt_path.read_text(encoding="utf-8"))["stage"] == "COMMITTED"


def test_independent_evidence_and_authorization_reviews_are_both_bound(
    tmp_path: Path,
) -> None:
    workspace, request, _ = _arrange(tmp_path, "T4")
    acceptance = workspace.envelope_paths("REVIEW-WP3C-T4")[0]
    fields = read_frontmatter(acceptance)
    for key in (
        "profile_ref", "transition", "issued_at", "expires_at",
        "authorization_scope", "operation_kind", "issuer_proof",
    ):
        fields.pop(key, None)
    acceptance.write_bytes(_frontmatter(fields, "fixture review"))
    authorization_fixture(
        workspace, "REVIEW-WP3C-T4-AUTH", task_id=request["task_id"],
        from_stage="review", to_stage="done", attempt_id=ATTEMPT_A,
    )
    request["authorization_ref"] = "REVIEW-WP3C-T4-AUTH"
    result = _project(tmp_path).transition(**request)
    event = read_frontmatter(Path(result["path"]))["transitions"][-1]
    assert event["evidence_ref"] == ["REPORT-WP3C-T4", "REVIEW-WP3C-T4"]
    assert event["authorization_ref"] == "REVIEW-WP3C-T4-AUTH"


def test_t6_authorization_evidence_must_be_structurally_complete(tmp_path: Path) -> None:
    workspace, request, _ = _arrange(tmp_path, "T6")
    evidence = workspace.envelope_paths("REVIEW-WP3C-T6")[0]
    fields = read_frontmatter(evidence)
    fields.pop("operation_kind")
    evidence.write_bytes(_frontmatter(fields, "fixture review"))
    authorization_fixture(
        workspace, "REVIEW-WP3C-T6-AUTH", task_id=request["task_id"],
        from_stage="done", to_stage="active", attempt_id=ATTEMPT_A,
    )
    request["authorization_ref"] = "REVIEW-WP3C-T6-AUTH"
    before = snapshot_tree(workspace.root)
    with pytest.raises(V4ProtocolError) as caught:
        _project(tmp_path).transition(**request)
    assert caught.value.code == "AUTHORIZATION_INVALID"
    assert snapshot_tree(workspace.root) == before


def test_changed_authorization_bytes_break_exact_retry_without_writes(tmp_path: Path) -> None:
    workspace, request, _ = _arrange(tmp_path, "T6")
    _project(tmp_path).transition(**request)
    authorization = workspace.envelope_paths("REVIEW-WP3C-T6")[0]
    authorization.write_bytes(authorization.read_bytes() + b"changed\n")
    before = snapshot_tree(tmp_path)
    with pytest.raises(V4ProtocolError) as caught:
        _project(tmp_path).transition(**request)
    assert caught.value.code == "EVIDENCE_DIGEST_MISMATCH"
    assert snapshot_tree(tmp_path) == before


@pytest.mark.parametrize("edge", ["T5", "T6"])
def test_historical_authorized_receipts_do_not_block_new_round(
    tmp_path: Path, edge: str
) -> None:
    workspace, request, _ = _arrange(tmp_path, edge)
    first = _project(tmp_path).transition(**request)
    task_id = request["task_id"]
    report = _project(tmp_path).write_report(**report_request(task_id, first["attempt_id"]))
    _project(tmp_path).transition(
        **transition_request(
            task_id, "active", "review", tool="submit_task", report_ref=report["report_id"]
        )
    )
    if edge == "T6":
        workspace.review(
            "REVIEW-WP3C-ROUND-T4", task_id=task_id, review_kind="acceptance",
            decision="approved", attempt_id=first["attempt_id"],
            references=[report["report_id"]], profile_ref="profile:test",
            transition={"from": "review", "to": "done"},
            authorization_scope="single_use",
        )
        _project(tmp_path).transition(
            **transition_request(
                task_id, "review", "done", tool="approve_task",
                report_ref=report["report_id"], review_ref="REVIEW-WP3C-ROUND-T4",
                authorization_ref="REVIEW-WP3C-ROUND-T4",
            )
        )
        review_id = "REVIEW-WP3C-ROUND-T6"
        authorization_fixture(
            workspace, review_id, task_id=task_id, from_stage="done", to_stage="active",
            attempt_id=first["attempt_id"],
        )
        next_request = transition_request(
            task_id, "done", "active", tool="reopen_task",
            review_ref=review_id, authorization_ref=review_id,
        )
    else:
        review_id = "REVIEW-WP3C-ROUND-T5"
        workspace.review(
            review_id, task_id=task_id, review_kind="rejection", decision="rejected",
            attempt_id=first["attempt_id"], references=[report["report_id"]],
            profile_ref="profile:test", transition={"from": "review", "to": "active"},
            authorization_scope="single_use",
        )
        next_request = transition_request(
            task_id, "review", "active", tool="reject_task",
            report_ref=report["report_id"], review_ref=review_id,
            authorization_ref=review_id,
        )
    second = _project(tmp_path).transition(**next_request)
    assert second["attempt_id"] != first["attempt_id"]
    expected_receipts = 3 if edge == "T5" else 4
    assert len(sorted((tmp_path / "fcop/operations").glob("transition-*.json"))) == expected_receipts


def _race_worker(root: str, request: dict[str, Any], start: Any, output: Any) -> None:
    start.wait()
    try:
        output.put(("ok", _project(Path(root)).transition(**request)))
    except BaseException as exc:
        output.put(("error", getattr(exc, "code", type(exc).__name__)))


def test_t4_t5_race_commits_only_one_authorization(tmp_path: Path) -> None:
    workspace, t4, _ = _arrange(tmp_path, "T4")
    task_id = t4["task_id"]
    workspace.review(
        "REVIEW-WP3C-RACE-T5",
        task_id=task_id,
        review_kind="rejection",
        decision="rejected",
        attempt_id=ATTEMPT_A,
        references=["REPORT-WP3C-T4"],
        profile_ref="profile:test",
        transition={"from": "review", "to": "active"},
        authorization_scope="single_use",
    )
    t5 = transition_request(
        task_id, "review", "active", tool="reject_task",
        report_ref="REPORT-WP3C-T4", review_ref="REVIEW-WP3C-RACE-T5",
        authorization_ref="REVIEW-WP3C-RACE-T5",
    )
    context = multiprocessing.get_context("spawn")
    start, output = context.Event(), context.Queue()
    processes = [
        context.Process(target=_race_worker, args=(str(tmp_path), request, start, output))
        for request in (t4, t5)
    ]
    for process in processes:
        process.start()
    start.set()
    results = []
    try:
        for _ in processes:
            results.append(output.get(timeout=20))
    except Empty as exc:
        raise AssertionError("authorization race did not complete") from exc
    finally:
        for process in processes:
            process.join(20)
    assert sorted(item[0] for item in results) == ["error", "ok"]
    paths = workspace.task_paths(task_id)
    assert len(paths) == 1 and paths[0].parent.name in {"active", "done"}
    events = read_frontmatter(paths[0])["transitions"]
    assert len([event for event in events if event.get("authorization_ref")]) == 1


def test_t7_remains_unimplemented_and_zero_write(tmp_path: Path) -> None:
    workspace = WorkspaceFixture(tmp_path).create()
    workspace.task("TASK-WP3C-T7", stage="done", attempt_id=ATTEMPT_A)
    authorization_fixture(
        workspace, "REVIEW-WP3C-T7", task_id="TASK-WP3C-T7",
        from_stage="done", to_stage="archive", attempt_id=ATTEMPT_A,
    )
    before = snapshot_tree(tmp_path)
    with pytest.raises(V4ProtocolError) as caught:
        _project(tmp_path).transition(
            **transition_request(
                "TASK-WP3C-T7", "done", "archive", tool="archive_task",
                authorization_ref="REVIEW-WP3C-T7",
            )
        )
    assert caught.value.code == "toolkit:OPERATION_NOT_IMPLEMENTED"
    assert snapshot_tree(tmp_path) == before
