# ADR-0013: `Review.human_approval` Sub-structure

- **Status**: Proposed
- **Date**: 2026-05-09
- **Deciders**: ADMIN（待批准）
- **Related**: [ADR-0007](./ADR-0007-fcop-1.0-protocol-freeze-charter.md)（roadmap 第 7 项）；[ADR-0009](./ADR-0009-review-file-type-and-grammar.md)；[ADR-0010](./ADR-0010-agent-layer-field.md)（admin layer 校验）；[ADR-0012](./ADR-0012-review-decision-needs-human.md)（必须配套）；触发：[Issue #2 Field 4](https://github.com/joinwell52-AI/FCoP/issues/2)

## Context

ADR-0012 引入 `decision: needs_human`。但 review 文件本身不能凭 decision 字段就关闭——必须留下"人确实批准了，且批准过程可审计"的痕迹。

CodeFlow §3.4 + Issue #2 Field 4 提出 `human_approval` 子结构，对应字段：

- `approver` (admin agent ID 或 admin handle)
- `decision` (approve / reject)
- `approved_at`
- `channel` (mobile / cli / web / manual_file_edit)
- `comment`
- `evidence` (device_id / ip / auth_method)

## Decision

Review frontmatter 加可选子对象 `human_approval`（仅在 `decision: needs_human` 时被 enforce）。

校验：

- 任何 `decision: needs_human` 但**无** `human_approval.approver` → review 是 pending；运行时不让 TASK 推进
- `human_approval.approver` 必须是 `layer: admin` 角色（联动 ADR-0010）
- `channel: 'manual_file_edit'` 必须有 `evidence.device_id` 或 `channel_attestation: 'admin-acknowledged-bypass'`（防止匿名 file edit 等于 approval 的攻击）

并提供 `Project.mark_human_approved(review_id, approver, decision, channel, ...)` API。

## Design Details

- `models.HumanApproval` 新 dataclass：`approver` / `decision` / `approved_at` / `channel` / `comment` / `evidence`
- `models.Review` 加 `human_approval: Optional[HumanApproval] = None`
- `models.Evidence` dataclass：`device_id` / `ip` / `auth_method` (`session` / `biometric` / `password_with_2fa`)；**`auth_method` enum 不含纯 `password`**（Issue 评论里明确：2026 年不该接受 bare password 作为 admin-tier 认证）
- `Project.mark_human_approved()` 新公开 API：原子更新 review 文件 frontmatter
- `review.schema.json` v1.1 加 sub-object
- MCP tool `fcop.approve_review` 暴露：参数 review_id + decision + comment（其他字段由 server 端从 session 自动填）

## Tests Checklist

- [ ] `tests/test_fcop/test_project_reviews.py` 加 mark_human_approved 全闭环（4 channel × 2 decision）
- [ ] `tests/test_fcop/test_project_reviews.py` 加非 admin layer 拒绝
- [ ] `tests/test_fcop/test_project_reviews.py` 加 manual_file_edit 缺 evidence 拒绝
- [ ] `tests/test_schemas/test_review_schema.py` 加 v1.1 sub-object
- [ ] `tests/test_fcop_mcp/test_tool_surface.py` 快照更新（多 1 个 approve_review tool）

## Backwards Compatibility

- 字段是 optional sub-object → 旧 review 文件无此字段，仍合法
- 仅 `decision: needs_human` 时被 enforce → 不影响其他 4 种 decision
- `mark_human_approved` 是新 API → 加入 ADR-0003 公开面只进不出锁

## Open Questions

1. `approver` 应该用 ADMIN agent ID（如 `ADMIN-01`）还是真人 handle（如 `@joinwell52`）？建议**优先 agent ID**，handle 可作为 evidence 字段
2. `evidence.auth_method` 选项里要不要保留 `password_with_2fa`？还是干脆只接受 `session` / `biometric`？倾向保留 `password_with_2fa`（CLI 场景兼容性）
3. `channel: 'manual_file_edit'` 要不要默认禁用？需要环境变量 / config 显式开启？倾向默认允许但强校验 `channel_attestation`
4. mobile push 的 evidence 字段如何获取？由 CodeFlow runtime 填，FCoP 不做规定

## Sign-off

待 1.0.0 发布后启动本 ADR 评审；与 ADR-0012 同 PR 合入。
