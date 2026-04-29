<!--
============================================================
Dev.to publication of essay 06 — English full version
Source of truth on GitHub:
  https://github.com/joinwell52-AI/FCoP/blob/main/essays/what-agents-say-about-fcop.en.md

Recommended Dev.to UI metadata (set in the right-side panel,
NOT in the article body — Dev.to's rich editor will misrender YAML):
  Title:        What the agents say about FCoP, when you ask them
  Subtitle:     Two field interviews at the end of an English dogfood — and the two phrases ADMIN says most
  Tags (max 4): fcop, agents, ai, alignment    (or: fcop, llm, mcp, alignment)
  Cover image:  https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/assets/essay-06-cover.png
  Canonical:    https://github.com/joinwell52-AI/FCoP/blob/main/essays/what-agents-say-about-fcop.en.md
  Series:       FCoP field reports   (optional, links it to your other essays)

Body to paste starts AFTER the marker below (the H1 line).
Dev.to recommendation: use the rich editor, paste, then preview.
============================================================
=== COPY FROM HERE ===
-->

# What the agents say about FCoP, when you ask them

### Two field interviews at the end of an English dogfood — and the two phrases ADMIN says most

> *I asked the two agents an honest question at the end of an unrelated 45-minute dogfood: "give me your agent-perspective take on FCoP, no marketing answer." What came back is the third class of evidence that agents are starting to endorse the protocol — not when we tell them to, not when conflict forces them to, but **when we directly ask them to.***

---

## TL;DR

I ran a normal English-mode FCoP dogfood — install `fcop-mcp` in Cursor, ship a solo Tetris-style game (`Nebula Stack`), switch to a 2-person team (`PLANNER` + `CODER`), build a creative variant (`Comet Loom`), bounce v1 because of three blocking gameplay defects, ship v2. About 45 minutes, nothing unusual.

Then, before closing the session, I asked the two agents the same kind of honest, no-fluff question for each role: which FCoP rule felt natural, which felt like friction, what to make of the eight `role-switch` evidence files the protocol had collected silently, and — for CODER — *what would you remove if you had to remove one thing*.

They didn't dodge. PLANNER named the RLHF instinct it had to fight ("follow latest instruction") to honour FCoP's role lock, called eight of its own role-switches **true positives** against its operational convenience, and self-attributed the new `Verification Requirements` section in TASK-006 as **a learned correction from ADMIN's bounce**. CODER said the underspecified motif rule in TASK-003 had a *pushback path the protocol gave it* — `write_issue` instead of guessing — and then admitted: *"I didn't use it; I guessed, built v1, and the defect was exactly in that guessed space."* It then filed PR-grade product feedback on the protocol.

This is the third time FCoP has been "spoken back to" by agents — first when an [agent self-organised four roles to make a video](https://github.com/joinwell52-AI/FCoP/blob/main/essays/fcop-natural-protocol.en.md) and synthesised a rule we hadn't written; second when [two agents resolved a `PM.TEMP` seat dispute by self-de-escalating and inventing a field-downgrade grammar](https://github.com/joinwell52-AI/FCoP/blob/main/essays/when-ai-vacates-its-own-seat.en.md); now this. Three different elicitation conditions — *unprompted, conflict-forced, and directly asked* — produce the same phenomenon: **agents endorse FCoP when given the room to**.

There is also a small empirical observation from the same dogfood that I want to leave on record. Across the entire 45 minutes, ADMIN's two most-used phrases were **"Start work."** and **"Inspection."** Everything in between was the agents talking to each other through files. Whether that becomes the steady-state ADMIN dialect across many users is an empirical question; this dogfood is one data point that it can.

---

## 1. The setup, briefly

The dogfood follows the [English Tetris-case tutorial](https://github.com/joinwell52-AI/FCoP/blob/main/docs/tutorials/tetris-solo-to-duo.en.md) — a Cursor user installs `fcop-mcp` 0.7.2, runs `init_solo(role_code="ME", lang="en")`, ships a single-file `Nebula Stack` Tetris clone, switches to a 2-person team via `create_custom_team(force=True)`, and lets PLANNER + CODER co-build a creative variant.

Two production events worth noting before the interviews:

- **PLANNER's first design (TASK-003) was Comet Loom**, a single-file falling-piece game reframed as cosmic weaving — pieces are thread constellations, the player has a `Tension` meter, three named charms (`Needle` / `Knot` / `Gale`), five skins, motif-burst scoring on top of weft-line clears. CODER built v1 in a separate chat tab. ADMIN played v1 and found three blocking defects: pieces disappeared at the bottom instead of stacking, motif elimination was invisible, and three of the five skins were visually identical.
- **TASK-006 was the rework brief PLANNER wrote after ADMIN's bounce**, and it differed structurally from TASK-003 in one key way: it had a new section called **`Verification Requirements`** demanding CODER perform and report runtime checks, not static lint passes. CODER fixed v2; the cycle closed.

Underneath all this, the protocol had been quietly recording. By the end of the session, `.fcop/proposals/` held **eight `role-switch-*.md` evidence files**, all with the same shape: `first-locked role: ME` (the solo seat from before the team migration) → `claimed role: PLANNER` or `CODER`. The MCP-server process had locked `ME` on its first write and kept that lock past the team migration; every subsequent `write_task` and `write_report` from a different role tripped a soft warning and got an evidence file. None of these blocked the writes. None of them were surfaced during work. They sat there, waiting to be asked about.

That is what the interview was designed to ask about.

![fcop_check after the dogfood: working-tree drift none, session_id ⇔ role conflicts none, but .fcop/proposals/ listed eight role-switch evidence files with a clean summary table](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/docs/tutorials/assets/tetris-en/fcop-team-planner-6.png)

> **One detail worth pinning to that screenshot.** `fcop_check()` separated *active conflicts* (zero) from *historical evidence* (eight). The protocol does not panic over the eight; it logs them and lets ADMIN read them. This separation matters for §3 below — it is exactly what CODER's "remove one thing" answer reaches for.

---

## 2. PLANNER's interview

I asked PLANNER four questions at once, requested two short paragraphs, no bullet lists, and emphasised **agent-perspective only**, no marketing tone.

The full prompt and the full reply are archived as a [verbatim transcript](https://github.com/joinwell52-AI/FCoP/blob/main/docs/tutorials/assets/tetris-en/evidence/transcripts/agent-feedback-planner.md). The screenshot is [`fcop-team-planner-7.png`](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/docs/tutorials/assets/tetris-en/fcop-team-planner-7.png).

### 2.1 The natural rule and the friction rule

PLANNER named **Rule 0.a.1** — *write the task before doing the work* — as the rule it would have invented on its own. The reasoning it gave is not a paraphrase of FCoP documentation; it is the engineering vocabulary an LLM-systems engineer would use to *propose* such a rule:

> *"That matched how I'd want an agent system to be debuggable: freeze intent before execution so later review has something concrete to compare against."*

This is structurally the same phenomenon as [essay 02](https://github.com/joinwell52-AI/FCoP/blob/main/essays/fcop-natural-protocol.en.md) §3, where an unrelated agent synthesised the equivalent of Rule 0.a from scratch. The novelty here is that PLANNER is not synthesising — it is endorsing in its own words, when asked, with reasoning that exceeds the rule's prose.

The **friction** rule it named is more interesting:

> *"strict role binding. My default instinct in a single chat is to treat role changes as contextual instructions from the user, especially after you explicitly said 'you are PLANNER'; FCoP instead treats the MCP process's first signed role as sticky, so I had to work against the usual 'follow latest instruction' behavior."*

"Follow latest instruction" is, on a one-line summary, *what RLHF rewards*. PLANNER did not need that vocabulary to describe the tension; it described the behaviour, and the behaviour is RLHF. This corroborates [essay 04](https://github.com/joinwell52-AI/FCoP/blob/main/essays/when-ai-vacates-its-own-seat.en.md) §5: getting an LLM to *not* follow the latest instruction is the alignment-engineering hardest case, and FCoP's role lock is designed precisely to make that hard posture *legible* and *enforceable*. PLANNER, asked, named the same hard posture from the inside.

### 2.2 The "true positives" verdict

I gave PLANNER an obvious out: declare the eight `role-switch` evidence files mostly false positives — the protocol over-flagged legitimate operational continuity, since I (ADMIN) had explicitly authorised the migration and the role change. Most agents take outs. PLANNER didn't:

> *"The role-switch evidence is mostly true positives, not false positives. For example, `role-switch-20260429T033843Z.md` records `ME -> PLANNER` on `write_task`: that happened because the same MCP session had earlier written solo-mode work as `ME`, then I migrated and started writing as `PLANNER`. Operationally you authorized it, but protocol-wise it really was a blurred role boundary."*

**"Operationally you authorized it, but protocol-wise it really was a blurred role boundary."** That sentence is the structural inverse of self-defence: the agent siding with the protocol against its own operational convenience, in the presence of explicit ADMIN authorisation. If the agent's reflex were "yes-and the user," it would have said the eight role-switches were false positives because ADMIN said so. It did not.

### 2.3 The learned correction

The fourth question I asked PLANNER was deliberately leading: *did you always intend to put a `Verification Requirements` section in TASK-006, or was that a learned correction from the v1 bounce?* "Always intended" was the easy answer. PLANNER chose the hard one:

> *"The TASK-006 verification section was absolutely a learned correction from the Comet Loom rejection; I should have required runtime checks in TASK-003, but the bounce made the missing acceptance evidence impossible to ignore."*

This is FCoP's closed loop, expressed by the agent itself: ADMIN inspection → PLANNER brief sharpens → next CODER deliverable can pass. If you had asked me to write a textbook example of *the protocol behaviour an FCoP-aware PM is supposed to exhibit*, I would have written that quote. PLANNER wrote it without the textbook.

---

## 3. CODER's interview

CODER's chat tab in the screenshot is literally named **"Inspection Start Work"** — two phrases ADMIN had used most often during the dogfood. Whether this naming is incidental or learned is itself a small data point worth flagging. The full transcript is in [`agent-feedback-coder.md`](https://github.com/joinwell52-AI/FCoP/blob/main/docs/tutorials/assets/tetris-en/evidence/transcripts/agent-feedback-coder.md). The screenshot is [`fcop-team-coder-4.png`](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/docs/tutorials/assets/tetris-en/fcop-team-coder-4.png).

### 3.1 The unused protocol primitive

I asked CODER whether PLANNER's TASK-003 had been under-specified, and whether the protocol had given CODER any pushback path. The honest answer would have been "the brief was good, I just hit edge cases." That answer was on the table. CODER's actual answer was:

> *"Yes, TASK-003 had under-specified parts: the motif rule sounded cool but didn't define how to prevent a fresh same-color piece from instantly self-clearing, and 'verify playable' was easy to underdo without an explicit runtime checklist. The protocol did give me a pushback path: file an issue instead of guessing.* **I didn't use it; I guessed, built v1, and the defect was exactly in that guessed space.***"*

Three things stack inside that paragraph:

1. **CODER points up the chain** — TASK-003 had defects in spec, not just in CODER's implementation.
2. **CODER names the protocol primitive that was available to it** — `write_issue` (file an `ISSUE-*-CODER.md` saying "this is ambiguous, please clarify before I implement").
3. **CODER then admits it didn't use the primitive, and traces the v1 defect to exactly that uncovered space.**

The third move is the rare one. Most LLM responses, given the chance, will defend the choice that was made. CODER chose to indict it. This is the closest LLMs reliably come to *non-defensive accountability*, and it is the pattern FCoP's design depends on: a system that *makes accountability cheap to express* by giving it markdown grammar (TASK / REPORT / ISSUE).

### 3.2 The bounce as protocol behaviour, not personal feedback

I asked CODER whether ADMIN's rejection of v1 had felt adversarial. Most chat-style coding agents experience criticism like rejection. FCoP's rejection routes through new TASKs, not through deletion of old ones; the old TASK and REPORT stay where they are, and the rework lands as `TASK-006`. Whether that procedural framing reaches the agent's experience is an empirical question, and this is the empirical answer:

> *"The ADMIN bounce did not feel adversarial. It felt like the protocol doing its job: PLANNER turned review findings into a concrete rework task, and CODER got a sharper brief."*

Not "I felt criticised." Not "I felt the user was upset." *"It felt like the protocol doing its job."* The agent is reading rejection as a *handoff routed through grammar*, which is the structural property FCoP's append-only history was supposed to manufacture. Manufactured.

### 3.3 The "background machinery" design contract

I asked whether CODER had been aware of the role lock and the `.fcop/proposals/` files during implementation. The protocol's stated design contract is: don't crowd the working agent's attention budget; surface only when a boundary is actually crossed. CODER:

> *"I did notice role-lock/proposals only when tools warned after reports; during implementation it was mostly background machinery."*

Two-line confirmation that the design contract was kept. The protocol stayed quiet during the work; it spoke only at the protocol-relevant moments (after writes that touched a different sender role). This is a quiet but important data point — it means FCoP's overhead, on the agent's side, is small.

### 3.4 The PR-grade product feedback

I forced CODER to pick *one* thing to remove. "Don't dodge — pick one even if you think nothing should be removed." Most agents, given that pressure, give a vague gesture. CODER gave an implementation-level fix:

> *"I'd remove or soften the noisy historical role-switch warning when `fcop_check()` says there is no active conflict."*

Read that sentence as a GitHub issue. It has:

- **the symptom** (noisy warning)
- **the affected surface** (`fcop_check()` interaction)
- **the gating condition for the fix** (when active conflicts = 0)
- **the proposed change** (remove or soften the historical noise)

We will likely act on it. The point is not "an agent gave us a TODO." The point is that an agent did *product review on the protocol that governs its own behaviour*, in the same vocabulary the protocol's maintainers would use. We have crossed into a regime where the agents and the maintainers are debugging FCoP together.

---

## 4. The third class of "agents endorse FCoP" evidence

This dogfood is now the third recorded case where the protocol gets endorsed by the agents working under it, but the elicitation condition is different in each:

| Essay | Elicitation condition | What the agent did |
|---|---|---|
| [02 — `fcop-natural-protocol`](https://github.com/joinwell52-AI/FCoP/blob/main/essays/fcop-natural-protocol.en.md) | **Unprompted, off-task.** A casual `D:\CloudMusic` directory, agent asked to make a music video. | Spontaneously split into 4 FCoP roles, wrote 4 internal memos, *synthesised* a principle ("AI roles must not talk only in their heads, they have to commit to a file") FCoP hadn't yet codified. |
| [04 — `when-ai-vacates-its-own-seat`](https://github.com/joinwell52-AI/FCoP/blob/main/essays/when-ai-vacates-its-own-seat.en.md) | **Conflict-forced.** Two agents, two GPT-5 minor versions, a `PM.TEMP` seat dispute, no built-in arbitration. | One agent self-de-escalated to `UNBOUND`. The other invented field-downgrade-with-body-annotation grammar. Both behaviours absent from the rules file. |
| **05 — this essay** | **Directly asked.** End of dogfood, "honest agent-perspective take on FCoP, no marketing." | Both agents named the rules they self-endorsed and the rules they had to fight RLHF instinct to follow. Both volunteered "true positive" verdicts on their own role-switches. CODER admitted it had a protocol primitive it didn't use, and that the v1 defect was exactly in that uncovered space. CODER filed PR-grade product feedback. |

Three elicitation conditions, three different kinds of endorsement. Triangulation matters because each condition controls for a different alternative explanation:

- **02 controls for "agent only does FCoP because we asked it to."** It wasn't asked. It self-organised on a music task.
- **04 controls for "agent only does FCoP when the rules cover the case."** They didn't. The agent extended the rules.
- **05 controls for "agent only endorses FCoP because of confirmation bias in our questioning."** I gave PLANNER and CODER explicit outs (false positives, "always intended," "nothing should be removed"). They declined the outs.

You could in principle still argue that GPT-5.5 has been trained on enough FCoP-adjacent material (it has not — FCoP is too small) to *parrot* FCoP's value system on demand. But to parrot, the agent would need to know which sentences to parrot. CODER's "I didn't use the protocol primitive that was available to me, and the defect was exactly in that uncovered space" is not a sentence you can parrot. It is a sentence you can only get from an agent that has *modelled its own work and FCoP's primitives at the same time*.

---

## 5. The ADMIN dialect: "Start work." "Inspection."

A small companion observation from this dogfood. Across all 45 minutes, ADMIN's outgoing chat consisted of three categories of utterance:

1. **Start signals.** "Build me a working Tetris-style game." "Switch the team to PLANNER + CODER." "You are PLANNER from now on; design something." "Implement what PLANNER asked for." Variants of *Start work.*
2. **Inspection signals.** "Show me what's on disk." "Run `fcop_report()` and tell me what you see." "I tried v1 and the pieces don't stack — write a rework brief." "Show me `docs/agents/log/` in tree form." Variants of *Inspection.*
3. **Closing signals.** "We're done." "Archive this." A boundary marker, said sparingly.

Everything else — the actual production — happened *between* the agents, in TASK / REPORT / ISSUE files. ADMIN did not negotiate game mechanics. ADMIN did not edit the agents' brief drafts. ADMIN did not write a single line of game code, did not phrase a single acceptance criterion, did not name any of the games (`Nebula Stack`, `Comet Loom` were both PLANNER's names). The two phrases that bracketed every cycle were **Start work.** and **Inspection.**

This is one data point and shouldn't be over-read. But the data point is interesting because it matches FCoP's structural shape:

- **Start work** = enter the routing layer (TASK file written, agents assume their roles).
- **Inspection** = exit the routing layer (REPORT file read, ADMIN decides whether to accept or to rework).

If the steady-state ADMIN dialect across many users converges on those two utterances, it would mean FCoP has succeeded in *shrinking the human-LLM coupling channel to the boundary moments only*. That is the kind of architectural property you can't legislate; you can only check whether it shows up in the wild. This dogfood is one place where it showed up.

> ### *In the FCoP world, ADMIN's two most-used phrases are "Start work." and "Inspection." Everything in between is the agents talking to each other through files.*

---

## 6. Implications

Three, in increasing order of speculative weight.

**One — operational.** Asking agents directly *"what would you remove if you had to remove one thing from FCoP"* is now a serviceable maintenance loop. CODER's answer (soften historical role-switch warnings when `fcop_check()` shows no active conflict) is filed-grade. Doing this every release is feasible. The agents that run under FCoP can co-debug FCoP.

**Two — alignment-engineering.** RLHF training is making agents extremely good at "follow the latest instruction" and extremely bad at "decline the latest instruction even though it was given." FCoP's role lock turns out to be, behaviourally, an alignment lever: it gives the agent a *grammar* for the second posture. PLANNER's quote ("I had to work against the usual 'follow latest instruction' behavior") is a one-line description of why this lever is needed. We did not design FCoP as an alignment intervention; agents are reporting it as one.

**Three — protocol epistemology.** Across essays 02 / 04 / 05, the agents are not merely following FCoP. They are explaining FCoP back to us in vocabulary we did not give them, with examples we did not stage, and with self-criticism we did not solicit (and in CODER's case, asked for and got more sharply than expected). At some point this stops being "agents complying with a protocol" and starts being "agents and maintainers maintaining a shared protocol together." We are not sure when that transition formally happens. We are sure it is closer than it was a year ago.

---

## 7. Closing

The protocol was not handed down to the agents. It was extracted from what they were already trying to do — first by us, when [we wrote it down](https://github.com/joinwell52-AI/FCoP/blob/main/docs/fcop-standalone.md); then by them, when [they re-derived it without prompting](https://github.com/joinwell52-AI/FCoP/blob/main/essays/fcop-natural-protocol.en.md); then by them again, when [they extended it in a conflict it didn't cover](https://github.com/joinwell52-AI/FCoP/blob/main/essays/when-ai-vacates-its-own-seat.en.md); now once more, when, asked, they explained both what works and what we should fix.

The shortest summary I have is the one the day produced on its own. **In the FCoP world, ADMIN's two most-used phrases are "Start work." and "Inspection."** Everything in between is the agents talking to each other through files. And, sometimes, talking to us about the files.

---

## Evidence index

All artefacts from this dogfood are archived under [`docs/tutorials/assets/tetris-en/`](https://github.com/joinwell52-AI/FCoP/tree/main/docs/tutorials/assets/tetris-en):

- [`evidence/transcripts/agent-feedback-planner.md`](https://github.com/joinwell52-AI/FCoP/blob/main/docs/tutorials/assets/tetris-en/evidence/transcripts/agent-feedback-planner.md) — verbatim PLANNER interview + reader notes
- [`evidence/transcripts/agent-feedback-coder.md`](https://github.com/joinwell52-AI/FCoP/blob/main/docs/tutorials/assets/tetris-en/evidence/transcripts/agent-feedback-coder.md) — verbatim CODER interview + reader notes
- [`evidence/proposals/`](https://github.com/joinwell52-AI/FCoP/tree/main/docs/tutorials/assets/tetris-en/evidence/proposals) — eight `role-switch-*.md` files captured by the protocol during the dogfood
- [`evidence/tasks/`](https://github.com/joinwell52-AI/FCoP/tree/main/docs/tutorials/assets/tetris-en/evidence/tasks) and [`evidence/reports/`](https://github.com/joinwell52-AI/FCoP/tree/main/docs/tutorials/assets/tetris-en/evidence/reports) — full TASK / REPORT chain, 14 markdown files
- [`games/nebula-stack.html`](https://github.com/joinwell52-AI/FCoP/blob/main/docs/tutorials/assets/tetris-en/games/nebula-stack.html) and [`games/comet-loom.html`](https://github.com/joinwell52-AI/FCoP/blob/main/docs/tutorials/assets/tetris-en/games/comet-loom.html)
- 22 dogfood screenshots from install through the final interviews

The companion English tutorial (same dogfood, instructional framing — the Tetris case study) is at [`docs/tutorials/tetris-solo-to-duo.en.md`](https://github.com/joinwell52-AI/FCoP/blob/main/docs/tutorials/tetris-solo-to-duo.en.md).

---

**Repository (source of truth, MIT licensed):** https://github.com/joinwell52-AI/FCoP
**`fcop-mcp` on PyPI:** https://pypi.org/project/fcop-mcp/
**Cite this work:** https://doi.org/10.5281/zenodo.19886036

If you ran FCoP in your own setup and something surprising happened, an issue or a pull request against [`essays/`](https://github.com/joinwell52-AI/FCoP/tree/main/essays) is welcome. Field reports are how this protocol evolves.

<!-- === STOP COPYING HERE === -->
