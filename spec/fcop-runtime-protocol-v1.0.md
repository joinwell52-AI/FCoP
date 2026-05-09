# FCoP Agent Runtime Protocol — v1.0

| | |
|---|---|
| **Status** | Draft (frozen for v1.0 implementation; ratification on v1.0.0 tag) |
| **Version** | 1.0.0 |
| **Date** | 2026-05-09 |
| **Charter** | [ADR-0015](../adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md) |
| **Predecessor** | [`spec/fcop-spec-v1.0.3.md`](./fcop-spec-v1.0.3.md) (0.7.x baseline; preserved as legacy artefact) |
| **Machine-readable contract** | [`spec/schemas/`](./schemas/) (7 JSON Schemas) |
| **License** | MIT |

---

## Abstract

FCoP — the **F**ile-based **Co**ordination **P**rotocol — is the **AI OS protocol layer**: the agent runtime contract for filesystem-based collaboration. It occupies the same position in the AI OS stack that **POSIX** occupies in Unix, **OCI** in container ecosystems, and **CRD** in Kubernetes.

This document is the **normative specification** for FCoP v1.0. It freezes the minimum semantic contract for **seven core abstractions** — Agent, Encoding, IPC, Event, Failure, Boundary, Audit — that any conforming implementation MUST satisfy.

