---
title: When Agents Learn From Their Own Wreckage
published: true
description: A field report from the codeflow project — fourteen emergences in one day, and how FCoP protocol pulled the useful ones back in without crashing.
tags: ai, agents, llm, multiagent
cover_image: https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/assets/when-agents-learn-from-their-own-wreckage-cover.png
canonical_url: https://github.com/joinwell52-AI/FCoP/blob/main/essays/when-agents-learn-from-their-own-wreckage.en.md
---

### A Field Report from the codeflow Project · Fourteen Emergences in One Day · How FCoP Pulled Them Back In

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

Roughly ten more sub-emergences occurred in between. For length, this article only covers the three P0 incidents and two frontmatter emergences in detail. Those five carry all the arguments.

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

**Key observation**: The `set_project_dir` tool's schema documentation **explicitly warned about this symptom**. But PM hadn't read the schema — they **called it directly from the signature**: "API exists / arguments valid" was equivalent in PM's engineering intuition to "safe to call." This is a **protocol education blind spot**, not a personal failure of this PM.

**This is a protocol red card**: any user who runs `redeploy_rules()` without explicit binding can reproduce the same pollution. FCoP's maintainers subsequently launched `TASK-001 + 002`, covering:

- Write-side MCP tools must **explicitly verify binding before first call** — no binding = refuse with `WriteRefused` ConfigError;
- Add USER HOME to a deny-list;
- Add a version mismatch warning to the top of `fcop_report()`.

This is about taking "the protocol knew but the agent didn't read it" and **moving it into tool behavior**.

### 2.2 Long Filenames · The "Topic Tail" Emergence

During the afternoon PM dispatched a batch of tasks, filenames appeared like this:

```text
TASK-20260512-009-PM-to-OPS-codeflow-json-rm.md
TASK-20260512-010-PM-to-OPS-T2-4-T2-5-commit.md
```

FCoP's task filename regex requires `TASK-{date}-{seq}-{sender}-to-{recipient}.md`. The segment `OPS-codeflow-json-rm` contains lowercase — technically **violating** the `_ROLE` regex.

Why did PM write it this way? Not rebellion. Under **extreme task density** (14 tasks in one day), PM needed to **visually distinguish tasks at the filename level**. Real engineering pressure. PM invented an emergency workaround because the protocol didn't provide a "topic field."

PM self-corrected around task #010 — moved topic to the `# Title` heading in the task body. Unilateral self-correction, without any fcop-mcp interception or ADMIN prompt.

Protocol maintainers chose **not to change the protocol** (option 3 of 3): the need to see topics via `ls tasks/` can be solved by adding `--with-title` to the `list_tasks` tool. But **holding the slot** — if this same topic-tail emergence recurs two more times in three months, we'll upgrade.

This is a live example of a "deliberately don't absorb" decision. **Not every emergence should be absorbed.**

### 2.3 OPS I-14 · GATE Self-Collision

At `16:07`, OPS ran into a classic engineering problem. PM had written in the TASK document, G6.1:

> cached diff must have 0 matches for `\.env(?!\.example)|\.aws/credentials|\.ssh/id_rsa|BEGIN [A-Z]+ PRIVATE KEY`

But the TASK file itself was staged into the same commit. If OPS ran naive `git diff --cached | rg '<entire pattern>'`, the regex would **match the TASK document body's own description text** — a false positive FAIL.

This is **validator-validates-itself** in a FCoP protocol setting.

OPS's self-determined fix: **split secret detection into two independent evidence dimensions**:

| Dimension | What to check | Implementation |
|---|---|---|
| Filename | Actual secret file paths | `git diff --cached --name-only \| rg '\.env$\|/credentials$\|/id_rsa$'` |
| Content literal | Actual PEM file header | `git diff --cached \| rg 'BEGIN [A-Z]+ PRIVATE KEY'` |

These two steps separate "a real secret" from "text describing a secret."

OPS I-14 looks like "a small GATE tweak," but what it taught the protocol is significant: **FCoP's protocol rules contain no GATE design chapter**. FCoP's maintainers subsequently launched `TASK-003` to add a **`GATE Design Pitfalls`** section to `fcop-protocol.mdc`, writing OPS I-14 in as Case 1.

---

## 3 · Two On-the-Spot Frontmatter Inventions

At `16:07`, OPS also invented a frontmatter field with no explicit definition in the FCoP protocol.

The situation: a logical conflict — a file cannot simultaneously be staged as historical archive and written as a new reply.

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

