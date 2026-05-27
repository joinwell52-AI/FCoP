# FCoP v3 Runtime Specification · Single-Page Complete Edition (3.0 → 3.2.4)

| Field | Value |
|---|---|
| **Protocol** | FCoP (Filesystem Coordination Protocol) |
| **Spec version** | **v3.2.4** (aligned with `fcop` / `fcop-mcp` PyPI **3.2.4**) |
| **Rules frontmatter** | `fcop_rules_version` / `fcop_protocol_version`: **3.2.3** ([CHANGELOG](../CHANGELOG.md)) |
| **Status** | **Current** — replaces [`fcop-3.0-spec.md`](./fcop-3.0-spec.md) as the default entry point |
| **Published** | 2026-05-27 |
| **License** | MIT |
| **ZH parallel** | [`fcop-v3-spec.zh.md`](./fcop-v3-spec.zh.md) (informative) |
| **Frozen baseline** | [`fcop-3.0-spec.md`](./fcop-3.0-spec.md) (2026-05-21; **no** `history/` layer) |

> **Conformance:** Implementations claiming **FCoP v3.2.x** MUST satisfy every **MUST** clause in this document.  
> **FCoP 3.0.0-only** claims remain governed by [`fcop-3.0-spec.md`](./fcop-3.0-spec.md) (no `history/` requirement).

---

## §0 · Core declarations

### §0.1 · Layer 1 · Cognitive guide

> **Files carry protocol. Paths address state. Events replay transitions.**

### §0.2 · Layer 2 · Semantic ontology

| | English | Section |
|---|---|---|
| 1 | Files externalize protocol semantics. | §6 |
| 2 | Paths address state. | §2 (`_lifecycle/`), §4 (`history/` terminal archive) |
| 3 | Events are replayable evidence of state transitions. | §3 |
| 4 | Governance verdicts live in `reviews/`, orthogonal to `_lifecycle/review/`. | §5 |

### §0.3 · Scope

FCoP is **not** an agent runtime, workflow engine, or orchestration kernel. See [ADR-0038](../adr/ADR-0038-fcop-boundary-charter.md).

### §0.4 · Version matrix

| Label | Meaning |
|---|---|
| **Spec 3.0.0** | Frozen 2026-05-21: `_lifecycle/` + `transitions:` only — [`fcop-3.0-spec.md`](./fcop-3.0-spec.md) |
| **Spec 3.2.x (this doc)** | 3.0 + **v3.1 lifecycle MCP** + **v3.2.0 `history/` deep archive** |
| **`fcop` package** | PyPI release; **3.2.4** is primarily a wheel encoding fix — **no new protocol semantics** |
| **Rules frontmatter** | **3.2.3** in bundled `.mdc` files |

---

## §1 · Terminology: repository root vs FCoP workspace root

Implementations resolve the **FCoP workspace root** via `fcop.lifecycle.find_workspace_root()`, not necessarily the Git repository root:

| Candidate (priority order) | Notes |
|---|---|
| `<repo>/fcop/` | **v1.0+ default** (this repository) |
| `<repo>/docs/agents/` | 0.7.x legacy layout |

All paths below are relative to **workspace root** (`<fcop-workspace>/`):

```
<repository>/
├── fcop/                        ← ★ typical FCoP workspace root
│   ├── fcop.json
│   ├── _lifecycle/              ← §2 state layer
│   ├── history/                   ← §4 deep archive (v3.2.0+)
│   ├── reports/
│   ├── issues/
│   ├── shared/
│   └── reviews/
├── workspace/<slug>/            ← Rule 7.5 (soft)
└── .cursor/rules/
```

**Common mistake:** diagrams that place `_lifecycle/` at the repository root describe the special case where workspace root **equals** repo root. In this repo, the truth is **`fcop/_lifecycle/`** (`src/fcop/lifecycle/state.py`, `src/fcop/project.py`).

---

## §2 · State layer (NOW truth · `_lifecycle/`)

### 2.1 Topology (v3 **MUST**)

Under **workspace root**:

```
<fcop-workspace>/
├── _lifecycle/
│   ├── inbox/
│   ├── active/
│   ├── review/
│   ├── done/
│   └── archive/
├── reports/
├── issues/
└── shared/
```

All five `_lifecycle/` subdirectories MUST share a **single mount point**.  
v2-only `tasks/` and `log/` MUST NOT coexist with a complete v3 `_lifecycle/` tree (**MIXED** topology).

### 2.2 Stages (frozen · ADR-0035)

