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

# WP4E integration and preserved history

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

## Worktree and ancestry

- New independent worktree: `D:/FCoP-wp4e-release-readiness`.
- Review branch: `codex/fcop-4.0-wp4e-release-readiness`.
- Original D:/FCoP worktree and all historical worktrees remain in place. Existing dirty
  files, untracked materials and dogfood are not cleared or upgraded.
- GitHub compare of main against the accepted parent: ahead 165 / behind 0 at preflight.
  This is an ancestry observation, not main mutation or a merge authorization.
- Pasted authorization section 1 contained a malformed 41-character ref. Its section 2,
  fixed Manifest URL and signed Gate agree on the valid 40-character ref used above.
  The original text and correction are both preserved in the committed taskbook.
- Taskbook commit precedes content. Content changes and their repairs retain parentage;
  no squash, history rewrite or force-push is used.

## Production boundary

`python -B scripts/wp4e_verify_scope.py` compares Git trees for src, mcp/src, spec and
tests/conformance with the accepted WP4D parent. All must be identical.
It also verifies on-disk LF bytes for 19 canonical rule files plus 2 frozen specs.
This is stricter than a statement that code “looks unchanged.”
No new public production API, dependency, runtime or state machine is introduced.

## Downstream independence

CodeFlowMu currently adopts versions below FCoP 4.0 and is outside WP4E.
No live shadow scan, coordination, quiet window, migration or write is performed.
The previous WP4D quiet-window misunderstanding is not inherited as a prerequisite.

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

### Content-head remote proof

`python -B scripts/wp4e_remote_readback.py 18f8d1ba3d0744bc4501e347312c3f97e2a4fede` returned
29/29 identical raw GitHub/local Git blobs and verified ancestry from the accepted parent.
The committed JSON includes each path, bytes, Git blob and SHA-256. Final evidence and
Manifest files require a new whole-delivery readback after their push; 29/29 is not
misreported as the final file count.
