---
stage: WP3A.1
delivery_role: NON_AUTHORITATIVE_REVIEW_MANIFEST
status: REVIEW_READY
authorized_scope: WP3A_1_ONLY
delivery_head: SELF
gate_self_signed: false
requested_gate: WP3A_IMPLEMENTATION_ACCEPTED
---

# FCoP 4.0 WP3A.1 review Manifest

Four-item boundary/initialization closeout, with ADMIN's explicit legacy CRLF
clarification. No WP3B work, main merge, tag, release, workspace migration or
CodeFlowMu change. ADMIN alone signs the implementation acceptance Gate.

## Delivery identity

```yaml
WP3A_1_STATUS: LOCAL_VERIFIED_REMOTE_CHECK_PENDING_AT_MANIFEST_CREATION
AUTHORIZED_SCOPE: WP3A_1_ONLY
AUTHORIZED_TASKBOOK_SHA256: 5f21440a88d90f5975a52db22fd37863595658b904eba3e3e1c03c408f69cb5f
ADMIN_CLARIFICATION: WP3A_1_MANIFEST_LINE_ENDING_COMPATIBILITY
ADMIN_CLARIFICATION_DECISION: APPROVED
LEGACY_MANIFEST_CRLF: ALLOWED
V4_MANIFEST_CRLF: REJECTED
DUPLICATE_JSON_KEYS: REJECTED_FOR_ALL_VERSION_CLASSIFICATION
INPUT_HEAD: 20b9fc25b66b6d52b9f7c761db5a18e1379794b8
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
CONFORMANCE_INPUT_HEAD: ffbfa0084f9b2758d95a09ecfbd89120b77b13cf
WORKTREE: D:/FCoP-wp3a1-boundary-closeout
BRANCH: review/fcop-4.0-wp3a.1-boundary-initialization
CONTENT_COMMIT: 0d4589d8d7b52e9ace8a33d782223284d5dffe3f
MANIFEST_COMMIT: SELF
REMOTE_HEAD: SELF_AFTER_SUCCESSFUL_PUSH_AND_FETCH
REMOTE_PUSHED: VERIFY_IN_FINAL_POST_FETCH_RECEIPT
REMOTE_REFETCH_VERIFIED: VERIFY_IN_FINAL_POST_FETCH_RECEIPT
COMMIT_REACHABILITY: REQUIRE_INPUT_AND_CONTENT_ANCESTORS_OF_FETCHED_SELF
DELIVERY_FILES: 8 content files plus this Manifest
DELIVERY_SHA256: 8 committed content blobs listed below
AUTHORIZED_FILES: 9
UNAUTHORIZED_FILES: 0
FROZEN_FILES_MODIFIED: 0
FROZEN_SHA256: 24/24 actual spec-WP1-conformance files matched input
P0_MANIFEST_FAIL_OPEN: RESOLVED
P0_WORKSPACE_PARTIAL_VISIBILITY: RESOLVED
P1_OPERATION_PATH_PORTABILITY: RESOLVED
P1_DESCRIPTOR_COMPATIBILITY: NARROWED
WP3A_TARGET_IDS_PASSED: 10/10
WP3A_1_TESTS: 46 passed
V3_REGRESSION: 1319 passed, 2 skipped
V3_NEW_FAILURES: 0
MCP_REGRESSION: 80 passed
V4_STATIC_META: 27 passed
V4_BEHAVIORAL: 25 passed / 67 deferred failures / 0 new failures
V4_COLLECT_ONLY: 119
FROZEN_TEST_IDS: 60/60
RUFF_BASELINE: 21 inherited frozen-test diagnostics; changed-file and MCP lint PASS
MYPY: PASS for core Windows-Linux-Darwin targets and MCP source/tests
NEW_RUNTIME_DEPENDENCIES: 0
NEW_BACKGROUND_COMPONENTS: 0
NEW_AUTHORITATIVE_STORES: 0
NEW_PUBLIC_APIS: 0
PUBLIC_APIS_REMOVED: 0
V3_METHOD_SIGNATURE_CHANGES: 0
CODEFLOWMU_FILES_MODIFIED: 0
MAIN_MODIFIED: false
MAIN_BEFORE_DELIVERY: 68dbeb15f4e7f84e1d03f907be9fa66c2265843e
RELEASE_CREATED: false
TAG_CREATED: false
PR_MERGED: false
WP3B_STARTED: false
NATIVE_WINDOWS_TESTED: true
LINUX_TYPE_CHECKED: true
MACOS_TYPE_CHECKED: true
NATIVE_LINUX_TESTED: false
NATIVE_MACOS_TESTED: false
REQUESTED_GATE: WP3A_IMPLEMENTATION_ACCEPTED
```

