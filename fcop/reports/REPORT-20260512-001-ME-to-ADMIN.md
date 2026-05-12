---
protocol: fcop
version: 1
kind: report
report_id: REPORT-20260512-001
task_id: TASK-20260512-001
sender: ME
recipient: ADMIN
status: done
thread_key: fcop-mcp-binding-guard-20260512
session_id: sess-20260512-me-01
created_at: 2026-05-12T16:18:00+08:00
---

# TASK-001 完成报告 · fcop-mcp 1.4 Write-side 绑定守门

## 结论

**全部 D1-D6 已交付，测试全绿（34 passed / 2 skipped）。**

`fcop-mcp` 版本号已升至 `1.4.0`（待 ADMIN 确认后发 PyPI）。

---

## 交付清单

| Deliverable | 状态 | 关键文件 |
|---|---|---|
| D1 · write-side 工具显式绑定守门 | ✅ 完成 | `server.py` → `_assert_write_allowed()` |
| D2 · Protected path deny-list | ✅ 完成 | `server.py` → `_is_protected_path()` |
| D3 · `fcop_report()` 顶部告警 | ✅ 完成 | `server.py` → `_compose_session_report()` |
| D4 · write-side schema `binding_required` | ✅ 完成 | `@mcp.tool(tags={"binding_required"})` × 15 |
| D5 · 测试用例（TC-01 ~ TC-08）| ✅ 11 通过 / 2 跳过 | `mcp/tests/test_write_guard.py` |
| D6 · Release notes + CHANGELOG | ✅ 完成 | `docs/releases/1.4.0.md`, `CHANGELOG.md` |

---

## 实现要点说明

### D1 — `_assert_write_allowed(tool_name)` + `_get_project_write(tool_name)`

- write-side 工具调用 `_get_project_write()` 替代 `_get_project()`
- 仅 `"cwd fallback"` 源被拒绝；`auto:{marker}` 和 `env:FCOP_PROJECT_DIR` 正常通过
- 覆盖工具：`init_project` / `init_solo` / `create_custom_team` / `write_task` /
  `archive_task` / `write_report` / `write_issue` / `write_review` /
  `mark_human_approved` / `deploy_role_templates` / `new_workspace` /
  `drop_suggestion` / `fcop_audit` / `redeploy_rules` / `fcop_create_alert`（15 个）

### D2 — `_is_protected_path(path)`

- 判定：HOME 目录、APPDATA、LOCALAPPDATA 及其父目录
- Windows 盘符根（`path == path.parent`）
- Unix 根 + 系统目录（`/etc`、`/usr`、`/opt`、`/bin`、`/sbin`、`/lib`）
- PROGRAMDATA

**注意**：HOME **子目录**当前实现**放行**（D2 只加 HOME 自身，不扩展到子目录）。
这与 TASK-002 S2 的要求一致，但 `casefold()` 规范化尚未加入（→ TASK-002 遗留项）。

### D3 — `fcop_report()` 告警

`_protected_warning` 变量注入到：
- 未初始化分支（中英各 1）
- 已初始化 UNBOUND 分支（中英各 1）

### D4 — `tags={"binding_required"}`

用 Python 脚本批量修改了 `@mcp.tool` 装饰器为 `@mcp.tool(tags={"binding_required"})`，
FastMCP `tools/list` 响应中携带 `tags` 字段，可机器可读。

---

## 测试结果

```
mcp/tests/test_write_guard.py  11 passed, 2 skipped
mcp/tests/test_governance.py   23 passed
Total: 34 passed, 2 skipped, 0 failures
```

ruff: All checks passed  
mypy: no issues found in 1 source file

---

## 未处理范围（遗留至 TASK-002）

巡检时发现 `TASK-20260512-002-ADMIN-to-ME.md`（ADMIN 于 16:03 落盘），
三项细化 S1 / S2 / S3 **尚未实现**：

- **S1** — write-side 工具验证 `fcop.json` 存在（三步守门第 2 步）
- **S2** — HOME 子目录放行 + `casefold()` Windows 路径规范化
- **S3** — 统一 `_assert_writable_project()` 公共助手 + parametrize 测试

---

— ME, 2026-05-12 16:18 (UTC+8)
