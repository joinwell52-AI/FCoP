# 升级 `fcop` / `fcop-mcp`（0.6.x 小版本）

面向**已经**在用 PyPI 上 `fcop` 与/或 `fcop-mcp` 的用户。从 **0.5.x** 跨大版本请先看 [MIGRATION-0.6.md](./MIGRATION-0.6.md)。

## 原则

- 两包**同一大版本线齐发**（如 `0.6.2`），见 [ADR-0002](../adr/ADR-0002-package-split-and-migration.md)。日常升级**建议一起升**，避免只升其一导致依赖不对齐。
- **0.6.x 内** MCP 工具形态**只增不改**（[ADR-0003](../adr/ADR-0003-stability-charter.md)），升级后一般**不必**改 `mcp.json` 结构，除非换启动方式（如 `uvx` ↔ 固定 venv 的 `python -m`）。

## 用 pip（推荐，与 `mcp.json` 里使用的 Python 同一 venv）

在**你运行 MCP 的那个环境**里执行：

```bash
pip install -U "fcop" "fcop-mcp"
```

若需钉到当前小版本，例如 0.6.2（把数字换成你需要的版本）：

```bash
pip install -U "fcop==0.6.2" "fcop-mcp==0.6.2"
```

## 用 uvx 启动的

- `uvx` 会解析并拉取；若首连慢或缓存异常，以 [mcp/README.md](../mcp/README.md) 为准，可考虑改为**独立 venv + `python -m fcop_mcp`**，之后只在 venv 里用 `pip install -U` 升级，行为更稳。

## 升级后

1. **完全重开** Cursor 或 *Developer: Reload Window*，让 MCP 加载新装包。
2. 自检（与 mcp 文档一致）：

```bash
python -c "from fcop import Project; print('fcop OK', Project)"
python -c "from fcop_mcp.server import mcp; print('fcop-mcp OK')"
```

## 升级协议规则文件（0.6.3+ 必读）

`fcop-mcp` wheel 里**始终捆绑**最新版的 FCoP 协议规则——
`fcop-rules.mdc`、`fcop-protocol.mdc`、`AGENTS.md`、`CLAUDE.md` 四份。
**但 `pip install -U` 只更新 wheel 里的副本**，**不会自动改写**你项目根
目录的旧文件。两边因此可能漂移。

从 0.6.3 起：

- 升级后第一次进 IDE，让 ADMIN（你自己）调一次新工具
  **`fcop_report`**。报告头部的 `[Versions]` / `[版本]` 段会显示

  ```
  [版本]
    fcop-mcp:  0.6.3
    fcop:      0.6.3
    rules:     local 1.5.0 | packaged 1.5.0 ✓
    protocol:  local 1.4.0 | packaged 1.4.0 ✓
  ```

  四行 `✓` 即对齐；任一行变成 `本地偏旧 / OUTDATED` 即漂移。
- 漂移时报告末尾会贴一句 ADMIN 提示：让 ADMIN 调
  **`redeploy_rules`** 一次。该工具会把四份规则 host-neutral 地写
  到项目根（Cursor 看 `.cursor/rules/*.mdc`，Codex CLI 看
  `AGENTS.md`，Claude Code 看 `CLAUDE.md`）。旧文件先归档到
  `.fcop/migrations/<时间戳>/rules/`，再覆写。
- `redeploy_rules` 是 **ADMIN-only** 工具：agent 不应主动调，只在 ADMIN
  在聊天框里明确说"请重部署规则"或读到 `fcop_report` 里的提示并征
  得 ADMIN 同意后再调。

> Library 用户对应的 API：`Project.deploy_protocol_rules(force=True, archive=True)`
> 和 `Project.init(deploy_rules=True)`。背景见
> [ADR-0006](../adr/ADR-0006-host-neutral-rule-distribution.md)。

## `unbound_report` → `fcop_report`（0.6.3 改名）

旧工具 `unbound_report` 在 0.6.3 起改名为 **`fcop_report`**：它本就是
项目状态/初始化报告的通用入口，不局限于"未绑定角色"的提醒。

- 0.6.3：`unbound_report` 仍可调，但每次调用都会发出
  `DeprecationWarning("unbound_report is deprecated; use fcop_report instead.
  This alias will be removed in fcop-mcp 0.7.0. See ADR-0006 for the rationale.")`。
  返回内容与 `fcop_report` **逐字节相同**——只是名字过渡期。
- **0.7.0 起**：`unbound_report` 从工具表里删除。届时 system prompt 里
  仍写老名字的会话会拿到 "tool not found"。

迁移操作（一次性即可）：把你项目里的 system prompt / 角色模板 /
`LETTER-TO-ADMIN.md` / 内部说明文档里所有 `unbound_report` 字面量替
换为 `fcop_report`。例如：

```bash
# 自检：哪些文件还在提 unbound_report
grep -rn "unbound_report" docs/ .cursor/ AGENTS.md CLAUDE.md
```

仓库内 0.6.3 已统一改完，所以你只需要改**你自己**项目里曾经从我们
模板复制过去的副本。

## 发版与 PyPI 说明

- 维护者发版流程、tag 与 CI 见 [release-process.md](./release-process.md)。  
- 各版本变更摘要见 [CHANGELOG.md](../CHANGELOG.md) 与 `docs/releases/*.md`。

## English (short)

- Bump **both** `fcop` and `fcop-mcp` in the same venv: `pip install -U "fcop" "fcop-mcp"`.  
- Full install paths and `mcp.json` templates: [mcp/README.md](../mcp/README.md).
