"""Deterministic MCP reference and schema snapshot from the single manifest."""
from __future__ import annotations

import json
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(root / "src"), str(root / "mcp/src")]
from fcop_mcp.registry import export_manifest  # noqa: E402

tools = export_manifest()
assert len(tools) == 25 and len({tool["name"] for tool in tools}) == 25
snapshot = root / "tests/test_fcop_mcp/snapshots/canonical_tools_405.json"
snapshot.write_text(json.dumps(tools, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

lines = ["# FCoP 4.0.5 Canonical MCP Tools", "",
         "The default MCP server exposes **25 Canonical MCP Tools + 6 read-only Core Resources**. The 25 tools below and the schema snapshot are generated from `fcop_mcp.canonical_tools.MANIFEST` and the registered Python signatures. FCoP Core owns every protocol fact and transition. Profiles, Toolkit commands, compatibility shims, Host configuration, Runtime services, packaging and application scaffolding are separate.",
         "", "Start the server with an explicit `--root PATH` or `FCOP_PROJECT_DIR`. Call `init_workspace` to create a pure v4 workspace. It does not generate host instruction files, Team/Solo/ME roles, seats, or session state. An optional `profile` is an explicit reference; it does not grant authority without a trusted evaluator installed at server startup.", ""]
category = None
for tool in tools:
    if tool["category"] != category:
        category = tool["category"]
        lines.extend([f"## {category}", ""])
    lines.extend([f"### `{tool['name']}`", "", tool["description"], "",
                  f"Status: `{tool['status']}` · Since: `{tool['since']}` · Owner: `{tool['owner']}`", "",
                  "Input schema:", "", "```json", json.dumps(tool["inputSchema"], ensure_ascii=False, indent=2), "```", ""])
lines.extend(["## Migration", "", "Every one of the original 49 tools has exactly one disposition in [the migration guide](migration-4.0.5-mcp.md). `write_task` is an opt-in deprecated Python shim; `fcop_audit` is `fcop audit` in the Toolkit. Neither is registered by the default MCP server.", ""])
(root / "docs/mcp-tools.md").write_text("\n".join(lines), encoding="utf-8")
print(snapshot, root / "docs/mcp-tools.md")
