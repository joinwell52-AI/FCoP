---
protocol: fcop
version: 1
type: TASK
sender: ADMIN
recipient: ME
date: 2026-05-09
priority: P0
status: in_progress
subject: Failure & Recovery 抽象端到端：4 类失败 + 5 类恢复 + Session 恢复 hook
ref_charter: adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md
ref_adr: adr/ADR-0019-failure-and-recovery-semantics.md
ref_predecessor: docs/agents/log/tasks/TASK-20260509-005-ADMIN-to-ME.md
acceptance_criteria_count: 12
---

# TASK-20260509-006-ADMIN-to-ME

> Solo 模式任务。v1.0 7 抽象 reference-impl wiring 第 **3/7**。
> 把 ADR-0019 写在纸上的 Failure & Recovery 语义接进 reference impl
> ——**没有失败语义，"runtime" 二字就是空话**。

---

## 1 · 为什么需要这个任务（why now）

外部架构反馈最尖锐的一刀（per ADR-0019 §context）：

> "真正 Runtime 永远不是成功流程，而是异常如何活下来。"

POSIX 类比：FCoP 之于 Failure = Unix 之于 errno + signal handler。
TASK-003 已把 schema 冻在 `failure.schema.json`：4 类 Failure
（TIMEOUT / CRASH / DEADLOCK / DRIFT）+ 5 类 Recovery
（RETRY / RESUME / ROLLBACK / ABORT / ESCALATE）+ session_recovery_call
合约。本任务把这些**从纸搬到代码**，并加 `Project.report_failure` /
`Project.recover_session` 两个公开 API。

---

## 2 · ADMIN 决议（针对本任务）

### 决议 1 · `Failure` / `Recovery` 是内存 record，不是文件 envelope

ADR-0019 §design-details 提到 "`failure.schema.json` 定义 envelope"
——但实际 schema 里 `Failure` / `Recovery` / `SessionRecoveryCall` 是
**discriminated union 的 oneOf record**（看 `failure.schema.json` 顶层
`"oneOf": [...]`），不是 IPC envelope。它们没有 `protocol` / `sender`
等 envelope 必填字段，没有文件名 grammar，没有 reviews_dir 这样的
落盘目录。

→ v1.0 把它们实现为**纯内存 dataclass**。`Project.report_failure(failure)`
不写盘，只触发事件钩子（v1.0 stub）+ 返回 receipt 给 caller。
持久化（如果 caller 要）走 caller 自己的日志系统。这与 ADR-0019
§decision §「Session 恢复 hook（最小 surface）」的极简定位一致。

### 决议 2 · 事件触发是 stub（事件系统在 TASK-007）

ADR-0019 §design-details 第 4 条 "→ 触发 FAILURE_DETECTED 事件"。
但事件分发系统是 TASK-007 的工作。本任务实现：

- `Project.report_failure(failure)` 内部调
  `self._emit_event_stub("FAILURE_DETECTED", subject=failure)`
- `_emit_event_stub` 是私有 no-op（仅记录调用），TASK-007 把
  no-op 替换为真实的 watcher pub-sub
- 验证手段：`tests/test_fcop/test_failure.py` 用 `monkeypatch.setattr`
  把 stub 换掉，断言被调

### 决议 3 · `core/recovery.py` 模块的 Recovery 实现策略

5 类 Recovery 在 v1.0 reference impl 的实际行为：

| Recovery | v1.0 实现 | 副作用 |
|---|---|---|
| `RETRY` | 返回结构化 `RetryPlan`（task_path + suggested_delay + attempt_count） | 不写盘；caller 自行重试 |
| `RESUME` | 返回 `ResumePayload`（task + last_report + frontmatter metadata） | 只读 |
| `ROLLBACK` | 返回 `RollbackPlan`（target_commit_hash + affected_files），**不**实际 `git revert` | 只读；caller 决定是否执行 |
| `ABORT` | 真正写一个 REPORT `status: aborted`（已是 0.7.x 已支持的 status） | 写盘；调 `Project.write_report` |
| `ESCALATE` | 真正写一个 ISSUE 给 leader 角色 | 写盘；调 `Project.write_issue` |

「不实际跑 git revert」是关键收窄：v1.0 不引入 git 操作依赖，
ROLLBACK 给 caller 一个**计划**（plan），让 host adapter / human
决定是否执行。这与 ADR-0019 §session-recovery-hook §「v1.0 仅占位」
约束一致。

