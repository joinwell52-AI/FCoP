# ADR-0028: 自动风险评估 — write_task() 风险推断与传导机制

- **Status**: Proposed — Pending Revision（见 ADR-0029：治理逻辑须迁出 write_task()）
- **Date**: 2026-05-11
- **Deciders**: ADMIN
- **Related**: [ADR-0024](./ADR-0024-task-risk-level.md), [ADR-0025](./ADR-0025-review-needs-human.md), [ADR-0026](./ADR-0026-review-human-approval.md), [ADR-0027](./ADR-0027-skill-tools-risk-metadata.md)

## TL;DR

**中文**：v1.2 在 `write_task()` 内部引入自动风险评估层：基于 `tools_hint`（Agent 声明的工具列表）查询 `Skill.tools[]` 元数据，自动推断并写入 `Task.risk_level`。系统推断值是下限——Agent 可加严但不可降低。风险拦截不抛异常，而是返回 `blocked=True` + `risk_assessment` 结构，通过事件系统向 PM 传导。

**English**: v1.2 adds an auto-assessment layer inside `write_task()`: infers `Task.risk_level` from `tools_hint` (caller-declared tool list) against `Skill.tools[]` metadata. System-inferred value is a floor — callers can raise it, never lower it. Risk blocking does not raise exceptions; instead it returns `blocked=True` + a `risk_assessment` struct and emits an event to notify PM.

---

## Context

### 问题：v1.1 的风险评估完全依赖调用者自律

v1.1 引入了 `Task.risk_level`（ADR-0024）和 `Skill.tools[]`（ADR-0027），但两者之间**没有自动关联**——`write_task()` 不读取 `Skill.tools[]`，完全依赖 Agent 手动填写 `risk_level`。

这产生三个漏洞：

1. **漏填**：Agent 忘记填 `risk_level`，默认值 `medium` 可能低于实际风险
2. **低填**：Agent 主观认为风险低（或故意降低）以绕过审批
3. **无溯源**：即使填了，也不知道为什么填这个值

### 目标

- 基于已有的 `Skill.tools[]` 元数据自动推断风险等级
- 系统推断值作为不可降低的下限
- 风险拦截产生可审计记录（不是沉默地丢弃任务）
- 风险信号及时传导给 Agent 和 PM，不依赖轮询

---

## Decision

### 一、新增 `tools_hint` 参数

```python
proj.write_task(
    sender="DEV", recipient="DEV",
    priority="P1",
    subject="清理测试数据",
    body="删除 test_* 表的所有记录",
    tools_hint=["db.delete", "db.query"],   # ← v1.2 新增，可选
    # risk_level 不填 → 系统自动推断
    # risk_level 填了 → 与系统推断值取最高
)
```

`tools_hint` 是 Agent 向协议层声明"我打算调用哪些工具"的唯一渠道。协议不强制要求填写，但不填则无法触发基于工具的自动评估（退化到关键词规则层）。

### 二、风险推断优先级（三层叠加取最高值）

```
Layer 1  工具溯源（最高可信度）
         tools_hint 中每个工具 → 查 fcop.json Skill.tools[]
         → 取所有匹配工具的 risk_level 最高值

         示例：tools_hint=["db.query","db.delete"]
               db.query  → low
               db.delete → high, irreversible=true
               推断结果  → irreversible

Layer 2  关键词规则（兜底）
         扫描 task.subject + task.body
         命中预置模式 → 风险等级对应提升

         示例规则：
           irreversible: drop table / truncate / force.?push / 不可恢复
           high:         delete / remove / modify.*schema / 删除 / 修改.*数据库
           medium:       update / patch / 修改

Layer 3  Agent 手动填写（加严通道）
         Agent 填写的 risk_level ≥ 系统推断值 → 采用 Agent 值
         Agent 填写的 risk_level <  系统推断值 → 忽略，保留系统值
                                                  写入 auto_assessed_override=true 标记
```

### 三、覆盖权限与 Agent.layer

```
Agent.layer = "PM"       → 可以降低推断值（有完整上下文的治理角色）
Agent.layer = "executor" → 只能加严，不能降低（默认所有非 PM 角色）
Agent.layer 未设置       → 等同于 executor
```

