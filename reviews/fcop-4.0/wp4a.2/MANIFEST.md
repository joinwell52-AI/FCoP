# WP4A.2 delivery Manifest

## Fixed authority and commit chain

```yaml
AUTHORIZED_SCOPE: WP4A_2_ONLY
REPOSITORY: joinwell52-AI/FCoP
TASKBOOK_COMMIT: 7e2dcd3cc45f043c7981e7e5b79a78505ec109e8
TASKBOOK_SHA256: 5caf02c25bd8a02989151066a801dfd83eef117d0342d3b01e5e7a885cd5adba
TASKBOOK_PATH: taskbooks/fcop-4.0/WP4A.2/01-CI-Quality-Gate-Closeout-Taskbook-v1.0.zh.md
INPUT_HEAD: 6ff8f213313c1f802e3498d2196b8c3bd363ceb5
CONTENT_PARENT: 7e2dcd3cc45f043c7981e7e5b79a78505ec109e8
CONTENT_COMMIT: 375c145a04652c9dd6f7febc72cc76ca2a52526c
MANIFEST_PARENT: 375c145a04652c9dd6f7febc72cc76ca2a52526c
MANIFEST_COMMIT: SELF
EXPECTED_REMOTE_HEAD: SELF
BRANCH: review/fcop-4.0-wp4a.1-machine-contract
DRAFT_PR: 14
WORKTREE: D:/FCoP-wp4a2-ci-closeout
LF_VERIFICATION_WORKTREE: D:/FCoP-wp4a2-lf-verification
CONTENT_FILES: 10
MANIFEST_FILES: 1
TOTAL_DELIVERY_FILES: 11
```

SELF means the Git commit containing this newly added Manifest. Its only changed path must be this Manifest; its first parent must equal CONTENT_COMMIT. Resolve it with `git log -1 --format=%H -- reviews/fcop-4.0/wp4a.2/MANIFEST.md` and pin all subsequent GitHub reads and CI to that full SHA, not an advancing branch name. The resulting full SHA and this file's independent SHA-256 are returned in the post-push final receipt.

