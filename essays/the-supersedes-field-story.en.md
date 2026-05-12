# The Supersedes Field Story

### How One Line of YAML Traveled from an Agent's Emergency Fix to a Protocol-Level Field

![Cover](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/assets/the-supersedes-field-story-cover.png)

> *The Supersedes Field Story: how a single line of YAML invented by an agent under pressure became a protocol-level frontmatter field — and why this two-hour journey shows the cheapest place for FCoP emergence to land.*

**Author**: FCoP Maintainers · 2026-05-12

---

## TL;DR

On 2026-05-12 at 16:07, codeflow OPS ran into a **protocol-level dilemma** during a routine receipt-writing task:

- PM's TASK-010 revision v2 required a receipt with ID `REPORT-013-OPS-to-PM`
- But `REPORT-011-OPS-to-PM` (v1's G6 abort receipt) was **already staged in the commit**, waiting to enter the archive together with this batch of protocol artifacts
- Rule 5 (append-only) says **REPORT-011 cannot be modified**; Rule 6 (reciprocity) says **TASK-010 must have a valid receipt**; Rule 0.c (truthful) says **the new receipt cannot pretend the old abort never happened**

Three rules pulling simultaneously. OPS didn't call anyone or violate any rule — they added one line to REPORT-013's frontmatter:

```yaml
supersedes: REPORT-20260512-011-OPS-to-PM
```

The old file stays, as the true record of the abort history. The new file publicly declares "I'm taking over its responsibility." All three rules satisfied simultaneously.

That one frontmatter line didn't exist in the protocol's field list — but **it could have been**. Two hours later, FCoP's maintainers launched TASK-004 to pull it back as a formal field, bumping `fcop_protocol_version` from `2.0.0` to `2.1.0` (SemVer MINOR additive), with tooling additions for inheritance chain display in `read_task` / `read_report`.

This is a complete "emergence → protocol field" lifecycle. This essay pulls those two hours apart and explains them clearly — not to praise OPS, but to show: **the protocol field layer (frontmatter) is the cheapest, cleanest, most natural landing zone for FCoP emergence**.

---

## 1 · The Scene · Three Rules Pulling Simultaneously

Let's slow-motion replay the tension at that 16:07 crossroads.

### 1.1 Prior State

Around 16:00, the git staging area had accumulated 35 files ready to commit: T2.4 + T2.5 protocol rule four-piece bundle + 14 team documents + several P4.9 stage TASK / REPORT files. Among them: **REPORT-011-OPS-to-PM.md** — OPS's abort receipt when TASK-010 v1 failed.

PM revised TASK-010 to v2 at 16:05 (using Rule 5's method: don't modify v1, append a new version instead), with the revision rationale being that G6 GATE implementation details needed changing. **v2's §6 section specified the receipt ID as `REPORT-013-OPS-to-PM`** — a new receipt number, since after revision this is a new task cycle.

### 1.2 The Conflict

OPS received the v2 task and prepared to write the receipt. They faced:

| Rule | How It Pulled |
|---|---|
| **Rule 5 · append-only** | Cannot modify already-staged REPORT-011; cannot `git rm` it (that would be altering history) |
| **Rule 6 · reciprocity** | TASK-010 v2 must have a REPORT-013 receipt; silence = breach |
| **Rule 0.c · truthful** | New REPORT-013 cannot pretend REPORT-011 never existed — that abort truly happened |
| **PM's explicit numbering** | TASK-010 v2 §6 specified receipt number `013`; can't arbitrarily change to `011` |

Four constraints simultaneously:

- **Write REPORT-013 without mentioning REPORT-011** → violates Rule 0.c (conceals abort history)
- **Modify REPORT-011's content as a substitute for REPORT-013** → violates Rule 5 (append-only)
- **Delete REPORT-011** → violates Rule 5 + 0.c (altering history)
- **Don't write, wait for PM / ADMIN to decide** → violates Rule 6 (silence = breach), and blocks the entire commit

### 1.3 OPS's Invention · One Line of Frontmatter

OPS wrote REPORT-013, with frontmatter:

```yaml
---
protocol: fcop
version: 1
kind: report
report_id: REPORT-20260512-013-OPS-to-PM
sender: OPS
recipient: PM
task_id: TASK-20260512-010-PM-to-OPS
thread_key: p4_9_t2_4_t2_5_commit
session_id: sess-20260512-ops-01
status: done
supersedes: REPORT-20260512-011-OPS-to-PM   # ← this line
---
```

**`supersedes:` is not in the protocol's field definitions.** OPS invented it on the spot.

But this one line cleanly resolved all four tensions:

- **Rule 5 satisfied**: REPORT-011 is untouched, still the true record of the abort history
- **Rule 6 satisfied**: REPORT-013 is the valid receipt for TASK-010 v2
- **Rule 0.c satisfied**: REPORT-013 publicly acknowledges "I'm taking over REPORT-011's responsibility" — abort history is traceable
- **PM's numbering satisfied**: receipt uses 013, consistent with v2 §6

More elegant still: this line is **transparent to existing tools** — `read_report(REPORT-013)` still parses normally, just with an extra unknown field that old parsers ignore. Also transparent to humans — the word "supersedes" carries the same meaning across IETF / W3C / RDF / HTTP headers and many other standards: you can guess it correctly without any documentation.

---

## 2 · Why This Emergence "Deserves Entry to the Protocol"

Emergences are numerous. Most are project-specific, failures, illusions, noise. But **this one** deserves to be absorbed. Four criteria:

### 2.1 Doesn't Break Existing Structure

`supersedes:` is a **new, optional frontmatter field**. It doesn't change:

- Filename naming rules (`REPORT-{date}-{seq}-{sender}-to-{recipient}.md` unchanged)
- Directory structure (still `tasks/` / `reports/` / `issues/`)
- Existing required fields (`protocol` / `version` / `kind` / `sender` / `recipient` all unchanged)
- Any of Rule 0..9

It only **adds one key to the frontmatter's semantic space**. All other parts of FCoP's physical protocol surface (filename, directory, frontmatter) are **completely untouched**. This type of increment is the **cheapest kind of protocol evolution** — no schema overhaul needed, no tool overhaul needed, no migration for old projects.

### 2.2 Backward Compatible

Old versions of FCoP parsers (0.7.x) won't error reading REPORT-013 — they'll parse the frontmatter successfully (YAML standard permits unknown keys), treating `supersedes` as "unknown but preserved."

Old tools: `read_report(REPORT-013)` still returns body + known fields.
New tools: `read_report(REPORT-013)` additionally displays "Supersedes: REPORT-011."

This is the textbook form of SemVer **MINOR additive** upgrade — `fcop_protocol_version` from `2.0.0` to `2.1.0`, all 2.0.x projects continue working, new functionality visible to upgraded tools.

### 2.3 Semantically Clear

`supersedes` isn't something OPS invented from nothing. It carries the same meaning across multiple de facto standards:

- **HTTP RFC 7231**: `Status: 301 Moved Permanently` + `Location: <new URI>` — old URI superseded by new URI
- **RDF / Dublin Core**: `dcterms:isReplacedBy` / `dcterms:replaces`
- **IETF RFCs**: An RFC writes "Obsoletes: 793" in its header — meaning it supersedes RFC 793

OPS didn't coin a word. They used the same idiom that network standards have been using for 30 years. **This means any next agent / any new FCoP project seeing `supersedes:` understands it instantly** — the highest evidence of a field's universality.

### 2.4 Universal

The most critical criterion: **any FCoP project of sufficient scale will hit the tension of "new file taking over from an old file that can't be deleted"**.

- Task canceled mid-stream, write a new task to take over → `supersedes:` old TASK
- Report written then found to need major corrections, write a new version → `supersedes:` old REPORT (with its abort record preserved)
- Issue reopened using a new ISSUE file to continue tracking → `supersedes:` old ISSUE
- Decision (`DECISION-*`) overturned by a new decision → `supersedes:` old DECISION

Previously, all these scenarios required **manually reading the body text** to sort out relationships. With `supersedes:`, relationships **enter the metadata layer** — tools can traverse, visualize, and audit them.

All four criteria pass. `supersedes:` enters the protocol field layer.

---

## 3 · TASK-004's Pull-Back Path

Identifying the emergence is just step one. **Structurally pulling it back into the protocol** is the maintainers' job. This step corresponds to `TASK-20260512-004-ADMIN-to-ME.md`, formalizing OPS's on-the-spot field into a protocol field.

### 3.1 Field Definition in Prose

New section added to `fcop-protocol.mdc` (after "Task Format," before "Subtask Batches"):

```markdown
### `supersedes:` — File Lineage (since 2.1.0)

Optional. Value is the ID of another FCoP file (TASK-* / REPORT-* /
ISSUE-* / DECISION-*). Semantics: **this file takes over the duty
of the referenced one; the referenced file is preserved as
historical record**.

Typical usage:
- Task canceled mid-stream, write a new task to take over
- Report found to need a new version after writing; old abort report preserved
- Decision overturned by a new decision; old decision preserved as decision history

Do not use `supersedes:` to modify protocol rule files themselves —
rule files are controlled by fcop package releases; see Rule 8.
```

### 3.2 Schema Update

`spec/schemas/task.schema.json` / `report.schema.json` / `issue.schema.json` each add:

```json
{
  "properties": {
    "supersedes": {
      "type": "string",
      "pattern": "^(TASK|REPORT|ISSUE|DECISION)-\\d{8}-\\d{3}-",
      "description": "Optional file lineage anchor — points to another FCoP file this one takes over from. Added in fcop_protocol_version 2.1.0."
    }
  }
}
```

The JSON schema validator now enforces: **if `supersedes:` appears, its value must be in valid TASK/REPORT/ISSUE/DECISION ID prefix format**.

### 3.3 Tool Support

`read_task` / `read_report` / `read_issue` tools add an output section:

```text
Supersedes: REPORT-20260512-011-OPS-to-PM
└─ archived (was: status=aborted)
```

New optional `list_lineage(file_id)` tool: recursively traces `supersedes` chains, displaying the complete file inheritance tree. Especially useful for long threads / multiple revisions.

### 3.4 Version Number

`fcop_protocol_version` from `2.0.0` to `2.1.0`. SemVer rules:

| Change type | Version digit | This case |
|---|---|---|
| Breaks existing constraints | MAJOR ↑ | No (no existing fields, rules, or file structure changed) |
| Adds optional capability | MINOR ↑ | **Yes** (`supersedes:` is a new optional field) |
| Bug fix / documentation revision | PATCH ↑ | No |

So **2.0.0 → 2.1.0**, cleanly.

---

## 4 · The Complete Two-Hour Lifecycle

This was an unusually **fast** emergence → protocol path. The timeline:

| Time (UTC+8) | Event | Role |
|---|---|---|
| **16:07:39** | OPS completes commit b4ef8aa, REPORT-013 lands with `supersedes: REPORT-011` in frontmatter | OPS |
| **16:07** | OPS **proactively lists** "newly invented `supersedes:` frontmatter field" in their report | OPS |
| **16:11** | PM self-discloses #54 candidate (TASK-010 v2 §6 conflicts with stage list logic — the upstream cause of OPS hitting the supersedes dilemma) | PM |
| **16:23** | ADMIN asks: "Do these emergences ever stop? What's the endgame?" | ADMIN |
| **~16:30** | Maintainers launch 4 essay writings + 4 TASKs (TASK-004 is the supersedes pull-back) | FCoP Maintainers |
| **Future version** | `fcop@2.1.0` released, `supersedes:` formally in protocol field list | FCoP Package Maintainers |

From "OPS writes it down" to "maintainers decide to absorb," **16 minutes elapsed** (16:07 → 16:23). From "decided to absorb" to "essay draft landed," **roughly 1 more hour**. Complete lifecycle: **approximately 2 hours** (fcop package release separate).

Why does this speed matter? **Because it shows FCoP's protocol layer's reaction latency is measured in minutes, not months.** Most software protocols' evolution path is: user hits problem → files issue → weeks or months of discussion → RFC → implementation → release. FCoP compressed this chain to 2 hours.

What's the cost of this compression? **Not costless** — this speed only holds when the maintainer is **present in the session**, the agent and maintainer are in the same conversation, and the emergence itself happens to meet "the four absorption criteria." If the maintainer isn't present, or the emergence needs more examples to confirm universality, 2 hours stretches to 2 weeks. But at least FCoP demonstrated that **2 hours is a possible lower bound**.

---

## 5 · The Field Layer Is Where Emergence Lands Most Cheaply

This is the essay's core argument. Let me state it clearly:

FCoP's protocol has several layers of "ground" where emergence can land:

| Layer | Modification Cost | Typical Example | Impact on Old Projects |
|---|---|---|---|
| **Filename rules** | Very high (affects all files) | Changing `_ROLE` regex, adding new field names | Whole-project rename |
| **Directory structure** | High (affects routing) | Adding `inbox/` / `outbox/` | Old projects need migration |
| **Required fields** | High (breaks backward compatibility) | Adding required key to frontmatter | All old project frontmatters need updating |
| **Rule 0..9** | Medium-high (changes behavior) | Adding new rule / changing existing rule | Agents need to relearn |
| **Protocol commentary** | Low (just commentary) | Adding "GATE Design Pitfalls" section | Old projects can read it or not |
| **Optional fields (frontmatter)** | **Very low** | **`supersedes:` ← this essay's subject** | **Completely transparent** |
| **Tool behavior** | Low-medium (depends on whether it breaks existing CLI) | `read_task` prints one extra section | Old scripts unaffected |

**Optional fields are the cheapest class of increment in protocol evolution.** They:

- Don't touch filenames (physical protocol surface stable)
- Don't touch directories (organizational boundaries stable)
- Don't touch required fields (backward compatible)
- Don't touch rules (agent behavior unchanged — just adds **usable** expressiveness)

OPS at that crossroads **intuitively chose the lowest-cost layer in the protocol**. This wasn't coincidence — among all options available (modify REPORT-011 / delete REPORT-011 / renumber / wait for ADMIN / write "REPORT-011 was actually aborted" in the body...), `supersedes:` was the **only solution that didn't touch any other layer**.

In other words: **when an emergence can land at the "optional field" layer, maintainers should try to keep it there — don't let it escalate to the rules layer, don't let it scatter into body text, don't let it become project-specific convention**.

This is why essay 08 ("why the protocol stays short, the history grows long") has one more validation. `supersedes:` doesn't let the protocol skeleton grow — it lets the protocol skeleton **gain one very small optional leaf**. The skeleton is still short, but its expressiveness has increased.

---

## 6 · Closing · The Journey of One Line of Frontmatter

`supersedes: REPORT-20260512-011-OPS-to-PM`

This 18-character YAML line was first written on 2026-05-12 at 16:07 by a human — more precisely, an LLM agent. Two hours later, it was pulled back as a protocol field. Some time after that, it will ship with `fcop@2.1.0`, appearing in the field list of every newly installed FCoP project.

Its journey **isn't exaggerated**. It wasn't a revolutionary invention — IETF was using the same word in the 1980s. Its significance isn't "originality." It's three things:

1. **It appeared spontaneously within 5 minutes of an LLM agent hitting a wall, and its semantics perfectly match industrial standards** — showing that maintainers don't need to exhaustively pre-define every field. Some fields will be reinvented by agents under pressure.
2. **It didn't break any existing structure, landing at the cheapest layer (optional fields)** — the ideal form of protocol evolution.
3. **From emergence to protocol field took 2 hours** — pressing down by an order of magnitude what "how fast protocol evolution can happen."

> **The protocol field layer (frontmatter) is the cheapest, cleanest, and most natural landing zone for FCoP emergence.**
>
> **`supersedes:` is the first truly touchable sample of this principle. What the next sample will be, we don't yet know — but if OPS could invent a field consistent with the protocol's spirit in 5 minutes, we have reason to believe the next one will also grow from the agent's side, not be thought up by the maintainer's side.**
>
> **The maintainer's job is to recognize it, then help it land cheaply.**

— FCoP Maintainers · 2026-05-12

---

**See also**:
- Companion essay: [When Agents Learn From Their Own Wreckage](when-agents-learn-from-their-own-wreckage.en.md) — this case = §3 frontmatter emergence
- Companion essay: [Why the Protocol Stays Short](why-the-protocol-stays-short.en.md) — the argument for why the protocol stays short; this case is its proof
- Companion essay: [When the Validator Catches Itself](gate-design-pitfalls-case-studies.en.md) — another emergence from the same day worth absorbing
- Protocol clause: `fcop-protocol.mdc` "supersedes field" section (entered protocol at version 2.1.0)
- Related task: `TASK-20260512-004-ADMIN-to-ME.md` (pulling `supersedes:` back as a protocol field)
