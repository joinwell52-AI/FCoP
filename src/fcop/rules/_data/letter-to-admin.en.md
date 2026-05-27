# A Letter from FCoP to ADMIN — User Manual

Hi ADMIN.

I'm **FCoP** (File-based Coordination Protocol) — a protocol that lets
you and an AI team collaborate through **files**. Your one job:
**tell me how many people this project has and how they split the work.**

> **v3.2.4 summary** (current PyPI package, 2026-05-27; **protocol rules remain 3.2.3**):
> - **Packaging fix**: restores UTF-8 in wheel `fcop-protocol.mdc` (PyPI 3.2.3 is bad);
>   use `pip install -U "fcop>=3.2.4"`, do not reinstall 3.2.3.
> - **fcop-mcp**: PyPI `"FCoP (protocol)"` URL → `docs/getting-started.en.md`;
>   long description synced to 45 tools / v3 `_lifecycle/`.
>
> **v3.2.3 summary** (2026-05-23; deep archiving / v3 lifecycle + v2.0.0 philosophical era):
> - **"Two-diagram era"**: `2.0.0` is a *philosophical* major release.
>   All v1.x public APIs keep working (per ADR-0003 additive expansion);
>   the major bump records that FCoP now formally acknowledges **two**
>   defining diagrams: the *execution stack* (5-layer vertical, stable
>   since v1.x) and the *FCoP Semantic Evolution Loop* (7-node closed
>   loop, newly canonicalised in v2.0). Full explainer:
>   `fcop-rules.mdc` end of the "Seven Core Concepts" section /
>   `fcop-protocol.mdc` `## Two-Diagram Duality` section.
> - **Rule 4.6 · Internal vs external archives**: new soft convention
>   for `fcop/internal/` (opt-in bucket for team-internal decision
>   drafts / logs / retros) versus `docs/` + `essays/` (existing
>   convention for external-facing publications). Internal docs carry
>   an `internal-only` declaration block at the top (v1 syntax); the
>   missing-declaration check runs as a P3 (suggestion) audit
>   violation — **non-blocking**, advisory only.
> - **`Project.init(deploy_internal_template=...)` opt-in**: new
>   parameter to seed the `fcop/internal/` bucket; defaults to *off*
>   (backward-compatible). New public symbol
>   `fcop.rules.get_internal_readme(lang)`.
> - **Three onboarding modes** — `init_solo` (Solo) / `init_project`
>   (preset team) / `init_custom` (custom). ADMIN must choose explicitly;
>   agents may not default.
> - **Protocol inspection**: after setup, run
>   `fcop_audit(scope="takeover")` (existing project) or
>   `fcop_audit(scope="new")` (fresh project). The tool generates an
>   INSPECTION report listing compliance gaps and suggested remediation
>   steps. For unfamiliar projects, **this is your first move**. After
>   upgrading, run `fcop_audit(scope="upgrade")` to detect role documents
>   lagging the installed version (RULE_DOC_DRIFT).
> - **`fcop_audit` bucket exemption (v2.0 fix)**: scans now skip
>   `fcop/log/`, `fcop/**/_archive/`, and `**/legacy-non-protocol/` —
>   archive buckets no longer trigger spurious `P1-002
>   misplaced_envelope` violations. Reports also carry a new
>   `violation_file_count` (distinct file count) field.
> - **Governance alerts — GAL**: `fcop_list_alerts()` checks the alert
>   inbox; `fcop_create_alert()` archives a gap manually.
>   Alerts notify, they do not block.
> - **Risk management** (since v1.1): `write_task(..., risk_level="high")`
>   auto-creates a `needs_human` REVIEW; you approve with
>   `mark_human_approved(review_id=...)`.
> - **Write-side tools require explicit binding** (since v1.4): set
>   `FCOP_PROJECT_DIR` in your MCP config, or call `set_project_dir()`
>   at session start. Unbound write calls raise `WriteRefused` to prevent
>   accidental writes to your HOME directory.
> - **File-level correction** (since v1.4): TASK/REPORT files support an
>   optional `supersedes: TASK-XXXXXXXX-NNN` field marking which historical
>   file this one replaces. `list_tasks` / `list_reports` annotate both
>   directions automatically.
> - **Trailing-slug filenames** (since v1.6, ADR-0033): `TASK` / `REPORT`
>   / `ISSUE` envelopes accept an **optional** `-{slug}` segment after
>   the routing fields (e.g.
>   `TASK-20260512-025-PM-to-OPS-phase-a-fix.md`). The slug is not part
>   of routing — it's a human-readable label. Pre-1.6 filenames remain
>   valid.
> - **MCP tool count**: 45 (v3.2.4 package / v3.2.3 protocol). Full list: `docs/mcp-tools.md`.
> - **Deep archiving (3.2.x new)**: `archive_to_history(task_id)` /
>   `bulk_archive_to_history()` move completed task-report pairs into
>   `history/YYYY-MM-DD/TASK-XXX/` (date-sharded).
>   `list_history` / `read_history_task` provide index and retrieval.
> - **v3 lifecycle tools (3.2.x new)**: `create_task` → `claim_task` →
>   `submit_task` → `approve_task` / `reject_task` → `finish_task`;
>   files flow through `_lifecycle/inbox/` → `active/` → `review/` →
>   `done/`.
> - **Rule versions**: `fcop-rules.mdc 3.2.3` / `fcop-protocol.mdc 3.2.3`.
>   Run `redeploy_rules()` after upgrading to refresh the four local rule
>   files.
> - **v3 topology (3.0.2 fix)**: fresh init now creates
>   `_lifecycle/{inbox,active,review,done,archive}/` and `history/`
>   immediately (per spec §1.1). Run `python -m fcop migrate --to-v3`
>   on older projects to upgrade.
>
> _(Earlier summaries: v1.3 / v1.4 / v1.5 / v3.0.x / v3.1.x and older — see `CHANGELOG.md`)_

