"""C5 attempts, REPORT heads, convergence, digest, and real races."""

from __future__ import annotations

import os

import pytest

from .driver import (
    V4ConformanceDriver, capture_error, digest_value, error_code, result_field,
    run_concurrent_operations,
)
from .fixtures import (
    ATTEMPT_A, ATTEMPT_B, WorkspaceFixture, canonical_family_digest,
    read_frontmatter, sha256_bytes, snapshot_tree,
)
from .scenarios import (
    assert_task_stage, authorization_fixture, create_request, report_request,
    review_request, transition_request,
)


def _family(workspace: WorkspaceFixture, *, second_state: str = "done") -> tuple[list[dict[str, str]], str]:
    workspace.task("TASK-C5-ROOT", stage="done", attempt_id=ATTEMPT_A)
    workspace.task("TASK-C5-B", stage="done", attempt_id=ATTEMPT_B, branch_of="TASK-C5-ROOT")
    workspace.task("TASK-C5-A", stage=second_state, attempt_id=ATTEMPT_A, branch_of="TASK-C5-ROOT")
    report_b = workspace.report("REPORT-C5-B", task_id="TASK-C5-B", attempt_id=ATTEMPT_B, body="B\n")
    report_a = workspace.report("REPORT-C5-A", task_id="TASK-C5-A", attempt_id=ATTEMPT_A, body="A\n")
    entries = [
        {"branch_task_id": "TASK-C5-B", "attempt_id": ATTEMPT_B,
         "report_id": "REPORT-C5-B", "report_digest": sha256_bytes(report_b.read_bytes())},
        {"branch_task_id": "TASK-C5-A", "attempt_id": ATTEMPT_A,
         "report_id": "REPORT-C5-A", "report_digest": sha256_bytes(report_a.read_bytes())},
    ]
    return entries, canonical_family_digest("TASK-C5-ROOT", entries)


def test_c5_n01(workspace: WorkspaceFixture, v4_driver: V4ConformanceDriver) -> None:
    # Arrange: active TASK with one current attempt and no REPORT.
    workspace.task("TASK-C5-N01", stage="active", attempt_id=ATTEMPT_A)

    # Act: append one final REPORT and submit T3 using it.
    report = v4_driver.write_report(
        test_id="C5-N01", clause="F4.6.1-F4.6.2",
        **report_request("TASK-C5-N01", ATTEMPT_A)
    )
    report_id = result_field(report, "report_id")
    result = v4_driver.transition(
        test_id="C5-N01", clause="F4.6.1-F4.6.2",
        **transition_request(
            "TASK-C5-N01", "active", "review", tool="submit_task", report_ref=report_id
        )
    )

    # Assert: review path, one head, and transition-bound ref plus exact byte digest.
    task_path, fields = assert_task_stage(workspace, "TASK-C5-N01", "review")
    event = fields["transitions"][-1]
    report_path = workspace.envelope_paths(report_id)[0]
    assert result is not None and task_path.exists()
    assert event["evidence_ref"] == [report_id]
    assert event["evidence_digest"] == [sha256_bytes(report_path.read_bytes())]


def test_c5_n02(workspace: WorkspaceFixture, v4_driver: V4ConformanceDriver) -> None:
    # Arrange: done Root, two completed Branches, unique current REPORTs and digest oracle.
    entries, expected_digest = _family(workspace)
    refs = [entry["report_id"] for entry in entries]

    # Act: append convergence, bind archive authorization, and commit Root T7.
    convergence = v4_driver.write_review(
        test_id="C5-N02", clause="F4.6.5-F4.6.8",
        **review_request(
            "TASK-C5-ROOT", review_kind="convergence", decision="approved",
            family_digest=expected_digest, references=refs,
        )
    )
    convergence_id = result_field(convergence, "review_id")
    authorization_fixture(
        workspace, "REVIEW-C5-AUTH", task_id="TASK-C5-ROOT",
        from_stage="done", to_stage="archive", family_digest=expected_digest,
    )
    result = v4_driver.transition(
        test_id="C5-N02", clause="F4.6.5-F4.6.8",
        **transition_request(
            "TASK-C5-ROOT", "done", "archive", tool="archive_task",
            review_ref=convergence_id, authorization_ref="REVIEW-C5-AUTH",
            family_digest=expected_digest,
        )
    )

    # Assert: Root archived only against the exact canonical family snapshot.
    _, fields = assert_task_stage(workspace, "TASK-C5-ROOT", "archive")
    assert result is not None
    assert fields["transitions"][-1]["family_digest"] == expected_digest
    assert set(fields["transitions"][-1]["evidence_ref"]) >= {convergence_id, *refs}


