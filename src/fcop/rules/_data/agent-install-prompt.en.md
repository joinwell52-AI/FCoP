# Have an Agent Install fcop-mcp For You (canonical prompt / en)

Current FCoP 4.x prompt, returned verbatim by the package and MCP resource `fcop://prompt/install/en`. README and PyPI link here without duplicating it.

## Copy the block below and send it to your agent

```
Install FCoP for my chosen MCP client and report actual commands and results.

1. Confirm the OS, client and Python environment without guessing. Use Python
   3.10+ and run python -m pip install fcop-mcp in that environment.
   Verify installed fcop and fcop-mcp versions and compatibility.

2. Run fcop version, fcop doctor and fcop tools.
   CLI = Setup + Observe + Diagnose; MCP = Work.
   doctor works locally, does not access the network or modify Host configuration.
   Package installation itself may need network access.

3. Configure the chosen MCP client only when I explicitly request it. Use that
   environment's fcop-mcp executable and preserve the existing transport.
   Preserve existing mcpServers and settings; do not overwrite other entries.
   Do not print credentials or full secret-bearing configuration.
   Client configuration belongs to the application, not the FCoP workspace.

4. Reconnect the MCP client. If first launch is still resolving dependencies,
   allow 30 seconds to 1 minute; report errors instead of repeatedly reconnecting.
   Verify 49 tools, 12 resources and 4 resource templates, including merge_branches.

5. Do not auto-init or migrate a project. Initialization and the target directory
   are ADMIN's explicit choice. Once requested, use fcop init --root <project>
   for a new v4 workspace, then fcop status and fcop validate with the same --root.
   Never automatically migrate a legacy workspace.

6. Do not create, modify or delete AGENTS.md, CLAUDE.md, .cursor rules or other
   project-root Host instruction files. Existing files are customer-owned bytes.
   Normal v4 state lives under <project>/fcop/. Read package and MCP
   rules/protocol/guidance resources directly; do not deploy Host projections.
   redeploy_rules is Legacy v1-v3 only, not a v4 install or upgrade step.

7. Task, approval, Branch, merge and authorization work uses MCP or the Python
   API, not CLI. Stop after the installation report unless project work is
   separately authorized.
```

## Install & Verify

After installation, `fcop version`, `fcop doctor` and `fcop tools` check the local environment without initializing a workspace. After ADMIN explicitly selects a new project, run `fcop init --root ./my-project`, `fcop status --root ./my-project` and `fcop validate --root ./my-project`.

Read `fcop://rules`, `fcop://protocol` and `fcop://guidance/{sequential,parallel}/{en,zh}` without Host rule files. Historical v1-v3 team and deployment workflows remain legacy-only; package upgrades do not migrate workspaces.
