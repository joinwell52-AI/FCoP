# ADR-0011: `Task.risk_level` Field (`low` / `medium` / `high` / `irreversible`)

- **Status**: Deferred to v1.1+（2026-05-09，由 [ADR-0015](./ADR-0015-fcop-1.0-ai-os-protocol-charter.md) §Context 决定：risk_level 属于 Layer 3 Governance Policy，不是协议本体；v1.0 仅保留 Governance Hook，不写 policy）
- **Date**: 2026-05-09
- **Deciders**: ADMIN（待批准）
- **Related**: [ADR-0007](./ADR-0007-fcop-1.0-protocol-freeze-charter.md)（roadmap 第 5 项）；[ADR-0008](./ADR-0008-json-schema-as-machine-readable-spec.md)；[ADR-0012](./ADR-0012-review-decision-needs-human.md)（high/irreversible 自动触发 needs_human）；触发：[Issue #2 Field 2](https://github.com/joinwell52-AI/FCoP/issues/2)；外部参考：[CodeFlow §0.9.4 高风险红线](https://github.com/joinwell52-AI/codeflow-pwa/blob/main/docs/design/codeflow-v2-on-fcop-sdk.md)

## Context

CodeFlow §0.9.4 列出 6 类高风险红线（数据破坏 / 生产环境 / 权限 / 协议 / 资金 / 不可逆）。Issue #2 Field 2 把它落到 `Task.risk_level`。

风险等级语义：

| risk_level | 典型动作 | 触发行为 |
|---|---|---|
| `low` | 写文档、跑单测、整理目录 | 直接执行 |
| `medium`（默认） | 实现功能、改配置 | 走单 reviewer Review |
| `high` | 发布、改生产配置、改权限 | Review **必须** `needs_human`（联动 ADR-0012） |
| `irreversible` | drop 数据库、force-push、删 git history、付费 API > 配额 | needs_human + 必须有 `requires_rollback_plan: true`（字段名预留，1.2 实现） |

## Decision

`TaskFrontmatter` 加可选字段 `risk_level: "low" | "medium" | "high" | "irreversible"`，默认 `medium`。

`Project.write_task()` MCP tool 加可选参数 `risk_level`。

`high` / `irreversible` 触发后续 ADR-0012 的 needs_human 自动注入。`irreversible` 同时要求 `requires_rollback_plan` 字段（1.1 仅保留字段名，不 enforce 内容；1.2 enforce）。

## Design Details

- `models.TaskFrontmatter` 加字段：`risk_level: Literal["low", "medium", "high", "irreversible"] = "medium"`
- `core/schema.OPTIONAL_TASK_FRONTMATTER_KEYS` 加 `"risk_level"` 与 `"requires_rollback_plan"`（仅占位）
- `core/frontmatter._KNOWN_KEYS` 同步加
- `task.schema.json` v1.1 加 enum + default
- `Project.write_task(risk_level="...")` 传入 → 写进 frontmatter
- `Project.write_task` 校验：`irreversible` 必须配 `requires_rollback_plan` 字段（值任意，1.1 仅检查存在）
- MCP tool `fcop.create_task` 暴露 `risk_level` 可选参数

## Tests Checklist

- [ ] `tests/test_fcop/test_models.py` 加默认 medium
- [ ] `tests/test_fcop/test_core_frontmatter.py` 加 4 个 risk_level 解析 + 非法值拒绝
- [ ] `tests/test_fcop/test_project_writes.py` 加 risk_level 写 + irreversible 缺 rollback_plan 拒绝
- [ ] `tests/test_schemas/test_task_schema.py` 加 v1.1 字段
- [ ] `tests/test_fcop_mcp/test_tool_surface.py` 快照更新（fcop.create_task 多一个可选参数）

## Backwards Compatibility

- 字段缺省 = `medium` → 旧 TASK 文件读取时填默认值，无感
- 旧 `Project.write_task()` 调用（无 risk_level）→ 默认 `medium`，无感
- MCP tool 加可选参数 → 旧 Cursor 调用不传亦可，行为同 `medium`
- ADR-0003 公开面承诺：可选参数加在末尾、有默认值 → 不破坏

## Open Questions

1. `risk_level: 'high'` 是否在 1.1 立刻 enforce 必须走 needs_human？建议**先弱后强**：1.1 只标注，1.2 才 enforce；避免 1.1 一上来就 break 现有 workflow
2. `requires_rollback_plan` 的最小内容（1.2 实现时）？倾向 markdown body 里的 H2 段落 `## Rollback`
3. risk_level 字段是否也加给 REVIEW？建议**不加**——REVIEW 是审 TASK 的事件，risk 应该在 TASK 上承载

## Sign-off

待 1.0.0 发布后启动本 ADR 评审。
