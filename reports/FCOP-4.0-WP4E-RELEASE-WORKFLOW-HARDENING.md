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

# WP4E release workflow hardening

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

## Default deny

release.yml now has manual dispatch only; a pushed tag cannot automatically publish.
Its default mode is dry-run. It downloads a supplied accepted artifact run and checks
the exact Manifest/head/content/four hashes, performs no build and uses no PyPI secret.
RC and stable are not interchangeable: this task permits only 4.0.0rc1, tag v4.0.0rc1,
and GitHub Pre-release; stable publication fails the validation.

## Publication control prepared, not exercised

A future publish-preflight requires an OWNER-authored structured signed release-ready
Gate plus explicit Phase B/tag/PyPI/GitHub Release grants. The earlier RC-accepted Gate
does not satisfy it. The grant binds repository, accepted head, content commit, exact
artifact run, Manifest SHA and all four artifacts. All three final-head workflows
and both actual PR-only jobs must have run successfully.

Before entering the publish job, the guard verifies that the pre-existing fcop-pypi
environment has independent required reviewers, self-review prevention and a deployment
branch policy. Currently only github-pages exists; this task does not create remote
permission configuration. Missing publishing protection fails closed before starting
a job that could auto-create an unprotected environment. Phase B ADMIN setup is required.

Global permissions are contents/actions read. Contents write and project-scoped PyPI
secrets exist only in the protected, separately authorized publish job.
After environment approval, all bindings are rechecked. The exact accepted artifacts
are uploaded without rebuild or skip-existing. The existing tag must resolve to the
accepted commit. Public PyPI is freshly read back (4 hashes), followed by clean
installation and installed identity verification, then --verify-tag --prerelease.
No Phase A invocation uses this path.

## Repair provenance

The old MCP PR-only CHANGELOG extraction selected the opening heading as its own
closing boundary. It now uses the same explicit start/next-heading interval pattern
as the Core check, without changing CHANGELOG or reducing the requirement.
Both PR-only jobs actually ran and passed at preliminary implementation HEAD.
A separate final-head run remains mandatory.

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

### Executed workflow evidence

[Actual release.yml dry-run 34427777738](https://github.com/joinwell52-AI/FCoP/actions/runs/34427777738)
verified the real content-head artifact set with no PyPI secrets. Verification succeeded;
publish was intentionally not applicable. No tag, environment, release or publication
was created. Unit tests exercise fabricated authority fixtures only and are not ADMIN grants.
