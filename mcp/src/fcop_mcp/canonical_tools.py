"""Canonical MCP manifest: names, metadata, signatures and thin Core adapters.

The decorated functions are the sole registry input. Schemas and documentation
are derived from their signatures; there is no independent display tool list.
"""
from __future__ import annotations

from typing import Any

from fcop import Project

MANIFEST: dict[str, dict[str, Any]] = {}


def canonical(category: str):
    def register(fn):
        MANIFEST[fn.__name__] = dict(
            name=fn.__name__, id=fn.__name__, category=category, owner="FCoP Core",
            status="canonical", since="4.0.5", replacement=None, deprecation=None,
            description=fn.__doc__, handler=fn,
        )
        return fn
    return register


@canonical("workspace")
def init_workspace(core: Project, profile: str | None = None) -> dict:
    """Create only a canonical FCoP 4.0 workspace at the server-bound root. An optional explicit profile is a reference, never executable authority."""
    return core.create_workspace(profiles=[] if profile is None else [profile])


@canonical("workspace")
def inspect_workspace(core: Project) -> dict:
    """Inspect protocol identity, envelopes, lifecycle, families and recovery facts without repair."""
    from fcop.workspace import inspect_workspace as inspect
    return inspect(core.path)


@canonical("workspace")
def validate_workspace(core: Project) -> dict:
    """Deterministically validate canonical workspace facts through Core validators; never repair or consult host/runtime state."""
    from fcop.workspace import validate_workspace as validate
    return validate(core.path)


@canonical("task")
def create_task(core: Project, workspace_id: str, operation_id: str, sender: str,
                recipient: str, subject: str, body: str, priority: str = "P2",
                references: list[str] | None = None, parent: str | None = None,
                branch_of: str | None = None, thread_key: str | None = None,
                risk_level: str | None = None) -> dict:
    """Create a TASK using Core T1 and its workspace-scoped operation identity. Repeated requests retain Core idempotency semantics."""
    fields = dict(workspace_id=workspace_id, operation_id=operation_id, sender=sender,
                  recipient=recipient, subject=subject, body=body, priority=priority,
                  references=references or [])
    fields.update({k: v for k, v in dict(parent=parent, branch_of=branch_of,
                  thread_key=thread_key, risk_level=risk_level).items() if v is not None})
    return core.create_task(**fields)


@canonical("task")
def claim_task(core: Project, task_id: str, actor: str) -> dict:
    """Request Core T2 inbox to active; actor records attribution and grants no authority."""
    return core.transition(task_id=task_id, from_stage="inbox", to_stage="active", tool="claim_task", actor=actor)


@canonical("task")
def submit_task(core: Project, task_id: str, actor: str, report_ref: str) -> dict:
    """Request Core T3 active to review with the explicit current-attempt REPORT."""
    return core.transition(task_id=task_id, from_stage="active", to_stage="review", tool="submit_task", actor=actor, report_ref=report_ref)


@canonical("task")
def approve_task(core: Project, task_id: str, actor: str, report_ref: str,
                 review_ref: str, authorization_ref: str, profile_ref: str) -> dict:
    """Request Core T4 review to done using independently validated review and authorization evidence."""
    return core.transition(task_id=task_id, from_stage="review", to_stage="done", tool="approve_task", actor=actor, report_ref=report_ref, review_ref=review_ref, authorization_ref=authorization_ref, profile_ref=profile_ref)


@canonical("task")
def reject_task(core: Project, task_id: str, actor: str, report_ref: str,
                review_ref: str, authorization_ref: str, profile_ref: str) -> dict:
    """Request Core T5 review to active; Core validates evidence and advances the attempt."""
    return core.transition(task_id=task_id, from_stage="review", to_stage="active", tool="reject_task", actor=actor, report_ref=report_ref, review_ref=review_ref, authorization_ref=authorization_ref, profile_ref=profile_ref)


@canonical("task")
def reopen_task(core: Project, task_id: str, actor: str, review_ref: str,
                authorization_ref: str, profile_ref: str) -> dict:
    """Request Core T6 done to active with explicit reopen evidence and authorization."""
    return core.transition(task_id=task_id, from_stage="done", to_stage="active", tool="reopen_task", actor=actor, review_ref=review_ref, authorization_ref=authorization_ref, profile_ref=profile_ref)


