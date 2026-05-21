```
Internet-Engineering-Style Specification             FCoP 工作组
Request for Comments: FCoP-3.0                              朱炜
Category: Coordination Protocol                      joinwell52-AI
ISSN: pending                                         2026 年 5 月


              文件系统协调协议（FCoP）
                  第 3.0 版（中文平行版）
```

## 关于本文 / Status of This Memo

本文档为 `spec/fcop-3.0-rfc.md`（英文 RFC 风格规范）的**中文平行版本**。规范性条款的权威表达以英文版为准；本文为 informative，便于中文实现者与社区阅读。

发布日期：2026-05-21  
许可证：MIT  
版权：Copyright (c) 2026 joinwell52-AI

---

## 摘要 / Abstract

本备忘录定义文件系统协调协议（FCoP）3.0 版——一个供多 Agent 系统在共享文件系统上协作的协议。FCoP 中：

- **文件位置定义当前工作状态**（NOW truth）
- **文件内只追加的事件记录审计历史**（PAST trace）
- **其余一切都不具权威性**

FCoP 在多 Agent 协调中所处的架构位置，等价于 POSIX 对进程、OCI 对容器：标准化参与者之间的契约，但不拥有它们的执行。

FCoP 3.0 把协议表面压缩为三层：

1. **状态层（NOW truth）**：目录位置
2. **事件层（PAST trace）**：文件 YAML frontmatter 中的只追加 `transitions:` 数组
3. **边界宪章**：防止协议吞噬 runtime、调度、强制等职责的元规则

"Custody（持有权）"概念**仅作派生解释保留**，绝不作为存储字段。

---

## 1. 引言 / Introduction

多 Agent 在共享文件系统上协作需要一小套稳定的约定，让所有参与者无需运行同一个 runtime 即可依赖。现有协调层要么把参与者绑定到特定编排框架（Temporal、LangGraph、CrewAI），要么定义需要回放才能重建当前状态的事件溯源日志（Git、Kafka、EventStore）。

FCoP 选择不同路径：**把文件系统本身当作协调基底**。目录位置即当前状态。文件内只追加的事件记录历史。其它信息不具权威。

这种方式刻意保持极简。任何能 `read` / `write` / `rename` 文件的 Agent 都可以参与 FCoP，无需采纳特定 SDK、runtime 或 daemon。

### 1.1 用语规范

文档中的 "MUST"（必须）、"MUST NOT"（必不得）、"REQUIRED"（必需）、"SHALL"（应当）、"SHALL NOT"（不应当）、"SHOULD"（应该）、"SHOULD NOT"（不应该）、"RECOMMENDED"（推荐）、"MAY"（可以）、"OPTIONAL"（可选）按 [RFC2119] 解释。

### 1.2 术语

| 术语 | 定义 |
|------|------|
| 生命周期根（Lifecycle root）| `fcop/_lifecycle/` 目录，包含五个阶段子目录 |
| 阶段（Stage）| 生命周期根下五个目录之一（`inbox`/`active`/`review`/`done`/`archive`）|
| L1 工具 | 契约允许在阶段间移动文件的工具 |
| 迁移（Transition）| 单次文件从一个阶段移动到另一阶段（或从创建到 `inbox`）|
| 事件（Event）| `transitions:` 数组中见证一次迁移的 YAML 记录 |
| NOW 真相 | 系统当前状态，仅由文件位置定义 |
| PAST 踪迹 | 状态变更的历史，仅由只追加 `transitions:` 数组定义 |
| Custody（持有权）| 派生的文件归属解释；不是协议字段 |

---

## 2. 核心声明 / Canonical Statement

> **FCoP is a filesystem-native protocol where file location defines current state, and all historical and ownership semantics are derived from append-only transition traces.**
>
> **FCoP 是一个文件系统原生协议：文件位置定义当前状态，所有历史与持有权语义都从只追加的迁移轨迹推导而来。**

三句话（Layer 1 · 认知引导，依据 ADR-0040）：

> **Files carry protocol. Paths address state. Events replay transitions.**
>
> **文件即协议；位置定义状态；事件记录历史。**

