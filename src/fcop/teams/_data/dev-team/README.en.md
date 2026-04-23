---
protocol: fcop
version: 1
kind: spec
sender: TEMPLATE
recipient: TEAM
team: dev-team
doc_id: TEAM-README
updated_at: 2026-04-17
---

# dev-team — Software Development Team

**Use case**: regular software development, feature delivery, fix releases.
**Leader**: `PM`
**Roles**: `PM` · `DEV` · `QA` · `OPS` (4 AI roles)

## Team positioning

`dev-team` is FCoP's stock "standard development crew" template. Role
boundaries, dispatch rules, and escalation conditions are all filed from
day one, so agents know the boundaries, who pairs with whom, and where
verdicts go.

## Who is ADMIN

`ADMIN` is the **human administrator**, not an AI role, and does **not**
belong under `roles/`.

- `ADMIN` is the only external input source — requests, goals, decisions,
  and approvals come from `ADMIN`.
- `ADMIN` **is not written into `fcop.json.roles`** — FCoP reserves this
  identity at the protocol level.
- The team does not talk to `ADMIN` directly; everything flows through
  `ADMIN ↔ PM` task files.
- Only two directions:
  - `ADMIN -> PM`: dispatch — `TASK-*-ADMIN-to-PM.md`
  - `PM -> ADMIN`: report — `TASK-*-PM-to-ADMIN.md`

So the team has 4 AI members (`PM / DEV / QA / OPS`) plus 1 human `ADMIN` —
5 parties collaborating total.

## Collaboration flow

```
ADMIN  ──request──▶  PM  ──dispatch──▶  DEV
  ▲                  │
  │                  ├──test task──▶   QA
  │                  │
  │                  └──deploy task──▶ OPS
  │
  └──phase report / final delivery──  PM
```

`PM` is the team's single external exit point; `DEV / QA / OPS` return
verdicts to `PM` only — never to `ADMIN` directly.

## Document layers (three)

| Layer | File | Purpose |
|---|---|---|
| Entry | `README.md` (this file) | Team positioning, ADMIN explanation, flow |
| Layer 1 | `TEAM-ROLES.md` | What each role owns and does not own |
| Layer 2 | `TEAM-OPERATING-RULES.md` | When to dispatch, how to report, when to escalate |
| Layer 3 | `roles/{PM,DEV,QA,OPS}.md` | Single-role depth: mission, inputs, outputs, standards, common mistakes |

Generality decreases, detail increases. The first two layers are enough
to run the team; Layer 3 is read deeply only when you actually play that
role.

## Quick start

If you are reading this README, you are likely in one of two situations:

### A. ADMIN wants to initialize the project with this crew

Tell the agent in one sentence:

> Initialize the project with the preset team `dev-team`.

The agent will call `init_project(team="dev-team", lang="en")`, deploy
the three-layer docs into `docs/agents/shared/`, and set up `fcop.json`.

### B. An agent has been assigned a role in this team

You should read:

1. This `README.md` (team overview)
2. `TEAM-ROLES.md` (boundaries)
3. `TEAM-OPERATING-RULES.md` (rules)
4. `roles/<your role>.md` (role depth)

Those four files are enough to work by the protocol. When you hit a
boundary issue, revisit Section 1 and Section 5 of `TEAM-OPERATING-RULES.md`.

## Relation to other preset teams

- `dev-team` = software development (this team)
- `media-team` = content creation (leader: `PUBLISHER`)
- `mvp-team` = startup MVP (leader: `MARKETER`)
- `qa-team` = dedicated testing (leader: `LEAD-QA`)

The four presets are **parallel samples**, not inheritance. To switch,
re-run `init_project` — do not mix multiple role naming conventions in
one project.
