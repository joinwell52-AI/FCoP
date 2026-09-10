---
stage: WP3C
delivery_role: NON_AUTHORITATIVE_REVIEW_MANIFEST
status: REVIEW_READY
authorized_scope: WP3C_ONLY
delivery_head: SELF
gate_self_signed: false
requested_gate: WP3C_AUTHORIZATION_ACCEPTED
---

# FCoP 4.0 WP3C review Manifest

This delivery implements only trusted Profile initialization, Authorization
REVIEW validation/single-use consumption, and T4/T5/T6. It does not implement
T7, convergence, family digest, Branch terminal gates, public recovery/fault
injection, MCP, Schema, CodeFlowMu, main, release, WP3D, or WP4. ADMIN alone may
sign the requested Gate.

## Delivery identity

```yaml
WP3C_STATUS: COMPLETE
AUTHORIZED_SCOPE: WP3C_ONLY
TASKBOOK_REPOSITORY: joinwell52-AI/FCoP
TASKBOOK_BRANCH: task/fcop-4.0-wp3c-authorization-transitions
TASKBOOK_PATH: taskbooks/fcop-4.0/WP3C/01-Authorization-and-Controlled-Transitions-Taskbook.zh.md
TASKBOOK_COMMIT: 46c7d7522f020e85ad658a9e0147578d61fe908a
TASKBOOK_SHA256: 9574b070cc9e850004954e9e5b1d3516c4f73bcaa5ea335da6dd226d31ff1340
CODE_BASELINE: 511039db227a23ae3e2d79aaae775a92ba392f5c
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
WP3B_LIFECYCLE_ACCEPTED: true
WORKTREE: D:/FCoP-wp3c-authorization
BRANCH: review/fcop-4.0-wp3c-authorization-transitions

TRUSTED_PROFILE_INITIALIZATION: PASS
CALLER_AUTHORITY_SMUGGLING: REJECTED
AUTHORIZATION_BINDING: PASS
AUTHORIZATION_SINGLE_USE: PASS
AUTHORIZATION_EXACT_RETRY: PASS
T4_STATUS: COMPLETE
T5_STATUS: COMPLETE
T6_STATUS: COMPLETE
T7_STATUS: NOT_AUTHORIZED

WP3C_TARGET_NODES: 33/33
WP3C_NEW_TESTS: 36/36
WP3B_REGRESSION: PASS
FROZEN_TEST_IDS: 60/60
TEST_FCOP: 1085 passed
V3_REGRESSION: 1402 passed, 2 inherited skips in bound full non-Conformance suite
MCP_REGRESSION: 80 passed
V4_STATIC_META: 27 passed
V4_BEHAVIORAL: 54 passed / 38 deferred / 0 unexpected
V4_TOTAL: 81 passed / 38 deferred
V4_COLLECT_ONLY: 119
UNEXPECTED_FAILURES: 0

NEW_PUBLIC_APIS: 0
NEW_RUNTIME_DEPENDENCIES: 0
NEW_BACKGROUND_COMPONENTS: 0
NEW_AUTHORITATIVE_STORES: 0
NEW_STATE_MACHINES: 0
NEW_PRODUCTION_MODULES: 1
NEW_BASE_ERROR_CODES: 0
V3_METHOD_SIGNATURE_CHANGES: 0
FROZEN_SPEC_FILES_MODIFIED: 0
SCHEMA_FILES_MODIFIED: 0
MCP_IMPLEMENTATION_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0

CONTENT_COMMIT: 212bee4eebe47f760c36294d629a46a2caa5a8dc
MANIFEST_COMMIT: SELF
REMOTE_HEAD: SELF_AFTER_PUSH
REMOTE_PUSHED: VERIFY_IN_FINAL_POST_FETCH_RECEIPT
REMOTE_REFETCH_VERIFIED: VERIFY_IN_FINAL_POST_FETCH_RECEIPT
COMMIT_REACHABILITY: REQUIRE_TASKBOOK_AND_CONTENT_ANCESTORS_OF_FETCHED_SELF
DELIVERY_FILES: 15 content files plus this Manifest
DELIVERY_SHA256: 15/15 CONTENT_BLOBS_LISTED_BELOW
REMOTE_MAIN_BEFORE_DELIVERY: 68dbeb15f4e7f84e1d03f907be9fa66c2265843e

WP3C_AUTHORIZATION_ACCEPTED: false
WP3D_AUTHORIZED: false
WP3D_STARTED: false
MAIN_MERGE_AUTHORIZED: false
MAIN_MODIFIED: false
RELEASE_AUTHORIZED: false
RELEASE_CREATED: false
REQUESTED_GATE: WP3C_AUTHORIZATION_ACCEPTED
```

