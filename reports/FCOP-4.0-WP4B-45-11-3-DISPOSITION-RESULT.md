# WP4B canonical disposition result (historical 45 + authorized 1)

Authority: WP4B.0 preserves three Profile templates; WP4B.1 adds only
reopen_task. The historical filename is retained as requested.
Counts are **46 tools, 11 static resources, 3 resource templates**.
They are surface/disposition counts, not claims of 60 or 46 independent
successful business scenarios. Behavioral evidence is identified separately.

All 45 historical tool names remain; close_issue and generic transition are
absent. T6 has exactly task_id, review_ref, authorization_ref, profile_ref,
actor and optional lang. Existing required parameters are not tightened.
Snapshot source: `tests/test_fcop_mcp/snapshots/tool_surface_v4.json`.
Historical `tool_surface.json` remains byte-identical in Git.

## Tools

Test paths below are under tests/test_fcop_mcp unless Core names are specified.
Every listed name is checked by exact surface equality; the policy column comes
from the single disposition table, not an independent dispatcher.

| # | Tool | Policy | v4 result boundary | Additional behavioral evidence |
|---:|---|---|---|---|
| 1 | `approve_task` | T4 | Project delegation / read-only projection | test_wp4b_delivery.py::test_mcp_entire_lifecycle_and_four_envelopes; test_wp4b_races.py |
| 2 | `archive_task` | T7 | Project delegation / read-only projection | test_wp4b_delivery.py::test_mcp_entire_lifecycle_and_four_envelopes; test_wp4b_races.py |
| 3 | `archive_to_history` | LEGACY_V3_ONLY | LEGACY_TRANSITION_NOT_ALLOWED; zero writes | test_wp4b_delivery.py::test_mcp_entire_lifecycle_and_four_envelopes |
| 4 | `bulk_archive_to_history` | LEGACY_V3_ONLY | LEGACY_TRANSITION_NOT_ALLOWED; zero writes | test_wp4b_delivery.py::test_mcp_entire_lifecycle_and_four_envelopes |
| 5 | `check_update` | GLOBAL_READ | Existing non-Core capability, no new workspace authority | test_tool_surface.py; declarative routing audit (not a claim of individual successful behavior) |
| 6 | `claim_task` | T2 | Project delegation / read-only projection | test_wp4b_delivery.py::test_mcp_entire_lifecycle_and_four_envelopes; test_wp4b_races.py |
| 7 | `create_custom_team` | BOOTSTRAP_PROFILE | Explicit OPERATION_NOT_IMPLEMENTED on bound v4; no v3 fallback | test_tool_surface.py; declarative routing audit (not a claim of individual successful behavior) |
| 8 | `create_task` | CREATE_TASK | Project delegation / read-only projection | test_wp4b_delivery.py::test_mcp_entire_lifecycle_and_four_envelopes; test_wp4b_races.py |
| 9 | `deploy_role_templates` | PROFILE_DEPLOY | Explicit OPERATION_NOT_IMPLEMENTED on bound v4; no v3 fallback | test_tool_surface.py; declarative routing audit (not a claim of individual successful behavior) |
| 10 | `drop_suggestion` | OPTIONAL_OBSERVATION | Explicit OPERATION_NOT_IMPLEMENTED on bound v4; no v3 fallback | test_tool_surface.py; declarative routing audit (not a claim of individual successful behavior) |
| 11 | `fcop_audit` | AUDIT | Project delegation / read-only projection | test_tool_surface.py; declarative routing audit (not a claim of individual successful behavior) |
| 12 | `fcop_check` | CHECK | Project delegation / read-only projection | test_tool_surface.py; declarative routing audit (not a claim of individual successful behavior) |
| 13 | `fcop_create_alert` | OPTIONAL_ALERT_WRITE | Explicit OPERATION_NOT_IMPLEMENTED on bound v4; no v3 fallback | test_tool_surface.py; declarative routing audit (not a claim of individual successful behavior) |
| 14 | `fcop_list_alerts` | OPTIONAL_ALERT_READ | Explicit OPERATION_NOT_IMPLEMENTED on bound v4; no v3 fallback | test_tool_surface.py; declarative routing audit (not a claim of individual successful behavior) |
| 15 | `fcop_report` | STATUS | Project delegation / read-only projection | test_tool_surface.py; declarative routing audit (not a claim of individual successful behavior) |
| 16 | `finish_task` | LEGACY_V3_ONLY | LEGACY_TRANSITION_NOT_ALLOWED; zero writes | test_wp4b_delivery.py::test_mcp_entire_lifecycle_and_four_envelopes |
| 17 | `get_available_teams` | GLOBAL_READ | Existing non-Core capability, no new workspace authority | test_tool_surface.py; declarative routing audit (not a claim of individual successful behavior) |
| 18 | `get_governance_summary` | OPTIONAL_GOVERNANCE_READ | Explicit OPERATION_NOT_IMPLEMENTED on bound v4; no v3 fallback | test_tool_surface.py; declarative routing audit (not a claim of individual successful behavior) |
| 19 | `get_team_status` | STATUS | Project delegation / read-only projection | test_tool_surface.py; declarative routing audit (not a claim of individual successful behavior) |
| 20 | `init_project` | BOOTSTRAP | Project delegation / read-only projection | test_tool_surface.py; declarative routing audit (not a claim of individual successful behavior) |
| 21 | `init_solo` | BOOTSTRAP | Project delegation / read-only projection | test_tool_surface.py; declarative routing audit (not a claim of individual successful behavior) |
| 22 | `inspect_task` | INSPECT | Project delegation / read-only projection | test_tool_surface.py; declarative routing audit (not a claim of individual successful behavior) |
| 23 | `list_governance_events` | OPTIONAL_GOVERNANCE_READ | Explicit OPERATION_NOT_IMPLEMENTED on bound v4; no v3 fallback | test_tool_surface.py; declarative routing audit (not a claim of individual successful behavior) |
| 24 | `list_history` | LEGACY_V3_ONLY | LEGACY_TRANSITION_NOT_ALLOWED; zero writes | test_wp4b_delivery.py::test_mcp_entire_lifecycle_and_four_envelopes |
| 25 | `list_issues` | LIST_ISSUE | Project delegation / read-only projection | test_tool_surface.py; declarative routing audit (not a claim of individual successful behavior) |
| 26 | `list_reports` | LIST_REPORT | Project delegation / read-only projection | test_wp4b_delivery.py::test_mcp_query_consumers; test_v4_report_queries.py |
| 27 | `list_reviews` | LIST_REVIEW | Project delegation / read-only projection | test_wp4b_delivery.py::test_v4_query_filters_are_real_projections |
| 28 | `list_tasks` | LIST_TASK | Project delegation / read-only projection | test_wp4b_delivery.py::test_v4_query_filters_are_real_projections |
| 29 | `list_workspaces` | DISCOVERY | Explicit OPERATION_NOT_IMPLEMENTED on bound v4; no v3 fallback | test_tool_surface.py; declarative routing audit (not a claim of individual successful behavior) |
| 30 | `mark_human_approved` | APPEND_AUTHORIZATION | Project delegation / read-only projection | test_wp4b_authorization_append.py; test_v4_authorization_append.py |
| 31 | `new_workspace` | NEW_WORKSPACE | Project delegation / read-only projection | test_tool_surface.py; declarative routing audit (not a claim of individual successful behavior) |
| 32 | `read_history_task` | LEGACY_V3_ONLY | LEGACY_TRANSITION_NOT_ALLOWED; zero writes | test_wp4b_delivery.py::test_mcp_entire_lifecycle_and_four_envelopes |
| 33 | `read_report` | READ_REPORT | Project delegation / read-only projection | test_wp4b_delivery.py::test_mcp_query_consumers; test_v4_report_queries.py |
| 34 | `read_review` | READ_REVIEW | Project delegation / read-only projection | test_tool_surface.py; declarative routing audit (not a claim of individual successful behavior) |
| 35 | `read_task` | READ_TASK | Project delegation / read-only projection | test_tool_surface.py; declarative routing audit (not a claim of individual successful behavior) |
| 36 | `redeploy_rules` | PROFILE_DEPLOY | Explicit OPERATION_NOT_IMPLEMENTED on bound v4; no v3 fallback | test_tool_surface.py; declarative routing audit (not a claim of individual successful behavior) |
| 37 | `reject_task` | T5 | Project delegation / read-only projection | test_wp4b_delivery.py::test_mcp_entire_lifecycle_and_four_envelopes; test_wp4b_races.py |
| 38 | `reopen_task` | T6 | Project delegation / read-only projection | test_wp4b_delivery.py::test_mcp_entire_lifecycle_and_four_envelopes; test_wp4b_races.py |
| 39 | `set_project_dir` | BIND | Project delegation / read-only projection | test_wp4b_delivery.py::test_rebind_version_and_registry_immutable |
| 40 | `submit_task` | T3 | Project delegation / read-only projection | test_wp4b_delivery.py::test_mcp_entire_lifecycle_and_four_envelopes; test_wp4b_races.py |
| 41 | `upgrade_fcop` | GLOBAL_READ | Existing non-Core capability, no new workspace authority | test_tool_surface.py; declarative routing audit (not a claim of individual successful behavior) |
| 42 | `validate_team_config` | GLOBAL_READ | Existing non-Core capability, no new workspace authority | test_tool_surface.py; declarative routing audit (not a claim of individual successful behavior) |
| 43 | `write_issue` | APPEND_ISSUE | Project delegation / read-only projection | test_wp4b_delivery.py::test_mcp_entire_lifecycle_and_four_envelopes; test_wp4b_races.py |
| 44 | `write_report` | APPEND_REPORT | Project delegation / read-only projection | test_wp4b_delivery.py::test_mcp_entire_lifecycle_and_four_envelopes; test_wp4b_races.py |
| 45 | `write_review` | APPEND_REVIEW | Project delegation / read-only projection | test_wp4b_delivery.py::test_mcp_entire_lifecycle_and_four_envelopes; test_wp4b_races.py |
| 46 | `write_task` | CREATE_TASK | Project delegation / read-only projection | test_wp4b_delivery.py::test_mcp_entire_lifecycle_and_four_envelopes; test_wp4b_races.py |

