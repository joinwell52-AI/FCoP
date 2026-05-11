# ADR-0029: FCoP 核心哲学宪章 v2.0 — 行为治理协议

- **Status**: Accepted
- **Date**: 2026-05-11
- **Deciders**: ADMIN
- **Supersedes**: 部分取代 ADR-0015（补充并收敛哲学定位）
- **Affects**: ADR-0028（write_task() 治理逻辑须迁出，待 Supersede）
- **Related**: [ADR-0015](./ADR-0015-fcop-1.0-ai-os-protocol-charter.md), [ADR-0003](./ADR-0003-stability-charter.md), [ADR-0028](./ADR-0028-auto-risk-assessment.md)

## TL;DR

**中文**：FCoP 是一个约束 Agent 行为的"可观测 + 可审计 + 可治理协议层"，它不调度任务，只规定行为如何被记录与评估。

FCoP = Multi-Agent Behavioral Governance Protocol Layer。它定义：Agent 如何"说清楚自己在做什么"，以及"别人如何验证它做过什么"。

核心三要素：`report`（语义行为声明）、`review`（Code as Law 判例库）、`capability governance`（物理护栏）。`write_task()` 降级为可选的协调原语，不再是协议核心抽象。

**English**: FCoP is the observability + auditability + governance protocol layer for multi-agent systems. It does not schedule tasks; it defines how behavior is recorded and evaluated.

FCoP = Multi-Agent Behavioral Governance Protocol Layer — defining how agents declare what they are doing, and how others verify what they have done.

Three pillars: `report` (semantic behavior declaration), `review` (Code-as-Law precedent chain), `capability governance` (physical guardrail). `write_task()` is demoted to an optional coordination primitive.

---

## Context

### 问题：FCoP 正在漂向工单系统

随着 `write_task()` 承载越来越多的逻辑（生命周期管理、路由、升级、同步、自动风险评估），FCoP 开始积累以下复杂度：

- task lifecycle（任务状态机）
- task ownership（归属与转交）
- task routing（路由到哪个 Agent）
- task escalation（升级机制）
- task synchronization（多 Agent 并发）
- task replay（失败重放）

这些复杂度使 FCoP 逐渐靠近 Jira / BPM / Workflow Engine / Orchestrator——而这些系统恰恰是 AI 协作场景下**最不需要**的东西。

### 根本原因

`write_task()` 被设计成协议核心，导致所有逻辑向它聚集。但 AI Agent 天然不是 ticket processor——它是一个**行为主体**，需要的是"被观察、被审计、被约束"，而不是"被任务化、被排队、被流转"。

### 触发本 ADR 的洞察

> "FCoP 不组织工作，而是治理行为。"

这一句话揭示了协议的真正定位，也指明了避免架构漂移的方向。

---

## Decision

### 一、核心定义

**FCoP = AI 行为基础设施（Behavior Infrastructure）**

| 维度 | 是 | 不是 |
|------|-----|------|
| 解决的问题 | Agent 做了什么？别人怎么看？能做什么？ | 谁该做什么？怎么排队？怎么流转？ |
| 类比 | Git（记录事实） + Code Review（治理行为） | Jira / Jenkins / BPM |
| 受众 | 需要多 Agent 协作可见性和治理的团队 | 需要工单流转系统的团队 |

### 二、三核心支柱

#### 支柱一：report — 语义行为声明（Semantic Behavior Declaration）

```
fcop_report()

本质：让行为成为事实，而不是黑箱。

Agent 不是丢出一段模糊日志，而是必须提供语义化报告，
回答三个核心问题：
  · 做了什么（具体操作动作）
  · 为什么做（意图与因果）
  · 输入输出（行为的物理边界）

价值：将 Agent 的灵活性限制在事实透明的框架内
```

#### 支柱二：review — Code as Law 判例库（Audit Chain）

```
fcop_review()

本质：建立一套"Code as Law"的判例库。

所有行为报告必须接受审阅。
通过 mark_human_approved 等机制，
将人类或高级 Agent 的意志织入行为流。
每一条 Review 都是一个可追溯的因果声明。

价值：形成多方背书的协作记录，建立决策追溯链
```

