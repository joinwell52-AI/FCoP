# NOTE: Custody Is Not a Protocol Layer
## Semantic Note · Custody Is an Interpretation, Not a Truth

| 字段 | 值 |
|---|---|
| **Type** | Semantic Note（非 ADR，不参与协议版本）|
| **Date** | 2026-05-21 |
| **Supersedes** | ADR-0037（原 Custody & Handoff Semantics · 已删除）|
| **Status** | Informative only |
| **Related** | ADR-0035（State）、ADR-0036（Event）、ADR-0038（Boundary）|

---

## Decision

> **Custody 不是协议层。**  
> **Custody is not a protocol layer.**

原计划中的 ADR-0037（Custody & Handoff Semantics）在 RFC 评审中被否决。  
原因：custody 一旦成为独立层，就会立即变成"第三套真相系统"——违反 ADR-0035 Rule A（path = state truth）与 ADR-0036 Rule G（events = audit-only）。

本文件保留 custody **思想**作为解释性注释，但**取消其协议层级地位**。

---

## What Custody IS

> Custody is an **emergent interpretation** of file ownership derived from:
> - **file location** (current state, per ADR-0035)
> - **event history** (transitions, per ADR-0036)
>
> It is **not stored, not authoritative, and not part of the protocol state model.**

中文：

> Custody（持有权）是一种**衍生解释**——它通过观察文件位置和事件历史**被推导出来**，而不是被独立记录。  
> 它**不落盘、不权威、不属于协议状态模型**。

---

## Why Custody Cannot Be a Layer

| 风险 | 后果 |
|------|------|
| custody 作为独立 truth | 系统出现"3 套真相"（state / event / custody）→ 永远存在不一致风险 |
| custody 作为字段 | 协议表面膨胀，从 coordination protocol 滑向 ownership system |
| custody 作为 layer | 必然引入 permission / scheduling / handoff workflow → OS drift |
| custody 作为 enforce | 违反 ADR-0038 §1 原则 1（describes, not executes）|

**Custody 一旦层级化，FCoP 就会从 protocol 退化为 Agent OS。**

---

## How to Read Custody (Without Storing It)

当需要回答"现在这个文件归谁"时，按以下规则推导：

| 文件所在位置 | 推导出的 custodian |
|------------|-------------------|
| `_lifecycle/inbox/` | none（无人持有，等待 claim）|
| `_lifecycle/active/` | 最后一次 `to: active` 事件的 `by` 字段 |
| `_lifecycle/review/` | none（任何合规 reviewer 可接手）|
| `_lifecycle/done/` | 最后一次进入 active 的 `by`（作为审计记录）|
| `_lifecycle/archive/` | 同上 |

这是**读取规则，不是协议规则**——runtime / tool / audit 可以按需实现，但**协议本体不承认 custody 字段的存在**。

---

## What Happens to Handoff?

> Handoff 不是协议原语。它是一次普通的 transition 事件序列：
>
> 1. 当前持有者调用 `release_task` → 产生 `to: <some-stage>, by: A` 事件
> 2. 下一个接手者调用 `claim_task` → 产生 `to: active, by: B` 事件
>
> 协议只看到两条事件，没有"handoff"这个原语。

如果 runtime 需要表达"A 把任务交给 B"的协调意图，应该用 L2 协调工具（如 `notify_agent`），**不进入 L1 lifecycle topology**。

---

## Position in the FCoP Stack

```
ADR-0038 · Boundary Charter（meta · 防 OS 化）
    ↓
ADR-0035 · State (path = NOW truth)         ← 唯一 NOW 真相
ADR-0036 · Event (transitions = PAST trace) ← 唯一 PAST 真相
    ↓
NOTE · Custody = interpretation             ← 仅注释，无层级
```

---

## Canonical One-Liner（two-layer per ADR-0040）

**Layer 1 · Cognitive bootstrap**

> **Files carry protocol. Paths address state. Events replay transitions.**
> **文件即协议；位置定义状态；事件记录历史。**

**Layer 2 · Semantic ontology**

> **Files externalize protocol semantics. Paths address state. Events are replayable evidence of state transitions.**
> **文件是协议的外化载体；位置是状态的地址映射；事件是状态转移的可重放证据。**

Custody 不在两层中的任何一层 —— 它是从位置 + 事件**派生出来的解释**，不是协议字段。这就是 ADR-0037 被拒绝的根本原因。

*(Historical / v1 epigraph: "file location is truth; everything else is trace." — see ADR-0040 for why this single line was split into two layers.)*

---

## 历史背景

ADR-0037 曾经存在（2026-05-21 同日提案），定义了独立的 `custodian` 字段、`custody_history` 数组、`handoff_task` / `release_task` 工具。RFC 评审认定该层级会引入"第三套真相系统"，与协议核心承诺冲突，**未进入 Accepted 即被作废**，思想以本 NOTE 形式保留。

---

*2026-05-21 · Semantic Note · Custody-as-Interpretation · Not a Protocol Layer*
