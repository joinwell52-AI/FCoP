# WP4C.3 Pre-implementation Plan — BLOCKED

Taskbook `de213ec0f74f8976283a24986d4eb7de77c67142`, SHA-256 `a4b782db3a984be9872d6c99428c5fc669a1cd3135468b33ef8eba7a6c1b57d2`; direct parent `1f4df9cc650f63b9e842d806340eb31b768f708e`.

## Authority verified

GitHub contents API raw taskbook bytes and the fetched Git blob match the supplied SHA-256. The taskbook commit adds exactly one taskbook file to the accepted parent. The accepted rule contract and frozen Core commits are ancestors.

The signed parent Gate is [ADMIN comment 5566832805](https://github.com/joinwell52-AI/FCoP/pull/20#issuecomment-5566832805); separate WP4C.3 authority is [ADMIN comment 5566995623](https://github.com/joinwell52-AI/FCoP/pull/20#issuecomment-5566995623). Neither authorizes WP4C.4, main merge or release.

A new independent worktree was created at the fixed commit:
- Worktree: D:/FCoP-wp4c3-rule-package-core
- Branch: review/fcop-4.0-wp4c.3-rule-package-core

Original worktrees were not switched, cleaned, stashed, reset, migrated or absorbed. No FCoP MCP report tool is available in this session; no workspace bootstrap or rule redeployment was attempted. The fixed ADMIN taskbook is the landed execution authority.

## Read-only wiring facts, not implemented changes

| Surface | Observed baseline | Authorized plan if unblocked |
| --- | --- | --- |
| Project version routing | src/fcop/v4/boundary.py:15 defines explicit method policies; lines 67-97 dispatch version wrappers; lines 100-115 require exact public-method classification | Add only rule_distribution policy and one Project forwarding method |
| Handler registry | src/fcop/v4/creation.py:241-272 maps named handlers; no rule_distribution entry | Register one private loader/selector handler without Core algorithm changes |
| Package data | pyproject.toml:99-106 explicitly includes existing rules and schemas; lines 109 onward include src/fcop in sdist | Add only the authorized v4 rule data inclusion |
| New production files | None created | The 19 taskbook-listed data files and private loader/selector modules only; final module split not selected before the blocker |
| Public signature | Project.rule_distribution absent in fixed baseline | Only Project.rule_distribution(*, action: str, request: Mapping[str, Any]) -> Mapping[str, Any] |
| State | No implementation started | Pure read-only library parsing/selection; no dependencies, Store, lock, state machine or background component |

The 73-clause content review, 18-artifact composition, legacy surface/rule byte inventory and final implementation file decomposition were not completed: the clean-baseline control-plane failure below triggers taskbook section 13 before coding. This document is a partial preflight record, not a completed implementation plan or a claim of clause parity.

## Blocking preflight finding

Frozen tests bind INPUT_HEAD to WP4C.2a commit 921be62c32ccccece53be74e7e565b1b37731fbe, while applying the WP4C.2-only ALLOWLIST to an open-ended current-worktree diff. Both Meta and DIST-30 therefore reject even the new authorized WP4C.3 taskbook before any implementation exists.

Source evidence at the fixed taskbook commit:
- tests/conformance/rule_distribution_v4/conftest.py:22 — historical INPUT_HEAD.
- conftest.py:91-95 — thirteen WP4C.2 delivery paths only.
- test_dist_00_meta.py:315-319 — historical-to-current diff plus untracked paths.
- test_dist_25_30_failures_artifacts_context_gates.py:293-296 — identical current-diff restriction.

The new taskbook requires Meta 33/33 and DIST-30 1/1 at section 11.3 while forbidding edits to the above frozen files at sections 8 and 10. Production code cannot change Git's committed path set legitimately. No monkeypatch, altered Git output, test relocation, selective exclusion, skip/xfail, checkout substitution or changed assertion is an authorized workaround.

## Required ADMIN decision

Separate the historical WP4C.2 delivery audit from current-stage WP4C.3 scope enforcement through an explicit taskbook/fixture authorization. Options and exact edits must be decided by ADMIN; no change is implemented here. Any correction should preserve DIST IDs and assertions' governance meaning, and must not widen the production/API authority. Stop under section 13; do not request WP4C_3_RULE_PACKAGE_ACCEPTED.
