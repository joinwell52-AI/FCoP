"""Patch write-side tool @mcp.tool decorators to include tags={"binding_required"}."""
import re

content = open("mcp/src/fcop_mcp/server.py", encoding="utf-8").read()
lines = content.split("\n")

WRITE_SIDE_FUNS = {
    "init_project", "init_solo", "create_custom_team",
    "write_task", "archive_task", "write_report", "write_issue", "write_review",
    "mark_human_approved", "deploy_role_templates", "new_workspace",
    "drop_suggestion", "fcop_audit", "redeploy_rules", "fcop_create_alert",
}

patched = 0
for i, line in enumerate(lines):
    m = re.match(r'^def (\w+)\b', line)
    if m and m.group(1) in WRITE_SIDE_FUNS:
        # look backward for @mcp.tool
        j = i - 1
        while j >= 0 and lines[j].strip() == "":
            j -= 1
        if j >= 0 and lines[j].strip() == "@mcp.tool":
            lines[j] = '@mcp.tool(tags={"binding_required"})'
            print(f"  Patched line {j+1}: {m.group(1)}")
            patched += 1

open("mcp/src/fcop_mcp/server.py", "w", encoding="utf-8").write("\n".join(lines))
print(f"Total patched: {patched}")
