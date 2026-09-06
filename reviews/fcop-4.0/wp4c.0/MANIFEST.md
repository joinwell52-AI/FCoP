# WP4C.0 Delivery Manifest — BLOCKED

## Authority and disposition

```yaml
WP4C_0_STATUS: BLOCKED
AUTHORIZED_SCOPE: WP4C_0_ONLY
STOP_CODE: ENGINEERING_CONSTITUTION_SOURCE_UNRESOLVED
PARENT_GATE_COMMIT: aad88ae5f1112881545d30c9938739e83481516d
TASKBOOK_COMMIT: 962b67d89e137c26440291d3a48fc7aea1cfebb6
TASKBOOK_SHA256: c8c4cb26708a480a6793d88c21511b103f140021c3827c9977b076dfed748e55
WORKTREE: 'D:\FCoP-wp4c0-distribution-audit'
BRANCH: review/fcop-4.0-wp4c.0-distribution-audit
CONTENT_COMMIT: 9804f6ddd3e9dcbf7a8939e62edd100c139ec6f0
MANIFEST_COMMIT: SELF_CONTAINING_COMMIT_RESOLVED_BY_GIT
P0_CONTRACT_CONFLICTS: 1
P0_COUNT_SCOPE: CONFIRMED_ONLY_FULL_AUDIT_INCOMPLETE
CANONICAL_SOURCE_IDENTIFIED: false
GENERATED_TARGETS_MAPPED: NOT_COMPLETED
V4_CLAUSE_MAPPING: NOT_COMPLETED_DENOMINATOR_NOT_ESTABLISHED
V3_ACTIVE_RULE_DISPOSITION: NOT_COMPLETED_DENOMINATOR_NOT_ESTABLISHED
HOST_CONSUMER_MATRIX: NOT_COMPLETED
CONTEXT_MEASUREMENTS: PARTIAL_SIX_BLOB_IDENTITIES_ONLY
CODEFLOWMU_SHADOW: NOT_AVAILABLE
CURRENT_TESTS: NOT_RUN_HARD_STOP
FILES_WRITTEN: 5/5
CODE_FILES_MODIFIED: 0
SPEC_FILES_MODIFIED: 0
SCHEMA_FILES_MODIFIED: 0
MCP_FILES_MODIFIED: 0
RULE_FILES_MODIFIED: 0
HOST_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0
MAIN_MODIFIED: false
RELEASE_CREATED: false
WP4C_1_STARTED: false
REQUESTED_GATE: NONE
```

