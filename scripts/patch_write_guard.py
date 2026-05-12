"""Patch write-side tools to use _get_project_write() instead of _get_project()."""
content = open("mcp/src/fcop_mcp/server.py", encoding="utf-8").read()
lines = content.split("\n")

write_side_lines = {
    716: "init_project",
    789: "init_solo",
    859: "create_custom_team",
    963: "write_task",
    1097: "archive_task",
    1138: "write_report",
    1235: "write_issue",
    1301: "write_review",
    1443: "mark_human_approved",
    1628: "deploy_role_templates",
    1771: "new_workspace",
    1956: "drop_suggestion",
    2689: "fcop_audit",
    2754: "redeploy_rules",
}

replaced = 0
for lineno, tool_name in write_side_lines.items():
    idx = lineno - 1
    line = lines[idx]
    if "_get_project()" in line:
        lines[idx] = line.replace("_get_project()", f'_get_project_write("{tool_name}")')
        print(f"  OK line {lineno}: {tool_name}")
        replaced += 1
    else:
        print(f"  MISS line {lineno}: {tool_name!r} -> {line.strip()!r}")

open("mcp/src/fcop_mcp/server.py", "w", encoding="utf-8").write("\n".join(lines))
print(f"Total replaced: {replaced}")
