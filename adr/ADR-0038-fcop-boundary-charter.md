# ADR-0038: FCoP Boundary Charter
## Meta-Charter · What FCoP Is and What FCoP Is Not

| 字段 | 值 |
|---|---|
| **Status** | **Accepted** (2026-05-21 · ADMIN signed-off · exemption clause §5.1 added per RFC) |
| **Date** | 2026-05-21 |
| **Type** | Meta-Charter (governs all future ADRs) |
| **Depends on** | ADR-0029（行为治理宪章 v2.0）、ADR-0035（State Ontology） |
| **Filters** | ADR-0036（已通过）, 及所有未来 ADR |
| **Already-rejected** | ADR-0037（Custody Layer · 2026-05-21 RFC 否决，详见 NOTE-custody-is-not-a-layer.md）|

---

## Core Statement

> **FCoP is Agent POSIX, not Agent OS.**  
> **FCoP 是 Agent POSIX，不是 Agent OS。**

FCoP 是**外化协调协议**（externalised coordination protocol），不是 runtime / scheduler / executor。  
本 ADR 是一份**元宪章（meta-charter）**：它不引入新功能，只定义"FCoP 不做什么"，作为后续所有 ADR 的过滤器。

---

## ⚠ HARD BOUNDARY

> **任何引入"执行 / 调度 / 强制 / 拥有"语义的 ADR，必须先通过本宪章的边界审查。**

---

## §1 · The Three Boundary Principles

> **以下三条是 FCoP 的版本承诺。任何后续 ADR 不得违反。**

> **Principle 1 · Protocol describes, not executes**  
> FCoP 定义"`active → review` 是合法 transition"，但不负责真正去 `mv`、不调度谁来做、不执行任务本身。
>
> **Principle 2 · Protocol externalises, not owns**  
> FCoP 定义事件格式、状态语义、文件契约，但不拥有日志系统、不拥有数据库、不拥有 runtime 状态。
>
> **Principle 3 · Protocol coordinates, not orchestrates**  
> FCoP 定义"谁可以接手 review"的语义，但不决定"现在让谁去 review"——后者是 runtime / scheduler 的职责。

---

## §2 · Scope Matrix

### ✔ FCoP IS responsible for

| 职责 | 含义 |
|------|------|
| 状态语义（State Semantics） | `inbox / active / review / done / archive` 的含义统一 |
| 生命周期定义（Lifecycle Definition） | 哪些状态合法、哪些 transition 合法 |
| Transition 契约（Transition Contract） | 哪个工具执行哪条迁移 |
| 行为外化格式（Event Externalisation Format） | 事件以什么 schema 落盘 |
| 协调语义（Coordination Semantics） | 多 Agent 如何理解同一份文件的状态 |
| 能力声明（Capability Declaration） | Agent 声称自己能做什么 |
| 审计契约（Audit Contract） | 历史只增不改、文件即证据链 |

### ❌ FCoP IS NOT responsible for

| 职责 | 属于谁 | 红线原因 |
|------|--------|---------|
| 任务执行（task execution） | Runtime（Cursor / Claude / OpenAI Operator）| 否则 FCoP 退化为 Agent Framework |
| LLM 调用（LLM invocation） | Runtime | 同上 |
| Tool 执行（tool execution） | Runtime / MCP host | 同上 |
| 调度（scheduling / queue / DAG / retry）| Workflow Engine（Temporal / LangGraph / CrewAI）| 否则与 orchestrator 打架 |
| 沙箱与权限强制（sandbox / capability enforcement）| OS / Runtime | FCoP 只声明 capability，由 runtime enforce |
| Memory / 向量检索（embedding / vector DB）| Memory System | 不在协议层 |
| 自动触发下一步（auto-trigger next action）| Orchestration kernel | 见 ADR-0035 EXCLUSION ZONE |
| Heartbeat / TTL / reclaim | Runtime policy | 见 ADR-0035 EXCLUSION ZONE |
| 决定任务由谁执行（task assignment policy）| Coordination intent / runtime | 协议只描述合法转移，不裁决执行者 |

