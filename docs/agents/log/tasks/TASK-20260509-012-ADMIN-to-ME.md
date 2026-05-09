---
fcop_version: "1.0.0rc1"
session_id: "main-2026-05-09"
task_id: "TASK-20260509-012"
sender: "ADMIN"
recipient: "ME"
date: "2026-05-09"
status: "done"
priority: "high"
references:
  - "adr/ADR-0022-workspace-directory-convention.md"
  - "src/fcop/project.py"
  - "mcp/src/fcop_mcp/server.py"
  - "tests/test_fcop/test_project_workspace_dir.py"
---

# TASK-20260509-012 — ADR-0022 Phase 2: `Project()` workspace_dir 改造

## 背景

`v1.0.0-rc.1` 已发布（commit `a... → main` + tag pushed）。ADR-0022
Phase 1（`fcop migrate-workspace` CLI）随 RC 落地。ADMIN 命令"继续推
进"，进入 RC → final 倒计时窗口。Known gaps 中体量最大的是 ADR-0022
Phase 2：把 `Project` 类的 hard-coded `docs/agents/` 路径全部改造为
可配置 + 自动 detect。

## 范围

实施 ADR-0022 §"Decision §1" + §"启动时 detect 行为" + §"Tests
Checklist" 中所有 deferred 项（`MIGRATION-1.0.md` 除外，那是 TASK-013）。

## 验收标准

1. `Project.__init__` 接受 `workspace_dir=` kwarg
2. 4 种 detect 场景（仅 fcop/、仅 docs/agents/、双存在、双不存在）
   行为符合 ADR-0022 §"启动时 detect 行为"
3. 仅 docs/agents/ 时打 `DeprecationWarning`，不 raise
4. 双存在时 `ConfigError` ABORT
5. 显式 override 永不 warn，relative 与 absolute 路径都接受
6. 8 个公开路径 properties 全部 derive from `self._workspace_root`
7. `LETTER-TO-ADMIN.md` 落盘路径动态化（fcop/ vs docs/agents/）
8. MCP server init reply 中 LETTER 路径与文件实际位置一致
9. 既有测试套全部通过（接受 RC 之前已存在的 1 个 pre-existing fail）
10. 新增 `tests/test_fcop/test_project_workspace_dir.py` 覆盖 4 detect
    + explicit override + path derivation invariant + is_initialized
    scoping + end-to-end init under custom workspace
11. ADR-0022 标记 Phase 2 已完成，含 commit hash + 测试覆盖证据
12. CHANGELOG 在 `[Unreleased]` 段记录本次变更

## 交付物

R1+R2+R3 合并 commit：`861713b`
- `src/fcop/project.py` — `__init__` + `_resolve_workspace_root` +
  路径 properties + ledger prefix dynamic
- `mcp/src/fcop_mcp/server.py` — init reply LETTER 路径动态化
- `tests/test_fcop/test_project_workspace_dir.py` — 新建 15 用例
- 9 fcop test 文件 + mcp test_server.py — 53 处期望 swap
- `tests/test_fcop/snapshots/public_surface.json` — 新增字段

R4：本 TASK 文档 + REPORT + ADR sign-off + CHANGELOG `[Unreleased]`

## 优先级理由

ADR-0022 Phase 2 是 known gaps 中体量最大的工程项（30+ 处路径 +
600+ 既有测试可能撞红）。Phase 2 完成后，1.0.0 final 仅余文档级工作
（`MIGRATION-1.0.md` + 去 1.0.0.md DRAFT marker + tag），风险下降到
非协议层级。

## 时间盒

D0（2026-05-09）单日完成 Phase 2。
