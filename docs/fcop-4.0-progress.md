# FCoP 4.0 setup and version guide / 接入与版本指南

[English README](../README.md) · [中文 README](../README.zh.md) · [Architecture](architecture.en.md) · [架构说明](architecture.zh.md)

**Current stable pair: 4.0.2 / 当前稳定版组合：4.0.2。** Updated September 11, 2026. This page supersedes the pre-release development note formerly at this address.

Official distribution: [GitHub v4.0.2](https://github.com/joinwell52-AI/FCoP/releases/tag/v4.0.2) · [PyPI fcop 4.0.2](https://pypi.org/project/fcop/4.0.2/) · [PyPI fcop-mcp 4.0.2](https://pypi.org/project/fcop-mcp/4.0.2/).

## Recommended: ask your AI / 推荐：让 AI 安装

Copy the request in the [AI installation guide](ai-install.md) into a coding agent with terminal and file access. It performs the checks, installation, client configuration and a task verification. The steps below are its technical reference; you do not need to type them yourself.

将 [AI 安装说明](ai-install.md)里的指令交给能运行命令、修改文件的编程 AI，由它完成环境检查、安装、客户端配置和任务验收。下方是执行时的技术参考，你不需要自己逐条输入。

## Manual reference: fresh environment / 手动参考：新环境

Python 3.10+ is required. Create an environment in the directory where you want to install the tools:

需要 Python 3.10+。在准备安装工具的目录创建虚拟环境：

```sh
python -m venv .venv
```

Activate it using the command for your shell / 根据所用终端激活环境：

| Shell / 终端 | Command / 命令 |
|---|---|
| Windows Command Prompt | `.venv\Scripts\activate.bat` |
| Windows PowerShell | `.\.venv\Scripts\Activate.ps1` |
| macOS / Linux bash or zsh | `source .venv/bin/activate` |

Install the exact stable pair. Python-only users can omit `fcop-mcp`:

安装一致的稳定版组合；只通过 Python 使用时可省略 `fcop-mcp`：

```sh
python -m pip install "fcop==4.0.2" "fcop-mcp==4.0.2"
python -c "from importlib.metadata import version; print(version('fcop'), version('fcop-mcp'))"
```

Expected / 预期输出：`4.0.2 4.0.2`.

The adapter's dependency is `fcop>=4.0.2,<4.1.0`. The pinned pair above makes this example reproducible; do not combine it with a 3.x adapter or library.

适配器的依赖范围是 `fcop>=4.0.2,<4.1.0`。上方固定组合便于复现，不要与 3.x 适配器或库混用。

## Create and inspect work / 创建并检查工作

The [Python demo](../README.md#try-it) writes an actual TASK and reads it through a new client. For a retained workspace, replace the temporary root with a new directory you control, then call `Project(root).create_workspace(protocol_version="4.0")`. Use the returned `workspace_id` with `create_task`; keep a stable `operation_id` when retrying that creation request. Read the state through `inspect_state(task_id=...)`.

[Python 示例](../README.zh.md#try-it)会写入真实 TASK 并通过新客户端读取。需要保留工作区时，把临时根目录换成自己管理的新目录，再调用 `Project(root).create_workspace(protocol_version="4.0")`。创建任务时使用返回的 `workspace_id`；重试同一创建请求时保留 `operation_id`，通过 `inspect_state(task_id=...)` 读取状态。

For MCP, use the [README configuration](../README.md#mcp) with absolute executable and project paths. Initialize a new workspace with `init_solo(role_code="ME", protocol_version="4.0")`; the returned workspace identity is used by `create_task`. Inspect through `inspect_task(filename=task_id)`. Parameters are documented in the [tool reference](mcp-tools.md).

MCP 使用 [README 配置](../README.zh.md#mcp)中的可执行文件和项目绝对路径。通过 `init_solo(role_code="ME", protocol_version="4.0")` 初始化新工作区，使用返回的身份创建任务，再通过 `inspect_task(filename=task_id)` 检查。参数见[工具参考](mcp-tools.md)。

## Complete work with explicit authority / 配置授权后完成工作

Default `profiles: []` permits Base operations without authorization gates, including creation, claim and submission. Acceptance, rejection, reopening and archival require a usable adopted authorization Profile. Supply an issuer evaluator through the Python `Project(..., trusted_profiles=...)` boundary or the MCP host's `create_server(..., trusted_profiles=...)` initialization, and explicitly adopt the matching Profile in the workspace. Request payloads cannot register trust policies.

默认 `profiles: []` 可进行创建、领取、提交等不受授权门槛约束的 Base 操作。验收、退回、重开、归档需要可用且已采纳的授权 Profile。Python 通过 `Project(..., trusted_profiles=...)`、MCP 宿主通过 `create_server(..., trusted_profiles=...)` 的可信初始化入口提供签发者评估器，并在工作区显式采纳对应 Profile；请求载荷不能自行注册信任策略。

Working reference consumers / 完整参考使用方：

- [Python application](../tests/stable/third-party/python-only/app.py): lifecycle, evidence, authority, retry and branch scenarios.
- [MCP client](../tests/stable/third-party/mcp-only/client.py) and its [server](../tests/stable/third-party/mcp-only/server.py): the same boundaries through an external stdio client.

These samples deliberately use an educational issuer proof. Read their evaluator before adapting them; a production host must verify authority according to its own policy. The default CLI server does not invent that policy for you.

这些示例刻意采用教学用签发证明。改编前应阅读评估器，实际宿主需按自身策略验证权限；默认命令行服务不会代替你建立这种策略。

## Rules and existing workspaces / 规则与已有工作区

4.0 rules have versioned manifests, explicit adoption, zero-write deployment planning, receipts and rollback. Select an assembly and host projection using the [rule distribution contract](fcop-4.0/rule-distribution-contract.md) / [中文契约](fcop-4.0/rule-distribution-contract.zh.md). Files on disk and rules actually consumed by a host are separate facts.

4.0 规则提供版本化清单、显式采纳、零写入部署计划、回执与回滚。根据上方契约选择规则组合与宿主投影；磁盘上有文件，不代表宿主已经消费规则。

**Installing packages does not migrate a workspace.** Existing 3.x workspaces retain 3.x semantics. Do not use a fresh-workspace example to overwrite an existing workspace or treat old installation prompts as a 4.0 migration procedure. Retain backups and inspect the version-specific rules before planning a migration.

**安装包不会迁移工作区。** 已有 3.x 工作区保持 3.x 语义。不要用新建示例覆盖已有工作区，也不要把旧版安装提示词当成 4.0 迁移流程。规划迁移前保留备份并核对对应版本规则。

Legacy references / 历史资料：[3.x specification](../spec/fcop-v3-spec.md) · [中文规范](../spec/fcop-v3-spec.zh.md) · [3.x getting started](getting-started.en.md) · [中文入门](getting-started.md).

## Release and design history / 发布与设计记录

- **Current release:** [v4.0.2](https://github.com/joinwell52-AI/FCoP/releases/tag/v4.0.2), with accepted commit, artifact run and hashes. The [4.0.0 release document](releases/4.0.0.md) records the promotion procedure; the public release establishes publication.
- **Historical candidate:** [v4.0.0rc1](https://github.com/joinwell52-AI/FCoP/releases/tag/v4.0.0rc1) is retained. Candidate guides and WP reports describe their original stages.
- **Current contracts:** [4.0 specification EN](../spec/fcop-4.0-spec.md) / [ZH](../spec/fcop-4.0-spec.zh.md). C1–C8, rather than a historical concept count, define Core compatibility.
- **Research:** [Complete index EN](../essays/README.md) / [中文](../essays/README.zh.md). The existing 3.2.5 and April 2026 citation archives retain their historical versions; they do not identify 4.0.0.

当前发布页列出验收提交、构建与产物摘要。WP 报告和候选指南保留其原始阶段含义；当前 Core 兼容性以 C1–C8 为准。3.2.5 和 2026 年 4 月研究 DOI 保持原有版本含义，不能改写为 4.0.0 的引用凭证。
