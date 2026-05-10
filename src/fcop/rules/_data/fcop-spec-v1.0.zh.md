# FCoP Agent 运行时协议 — v1.0（简体中文版）

| | |
|---|---|
| **状态** | **正式发布** — 七大核心概念已固化为 v1.x 系列稳定标准（标签 `v1.0.0`，2026-05-09） |
| **版本** | 1.0.0 |
| **日期** | 2026-05-09 |
| **章程** | [ADR-0015](../adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md) |
| **前身** | [`spec/fcop-spec-v1.0.3.md`](./fcop-spec-v1.0.3.md)（0.7.x 基线；保留为遗留参考） |
| **机器可读契约** | [`spec/schemas/`](./schemas/)（7 个 JSON Schema） |
| **许可证** | MIT |
| **权威版本** | **本文为参考译文（informative）**；与英文版 [`spec/fcop-runtime-protocol-v1.0.md`](./fcop-runtime-protocol-v1.0.md) 不一致时，**以英文版为准**。 |

---

## 摘要

FCoP（**F**ile-based **Co**ordination **P**rotocol，文件驱动协作协议）是 **AI OS 协议层**——agent 在共享文件系统上协作的运行时契约。它在 AI OS 栈中的位置等同于 Unix 中的 **POSIX**、容器生态中的 **OCI**、Kubernetes 中的 **CRD**。

本文是 **FCoP v1.0 的规范性说明（中文版）**，将七大核心概念——**Agent、Encoding、IPC、Event、Failure、Boundary、Audit**——的最小语义契约正式固化为稳定标准，任何合规实现都必须满足。