@pytest.mark.parametrize("case", ["missing", "ambiguous"])
def test_c5_r01(
    workspace: WorkspaceFixture, v4_driver: V4ConformanceDriver, case: str
) -> None:
    # Arrange: active current attempt with zero or two valid REPORT heads.
    workspace.task("TASK-C5-R01", stage="active", attempt_id=ATTEMPT_A)
    if case == "ambiguous":
        workspace.report("REPORT-C5-R01-A", task_id="TASK-C5-R01", attempt_id=ATTEMPT_A)
        workspace.report("REPORT-C5-R01-B", task_id="TASK-C5-R01", attempt_id=ATTEMPT_A)
    before = snapshot_tree(workspace.root)

    # Act: execute T3 without selecting an arbitrary head.
    exc = capture_error(
        lambda: v4_driver.transition(
            test_id="C5-R01", clause="F4.3.4; F4.6.2",
            **transition_request("TASK-C5-R01", "active", "review", tool="submit_task")
        )
    )

    # Assert: exact gate error and no state/event mutation.
    assert error_code(exc) == ("REPORT_REQUIRED" if case == "missing" else "REPORT_HEAD_AMBIGUOUS")
    assert snapshot_tree(workspace.root) == before


def test_c5_r02(workspace: WorkspaceFixture, v4_driver: V4ConformanceDriver) -> None:
    # Arrange: TASK current attempt B but REPORT bound to obsolete attempt A.
    workspace.task("TASK-C5-R02", stage="active", attempt_id=ATTEMPT_B)
    workspace.report("REPORT-C5-OLD", task_id="TASK-C5-R02", attempt_id=ATTEMPT_A)
    before = snapshot_tree(workspace.root)

    # Act: try T3 with the old attempt REPORT.
    exc = capture_error(
        lambda: v4_driver.transition(
            test_id="C5-R02", clause="F4.6.1-F4.6.2",
            **transition_request(
                "TASK-C5-R02", "active", "review", tool="submit_task",
                report_ref="REPORT-C5-OLD",
            )
        )
    )

    # Assert: ATTEMPT_MISMATCH and unchanged state.
    assert error_code(exc) == "ATTEMPT_MISMATCH"
    assert snapshot_tree(workspace.root) == before


def _stale_convergence(workspace: WorkspaceFixture) -> str:
    entries, old_digest = _family(workspace)
    workspace.review(
        "REVIEW-C5-CONVERGENCE", task_id="TASK-C5-ROOT", review_kind="convergence",
        decision="approved", family_digest=old_digest,
        references=[entry["report_id"] for entry in entries],
    )
    workspace.report(
        "REPORT-C5-A-NEW", task_id="TASK-C5-A", attempt_id=ATTEMPT_A,
        report_kind="replacement", references=["REPORT-C5-A"], body="changed\n",
    )
    authorization_fixture(
        workspace, "REVIEW-C5-AUTH", task_id="TASK-C5-ROOT",
        from_stage="done", to_stage="archive", family_digest=old_digest,
    )
    return old_digest


