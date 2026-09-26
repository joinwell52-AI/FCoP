# Migrating the 49-tool MCP surface to FCoP 4.0.5

The 4.0.5 default MCP server exposes exactly **25 Canonical MCP Tools + 6 read-only Core Resources**. The 49 rows below describe the historical 49-tool implementation surface and are sourced from the supplied decision workbook and frozen 4.0.3 `tools/list` baseline. The final taskbook overrides the workbook on `write_task` and `fcop_audit`.

The default server root is chosen by `fcop-mcp --root PATH` or `FCOP_PROJECT_DIR` before startup. `init_workspace` creates a pure v4 workspace. `inspect_workspace` and `validate_workspace` use only protocol facts. Team/Solo/ME, seats, Host sessions and Runtime/EVAL governance remain outside the Base server.

| # | Old tool | 4.0.5 disposition | Replacement | Compatibility mode |
|---:|---|---|---|---|
| 1 | `fcop_report` | host-process | `inspect_workspace` | none |
| 2 | `fcop_check` | split-pure-protocol | `validate_workspace` | none |
| 3 | `init_solo` | profile-cli | `fcop init --profile` | none |
| 4 | `init_project` | profile-cli | `fcop init --profile` | none |
| 5 | `create_custom_team` | legacy-v3 | — | explicit legacy only |
| 6 | `set_project_dir` | host-process | `--root or FCOP_PROJECT_DIR` | none |
| 7 | `deploy_role_templates` | legacy-v3 | — | explicit legacy only |
| 8 | `validate_team_config` | profile-cli | `fcop profile validate` | none |
| 9 | `create_task` | canonical | `create_task` | default MCP |
| 10 | `claim_task` | canonical | `claim_task` | default MCP |
| 11 | `submit_task` | canonical | `submit_task` | default MCP |
| 12 | `finish_task` | legacy-v3 | — | explicit legacy only |
| 13 | `approve_task` | canonical | `approve_task` | default MCP |
| 14 | `reject_task` | canonical | `reject_task` | default MCP |
| 15 | `reopen_task` | canonical | `reopen_task` | default MCP |
| 16 | `inspect_task` | canonical | `inspect_task` | default MCP |
| 17 | `list_tasks` | canonical | `list_tasks` | default MCP |
| 18 | `read_task` | canonical | `read_task` | default MCP |
| 19 | `create_branch` | canonical | `create_branch` | default MCP |
| 20 | `inspect_family` | canonical | `inspect_family` | default MCP |
| 21 | `merge_branches` | canonical | `merge_branches` | default MCP |
| 22 | `write_task` | deprecated-alias | `create_task` | opt-in Python shim; not MCP |
| 23 | `write_report` | canonical | `write_report` | default MCP |
| 24 | `write_issue` | canonical | `write_issue` | default MCP |
| 25 | `write_review` | canonical | `write_review` | default MCP |
| 26 | `list_reports` | canonical | `list_reports` | default MCP |
| 27 | `read_report` | canonical | `read_report` | default MCP |
| 28 | `list_issues` | canonical | `list_issues` | default MCP |
| 29 | `list_reviews` | canonical | `list_reviews` | default MCP |
| 30 | `read_review` | canonical | `read_review` | default MCP |
| 31 | `mark_human_approved` | canonical | `mark_human_approved` | default MCP |
| 32 | `archive_task` | canonical | `archive_task` | default MCP |
| 33 | `archive_to_history` | legacy-v3 | — | explicit legacy only |
| 34 | `bulk_archive_to_history` | legacy-v3 | — | explicit legacy only |
| 35 | `list_history` | legacy-v3 | `list_tasks` | explicit legacy only |
| 36 | `read_history_task` | legacy-v3 | `read_task` | explicit legacy only |
| 37 | `fcop_audit` | toolkit-cli | `fcop audit` | none |
| 38 | `fcop_list_alerts` | runtime-eval | — | none |
| 39 | `fcop_create_alert` | runtime-eval | — | none |
| 40 | `list_governance_events` | runtime-eval | — | none |
| 41 | `get_governance_summary` | runtime-eval | — | none |
| 42 | `drop_suggestion` | repository-governance | — | none |
| 43 | `new_workspace` | application-scaffolding | — | none |
| 44 | `list_workspaces` | application-scaffolding | — | none |
| 45 | `get_team_status` | split-pure-protocol | `inspect_workspace` | none |
| 46 | `get_available_teams` | profile-cli | `fcop profile list` | none |
| 47 | `check_update` | packaging-cli | `fcop check-update` | none |
| 48 | `upgrade_fcop` | packaging-cli | `fcop upgrade` | none |
| 49 | `redeploy_rules` | legacy-v3 | — | explicit legacy only |

The full machine-checkable mapping, including original registry implementation and XLSX cell, is [migration-matrix.json](../workspace/mcp-boundary-405/migration-matrix.json). Historical v3 APIs are explicit under `fcop.compatibility.v3` and `fcop_mcp.compatibility.v3`. `write_task` has an opt-in deprecated Python shim that only forwards to `create_task`. `fcop audit` runs the same protocol validator as the MCP tool; it does not repair or inspect Git, Host or Runtime state.
