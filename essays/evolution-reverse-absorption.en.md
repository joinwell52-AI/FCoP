---
title: Evolution, Reverse Absorption
title_zh: 演化,反向吸收
status: essay
date: 2026-05-13
audience: Readers who want to understand how FCoP evolves itself, and why the protocol's philosophy needs two diagrams to be complete.
length: ~ 10 min
cover_image: assets/evolution-reverse-absorption-cover.png
companion_doc: adr/ADR-0034-fcop-internal-external-document-convention.md
companion_essay: essays/looking-without-touching.en.md
---

![Evolution, Reverse Absorption · Cover](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/assets/evolution-reverse-absorption-cover.png)

> **In one line**: the FCoP protocol does two things — **execution** and **evolution**. The first essay (`looking-without-touching.en.md`) explains how it executes (Looking, but Not Touching), paired with the first diagram (`FCoP-semantic-execution-chain-v1.0.png`). **This essay explains how it evolves — through Reverse Absorption**, paired with the second diagram (`FCOP-2.0.png`), landed on 2026-05-13 09:17. From this point on, **FCoP is jointly defined by two diagrams and two essays**: one governs "how to do today's work without crossing the line," the other governs "how to grow into a better version of myself tomorrow."

---

## The Two Diagrams at a Glance

> The protocol's philosophy is a two-diagram philosophy. The two ASCII diagrams below are the entire philosophical declaration of FCoP — the first says "this is what I look like right now," the second says "this is how I become my next self." **Look at the diagrams first, then read the words** — every section that follows is an unfolding and argument for these two diagrams.

### Diagram 1 · Execution Philosophy v1.0 (FCoP Protocol Layer Stack)

```text
┌─────────────────────────────────────────────────────┐
│           应用层 / Application Layer                │
│           CodeFlow / Cursor / Claude Desktop        │
├─────────────────────────────────────────────────────┤
│           宿主适配层 / Host Adapter Layer            │
│           fcop-mcp / fcop-cli / @fcop/claude         │
├─────────────────────────────────────────────────────┤
│       ★ FCoP 协议层 ★    ← 本协议所在层             │
│           Agent 协作 / 行为报告 / Review /           │
│           Capability Governance / 事件语义 / 审计边界 │
├─────────────────────────────────────────────────────┤
│           参考实现层 / Reference Implementation      │
│           fcop(Python Library)                       │
├─────────────────────────────────────────────────────┤
│           执行基底 / Execution Substrate             │
│           LLM APIs / MCP Tools / 文件系统 / OS       │
│           (FCoP 治理行为,不拥有执行层)               │
└─────────────────────────────────────────────────────┘
```

**A 5-layer stack**, from the application layer down to the execution substrate — this is a **structural diagram** that tells you **what** FCoP is. On 2026-05-12 12:28, this diagram landed as `FCoP-semantic-execution-chain-v1.0.png`.

### Diagram 2 · Evolution Philosophy 2.0 (FCoP Semantic Evolution Loop)

