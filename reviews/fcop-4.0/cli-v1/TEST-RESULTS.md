# CLI v1 test results

STATUS: FINAL_VALIDATION_PENDING
REQUESTED_ADMIN_GATE: NONE
Publication, tag and merge have not been performed.

## Current amended validation

Intermediate cafffa53 validation found one exact RELEASE-GATE-01 wording failure
and was interrupted after the focused reproduction (1 failed / 2 passed).
Its 29/29 green CI did not override this local failure. The EN/ZH self-reference
now retains the original restriction verbatim; the frozen test was NOT changed.
Current exact spec identity is 81d3229ee602341063879fe9100ab7db92417ffe.
All final validation below must run again on the next manifest HEAD.

The post-correction targeted run explicitly includes RELEASE-GATE-01:
**124 passed**, 3 warnings, 57.58s; Ruff PASS. The original frozen release
assertion passed unchanged. Current collection remains **2423 nodes**.

Both historical holds below have ADMIN resolution; no unresolved scope blocker.
Identity/resources/prompt/Conformance targeted run: **121 passed**, 3 warnings,
49.60s. CLI/Catalog: **88 passed**, 3 warnings, 15.81s.
Ruff PASS; Core mypy PASS (58 files); MCP/source tests mypy PASS (35 files).
Three new identity tests prove exact Stable EN/ZH bytes, ordered clause parity,
Core citation and unchanged normative remainder against historical digests.
The four self-reference lines retain their migration/authority restrictions.

The preceding README-alignment HEAD 80a6b08c48305a845b6fb2b025886db34375a7be
passed the full repository run: **2418 passed, 2 pre-existing skipped**, 3 warnings,
850.82s; its GitHub CI passed **29/29**. Runs: 34556627134 and 34556627108.
This is intermediate evidence, not acceptance of the amended release HEAD.

Final validation command: python -X utf8 -m pytest -q --tb=short
--junitxml=C:/Users/Administrator/AppData/Local/Temp/fcop-402-cli-final-head.xml.
Final HEAD, actual result, GitHub check runs and hashes will be bound in the
PR #40 completion receipt after the manifest-only commit. No source change may
be made between that run and merge. The final receipt, not the historical rows
below, determines C19/final-release acceptance.

## Historical initial implementation run (blocker preserved)

Development Python:
C:/Users/Administrator/AppData/Local/Temp/fcop-401-branch-venv/Scripts/python.exe.
Editable imports point to this isolated worktree, not the original workspace.

- First targeted run: 96 passed, 2 failed. Fixed only the new catalog integration
  (legacy wrapper accidentally included Branch tools) and the new test fixture
  (create a genuinely incomplete Branch, not an empty family).
- Targeted CLI, catalog, snapshots and migration compatibility: 102 passed.
- Expanded CLI/catalog/documentation run: 154 passed, 3 pre-existing warnings.
  Command: pytest tests/test_fcop/test_cli_v1.py
  tests/test_fcop_mcp/test_cli_catalog.py
  tests/test_fcop/test_wp4f_release_readiness.py -q --tb=short.
- Latest collect-only: 2420 nodes.
- Latest two new CLI/catalog files: 88 passed in 20.38s after the report-head
  typing correction. The original full run was collected before two added
  cases and is retained as intermediate evidence, not final-HEAD acceptance.
- Ruff: src tests mcp/src scripts/cli_v1_installed_probe.py PASS.
- mypy src/fcop: PASS; MCP source and tests strict mypy: PASS.
- git diff --check: PASS (normal checkout EOL notices only).
- Full-suite command: pytest -q --tb=short. Result: **2415 passed, 1 failed,
  2 skipped, 3 warnings**, 852.46 seconds (2418 collected before two added tests).
  The two pre-existing skips are test_legacy_files_validate.py:80 (absent legacy
  docs/agents/log) and :89 (empty legacy parameter set). No skip/xfail was added.
  The failure is precisely the old inline-prompt assertion identified below.
- Isolated legacy prompt test: 1 failed, 10 passed, reproduced in fixed baseline.

## C01–C20 disposition

| ID | Result | Evidence |
|---|---|---|
| C01 | PASS | test_exact_top_level_surface; test_help |
| C02 | PASS | test_init_core_only_and_existing |
| C03 | PASS | test_readonly_matrix; installed probe |
| C04 | PASS | v4 inspection and exact current REPORT head tests |
| C05 | PASS | malformed identity rejected, v3/v4 valid cases |
| C06 | PASS | catalog/CLI/declaration/real stdio set equality |
| C07 | PASS | Core-only wheel and sdist isolated probes |
| C08 | PASS | doctor matrix and Core-only installed checks |
| C09 | PASS | installed version probe |
| C10 | PASS | installed offline spec/schema/rule inventory |
| C11 | PASS | existing test_lifecycle/test_cli_migrate_v3.py |
| C12 | PASS | retained migration and help tests |
| C13 | PASS | test_compat_cli.py and exact surface test |
| C14 | PASS | READONLY-PROOF.md |
| C15 | PASS | real subprocess JSON and command matrix |
| C16 | PASS | independent Core-only environments |
| C17 | PASS | unchanged tool snapshot and real stdio |
| C18 | PASS | native Windows paths with spaces and Chinese |
| C19 | PENDING FINAL HEAD | historical inline-prompt failure resolved by ADMIN; see current validation |
| C20 | PASS | EN/ZH docs, code-block/link parity and example execution |

C19 prevents release until final-HEAD local/remote verification completes.
Public publication checks are not claimed as passed in this pre-merge report.
