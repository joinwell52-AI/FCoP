# FCoP Agent 运行时协议 — v1.1

| | |
|---|---|
| **状态** | **已批准** — v1.1 additive 扩展，向后兼容 v1.0 |
| **版本** | 1.1.0 |
| **日期** | 2026-05-11 |
| **决策依据** | [ADR-0023](../adr/ADR-0023-agent-layer-governance-field.md) · [ADR-0024](../adr/ADR-0024-task-risk-level.md) · [ADR-0025](../adr/ADR-0025-review-needs-human.md) · [ADR-0026](../adr/ADR-0026-review-human-approval.md) · [ADR-0027](../adr/ADR-0027-skill-tools-risk-metadata.md) |
| **前版本** | [`spec/fcop-runtime-protocol-v1.0.zh.md`](./fcop-runtime-protocol-v1.0.zh.md) |
| **机器可读 schema** | [`spec/schemas/`](./schemas/)（8 个 JSON Schema） |
| **捆绑规则** | `fcop-rules.mdc` v2.2.0 · `fcop-protocol.mdc` v2.0.0 |
| **参考实现** | `fcop>=1.1.0` · `fcop-mcp>=1.1.0`（当前版本：`1.2.1`，锁步） |
| **英文版** | [`spec/fcop-runtime-protocol-v1.1.md`](./fcop-runtime-protocol-v1.1.md) |

---

## 范围

本文记录相对于
[`spec/fcop-runtime-protocol-v1.0.zh.md`](./fcop-runtime-protocol-v1.0.zh.md)
的 **v1.1 协议变更**。

v1.1 是在 FCoP 稳定性章程（[ADR-0003](../adr/ADR-0003-stability-charter.md)）下的
**MINOR additive 版本**。所有 v1.0 规则、schema 和工具调用保持有效。
全部变更均为 opt-in 新增——现有 frontmatter 字段、文件和工具调用均无破坏。

---

## 变更摘要

| ADR | 变更内容 | Schema 影响 |
|---|---|---|
| [ADR-0023](../adr/ADR-0023-agent-layer-governance-field.md) | `Agent.layer` 运行时治理合约 | `ipc-envelope.schema.json`（role 对象） |
| [ADR-0024](../adr/ADR-0024-task-risk-level.md) | `Task.risk_level` 字段（4 级枚举） | `ipc-envelope.schema.json`（task 形状） |
| [ADR-0025](../adr/ADR-0025-review-needs-human.md) | `Review.decision = needs_human`（第 5 个枚举值） | `review.schema.json` |
| [ADR-0026](../adr/ADR-0026-review-human-approval.md) | `Review.human_approval` 子对象 | `review.schema.json` |
| [ADR-0027](../adr/ADR-0027-skill-tools-risk-metadata.md) | `Skill.tools[]` 风险元数据 | `skill.schema.json` |

`fcop-mcp 1.1.0` 新增 MCP 工具：`write_review`、`list_reviews`、
`read_review`、`mark_human_approved`。扩展工具：`write_task` 新增
`risk_level` 参数。

---

## 详细变更说明

### 1. Agent.layer — 治理层级字段（ADR-0023）

`fcop.json` 的角色对象现在可携带 `layer` 字段：

```json
{
  "code": "PM",
  "label": "项目经理",
  "layer": "governance"
}
```

**三层体系：**

| 层级 | 描述 | 约束 |
|---|---|---|
| `worker` | 执行角色（DEV, QA, OPS, ME …） | 不得审核 `governance` 主体 |
| `governance` | 决策角色（PM, LEAD-*, PLANNER …） | 不得创建新 `governance` 角色（NO_GOVERNANCE_FISSION） |
| `admin` | 最高权限 | 程序化创建需要显式 override（NO_ADMIN_PROGRAMMATIC_CREATE） |

`layer` 可选，缺省时默认为 `worker`。这是**运行时合约**——
agent 在敏感操作前必须自我检查所在层级，违规时触发
`BOUNDARY_VIOLATED` 并写一条 `ISSUE-`。

---

### 2. Task.risk_level — 操作风险等级（ADR-0024）

任务文件 frontmatter 可携带可选的 `risk_level` 字段：

```yaml
---
protocol: fcop
version: 1
sender: PM
recipient: OPS
risk_level: high        # ← v1.1 新增
subject: 重启生产服务
---
```

**四级枚举：**

| 值 | 含义 | 工具层行为 |
|---|---|---|
| `low` | 标准操作（默认）| — |
| `medium` | 需关注，建议提供回滚方案 | 软提示 |
| `high` | 执行前需人工审批 | 自动写出 `REVIEW (decision=needs_human)` |
| `irreversible` | 不可撤销（生产数据删除、公开发布等）| 自动写出 REVIEW + 必须包含回滚方案 |

当 `write_task` 收到 `risk_level=high` 或 `irreversible` 时，自动创建
配套 REVIEW（`decision=needs_human`）。任务执行者**不得**在
`mark_human_approved` 被调用前继续执行。

---

### 3. Review.decision = needs_human（ADR-0025）

`review.schema.json` 中的 `decision` 枚举从 4 个值扩展至 **5 个值**：

```
approved | changes_requested | blocked | rejected | needs_human
```

