# FCoP Agent Runtime Protocol — v1.1

| | |
|---|---|
| **Status** | **Ratified** — v1.1 additive extension, backward-compatible with v1.0 |
| **Version** | 1.1.0 |
| **Date** | 2026-05-11 |
| **Charter** | [ADR-0023](../adr/ADR-0023-agent-layer-governance-field.md) · [ADR-0024](../adr/ADR-0024-task-risk-level.md) · [ADR-0025](../adr/ADR-0025-review-needs-human.md) · [ADR-0026](../adr/ADR-0026-review-human-approval.md) · [ADR-0027](../adr/ADR-0027-skill-tools-risk-metadata.md) |
| **Predecessor** | [`spec/fcop-runtime-protocol-v1.0.md`](./fcop-runtime-protocol-v1.0.md) |
| **Machine-readable contract** | [`spec/schemas/`](./schemas/) (8 JSON Schemas) |
| **Bundled rules** | `fcop-rules.mdc` v2.2.0 · `fcop-protocol.mdc` v2.0.0 |
| **Reference impl** | `fcop>=1.1.0` · `fcop-mcp>=1.1.0` (current: `1.2.1`, lockstep) |

---

## Scope

This document records the **v1.1 protocol changes** relative to
[`spec/fcop-runtime-protocol-v1.0.md`](./fcop-runtime-protocol-v1.0.md).

v1.1 is a **MINOR additive release** under the FCoP stability charter
([ADR-0003](../adr/ADR-0003-stability-charter.md)). Every v1.0 rule,
schema, and tool remains valid. All changes are opt-in additions — no
existing frontmatter field, file, or tool call breaks.

---

## Summary of Changes

| ADR | Change | Schema impact |
|---|---|---|
| [ADR-0023](../adr/ADR-0023-agent-layer-governance-field.md) | `Agent.layer` runtime governance contracts | `ipc-envelope.schema.json` (role object) |
| [ADR-0024](../adr/ADR-0024-task-risk-level.md) | `Task.risk_level` field (4-level enum) | `ipc-envelope.schema.json` (task shape) |
| [ADR-0025](../adr/ADR-0025-review-needs-human.md) | `Review.decision = needs_human` (5th enum value) | `review.schema.json` |
| [ADR-0026](../adr/ADR-0026-review-human-approval.md) | `Review.human_approval` sub-object | `review.schema.json` |
| [ADR-0027](../adr/ADR-0027-skill-tools-risk-metadata.md) | `Skill.tools[]` risk metadata per tool | `skill.schema.json` |

New MCP tools in `fcop-mcp 1.1.0`: `write_review`, `list_reviews`,
`read_review`, `mark_human_approved`. Extended tool: `write_task`
gains `risk_level` parameter.

---

## Detailed Changes

### 1. Agent.layer — Governance Hierarchy Field (ADR-0023)

`fcop.json` role objects may now carry a `layer` field:

```json
{
  "code": "PM",
  "label": "Project Manager",
  "layer": "governance"
}
```

**Three-tier hierarchy:**

| Layer | Description | Constraints |
|---|---|---|
| `worker` | Execution roles (DEV, QA, OPS, ME …) | Cannot review `governance` subjects |
| `governance` | Decision roles (PM, LEAD-*, PLANNER …) | Cannot create new `governance` roles (NO_GOVERNANCE_FISSION) |
| `admin` | Top-level authority | Programmatic creation requires explicit override (NO_ADMIN_PROGRAMMATIC_CREATE) |

`layer` is optional and defaults to `worker` when absent. It is a
**runtime contract** — agents must self-check their layer before
sensitive operations and emit `BOUNDARY_VIOLATED` + write an `ISSUE-`
on violation.

---

### 2. Task.risk_level — Operation Risk Classification (ADR-0024)

Tasks may carry an optional `risk_level` frontmatter field:

```yaml
---
protocol: fcop
version: 1
sender: PM
recipient: OPS
risk_level: high        # ← new in v1.1
subject: Restart production service
---
```

**Four-level enum:**

| Value | Meaning | Auto-trigger |
|---|---|---|
| `low` | Standard operation (default) | — |
| `medium` | Elevated attention, suggest rollback plan | Soft reminder |
| `high` | Human approval required before execution | Auto-writes `REVIEW (decision=needs_human)` |
| `irreversible` | Cannot be undone (prod data delete, public release…) | Auto-writes REVIEW + must include rollback plan |

When `write_task` receives `risk_level=high` or `irreversible`, it
automatically creates a companion REVIEW with `decision=needs_human`.
The task executor MUST NOT proceed until `mark_human_approved` is
called on that REVIEW.

---

### 3. Review.decision = needs_human (ADR-0025)

The `decision` enum in `review.schema.json` expands from 4 to **5 values**:

```
approved | changes_requested | blocked | rejected | needs_human
```

`needs_human` semantics:
- The reviewing agent has determined that **human judgment is required**.
- The subject task/report is **frozen** — no agent may proceed with
  execution until ADMIN approves via `mark_human_approved`.
- `needs_human` is **not** a temporary placeholder; it is a hard gate.
- Agents must never overwrite `needs_human` with another decision
  value without human intervention.

---

### 4. Review.human_approval Sub-object (ADR-0026)

When `decision = needs_human`, the REVIEW file may carry an optional
`human_approval` block in its YAML frontmatter:

```yaml
decision: needs_human
human_approval:
  approved_by: "alice@example.com"
  approved_at: "2026-05-11T09:00:00+08:00"
  note: "Confirmed with security team. Proceed."
```

**Flow:**

```
1. Agent calls write_task(risk_level="high")
   → TASK-*.md created (risk_level: high)
   → REVIEW-*.md created (decision: needs_human)

2. ADMIN reviews and approves:
   → calls mark_human_approved(review_id="REVIEW-*.md")
   → human_approval block written
   → decision transitions to approved (human-delegated)

3. Executor reads updated REVIEW → proceeds with task
```

The `human_approval` block is **write-once**: once an approval is
recorded, the REVIEW file becomes an immutable audit record.

---

### 5. Skill.tools[] Risk Metadata (ADR-0027)

`skill.schema.json` now allows each tool entry in the `tools[]` array
to carry risk metadata:

```yaml
tools:
  - name: deploy_to_production
    description: "Deploys the built artifact to the production server"
    risk_level: high
    requires_human_approval: true
    side_effects: "Modifies live traffic routing; partial rollback possible via load balancer"
  - name: run_tests
    description: "Runs the full test suite"
    risk_level: low
    requires_human_approval: false
```

**Fields (all optional):**

| Field | Type | Description |
|---|---|---|
| `risk_level` | string (4-level enum) | Inherits the same values as `Task.risk_level` |
| `requires_human_approval` | bool | When true, callers should gate with `write_task(risk_level=high/irreversible)` before invoking |
| `side_effects` | string | Human-readable description of non-reversible side effects |

This metadata is **machine-readable** and intended for orchestration
frameworks to make automated approval decisions.

---

## Schema Changes

### `review.schema.json`

- `decision` enum extended from 4 to 5 values: added `needs_human`.
- New optional property: `human_approval` (object with
  `approved_by` string, `approved_at` datetime string, `note` string).
- `human_approval` is **not required** even when `decision=needs_human`
  (the block is only present after `mark_human_approved` is called).

### `ipc-envelope.schema.json`

- TASK shape: new optional `risk_level` property (4-value string enum).
- Agent/role shape: new optional `layer` property
  (`worker` | `governance` | `admin`).

### `skill.schema.json`

- `tools[]` array items: new optional properties `risk_level`,
  `requires_human_approval`, `side_effects`.

---

## New MCP Tools (fcop-mcp 1.1.0)

| Tool | Description |
|---|---|
| `write_review(subject_id, decision, reviewer, body)` | Create a REVIEW envelope; use `decision=needs_human` to gate human approval |
| `list_reviews(decision=None, subject_id=None)` | List REVIEW files, optionally filtered |
| `read_review(review_id)` | Read a single REVIEW file by ID |
| `mark_human_approved(review_id, approved_by, note)` | Record human approval on a `needs_human` REVIEW |

Extended tool:

| Tool | Added parameter |
|---|---|
| `write_task(...)` | `risk_level: str = ""` — when `high` or `irreversible`, auto-creates companion REVIEW |

Full parameter reference: [`docs/mcp-tools.md`](../docs/mcp-tools.md).

---

## Backward Compatibility

v1.1 is **fully backward-compatible** with v1.0:

- All existing TASK / REPORT / ISSUE / REVIEW files remain valid.
- `risk_level` is optional; absent means `low`.
- `human_approval` is optional even when `decision=needs_human`.
- `layer` in `fcop.json` is optional; absent defaults to `worker`.
- `Skill.tools[]` risk fields are optional.
- No existing MCP tool signature changed (only additive parameters).
- Projects at v1.0 do not need to migrate; they gain v1.1 features by
  opting in (using the new fields and tools).

---

## References

- [`spec/fcop-runtime-protocol-v1.0.md`](./fcop-runtime-protocol-v1.0.md) — base protocol
- [`adr/ADR-0023..0027`](../adr/) — individual change rationale
- [`docs/mcp-tools.md`](../docs/mcp-tools.md) — full MCP tool index (30 tools, 14 resources)
- [`docs/releases/1.1.0.md`](../docs/releases/1.1.0.md) — release notes