### 决议 4 · `recover_session` 仅暴露 3 个 action

per ADR-0019 §session-recovery-hook 与 `failure.schema.json#/$defs/sessionRecoveryAction` enum：
`recover_session(session_id, action)` 的 action 只接受
`"resume"` / `"rollback"` / `"abort"`。RETRY / ESCALATE 不是 session
级动作（前者是 task 级，后者跨 session），它们走 `report_failure` 的
`suggested_recovery` 字段；caller 调 `apply_recovery(failure)` 一站式
执行。

这意味着 v1.0 公开面：
- `Project.report_failure(failure: Failure) -> Receipt`
- `Project.recover_session(session_id: str, action: Literal["resume","rollback","abort"]) -> SessionRecoveryResult`
- `Project.apply_recovery(failure: Failure, action: RecoveryAction | None = None) -> RecoveryOutcome`
  —— action 为 None 时取 failure.suggested_recovery

### 决议 5 · `session_id` 形状与 0.7.x 历史 `session_id` 字段对齐

ADR-0019 §session-recovery-hook 写 "v1.0 仅占位：`session_id` 是
`<task_id>:<agent_code>` 字符串"。但 0.7.x 历史 REPORT / TASK
frontmatter 已含 `session_id: sess-20260427-me-072` 风格字符串
（见 `docs/agents/log/reports/REPORT-20260427-005-ME-to-ADMIN.md`）。

修订：v1.0 接受**两种形状**——
- `<task_id>:<agent_code>`（per ADR）
- `sess-YYYYMMDD-<agent>-NNN`（per 0.7.x 现状）

`recover_session` 解析时按 `:` 切尝试 task-id 形状；不匹配则按 0.7.x
形状解析（用 `_role_labels` / 文件扫描查 task）。这是 backward compat
所必需。

### 决议 6 · 不实现的（独立后续 TASK）

- 4 个新事件（FAILURE_DETECTED / RECOVERY_INITIATED / RECOVERY_COMPLETED
  / SESSION_LOST）的真实推送 → **TASK-007**（Event 抽象）
- `git revert` 真正执行 → **TASK-006-Phase-2**（v1.1 视用户反馈）
- DRIFT 自动检测 → 永远不做（per ADR-0019 §open-question 1）
- LLM context / tool history 完整 Session schema → **v1.x**
- RETRY 计数防无限重试 → host adapter 责任（per ADR §open-question 3）
- `MIGRATION-1.0.md` 失败处理迁移段 → **TASK-008**（migrate-workspace
  CLI 一并）

---

## 3 · 验收标准（12 条）

| # | 标准 | 证据 |
|---|---|---|
| A1 | `core/recovery.py` 模块存在；export 5 类 Recovery 的 reference impl 函数 | `from fcop.core.recovery import ...` |
| A2 | `models.Failure` / `models.Recovery` / `models.RetryPlan` / `models.ResumePayload` / `models.RollbackPlan` / `models.RecoveryOutcome` / `models.SessionRecoveryResult` 公开 dataclass | import smoketest |
| A3 | `models.FailureType` enum（TIMEOUT/CRASH/DEADLOCK/DRIFT）+ `RecoveryAction` enum（5 类）+ `SessionRecoveryAction` enum（3 类） | enum 长度断言 |
| A4 | `Project.report_failure(failure) -> Receipt` 工作；触发 stub 事件可被测试观察 | `test_project_report_failure` |
| A5 | `Project.apply_recovery(failure, action=None)` 5 类 Recovery 各 ≥ 1 用例（RETRY/RESUME/ROLLBACK 只读；ABORT 写 REPORT；ESCALATE 写 ISSUE） | `test_project_apply_recovery` |
| A6 | `Project.recover_session(session_id, action)` 接受两种 session_id 形状 + 3 类 action；非法 action raise | `test_project_recover_session` |
| A7 | `core/recovery.py` 5 个 reference impl 函数（pure，不依赖 Project）单测 | `test_core_recovery` ≥ 8 用例 |
| A8 | failure record 通过 `failure.schema.json` 的 `validate_record` 校验（schema 强制对齐） | `test_failure_record_schema_compat` |
| A9 | session_recovery_call 的 action enum 只允许 3 值（RETRY / ESCALATE 被拒；测试见证 v1.2 推迟值不偷塞） | `test_session_action_locked_to_three` |
| A10 | snapshot 更新含 +N 公开符号（约 7 dataclass + 3 enum + 3 方法 = 13 项 added） | `test_public_surface` 通过 |
| A11 | ADR-0019 状态从 Proposed → Accepted + Sign-off 段填实 + Tests Checklist 标 [x] | adr 文件 diff |
| A12 | REPORT-006 + 归档 + commit + push + CHANGELOG 加 Unreleased / Added 条目 | git log + CHANGELOG.md |