SELF is the commit containing this Manifest. Its own hash cannot recursively
appear inside it, and a pre-push file cannot attest a future remote operation.
The final post-fetch receipt resolves exact SELF and remote HEAD, and confirms
actual push/reachability/hash results. LOCAL_VERIFIED alone is not COMPLETE.

## Content hashes

SHA-256 values cover Git blob bytes, not platform-translated checkouts. This
Manifest is excluded from its own content hash table. The only difference
between CONTENT_COMMIT and SELF must be this Manifest.

| SHA-256 | Bytes | File |
|---|---:|---|
| `1d3ffadbcb523108d50677a798f98535696d4314a5421892763476cce8dd42e0` | 10643 | `reports/FCOP-4.0-WP3A.1-COMPATIBILITY-DECISION.md` |
| `46323756039b7d32d13330ace056530498bcc26bd3ba9743bd294b02bbfee836` | 9731 | `reports/FCOP-4.0-WP3A.1-CORRECTION-PLAN.md` |
| `9b95ac4f73d711ca34868a23576b91183ab449d003b87bc6ce72dba53c128eb9` | 10600 | `reports/FCOP-4.0-WP3A.1-CORRECTION-RESULT.md` |
| `9fbc5e869bd3b40255bcbb385a6e2bb214a4d037f77ebf9299f02ea51fd53d7b` | 263465 | `src/fcop/project.py` |
| `504f404edbc9a964ac36fc65a42593f28632574958fc6ec5725e3e5e23e2ec28` | 5823 | `src/fcop/v4/boundary.py` |
| `90b151162922fb82702b5b7d7fc1dd9beca65c1a41651acd6ebcbf547bcf5e1f` | 32569 | `src/fcop/v4/creation.py` |
| `2dda48c42b9d76fc3b2759c519cfee08651f26388c3434603cf667d4951271cd` | 15475 | `src/fcop/v4/encoding.py` |
| `7554aa0eaa981014fc4716cc952b048b541bcbc8bc0259ede523ea411f76cb74` | 37131 | `tests/test_fcop/test_v4_creation.py` |

## Review focus and limitations

1. Unique-key strict UTF-8 classification happens before version-specific
   Encoding; legacy CRLF stays legal, v4 CRLF does not. Business requests do
   not select a version.
2. Canonical fcop/ is published only after complete staging, with a real
   no-replace directory primitive. Failed staging is retained, not aged out.
   Two spawned creators race real operations; only one canonical result wins.
3. Operation fact paths are Project-relative POSIX values. A moved temporary
   project retries the same request without changing facts or adding a TASK.
4. Original 38 v3 method bodies/signatures/docs and the public snapshot remain
   unchanged. Explicit policies replace automatic descriptor installation.
   v4 bound signatures are their handlers; class and legacy remain compatible.
5. Class/legacy-object and v4 bound-method autospec are tested. Whole-object v4
   autospec still encounters the existing unsupported legacy config property;
   no new config API or property behavior is smuggled into this package.
6. All 11 prior v3 and four prior v4 candidate failures are closed. Historical
   failed iterations remain documented in the plan/decision; no failed content
   commit was made. All original 48 creation tests retain their source text.
7. The 67 later-stage behavior failures and 15 incidental WP3A passes remain
   unchanged, not reclassified as completed lifecycle/authorization/family work.
8. Root Ruff has 21 pre-existing frozen diagnostics. Native POSIX verification
   remains a pre-merge/release gate; type checking is not native execution.

## Remote verification procedure

Push only the new review branch without force, then fetch origin. Require
fetched review HEAD == local HEAD; INPUT_HEAD and CONTENT_COMMIT must be
ancestors, and SELF's direct parent must be CONTENT_COMMIT. Read the Manifest
and all eight content blobs from the fetched ref, verify table paths/byte
lengths/SHA-256 and equality with the content commit. Verify the overall
nine-file inventory, untouched protected paths and main, no changes to the
original WP3A branch, and a clean worktree. The final receipt reports actual
REMOTE_PUSHED=true, REMOTE_REFETCH_VERIFIED=PASS and DELIVERY_SHA256=8/8 only
after these checks succeed. Then request WP3A_IMPLEMENTATION_ACCEPTED and stop.
