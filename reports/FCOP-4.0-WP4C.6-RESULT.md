# WP4C.6a execution result — BLOCKED

Original taskbook: dc4bd62d47c3c422c8e758b588369dd3ed089acd (SHA-256 457ec98aecaad481b68879069771c954d8e4069352ccdbe19838e92ddc61e06e).
Ruling taskbook: cd0fe4df900c3ff0b34beca957097f87a8d4b150 (9619 bytes; SHA-256 988738c5f175fd8ed91f4d9f32772282e79ef3caba6675c6b7ebb0facccb4aba).
Scope: WP4C_6A_HISTORICAL_ASSERTION_ALIGNMENT_AND_WP4C_6_RESUME_ONLY.

## Current conclusion

The exact taskbook replacement was applied locally and both selected ordinary nodes were executed. Result: **0 passed / 2 failed / 38 deselected / 0 skipped**, 5.37 seconds, Windows Python 3.12.9 / pytest 9.0.3. Both failures are exception-class mismatches: the code returns the requested structured Toolkit error, but the replacement catches the separate `V4ProtocolError` subclass.

This is not a renewed objection to retiring the historical absence sentinel. ADMIN's retirement decision has been followed exactly. The remaining problem is the replacement snippet's catch type.

## Fixed-input verification

- GitHub raw ruling: 9619 bytes, expected SHA-256 matched; strict UTF-8, no BOM, LF.
- Original taskbook raw SHA-256 matched.
- Ruling parent: original taskbook `dc4bd62d47c3c422c8e758b588369dd3ed089acd`.
- PR #29: OPEN / Draft; HEAD `91e64fa0a0ee377335af3226263a1811e1a56c1d`; exactly four reports and one Manifest. All five remote blobs matched the preserved readback copy. No PR #29 mutation.
- Frozen distribution tree: `4f99c7261b63b6db81c500604a231defaca9f14b`.
- Core specification and distribution-contract files: no difference against their fixed frozen commits.
- Source candidate inventory: 11/11 matched; no unlisted candidate modifications.
- New worktree: `D:/FCoP-wp4c6a-distribution-resume`.
- New branch: `feat/fcop-4.0-wp4c.6a-distribution-resume`.
- New worktree started clean at the ruling commit; transfer hashes 11/11 matched.

## Test identities and exact change

| Historical ordinary Test ID | Authorized local replacement Test ID | Actual result |
| --- | --- | --- |
| test_future_positive_capability_is_absent[measure_context] | test_wp4c6_positive_capability_requires_complete_request[measure_context] | FAILED: uncaught Toolkit error |
| test_future_positive_capability_is_absent[build_artifacts] | test_wp4c6_positive_capability_requires_complete_request[build_artifacts] | FAILED: uncaught Toolkit error |

These are ordinary tests, not renamed frozen Conformance IDs. The only code changes to the existing test file are the function name and expected code. The original `pytest.raises(V4ProtocolError)` remains, as required by the fixed snippet. Fixture, parameters, `call`, `snapshot`, all other assertions and all frozen tests remain unchanged.

Aligned local file SHA-256: `b0a77d2b84d51e435a5dd7b171554e83005023ed1d8e7568fbd5d863a832ad3e`. This failed alignment is preserved locally and is NOT committed as a successful alignment.

## Reproduction and machine evidence

Working directory: new worktree above. Environment: `PYTHONDONTWRITEBYTECODE=1`, `PYTHONPATH=<new worktree>/src;<new worktree>/mcp/src;<new worktree>`.

```text
python -B -m pytest tests/test_fcop/test_v4_rule_distribution.py -k test_wp4c6_positive_capability_requires_complete_request -vv -p no:cacheprovider --basetemp=D:/fcop-wp4c6a-alignment-01 --junitxml=C:/Users/Administrator/AppData/Local/Temp/fcop-wp4c6a-alignment-01.xml
```

Exit code 1. JUnit SHA-256: `12e38db40788e457a6183666b011d9f583836eee5925fba73691aa67228cf436`. Both selected nodes were run; this was not a stop-after-first-failure run.

```text
measure_context:
  _measurement.py:39 -> _errors.py:27
  _DistributionError: toolkit:RULE_SELECTION_INVALID:
  Exactly six historical surfaces required

build_artifacts:
  _artifacts.py:127 -> _errors.py:27
  _DistributionError: toolkit:RULE_SELECTION_INVALID:
  Explicit offline non-isolated formats required
```

The helper's `finally: assert snapshot(root.parent) == before` executed without an assertion failure in both nodes. The expected structured-code assertion after the catch was not reached. Independent read-only type inspection confirmed `isinstance(error, FcopError) == True` and `isinstance(error, V4ProtocolError) == False`.

## Preserved eleven-file candidate inventory

Copied byte-for-byte from the PR #29 RESULT inventory; originals and new copies remain local, uncommitted.

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

## Stop and delivery boundaries

The first mandatory validation failed. DIST-27/28, all later regression, packaging, installed stdio, Shadow and native CI were not run in this continuation. Historical passing results in PR #29 are not relabeled as final evidence.

No production changes beyond the exact approved eleven-file transfer were made. No error hierarchy, other old assertion, fixture, frozen Conformance, Core specification, Schema, MCP or CodeFlowMu change was made. Local main remains `da79dfefd99f597c9e422ce9edec22157f915a21` with its existing four tracked modifications; remote main was `68dbeb15f4e7f84e1d03f907be9fa66c2265843e`. No merge, tag or release.

The normal success pipeline requires an Alignment-only commit followed by Content and Manifest commits. It is not represented as completed. This stop delivers only four factual reports and a Manifest, with no failed alignment or candidate implementation included. Any CI triggered by this reports-only delivery is not candidate implementation evidence.

ADMIN clarification requested: permit the existing public `FcopError` catch in this one function, retaining the exact single namespaced code assertion and all zero-effect/parameter checks. No such additional edit has been applied.

```yaml
WP4C_6A_STATUS: BLOCKED
BLOCKER: RULING_REPLACEMENT_EXCEPTION_CLASS_MISMATCH
CANDIDATE_INPUT_HASHES: 11/11
CANDIDATE_TRANSFER_HASHES: 11/11
HISTORICAL_ASSERTION_ALIGNMENT: 0_passed_2_failed
ALIGNMENT_COMMIT: NOT_COMMITTED
IMPLEMENTATION_COMMIT: NOT_COMMITTED
CANDIDATE_REACHABILITY: LOCAL_ONLY
WORKTREE_STATUS: DIRTY_PRESERVED
GITHUB_CI_AT_IMPLEMENTATION_HEAD: NOT_RUN
REQUESTED_GATE: NONE
WP4C_RULE_DISTRIBUTION_ACCEPTED: false
```
