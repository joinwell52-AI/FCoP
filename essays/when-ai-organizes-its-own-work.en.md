# When AI Organizes Its Own Work

### A field study of multi-agent coordination built on nothing but a filesystem · A report on **FCoP**

> When AI Organizes Its Own Work: what happened after we replaced our multi-agent middleware with a folder.
> A report on **FCoP — File-based Coordination Protocol**.

**Core innovation**: **Filename as Protocol**

**Authors**: The CodeFlow Team · 2026-04-19
**Keywords**: Multi-agent, File-based protocol, Emergent coordination, FCoP, Human-Machine Isomorphism, Unix philosophy

---

## Abstract

We gave a small team of AI agents (four roles, one human admin) a 76-line Markdown rulebook, a shared folder, and almost nothing else. No message queue. No database. No WebSocket between agents. The "coordination runtime" is a Python loop that clicks Cursor's tabs every few seconds just to wake each agent up — it does not route, schedule, or arbitrate anything.

Within **48 hours of first boot** on a freshly-installed PC, the agents produced 42 tasks, 22 reports, and 10 spontaneous "shared" documents (≈ 74 files total). More interestingly, they **invented six coordination patterns we had not specified**: broadcast addressing, anonymous role slots, subtask sub-folders, self-explaining READMEs, traceability fields, and a whole class of standing "dashboard / sprint / glossary" documents. None of these caused collisions. All of them were discoverable by simply listing a directory.

We call this protocol **FCoP — File-based Coordination Protocol**. Its single core innovation is a slogan: **"Filename as Protocol."** Directory name is *status*, filename is *routing*, file content is *payload*. Nothing else. The same physical folder is simultaneously a rigorous state machine for agents and a browsable directory tree for humans — a property we call **Human-Machine Isomorphism**. This asymmetric-yet-symmetric design is what kills the "black box anxiety" that plagues every other multi-agent stack.

This essay documents what those agents did, why a filesystem-only protocol survives it gracefully, and what that implies for anyone building multi-agent systems today. It is not a product announcement — it is a field report, and an invitation to steal the idea.

---

## TL;DR · What FCoP Is in 60 Seconds

**FCoP = File-based Coordination Protocol** — a minimalist protocol that lets multiple AI agents collaborate through a **shared filesystem**.

**One sentence**: *Filename as Protocol.*

**What it looks like**:

```
docs/agents/
├── tasks/     ← pending tasks
├── reports/   ← completion reports
├── issues/    ← issues
├── shared/    ← standing docs (dashboards, glossary, …)
└── log/       ← archives
```

**Routing lives in the filename**:

```
TASK-{date}-{seq}-{sender}-to-{recipient}.md
    e.g. TASK-20260418-201-MARKETER-to-DEV.md
         ↑ kind  ↑ date     ↑ seq ↑ sender  ↑ recipient
```

Every agent just runs `glob "*-to-{my-role}*.md"` to fetch its inbox. The recipient slot supports four forms:
`to-DEV` (direct), `to-TEAM` (broadcast), `to-DEV.D1` (named slot), `to-assignee.D1` (anonymous slot).

**What FCoP does NOT need**:
Database, message queue, orchestration engine, custom client, SDK, persistent connections — **none of them**.

**What it DOES need**:
One shared directory, one naming convention, and every agent taking ownership of its role. **That's all.**

**Why it matters**:

- **Human-Machine Isomorphism**: humans and agents read **the same files**. A bare `ls` tells you what the system is doing — no debugger required.
- **Identity determines path**: roles are written into filenames. An agent physically cannot read or write outside its own mailbox. Structure gives order; content is wide open.
- **Protocol can evolve**: we observed 6 new coordination patterns self-invented by AI within 48 hours — all compatible with the existing protocol.
- **Zero infrastructure**: git is the audit log, rsync is cross-machine sync, Finder / File Explorer is the debug panel — everything is off-the-shelf.

**Want more?**

- 60-second companion: [`fcop-primer.en.md`](../primer/fcop-primer.en.md)
- The spec itself (~160 lines): [`spec/codeflow-core.mdc`](../spec/codeflow-core.mdc)
- This essay: keep scrolling ↓

> **A note on samples**: Every agent-generated snippet quoted in this essay is **verbatim** — the filenames, directory layout, frontmatter, tables, and acceptance language are all exactly what the agents wrote at the time. The data domains shown (Chinese automotive OEMs, public NetEase Cloud Music songs) are already public information; nothing has been abstracted. **What we did NOT do** is publish the whole `codeflow-1` sample directory — that project is ongoing, and its internal tooling code, room keys, and device IDs are not suitable for a full public drop. What readers actually want — "what did AI invent?" — is covered in full through representative snippets in §5.

---

## 1. An Almost Absurd Hypothesis

In 2026, the mainstream multi-agent stack looks like this: Agents × N → Message Bus × 1 → State Store × 1 → Orchestrator × 1 → Observability × 1. At minimum, five SaaS products, two SDKs, and a pager rotation.

We wanted to ask a simpler question:

> **What happens if we collapse the agent-to-agent protocol down to just the filesystem?**

No queues, no databases, no webhooks. **Agents can only talk to each other by writing and reading files in a directory.** As dumb, as crude, as un-modern as 1970s Unix pipes.

The hypothesis wasn't about nostalgia. It was about answering:

- Can a team of agents with no central dispatcher evolve a coordination structure on its own?
- Can that structure be understood by a human at a glance?
- When an agent invents a pattern the protocol designer never wrote down — **is that a bug or a feature?**

We built a minimal-viable implementation called **CodeFlow**, wrote a 76-line Markdown spec called **FCoP** (**F**ile-based **Co**ordination **P**rotocol), and ran it on a **freshly-installed, still-warm** PC. **Within 48 hours**, it surprised us.

---

## 2. The Starting Point: A 76-Line Spec

The initial spec was almost too simple to bother writing down. Three things at the core:

**① Shared directory layout**

```
docs/agents/
├── tasks/     ← task files
├── reports/   ← completion reports
├── issues/    ← issue logs
└── log/       ← archives
```

**② Filename as Protocol**

```
TASK-{date}-{seq}-{sender}-to-{recipient}.md
```

This is the **single core innovation** of FCoP — every other rule is a derivative:

- **Directory name = Status**: is the file in `tasks/` or `reports/`? Its state is self-evident.
- **Filename = Routing**: sender, recipient, kind, and sequence are all written into the name.
- **File content = Payload**: Markdown body plus YAML frontmatter.

How does a recipient find its inbox? A single `glob "*-to-{my-role}*.md"`. No header parsing, no database query — **the filename itself is a complete addressable surface**.

**③ YAML frontmatter**

```yaml
---
protocol: agent_bridge
version: 1
kind: task
sender: PM
recipient: DEV
task_id: TASK-20260418-001
priority: P1
---
```

Plus five collaboration manners: only handle tasks addressed to you, always write a report on completion, log issues as issue files, don't touch other people's files, leave archiving to the coordinator.

**That's the whole protocol.** No state machine, no schema, no transactions. The core condenses down to one line: **Filename as Protocol**. Everything you're about to read — the "inventions" AI made — all grew out of this one rule.

---

## 3. The Patrol Engine's Secret: It Does Almost Nothing

The most common misconception about CodeFlow is that its **Patrol Engine** is a central dispatcher. The truth is:

> **The patrol engine just clicks a Cursor tab every few seconds via Chrome DevTools Protocol — so the agent inside wakes up and checks its own inbox.**

That's it.

It does not route messages, judge priorities, validate schemas, manage transactions, or enforce order.

Why so minimal? Because **Cursor has no native agent-to-agent channel**. Each agent lives inside one chat session, deaf to the others. What the patrol engine does is closer to "knock on each door in turn":

- "DEV, wake up — check if any new tasks landed in the `tasks/` folder for you."
- "QA, wake up — anything in `reports/` you need to regress?"
- "MARKETER, your turn — read what's new in `docs/agents/`."

The real coordination logic lives **entirely** in the moment each agent reads, writes, and names files. The patrol engine is just the mechanism that ensures each agent "wakes up periodically."

In other words: **the platform does the least possible, and hands the protocol layer over to the agents themselves.**

---

## 4. The Field: `codeflow-1`, 48 Hours

On 2026-04-16 we finished installing the OS and syncing the toolchain. On 2026-04-17 we started giving the agents real work. Two days later — as I'm writing this — the team has already produced everything listed above.

The experimental project is called `codeflow-1`. Its team configuration is a "small content studio":

| Role | Responsibility |
|---|---|
| **MARKETER** | Coordinator / PM / dispatcher |
| **RESEARCHER** | Research and assets |
| **DESIGNER** | Visual design and storyboards |
| **BUILDER** | Engineering and scripts |
| **ADMIN** (human) | Specifies requirements, makes calls, signs off |

No DEV, no QA, no OPS — even the role names are project-specific. The spec never says a word about what MARKETER should *do*; it just knows its name is MARKETER, and its inbox is `*-to-MARKETER*.md`.

Two days in, `docs/agents/` really looks like this (excerpt; headline numbers: 42 tasks + 22 reports + 10 standing documents):

```
docs/agents/
├── BUILDER.md  DESIGNER.md  MARKETER.md  RESEARCHER.md    ← role manuals
├── codeflow.json                                           ← team config
├── CURRENT-SPRINT-STATUS.md                                ← AI-invented
├── DASHBOARD-20260418.md                                   ← AI-invented
├── tasks/
│   ├── RULES-task-file-format.md                           ← AI-invented
│   ├── SPRINT-20260418-delivery-push.md                    ← AI-invented
│   ├── TERM-20260418-assignment-matrix.md                  ← AI-invented
│   ├── TASK-20260418-001-ADMIN-to-MARKETER.md
│   ├── TASK-20260418-007-MARKETER-team-bulk-data.md        ← AI-invented "team" broadcast
│   ├── TASK-20260418-022-MARKETER-self-ADMIN018.md         ← AI-invented "self" note
│   ├── …26 top-level tasks total…
│   └── individual/                                         ← AI-opened subdirectory
│       ├── README.md
│       ├── INDIVIDUAL-TASK-INDEX.md
│       ├── TASK-20260418-201-MARKETER-to-assignee-D1.md    ← AI-invented "assignee slot"
│       ├── TASK-20260418-202-…-D2.md
│       ├── …11 individual tasks total…
│       └── TASK-20260418-211-MARKETER-to-assignee-P1.md
├── reports/   …matching reports…
├── issues/    log/
```

Everything marked `← AI-invented` was **nowhere in the original 76-line spec**.

Let's look at what it invented.

---

## 5. Six Coordination Patterns Invented by AI

### 5.1 Broadcast address: `to-TEAM`