`SELF` denotes the commit containing this Manifest and avoids a recursive hash.
A committed file cannot truthfully attest a future push/fetch operation. The
final post-fetch receipt resolves `SELF`, remote HEAD, reachability, push state,
remote main stability, and every remote blob hash.

## Content blob hashes

SHA-256 values cover exact Git blob bytes at Content Commit
`212bee4eebe47f760c36294d629a46a2caa5a8dc`. The Manifest is intentionally
excluded from its own recursive hash table.

| SHA-256 | Bytes | File |
|---|---:|---|
| `69e1c49d34ef117b47a89fe69a67d5bfd0d956e5d54d747d12ceeacab15891fe` | 3523 | `reports/FCOP-4.0-WP3C-ATOMICITY-AND-RETRY-PROOF.md` |
| `1ce6b5b5ed0559abd9e54d393e84c359838e6156f9df2debddfecb0be1272083` | 5591 | `reports/FCOP-4.0-WP3C-AUTHORIZATION-MODEL.md` |
| `96f91dadd6a8a81bd2fb099ca3033d522db825c21650ed59a19ee20ecd8675ae` | 5193 | `reports/FCOP-4.0-WP3C-CONFORMANCE-ALIGNMENT.md` |
| `2cd577cc3fd3763df68a481f9a50381863ea1e9dd4e14388014d2598d4ad5e34` | 3556 | `reports/FCOP-4.0-WP3C-IMPLEMENTATION-PLAN.md` |
| `fd0e3d5c834ac326c82f279e76e8fdb8dce67cac3926c9f2c96511636adc9fb6` | 3944 | `reports/FCOP-4.0-WP3C-RESULT.md` |
| `320f89afb4ba08ad97f4ce0a7c019b8e5a56bc04fbf5b9e937df70c6e08564de` | 263617 | `src/fcop/project.py` |
| `f0a101dc121ce5b84babb08dfde4d4055ec62ae067b5bb1a6cc76a50d173099f` | 11507 | `src/fcop/v4/authorization.py` |
| `4212205f9199e123629239a4b21a1c81faa2edc20bf6c23547b033eec7979857` | 36346 | `src/fcop/v4/creation.py` |
| `3cc3f1f53adad7a741e976588e6f4c709d0faa6837a0a023e08e28d61703bfb6` | 25199 | `src/fcop/v4/lifecycle.py` |
| `8dbe9bbb877b17a748e7667b2874521fd1505a0d838e5e798db5eb634125a397` | 13628 | `src/fcop/v4/receipts.py` |
| `4bc0dcfcf343b271381d2e07ac55a53105ace5fb2092ae410a7961e9b1f469fd` | 10546 | `tests/conformance/v4/fixtures.py` |
| `0037aebbe1ae1a6b7098eb82e0f6404dc7a8dc7581ae875d33c7dd8956e05a25` | 12112 | `tests/conformance/v4/test_c3_lifecycle.py` |
| `4973611891e354c973ad6f6e315746792b9eeffa241160dea7ea238bd5f3b273` | 17488 | `tests/conformance/v4/test_c6_authorization.py` |
| `69d4607fca9d0512f515cba49e1ab941241483d512a830686f3c041ce3769a7c` | 19750 | `tests/conformance/v4/test_c8_recovery.py` |
| `93d48db5bd0eb1e593cd4ff4a854ec5cd956fe0113db393277eed14618cd1c6b` | 16228 | `tests/test_fcop/test_v4_authorization.py` |

## WP3C target nodes

- C3: `C3-N02`, `C3-GATE-01[T4]`, `C3-GATE-01[T5]`, `C3-GATE-01[T6]`.
- C6: `C6-N01`, `test_c6_profile_evaluator_rejects[DENIED]`,
  `test_c6_profile_evaluator_rejects[UNKNOWN]`,
  `test_c6_caller_cannot_replace_trusted_profile[profile_evaluator]`,
  `[profile_resolver]`, `[trusted_profiles]`, `[caller_judge]`,
  `C6-R02[expired]`, `C6-R02[reused]`, `C6-PROFILE-01`,
  `C6-SPOOF-01`, `C6-DIGEST-01`.
