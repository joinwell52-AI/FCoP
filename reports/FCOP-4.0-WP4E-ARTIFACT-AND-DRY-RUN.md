---
protocol: fcop
version: '4.0'
sender: ME
recipient: ADMIN
stage: WP4E_PHASE_A
taskbook_commit: 793b5eef808cecc55437c8c2dc43e737b56b1300
baseline: 64a24295d6c1fa53a182a819d39b295c2ba8d2d0
status: FINAL_HEAD_VERIFICATION_PENDING
---

# WP4E artifact identity and dry-run

## Evidence boundary

This is an executor report, not an ADMIN signature. The accepted WP4D parent is
`64a24295d6c1fa53a182a819d39b295c2ba8d2d0`, authenticated through
[OWNER Gate comment](https://github.com/joinwell52-AI/FCoP/pull/31#issuecomment-5610960987).
The remote Manifest was read as 34249 bytes with SHA-256
`21728890f757189cbc47e3ac131efcfb37d5ea0935de2b7467575de95f95314d`.
Taskbook: `793b5eef808cecc55437c8c2dc43e737b56b1300`, 13138 bytes, SHA-256
`05e39d231950917e56fef6cf63c9ee081316356058115a4942c47dffe3678bbc`.

Draft PR [#33](https://github.com/joinwell52-AI/FCoP/pull/33) targets main.
No main merge, tag, publication or CodeFlowMu operation is authorized or executed.
Final evidence/Manifest commits cannot substitute an earlier CI run for final HEAD CI.

## Rebuild identity, not reuse

Builds export the fixed WP4E content commit twice into distinct fresh directories.
A contiguous WP4E-only evidence/Manifest suffix can be excluded from content identity;
README, scripts, tests, examples and other-stage reports cannot be hidden.
The legacy WP4D resolver default remains covered by its six original tests.

Pinned tools: build 1.4.2, hatchling 1.32.0, setuptools 82.0.1, wheel 0.45.1,
twine 7.0.0, packaging 26.3. SOURCE_DATE_EPOCH=1788940367. Build on Ubuntu/Python 3.12.
Both sets run Twine against all four distributions, inspect exact metadata and the
dependency fcop>=4.0.0rc1,<4.1.0, and compare raw bytes, not normalized archives.

## Observed preliminary artifact delta (0b0da39)

| Artifact | SHA-256 | Changed archive members relative to WP4D |
|---|---|---|
| fcop-4.0.0rc1-py3-none-any.whl | b539fdd496d52ea608b5f42abd270c2ed04e8f011242d932ddedac48f8d7cee9 | none |
| fcop-4.0.0rc1.tar.gz | 1e1dc76f46f2e5b5875153f83552155784ac0fadab4cec37bdf43c1a7cc22a5e | README.md, README.zh.md |
| fcop_mcp-4.0.0rc1-py3-none-any.whl | 53ca18feee98f37992764748d4faa8ac1811330d7c3229ad3ed312ff3bb2736e | METADATA description and RECORD |
| fcop_mcp-4.0.0rc1.tar.gz | a77729d8718909db47b8c08c310688a015d20f1e91a88051e88e4ae5c3c52de9 | README.md, PKG-INFO description |

These are preliminary WP4E identities, not permission to publish and not yet a
substitute for the final HEAD manifest. No production archive member changed.
The metadata description is compared to the actual authorized MCP README; metadata
headers and archive member sets must remain identical.

## Real artifact verification

[RC run 34426611345](https://github.com/joinwell52-AI/FCoP/actions/runs/34426611345)
passed build reproducibility, member attribution, actual-artifact dry-run and 12 consumer
jobs. Each consumer separately installs wheel and sdist outside checkout.
Its preliminary machine Manifest SHA is
`64d475805d1f10f4439cc626b45f2780f6a7e5010ee5bb547f4338ece750dece`.
Dry-run output: upload_authorized=false, uploads_executed=0, releases_created=0.
Final content and final Manifest HEAD must repeat all checks.

The first attribution attempt failed because email's text payload view used replacement
characters for non-ASCII description bytes. Fixed by decoding get_payload(decode=True)
as strict UTF-8, retaining exact description/header comparisons and adding a negative
wrong-description test. This was a verification bug, not artifact non-reproducibility.

