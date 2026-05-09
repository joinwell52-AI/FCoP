---
protocol: fcop
version: 1
type: REPORT
sender: ME
recipient: ADMIN
date: 2026-05-09
status: done
ref_task: docs/agents/log/tasks/TASK-20260509-008-ADMIN-to-ME.md
subject: TASK-008 完成 —— migrate-workspace CLI 落地（ADR-0022 Phase 1）
---

# REPORT-20260509-008-ME-to-ADMIN

> TASK-008 完成报告。3 commits 收口；ADR-0022 Phase 1 全部 8 项验收
> 标准 ✅；Phase 2（Project workspace_dir + detect）显式 deferred 到
> v1.0 final 之前的独立 task。

---

## 1 · TL;DR

- **3 commits**：R1 = 实现+测试；R2 = ADR+CHANGELOG；R3 = 本 report+归档
- **+1162 / -18** 行；7 文件（4 新增 / 3 修改）
- **测试**：新增 25 用例（`test_migrate_workspace.py`）+ 1 用例放宽
  （`test_compat_cli.py`）
- **回归**：`pytest tests/ -q` → 963 passed（含本 task 25 新）；
  唯一 fail 是 fcop-mcp 已知 pre-existing red，与本 task 无关
- **范围**：仅交付 ADR-0022 Phase 1（CLI 本身 + entry point bump），
  Phase 2（Project 改造）显式 deferred；理由见 ADR-0022 §v1.0 RC
  Implementation Notes

## 2 · 8 项验收标准（acceptance）

| # | 标准 | 状态 |
|---|---|---|
| 1 | `fcop migrate-workspace --help` 退 0、列出选项 | ✅ |
| 2 | dry-run 不动盘，输出 `[dry-run]` summary | ✅ |
| 3 | `--apply` 实际移动 + 写 breadcrumb | ✅ |
| 4 | git-aware：tracked path 自动 git mv，git status 可见 | ✅ |
| 5 | 已迁移 tree 上 `--apply` 是 no-op 退 0 | ✅ |
| 6 | both-exist 时 `--apply` 退 2 ABORT 不动盘 | ✅ |
| 7 | 顾问扫描列出 .gitignore / README.md 等 | ✅ |
| 8 | bare `fcop` 仍打 0.5→0.6 legacy 信息退 1 | ✅ |

## 3 · 交付物（deliverables）

### 新增模块（3 文件）

| 文件 | 行数 | 职责 |
|---|---|---|
| `src/fcop/cli/__init__.py` | ~15 | namespace 占位 + docstring |
| `src/fcop/cli/_main.py` | ~63 | subcommand 派发器 + 0.5→0.6 legacy fallback |
| `src/fcop/cli/migrate_workspace.py` | ~340 | plan/apply/render + argparse glue |

### 测试（1 新增 + 1 调整）

| 文件 | 用例 | 调整 |
|---|---|---|
| `tests/test_fcop/test_migrate_workspace.py` | 25 (新) | TestPlan 7 / TestApply 6 / TestRenderSummary 3 / TestCli 6 / TestRunStandalone 2 |
| `tests/test_fcop/test_compat_cli.py` | 5 → 5 | `test_console_script_resolves_to_cli_main` 放宽接受 v1.0 + v0.7 entry |

### 文档（3 修改）

| 文件 | 改动 |
|---|---|
| `pyproject.toml` | console-script entry → `fcop.cli._main:main` |
| `adr/ADR-0022-workspace-directory-convention.md` | Tests Checklist 打勾 + Implementation 段 + Phase 1/2 拆分注 + Sign-off 更新 |
| `CHANGELOG.md` | `[1.0.0-rc.1]` 新增 "Added — fcop CLI" 子段 |

### 任务文件（1 新增 + 1 归档）

| 文件 | 状态 |
|---|---|
| `docs/agents/tasks/TASK-20260509-008-ADMIN-to-ME.md` → `docs/agents/log/tasks/...` | 归档 |
| `docs/agents/log/reports/REPORT-20260509-008-ME-to-ADMIN.md` | 本文 |

## 4 · 设计决策（与 ADR-0022 的差异）

| ADR-0022 原描述 | 本 task 实际落地 | 理由 |
|---|---|---|
| `Project()` 检测到 `docs/agents/` 时 warning + 提示 | **deferred 到 Phase 2** | 牵动 30+ 处 hard-coded 路径 + 600+ 测试，与 RC tag 风险隔离 |
| `Project()` init 默认创建 `fcop/` | **deferred 到 Phase 2** | 同上 |
| MCP `init_project` tool 创建 `fcop/` | **deferred 到 Phase 2** | 依赖 `Project()` 改造 |
| `MIGRATION-1.0.md` 含 "Workspace 迁移" 段 | **deferred 到 v1.0 final** | 应与 Phase 2 一并交付，避免出现后被 Phase 2 改写 |

> 所有 deferred 项已写进 ADR-0022 §v1.0 RC Implementation Notes，
> Sign-off 段也注明 "Phase 2 待 v1.0.0 final 前独立 task"。

## 5 · 风险回顾

| 风险 | 实际表现 | 缓解 |
|---|---|---|
| 既有测试受 entry point 变更影响 | `test_console_script_resolves_to_compat_cli` 假红 | 重命名 + 接受新旧两个 entry value，加历史 docstring |
| Windows 路径分隔符 | git mv 用 `as_posix()` + replace | 在所有 git 子进程调用前归一化 |
| 顾问扫描误报 prose | 3 用例显式断言 | 仅列出不改写，risk 控制 |
| Editable install 缓存 | `entry_points` 仍是旧值 | 测试已宽容；用户 reinstall 后即生效 |

## 6 · 下一 task 候选

按 user 顺序 1-2-3-4 → 接下来：

| # | task | 内容 |
|---|---|---|
| 3 | **TASK-Z01** | 双语补齐（核心文档优先：getting-started / homepage / spec / ADR-0015..0022） |
| 4 | **TASK-009** | 回 GitHub Issue #2（v1.0 reframing 完成通告） |
| 4 | **TASK-010** | 重 emit `fcop-rules.mdc`：反映 v1.0 + 加 REVIEW/Boundary/Failure/Event 段 |
| - | **TASK-011 final** | 实际打 v1.0.0-rc.1 git tag + Zenodo DOI bump（最后） |

> Phase 2（Project workspace_dir 改造）作为单独 task 排在 v1.0 final
> 之前；不在本批次 1-2-3-4 内。

## 7 · self-review

- [x] 8 项验收 100% 通过
- [x] 3 commits 收口（R1/R2/R3 模板）
- [x] 全回归无新红
- [x] ADR-0022 status / Tests Checklist / Sign-off 同步
- [x] CHANGELOG `[1.0.0-rc.1]` 段同步
- [x] 范围控制（Phase 1 only）显式记入 ADR
- [x] task 归档；report 落入 log/reports/
