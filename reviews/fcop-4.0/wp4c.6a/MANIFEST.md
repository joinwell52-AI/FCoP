# WP4C.6a blocked-delivery Manifest

This is a reports-only blocker receipt, not a successful implementation delivery or Gate request.

## Fixed identity and parent chain

```yaml
WP4C_6A_STATUS: BLOCKED
AUTHORIZED_SCOPE: WP4C_6A_HISTORICAL_ASSERTION_ALIGNMENT_AND_WP4C_6_RESUME_ONLY
ORIGINAL_TASKBOOK_COMMIT: dc4bd62d47c3c422c8e758b588369dd3ed089acd
ORIGINAL_TASKBOOK_SHA256: 457ec98aecaad481b68879069771c954d8e4069352ccdbe19838e92ddc61e06e
RULING_TASKBOOK_COMMIT: cd0fe4df900c3ff0b34beca957097f87a8d4b150
RULING_TASKBOOK_SHA256: 988738c5f175fd8ed91f4d9f32772282e79ef3caba6675c6b7ebb0facccb4aba
RULING_TASKBOOK_BYTES: 9619
BLOCKED_PR_29_HEAD: 91e64fa0a0ee377335af3226263a1811e1a56c1d
ALIGNMENT_COMMIT: NOT_COMMITTED_FAILED
CONTENT_COMMIT: 00df52e8b598a45c22f13aa23f63febab729f163
CONTENT_ROLE: FOUR_FACTUAL_REPORTS_ONLY
CONTENT_PARENT: cd0fe4df900c3ff0b34beca957097f87a8d4b150
MANIFEST_COMMIT: SELF
MANIFEST_PARENT: 00df52e8b598a45c22f13aa23f63febab729f163
IMPLEMENTATION_COMMIT: NOT_COMMITTED
BRANCH: feat/fcop-4.0-wp4c.6a-distribution-resume
PR_BASE: taskbook/fcop-4.0-wp4c.6-closeout
WORKTREE: D:/FCoP-wp4c6a-distribution-resume
WORKTREE_STATUS: DIRTY_PRESERVED
REQUESTED_GATE: NONE
```

`SELF` means the commit containing this Manifest. Its exact SHA and this Manifest's independent SHA-256 must be recorded in the post-push readback receipt; self-embedding either would be circular. The normal three-commit success sequence was not completed: the mandated first alignment validation failed. No failed alignment or candidate implementation is included in these two evidence-only commits. PR #29 remains untouched BLOCKED history.

## Delivered content inventory

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| reports/FCOP-4.0-WP4C.6-ARTIFACT-PARITY.md | 1882 | d624b5bdf2a915d3972fccfa71f7c0382d9957bacc4bfa49d73733fc353bb95d |
| reports/FCOP-4.0-WP4C.6-CONTEXT-MEASUREMENT.md | 1787 | 47dbc861cee7d0cd4ae1797e491aa36ab8a010c295949316d1c07ac442d6e713 |
| reports/FCOP-4.0-WP4C.6-IMPLEMENTABILITY-PROOF.md | 3347 | a312f7bc5ba0537e5b6ef788ceeebfbcf7ba25f5d141e9ac122c6e3de1062f58 |
| reports/FCOP-4.0-WP4C.6-RESULT.md | 7417 | 147ca72b2bf9c7a675d87ec3b75975077f75d006984bf80f3505fcda97dec269 |

Fifth and only other delivered path: `reviews/fcop-4.0/wp4c.6a/MANIFEST.md`. All files use UTF-8 without BOM and LF. Remote readback must verify the four listed hashes plus the Manifest independently.

## Recovered candidate inputs — not delivered

Each original source file and recovered copy matched the following PR #29 RESULT inventory before testing. No unlisted candidate changes existed. Original worktree: `D:/FCoP-wp4c6-distribution-closeout`.

| Path | Bytes | SHA-256 |
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

Additionally preserved, uncommitted: `tests/test_fcop/test_v4_rule_distribution.py` with the exact mandated replacement, SHA-256 `b0a77d2b84d51e435a5dd7b171554e83005023ed1d8e7568fbd5d863a832ad3e`.

## Ordinary Test ID mapping

| Historical ID | Authorized local replacement |
| --- | --- |
| test_future_positive_capability_is_absent[measure_context] | test_wp4c6_positive_capability_requires_complete_request[measure_context] |
| test_future_positive_capability_is_absent[build_artifacts] | test_wp4c6_positive_capability_requires_complete_request[build_artifacts] |

Both replacement nodes were executed and failed on uncaught `_DistributionError`. Each action rejected with structured `toolkit:RULE_SELECTION_INVALID`; the existing snapshot assertion did not fail. The expected-code assertion after `pytest.raises(V4ProtocolError)` was not reached.

JUnit: `C:/Users/Administrator/AppData/Local/Temp/fcop-wp4c6a-alignment-01.xml`; SHA-256 `12e38db40788e457a6183666b011d9f583836eee5925fba73691aa67228cf436`. Result: 0 passed / 2 failed / 38 deselected / 0 skipped, 5.37 seconds. Command and exception traces are in RESULT.

## Validation status and non-claims

| Check | Current continuation |
| --- | --- |
| Candidate source / transferred bytes | 11/11 / 11/11 matched |
| Exact ordinary alignment | 0 passed / 2 failed |
| Frozen distribution tree | 4f99c7261b63b6db81c500604a231defaca9f14b unchanged |
| DIST-27/28 / full distribution / Core | NOT_RUN_AFTER_ALIGNMENT_BLOCKER |
| FCoP / isolated MCP / serial combined | NOT_RUN_AFTER_ALIGNMENT_BLOCKER |
| Source / wheel / sdist / clean install | NOT_RUN_AFTER_ALIGNMENT_BLOCKER |
| Installed real stdio MCP 46/12/4 | NOT_RUN_AFTER_ALIGNMENT_BLOCKER |
| Fixed-ref CodeFlowMu Shadow | NOT_RUN_AFTER_ALIGNMENT_BLOCKER |
| Final implementation native Windows/Linux/macOS | NOT_RUN_NO_IMPLEMENTATION_COMMIT |
| Final implementation HEAD GitHub CI | NOT_RUN_NO_IMPLEMENTATION_COMMIT |
| Report UTF-8/no-BOM/LF and git diff check | PASS |

No earlier-stage test result or reports-only CI is an implementation PASS. No main, CodeFlowMu, merge, release, frozen specification, Schema, MCP, other old assertion or frozen Conformance change was made. Production error classes remain unchanged.

The narrow proposed ADMIN clarification is to allow the existing public `FcopError` catch in this single function, retaining the exact single structured-code assertion and unchanged parameter/snapshot checks. This proposal has not been implemented.

WP4C_RULE_DISTRIBUTION_ACCEPTED: false
REQUESTED_GATE: NONE