## Static resources

Every URI is actually read for both v3 and v4 by
test_all_static_resources_and_disposition, including expected typed failures;
full workspace bytes remain unchanged.

| # | URI | Policy | Result |
|---:|---|---|---|
| 1 | `fcop://config` | WORKSPACE_VIEW | Read-only versioned/catalog projection |
| 2 | `fcop://letter/en` | GUIDANCE | v4 typed unavailable; v3 legacy text |
| 3 | `fcop://letter/zh` | GUIDANCE | v4 typed unavailable; v3 legacy text |
| 4 | `fcop://prompt/install` | GUIDANCE | v4 typed unavailable; v3 legacy text |
| 5 | `fcop://prompt/install/en` | GUIDANCE | v4 typed unavailable; v3 legacy text |
| 6 | `fcop://protocol` | RULES_PENDING_WP4C | v4 typed unavailable; v3 legacy text |
| 7 | `fcop://rules` | RULES_PENDING_WP4C | v4 typed unavailable; v3 legacy text |
| 8 | `fcop://spec` | VERSIONED_SPEC | Read-only versioned/catalog projection |
| 9 | `fcop://spec/en` | VERSIONED_SPEC | Read-only versioned/catalog projection |
| 10 | `fcop://status` | WORKSPACE_VIEW | Read-only versioned/catalog projection |
| 11 | `fcop://teams` | PROFILE_CATALOG | Read-only versioned/catalog projection |

