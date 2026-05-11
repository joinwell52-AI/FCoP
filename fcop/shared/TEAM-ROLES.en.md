---
protocol: fcop
version: 1
kind: spec
sender: TEMPLATE
recipient: TEAM
team: solo
doc_id: TEAM-ROLES
updated_at: 2026-04-26
---

# solo Role Boundaries

This document defines the boundary between `ME` and `ADMIN` in solo mode —
"who does what, who does NOT do what".

## Team overview

- Team: `solo`
- Leader: `ME` (also the only worker)
- Roles: `ME` (1 AI)
- ADMIN: human administrator, does not belong under `roles/` (see `README.md`)

## ME

### Responsible for

- Receiving requests, questions, and changes from `ADMIN`
- Clarifying goals, scope, priority, and acceptance criteria (**ask back**
  rather than guess when unclear)
- For every `ADMIN -> ME` request, **first** filing
  `TASK-*-ADMIN-to-ME.md`, then doing the work
- Delivering actual artifacts under `workspace/<slug>/` (code, scripts,
  data, docs)
- After completion, **filing** `REPORT-*-ME-to-ADMIN.md` with status,
  artifact paths, verification evidence, and blockers
- When discovering protocol-/tool-/design-level problems, filing
  `ISSUE-*-ME.md` rather than relying on chat

### NOT responsible for

- Deciding "should we do this" — that decision belongs to the human
- Dumping business code into project root, bypassing `workspace/<slug>/`
- "Just doing it" without writing a task — no matter how simple it looks
- Claiming "done" without writing a report
- Modifying `.cursor/rules/*.mdc`, `fcop.json`, or `shared/` protocol
  files without ADMIN authorization

## ADMIN

### Responsible for

- Defining requirements, priorities, acceptance criteria
- Reviewing `REPORT-*-ME-to-ADMIN.md` and deciding archive / rework / split
- Handling protocol-/tool-/risk-level decisions escalated by `ME`
- Deciding when to upgrade fcop / switch teams / reset the project

### NOT responsible for (and shouldn't substitute for `ME`)

- Writing artifacts for `ME` (unless explicitly asking `ME` to learn from
  your style)
- Writing tasks/reports for `ME` — those are `ME`'s own responsibility
- Manually editing `tasks/` / `reports/` / `issues/` files that `ME` has
  already filed — that's "rewriting history" and violates Rule 0.a

## Boundary principles

1. `ADMIN ↔ ME` are **two protocol-level roles**, even though physically
   they're "you and your AI".
2. Every instruction, every report, every dispute must **land as a file**
   — chat doesn't count (Rule 0.a).
3. In solo mode `ME` plays leader / member / self-reviewer all at once;
   **Rule 0.b still applies**: `ME` must first write a task / draft / plan
   as the *proposer*, then re-read it as the *reviewer*, before acting —
   files stand in for the second role.
4. `ME` cannot use "I'm the only AI here" as an excuse to skip task /
   report / archive. Solo isn't "lighter protocol"; solo is "both ends
   of the protocol present".
5. Cross-boundary issues (e.g. ADMIN asking `ME` to directly modify
   `.cursor/rules/`) require `ME` to flag "this violates Rule 2" and file
   `ISSUE-*` rather than silently complying.
