---
protocol: fcop
version: '4.0'
sender: ME
recipient: ADMIN
stage: WP4E_PHASE_A
taskbook_commit: 793b5eef808cecc55437c8c2dc43e737b56b1300
baseline: 64a24295d6c1fa53a182a819d39b295c2ba8d2d0
status: CONTENT_VERIFIED_FINAL_RECEIPT_REQUIRED
---

# WP4E Phase A result

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

## Current truthful status

Final HEAD verification is pending; no completion Gate is requested by this report yet.
Documentation, verifier, MCP sample and workflow repairs remain within Phase A.
The final Manifest and a subsequent remote verification receipt will bind actual
HEAD, all Actions runs, command results and every delivered file hash.

## Preserved intermediate failures

1. Root READMEs omitted legacy install-prompt links; existing two assertions failed.
   Restore both links plus the historical URI and explicit legacy-only scope.
   Do not edit, remove or weaken the tests.
2. New artifact-delta check decoded email payload as replacement-character text.
   Strict decoded UTF-8 preserves real Chinese bytes and matches authorized README;
   headers/member identities remain required. Repair commit 0b0da39 retains the failure.
3. Old MCP PR-only awk interval bug was found during review and fixed at the workflow
   extraction statement, not by changing CHANGELOG or omitting the job.

## Phase B proposal, not execution

After ADMIN accepts FCOP_4_RC_RELEASE_READY, obtain explicit approval for each intended
irreversible action, confirm protected publishing environment and credentials, preserve
the accepted ancestry while integrating main, create the exact authorized tag, upload
the accepted four artifacts without rebuilding, verify public PyPI bytes and fresh
installation, and create an RC Pre-release. Do not update MCP Registry/Zenodo or publish
stable without their own authorization. A partially published set is irreversible and
must be reported, not erased or disguised.

```yaml
REQUESTED_GATE_AFTER_COMPLETE: FCOP_4_RC_RELEASE_READY
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

## Content verification closeout (not a self-signed Gate)

Fixed candidate content: `18f8d1ba3d0744bc4501e347312c3f97e2a4fede`.
Evidence observed at 2026-09-10T02:07:22.060075+00:00.
[Machine evidence](../tests/rc/evidence/wp4e/content-verification.json) retains
GitHub job/step timestamps, JUnit counts/hashes, every consumer result, build metadata,
dry-run result, 21 authoritative hashes and the 29/29 content-commit blob readback.

Windows and Ubuntu each passed 1973/1973 (1519 FCoP, 159 MCP, 295 frozen Conformance),
including 42/42 new WP4E tests; zero failures/errors/skips. 44/44 CI jobs and 2/2 actual
PR-only gates passed. Twelve consumers and 24 wheel/sdist origins passed the installed
MCP-only 24-transition / two-Branch / two-real-writer / three-process proof.
The separate release workflow dry-run passed its verification job; its publish job was
not applicable and was NOT counted as a passing job. Thus 45 applicable successful jobs.

Only the subsequent evidence and Manifest commits remain outside this verified content.
The executor must re-run all CI and release dry-run on the Manifest commit, read back all
final files, and post a fixed-head completion receipt on [PR #33](https://github.com/joinwell52-AI/FCoP/pull/33).
That later receipt is mandatory: these content-head results alone do not finish Phase A.
No source, test, example, workflow or README may be changed in the evidence suffix.

### Content-stage receipt

```yaml
CONTENT_STATUS: VERIFIED
CANDIDATE_CONTENT: 18f8d1ba3d0744bc4501e347312c3f97e2a4fede
README_BILINGUAL_PARITY: PASS
MCP_DISCOVERY: 46/12/4
MCP_BRANCHES: 2
MCP_REAL_CONCURRENT_WRITERS: 2
MCP_PERSISTED_TRANSITIONS: 24
WINDOWS_FULL: 1973/1973
UBUNTU_FULL: 1973/1973
WP4E_NEW_TESTS: 42/42
UNEXPECTED_FAILURES: 0
SKIPPED_TESTS: 0
CI_JOBS: 44/44
PR_ONLY: 2/2
CONSUMERS: 12/12
INSTALLED_ORIGINS: 24/24
RAW_REPRODUCIBILITY: 4/4
CANONICAL_IDENTITIES: 19/19
AUTHORITATIVE_IDENTITIES: 21/21
CONTENT_REMOTE_HASHES: 29/29
RELEASE_WORKFLOW_DRY_RUN: PASS
UPLOADS_EXECUTED: 0
FINAL_MANIFEST_HEAD_RECEIPT: REQUIRED_AFTER_FINAL_CI
FCOP_4_RC_RELEASE_READY: NOT_SIGNED
```

This file deliberately does not claim its own future commit SHA, final-head CI results
or self hash. The final Manifest commit and a subsequent fixed-head remote completion
receipt supply those identities without another self-referential evidence loop.
