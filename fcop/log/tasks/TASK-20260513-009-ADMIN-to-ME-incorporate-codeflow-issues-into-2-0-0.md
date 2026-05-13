---
protocol: fcop
version: 1
kind: task
task_id: TASK-20260513-009
sender: ADMIN
recipient: ME
priority: P1
parent: TASK-20260513-008
related: [ISSUE-20260513-008, ISSUE-20260513-009, ISSUE-20260513-010]
thread_key: fcop-2-0-0-release-sprint
session_id: sess-20260513-me-c8_5
risk_level: medium
---

# 把 codeflow 上报的 3 个上游 bug 一并并入 fcop 2.0.0

## 背景

在 codeflow 跨项目巡检（TASK-20260513-003 / -004）中，扇出了 3 份针对
`fcop` 上游的 ISSUE：

- **ISSUE-008** · `fcop_audit` 不豁免 `_archive/` 与 `log/`，导致
  *合规* 的归档文件被误报 `P1-002 misplaced_envelope`（4 个 sub-case）。
- **ISSUE-009** · `_read_local_rules_version` 永远返回 `null`——
  函数在文件里搜 `"Rules version:"` 字面量，但实际版本字段是
  frontmatter 的 `fcop_rules_version:`。
- **ISSUE-010** · 四个预设团队的 `PM.md` 角色模板停留在 v1.3.0
  时代的内容，缺 `supersedes` / `risk_level` / **REVIEW envelope**
  三段——与 DEV/QA/OPS 模板（已含上述三段）失衡。

ADMIN 明确指示："加进去全部修复，合并为 2.0.0！"

## 范围 / Scope

将上述 3 个 ISSUE 的修复 **作为 sub-task** 加入 `2.0.0` sprint
（TASK-20260513-008），不开 `2.0.1` patch。

### 修复要点 / Fix Outline

1. **ISSUE-008** —— `src/fcop/project.py`
   - `_scan_misplaced_envelopes` 加桶豁免列表（`fcop/log/**`、
     `fcop/**/_archive/**`、`**/legacy-non-protocol/**`）。
   - `_scan_ghost_prefixes` 同步加豁免。
   - `InspectionReport` 加 `violation_file_count` 字段（distinct
     file count）+ frontmatter 渲染。

2. **ISSUE-009** —— `src/fcop/project.py`
   - `_read_local_rules_version` 改为：先按 YAML frontmatter 抓
     `fcop_rules_version:` 字段，找不到再 fallback 旧的
     `Rules version:` 哨兵（不破坏老 1.x 项目）。

3. **ISSUE-010** —— `src/fcop/teams/_data/{dev,media,mvp,qa}-team/roles/PM.{md,en.md}`
   - 对齐 DEV/QA/OPS 模板的三段：
     - `supersedes:` 用法
     - `risk_level:` 写入与升级路径
     - **REVIEW envelope** 写作时机与字段

## 验收 / Acceptance

- [ ] `pytest` 全过，回归 0。
- [ ] `fcop_audit` 在含 `fcop/log/` 与 `_archive/` 的项目（如本仓
      + codeflow）跑出来 `P1-002 = 0`（活动桶里仍正常扫）。
- [ ] `fcop_audit` 输出含 `fcop_rules_version_local: 3.0.0`（非 null）。
- [ ] 4 个团队的 PM.md / PM.en.md 同时含
      `supersedes:` / `risk_level:` / `REVIEW envelope` 三段（命中数与
      DEV.md 相当）。
- [ ] CHANGELOG.md `[2.0.0]` 段在 **Fixed** 子节列出三个 ISSUE。

## 回滚 / Rollback

三处修复都是非破坏性（豁免列表 = 软扩展，frontmatter 解析 = 向后
兼容，模板补丁 = 内容追加）。若某一项打破回归，按 Rule 5 追加
TASK-010 + `supersedes: TASK-009` 撤回该改动；老版本仍可
`pip install fcop==1.6.0` 回到上一个 stable。
