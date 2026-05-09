# ADR-0020: Agent Boundary & Capability

- **Status**: Accepted
- **Date**: 2026-05-09
- **Accepted-on**: 2026-05-09（solo 模式 ADMIN ≡ ME 自签；详见 §Sign-off）
- **Deciders**: ADMIN
- **Supersedes**: [ADR-0010](./ADR-0010-agent-layer-field.md)（layer 字段单独视角）
- **Related**: [ADR-0015](./ADR-0015-fcop-1.0-ai-os-protocol-charter.md) §抽象 6 Boundary；[ADR-0016](./ADR-0016-json-schema-for-7-abstractions.md) `boundary.schema.json`；[ADR-0018](./ADR-0018-event-model.md)（boundary 校验失败应触发 BOUNDARY_VIOLATED 事件）；触发：[Issue #2 Field 1](https://github.com/joinwell52-AI/FCoP/issues/2)
- **Implementation**: [TASK-20260509-005](../docs/agents/log/tasks/TASK-20260509-005-ADMIN-to-ME.md) R1 commit `6a2dd93`（core/boundary.py + 4 规则 + 测试）+ R2 commit `2f5b917`（Project 公开 API + write_review 接强制 + 配置层支持 layer/can/cannot）

## Context

ADR-0010 把 Issue #2 Field 1 的 `Agent.layer` 设计成单字段 `worker | governance | admin`——但外部架构反馈指出：

> "Agent Boundary 不够明确——缺少权限定义。否则 Runtime 很容易漂移。"

`layer` 是 **capability bundle 的简写**——`worker` 实际意味着 "can=[file_io, task_io], cannot=[approve_release, escalate]"。直接暴露 capability schema 比仅暴露 layer 字段更接近 POSIX 权限模型。

## Decision

`fcop.json` 的 `roles[i]` 加可选字段：

```json
{
  "code": "DEV",
  "label": "开发者",
  "layer": "worker",        // capability bundle 简写
  "can": ["file_io", "task_io", "modify_code"],
  "cannot": ["approve_release", "escalate", "spawn_agent"]
}
```

`layer` 与 `can`/`cannot` **同时存在时**，`can`/`cannot` 是显式真相，`layer` 仅作 default bundle 简写。

层级语义（v1.0 锁定 3 个 bundle）：

| layer | default `can` | default `cannot` |
|---|---|---|
| `worker`（默认） | `file_io`, `task_io` | `approve_release`, `escalate`, `spawn_agent` |
| `governance` | `file_io`, `task_io`, `review_decision` | `modify_code`, `spawn_agent` |
| `admin` | `file_io`, `task_io`, `review_decision`, `escalate`, `override` | （无）—— 但 `admin` programmatic create 必须被 runtime 拒绝 |

校验：

- `Agent.create({layer: 'admin'})` 必须被 runtime 拒绝（除非有 admin token）
- `governance` agent 不允许 spawn 其他 agent（防 governance fission）
- `worker` agent 不允许 review `governance` 输出
- 显式 `can`/`cannot` 覆盖 layer default

## Design Details

- `models.Role` dataclass 加字段：`layer: Literal[...] = "worker"`, `can: list[str] = []`, `cannot: list[str] = []`
- `core/config.parse_team_config` 接受新字段；旧文件无字段时填 layer default
- `core/schema.py` 新增 `validate_role_boundary(actor, target)`：传入 actor + target，校验 4 条 boundary rule
- `Project.write_task` / `write_review` / `archive_*` 在写之前调 boundary 校验
- `boundary.schema.json` 给 capability 词表（v1.0 词表 ~10 个；v1.1 build out）
- v1.0 词表（最小集）：`file_io`, `task_io`, `modify_code`, `review_decision`, `approve_release`, `escalate`, `spawn_agent`, `override`, `archive`, `mark_done`
- 1.0 不强制旧 `fcop.json` 添加新字段（grace period），但 `fcop_report()` 显示警告

## Tests Checklist

- [x] `tests/test_fcop/test_boundary.py`（新文件，25 用例）—— 4 条 boundary rule 各 ≥ 2 用例 + 显式 can/cannot 覆盖 layer default + UNKNOWN_CAPABILITY warning
- [x] `tests/test_fcop/test_core_config_role_capability.py`（新文件，10 用例）—— dict-form roles 新字段解析 / 默认 / 非法值 / round-trip
- [x] `tests/test_fcop/test_project_boundary.py`（新文件，14 用例）—— `Project.boundary_violations` / `assert_boundary` / `write_review` 端到端 + admin layer 拒收 + governance fission 拒绝 + worker 不能审 governance
- [x] `tests/test_schemas/test_boundary_schema.py`（已在 TASK-004 R1 落地）
- ~~`tests/test_fcop/test_models.py` 加 Role.layer / can / cannot default~~ —— **不适用**：v1.0 不引入 `Role` dataclass（per TASK-005 §决议 1），数据走 `_role_labels` 路径
- ~~`tests/test_fcop/test_project_writes.py` 加 boundary 强制~~ —— **范围调整**：仅 `write_review` 接强制（v1.0 第一个新增写入路径）；write_task / write_report / write_issue 留待 v1.1 通过 `enforce_boundary` 参数 opt-in

## Backwards Compatibility

- 字段缺省 = `worker` + 对应 default bundle → 旧 `fcop.json` 无感
- 显式 can/cannot 完全 opt-in
- 0.7.x 没有 boundary 校验 → v1.0 加上是新行为；旧代码不调用 governance fission 等场景也不会被拒
- `fcop_report()` 警告级别，不阻塞

## Open Questions（实现时已解决）

1. ~~`admin` layer 是否允许出现在 `fcop.json.roles`？~~ **已决：不允许**（per TASK-005 §决议 4）。`lookup_capability` 在解析 fcop.json 时若发现 `layer: "admin"` 直接 raise `BoundaryViolationError(NO_ADMIN_PROGRAMMATIC_CREATE)`。`AgentLayer.ADMIN` 枚举仍保留——它描述「人在角色」语义（envelope sender 可以是 ADMIN），不是 fcop.json roles 字段
2. 第三方自定义 capability 词如何注册？**v1.0 不做扩展机制**；词表硬编码 10 个；词表外 token 触发 `UNKNOWN_CAPABILITY` warning（advisory，不阻塞）。v1.1 视社区反馈考虑 `Project.register_capability` 之类的 hook
3. capability 是否细到方法级（如 `task_io` 拆 `task_read` / `task_write`）？**v1.0 粗粒度**；v1.1 视用户反馈细化
4. `governance` 与 `worker` 之间是否有子层级（如 SECURITY 高于 REVIEW）？**v1.0 不做**；v1.x 后续

## Sign-off

| Role | Decision | Date | Note |
|---|---|---|---|
| ADMIN（solo 模式 ≡ ME） | Accepted | 2026-05-09 | TASK-005 R3 commit；charter ADR-0015 已 Accepted；本 ADR 实现验收 11/11 通过；测试 49 用例全过 |