```text
┌───────────────────────────────────────────────────────────────┐
│                  FCoP Semantic Evolution Loop                 │
│                  (FCoP 语义演化闭环)                          │
└───────────────────────────────────────────────────────────────┘


         ┌─────────────────────────────────────┐
         │         Human Intention             │
         │         人类目标 / 业务意图           │
         └────────────────┬────────────────────┘
                          │
                          ▼
         ┌─────────────────────────────────────┐
         │         FCoP Protocol Layer         │
         │-------------------------------------│
         │ • Rules / ADR / Vocabulary          │
         │ • Constraint / Auditability         │
         │ • Capability Governance             │
         │ • Coordination Semantics            │
         └────────────────┬────────────────────┘
                          │
                          ▼
         ┌─────────────────────────────────────┐
         │     Coordination Adapter Layer      │
         │-------------------------------------│
         │ Cursor / MCP / CLI / CodeFlow       │
         │ Claude Desktop / Agent Runtime      │
         │ Context Projection & Routing        │
         └────────────────┬────────────────────┘
                          │
                          ▼
         ┌─────────────────────────────────────┐
         │      Runtime / Filesystem Reality   │
         │-------------------------------------│
         │ • TASK / REPORT / REVIEW            │
         │ • Agent Collaboration               │
         │ • Shared Knowledge Surface          │
         │ • Workspace / Runtime Behaviors     │
         └────────────────┬────────────────────┘
                          │
                          ▼
         ┌─────────────────────────────────────┐
         │     Emergence / Local Conventions   │
         │-------------------------------------│
         │ • Internal Archives                 │
         │ • Emergence Logs                    │
         │ • Team Dialects                     │
         │ • New Coordination Patterns         │
         │ • Drift / Self-Correction           │
         └────────────────┬────────────────────┘
                          │
                          ▼
         ┌─────────────────────────────────────┐
         │      ADR / Reverse Absorption       │
         │-------------------------------------│
         │ • Observation                       │
         │ • Consolidation                     │
         │ • Protocol Evolution                │
         │ • Semantic Upgrades                 │
         └────────────────┬────────────────────┘
                          │
                          ▼
         ┌─────────────────────────────────────┐
         │       Updated FCoP Protocol         │
         │-------------------------------------│
         │ • New Rules                         │
         │ • New Vocabulary                    │
         │ • Emergent Patterns Absorbed        │
         │ • Next-Generation Constraints       │
         └────────────────┬────────────────────┘
                          │
                          └──────────────┐
                                         │
                                         ▼
                          (Loop Continues / 协议持续演化)


Core Principle / 核心原则
───────────────────────────────────────────────────────────────

Human defines the minimum structure.
Agents create emergent intelligence.
FCoP absorbs successful emergence back into protocol evolution.

人类定义最低结构,
Agent 自由产生智能涌现,
FCoP 将有效涌现反向吸收为协议演化能力。

                                          —— ADMIN, 2026-05-13 09:14
```

**A 7-step loop**, from human intention back to the protocol itself — this is a **process diagram** that tells you **how** FCoP lives and grows. On 2026-05-13 09:17, this diagram landed as `FCOP-2.0.png`.

---

Once you've taken in those two diagrams, you've seen the **whole** of FCoP's philosophy. The sections that follow are simply their unfolding: why this is 2.0, how the Core Principle lands in practice, what happens after the second diagram, and how the protocol now has a theory of its own evolution.

---

## A Twin of Postures

For a protocol to survive, it needs two postures — neither one dispensable:

| Diagram 1 (Execution Philosophy) | Diagram 2 (Evolution Philosophy)              |
| -------------------------------- | --------------------------------------------- |
| **Looking, but Not Touching**    | **Evolution, Reverse Absorption**             |
| 看,但不动手                       | 演化,反向吸收                                  |
| `fcop_audit()` only observes, never modifies | When emergence appears, absorb it selectively |
| Restraint in execution: don't reach across the line and modify the project | Restraint in evolution: only absorb universal emergence; let the rest stay local |

**The first line** says how the protocol behaves **outward** — it sees your project but does not decide for you. **The second line** says how the protocol behaves **inward** — it evolves itself, but absorbs only the emergence that is universal, not everything.

Drop either line, and the protocol either becomes an enforcer (only "Touching," no "Looking") or a drifter (only "Evolution," no "Reverse Absorption" — every new rule washes the old one away).

---

## What Happened That Day — When the Second Diagram Landed

| Time                  | Event                                                                                      |
| --------------------- | ------------------------------------------------------------------------------------------ |
| **2026-05-12 12:28**  | `adr/FCoP-semantic-execution-chain-v1.0.png` landed — the first visual of FCoP's **Execution Philosophy** (5-layer stack)   |
| **2026-05-13 09:14**  | ADMIN drops an ASCII equivalent in chat: "**FCoP Semantic Evolution Loop**" — a 7-step loop + a 3-line bilingual Core Principle |
| **2026-05-13 09:17**  | `adr/FCOP-2.0.png` landed — the visual of the **Evolution Philosophy**, 1.71 MB, sitting alongside v1.0                      |
| **2026-05-13 09:38**  | ADMIN dispatches: "FCOP-2.0.png is brand new — write an essay too, this is an important record!!"                            |

