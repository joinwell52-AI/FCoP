---
title: FCoP 4.0 WP3B.1 Contract Test Alignment
document_role: CONFORMANCE_ALIGNMENT_EVIDENCE
status: VERIFIED
authorized_scope: WP3B_1_ONLY
frozen_contract_commit: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
frozen_test_ids: 60/60
---

# FCoP 4.0 WP3B.1 Contract Test Alignment

## 1. Frozen authority

F4.6.1 states that each T2/T5/T6 entry into active creates a non-reusable
`attempt_id` in that transition, and that the current attempt is the ID on the
last transition entering active. A top-level `attempt_id` is not an alternative
fact source. F4.6.2 requires T3 evidence to match that current attempt.

The baseline fixture contradicted this contract by producing, by default:

```yaml
attempt_id: urn:uuid:...
transitions: []
```

Production had a special fallback for that shape. WP3B.1 removes the fallback
and aligns test persistence with the frozen contract.

## 2. Modified Conformance files

| File | Before | Frozen clause | After |
|---|---|---|---|
| `tests/conformance/v4/fixtures.py` | `task(attempt_id=...)` stored the value only at top level and defaulted to an empty transition list | F4.4.5, F4.6.1 | when transitions are omitted, the fixture writes a valid inbox-to-active event carrying the supplied attempt; explicitly supplied histories remain exact test input |
| `tests/conformance/v4/test_c3_lifecycle.py` | C3-N02 explicitly forced `transitions=[]` and expected zero previous events | F4.6.1 | C3-N02 uses the aligned fixture and expects one previous active-entry event before the future T6 event |

No C5 or C8 test edit was necessary. Their existing calls use
`WorkspaceFixture.task(attempt_id=...)`; the corrected fixture gives those
arrangements the required persistent history without changing their actions or
assertions.

Ruff's deterministic formatter also removed one unused C3 import and normalized
pre-existing import/annotation style in these two changed files so that the
taskbook's changed-file Ruff requirement passes. Those mechanical edits do not
alter test semantics.

## 3. Persisted shape after alignment

A fixture TASK with an attempt now contains at least:

```yaml
transitions:
  - at: 2026-09-03T00:00:01+08:00
    attempt_id: urn:uuid:...
    by: ME
    from: inbox
    to: active
    tool: claim_task
```

The existing top-level value is retained only as a non-authoritative extension
for fixture compatibility. Production ignores it. A dedicated negative test
constructs an active TASK with a top-level value and `transitions: []` and
proves `ATTEMPT_MISMATCH` with zero writes. Another test makes the top-level
value disagree with the transition value and proves that only the transition
value is used. A third supplies multiple entry-to-active events and proves that
the last legal one wins while a later malformed `to: active` fragment does not.

## 4. Test ID and purpose preservation

Comparison against `297dc06ece87f1d4adf938875cb19e59be87def0` shows:

```yaml
CONFORMANCE_FILES_CHANGED: 2
TEST_FUNCTION_NAME_ADDITIONS_OR_REMOVALS: 0
TEST_ID_TEXT_ADDITIONS_OR_REMOVALS: 0
FROZEN_TEST_IDS: 60/60
SKIP_ADDED: 0
XFAIL_ADDED: 0
ASSERTIONS_REMOVED: 0
EXPECTED_ERROR_CHANGES: 0
```

C3-N02 still tests that T6 creates a genuinely new attempt; its prior-event
count changes from zero to one solely because the old attempt is now represented
by the contract-required active-entry history. All 119 collected v4 nodes and
the baseline pass/fail split remain unchanged.

## 5. Production fallback removal

`src/fcop/v4/lifecycle.py::current_attempt()` no longer reads
`fields["attempt_id"]`. It scans transition history in reverse and recognizes
only legal T2/T5/T6 entry shapes:

| From | To | Tool |
|---|---|---|
| inbox | active | claim_task |
| review | active | reject_task |
| done | active | reopen_task |

The event must also carry non-empty `by`, string `at`, and a UUID-URN
`attempt_id`. With no legal event it returns the frozen `ATTEMPT_MISMATCH`.
There is no environment variable, test mode, path check, mock driver, or
hard-coded test identity in production.

## 6. REPORT contract alignment

The active-only rejection was removed. When a transition-derived current
attempt exists, REPORT final/replacement writes in active, review, done, and
archive all reject a different attempt with `ATTEMPT_MISMATCH`. An otherwise
valid replacement in review/done/archive is appended under the same family
lock, must reference the unique current head, and does not modify the TASK, old
REPORT, or old T3 event.

The existing T1/inbox compatibility test remains valid: before any active entry,
an inbox TASK may carry an append-only REPORT fact, but it cannot satisfy T3
because T3 requires an active path and transition-derived current attempt. This
preserves existing behavior without restoring a top-level attempt fallback.

## 7. Behavioral quality

New tests call the real public `Project` production entry points. Fixture code
only materializes a completed T5 state that WP3B.1 needs as precondition; it
does not decide receipt relevance or return production results. Monkeypatch is
used only to stop at the private PREPARED/COMMITTED physical crash boundaries.
The two replacement contenders run in spawned processes against the same
workspace and real family lock. No driver result, skip, xfail, or PASS is
fabricated.
