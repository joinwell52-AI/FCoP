# Looking, but Not Touching

### A Popular-Science Walkthrough of FCoP's Three-Layer Semantic Execution Chain — Why the Protocol "Only Looks, Never Modifies"

![Cover](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/assets/looking-without-touching-cover.png)

> *Looking, not Touching: a popular-science walkthrough of FCoP's three-layer semantic execution chain — why the protocol can see, interpret, and write a remediation plan, but stops short of executing it.*

---

## TL;DR · For Readers in a Hurry

- FCoP is a file protocol, not a task executor — the protocol deliberately separates "seeing a violation" from "reaching in to fix it," with three layers between them.
- The three-layer semantic execution chain: **L1 See the Facts** → **L2 Interpret as Violations** → **L3 Write the Remediation Playbook**.
- The output is called `INSPECTION.md`: **structured findings + suggested remediation plan** — not a command; execution authority stays with the human or a human-authorized agent.
- This layering is a hard constraint in FCoP: any extension that would "let the tool act on its own" **must be proposed in a separate ADR**, approved by ADMIN. It cannot silently grow out of the audit tool.

Why split a simple "check + fix" into three layers? Because once a protocol tool can "act automatically," it's only one LLM hallucination away from scrambling the whole project — see the body for details.

---

## 1 · A Design Choice Invisible to Most Developers

If you've only used `eslint --fix` / `black .` / `pre-commit run --all-files`, you probably default to:

> Check tool finds a problem and fixes it right away — isn't that convenient? Saves effort.

FCoP doesn't do that. After FCoP's equivalent tool `fcop_audit()` finishes, **not one line of project file is changed** (except the report it writes). It only produces one Markdown file:

```text
fcop/shared/INSPECTION-20260512-001-takeover.md
```

That report contains:

- What was found (facts)
- What that means as a violation (interpretation)
- What to do about it (remediation plan + copyable commands + rollback steps)

Then the tool exits. Whether to follow that playbook and make changes is **your decision — or the decision of an agent you've authorized**.

Engineers seeing this design for the first time often ask:

> If it already knows how to fix it, why not just fix it? Isn't that one extra manual step wasted?

The answer to this question is everything in this essay: **because "seeing" and "acting" are two different things, and keeping them separate is the core mechanism that lets FCoP run stably**.

---

## 2 · The Three-Layer Execution Chain — What the Protocol's Eyes Look Like

The diagram below is a schematic of FCoP's "internal organs" — splitting "see → interpret → write the playbook" into three layers, with no short-circuit permitted between any of them:

![FCoP Three-Layer Semantic Execution Chain Model v1.0](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/adr/FCoP-semantic-execution-chain-v1.0.png)

The fastest way to read this diagram is top-to-bottom:

```text
Project Working Tree
       │
       ▼  scan (read-only)
┌─────────────────────────────────────────┐
│  L1 · Detection Layer · See the Facts   │
│  6 scan_*() methods, pure scanning,     │
│  no interpretation                      │
│  Output: Facts (raw facts / counts /    │
│  evidence)                              │
└──────────────┬──────────────────────────┘
               │  interpret
               ▼
┌─────────────────────────────────────────┐
│  L2 · Interpretation Layer ·            │
│  Explain the Meaning                    │
│  Facts → Rule matching → Violation list │
│  Output: Violations (structured,        │
│  machine-readable)                      │
└──────────────┬──────────────────────────┘
               │  generate
               ▼
┌─────────────────────────────────────────┐
│  L3 · Documentation Layer ·             │
│  Write the Playbook                     │
│  Violations → Tier 1/2/3 groups →       │
│  copyable commands                      │
│  Output: INSPECTION.md (human-readable) │
└──────────────┬──────────────────────────┘
               │  use
               ▼
        Human or agent decides and acts
        (execution happens outside FCoP)
```

Two things to notice:

1. **The three layers are a one-way pipeline**: L1 doesn't know what L3 looks like; L3 cannot skip L2 to directly read project files. Each layer only interacts with the output of the layer before it.
2. **The protocol's boundary stops at `INSPECTION.md`**: the execution box is drawn outside the dashed line — FCoP protocol itself never crosses over.

Together, these define FCoP protocol tools' "restraint": the protocol provides complete "see + think + write," but **does not provide "do"**.