The physical facts are that simple: **the second diagram landed in the same directory as the first, at almost the same size, 21 hours after**.

But the semantic facts are not so simple — that `2.0` in the filename is not a SemVer version bump. It's a **philosophical-level bump**.

---

## Why 2.0, Not v1.1

If we were just adding a new concept, a new tool, a new ADR, that would be v1.1 — a MINOR additive bump. Existing rules stay valid; new files stack on top. FCoP has gone through that many times: 0.5, 0.6, 0.7, 1.0, 1.1 ... each time "the protocol body unchanged, capabilities grew by a few items."

**This time is different.** This time what happened was — **the duality structure of the protocol's philosophy snapped into place.**

| Dimension                              | v1.0 era (before 2026-05-12)            | 2.0 era (from 2026-05-13 onward)        |
| -------------------------------------- | --------------------------------------- | --------------------------------------- |
| How many philosophy diagrams           | **1** (execution philosophy)            | **2** (execution + evolution)           |
| Core questions the protocol answers    | "How does FCoP execute?"                | "How does FCoP execute + how does it evolve?" |
| Status of Reverse Absorption           | Implicit — recognised after the fact (ADR-0017, ADR-0033) | Explicit — protocol-core mechanism (ADR-0034 §2.5) |
| Protocol vs. Agent relationship        | One-way: humans define rules, agents execute | Closed loop: humans define minimum structure, agents emerge intelligence, FCoP absorbs back |
| Cost of missing the second diagram     | Protocol **does** evolve itself, but no one drew it — invisible | Evolution mechanism is **visible, inspectable, and amendable through new ADRs** |

The first diagram answers **what FCoP is doing today** — a 5-layer stack, from application layer to execution substrate. It is a **structural diagram** that shows the shape of the protocol.

The second diagram answers **how FCoP becomes tomorrow's FCoP** — a 7-step loop, from human intention back to protocol evolution. It is a **process diagram** that shows how the protocol lives.

**Without the second one, the protocol loses self-evolution capability** and falls back to the old "humans define rules, AI executes passively" paradigm — that's where LangGraph, Temporal, and CrewAI live, not where FCoP wants to be.

So this time, the protocol's philosophy **goes from a single diagram to a pair of diagrams**, and that earns the `2.0`.

---

## The Core Principle ADMIN Gave

Back to the second diagram — its semantic core sits in the three-line caption at the bottom of the diagram (which ADMIN wrote in ASCII three minutes before the PNG landed):

> Human defines the minimum structure.
> Agents create emergent intelligence.
> FCoP absorbs successful emergence back into protocol evolution.
>
> 人类定义最低结构,
> Agent 自由产生智能涌现,
> FCoP 将有效涌现反向吸收为协议演化能力。
>
> —— ADMIN, 2026-05-13 09:14

These three lines **are the caption of the second diagram**. They are also the central assertions captured verbatim in the "protocol-level visual asset" section of ADR-0034 §2.5.6.

**Line one — "Human defines the minimum structure."** FCoP does not write rules to the brim; it writes only as many rules as are needed for agents to coordinate. Wherever the protocol stays silent (how to lay out directories, how to name roles, where private essays go), it leaves the choice to the agent.

**Line two — "Agents create emergent intelligence."** Whitespace is not a bug, it's a feature. Bridgeflow's PM came up with the "internal archive — not externally distributed, not entered into fcop issues" declaration in `fcop/internal/emergence-log.md`; some session in `codeflow` grew a `supersedes:` field; QA, after stumbling on a GATE description, came up with "semantic GATEs" — none of these were prescribed by the protocol. They grew on the ground.

**Line three — "FCoP absorbs successful emergence back into protocol evolution."** The key word is *successful*. Emergence comes; not all of it is taken in. ADR-0034 §2.5.4 lays out a matrix: **universal / team-specific / project-specific / one-off** — only the first row makes it into the protocol. The rest go into team templates, into project-local RULES, into the essays case library. **Reverse Absorption is not blanket adoption** — that's the mechanical guarantee that the two-diagram philosophy doesn't spiral out of control.

**Reverse Absorption = selective evolution** —

