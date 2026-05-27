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

## §5 · Other coordination directories

| Directory | Envelope | Moves with L1 lifecycle? |
|-----------|----------|-------------------------|
| `reports/` | `REPORT-*` | No (fixed path; deep archive moves copies into `history/`) |
| `issues/` | `ISSUE-*` | No |
| `shared/` | team docs, `INSPECTION-*` | No |
| `reviews/` | `REVIEW-*` | No |

---

## §6 · Identity (filename grammar)

```
{TYPE}-{YYYYMMDD}-{NNN}-{SENDER}-to-{RECIPIENT}(-{slug}).md
```

`slug` is optional; MUST start with `[a-z]` (ADR-0033); does **not** participate in routing.  
Filenames are immutable; only directory position changes.

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

### 9.3 Prohibitions

P1–P5 from 3.0 spec; plus **P6**: MUST NOT document fictional MCP tool names as normative FCoP (e.g. `search_history`, `move_to_history`).

---

## §10 · Tool index (informative)

**45 MCP tools** in `fcop-mcp` 3.2.4 — full table in [`docs/mcp-tools.md`](../docs/mcp-tools.md).

Lifecycle: `claim_task`, `submit_task`, `finish_task`, `approve_task`, `reject_task`.  
History: `archive_to_history`, `bulk_archive_to_history`, `list_history`, `read_history_task`.

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

---

## §13 · References

- [ADR-0035](../adr/ADR-0035-lifecycle-directory-and-tool-layers.md)  
- [ADR-0036](../adr/ADR-0036-lifecycle-event-layer.md) (**not** the history shard)  
- [ADR-0038](../adr/ADR-0038-fcop-boundary-charter.md)  
- [`docs/mcp-tools.md`](../docs/mcp-tools.md)  
- [`CHANGELOG.md`](../CHANGELOG.md)  

---

*FCoP v3 runtime specification · authoritative EN · aligned with fcop@3.2.4 · 2026-05-27*
