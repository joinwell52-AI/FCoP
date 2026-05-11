---
protocol: fcop
version: 1
type: REPORT
sender: ME
recipient: ADMIN
ref_task: docs/agents/log/tasks/TASK-20260509-003-ADMIN-to-ME.md
date: 2026-05-09
status: done
priority: P0
subject: Materialize ADR-0015..0021 into machine-readable schema + long-form spec — done
---

# REPORT-20260509-003-ME-to-ADMIN

> Solo-mode report for `TASK-20260509-003`. Both rounds shipped, all 8 acceptance criteria met, two commits on `main`.

---

## 1 · Executive summary

`TASK-20260509-003` asked me to take the v1.0 charter (ADR-0015..0022) and turn it into:
1. **Machine-readable**: 7 JSON Schemas under `spec/schemas/`
2. **Human-readable**: one consolidated long-form spec at `spec/fcop-runtime-protocol-v1.0.md`

Both shipped. Hard scope held: nothing under `src/fcop/` was touched (that is TASK-004's work). Cross-validation passed before R1 commit, including the critical backward-compatibility check against real 0.7.x agent files.

| Round | Deliverable | Commit | Lines |
|---|---|---|---|
| R1 | 7 schemas + README + pyproject patch + TASK-003 charter | `3c35e0e` | +868 / -5 |
| R2 | `spec/fcop-runtime-protocol-v1.0.md` long-form spec + REPORT-003 + TASK-003 archive | (this) | +412 + ~250 |

---

## 2 · Acceptance check (against TASK-20260509-003 §3)

| # | Criterion | Pass? | Evidence |
|---|---|---|---|
| A1 | `spec/schemas/` exists with exactly 8 files (7 schemas + 1 README) | ✅ | `agent`, `boundary`, `encoding`, `event`, `failure`, `ipc-envelope`, `review` + README |
| A2 | Each `.schema.json` is valid JSON | ✅ | `python -c "json.load(open(p))"` ran on all 7, no errors |
| A3 | Each declares Draft 2020-12, `$id` under `https://fcop.dev/schemas/`, `version: "1.0.0"` | ✅ | Verified by `Draft202012Validator.check_schema()`; all 7 meta-OK |
| A4 | Every required field carries `description` citing originating ADR | ✅ | grep `ADR-` in spec/schemas/*.json yields 30+ matches across all 7 files |
| A5 | `spec/fcop-runtime-protocol-v1.0.md` exists with the 9-section structure | ✅ | §1 Scope · §2 Stack · §3 Abstractions · §4 Per-abstraction (×7) · §5 Invariants · §6 Reference Encoding · §7 Versioning · §8 Conformance · §9 Glossary + Appendices A/B/C |
| A6 | Long-form spec uses RFC-2119 (MUST/SHOULD/MAY) consistently and links each abstraction to schema + ADR | ✅ | 39 MUST · 8 SHOULD · 7 MAY · 64 ADR backlinks · §1.3 conformance-language declaration |
| A7 | `pyproject.toml` includes `jsonschema>=4.0,<5.0` | ✅ | Added to `dependencies` (alongside existing `pyyaml`); also fixed dead `Documentation` URL (was → `docs/fcop-standalone.en.md`, now → `docs/getting-started.en.md`) |
| A8 | REPORT-003 + TASK-003 archive + commit + push | ✅ | This commit |

**8/8 met.**

---

## 3 · Validation done before R1 commit

I wrote a throwaway `.git/schema_check.py` (now deleted) that did the following before staging anything:

```
=== TASK envelope validation against ipc-envelope.schema.json (real 0.7.x files) ===
  OK   docs/agents/log/tasks/TASK-20260427-001-ADMIN-to-ME.md
  OK   docs/agents/log/tasks/TASK-20260509-002-ADMIN-to-ME.md

=== sample REVIEW envelope via ipc-envelope.schema.json (synthetic) ===
  OK

=== full REVIEW schema, decision=needs_changes + EMPTY required_changes (must FAIL) ===
  expected-FAIL OK (1 errors)
    - required_changes: [] should be non-empty

=== Agent record validation ===
  ok_agent: PASS
  bad_agent (lowercase code): expected-FAIL OK
  bad_agent (bogus capability via cross-ref): expected-FAIL OK

=== Failure record validation ===
  ok_failure: PASS  ok_recovery: PASS  ok_session_call: PASS

=== Event validation ===
  ok_event TASK_CREATED: PASS
  bad_event ALIEN_LANDED: expected-FAIL OK
```

**The single most important line is the second one**: real 0.7.x agent-produced TASK files validate clean against the new v1.0 schema. That confirms invariant **I5** (backward compatibility within v1.x; ADR-0003).

Cross-file `$ref` resolution required a fix: I initially wrote `"$ref": "boundary.schema.json#/$defs/capabilityToken"` (relative filename), but `referencing.Registry` can only resolve absolute URIs. Switched all 5 cross-file refs to the target schema's `$id` form (`https://fcop.dev/schemas/.../v1.0.json#/$defs/...`) and re-validated. All green. The decision is documented in `spec/schemas/README.md`.

---

## 4 · Three-angle self-audit

### 4.1 Proposer (does this move v1.0 closer to ship?)

Yes. After this task, an external implementer can:
- Read `spec/fcop-runtime-protocol-v1.0.md` to learn what FCoP v1.0 IS.
- Cite `spec/schemas/*.schema.json` to make their build CI catch protocol violations.
- Run `Draft202012Validator(schema, registry=...)` against any envelope and get a deterministic verdict.

Before this task, an implementer would have had to read 8 ADRs and reverse-engineer the field set from Python dataclasses. That is no longer the path of least resistance.

### 4.2 Executor (was the work bounded?)

Yes — strictly. Two commits, ~1280 net lines added (868 R1 + ~412 R2). Zero lines under `src/fcop/`. The only `src/`-adjacent change was `pyproject.toml`'s `dependencies` list, which is metadata, not code.

One discipline call: the throwaway `.git/schema_check.py` was deleted before R1 commit because it is not a proper test (no assertion harness, no CI hook). Equivalent assertions belong in `tests/test_schemas/` and that is TASK-004's territory. Dropping it kept this task clean rather than half-shipping a test.

### 4.3 Reviewer (would I block this if a peer submitted it?)

Would-accept reasons:
1. The 7 schemas + spec are internally consistent. Every `MUST` in the spec is traceable to a schema rule or an ADR clause. Every schema's `description` is traceable to an ADR §.
2. Backward-compat verified against real files, not synthetic ones.
3. Cross-ref decision (absolute `$id` form) is documented in `spec/schemas/README.md` so future maintainers won't mis-add a relative ref.
4. `additionalProperties: false` is used surgically: closed sub-objects only; envelope root stays open. This is the rule that made 0.7.x files validate.

Would-push-back reasons:
1. The `failure.schema.json` `oneOf` discriminator uses an explicit `kind` field rather than overloading on field presence. This is verbose but unambiguous. Acceptable.
2. The `event.schema.json` `subject` is intentionally permissive (`additionalProperties: true`) — a stricter per-event-type discriminator would be safer but require 12 sub-schemas. Deferred to v1.1 if the loose form proves insufficient. Acceptable for v1.0.
3. `$id` URLs point at `https://fcop.dev/...` which is not (yet) a registered domain. Documented as "protocol identifier, not fetch URL" in `spec/schemas/README.md`. If we later register `fcop.dev`, we can serve the schemas there without changing any field.

Net verdict: I would accept.

---

## 5 · Alignment with FCoP self-rules

| Rule | Compliance |
|---|---|
| TASK before code | ✅ TASK-20260509-003 written and committed (in R1) before any schema file existed |
| REPORT after task | ✅ this file |
| Archive on done | ✅ TASK-003 moves to `log/tasks/` in this commit |
| Three-angle self-audit | ✅ §4 above |
| Atomic commits with task ref | ✅ R1 (`3c35e0e`) and R2 (this) both reference `TASK-20260509-003` |
| Spec change goes through ADR | ✅ Every spec field has an ADR backref; no spec decision was made fresh in this task |
| Hard scope guardrail | ✅ Zero lines under `src/fcop/`. The pyproject `dependencies` patch is metadata — `jsonschema` is declared but not yet imported anywhere. The first import will be in TASK-004. |

---

## 6 · What this leaves open (unchanged from REPORT-002 §6, minus what TASK-003 closed)

The 8 next-task seeds list from REPORT-002 narrows to **6 remaining**:

1. ~~TASK-003 — schemas + long-form spec~~ ✅ done in this report
2. **TASK-004** — Python API: dataclass alignment with schemas, `Project.write_review()`, `subscribe_events()`, `recover_session()`, `report_failure()`, plus `tests/test_schemas/` and `tests/test_encoding/test_contract_compliance.py`
3. **TASK-005** — `fcop migrate-workspace` CLI + `docs/agents/` detect-and-warn + `MIGRATION-1.0.md`
4. **TASK-006** — Reply to GitHub Issue #2 (governance-fields request → Deferred to v1.2+, with link to `spec/fcop-runtime-protocol-v1.0.md`)
5. **TASK-007** — `fcop deploy_rules` re-emit so `.cursor/rules/*.mdc` references the new schema files
6. **TASK-008** — v1.0.0 RC tagging + Zenodo DOI bump + release notes finalization

Recommended next-up: **TASK-004**. Schemas without a validator are just JSON; the value flows when `Project()` round-trips through them.

---

## 7 · Sign-off

```
TASK-20260509-003 — Materialize ADR-0015..0021 into machine-readable schema + long-form spec
Status: COMPLETED
Sender: ME (solo mode)
Recipient: ADMIN
Date: 2026-05-09
Commits on main: 3c35e0e (R1), (this) (R2)
```

The spec is on paper AND in JSON. Implementations now have a contract to point at. Next task makes the reference implementation actually honour it.
