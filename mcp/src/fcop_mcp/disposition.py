"""Single declarative tool-disposition table: historical 45 plus authorized T6."""

from __future__ import annotations

from types import MappingProxyType

TOOLS = MappingProxyType({
    "approve_task": "T4",
    "archive_task": "T7",
    "archive_to_history": "LEGACY_V3_ONLY",
    "bulk_archive_to_history": "LEGACY_V3_ONLY",
    "check_update": "GLOBAL_READ",
    "claim_task": "T2",
    "create_custom_team": "BOOTSTRAP_PROFILE",
    "create_task": "CREATE_TASK",
    "deploy_role_templates": "PROFILE_DEPLOY",
    "drop_suggestion": "OPTIONAL_OBSERVATION",
    "fcop_audit": "AUDIT",
    "fcop_check": "CHECK",
    "fcop_create_alert": "OPTIONAL_ALERT_WRITE",
    "fcop_list_alerts": "OPTIONAL_ALERT_READ",
    "fcop_report": "STATUS",
    "finish_task": "LEGACY_V3_ONLY",
    "get_available_teams": "GLOBAL_READ",
    "get_governance_summary": "OPTIONAL_GOVERNANCE_READ",
    "get_team_status": "STATUS",
    "init_project": "BOOTSTRAP",
    "init_solo": "BOOTSTRAP",
    "inspect_task": "INSPECT",
    "list_governance_events": "OPTIONAL_GOVERNANCE_READ",
    "list_history": "LEGACY_V3_ONLY",
    "list_issues": "LIST_ISSUE",
    "list_reports": "LIST_REPORT",
    "list_reviews": "LIST_REVIEW",
    "list_tasks": "LIST_TASK",
    "list_workspaces": "DISCOVERY",
    "mark_human_approved": "APPEND_AUTHORIZATION",
    "new_workspace": "NEW_WORKSPACE",
    "read_history_task": "LEGACY_V3_ONLY",
    "read_report": "READ_REPORT",
    "read_review": "READ_REVIEW",
    "read_task": "READ_TASK",
    "redeploy_rules": "PROFILE_DEPLOY",
    "reject_task": "T5",
    "reopen_task": "T6",
    "set_project_dir": "BIND",
    "submit_task": "T3",
    "upgrade_fcop": "GLOBAL_READ",
    "validate_team_config": "GLOBAL_READ",
    "write_issue": "APPEND_ISSUE",
    "write_report": "APPEND_REPORT",
    "write_review": "APPEND_REVIEW",
    "write_task": "CREATE_TASK",
})

EDGES = MappingProxyType({
    "T2": ("inbox", "active"), "T3": ("active", "review"),
    "T4": ("review", "done"), "T5": ("review", "active"),
    "T6": ("done", "active"), "T7": ("done", "archive"),
})

RESOURCES = MappingProxyType({
    "fcop://config": "WORKSPACE_VIEW",
    "fcop://letter/en": "GUIDANCE",
    "fcop://letter/zh": "GUIDANCE",
    "fcop://prompt/install": "GUIDANCE",
    "fcop://prompt/install/en": "GUIDANCE",
    "fcop://protocol": "DISTRIBUTION",
    "fcop://rules": "DISTRIBUTION",
    "fcop://spec": "VERSIONED_SPEC",
    "fcop://spec/en": "VERSIONED_SPEC",
    "fcop://status": "WORKSPACE_VIEW",
    "fcop://teams": "PROFILE_CATALOG",
    "fcop://team": "DISTRIBUTION",
})

TEMPLATES = MappingProxyType({
    "fcop://teams/{team}": "PROFILE_RESOURCE",
    "fcop://teams/{team}/{role}": "PROFILE_RESOURCE",
    "fcop://teams/{team}/{role}/en": "PROFILE_RESOURCE",
    "fcop://guidance/{assembly}/{language}": "DISTRIBUTION",
})
