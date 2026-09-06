# WP4A.3 result

## Scope and authority

Executor ME (solo), scope `WP4A_3_ONLY`. Taskbook commit `db4c99806e797a563541381e376c7c62e13f8da0`, SHA-256 `a1dac079f1744eb97ab15bcfa56088dac656b8843454dc49ae01ca36dbe045ee`; direct input `2ef95e5afdabfc7aa25a93fb287827682b467c9d`. Existing [Draft PR #14](https://github.com/joinwell52-AI/FCoP/pull/14), branch `review/fcop-4.0-wp4a.1-machine-contract`.

Only the exact two-line `.gitattributes` policy and three new evidence documents are authorized. The companion [checkout-policy report](FCOP-4.0-WP4A.3-WINDOWS-SCHEMA-CHECKOUT-POLICY.md) records all four old Windows failures, scope attributes, the original-tree failure, and the complete 24-file baseline blob/SHA inventory. Previous WP4A.1/WP4A.2 deliveries remain intact.

Execution worktree: `D:/FCoP-wp4a3-checkout-policy`. Fresh Windows validation worktree: `D:/FCoP-wp4a3-clean-windows`, checked out from local committed-policy snapshot `a15a0376c394f034031e3fa5580cc7ec32ac3225` with unchanged `core.autocrlf=true`. This commit contains the taskbook base plus only `.gitattributes`; it is local-only and not in the two-commit delivery chain. No pre-normalized LF tree was reused.

## Fresh-checkout and complete regression evidence

All commands below ran on native Windows / Python 3.12 in the new committed-policy checkout. Linux/macOS and Python 3.10/3.11/3.13 conclusions must come from final-head GitHub CI.

| Command / check | Observed result |
|---|---|
| Check all 24 fresh Schema byte strings against INPUT_HEAD blobs | 24/24 identical; zero CRLF; no normalization |
| `git check-attr text eol` on both v4 roots | text=set, eol=lf |
| Same attribute check on historical spec/schemas/agent.schema.json | text/eol unspecified |
| `python spec/schemas/v4/generate.py --check` | 12 schema pairs: verified |
| `python -m ruff check src tests` | PASS, zero diagnostics |
| `python -m mypy src/fcop` | PASS, 40 source files |
| `python -m pytest tests/conformance/v4 -q` | 119 passed, 3 existing warnings, 50.38s |
| `python -m pytest tests/test_fcop -q` | 1190 passed, 3 existing warnings, 406.69s |
| `python -m pytest tests/test_fcop/test_v4_schema.py -q` | 47 passed, 3 existing warnings, 200.15s; SB-01 through SB-10 PASS |
| `python -m pytest tests/test_fcop/test_public_surface.py -q` | 4 passed, drift 0, 0.16s |
| `python -m pytest tests/test_fcop_mcp -q` | 80 passed, 1 existing warning, 67.16s |
| Frozen contract ID extraction and Git comparison of tests | 60/60 IDs; every test blob unchanged |

For MCP, PYTHONPATH was explicitly set to the fresh worktree's `src` and `mcp/src`; no old installed adapter was substituted. Existing Traversable/RefResolver deprecation warnings remain; no test or warning policy changed.

The original execution tree, checked out before the attributes existed, still returned Schema drift for 24 paths. That result is preserved in the policy report and is not represented as the fresh-checkout result. Neither its Schema files nor the strict generator were rewritten.

## Build, clean wheel installation and application proof

Using the existing isolated build tools, executed from the **new committed-policy Windows checkout**:

```text
D:/FCoP-wp4a1-artifact-proof/build-env/Scripts/python.exe -m build --no-isolation --outdir D:/FCoP-wp4a3-artifact-proof/dist
python -m venv D:/FCoP-wp4a3-artifact-proof/clean-env
```

The build created an sdist then a wheel from that sdist. Package version stays 3.2.5; no release or upload took place.

| Artifact | SHA-256 |
|---|---|
| fcop-3.2.5-py3-none-any.whl | 616cfa9b4faa6d81ce64bba432ebb4d900f101865b26caeb1afd196f2474f45b |
| fcop-3.2.5.tar.gz | 116d4251b8652d2450edfe3698d0e764060069ed6eaa6e890e48c8979e17071b |

zipfile/tarfile reads proved all twelve v4 schemas in **both** artifacts equal the unchanged canonical source/package bytes. No regeneration or text normalization was used for this comparison.

The new clean venv installed this wheel using `--no-index --find-links D:/FCoP-wp4a1-artifact-proof/wheelhouse`. The wheelhouse is an existing dependency cache, not a new project dependency. Working directory was `D:/FCoP-wp4a3-artifact-proof`, with PYTHONPATH containing only `D:/FCoP-wp4a3-clean-windows/examples/v4/offline_guard`; the audit hook prevents network connections and DNS in the smoke process and descendants. No src fallback or system-site-packages.

Then the unchanged `examples/v4/artifact_smoke.py` was executed by the clean-env Python. Result: PASS. Import was `D:/FCoP-wp4a3-artifact-proof/clean-env/Lib/site-packages/fcop/__init__.py`, all twelve validators loaded, and installed Schema hashes matched the immutable inventory. Both public API applications reopened in separate interpreters:

| Mode | Reopened task | State / events | TASK SHA-256 |
|---|---|---|---|
| sequential | TASK-0c291930e374477882cb2bd11b9bbf44 | archive / 5 | ccfe56445f646f10bc9e05a75d2706938da2768f146bc1e2bc9893ff7db8f3a6 |
| family | TASK-4ba0c4a9d1f0445982ba8523b5f0ab08 | archive / 5 | 29c7bc33398e95f2d43d03f2e0ba830a87d01d850379db43e23ca787de3573eb |

The source-run minimal sequential/family application checks also passed in the 47-node Schema module. Only example-owned temporary workspaces were created and removed by their existing TemporaryDirectory contexts; no user workspace was changed.

## Delivery and remote CI boundary

The Content Commit adds only `.gitattributes` and the two new reports. The Manifest Commit adds only `reviews/fcop-4.0/wp4a.3/MANIFEST.md`. No third delivery commit, force-push or published-history amend is permitted. The local-only checkout snapshot is not a delivery ancestor; all executable/schema/test/workflow content of the delivered candidate must equal the validated snapshot. Manifest records the exact parent/content chain and four-file hash inventory; its own hash and containing commit are returned separately in the final receipt to avoid self-reference.

At report sealing, the final Manifest HEAD and its CI have not yet been published or run. This file does **not** claim prospective CI success. After normal push, remote branch refetch and GitHub commit/tree/blob readback must verify final HEAD, parent chain, 4/4 delivery hashes, and all 24 unchanged schema blob/SHA values.

Final CI must independently show Windows 4/4 and Ubuntu/macOS 8/8, Coverage, Stability Charter, library build/install/audit (not skipped), and all MCP matrix/contract/package checks. Only all 29 final-head jobs passing permits `REQUESTED_GATE: WP4A_MACHINE_CONTRACT_ACCEPTED`. Any failure/cancellation/missing check/unexpected skip requires BLOCKED and no Gate request. Intermediate taskbook CI or prior Linux-only success cannot substitute.

## Preserved state and stop condition

Existing Schema, generator, test, workflow, production, MCP, frozen spec, CHANGELOG, dependency and release files modified: 0. The only non-report addition is `.gitattributes`. No global Git config change. No original workspace migration/cleanup/redeploy, CodeFlowMu action, main merge, tag, release or WP4B work.

Pre-delivery remote main remains `68dbeb15f4e7f84e1d03f907be9fa66c2265843e`. D:/FCoP and all old deliverables are preserved. ADMIN alone signs the Gate. After the final CI receipt, stop regardless of success or blockage.
