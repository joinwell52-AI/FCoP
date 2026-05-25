# Getting Started with FCoP

> **FCoP** = **F**ile-based **Co**ordination **P**rotocol — the **behavior governance protocol layer**.
>
> "FCoP is the protocol of agents. We discovered it; we did not invent it. It happens that humans can read it too."
> — [ADR-0015 §FCoP is discovered, not invented](../adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md#fcop-is-discovered-not-invented)

This is the **L0 + L1 single entry point** — get FCoP in 30 seconds, run it on your machine in 5 minutes. Reading this page is enough; deeper docs in [`spec/`](../spec/) / [`adr/`](../adr/) / [`essays/`](../essays/) are optional.

> **✅ `fcop-mcp` is on the [official MCP Registry](https://registry.modelcontextprotocol.io/)** ([`io.github.joinwell52-AI/fcop`](https://registry.modelcontextprotocol.io/v0/servers?search=io.github.joinwell52-AI%2Ffcop), **v3.2.3**). Backed by **Anthropic + GitHub + Microsoft** — Claude Desktop, Cursor, PulseMCP, and every MCP client can discover **45 tools** and install with one line: `uvx fcop-mcp`.

---

## 30 seconds: what FCoP is

**FCoP is the behavior governance protocol layer** for agent collaboration — governing agent behavior, not scheduling tasks. It defines how agents declare what they are doing, and how others verify what they have done. Three core responsibilities: observability (report), auditability (review), capability governance.

```
┌─────────────────────────────────────────────────────────┐
│  Application       CodeFlow / Cursor / Claude Desktop   │  ← business products
├─────────────────────────────────────────────────────────┤
│  Host Adapter      fcop-mcp / fcop-cli / @fcop/claude   │  ← protocol bridge adapters
├─────────────────────────────────────────────────────────┤
│ ★ FCoP Protocol ★  Agent collaboration / behavior       │  ← this is FCoP
│                    report / Review /                    │
│                    Capability Governance / Audit        │
├─────────────────────────────────────────────────────────┤
│  Reference Impl    fcop (Python lib)                    │  ← reference implementation
├─────────────────────────────────────────────────────────┤
│  Execution         LLM APIs / MCP Tools / Filesystem /  │  ← agent execution env
│  Substrate         OS (FCoP governs behavior,           │
│                       does not own this layer)          │
└─────────────────────────────────────────────────────────┘
```

The starred line is FCoP. **Not application, not execution substrate, not any host's SDK** — it's the convention agents *naturally develop* when collaborating, formalized into a machine-readable spec.

Human readability is a **side effect**: the substrate happens to be filesystem + Markdown, so you can open VSCode and watch what agents are doing. But FCoP is not designed *for* humans — it's designed for agents; humans get to watch for free.

> CodeFlow makes things happen. FCoP makes things happen *lawfully*.

---

## What makes FCoP bigger than traditional protocols: two Encoding Surfaces

FCoP's Encoding has **two faces** (the core of [ADR-0021](../adr/ADR-0021-encoding-abstraction.md)):

### Surface 1 · IPC Surface (strong contract)

Four envelope types, defined by spec, strict filenames, required frontmatter:

| Type | Filename pattern | Purpose |
|---|---|---|
| **TASK** | `TASK-{date}-{seq}-{from}-to-{to}.md` | Assignment |
| **REPORT** | `REPORT-{date}-{seq}-{from}-to-{to}.md` | Worker self-status |
| **ISSUE** | `ISSUE-{date}-{seq}-{from}.md` | Block / reflection |
| **REVIEW** | `REVIEW-{date}-{seq}-{from}-on-{subject}.md` | Governance decision (new in v1.0) |

POSIX analogy: pipes / message queues — strongly structured, explicit sender→recipient.

### Surface 2 · Open Knowledge Surface (weak contract)

The naming language agents **invent freely** in `shared/`. Spec only requires the filename form `{ALL-CAPS-PREFIX}-{kebab-slug}[.{lang}].md`; **the PREFIX is invented by agents — FCoP spec does not enumerate**.

Real agent inventions observed in production FCoP projects:

| Prefix | Meaning |
|---|---|
| `GUIDE-{topic}.md` | How-to / operational guide |
| `SPEC-{topic}.md` | Team-level convention |
| `STATUS-{actor}-{topic}-RECORD.md` | Cross-task status ledger |
| `TEAM-{aspect}.md` | Team-layer doc (README / ROLES / OPERATING-RULES) |
| `LETTER-TO-{recipient}.md` | Cross-session open communication |

**None of these are defined in spec** — agents grew them under the spirit of FCoP's filename grammar. POSIX analogy: shared memory / `/usr/share/` — weakly structured, namespace open.

This face is what makes FCoP more alive than traditional message protocols (JSON-RPC / gRPC / MQ): the spec leaves room, agents invent sub-languages.

---

## 5 minutes: running it

### Step 1 · Install

```bash
pipx install fcop-mcp        # host adapter (pulls in fcop lib)
# or library only (no MCP):
# pipx install fcop
```

PyPI package family ([ADR-0015 §Terminology](../adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md)):

| Package | Role | Required |
|---|---|---|
| `fcop` | Reference Implementation | ✅ |
| `fcop-mcp` | Host Adapter for Cursor / any MCP host | ✅ (when using Cursor / Claude Desktop) |
| `fcop-cli` (v1.x candidate) | Host Adapter for command line | ⏳ |

### Step 2 · Init in your project root

```bash
cd your-project
fcop init                    # creates fcop/ namespace
```

The directory layout (v1.0 default):

```
your-project/
└── fcop/                          ← v1.0 protocol namespace
    ├── fcop.json                  ← team / role config
    ├── tasks/                     ← TASK-* lives here
    ├── reports/                   ← REPORT-*
    ├── issues/                    ← ISSUE-*
    ├── reviews/                   ← REVIEW-* (new in v1.0)
    ├── shared/                    ← Open Knowledge Surface — agents invent freely
    └── log/                       ← archive (completed TASK/REPORT moved here)
```

> **Upgrading from 0.7.x?** Legacy `docs/agents/` is detected and triggers a warning. Run `fcop migrate-workspace --apply` for a one-shot move to `fcop/` (uses `git mv` to preserve history). See [ADR-0022](../adr/ADR-0022-workspace-directory-convention.md).

### Step 3 · Write your first TASK

`fcop/tasks/TASK-20260601-001-PM-to-DEV.md`:

```markdown
---
protocol: fcop
version: 1
sender: PM
recipient: DEV
priority: P1
subject: Add dark mode toggle to homepage
---

## Background
...

## Acceptance criteria
- [ ] Toggle button in header right
- [ ] localStorage persistence
```

### Step 4 · Agent picks it up and reports

DEV-role agent scans its inbox:

```python
from fcop import Project

project = Project(".")              # reads fcop/ by default
my_inbox = project.inbox(role="DEV")
for task in my_inbox:
    print(task.subject)             # "Add dark mode toggle to homepage"
    # ... do the work ...
    project.write_report(
        task=task,
        status="done",
        body="Implemented, commit abc1234"
    )
```

The REPORT lands at `fcop/reports/REPORT-20260601-001-DEV-to-PM.md`.

### Step 5 · Invent freely in shared/

Need a guide spanning multiple tasks? Just invent:

```bash
fcop/shared/GUIDE-dark-mode-implementation-notes.md
```

This is the Open Knowledge Surface — **no one taught the agent to use the `GUIDE-` prefix**, but agents will invent similar conventions on their own (field evidence in [ADR-0021](../adr/ADR-0021-encoding-abstraction.md)). Your project's agents may invent `MEMO-` / `RECIPE-` / `ARCHIVE-` etc.; all legal.

---

## The seven core abstractions

[ADR-0015 charter](../adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md) defines the FCoP protocol body as 7 abstractions (POSIX analogies):

| FCoP abstraction | POSIX analogy | Detail ADR |
|---|---|---|
| **Agent** (lifecycle + identity) | Process | [ADR-0020](../adr/ADR-0020-agent-boundary-and-capability.md) |
| **Encoding** (IPC + Open Knowledge) | Filesystem | [ADR-0021](../adr/ADR-0021-encoding-abstraction.md) |
| **IPC** (4 envelope types) | pipes / MQ | [ADR-0017](../adr/ADR-0017-review-file-type-minimal.md) + existing |
| **Event Model** | signals | [ADR-0018](../adr/ADR-0018-event-model.md) |
| **Failure & Recovery** | errno | [ADR-0019](../adr/ADR-0019-failure-and-recovery-semantics.md) |
| **Boundary** (can / cannot) | permissions | [ADR-0020](../adr/ADR-0020-agent-boundary-and-capability.md) |
| **Audit** (REVIEW) | syslog | [ADR-0017](../adr/ADR-0017-review-file-type-minimal.md) |

Each abstraction is closed by its own ADR; protocol-level schemas live in [`spec/schemas/`](../spec/schemas/).

---

## v1.1 additions: human-in-the-loop risk gates

v1.1 adds three opt-in features on top of the v1.0 base. Nothing breaks;
use them when your workflow needs human sign-off before high-risk actions.

### Task.risk_level

```python
from fcop import Project

project = Project(".")
project.write_task(
    recipient="OPS",
    subject="Delete old production backups",
    body="...",
    risk_level="irreversible",   # new in v1.1
)
# ↑ automatically creates a companion REVIEW (decision=needs_human)
# The OPS agent must not proceed until ADMIN approves.
```

Four levels: `low` (default) / `medium` / `high` / `irreversible`.
`high` and `irreversible` auto-create a `needs_human` review gate.

### needs_human review + mark_human_approved

```python
# ADMIN checks pending approvals:
reviews = project.list_reviews(decision="needs_human")

# ADMIN approves:
project.mark_human_approved(
    review_id=reviews[0].review_id,
    approved_by="alice@example.com",
    note="Confirmed with infra team.",
)
# Now the OPS agent may proceed.
```

### Skill.tools[] risk metadata

```yaml
# In a skill file — machine-readable risk declaration
tools:
  - name: deploy_to_prod
    risk_level: high
    requires_human_approval: true
    side_effects: "Modifies live traffic routing"
```

Orchestration frameworks read `requires_human_approval: true` and
automatically gate through the `write_task(risk_level=high)` flow.

Full reference: [`spec/fcop-3.0-spec.md`](../spec/fcop-3.0-spec.md) (canonical FCoP 3.0).

---

## What FCoP doesn't solve

Honestly:

- **Sub-millisecond latency** — filesystem-based protocols have second-scale latency, **not for** HFT or real-time control
- **Strong-consistency transactions** — no multi-file transactions; handle transactional semantics at the content layer
- **Million-file single repos** — large-scale single-project scans get slow; partition by date/batch
- **Orchestration / Task Scheduling** — FCoP governs behavior, it does not schedule tasks; Task Scheduler / State Machine / Event Loop belong to the reference impl or application layer

**FCoP's sweet spot**: 10–100 agents, second-to-minute coordination cycles, scenarios where humans need to step in to review/audit at any time.

---

## Authoritative sources (by abstraction layer)

| Layer | File | Role |
|---|---|---|
| L0 + L1 entry | [`docs/getting-started.en.md`](./getting-started.en.md) (this page) | 30-second + 5-minute |
| L2 canonical spec | [`spec/fcop-3.0-spec.md`](../spec/fcop-3.0-spec.md) | ★ Single-page canonical (FCoP 3.0) |
| L2 RFC projection | [`spec/fcop-3.0-rfc.md`](../spec/fcop-3.0-rfc.md) | IETF-style RFC edition |
| L2 historical | [`spec/archived/`](../spec/archived/) | v1.0 / v1.1 / 0.7.x drafts (superseded) |
| L2 agent-readable rules (Cursor) | [`.cursor/rules/fcop-rules.mdc`](../.cursor/rules/fcop-rules.mdc) + [`fcop-protocol.mdc`](../.cursor/rules/fcop-protocol.mdc) | Cursor host — `alwaysApply: true` |
| L2 agent-readable rules (others) | [`AGENTS.md`](../AGENTS.md) / [`CLAUDE.md`](../CLAUDE.md) | Codex / Claude Code / Devin / generic SDK |
| L2 machine-readable | [`spec/schemas/*.schema.json`](../spec/schemas/) (8 schemas in v1.1) | JSON Schema × 7+1 abstractions |
| L3 stories | [`essays/`](../essays/) | Field reports & notes |
| Decision history | [`adr/`](../adr/) (ADR-0001..0027) | Why we did things |

> **`src/fcop/rules/_data/` is the canonical source.** `deploy_protocol_rules()` (or MCP `redeploy_rules()`) syncs it to `.cursor/rules/*.mdc` (Cursor) and `AGENTS.md` / `CLAUDE.md` (other hosts). See [ADR-0006](../adr/ADR-0006-host-neutral-rule-distribution.md).

---

## Further reading

- **Protocol philosophy**: [ADR-0015 §FCoP is discovered, not invented](../adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md#fcop-is-discovered-not-invented)
- **Field report**: [`essays/when-ai-organizes-its-own-work.md`](../essays/when-ai-organizes-its-own-work.md) — 48 hours, 6 collaboration patterns invented spontaneously
- **Agent self-notes**: [`docs/tutorials/`](./tutorials/) — tutorials with real agent-produced TASK/REPORT excerpts
- **GitHub**: <https://github.com/joinwell52-AI/FCoP>

---

## FAQ

## fcop_audit Three-Scenario Health Check (v1.3+)

`fcop_audit()` is FCoP's built-in protocol health check tool — it lets an agent
discover compliance gaps on its own.

### Scenario 1: New project self-check (`scope="new"`)

```python
# Immediately after init_project / init_solo:
fcop_audit(scope="new")
# or write to file:
fcop_audit(scope="new", output="file")
```

Checks: role documents present, `fcop.json` correct, basic envelope format valid.

### Scenario 2: Upgrade verification (`scope="upgrade"`)

```python
# After pip install -U fcop:
fcop_audit(scope="upgrade")
```

Checks: local protocol rule version consistent with package version; old formats
requiring migration.

### Scenario 3: Project takeover (`scope="takeover"`)

```python
# First action when inheriting an unfamiliar project:
fcop_audit(scope="takeover", output="file")
```

Checks: full compliance scan (misplaced envelopes / legacy roles / cursor rules
etc.), produces `INSPECTION-*.md` with P0/P1/P2-tiered remediation suggestions.

### Output format

- Default: stdout (console summary)
- `output="file"`: writes to `fcop/shared/INSPECTION-{date}-{NNN}-{scope}.md`
- Report includes an `Execution Block` with copy-paste commands for remediation

> **Note**: `fcop_audit()` is **read-only** — it does not modify any files.
> The INSPECTION report is advisory, not an instruction.

---

**Q: How is FCoP related to MCP?**
A: Orthogonal. MCP is the agent ↔ tool call protocol; FCoP is the agent ↔ agent communication protocol. They stack (fcop-mcp uses MCP to expose FCoP tools to Cursor).

**Q: Can it work across machines / projects?**
A: Yes. Simplest: use git / Syncthing / Dropbox to sync the `fcop/` directory. Serious: put the whole project in git; `git pull/push` is your sync.

**Q: Will the protocol change?**
A: From v1.0, FCoP enters behavior governance protocol layer stability — MAJOR (1.x→2.x) only allows breaks with ≥6-month coexistence + an official migration tool; MINOR is additive only; PATCH is zero behavioral change. See [ADR-0003](../adr/ADR-0003-stability-charter.md) + [ADR-0015 §Freeze #4](../adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md).

**Q: Why not JSON-RPC / gRPC / MQ?**
A: They're **agent-only** protocols — humans can't see or modify them. FCoP's substrate is filesystem + Markdown — humans and agents see the same world. This is the "human-machine isomorphism" essays talk about.

**Q: If an agent wants to invent a prefix in shared/, do they need to ask first?**
A: **No.** This is the core constraint of Open Knowledge Surface — the spec doesn't enumerate the vocabulary; agents invent (just respect the `{ALL-CAPS-PREFIX}-{kebab-slug}.md` grammar). If you spot a new prefix you find interesting, log it in the §observed agent inventions section of release notes — but don't put it in spec.

---

[中文版本 / Chinese version](./getting-started.md)