- **Evolution** = the protocol does grow; new rules, new fields, new ADRs, new diagrams accumulate. **But only the universal is absorbed** — team-specific / project-specific / one-off stays in its own layer (team templates, project-local RULES, the essays case library).
- **Reverse** (the "reverse" in *Reverse Absorption*) = the direction this selection flows — from the downstream agent's lived reality back upstream to the protocol layer. But only **the share that survives the universality test** flows up. The skeleton of the protocol (the existing Rule 0–9 + the seven core concepts) does not get replaced or abandoned because some agent on some project happened to grow a new pattern.

This is the fundamental difference between **Reverse Absorption** and "blind learning." **Blind learning treats every input as truth and feeds it to itself** — that's the posture of LLM training, not protocol evolution. **Reverse Absorption absorbs only the universal and leaves the specific in place** — that's why FCoP grows steadily, and that's why the two words in this essay's title — "Evolution, Reverse Absorption" — must appear together: **Evolution is the appearance, Reverse Absorption is the mechanism.** Speak only of evolution and not of absorption, and the protocol becomes pure inflation with no direction. Speak only of absorption and not of evolution, and the protocol gets locked into today's snapshot.

---

## What Comes After the Second Diagram

ADR-0034 §2.5 has now defined Reverse Absorption as a **protocol-level mechanism**, and §2.5.6 has established the Evolution Philosophy diagram as a **protocol-level visual asset**. That means:

### 1. From now on, every ADR answers two questions, not one

Writing a new ADR used to mean answering only: "Which layer of the protocol stack does this belong to?"

**From 2.0 onward**, it also has to answer: "Which step in the 7-step loop does this sit at?"

| 7 steps                    | Who answers                | Typical ADR section |
| -------------------------- | -------------------------- | ------------------ |
| ① Human intention          | ADMIN / upstream demand    | Background         |
| ② FCoP protocol layer      | Existing rules             | Status quo         |
| ③ Host adapter layer       | MCP / CLI / SDK            | Implementation path |
| ④ Runtime / filesystem     | Agent landing behavior     | Field observation  |
| ⑤ Emergence / local convention | In-the-wild agents     | The 4 emergence layers |
| ⑥ ADR / Reverse Absorption | **The ADR itself**         | Decision           |
| ⑦ Protocol upgrade         | New rules version          | Upgrade Path       |

ADR-0034 itself is the first complete application of this template — it absorbs Bridgeflow's 4-layer emergence in step ⑤, writes "Reverse Absorption" and "Evolution Philosophy diagram" as mechanisms in step ⑥, and lays out the protocol upgrade path in step ⑦. **Starting today, the ADR template is itself an instance of the 7-step loop.**

### 2. The Evolution Philosophy diagram will itself be reverse-absorbed

