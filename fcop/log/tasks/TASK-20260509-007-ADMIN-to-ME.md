---
protocol: fcop
version: 1
type: TASK
sender: ADMIN
recipient: ME
date: 2026-05-09
priority: P0
status: in_progress
subject: Event 抽象端到端：12 事件 + polling watcher + subscribe_events
ref_charter: adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md
ref_adr: adr/ADR-0018-event-model.md
ref_predecessor: docs/agents/log/tasks/TASK-20260509-006-ADMIN-to-ME.md
acceptance_criteria_count: 12
---

# TASK-20260509-007-ADMIN-to-ME

> Solo 模式任务。v1.0 7 抽象 reference-impl wiring 第 **4/7**——
> **闭合最后一环**。Event 完成后 v1.0.0 即可进 RC 候选状态。

---

## 1 · 为什么需要这个任务（why now）

外部架构反馈精准命中：

> "Runtime 真正核心不是对象，而是事件。FCoP 现在更像静态文档系统，
> 而不是 Runtime Protocol。"
> "5 类 Schema 是静态结构 vs Event-driven State Protocol。"

POSIX 类比：FCoP 之于 Event = Unix 之于 signal。没有 signal，进程
无法响应外部状态变化。

TASK-005（boundary）和 TASK-006（failure）都遗留了 stub 事件钩子
（`_emit_event_stub`、boundary violation 不触发事件）。本任务把这些
钩子接到真实 watcher，闭合 v1.0 7 抽象的最后一环。

**完成本任务后**：

- `Project.subscribe_events(types, callback)` 公开 API 可用
- TASK-006 的 `Project._emit_event_stub` 替换成真实 emitter
- TASK-005 的 `BoundaryViolation` 自动 emit `BOUNDARY_VIOLATED` 事件
- 12 个事件类型全部有 trigger 实现 + 测试守门
- v1.0.0 RC 候选条件 100% 达成

---

## 2 · ADMIN 决议（针对本任务）

### 决议 1 · 走 ADR-0018 §decision 的"派生"路径，不新增 EVENT-*.md

事件由 file system 状态变化 / git diff 派生，**不**新增第 5 类
envelope 文件类型。理由：

- FCoP 核心原创性是"文件即 IPC"——事件已隐含在文件创建 / 移动 /
  状态字段变化里
- 新加 EVENT-*.md 会让协议从"4 类 envelope"变"5 类"，膨胀
- v1.x 后续如发现派生不够再加（superset，向后兼容）

### 决议 2 · v1.0 锁定 **12 个**事件类型（不是 ADR-0018 §minimal 列的 8 个）

`event.schema.json` 已经 v1.0 frozen 12 个 event_type enum 值：

**ADR-0018 §minimal-event-set 8 个**：

1. `TASK_CREATED` —— 新 TASK-*.md 文件落盘
2. `TASK_ACCEPTED` —— TASK frontmatter `status: accepted` 或 recipient 写第一份 REPORT
3. `TASK_BLOCKED` —— REPORT `status: blocked`
4. `TASK_COMPLETED` —— REPORT `status: done` + TASK 移到 log/tasks/
5. `REPORT_FILED` —— 新 REPORT-*.md 文件落盘
6. `REVIEW_DECIDED` —— 新 REVIEW-*.md 文件落盘 with decision
7. `BOUNDARY_VIOLATED` —— boundary check fail（TASK-005 接入）
8. `ROLE_SWITCHED` —— `fcop.json` 的 `roles` / `leader` 改动

**ADR-0019 §design-details 4 个 Failure 事件**：

9. `FAILURE_DETECTED` —— `Project.report_failure` 调用（TASK-006 stub 接入）
10. `RECOVERY_INITIATED` —— `Project.apply_recovery` 调用前
11. `RECOVERY_COMPLETED` —— `Project.apply_recovery` 调用成功后
12. `SESSION_LOST` —— `Project.recover_session(action=resume)` 找不到 session

### 决议 3 · v1.0 reference impl 用 polling + state diff

ADR-0018 §open-question 1 已建议。理由：

- 跨 OS 稳定性：filesystem watcher（inotify/FSEvents/ReadDirectoryChangesW）
  各平台行为差异大；polling 简单可控
- 确定性高：state diff 显式 == 易测试
- v1.0 不追求实时性（< 1s latency 是 host adapter 的事）

实现策略：

- `core/events.py` 提供 `compute_diff(prev_state: WatcherState,
  curr_state: WatcherState) -> list[Event]` 纯函数
- `Project.subscribe_events(types, callback)` 内部维护 `WatcherState`
  缓存；每次调 `poll_once()` 比较前后状态生成事件
