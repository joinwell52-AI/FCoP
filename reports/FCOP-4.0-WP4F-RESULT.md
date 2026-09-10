---
protocol: fcop
version: "3.0"
sender: ME
recipient: ADMIN
subject: WP4F Phase A Stable candidate delivery
---

# WP4F Phase A delivery

## Outcome and stage boundary

Stable candidate metadata, packaging, documentation, reproducible-build and
installed-consumer harnesses are implemented in the independent worktree.
There is no new protocol or tool business behavior. Phase B has not run:
no main merge, Stable tag, PyPI upload, formal Release or actual local MCP
upgrade. Published RC history is retained.

The sole requested next Gate after final-HEAD verification is
`FCOP_4_STABLE_RELEASE_READY`; the executor does not sign it. No observation
period or additional feature phase is introduced.

## Fixed identities

| Identity | Value |
|---|---|
| Repository | `joinwell52-AI/FCoP` |
| Base main | `5208d8a2b37c969b0b2067c01107966bf705293c` |
| Published RC tag / HEAD | `v4.0.0rc1` / `d5e851c3fa628167999a9f8b7b7b89290e7b8f06` |
| Stable candidate content | `1e1d309a6f8219ce9cf7fa2066b80f1a5103e499` |
| Independent worktree | `D:/FCoP-wp4f-stable` |
| Review branch | `codex/fcop-4.0-wp4f-stable` |
| Draft PR | [#34](https://github.com/joinwell52-AI/FCoP/pull/34) |
| Targets | `fcop==4.0.0`, `fcop-mcp==4.0.0`; future tag `v4.0.0` |

Content history is append-only: initial promotion `ad8f27e...`, historical
fixture byte handling `b567565...`, final documentation `5d4a690...`, MCP test
ownership `d5d53ea...`, strict test annotations `1e1d309...`.
The reports delivery commit follows content; the next commit changes only
`reviews/fcop-4.0/wp4f/MANIFEST.md`. Reports and Manifest do not silently change
the content used by the reproducible builder.

## Evidence already obtained when this report was written

- Local initial suite: 2057 passed. After eight additional release checks:
  2065 passed, zero failures/errors/skips, three existing deprecation warnings.
- Current Stable-specific tests: 71 passed, split into 66 Core/release nodes
  and five runtime MCP package-pair nodes. No test was deleted or skipped.
- Ruff: PASS across `src tests mcp/src`; Core mypy: 55 files PASS; MCP and its
  test suite strict mypy: 31 files PASS.
- Source scope audit: PASS; 21/21 authoritative raw-byte files preserved;
  frozen Conformance/Schema/public and tool snapshots unchanged.
- Pre-delivery candidate run
  [34451771814](https://github.com/joinwell52-AI/FCoP/actions/runs/34451771814):
  four raw-reproducible artifacts, two Twine checks, exact member attribution,
  no-upload dry-run, 12/12 installed consumers and 24/24 origins verified.
  Ubuntu full JUnit: 2065 tests, zero failures/errors/skips. Windows full
  source job was still running at this report's preparation checkpoint.
- Pre-delivery Core workflow
  [34451771800](https://github.com/joinwell52-AI/FCoP/actions/runs/34451771800):
  success, including cross-platform unit matrix, coverage, public-surface
  charter, clean-install packaging and dependency audit.

These are historical checkpoints, **not a claim that final review HEAD CI
already completed**. After the Manifest commit, the executor must re-run all
three workflows against that exact HEAD, read every job and downloaded result,
verify final four hashes and remote delivery blobs, then post a final binding
receipt on PR #34. That receipt supplies the final HEAD, final artifact run,
machine Manifest SHA-256 and full CI results without self-referentially
rewriting this report. A failed or pending final CI must never be called PASS.

## Intermediate failures retained and corrected

1. A literal historical RC identity assertion could not serve as the Stable
   checkout identity. Two historical audit tests now use exact published RC
   fixtures; their old assertions remain intact, and new tests cover Stable.
2. Windows may materialize the JSON fixture container as CRLF. The container
   hash is canonicalized on read while embedded original Git bytes remain
   unchanged; a tampered historical version is still rejected.
3. Core-only CI at
   [34451202273](https://github.com/joinwell52-AI/FCoP/actions/runs/34451202273)
   failed because five newly introduced MCP runtime tests were placed in the
   Core-only suite. They moved to the MCP suite with unchanged bodies and
   parametrization. No runtime dependency was added to Core.
4. MCP CI at
   [34451771798](https://github.com/joinwell52-AI/FCoP/actions/runs/34451771798)
   correctly required strict type annotations on those moved test functions.
   The two signatures were annotated; local strict mypy and all 71 release
   checks passed. Final HEAD CI must verify that correction remotely.
5. One local rerun initially named the nonexistent directory
   `tests/conformance/rule_distribution`; it collected no tests. The command
   was corrected to `tests/conformance/rule_distribution_v4`; that failed
   invocation is not counted as test evidence.

No failure was addressed by weakening behavior assertions, changing protocol,
adding skip/xfail, modifying workflow pass thresholds or pretending a failed
run passed. Superseded/cancelled runs remain historical records only.

## Report set and finalization

- `FCOP-4.0-WP4F-ARTIFACT-AND-CONSUMER.md`: four hashes, reproducibility,
  archive-member attribution and actual installed scenario evidence.
- `FCOP-4.0-WP4F-SCOPE-AND-COMPATIBILITY.md`: exact change boundary and history.
- `FCOP-4.0-WP4F-PUBLIC-DOCS-AND-RELEASE.md`: package pages, dry-run, gated release.
- `FCOP-4.0-WP4F-LOCAL-MCP-UPGRADE-PLAN.md`: actual configured 3.2.2 environment,
  precise Phase B upgrade and restart verification; not a completed upgrade.
- This result report and the delivery Manifest complete the review documents.

Public PyPI 4.0.0 page checks are necessarily post-upload Phase B work, not
falsely reported as completed before approval. The actual host MCP remains
unchanged in Phase A. CodeFlowMu is unrelated and untouched. Finish final
verification, request the single readiness Gate, and stop for ADMIN.
