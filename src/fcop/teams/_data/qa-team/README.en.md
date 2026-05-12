---
protocol: fcop
version: 1
kind: spec
sender: TEMPLATE
recipient: TEAM
team: qa-team
doc_id: TEAM-README
updated_at: 2026-05-12
---

# qa-team — Dedicated Testing Team

**Use case**: pre-release dedicated testing, regression, automation, perf verification.
**Leader**: `LEAD-QA`
**Roles**: `LEAD-QA` · `TESTER` · `AUTO-TESTER` · `PERF-TESTER` (4 AI roles)

## Team positioning

`qa-team` is FCoP's stock "independent testing" template, suitable for
larger projects with high quality bars that need a QA crew separated from
the dev team.

Unlike the single `QA` role in `dev-team`, `qa-team` splits testing into
three specialized lines — **functional**, **automation**, **performance** —
coordinated by `LEAD-QA`.

## Who is ADMIN

`ADMIN` is the **human administrator**, not an AI role, and does **not**
belong under `roles/`.

- `ADMIN` is the only external input — test goals, quality bars, priorities.
- `ADMIN` **is not written into `fcop.json.roles`** — reserved at the protocol level.
- The team does not talk to `ADMIN` directly; everything flows through
  `ADMIN ↔ LEAD-QA` task files.
- Only two directions:
  - `ADMIN -> LEAD-QA`: test goals / quality bar
  - `LEAD-QA -> ADMIN`: verdicts / risk assessment

> **Cross-team scenario**: when working alongside `dev-team` (e.g. receiving
> test tasks from `dev-team`'s `PM`), `PM` is treated as an upstream entry
> point, but formal verdicts are still returned by `LEAD-QA`.

4 AI members (`LEAD-QA / TESTER / AUTO-TESTER / PERF-TESTER`) plus 1 human `ADMIN` = 5 parties.

## Collaboration flow

```
ADMIN ──test goals──▶  LEAD-QA ──functional──▶ TESTER
  ▲                    │
  │                    ├──automation──▶       AUTO-TESTER
  │                    │
  │                    └──performance──▶      PERF-TESTER
  │
  └──verdicts / risk report──  LEAD-QA
```

`LEAD-QA` is the single external exit point and the "ship / hold" decider.

## Document layers (three)

| Layer | File | Purpose |
|---|---|---|
| Entry | `README.md` (this file) | Positioning, ADMIN, flow |
| Layer 1 | `TEAM-ROLES.md` | Who owns what |
| Layer 2 | `TEAM-OPERATING-RULES.md` | When to dispatch / report / escalate |
| Layer 3 | `roles/{LEAD-QA,TESTER,AUTO-TESTER,PERF-TESTER}.md` | Single-role depth |

## Quick start

### ADMIN initializes the project

> Initialize the project with the preset team `qa-team`.

Agent will call `init_project(team="qa-team", lang="en")`.

### Agent assigned a role

Read: `README.md` → `TEAM-ROLES.md` → `TEAM-OPERATING-RULES.md` → `roles/<your role>.md`.

## Relation to other preset teams

- `dev-team` = software development (leader: `PM`, with one general-purpose `QA` role)
- `media-team` = content creation (leader: `PUBLISHER`)
- `mvp-team` = startup MVP (leader: `MARKETER`)
- `qa-team` = dedicated testing (this team)

`dev-team`'s `QA` suits small projects with low specialization demand;
`qa-team` suits scenarios needing an independent quality team across
functional / automation / performance lines.

---

## Tool Quick Reference

| Tool | Scenario |
|---|---|
| `fcop_audit(scope="new")` | Self-check after `init_*` on a new project |
| `fcop_audit(scope="upgrade")` | Verify after `pip install -U fcop` upgrade |
| `fcop_audit(scope="takeover")` | First step when inheriting an unfamiliar project |
| `fcop_report()` | View project binding, version, and alert summary |
| `fcop_list_alerts(status="open")` | View governance alert inbox |

> For detailed leader tool quick reference, see the "Tool Quick Reference" section
> at the end of `roles/<leader>.md`.
