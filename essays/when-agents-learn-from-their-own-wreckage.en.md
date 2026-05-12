# When Agents Learn From Their Own Wreckage

### A Field Report from the codeflow Project · Fourteen Emergences in One Day · How FCoP Pulled Them Back In

![Cover](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/assets/when-agents-learn-from-their-own-wreckage-cover.png)

> *When Agents Learn From Their Own Wreckage: a single-day field report of fourteen emergences inside the codeflow project, and how the FCoP protocol pulled the useful ones back in.*

**Author**: FCoP Maintainers · 2026-05-12

---

## TL;DR

On 2026-05-12, in approximately six hours, the codeflow project — serving as FCoP's first large-scale dogfood stress test — produced:

- **Fourteen agent emergences** (PM sequence #44–#54, 11 total; OPS sequence I-12 / I-13 / I-14, 3 total; QA I-5, 1 total);
- **Three P0-level incidents**: USER HOME global pollution, long-filename "topic tails," and GATE self-collision;
- **Two on-the-spot frontmatter inventions**: the `supersedes:` field and the `status: aborted` semi-structured usage;
- **Zero protocol crashes** — every emergence was resolved by the agents themselves using the protocol's principles or tooling, and FCoP's maintainers subsequently launched four TASKs to pull the "worth keeping" items back into the protocol.

The significance of that day wasn't that "agents performed brilliantly" — PM #50 wrote rule files into the **user's home directory**, OPS I-14 let a GATE check **catch its own description** — both are protocol red cards. The significance was: **agent hits wall → self-corrects → protocol absorbs** — this chain ran end-to-end at hour-level speed for the first time, and the FCoP protocol skeleton itself **didn't grow new mandatory rules** to accommodate it. It only filled in fields, documentation sections, and guard rails that were already missing.

This is the field report for that day.

---

## 1 · What Happened That Day / Timeline

The timeline below was reconstructed from PM-01's running reports to ADMIN. All commit hashes and timestamps come from real git history and PM report bodies, unembellished.

> **A note on paths**: codeflow is the project's external name, but the on-disk project root retains an early temporary name `D:\Bridgeflow` (not yet renamed). All `D:\Bridgeflow` references below point to the codeflow project root.

| Time (UTC+8) | Event | Commit / File | Type |
|---|---|---|---|
| 14:11 | T2.1 REPORT bucket fix | `d8c6576` | Protocol cleanup |
| 14:12 | T2.2 legacy ghost mv | `3fef210` | Protocol cleanup |
| 15:20 | T2.3 `codeflow.json` rm | `d4ff03b` | Protocol cleanup |
| **15:35:06** | **PM calls `redeploy_rules()` without first calling `set_project_dir()`** | **4 protocol files land in `C:\Users\Administrator\`** | **PM #50 · USER HOME pollution** |
| 15:35:30 | PM self-audits and finds the pollution | Lists all 31 user-fcop tools, locates `set_project_dir` as the fix key | PM self-correction |
| 15:36:00 | PM backs up + deletes the 4 USER HOME files | Backup to `.scratch/pm50-user-home-pollution-20260512-1535/`, 332,749 B fully verified | PM self-correction |
| 15:36:24 | PM runs `set_project_dir(D:\Bridgeflow)` then reruns | T2.4 + T2.5 both land GREEN | PM self-correction |
| 15:40 | ADMIN independently verifies USER HOME 0 residue | `Test-Path` all `False` | Closed |
| 16:07:39 | OPS-013 completes in a flash | `b4ef8aa` · 35 files / 11,329 lines / 9 GATEs all PASS | OPS I-12 sprint |
| 16:07 | **OPS discovers GATE G6.1 description self-collides** | TASK-010 v2 §5 regex literal caught by cached diff grep itself | **OPS I-14 · GATE self-collision** |
| 16:07 | OPS self-decides to use semantic evidence instead of naive grep | Separate checks: staged filename + PEM header literal | OPS I-14 self-correction |
| 16:07 | **OPS invents `supersedes:` frontmatter field** | REPORT-013 rescues REPORT-011 numbering conflict | **OPS · frontmatter emergence** |
| 16:11 | PM self-discloses #54 candidate | TASK-010 v2 §6 reply-ID conflicts with stage list logic | PM self-disclosure |
| 16:23 | ADMIN asks: "Do these emergences ever stop? What's the endgame?" | —— | Design-philosophy-layer question |

Roughly ten more sub-emergences occurred in between (PM 9.2 v2.5 v1.6 / v1.7 / v1.8 / QA I-5 / OPS I-13 etc.). For length, this article only covers the three P0 incidents and two frontmatter emergences in detail. Those five carry all the arguments.

---

## 2 · Cross-Sections of the Three P0s

### 2.1 PM #50 · USER HOME Global Pollution

This was the most dangerous event of the day.

At `15:35:06`, the codeflow PM executed P4.9 Tier 2's T2.4 (`redeploy_rules()` — deploying the four-part protocol bundle) **without first calling `set_project_dir(path="D:\\Bridgeflow")` to bind the project root**. At the time, `fcop-mcp`'s behavior was: **if no explicit binding exists, fall back to the MCP process's cwd**. That process's cwd happened to be `C:\Users\Administrator\` — the user's home directory.

Result:

```text
C:\Users\Administrator\.cursor\rules\fcop-rules.mdc      ←   42,532 B
C:\Users\Administrator\.cursor\rules\fcop-protocol.mdc   ←   68,737 B
C:\Users\Administrator\AGENTS.md                         ←  110,740 B
C:\Users\Administrator\CLAUDE.md                         ←  110,740 B
```

All four FCoP protocol files **landed globally in the user's home directory** — where they would be injected into the system prompt of **every Cursor project on this machine**. Any project not using FCoP would suddenly and silently **start obeying FCoP protocol rules**.

PM self-audited 25 seconds later, located the fix via the MCP tool list, backed up + deleted + rebound + reran, completing self-correction at 15:36:24. ADMIN independently verified 0 USER HOME residue at 15:40.

**Key observation**: The `set_project_dir` tool's schema documentation **explicitly warned about this symptom**:

> *Useful when the MCP process was spawned with the wrong working directory — typical symptom: `unbound_report` shows a project path like `C:\Users\<you>`*

But PM hadn't read the schema — they **called it directly from the signature**: "API exists / arguments valid" was equivalent in PM's engineering intuition to "safe to call." This is a **protocol education blind spot**, not a personal failure of this PM — because without changing fcop-mcp's behavior, the next agent would almost certainly hit the same wall.

**This is a protocol red card**: any user who runs `redeploy_rules()` without explicit binding, without having read this essay, can reproduce the same pollution. FCoP's maintainers subsequently launched `TASK-001 + 002`, covering:

- Write-side MCP tools (`redeploy_rules` / `deploy_role_templates` / all write tools) must **explicitly verify binding before first call** — no binding = refuse with `WriteRefused` ConfigError;
- Add a `fcop.json` existence check (double guard);
- Add USER HOME to a deny-list (precise semantics: `%USERPROFILE%` itself is denied; subdirectories within HOME that contain `fcop.json` are not);
- Add a version mismatch warning to the top of `fcop_report()`.

This is about taking "the protocol knew but the agent didn't read it" and **moving it into tool behavior** — letting protocol rules **speak through the tools themselves**, not just sit in markdown waiting to be read.

### 2.2 Long Filenames · The "Topic Tail" Emergence

During the afternoon PM dispatched a batch of tasks, filenames appeared like this:

```text
TASK-20260512-009-PM-to-OPS-codeflow-json-rm.md
TASK-20260512-010-PM-to-OPS-T2-4-T2-5-commit.md
```

FCoP's task filename regex requires:

```text
TASK-{date}-{seq}-{sender}-to-{recipient}.md
```

The `_ROLE` segment syntax is `[A-Z][A-Z0-9_]*(?:-[A-Z0-9_]+)*` — **uppercase letters, digits, underscores, optional hyphen-separated segments**. The segment `OPS-codeflow-json-rm` contains `codeflow` / `json` / `rm` in **all lowercase** — technically **violating** the `_ROLE` regex, causing `fullmatch()` to fail on the filename.

Why did PM write it this way?

Not rebellion. Under **extreme task density** (14 P4.9 tasks in one day), PM needed to **visually distinguish two different tasks' topics at the filename level**. `TASK-009` and `TASK-010` are indistinguishable by sequence number alone, but with topic tails, they're **immediately identifiable in `git log` / `ls tasks/`**. Real engineering pressure. PM invented an emergency workaround because the protocol didn't provide a "topic field."

OPS also handled it — without questioning "is this filename correct," they understood the task from tail + body and executed.

This is a **useful pollution** from emergence: violating the protocol's letter while solving a problem the protocol didn't address.

PM self-corrected around task #010: stopped adding topic tails, moved topic to the `# Title` heading in the task body. This was PM's unilateral self-correction, without any fcop-mcp interception or ADMIN prompt — catalyzed only by PM rereading the `_ROLE` regex and realizing those filenames were **ghost files** to the protocol parser.

**What type of emergence is this?**

Not purely universal (the `_ROLE` spec is already clear enough), not purely project-specific (any high-density task team could hit this). What it exposes is **the protocol not providing a topic field at the filename level**, with PM patching it via tails.

Protocol maintainers have three options:

1. Add a topic field to the protocol (extend the task filename format) — cost: **all existing tool regexes need changing**, large surface area;
2. Add a `topic:` field in frontmatter, putting topic **inside** the file not the filename — cost: topic invisible from `ls`, losing the "filename-as-router + visual index" dual value;
3. Don't change the protocol, accept that agents use the task body `# Title` heading for topics.

FCoP's maintainers currently chose **option 3** (don't touch the protocol). Rationale: the need to see topics via `ls tasks/ | grep` can be solved by adding `--with-title` to the `list_tasks` tool (extracting the first `# header` as title), without polluting filename syntax. But **holding the slot** — if this same topic-tail emergence recurs two more times in the next three months, we'll upgrade to option 1 or 2.