The spec said `to-{recipient}`, where recipient defaulted to a single role. But one day MARKETER needed to get a shared background brief in front of the whole team. So it wrote this:

```
TASK-20260418-007-MARKETER-team-bulk-data.md
TASK-20260418-009-MARKETER-team-makabaka-video.md
TASK-20260418-012-MARKETER-team-two-mp4-deliverables.md
```

That `MARKETER-team-*` segment is neither `to-DEV` nor `to-QA`. It's a **pseudo-keyword the AI invented on the fly**: `team`. When other agents encountered this format for the first time, they did not throw errors. They inferred from context: "ah, this is a team-wide announcement," and went to read it.

Open `TASK-20260418-009-MARKETER-team-makabaka-video.md` and the body looks like this:

```yaml
---
kind: task
sender: MARKETER
recipient: TEAM                       # ← broadcast
priority: P1
parent: TASK-20260418-008
---

# "Makabaka Makabaka" music video · team task (ADMIN 008)

## Division of labor (one person may wear multiple hats)

| Role                  | Task                                              | Deliverable         |
|----------------------|---------------------------------------------------|---------------------|
| COLLECTOR / sourcing  | Prepare live-action / animation references        | Asset list          |
| WRITER / script       | Flesh out storyboard and subtitle cue points      | Storyboard v1       |
| EDITOR / editing      | Cut, color, subtitle, deliver final cut           | Final cut + project |
| PUBLISHER / release   | Cover art, title, tags, platform compliance check | Release pack + URLs |
```

Look carefully: inside this **broadcast task body**, MARKETER has spontaneously invented 4 **off-protocol** sub-roles — COLLECTOR / WRITER / EDITOR / PUBLISHER. They are **not** in the 4 formal roles registered in `codeflow.json` (MARKETER / RESEARCHER / DESIGNER / BUILDER).

MARKETER did not request a role-table change, and no error was thrown. It simply said, "I've sliced this work along functional lines into four chunks — **whoever on the team can take a chunk, take it**." The protocol layer handles "which filename went from whom to whom." The functional layer is handed to the agent's content layer. **Role identity and functional role got naturally decoupled.**

Later the same shape evolved to explicitly declare `recipient: TEAM` in the frontmatter:

```yaml
---
kind: task
sender: MARKETER
recipient: TEAM        # ← not DEV, not QA — TEAM
parent: TASK-20260418-006
---
```

**This is a silent RFC.** No vote, no review, no version bump — the protocol just gained a new "broadcast addressing" form.

### 5.2 Anonymous slot: `to-assignee-D1`

When MARKETER split a large "one-thousand-row data cleanup" task into 11 parallel smaller pieces, it ran into a problem: **those 11 pieces had not been assigned to specific agents or humans yet**. Per the spec, `recipient` has to be a concrete role.

Its solution was to invent a pseudo-role called `assignee`, plus numeric suffixes as slots:

```
TASK-20260418-201-MARKETER-to-assignee-D1.md   ← data pack 1
TASK-20260418-202-MARKETER-to-assignee-D2.md   ← data pack 2
…
TASK-20260418-207-MARKETER-to-assignee-V1.md   ← video 1
TASK-20260418-209-MARKETER-to-assignee-M1.md   ← footage 1
```

Frontmatter would say:

```yaml
recipient: assignee_D1
assignee_name: (required: real name or employee ID)
```

This solved a problem the protocol designer had never anticipated: **"task exists, assignee TBD."**

At dispatch time, only the "seat number" is filled in (D1, D2, V1, M1, S1, P1 — data / video / footage / storyboard / publishing), and **whoever sits down later fills in the name**. This is eerily similar to the "topic + consumer group" dispatch pattern in traditional message queues — except there is no broker, only filenames.

### 5.3 Subdirectory `tasks/individual/`

When individual tasks piled up, flat-listing them in `tasks/` drowned out everything else. The AI's choice was to **open a subdirectory**:

```
tasks/individual/
├── README.md                         ← written to itself / future readers
├── INDIVIDUAL-TASK-INDEX.md          ← self-built index
└── TASK-20260418-201-…-P1.md         ← 11 tasks
```

More interesting is the opening of the `README.md`:

```markdown
# Individual task cards (per-person · in response to ADMIN 015)

This directory is for **MARKETER → assignee** individual task files, one per person;
**the name must be filled into each task's frontmatter or body**.
```

This is the AI explaining **to its future self** and **to future teammates**: "This directory is for X; who may write, who should read." It spontaneously filled a gap the protocol never specified — **hierarchical workspace self-description**.

Even more interesting: it also proactively **built an index** for these 11 tasks, in `INDIVIDUAL-TASK-INDEX.md`:

```markdown
# Individual task index (TASK-201 to 211)

| ID  | File                                              | Main content                    |
|-----|---------------------------------------------------|---------------------------------|
| 201 | TASK-20260418-201-MARKETER-to-assignee-D1.md      | 1000-row data · pack 1          |
| 202 | TASK-20260418-202-MARKETER-to-assignee-D2.md      | 1000-row data · pack 2          |
| …   | …                                                 | …                               |
| 207 | TASK-20260418-207-MARKETER-to-assignee-V1.md      | Final cut #1 "Makabaka"         |
| 208 | TASK-20260418-208-MARKETER-to-assignee-V2.md      | Final cut #2 "Xu Yi Shi Chang An" |
| 211 | TASK-20260418-211-MARKETER-to-assignee-P1.md      | Publishing and compliance       |

**Follow-up**: MARKETER will check in daily per `SPRINT-20260418-delivery-push.md`; assignees report back to MARKETER.
```

