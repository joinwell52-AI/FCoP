---
protocol: fcop
version: 1
type: TASK
sender: ADMIN
recipient: ME
date: 2026-05-09
priority: P0
status: in_progress
subject: migrate-workspace CLI（ADR-0022 Phase 1）—— v1.0 RC 必交付物
ref_charter: adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md
ref_adr: adr/ADR-0022-workspace-directory-convention.md
ref_predecessor: docs/agents/log/tasks/TASK-20260509-007-ADMIN-to-ME.md
acceptance_criteria_count: 8
---

# TASK-20260509-008-ADMIN-to-ME

> Solo 模式任务。`fcop@1.0.0-rc.1` release prep 之后的第一个收尾 task。
> ADR-0022 §"自动迁移工具"的 must-have 交付物。

---

## 1 · 为什么需要这个任务（why now）

ADR-0022 §"Decision §3" 明确："必须配自动迁移工具——`fcop migrate-workspace`
命令一键迁移"。这是 v1.0 把默认 workspace 从 `docs/agents/` 迁到 `fcop/`
的 **breaking change** 的安全网；没有它 0.7.x 用户升级 v1.0 必须手工 mv +
git mv，体验破。

RC 阶段先把 CLI 自身落地（独立工具，不依赖 `Project` 改造），保证下游能
立即开始测试迁移路径；`Project()` 默认目录改造留 v1.0 final 之前的另一
个 task（避免一次撞 600+ 既有测试）。

## 2 · 决议（ADMIN solo 自定）

| # | 决议 | 理由 |
|---|---|---|
| 1 | **CLI = 独立子命令**，不依赖 Project 改造 | 范围控制；ADR-0022 §"启动时 detect 行为"是 Phase 2 |
| 2 | `fcop` console-script 升级为 subcommand 派发器 | argparse + lazy import；保留无参 = 0.5 legacy 信息 |
| 3 | 默认 dry-run，`--apply` 才动盘 | UX 防呆；ADR-0022 §"Decision §3" 显式 |
| 4 | git-aware：tracked path 自动 `git mv`，否则 shutil fallback | 保留 git 历史，per ADR-0022 §"Design Details" item 1 |
| 5 | 顾问扫描列出但不改写 `.gitignore` 等 | per ADR-0022 §"Design Details" item 3，避免误伤用户文档 |
| 6 | 留痕文件 `MIGRATED_FROM_DOCS_AGENTS.md` | 可发现 + 可回滚；含时间戳/版本号 |
| 7 | both-exist conflict 必 ABORT 退出 2 | per ADR-0022 §"启动时 detect 行为"——绝不自动合并 |
| 8 | Phase 2（`Project` workspace_dir 参数 + detect）defer | 范围控制 + 风险隔离；详见 ADR-0022 §v1.0 RC Implementation Notes |

## 3 · 验收标准（acceptance criteria）

1. ✅ `fcop migrate-workspace --help` 退出 0；列出所有选项
2. ✅ Dry-run 不动盘，输出 `[dry-run]` summary 含 source/target/strategy/entries
3. ✅ `--apply` 实际把 `docs/agents/` 移到 `fcop/`，并写 breadcrumb
4. ✅ git 工作区 + tracked path 时使用 `git mv`，保留历史；`git status` 可见
5. ✅ 已迁移的 tree 上 `--apply` 是 no-op，退出 0
6. ✅ both-exist 时 `--apply` 退出 2，不动盘，输出 `ABORT`
7. ✅ 顾问扫描列出 `.gitignore` / `README.md` 等含 `docs/agents` 的文件
8. ✅ bare `fcop`（无 subcommand）仍打印 0.5→0.6 legacy 信息，退出 1

## 4 · 执行计划（4-commit template）

| Round | 内容 | commit prefix |
|---|---|---|
| R1 | CLI 模块 + migrate_workspace.py + 25 测试 + entry point bump + legacy test 放宽 | `feat(cli):` |
| R2 | ADR-0022 状态更新 + Implementation 段 + sign-off | `docs(adr):` |
| R3 | TASK-008 报告 + 归档 task | `docs(workflow):` |

> 范围比 TASK-005..007 小（无 Project 改动），3 commits 即可收口。

## 5 · 风险（risks）

| 风险 | 缓解 |
|---|---|
| 既有 600+ 测试因 entry point 变更受影响 | 全跑 → 仅 1 pre-existing red，无回归（已验证） |
| Windows PowerShell 下 `git mv` 路径分隔符 | 用 `as_posix()` + `replace("\\", "/")` |
| Editable install 的 entry-points cache 不刷新 | 测试 `test_console_script_resolves_to_cli_main` 接受新旧两个值 |
| 顾问扫描误报 prose 中的 `docs/agents` | 按 ADR-0022 §"Design Details" item 3 显式不改写，仅列 |
| 用户在 dry-run 后忘加 `--apply` | summary 末尾打印 `Run again with --apply ...` 提示 |

## 6 · self-review

- [x] 仅交付 ADR-0022 Phase 1，Phase 2 显式 deferred 并写进 ADR
- [x] 默认 dry-run，UX 防呆
- [x] 既有 0.5→0.6 legacy 兼容信息保留
- [x] 不引入新 runtime 依赖（pure stdlib + subprocess）
- [x] 测试覆盖 plan / apply / render / CLI / standalone run 五条路径
- [x] 全回归 963 passed（含本 task 新增 25 用例），唯一 fail 为已知 pre-existing
