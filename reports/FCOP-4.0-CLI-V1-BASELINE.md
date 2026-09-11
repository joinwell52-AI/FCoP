# CLI v1 baseline / task record

Task: FCOP-4.0-CLI-ADAPTER-V1-20260911; executor ME (solo), decision ADMIN.
Authority: taskbooks/fcop-4.0/CLI-V1/01-CLI-Adapter-v1-Development-Taskbook-v4.zh.md
at 8bedfd3e132b7cca38e017ca518807332abb4bc2, GitHub original blob verified:
923480c9a6c4ffa7211cb0032f5497ba4089bb97339fe203978359cd97254e3f (29943 bytes).
Old v3 taskbook is superseded. Current phase: WP0, no behavior edits yet.

Latest origin/main fetched: 8bedfd3e132b7cca38e017ca518807332abb4bc2.
Independent worktree D:/FCoP-4.0.2-cli-v1, branch codex/fcop-4.0.2-cli-v1.
Original D:/FCoP dirty/untracked/dogfood content preserved.

Read-back facts:
- src/fcop/_version.py and mcp/src/fcop_mcp/_version.py: both 4.0.1.
- pyproject.toml: fcop = fcop.cli._main:main; dynamic version; no MCP dependency.
- cli/_main.py: migrate and migrate-workspace only; bare invocation delegates
  unchanged legacy stderr guidance/exit 1. migrate is dry-run unless --apply.
- mcp/disposition.py has 46 declarations; branches.py registers the existing
  create_branch, inspect_family, merge_branches outside this table. Server 49,
  resource/template surface remains 12/4, as the retained surface snapshot records.
- Project: create_workspace, inspect_state, read_task, inspect_family and
  rule_distribution available; status/legacy inspection unavailable for v4.
  Existing v4 parser/schema/relationship inspection can be reused through a
  minimal public read-only aggregation module, without changing mutators.
- Frozen specification citation is carried by rule_distribution, not a second
  bundled copy of the v4 specification. CLI must distinguish citation from file.
- PR #38 PyPI source documentation is present. Core long description source is
  fcop-README.pypi.md; MCP source is mcp/README.md.
- Baseline collect-only: 2332 tests collected in 4.95 seconds (not a regression PASS).

No VERSION_BASELINE_ADVANCED or incompatible baseline change observed.
Scope: 9 CLI commands, optional MCP catalog, read-only queries, tests, docs,
two-package 4.0.2 metadata, and conditionally authorized release. No Host upgrade,
CodeFlowMu changes, protocol/schema changes, work tools or implicit repairs.
