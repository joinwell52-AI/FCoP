"""C3 exact lifecycle, evidence gates, and archive behavior."""

from __future__ import annotations

import pytest

from .driver import V4ConformanceDriver, capture_error, error_code, result_field
from .fixtures import (
    ATTEMPT_A,
    DeterministicProfileEvaluator,
    WorkspaceFixture,
    bind_t3,
    read_frontmatter,
    snapshot_tree,
)
from .scenarios import (
    assert_committed_transition,
    assert_task_stage,
    authorization_fixture,
    create_request,
    report_request,
    review_request,
    transition_request,
)

T1_EVENT = {"at": "2026-09-03T00:00:00+08:00", "from": None, "to": "inbox", "by": "ME", "tool": "create_task"}


def test_c3_n01(workspace: WorkspaceFixture, v4_driver: V4ConformanceDriver) -> None:
    # Arrange: one inbox TASK whose only event is T1.
    workspace.task("TASK-C3-N01", stage="inbox", transitions=[T1_EVENT])
    driver = V4ConformanceDriver(
        workspace.root,
        trusted_profiles={"profile:test": DeterministicProfileEvaluator("AUTHORIZED")},
        test_id="C3-N01",
    )

    # Act: execute T2→T3→T4→T7 with actual REPORT/REVIEW/authorization evidence.
    claimed = driver.transition(
        test_id="C3-N01", clause="F4.4.1-F4.4.3", **transition_request(
            "TASK-C3-N01", "inbox", "active", tool="claim_task"
        )
    )
    attempt_id = result_field(claimed, "attempt_id")
    report = driver.write_report(
        test_id="C3-N01", clause="F4.4.1-F4.4.3",
        **report_request("TASK-C3-N01", attempt_id)
    )
    report_id = result_field(report, "report_id")
    submitted = driver.transition(
        test_id="C3-N01", clause="F4.4.1-F4.4.3", **transition_request(
            "TASK-C3-N01", "active", "review", tool="submit_task", report_ref=report_id
        )
    )
    acceptance = driver.write_review(
        test_id="C3-N01", clause="F4.4.1-F4.4.3",
        **review_request(
            "TASK-C3-N01", review_kind="acceptance", decision="approved",
            attempt_id=attempt_id, references=[report_id], profile_ref="profile:test",
            transition={"from": "review", "to": "done"}, authorization_scope="single_use",
        )
    )
    acceptance_id = result_field(acceptance, "review_id")
    approve_auth = authorization_fixture(
        workspace,
        "REVIEW-C3-APPROVE-AUTH",
        task_id="TASK-C3-N01",
        from_stage="review",
        to_stage="done",
        attempt_id=attempt_id,
    )
    approved = driver.transition(
        test_id="C3-N01", clause="F4.4.1-F4.4.3", **transition_request(
            "TASK-C3-N01", "review", "done", tool="approve_task",
            report_ref=report_id,
            review_ref=acceptance_id,
            authorization_ref=read_frontmatter(approve_auth)["review_id"],
        )
    )
    archive_auth = authorization_fixture(
        workspace, "REVIEW-C3-ARCHIVE-AUTH", task_id="TASK-C3-N01",
        from_stage="done", to_stage="archive", attempt_id=attempt_id,
    )
    archived = driver.transition(
        test_id="C3-N01", clause="F4.4.1-F4.4.3", **transition_request(
            "TASK-C3-N01", "done", "archive", tool="archive_task",
            authorization_ref=read_frontmatter(archive_auth)["review_id"],
        )
    )

    # Assert: each command committed one edge; final TASK has five ordered events.
    assert submitted is not None and approved is not None and archived is not None
    path, fields = assert_task_stage(workspace, "TASK-C3-N01", "archive")
    assert [(event["from"], event["to"]) for event in fields["transitions"]] == [
        (None, "inbox"), ("inbox", "active"), ("active", "review"),
        ("review", "done"), ("done", "archive"),
    ]
    assert len(workspace.task_paths("TASK-C3-N01")) == 1
    assert path.exists()