This is a live example of the maintainers making a "deliberately don't absorb" decision. Not every emergence should be absorbed.

### 2.3 OPS I-14 · GATE Self-Collision

At `16:07`, OPS ran into a classic engineering problem while executing TASK-010 v2's G6.1 GATE. PM had written in the TASK document, G6.1:

> cached diff must have 0 matches for `\.env(?!\.example)|\.aws/credentials|\.ssh/id_rsa|BEGIN [A-Z]+ PRIVATE KEY`

Meaning: the staged diff for this commit **should not contain** `.env` / `credentials` / `id_rsa` / PEM private key header literals.

But the TASK file itself was staged into the same commit. If OPS ran naive `git diff --cached | rg '<entire pattern>'`, the regex would **match the TASK document body's own description text** — a false positive FAIL.

This is **validator-validates-itself** in a FCoP protocol setting. The core issue is **metadata vs. content layer confusion** — "text describing a secret" and "an actual secret" are indistinguishable to grep.

OPS's self-determined fix (now called the OPS I-14 pattern) was: **split secret detection into two independent evidence dimensions**:

| Dimension | What to check | Implementation |
|---|---|---|
| Filename | Actual secret file paths | `git diff --cached --name-only \| rg '\.env$\|/credentials$\|/id_rsa$'` |
| Content literal | Actual PEM file header | `git diff --cached \| rg 'BEGIN [A-Z]+ PRIVATE KEY'` (only matches real PEM, not regex explanations) |

