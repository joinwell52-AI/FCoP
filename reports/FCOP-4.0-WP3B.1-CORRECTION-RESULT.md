---
title: FCoP 4.0 WP3B.1 Correction Result
document_role: EXECUTION_RESULT
status: COMPLETE_PENDING_GITHUB_DELIVERY
authorized_scope: WP3B_1_ONLY
input_head: 297dc06ece87f1d4adf938875cb19e59be87def0
taskbook_commit: 48082cd1c7e96cce7f1da8c7677ba4caf7ab8c74
frozen_contract_commit: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
requested_gate: WP3B_LIFECYCLE_ACCEPTED
---

# FCoP 4.0 WP3B.1 Correction Result

## 1. Outcome

```yaml
WP3B_1_STATUS: COMPLETE_PENDING_GITHUB_DELIVERY
AUTHORIZED_SCOPE: WP3B_1_ONLY
RECEIPT_ROUND_IDENTITY: PASS
HISTORICAL_RECEIPT_REUSE: PASS
MULTI_ATTEMPT_T3: PASS
LOST_RESPONSE_CURRENT_ROUND: PASS
HISTORICAL_RECEIPTS_PRESERVED: PASS
CURRENT_ATTEMPT_SOURCE: TRANSITION_ONLY
TOP_LEVEL_ATTEMPT_FALLBACK: REMOVED
CONFORMANCE_ALIGNMENT: PASS
REPORT_STATE_POLICY: CONTRACT_ALIGNED
WP3B_TARGET_NODES: 9/9
WP3B_1_NEW_TESTS: 15/15
FROZEN_TEST_IDS: 60/60
UNEXPECTED_FAILURES: 0
WP3C_STARTED: false
REQUESTED_GATE: WP3B_LIFECYCLE_ACCEPTED
```

No Gate is self-signed.

## 2. Three corrected findings

### P0-A · receipt round identity — closed

Receipt enumeration no longer assumes one lifetime T3 receipt per TASK edge.
T3 derives the current attempt from visible source/target transition history
under the family lock and selects only receipt files carrying that attempt.
Older committed receipts remain untouched and cannot block a later attempt.
More than one receipt for the current attempt fails closed with
`RECOVERY_REQUIRED` and zero writes.

Two-round, historical-plus-PREPARED, current-round response-loss, identical
actor/null-report-ref, and multiple-current-receipt cases all pass through the
real `Project.transition()` production path.

### P0-B · current attempt source — closed

`current_attempt()` no longer reads top-level `attempt_id`. It recognizes the
last legal T2/T5/T6 entry-to-active transition only. Top-level-only input returns
`ATTEMPT_MISMATCH`; disagreement between top-level and transition values selects
the transition value; multiple entries select the last legal one.

The shared Conformance fixture now materializes active-entry history whenever an
attempt is supplied and no explicit history is requested. C3-N02's prior-event
assertion was aligned from zero to one. No Test ID, purpose, expected error, or
behavior assertion changed.

### P1-C · REPORT state policy — closed

The non-contractual active-only rejection was removed. Current-attempt
replacement REPORTs can be appended in review, done, and archive while retaining
unique-head validation inside the family lock. Old attempts fail with
`ATTEMPT_MISMATCH` in every post-entry state. Concurrent replacements leave one
accepted head; old REPORT and TASK bytes remain unchanged.

The pre-existing T1/inbox append-only behavior remains compatible when no active
attempt yet exists. Such a fact cannot satisfy T3, which still requires an active
path and a transition-derived current attempt.

## 3. Exact content files

```text
src/fcop/v4/creation.py
src/fcop/v4/lifecycle.py
src/fcop/v4/receipts.py
tests/conformance/v4/fixtures.py
tests/conformance/v4/test_c3_lifecycle.py
tests/test_fcop/test_v4_lifecycle.py
reports/FCOP-4.0-WP3B.1-CORRECTION-PLAN.md
reports/FCOP-4.0-WP3B.1-RECEIPT-ROUND-PROOF.md
reports/FCOP-4.0-WP3B.1-CONTRACT-TEST-ALIGNMENT.md
reports/FCOP-4.0-WP3B.1-CORRECTION-RESULT.md
```

