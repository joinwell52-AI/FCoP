---
protocol: fcop
version: 1
fcop_version: "1.0.0rc1"
session_id: "main-2026-05-09"
report_id: "REPORT-20260509-013"
type: REPORT
sender: "ME"
recipient: "ADMIN"
ref_task: "docs/agents/log/tasks/TASK-20260509-013-ADMIN-to-ME.md"
date: "2026-05-09"
status: "done"
---

# REPORT-20260509-013 — `MIGRATION-1.0.md` 用户向迁移指南完成

## 一句话结论

`docs/MIGRATION-1.0.md` 落地（≈ 250 行，8 章节）；README 双语 callout
就位；ADR-0022 全量收尾。距离 v1.0.0 final tag 仅余文档级 + git tag
工作。

## 验收标准 8/8 全部满足

| # | 标准 | 证据 |
|---|---|---|
| 1 | 文件存在 | `docs/MIGRATION-1.0.md`（新增）|
| 2 | "Workspace 迁移"段 | §2（4 个 sub-sections：选项 A/B/C + auto-detect 矩阵 + workspace_layout API + rollback）|
| 3 | escape hatch 完整说明 | §2.2 选项 B + §5.4 monorepo |
| 4 | `fcop migrate-workspace` 命令 + 风险 | §2.2 选项 A 含命令 + 顾问扫描行为 + git mv 历史保留 |
| 5 | 3 条独立 breaking 轴 | §0 心智模型表 + §1（framing）/ §2（workspace）/ §3（4 新抽象）独立章节 |
| 6 | README 双语 callout | `README.md:247` + `README.zh.md:230` 头部新增 v1.0 升级 callout，与既有 0.5.x 升级 callout 并列 |
| 7 | ADR-0022 Tests Checklist + Sign-off 更新 | `adr/ADR-0022-workspace-directory-convention.md` Tests Checklist 最后一项 ✅；`v1.0 RC Implementation Notes` Phase 2 段尾追加 MIGRATION-1.0.md 已交付；Sign-off ME 行更新为"ADR-0022 全量完成" |
| 8 | CHANGELOG `[Unreleased]` 记录 | `CHANGELOG.md` `[Unreleased]` 新增 "Added — docs" 段含 `docs/MIGRATION-1.0.md` + README 双语 callout 条目 |

## 设计决策

### 体例参考 `MIGRATION-0.6.md` 但不照搬

`MIGRATION-0.6.md` 的"人视角 vs agent 视角"二分法是 0.6 引入"严格
模式"的核心心智模型，并不直接适用于 1.0——1.0 的核心是"3 条独立
breaking 维度"（framing / workspace / 4 新抽象）。本指南改用 §0 心
智模型表来开题，明确告诉读者"你只需要关心你处于哪条轴"，避免一上
来就被 `is_initialized` / `list_*` 严格性这种 0.6 议题裹挟。

### Walkthrough vs reference

每个新抽象（§3）只给最简代码示例 + ADR/schema 链接，**不复制粘贴
完整 API 文档**。理由：完整 API 表在 `spec/fcop-runtime-protocol-v1.0.md`
和各 ADR 里已经有了；MIGRATION 文档目的是让读者"知道有这东西、
知道开关在哪、知道在哪深读"，不是替代 spec。

### Rollback 段的安全保证（§2.5）

明确写"迁移工具不会动 .git/，rollback 安全"。这是 ADR-0022
§"Design Details" 隐含的 invariant，但用户向文档应该明示——避免
有人因为不放心而干脆不跑迁移。

### 时间线参考表（§6）

把不同状态用户的迁移工时做成估时表（0 分钟到 4 小时）。这是
`MIGRATION-0.6.md` 没做的——0.6 没有"零成本路径"，1.0 有（选项 B），
所以估时表对说服用户尝试很重要。

### README callout 与 0.5.x callout 并列

同时保留 0.5.x → 0.6 的旧 callout，新增 0.7.x → v1.0 callout 列在
其上方。这样跨版本跳级用户（如 0.5 → 1.0）能依次读两份指南。

## 文件统计

| 文件 | 行数 | 说明 |
|---|---|---|
| `docs/MIGRATION-1.0.md` | ~250 | 新建，8 章节 |
| `README.md` | +2 | 头部 callout |
| `README.zh.md` | +2 | 头部 callout |
| `adr/ADR-0022-workspace-directory-convention.md` | +5 | Tests Checklist / Implementation Notes / Sign-off 三处微调 |
| `CHANGELOG.md` | +14 | `[Unreleased]` 段新 "Added — docs" block |

## 后续工作

ADR-0022 全量交付。**下一步**：

- **TASK-011 final** —— 去 `docs/releases/1.0.0.md` DRAFT marker +
  打 `v1.0.0` final tag + GitHub Release + Zenodo DOI bump

到此 v1.0 final 之前的所有工程工作就绪；剩下的全是 release 流程
（destructive op，需 ADMIN 确认）。
