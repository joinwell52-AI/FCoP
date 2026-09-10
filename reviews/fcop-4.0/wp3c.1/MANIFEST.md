---
stage: WP3C.1
delivery_role: NON_AUTHORITATIVE_REVIEW_MANIFEST
status: REVIEW_READY
authorized_scope: WP3C_1_ONLY
delivery_head: SELF
gate_self_signed: false
requested_gate: WP3C_AUTHORIZATION_ACCEPTED
---

# FCoP 4.0 WP3C.1 review Manifest

This delivery closes only the three WP3C authorization findings fixed by the
authorized WP3C.1 Taskbook: carrier/edge binding, expiry linearization after
the trusted evaluator, and recovery-time receipt/Profile rebinding. It does
not enter WP3D or WP4. ADMIN alone may sign the requested Gate.

## Delivery identity

```yaml
WP3C_1_STATUS: COMPLETE
AUTHORIZED_SCOPE: WP3C_1_ONLY
TASKBOOK_REPOSITORY: joinwell52-AI/FCoP
TASKBOOK_BRANCH: task/fcop-4.0-wp3c.1-authorization-closeout
TASKBOOK_PATH: taskbooks/fcop-4.0/WP3C.1/01-Authorization-Carrier-and-Expiry-Linearization-Closeout-Taskbook.zh.md
TASKBOOK_COMMIT: 2569e452824e41094b46e03c4b2a80930f8f01dc
TASKBOOK_SHA256: b7bbdde6448d098998619a9cf21732a7526c0c1414d363cf261503d5c03c3ec9
INPUT_HEAD: bd61efeb04d3cfe52b02c433226492e07a525fce
WP3C_CONTENT_COMMIT: 212bee4eebe47f760c36294d629a46a2caa5a8dc
WP3C_MANIFEST_COMMIT: bd61efeb04d3cfe52b02c433226492e07a525fce
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
WORKTREE: D:/FCoP-wp3c1-auth-closeout
WORKTREE_BASELINE: CLEAN
BRANCH: review/fcop-4.0-wp3c.1-authorization-closeout

AUTHORIZATION_KIND_EDGE_MATRIX: PASS
REOPEN_AS_AUTHORIZATION: REJECTED
POST_EVALUATOR_EXPIRY_CHECK: PASS
EXPIRED_ZERO_WRITE: PASS
EXPIRED_EXACT_RETRY: EXISTING
RECEIPT_PROFILE_BINDING: PASS
WP3C_REGRESSION: PASS
V3_NEW_FAILURES: 0

WP3C_1_NEW_TESTS: 10/10
WP3C_TARGET_NODES: 10/10
FROZEN_TEST_IDS: 60/60
TEST_FCOP: 1095 passed
V3_REGRESSION: 1412 passed, 2 inherited skips in bound full non-Conformance suite
MCP_REGRESSION: 80 passed
V4_STATIC_META: 27 passed
V4_BEHAVIORAL: 53 passed / 38 inherited deferred / 1 taskbook-corrected expected red / 0 unexpected
V4_TOTAL: 80 passed / 39 expected red
V4_COLLECT_ONLY: 119
UNEXPECTED_FAILURES: 0

NEW_PUBLIC_APIS: 0
NEW_RUNTIME_DEPENDENCIES: 0
NEW_BACKGROUND_COMPONENTS: 0
NEW_AUTHORITATIVE_STORES: 0
NEW_STATE_MACHINES: 0
NEW_PRODUCTION_MODULES: 0
NEW_BASE_ERROR_CODES: 0
FROZEN_SPEC_FILES_MODIFIED: 0
SCHEMA_FILES_MODIFIED: 0
CONFORMANCE_FILES_MODIFIED: 0
MCP_IMPLEMENTATION_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0

CONTENT_COMMIT: 3c817d47bda21a4acd5992861d84f5ee4366ccbb
MANIFEST_COMMIT: SELF
REMOTE_HEAD: SELF_AFTER_PUSH
REMOTE_PUSHED: VERIFY_IN_FINAL_POST_FETCH_RECEIPT
REMOTE_REFETCH_VERIFIED: VERIFY_IN_FINAL_POST_FETCH_RECEIPT
COMMIT_REACHABILITY: REQUIRE_INPUT_AND_CONTENT_ANCESTORS_OF_FETCHED_SELF
DELIVERY_FILES: 6 content files plus this Manifest
DELIVERY_SHA256: 6/6 CONTENT_BLOBS_LISTED_BELOW
REMOTE_MAIN_BEFORE_DELIVERY: 68dbeb15f4e7f84e1d03f907be9fa66c2265843e

WP3C_AUTHORIZATION_ACCEPTED: false
WP3D_AUTHORIZED: false
WP3D_STARTED: false
WP4_STARTED: false
MAIN_MERGE_AUTHORIZED: false
MAIN_MODIFIED: false
RELEASE_AUTHORIZED: false
RELEASE_CREATED: false
REQUESTED_GATE: WP3C_AUTHORIZATION_ACCEPTED
```

