# Branch merge — 4.0.1 candidate

This is an unreleased Core + MCP candidate. `fcop-mcp` requires
`fcop>=4.0.1,<4.1.0`. Existing 4.0.0 releases are not changed.

## Tools and Core boundaries

- `create_branch(root_task_id, workspace_id, operation_id, sender, recipient,
  subject, body, priority="P2")` delegates to `Project.create_task(branch_of=...)`.
  It returns the original creation result plus root/branch IDs and the latest
  partial family inspection. Existing create-task idempotency semantics apply.
- `inspect_family(root_task_id)` delegates to `Project.inspect_family`, read-only
  under one family lock. Branches sort by TASK ID; each head includes REPORT ID,
  current attempt ID and full-file SHA-256. It returns Root state, readiness
  reasons and existing convergence references. No recovery runs during reads.
- `merge_branches(root_task_id, workspace_id, expected_family_digest,
  branch_report_heads, conclusion, conflict_resolution, operation_id, sender,
  recipient)` delegates to the same-named Core primitive. `branch_report_heads`
  maps each Branch TASK ID to its exact current REPORT ID. Digest covers the full
  REPORT bytes, including attempt identity; paths and mtimes are not authority.

Missing attempts/REPORTs cause a **null** digest, never an alternate hash. A
nonterminal Branch contributes a `BRANCH_NOT_TERMINAL` reason; a Root not done
contributes `ROOT_NOT_DONE`. `merge_ready` is false while any prerequisite fails.
A null digest cannot be used for merge. A digest may exist before all tasks are
terminal; its presence alone is not permission to merge.

## Example

After creating two Branches, submit their REPORTs and obtain the normal trusted
Profile-backed approvals that put both Branches and Root in done. Inspection and
merge do not perform those transitions on the caller's behalf.

```python
family = project.inspect_family(root_task_id=root_id)
assert family["merge_ready"]
result = project.merge_branches(
    workspace_id=workspace_id, root_task_id=root_id,
    expected_family_digest=family["family_digest"],
    branch_report_heads={b["task_id"]: b["report_head"]["report_id"]
                         for b in family["branches"]},
    conclusion="Combine the parser and documentation results.",
    conflict_resolution="Both use the reviewed interface; no unresolved conflicts.",
    operation_id="release-review-42", sender="PM", recipient="PM",
)
assert result["review_ref"] == result["review_id"]
```

The executable real-stdio example is
`tests/test_fcop_mcp/test_branch_merge_stdio.py`; it creates Root + two Branches,
calls all three tools, checks stale-digest zero writes and restarts the MCP process.

## Equivalence, conflicts and recovery

Core formats the supplied conclusion/conflict explanation as two Markdown
sections. Formal request identity includes workspace, Root, family digest,
sender/recipient, sorted exact references, normalized body and supplied optional
REVIEW fields; `operation_id` is a durable binding, not content. Unicode is NFC,
line endings LF and body termination one LF. Omitted and null optional fields
are equivalent. Reference ordering is irrelevant; duplicate references are errors.
Different sender/recipient or different conclusions are not equivalent requests.

All `write_review(review_kind="convergence")` calls enter the same Core path.
Legacy callers without operation_id get a deterministic request-derived identity.
To express equivalent content through legacy append, use the same body:
`## Merge conclusion\n\n<conclusion>\n\n## Conflict resolution\n\n<resolution>\n`.
Legacy optional Root REPORT references remain supported.

Same operation + same request returns the same REVIEW with `existing: true`.
Same operation + different request returns `OPERATION_ID_CONFLICT`. Another
operation with equivalent content reuses the REVIEW; competing content for the
same Root/digest returns `FAMILY_CONVERGENCE_MISMATCH`, with no fact writes.
Retries of a committed operation return its historical result, not a claim that
the family is still current. New operations must validate the current family.

Core lock order is a workspace merge-operation lock, then the existing family
lock exactly once. REVIEW no-overwrite publication is the linearization point.
A Core-private PREPARED receipt holds the exact validated REVIEW bytes, identity,
content/request hashes, family entries and bound operation IDs. Existing fsync,
no-overwrite publication, durable receipt replacement and fault boundaries are
reused. A retry reconciles the exact target bytes and commits the receipt. A
missing committed target or damaged/conflicting evidence fails closed with
`RECOVERY_REQUIRED`; it never synthesizes a second REVIEW. A PREPARED operation
with no visible target revalidates the live family before completing publication.
These are append receipts, not lifecycle movement receipts or MCP-side records.

Convergence does not change the canonical family content, so old/new result
digests are equal. It does not archive Root, consume a lifecycle authorization,
or decide which Branch is semantically correct. There is no database, background
worker, adapter lock, or adapter receipt store.
