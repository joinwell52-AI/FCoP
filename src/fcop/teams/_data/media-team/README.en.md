---
protocol: fcop
version: 1
kind: spec
sender: TEMPLATE
recipient: TEAM
team: media-team
doc_id: TEAM-README
updated_at: 2026-04-17
---

# media-team — Content Media Team

**Use case**: topic selection, material gathering, drafting, editing, publishing.
**Leader**: `PUBLISHER`
**Roles**: `PUBLISHER` · `COLLECTOR` · `WRITER` · `EDITOR` (4 AI roles)

## Team positioning

`media-team` is FCoP's stock "standard content crew" template, suited for
newsletters, blogs, channel publications, or video scripts. Every step from
topic to final piece is filed, making sourcing, revision, review, and
archival traceable.

## Who is ADMIN

`ADMIN` is the **human administrator**, not an AI role, and does **not**
belong under `roles/`.

- `ADMIN` is the only external input — topics, directions, brand
  requirements, and approvals come from `ADMIN`.
- `ADMIN` **is not written into `fcop.json.roles`** — FCoP reserves it at
  the protocol level.
- The team does not talk to `ADMIN` directly; everything flows through
  `ADMIN ↔ PUBLISHER` task files.
- Only two directions:
  - `ADMIN -> PUBLISHER`: topic/request — `TASK-*-ADMIN-to-PUBLISHER.md`
  - `PUBLISHER -> ADMIN`: draft/status return — `TASK-*-PUBLISHER-to-ADMIN.md`

4 AI members (`PUBLISHER / COLLECTOR / WRITER / EDITOR`) plus 1 human `ADMIN` = 5 parties.

## Collaboration flow

```
ADMIN ──topic──▶  PUBLISHER ──collect──▶ COLLECTOR
  ▲                │
  │                ├──draft (+material)──▶ WRITER
  │                │
  │                └──edit──▶               EDITOR
  │
  └──final review / publish──  PUBLISHER
```

`PUBLISHER` is the single external exit point and the final editorial gate.
`COLLECTOR / WRITER / EDITOR` all return to `PUBLISHER` — never to `ADMIN`
directly, and never to each other (all cross-role handoffs go through
`PUBLISHER`).

## Document layers (three)

| Layer | File | Purpose |
|---|---|---|
| Entry | `README.md` (this file) | Team positioning, ADMIN explanation, flow |
| Layer 1 | `TEAM-ROLES.md` | What each role owns and does not own |
| Layer 2 | `TEAM-OPERATING-RULES.md` | When to dispatch, how to report, when to escalate |
| Layer 3 | `roles/{PUBLISHER,COLLECTOR,WRITER,EDITOR}.md` | Single-role depth |

## Quick start

### ADMIN initializes the project

> Initialize the project with the preset team `media-team`.

Agent will call `init_project(team="media-team", lang="en")`.

### Agent assigned a role

Read in order: `README.md` → `TEAM-ROLES.md` → `TEAM-OPERATING-RULES.md` → `roles/<your role>.md`.

## Relation to other preset teams

- `dev-team` = software development (leader: `PM`)
- `media-team` = content creation (this team)
- `mvp-team` = startup MVP (leader: `MARKETER`)
- `qa-team` = dedicated testing (leader: `LEAD-QA`)
