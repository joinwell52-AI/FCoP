# WP4C.6 blocked-delivery Manifest

## Disposition

```yaml
WP4C_6_STATUS: BLOCKED
AUTHORIZED_SCOPE: WP4C_6_ONLY
DELIVERY_KIND: BLOCKED_REPORTS_ONLY
BLOCKER: HISTORICAL_FUTURE_CAPABILITY_ABSENCE_ASSERTION_CONFLICT
TASKBOOK_COMMIT: dc4bd62d47c3c422c8e758b588369dd3ed089acd
TASKBOOK_SHA256: 457ec98aecaad481b68879069771c954d8e4069352ccdbe19838e92ddc61e06e
TASKBOOK_BYTES: 14399
INPUT_HEAD: 8a4e2b175938af8b28e2983161862b49e8650256
WP4C_5_GATE_COMMIT: b5c1e11a4fc05b4c659f69ddad09d3290840f86a
FROZEN_CORE_CONTRACT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
FROZEN_DISTRIBUTION_CONTRACT: f6831de12991010f22672fb6e776ce85ef1507ff
FROZEN_DISTRIBUTION_TEST_TREE: 4f99c7261b63b6db81c500604a231defaca9f14b
CONTENT_COMMIT: 5015e083a6adc4aefbc0e1eea9f40fb7b450ed26
CONTENT_PARENT: dc4bd62d47c3c422c8e758b588369dd3ed089acd
MANIFEST_COMMIT: SELF
IMPLEMENTATION_COMMIT: NOT_COMMITTED
CANDIDATE_FILES_PRESERVED: 11/11
CANDIDATE_REACHABILITY: LOCAL_ONLY
WORKTREE_STATUS: DIRTY_PRESERVED
REVIEW_BRANCH: feat/fcop-4.0-wp4c.6-distribution-closeout
PR_BASE: taskbook/fcop-4.0-wp4c.6-closeout
REQUESTED_GATE: NONE
WP4C_RULE_DISTRIBUTION_ACCEPTED: false
MAIN_MODIFIED: false
CODEFLOWMU_FILES_MODIFIED: 0
RELEASE_CREATED: false
```

SELF denotes the commit containing only this Manifest, directly following the Content commit. Its SHA, remote HEAD and this file's own raw SHA-256 are reported in the post-push PR receipt; a file cannot truthfully embed its own final Git/hash identity. No report-only commit/CI is an implementation HEAD.

## Delivered content: four reports plus this Manifest

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| reports/FCOP-4.0-WP4C.6-ARTIFACT-PARITY.md | 5543 | 2580e6834a103062dbfeb1745cf24e08169a8b93e59f6e6035f48f247680a629 |
| reports/FCOP-4.0-WP4C.6-CONTEXT-MEASUREMENT.md | 3288 | 6729a14dd3b1f68500d357d5e70418bf6f7a29cbc41b58c3623a3a78d6a45b55 |
| reports/FCOP-4.0-WP4C.6-IMPLEMENTABILITY-PROOF.md | 4947 | 8bb2ee32a9c6033229d7fec57d36946fa39a6960e9708eb612a334a3b32cb58e |
| reports/FCOP-4.0-WP4C.6-RESULT.md | 7324 | 085305b6505b53420155df537c81383bed9c53d7e5f1215a55991f4ec1a6c048 |

The fifth delivered file is `reviews/fcop-4.0/wp4c.6/MANIFEST.md`. The Content commit changes only the four rows above; the Manifest-only commit adds only this file. Remote raw-Blob readback must verify all five after pushing. The eleven candidate implementation/test/CI/CHANGELOG files are NOT in these commits; their exact byte inventory is preserved in RESULT. No failed code or assertion correction is smuggled into a reports-only delivery.

## Actual execution evidence

