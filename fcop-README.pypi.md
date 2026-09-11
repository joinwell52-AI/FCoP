# FCoP — Python Core

`fcop` is the official Python implementation of the **File-based Coordination
Protocol (FCoP)**. It gives agents and automation a durable, reviewable way to
coordinate work through UTF-8 Markdown files with YAML front matter.

This package is the protocol Core, Python API and thin CLI. The optional MCP adapter is
published separately as [`fcop-mcp`](https://pypi.org/project/fcop-mcp/).

**FCoP 4.0 is Stable, Implemented and Released.** The current package release
is **4.0.2**. The optional adapter provides **49 Tools / 12 Resources /
4 Templates**, including the official `create_branch`, `inspect_family`, and
`merge_branches` tools.

## Install

FCoP 4.0 supports Python 3.10–3.13.

```bash
python -m pip install --upgrade "fcop>=4.0.2,<4.1.0"
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

## CLI v1: Setup + Observe + Diagnose

FCoP 4.0.2 provides nine commands: `init`, `status`, `inspect`, `validate`,
`tools`, `doctor`, `version`, `spec`, `migrate`.
**CLI = Setup + Observe + Diagnose; MCP = Work.**

```bash
pip install fcop==4.0.2
fcop version
fcop doctor
fcop init
fcop status
```

Use `--root <path>` for workspace commands. The eight non-migration commands
support `--json`; `fcop --help` discovers the full surface. Observe/diagnose
commands never fix, repair, migrate, create work records or configure a Host.
Only explicit `init` and migration `--apply` may write. Bare `fcop` retains
its historical migration guidance and exit 1; use `fcop --help` for help.

Exit codes: 0 success/valid, 1 internal failure, 2 invalid data/input,
3 unavailable/unsupported. An absent optional MCP package is reported explicitly
by `tools`; Core remains independently usable. `doctor` warns, not installs it.

[CLI reference](https://github.com/joinwell52-AI/FCoP/blob/main/docs/cli.md) /
[中文 CLI 参考](https://github.com/joinwell52-AI/FCoP/blob/main/docs/cli.zh.md).

For MCP work, install `fcop-mcp==4.0.2` in the same environment and use its
[client configuration and verification guide](https://pypi.org/project/fcop-mcp/4.0.2/).
Point the client at that environment's Python with `-m fcop_mcp` and explicitly
set `FCOP_PROJECT_DIR`; run `fcop tools` to inspect the installed Tool Catalog.

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

FCoP 4.0 已正式稳定发布，当前包版本为 4.0.2。
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