[Existing Draft PR #14](https://github.com/joinwell52-AI/FCoP/pull/14). No new PR, force-push, history rewrite, main merge or release.

## Content inventory: SHA-256 of exact UTF-8/LF Git bytes

| Path | SHA-256 |
|---|---|
| `.github/workflows/test-fcop.yml` | `4cb0c35b5136823b01d290e6a4e0a07413aa7e08d311c776554710a9c460bdc0` |
| `reports/FCOP-4.0-WP4A.2-CI-GATE-DIAGNOSIS.md` | `b791216d90b372758c08f9b1d08db11c124ab59ac3718eb683633fdf25278c4e` |
| `reports/FCOP-4.0-WP4A.2-RESULT.md` | `340f4ba41e0799c19aea585e7e47a1b9389146305d3c788501d02406b88dfbeb` |
| `tests/conformance/v4/driver.py` | `9930b62b622bd5de7ab549f5ec2907c4ae1ee3e6279bafb57de06d147d2da9b9` |
| `tests/conformance/v4/scenarios.py` | `1babb1d0cd2acdae9560baed2830ace02887bc1bca735e959fcd314e5a565d11` |
| `tests/conformance/v4/test_c0_contract_authority.py` | `34a6531ece482a00e52c4fe0e4584f5e29e6a8d6c8e4377c2e84fb43f82424b3` |
| `tests/conformance/v4/test_c5_convergence.py` | `29ea26da71599d6a22f2fe0faa40981a6a7d891f8e1aea2547fa909dd5b2cabe` |
| `tests/conformance/v4/test_c7_idempotency.py` | `5af768c20022819151a0a6177f888b969dd25cee9b9866757e93d2c5fb1130f7` |
| `tests/conformance/v4/test_mcp_surface_contract.py` | `27a334f8efb73d2e5fadac9c85ab4e15dc873360624ccd51ac82d75cec86f7a5` |
| `tests/conformance/v4/test_meta_profile_boundary.py` | `06055905f1f9f33540596f43dddcdabe1477a7e2073104b2ca6e0883b60bd7ef` |
| `reviews/fcop-4.0/wp4a.2/MANIFEST.md` | SELF_FILE_SHA256_IN_FINAL_RECEIPT |

The ten concrete hashes above were computed from Content Commit Git blobs and independently matched execution files, UTF-8 without BOM and LF-only. The eleventh hash cannot be embedded in its own file; it must be computed and compared with the GitHub blob after the Manifest commit.

## Validation at content sealing

```yaml
RUFF_DIAGNOSTICS_BEFORE: 10
RUFF_DIAGNOSTICS_AFTER: 0
RUFF_FILES_CHANGED: 7
FROZEN_TEST_IDS: 60/60
V4_COLLECTED_NODES: 119
COLLECTED_NODE_SEQUENCE: UNCHANGED
NORMALIZED_NON_IMPORT_AST: 7/7_EQUAL_EXCEPT_AUTHORIZED_EXCEPTION_RENAME
ASSERT_NODES_PRESERVED: 90/90
ASSERTIONS_REMOVED: 0
SKIP_XFAIL_ADDED: 0
TESTS_RENAMED: 0
BEHAVIOR_EXPECTATION_CHANGED: 0
STABILITY_SECTION_EXTRACTION: CORRECTED
STABILITY_POSITIVE_CASE: PASS
STABILITY_NEGATIVE_CASES: 2/2
V4_CONFORMANCE: 119/119
TEST_FCOP: 1190/1190
MCP_REGRESSION: 80/80
SCHEMA_BINDING: 10/10
SCHEMA_BINDING_MODULE: 47/47
SCHEMA_SOURCE_PACKAGE_PARITY: 12/12
CLEAN_WHEEL_SCHEMA_PARITY: 12/12
CLEAN_WHEEL_APPLICATIONS: 2/2
PUBLIC_SURFACE_DRIFT: 0
MYPY: PASS_40_FILES
GITHUB_CI_AT_FINAL_HEAD: PENDING_REMOTE_EXECUTION
WP4A_MACHINE_CONTRACT_ACCEPTED: false
WP4B_STARTED: false
MAIN_MODIFIED: false
RELEASE_CREATED: false
```

The initial CRLF checkout run's 1189-pass/1-fail byte-check result is retained in DIAGNOSIS. Final local pass above is from a fresh LF checkout with the same authorized patch, not a Schema/test workaround. Local Windows proof never substitutes for GitHub Linux/macOS/native Windows jobs. Reports are sealed before final CI exists; no prospective PASS is claimed.

## Mandatory remote readback and final decision

1. Push the two appended commits normally to the existing review ref; reject head drift and do not force.
2. Refetch the review ref and assert its HEAD equals SELF; verify first-parent chain INPUT_HEAD -> taskbook -> content -> Manifest.
3. Read GitHub commit/tree/blob objects at SELF. Decode each of eleven delivery files and compare SHA-256 with local committed bytes and this inventory (ten embedded hashes plus the separately computed Manifest hash).
4. Confirm Content Commit modifies exactly the ten inventory paths and Manifest Commit modifies only this file. Confirm no production, Schema, frozen spec, MCP, CHANGELOG, public-surface snapshot, dependency or release changes.
5. `gh run list --repo joinwell52-AI/FCoP --commit <SELF SHA>`: inspect final-head **test-fcop** (12 OS/Python cells + Coverage + Stability Charter + package) and **test-fcop-mcp** (12 cells + tool contract + package). Require all 29 jobs to succeed, with no missing/cancelled/failed/unexpectedly skipped checks; inspect additional PR checks if any.
6. Return actual run URLs, final head, eleven-file verification and final CI result. If any new blocker appears, request no Gate and stop. Only all green permits requesting `WP4A_MACHINE_CONTRACT_ACCEPTED`; acceptance remains ADMIN's decision. Stop in either case; no WP4B.

Old WP4A.1 reports/Manifest, previous failed runs, all existing user workspaces and history are preserved. No CI rule was disabled or weakened; no noqa, lint ignore or CHANGELOG edit was introduced.
