# The Day We Almost Added Custody to FCoP

> On 21 May 2026, FCoP did something rare: the protocol rejected its own well-meaning extension.

---

## 1. Where it started

That morning, FCoP 3.0's State Ontology (ADR-0035) had just been Accepted. We had nailed down the lifecycle directory:

```
fcop/_lifecycle/
├── inbox/
├── active/
├── review/
├── done/
└── archive/
```

Whatever folder a file lives in *is* the lifecycle stage it is in. Rule A puts it bluntly: **file path = state truth**.

But 0035 only answered "where is it now?" It did not answer:

- How did it get there?
- Who's holding it?
- Who handed it off to whom?

So I started drafting three new ADRs:

| ADR | Proposal |
|-----|----------|
| 0036 | Event Layer — every `mv` appends a `transitions:` event |
| **0037** | **Custody Layer — introduce a `custodian` field to track ownership** |
| 0038 | Boundary Charter — meta-rule to prevent OS drift |

All three were written. README updated. Looking at it, I felt satisfied: the protocol was closed, the lifecycle complete, ownership clear.

I sent it to ADMIN.

---

## 2. The RFC that flagged it

ADMIN did not nod. She replied:

> "You now have **3 truth systems**:
> 
> - State truth (0035) — path = truth
> - Event truth (0036) — transitions = history
> - **Custody truth (0037) — custodian field**
> 
> This isn't a design error. But it's a *non-convergent structure*."

My first reaction was to push back. "Custody is a real need," I said. "The book in the library — who's holding it right now — is independent information. Location can't express it, events can't either. Events are past, location is now, custody is *who has it in their hands*."

ADMIN didn't engage with the example. She made a sharper claim:

> "The moment custody becomes a layer, it inevitably becomes a second truth system."

So I tried a counter-design. "Fine. Let's go full Event Sourcing: events are the only truth, state and custody are derived projections. Then there's only one truth."

ADMIN saw through it immediately:

> "You're trying to kill the custody pollution by pushing the entire protocol toward Event Sourcing.
> 
> But you forgot what Rule A physically *means* — `ls active/` gives you current state at a glance.
> 
> If state is a derived projection, then what `ls` shows you is a cache, not truth.
> 
> FCoP devolves into an Event Store."

That's when I saw the actual problem:

**I was using one mistake (Event Sourcing-ification) to mask another (custody being redundant).**

The real issue wasn't "the protocol has multiple truths." It was that **custody as a separate truth was the redundant one**. State and Event are *time-orthogonal*—one is NOW, the other is PAST. They are not two truths; they are two temporal faces of the same truth.

Only custody sits in between. Not NOW (state already says so), not PAST (events already say so). It floats in a gap of its own making. That gap is its problem.

---

## 3. The decision

The protocol settled into this shape:

```
META       ADR-0038 · Boundary Charter (prevents OS drift)
              ↓
NOW         ADR-0035 · State (path = truth)         ← Accepted & Frozen
PAST        ADR-0036 · Event (audit trace)          ← Accepted
            NOTE   · Custody = interpretation       ← no layer, note only
```

ADR-0037 was **withdrawn before reaching Accepted**. Its idea survives as an informative NOTE:

> Custody is not a protocol layer.
>
> It is an emergent interpretation of file ownership derived from:
> - file location (current state)
> - event history (transitions)
>
> It is not stored, not authoritative, and not part of the protocol state model.

That paragraph now lives permanently at `adr/NOTE-custody-is-not-a-layer.md`.

---

## 4. Why custody had to vanish

I thought about it afterward. Custody looks reasonable but carries three invisible gravity wells, each of which would pull the protocol toward Agent OS:

### 4.1 The field-isation well

The moment custody is a **field**, it needs **maintenance**. Maintenance means:

- Should we initialise `custodian` at task creation?
- Should `claim` update it?
- Who is allowed to modify `custodian`?
- Is modifying `custodian` an event?

Each question demands a new tool, a new rule, a new validator. The protocol surface doubles in six months.

### 4.2 The layer-isation well

The moment custody is a **layer**, it **attracts policy**:

- Since we have custody, let's add an assignment policy (who should take it)
- Since we have assignment, let's add permissions (who can assign)
- Since we have permissions, let's add capability enforcement (who can override)

Three steps in, FCoP is competing head-on with Kubernetes RBAC and IAM systems.

