# FCoP 3.0 Upgrade Guide: Ledger + Fixed Work Folders

## Purpose
Provide detailed instructions for Cursor to upgrade an existing FCoP project to 3.0 standards with fixed work folders and an agent-facing ledger.

## Scope
- Initialize stable directories: tasks/, reports/, issues/.
- Initialize ledger structure with tasks.jsonl, reports.jsonl, threads.jsonl, views/*.
- Ensure `_lifecycle/` remains runtime-owned projection.
- Agent reads only fixed folders and ledger; lifecycle movement is managed by LifecycleRail/LifecycleKernel.

## Upgrade Steps

### 1. Initialize directories
Ensure the following exist (create if missing):
```
fcop/tasks/
fcop/reports/
fcop/issues/
fcop/ledger/
fcop/ledger/tasks.jsonl
fcop/ledger/reports.jsonl
fcop/ledger/threads.jsonl
fcop/ledger/views/ADMIN.inbox.md
fcop/ledger/views/ADMIN.review.md
fcop/ledger/views/PM.todo.md
fcop/ledger/views/OPS.todo.md
fcop/ledger/views/DEV.todo.md
fcop/ledger/views/QA.todo.md
fcop/_lifecycle/inbox/
fcop/_lifecycle/active/
fcop/_lifecycle/review/
fcop/_lifecycle/done/
fcop/_lifecycle/archive/
```

### 2. Rebuild ledger
Run LedgerBuilder to scan existing tasks, reports, issues, and lifecycle buckets to populate ledger JSONL and views.

### 3. Update agent access
- Agents now read fixed directories and ledger views.
- Agents MUST NOT directly move files in `_lifecycle/`.
- Agents write TASK/REPORT/ISSUE facts only.

### 4. Lifecycle authority
- LifecycleKernel / LifecycleRail / MutationKernel manages `_lifecycle` buckets.
- syscalls: dispatch_task, submit_review, approve_review, reject_review, archive_task, supersede_report, invalidate_report.

### 5. ReportResolver
- Triggered after `write_report()`.
- Updates ledger and role views.
- Enforces PM settlement automatically.
- Prevents ReportGate from premature blocked reports.

### 6. PM settlement automation
- Detect child task REPORT done.
- Generate pending_pm_review in PM.todo.md.
- Update unique PM→ADMIN summary.
- Trigger submit_review for root task.

### 7. Test cases
1. Confirm initialization creates all required directories and files.
2. Rebuild ledger from existing TASK/REPORT/ISSUE files.
3. Verify list_tasks() matches ledger facts.
4. OPS reports to PM → PM summary auto-update → submit_review.
5. Ensure root task lifecycle advances correctly through review → done → archive.
6. ReportGate does not generate blocked when done report exists.

### 8. Safety and consistency
- init must be idempotent.
- ledger must be rebuildable anytime.
- Agent-facing views must reflect current facts.
- Lifecycle MV must be atomic and journaled.

## Outcome
After upgrade:
- Agents have a stable, predictable workspace.
- Lifecycle projection is centrally managed.
- PM no longer waits for ADMIN to trigger summary.
- ReportGate behavior is safe and delayed.
- list_tasks() and views reflect accurate project state.
- Initialization avoids missing directories for new projects.