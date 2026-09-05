"""WP3D canonical family, convergence, T7, retry, and race proofs."""

from __future__ import annotations

import multiprocessing
import os
from pathlib import Path
from queue import Empty
from typing import Any

import pytest

from fcop import Project
from fcop.errors import V4ProtocolError
from tests.conformance.v4.driver import run_concurrent_operations
from tests.conformance.v4.fixtures import (
    ATTEMPT_A,
    ATTEMPT_B,
    DeterministicProfileEvaluator,
    WorkspaceFixture,
    canonical_family_digest,
    read_frontmatter,
    sha256_bytes,
    snapshot_tree,
)
from tests.conformance.v4.scenarios import (
    authorization_fixture,
    create_request,
    report_request,
    review_request,
    transition_request,
)


def _race_worker(
    root: str,
    start: Any,
    output: Any,
    action: str,
    request: dict[str, Any],
) -> None:
    project = _project(Path(root))
    start.wait()
    try:
        result = getattr(project, action)(**request)
        output.put(("ok", result))
    except BaseException as exc:  # pragma: no cover - child-process evidence
        output.put(("error", getattr(exc, "code", type(exc).__name__)))


def _race(
    root: Path, operations: list[tuple[str, dict[str, Any]]]
) -> list[tuple[str, Any]]:
    context = multiprocessing.get_context("spawn")
    start, output = context.Event(), context.Queue()
    workers = [
        context.Process(
            target=_race_worker,
            args=(str(root), start, output, action, request),
        )
        for action, request in operations
    ]
    for worker in workers:
        worker.start()
    start.set()
    results: list[tuple[str, Any]] = []
    try:
        for _ in workers:
            results.append(output.get(timeout=30))
    except Empty as exc:
        raise AssertionError("WP3D race worker returned no result") from exc
    finally:
        for worker in workers:
            worker.join(30)
            if worker.is_alive():
                worker.terminate()
                worker.join(5)
                raise AssertionError("WP3D race worker timed out")
    return results


def _project(root: Path, decision: str = "AUTHORIZED") -> Project:
    return Project(
        root,
        trusted_profiles={"profile:test": DeterministicProfileEvaluator(decision)},
    )


def _family(root: Path) -> tuple[WorkspaceFixture, list[dict[str, str]], str]:
    workspace = WorkspaceFixture(root).create()
    workspace.task("TASK-ROOT", stage="done", attempt_id=ATTEMPT_A)
    workspace.task(
        "TASK-B", stage="done", attempt_id=ATTEMPT_B, branch_of="TASK-ROOT"
    )
    workspace.task(
        "TASK-A", stage="done", attempt_id=ATTEMPT_A, branch_of="TASK-ROOT"
    )
    report_b = workspace.report(
        "REPORT-B", task_id="TASK-B", attempt_id=ATTEMPT_B, body="B\n"
    )
    report_a = workspace.report(
        "REPORT-A", task_id="TASK-A", attempt_id=ATTEMPT_A, body="A\n"
    )
    entries = [
        {
            "branch_task_id": "TASK-B",
            "attempt_id": ATTEMPT_B,
            "report_id": "REPORT-B",
            "report_digest": sha256_bytes(report_b.read_bytes()),
        },
        {
            "branch_task_id": "TASK-A",
            "attempt_id": ATTEMPT_A,
            "report_id": "REPORT-A",
            "report_digest": sha256_bytes(report_a.read_bytes()),
        },
    ]
    return workspace, entries, canonical_family_digest("TASK-ROOT", entries)


def _converged(root: Path) -> tuple[WorkspaceFixture, Project, str, str]:
    workspace, entries, expected = _family(root)
    project = _project(root)
    result = project.write_review(
        **review_request(
            "TASK-ROOT",
            review_kind="convergence",
            decision="approved",
            family_digest=expected,
            references=[item["report_id"] for item in entries],
        )
    )
    return workspace, project, expected, result["review_id"]


def test_family_digest_matches_independent_oracle_and_ignores_path_mtime(
    tmp_path: Path,
) -> None:
    workspace, _, expected = _family(tmp_path)
    project = _project(tmp_path)
    assert project.family_digest(root_task_id="TASK-ROOT") == expected
    branch = workspace.task_paths("TASK-B")[0]
    os.utime(branch, (1, 1))
    branch.replace(branch.parent.parent / "archive" / branch.name)
    assert project.family_digest(root_task_id="TASK-ROOT") == expected