> 「FCoP 是 agent 的协议，我们发现了它，而不是发明；而正好人类也可以读懂。」——[ADR-0015 §FCoP is discovered, not invented](../adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md#fcop-is-discovered-not-invented)

---

## §1 · 范围、状态与合规性

### 1.1 本文是什么

本文是 FCoP v1.0 的**唯一规范性说明（中文参考版）**。ADR（`adr/ADR-NNNN-*.md`）记录每个决策**为什么**这样做，并在协议版本之间相互取代；本文记录实现**今天必须做什么**。

当 ADR 与本文在**协议要求**上矛盾时，**本文优先**。当本文与 [`spec/schemas/`](./schemas/) 中的 JSON Schema 在**字段定义**上矛盾时，**Schema 优先**（[ADR-0016](../adr/ADR-0016-json-schema-for-7-abstractions.md)）。

### 1.2 本文不是什么

- 不是教程——见 [`docs/getting-started.md`](../docs/getting-started.md)。
- 不是决策日志——见 [`adr/`](../adr/)。
- 不是参考实现指南——见 `src/fcop/` 及其 README。
- 不是 0.7.x 规范——那个版本保留在 [`spec/fcop-spec-v1.0.3.md`](./fcop-spec-v1.0.3.md)，仅用于遗留合规测试。

### 1.3 合规性语言

本文中大写的关键词 **MUST（必须）**、**MUST NOT（禁止）**、**REQUIRED（要求）**、**SHALL（应当）**、**SHALL NOT（不应当）**、**SHOULD（建议）**、**SHOULD NOT（不建议）**、**RECOMMENDED（推荐）**、**MAY（可以）**、**OPTIONAL（可选）** 依照 [BCP 14 / RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) 和 [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174) 解释。

### 1.4 合规性等级

**v1.0 合规实现**必须满足以下 §3 至 §6 中所有 MUST 条款。

**v1.0 合规实现** MAY 提供超出本规范要求的额外能力，但扩展：

- MUST NOT 改变任何 v1.0 合规要求的含义
- MUST NOT 引入第 5 种 IPC 信封类型
- MUST NOT 为 REVIEW 引入新的 `decision` 值（4 值枚举在 v1.0 已固化）
- SHOULD 标注为实现专有扩展

---

## §2 · AI OS 协议栈——FCoP 的位置

```
┌─────────────────────────────────────────────────────────────────┐
│  应用层（Application）  CodeFlow / Cursor / Claude Desktop     │
│                         （基于 agent 构建的业务产品）           │
├─────────────────────────────────────────────────────────────────┤
│  宿主适配层（Host Adapter）fcop-mcp / fcop-cli / @fcop/claude  │
│                         （libc 等价层：将宿主桥接到协议）       │
│                         注：.mdc 文件是 Cursor 专属适配产物     │
├─────────────────────────────────────────────────────────────────┤
│ ★ FCoP 协议层 ★         Agent / IPC / Encoding / Event /       │
│  （本规范）             Failure / Boundary / Audit             │
│                         （POSIX 等价层：协议契约）              │
├─────────────────────────────────────────────────────────────────┤
│  参考实现               `fcop`（Python 库）                     │
│                         （v1.0 提供唯一实现）                   │
├─────────────────────────────────────────────────────────────────┤
│  内核原语               LLM API / 文件系统 / 进程管理器         │
│                         （AI OS 内核——超出本规范范围）          │
└─────────────────────────────────────────────────────────────────┘
```

本规范**仅定义★标注的一行**。基于 FCoP 构建的实现和应用超出范围，仅受本规范公开的契约约束。

---

## §3 · 七大核心概念

下表汇总七个概念及其 POSIX 类比。每个概念的详细契约见 §4。

| # | 概念 | POSIX 类比 | Schema | 来源 ADR |
|---|---|---|---|---|
| 1 | **Agent**（生命周期 + 身份） | 进程 | [`agent.schema.json`](./schemas/agent.schema.json) | [ADR-0020](../adr/ADR-0020-agent-boundary-and-capability.md) |
| 2 | **Encoding**（IPC + 开放知识双 surface） | 文件系统 | [`encoding.schema.json`](./schemas/encoding.schema.json) | [ADR-0021](../adr/ADR-0021-encoding-abstraction.md) + [ADR-0022](../adr/ADR-0022-workspace-directory-convention.md) |
| 3 | **IPC**（4 种信封类型） | 管道 / 消息队列 | [`ipc-envelope.schema.json`](./schemas/ipc-envelope.schema.json) | [ADR-0017](../adr/ADR-0017-review-file-type-minimal.md) + 0.7.x 基线 |
| 4 | **Event**（12 种派生事件） | 信号 | [`event.schema.json`](./schemas/event.schema.json) | [ADR-0018](../adr/ADR-0018-event-model.md) |
| 5 | **Failure & Recovery**（故障与恢复） | errno + 信号处理器 | [`failure.schema.json`](./schemas/failure.schema.json) | [ADR-0019](../adr/ADR-0019-failure-and-recovery-semantics.md) |
| 6 | **Boundary & Capability**（边界与能力） | 权限 | [`boundary.schema.json`](./schemas/boundary.schema.json) | [ADR-0020](../adr/ADR-0020-agent-boundary-and-capability.md) |
| 7 | **Audit**（审计，通过 REVIEW 实现） | syslog | [`review.schema.json`](./schemas/review.schema.json) | [ADR-0017](../adr/ADR-0017-review-file-type-minimal.md) |

---

## §4 · 各概念的契约

### §4.1 概念 1——Agent

**Agent** 是 FCoP 项目中的自主参与者，具有稳定身份（`code`）、层级（`worker` | `governance` | `admin`）和能力集合。

合规实现 MUST：

- A1.1 将角色 `code`（大写，1–16 字符，匹配 `^[A-Z][A-Z0-9]{0,15}$`）作为 IPC 信封文件名中的路由键。人类可读的 `label` MUST NOT 用于路由。
- A1.2 拒绝以编程方式创建 `layer: "admin"` 的 Agent。`admin` 层保留给人类操作员。
- A1.3 当 Agent 记录中指定了 `can` 和/或 `cannot` 时，将这些列表视为权威。仅当 `can` 和 `cannot` 均缺失或为空时，才应用 `layer` 默认能力集（见 §4.6）。
- A1.4 在参考实现中，将 `session_id`（若存在）以 `<task_id>:<agent_code>` 格式暴露。其他实现 MAY 使用其他形式，但 MUST 在 `recover_session` 调用中保持标识符稳定。

完整 Schema 见 [`agent.schema.json`](./schemas/agent.schema.json)。

### §4.2 概念 2——Encoding

**Encoding** 概念有**两个 surface**（[ADR-0021](../adr/ADR-0021-encoding-abstraction.md)），共享同一 `workspace_dir` 契约。

**IPC Surface（强契约）。** 合规实现 MUST：

- A2.1 恰好识别四种 IPC 信封类型：`TASK`、`REPORT`、`ISSUE`、`REVIEW`。添加第五种是 MAJOR 版本协议变更。
- A2.2 将信封文件名与 [`encoding.schema.json`](./schemas/encoding.schema.json) 中的 `filename_grammar` 模式匹配。日期格式为 `YYYYMMDD`；序号为 3 位零填充，每天单调递增。
- A2.3 要求每个信封的 frontmatter 中包含 `protocol`、`version`、`type`、`sender`。各信封类型的 Schema（见 §4.3）会添加更多必填字段。

**开放知识 Surface（弱契约）。** 合规实现 MUST：

- A2.4 允许 `<workspace_dir>/shared/` 下任何匹配 `^[A-Z][A-Z0-9-]*-[a-z0-9-]+(\.[a-z]{2,5})?\.md$` 的文件名。PREFIX 词表是开放的：实现 MUST NOT 因 PREFIX 不在任何列表中而拒绝。
- A2.5 将 frontmatter 视为开放知识 Surface 上的 OPTIONAL。
- A2.6 不枚举或规范性推荐任何具体 PREFIX 词汇。`encoding.schema.json` 中的 `informative_observed_prefixes` 列表（`GUIDE / SPEC / STATUS / TEAM / LETTER / MEMO / RECIPE / ARCHIVE`）**仅为参考**，不得用作验证门控。

> **为什么需要双 Surface？** 现场数据表明，agent 在没有任何规范指导的情况下，会自然收敛到一小组 PREFIX 来共享临时文档。将 `shared/` 排除在协议外会丢弃 50%+ 的真实 agent 产出；在规范中枚举 PREFIX 则会固化 agent 的创造力。双 Surface 解决了这个张力。详见 [ADR-0021 §why two surfaces](../adr/ADR-0021-encoding-abstraction.md#why-two-surfaces)。

**Workspace 目录。** 合规实现 MUST：

- A2.7 默认将 `workspace_dir` 设为 `fcop/`（[ADR-0022](../adr/ADR-0022-workspace-directory-convention.md)）。
- A2.8 检测到遗留 `docs/agents/` workspace 时发出弃用警告。实现 MAY 提供一键迁移工具（参考实现提供 `fcop migrate-workspace`）。
- A2.9 允许注册替代 Encoding 实现，前提是满足本概念的契约。v1.0 提供唯一一种具体 Encoding（`MarkdownEncoding`）；见 §6。

### §4.3 概念 3——IPC

四种 IPC 信封类型共享一个公共基础；每种类型添加特定的必填字段。完整 Schema 见 [`ipc-envelope.schema.json`](./schemas/ipc-envelope.schema.json)。

| 信封类型 | 必填字段（基础之外） | 文件名模式 |
|---|---|---|
| **TASK** | `recipient`、`subject` | `TASK-{日期}-{序号}-{发件人}-to-{收件人}.md` |
| **REPORT** | `recipient`、`ref_task`、`status` | `REPORT-{日期}-{序号}-{发件人}-to-{收件人}.md` |
| **ISSUE** | `subject` | `ISSUE-{日期}-{序号}-{发件人}.md` |
| **REVIEW** | `subject_type`、`subject_ref`、`decision` | `REVIEW-{日期}-{序号}-{发件人}-on-{主题}.md` |

合规实现 MUST：

- A3.1 将每个信封的 `status`（TASK / REPORT）视为枚举 `pending | accepted | in_progress | blocked | done | aborted` 的成员。`aborted` 值由 [ADR-0019](../adr/ADR-0019-failure-and-recovery-semantics.md) 添加，v1.0 中为 REQUIRED。
- A3.2 允许信封根部存在未知的额外 frontmatter 键（`additionalProperties: true`）。这保持了 0.7.x 向后兼容性（[ADR-0003](../adr/ADR-0003-stability-charter.md)）。
- A3.3 当 REPORT 引用 TASK 时，将 `ref_task` 设置为 TASK 文件的**路径**（不是其 frontmatter 的 `subject`）。
- A3.4 当信封缺少 `type`（遗留 0.7.x 文件）时，实现 SHOULD 在验证前从文件名 PREFIX 推断 `type`。

### §4.4 概念 4——Event（事件）

FCoP v1.0 事件**派生自文件系统状态变化**；不存在 `EVENT-*.md` 信封类型（[ADR-0018](../adr/ADR-0018-event-model.md)）。

合规实现 MUST：

- A4.1 恰好识别十二种事件类型（[`event.schema.json`](./schemas/event.schema.json)）：
  - **来自任务 / 报告 / 审核状态变化**：`TASK_CREATED`、`TASK_ACCEPTED`、`TASK_BLOCKED`、`TASK_COMPLETED`、`REPORT_FILED`、`REVIEW_DECIDED`
  - **来自边界 / 角色变化**：`BOUNDARY_VIOLATED`、`ROLE_SWITCHED`
  - **来自故障 / 恢复处理**（per [ADR-0019](../adr/ADR-0019-failure-and-recovery-semantics.md)）：`FAILURE_DETECTED`、`RECOVERY_INITIATED`、`RECOVERY_COMPLETED`、`SESSION_LOST`
- A4.2 提供至少一种机制让应用订阅事件（参考实现提供 `Project.subscribe_events(types, callback)`；宿主适配器 MAY 通过 MCP 工具、WebSocket、文件监视器等暴露此功能）。
- A4.3 每个源状态变化最多触发一次事件。实现 SHOULD 对单次文件系统操作产生的重复事件进行去重。
- A4.4 保证**单个 agent 内**的时间戳单调排序。跨 agent 的 happens-before 关系超出 v1.0 范围；如需此功能，应用 MUST 自行在上层实现因果关系。

合规实现 MAY：

- A4.5 持久化事件日志（例如写入 `<workspace_dir>/log/events/`）。v1.0 不要求持久化。

### §4.5 概念 5——Failure & Recovery（故障与恢复）

真正的运行时由异常的处理方式定义，而不仅仅是正常路径。v1.0 固化了**四种故障模式**和**五种恢复动作**。

| 故障模式 | 触发条件 |
|---|---|
| `TIMEOUT` | Agent 未在 TASK 的 `timeout_at` 之前交付 |
| `CRASH` | 参考实现或宿主适配器异常退出 |
| `DEADLOCK` | 两个或更多 agent 相互等待对方的输出 |
| `DRIFT` | Agent 的输出与 TASK 契约不匹配 |

| 恢复动作 | 效果 |
|---|---|
| `RETRY` | 同一 agent 重新执行同一 TASK |
| `RESUME` | 加载会话状态，从中断处继续 |
| `ROLLBACK` | `git revert` 到 TASK 前的文件状态 |
| `ABORT` | 将 TASK 状态标记为 `aborted`，不再重试 |
| `ESCALATE` | 提升到下一治理层（默认为 `fcop.json` 中的 `leader`） |

合规实现 MUST：

- A5.1 拒绝 `failure_type` 不在四种之内的故障记录；拒绝 `recovery_action` 不在五种之内的恢复记录。
- A5.2 将每次应用的恢复与触发它的故障关联（关联字段：`trigger_failure_id`）。
- A5.3 提供 `recover_session(session_id, action)` API，至少支持 `resume`、`rollback`、`abort` 三种动作。（`RETRY` 和 `ESCALATE` 是调用方的调度决策，不是会话状态操作。）
- A5.4 在写入对应记录时触发 `FAILURE_DETECTED`、`RECOVERY_INITIATED`、`RECOVERY_COMPLETED` 事件（per §4.4）。

合规实现 SHOULD：

- A5.5 不在协议层强制执行特定的 Failure→Recovery 映射。映射由实现定义；例如，一种实现可能对 TIMEOUT 自动 RETRY，另一种可能自动 ESCALATE。

### §4.6 概念 6——Boundary & Capability（边界与能力）

Agent 有明确的能力边界。v1.0 固化了 **10 个能力词汇 token** 和 **4 条边界规则**。

**能力词汇（固化为 10 个）：**

`file_io`、`task_io`、`modify_code`、`review_decision`、`approve_release`、`escalate`、`spawn_agent`、`override`、`archive`、`mark_done`

各 token 的语义见 [`boundary.schema.json`](./schemas/boundary.schema.json)。

**层级默认值（参考，可被 Agent 配置覆盖）：**

| 层级 | 默认 `can` | 默认 `cannot` |
|---|---|---|
| `worker` | `file_io`、`task_io` | `approve_release`、`escalate`、`spawn_agent` |
| `governance` | `file_io`、`task_io`、`review_decision` | `modify_code`、`spawn_agent` |
| `admin` | `file_io`、`task_io`、`review_decision`、`escalate`、`override` | （无——但 `admin` MUST NOT 出现在 `fcop.json` 中） |

**边界规则（所有写操作前 MUST 强制执行）：**

- B1 `NO_ADMIN_PROGRAMMATIC_CREATE` — 实现 MUST 拒绝任何以编程方式创建 `layer: "admin"` Agent 的尝试。
- B2 `NO_GOVERNANCE_FISSION` — `governance` 层 Agent MUST NOT 生成其他 Agent。
- B3 `NO_WORKER_REVIEWS_GOVERNANCE` — `worker` 层 Agent 对 `governance` 层 Agent 输出的 REVIEW MUST 被拒绝。
- B4 `EXPLICIT_OVERRIDES_LAYER` — 当 Agent 有显式的 `can`/`cannot` 时，这些列表优先于层级默认能力集。

任何 B1–B4 触发时，合规实现 MUST 触发 `BOUNDARY_VIOLATED` 事件。

### §4.7 概念 7——Audit（审计，REVIEW）

REVIEW 是治理层对某个制品的决策。v1.0 仅提供**最小 surface**（[ADR-0017](../adr/ADR-0017-review-file-type-minimal.md)）。

合规实现 MUST：

- A7.1 恰好识别四个 `decision` 值：`approved`、`rejected`、`needs_changes`、`abstained`。添加第五个（例如 `needs_human`）是 MINOR 版本变更，且 MUST NOT 在 v1.2 之前发生（per [ADR-0015 §non-goals](../adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md)）。
- A7.2 拒绝 `decision: needs_changes` 且 `required_changes` 列表为空（或缺失）的 REVIEW。
- A7.3 识别四种 `subject_type` 值：`task`、`report`、`role_switch`、`code_change`。
- A7.4 不实现 `Project.mark_human_approved()`、`human_approval` 子对象、admin 层手动文件编辑守卫，以及任何其他 v1.2 延期功能。

合规实现 MAY：

- A7.5 将 REVIEW 存储在 `<workspace_dir>/reviews/`，关闭时归档到 `<workspace_dir>/log/reviews/`。

---

## §5 · 协议不变量

实现 MUST 在所有操作中保持以下不变量：

- **I1 · 文件名原子性** — 文件即路由。将 `tasks/TASK-X.md` 重命名为 `log/tasks/TASK-X.md` 就是状态转换 `TASK_COMPLETED`。实现 MUST 将 `os.rename()`（或等价操作）视为挂载点内唯一的同步原语，不需要锁，不需要中间人。
- **I2 · 文件系统是唯一真理来源** — 实现 MUST NOT 维护与文件系统不一致的隐藏状态存储。若 UI 显示 TASK 为 `done` 但文件仍在 `tasks/`，以文件为准。
- **I3 · Schema 是契约** — 当进程内 dataclass 与 `spec/schemas/*.schema.json` 不一致时，Schema 优先。实现 SHOULD 有 CI 检查来强制执行（[ADR-0016](../adr/ADR-0016-json-schema-for-7-abstractions.md)）。
- **I4 · 开放知识 Surface 保持开放** — 实现 MUST NOT 仅因 PREFIX 未知而拒绝 `<workspace_dir>/shared/` 中的文件。
- **I5 · v1.x 内向后兼容** — v1.0 合规实现写入的文件 MUST 对任何 v1.x 合规实现保持有效。v1.x 变更仅为 additive（[ADR-0003](../adr/ADR-0003-stability-charter.md)）。

---

## §6 · 参考 Encoding（Markdown + YAML frontmatter）

v1.0 提供唯一一种具体 Encoding 实现：`MarkdownEncoding`（[ADR-0021](../adr/ADR-0021-encoding-abstraction.md)）。

### 6.1 文件格式

每个 IPC 信封是一个 UTF-8 文本文件，结构如下：

```
---
<YAML frontmatter>
---

<Markdown 正文>
```

- Frontmatter MUST 兼容 YAML 1.2。
- 正文 MUST 为 Markdown（CommonMark，不要求特定方言扩展）。
- 文件 MUST 以 `.md` 为扩展名。

### 6.2 文件系统布局

```
<项目根目录>/
└── fcop/                      ← workspace_dir（per ADR-0022 默认值）
    ├── fcop.json              ← 团队 / 角色配置
    ├── tasks/                 ← 活跃的 TASK-*.md
    ├── reports/               ← 活跃的 REPORT-*.md
    ├── issues/                ← 活跃的 ISSUE-*.md
    ├── reviews/               ← 活跃的 REVIEW-*.md（v1.0；首次 REVIEW 时创建）
    ├── shared/                ← 开放知识 Surface——agent 自由创造
    └── log/                   ← 归档
        ├── tasks/
        ├── reports/
        ├── issues/
        └── reviews/
```

### 6.3 替代 Encoding

v1.x 合规的替代 Encoding（例如 JSON / SQLite / 事件流）MUST：

- 实现 [`encoding.schema.json`](./schemas/encoding.schema.json) 中的契约。
- 与 `MarkdownEncoding` 在两个 surface（IPC 和开放知识）上无损互转。
- 通过 `Project(encoding=...)` 注册（参考实现暴露此构造器参数）。

v1.0 不提供任何替代 Encoding。该构造器参数的存在是为了在 v1.x 添加替代 Encoding 时不破坏 API。

---

## §7 · 版本控制与稳定性

FCoP 遵循语义化版本控制（[ADR-0003](../adr/ADR-0003-stability-charter.md)）。协议变更规则：

| 变更类型 | SemVer | 冷却期 |
|---|---|---|
| 添加新可选字段、新枚举值、新 Schema 文件 | MINOR（如 1.0 → 1.1） | 无——additive |
| 将可选字段改为必填、删除字段、改变类型 | **MAJOR（如 1.x → 2.0）** | ≥ 6 个月共存 + 官方迁移工具 |
| 收紧正则 / 模式 | **MAJOR（如 1.x → 2.0）** | 同上 |
| 在不改变签名的情况下改变现有 API 行为 | PATCH（如 1.0.0 → 1.0.1） | 无——必须是 bug fix |

PyPI 包系列（[ADR-0015](../adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md)）：

| 包名 | 角色 | v1.0 版本 |
|---|---|---|
| `fcop` | 参考实现（本协议） | 1.0.0 |
| `fcop-mcp` | MCP 兼容宿主的宿主适配器 | 1.0.0 |
| `fcop-cli` | 命令行宿主适配器 | （v1.x 候选） |

协议级 v1.0.0 发布标签对应 `fcop` 和 `fcop-mcp` 同时达到 1.0.0。

### §7.1 七大核心概念的稳定性（规范性）

短语**「七大核心概念——Agent、Encoding、IPC、Event、Failure、Boundary、Audit——已固化为 v1.x 大版本系列的稳定标准」**贯穿本规范、README、发布说明和 `docs/MIGRATION-1.0.md`。本小节是唯一规范性定义；所有其他文档 MUST 引用此处，不得重复释义。

**固化范围。** 以下 §3–§6 中每个概念的 5 项属性在整个 v1.x 大版本系列中固化：

1. 每个信封 / 事件 / 故障 / 恢复 / 边界 / agent / encoding 契约中定义的**字段集**。
2. 每个字段的**类型**（string / integer / enum / array / object）。
3. 每个枚举的**合法值集合**（例如 `EventType` 有 12 个值；`Failure.kind` 有 4 个；`Recovery.action` 有 5 个；`Review.decision` 有 4 个）。
4. 每个字段的**语义**（合规实现 MUST 赋予的含义）。
5. §6.2 中定义的**文件名 grammar**（`{TYPE}-{YYYYMMDD}-{NNN}-{SENDER}-to-{RECIPIENT}.md`）。

**v1.x 期间禁止的变更。** 合规实现 MUST NOT：

- 从上述任何契约中删除已有字段；
- 改变已有字段的类型；
- 从已有枚举中删除值；
- 在保持字段名不变的情况下改变其语义；
- 收紧文件名 grammar（正则范围收窄）。

上述任何变更都需要 MAJOR bump 到 v2.0，且 v2.0 本身 MUST 满足 SemVer 表中的三个硬性要求（RFC + ≥ 6 个月共存 + 官方迁移工具），依据 [ADR-0015](../adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md) 和 [ADR-0003](../adr/ADR-0003-stability-charter.md)。

**v1.x 期间允许的变更（additive expansion）。** 合规实现 MAY 在任何 MINOR 版本中：

- 添加有默认值的新可选字段（旧消费者忽略它）；
- 添加新枚举值（前提是添加后不会破坏现有消费者）；
- 为新的概念扩展添加新 Schema 文件；
- 在 `fcop.Project` 上添加新公开 API 方法，在 `fcop-mcp` 上添加新 MCP 工具（同样遵循 additive 规则）。

合规实现 MAY 在任何 PATCH 版本中修复参考实现中的 bug，前提是通过 v1.x 契约可见的任何可观测行为不发生变化。

**固化 ≠ 停滞。** 固化的是上述**契约 surface**，而不是**实现**。参考实现（`fcop` Python 库）、宿主适配器（`fcop-mcp`）、Schema（additive 扩展）、文档、教程、性能和 bug fix 在整个 v1.x 期间自由演进。类比：POSIX `read()` 系统调用的签名几十年未变，而 Linux kernel 实现一直在演化。

**「固化」的时限。** 在本规范中，「固化」意味着：在 v1.x 大版本系列的生命周期内（1.0.0 至 1.99.99）。超出 v1.x 后，只能通过上述 MAJOR bump 打破固化；v1.x 和 v2.x MUST 至少共存 6 个月，且官方迁移工具 MUST 在 v1.x 弃用前发布。

---

## §8 · 合规测试 surface

v1.0 合规实现 SHOULD 通过本仓库 `tests/test_schemas/` 和 `tests/test_encoding/test_contract_compliance.py` 中的测试套件。依照 [ADR-0016](../adr/ADR-0016-json-schema-for-7-abstractions.md)，每个概念的 Schema 至少有三个测试用例：合法示例、缺少必填字段示例、非法枚举值示例。

**向后兼容见证**：本仓库 `docs/agents/log/` 下的每个 TASK / REPORT / ISSUE / REVIEW 文件（包含真实的 0.7.x agent 产出）MUST 在经过 [`spec/schemas/README.md`](./schemas/README.md) 中的遗留字段映射后，通过 [`spec/schemas/ipc-envelope.schema.json`](./schemas/ipc-envelope.schema.json) 验证。这是 I5 的规范性回归测试。

---

## §9 · 术语表

| 术语 | 定义 |
|---|---|
| **Agent** | 项目中的自主参与者，以大写角色 `code` 标识。 |
| **AI OS** | （应用层 / 宿主适配层 / FCoP 协议层 / 参考实现 / 内核原语）概念栈，让 agent 能够协作。FCoP 是该栈的协议层。 |
| **Audit（审计）** | 由 REVIEW 实现的协议概念，FCoP 的 syslog 等价物。 |
| **Boundary（边界）** | Agent 所拥有的能力集合。 |
| **Capability（能力）** | v1.0 词汇表中的 token（`file_io`、`task_io` 等），代表一个允许的动作。 |
| **Encoding** | 定义 IPC 信封和开放知识文档如何存储在磁盘上的协议概念。v1.0 提供 `MarkdownEncoding`。 |
| **Envelope（信封）** | 一种类型化消息：TASK、REPORT、ISSUE 或 REVIEW。 |
| **Event（事件）** | 从文件系统状态变化派生的类型化信号。v1.0 有 12 种事件类型。 |
| **Failure（故障）** | `TIMEOUT`、`CRASH`、`DEADLOCK`、`DRIFT` 之一。 |
| **FCoP** | File-based Coordination Protocol（文件驱动协作协议）——AI OS 协议层，即本文。 |
| **固化（Stabilised）** | 七大核心概念在 v1.x 下的状态：其五项属性（字段集 / 字段类型 / 枚举值集合 / 字段语义 / 文件名 grammar）在不进行 MAJOR bump 的情况下不得变更。详见 §7.1。 |
| **Host Adapter（宿主适配器）** | libc 等价层：将特定宿主（Cursor、Claude Desktop、命令行）桥接到 FCoP。注：`fcop-rules.mdc` / `fcop-protocol.mdc` 是 Cursor 专属的宿主适配层产物。 |
| **IPC Surface** | Encoding 的强契约 surface：4 种信封类型。 |
| **MAJOR 版本** | 协议契约以向后不兼容方式变更时递增。v2.0 需要协议级 RFC + 6 个月 v1/v2 共存窗口 + 官方迁移脚本。 |
| **MINOR 版本** | additive、向后兼容的扩展时递增：新可选字段、新枚举值、新 Schema、新公开 API 方法。在 v1.x 内允许，不破坏合规性。 |
| **Open Knowledge Surface（开放知识 Surface）** | Encoding 的弱契约 surface：agent 在 `shared/` 下自创 PREFIX 的文档。 |
| **PATCH 版本** | 向后兼容的修复和改进时递增：重构、性能优化、bug fix、文档、测试。不涉及协议契约变更。 |
| **预发布版（Pre-release）** | 以 `-rc.N` 结尾的版本（如 `1.0.0-rc.1`），表示契约处于最终审核阶段，不建议用于生产。 |
| **参考实现（Reference Implementation）** | 本仓库提供的 `fcop` Python 库。 |
| **Recovery（恢复）** | `RETRY`、`RESUME`、`ROLLBACK`、`ABORT`、`ESCALATE` 之一。 |
| **REVIEW** | v1.0 新增的第 4 种 IPC 信封类型，编码治理决策。 |
| **Schema** | [`spec/schemas/`](./schemas/) 中的 JSON Schema 文件，定义某个概念的字段契约。 |
| **Workspace dir** | 宿主项目内的协议命名空间目录。v1.0 默认：`fcop/`；v0.7.x 遗留：`docs/agents/`。 |

---

## Appendix A · 与 `spec/fcop-spec-v1.0.3.md`（0.7.x 基线）的差异

| 领域 | 0.7.x | v1.0 |
|---|---|---|
| 定位 | "基于文件的协作协议" | "AI OS 协议层" |
| 概念 | 隐式（5 个 dataclass：Agent、Task、Review*、Session、Skill） | 显式（7 个命名概念） |
| Schema | 无（dataclass 是真理） | 7 个 JSON Schema（Schema 是真理） |
| Workspace 目录 | `docs/agents/` | `fcop/`（含遗留检测与警告） |
| 信封类型 | 3 种（TASK、REPORT、ISSUE） | 4 种（+ REVIEW） |
| 开放知识 Surface | 隐式（agent 写 `shared/` 文件但无契约） | 显式（独立 surface，不枚举 PREFIX） |
| Event 模型 | 无 | 12 种派生事件 |
| Failure 模型 | 无 | 4 种模式 × 5 种恢复动作 |
| Boundary 模型 | 仅 `Agent.layer` | `layer` + `can` + `cannot` + 10 token 词汇 + 4 条规则 |
| 稳定性章程 | 1.0 前（MINOR 中允许 breaking change） | v1.0 章程（[ADR-0003](../adr/ADR-0003-stability-charter.md) + [ADR-0015](../adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md)） |

> *0.7.x 有 `Review` dataclass 但没有 REVIEW 信封文件类型——Review 是 Task 上的内存注解。v1.0 将其提升为第一类文件类型。*

---

## Appendix B · 权威文档地图

阅读顺序建议：
**新手** → `README.zh.md` / `getting-started.md` →
**升级** → `MIGRATION-1.0.md` →
**深入** → 本文（spec）+ ADR →
**参考** → schemas + CHANGELOG

### B.1 规范文件

| 文件 | 说明 |
|---|---|
| `spec/fcop-runtime-protocol-v1.0.md` | **英文权威规范**（normative，与本文不一致时以此为准） |
| `spec/fcop-runtime-protocol-v1.0.zh.md` | **本文**——完整中文平行版（informative） |
| `spec/schemas/*.schema.json` | 机器可读字段契约（7 个 Schema） |
| `spec/schemas/README.md` | Schema 索引、合规语言、校验代码片段 |

### B.2 宿主适配层（Cursor 专属）

> 注：以下 `.mdc` 文件是 **Cursor 专属格式**，属于宿主适配层，不是协议规范本身。其他宿主（CLI、Claude Desktop 等）使用不同格式的适配器。

| 文件 | 说明 |
|---|---|
| `src/fcop/rules/_data/fcop-rules.mdc` | Agent 规则主体（v1.9）——由 `fcop-mcp` 在 `init_project` 时自动部署到 `.cursor/rules/` |
| `src/fcop/rules/_data/fcop-protocol.mdc` | 协议注释（v1.7）——文件命名、YAML frontmatter、目录布局、巡逻规范 |
| `spec/codeflow-core.mdc` | **弃用占位**——仅防旧链接失效，无规范性内容 |

### B.3 架构决策记录（ADR）

| 文件 | 说明 |
|---|---|
| `adr/ADR-0015` | v1.0 总章程（AI OS 协议层定位） |
| `adr/ADR-0016` | 7 个概念的 JSON Schema 决策 |
| `adr/ADR-0017` | REVIEW 信封类型 |
| `adr/ADR-0018` | Event 模型（12 种事件） |
| `adr/ADR-0019` | Failure / Recovery 语义 |
| `adr/ADR-0020` | Boundary 能力模型 |
| `adr/ADR-0021` | Encoding 概念（IPC + 开放知识双 surface） |
| `adr/ADR-0022` | Workspace 目录约定（`fcop/` 迁移） |
| `adr/ADR-0003` | 稳定性章程（SemVer 策略） |
| `adr/ADR-0001..0006` | v1.0 前的基础决策 |
| `adr/ADR-0007..0014` | 已废弃 / 暂缓（保留历史） |

### B.4 用户指南

| 文件 | 说明 |
|---|---|
| `README.zh.md` | 中文项目入口 |
| `README.md` | 英文项目入口 |
| `docs/getting-started.md` | L0+L1 教程入口（非规范性） |
| `docs/MIGRATION-1.0.md` | 0.7.x → 1.0 迁移指南 |
| `docs/tutorials/` | 手把手实战教程 |

### B.5 发布记录

| 文件 | 说明 |
|---|---|
| `CHANGELOG.md` | 按版本归档的变更列表 |
| `docs/releases/1.0.0.md` | v1.0.0 最终发布说明 |
| `docs/releases/1.0.0-rc.1.md` | v1.0.0-rc.1 预发布说明 |
| `spec/fcop-spec-v1.0.3.md` | 0.7.x 基线（遗留合规测试用） |

---

## Appendix C · 致谢

FCoP 从实际部署中提炼而来，而非由委员会设计。v1.0 章程（[ADR-0015](../adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md)）详细记录了「发现，而非发明」的理念。塑造本规范的现场报告：

- `essays/when-ai-organizes-its-own-work.md` — agent 在 48 小时内自主发明的 6 种协作模式
- `essays/fcop-natural-protocol.md` — agent 在没有任何提示的情况下主动认可 FCoP 规则
- `essays/when-ai-vacates-its-own-seat.md` — agent 在冲突中自主补全协议中未写明的部分
- `essays/what-agents-say-about-fcop.md` — 直接询问 agent 的反馈
- `docs/tutorials/snake-solo-to-duo.zh.md` 和 `tetris-solo-to-duo.en.md` — 45 分钟实战 dogfood，产出了首次观测到的 `STATUS-*-RECORD.md` agent 自创发明

开放知识 Surface（§4.2）正是因为最后两个文件而存在。
