"""Render one migration guide from the verified XLSX-backed matrix."""
from __future__ import annotations

import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
matrix = json.loads((root / "workspace/mcp-boundary-405/migration-matrix.json").read_text(encoding="utf-8"))
assert matrix["old_count"] == 49 and matrix["canonical_count"] == 25
lines = ["# Migrating the 49-tool MCP surface to FCoP 4.0.5", "",
         "The 4.0.5 default MCP server exposes exactly **25 Canonical MCP Tools + 6 read-only Core Resources**. The 49 rows below describe the historical 49-tool implementation surface and are sourced from the supplied decision workbook and frozen 4.0.3 `tools/list` baseline. The final taskbook overrides the workbook on `write_task` and `fcop_audit`.",
         "", "The default server root is chosen by `fcop-mcp --root PATH` or `FCOP_PROJECT_DIR` before startup. `init_workspace` creates a pure v4 workspace. `inspect_workspace` and `validate_workspace` use only protocol facts. Team/Solo/ME, seats, Host sessions and Runtime/EVAL governance remain outside the Base server.",
         "", "| # | Old tool | 4.0.5 disposition | Replacement | Compatibility mode |", "|---:|---|---|---|---|" ]
for row in matrix["rows"]:
    replacement = "`" + row["replacement"] + "`" if row["replacement"] else "—"
    lines.append(f"| {row['old_order']} | `{row['old_tool']}` | {row['disposition']} | {replacement} | {row['compatibility_mode']} |")
lines += ["", "The full machine-checkable mapping, including original registry implementation and XLSX cell, is [migration-matrix.json](../workspace/mcp-boundary-405/migration-matrix.json). Historical v3 APIs are explicit under `fcop.compatibility.v3` and `fcop_mcp.compatibility.v3`. `write_task` has an opt-in deprecated Python shim that only forwards to `create_task`. `fcop audit` runs the same protocol validator as the MCP tool; it does not repair or inspect Git, Host or Runtime state.", ""]
(root / "docs/migration-4.0.5-mcp.md").write_text("\n".join(lines), encoding="utf-8")
print(root / "docs/migration-4.0.5-mcp.md")
