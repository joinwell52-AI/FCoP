# ADR-0030-bis: Capability Enforcement — Accountability Model

- **Status**: Accepted
- **Date**: 2026-05-11
- **Deciders**: ADMIN
- **Depends on**: [ADR-0030](./ADR-0030-capability-governance-boundary.md)（边界定义层）
- **Type**: Enforcement + Audit Model（How，执行层规范）
- **Related**: [ADR-0029](./ADR-0029-fcop-behavior-governance-charter.md), [ADR-0025](./ADR-0025-review-needs-human.md), [ADR-0026](./ADR-0026-review-human-approval.md)

---

## TL;DR

**ADR-0030 定义"什么是风险"（What），ADR-0030-bis 定义"风险如何被约束"（How）。**

FCoP 不是执行控制系统（execution gatekeeper）。
FCoP 是**行为可追责系统（accountability enforcement system）**。

```
核心原则：
  Governance without enforcement is advisory, not governance.
  FCoP does not prevent all execution paths.
  FCoP ensures all execution paths are accountable.
```

---

## Context

### 问题：ADR-0030 只有声明，没有执行

ADR-0030 定义了 Safe / Sensitive / Critical 三层分类和对应治理规则，但未定义这些规则如何在运行时被强制执行。结果：

- Critical 操作被协议"要求"人工审批
- 但 Agent 可以完全绕过 MCP，直接调用 shell / Python API / 外部服务
- 治理变成君子协定

### 关键澄清：什么是可实现的"不可绕过"？

**工程上不存在绝对封闭模型：**

```
FCoP 无法控制：
  OS / shell / Python runtime
  external MCP servers（非 fcop-mcp）
  LLM API 直接调用
  IDE 侧边效应
```

因此"所有 Agent 行为必须经过 FCoP"在工程上不成立。

**FCoP 真正能做到的：**

```
所有可观测行为必须进入 FCoP 可追责域。
```

**"不可绕过"的正确定义：**

```
❌ 错误：不可绕过 = 无法执行绕过路径
✔ 正确：不可绕过 = 绕过行为无法不留下证据

Bypass is Observable.（绕过即暴露）
```

这是 FCoP 治理能力的真实边界，也是与 OS kernel / container 安全系统的根本区别。
FCoP 对齐的是法律/审计类系统：不阻止犯罪，但确保犯罪留下证据、面临后果。

---

## Decision

### 一、双层执行模型（Dual-Layer Enforcement Model）

```
Tool Call
   ↓
┌────────────────────────────────────────────┐
│ Layer 1: MCP Interceptor                   │
│  ← 唯一的 intent-to-tool enforcement 边界  │
│  - 拦截 fcop-mcp 路径的工具调用             │
│  - Critical → 物理阻断                     │
│  - Sensitive → 注入 Review                 │
│  - Safe → 直接放行                         │
└────────────────────┬───────────────────────┘
                     │
┌────────────────────▼───────────────────────┐
│ Layer 2: Execution Domain                  │
│  ← 不可控现实层（FCoP 明确承认不控制此层） │
│  shell / Python / ext MCP / LLM API        │
└────────────────────┬───────────────────────┘
                     │
┌────────────────────▼───────────────────────┐
│ Layer 3: Post-hoc Audit                    │
│  ← 唯一的 uncontrolled path 观察者         │
│  fcop_check() / git diff                   │
│  Task graph reconciliation                 │
│  绕过 → 暴露给 ADMIN（不拦截，只发现）     │
└────────────────────────────────────────────┘
```

### 二、Layer 1 — MCP Interceptor（预防层）

**拦截点**：FastMCP middleware `before_tool_call(tool_name, args, context)`

**职责范围**：仅覆盖经过 `fcop-mcp` 的工具调用（不覆盖直接 Python API）

**执行逻辑**：

```python
1. 解析 tool_name → 查询 Skill.tools[] 元数据
2. 确定 risk_level（Safe / Sensitive / Critical）
3. 按 ADR-0030 策略执行：
```

| 风险层 | 执行动作 |
|--------|---------|
| **Safe** | 直接放行，无额外开销 |
| **Sensitive** | 自动创建 Review（`decision=pending`），可配置为允许执行或延迟 |
| **Critical** | **物理阻断**，返回 blocked 结构，生成 `approval_token` |

**Critical 阻断返回格式**：