---

## 3 · L1 Detection Layer — Only Looking, Not Judging

L1 is the protocol's eyes. It does one thing: **tell you what's currently in the project**. It does **not** tell you whether those things are "correct" — that's L2's job.

L1 currently consists of 6 `scan_*()` methods, each answering one independent question:

| Method | What It's Asking | Related Rule |
|---|---|---|
| `scan_misplaced_envelopes()` | Are any envelope files in the wrong bucket? (e.g., a `kind: report` file in `tasks/`) | Rule 2 · Files are Protocol |
| `scan_legacy_role_docs()` | Are there "grassroots role docs" in the project root (scattered `.md` files without frontmatter)? | Rule 1 · Two-Phase Startup |
| `scan_legacy_manifests()` | Besides `fcop.json`, are there other `fcop/*.json` files pretending to be "another identity"? | Rule 0 · Single Source of Truth |
| `scan_cursor_rules()` | Are the protocol rules in `.cursor/rules/` complete? Any grassroots `.mdc` mixed in? | P0 · Rule Deployment |
| `scan_shared_deployment()` | How complete is `fcop/shared/`'s three-layer team document deployment? | Rule 4.5 · Three-Layer Docs |
| `scan_ghost_prefixes()` | Are there ghost prefixes like `DRAFT-` / `HANDOFF-` / `AMEND-` / `*-v2.md`? | Rule 5 · History Only Appends |

Each method returns a set of **Facts**:

```python
Fact {
    fact_id:    "F-001"
    source:     "scan_legacy_manifests"
    evidence:   ["fcop/codeflow.json"]   # which files triggered this
    count:      1
    raw_data:   {...}                     # file size / timestamps etc.
}
```

Notice **Facts have no "severity"** — L1 doesn't know whether this counts as P0 or P2; its job is only "seeing." Separating "seeing" from "rating" is intentional in FCoP:

- When rules evolve (e.g., upgrading "ghost prefixes" from P1 to P0), only L2's interpretation logic needs changing — **L1 doesn't change a single line**.
- L1 doesn't depend on any human judgment about "how serious should this rule be" — that kind of judgment drifts over time, but raw facts don't.

Engineering benefit: **L1 can be independently unit-tested**. Give it a fixture directory, assert how many Facts it returns — no need to simultaneously verify "P0 or P1." When rules evolve, L1's tests don't break along with them.

---

## 4 · L2 Interpretation Layer — Turning Facts into "Violations"

L1 sees `fcop/codeflow.json`. **Is it a violation?** L1 doesn't decide.

L2 decides. L2 takes L1's Fact list, runs "rule matching + severity assessment + remediation mapping," and outputs a **structured Violation list**:

```python
Violation {
    violation_id:   "P0-001"
    severity:       "P0"                                # P0 / P1 / P2
    rule_violated:  "Rule 0 · Single Source of Truth"
    summary:        "fcop/codeflow.json and fcop.json form a dual manifest"
    evidence:       ["fcop/codeflow.json"]
    impact:         "agents will drift between two identity sources"
    remediation:    [                                    # machine-readable, used by L3 to render
        RemediationStep {
            tier:     1
            command:  "git rm fcop/codeflow.json"
            rollback: "git checkout HEAD -- fcop/codeflow.json"
            executor: "OPS"
            estimate: "5 min"
        }
    ]
}
```

A few key points worth pausing on:

**(a) Three severity tiers — P0 must fix, P2 can wait**

- **P0**: Blocks protocol operation — truth has been corrupted / protocol rules aren't deployed / history has been altered. At this tier, if unfixed, FCoP can't guarantee other rules continue to hold.
- **P1**: Normative — files miscategorized, naming non-compliant; the protocol still runs but the next agent will be confused.
- **P2**: Cleanliness — drafts not archived, temp files not deleted; affects aesthetics not function.

**(b) `remediation` is a suggestion, not a command**

Look carefully at that field name — **remediation** (a suggested remediation plan), not `action` or `execute`. L2 has thought through "how to fix this" but **doesn't act** — it just attaches the plan to the Violation for L3 to render.

**(c) L2 doesn't see project files**

This layer only reads L1's Fact list — it doesn't re-scan the filesystem. This means:

- Every L2 decision is traceable — every Violation can be traced back to a specific Fact.
- L2's unit tests can use pure in-memory Fact fixtures, no disk dependency.

---

## 5 · L3 Documentation Layer — Turning Violations into a Human-Readable Playbook

L2's output is already suitable for direct LLM consumption — structured, machine-readable, complete fields. But **humans** find it hard to read.

L3's job is "rendering": turning L2's Violation list into a Markdown document readable by humans (or agents supervised by humans).

It does three things:

1. **Group + sort**: split by severity into P0 / P1 / P2 sections, within each section sorted by rule number.
2. **Humanize**: each Violation rendered as "title + evidence + impact + suggested command + rollback," not a JSON dump.
3. **Execution Block**: regroup all `remediation.command` entries by Tier 1/2/3, providing a **one-copy-to-run command list** (each line with rollback instruction).

Final output: `fcop/shared/INSPECTION-{YYYYMMDD}-{NNN}-{scope}.md`:

```markdown
---
inspection_id: INSPECTION-20260512-001-takeover
status: red                              # red / amber / green
p0_count: 2
p1_count: 5
p2_count: 1
estimate: "1-2 hours"
---

# INSPECTION Report · 2026-05-12 · takeover

## Summary
🔴 RED · P0 × 2 / P1 × 5 / P2 × 1 · Estimated remediation: 1-2 hours

## P0 · Blocking Violations

### P0-001 · Dual Manifest (Rule 0)
- **Evidence**: `fcop/codeflow.json` and `fcop.json` both exist
- **Impact**: agents will drift between two identity sources
- **Suggestion**: `git rm fcop/codeflow.json` (5 min, OPS)
- **Rollback**: `git checkout HEAD -- fcop/codeflow.json`

...

## ▶ Execution Block

### Tier 1 · Immediate (today, low risk, no dependencies)
\`\`\`bash
git rm fcop/codeflow.json
# Rollback: git checkout HEAD -- fcop/codeflow.json
\`\`\`

### Tier 2 · This Sprint (1-2 days, has dependencies)
...
```

Notice that last Execution Block — **this is L3's core innovation**: it packages "what order should I do things, what are the execute/rollback commands for each step" into pasteable code blocks.

But this text is still only a **playbook**. FCoP won't run those commands itself — once `INSPECTION.md` is written, the tool's work is done.

---

## 6 · Why INSPECTION Is Not a Remediation Plan

This is a subtle but very important naming choice:

> **INSPECTION ≠ Remediation Plan**
>
> **INSPECTION = Structured Findings + Suggested Remediation Plan**

Called "Remediation Plan," it sounds like "the plan to be executed next." Called "Inspection," it sounds like "a physical exam report." FCoP chose the latter, deliberately steering the semantics toward "observation."

`INSPECTION.md` also follows FCoP's standard envelope rules:

- **Append-only**: running the same scope a second time on the same day produces `NNN+1`, doesn't overwrite the first — history preserved.
- **Traceable**: every Violation includes `violation_id` + `scan_source` + `evidence`, fully traceable back to L1's raw Fact.
- **Human-first**: Tier grouping, commands with rollback, "suggested executor" for each item.

This means even months later when looking back at "what did we remediate during that takeover," the INSPECTION file in `fcop/shared/` is still there — it's itself a link in the audit chain.

---

## 7 · Five Principles — Why "Not Touching" Is a Design Goal

FCoP summarizes this architecture in five principles, each worth reading closely:

### ① No Boundary Violation

> Work within the boundaries defined by the protocol rules.

`fcop_audit()` only does what the protocol specifies — it doesn't extend to "tidying up the git repo while we're at it" or "reorganizing files."

### ② Observe Only

> Don't modify project state; don't write business files.

The tool is read-only. Its only side effect on disk is the `INSPECTION.md` it produces. This permanently blocks "the tool silently modifying the project."

### ③ No Execution

> Only generate the playbook; execution decisions are made by humans.

The commands in the Execution Block are **suggestions**, not **instructions**. After the tool exits, it waits for human intervention.

### ④ Traceable

> Every violation is traceable; every step is auditable.

Every Violation can be traced back to a specific Fact, scan_source, and evidence. No conclusion is "out of thin air."

### ⑤ Anti-Creep

