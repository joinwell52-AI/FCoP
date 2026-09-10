---
stage: WP3A
delivery_role: NON_AUTHORITATIVE_REVIEW_MANIFEST
status: REVIEW_READY
authorized_scope: WP3A_ONLY
delivery_head: SELF
gate_self_signed: false
requested_gate: WP3A_IMPLEMENTATION_ACCEPTED
---

# FCoP 4.0 WP3A GitHub review manifest

Creation plane only. No WP3B execution, main merge, release, frozen-file edits
or CodeFlowMu changes. ADMIN decides acceptance.

## Delivery identity

```yaml
WP3A_STATUS: LOCAL_VERIFIED_REMOTE_CHECK_PENDING_AT_MANIFEST_CREATION
AUTHORIZED_TASKBOOK: D:/FCoP/docs/fcop-architecture-series/FCoP-4.0-WP3-Implementation-Master-Taskbook.zh.md
AUTHORIZED_TASKBOOK_SHA256: 2fdc907703fabb60c4ce89092588fbdc86bf821fb05007c9165a5b0593b2d99c
START_POINT: ffbfa0084f9b2758d95a09ecfbd89120b77b13cf
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
CONFORMANCE_INPUT_HEAD: ffbfa0084f9b2758d95a09ecfbd89120b77b13cf
BRANCH: review/fcop-4.0-wp3a-creation-plane
CONTENT_COMMIT: 56958f6575e284bf8f244f008cac4b19d13d8dfe
MANIFEST_COMMIT: SELF
REMOTE_HEAD: SELF_AFTER_SUCCESSFUL_PUSH_AND_FETCH
REMOTE_PUSHED: VERIFY_IN_FINAL_POST_FETCH_RECEIPT
REMOTE_REFETCH_VERIFIED: VERIFY_IN_FINAL_POST_FETCH_RECEIPT
COMMIT_REACHABILITY: REQUIRE_INPUT_AND_CONTENT_ANCESTORS_OF_FETCHED_SELF
DELIVERY_FILES: 11 content files plus this Manifest
DELIVERY_SHA256: 11 content Git blobs listed below
AUTHORIZED_FILES: 12
UNAUTHORIZED_FILES: 0
FROZEN_FILES_MODIFIED: 0
FROZEN_SHA256: 48/48 matched input after checkout EOL normalization in memory
V3_REGRESSION: 1273 passed, 2 skipped (1225 baseline plus 48 new)
V3_NEW_FAILURES: 0
V4_STATIC_META: 27 passed
V4_BEHAVIORAL_TOTAL: 92 nodes; 25 passed, 67 expected future-stage failures
WP3A_TARGET_IDS: 10/10
WP3A_TARGET_IDS_PASSED: 10/10
UNEXPECTED_PASSES: 15 incidental nodes explained in result report; no later-stage completion
UNEXPECTED_FAILURES: 0 in WP3A targets, static/meta or regression
CONCURRENCY_TESTS: PASS; same-key same/different digest spawn races, fresh-process retry, bounded kernel-lock timeout
NEW_RUNTIME_DEPENDENCIES: 0
NEW_BACKGROUND_COMPONENTS: 0
NEW_AUTHORITATIVE_STORES: 0
CODEFLOWMU_FILES_MODIFIED: 0
MAIN_MODIFIED: false
MAIN_BEFORE_DELIVERY: 68dbeb15f4e7f84e1d03f907be9fa66c2265843e
RELEASE_CREATED: false
WP3B_STARTED: false
REQUESTED_GATE: WP3A_IMPLEMENTATION_ACCEPTED
```

SELF denotes the commit containing this Manifest. It cannot recursively
embed its own SHA or attest a push that has not happened at commit time.
The final receipt must resolve SELF to an exact SHA, confirm remote equality,
and report the actual post-fetch outcome. LOCAL_VERIFIED alone is not COMPLETE.
This is the same non-recursive delivery convention used by the input Manifest.

## Content hashes

Hashes are SHA-256 of committed Git blob bytes, not platform-converted
checkout text. This Manifest is deliberately excluded from its own hash list.
The only change from CONTENT_COMMIT to SELF must be this file.

