# ADR-0035: FCoP 3.0 State Ontology
## Composite Protocol Document · One File, Multiple Layers, Single Version Anchor

| 字段 | 值 |
|---|---|
| **Status** | **Accepted & Frozen** (2026-05-21 · semantics frozen per RFC 2026-05-21) |
| **Date** | 2026-05-19 |
| **Accepted-on** | 2026-05-21（由 ADMIN 签署通过，正式作为 FCoP 3.0 Canonical Spec） |
| **Frozen-on** | 2026-05-21（RFC 评审锁定：path-only truth，不再扩展任何语义） |
| **Depends on** | Rule 2（文件夹即组织）、ADR-0003（稳定性宪章）、ADR-0004（`os.rename()` 原子性） |
| **Type** | Protocol Breaking Change — State Ontology ONLY (MAJOR, targets fcop 3.0) |

---

## Core Insight

> **文件夹即状态。**

| 版本 | Rule 2 语义 |
|------|------------|
| FCoP 1.x | 文件夹即组织（类型分类：tasks / reports / issues） |
| FCoP 3.0 | 文件夹即组织 **+** 文件夹即状态（生命周期阶段） |

文件在哪里，它就处于哪个生命周期阶段。不需要读内容，不需要查字段，目录位置即真相。

这是 ADR-0035 在 Rule 2 基础上新增的语义层，也是它作为 Major 版本变更的唯一理由。

---

## ⚠ HARD BOUNDARY

> **ADR-0035 只有一个版本生成点：§1 State Ontology。其余全部是注释性扩展。**

| 章节 | 标签 | 版本权 |
|------|------|--------|
| **§1 STATE ONTOLOGY** | VERSION ANCHOR | ✔ 唯一。FCoP 3.0 = §1 |
| NON-VERSION: TOOL LAYER | implementation appendix | ✗ 可随实现演进 |
| NON-VERSION: MIGRATION | ephemeral | ✗ 执行后过时 |
| NON-VERSION: RUNTIME NOTES | informative only | ✗ 不参与协议定义 |
| NON-VERSION: EXCLUSION ZONE | reference only | ✗ 防滑坡边界 |

---

## 动机 / Motivation（context, not protocol）

FCoP 1.x 的 `tasks/` 目录里，一个任务从投递到完成物理位置始终不变——协议无法从目录层面区分"待领取"和"执行中"。这导致多 Agent 并发时无法幂等去重，产生重复派发。

---
---

# §1 · STATE ONTOLOGY
## ⬛ VERSION ANCHOR · THIS IS FCoP 3.0

### 目录结构

```
fcop/
├── _lifecycle/
│   ├── inbox/
│   ├── active/
│   ├── review/
│   ├── done/
│   └── archive/
├── reports/
├── issues/
└── shared/
```

### 各阶段定义

| 阶段 | 定义 |
|------|------|
| `inbox` | created |
| `active` | claimed |
| `review` | pending confirmation |
| `done` | completed |
| `archive` | closed |

### Allowed Transitions

| from | to | tool |
|------|----|------|
| — | `inbox` | `create_task` |
| `inbox` | `active` | `claim_task` |
| `active` | `review` | `submit_task` |
| `active` | `done` | `finish_task(skip_review=true)` |
| `review` | `done` | `approve_task` |
| `review` | `active` | `reject_task` |
| `done` | `archive` | `archive_task` |

### 协议收敛规则（§1 内的版本承诺）

> **Rule A · File path = state truth**  
> 目录位置是唯一状态真相。无需读文件内容判断任务状态。
>
> **Rule B · L1 tools perform filesystem state transitions**  
> L1 工具执行 lifecycle 目录间的文件移动。
>
> **Rule C · Transitions are governed by explicit tool invocation only**  
> 状态转移路径与执行权限均由工具调用本身决定。任何文件字段、角色推断或外部策略不得影响谁能执行、执行什么转移。

---
---

# NON-VERSION: SEMANTIC NOTES
## commentary on §1 · 不修改定义，只解释意图

**done ≠ archive**

`done` 是完成态，任务仍处于活跃治理视野（active governance scope）内——可被引用、可被审计、可触发后续流程。  
`archive` 是关闭态，任务已退出协调空间（coordination scope）——协议上不再参与任何调度或决策。

两者都是终态候选，但语义权不同：`done` 是"完成但可见"，`archive` 是"关闭且移出"。维护者不应将 `done` 直接当最终归档态使用；`archive_task` 是显式的退出协调空间动作。

**review 的边界**

`review` = pending confirmation，不绑定具体的确认主体（QA / PM / human）。确认主体由调用方在工具调用时决定，不写入协议。

**TASK vs PLAN 判断器**

判断一个文档是否应该进入 `_lifecycle/`，问一句：

> 它是否有明确的终态（clear terminal state）？

- YES → TASK，进入 `_lifecycle/`，适用 §1 状态机
- NO → PLAN，不进入 `_lifecycle/`，属于 intent layer（持续演化的意图空间）

PLAN 的语义是 continuous state document——没有完成态，只有演化态。强行塞入 `_lifecycle/` 会引入错误的 archive 逻辑和错误的执行模型。PLAN 文件的协调位置待独立设计（候选：`fcop/plan/` 或 `fcop/_intent/`）。

**scheduler 边界**

scheduler（如 `FixedTaskRunner`）可以将任务写入 `inbox/`，但不能调用 `claim_task()`。  
`claim_task()` 是 agent 的显式意图声明，scheduler 调用它意味着 scheduler 成为隐式 agent，破坏"claim = observable agent intention"这条不变量。  
一句话：scheduler produces opportunity, not ownership。

