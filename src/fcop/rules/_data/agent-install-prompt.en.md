# Have an Agent Install fcop-mcp For You (canonical prompt / en)

Send the block below to a **fresh agent that can run shell commands**
(new Cursor chat, or any AI with terminal access). It will install
`fcop-mcp` into Cursor step by step, no manual work from you.

> This prompt is the source-of-truth in the fcop repo at
> `src/fcop/rules/_data/agent-install-prompt.en.md`, also exposed as the
> MCP resource `fcop://prompt/install` — the same text powers the GitHub
> README, the PyPI project page, and the human-readable instructions
> for agents.

---

## Copy the block below and send it to your agent

```
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

---

## After install: initialization is ADMIN's pick

Once `fcop-mcp` is installed, the agent **must not** default to
`init_project(team="dev-team")` —
- Is this a 4-person team?
- Or solo (single AI)?
- Or a custom roster?

That's `ADMIN`'s call (yours), not the agent's default. After Cursor
restarts, in a new chat the agent will first call `fcop_report()`,
whose output includes a **3-way choice**. You pick, then the agent
can invoke the matching `init_*` tool.

For the full reasoning, read `docs/agents/LETTER-TO-ADMIN.md` in your
project — that's fcop's complete manual for ADMIN.