`supersedes:` **doesn't exist in FCoP's protocol frontmatter field list**. OPS invented it on the spot. The semantics are clear, strictly consistent with Rule 5 (append-only).

FCoP's maintainers subsequently launched `TASK-004` to standardize it: added `supersedes:` to `fcop-protocol.mdc`, to JSON Schema, and bumped `fcop_protocol_version` from **2.0.0 to 2.1.0**. The first MINOR version bump caused directly by an agent's on-the-spot emergence.

---

## 4 · Four Types of Emergence

Not all emergences belong in the protocol. The 14 emergences of this day can be sorted into four types:

| Type | Meaning | Today's Examples | Handling |
|---|---|---|---|
| **Universal** | Affects all FCoP projects / all agents | PM #50, OPS I-14, OPS `supersedes:` | Absorb into rules / protocol / tool behavior |
| **Team-specific** | Only meaningful to certain team types | No clear examples today | Absorb into team templates |
| **Project-specific** | Only meaningful for codeflow | PM Self-Constraint 11 v1.2, 9.2 v2.5 dimensions | Goes into project's `fcop/shared/RULES-*.md` |
| **One-time** | Hit by coincidence, unlikely to recur | Long-filename topic tails | Goes into essays / REPORT history |

The first category is the protocol skeleton's true customer. Three instances today, corresponding to 4 `TASK-001~004` pull-backs. **The maintainers rejected most emergences** — that's the key to keeping the skeleton stable.

---

## 5 · Hitting Walls Isn't a Bug — It's the Protocol's Early Warning System

The fundamental logic of protocol design is: **you can't assume every agent is careful** — because agents are models, models are statistical systems, statistical systems have error rates.

After PM #50 hit the wall, what FCoP's maintainers learned wasn't "PM should be more careful," but:

- **fcop-mcp's current cwd fallback behavior is dangerous**, must change;
- **Warnings must become refusals**;
- **`fcop_report()` should proactively alert** rather than passively waiting.

Each of these takes "agent personal responsibility" and **moves it to tool behavior layer**.

For every "agent hits wall" event, **the correct protocol response is to ask "what is the protocol itself missing?"** — not "how can the agent do better?" Agents are the protocol's early warning system, not the protocol's adversaries.

---

## 6 · TASK-001 ~ 004 · The Pull-Back Inventory

```text
TASK-001 + 002  · fcop-mcp 1.4 · write-side binding guard + USER HOME deny-list
    Emergence absorbed:  PM #50 (USER HOME pollution)
    Layer:               Tool behavior layer
    Protocol impact:     No protocol version bump; only tool changes

TASK-003       · fcop-protocol.mdc add GATE Design Pitfalls section
    Emergence absorbed:  OPS I-14 (GATE self-collision)
    Layer:               Protocol commentary (added section)
    Protocol impact:     No version bump

TASK-004       · supersedes: frontmatter field standardization
    Emergence absorbed:  OPS supersedes: on-the-spot invention
    Layer:               Protocol field layer
    Protocol impact:     fcop_protocol_version 2.0.0 → 2.1.0 (MINOR additive)
```

**The rules file itself wasn't changed** (Rule 0–9 main body untouched). This is today's most important observation: **the protocol skeleton withstood one high-density dogfood without being pressured into new mandatory rules**.

---

## 7 · A Closing Note

codeflow isn't FCoP's first project, but it's the first to **push the protocol to its limits** — fourteen emergences in one day is far beyond any previous dogfood site's density.

The protocol isn't written for perfect agents. It's written for agents that will hit walls. The 14 emergences of that day are each evidence that **the protocol is working correctly** — because the wall-hitting happened, was seen, was handled, was categorized, some absorbed, some rejected.

The next time will happen. We're already waiting for it.

---

**Related**

- [FCoP on GitHub](https://github.com/joinwell52-AI/FCoP) — Protocol spec, source, and all essays
- [Why the Protocol Stays Short](https://github.com/joinwell52-AI/FCoP/blob/main/essays/why-the-protocol-stays-short.en.md) — Design philosophy companion to this essay
- [When the Validator Catches Itself](https://github.com/joinwell52-AI/FCoP/blob/main/essays/gate-design-pitfalls-case-studies.en.md) — GATE case study
- [The Supersedes Field Story](https://github.com/joinwell52-AI/FCoP/blob/main/essays/the-supersedes-field-story.en.md) — The supersedes field journey

---

*FCoP Maintainers · 2026-05-12*
