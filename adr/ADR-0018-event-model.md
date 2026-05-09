# ADR-0018: Event Model

- **Status**: Accepted
- **Date**: 2026-05-09
- **Accepted-on**: 2026-05-09
- **Deciders**: ADMIN（solo 模式 sign-off）
- **Implementation**:
  - Schema: `spec/schemas/event.schema.json`（v1.0 frozen 12 enum，TASK-003 R1）
  - Reference impl：`src/fcop/core/events.py`（commit `3706d9b`，TASK-007 R1）
  - Project facade：`Project.subscribe_events / poll_once / workspace_dir` + 5 处 stub 替换（commit `2d12681`，TASK-007 R2）
- **Related**: [ADR-0015](./ADR-0015-fcop-1.0-ai-os-protocol-charter.md) §抽象 4 Event；[ADR-0016](./ADR-0016-json-schema-for-7-abstractions.md) `event.schema.json`；[ADR-0019](./ADR-0019-failure-and-recovery-semantics.md)（Failure 事件子集）；[ADR-0020](./ADR-0020-agent-boundary-and-capability.md)（boundary 校验失败应触发事件）；[TASK-20260509-007](../docs/agents/log/tasks/TASK-20260509-007-ADMIN-to-ME.md)（implementation charter）

## Context

FCoP 0.7.x 与 ADR-0007 路线把"对象 + 字段"当协议本体——外部反馈精准命中：

> "Runtime 真正核心不是对象，而是事件。FCoP 现在更像静态文档系统，而不是 Runtime Protocol。"
> "5 类 Schema 是静态结构 vs Event-driven State Protocol。"

POSIX 类比：FCoP 之于 Event = Unix 之于 signal。没有 signal，进程无法响应外部状态变化。

事件 vs 文件的关系是设计核心问题：事件**派生**自文件状态变化（filesystem watcher / git diff / CRDT）？还是**另存**为 EVENT-*.md 文件类型？

## Decision

**v1.0 走"派生"路径**：事件由 file system / git diff 派生，**不**新增 EVENT-*.md 文件类型。

理由：
- FCoP 核心原创性是"文件即 IPC"——事件已经隐含在文件创建 / 移动 / 状态字段变化里
- 新加 EVENT-*.md 会让协议从"4 类 envelope"变"5 类"，膨胀
- v1.x 后续如发现派生不够再加（superset，向后兼容）

最小事件集（v1.0 锁定 8 个）：

| Event | Trigger | Subject |
|---|---|---|
| `TASK_CREATED` | 新 TASK-*.md 文件落盘 | task_id |
| `TASK_ACCEPTED` | TASK frontmatter `status: accepted` 或被 recipient 写第一份 REPORT | task_id |
| `TASK_BLOCKED` | REPORT `status: blocked` | task_id, reason |
| `TASK_COMPLETED` | REPORT `status: done` + TASK 移到 log/tasks/ | task_id |
| `REPORT_FILED` | 新 REPORT-*.md 文件落盘 | report_id, task_id |
| `REVIEW_DECIDED` | 新 REVIEW-*.md 文件落盘 with decision != null | review_id, subject_ref, decision |
| `BOUNDARY_VIOLATED` | boundary check fail（ADR-0020） | actor, target, attempted_action |
| `ROLE_SWITCHED` | `fcop.json` 的 `roles` / `leader` 改动 | from, to, reason |

`SESSION_LOST` / `AGENT_TIMEOUT` / `RECOVERY_*` 等失败相关事件由 [ADR-0019](./ADR-0019-failure-and-recovery-semantics.md) 收口。

## Design Details

- `event.schema.json` 定义 envelope：`event_type` (enum)、`event_id`、`occurred_at`、`subject` (object)、`source` (file path or git ref)、`metadata` (free)
- `models.Event` dataclass 与 schema 对照
- `Project.subscribe_events(types: list[str], callback: Callable)` 公开 API
- v1.0 reference impl：`fcop` 库内置 polling watcher（基于 `os.scandir` + state diff）
- host adapter 可替代 watcher 实现（mobile push / cloud webhook）—— 这是 host 层的事，协议只暴露 subscribe contract
- 不持久化事件流（v1.0 选择"无 event log"）；事件仅在订阅瞬间发出
- v1.x 如需 event log，新增 `Project.tail_events()` API + 可选 `docs/agents/log/events/` 文件类型

## Tests Checklist

- [x] `tests/test_fcop/test_core_events.py` 新文件：23 用例覆盖
  scan_workspace + compute_diff + 12 事件类型词表对齐 + 8 事件 × 多个
  触发场景（TASK-007 R1）
