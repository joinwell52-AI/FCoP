# ADR-0039 · FCoP Freeze Discipline & Runtime Absorption Era

* **Status**: Accepted (informative · self-binding)
* **Date**: 2026-05-21
* **Companion documents**: ADR-0035 (State) · ADR-0036 (Event) · ADR-0038 (Boundary) · NOTE-custody-is-not-a-layer

---

## 1 · Context

On 2026-05-21, FCoP 3.0 was sealed:

* ADR-0035 frozen (path = NOW truth, Rules A/B/C)
* ADR-0036 accepted (transitions = PAST trace, Rules E/F/G)
* ADR-0038 accepted (boundary charter, 5-question filter, §5.1 exemption)
* ADR-0037 withdrawn before reaching Accepted (custody as layer rejected; preserved as NOTE)
* `spec/fcop-3.0-spec.md` published as the canonical single-page specification
* `src/fcop/lifecycle/` reference implementation merged with 1174/0 green

At this exact point in the protocol's life, the maintainer made an
explicit declaration:

> **FCoP 3.0 is the end of the protocol-design era.
> From now on, no new protocol mechanism may be added without a
> documented runtime pain point from a real coordination scenario.**

This ADR records that declaration as a binding meta-rule.

It is filed under FCoP's own dogfooded process — proposing a meta-
constraint that limits future ADRs is itself an ADR. After this one
lands, the constraint applies to every subsequent proposal,
including any from the same maintainer.

---

## 2 · Decision

### 2.1 · The Freeze

FCoP enters its **Runtime Absorption Era**. The only legitimate path
for any change to the protocol surface (the State Layer, the Event
Layer, the Boundary Charter, or anything they reference normatively)
is:

```
runtime pressure  →  evidence  →  §5.1 exemption clause  →  protocol absorption
```

In particular, all four of the following are explicitly **forbidden**
as triggers for a new ADR:

* **Pre-emptive design**
  "This will probably be useful one day."
* **Aesthetic extension**
  "It would be more elegant if we also had X."
* **Completeness urge**
  "The protocol feels incomplete without Y."
* **Theoretical purity**
  "If we refactored Z, the model would be cleaner."

If a proposal cannot point to a concrete, reproducible coordination
failure in a real multi-agent runtime, it does not enter the ADR
queue. Period.

### 2.2 · The Permitted Driver

The only permitted reason to amend the protocol is the one already
formalised in ADR-0038 §5.1:

* **E1 · complexity-forced** — 2+ independent projects report the
  same gap inside 6 months
* **E2 · cross-runtime breakdown** — a real coordination scenario
  is demonstrably impossible without the extension (not
  "inconvenient" — *impossible*)
* **E3 · internal contradiction** — existing rules conflict in a
  way that cannot be reconciled

ADR-0039 does not weaken or override §5.1. It *strengthens* it by
removing the implicit fourth lane ("the maintainer felt like it")
that all real-world protocols accidentally leave open.

### 2.3 · The Pre-flight Checklist

Any proposed protocol change MUST pass the following four self-
checks **before** an ADR is drafted. The checklist exists so
proposals fail fast, while the writing energy is still cheap.

1. **Does this come from a runtime?**
   What multi-agent scenario surfaced the need? Which runtime ran
   it (CodeFlowMu / Cursor multi-agent / etc.)? Link the failure.
2. **Did it actually break, or was it just awkward?**
   Awkward maps to L2 tooling or user education, not to protocol.
   Only an inability-to-complete maps to protocol.
3. **Does it pass ADR-0038's 5-question filter?**
   Describe-not-execute · file-contract-not-runtime-state ·
   coordinate-not-orchestrate · host-independent · non-overlapping
   with Temporal / LangGraph / CrewAI. If any question fails →
   reject.
4. **Does it fit one of §5.1 E1/E2/E3?**
   If none — close the proposal, log it as a "not-yet" observation,
   re-evaluate in 6 months.

Only after **all four** pass does an ADR get written.

### 2.4 · The Observation Backlog

Proposals that fail any check above are not deleted. They go into
an **observation backlog**:

```
.fcop/observations/YYYYMMDD-<short-slug>.md
```

Each observation file is a 1-page note:

* What was tried
* What felt awkward or insufficient
* Why it does NOT yet qualify as runtime pressure
* When to re-evaluate (date or event trigger)

The backlog is the protocol's working memory between absorption
cycles. Re-reading it in 6 months — after another 6 months of
runtime evidence — is the primary §5.1 re-evaluation mechanism.

### 2.5 · Specifically Permitted, Specifically Forbidden

To make the discipline operational instead of philosophical:

**Permitted without an ADR**:

* Reference-implementation bug fixes (`src/fcop/`)
* Reference-implementation performance work
* MCP-tool surface refinements that preserve the public schema
* Documentation, examples, tutorials, essays
* Tool-tier reclassification within §8 (informative)
* New language bindings of the existing protocol
* CI / packaging / release infrastructure

**Forbidden without §5.1 evidence + an ADR**:

* New stages, or new edges in the 7-row allowed-transitions table
* New `transitions:` schema fields beyond optional `note` /
  `supersedes` / forward-compat `extra` bag
* New layers (custody-style, role-style, plan-style, etc.)
* New required frontmatter fields
* Any change to Rules A / B / C / E / F / G
* Any change to the Boundary Charter

This list is **exhaustive at the time of writing**. Items can move
between the two columns only through this ADR's amendment process
(itself bound by §5.1).

### 2.6 · The Immunity Record

ADR-0039 also serves as the public memory of the immune event that
motivated it. On the same day the protocol was sealed, the
maintainer drafted ADR-0037 (Custody Layer) — a feature that
"looked reasonable" — and the protocol rejected it before it
reached Accepted because:

* It violated Rule A (would have introduced a second source of NOW
  truth alongside file location)
* It violated Rule G (would have invited derivation of current
  state from stored ownership data)
* It failed ADR-0038 question 2 (would have made FCoP own runtime
  state instead of describing a file contract)

That rejection is recorded in:

* `adr/NOTE-custody-is-not-a-layer.md` (the formal demotion)
* `essays/the-day-we-almost-added-custody.md` (the field report)
* `.fcop/proposals/20260521-rfc-semantic-collapse-and-custody-rejection.md`
  (the decision chain)

ADR-0039 closes the loop: the discipline that produced that
rejection is now itself the discipline that governs future
proposals.

---

## 3 · Consequences

### 3.1 · For maintainers

* Drafting energy shifts from "designing more protocol" to "running
  CodeFlowMu (and any subsequent real runtime) hard enough to
  generate genuine pressure."
* The default answer to any new architectural temptation becomes
  "log it in `.fcop/observations/`, come back in 6 months."
* The 6-month cadence is not a hard rule — re-evaluation can
  happen sooner if E1/E2/E3 evidence arrives — it is the default
  patience window.

### 3.2 · For external implementers

* The protocol surface is stable, with semver guarantees against
  `fcop 3.x`. Any change rebrands a release as `4.0`.
* Tool tier classification (§8 of the spec) remains informative
  and may evolve within 3.x without re-validating implementations.
* Bug-fix releases (`3.0.x`) carry no protocol semantics; any
  apparent semantic change is itself a bug.

### 3.3 · For the protocol itself

* FCoP joins the small group of protocols (TCP, POSIX, OCI image
  spec, Git plumbing surface) that have made it past the
  "kindly extended to death" trap. Not because nobody has good
  ideas — because the protocol now refuses the ones it does not
  need.

### 3.4 · For ADR-0040 and beyond

* The next ADR may not appear for months. That is the expected
  outcome, not a problem.
* When it does appear, its §1 Context section MUST cite either an
  observation backlog entry (filed ≥ 6 months earlier, unless E2
  applies) or a documented cross-runtime breakdown.
* If a future ADR proposal cannot do this, the correct action is
  not to weaken the discipline — it is to write the missing
  observation file and wait.

---

## 4 · Alternatives considered

* **Status quo (no meta-rule)** — leaves the implicit fourth lane
  open. History (CORBA, SOAP, POSIX threads) suggests this is
  exactly how protocols accrete themselves to death. Rejected.
* **Hard freeze (no changes ever)** — would calcify the protocol
  against real evolution and force users to fork. Rejected.
* **Time-based freeze (no ADRs for N months)** — arbitrary and
  decouples the freeze from actual evidence. Rejected.
* **Council / RFC process** — adds governance machinery FCoP does
  not need at its current scale; the §5.1 evidence test plus the
  pre-flight checklist already do the same filtering job at
  zero overhead. Rejected for now (may revisit if the
  contributor base grows past ~5 active maintainers — which
  itself would qualify as the kind of evidence ADR-0039 demands).

---

## 5 · Status note · the era this opens

Adopting ADR-0039 is the moment FCoP stops being a *designed*
protocol and starts being a *lived* one. From this date forward
the protocol's growth surface is not whiteboards or ADR drafts —
it is the friction of agents actually moving files in real
coordinated work.

The next time the protocol changes, the change will not have been
imagined.
It will have been observed.

---

*Filed 2026-05-21 · the day the design era ended and the
absorption era began.*
