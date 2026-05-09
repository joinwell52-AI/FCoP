# ADR-0012: `Review.decision = needs_human` Enum Extension

- **Status**: Proposed
- **Date**: 2026-05-09
- **Deciders**: ADMIN（待批准）
- **Related**: [ADR-0007](./ADR-0007-fcop-1.0-protocol-freeze-charter.md)（roadmap 第 6 项）；[ADR-0009](./ADR-0009-review-file-type-and-grammar.md)（REVIEW 文件类型）；[ADR-0011](./ADR-0011-task-risk-level-field.md)（high/irreversible 自动触发本字段）；[ADR-0013](./ADR-0013-review-human-approval.md)（必须配套）；触发：[Issue #2 Field 3](https://github.com/joinwell52-AI/FCoP/issues/2)

## Context

ADR-0009 在 1.0 已经引入 `Review.decision` 枚举：`approved` / `rejected` / `needs_changes` / `abstained`。

CodeFlow §3.4 + Issue #2 Field 3 提出第五个值 `needs_human`：reviewer 主动声明"我不该单方面决定，必须 Human Admin 拍板"。

`needs_human` 不是 `rejected`（reviewer 没发现问题）也不是 `approved`（reviewer 不愿背书）—— 它是**主动升级**。典型场景：

- SQL 看起来对，但缺 `tenant_id` 隔离 → reviewer 不确定是否故意 → 升级
- 配置改动看起来对，但触及生产 → 升级
- 付费 API 调用，cost > $10 → 升级

## Decision

`Review.decision` enum 在 1.1 加第五个值：`needs_human`。

语义约束：

- `decision: needs_human` → review 记录 `status = pending`；不能被关闭
- 必须配 `human_approval` 子结构（ADR-0013）才能真正关闭
- `Project.write_review(decision="needs_human")` 自动 enforce `human_approval` 字段在 frontmatter 占位（即使 `approved_by` 为 null）

## Design Details

- `models.Review.decision` 类型 `Literal[..., "needs_human"]` 增项
- `review.schema.json` v1.1 enum 加新值
- `Project.write_review()` 校验：`needs_human` 必须配 `human_approval` 占位
- `Project.list_reviews(status="pending")` 能过滤出所有 needs_human 待办
- ADR-0011 的 high / irreversible TASK 在被审时，reviewer 可以主动选 `needs_human`（或后续由 Review Engine 自动注入，1.x 后续做）
- MCP tool `fcop.write_review` 暴露 decision 参数

## Tests Checklist

- [ ] `tests/test_fcop/test_project_reviews.py` 加 `needs_human` write + 必须配 human_approval 占位
- [ ] `tests/test_fcop/test_project_reviews.py` 加 list pending（仅 needs_human 未被 human approve）
- [ ] `tests/test_schemas/test_review_schema.py` 加 v1.1 enum
- [ ] `tests/test_fcop_mcp/test_tool_surface.py` 快照更新（write_review decision 多一个值）

## Backwards Compatibility

- enum 加值 → 旧 reviewer 不返回 `needs_human` 即旧行为，完全兼容
- v1.0 schema 仍有效（`decision` 仅 4 值），v1.1 schema 是 superset
- ADR-0003 公开面承诺：枚举加值不破坏

## Open Questions

1. `needs_human` review 是否能被自动 expire？建议**不**——pending 永久挂起直到 admin 处理
2. 是否需要 `escalation_reason` 字段独立于 `rationale`？倾向**合并**到 rationale，避免字段膨胀
3. 同一 TASK 是否能被多次 needs_human review？建议允许，但 list_pending 需 deduplicate

## Sign-off

待 1.0.0 发布后启动本 ADR 评审；与 ADR-0013 同 PR 合入。
