# ADR-0015: FCoP 1.0 AI OS Protocol Charter

- **Status**: Accepted
- **Date**: 2026-05-09
- **Deciders**: ADMIN
- **Supersedes**: [ADR-0007](./ADR-0007-fcop-1.0-protocol-freeze-charter.md)（Plan B "5 字段进 1.1.0" 路线）
- **Related**: [ADR-0001](./ADR-0001-library-api.md)、[ADR-0002](./ADR-0002-package-split-and-migration.md)、[ADR-0003](./ADR-0003-stability-charter.md)、[ADR-0006](./ADR-0006-host-neutral-rule-distribution.md)；下游触发：[Issue #2](https://github.com/joinwell52-AI/FCoP/issues/2)；外部参考：[CodeFlow v2 Design §3 / §3.3.1.b / §8.0 hard rule #4](https://github.com/joinwell52-AI/codeflow-pwa/blob/main/docs/design/codeflow-v2-on-fcop-sdk.md)；本 ADR 上游 TASK：[TASK-20260509-002](../docs/agents/log/tasks/TASK-20260509-002-ADMIN-to-ME.md)

## FCoP is discovered, not invented

> 「FCoP 是 agent 的协议，我们发现了他，而不是发明；而正好人类可以读懂。」
> — ADMIN, 2026-05-09 15:09 CST

这是 charter 的第一行。后面所有内容——7 抽象、AI OS Protocol Layer 定位、四大冻结、timeline——都是**我们如何选择把观察到的形式化**，不是**我们凭空想出来的**。

三条对 v1.x 全部决策的 tiebreaker：

1. **FCoP belongs to agents, not to us.** 任何候选加进协议的东西必须先答：「agent 在共享文件系统里自由协作时，会自然做这件事吗？」答否就是**发明**，属于上层 Application 层，不属于 FCoP。
2. **Our job is observation + naming + formalization**, not design. 两个方案二选一时，tiebreaker 是「哪个有更多真实 agent run 的 field 证据」，不是「哪个理论上更漂亮」。
3. **Human readability is a bonus, not a goal.** substrate 恰好是 filesystem + Markdown，人能读——这是 FCoP 最重要的**副作用**。但**为人类可读而设计**会让 FCoP 退化回文档格式。We design for agents; humans get to watch for free.

最强的 field evidence：用户在真实 FCoP 项目（`D:\cyberv\cybervcar\docs\agents/shared/`）里观察到 agent 在**没有任何 spec 指导**的情况下自发涌现 5 类命名前缀（`GUIDE-` / `SPEC-` / `STATUS-` / `TEAM-` / `LETTER-`），全部遵守 `{ALL-CAPS-PREFIX}-{kebab-case-topic}[.{lang}].md` 这一相同 grammar。这件事在 [ADR-0021](./ADR-0021-encoding-abstraction.md) 落实为 **Open Knowledge Surface**——Encoding Abstraction 的第二面。

---

## ADMIN 决议（2026-05-09，14:01-14:34 CST）

ADR-0007（Plan B 路线）落定后约 30 分钟，ADMIN 通过 ME 转述的外部架构反馈，做出元批评：

> 「FCoP 现在最大的问题不是『不完整』，而是『协议层级混杂』。」
> 「FCoP 不应该被定义成『AI 协作规则』，而应该是『Agent Runtime Protocol』。」
> 「现在整个目标也改变了，是 ai os；那么 fcop 要有更高的高度了；必须整改！」

并通过 `AskQuestion` 5 项关键决策固化方向：

| 决策点 | 选定 | 含义 |
|---|---|---|
| FCoP 在 AI OS 栈中的位置 | **POSIX 层** | 协议层。不含 kernel、不含 host、不含 application。与 POSIX/OCI/CRD 类比 |
| AI OS 高度 vs 最小可运行平衡 | **min_kernel** | v1.0 只冻结 7 核心抽象的"最小语义"；详细字段留 v1.x |
| 文档入口重组 | **merge_strict** | 删 `fcop-standalone.md` + `fcop-primer.md`，钉一份 `docs/getting-started.md` 作 L0+L1 唯一入口 |
| ADR-0007..0014 处理 | **supersede** | 全部加 `Status: Superseded by ADR-00XX`，**不删**，保留历史决策痕迹 |
| 下一步 | **write_task** | 现在就写 TASK-20260509-002 启动整改 |

ADMIN 同时显式调和了一个张力（必须落进本 charter）：外部反馈中"FCoP 越来越像 AI OS 去人格化"是赞许，但同一段也警告"不做通用 AI OS"——这两句不矛盾。**定位升级到 AI OS 协议层 ✅；scope 仍要『最小可稳定运行』✅。**

也即：**以 AI OS 的高度定位 FCoP，但 v1.0 只交付 AI OS 协议的最小可运行内核**。本 charter 全篇按这一尺度写。

---

## Context

### 为什么 ADR-0007 必须被取代

ADR-0007（Plan B "1.0 freeze + 1.1 加 5 字段"）落定 30 分钟后，外部架构评议指出我们方案的根本盲点：

| ADR-0007 路线 | 真实盲点 |
|---|---|
| 8 ADR 全是「**对象 + 字段**」视角（Agent / Task / Review / Skill 加 schema、加字段、加 enum） | **Event Model 完全缺席**——`TASK_CREATED` / `REVIEW_REJECTED` / `SESSION_LOST` 这种事件一字未提；把"对象的当前状态"当成了协议本体，把"状态如何流转"当成了实现细节 |
| 8 ADR timeline 全是 happy path（D+3 / D+7 / D+14 一站站走） | **Failure Model 完全缺席**——Agent Timeout / Session Crash / Review Deadlock / Drift / Recovery 协议级别一字未定 |
| 4 大冻结锁了"结构层"（schema / REVIEW / 公开面 / 版本语义） | **行为层完全没冻**——也就是协议的另一半 |
| `fcop-rules.mdc`（哲学/规则）+ `fcop-protocol.mdc`（落地解释）+ `spec/fcop-spec.md`（长文）+ Python dataclass（实现）4 个抽象层平起平坐 | **协议层级未明示**——读者无法判断"哪一层是协议本体、哪一层是当前实现" |
| `fcop-mcp` 在文档里偶尔被称作"kernel" | 工程上合理，**协议层面危险**——会让 FCoP 退化为 CodeFlow 的实现细节 |
| `docs/fcop-standalone.md` 自称 standalone，内文却把读者甩到 4-7 份其他文档 | **入口层级也是混杂**——L0/L1/L2/L3 没切开 |
| `Markdown` 在 ADR-0007 中被默认为协议本体 | 但同时 ADMIN 自己承认"文件即 IPC"是体系里最原创的一刀——**这两个判断需要在 charter 里调和**，不是简单"剥离 Markdown" |

ADR-0007 不是错的，是**只覆盖了协议的一半**。本 charter 在它的基础上，把另一半（行为 + 协议层级 + 入口层级）一起冻进 v1.0。

### FCoP 在 AI OS 栈中的位置（决议 1 落地）

```
┌─────────────────────────────────────────────────────────────┐
│  Application Layer                                          │
│  CodeFlow / Cursor App / Claude Desktop / Mobile Console    │  ← 业务产品
├─────────────────────────────────────────────────────────────┤
│  Host Adapter Layer                                         │
│  fcop-mcp / fcop-claude / fcop-cli / fcop-mobile            │  ← libc 的位置
├─────────────────────────────────────────────────────────────┤
│ ★ FCoP Protocol Layer ★                                    │
│  Agent / IPC / Encoding / Event / Failure / Boundary /      │  ← POSIX 的位置
│  Audit                                                      │     这就是 FCoP
├─────────────────────────────────────────────────────────────┤
│  Reference Implementation Layer                             │
│  fcop (Python lib) — official reference impl                │  ← 协议的参考实现
├─────────────────────────────────────────────────────────────┤
│  Kernel Primitives Layer                                    │
│  LLM API / Filesystem / Process Manager / Memory Backend    │  ← AI OS 内核（未来）
└─────────────────────────────────────────────────────────────┘
```

**FCoP 是中间那条带 ★ 的线。** 不是 application、不是 kernel、不是某个 host 的 SDK、也不是 reference impl 本身。这条线决定了所有后续 ADR 的判断标准——任何"功能 X 该不该进 v1.0？"的问题，都先问"它属于这条 ★ 线吗？"。

### 7 核心抽象（决议 2 的尺度）

POSIX 把 OS 抽象成 7 件事；FCoP 必须各自对应一刀：

| POSIX | FCoP 抽象 | 0.7.x 现状 | v1.0 最小冻结内容 |
|---|---|---|---|
| 进程 Process | **Agent**（生命周期、身份） | `fcop.json` + `roles[]`，无生命周期 | Lifecycle 状态集（INIT / RUNNING / BLOCKED / SWITCHED / TERMINATED）+ 身份字段 |
| 文件系统 File | **Encoding**（filename + frontmatter + 目录） | 有，但绑死 Markdown，无抽象层 | 抽象层 vs Reference Encoding 切开；含 **IPC Surface**（强 contract：4 类 envelope）+ **Open Knowledge Surface**（弱 contract：agent-invented `{PREFIX}-{slug}.md` 在 `shared/`）两面，详见 [ADR-0021](./ADR-0021-encoding-abstraction.md) |
| IPC | **Task / Report / Issue / Review** = agent 间消息 | 有，但视作"文档"不是"消息" | Reframe 为 IPC envelope：sender / recipient / type / seq = message header |
| 信号 Signal | **Event Model** | ❌ 完全缺失 | 最小事件集（5-8 个）+ 事件 vs 文件的关系（事件 derive 还是另存为 EVENT-*.md）|
| errno | **Failure Semantics** | ❌ 完全缺失 | 失败模式枚举（Timeout / Crash / Deadlock / Drift）+ 恢复动作枚举（RETRY / RESUME / ROLLBACK / ABORT / ESCALATE）|
| 权限 Permission | **Agent Boundary**（can / cannot capability） | 部分有（rule 4 单一交接），无 capability 表达 | Boundary Schema 占位：每个 role 显式声明 can / cannot |
| 审计 syslog | **Review + Patrol Trail** | 有 REPORT；REVIEW 在 ADR-0009 待落 | REVIEW 文件类型最小 surface（不含 needs_human / human_approval —— 那俩 v1.2+） |

这 7 抽象就是 v1.0 的"最小可运行内核"。每一抽象由后续 ADR 各自落地：

| 抽象 | ADR | 类型 | 备注 |
|---|---|---|---|
| Agent | [ADR-0020](./ADR-0020-agent-boundary-and-capability.md) | 取代 ADR-0010 | 把 layer 升级为 capability bundle |
| Encoding | [ADR-0021](./ADR-0021-encoding-abstraction.md) | 新 | Markdown 降为 reference encoding；抽象层留接口 |
| IPC（4 类 envelope） | 现有 + [ADR-0017](./ADR-0017-review-file-type-minimal.md) | 含 ADR-0009 reframe | TASK / REPORT / ISSUE 已稳定；REVIEW 由 0017 收口 |
| Event | [ADR-0018](./ADR-0018-event-model.md) | 新 | 协议本体最关键缺失 |
| Failure | [ADR-0019](./ADR-0019-failure-and-recovery-semantics.md) | 新 | 协议本体次关键缺失 |
| Boundary | [ADR-0020](./ADR-0020-agent-boundary-and-capability.md) | 同 Agent | 与 Agent capability 同 schema |
| Audit | [ADR-0017](./ADR-0017-review-file-type-minimal.md) | 取代 ADR-0009 | REVIEW 最小 surface，砍膨胀 |
| 全协议 schema 形式化 | [ADR-0016](./ADR-0016-json-schema-for-7-abstractions.md) | 取代 ADR-0008 | 7 抽象的 JSON Schema |

### 与 CodeFlow §8.0 hard rule #4 + §3.3.1.b 的契约

> 「协议演进唯一合法仓库 = `D:\FCoP` / `joinwell52-AI/FCoP`。任何"v2 想要但 FCoP 没有"的字段需求 → 必须先去 `D:\FCoP` 提 Issue / PR。」 —— CodeFlow §8.0 #4

本 charter 把 [Issue #2](https://github.com/joinwell52-AI/FCoP/issues/2) 提的 5 字段需求**重新分配**：

| Issue #2 字段 | ADR-0007 路线 | ADR-0015 路线 |
|---|---|---|
| `Agent.layer` | ADR-0010（v1.1.0）| **进 ADR-0020（v1.0.0）**——升级为 Agent Boundary & Capability，作为 7 抽象之一 |
| `Task.risk_level` | ADR-0011（v1.1.0）| **延后到 v1.1+**——属于 Risk Policy（Layer 3 Governance），不是协议本体；v1.0 不做 |
| `Review.decision = needs_human` | ADR-0012（v1.1.0）| **延后到 v1.2+**——REVIEW v1.0 仅最小 surface；needs_human / human_approval 推到 Audit 抽象成熟后再加 |
| `Review.human_approval` | ADR-0013（v1.1.0）| **延后到 v1.2+**——同上 |
| `Skill.tools[]` 风险元数据 | ADR-0014（v1.1.0）| **延后到 v1.1+**——Skill 是 Encoding 的扩展（特定文件类型），不是协议本体；v1.0 不做 |

CodeFlow 那边的影响：5 字段中只有 1 个（`Agent.layer` → Boundary）进 v1.0；其他 4 个推后。需要在 Issue #2 上发后续 comment 通知（不属于本 charter 范围；由后续 TASK 在 v1.0 ship 前完成）。CodeFlow S2-S6 sprint 的 interim option：**继续 pin `fcop>=0.7.2,<1.0`**，等 v1.0 ship 后再升。

---

## Decision

### 核心决策

**FCoP 1.0 = AI OS Protocol 的最小可运行内核（POSIX 层 minimum-viable kernel）。**

具体含义：

1. **定位**：FCoP 是 AI OS 栈中的协议层（POSIX 类比）。不是 AI 协作规则、不是 prompt engineering 模板、不是 workflow 引擎。
2. **Scope**：v1.0 只冻结 7 核心抽象的**最小语义**——每抽象都有"协议级 contract"，但具体字段集、policy 表、详细 enforcement 留给 v1.1+ / v1.2+ 各自的 minor。
3. **结构**：FCoP 协议本体不绑定具体 host（Cursor / Claude / CLI / mobile）、不绑定具体 encoding（Markdown 是 v1.0 reference encoding，但抽象层为未来 JSON / SQLite / event stream 留接口）。
4. **行为**：v1.0 必须给出 Event Model 与 Failure Model 的协议级 contract——这是协议从"静态文档系统"变"真正 Runtime"的临界点。

### v1.0 的「四大冻结」（升级 ADR-0007 §四大冻结）

| # | 冻结 | 取代 ADR-0007 哪一项 | 关键 ADR |
|---|---|---|---|
| 1 | **7 核心抽象的最小契约** | 取代"4 大冻结 #1 JSON Schema" + #2 REVIEW + #3 公开面"——实质上把它们合并成 7 抽象的统一冻结 | 0016（schema 形式化）+ 0017（REVIEW）+ 0018（Event）+ 0019（Failure）+ 0020（Boundary）+ 0021（Encoding） |
| 2 | **协议层级宪章** | 新增（ADR-0007 没冻这个）| 本 ADR §FCoP 在 AI OS 栈中的位置 + §术语表（见下） |
| 3 | **Reference Encoding 概念** | 新增（ADR-0007 默认 Markdown = 协议本体）| ADR-0021 |
| 4 | **版本号语义 1.x lock** | 保留 ADR-0007 §冻结 #4 不变 | 本 ADR §Design Details |

### 术语表（v1.0 永久冻结）

下面 5 个术语是 FCoP 1.x 文档与代码必须使用的标准措辞：

| 术语 | 定义 | 不要再说 |
|---|---|---|
| **FCoP Protocol** | 抽象规约。含 7 核心抽象、Encoding 抽象、跨语言契约。语言/host/encoding 中立 | "FCoP 协议" 与 "FCoP 库" 混用 |
| **FCoP Reference Implementation** | 协议的参考实现。当前唯一为 `fcop` Python 库 | "FCoP" 单独指代库 |
| **FCoP Host Adapter** | 把 FCoP 接到具体 host 的适配器。当前为 `fcop-mcp`（Cursor MCP 适配器）；将来可能有 `fcop-claude` / `fcop-cli` / `fcop-mobile` | "fcop-mcp 是 kernel" / "fcop-mcp 是 FCoP 本身" |
| **FCoP Reference Encoding** | 协议的参考编码。v1.0 唯一为 filename + Markdown frontmatter + filesystem layout | "Markdown 是 FCoP 协议的一部分" |
| **AI OS Protocol Layer** | FCoP 在 AI OS 栈中的角色。等价于 POSIX 在 Unix 中的位置 | "FCoP 是 AI 协作规则" |

任何 v1.x 文档（含 README / spec / mdc / homepage）都必须按这套术语写。Reviewer 在 PR 审查时按此 enforce。

**包族命名约定（v1.0 锁定）**：

- **FCoP Reference Implementation**：Python 生态命名 `fcop`（一份；跨语言 reference impl 不计划——下游 mirror 由各自仓维护，FCoP 上游只保证 Python `fcop` + `spec/schemas/*.schema.json` 是真相）
- **FCoP Host Adapter**：
  - Python 生态：PyPI 命名 `fcop-{host}`（已发：`fcop-mcp`；未来候选：`fcop-cli`）
  - 非 Python 生态：用宿主生态包名约定（npm: `@fcop/{host}`；Maven: `dev.fcop.{host}`；Swift Package / 其他亦然）
  - 所有 Host Adapter 都必须遵守 `spec/schemas/*.schema.json` 协议契约，否则不承认是 FCoP 兼容实现

### 落地节奏（取代 ADR-0007 timeline）

| 时间窗 | 产出 | commit 颗粒度 |
|---|---|---|
| **D0**（今天 2026-05-09）| TASK-002 + ADR-0015 charter + ADR-0016/0017/0020 reframe 大纲 + ADR-0018/0019/0021 新增大纲 + 旧 ADR Status 更新 + release notes 重写 + getting-started.md + 文档入口重组 + README/homepage framing 升级 + mdc description 升级 + REPORT-002 | 5-6 commits |
| D+3 ~ D+7 | ADR-0016..0021 各自完整稿 + 各自 PR | 每 ADR 1 commit |
| D+14 ~ D+21 | reference impl 开工：Event Loop / Failure Handling / Boundary 校验 / Encoding 抽象层 | 多 commit |
| D+28 ~ D+35 | reference impl 完成；CI / 测试 / 文档同步 | 多 commit |
| **D+42 ~ D+56**（2026-06-20 ~ 2026-07-04）| **`fcop@1.0.0` + `fcop-mcp@1.0.0` 上 PyPI** | tag + GitHub Release |

每个里程碑允许 ±5 天浮动。任何超过 10 天的延期触发"重新评估"。

---

## Design Details

### 7 核心抽象的最小语义边界

每个抽象在 v1.0 必须冻什么、必须**不**冻什么——避免实现阶段 scope creep：

#### 抽象 1 · Agent

| 必冻 | 不冻 |
|---|---|
| Lifecycle 5 状态：INIT / RUNNING / BLOCKED / SWITCHED / TERMINATED | 详细 transition rule（哪些状态间能直接跳转） |
| 身份字段：`code` / `label` / `team` | 详细 capability ACL 表（v1.1 做） |
| 状态留痕约定：状态变化必须落文件（不能只在内存）| state-event mapping（ADR-0018 做） |

#### 抽象 2 · Encoding

| 必冻 | 不冻 |
|---|---|
| 抽象层 contract：4 类 IPC envelope（sender/recipient/type/seq）+ frontmatter 必填字段 | JSON / SQLite / event stream 替代实现（v1.x） |
| Reference Encoding：Markdown frontmatter + filename grammar = v1.0 唯一推荐 | Markdown 字段集详细 enum（已有 ADR-0008 reframe 进 ADR-0016） |
| `_data/` vs `.cursor/rules/` 关系：`_data/` 是真本，`.cursor/rules/` 是 deployed copy（ADR-0006 既定）| 第三方 host 怎么 deploy（host adapter 各自决定）|

#### 抽象 3 · IPC（4 类 envelope）

| 必冻 | 不冻 |
|---|---|
| 4 类：TASK / REPORT / ISSUE / REVIEW（REVIEW 由 ADR-0017 收口） | enforce 谁能写哪类（部分由 ADR-0020 Boundary 决定）|
| filename grammar：现有 TASK/REPORT/ISSUE 已稳定 + REVIEW 新加 | 新增第 5 类 envelope（v1.x 之后再说）|
| frontmatter 必填字段：`protocol` / `version` / `sender` / `recipient` / `priority` / `subject` | optional 字段 enum（部分留 v1.1）|

#### 抽象 4 · Event Model（详见 ADR-0018）

| 必冻 | 不冻 |
|---|---|
| 最小事件集（5-8 个）：TASK_CREATED / TASK_ACCEPTED / TASK_BLOCKED / REPORT_FILED / REVIEW_DECIDED / SESSION_LOST / ROLE_SWITCHED 等（最终集合在 ADR-0018 拍板）| 完整事件集（v1.x 持续扩） |
| 事件 vs 文件关系：事件**派生**自文件状态变化，不另存为 EVENT-*.md（v1.0 决定）| event log 文件类型 EVENT-*.md（如 v1.x 需要再加）|
| 事件订阅 contract（host adapter 必须暴露 subscribe API） | 具体 transport（pubsub / polling / file watcher 由 host 决定）|

#### 抽象 5 · Failure Semantics（详见 ADR-0019）

| 必冻 | 不冻 |
|---|---|
| 失败模式枚举：TIMEOUT / CRASH / DEADLOCK / DRIFT | 详细诊断 metric（v1.1）|
| 恢复动作枚举：RETRY / RESUME / ROLLBACK / ABORT / ESCALATE | 详细 retry policy（指数退避 etc，留 host adapter）|
| Session 恢复 hook：`Project.recover_session()` API 占位 | 完整 Session schema（v1.x；v1.0 仅最小 hook） |

#### 抽象 6 · Agent Boundary（详见 ADR-0020）

| 必冻 | 不冻 |
|---|---|
| Boundary Schema 占位字段：`can: list[str]` / `cannot: list[str]` 在 `roles[i]` 上 | 详细 capability 词表（v1.1 build out）|
| layer 概念升级：layer = capability bundle 的简写（worker = 默认 can=[file_io,task_io]，governance = + can=[review_decision]，admin = + can=[escalate,override]）| 用户自定义 capability bundle（v1.1）|
| enforcement hook：`Project.write_task` 调用前必须经 boundary check | 跨 host 同步 capability ACL（v1.x）|

#### 抽象 7 · Audit（详见 ADR-0017）

| 必冻 | 不冻 |
|---|---|
| REVIEW 文件类型 minimal surface：filename grammar + 4 个最小 decision enum（approved / rejected / needs_changes / abstained） | needs_human enum 值（推 v1.2）|
| `Project.write_review() / read_review() / list_reviews() / archive_review()` API | `mark_human_approved()` API（推 v1.2）|
| Patrol trail：plain text log 由 host adapter 各自实现 | 协议级 patrol schema（不做）|

### 协议层级宪章（决议 4 落地）

v1.0 在文件层面**已经切了**的 vs **必须再切的**：

| 层 | 已切 | 还需切 |
|---|---|---|
| Layer 1 Core Principles（哲学）| 部分（fcop-rules.mdc 0.a/0.b/0.c）| Layer 1 与 Layer 2 在同一份 rules.mdc 里——v1.x 再分（v1.0 不动正文）|
| Layer 2 Runtime Protocol（协议本体）| 部分（fcop-rules.mdc 1-7）| Event / Failure / Boundary 三个抽象当前完全没载体——由 ADR-0018/0019/0020 各自落 |
| Layer 3 Governance Policy（策略）| ❌ 无独立载体 | v1.0 仍不切（避免膨胀）；ADR-0017 把 needs_human 推延到 v1.2 是这一层尚未抽离的标志 |
| Layer 4 Implementation（实现细节）| 部分（fcop-protocol.mdc 已经主要承担这层）| 不动 |

**v1.0 切出 2 层（Protocol vs Implementation）**——通过术语表与 ADR-0021（Encoding Abstraction）实现。Layer 1 与 Layer 3 留 v1.x。这是决议 2 (min_kernel) 的具体兑现。

### 跨语言契约（与 CodeFlow TS mirror 的协同）

```
本仓 (spec/schemas/*.schema.json + spec 文档) ── single source of truth ──► CodeFlow TS schema
                                              ◄────── fuzz test enforce ──
```

Charter 级承诺：

1. 本仓发版 → CHANGELOG 列出 7 抽象任何 schema 变化
2. CodeFlow 同 minor 跟随
3. CodeFlow 仓 CI 跑跨语言 fuzz 测试
4. 任何 schema 偏离 → CodeFlow 侧 build fail，强制走 §3.3.1.b 5 步流程

### 文档入口重组（决议 3 落地）

由后续步骤实施（不在本 charter 范围）；但 charter 必须明示**新入口结构**：

| 层 | 文件 | 角色 |
|---|---|---|
| L0 + L1 入口 | `docs/getting-started.md` | 30 秒 framing + 5 分钟跑起来；唯一入口 |
| L2 规范 | `spec/fcop-runtime-protocol-v1.0.md`（v1.0 ship 时取代 `spec/fcop-spec-v1.0.3.md`）| 长文 spec |
| L2 规约 | `.cursor/rules/fcop-rules.mdc` + `fcop-protocol.mdc` | Agent 必读 |
| L3 故事 | `essays/` | 现场报告 |
| 导航 | `README.md` / `README.zh.md` / `docs/index.html` | 纯导航，不重复内容 |

`docs/fcop-standalone.md` / `docs/fcop-standalone.en.md` / `primer/fcop-primer.md` 全部删/归档。

---

## Non-Goals

- **不做 Kernel**：FCoP 是 POSIX 层，不是 Linux Kernel。Task Scheduler / Event Loop / State Machine 是 reference impl 的事，不是协议本体。
- **不做完整 AI OS**：v1.0 不引入 Multi-node / AI Consensus / Memory Backend / Skill Marketplace 等"OS 应用层"概念。这些**可能永远不在 FCoP 范围**——它们是 Application 层的事。
- **不做 Layer 3 Governance Policy 抽离**：risk_level / human_approval 等 policy-level 概念延后到 v1.2+。v1.0 只保留 Governance Hook（让 host adapter 决定如何处理 high-risk 动作），不写策略本体。
- **不做 Mobile / Cloud host adapter 设计**：v1.0 仅明示 Host Adapter 概念存在；具体 mobile/cloud adapter 由 v2+ 排期。
- **不动 0.7.x release notes / CHANGELOG 历史段落**：保持历史不可变。
- **不动 Python 实现代码**（在本 charter 落定的 D0 这一天）：本 charter 只产文档与 ADR；reference impl 由后续每个 ADR 各自的 PR 落地。**Carve-out**：[ADR-0022](./ADR-0022-workspace-directory-convention.md) 决定的 `fcop migrate-workspace` 命令是 v1.0 必交付物（不能让 0.7.x 用户手工迁移），由 ADR-0022 §Timeline 排期，不属本 charter "不动实现"承诺范围。
- **不在 1.x 触碰 `core/schema.PROTOCOL_VERSION` 整数**：它仅代表 frontmatter on-disk format 的破坏性升级。
- **不发 0.8 / 0.9 中转版本**：直接 0.7.2 → 1.0.0。
- **不强求 v1.0 把 layer 1 vs layer 2 切开**：rules.mdc 正文 v1.0 不动。

---

## Alternatives Considered

### Alt-A：维持 ADR-0007 Plan B 路线（5 字段进 1.1.0）

**否决原因**：
- Event Model / Failure Model 完全缺失——协议非真 Runtime
- 8 ADR 全是字段视角——把"对象状态"当协议本体，错配
- 没有协议层级宪章——`fcop-mcp = kernel` 危险表述无法纠正
- 文档入口混杂问题没解决——standalone.md 还是不 standalone
- ADMIN 已明确"必须整改"——继续 ADR-0007 路线 = 违背决议

### Alt-B：直接做 K8s 级完整 AI OS

把 Multi-node / Consensus / Memory Backend / Skill Marketplace / Audit Board 等全塞进 v1.0。

**否决原因**：
- 外部架构反馈明确警告"不做通用 AI OS"
- v1.0 必须"最小可稳定运行"——k8s-isation 违反 min_kernel 决议
- timeline 会从 D+42~56 推到 D+180+（6+ 个月）
- 大部分功能属于 Application 层，不属于协议层
- Docker 1.0 也不是从 K8s 抽象层级起手的——这是历史教训

### Alt-C：4 层架构图 v1.0 直接到位（Core Principles / Runtime Protocol / Governance Policy / Implementation 全切开）

**否决原因**：
- v1.0 上来就 4 层 = over-engineering
- Principles vs Protocol 的切分要等 Event Model 落地后才有 ground truth 可分
- Governance Policy 独立载体在 v1.0 阶段没有真用例（needs_human / human_approval 已延后到 v1.2）
- 渐进路径更稳：v1.0 切 2 层（Protocol vs Implementation） → v1.x 切 3 层（+ Principles 独立） → v2 切 4 层（+ Governance 独立）

### Alt-D：跳过 1.0，直接 0.7.2 → 1.1.0

按 Issue #2 字面字段实施。

**否决原因**：同 ADR-0007 §Alternatives Alt-D（违反 semver、没有 freeze 锚点、跨语言 mirror 跑不通）。本 charter 继承该否决。

### Alt-E：仅升级 framing（README/homepage 改"AI OS Protocol"措辞），不动 ADR/spec

**否决原因**：
- 等于"换个标语"——ADMIN 明确说"必须整改"
- Event Model / Failure Model 缺失没解决——协议本体仍然不完整
- 外部期望与协议实质背离——下游 adopter 会发现"挂的招牌和实际能力不符"

---

## Consequences

### Positive

- **POSIX 时刻**：FCoP 第一次有"机器可读、跨语言可 mirror、被 fuzz test enforce、含 Event/Failure 协议级 contract"的 spec。这是从"良好实践"升级为"真正 Runtime Protocol"的临界点
- **外部期望升级**：v1.0 ship 后 FCoP 自动获得"AI OS 协议层"的学术与工程声誉等级
- **CodeFlow §3.3.1.b 流程首例**：本 charter + 后续 6 个 ADR + reference impl + spec 同步 = 5 步流程的完整 reference run
- **协议演进路径模板**：未来任何"v2 想要但 FCoP 没有"的字段都按本次 ADR-0015..0021 的模板走
- **下游 adopter 增长**：AI OS Protocol Layer 的定位让其他 host（Claude Desktop / CLI / Mobile）adapter 团队有清晰对接面
- **昨天 8 份 ADR 的工作不浪费**：ADR-0007/0008/0009 的内容被 0015/0016/0017 reframe 复用；ADR-0010 的 layer 字段进 ADR-0020 的 Boundary

### Negative

- **timeline 推迟 28-42 天**：从 D+14 推到 D+42 ~ D+56。CodeFlow S2-S6 sprint 必须接受 interim option（继续 pin `<1.0`）
- **v1.0 增加一处 workspace breaking change**：默认工作区目录从 `docs/agents/` 改为顶层 `fcop/`（[ADR-0022](./ADR-0022-workspace-directory-convention.md)）。配 `fcop migrate-workspace` 自动迁移工具 + detect 旧布局打 warning，**不报错**。0.7.x 用户升级体验：第一次跑得 warning，需手工运行迁移命令（或显式传 `workspace_dir="docs/agents/"`）。所有教程文档 / essay / forum post 中的 `docs/agents/` 路径示例都要改
- **文档面 15+ 份要动**：README / homepage / 4 份 mdc / spec / standalone / primer / getting-started / release notes 等。文档同步成本是工程量大头
- **外部期望永久绑死**：一旦挂"AI OS Protocol"招牌，任何 1.x 内的 schema 变动都不能 break 1.0.0 用户。等同 POSIX 级稳定性压力
- **Issue #2 5 字段中 4 个推后**：CodeFlow 那边可能需要在 v1.1 / v1.2 跨多个 minor 才能拿全字段
- **Layer 1 Core Principles 与 Layer 2 Runtime Protocol 在 rules.mdc 仍然混着**：v1.0 决议不动；外部反馈"哲学和规则混"的批评在 v1.0 内部分残留
- **`core/schema.py` 的 dataclass 与 `spec/schemas/*.schema.json` 双源真相风险**：由 ADR-0016 解决；v1.0 ship 必须有对照测试

### Neutral

- **不影响 Zenodo DOI**：DOI 是 research snapshot 时点引用；v1.0 / v1.1 发版可以再发 DOI（可选）
- **不影响 `fcop-rules` / `fcop-protocol` 版本号**：v1.0 仅顶部 description 升级，正文不动；rules version / protocol version 不 bump
- **不影响 `core/schema.PROTOCOL_VERSION` 整数**：它只代表 frontmatter on-disk format 破坏；7 抽象冻结都是 additive，不破坏
- **不影响 fcop / fcop-mcp lockstep MINOR 约定**（ADR-0003 既定）

---

## Timeline

| 日期 | 里程碑 | 产出 |
|---|---|---|
| **2026-05-09**（D0）| 整改"宪法"完成 | TASK-002 + ADR-0015 + ADR-0016..0021 大纲 + 旧 ADR Status 更新 + release notes 重写 + getting-started.md + 文档入口重组 + README/homepage framing 升级 + mdc description 升级 + REPORT-002 |
| 2026-05-12 (D+3) | ADR-0016 完整稿 + PR | spec/schemas/ 7 抽象的 JSON Schema 落地 |
| 2026-05-15 (D+6) | ADR-0017 完整稿 + PR | REVIEW 文件类型最小 surface |
| 2026-05-18 (D+9) | ADR-0018 完整稿 + PR | Event Model 最小事件集 |
| 2026-05-22 (D+13) | ADR-0019 完整稿 + PR | Failure & Recovery Semantics |
| 2026-05-25 (D+16) | ADR-0020 完整稿 + PR | Agent Boundary & Capability |
| 2026-05-28 (D+19) | ADR-0021 完整稿 + PR | Encoding Abstraction |
| 2026-06-04 (D+26) | reference impl 50% | Event Loop / Failure handler |
| 2026-06-13 (D+35) | reference impl 100% + CI / 测试 / 文档同步 | 全绿 |
| **2026-06-20 (D+42) ~ 2026-07-04 (D+56)** | **`fcop@1.0.0` + `fcop-mcp@1.0.0` 上 PyPI** | docs/releases/1.0.0.md final + GitHub Release + CHANGELOG `[1.0.0]` + MIGRATION-1.0.md |

每个里程碑允许 ±5 天浮动。任何超过 10 天的延期触发"重新评估"——由后续 TASK 决定调整路线还是延长 timeline。

v1.1 / v1.2 timeline 不在本 charter 范围；由 ADR-0017 / 0020 / 0021 收口后再单独 charter。

---

## Sign-off

- **ADMIN**：已批准（2026-05-09 14:01-14:34 CST，AskQuestion 5 项决策全部 buy 推荐方案）
- **ME**：负责执行；REPORT-20260509-002-ME-to-ADMIN.md 在 13 步全部完成后签字

---

_Last edited: 2026-05-09. Status changes go in the table at the top; body content is frozen per ADR convention._
