# ADR-0031: Governance Alert Layer (GAL)

| 字段 | 值 |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-05-11 |
| **Depends on** | ADR-0029（行为治理协议）, ADR-0030-bis（Capability Enforcement） |
| **Type** | Protocol Extension — Observability |

---

## 1. 背景（Motivating Example）

**实战案例 #24（2026-05-11）**：

> PM-01 自评：QA 缺位 ~8 小时（结构性 — 心智模型缺失）。  
> v0.3.0-alpha 含 8 个 commit，无独立 Review，无治理确认，若无 ADMIN 第二次介入，将以「无 QA sign-off」状态进入 5/12。  
> ——"没有这一问，代价更大。"

**根因不是 QA 缺席**，而是：

> **高影响行为长时间缺少独立治理确认，且 ADMIN 未被及时提醒。**

"治理存在" ≠ "ADMIN 能感知"。两者之间的断层，就是 GAL 要填补的。

---

## 2. 决策

引入 **Governance Alert Layer（GAL）**，作为 FCoP 的第四支柱。

### 核心原则

> **Potential governance gaps must become ADMIN-visible within SLA.**  
> （潜在治理缺口必须在 SLA 内进入 ADMIN 可见域）

GAL 的唯一职责是**升级（escalation）**，不做：

- ❌ 判断架构对错
- ❌ 阻止开发执行
- ❌ 指挥 Agent 行为
- ❌ 替 ADMIN 做治理决策
- ❌ 自动修复治理缺口

GAL 只做：

- ✅ 检测治理漂移信号
- ✅ 写入结构化 ALERT 文件
- ✅ 让 ADMIN 无需巡逻即可感知异常

---

## 3. 四大漂移信号（Governance Drift Signals）

### Signal 1 — `missing_independent_verdict`（独立治理视角缺失）

```yaml
trigger: high_impact_action_completed
  # 包括：milestone 推进 / release 标记 / CRITICAL_TAG 工具调用
condition:
  no_review_from_different_actor: true
  duration_threshold: 2h
severity: high
```

**案例 #24** 命中此信号：8 小时内连续开发，无第二视角 Review。

### Signal 2 — `commit_flood_without_governance`（大量行为无治理记录）

```yaml
trigger: governance_event_count
condition:
  actions_by_same_actor: ">= 5"
  governance_events_in_window: 0
  window: 4h
severity: medium
```

### Signal 3 — `critical_tool_unreviewed`（Critical 工具调用无配套 Review）

```yaml
trigger: tool_call_tag == "CRITICAL_TAG"
condition:
  no_corresponding_review: true
  within: 1h
severity: high
```

数据来源：`fcop_events.jsonl`（ADR-0030-bis Layer 1 审计日志）。

### Signal 4 — `long_running_without_reconciliation`（长时间未对账）

```yaml
trigger: open_task_age
condition:
  age: "> 24h"
  no_report_filed: true
severity: low
```

---

## 4. Alert 文件格式

**路径**：`fcop/alerts/ALERT-{YYYYMMDD}-{NNN}.md`

```yaml
---
alert_id: ALERT-20260511-001
severity: high          # high / medium / low
type: missing_independent_verdict
status: open            # open / acknowledged / resolved
created_at: "2026-05-11T11:42:00+08:00"
---

## 治理缺口摘要

- **影响范围**：v0.3.0-alpha（8 commits）
- **缺口持续时长**：8h 12m
- **触发信号**：no independent review path detected
- **相关事件**：fcop_events.jsonl（CRITICAL_TAG × 3）

## 建议关注

ADMIN review recommended before merge / release.
```

**设计约束**：

- 文件只增不改（append-only，同 `fcop_events.jsonl`）
- `status: open` 由 GAL 写入；`acknowledged` / `resolved` 由 ADMIN 手动更新
- 文件名即优先级入口：ADMIN 扫一眼目录即知有多少未处理告警

---

## 5. FCoP 工具层

新增 2 个 MCP 工具（`fcop-mcp 1.3.0`）：

| 工具 | 职责 |
|---|---|
| `list_alerts` | 读取 `fcop/alerts/` 下所有 ALERT 文件；支持按 severity / status 过滤；ADMIN 的「告警收件箱」 |
| `create_alert` | 由 `fcop_check()` 内部调用，检测到漂移信号后写入新 ALERT 文件；Agent 不得直接调用 |

`fcop_check()` 在 Layer 3 Audit 环节新增漂移信号扫描，命中即调用 `create_alert`，输出摘要标注 `⚠ GAL:` 前缀。

---

## 6. 浮现机制（Surfacing）

GAL 的有效性取决于 ADMIN **无需主动巡检**即能感知：

```
fcop_check() 检测到漂移
        ↓
写入 fcop/alerts/ALERT-*.md
        ↓
CodeFlow PWA 首页 → ⚠ Governance Alerts: N
手机 Push → "Governance drift detected"
ADMIN Dashboard 红点 → Governance Inbox (N)
```

