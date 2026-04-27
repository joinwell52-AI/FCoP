# fcop-mcp

**MCP (stdio) server** — the optional **IDE bridge** for the same FCoP stack. It
wraps the official [`fcop`](https://pypi.org/project/fcop/) library; it is **not**
a second “FCoP product” and does not replace the protocol text.

- **What FCoP is (protocol only, product-agnostic):** [`docs/fcop-standalone.en.md`](../docs/fcop-standalone.en.md) (中文 [`fcop-standalone.md`](../docs/fcop-standalone.md))  
- **Pure Python lib / `pip install fcop`:** filesystem + Project API, PyYAML only — [PyPI `fcop`](https://pypi.org/project/fcop/) (see that package’s `description` and **Documentation**).  
- **This package (`fcop-mcp`):** `pip install fcop-mcp` — stdio tools/resources for clients; same repo, folder `mcp/`.  
- **Source home:** [joinwell52-AI/FCoP](https://github.com/joinwell52-AI/FCoP)

**Already on `0.6.x` and just upgrading?** See [**`docs/upgrade-fcop-mcp.md`**](https://github.com/joinwell52-AI/FCoP/blob/main/docs/upgrade-fcop-mcp.md) (`pip install -U` both `fcop` and `fcop-mcp` in the MCP venv, then restart the IDE; **0.6.3+** also documents how to refresh on-disk protocol rule files via `redeploy_rules`).

**What can the server actually do?** The 26 MCP tools and 12 read-only resources are indexed (with grouping, when-to-call, and parameter cheatsheet) in [**`docs/mcp-tools.md`**](https://github.com/joinwell52-AI/FCoP/blob/main/docs/mcp-tools.md). Authoritative descriptions remain in source docstrings ([`mcp/src/fcop_mcp/server.py`](https://github.com/joinwell52-AI/FCoP/blob/main/mcp/src/fcop_mcp/server.py)). **0.6.4** adds 2 new resources (`fcop://prompt/install` zh + en) and gives every `init_*` tool a `force` parameter for clean ADMIN-driven team switches. **0.6.5** wires the **Rule 0.a.1 hard constraint** (`task → do → report → archive` four-step cycle) into the tool layer: `new_workspace` prepends a soft Rule 0.a.1 reminder when no open `TASK-*.md` mentions the slug, and `fcop_report` (initialised branch) ends with the explicit four-step template — both bilingual, both additive (no signature changes). See [`docs/releases/0.6.5.md`](https://github.com/joinwell52-AI/FCoP/blob/main/docs/releases/0.6.5.md).

**0.6.3 ships [ADR-0006](https://github.com/joinwell52-AI/FCoP/blob/main/adr/ADR-0006-host-neutral-rule-distribution.md)** — host-neutral protocol-rule distribution. New tool **`fcop_report`** is now the canonical session/init report (its header carries a `[Versions]` block that flags drift between the wheel-bundled rules and the project-local `.cursor/rules/` copy). New ADMIN-only tool **`redeploy_rules`** writes the four protocol-rule targets — `.cursor/rules/fcop-rules.mdc`, `.cursor/rules/fcop-protocol.mdc`, `AGENTS.md`, `CLAUDE.md` — so Cursor, Claude Code CLI, and Codex CLI all see the same rules. Legacy **`unbound_report`** stays as a deprecated alias of `fcop_report` (emits `DeprecationWarning`, removed in 0.7.0). See [`docs/releases/0.6.3.md`](https://github.com/joinwell52-AI/FCoP/blob/main/docs/releases/0.6.3.md) for the full migration story.

> The **`fcop`** on PyPI **must** be the **FCoP library** (summary mentions *File-based Coordination Protocol*, `pyyaml`, no `fastmcp` inside `fcop`). If `pip show fcop` says *MCP toolbox* or `from fcop import Issue` fails, you have a **wrong** distribution — fix with a clean venv and reinstall (see *Verify* below).

---

## TL;DR — Have an agent install fcop-mcp for you

Don't want to read the rest of this page? Open a fresh chat with any
shell-capable AI agent (Cursor with a new tab, Claude Code CLI, Codex
CLI…) and **paste this prompt verbatim**. The agent will detect your
OS, install `uv`, edit your `~/.cursor/mcp.json` (preserving every
other server you already have), and tell you when to restart.

```text
Install fcop-mcp into Cursor for me — you run the commands end to end.

1. Detect my OS first: in the terminal, run
   `uname -s 2>$null; echo $env:OS` to see whether this is Windows
   or macOS / Linux.

2. Install uv (if not already present). One-liner:
   - Windows PowerShell:
     powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   - macOS / Linux:
     curl -LsSf https://astral.sh/uv/install.sh | sh
   Then run `uvx --version` to confirm.

3. Add an fcop entry to the global mcp.json. **Preserve** existing
   mcpServers — do not overwrite them.
   - Windows path: %USERPROFILE%\.cursor\mcp.json
   - macOS / Linux path: ~/.cursor/mcp.json
   - Add this snippet inside the mcpServers object:
     "fcop": {
       "command": "uvx",
       "args": ["fcop-mcp"]
     }

4. Print the final mcp.json contents back to me.

5. Remind me to restart Cursor; on first launch fcop-mcp will pull
   dependencies, **wait 30 seconds to 1 minute**, do not close or
   reconnect early.

Report back after each step before moving on. **Do not** auto-init
a project after install — initialization is my (ADMIN's) choice; I
will pick solo / dev-team / custom myself.
```

中文版本 / Chinese version: see
[`agent-install-prompt.zh.md`](https://github.com/joinwell52-AI/FCoP/blob/main/src/fcop/rules/_data/agent-install-prompt.zh.md)
in the repo, or after install read the MCP resource
`fcop://prompt/install`.

> **Why the "do not auto-init" line?** Initialisation is ADMIN's
> three-way choice (`solo` / preset team / custom). 0.6.3 had agents
> defaulting to `init_project(team="dev-team")`, which silently
> overwrote ADMIN's intended Solo flow. 0.6.4 makes the prompt and
> the `fcop_report` Phase-1 message say the choice out loud and
> forbid the agent from picking on ADMIN's behalf.

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

If the first line fails, **`fcop` is not the FCoP library** — uninstall and reinstall in a **clean** venv (`fcop` / `fcop-mcp` from PyPI, same `0.6.x` minor in lockstep with the current release).

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