- [x] `tests/test_fcop/test_project_events.py` 新文件：20 用例覆盖
  subscribe + filter by type + unsubscribe + 4 in-process 事件集成
  + RoleSwitched + back-compat（TASK-007 R2）
- [x] `tests/test_schemas/test_event_schema.py` —— TASK-003 R2 已落地
  （4 用例：合法 Event / 缺必填 / 非法 enum / source 子句）
- [x] 事件去重：`test_dedup_task_created_across_polls`（R1）+
  `test_poll_dedup_across_runs`（R2）—— 同一 state 跨 poll 不重复
  触发，由 compute_diff 的 seen_ids set 守门
- [x] `tests/test_fcop/test_public_surface.py` 快照已更新含
  EventSubscription + subscribe_events / poll_once / workspace_dir
- [ ] `tests/test_fcop_mcp/test_tool_surface.py` MCP `subscribe_events`
  tool —— **推迟到 TASK-010**（mcp 层 emit + 重 deploy_rules 一并做）

## Backwards Compatibility

- 无 frontmatter / filename 改动 → 0.7.x 文件 100% 兼容
- subscribe_events 是新公开 API → 加入 ADR-0003 公开面只进不出锁
- 事件 schema 进 v1.x 仅允许加新 enum 值（additive）

## Open Questions

1. ~~事件触发时机：文件落盘瞬间？git commit 时？filesystem watcher
   debounce？~~ **Resolved**（TASK-007 §决议 3）：v1.0 reference impl
   走 polling + state diff（caller 显式调 `Project.poll_once`）；
   filesystem watcher（inotify/FSEvents/ReadDirectoryChangesW）是
   host adapter 的责任（per ADR §design-details + TASK-007 §决议 7）。
2. ~~事件 ordering：跨 agent 的 happens-before 关系如何保证？~~
   **Resolved**：v1.0 仅保证单一 agent 内的 monotonic timestamp；
   分布式 ordering 不做（需要 Lamport / vector clock，超 v1.0 范围）。
   `Event.occurred_at` 在 ADR §design-details 已写明此约束。
3. ~~是否需要 `TASK_REASSIGNED` / `REVIEW_AMENDED` 等更细的事件？~~
   **Resolved**（TASK-007 §决议 7）：v1.0 不加；v1.x 视使用情况。
   12 类已 frozen 在 `event.schema.json` enum；扩 enum 是 MINOR
   bump（additive），无破坏性。
4. ~~host adapter 怎么暴露 subscribe（MCP tool / WebSocket / file
   watcher API）？~~ **Resolved**（TASK-007 §决议 7）：v1.0 仅在协议
   层定义 callback contract（`Project.subscribe_events` 同步回调）；
   host 自由实现。MCP `subscribe_events` tool 推迟到 TASK-010。

## v1.0 Implementation Notes（per TASK-007）

落地时与原文有 2 处偏差，由 TASK-007 charter §决议 2/5 sign-off 授权：

1. **v1.0 锁 12 个事件而不是 ADR §minimal-event-set 列的 8 个**
   （决议 2）：`event.schema.json` v1.0 frozen 12 enum（8 from ADR-0018
   §minimal + 4 from ADR-0019 §design-details Failure 子集）。
   Reference impl 的 `EventType` enum 必须与 schema 词表完全对齐
   （`test_event_type_aligns_with_schema` CI 守门）。
2. **同步触发 vs 文件 polling 双路径**（决议 5）：
   - 文件 polling 派生 8 类（CREATED/ACCEPTED/BLOCKED/COMPLETED/
     FILED/DECIDED/ROLE_SWITCHED + 部分 BOUNDARY_VIOLATED）
   - 同步 callback 触发 4-5 类（FAILURE_DETECTED / RECOVERY_INITIATED
     / RECOVERY_COMPLETED / SESSION_LOST + 同步 BOUNDARY_VIOLATED）
   - `subscribe_events` 对两类来源统一。

`_emit_event_stub` 改为 bridge —— 同时维护 TASK-006 期望的
`_emit_event_stub_calls` legacy log + 派发到真实事件总线。这是
"零破坏既有测试"的实现技巧，不是协议层契约。

## Sign-off

| 角色 | 决议 | 日期 |
|---|---|---|
| ADMIN（solo 模式） | Accepted | 2026-05-09 |

实现承接：TASK-20260509-007（commits `3706d9b` R1 / `2d12681` R2 /
R3 = 本 commit）。

**v1.0 7 抽象 reference-impl wiring 100% 完成（4/7 由本 ADR
闭合最后一环）**。下一步 v1.0.0 RC：剩 migrate-workspace CLI
（TASK-008）+ release 工具链（TASK-009..011）。
