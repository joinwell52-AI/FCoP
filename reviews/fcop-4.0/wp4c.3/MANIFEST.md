# WP4C.3 Blocked Evidence Manifest

This is a **fact-report-only blocked package**, not completed WP4C.3 implementation. No acceptance Gate is requested. Taskbook section 13 required stopping on the clean-baseline frozen control-plane mismatch.

## Fixed chain

```yaml
WP4C_3_STATUS: BLOCKED
AUTHORIZED_SCOPE: WP4C_3_ONLY
TASKBOOK_COMMIT: de213ec0f74f8976283a24986d4eb7de77c67142
TASKBOOK_SHA256: a4b782db3a984be9872d6c99428c5fc669a1cd3135468b33ef8eba7a6c1b57d2
ACCEPTED_INPUT_HEAD: 1f4df9cc650f63b9e842d806340eb31b768f708e
CONTENT_COMMIT: 0e89f94aa8df017817f76dadc8572c8bc5c0afdf
CONTENT_DIRECT_PARENT: de213ec0f74f8976283a24986d4eb7de77c67142
MANIFEST_COMMIT: SELF_CONTAINING_COMMIT
MANIFEST_REQUIRED_DIRECT_PARENT: 0e89f94aa8df017817f76dadc8572c8bc5c0afdf
BRANCH: review/fcop-4.0-wp4c.3-rule-package-core
DRAFT_PR_BASE: taskbook/fcop-4.0-wp4c.3-rule-package-core
STOP_REASON: HISTORICAL_CONTROL_PLANE_ALLOWLIST_REJECTS_AUTHORIZED_WP4C3_INPUT
PRE_REPORT_WORKTREE: CLEAN
RULE_DISTRIBUTION_META: 32_PASS_1_FAIL
DIST_30_CONTROL: FAIL
COLLECT_ONLY: 176
WP4C_3_TARGET_NODES_COLLECTED: 56/56
WP4C_3_TARGET_NODES_PASSED: NOT_RUN
PRODUCTION_FILES_MODIFIED: 0
FROZEN_FILES_MODIFIED: 0
MCP_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0
IMPLEMENTATION_STARTED: false
WP4C_4_STARTED: false
MAIN_MODIFIED: false
RELEASE_CREATED: false
WP4C_3_RULE_PACKAGE_ACCEPTED: false
REQUESTED_GATE: NONE_BLOCKED
REMOTE_VERIFICATION_AT_AUTHORING: PENDING_PUSH_AND_READBACK
```

SELF_CONTAINING_COMMIT is the commit adding this Manifest; its full SHA and raw file hash are reported externally after push, avoiding impossible self-reference. This document does not predict remote verification results.

## Content paths and raw Git blob SHA-256

| Path | SHA-256 |
| --- | --- |
| reports/FCOP-4.0-WP4C.3-CLAUSE-AND-ARTIFACT-MAPPING.md | 7056da2bb6d7a82c1665fe1176539b5d93933e63099f32240ecfb318d4d9f181 |
| reports/FCOP-4.0-WP4C.3-CONFORMANCE-RESULT.md | 41906b72d1ff92a539d8f5ae1b54b43931d19130a934d9e0c5e285c9095f92a1 |
| reports/FCOP-4.0-WP4C.3-IMPLEMENTATION-PLAN.md | 45aabfc8ce2711ddb0a18b704349c3a06f5f30776be0dbfe9394b907777a4eaf |
| reports/FCOP-4.0-WP4C.3-RESULT.md | 79672e78c5b4e85fbbb07e2981f0eb940e6a9b64971558453d861c5be19d0788 |

This Manifest is the fifth and final delivery path and the only change in its own commit. Four report files passed UTF-8/LF and staged diff checks. No production, test, package data, schema, workflow or public-surface change is part of this delivery.

## Reproduction and interpretation

[Conformance evidence](../../../reports/FCOP-4.0-WP4C.3-CONFORMANCE-RESULT.md) records the exact pytest invocation: 2 failed, 32 passed, exit 1, 11.66 seconds. Both failures name only the already committed WP4C.3 taskbook path as an extra item in the WP4C.2 allowlist. The run occurred before these reports existed. All nine distribution test blobs match the accepted parent. The target node count is correct; the blocker is not collection drift or missing implementation.

The partial [plan](../../../reports/FCOP-4.0-WP4C.3-IMPLEMENTATION-PLAN.md) records authority, source lines and the needed ADMIN decision. [Result](../../../reports/FCOP-4.0-WP4C.3-RESULT.md) explicitly distinguishes blocked preflight from implementation acceptance. The mapping status does not fabricate clause/artifact work that has not occurred.

After push, refetch the fixed review ref, verify both direct parents and all five files through GitHub contents API, and record the actual HEAD/hashes in the new Draft PR. Inspect actual CI without changing the taskbook base or workflow filters. A blocked report's green or absent CI cannot accept implementation. Stop; request ADMIN correction authority, not WP4C_3_RULE_PACKAGE_ACCEPTED.
