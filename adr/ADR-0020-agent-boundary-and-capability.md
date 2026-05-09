# ADR-0020: Agent Boundary & Capability

- **Status**: Proposed
- **Date**: 2026-05-09
- **Deciders**: ADMIN（待批准）
- **Supersedes**: [ADR-0010](./ADR-0010-agent-layer-field.md)（layer 字段单独视角）
- **Related**: [ADR-0015](./ADR-0015-fcop-1.0-ai-os-protocol-charter.md) §抽象 6 Boundary；[ADR-0016](./ADR-0016-json-schema-for-7-abstractions.md) `boundary.schema.json`；[ADR-0018](./ADR-0018-event-model.md)（boundary 校验失败应触发 BOUNDARY_VIOLATED 事件）；触发：[Issue #2 Field 1](https://github.com/joinwell52-AI/FCoP/issues/2)

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

- [ ] `tests/test_fcop/test_models.py` 加 Role.layer / can / cannot default
- [ ] `tests/test_fcop/test_core_config.py` 加新字段解析 / 默认 / 非法值
- [ ] `tests/test_fcop/test_boundary.py` 新文件：4 条 boundary rule × 5 种 actor/target 组合
- [ ] `tests/test_fcop/test_boundary.py` 加显式 can/cannot 覆盖 layer default
- [ ] `tests/test_schemas/test_boundary_schema.py`
- [ ] `tests/test_fcop/test_project_writes.py` 加 governance fission 拒绝、worker 不能审 governance

## Backwards Compatibility

- 字段缺省 = `worker` + 对应 default bundle → 旧 `fcop.json` 无感
- 显式 can/cannot 完全 opt-in
- 0.7.x 没有 boundary 校验 → v1.0 加上是新行为；旧代码不调用 governance fission 等场景也不会被拒
- `fcop_report()` 警告级别，不阻塞

## Open Questions

1. `admin` layer 是否允许出现在 `fcop.json.roles`？倾向**不允许**（admin 是人不是 agent）→ schema enum 排除 admin？需要确认
2. 第三方自定义 capability 词如何注册？v1.0 不做扩展机制；词表硬编码 ~10 个
3. capability 是否细到方法级（如 `task_io` 拆 `task_read` / `task_write`）？v1.0 粗粒度；v1.1 视用户反馈细化
4. `governance` 与 `worker` 之间是否有子层级（如 SECURITY 高于 REVIEW）？v1.0 不做；v1.x 后续

## Sign-off

待 ADR-0015 charter 通过后，本 ADR 由 ADMIN 直接 sign 进入 Accepted。