FCoP 协议层职责止于写入 ALERT 文件；**浮现渠道（PWA / Push / Dashboard）由 CodeFlow 应用层实现**，不在本 ADR 范围内。

---

## 7. 与既有层级的关系

```
Capability Governance (ADR-0030-bis, Layer 1)
        ↓  fcop_events.jsonl（行为账本）
Review / Report（行为审计）
        ↓
GAL — 治理缺口检测（本 ADR）
        ↓  fcop/alerts/ALERT-*.md
ADMIN 可见域
```

GAL 是 **协议自监控层（Protocol Self-Monitor）**，消费 Capability 层的审计日志 + Review/Task 文件系统，输出告警文件，不产生新的执行约束。

---

## 8. Solo Blindspot 信号的域模型实现

基于 §9.2 FCoP-Rule-G1，Solo Blindspot 的触发逻辑为：

```python
# 执行窗口计时：仅 execution_domain 事件推进窗口
# 治理窗口重置：governance_domain 事件（任意来源）重置计时

for event in chronological_events:
    if event.domain == "execution":
        exec_window_start = exec_window_start or event.ts
    elif event.domain == "governance":
        exec_window_start = None          # 独立治理视角出现，窗口重置
    
    if exec_window_start:
        gap = event.ts - exec_window_start
        if gap > threshold:
            emit_alert(type="solo_blindspot", duration=gap)
```

**关键**：`domain == "governance"` 的来源不限 Actor。
任何独立治理事件（包括 ADMIN 发起的 `fcop_check`）均可重置窗口。

## 9. 反目标（Non-Goals）

GAL 明确不做：

- ❌ Governance Brain（AI 决策治理）
- ❌ Autonomous Compliance Engine
- ❌ QA Role Replacement
- ❌ Blocking execution on alert
- ❌ Auto-resolving alerts

---

## 9. 三域模型与 FCoP-Rule-G1（核心公理）

### 9.1 三域严格定义

GAL 的漂移信号依赖对所有工具调用的**域（Domain）**分类。三个域的边界如下：

#### ① Execution Domain（执行域）

```
工具示例：write_task, write_report, fcop_report, archive_task,
          delete_task, log_event, write_issue
特征：
  - self-generated：由执行 Actor 自身产生
  - self-contained：信息源与执行源相同
  - non-verifying：不对行为形成外部验证
  - non-blocking：不阻止或改变后续执行
作用：记录行为，不约束行为
```

#### ② Governance Domain（治理域）

```
工具示例：write_review, mark_human_approved, fcop_check
特征：
  - cross-actor OR cross-time OR cross-system validation
  - 引入约束或决策边界（constraint / decision boundary）
  - 可能阻止或改变执行（may block execution）
作用：改变行为是否允许发生
```

#### ③ Enforcement Domain（强制域）

```
机制：FCoPGovernanceMiddleware.on_call_tool, MCP interceptor
特征：
  - runtime hook，pre-execution
  - physical interception
  - 决策权在 MCP Interceptor，不在 Agent（ADR-0030 §四）
作用：物理拦截（v1.x 为审计，v2.x 可强制阻断）
```

### 9.2 FCoP-Rule-G1（协议级公理）

> **Self-reported information ≠ governance signal.**

形式化规则：

```
write_report / fcop_report ∈ Execution Domain
write_report / fcop_report ∉ Governance Domain
write_report / fcop_report CANNOT reset governance state
```

**具体含义**：

- ❌ 禁止：`report` 被视为 Solo Blindspot 窗口的重置条件
- ❌ 禁止：`report` 被视为"治理完成"的证据
- ❌ 禁止：`report` 替代 `review` / `fcop_check`
- ✅ 允许：`report` 提供 audit trace（执行痕迹）
- ✅ 允许：`report` 支持后验分析的上下文

**为什么这是公理级约束**：

如果 `report` 算作治理事件，Agent 可以通过"持续自我报告"绕过治理要求，
GAL 的 Solo Blindspot 信号会被自我叙述污染成假治理信号。
FCoP 的治理有效性从根本上依赖"独立性（independence）"，
而 `report` 本质是**同一 Actor、同一上下文、同一信息源**的自述，
无法满足独立性的最低要求。

**ADR-level statement（可被下游系统直接引用）**：

> `write_report` / `fcop_report` belongs to **Execution Domain**.
> It is a self-generated trace artifact and does **not** constitute a governance signal.
> Governance state can only be modified by independent or enforcing mechanisms:
> `write_review` / `mark_human_approved` / `fcop_check` / MCP interceptor.

---

## 11. 成功标准

> 任何持续超过 SLA 阈值的治理漂移，必须在 ADMIN 下次打开工作台时**已存在对应 ALERT 文件**。

不需要：ADMIN 记得去看。  
需要：系统把异常送到 ADMIN 面前。

---

## 10. 一句话定性

> GAL 不治理行为，它让治理断层**自己发光**。
