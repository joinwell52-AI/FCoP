# ADR-0024: Task.risk_level — Operation Risk Classification

- **Status**: Accepted
- **Date**: 2026-05-10
- **Deciders**: ADMIN
- **Related**: [ADR-0015](./ADR-0015-fcop-1.0-ai-os-protocol-charter.md), [ADR-0019](./ADR-0019-failure-and-recovery-semantics.md) (abort/rollback), [ADR-0025](./ADR-0025-review-needs-human.md), [Issue #2](https://github.com/joinwell52-AI/FCoP/issues/2)

## TL;DR

**中文**：在 TASK frontmatter 中加入 `risk_level: low | medium | high | irreversible`（默认 `medium`）。`high`/`irreversible` 级别任务由运行时自动注入人工审核节点（`Review.decision: needs_human`，见 ADR-0025），`irreversible` 额外要求 dry_run 或 rollback plan。

**English**: Adds `risk_level: low | medium | high | irreversible` (default `medium`) to TASK frontmatter. `high` / `irreversible` tasks automatically require a `needs_human` review gate (ADR-0025). `irreversible` additionally requires `dry_run: true` or a rollback plan (deferred detail to v1.2).

## Context

FCoP v1.0 的 TASK 只有 `priority`（P0–P3）表示紧急度，没有"风险度"字段。两者正交：一个任务可以是 P2（低优先级）但 `irreversible`（删除历史数据），也可以是 P0（紧急）但 `low`（紧急写一行注释）。

CodeFlow v2 在 Session Manager 实现中发现（Issue #2 §Field 2）：没有协议级风险分类，运行时只能在调度层硬编码特定任务名关键词，脆弱且不可跨项目移植。

## Decision

### 字段定义

```yaml
# TASK frontmatter
risk_level: medium   # low | medium | high | irreversible（可选，默认 medium）
```

| 值 | 含义 | 自动触发 |
|---|---|---|
| `low` | 只读/无副作用（run tests, write docs） | 无 |
| `medium` | 常规开发操作，默认值 | 正常 review 流程 |
| `high` | 影响生产/权限/配置 | 必须经 `needs_human` review |
| `irreversible` | 不可撤销操作（drop DB, force-push, 超额 API 调用） | `needs_human` + 须有 dry_run 或 rollback plan |

### 运行时合约

1. 运行时读取 `risk_level`（缺省视为 `medium`）
2. 若 `risk_level in {high, irreversible}`，Review Engine 在创建 REVIEW 文件时**自动写入** `decision: needs_human`（由 ADR-0025 定义）
3. `irreversible` + 无 `dry_run: true` + 无 rollback plan 文件 → `write_task` 可选择拒绝（`BoundaryViolationError`）；v1.1 不强制，v1.2 收严

### Python 实现

- `ipc-envelope.schema.json` → `task.$defs` 新增 `risk_level` 属性
- `models.py` 新增 `RiskLevel` enum（`low | medium | high | irreversible`）
- `TaskFrontmatter` 新增 `risk_level: RiskLevel = RiskLevel.MEDIUM`
- `Project.write_task(risk_level=...)` 新增可选参数

## Consequences

- 向后兼容：缺少 `risk_level` 字段 = `medium`
- 下游 CodeFlow 可在 Session Manager 的调度决策中直接读取 `risk_level` 做门控
