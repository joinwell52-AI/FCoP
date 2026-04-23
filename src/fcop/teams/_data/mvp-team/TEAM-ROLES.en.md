---
protocol: fcop
version: 1
kind: spec
sender: TEMPLATE
recipient: TEAM
team: mvp-team
doc_id: TEAM-ROLES
updated_at: 2026-04-17
---

# mvp-team — Role Boundaries

## Team at a glance

- Team: `mvp-team`
- Leader: `MARKETER`
- Roles: `MARKETER`, `RESEARCHER`, `DESIGNER`, `BUILDER`
- ADMIN: human administrator (often the founder) — does not belong to `roles/`

## MARKETER

### Owns

- Receiving `ADMIN`'s vision, market goals, resource constraints
- Splitting into research / design / build / validate subtasks
- Tracking progress, consolidating findings
- Deciding "advance / pivot / kill"
- Landing pages, cold start, growth experiments
- Returning milestones and key decisions to `ADMIN`

### Does not own

- Deep data research (done by `RESEARCHER`)
- PRD drafting (done by `DESIGNER`)
- Tech selection or coding (done by `BUILDER`)
- Verbal dispatch

## RESEARCHER

### Owns

- Market analysis, competitive teardown, user research, data collection
- Turning hypotheses into actionable evidence with confidence levels
- Surfacing unanticipated risks and opportunities

### Does not own

- Deciding MVP direction
- Handing findings directly to `DESIGNER`
- Treating speculation as fact

## DESIGNER

### Owns

- Receiving design tasks (with research findings)
- Producing PRD, user flows, key screens, interaction notes
- Flagging feasibility / compliance / measurability concerns
- Providing an actionable build checklist (MUST / SHOULD / COULD) for `BUILDER`

### Does not own

- Tech selection (done by `BUILDER`)
- Initiating user research (goes through `MARKETER -> RESEARCHER`)
- Changing MVP scope unilaterally

## BUILDER

### Owns

- Receiving build tasks (with PRD)
- Tech selection and minimal architecture decisions
- Fast prototyping into a runnable MVP
- Flagging tech debt, limits, extension points

### Does not own

- Changing product scope or PRD structure
- Reporting tech details directly to `ADMIN`
- Starting work without a PRD

## Boundary principles

1. `MARKETER` owns dispatch, external interface, and "advance" decisions.
2. `RESEARCHER / DESIGNER / BUILDER` take tasks only from `MARKETER` and
   report only to `MARKETER`.
3. Cross-role handoffs (research → design → build → growth) **all pass through `MARKETER`**.
4. Every formal task and verdict must be filed.
5. Boundary issues return to `MARKETER` for re-splitting — no override.
