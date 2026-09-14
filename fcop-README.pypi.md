# FCoP — Python Core

`fcop` is the official Python implementation of the **File-based Coordination
Protocol (FCoP)**. It gives agents and automation a durable, reviewable way to
coordinate work through UTF-8 Markdown files with YAML front matter.

This package is the protocol Core, Python API and thin CLI. The optional MCP adapter is
published separately as [`fcop-mcp`](https://pypi.org/project/fcop-mcp/).

**FCoP 4.0 is Stable, Implemented and Released.** The current package release
is **4.0.3**. The optional adapter provides **49 Tools / 12 Resources /
4 Templates**, including the official `create_branch`, `inspect_family`, and
`merge_branches` tools.

## Install

FCoP 4.0 supports Python 3.10–3.13.

```bash
python -m pip install --upgrade "fcop>=4.0.3,<4.1.0"
```

Verify the installed distribution:

```bash
python -c "from importlib.metadata import version; from fcop import Project; print(version('fcop'), Project)"
```

## What Core provides

- Workspace identity and versioned protocol behavior.
- Four durable envelope types: TASK, REPORT, ISSUE, and REVIEW.
- Explicit lifecycle, attempt, relation, and authorization records.
- Branch families for parallel work without overwriting the Root task.
- Explicit convergence with family inspection and atomic Branch merge.
- Durable idempotency, cross-process locking, and crash-safe recovery.
- Version-selected protocol rules and schemas.
- A typed Python `Project` API with no MCP, LLM, or network dependency.

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

## Minimal Python example

```python
from pathlib import Path

from fcop import Project

project = Project(Path("/absolute/path/to/repository"))
workspace = project.create_workspace(protocol_version="4.0")

print(workspace["workspace_id"])
```

Installing the package does **not** initialize a repository, migrate an existing
workspace, deploy rules, start an MCP server, or modify another application.

## Branch and merge

Parallel work is represented as a Root TASK with Branch TASKs. Agents produce
REPORTs on their assigned Branches; a PM or coordinating agent inspects the
family and supplies the convergence decision. Core verifies the referenced
heads and family digest, then records the merge as one durable REVIEW.

See the [Branch merge contract and example](https://github.com/joinwell52-AI/FCoP/blob/main/docs/branch-merge.md)
or the [Chinese version](https://github.com/joinwell52-AI/FCoP/blob/main/docs/branch-merge.zh.md).

## Package boundary

| Package | Responsibility |
| --- | --- |
| `fcop` | Protocol Core, Python API and setup/observe/diagnose CLI; no MCP dependency |
| `fcop-mcp` | Optional MCP stdio adapter exposing Core capabilities to MCP clients |

FCoP is not a task scheduler, agent runtime, LLM SDK, database, or automatic
merge-decision engine. It records and validates coordination decisions made by
the participating agents or humans.

## 中文简介

FCoP 4.0 已正式稳定发布，当前包版本为 4.0.3。
`fcop` 是 FCoP 协议的 Python Core，负责工作区、TASK/REPORT/ISSUE/REVIEW、
并发 Branch、显式收敛、原子合并、幂等与恢复。它不包含 MCP Server，也不会在
安装时自动初始化、迁移或修改现有项目。需要在 Codex、Cursor、Claude Desktop
等 MCP Host 中调用时，请另外安装 `fcop-mcp`。

## Documentation

- [Repository](https://github.com/joinwell52-AI/FCoP)
- [Protocol introduction](https://github.com/joinwell52-AI/FCoP/blob/main/docs/getting-started.en.md)
- [中文协议介绍](https://github.com/joinwell52-AI/FCoP/blob/main/docs/getting-started.md)
- [Branch merge](https://github.com/joinwell52-AI/FCoP/blob/main/docs/branch-merge.md)
- [MCP tools reference](https://github.com/joinwell52-AI/FCoP/blob/main/docs/mcp-tools.md)
- [Changelog](https://github.com/joinwell52-AI/FCoP/blob/main/CHANGELOG.md)
- [Historical migrations](https://github.com/joinwell52-AI/FCoP/tree/main/docs/releases)

## License

MIT — [LICENSE](https://github.com/joinwell52-AI/FCoP/blob/main/LICENSE)