@canonical("task")
def archive_task(core: Project, task_id: str, actor: str,
                 authorization_ref: str, profile_ref: str, review_ref: str | None = None,
                 family_digest: str | None = None) -> dict:
    """Request Core T7 done to archive; Core enforces authorization and family convergence."""
    evidence = {} if family_digest is None else {"family_digest": family_digest}
    if review_ref is not None:
        evidence["review_ref"] = review_ref
    return core.transition(task_id=task_id, from_stage="done", to_stage="archive", tool="archive_task", actor=actor, authorization_ref=authorization_ref, profile_ref=profile_ref, **evidence)


@canonical("task")
def inspect_task(core: Project, task_id: str) -> dict:
    """Read Core lifecycle, current attempt and transition evidence for a TASK."""
    return core.inspect_state(task_id=task_id)


@canonical("task")
def list_tasks(core: Project, stage: str | None = None, sender: str | None = None,
               recipient: str | None = None, parent: str | None = None,
               branch_of: str | None = None, offset: int = 0, limit: int | None = None) -> dict:
    """List validated canonical TASK facts, optionally filtered by stage or relations."""
    from fcop.workspace import list_envelopes
    return list_envelopes(core.path, "TASK", filters=dict(stage=stage, sender=sender, recipient=recipient, parent=parent, branch_of=branch_of), offset=offset, limit=limit)


@canonical("task")
def read_task(core: Project, task_id: str) -> dict:
    """Read a canonical TASK by its typed identity through Core."""
    return core.read_task(task_id=task_id)


@canonical("branch")
def create_branch(core: Project, root_task_id: str, workspace_id: str, operation_id: str,
                  sender: str, recipient: str, subject: str, body: str, priority: str = "P2") -> dict:
    """Create a branch TASK through Core T1 with an explicit branch_of relation."""
    return core.create_task(workspace_id=workspace_id, operation_id=operation_id,
                           sender=sender, recipient=recipient, subject=subject, body=body,
                           priority=priority, branch_of=root_task_id)


@canonical("branch")
def inspect_family(core: Project, root_task_id: str) -> dict:
    """Read Core family membership, REPORT heads, digest and convergence readiness."""
    return core.inspect_family(root_task_id=root_task_id)


@canonical("branch")
def merge_branches(core: Project, root_task_id: str, workspace_id: str,
                   expected_family_digest: str, branch_report_heads: dict[str, str],
                   conclusion: str, conflict_resolution: str, operation_id: str,
                   sender: str, recipient: str) -> dict:
    """Record the caller's convergence decision atomically in Core; never choose winners or archive the root."""
    return core.merge_branches(root_task_id=root_task_id, workspace_id=workspace_id,
                              expected_family_digest=expected_family_digest,
                              branch_report_heads=branch_report_heads, conclusion=conclusion,
                              conflict_resolution=conflict_resolution, operation_id=operation_id,
                              sender=sender, recipient=recipient)


@canonical("envelope-write")
def write_report(core: Project, workspace_id: str, sender: str, recipient: str,
                 subject_ref: str, attempt_id: str, body: str, result: str,
                 report_kind: str = "final", references: list[str] | None = None) -> dict:
    """Append a Core REPORT for the explicit TASK attempt; reporting does not accept or archive work."""
    return core.write_report(workspace_id=workspace_id, sender=sender, recipient=recipient,
                             subject_ref=subject_ref, attempt_id=attempt_id, body=body,
                             result=result, report_kind=report_kind, references=references or [])


@canonical("envelope-write")
def write_issue(core: Project, workspace_id: str, sender: str, recipient: str,
                subject_ref: str, body: str, severity: str, references: list[str] | None = None) -> dict:
    """Append a Core ISSUE with explicit workspace and subject identity."""
    return core.write_issue(workspace_id=workspace_id, sender=sender, recipient=recipient,
                            subject_ref=subject_ref, body=body, severity=severity, references=references or [])


