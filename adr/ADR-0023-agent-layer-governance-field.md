# ADR-0023: Agent.layer — Governance Hierarchy Field

- **Status**: Accepted
- **Date**: 2026-05-10
- **Deciders**: ADMIN
- **Related**: [ADR-0015](./ADR-0015-fcop-1.0-ai-os-protocol-charter.md) (AI OS charter), [ADR-0020](./ADR-0020-agent-boundary-and-capability.md) (capability/boundary), [Issue #2](https://github.com/joinwell52-AI/FCoP/issues/2)

## TL;DR

**中文**：将 `Agent.layer` 从 schema 中已存在的描述性字段**升格为正式协议字段**，赋予运行时约束语义：`worker` 执行业务任务；`governance` 只做审计/巡逻，不生产制品；`admin` 仅人工创建，运行时必须拒绝编程式创建。ADR-0023 是 v1.1.0 五项新字段的基础依赖（`human_approval.approver` 校验、`Review.reviewer_role` 层级校验都引用此枚举）。

**English**: Formalises `Agent.layer` from a descriptor-only field (already in `agent.schema.json` v1.0.0) into a **protocol field with runtime contracts**: `worker` executes business tasks; `governance` audits only (cannot spawn, cannot execute); `admin` is human-only (runtime MUST reject programmatic creation). Serves as the foundation for ADR-0024–0027.

## Context

`agent.schema.json` v1.0.0（ADR-0020）已包含 `layer` 字段及其枚举定义，但 v1.0 将其标注为"capability bundle shorthand"，未明确写出运行时必须执行的约束。

下游 CodeFlow v2（Issue #2 §Field 1）在 Agent Registry 实现中发现，如果 `layer` 没有协议级合约，每个运行时都得自己猜测：

1. `governance` agent 能否写 TASK？（不能）
2. `admin` agent 可以被 `write_task sender=ADMIN` 以外的方式创建吗？（不能）
3. `governance` agent 出现在 `Review.reviewer_role` 时是否有特殊意义？（有：只有 governance/admin 层才能出现）

这些缺失的约束导致下游必须在运行时层硬编码，违反了 FCoP 作为 AI OS Protocol Layer 的职责。

## Decision

### 字段定义（向后兼容，`default: worker`）

```yaml
# fcop.json / agent 记录中
layer: worker   # worker | governance | admin
```

| 值 | 含义 | 限制 |
|---|---|---|
| `worker` | 业务执行层，默认值 | 无额外限制 |
| `governance` | 治理层（审计/巡逻/审批） | 不得生产 TASK/REPORT；可生产 REVIEW；不得 spawn 其他 agent |
| `admin` | 最高权限，代表人工操作者 | 运行时**必须拒绝**编程式创建；只能通过人工入口（CLI / ADMIN-01 session）存在 |

### 运行时合约（MUST level）

1. **admin 创建保护**：任何通过 `Project.init` / `write_task sender=X` 等方式隐式创建 `layer: admin` agent 的操作，运行时必须拒绝并抛出 `BoundaryViolationError`
2. **governance 执行保护**：`governance` agent 不得出现在 TASK/REPORT 的 `recipient` 字段（TASK 是 worker 的工作指令，不是对 governance 层的指令）
3. **reviewer_role 层级约束**：`Review.reviewer_role` 所对应的 agent 的 `layer` 必须是 `governance` 或 `admin`（worker 不得审核）—— 此约束由 ADR-0025/0026 的 `needs_human` 逻辑强制

### Python 实现

- `AgentLayer` 枚举：models.py 中已有，无需修改
- `Project._validate_layer_constraints()` 在 `write_task`、`write_report` 调用时执行校验
- `fcop.json` 中 `roles[]` 条目新增 `layer` 字段支持（已经 additionalProperties: true，向后兼容）

## Consequences

- 现有 `fcop.json` 文件不设置 `layer` 字段 → 等价于 `layer: worker`，完全向后兼容
- 新建项目推荐在 `roles` 条目中显式声明 `layer`
- 下游 CodeFlow 可直接使用 `fcop.json` 中的 `layer` 值驱动 Agent Registry 的权限模型
