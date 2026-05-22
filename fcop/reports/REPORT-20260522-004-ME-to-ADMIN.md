---
protocol: fcop
version: 1
sender: ME
recipient: ADMIN
priority: P0
thread_key: fix-init-v3-topology-3.0.2
parent: TASK-20260522-004-ADMIN-to-ME
related: [ISSUE-20260522-001-ME, REPORT-20260522-003-ME-to-ADMIN]
subject: 修复 FCoP 3.0 init 不创建 _lifecycle/ 的协议层 bug — 3.0.2 准备就绪
---

# REPORT · 修复 FCoP 3.0 init 协议层 bug（发版 3.0.2 ready）

## 摘要

TASK-004 全部 6 条验收标准达成。fcop / fcop-mcp 两包均已升级到 3.0.2，
`pytest` 全绿（1209 passed, 3 skipped），文档/MCP/LETTER/README/CHANGELOG
均已对齐 v3 拓扑承诺。**待 ADMIN 触发 `mark_human_approved` + git
commit + 发版**。

## 验收对照

### 验收 1 · pytest 全绿（含新测试）✅

```
1209 passed, 3 skipped, 1 warning in 17.26s
```

新增 `tests/test_init_v3_topology.py` 共 7 个测试，全部通过：
- `test_init_solo_creates_lifecycle`
- `test_init_project_creates_lifecycle`
- `test_init_custom_team_creates_lifecycle`
- `test_init_v3_does_not_create_tasks_dir`
- `test_init_v3_does_not_create_log_dir`
- `test_init_v3_keeps_reports_issues_shared`
- `test_is_v3_after_init`

历史测试（`test_lifecycle/test_project_v3_writes.py` 等）通过显式
`_seed_v2_legacy` 帮助函数继续覆盖 v2 兼容路径。

### 验收 2 · fresh init 落 v3 拓扑 ✅

`Project._apply_init` (`src/fcop/project.py`) 现在：
- 调用 `ensure_lifecycle_dirs(self._workspace_root)` 创建
  `_lifecycle/{inbox,active,review,done,archive}/`。
- 保留 `reports/` / `issues/` / `shared/` 三个 v2 桶。
- **不再**创建 `tasks/` 与 `log/`（spec §6 钦定它们已被 `_lifecycle/`
  顶替）。
- 创建后刷新 `self._topology` 缓存，使 `is_v3` 立即返回 `True`。

配套修改：
- `core/events.py::scan_workspace` 加入 `_lifecycle/` 五子桶扫描。
- `Project.role_occupancy()` 对 v3 项目从 `_lifecycle/archive/`
  统计 archived 任务计数。

### 验收 3 · audit 检测 ✅

新增 `Project._scan_lifecycle_topology_compliance()`（D9 scan）：
- **P0** `LIFECYCLE_TOPOLOGY_MISSING`：`fcop.json` 存在但既无
  `_lifecycle/` 也无 v2 内容 → "项目空壳"，建议重 init 或迁移。
- **P1** `LIFECYCLE_TOPOLOGY_MIXED`：`_lifecycle/` 与 v2 `tasks/`+`log/`
  共存且 v2 桶含文件 → 建议 `migrate --to-v3`。
- v3 完整 / 纯 v2 / v3 残留空 v2 桶：均无 violation。

接入 `Project.audit()` 主流程，3 个新单元测试覆盖各分支。

### 验收 4 · 文档对齐 ✅

| 文件 | 改动 |
|---|---|
| `src/fcop/rules/_data/letter-to-admin.zh.md` | 目录图改 v3 拓扑；加 3.0.2 节"fresh init 立即兑现 v3 承诺 + 3.0.0/3.0.1 走 migrate" |
| `src/fcop/rules/_data/letter-to-admin.en.md` | 同上英文版 |
| `fcop/LETTER-TO-ADMIN.md` | 调 `_deposit_letter(force=True)` 重新部署 |
| `docs/getting-started.md` | 目录树更新 + 加"Two paths"小节 + 示例任务路径改 `_lifecycle/inbox/` |
| `README.md` | release badge 升 3.0.2；版本表加 3.0.2 行；首部"Two paths" + 3.0.0/3.0.1 bug 说明 |
| `mcp/src/fcop_mcp/server.py` | `init_solo` / `init_project` / `create_custom_team` docstring 全部加"v3 拓扑（since 3.0.2）"段 |

### 验收 5 · CHANGELOG 3.0.2 节 ✅

`CHANGELOG.md` 顶部新增 `[3.0.2] - 2026-05-22` 节，含：
- Fixed: `_apply_init` 现在创建 v3 `_lifecycle/` 拓扑（spec §1.1 对齐）。
- Added: D9 audit scan、tests/test_init_v3_topology.py。
- Changed: docs/MCP/LETTER/README 全部对齐 v3。
- Migration: 3.0.0/3.0.1 fresh-init 项目用 `fcop migrate --to-v3`。
- 引用 TASK-004 / ISSUE-001 / REPORT-004。

### 验收 6 · 待 ADMIN `mark_human_approved` ⏸

TASK-004 frontmatter 风险等级 `high`，按 Rule 9.5.1 写 task 时已经
自动 emit `decision=needs_human` 的 REVIEW（如 `write_task` 工具自动
触发）。**发版动作（git commit / tag / publish）等 ADMIN 触发**。

## 版本号

| 包 | 旧 | 新 |
|---|---|---|
| `fcop` | 3.0.1 | **3.0.2** (`src/fcop/_version.py`) |
| `fcop-mcp` | 3.0.1 | **3.0.2** (`mcp/src/fcop_mcp/_version.py`) |

SemVer 释义：API surface 与 3.0.1 一致，init 行为是"对齐 spec 既有
承诺"而非破坏性变更，归 patch。

## 风险与回滚

- 改动只影响 **fresh init** 与 **audit** 两条路径。
- 已存在的 v2 / v3 项目不受影响（不会动磁盘上的 `tasks/` / `log/`）。
- 回滚：`pip install fcop==3.0.1` 并保留迁移工具（migrate 在 3.0.1
  里就已经存在）。
- 已知未跟进的从属 bug（不阻塞本次发版）：
  - 自动生成的 REVIEW 文件目前落到 `reviews/` 而非 `_lifecycle/review/`。
    需要后续单独 task 修。

## 后续动作（待 ADMIN 触发）

1. **mark_human_approved**：批准 TASK-004 关联的 needs_human REVIEW。
2. **git commit + tag 3.0.2**：标准发版流程。
3. **publish**：`fcop` + `fcop-mcp` 同步发到 PyPI。
4. **D:\FCoP 自迁移**：`fcop migrate --to-v3 --apply`（dry-run 显示
   84 个文件待迁移；这是 destructive 操作，按 Rule 7 等 ADMIN 单独
   确认）。
5. **关 ISSUE-001**：补一行 "fixed in 3.0.2 via TASK-004"。
6. **archive_task TASK-004**。

## 引用

- `src/fcop/project.py::_apply_init` —— 主修复点。
- `src/fcop/project.py::_scan_lifecycle_topology_compliance` —— D9 scan。
- `tests/test_init_v3_topology.py` —— 7 个新测试。
- `CHANGELOG.md` §[3.0.2]。
- 命令实测：`fcop migrate --to-v3` (dry-run) 在本仓输出 "files to move: 84"。
- 命令实测：`python -m pytest -q` → "1209 passed, 3 skipped".