| SHA-256 | Bytes | File |
|---|---:|---|
| `99ad3cf154f565891b59a3f26115403406fb74183a59b4a53e645f8bcfacb4b6` | 8246 | `reports/FCOP-4.0-WP3A-ARCHITECTURE-DELTA.md` |
| `ff727986376aa53943263bf2cccfbbaa52dc214ab639435c48b406eb592a20fa` | 8156 | `reports/FCOP-4.0-WP3A-IMPLEMENTATION-PLAN.md` |
| `e156a579cad39a7433fe6c1b6ea455dd6b03a0cb2ec1261b85446e39243766d8` | 9178 | `reports/FCOP-4.0-WP3A-IMPLEMENTATION-RESULT.md` |
| `33e42837ceaca9825effc86af26229ec7a9023e0435f5aa3f683474df2c27aa0` | 7319 | `src/fcop/errors.py` |
| `51a418f88f397fc768ca63a1b1a910eef656335578f5a96039a73bd27c93502a` | 263300 | `src/fcop/project.py` |
| `33e70ee3bbe8d663d52fd62fb3588eee63e2700a00bd9711caada55bcbba0a91` | 70 | `src/fcop/v4/__init__.py` |
| `27416f0f11cd8ae448bffeeefe78c96eda8576d83a1ccb1879172494b2223c47` | 2758 | `src/fcop/v4/boundary.py` |
| `e22875ff84d85ff12ea6cf5f398f3f5993c0c95ce08fdfb221158063947850df` | 30576 | `src/fcop/v4/creation.py` |
| `e5fec1259bce2a670b6ed9d52de539a6bd64bb09e76c665543a1b6937f040144` | 12307 | `src/fcop/v4/encoding.py` |
| `acc8424b64e09876e3fbbd21b3e144578173b79192c3824afdaf38df7e272edb` | 51493 | `tests/test_fcop/snapshots/public_surface.json` |
| `da8f8c7409f303881535f51f5a8bb6354608529a26f82df6ba5741ceadcb7f39` | 17433 | `tests/test_fcop/test_v4_creation.py` |

## Review focus

1. Single Project version boundary, preserving all 38 old method signatures;
   only creation APIs and explicit unavailable-operation boundaries added.
2. Exactly four envelopes and one T1 event, with an immutable result fact.
3. Distinct operation key and canonical request digest; real cross-process
   same-key concurrency and durable Existing, not an in-memory/surface probe.
4. Caller logic cannot register or execute Profile evaluators through business
   requests. No authorization or lifecycle migration implementation lands.
5. C5-FAMILY-RACE-01 and AT-04 currently permit an unavailable transition plus
   a successful creation. Their green status is explicitly not proof of family
   locking or convergence. No frozen tests are changed to mask that limitation.
6. Root Ruff has 21 pre-existing frozen-test diagnostics, reproduced at input.
   Modified-file/MCP lint and all requested type checks pass.
7. Native evidence is Windows/NTFS. Linux/macOS are type-checked, not claimed
   natively executed. Existing workflows do not trigger on review-branch pushes.

## Remote verification procedure

After committing this file, push only the authorized review branch, then fetch
origin again. Resolve local HEAD and the fetched review ref and require equality.
Require both input and content commits to be ancestors; require the Manifest
commit's parent to equal CONTENT_COMMIT; require the final diff to contain only
this Manifest. Re-read this file from the fetched GitHub object and verify all
11 content blobs against the table, also comparing every fetched blob with
CONTENT_COMMIT. Verify main remains at MAIN_BEFORE_DELIVERY, the worktree is
clean, and the overall 12-file diff is inside the explicit inventory.

The final receipt, not this pre-push text, records REMOTE_PUSHED=true,
REMOTE_REFETCH_VERIFIED=PASS, exact REMOTE_HEAD and DELIVERY_SHA256=11/11.
Stop immediately after successful delivery and request
`WP3A_IMPLEMENTATION_ACCEPTED`; do not start WP3B.
