# ADR-0019: Failure & Recovery Semantics

- **Status**: Accepted
- **Date**: 2026-05-09
- **Accepted-on**: 2026-05-09
- **Deciders**: ADMIN（solo 模式 sign-off）
- **Implementation**:
  - Schema: `spec/schemas/failure.schema.json`（v1.0 frozen，TASK-003 R1）
  - Reference impl：`src/fcop/core/recovery.py`（commit `442cbe9`，TASK-006 R1）
  - Project facade：`Project.report_failure / apply_recovery / recover_session`（commit `61371a5`，TASK-006 R2）
- **Related**: [ADR-0015](./ADR-0015-fcop-1.0-ai-os-protocol-charter.md) §抽象 5 Failure；[ADR-0016](./ADR-0016-json-schema-for-7-abstractions.md) `failure.schema.json`；[ADR-0018](./ADR-0018-event-model.md)（Failure 通过事件流暴露）；[TASK-20260509-006](../docs/agents/log/tasks/TASK-20260509-006-ADMIN-to-ME.md)（implementation charter）

## Context

外部架构反馈最尖锐的一刀：

> "真正 Runtime 永远不是成功流程，而是异常如何活下来。"
> "你现在必须正式定义：Agent Timeout / Session Lost / Infinite Retry / Review Deadlock / Drift / Recovery —— 否则 Runtime 会非常脆。"

POSIX 类比：FCoP 之于 Failure = Unix 之于 errno + signal handler。没有失败语义，协议只能跑"理想情况"。

ADR-0007 路线 8 个 ADR + 整个 timeline 全是 happy path —— 这是协议本体最大缺失。

## Decision

v1.0 冻结 4 类**失败模式枚举** + 5 类**恢复动作枚举** + 最小 Session 恢复 hook。

### 失败模式（4 类）

| Failure | 含义 | 触发示例 |
|---|---|---|
| `TIMEOUT` | agent 在约定时间内未交付 | 超过 TASK frontmatter `timeout_at` |
| `CRASH` | reference impl / host adapter 异常退出 | Python OOM、MCP server SIGKILL |
| `DEADLOCK` | 多 agent 互相等待对方完成 | A 等 B 的 REVIEW；B 等 A 的 REPORT |
| `DRIFT` | agent 输出与 TASK 约定不符 | recipient 写了无关的代码 / 越界改文件 |

### 恢复动作（5 类）

| Recovery | 含义 | 谁触发 |
|---|---|---|
| `RETRY` | 同一 agent 重做同一 TASK | host adapter / leader |
| `RESUME` | 加载 session state，从中断点继续 | host adapter |
| `ROLLBACK` | 回到 TASK 创建前的文件状态 | leader / admin |
| `ABORT` | 终止 TASK，标 `status: aborted` | leader / admin |
| `ESCALATE` | 升级到上一层 governance 处理 | governance / admin |

每个 Failure 必须配对至少一个 Recovery；具体 mapping 由 host adapter 决定（FCoP 协议层不强制 enforce 哪个 Failure 走哪个 Recovery）。

### Session 恢复 hook（最小 surface）

`Project.recover_session(session_id, action: Literal["resume","rollback","abort"])` 公开 API：

- v1.0 仅占位：`session_id` 是 `<task_id>:<agent_code>` 字符串
- v1.0 实现：`resume` = 重读 TASK + 最后一份 REPORT；`rollback` = `git revert` 到 TASK 创建前；`abort` = 写 REPORT `status: aborted`
- 完整 Session schema（含 LLM context / tool history）推 v1.x

## Design Details

- `failure.schema.json` 定义 envelope：`failure_type` (enum)、`subject` (task_id / agent_code)、`detected_at`、`evidence` (free)、`suggested_recovery` (enum)
- `models.Failure` / `models.Recovery` dataclass
- `Project.report_failure(failure: Failure)` 公开 API → 触发 `FAILURE_DETECTED` 事件 + 可选自动 Recovery
- `Project.recover_session(...)` 公开 API
- `core/recovery.py` 新文件：实现 5 类 Recovery 的 reference impl
- 新事件（补 ADR-0018 §最小事件集）：`FAILURE_DETECTED`、`RECOVERY_INITIATED`、`RECOVERY_COMPLETED`、`SESSION_LOST`
- `MIGRATION-1.0.md` 必须有"如何把 0.7.x 的失败处理（throw exception）迁移到 v1.0 的 report_failure"段