- v1.0 **不**自动后台轮询；caller 必须显式调 `poll_once()`（或者
  host adapter 实现自己的 loop）。这避免 reference impl 引入线程 /
  asyncio 复杂性

### 决议 4 · v1.0 不持久化事件流

ADR-0018 §design-details 已锁定。事件仅在订阅瞬间发出；caller 自己
决定是否记录到自己的日志。理由：

- 持久化要求事件 schema 完全稳定（v1.x 加 enum 值会破坏老 log）
- 持久化引入 storage / rotation / GC 复杂性
- v1.x 如需 event log，新增 `Project.tail_events()` API +
  `docs/agents/log/events/` 文件类型（superset，向后兼容）

### 决议 5 · 同步触发 vs 文件 polling 双路径

两种事件触发机制：

- **A. 文件 polling 派生**（11 个文件类事件）：
  - `TASK_CREATED` / `TASK_ACCEPTED` / `TASK_BLOCKED` /
    `TASK_COMPLETED` / `REPORT_FILED` / `REVIEW_DECIDED` /
    `ROLE_SWITCHED` 8 个
  - 触发器：caller 调 `Project.poll_once()` 时 state diff 派生
- **B. 同步 callback 触发**（5 个 in-process 事件）：
  - `BOUNDARY_VIOLATED`（TASK-005 violation 时）
  - `FAILURE_DETECTED`（TASK-006 report_failure）
  - `RECOVERY_INITIATED` / `RECOVERY_COMPLETED`（TASK-006 apply_recovery）
  - `SESSION_LOST`（recover_session 找不到 session 时）
  - 触发器：Project 内部代码直接调 `_emit_event(event)`

`subscribe_events(types, callback)` 对两类来源是统一的——caller
拿到的 Event 对象一致。

### 决议 6 · 事件去重：基于 (event_type, subject_hash) 单调 cache

polling watcher 必然会发现"已有文件"——必须区分"新建"和"已存在"。
方案：

- `WatcherState.seen_paths: dict[Path, mtime]` 记录已知文件
- `compute_diff` 仅对新增 / mtime 增加的路径生成 `_CREATED` / `_FILED`
  类事件
- `_BLOCKED` / `_COMPLETED` / `_ACCEPTED` 看 frontmatter status
  字段变化（前后比对）
- `_DECIDED` 只触发一次（review 文件首次出现时）

去重 key = `(event_type, subject_hash)`；同一 poll 周期内重复抑制。
跨 poll 周期不抑制（避免内存泄漏；正常情况下文件状态稳定后不会
再触发）。

### 决议 7 · 不实现的（独立后续 TASK）

- `Project.tail_events()` / event log 持久化 → **v1.x**
- 后台自动 polling loop（线程 / asyncio） → **host adapter 责任**
- filesystem watcher（inotify 等真实 OS API） → **host adapter 责任**
- 跨 agent ordering / Lamport clock → **永远不做**（per ADR-0018
  §open-question 2）
- MCP `subscribe_events` tool → **TASK-010**（mcp 层任务）
- `TASK_REASSIGNED` / `REVIEW_AMENDED` 等更细事件 → **v1.x 视使用情况**

---

## 3 · 验收标准（12 条）

| # | 标准 | 证据 |
|---|---|---|
| A1 | `core/events.py` 模块存在；export `Event` / `EventType` / `WatcherState` / `compute_diff` / `make_event` | import smoketest |
| A2 | `models.Event` 公开 dataclass + `EventType` enum 含 12 值 | `len(EventType) == 12` |
| A3 | `Project.subscribe_events(types, callback)` 公开 API 可用 | `test_project_events::TestSubscribeEvents` |
| A4 | `Project.poll_once()` 公开方法；触发文件类 8 事件至少 6 类（CREATED/ACCEPTED/BLOCKED/COMPLETED/FILED/DECIDED） | `test_project_events::TestPollOnce` ≥ 6 用例 |
| A5 | `BOUNDARY_VIOLATED` 事件：`Project.write_review` 触发 boundary 违规时 emit | `TestBoundaryEventIntegration` |
| A6 | `FAILURE_DETECTED` / `RECOVERY_INITIATED` / `RECOVERY_COMPLETED` 接 TASK-006 路径（`_emit_event_stub` 替换） | `TestFailureRecoveryEvents` |
| A7 | `SESSION_LOST` 事件：`recover_session(resume)` 找不到时 emit | `TestSessionLostEvent` |
| A8 | `ROLE_SWITCHED` 事件：fcop.json roles / leader 改动 detect | `TestRoleSwitchEvent` |
| A9 | 事件去重：同一文件重复 poll 不重复触发 `_CREATED` / `_FILED` | `TestEventDedup` |
| A10 | event record 通过 `event.schema.json` 校验（包括 source / subject 子句） | `test_event_record_schema_compat` |
| A11 | snapshot 更新含 +N 公开符号（约 1 dataclass + 1 enum + 2 方法 = 4 + Event/EventType 字段） | `test_public_surface` 通过 |
| A12 | ADR-0018 → Accepted + Sign-off + Tests Checklist 标 [x] + Open Questions 标解决；REPORT-007 + 归档 + push + CHANGELOG | adr / git log / changelog diff |