PM 降低风险等级时，必须附带 `override_reason` 字段，写入审计日志。

### 四、write_task() 永不因风险而抛异常

```
协议违规（非法输入、角色不存在）→ 抛异常   → 任务没有写入
风险拦截（irreversible / high）  → 成功返回 → 任务写入，状态=blocked
```

**理由**：被拦截的任务本身是有价值的审计记录。审计日志应能回答：
"Agent 在什么时间尝试了什么操作，为什么被拦截，最终谁批准了。"
任务不写入 = 这段历史消失 = 违背 FCoP 可追溯原则。

### 五、返回值新增 risk_assessment 结构

```python
@dataclass
class RiskAssessment:
    auto_risk_level: RiskLevel          # 系统推断的风险等级
    final_risk_level: RiskLevel         # 实际写入 Task 的风险等级
    triggered_by: list[str]             # 触发风险升级的工具或关键词
    assessment_layers: list[str]        # 经过了哪些评估层
    blocked: bool                       # 是否触发 needs_human
    override_by_agent: bool             # Agent 手动填写是否生效
    auto_assessed_override: bool        # Agent 试图降低但被系统拒绝

# write_task() 返回值
@dataclass
class TaskWriteResult:
    task: Task
    risk_assessment: RiskAssessment | None   # 仅 v1.2+ 填写
```

### 六、风险信号传导机制

```
write_task() 执行
      ↓
risk_assessment.blocked == True
      ↓
┌──────────────────────────────────────────────┐
│ 同步传导（Agent 立刻感知）                    │
│   result.risk_assessment.blocked == True     │
│   result.risk_assessment.triggered_by = [...] │
└──────────────────────────────────────────────┘
      ↓
┌──────────────────────────────────────────────┐
│ 异步传导（事件系统）                          │
│   事件类型：review_needs_human               │
│   载荷：review_id, risk_level, triggered_by  │
│   接收方：所有订阅了该项目事件的 Agent        │
│   PM 收到后调用 mark_human_approved()        │
└──────────────────────────────────────────────┘
      ↓
┌──────────────────────────────────────────────┐
│ 批准后传导（Agent 继续执行）                  │
│   事件类型：review_approved                  │
│   载荷：review_id, approver, timestamp       │
│   Agent 监听到后继续执行后续操作              │
└──────────────────────────────────────────────┘
```

---

## 实现范围（v1.2）

| 组件 | 变更 |
|------|------|
| `fcop.project.write_task()` | 新增 `tools_hint` 参数；内部调用评估层；返回 `TaskWriteResult` |
| `fcop.core.risk_assessor` | 新模块，实现三层评估逻辑 |
| `fcop.models` | 新增 `RiskAssessment`、`TaskWriteResult` dataclass |
| `fcop.core.events` | 新增 `review_needs_human`、`review_approved` 事件类型 |
| `fcop-mcp` | `write_task` 工具透传 `tools_hint`；返回 `risk_assessment` 字段 |
| `fcop.json` schema | `Skill.tools[]` 已就绪（ADR-0027），本 ADR 新增消费逻辑 |

---

## 不在本 ADR 范围内

- **Layer B（工具执行中的拦截）**：由 Agent runtime / MCP server 自行实现，FCoP 提供 `Skill.tools[]` 元数据供其参考，不直接介入执行过程
- **LLM 辅助评估**：作为可选的 Layer 4，留待独立 ADR 决策
- **关键词规则库的具体内容**：由实现时的 `risk_assessor.py` 维护，不固化到协议层

---

## Consequences

- **向后兼容**：`tools_hint` 可选，不填时 Layer 1 不运行，行为与 v1.1 相同
- **可审计性提升**：每个任务的 `risk_assessment` 字段记录推断过程，PM 审阅时可见推断依据
- **Agent 无法绕过门控**：executor 层 Agent 无论是否填写 `risk_level`，系统下限都在
- **PM 权力明确**：只有 `Agent.layer="PM"` 且附带 `override_reason` 才能降低风险等级
- **事件驱动替代轮询**：`review_needs_human` / `review_approved` 事件让双方都能及时感知，减少 Agent 空转轮询
