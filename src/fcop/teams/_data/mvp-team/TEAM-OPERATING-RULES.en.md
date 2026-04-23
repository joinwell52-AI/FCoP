---
protocol: fcop
version: 1
kind: rules
sender: TEMPLATE
recipient: TEAM
team: mvp-team
doc_id: TEAM-OPERATING-RULES
updated_at: 2026-04-17
---

# mvp-team — Operating Rules

## 1. Basic routing

1. `ADMIN ↔ MARKETER` is the only external interface.
2. `RESEARCHER / DESIGNER / BUILDER` take tasks only from `MARKETER` and
   report only to `MARKETER`.
3. Cross-role handoffs are not allowed — all go through `MARKETER`.
4. Cross-role needs return to `MARKETER` for re-splitting.

## 2. Dispatch rules

### MARKETER does directly

- Vision clarification, goal definition, constraint ranking
- Task splitting, milestone planning
- "Advance / pivot / kill" decisions
- Landing pages, cold start, growth experiments
- Phase reports to `ADMIN`

### MARKETER dispatches to RESEARCHER

- Market analysis, competitive teardown
- User interviews, surveys, data collection
- Opportunity / risk assessment

### MARKETER dispatches to DESIGNER

- PRD (dispatched with **reviewed research findings**)
- User flow, interaction, key screens
- Feasibility / compliance / measurability assessment

### MARKETER dispatches to BUILDER

- Tech selection, architecture
- MVP build, environment, deployment
- Tech debt and limits documentation

## 3. Handoff rules

1. Every handoff is "task + previous-round artifact". No direct pulls.
2. `MARKETER` attaches research findings to `MARKETER-to-DESIGNER` tasks.
3. `BUILDER` receives the PRD routed through `MARKETER`, not from `DESIGNER` directly.
4. Every handoff leaves a traceable file record.

## 4. Report rules

1. Every task has a matching report.
2. Reports state: status, artifact, key findings, uncertainty, next step.
3. Formal reports from `RESEARCHER / DESIGNER / BUILDER` target `MARKETER`.
4. `MARKETER` consolidates and reports milestones to `ADMIN`.
5. Verbal sync is not a report.

## 5. Thread and cadence

1. One `thread_key` (a hypothesis's full validation loop) has one active driver — `MARKETER`.
2. Other roles handle only their subtasks.
3. Return to `MARKETER` promptly.
4. `MARKETER` decides advance or pivot.

## 6. When to escalate to ADMIN

- Key hypothesis rejected — pivot needed
- Resources (time / budget / people) insufficient for next round
- Compliance / legal / market-access risk
- "Kill / continue / pivot" decision needed
- External partnership or paid resources need approval

## 7. High-risk action rules

Record and confirm before execution:

- Public launch to real users
- Features touching payment / personal data / accounts
- Brand-facing communication (landing-page public release, press)
- Spending: services, paid ads, outsourcing

Spend, brand reach, user data → **return to `ADMIN`** by default.

## 8. Documents and archival

1. Flow files in `tasks/`, `reports/`, `issues/`.
2. Findings, PRDs, architecture decisions in `shared/`.
3. After a round, `MARKETER` archives and leaves a retro in `shared/`.
4. `shared/` docs may update in place; tasks/reports are append-only.

## 9. Operating stance

MVP is about "validate the most critical assumption with minimum cost",
not "build the most complete thing":

- `MARKETER` owns dispatch, growth, decisions
- `RESEARCHER` turns hypotheses into evidence
- `DESIGNER` turns evidence into plans
- `BUILDER` turns plans into something usable

Clear hypothesis → reliable validation → grounded decision → next round worth starting.