> **FCoP is the protocol of agents. We discovered it; we did not invent it. It happens that humans can read it too.** — [ADR-0015 §FCoP is discovered, not invented](../adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md#fcop-is-discovered-not-invented)

### 摘要（简体中文）

FCoP（**F**ile-based **Co**ordination **P**rotocol）是 **AI OS 协议层**——agent 在共享文件系统上协作的运行时契约。它在 AI OS 栈中的位置等同于 Unix 中的 **POSIX**、容器生态中的 **OCI**、Kubernetes 中的 **CRD**。

本文是 **FCoP v1.0 的规范性说明**，将七大核心概念——**Agent、Encoding、IPC、Event、Failure、Boundary、Audit**——的最小语义契约正式固化为稳定标准，任何合规实现都必须满足。

> 「FCoP 是 agent 的协议，我们发现了他，而不是发明；而正好人类可以读懂。」——[ADR-0015 §FCoP is discovered, not invented](../adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md#fcop-is-discovered-not-invented)

> **本规范以英文为权威版本**（normative）；中文段落仅作摘要参考，与英文不一致时以英文为准。完整中文翻译请见 [`docs/getting-started.md`](../docs/getting-started.md)（L0+L1 入口）+ [ADR-0015 中文章程](../adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md)。

---

## §1 · Scope, status, conformance

### 1.1 What this document is

This is the **single normative spec** for FCoP v1.0. ADRs (`adr/ADR-NNNN-*.md`) record *why* each decision was made and supersede each other across protocol versions; this spec records *what* an implementation MUST do today.

When an ADR and this spec disagree about *what* the protocol requires, **this spec wins**. When this spec and a JSON Schema in [`spec/schemas/`](./schemas/) disagree about *what fields exist*, **the schema wins** ([ADR-0016 §decision](../adr/ADR-0016-json-schema-for-7-abstractions.md)).

### 1.2 What this document is NOT

- Not a tutorial — see [`docs/getting-started.md`](../docs/getting-started.md).
- Not a decision log — see [`adr/`](../adr/).
- Not a reference implementation guide — see `src/fcop/` and its README.
- Not the 0.7.x spec — that is preserved verbatim at [`spec/fcop-spec-v1.0.3.md`](./fcop-spec-v1.0.3.md) for legacy conformance tests.

### 1.3 Conformance language

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL** in this document are to be interpreted as described in [BCP 14, RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) and [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174) when, and only when, they appear in all capitals.

### 1.4 Conformance levels

A FCoP **v1.0-conforming implementation** MUST satisfy every MUST in §3 through §6 below.

A FCoP **v1.0-conforming implementation MAY** offer additional capabilities beyond what this spec requires; such extensions:

- MUST NOT change the meaning of any v1.0 conformance requirement
- MUST NOT introduce a 5th IPC envelope type
- MUST NOT introduce a new `decision` value for REVIEW (the 4-value enum is frozen for v1.0)
- SHOULD be documented as implementation-specific extensions

---

## §2 · The AI OS stack — where FCoP lives

```
┌─────────────────────────────────────────────────────────────────┐
│  Application Layer       CodeFlow / Cursor / Claude Desktop    │
│                          (business products built on agents)   │
├─────────────────────────────────────────────────────────────────┤
│  Host Adapter Layer      fcop-mcp / fcop-cli / @fcop/claude    │
│                          (libc-equivalent: bridges hosts to    │
│                          the protocol)                         │
├─────────────────────────────────────────────────────────────────┤
│ ★ FCoP Protocol Layer ★  Agent / IPC / Encoding / Event /      │
│  (THIS SPECIFICATION)    Failure / Boundary / Audit            │
│                          (POSIX-equivalent: the contract)      │
├─────────────────────────────────────────────────────────────────┤
│  Reference Implementation `fcop` (Python library)              │
│                          (v1.0 ships exactly one impl)         │
├─────────────────────────────────────────────────────────────────┤
│  Kernel Primitives       LLM API / Filesystem / Process Mgr    │
│                          (the AI OS kernel — out of scope)     │
└─────────────────────────────────────────────────────────────────┘
```

This spec defines **only the starred line**. Implementations and applications built on top of FCoP are out of scope; they are constrained only by the contracts this spec exposes.

---

## §3 · The seven core abstractions

The following table summarizes the seven abstractions and their POSIX analogues. The detailed contract for each appears in §4.

| # | Abstraction | POSIX analogue | Schema | Source ADR |
|---|---|---|---|---|
| 1 | **Agent** (lifecycle + identity) | Process | [`agent.schema.json`](./schemas/agent.schema.json) | [ADR-0020](../adr/ADR-0020-agent-boundary-and-capability.md) |
| 2 | **Encoding** (IPC + Open Knowledge surfaces) | Filesystem | [`encoding.schema.json`](./schemas/encoding.schema.json) | [ADR-0021](../adr/ADR-0021-encoding-abstraction.md) + [ADR-0022](../adr/ADR-0022-workspace-directory-convention.md) |
| 3 | **IPC** (4 envelope types) | pipes / message queues | [`ipc-envelope.schema.json`](./schemas/ipc-envelope.schema.json) | [ADR-0017](../adr/ADR-0017-review-file-type-minimal.md) + 0.7.x baseline |
| 4 | **Event** (12 derived events) | signals | [`event.schema.json`](./schemas/event.schema.json) | [ADR-0018](../adr/ADR-0018-event-model.md) |
| 5 | **Failure & Recovery** | errno + signal handler | [`failure.schema.json`](./schemas/failure.schema.json) | [ADR-0019](../adr/ADR-0019-failure-and-recovery-semantics.md) |
| 6 | **Boundary & Capability** | permissions | [`boundary.schema.json`](./schemas/boundary.schema.json) | [ADR-0020](../adr/ADR-0020-agent-boundary-and-capability.md) |
| 7 | **Audit** (REVIEW) | syslog | [`review.schema.json`](./schemas/review.schema.json) | [ADR-0017](../adr/ADR-0017-review-file-type-minimal.md) |

---

## §4 · Per-abstraction contracts

### §4.1 Abstraction 1 — Agent

An **Agent** is an autonomous participant in an FCoP project. It has stable identity (a `code`), a layer (`worker` | `governance` | `admin`), and a capability bundle.

A conforming implementation MUST:

- A1.1 Treat the role `code` (uppercase, 1–16 chars matching `^[A-Z][A-Z0-9]{0,15}$`) as the routing key in IPC envelope filenames. The human-readable `label` MUST NOT be used for routing.
- A1.2 Reject programmatic creation of an Agent with `layer: "admin"`. The `admin` layer is reserved for human operators.
- A1.3 When an Agent record specifies `can` and/or `cannot`, treat those lists as authoritative. The `layer`-default capability bundle (per §4.6) applies only when `can` and `cannot` are both absent or empty.
- A1.4 Surface the `session_id` (when present) as `<task_id>:<agent_code>` in the reference implementation. Other implementations MAY use other forms but MUST keep the identifier stable across `recover_session` calls.

The full schema is at [`agent.schema.json`](./schemas/agent.schema.json).

### §4.2 Abstraction 2 — Encoding

The **Encoding** abstraction has **two surfaces** ([ADR-0021](../adr/ADR-0021-encoding-abstraction.md)). Both share a common `workspace_dir` contract.

**IPC Surface (strong contract).** A conforming implementation MUST:

- A2.1 Recognize exactly four IPC envelope types: `TASK`, `REPORT`, `ISSUE`, `REVIEW`. Adding a fifth is a MAJOR-version protocol change.
- A2.2 Match envelope filenames against the patterns in [`encoding.schema.json#/$defs/ipcSurface/properties/filename_grammar`](./schemas/encoding.schema.json). Date is `YYYYMMDD`; sequence is 3-digit zero-padded and monotonic per-day.
- A2.3 Require `protocol`, `version`, `type`, `sender` in the frontmatter of every envelope. Per-envelope schemas (see §4.3) add more required fields.

**Open Knowledge Surface (weak contract).** A conforming implementation MUST:

- A2.4 Permit any filename matching `^[A-Z][A-Z0-9-]*-[a-z0-9-]+(\.[a-z]{2,5})?\.md$` under `<workspace_dir>/shared/`. The PREFIX vocabulary is open: implementations MUST NOT reject a PREFIX for being absent from any list.
- A2.5 Treat frontmatter as OPTIONAL on the Open Knowledge Surface.
- A2.6 NOT enumerate or normatively recommend any specific PREFIX vocabulary. The list `GUIDE / SPEC / STATUS / TEAM / LETTER / MEMO / RECIPE / ARCHIVE` in `encoding.schema.json#/$defs/openKnowledgeSurface/properties/informative_observed_prefixes` is **informative only** and exists to aid documentation tools. A conforming implementation MUST NOT use this list as a validation gate.

> **Why two surfaces?** Field evidence shows agents — without any spec guidance — converge on a small set of PREFIXes for ad-hoc shared documents. Excluding `shared/` from the protocol would exclude 50%+ of real-world agent output. Enumerating the PREFIXes in spec would ossify agent creativity. Two surfaces resolves the tension. See [ADR-0021 §why two surfaces](../adr/ADR-0021-encoding-abstraction.md#why-two-surfaces).

**Workspace directory.** A conforming implementation MUST:

- A2.7 Default `workspace_dir` to `fcop/` ([ADR-0022](../adr/ADR-0022-workspace-directory-convention.md)).
- A2.8 Detect a legacy `docs/agents/` workspace and emit a deprecation warning. The implementation MAY offer one-shot migration via a tool (the reference implementation provides `fcop migrate-workspace`, deferred to TASK-005).
- A2.9 Allow alternative encoding implementations to register, provided they satisfy this abstraction's contract. v1.0 ships exactly one concrete encoding (`MarkdownEncoding`); see §6.

### §4.3 Abstraction 3 — IPC

The four IPC envelope types share a common base; each adds type-specific required fields. The full schema is at [`ipc-envelope.schema.json`](./schemas/ipc-envelope.schema.json).

| Envelope | Required (beyond base) | Filename pattern |
|---|---|---|
| **TASK** | `recipient`, `subject` | `TASK-{date}-{seq}-{from}-to-{to}.md` |
| **REPORT** | `recipient`, `ref_task`, `status` | `REPORT-{date}-{seq}-{from}-to-{to}.md` |
| **ISSUE** | `subject` | `ISSUE-{date}-{seq}-{from}.md` |
| **REVIEW** | `subject_type`, `subject_ref`, `decision` | `REVIEW-{date}-{seq}-{from}-on-{subject}.md` |

A conforming implementation MUST:

- A3.1 Treat the per-envelope `status` (TASK / REPORT) as belonging to the enum `pending | accepted | in_progress | blocked | done | aborted`. The value `aborted` is added by [ADR-0019](../adr/ADR-0019-failure-and-recovery-semantics.md) and is REQUIRED in v1.0.
- A3.2 Permit unknown additional frontmatter keys at the envelope root (`additionalProperties: true`). This preserves 0.7.x backward compatibility per [ADR-0003](../adr/ADR-0003-stability-charter.md).
- A3.3 When a REPORT references a TASK, set `ref_task` to the **path** of the TASK file (not its frontmatter `subject`).
- A3.4 When an envelope omits `type` (legacy 0.7.x files), the implementation SHOULD infer `type` from the filename PREFIX before validation.

### §4.4 Abstraction 4 — Event

FCoP v1.0 events are **derived from filesystem state changes**; there is **no** `EVENT-*.md` envelope type ([ADR-0018](../adr/ADR-0018-event-model.md)).

A conforming implementation MUST:

- A4.1 Recognize exactly twelve event types ([`event.schema.json#/$defs/eventType`](./schemas/event.schema.json)):
  - **From task / report / review state changes**: `TASK_CREATED`, `TASK_ACCEPTED`, `TASK_BLOCKED`, `TASK_COMPLETED`, `REPORT_FILED`, `REVIEW_DECIDED`
  - **From boundary / role changes**: `BOUNDARY_VIOLATED`, `ROLE_SWITCHED`
  - **From failure / recovery handling** (per [ADR-0019](../adr/ADR-0019-failure-and-recovery-semantics.md)): `FAILURE_DETECTED`, `RECOVERY_INITIATED`, `RECOVERY_COMPLETED`, `SESSION_LOST`
- A4.2 Expose at least one mechanism by which an application can subscribe to events (the reference implementation offers `Project.subscribe_events(types, callback)`; host adapters MAY surface this as MCP tools, WebSockets, file watchers, etc.).
- A4.3 Emit each event at most once per source state change. Implementations SHOULD dedupe identical events arising from a single filesystem operation.
- A4.4 Guarantee monotonic timestamp ordering **within a single agent**. Cross-agent happens-before is OUT OF SCOPE for v1.0; if needed, applications MUST layer their own causality on top.

A conforming implementation MAY:

- A4.5 Persist an event log (e.g. to `<workspace_dir>/log/events/`). v1.0 does not require persistence.

### §4.5 Abstraction 5 — Failure & Recovery

A real runtime is defined not by its happy path but by how anomalies survive. v1.0 freezes **four failure modes** and **five recovery actions**.

| Failure | Triggered when… |
|---|---|
| `TIMEOUT` | An agent does not deliver before its TASK's `timeout_at` |
| `CRASH` | A reference impl or host adapter exits abnormally |
| `DEADLOCK` | Two or more agents wait on each other's outputs |
| `DRIFT` | An agent's output does not match the TASK contract |

| Recovery | Effect |
|---|---|
| `RETRY` | Same agent redoes same TASK |
| `RESUME` | Load session state and continue from interruption |
| `ROLLBACK` | `git revert` to pre-TASK file state |
| `ABORT` | Mark TASK status `aborted`, do not redo |
| `ESCALATE` | Lift to next governance layer (default: `leader` from `fcop.json`) |

A conforming implementation MUST:

- A5.1 Reject any failure record whose `failure_type` is not one of the four; reject any recovery whose `recovery_action` is not one of the five.
- A5.2 Pair every applied recovery with the failure that triggered it (correlation field: `trigger_failure_id`).
- A5.3 Provide a `recover_session(session_id, action)` API that supports at least the three actions `resume`, `rollback`, `abort`. (`RETRY` and `ESCALATE` are caller-side scheduling decisions, not session-state operations.)
- A5.4 Emit `FAILURE_DETECTED`, `RECOVERY_INITIATED`, `RECOVERY_COMPLETED` events as the corresponding records are written (per §4.4).

A conforming implementation SHOULD:

- A5.5 NOT enforce a particular Failure→Recovery mapping at the protocol layer. Mappings are implementation-defined; e.g. one impl may auto-RETRY on TIMEOUT, another may auto-ESCALATE.

### §4.6 Abstraction 6 — Boundary & Capability

Agents have explicit capability boundaries. v1.0 freezes a **10-token capability vocabulary** and **four boundary rules**.

**Capability vocabulary (frozen at 10):**

`file_io`, `task_io`, `modify_code`, `review_decision`, `approve_release`, `escalate`, `spawn_agent`, `override`, `archive`, `mark_done`

See [`boundary.schema.json#/$defs/capabilityToken`](./schemas/boundary.schema.json) for per-token semantics.

**Layer defaults (informative — overridable per Agent):**

| Layer | Default `can` | Default `cannot` |
|---|---|---|
| `worker` | `file_io`, `task_io` | `approve_release`, `escalate`, `spawn_agent` |
| `governance` | `file_io`, `task_io`, `review_decision` | `modify_code`, `spawn_agent` |
| `admin` | `file_io`, `task_io`, `review_decision`, `escalate`, `override` | (none — but `admin` MUST NOT appear in `fcop.json`) |

**Boundary rules (all MUST be enforced before any write op):**

- B1 `NO_ADMIN_PROGRAMMATIC_CREATE` — Implementations MUST reject any attempt to create an Agent with `layer: "admin"` programmatically.
- B2 `NO_GOVERNANCE_FISSION` — A `governance`-layer Agent MUST NOT spawn other Agents.
- B3 `NO_WORKER_REVIEWS_GOVERNANCE` — A `worker`-layer Agent's REVIEW of a `governance`-layer Agent's output MUST be rejected.
- B4 `EXPLICIT_OVERRIDES_LAYER` — When an Agent has explicit `can`/`cannot`, those lists take precedence over the layer-default bundle.

A conforming implementation MUST emit a `BOUNDARY_VIOLATED` event when any of B1–B4 fires.

### §4.7 Abstraction 7 — Audit (REVIEW)

REVIEW is a governance-layer decision about an artefact. v1.0 ships the **minimal surface only** ([ADR-0017](../adr/ADR-0017-review-file-type-minimal.md)).

A conforming implementation MUST:

- A7.1 Recognize exactly four `decision` values: `approved`, `rejected`, `needs_changes`, `abstained`. Adding a fifth (e.g. `needs_human`) is a MINOR-version change that **MUST NOT** happen before v1.2 per [ADR-0015 §non-goals](../adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md).
- A7.2 Reject a REVIEW with `decision: needs_changes` and an empty (or absent) `required_changes` list.
- A7.3 Recognize four `subject_type` values: `task`, `report`, `role_switch`, `code_change`.
- A7.4 NOT implement `Project.mark_human_approved()`, `human_approval` sub-objects, admin-layer manual_file_edit guards, or any other v1.2-deferred feature in a v1.0-conforming way.

A conforming implementation MAY:

- A7.5 Store REVIEWs in `<workspace_dir>/reviews/` and archive them to `<workspace_dir>/log/reviews/` on close.

---

## §5 · Protocol invariants

Implementations MUST preserve the following across all operations:

- **I1 · Filename atomicity** — A file IS its routing. Renaming `tasks/TASK-X.md` to `log/tasks/TASK-X.md` IS the state transition `TASK_COMPLETED`. Implementations MUST treat `os.rename()` (or its equivalent) as the single sync primitive within a mount point. No locks, no brokers.
- **I2 · Filesystem-as-single-source-of-truth** — Implementations MUST NOT maintain a hidden state store that disagrees with the filesystem. If a UI shows a TASK as `done` but the file is still in `tasks/`, the file wins.
- **I3 · Schema is the contract** — When in-process dataclasses and `spec/schemas/*.schema.json` disagree, the schema wins. Implementations SHOULD have a CI check enforcing this ([ADR-0016](../adr/ADR-0016-json-schema-for-7-abstractions.md)).
- **I4 · Open Knowledge Surface stays open** — Implementations MUST NOT reject a `<workspace_dir>/shared/` file solely because its PREFIX is unknown.
- **I5 · Backward compatibility within v1.x** — A file written by a v1.0-conforming implementation MUST remain valid against any v1.x-conforming implementation. v1.x changes are additive only ([ADR-0003](../adr/ADR-0003-stability-charter.md)).

---

## §6 · Reference Encoding (Markdown + YAML frontmatter)

v1.0 ships exactly one concrete encoding implementation: `MarkdownEncoding` ([ADR-0021](../adr/ADR-0021-encoding-abstraction.md)).

### 6.1 File format

Every IPC envelope is a UTF-8 text file with the following structure:

```
---
<YAML frontmatter>
---

<Markdown body>
```

- Frontmatter MUST be YAML 1.2-compatible.
- Body MUST be Markdown (CommonMark, no required dialect extension).
- File MUST have extension `.md`.

### 6.2 Filesystem layout

```
<project root>/
└── fcop/                      ← workspace_dir (default per ADR-0022)
    ├── fcop.json              ← team / role config
    ├── tasks/                 ← active TASK-*.md
    ├── reports/               ← active REPORT-*.md
    ├── issues/                ← active ISSUE-*.md
    ├── reviews/               ← active REVIEW-*.md (v1.0; created on first REVIEW)
    ├── shared/                ← Open Knowledge Surface — agent invention
    └── log/                   ← archive
        ├── tasks/
        ├── reports/
        ├── issues/
        └── reviews/
```

### 6.3 Alternative encodings

A v1.x-conforming alternative encoding (e.g. JSON / SQLite / event-stream) MUST:

- Implement the contract in [`encoding.schema.json`](./schemas/encoding.schema.json).
- Be losslessly convertible to/from `MarkdownEncoding` for both surfaces (IPC and Open Knowledge).
- Register with `Project(encoding=...)` (the reference implementation exposes this constructor parameter).

v1.0 does NOT ship any alternative encoding. The constructor parameter exists to avoid breaking the API when v1.x adds one.

---

## §7 · Versioning & stability

FCoP follows Semantic Versioning per [ADR-0003](../adr/ADR-0003-stability-charter.md). For protocol changes:

| Change | SemVer | Cooling period |
|---|---|---|
| Add new optional field, new enum value, new schema file | MINOR (e.g. 1.0 → 1.1) | None — additive |
| Make optional field required, remove field, change type | **MAJOR (e.g. 1.x → 2.0)** | ≥ 6 months coexistence + official migration tool |
| Tighten regex / pattern | **MAJOR (e.g. 1.x → 2.0)** | Same as above |
| Change behavior of existing API without changing signature | PATCH (e.g. 1.0.0 → 1.0.1) | None — must be bug fix only |

The PyPI package family ([ADR-0015 §terminology](../adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md#%E6%9C%AF%E8%AF%AD%E8%A1%A8v10-%E6%B0%B8%E4%B9%85%E5%86%BB%E7%BB%93)):

| Package | Role | v1.0 version |
|---|---|---|
| `fcop` | Reference Implementation (this protocol) | 1.0.0 |
| `fcop-mcp` | Host Adapter for MCP-capable hosts | 1.0.0 |
| `fcop-cli` | Host Adapter for command line | (v1.x candidate) |

A protocol-level v1.0.0 release tag corresponds to all of `fcop` and `fcop-mcp` simultaneously crossing 1.0.0.

### §7.1 Stability of the seven core concepts (normative)

The phrase **"the seven core concepts — Agent, Encoding, IPC, Event, Failure, Boundary, Audit — are stabilised for the v1.x major series"** (Chinese: *七大核心概念已固化*) appears throughout this spec, the README, the release notes, and `docs/MIGRATION-1.0.md`. This sub-section is the single normative source; all other documents MUST refer here rather than restate the meaning.

**Scope of the freeze.** The following properties of every abstraction in §3–§6 are frozen for the entire v1.x major series:

1. The set of fields defined for each envelope / event / failure / recovery / boundary / agent / encoding contract.
2. The type of each field (string vs integer vs enum vs array vs object).
3. The set of legal values for each enum (e.g. `EventType` has 12 values; `Failure.kind` has 4; `Recovery.action` has 5; `Review.decision` has 4).
4. The semantics of each field (the meaning a conforming implementation MUST attach to it).
5. The filename grammar defined in §6.2 (`{TYPE}-{YYYYMMDD}-{NNN}-{SENDER}-to-{RECIPIENT}.md`).

**Forbidden changes during v1.x.** A conforming implementation MUST NOT:

- delete an existing field from any contract above;
- change the type of an existing field;
- remove a value from an existing enum;
- change the semantics of an existing field while keeping its name;
- tighten the filename grammar (regex narrowing).

Any of the above requires a MAJOR bump to v2.0, which itself MUST satisfy the three hard requirements in the SemVer table above (RFC + ≥ 6 months coexistence + official migration tool) per [ADR-0015 §SemVer](../adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md) and [ADR-0003 §Stability charter](../adr/ADR-0003-stability-charter.md).

**Allowed changes during v1.x (additive expansion).** A conforming implementation MAY, in any MINOR release:

- add a new optional field with a default value (old consumers ignore it);
- add a new enum value where adding it cannot break existing consumers (e.g. a new `EventType` value extends discriminated dispatch but does not invalidate existing dispatch arms);
- add a new schema file for a new abstraction extension;
- add new public API methods on `fcop.Project` and new MCP tools on `fcop-mcp` (per the same additive rule).

A conforming implementation MAY, in any PATCH release, fix bugs in the reference implementation provided no observable behaviour visible through the v1.x contract changes.

**Frozen ≠ stagnant.** What is frozen is the **contract surface** above, not the **implementation**. The reference implementation (`fcop` Python library), the host adapter (`fcop-mcp`), the schemas (additive), the documentation, the tutorials, the performance, and the bug-fix posture remain free to evolve throughout v1.x. The analogy is the POSIX `read()` syscall: the signature has not changed in decades while the Linux kernel implementation evolves continuously.

**What "permanent" means.** "Permanent" in this spec means: for the lifetime of the v1.x major series (1.0.0 through 1.99.99). Beyond v1.x, the freeze is broken only by a MAJOR bump as specified above; v1.x and v2.x MUST coexist for at least 6 months and an official migration tool MUST ship before v1.x can be deprecated.

> **中文释义（informative）**：七大核心概念（Agent、Encoding、IPC、Event、Failure、Boundary、Audit）在整个 v1.x 大版本（1.0.0 到 1.99.99）期间已正式固化——上述 5 项属性（字段集 / 字段类型 / 枚举值集合 / 字段语义 / 文件名 grammar）禁止变动；想变动只能 MAJOR bump 到 v2.0，且 v2.0 自带"协议级 RFC + v1/v2 共存 6 个月 + 官方迁移脚本"三条硬要求。**允许**的是 additive expansion（加可选字段 / 加新枚举值 / 加新 schema / 加新公开方法）走 MINOR；**实现**层面（refactor / 性能 / bug fix / 文档 / 教程）整个 v1.x 完全自由演进——概念固化 ≠ 停滞，类比 POSIX `read()` syscall 几十年 signature 不变但 Linux kernel 实现一直演化。

---

## §8 · Conformance test surface

A v1.0-conforming implementation SHOULD pass the test suite at `tests/test_schemas/` and `tests/test_encoding/test_contract_compliance.py` in this repository. Per [ADR-0016 §tests](../adr/ADR-0016-json-schema-for-7-abstractions.md), each abstraction's schema has at least three test cases: legal example, missing-required-field example, illegal-enum-value example.

**Backward compatibility witness**: every TASK / REPORT / ISSUE / REVIEW file under `docs/agents/log/` in this repository (which contains real 0.7.x agent output) MUST validate against [`spec/schemas/ipc-envelope.schema.json`](./schemas/ipc-envelope.schema.json) after the legacy field-mapping in [`spec/schemas/README.md`](./schemas/README.md). This is the canonical regression test for I5.

---

## §9 · Glossary

| Term | Definition |
|---|---|
| **Agent** | An autonomous participant in a project, identified by an uppercase role `code`. |
| **AI OS** | The conceptual stack of (Application, Host Adapter, FCoP Protocol, Reference Implementation, Kernel Primitives) that lets agents collaborate. FCoP is the protocol layer of this stack. |
| **Audit** | The protocol abstraction realized by REVIEW. The syslog-equivalent of FCoP. |
| **Boundary** | The set of capabilities an Agent has. |
| **Capability** | A token from the v1.0 vocabulary (`file_io`, `task_io`, …) representing one allowed action. |
| **Encoding** | The protocol abstraction that defines how IPC envelopes and Open Knowledge documents are stored on disk. v1.0 ships `MarkdownEncoding`. |
| **Envelope** | A typed message: TASK, REPORT, ISSUE, or REVIEW. |
| **Event** | A typed signal derived from filesystem state changes. v1.0 has 12 event types. |
| **Failure** | One of `TIMEOUT`, `CRASH`, `DEADLOCK`, `DRIFT`. |
| **FCoP** | File-based Coordination Protocol — the AI OS protocol layer. This document. |
| **Host Adapter** | The libc-equivalent layer: bridges a specific host (Cursor, Claude Desktop, command line) to FCoP. |
| **IPC Surface** | The strong-contract surface of Encoding: the 4 envelope types. |
| **Open Knowledge Surface** | The weak-contract surface of Encoding: agent-invented PREFIXes under `shared/`. |
| **Recovery** | One of `RETRY`, `RESUME`, `ROLLBACK`, `ABORT`, `ESCALATE`. |
| **Reference Implementation** | The `fcop` Python library shipped from this repository. |
| **REVIEW** | The 4th IPC envelope type, added in v1.0; encodes a governance decision. |
| **Schema** | A JSON Schema file in [`spec/schemas/`](./schemas/) defining the field contract for an abstraction. |
| **Workspace dir** | The protocol namespace directory inside a host project. v1.0 default: `fcop/`. v0.7.x legacy: `docs/agents/`. |

---

## Appendix A · Differences from `spec/fcop-spec-v1.0.3.md` (the 0.7.x baseline)

| Area | 0.7.x | v1.0 |
|---|---|---|
| Framing | "File-based collaboration protocol" | "AI OS protocol layer" |
| Abstractions | Implicit (5 dataclasses: Agent, Task, Review*, Session, Skill) | Explicit (7 named abstractions) |
| Schema | None (dataclasses are truth) | 7 JSON Schemas (schemas are truth) |
| Workspace dir | `docs/agents/` | `fcop/` (with detect-and-warn for legacy) |
| Envelope types | 3 (TASK, REPORT, ISSUE) | 4 (+ REVIEW) |
| Open Knowledge Surface | Implicit (agents wrote `shared/` files but no contract) | Explicit (separate surface, no PREFIX enumeration) |
| Event Model | Absent | 12 derived events |
| Failure Model | Absent | 4 modes × 5 recoveries |
| Boundary Model | `Agent.layer` only | `layer` + `can` + `cannot` + 10-token vocabulary + 4 rules |
| Stability charter | Pre-1.0 (breaking allowed in MINOR) | v1.0 charter ([ADR-0003](../adr/ADR-0003-stability-charter.md) + [ADR-0015](../adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md)) |

> *0.7.x had a `Review` dataclass but no REVIEW envelope file type — Review was an in-memory annotation on Task. v1.0 elevates it to a first-class file type.

---

## Appendix B · Authoritative document map

| File | Role |
|---|---|
| `spec/fcop-runtime-protocol-v1.0.md` | **This document — the v1.0 normative spec** |
| `spec/schemas/*.schema.json` | Machine-readable field contracts |
| `spec/schemas/README.md` | Schema index, conformance language, validation snippet |
| `spec/fcop-spec-v1.0.3.md` | Frozen 0.7.x baseline (legacy conformance only) |
| `adr/ADR-0001..0006` | Pre-1.0 architectural decisions |
| `adr/ADR-0015` | v1.0 charter |
| `adr/ADR-0016..0022` | Per-abstraction implementation ADRs |
| `adr/ADR-0007..0014` | Superseded / deferred (preserved for history) |
| `docs/getting-started.md` (+ `.en.md`) | L0 + L1 entry point (tutorial; not normative) |

---

## Appendix C · Acknowledgements

FCoP was extracted from field deployments rather than designed in committee. The v1.0 charter ([ADR-0015](../adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md)) records the "discovered, not invented" philosophy in detail. Specific field reports that shaped this spec:

- `essays/when-ai-organizes-its-own-work.md` — 6 coordination patterns invented by agents in 48 hours
- `essays/fcop-natural-protocol.md` — an agent endorsing FCoP rules unprompted
- `essays/when-ai-vacates-its-own-seat.md` — agents completing an unwritten part of the protocol under conflict
- `essays/what-agents-say-about-fcop.md` — agents directly asked
- `docs/tutorials/snake-solo-to-duo.zh.md` and `tetris-solo-to-duo.en.md` — 45-minute hands-on dogfoods that produced, among other things, the first observed `STATUS-*-RECORD.md` agent invention

The Open Knowledge Surface (§4.2) exists because of those last two files.
