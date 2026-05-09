# ADR-0010: `Agent.layer` Field (`worker` / `governance` / `admin`)

- **Status**: Proposed
- **Date**: 2026-05-09
- **Deciders**: ADMIN（待批准）
- **Related**: [ADR-0007](./ADR-0007-fcop-1.0-protocol-freeze-charter.md)（roadmap 第 4 项）；[ADR-0008](./ADR-0008-json-schema-as-machine-readable-spec.md)；触发：[Issue #2 Field 1](https://github.com/joinwell52-AI/FCoP/issues/2)；外部参考：[CodeFlow §0.9.1 三层组织](https://github.com/joinwell52-AI/codeflow-pwa/blob/main/docs/design/codeflow-v2-on-fcop-sdk.md)

## Context

CodeFlow §0.9.1 定义三层组织（Worker / Governance / Human Admin）。Issue #2 Field 1 把它落到 `Agent.layer`。FCoP 现状：`fcop.json` 的 `roles` 只有 `code` + `label`，无层级概念。

层级语义：

| layer | 典型 role | 运行时强制 |
|---|---|---|
| `worker` | DEV / TEST / DOC / OPS / PM | 不允许签发 Review；不允许调用 Human Admin；不允许撤销其他 agent |
| `governance` | REVIEW / AUDIT / SECURITY / PATROL | 不允许直接修改业务代码；签发的 Review 才有合法性；可以路由到 Human Admin |
| `admin` | ADMIN（人，不是 agent） | 唯一可越过协议干预；只通过 Mobile / CLI 进入 Runtime；programmatic create 必须被运行时拒绝 |

## Decision

`fcop.json` 的 `roles[i]` 加可选字段 `layer: "worker" | "governance" | "admin"`。

默认 `worker`。校验：

- `Agent.create({layer: 'admin'})` 必须被运行时拒绝（除非有 admin token）
- `governance` agent 不允许 spawn 其他 agent（防 governance fission）
- `worker` agent 不允许 review `governance` 输出

校验细节由 `core/schema.py` 的新 helper 函数实现，`fcop` 库 + `fcop-mcp` 共用。

## Design Details

- `models.Role` dataclass 加字段：`layer: Literal["worker", "governance", "admin"] = "worker"`
- `core/config.parse_team_config` 接受新字段、旧文件无此字段时填默认值
- `core/schema.py` 新增 `validate_role_layer_constraint()`：传入 actor + target，校验 4 条 layer rule
- `Project.write_task` / `Project.write_review` 在写之前调用 layer 校验
- `agent.schema.json` v1.1 加 `layer` enum + default
- 1.1 不强制旧 `fcop.json` 添加 layer 字段（grace period），但 `fcop_report()` 显示警告

## Tests Checklist

- [ ] `tests/test_fcop/test_models.py` 加 Role.layer default
- [ ] `tests/test_fcop/test_core_config.py` 加 layer 解析 / 默认 / 非法值
- [ ] `tests/test_fcop/test_layer_constraints.py` 新文件：4 条 layer rule × 5 种 actor/target 组合
- [ ] `tests/test_schemas/test_agent_schema.py` 加 v1.1 字段
- [ ] `tests/test_fcop/test_project_writes.py` 加 governance fission 拒绝、worker 不能审 governance 等行为测试

## Backwards Compatibility

- 字段缺省 = `worker` → 旧 `fcop.json` 无感
- 0.7.x 没有 layer 校验 → 1.1 加上是新行为，但旧代码不调用 governance fission 等场景也不会被拒
- `fcop_report()` 警告级别，不阻塞

## Open Questions

1. `governance` 与 `worker` 是否应该有 spec-level 推荐角色映射表？建议在 spec 文档里给推荐表，但不在 schema 里 enforce
2. `admin` layer 是否允许出现在 `fcop.json.roles`？倾向**不允许**（admin 是人不是 agent；agent 角色只能是 worker/governance）→ schema enum 排除 admin？需要确认
3. `governance` 角色之间是否有子层级（如 SECURITY 高于 REVIEW）？v1.1 不做，留 1.x 后续

## Sign-off

待 1.0.0 发布后启动本 ADR 评审。
