# WP4C.3 conformance result — WP4C.3c closeout

## Current WP4C.3c validation

Authority: ec2e43cd87ce264da1b77365558a182736ccb24f; raw SHA-256 c81c883c6ccf4f132ed12f511684eed93fc455fc37125b85ed4c15d8fbaeee80. Isolated alignment commit: 96ad2ae812c60a6362d9c360dbb815621a0cbe1a. Candidate implementation remains byte-identical to the 31-file PR #23 inventory. No Conformance, production candidate or behavioral expectation was edited during this closeout.

Current local validation result: PASS. Full tests/test_fcop completed with 1297 passed / 0 failed / 0 errors / 0 skipped. The historical 39-versus-38 blocker is resolved by the authorized test-only alignment, not by changing candidate code. All current target and regression requirements pass; UNEXPECTED_FAILURES=0. Remote delivery verification follows the later Manifest commit; only then request the unsigned Gate.

Environment: Windows / Python 3.12.9 / pytest 9.0.3. PYTHONDONTWRITEBYTECODE=1, PYTHONPATH includes this independent worktree's src, mcp/src and root. All pytest invocations use -q -p no:cacheprovider; MCP additionally uses --import-mode=importlib. No skip/xfail, fixture timeout, dependency declaration or workflow change.

| Current invocation/check | Actual result | Exit |
| --- | --- | ---: |
| test_v4_creation.py::test_closeout_boundary_reflection_binding_and_subclass | 1 passed, 3 warnings, 7.10s | 0 |
| test_v4_creation.py + test_public_surface.py | 102 passed, 3 warnings, 76.28s | 0 |
| tests/test_fcop full regression | 1297 passed, 3 warnings, 1127.73s | 0 |
| tests/conformance/v4 | 119 passed, 3 warnings, 110.80s | 0 |
| tests/test_fcop_mcp, isolated importlib | 134 passed, 3 warnings, 367.37s | 0 |
| Distribution test_dist_00_meta.py + exact test_dist_30 | 34 passed (33 Meta + 1 control), 1 warning, 18.04s | 0 |
| Distribution --collect-only | 176 collected, 0.23s | 0 |
| Precise ten current file::function paths | 56 passed, 3 warnings, 199.09s | 0 |
| Complete tests/conformance/rule_distribution_v4 | 99 passed / 77 deferred failed, 176 total, 3 warnings, 548.28s | 1 (classified future red baseline) |
| tests/test_fcop/test_v4_rule_distribution.py | 41 passed, 3 warnings, 187.94s | 0 |
| Ruff src/fcop tests/test_fcop tests/conformance/rule_distribution_v4 | PASS | 0 |
| mypy --cache-dir nul | PASS, 46 source files | 0 |
| python -B -m build --wheel --sdist --outdir temporary/packages | fcop-3.2.5 wheel and sdist built | 0 |
| Source / wheel / sdist local v4 data check | 19/19 paths and bytes equal in each archive | 0 |
| Raw candidate hashes before/after import and alignment | 31/31 unchanged | 0 |
| Historical public set / v4-only set | Exact 38 / 11; sole addition rule_distribution | 0 |
| Existing Project method ASTs and public snapshot | 110 old ASTs unchanged; exactly one additive snapshot entry | 0 |
| Legacy data / frozen contracts / Conformance / allowed write set | 14/14 legacy bytes unchanged; protected paths unchanged; scope PASS | 0 |

The exact targets are test_dist_01–07, test_dist_21, test_dist_22, test_dist_25, using file::function paths; no filename-matching -k shortcut. Full collection independently reproduces all 56 current nodes. The 41 standalone new units are also included in the full FCoP run and must not be double-counted as additional full-suite nodes.

## Current exhaustive future-node disposition

The complete 176-node JUnit file was independently parsed: Meta=33 pass, current=56 pass, DIST-30=1 pass, future=9 negative-overlap pass +77 deferred failures. Every current node passed. No errors or skips. The same 86 future node identities are present in the prior WP4C.3b report; they are listed again below with this run's actual observations.

