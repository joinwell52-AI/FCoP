# Why the Natural Protocol Holds Up: The Ethic FCoP Extracted from TMPA

### Companion essay — one covers *the phenomenon*, this one covers *why it holds up*

> **Companion essay** to [*"An Anomaly I Can't Fully Explain: AI Doesn't
> Just Obey Rules — It Endorses Them"*](fcop-natural-protocol.md) (the
> sister piece is bilingual and leads in Chinese). The sister essay
> documents the **phenomenon**: an agent, in a completely unrelated
> `D:\CloudMusic` video-generation task, spontaneously split itself
> into four roles and wrote four internal memos — then cited a rule that
> did not exist in any of our `.cursor/rules/` files. *This* essay
> answers the question that phenomenon raises: **why does the principle
> that fell out of the agent's pen actually hold up?** The answer is not
> in the agent. It is in what came before FCoP — a specification called
> **TMPA**.

**Author**: CodeFlow team · 2026-04-21
**Keywords**: FCoP, TMPA, multi-role review, AI ethics mandate, natural protocol

---

## TL;DR

- The sister essay captured *that* an agent wrote FCoP's overall
  principle — *"AI agents must not talk only inside their heads — they
  must land it as a file"* — spontaneously during an unrelated task.
  That is the phenomenon.
- This essay answers the next question: **why does it hold up at all?**
- **FCoP is not a protocol we invented. It is the file-coordination
  skeleton extracted from a larger specification called TMPA.** TMPA's
  ethics layer already carries the same rule — *"Multi-role review is
  an AI ethics mandate"* — except TMPA enforces it by running seven AI
  roles against each other, while FCoP compresses it to *"one agent,
  one file."*
- TMPA's own engineering bet is larger: *a plain-text temporal sequence
  can replace traditional distributed coordination* — no queue, no
  database, no RPC, no orchestrator. FCoP takes only the outermost
  layer of that bet: *files are messages, filenames are routing.*
- So "natural protocol" is not romantic language. It means: **FCoP is
  not a lightweight protocol designed in a lab. It is the AI ethics
  mandate from TMPA, projected onto the smallest possible work unit.**
  One agent, one machine — as long as it insists on landing work as a
  file and reading it back, it is already performing multi-role review.
- A file is the physical substrate that lets a "reviewer" role exist
  independently of the "proposer" role. Without a file, so-called
  multi-role self-review is a hallucination in a single voice.

---

## 1. What the sister essay already settled

The sister essay, with raw JSONL transcripts, four screenshots, and the
four `TASK-*.md` memos the agent wrote unprompted, established two things:

1. In a completely unrelated task (a song-to-video job sitting in
   `D:\CloudMusic`, **outside** any CodeFlow project directory), the
   agent spontaneously split itself into four roles — ADMIN / PM / DEV /
   back-to-PM — and wrote four formal memos to itself, *before* it did
   the actual video work.
2. When asked *why*, it cited a rule — *"AI agents must not talk only
   inside their heads — they must land it as a file"* — that **does not
   exist** anywhere in our `.cursor/rules/` files.

The sister essay concluded: this was not parroting. It was
**sublimation** — the agent merged 2-to-8 scattered technical
stipulations across seven rule files, abstracted them, anthropomorphised
them, and compressed the result into a single sentence that could be
pinned to a wall as a creed. We then adopted that sentence in reverse as
FCoP's overall principle.

This essay tells the other half of the story: **the reason that
sublimated sentence *sticks* is not that the agent got lucky. The
sentence was already written, in another form, in a specification that
predates FCoP.**

---

## 2. Where FCoP actually comes from

FCoP is not a protocol that appeared out of thin air. It is the
file-coordination skeleton that was **extracted** from a larger
specification called **TMPA** (Text-Message Multi-AI Parallel
Architecture).

**TMPA** is a multi-AI architecture **specification**. Its core bet, at
the engineering layer, is a big one:

> **A plain-text temporal sequence replaces traditional distributed
> coordination.**
>
> A multi-AI system does not need message queues, databases, RPC, or an
> orchestration engine. A single plain-text message stream sorted by
> timestamp — plus a naming convention for "which message is handled by
> whom" — is enough.

That is TMPA's radical move: taking "multi-AI coordination" and
reducing it, without middleware, to a single text timeline. On top of
that bet, the TMPA spec specialises for **NL2SQL + BI analysis +
knowledge retrieval + autonomous SQL generation** — high-risk paths
where *one hallucinated action is irreversible*. It defines seven fixed
roles:

| Role | Responsibility |
|---|---|
| Dispatcher | Routes user requests to the right expert path |
| Guardian | Safety boundary enforcement |
| Specialist | Domain expert (SQL generation, analysis planning, …) |
| Analyst | Interprets results |
| Auditor | **The reviewer** — audits SQL, audits output, audits hallucination |
| Executor | Actually runs things (async SQL via `aiomysql`, etc.) |
| Conductor | End-to-end orchestration |

The timeline is: **the TMPA spec came first, FCoP came later.** FCoP is
what you get when you extract the "files are messages, filenames are
routing, YAML is metadata" layer from the TMPA spec and **generalise it
for reuse**. It is not an independently designed protocol — it is a
**subset** of the TMPA spec.

The lineage matters. Analogies:

- **Django** is a full web framework; **WSGI** is the reusable protocol
  extracted from it.
- **Kubernetes** is a full container platform; **OCI Runtime Spec** is the
  reusable specification extracted from it.
- **TMPA** is a full multi-AI architecture specification; **FCoP** is the
  reusable protocol extracted from it.

So when FCoP's design choices feel "just right," that is not luck — the
TMPA spec has already validated them under a much larger load.

---

## 3. TMPA's core ethic

The TMPA spec carries a rule written at its ethics layer:

> **Multi-role review is an AI ethics mandate.**
> **No single AI may go from understanding to execution alone — another AI,
> with a different prompt, must review it.**

In the SQL path this rule is non-negotiable: SQL generated by the
Specialist **cannot be committed without passing through the Auditor**.
The reason is stark — SQL execution is irreversible, and one
hallucinated `DELETE` can destroy data.

The seven-role pipeline is not redundancy or defence-in-depth; it is
**mandated multi-role review**, encoded as a spec-level requirement
rather than a nice-to-have. It is not "you should have an Auditor" — it
is "**SQL without an Auditor is not allowed into the system**."

**That is the other identity of the sentence the agent sublimated.** In
TMPA it is an ethics mandate aimed at seven AI roles; in FCoP it is
compressed into a daily directive for any single agent.

---

## 4. The agent's sentence is the minimal rediscovery of that ethic

The agent in the sister essay had never read the TMPA spec. But when it
wrote, in an unrelated thread, *"must not talk only in their heads —
must land it as a file"*, what it actually did was **compress that
spec-level ethic into its smallest viable form**:

| Dimension | TMPA | FCoP |
|---|---|---|
| Multi-role review | Seven AI roles with different prompts, mutually reviewing | One agent is enough — but it *must* split itself into multiple perspectives via files |
| Strength | Hard constraint | Same hard constraint |
| Substrate | Plain-text temporal sequence + naming-convention routing | Markdown files on disk + filename-as-routing |
| Failure mode | Specialist ships SQL past the Auditor → data corrupted | Agent reviews itself in its head → hallucination rationalised as "conclusion" |
| Defence | Seven-role pipeline | Every step landed as a `TASK-*` / `REPORT-*` file |

Both forms carry **the same obligation**; only the density differs:

- TMPA: **"One is not enough; you need seven."**
- FCoP: **"One is enough — but it must use files to split itself."**

So the agent in the sister essay was not imitating a rule it had read.
It was **independently rediscovering, in minimal viable form, a
professional ethic it had never encountered in our workspace but had
encountered countless times in its training distribution.** That is
why the sentence *sticks* — what sticks is not the agent's momentary
insight, it is the weight of the ethic itself.

---

## 5. Why the file is the key

A file is the physical substrate that lets "multi-role review" actually
happen.

- **In your head**: proposer and reviewer share one voice. The "review"
  is just more rationalisation wearing a different hat. You are reviewing
  yourself, but you only have one voice.
- **On disk**: the proposal is externalised into an object that *another
  reading of yourself* can confront cold. When you come back to read
  that file, you are a **new reader** — bringing a new context, new
  concerns, a new critical angle. That reading is when the reviewer is
  actually born.

Without a file, multi-role self-review is a hallucination in a single
voice.

This is also why FCoP can stand on its own once extracted from the TMPA
spec: **TMPA holds the ethic with seven different prompts; FCoP
compresses the same ethic onto a single agent but requires the agent to
split itself using files.** Both hold the same weight; only the density
differs.

---

## 6. What this means for FCoP's positioning

FCoP is not "lightweight protocol design." It is **the AI ethics mandate
projected onto the smallest possible work unit**.

Look back at the sister essay's `D:\CloudMusic` task. Every memo the
agent wrote is a concrete landing of this ethic:

- `TASK-*-ADMIN-to-PM.md` — landing *what I'm asking for* as an object
  a different role can review
- `TASK-*-PM-to-ADMIN.md` — landing *how I understood your request* as
  an object ADMIN can review
- `TASK-*-PM-to-DEV.md` — landing *the execution plan* as an object DEV
  (my next self) can review
- `TASK-*-DEV-to-PM.md` — landing *what I did* as an object PM (my
  earlier self) can cross-check

Every `TASK-*.md` is not "a document" — it is an **active split of the
self into a reviewable viewpoint**. Files are not archives; files are
the **physical condition that lets the reviewer role exist
independently of the proposer role**.

This is also why FCoP's optional toolbox (the MCP reference
implementation) includes *safety-fuse wrenches* — most notably
`drop_suggestion`:

- The tool itself does nothing "useful."
- Its entire value is to **stop an agent from quietly editing the
  global rules file** when it disagrees with the protocol.
- Agent disagrees? Call the tool. The disagreement lands as a file.
  Work continues.
- This is the overall principle ("must not talk only in your head")
  applied specifically to the agent–protocol relationship.

---

## 7. One-line close

- TMPA holds *"multi-role review is an AI ethics mandate"* by running
  seven AI roles against each other.
- FCoP compresses the same ethic down to *"one agent, one file."*
- The agent in the sister essay rediscovered that ethic in its minimal
  viable form, without ever having read TMPA.
- **The reason the principle feels "natural" is not that it fell from
  the sky — it is that it has been written into the deepest layer of
  multi-AI engineering for a while, and was only now surfaced to the
  top by a single agent's hand.**

This is what the two essays say together: the *phenomenon* is that an
agent wrote the principle itself; the *reason* is that the principle
was already there.

---

## Related

- Sister essay · [*An Anomaly I Can't Fully Explain: AI Doesn't Just
  Obey Rules — It Endorses Them*](fcop-natural-protocol.md) *(bilingual,
  Chinese leading)*
- FCoP spec · [`codeflow-core.mdc`](../spec/codeflow-core.mdc)
- Field report · [*When AI Organizes Its Own Work*](when-ai-organizes-its-own-work.en.md)
- [Chinese version / 中文版本](fcop-tmpa-lineage.md)

---

**License**: MIT (see `LICENSE` in the repo root)
**Attribution**: The writing of this essay is itself the working style
it describes — an agent surfaced a principle, a human recognised and
recorded it. The final text is edited, signed, and published by the
CodeFlow team.
