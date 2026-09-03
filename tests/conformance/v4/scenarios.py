"""Reusable request builders and postcondition assertions for behavior tests."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence

from .driver import result_field
from .fixtures import WORKSPACE_A, WorkspaceFixture, read_frontmatter, sha256_bytes


def create_request(
    operation_id: str, *, workspace_id: str = WORKSPACE_A,
    subject: str = "created task", body: str = "body\n",
    parent: str | None = None, branch_of: str | None = None,
    references: Sequence[str] = (),
) -> dict[str, Any]:
    return {
        "workspace_id": workspace_id, "operation_id": operation_id,
        "operation_kind": "create_task", "sender": "ME", "recipient": "ME",
        "priority": "P2", "subject": subject, "body": body,
        "parent": parent, "branch_of": branch_of, "references": list(references),
    }


def report_request(
    task_id: str, attempt_id: str, *, report_kind: str = "final",
    references: Sequence[str] = (), body: str = "report\n",
) -> dict[str, Any]:
    return {
        "workspace_id": WORKSPACE_A, "subject_ref": task_id,
        "attempt_id": attempt_id, "report_kind": report_kind, "result": "done",
        "sender": "ME", "recipient": "ME", "body": body,
        "references": list(references),
    }


def review_request(
    task_id: str, *, review_kind: str, decision: str,
    attempt_id: str | None = None, family_digest: str | None = None,
    references: Sequence[str] = (), profile_ref: str | None = None,
    transition: Mapping[str, str] | None = None,
    expires_at: str | None = "2099-01-01T00:00:00+00:00",
    authorization_scope: str | None = None,
) -> dict[str, Any]:
    return {
        "workspace_id": WORKSPACE_A, "review_kind": review_kind,
        "subject_ref": task_id, "decision": decision, "attempt_id": attempt_id,
        "family_digest": family_digest, "references": list(references),
        "profile_ref": profile_ref, "transition": dict(transition) if transition else None,
        "issued_at": "2026-09-03T00:03:00+08:00", "expires_at": expires_at,
        "authorization_scope": authorization_scope, "sender": "ME", "recipient": "ME",
        "body": "review\n",
    }


def transition_request(
    task_id: str, from_stage: str | None, to_stage: str, *, tool: str,
    report_ref: str | None = None, review_ref: str | None = None,
    authorization_ref: str | None = None, family_digest: str | None = None,
) -> dict[str, Any]:
    return {
        "task_id": task_id, "from_stage": from_stage, "to_stage": to_stage,
        "tool": tool, "actor": "ME", "report_ref": report_ref,
        "review_ref": review_ref, "authorization_ref": authorization_ref,
        "family_digest": family_digest,
    }


def assert_task_stage(
    workspace: WorkspaceFixture, task_id: str, stage: str
) -> tuple[Path, dict[str, Any]]:
    paths = workspace.task_paths(task_id)
    assert len(paths) == 1, f"expected one authoritative path, got {paths}"
    assert paths[0].parent.name == stage
    return paths[0], read_frontmatter(paths[0])


def assert_committed_transition(
    workspace: WorkspaceFixture, task_id: str, stage: str, result: Any,
    *, previous_events: int, expected_from: str | None, expected_to: str,
) -> dict[str, Any]:
    assert result is not None
    path, fields = assert_task_stage(workspace, task_id, stage)
    events = fields["transitions"]
    assert len(events) == previous_events + 1
    event = events[-1]
    assert event["from"] == expected_from
    assert event["to"] == expected_to
    assert result_field(result, "task_id") == task_id
    assert sha256_bytes(path.read_bytes())
    return event


def authorization_fixture(
    workspace: WorkspaceFixture, review_id: str, *, task_id: str,
    from_stage: str, to_stage: str, attempt_id: str | None = None,
    family_digest: str | None = None,
    expires_at: str | None = "2099-01-01T00:00:00+00:00",
    profile_ref: str = "profile:test", decision: str = "authorize",
) -> Path:
    return workspace.review(
        review_id, task_id=task_id, review_kind="authorization", decision=decision,
        attempt_id=attempt_id, family_digest=family_digest, profile_ref=profile_ref,
        transition={"from": from_stage, "to": to_stage}, expires_at=expires_at,
        authorization_scope="single_use",
    )
