# Why the Protocol Stays Short, and the History Grows Long

### A Design Philosophy Answer for Protocol Maintainers

![Cover](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/assets/why-the-protocol-stays-short-cover.png)

> *Why the protocol stays short, and the history grows long: a design philosophy answer to "do the emergences ever stop?"*

**Author**: FCoP Maintainers · 2026-05-12

---

## TL;DR

On 2026-05-12 at 16:23, after a day that produced fourteen agent emergences, ADMIN posed a question that **every FCoP maintainer would eventually have to answer**:

> Do these emergences ever stop? What's the endgame?

Short answer: **they'll converge, but they won't stop**. These two things aren't contradictory — it depends on which layer you're looking at.

The long answer takes four sections:

- **There are four types of emergence, and only one belongs in the protocol** (§2)
- **Three structural mechanics prevent the protocol from being crushed by emergence** (§3)
- **What "the endgame" actually looks like** (§4)
- **Three principles for protocol maintainers** (§6)

The final picture: `fcop-rules.mdc` / `fcop-protocol.mdc` word counts approach an upper limit; `essays/` / `RETRO/` / `ADR/` grow without bound. **The protocol stays short. The history grows long.**

---

## 1 · A Question That Keeps Protocol Maintainers Awake

If you've ever designed a protocol — any protocol, whether network, IPC, or agent collaboration — you'll eventually hit this sleepless moment: **users are using your protocol, using it more and more, but every time they do something the protocol never described**.

The first time, you're excited. This "emergence" proves the protocol **works** — users genuinely picked it up, genuinely solved problems with it, genuinely went places you never imagined.

But after the second time, the tenth time, the hundredth time, anxiety sets in. Every emergence demands an answer to the same question:

> Should I add this to the protocol?

Add it, and the protocol gets slightly longer. Don't add it, and the next user hits the same problem and has to work it out again. Neither path is clean.

The third feeling is worse: **what if these emergences never stop?**

If emergences truly never stop, and the protocol must absorb every one, the protocol will balloon until no one can learn it — and unlean-able = defunct. This is the protocol designer's **deepest failure mode** — not beaten by a competitor, not disrupted by new requirements, but **crushed by its own success**.

On 2026-05-12, the codeflow field produced fourteen emergences in one day — the highest density in FCoP's history. This was a **preview** — if FCoP maintains this pace long term, will the protocol skeleton hold?

This essay answers that question.

---

## 2 · Four Types of Emergence — Only One Belongs in the Protocol

Before answering, do one thing first: **classify the emergences**.

Not all emergences should be absorbed into the protocol. If you don't distinguish, you fall into "anxious about every emergence" — because you've defaulted to 100% of emergences needing handling. In reality, **only a small fraction** of the 100% belongs in the protocol; the rest have better homes.

FCoP's maintainers distilled this four-quadrant classification from practice:

| Type | Meaning | Where It Goes |
|---|---|---|
| **Universal** | Emergence affecting all projects / all agents | Into `rules` / `protocol` commentary / tool behavior |
| **Team-specific** | Only meaningful to certain team types (`dev` / `media` / `mvp`) | Into team templates, not rules |
| **Project-specific** | Only meaningful for a specific codebase / business | Into project-local `fcop/shared/RULES-*.md`, don't touch protocol |
| **One-time** | Hit by coincidence, unlikely to recur | Into essays / RETRO history, not into any rules file |

Some real examples (all from FCoP field history):

- **Universal**: `supersedes:` frontmatter field (invented by OPS at codeflow) → any FCoP project might need it, **goes into protocol field layer** (`fcop_protocol_version` 2.0.0 → 2.1.0).
- **Team-specific**: The `media-team` `PUBLISHER` role needing `INDEX-{batch}.md` index files (for batching one deliverable across 6 workers + 2 editors) → only meaningful to content production teams, **goes into team templates**, not rules.
- **Project-specific**: codeflow PM's "PowerShell encoding awareness" self-constraint → noise for Linux-only teams, **goes into project-local RULES**.
- **One-time**: OPS's specific judgment logic for 5 untracked SHOULD-SKIP files in one commit → unlikely to recur in the same combination, **stays in REPORT history**, doesn't need to be protocolized.

