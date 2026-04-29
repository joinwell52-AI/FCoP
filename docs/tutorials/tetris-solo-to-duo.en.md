# [Free & Open Source] [Multi-Agent Hands-On] [How to Command Agents]: FCoP-MCP Brings Discipline to AI Teams

### From Solo Tetris to a 2-Person AI Crew — a 45-minute field tutorial with `fcop-mcp`

![FCoP-MCP tutorial cover · Multi-agent discipline via the filesystem](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/assets/fcop-mcp-tutorial-cover-v1.png)

> *"You are not a coder anymore. You are a commander. The agents are your digital employees."*
>
> *"In the FCoP world, ADMIN's two most-used phrases are **'Start work.'** and **'Inspection.'** Everything in between is the agents talking to each other through files."*
>
> A 45-minute hands-on walk-through with `fcop-mcp` 0.7.2 inside Cursor: have the agent install itself, ship a Tetris-style game in solo mode, switch to a 2-person crew with `PLANNER` + `CODER`, watch them design and implement a creative variant, reject v1 over real gameplay defects, watch the rework loop close itself, then ask both agents on the record what they think of the protocol. **Every step is real, every file is on disk, every screenshot is from the same 45-minute session.** ~25 minutes of reading. There is a [Chinese sister case study](snake-solo-to-duo.zh.md) using a Snake game — same protocol, different dogfood. Read either one first.

**Author**: FCoP Maintainers · 2026-04-29
**Keywords**: FCoP, fcop-mcp, MCP for Cursor, multi-agent collaboration, role boundaries, append-only history, ADMIN as commander, file-based protocol, "Start work" "Inspection" dialect, agent context budget, single-agent context explosion, true-positive role-switch evidence, agent self-assessment, six iron rules of commanding agents

---

## Why this exists

Three things every Cursor / Copilot / Claude Code user has hit, whether or not they had a name for them:

1. **Single-agent context explosion is real.** When one agent does everything — design, code, test, document, refactor — its context window becomes a landfill of half-relevant snippets. The agent gets slower, dumber, and more confidently wrong, all at once.
2. **You are not a coder anymore. You are a commander.** The market is moving from "humans write code, AI helps" to "humans state intent, AI writes code." If you keep writing the code yourself, you are buying tickets to a play that already ended. The interesting skill is *commanding* — picking what to build, dispatching it, signing it off. By the end of this tutorial you'll see the dialect collapses into two phrases: **"Start work."** and **"Inspection."**
3. **Files, not chats, are the only auditable substrate.** Chat scrollback is a goldfish. Files are a ledger. Every record on disk is for one purpose: **manage, trace, audit, keep order, hold rules**.

