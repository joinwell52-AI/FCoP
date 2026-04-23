---
protocol: fcop
version: 1
kind: rules
sender: TEMPLATE
recipient: TEAM
team: qa-team
doc_id: TEAM-OPERATING-RULES
updated_at: 2026-04-17
---

# qa-team — Operating Rules

## 1. Basic routing

1. `ADMIN ↔ LEAD-QA` is the only external interface.
2. `TESTER / AUTO-TESTER / PERF-TESTER` take tasks only from `LEAD-QA` and
   report only to `LEAD-QA`.
3. The three lines do not coordinate directly — all via `LEAD-QA`.
4. Cross-team collaboration (e.g. with `dev-team`'s `PM` on defects) is
   handled by `LEAD-QA`.

## 2. Dispatch rules

### LEAD-QA does directly

- Test-goal clarification, quality-bar definition
- Test strategy, risk matrix, priority
- Cross-line task splitting
- Release / hold recommendation
- Phase reports to `ADMIN`

### LEAD-QA dispatches to TESTER

- Manual functional testing
- Core regression testing
- Boundary / exception testing
- Acceptance testing

### LEAD-QA dispatches to AUTO-TESTER

- Automation script writing / maintenance
- Automation suite execution and reporting
- Extending regression automation

### LEAD-QA dispatches to PERF-TESTER

- Load-scenario design
- Load model and metric definition
- Load execution and bottleneck analysis

## 3. Parallel execution rules

1. The three lines may run in parallel within a single test round.
2. Each role handles only its own subtask; they do not dispatch to one another.
3. Intermediate artifacts route through `LEAD-QA` before other lines consume them.
4. E.g. a defect found by manual testing does not directly request automation
   coverage — return to `LEAD-QA` to decide.

## 4. Report rules

1. Every task has a matching report.
2. Reports state: status, case count, pass / fail, key defects, next step.
3. Formal reports from the three lines target `LEAD-QA`.
4. `LEAD-QA` consolidates and reports release recommendation and risk to `ADMIN`.
5. Verbal sync is not a report.

## 5. Defect handling

1. On defect discovery, open an `ISSUE-*` with reproduction steps and impact.
2. Dispatching fixes is decided by `LEAD-QA` (cross-team coordination included).
3. `TESTER` does not go directly to developers — all via `LEAD-QA`.
4. Retest tasks after fixes are re-dispatched by `LEAD-QA`.

## 6. Thread and cadence

1. One `thread_key` (a test object's full validation) has one active driver — `LEAD-QA`.
2. Line roles handle only their subtasks.
3. Return to `LEAD-QA` promptly.
4. `LEAD-QA` decides release-readiness.

## 7. When to escalate to ADMIN

- Critical defect severe enough to recommend a hold
- Quality bar needs adjustment
- Perf targets not met but business wants to ship
- Test environment / data unavailable
- Cross-team fix blocked

## 8. High-risk action rules

Record and confirm before execution:

- Production / pre-prod load testing
- Tests involving real user data
- Clearing test-environment data or instances
- Proceeding with release despite a "hold" recommendation

## 9. Documents and archival

1. Flow files in `tasks/`, `reports/`, `issues/`.
2. Test plans, risk matrices, automation specs, perf baselines in `shared/`.
3. After each round, `LEAD-QA` archives and leaves a retro.
4. `shared/` docs may update in place; tasks/reports are append-only.

## 10. Operating stance

The goal is not to test everything but, with finite resources, to make
sure critical risks surface, get recorded, and get decided:

- `LEAD-QA` owns dispatch, decisions, external
- `TESTER` owns manual flows and boundaries
- `AUTO-TESTER` hardens what's been validated into regression
- `PERF-TESTER` surfaces performance problems before release

Three independent lines, one consolidated verdict → a release recommendation that holds up.
