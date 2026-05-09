# `spec/schemas/` — FCoP machine-readable contract

> **Single source of truth** for the FCoP v1.0 protocol. Per [ADR-0016](../../adr/ADR-0016-json-schema-for-7-abstractions.md): when these schemas and any Python dataclass disagree, **the schemas win**. CI in TASK-004 (next) will enforce this.

## What lives here

| File | Abstraction | Source ADR | What it covers |
|---|---|---|---|
| `agent.schema.json` | 1 · Agent | [ADR-0020](../../adr/ADR-0020-agent-boundary-and-capability.md) | Lifecycle + identity (`code`, `label`, `layer`, `can`, `cannot`, `session_id`) |
| `encoding.schema.json` | 2 · Encoding | [ADR-0021](../../adr/ADR-0021-encoding-abstraction.md) + [ADR-0022](../../adr/ADR-0022-workspace-directory-convention.md) | IPC Surface + Open Knowledge Surface + `workspace_dir` contract |
| `ipc-envelope.schema.json` | 3 · IPC | [ADR-0017](../../adr/ADR-0017-review-file-type-minimal.md) + 0.7.x baseline | Shared envelope base + 4 envelope types (TASK / REPORT / ISSUE / REVIEW) |
| `event.schema.json` | 4 · Event | [ADR-0018](../../adr/ADR-0018-event-model.md) + [ADR-0019](../../adr/ADR-0019-failure-and-recovery-semantics.md) | 12 event types derived from filesystem state changes |
| `failure.schema.json` | 5 · Failure | [ADR-0019](../../adr/ADR-0019-failure-and-recovery-semantics.md) | 4 failure modes × 5 recovery actions + Session recovery hook |
| `boundary.schema.json` | 6 · Boundary | [ADR-0020](../../adr/ADR-0020-agent-boundary-and-capability.md) | 10-token capability vocabulary + 4 boundary rules |
| `review.schema.json` | 7 · Audit | [ADR-0017](../../adr/ADR-0017-review-file-type-minimal.md) | REVIEW envelope (minimal surface — no `needs_human` until v1.2+) |

## Conformance

- **Draft**: JSON Schema **2020-12** (`$schema: https://json-schema.org/draft/2020-12/schema`)
- **`$id`**: `https://fcop.dev/schemas/{abstraction}/v1.0.json` — these are *protocol identifiers*, not fetch URLs. The `fcop.dev` host is not (yet) a live schema registry; do not assume HTTP `GET` on these IDs returns the schema body. Cross-schema `$ref` uses **the absolute `$id`** of the target so validators can resolve them through any registry that maps these IDs to the local schema bodies (the validating-script snippet below shows the pattern with `referencing.Registry`). Relative `$ref` is intentionally avoided: it depends on a base URI inferred from the referrer, which differs across implementations.
- **Version**: every schema declares `"version": "1.0.0"`. Frozen for the entire FCoP v1.x line per [ADR-0003](../../adr/ADR-0003-stability-charter.md). v1.1 may add fields (additive); v2.0 may remove or change types (breaking).
- **`additionalProperties`**: closed sub-objects (e.g. `subject` in `failure.schema.json`) use `additionalProperties: false`. The IPC envelope **root** uses `additionalProperties: true` so 0.7.x files with extra unknown frontmatter keys remain valid (per [ADR-0003](../../adr/ADR-0003-stability-charter.md) backward-compat rule).

## Validating a file by hand

```bash
pip install jsonschema referencing pyyaml
python - <<'PY'
import json, yaml
from pathlib import Path
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

schemas_dir = Path("spec/schemas")
schemas = {p.name: json.loads(p.read_text(encoding="utf-8"))
           for p in schemas_dir.glob("*.schema.json")}

registry = Registry()
for s in schemas.values():
    registry = registry.with_resource(uri=s["$id"], resource=Resource.from_contents(s))

ipc = schemas["ipc-envelope.schema.json"]
validator = Draft202012Validator(ipc, registry=registry)

raw = Path("fcop/tasks/TASK-20260601-001-PM-to-DEV.md").read_text(encoding="utf-8")
fm = yaml.safe_load(raw.split("---", 2)[1])
fm.setdefault("type", "TASK")  # type is implicit in 0.7.x; v1.0 wants it explicit

errors = sorted(validator.iter_errors(fm), key=lambda e: list(e.path))
for e in errors:
    print(f"  - {'.'.join(map(str, e.path)) or '<root>'}: {e.message}")
print("OK" if not errors else f"FAIL ({len(errors)} errors)")
PY
```