def test_replacement_changes_digest_and_old_report_remains(tmp_path: Path) -> None:
    workspace, _, old = _family(tmp_path)
    project = _project(tmp_path)
    project.write_report(
        **report_request(
            "TASK-A",
            ATTEMPT_A,
            report_kind="replacement",
            references=["REPORT-A"],
            body="replacement\n",
        )
    )
    assert project.family_digest(root_task_id="TASK-ROOT") != old
    assert workspace.envelope_paths("REPORT-A")[0].is_file()


@pytest.mark.parametrize("case", ["missing-root", "branch-subject", "duplicate-branch"])
def test_family_identity_fails_closed(tmp_path: Path, case: str) -> None:
    workspace, _, _ = _family(tmp_path)
    subject = "TASK-MISSING" if case == "missing-root" else "TASK-A"
    if case == "duplicate-branch":
        original = workspace.task_paths("TASK-A")[0]
        duplicate = original.parent.parent / "archive" / original.name
        duplicate.write_bytes(original.read_bytes())
        subject = "TASK-ROOT"
    with pytest.raises(V4ProtocolError) as caught:
        _project(tmp_path).family_digest(root_task_id=subject)
    assert caught.value.code in {"RELATION_INVALID", "STATE_AMBIGUOUS"}


@pytest.mark.parametrize("case", ["missing", "extra", "duplicate", "wrong-digest"])
def test_convergence_rejects_nonexact_snapshot(tmp_path: Path, case: str) -> None:
    workspace, entries, expected = _family(tmp_path)
    refs = [item["report_id"] for item in entries]
    if case == "missing":
        refs.pop()
    elif case == "extra":
        workspace.task("TASK-OTHER", stage="done", attempt_id=ATTEMPT_A)
        workspace.report("REPORT-EXTRA", task_id="TASK-OTHER", attempt_id=ATTEMPT_A)
        refs.append("REPORT-EXTRA")
    elif case == "duplicate":
        refs.append(refs[0])
    digest_value = "0" * 64 if case == "wrong-digest" else expected
    before = snapshot_tree(tmp_path)
    with pytest.raises(V4ProtocolError) as caught:
        _project(tmp_path).write_review(
            **review_request(
                "TASK-ROOT",
                review_kind="convergence",
                decision="approved",
                family_digest=digest_value,
                references=refs,
            )
        )
    assert caught.value.code == "FAMILY_CONVERGENCE_MISMATCH"
    assert snapshot_tree(tmp_path) == before


def test_root_without_branches_cannot_record_convergence(tmp_path: Path) -> None:
    workspace = WorkspaceFixture(tmp_path).create()
    workspace.task("TASK-ROOT", stage="done", attempt_id=ATTEMPT_A)
    with pytest.raises(V4ProtocolError) as caught:
        _project(tmp_path).write_review(
            **review_request(
                "TASK-ROOT",
                review_kind="convergence",
                decision="approved",
                family_digest=canonical_family_digest("TASK-ROOT", []),
            )
        )
    assert caught.value.code == "FAMILY_CONVERGENCE_REQUIRED"


def test_root_t7_binds_digest_evidence_and_exact_retry(tmp_path: Path) -> None:
    workspace, project, family_digest, convergence_ref = _converged(tmp_path)
    authorization_fixture(
        workspace,
        "REVIEW-AUTH",
        task_id="TASK-ROOT",
        from_stage="done",
        to_stage="archive",
        attempt_id=ATTEMPT_A,
        family_digest=family_digest,
    )
    request = transition_request(
        "TASK-ROOT",
        "done",
        "archive",
        tool="archive_task",
        review_ref=convergence_ref,
        authorization_ref="REVIEW-AUTH",
        family_digest=family_digest,
    )
    first = project.transition(**request)
    after = snapshot_tree(tmp_path)
    retry = project.transition(**request)
    assert first["existing"] is False and retry["existing"] is True
    assert snapshot_tree(tmp_path) == after
    fields = read_frontmatter(workspace.task_paths("TASK-ROOT")[0])
    event = fields["transitions"][-1]
    assert event["attempt_id"] == ATTEMPT_A
    assert event["family_digest"] == family_digest
    assert event["evidence_ref"][0] == convergence_ref
    assert event["evidence_ref"][1:] == ["REPORT-A", "REPORT-B"]
    assert len(event["evidence_ref"]) == len(event["evidence_digest"])