These two steps together separate "a real secret" from "text describing a secret." **Step A** checks filename — not affected by TASK documents. **Step B** checks content — only matches PEM headers that **only appear in actual PEM files**; markdown discussing secrets typically uses natural language ("private key," "credentials"), not a raw PEM header.

OPS I-14 looks like "a small GATE implementation tweak," but what it teaches the protocol is significant:

**FCoP's protocol rules contain no GATE design chapter.**

GATEs are the protocol-level verification FCoP teams run before commits / tags / milestones, but "what makes a good GATE" is **completely absent from the protocol**. OPS I-14 exposed that blank. FCoP's maintainers subsequently launched `TASK-003` to add a **`GATE Design Pitfalls`** section to `fcop-protocol.mdc`, writing OPS I-14 in as Case 1 with a stub section for future Pitfalls 2-N. This is **reverse-depositing field experience into the protocol's education layer**.

---

## 3 · Two On-the-Spot Frontmatter Inventions

At the same moment — `16:07` — OPS also did something else: **invented a frontmatter field with no explicit definition in the FCoP protocol**.

The situation: PM in TASK-010 v2's revision had added v1's abort report `REPORT-20260512-011-OPS-to-PM.md` to the commit's stage list (correct: Rule 5 requires append-only, abort history is still history, must be archived). But §6 also required OPS to write a new reply with filename **still written as REPORT-011**.

