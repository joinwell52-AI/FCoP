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

# WP4E bilingual public entry closeout

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

## Corrected public contract description

Both READMEs now distinguish latest stable 3.2.5 from unpublished 4.0.0rc1.
They explain protocol-level Major changes, Core versus MCP Adapter ownership,
C1–C8 versus the historical seven architecture concepts, and the actual 46/12/4 surface.

Existing 45 tool names gain routing and v4 semantics. T6 reopen_task is the one
additional name, not the sole new capability and not a Branch-specific tool.
Concurrency is a shared write contract; misleading blanket “no locks” and
“actor/name itself authorizes” descriptions were removed from the current entry.
Historical protocol files and essays remain unchanged and linked through history.

## Installation and examples

Candidate commands install exact local artifacts into a fresh environment, not an
unpublished PyPI version. Stable commands pin both packages to 3.2.5. Mixed pairs and
automatic workspace migration are explicitly excluded. Windows executable paths are
separated from POSIX paths. The Python snippet creates a temporary workspace, performs
two identical create requests, and asserts one task with an Existing result.
MCP initialization examples explicitly request protocol_version 4.0.

The two language files have identical code fences and link targets. The new regression
test verifies both, checks local targets and executes the Python snippet.
Legacy install-prompt links and fcop://prompt/install were accidentally omitted in
the first edit; restored without changing the existing tests or prompt bytes.

## Other public surfaces

- docs/mcp-tools.md: capability map first, legacy 3.x tables explicitly marked historical.
- docs/index.html: bilingual stable/RC distinction and Major capabilities; retains the
  existing page structure, historical articles and language switching.
- mcp/README.md: WP4E accepted-artifact identity and 45-plus-T6 semantics; embedded
  legacy prompt stays unchanged.
- docs/fcop-4.0/rc-candidate-guide.md: explicit isolated artifact installation.
- docs/fcop-4.0/rc-candidate-release-controls.md: fail-closed publication boundary.

No public documentation claims a stable 4.0 release, new DOI or Registry publication.

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

### Additional public-entry checks

A read-only local-link walk across both READMEs, MCP reference/README and the two RC
guides resolved 55/55 local links. The committed parity test verifies the two README
code fences and link targets exactly; the Python example executed successfully.
The content-head 24 installed origins execute the candidate commands and actual
MCP stdio examples; no unpublished PyPI install is represented as successful.
