"""C2 four-envelope and append-only behavioral conformance."""

from __future__ import annotations

from .driver import V4ConformanceDriver, capture_error, error_code, result_field
from .fixtures import ATTEMPT_A, WORKSPACE_A, WorkspaceFixture, read_frontmatter, snapshot_tree


def test_c2_n01(workspace: WorkspaceFixture, v4_driver: V4ConformanceDriver) -> None:
    # Arrange: a valid active TASK target for REPORT/ISSUE/REVIEW.
    task_path = workspace.task("TASK-C2-N01", stage="active", attempt_id=ATTEMPT_A)

    # Act: create all four formal envelope types through production operations.
    task = v4_driver.create_task(
        test_id="C2-N01", clause="F4.3.1-F4.3.2", workspace_id=WORKSPACE_A,
        operation_id="c2-task", operation_kind="create_task", sender="ME",
        recipient="ME", priority="P2", subject="four types", body="task\n",
        parent=None, branch_of=None, references=[],
    )
    report = v4_driver.write_report(
        test_id="C2-N01", clause="F4.3.1-F4.3.2", workspace_id=WORKSPACE_A,
        subject_ref="TASK-C2-N01", attempt_id=ATTEMPT_A, report_kind="final",
        result="done", sender="ME", recipient="ME", body="report\n", references=[],
    )
    issue = v4_driver.write_issue(
        test_id="C2-N01", clause="F4.3.1-F4.3.2", workspace_id=WORKSPACE_A,
        subject_ref="TASK-C2-N01", severity="medium", sender="ME", recipient="ME",
        body="issue\n", references=[],
    )
    review = v4_driver.write_review(
        test_id="C2-N01", clause="F4.3.1-F4.3.2", workspace_id=WORKSPACE_A,
        review_kind="assessment", subject_ref="TASK-C2-N01", decision="approved",
        sender="ME", recipient="ME", body="review\n", references=[],
    )

    # Assert: each result resolves to exactly one typed UTF-8/LF envelope.
    expected = [(task, "task_id", "TASK"), (report, "report_id", "REPORT"),
                (issue, "issue_id", "ISSUE"), (review, "review_id", "REVIEW")]
    for result, id_field, envelope_type in expected:
        envelope_id = result_field(result, id_field)
        paths = workspace.envelope_paths(envelope_id)
        assert len(paths) == 1
        fields = read_frontmatter(paths[0])
        assert fields["type"] == envelope_type
        assert fields["workspace_id"] == WORKSPACE_A
        assert b"\r" not in paths[0].read_bytes()
    assert task_path.exists()


def test_c2_r01(workspace: WorkspaceFixture, v4_driver: V4ConformanceDriver) -> None:
    # Arrange: a complete but forbidden fifth envelope type.
    fields = {
        "protocol": "fcop", "version": 4, "type": "EVAL", "eval_id": "EVAL-1",
        "workspace_id": WORKSPACE_A, "sender": "ME", "recipient": "ME",
        "created_at": "2026-09-03T00:00:00+08:00", "subject_ref": "workspace:" + WORKSPACE_A,
    }
    invalid_path = workspace.raw_envelope("fcop/issues/EVAL-1.md", fields, "forbidden")
    before = snapshot_tree(workspace.root)

    # Act: ask the production state inspector to validate the landed formal candidate.
    exc = capture_error(
        lambda: v4_driver.inspect_state(
            test_id="C2-R01", clause="F4.3.1-F4.3.2", envelope_path=invalid_path,
        )
    )

    # Assert: INVALID_ENVELOPE and no disk mutation.
    assert error_code(exc) == "INVALID_ENVELOPE"
    assert snapshot_tree(workspace.root) == before


def test_c2_r02(workspace: WorkspaceFixture, v4_driver: V4ConformanceDriver) -> None:
    # Arrange: landed REPORT and REVIEW facts whose bytes must never change.
    workspace.task("TASK-C2-R02", stage="active", attempt_id=ATTEMPT_A)
    old_report = workspace.report("REPORT-C2-OLD", task_id="TASK-C2-R02", attempt_id=ATTEMPT_A)
    old_review = workspace.review(
        "REVIEW-C2-OLD", task_id="TASK-C2-R02", review_kind="assessment",
        decision="needs_human", references=["REPORT-C2-OLD"],
    )
    report_bytes = old_report.read_bytes()
    review_bytes = old_review.read_bytes()

    # Act: append a replacement REPORT and an approval REVIEW referencing old facts.
    replacement = v4_driver.write_report(
        test_id="C2-R02", clause="F4.3.3; F4.3.5", workspace_id=WORKSPACE_A,
        subject_ref="TASK-C2-R02", attempt_id=ATTEMPT_A, report_kind="replacement",
        result="done", sender="ME", recipient="ME", body="replacement\n",
        references=["REPORT-C2-OLD"],
    )
    approval = v4_driver.mark_human_approved(
        test_id="C2-R02", clause="F4.3.3; F4.3.5", review_id="REVIEW-C2-OLD",
        decision="approved", approver="human:test", profile_ref="profile:test",
        comment="append, do not edit",
    )

    # Assert: new IDs/files exist, reference old facts, and old bytes are identical.
    assert old_report.read_bytes() == report_bytes
    assert old_review.read_bytes() == review_bytes
    replacement_id = result_field(replacement, "report_id")
    approval_id = result_field(approval, "review_id")
    assert replacement_id != "REPORT-C2-OLD"
    assert approval_id != "REVIEW-C2-OLD"
    assert "REPORT-C2-OLD" in read_frontmatter(workspace.envelope_paths(replacement_id)[0])["references"]
    assert "REVIEW-C2-OLD" in read_frontmatter(workspace.envelope_paths(approval_id)[0])["references"]