def test_archived_root_freezes_branch_report_head(tmp_path: Path) -> None:
    workspace, project, family_digest, convergence_ref = _converged(tmp_path)
    authorization_fixture(
        workspace,
        "REVIEW-AUTH",
        task_id="TASK-ROOT",
        from_stage="done",
        to_stage="archive",
        attempt_id=ATTEMPT_A,
        family_digest=family_digest,
    )
    project.transition(
        **transition_request(
            "TASK-ROOT",
            "done",
            "archive",
            tool="archive_task",
            review_ref=convergence_ref,
            authorization_ref="REVIEW-AUTH",
            family_digest=family_digest,
        )
    )
    before = snapshot_tree(tmp_path)
    with pytest.raises(V4ProtocolError) as caught:
        project.write_report(
            **report_request(
                "TASK-A",
                ATTEMPT_A,
                report_kind="replacement",
                references=["REPORT-A"],
            )
        )
    assert caught.value.code == "INVALID_TRANSITION"
    assert snapshot_tree(tmp_path) == before


def test_archived_root_blocks_branch_reopen(tmp_path: Path) -> None:
    workspace, project, family_digest, convergence_ref = _converged(tmp_path)
    authorization_fixture(
        workspace,
        "REVIEW-ROOT-AUTH",
        task_id="TASK-ROOT",
        from_stage="done",
        to_stage="archive",
        attempt_id=ATTEMPT_A,
        family_digest=family_digest,
    )
    authorization_fixture(
        workspace,
        "REVIEW-BRANCH-REOPEN",
        task_id="TASK-A",
        from_stage="done",
        to_stage="active",
        attempt_id=ATTEMPT_A,
    )
    project.transition(
        **transition_request(
            "TASK-ROOT",
            "done",
            "archive",
            tool="archive_task",
            review_ref=convergence_ref,
            authorization_ref="REVIEW-ROOT-AUTH",
            family_digest=family_digest,
        )
    )
    before = snapshot_tree(tmp_path)
    with pytest.raises(V4ProtocolError) as caught:
        project.transition(
            **transition_request(
                "TASK-A",
                "done",
                "active",
                tool="reopen_task",
                review_ref="REVIEW-BRANCH-REOPEN",
                authorization_ref="REVIEW-BRANCH-REOPEN",
            )
        )
    assert caught.value.code == "INVALID_TRANSITION"
    assert snapshot_tree(tmp_path) == before


@pytest.mark.parametrize("decision", ["DENIED", "UNKNOWN"])
def test_t7_profile_denial_is_atomic(tmp_path: Path, decision: str) -> None:
    workspace = WorkspaceFixture(tmp_path).create()
    workspace.task("TASK-T7", stage="done", attempt_id=ATTEMPT_A)
    authorization_fixture(
        workspace,
        "REVIEW-T7",
        task_id="TASK-T7",
        from_stage="done",
        to_stage="archive",
        attempt_id=ATTEMPT_A,
    )
    before = snapshot_tree(tmp_path)
    with pytest.raises(V4ProtocolError) as caught:
        _project(tmp_path, decision).transition(
            **transition_request(
                "TASK-T7",
                "done",
                "archive",
                tool="archive_task",
                authorization_ref="REVIEW-T7",
            )
        )
    assert caught.value.code == "AUTHORIZATION_INVALID"
    assert snapshot_tree(tmp_path) == before


def test_branch_t7_keeps_family_digest_stable(tmp_path: Path) -> None:
    workspace, _, expected = _family(tmp_path)
    authorization_fixture(
        workspace,
        "REVIEW-BRANCH-AUTH",
        task_id="TASK-A",
        from_stage="done",
        to_stage="archive",
        attempt_id=ATTEMPT_A,
    )
    project = _project(tmp_path)
    project.transition(
        **transition_request(
            "TASK-A",
            "done",
            "archive",
            tool="archive_task",
            authorization_ref="REVIEW-BRANCH-AUTH",
        )
    )
    assert project.family_digest(root_task_id="TASK-ROOT") == expected


