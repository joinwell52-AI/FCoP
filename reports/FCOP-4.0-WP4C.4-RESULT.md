# WP4C.4 result and verification record

## Authority and scope

```yaml
WP4C_4_STATUS: LOCAL_VALIDATION_COMPLETE
AUTHORIZED_SCOPE: WP4C_4_ONLY
TASKBOOK_COMMIT: 01c53355293c08f100b9f6e5aba0caea015d27cd
TASKBOOK_SHA256: c8d91d0c0d24804f8b06bb3dde9d07f14febc1d75411778fd74f6272398b0d78
TASKBOOK_BYTES: 18707
INPUT_HEAD: 4f56cfcf9754bb509b7bd353e830a8e4003810ea
WP4C_3_GATE_COMMIT: e24b16185dcd9b8746c26d08654c6ed285a2a8c7
FROZEN_DISTRIBUTION_CONTRACT: f6831de12991010f22672fb6e776ce85ef1507ff
WORKTREE: D:/FCoP-wp4c4-host-projection
BRANCH: review/fcop-4.0-wp4c.4-host-projection
PR_BASE: taskbook/fcop-4.0-wp4c.4-host-projection
NEW_PUBLIC_FACADES: 0
NEW_RUNTIME_DEPENDENCIES: 0
NEW_BACKGROUND_COMPONENTS: 0
NEW_AUTHORITATIVE_STORES: 0
NEW_PRIVATE_MODULES: 5
FROZEN_FILES_MODIFIED: 0
MCP_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0
MAIN_MODIFIED: false
RELEASE_CREATED: false
WP4C_5_STARTED: false
WP4C_4_HOST_PROJECTION_ACCEPTED: false
REQUESTED_GATE: NONE
```

