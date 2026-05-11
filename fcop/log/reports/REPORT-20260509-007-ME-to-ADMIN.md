---
protocol: fcop
version: 1
type: REPORT
sender: ME
recipient: ADMIN
ref_task: docs/agents/log/tasks/TASK-20260509-007-ADMIN-to-ME.md
priority: P0
status: done
acceptance_criteria_met: 12
acceptance_criteria_total: 12
---

# TASK-20260509-007 完成回报：Event 抽象端到端 — v1.0 7 抽象 100% 闭合

## 1 · 一句话结论

**v1.0 7 抽象 reference-impl wiring 100% 完成**——Event 闭合最后
一环。12 类事件 + polling watcher + subscribe_events 公开 API 全部
落地，并把 TASK-005/006 留下的 5 处 stub 钩子全部替换为真实事件
总线。**v1.0.0 RC 候选条件全达成**。

## 2 · 交付物

| Commit | 文件数 | +/- | 描述 |
|---|---|---|---|
| `3706d9b` (R1) | 6 | +1246 / 0 | core/events.py + Event/EventType 模型 + test_core_events 23 用例 |
| `2d12681` (R2) | 7 | +680 / -39 | Project subscribe_events/poll_once + 5 处 stub 替换 + test_project_events 20 用例 |
| `26d1f0b` (R3) | 2 | +71 / -15 | ADR-0018 Proposed → Accepted + 索引同步 |
| 本 commit (R4) | 2 | ~280 / 0 | REPORT-007 + 归档 TASK-007 |

合计 17 文件、+2277 行 / -54 行。**snapshot diff 仍 100% additive**。

### 公开面新增（5 项，全 additive）

**Dataclass / Enum（4）**

- `fcop.Event` —— 内存 record（不写盘，per ADR-0018 §design-details）
- `fcop.EventSource` —— 来源元数据
- `fcop.EventSourceKind`（4 值：file / git / derived / callback）
- `fcop.EventType`（12 值，与 `event.schema.json` 词表对齐）

**Subscription 句柄（1）**

- `fcop.EventSubscription` —— `subscribe_events` 返回；含 `unsubscribe()` 方法

**Project 方法 / property（3）**

- `Project.subscribe_events(types, callback)` → `EventSubscription`
- `Project.poll_once()` → `list[Event]`
- `Project.workspace_dir` property（v1.0 显式 accessor）

### 协议层落地

- `src/fcop/core/events.py`：polling watcher 的 4 个 pure reference impl
  函数（`scan_workspace` / `compute_diff` / `make_event` /
  `make_event_id`）+ 2 个 dataclass（`WatcherState` / `FileSnapshot`）
  + `WATCHER_ID` 常量
- `src/fcop/project.py`：`EventSubscription` dataclass（顶层）+
  Project 加 3 个公开 + 4 个内部 helpers + 5 处 stub 替换 + 1 处
  scan_workspace 修复（fcop.json 实际位于 docs/agents/）

### 5 处 stub 替换详细

| 站点 | 原 TASK | 接到的事件 |
|---|---|---|
| `Project.assert_boundary` raise 前 | TASK-005 | `BOUNDARY_VIOLATED` |
| `Project.report_failure` | TASK-006 | `FAILURE_DETECTED`（既有调用，无需改） |
| `Project.apply_recovery` 入口 | TASK-006 | `RECOVERY_INITIATED` |
| `Project.apply_recovery` 5 个 return 路径 | TASK-006 | `RECOVERY_COMPLETED` |
| `Project.recover_session` session_not_found | TASK-006 | `SESSION_LOST` |

### 测试新增（43 用例）

- `tests/test_fcop/test_core_events.py` × 23 用例（R1）
- `tests/test_fcop/test_project_events.py` × 20 用例（R2）

## 3 · 验收对照（12/12）

