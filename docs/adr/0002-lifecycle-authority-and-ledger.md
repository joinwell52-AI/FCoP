# ADR-0002: Lifecycle Authority, Rail Kernel, and Agent-Facing Ledger

## Status

Proposed

## Date

2026-05-31

## Context

FCoP 3.0 introduces lifecycle buckets such as:

```txt
fcop/_lifecycle/inbox/
fcop/_lifecycle/active/
fcop/_lifecycle/review/
fcop/_lifecycle/done/
fcop/_lifecycle/archive/
```

These buckets externalize task lifecycle state through the filesystem. However, the TASK-20260531-237 thread exposed a serious implementation gap:

- OPS produced a valid `REPORT-20260531-002-OPS-to-PM.md` with `status: done`.
- PM later produced a final summary report, but the root TASK and child TASK remained in `_lifecycle/active/`.
- `REPORT status=done` was confused with lifecycle completion.
- ReportGate generated a premature `blocked` report even though a valid done report existed.
- PM waited for ADMIN to say "汇总" instead of automatically reviewing the child report and submitting the root task for review.
- `list_tasks()` and the actual filesystem state diverged.
- Agents became confused by having to reason across `_lifecycle/`, `reports/`, `issues/`, YAML status fields, and references.

The root cause is not that lifecycle buckets are wrong. The root cause is that agents were exposed to lifecycle mechanics that should belong to the runtime.

In FCoP, files are the truth, but agents should not be responsible for moving files between lifecycle buckets.

## Decision

FCoP implementations MUST separate three responsibilities:

```txt
Agent        -> writes and reads business facts
Ledger       -> exposes stable role/task/thread views
Rail Kernel  -> owns lifecycle movement and filesystem MV
```

The lifecycle buckets are runtime-owned state projections. They are not the primary work queue for agents.

Agents SHOULD read a stable ledger view and write TASK / REPORT / ISSUE facts. Agents MUST NOT directly move files between lifecycle buckets.

Lifecycle movement MUST be performed only by a dedicated lifecycle authority, called here:

```txt
LifecycleRail
LifecycleKernel
MutationKernel
```

Any implementation may choose the exact name, but there must be a single authority for lifecycle mutation.

## Core Principle

```txt
REPORT done is evidence.
TASK done is lifecycle state.
Only the lifecycle authority may move lifecycle state.
```

Therefore:

```txt
write_report(status=done) != task done
write_report(status=done) -> evidence available
submit_review(task_id)    -> active -> review
approve_review(task_id)   -> review -> done
archive_task(task_id)     -> done -> archive
```

## Agent Boundary

Agents MAY:

- read TASK facts
- read REPORT facts
- read ISSUE facts
- read ledger views
- write TASK files through approved tools
- write REPORT files through approved tools
- write ISSUE files through approved tools
- express business status such as `done`, `blocked`, `in_progress`

Agents MUST NOT:

- directly move files between `_lifecycle/` buckets
- treat `_lifecycle/active/` as their only task source
- treat `REPORT status=done` as equivalent to `TASK done`
- create duplicate final PM-to-ADMIN reports for the same root task without a supersede chain
- bypass `review`
- archive tasks directly

## Lifecycle Authority

The lifecycle authority owns the following operations:

```txt
dispatch_task(task_id)
submit_review(task_id)
approve_review(task_id)
reject_review(task_id, reason)
archive_task(task_id)
supersede_report(old_report_id, new_report_id)
invalidate_report(report_id, reason)
```

Only these operations may cause lifecycle MV.

Recommended lifecycle transitions:

```txt
inbox  -> active   via dispatch_task
active -> review   via submit_review
review -> done     via approve_review
review -> active   via reject_review
done   -> archive  via archive_task
```

`done` and `archive` MUST NOT be reached directly from `active` for normal reviewed work.

## Ledger as Agent-Facing Reality

Agents need a stable work surface. They should not have to search across lifecycle buckets and reports manually.

A FCoP runtime SHOULD provide:

```txt
fcop/ledger/
  tasks.jsonl
  reports.jsonl
  threads.jsonl
  views/
    ADMIN.inbox.md
    ADMIN.review.md
    PM.todo.md
    OPS.todo.md
    DEV.todo.md
    QA.todo.md
```

The ledger is not a replacement for files. It is a deterministic index rebuilt from disk facts:

- TASK files
- REPORT files
- ISSUE files
- YAML frontmatter
- references
- current lifecycle bucket location

The ledger MUST be rebuildable from the filesystem.

The ledger SHOULD record inconsistencies, for example:

```json
{"task_id":"TASK-20260531-237","yaml_state":"done","bucket":"active","inconsistent":true}
```

Role views SHOULD answer the question:

```txt
What should this role do next?
```

Instead of forcing an agent to infer state from physical directories.

## Suggested Directory Contract