@canonical("envelope-write")
def write_review(core: Project, workspace_id: str, sender: str, recipient: str,
                 subject_ref: str, review_kind: str, decision: str, body: str,
                 attempt_id: str | None = None, references: list[str] | None = None,
                 family_digest: str | None = None, authorization_ref: str | None = None,
                 profile_ref: str | None = None, transition: dict[str, str] | None = None,
                 issued_at: str | None = None, expires_at: str | None = None,
                 authorization_scope: str | None = None, operation_kind: str | None = None,
                 issuer_proof: Any = None) -> dict:
    """Append a typed Core REVIEW. Authority is evaluated only by trusted startup Profile evaluators."""
    fields = dict(workspace_id=workspace_id, sender=sender, recipient=recipient,
                  subject_ref=subject_ref, review_kind=review_kind, decision=decision,
                  body=body, references=references or [])
    fields.update({k: v for k, v in dict(attempt_id=attempt_id, family_digest=family_digest,
                  authorization_ref=authorization_ref, profile_ref=profile_ref, transition=transition,
                  issued_at=issued_at, authorization_scope=authorization_scope,
                  operation_kind=operation_kind, issuer_proof=issuer_proof).items() if v is not None})
    if review_kind == "authorization":
        fields["expires_at"] = expires_at
    return core.write_review(**fields)


@canonical("envelope-read")
def list_reports(core: Project, subject_ref: str | None = None, sender: str | None = None,
                  attempt_id: str | None = None, head_only: bool = False,
                  offset: int = 0, limit: int | None = None) -> dict:
    """List REPORTs through Core, including exact attempt and head selection semantics."""
    return {"items": core.list_reports(subject_ref=subject_ref, sender=sender,
            attempt_id=attempt_id, head_only=head_only, offset=offset, limit=limit)}


@canonical("envelope-read")
def read_report(core: Project, filename_or_id: str) -> dict:
    """Read a canonical REPORT through Core identity resolution."""
    return core.read_report(filename_or_id=filename_or_id)


@canonical("envelope-read")
def list_issues(core: Project, sender: str | None = None, subject_ref: str | None = None,
                severity: str | None = None, offset: int = 0, limit: int | None = None) -> dict:
    """List validated canonical ISSUE facts, with deterministic filtering and pagination."""
    from fcop.workspace import list_envelopes
    return list_envelopes(core.path, "ISSUE", filters=dict(sender=sender, subject_ref=subject_ref, severity=severity), offset=offset, limit=limit)


@canonical("envelope-read")
def list_reviews(core: Project, sender: str | None = None, subject_ref: str | None = None,
                 review_kind: str | None = None, decision: str | None = None,
                 offset: int = 0, limit: int | None = None) -> dict:
    """List validated canonical REVIEW facts; listing grants no authorization."""
    from fcop.workspace import list_envelopes
    return list_envelopes(core.path, "REVIEW", filters=dict(sender=sender, subject_ref=subject_ref, review_kind=review_kind, decision=decision), offset=offset, limit=limit)


@canonical("envelope-read")
def read_review(core: Project, review_id: str) -> dict:
    """Read a validated REVIEW from its canonical bucket without changing its decision."""
    return core.inspect_state(envelope_path=f"fcop/reviews/{review_id}.md")


@canonical("review-decision")
def mark_human_approved(core: Project, review_id: str, decision: str, approver: str,
                        profile_ref: str, from_stage: str, to_stage: str,
                        issued_at: str, expires_at: str | None,
                        attempt_id: str | None = None, family_digest: str | None = None,
                        issuer_proof: Any = None, comment: str = "") -> dict:
    """Ask Core to append independent authorization evidence. Caller-supplied approver text alone is never authority; expires_at must be explicit."""
    return core.mark_human_approved(review_id=review_id, decision=decision, approver=approver,
        profile_ref=profile_ref, from_stage=from_stage, to_stage=to_stage, issued_at=issued_at,
        expires_at=expires_at, attempt_id=attempt_id, family_digest=family_digest,
        issuer_proof=issuer_proof, comment=comment)