压缩形式化定义（Layer 2 · 语义本体）：

> **Files externalize protocol semantics. Paths address state. Events are replayable evidence of state transitions.**
>
> **文件是协议的外化载体；位置是状态的地址映射；事件是状态转移的可重放证据。**

（历史/题词：*"file location is truth; everything else is trace." / "文件位置即真相；其它一切都是踪迹。"* —— v1 canonical，依据 ADR-0040 已退出定义性表面，但保留在 2026-05-21 及之前归档的 essays 和 reviews 中。）

FCoP **不是** Agent 运行时、**不是**工作流引擎、**不是**编排内核。它定义参与者之间的契约；它不执行该契约。

---

## 3. 状态层（NOW 真相）/ State Layer (NOW Truth)

### 3.1 目录拓扑

合规实现 MUST 在项目根目录维护以下结构：

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

所有五个生命周期子目录 MUST 位于同一文件系统挂载点。

### 3.2 基底假设

> **FCoP 3.0 假设每一个生命周期根都位于一致性单一边界的文件系统内。**

跨分布式文件系统、弱一致性网络挂载点、或多主机并发写入场景下的实现 MUST 自行提供外部一致性层。协议本身不规定也不提供。

### 3.3 阶段定义

| 阶段 | 定义 |
|------|------|
| `inbox` | created（已创建）|
| `active` | claimed（已认领）|
| `review` | pending confirmation（等待确认）|
| `done` | completed（已完成）|
| `archive` | closed（已关闭）|

定义已冻结。实现 MUST NOT 为这些名称赋予额外语义。

### 3.4 允许的迁移

| 从 | 到 | 工具 |
|----|----|------|
| — | `inbox` | `create_task` |
| `inbox` | `active` | `claim_task` |
| `active` | `review` | `submit_task` |
| `active` | `done` | `finish_task(skip_review=true)` |
| `review` | `done` | `approve_task` |
| `review` | `active` | `reject_task` |
| `done` | `archive` | `archive_task` |

上表以外的迁移 NOT permitted。实现 MUST 拒绝。

### 3.5 核心规则（A / B / C）

> **规则 A · 文件路径是唯一的 NOW 真相。**
> 实现 MUST NOT 依赖文件内容判定当前状态。

> **规则 B · L1 工具执行文件系统状态迁移。**
> 只有 L1 工具 MAY 在生命周期子目录间移动文件。

> **规则 C · 状态迁移仅由显式工具调用治理。**
> 迁移路径与执行权限 MUST 编码在工具调用本身。文件字段、角色推断、外部策略不得决定。

---

## 4. 事件层（PAST 踪迹）/ Event Layer (PAST Trace)

### 4.1 Frontmatter Schema

`_lifecycle/` 下每个文件 MUST 在 YAML frontmatter 携带 `transitions:` 数组：

```yaml
---
protocol: fcop
version: 3
type: TASK
task_id: TASK-20260521-001-PM-to-DEV
transitions:
  - at: 2026-05-21T10:00:00+08:00
    from: null
    to: inbox
    by: PM-01
    tool: create_task
---
```

### 4.2 事件 Schema

每条事件 MUST 包含：

| 字段 | 类型 | 说明 |
|------|------|------|
| `at` | ISO-8601 datetime | 迁移发生时间 |
| `from` | string \| null | 源阶段（创建时为 `null`）|
| `to` | string | 目标阶段 |
| `by` | string | 执行者标识 |
| `tool` | string | 执行迁移的 L1 工具名 |

可选字段：`note`、`supersedes`。

### 4.3 核心规则（E / F / G）

> **规则 E · 每次 mv 必产生一条事件。**

> **规则 F · 事件只追加。** 修正时追加新事件并通过 `supersedes` 引用旧事件。

> **规则 G · 事件是仅供审计的 PAST 踪迹。**
> 事件流是历史、审计、追溯的**唯一**权威源。**当前状态由文件位置定义（规则 A），绝不通过回放事件得出。** 实现 MUST NOT 从 `transitions:` 派生 `current_state(file)`。回放仅允许用于审计与一致性校验。