def test_replacement_and_convergence_are_cross_process_linearizable(tmp_path: Path) -> None:
    workspace, entries, old = _family(tmp_path)
    commands = [
        {
            "action": "write_report",
            "kwargs": {
                "test_id": "WP3D-RACE",
                "clause": "F4.6.6-F4.6.8; F4.9.5",
                **report_request(
                    "TASK-A",
                    ATTEMPT_A,
                    report_kind="replacement",
                    references=["REPORT-A"],
                    body="new\n",
                ),
            },
        },
        {
            "action": "write_review",
            "kwargs": {
                "test_id": "WP3D-RACE",
                "clause": "F4.6.6-F4.6.8; F4.9.5",
                **review_request(
                    "TASK-ROOT",
                    review_kind="convergence",
                    decision="approved",
                    family_digest=old,
                    references=[item["report_id"] for item in entries],
                ),
            },
        },
    ]
    results = run_concurrent_operations(workspace.root, commands)
    assert all(item["status"] in {"returned", "error"} for item in results)
    current = _project(tmp_path).family_digest(root_task_id="TASK-ROOT")
    reviews = [
        read_frontmatter(path)
        for path in (tmp_path / "fcop/reviews").glob("REVIEW-*.md")
        if read_frontmatter(path).get("review_kind") == "convergence"
    ]
    assert not reviews or reviews[0]["family_digest"] in {old, current}


def test_root_t7_and_branch_reopen_have_one_cross_process_winner(tmp_path: Path) -> None:
    workspace, project, family_digest, convergence_ref = _converged(tmp_path)
    authorization_fixture(
        workspace, "REVIEW-ROOT-AUTH", task_id="TASK-ROOT",
        from_stage="done", to_stage="archive", attempt_id=ATTEMPT_A,
        family_digest=family_digest,
    )
    authorization_fixture(
        workspace, "REVIEW-BRANCH-REOPEN", task_id="TASK-A",
        from_stage="done", to_stage="active", attempt_id=ATTEMPT_A,
    )
    del project
    results = _race(
        tmp_path,
        [
            (
                "transition",
                transition_request(
                    "TASK-ROOT", "done", "archive", tool="archive_task",
                    review_ref=convergence_ref,
                    authorization_ref="REVIEW-ROOT-AUTH",
                    family_digest=family_digest,
                ),
            ),
            (
                "transition",
                transition_request(
                    "TASK-A", "done", "active", tool="reopen_task",
                    review_ref="REVIEW-BRANCH-REOPEN",
                    authorization_ref="REVIEW-BRANCH-REOPEN",
                ),
            ),
        ],
    )
    assert sorted(item[0] for item in results) == ["error", "ok"]
    root_stage = workspace.task_paths("TASK-ROOT")[0].parent.name
    branch_stage = workspace.task_paths("TASK-A")[0].parent.name
    assert (root_stage, branch_stage) in {("archive", "done"), ("done", "active")}


def test_root_t7_and_branch_replacement_have_one_cross_process_winner(
    tmp_path: Path,
) -> None:
    workspace, project, family_digest, convergence_ref = _converged(tmp_path)
    authorization_fixture(
        workspace, "REVIEW-ROOT-AUTH", task_id="TASK-ROOT",
        from_stage="done", to_stage="archive", attempt_id=ATTEMPT_A,
        family_digest=family_digest,
    )
    del project
    results = _race(
        tmp_path,
        [
            (
                "transition",
                transition_request(
                    "TASK-ROOT", "done", "archive", tool="archive_task",
                    review_ref=convergence_ref,
                    authorization_ref="REVIEW-ROOT-AUTH",
                    family_digest=family_digest,
                ),
            ),
            (
                "write_report",
                report_request(
                    "TASK-A", ATTEMPT_A, report_kind="replacement",
                    references=["REPORT-A"], body="raced replacement\n",
                ),
            ),
        ],
    )
    assert sorted(item[0] for item in results) == ["error", "ok"]
    if workspace.task_paths("TASK-ROOT")[0].parent.name == "archive":
        assert len(workspace.envelope_paths("REPORT-A")) == 1
    else:
        assert workspace.task_paths("TASK-ROOT")[0].parent.name == "done"
        assert len(list((tmp_path / "fcop/reports").glob("REPORT-*.md"))) == 3


