# ADR-0014: `Skill.tools[]` Risk Metadata

- **Status**: Proposed
- **Date**: 2026-05-09
- **Deciders**: ADMIN（待批准）
- **Related**: [ADR-0007](./ADR-0007-fcop-1.0-protocol-freeze-charter.md)（roadmap 第 8 项）；[ADR-0008](./ADR-0008-json-schema-as-machine-readable-spec.md)；[ADR-0011](./ADR-0011-task-risk-level-field.md)（同 enum 集合）；触发：[Issue #2 Field 5](https://github.com/joinwell52-AI/FCoP/issues/2)；外部参考：[CodeFlow §3.6 Skill Schema](https://github.com/joinwell52-AI/codeflow-pwa/blob/main/docs/design/codeflow-v2-on-fcop-sdk.md)

## Context

FCoP 当前没有 Skill schema。MCP 工具是 `fcop-mcp` 内 FastMCP 装饰器声明的，没有"工具风险元数据"概念。

CodeFlow §3.6 + Issue #2 Field 5 提出每个 MCP tool 应该声明：

| 字段 | 含义 |
|---|---|
| `risk_level` | 同 ADR-0011 的 4 值 enum |
| `irreversible` | bool，是否不可回滚 |
| `cost_sensitive` | bool，是否触发付费 |

例：`git_push_force` → `high` + `irreversible`；`db_drop_table` → `irreversible`；`openai_chat` → `cost_sensitive`。

运行时行为（由 CodeFlow Skill Runtime 实现，不在 FCoP 范围）：`high` / `irreversible` 拦截调用 → 转 needs_human Review；`cost_sensitive` 估算成本 → 超阈值同 high。

## Decision

`spec/schemas/skill.schema.json` v1.1 落地 Skill schema 完整字段（不是仅占位）。

`fcop` 库一侧加 Skill loader：解析 `.fcop/skills/*.json` 或外部 `--skill-file` 指向的 JSON 文件，校验后供 `fcop_report()` 等输出使用。

`fcop` 库本身**不**enforce 运行时行为（"调用前拦截"）——这是 CodeFlow Skill Runtime 的事；FCoP 只提供 schema 与 loader，让任何 host 都能消费这套元数据。

## Design Details

- `spec/schemas/skill.schema.json` v1.1 完整字段：`skill_id`, `version`, `displayName`, `provided_by` (`type` / `transport` / `command` / `url`), `tools[]` (含 `name` / `required_perms` / `risk_level` / `irreversible` / `cost_sensitive`), `available_to_roles`, `required_kernel`, `compatible_runtimes`, `homepage`, `license`
- `models.Skill` / `models.SkillTool` 新 dataclass
- `fcop.skills` 子模块新增：`load_skills_dir()` / `validate_skill()`
- `_data/skills/` 模板目录（与 `_data/teams/` 风格一致）；1.1 仅放 `git.json`、`fcop.json` 两个示例
- `fcop_mcp` 的 22 个 tool 不强制声明 risk_level（1.1 阶段 host-neutral 优先）；可选地由 `fcop-mcp` 在自己包里维护一个 `_data/skills/fcop-mcp.json` 作为示例
- `Project.list_skills()` 公开方法（可选，1.1 不强制）

## Tests Checklist

- [ ] `tests/test_schemas/test_skill_schema.py` 加 v1.1 完整字段（合法 / 缺必填 / 非法值）
- [ ] `tests/test_fcop/test_skills.py` 新文件：load / validate 闭环
- [ ] `tests/test_fcop/test_skills.py` 加示例 git.json 与 fcop.json 的 round-trip
- [ ] `tests/test_fcop/test_public_surface.py` 快照更新（如新增 `Project.list_skills`）

## Backwards Compatibility

- 加新模块 / 新 schema / 新目录 → 对 0.7.x 用户**完全透明**
- `fcop-mcp` 不修改 tool 声明 → MCP tool surface snapshot 不变
- 1.1 起，spec 鼓励第三方 MCP server 包含 `_data/skills/<server>.json` 自描述

## Open Questions

1. `_data/skills/` 还是 `.fcop/skills/`？倾向**前者作为模板、后者作为运行时实例目录**
2. `risk_level: 'high'` 的 tool 是否在 fcop 库一侧就拦截？建议**不**——FCoP 仅描述、不 enforce；enforce 是 host runtime 的事
3. `compatible_runtimes` 是否包含 `mobile` / `cloud`？1.1 仅 `local` / `cloud`，与 CodeFlow §3.6 对齐
4. 第三方 skill 缺省值——`risk_level` 缺省 `medium`；`irreversible` 缺省 `false`；`cost_sensitive` 缺省 `false`

## Sign-off

待 1.0.0 发布后启动本 ADR 评审。
