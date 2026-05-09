# ADR-0019: Failure & Recovery Semantics

- **Status**: Proposed
- **Date**: 2026-05-09
- **Deciders**: ADMIN（待批准）
- **Related**: [ADR-0015](./ADR-0015-fcop-1.0-ai-os-protocol-charter.md) §抽象 5 Failure；[ADR-0016](./ADR-0016-json-schema-for-7-abstractions.md) `failure.schema.json`；[ADR-0018](./ADR-0018-event-model.md)（Failure 通过事件流暴露）

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

- [ ] `tests/test_fcop/test_failure.py` 新文件：4 类 Failure × 各自典型 evidence
- [ ] `tests/test_fcop/test_recovery.py` 新文件：5 类 Recovery × 闭环测试
- [ ] `tests/test_fcop/test_recovery.py` 加 Session resume / rollback / abort
- [ ] `tests/test_schemas/test_failure_schema.py`
- [ ] `tests/test_fcop/test_events.py` 加 FAILURE_DETECTED / RECOVERY_* 事件
- [ ] `tests/test_fcop/test_public_surface.py` 快照增加 report_failure / recover_session

## Backwards Compatibility

- 0.7.x throw exception 行为不变；report_failure 是新 API、opt-in
- recover_session 是新 API → ADR-0003 公开面只进不出锁
- failure / recovery enum 进 v1.x 仅允许加值（additive）

## Open Questions

1. `DRIFT` 怎么自动检测？v1.0 reference impl 仅提供 hook，**不**自动检测；由 reviewer / patrol 上报
2. Session schema 完整字段集 v1.0 不冻 → 但 `recover_session` 已经签 API。**冲突**：v1.0 锁了 API 签名但内部实现不完整 → API 用 free-form `metadata` 兜底，v1.x 完善
3. `RETRY` 是否需要计数防 infinite retry？v1.0 不在协议层 enforce；host adapter 自行决定
4. `ESCALATE` 升级目标如何指定？v1.0 默认升级到 `leader`（来自 fcop.json）；v1.x 加显式 escalation chain

## Sign-off

待 ADR-0015 charter 通过后，本 ADR 由 ADMIN 直接 sign 进入 Accepted。