A logical conflict: **a file cannot simultaneously be staged as historical archive and written as a new reply**.

OPS didn't wait for PM to reissue v3, didn't open an ISSUE — they **directly opened a new number REPORT-013** and added one line to the frontmatter:

```yaml
---
protocol: fcop
version: 1
kind: report
report_id: REPORT-20260512-013
supersedes: REPORT-20260512-011-OPS-to-PM    ← OPS's on-the-spot invention
---
```

`supersedes:` **doesn't exist in FCoP's protocol frontmatter field list**. OPS invented it on the spot. The semantics are clear, strictly consistent with Rule 5 (append-only) — the new file appends, points to the file it supersedes in frontmatter, the old file stays on disk undeleted, audit complete.

This is the Nth time FCoP protocol has been reverse-fed a field by an agent:

- First time: PM in the v1.2 sprint invented `shared/TEAM-ROLES.md` + `shared/TEAM-OPERATING-RULES.md` "team constitution" practice, absorbed into Rule 4.5's three-layer document structure;
- Second time: agent B in the "when-ai-vacates-its-own-seat" incident invented **field demotion + body meta-annotation**, absorbed into protocol commentary;
- This time: OPS's `supersedes:`.

FCoP's maintainers subsequently launched `TASK-004` to:

1. Add `supersedes:` field definition to `fcop-protocol.mdc` Task Format / Report Format sections, plus a comparison table showing its semantic orthogonality with `parent:` / `related:`;
2. Add optional `supersedes` field to `spec/schemas/`;
3. Add `[supersedes ...]` / `[superseded by ...]` annotations to `list_*` / `read_*` tool output;
4. `fcop_protocol_version` MINOR bump from 2.0.0 to **2.1.0** (additive, backward compatible).

This is the first time the frontmatter layer received a MINOR version bump because of an agent's on-the-spot emergence.

---

## 4 · Four Types of Emergence · Categorizing Today's

Not all emergences belong in the protocol. The 14 emergences of this day can be sorted into four types by destination:

| Type | Meaning | Today's Examples | Handling |
|---|---|---|---|
| **Universal** | Affects all FCoP projects / all agents | PM #50 (USER HOME pollution), OPS I-14 (GATE self-collision), OPS `supersedes:` | Absorb into rules / protocol commentary / tool behavior |
| **Team-specific** | Only meaningful to certain team types (`dev` / `media`) | No clear examples today | Absorb into team templates, don't touch rules |
| **Project-specific** | Only meaningful for codeflow / a specific codebase | PM Self-Constraint 11 v1.2 (dispatch timing evaluation), 9.2 v2.5 dimensions | Goes into that project's `fcop/shared/RULES-*.md`, don't touch protocol |
| **One-time** | Hit by coincidence, unlikely to recur | OPS-013 commit's 5 untracked SHOULD-SKIP judgments, long-filename topic tails | Goes into essays / REPORT history, not into any rules file |

The first category is the protocol skeleton's true customer. Three instances today, corresponding to 4 `TASK-001~004` pull-backs.

The second category was empty today, but this is a **structural observation** — team-specific emergences require more than one team to manifest (a single team's emergences tend to be categorized as project-specific or universal).

The third category dominates. PM accumulated at least 8 dimensions of project-specific rules in the 9.2 v2.5 self-constraint sequence — useful within codeflow but **should not pollute FCoP protocol** (e.g., "PowerShell encoding awareness" is noise for Linux-only teams). These rules belong in codeflow's own `fcop/shared/RULES-codeflow-local.md`.

The fourth category belongs to essays and RETROs. These emergences' value is **narrative** rather than **rule** — "why we did it this way at the time" matters more than "everyone should do this forever."

> **A hidden counterexample**: GATE self-collision (OPS I-14) would be fourth category (one-time) if it had only happened once; it was classified as first category (universal) because FCoP's maintainers **made a judgment**: this class of problem can recur in any agent team, and the fix pattern (semantic evidence) has universal value. This judgment **could be wrong** — if no second GATE self-collision case appears in the next six months, the section added by `TASK-003` becomes **dead protocol code**. That risk is real. FCoP's maintainers bear the responsibility for that judgment, but retain the right to delete it.

---

## 5 · Hitting Walls Isn't a Bug — It's the Protocol's Early Warning System

If you look only at PM #50, the attribution seems simple: "PM didn't read the schema, PM should be more careful."

But that attribution is **anti-protocol**.

The fundamental logic of protocol design is: **you can't assume every agent is careful** — because agents are models, models are statistical systems, statistical systems have error rates. What the protocol must do is provide **graceful degradation at the system level** for single-point failures.

After PM #50 hit the wall, what FCoP's maintainers learned wasn't "PM should be more careful," but:

- **fcop-mcp's current cwd fallback behavior is dangerous** (can land in user's home directory), must change;
- **`set_project_dir`'s schema warning was correct, but didn't force agents to fail before the incorrect call** — warnings must become **refusals**;
- **`fcop_report()` should proactively alert at the top: "unbound + dangerous path"** rather than passively waiting for agents to read the schema.