```json
{
  "status": "blocked",
  "reason": "CRITICAL_RISK",
  "requires": "human_approval",
  "approval_token": "<generated_id>",
  "tool_name": "<tool>",
  "args_hash": "<sha256>",
  "session_id": "<session>",
  "expires_at": "<timestamp>"
}
```

**Skill 未声明时的默认策略**：

```
Missing Skill → Default = Safe（Fail-open）
```

理由：治理不因配置缺失而阻断正常使用；缺失配置由 audit 层发现。

### 三、Layer 2 — Execution Domain（不可控现实层）

FCoP **明确承认**此层不可控：

```
包括：
  直接 shell 执行
  Python runtime 直接调用
  非 fcop-mcp 的外部 MCP server
  任何非 FCoP 工具调用路径
```

**设计假设**：Agent 在执行层不可信（untrusted at execution layer）。

**FCoP 的响应不是阻止，而是观察**：Layer 3 负责发现此层的行为。

### 四、Layer 3 — Post-hoc Audit（审计补偿层）

**机制**：`fcop_check()` 扫描引擎

```
检查项：
  git diff vs Task 账本对照
  文件系统变更 vs open TASK-*.md 对照
  产物变更未关联任务链 → 标记为异常
```

**处置规则**：

| 场景 | 输出 |
|------|------|
| 变更在任务链路内 | OK，正常 |
| 变更无对应 TASK | 上报 ADMIN（列出具体文件） |
| Critical 操作痕迹但无 approval 记录 | 生成 ISSUE，强制要求说明 |

**核心保证**：绕过 MCP 的行为会在 `fcop_check()` 时被发现，记录在审计链，ADMIN 可见。

### 五、Approval Binding 机制（防止 approval 复用）

Approval token 必须绑定：

```yaml
tool_name: <exact tool>
args_hash: sha256(canonical_args)  # 参数精确绑定
session_id: <current session>      # 会话绑定
issued_at: <timestamp>
expires_at: <issued_at + window>   # 时间窗口，默认 30 分钟
used: false                        # 单次使用
```

**解锁流程**：

```
1. Critical 调用被阻断 → 生成 approval_token
2. ADMIN 执行 mark_human_approved(approval_token, ...)
3. 系统验证：hash 匹配 + session 匹配 + 未过期 + 未使用
4. 验证通过 → 原始调用重放
5. token 标记 used=true（不可复用）
```

### 六、MCP 层的信任边界定义

```
MCP layer   = the only intent-to-tool enforcement boundary（预防）
Audit layer = the only execution observer for uncontrolled paths（追责）
Python SDK  = 不独立作为 enforcement boundary
            （SDK 的 hook 辅助但不作为 trust boundary）
```

> **MCP is the only intent-to-tool enforcement boundary, but not the only execution observer.**
>
> 这两个角色不是优先级之分，而是职责分离：
> MCP 负责"工具调用意图的拦截"，Audit 负责"所有执行路径的观察"。
> 不存在"次级 enforcement boundary"——MCP 之外没有任何路径会被拦截，只会被发现。

**明确不做的**：

- ❌ 不依赖 monkey-patch 作为安全机制
- ❌ 不允许隐式 approval 复用
- ❌ 不在 MCP Interceptor 之外做 governance decision
- ❌ 不承诺在 OS / shell 层面物理阻止绕过

---

## Summary

### 核心转变

| 维度 | 旧假设（错误） | ADR-0030-bis（正确） |
|------|--------------|-------------------|
| 目标 | 控制所有执行路径 | 确保所有行为可追责 |
| 不可绕过的定义 | 物理上无法绕过 | 绕过即暴露（Bypass is Observable） |
| 执行模型 | 单一拦截器 | 预防 + 不可控现实 + 审计补偿 |
| 对 Agent 的假设 | 可信 | 执行层不可信 |
| 类比对象 | OS kernel | 法律 + 审计系统 |

### 一句话

> **ADR-0030-bis 将 FCoP 从"可描述的治理系统"升级为"不可抵赖的治理系统"。**
> 它不阻止所有绕过，但确保所有绕过都留下证据。

---

## Implementation Spec（Layer 1 MVP）

### 核心定性

> **FastMCP Layer 1 is not a firewall.**
> **It is a decision trace generator for execution governance.**

它不是安全系统、权限系统、AI 判断系统。它是：

