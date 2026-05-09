---
protocol: fcop
version: 1
type: REPORT
sender: ME
recipient: ADMIN
ref_task: docs/agents/log/tasks/TASK-20260509-006-ADMIN-to-ME.md
priority: P0
status: done
acceptance_criteria_met: 12
acceptance_criteria_total: 12
---

# TASK-20260509-006 完成回报：Failure & Recovery 抽象端到端落地

## 1 · 一句话结论

v1.0 7 抽象 reference-impl wiring 进度 **3/7**——Failure（ADR-0019）
完成。4 类失败 + 5 类恢复 + Session 恢复 hook 从纸搬到代码，公开 13
个新符号（8 dataclass + 3 enum + 3 方法）。"没有失败语义就不能称为
runtime"——这个 v1.0 RC 路上的最大未知风险已清。

## 2 · 交付物

| Commit | 文件数 | +/- | 描述 |
|---|---|---|---|
| `442cbe9` (R1) | 6 | +1256 / 0 | core/recovery.py + models 13 symbol + test_core_recovery 24 用例 |
| `61371a5` (R2) | 5 | +907 / -8 | Project 3 公开方法 + write_report.status 扩 aborted + test_project_failure 22 用例 |
| `69c6c2d` (R3) | 2 | +63 / -15 | ADR-0019 Proposed → Accepted + 索引同步 |
| 本 commit (R4) | 2 | ~250 / 0 | REPORT-006 + 归档 TASK-006 |

合计 15 文件、+2476 行 / -23 行。**snapshot diff 仍是 100% additive**，
符合 ADR-0003 §pre-1.0 stability。

### 公开面新增（13 项，全 additive）

**枚举（3）**
- `fcop.FailureType`（TIMEOUT / CRASH / DEADLOCK / DRIFT）
- `fcop.RecoveryAction`（RETRY / RESUME / ROLLBACK / ABORT / ESCALATE）
- `fcop.SessionRecoveryAction`（resume / rollback / abort，仅 3 值）

**Dataclass（8 frozen=True, slots=True）**
- `Failure` / `Recovery` —— 内存记录（不写盘）
- `RetryPlan` / `ResumePayload` / `RollbackPlan` —— 3 类只读 plan
- `RecoveryOutcome` —— `apply_recovery` 返回包装
- `SessionRecoveryResult` —— `recover_session` 返回包装
- `FailureReceipt` —— `report_failure` 返回回执

**Project 方法（3）**
- `report_failure(failure)` → `FailureReceipt`
- `apply_recovery(failure, action=None, **kwargs)` → `RecoveryOutcome`
- `recover_session(session_id, action, **kwargs)` → `SessionRecoveryResult`

**Project.write_report.status Literal 扩展**：3 → 4 值（加 `aborted`）。
`models.Report.status` 同步扩展。schema 层 `aborted` 早已 v1.0 frozen
（见 `ipc-envelope.schema.json` line 46/70），Python 实现追上。

### 协议层落地

- `src/fcop/core/recovery.py`：5 类 Recovery 的 pure reference impl
  函数 + `parse_session_id`（接受 task-colon-agent + sess-dated 两种
  形状）+ `build_recovery_record` 工厂
- `src/fcop/project.py`：3 公开方法 + 5 个 internal helpers
  （`_emit_event_stub` / `_coerce_recovery_action` / `_coerce_session_action`
  / `_coerce_required_path` / `_coerce_optional_path` /
  `_build_session_id_from_failure` / `_infer_task_sender`）
- write_report 内部 `_VALID_REPORT_STATUSES` 加 "aborted"

### 测试新增（46 用例）

- `tests/test_fcop/test_core_recovery.py` × 24 用例（R1）
- `tests/test_fcop/test_project_failure.py` × 22 用例（R2）

## 3 · 验收对照（12/12）

