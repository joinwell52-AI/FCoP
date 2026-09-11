# CLI v1 test results

STATUS: BLOCKED
REQUESTED_ADMIN_GATE: NONE
Publication, tag and merge have not been performed.

## Commands and actual results

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
| C19 | FAIL | pre-existing README inline-prompt assertion |
| C20 | PASS | EN/ZH docs, code-block/link parity and example execution |

C19 prevents release irrespective of other passes. Final-HEAD remote CI and
publication checks are not claimed as passed.
