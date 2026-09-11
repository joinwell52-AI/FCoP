# FCoP — Python Core

`fcop` is the official Python implementation of the **File-based Coordination
Protocol (FCoP)**. It gives agents and automation a durable, reviewable way to
coordinate work through UTF-8 Markdown files with YAML front matter.

This package is the protocol Core and Python API. The optional MCP adapter is
published separately as [`fcop-mcp`](https://pypi.org/project/fcop-mcp/).

## Install

FCoP 4.0 supports Python 3.10–3.13.

```bash
python -m pip install --upgrade "fcop>=4.0.1,<4.1.0"
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

FCoP 4.0.1 adds the public Core support used to inspect incomplete Branch
families and to commit a convergence decision atomically and idempotently.

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
| `fcop` | Protocol Core, filesystem model, validation, persistence, recovery, and Python API |
| `fcop-mcp` | Optional MCP stdio adapter exposing Core capabilities to MCP clients |

FCoP is not a task scheduler, agent runtime, LLM SDK, database, or automatic
merge-decision engine. It records and validates coordination decisions made by
the participating agents or humans.

## 中文简介

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
