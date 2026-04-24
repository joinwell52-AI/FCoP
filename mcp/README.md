# fcop-mcp

**MCP server** that exposes the official [`fcop`](https://pypi.org/project/fcop/)
Python library to Cursor, Claude Desktop, and other MCP clients over stdio.

- **Protocol & source home:** [joinwell52-AI/FCoP](https://github.com/joinwell52-AI/FCoP)  
- **This package** lives in the same repo under `mcp/`.

> The **`fcop`** on PyPI **must** be the **FCoP library** (summary mentions *File-based Coordination Protocol*, `pyyaml`, no `fastmcp` inside `fcop`). If `pip show fcop` says *MCP toolbox* or `from fcop import Issue` fails, you have a **wrong** distribution — fix with a clean venv and reinstall (see *Verify* below).

---

## One-page install (what we recommend for customers)

**Goal:** a dedicated Python environment for MCP only, so no other project’s `.pth` or wrong `fcop` shadows the real library.

### A. Recommended: dedicated venv + `python -m fcop_mcp`

1. **Python 3.10+** on `PATH` (3.10–3.13 tested in CI; avoid very new 3.14 until CI covers it).
2. Create a venv (paths are examples — adjust if you like):

**Windows (PowerShell)**

```powershell
$v = "$env:USERPROFILE\.cursor\fcop_mcp_venv"
py -3.10 -m venv $v
& "$v\Scripts\pip.exe" install -U pip
& "$v\Scripts\pip.exe" install -U "fcop" "fcop-mcp"
```

**macOS / Linux**

```bash
VENV="$HOME/.cursor/fcop_mcp_venv"
python3 -m venv "$VENV"
"$VENV/bin/pip" install -U pip
"$VENV/bin/pip" install -U "fcop" "fcop-mcp"
```

3. **Cursor** user config — file:

- Windows: `%USERPROFILE%\.cursor\mcp.json`
- macOS / Linux: `~/.cursor/mcp.json`

Add or merge (use the **real** `python` path from step 2):

```json
{
  "mcpServers": {
    "fcop": {
      "command": "C:\\Users\\YOUR_USER\\.cursor\\fcop_mcp_venv\\Scripts\\python.exe",
      "args": ["-m", "fcop_mcp"]
    }
  }
}
```

On macOS, `command` is like `/Users/YOUR_USER/.cursor/fcop_mcp_venv/bin/python`.

4. **Fully restart Cursor** (or *Developer: Reload Window*), then open MCP and confirm `fcop` is connected.

**Why this path?** `uvx` (below) is convenient but **first run** can take a long time to download dependencies; some MCP hosts time out. A fixed venv avoids that and avoids **name conflicts** with other editable installs of `fcop` on the same machine.

---

### B. Alternative: `uvx fcop-mcp` (quickest to try, slower cold start)

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

Install [uv](https://docs.astral.sh/uv/) first. **First connection** may download many wheels — **wait** for it; don’t spam reconnect. If you see *Aborted* or timeouts, use **A** above.

---

## Verify (2 commands)

In the **same** venv you use for MCP:

```bash
python -c "from fcop import Issue, Project; print('fcop OK', Project)"
python -c "from fcop_mcp.server import mcp; print('fcop-mcp OK')"
```

If the first line fails, **`fcop` is not the FCoP library** — uninstall and reinstall in a **clean** venv (`fcop` / `fcop-mcp` from PyPI, versions `0.6.2+` in lockstep with the current release).

---

## Claude Desktop

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`  
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`  

Use the same `command` / `args` as Cursor (either **A** with your venv `python`, or **B** with `uvx`).

---

## Upgrading from `uvx` / `args: ["fcop"]` (0.5.x)

```json
"fcop": { "command": "uvx", "args": ["fcop-mcp"] }
```

The `mcpServers` key name can stay `"fcop"`. Full guide:  
[`docs/MIGRATION-0.6.md`](https://github.com/joinwell52-AI/FCoP/blob/main/docs/MIGRATION-0.6.md)

---

## Where the server looks for the project

Resolution order (see [ADR-0003](https://github.com/joinwell52-AI/FCoP/blob/main/adr/ADR-0003-stability-charter.md)):

1. Last `set_project_dir` in this MCP session  
2. `FCOP_PROJECT_DIR`  
3. Legacy 0.5.x env var `CODEFLOW_PROJECT_DIR` (still recognized with a deprecation warning — use `FCOP_PROJECT_DIR`)  
4. Walk up for `docs/agents/fcop.json` / `fcop-rules.mdc` / `docs/agents/tasks/`  
5. Current working directory  

To pin a folder in config:

```json
"env": { "FCOP_PROJECT_DIR": "D:/path/to/your/repo" }
```

---

## Stability (0.6.x)

Tool and resource **shapes** are **additive-only** within `0.6.x` ([stability charter](https://github.com/joinwell52-AI/FCoP/blob/main/adr/ADR-0003-stability-charter.md)). Configs that work on `fcop-mcp` `0.6.0+` should keep working on later `0.6.x` patch releases.

---

## License

MIT — see [`LICENSE`](../LICENSE).
