# WP4A.3 delivery Manifest

## Fixed authority and two-commit chain

```yaml
AUTHORIZED_SCOPE: WP4A_3_ONLY
REPOSITORY: joinwell52-AI/FCoP
TASKBOOK_COMMIT: db4c99806e797a563541381e376c7c62e13f8da0
TASKBOOK_SHA256: a1dac079f1744eb97ab15bcfa56088dac656b8843454dc49ae01ca36dbe045ee
TASKBOOK_PATH: taskbooks/fcop-4.0/WP4A.3/01-Windows-Schema-LF-Checkout-Contract-Closeout-Taskbook-v1.0.zh.md
INPUT_HEAD: 2ef95e5afdabfc7aa25a93fb287827682b467c9d
CONTENT_PARENT: db4c99806e797a563541381e376c7c62e13f8da0
CONTENT_COMMIT: eb2c20a29b5d6d2d24f238ac2d266b671ab38fca
MANIFEST_PARENT: eb2c20a29b5d6d2d24f238ac2d266b671ab38fca
MANIFEST_COMMIT: SELF
EXPECTED_REMOTE_HEAD: SELF
BRANCH: review/fcop-4.0-wp4a.1-machine-contract
DRAFT_PR: 14
WORKTREE: D:/FCoP-wp4a3-checkout-policy
CONTENT_FILES: 3
MANIFEST_FILES: 1
TOTAL_DELIVERY_FILES: 4
```

SELF is the full SHA of the commit containing this newly added Manifest, with exactly this file as its changed path. Resolve it once, then pin CI and remote verification to that SHA. Its independent file hash and resolved commit SHA are returned in the final receipt, not embedded in their own hashed content.

Taskbook is the direct child of INPUT_HEAD. Content is its direct child; Manifest is Content's direct child. Exactly two delivery commits are appended to the existing [Draft PR #14](https://github.com/joinwell52-AI/FCoP/pull/14). No force-push, third evidence commit, old report rewrite, main merge or release.

## Four-file delivery inventory

Hashes are SHA-256 of exact committed UTF-8/LF bytes. Content files were independently compared with local bytes before sealing.

| Path | SHA-256 |
|---|---|
| `.gitattributes` | `0c976f274663a6904cde1cbba7bfcd10c7238745bbe065f31b52b128297b3745` |
| `reports/FCOP-4.0-WP4A.3-RESULT.md` | `a2aa4eefc48abb90e573af3757776c65384664d7012211a930db43686f1d0f9b` |
| `reports/FCOP-4.0-WP4A.3-WINDOWS-SCHEMA-CHECKOUT-POLICY.md` | `ddc9b5670664812617aff015ed8e7e6a5bbe67f335b72c9c11e0032be32af3c9` |
| `reviews/fcop-4.0/wp4a.3/MANIFEST.md` | SELF_FILE_SHA256_IN_FINAL_RECEIPT |

## Immutable Schema proof

The checkout-policy report above, pinned by its content hash, records all 24 full paths, input Git blob IDs and SHA-256 values. All must remain identical in Content, Manifest and remote GitHub readback. There are twelve distinct JSON documents, each present in source and package.

```yaml
WINDOWS_FAILURE_JOBS_REVIEWED: 4/4
CHECKOUT_POLICY_FILE: .gitattributes
CHECKOUT_POLICY_SCOPE: V4_SCHEMA_ONLY
GIT_CHECK_ATTR: PASS_BOTH_ROOTS_AND_OUTSIDE_SCOPE
V4_SCHEMA_FILES: 24
V4_SCHEMA_BLOB_DRIFT: 0
V4_SCHEMA_SHA256_DRIFT: 0
SCHEMA_SOURCE_PACKAGE_PARITY: 12/12
SCHEMA_FILES_MODIFIED: 0
GENERATOR_FILES_MODIFIED: 0
TEST_FILES_MODIFIED: 0
WORKFLOW_FILES_MODIFIED: 0
PRODUCTION_FILES_MODIFIED: 0
MCP_IMPLEMENTATION_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0
```

The only policy rules are the taskbook's exact `spec/schemas/v4/*.schema.json text eol=lf` and `src/fcop/_data/schemas/v4/*.schema.json text eol=lf`. No global setting changed, no broad file glob, no weakening of raw-byte generation checks.