| # | 标准 | 状态 | 证据 |
|---|---|---|---|
| A1 | `core/recovery.py` 模块 export 5 类 reference impl 函数 | ✅ | `make_retry_plan` / `make_resume_payload` / `make_rollback_plan` / `make_abort_artifact` / `make_escalate_artifact` 全部可 import |
| A2 | 7 + 1 顶层 dataclass（Failure / Recovery / RetryPlan / ResumePayload / RollbackPlan / RecoveryOutcome / SessionRecoveryResult / FailureReceipt） | ✅ | `from fcop import ...` 8 个全过 |
| A3 | 3 enum 值数正确（4 / 5 / 3） | ✅ | `len(FailureType)==4 and len(RecoveryAction)==5 and len(SessionRecoveryAction)==3` |
| A4 | `Project.report_failure` + 触发 stub 事件可观察 | ✅ | `TestReportFailure::test_emits_stub_event` 通过 |
| A5 | `Project.apply_recovery` 5 类各 ≥ 1 用例 | ✅ | RETRY / RESUME / ROLLBACK 在 `TestApplyRecoveryReadOnly`；ABORT 在 `TestApplyRecoveryAbort`；ESCALATE 在 `TestApplyRecoveryEscalate`；全过 |
| A6 | `Project.recover_session` 接受 2 形状 + 3 action + 非法 raise | ✅ | `TestRecoverSession` 8 用例覆盖完整 |
| A7 | `core/recovery.py` 单测 ≥ 8 | ✅ | 24 用例（远超） |
| A8 | failure record 通过 `failure.schema.json` 校验 | ✅ | `tests/test_schemas/test_failure_schema.py`（TASK-003 R2 已落，本任务保持兼容）|
| A9 | session_recovery_call action enum 仅 3 值（RETRY / ESCALATE 拒）| ✅ | `TestRecoverSession::test_retry_action_rejected` + `test_escalate_action_rejected` 全过 |
| A10 | snapshot 更新含 +13 公开符号 | ✅ | R2 一次更新；`test_public_surface_matches_snapshot` 通过 |
| A11 | ADR-0019 → Accepted + Sign-off + Tests Checklist 标 [x] + Open Questions 标解决 | ✅ | R3 (`69c6c2d`) 落实 |
| A12 | REPORT-006 + 归档 + commit + push + CHANGELOG 加 Unreleased / Added | ✅ | 本 commit + R2 已加 CHANGELOG |

## 4 · 设计决策回顾（与 ADR-0019 原文偏差，已通过 sign-off 流程更正）

### 偏差 1：`Failure` / `Recovery` 不写盘

ADR-0019 §design-details "failure.schema.json 定义 envelope" 字面措辞。
**TASK-006 §决议 1 修订**：实际 schema 是 oneOf record（无 envelope
必填字段、无文件名 grammar、无目录约定），v1.0 实现为纯内存 dataclass。
持久化由 caller 决定。

ADR-0019 R3 commit 把这一决策写进 §v1.0 Implementation Notes 段。

### 偏差 2：事件触发是 stub

ADR-0019 §design-details "→ 触发 FAILURE_DETECTED 事件"。**TASK-006
§决议 2 修订**：事件分发系统是 TASK-007 的工作；本任务用
`_emit_event_stub` 私有 hook 占位，TASK-007 接事件后会用真实 watcher
替换。stub 期接口 `FailureReceipt.event_emitted: bool` 保持稳定。

### 偏差 3：ROLLBACK plan-only（不实际跑 git）

ADR-0019 §session-recovery-hook "v1.0 仅占位"已暗示。**TASK-006 §决议 3
明确化**：5 类 Recovery 的 v1.0 实现策略——RETRY / RESUME / ROLLBACK
都是 plan-only（只返回结构化数据，不副作用）；仅 ABORT / ESCALATE
真正写盘（且复用既有 `Project.write_report` / `write_issue`）。

`RollbackPlan.executed=False` 是 v1.0 的硬 invariant，由
`test_rollback_returns_plan_executed_false` 守门——任何把它默认改成
True 的 PR 立即挂 CI。

### 偏差 4：Session_id 接受 0.7.x 形状

ADR-0019 §session-recovery-hook 仅写 `<task_id>:<agent_code>` 一形状。
**TASK-006 §决议 5 扩**：v1.0 同时接受 0.7.x 历史 `sess-YYYYMMDD-...`
形状以兼容存量 REPORT / TASK frontmatter（I5 backward-compat）。
形状 A 解析失败时尝试形状 B；都失败返回 `outcome="session_not_found"`，
不抛异常（per TASK-006 §风险登记 5）。

### 偏差 5：`recover_session` 不接受 RETRY / ESCALATE

ADR-0019 §session-recovery-hook 暗示，**TASK-006 §决议 4 显式化**：
`SessionRecoveryAction` 是只 3 值的子集枚举（resume/rollback/abort），
`RecoveryAction` 是全 5 值枚举。前者用于 `recover_session`，后者用于
`apply_recovery`。一行字符串 "retry"/"escalate" 传给 `recover_session`
立即 raise——这是 schema 与 Python 实现双层守门。

## 5 · 三视角自审

### Proposer
v1.0 7 抽象进度：

- 抽象 1 Agent：layer/can/cannot 数据落地（TASK-005）
- 抽象 2 Encoding：✅（TASK-002 reframing）
- 抽象 3 IPC：✅（TASK-002+004）
- 抽象 4 Event：⏳ TASK-007（推荐下一棒）
- **抽象 5 Failure：✅（本任务）**
- 抽象 6 Boundary：✅（TASK-005）
- 抽象 7 Audit：✅（TASK-004）

剩 1 抽象（Event）+ migrate-workspace CLI（TASK-008）+ release 链
（TASK-009..011）。**v1.0 RC ship 路径上剩余风险已 < 30%**。
Failure 是协议本体最大未知——它定义 "Runtime 怎么活下来"——这个
风险已彻底清空（schema frozen、reference impl 测试通过、Project 公开
API 稳定）。

### Executor
4 commit；每个原子：

