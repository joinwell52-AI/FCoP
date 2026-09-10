---
title: FCoP 4.0 WP3B.1 Receipt Round Proof
document_role: IMPLEMENTATION_EVIDENCE
status: VERIFIED
authorized_scope: WP3B_1_ONLY
input_head: 297dc06ece87f1d4adf938875cb19e59be87def0
frozen_contract_commit: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
---

# FCoP 4.0 WP3B.1 Receipt Round Proof

## 1. Old failure sequence

The WP3B selector treated `(workspace_id, task_id, from_stage, to_stage)` as a
globally unique receipt key:

```text
attempt A active
  -> T3 prepares and commits receipt RA(active, review, attempt A)
  -> TASK is in review
fixture materializes authorized T5 result
  -> TASK returns to active with new attempt B
attempt B T3
  -> old selector finds RA because TASK and edge match
  -> either RA is recovered against B's files or a second receipt makes the
     selector reject the entire edge
```

The receipt already persisted `attempt_id`; the defect was failure to use it
when selecting the current recovery round.

## 2. New deterministic relevance rule

All receipt files are still parsed and strictly validated. Enumeration then
returns every receipt for the workspace/TASK/edge. T3 performs a second,
contract-derived relevance step under the existing family lock:

```text
visible active/review TASK copy or copies
  -> current_attempt(transition history only)
  -> require one unique visible attempt
  -> receipts where receipt.attempt_id == visible attempt
  -> 0: prepare a new T3 from the unique active source
     1: check request digest, classify, and recover/return it
    >1: RECOVERY_REQUIRED, zero mutation
```

T2 has no prior attempt at its inbox source and remains a single-entry edge;
its one edge receipt is selected exactly as before. More than one T2 receipt is
still fail-closed.

## 3. Receipt relevance table

| Receipt fact | Visible current attempt | Relevant? | Result |
|---|---|---:|---|
| RA `COMMITTED`, attempt A | B | No | Retained as history; cannot block B |
| RB `PREPARED`, attempt B | B | Yes | Resume B from source-only state |
| RB `TARGET_DURABLE`, attempt B | B | Yes | Apply frozen five-state classification |
| RB `COMMITTED`, attempt B | B | Yes | Return B's committed result after response loss |
| RA and RB both `COMMITTED` | B | RB only | Return B, never A |
| Two receipts both claiming B | B | Ambiguous | `RECOVERY_REQUIRED`, preserve both |
| Visible source and target prove different attempts | A and B | Unprovable | `RECOVERY_REQUIRED`, preserve all copies |
| Neither TASK copy visible | none | Unprovable | `RECOVERY_REQUIRED`; no receipt-order guess |

## 4. Attempt A/B persisted example

The production-entry test `test_t3_receipts_are_scoped_to_attempt_rounds`
creates these facts:

1. active TASK with a valid T2 event carrying attempt A;
2. attempt-A REPORT and committed T3 event/receipt RA;
3. a fixture-only completed T5 materialization carrying attempt B;
4. attempt-B REPORT and committed T3 event/receipt RB.

It asserts:

- two receipt files remain;
- their operation IDs differ;
- their attempt IDs are exactly A and B;
- both T3 events remain and bind different REPORT evidence;
- an exact retry returns RB and attempt B;
- RA's bytes are unchanged before and after B and its retry;
- the final TASK contains one event per physical transition, not a duplicate T3.

Actor is `ME` in both rounds and the public T3 request uses `report_ref=None` in
both rounds. The selector therefore proves that attempt identity, not actor,
optional report reference, mtime, or request coincidence, separates rounds.

## 5. Historical COMMITTED plus current PREPARED

`test_current_prepared_t3_wins_over_historical_committed_receipt` first commits
RA, then injects a failure immediately after RB is durably published as
`PREPARED`. The next production T3 call sees:

```text
RA: attempt A, COMMITTED
RB: attempt B, PREPARED
NOW: active TASK, last legal entry-to-active = attempt B
```

Only RB is recovered. It becomes `COMMITTED`, the TASK reaches review once, and
RA remains byte-for-byte unchanged.

## 6. Lost-response example

`test_lost_response_recovers_current_not_historical_round` injects failure at
RB's `COMMITTED` receipt update after the target is durable and the source has
been removed. The retry derives B from the review target, selects RB rather than
RA, completes the receipt, and returns B's result. Exactly two T3 events exist:
one for A and one for B. No third event or TASK copy is created.

## 7. Multiple-current-receipt conflict

`test_multiple_receipts_for_current_attempt_fail_closed` reaches a real
`PREPARED` receipt through the production transition path, then materializes a
second valid receipt identity that claims the same current attempt. The retry
returns structured `RECOVERY_REQUIRED`; a complete pre/post tree digest proves
zero mutation and both receipt files remain present.

## 8. Physical state proof

| Filesystem observation | Round discovery | Mechanical decision boundary |
|---|---|---|
| source only | attempt from active source history | matching PREPARED may resume |
| target only | attempt from review target history | matching TARGET_DURABLE/COMMITTED may complete/return |
| source + target | both histories must agree | frozen classifier decides duplicate/divergent/indeterminate |
| neither | no provable current attempt | fail closed; preserve receipts |

The existing five-state classifier, no-overwrite target publication, durable
receipt stage replacement, and authoritative-source removal are unchanged.

## 9. No ordering or deletion oracle

Selection does not read file mtime, creation time, directory position, sorted
filename priority, lock timestamp, process-local generation, or cache state.
Directory sorting remains only deterministic enumeration; it cannot choose a
winner because all relevant candidates are counted and more than one fails
closed. No receipt cleanup or deletion path was added. Historical receipts are
permanent audit evidence.

## 10. Verification

```yaml
MULTI_ATTEMPT_T3: PASS
HISTORICAL_COMMITTED_PLUS_CURRENT_PREPARED: PASS
LOST_RESPONSE_CURRENT_ROUND: PASS
SAME_ACTOR_AND_NULL_REPORT_REF_ACROSS_ROUNDS: PASS
MULTIPLE_CURRENT_RECEIPTS: RECOVERY_REQUIRED_ZERO_WRITE
HISTORICAL_RECEIPTS_PRESERVED: PASS
MTIME_OR_DIRECTORY_ORDER_USED: false
PUBLIC_OPERATION_ID_ADDED: false
```