| # | 标准 | 状态 | 证据 |
|---|---|---|---|
| A1 | `core/events.py` 模块存在；export 5 个核心符号 | ✅ | `from fcop.core.events import scan_workspace, compute_diff, make_event, WatcherState, WATCHER_ID` 可用 |
| A2 | `EventType` enum 12 值 + 与 schema 对齐 | ✅ | `test_event_type_has_12_values` + `test_event_type_aligns_with_schema` 全过 |
| A3 | `Project.subscribe_events` 公开 API | ✅ | `TestSubscribeEvents` 8 用例全过 |
| A4 | `Project.poll_once` + 触发文件类 8 事件至少 6 类 | ✅ | TASK_CREATED / REPORT_FILED / TASK_COMPLETED / TASK_BLOCKED / REVIEW_DECIDED / ROLE_SWITCHED 共 6 类有 R1+R2 测试覆盖（TASK_ACCEPTED 已在 compute_diff 实现，缺测试用例可 v1.x 补） |
| A5 | `BOUNDARY_VIOLATED` 集成 | ✅ | `TestBoundaryEventIntegration::test_boundary_violation_emits_event` 通过 |
| A6 | `FAILURE_DETECTED / RECOVERY_INITIATED / RECOVERY_COMPLETED` 接 TASK-006 | ✅ | `TestFailureRecoveryEvents` 3 用例全过；顺序断言 INITIATED < COMPLETED |
| A7 | `SESSION_LOST` 事件 | ✅ | `TestSessionLostEvent::test_invalid_session_id_emits_session_lost` 通过 |
| A8 | `ROLE_SWITCHED` 事件 | ✅ | `TestRoleSwitchEvent::test_fcop_json_change_emits_role_switched` 通过 |
| A9 | 事件去重 | ✅ | `test_dedup_task_created_across_polls`（R1）+ `test_poll_dedup_across_runs`（R2）双层守门 |
| A10 | event record 通过 schema 校验 | ✅ | `tests/test_schemas/test_event_schema.py`（TASK-003 R2 已落，本任务保持 enum 完全对齐） |
| A11 | snapshot 更新含 +5 公开符号 | ✅ | R2 一次更新；`test_public_surface_matches_snapshot` 通过 |
| A12 | ADR-0018 → Accepted + Sign-off + Tests Checklist 标 [x] + Open Questions 标解决；REPORT-007 + 归档 + push + CHANGELOG | ✅ | R3 (`26d1f0b`) + 本 commit |

## 4 · 设计决策回顾（与 ADR-0018 原文偏差，已通过 sign-off 流程更正）

### 偏差 1：v1.0 锁 12 个事件而不是 ADR §minimal 列的 8 个

ADR-0018 §decision §最小事件集只列 8 个。**TASK-007 §决议 2 修订**：
`event.schema.json` 已 v1.0 frozen 12 个 enum（8 from ADR-0018 +
4 from ADR-0019 §design-details Failure 子集）。Reference impl 必须
对齐 schema —— 这不是协议本体扩张，是把 ADR-0019 的事件签名 cherry-pick
到事件总线词表。

`test_event_type_aligns_with_schema` 在 CI 守门词表对齐。

### 偏差 2：双触发路径（同步 callback + 文件 polling）

ADR-0018 §design-details 没明确分类。**TASK-007 §决议 5 显式化**：

- 文件 polling 派生 8 类（CREATED/ACCEPTED/BLOCKED/COMPLETED/FILED/
  DECIDED/ROLE_SWITCHED + 部分 BOUNDARY_VIOLATED）
- 同步 callback 触发 4-5 类（FAILURE_DETECTED / RECOVERY_INITIATED
  / RECOVERY_COMPLETED / SESSION_LOST + 同步 BOUNDARY_VIOLATED）

`subscribe_events` 对两种来源是统一的——caller 拿到的 Event 对象一致。

### 偏差 3：scan_workspace 找 fcop.json 的位置

R1 写代码时假设 fcop.json 在 project_root（如 `<proj>/fcop.json`），
R2 集成 Project 时发现实际是 `<proj>/docs/agents/fcop.json`（per
`Project.config_path`）。修复策略：**先查 workspace_dir / fcop.json
再回退 project_root / fcop.json**——既支持 v1.0 实际 layout 又向后
兼容假想老 layout。

### 偏差 4：`_emit_event_stub` 改为 bridge 而非删除

ADR-0018 §design-details "TASK-006 stub 替换"暗示直接删除。**TASK-007
R2 实现策略**：保留 `_emit_event_stub` + `_emit_event_stub_calls`
list 接口，**内部实现**改为先 append legacy log 再 dispatch 到真实
事件总线。这样 TASK-006 既有 22 测试**零修改**全部通过——零破坏
backward compat。

`_emit_event_stub_calls` 从 class attribute 改为 lazy property
（避免在没用过的实例上 None）；list shape 不变。

### 偏差 5：v1.0 不实现的（per 决议 7 推迟）

- 后台自动 polling loop（线程 / asyncio）→ host adapter 责任
- filesystem watcher（inotify 等）→ host adapter 责任
- 事件流持久化（`tail_events()` / `log/events/`）→ v1.x
- 跨 agent ordering / Lamport clock → 永远不做（per ADR §open-question 2）
- MCP `subscribe_events` tool → TASK-010

## 5 · 三视角自审

### Proposer
**v1.0 7 抽象 reference-impl wiring 进度 4/4 完成**：

| # | 抽象 | 状态 |
|---|---|---|
| 1 | Agent | ✅（layer/can/cannot via TASK-005） |
| 2 | Encoding | ✅（TASK-002 reframing） |
| 3 | IPC | ✅（TASK-002 + TASK-004） |
| 4 | **Event** | **✅（本任务）** |
| 5 | Failure | ✅（TASK-006） |
| 6 | Boundary | ✅（TASK-005） |
| 7 | Audit | ✅（TASK-004） |

**v1.0.0 RC 候选条件全达成**：

