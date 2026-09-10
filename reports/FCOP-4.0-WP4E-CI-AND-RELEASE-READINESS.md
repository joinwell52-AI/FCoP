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

# WP4E CI and release readiness

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

## Acceptance matrix

Final HEAD requires: Windows and Ubuntu full regression with zero failures/errors/skips,
all applicable Core and MCP matrix/package jobs, both actual PR-only checks, RC source
parity, 12 installed consumers / 24 origins, 4 reproducible artifacts, 19 canonical and
21 authoritative identities, README parity/executable snippets, release dry-run and
all delivered GitHub blob hashes. An earlier taskbook-only or implementation run cannot
be reused as a final-head CI claim.

## Known intermediate runs

| Head | Workflow | Result at this report revision |
|---|---|---|
| 208ebb12e33518e7909dbcf4f6d0ad6c72c7e584 | 34426442905 RC | artifact-attribution failed; later cancelled by follow-up push |
| 208ebb12e33518e7909dbcf4f6d0ad6c72c7e584 | 34426442875 Core / 34426442874 MCP | both PR-only checks passed; full runs superseded/cancelled |
| 0b0da39d360952909305e0e20f4aad37cd8f8078 | 34426611345 RC | 15/15 jobs succeeded, including both full source platforms and 12 consumers |
| 0b0da39d360952909305e0e20f4aad37cd8f8078 | 34426611368 MCP | succeeded |
| 0b0da39d360952909305e0e20f4aad37cd8f8078 | 34426611357 Core | final observation pending |

Jobs use the actual pull-request head rather than the synthetic merge checkout.
The PR still targets main so both existing PR-only checks execute with their original
snapshot/change-log requirements. Final aggregate counts and time-stamped evidence
will be appended after the last HEAD is verified.

## Local commands

- pytest test_install_prompt.py + initial WP4E tests: 46 passed, 0 failures; 109.46s.
- pytest -k metadata/readme after UTF-8 repair: 7 passed, 40 deselected (targeted, not full).
- Final six CI-guard cases + metadata case: 7 passed, 35 deselected; 0.09s.
- Full source parity command: python -B scripts/wp4d_source.py; returned SOURCE_ONLY
  Python and MCP success, the latter 24 transitions / 3 server processes / 2 real racers.
- Initial local full suite is preserved separately; its two missing-prompt-link failures
  are not relabeled as passing. Final new-head regressions are required.

Local timestamps not captured by an individual earlier command are not invented.
Final CI API started/completed times and JUnit counts provide the full auditable timing.

