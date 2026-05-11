# ADR-0029: FCoP 核心哲学宪章 v2.0 — 行为治理协议

- **Status**: Accepted
- **Date**: 2026-05-11
- **Deciders**: ADMIN
- **Supersedes**: 部分取代 ADR-0015（补充并收敛哲学定位）
- **Affects**: ADR-0028（write_task() 治理逻辑须迁出，待 Supersede）
- **Related**: [ADR-0015](./ADR-0015-fcop-1.0-ai-os-protocol-charter.md), [ADR-0003](./ADR-0003-stability-charter.md), [ADR-0028](./ADR-0028-auto-risk-assessment.md)

## TL;DR

**中文**：FCoP 是 AI 行为治理协议（Behavior Governance Protocol），不是工单系统、工作流引擎或编排框架。核心三要素：`report`（可观测）、`review`（可审计）、`capability governance`（可约束）。`write_task()` 降级为可选的协调原语，不再是协议核心抽象。

**English**: FCoP is a Behavior Governance Protocol, not a ticket system, workflow engine, or orchestration framework. Its three pillars are: `report` (observability), `review` (governance), and `capability governance` (control boundary). `write_task()` is demoted to an optional coordination primitive, no longer a core protocol abstraction.

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

#### 支柱一：report — 可观测性（Observability）

```
fcop_report()

解决：Agent 到底干了什么？

行为：Agent 将自身行为以结构化方式落盘
价值：让协作方、审阅者、ADMIN 能看见 Agent 的行动轨迹
```

#### 支柱二：review — 可审计性（Auditability）

```
fcop_review()

解决：别人怎么看这个行为？

行为：另一个 Agent 或人类对 report 内容发表意见、批准或否决
价值：形成多方视角的协作记录，建立决策追溯链
```

#### 支柱三：capability governance — 可约束性（Control Boundary）

```
capability governance

解决：哪些行为被允许？

行为：在工具调用层面设置权限边界，高风险操作需审批
价值：让 Agent 的能力边界可定义、可执行、可审计
```

**三支柱形成完整闭环：**

```
Agent 行为
    ↓ report（记录）
    ↓ review（审计）
    ↓ governance（约束）
    ↓ capability restriction（执行边界）
```

这个闭环足以支撑：多 Agent 协作、中小企业治理、MCP 工具控制、风险审计。

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
Codeflow 负责：          FCoP 负责：
  多 Agent 开发协作         行为可观测
  上下文共享               审计可追溯
  代码生成                 能力可约束
  开发体验                 风险可治理
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

> **FCoP 不组织工作，而是治理行为。**