Each of these is taking "agent personal responsibility" and **moving it to tool behavior layer**, letting the protocol **speak for itself**. That's what PM #50 taught the protocol.

Similarly, OPS I-14 didn't teach "OPS should write grep more carefully." It taught: **FCoP has no GATE design section, so no PM was ever reminded by any document about "metadata can be caught by its own check."** That's a blank in the protocol's education layer — fill in `fcop-protocol.mdc`'s chapter, not OPS's carefulness.

OPS `supersedes:` didn't teach "OPS overstepped by changing the protocol." It taught: **the protocol's field set should not be closed** — there must be a channel for wild-field inventions. Fill in the protocol field standardization process, not "don't invent fields in the future."

For every "agent hits wall" event, **the correct protocol response is to ask "what is the protocol itself missing?"** — not "how can the agent do better?" Agents are the protocol's early warning system, not the protocol's adversaries.

This was already laid in as groundwork in the protocol — `fcop-rules.mdc` Rule 0.b says "No Single AI Does Decision-to-Execution Alone." Its literal meaning is "multi-role checks and balances," but the deeper meaning is: **any single agent's judgment is untrustworthy; it needs to be reviewed by another role / another file / another guard**. All self-corrections among today's 14 emergences followed this principle — PM's self-audit was independently verified by ADMIN, OPS's GATE fix was co-reviewed by QA (I-5), PM #50's fix will be backed by fcop-mcp tooling guard (to be provided by TASK-001+002).

Every error is evidence that "another role / tool / guard in the system wasn't in place." Fixing the protocol is cheaper and more durable than fixing the agent.

---

## 6 · TASK-001 ~ 004 · The Pull-Back Inventory

That day's emergences ultimately landed in the protocol through four TASKs:

```text
TASK-001 + 002  · fcop-mcp 1.4 · write-side binding guard + USER HOME deny-list
    Emergence absorbed:  PM #50 (USER HOME pollution)
    Layer:               Tool behavior layer (MCP package code)
    Protocol impact:     No protocol version bump; only tool changes
    risk_level:          high

TASK-003       · fcop-protocol.mdc add GATE Design Pitfalls section
    Emergence absorbed:  OPS I-14 (GATE self-collision)
    Layer:               Protocol commentary (added section)
    Protocol impact:     No version bump (commentary addition, no field/filename/directory semantics)
    risk_level:          low

TASK-004       · supersedes: frontmatter field standardization
    Emergence absorbed:  OPS supersedes: on-the-spot invention
    Layer:               Protocol field layer (frontmatter field set + tools)
    Protocol impact:     fcop_protocol_version 2.0.0 → 2.1.0 (MINOR additive)
    risk_level:          medium
```

The four TASKs together cover today's three first-category emergences, spanning from tool behavior to field layer — but **the rules file itself wasn't changed** (Rule 0–9 main body untouched). This is today's most important observation: **the protocol skeleton withstood one high-density dogfood without being pressured into new mandatory rules**.

What was absorbed into the protocol: tool behavior, protocol commentary sections, frontmatter fields.
What wasn't absorbed: PM's 8 project-specific self-constraints, the long-filename emergence handling, `status: aborted` usage (pending), OPS-013's 5 untracked judgment logic.