def test_branch_t7_and_root_t7_both_commit_under_one_family_lock(tmp_path: Path) -> None:
    workspace, project, family_digest, convergence_ref = _converged(tmp_path)
    authorization_fixture(
        workspace, "REVIEW-ROOT-AUTH", task_id="TASK-ROOT",
        from_stage="done", to_stage="archive", attempt_id=ATTEMPT_A,
        family_digest=family_digest,
    )
    authorization_fixture(
        workspace, "REVIEW-BRANCH-AUTH", task_id="TASK-B",
        from_stage="done", to_stage="archive", attempt_id=ATTEMPT_B,
    )
    del project
    results = _race(
        tmp_path,
        [
            (
                "transition",
                transition_request(
                    "TASK-ROOT", "done", "archive", tool="archive_task",
                    review_ref=convergence_ref,
                    authorization_ref="REVIEW-ROOT-AUTH",
                    family_digest=family_digest,
                ),
            ),
            (
                "transition",
                transition_request(
                    "TASK-B", "done", "archive", tool="archive_task",
                    authorization_ref="REVIEW-BRANCH-AUTH",
                ),
            ),
        ],
    )
    assert [item[0] for item in results].count("ok") == 2
    assert workspace.task_paths("TASK-ROOT")[0].parent.name == "archive"
    assert workspace.task_paths("TASK-B")[0].parent.name == "archive"


def test_two_root_t7_calls_converge_on_one_receipt(tmp_path: Path) -> None:
    workspace, project, family_digest, convergence_ref = _converged(tmp_path)
    authorization_fixture(
        workspace, "REVIEW-ROOT-AUTH", task_id="TASK-ROOT",
        from_stage="done", to_stage="archive", attempt_id=ATTEMPT_A,
        family_digest=family_digest,
    )
    del project
    request = transition_request(
        "TASK-ROOT", "done", "archive", tool="archive_task",
        review_ref=convergence_ref, authorization_ref="REVIEW-ROOT-AUTH",
        family_digest=family_digest,
    )
    results = _race(tmp_path, [("transition", request), ("transition", request)])
    assert [item[0] for item in results].count("ok") == 2
    assert sorted(item[1]["existing"] for item in results) == [False, True]
    fields = read_frontmatter(workspace.task_paths("TASK-ROOT")[0])
    assert sum(event.get("to") == "archive" for event in fields["transitions"]) == 1


def test_root_t7_race_cannot_create_branch_below_done_root(tmp_path: Path) -> None:
    workspace, project, family_digest, convergence_ref = _converged(tmp_path)
    authorization_fixture(
        workspace, "REVIEW-ROOT-AUTH", task_id="TASK-ROOT",
        from_stage="done", to_stage="archive", attempt_id=ATTEMPT_A,
        family_digest=family_digest,
    )
    del project
    create = create_request("wp3d-root-branch-race", branch_of="TASK-ROOT")
    results = _race(
        tmp_path,
        [
            (
                "transition",
                transition_request(
                    "TASK-ROOT", "done", "archive", tool="archive_task",
                    review_ref=convergence_ref,
                    authorization_ref="REVIEW-ROOT-AUTH",
                    family_digest=family_digest,
                ),
            ),
            ("create_task", create),
        ],
    )
    assert sorted(item[0] for item in results) == ["error", "ok"]
    assert workspace.task_paths("TASK-ROOT")[0].parent.name == "archive"
    assert not any(
        read_frontmatter(path).get("branch_of") == "TASK-ROOT"
        for path in (tmp_path / "fcop/_lifecycle").glob("*/*.md")
        if path.stem not in {"TASK-A", "TASK-B"}
    )


def test_t7_authorization_race_cannot_consume_a_different_edge(tmp_path: Path) -> None:
    workspace = WorkspaceFixture(tmp_path).create()
    workspace.task("TASK-AUTH-RACE", stage="done", attempt_id=ATTEMPT_A)
    authorization_fixture(
        workspace, "REVIEW-AUTH-RACE", task_id="TASK-AUTH-RACE",
        from_stage="done", to_stage="archive", attempt_id=ATTEMPT_A,
    )
    results = _race(
        tmp_path,
        [
            (
                "transition",
                transition_request(
                    "TASK-AUTH-RACE", "done", "archive", tool="archive_task",
                    authorization_ref="REVIEW-AUTH-RACE",
                ),
            ),
            (
                "transition",
                transition_request(
                    "TASK-AUTH-RACE", "done", "active", tool="reopen_task",
                    review_ref="REVIEW-AUTH-RACE",
                    authorization_ref="REVIEW-AUTH-RACE",
                ),
            ),
        ],
    )
    assert sorted(item[0] for item in results) == ["error", "ok"]
    assert workspace.task_paths("TASK-AUTH-RACE")[0].parent.name == "archive"
    fields = read_frontmatter(workspace.task_paths("TASK-AUTH-RACE")[0])
    assert sum(
        event.get("authorization_ref") == "REVIEW-AUTH-RACE"
        for event in fields["transitions"]
    ) == 1