def test_c3_n02(workspace: WorkspaceFixture, v4_driver: V4ConformanceDriver) -> None:
    # Arrange: done TASK with an old attempt and a valid reopen authorization REVIEW.
    workspace.task("TASK-C3-N02", stage="done", attempt_id=ATTEMPT_A)
    auth = authorization_fixture(
        workspace, "REVIEW-C3-REOPEN", task_id="TASK-C3-N02",
        from_stage="done", to_stage="active", attempt_id=ATTEMPT_A,
    )

    # Act: perform T6.
    driver = V4ConformanceDriver(
        workspace.root,
        trusted_profiles={"profile:test": DeterministicProfileEvaluator("AUTHORIZED")},
        test_id="C3-N02",
    )
    result = driver.transition(
        test_id="C3-N02", clause="F4.4.2; F4.6.1", **transition_request(
            "TASK-C3-N02", "done", "active", tool="reopen_task",
            review_ref="REVIEW-C3-REOPEN", authorization_ref="REVIEW-C3-REOPEN",
        )
    )

    # Assert: unique active path and a genuinely new attempt.
    event = assert_committed_transition(
        workspace, "TASK-C3-N02", "active", result, previous_events=1,
        expected_from="done", expected_to="active",
    )
    assert result_field(result, "attempt_id") != ATTEMPT_A
    assert event["attempt_id"] == result_field(result, "attempt_id")
    assert auth.exists()


def test_c3_r01(workspace: WorkspaceFixture, v4_driver: V4ConformanceDriver) -> None:
    # Arrange: an inbox TASK and a complete before snapshot.
    workspace.task("TASK-C3-R01", stage="inbox", transitions=[T1_EVENT])
    before = snapshot_tree(workspace.root)

    # Act: request the nonexistent inbox→archive edge.
    exc = capture_error(
        lambda: v4_driver.transition(
            test_id="C3-R01", clause="F4.4.2-F4.4.3", **transition_request(
                "TASK-C3-R01", "inbox", "archive", tool="archive_task"
            )
        )
    )

    # Assert: stable error and no path/event change.
    assert error_code(exc) == "INVALID_TRANSITION"
    assert snapshot_tree(workspace.root) == before
    assert_task_stage(workspace, "TASK-C3-R01", "inbox")


def test_c3_r02(workspace: WorkspaceFixture, v4_driver: V4ConformanceDriver) -> None:
    # Arrange: active 4.0 TASK and no review gate evidence.
    workspace.task("TASK-C3-R02", stage="active", attempt_id=ATTEMPT_A)
    before = snapshot_tree(workspace.root)

    # Act: invoke the v3 legacy active→done tool semantic.
    exc = capture_error(
        lambda: v4_driver.transition(
            test_id="C3-R02", clause="F4.4.4", **transition_request(
                "TASK-C3-R02", "active", "done", tool="finish_task"
            )
        )
    )

    # Assert: the dedicated legacy error and zero writes.
    assert error_code(exc) == "LEGACY_TRANSITION_NOT_ALLOWED"
    assert snapshot_tree(workspace.root) == before


def test_c3_r03(workspace: WorkspaceFixture, v4_driver: V4ConformanceDriver) -> None:
    # Arrange: authoritative archive TASK.
    archive_path = workspace.task("TASK-C3-R03", stage="archive")
    before = archive_path.read_bytes()

    # Act: request movement into legacy history.
    exc = capture_error(
        lambda: v4_driver.transition(
            test_id="C3-R03", clause="F4.4.6; F4.11.2", **transition_request(
                "TASK-C3-R03", "archive", "history", tool="archive_to_history"
            )
        )
    )

    # Assert: archive stays authoritative and unchanged.
    assert error_code(exc) in {"INVALID_TRANSITION", "LEGACY_TRANSITION_NOT_ALLOWED"}
    assert archive_path.read_bytes() == before
    assert_task_stage(workspace, "TASK-C3-R03", "archive")


def test_c3_x01(workspace: WorkspaceFixture, v4_driver: V4ConformanceDriver) -> None:
    # Arrange: terminal archive bytes and a fault at cold-export target durability.
    archive_path = workspace.task("TASK-C3-X01", stage="archive")
    before = archive_path.read_bytes()
    v4_driver.inject_fault(
        test_id="C3-X01", clause="F4.4.6; F4.9.4",
        operation="export_archive", stage="TARGET_DURABLE",
    )

    # Act: execute the real cold-storage export until the injected crash.
    capture_error(
        lambda: v4_driver.export_archive(
            test_id="C3-X01", clause="F4.4.6; F4.9.4", task_id="TASK-C3-X01"
        )
    )

    # Assert: authoritative archive is unchanged; cold files cannot become NOW.
    assert archive_path.read_bytes() == before
    assert_task_stage(workspace, "TASK-C3-X01", "archive")
    assert all("_lifecycle" not in path.relative_to(workspace.root).parts for path in (workspace.root / "fcop" / "cold").rglob("*"))


