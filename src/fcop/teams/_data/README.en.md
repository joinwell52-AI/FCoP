# FCoP Preset Team Templates

This directory ships the stock **template library** bundled inside the
`fcop` Python package, giving users without role docs a copy-and-run
starting point that already follows the FCoP protocol.

## Directory layout

```
teams/
├── README.md          # Chinese
├── README.en.md       # this file
├── index.json         # machine-readable index
├── solo/              # single-AI collaboration  [0.6.4]
├── dev-team/          # software development
├── media-team/        # content media
├── mvp-team/          # startup MVP
└── qa-team/           # dedicated testing
```

## Three-layer docs per team

```
<team>/
├── README.md / README.en.md                     # entry: positioning / ADMIN / flow
├── TEAM-ROLES.md / TEAM-ROLES.en.md             # layer 1: who owns what
├── TEAM-OPERATING-RULES.md / .en.md             # layer 2: when to dispatch / report / escalate
└── roles/
    ├── {LEADER}.md / .en.md                     # layer 3: leader role
    ├── {ROLE-2}.md / .en.md
    ├── {ROLE-3}.md / .en.md
    └── {ROLE-4}.md / .en.md
```

- **Entry**: understand what the team does, where `ADMIN` fits, how flow works.
- **Layer 1**: role boundaries.
- **Layer 2**: operating rules (dispatch, report, escalate, high-risk actions).
- **Layer 3**: single-role depth.

Generality decreases, detail increases. The first two layers are enough
to run the team; Layer 3 is read only when playing that role.

## Five preset modes

| Mode/Team | Leader | Roles (AI) | Scenario | Entry tool |
|-----------|--------|------------|----------|------------|
| `solo` *(0.6.4)* | `ME` | `ME` (1) | Single AI; ADMIN ↔ ME direct | `init_solo(role_code="ME")` |
| `dev-team` | `PM` | `PM / DEV / QA / OPS` | Software dev, fix & release | `init_project(team="dev-team")` |
| `media-team` | `PUBLISHER` | `PUBLISHER / COLLECTOR / WRITER / EDITOR` | Topic → draft → publish | `init_project(team="media-team")` |
| `mvp-team` | `MARKETER` | `MARKETER / RESEARCHER / DESIGNER / BUILDER` | Startup MVP, idea validation | `init_project(team="mvp-team")` |
| `qa-team` | `LEAD-QA` | `LEAD-QA / TESTER / AUTO-TESTER / PERF-TESTER` | Independent testing, multi-line parallel | `init_project(team="qa-team")` |

`solo` has 1 AI role; the other four teams have 4 each. Plus the human
`ADMIN` → 2 to 5 parties total.

`ADMIN` is the **human administrator**. FCoP reserves it at the protocol
level — it is **not written into `fcop.json.roles`** and **not placed in
`roles/`**. The ADMIN description lives in each team's own `README.md`.

## Custom teams

Don't want a preset? Use `init_custom(team_name="...", roles="...",
leader="...")` to roll your own. FCoP ships **no templates** for custom
teams, but the recommended path is: agent reads the closest preset (full
bundle from `fcop://teams/<closest-preset>`), renames the roles, and
writes the result into `docs/agents/shared/`. This matches the
letter-to-admin.md section "custom teams have no charter; copy a sample".

## How to use

Two paths:

### A. Initialize a new project

One sentence to the agent:

> Initialize the project with the preset team `<team-id>`.

Agent calls `init_project(team="<team-id>", lang="en" or "zh")`. The
three-layer docs are deployed to `docs/agents/shared/`, and `fcop.json`
is set up.

### B. Existing project — deploy or upgrade role docs only

One sentence:

> Deploy the `<team-id>` role docs into this project.

Agent calls `deploy_role_templates(team="<team-id>", lang="en" or "zh")`.
Legacy flat role files (like `PM-01.md`) are automatically archived into
`.fcop/migrations/<timestamp>/`, then the new three-layer structure is
written on top. Archive first, safe to roll back.

## URI conventions

Bundled docs are exposed as MCP resources:

- `fcop://teams` — index
- `fcop://teams/{team}` — team README
- `fcop://teams/{team}/TEAM-ROLES` — role boundaries (layer 1)
- `fcop://teams/{team}/TEAM-OPERATING-RULES` — operating rules (layer 2)
- `fcop://teams/{team}/{role}` — single role (layer 3)
  - e.g. `fcop://teams/dev-team/PM`, `fcop://teams/qa-team/LEAD-QA`
  - Legacy URIs like `fcop://teams/dev-team/PM-01` still resolve (backward compat)

All URIs accept a language suffix: `?lang=zh` (default) or `?lang=en`.

## Not in here

- Real task files (`TASK-*.md`) — produced at runtime, live in `docs/agents/tasks/`.
- Real reports / issues (`REPORT-*.md` / `ISSUE-*.md`) — same.
- Project-specific norms — put them in the project's own `docs/agents/shared/`,
  don't modify these bundled templates.

The goal of this template library is to make FCoP **work out of the box**,
not to prescribe that every project must look exactly like this. Once a
project is running, it will evolve its own specifics — but entry,
boundary, exit should stay in the FCoP shape.
