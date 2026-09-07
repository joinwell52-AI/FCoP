# WP4C.3b DIST-02 fixture alignment

Status: fixture phase COMPLETE; resumed WP4C.3 BLOCKED by the historical public-method count assertion (39 vs 38) outside this task's write scope. The isolated fixture commit remains valid. The implementation and package are preserved LOCAL_ONLY; only facts and the fixture are delivered remotely. No Gate is requested. See RESULT for the blocker and exact preservation inventory.

## Fixed task and authority

- Taskbook: `3a11498c0d4aff736628e781f34516950cb34be8`, `taskbooks/fcop-4.0/WP4C.3b/01-DIST-02-Development-Reference-Fixture-and-WP4C.3-Resume-Taskbook-v1.0.zh.md`.
- Raw identity: 13446 bytes, SHA-256 `5c4cb2506a6d987dea705a2c5d1b28108b01a3d2b68cbf7b0047dbb8d3d4dbcb`; GitHub raw Blob equals fetched Git Blob.
- Input: `ec81dc5ed80ff2a4492fd0d1611aad234949bfb5`. [ADMIN approval](https://github.com/joinwell52-AI/FCoP/pull/22#issuecomment-5568219764).
- Executor: ME, solo, acting on the fixed ADMIN taskbook. Original D:\FCoP and CodeFlowMu are not execution targets.
- Worktree: `D:\FCoP-wp4c3b-development-fixture-and-rule-package`.
- Fixture commit: `115751b4c24a1924062a81a21e0d655e8cb5fedc`, direct child of the taskbook, only `tests/conformance/rule_distribution_v4/test_dist_01_06_manifest.py` changed, 16 insertions.

## Correction and preservation

Only development-no-constitution constructs four files through case.put inside the isolated workspace, under docs/fcop-4.0/development/. Each is explicitly non-normative, UTF-8/LF, and pinned to fixed test revision `1111111111111111111111111111111111111111`. The production implementation never supplies this revision or a default reference.

| File | Actual raw SHA-256 |
| --- | --- |
| entry.md | c128375367d8753687e53f1dd45dcaf1c9790193534d66d9bbee6efaef0081fc |
| manual.md | d3fe69b6cb6a6ecd42edc29517704054c12572c494d8bdda9610b76fcfa897a9 |
| contracts.md | 9d3b5bd2831f2602905ab9d682313b285eeebe6a672ea81b9eac3fdedf6b2f4e |
| task-scope.md | b5b78c13494871ea264a85a0488191b9ddcb1f8c6ec9b4bf5b1c991502428aab |

The hash table was independently recomputed from the four actual fixture byte strings: 4/4 matched. All six original assertion statements remain, with three added statements verifying containment, input hashes and exact ordered returned references. The original Test ID, parameter variants and constitution_ref=None remain. Other test functions and decorators are AST-identical; global Scenario/driver and DIST-22 are unchanged. No skip/xfail was introduced. The fixture file is frozen again after its isolated commit.

## Pre-implementation evidence

Commands run with source-root PYTHONPATH and PYTHONDONTWRITEBYTECODE=1; pytest used -p no:cacheprovider.

| Check | Observed result |
| --- | --- |
| DIST-02 and DIST-22 | 8 expected missing-capability failures, no other failure |
| Meta + DIST-30 | 34 passed (33 + 1) |
| Distribution collect-only | 176 nodes |
| Full behavior baseline | 142 expected missing-capability failures / 1 control pass; 417.28 s |
| Frozen v4 Core | 119 passed; 70.53 s |
| FCoP | 1256 passed; 903.76 s |
| Isolated MCP | 134 passed; 227.77 s |
| Ruff / mypy | PASS / 41 source files PASS before implementation |

A redundant explicit UTF-8 encode argument initially triggered Ruff UP012; removing only that redundant argument preserved bytes and passed lint before the fixture commit. Historical PR #21 audit-scope and PR #22 missing-input blockers remain recorded, not erased. The original Manifest prose miscount is resolved by ADMIN: exactly ELEVEN fields including conflicts_with.

## Resume checkpoint

After the fixture commit, 18 canonical guidance files and one Manifest were authored and independently checked before public wiring: 19/19 files, 18 hashes/sizes, 73 unique clause owners, EN/ZH primary-ID parity, ordered acyclic graph, UTF-8/LF and 11-field records all passed.

The precise ten target functions produced 56 passed, 3 deprecation warnings, 197.69 s. A preliminary -k selector also matched filenames and included future tests; its mixed result is not the 56-node acceptance command. Final results: Core 119 passed, MCP 134 passed, FCoP 1296 passed / 1 blocked historical count assertion, distribution 99 passed / 77 deferred failures (including nine explained negative overlaps). All 41 new units passed. The current GitHub delivery is fixture plus blocker facts only; the 31 implementation/data/support files remain uncommitted locally. No completion or Gate claim is made for WP4C.3.

The original workspaces and PRs are preserved; no Host, MCP, CodeFlowMu, main or release changes. Only after complete verified delivery will the executor stop and request WP4C_3_RULE_PACKAGE_ACCEPTED.
