# FCoP 三层语义执行链模型

**文档类型**：核心规范参考（Canonical Reference）  
**版本**：1.0  
**日期**：2026-05-12  
**依赖**：ADR-0030 · ADR-0031 · ADR-0032  

---

## 一、模型概述

FCoP 协议由三个语义层组成，构成一条完整的**语义执行链（Semantic Execution Chain）**：

```
Protocol State
      │
      ▼
┌─────────────────────────────────────────────────────────┐
│  Layer 1 · Schema Layer (ADR-0030)                      │
│  定义：能力边界 / 行为是否被允许                           │
│  产出：Capability schema · risk_level (Safe/Sensitive/  │
│        Critical) · MCP Interceptor policy               │
└────────────────────────┬────────────────────────────────┘
                         │ capability decisions
                         ▼
┌─────────────────────────────────────────────────────────┐
│  Layer 2 · Signal Layer (ADR-0031)                      │
│  观察：发生了什么 / 治理信号产生                           │
│  产出：Alert · drift signal (S1/S3/S4) ·                │
│        FCoP-Rule-G1 (report ≠ governance)               │
└────────────────────────┬────────────────────────────────┘
                         │ governance signals
                         ▼
┌─────────────────────────────────────────────────────────┐
│  Layer 3 · Compiler Layer (ADR-0032)                    │
│  翻译：协议状态 → 结构化发现 + 整改建议                    │
│  产出：INSPECTION.md                                     │
│        = Structured Findings + Suggested Remediation    │
└─────────────────────────────────────────────────────────┘
                         │ structured documentation
                         ▼
              Human / Agent Decision
              (执行决策在 FCoP 之外)
```

---

## 二、逐层定义

### Layer 1 · Schema Layer（ADR-0030）

**核心问题**：这个行为，**能不能做**？

| 属性 | 值 |
|---|---|
| **ADR** | ADR-0030: Capability Governance Boundary |
| **输入** | Tool call（MCP 工具调用） |
| **输出** | `risk_level`: Safe / Sensitive / Critical |
| **机制** | MCP Interceptor `before_tool_call()` |
| **效果** | Safe → 放行 · Sensitive → 附加 Review · Critical → 阻断 |
| **性质** | **约束层**（防止行为发生） |

**关键原则**：
- 判断依据是 `Skill.tools[]` 中静态声明的 `risk_level`，不做动态 AI 判断
- Fail-open：未知 Skill 默认 `Safe`（治理不因配置缺失而误阻断）
- MCP 是唯一强制执行边界，Python SDK 是防绕过 fallback

---

### Layer 2 · Signal Layer（ADR-0031: GAL）

**核心问题**：**发生了什么**？治理视角是否出现？

| 属性 | 值 |
|---|---|
| **ADR** | ADR-0031: Governance Alert Layer |
| **输入** | 执行事件流 · 时间窗口 · 行为模式 |
| **输出** | Alert · Drift Signal |
| **机制** | 漂移信号检测（S1 solo-blindspot / S3 review-gap / S4 ...） |
| **效果** | 产生告警，推送给 ADMIN/PM |
| **性质** | **观察层**（让异常变得可见） |

**关键原则（FCoP-Rule-G1）**：
- `write_report()` / `fcop_report()` 属于 **Execution Domain**，不构成 Governance Signal
- Governance state 只能由独立机制修改（`write_review` / `mark_human_approved` / `fcop_check`）
- 防止"Agent 通过写报告骗过治理"

---

### Layer 3 · Compiler Layer（ADR-0032）

**核心问题**：协议状态和规范要求的差距，**该怎么理解和修**？

| 属性 | 值 |
|---|---|
| **ADR** | ADR-0032: fcop_audit() Protocol Inspection |
| **输入** | 项目文件系统（纯读） |
| **输出** | INSPECTION.md = Structured Findings + Suggested Remediation Plan |
| **机制** | 6 个 `scan_*()` 方法 + `InspectionReport.to_markdown()` |
| **效果** | 生成体检报告（带 Execution Block 建议命令） |
| **性质** | **编译层**（翻译协议状态为人可读行动认知） |

**内部三阶段**：

```
L3 内部流水线

Files  →  [L3-1 Detection]   →  Violation 列表
              scan_*()

       →  [L3-2 Interpretation] →  Structured Violation
              severity / impact

       →  [L3-3 Documentation]  →  INSPECTION.md
              to_markdown()         ├─ Structured Findings（客观事实）
                                    └─ Suggested Remediation Plan（建议）
```

**关键语义边界**：

> `INSPECTION` ≠ Remediation Plan  
> `INSPECTION` = Structured Findings + **Suggested** Remediation Plan