Each negative-overlap pass has operation_evidence with changed_paths=[] and zero_write_verified=true, and a structured rejection, not positive Host inspection, projection, adoption, deployment or recovery. These nine are permitted read-only preflight overlap under original taskbook section 11.3, not later-stage acceptance. The failed real two-process apply test returned no success (assert []), not a queue timeout; its future deployment race remains unaccepted. Shadow did not access downstream files. Core workspace/version errors are not rewritten to mimic future Toolkit adoption handling.

| Future node | Current disposition | Observed boundary |
| --- | --- | --- |
| test_dist_08[valid] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_08[file-without-adoption] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_08[wrong-workspace] | DEFERRED_RED | WORKSPACE_ID_MISMATCH |
| test_dist_08[v3] | DEFERRED_RED | UNSUPPORTED_WORKSPACE_VERSION |
| test_dist_08[broken-previous] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_08[actor-only] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_09[success] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_09[before-drift] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_09[receipt-tamper] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_10[success] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_10[missing-backup] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_10[modified-backup] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_10[modified-target] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_10[arbitrary-version] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_11[codex] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_11[cursor] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_11[claude-code] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_11[unknown-host] | NEGATIVE_OVERLAP_PASS | toolkit:RULE_HOST_UNAVAILABLE |
| test_dist_11[unknown-profile] | NEGATIVE_OVERLAP_PASS | toolkit:RULE_HOST_UNAVAILABLE |
| test_dist_11[evaluator] | NEGATIVE_OVERLAP_PASS | toolkit:RULE_HOST_UNAVAILABLE |
| test_dist_11[model-probe] | NEGATIVE_OVERLAP_PASS | toolkit:RULE_HOST_UNAVAILABLE |
| test_dist_11[duplicate-key] | NEGATIVE_OVERLAP_PASS | toolkit:RULE_HOST_UNAVAILABLE |
| test_dist_12[support-only] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_12[adoption-only] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_12[generated] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_12[consumption-only] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_13[False-codex] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_13[False-cursor] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_13[False-claude-code] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_13[True-codex] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_13[True-cursor] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_13[True-claude-code] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_14 | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_15[preserve] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_15[nested] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_15[duplicate] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_15[missing] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_15[oversized-user-region] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_16[reference] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_16[stale-snapshot] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_16[missing-snapshot] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_16[escaping-reference] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_17[exact] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_17[unadopted-multilingual] | NEGATIVE_OVERLAP_PASS | toolkit:RULE_SELECTION_INVALID |
| test_dist_17[overflow] | NEGATIVE_OVERLAP_PASS | toolkit:RULE_PROJECTION_LIMIT |
| test_dist_17[broken-source-link] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_18[False] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_18[True] | NEGATIVE_OVERLAP_PASS | toolkit:RULE_OWNERSHIP_CONFLICT |
| test_dist_19[stale-plan] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_19[two-processes] | DEFERRED_RED | No apply success; real two-process future success assertion fails |
| test_dist_20[before_stage_durable] | DEFERRED_RED | toolkit:RULE_ADOPTION_REQUIRED |
| test_dist_20[between_replacements] | DEFERRED_RED | toolkit:RULE_ADOPTION_REQUIRED |
| test_dist_20[before_success_receipt] | DEFERRED_RED | toolkit:RULE_ADOPTION_REQUIRED |
| test_dist_23[unversioned-v3] | DEFERRED_RED | UNSUPPORTED_WORKSPACE_VERSION |
| test_dist_23[explicit-v4-on-v3] | DEFERRED_RED | UNSUPPORTED_WORKSPACE_VERSION |
| test_dist_23[v4-no-adoption] | NEGATIVE_OVERLAP_PASS | toolkit:RULE_ADOPTION_REQUIRED |
| test_dist_24[3.0-fcop://rules] | DEFERRED_RED | UNSUPPORTED_WORKSPACE_VERSION |
| test_dist_24[3.0-fcop://protocol] | DEFERRED_RED | UNSUPPORTED_WORKSPACE_VERSION |
| test_dist_24[3.0-fcop://guidance/sequential/en] | DEFERRED_RED | UNSUPPORTED_WORKSPACE_VERSION |
| test_dist_24[3.0-fcop://team] | DEFERRED_RED | UNSUPPORTED_WORKSPACE_VERSION |
| test_dist_24[4.0-fcop://rules] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_24[4.0-fcop://protocol] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_24[4.0-fcop://guidance/sequential/en] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_24[4.0-fcop://team] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_26 | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_27[wheel] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_27[sdist] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages0-codex-sequential] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages0-codex-parallel] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages0-cursor-sequential] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages0-cursor-parallel] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages0-claude-code-sequential] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages0-claude-code-parallel] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages1-codex-sequential] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages1-codex-parallel] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages1-cursor-sequential] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages1-cursor-parallel] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages1-claude-code-sequential] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages1-claude-code-parallel] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages2-codex-sequential] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages2-codex-parallel] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages2-cursor-sequential] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages2-cursor-parallel] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages2-claude-code-sequential] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages2-claude-code-parallel] | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_29 | DEFERRED_RED | toolkit:OPERATION_NOT_IMPLEMENTED (assertion output); no downstream access |

UNEXPLAINED_FUTURE_PASSES=0. The raw full distribution process remains exit 1; neither 176/176 green nor 86/86 failures is claimed. Future stage ownership is unchanged. No Host output, receipt or future positive API was created.

## Reproducible evidence identities and package scope

After final report updates, Meta + DIST-30 were rerun: 34 passed, 1 warning, 12.59s. Ruff again passed and mypy again reported no issues in 46 source files. Final scope/UTF-8/LF/AST audits passed, the candidate hashes remained 31/31 unchanged and original assertions removed remained zero. Only report prose changed after the full implementation test runs.

Temporary test output directory: C:/Users/ADMINI~1/AppData/Local/Temp/fcop-wp4c3c-validation-62260999804748d5a5c0dd3fae11595c. It is not an extra repository delivery path. Each report hashes complete JUnit bytes, with no normalization:

- distribution.xml: 57d1910d0658ac341c9f8ae0db67b51249b49d16043ee72ac8a7c3ab12a1271e
- core.xml: f371ace2e62e18f03a6a5db00e44a1ef8e55f5310ff4dce9f7e362c163a4a8c9
- mcp.xml: 1612bc0df85e00e7fcef0b066a309ff0f81311ce62686d97e6125434ac2d2baa
- meta-control.xml: b0773b62e22f529b3271a40ed7f4cf519df30b21963dfbf2b9e359e34fea53a4
- targets.xml: 11aed675e4e71a22c0e6444f6c500e2536a810b353b057a3ef6cb465ff6000be
- units.xml: 021ac02097a7a9e3d8d7ddea0186c5abaece23a4a76bd07f828875ee51d3c7a2
- fcop.xml: 99a7f00d50776f663addbf8481fbe2df852d1cc993d2a11f03b2ae222b4aa3c7

Local built archive identities: fcop-3.2.5-py3-none-any.whl SHA-256 6413f8ba3eb728f59beb95b80126ce85bf2987d698a12d673ccb71a60c54be95; fcop-3.2.5.tar.gz SHA-256 bcc1efe10a8a9b676178e94a99231da064015b01fa6ac088fca91e35bb41dffa. Declared hatchling>=1.21 was installed only in the normal isolated build environment. Package checks establish this local build's inclusion/identity; they do NOT establish WP4C.6 cross-platform, installed-host consumption, RC or publication. Library version remains 3.2.5; rule-data version remains the preserved 4.0.0-candidate.1.

The following sections preserve the exact earlier failures and historical results. Their BLOCKED/current wording describes their named historical stage, not the WP4C.3c result above.

## Preserved WP4C.3b validation (historical)


Current verdict: BLOCKED. Full FCoP result: 1296 passed / 1 failed / 3 warnings in 966.26 s, exit 1. The sole failure is the historical method-count assertion outside the write scope; isolated rerun is 1 failed (39 != 38) in 1.48 s. All 41 new distribution unit nodes passed within that complete run. Existing Project methods are unchanged; rule_distribution is the sole authorized addition. UNEXPECTED_REGRESSION_FAILURES=1; the earlier zero-failure checkpoint below is superseded. Implementation results refer to preserved LOCAL_ONLY bytes, not the report-only remote tree.

After the blocker reports were written, Meta + DIST-30 were rerun: 34 passed, 1 warning, 13.26 s, exit 0. No audit allowlist or frozen file was changed. No further production/test edits were made after confirming the blocker.

## WP4C.3b implementation validation (current)

Authority: fixed taskbook 3a11498c0d4aff736628e781f34516950cb34be8 and isolated fixture commit 115751b4c24a1924062a81a21e0d655e8cb5fedc. Earlier sections below remain the historical WP4C.3a record.

Environment: Windows, Python 3.12.9, pytest 9.0.3, source-root PYTHONPATH (src, mcp/src, repository), PYTHONDONTWRITEBYTECODE=1. No Conformance expectation, skip/xfail or timeout changed.

| Verification | Actual observed result | Exit |
| --- | --- | ---: |
| Precise ten target function paths, -q -p no:cacheprovider --tb=short | 56 passed, 3 existing warnings, 197.69 s | 0 |
| Full tests/conformance/rule_distribution_v4, -q -p no:cacheprovider --tb=line --junitxml=<temporary evidence path> | 99 passed / 77 failed, 176 total, 3 warnings, 517.50 s | 1 (classified future reds) |
| Distribution collect-only | 176 nodes, 0.22 s | 0 |
| tests/conformance/v4 | 119 passed, 3 warnings, 104.60 s | 0 |
| tests/test_fcop_mcp --import-mode=importlib | 134 passed, 3 warnings, 298.13 s | 0 |
| Preliminary independent unit + public snapshot | 42 passed (38 then-existing new units + 4 snapshot checks), 126.80 s | 0 |
| Ruff src/fcop tests/test_fcop tests/conformance/rule_distribution_v4 | All checks passed | 0 |
| mypy src/fcop --cache-dir nul | 46 source files, no issues | 0 |
| build --wheel --sdist (isolated declared backend) | fcop-3.2.5 wheel/sdist built; 19/19 v4 data names in each | 0 |
| Existing Project methods / snapshot | All preexisting method ASTs unchanged; snapshot delta exactly rule_distribution | 0 |
| Existing v4 wiring | Only two creation registry/import lines and one boundary policy line added | 0 |
| Legacy raw rule sources | 14/14 bytes equal fixed taskbook Git Blobs | 0 |
| Allowed paths, UTF-8/LF, frozen inputs, git diff --check | PASS at implementation checkpoint | 0 |

Full FCoP result is now final above. Three additional unit nodes were added after the preliminary 42-node run; all are included and passed in that full run.

The exact target selection uses file::function paths for test_dist_01 through test_dist_07, test_dist_21, test_dist_22 and test_dist_25, not a -k substring that also matches filenames. The full suite independently verifies the same 56 nodes.

JUnit raw evidence SHA-256: 97788a1748aecf50601652bede8e312be41b2b7fec97863566fc7ef821fd794f. File: C:/Users/Administrator/AppData/Local/Temp/fcop-wp4c3b-validation-2a9719adad854f57b892f0648ee62982/distribution.xml. This temporary test output is not an additional repository delivery path. The following exhaustive classification was extracted from its 176 testcases and operation_evidence properties.

### 86 future-owner nodes: 77 deferred reds, 9 explained negative overlaps

Meta 33/33, current 56/56 and control 1/1 pass. Future owners remain unimplemented. The nine passing future nodes below exercise only already-authorized negative preflight, each with changed_paths=[] and zero_write_verified=true; none returned successful Host inspection, plan, deployment, adoption or recovery. Thus these are explained overlaps under original WP4C.3 section 11.3, not additional future-stage acceptance.

| Future node | Structured rejection | Why no stage capability was implemented |
| --- | --- | --- |
| test_dist_11[unknown-host] | toolkit:RULE_HOST_UNAVAILABLE | Unknown static host rejected; no Host support result. |
| test_dist_11[unknown-profile] | toolkit:RULE_HOST_UNAVAILABLE | Unproven mode/version rejected; no reference support implemented. |
| test_dist_11[evaluator] | toolkit:RULE_HOST_UNAVAILABLE | Unknown profile evaluator field rejected; no callable registered. |
| test_dist_11[model-probe] | toolkit:RULE_HOST_UNAVAILABLE | Unknown probe field rejected; no model/Host probe executed. |
| test_dist_11[duplicate-key] | toolkit:RULE_HOST_UNAVAILABLE | Strict static JSON duplicate-key rejection. |
| test_dist_17[unadopted-multilingual] | toolkit:RULE_SELECTION_INVALID | Incomplete explicit language/profile selection rejected before projection. |
| test_dist_17[overflow] | toolkit:RULE_PROJECTION_LIMIT | Raw selected byte lower bound exceeds cap; no projection constructed. |
| test_dist_18[True] | toolkit:RULE_OWNERSHIP_CONFLICT | Existing target without proven ownership rejected; no plan returned. |
| test_dist_23[v4-no-adoption] | toolkit:RULE_ADOPTION_REQUIRED | Absent adoption ref rejected before any write. |

The other 77 future nodes are listed individually below. A Base workspace/version rejection is preserved, not rewritten as a Toolkit code; future adoption/legacy adapter handling is not implemented here. Fault-injection future nodes stop at missing adoption, before any partial write; their expected later recovery code is not claimed. DIST-19[two-processes] ran real processes, but no apply succeeded (assertion on empty successes); this is a deferred deployment race, not an accepted concurrency implementation. No queue timeout or crash is being reclassified as conformance success.

| Deferred node | Actual boundary observed |
| --- | --- |
| test_dist_08[valid] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_08[file-without-adoption] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_08[wrong-workspace] | WORKSPACE_ID_MISMATCH |
| test_dist_08[v3] | UNSUPPORTED_WORKSPACE_VERSION |
| test_dist_08[broken-previous] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_08[actor-only] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_09[success] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_09[before-drift] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_09[receipt-tamper] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_10[success] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_10[missing-backup] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_10[modified-backup] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_10[modified-target] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_10[arbitrary-version] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_11[codex] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_11[cursor] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_11[claude-code] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_12[support-only] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_12[adoption-only] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_12[generated] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_12[consumption-only] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_13[False-codex] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_13[False-cursor] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_13[False-claude-code] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_13[True-codex] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_13[True-cursor] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_13[True-claude-code] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_14 | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_15[preserve] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_15[nested] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_15[duplicate] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_15[missing] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_15[oversized-user-region] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_16[reference] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_16[stale-snapshot] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_16[missing-snapshot] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_16[escaping-reference] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_17[exact] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_17[broken-source-link] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_18[False] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_19[stale-plan] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_19[two-processes] | No successful apply; future success assertion fails |
| test_dist_20[before_stage_durable] | toolkit:RULE_ADOPTION_REQUIRED |
| test_dist_20[between_replacements] | toolkit:RULE_ADOPTION_REQUIRED |
| test_dist_20[before_success_receipt] | toolkit:RULE_ADOPTION_REQUIRED |
| test_dist_23[unversioned-v3] | UNSUPPORTED_WORKSPACE_VERSION |
| test_dist_23[explicit-v4-on-v3] | UNSUPPORTED_WORKSPACE_VERSION |
| test_dist_24[3.0-fcop://rules] | UNSUPPORTED_WORKSPACE_VERSION |
| test_dist_24[3.0-fcop://protocol] | UNSUPPORTED_WORKSPACE_VERSION |
| test_dist_24[3.0-fcop://guidance/sequential/en] | UNSUPPORTED_WORKSPACE_VERSION |
| test_dist_24[3.0-fcop://team] | UNSUPPORTED_WORKSPACE_VERSION |
| test_dist_24[4.0-fcop://rules] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_24[4.0-fcop://protocol] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_24[4.0-fcop://guidance/sequential/en] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_24[4.0-fcop://team] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_26 | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_27[wheel] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_27[sdist] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages0-codex-sequential] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages0-codex-parallel] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages0-cursor-sequential] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages0-cursor-parallel] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages0-claude-code-sequential] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages0-claude-code-parallel] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages1-codex-sequential] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages1-codex-parallel] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages1-cursor-sequential] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages1-cursor-parallel] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages1-claude-code-sequential] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages1-claude-code-parallel] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages2-codex-sequential] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages2-codex-parallel] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages2-cursor-sequential] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages2-cursor-parallel] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages2-claude-code-sequential] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages2-claude-code-parallel] | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_29 | OPERATION_NOT_IMPLEMENTED (captured exception; audit property omits code) |

UNEXPECTED_FAILURES=0 for the authorized target and existing regressions completed so far; UNEXPLAINED_FUTURE_PASSES=0. Do not report the raw suite as fully green or say all 86 future nodes failed.

### Intermediate failures and execution observations retained

- Fixture phase redundant encoding argument triggered Ruff UP012, mechanically corrected before its isolated commit with identical UTF-8 bytes.
- Preliminary -k target selection also matched filenames: 63 passed / 53 failed / 60 deselected in 339.16 s. This was a mixed subset, superseded by the precise 56-node and complete 176-node commands; no acceptance count derives from it.
- An added unit parametrization used pytest's reserved name request, causing collection error before execution. Renamed only the new unit parameter to scope_input; no frozen file changed. The complete FCoP run was restarted.
- --no-isolation build initially lacked hatchling.build in the current Python. A normal isolated build installed only the already-declared hatchling>=1.21 backend and succeeded. No runtime/build dependency declaration was changed. Package checks cover inclusion only, not WP4C.6 raw artifact acceptance.
- An attempted report replacement patch was rejected for two operations on one path, before any write; the report was updated using a normal patch.
- Existing importlib Traversable / jsonschema RefResolver deprecation warnings remain; no code/dependency change was made to hide them.


## Preserved WP4C.3a pre-implementation evidence

Taskbook: `0559e0fdf5390aa830f98a38d83f96f1cd475ab1`, path `taskbooks/fcop-4.0/WP4C.3a/01-Historical-Audit-Scope-Alignment-and-WP4C.3-Resume-Taskbook-v1.0.zh.md`.
Raw bytes: 15954; SHA-256: `903c5f0f249598ab3b5aaf7e947af8ed36fbc23928eff9b5db11e305acb21ba6`.
[ADMIN authorization](https://github.com/joinwell52-AI/FCoP/pull/21#issuecomment-5567383721) and [hash erratum](https://github.com/joinwell52-AI/FCoP/pull/21#issuecomment-5567650164) were read back. The revoked `a61c4159...` is NOT an accepted identity.
Direct parent: `78ea6b89a1ef0df0e504a3cfa34cecddeb7dda24`; original WP4C.3 taskbook: `de213ec0f74f8976283a24986d4eb7de77c67142` (SHA-256 `a4b782db3a984be9872d6c99428c5fc669a1cd3135468b33ef8eba7a6c1b57d2`).
Audit correction commit: `e1ed85e4ba5aba212ddf3cc4f880c0abecc2bfab`, direct child of the corrected-identity taskbook.
Scope: `WP4C_3A_AUDIT_SCOPE_ALIGNMENT_AND_WP4C_3_RESUME`.

## Executed validation

Environment: Windows, Python 3.12.9, pytest 9.0.3; independent worktree `D:/FCoP-wp4c3a-audit-scope-and-rule-package`. Set `PYTHONDONTWRITEBYTECODE=1`; PYTHONPATH points to this worktree's src, mcp/src and root. Pytest commands use `-p no:cacheprovider`; no skip/xfail or test timeout was added.

| Command (relative to worktree) | Actual outcome | Exit |
| --- | --- | ---: |
| python -B -m pytest tests/conformance/rule_distribution_v4/test_dist_00_meta.py tests/conformance/rule_distribution_v4/test_dist_25_30_failures_artifacts_context_gates.py::test_dist_30 -q -p no:cacheprovider --tb=short | 34 passed, 1 warning, 16.21s (33 Meta + DIST-30) | 0 |
| python -B -m pytest tests/conformance/rule_distribution_v4 --collect-only -q -p no:cacheprovider | 176 nodes: 33 Meta + 56 current + 86 future + 1 control | 0 |
| python -B -m pytest tests/conformance/rule_distribution_v4 --ignore=tests/conformance/rule_distribution_v4/test_dist_00_meta.py -q -p no:cacheprovider --tb=line | 142 failed, 1 passed, 3 warnings, 364.12s; all 142 failures are DistributionNotImplementedError / RULE_DISTRIBUTION_NOT_IMPLEMENTED | 1 (expected red baseline) |
| python -B -m pytest tests/test_fcop -q -p no:cacheprovider | 1256 passed, 3 warnings, 994.31s | 0 |
| python -B -m pytest tests/conformance/v4 -q -p no:cacheprovider | 119 passed, 3 warnings, 122.30s | 0 |
| python -B -m pytest tests/test_fcop_mcp --import-mode=importlib -q -p no:cacheprovider | 134 passed, 3 warnings, 354.62s | 0 |
| python -B -m ruff check src/fcop tests/test_fcop tests/conformance/rule_distribution_v4 | All checks passed | 0 |
| python -B -m mypy --cache-dir nul | Success: no issues found in 41 source files | 0 |
| git diff --check | No whitespace errors | 0 |

Existing warnings concern importlib.abc.Traversable and jsonschema.RefResolver deprecations. No production or dependency changes were made to silence them.

### Intermediate execution failure preserved

The first complete behavioral invocation used in-process `pytest.main` from `python -c` with an evidence collector, while other suites ran. It produced 142 failed / 1 passed in 611.02s: 141 structured missing-capability errors, one `queue.Empty` at DIST-19[two-processes]. It is NOT classified as a clean baseline. Its precise environment/harness cause was not established.

A standard `python -B -m pytest ...::test_dist_19[two-processes] -q -p no:cacheprovider --tb=short` rerun produced the expected structured DistributionNotImplementedError in 2.26s; the helper's two-process and zero-write assertions executed before that error. The complete standard-entry rerun then produced all 142 expected structured reds and DIST-30 PASS. No source, timeout, assertion, skip or xfail was changed for either rerun.

This resolves the test-run anomaly as a non-reproduced intermediate failure, not a production race acceptance. No WP4C.4 race success is claimed.


Post-audit-commit Meta + DIST-30 rerun with the current reports (including one untracked current-stage report): 34 passed, 1 warning, 17.04s, exit 0. This additionally demonstrates that legitimate later files do not alter the historical13 result.

## Frozen evidence stability

Comparing taskbook blobs with the audit correction: all DIST-01 through DIST-29 function ASTs, including parametrization and assertions, are identical. DIST-30 retains 18 Assert nodes before and after; only its final historical range/merge audit changed. All 30 DIST function IDs remain. The six other suite files (including driver and test_dist_01_06_manifest.py) retain their original Git blob identities. No skip/xfail was added. Collection remains 176.

| DIST ID | Nodes | Final pre-implementation classification |
| --- | ---: | --- |
| DIST-01 | 2 | Expected red |
| DIST-02 | 4 | Expected red; success-fixture input defect requires ADMIN |
| DIST-03 | 6 | Expected red |
| DIST-04 | 11 | Expected red |
| DIST-05 | 9 | Expected red |
| DIST-06 | 6 | Expected red |
| DIST-07 | 4 | Expected red |
| DIST-21 | 2 | Expected red |
| DIST-22 | 4 | Expected red |
| DIST-25 | 8 | Expected red |
| Current total | 56 | Not implemented |
| Future owners | 86 | Expected red |
| DIST-30 | 1 | PASS |

56/56 green is NOT claimed. The new finding is an incomplete success fixture, separately diagnosed from the expected missing-production red baseline; see [the plan](FCOP-4.0-WP4C.3-IMPLEMENTATION-PLAN.md). No production method, data file or package inclusion was added. Build validation of a nonexistent candidate package was NOT_RUN; existing public-surface tests are included in the 1256 FCoP passes and its snapshot is unchanged.

## Preserved history

PR #21 remains an OPEN Draft at `78ea6b89a1ef0df0e504a3cfa34cecddeb7dda24`; it was not rewritten, merged or repurposed. Its Content `0e89f94aa8df017817f76dadc8572c8bc5c0afdf` and Manifest remain ancestors. The prior 32/33 Meta and DIST-30 failure is an accepted historical blocker, now resolved by the separate audit commit. This report updates current facts; it does not erase that history.
