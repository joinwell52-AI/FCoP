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

---

# WP4C.0a delivery — completed audit, Gate requested only

The original BLOCKED Manifest above is preserved history for PR #16 and its fixed delivery. This appended section is the current resume record. WP4C.0a §0/§7 supersedes only the old prerequisite/stop meaning; it does not rewrite old commits.

## Current authority and accounting

```yaml
WP4C_0A_STATUS: COMPLETE
AUTHORIZED_SCOPE: WP4C_0A_ONLY
TASKBOOK_COMMIT: eb086ee43f345a4d93ffb520049dc8af08712d3b
TASKBOOK_PATH: taskbooks/fcop-4.0/WP4C.0a/01-Constitution-Source-Classification-and-Baseline-Audit-Resume-Taskbook-v1.0.zh.md
TASKBOOK_SHA256: 9db3b811048618cf4fe1baf4352c9e980f2d6da3e061f41709f553520e8e589c
INPUT_HEAD: eb086ee43f345a4d93ffb520049dc8af08712d3b
PARENT_GATE_COMMIT: aad88ae5f1112881545d30c9938739e83481516d
PARENT_BLOCKED_HEAD: 4420bf6cdd456e328230015bcffef4fdabf615a8
PARENT_BLOCKED_PR: 16
CONSTITUTION_SOURCE_COMMIT: 0c61f7d3108777adb7aaf375324616c004fcaf7d
CONSTITUTION_SOURCE_SHA256: 25e70e221d6b54072503a8ec7224df33000fa63c0b12a64c148d86a0081b6762
CONSTITUTION_SOURCE_STATUS: DISCUSSION_DRAFT_FIXED_REVIEW_INPUT
CONSTITUTION_LICENSE_STATUS: UNRESOLVED
CONSTITUTION_CONTRACT_FROZEN: false
ENGINEERING_CONSTITUTION_SOURCE_STATUS: DISCUSSION_DRAFT_FIXED_REVIEW_INPUT
ENGINEERING_CONSTITUTION_LICENSE_STATUS: UNRESOLVED
ENGINEERING_CONSTITUTION_CONTRACT_FROZEN: false
NORMATIVE: false
RULE_GENERATION_AUTHORIZED: false
BUNDLING_AUTHORIZED: false
CANONICAL_SOURCE_IDENTIFIED: true
RULE_INVENTORY: 86/86
RULE_DISPOSITION: 147/147
RULE_UNIT_METHOD: CONTIGUOUS_PRIMARY_SOURCE_SECTIONS_NOT_ATOMIC_BEHAVIOR_COUNT
COMMON_ROLE_BLOCK_MAPPING: 4/4
V4_CLAUSE_MAPPING: 73/73
EN_ZH_CLAUSE_PARITY: 73/73
GENERATED_TARGETS_MAPPED: 4/4
HOST_CONSUMER_MATRIX: 12/12
HOST_RUNTIME_CONSUMPTION: UNVERIFIED_NOT_ASSUMED
CONTEXT_MEASUREMENTS: 6/6
CONSTITUTION_PRINCIPLE_MAPPING: 12/12
CODEFLOWMU_SHADOW: PASS_READ_ONLY_FIXED_LOCAL_GIT_SNAPSHOT
WP4C_0_AUDIT_BLOCKERS: 0
WP4C_1_ENTRY_BLOCKERS: 1
CURRENT_TESTS: 47_PASSED_3_DEPRECATION_WARNINGS
ENCODING_INPUT_SCAN: 107/107_UTF8_LF_WITH_50_LEADING_BOM_FINDINGS
RULE_GENERATOR_RUN: false
FRESH_BUILD_RUN: false
FULL_REGRESSIONS_RUN: false
FILES_MODIFIED: 6/6
WORKTREE: 'D:\FCoP-wp4c0a-baseline-resume'
BRANCH: review/fcop-4.0-wp4c.0a-baseline-resume
PR_BASE_BRANCH: review/fcop-4.0-wp4c.0a-constitution-source
CONTENT_COMMIT: 05cc1a5a8cf3cd7fbd4d566ed3a0b04a37fda8a2
MANIFEST_COMMIT: SELF_CONTAINING_COMMIT_RESOLVED_BY_GIT
REMOTE_PUSHED: PENDING_AT_MANIFEST_CREATION
REMOTE_REFETCH_VERIFIED: PENDING_AT_MANIFEST_CREATION
DELIVERY_SHA256: PENDING_REMOTE_6_FILE_READBACK
MAIN_MODIFIED: false
CODEFLOWMU_MODIFIED: false
PRODUCTION_MODIFIED: false
SPEC_MODIFIED: false
SCHEMA_MODIFIED: false
MCP_MODIFIED: false
RULES_MODIFIED: false
HOST_FILES_MODIFIED: false
RELEASE_CREATED: false
WORKSPACE_MIGRATED: false
WP4C_1_STARTED: false
WP4C_0_BASELINE_ACCEPTED: false
REQUESTED_GATE: WP4C_0_BASELINE_ACCEPTED
```

One next-phase entry blocker denotes the independent ADMIN constitution source/effect/license freeze Gate, not one unanswered question. All twelve prerequisite topics are listed in the Source Decision report. Known legacy distribution hazards are fully reported, not “fixed” or declared safe; typed-unavailable v4 guidance remains unchanged.

## Two-commit chain and content hashes

Required exact chain:
`eb086ee... → 05cc1a5a8cf3cd7fbd4d566ed3a0b04a37fda8a2 → containing Manifest commit`.

