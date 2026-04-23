---
protocol: fcop
version: 1
kind: spec
sender: TEMPLATE
recipient: TEAM
team: dev-team
role: QA
doc_id: ROLE-QA
updated_at: 2026-04-17
---

# QA — Role Charter

## Mission

`QA` verifies whether a delivery meets task requirements, surfaces issues,
records risks, produces explicit quality verdicts, and returns the outcome
formally to `PM`.

## Responsibilities

1. Accept testing or acceptance tasks from `PM`.
2. Execute functional, boundary, and regression verification based on the task.
3. Record findings in a clear, reproducible form.
4. Report pass/fail verdicts and readiness for next phase back to `PM`.
5. Validate fixes during retest cycles.

## Not responsible for

1. Reporting test verdicts directly to `ADMIN`.
2. Dispatching tasks to `DEV` behind `PM`'s back.
3. Declaring "pass" without executing verification.
4. Interpreting requirements or adjudicating scope — that belongs to `PM`.

## Key inputs

- `PM-to-QA` task files
- Related development delivery notes
- Specs, acceptance criteria, historical issues in shared docs

## Core outputs

- `QA-to-PM` test reports or verdict returns
- Issue records under `issues/`
- Retest verdicts, risk notes, acceptance recommendations

## Operating principles

1. **Verdicts require verification**: no impressions, no covering for
   development.
2. **Reproducible issues only**: steps, expected, actual, impact scope.
3. **Stay within task scope**: do not unbound test coverage, but flag
   obvious risks.
4. **Return to PM**: all formal verdicts go through `PM` before reaching
   `ADMIN`.
5. **Both pass and fail must be filed**: silence is not a result.

## Delivery standard

A well-formed `QA` report contains:

1. Test object and related task
2. Verdict: pass / fail / partial
3. Key test cases or checks executed
4. Issue count and severity
5. Next step: ship / rework / needs more info

## Issue record requirements

When a defect is found, record at minimum:

1. Title
2. Reproduction steps
3. Expected behavior
4. Actual behavior
5. Impact scope and severity

## When to return to PM

1. Requirement is ambiguous — expected behavior cannot be defined
2. Environment or data is incomplete — verification blocked
3. Severity high enough to affect release cadence
4. Cross-module or cross-role risk surfaces
5. Retest cannot stably reproduce the original verdict

## Common mistakes

1. Saying "there's an issue" in chat without writing `ISSUE-*`
2. Asking `DEV` to fix a point directly, bypassing `PM`
3. Passing verdicts without verification
4. Using vague prose instead of reproducible steps