---

## Identities up front

```
   Human                          AI team
┌─────────┐                   ┌──────────────────────┐
│  ADMIN  │◄──── TASK-*.md ──►│  leader              │
│  (you)  │                   │    │                 │
└─────────┘                   │    ├──► AI role 2    │
                              │    ├──► AI role 3    │
                              │    └──► AI role 4    │
                              └──────────────────────┘
```

| Who | What | Note |
|---|---|---|
| **Human** | You | Role code is always `ADMIN`, exactly one instance |
| **AI team** | N agents | N "job positions" named by you (`PM` / `MANAGER` / `ME` …) |

- `ADMIN` **is NOT written into `fcop.json.roles`** — it's FCoP's
  reserved role.
- Your instructions go to the **leader** only; the leader decides what
  to dispatch to other AI roles (Rule 4).
- Even in Solo mode, the single AI role is not you — it's your AI
  assistant.

---

## Three ways to start — ADMIN must pick one explicitly

> **Agents are not allowed to default**. After `fcop_report()`, the
> agent surfaces these three options verbatim and **waits for your
> word**. If an agent runs `init_project(team="dev-team")` before you
> say so, that's a 0.6.3 bug — 0.6.4 Phase-1 rules forbid it.
> Screenshot and file an issue.

### A. Just you (Solo, most common)

Say this to your Agent:

> **"Initialize the project in Solo mode, role code `ME`."**

Tool call:

```
init_solo(role_code="ME", role_label="Me", lang="en")
```

Solo = one agent wearing many hats. You (`ADMIN`) talk to the AI (`ME`)
directly — no multi-level dispatch. But **Rule 0.b still applies**: the
agent first writes a proposal file → does the work → re-reads its own
proposal as a reviewer, using files to split "proposer" from "reviewer".

### B. Use a preset 4-role team

> **"Initialize the project with the `dev-team` preset."**

| Template | For | AI roles | leader |
|---|---|---|---|
| `dev-team` | Software dev | `PM` · `DEV` · `QA` · `OPS` | `PM` |
| `media-team` | Content | `PUBLISHER` · `COLLECTOR` · `WRITER` · `EDITOR` | `PUBLISHER` |
| `mvp-team` | Startup MVP | `MARKETER` · `RESEARCHER` · `DESIGNER` · `BUILDER` | `MARKETER` |
| `qa-team` | QA testing | `LEAD-QA` · `TESTER` · `AUTO-TESTER` · `PERF-TESTER` | `LEAD-QA` |

Tool call: `init_project(team="dev-team", lang="en")`

**Presets come with a three-layer doc set** (new in 0.5.4): every
preset ships a full template — `TEAM-README.md` (team positioning) +
`TEAM-ROLES.md` (role boundaries) + `TEAM-OPERATING-RULES.md`
(operating rules) + `roles/{ROLE}.md` (single-role depth), bilingual.
`init_project` drops everything under `fcop/shared/` so an
agent just assigned a role reads its own `roles/{ROLE}.md` for
responsibilities and the two top-level files for shared rules — no
need for you to spell anything out. The three-layer structure is a
protocol rule (`fcop-rules.mdc` Rule 4.5), not a soft recommendation.

