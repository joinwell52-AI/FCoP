---
protocol: fcop
version: 1
type: TASK
sender: ADMIN
recipient: ME
date: 2026-05-09
priority: P1
status: in_progress
subject: 重 emit fcop-rules.mdc / fcop-protocol.mdc 反映 v1.0
ref_charter: adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md
ref_predecessor: docs/agents/log/tasks/TASK-20260509-Z01-ADMIN-to-ME.md
acceptance_criteria_count: 5
---

# TASK-20260509-010-ADMIN-to-ME

> Solo 模式任务。RC 阶段必须把宿主级 rule 文件升级以反映 v1.0 reframing 与
> 4 个新抽象。范围控制：rules.mdc 加正式 Rule 9（4 子段）；protocol.mdc
> 仅加 pointer，详细 commentary 留 final。

---

## 1 · 为什么需要这个任务

`fcop-rules.mdc` / `fcop-protocol.mdc` 是 FCoP 部署到用户项目的协议
**操作面**——任何 Cursor / Claude / Codex agent 都会自动读到。v1.0
新增的 REVIEW / Boundary / Failure / Event 4 抽象如果不在这两个文件
里有规则化表达，agent 就无从知道这些能力存在或如何使用。

per ADR-0015 §execution roadmap：v1.0 ship 必须包含 mdc 重 emit。

## 2 · 决议

| # | 决议 | 理由 |
|---|---|---|
| 1 | rules.mdc 加 Rule 9，4 子段对齐 4 抽象 | 形式必须与既有 Rule 0..8 一致 |
| 2 | rules.mdc 1.8.0 → 1.9.0 | 严格 SemVer additive |
| 3 | protocol.mdc 加 pointer callout，不展开 | 1194 行 mdc 不能再加 commentary 进去；详细留 v1.0 final |
| 4 | protocol.mdc 1.6.0 → 1.7.0 | minor bump 反映新增 callout |
| 5 | 不动 Rule 0..8 主体 | additive expansion；既有规则全部继续生效 |

## 3 · 验收标准

1. ✅ rules.mdc 含 Rule 9 完整 4 子段（含双语正文）
2. ✅ rules.mdc frontmatter `fcop_rules_version: 1.9.0` + body changelog 顶部 1.9.0 段
3. ✅ protocol.mdc 顶部含 v1.0 capabilities pointer callout
4. ✅ protocol.mdc frontmatter `fcop_protocol_version: 1.7.0` + Protocol Version Log v1.7 段
5. ✅ `tests/test_fcop/test_rules_metadata_consistency.py` 全绿；全回归无新红

## 4 · 执行计划

| Round | 内容 |
|---|---|
| R1 | rules.mdc + protocol.mdc + CHANGELOG | `feat(rules):` |
| R2 | TASK-010 报告 + 归档 | `docs(workflow):` |

## 5 · self-review

- [x] 范围控制：rules 加正式规则，protocol 仅 pointer
- [x] 既有 Rule 0..8 主体不动
- [x] frontmatter ↔ body changelog 同步（既有 ISSUE-20260427-007
  防止 metadata drift 测试守门）
- [x] CHANGELOG 同步
