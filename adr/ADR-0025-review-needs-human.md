# ADR-0025: Review.decision — needs_human 枚举扩展

- **Status**: Accepted
- **Date**: 2026-05-10
- **Deciders**: ADMIN
- **Related**: [ADR-0017](./ADR-0017-review-file-type-minimal.md) (REVIEW minimal surface), [ADR-0024](./ADR-0024-task-risk-level.md) (risk_level 触发源), [ADR-0026](./ADR-0026-review-human-approval.md) (配套 human_approval), [Issue #2](https://github.com/joinwell52-AI/FCoP/issues/2)

## TL;DR

**中文**：将 `Review.decision` 枚举从 4 值扩展为 5 值，新增 `needs_human`。语义：审核 agent 认为此决策不应独自做出，主动上报人工。这是"主动升级"而非"驳回"。配套 ADR-0026 的 `human_approval` 子结构实现闭环。

**English**: Extends `Review.decision` enum by one value: `needs_human`. Semantics: the reviewing agent escalates to a human rather than deciding alone. This is an **active escalation** (not a rejection). Paired with ADR-0026 `human_approval` to close the loop.

## Context

ADR-0017 明确说：`needs_human` 推迟到 v1.2，因为当时没有 `human_approval` 子结构，孤立的 `needs_human` 决策没有闭环机制，会让 review 记录永远悬挂。

v1.1 同时引入 ADR-0026（`human_approval`），使 `needs_human` 有了配套的"人工批准后如何写回"路径，ADR-0017 的 deferral 理由消除。

Issue #2 §Field 3 给出了具体触发场景：
- SQL 查询遗漏 tenant_id 隔离 → 审核 agent 不确定是否故意 → 升级
- 任何 `risk_level: high | irreversible` 的任务 → 审核 agent 强制升级（ADR-0024 合约）
- 付费 API 调用成本超阈值 → 升级

## Decision

### 枚举扩展

```
approved | rejected | needs_changes | abstained | needs_human
```

（保留 v1.0 全部 4 值，纯加法）

### 语义

| 值 | 含义 |
|---|---|
| `needs_human` | 审核 agent 主动上报，认为此决策需要人工介入；record `status = pending`，不可关闭；必须等待 `human_approval` 填写后才能推进 |

### 运行时合约

1. `decision: needs_human` 的 REVIEW 记录 `status` 必须是 `pending`
2. `human_approval` 字段缺失时，运行时不得将此任务标记为"completed"
3. `reviewer_role` 对应 agent 的 `layer` 必须是 `governance` 或 `admin`（ADR-0023 约束）

### ADR-0017 deferral 解除理由

ADR-0017 写道：_"v1.2 may extend additively (e.g. `needs_human`)"_。v1.1 满足当时的 deferral 前置条件（`human_approval` 同步落地），故提前到 v1.1。

### Python 实现

- `review.schema.json` `$defs.decisionEnum.enum` 追加 `needs_human`
- `ReviewDecision` enum 追加 `needs_human = "needs_human"`
- `Project.write_review(decision=...)` 无需改动（已接受 `ReviewDecision | str`）

## Consequences

- 向后兼容：现有不使用 `needs_human` 的代码无任何影响
- `ReviewDecision.needs_human` 触发 `Project.mark_human_approved()` 工作流（ADR-0026）