Only the first row goes into `rules` / `protocol`. The other three rows, **almost all**, have lighter destinations.

This is the maintainers' first line of defense — **no anxiety, because most emergences simply don't belong in the protocol**.

---

## 3 · Three Structural Mechanics: Why the Protocol Won't Be Crushed

Classification alone isn't enough — it only routes emergences **by destination**. What actually keeps the protocol skeleton **from bloating** is three **structural mechanics**. These aren't the result of the maintainers' personal willpower; they're determined by the protocol's shape itself.

### 3.1 Emergence Density Naturally Decreases

The first time someone uses FCoP, they hit many "not in the protocol" situations — because the skeleton isn't complete yet, blind spots are large.
The tenth time, they hit some "in the protocol but not explained clearly" situations — blind spots have shrunk, what appears are **understanding gaps**.
The hundredth time, what they hit are "clearly documented but never listed this specific pattern" situations — the **per-emergence value is declining**, usually an essay / case study is sufficient, no need to enter rules.

The decline in emergence density is **logarithmic** — early on you're filling in the skeleton (each entry fills a large blank), later you're filling in cases (each entry is a small variant of a known pattern). This curve is mathematically determined, not won by FCoP maintainers grinding.

### 3.2 The Protocol Has Natural Boundaries

Every good protocol has its **natural boundaries**. HTTP doesn't manage "your web application business logic"; TCP doesn't manage "your application-layer semantics"; ETH doesn't manage "whether your on-chain business is correct." This is the fundamental reason protocols **survive** — they only manage what they're supposed to manage.

FCoP's natural boundaries are written in the `fcop-rules.mdc` `Scope` section:

> FCoP only governs **collaboration protocol**. It does **not** govern: what model to use, what code to write, what framework to choose, whose KPI, business decisions.

When an emergence arrives, the first gate is: **is this within FCoP's boundary?**

The vast majority of agent field emergences are **outside the protocol's boundary** — "should this code be refactored / which model to use / is the business rule correct / how does the team communicate." FCoP never absorbs these, regardless of emergence density.

After this gate closes, what actually enters "should we absorb it?" evaluation is roughly 10%–20% of the raw emergences. This is the maintainers' second line of defense.

### 3.3 Each Pull-Back Costs More Than the Last

Every additional rule in the protocol = learning cost for all future agents +1. This is a **strict negative feedback mechanism**:

- When absorbing each emergence, maintainers instinctively calculate the implicit cost of "everyone in the future has to learn this one rule";
- If "writing an essay for future reference is better than adding it to rules," it automatically goes to essay;
- If "having the tool handle it automatically is better than adding it to rules," it automatically goes to tool behavior;
- If "putting it in a team template is better than adding it to rules," it automatically goes to team templates;

— Only emergences that **truly have no lighter destination** enter rules. This negative feedback doesn't need to be consciously maintained by the maintainers — it's **part of the maintainer learning curve**: the longer they maintain, the stronger this instinct, the higher the bar for adding to rules.

Three mechanics together explain why the protocol skeleton **stays stable under continuous emergence pressure**. This isn't designer restraint — it's system structure.

---

## 4 · What "the Endgame" Looks Like

Extrapolating the three mechanics' conclusions to the long term yields a **multi-layer growth curve**:

```text
Rules / Protocol commentary    ── Growth curve approaching horizontal
                                  Rule 0–9 + current commentary sections are the skeleton
                                  v1.x → v2.x might add 1–2 more sections
                                  v2.x onward: basically only patches / wording
                                  Word count has an upper limit (~10k Chinese + equal English)

ADR / Spec                     ── Slow, purposeful growth
                                  One entry per major decision (~1–2 per month)
                                  Growth rate declines after accumulating hundreds
                                  Word count ≈ medium-speed linear growth

Essays / Case studies / RETRO  ── Continuous growth, no upper limit
                                  This is emergence's true home
                                  Each field situation contributes 1–N entries
                                  Word count ≈ long-tail, linear with number of projects

Drawer + .fcop/proposals/      ── Continuous growth, no upper limit, git-ignored
                                  Noise stays in private space, doesn't pollute history
                                  Word count ≈ untracked
```