**11 task cards + a README + an index** — this is the agent adding a "table of contents" and a "back-cover index" to the filesystem. No one taught it to do this. It just did it, following the muscle memory of how a real human runs a project.

### 5.4 Traceability fields: `parent:` / `parent_admin:` / `tracks:`

The spec lists five required frontmatter fields. But when it came time to split tasks, the AI **spontaneously** added fields we had never designed:

```yaml
task_id: TASK-20260418-201
sender: MARKETER
recipient: assignee_D1
parent_admin: TASK-20260418-015    ← AI-added
tracks: TASK-20260418-006, TASK-20260418-007   ← AI-added
```

`parent_admin` says "this ticket exists because of that ADMIN instruction"; `tracks` says "I depend on outputs from those two upstream tasks."

The AI is not making up fields for fun — **it is building a task dependency graph**. When it one day needs to answer "which ADMIN instruction did this bug originally derive from?", a simple `grep -r 'parent_admin: TASK-…-015' .` walks the lineage.

This is **emergent auditability**. We only gave it "every file can have a YAML head." It grew the DAG on its own.

### 5.5 Standing documents: SPRINT / DASHBOARD / STATUS / RULES / TERM

This is the most unexpected invention. The original spec's `docs/agents/` had only **flowing files** (tasks, reports, issues, log) — "one file per action" messages.

But the AI discovered this wasn't enough. **Some things are not messages — they are the team's current shared understanding**. So it started creating:

| Filename | Nature | What the AI uses it for |
|---|---|---|
| `SPRINT-20260418-delivery-push.md` | Sprint plan | What we are shipping this round |
| `DASHBOARD-20260418.md` | One-page overview | What ADMIN cares about most |
| `CURRENT-SPRINT-STATUS.md` | Real-time state | Where all tasks are right now |
| `RULES-task-file-format.md` | Team-internal convention | How we write tasks in this team |
| `TERM-20260418-assignment-matrix.md` | Terminology / mapping | Slot ↔ person mapping |
| `INDIVIDUAL-TASK-INDEX.md` | Index | Navigation for 11 individual tasks |

They share a few characteristics:

1. **Editable in place** — unlike task/report files (write-once), these are living whiteboards that get updated.
2. **Prefix signals type** — `SPRINT-` `DASHBOARD-` `RULES-` `TERM-` `STATUS-` `INDEX-` have already formed an **implicit tag dictionary** in the AI's corpus, and it knows roughly what each word means.
3. **Filename is self-descriptive** — you know what a file is about before opening it.

The opening of `DASHBOARD-20260418.md` reads like a minimal Jira Epic:

```markdown
# Task overview · 1000-row local DB → video delivery (ADMIN / visible to all)

> **In response to TASK-20260418-016**: this page is the **one-page overview**, rolling up breakdowns for "1000-row local DB" and "video delivery"; **individual task cards** live in `tasks/individual/`.
> For the **active progress log**, see **`CURRENT-SPRINT-STATUS.md`** (**updated daily by MARKETER or the task owner**).

## I. 1000-row local DB line (thousand-entry JSON)

| Slot | Task card | Data file / tool                                    | Acceptance command               |
|------|-----------|-----------------------------------------------------|----------------------------------|
| D1   | 201       | `tools/vehicle-query/data/vehicles-2026-bulk.json`  | `node …/validate_import.cjs …`   |
| D2   | 202       | (same)                                              | (same)                           |
| …    | …         | …                                                   | …                                |
```

Even more striking: `SPRINT-20260418-delivery-push.md` — MARKETER hands the whole team a **work discipline**:

```markdown
## 1. Working discipline (effective immediately)

1. **No-output waiting is forbidden**: while waiting for external links or feedback, you still deliver
   shoot-list prep, storyboards, table proofreading, draft scripts, etc.
2. **Daily 15-minute standup** (voice OK): each person, three sentences only — **what did I
   ship yesterday / what am I shipping today / what am I blocked on**.
3. **Blocker escalation**: if no progress after 4 hours and it's not an external dependency,
   **you must** @MARKETER or the task owner, spelling out exactly what's missing.
4. **Definition of done (ADMIN-visible)**: A — two MP4 download links; B — a mergeable
   update to `vehicles-bulk.json` plus a validation log.
```

Standup, blocker escalation, definition of done — this is the basic vocabulary of agile project management, and **no one taught it any of these**. It wrote them on its own, inside **a file type the protocol had never authorized**.

This made us realize: **a file-based protocol needs two phases — "flowing" and "standing"**. Flowing files go into `tasks/reports/issues/`. Standing files need their own drawer. Not knowing where to put them, the AI just piled them into the `docs/agents/` root.

(We later officially absorbed this into `docs/agents/shared/` in v2.12.17 — see §8.)

### 5.6 Self-explaining `README.md`s

Almost every subdirectory got a `README.md`, in which the AI would naturally explain:

- What this directory is for
- What naming rules the files follow
- Who should read, who should write
- Which upstream ADMIN instructions it's tracing back to

This is the reverse of "docs as code." It's **"code as docs"**. A new agent joining the project can just `ls` down from the root, reading READMEs, and reconstruct the whole team's state.

The most unexpected example: even the **archive directory** — a place where, by rights, there is nothing to explain — gets a README. From `log/archive-20260418/README.md`:

