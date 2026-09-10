"""C4 four-relation and Branch-depth behavioral conformance."""

from __future__ import annotations

import pytest

from .driver import V4ConformanceDriver, capture_error, error_code, result_field
from .fixtures import ATTEMPT_A, WorkspaceFixture, read_frontmatter, snapshot_tree
from .scenarios import create_request, report_request, review_request


def test_c4_n01(workspace: WorkspaceFixture, v4_driver: V4ConformanceDriver) -> None:
    # Arrange: valid parent and citation targets in this workspace.
    workspace.task("TASK-C4-PARENT", stage="active", attempt_id=ATTEMPT_A)
    workspace.issue("ISSUE-C4-CITE", subject_ref="TASK-C4-PARENT")

    # Act: create parent/references TASK plus subject_ref REPORT/ISSUE/REVIEW facts.
    child = v4_driver.create_task(
        test_id="C4-N01", clause="F4.5.1-F4.5.2",
        **create_request(
            "c4-child", subject="child", parent="TASK-C4-PARENT",
            references=["ISSUE-C4-CITE"],
        )
    )
    child_id = result_field(child, "task_id")
    report = v4_driver.write_report(
        test_id="C4-N01", clause="F4.5.1-F4.5.2",
        **report_request("TASK-C4-PARENT", ATTEMPT_A)
    )
    issue = v4_driver.write_issue(
        test_id="C4-N01", clause="F4.5.1-F4.5.2", workspace_id=workspace.workspace_id,
        subject_ref="TASK-C4-PARENT", severity="low", sender="ME", recipient="ME",
        body="issue\n", references=[result_field(report, "report_id")],
    )
    review = v4_driver.write_review(
        test_id="C4-N01", clause="F4.5.1-F4.5.2",
        **review_request(
            "TASK-C4-PARENT", review_kind="assessment", decision="approved",
            references=[result_field(issue, "issue_id")],
        )
    )

    # Assert: all four relations decode and references do not change ownership.
    child_fields = read_frontmatter(workspace.task_paths(child_id)[0])
    assert child_fields["parent"] == "TASK-C4-PARENT"
    assert child_fields["branch_of"] in {None, ""}
    assert child_fields["references"] == ["ISSUE-C4-CITE"]
    for result, field in ((report, "report_id"), (issue, "issue_id"), (review, "review_id")):
        envelope = read_frontmatter(workspace.envelope_paths(result_field(result, field))[0])
        assert envelope["subject_ref"] == "TASK-C4-PARENT"


def test_c4_n02(workspace: WorkspaceFixture, v4_driver: V4ConformanceDriver) -> None:
    # Arrange: one unambiguous active Root.
    workspace.task("TASK-C4-ROOT", stage="active", attempt_id=ATTEMPT_A)

    # Act: create two ordinary TASK siblings with the same branch_of Root.
    branch_a = v4_driver.create_task(
        test_id="C4-N02", clause="F4.5.3-F4.5.4",
        **create_request("c4-branch-a", subject="branch a", branch_of="TASK-C4-ROOT")
    )
    branch_b = v4_driver.create_task(
        test_id="C4-N02", clause="F4.5.3-F4.5.4",
        **create_request("c4-branch-b", subject="branch b", branch_of="TASK-C4-ROOT")
    )

    # Assert: two distinct sibling TASKs, depth one, Root remains active.
    ids = {result_field(branch_a, "task_id"), result_field(branch_b, "task_id")}
    assert len(ids) == 2
    assert all(read_frontmatter(workspace.task_paths(task_id)[0])["branch_of"] == "TASK-C4-ROOT" for task_id in ids)
    assert "branch_of" not in read_frontmatter(workspace.task_paths("TASK-C4-ROOT")[0])


INVALID_RELATIONS = [
    ("dangling-parent", {"parent": "TASK-MISSING"}, "RELATION_INVALID"),
    ("cross-workspace", {"parent": "TASK-C4-FOREIGN"}, "RELATION_INVALID"),
    ("self-cycle", {"parent": "TASK-C4-SELF"}, "RELATION_INVALID"),
    ("dangling-gate-reference", {"references": ["REPORT-MISSING"]}, "REFERENCE_UNRESOLVED"),
    ("nonunique-parent", {"parent": "TASK-C4-DUP"}, "RELATION_INVALID"),
]


@pytest.mark.parametrize(
    ("case", "relations", "expected_code"), INVALID_RELATIONS,
    ids=[item[0] for item in INVALID_RELATIONS],
)
def test_c4_r01(
    workspace: WorkspaceFixture, v4_driver: V4ConformanceDriver,
    case: str, relations: dict[str, object], expected_code: str,
) -> None:
    # Arrange: distinct invalid relation graphs, including a duplicate strong target.
    if case == "self-cycle":
        workspace.task("TASK-C4-SELF", stage="inbox", parent="TASK-C4-SELF")
    if case == "cross-workspace":
        from .fixtures import WORKSPACE_B
        foreign = WorkspaceFixture(workspace.root.parent / "foreign", WORKSPACE_B).create()
        foreign.task("TASK-C4-FOREIGN", stage="inbox")
    if case == "nonunique-parent":
        workspace.task("TASK-C4-DUP", stage="inbox")
        workspace.task("TASK-C4-DUP", stage="done")
    before = snapshot_tree(workspace.root)
    kwargs = create_request(f"c4-invalid-{case}", subject=f"invalid {case}")
    kwargs.update(relations)
    if case == "dangling-gate-reference":
        kwargs["references_required_by_gate"] = True

    # Act: attempt to persist the invalid relation.
    exc = capture_error(
        lambda: v4_driver.create_task(
            test_id="C4-R01", clause="F4.5.2", **kwargs
        )
    )

    # Assert: stable relation error and no new/modified bytes.
    assert error_code(exc) == expected_code
    assert snapshot_tree(workspace.root) == before


def test_c4_r02(workspace: WorkspaceFixture, v4_driver: V4ConformanceDriver) -> None:
    # Arrange: a Root and an existing depth-one Branch.
    workspace.task("TASK-C4-ROOT", stage="active", attempt_id=ATTEMPT_A)
    workspace.task("TASK-C4-BRANCH", stage="active", branch_of="TASK-C4-ROOT")
    before = snapshot_tree(workspace.root)

    # Act: attempt to use the Branch as another Branch's Root.
    exc = capture_error(
        lambda: v4_driver.create_task(
            test_id="C4-R02", clause="F4.5.3",
            **create_request("c4-depth-two", branch_of="TASK-C4-BRANCH")
        )
    )

    # Assert: exact depth error and no TASK creation.
    assert error_code(exc) == "BRANCH_DEPTH_EXCEEDED"
    assert snapshot_tree(workspace.root) == before
