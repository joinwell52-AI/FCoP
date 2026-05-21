# ADR-0040 · Canonical One-Liner Two-Layer Convention

* **Status**: Accepted (informative · documentation convention)
* **Date**: 2026-05-21
* **Companion**: ADR-0035 (State) · ADR-0036 (Event) · ADR-0038 (Boundary) · ADR-0039 (Freeze Discipline)
* **Replaces canonical**: ~~`file location is truth; everything else is trace.`~~ (v1 canonical, retired to historical record)

---

## 1 · Context

On the same day FCoP 3.0 was sealed (2026-05-21), the maintainer
identified a structural tension in how the protocol describes
itself: the v1 canonical one-liner —

> *file location is truth; everything else is trace.*

— was being asked to serve two incompatible roles at once:

1. **Teaching role** (README, landing page, social posts,
   conference talk): help a reader unfamiliar with FCoP form a
   minimum-viable mental model in under five seconds.
2. **Definition role** (spec, ADR, formal documents): be precise
   enough that an implementer can derive correct behaviour from
   it without consulting prose.

A single sentence cannot do both well:

* For teaching, "*everything else*" is vague — what is "else"?
* For definition, "*location is truth*" misses the protocol-
  externalisation claim (that files themselves *are* the protocol,
  not just where state lives).

The v1 line is good prose. It is also undersized for the load it
was carrying. The fix is not to lengthen it — that would destroy
its mnemonic power. The fix is to **stop asking one line to do
two jobs**.

---

## 2 · Decision

FCoP's self-description is hereby **split into two parallel
canonical layers**. Both are normative-as-documentation; both are
permanent surface; neither is allowed to drift from the other.

### 2.1 · Layer 1 · Cognitive Bootstrap

**Role**: Build the reader's mental model in the shortest possible
time. Suitable for any context where a reader does not yet believe
"there is such a system."

**Audience**: humans encountering FCoP for the first time —
README, landing page, social posts, README of downstream projects,
conference slides, podcast intros, hallway elevator pitch.

**Surface**:

> 中文（authoritative）：
> **文件即协议；位置定义状态；事件记录历史。**
>
> English (authoritative parallel):
> **Files carry protocol. Paths address state. Events replay transitions.**

**Discipline**:

* Three clauses, three semicolons. Symmetric on purpose — the
  rhythm IS the teaching device.
* Each clause stands alone. A reader who only catches one of the
  three still walks away with one true fact about FCoP.
* No technical vocabulary that requires prior FCoP exposure.
* Does not carry compliance weight: an implementation that
  satisfies Layer 2 is conformant even if it does not quote
  Layer 1 anywhere.

### 2.2 · Layer 2 · Semantic Ontology

**Role**: Be precise enough that an agent, engine, or interpreter
can derive correct behaviour from it without reading the rest of
the spec. The formal definition of what the system *is*.

**Audience**: spec readers, ADR readers, implementers, formal-
methods practitioners, anyone building a second implementation.

**Surface**:

> 中文（authoritative）：
> * **文件是协议的外化载体**
> * **位置是状态的地址映射**
> * **事件是状态转移的可重放证据**
>
> English (authoritative parallel):
> * **Files externalize protocol semantics.**
> * **Paths address state.**
> * **Events are replayable evidence of state transitions.**

**Discipline**:

* Each clause maps to exactly one normative section of the spec:
  | clause              | governs              | normative section |
  |---------------------|----------------------|-------------------|
  | files externalize…  | protocol identity    | spec §0           |
  | paths address state | State Layer (Rule A) | spec §1           |
  | events are evidence | Event Layer (Rule E) | spec §2           |
* Compliance-bearing. An implementation MUST satisfy all three.
* Re-derivable: deleting Layer 2 from the spec would not lose
  information that the Rules tables do not also carry, but it
  would lose the compression that lets new readers form the
  whole-system picture from one paragraph.

### 2.3 · Relationship between the two layers

```
Layer 1 (cognitive bootstrap)  is the  shortcut to  Layer 2.
Layer 2 (semantic ontology)    is the  ground for   Layer 1.
```

They are not translations of one another. They are the same fact
at two different abstraction levels:

* Layer 1 says "**files carry protocol**" — Layer 2 says **why**
  ("they externalise the protocol's semantics, no runtime needed").
* Layer 1 says "**paths address state**" — Layer 2 says **how**
  ("path location is the address; the rule is in §1 Rule A").