The Manifest is intentionally excluded from the Content Commit and is added by
the second commit only.

## 4. Final verification

All commands were run in `D:/FCoP-wp3b1-round-correction` on native Windows.
MCP commands explicitly bound `PYTHONPATH=mcp/src;src` to the current worktree.

| Check | Final actual result |
|---|---|
| `python -m pytest tests/test_fcop/test_v4_lifecycle.py -q` | 47 passed (32 retained WP3B cases + 15 new cases) |
| WP3B frozen target selection | 9 passed |
| affected C3/C5/C8 | 17 passed / 37 expected later-stage failures |
| `python -m pytest tests/test_fcop -q` | 1049 passed |
| bound `python -m pytest tests/test_fcop_mcp -q` | 80 passed |
| bound full non-Conformance suite | 1366 passed, 2 existing legacy-fixture skips |
| five v4 Static/Meta modules | 27 passed |
| v4 Behavioral C1-C8 | 35 passed / 57 expected later-stage failures |
| complete v4 suite | 62 passed / 57 expected later-stage failures |
| v4 collect-only | 119 collected |
| mypy Windows/Linux/Darwin core | PASS / PASS / PASS, 36 files each |
| mypy MCP source/tests | PASS, 17 files |
| changed-file Ruff | PASS |
| `git diff --check` | PASS |

The two skipped non-Conformance nodes are the inherited absence/empty parameter
cases for migrated `docs/agents/log`; no skip or xfail was added. The 57 v4
failures are the exact WP3B baseline set for T4-T7, authorization, convergence,
public recovery, and fault injection. The pass/fail set did not drift.

## 5. Deferred failures and known limits

- T4, T5, T6, and T7 remain deliberately unimplemented.
- Authorization/Profile evaluation and consumption remain deliberately
  unimplemented.
- Convergence REVIEW, family digest, Branch terminal gates, public recovery,
  and public fault injection remain deliberately unimplemented.
- Native Linux and macOS tests were not run; only their mypy platform branches
  were checked.
- Receipt validation remains globally fail-closed: a damaged receipt is not
  silently ignored merely because a newer attempt exists.

No deferred failure was removed, added, skipped, xfailed, or converted into a
stub pass by WP3B.1.

## 6. Complexity and scope ledger

```yaml
NEW_RUNTIME_DEPENDENCIES: 0
NEW_BACKGROUND_COMPONENTS: 0
NEW_AUTHORITATIVE_STORES: 0
NEW_PUBLIC_APIS: 0
PUBLIC_APIS_REMOVED: 0
NEW_BASE_ERROR_CODES: 0
V3_METHOD_SIGNATURE_CHANGES: 0
FROZEN_SPEC_FILES_MODIFIED: 0
SCHEMA_FILES_MODIFIED: 0
MCP_IMPLEMENTATION_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0
MAIN_MODIFIED: false
RELEASE_CREATED: false
TAG_CREATED: false
WP3C_STARTED: false
```

The implementation reuses the existing Root-family lock, receipt schema,
five-state classifier, atomic file primitives, report-head resolver, and public
Project facade. No production module, recovery API, database, cache, index
service, queue, watcher, daemon, scheduler, or future-stage abstraction was
added.

## 7. Delivery state

This report precedes the required Content Commit and Manifest-only Commit. Their
exact hashes, remote HEAD, per-file Git-blob SHA-256 values, ancestry, and remote
refetch result are recorded in `reviews/fcop-4.0/wp3b.1/MANIFEST.md`. After that
remote verification, execution stops and requests
`WP3B_LIFECYCLE_ACCEPTED` from ADMIN.