@pytest.mark.parametrize("test_id", ["C5-R03", "C5-X01"])
def test_stale_convergence_rejected(
    workspace: WorkspaceFixture, v4_driver: V4ConformanceDriver, test_id: str
) -> None:
    # Arrange: valid convergence followed by a replacement REPORT that changes family bytes.
    old_digest = _stale_convergence(workspace)
    before = snapshot_tree(workspace.root)

    # Act: archive Root using the stale convergence and authorization binding.
    exc = capture_error(
        lambda: v4_driver.transition(
            test_id=test_id, clause="F4.6.6-F4.6.8; F4.9.5",
            **transition_request(
                "TASK-C5-ROOT", "done", "archive", tool="archive_task",
                review_ref="REVIEW-C5-CONVERGENCE", authorization_ref="REVIEW-C5-AUTH",
                family_digest=old_digest,
            )
        )
    )

    # Assert: stale family snapshot cannot move Root.
    assert error_code(exc) == "FAMILY_CONVERGENCE_MISMATCH"
    assert snapshot_tree(workspace.root) == before
    assert_task_stage(workspace, "TASK-C5-ROOT", "done")


def test_c5_branch_01(workspace: WorkspaceFixture, v4_driver: V4ConformanceDriver) -> None:
    # Arrange: done Root with one active Branch and otherwise valid archive authorization.
    _, digest = _family(workspace, second_state="active")
    authorization_fixture(
        workspace, "REVIEW-C5-BRANCH-AUTH", task_id="TASK-C5-ROOT",
        from_stage="done", to_stage="archive", family_digest=digest,
    )
    before = snapshot_tree(workspace.root)

    # Act: attempt Root T7.
    exc = capture_error(
        lambda: v4_driver.transition(
            test_id="C5-BRANCH-01", clause="F4.6.5",
            **transition_request(
                "TASK-C5-ROOT", "done", "archive", tool="archive_task",
                authorization_ref="REVIEW-C5-BRANCH-AUTH", family_digest=digest,
            )
        )
    )

    # Assert: explicit terminal-gate error and Root remains done.
    assert error_code(exc) == "BRANCH_NOT_TERMINAL"
    assert snapshot_tree(workspace.root) == before


def test_c5_archived_01(workspace: WorkspaceFixture, v4_driver: V4ConformanceDriver) -> None:
    # Arrange: completed family and an authorization for Branch B T7.
    _, expected = _family(workspace)
    authorization_fixture(
        workspace, "REVIEW-C5-B-ARCHIVE", task_id="TASK-C5-B",
        from_stage="done", to_stage="archive", attempt_id=ATTEMPT_B,
    )
    before = v4_driver.family_digest(
        test_id="C5-ARCHIVED-01", clause="F4.6.6-F4.6.8", root_task_id="TASK-C5-ROOT"
    )

    # Act: archive one Branch, then recompute the family digest.
    moved = v4_driver.transition(
        test_id="C5-ARCHIVED-01", clause="F4.6.6-F4.6.8",
        **transition_request(
            "TASK-C5-B", "done", "archive", tool="archive_task",
            authorization_ref="REVIEW-C5-B-ARCHIVE",
        )
    )
    after = v4_driver.family_digest(
        test_id="C5-ARCHIVED-01", clause="F4.6.6-F4.6.8", root_task_id="TASK-C5-ROOT"
    )

    # Assert: path changes, canonical content does not.
    assert moved is not None
    assert digest_value(before) == expected
    assert digest_value(after) == expected
    assert_task_stage(workspace, "TASK-C5-B", "archive")


