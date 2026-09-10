---
protocol: fcop
version: "3.0"
sender: ME
recipient: ADMIN
subject: WP4F Stable promotion scope and compatibility audit
---

# WP4F scope and compatibility

## Authority and baseline

The user-authorized WP4F task is recorded in
`taskbooks/fcop-4.0/WP4F/01-Stable-Release-and-Local-MCP-Upgrade.zh.md`.
The independent review branch starts at main
`5208d8a2b37c969b0b2067c01107966bf705293c`; the published RC remains
`v4.0.0rc1` at `d5e851c3fa628167999a9f8b7b7b89290e7b8f06`.
This is a release-metadata promotion, not a protocol or implementation phase.

## Production delta

| File | Entire authorized change |
|---|---|
| `src/fcop/_version.py` | Package version `4.0.0rc1` to `4.0.0` |
| `mcp/src/fcop_mcp/_version.py` | Package version `4.0.0rc1` to `4.0.0` |
| `mcp/src/fcop_mcp/routing.py` | Register the exact `(4.0.0, 4.0.0)` package-version pair |

The compatibility check algorithm, version routing, handlers and protocol
operations are unchanged. The exact legacy `(3.2.5, 3.2.5)` and RC
`(4.0.0rc1, 4.0.0rc1)` pairs remain registered. Mixed Stable/RC and
Stable/3.2.5 pairs must still fail with `toolkit:MCP_PACKAGE_INCOMPATIBLE`.
`fcop-mcp` metadata requires `fcop>=4.0.0,<4.1.0`; both classifiers become
`Development Status :: 5 - Production/Stable`.

`scripts/wp4f_verify_scope.py` checks the full production tree against the
fixed main base. For the three files above it removes only the named version
assignment before comparing ASTs, and separately verifies its exact value.
All other production files must match, allowing only Git checkout CRLF/LF
materialization. It also verifies unchanged Git trees for `spec`, all
Conformance, both public/tool snapshot directories and `mcp/server.json`.
The 19 canonical rule-package files and both normative specifications are
additionally compared as raw bytes: 21/21.

## Historical release assertions

Two RC audit tests formerly assumed the current checkout was permanently RC:
`test_wp4d_rc_identity.py` and the historical README check in
`test_wp4e_release_readiness.py`. Their RC assertions are preserved and now
read seven original blobs from the published RC commit, stored in
`tests/stable/accepted-rc-fixture.json`. The canonical UTF-8/LF JSON container
hash is `d6c868d8e92015c11905db31ec4987ee3ffb52eb2e9beab6cdd763ce85e63fd3`.
Embedded source strings retain the original Git bytes. Only container line
endings are normalized on read, not embedded source text. Tampering is tested
and rejected. No frozen Conformance, prior behavioral assertions, skip or
xfail was changed.

The new Stable tests independently verify current 4.0.0 metadata, dependency,
documentation, content identity and release authorization. Five new runtime
package-pair nodes belong to `tests/test_fcop_mcp/test_wp4f_release_pairs.py`:
Core-only CI intentionally does not install MCP. Their inputs and assertions
were preserved when moved out of the Core suite after CI exposed that
test-placement mistake. This does not add an MCP runtime dependency to Core.

## Build-byte attribution

`scripts/wp4f_artifact_delta.py` compares every archive member to the four
published RC artifacts from run `34442779465`. New/removed unexplained
members and business-code changes are rejected. Permitted deltas are version
identities, the exact package-pair constant, package metadata, RECORD and
authorized documentation. Metadata description bytes must equal the correct
package README. Reproducibility and member-delta results are recorded in the
artifact report; they are not inferred from this source audit.

## Isolation

All work is in `D:/FCoP-wp4f-stable`, branch
`codex/fcop-4.0-wp4f-stable`, Draft PR #34. The original dirty `D:/FCoP`
checkout and dogfood files are not upgraded, cleaned or migrated. CodeFlowMu
is not a release dependency and receives no reads, writes, restart or quiet
window request. No Stable tag, main merge, registry submission, Zenodo
publication or live MCP upgrade belongs to Phase A.