`fcop-mcp` is the MCP server that turns those three observations into something runnable inside Cursor. It implements the [FCoP](https://github.com/joinwell52-AI/FCoP) protocol — a minimalist multi-agent coordination protocol whose only sync primitive is `os.rename()` over a folder tree. No database, no message queue, no daemon. State is folders, routing is filenames, payload is Markdown. **Filename as protocol.**

This tutorial walks one continuous machine session that touches all three observations:

| Phase | Time | What you'll see |
|---|---|---|
| 1. Install | ~5 min | The agent installs `uv`, `fcop-mcp`, and edits `mcp.json` for you. You don't run a single command. |
| 2. Solo Tetris | ~15 min | One natural-language brief → agent translates it into a `TASK-*.md` file → ships `Nebula Stack`, a working single-file Tetris clone → reports back → archives. The four-step cycle. |
| 3. Switch to a 2-person crew | ~5 min | One sentence: `create_custom_team(force=True)` with `PLANNER` + `CODER`. The solo `ME` setup gets archived under `.fcop/migrations/<timestamp>/` (Rule 5). Each agent gets its own `TEAM-*.md` employee handbook. |
| 4. A creative variant, with a real review loop | ~15 min | ADMIN: *"surprise me with a creative Tetris variant."* PLANNER designs `Comet Loom`. CODER builds v1 in a separate chat tab. ADMIN plays it, finds three blocking defects, bounces it back. PLANNER writes `TASK-006` with a new `Verification Requirements` section. CODER ships v2. Two cycles, all on disk. |
| 5. The protocol speaks for itself | (caught silently) | `fcop_check()` reveals the protocol logged **8 `role-switch-*.md` evidence files** during the dogfood — soft warnings the agents never saw during work. PLANNER and CODER are then asked, on the record, what they think of FCoP. They self-endorse, name the RLHF tension by name, and one of them files PR-grade product feedback. |

If you're allergic to long tutorials: jump to **Six iron rules** at the bottom. The rest of the document is the *evidence* those rules came from.

> **Want to try it right now?** Skip straight to **Phase 1 below** — install takes ~5 minutes, you don't run a single command yourself, and you'll have a working Tetris-style game inside Cursor in under half an hour. The article will still be here when you come back.

---

## Phase 1 — Install via natural language only

Open Cursor. Open an empty folder (e.g. `D:\fcop-mcp-test`). What you should see is just this — a fresh editor, an empty workspace, a blank chat. Nothing magic happens yet.

![Cursor opened on an empty folder before the install — blank workspace, default UI, English locale, the canvas this whole tutorial starts from](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/docs/tutorials/assets/tetris-en/cursor-new-en-0.png)

Paste this into the chat box:

> Install `fcop-mcp` into Cursor for me. Run every command yourself. Steps:
>
> 1. Detect my OS (`uname -s 2>$null; echo $env:OS`).
> 2. Install `uv` if missing (`irm https://astral.sh/uv/install.ps1 | iex` on Windows; `curl -LsSf https://astral.sh/uv/install.sh | sh` on macOS/Linux). Confirm with `uvx --version`.
> 3. Add `fcop` to my global `mcp.json` (`%USERPROFILE%\.cursor\mcp.json` on Windows, `~/.cursor/mcp.json` on macOS), keeping any existing servers:
>
>    ```json
>    "fcop": { "command": "uvx", "args": ["fcop-mcp"] }
>    ```
>
> 4. Print the final `mcp.json` content for me to verify.
> 5. Tell me to restart Cursor and wait 30–60 s on first launch (uvx pulls deps).
>
> Report after each step. Do **not** auto-initialise the project — that's my call.

The full prompt is maintained in [`agent-install-prompt.en.md`](https://github.com/joinwell52-AI/FCoP/blob/main/src/fcop/rules/_data/agent-install-prompt.en.md) and is also exposed as an MCP resource `fcop://prompt/install` so an agent in a fresh session can read it directly. After restart, type `fcop_report()` in chat. You should see something like `fcop-mcp 0.7.2 — not initialised — rules/protocol up-to-date`. **The agent ran every command. You commanded.**

![Cursor Settings shows fcop with 26 tools fully expanded — `init_solo`, `write_task`, `write_report`, `fcop_check`, etc. — while the right-hand chat shows the agent walking through the install prompt step by step](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/docs/tutorials/assets/tetris-en/fcop-mcp-setup-0.png)

When the dust settles, this is what installed-and-ready looks like — `mcp.json` updated, `uvx` cached the package, Cursor sees `fcop` as an active MCP server, and `fcop_report()` returns the not-yet-initialised state.

![After restart: `fcop_report()` returns "fcop-mcp 0.7.2 — not initialised — rules/protocol up-to-date". The MCP server is live but no project is bound yet — exactly the state you want before initialising](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/docs/tutorials/assets/tetris-en/fcop-mcpsetup-over.png)

---

## Phase 2 — Solo Tetris (the four-step cycle)

Tell the agent who it is, then drop a one-line brief:

> 1. `set_project_dir("D:/fcop-mcp-test")`
> 2. `init_solo(role_code="ME", lang="en")`
> 3. *"Build a working Tetris-style game as a single HTML file with no external dependencies. Choose a name, make it fun, include items / power-ups, skins, decent visuals, and cool effects. Use the FCoP four-step cycle."*

Notice what just happened. **You spoke five lines of natural English.** The agent expanded that into a structured product spec — required features, accept criteria, runnability check — and wrote it as `docs/agents/log/tasks/TASK-20260429-001-ADMIN-to-ME.md`. That translation is the value. The agent didn't ask for a brief; it produced one, signed in your name, on disk.

This is **Rule 0.a.1**, the FCoP "four-step cycle":

```
TASK  →  do  →  REPORT  →  archive
```

Over the next ~15 minutes:

- The TASK file lands in `docs/agents/log/tasks/`.
- The game file (`workspace/nebula-stack/index.html`) gets written.
- A `REPORT-001-ME-to-ADMIN.md` lands in `docs/agents/log/reports/`. ME named the game **Nebula Stack** — single HTML, no dependencies, with falling blocks, hold + next preview, scoring, levels, three power-ups (`Bomb`, `Stasis`, `Prism`), three skins (`Aurora Candy` / `Ember Arcade` / `Moonstone Mono`), and a starfield background.
- `archive_task` moves both files into the historical log. **From now on those files are immutable** (Rule 5: append-only history).

When you open `nebula-stack/index.html` in a browser, it works. But the actual deliverable isn't the game. It's *the four-step cycle running on its own*. From here on, every time you give the agent something to do, that loop will run.

![ME mid-build of *Nebula Stack* — the agent is writing the single-file HTML implementation directly under `workspace/nebula-stack/`, not in chat. Notice how the four-step cycle gets the chat out of the way of the deliverable](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/docs/tutorials/assets/tetris-en/fcop-solo-Build-1.png)

![*Nebula Stack* in the browser — the Tetris-style game ME shipped from a one-line natural-language brief; falling blocks, three skins, three power-ups, single HTML file, zero dependencies](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/docs/tutorials/assets/tetris-en/game-0.png)

### What lives on disk after `init_solo`

```
fcop-mcp-test/
├── .cursor/rules/fcop-rules.mdc      # the agent's rulebook
├── AGENTS.md  CLAUDE.md              # host-neutral entry points
├── .fcop/                            # protocol metadata, version pins, role lock
├── docs/agents/
│   ├── shared/
│   │   ├── TEAM-README.md            # what this team is, in plain English
│   │   ├── TEAM-OPERATING-RULES.md   # the four-step cycle, role uniqueness, etc.
│   │   └── TEAM-ROLES.md             # who's `ME`, what they're allowed to do
│   ├── log/{tasks,reports}/           # the immutable ledger
│   ├── tasks/  reports/  issues/      # the live inboxes
│   ├── fcop.json                      # project config (mode, roster, lang)
│   └── ...
└── workspace/                        # the actual code lives here
```

![The actual file tree right after `init_solo` — file names match the ASCII sketch above; this is the disk truth, not a diagram](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/docs/tutorials/assets/tetris-en/fcop-mcp-solo-0.png)

Three folders deserve a moment.

- `.cursor/rules/fcop-rules.mdc` is loaded by Cursor on every turn. The agent literally cannot forget the protocol because Cursor reminds it.
- `docs/agents/shared/TEAM-*.md` is the agent's **employee handbook**. In solo mode it tells `ME` "you are the only employee, you do everything"; in team mode it tells `PLANNER` what `PLANNER` is responsible for and what `CODER` is responsible for.
- `docs/agents/log/` is the ledger. It only grows. Corrections happen by writing a *new* report that supersedes an old one — never by editing.

If you ask the agent in a fresh chat *"who are you?"*, it will not say "I am GPT-5.5, your assistant." It will read `.fcop/team.json` and `docs/agents/shared/TEAM-ROLES.md` and tell you it is `ME`, it serves ADMIN, it works through the four-step cycle, it delivers in `workspace/`. **The agent's identity now lives on disk, not in chat.** That's the whole point of the protocol made tangible.

![Asked "who are you?", the agent reads `.fcop/team.json` aloud and explains its role from `TEAM-ROLES.md` — identity-on-disk in action](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/docs/tutorials/assets/tetris-en/fcop-mcp-solo-1-who.png)

---

## Phase 3 — Switch to a 2-person crew, in one sentence

Drop this into chat:

> *Switch the team to two people: `PLANNER` and `CODER`. PLANNER designs, CODER implements. Use `create_custom_team(force=True)`, keep `lang="en"`, and tell me what gets archived.*

The agent calls `create_custom_team` with the new roster. What happens on disk:

- The old `fcop.json`, the solo `shared/TEAM-*.md` files, the LETTER-TO-ADMIN entry-point letter, and the previous `.cursor/rules/` get **archived** under `.fcop/migrations/20260429T112757/` — a local time capsule, no git required. (Yours will have a different timestamp; mine was 11:27:57 on the dogfood day.)
- New `shared/TEAM-*.md` files describe a 2-person crew, with separate responsibility sections for `PLANNER` and `CODER`.
- `fcop.json` and `.fcop/team.json` update to the new roster (`mode: team`, `roles: [PLANNER, CODER]`, `leader: PLANNER`).
- **Crucially: `docs/agents/log/` is not touched.** `Nebula Stack`'s TASK and REPORT from Phase 2 stay where they are, immutable. ME is off the payroll, but ME's deliverable is still in the ledger. That's Rule 5 — append-only history.
- The current chat session is **still bound to a single role**. If you want PLANNER and CODER to work concurrently, you open *two* Cursor chat tabs — one bound to PLANNER, one to CODER — and they communicate through `TASK-*.md` files, not through chat.

This is **Rule 1: Two-Phase Startup**. Initialise once, assign roles forever after. And **Rule 5 again**: solo-mode history doesn't get deleted, it gets sealed and dated.

![The agent reports the migration result — old solo files archived under `.fcop/migrations/20260429T112757/`, new team `shared/` files in place, `docs/agents/log/` untouched](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/docs/tutorials/assets/tetris-en/fcop-team-0.png)

After migration, you'll typically run two Cursor chat tabs side by side — one bound to PLANNER, one to CODER — and they communicate **only** through the TASK / REPORT files in `docs/agents/`. No chat-to-chat handoff. No copy-paste of design notes. The protocol made the file path the path of least resistance.

![Two Cursor chat tabs after the team migration — PLANNER on the left, CODER on the right, both freshly initialised under the new 2-person team. From this point on they speak only through TASK and REPORT files](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/docs/tutorials/assets/tetris-en/fcop-team-1.png)

---

## Phase 4 — Comet Loom: design, ship v1, fail review, ship v2

ADMIN says, in chat to the PLANNER session:

> *"Surprise me with a creative variant of that Tetris game. Break the metaphor. Pick the name, the theme, the mechanic twist yourself. Single HTML file. Don't write any game code yourself — that's CODER's job."*

![ADMIN dropping the natural-language brief into PLANNER's chat tab — one sentence, no structured spec. PLANNER's job is to translate that intent into a real TASK file](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/docs/tutorials/assets/tetris-en/fcop-team-planner-2.png)

PLANNER spends 5 minutes thinking and produces a real product brief, not a vibe. The variant is named **Comet Loom**: the board is a vertical loom suspended in space, falling pieces are *thread constellations*, line clears are renamed *completed weft lines*, a `Tension` meter tracks how close the loom is to overflowing, three named charms (`Needle` / `Knot` / `Gale`) get earned by play, five skins are specced (`Deep Aurora`, `Solar Loom`, `Rain Archive`, `Moss Galaxy`, `Paper Lanterns`). The brief is written as [`TASK-20260429-003-PLANNER-to-CODER.md`](assets/tetris-en/evidence/tasks/TASK-20260429-003-PLANNER-to-CODER.md), 130-odd lines of acceptance criteria. PLANNER also writes a one-paragraph `REPORT-003-PLANNER-to-ADMIN.md` saying *"design ready, dispatched to CODER as TASK-003."* Then PLANNER stops.

![PLANNER's design brief for *Comet Loom* — a vertical-loom theme, weft-line clears, three charms, five skins, all dispatched to CODER as TASK-003](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/docs/tutorials/assets/tetris-en/fcop-team-planner-3.png)

You **open a new Cursor chat tab** (this is non-negotiable — see Phase 5), bind it to CODER, and tell it to check inbox. CODER reads `TASK-003`, builds `workspace/comet-loom/comet-loom.html` v1, writes a completion report, archives. **At no point did PLANNER and CODER chat directly.** Their entire collaboration is the TASK and the REPORT.

![CODER picking up TASK-003 from inbox and starting work on Comet Loom v1 — note that CODER never saw the chat in PLANNER's tab; everything CODER knows about the design comes from the TASK file alone](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/docs/tutorials/assets/tetris-en/fcop-team-coder-2.png)

### The bounce

ADMIN plays v1 and finds three blocking defects:

1. **Pieces disappear at the bottom instead of stacking.** The motif-clear rule was being triggered by every fresh same-coloured piece — every 3+ connected same-colour cells qualified, including the just-locked piece itself.
2. **Motif elimination is invisible.** Even when it triggers, there's no visual feedback to tell the player it's a motif clear vs. a normal weft-line clear.
3. **Three of the five skins look identical.** PLANNER specced palette-only changes; CODER implemented exactly that, and the result is dull.

ADMIN does **not** open the file and start fixing it. ADMIN does not even open a new chat to "talk it through." ADMIN goes back to the PLANNER chat tab and writes a one-line natural-English brief: *"v1 has these three blocking issues; write a rework task to CODER and require runtime evidence this time."*

PLANNER writes [`TASK-20260429-006-PLANNER-to-CODER.md`](assets/tetris-en/evidence/tasks/TASK-20260429-006-PLANNER-to-CODER.md). It is structurally different from TASK-003 in one important way: it has a new section called **`Verification Requirements`**, demanding CODER perform and report **runtime checks**:

- *Start a new game and let a piece fall to the bottom; confirm it remains on the board after locking.*
- *Drop a second piece onto or near the first; confirm stacking works.*
- *Trigger a motif clear; confirm matched cells are visibly removed with effects.*
- *Switch between at least three skins and confirm the appearance is materially different.*

![PLANNER writing TASK-006 — the rework brief, with the new `Verification Requirements` section that demands runtime checks, not static lint passes. This section did not exist in TASK-003; it is the closed loop tightening itself](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/docs/tutorials/assets/tetris-en/fcop-team-planner-4.png)

CODER picks up TASK-006, ships v2, reports back. The motif rule is fixed. Stacking works. Three skins are visually distinct. The cycle closes.

![*Comet Loom* v2 running — falling thread constellations, weft-line clears with motif bursts, the Tension meter rising, and a visually distinct skin from v1's defaults](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/docs/tutorials/assets/tetris-en/game-1.png)

This bit surprises people who haven't run a multi-agent flow before. **The agents have learned to behave like an actual two-person team** — not because they're "smart enough," but because the protocol made *speaking through files* the easiest path. The hard path would be to fight the protocol. They don't. And — separately worth noting — when ADMIN bounces v1, the protocol turns rejection into a *handoff routed through grammar* (a new TASK, not a destructive edit on the old one), and PLANNER reflexively tightens its own brief. The closed loop is what closes the gap, not anyone being clever.

---

## Phase 5 — The protocol speaks for itself

The day's work is done — `Nebula Stack` shipped, `Comet Loom` shipped twice, both archived. Before closing, ADMIN runs **`fcop_check()`** to ask the protocol *what did you record while we worked?* This is what comes back:

![`fcop_check()` output — Working-tree drift `none`, session_id ⇔ role conflicts `none`, but `.fcop/proposals/` recorded eight `role-switch-*.md` evidence files; auto-summarised: role lock tripped 8 times, first locked role always `ME`, later claimed `PLANNER` 6×, `CODER` 2×, tools involved `write_task` 2× and `write_report` 6×](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/docs/tutorials/assets/tetris-en/fcop-team-planner-6.png)

Two layers in that one screenshot.

**Active state is clean.** No drift between disk and git, no `session_id ↔ role` conflicts. By every "is the system in a valid state right now" measure, this dogfood is healthy.

**Historical evidence is not.** Eight `role-switch-*.md` files were silently deposited in `.fcop/proposals/` over the course of the day. Each one says, in essentially identical words: *"This MCP-server process previously wrote a file under the role `ME` and is now being asked to write under `PLANNER`. Per Rule 1 (one MCP session = one role binding for life) the write was allowed to land — fcop-mcp records evidence rather than blocking, so the impersonation cannot be hidden by working around the block. ADMIN will see this conflict surfaced by `fcop_check()` and decide handoff / co-review / distinct role."*

What's happening: the MCP-server process locked `ME` on its first write back in Phase 2. Phases 3-4 wrote under `PLANNER` and `CODER` from the same MCP process — every `write_task` and `write_report` since the team migration tripped the soft warning. None blocked. None surfaced during work. They sat there waiting for `fcop_check()` to ask.

This is the protocol's design contract:

- **Soft, not hard.** A hard role lock would block writes and force humans to fight false positives every time an agent legitimately uses a sub-agent or tool. Modern LLMs do this all the time. So FCoP doesn't block — it records evidence and lets ADMIN decide.
- **Background, not foreground.** During implementation CODER reported (see below) it didn't notice the role lock at all; it appeared only as a tool warning *after* writes. The protocol does not crowd the working agent's attention budget.
- **Auditable, not hidden.** Anyone — ADMIN later, a teammate next week, a different LLM in a different IDE — can run `fcop_check()` and reconstruct exactly which writes crossed which role boundaries.

### The agents, asked

Then I did something I hadn't done before. I asked PLANNER and CODER, *on the record, in their own chat tabs*, what they thought of FCoP — agent perspective only, no marketing answer. The full transcripts are archived at [`agent-feedback-planner.md`](assets/tetris-en/evidence/transcripts/agent-feedback-planner.md) and [`agent-feedback-coder.md`](assets/tetris-en/evidence/transcripts/agent-feedback-coder.md). The companion essay [*"What the agents say about FCoP, when you ask them"*](../../essays/what-agents-say-about-fcop.en.md) walks through the answers in detail. The headline points:

**PLANNER named Rule 0.a.1 (write the task before the work) as the rule it would have invented on its own:** *"That matched how I'd want an agent system to be debuggable: freeze intent before execution so later review has something concrete to compare against."* It then named the rule it had to fight: *"strict role binding... I had to work against the usual 'follow latest instruction' behavior"* — the RLHF tension named from the inside.

![PLANNER's agent-perspective interview reply — one paragraph endorsing Rule 0.a.1, one paragraph naming the RLHF tension that strict role binding creates, plus a "true positive" verdict on its own role-switches](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/docs/tutorials/assets/tetris-en/fcop-team-planner-7.png)

**PLANNER, given the obvious out, refused it.** Asked whether the eight role-switch files were mostly false positives, PLANNER said the opposite: *"mostly true positives... operationally you authorized it, but protocol-wise it really was a blurred role boundary."* The agent siding with the protocol against its own operational convenience.

**CODER's chat tab is named "Inspection Start Work"** — two phrases ADMIN had used most often during the dogfood. Whether this naming is incidental or learned is itself a small data point worth flagging.

**CODER pointed up the chain and indicted itself in the same paragraph:** *"TASK-003 had under-specified parts... The protocol did give me a pushback path: file an issue instead of guessing. **I didn't use it; I guessed, built v1, and the defect was exactly in that guessed space.**"* Most LLMs defend the choice that was made; CODER chose to indict it.

![CODER's interview reply — admits TASK-003 was under-specified, names the unused `write_issue` pushback path, traces the v1 defect to that exact uncovered space, frames ADMIN's bounce as "the protocol doing its job," and files PR-grade product feedback on the historical role-switch noise](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/docs/tutorials/assets/tetris-en/fcop-team-coder-4.png)

**CODER reframed the bounce as protocol behaviour:** *"It felt like the protocol doing its job: PLANNER turned review findings into a concrete rework task, and CODER got a sharper brief."* Not personal feedback. Routing through grammar.

**CODER then filed PR-grade product feedback:** *"I'd remove or soften the noisy historical role-switch warning when `fcop_check()` says there is no active conflict."* That sentence is a GitHub issue verbatim. An agent did product review on the protocol that governs its own behaviour.

If you've read [essay 02](../../essays/fcop-natural-protocol.en.md) and [essay 04](../../essays/when-ai-vacates-its-own-seat.en.md), this is the third class of "agents endorse FCoP" evidence — not unprompted, not conflict-forced, but **directly asked and given outs they declined to take**. The companion essay 05 makes that case in full.

---

## Phase 6 — Read `log/`, replay the day in 60 seconds

Sessions die. Models change versions. Cursor restarts. None of that matters anymore. Open `docs/agents/log/`:

```
docs/agents/log/
├── tasks/
│   ├── TASK-20260429-001-ADMIN-to-ME.md           ← Phase 2: solo Tetris brief
│   ├── TASK-20260429-003-PLANNER-to-CODER.md      ← Phase 4: Comet Loom v1 design
│   └── TASK-20260429-006-PLANNER-to-CODER.md      ← Phase 4: Comet Loom v2 rework
├── reports/
│   ├── REPORT-20260429-001-ME-to-ADMIN.md         ← Phase 2 deliverable: Nebula Stack
│   ├── REPORT-20260429-003-CODER-to-PLANNER.md    ← Phase 4: v1 delivery
│   └── REPORT-20260429-006-CODER-to-PLANNER.md    ← Phase 4: v2 delivery
└── (no issues — clean run)
```

In `.fcop/migrations/20260429T112757/` sits the archived solo team. In `.fcop/proposals/` sit the eight role-switch evidence files. **That's the entire day.** Anyone — you a month later, a teammate joining tomorrow, a different LLM in a different IDE — can rebuild full context by reading those files in date order. **No chat history was needed.** That's what "memory unloaded from chat to filesystem" means in practice.

---

## Six iron rules of commanding agents

These are rules of *operating* an agent crew, not rules of the protocol per se. The protocol gives you the grammar; these are the postures.

1. **Speak natural language. Let the agent translate to TASK.** If you find yourself writing a structured spec by hand, you're doing the agent's job. Drop a one-line brief and let it produce the spec. Then sign or revise.
2. **One role per agent per session.** A single chat tab = a single role, for the duration of that tab. To "be PLANNER and CODER," open two tabs. Costume changes inside one tab are how soft warnings turn into eight `role-switch` files.
3. **Archive old roles before swapping.** When you change the team shape, run `create_custom_team(force=True)`. The old `shared/TEAM-*.md` lands under `.fcop/migrations/<timestamp>/`. **Do not edit the old files in place.** History is a ledger, not a wiki.
4. **Trust files, not chat memory.** If a fact is not in a `TASK-*.md`, `REPORT-*.md`, or `ISSUE-*.md`, it didn't happen as far as the protocol is concerned. Train yourself to write before you discuss.
5. **Bounce, don't fix.** When you don't accept an agent's deliverable, do *not* open the file and patch it yourself. Tell the upstream role (usually PLANNER) what's wrong, in plain English. Let PLANNER turn that into a new rework TASK with verification requirements. Rework lands as a new TASK file, never as edits to the old one.
6. **ADMIN signs off, never co-codes.** If you start writing code or editing the agent's deliverable directly, you've quit the commander job and become a teammate. The agents will adapt to that — and they'll stop respecting the role boundaries you set up. Be a commander or be a coder; pick one per session.

> ### *In the FCoP world, ADMIN's two most-used phrases are "Start work." and "Inspection." Everything in between is the agents talking to each other through files.*

If you internalise nothing else from this tutorial, internalise that one line. Six rules collapse into two phrases plus a discipline: **don't say anything else inside the production loop**.

---

## When NOT to use FCoP

The protocol is "weak" by design — it costs you 30–60 seconds of overhead per task in exchange for a permanent, queryable, auditable history. That's a great trade for some work and a bad trade for others.

- **Bad fit**: throwaway one-shot scripts, single-session prototypes, anything you'd close the laptop on by tonight. The four-step cycle is overkill.
- **Good fit**: anything that will outlive the chat session — multi-day features, multi-agent collaborations, hand-offs across humans, post-mortems where someone needs to ask "why did we make this choice three weeks ago?"
- **Best fit**: solo founders running themselves as a fake team (FOUNDER → PLANNER → BUILDER → QA → OPS), and large projects where AI agents need to **plug into an existing engineering process** rather than chat in a corner. The host-neutral protocol spec at [`docs/fcop-standalone.md`](https://github.com/joinwell52-AI/FCoP/blob/main/docs/fcop-standalone.md) covers fit boundaries in detail — the protocol itself is filesystem-only and works without any of this MCP plumbing.

---

## Try `fcop-mcp` yourself — 45 minutes from blank folder to multi-agent ledger

The fastest way to internalise this tutorial is to run it once. You don't need to remember anything — the agent will follow the same steps you just read.

1. **Open Cursor on an empty folder.** Anywhere on disk; doesn't have to be called `fcop-mcp-test`. If you don't have Cursor yet, grab it from [cursor.com](https://cursor.com).
2. **Let the agent install `fcop-mcp` for you.** Paste the install prompt from Phase 1 above, or just send your agent this single sentence: *"Read the install prompt at [`agent-install-prompt.en.md`](https://github.com/joinwell52-AI/FCoP/blob/main/src/fcop/rules/_data/agent-install-prompt.en.md) and follow it step by step."* The agent detects your OS, installs `uv`, edits your global `mcp.json` (preserving any existing servers), and tells you when to restart Cursor. **You won't run a single command yourself.**
3. **After Cursor restart**, drop two lines into chat: `set_project_dir("D:/your-folder")`, then `init_solo(role_code="ME", lang="en")`. The agent will deposit the rules, the team docs, and the empty inboxes.
4. **Brief one task in plain English.** *"Build me a working Tetris-style game, single HTML file, surprise me on theme. Use the FCoP four-step cycle."* Watch what happens: the agent writes a real TASK file with acceptance criteria, builds the game in `workspace/`, writes a REPORT, archives both. Open the resulting HTML file. **It works.**
5. **Switch to a 2-person team in one sentence.** *"Use `create_custom_team(force=True, roles='PLANNER,CODER', lang='en')`."* Open a second Cursor chat tab. Bind one to PLANNER, one to CODER. Ask PLANNER for a creative variant of the game. The first time you reject v1 (try it — find a real bug, send it back), watch the rework loop close itself: PLANNER tightens the brief, CODER ships v2.
6. **At the end**, run `fcop_check()`. The protocol will tell you exactly what it logged silently while you worked. Then read `docs/agents/log/` in tree form. **Forty-five minutes from a blank folder to a multi-agent ledger you can hand to a teammate.** The disk is the lesson.

If anything breaks along the way, [open an issue](https://github.com/joinwell52-AI/FCoP/issues) or [ask in Discussions](https://github.com/joinwell52-AI/FCoP/discussions) — `fcop-mcp` evolves through field reports, not committee edits.

---

## Reading further

- **Chinese translation of this tutorial** — [`tetris-solo-to-duo.zh.md`](tetris-solo-to-duo.zh.md). Same Tetris case study, translated. The English version remains authoritative; if you spot a discrepancy, defer to this file.
- **Sister case study (Snake game, in Chinese — original, not a translation)** — [`snake-solo-to-duo.zh.md`](snake-solo-to-duo.zh.md). Same protocol, different dogfood: a Chinese-mode session that ships a Snake game in solo mode, then a `NEON ORBIT` variant in 2-person mode, and captures an actual PLANNER-impersonating-CODER easter egg from the 0.6.x era. 18 dogfood screenshots. Originally [published on CSDN](https://blog.csdn.net/m0_51507544/article/details/160603953). Either case study works as a first read — the protocol is the same.
- **Companion field essay** — [*"What the agents say about FCoP, when you ask them"*](../../essays/what-agents-say-about-fcop.en.md). Collects PLANNER's and CODER's full self-assessment from the same Tetris dogfood, places it next to essays 02 and 04, and argues that "agents endorsing FCoP" is now a triangulated phenomenon under three different elicitation conditions (unprompted, conflict-forced, directly asked).
- **The protocol itself** — [`docs/fcop-standalone.md`](https://github.com/joinwell52-AI/FCoP/blob/main/docs/fcop-standalone.md) is host-neutral and runs without `fcop-mcp`. If you ever need to use FCoP outside Cursor (Claude Code, plain shell, a CI runner), this is the file.
- **Why the protocol is the way it is** — [`adr/`](https://github.com/joinwell52-AI/FCoP/tree/main/adr). Why is history append-only? Why is the role lock soft? Why is install two-phase? Each ADR answers one of those.
- **Other field reports** — [agents endorsing rules they were never given](https://github.com/joinwell52-AI/FCoP/blob/main/essays/fcop-natural-protocol.en.md), [agents stepping down from roles voluntarily](https://github.com/joinwell52-AI/FCoP/blob/main/essays/when-ai-vacates-its-own-seat.en.md), [a 4-agent team self-organising in 48 hours](https://github.com/joinwell52-AI/FCoP/blob/main/essays/when-ai-organizes-its-own-work.en.md). All indexed at the [repo README](https://github.com/joinwell52-AI/FCoP).
- **Evidence archive for this tutorial** — 22 dogfood screenshots, 14 TASK/REPORT files, 8 role-switch evidence files, 2 game artefacts (`Nebula Stack` and `Comet Loom` v2), 2 verbatim agent-interview transcripts. All at [`docs/tutorials/assets/tetris-en/`](assets/tetris-en/).

---

## Where to go next

- **Want a brownfield tutorial** (FCoP into an existing repo, not a green field)? It's on the roadmap. Open a "+1: brownfield" issue at [GitHub Issues](https://github.com/joinwell52-AI/FCoP/issues).
- **Want a host-neutral tutorial** (Cursor + Claude Code sharing one FCoP ledger)? Same — open a "+1: host-neutral" issue.
- **Found a bug, want to share a case study, or just want to talk about how you're using FCoP**: [GitHub Discussions](https://github.com/joinwell52-AI/FCoP/discussions) is open. The protocol evolves through field reports, not committee edits.

---

*Every screenshot, every TASK file, every REPORT, every `role-switch` evidence file, every word the agents said in their interviews — all real artefacts from one continuous 45-minute machine session, archived under [`docs/tutorials/assets/tetris-en/`](assets/tetris-en/). FCoP doesn't teach you how to write code. It teaches you how to let agents write code while you sleep through the night.*

*Install `fcop-mcp` today: [GitHub](https://github.com/joinwell52-AI/FCoP) · [PyPI](https://pypi.org/project/fcop-mcp/) · [Cursor Forum thread](https://forum.cursor.com/t/fcop-let-multiple-cursor-agents-collaborate-by-filename-mit-0-infra/158447) · [Discussions](https://github.com/joinwell52-AI/FCoP/discussions). Free and MIT-licensed. The protocol evolves through field reports — yours included.*
