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