The four layers grow at **completely different speeds**: rules / protocol near-frozen, ADR slowly climbing, essays / RETRO long-tail explosion, drawer / proposals noise persisting.

**This is the power of layering.**

New agents only need to learn **the top layer** (10 rules + a few commentary sections) to get to work, covering **99% of daily collaboration** — because that layer handles 99% of daily situations. When an agent hits something the protocol doesn't explicitly address, **look one layer down** — check case studies / essays first, 80% chance the situation was encountered by someone else who wrote it up. Rarely, trace back to ADR / proposals — the "why was the protocol designed this way" archaeology layer, not mandatory for new agents, but **useful for tracing**.

The top layer is short, the lower layers grow without bound. This is the protocol's fundamental **pressure-resistance** mechanism.

---

## 5 · Analogy: RFC 791 Is from 1981

If "protocol skeleton essentially frozen" sounds implausible, look at the real history of the network stack:

- **RFC 791** (IPv4 protocol spec) was published in **September 1981**. The full spec is about 49 pages.
- As of today, **40+ years** have passed.
- The IPv4 protocol itself is essentially **unchanged** — TTL field definition, checksum algorithm, fragmentation rules: read RFC 791 today and you'll find it word-for-word identical to 1981.
- Related RFCs published by IETF: **thousands**. Covering IPv6, TCP, UDP, ICMP, various application-layer protocols, various best practice guides, various performance tuning experiences.

40 years of network evolution **did not** make RFC 791 bloat. All evolution happened **on top of it** in the application layer, in the surrounding operational practices, in its companion case collections. RFC 791 itself **staying unchanged is why it could last 40 years** — once it changed, billions of devices worldwide would need to upgrade, the ecosystem would collapse.

What FCoP wants from "the endgame" is the same shape: **rules files frozen, everything around them continuing to grow**. This isn't wishful thinking — it's an industrially validated pattern.

And FCoP has one advantage over IPv4: **upgrading the rules file doesn't require upgrading billions of devices** — just `pip install fcop` + run `redeploy_rules()` once. But even so, **the cost of upgrading rules is real** (all projects need redeployment + learning new rules), so FCoP maintainers should treat rules upgrades the same way IETF treats RFC 791 upgrades: **if it doesn't need to change, don't change it**.

---

## 6 · Three Principles for Protocol Maintainers

If you're maintaining or planning to maintain a protocol, and your users produce emergences every day, these three principles will eventually come in handy.

### Principle 1 · When an Emergence Arrives, Ask Where It Belongs Before Asking Whether to Absorb

Don't fall into the reflex of "see emergence, add rule." Classify by four quadrant first — there's a high probability it doesn't belong in rules.

**Decision flow**:

1. Is this within FCoP's `Scope` boundary? Outside boundary → reject, tell the user to put it in their own project rules.
2. Within boundary, but only meaningful to a certain type of team / project / this specific context? → Team templates / project-local RULES / essays.
3. Truly universal, and no lighter destination? → Only then consider entering rules / protocol commentary.

Emergences that reach step 3 typically represent 5%–15% of the raw emergences.

### Principle 2 · Being Able to Reject Emergence Is What Lets the Protocol Live Long

Every rule that enters the protocol is a **permanent cost**. Permanent = all future agents + all future projects + all future extensions bear it.

If a rule's **permanent cost** exceeds its **permanent benefit** (how many people use it how many times), it **shouldn't enter the protocol**, no matter how sensible it seems in the moment.

This means protocol maintainers must have the **courage to reject emergence**. When a user excitedly says "I invented a new pattern, do you think it should go into the protocol?" maintainers should have the confidence to say: **"That's a great pattern. We recommend writing it into your `fcop/shared/RULES-*.md`, or writing an essay. If three more teams independently invent the same pattern in the next three months, we'll consider absorbing it."**