## Tests Checklist

- [x] `tests/test_fcop/test_core_recovery.py` 新文件：4 类 Failure 与
  5 类 Recovery × 各自典型 evidence + plan invariants（24 用例，TASK-006 R1）
- [x] `tests/test_fcop/test_project_failure.py` 新文件：3 公开方法的端到
  端测试（22 用例，TASK-006 R2）。**注**：本 ADR 原计划拆 `test_failure.py`
  与 `test_recovery.py` 两份，TASK-006 R2 落地时合并为单文件
  `test_project_failure.py`——按 facade 层次而非主题切分，便于 reviewer
  一次读懂 API 接面。
- [x] `tests/test_schemas/test_failure_schema.py` —— TASK-003 R2 已落地
  （4 用例：合法 Failure / 缺必填 / 非法 enum / Recovery 子句）
- [ ] `tests/test_fcop/test_events.py` 加 FAILURE_DETECTED / RECOVERY_*
  事件 —— **推迟到 TASK-007**（Event 抽象）。本任务里 Failure 事件通过
  `Project._emit_event_stub` 触发 stub（per TASK-006 §决议 2），由
  `test_project_failure.py::TestReportFailure::test_emits_stub_event`
  守门 stub 调用语义。
- [x] `tests/test_fcop/test_public_surface.py` 快照增加 report_failure /
  apply_recovery / recover_session + 8 dataclass + 3 enum（TASK-006 R2
  已更新 snapshots/public_surface.json）

## Backwards Compatibility

- 0.7.x throw exception 行为不变；report_failure 是新 API、opt-in
- recover_session 是新 API → ADR-0003 公开面只进不出锁
- failure / recovery enum 进 v1.x 仅允许加值（additive）

## Open Questions

1. ~~`DRIFT` 怎么自动检测？~~ **Resolved**（TASK-006 §决议 6）：永远
   不在 reference impl 自动检测；本 ADR §design-details 已明确 hook
   语义。Reviewer / patrol agent 上报；caller 自己实现检测策略。
2. ~~Session schema 完整字段集 v1.0 不冻 vs `recover_session` 已签
   API。~~ **Resolved**（TASK-006 R2）：`Project.recover_session` 用
   两种 session_id 形状（`TASK-...:agent` + `sess-YYYYMMDD-...`）+
   `ResumePayload.metadata: dict[str, object]` 兜底；完整 Session
   schema 推 v1.x。
3. ~~`RETRY` 是否需要计数防 infinite retry？~~ **Resolved**（TASK-006
   R1）：v1.0 不在协议层 enforce；`RetryPlan.attempt_count` 是 caller
   自报的元数据，host adapter 自己决定 backoff / circuit-breaker。
4. ~~`ESCALATE` 升级目标如何指定？~~ **Resolved**（TASK-006 R2）：
   `Project.apply_recovery(action=ESCALATE, leader_recipient=...)`
   要求 caller 显式传角色 code；v1.0 不强制查 `fcop.json` 里的
   `leader`，让 caller 灵活指定（避免 single-leader 假设）。v1.x 可
   加便利方法 `escalate_to_leader()` 自动查。

## v1.0 Implementation Notes（per TASK-006）

落地时与原文有 3 处偏差，由 TASK-006 charter §决议 1/2/6 sign-off 授权：

1. **Failure / Recovery 不写盘**（决议 1）：原文 §design-details 说
   `failure.schema.json` 定义 envelope；实际 schema 是 discriminated
   union 的 oneOf record，本就不是 IPC envelope。v1.0 实现为纯内存
   dataclass，持久化由 caller 自决。
2. **事件触发是 stub**（决议 2）：本 ADR §design-details 第 4 条
   "→ 触发 FAILURE_DETECTED 事件"——v1.0 实现为
   `Project._emit_event_stub`（in-memory log），TASK-007（Event 抽象）
   接事件后会换成真实 watcher pub-sub。stub 期保持 receipt 接口稳定。
3. **MIGRATION-1.0.md 失败处理段不在本任务**（决议 6）：原文
   §design-details 第 6 条提到迁移段；推迟到 TASK-008（migrate-workspace
   CLI）一并写。

## Sign-off

| 角色 | 决议 | 日期 |
|---|---|---|
| ADMIN（solo 模式） | Accepted | 2026-05-09 |

实现承接：TASK-20260509-006（commits `442cbe9` R1 / `61371a5` R2 / R3 = 本 commit）。
