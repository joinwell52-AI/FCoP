# WP4C.6 execution result

Status: BLOCKED. Taskbook section 9 requires stopping on any old-test regression. Only the factual reports are delivered; candidate implementation is preserved locally, not committed as accepted code.

## Authority and scope

Taskbook `dc4bd62d47c3c422c8e758b588369dd3ed089acd`, SHA-256 `457ec98aecaad481b68879069771c954d8e4069352ccdbe19838e92ddc61e06e`, 14399 bytes. Parent Gate `b5c1e11a4fc05b4c659f69ddad09d3290840f86a` accepts WP4C.5 HEAD `8a4e2b175938af8b28e2983161862b49e8650256`. Only WP4C_6_ONLY is executed, in `D:/FCoP-wp4c6-distribution-closeout` on `feat/fcop-4.0-wp4c.6-distribution-closeout`.

No merge/release, CodeFlowMu write, existing-workspace migration, frozen-test change, new public facade, runtime dependency or background component is authorized or performed.

## Actual results so far

| Check | Actual result | Machine evidence |
| --- | --- | --- |
| Fixed initial distribution baseline | 156 passed / exactly 20 expected failures / 0 skipped, 724.03 s | fcop-wp4c6-baseline-01.xml |
| Initial new ordinary tests | 59 passed / 0 failed, 176.18 s | fcop-wp4c6-unit-01.xml |
| Frozen DIST-27/28 | 20 passed / 0 failed, 109.74 s | fcop-wp4c6-target-01.xml |
| Full final distribution suite | 176 passed / 0 failed / 0 skipped, 736.28 s | fcop-wp4c6-distribution-final01.xml |
| v4 Core Conformance | 119 passed / 0 failed / 0 skipped, 57.26 s | fcop-wp4c6-core-final01.xml |
| FCoP full regression, stopped by -x | 1240 passed / 1 failed / 0 skipped; incomplete, 648.47 s | fcop-wp4c6-fcop-final01.xml |
| Isolated MCP / serial combined | NOT_RUN_AFTER_BLOCKER | Sequential command chain exited on the failed FCoP run |
| Private implementation Ruff / mypy | PASS | Command output; full final checks pending |
| Installed package parity / stdio / fixed-ref Shadow | NOT_RUN_AFTER_BLOCKER | No earlier-stage evidence substituted |
| Final implementation HEAD native GitHub CI | NOT_RUN; no implementation commit | NOT_PASS |

JUnit files are under `C:/Users/Administrator/AppData/Local/Temp/`. Baseline SHA-256: `53afa98a2b5002c8a4f83d560f2ac73509fd360c08f02510edef84595b3d1613`; initial unit SHA-256: `7874a94d3147b9526928685ce2f6719dc8fa6f20d5cc5577c74f18f19ff38fa2`; target SHA-256: `dbbfbb5f3e7a7ca7d630a143b1247f9baaa742a28691b2f9e24062cba87d1529`.

The initial ordinary run preceded the final two small error-translation hardenings and three added checks; it is retained as intermediate evidence, not substituted for the final FCoP suite. The frozen target and full distribution/Core runs used the resulting production bytes. The later FCoP run stopped at the first old-test failure; remaining tests are unexecuted, not skipped or passed.

Final distribution JUnit SHA-256: `abd182c0ddfdc564fde9530aedb17a43a0f6e449094682efcd452e611bb11d83` (176 tests, zero failures/errors/skips).

## Observed blocker: historical absence assertion versus current action contract

`tests/test_fcop/test_v4_rule_distribution.py:174-178`, unchanged from the taskbook commit, parametrizes `measure_context` and `build_artifacts`. It requires `V4ProtocolError` with code `toolkit:OPERATION_NOT_IMPLEMENTED` for both actions. This is an earlier-stage absence assertion, not the frozen DIST-27/28 contract.

The first observed failing node is `test_future_positive_capability_is_absent[measure_context]`. Its ordinary fixture provides no `historical_surfaces`. The now-implemented public action rejects the incomplete request with structured `toolkit:RULE_SELECTION_INVALID: Exactly six historical surfaces required`, before any effects. The exception class/code therefore fails the historical absence expectation. The `build_artifacts` parameter contains the same historical expectation, but was NOT executed after `-x`; its conflict is a source-level finding, not a second observed test failure.

