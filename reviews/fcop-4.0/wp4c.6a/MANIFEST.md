# WP4C.6b resumed implementation delivery Manifest

Local verification passed. Final remote/native CI is deliberately not preclaimed in this commit. The fixed-head post-push receipt in Draft PR #30 must supply remote hashes and actual CI conclusions before any Gate request.

## Fixed identity and append-only commit chain

```yaml
WP4C_6B_STATUS: LOCAL_VERIFIED_AWAITING_FINAL_HEAD_CI
AUTHORIZED_SCOPE: WP4C_6B_EXCEPTION_CATCH_CORRECTION_AND_WP4C_6_RESUME_ONLY
ORIGINAL_TASKBOOK_COMMIT: dc4bd62d47c3c422c8e758b588369dd3ed089acd
ORIGINAL_TASKBOOK_SHA256: 457ec98aecaad481b68879069771c954d8e4069352ccdbe19838e92ddc61e06e
WP4C_6A_RULING: cd0fe4df900c3ff0b34beca957097f87a8d4b150
WP4C_6A_SHA256: 988738c5f175fd8ed91f4d9f32772282e79ef3caba6675c6b7ebb0facccb4aba
ERRATUM_COMMIT: 8162d6ae9a91b8b23a6698bfd292a2cb2a75194c
ERRATUM_SHA256: 4fbf32c198f4ee624d55bd149c4152e3382894623c638b1001f943849900e306
ERRATUM_BYTES: 5334
ACCEPTED_WP4C_5_HEAD: 8a4e2b175938af8b28e2983161862b49e8650256
WP4C_5_GATE_COMMIT: b5c1e11a4fc05b4c659f69ddad09d3290840f86a
FROZEN_CORE_CONTRACT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
FROZEN_DISTRIBUTION_CONTRACT: f6831de12991010f22672fb6e776ce85ef1507ff
FROZEN_DISTRIBUTION_TEST_TREE: 4f99c7261b63b6db81c500604a231defaca9f14b
FROZEN_CORE_TEST_TREE: 24ab264c6bca9a3183ee270becb552f22a4c4f9e
BLOCKED_PR_29_HEAD: 91e64fa0a0ee377335af3226263a1811e1a56c1d
BLOCKED_PR_30_CONTENT: 00df52e8b598a45c22f13aa23f63febab729f163
BLOCKED_PR_30_HEAD: 576bad0025038ee085fc53da46c125143d126bd3
FAILED_LOCAL_ALIGNMENT_SHA256: b0a77d2b84d51e435a5dd7b171554e83005023ed1d8e7568fbd5d863a832ad3e
CANDIDATE_INPUT_HASHES: 11/11
ALIGNMENT_COMMIT: 22e2f558d3980d5647a1669e9455e4dacb60bc85
ALIGNMENT_PARENT: 8162d6ae9a91b8b23a6698bfd292a2cb2a75194c
CONTENT_COMMIT: 2cb503e627cdc44f09853748519d32b47284f0cb
CONTENT_PARENT: 22e2f558d3980d5647a1669e9455e4dacb60bc85
CONTENT_FILES: 15
MANIFEST_COMMIT: SELF
MANIFEST_PARENT: 2cb503e627cdc44f09853748519d32b47284f0cb
MANIFEST_FILES: 1
BRANCH: feat/fcop-4.0-wp4c.6a-distribution-resume
DRAFT_PR: 30
PR_BASE: taskbook/fcop-4.0-wp4c.6-closeout
WORKTREE: D:/FCoP-wp4c6a-distribution-resume
MAIN_MERGE_AUTHORIZED: false
RELEASE_AUTHORIZED: false
CODEFLOWMU_WRITE_AUTHORIZED: false
WP4C_RULE_DISTRIBUTION_ACCEPTED: false
REQUESTED_GATE: NONE
```

SELF means the commit that introduces this version of the Manifest. Its exact Git SHA and independent raw SHA-256 are recorded after push; self-embedding either would be circular. The post-push receipt must identify this exact implementation-containing HEAD, not an older reports-only run.

No blocked commit was rewritten, squashed, deleted or force-pushed. PR #29 remains unchanged. The user explicitly confirmed the erratum as PR #30's new current HEAD; the previous blocked HEAD in erratum section 2 remains the preserved historical checkpoint.

## Ordinary test alignment

| Historical ordinary ID | Active ADMIN-authorized ordinary ID |
| --- | --- |
| test_future_positive_capability_is_absent[measure_context] | test_wp4c6_positive_capability_requires_complete_request[measure_context] |
| test_future_positive_capability_is_absent[build_artifacts] | test_wp4c6_positive_capability_requires_complete_request[build_artifacts] |

