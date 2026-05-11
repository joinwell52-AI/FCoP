# ADR-0030: Capability Governance Boundary — 工具调用风险边界

- **Status**: Accepted
- **Date**: 2026-05-11
- **Deciders**: ADMIN
- **Related**: [ADR-0029](./ADR-0029-fcop-behavior-governance-charter.md), [ADR-0027](./ADR-0027-skill-tools-risk-metadata.md), [ADR-0025](./ADR-0025-review-needs-human.md)

## TL;DR

**中文**：FCoP Capability Governance = 工具调用风险边界。将 MCP 工具分为三层：Safe（默认允许）/ Sensitive（需要 review）/ Critical（需要人工审批）。治理的对象是**行为风险**，不是身份等级。FCoP 不构建企业 IAM、不定义角色权限树、不处理业务策略。

**English**: FCoP Capability Governance = tool-call risk boundary. Three tiers: Safe (allow by default) / Sensitive (review required) / Critical (human approval required). Governance targets **behavioral risk**, not identity level. FCoP does not build enterprise IAM, role hierarchies, or business policy engines.

---

## Context

### 问题：capability governance 的边界在哪里？

ADR-0029 确立了"行为治理协议"的定位，capability governance 是其执行层。但不明确边界，就会膨胀成：

- Enterprise IAM（身份访问管理）
- RBAC Platform（角色权限平台）
- 业务流程审批系统
- ERP 权限树

这些都超出 FCoP 的职责范围，也超出 SME 的复杂度预算。

### 关键边界澄清

**FCoP 治理的是：**
```yaml
工具能力边界（Tool-level capability）

示例：
  allowed_tools: [read_file, write_file, playwright]
  restricted_tools: [deploy_production, delete_database]
```

**FCoP 不治理的是：**
```
业务行为策略（Business policy）

示例（超出范围）：
  谁可以审批订单
  哪个员工能看客户资料
  财务流程规则
  ERP 权限树
```

**Agent 不是员工。** capability governance 不基于身份等级（senior_agent / junior_agent），而是基于工具调用的**行为风险**。

---

## Decision

### 一、能力分类体系（Capability Taxonomy）

三层，不再细化：

#### Layer 1 — Safe（安全，默认允许）

| 特征 | 只读或低影响，无需审批 |
|------|----------------------|
| **典型工具** | `read_file` · `search_code` · `grep` · `git.status` · `git.diff` · `list_directory` · `web_search` |
| **风险等级** | `low` |
| **治理行为** | 直接执行，写入 report 留存记录 |

#### Layer 2 — Sensitive（敏感，需要 review）

| 特征 | 写操作或有副作用，需要至少一个 Agent 审阅 |
|------|------------------------------------------|
| **典型工具** | `write_file` · `execute_shell` · `git.commit` · `git.push` · `create_branch` · `send_email` |
| **风险等级** | `medium` / `high` |
| **治理行为** | 触发 `write_review(decision=needs_review)`；审阅通过后执行 |

#### Layer 3 — Critical（关键，需要人工审批）

| 特征 | 不可逆或高影响，必须人类签字 |
|------|------------------------------|
| **典型工具** | `deploy_production` · `delete_database` · `payment_transfer` · `git.push_force` · `drop_table` · `revoke_access` |
| **风险等级** | `irreversible` |
| **治理行为** | 触发 `write_review(decision=needs_human)`；等待 `mark_human_approved()` 后才执行 |

### 二、分类的依据：行为风险，不是身份等级

```
✔ 问的问题：
  "这个工具调用，如果出错或被滥用，后果有多严重？"

✔ 正确分类维度：
  - 是否可撤销（irreversible）
  - 影响范围（本地 / 团队 / 生产环境 / 外部系统）
  - 是否产生计费（cost_sensitive）

✗ 错误分类维度：
  - "高级 Agent 才能调用"
  - "PM 角色才有权限"
  - "需要二级审批"（这是业务流程，不是能力边界）
```

### 三、与 Skill.tools[] 的关系

ADR-0027 已定义 `Skill.tools[]` 的元数据结构（`risk_level` / `irreversible` / `cost_sensitive`）。本 ADR 在其上定义治理行为的映射：