`needs_human` 的语义：
- 审核 agent 判断**需要人类介入**来做出决策。
- 被审核的任务/报告**被冻结**——在 ADMIN 调用 `mark_human_approved` 前，
  任何 agent 不得继续执行。
- `needs_human` **不是**临时占位符；它是一个硬门控。
- Agent **不得**在没有人工干预的情况下将 `needs_human` 改写为其他值。

---

### 4. Review.human_approval 子对象（ADR-0026）

当 `decision = needs_human` 时，REVIEW 文件的 YAML frontmatter
可携带可选的 `human_approval` 块：

```yaml
decision: needs_human
human_approval:
  approved_by: "alice@example.com"
  approved_at: "2026-05-11T09:00:00+08:00"
  note: "已与安全团队确认，可以执行"
```

**完整流程：**

```
1. Agent 调用 write_task(risk_level="high")
   → 创建 TASK-*.md（含 risk_level: high）
   → 创建 REVIEW-*.md（decision: needs_human）

2. ADMIN 审阅并批准：
   → 调用 mark_human_approved(review_id="REVIEW-*.md")
   → human_approval 块被写入
   → decision 转换为 approved（由人工代理）

3. 执行角色读到更新后的 REVIEW → 继续执行任务
```

`human_approval` 块**只能写入一次**：一旦审批记录落盘，REVIEW 文件
即成为不可变的审计记录。

---

### 5. Skill.tools[] 风险元数据（ADR-0027）

`skill.schema.json` 现在允许 `tools[]` 数组的每个工具条目携带风险元数据：

```yaml
tools:
  - name: deploy_to_production
    description: "将构建产物部署到生产服务器"
    risk_level: high
    requires_human_approval: true
    side_effects: "修改生产流量路由；可通过负载均衡器部分回滚"
  - name: run_tests
    description: "运行完整测试套件"
    risk_level: low
    requires_human_approval: false
```

**字段说明（全部可选）：**

| 字段 | 类型 | 说明 |
|---|---|---|
| `risk_level` | 字符串（4 级枚举） | 继承与 `Task.risk_level` 相同的值 |
| `requires_human_approval` | bool | 为 true 时，调用方应在调用前走 `write_task(risk_level=high/irreversible)` 流程 |
| `side_effects` | 字符串 | 不可逆副作用的人类可读描述 |

这些元数据**机器可读**，供上层编排框架自动判断是否需要经过审批门。

---

## Schema 变更

### `review.schema.json`

- `decision` 枚举从 4 个值扩展至 5 个值：新增 `needs_human`。
- 新增可选属性：`human_approval`（包含 `approved_by` 字符串、
  `approved_at` 日期时间字符串、`note` 字符串的对象）。
- 即使 `decision=needs_human`，`human_approval` 也**非必填**
  （只在 `mark_human_approved` 被调用后才会出现）。

### `ipc-envelope.schema.json`

- TASK 形状：新增可选的 `risk_level` 属性（4 值字符串枚举）。
- Agent/role 形状：新增可选的 `layer` 属性（`worker` | `governance` | `admin`）。

### `skill.schema.json`

- `tools[]` 数组项：新增可选属性 `risk_level`、`requires_human_approval`、
  `side_effects`。

---

## 新增 MCP 工具（fcop-mcp 1.1.0）

| 工具 | 说明 |
|---|---|
| `write_review(subject_id, decision, reviewer, body)` | 创建 REVIEW envelope；用 `decision=needs_human` 开启人工审批门 |
| `list_reviews(decision=None, subject_id=None)` | 列出 REVIEW 文件，可按条件过滤 |
| `read_review(review_id)` | 按 ID 读取单个 REVIEW 文件 |
| `mark_human_approved(review_id, approved_by, note)` | 在 `needs_human` REVIEW 上记录人工审批 |

扩展工具：

| 工具 | 新增参数 |
|---|---|
| `write_task(...)` | `risk_level: str = ""` — `high` 或 `irreversible` 时自动创建配套 REVIEW |

完整参数参考：[`docs/mcp-tools.md`](../docs/mcp-tools.md)。

---

## 向后兼容性

v1.1 与 v1.0 **完全向后兼容**：

- 所有现有 TASK / REPORT / ISSUE / REVIEW 文件继续有效。
- `risk_level` 可选；缺失时默认为 `low`。
- `human_approval` 可选，即使 `decision=needs_human` 也不强制。
- `fcop.json` 中的 `layer` 可选；缺失时默认为 `worker`。
- `Skill.tools[]` 风险字段可选。
- 没有现有 MCP 工具签名发生变化（只有 additive 参数）。
- v1.0 项目无需迁移；通过使用新字段和工具来 opt-in v1.1 特性。

---

## 参考链接

- [`spec/fcop-runtime-protocol-v1.0.zh.md`](./fcop-runtime-protocol-v1.0.zh.md) — 基础协议（中文）
- [`spec/fcop-runtime-protocol-v1.1.md`](./fcop-runtime-protocol-v1.1.md) — 本文英文版
- [`adr/ADR-0023..0027`](../adr/) — 各项变更的决策依据
- [`docs/mcp-tools.md`](../docs/mcp-tools.md) — MCP 工具完整索引（30 个工具，14 个资源）
- [`docs/releases/1.1.0.md`](../docs/releases/1.1.0.md) — 发版说明