The earlier local WP4C.6a function-name/code replacements were not previously committed. Thus Alignment contains three line replacements relative to its Git parent, but only the FcopError catch differs from the verified failed local input. Both parameters, exact toolkit:RULE_SELECTION_INVALID, imports, fixture/call/snapshot and every zero-effect assertion are preserved. No production error hierarchy or other old assertion changed. Fresh alignment is 2/2.

## Delivered content inventory

Sixteen files below plus this Manifest constitute seventeen agent-delivered paths relative to the erratum commit. Content alone contains eleven approved candidate files plus four reports (15); Alignment contains only the existing ordinary test file. The overall PR diff also includes the separate ADMIN erratum taskbook, not an additional agent implementation edit.

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| .github/workflows/test-fcop-mcp.yml | 9106 | f709b11b870012aac468fde079b3a6b0f2a3a599fbc5dbd3cc59c31d14fbb067 |
| .github/workflows/test-fcop.yml | 12763 | caa2d77983c52530049d9e171b19258df0724aaa484374e289d77e12cfeeb1f1 |
| CHANGELOG.md | 132298 | 886207904c7d42caaf822f509ca2c65c911efa652ea81f22dcacf743c9f44318 |
| reports/FCOP-4.0-WP4C.6-ARTIFACT-PARITY.md | 7660 | 1849121f3e431d0a83f5f76fb8efe217b2d5e8f337ddf3486128307205f4c55e |
| reports/FCOP-4.0-WP4C.6-CONTEXT-MEASUREMENT.md | 5231 | 0de12d5329c2f22a865824b6d306cb3634b388b509d41250b0f3959d89172d0c |
| reports/FCOP-4.0-WP4C.6-IMPLEMENTABILITY-PROOF.md | 5367 | fde4182cfeb84c226fd211929cf609b8a6c85bae8f1d8e5eb08ae8753403ffc7 |
| reports/FCOP-4.0-WP4C.6-RESULT.md | 14757 | 58128c8a410ffe40e9fa9ad03e1b541353e6a55ca50b39c7a3ae1a08fc083c8b |
| src/fcop/v4/rule_distribution/__init__.py | 5595 | 9566f6deac89bafed304957150d4585e8ed8ac9838e2fae28b0cebb19d6c398d |
| src/fcop/v4/rule_distribution/_artifacts.py | 7902 | 405aaac145415302326bb68762a7861a162c81211cf9e9f4622dbf6054b52e0e |
| src/fcop/v4/rule_distribution/_measurement.py | 3672 | 5da4ba521c8ea07b0a584dcf1323c3ecc3ec76d3046711025bc7ecd03700391a |
| src/fcop/v4/rule_distribution/_profiles.py | 3232 | c999662959d5dd94518711db3ec007333943a5101608973cb096d36af3b37784 |
| src/fcop/v4/rule_distribution/_projection.py | 6467 | b24ebd30e563d24f3947ca8b9f0b46becc5eea9d53ce1bc0ec085aeb45b33ffd |
| src/fcop/v4/rule_distribution/_selection.py | 6736 | 16b6ce8025f265c76a86b62c15451a83a656608c3c7a00aaab2b3a20bcc1f056 |
| tests/test_fcop/rule_distribution_artifact_probe.py | 3092 | 3bb3ce4f5bef9d1881a198efa118cbf3f61a07de5a0113e51a0099a1a611fbfc |
| tests/test_fcop/test_v4_rule_distribution.py | 9598 | 1905cc752c455b41d77defb41a4dd7a21d1fba3a1d51850dd74d7390e0b97bc2 |
| tests/test_fcop/test_v4_rule_distribution_closeout.py | 12883 | e2bbff2de538b06faa8c41b333ec9e6afd86c44dbd18bf67b6fdd661cf06fc9d |

Seventeenth path: reviews/fcop-4.0/wp4c.6a/MANIFEST.md. Its own raw byte count/hash are verified separately in the post-push receipt.

The eleven original/recovered candidates match PR #29's inventory exactly; their hashes above are unchanged. Original D:/FCoP-wp4c6-distribution-closeout and the user's D:/FCoP workspace remain preserved. All seventeen delivery files must be strict UTF-8/no-BOM/LF at remote readback and fresh checkout.

## Fresh stable-byte local evidence

