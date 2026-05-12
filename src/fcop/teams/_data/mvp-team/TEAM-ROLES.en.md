---
protocol: fcop
version: 1
kind: spec
sender: TEMPLATE
recipient: TEAM
team: mvp-team
doc_id: TEAM-ROLES
updated_at: 2026-05-12
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

---

## Protocol Evolution (v1.0 ~ v1.4)

| Version | Change | Affected roles |
|---|---|---|
| v1.0 | REVIEW envelope: high-risk tasks generate `REVIEW-*.md`, require ADMIN approval | leader / all |
| v1.1 | `risk_level` field: `low / medium / high`; `needs_human` triggers human approval | leader (on dispatch) |
| v1.3 | `fcop_audit()`: protocol health-check tool, produces `INSPECTION-*.md` | leader / ADMIN |
| v1.3 | GAL (Governance Alert Layer): `fcop_create_alert` / `fcop_list_alerts` | leader |
| v1.4 | `supersedes:` field: file-level correction link (distinct from `parent:` derivation) | all |
| v1.4 | Write-side tools require explicit project binding (`set_project_dir()`) | MCP Server layer |

> See the corresponding `roles/` file for each leader's detailed tool quick reference.
