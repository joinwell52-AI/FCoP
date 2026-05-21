---
protocol: fcop
version: 1
type: REVIEW
review_id: REVIEW-20260521-001-ADMIN-on-adr-0035
subject_type: code_change
subject_ref: adr/ADR-0035-lifecycle-directory-and-tool-layers.md
reviewer_role: ADMIN
decision: approved
decided_at: "2026-05-21T15:45:00+08:00"
subject: Sign-off FCoP 3.0 State Ontology ADR-0035
---

# FCoP 3.0 State Ontology (ADR-0035) Formal Review Sign-off

## 1. Rationale / 评审理据
- **收敛性与自洽性**：ADR-0035 收敛版已彻底消除所有“第二层语义系统”和解释性冗余。§1 仅定义最基础的拓扑桶（inbox, active, review, done, archive）、纯粹阶段释义（5个词）与硬跳转关系表（7条 Allowed Transitions）。
- **硬跳转约束**：Allowed Transitions 全面绑定具体的 L1 工具参数（如 `finish_task(skip_review=true)`），完全摒弃了“通过文件内容字段（如 `risk_level`）隐式推理路径”的自指、不可验证风险，全面满足 Rule C。
- **职责清晰分层**：
  - 成功解决了 Q1（`risk_level` 驱逐至 Exclusion Zone，直通显式化）。
  - 成功解决了 Q2（Scheduler `FixedTaskRunner` 不得拥有 Claim 状态特权，claim_task 保持 agent-exclusive）。
  - 成功解决了 Q3（TASK 与 PLAN 哲学切割，PLAN 进入 Intent 层，非 Lifecycle 对象）。
- **认知边界保护**：所有解释性的、指导人类的知识均降级为 NON-VERSION 下的 implementation appendix（工具层降级、Semantic Notes 科普化），达成了 “Only §1 defines version, others are commentary” 的 HARD BOUNDARY 治理原则。

## 2. Decision / 评审结论
- **Decision**: `approved`
- **Action**: ADR-0035 状态晋升为 **Accepted**，合入主干并载入 `adr/README.md`。FCoP 3.0 正式作为行为治理协议的 Canonical Spec。
