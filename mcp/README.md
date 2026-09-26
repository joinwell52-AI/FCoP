# fcop-mcp · Canonical MCP adapter for FCoP

mcp-name: io.github.joinwell52-AI/fcop

`fcop-mcp` exposes the official [FCoP Python Core](https://pypi.org/project/fcop/)
to Codex, Cursor, Claude Desktop, and other MCP clients. It is a thin adapter
over Core, which remains the sole authority for protocol facts, validation,
state transitions, persistence, locking, and recovery.

**Current version: 4.0.5.** The default server exposes exactly **25 Canonical
MCP Tools** and **6 read-only Core Resources**. The tool registry is derived
from one canonical manifest. The resource registry projects versioned content
owned by Core.

## Install

Install the matching 4.0.5 package pair in a dedicated Python 3.10–3.13
environment:

```bash
python -m pip install "fcop==4.0.5" "fcop-mcp==4.0.5"
```

`fcop-mcp==4.0.5` declares `fcop>=4.0.5,<4.1.0`. Verify both distributions:

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
  "fcop>=4.0.5,<4.1.0" \
  "fcop-mcp>=4.0.5,<4.1.0"

~/.local/share/fcop/venv/bin/fcop version
~/.local/share/fcop/venv/bin/fcop doctor
~/.local/share/fcop/venv/bin/fcop tools --json
```

The installed CLI provides `init`, `status`, `inspect`, `validate`, `tools`, `doctor`, `version`, `spec`, and `migrate`. MCP additionally requires a client that supports local stdio servers. Configure the command as the absolute `/Users/.../.local/share/fcop/venv/bin/python` path, pass `["-m", "fcop_mcp"]`, and set `FCOP_PROJECT_DIR` to the actual project root.

For an isolated launcher:

```bash
uvx --from fcop-mcp==4.0.5 --with fcop==4.0.5 fcop-mcp --root /absolute/path/to/repository
```

## Canonical 4.0.5 surface

The workspace tools include `init_workspace`, `inspect_workspace`, and
`validate_workspace`. `create_task` is the canonical TASK creation entry.
Profiles are explicit extensions. Toolkit commands, compatibility shims,
packaging operations, Host configuration, Runtime services, and application
scaffolding are outside the default MCP registry.

Team models, Solo mode, ME or other fixed roles, seats, and Host sessions are
not Base Protocol prerequisites. The default server neither requires nor
creates them. `init_workspace` does not generate `AGENTS.md`, `CLAUDE.md`,
Cursor rules, role templates, or session state.

The prior inventory is the **historical 49-tool implementation surface**. It
is not the current MCP contract. Every historical tool has one disposition in
the [4.0.5 migration guide](https://github.com/joinwell52-AI/FCoP/blob/main/docs/migration-4.0.5-mcp.md).
For example, `write_task` is an opt-in deprecated Python compatibility shim,
and `fcop_audit` is a Toolkit CLI command. Neither appears in default
`tools/list`.

See the generated
[MCP tools reference](https://github.com/joinwell52-AI/FCoP/blob/main/docs/mcp-tools.md)
for all 25 names, descriptions, and input schemas.

## Configure an MCP client

A fixed virtual environment gives predictable startup and avoids importing a
different editable package from another project.

```json
{
  "mcpServers": {
    "fcop": {
      "command": "/absolute/path/to/venv/bin/python",
      "args": ["-m", "fcop_mcp", "--root", "/absolute/path/to/repository"]
    }
  }
}
```

On Windows, `command` is the virtual environment's `Scripts\\python.exe`.
Restart the MCP host after changing its configuration.

Installation only installs packages. It does not initialize or migrate a
workspace, deploy rules, modify Host instructions, or configure another
application.

## CLI — Setup, inspect, and diagnose

**CLI = Setup + Observe + Diagnose; MCP = Work.**

| Command | Purpose |
| --- | --- |
| `fcop init` | Initialize a pure FCoP workspace |
| `fcop status` | View workspace status |
| `fcop inspect` | Inspect TASK / REPORT / ISSUE / REVIEW |
| `fcop validate` | Validate protocol structure |
| `fcop tools` | Inspect the installed MCP catalog |
| `fcop doctor` | Diagnose installation, environment, and compatibility |
| `fcop version` | Show installed versions |
| `fcop spec` | Show specification and rule identity |
| `fcop migrate` | Explicitly plan or apply a legacy workspace migration |

```bash
python -m pip install fcop
fcop version
fcop doctor
fcop init --root ./my-project
fcop status --root ./my-project
fcop validate --root ./my-project

python -m pip install fcop-mcp
fcop tools
fcop tools merge_branches --json
```

The local CLI operates without starting MCP. `fcop tools` reads this adapter's
canonical catalog without starting a server. Work operations such as
`create_task`, lifecycle transitions, Branch merge, and authorization use MCP
or the Python API. Canonical v4 workspace state belongs under `<project>/fcop/`.
`fcop doctor` does not access the network or modify Host configuration.

## Authority and package boundary

An optional authorization Profile and evaluator must be supplied by the trusted
application. A role name, TASK field, Profile document, or tool argument does
not grant authority by itself.

| Package | Responsibility |
| --- | --- |
| `fcop` | Protocol Core, validation, atomic persistence, and recovery |
| `fcop-mcp` | 25 canonical MCP tools and 6 read-only Core resources |

FCoP uses local stdio by default. Relay support is an explicit optional extra.
Python applications that use `Project` directly only need `fcop`.

## 中文简介

`fcop-mcp` 4.0.5 是 FCoP Core 的薄 MCP 适配层。默认服务精确提供
**25 个 Canonical MCP Tools**和 **6 个只读 Core Resources**。
Core 是协议事实和状态迁移的唯一权威。Team、Solo、ME、seat、Host session、
Profile、Toolkit、Compatibility 与 Runtime 都不会成为 Base Protocol 的默认前置条件。
历史 49 工具实现面的每个入口均已在 4.0.5 迁移指南中给出明确去向。

## Documentation

- [Repository](https://github.com/joinwell52-AI/FCoP)
- [Authoritative install prompt (English)](https://github.com/joinwell52-AI/FCoP/blob/main/src/fcop/rules/_data/agent-install-prompt.en.md)
- [权威安装提示词（中文）](https://github.com/joinwell52-AI/FCoP/blob/main/src/fcop/rules/_data/agent-install-prompt.zh.md)
- [Installation prompt MCP Resource](fcop://prompt/install)
- [MCP tools reference](https://github.com/joinwell52-AI/FCoP/blob/main/docs/mcp-tools.md)
- [4.0.5 migration guide](https://github.com/joinwell52-AI/FCoP/blob/main/docs/migration-4.0.5-mcp.md)
- [Protocol introduction](https://github.com/joinwell52-AI/FCoP/blob/main/docs/getting-started.en.md)
- [中文协议入门](https://github.com/joinwell52-AI/FCoP/blob/main/docs/getting-started.md)
- [Changelog](https://github.com/joinwell52-AI/FCoP/blob/main/CHANGELOG.md)

## License

MIT · [LICENSE](https://github.com/joinwell52-AI/FCoP/blob/main/LICENSE)
