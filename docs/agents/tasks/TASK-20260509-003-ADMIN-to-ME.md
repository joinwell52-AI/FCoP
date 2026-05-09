---
protocol: fcop
version: 1
type: TASK
sender: ADMIN
recipient: ME
date: 2026-05-09
priority: P0
status: in_progress
subject: Materialize ADR-0015..0021 into machine-readable schema + long-form spec
ref_charter: adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md
ref_predecessor: docs/agents/log/tasks/TASK-20260509-002-ADMIN-to-ME.md
acceptance_criteria_count: 8
---

# TASK-20260509-003-ADMIN-to-ME

> Solo-mode task. The TASK-002 reframing closed with the charter on paper (ADR-0015..0022 + READMEs + getting-started + mdc tags). The next atomic step is to **materialize that paper into a machine-readable contract** — 7 JSON Schemas + one consolidated long-form spec — so v1.0.0 implementation work has a single source of truth to point at.

---

## 1 · Background — what TASK-002 left open

REPORT-20260509-002 §6 listed 8 next-task seeds:

1. ✅ this task — `spec/schemas/*.schema.json` × 7 + long-form spec
2. ⏳ next task (TASK-004) — Python API: `Project.write_review` / `subscribe_events` / `recover_session` / `report_failure` + dataclass alignment + pytest
3. ⏳ TASK-005 — `fcop migrate-workspace` CLI + detect+warn
4. ⏳ TASK-006 — Reply to GitHub Issue #2 (governance fields → Deferred to v1.2+)
5. ⏳ TASK-007 — `fcop deploy_rules` re-emit so `.cursor/rules/*.mdc` references the new schemas
6. ⏳ TASK-008 — v1.0.0 RC tagging + Zenodo DOI bump

This TASK-003 only owns item #1. **Strict scope**: nothing in `src/fcop/` is touched. Pure `spec/` work.

The reason for splitting it out: schemas are the **contract** that all subsequent code must match. Writing schemas first lets ADR-0016's "schema is truth, dataclass is derived" rule actually apply. If we wrote dataclass first and schema second we would be deciding the contract by accident — exactly the failure mode ADR-0008 era exhibited.

---

## 2 · ADMIN decisions for TASK-003

### Decision 1 · Schema layout

7 files exactly as ADR-0016 §Decision lists:

```
spec/schemas/
├── README.md                  ← index + how-to-validate
├── agent.schema.json          ← abstraction 1: Agent (lifecycle + identity)
├── encoding.schema.json       ← abstraction 2: Encoding (filename + workspace_dir)
├── ipc-envelope.schema.json   ← abstraction 3: IPC (4 envelope types share a base)
├── event.schema.json          ← abstraction 4: Event Model
├── failure.schema.json        ← abstraction 5: Failure & Recovery
├── boundary.schema.json       ← abstraction 6: Boundary & Capability
└── review.schema.json         ← abstraction 7: Audit (REVIEW)
```

Each schema:

- JSON Schema Draft 2020-12 (`$schema: "https://json-schema.org/draft/2020-12/schema"`)
- `$id: "https://fcop.dev/schemas/{abstraction}/v1.0.json"`
- Top-level `title`, `description`, `version: "1.0.0"`, `additionalProperties: false` on closed objects
- Cross-reference siblings via relative `$ref` where it cuts duplication (e.g. boundary capabilities referenced from agent + ipc-envelope)
- Each enum / required field traceable to the originating ADR by inline `description`

### Decision 2 · Long-form spec

`spec/fcop-runtime-protocol-v1.0.md` — single normative spec consolidating ADR-0015..0022 into one readable document. **NOT** a copy-paste of ADRs; a re-organized normative spec that says "this is what FCoP v1.0 IS" — ADRs say "this is WHY we decided." Both must exist.

Structure:

1. Abstract + status block + version
2. Conformance language (RFC-2119 MUST / SHOULD / MAY)
3. The 5-layer AI OS stack diagram + FCoP's position
4. The 7 core abstractions, each as one §
5. Protocol invariants (the things implementations MUST preserve)
6. Reference Encoding (Markdown) — concrete file format
7. Versioning & stability (link to ADR-0003)
8. Conformance test surface (link to schemas)
9. Glossary

`spec/fcop-spec-v1.0.3.md` (the existing 0.7.x-era document) is **not** deleted. It stays as historical artefact + the 0.7.x conformance baseline. The new file is the v1.0 spec.

### Decision 3 · Dependency

Add `jsonschema>=4.0,<5.0` to `pyproject.toml` `dependencies` list. **Only** the dependency entry — no Python import yet (that's TASK-004's work).

