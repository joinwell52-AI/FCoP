# WP4C.1 Factual Blocker Delivery Manifest

## Authority and delivery boundary

```yaml
WP4C_1_STATUS: BLOCKED
AUTHORIZED_SCOPE: WP4C_1_ONLY
STOP_CODE: TASKBOOK_RELATION_SET_CONFLICT
P0_OPEN: 1
TASKBOOK_COMMIT: 81d5cd416515d9d712db0250514f7011c346a07c
TASKBOOK_SHA256: 21c77fa93750c95e1b27dabaab59a938ef9f6f49677c15c069cbbf3e6dc80220
INPUT_HEAD: 81d5cd416515d9d712db0250514f7011c346a07c
CONTENT_COMMIT: 741b1829283f6a7fc1023e0edd8176b58c63ded4
BRANCH: review/fcop-4.0-wp4c.1-rule-distribution-contract
PR_BASE_BRANCH: taskbook/fcop-4.0-wp4c.1-rule-distribution-contract
CONTENT_FILES: 3
TOTAL_DELIVERY_FILES: 4
SUCCESS_PACKAGE_PATHS_WRITTEN: 4/6
CONTRACT_DOCUMENTS_CREATED: 0
PRODUCT_TESTS: NOT_RUN
REQUESTED_GATE: NONE
WP4C_1_RULE_DISTRIBUTION_CONTRACT_FROZEN: false
WP4C_2_STARTED: false
```

Taskbook section 12 requires factual reports only when stopped, with no Gate request. Consequently this is not the six-file successful contract package described in section 13. No placeholder English or Chinese contract is produced. The three content reports document the mismatch between taskbook section 4.1 and frozen F4.5.1; their matrix explicitly marks incomplete work, not successful clause coverage.

## Content files at the fixed Content commit

Hashes are SHA-256 over exact UTF-8/LF Git blob bytes, without BOM.

| Path | SHA-256 |
| --- | --- |
| reports/FCOP-4.0-WP4C.1-CONTRACT-DECISIONS.md | 3c5d0de185515fc5d47c4dd898d9d9a8a3d791c649333f805b122c4366e06457 |
| reports/FCOP-4.0-WP4C.1-CONFORMANCE-MATRIX.md | c522e170109057fcc3af121dc527d3def804227194d35b08039e0ddb315cb488 |
| reports/FCOP-4.0-WP4C.1-RESULT.md | 50a8a72b3bff6231bc75485cc787e924e406e6a6e83bbf9180477878f7f364fe |

## Commit and readback protocol

The Content commit directly follows INPUT_HEAD. The immediately following Manifest commit adds only this file, with no content-report modification. Its own SHA and this file's SHA-256 cannot be embedded self-referentially; they will be recorded in the final Draft PR receipt after push and remote refetch.

The remote verification must compare all four delivered file bytes using the fixed remote Manifest HEAD, verify its direct parent is CONTENT_COMMIT and that CONTENT_COMMIT directly parents INPUT_HEAD, and confirm the remote branch HEAD matches. The final receipt must distinguish actual 4/4 factual-file hash verification from the uncompleted 6/6 success package.

Local pre-commit validation: exact three-report content allowlist, strict UTF-8/LF/no-BOM, filesystem/staged byte equality, and git diff --check passed. Manifest validation and network results are recorded in the final receipt, not asserted prospectively here.

No rules, frozen specifications, Core, MCP, Schema, tests, Host projections, CodeFlowMu, existing workspace, main or release content are changed. PR #17 is preserved. No product regression or rule generator is run for this stopped documentation-only task.

After factual delivery, stop for ADMIN to correct the relation responsibility and clarify ordinary sequential relation coverage. No contract freeze or WP4C.2 execution is requested.
