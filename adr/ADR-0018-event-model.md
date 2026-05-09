# ADR-0018: Event Model

- **Status**: Proposed
- **Date**: 2026-05-09
- **Deciders**: ADMIN（待批准）
- **Related**: [ADR-0015](./ADR-0015-fcop-1.0-ai-os-protocol-charter.md) §抽象 4 Event；[ADR-0016](./ADR-0016-json-schema-for-7-abstractions.md) `event.schema.json`；[ADR-0019](./ADR-0019-failure-and-recovery-semantics.md)（Failure 事件子集）；[ADR-0020](./ADR-0020-agent-boundary-and-capability.md)（boundary 校验失败应触发事件）

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

- [ ] `tests/test_fcop/test_events.py` 新文件：8 事件 × 3 触发场景
- [ ] `tests/test_fcop/test_events.py` 加 subscribe + filter by type
- [ ] `tests/test_schemas/test_event_schema.py`
- [ ] `tests/test_fcop/test_events.py` 加事件去重测试（同一 file change 不应触发两次）
- [ ] `tests/test_fcop/test_public_surface.py` 快照增加 subscribe_events
- [ ] `tests/test_fcop_mcp/test_tool_surface.py` 视情况加 MCP `subscribe_events` tool

## Backwards Compatibility

- 无 frontmatter / filename 改动 → 0.7.x 文件 100% 兼容
- subscribe_events 是新公开 API → 加入 ADR-0003 公开面只进不出锁
- 事件 schema 进 v1.x 仅允许加新 enum 值（additive）

## Open Questions

1. 事件触发时机：文件落盘瞬间？git commit 时？filesystem watcher debounce？**建议**：v1.0 reference impl 用 polling + state diff（确定性高、跨 OS 稳定）；host adapter 可优化
2. 事件 ordering：跨 agent 的 happens-before 关系如何保证？**建议**：v1.0 仅保证单一 agent 内的 monotonic timestamp；分布式 ordering 不做（需要 Lamport / vector clock，超 v1.0 范围）
3. 是否需要 `TASK_REASSIGNED` / `REVIEW_AMENDED` 等更细的事件？**建议** v1.0 不加；v1.x 视使用情况
4. host adapter 怎么暴露 subscribe（MCP tool / WebSocket / file watcher API）？**建议**：v1.0 仅在协议层定义 callback contract，host 自由实现

## Sign-off

待 ADR-0015 charter 通过后，本 ADR 由 ADMIN 直接 sign 进入 Accepted。
