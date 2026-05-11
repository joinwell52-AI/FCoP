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
┌────────────────────────────────┐
│ Layer 1: MCP Interceptor       │  ← 预防层（Preventive）
│  - 拦截 fcop-mcp 路径的工具调用 │
│  - Critical → 物理阻断          │
│  - Sensitive → 注入 Review      │
│  - Safe → 直接放行              │
└────────────────┬───────────────┘
                 │
┌────────────────▼───────────────┐
│ Layer 2: Execution Domain      │  ← 不可控现实层（Uncontrolled Reality）
│  shell / Python / ext MCP /    │
│  LLM API / IDE effects         │
│  ← FCoP 不控制，但可以观察      │
└────────────────┬───────────────┘
                 │
┌────────────────▼───────────────┐
│ Layer 3: Post-hoc Audit        │  ← 审计补偿层（Accountability）
│  fcop_check() / git diff       │
│  Task graph reconciliation     │
│  绕过 → 暴露给 ADMIN            │
└────────────────────────────────┘
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
MCP layer  = primary enforcement point（预防）
Audit layer = secondary accountability point（追责）
Python SDK = 不独立作为 enforcement boundary
           （SDK 的 hook 辅助但不作为 trust boundary）
```

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