[Fixed taskbook](https://github.com/joinwell52-AI/FCoP/blob/01c53355293c08f100b9f6e5aba0caea015d27cd/taskbooks/fcop-4.0/WP4C.4/01-Host-Projection-Adoption-Deployment-and-Rollback-Taskbook-v1.0.zh.md). Before implementation, GitHub raw bytes, fetched Git Blob, exact SHA/size, UTF-8/no BOM/LF and direct parent Gate were verified. The new independent worktree was created from that fixed taskbook, not main or a local candidate commit. The pre-code proof was written and reviewed before production edits.

Original D:/FCoP remains at da79dfefd99f597c9e422ce9edec22157f915a21 with its pre-existing dirty dogfood/history materials preserved. Previous accepted rule-package worktree remains unmodified. Remote main baseline is 68dbeb15f4e7f84e1d03f907be9fa66c2265843e. No clean, migration, rule redeploy, role reassignment or CodeFlowMu operation was performed.

## Delivered behavior

The existing facade now provides strictly static Profile inspection/status, explicit byte-bound adoption, deterministic bounded/reference projection, zero-write plans, fresh-input deployment with immutable evidence, verified immediate rollback and explicit partial-failure inspection/restoration. No Host process is detected or contacted. No evaluator, network callback, probe, background replay, registry, publication or automatic adoption is installed.

Use [HOST-PROJECTION-MAPPING](FCOP-4.0-WP4C.4-HOST-PROJECTION-MAPPING.md) for field/action/ownership mapping and [ATOMICITY-AND-RECOVERY-PROOF](FCOP-4.0-WP4C.4-ATOMICITY-AND-RECOVERY-PROOF.md) for exact physical windows and limits. The [IMPLEMENTABILITY-PROOF](FCOP-4.0-WP4C.4-IMPLEMENTABILITY-PROOF.md) retains the complete 53-row pre-code baseline instead of replacing historical red evidence with final results.

Native platform: Windows, Python 3.12.9. Linux/macOS: NOT_NATIVE_VERIFIED unless actual review-HEAD runners run. Runtime consumption is UNKNOWN/None, not proven by successful generation or package installation.

## Development failures and superseded runs — retained

1. Baseline exact 53 target nodes: 8 passed / 45 expected failures, 130.93s. These were missing WP4C.4 behavior, not completed capability.
2. First implementation exact targets: 33 passed / 20 failed, 207.89s. A reproduced class of failures was Windows MAX_PATH during immutable publication under a long pytest root. Private extended-length Win32 I/O and short, fresh test roots addressed that environmental/implementation boundary without relaxing path hashes or changing Core.
3. Next target run: 53/53 passed, 317.92s. This was not treated as sufficient delivery proof. Further review found normal rollback lacked durable evidence for the restore-before-receipt window; deployment and rollback were moved onto one private commit path, and staging/backup ordering was aligned with taskbook section 9.
4. Initial supplemental units incorrectly expected V4ProtocolError for Toolkit failures. Actual _DistributionError derives from FcopError and carries the existing structured toolkit code. The new units and the two authorized stage-advanced old unit expectations were corrected to that error boundary, preserving code and zero-write assertions. No frozen Conformance was edited. The obsolete run was stopped before completion; no final pass/fail count is inferred from partial output.
5. Superseded full/distribution collections were stopped as this review added mandatory history/receipt checks and the final pre-loader UNC rejection. Their test sandboxes and raw available outputs were retained. They are not counted as final acceptance. Completed intermediate runs below remain explicit evidence, not a substitute for the final complete collection.
6. `python -m build --no-isolation` initially failed before compilation because the host Python lacked Hatchling. Standard isolated `python -m build` then built both artifacts successfully, without changing dependencies or global tooling. Earlier builds were superseded by a rebuild after the final source correction.
7. A completed comprehensive development run produced 142 passed / 34 failed in 1258.87s. Exactly two were WP4C.4 defects: DIST-15[preserve] misclassified a legitimate new user-region plan as an exact replay; DIST-19[two-processes] exposed the reused primitive's default 15-second lock wait during slow native file flushes. The other 32 failures belonged to WP4C.5/6. This run is not accepted as final. Its JUnit SHA-256 is 9d6f5f70d3d2040f9d87c66cf7bcb4570dce4cab9460aa48660e388476393b17.
8. The retry path now first distinguishes current target bytes from the last committed full bytes; a fresh user-region update follows ordinary plan validation, while an unchanged-target replay still requires the complete original supplied plan. The private apply call explicitly waits at most 45 seconds using the unchanged Core lock, and checks pending intents only after acquiring it. This does not change the frozen race test's 60-second queue bound, rewrite a Base error, create a lease or replay a failed operation. The reproduced error was LOCK_RECOVERY_REQUIRED with one genuine success, not a guessed exception message. Preserved-region update, real two-process contention and exact-plan tamper rejection then passed together, 3/3 in 75.28s. Full-suite reruns follow these scoped corrections.

No failed state was committed, no assertion was removed to make a red light disappear, and no skip/xfail was added. New tests also cover a real spawned process exit after actual replacement, interrupted rollback receipt publication, invalid rollback time before effects, user bytes added between deployments, complete-plan retry tampering, indirect paths, strict Profile bytes, receipt identity/chain substitution and all input/history drift before apply. The UNC guard is a negative I/O test: it fails if Loader is reached; it does not fake a successful result.

## Reproducible commands and completed supporting evidence

Commands run from the independent worktree with PYTHONDONTWRITEBYTECODE=1 and PYTHONPATH set only to its src, mcp/src and root. Every pytest command uses `-q -p no:cacheprovider`, a new explicit `--basetemp=D:/fcop-wp4c4-...` and an external JUnit path. Existing test roots were not reused or deleted.

| Scope | Command suffix / evidence | Actual result |
| --- | --- | --- |
| Core + MCP | `python -m pytest tests/conformance/v4 tests/test_fcop_mcp` | 253 passed: Core 119, MCP 134; 564.06s |
| Independent Host units, earlier complete collection | `python -m pytest tests/test_fcop/test_v4_rule_distribution_host.py -x` | 44 passed; 780.83s |
| Owned-target windows, user bytes and rollback interruption | same file, `-k 'fault_with_owned or rollback_receipt_interruption or rollback_keeps'` | 5 passed / 40 deselected; 279.95s |
| Receipt/chain and historical input substitution | same file, `-k 'identity_and_chain or historical_evidence'` | 6 passed / 45 deselected; 132.64s |
| UNC before Loader I/O | same file, `-k manifest_unc` | 1 passed / 51 deselected; 4.68s |
| Ruff | `python -m ruff check src tests` | PASS |
| mypy | `python -m mypy src/fcop` | PASS, 51 source files |
| Git whitespace | `git diff --check` | PASS; global autocrlf warnings are not file changes |

These supporting test runs overlap; their counts must not be summed into a fictitious total. Final full-run counts and exact future-owner accounting are recorded in the completion section below.

| JUnit evidence in C:/Users/Administrator/AppData/Local/Temp | Raw SHA-256 |
| --- | --- |
| fcop-wp4c4-target-baseline.xml | f042ba79dc905d9d02c9a67ca51c60c9058a74bc7f19badf40e553dcdc61c54c |
| fcop-wp4c4-target-implementation.xml | df353b1b2895416d4fc1febe794a0cf5abdd31b245583bc920837428b048201a |
| fcop-wp4c4-target-02.xml | 1c57aa379c8616b2a02e0a8332bc4a02cbcf004b3a40f2498e8c686d1ca3993a |
| fcop-wp4c4-unit-02.xml | c4ab553b6ee5958769a41d1ed97a11485b71e0614a7823ddadf60e951e8b0d6f |
| fcop-wp4c4-recovery-01.xml | a65ad0f09dd292fe261572b1fb4324b3a0600f7728f993909d196592e3a90f44 |
| fcop-wp4c4-evidence-final.xml | e5bd62b9b0ea8cbef753e6322c90034e25f64a6c012ae049b62882fc41eaa31c |
| fcop-wp4c4-core-mcp-final.xml | 6030b7ddd85be3a8b9ed39aa68f4e89e6fb4dcde6ff52f197af2311c0b7215fc |

## Local artifact evidence

Final build: `python -m build --outdir C:/Users/Administrator/AppData/Local/Temp/fcop-wp4c4-build-delivery`. Wheel is built from the generated sdist. Raw member comparison passes 30/30 for each artifact: 19 unchanged canonical package members, all ten private distribution Python modules, and Project. No bundled Host Profile data or package-data edit is introduced.

- fcop-3.2.5-py3-none-any.whl SHA-256: 286f022ec66b3829860a638bcdc7f303e7933bfa30c4fac087ed1ca8b1796c55
- fcop-3.2.5.tar.gz SHA-256: e4823f2e4179b857ef5bbd95af90f7cde37accd8bfa2f889b23a2de6830a42e6
- Canonical Manifest SHA-256 remains 7efb1ba14df4d1ffbe164b8ec85dbf4316e7da4c0f367f3a506c78e4e29862d4.
- Installation uses a new external target with `--no-index --no-deps`; it does not upgrade the original workspace or publish a package.
- Verified installed location: C:/Users/Administrator/AppData/Local/Temp/fcop-wp4c4-installed-delivery. All five new module imports resolve there, not the source tree; bundled loading returns 18 artifacts and the same Manifest identity. The public signature remains `(self, *, action, request)`.

## Scope and independent public checks

159 tracked raw Git Blobs under frozen spec/contracts/Conformance, MCP, canonical rules, Schema, workflow and package configuration matched the fixed taskbook commit byte-for-byte. Project retains all 111 method names; only rule_distribution's authorized narrow legacy-adopt rejection changes its AST body, and its signature AST is identical. The other 110 method ASTs are unchanged. Public-surface tests pass 4/4 without updating the snapshot. Full final collection is 1349 FCoP nodes, including 93 distribution units (41 prior-stage units plus 52 new Host units); rule-distribution collection remains 176 nodes with frozen IDs untouched.

## Delivery protocol

Content commit contains only authorized implementation/units/CHANGELOG and four reports. Manifest-only commit will contain only reviews/fcop-4.0/wp4c.4/MANIFEST.md. Actual commit IDs, final HEAD, file hashes and post-push verification belong to that Manifest and the external PR receipt, avoiding self-hashing claims.

A new Draft PR targets the taskbook branch, not main and not old PR #24. Existing test workflows trigger only on main/feat pushes or PRs to main. If no final-HEAD run/check exists for this authorized review/base pair, record NOT_TRIGGERED_BRANCH_FILTER, not PASS; no workflow edit or unauthorized main-target PR is used to force CI. No reviewer, merge, auto-merge or release is requested.

## Final distribution owner accounting

The final full command returned **144 passed / 32 failed / zero skipped**, exit 1, in 1195.14s. Exit 1 is retained: the suite contains unauthorized future-stage obligations. Its JUnit raw SHA-256 is 98ca2b0bce1cda2a5268618f71a94ba54009c1abc10713c38312120c1be0ce21 (fcop-wp4c4-dist-delivery.xml). Exact frozen docstring owners were parsed and reconciled against every collected result; no failing node belongs to WP4C.4 or a previously accepted owner.

| Owner / classification | Total | Passed | Expected future failures |
| --- | ---: | ---: | ---: |
| Meta / Static | 33 | 33 | 0 |
| WP4C.2 control plane DIST-30 | 1 | 1 | 0 |
| WP4C.3 previous targets | 56 | 56 | 0 |
| WP4C.4 DIST-08–20 | 53 | 53 | 0 |
| WP4C.5 | 13 | 1 | 12 |
| WP4C.6 | 20 | 0 | 20 |

The single future-owner overlap pass is DIST-23[v4-no-adoption], an existing rejection boundary. It is not WP4C.5 execution or acceptance. DIST-26 and DIST-29 belong to WP4C.5 according to their frozen metadata; artifact/context nodes belong to WP4C.6. Local packaging verification does not implement the future public build_artifacts action.

| Exact remaining red node | Unique future owner | Action | Recorded structured outcome |
| --- | --- | --- | --- |
| test_dist_23[unversioned-v3] | WP4C.5 | redeploy | UNSUPPORTED_WORKSPACE_VERSION |
| test_dist_23[explicit-v4-on-v3] | WP4C.5 | apply | UNSUPPORTED_WORKSPACE_VERSION |
| test_dist_24[3.0-fcop://rules] | WP4C.5 | read_resource | UNSUPPORTED_WORKSPACE_VERSION |
| test_dist_24[3.0-fcop://protocol] | WP4C.5 | read_resource | UNSUPPORTED_WORKSPACE_VERSION |
| test_dist_24[3.0-fcop://guidance/sequential/en] | WP4C.5 | read_resource | UNSUPPORTED_WORKSPACE_VERSION |
| test_dist_24[3.0-fcop://team] | WP4C.5 | read_resource | UNSUPPORTED_WORKSPACE_VERSION |
| test_dist_24[4.0-fcop://rules] | WP4C.5 | read_resource | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_24[4.0-fcop://protocol] | WP4C.5 | read_resource | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_24[4.0-fcop://guidance/sequential/en] | WP4C.5 | read_resource | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_24[4.0-fcop://team] | WP4C.5 | read_resource | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_26 | WP4C.5 | inspect_layers | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_27[wheel] | WP4C.6 | build_artifacts | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_27[sdist] | WP4C.6 | build_artifacts | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages0-codex-sequential] | WP4C.6 | measure_context | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages0-codex-parallel] | WP4C.6 | measure_context | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages0-cursor-sequential] | WP4C.6 | measure_context | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages0-cursor-parallel] | WP4C.6 | measure_context | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages0-claude-code-sequential] | WP4C.6 | measure_context | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages0-claude-code-parallel] | WP4C.6 | measure_context | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages1-codex-sequential] | WP4C.6 | measure_context | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages1-codex-parallel] | WP4C.6 | measure_context | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages1-cursor-sequential] | WP4C.6 | measure_context | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages1-cursor-parallel] | WP4C.6 | measure_context | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages1-claude-code-sequential] | WP4C.6 | measure_context | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages1-claude-code-parallel] | WP4C.6 | measure_context | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages2-codex-sequential] | WP4C.6 | measure_context | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages2-codex-parallel] | WP4C.6 | measure_context | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages2-cursor-sequential] | WP4C.6 | measure_context | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages2-cursor-parallel] | WP4C.6 | measure_context | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages2-claude-code-sequential] | WP4C.6 | measure_context | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_28[languages2-claude-code-parallel] | WP4C.6 | measure_context | toolkit:OPERATION_NOT_IMPLEMENTED |
| test_dist_29 | WP4C.5 | shadow | Not recorded in operation property; unmet authorization assertion |

All 13 target IDs are present, with these per-ID node counts: DIST-08 6; 09 3; 10 5; 11 8; 12 4; 13 6; 14 1; 15 5; 16 4; 17 4; 18 2; 19 2; 20 3 = 53. All passed. The frozen two-process test performs real concurrent apply with one unique success identity, and the three failure windows all inspect/restore real effects.

## Final completion evidence

Final source was frozen before the following runs and rehashed after them; the 13-file implementation/test fingerprint was unchanged. No final acceptance count below comes from a run started on superseded code.

| Final native command scope | Result | CLI elapsed | JUnit raw SHA-256 |
| --- | --- | --- | --- |
| `python -m pytest tests/test_fcop` | 1349 passed / 0 failed / 0 skipped | 1345.88s | 27658485005e39fd65927c1b590a7f6ba996ce5364b7013ef98d5d5583753439 |
| `python -m pytest tests/conformance/v4 tests/test_fcop_mcp` | 253 passed: 119 Core + 134 MCP | 446.28s | 81dba77bf3ea26859f94b6fc3149311eb7be15676720990c7f6fd4799eb72d7d |
| `python -m pytest tests/conformance/rule_distribution_v4` | 144 passed / 32 expected future failures | 1195.14s | 98ca2b0bce1cda2a5268618f71a94ba54009c1abc10713c38312120c1be0ce21 |
| Public-surface snapshot | 4 passed, no snapshot change | 0.29s | 2e013805962b67d7b84b69defe840c2226ebce6b7d547d115edab2e886dbb82b |

Final JUnit files, respectively: fcop-wp4c4-fcop-delivery.xml, fcop-wp4c4-core-mcp-delivery.xml, fcop-wp4c4-dist-delivery.xml and fcop-wp4c4-surface-verified.xml, under the external Temp directory recorded above. Full commands additionally use `-q --tb=line -p no:cacheprovider`, fresh D:/fcop-wp4c4-{fcop,core-mcp,dist}-delivery sandboxes and the matching `--junitxml` path. The 93 distribution units (41 existing-stage + 52 new Host units) are a verified subset of the 1349 pass count, not an additional independent total. Three existing deprecation warnings were retained; no warning suppression was introduced.

Post-run Ruff, mypy (51 files), whitespace, 16/16 content-file strict UTF-8/LF/no-BOM and 159/159 protected raw-Blob checks pass. Public facade signature and the other 110 Project method ASTs remain unchanged. Packaged raw members match the final source 30/30 in each archive. Required local verification is complete; unexpected failures: zero. Windows is native-verified; Linux/macOS remain NOT_NATIVE_VERIFIED.

At this Content Commit, remote delivery is intentionally PENDING. The following Manifest-only commit binds these 16 content files and their actual Content Commit. The post-push PR execution receipt will record remote HEAD, all 17 raw file hashes (including Manifest), parent sets, new LF detached checkout and actual CI status. Only that completed external receipt requests WP4C_4_HOST_PROJECTION_ACCEPTED; this pre-push document does not claim remote verification or ADMIN acceptance in advance.
