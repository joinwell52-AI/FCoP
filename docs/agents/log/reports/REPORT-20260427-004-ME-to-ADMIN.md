---
protocol: fcop
version: 1
sender: ME
recipient: ADMIN
priority: P1
references:
- TASK-20260427-003
status: done
---

# ISSUE-003 修复交付——seq 生成器 union active+log/

## 状态

`status=done`。TASK-20260427-003 的全部交付物已落盘并通过测试。

## 交付清单（与 TASK-003 验收标准逐条对照）

| 验收项 | 落地证据 |
|---|---|
| 三份新测试绿 | `tests/test_fcop/test_project_tasks.py::test_seq_skips_archived_basename`、`test_project_reports.py::test_seq_skips_archived_basename`、`test_project_issues.py::test_seq_skips_archived_basename` 全绿 |
| 现有 587 passed 不退 | 598 passed（前述 +11 含本任务 +3）|
| ruff clean | `All checks passed!` |
| 被抢救的 002 双件不被误伤 | TASK-20260427-002 / REPORT-20260427-002 仍在 active；002 与 log/ 中的 001 不冲突 |

## 实现的关键代码动作

- `src/fcop/project.py`：抽出 `_existing_filenames_for_seq(*dirs)`
  私有 helper（`Iterator[str]` 生成器，跳不存在的目录），统一
  被三个 `write_*` 方法调用。
- `write_task` 调用为
  `_existing_filenames_for_seq(tasks_dir, self.log_dir / "tasks")`。
- `write_report` 调用为
  `_existing_filenames_for_seq(reports_dir, self.log_dir / "reports")`。
- `write_issue` 调用为
  `_existing_filenames_for_seq(issues_dir, self.log_dir / "issues")`。
- `next_sequence()` 本身保持纯函数语义不变——决定扫哪是调用者
  职责。

## 与设计的偏差

零偏差。候选 A（推荐方案）逐字落地；候选 B（tombstone 文件）与
候选 C（手册警告）按设计明确否决，未实现。

## 哲学位置

本 bug 是 ISSUE-002（双 ME 角色冲突）的同一架构裂缝的"另一面"：

- ISSUE-002：「角色占用必须从磁盘账本推得」——`tasks/` /
  `reports/` 在归档后只剩半部账本。
- ISSUE-003：同一半部账本被 seq 生成器忽略，归档后再写产生
  同名碰撞。

两个 issue 一起在 0.7.0 闭环——`role_occupancy` 与
`_existing_filenames_for_seq` 都在落实"`<type>/` + `log/<type>/`
合起来才是账本"的同一架构原则。

## 验证

```
.venv/Scripts/python.exe -m pytest tests/test_fcop/test_project_tasks.py::test_seq_skips_archived_basename tests/test_fcop/test_project_reports.py::test_seq_skips_archived_basename tests/test_fcop/test_project_issues.py::test_seq_skips_archived_basename -v
# 3 passed
```

## References

- 任务单：`TASK-20260427-003-ADMIN-to-ME.md`
- 配套 issue：`ISSUE-20260427-003-ME.md` (status=closed)
- 姊妹任务：`TASK-20260427-002-ADMIN-to-ME.md`（Rule 1 硬化）
- 发版说明：`docs/releases/0.7.0.md`
