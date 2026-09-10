# WP4C.3a historical audit correction — PASS (overall resume BLOCKED)

Taskbook: `0559e0fdf5390aa830f98a38d83f96f1cd475ab1`, path `taskbooks/fcop-4.0/WP4C.3a/01-Historical-Audit-Scope-Alignment-and-WP4C.3-Resume-Taskbook-v1.0.zh.md`.
Raw bytes: 15954; SHA-256: `903c5f0f249598ab3b5aaf7e947af8ed36fbc23928eff9b5db11e305acb21ba6`.
[ADMIN authorization](https://github.com/joinwell52-AI/FCoP/pull/21#issuecomment-5567383721) and [hash erratum](https://github.com/joinwell52-AI/FCoP/pull/21#issuecomment-5567650164) were read back. The revoked `a61c4159...` is NOT an accepted identity.
Direct parent: `78ea6b89a1ef0df0e504a3cfa34cecddeb7dda24`; original WP4C.3 taskbook: `de213ec0f74f8976283a24986d4eb7de77c67142` (SHA-256 `a4b782db3a984be9872d6c99428c5fc669a1cd3135468b33ef8eba7a6c1b57d2`).
Audit correction commit: `e1ed85e4ba5aba212ddf3cc4f880c0abecc2bfab`, direct child of the corrected-identity taskbook.
Scope: `WP4C_3A_AUDIT_SCOPE_ALIGNMENT_AND_WP4C_3_RESUME`.

## Original failure and corrected boundary

Original blocker Content 0e89f94aa8df017817f76dadc8572c8bc5c0afdf / Manifest 78ea6b89a1ef0df0e504a3cfa34cecddeb7dda24 records the clean WP4C.3 taskbook baseline: 32 Meta passed, 1 Meta failed; DIST-30 failed; combined 2 failed / 32 passed in 11.66s. Both compared current changes to the WP4C.2-only whitelist. The later authorized taskbook was the sole extra path. This historical result is not represented as a fresh run against old code.

Corrected audit is exactly:

```text
921be62c32ccccece53be74e7e565b1b37731fbe..1f4df9cc650f63b9e842d806340eb31b768f708e
```

After correction the same Meta + DIST-30 command yields 34 passed / 0 failed in 16.21s. History contains no merge; its accepted endpoint is an ancestor of the current taskbook/audit commit. No allowlist expansion occurred.

## Exact historical 13 paths

```text
reports/FCOP-4.0-WP4C.2-CONFORMANCE-PLAN.md
reports/FCOP-4.0-WP4C.2-RED-BASELINE.md
reports/FCOP-4.0-WP4C.2-RESULT.md
reviews/fcop-4.0/wp4c.2/MANIFEST.md
tests/conformance/rule_distribution_v4/__init__.py
tests/conformance/rule_distribution_v4/conftest.py
tests/conformance/rule_distribution_v4/driver.py
tests/conformance/rule_distribution_v4/test_dist_00_meta.py
tests/conformance/rule_distribution_v4/test_dist_01_06_manifest.py
tests/conformance/rule_distribution_v4/test_dist_07_12_profiles.py
tests/conformance/rule_distribution_v4/test_dist_13_20_projection.py
tests/conformance/rule_distribution_v4/test_dist_21_24_assembly_compat_mcp.py
tests/conformance/rule_distribution_v4/test_dist_25_30_failures_artifacts_context_gates.py
```

## Three-file correction and regression proof

| File | Exact responsibility / retained boundary |
| --- | --- |
| conftest.py | Add immutable WP4C_2_INPUT_HEAD / WP4C_2_ACCEPTED_HEAD; preserve INPUT_HEAD meaning; history-only helper has no ref arguments and invokes one Git-object diff; exact set validator rejects an injected fourteenth path |
| test_dist_00_meta.py | Existing test_meta_allowlist_and_no_stage_advance now compares exact historical13, tests 14th-path rejection, no historical merge, ancestor relationship, later authorized taskbook exclusion and fixed literals; retains all other Meta and anti-stub checks |
| test_dist_25_30_failures_artifacts_context_gates.py | Change only final DIST-30 paths/merge audit to the fixed interval; preserve Gate provenance, original input facts, all zero-write assertions and total 18 Assert nodes |

The new regression checks are inside an existing Meta test, so 33 Meta and 176 total collection stay unchanged. AST comparison proves DIST-01-29 entirely unchanged, including decorators/behavior assertions. No mocks of Git output, environment audit bypass, renamed ID or skip/xfail were introduced.

Current untracked files cannot affect historical_delivery_paths: its source is AST-checked to have no arguments and exactly one Git call using the two immutable SHAs; it never consults ls-files or filesystem enumeration. The later WP4C.3 taskbook's real committed path set is separately compared and cannot intersect the historical13. Current-stage untracked changes remain executor/Manifest concerns: this worktree started clean at the taskbook, only three allowlisted files existed before the audit commit, then only the five reports and Manifest are permitted for this blocker delivery. A final whole-diff and clean-worktree check is required; this history helper is not a current-scope bypass.

## Executed validation

Environment: Windows, Python 3.12.9, pytest 9.0.3; independent worktree `D:/FCoP-wp4c3a-audit-scope-and-rule-package`. Set `PYTHONDONTWRITEBYTECODE=1`; PYTHONPATH points to this worktree's src, mcp/src and root. Pytest commands use `-p no:cacheprovider`; no skip/xfail or test timeout was added.

| Command (relative to worktree) | Actual outcome | Exit |
| --- | --- | ---: |
| python -B -m pytest tests/conformance/rule_distribution_v4/test_dist_00_meta.py tests/conformance/rule_distribution_v4/test_dist_25_30_failures_artifacts_context_gates.py::test_dist_30 -q -p no:cacheprovider --tb=short | 34 passed, 1 warning, 16.21s (33 Meta + DIST-30) | 0 |
| python -B -m pytest tests/conformance/rule_distribution_v4 --collect-only -q -p no:cacheprovider | 176 nodes: 33 Meta + 56 current + 86 future + 1 control | 0 |
| python -B -m pytest tests/conformance/rule_distribution_v4 --ignore=tests/conformance/rule_distribution_v4/test_dist_00_meta.py -q -p no:cacheprovider --tb=line | 142 failed, 1 passed, 3 warnings, 364.12s; all 142 failures are DistributionNotImplementedError / RULE_DISTRIBUTION_NOT_IMPLEMENTED | 1 (expected red baseline) |
| python -B -m pytest tests/test_fcop -q -p no:cacheprovider | 1256 passed, 3 warnings, 994.31s | 0 |
| python -B -m pytest tests/conformance/v4 -q -p no:cacheprovider | 119 passed, 3 warnings, 122.30s | 0 |
| python -B -m pytest tests/test_fcop_mcp --import-mode=importlib -q -p no:cacheprovider | 134 passed, 3 warnings, 354.62s | 0 |
| python -B -m ruff check src/fcop tests/test_fcop tests/conformance/rule_distribution_v4 | All checks passed | 0 |
| python -B -m mypy --cache-dir nul | Success: no issues found in 41 source files | 0 |
| git diff --check | No whitespace errors | 0 |

Existing warnings concern importlib.abc.Traversable and jsonschema.RefResolver deprecations. No production or dependency changes were made to silence them.

### Intermediate execution failure preserved

The first complete behavioral invocation used in-process `pytest.main` from `python -c` with an evidence collector, while other suites ran. It produced 142 failed / 1 passed in 611.02s: 141 structured missing-capability errors, one `queue.Empty` at DIST-19[two-processes]. It is NOT classified as a clean baseline. Its precise environment/harness cause was not established.

A standard `python -B -m pytest ...::test_dist_19[two-processes] -q -p no:cacheprovider --tb=short` rerun produced the expected structured DistributionNotImplementedError in 2.26s; the helper's two-process and zero-write assertions executed before that error. The complete standard-entry rerun then produced all 142 expected structured reds and DIST-30 PASS. No source, timeout, assertion, skip or xfail was changed for either rerun.

This resolves the test-run anomaly as a non-reproduced intermediate failure, not a production race acceptance. No WP4C.4 race success is claimed.


## Post-commit current-file witness

After the independent audit commit, with four current report modifications and the new, untracked FCOP-4.0-WP4C.3A-AUDIT-SCOPE-CORRECTION.md present, the same Meta + DIST-30 command was run again: 34 passed, 1 warning, 17.04s, exit 0. The historical13 remained exact. The new report is unrelated to the historical WP4C.2 delivery, but is explicitly allowed by the current taskbook and must be included in the current Manifest. No arbitrary untracked artifact is accepted by the delivery process.

## Resume decision

All first-phase prerequisites passed before commit e1ed85e4ba5aba212ddf3cc4f880c0abecc2bfab. The three audit files are frozen again after that commit. The subsequent pre-implementation input review found DIST-02's missing mandatory development bundle, requiring an unapproved fourth Conformance file; see [the implementation plan](FCOP-4.0-WP4C.3-IMPLEMENTATION-PLAN.md). No production implementation started. First-phase success does not sign the full rule-package Gate.

## Preserved history

PR #21 remains an OPEN Draft at `78ea6b89a1ef0df0e504a3cfa34cecddeb7dda24`; it was not rewritten, merged or repurposed. Its Content `0e89f94aa8df017817f76dadc8572c8bc5c0afdf` and Manifest remain ancestors. The prior 32/33 Meta and DIST-30 failure is an accepted historical blocker, now resolved by the separate audit commit. This report updates current facts; it does not erase that history.
