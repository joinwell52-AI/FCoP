# FCoP / fcop-mcp 4.0.1 delivery evidence

Authority: ADMIN_DECISION AUTHORIZE_FCOP_4_0_1_CORE_MERGE_PRIMITIVE,
2026-09-11 continuation of PR #37. This is a development delivery, not publication.

## Fixed implementation and scope

- Baseline: ec7f415f84bfb93534ffccedaad873accd744095.
- Preserved blocker: 94d840bc7fdaa8988ddb316ab06b58d7e48a1c45.
- Core/MCP implementation: 5116fec21f61545ac2bf0f87c100be85c9c321cf.
- Subsequent changes only strengthen test typing, preserve historical count
  assertions against their retained snapshot, and add executable installed proof.
- Two Core APIs, three new MCP tools; 49 tools, 12 resources, 4 templates.
- Both packages 4.0.1; MCP requires fcop>=4.0.1,<4.1.0.
- Frozen Conformance, Schema, rules, release workflows, main, CodeFlowMu and
  the existing MCP installation/configuration are unchanged.

## Verified local evidence

Native Windows Python 3.12, independent environments:

```text
Development: C:/Users/Administrator/AppData/Local/Temp/fcop-401-branch-venv
Installed:   C:/Users/Administrator/AppData/Local/Temp/fcop-401-installed-venv
```

- New Core/MCP tests: 28 passed. Real worker processes rendezvous at a Barrier
  before submitting operations, rather than probing method availability.
- Targeted existing compatibility checks: 74 passed.
- Ruff: source, tests and MCP source pass.
- Core mypy: 56 source files pass; MCP source: 19 files pass; MCP tests: 14 files pass.
- Build: Core and MCP wheel + sdist (wheel built from sdist), 4/4 built.
- Twine: 4/4 pass.
- Fresh installed wheel pair: asserted both imports are inside the clean venv
  site-packages with distribution version 4.0.1, not checkout/editable Core.
- `python -I reports/branch-merge/installed_probe.py`: real stdio 49/12/4,
  all three new tools, four cross-process race modes, four process-death/restart
  boundaries PASS. No original workspace was involved.
- Existing installed `artifact_probe.py base`: 49/12/4, create/retry/spec/error,
  five Project/resource/stdio parity and zero-write checks PASS.
- Existing installed `artifact_probe.py relay`: real MCP initialize/tool listing
  and missing-dependency diagnostic PASS. Relay implementation is unchanged.

## Local candidate artifacts (not published)

Built from implementation 5116fec; later changes are excluded test/report files.

| File | SHA-256 |
| --- | --- |
| fcop-4.0.1-py3-none-any.whl | 33047b1ef3122dd80f3d9d9e0b41a7784bddcd0b23a9cb0665d5f148bca59ca7 |
| fcop-4.0.1.tar.gz | fa2036956486e8adf303318ddea5cf142afa12e678fb84170e4e2d4de00386dc |
| fcop_mcp-4.0.1-py3-none-any.whl | 62977d8d12ed90dc2ea4aff28142b215f74a6b9c1e3cd3e96397997d7a42d5b7 |
| fcop_mcp-4.0.1.tar.gz | 063815304adc5e5e413c32dc30ffbebb5097000707a9324bcabf788e37707887 |

Artifact root: C:/Users/Administrator/AppData/Local/Temp/fcop-401-artifacts-final.
Hashes identify these local candidate files, not a release authorization or a
claim that independently rebuilt CI archives necessarily share archive timestamps.

## Failures preserved and corrected

- First combined regression: 1899 passed, 10 failures (new surface/version/count
  and bilingual link alignment); none counted as successful acceptance.
- Subsequent full `tests/` run: 2329 passed, 1 failure, 2 existing skips. Failure
  was the historical 46-tool snapshot check. It now reads the exact preserved
  4.0.0 snapshot; current 49-tool comparison is separately enforced.
- First implementation CI MCP matrix failed on ten static type errors in the new
  tests (optional structuredContent and the surface container type). Explicit
  assertions were added, without removing behavior checks or loosening mypy.
- The two existing schema skips concern absent 0.7.x historical fixture files in
  an independent worktree. No skip/xfail was introduced or expanded.

## Final validation binding

At this document's creation the final full regression and final HEAD CI are
running. This document deliberately does not predict their results. Final counts,
CI run IDs and conclusions, remote HEAD, per-file hashes and release-ready request
are bound together in the final PR #37 receipt after verification. The final
receipt must name the exact review HEAD, not a previous blocker/implementation CI.

Reproduce the full local run:

```text
python -m pytest tests -q --tb=short --junitxml=<outside-worktree>/fcop-401-final-junit.xml
```

Only after successful verification request FCOP_4_0_1_RELEASE_READY. No merging,
tags, public package uploads, local MCP upgrade or independent-reviewer rule is
authorized by this development delivery.