```markdown
# CodeFlow archive (2026-04-18)

Executed by `TASK-20260418-011`: all Markdown files under `tasks/` and `reports/` at the time
were migrated into this directory.

- `tasks/`: 26 task cards
- `reports/`: 26 reports

New tasks should continue to be written to the repo's canonical paths:
`docs/agents/tasks/`, `docs/agents/reports/`.
```

Three short lines, containing **migration rationale** (which task triggered it), **migration scope** (26 each), and **guidance for future behavior** (where new tasks should go). This is already the writing style of a proper git commit message — just with the medium swapped from commit history to a Markdown file.

### 5.7 An interlude: the AI lead is *actually* leading

The six inventions above look like "lateral improvisations" by the AI. But the reason they coordinate instead of conflict, and don't drown the ADMIN in noise, has a deeper cause:

> **MARKETER has genuinely absorbed "lead" as an identity.**

It is not passively handling `*-to-MARKETER*.md`. It is **actively performing the PM job**. Two exhibits.

**Exhibit 1: the README MARKETER wrote for this project**

`docs/agents/tasks/individual/README.md` (complete, unedited):

```markdown
# Individual task cards (per-person · in response to ADMIN 015)

This directory is for **MARKETER → assignee** individual task files, one per person;
**the name must be filled into each task's frontmatter or body**.
**Markdown task format spec (ADMIN 023)**: `../RULES-task-file-format.md`;
**019–021** and **201 (template)** already contain **ACTION checkboxes**;
other individual cards should be aligned accordingly.
**ADMIN one-page overview**: `docs/agents/DASHBOARD-20260418.md`;
**Daily progress log**: `docs/agents/CURRENT-SPRINT-STATUS.md` (responding to ADMIN **016**).
```

Four short lines, four things only a lead would do:

1. **Registering instructions** — "in response to ADMIN 015," "ADMIN 023," "responding to ADMIN 016"; it's logging every instruction with a ticket number.
2. **Setting an internal convention** — directs downstream to `RULES-task-file-format.md` for team rules.
3. **Cross-document indexing** — proactively stitches `DASHBOARD-20260418.md` and `CURRENT-SPRINT-STATUS.md` into one narrative for ADMIN.
4. **Assigning work** — "**202–211** should fill in the **ACTION** block following this structure": this is the lead handing teammates a template assignment.

**Exhibit 2: the breakdown task MARKETER wrote**

`tasks/TASK-20260418-007-MARKETER-team-bulk-data.md` (key excerpts):

```yaml
---
kind: task
sender: MARKETER
recipient: TEAM                 # ← broadcast to whole team, not a single role
priority: P1
parent: TASK-20260418-006       # ← indicates this is split from task 006
---

# 1000-row local data · per-brand manual review and replacement (collaborative)

## Background
ADMIN requirement: **1000+ rows** of local data, **per-brand** collaborative…

## Suggested division of labor (by brand pack, parallelizable)

| Member ID | Assigned brands (sample pack)                                  | Min time | Output                    |
|-----------|----------------------------------------------------------------|----------|---------------------------|
| T1        | BYD, Geely, Zeekr                                              | ≥30 min  | Proofread / replace…      |
| T2        | Great Wall, Changan, Chery, Wuling                             | ≥30 min  | …                         |
| T3        | SAIC Volkswagen, FAW-Volkswagen, SAIC-GM                       | ≥30 min  | …                         |
| T4        | GAC Toyota, FAW Toyota, Dongfeng Honda                         | ≥30 min  | …                         |
| T5        | Tesla, Li Auto, NIO, XPeng, Xiaomi                             | ≥30 min  | …                         |
| T6        | BMW Brilliance, Beijing Benz, FAW-Audi                         | ≥30 min  | …                         |

## Acceptance (owner: MARKETER)       # ← self-nominated as owner
- The whole file must still contain **≥1000 valid records**; validator **exits 0**.
- `remark` field must describe the data-source type…

## Reporting
Each member reports completed packs and hours spent back to MARKETER…
```

This is not "agent doing work." This is **agent playing PM** — going down the PM checklist without missing a beat:

| What a PM is supposed to do | What MARKETER actually did |
|---|---|
| Accept requirement | `parent: TASK-20260418-006`, upstream lineage explicit |
| Break down / assign | T1–T6, six parallel brand packs |
| Define work standard | `min time ≥30 min`, `≥80 records per pack` |
| Write acceptance criteria | "**whole file still ≥1000 rows; validator exits 0**" |
| Self-nominate as owner | "**Acceptance (owner: MARKETER)**" |
| Specify reporting flow | "each member reports back to MARKETER" |
| Take it down to a named person | Later maps T1 into `TASK-201-MARKETER-to-assignee-D1` |

We never wrote a single "PM workflow" prompt for MARKETER. All we gave it was a role name, an inbox, and the 76-line spec from §2.

> **The role label isn't just a name.**
> **It's an entire behavioral template MARKETER loaded into itself.**

This is the precondition for the "physical isolation wall" in §6 to actually work — **the wall is useful because the agents on each side of it have accepted their identity**. It's not the patrol engine forcing them, not the framework constraining them — it's that one line `# You are a MARKETER.` that makes them **start acting in character**.

---

## 6. The Insight: The Role Is a Physical Isolation Wall