#### 支柱三：capability governance — 物理护栏（Physical Guardrail）

```
capability governance

本质：为 Agent 打造一个不可逾越的物理护栏。

基于工具调用的后果严重性设定边界（非身份等级）。
Safe → 直接执行
Sensitive → 需要 review
Critical → 需要 human approval，物理拦截直到批准

价值：从"建议遵守"到"强制执行"——高风险行为在获得
      Review 批准前，物理上无法发生
```

**三支柱形成完整闭环：**

```
Agent 行为
    ↓ report（语义声明，拒绝黑箱）
    ↓ review（集体意志，Code as Law）
    ↓ governance（物理护栏，不可逾越）
```

### 三、write_task() 的定位调整

```
原定位（废止）：Core runtime abstraction
新定位：Optional coordination primitive
```

`write_task()` 不删除，但明确降级：

- 对需要显式任务分配的团队，它是一个**可选的协调惯例**
- 它不承载治理逻辑、不触发审批流、不管理生命周期
- 治理逻辑属于独立的 Governance Engine（见 ADR-0028 修订方向）
- 代码组织上移至 `fcop.optional` 命名空间（v2.x 实施）

### 四、极简主义原则（Minimalism Principle）

FCoP 应保持：

- **可观测（Observable）**：Agent 行为必须可见
- **可治理（Governable）**：行为必须可审计、可约束
- **轻量（Lightweight）**：协议本身不成为负担

FCoP 应避免：

- **编排复杂度（Orchestration complexity）**：不做 agent 调度
- **运行时所有权（Runtime ownership）**：不托管 agent 执行状态
- **工作流中心化（Workflow centralization）**：不成为工作流引擎

### 五、非目标声明（Non-Goals）

FCoP **明确不**追求成为：

- Workflow engine（工作流引擎）
- BPM system（业务流程管理系统）
- Project management platform（项目管理平台）
- Ticket orchestration framework（工单编排框架）
- Agent scheduler / orchestrator（Agent 调度器）

此列表作为永久架构约束，任何导致 FCoP 向上述方向漂移的设计应触发 ADR 审查。

### 六、FCoP 与 Codeflow 的边界

```
CodeFlow 负责："让事情发生"
FCoP 负责：  "让事情合法地发生"
```

CodeFlow 丢弃臃肿的任务状态机，直接调用 FCoP 治理原语。

**涌现优先原则**：CodeFlow 中涌现出的任何复杂协作模式，只要它最终能产出 FCoP 认可的 Report 并通过 Review，它就是安全的。FCoP 不限制协作方式，只约束行为合法性。

```
Codeflow 负责：          FCoP 负责：
  多 Agent 开发协作         语义行为声明（report）
  上下文共享               Code as Law 判例链（review）
  代码生成                 物理护栏执行（capability）
  开发体验
```

FCoP 是 Codeflow 的**治理层**，不是 Codeflow 的**流程引擎**。

---

## Consequences

### 正面影响

- **复杂度大幅降低**：消除 task lifecycle / routing / escalation / replay 等非核心概念
- **哲学统一**：所有设计决策都可以对照"是否增强可观测/可审计/可约束"来判断
- **SME 友好**：中小企业真正需要的是"AI 干了什么、有没有风险、谁审核了"——三支柱恰好覆盖
- **防止架构漂移**：Non-Goals 列表提供明确的反向约束

### 对已有 ADR 的影响

| ADR | 影响 |
|-----|------|
| ADR-0028 | 须修订：write_task() 内的治理逻辑迁出，由独立 Governance Engine 承接 |
| ADR-0015 | 本 ADR 补充并收敛其哲学定位，不冲突 |
| ADR-0024~0027（v1.1） | 保留：risk_level / needs_human / human_approval / Skill.tools[] 均属于 review + governance 支柱，方向正确 |

### 一句话

> **FCoP 是一个约束 Agent 行为的"可观测 + 可审计 + 可治理协议层"，它不调度任务，只规定行为如何被记录与评估。**
