---
title: FCoP 4.0 WP3B.1 Correction Plan
document_role: IMPLEMENTATION_PLAN
status: PROOF_COMPLETE_BEFORE_CODE_CHANGE
authorized_scope: WP3B_1_ONLY
input_head: 297dc06ece87f1d4adf938875cb19e59be87def0
taskbook_commit: 48082cd1c7e96cce7f1da8c7677ba4caf7ab8c74
frozen_contract_commit: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
requested_gate: WP3B_LIFECYCLE_ACCEPTED
---

# FCoP 4.0 WP3B.1 Correction Plan

## 1. Verified execution boundary

The authoritative taskbook blob at
`taskbooks/fcop-4.0/WP3B.1/01-Lifecycle-Round-Contract-Correction-Taskbook.zh.md`
has 23,023 bytes, 784 lines, and SHA-256
`26eb81dd022758cfc9a55c4eaf1cf637486175d873b2f65eae6ac2ad5b3c07c5`.
Commit `48082cd1c7e96cce7f1da8c7677ba4caf7ab8c74` contains code baseline
`297dc06ece87f1d4adf938875cb19e59be87def0` as an ancestor; the only
changes between them are under `taskbooks/**`. The English and Chinese frozen
specification blobs are byte-identical to commit
`aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6`.

This plan covers only the three authorized WP3B.1 corrections. It does not
start T4-T7, authorization, convergence, MCP, Schema, CodeFlowMu, main, or
release work.

## 2. Why the current receipt selector blocks a second T3 round

`matching_receipts()` currently selects by workspace, TASK, source stage, and
target stage, then rejects more than one match. A completed attempt-A T3 receipt
therefore still occupies the sole `active -> review` slot. After a fixture
materializes a lawful T5/T6 return to active with attempt B, a T3 request for B
finds A before it derives B from transition history. It either attempts recovery
against A or fails because A and B both have receipts. The persisted
`attempt_id` already exists in each receipt, but the selector does not use it as
round identity.

## 3. Round-selection algorithm

The correction will keep every receipt and validate every encountered receipt,
but separate enumeration from relevance:

1. Compute the canonical source and target paths for the requested edge.
2. For T3, parse every visible source/target copy and derive its attempt only by
   `current_attempt()` from transition history.
3. If visible copies disagree about the attempt, or no visible copy can prove
   an attempt, fail closed with `RECOVERY_REQUIRED`/the existing frozen error.
4. Enumerate all valid receipts for the workspace, TASK, and edge without using
   mtime, filename recency, directory iteration order, or process memory.
5. For T3, retain only receipts whose persisted `attempt_id` equals the proved
   current attempt. Historical receipts for older attempts remain audit facts
   but are not recovery candidates.
6. Zero relevant receipts means a new operation may be prepared from the
   uniquely authoritative source. One relevant receipt means recover that exact
   operation after its normalized request digest is checked. More than one
   relevant receipt is ambiguous and fails closed without mutation.
7. T2 remains a single-entry edge. Its existing receipt is recoverable only as
   the unique edge receipt; multiple receipts remain a fail-closed corruption.

This distinguishes four persisted classes:

| Persisted facts | Classification |
|---|---|
| Older-attempt `COMMITTED` receipt | Historical audit fact; ignored for current T3 selection |
| Current-attempt `PREPARED`/`TARGET_DURABLE` receipt | Current incomplete round; recover only it |
| Current-attempt `COMMITTED` receipt with target visible | Current committed/lost-response round; return its existing result |
| Multiple current-attempt receipts, damaged identity, or divergent copies | `RECOVERY_REQUIRED`; preserve everything |

## 4. Crash-state lookup proof

- **Source only:** T3 derives the current attempt from the active source's last
  entry-to-active transition, then chooses only that attempt's receipt. A
  `PREPARED` match is `NOT_COMMITTED` and can resume.
- **Target only:** T3 derives the same attempt from the review target. A matching
  `TARGET_DURABLE` or `COMMITTED` receipt is the lost-response candidate and is
  completed/returned without appending another event.
- **Source and target:** both copies must independently prove the same current
  attempt before receipt selection. The frozen five-state classifier then
  decides recoverable duplicate, divergent duplicate, or indeterminate; the
  selector does not guess.
- **Neither copy:** the current round is not provable. No timestamp or receipt
  ordering substitutes for NOW, so the operation fails closed and preserves all
  evidence.

An old `COMMITTED` receipt cannot be selected for a new attempt because its
persisted `attempt_id` differs from the attempt on the latest entry-to-active
event. This remains true when actor and `report_ref=None` are identical across
rounds.

## 5. Attempt contract and fixture alignment

Production `current_attempt()` will remove the top-level `attempt_id` fallback.
Only the final valid transition whose destination is `active` can supply the
current attempt, as required by F4.6.1. A top-level value may remain an extension
field in deliberately malformed fixtures, but it has no Core authority.

`WorkspaceFixture.task()` currently writes `attempt_id` at top level while its
default transition list is empty. When an attempt is supplied and transition
history is omitted, the fixture will instead materialize an entry-to-active
event carrying that attempt. An explicitly supplied transition sequence remains
under the individual test's control. The C3 T6 fixture that explicitly requests
an empty history will be aligned to the default valid history. No Test ID,
purpose, expected error, assertion, skip, or xfail will change.

## 6. REPORT boundary correction

The current production code rejects a current-attempt REPORT solely because the
TASK path is not `active`. That policy is not frozen. The correction will:

- derive the TASK's current attempt from transition history for every lifecycle
  state;
- reject any REPORT for a non-current attempt with `ATTEMPT_MISMATCH`;
- retain final uniqueness and replacement-current-head validation inside the
  existing family lock;
- allow an otherwise valid current-attempt replacement in review, done, or
  archive;
- append a new REPORT only, without changing the old REPORT or TASK transition
  event.

No later T4/T7 evidence decision is implemented here.

## 7. Exact planned files

Production:

- `src/fcop/v4/lifecycle.py`
- `src/fcop/v4/receipts.py`
- `src/fcop/v4/creation.py`

Tests and frozen-fixture alignment:

- `tests/test_fcop/test_v4_lifecycle.py`
- `tests/conformance/v4/fixtures.py`
- `tests/conformance/v4/test_c3_lifecycle.py`

Reports and delivery:

- this correction plan;
- `reports/FCOP-4.0-WP3B.1-RECEIPT-ROUND-PROOF.md`;
- `reports/FCOP-4.0-WP3B.1-CONTRACT-TEST-ALIGNMENT.md`;
- `reports/FCOP-4.0-WP3B.1-CORRECTION-RESULT.md`;
- `reviews/fcop-4.0/wp3b.1/MANIFEST.md` in the second commit only.

No change is planned for `linearization.py`, C5, C8, or any forbidden path.

## 8. Complexity budget

```yaml
NEW_RUNTIME_DEPENDENCIES: 0
NEW_BACKGROUND_COMPONENTS: 0
NEW_AUTHORITATIVE_STORES: 0
NEW_PUBLIC_APIS: 0
PUBLIC_APIS_REMOVED: 0
NEW_BASE_ERROR_CODES: 0
V3_METHOD_SIGNATURE_CHANGES: 0
FROZEN_SPEC_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0
NEW_PRODUCTION_MODULES: 0
```

The implementation will reuse the existing receipt validator, five-state
classifier, report-head function, family lock, and atomic file primitives. It
adds no future-WP3C abstraction.
