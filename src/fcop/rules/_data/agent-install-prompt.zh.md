# 让 Agent 帮你装 fcop-mcp（标准提示词 / zh）

把下面整段话发给一个**新开的、能跑命令的 agent**（Cursor 里开新会话，
或者任何带 shell 工具的 AI），它会一步步把 `fcop-mcp` 装到 Cursor 里，
全程不用你自己动手。

> 这份提示词是 fcop 官方仓库 `src/fcop/rules/_data/agent-install-prompt.zh.md`
> 的内容，也作为 MCP 资源 `fcop://prompt/install` 暴露——同一份文本同时
> 用于 GitHub README、PyPI 项目页、给 agent 的人工指令。

---

## 复制下面这段，发给 Agent

```
帮我把 fcop-mcp 装到 Cursor，全程你来跑命令。要求：

1. 先识别我的系统：终端跑 `uname -s 2>$null; echo $env:OS` 看一眼是 Windows 还是 macOS / Linux。

2. 装 uv（如果还没有）。一行命令：
   - Windows PowerShell:
     powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   - macOS / Linux:
     curl -LsSf https://astral.sh/uv/install.sh | sh
   装完跑 `uvx --version` 确认。

3. 在全局 mcp.json 里加 fcop entry。**保留**已有的其他 mcp servers，不要覆盖：
   - Windows 路径：%USERPROFILE%\.cursor\mcp.json
   - macOS / Linux 路径：~/.cursor/mcp.json
   - 加到 mcpServers 对象里这一段：
     "fcop": {
       "command": "uvx",
       "args": ["fcop-mcp"]
     }

4. 把最终的 mcp.json 完整内容打印给我看。

5. 提醒我重启 Cursor；首次启动 fcop-mcp 会下载依赖，**等 30 秒到 1 分钟**，
   不要急着关掉或重连。

每完成一步报告结果再走下一步。装完后**不要**自动初始化项目——初始化是
我（ADMIN）的选择题，我会单独决定走 solo / dev-team / 自定义。
```

---

## 装完之后：初始化是 ADMIN 的选择题

`fcop-mcp` 装好以后，agent **不应该**自己 `init_project(team="dev-team")` —
- 团队是不是 4 人组？
- 还是 solo 一个人？
- 还是自定义角色？

这是 `ADMIN`（你）要决定的事情，不是 agent 的默认值。重启 Cursor 之后，新会话
里 agent 会先调 `fcop_report()`，输出会包含**三选一**清单——你选完，agent 才
能调对应的 `init_*` 工具。

更细的解读看仓库里的 `docs/agents/LETTER-TO-ADMIN.md`，那是 fcop 给 ADMIN
的完整说明书。