### Decision 4 · Out-of-scope (do NOT do in this task)

- Python `models.*` dataclass changes
- `core/schema.py` validator implementation
- `Project.*` new methods
- `pytest` tests for schemas
- `fcop_report` CLI changes
- `MIGRATION-1.0.md` (deferred to TASK-005 alongside `migrate-workspace` CLI)
- Reply to GitHub Issue #2 (TASK-006)
- Anything in `src/fcop_mcp/`

If any of these creep in during execution, **stop and split into a follow-up TASK** — do not silently expand scope.

---

## 3 · Acceptance criteria (8)

| # | Criterion | Evidence |
|---|---|---|
| A1 | `spec/schemas/` exists with exactly 8 files (7 schemas + 1 README) | `ls spec/schemas/` |
| A2 | Each `.schema.json` is valid JSON, parseable by `python -c "import json; json.load(open(p))"` | manual sanity check |
| A3 | Each `.schema.json` declares Draft 2020-12, `$id` under `https://fcop.dev/schemas/`, `version: "1.0.0"` | grep top-level keys |
| A4 | Each schema's `description` for every field cites its originating ADR (ADR-0015..0022) | grep `"ADR-"` count > 30 |
| A5 | `spec/fcop-runtime-protocol-v1.0.md` exists with the 9-section structure listed in Decision 2 | structural read |
| A6 | Long-form spec uses RFC-2119 keywords (MUST / SHOULD / MAY) consistently and links each abstraction to its schema + ADR | grep MUST count, link audit |
| A7 | `pyproject.toml` `dependencies` includes `jsonschema>=4.0,<5.0` | grep `jsonschema` |
| A8 | REPORT-003 + TASK-003 archive + commit + push | git log shows TASK-003 closed |

---

## 4 · Execution plan (one TASK, two commits)

| Round | Deliverable | Commit |
|---|---|---|
| R1 | All 7 schemas + `spec/schemas/README.md` + `pyproject.toml` patch | `spec(schemas): freeze 7 JSON Schemas for FCoP v1.0 abstractions` |
| R2 | `spec/fcop-runtime-protocol-v1.0.md` long-form spec + REPORT-003 + TASK-003 archive | `spec: ship fcop-runtime-protocol-v1.0.md (close TASK-20260509-003)` |

Two commits, in order. R1 lands the contract; R2 lands the human-readable spec that points at the contract.

---

## 5 · Risk register

| Risk | Mitigation |
|---|---|
| Schemas drift from ADR text | Inline `description` on every field cites ADR §; spec doc cross-links the schema files |
| Spec doc becomes a copy of ADRs | Use different voice — ADR = "we decided X because Y"; spec = "implementations MUST do X". No "we" in spec |
| `additionalProperties: false` is too strict and breaks 0.7.x files | Use `additionalProperties: false` ONLY on closed sub-objects; envelope frontmatter root uses `additionalProperties: true` so 0.7.x extra fields stay legal |
| `$id` URL doesn't resolve (fcop.dev not registered) | Acceptable in v1.0 — `$id` is a protocol identifier, not a fetch URL. Document this in `spec/schemas/README.md` |
| Long-form spec turns into 2000 lines | Cap at ~600 lines; details live in ADRs and schemas; spec is the **normative summary** |

---

## 6 · Three-angle pre-flight check (proposer / executor / reviewer)

### Proposer (does this task move v1.0 closer to ship?)

Yes. Without machine-readable schemas, no implementation can claim conformance. Without a long-form spec, downstream consumers (CodeFlow v2, third-party host adapters) can't cite a single document. This task closes the "charter exists but is unenforceable" gap.

### Executor (is the work bounded?)

Yes. Hard scope boundary: nothing in `src/`. Two commits. ~600 + ~7×80 ≈ 1200 lines total. Doable in one session.

### Reviewer (would I block this if a peer submitted it?)

Would-block conditions to watch for during execution:
- Any schema with no `description` on required fields → block
- Any spec section without an ADR backref → block
- `additionalProperties: false` on the root envelope → block (breaks 0.7.x compat)
- Long-form spec exceeding 800 lines → block (means ADR content was duplicated)

If executor catches itself doing any of those, **stop and split**.

---

## 7 · Sign-off

```
Sender:    ADMIN
Recipient: ME (solo mode)
Status:    in_progress
Opened:    2026-05-09
Charter:   ADR-0015 §execution roadmap step 1 (machine-readable spec)
```

Begin execution immediately. R1 first.