Current FCoP 3.0 implementations may keep TASK files inside `_lifecycle/` buckets and REPORT files inside `fcop/reports/`.

This ADR does not require immediately adding `fcop/tasks/`.

Minimum required addition:

```txt
fcop/ledger/
  tasks.jsonl
  reports.jsonl
  threads.jsonl
  views/
```

The lifecycle directory remains valid, but it becomes runtime-owned:

```txt
fcop/_lifecycle/    # Rail Kernel projection, not agent primary workspace
fcop/reports/       # report facts
fcop/issues/        # issue facts
fcop/ledger/        # agent-facing externalized ledger
```

## PM Settlement Rule

When a PM-dispatched child task receives a valid role report:

```yaml
sender: OPS | DEV | QA
recipient: PM
status: done
references:
  - TASK-xxx-PM-to-ROLE
```

The runtime and PM workflow MUST proceed as follows:

1. Mark child delivery as received in the ledger.
2. Present `pending_pm_review` in `ledger/views/PM.todo.md`.
3. PM reviews the child report.
4. PM updates the unique PM-to-ADMIN summary report for the root task.
5. The lifecycle authority calls `submit_review(root_task_id)`.
6. The root task moves from `active` to `review`.
7. ADMIN reviews and calls `approve_review` or `reject_review`.

PM MUST NOT wait for ADMIN to say "汇总" once all required child reports are available.

## PM-to-ADMIN Report Uniqueness

For one root task, there SHOULD be one canonical PM-to-ADMIN summary report.

If an `in_progress` PM-to-ADMIN report already exists, PM MUST update that report instead of creating another final report.

If a new report is unavoidable, the runtime MUST create a supersede chain:

```yaml
status: superseded
superseded_by: REPORT-xxxx-PM-to-ADMIN
```

and the replacement report MUST include:

```yaml
supersedes:
  - REPORT-xxxx-PM-to-ADMIN
```

## ReportGate Boundary

ReportGate MUST NOT race the normal reporting path.

ReportGate MAY only generate an automatic blocked report when all of the following are true:

1. Worker session has ended.
2. A settle delay has passed.
3. The ledger has been rebuilt or reports have been directly scanned.
4. No valid report exists for the task.
5. The task is not already pending PM review.

Hard rule:

```txt
If a valid done report exists for the same task_id + sender + recipient,
ReportGate MUST NOT generate an automatic blocked report.
```

A valid report is identified by YAML frontmatter, not by filename alone:

```yaml
sender: <task assignee>
recipient: <task requester>
status: done
references:
  - <canonical task id>
```

## list_tasks Contract

`list_tasks()` MUST use the ledger or directly rebuild from disk facts. It MUST NOT rely only on stale memory, stale cache, or unbound project context.

At minimum, `list_tasks()` must scan:

```txt
fcop/_lifecycle/inbox/
fcop/_lifecycle/active/
fcop/_lifecycle/review/
fcop/_lifecycle/done/
fcop/_lifecycle/archive/
```

and parse YAML frontmatter.

If a cache exists, it is an optimization only. It is not the source of truth.

## Acceptance Criteria

A minimal ADMIN -> PM -> OPS test must pass:

```txt
ADMIN writes root TASK to PM
PM dispatches child TASK to OPS
OPS writes REPORT to PM with status=done
```

Expected behavior:

1. OPS report is indexed in `ledger/reports.jsonl`.
2. ReportGate does not generate a duplicate blocked report.
3. `ledger/views/PM.todo.md` shows `pending_pm_review`.
4. PM updates the unique PM-to-ADMIN summary report.
5. Lifecycle authority calls `submit_review(root_task_id)`.
6. Root task moves `active -> review`.
7. Child task moves to a reviewed/completed state according to implementation policy.
8. `ledger/views/ADMIN.review.md` shows the root task awaiting approval.
9. ADMIN approval moves the root task `review -> done`.
10. Archiving moves the task `done -> archive`.
11. `list_tasks()` matches ledger and filesystem facts.

## Consequences

Positive:

- Agents no longer need to understand physical lifecycle buckets.
- PM no longer waits for ADMIN to manually say "汇总" once child reports are present.
- ReportGate cannot prematurely mark completed work as blocked.
- Lifecycle MV becomes auditable and centralized.
- UI can display lifecycle state from ledger + rail projection, not agent guesswork.

Tradeoffs:

- Requires a ledger builder.
- Requires lifecycle syscalls.
- Requires report resolver logic after `write_report()`.
- Requires careful migration from existing mixed v2/v3 layouts.

## Summary

FCoP externalizes reality through files, but lifecycle movement must not be pushed into agent cognition.

Agents write facts.
The ledger exposes role-specific reality.
The rail kernel moves lifecycle state.
ADMIN approves governance transitions.

This is the required boundary for reliable FCoP 3.0 execution.