| Stage | Meaning |
|------|---------|
| `inbox` | created |
| `active` | claimed |
| `review` | pending confirmation |
| `done` | completed |
| `archive` | closed (coordination archive, not yet deep history) |

### 2.3 Allowed `_lifecycle/` transitions

| From | To | L1 tool | Since |
|----|----|---------|-------|
| — | `inbox` | `create_task` / `write_task` | 3.0 |
| `inbox` | `active` | `claim_task` | **3.1.0** |
| `active` | `review` | `submit_task` | **3.1.0** |
| `active` | `done` | `finish_task` | **3.1.0** |
| `review` | `done` | `approve_task` | **3.1.0** |
| `review` | `active` | `reject_task` | **3.1.0** |
| `done` | `archive` | `archive_task` | 3.0 |

No other `_lifecycle/` transitions are permitted.

**End-to-end (informative, including deep archive):**

```
inbox → active → review → done → archive → history/YYYY-MM-DD/<task-stem>/
         └──── finish_task ─────────┘              ↑ archive_to_history (§4)
```

### 2.4 Core rules

**Rule A** — File path is the only **NOW** truth; MUST NOT infer `_lifecycle` stage from frontmatter.  
**Rule B** — Only L1 tools may move files between `_lifecycle/` stage directories.  
**Rule C** — Transition paths are encoded in tool calls, not driven by fields such as `risk_level`.

### 2.5 Atomicity and mount points

L1 transitions MUST use write-then-rename (see [`fcop-3.0-spec.md` §2.4](./fcop-3.0-spec.md)).

---

## §3 · Event layer (PAST trace · `transitions:`)

Every TASK under `_lifecycle/` SHOULD carry a YAML `transitions:` array (`version: 3`).

Each event MUST include: `at`, `from`, `to`, `by`, `tool`.  
Rules **E–G** match [`fcop-3.0-spec.md` §2](./fcop-3.0-spec.md): append-only; MUST NOT derive current stage by replaying events.

After a file moves into `history/`, its `transitions:` are frozen audit data — no longer **NOW** state.

---

## §4 · History deep archive (v3.2.0+ · `history/`)

### 4.1 Why a separate layer

| Layer | Path | Role | Scale |
|---|---|---|---|
| Coordination archive | `_lifecycle/archive/` | Completed tasks still on the coordination surface | Flat; **O(total tasks)** |
| **Deep archive** | `history/YYYY-MM-DD/<task-stem>/` | Read-only terminal home; task + reports co-located | **O(tasks per day)** per shard |

`archive_task` is unchanged; `history/` is an **optional deeper layer** (implementations SHOULD create `history/` on `init_*`).

### 4.2 Topology (MUST if implementing v3.2 history)

```
<fcop-workspace>/history/
└── YYYY-MM-DD/
    └── TASK-YYYYMMDD-NNN-SENDER-to-RECIPIENT/
        ├── TASK-....md
        └── REPORT-....md   (zero or more)
```

**Rule H** — Deep archive is terminal on the protocol surface: files MUST NOT re-enter `_lifecycle/` via L1 tools. Revival = new `TASK-*` with next sequence number (append-only history).

**Rule I** — Shard key `YYYY-MM-DD` MUST be the UTC date of `done_at`.

**Rule J** — `archive_to_history` MUST move the task and its paired report(s) into the same `<task-stem>/` directory.

### 4.3 L1 history tools (MUST if exposed via MCP)

| Tool | Behavior | Tier |
|------|----------|------|
| `archive_to_history` | `archive/` task + paired reports → `history/<date>/<stem>/` | L1 |
| `bulk_archive_to_history` | Batch by `done_date` | L1 |
| `list_history` | List task IDs; optional `date` filter | L0 |
| `read_history_task` | Read archived task | L0 |

Authoritative index: [`docs/mcp-tools.md` §8](../docs/mcp-tools.md).  
Reference: `Project.archive_to_history` in `src/fcop/project.py`.

---

## §5 · Other coordination dirs and governance review (not `_lifecycle` stages)

### 5.0 Directory map

| Directory | Envelope | Moves with L1? | Notes |
|---|---|---|---|
| `reports/` | `REPORT-*` | No | Execution reciprocity (Rule 6); deep archive **copies/moves** into `history/` |
| `issues/` | `ISSUE-*` | No | Blockers / risks / violations |
| `shared/` | `INSPECTION-*`, team docs | No | Standing docs may be updated in place; `INSPECTION` = protocol audit (Rule 9.6) |
| `reviews/` | `REVIEW-*` | No | **Governance audit verdict** (v1.0+, ADR-0017); see §5.2–§5.5 |
| `alerts/` (optional) | `ALERT-*` | No | Governance Alert Layer GAL (v1.3+, ADR-0031); see §5.6 |

