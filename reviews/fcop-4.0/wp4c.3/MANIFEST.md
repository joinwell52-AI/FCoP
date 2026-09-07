# WP4C.3c delivery Manifest — canonical rule-package closeout

## Authority and local validation

```yaml
AUTHORIZED_SCOPE: WP4C_3C_LEGACY_PUBLIC_METHOD_SET_ALIGNMENT_AND_WP4C_3_RESUME
TASKBOOK_COMMIT: ec2e43cd87ce264da1b77365558a182736ccb24f
TASKBOOK_SHA256: c81c883c6ccf4f132ed12f511684eed93fc455fc37125b85ed4c15d8fbaeee80
TASKBOOK_BYTES: 13805
INPUT_HEAD: c19808f4bc07948729bb841ec569627cb672fde7
TEST_ALIGNMENT_COMMIT: 96ad2ae812c60a6362d9c360dbb815621a0cbe1a
CONTENT_COMMIT: e5218e7133e81dd9393922f684f311f249a32dd3
MANIFEST_PARENT: e5218e7133e81dd9393922f684f311f249a32dd3
MANIFEST_COMMIT: SELF_COMMIT_CONTAINING_THIS_MANIFEST
BRANCH: review/fcop-4.0-wp4c.3c-public-method-closeout
PR_BASE: taskbook/fcop-4.0-wp4c.3c-public-method-set
WORKTREE: D:/FCoP-wp4c3b-development-fixture-and-rule-package
LOCAL_VALIDATION: PASS
IMPLEMENTATION_COMMITTED: true
CANDIDATE_PROVENANCE_HASHES: 31/31_UNCHANGED
HISTORICAL_TEST_FILES_MODIFIED: 1
LEGACY_METHODS: 38/38
V4_ONLY_METHODS: 11/11
PUBLIC_API_ADDITIONS: 1
PUBLIC_API_ADDITION: Project.rule_distribution
ORIGINAL_ASSERTIONS_REMOVED: 0
CANONICAL_MODULES: 9/9
CANONICAL_ARTIFACTS: 18/18
PACKAGE_MANIFEST_FILES: 1/1
ARTIFACT_FIELDS: 11/11
CLAUSE_OWNERSHIP: 73/73
WP4C_3_TARGET_IDS: 10/10
WP4C_3_TARGET_NODES: 56/56
DIST_30_CONTROL: 1/1
TEST_FCOP: 1297/1297
V4_CORE_CONFORMANCE: 119/119
MCP_REGRESSION: 134/134
NEW_UNIT_NODES: 41/41
RULE_DISTRIBUTION_META: 33/33
RULE_DISTRIBUTION_COLLECT_ONLY: 176
RULE_DISTRIBUTION_FULL: 99_PASS_77_DEFERRED_FAIL
FUTURE_NODES: 86
FUTURE_NEGATIVE_OVERLAP_PASSES: 9
FUTURE_DEFERRED_FAILURES: 77
UNEXPECTED_FAILURES: 0
UNEXPLAINED_FUTURE_PASSES: 0
RUFF: PASS
MYPY: PASS
REMOTE_READBACK: PENDING_POST_PUSH_EXTERNAL_RECEIPT
WP4C_3_RULE_PACKAGE_ACCEPTED: false
WP4C_4_STARTED: false
MAIN_MERGE_AUTHORIZED: false
RELEASE_AUTHORIZED: false
REQUESTED_GATE_AFTER_REMOTE_VERIFICATION: WP4C_3_RULE_PACKAGE_ACCEPTED
```

