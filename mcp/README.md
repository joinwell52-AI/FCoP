# fcop-mcp

**MCP server that exposes the [`fcop`](https://pypi.org/project/fcop/)
library as a Model Context Protocol toolkit** for Cursor, Claude
Desktop, and every other MCP-aware client.

> This is the server shell. For the Python library (no MCP, no
> `fastmcp` dep), install [`fcop`](https://pypi.org/project/fcop/).

---

## Install

```bash
pip install fcop-mcp
```

or let `uvx` pull it on demand (recommended for Cursor / Claude
Desktop, because the MCP host upgrades the server without touching
your Python env):

```bash
uvx fcop-mcp
```

## Wire it into Cursor

Edit `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "fcop": {
      "command": "uvx",
      "args": ["fcop-mcp"]
    }
  }
}
```

## Wire it into Claude Desktop

Edit the Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`
on macOS, `%APPDATA%\Claude\claude_desktop_config.json` on Windows):

```json
{
  "mcpServers": {
    "fcop": {
      "command": "uvx",
      "args": ["fcop-mcp"]
    }
  }
}
```

Restart the client. You should see 22 tools named
`set_project_dir`, `unbound_report`, `init_project`, `init_solo`,
`create_custom_team`, `validate_team_config`, `deploy_role_templates`,
`new_workspace`, `list_workspaces`, `get_team_status`, `list_tasks`,
`read_task`, `write_task`, `inspect_task`, `drop_suggestion`,
`list_reports`, `read_report`, `list_issues`, `archive_task`,
`check_update`, `upgrade_fcop`, `get_available_teams`.

## Where does it put files?

By default the server resolves the **project root** in this order
(locked by [ADR-0003](https://github.com/joinwell52-AI/FCoP/blob/main/adr/ADR-0003-stability-charter.md)):

1. The last `set_project_dir("…")` call in this MCP session.
2. `FCOP_PROJECT_DIR` environment variable.
3. `CODEFLOW_PROJECT_DIR` (deprecated, prints one warning).
4. Walk up from the current working directory looking for
   `docs/agents/fcop.json`, `.cursor/rules/fcop-rules.mdc`, or a
   pre-existing `docs/agents/tasks/` directory.
5. Current working directory, plain.

To pin a project unconditionally, put it in your MCP client config:

```json
{
  "mcpServers": {
    "fcop": {
      "command": "uvx",
      "args": ["fcop-mcp"],
      "env": { "FCOP_PROJECT_DIR": "D:/projects/your-project" }
    }
  }
}
```

## Upgrading from `fcop 0.5.x`

If your `mcp.json` looks like this:

```json
"fcop": { "command": "uvx", "args": ["fcop"] }
```

change the one arg to:

```json
"fcop": { "command": "uvx", "args": ["fcop-mcp"] }
```

and you're done. All 22 tool names, arguments, and semantics are
preserved. The key in `mcpServers` (`"fcop"`) does not have to
change — Cursor does not care about the key name.

See [`MIGRATION-0.6.md`](https://github.com/joinwell52-AI/FCoP/blob/main/docs/MIGRATION-0.6.md)
for the full upgrade guide.

## Stability commitment

`fcop-mcp` follows the [Pre-1.0 Stability
Charter](https://github.com/joinwell52-AI/FCoP/blob/main/adr/ADR-0003-stability-charter.md):

- Tool names, parameter names, and return shapes are **additive-only**
  within any `0.6.x` release.
- Breaking changes require a `DeprecationWarning` in a preceding
  minor version and a minimum 30-day migration window.
- New capabilities arrive as **new tools**, not modifications to old
  tools.

In practice: MCP client configs that work with `fcop-mcp 0.6.0`
continue working with every subsequent `0.6.x` and `0.7.x` patch.

## License

MIT. See [`LICENSE`](../LICENSE).
