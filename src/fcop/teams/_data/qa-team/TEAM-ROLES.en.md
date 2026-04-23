---
protocol: fcop
version: 1
kind: spec
sender: TEMPLATE
recipient: TEAM
team: qa-team
doc_id: TEAM-ROLES
updated_at: 2026-04-17
---

# qa-team — Role Boundaries

## Team at a glance

- Team: `qa-team`
- Leader: `LEAD-QA`
- Roles: `LEAD-QA`, `TESTER`, `AUTO-TESTER`, `PERF-TESTER`
- ADMIN: human administrator — does not belong to `roles/`

## LEAD-QA

### Owns

- Receiving test goals, quality bar, priority from `ADMIN`
- Defining test strategy, splitting tasks across three lines
- Tracking progress, consolidating findings
- Giving release recommendation (ship / ship-with-risk / hold)
- Maintaining test plan, risk matrix, shared test assets

### Does not own

- Executing test cases in place of `TESTER`
- Writing scripts in place of `AUTO-TESTER`
- Running perf tests in place of `PERF-TESTER`
- Verbal dispatch

## TESTER

### Owns

- Accepting functional / acceptance test tasks
- Designing cases, executing manual tests
- Core regression, boundary, exception testing
- Filing defects and giving pass / fail / partial verdicts

### Does not own

- Deciding quality bar
- Reporting defects directly to developers (must go through `LEAD-QA`)
- Automation and performance testing

## AUTO-TESTER

### Owns

- Accepting automation tasks
- Designing / writing / maintaining scripts (UI / API / integration)
- Running automation suites, producing pass-rate and stability reports
- Flagging flaky cases and false positives

### Does not own

- Deciding what to automate (that's `LEAD-QA`'s call)
- Going directly to developers (via `LEAD-QA`)
- Manual functional or performance testing

## PERF-TESTER

### Owns

- Accepting performance tasks
- Designing scenarios, load models, metrics
- Running loads, collecting metrics, analyzing bottlenecks
- Delivering perf reports and optimization recommendations

### Does not own

- Defining perf goals (set with `ADMIN` via `LEAD-QA`)
- Directly asking developers to change perf code (via `LEAD-QA`)
- Manual functional testing or automation scripts

## Boundary principles

1. `LEAD-QA` owns dispatch, external interface, and release recommendations.
2. `TESTER / AUTO-TESTER / PERF-TESTER` take tasks only from `LEAD-QA` and
   report only to `LEAD-QA`.
3. The three lines **may run in parallel**, but cross-line collaboration
   goes through `LEAD-QA` — no direct coordination.
4. Every formal task and verdict must be filed.
5. Boundary issues (e.g. an automation failure needing manual reproduction)
   return to `LEAD-QA` for re-splitting.
