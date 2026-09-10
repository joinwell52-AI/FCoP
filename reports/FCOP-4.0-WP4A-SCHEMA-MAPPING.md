# WP4A.1 Schema mapping and input audit

## Inputs and historical schema audit

Authority and preserved-blocker hashes are in `FCOP-4.0-WP4A.1-SCHEMA-BINDING.md`. Input audit confirmed no drift from the taskbook's eight legacy schemas, 119 frozen Conformance nodes and unchanged public snapshot. The original package-data glob covered only flat `*.schema.json`; this change adds only the v4 data glob.

| Old file | Declared version | Existing $id suffix | Historical purpose |
|---|---|---|---|
| agent.schema.json | 1.0.0 | agent/v1.0.json | Agent identity/capability abstraction |
| boundary.schema.json | 1.0.0 | boundary/v1.0.json | Capability boundary |
| encoding.schema.json | 1.0.0 | encoding/v1.0.json | Encoding abstraction |
| event.schema.json | 1.0.0 | event/v1.0.json | Event abstraction |
| failure.schema.json | 1.0.0 | failure/v1.0.json | Failure abstraction |
| ipc-envelope.schema.json | 1.1.0 | ipc-envelope/v1.0.json | Legacy IPC envelope |
| review.schema.json | 1.1.0 | review/v1.0.json | Legacy review |
| skill.schema.json | 1.1.0 | skill/v1.1.json | Skill extension |

IDs have prefix `https://fcop.dev/schemas/`. Count is **5 x 1.0.0 + 3 x 1.1.0**. IPC/review retain their known version/$id mismatch. `spec/schemas/README.md` still calls the historical collection v1.0 SSOT. None was edited. Windows may check these historical text files out as CRLF; the isolation test compares their Git-normalized content to the fixed input, without rewriting them.

## Structural mapping: 12/12 applicable object groups

This is object-group coverage, not a claim that twelve tests prove every behavioral clause. Each row names the exact generated schema basename; each has Draft 2020-12, revision 4.0.0, and unique ID `https://fcop.dev/schemas/v4/<basename>.schema.json`.

| Schema basename | Frozen clause / stable Toolkit source | Structural coverage |
|---|---|---|
| workspace | F4.2.1–3 | Protocol/version, canonical UUID URN, unique Profile list, closed encoding |
| task | F4.3.1–2, F4.5, F4.8.2 | Common fields, typed ID, subject, transitions, relations and operation fields |
| report | F4.3.2/4, F4.6.1–2 | Subject, current-attempt format, final/replacement enum, result, references |
| issue | F4.3.2 | Subject, severity, references |
| review | F4.3.2/5, F4.6.5, F4.7.1–2 | Review kind/decision, attempts/digests, conditional authorization binding and Profile |
| transition | F4.4.5 | Closed timestamp/from/to/by/tool object, attempts, evidence and authorization digests |
| authorization-binding | F4.7.1 | Closed from/to binding with stage enumerations |
| family-canonical | F4.6.6 | Closed contract/root/branches and closed Branch tuple objects |
| create-request-canonical | F4.8.4 | Closed exact thirteen-field canonical request, ID format, normalized relations |
| create-operation | F4.8.5; creation.py fact | Closed stable identity/path/request/content digest fact |
| lifecycle-receipt | F4.9.4/9; receipts.py | Closed stable base and authorized-edge receipt variants, paths/stages/digests/event |
| recovery-observation | recovery.py::_compact_receipt | Existing closed five-field compact observation |

All schemas are generated from one declarative source into `spec/schemas/v4` and `src/fcop/_data/schemas/v4`; `generate.py --check` proves byte parity. The loader scans every `$ref` against bundled IDs before constructing validators; no URL fetch is a fallback. The existing jsonschema dependency supplies validation, with no new dependency or registry service.

## Integration and limits

`creation.py::_manifest` and `_Creation._validate` share `schema._validate` with the writer. A duplicated per-envelope required-field table was removed. `encoding.py::envelope_bytes` and `rewritten_envelope_bytes` strictly reparse actual proposed publication bytes and validate the full object. Create request/fact, lifecycle receipt, compact recovery observation, and family canonical inputs invoke the same validator at their existing boundaries. Specialized workspace identity, relation, authorization and recovery errors retain their existing Core owners. No Project API or lifecycle algorithm changed.

Five root objects alone are open. Nested Core objects are closed; issuer proof is Profile-owned opaque data, not an invented Core subobject. Authorization-context nulls on assessment/convergence do not turn those reviews into authorization. Authorization-kind reviews require non-null profile/binding/single-use fields; nullable expiry/attempt/family applicability still undergoes the existing gate, not a Schema-only permission decision.

Historical transition `from/to/tool` are structurally strings. This preserves the existing `test_last_entry_to_active_is_current_attempt` contract: a later event with `from: unknown` is not a valid active-entry and cannot select current attempt. It is not authorization to perform an unknown edge. Binding/receipt stage fields use closed enumerations. The schema does not replay history or certify T1–T7 legality; NOW and legal-edge decisions remain in Core. This boundary is explicitly disclosed rather than labelling historical event shape as behavioral conformance.

Schema cannot prove authoritative path uniqueness, evidence freshness, current REPORT head, Profile trust, expiry/single-use, family coverage, lock serialization, races or five-state recovery. Corresponding frozen behavioral tests remain mandatory. Canonical normalization/sorting/hash equality is implemented by existing Core; Schema represents the input shape, not the hash algorithm. No 4.0 contract, Conformance, MCP, rules, version, workflow or CodeFlowMu file was modified.

## Test provenance

`tests/test_fcop/test_v4_schema.py` validates actual Project-produced workspace/four envelopes/receipt bytes, checks required-field deletion and incorrect types/enums for every mapped object, runs two public examples, and exercises SB-01–10. Synthetic compact observation/canonical dictionaries supplement, not replace, real lifecycle/family tests. Final run totals are recorded in RESULT; early development red runs are not reported as delivery success.
