# Let your AI install FCoP / 让 AI 帮你安装 FCoP

[English README](../README.md#ai-install) · [中文 README](../README.zh.md#ai-install)

Current guide: **fcop 4.0.2 + fcop-mcp 4.0.2**, checked September 11, 2026.

Use a coding agent with terminal and file access, such as Cursor Agent or Codex. Paste a request below; the agent performs the setup. A chat-only assistant cannot install software on your computer.

使用能运行命令、修改文件的编程 AI，例如 Cursor Agent 或 Codex。复制下方指令，安装操作由 AI 完成；只有聊天能力、无法访问电脑的助手不能代装。

## Copy to your AI / 复制给 AI

### 中文

```text
请为我当前使用的 AI 编程客户端和项目安装 FCoP，按这份说明操作：
https://github.com/joinwell52-AI/FCoP/blob/main/docs/ai-install.md
环境检查、安装、配置和验收都由你执行。保留我现有的配置和项目状态。完成后告诉我实际验证结果；只在缺少客户端/项目选择，或确实需要授权、重连时让我介入。
```

### English

```text
Install FCoP for the coding client and project I am using. Follow:
https://github.com/joinwell52-AI/FCoP/blob/main/docs/ai-install.md
Run the environment checks, installation, configuration and verification yourself. Preserve my existing configuration and project state. Report what actually works; ask me only for a missing client/project choice or a required approval/reload.
```

## Execution guide for the AI / 给 AI 的执行说明

### 1. Inspect the current environment / 检查当前环境

Identify the OS, shell, coding client, target project, existing FCoP state, Python and uv availability. Use the user's current client and project when known. Ask only when a missing choice would change the installation target. If an appropriate newer stable version already exists, check its versioned documentation rather than downgrade it to this guide's pin.

确认系统、终端、客户端、目标项目、已有 FCoP 状态，以及 Python/uv 是否可用。已有会话信息足够时直接使用；只有无法确定安装目标才问用户。若已装了合适的较新稳定版，先核对其版本说明，避免为了匹配本页而降级。

### 2. Install in an isolated environment / 在隔离环境安装

If uvx is available, use this stdio launch command; it resolves the exact pair in an isolated environment:

```text
uvx --from fcop-mcp==4.0.2 --with fcop==4.0.2 fcop-mcp
```

This command starts a server awaiting MCP messages; it is not a command that should immediately print a success message and exit. Validate it with an MCP client and close the test process afterward.

When Python 3.10+ is available without uv, an isolated venv with the exact pair is also supported. Use its Python executable directly, so shell activation is unnecessary:

```text
python -m venv <new-install-directory>
<venv-python> -m pip install "fcop==4.0.2" "fcop-mcp==4.0.2"
<venv-python> -c "from importlib.metadata import version; print(version('fcop'), version('fcop-mcp'))"
```

Use a new directory, not another project's existing environment. On Windows the executable is Scripts/python.exe; on macOS/Linux it is bin/python. If the runtime is missing, perform the appropriate installation from the [official uv instructions](https://docs.astral.sh/uv/getting-started/installation/) within the client's permissions, then verify the executable path. Do not give the user a command list as the completed installation.

已有 uvx 时使用上方固定双包启动命令；它会自动准备隔离环境。这个进程会等待 MCP 消息，应通过 MCP 客户端验收，随后关闭测试进程，不能因为没有立即退出就判失败。

只有 Python 3.10+ 时，可以新建独立 venv 并安装同版本双包，直接调用虚拟环境里的 Python，无需让用户手工激活终端。缺少运行环境时，由 AI 按官方 uv 说明完成适合当前系统的安装并验证路径。检查和安装都实际执行，不能把一串命令交回用户就算完成。

### 3. Configure the actual client / 配置实际使用的客户端

Use an absolute executable path when the client's PATH differs from the terminal. Set FCOP_PROJECT_DIR to the chosen project root, not the FCoP source checkout. Preserve other servers and settings; retain a private backup before changing an existing configuration. Summarize only the relevant changes and redact secrets.

- **Cursor:** merge the FCoP entry into the project's .cursor/mcp.json, or the user-level configuration when that scope was requested. Use the [current FCoP client examples](https://joinwell52-ai.github.io/FCoP/#cursor) and [Cursor MCP documentation](https://cursor.com/docs/context/mcp).
- **Codex:** use a project-scoped .codex/config.toml for a trusted project, or the requested user-level configuration. The official `codex mcp add` command can register a stdio server; `codex mcp list` checks its configuration. Configuration listing alone does not establish a live connection. See the [current FCoP examples](https://joinwell52-ai.github.io/FCoP/#codex) and [official MCP configuration guide](https://learn.chatgpt.com/docs/extend/mcp?surface=cli).
- **Another client:** follow its official MCP configuration format rather than applying Cursor's JSON to every host.

客户端的 PATH 与终端不一致时使用可执行文件绝对路径。FCOP_PROJECT_DIR 指向已选项目根目录。合并配置时保留其他服务和设置，修改前保留本地备份；回报相关变更即可，不打印其他服务的密钥。根据实际客户端选择格式：Cursor 使用 mcp.json，Codex 使用 config.toml，不能混用。

### 4. Verify installation, connection and a real task / 验证安装、连接与真实任务

Check these outcomes separately:

1. **Installed:** verify the resolved fcop and fcop-mcp versions. For the pinned 4.0.2 pair, MCP discovery exposes 49 tools, 12 resources and 4 resource templates.
2. **Connected:** confirm FCoP tools are available in the user's actual coding client and perform an appropriate read-only call. If a reload is needed, report “configured; client reconnection pending,” give the single required step, and continue verification after reconnection. A separate stdio probe proves the server works, not that the user's client has connected.
3. **Task verified:** create a new isolated example directory and run the [create-and-read example](../README.md#try-it), or a corresponding MCP example after reading its tool schemas. Verify the stored task and its identity from a fresh reader. Keep the result or a concise verification receipt. Installation of the packages is not evidence of this task check.

分别回报“包已安装”“客户端已连接”“示例已验证”。4.0.2 的工具清单应为 49/12/4；配置文件已写好不等于客户端已连接。如果当前会话需要重连，明确标为待重连，告诉用户具体一步，重连后继续验收。独立 MCP 进程验证不能冒充当前客户端已经能用。

在独立新目录中运行“创建任务—重新读取”的真实示例，不改写已有业务项目的状态。现有 3.x 工作区保持原状；迁移、团队角色选择与规则部署依照用户目标另行处理。报告写了 done 也不等于审查已批准。

### 5. Give a short result / 交付简短结果

Report the actual versions, configuration scope/path, connection status, task-check result, retained evidence location, and any remaining user step. Act on permissions already granted. If the host requires an approval or reload that the AI cannot perform, identify exactly that action.

最后给出实际版本、配置范围与路径、连接状态、示例结果、证据位置，以及尚需用户操作的具体一步。已有授权不重复询问；只有宿主确实要求用户批准或重连时才交给用户处理。

## Technical and historical references / 技术与历史资料

- [Manual installation and 4.0 workspace guidance](fcop-4.0-progress.md)
- [MCP tool reference](mcp-tools.md)
- [4.0 rule distribution](fcop-4.0/rule-distribution-contract.md) / [中文](fcop-4.0/rule-distribution-contract.zh.md)

The bundled resources fcop://prompt/install and fcop://prompt/install/en still contain legacy installation material in the published 4.0.2 package. This document is the current website/repository installation guide. Use the linked 4.0 contracts for initialization and rule deployment.

已发布 4.0.2 包内的 fcop://prompt/install 等资源仍是旧版安装资料。本页是当前网站与仓库的安装说明，初始化和规则部署以链接的 4.0 契约为准。
