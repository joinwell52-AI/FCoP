---
protocol: fcop
version: 1
kind: rules
sender: TEMPLATE
recipient: TEAM
team: dev-team
doc_id: TEAM-OPERATING-RULES
updated_at: 2026-04-17
---

# dev-team — Operating Rules

This document defines how the team works — when to dispatch, how to report,
when to escalate.

## 1. Basic routing

1. `ADMIN ↔ PM` is the only external interface.
2. `DEV / QA / OPS` take tasks only from `PM` and report only to `PM`.
3. `DEV ↔ QA`, `DEV ↔ OPS`, `QA ↔ OPS` cross-dispatch is not allowed.
4. Cross-role needs go back to `PM`, who decides whether to split a new task.

## 2. Dispatch rules

### PM does directly

The following are handled by `PM` directly, no sub-dispatch:

- Requirement clarification
- Priority ranking
- Task splitting
- Progress consolidation
- Phase reports to `ADMIN`
- Shared doc maintenance

### PM dispatches to DEV

- Feature development
- Bug fix
- Code refactor
- Technical validation or prototype

### PM dispatches to QA

- Functional verification
- Regression verification
- Acceptance check
- Defect retest

### PM dispatches to OPS

- Environment preparation
- Deployment / release
- Service restart
- Config change
- Runtime state check
- Rollback execution

## 3. Report rules

1. Every task must have a matching report.
2. Reports must state: status, what's done, blockers, next step.
3. Formal reports from `DEV / QA / OPS` all target `PM`.
4. `PM` consolidates and sends a unified phase verdict or final result
   to `ADMIN`.
5. Verbal sync is not a report — it must be filed.

## 4. Issue handling

1. When a problem is found, file an `ISSUE-*` or explicitly state the
   blocker in a report.
2. Cross-role impact is coordinated by `PM`.
3. Whether to rework or reprioritize is decided by `PM`.
4. Quality issues are raised by `QA`, fixed by `DEV`, environment issues
   are handled by `OPS`.

## 5. Thread and cadence

1. At any moment, one `thread_key` has only one active driver — by default, `PM`.
2. Other roles handle only their received subtasks; they do not drive the
   whole thread unless explicitly handed over by `PM`.
3. Finish a subtask and return to `PM` promptly — no backlog, no silence.
4. `PM` decides whether a thread is closed, continues splitting, or is archived.

## 6. When to escalate to ADMIN

Escalate to `ADMIN` when:

- Scope changes materially
- Priority conflict needs arbitration
- High-risk action needs second approval
- External dependency blocks original plan
- Release risk exceeds prior estimate
- Resource or time trade-off is required

## 7. High-risk action rules

The following must be recorded and confirmed before execution:

- Restarting production services
- Modifying network, firewall, gateway, Nginx, CI/CD
- Deleting data, logs, or cache
- Publishing to trunk or public artifact registry

No rollback plan → do not execute.

## 8. Documents and archival

1. Flow files go in `tasks/`, `reports/`, `issues/`.
2. Shared knowledge goes in `shared/`.
3. Closed threads are archived by `PM`.
4. `shared/` docs may be updated in place; tasks and reports follow
   append-only history.

## 9. Operating stance

The goal of `dev-team` is not to keep every role busy, but to keep every
role working within a clear boundary:

- `PM` owns dispatch and the single exit point
- `DEV` owns implementation
- `QA` owns verification
- `OPS` owns environment and release

Clear boundaries keep threads stable; stable threads keep the team
handing off cleanly.