```
Skill.tools[].risk_level    →  Capability Tier  →  Governance Action
─────────────────────────────────────────────────────────────────────
low                         →  Safe             →  直接执行 + report
medium                      →  Sensitive        →  write_review(needs_review)
high                        →  Sensitive        →  write_review(needs_review)
irreversible                →  Critical         →  write_review(needs_human)

Skill.tools[].irreversible = true  →  强制 Critical，无论 risk_level
Skill.tools[].cost_sensitive = true →  Sensitive（最低），可配置升为 Critical
```

### 四、Authority Rule（权责归宿原则）

**Capability classification MUST NOT be resolved within the Agent execution layer.**

这是 ADR-0030 最核心的约束，防止 governance 退化为 lint system：

```
❌ 危险模型（Agent 自主判断）：
  Agent → 读 Skill.tools[] → 自行判断 risk → 自行决定执行
  问题：等于"自己给自己放行"，governance 形同虚设

✔ 正确模型（MCP Interceptor 裁定）：
  Agent → 提交工具调用意图
          ↓
  MCP Interceptor（受信任的运行时边界）
          ↓
  Skill Resolver（查询 Skill.tools[]）
          ↓
  决策：allow / review_tag / critical_tag
```

**Agent 可以做：**
- 提出工具调用（propose tool calls）
- 提供上下文（provide context for risk evaluation）

**Agent 不可以做：**
- 最终确定 capability tier 分类
- 覆盖 Skill.tools[] 派生的 risk resolution
- 对 Critical 操作自我授权

**权威决策边界：**
- v1.x：MCP Interceptor 层（`FCoPGovernanceMiddleware`）
- v2.x：等效的受信任运行时边界（独立进程 / sidecar）

> 三层分类（Safe / Sensitive / Critical）是分类结构，不是决策结构。
> 决策权在 MCP Interceptor，不在 Agent。

### 五、MCP 拦截行为

v1.x 阶段（库模式，`FCoPGovernanceMiddleware`）：

```
拦截点：on_call_tool hook（Agent 提交意图后，工具实际执行前）
决策者：MCP Interceptor（受信任边界），不是 Agent

行为：
  - Safe 工具     → 写入审计事件（ALLOW tag）→ 执行
  - Sensitive 工具 → 写入审计事件（REVIEW_TAG）→ 执行（行为可见）
  - Critical 工具  → 写入审计事件（CRITICAL_TAG）→ 执行（强制留痕）

v1.x 定位：审计优先（audit-first），记录是强制的，阻断是可选的
违规追责：通过 fcop_events.jsonl + fcop_check() 事后发现
```

v2.x 阶段（独立 runtime 进程）可在此基础上加入系统级强制阻断，超出当前规范范围。

### 六、approval trigger 条件总结

| 触发条件 | Governance Action |
|----------|------------------|
| `risk_level = irreversible` | `needs_human`，阻塞直到 `mark_human_approved()` |
| `irreversible = true` | 同上，强制 |
| `risk_level = high` | `needs_review`，至少一个 reviewer 通过 |
| `cost_sensitive = true` + 超过费用阈值 | `needs_human`（可配置） |
| `risk_level = medium` | `needs_review`（推荐），可配置为 `allow` |
| `risk_level = low` | 直接允许 |

---

## Non-Goals（明确不做）

- ❌ 构建 Enterprise IAM / RBAC 系统
- ❌ 定义 Agent 角色等级（senior / junior / admin）
- ❌ 处理业务流程审批（订单审批、财务权限）
- ❌ 实现 v2.x sidecar 强制拦截（留待独立 ADR）
- ❌ 细化超过三层的能力分类（防止权限系统地狱）

---

## Consequences

- **够用**：三层分类覆盖 SME 99% 的风险治理需求
- **轻量**：不引入 IAM / RBAC 复杂度
- **可执行**：MCP Interceptor 查询 `Skill.tools[]` 做权威裁定，Agent 仅提交意图
- **可审计**：所有工具调用都留有结构化事件，Sensitive / Critical 强制可见
- **可扩展**：v2.x 可在此分类体系上加 sidecar 强制阻断，无需重新设计分类
- **权责清晰**：Authority Rule 确保决策权在受信任边界，而非 Agent 执行层

---

## 一句话

> **FCoP capability governance = 工具调用风险边界。三层，够了。**
> **决策权在 MCP Interceptor，不在 Agent——这是治理系统与建议系统的分水岭。**
