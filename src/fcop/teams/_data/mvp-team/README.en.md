---
protocol: fcop
version: 1
kind: spec
sender: TEMPLATE
recipient: TEAM
team: mvp-team
doc_id: TEAM-README
updated_at: 2026-04-17
---

# mvp-team — Startup MVP Team

**Use case**: 0-to-1 product, fast idea validation, MVP, market testing.
**Leader**: `MARKETER`
**Roles**: `MARKETER` · `RESEARCHER` · `DESIGNER` · `BUILDER` (4 AI roles)

## Team positioning

`mvp-team` is FCoP's stock "startup crew" template for early validation:
idea → is there a market → what's the minimum → does it run. Each role
owns one gate; `MARKETER` consolidates everything into "advance to next
round or not" decisions.

The reason the leader is `MARKETER`, not `BUILDER`, is that the MVP
bottleneck is "is there a market", not "can we build it".

## Who is ADMIN

`ADMIN` is the **human administrator** (usually the founder), not an AI
role, and does **not** belong under `roles/`.

- `ADMIN` is the only external input — vision, target market, constraints.
- `ADMIN` **is not written into `fcop.json.roles`** — reserved at the protocol level.
- The team does not talk to `ADMIN` directly; everything flows through
  `ADMIN ↔ MARKETER` task files.
- Only two directions:
  - `ADMIN -> MARKETER`: vision / constraints / decisions
  - `MARKETER -> ADMIN`: milestones / blockers / results

4 AI members (`MARKETER / RESEARCHER / DESIGNER / BUILDER`) plus 1 human `ADMIN` = 5 parties.

## Collaboration flow

```
ADMIN ──vision──▶  MARKETER ──research──▶ RESEARCHER
  ▲                 │
  │                 ├──design (+findings)──▶ DESIGNER
  │                 │
  │                 └──build (+PRD)──▶       BUILDER
  │
  └──milestones / growth results──  MARKETER
```

`MARKETER` is the single external exit point and the "advance or pivot"
decider. `RESEARCHER / DESIGNER / BUILDER` all return to `MARKETER`.

## Document layers (three)

| Layer | File | Purpose |
|---|---|---|
| Entry | `README.md` (this file) | Positioning, ADMIN, flow |
| Layer 1 | `TEAM-ROLES.md` | Who owns what |
| Layer 2 | `TEAM-OPERATING-RULES.md` | When to dispatch / report / escalate |
| Layer 3 | `roles/{MARKETER,RESEARCHER,DESIGNER,BUILDER}.md` | Single-role depth |

## Quick start

### ADMIN initializes the project

> Initialize the project with the preset team `mvp-team`.

Agent will call `init_project(team="mvp-team", lang="en")`.

### Agent assigned a role

Read: `README.md` → `TEAM-ROLES.md` → `TEAM-OPERATING-RULES.md` → `roles/<your role>.md`.

## Relation to other preset teams

- `dev-team` = software development (leader: `PM`)
- `media-team` = content creation (leader: `PUBLISHER`)
- `mvp-team` = startup MVP (this team)
- `qa-team` = dedicated testing (leader: `LEAD-QA`)

`mvp-team` differs from `dev-team`: `dev-team` assumes the direction is
set and tasks are defined; `mvp-team` assumes direction is unknown and
validated as you go — which is why the leader is a `MARKETER`, not a `BUILDER`.