### 4.3 The cognitive well

This one is the most dangerous. **Custody is a human-native concept.** Even if the protocol doesn't have it, six months from now someone will inevitably propose:

> "Can we add an `assignee` field?"
> "Can we add an `owner` field?"
> "Can we add a `holder` field?"

Each is the same mistake under a new name.

This isn't a design problem; it's a cognitive one. So the NOTE exists not just to "preserve the idea." It exists to **leave the future us an immune memory**—next time someone proposes adding custody, please read the NOTE first, then this essay.

---

## 5. How "well-meaning extensions" kill protocols

I read some protocol history afterward and noticed a pattern:

**Most protocols don't die by being overthrown. They die by being kindly extended.**

- POSIX hesitated on threading; pthread fragmented into incompatible branches
- HTTP/1.1 over-specified long connections; WebSocket had to be invented to escape
- CORBA tried to "do everything"; was killed by HTTP+JSON
- SOAP wanted "enterprise-complete"; was abandoned for REST

None of these deaths were caused by competitors. Each one was **self-inflicted bloat**.

What FCoP learned on 21 May 2026:

> **The greatest danger to a protocol is not being overthrown — it is being kindly extended.**
>
> Every new field, layer, or concept that "looks reasonable" comes with a well-intentioned argument: *"if we added this, it would be so much more convenient."*
>
> But a protocol's simplicity is the entire reason it exists. Lose that, and it's no longer a protocol — just another framework.

---

## 6. How ADR-0038 came to be

That afternoon we wrote a meta-charter — ADR-0038 Boundary Charter. It introduces no new features. It only defines what FCoP **doesn't do**.

Its core is the "five-question filter." Any future extension proposal must pass these before reaching Accepted:

1. Does it describe semantics, or execute behavior? Reject the latter.
2. Does it define file contracts, or own runtime state? Reject the latter.
3. Does it coordinate multiple agents, or schedule a specific agent? Reject the latter.
4. Can it be re-implemented by another host without an FCoP runtime? Reject if no.
5. Does it overlap with Temporal / LangGraph / CrewAI in responsibility? Reject if yes.

But 0038 also carries an **exemption clause** (§5.1). Because a protocol that never evolves freezes to death, which is worse than dying of bloat. The exemption conditions are strict: 2+ independent projects must report the same gap within 6 months (complexity-forced), or a real scenario must be demonstrably **impossible** without the extension (cross-runtime breakdown).

The Boundary Charter's real job is not "reject all extensions." It is to **make every extension pay an argumentative cost commensurate with its impact**.

---

## 7. Something else that happened that day

After finishing 0038, I went back to look at ADR-0035. Its status was `Accepted`.

I added one line:

> `Status: Accepted & Frozen (2026-05-21 · semantics frozen per RFC)`

Then I added a sentence at the bottom:

> **FCoP = file location is truth; everything else is trace.**

That is the entirety of FCoP 3.0's ontology.

The next day I opened the `spec/` directory, compressed 0035 / 0036 / 0038 / NOTE into a 14-page formal specification (`spec/fcop-3.0-spec.md`), and wrote an RFC-style version (`spec/fcop-3.0-rfc.md`) as the protocol's "external stable surface."

Then the protocol stopped there. 3.0 is 3.0. Any next move must pass through ADR-0038 §5's five questions.

---

## 8. Closing

I want to leave ADMIN's last sentence here:

> "You're not 'refining the protocol' anymore. You're doing **protocol semantic sealing**."

FCoP 3.0 didn't come into being by what was added. It came into being by what was refused.

It refused custody.  
It refused Event Sourcing.  
It refused runtime ownership.  
It refused scheduling.  
It refused every "reasonable-looking" extension.

What's left is one line:

> **file location is truth; everything else is trace.**

That's enough.

---

*2026-05-21 · The day the protocol refused its own extension · FCoP 3.0 sealed*

**Further reading**:
- `spec/fcop-3.0-spec.md` — formal specification
- `adr/ADR-0038-fcop-boundary-charter.md` — boundary charter
- `adr/NOTE-custody-is-not-a-layer.md` — custody's epitaph
- `.fcop/proposals/20260521-rfc-semantic-collapse-and-custody-rejection.md` — full decision chain
- Chinese version: `essays/the-day-we-almost-added-custody.md`