### 4.4 原子性（Write-Then-Rename）

> **事件不是状态迁移的副作用。**
> **事件本身就是被书面见证的状态迁移。**

事件与文件移动**不是需要排序的两个操作**，而是**同一个协调行为的两个面**。

实现 MUST 用以下模式作为单次原子操作：

```
1. 读取源文件
2. 在内存中向 transitions: 追加事件
3. 写入目标目录的临时文件（.{id}.tmp）
4. fsync 临时文件
5. os.rename(tmp, destination)   ← POSIX 原子性保证
6. 若源与目标不同，删除源文件
```

第 5 步是原子提交点。第 5 步前：状态 = 源位置，事件未写入。第 5 步后：状态 = 目标位置，事件已写入。**不存在可观察的中间状态。**

---

## 5. 边界宪章 / Boundary Charter

### 5.1 三大原则

> **原则 1 · 协议描述，不执行。**

> **原则 2 · 协议外化，不拥有。**

> **原则 3 · 协议协调，不编排。**

### 5.2 排除范围

| 排除项 | 所属 |
|--------|------|
| 任务执行（LLM 调用、Tool 调用）| Runtime 层 |
| 调度（队列、DAG、重试）| 工作流引擎 |
| 沙箱、能力强制 | OS / Runtime |
| 内存系统、向量数据库 | 内存层 |
| 心跳、TTL、reclaim、自动恢复 | Runtime policy |
| 任务分派策略（谁做什么）| 协调意图 |
| `risk_level` 驱动状态迁移 | 协调提示 |
| `custody` / `ownership` 存储字段 | 仅作解释 |

### 5.3 五问过滤器

任何扩展提案 MUST 通过：

1. 描述语义 vs 执行行为？后者拒绝。
2. 文件契约 vs runtime 状态？后者拒绝。
3. 协调多 Agent vs 调度某 Agent？后者拒绝。
4. 能否在没有 FCoP runtime 下被另一 host 重新实现？不能则拒绝。
5. 是否与 Temporal / LangGraph / CrewAI 职责重叠？重叠则拒绝。

### 5.4 豁免条款

仅在证据支持下重新讨论：

- **E1 复杂度逼迫**：6 个月内 2+ 独立项目报告同一缺口
- **E2 跨 runtime 失效**：实证某场景缺该扩展时无法完成
- **E3 内部矛盾**：现有规则不可调和地冲突

**永远不豁免**：FCoP 拥有 LLM/Tool 执行、runtime sandbox / capability enforcement、协议专属 daemon / 长进程。

---

## 6. 身份（文件名语法）/ Identity

```
{TYPE}-{YYYYMMDD}-{NNN}-{SENDER}-to-{RECIPIENT}(-{slug}).md
```

文件名 MUST NOT 在文件生命周期内改变。只有文件位置（§3）变化。

---

## 7. Custody（说明性）

Custody NOT 协议状态模型的一部分。实现 MUST NOT 引入 `custodian` 字段。

派生读取模式：

| 文件位置 | 派生的 custodian |
|---------|-----------------|
| `_lifecycle/inbox/` | 无 |
| `_lifecycle/active/` | 最近一次 `to: active` 事件的 `by` |
| `_lifecycle/review/` | 无 |
| `_lifecycle/done/` / `archive/` | 最后一次 active 的 `by`（仅审计）|

---

## 8. 合规要求 / Conformance Requirements

合规实现 MUST：C1-C10（见英文 RFC § 8）。
合规实现 MUST NOT：P1-P5（见英文 RFC § 8）。

完整条款见 `spec/fcop-3.0-rfc.md` § 8 或 `spec/fcop-3.0-spec.zh.md` § 6。

---

## 9. 安全考量 / Security Considerations

FCoP 将所有强制委托给底层 OS 与 runtime 层（原则 1，§5.1）。

