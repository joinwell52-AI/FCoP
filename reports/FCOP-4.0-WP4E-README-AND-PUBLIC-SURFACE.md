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