def test_c5_family_digest_01(workspace: WorkspaceFixture, v4_driver: V4ConformanceDriver) -> None:
    # Arrange: branches deliberately created B then A, plus distinct mtimes.
    _, expected = _family(workspace)
    branch_a = workspace.task_paths("TASK-C5-A")[0]
    branch_b = workspace.task_paths("TASK-C5-B")[0]
    os.utime(branch_a, (1_000_000, 1_000_000))
    os.utime(branch_b, (2_000_000, 2_000_000))

    # Act: compute through production, then move B done→archive without changing bytes.
    first = v4_driver.family_digest(
        test_id="C5-FAMILY-DIGEST-01", clause="F4.6.6", root_task_id="TASK-C5-ROOT"
    )
    archived_b = workspace.root / "fcop" / "_lifecycle" / "archive" / branch_b.name
    branch_b.replace(archived_b)
    second = v4_driver.family_digest(
        test_id="C5-FAMILY-DIGEST-01", clause="F4.6.6", root_task_id="TASK-C5-ROOT"
    )

    # Assert: independent oracle, lowercase SHA-256, order/mtime/path independence.
    assert digest_value(first) == expected
    assert digest_value(second) == expected
    assert len(expected) == 64 and expected == expected.lower()


def test_c5_family_race_01(workspace: WorkspaceFixture) -> None:
    # Arrange: active Root with a current REPORT; Branch-create and Root T3 share a family.
    workspace.task("TASK-C5-RACE-ROOT", stage="active", attempt_id=ATTEMPT_A)
    workspace.report("REPORT-C5-RACE", task_id="TASK-C5-RACE-ROOT", attempt_id=ATTEMPT_A)
    commands = [
        {"action": "create_task", "kwargs": {
            "test_id": "C5-FAMILY-RACE-01", "clause": "F4.5.4; F4.9.5",
            **create_request("family-race-branch", branch_of="TASK-C5-RACE-ROOT"),
        }},
        {"action": "transition", "kwargs": {
            "test_id": "C5-FAMILY-RACE-01", "clause": "F4.5.4; F4.9.5",
            **transition_request(
                "TASK-C5-RACE-ROOT", "active", "review", tool="submit_task",
                report_ref="REPORT-C5-RACE",
            ),
        }},
    ]

    # Act: synchronize two real processes and execute both production commits.
    results = run_concurrent_operations(workspace.root, commands)

    # Assert: no missing surface; committed order leaves a coherent family boundary.
    assert all(item.get("code") != "V4_NOT_IMPLEMENTED" for item in results), (
        f"[C5-FAMILY-RACE-01] F4.5.4/F4.9.5 production operation missing: {results}"
    )
    assert any(item["status"] == "returned" for item in results)
    root_stage = workspace.task_paths("TASK-C5-RACE-ROOT")[0].parent.name
    branch_files = [
        path for path in (workspace.root / "fcop" / "_lifecycle").glob("*/*.md")
        if read_frontmatter(path).get("branch_of") == "TASK-C5-RACE-ROOT"
    ]
    assert root_stage in {"active", "review"}
    assert len(branch_files) <= 1
    if not branch_files:
        assert any(item["status"] == "error" for item in results)


def test_c5_report_race_01(workspace: WorkspaceFixture) -> None:
    # Arrange: one Branch with old head and a Root ready for convergence.
    entries, digest = _family(workspace)
    commands = [
        {"action": "write_report", "kwargs": {
            "test_id": "C5-REPORT-RACE-01", "clause": "F4.6.6-F4.6.8; F4.9.5",
            **report_request(
                "TASK-C5-A", ATTEMPT_A, report_kind="replacement",
                references=["REPORT-C5-A"], body="new head\n",
            ),
        }},
        {"action": "write_review", "kwargs": {
            "test_id": "C5-REPORT-RACE-01", "clause": "F4.6.6-F4.6.8; F4.9.5",
            **review_request(
                "TASK-C5-ROOT", review_kind="convergence", decision="approved",
                family_digest=digest, references=[entry["report_id"] for entry in entries],
            ),
        }},
    ]

    # Act: replacement and convergence compete as real operations.
    results = run_concurrent_operations(workspace.root, commands)

    # Assert: never accept a missing surface or a mixed, unverifiable snapshot.
    assert all(item.get("code") != "V4_NOT_IMPLEMENTED" for item in results), (
        f"[C5-REPORT-RACE-01] F4.6.6-F4.6.8/F4.9.5 operation missing: {results}"
    )
    driver = V4ConformanceDriver(workspace.root)
    observed = driver.family_digest(
        test_id="C5-REPORT-RACE-01", clause="F4.6.6-F4.6.8; F4.9.5",
        root_task_id="TASK-C5-ROOT",
    )
    after_digest = digest_value(observed)
    convergence_files = [
        path for path in (workspace.root / "fcop" / "reviews").glob("*.md")
        if read_frontmatter(path).get("review_kind") == "convergence"
    ]
    if convergence_files:
        stored = read_frontmatter(convergence_files[0])
        assert stored["family_digest"] in {digest, after_digest}
        assert stored["family_digest"] == digest or "REPORT-C5-A-NEW" in stored["references"]
    assert all(item["status"] in {"returned", "error"} for item in results)