- **文件系统权限**：生命周期根的访问控制由 OS 负责。FCoP 不规定文件模式、ACL、用户/组约定。
- **能力声明 vs 强制**：实现 MAY 声明 Agent 能力，但 MUST NOT 强制。强制由 host runtime 负责。
- **只追加审计**：规则 F 在协议层提供防篡改证据。抗篡改性（针对拥有生命周期根写权限的攻击者）需外部机制（签名 commit、一次写存储等）；FCoP 不规定。
- **基底信任**：§3.2 把单一致性文件系统假设显式化。部署在不可信一致性层的实现继承该层的安全性质。

---

## 10. 互操作性考量 / Interoperability Considerations

FCoP 为跨 runtime 互操作而设计。任何能 `read`/`write`/`rename` 生命周期根的 Agent 都能参与，无关语言、框架、runtime。

实现 SHOULD：

- 发出相同的事件 schema（§4.2），使踪迹跨实现可读
- 修改文件时保留未知可选字段
- 把缺少 `transitions:` 的文件视为合法历史产物（见附录 B）
- 绝不向 `_lifecycle/` 目录结构引入 host 专属扩展

---

## 11. 版本管理 / Versioning

| 版本 | 日期 | 变更 |
|------|------|------|
| 3.0 | 2026-05-21 | 首次发布。State + Event + Boundary。 |

未来规则：

- **MAJOR（4.0）**：变更 §3 拓扑、阶段定义、允许迁移、规则 A/B/C
- **MINOR（3.x）**：新增可选字段、说明性章节、非破坏 schema 扩展
- **PATCH（3.0.x）**：仅编辑性修正

附录 A（工具层）与附录 B（迁移）MAY 在不 bump 版本下变更。

---

## 12. 引用 / References

### 规范性引用

- [RFC2119] Bradner, S., "Key words for use in RFCs to Indicate Requirement Levels", BCP 14, RFC 2119, March 1997.
- [POSIX-rename] IEEE Std 1003.1-2017, `rename()` atomicity guarantee.

### 说明性引用

- ADR-0035 · State Ontology（已冻结）
- ADR-0036 · Event Layer
- ADR-0038 · Boundary Charter
- NOTE-custody-is-not-a-layer
- ADR-0033 · 尾标文件名采纳
- ADR-0004 · `os.rename()` 原子性保证
- `fcop-rules.mdc` Rule 2 · 文件即协议，文件夹即组织
- PROPOSAL `20260521-rfc-semantic-collapse-and-custody-rejection.md`

---

## 13. 作者地址 / Authors' Addresses

```
Wei Zhu / 朱炜
joinwell52-AI

Repository: https://github.com/joinwell52-AI/FCoP
DOI:        10.5281/zenodo.19886036
License:    MIT
```

---

## 附录 A · 工具层（说明性）

工具分类仅供实现者参考，MAY 在不 bump 版本下演进。

| 层 | 用途 | 示例 |
|----|------|------|
| L1 | 生命周期拓扑 | `create_task`, `claim_task`, `submit_task`, `finish_task`, `approve_task`, `reject_task`, `archive_task` |
| L2 | 协调意图（不改拓扑）| `assign_agent`, `set_priority`, `notify_agent` |
| L3 | 执行产物 | `run_task`, `generate_report` |
| L4 | 观察（只读）| `list_tasks`, `get_task`, `trace_task` |
| L5 | 系统 / 治理 | `init_project`, `fcop_audit` |

---

## 附录 B · 从 2.x 迁移（说明性）

```
fcop/tasks/*.md       → fcop/_lifecycle/inbox/*.md
fcop/log/tasks/*.md   → fcop/_lifecycle/archive/*.md
fcop/log/reports/*.md → fcop/reports/*.md          （不再归档）
fcop/log/issues/*.md  → fcop/issues/*.md           （加 resolved: true）
fcop/log/             → 删除
```

迁移的文件 MUST 接收合成事件：

```yaml
transitions:
  - at: <file-mtime>
    from: null
    to: <current-stage>
    by: migration
    tool: fcop_migrate_v3
```

迁移脚本：`python -m fcop migrate --to-v3`

---

## 附录 C · 一句话规范

> **FCoP 是一个协调协议：文件位置定义当前工作状态，文件内只追加的事件记录审计历史，其余一切都不具权威性。**

---

```
FCoP 3.0 RFC 中文平行版完                              [第 12 页]
```