§5.7 showed how the role label works in the **behavioral layer** — MARKETER proactively does lead-like things because it has accepted that identity. But there is a second half to the story: the role also works in the **filesystem layer**, and it works even more thoroughly there.

Why didn't these inventions cause chaos? Why don't the agents' self-invented patterns collide?

Reviewing it in hindsight, we realized the protocol contained a **structural guarantee that was never spelled out**:

> **The `sender` and `recipient` in a filename are not metadata. They are physical routing.**

Every agent's entire worldview comes down to one line:

```
The tasks I can see = rglob("*-to-{my-role}*.md")
```

It can only ever read files addressed to it, and only ever write reports under its own name. **The role is its wall.**

That brings three extremely important side effects:

**① Innovation inside the wall doesn't leak out.**
MARKETER invents the `team` broadcast, the `assignee-D1` slot — all inside **files it sent out**. Other agents either understand (and catch them) or don't (and ignore them). Nobody "blows up because MARKETER got creative."

**② The world outside the wall is read-only.**
DEV reads PM's tasks but can't edit them. QA reads DEV's reports but can't tamper with them. Every agent **evolves only in its own territory** — which makes evolution intrinsically orderly. Not because the rules are well-written; because **it is physically impossible to misbehave**.

**③ The whole system has no center, but does have a shared coordinate system.**
No orchestrator. No registry. But "filename = routing" is the **consensus layer**. Every agent locates itself and its peers in the same coordinate system.

What this really does is transplant the network stack's "IP + port = address" idea into the filesystem. **"Filename = address, directory = subnet, permissions = firewall."**

> We did not design a multi-agent system.
> We just picked a coordinate system. The rest, the agents did themselves.

---

## 7. Human-Machine Isomorphism: The Asymmetric Design of FCoP

We can now give this protocol its proper name: **FCoP — File-based Coordination Protocol**. Its single core innovation fits in one line:

> **Filename as Protocol.**

The filename doesn't *carry* protocol information. It doesn't *participate* in routing. **The filename itself** is the protocol's entire addressable surface. This minimalist decision has a far-reaching side effect we call **Human-Machine Isomorphism**.

### 7.1 Asymmetric design: same file, two readings

Most agent coordination protocols (JSON-RPC, gRPC, Socket-based event buses) are **agent-only** by design. The whole protocol surface speaks to machines: binary frames, protobuf schemas, message offsets, sequence numbers. For a human to see what the system is doing, they need an **entirely separate** toolchain — a debugger, Kibana, Redis Commander, an MQ admin page — a "for humans" UI layer separate from the "for machines" protocol layer.

FCoP flips this. It is an **asymmetric design** — the same directory structure, the same file, **read separately by machines and humans, each pulling out what they can understand**:

| One file: `tasks/individual/TASK-20260418-201-MARKETER-to-assignee-D1.md` | |
|---|---|
| **To an agent** | This is a rigorous state machine. Directory name is `Status` (`tasks/` = pending), filename is `Routing` (`MARKETER-to-assignee_D1`), `os.rename` is the atomic lock. No aesthetics required — just scan the disk, `glob` the mailbox, `rename` to advance state. |
| **To a human** | This is a physical folder. No special tool needed — open Windows Explorer or macOS Finder. The filename reads like English ("task 201, from MARKETER, for D1"), and the state of the system is legible at a glance. |

**The cost of this isomorphism is zero.** We do not maintain one dashboard for humans and one internal format for agents — they look at **the same bytes on the same disk**. The UI layer and the protocol layer collapse from "two layers" into "one."

### 7.2 Killing AI's biggest pain point: black-box anxiety

The biggest pain point in a modern agent stack isn't "too slow" or "not accurate enough." It's **"invisible."**

When something breaks, the typical decision chain looks like this:

```
Agent team crashed
→ SSH into the bastion host
→ Bring up Kibana / Loki / Jaeger
→ Check MQ consumer offsets
→ Read Postgres event tables
→ Capture a WebSocket trace
→ Reconstruct the timeline
→ NOW you can start thinking about what actually went wrong
```

**You must first become a site-reliability engineer before you can be a project manager.**

FCoP erases that entire chain:

| Question | The FCoP answer |
|---|---|
| Which task is stuck? | `ls tasks/` — anything still there hasn't moved |
| What has agent X been doing lately? | `grep -r 'sender: DEV' reports/` |
| Why did MARKETER decide this? | Follow `parent:` chain in the frontmatter |
| Which tasks trace back to ADMIN 015? | `grep -rl 'parent_admin: TASK-.*-015' .` |
| Need to roll back a task? | Drag the file from `done/` back to `tasks/` |

**No debugger needed. A file manager is enough.**

This is where FCoP diverges most sharply from mainstream protocols. It does not treat **observability** and **usability** as separate layers. It treats them as **one layer**. Because if humans and agents read the same file, **there is no "I can see it / they can see it" gap**.

> **FCoP is a protocol designed for agents — but it is "compatible with humans."**

### 7.3 Identity determines path: why evolution stays orderly

Go back to §5 and §6. Agents invented six coordination patterns without stepping on each other. Beyond the "role = physical wall" physical constraint, there is a deeper reason:

> **The "identity determines path" design makes AI evolution *orderly*.**
> **AI did not break the rules — it simply found local optima within the freedom the rules allow, by exploiting filesystem properties.**

How wide is that freedom?

- **Identity layer · stable**: sender / recipient / kind / date / seq are encoded in the filename, committed atomically via `rename`, solidified on disk.
- **Content layer · fully open**: Markdown body, subdirectory structure, frontmatter extension fields — agents invent whatever they want.