Taskbook: [fixed WP4C.0 taskbook](https://github.com/joinwell52-AI/FCoP/blob/962b67d89e137c26440291d3a48fc7aea1cfebb6/taskbooks/fcop-4.0/WP4C.0/01-Rule-Distribution-Host-Assembly-and-Development-Context-Baseline-Audit-Taskbook-v1.0.zh.md).

Sections 3 and 14 require stopping when the engineering constitution's fixed source, license or digest cannot be established. Only factual BLOCKED delivery continues under sections 13–14. This is not a completed baseline, not acceptance, and not authorization for WP4C.1.

The two loader-declared input paths are identified, but the complete canonical-authority audit is unfinished; the false value above means completion was not established, not that multiple canonical sources were proven. No fictional denominator is substituted for unfinished mappings. CodeFlowMu shadow was not attempted after the stop; access failure was not established.

## Content file SHA-256

Hashes cover exact UTF-8/LF Git blobs in the Content Commit.

| File | SHA-256 |
|---|---|
| reports/FCOP-4.0-WP4C.0-DISTRIBUTION-BASELINE.md | 70fcc3638ea6122d5ccdc48492f9a26926d616584812a3d2c5e9d35a3c656605 |
| reports/FCOP-4.0-WP4C.0-RULE-DISPOSITION.md | 97f8d11f5ec990f6cb88b38283f8bd70de524acdb31c439165a8ad3a8c916ea5 |
| reports/FCOP-4.0-WP4C.0-HOST-CONSUMER-MATRIX.md | 0a768a1242075d9192f6ab687cb11e1123e0fdbc512574197d7ed6ffe0a7fbbd |
| reports/FCOP-4.0-WP4C.0-CONTEXT-AND-COLLISION-AUDIT.md | 94e2c148b59c169f9da8e7d2d8b79a39312cb3c040c96d9c0b24f7b65843d67e |

The fifth delivery file is this Manifest. Its own commit SHA and file SHA-256 cannot be embedded self-referentially. Resolve them from the containing commit and the final GitHub PR receipt. The Manifest commit must have the Content Commit above as its direct parent and must add only this file. The Content Commit must have the Gate as its direct parent and add only the four reports.

## Evidence commands and observed scope

Commands ran in the independent audit worktree unless a read-only fixed-tree lookup required the existing local Git object store.

```text
gh api repos/joinwell52-AI/FCoP/contents/<taskbook-path>?ref=962b67d89e137c26440291d3a48fc7aea1cfebb6
git show 962b67d89e137c26440291d3a48fc7aea1cfebb6:<taskbook-path>
git rev-parse 962b67d89e137c26440291d3a48fc7aea1cfebb6^
git diff-tree --no-commit-id --name-status -r 962b67d89e137c26440291d3a48fc7aea1cfebb6
git ls-tree -r --name-only aad88ae5f1112881545d30c9938739e83481516d
git grep -I -n -i -E 'constitution|宪法' aad88ae5f1112881545d30c9938739e83481516d -- .
git log aad88ae5f1112881545d30c9938739e83481516d --regexp-ignore-case --grep='constitution\|宪法'
git show aad88ae5f1112881545d30c9938739e83481516d:<measured-path>
git diff --cached --check
git diff --cached --stat
git status --short
```

- Taskbook API response was base64-decoded and SHA-256 checked, then compared byte-for-byte with the Git blob. Its direct parent equals the Gate.
- Constitution search returned 42 matching lines. Historical team constitutions and charter terminology do not fix the named engineering constitution.
- Six measured source/Host blobs passed strict UTF-8 decoding and no-CR checks. Line counting used Python splitlines; hashing used raw Git bytes. No tokenizer was used.
- A historical log produced an invalid-UTF-8 search-output diagnostic; escaped byte decoding was used for discovery. No repair was made. Whole-repository UTF-8/LF PASS is not asserted.
- Report table data-row counts: Baseline 6 and 9; Rule Disposition 3, 4 and 15; Host Matrix 3; Context 6; this Manifest's hash table 4. These are documentation table counts, not audit coverage denominators.
- Four reports passed UTF-8/no-BOM/LF and consistent table-column checks before the content commit. Final five-file checks and remote results belong in the PR receipt.

## Explicitly unperformed work

The full normative EN/ZH mapping, 3.x rule-unit disposition, complete mandatory input/history deep-read, full WP4B evidence review, deployment call graph and overwrite/recovery analysis, wheel/sdist inventory, rule-related tests, full regressions, dry-runs, Host probes, downstream shadow, token estimates, normative fraction, repeated-body ratio and candidate minimal assemblies remain incomplete/not run. No old test green result is represented as a current run.

## Remote verification protocol

After the Manifest Commit: push only the fixed review branch; create a Draft PR (do not modify PR #15); refetch that review branch; verify HEAD and both parent links; read all five files through GitHub at the final fixed SHA; compare bytes and SHA-256 with local Git blobs; verify four-plus-one commit file scopes; publish the five hashes and actual Manifest SHA in the PR receipt.

At creation of this file, remote push/refetch/hash verification is PENDING, not claimed PASS. The final PR receipt records the actual result without adding a third commit. Main's remote SHA observed before this delivery is 68dbeb15f4e7f84e1d03f907be9fa66c2265843e; no main update is authorized.

After verified BLOCKED delivery, stop. ADMIN must fix the constitution authority/version/hash/license/acquisition input or issue a fixed taskbook clarification; the executor does not adopt a substitute or request WP4C_0_BASELINE_ACCEPTED while this P0 remains open.