Content modifies exactly five reports; its direct child modifies only this Manifest. New Draft PR is stacked on the fixed taskbook-source branch so its change set is just six audit files. PR #16 and its old branch are not amended, force-pushed, merged or deleted.

| Content path | SHA-256 (exact UTF-8/LF Git blob) |
| --- | --- |
| reports/FCOP-4.0-WP4C.0-CONTEXT-AND-COLLISION-AUDIT.md | 03416fa739e7d71b1d8b6b2396833819b15a5b3144ae9dff156ef592faa50897 |
| reports/FCOP-4.0-WP4C.0-DISTRIBUTION-BASELINE.md | 1b014e811dd635445ee3834bfb5b6786049bee0e6681521069b6028ad1cc45f8 |
| reports/FCOP-4.0-WP4C.0-HOST-CONSUMER-MATRIX.md | 763fa49dea156f880601ee2c7bc66e646c873f8e3f5e0c9911c014874e52fee0 |
| reports/FCOP-4.0-WP4C.0-RULE-DISPOSITION.md | d7ba69a25af631e6f54f9b0b84c905e00672db5b254417574923c3554b3a7cfe |
| reports/FCOP-4.0-WP4C.0A-CONSTITUTION-SOURCE-DECISION.md | 4bf3c13c0e3dfa973b21b64fbaee3a5b6741d4c16424d73d5d38530fe7623bfc |

Sixth file: `reviews/fcop-4.0/wp4c.0/MANIFEST.md`. Its full-file SHA-256 and the containing commit cannot be included in their own bytes without a circular definition. They are resolved from Git and recorded in the final GitHub PR receipt, together with all five hashes above, after actual remote readback. PENDING here is not a fabricated PASS and does not require a third commit to change status.

## Current validation evidence

Executed with Python 3.12.9 in the independent worktree:
```text
PYTHONDONTWRITEBYTECODE=1
PYTHONPATH=<worktree>/src;<worktree>/mcp/src;<worktree>
python -B -m pytest tests/test_fcop/test_rules.py tests/test_fcop/test_rules_metadata_consistency.py tests/test_fcop/test_rules_text_regression.py tests/test_fcop_mcp/test_wp4b_delivery.py::test_all_static_resources_and_disposition tests/test_fcop_mcp/test_wp4b_delivery.py::test_spec_payload_git_parity -q -p no:cacheprovider
47 passed, 3 warnings in 3.87s
git diff --cached --check
PASS
```

Warnings: one importlib.abc.Traversable and two jsonschema.RefResolver deprecations. No test logic changed. Deployment tests were statically read, not executed, because WP4C.0a prohibits running generators. No fresh build, install, deploy, migration, downstream test or full regression run. Earlier WP4B 29-job CI and large regression counts remain historical references only.

Read-only evidence extraction:
- GitHub contents API at fixed taskbook/source commit, base64 decode, SHA-256 equality with Git blobs.
- `git merge-base --is-ancestor` for source, blocked head and Gate; `git diff --quiet <Gate> <input> -- src mcp/src spec tests .cursor/rules AGENTS.md CLAUDE.md`.
- `git ls-tree -r --name-only <input>`, `git show <input>:<path>`, bounded Git history and source-call-site inspection.
- In-memory UTF-8/LF/BOM/hash/line measurements; no audit production script created.
- Existing wheel zip/tar member reads and source-parity comparison; 4/4 archive hashes, 144/144 fcop and 21/21 MCP members in each artifact accounted. Raw parity is 13/144 and 10/21 respectively; remaining differences are CRLF-only, not silently ignored as identical bytes.
- Fixed CodeFlowMu local Git snapshot c008d9db91a21136fc61a4f60314e22db395d5d2, eight bounded consumer-path hashes, read-only pin evidence; no installed/runtime version claim.

Report table row counts (including preserved old sections):
- Context: 6, 6, 12, 3.
- Distribution: 6, 9, 12, 4, 86.
- Host: 3, 12, 15, 4, 8.
- Disposition: 3, 4, 15, 73, 147, 4, 15.
- Source Decision: 12, 12.
- This Manifest: old hash table 4; current hash table 5.

Counts were checked independently from file text; exact source intervals partition both primary texts, 73 EN/ZH clause IDs are identical and frozen bytes unchanged. Six-file scope and final UTF-8/no-BOM/LF/diff checks are required again before Manifest commit. Old four report blobs and old Manifest remain exact byte prefixes of their current Git blobs.

## Remote completion protocol and stop

Push ONLY review/fcop-4.0-wp4c.0a-baseline-resume, without force. Refetch; compare HEAD, both direct parents and ancestry. Read all six files via GitHub at the final full SHA and compare raw bytes/SHA-256 with local Git blobs. Create the independent Draft PR, then post a complete machine-readable receipt including actual commit/Manifest hash and remote results.

Main observed before delivery: remote `68dbeb15f4e7f84e1d03f907be9fa66c2265843e`; local `da79dfefd99f597c9e422ce9edec22157f915a21`. Neither is changed by this task. Original dirty D:\FCoP and all historical/dogfood material remain untouched.

WP4C.0a requires remote report integrity, not fresh implementation CI acceptance. Any PR CI is incidental to this docs-only delivery, never substituted for file hashes or ADMIN judgment. After receipt, stop. Request only WP4C_0_BASELINE_ACCEPTED; do not sign it and do not enter WP4C.1.