Four IPC envelopes: `TASK` / `REPORT` / `ISSUE` / `REVIEW`. Schemas: `spec/schemas/ipc-envelope.schema.json`, `spec/schemas/review.schema.json`. Rules: bundled `fcop-rules.mdc` Rule 9, `fcop-protocol.mdc` Rule 9 Commentary.

### 5.1 Two meanings of “review” — **MUST** disambiguate

FCoP v3 uses **review** for two orthogonal concepts. Conflating them breaks directories, tools, and approval flows.

| Dimension | **A · Lifecycle stage** `_lifecycle/review/` | **B · Governance envelope** `reviews/REVIEW-*.md` |
|---|---|---|
| **What** | TASK file’s **current stage** (directory = NOW truth) | **Audit verdict** on an artefact (standalone file, no L1 move) |
| **Typical ops** | `submit_task` → `approve_task` / `reject_task` | `write_review` → (optional) `mark_human_approved` |
| **Who** | Executor submits; leader / ADMIN approves or rejects task | `layer: governance` or `admin` writes REVIEW |
| **Rule 6** | `approve_task` does **not** replace `REPORT-*` | REVIEW does **not** replace `REPORT-*` |
| **Human gate** | `reject_task` `note` is rework text, not `needs_human` enum | `decision: needs_human` + `human_approval` (ADR-0026) |

> **Mnemonic:** **folder review = task waiting for approve/reject; file REVIEW = verdict in `reviews/`.**

Both chains **may** coexist (TASK in `_lifecycle/review/` while a `REVIEW-*` demands ADMIN sign-off), but the protocol does **not** auto-link them. Implementations MUST NOT assume one implies the other.

### 5.2 Governance `REVIEW-*` envelope (v1.0+ · ADR-0017)

**Semantics:** REVIEW is the fourth IPC envelope — a **judgment on an existing artefact**, not a new work round.

**R1 (vs REPORT)** — REVIEW is an **audit trace**; closing a TASK still requires `REPORT-*` (or a follow-up `TASK-*`), Rule 6.  
**R2 (append-only)** — MUST NOT rewrite `decision` in place; corrections append a new REVIEW with `supersedes:` (Rule 5).  
**R3 (boundary)** — `worker` MUST NOT review `governance` subjects (Rule 9.2 / ADR-0020); `write_review` calls `assert_boundary`.

#### 5.2.1 Filename grammar (**not** TASK/REPORT routing)

REVIEW does **not** use `{SENDER}-to-{RECIPIENT}`:

```
REVIEW-{YYYYMMDD}-{NNN}-{REVIEWER}-on-{subject_short}.md
```

| Segment | Meaning |
|---|---|
| `{REVIEWER}` | Role code of the reviewer |
| `{subject_short}` | Short slug for the subject (**not** full `subject_ref`) |

`subject_ref` in frontmatter points at the full ID (e.g. `TASK-20260510-003-ADMIN-to-DEV`). `write_review` may derive `subject_short` from `subject_ref`.

#### 5.2.2 Frontmatter (**MUST** for REVIEW)

| Field | Required | Notes |
|---|---|---|
| `protocol` | ✅ | `fcop` |
| `version` | ✅ | Envelope version (integer, currently `1`) |
| `type` | ✅ | `REVIEW` |
| `review_id` | ✅ | Matches filename stem |
| `subject_type` | ✅ | `task` \| `report` \| `role_switch` \| `code_change` |
| `subject_ref` | ✅ | Subject ID (usually `TASK-*` / `REPORT-*`) |
| `reviewer_role` | ✅ | Reviewer role code |
| `decision` | ✅ | See §5.2.3 |
| `decided_at` | ✅ | ISO-8601 timestamp |
| `sender` | ✅ | Same as `reviewer_role` (IPC convention) |
| `reviewer_agent` | optional | Session / agent instance |
| `rationale` | recommended | SHOULD for `rejected` / `needs_changes` / `needs_human` |
| `required_changes` | conditional | **MUST** be non-empty when `decision=needs_changes` |
| `human_approval` | conditional | Written by `mark_human_approved` after human sign-off |

Body: Markdown with rationale and citations (Rule 0.c).

#### 5.2.3 `decision` enum (v1.1 frozen · ADR-0025)

Tool and `review.schema.json` **MUST** use these strings:

| Value | Meaning |
|---|---|
| `approved` | Pass / may proceed |
| `rejected` | Reject; do not continue as proposed |
| `needs_changes` | Requires changes; **MUST** pair with non-empty `required_changes` |
| `abstained` | Recusal / out of scope |
| `needs_human` | **Escalate to human**; pending until `human_approval` |

`pending` is **not** a valid `decision` value.

> Bundled `fcop-rules.mdc` Rule 9.1 may use teaching labels like `changes_requested` / `blocked`. **On-disk and MCP validation** follow this table and `spec/schemas/review.schema.json`.

### 5.3 Human approval loop (`needs_human` · ADR-0026)

When `decision: needs_human`:

1. Related work **SHOULD** pause in governance terms until the loop closes (host-specific enforcement).
2. Agents **MUST NOT** change `needs_human` to `approved` directly.
3. Only **`mark_human_approved(review_id, ...)`** (admin layer / human delegate) **appends** `human_approval` to mark resolution.

**Typical flow (informative):**

```
write_task(risk_level="high"|"irreversible")
  → (recommended) write_review(decision="needs_human", subject_ref=<task_id>)
  → ADMIN reviews REVIEW + TASK
  → mark_human_approved(review_id, ...)
  → executor continues / write_report / approve_task (if applicable)
```

`human_approval` minimum fields (per schema): `approver`, `decision` (`approve` / `reject`), `approved_at`, `channel`.

### 5.4 `risk_level` and REVIEW (ADR-0024)

Optional TASK frontmatter `risk_level`: `low` (default) | `medium` | `high` | `irreversible`.

| `risk_level` | Expectation |
|---|---|
| `low` / `medium` | No mandatory REVIEW |
| `high` / `irreversible` | **SHOULD** pair with `write_review(decision="needs_human")`; `write_task` may auto-hint or emit REVIEW (see `fcop-mcp`) |
| `irreversible` | **SHOULD** document rollback in TASK body (Rule 7) |

`risk_level` does **not** move `_lifecycle/` directories (Rule C, §2.4).

### 5.5 Lifecycle approval vs governance REVIEW (end-to-end)

| Step | Lifecycle (§2) | Governance (this section) |
|---|---|---|
| 1 | `write_task` → `inbox/` | (optional) `risk_level` |
| 2 | `claim_task` → `active/` | — |
| 3 | Execute | (if high risk) `write_review` |
| 4a | `submit_task` → `review/` | — |
| 4b | or `finish_task` → `done/` | — |
| 5 | `approve_task` / `reject_task` | `mark_human_approved` (if `needs_human`) |
| 6 | `write_report` | — |
| 7 | `archive_task` | — |
| 8 | (optional) `archive_to_history` | — |

### 5.6 Governance signals and GAL (summary · ADR-0031)

**FCoP-Rule-G1:** `write_report` / `fcop_report` are **self-reports** in the execution domain — **not** independent governance signals. Only `write_review`, `mark_human_approved`, `fcop_check`, etc. count as independent governance perspective.

**GAL:** `fcop/alerts/ALERT-*.md` records drift (e.g. no independent verdict in 6h, critical tool without REVIEW). GAL does **not** auto-block writes. Tools: `fcop_list_alerts`, `fcop_create_alert` — see [`docs/mcp-tools.md`](../docs/mcp-tools.md).

---

## §6 · Identity (filename grammar)

### 6.1 TASK / REPORT / ISSUE (routing envelopes)

```
{TYPE}-{YYYYMMDD}-{NNN}-{SENDER}-to-{RECIPIENT}(-{slug}).md
```

- `TYPE`: `TASK` | `REPORT` | `ISSUE`
- `slug`: optional; MUST start with `[a-z]` (ADR-0033); does **not** participate in routing
- Under `_lifecycle/`, TASK filenames are immutable; stage changes are **directory moves only**

### 6.2 REVIEW (governance · non-routing)

```
REVIEW-{YYYYMMDD}-{NNN}-{REVIEWER}-on-{subject_short}.md
```

See §5.2.1. `REVIEW` is **not** dispatched by `list_tasks(recipient=...)`.

---

## §7 · Custody (informative)

Same as [`fcop-3.0-spec.md` §5](./fcop-3.0-spec.md): derived read model only; no stored `custodian` field.

---

## §8 · Boundary charter (summary)

See [`fcop-3.0-spec.md` §3](./fcop-3.0-spec.md) and [ADR-0039](../adr/ADR-0039-fcop-freeze-discipline-and-runtime-absorption-era.md).

---

## §9 · Conformance

### 9.1 v3.0 (inherited)

C1–C10: [`fcop-3.0-spec.md` §6](./fcop-3.0-spec.md).

