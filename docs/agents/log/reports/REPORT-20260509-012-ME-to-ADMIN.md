---
protocol: fcop
version: 1
fcop_version: "1.0.0rc1"
session_id: "main-2026-05-09"
report_id: "REPORT-20260509-012"
type: REPORT
sender: "ME"
recipient: "ADMIN"
ref_task: "docs/agents/log/tasks/TASK-20260509-012-ADMIN-to-ME.md"
date: "2026-05-09"
status: "done"
---

# REPORT-20260509-012 — ADR-0022 Phase 2: `Project()` workspace_dir 改造完成

## 一句话结论

ADR-0022 Phase 2 全量落地，commit `861713b`，回归 971 passed / 1
failed（pre-existing 与本次无关）。1.0.0 final 距离仅余文档级 + tag
工作。

## 验收标准 12/12 全部满足

| # | 标准 | 证据 |
|---|---|---|
| 1 | `Project.__init__` 接 `workspace_dir=` | `src/fcop/project.py:202-237` |
| 2 | 4 detect 场景行为正确 | `tests/test_fcop/test_project_workspace_dir.py::TestAutoDetect`（4 用例 PASS）|
| 3 | 仅 docs/agents/ → `DeprecationWarning` | `test_legacy_root_when_only_docs_agents_exists` PASS |
| 4 | 双存在 → `ConfigError` ABORT | `test_both_exist_raises_config_error` PASS |
| 5 | 显式 override 永不 warn / accepts relative + absolute | `TestExplicitOverride`（4 用例 PASS）|
| 6 | 8 properties derive from `self._workspace_root` | `TestPathPropertiesFollowWorkspace`（3 parametrize PASS）|
| 7 | LETTER 路径动态化 | `src/fcop/project.py:804`（line 改为 `self._workspace_root / "LETTER-TO-ADMIN.md"`）|
| 8 | MCP init reply 与文件落地一致 | `mcp/src/fcop_mcp/server.py::_letter_relpath` 新建 + 3 处 reply call site 改造 |
| 9 | 既有测试全过 | 971 passed, 1 pre-existing failure（`test_role_switch_via_write_report_also_warns`，硬编码 2026-04-27 日期）|
| 10 | 新测试套覆盖完整 | `test_project_workspace_dir.py` 15 用例全 PASS |
| 11 | ADR-0022 标 Phase 2 done + commit hash | `adr/ADR-0022-workspace-directory-convention.md` Tests Checklist + Implementation §Phase 2 + Sign-off 三段 update |
| 12 | CHANGELOG `[Unreleased]` 有条目 | `CHANGELOG.md:11-75` 新增 `[Unreleased]` 段 |

## 实施分阶段

| 轮次 | 内容 | commit |
|---|---|---|
| R1+R2+R3 合并 | `Project.__init__` 改造 + 路径 properties + MCP 调整 + 53 处既有测试期望 swap + 新建 15 用例测试套 | `861713b` |
| R4（本回合） | TASK + REPORT 文档 + ADR sign-off + CHANGELOG `[Unreleased]` | （本 commit）|

R1/R2/R3 合并的原因：路径 swap 是单原子动作，分两 commit 反而让中间
状态不可跑（既改 Project 又得改测试期望，否则 600+ 测试都红）。

## 关键设计决策

### `workspace_layout` property 的引入

ADR-0022 §"启动时 detect 行为" 没明示需要把 detect 结果对外暴露，
但实施时发现：
- 下游工具（如 `fcop migrate-workspace`、IDE plugin、CI 检查）需要知
  道当前项目处于哪种 layout 才能给出对的提示
- 把 detect 结果存成 instance attr 再暴露 read-only property 比每次
  调用 `_resolve_workspace_root` 重算成本低

值域 `"v1"` / `"legacy"` / `"explicit"` 三选一，与 ADR-0022 §"启动
时 detect 行为" 4 场景的对应：
- `"v1"`       → 场景 1 + 场景 4（fcop/ 存在或全空）
- `"legacy"`   → 场景 2（仅 docs/agents/）
- `"explicit"` → 任何 explicit override

### Drift parser ledger prefixes 动态化

原 `_LEDGER_RELATIVE_PREFIXES` 是模块级常量，hard-coded 4 条
`docs/agents/...`。Phase 2 改造后必须为 per-project 动态：
- v1 项目应识别 `fcop/{tasks,reports,issues,log}/` 为 in-ledger
- legacy 项目应识别 `docs/agents/...`
- explicit 项目应识别 `<custom>/...`

新引入 `_ledger_prefixes_for(project)` helper：从 `project.workspace_dir`
派生 own prefixes，**额外 union 进 historical `docs/agents/...` 集**。
理由：half-migrated 项目可能在 v1 layout 已落地后还有零星文件挂在
`docs/agents/` 下未清理；这些文件应继续报为 in-ledger 而非 hidden，
避免审计漏洞。

`_parse_git_porcelain` 接受 `ledger_prefixes` 形参（默认值=历史常量，
保持向后兼容），调用 site `Project._scan_drift` 显式传入
`_ledger_prefixes_for(self)`。

### 测试期望批量 swap 的安全性

48 + 5 = 53 处 hard-coded `"docs/agents/..."` 期望。一次性脚本
`.git/migrate_test_paths.py`（跑完即弃）：
- 精准列定 9 个 fcop test + 1 个 mcp test 文件
- 故意排除 `test_migrate_workspace.py`（migration 源）/
  `test_legacy_files_validate.py`（legacy fixture）/
  `test_encoding_schema.py`（raw schema）/ `test_audit_drift.py`
  （drift 字符串字面量）
- 替换规则：`"docs" / "agents"` → `"fcop"`，`"docs/agents/..."` →
  `"fcop/..."`，`"docs/agents"` → `"fcop"`

事后审计：`grep -rn 'docs/agents' tests/` 结果应只留排除清单中的文件，
确认 swap 范围严丝合缝。

## 回归数据

```
971 passed, 1 failed, 16 warnings in 37.58s
```

唯一 fail：`tests/test_fcop_mcp/test_role_lock.py::TestRoleLock::
test_role_switch_via_write_report_also_warns` —— `git stash` 状态
（即 Phase 2 未改前）也 fail，证明与本次无关，属 pre-existing
（测试硬编码 `TASK-20260427-001`，今天是 `2026-05-09`）。

PR / issue 拆分到 cleanup task 单独修。

## 后续工作

1. **TASK-013** —— `MIGRATION-1.0.md` 用户向迁移指南（拆 ADR-0022
   §"Tests Checklist" 最后一项）
2. **TASK-011 final** —— 去 `docs/releases/1.0.0.md` DRAFT marker +
   打 `v1.0.0` final tag + GitHub Release + Zenodo DOI bump

ADR-0022 至此全量交付（`MIGRATION-1.0.md` 是其外延文档，独立交付）。