- C8: `C8-RETRY-01[T4]`, `C8-RETRY-01[T5]`, `C8-RETRY-01[T6]`.
- WP2.1b Meta: `test_registry_crosses_initialization_only`;
  `test_business_adapter_rejects_caller_authority` for each of
  `{profile_evaluator, profile_resolver, trusted_profiles, caller_judge}` ×
  `{transition, create_task, recover_operation}`; and
  `test_existing_production_business_signatures_do_not_advertise_judges`.

All 33 pass. The 60 frozen Test IDs and 119 collected nodes are unchanged.

## Deferred nodes and exact cause

| Nodes | Cause outside WP3C |
|---|---|
| `C3-N01`, `C3-GATE-01[T7]` | Both reach the deliberately unimplemented T7 edge |
| `C3-X01` | Cold export and public fault injection |
| `C4-R01[dangling-gate-reference]` | Inherited C4 create/gate-reference behavior; WP3C cannot alter C4 creation |
| `C5-N02` | Convergence, family digest, and Root T7 |
| `C5-R03`, `C5-X01` | Stale convergence evaluation |
| `C5-BRANCH-01` | Branch terminal gate |
| `C5-ARCHIVED-01` | T7 archive/cold export |
| `C5-FAMILY-DIGEST-01` | family_digest implementation |
| `C5-REPORT-RACE-01` | REPORT-driven convergence/family invalidation |
| `C6-R01[missing]`, `[actor-admin-only]`, `[wrong-subject]`, `[wrong-edge]`, `[wrong-attempt]` | These five parameter nodes exclusively construct T7; equivalent T4/T5/T6 binding cases pass in WP3C unit coverage |
| `C6-X01` | T7 authorization response-loss/public fault injection |
| `C7-CREATE-01` | Inherited second-T2 expectation conflicts with existing WP3B receipt Existing result; not introduced by WP3C |
| `C8-X01[PREPARED]`, `[TARGET_DURABLE]`, `[COMMITTED]`, `[RESPONSE_LOST]` | Public fault injection/recover operation |
| `C8-X03[divergent]`, `[corrupt-receipt]`, `[unsupported-filesystem]` | Public recovery error branches |
| `C8-RETRY-01[T7]` | T7 retry |
| `C8-STATE-01[S1]`, `[S2]`, `[S3]`, `[S4]`, `[S5]` | Public five-state recovery surface |
| `C8-INDETERMINATE-01` | Public recovery indeterminate branch |
| `AT-05[PREPARED]`, `[TARGET_DURABLE]`, `[RESPONSE_LOST]` | Public fault injection |
| `AT-06[S2]`, `[S4]`, `[S5]` | Public recover_operation |

These are exactly the 38 failures in the final complete v4 run. No target or
start-point pass regressed.

## Verification evidence

- New unit: 36 passed; lifecycle: 47 passed; creation: 94 passed.
- Bound non-Conformance: 1402 passed, 2 inherited legacy-fixture skips.
- Isolated MCP: 80 passed.
- Core mypy: win32/linux/darwin each PASS over 37 source files; MCP mypy PASS
  over 17 source files; changed-file Ruff and `git diff --check` PASS.
- Independent temporary production smoke completed T1/T2/T3/T4/T6/T3/T5 and
  proved three distinct attempts.
- Native Windows spawn T4/T5 race and T4/T5/T6 response-loss retry: 4 passed.
- Frozen English/Chinese specs match Frozen Contract Commit; Schema, MCP,
  taskbooks, dependency/build files, CodeFlowMu, and main were not modified.

## Required post-push verification

Push without force, fetch the review branch again, and require fetched HEAD to
equal local `SELF`; Content must be its direct parent and Taskbook Commit the
direct parent of Content. Verify the Manifest commit changes only this file,
all 15 remote content blobs match the table, the remote Manifest bytes match
local bytes, remote main remains
`68dbeb15f4e7f84e1d03f907be9fa66c2265843e`, and the worktree is clean. Then
stop and request `WP3C_AUTHORIZATION_ACCEPTED`.
