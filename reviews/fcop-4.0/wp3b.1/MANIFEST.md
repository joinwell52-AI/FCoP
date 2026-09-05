---
stage: WP3B.1
delivery_role: NON_AUTHORITATIVE_REVIEW_MANIFEST
status: REVIEW_READY
authorized_scope: WP3B_1_ONLY
delivery_head: SELF
gate_self_signed: false
requested_gate: WP3B_LIFECYCLE_ACCEPTED
---

# FCoP 4.0 WP3B.1 review Manifest

This delivery corrects only WP3B receipt round identity, current-attempt fact
source, Conformance fixture alignment, and the REPORT state boundary. It does
not implement WP3C, T4-T7, authorization, convergence, MCP, Schema, CodeFlowMu,
main, or release changes. ADMIN alone may sign the requested Gate.

## Delivery identity

```yaml
WP3B_1_STATUS: COMPLETE
AUTHORIZED_SCOPE: WP3B_1_ONLY
TASKBOOK_REPOSITORY: joinwell52-AI/FCoP
TASKBOOK_PATH: taskbooks/fcop-4.0/WP3B.1/01-Lifecycle-Round-Contract-Correction-Taskbook.zh.md
TASKBOOK_COMMIT: 48082cd1c7e96cce7f1da8c7677ba4caf7ab8c74
TASKBOOK_SHA256: 26eb81dd022758cfc9a55c4eaf1cf637486175d873b2f65eae6ac2ad5b3c07c5
INPUT_HEAD: 297dc06ece87f1d4adf938875cb19e59be87def0
WP3B_CONTENT_COMMIT: 6bdde7038f124e2a6c0895166a2f76fad05fc860
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
WORKTREE: D:/FCoP-wp3b1-round-correction
BRANCH: review/fcop-4.0-wp3b.1-lifecycle-round-correction

RECEIPT_ROUND_IDENTITY: PASS
HISTORICAL_RECEIPT_REUSE: PASS
CURRENT_ATTEMPT_SOURCE: TRANSITION_ONLY
TOP_LEVEL_ATTEMPT_FALLBACK: REMOVED
CONFORMANCE_ALIGNMENT: PASS
REPORT_STATE_POLICY: CONTRACT_ALIGNED

WP3B_TARGET_NODES: 9/9
WP3B_1_NEW_TESTS: 15/15
FROZEN_TEST_IDS: 60/60
V3_REGRESSION: 1366 passed, 2 inherited skips in full non-Conformance suite
MCP_REGRESSION: 80 passed
V4_STATIC_META: 27 passed
V4_BEHAVIORAL: 35 passed / 57 expected later-stage failures
V4_TOTAL: 62 passed / 57 expected later-stage failures
V4_COLLECT_ONLY: 119
UNEXPECTED_FAILURES: 0

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
WP3C_STARTED: false
RELEASE_CREATED: false

CONTENT_COMMIT: b4648d223c2303997fe394c30feaa68e070264d2
MANIFEST_COMMIT: SELF
REMOTE_HEAD: SELF_AFTER_PUSH
REMOTE_PUSHED: VERIFY_IN_FINAL_POST_FETCH_RECEIPT
REMOTE_REFETCH_VERIFIED: VERIFY_IN_FINAL_POST_FETCH_RECEIPT
COMMIT_REACHABILITY: REQUIRE_INPUT_TASKBOOK_AND_CONTENT_ANCESTORS_OF_FETCHED_SELF
DELIVERY_FILES: 10 content files plus this Manifest
DELIVERY_SHA256: 10/10 CONTENT_BLOBS_LISTED_BELOW
REMOTE_MAIN_BEFORE_DELIVERY: 68dbeb15f4e7f84e1d03f907be9fa66c2265843e
REQUESTED_GATE: WP3B_LIFECYCLE_ACCEPTED
```

`SELF` denotes the commit containing this Manifest and avoids a recursive hash.
A committed file cannot truthfully attest a future push/fetch operation, so the
final post-fetch execution receipt resolves `SELF`, remote HEAD, reachability,
push status, and every remote blob hash.

## Content blob hashes

SHA-256 values cover exact LF-normalized Git blob bytes at Content Commit
`b4648d223c2303997fe394c30feaa68e070264d2`. The Manifest is intentionally
excluded from its own recursive hash table.

| SHA-256 | Bytes | File |
|---|---:|---|
| `fca0724e5e7b32f242b9ceff49011a715966324fafee092ddfd8c6f0e8193211` | 5285 | `reports/FCOP-4.0-WP3B.1-CONTRACT-TEST-ALIGNMENT.md` |
| `099436b8645ac87d3c73fc9402313b347581c8b86bec3ae38788b2f9b4ae9c55` | 7447 | `reports/FCOP-4.0-WP3B.1-CORRECTION-PLAN.md` |
| `9983075b9348265669cd319de7cc3f4ac9ebcc183e9ba18176d18acb5a461fa4` | 6546 | `reports/FCOP-4.0-WP3B.1-CORRECTION-RESULT.md` |
| `a22dd3f2f6efa6aa8d6be3a43aef0c1591ea87d772722f8a0cee1f6b5f1e3718` | 6255 | `reports/FCOP-4.0-WP3B.1-RECEIPT-ROUND-PROOF.md` |
| `639e62411723265d06e82fe4ccfe2859a9ca8c38ad9a437efe40b23916738161` | 35566 | `src/fcop/v4/creation.py` |
| `18ea50951903225e7412ca3099f786e359ae562ee36027cb6f47c0e915816a98` | 18931 | `src/fcop/v4/lifecycle.py` |
| `4282f38cd01720b9af7550e8c11fdf3880f28c875aef3198d6ff9f39dbb7ebb8` | 9878 | `src/fcop/v4/receipts.py` |
| `a1056c34e601e71bb8fcbf512aeaf4b98efed1b450ac60adc387d1b66f29f5fc` | 9617 | `tests/conformance/v4/fixtures.py` |
| `23d0a9ca7d7796a07571580e4b1bec1859ea1779fe37833552654cf7215fd857` | 11009 | `tests/conformance/v4/test_c3_lifecycle.py` |
| `aef76d9727f7a0dc4eaf113340fafe712b37b9a73c7f259f8b3659de5931283c` | 37966 | `tests/test_fcop/test_v4_lifecycle.py` |

## Review focus

1. T3 receipt selection uses the transition-derived visible attempt, not the
   lifetime TASK/edge pair, and never uses mtime or directory order as winner.
2. Historical committed receipts remain byte-for-byte present while current
   PREPARED/TARGET_DURABLE/COMMITTED receipts recover independently.
3. `current_attempt()` accepts only legal T2/T5/T6 entry-to-active events and no
   longer reads top-level `attempt_id`.
4. Fixture alignment changes persistent arrangement only. The 60 frozen Test
   IDs, 119 nodes, actions, expected errors, and pass/fail split are unchanged.
5. REPORT replacement is append-only and current-attempt checked in review,
   done, and archive without prematurely implementing later evidence Gates.
6. The 15 new test nodes exercise real `Project` methods, a real spawned-process
   replacement race, and private fault stops only at physical receipt stages.

## Required remote verification

Push this review branch without force, fetch it again, and require the fetched
HEAD to equal local `SELF`. Verify that Input HEAD, Taskbook Commit, and Content
Commit are ancestors; Content is the direct parent of Manifest; their sole
difference is this Manifest; all 11 delivery paths and ten Content blob
byte/SHA-256 pairs match; frozen specs and `origin/main` remain unchanged; and
the worktree is clean. Then stop and request `WP3B_LIFECYCLE_ACCEPTED`.