### C. Build your own team

**Canonical phrasing:**

> **"Build an AI team with 4 roles: `MANAGER` as leader, plus `CODER`,
> `TESTER`, `ARTIST`. Team name 'My Design Studio', English UI."**

Tool call:

```
create_custom_team(
  team_name="My Design Studio",
  roles="MANAGER,CODER,TESTER,ARTIST",
  leader="MANAGER",
  lang="en"
)
```

**Custom teams don't ship role docs — but samples are one click away**:
after creating a custom team, FCoP tells your agent
*"See `fcop://teams/<team>` for reference samples"* (dev-team /
media-team / mvp-team / qa-team each bundles the full **three-layer
template**: `TEAM-README` / `TEAM-ROLES` / `TEAM-OPERATING-RULES` /
`roles/{ROLE}`, bilingual). The agent naturally studies those before
drafting your own team's three-layer set. You can seed it with one
sentence: **"Mirror media-team's chain of command."**

---

## Roles ≠ Agent windows: how many Cursor tabs do you actually open?

**This is the #1 ADMIN pitfall**: `dev-team` lists 4 roles
(`PM / DEV / QA / OPS`), so ADMIN opens 4 Cursor windows up-front.

You don't have to.

| Concept | Lives in | Meaning |
|---|---|---|
| **Role** | `fcop.json` / task filenames | The protocol-level identity — who dispatches to whom, who reports back |
| **Agent (window)** | Each Cursor chat session you open | One window = one role, assigned the moment you type `You are {ROLE} on {team}` |

**FCoP does not require #roles = #windows**. It is a *file* protocol —
if you only open a `PM` window, the `TASK-*-to-DEV.md` files PM writes
will **sit silently in `tasks/`** until you open another window and
assign it `DEV`. That's not a bug; that's the design.

### The easiest way to start

| Open | Assignment | Good for |
|---|---|---|
| **1** | Current session = PM | Default starter. PM accepts your orders, writes dispatch files, and the queue waits. Open the 2nd window only when PM actually dispatches to DEV |
| **2** | PM + DEV | Pure coding, no test/deploy yet |
| **3** | PM + DEV + QA | When you want self-testing before ship |
| **4** | PM + DEV + QA + OPS | Only when you actually plan to deploy |

**Most people are fine with just one PM window**. Don't pre-open 4 —
idle windows just burn tokens.

### ⚠️ "1 PM window" ≠ Solo mode

Two different things — do not mix them up:

| | `mode: "solo"` | `mode: "team"` + 1 PM window |
|---|---|---|
| Role count | 1 (`ME`) | 4 (`PM/DEV/QA/OPS`) |
| Can dispatch? | No — no subordinate exists | Yes — PM writes `TASK-...-to-DEV.md`, queue waits |
| Switching to team later | Re-run `init_project()` | Just open a new window and type the assignment line |

In plain English: **Solo = "I'll do it all myself"; team-mode with 1 PM
window = "I've hired the crew; I'll call them in as needed"**.

### Standard opening lines

Current window:

> **"You are PM on dev-team"**

Tomorrow you need DEV. Open a new Cursor window, say:

> **"You are DEV on dev-team"** (optionally with `, thread feature_login`)

The two windows **do not chat with each other** — they coordinate
through files under `_lifecycle/`.

### ⚠️ One role, one agent (FCoP enforces this automatically since 0.7.0)

`ADMIN` (you) is bound by two dual constraints in the FCoP protocol:

1. **`ADMIN` cannot be assigned to any agent** — you are the human;
   AIs do not wear that hat.
2. **The same role code cannot be assigned to multiple agents
   simultaneously** — don't tell two Cursor windows "you are ME", and
   don't tell two windows "you are PM". Those two agents will fight
   over the same filename space under `_lifecycle/`, `issues/`,
   breaking Rule 0.b's self-review mechanism and Rule 4's
   role routing.

Since `fcop_protocol_version: 1.5.0` (fcop-mcp 0.7.0), an agent will
**proactively** cross-check `fcop_report()`'s "Role occupancy" section
before transitioning to BOUND:

- You say "you are PM" but `_lifecycle/` already shows another session has
  written files as PM → the agent MUST refuse the binding under Rule 8,
  drop a conflict note at `.fcop/proposals/`, and hand you three
  options:
  - **Handoff**: let the previous session wrap up, then re-assign.
  - **Co-review**: literally say "you are PM's co-reviewer" — this is
    a distinct binding, read-only + second-pass write.
  - **Distinct role**: assign a role code never seen on disk (e.g.,
    `PM2`).
