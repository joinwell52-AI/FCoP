---
protocol: fcop
version: 1
sender: ADMIN
recipient: ME
priority: P1
subject: ISSUE-003 修复：write_task / write_report / write_issue 序号生成器 union-scan active
  + log/
references:
- ISSUE-20260427-003-ME.md; TASK-20260427-002-ADMIN-to-ME.md; src/fcop/project.py:1024
- '1468'
- '1710'
---

## 范围

针对 `ISSUE-20260427-003-ME.md`。修 `src/fcop/project.py` 中 `write_task` / `write_report` / `write_issue` 三个方法，使 next_seq 计算同时看 active 与 archived 两路径，防止归档后同名碰撞。

## 现场

三处 bug 同型，都在 retry 循环内：

```
src/fcop/project.py:1024-1026  write_task
  existing = (entry.name for entry in tasks_dir.iterdir() if entry.is_file())
  sequence = next_sequence(existing, date=date, kind="task")

src/fcop/project.py:1468-1473  write_report
  existing = (entry.name for entry in reports_dir.iterdir() if entry.is_file())
  sequence = next_sequence(existing, date=date, kind="report")

src/fcop/project.py:1710-1715  write_issue
  existing = (entry.name for entry in issues_dir.iterdir() if entry.is_file())
  sequence = next_sequence(existing, date=date, kind="issue")
```

三个 generator 都只查现役目录。在 archive_task 迁走 `tasks/` 同名任务后，`tasks/` 重变空，`next_sequence` 返回 1，与 `log/tasks/` 里的 001 同名。report 同型（archive_task 会连带 report 一起归档）。issue 现阶段没有 archive_issue 函数，但为对称与将来不被同型问题咔到，同步修。

## 修法

1. 在 `src/fcop/project.py` 加一个私有辅助函数：

   ```python
   def _existing_filenames_for_seq(
       *dirs: pathlib.Path,
   ) -> Iterator[str]:
       """Yield basenames of files under *all* given directories.

       Used to compute the next sequence for task/report/issue
       writes so that archived files in ``log/<type>/`` are taken
       into account and we never reuse a basename that is already
       on disk somewhere in the project ledger.
       """
       for d in dirs:
           if not d.is_dir():
               continue
           for entry in d.iterdir():
               if entry.is_file():
                   yield entry.name
   ```

2. `write_task` 里调用为 `_existing_filenames_for_seq(tasks_dir, self.log_dir / "tasks")`。
3. `write_report` 里调用为 `_existing_filenames_for_seq(reports_dir, self.log_dir / "reports")`。
4. `write_issue` 里调用为 `_existing_filenames_for_seq(issues_dir, self.log_dir / "issues")`。

O_EXCL 原子预占逻辑不变。retry 限不变。`next_sequence()` 本身不变。

## 测试

在 `tests/test_fcop/test_project_tasks.py`、`test_project_reports.py`、`test_project_issues.py` 中各加一个测试点：

```python
def test_write_task_seq_skips_archived_basename(tmp_path):
    # 预存入 log/tasks/TASK-{date}-001-... （手工造一个文件）
    # 调用 write_task，应该拿到 002 而不是 001
```

测试名字要明确包含 `seq_skips_archived` 这样语义，方便后人达到同样问题时 grep 能找到。

## 验收标准

- 三份新测试绿
- 现有 587 passed 不退
- ruff clean
- D:\FCoP 本仓被抢救过的两件手工 rename 文件在运行中不被误伤（他们在 `tasks/` 与 `reports/`、本身序号 002、与 log/ 中的 001 不冲）

## 不做

- 不引入 `.archived/<id>.tombstone` 隐藏占位文件（ISSUE-003 候选 B，被明确否决）
- 不改 `next_sequence()` 本身的语义——它是纯函数，决定扫哪是调用者职责

## 关联

- ISSUE：`docs/agents/issues/ISSUE-20260427-003-ME.md`
- 上游任务：`docs/agents/tasks/TASK-20260427-002-ADMIN-to-ME.md`（Rule 1 硬化 — 同仅进在 0.7.0）
- 被抢救的他现场：`TASK-20260427-002`、`REPORT-20260427-002`（手工 rename）