GATE_CASES = [
    ("T1", None, "inbox", "create_task", None),
    ("T2", "inbox", "active", "claim_task", None),
    ("T3", "active", "review", "submit_task", "REPORT_REQUIRED"),
    ("T4", "review", "done", "approve_task", "AUTHORIZATION_REQUIRED"),
    ("T5", "review", "active", "reject_task", "AUTHORIZATION_REQUIRED"),
    ("T6", "done", "active", "reopen_task", "AUTHORIZATION_REQUIRED"),
    ("T7", "done", "archive", "archive_task", "AUTHORIZATION_REQUIRED"),
]


@pytest.mark.parametrize(
    ("edge", "source", "target", "tool", "missing_error"), GATE_CASES,
    ids=[case[0] for case in GATE_CASES],
)
def test_c3_gate_01(
    workspace: WorkspaceFixture, v4_driver: V4ConformanceDriver,
    edge: str, source: str | None, target: str, tool: str, missing_error: str | None,
) -> None:
    # Arrange: one complete gate and, where evidence is required, one incomplete twin.
    task_id = f"TASK-GATE-{edge}"
    bad_id = f"TASK-GATE-{edge}-BAD"
    if source is not None:
        workspace.task(task_id, stage=source, attempt_id=ATTEMPT_A)
        if missing_error:
            workspace.task(bad_id, stage=source, attempt_id=ATTEMPT_A)
    report_ref = review_ref = auth_ref = None
    if edge in {"T3", "T4", "T5"}:
        workspace.report(f"REPORT-{edge}", task_id=task_id, attempt_id=ATTEMPT_A)
        report_ref = f"REPORT-{edge}"
        if edge in {"T4", "T5"}:
            bind_t3(workspace, task_id, report_ref)
    if edge in {"T4", "T5", "T6"}:
        kind = {"T4": "acceptance", "T5": "rejection", "T6": "reopen"}[edge]
        decision = "approved" if edge != "T5" else "rejected"
        workspace.review(
            f"REVIEW-{edge}", task_id=task_id, review_kind=kind, decision=decision,
            attempt_id=ATTEMPT_A, references=[report_ref] if report_ref else [],
            profile_ref="profile:test", transition={"from": source, "to": target},
            authorization_scope="single_use",
        )
        review_ref = auth_ref = f"REVIEW-{edge}"
    if edge == "T7":
        authorization_fixture(
            workspace, "REVIEW-T7", task_id=task_id, from_stage="done", to_stage="archive",
            attempt_id=ATTEMPT_A,
        )
        auth_ref = "REVIEW-T7"

    # Act: commit the complete edge; then attempt the twin without required evidence.
    if edge == "T1":
        result = v4_driver.create_task(
            test_id="C3-GATE-01", clause="F4.4.2; F4.4.7",
            **create_request("gate-t1", subject=task_id)
        )
        task_id = result_field(result, "task_id")
    else:
        driver = (
            V4ConformanceDriver(
                workspace.root,
                trusted_profiles={
                    "profile:test": DeterministicProfileEvaluator("AUTHORIZED")
                },
                test_id="C3-GATE-01",
            )
            if edge in {"T4", "T5", "T6"}
            else v4_driver
        )
        result = driver.transition(
            test_id="C3-GATE-01", clause="F4.4.2; F4.4.7",
            **transition_request(
                task_id, source, target, tool=tool, report_ref=report_ref,
                review_ref=review_ref, authorization_ref=auth_ref,
            )
        )
    if missing_error:
        before_bad = snapshot_tree(workspace.root)
        exc = capture_error(
            lambda: driver.transition(
                test_id="C3-GATE-01", clause="F4.4.2; F4.4.7",
                **transition_request(bad_id, source, target, tool=tool)
            )
        )

    # Assert: complete edge commits exactly once; incomplete gate is stable and atomic.
    assert result is not None
    assert_task_stage(workspace, task_id, target)
    if missing_error:
        assert error_code(exc) == missing_error
        assert snapshot_tree(workspace.root) == before_bad
        assert_task_stage(workspace, bad_id, source)