> **Note on `type` field**: 0.7.x envelope files do not always carry an explicit `type` key in frontmatter — the type was inferred from the filename PREFIX. v1.0 schemas require `type` explicitly because the IPC envelope discriminator depends on it. The reference implementation will inject `type` automatically when reading legacy files, so 0.7.x files remain valid on disk; only the in-memory frontmatter passed to a validator needs the field.

## Cross-schema `$ref` map

All cross-file `$ref` use the absolute target `$id`:

```
ipc-envelope.schema.json
    └─ $defs.review            → https://fcop.dev/schemas/review/v1.0.json#/$defs/{subjectType, decisionEnum}
agent.schema.json
    ├─ properties.can          → https://fcop.dev/schemas/boundary/v1.0.json#/$defs/capabilityToken
    └─ properties.cannot       → https://fcop.dev/schemas/boundary/v1.0.json#/$defs/capabilityToken
event.schema.json
    ├─ $defs.subject.decision         → https://fcop.dev/schemas/review/v1.0.json#/$defs/decisionEnum
    ├─ $defs.subject.attempted_action → https://fcop.dev/schemas/boundary/v1.0.json#/$defs/capabilityToken
    ├─ $defs.subject.failure_type     → https://fcop.dev/schemas/failure/v1.0.json#/$defs/failureType
    └─ $defs.subject.recovery_action  → https://fcop.dev/schemas/failure/v1.0.json#/$defs/recoveryAction
```

All targets are mapped by the registry to local schema bodies; no network resolution happens.

## Versioning rules (per [ADR-0003](../../adr/ADR-0003-stability-charter.md))

| Change kind | SemVer bump | Example |
|---|---|---|
| Add a new optional field | MINOR (1.0 → 1.1) | new `Agent.alias` field |
| Add a new enum value | MINOR (1.0 → 1.1) | new event type `TASK_REASSIGNED` |
| Add a new schema file | MINOR (1.0 → 1.1) | `skill.schema.json` |
| Make an optional field required | **MAJOR (1.x → 2.0)** | requiring `Agent.layer` |
| Remove a field or enum value | **MAJOR (1.x → 2.0)** | dropping `priority: P3` |
| Change a field's type | **MAJOR (1.x → 2.0)** | `version: 1` → `version: "1.0"` |
| Tighten a regex / pattern | **MAJOR (1.x → 2.0)** | role code max length 16 → 8 |

Every MAJOR bump requires a new ADR superseding the relevant per-abstraction ADR.

## Not in v1.0 (deferred)

These artefacts are **deliberately absent** in v1.0 per [ADR-0015 §non-goals](../../adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md):

- `skill.schema.json` — Skill registry → v1.1 (per [ADR-0011 → Deferred](../../adr/ADR-0011-skill-registry.md))
- `session.schema.json` — Full Session state → v1.x (only the recovery-call sub-shape is in `failure.schema.json`)
- `needs_human` decision value + `human_approval` sub-object → v1.2+ (per [ADR-0017 §what-v1.0-does-not-include](../../adr/ADR-0017-review-file-type-minimal.md))
- `EVENT-*.md` envelope type → never planned; events are derived per [ADR-0018](../../adr/ADR-0018-event-model.md)

## Where to read next

- **Long-form normative spec**: [`spec/fcop-runtime-protocol-v1.0.md`](../fcop-runtime-protocol-v1.0.md)
- **Decision history**: [`adr/`](../../adr/) — ADR-0015 is the v1.0 charter; ADR-0016..0022 are the per-abstraction implementation ADRs
- **0.7.x baseline (frozen)**: [`spec/fcop-spec-v1.0.3.md`](../fcop-spec-v1.0.3.md) — kept for legacy conformance tests; not the v1.0 spec
