---
protocol: fcop
version: 1
fcop_version: "1.0.0rc1"
session_id: "main-2026-05-09"
task_id: "TASK-20260509-013"
type: TASK
sender: "ADMIN"
recipient: "ME"
subject: "MIGRATION-1.0.md 用户向迁移指南"
date: "2026-05-09"
status: "done"
priority: "P1"
references:
  - "adr/ADR-0022-workspace-directory-convention.md"
  - "docs/MIGRATION-0.6.md"
  - "docs/releases/1.0.0-rc.1.md"
---

# TASK-20260509-013 — `MIGRATION-1.0.md` 用户向迁移指南

## 背景

ADR-0022 §"Tests Checklist" 最后一项："`MIGRATION-1.0.md` 必须有
'Workspace 迁移'段（含命令 + 风险说明）"。Phase 1（CLI）+ Phase 2
（Project workspace_dir 改造）已落地（TASK-008 + TASK-012），用户向
迁移指南是 ADR-0022 收尾。

## 范围

参考 `docs/MIGRATION-0.6.md` 的体例，写一份 0.7.x → 1.0 完整迁移
指南，覆盖：

1. workspace 目录变化（最大 breaking）+ 3 个选项 + 自动 detect 矩阵
2. 协议 framing 升级（"规则"→"协议层"）
3. 4 个新抽象（REVIEW / Failure / Boundary / Event）—— additive
4. JSON Schema 形式化（给写工具的人）
5. 5+ 常见踩坑
6. 估时表 + 进一步阅读链接

## 验收标准

1. `docs/MIGRATION-1.0.md` 存在
2. 涵盖 ADR-0022 §"Tests Checklist" 要求的"Workspace 迁移"段
3. 提供 escape hatch（`workspace_dir="docs/agents"`）的完整说明
4. 列出 `fcop migrate-workspace` 命令 + dry-run / `--apply` / 风险
5. 区分"协议 framing"/"workspace"/"4 新抽象" 3 条独立 breaking 轴
6. README.md / README.zh.md 头部加 callout 指向新指南
7. ADR-0022 Tests Checklist + Sign-off 标记完成
8. CHANGELOG `[Unreleased]` 段记录本次变更

## 优先级理由

ADR-0022 是 v1.0 唯一的物理 breaking。无用户向迁移指南，0.7.x 用户
升级会迷茫——尤其是企业用户与下游集成方（CodeFlow / Bridgeflow）。
final tag 之前必须落地。

## 时间盒

D0（2026-05-09），单 session 完成。