---

## 4 · 执行计划（4 commit）

| Round | 交付物 | Commit |
|---|---|---|
| R1 | `models.Event` / `EventType`；`core/events.py` 含 `WatcherState` / `compute_diff` / `make_event`；`tests/test_fcop/test_core_events.py`（≥ 12 用例） | `feat(core): event model + polling watcher diff` |
| R2 | `Project.subscribe_events / poll_once / _emit_event` 公开/私有方法；接入 TASK-005/006 stub 替换；`tests/test_fcop/test_project_events.py`（≥ 12 用例）；snapshot 更新；CHANGELOG | `feat(project): subscribe_events + poll_once + 替换 stub 事件` |
| R3 | ADR-0018 状态 Proposed → Accepted（含 Sign-off + Tests Checklist 标 [x] + Open Questions 标解决）；adr/README.md 索引同步 | `adr(0018): accept event model ADR + 索引同步` |
| R4 | REPORT-007 + 归档 TASK-007 + push | `close TASK-20260509-007：event 抽象已发车（v1.0 7 抽象闭合）` |

---

## 5 · 风险登记

| 风险 | 缓解 |
|---|---|
| polling watcher 跨 OS mtime 精度差异（Windows FAT 是 2s）| 降级处理：mtime ± 1s 视为同一时刻；测试用 in-memory mock filesystem |
| _emit_event_stub 替换可能破坏 TASK-006 既有测试 | 保留 stub 入口；新 _emit_event 内部调 stub 入口；test_project_failure 不改 |
| 事件去重 cache 内存泄漏（长跑后 seen_paths 无限增长）| v1.0 不解决（host adapter 责任）；docstring 写明 + 测试覆盖典型用例 |
| BOUNDARY_VIOLATED 集成需要在 TASK-005 enforce 路径插桩 | 仅在 `Project.write_review` 抛 BoundaryViolationError 前 emit；不动 boundary.py 核心逻辑 |
| 12 事件类型测试用例量大 | A4 仅要求 ≥ 6 类，剩余在 v1.x 补；A6/A7/A8 各 1 类已覆盖 4 个 |

---

## 6 · 三视角预飞

### Proposer
v1.0 7 抽象进度跨过 4/7（**最后一环**），完成后 v1.0.0 RC 候选条件
全达成：

- 协议 schema 全 frozen ✅
- 7 抽象 reference-impl 全落地 ✅
- 全 ADR Accepted ✅
- 公开面 snapshot 全 additive 演化 ✅

只剩 migrate-workspace CLI（TASK-008）+ release 链（TASK-009..011）
非协议核心。**v1.0.0 进 RC 还差 1 步**。

### Executor
4 commit；R1 全新模块 + 测试；R2 加 Project 2-3 个方法 + 集成 stub
替换；R3 仅 ADR 元数据；R4 文档归档。

预期文件 ≤ 18，+/- 在 2200-3000 区间（参考 TASK-005/006 实测）。

### Reviewer
拒收预设：

- ❌ 新增 EVENT-*.md envelope → 拒（per 决议 1，永远不加）
- ❌ EventType enum 偏离 schema 12 值 → 拒
- ❌ 后台线程 / asyncio 自动轮询 → 拒（per 决议 3，caller 显式 poll）
- ❌ 事件流持久化 → 拒（per 决议 4，v1.x 工作）
- ❌ filesystem watcher（inotify 等）出现在 reference impl → 拒（per 决议 7）
- ❌ TASK-006 既有测试被破坏 → 拒（per 风险 2）
- ❌ MIGRATION-1.0.md 段被本任务塞进来 → 拒（TASK-008 工作）
- ❌ MCP subscribe_events tool → 拒（TASK-010 工作）

---

## 7 · 签收

```
Sender:    ADMIN
Recipient: ME (solo 模式)
Status:    in_progress
Opened:    2026-05-09
Charter:   ADR-0015 §execution roadmap step 2（reference-impl wiring 4/7
           —— 闭合最后一环）
ADR:       ADR-0018 Event Model（本任务接 R3 转 Accepted）
Touches:   src/fcop/core/events.py（新建）、models.py（additive）、
           project.py（additive 2-3 方法 + stub 替换）
```

立即开始 R1。