## Fresh committed-policy Windows checkout

```yaml
LOCAL_CHECKOUT_FIXTURE_COMMIT: a15a0376c394f034031e3fa5580cc7ec32ac3225
FIXTURE_PARENT: db4c99806e797a563541381e376c7c62e13f8da0
FIXTURE_ADDED_FILES: [.gitattributes]
FIXTURE_IS_DELIVERY_ANCESTOR: false
FRESH_WINDOWS_WORKTREE: D:/FCoP-wp4a3-clean-windows
CORE_AUTOCRLF_UNCHANGED: true
FRESH_SCHEMA_CRLF_FILES: 0
FRESH_SCHEMA_BYTES_EQUAL_INPUT: 24/24
SCHEMA_CHECK_CLEAN_WINDOWS_CHECKOUT: PASS
SCHEMA_BINDING_MODULE: 47/47
SCHEMA_BINDING: 10/10
RUFF: PASS
MYPY: PASS_40_FILES
FROZEN_TEST_IDS: 60/60
V4_CONFORMANCE: 119/119
TEST_FCOP: 1190/1190
MCP_REGRESSION: 80/80
PUBLIC_SURFACE_DRIFT: 0
MINIMAL_APPLICATIONS: 2/2
CLEAN_WHEEL_INSTALL: PASS
CLEAN_WHEEL_SCHEMA_PARITY: 12/12
```

The local-only fixture made a committed attribute policy available for a genuinely new Windows checkout **before** the two reports were sealed. It is not pushed or attached to the delivery parent chain. `git diff --name-only <fixture> <Content>` lists only the two new reports: the complete executable/test/workflow/Schema/policy tree is identical to the tested one. No old pre-normalized WP4A.2 LF tree was reused. The pre-attribute execution tree's red check is preserved in the policy report.

Full regression and a separate 47-node Schema suite ran in the fresh checkout without test modifications. Fresh wheel and sdist were built from this tree, all twelve embedded schemas compared byte-for-byte, and the wheel was installed into a new external venv with no-index dependencies and the existing network guard. Both restarted public applications passed. Local native environment: Windows / Python 3.12 only.

## Remote readback and final CI rule

At this Manifest's sealing, final-head CI is not yet executed. `GITHUB_CI_AT_FINAL_HEAD: PENDING_REMOTE_EXECUTION`; no prospective PASS or Gate signature is asserted here.

After the normal push:

1. Refetch the designated review ref; PR remains draft, and both PR HEAD and remote ref must equal SELF. Verify the direct input/taskbook/content/Manifest chain and exactly two delivery commits.
2. Read GitHub commit/tree/blob objects at SELF. Compare all four delivered files with committed local bytes and the three concrete hashes above, plus this Manifest's independently computed hash. Recheck each of the 24 Schema blob IDs and SHA-256 values against INPUT_HEAD and the report inventory.
3. Confirm Content changes only the three listed files; Manifest only this file. No extra files, Schema drift, or protected-area edits.
4. Inspect runs with `gh run list --repo joinwell52-AI/FCoP --commit <SELF SHA>`. Require **test-fcop**: Windows Python 3.10/3.11/3.12/3.13 4/4, Ubuntu/macOS 8/8, Coverage, Stability Charter, and build/install/audit package (not skipped). Require **test-fcop-mcp**: twelve OS/Python cells, tool contract and package. All 29 jobs and any additional required checks must succeed.
5. Return the actual full HEAD, four-file hash verification, zero Schema drift, run/job links and CI outcome in the final receipt. Taskbook/intermediate runs are not final evidence. Any failure, cancellation, missing check or unexpected skip means BLOCKED and `REQUESTED_GATE: NONE`; stop without repair.
6. Only full success allows requesting `WP4A_MACHINE_CONTRACT_ACCEPTED`. ADMIN alone signs it. Stop without entering WP4B or modifying main/release/CodeFlowMu.

```yaml
WP4A_MACHINE_CONTRACT_ACCEPTED: false
MAIN_MODIFIED: false
RELEASE_CREATED: false
WP4B_STARTED: false
```
