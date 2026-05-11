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

### 四、MCP 拦截行为

v1.x 阶段（库模式，无 sidecar）：

```
拦截点：在调用 MCP 工具前，Agent 查询 fcop.json Skill.tools[]
行为：
  - Critical 工具 → 先 write_review(needs_human) → 等批准 → 再调用
  - Sensitive 工具 → 先 write_review() → 审阅通过 → 再调用
  - Safe 工具 → 直接调用，write_report() 留存记录

遵从原则：Agent 自觉遵守（协议约束，非系统强制）
违规处理：通过 review / audit 事后发现，不做实时强制拦截
```

v2.x 阶段（独立 runtime 进程）可实现真正的系统强制拦截，超出当前规范范围。

### 五、approval trigger 条件总结

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
- **可执行**：Agent 自查 `fcop.json Skill.tools[]` 即可判断层级，无需外部服务
- **可审计**：所有 Sensitive / Critical 操作都有 review 记录，满足基本合规要求
- **可扩展**：v2.x 可在此分类体系上加 sidecar 强制执行，无需重新设计分类

---

## 一句话

> **FCoP capability governance = 工具调用风险边界。三层，够了。**
