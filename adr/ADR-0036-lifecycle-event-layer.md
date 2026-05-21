# ADR-0036: FCoP 3.0 Lifecycle Event Layer
## Layer 3 · Process Must Be Loggable

| 字段 | 值 |
|---|---|
| **Status** | **Accepted** (2026-05-21 · ADMIN signed-off · Rule G hardened per RFC) |
| **Date** | 2026-05-21 |
| **Extends** | ADR-0035（State Ontology · NOW truth）|
| **Filtered by** | ADR-0038（Boundary Charter）|
| **Depends on** | Rule 5（append-only history）、ADR-0004（`os.rename()` 原子性） |
| **Type** | Protocol Additive (MINOR, targets fcop 3.0) |

---

## Core Insight

> **过程本身也是协议。**  
> **Process itself is part of the protocol.**

ADR-0035 解决了"文件在哪个桶"——Layer 2 · Location。  
ADR-0036 解决"文件经历了什么"——Layer 3 · Event。

文件夹只能表达**当前位置**，不能表达**它是怎么来到这里的**。本 ADR 给每一次状态迁移留下可登记的事件痕迹。

---

## ⚠ Boundary Compliance（per ADR-0038）

| 五问 | 答 |
|------|----|
| 描述还是执行？ | 描述 ✔（只定义事件 schema） |
| 文件契约还是 runtime 状态？ | 文件契约 ✔（事件落盘） |
| 协调还是调度？ | 协调 ✔（不决定谁、不触发什么） |
| 能否被另一 host 重新实现？ | 能 ✔（任何能写 frontmatter 的 host）|
| 与 Temporal / LangGraph 重叠？ | 不重叠 ✔（不做 event bus / pub-sub）|

通过。

---

## §1 · Event Layer Specification

### 1.1 每个文件自带 transitions 履历

每个 task 文件的 frontmatter 携带 `transitions:` 数组。  
每次 L1 工具执行 `mv` 时，**必须**在数组末尾追加一条事件，**不得**修改既有条目。

```yaml
---
protocol: fcop
version: 1
type: TASK
task_id: TASK-20260521-001-PM-to-DEV
transitions:
  - at: 2026-05-21T10:00:00+08:00
    from: null
    to: inbox
    by: PM-01
    tool: create_task
  - at: 2026-05-21T10:15:00+08:00
    from: inbox
    to: active
    by: DEV-01
    tool: claim_task
  - at: 2026-05-21T14:30:00+08:00
    from: active
    to: review
    by: DEV-01
    tool: submit_task
---
```

### 1.2 事件 Schema

每条 transition 事件**必须**包含以下字段，**不得**新增 transition 之外的隐式字段：

| 字段 | 类型 | 含义 |
|------|------|------|
| `at` | ISO-8601 datetime | 事件发生时间 |
| `from` | string \| null | 源状态（首次创建为 `null`）|
| `to` | string | 目标状态 |
| `by` | string | 执行者标识（agent role / id）|
| `tool` | string | 实际调用的 L1 工具名 |

可选字段：

| 字段 | 类型 | 含义 |
|------|------|------|
| `note` | string | 自由文本说明 |
| `supersedes` | string | 关联修订事件（per Rule 5）|

### 1.3 三条事件层规则（§1 内的版本承诺）

> **Rule E · Every mv produces an event**  
> 每次 L1 工具执行的 `mv` 必须在文件 frontmatter 的 `transitions:` 追加一条事件。无事件的 mv 视为协议违反。
>
> **Rule F · Events are append-only**  
> `transitions:` 数组只追加，不修改、不删除。已落盘事件即历史，与 Rule 5 一致。
>
> **Rule G · Events are audit-only, not state**  
> 事件流是 **PAST 的唯一真相**（only canonical source for history / audit / trace）。  
> **当前状态由文件位置决定**（ADR-0035 Rule A · path = NOW truth）。  
> 任何"从 events 推导当前状态"的做法只能用于审计与一致性校验，**不得**用于运行时的状态判定。  
> Events ≠ State；events 是 trace，不是 truth-of-now。

---

## §2 · Optional Global Ledger（NON-VERSION）

> **本节为可选审计冗余，不参与版本定义。Runtime 可实现，可不实现。**

项目**可选**在 `fcop/_ledger/` 下维护 append-only 的月度全局事件簿：

```
fcop/
└── _ledger/
    ├── LEDGER-202605.md
    └── LEDGER-202606.md
```

每条记录是文件级 transition 的全局回声（actor / from / to / at / file-id）。  
ledger **与文件履历互为冗余**：文件丢失时 ledger 可作审计参考，ledger 损坏时文件履历仍是真相。  
**ledger 不参与 Rule A（path = state truth），不得作为状态判定依据**。

---

## §3 · NON-VERSION: SEMANTIC NOTES

**为什么不引入 `_transit/` 在途桶？**

因为 `os.rename()` 在同一挂载点是原子的（ADR-0004），中间不存在文件系统层面的"运送过程"。引入 `_transit/` 会制造"卡在中间"的伪状态，破坏 ADR-0035 Rule A。  
"过程"由 transitions 履历表达，不由位置表达。

