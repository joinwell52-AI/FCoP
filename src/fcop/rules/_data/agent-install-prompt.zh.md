# 让 Agent 帮你装 fcop-mcp（标准提示词 / zh）

本文件为当前 FCoP 4.x 提示词，包内访问器及 MCP 资源 `fcop://prompt/install` 逐字返回正文。README 与 PyPI 只链接这里，不复制正文。

## 复制下面这段，发给 Agent

```
为我选择的 MCP 客户端安装 FCoP，汇报实际命令与结果。

1. 先确认操作系统、客户端与 Python 环境，不得猜测。使用 Python 3.10+，
   在该环境运行 python -m pip install fcop-mcp。
   核验 fcop、fcop-mcp 已安装版本及兼容性。

2. 运行 fcop version、fcop doctor、fcop tools。
   CLI = Setup + Observe + Diagnose；MCP = Work。
   doctor 本地运行，不联网、不修改 Host；安装包本身可能需要联网。

3. 只有我明确要求配置所选 MCP 客户端时，才进行配置。
   使用该环境的 fcop-mcp 可执行文件，保留现有传输方式。
   保留已有 mcpServers 与设置，不要覆盖其他条目。
   不得打印凭据或包含秘密的完整配置。
   客户端配置属于应用，不属于 FCoP workspace。

4. 重新连接 MCP 客户端。首次启动若仍在解析依赖，等 30 秒到 1 分钟；
   出错如实报告，不反复重连。核验 49 tools、12 resources、
   4 resource templates，确认包含 merge_branches。

5. 不要自动初始化或迁移项目。初始化及目标目录由 ADMIN 明确选择。
   获准创建新的 v4 workspace 后，运行 fcop init --root <project>，
   随后以同一个 --root 运行 fcop status 与 fcop validate。
   不得自动迁移旧 workspace。

6. 不得创建、修改或删除 AGENTS.md、CLAUDE.md、.cursor 规则或其他
   项目根 Host 指令文件；已有文件是客户拥有的字节。
   v4 正常状态位于 <project>/fcop/。直接读取包内规则及 MCP
   rules/protocol/guidance 资源，不部署 Host 投影。
   redeploy_rules 仅供 Legacy v1-v3，不是 v4 安装或升级步骤。

7. TASK、审批、Branch、merge、authorization 工作由 MCP 或 Python API
   承担，不由 CLI 承担。提交安装报告后停止，除非项目工作已单独授权。
```

## 安装后快速自检

安装后用 `fcop version`、`fcop doctor`、`fcop tools` 检查本地环境，不会初始化 workspace。ADMIN 明确选定新项目后，运行 `fcop init --root ./my-project`、`fcop status --root ./my-project`、`fcop validate --root ./my-project`。

通过 `fcop://rules`、`fcop://protocol`、`fcop://guidance/{sequential,parallel}/{en,zh}` 读取规则，无需 Host 规则文件。历史 v1-v3 团队及部署流程仅为 Legacy 兼容；安装新版包不会迁移旧 workspace。
