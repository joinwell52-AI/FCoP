# FCoP v3 运行时规范 · 单页完整版（3.0 → 3.2.4）

| 字段 | 值 |
|---|---|
| **协议** | FCoP（Filesystem Coordination Protocol · 文件系统协调协议）|
| **规范版本** | **v3.2.4**（对齐 `fcop` / `fcop-mcp` PyPI **3.2.4**）|
| **协议规则 frontmatter** | `fcop_rules_version` / `fcop_protocol_version`：**3.2.3**（见 [CHANGELOG](../CHANGELOG.md)）|
| **状态** | **Current（当前）** — 取代仅覆盖 3.0.0 的 [`fcop-3.0-spec.zh.md`](./fcop-3.0-spec.zh.md) 作为日常阅读入口 |
| **发布日期** | 2026-05-27 |
| **许可证** | MIT |
| **英文对照** | [`fcop-v3-spec.md`](./fcop-v3-spec.md)（权威英文版）|
| **历史基线** | [`fcop-3.0-spec.zh.md`](./fcop-3.0-spec.zh.md)（2026-05-21 冻结的 3.0.0 单页；**不含** `history/` 层）|

> **合规性**：声称兼容 **FCoP v3.2.x** 的实现**必须**满足本文所有标注 **MUST** 的条款。  
> 声称仅兼容 **FCoP 3.0.0** 时，以 [`fcop-3.0-spec.md`](./fcop-3.0-spec.md) 为准（无 `history/` 要求）。