**为什么 transitions 在 frontmatter 而不是独立文件？**

文件履历必须**跟着文件走**。如果履历独立于文件存放，文件被移动/复制/借出时履历会丢失。frontmatter 保证了 Identity + Location + Event 三层物理不可分离。

**Event Layer 与 ADR-0035 Rule A 的关系**

Rule A："File path = state truth"——**当前**状态由路径定义。  
Rule E/F/G："transitions = history of state changes"——**历史**由事件定义。  
两者不冲突：路径是 *now*，事件是 *past*。

---

## §4 · NON-VERSION: TOOL LAYER

### 4.1 事件 + mv 的原子性策略（**必须遵守**）

事件写入与文件移动**不是天然原子**。错误的实现顺序会留下两类不一致：
- **先 rename 后写履历**：状态变了，履历缺失 → Rule E 违反
- **先写履历后 rename**（直接修改源文件）：履历更新了，状态没变 → 出现"未来事件"

**强制实现策略**：**Write-Then-Rename Atomic Pattern**

```
# 标准 L1 工具实现（伪代码）
def claim_task(task_id):
    src = _lifecycle/inbox/{task_id}
    dst = _lifecycle/active/{task_id}

    # 1. 读原文件
    file = read(src)

    # 2. 在内存中追加事件
    file.frontmatter.transitions.append({
        at: now(), from: "inbox", to: "active",
        by: caller_id, tool: "claim_task"
    })

    # 3. 写到临时文件（与 dst 同目录，确保同一挂载点）
    tmp = _lifecycle/active/.{task_id}.tmp
    write(tmp, file)
    fsync(tmp)

    # 4. 原子 rename：tmp → dst（POSIX 保证）
    os.rename(tmp, dst)

    # 5. 删除原文件（如果与 dst 不是同一路径）
    if src != dst:
        os.unlink(src)
```

**关键性质**：
- 步骤 4 的 `os.rename(tmp, dst)` 是 POSIX 原子操作（per ADR-0004）
- 在步骤 4 完成的**前一刻**，系统状态是"文件仍在 inbox，无事件"；**后一刻**是"文件在 active，事件已写"
- 不存在中间状态 → 满足 Rule A 和 Rule E 同时不被破坏

**失败处理**：
- 若步骤 3/4 失败：tmp 文件可能残留，由 `fcop_audit` 检出（"orphan tmp file"）并清理；源文件未变，可重试
- 若步骤 5 失败（极少见）：出现"同一文件存在两处"，由 `fcop_audit` 检出（"duplicate task_id across stages"），人工介入

### 4.2 跨挂载点的限制

`os.rename()` 只在**同一挂载点**内保证原子性。FCoP 3.0 要求 `_lifecycle/` 五个子目录**必须在同一挂载点**，否则原子性失效。

实现者**不得**将 `_lifecycle/archive/` 挂载到独立存储（如 NAS / S3-fuse）——归档迁移到冷存储必须通过应用层 copy + delete + verify 流程，且**不再属于本协议范围**（per ADR-0038）。

---

## §5 · NON-VERSION: MIGRATION

**2.x → 3.1 迁移**：

- 新建任务：直接带 `transitions:` 字段。
- 历史任务：迁移脚本写入一条合成事件 `{at: <file-mtime>, from: null, to: <current-bucket>, by: "migration", tool: "fcop_migrate_v3"}`。
- 缺少 `transitions:` 字段的旧文件视为**合法历史**，但所有新 mv 必须开始追加事件。

脚本：`python -m fcop migrate --to-v31`

---

## §6 · NON-VERSION: EXCLUSION ZONE

| 排除内容 | 所属层 | 原因 |
|---------|--------|------|
| Event Bus / pub-sub | Runtime | 见 ADR-0038 §2 |
| Webhook trigger | Runtime | 同上 |
| 自动触发下一步动作 | Orchestration | 见 ADR-0035 |
| Event-driven scheduler | Workflow engine | 见 ADR-0038 |
| 实时事件流（streaming）| Runtime | 文件 + ledger 是 batch-friendly，不是 stream |

---

## Open Questions

| # | 问题 | 优先级 |
|---|------|--------|
| Q1 | `_ledger/` 是否进入 §1 必选？ | P2 — 暂留 optional |
| Q2 | transitions 是否需要 schema 校验（JSON Schema）？ | P1 — 建议是 |
| Q3 | 跨文件 supersedes 链如何与 transitions 协同？ | P2 |

## 参考

- ADR-0035 · State Ontology（被本 ADR extends）
- ADR-0038 · Boundary Charter（本 ADR 接受其过滤）
- `fcop-rules.mdc` Rule 5（append-only history）
- ADR-0033 · trailing-slug filename

---

*2026-05-21 · FCoP 3.0 Event Layer · Accepted · ADMIN signed-off · audit-only PAST truth · atomic write-then-rename pattern locked*
