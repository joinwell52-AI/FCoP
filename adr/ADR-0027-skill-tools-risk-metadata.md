# ADR-0027: Skill.tools[] — MCP 工具风险元数据

- **Status**: Accepted
- **Date**: 2026-05-10
- **Deciders**: ADMIN
- **Related**: [ADR-0021](./ADR-0021-encoding-abstraction.md), [ADR-0024](./ADR-0024-task-risk-level.md), [Issue #2](https://github.com/joinwell52-AI/FCoP/issues/2)

## TL;DR

**中文**：在 `fcop.json` 的 `skills[]` 记录中新增 `tools[]` 子数组，允许 Skill 声明每个 MCP 工具的风险元数据：`risk_level`、`irreversible`、`cost_sensitive`。运行时据此自动决定是否需要 review 门控。

**English**: Adds optional `tools[]` sub-array to `skills[]` in `fcop.json`, letting each Skill declare per-tool risk metadata: `risk_level`, `irreversible`, `cost_sensitive`. Runtimes use these flags to auto-apply review gates or cost guards.

## Context

FCoP v1.0 的 `skills[]` 记录只有 `id`/`label`/`uri` 等标识字段（ADR-0021）。运行时对 MCP 工具的危险程度一无所知，只能靠 agent 自述或 prompt 约束——两者都不可靠。

Issue #2 §Field 5 来自 CodeFlow v2 的 Tool Execution Engine：某些工具（`git push --force`、`db.exec DROP TABLE`、`openai.chat`）需要特殊门控，但没有协议层的结构化声明，运行时只能硬编码工具名字字符串匹配。

## Decision

### 字段定义

```yaml
# fcop.json skills 记录
skills:
  - id: git-tools
    label: Git Operations
    uri: mcp://local/git
    tools:                    # 可选，per-tool 风险声明
      - name: git.status
        risk_level: low
        irreversible: false
        cost_sensitive: false
      - name: git.commit
        risk_level: medium
        irreversible: false
      - name: git.push_force
        risk_level: high
        irreversible: true
      - name: openai.chat
        risk_level: medium
        cost_sensitive: true
      - name: db.exec
        risk_level: irreversible
        irreversible: true
```

| 字段 | 类型 | 默认值 | 含义 |
|---|---|---|---|
| `name` | string | 必填 | MCP 工具名（与 MCP server 的 tool name 对应） |
| `risk_level` | `low\|medium\|high\|irreversible` | `low` | 工具操作风险等级（与 Task.risk_level 同枚举） |
| `irreversible` | boolean | false | 此工具的操作无法撤销 |
| `cost_sensitive` | boolean | false | 调用此工具会产生计费/付费 API 消耗 |

### 运行时合约

1. `irreversible: true` 的工具调用 → 运行时 wraps 为 review-required TASK（不得直接执行）
2. `risk_level: high | irreversible` → 调用前自动触发 `needs_human` review gate
3. `cost_sensitive: true` → 运行时可实施费用阈值检查，超阈值触发 `needs_human`
4. 未声明 `tools[]` 的 Skill 等价于所有工具 `risk_level: low, irreversible: false`（最宽松假设，运行时可选择更保守的默认值）

### Python 实现

- `agent.schema.json` 中 `skills` 属性（若存在）添加 `tools[]` 子 schema，或新建 `skill.schema.json`
- `models.py` 新增 `SkillTool` dataclass（`name`, `risk_level`, `irreversible`, `cost_sensitive`）、`Skill` dataclass（`id`, `label`, `uri`, `tools`）
- `TeamConfig` dataclass 的 `skills` 字段改为 `list[Skill]`（目前是 list[Any]）
- `fcop-mcp` server.py 新增 `list_skill_tools()` MCP 工具

## Consequences

- 向后兼容：不带 `tools[]` 的 Skill 记录无任何变化
- CodeFlow v2 的 Tool Execution Engine 可直接读取 `fcop.json` 的 `tools[]` 做门控决策，无需硬编码
