---
protocol: fcop
version: 1
kind: spec
sender: TEMPLATE
recipient: TEAM
team: solo
doc_id: TEAM-README
updated_at: 2026-04-26
---

# solo — Single-AI Collaboration Mode

**Use case**: one AI helping you do work; no team to dispatch to.
**Leader**: `ME` (also the only worker)
**Roles**: `ME` (1 AI) + `ADMIN` (you, the human)

## Team positioning

`solo` is a **first-class** FCoP collaboration mode — not a "lite version"
of the team modes. It solves the most common scenario: "I'm alone, but I
still want FCoP's file discipline":

- No need to keep four Cursor windows alive;
- No need to remember leader/member dispatch order;
- **But Rule 0.a / 0.b / 0.c apply at full strength** — every instruction
  still lands in `TASK-*-ADMIN-to-ME.md`, every result still lands in
  `REPORT-*-ME-to-ADMIN.md`, every objection still goes through
  `ISSUE-*` or `.fcop/proposals/`.

> Solo isn't "skip the protocol"; solo is "both protocol roles
> (ADMIN + ME) are present, but only one AI client lives on this machine."

## Who is ADMIN

`ADMIN` is the **human administrator**, not an AI role, and does **not**
belong under `roles/`.

- `ADMIN` is the only external input source.
- `ADMIN` is **not** written into `fcop.json.roles` — FCoP reserves it.
- In solo mode `ADMIN ↔ ME` is a **direct interface** (no PM/Leader
  intermediary), but it still goes through the file protocol — no verbal
  dispatch, no verbal verdicts.

## Collaboration link

```
ADMIN  ──new task──▶  ME  ──artifacts──▶  workspace/<slug>/
  ▲                   │
  │                   └──report──▶  REPORT-*-ME-to-ADMIN.md
  │                                          │
  └──read / verify / next ticket  ◀──────────┘
```

`ADMIN` interfaces only with `ME`; every task must have a matching report.

## Document layers (3-tier)

| Layer | File | Purpose |
|---|---|---|
| Entry | `README.md` (this file) | Team positioning, ADMIN explanation, link diagram |
| Layer 1 | `TEAM-ROLES.md` | What `ME` does and does not do; ADMIN boundary |
| Layer 2 | `TEAM-OPERATING-RULES.md` | How tasks are written, how reports look, when to escalate, how solo "self-review" works |
| Layer 3 | `roles/ME.md` | `ME`'s core duties (incl. **workflow hard constraint**: write task → do → write report → archive) |

Solo also has all three layers — not for symmetry. `roles/ME.md`
documents specifically how Rule 0.b is enforced when there's only one AI:
the file system stands in for the second role.

## Quick start

### Case A: ADMIN wants to init a project in solo mode

Tell the agent in plain English:

> Initialize this project in solo mode, role code `ME`.

The agent will call `init_solo(role_code="ME", lang="en")`, deploying the
three-layer documents into `docs/agents/shared/`, plus
`fcop.json` / `LETTER-TO-ADMIN.md` / `workspace/`.

### Case B: An agent has been assigned the `ME` role

Read in this order:

1. `README.md` (this file — team big picture)
2. `TEAM-ROLES.md` (role boundaries / ADMIN boundary)
3. `TEAM-OPERATING-RULES.md` (operating rules, self-review)
4. `roles/ME.md` (**workflow hard constraint** + deep duties)

When you catch yourself thinking "I'll just do this directly", go back to
`roles/ME.md` § "Core workflow (hard constraint)".

## Relationship with other preset teams

- **solo** = single AI (this team)
- `dev-team` = 4-person software dev (PM / DEV / QA / OPS)
- `media-team` = 4-person content team (PUBLISHER / COLLECTOR / WRITER / EDITOR)
- `mvp-team` = 4-person startup MVP (MARKETER / RESEARCHER / DESIGNER / BUILDER)
- `qa-team` = 4-person dedicated testing (LEAD-QA / TESTER / AUTO-TESTER / PERF-TESTER)

Solo and the four multi-role teams are **parallel samples**, not an
inheritance hierarchy. Switching from solo to a team requires a fresh
`init_project`; FCoP archives the old `shared/` to
`.fcop/migrations/<timestamp>/` automatically.
