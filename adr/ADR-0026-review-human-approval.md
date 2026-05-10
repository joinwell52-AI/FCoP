# ADR-0026: Review.human_approval — 人工审批子结构

- **Status**: Accepted
- **Date**: 2026-05-10
- **Deciders**: ADMIN
- **Related**: [ADR-0025](./ADR-0025-review-needs-human.md), [ADR-0023](./ADR-0023-agent-layer-governance-field.md), [Issue #2](https://github.com/joinwell52-AI/FCoP/issues/2)

## TL;DR

**中文**：在 REVIEW frontmatter 中加入可选子结构 `human_approval`，记录人工审批事件（审批人、决策、时间、渠道、审计证据）。配合 `decision: needs_human` 实现闭环。引入 `Project.mark_human_approved()` API。

**English**: Adds optional `human_approval` sub-object to REVIEW frontmatter to record the human decision (approver, decision, timestamp, channel, evidence). Closes the loop opened by `decision: needs_human` (ADR-0025). Introduces `Project.mark_human_approved()`.

## Context

`decision: needs_human` 只表示"需要人工"，但没有"人工如何回应"的结构化记录。ADR-0026 填补这个缺口：

- 移动端 push → 人工查看任务/审核摘要 → 滑动批准 → relay 回写 `human_approval`
- CLI `fcop review approve <review-id>` → 同等效果，`channel: cli`
- 人工直接编辑 review.md → `channel: manual_file_edit`，证据字段可选

## Decision

### 字段定义

```yaml
# REVIEW frontmatter（可选，仅在 decision: needs_human 时出现）
human_approval:
  approver: ADMIN-01          # layer: admin 的 agent，必填
  decision: approve           # approve | reject，必填
  approved_at: "2026-05-10T23:30:00+08:00"  # datetime，必填
  channel: mobile             # mobile | cli | web | manual_file_edit，必填
  comment: "看了一遍没问题"    # 可选
  evidence:                   # 可选审计证据
    device_id: "iPhone-ABC"
    ip: "192.168.1.1"
    auth_method: session      # session | biometric | password
```

### 运行时合约

1. `human_approval.approver` 必须是 `layer: admin` 的 agent（防止 worker 自批）
2. 任何 `decision: needs_human` + `human_approval` 存在 → `status` 可从 `pending` 推进
3. `human_approval.decision: reject` → 整个 REVIEW `decision` 等效为 `rejected`
4. `human_approval.evidence` 字段可选，建议移动端/web 渠道填充以满足审计要求

### Python 实现

- `review.schema.json` 追加 `human_approval` 属性定义
- `models.py` 新增 `HumanApprovalChannel` enum、`HumanApprovalDecision` enum、`HumanApproval` dataclass、`HumanApprovalEvidence` dataclass
- `Review` dataclass 追加 `human_approval: HumanApproval | None = None`
- `Project.mark_human_approved(review_id, approver, decision, channel, comment=None, evidence=None)` → 读取现有 REVIEW 文件，写入 `human_approval` 子结构，返回更新后的 `Review`

## Consequences

- 纯加法，向后兼容
- 为 CodeFlow v2 的移动端审批工作流提供标准化存储格式
- `fcop-mcp` v1.1 新增 `mark_human_approved` MCP 工具
