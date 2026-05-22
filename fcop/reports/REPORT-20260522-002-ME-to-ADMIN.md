---
protocol: fcop
version: 1
sender: ME
recipient: ADMIN
priority: P1
references:
- TASK-20260522-002
status: done
---

## 完成情况 / Completion

按 TASK-20260522-002 的批量授权 `batch_id: letter-3.0-sync-20260522` 完成 `fcop/LETTER-TO-ADMIN.md` 的 v3.0.1 同步重写。Option C 全文重构。

## 实际改动 diff 摘要 / Diff Summary

**目标文件**：`fcop/LETTER-TO-ADMIN.md`（单文件批量整改）

### 1. 顶部摘要块（v2.0.0 → v3.0.1）
- 旧：「v2.0.0 摘要 · 两图对偶纪元」
- 新：「v3.0.1 摘要 · 文件夹即状态纪元（v3.0.0，BREAKING）」
- 涵盖：`_lifecycle/` 五桶拓扑、7 类 transition、三层规则集、`python -m fcop migrate --to-v3` 升级路径、v3.0.1 path-consolidation patch、保留 v1.x/v2.0 已稳定能力
- 工具/资源数对齐 `docs/mcp-tools.md` L1：35 tools, 14 resources

### 2. 目录拓扑章节
- 旧：单棵 v2.x 目录树
- 新：双轨布局
  - 「v3.0 标准拓扑」：`_lifecycle/{inbox,active,review,done,archive}/` + `_events.jsonl` + reports/ append-only 注解
  - 「v2.x 兼容拓扑」：保留原 `tasks/ + log/`，明确标注「本仓库当前实际状态」
- 升级提示框：`pip install -U fcop>=3.0` + `python -m fcop migrate --to-v3` + 链向 `docs/MIGRATION-3.0.md`

### 3. 工具数（L533, L641 共 2 处）
- 「FCoP 有 32 个工具」→「FCoP 有 35 个工具」
- 「剩下的 24 个你用不到的可以灰」→「剩下的工具你用不到的可以灰」

### 4. 「四条必读规则」章节
- 保留原 0.a / 0.b / 0.c / Rule 1 表格（NOW 视角）
- 新增子节「v3.0 三层规则集（速查）」三行表：NOW Rule A · State / PAST Rule E · Event / META Boundary Charter
- 收口提示：本仓库当前还在 v2.x 拓扑下，看到 `tasks/` 而不是 `_lifecycle/` 是正常的

### 5. 升级章节
- 横幅范例 `0.5.4 → 0.5.5` → `3.0.0 → 3.0.1`
- 新增区分三件事：包升级 (`pip install -U`) / 规则文件升级 (`redeploy_rules`) / 拓扑迁移 (`migrate --to-v3`)

### 6. 收尾「lint」性微调
- `_lifecycle/_events.jsonl` 从 fcop/ 顶层平级条目移到 `_lifecycle/` 子目录内（修正层级显示）

## 实证依据 / Citations

- 工具/资源数：`docs/mcp-tools.md` L1「35 tools, 14 resources — v1.5.0」
- v3.0 拓扑：`spec/fcop-3.0-spec.md` `_lifecycle/{inbox,active,review,done,archive}/` 节
- 迁移命令：`src/fcop/cli/_main.py` L36–L43 `migrate --to-v3` 子命令注册
- 当前仓库状态：`Get-ChildItem fcop -Directory` 实测显示 `tasks/ reports/ issues/ shared/ log/ reviews/`，**无 `_lifecycle/`**
- 版本号：`CHANGELOG.md` L1 实证 v3.0.1 (2026-05-21) 紧跟 v3.0.0
- `fcop_report()` 本会话输出实证：fcop/fcop-mcp 包内 3.0.1，rules/protocol 项目本地 3.0.0

## 未做范围 / Out of Scope

- 未触发 v3.0 实际迁移（本仓库继续按 v2.x 工作）
- 未改 `LETTER-TO-ADMIN.en.md`（如存在）
- 未改其他需要 v3.0 同步的文档（越界须先停下来跑 drop_suggestion）

## 验收清单 / Acceptance

- [x] 顶部摘要明确反映 v3.0.1 + v3.0.0 是协议级 BREAKING
- [x] 目录拓扑同时展示 v3.0 标准 + v2.x 兼容
- [x] 提及 `python -m fcop migrate --to-v3`
- [x] Rule A / Rule E / Boundary Charter 三层概念以速查表出现
- [x] 工具计数 32 → 35 全文一致
- [x] 升级章节区分三件事
- [x] 不删除 ADMIN 已熟悉的 v1.x / v2.0 操作语义

## 下一步 / Next Step

建议 ADMIN 通读重写后的 `LETTER-TO-ADMIN.md`（特别是顶部摘要 / 目录双轨节 / v3.0 三层规则集速查）。验收后由 ADMIN 触发 `archive_task('TASK-20260522-002')` 完成 Rule 0.a.1 第 4 步。