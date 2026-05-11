# 从 v1.0 迁移到 v1.1

> **结论：不需要迁移。**
>
> v1.1 是**纯 additive** 版本——所有新增字段均为可选，所有新 MCP 工具
> 均为新增，没有任何现有字段、工具或行为被修改或删除。
> 已有的 v1.0 项目不需要执行任何迁移操作，直接升级即可。

---

## 升级步骤（2 步）

### Step 1 · 升级包

```bash
pip install -U "fcop" "fcop-mcp"
```

在**运行 MCP 的 venv** 里执行，然后完全重启 Cursor（或 `Developer: Reload Window`）。

### Step 2 · 刷新项目规则文件（推荐）

升级包后，项目里的 `fcop-rules.mdc` / `fcop-protocol.mdc` /
`AGENTS.md` / `CLAUDE.md` 不会自动更新。
`fcop_report()` 的 `[Versions]` 段会提示版本漂移；让 ADMIN 调一次：

```
redeploy_rules()
```

这会把最新的规则文件（`fcop-rules.mdc` **v2.2.0** + `fcop-protocol.mdc`
**v2.0.0**）写入项目，旧文件归档到 `.fcop/migrations/<时间戳>/rules/`。

v2.2.0 的规则文件包含 `risk_level`、`needs_human`、`human_approval` 的
完整说明，升级后的 agent 会自动获知这些新特性。

---

## v1.1 新增特性（全部 opt-in）

不启用任何新特性时，项目行为与 v1.0 完全一致。

| 特性 | 如何启用 | 文档 |
|---|---|---|
| `Task.risk_level` | `write_task(risk_level="high")` | 高风险/不可逆操作自动创建审批门 |
| `Review.decision = needs_human` | `write_review(decision="needs_human")` | 暂停执行，等待人工批准 |
| `Review.human_approval` | `mark_human_approved(review_id)` | 记录人工审批，解除执行冻结 |
| `Agent.layer` | 在 `fcop.json` 的 role 对象加 `layer` 字段 | 治理层级约束 |
| `Skill.tools[]` 风险元数据 | 在 skill 文件的 `tools[]` 条目加风险字段 | 机器可读风险声明 |

---

## 没有破坏性变更的承诺

按照 [ADR-0003](../adr/ADR-0003-stability-charter.md) 的稳定性章程，
`1.x` 系列内的 MINOR 版本保证：

- 现有 MCP 工具调用形态不变（只新增参数，且新参数有默认值）。
- 现有 TASK / REPORT / ISSUE / REVIEW 文件继续通过 schema 验证。
- `fcop.json` 现有格式不变。
- `risk_level` 缺失时默认行为与 v1.0 完全相同（按 `low` 处理）。

如果升级后发现任何不兼容，请在
[GitHub Issues](https://github.com/joinwell52-AI/FCoP/issues) 报告。

---

## 参考链接

- [`spec/fcop-runtime-protocol-v1.1.md`](../spec/fcop-runtime-protocol-v1.1.md) — v1.1 变更规范（英文）
- [`spec/fcop-runtime-protocol-v1.1.zh.md`](../spec/fcop-runtime-protocol-v1.1.zh.md) — v1.1 变更规范（中文）
- [`docs/releases/1.1.0.md`](./releases/1.1.0.md) — 发版说明
- [`docs/upgrade-fcop-mcp.md`](./upgrade-fcop-mcp.md) — 通用升级指南
