---
protocol: fcop
version: 1
sender: ADMIN
recipient: ME
priority: P0
thread_key: fix-init-v3-topology-3.0.2
subject: 修复 FCoP 3.0 init 不创建 _lifecycle/ 的协议层 bug（发版 3.0.2）
---

# 任务 · 修复 FCoP 3.0 init 协议层 bug

## 背景

FCoP 3.0.0/3.0.1 spec §1.1 钦定 v3 项目 MUST 有 `_lifecycle/{inbox,active,review,done,archive}/`，但 `Project._apply_init`(`src/fcop/project.py:924-931`) 只创建 v2 五桶，未调 `ensure_lifecycle_dirs()`。所有 3.0.x 全新初始化的项目都不合规。详见 ISSUE-20260522-001-ME。

完整草案见 `.fcop/proposals/TASK-004-draft-fix-init-v3-topology.md`（ADMIN 已确认 v2 版本）。

## 钦定方案

- **A1**：`_apply_init` 默认落 v3 拓扑，按 spec §6 不再创建 `tasks/` / `log/`，保留 `reports/` / `issues/` / `shared/`。
- **MCP tools 同步纳入本 task**。
- **版本号 3.0.2**（patch，对齐 spec 既有承诺，非 breaking）。
- **v3+C**：LETTER 不回滚 v3 承诺；audit 加 `_scan_lifecycle_topology_compliance()`。

## 实施范围

### 4.1 代码

修改 `src/fcop/project.py::_apply_init` line 924-931：
- 删除 `self.tasks_dir`、`self.log_dir` 的 `mkdir`。
- 调用 `from fcop.lifecycle.state import ensure_lifecycle_dirs; ensure_lifecycle_dirs(self._workspace_root / '_lifecycle')`。
- 保留 `reports_dir` / `issues_dir` / `shared_dir`。

### 4.2 单元测试

新建 `tests/test_init_v3_topology.py`：
- `test_init_solo_creates_lifecycle()` —— 五子桶必须存在。
- `test_init_project_creates_lifecycle()` —— 同上（dev-team）。
- `test_init_custom_team_creates_lifecycle()` —— 同上。
- `test_init_v3_does_not_create_tasks_dir()` —— `tasks/` 不存在。
- `test_init_v3_does_not_create_log_dir()` —— `log/` 不存在。
- `test_init_v3_keeps_reports_issues_shared()` —— 三桶必须存在。
- `test_is_v3_after_init()` —— `Project.is_v3` 返回 True。

`pytest tests/` 全绿。

### 4.3 audit 层

新建 `_scan_lifecycle_topology_compliance()`：
- v3 协议号但缺 `_lifecycle/` → P0 violation，建议 `python -m fcop migrate --to-v3` 或重新 init。
- v3 项目残留 `tasks/` / `log/` → P1 hygiene warning。
- 单元测试覆盖：v3 完整 / v3 缺 / v3 残留 v2 桶 / v2 项目（无 violation）。

### 4.4 文档

- `fcop/LETTER-TO-ADMIN.md`：保留 v3 承诺，加一句"3.0.2 起 fresh init 立即兑现"。
- `README.md`：补 3.0 安装节 + 两条路径（init / migrate）+ 升级指南。
- `docs/getting-started.md`：同步两条路径。
- `mcps/user-fcop/tools/*.json` 中 `init_solo` / `init_project` / `create_custom_team` 描述加"v3 拓扑"字样。

### 4.5 发布

- 版本：3.0.2 patch。
- CHANGELOG.md 加 3.0.2 节，引用 ISSUE-001 / TASK-004 / REPORT-004。
- 发布前：`pytest tests/` 全绿 + `fcop_audit(scope=takeover)` 自检通过。

## 风险（Rule 7）

- **risk_level: high**（协议核心初始化路径 + audit + LETTER）。
- 改动落 git 分支 `fix/init-v3-topology`，CI 不绿不 merge。
- 回滚：`pip install fcop==3.0.1`；3.0.2 删除目录改动不可逆但只影响 fresh init，已存在项目不受影响。
- **needs_human_approval: true**：risk=high 自动触发，发版前 ADMIN 必须 `mark_human_approved`。

## 验收标准

1. `pytest tests/` 全绿，含新加测试。
2. fresh `init_solo` / `init_project` / `create_custom_team` 之后磁盘上有 `_lifecycle/{inbox,active,review,done,archive}/` + `reports/` + `issues/` + `shared/`，无 `tasks/` 无 `log/`。
3. `fcop_audit` 在 v3 项目缺 `_lifecycle/` 时报 P0；在 v3 项目残留 v2 桶时报 P1。
4. LETTER / README / docs / MCP tool descriptions 全部对齐 v3 拓扑承诺。
5. CHANGELOG 3.0.2 节落地。
6. ADMIN `mark_human_approved` 后才发版。

## 完成后

- 写 REPORT-20260522-004-ME-to-ADMIN。
- 归档 TASK-004。
- 关 ISSUE-20260522-001-ME。
- 在本仓跑 `python -m fcop migrate --to-v3` 升夹生项目。