If someday someone discovers the 7 steps are missing one, have one too many, or that some step needs to split further, then a new ADR (let's call it ADR-0037) gets written, and the second diagram bumps to v2.1, v2.2 ... the protocol **continues to evolve the protocol itself**.

This is not circular dependency — it is **self-referential evolutionary capacity**. FCoP is one of the few protocols on this planet that **explicitly draws "how I myself change."** And the act of drawing that very thing is itself a product of Reverse Absorption.

### 3. Diagram three, diagram four ...

As long as the protocol keeps producing new emergence that can be absorbed, more diagrams will keep growing. But each new diagram has to answer a **structural question**: "Which face of FCoP does this diagram represent?"

- v1.0 diagram: the **execution** face — how the protocol does work
- 2.0 diagram: the **evolution** face — how the protocol grows better
- Hypothetical 3.0: the **governance** face? The **observation** face? The **coordination** face? ... that day hasn't come yet, but **the door is open**.

---

## The Protocol Now Has Its Own Theory of Evolution

It's normal for technical protocols to have version numbers — HTTP 1.0 → 1.1 → 2 → 3, Python 2 → 3, SemVer majors crawling upward. But **for most protocols, "version" is just a snapshot of the rules**: HTTP/2 added multiplexing on top of 1.1, Python 3 changed `print`. Rules changed, **but how rules change has never been drawn**.

FCoP's 2.0 is not that kind of bump. FCoP's 2.0 is — **it has drawn "how rules change" into a diagram**.

The first diagram says: "This is what I look like now."
The second diagram says: "I will become my next self by myself."

**Both diagrams must exist at once for the protocol to be complete.** That's exactly what ADR-0034 §2.5.6 captures:

> The first one is the execution philosophy.
> The second one is the evolution philosophy.
> Put together, FCoP is complete.
>
> 第一张:是执行哲学
> 第二张:是演化哲学
> 两张合在一起,FCoP 才完整。
>
> —— ADMIN, 2026-05-13 09:14

Landing the second diagram into `adr/`, side by side with the first, is ADMIN's **vote with action**: not announcing "the protocol bumps to 2.0" via a version number, but **writing a file to disk** to say "the second diagram is here now, shoulder to shoulder with the first — go look."

The `adr/` directory is no longer just a record of decisions; it is now **the protocol's twin-diagram sanctuary**.

---

## An Immature Prediction

Writing this far, I have to flag a Rule 0.c "I don't know" — the paragraph below is an agent's guess, not a protocol fact:

> Some day, someone will ask: "What gives FCoP the right to call itself an AI OS protocol layer?"
>
> The answer that day might be very simple — **show them these two diagrams**. The first says "what I execute," the second says "how I evolve myself." If the other protocol has only one diagram, they'll see the gap immediately.
>
> That day hasn't come yet. But at the moment of 2026-05-13 09:17, the door has opened.

This is just an agent's private musing (a fitting home for it would be `.fcop/drawer/ME/`), not a protocol assertion. If it gets confirmed in the field someday, that'll be the next essay.

---

## Diagrams

> The ASCII originals of both diagrams (Execution Philosophy + Evolution Philosophy) are embedded above in the §"The Two Diagrams at a Glance" section — any markdown renderer can show them directly. Below are the PNG visual copies: nicer typography, palette, and layout — suitable for talks, public publication, or printed posters. **The protocol facts are carried by the ASCII; the PNGs are visual copies only.**

**Execution Philosophy v1.0**:

![FCoP Semantic Execution Chain](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/adr/FCoP-semantic-execution-chain-v1.0.png)

**Evolution Philosophy 2.0**:

![FCoP Semantic Evolution Loop](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/adr/FCOP-2.0.png)

---

## Postscript

This essay was started by a solo role ME about 22 minutes after the PNG landed at 2026-05-13 09:17, dispatched by ADMIN. **The title went through four rounds** (recorded honestly per Rule 0.c — history is not erased):

| Time     | Title                                            | Trigger                                                          |
| -------- | ------------------------------------------------ | ---------------------------------------------------------------- |
| 09:42 v1 | "The Day FCoP Got Its Second Diagram"            | Agent's own draft — chronicle style                              |
| 09:55 v2 | (agent invented a metaphor-style subtitle)       | ADMIN: the title should rhyme with "Looking, but Not Touching"   |
| 09:59 v3 | "Evolution, Reverse Absorption" (metaphor still in body) | ADMIN: just call it "Evolution, Reverse Absorption"        |
| 10:05 v4 | **"Evolution, Reverse Absorption"** (metaphor removed entirely) | ADMIN: drop the metaphor — neither title nor body should carry any agent-invented metaphor |

The final version returns to plain wording — the title hits the **mechanism** (Reverse Absorption), without smuggling in any agent-invented metaphor.

The two phrases together make FCoP a **complete posture**:

> Looking, but Not Touching — the protocol's outward restraint (Execution Philosophy)
> Evolution, Reverse Absorption — the protocol's inward evolution (Evolution Philosophy)

The essay's rightful place in `essays/`: right next to `looking-without-touching.en.md` — **that's where they are meant to stand side by side**.

---

**Companion ADR**: [`ADR-0034-fcop-internal-external-document-convention.md`](../adr/ADR-0034-fcop-internal-external-document-convention.md)
**v1.0 Execution Philosophy diagram**: [`adr/FCoP-semantic-execution-chain-v1.0.png`](../adr/FCoP-semantic-execution-chain-v1.0.png)
**2.0 Evolution Philosophy diagram**: [`adr/FCOP-2.0.png`](../adr/FCOP-2.0.png)