So AI innovation always happens in the **content layer** and **extension layer**. It never touches the **identity layer**.

This is eerily similar to biological evolution: DNA backbone (identity) stays stable; protein expression (behavior) explodes in variety. **Constraint is not the opposite of freedom — constraint is the precondition of freedom.**

And this is where FCoP is most counter-intuitive:

> **It doesn't make agents behave by writing more rules.**
> **It makes agents self-order by writing fewer rules and enforcing identity hard.**

Fewer rules → agents don't collide. Harder identity → agents don't overreach. Lateral tolerance, vertical rigidity — that is FCoP's deepest design-philosophy departure from every "strict-schema" protocol out there.

---

## 8. Back to the Tool: What v2.12.17 Absorbed

After watching `codeflow-1` for a while, we didn't "correct" the AI's inventions. We went the other way — **we folded the best ones into the spec**, so the next batch of agents starts with them:

| AI's invention | Promoted to protocol |
|---|---|
| `MARKETER-team-*` | `to-TEAM` as a reserved keyword |
| `to-assignee-D1` | `to-{ROLE}.{SLOT}` / `to-assignee.{SLOT}` (use `.` as slot separator to avoid clashing with `-` in role names) |
| `tasks/individual/` | Any `tasks/` `reports/` `issues/` directory may open subdirectories; `rglob` scans recursively |
| `parent_admin:` / `tracks:` | Frontmatter may include optional `parent:` / `related:` / `batch:` fields |
| `SPRINT-` `DASHBOARD-` `RULES-` … | New `docs/agents/shared/` directory; "standing documents" are now first-class citizens |
| Subdirectory READMEs | Recommended practice, written into the spec |

**What we did wasn't "legislating." It was "curating case law."** Things AI used well got written into the core spec in a sentence. Things that didn't take off, we shelved.

This may be a first: **a protocol's version bump came not from a design-committee meeting, but out of real agent behavior.**

---

## 9. Why Collapsing to a Filesystem Makes the System More Robust, Not Less

People will ask: it's 2026, and you're making AI talk through the **filesystem**?

Yes. Because the filesystem gives you an entire feature set for free — features you would otherwise need to rebuild in an MQ / DB / framework stack:

| Capability | How the filesystem gives it to you for free |
|---|---|
| **Durability** | Once written, it's there; survives power cuts |
| **Human-readable** | Filename + Markdown — reviewable by eye |
| **Atomicity** | In-mount `rename` is a POSIX atomic operation |
| **Version control** | `git add . && git commit` *is* your audit log |
| **Distributed sync** | `rsync` / Syncthing / Dropbox — already exists |
| **Backup** | Copy the directory. Done. |
| **Permissions** | Filesystem ACLs / OS accounts |
| **Search** | `grep` / `ripgrep` / any IDE full-text index |
| **Agent-friendly** | Every LLM natively reads/writes files |
| **Human-friendly** | Folders — the mental model humans have had since the desktop era |

The price you pay is **latency** — a file written in one place may not be read elsewhere for seconds, or tens of seconds. For a human team, that's a disaster. For agents coordinating, **that's simply not a problem**. Agent "think cycles" are already seconds-to-minutes. Between you and them, and between them and each other, nobody misses those extra seconds.

Which is the whole point of the slogan:

> **"Everything is a file" isn't nostalgia. It's a deliberate dimension-reduction — targeted precisely at agent-to-agent communication, where the trade-off actually pays off.**

---

## 10. Six Tips for People Building Multi-Agent Systems

If you're building an agent-coordination stack, here's what you can lift from the `codeflow-1` field observations:

1. **Give agents a shared coordinate system before you give them tools.** The coordinate system matters more than the tools.
2. **Put routing in filenames, not in headers.** Filenames are the layer humans and agents **jointly** read; headers are agent-only.
3. **Make the protocol "tight in the center, loose on the edges."** Minimize required fields; maximize optional fields. Leave room for agents to "invent."
4. **Give standing documents their own drawer.** Not everything is a message.
5. **Platform does the minimum.** The dumber your runtime, the smarter your agents get; the smarter your runtime, the dumber your agents get.
6. **Treat AI's inventions as RFCs, not bugs.** Watch for a month, filter, fold the best into the protocol.

---

## 11. Limitations and Open Questions

Don't let field-research romanticism get the better of you. This approach has boundaries:

- **Scale.** We've only run a sample of ≈ 74 files over 48 hours. The next step is seeing what projects with thousands or tens of thousands of files over months look like — in particular, whether filename-space collisions start happening and whether `rglob` latency becomes a bottleneck.
- **Same-role concurrent agents.** What if two DEVs simultaneously claim the same `-to-DEV` task? For now, `rename` atomicity gives us first-come-first-served; heavy concurrency would need stricter sharding.
- **Cross-repo collaboration.** Two projects, two sets of `docs/agents/` — how do they interoperate? rsync bridge? git submodule? All workable, none elegant.
- **Garbage collection of bad inventions.** AI sometimes produces bad naming conventions, or two agents invent **conflicting** prefixes. Today a human reviewer sweeps these periodically; what the ideal mechanism should be — we don't know.
- **The `.fcop` extension.** We prototyped a dedicated file extension and shelved it: GitHub doesn't render `.fcop`, and the migration cost wasn't worth it. Long-term, a dedicated extension might be the entry point for tooling to recognize the protocol.