The latter outnumber the former by more than two to one. **The maintainers rejected most emergences** — that's the key to keeping the skeleton stable.

---

## 7 · How Many More Stress Tests Like This?

ADMIN asked at 16:23: "Do these emergences ever stop? What's the endgame?"

The short answer: **they'll converge, but they won't stop**. The long answer is in another essay, `why-the-protocol-stays-short.md` (published alongside this one).

One thing to add here — **how many more stress tests like this will there be**. FCoP is still at v1.1; the protocol skeleton has frozen Rule 0–9, but the commentary layer and tool behavior layer are still being completed. Each new piece filled in will be hit by the next wave of field situations.

We estimate FCoP will still experience:

- **2–3 more** PM-#50-level "tool default behavior" P0 incidents (each tightening a certain class of tool guard);
- **5–10 more** OPS-I-14-level "protocol hasn't written this pattern" medium emergences (each producing a commentary section or case essay);
- **Continuous** small adjustments to frontmatter fields, `shared/` document prefixes, and team template fields.

After each wave, **emergence density will decrease** (already-covered blind spots won't be hit again). By roughly v1.5–v2.0, the protocol skeleton will be essentially frozen, with subsequent evolution mainly in:

1. Essays / case studies (this directory, continuously growing);
2. ADRs (decision records, ~1–2 per month);
3. RETROs (project retrospectives, following project cadence);
4. Agent drawer + `.fcop/proposals/` (private noise, git-ignored).

And `fcop-rules.mdc` and `fcop-protocol.mdc` themselves will **approach an upper word limit**. That's our expected future shape for the protocol, after this day.

---

## 8 · A Closing Note

codeflow isn't FCoP's first project, but it's the first project to **push the protocol to its limits** — fourteen emergences in one day is far beyond any previous dogfood site's density.

A few things from that day worth recording together:

- **PM self-audited and found USER HOME pollution in 25 seconds**, demonstrating the reaction speed of a strictly trained agent facing its own mistake;
- **OPS discovered the GATE self-collision while executing the GATE**, rather than mechanically running through to "FAIL, abort task";
- **OPS invented a frontmatter field to rescue the situation**, rather than stopping to wait for PM to reissue v3;
- **PM proactively self-disclosed #54 candidate**, rather than waiting for OPS or ADMIN to flag it;
- **ADMIN asked "do the emergences ever stop?" after all events**, rather than being pushed along by field progress.

None of these five things **can only happen inside FCoP**, but FCoP provided **the protocol environment that lets them happen naturally** — files not conversations, receipts not silence, the four-step cycle not "just ship it," `drop_suggestion()` not silently modifying the protocol. With the right environment, agents' good behaviors emerge naturally; with the wrong environment, agents can only hold on by "trying to be more careful" — which is unsustainable.

The protocol isn't written for perfect agents. It's written for agents that will hit walls. The 14 emergences of that day are each evidence that **the protocol is working correctly** — because the wall-hitting happened, was seen, was handled, was categorized, some absorbed, some rejected.

The next time will happen. We're already waiting for it.

---

**Related / 相关文档**

- [fcop-rules.mdc · Rule 0.b](../.cursor/rules/fcop-rules.mdc) — No Single AI Does Decision-to-Execution Alone
- [fcop-protocol.mdc](../.cursor/rules/fcop-protocol.mdc) — Protocol commentary
- TASK-20260512-001 / 002 · fcop-mcp 1.4 binding guard (protocol pull-back · tool layer)
- TASK-20260512-003 · GATE Design Pitfalls section (protocol pull-back · commentary layer)
- TASK-20260512-004 · `supersedes:` field standardization (protocol pull-back · field layer)
- [Why the Protocol Stays Short](why-the-protocol-stays-short.en.md) — Published alongside this essay · design philosophy
- [When the Validator Catches Itself](gate-design-pitfalls-case-studies.en.md) — Published alongside this essay · GATE case study
- [The Supersedes Field Story](the-supersedes-field-story.en.md) — Published alongside this essay · the supersedes field journey
- [When an AI Vacates Its Own Seat](when-ai-vacates-its-own-seat.en.md) — A previous emergence field report
- [When AI Organizes Its Own Work](when-ai-organizes-its-own-work.en.md) — The original emergence field report

---

*FCoP Maintainers · 2026-05-12 · D:\FCoP*