[Fixed taskbook](https://github.com/joinwell52-AI/FCoP/blob/ec2e43cd87ce264da1b77365558a182736ccb24f/taskbooks/fcop-4.0/WP4C.3c/01-Legacy-Public-Method-Set-Alignment-and-WP4C.3-Closeout-Taskbook-v1.0.zh.md) and [ADMIN authorization](https://github.com/joinwell52-AI/FCoP/pull/23#issuecomment-5572037831). Raw taskbook API bytes, Git Blob, size, UTF-8/LF and SHA were verified before the authorized fast-forward.

## Direct parent chain and exact sets

1. Taskbook ec2e43cd87ce264da1b77365558a182736ccb24f directly follows input c19808f4bc07948729bb841ec569627cb672fde7, adding only the fixed taskbook.
2. Test alignment 96ad2ae812c60a6362d9c360dbb815621a0cbe1a directly follows Taskbook and changes only tests/test_fcop/test_v4_creation.py.
3. Content e5218e7133e81dd9393922f684f311f249a32dd3 directly follows alignment and changes exactly 36 paths: the 31 preserved candidate files plus five current reports.
4. This Manifest-only commit directly follows Content and changes exactly reviews/fcop-4.0/wp4c.3/MANIFEST.md.

No merge, amend, force push, cherry-pick or discarded candidate rewrite. Original source provenance and PRs #21/#22/#23 remain intact. The old DIST-02 fixture and audit-alignment Conformance files are inherited unchanged, not included as newly changed delivery paths.

## Exact 37 content/alignment identities

Each identity below hashes the complete raw Git Blob at Content. All 37 blobs already match the execution worktree bytes; all 31 candidate blobs match their original PR #23 hashes. The Manifest itself is the 38th cumulative path and its hash/final HEAD are verified externally, avoiding self-reference.

| Exact path | Bytes | Raw SHA-256 |
| --- | ---: | --- |
| CHANGELOG.md | 130694 | aea366e3f64d903049e45d79bacec56fccf5057959f15abfe65d2671f8992c8d |
| pyproject.toml | 6075 | e51ff7f3fda0a1b9c27ab407275d452a0ea5dcfaeb5650c4137c485db8d446b5 |
| reports/FCOP-4.0-WP4C.3-CLAUSE-AND-ARTIFACT-MAPPING.md | 11711 | d63bdadeebd9053bbfca61a909a5379e9b4aa58091bd066f866cc04cde1f09b7 |
| reports/FCOP-4.0-WP4C.3-CONFORMANCE-RESULT.md | 32854 | 4e6fd9667b4939446817116831c6201ccfeb721b2016c28a403a49c1902a6d74 |
| reports/FCOP-4.0-WP4C.3-IMPLEMENTATION-PLAN.md | 16494 | 4d22b3e17361c6db64efb0f31652192ab8833a037127688d4688f05e27e8a377 |
| reports/FCOP-4.0-WP4C.3-RESULT.md | 25009 | 396d12ecce6df1af3a1bca50794e6d07468249b870416bdd1c7a89aa272c4c0a |
| reports/FCOP-4.0-WP4C.3C-PUBLIC-METHOD-SET-ALIGNMENT.md | 11227 | a122b1737bb1285522d3622ef7e82775e76606180a95e040f1ab3e245a10d082 |
| src/fcop/project.py | 265857 | f421d7fb2a444b90c63c18bea8c8c4751af90f3c8eeb9f2ed139e32f6acbf6ec |
| src/fcop/rules/_data/v4/authorization.en.md | 2128 | 96c1c18bab3a879b51a1e2d0041f1f08eeae685185ad9489f13ed0a999f9a00b |
| src/fcop/rules/_data/v4/authorization.zh.md | 2033 | 13b82fdeb7c577a68a70d94303bf090eac42ce44c137c1a166b23f7014c1b854 |
| src/fcop/rules/_data/v4/compatibility.en.md | 3521 | a65385a3a2e68d043c65f9b8c34c6ac311bb7f9b2ea1e9f4c162886f858a64d8 |
| src/fcop/rules/_data/v4/compatibility.zh.md | 3024 | d6ce267c8216a2d6df2e5e601f4d237d941778a36687eae1d310616f6170585e |
| src/fcop/rules/_data/v4/convergence.en.md | 2283 | ec3cf38b6dba4d3eb8447cc7cd25e947c06abed228c37c9d651f873662edc70e |
| src/fcop/rules/_data/v4/convergence.zh.md | 2114 | 2b5c2a52c33bc38e8c3c85fdd75d5de3c837cc483a29941ec02a61a059c1701a |
| src/fcop/rules/_data/v4/envelopes.en.md | 1743 | 0405885cbe3fe791c0e1a6c76da004d093d58cd55159ffeb3ca8c89e4ec045a3 |
| src/fcop/rules/_data/v4/envelopes.zh.md | 1672 | 0a69c9196e95185cf9e98b71af8c564be5797e26a71c5a9b7dc32d0735a08fef |
| src/fcop/rules/_data/v4/idempotency.en.md | 1720 | 1b100010d36342e6d98e9031429b3e11aad5657dfa953031e43bc4c99772a16a |
| src/fcop/rules/_data/v4/idempotency.zh.md | 1591 | 51c53931e02b1f39950f4a2f16b5e8e9a5f9d10b77f5ea1ad6b07c3e96385f08 |
| src/fcop/rules/_data/v4/lifecycle.en.md | 3041 | b6356c078ab00b893379f0b4f558616444ef4a4aa0e17432460719a9be362b2b |
| src/fcop/rules/_data/v4/lifecycle.zh.md | 2787 | 26b338914cffe2ea076f0e88133fc69617c91ecb149b3e40217baeef708cffef |
| src/fcop/rules/_data/v4/manifest.json | 11221 | 7efb1ba14df4d1ffbe164b8ec85dbf4316e7da4c0f367f3a506c78e4e29862d4 |
| src/fcop/rules/_data/v4/recovery.en.md | 3534 | aad4861efa59df69742c4bf577d57a553cbb170f6f92d61f6df74ec3ec503908 |
| src/fcop/rules/_data/v4/recovery.zh.md | 3099 | b19226071498f6414e11379b9d67cee36e4a79d65510fffefd14a021cd829000 |
| src/fcop/rules/_data/v4/relations.en.md | 1106 | 1b706c4ff76efb6edad40ab7985a0693eb9466da483d7024eb1f29668e022789 |
| src/fcop/rules/_data/v4/relations.zh.md | 1057 | fa51c77a568dae7f7cf41242b612ae2b2963075004aaebef533334a0466d3d42 |
| src/fcop/rules/_data/v4/workspace.en.md | 1920 | 06d4a9604fbab50ade36369f8f1d2950f099a241d659613cc78f1dd7e93555b3 |
| src/fcop/rules/_data/v4/workspace.zh.md | 1723 | 617009dc95cf4bedd252491334f45cf61fa1fe8ccf935f2127e2a1da9a49e30b |
| src/fcop/v4/boundary.py | 5988 | 1cb04f82d7bf5c4d14b73847e647131532019539ef801cae2344006f61dc9b4f |
| src/fcop/v4/creation.py | 45982 | 521288527b3335946a18ea136aa8ac2c53f4e0574bd3767633e58873039ce434 |
| src/fcop/v4/rule_distribution/__init__.py | 4096 | a7402c3c67b23d00201646be413e1fe12e6105c5caf2febca41742e408361f57 |
| src/fcop/v4/rule_distribution/_contract.py | 1716 | 519a40daf73012ee8f64009d744af59138390e67bbf6fd8dd7f07a14e1cec6e3 |
| src/fcop/v4/rule_distribution/_errors.py | 1022 | df1c0bece920f449bd4b60863188761fb18ee0a81280e0c1628f73e03e6815c8 |
| src/fcop/v4/rule_distribution/_loader.py | 6886 | eca7c4c9330dd6c351f07ebeee4112dcade03a76be93877df4fcd95a4b380ff4 |
| src/fcop/v4/rule_distribution/_selection.py | 6520 | 146027786c67e632ed18f2b7673211a27b58e818c3ced35fd7eee92b1f00a2f8 |
| tests/test_fcop/snapshots/public_surface.json | 54775 | 96d45a001c073083465ed3ae9a6db9725cdf3842256312a742808c6f15c456c5 |
| tests/test_fcop/test_v4_creation.py | 41309 | 960f24c1e9063101e7202cd4e73ec891d77bac19646f2c0054a844a265b04722 |
| tests/test_fcop/test_v4_rule_distribution.py | 9179 | ef8a9716ff47682408f378971be7252b4f1015ca479576ff1e9a5e41647b012a |

## Evidence qualification

The five current reports are IMPLEMENTATION-PLAN, CLAUSE-AND-ARTIFACT-MAPPING, CONFORMANCE-RESULT, RESULT and WP4C.3C-PUBLIC-METHOD-SET-ALIGNMENT. They retain historical failures with explicit stage labels and establish current raw candidate continuity, exact 38/11 sets, all twelve original assertions, 110 unchanged pre-existing Project method ASTs, all 86 future-node outcomes and raw test evidence identities.

Unlike PR #23's report-only delivery, this Content contains the actual candidate implementation and nineteen package data files. FCoP 1297/1297, Core 119/119, MCP 134/134 and current targets 56/56 ran against exactly these unchanged candidate bytes and the aligned historical test. Full distribution still exits 1 with 77 deferred future failures; the other nine future passes are structured zero-write negative preflight, not positive later-stage capabilities. No skipped/xfail cases or altered Conformance expectations.

The package is nine newly authored bilingual guidance modules, a strict offline loader, explicit sequential/parallel/development selection and one thin Project entry. Only validate/select/validate_operation_scope may succeed. All eighteen bytes/hash/size/parity and 73 primary owners validate before selection. Artifact records have ELEVEN fields, including conflicts_with; original taskbook's ten-field wording was already explicitly corrected by ADMIN. No mutable cache, network lookup, database, service, new runtime dependency or additional Core error.

Fourteen legacy rule data files match input bytes. Frozen specifications/contracts, Conformance, MCP, Host entries, CodeFlowMu, versions, workflows and releases remain unchanged. Local wheel/sdist contain nineteen matching source members; this is local inclusion/identity evidence only, not WP4C.6/RC/Host-consumption acceptance.

## Required fixed-HEAD remote verification and stop

After push, refetch the exact new review branch and require its HEAD to equal this Manifest commit. Verify each direct parent and exact per-commit set. Read all 38 cumulative paths from GitHub Contents API pinned to that same immutable SHA; compare complete raw bytes, sizes and SHA-256 against Git Blobs and a new detached LF checkout created with git -c core.autocrlf=false worktree add. Do not normalize any side or rewrite original working bytes. Verify clean execution and byte-check worktrees, original main da79dfefd99f597c9e422ce9edec22157f915a21, and remote main 68dbeb15f4e7f84e1d03f907be9fa66c2265843e.

Create a NEW Draft PR against taskbook/fcop-4.0-wp4c.3c-public-method-set, not main; never repurpose historical PRs, request reviewers, enable auto-merge or merge. Query real check/action state. The main/feat push and main-base PR filters may result in no runs; record NOT_TRIGGERED_BRANCH_FILTER instead of manufacturing green CI.

Only after successful readback publish the external final receipt with real Content/Manifest/remote HEAD, all-file hash count, Manifest self-hash, Draft PR URL and actual CI. Request WP4C_3_RULE_PACKAGE_ACCEPTED, do not sign it, and stop. WP4C.4, main merge, migration and publication remain unauthorized.
