# WP4C.3a delivery Manifest — audit correction and BLOCKED resume evidence

This is NOT a completed rule-package implementation and requests NO acceptance Gate.

## Fixed authority and direct parent chain

```yaml
TASKBOOK_COMMIT: 0559e0fdf5390aa830f98a38d83f96f1cd475ab1
TASKBOOK_BYTES: 15954
TASKBOOK_SHA256: 903c5f0f249598ab3b5aaf7e947af8ed36fbc23928eff9b5db11e305acb21ba6
TASKBOOK_PARENT: 78ea6b89a1ef0df0e504a3cfa34cecddeb7dda24
AUDIT_CORRECTION_COMMIT: e1ed85e4ba5aba212ddf3cc4f880c0abecc2bfab
CONTENT_COMMIT: 67bf7a08915024fa5d88b5e66eb6396b68d1c6c8
MANIFEST_COMMIT: SELF_COMMIT_CONTAINING_THIS_MANIFEST
AUTHORIZED_SCOPE: WP4C_3A_AUDIT_SCOPE_ALIGNMENT_AND_WP4C_3_RESUME
BRANCH: review/fcop-4.0-wp4c.3a-audit-scope-and-rule-package
PR_BASE: taskbook/fcop-4.0-wp4c.3a-audit-scope-alignment
WP4C_3A_STATUS: BLOCKED
AUDIT_SCOPE_CORRECTION: PASS
WP4C_3_STATUS: BLOCKED
STOP_REASON: DIST_02_DEVELOPMENT_REFERENCE_FIXTURE_INPUT_MISSING
REQUESTED_GATE: NONE_BLOCKED
```

[Taskbook](https://github.com/joinwell52-AI/FCoP/blob/0559e0fdf5390aa830f98a38d83f96f1cd475ab1/taskbooks/fcop-4.0/WP4C.3a/01-Historical-Audit-Scope-Alignment-and-WP4C.3-Resume-Taskbook-v1.0.zh.md), [ADMIN authorization](https://github.com/joinwell52-AI/FCoP/pull/21#issuecomment-5567383721), [corrected-hash erratum](https://github.com/joinwell52-AI/FCoP/pull/21#issuecomment-5567650164). Old a61c4159... hash is revoked.

The audit commit changes exactly three authorized Conformance files. Content changes exactly five reports, not production. This Manifest-only commit directly follows Content, which directly follows Audit, which directly follows Taskbook. PR #21's blocker commits remain in the ancestor chain and its PR is preserved.

## Exact cumulative delivery inventory

All values below hash complete raw Git blobs at Content. No newline normalization is used for these identities. The eight paths include the three prior Audit-commit files and all five Content reports.

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| reports/FCOP-4.0-WP4C.3-CLAUSE-AND-ARTIFACT-MAPPING.md | 5360 | d54235d9c917c609c9c72e045fd45b3d390ec8b62f0f5d0efeb963717572e2a3 |
| reports/FCOP-4.0-WP4C.3-CONFORMANCE-RESULT.md | 6013 | 1dac8aa17332abf69d1070de23d9efa71a0aca336cc595a9dc69dcb5e03cb59e |
| reports/FCOP-4.0-WP4C.3-IMPLEMENTATION-PLAN.md | 9260 | 389864d2c7a1c4e3ccedb17a52f65db9dc12752b674c6f569eddb02f765a49d5 |
| reports/FCOP-4.0-WP4C.3-RESULT.md | 7253 | b80e48c8978de16e51e7d324db00d94afc115c9898d5191f60df90c36607d086 |
| reports/FCOP-4.0-WP4C.3A-AUDIT-SCOPE-CORRECTION.md | 8795 | 7b8ed6fe4322c7c508ef789ab011149259deb4435c7c241dc854b21181b0837c |
| tests/conformance/rule_distribution_v4/conftest.py | 16826 | e9571f4d0051e04cbc0e63ef9a8e2cdc9d5facd427afafb6c4934c305d835a67 |
| tests/conformance/rule_distribution_v4/test_dist_00_meta.py | 14382 | 816d739dd4eed73c545ee75947c893eba44f5a9f944dbc37ef978b582746c9d6 |
| tests/conformance/rule_distribution_v4/test_dist_25_30_failures_artifacts_context_gates.py | 13044 | be6a3fe99b19da82f1c14b964c96d02160812b169d5ad10b4d5cd5203a64839c |

The ninth and only additional path is `reviews/fcop-4.0/wp4c.3/MANIFEST.md`. Its final SHA-256 and immutable Manifest HEAD cannot be embedded recursively here; they are verified from the commit containing this file and included in the post-push Draft PR receipt. No other path is authorized by this blocked delivery.

## Validation and boundary

- Historical WP4C.2 diff remains exactly its original 13 paths, no historical merge.
- Meta 33/33 + DIST-30 1/1 pass; collection remains 176 (33 + 56 + 86 + 1).
- Standard-entry behavior baseline: 142 expected missing-production reds / 1 control pass, 364.12s. Earlier queue timeout and reruns are preserved in the report.
- FCoP 1256/1256; frozen v4 Core 119/119; MCP 134/134; Ruff and mypy PASS.
- DIST-01-29 ASTs unchanged; DIST-30 has 18 Assert nodes before/after; no skip/xfail or renamed IDs.
- No production, package rules, frozen spec/contract, public snapshot, Schema, Host, MCP, CodeFlowMu, main, version or release changes.
- New unresolved fixture: DIST-02 requests four development references without providing their identities/files. The fourth Conformance file needed for a local fixture correction is not authorized. See the plan and result reports.
- Canonical artifacts 0/18; package Manifest 0/1; new API 0. No implementation Gate requested.

## Raw local-byte verification method and preserved Windows checkout

The execution worktree is `D:/FCoP-wp4c3a-audit-scope-and-rule-package`.
Its five report files match raw Git bytes. The three Audit files retain pre-existing Windows checkout CRLF lines (417, 325 and 304 respectively); their Git blobs contain no CRLF. Diagnostic newline normalization matches, but that diagnostic is NOT counted as raw-byte proof. The original three files were not rewritten after their independent commit.

Final raw local proof uses a new, detached verification-only checkout at the immutable Manifest HEAD:

```text
git -c core.autocrlf=false worktree add --detach D:/FCoP-wp4c3a-delivery-byte-check <MANIFEST_HEAD>
```

No repository attributes/config or original working bytes are changed. At this fresh checkout, compare all nine raw filesystem byte strings with Git blobs and GitHub Contents API raw responses pinned to the SAME final SHA. Check SHA-256 and size independently; do not normalize any side. The final receipt must distinguish this verified local checkout from the preserved execution checkout.

## Required remote readback

After push, refetch only the new review branch; resolve its HEAD; verify the direct three-commit chain, exact per-commit path sets, no merge, preserved PR #21 and unchanged main. Read all nine paths from GitHub at that immutable HEAD and perform the raw three-way comparisons described above. Until that actual check completes, remote delivery is PENDING; the Draft PR receipt records actual outcomes rather than forecasting PASS.

Create a NEW Draft PR against the taskbook branch; do not target main, reuse PR #21, request reviewers, enable auto-merge or merge. Workflows filter push main/feat and PR base main; no CI is expected for this review/taskbook combination. Actual runs must be checked: no runs means NOT_TRIGGERED_BRANCH_FILTER, not green.

Stop for ADMIN fixture disposition. WP4C.4, main merge and publishing remain unauthorized.
