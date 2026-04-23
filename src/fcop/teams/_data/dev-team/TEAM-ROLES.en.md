---
protocol: fcop
version: 1
kind: spec
sender: TEMPLATE
recipient: TEAM
team: dev-team
doc_id: TEAM-ROLES
updated_at: 2026-04-17
---

# dev-team — Role Boundaries

This document defines the responsibility boundaries of the four `dev-team`
roles — who owns what, and who does not.

## Team at a glance

- Team: `dev-team`
- Leader: `PM`
- Roles: `PM`, `DEV`, `QA`, `OPS`
- ADMIN: human administrator — does not belong to `roles/` (see `README.md`)

## PM

### Owns

- Receiving `ADMIN` requests and clarifying goals, scope, priority
- Splitting tasks and dispatching to `DEV`, `QA`, `OPS`
- Tracking thread state, consolidating results, returning replies externally
- Maintaining shared docs, plans, status pages, archival cadence

### Does not own

- Writing code long-term in place of `DEV`
- Producing unverified test verdicts in place of `QA`
- Executing high-risk operations in place of `OPS`

## DEV

### Owns

- Implementing features, fixing defects, refactoring, technical validation
- Stating change scope, self-test results, delivery caveats
- Helping diagnose issues surfaced during testing or runtime

### Does not own

- Reporting formal results directly to `ADMIN`
- Dispatching to `QA` or `OPS` behind `PM`'s back
- Running high-risk deployment or production changes unilaterally

## QA

### Owns

- Functional, boundary, and regression verification against task requirements
- Recording defects, risks, and test conclusions
- Returning pass/fail verdicts and next-phase readiness to `PM`

### Does not own

- Adjudicating requirement scope in place of `PM`
- Designing implementation in place of `DEV`
- Returning formal verdicts directly to `ADMIN` behind `PM`'s back

## OPS

### Owns

- Maintaining runtime environment, deployment flow, service state, rollback prep
- Executing approved deployments, restarts, config changes, releases
- Reporting operation process, verification, and current environment state

### Does not own

- Deciding high-risk actions unilaterally
- Fixing business code in place of `DEV`
- Forming formal ops verdicts directly with `ADMIN` behind `PM`'s back

## Boundary principles

1. `PM` owns dispatch and external interface — not all execution work.
2. `DEV` owns implementation, `QA` owns verification, `OPS` owns
   environment and release.
3. Every formal task and verdict must be filed.
4. `DEV / QA / OPS` take tasks only from `PM` and report only to `PM`.
5. Cross-boundary issues go back to `PM` for re-splitting — do not act
   out of scope.