`SELF` denotes the commit containing this Manifest and avoids a recursive
hash. A committed file cannot truthfully attest a future push/fetch operation;
the final post-fetch receipt resolves `SELF`, remote HEAD, reachability, push
state, remote main stability, and every remote blob hash.

## Content blob hashes

SHA-256 values cover exact Git blob bytes at Content Commit
`3c817d47bda21a4acd5992861d84f5ee4366ccbb`. The Manifest is intentionally
excluded from its own recursive hash table.

| SHA-256 | Bytes | File |
|---|---:|---|
| `0bdbda0fdd440a7b0543b80e69ec9e7a8b14d5eb763e00e8df15a1580f98ac6d` | 2896 | `reports/FCOP-4.0-WP3C.1-AUTHORIZATION-MATRIX.md` |
| `016431753bae88f1b2c68f1b6bb0bb3ea364ea70f273df56a3fef01b5a0faae5` | 3633 | `reports/FCOP-4.0-WP3C.1-CORRECTION-RESULT.md` |
| `ae04a8b5cacfd40d3171c8663daa4d20bba6bc9eaa9c55777f10436061b9cd54` | 2705 | `reports/FCOP-4.0-WP3C.1-EXPIRY-AND-RECOVERY-PROOF.md` |
| `dd0023e82e3e44ff9a0fac98c04e048ccaa4833a0e9b81885b28a51e061ce018` | 12133 | `src/fcop/v4/authorization.py` |
| `a005c64bf45de85e0f905324c5e13f44ddccadb116b4fca26d31ac40d2480d57` | 25565 | `src/fcop/v4/lifecycle.py` |
| `b779a6dde005278cb361b13f6b310c60df7a957b86f3234f15d441fa94fbfe18` | 23548 | `tests/test_fcop/test_v4_authorization.py` |

## Corrected Conformance expectation

The frozen `C3-GATE-01[T6]` fixture still supplies a `reopen` REVIEW as both
`review_ref` and `authorization_ref`. WP3C.1 explicitly requires that exact
arrangement to return `AUTHORIZATION_INVALID`, while also forbidding any edit
to frozen Conformance. The resulting single new red node is therefore recorded
separately from the 38 inherited deferred nodes. Both permitted T6 arrangements
pass direct production-entry tests, frozen Test IDs remain 60/60, and no
Conformance file changed. There are zero unexpected failures.

## Verification evidence

- Pre-fix WP3C.1 run: 5 failed / 5 passed; post-fix: 10 passed.
- WP3C authorization unit: 46 passed; lifecycle: 47 passed; creation: 94 passed.
- Bound non-Conformance: 1412 passed, 2 inherited legacy-fixture skips.
- Isolated MCP: 80 passed.
- Core mypy win32/linux/darwin each passed over 37 source files; MCP mypy
  passed over 17 source files; changed-file Ruff and `git diff --check` passed.
- Native Windows expiry/recovery/race/response-loss target set: 7 passed.
- Frozen English/Chinese specs match the Frozen Contract Commit; Schema,
  Conformance, MCP, taskbooks, dependencies, build/release files, CodeFlowMu,
  and main were not modified.

## Required post-push verification

Push without force, fetch the review branch again, and require fetched HEAD to
equal local `SELF`; Content must be its direct parent and `INPUT_HEAD` the
direct parent of Content. Verify that the Manifest commit changes only this
file, all six remote content blobs match the table, the remote Manifest bytes
match local bytes, remote main remains
`68dbeb15f4e7f84e1d03f907be9fa66c2265843e`, and the worktree is clean. Then
stop and request `WP3C_AUTHORIZATION_ACCEPTED`.