Taskbook sections 0/3/4 require implementing the actions with explicit input validation. Section 6 forbids changing assertions/Test IDs, and section 9 explicitly requires a stop on an old-test regression. Returning OPERATION_NOT_IMPLEMENTED solely to satisfy this old probe would disguise an implemented action's request-validation result. No such compatibility branch was added. The old test, frozen tests, contracts and all protected files remain unchanged.

FCoP failed-run JUnit SHA-256: `09ccfcbf909a56914b50ff559111317dfd24ea479b67b776fdd90ea246680d05` (1241 executed tests, 1 failure, 0 errors/skips). Core JUnit SHA-256: `3b4869a48239ef60f21126063dacf6ce125e70be520b595c34ec08f83bf2ae63`.

ADMIN decision needed: explicitly authorize aligning these two ordinary historical absence expectations with the newly authorized request boundary, or fix their historical audit scope. Preserve the two action parameters and the existing zero-effect helper. This report does not execute that correction or propose weakening the 176 frozen distribution nodes.

## Local candidate preservation — 11/11

The following exact bytes remain uncommitted in `D:/FCoP-wp4c6-distribution-closeout`. No reset, cleanup, stash, overwrite or migration was used. Reports-only GitHub CI cannot validate these local candidate bytes. A future separately authorized continuation must verify every hash before reuse and rerun the required sequence.

| Candidate path | Bytes | SHA-256 |
| --- | ---: | --- |
| .github/workflows/test-fcop.yml | 12763 | caa2d77983c52530049d9e171b19258df0724aaa484374e289d77e12cfeeb1f1 |
| .github/workflows/test-fcop-mcp.yml | 9106 | f709b11b870012aac468fde079b3a6b0f2a3a599fbc5dbd3cc59c31d14fbb067 |
| CHANGELOG.md | 132298 | 886207904c7d42caaf822f509ca2c65c911efa652ea81f22dcacf743c9f44318 |
| src/fcop/v4/rule_distribution/__init__.py | 5595 | 9566f6deac89bafed304957150d4585e8ed8ac9838e2fae28b0cebb19d6c398d |
| src/fcop/v4/rule_distribution/_artifacts.py | 7902 | 405aaac145415302326bb68762a7861a162c81211cf9e9f4622dbf6054b52e0e |
| src/fcop/v4/rule_distribution/_measurement.py | 3672 | 5da4ba521c8ea07b0a584dcf1323c3ecc3ec76d3046711025bc7ecd03700391a |
| src/fcop/v4/rule_distribution/_profiles.py | 3232 | c999662959d5dd94518711db3ec007333943a5101608973cb096d36af3b37784 |
| src/fcop/v4/rule_distribution/_projection.py | 6467 | b24ebd30e563d24f3947ca8b9f0b46becc5eea9d53ce1bc0ec085aeb45b33ffd |
| src/fcop/v4/rule_distribution/_selection.py | 6736 | 16b6ce8025f265c76a86b62c15451a83a656608c3c7a00aaab2b3a20bcc1f056 |
| tests/test_fcop/rule_distribution_artifact_probe.py | 3092 | 3bb3ce4f5bef9d1881a198efa118cbf3f61a07de5a0113e51a0099a1a611fbfc |
| tests/test_fcop/test_v4_rule_distribution_closeout.py | 12883 | e2bbff2de538b06faa8c41b333ec9e6afd86c44dbd18bf67b6fdd661cf06fc9d |

## Delivery state

The blocked delivery consists only of four factual reports plus a Manifest, in two commits on the authorized branch/new Draft PR. Candidate implementation, ordinary tests, CI wiring and CHANGELOG stay local and uncommitted. PRs #26–#28 remain preserved. Any CI on this reports-only HEAD is not implementation evidence. No claim of final native CI success, clean candidate worktree or implementation completion is made.

WP4C_6_STATUS: BLOCKED
BLOCKER: HISTORICAL_FUTURE_CAPABILITY_ABSENCE_ASSERTION_CONFLICT
CANDIDATE_FILES_PRESERVED: 11/11
CANDIDATE_REACHABILITY: LOCAL_ONLY
WORKTREE_STATUS: DIRTY_PRESERVED

REQUESTED_GATE: NONE
WP4C_RULE_DISTRIBUTION_ACCEPTED: false
