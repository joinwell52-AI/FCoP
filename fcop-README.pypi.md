# FCoP · Python Core

`fcop` is the official Python implementation of the **File-based Coordination
Protocol (FCoP)**. It records durable, reviewable coordination facts as UTF-8
Markdown documents with YAML front matter.

**Current version: 4.0.5.** This package is the protocol Core, Python API, and
local CLI. The optional [`fcop-mcp`](https://pypi.org/project/fcop-mcp/) package
is a thin adapter over this Core. Core remains the sole authority for protocol
facts, validation, state transitions, idempotency, locking, and recovery.

## Install

FCoP 4.0.5 supports Python 3.10–3.13.

```bash
python -m pip install "fcop==4.0.5"
```

Verify the installed distribution:

```bash
python -c "from importlib.metadata import version; from fcop import Project; print(version('fcop'), Project)"
```

## macOS (Intel and Apple silicon)

The same package supports Intel and Apple silicon Macs; Rosetta is not required. Install the CLI and optional MCP adapter together in a dedicated Python 3.10–3.13 environment:

```bash
python3 -m venv ~/.local/share/fcop/venv
~/.local/share/fcop/venv/bin/python -m pip install --upgrade \
  "fcop>=4.0.5,<4.1.0" \
  "fcop-mcp>=4.0.5,<4.1.0"

~/.local/share/fcop/venv/bin/fcop version
~/.local/share/fcop/venv/bin/fcop doctor
~/.local/share/fcop/venv/bin/fcop tools --json
```

The CLI provides `init`, `status`, `inspect`, `validate`, `tools`, `doctor`, `version`, `spec`, and `migrate`. MCP additionally requires a local-stdio-capable client. Use the absolute `/Users/.../.local/share/fcop/venv/bin/python` path with `args = ["-m", "fcop_mcp"]`, and set `FCOP_PROJECT_DIR` to the actual project root.

## Base Protocol boundary

FCoP Core provides:

- Workspace identity and versioned protocol behavior.
- Four durable envelope types: TASK, REPORT, ISSUE, and REVIEW.
- Explicit lifecycle, attempt, relation, evidence, and authorization records.
- Branch families, explicit convergence, and atomic Branch merge.
- Durable idempotency, cross-process locking, and crash-safe recovery.
- Version-selected protocol rules and schemas.
- A typed Python `Project` API with no MCP, LLM, Runtime, or network dependency.

Team models, Solo mode, ME or other fixed roles, seats, and Host sessions are
outside the Base Protocol. A Host, Profile, or Runtime may define such concepts,
but Core does not require them. Legacy compatibility is also a separate boundary
and does not redefine canonical 4.x behavior. FCoP Core can be used independently
of CodeFlowMu.

`init_workspace` and the matching Core workspace API initialize a pure FCoP v4
workspace. They do not create `AGENTS.md`, `CLAUDE.md`, Cursor rules, role files,
or session state.

## CLI — Setup, inspect, and diagnose

**CLI = Setup + Observe + Diagnose; MCP = Work.**

| Command | Purpose |
| --- | --- |
| `fcop init` | Initialize a pure FCoP workspace |
| `fcop status` | View workspace status |
| `fcop inspect` | Inspect TASK / REPORT / ISSUE / REVIEW |
| `fcop validate` | Validate protocol structure |
| `fcop tools` | Inspect the installed optional MCP catalog |
| `fcop doctor` | Diagnose installation, environment, and compatibility |
| `fcop version` | Show installed versions |
| `fcop spec` | Show specification and rule identity |
| `fcop migrate` | Explicitly plan or apply a legacy workspace migration |

Example:

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

Package installation does not initialize a repository, migrate a workspace,
deploy Host instructions, start an MCP server, or modify another application.
Canonical v4 workspace state belongs under `<project>/fcop/`.
`fcop doctor` does not access the network or modify Host configuration.

## Minimal Python example

```python
from pathlib import Path

from fcop import Project

project = Project(Path("/absolute/path/to/repository"))
workspace = project.create_workspace(protocol_version="4.0")
print(workspace["workspace_id"])
```

## Package boundary

| Package | Responsibility |
| --- | --- |
| `fcop` | Protocol Core, Python API, and setup/observe/diagnose CLI |
| `fcop-mcp` | Optional canonical MCP adapter exposing Core capabilities |

The 4.0.5 default MCP surface contains **25 Canonical MCP Tools** and **6
read-only Core Resources**. The
[MCP reference](https://github.com/joinwell52-AI/FCoP/blob/main/docs/mcp-tools.md)
is generated from its canonical manifest. Every entry from the historical
49-tool implementation surface has an explicit disposition in the
[4.0.5 migration guide](https://github.com/joinwell52-AI/FCoP/blob/main/docs/migration-4.0.5-mcp.md).

## 中文简介

FCoP 4.0.5 是 File-based Coordination Protocol 的官方 Python Core。
Core 是协议事实、校验和状态迁移的唯一权威；`fcop-mcp` 只是可选的薄适配层。
Base Protocol 不要求 Team、Solo、ME、seat 或 Host session，这些概念属于
Host、Profile 或 Runtime。Legacy compatibility 也不属于 canonical 4.x 路径。
`init_workspace` 初始化纯 FCoP v4 工作区，不生成 Host 指令或角色文件。
FCoP Core 可以脱离 CodeFlowMu 独立使用。

## Documentation

- [Repository](https://github.com/joinwell52-AI/FCoP)
- [Protocol introduction](https://github.com/joinwell52-AI/FCoP/blob/main/docs/getting-started.en.md)
- [中文协议入门](https://github.com/joinwell52-AI/FCoP/blob/main/docs/getting-started.md)
- [MCP tools reference](https://github.com/joinwell52-AI/FCoP/blob/main/docs/mcp-tools.md)
- [4.0.5 migration guide](https://github.com/joinwell52-AI/FCoP/blob/main/docs/migration-4.0.5-mcp.md)
- [Changelog](https://github.com/joinwell52-AI/FCoP/blob/main/CHANGELOG.md)

## License

MIT · [LICENSE](https://github.com/joinwell52-AI/FCoP/blob/main/LICENSE)