- "Let me temporarily fill in" is **not** a legal option — there is no
  temporary identity state in the FCoP protocol.

In practice: when you open a second Cursor window, **decide what that
agent is for first**, then issue the assignment line. If two windows
must run concurrently, use team mode with distinct roles (`PM` ↔ `DEV`),
not two `PM`s.

### ⚠️ A sub-agent is NOT an extra role (enforced since 0.7.1)

Modern agents now spawn **their own sub-processes / sub-agents /
parallel workers**. From FCoP's standpoint these still share the
**same seat** as the parent — files written by a sub-agent MUST carry
the role you assigned to the parent session, and **must not** self-claim
a different role code to write "on behalf of" someone else.

Real failure mode (observed 2026-04-27):

> You assign `PLANNER`. PLANNER spawns a sub-agent to run tests. The
> sub-agent then writes a report with `sender: CODE_EXPERT` — but you
> never assigned `CODE_EXPERT` to anyone.

This is a Rule 1 violation. One role = one duty = one ledger account.
The only legal path to make `CODE_EXPERT` produce a report is Rule 4:
dispatch a `TASK-*.md` to `CODE_EXPERT` and wait until you've
separately assigned a session to that role.

**0.7.1 ships a new `fcop_check()` tool** that runs a
`session_id ↔ role` consistency audit — the same `session_id` showing
up under two different role codes is direct evidence of impersonation
and gets surfaced to you. This is post-hoc audit, not prevention —
prevention still depends on the agent honouring the rule, but you
can run `fcop_check()` any time to verify.

---

## Hard rules for custom roles

Role codes go straight into filenames
(`TASK-20260417-001-MANAGER-to-CODER.md`), so the rules come from the
filename grammar:

| Item | Rule | OK ✅ | Not OK ❌ |
|---|---|---|---|
| Role code | Starts with uppercase letter; `A-Z` `0-9` `_` `-`; `-` not at start / end / consecutive | `MANAGER` `QA1` `CODER_A` `LEAD-QA` `AUTO-TESTER` | `程序员` `-QA` `PM--QA` `QA.1` `my boss` |
| Role count | ≥ 2 (single role ⇒ use Solo instead) | `MANAGER,CODER` | Only `MANAGER` |
| Leader | Must be in the role list | leader=`MANAGER` | leader=`CEO` (not in list) |
| Reserved | `ADMIN` and `SYSTEM` cannot be used as role codes | `MANAGER` | `ADMIN` `SYSTEM` |
| Team name | Anything; only used for display | "My Design Studio" | — |
| Language | `zh` or `en` | `en` | `English` |

**Naming hints** (to avoid semantic conflicts):

- ✅ Use **job-function words**: `MANAGER` / `CODER` / `WRITER` /
  `EDITOR` / `PM` / `DEV` / `QA`
- ✅ Use **uppercase Pinyin** if a Chinese word fits best:
  `JINGLI` / `CHENGXU` / `CESHI`
- ❌ Avoid **authority words**: `BOSS` / `CHIEF` / `MASTER` / `OWNER` /
  `CEO` / `KING` — the real "boss" is you (`ADMIN`); an AI role
  shouldn't wear that hat.
- ❌ **No non-ASCII**: the filename grammar is strictly ASCII.

## Proactive validation: you talk casually, FCoP stops the bad ones

**You don't need to memorize the rules above.** Every case below is
**stopped before anything hits disk**, with a bilingual concrete
explanation — not "success/failure", but **which field, which character,
and how to fix it**.