| Check | Actual result | JUnit SHA-256 |
| --- | --- | --- |
| Initial frozen distribution | 156 passed + 20 expected DIST-27/28 failures; 0 skips | 53afa98a2b5002c8a4f83d560f2ac73509fd360c08f02510edef84595b3d1613 |
| Initial candidate ordinary tests | 59 passed; intermediate evidence, not final suite | 7874a94d3147b9526928685ce2f6719dc8fa6f20d5cc5577c74f18f19ff38fa2 |
| DIST-27 and DIST-28 | 2/2 and 18/18 passed | dbbfbb5f3e7a7ca7d630a143b1247f9baaa742a28691b2f9e24062cba87d1529 |
| Frozen distribution full | 176 passed, 0 failures/errors/skips | abd182c0ddfdc564fde9530aedb17a43a0f6e449094682efcd452e611bb11d83 |
| v4 Core | 119 passed, 0 failures/errors/skips | 3b4869a48239ef60f21126063dacf6ce125e70be520b595c34ec08f83bf2ae63 |
| FCoP full attempt with stop-on-first-failure | 1240 passed / 1 failed / incomplete | 09ccfcbf909a56914b50ff559111317dfd24ea479b67b776fdd90ea246680d05 |

Failure: `tests/test_fcop/test_v4_rule_distribution.py::test_future_positive_capability_is_absent[measure_context]`. The unchanged old test requires V4ProtocolError/OPERATION_NOT_IMPLEMENTED, whereas the implemented action correctly rejects its missing six historical inputs with structured RULE_SELECTION_INVALID. The other parameter, build_artifacts, has the same source-level old expectation but was not executed after the first failure. See RESULT for exact evidence and the requested ADMIN clarification.

Local commands used Python 3.12 on Windows, with PYTHONDONTWRITEBYTECODE=1 and PYTHONPATH selecting this worktree's src, mcp/src and root. All pytest runs used `-q --tb=short -p no:cacheprovider`, explicit fresh `D:/fcop-wp4c6-*` basetemp paths, and explicit JUnit outputs under `C:/Users/Administrator/AppData/Local/Temp/`. Full Core and subsequent FCoP runs used `-x`; the sequential shell chain stopped on the failed FCoP exit code before MCP/combined.

Frozen test commands: `python -X utf8 -m pytest tests/conformance/rule_distribution_v4`; target command selects only `test_dist_27 or test_dist_28` in `test_dist_25_30_failures_artifacts_context_gates.py`; Core command selects `tests/conformance/v4`; FCoP command selects `tests/test_fcop`. No skip, xfail, Test ID, frozen fixture or assertion was changed.

## Artifact and context facts

The real public candidate export test proved 19/19 canonical raw members in both formats and same-platform repeated archive hashes. ARTIFACT-PARITY lists all 19 source byte identities, and the separate data-carrier metadata meaning; normal Toolkit build/clean-install verification was not reached. CONTEXT-MEASUREMENT records all 18 frozen combinations and exact UTF-8 framing reuse with unknown Runtime consumption.

## Platform / CI limits and stop

| Evidence | Windows Python 3.12 local | Linux | macOS |
| --- | --- | --- | --- |
| DIST-27/28 and full distribution | PASS | NOT_RUN | NOT_RUN |
| Core | PASS | NOT_RUN | NOT_RUN |
| Full regression | BLOCKED | NOT_RUN | NOT_RUN |
| Final implementation HEAD CI | NOT_RUN | NOT_RUN | NOT_RUN |

Supported GitHub Python matrix remains 3.10/3.11/3.12/3.13 on the three native OSes, but it has not verified an implementation commit. The candidate additive CI wiring is also local/uncommitted. Any automatic Actions run on this reports-only branch is a baseline/report run and cannot satisfy WP4C.6 acceptance. No old-HEAD, pending, skipped or untriggered check is labeled PASS.

Taskbook section 9 is now enforced: no further implementation/testing, no Gate request, no merge, tag, publication, migration or downstream write. PRs #26–#28 and all original worktrees are preserved. Only report-delivery readback remains after this commit. ADMIN must explicitly resolve the historical ordinary-test assertion boundary before execution resumes.
