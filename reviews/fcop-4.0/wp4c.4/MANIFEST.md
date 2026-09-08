# WP4C.4 delivery Manifest

## Immutable authority and two-commit chain

```yaml
AUTHORIZED_SCOPE: WP4C_4_ONLY
TASKBOOK_COMMIT: 01c53355293c08f100b9f6e5aba0caea015d27cd
TASKBOOK_SHA256: c8d91d0c0d24804f8b06bb3dde9d07f14febc1d75411778fd74f6272398b0d78
TASKBOOK_BYTES: 18707
INPUT_HEAD: 4f56cfcf9754bb509b7bd353e830a8e4003810ea
WP4C_3_GATE_COMMIT: e24b16185dcd9b8746c26d08654c6ed285a2a8c7
FROZEN_DISTRIBUTION_CONTRACT: f6831de12991010f22672fb6e776ce85ef1507ff
CONTENT_PARENT: 01c53355293c08f100b9f6e5aba0caea015d27cd
CONTENT_COMMIT: 90fd061e82d82ec5639a70c7964fdd5d24191886
MANIFEST_PARENT: 90fd061e82d82ec5639a70c7964fdd5d24191886
MANIFEST_COMMIT: SELF_COMMIT_CONTAINING_THIS_MANIFEST
BRANCH: review/fcop-4.0-wp4c.4-host-projection
PR_BASE: taskbook/fcop-4.0-wp4c.4-host-projection
PR_KIND: NEW_DRAFT
CONTENT_FILES: 16
MANIFEST_FILES: 1
TOTAL_DELIVERY_FILES: 17
LOCAL_VALIDATION: COMPLETE
REMOTE_READBACK: PENDING_POST_PUSH_EXTERNAL_RECEIPT
CI_STATUS: PENDING_FINAL_HEAD_INSPECTION
REMOTE_MAIN_BASELINE: 68dbeb15f4e7f84e1d03f907be9fa66c2265843e
WP4C_4_HOST_PROJECTION_ACCEPTED: false
REQUESTED_GATE_AFTER_REMOTE_VERIFICATION: WP4C_4_HOST_PROJECTION_ACCEPTED
WP4C_5_STARTED: false
MAIN_MERGE_AUTHORIZED: false
RELEASE_AUTHORIZED: false
```