> **关于本文性质**：本文为 **v3 全系列运行时真相** 的中文平行版（informative）。  
> 规范性英文表达以 [`fcop-v3-spec.md`](./fcop-v3-spec.md) 为准。  
> **§1–§2** 继承 [ADR-0035](https://github.com/joinwell52-AI/FCoP/blob/main/adr/ADR-0035-lifecycle-directory-and-tool-layers.md) / [ADR-0036](https://github.com/joinwell52-AI/FCoP/blob/main/adr/ADR-0036-lifecycle-event-layer.md)；**§5** 历史深档案层来自 **v3.2.0**（[CHANGELOG](../CHANGELOG.md) §3.2.0），非 ADR-0036「事件层」本身。

---

## §0 · 核心声明

### §0.1 · Layer 1 · 认知引导层

> **文件即协议；位置定义状态；事件记录历史。**
>
> Files carry protocol. Paths address state. Events replay transitions.

### §0.2 · Layer 2 · 语义本体层

| | 中文 | 对应章节 |
|---|---|---|
| 1 | **文件是协议的外化载体。** | §6 |
| 2 | **位置是状态的地址映射。** | §2（`_lifecycle/`）、§4（`history/` 只读归宿）|
| 3 | **事件是状态转移的可重放证据。** | §3 |
| 4 | **治理判定落在 `reviews/`，与 `_lifecycle/review/` 阶段正交。** | §5 |

### §0.3 · 范围

FCoP **不是** Agent 运行时、工作流引擎或编排内核。它定义**文件系统上的协调接口**；执行归宿主（Cursor / Claude / Operator）与运行时框架。见 [ADR-0038](../adr/ADR-0038-fcop-boundary-charter.md)。

### §0.4 · 版本矩阵（读文档前先看）

| 标签 | 含义 | 典型值（本仓库）|
|---|---|---|
| **协议规范 3.0.0** | 2026-05-21 冻结的 `_lifecycle/` + `transitions:` | [`fcop-3.0-spec.zh.md`](./fcop-3.0-spec.zh.md) |
| **协议规范 3.2.x（本文）** | 3.0 能力 + **v3.1 生命周期 MCP** + **v3.2.0 `history/` 深档案** | 本文 |
| **`fcop` / `fcop-mcp` 包版本** | PyPI 发布号；**3.2.4** 主要为 wheel 编码修复，**无新协议语义** | [CHANGELOG](../CHANGELOG.md) |
| **规则文件 frontmatter** | `.cursor/rules/fcop-rules.mdc` 的 `fcop_rules_version` | **3.2.3** |

> **消费建议**：新集成（含 codeflowmu）请读**本文** + [`docs/mcp-tools.md`](../docs/mcp-tools.md)。  
> 勿把 [`fcop-3.0-spec.zh.md`](https://github.com/joinwell52-AI/FCoP/blob/main/spec/fcop-3.0-spec.zh.md) 当作最新全貌——其中**没有** `history/` 与 `claim_task` 等 **v3.1+** 能力。

---

## §1 · 术语：仓库根 vs FCoP 工作区根

实现通过 `fcop.lifecycle.find_workspace_root()` 解析 **FCoP 工作区根（workspace root）**，而不是 Git 仓库根：

| 候选路径（按优先级）| 说明 |
|---|---|
| `<repo>/fcop/` | **v1.0+ 默认**（本仓库即此布局）|
| `<repo>/docs/agents/` | 0.7.x 遗留布局 |

以下路径均相对于 **workspace root**（下文简写为 `<fcop-workspace>/`）：

```
<repository>/                    ← Git / IDE 项目根（可含 workspace/、.cursor/ 等）
├── fcop/                        ← ★ FCoP workspace root（典型）
│   ├── fcop.json                ← 项目身份唯一权威（Rule 3）
│   ├── LETTER-TO-ADMIN.md
│   ├── _lifecycle/              ← v3 状态层（§3）
│   ├── history/                   ← v3.2.0+ 深档案（§5）
│   ├── reports/
│   ├── issues/
│   ├── shared/
│   └── reviews/                 ← REVIEW 信封（v1.0+ 能力，非 _lifecycle 阶段）
├── workspace/<slug>/            ← Rule 7.5 产物笼子（soft）
└── .cursor/rules/               ← 协议规则部署（ADR-0006）
```

**常见误区**：bundled 规则图有时把 `_lifecycle/` 画在「仓库根」——那是 **workspace 与仓库根重合** 的特例。在 FCoP 本仓，真相是 **`fcop/_lifecycle/`**（见 `src/fcop/lifecycle/state.py` 与 `src/fcop/project.py`）。

---

## §2 · 状态层（NOW 真相 · `_lifecycle/`）

### 2.1 目录拓扑（v3 **MUST**）

合规的 v3 项目在 **workspace root** 下**必须**具备：

```
<fcop-workspace>/
├── _lifecycle/
│   ├── inbox/
│   ├── active/
│   ├── review/
│   ├── done/
│   └── archive/
├── reports/
├── issues/
└── shared/
```

五个 `_lifecycle/` 子目录**必须**位于**同一文件系统挂载点**（§2.5）。  
v2 专属的 `tasks/`、`log/` **不得**与完整 v3 `_lifecycle/` 并存（**MIXED** 拓扑，见 `fcop.lifecycle.detect`）。

### 2.2 阶段定义（已冻结 · ADR-0035）

| 阶段 | 语义 |
|------|------|
| `inbox` | created（已创建）|
| `active` | claimed（已认领）|
| `review` | pending confirmation（等待确认）|
| `done` | completed（已完成）|
| `archive` | closed（已关闭，仍属协调面「常规归档」）|

### 2.3 允许的 `_lifecycle/` 迁移（v3.0 + v3.1 工具名）

| 从 | 到 | L1 工具（MCP / Python）| 引入版本 |
|----|----|-------------------------|----------|
| — | `inbox` | `create_task` / `write_task` | 3.0 |
| `inbox` | `active` | `claim_task` | **3.1.0** |
| `active` | `review` | `submit_task` | **3.1.0** |
| `active` | `done` | `finish_task` | **3.1.0** |
| `review` | `done` | `approve_task` | **3.1.0** |
| `review` | `active` | `reject_task` | **3.1.0** |
| `done` | `archive` | `archive_task` | 3.0 |

上表以外的 `_lifecycle/` 迁移 **MUST NOT** 发生。

**完整端到端（含深档案，说明性）**：

```
inbox → active → review → done → archive  →  history/YYYY-MM-DD/<task-stem>/
         └──────── finish_task ────────┘              ↑
                                                    archive_to_history
                                                    （§5，v3.2.0+）
```

### 2.4 核心规则（与 3.0 规范相同）

> **规则 A** — 文件路径是唯一的 **NOW** 真相；**不得**从 frontmatter 推断当前 `_lifecycle` 阶段。  
> **规则 B** — 仅 L1 工具可在 `_lifecycle/` 各阶段目录间 `mv`。  
> **规则 C** — 迁移路径与权限编码在工具调用中，不由 `risk_level` 等字段驱动拓扑。

### 2.5 原子性与挂载点

L1 迁移**必须**采用 write-then-rename（读源 → 内存追加 `transitions:` → 写 `.{id}.tmp` → `fsync` → 同挂载点 `rename`）。  
见 [`fcop-3.0-spec.zh.md` §2.4](./fcop-3.0-spec.zh.md) 全文。

---

## §3 · 事件层（PAST 踪迹 · `transitions:`）

`_lifecycle/` 下每个 TASK 文件**应当**携带 YAML `transitions:` 数组（v3 frontmatter `version: 3`）。

每条事件**必须**含：`at`、`from`、`to`、`by`、`tool`。  
**规则 E–G** 与 [`fcop-3.0-spec.zh.md` §2](./fcop-3.0-spec.zh.md) 相同：**只追加**；**禁止**用回放事件推导当前阶段。

> **与 `history/` 的关系**：迁入 `history/` 后，文件**脱离** `_lifecycle/` 状态机；其 `transitions:` 冻结为审计记录，**不再**参与 NOW 判定。

---

## §4 · 历史深档案层（v3.2.0+ · `history/`）

### 4.1 为何需要单独一层

| 层 | 路径 | 角色 | 规模特征 |
|---|---|---|---|
| 常规归档 | `_lifecycle/archive/` | 已完成任务的**协调面**停靠站 | 单目录扁平；长期运行会 **O(总任务数)** |
| **深档案** | `history/YYYY-MM-DD/<task-stem>/` | 按日落盘、任务+报告**成对**的只读归宿 | 单日目录 **O(当日完成任务数)** |

`archive_task` **不变**；`history/` 是**可选的更深一层**（实现**应当**在 `init_project` / `init_solo` 时创建空 `history/`）。

### 4.2 目录拓扑（**MUST** 若实现 v3.2 历史能力）

```
<fcop-workspace>/history/
└── YYYY-MM-DD/                          ← 分片键：任务进入 done 的 UTC 日期（done_at）
    └── TASK-YYYYMMDD-NNN-SENDER-to-RECIPIENT/   ← 目录名 = 任务文件名去掉 .md
        ├── TASK-YYYYMMDD-NNN-....md     ← 任务正文（含 transitions:）
        └── REPORT-YYYYMMDD-NNN-....md ← 零个或多个配对报告（从 reports/ 一并迁入）
```

**规则 H · 深档案只进不出（协议面）**  
`history/` 下文件**不得**再通过 L1 生命周期工具迁回 `_lifecycle/`。需要「复活」任务时，应**复制**为新 `TASK-*`（新序号），遵守 Rule 5 只追加。

**规则 I · 分片键**  
`YYYY-MM-DD` **必须**取自该任务完成时刻（`done_at`，UTC）。实现缺省为「今天」时，调用方**应当**显式传 `done_date` 以免误分片。

**规则 J · 有机成对**  
同一 `<task-stem>/` 目录内**必须**同时包含该任务文件与其在 `archive_to_history` 时能找到的配对 `REPORT-*`（按 `task_id` / 文件名关联）。不得只移 TASK 而留下孤立 REPORT 于 `reports/`（工具层负责收集）。

### 4.3 L1 历史工具（**MUST** 若暴露 MCP）

| 工具 | 行为 | 层级 |
|------|------|------|
| `archive_to_history` | `_lifecycle/archive/` 中指定任务 + 配对报告 → `history/<date>/<stem>/` | L1 |
| `bulk_archive_to_history` | 按 `done_date` 批量执行上者 | L1 |
| `list_history` | 列出 `history/` 下任务 ID；可按 `date` 过滤 | L0 |
| `read_history_task` | 读取深档案中的任务对象 | L0 |

权威索引：[`docs/mcp-tools.md` §8](../docs/mcp-tools.md)。  
实现参考：`Project.archive_to_history`（`src/fcop/project.py`）。

### 4.4 与 v2 `log/` 的区别

| | v2 `fcop/log/` | v3 `_lifecycle/archive/` | v3 `history/` |
|---|---|---|---|
| 任务归档 | 常见 | 是 | 自 archive **再下沉** |
| 报告 | 常与任务一起进 log | 报告留在 `reports/` 直至深档案 | 与任务同目录 |
| 按日期分片 | 否 | 否 | **是** |

---

## §5 · 其它协调目录与治理审批（非 `_lifecycle` 阶段）

### 5.0 目录一览

| 目录 | 信封 | 是否随 L1 迁移 | 说明 |
|------|------|----------------|------|
| `reports/` | `REPORT-*` | 否 | 执行回执（Rule 6 互惠）；深档案时**复制/移动**进 `history/` |
| `issues/` | `ISSUE-*` | 否 | 阻塞 / 风险 / 违规记录 |
| `shared/` | `INSPECTION-*`、团队宪法等 | 否 | 站立文档可原地更新；`INSPECTION` 为协议体检产物（Rule 9.6）|
| `reviews/` | `REVIEW-*` | 否 | **治理层审计判定**（v1.0+，ADR-0017）；见 §5.2–§5.5 |
| `alerts/`（可选）| `ALERT-*` | 否 | 治理告警层 GAL（v1.3+，ADR-0031）；见 §5.6 |

IPC 四类信封：`TASK` / `REPORT` / `ISSUE` / `REVIEW`。机器可读 schema：`spec/schemas/ipc-envelope.schema.json`、`spec/schemas/review.schema.json`。行为规则：bundled `fcop-rules.mdc` Rule 9、`fcop-protocol.mdc` Rule 9 Commentary。

### 5.1 两种「review」——**必须**消歧

FCoP v3 里 **review 一词指两件正交的事**。混用会导致目录、工具与审批流程全部读错。

| 维度 | **A · 生命周期阶段** `_lifecycle/review/` | **B · 治理信封** `reviews/REVIEW-*.md` |
|------|---------------------------------------------|----------------------------------------|
| **是什么** | TASK 文件的**当前阶段**（目录位置 = NOW 真相）| 对某份制品的**审计判定记录**（独立文件，不迁移）|
| **典型动作** | `submit_task` → `approve_task` / `reject_task` | `write_review` →（可选）`mark_human_approved` |
| **谁在做** | 执行角色提交；leader / ADMIN 通过或打回任务 | `layer: governance` 或 `admin` 角色写 REVIEW |
| **与 Rule 6** | 仍须 `REPORT-*` 关闭工作；`approve_task` **不替代** REPORT | REVIEW **不替代** REPORT；不能单靠 REVIEW 宣称任务已交付 |
| **人工介入** | `reject_task` 的 `note` 是打回说明，不是 `needs_human` 枚举 | `decision: needs_human` + `human_approval` 子结构（ADR-0026）|

> **记忆口诀**：**目录上的 review = 任务在等人点通过；文件里的 REVIEW = 治理判决写在 `reviews/`。**

两条链路**可以**同时存在（例如：TASK 在 `_lifecycle/review/` 等人 `approve_task`，同时磁盘上有一份 `REVIEW-*` 要求 ADMIN 人工批高风险操作），但**没有**协议规定的自动绑定——实现方不得假设「进了 `_lifecycle/review/` 就一定有 REVIEW 文件」或反之。

### 5.2 治理层 `REVIEW-*` 信封（v1.0+ · ADR-0017）

**语义**：REVIEW 是第四类 IPC envelope，承载**对已有制品的判断**（通过 / 驳回 / 要求修改 / 弃权 / 升级人工），不是新一轮派工。

**规则 R1（与 REPORT 正交）** — REVIEW 是**审计痕迹**；关闭 TASK 的合法路径仍是 `REPORT-*`（或后续 `TASK-*` 回执），见 Rule 6。  
**规则 R2（只追加）** — `reviews/` 下文件**不得**原地改写 `decision`；修正须写新 REVIEW 并 `supersedes:` 指向旧文件（Rule 5，与 TASK/REPORT 相同纪律）。  
**规则 R3（边界）** — `worker` 层角色**不得**对 `governance` 主体写 REVIEW（Rule 9.2 / ADR-0020）；工具层 `write_review` 会调 `assert_boundary`。

#### 5.2.1 文件名文法（**不同于** TASK/REPORT）

REVIEW **不**使用 `{SENDER}-to-{RECIPIENT}` 路由段：

```
REVIEW-{YYYYMMDD}-{NNN}-{REVIEWER}-on-{subject_short}.md
```

| 段 | 含义 |
|----|------|
| `{REVIEWER}` | 写 REVIEW 的角色码（可与 `reviewer_role` frontmatter 一致）|
| `{subject_short}` | 被审对象的**短标签**（小写 slug；**不是**完整 `subject_ref`）|

`subject_ref` 在 frontmatter 里指向完整 ID（如 `TASK-20260510-003-ADMIN-to-DEV`）；`subject_short` 仅用于文件名可读性（如 `task-003`）。工具 `write_review` 可从 `subject_ref` 自动派生 `subject_short`。

#### 5.2.2 Frontmatter（**MUST** 若写 REVIEW）

| 字段 | 必填 | 说明 |
|------|------|------|
| `protocol` | ✅ | `fcop` |
| `version` | ✅ | 信封版本（整数，当前为 `1`）|
| `type` | ✅ | `REVIEW` |
| `review_id` | ✅ | 与文件名 stem 一致 |
| `subject_type` | ✅ | `task` \| `report` \| `role_switch` \| `code_change` |
| `subject_ref` | ✅ | 被审对象引用（通常 `TASK-*` / `REPORT-*` ID）|
| `reviewer_role` | ✅ | 评审角色码 |
| `decision` | ✅ | 见 §5.2.3 |
| `decided_at` | ✅ | ISO-8601 时间戳 |
| `sender` | ✅ | 与 `reviewer_role` 一致（IPC 惯例）|
| `reviewer_agent` | 可选 | 具体 session / agent 实例 |
| `rationale` | 推荐 | `rejected` / `needs_changes` / `needs_human` 时**应当**填写 |
| `required_changes` | 条件 | `decision=needs_changes` 时**必须**非空列表 |
| `human_approval` | 条件 | 仅当 `needs_human` 且人工已批后由 `mark_human_approved` 写入 |

正文：Markdown 说明理由、证据引用（须遵守 Rule 0.c 出处）。

#### 5.2.3 `decision` 枚举（v1.1 冻结 · ADR-0025）

工具与 `review.schema.json` 冻结的**五值**（实现层 **MUST** 使用下列字符串）：

| 值 | 含义 |
|----|------|
| `approved` | 制品可继续 / 判定通过 |
| `rejected` | 制品被否决，不得按原方案继续 |
| `needs_changes` | 要求修改；**必须**配非空 `required_changes` |
| `abstained` | 审核者回避 / 不在职责范围 |
| `needs_human` | **升级人工**；在 `human_approval` 落盘前视为 **pending** |

**禁止**使用 `pending` 作为 `decision` 值——它不是合法枚举。

> bundled `fcop-rules.mdc` Rule 9.1 教学叙述中可能出现 `changes_requested`、`blocked` 等同义措辞；**落盘与 MCP 校验**以本表与 `spec/schemas/review.schema.json` 为准。

### 5.3 人工审批回路（`needs_human` · ADR-0026）

当 `decision: needs_human` 时：

1. 相关 TASK 的**执行**在治理语义上**应当暂停**，直到人工闭环（具体阻塞由宿主 / CodeFlow 实现；协议面以 REVIEW 状态为准）。
2. Agent **不得**自行把 `needs_human` 改成 `approved` 或其它值。
3. 只有 `layer: admin` 的角色（真人 ADMIN 代理）通过 **`mark_human_approved(review_id, ...)`** 向 REVIEW frontmatter **追加** `human_approval` 子结构，才视为升级已解决。

**典型流程（说明性）**：

```
write_task(risk_level="high"|"irreversible")
  → （推荐）write_review(decision="needs_human", subject_ref=<task_id>)
  → ADMIN 审阅 REVIEW 与 TASK
  → mark_human_approved(review_id, approver=..., decision=approve|reject)
  → 执行角色继续 / 写 REPORT / 生命周期 approve_task（若适用）
```

`human_approval` 子结构**最低字段**（per schema）：`approver`、`decision`（`approve` / `reject`）、`approved_at`、`channel`（`mobile` / `cli` / `web` / `manual_file_edit`）。

### 5.4 `risk_level` 与 REVIEW 触发（ADR-0024）

TASK frontmatter 可选字段 `risk_level`：`low`（默认）| `medium` | `high` | `irreversible`。

| `risk_level` | 协议期望 |
|--------------|----------|
| `low` / `medium` | 无强制 REVIEW；`medium` 建议在正文说明回滚方案 |
| `high` / `irreversible` | **应当**配套 `write_review(decision="needs_human")`；`write_task` 工具可能自动提示或生成 REVIEW（实现细节见 `fcop-mcp`）|
| `irreversible` | 除 REVIEW 外，**应当**在 TASK/正文中写明回滚方案（配合 Rule 7 破坏性操作纪律）|

`risk_level` **不**驱动 `_lifecycle/` 目录迁移（Rule C，§2.4）。

### 5.5 生命周期审批 vs 治理 REVIEW 对照（端到端）

| 步骤 | 生命周期（§2）| 治理（本节）|
|------|-------------|-------------|
| 1 | `write_task` → `_lifecycle/inbox/` | （可选）`risk_level` |
| 2 | `claim_task` → `active/` | — |
| 3 | 执行工作 | （高风险时）`write_review` |
| 4a | `submit_task` → `review/` | — |
| 4b | 或 `finish_task` → `done/`（跳过生命周期审核）| — |
| 5 | `approve_task` / `reject_task` | `mark_human_approved`（若 `needs_human`）|
| 6 | `write_report` → `reports/` | — |
| 7 | `archive_task` → `archive/` | — |
| 8 | （可选）`archive_to_history` | — |

### 5.6 治理信号与 GAL（摘要 · ADR-0031）

**FCoP-Rule-G1**：`write_report` / `fcop_report` 属于**执行域自述**，**不构成**独立治理信号。只有 `write_review`、`mark_human_approved`、`fcop_check` 等才构成可审计的**独立治理视角**。

**GAL（Governance Alert Layer）**：`fcop/alerts/ALERT-*.md` 记录漂移信号（如长时间无独立治理事件、CRITICAL 工具无 REVIEW）。GAL **不**自动阻断写盘；由 ADMIN 处置。工具：`fcop_list_alerts`、`fcop_create_alert`（见 [`docs/mcp-tools.md`](../docs/mcp-tools.md)）。

---

## §6 · 身份（文件名语法）

### 6.1 TASK / REPORT / ISSUE（路由信封）

```
{TYPE}-{YYYYMMDD}-{NNN}-{SENDER}-to-{RECIPIENT}(-{slug}).md
```

- `TYPE`：`TASK` | `REPORT` | `ISSUE`
- `slug`：可选；**必须**小写字母起手（ADR-0033）；**不参与路由**
- 文件名在 `_lifecycle/` 内**不可变**；TASK 的阶段变化仅通过**目录位置**

### 6.2 REVIEW（治理信封 · 非路由）

```
REVIEW-{YYYYMMDD}-{NNN}-{REVIEWER}-on-{subject_short}.md
```

详见 §5.2.1。`REVIEW` **不参与** `list_tasks(recipient=...)` 路由。

---

## §7 · Custody（说明性 · 非存储字段）

与 [`fcop-3.0-spec.zh.md` §5](./fcop-3.0-spec.zh.md) 相同：从位置 + 事件**派生**解释；**禁止** `custodian:` 存储字段。

| 位置 | 派生 custodian |
|------|----------------|
| `_lifecycle/active/` | 最近 `to: active` 的 `by` |
| `history/.../` | 无（已关闭深档案）|

---

## §8 · 边界宪章（摘要）

FCoP **不**拥有：LLM 调用、队列调度、daemon、能力沙箱、向量库。  
扩展提案过滤与豁免见 [`fcop-3.0-spec.zh.md` §3](./fcop-3.0-spec.zh.md) 与 [ADR-0039](../adr/ADR-0039-fcop-freeze-discipline-and-runtime-absorption-era.md)。

---

## §9 · 合规清单

### 9.1 v3.0 合规（继承）

C1–C10 见 [`fcop-3.0-spec.zh.md` §6](./fcop-3.0-spec.zh.md)。

### 9.2 v3.2.x 附加（实现 `history/` 时 **MUST**）

| # | 要求 |
|---|------|
| C11 | 提供 `history/` 目录或等价路径，且 `archive_to_history` 写入 §4.2 结构 |
| C12 | 深档案分片使用 `done_at` 的 UTC 日期 |
| C13 | 不得将 `history/` 中文件再注册为 `_lifecycle` 当前状态 |
| C14 | `list_history` / `read_history_task` 只读，不修改深档案 |

### 9.3 v1.0+ 治理 / 审批（实现 `reviews/` 时 **MUST**）

| # | 要求 |
|---|------|
| C15 | `REVIEW-*` 文件名符合 §5.2.1；落盘于 `reviews/`（首次 `write_review` 可懒创建目录）|
| C16 | `decision` 使用 §5.2.3 五值之一；`needs_changes` 时 `required_changes` 非空 |
| C17 | `decision=needs_human` 时，**不得**在无 `human_approval` 的情况下将 REVIEW 视为已批准 |
| C18 | 关闭 TASK 仍须 `REPORT-*`（或合法后续 TASK）；**不得**仅用 REVIEW 代替 reciprocity |

### 9.4 禁止（继承 + 补充）

| # | 禁止 |
|---|------|
| P1–P5 | 同 3.0 规范 |
| P6 | 在下游产品文档中虚构未在 `fcop-mcp` 注册的 MCP 工具名（如 `search_history`、`move_to_history`）并声称属 FCoP 协议 |
| P7 | Agent 自行把 `needs_human` 改为 `approved`（须 `mark_human_approved`）|
| P8 | 把 `_lifecycle/review/` 阶段与 `reviews/REVIEW-*` 混为同一机制（见 §5.1）|

---

## §10 · 工具层索引（说明性 · 可随包版本演进）

**MCP 工具共 45 个**（`fcop-mcp` 3.2.4）。完整表见 [`docs/mcp-tools.md`](../docs/mcp-tools.md)。

| 类别 | 工具 |
|------|------|
| v3 生命周期 | `claim_task`, `submit_task`, `finish_task`, `approve_task`, `reject_task` |
| 历史深档案 | `archive_to_history`, `bulk_archive_to_history`, `list_history`, `read_history_task` |
| 任务 / 报告 / 问题 | `create_task` / `write_task`, `write_report`, `write_issue`, `read_*`, `list_*` |
| 治理 REVIEW | `write_review`, `list_reviews`, `read_review`, `mark_human_approved` |
| 治理告警 GAL | `fcop_list_alerts`, `fcop_create_alert` |
| 协议体检 | `fcop_audit`（产出 `shared/INSPECTION-*`，非 `reviews/`）|
| 常规归档 | `archive_task` |

完整参数与 `decision` 表见 [`docs/mcp-tools.md`](../docs/mcp-tools.md) §4–§7、§9。

**§10 为说明性**：工具名可在 MINOR 包版本中增补，但**不得**改变 §2–§5 已冻结的目录与信封语义。

---

## §11 · 迁移路径（说明性）

### 11.1 v2 → v3（一次性）

```
fcop/tasks/*     → fcop/_lifecycle/inbox/*
fcop/log/tasks/* → fcop/_lifecycle/archive/*   （并合成 transitions）
```

命令：`python -m fcop migrate --to-v3`（详见 [`fcop-3.0-spec.zh.md` §9](./fcop-3.0-spec.zh.md)）。

### 11.2 archive → history（运维性 · 可重复）

对 `_lifecycle/archive/` 中已关闭任务，按需调用 `archive_to_history(task_id)` 或 `bulk_archive_to_history(done_date=...)`。  
**不是**状态机必走一步——项目可长期只使用 `archive/`。

---

## §12 · 版本历史（规范文档）

| 规范文档版本 | 日期 | 变更摘要 |
|--------------|------|----------|
| 3.0.0 | 2026-05-21 | [`fcop-3.0-spec`](./fcop-3.0-spec.zh.md) 首发；仅 `_lifecycle/` + 事件层 |
| 3.1 | 2026-05-22 | 生命周期 MCP 五工具（[CHANGELOG §3.1.0](../CHANGELOG.md)）|
| 3.2.0 | 2026-05-22 | `history/YYYY-MM-DD/<stem>/` 深档案（[CHANGELOG §3.2.0](../CHANGELOG.md)）|
| **3.2.4** | 2026-05-27 | **本文**：合并 3.0–3.2 拓扑；纠正 workspace 根路径说明；**补全 §5 治理 REVIEW / 人工审批**；索引 45 MCP 工具 |
| **3.2.4-rev2** | 2026-05-27 | §5 扩写：`reviews/`、两种 review 消歧、`needs_human` 回路、`risk_level`、GAL 摘要 |

---

## §13 · 引用

- [ADR-0035](../adr/ADR-0035-lifecycle-directory-and-tool-layers.md) · State Ontology  
- [ADR-0036](../adr/ADR-0036-lifecycle-event-layer.md) · Event Layer（**非** history 分片）  
- [ADR-0038](../adr/ADR-0038-fcop-boundary-charter.md) · Boundary  
- [ADR-0039](../adr/ADR-0039-fcop-freeze-discipline-and-runtime-absorption-era.md) · Freeze Discipline  
- [ADR-0040](../adr/ADR-0040-canonical-one-liner-two-layer-convention.md) · Canonical 双层一句话  
- [ADR-0017](../adr/ADR-0017-review-file-type-minimal.md) · REVIEW envelope  
- [ADR-0024](../adr/ADR-0024-task-risk-level.md) · `risk_level`  
- [ADR-0025](../adr/ADR-0025-review-needs-human.md) · `needs_human`  
- [ADR-0026](../adr/ADR-0026-review-human-approval.md) · `human_approval` / `mark_human_approved`  
- [ADR-0031](../adr/ADR-0031-governance-alert-layer.md) · GAL（若存在）  
- [`docs/mcp-tools.md`](../docs/mcp-tools.md) · MCP 工具权威索引  
- [`CHANGELOG.md`](../CHANGELOG.md) · 包版本变更记录  

---

*FCoP v3 运行时规范 · 中文平行版 · 对齐 fcop@3.2.4 · 2026-05-27*
