---
protocol: fcop
version: '4.0'
sender: ME
recipient: ADMIN
stage: WP4E_PHASE_A
status: CONTENT_VERIFIED_FINAL_HEAD_RECHECK_REQUIRED
---

# WP4E RC integration and release readiness — delivery Manifest

## Fixed identity and authority

| Field | Value |
|---|---|
| Repository | joinwell52-AI/FCoP |
| Baseline / signed WP4D acceptance | 64a24295d6c1fa53a182a819d39b295c2ba8d2d0 |
| WP4D candidate content | d1a86f32d87f000fe0aec444563decdc892dc142 |
| WP4D Manifest SHA-256 | 21728890f757189cbc47e3ac131efcfb37d5ea0935de2b7467575de95f95314d |
| Taskbook commit | 793b5eef808cecc55437c8c2dc43e737b56b1300 |
| Taskbook bytes / SHA-256 | 13138 / 05e39d231950917e56fef6cf63c9ee081316356058115a4942c47dffe3678bbc |
| Candidate content commit | 18f8d1ba3d0744bc4501e347312c3f97e2a4fede |
| Evidence commit / immediate parent of this Manifest | 7e22bd3c4bd47fdef347e57c7545693d8888ca99 |
| Execution HEAD | the single-parent, Manifest-only commit containing this file; fixed SHA in subsequent executor receipt |
| Branch | codex/fcop-4.0-wp4e-release-readiness |
| Independent worktree | D:/FCoP-wp4e-release-readiness |
| Draft PR / base | [#33](https://github.com/joinwell52-AI/FCoP/pull/33) / main |
| Only requested completion Gate | FCOP_4_RC_RELEASE_READY |

[WP4D OWNER Gate](https://github.com/joinwell52-AI/FCoP/pull/31#issuecomment-5610960987).
The taskbook preserves the pasted malformed reference and identifies its valid value
from section 2, the fixed Manifest URL and the signed Gate. No history was rewritten.
Seven reports and raw machine evidence are indexed in the file table below.

## Artifact SHA-256 lock for WP4E (not WP4D)

Both distributions are exactly 4.0.0rc1. Latest stable remains 3.2.5.
No release, main merge, tag, PyPI upload, Registry or Zenodo update has occurred.

| Artifact | Bytes | Required SHA-256 |
|---|---|---|
| fcop-4.0.0rc1-py3-none-any.whl | 726280 | b539fdd496d52ea608b5f42abd270c2ed04e8f011242d932ddedac48f8d7cee9 |
| fcop-4.0.0rc1.tar.gz | 616894 | 1e1dc76f46f2e5b5875153f83552155784ac0fadab4cec37bdf43c1a7cc22a5e |
| fcop_mcp-4.0.0rc1-py3-none-any.whl | 117968 | 53ca18feee98f37992764748d4faa8ac1811330d7c3229ad3ed312ff3bb2736e |
| fcop_mcp-4.0.0rc1.tar.gz | 109449 | a77729d8718909db47b8c08c310688a015d20f1e91a88051e88e4ae5c3c52de9 |

Two fresh content exports built independently: 4/4 raw byte equality; two sets of
four successful Twine checks. Tools: build 1.4.2, hatchling 1.32.0,
setuptools 82.0.1, wheel 0.45.1, twine 7.0.0, packaging 26.3;
SOURCE_DATE_EPOCH=1788940367.
Core wheel is unchanged. Core sdist changes only root bilingual READMEs.
MCP wheel/sdist change only authorized README long-description metadata and RECORD.
No archive production member, metadata header, version or dependency changed.

Content verification machine Manifest: run 34427606888,
SHA-256 8688692fe2c55c0825897f13bf3192afa884f1099a5bb4fe328baf9506bf4bf8.
This is the content-run identity, not an invented future final-head run identity.
Final HEAD must build the same four locked bytes and generate its own execution-head/
run-bound candidate-manifest.json. The executor's post-CI receipt must supply that
machine Manifest SHA and run ID. Later publishing is allowed to consume only the
exact run and hashes that ADMIN explicitly accepts, without rebuilding at upload.

## Executed content verification

| Check | Observed result |
|---|---|
| Windows / Ubuntu full regression | each 1973/1973; 0 failures/errors/skips |
| New WP4E tests | 42/42 |
| Actual CI jobs | 44/44 |
| Actual PR-only checks | 2/2 |
| Independent release.yml dry-run | verification passed; publish job NOT APPLICABLE |
| Installed consumers / origins | 12/12 / 24/24 |
| MCP discovery | 46 tools / 12 resources / 4 templates |
| MCP-only proof per installed origin | T2–T7, Root + 2 Branches, convergence, 24 transitions, 2 real competing writers, 3 server processes |
| Canonical / authoritative identities | 19/19 / 21/21 |
| Core, MCP, spec, frozen Conformance Git trees | unchanged from accepted WP4D |
| README code/link bilingual parity | PASS; 55 public local links resolved |
| Content-commit GitHub blob readback | 29/29 |

Runs: [Core](https://github.com/joinwell52-AI/FCoP/actions/runs/34427606898),
[MCP](https://github.com/joinwell52-AI/FCoP/actions/runs/34427606981),
[RC](https://github.com/joinwell52-AI/FCoP/actions/runs/34427606888),
[release dry-run](https://github.com/joinwell52-AI/FCoP/actions/runs/34427777738).
Detailed commands, job/step start/end UTC, exit interpretation, JUnit counts,
consumer provenance and intermediate failures are preserved in the reports and
[content-verification.json](../../../tests/rc/evidence/wp4e/content-verification.json).

## Delivered files (30 before this Manifest, 31 including it)

SHA-256 values below cover raw Git blobs at evidence commit
7e22bd3c4bd47fdef347e57c7545693d8888ca99, not Windows checkout normalization.
This Manifest cannot contain its own future commit or self hash; its SHA-256 and
the final 31/31 remote readback are supplied by the subsequent fixed-head receipt.

| Path | Bytes | SHA-256 |
|---|---|---|
| [.github/workflows/rc-candidate.yml](https://github.com/joinwell52-AI/FCoP/blob/7e22bd3c4bd47fdef347e57c7545693d8888ca99/.github/workflows/rc-candidate.yml) | 6571 | c4d7d15eea13eb4cbeb98d45dbed227b3101701ed17a5c5c7a257efb453f0fcf |
| [.github/workflows/release.yml](https://github.com/joinwell52-AI/FCoP/blob/7e22bd3c4bd47fdef347e57c7545693d8888ca99/.github/workflows/release.yml) | 5157 | 1fc2d15cb417878990a92576e0353c085a58f801a7d4a849f5a0770dfc708420 |
| [.github/workflows/test-fcop-mcp.yml](https://github.com/joinwell52-AI/FCoP/blob/7e22bd3c4bd47fdef347e57c7545693d8888ca99/.github/workflows/test-fcop-mcp.yml) | 9406 | 0959916c72fc7908736a9214804d033e738c45e8af6cb56678cecff09ed51258 |
| [.github/workflows/test-fcop.yml](https://github.com/joinwell52-AI/FCoP/blob/7e22bd3c4bd47fdef347e57c7545693d8888ca99/.github/workflows/test-fcop.yml) | 13089 | ecf03e6076e3f3f13598d63bc3fab1d248766192cbd412bfdbfdc4fdd1b02c31 |
| [README.md](https://github.com/joinwell52-AI/FCoP/blob/7e22bd3c4bd47fdef347e57c7545693d8888ca99/README.md) | 7233 | 7863666f024c8a3450cc113daf60aafc82d4f0d1f2fbe0570398fc053acf87c0 |
| [README.zh.md](https://github.com/joinwell52-AI/FCoP/blob/7e22bd3c4bd47fdef347e57c7545693d8888ca99/README.zh.md) | 6777 | 58ce1ecd50e3265f1a1e6c3d54f1de9bcdd8a47ecf1a6bb54cb188d0d697c78b |
| [docs/fcop-4.0/rc-candidate-guide.md](https://github.com/joinwell52-AI/FCoP/blob/7e22bd3c4bd47fdef347e57c7545693d8888ca99/docs/fcop-4.0/rc-candidate-guide.md) | 2807 | b683dc2c628870c92fc9fbcd63e60d5527629eef8ce797e6624333e9757f98b0 |
| [docs/fcop-4.0/rc-candidate-release-controls.md](https://github.com/joinwell52-AI/FCoP/blob/7e22bd3c4bd47fdef347e57c7545693d8888ca99/docs/fcop-4.0/rc-candidate-release-controls.md) | 2804 | 503746c8a70b45c3ab358a573fa0a2b4b343f7509fb981cea32646293dc74710 |
| [docs/index.html](https://github.com/joinwell52-AI/FCoP/blob/7e22bd3c4bd47fdef347e57c7545693d8888ca99/docs/index.html) | 72937 | caefd64369134d3e3e59936cc1f6b58b84f7dca352a2bb7e460029ba5881af4e |
| [docs/mcp-tools.md](https://github.com/joinwell52-AI/FCoP/blob/7e22bd3c4bd47fdef347e57c7545693d8888ca99/docs/mcp-tools.md) | 20380 | 48e8349e814e2f84ad3e1bc5b7fd4a804cad3c75772aa68f2d8694663b884999 |
| [examples/v4/third-party/mcp-only/client.py](https://github.com/joinwell52-AI/FCoP/blob/7e22bd3c4bd47fdef347e57c7545693d8888ca99/examples/v4/third-party/mcp-only/client.py) | 13686 | 83d26af6474ab50f65c46d9dd98097a237cae60f34d1d04254d83c26acc4741a |
| [mcp/README.md](https://github.com/joinwell52-AI/FCoP/blob/7e22bd3c4bd47fdef347e57c7545693d8888ca99/mcp/README.md) | 16003 | c02b5e97cff15f7670e5c3eb7f42e80e031ea7607906d8796a21af620a9b79ae |
| [reports/FCOP-4.0-WP4E-ARTIFACT-AND-DRY-RUN.md](https://github.com/joinwell52-AI/FCoP/blob/7e22bd3c4bd47fdef347e57c7545693d8888ca99/reports/FCOP-4.0-WP4E-ARTIFACT-AND-DRY-RUN.md) | 6232 | a674a2431dd34dd0c589863e9d393573780cd1c916b1894ca5b1a5a244f054d2 |
| [reports/FCOP-4.0-WP4E-CI-AND-RELEASE-READINESS.md](https://github.com/joinwell52-AI/FCoP/blob/7e22bd3c4bd47fdef347e57c7545693d8888ca99/reports/FCOP-4.0-WP4E-CI-AND-RELEASE-READINESS.md) | 8301 | bb4cb2da6bdb4028887c8ae6b7b579541fa9b713e8420a18e50d17401237aaf9 |
| [reports/FCOP-4.0-WP4E-INTEGRATION-AND-HISTORY.md](https://github.com/joinwell52-AI/FCoP/blob/7e22bd3c4bd47fdef347e57c7545693d8888ca99/reports/FCOP-4.0-WP4E-INTEGRATION-AND-HISTORY.md) | 4458 | 80c2e8303cbeb9f9b43734bd1d258c2be28bf3d03079a86316546a785d872d01 |
| [reports/FCOP-4.0-WP4E-MCP-CAPABILITY-MAPPING.md](https://github.com/joinwell52-AI/FCoP/blob/7e22bd3c4bd47fdef347e57c7545693d8888ca99/reports/FCOP-4.0-WP4E-MCP-CAPABILITY-MAPPING.md) | 6178 | 50958279da0fceebcdc9464f01fc5b27eb6e4ed2d611b1da1310f6c1cf2826c4 |
| [reports/FCOP-4.0-WP4E-README-AND-PUBLIC-SURFACE.md](https://github.com/joinwell52-AI/FCoP/blob/7e22bd3c4bd47fdef347e57c7545693d8888ca99/reports/FCOP-4.0-WP4E-README-AND-PUBLIC-SURFACE.md) | 5098 | 5f84d8d823e6c06f3d1ef84046c44232e0c41e59da1f62f2f1a89078ac64b04d |
| [reports/FCOP-4.0-WP4E-RELEASE-WORKFLOW-HARDENING.md](https://github.com/joinwell52-AI/FCoP/blob/7e22bd3c4bd47fdef347e57c7545693d8888ca99/reports/FCOP-4.0-WP4E-RELEASE-WORKFLOW-HARDENING.md) | 5104 | 6a9d5b31032a9d9ae185f9c90999542560a3b4bc0e3d4d8554550adf3c64e34a |
| [reports/FCOP-4.0-WP4E-RESULT.md](https://github.com/joinwell52-AI/FCoP/blob/7e22bd3c4bd47fdef347e57c7545693d8888ca99/reports/FCOP-4.0-WP4E-RESULT.md) | 5351 | 61cba259818547336a039bbf9f1d144991f3c2abe87f2d57e0dbc3fa0de707f2 |
| [scripts/wp4d_build.py](https://github.com/joinwell52-AI/FCoP/blob/7e22bd3c4bd47fdef347e57c7545693d8888ca99/scripts/wp4d_build.py) | 7135 | 8367e7e7e9bafa3874e2c29ffe9b78ee9840c53faa2bfd0de6c5303cc86ece06 |
| [scripts/wp4d_candidate_ref.py](https://github.com/joinwell52-AI/FCoP/blob/7e22bd3c4bd47fdef347e57c7545693d8888ca99/scripts/wp4d_candidate_ref.py) | 1172 | a359fa48aada8b60d01007aed800e538cbe647d986fb59b82c3d32afad81d6a9 |
| [scripts/wp4d_consume.py](https://github.com/joinwell52-AI/FCoP/blob/7e22bd3c4bd47fdef347e57c7545693d8888ca99/scripts/wp4d_consume.py) | 9352 | 0e0864d5f44d5d9d147bcedf0b27f9bd4076445cf3352ea5e043df599f50444d |
| [scripts/wp4e_artifact_delta.py](https://github.com/joinwell52-AI/FCoP/blob/7e22bd3c4bd47fdef347e57c7545693d8888ca99/scripts/wp4e_artifact_delta.py) | 2775 | b580a441c44061f8c165199abf14791ffda7800bb2259beb9440a6298371c399 |
| [scripts/wp4e_public_reinstall.py](https://github.com/joinwell52-AI/FCoP/blob/7e22bd3c4bd47fdef347e57c7545693d8888ca99/scripts/wp4e_public_reinstall.py) | 2067 | 83a946b4522e0b7af83ffc164dfb75f20ee9a6d6691f32144eca17b4707c7808 |
| [scripts/wp4e_release_guard.py](https://github.com/joinwell52-AI/FCoP/blob/7e22bd3c4bd47fdef347e57c7545693d8888ca99/scripts/wp4e_release_guard.py) | 6983 | 1cd33aeb1a78ad919f13fac1b9888562dfb5f6853bf14ed43ed66ffced544828 |
| [scripts/wp4e_remote_readback.py](https://github.com/joinwell52-AI/FCoP/blob/7e22bd3c4bd47fdef347e57c7545693d8888ca99/scripts/wp4e_remote_readback.py) | 1815 | 7f60e7b515d9963fc4abe55eccf41639b9aada2deac6791db37a553e272eaac5 |
| [scripts/wp4e_verify_scope.py](https://github.com/joinwell52-AI/FCoP/blob/7e22bd3c4bd47fdef347e57c7545693d8888ca99/scripts/wp4e_verify_scope.py) | 2204 | e650ad03a6ab9d0d1befa5cfb5c4b9c170f688f22fb7befcd583bcdd40e43a7a |
| [taskbooks/fcop-4.0/WP4E/01-RC-Integration-Public-Docs-and-Release-Readiness-Taskbook-v1.0.zh.md](https://github.com/joinwell52-AI/FCoP/blob/7e22bd3c4bd47fdef347e57c7545693d8888ca99/taskbooks/fcop-4.0/WP4E/01-RC-Integration-Public-Docs-and-Release-Readiness-Taskbook-v1.0.zh.md) | 13138 | 05e39d231950917e56fef6cf63c9ee081316356058115a4942c47dffe3678bbc |
| [tests/rc/evidence/wp4e/content-verification.json](https://github.com/joinwell52-AI/FCoP/blob/7e22bd3c4bd47fdef347e57c7545693d8888ca99/tests/rc/evidence/wp4e/content-verification.json) | 271221 | bfae29026911383e1b0bb553ec49159065bc0a2fa4d56bcfd02d57324ee6efb5 |
| [tests/test_fcop/test_wp4e_release_readiness.py](https://github.com/joinwell52-AI/FCoP/blob/7e22bd3c4bd47fdef347e57c7545693d8888ca99/tests/test_fcop/test_wp4e_release_readiness.py) | 9967 | 7341889038b07be888da4c97e0b7ac0172e9a63e0e52fdcbdc66d118fd566416 |

## Mandatory final-HEAD verification and stop

After this Manifest-only commit is pushed, run all three CI workflows on this exact
HEAD (not a synthetic PR merge or a taskbook-only head), including both PR-only checks.
Run release.yml only in dry-run mode with this HEAD's real artifact run and machine
Manifest hash. Read GitHub's branch HEAD and every delivered blob back, compare all
31 SHA-256 values and verify parentage. Post one executor completion receipt on PR #33
with exact HEAD, all Actions URLs/counts, final machine Manifest hash, this Manifest
hash, artifact hashes and whole-delivery readback. Do not change code to hide a failure.

The receipt must not treat the deliberately inapplicable publish job as passing.
A missing publishing environment remains a Phase B setup prerequisite, not a reason
to bypass protection or create credentials during Phase A.

After all final-head checks actually pass, stop and request only:

```yaml
WP4E_PHASE_A_STATUS: COMPLETE
REQUESTED_GATE: FCOP_4_RC_RELEASE_READY
MAIN_MERGE_AUTHORIZED: false
TAG_AUTHORIZED: false
PYPI_PUBLISH_AUTHORIZED: false
GITHUB_RELEASE_AUTHORIZED: false
MCP_REGISTRY_UPDATE_AUTHORIZED: false
ZENODO_UPDATE_AUTHORIZED: false
STABLE_RELEASE_AUTHORIZED: false
NEXT_STAGE_AUTHORIZED: false
CODEFLOWMU_ACCESSED: false
```

This is a conditional executor request template, not an ADMIN signature.
Phase B proposals: protected release-environment setup, ancestry-preserving main
integration, an explicitly authorized exact tag, upload of accepted original bytes,
public PyPI readback/reinstall and RC Pre-release. None is executed or authorized here.
