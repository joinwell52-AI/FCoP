# WP4C.3 Clean-baseline Conformance Result — BLOCKED

Taskbook `de213ec0f74f8976283a24986d4eb7de77c67142`, SHA-256 `a4b782db3a984be9872d6c99428c5fc669a1cd3135468b33ef8eba7a6c1b57d2`; direct parent `1f4df9cc650f63b9e842d806340eb31b768f708e`.

## Environment and command

Windows; Python 3.12.9, pytest 9.0.3. Working directory D:/FCoP-wp4c3-rule-package-core. PYTHONPATH contains this worktree's src, mcp/src and root; PYTHONDONTWRITEBYTECODE=1, PYTHONIOENCODING=utf-8. No configuration changes.

Before the run, git status --porcelain was empty. No implementation or report file existed as a new change. The frozen distribution test files are byte-identical Git blobs to the accepted parent (9/9). Fixed taskbook parent and one-file diff were verified.

```text
python -B -m pytest tests/conformance/rule_distribution_v4/test_dist_00_meta.py tests/conformance/rule_distribution_v4/test_dist_25_30_failures_artifacts_context_gates.py::test_dist_30 -q -p no:cacheprovider --tb=short
```

Actual exit: 1. Result: **2 failed, 32 passed, 1 existing Traversable deprecation warning, 11.66 seconds**.

| Node | Assertion location | Actual failure |
| --- | --- | --- |
| test_dist_00_meta.py::test_meta_allowlist_and_no_stage_advance | line 318: assert changes <= ALLOWLIST | New fixed WP4C.3 taskbook path is outside WP4C.2 allowlist |
| test_dist_25_30_failures_artifacts_context_gates.py::test_dist_30 | line 295: assert changed <= ALLOWLIST | Same new fixed WP4C.3 taskbook path is outside WP4C.2 allowlist |

Both failures list exactly this extra path:

```text
taskbooks/fcop-4.0/WP4C.3/01-Canonical-Rule-Package-Manifest-Loader-and-Assemblies-Taskbook-v1.0.zh.md
```

These are current-stage control-plane preflight failures, not expected missing-production red nodes. They must not be reclassified as PASS or deferred implementation failures. Reports written after this run would add further paths outside the same old allowlist; the original reproduction predates all such report additions.

## Collection evidence

```text
python -B -m pytest tests/conformance/rule_distribution_v4 --collect-only -q -p no:cacheprovider
```

Exit 0: 176 collected in 0.18 seconds. A separate read-only collection/count script also exited 0 and confirmed:

| Target ID | Collected nodes |
| --- | --- |
| DIST-01 | 2 |
| DIST-02 | 4 |
| DIST-03 | 6 |
| DIST-04 | 11 |
| DIST-05 | 9 |
| DIST-06 | 6 |
| DIST-07 | 4 |
| DIST-21 | 2 |
| DIST-22 | 4 |
| DIST-25 | 8 |
| Total WP4C.3 | 56 |
| Other future production nodes | 86 |
| DIST-30 | 1 |

Meta has 33 collected nodes. Collection is not behavior execution: target 56 and future 86 were not rerun as behavior following the mandatory stop.

## Checks not claimed

No new production implementation exists. Full FCoP, Core, MCP, Ruff/mypy production validation, public-surface update, artifact creation or wheel/sdist inclusion build were not run for a completed WP4C.3 implementation. Earlier WP4C.2 results remain historical and are not relabeled as current WP4C.3 passes.

The stop follows taskbook section 13: completing the required Meta/DIST-30 result requires resolving a frozen-test/current-stage audit mismatch, which cannot be repaired through authorized production files.