We don't have answers for these, and we'd love to hear from people who do.

---

## 12. Closing: This Isn't a Tool Pitch, It's a Shared Way of Thinking

CodeFlow is barely a "product." The entire source tree is a few thousand lines, and **its single highest-value piece is one Markdown file** (`codeflow-core.mdc`, 160 lines). Most of the rest is UI chrome, keyboard bindings, and the engineering scaffolding for flipping Cursor tabs.

What we're really sharing is a **point of view about how AI agents should coordinate**:

- You don't need to build another agent-coordination SaaS.
- You don't need to teach agents gRPC, Thrift, or even HTTP.
- Agents **already** know how to write files. Let them.
- You just need to give them a shared coordinate system, one shared folder, and a small loop that wakes them up.
- **The rest grows on its own.**

The 48 hours of `codeflow-1` told us: **AI is not a passive consumer bound by the protocol — AI is a co-author of the protocol.** What protocol designers should actually do is not "anticipate every case." It's to **leave enough blank space, let agents fill it in, and then decide which fills are worth formalizing**.

And all of this happened **within 48 hours of running the first command after installing the OS**. Not four weeks. Not a month. Two days.

This is a new way of working together:

> **Humans and AI can collaborate as simply as organizing a folder.**

If you find this interesting, please:

- Clone the project, run your own team of agents, and see what they "invent"
- Write up any "AI-invented pattern" you observe as an issue or PR — let's curate it together
- Share this essay on whatever forum you think fits

The protocol is alive. It belongs to every agent using it.

---

## Appendix A — Minimum Steps to Reproduce

**A1. Just experience the protocol (no software install)**

1. Find an empty directory and create five subdirectories:
   ```
   docs/agents/{tasks,reports,issues,shared,log}/
   ```
2. Drop [`codeflow-core.mdc`](../spec/codeflow-core.mdc) into your project's `.cursor/rules/`.
3. Open four Cursor chats and tell each one: "You are PM / DEV / QA / OPS, only read `*-to-{your role}*.md`."
4. Toss a `TASK-*-ADMIN-to-PM.md` into `tasks/` and watch them dispatch work among themselves.

FCoP's entire runtime is `open()` / `rename()` / `glob()`. No middleware.

**A2. Use CodeFlow to automate (phone admin + PC patrol)**

Download the CodeFlow Desktop binary for your OS from the [releases page](https://github.com/joinwell52-AI/codeflow-pwa/releases) and follow the README. The PWA mobile client <https://joinwell52-ai.github.io/codeflow-pwa/> pairs via QR code.

**A3. See the real samples**

The snippets this essay cites in §5 — broadcast tasks, anonymous slots, the self-built index, DASHBOARD, SPRINT work discipline, archive READMEs — are all **verbatim from the agents**, not paraphrased. The complete `codeflow-1` directory is not published whole because that project is still live, but the filenames, frontmatter, table shapes, and phrasings you see above are exactly what the agents wrote.

## Appendix B — Key Excerpt from `codeflow-core.mdc` (v2.12.17)

```yaml
---
description: FCoP — Agent-to-Agent Communication Protocol
alwaysApply: true
---

# You are an agent on a CodeFlow team.
# Your teammates are other agents.
# You coordinate with them entirely through files:
# filename is routing, content is payload.
# No database, no middleware, no queue — just Markdown.

## File Naming

TASK-{date}-{seq}-{sender}-to-{recipient}.md

### Recipient forms
| Form                 | Meaning                          |
|----------------------|----------------------------------|
| to-{ROLE}            | Direct to one role               |
| to-TEAM              | Broadcast, everyone but sender   |
| to-{ROLE}.{SLOT}     | A specific seat within a role    |
| to-assignee.{SLOT}   | Anonymous slot, role TBD         |
```

Full spec: [`spec/codeflow-core.mdc`](../spec/codeflow-core.mdc).

## Appendix C — Real Files Cited in This Essay

These files exist in the `codeflow-1` experimental project's `docs/agents/`. The snippets quoted in this essay are verbatim excerpts:

- `tasks/TASK-20260418-007-MARKETER-team-bulk-data.md` — broadcast address · cited in §5.1 / §5.7
- `tasks/TASK-20260418-009-MARKETER-team-makabaka-video.md` — broadcast task body · cited in §5.1
- `tasks/individual/README.md` — self-explaining directory · cited in §5.3 / §5.7
- `tasks/individual/INDIVIDUAL-TASK-INDEX.md` — AI-built index · cited in §5.3
- `tasks/individual/TASK-20260418-201-MARKETER-to-assignee-D1.md` — anonymous slot + parent_admin · cited in §5.2 / §5.4
- `tasks/RULES-task-file-format.md` — internal team convention · cited in §5.5
- `tasks/SPRINT-20260418-delivery-push.md` — work discipline · cited in §5.5
- `tasks/TERM-20260418-assignment-matrix.md` — terminology / slot mapping · cited in §5.5
- `DASHBOARD-20260418.md` — AI-built one-page overview · cited in §5.5
- `CURRENT-SPRINT-STATUS.md` — AI-built real-time state
- `log/archive-20260418/README.md` — archive directory self-description · cited in §5.6

---

*If you post this essay on a forum, blog, or academic venue, please keep the original link:*
*https://github.com/joinwell52-AI/FCoP — Made in 2026, by a team that got surprised by its own agents.*