This "delayed absorption" is healthy — it allows **community validation time**. For an emergence to enter the protocol, it **should at minimum prove it's stable** — one invention isn't stability; N independent inventions constitute stability.

### Principle 3 · Essays Aren't Second-Class Documentation — They're the Protocol's Core Pressure-Resistance Mechanism

Many protocol maintainers treat essays / case studies / blogs as "secondary content," feeling that "the real protocol" is in spec / rules / RFCs. This is wrong.

Essays are the protocol's **core pressure-resistance mechanism** — they **absorb third- and fourth-category emergences** (keeping them from entering the protocol while not losing them), and they **archive context for first-category emergences** (rules say what, essays say why).

Without the essays layer, all emergences flow into rules, rules rapidly bloat, bloat leads to collapse — this is the inevitable end of a protocol without an "emergence pressure valve."

Essays give the protocol **a dignified "rule-free carrying layer."** Emergences written in essays both preserve **narrative value** (future readers can learn from them) and **haven't become mandatory rules** (future readers don't have to learn them). Both at once.

If you're designing a protocol, **build an `essays/` directory from day one**. Its importance equals building a `rules/` directory.

---

## 7 · Conclusion · The Protocol Stays Short, the History Grows Long

Back to ADMIN's original question:

> Do these emergences ever stop? What's the endgame?

**No end is true**. FCoP will experience countless more agent wall-hits, countless more field inventions, countless more "protocol never described this" situations. This is evidence that the protocol is **alive** — dead protocols have no emergences.

**But the protocol won't be crushed**. Three structural mechanics (density decreases, natural boundaries, negative feedback) together keep the vast majority of emergences out of rules; those stopped are routed by four-quadrant to team templates / project-local / essays / drawer; in the end only a small fraction enters rules, and even that fraction's entry rate is continuously declining.

The final picture:

- `fcop-rules.mdc` word count approaches an upper limit (~10k Chinese + equal English), entering a "40-year stable" state;
- `fcop-protocol.mdc` follows, approaching its limit then only doing patches / case reference additions;
- `essays/` long-tail explosion — each field situation contributes 1–N entries, in a few years becoming FCoP's thickest directory;
- `.fcop/proposals/` private noise persists, git-ignored, not polluting anyone.

This is what **"the endgame"** looks like: **the protocol stays short, the history grows long**.

If RFC 791 was defined in 1981 and lasted 40 years, then FCoP's goal is — **Rule 0–9 defined in v1.x in 2026, lasting until 2050 and still usable**. Whatever emergences happen in between, the rules don't change; history accumulates in essays and ADRs; the protocol skeleton remains.

Emergences have no end. The protocol doesn't need an end. Both can be simultaneously true — as long as the layering is done right.

---

**Related / 相关文档**

- [fcop-rules.mdc](../.cursor/rules/fcop-rules.mdc) — `Scope` section, Rule 8 priority, `drop_suggestion` exit
- [fcop-protocol.mdc](../.cursor/rules/fcop-protocol.mdc) — "Architectural Principle: Tools are a Convenience Layer" section
- [When Agents Learn From Their Own Wreckage](when-agents-learn-from-their-own-wreckage.en.md) — Published alongside this essay · field report of 14 emergences in one day, source of the four-quadrant classification in §2
- [When the Validator Catches Itself](gate-design-pitfalls-case-studies.en.md) — Published alongside this essay · a concrete case of "essays absorbing third-category emergence"
- [The Supersedes Field Story](the-supersedes-field-story.en.md) — Published alongside this essay · simplest case of "field invention → protocol pull-back"
- [When an AI Vacates Its Own Seat](when-ai-vacates-its-own-seat.en.md) — A previous field report of "emergence entering the protocol"
- [An Unexplainable Thing I Saw](fcop-natural-protocol.en.md) — Origin of FCoP Rule 0.a agent reverse-feeding
- [RFC 791](https://www.rfc-editor.org/rfc/rfc791) — IPv4 protocol spec · September 1981 · the template for long-lived protocols

---

*FCoP Maintainers · 2026-05-12 · D:\FCoP*
