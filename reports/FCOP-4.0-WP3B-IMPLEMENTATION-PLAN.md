# FCoP 4.0 WP3B Implementation Plan

Status: **APPROVED FOR IMPLEMENTATION BY PRE-CODE PROOF**

Authorized scope: `WP3B_ONLY`

Input: `d2d2e9518451d58d165e3705f13f1ceb24388571`

## 1. Scope

Implement only T2 `inbox -> active`, T3 `active -> review`, their private
durable receipts, deterministic TASK inspection, and the minimum family-lock
connections required to make T3 evidence linearizable with Branch creation and
REPORT final/replacement writes.

T4–T7, authorization, convergence, public recovery/fault injection,
`list_branches`, `family_digest`, MCP, CodeFlowMu, main, schemas, frozen
specifications and frozen conformance tests remain untouched.

## 2. Planned files and responsibilities

| File | Planned change |
|---|---|
| `src/fcop/v4/linearization.py` | New private stable family key, lock path and one-lock context. |
| `src/fcop/v4/receipts.py` | New private T2/T3 receipt schema, strict identity/path validation, five-state classification, stage update and mechanical recovery helpers. |
| `src/fcop/v4/lifecycle.py` | New private T2/T3 request validation, attempt/head/evidence resolution, event planning, receipt-backed commit, and deterministic `inspect_state`. |
| `src/fcop/v4/creation.py` | Minimal lifecycle routing plus family-lock integration for Branch create and REPORT final/replacement publication. |
| `src/fcop/v4/encoding.py` | Add dedicated receipt atomic-replace and durable authoritative-source removal primitives; preserve `publish()` no-overwrite semantics. |
| `tests/test_fcop/test_v4_lifecycle.py` | Public-`Project` behavior, race, receipt, crash-window, relocation and fail-closed tests required by §13.3. |
| `tests/test_fcop/test_v4_creation.py` | Only if a focused Branch/REPORT regression cannot live in the lifecycle test file. |
| Required WP3B reports and Manifest | Evidence, results and GitHub delivery metadata only. |

No other production file is planned.

## 3. Test mapping

| Requirement | Verification |
|---|---|
| T2 unique move/event/attempt/result | New lifecycle tests plus `C3-GATE-01[T2]` and `C8-N01` |
| T2 two-process serialization and no overwrite | New multiprocessing test plus `C8-R01` |
| T3 current attempt/head/digest | New lifecycle tests plus `C3-GATE-01[T3]`, `C5-N01`, `C5-R01` and `C5-R02` |
| REPORT replacement/T3 linearizability | New true-operation multiprocessing race |
| Branch/T3 linearizability and depth | New true-operation race plus `C4-R02` |
| Five-state receipt coverage | New state-table and crash-boundary tests tied to the Implementability Proof |
| Relative receipt paths and relocation | New project-directory relocation test |
| v3/MCP/WP3A/WP3A.1 compatibility | Full taskbook command set and targeted existing suites |

## 4. Commit discipline

1. Keep the two pre-code documents present before the first production edit.
2. Implement private modules and minimal connections; add production behavior
   tests without modifying `tests/conformance/v4/**`.
3. Run targeted tests, then all required regression, static and collection
   commands. Record actual counts without turning later-WP failures green by
   stubs.
4. Write atomicity mapping and result reports.
5. Create one content commit.
6. Generate `reviews/fcop-4.0/wp3b/MANIFEST.md` from committed blob bytes and
   create a Manifest-only commit.
7. Push only `review/fcop-4.0-wp3b-lifecycle-plane`, fetch it again, verify
   ancestry, parentage, paths, bytes and SHA-256, and stop at the requested Gate.

## 5. Invariants

- Filesystem remains the only authoritative fact source; path is NOW and event
  is PAST.
- One command commits one edge and one event.
- Destination publication never overwrites.
- One operation holds at most one family lock; Branch create alone nests its
  existing operation lock under the family lock.
- No cache, database, registry, queue, daemon, watcher, timer, network call, new
  runtime dependency, role policy or second public facade is introduced.
- No new Base error code is required; existing stable codes express every WP3B
  outcome.