def test_at_03(workspace: WorkspaceFixture) -> None:
    # Arrange: active Branch without a REPORT; REPORT write races T3.
    workspace.task("TASK-AT-03", stage="active", attempt_id=ATTEMPT_A)
    commands = [
        {"action": "write_report", "kwargs": {
            "test_id": "AT-03", "clause": "F4.6.2-F4.6.3",
            **report_request("TASK-AT-03", ATTEMPT_A),
        }},
        {"action": "transition", "kwargs": {
            "test_id": "AT-03", "clause": "F4.6.2-F4.6.3",
            **transition_request("TASK-AT-03", "active", "review", tool="submit_task"),
        }},
    ]

    # Act: execute both operations in synchronized processes.
    results = run_concurrent_operations(workspace.root, commands)

    # Assert: no false success; review implies a durable current REPORT, otherwise stable reject.
    assert all(item.get("code") != "V4_NOT_IMPLEMENTED" for item in results), (
        f"[AT-03] F4.6.2-F4.6.3 production operation missing: {results}"
    )
    stage = workspace.task_paths("TASK-AT-03")[0].parent.name
    reports = list((workspace.root / "fcop" / "reports").glob("REPORT-*.md"))
    if stage == "review":
        assert len(reports) == 1
    else:
        assert stage == "active"
        assert any(item.get("code") == "REPORT_REQUIRED" for item in results)


def test_at_04(workspace: WorkspaceFixture) -> None:
    # Arrange: complete family; convergence creation races Root archive.
    entries, digest = _family(workspace)
    authorization_fixture(
        workspace, "REVIEW-AT-04-AUTH", task_id="TASK-C5-ROOT",
        from_stage="done", to_stage="archive", family_digest=digest,
    )
    commands = [
        {"action": "write_review", "kwargs": {
            "test_id": "AT-04", "clause": "F4.6.5-F4.6.8",
            **review_request(
                "TASK-C5-ROOT", review_kind="convergence", decision="approved",
                family_digest=digest, references=[item["report_id"] for item in entries],
            ),
        }},
        {"action": "transition", "kwargs": {
            "test_id": "AT-04", "clause": "F4.6.5-F4.6.8",
            **transition_request(
                "TASK-C5-ROOT", "done", "archive", tool="archive_task",
                authorization_ref="REVIEW-AT-04-AUTH", family_digest=digest,
            ),
        }},
    ]

    # Act: execute real competing commits.
    results = run_concurrent_operations(workspace.root, commands)

    # Assert: archive only if matching convergence became durable; otherwise stable refusal.
    assert all(item.get("code") != "V4_NOT_IMPLEMENTED" for item in results), (
        f"[AT-04] F4.6.5-F4.6.8 production operation missing: {results}"
    )
    stage = workspace.task_paths("TASK-C5-ROOT")[0].parent.name
    if stage == "archive":
        convergence = [
            read_frontmatter(path) for path in (workspace.root / "fcop" / "reviews").glob("*.md")
            if read_frontmatter(path).get("review_kind") == "convergence"
        ]
        assert any(item.get("family_digest") == digest for item in convergence)
    else:
        assert stage == "done"
        assert any(item["status"] == "error" for item in results)