## Resource templates

| # | URI | Boundary |
|---:|---|---|
| 1 | `fcop://teams/{team}` | PROFILE_RESOURCE; registered read-only catalog; never authorization |
| 2 | `fcop://teams/{team}/{role}` | PROFILE_RESOURCE; registered read-only catalog; never authorization |
| 3 | `fcop://teams/{team}/{role}/en` | PROFILE_RESOURCE; registered read-only catalog; never authorization |

Known catalog reads, unknown names and path traversal are tested individually
in test_wp4b_resume.py. Empty-registry T6 remains rejected after reading a role.
These are Profile documents, not business-envelope generators. Their version: 1
is never used to classify a workspace.

## Behavioral execution

Real FastMCP Client tests cover four envelope writers, T1–T7, durable create
retry, fresh-server authorized retry, public REPORT-head parity, local trusted
authorization append, rejection/zero writes and version rebinding.
Five race tests submit actual operations: same/different-digest cross-process
create requests with the same operation_id; Branch reopen vs Root archive;
Root reopen vs Branch creation; same-authorization T6 plus different-edge reuse.
No parallel parameter probe is counted as a race.
TASK filters cover parent/branch_of/references; REVIEW subject_ref covers the
fourth Core relation and its kind/reference/authorization binding projection.
Profile/Legacy thread_key is not silently promoted into a Core relation.