- 协议 schema 全 frozen ✅（TASK-003）
- 7 抽象 reference-impl 全落地 ✅（TASK-004/005/006/007）
- 全 ADR Accepted ✅（ADR-0015..0022 全部完成）
- 公开面 snapshot 全 additive 演化 ✅
- I5 backward compat：0.7.x 文件 100% 仍可读 ✅

剩 migrate-workspace CLI（TASK-008，可选）+ release 工具链
（TASK-009..011）非协议核心。**理论上现在就可以打 v1.0.0-rc.1
tag 了**。

### Executor
4 commit；每个原子：

- R1 全新模块 + 测试 + dataclass，0 既有 src 修改（除 __init__/models 导出）
- R2 加 Project 3 个公开 + 4 个内部 + EventSubscription dataclass +
  5 处 stub 替换 + 1 处 fcop.json 路径修复
- R3 仅 ADR 文档元数据 + adr/README 索引
- R4 仅文档移动 / 创建

**0.7.x callers 0 影响 + TASK-006 既有测试 0 修改**：

- 所有 v1.0 新 API 都是 additive
- `_emit_event_stub` bridge 设计完美保持向后兼容
- TASK-006 22 个测试 + TASK-005 49 个测试全部不变通过
- 871 总测试 0 回归

### Reviewer
拒收预设全部触发并通过：

- ❌ 新增 EVENT-*.md envelope 文件 → 没发生
- ❌ EventType 偏离 schema 12 值 → 没发生（CI 词表对齐守门）
- ❌ 后台线程 / asyncio 自动轮询 → 没发生（caller 显式 poll_once）
- ❌ 事件流持久化 → 没发生（v1.x 工作）
- ❌ filesystem watcher 出现在 reference impl → 没发生
- ❌ TASK-006 既有测试被破坏 → 没发生（bridge 设计保住）
- ❌ MIGRATION-1.0.md 段被本任务塞进来 → 没发生（TASK-008 工作）
- ❌ MCP subscribe_events tool → 没发生（TASK-010 工作）

snapshot diff 全 added，符合 ADR-0003 additive-only。

## 6 · 余下种子（next-task 候选）

**v1.0 协议本体 100% 完成**。剩余任务都是 release / 工具 / 文档：

1. **TASK-008 migrate-workspace CLI**（ADR-0022）—— `fcop migrate-workspace`
   + `docs/agents/` detect+warn + `MIGRATION-1.0.md`（含 Failure /
   Event 迁移段）。**v1.0.0 RC 之前推荐做**（用户友好）。
2. **TASK-Z01 双语补齐** —— ADR-0015..0022 / spec 长文 / TASK-002..007
   报告补 `.zh.md`。
3. **TASK-009 回 GitHub Issue #2** —— 告诉外部贡献者 v1.0 reframing
   完成 + 7 抽象全落地 + REVIEW + boundary + failure + event 都可用。
4. **TASK-010** 重 emit `fcop-rules.mdc` 加 REVIEW / boundary /
   failure / event 段；MCP `subscribe_events` tool。
5. **TASK-011** **v1.0.0-rc.1 tag** + Zenodo DOI bump（**可立即开始**）。

按"最小可发布产物"路径：**TASK-011 直接打 RC tag 是最快的发车方式**。
若优先用户友好，则先做 TASK-008 + TASK-010。

## 7 · 元反思

TASK-004/005/006/007 都走 "4-commit 模板"（R1 core+test → R2 Project
facade+test → R3 ADR sign-off → R4 close report）：

| 任务 | commit | 文件 | +/- | 测试用例 | 抽象进度 |
|---|---|---|---|---|---|
| TASK-004 | 3 | 35 | +3885/-8 | 58 | Audit (7/7) |
| TASK-005 | 4 | 17 | +1731/-16 | 49 | Boundary (6/7) |
| TASK-006 | 4 | 15 | +2476/-23 | 46 | Failure (5/7) |
| **TASK-007** | **4** | **17** | **+2277/-54** | **43** | **Event (4/7) — 闭环** |

模板有效性继续验证：**单 commit 可 review、单任务 < 1 天、测试用例
线性增长、文件数稳定在 15-17、+/- 在 1700-2500 区间**。

7 抽象 reference-impl wiring 总计：**14 commits、64 文件次、
+8369 行 / -101 行、196 测试用例**。

下一步无论选 TASK-008 / TASK-Z01 / TASK-011，都不再涉及协议本体
变更——**v1.0 协议表面已冻结**，进入"工程收尾 + release"阶段。

## 8 · 签收

```
Status:    done
Closed:    2026-05-09
Commits:   3706d9b (R1) → 2d12681 (R2) → 26d1f0b (R3) → 本 commit (R4)
ADR:       ADR-0018 Status: Accepted（同日 sign-off）
Branches:  main
Milestone: v1.0 7 抽象 reference-impl wiring 100% 完成
RC ready:  YES —— v1.0.0-rc.1 candidate
Next:      ADMIN 选下一棒；推荐 TASK-011（直接打 RC tag）或
           TASK-008（migrate-workspace CLI 用户友好）
```