---

## §3 · The Layer Map

FCoP 在整个 Agent 协作栈中的精确位置：

```
┌─────────────────────────────────────────────────────────────┐
│  Application Layer    Cursor / Claude / OpenAI Operator     │  ← 应用
├─────────────────────────────────────────────────────────────┤
│  Runtime Layer        LangGraph / CrewAI / AutoGen / MCP    │  ← 执行
├─────────────────────────────────────────────────────────────┤
│  ★ FCoP Protocol ★    Identity + Location + Event           │  ← 协调（本协议）
│                       状态语义 · 生命周期 · 行为外化           │
├─────────────────────────────────────────────────────────────┤
│  Substrate            LLM API / MCP / Filesystem / OS       │  ← 基底
└─────────────────────────────────────────────────────────────┘
```

类比定位：

| 协议 | 定位 | FCoP 对应 |
|------|------|----------|
| TCP/IP | 不拥有任何应用，但所有应用必经 | ✔ 类似 |
| POSIX | 不拥有任何进程，但所有进程按它的接口工作 | ✔ 类似（最接近）|
| Git | 不拥有 IDE / CI，但所有人通过它交换代码状态 | ✔ 类似 |
| OCI | 不运行容器，但所有 runtime 按它的格式工作 | ✔ 类似 |
| Kubernetes | 拥有 runtime + scheduler + executor | ❌ FCoP 不要走这条路 |

---

## §4 · The Three-Layer Reference Model

> **以下是 FCoP 协议本身的内部分层，三层都属于 FCoP 范围，由不同 ADR 定义。**

| Layer | 回答 | 定义于 |
|-------|------|--------|
| **Layer 1 · Identity** | 它是谁？ | Rule 2 + ADR-0033（trailing slug） |
| **Layer 2 · Location** | 它现在在哪？ | ADR-0035 |
| **Layer 3 · Event** | 它经历了什么？ | ADR-0036（待提案）|

Layer 1 是原子（永不变），Layer 2 是当前状态（可 `mv`），Layer 3 是历史（只追加）。

---

## §5 · The Filter Rule（针对所有未来 ADR）

> **任何新 ADR 在 Accepted 之前必须通过以下五问：**

1. **它是在描述语义，还是在执行行为？** —— 后者拒绝。
2. **它是在定义文件契约，还是在拥有 runtime 状态？** —— 后者拒绝。
3. **它是在协调多 Agent，还是在调度某个 Agent？** —— 后者拒绝。
4. **它能否在没有 FCoP runtime 的情况下被另一个 host 重新实现？** —— 不能则拒绝。
5. **它是否会让 FCoP 与 Temporal / LangGraph / CrewAI 在职责上重叠？** —— 重叠则拒绝。

通不过五问的 ADR，要么改写到本边界之内，要么放弃。

---

## §5.1 · Exemption Clause / 豁免条款

> **本边界不是为了冻结协议，而是为了防止盲目扩张。**

边界宪章存在一个**反向风险**：过于严格的过滤器会拒绝所有演进，让 FCoP 陷入"理论纯粹但无法适应真实复杂度"的僵化。本豁免条款明确**什么情况下可以重新讨论边界**：

### 可豁免的触发条件

| # | 触发情形 | 证据要求 |
|---|---------|---------|
| E1 | **复杂度逼迫（complexity-forced）** | 至少 2 个独立项目/团队在 6 个月内报告同一类协议缺口（field reports）|
| E2 | **跨 runtime 不可协作（cross-runtime breakdown）** | 实证某种 Agent 协作场景在没有该扩展时**根本无法完成**（不是"不方便"）|
| E3 | **核心规则自相矛盾（internal contradiction）** | 现有 ADR 之间出现无法调和的语义冲突 |

### 豁免流程

满足 E1/E2/E3 中任一条件的提案，可以：