> Want to "let the tool act automatically" in the future? **Must be proposed in a separate ADR**, approved by ADMIN again. Cannot silently grow out of the audit tool.

This is the most important principle. Its meaning: **the tool not acting today, and acting in the future, both require explicit legislation** — not someone quietly adding a `--fix` parameter in some future PR.

Why so strict? Because FCoP is the protocol layer. Once the protocol layer can "automatically modify projects," the boundary between it and the application layer (the tools actually responsible for doing work) blurs — and then all "protocol rules are just guidelines" stories begin. FCoP draws this line firmly: **protocol tools are always observers; execution authority is always outside the protocol**.

---

## 8 · Boundary Comparison with Similar Tools

If "not touching" still feels strange, look at how other familiar tools draw the line:

| Tool type | See | Think | Write Playbook | Execute |
|---|:-:|:-:|:-:|:-:|
| `linter` (eslint / ruff) | ✅ | ✅ | △ brief | ❌ |
| `linter --fix` | ✅ | ✅ | ❌ | ✅ auto-fix |
| `test runner` (pytest) | ✅ | ✅ | ❌ | ❌ only reports errors |
| `CI pipeline` | ✅ | △ | ❌ | ✅ runs commands |
| `agent` (claude / cursor) | ✅ | ✅ | △ in chat | ✅ actively modifies |
| **`fcop_audit()`** | ✅ | ✅ | ✅ structured | ❌ |

Notice `fcop_audit()`'s unique cell: **"Write Playbook · Structured"** — that's its distinctive position: **write a detailed enough, copyable, auditable playbook, then stop there**.

It doesn't compete with linter for the "auto-fix" market, doesn't compete with CI for the "auto-run" market, doesn't compete with agents for the "actively modify" market. Its position is:

> **The gap between "only reports errors" and "auto-fixes"**: write "how to fix this" as readable + copyable + auditable documentation, leaving full execution authority to humans.

Why does FCoP occupy this position? Because protocol evolution needs this position — after the protocol changes, old projects need "takeover" or "upgrade," and the remediation path between must be **reviewable, stoppable, batchable**. Auto-fix tools can't do this (they're "do it all at once"); agents can't either (their execution isn't auditable or stoppable).

---

## 9 · The Protocol's Restraint Is Meant to Be Passed Down

Whether a protocol tool still works correctly ten years later depends on a simple question:

> **Does it have the ability to "act on its own"?**

Protocol tools that can act on their own will eventually act wrongly. Because:

- Their execution depends on code version, on the underlying OS, on the state of the checked project — all three things drift over time.
- One execution error can scramble the checked project, and since the protocol is a "trusted layer," the cost of errors is much higher than at the application layer.

After FCoP separated "seeing" from "doing," this risk is significantly reduced — even if `fcop_audit()` writes a bad INSPECTION due to some bug, **the project itself hasn't been touched**. Humans reading the INSPECTION can immediately see "this suggestion is wrong" and choose not to execute it.

This is the deepest design intent of this three-layer architecture: **leave decision-making authority and execution authority completely on the human side**.

The protocol is responsible for "seeing clearly." The protocol is responsible for "thinking through." The protocol is responsible for "writing clearly."

As for "whether to do it" — that's outside the protocol's jurisdiction.

---

## One-Sentence Review

FCoP uses three layers `L1 → L2 → L3` to separate "see → interpret → write playbook," producing `INSPECTION.md`, then stopping there. **The protocol's eyes don't touch — this is by design, not oversight.**

---

**Related Reading**

- **`adr/FCoP-semantic-execution-chain.md`** — The source document for this essay; normative three-layer definition, complete ADR references, protocol maturity snapshot
- **`adr/ADR-0030-capability-governance-boundary.md`** — Schema layer: capability boundaries (what can be done)
- **`adr/ADR-0031-governance-alert-layer.md`** — Signal layer: governance signals (what happened)
- **`adr/ADR-0032-fcop-audit-protocol-inspection.md`** — Compiler layer: tool capability (suggested remediation)
- [Why the Protocol Stays Short](why-the-protocol-stays-short.en.md) — Why FCoP doesn't let the protocol grow on its own — the same guardrail as "protocol tools don't act," from both ends

---

*"Look clearly, but don't touch — this is restraint, not a defect."*