| Check | Actual result |
| --- | --- |
| Alignment | 2/2 |
| DIST-27 / DIST-28 | 2/2 / 18/18 |
| Full Rule Distribution | 176/176 |
| v4 Core | 119/119 |
| FCoP isolated | 1459/1459 |
| MCP isolated | 158/158 |
| Serial combined | 1736/1736 |
| Explicit public surface | 4/4, unchanged snapshot |
| Ruff root / MCP canonical CI commands | PASS / PASS |
| mypy FCoP / MCP source / MCP tests | PASS (55 / 18 / 11 files) |
| Normal FCoP and MCP wheel/sdist builds | PASS, unchanged development versions |
| Source/wheel/sdist/isolated installed canonical bytes | 19/19 |
| Installed actual stdio | 46 tools / 12 static resources / 4 templates |
| Installed Project/MCP resource parity and zero writes | 5/5 |
| Installed Relay and missing-extra diagnostic | PASS |
| Context matrix / full projection oracle | 18/18 |
| Fixed-ref CodeFlowMu read-only Shadow | 14/14 raw Blobs, zero task writes |

Every completed pytest suite has zero failures, errors and skips. Final combined JUnit: C:/Users/Administrator/AppData/Local/Temp/fcop-wp4c6b-combined-01.xml, SHA-256 ca3e6458932974121ff059226e6aa715e2878c67ce5104dc0eb09cf3ed952862, 1736 tests, 3174.433 seconds. Other JUnit hashes, exact selections and temporary-environment installation retry are recorded in RESULT. No pre-blocker result substitutes for this continuation.

## Canonical artifacts and measurement

Manifest raw identity: 7efb1ba14df4d1ffbe164b8ec85dbf4316e7da4c0f367f3a506c78e4e29862d4, 11221 bytes. ARTIFACT-PARITY lists all nineteen canonical members, sizes and hashes and the source/archive/installed checks.

| Normal local artifact | SHA-256 |
| --- | --- |
| fcop-3.2.5-py3-none-any.whl | b382282a76d93f0cfa08b898445e2614b3f8732f61e1fd74256003c74b441b28 |
| fcop-3.2.5.tar.gz | e72b1fd41e62664ce83b7342fb5b962b2df145cbb91eb389d9065e1f49fd2faf |
| fcop_mcp-3.2.5-py3-none-any.whl | 5e3ff514c1fca324bbd27a6597c44bc0db4189ea58705b866718f1102a0ba132 |
| fcop_mcp-3.2.5.tar.gz | 46b245d0d9ad686fe6daf25a97e28fef223d93febf0573d5412be07ddafd2756 |

Same-platform repeated public offline exports produced wheel SHA 152716140d60e435a040ba6e524deda46a8b80407521cb1d1015e87afbe003f2 and sdist SHA ffc8ce654bde1049f69c87a466272f43038bc7772f5cc4d6117c8a2f998c4f87 on both invocations. These are local rule-data carriers, not releases. Whole-archive cross-platform digest equality is not inferred.

CONTEXT-MEASUREMENT records the actual eighteen canonical-package measurements. Estimator: exact-utf8-byte-count/v1; unit utf8_bytes; runtime_consumption_verified=null. No Host or Runtime consumption is claimed.

## Final remote/native acceptance is not yet established

At this Manifest's construction time:

| Platform / check | State |
| --- | --- |
| Local Windows Python 3.12 | Completed evidence above |
| Final HEAD Windows 3.10-3.13 CI | PENDING |
| Final HEAD Ubuntu 3.10-3.13 CI | PENDING |
| Final HEAD macOS 3.10-3.13 CI | PENDING |
| Final HEAD package/coverage and other applicable jobs | PENDING |
| Raw GitHub Blob readback / fresh LF checkout | PENDING_POST_PUSH |

The known erratum-only Windows encoding/specification-drift failures are preserved in RESULT, not hidden or called final implementation results. No .gitattributes, loader tolerance, frozen data, tests or thresholds were changed to mask them. Final implementation HEAD jobs must actually finish. Old-head success, skipped applicable jobs, pending, cancellation and absence of runs do not authorize a Gate.

Post-push procedure: push this branch without force; refetch; verify the three appended commits and GitHub PR HEAD; compare each of seventeen raw GitHub file Blobs against committed and fresh-LF-checkout bytes; confirm main remains 68dbeb15f4e7f84e1d03f907be9fa66c2265843e and original workspace HEAD da79dfefd99f597c9e422ce9edec22157f915a21; inspect the exact final Manifest HEAD's native jobs and package checks. Publish that fixed-head receipt in PR #30.

If any applicable final check fails or needs a new unauthorized correction, stop with REQUESTED_GATE: NONE and preserve the actual failure. Only complete verification permits requesting WP4C_RULE_DISTRIBUTION_ACCEPTED. ADMIN alone signs it. No main merge, release, CodeFlowMu change or next-stage work is authorized.