```
Execution Trace Generator + Deterministic Policy Gate
```

### 成功标志（重要）

Layer 1 成功的判断标准**不是**"能拦截 Critical"，而是：

> **任何 Critical 操作都必须留下结构化痕迹。**
> 记录优先于阻断（Audit-first over enforcement-first）。

### SAL（语义层）归位结论

讨论过程中出现的"语义层（SAL）"不应成为独立 runtime layer。结论：

```
SAL 已内化为 Skill schema 的语义字段。
不需要独立 SAL → PAL → RAL 的运行时分层。
```

最终架构：

```
[ Skill Schema ]        ← 语义定义（SAL 内化于此）
       ↓
[ MCP Interceptor ]     ← Layer 1 唯一入口
       ↓
[ Execution Domain ]    ← 不可信现实层
       ↓
[ Audit Layer ]         ← Layer 3 fcop_check
```

### 四个 MVP 组件

**实现顺序（严格按此）：**

```
Step 1: Skill Resolver    — tool_name → risk_level（最小函数，先跑通）
Step 2: Policy Engine     — ADR-0030 pure mapping（纯表驱动，无逻辑）
Step 3: Interceptor stub  — before_tool_call（先 log 不拦截，验证管道）
Step 4: Block / Review    — 加入阻断和 Review 注入
Step 5: Approval token    — Critical 解锁机制
```

**组件 1：Skill Resolver**

```
input:  tool_name
output: risk_level + metadata
policy: Missing Skill → Safe（fail-open，治理不因配置缺失而阻断）
```

**组件 2：Policy Engine（纯 deterministic，禁止 AI 判断）**

```python
# ✔ 正确（deterministic lookup）
risk = SkillRegistry.lookup(tool_name)
apply_policy(risk)

# ❌ 错误（禁止）
if model.thinks_risky():
    block()
```

```
Safe     → ALLOW
Sensitive → REVIEW（注入 Review，可配置是否延迟执行）
Critical  → BLOCK + 生成 approval_token
```

**组件 3：Interceptor Hook（`before_tool_call`）**

三件事，顺序不可变：
1. Resolve（解析 Skill → risk_level）
2. Decide（policy mapping → ALLOW / REVIEW / BLOCK）
3. Emit（**必须先于执行决策写入审计事件流**）

**组件 4：Event Logger（append-only，审计链核心）**

```json
{
  "type": "tool_call_intercept",
  "tool": "<tool_name>",
  "risk": "Critical",
  "decision": "BLOCK",
  "args_hash": "<sha256>",
  "approval_token": "<token_id>",
  "session_id": "<session>",
  "timestamp": 1234567890.0
}
```

> 事件必须 append-only 写入。没有此事件，Layer 3 Audit 无从核查。

### Approval Token 规格

```yaml
tool_name: <exact tool>
args_hash: sha256(canonical_json(args))   # 参数精确绑定，防止复用
session_id: <current session>              # 会话绑定
issued_at: <unix timestamp>
expires_at: issued_at + 1800              # 默认 30 分钟
used: false                               # 单次使用，验证后立即标记
```

## Consequences

### 对实现的影响

| 模块 | 新增工作 |
|------|---------|
| `fcop-mcp` | 实现 FastMCP `before_tool_call` 中间件 + Critical 阻断逻辑 |
| `fcop` Python 库 | `approval_token` 生成、存储、校验、单次使用标记 |
| `fcop_check()` | 新增 Task graph reconciliation + Critical 痕迹检测 |
| `mark_human_approved` | 扩展：支持 `approval_token` 绑定校验 |
| `Skill.tools[]` | 已有（ADR-0027），作为 risk resolution 的 source of truth |

### 对 ADR-0028 的影响

ADR-0028（自动风险评估）须修订：

- 自动推断逻辑迁入 MCP Interceptor（Layer 1），不放在 `write_task()`
- `write_task()` 保持纯净（Optional coordination primitive）
- ADR-0028 v2 = "Skill.tools[] → risk_level 推断算法"，作为 Layer 1 的子模块

### 对协议承诺的影响

FCoP 正式确立：

> **FCoP is not an execution gatekeeper.**
> **FCoP is an accountability enforcement system.**

此定位写入协议核心文档（ADR-0029 + spec），防止未来实现层再次向"全控制"幻想漂移。