* Layer 1 says "**events replay transitions**" — Layer 2 says
  **with what guarantee** ("replayable evidence — append-only,
  audit-only, never the source of NOW truth").

### 2.4 · Retirement of the v1 canonical

The v1 line —

> *file location is truth; everything else is trace.*

— is **retired from the active canonical surface**. It is NOT
removed from history: it remains in essays and ADMIN reviews
filed on or before 2026-05-21, because rewriting those documents
would falsify the timestamp on which the protocol was actually
sealed. Specifically:

* `essays/the-day-we-almost-added-custody.{md,en.md}` — unchanged
* `essays/what-five-ai-models-say-about-fcop.md` — unchanged
* `fcop/reviews/REVIEW-20260521-*.md` — unchanged
* `.fcop/proposals/20260521-*.md` — unchanged

The v1 line MAY also continue to appear in the spec as an
**epigraph** (a poetic preface) — but its role there is
ornamental, not definitional. The definitional load now sits on
Layer 1 + Layer 2.

### 2.5 · Editing discipline going forward

To prevent the two-layer convention from collapsing back into a
single line over time, the following rules apply to any future
docs work:

1. **Don't mix layers in one sentence.** A sentence is either
   Layer 1 (teaching) or Layer 2 (definitional). The two layers
   may appear in the same document, but each sentence picks a
   side.
2. **Never alter Layer 1 without ADR amendment.** Its three
   clauses are the protocol's teaching DNA. Improving the rhythm
   is fine; changing what the clauses *mean* is not.
3. **Never alter Layer 2 without satisfying ADR-0039.** Layer 2
   sentences are normative; they fall under the Freeze Discipline.
4. **The English and Chinese versions of each layer are co-
   authoritative.** Neither is a translation of the other.
   Both are designed at the same time, in the same review, and
   amended together or not at all.

---

## 3 · Consequences

### 3.1 · For documentation

* `spec/fcop-3.0-spec.md` §0 grows by two short subsections
  (§0.1 Layer 1 and §0.2 Layer 2). No other normative section
  changes; the Rules tables are unchanged.
* `README.md` / `README.zh.md` headline quote becomes the
  Layer 1 line. The Layer 2 line is linked, not inlined.
* `CHANGELOG.md` [3.0.0] gets a footnote pointing at ADR-0040
  for the explanation of the canonical change.
* `docs/MIGRATION-3.0.md` / `.zh.md` headline quote becomes the
  Layer 1 line.
* GitHub Release v3.0.0 notes are re-edited via
  `gh release edit v3.0.0 --notes-file …` to carry the Layer 1
  line on top.

### 3.2 · For implementations

Zero change. Layer 2 says nothing the Rules tables did not
already say — it just compresses them into three sentences. An
implementation conformant to fcop@3.0.0 before this ADR is still
conformant after it.

### 3.3 · For future ADRs

Future protocol changes (filed under ADR-0039 §5.1 evidence)
SHOULD also state, in their Consequences section, whether they
require an amendment to Layer 2. Most will not. Any that do
must amend Layer 1 and Layer 2 in lockstep, in both languages,
in the same commit.

### 3.4 · For external teachers / writers

Anyone writing about FCoP — blog posts, conference talks, books —
SHOULD use Layer 1 when introducing the protocol and Layer 2 (or
direct citations of the Rules) when defending technical claims
about it. Conflating the two layers in a single sentence is a
documentation smell, not a protocol violation.

---

## 4 · Alternatives considered

* **Keep the v1 single-line canonical and lengthen it.** Would
  destroy the mnemonic property that made it canonical in the
  first place. Rejected.
* **Replace the v1 line with Layer 2 only.** Loses the elevator-
  pitch register. Anyone trying to explain FCoP in one sentence
  to a non-implementer would still re-invent Layer 1 informally
  — better to canonicalise the informal version. Rejected.
* **Replace the v1 line with Layer 1 only.** Loses the formal-
  definition register. Spec readers want compressed truth they
  can derive from, not slogans. Rejected.
* **Make Layer 1 a translation of Layer 2 (or vice-versa).**
  Would mean improving one would automatically degrade the
  other — they have different optimisation targets. Rejected;
  they are deliberately co-authored, not translated.

---

## 5 · Status note · why this ADR exists

ADR-0040 is itself a Freeze-Discipline edge case (per ADR-0039
§2.5): it makes no protocol mechanism change, only a documentation
convention change. Strictly, a commit message could have carried
the same information. It is filed as an ADR because:

* The canonical one-liner is referenced in 15+ files, including
  the GitHub Release notes that external readers see first. A
  convention this load-bearing deserves a citable artifact, not
  a commit hash.
* Future readers asking "why does the spec say the same thing
  twice in §0" need a stable URL to answer that question.
* The two-layer split itself is a transferable insight — other
  filesystem-native protocols (and possibly other ADR-driven
  systems in general) face the same single-line tension. This
  ADR is the most natural place to record the resolution.

It is **not** a protocol-level ADR. It does not add a Rule, change
a Stage, or amend a Boundary clause. The Freeze Discipline holds.

---

*Filed 2026-05-21 · same day as ADR-0039 · the day FCoP learned
to teach itself in two registers at once.*