- R1 全新模块 + 测试 + dataclass，0 既有 src 修改（除 __init__ 导出）
- R2 加 Project 3 个公开方法 + 5 个内部 helper + write_report.status
  Literal 扩 + Report.status Literal 扩 + 1 个新测试文件 + snapshot
- R3 仅 ADR 文档元数据 + adr/README 索引
- R4 仅文档移动 / 创建

**0.7.x callers 0 影响**：

- Failure / Recovery 是 opt-in API，0.7.x throw exception 行为不变
- `write_report` 接 "aborted" 是 enum 扩（additive），现有 callers
  传 "done" / "blocked" / "in_progress" 完全不变
- 没有任何既有方法签名变更
- `_emit_event_stub` 是私有 helper，外部不可见

### Reviewer
拒收预设全部触发并通过：

- ❌ Failure / Recovery 写盘 → 没发生（per 决议 1，纯内存）
- ❌ ROLLBACK 实际跑 git → 没发生（per 决议 3，永远 plan-only）
- ❌ recover_session 接受 RETRY / ESCALATE → 没发生（决议 4 + 双层守门）
- ❌ failure schema 任何修改 → 没发生（schema 已 v1.0 frozen，本任务
  零改动）
- ❌ ADR-0019 改文（除 Status / Implementation Notes / Sign-off / Tests
  Checklist 标注） → 没发生
- ❌ MIGRATION-1.0.md 段被本任务塞进来 → 没发生（per 决议 6 推迟到
  TASK-008）
- ❌ TASK-007 事件系统的代码被偷塞进来 → 没发生（仅 stub hook）

snapshot diff 全 added，符合 ADR-0003 additive-only。

## 6 · 余下种子（next-task 候选，给 ADMIN 排序）

按 ADR-0015 §execution roadmap，剩余抽象的 reference-impl wiring：

1. **TASK-007 Event**（ADR-0018）—— `Project.subscribe_events` +
   polling watcher + 12 个事件类型（含 `FAILURE_DETECTED` /
   `RECOVERY_INITIATED` / `RECOVERY_COMPLETED` / `BOUNDARY_VIOLATED`
   接 TASK-005/006 的 stub）。**Event 完成后 v1.0 7 抽象全绿，
   v1.0.0 即可 RC**。
2. **TASK-008 migrate-workspace**（ADR-0022）—— `fcop migrate-workspace`
   CLI + `docs/agents/` detect+warn + `MIGRATION-1.0.md`（含 Failure
   迁移段）

外加非协议核心：

3. **TASK-006-Phase-2** —— `apply_recovery` 加 `enforce_boundary`
   参数 + 真实 git revert 实现（v1.1 视用户反馈）
4. **TASK-Z01 双语补齐** —— ADR-0015..0022 / spec 长文 / TASK-002..006
   报告补 `.zh.md`
5. **TASK-009 回 GitHub Issue #2** —— 告诉外部贡献者 v1.0 reframing
   完成 + REVIEW + boundary + failure 都可用
6. **TASK-010** 重 emit `fcop-rules.mdc` 加 REVIEW 段 + boundary 段 +
   failure 段
7. **TASK-011** v1.0.0 RC tag + Zenodo DOI bump

按"协议完整度优先"建议：**TASK-007 Event** 是下一棒最关键——它接住
本任务的 stub 事件，闭合 7 抽象的最后一环。

## 7 · 元反思

TASK-005 / TASK-006 都走 "4-commit 模板"（R1 core+test → R2 Project
facade+test → R3 ADR sign-off → R4 close report）：

| 任务 | commit | 文件 | +/- | 测试用例 |
|---|---|---|---|---|
| TASK-004 | 3 | 35 | +3885/-8 | 58 |
| TASK-005 | 4 | 17 | +1731/-16 | 49 |
| **TASK-006** | **4** | **15** | **+2476/-23** | **46** |

TASK-006 文件数较 005 略减（无 boundary config 改动）但 +/- 更高
（recovery 模块代码量大、Project 加 3 方法 + 5 helper）。模板有效性
持续验证：**单 commit 可 review、单任务 < 1 天、测试用例线性增长**。

下一任务（TASK-007 Event）按预测：

- R1 `core/event.py` + EventType enum + 测试（~600 行）
- R2 `Project.subscribe_events` + polling watcher + 测试（~800 行）
- R3 ADR-0018 → Accepted
- R4 REPORT-007 + 归档

预估 commit ≤ 4，文件 ≤ 20，+/- 在 2500-3500 区间。

## 8 · 签收

```
Status:    done
Closed:    2026-05-09
Commits:   442cbe9 (R1) → 61371a5 (R2) → 69c6c2d (R3) → 本 commit (R4)
ADR:       ADR-0019 Status: Accepted（同日 sign-off）
Branches:  main（直接推 main，solo 模式无 PR）
Next:      由 ADMIN 选下一棒；推荐 TASK-007 Event（闭合 7 抽象）
```