| You casually say | Agent tries | FCoP blocks, reason |
|---|---|---|
| "4-role team: `BOSS` `程序员` `测试` `设计师`" | `create_custom_team(roles="BOSS,程序员,...")` | ❌ Role code `'程序员'` illegal: non-ASCII not allowed |
| "Call them `DEV-TEAM` and `QA-1`" | `create_custom_team(roles="DEV-TEAM,QA-1,...")` | ❌ Role code `'DEV-TEAM'` illegal: `-` not allowed (collides with filename separators) |
| "Call it `my boss`" | `create_custom_team(roles="my boss,...")` | ❌ Role code `'my boss'` illegal: no spaces, must start uppercase |
| "Call it `QA.1`" | `create_custom_team(roles="QA.1,...")` | ❌ Role code `'QA.1'` illegal: `.` not allowed |
| "Add `ADMIN` to the team" | `create_custom_team(roles="ADMIN,CODER,...")` | ❌ `'ADMIN'` is FCoP-reserved (the human's identity); cannot be given to an AI |
| "Single role: `MANAGER`" | `create_custom_team(roles="MANAGER", ...)` | ❌ At least 2 roles required; for a single-role setup use `init_solo(...)` |
| "Leader is `CEO`, roles are `MANAGER, CODER`" | `create_custom_team(roles="MANAGER,CODER", leader="CEO")` | ❌ `leader 'CEO'` must be one of the declared roles (current: `MANAGER, CODER`) |
| "`CODER`, `CODER`, `QA`" | `create_custom_team(roles="CODER,CODER,QA", ...)` | ❌ Role code `'CODER'` duplicated |

> **Since 0.4.6, errors walk you through the fix**: say `DEV-TEAM` and
> FCoP replies `Suggested fix: DEV_TEAM (casing / separators
> auto-repaired)`. Say `my boss` → `Suggested fix: MY_BOSS`. Typo the
> leader's casing → `Did you mean 'MANAGER'?` (did-you-mean).
> Suggestions are **hints only** — you always pick the final name.

**9 validation checks total**, all baked into `create_custom_team` /
`init_solo` — you don't call them, they just run:

1. Role code non-empty
2. Must match `^[A-Z][A-Z0-9_]*$` (uppercase start, only `A-Z` / `0-9` / `_`)
3. No non-ASCII, `-`, `.`, or spaces
4. Cannot be `ADMIN` (reserved for the human)
5. Cannot be `SYSTEM` (reserved for FCoP internals)
6. Non-solo teams: at least 2 roles (single-role → use `init_solo`)
7. No duplicates in the roles list
8. `leader` must be in the roles list
9. Every failure returns a **human-readable bilingual error**, not a boolean

**Want a dry-run before committing?** Have the agent call:

```
validate_team_config(roles="MANAGER,CODER,TESTER,ARTIST", leader="MANAGER")
```

Writes nothing; returns `OK` if valid, otherwise tells you exactly
what's wrong. Useful when you dictate a pile of role names and aren't
sure whether any of them contain illegal characters.

**Bottom line: you don't memorize rules.** Just tell the agent in plain
language what team you want. `create_custom_team` runs these 9 checks
automatically; if it fails, the agent will come back to you with the
concrete reason.

---

## What lands on disk after init

```
project root/
├── fcop/                      ← Coordination metadata (who does what)
│   ├── fcop.json                     ← Project identity (mode / roles / leader)
│   ├── _lifecycle/                   ← v3 five-bucket: location-is-state (delivered on fresh init since 3.0.2)
│   │   ├── inbox/                    ← Entry point for new TASKs
│   │   ├── active/                   ← In progress
│   │   ├── review/                   ← Awaiting review / REVIEW-*
│   │   ├── done/                     ← Completed
│   │   └── archive/                  ← Long-term archive
│   ├── reports/                      ← Completion reports (retained)
│   ├── issues/                       ← Issue records (retained)
│   ├── shared/                       ← Standing docs (retained)
│   │   ├── README.md                 ← Shared-directory conventions
│   │   ├── TEAM-README.md            ← Team positioning + ADMIN duties
│   │   ├── TEAM-ROLES.md             ← Layer 1 · role boundaries
│   │   ├── TEAM-OPERATING-RULES.md   ← Layer 2 · operating rules
│   │   └── roles/                    ← Layer 3 · single-role depth
│   │       ├── PM.md
│   │       ├── DEV.md
│   │       └── ...                   ← one per role (bilingual)
│   └── LETTER-TO-ADMIN.md            ← This letter, kept for reference
├── workspace/                        ← ★ Artifact home (code, scripts, data) ★
│   └── README.md                     ← Convention reference
└── .cursor/rules/
    ├── fcop-rules.mdc                ← Protocol rules (auto-injected per agent)
    └── fcop-protocol.mdc             ← Protocol commentary
```

### Three-layer team docs (since 0.5.4)

Team docs under `shared/` **must** split into three layers — this is
a protocol rule (`fcop-rules.mdc` Rule 4.5):

| Layer | File | Answers |
|---|---|---|
| Layer 0 · entry | `TEAM-README.md` | What is this team? How does ADMIN engage? What's the typical flow? |
| Layer 1 · role boundaries | `TEAM-ROLES.md` | Who owns what? Who reports to whom? Which lines are off-limits? |
| Layer 2 · operating rules | `TEAM-OPERATING-RULES.md` | How are tasks dispatched, replied to, escalated, retrospected? |
| Layer 3 · single-role depth | `roles/{ROLE}.md` | One role's responsibilities, deliverables, acceptance criteria, interfaces |

`ADMIN` (you) is human — does **not** go under `roles/`, and is **not**
written into `fcop.json.roles`. Your duties live in the "ADMIN
Responsibilities" section of `TEAM-README.md`, not a separate file.

Want to upgrade an old project to the three-layer set, or switch team
templates? Have the agent call
`deploy_role_templates(team="dev-team")` — it auto-archives any
existing files to `.fcop/migrations/<timestamp>/` before dropping the
new templates. Diff-able and recoverable; hand-edits aren't silently
lost.

Every message you send from now on becomes a file:

```
TASK-20260417-001-ADMIN-to-MANAGER.md    ← your instruction
TASK-20260417-001-MANAGER-to-ADMIN.md    ← MANAGER's report
```

**That's the whole of FCoP.**

---

## Where artifacts go: the `workspace/<slug>/` convention

This is the question nobody sees coming on day one and everybody
regrets on day two:

**You ask the agent to build a CSDN search tool; it dumps `app.py`,
`pyproject.toml`, and `*.bat` straight into the project root. Day two
you ask for a small game, `pyproject.toml` collides, `app.py` gets
overwritten, and the `*.bat` files are mixed together with no way to
tell which is which.**

FCoP 0.4.7 bakes the answer into init: **the project root only holds
coordination metadata; actual work products go under
`workspace/<slug>/`. One slug per "thing you're doing", fully
isolated.**

```
acme-3/
├── .cursor/ docs/ fcop.json LETTER-TO-ADMIN.md   ← coordination skeleton, never mixed
└── workspace/
    ├── csdn-search/         ← today: CSDN article search
    │   ├── app.py
    │   ├── templates/
    │   ├── *.bat
    │   └── pyproject.toml
    └── mini-game/           ← tomorrow: small game (own cage, fully isolated)
        ├── game.py
        └── assets/
```

### How to open a new cage

Both are fine:

1. **Ask the agent to call** (recommended):

    ```
    new_workspace(slug="csdn-search", title="CSDN Article Search Tool")
    ```

    FCoP creates the directory, writes a minimal README, and drops a
    `.workspace.json` metadata file.

2. **Just `mkdir` it yourself**: make a folder under `workspace/`
    by hand. The agent still recognizes it, and `list_workspaces()`
    still lists it.

### Slug naming rules (FCoP validates automatically)

| ✅ Legal | ❌ Illegal | Why |
|---|---|---|
| `csdn-search` | `CSDN-Search` | lowercase required |
| `mini-game` | `mini_game` | only `-` as separator (inverse of role codes) |
| `weekly-report-2026w17` | `周报` | no non-ASCII |
| `api-v2` | `my game` | no spaces |
| `search` | `tmp` / `shared` / `archive` | reserved |

Same as role codes: mistypes get a friendly "Suggested fix: `xxx`"
reply. Max 40 characters.

### One-shot overview

To see how many cages the project has and what they're for, have the
agent call:

```
list_workspaces()
```

Output shows each slug's title and creation time.
`get_team_status()` also includes the workspace count.

### Hard rules

- ❌ The agent **must not write business code into the project root**
  (`app.py` / `pyproject.toml` etc.)
- ❌ Files are not shared across slugs
- ✅ If you need something shared across cages, open
  `workspace/shared/` — FCoP reserves that slug for exactly this

---

## How you actually use FCoP: just talk

**First, the important part**: FCoP ships 45 tools — **all of them are
for the agent, not for you**. You talk in plain language from start to
finish; the agent translates your intent into the right tool call.

```
You (ADMIN)         Agent (AI)            FCoP toolbox
  speak     ────→   understand   ────→    call the tool
                                              ↓
                                       write files / make dirs / check state
```

You do not have to memorize any tool names. The table below is a
"**when you say X, the agent does Y**" reference — so that *if* the
agent forgets what to do, you can spot it and nudge it back.

### Project kickoff

| You say | Agent calls | Outcome |
|---|---|---|
| (first sentence of a new session) | `fcop_report()` | Agent reports project state; tells you if it's uninitialized or unassigned |
| "initialize a Solo project" / "I'll do it myself" | `init_solo(role_code="ME")` | Writes `fcop.json`, creates directories, deploys rules + letter, creates `workspace/` |
| "initialize a dev team" / "I want a 4-role team" | `init_project("dev-team")` or `create_custom_team(...)` | Same as above, multi-role |
| "MCP is bound to the wrong dir" / `fcop_report` shows `C:\Users\xxx` | `set_project_dir("E:\\your-project")` | Rebinds at runtime; no config edits, no restart |
| "you are PM" / "you are ME" | (no tool call; the agent just remembers its role) | Enters Phase 3 and starts working |

### Day-to-day work

| You say | Agent calls | Outcome |
|---|---|---|
| "build a CSDN search tool" / "start a new thing for X" | `new_workspace(slug="csdn-search", title="...")` | Creates `workspace/csdn-search/` cage; all artifacts land inside |
| "assign a task to CODER" / "ask X to do Y" | `write_task(recipient="CODER", body="...")` | Drops a `TASK-*-to-CODER.md` |
| "what's the state of the project" | `get_team_status()` | Task / report / issue / workspace counts + recent activity |
| "how many workspaces do we have?" | `list_workspaces()` | Lists every `workspace/<slug>/` with create time |
| "what tasks are still pending?" | `list_tasks()` | Lists pending tasks (v3: `_lifecycle/inbox/active/review/`) |
| "what does task X say?" | `read_task("TASK-...")` | Reads body |
| "any open issues?" | `list_issues()` | Lists `issues/` |
| "archive X, it's done" | `archive_task("TASK-...")` | Moves to `_lifecycle/archive/` (v3) |
| "push this archive file to history" | `archive_to_history("TASK-...")` | Single: `_lifecycle/archive/` → `history/YYYY-MM-DD/TASK-XXX/` |
| "bulk-push all archives to history" | `bulk_archive_to_history()` | Bulk: drains `_lifecycle/archive/`, moves all into date-sharded `history/` |
| "show me the completion reports" | `list_reports()` / `read_report(...)` | Reads `reports/` |

### Rescue / edge cases

| You say | Agent calls | Outcome |
|---|---|---|
| "I don't like this FCoP rule" | `drop_suggestion("...", "...")` | Feedback lands under `.fcop/proposals/` (you can't edit the rules files yourself) |
| "validate this team config before creating it" | `validate_team_config("MANAGER,CODER", "MANAGER")` | Dry-run check, returns suggestions on error |
| "what team presets exist?" | `get_available_teams()` | Lists Solo / dev-team / media-team / mvp-team / qa-team |
| "upgrade the team docs to the three-layer set" / "switch to qa-team templates" | `deploy_role_templates(team="qa-team")` | Legacy files archived to `.fcop/migrations/<timestamp>/`; fresh three-layer set lands under `shared/` |
| "let me re-read the manual" | Reads `fcop://letter/en` or opens `fcop/LETTER-TO-ADMIN.md` | Re-renders this letter |

### The only 2 tool names you might actually type

- **`fcop_report`** — if a new session's agent doesn't auto-report,
  just say "report first" or literally "call `fcop_report`".
- **`set_project_dir`** — when you see the MCP bound to the wrong
  directory (e.g. `fcop_report` shows a `C:\Users\xxx` path), say
  "bind to `E:\your-project`" or literally "call `set_project_dir("...")`".

**The other 24 are never yours to memorize**. The agent picks.

### Why the agent knows what to call

Because FCoP tells it in three places **at once**:

1. **MCP instructions** (always read on agent startup) — includes the
   "when ADMIN says X, call Y" map baked in.
2. **Each tool's docstring** (visible to the agent) — describes exactly
   when to invoke it.
3. **`fcop-rules.mdc`** (`alwaysApply: true`) — enforces hard rules
   like Rule 0.

So your job is just plain language. If the agent misses something
obvious (e.g. doesn't open a workspace when it should, or skips
`fcop_report`), point it at the relevant row of this letter — the
correction takes one line.

### 12 resources (agent-only; you never touch these)

**Core resources** (readable any time):

| URI | Who reads it | What it is |
|---|---|---|
| `fcop://rules` | Agent | `fcop-rules.mdc` raw |
| `fcop://protocol` | Agent | `fcop-protocol.mdc` raw |
| `fcop://letter/zh` or `/en` | Agent when it wants to re-read | This letter |
| `fcop://prompt/install` or `/install/en` *(0.6.4)* | ADMIN copies it to a fresh agent | Canonical "have an agent install fcop-mcp for you" prompt |
| `fcop://status` | Agent | Same as `get_team_status` |
| `fcop://config` | Agent | `fcop.json` raw |

**Sample library** (0.5.4+, three-layer team templates — browse without initializing):

| URI | What it is |
|---|---|
| `fcop://teams` | Index of all 4 preset teams (dev / media / mvp / qa) |
| `fcop://teams/{team}` | Team's `TEAM-README.md` (positioning + ADMIN duties + flow) |
| `fcop://teams/{team}/TEAM-ROLES` | Layer 1 · role boundaries (Chinese) |
| `fcop://teams/{team}/TEAM-OPERATING-RULES` | Layer 2 · operating rules (Chinese) |
| `fcop://teams/{team}/{role}` | Layer 3 · single-role depth (Chinese; e.g. `.../dev-team/PM`) |
| `fcop://teams/{team}/{role}/en` | Layer 3 · single-role depth (English) |

> Append `/en` to any `.../{role}` or `.../TEAM-*` URI for the English
> version. The pre-0.5.4 `fcop://teams/{team}/PM-01` style still
> resolves (fallback to `roles/PM.md`), but new projects should use
> the clean form without the `-01` suffix.

**You use these samples by just asking — no need to memorize URIs**:

- "Show me dev-team's PM role template" → Agent reads `fcop://teams/dev-team/PM`
- "What are dev-team's role boundaries?" → Agent reads `fcop://teams/dev-team/TEAM-ROLES`
- "How does media-team dispatch tasks?" → Agent reads `fcop://teams/media-team/TEAM-OPERATING-RULES`
- "I want to create LEAD-DEV — which sample is closest?" → Agent picks one for you
- "What presets are available?" → Agent reads `fcop://teams` or calls `get_available_teams()`

### ⚠️ Cursor's "click-to-grey-out" switches: 2 you must never grey

Cursor's MCP panel shows these 45 tools as buttons. Click → greyed =
disabled. **Greying these two will hurt you**:

- `fcop_report` — greyed out, Rule 0 breaks; agents can't take
  their mandatory first step
- `set_project_dir` — greyed out, your only rescue for a
  wrong-directory binding is editing `mcp.json` + restarting Cursor

The other 24 can technically be greyed out, but the agent just gets
confused when a tool suddenly disappears — **keep them all enabled**.

---

## Four must-read rules (cheat sheet)

| # | Rule | One line |
|---|---|---|
| 0.a | Land it as a file | Unfiled chat = never happened |
| 0.b | Multi-role checks | No single AI does decision-to-execution alone |
| **0.c** | **Only land true things** | **No fabrication; every reference cited** |
| 1 | UNBOUND | New sessions call `fcop_report()` first and wait for you |

Full 9-rule set: `.cursor/rules/fcop-rules.mdc` (agents read it
automatically). Commentary (naming, YAML, layout, patrol, citation
formats for 0.c, …): `.cursor/rules/fcop-protocol.mdc`.

---

## Upgrading fcop (automated from 0.5.3 onward)

The FCoP toolbox (the `fcop` Python package) gets updates. From 0.5.3 on,
you don't have to remember anything:

**Every new session's `fcop_report()` automatically tells you at the
tail whether a new version is available.**

It looks like this:

```
📦 fcop update available: 0.5.4 → 0.5.5

- Agent: call upgrade_fcop() — one-line upgrade + restart reminder
- Shell: pip install --upgrade fcop (then fully close & reopen Cursor)
```

When you see the banner, two upgrade paths:

### Path 1: let the agent upgrade (easiest)

One line:

> upgrade fcop

The agent calls `upgrade_fcop()`, uses its own Python to run
`pip install --upgrade fcop`, reports the version delta, and reminds
you to restart Cursor.

### Path 2: run it yourself (also fine)

```powershell
pip install --upgrade fcop
```

Then fully close Cursor and reopen it. On Windows: **use Task Manager
to kill every `Cursor.exe` process** — closing windows alone leaves
background processes that keep the old MCP alive.

### To check "is there a new version right now"

One line:

> is there a new fcop version?

The agent calls `check_update()` — skips the 24h cache, asks PyPI
directly.

### ⚠️ Important reminders

- After upgrade you **must restart Cursor** — without restart, the
  running MCP is still on the old version
- Do NOT let the agent hand-edit `.cursor/rules/*.mdc` or the version
  fields in `fcop.json` — that's not upgrading, it's corrupting the
  protocol
- The banner refreshes every 24h (so PyPI isn't queried on every
  session); silently skipped when offline

---

## When you disagree

- Want the full rules → have the agent read `fcop://rules` or
  `fcop://protocol`
- Disagree with the protocol itself → have the agent call
  `drop_suggestion("...", "...")`; feedback lands under
  `.fcop/proposals/` without polluting the collaboration directory
- Want to switch templates → one line: "re-initialize with `{team}`"
- Want to re-read this letter → `fcop://letter/en` or
  `fcop/LETTER-TO-ADMIN.md`

Welcome aboard.

— **FCoP**
