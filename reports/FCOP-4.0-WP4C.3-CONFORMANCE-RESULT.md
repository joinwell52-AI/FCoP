# WP4C.3 conformance result — WP4C.3b implementation verification

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