---

# NON-VERSION: TOOL LAYER
## implementation appendix · 可随实现演进，不触发版本升级

> 如果本节某个工具分类开始影响"文件夹语义"，必须移入 §1 审查。

**L1 · Lifecycle Topology**（filesystem state transitions）

```
create_task / claim_task / assign_task
submit_task / finish_task / approve_task / reject_task / archive_task
```

**L2 · Coordination Intent**（意图，不改变 topology）

```
assign_agent / reassign_task / escalate_task / set_priority / notify_agent
```

**L3 · Execution Artifacts**（产出，可间接触发 L1）

```
run_task / debug_task / generate_report / run_tests
```

**L4 · Observation**（只读）

```
list_tasks(stage=...) / get_task / trace_task / status_snapshot
```

**L5 · System**（治理基础设施）

```
init_project / fcop_report / fcop_audit / redeploy_rules
```

新增工具（fcop-mcp 3.0）：`claim_task` / `submit_task` / `finish_task` / `approve_task` / `reject_task` / `trace_task` / `status_snapshot`

已删除：`run_task_done`（runtime completion signaling，超出协议职责边界）

---

# NON-VERSION: MIGRATION
## ephemeral · 迁移完成后本节过时，不可从本节推断协议语义

文件迁移映射：

```
tasks/*.md       → _lifecycle/inbox/
log/tasks/*.md   → _lifecycle/archive/
log/reports/*.md → reports/         （不再归档）
log/issues/*.md  → issues/          （added resolved: true）
log/（清空后）   → 删除
```

脚本：`python -m fcop migrate --to-v3`

两阶段建议：先加 `_lifecycle/active/` + `claim_task` 解决重复派发（2.x 补丁），再完整迁移（3.0）。

---

# NON-VERSION: RUNTIME NOTES
## informative only · 不参与协议定义

以下内容是触发本 ADR 的系统层观察，记录在此仅供参考，不构成协议语义。

- `FixedTaskRunner.setInterval(30min)` 与 PM-01 playbook 的双重触发链，是 §1 `active/` 阶段可见性缺失的直接后果。解法：写入 `inbox/` 后由 `claim_task` 原子保护，消除重复。
- OPS session 计数（17 sessions > threshold 10）是 runtime 监控层的表现，不属于 FCoP 协议范围。
- reclaim / TTL / heartbeat 属于 execution runtime policy，见 §EXCLUSION ZONE。

---

# NON-VERSION: EXCLUSION ZONE
## 显式排除 · 以下内容不属于 FCoP 协议，不得进入 §1

| 排除内容 | 所属层 |
|---------|--------|
| 任务超时自动回收（TTL / reclaim） | runtime policy |
| Agent 心跳 / 在线检测 | runtime 监控 |
| health-check 调度频率 | scheduler（FixedTaskRunner） |
| 自动触发下一步动作 | orchestration kernel |
| 决定任务由谁执行 | coordination intent，非 ontology |
| PLAN 文件进入 `_lifecycle/` | PLAN 无终态，属于 intent layer，不是 lifecycle object |
| `risk_level` 字段 | coordination hint，不得驱动状态转移 |
| risk scoring / auto classification | policy inference，不得影响 lifecycle path |
| scheduler 调用 `claim_task()` | scheduler 只能生成机会（写 `inbox/`），不能获取状态所有权 |

---
---

## 开放问题

| # | 问题 | 优先级 | 状态 |
|---|------|--------|------|
| Q1 | `finish_task` 直通路径：`risk_level` 字段决定，还是 PM 显式指定？ | P1 | ✔ 已决：PM 显式 `finish_task(skip_review=true)`；`risk_level` 进 EXCLUSION ZONE |
| Q2 | `FixedTaskRunner` health-check 立即改写 `inbox/` + `claim_task`？ | P1 | ✔ 已决：scheduler 只能写 `inbox/`，不能调用 `claim_task()`；claim 是 agent-exclusive |
| Q3 | PLAN 文件是否进入 `_lifecycle/`？ | P2 | ✔ 已决：不进入；PLAN 是持续演化的意图空间，不是离散状态机；待独立设计 `fcop/plan/` |

## 参考

- `fcop-rules.mdc` Rule 2
- ADR-0003 / ADR-0004
- `.fcop/proposals/20260514-protocol-prune-candidates.md` §3.1

---

## Canonical One-Liner（RFC 2026-05-21 collapse · two-layer per ADR-0040）

**Layer 1 · Cognitive bootstrap**

> **Files carry protocol. Paths address state. Events replay transitions.**
> **文件即协议；位置定义状态；事件记录历史。**

**Layer 2 · Semantic ontology**

> **Files externalize protocol semantics. Paths address state. Events are replayable evidence of state transitions.**
> **文件是协议的外化载体；位置是状态的地址映射；事件是状态转移的可重放证据。**

*(Historical / v1 epigraph: "file location is truth; everything else is trace." — see ADR-0040.)*

| 维度 | 真相载体 | 协议层 |
|------|---------|--------|
| NOW（当前状态）| file path | ADR-0035 §1（本文）|
| PAST（历史轨迹）| transitions events | ADR-0036 |
| Custody（持有解释）| **不存储**，从上两者推导 | NOTE-custody-is-not-a-layer |
| Boundary（边界宪章）| —— | ADR-0038 |

§1 已 frozen。后续任何对 §1 的修改必须先 Supersede 本 ADR。

---

*2026-05-21 · FCoP 3.0 State Ontology · Accepted & Frozen · ADMIN signed-off · semantics locked per RFC*