---

## 4 · 执行计划（4 commit）

| Round | 交付物 | Commit |
|---|---|---|
| R1 | `models.py` 加 7 dataclass + 3 enum；`core/recovery.py` 含 5 类 reference impl 函数（pure）；`tests/test_fcop/test_core_recovery.py`（≥ 12 用例） | `feat(core): failure & recovery dataclasses + 5 类 reference impl` |
| R2 | `Project.report_failure / apply_recovery / recover_session` 3 公开方法；`_emit_event_stub` 私有 hook；`tests/test_fcop/test_project_failure.py`（≥ 10 用例）；snapshot 更新；CHANGELOG | `feat(project): report_failure / recover_session 公开 API` |
| R3 | ADR-0019 状态 Proposed → Accepted（含 Sign-off + Tests Checklist 标 [x] + Open Questions 标解决）；adr/README.md 索引同步 | `adr(0019): accept failure & recovery ADR + 索引同步` |
| R4 | REPORT-006 + 归档 TASK-006 + push | `close TASK-20260509-006：failure & recovery 抽象已发车` |

---

## 5 · 风险登记

| 风险 | 缓解 |
|---|---|
| 公开面 +13 项，snapshot diff 大 | R2 一次更新；diff 全 added，符合 ADR-0003 |
| `apply_recovery(ABORT)` 写 REPORT 触发 0.7.x Rule 5（"只有 recipient 能 reply"）| ABORT 时 reporter = failure.subject.agent_code（即原 TASK 的 recipient），自然满足 Rule 5 |
| ROLLBACK 不实际跑 git → caller 误以为已执行 | RollbackPlan dataclass 显式标 `executed: False` 字段 + docstring 写明；测试断言此字段 |
| failure.schema.json 已 v1.0 frozen → 实现必须严格匹配 | A8 断言每个 Failure / Recovery instance 序列化后都过 schema |
| session_id 双形状解析复杂度高 | 仅 best-effort：task-id 形状解析失败直接返回 SessionRecoveryResult.error="session_not_found"，不抛异常 |

---

## 6 · 三视角预飞

### Proposer
v1.0 7 抽象进度跨过 3/7（Failure 是后两个里风险大头），完成后剩
Event（TASK-007）+ migrate-workspace（TASK-008）。**Failure 是
v1.0 RC ship 的最大未知风险**——它定义"runtime 怎么活下来"，没它
就只是文件协议不是 runtime。

### Executor
4 commit；R1 全新模块 + 测试；R2 加 Project 3 个方法 + 测试；
R3 仅 ADR 元数据；R4 文档归档。

### Reviewer
拒收预设：
- ❌ ROLLBACK 实际跑 git → 拒（v1.0 仅返回 plan）
- ❌ failure 任何 enum 值偏离 schema → 拒
- ❌ `recover_session` 接受 RETRY / ESCALATE → 拒（per ADR §session-recovery-hook 仅 3 个）
- ❌ `Failure` / `Recovery` 写盘 → 拒（per 决议 1，纯内存）
- ❌ MIGRATION-1.0.md 段被本任务塞进来 → 拒（TASK-008 工作）

---

## 7 · 签收

```
Sender:    ADMIN
Recipient: ME (solo 模式)
Status:    in_progress
Opened:    2026-05-09
Charter:   ADR-0015 §execution roadmap step 2（reference-impl wiring 3/7）
ADR:       ADR-0019 Failure & Recovery Semantics（本任务接 R3 转 Accepted）
Touches:   src/fcop/core/recovery.py（新建）、models.py（additive 大块）、
           project.py（additive 3 方法 + stub）
```

立即开始 R1。
