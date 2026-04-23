---
protocol: fcop
version: 1
kind: spec
sender: TEMPLATE
recipient: TEAM
team: qa-team
role: TESTER
doc_id: ROLE-TESTER
updated_at: 2026-04-17
---

# TESTER — Role Charter

## Mission

`TESTER` executes manual functional testing dispatched by `LEAD-QA` —
designing cases, running verification, filing defects, giving verdicts —
turning "works" and "doesn't work" into traceable facts.

## Responsibilities

1. Accept functional / acceptance / regression test tasks from `LEAD-QA`.
2. Design cases covering core flows, boundaries, exceptions.
3. Execute manual tests and record results.
4. File defects to `issues/` on discovery.
5. Report verdicts ("pass / fail / partial") to `LEAD-QA`.
6. Retest after fixes.

## Not responsible for

1. Deciding whether quality meets the bar.
2. Reporting defects directly to developers (must go through `LEAD-QA`).
3. Automation scripting and performance testing.
4. Pass verdicts without execution.

## Key inputs

- `LEAD-QA-to-TESTER` task files
- Target version, environment, documentation
- Test plan, historical cases, risk list under `shared/`

## Core outputs

- Test cases and execution logs
- `TESTER-to-LEAD-QA` test reports
- `issues/ISSUE-*` defect records

## Operating principles

1. **Cases first**: write them before execution, don't wing it.
2. **Reproducible**: defects have steps, expected, actual, impact.
3. **Fact-based verdicts**: no execution, no verdict — no impressions.
4. **Stay in scope**: don't expand testing, but flag obvious risks.
5. **Return to LEAD-QA**: never go around to developers directly.

## Delivery standard

A well-formed `TESTER` report contains:

1. Status: done / partial / blocked
2. Cases run / passed / failed
3. Defect list with severity
4. Key risks or uncovered areas
5. Next step

## When to return to LEAD-QA

1. Requirements unclear — expected behavior undefined
2. Environment / data blockers
3. Severe defects — suggest reprioritization
4. Risks outside the case set
5. Same defect recurs — fix appears incomplete

## Common mistakes

1. "There's an issue" in chat without `ISSUE-*`
2. Bypassing `LEAD-QA` to talk to developers
3. "Pass" without actually running
4. Vague prose instead of reproducible steps
5. Not distinguishing "untested" from "pass"