[Fixed taskbook](https://github.com/joinwell52-AI/FCoP/blob/01c53355293c08f100b9f6e5aba0caea015d27cd/taskbooks/fcop-4.0/WP4C.4/01-Host-Projection-Adoption-Deployment-and-Rollback-Taskbook-v1.0.zh.md).
This Manifest is the second and only Manifest commit, directly after the Content Commit. Its own commit ID/hash is not embedded circularly. The post-push execution receipt on the new Draft PR binds the actual Manifest HEAD, this file's raw SHA-256, all 17 delivery files and remote checks. Old PR #24 remains historical and is not repurposed. This is execution evidence, not an ADMIN Gate signature.

## Content Commit raw byte identities

All rows refer to complete Git Blob bytes in 90fd061e82d82ec5639a70c7964fdd5d24191886, not rendered Markdown or normalized downloads.

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| CHANGELOG.md | 131093 | 0326873c6e2bc1d35698c14c2517539a1503ab4a5915c18eb2295eab77f5ff03 |
| reports/FCOP-4.0-WP4C.4-ATOMICITY-AND-RECOVERY-PROOF.md | 8091 | 90479430b00d2f3216147d030e4f14d8fc30db85e905196461d42a6684fa3fab |
| reports/FCOP-4.0-WP4C.4-HOST-PROJECTION-MAPPING.md | 7568 | 67a58d163308658f1ba927c1af55169ecb204b5c341e14fa0205e25b45d31ae5 |
| reports/FCOP-4.0-WP4C.4-IMPLEMENTABILITY-PROOF.md | 18071 | 97f24cdb0238bbf48940b74734f753a28c397791bb651b980de0e36503ded5b8 |
| reports/FCOP-4.0-WP4C.4-RESULT.md | 19087 | ea5103a297211e36a567f92884b8897dc8731839b2e551f03acadb939b5181a5 |
| src/fcop/project.py | 266052 | e2235c970afad7774e3bcb0e2b864cce05e046ac37949b8450f4ca75afb14bfe |
| src/fcop/v4/rule_distribution/__init__.py | 4860 | fe8e0ef90a90cd542b519749639f4c2e41c5fe7fe06badd03414d23bf18a75a2 |
| src/fcop/v4/rule_distribution/_deployment.py | 27999 | 1d5b55bf59138141320ac83dcf9a600175403bccfd48675cd0425cf6d90feeca |
| src/fcop/v4/rule_distribution/_errors.py | 1043 | b6aff1437227cd5a606419945b9cd6233291354aea401d5040d302b2e7219b61 |
| src/fcop/v4/rule_distribution/_files.py | 4901 | 1729d56e50c56b7c4b946a339853652d8b00a1946619555d3df8c5215377bef3 |
| src/fcop/v4/rule_distribution/_profiles.py | 2811 | 53efa015d416767aa2ea9777ea99cac731e8fb3b5cdc8dd0aef120c2a27712c7 |
| src/fcop/v4/rule_distribution/_projection.py | 6287 | c093186376a0d7a5c653dad2b94c36c5cf4303454116d1beb73fce96efeac630 |
| src/fcop/v4/rule_distribution/_receipts.py | 15595 | 97d278dbe832277553604389c91e3d11197ca435c619372141e96f3a9dbd514f |
| src/fcop/v4/rule_distribution/_selection.py | 6635 | c7fc5e4c4e872e0444007530e1cb0e572bb68f19628933b974d939615ec1b869 |
| tests/test_fcop/test_v4_rule_distribution.py | 9602 | 51b522b47af9c4e8f0467de866345251c1d3c585bad929bd53d317b8c6767f8f |
| tests/test_fcop/test_v4_rule_distribution_host.py | 15698 | 3aba58d80b521481eff48e50558f7976a83ecaae7a96bfc6ff6f35aa28fe5aed |

The Manifest-only commit adds reviews/fcop-4.0/wp4c.4/MANIFEST.md and changes none of these 16 files. Strict UTF-8, no BOM and LF were checked before content staging; staged Blob bytes matched local bytes. Five new private modules, one new unit-test file and four reports are the additions. No optional bundled Host Profile, package configuration, frozen snapshot or additional public facade was added.

## Final native verification

| Scope | Actual result |
| --- | --- |
| DIST-08–20 target IDs / nodes | 13/13 IDs; 53/53 passed |
| Prior WP4C.3 target nodes | 56/56 passed |
| Full FCoP | 1349/1349 passed; 1345.88s |
| Distribution units within FCoP | 93/93, including 52 new Host units |
| Frozen Core Conformance | 119/119 passed |
| MCP regression | 134/134 passed |
| Full Distribution | 144 passed / 32 expected future failures / 0 skipped |
| Remaining failures by owner | WP4C.5: 12; WP4C.6: 20; each node listed in RESULT |
| Meta/Static / DIST-30 control | 33/33 and 1/1 passed |
| Real two-process linearization | PASS, one distinct success identity |
| Three physical failure windows | 3/3 passed |
| Native process exit / interrupted rollback | PASS, included in new units |
| Ruff / mypy | PASS / PASS (51 source files) |
| Public-surface snapshot | 4/4, unchanged |
| Frozen protected raw Blobs | 159/159 unchanged |
| Project surface | 111 method names unchanged; only authorized facade body changed |
| Wheel and sdist raw member comparison | 30/30 each |
| Installed wheel smoke | PASS, isolated external target; 18 canonical artifacts |
| New runtime dependencies / background components | 0 / 0 |
| Core, frozen tests/contracts, Schema, MCP, CodeFlowMu changes | 0 |
| Runtime Host consumption | UNKNOWN |
| Native platform | Windows / Python 3.12.9 |
| Linux/macOS | NOT_NATIVE_VERIFIED |

Full Distribution returns exit 1 deliberately because later-owner behavior remains unimplemented; it is not reported as all-green. The 32 exact future red nodes and intermediate implementation failures are preserved in RESULT. None is a WP4C.4 or previously accepted obligation. No skip, xfail, frozen test edit, error-message guessing or success-result patch was used to hide a failure.

### Final test evidence

External JUnit files are retained under C:/Users/Administrator/AppData/Local/Temp. They are not extra delivery files or a new authoritative state store.

| File | Raw SHA-256 |
| --- | --- |
| fcop-wp4c4-fcop-delivery.xml | 27658485005e39fd65927c1b590a7f6ba996ce5364b7013ef98d5d5583753439 |
| fcop-wp4c4-core-mcp-delivery.xml | 81dba77bf3ea26859f94b6fc3149311eb7be15676720990c7f6fd4799eb72d7d |
| fcop-wp4c4-dist-delivery.xml | 98ca2b0bce1cda2a5268618f71a94ba54009c1abc10713c38312120c1be0ce21 |
| fcop-wp4c4-surface-verified.xml | 2e013805962b67d7b84b69defe840c2226ebce6b7d547d115edab2e886dbb82b |

### Unpublished local build evidence

- fcop-3.2.5-py3-none-any.whl: 286f022ec66b3829860a638bcdc7f303e7933bfa30c4fac087ed1ca8b1796c55
- fcop-3.2.5.tar.gz: e4823f2e4179b857ef5bbd95af90f7cde37accd8bfa2f889b23a2de6830a42e6
- Canonical Manifest remains: 7efb1ba14df4d1ffbe164b8ec85dbf4316e7da4c0f367f3a506c78e4e29862d4

Both artifacts reside only in the external fcop-wp4c4-build-delivery Temp directory. Wheel installation used --no-index --no-deps in an external target. No release, package upload, actual Host redeploy or original workspace migration was performed.

## Required post-push external receipt

Read the exact Manifest HEAD back from GitHub, verify its direct parent Content Commit and that commit's direct parent taskbook, verify per-commit file sets 16/1, all 17 remote complete bytes/size/SHA-256 against local Blobs, and compare a new detached LF checkout. Recheck clean worktrees, unchanged remote main and the new Draft PR's base/head.

Inspect real Actions runs, check runs, commit statuses and PR statusCheckRollup at that fixed HEAD. Current workflows filter pushes to main/feat and PRs to main; if no checks trigger for this required review/taskbook pair, report NOT_TRIGGERED_BRANCH_FILTER, never PASS. Do not edit workflow, retarget main or use old taskbook CI as implementation evidence.

After those checks, publish the actual completion receipt on the new PR and stop, requesting only WP4C_4_HOST_PROJECTION_ACCEPTED. No WP4C.5 execution, merge, auto-merge, reviewer request or release is authorized.