Execution Block 里的命令是**建议语义（suggestion）**，不是**执行语义（execution）**。`fcop_audit()` 不执行任何命令。

---

## 三、链式关系图（完整）

```
┌─────────────────────────────────────────────────────────────────┐
│                    FCoP Semantic Execution Chain                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ADR-0030 · Schema Layer                                        │
│  ┌────────────────────────────────────┐                         │
│  │ Skill.tools[] → risk_level        │                         │
│  │ MCP Interceptor before_tool_call  │ ← 唯一执行边界           │
│  │ Safe / Sensitive / Critical       │                         │
│  └────────────────┬───────────────────┘                         │
│                   │ allows / blocks / tags                      │
│                   ▼                                             │
│  ADR-0031 · Signal Layer                                        │
│  ┌────────────────────────────────────┐                         │
│  │ Drift detection (S1/S3/S4)        │                         │
│  │ GAL Alert generation              │ ← 治理可见性             │
│  │ FCoP-Rule-G1: report ≠ gov signal │                         │
│  └────────────────┬───────────────────┘                         │
│                   │ signals → ADMIN/PM                          │
│                   ▼                                             │
│  ADR-0032 · Compiler Layer                                      │
│  ┌────────────────────────────────────┐                         │
│  │ scan_*() → Violation              │                         │
│  │ InspectionReport.to_markdown()    │ ← 协议状态编译           │
│  │ INSPECTION.md                     │                         │
│  │  ├─ Structured Findings           │                         │
│  │  └─ Suggested Remediation Plan    │                         │
│  └────────────────┬───────────────────┘                         │
│                   │ documentation                               │
│                   ▼                                             │
│  Human / Agent Decision（执行在 FCoP 之外）                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 四、三层职责边界对照

| 维度 | Layer 1 (Schema) | Layer 2 (Signal) | Layer 3 (Compiler) |
|---|---|---|---|
| **核心问题** | 能不能做？ | 发生了什么？ | 差距怎么修？ |
| **工作时机** | 执行前（pre-execution） | 执行后（post-execution） | 按需（on-demand） |
| **触发方式** | 每次工具调用 | 持续观察 | 人工或 CI 触发 |
| **执行效果** | 阻断 / 放行 / 标记 | 告警 / 信号 | 生成文档 |
| **是否写盘** | ✅（事件日志） | ✅（Alert 记录） | ✅（INSPECTION.md 仅） |
| **是否执行命令** | ❌ | ❌ | ❌ |
| **性质** | 约束层 | 观察层 | 编译层 |

---

## 五、关键非目标（防止架构漂移）

FCoP 三层模型明确**不是**：

- ❌ **Orchestration Layer**：FCoP 不调度任何 agent 的工作
- ❌ **Remediation Engine**：三层均不自动执行整改命令
- ❌ **Security System**：漏洞扫描、密钥检测不在范围
- ❌ **Project Management System**：任务分配、进度管理不在范围

**防漂移硬约束**：

> 若未来出现"让 FCoP 自动执行整改"或"让 FCoP 调度 agent 工作"的需求，必须单独立新 ADR（如 `fcop_remediate()`），经 ADMIN 明确审批后才能实施。任何扩展都不得悄然改变现有三层的职责边界。

---

## 六、协议成熟度快照（2026-05-12）

| 层 | ADR | 状态 | 实现状态 |
|---|---|---|---|
| Schema Layer | ADR-0030 | ✅ Accepted | ✅ 已实现（risk_level · MCP interceptor · GAL drift signals） |
| Signal Layer | ADR-0031 | ✅ Accepted | ✅ 已实现（fcop_list_alerts · fcop_create_alert · S1/S3/S4） |
| Compiler Layer | ADR-0032 | ✅ Accepted | ✅ 已实现（fcop_audit · 6 scan_* · InspectionReport · INSPECTION.md） |

**下一步候选**（需独立 ADR）：
- `fcop_remediate(inspection_id)` — 按 INSPECTION 报告半自动执行 Tier 1 整改（需 ADMIN 二次确认）
- `INSPECTION-` 升格为 frozen 第 5 类 envelope — 让 inspection 进入 audit chain
- 三层模型对 Codeflow 的适配接口规范

---

## 七、参考

- `adr/ADR-0030-capability-governance-boundary.md`
- `adr/ADR-0031-governance-alert-layer.md`
- `adr/ADR-0032-fcop-audit-protocol-inspection.md`
- `src/fcop/inspection.py` — L3 数据类实现
- `src/fcop/project.py` — `Project.audit()` + `scan_*()` 实现
- `mcp/src/fcop_mcp/server.py` — `fcop_audit()` MCP 工具
