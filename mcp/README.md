# fcop-mcp — MCP adapter for FCoP

mcp-name: io.github.joinwell52-AI/fcop

`fcop-mcp` exposes the official [FCoP Python Core](https://pypi.org/project/fcop/)
to Codex, Cursor, Claude Desktop, and other MCP clients. It is an optional
adapter over the same protocol—not a second protocol implementation.

## Current stable surface

FCoP 4.0 is **Stable, Implemented and Released**. Package version **4.0.3** provides:

- **49 tools**
- **12 resources**
- **4 resource templates**
- Python 3.10–3.13 support
- Version-routed behavior for existing v3 and v4 workspaces

The original 46-tool surface remains available. The 4.0.1 Branch workflow adds:

| Tool | Purpose |
| --- | --- |
| `create_branch` | Create a Branch TASK under a Root TASK for parallel work |
| `inspect_family` | Read the Root/Branch family, REPORT heads, readiness, and canonical family digest |
| `merge_branches` | Commit an explicit convergence decision through Core's atomic merge operation |

## Install

Install Core and the MCP adapter together in a dedicated virtual environment:

```bash
python -m pip install --upgrade \
  "fcop>=4.0.3,<4.1.0" \
  "fcop-mcp>=4.0.3,<4.1.0"
```

Verify both distributions:

```bash
python -c "from importlib.metadata import version; print('fcop', version('fcop')); print('fcop-mcp', version('fcop-mcp'))"
python -c "from fcop_mcp.server import mcp; print('fcop-mcp ready')"
```

`fcop` and `fcop-mcp` are released in lockstep within the same minor line.
Do not mix incompatible minor versions.

## macOS (Intel and Apple silicon)

FCoP MCP supports both Intel and Apple silicon Macs; Rosetta is not required. With Python 3.10–3.13:

```bash
python3 -m venv ~/.local/share/fcop/venv
~/.local/share/fcop/venv/bin/python -m pip install --upgrade \
  "fcop>=4.0.3,<4.1.0" \
  "fcop-mcp>=4.0.3,<4.1.0"

~/.local/share/fcop/venv/bin/fcop version
~/.local/share/fcop/venv/bin/fcop doctor
~/.local/share/fcop/venv/bin/fcop tools --json
```

The installed CLI provides `init`, `status`, `inspect`, `validate`, `tools`, `doctor`, `version`, `spec`, and `migrate`. MCP additionally requires a client that supports local stdio servers. Configure the command as the absolute `/Users/.../.local/share/fcop/venv/bin/python` path, pass `["-m", "fcop_mcp"]`, and set `FCOP_PROJECT_DIR` to the actual project root.

## CLI — Local Setup, Inspect & Diagnose

**CLI = Setup + Observe + Diagnose; MCP = Work.**

| Command | Purpose |
| --- | --- |
| `fcop init` | Initialize an FCoP workspace |
| `fcop status` | View workspace status |
| `fcop inspect` | Inspect TASK / REPORT / ISSUE / REVIEW |
| `fcop validate` | Validate protocol structure |
| `fcop tools` | Inspect the installed MCP Tool Catalog |
| `fcop doctor` | Diagnose installation, environment and compatibility |
| `fcop version` | Show installed versions |
| `fcop spec` | Show specification / rule identity |
| `fcop migrate` | Explicitly migrate a legacy workspace; inspect the plan before apply |

### Install & Verify

In an activated Python 3.10+ environment:

```bash
python -m pip install fcop

fcop version
fcop doctor
fcop init --root ./my-project
fcop status --root ./my-project
fcop validate --root ./my-project
```

For the optional MCP Tool Catalog:

```bash
python -m pip install fcop-mcp

fcop tools
fcop tools merge_branches --json
```

Once installed, the CLI can initialize, inspect, validate and diagnose locally and offline.
`doctor` does not access the network or modify Host configuration. Package installation itself may need a package index; offline installation requires locally available packages.
The CLI does not perform `create_task`, approval, Branch, merge or authorization work operations; use MCP or the Python API for those.
Installing `fcop` does not create Host instruction files. Normal v4 workspace state belongs in `<project>/fcop/`, never in project-root `AGENTS.md`, `CLAUDE.md` or Cursor rules.
Existing atomic initialization staging and failed-initialization evidence are preserved; customer files are never cleaned up automatically.
`migrate` is a separate explicit legacy operation, not an automatic package-upgrade step.
`tools` requires the optional MCP package and never starts a server or installs it automatically.

[CLI reference](https://github.com/joinwell52-AI/FCoP/blob/main/docs/cli.md) · [中文 CLI 参考](https://github.com/joinwell52-AI/FCoP/blob/main/docs/cli.zh.md).

## Configure an MCP client

**CLI = Setup + Observe + Diagnose; MCP = Work.** Inspect this adapter's
authoritative Tool Catalog without starting a server:

```bash
pip install fcop-mcp==4.0.3
fcop version
fcop doctor
fcop tools
fcop tools merge_branches --json
```

The public `fcop_mcp.catalog.get_tool_catalog(name=None)` query returns fresh,
sorted name/disposition rows from `disposition.TOOLS`. It imports no MCP runtime,
does not start a server and does not duplicate handler signatures. Unknown names
raise `KeyError`. CLI Catalog, registry and real `tools/list` have equal sets;
4.0.3 does not add, remove or change any MCP work tool.

See the [CLI reference](https://github.com/joinwell52-AI/FCoP/blob/main/docs/cli.md).

A fixed virtual environment gives predictable startup and avoids importing a
different editable `fcop` package from another project.

```json
{
  "mcpServers": {
    "fcop": {
      "command": "/absolute/path/to/venv/bin/python",
      "args": ["-m", "fcop_mcp"],
      "env": {
        "FCOP_PROJECT_DIR": "/absolute/path/to/repository"
      }
    }
  }
}
```

On Windows, `command` is the virtual environment's
`Scripts\\python.exe`. Restart the MCP host after changing its configuration.

Installation only installs the packages. It does **not** initialize a workspace,
migrate existing files, deploy rules, publish anything, or modify another
application.

## Parallel Branch workflow

```text
create_branch → agents write REPORTs → inspect_family → merge_branches
```

A PM, coordinating agent, or authorized human supplies the convergence decision.
FCoP does not invent that decision. Core validates the exact REPORT heads and
family digest, uses a family-scoped cross-process lock, and records one durable
REVIEW. An exact retry is idempotent; a conflict fails without partial writes.

Core owns validation, persistence, locking, and recovery. The MCP adapter
validates the tool request and forwards it to the public Core API.

See the [Branch merge contract and example](https://github.com/joinwell52-AI/FCoP/blob/main/docs/branch-merge.md)
or the [Chinese version](https://github.com/joinwell52-AI/FCoP/blob/main/docs/branch-merge.zh.md).

## Authority and safety

Profile and evaluator authority must be adopted by the trusted application when
the server starts. A role name, TASK field, Profile document, or tool argument
does not grant authority by itself.

FCoP uses a local stdio transport by default. Relay support is an explicit
optional extra and is never activated merely because a WebSocket dependency or
environment variable is present.

## Package boundary

| Package | Responsibility |
| --- | --- |
| `fcop` | Protocol Core, filesystem model, validation, atomic persistence, and recovery |
| `fcop-mcp` | MCP tools and resources that call the Core API |

You need `fcop-mcp` when an MCP client must operate FCoP through tools. Python
applications using `Project` directly only need `fcop`.

## 中文简介

FCoP 4.0 已正式稳定发布，当前包版本为 4.0.3。
`fcop-mcp` 是 FCoP Core 的 MCP 适配层，当前提供 49 个 Tools、12 个
Resources 和 4 个 Templates。4.0.1 新增 `create_branch`、
`inspect_family`、`merge_branches`，让 MCP Host 能创建并发 Branch、
检查 REPORT 家族并提交原子合并。合并判断由 PM、Agent 或人类给出，Core
负责校验、落盘、幂等和崩溃恢复。

## Documentation

- [Authoritative install prompt (EN)](https://github.com/joinwell52-AI/FCoP/blob/main/src/fcop/rules/_data/agent-install-prompt.en.md)
- [权威安装提示词（中文）](https://github.com/joinwell52-AI/FCoP/blob/main/src/fcop/rules/_data/agent-install-prompt.zh.md)
- [Installation prompt MCP Resource](fcop://prompt/install)
- [Repository](https://github.com/joinwell52-AI/FCoP)
- [MCP tools reference](https://github.com/joinwell52-AI/FCoP/blob/main/docs/mcp-tools.md)
- [Protocol introduction](https://github.com/joinwell52-AI/FCoP/blob/main/docs/getting-started.en.md)
- [中文协议介绍](https://github.com/joinwell52-AI/FCoP/blob/main/docs/getting-started.md)
- [Branch merge](https://github.com/joinwell52-AI/FCoP/blob/main/docs/branch-merge.md)
- [Changelog](https://github.com/joinwell52-AI/FCoP/blob/main/CHANGELOG.md)
- [Historical upgrades](https://github.com/joinwell52-AI/FCoP/blob/main/docs/upgrade-fcop-mcp.md)

## License

MIT — [LICENSE](https://github.com/joinwell52-AI/FCoP/blob/main/LICENSE)