### 9.2 v3.2.x additions (when implementing `history/`)

| # | Requirement |
|---|---------------|
| C11 | `history/` with §4.2 layout on `archive_to_history` |
| C12 | Shard by UTC `done_at` date |
| C13 | MUST NOT treat `history/` files as current `_lifecycle` state |
| C14 | `list_history` / `read_history_task` are read-only |

### 9.3 v1.0+ governance / approval (when implementing `reviews/`)

| # | Requirement |
|---|---|
| C15 | `REVIEW-*` filenames per §5.2.1; stored under `reviews/` (directory may be created on first `write_review`) |
| C16 | `decision` uses §5.2.3 five values; `needs_changes` requires non-empty `required_changes` |
| C17 | `decision=needs_human` MUST NOT be treated as approved without `human_approval` |
| C18 | Closing a TASK still requires `REPORT-*`; MUST NOT use REVIEW alone for reciprocity |

### 9.4 Prohibitions

P1–P5 from 3.0 spec; plus **P6**: MUST NOT document fictional MCP tool names as normative FCoP (e.g. `search_history`, `move_to_history`).  
**P7:** Agents MUST NOT rewrite `needs_human` to `approved` without `mark_human_approved`.  
**P8:** MUST NOT conflate `_lifecycle/review/` with `reviews/REVIEW-*` (§5.1).

---

## §10 · Tool index (informative)

**45 MCP tools** in `fcop-mcp` 3.2.4 — full table in [`docs/mcp-tools.md`](../docs/mcp-tools.md).

| Category | Tools |
|---|---|
| v3 lifecycle | `claim_task`, `submit_task`, `finish_task`, `approve_task`, `reject_task` |
| Deep history | `archive_to_history`, `bulk_archive_to_history`, `list_history`, `read_history_task` |
| Task / report / issue | `create_task` / `write_task`, `write_report`, `write_issue`, `read_*`, `list_*` |
| Governance REVIEW | `write_review`, `list_reviews`, `read_review`, `mark_human_approved` |
| GAL | `fcop_list_alerts`, `fcop_create_alert` |
| Protocol inspection | `fcop_audit` (writes `shared/INSPECTION-*`, not `reviews/`) |
| Archive | `archive_task` |

See [`docs/mcp-tools.md`](../docs/mcp-tools.md) §4–§7, §9 for parameters and `decision` tables.

**§10 is informative:** tool names may grow in MINOR releases; MUST NOT change frozen semantics in §2–§5.

---

## §11 · Migration (informative)

**v2 → v3:** `python -m fcop migrate --to-v3` — see [`fcop-3.0-spec.md` §9](./fcop-3.0-spec.md).

**archive → history:** optional ops step via `archive_to_history` / `bulk_archive_to_history`; not a required state-machine edge.

---

## §12 · Spec document history

| Spec | Date | Summary |
|------|------|---------|
| 3.0.0 | 2026-05-21 | [`fcop-3.0-spec.md`](./fcop-3.0-spec.md) |
| 3.1 | 2026-05-22 | Lifecycle MCP tools ([CHANGELOG §3.1.0](../CHANGELOG.md)) |
| 3.2.0 | 2026-05-22 | `history/` deep archive ([CHANGELOG §3.2.0](../CHANGELOG.md)) |
| **3.2.4** | 2026-05-27 | **This document** — merged topology + workspace-root clarification |
| **3.2.4-rev2** | 2026-05-27 | §5 expanded: `reviews/`, two-review disambiguation, `needs_human` loop, `risk_level`, GAL summary |

---

## §13 · References

- [ADR-0035](../adr/ADR-0035-lifecycle-directory-and-tool-layers.md)  
- [ADR-0036](../adr/ADR-0036-lifecycle-event-layer.md) (**not** the history shard)  
- [ADR-0038](../adr/ADR-0038-fcop-boundary-charter.md)  
- [ADR-0017](../adr/ADR-0017-review-file-type-minimal.md) · REVIEW envelope  
- [ADR-0024](../adr/ADR-0024-task-risk-level.md) · `risk_level`  
- [ADR-0025](../adr/ADR-0025-review-needs-human.md) · `needs_human`  
- [ADR-0026](../adr/ADR-0026-review-human-approval.md) · `human_approval`  
- [ADR-0031](../adr/ADR-0031-governance-alert-layer.md) · GAL  
- [`docs/mcp-tools.md`](../docs/mcp-tools.md)  
- [`CHANGELOG.md`](../CHANGELOG.md)  

---

*FCoP v3 runtime specification · authoritative EN · aligned with fcop@3.2.4 · 2026-05-27*