1. **写一份 PROPOSAL** 详述触发条件与证据
2. 在 PROPOSAL 中明确说明**违反五问中的哪一条**及**为什么必须违反**
3. 经 ADMIN review 后可作为**Boundary Amendment ADR**进入正式 ADR 流程
4. Amendment ADR 一旦 Accepted，应当**同时修订本宪章**——把新增的合法例外写进 §5 或新增 §X，让边界条件保持透明

### 不可豁免的红线

以下三条**永远不豁免**（即使触发 E1/E2）：

| 红线 | 原因 |
|------|------|
| ❌ FCoP 拥有 LLM 调用 / Tool 执行 | 一旦拥有，FCoP 与所有 Agent Runtime 直接竞争，失去"最低公共分母"地位 |
| ❌ FCoP 拥有 runtime sandbox / capability enforcement | 一旦拥有，FCoP 必须管理进程/权限/隔离，成为 OS |
| ❌ FCoP 拥有专属于本协议的 daemon / 长进程 | 一旦拥有，FCoP 不再是 filesystem-native 协议 |

这三条是 FCoP **存在的基础假设**——豁免它们等于另起一个新协议，不是演进。

---

## §5.2 · 为什么需要豁免条款（meta）

历史教训：纯粹主义协议往往因为太严而被绕过。POSIX 因为对线程的支持来得太晚，导致 pthread 长期是分裂状态；HTTP/1.1 因为对长连接的严格定义，导致 WebSocket 不得不另起协议。

FCoP 选择**承认边界本身是可演进的**——但演进必须经过同样严格的协议流程，不是某个人某天觉得"加个字段没什么"就动手。

边界宪章的真正职责不是"拒绝一切扩展"，而是**让每一次扩展都付出与其影响相称的论证代价**。

---

## §6 · 战略定位（informative）

> **本节为说明性内容，不构成协议规则。**

FCoP 的护城河来自一个简单事实：

> **FCoP 不与任何 Runtime 竞争，所以所有 Runtime 都能采用它。**

文件系统是当前所有 Agent runtime 共有的最低公共分母：Cursor / Claude / OpenAI Operator / 本地 Agent / GitHub Actions 都能 `read / write / rename` 一个文件。FCoP 把"行为外化到共享文件语义空间"作为唯一要求，绕开了 Runtime 统一难题。

协议的采用从来不是因为"大家愿意统一"，而是因为"复杂度逼迫统一"。FCoP 的机会窗口是**跨 Runtime Agent 协作场景成为常态**的那一天——当 Cursor Agent 与 Claude Code 必须协作完成同一项目时，除了 FCoP 没有第二个公共语言可用。

---

## §7 · Relationship to Existing ADRs

- **ADR-0029（行为治理宪章 v2.0）**：本 ADR 是 0029 的边界细化。0029 说"FCoP 治理行为不调度任务"，本 ADR 把这句话展开为可执行的五问过滤器。
- **ADR-0035（State Ontology）**：本 ADR 为 0035 的 EXCLUSION ZONE 提供原则依据。0035 的 EXCLUSION ZONE 是本宪章在 Layer 2 的具体应用。
- **ADR-0036 / 0037（待提案）**：必须先通过本宪章 §5 五问，才能进入 Accepted。

---

## Open Questions

| # | 问题 | 优先级 |
|---|------|--------|
| Q1 | 是否需要在 `fcop-rules.mdc` 中加一条 Meta-Rule 引用本宪章？ | P2 |
| Q2 | 五问过滤器是否需要写成 `fcop_audit()` 的自动检查项？ | P3（runtime 层，不在本协议范围）|

## 参考

- ADR-0029 · FCoP 行为治理宪章 v2.0
- ADR-0035 · State Ontology
- `fcop-protocol.mdc` §Architectural Principle: Tools are a Convenience Layer

---

*2026-05-21 · FCoP Boundary Charter · Accepted · ADMIN signed-off · with exemption clause · Agent POSIX locked*
