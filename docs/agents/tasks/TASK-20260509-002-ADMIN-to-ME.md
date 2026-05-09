---
protocol: fcop
version: 1
sender: ADMIN
recipient: ME
priority: P0
subject: FCoP 1.0 framing 升级为 AI OS Protocol — 整改 ADR-0007..0014 + 文档入口重组
---

## 背景

[TASK-20260509-001](../log/tasks/TASK-20260509-001-ADMIN-to-ME.md) 落定 8 ADR roadmap
后约 30 分钟，ADMIN 在 5/9 1:25-2:16 PM CST 的对话里抛出**对刚 commit 路线本身的元批评**：

> 「FCoP 现在最大的问题不是『不完整』，而是『协议层级混杂』。」
> 「FCoP 不应该被定义成『AI 协作规则』，而应该是『Agent Runtime Protocol』。」
> 「现在整个目标也改变了，是 ai os；那么 fcop 要有更高的高度了；必须整改！」

ADMIN 在 `AskQuestion` 5 项关键决策里全部选定推荐方案：

| 决策点 | 选定 | 含义 |
|---|---|---|
| FCoP 在 AI OS 栈中的位置 | **POSIX 层** | 协议层。不含 kernel、不含 host。与 POSIX/OCI/CRD 类比 |
| AI OS 高度 vs 最小可运行平衡 | **min_kernel** | v1.0 只冻结 7 核心抽象的"最小语义"；详细字段留 v1.x |
| 文档入口重组 | **merge_strict** | 删 `fcop-standalone.md` + `fcop-primer.md`，钉一份 `docs/getting-started.md` 作 L0+L1 唯一入口 |
| 昨天 ADR-0007..0014 的处理 | **supersede** | 全部加 `Status: Superseded by ADR-00XX`，**不删**，保留历史决策痕迹 |
| 下一步 | **write_task** | 现在就按上述 4 项决议写 TASK-002，启动整改 |

ADMIN 同时显式调和了一个张力（必须落进 charter）：

> Plan-mode 朋友的两段建议里，"AI OS"作为**长期定位**是对的，但同一段也警告"不做通用 AI OS"——
> 这两句不是矛盾。**定位升级到 AI OS 协议层 ✅；scope 仍要『最小可稳定运行』✅。**

也即：以 AI OS 的高度定位 FCoP，但 v1.0 只交付 AI OS 协议的**最小可运行内核**。

### 触发本 TASK 的具体观察链

| 观察 | 来自 |
|---|---|
| Event Model / Failure Model 完全缺席 | ADMIN 转的朋友建议第二段，"5 类 Schema 是静态结构 vs Event-driven State Protocol" |
| Markdown 绑定过深 vs 文件即 IPC 是原创性所在 | 朋友建议第一段 + 第二段（看似矛盾，调和方案见 §决策） |
| Review 在膨胀成"神" | 朋友建议第二段 |
| `fcop-mcp = kernel` 表述危险 | 朋友建议第二段 |
| 协议层级混杂（哲学/规则/Runtime/Prompt 混） | 朋友建议第一段 |
| `fcop-standalone.md` 不 standalone（内文要去翻 4-7 份其他文档） | ADMIN 直接指出 |
| `_data/` vs `.cursor/rules/` 哪个 source-of-truth 在 standalone 里没说清 | ME 探索发现 |

## ADMIN 决议（5 项）

详见 §背景表格。本节展开为执行约束：

### 决议 1：FCoP 是 AI OS 的 **POSIX 层**（协议层）

实操含义：

- FCoP **不**包含 Kernel（Task Scheduler / Event Loop / State Machine 是 reference impl 的事，不是协议本体）
- FCoP **不**包含 Host（fcop-mcp / fcop-claude / fcop-cli 是 Host Adapter，类比 libc）
- FCoP **不**包含 Application（CodeFlow / Cursor / Claude Desktop 是用户态产品）
- FCoP **就是**协议层：定义 7 核心抽象（Agent / IPC / Encoding / Event / Failure / Boundary / Audit）的契约
- 类比谱系：POSIX → Unix/Linux；OCI → Docker；CRD → K8s；**FCoP → AI OS**

### 决议 2：v1.0 = "最小可稳定运行协议"

只冻结 **7 核心抽象的最小语义**：

| 抽象 | v1.0 最小冻结内容 | 留给 v1.x |
|---|---|---|
| Agent | Lifecycle 状态集 + 身份字段 | layer / capability 详细 |
| IPC（Task/Report/Issue/Review） | 4 类 envelope 的最小字段 + filename grammar | risk_level enforce / human approval |
| Encoding | Markdown 是 reference encoding；抽象层 vs 实现层切开 | JSON / SQLite / event stream 替代 |
| Event | 最小事件集（5-8 个）+ 事件 vs 文件的关系 | event log 文件类型、replay |
| Failure | 失败模式枚举 + 恢复动作枚举 | session 完整恢复语义 |
| Boundary | can / cannot capability schema 占位 | role-based ACL |
| Audit | REVIEW 文件类型最小 surface | needs_human / human_approval（v1.2+） |

### 决议 3：文档入口 merge_strict

- **删**：`docs/fcop-standalone.md` + `docs/fcop-standalone.en.md` + `primer/fcop-primer.md`（归档到 `primer/_archived/`）
- **新建**：`docs/getting-started.md` 作 L0+L1 唯一入口（30 秒 framing + 5 分钟跑起来）
- **保留 reframe**：`spec/fcop-spec-v1.0.3.md` → 在 v1.0 ship 时取代为 `spec/fcop-runtime-protocol-v1.0.md`（书名直接表达 AI OS 协议层身份）
- **README.md / README.zh.md / docs/index.html homepage**：第一段 framing 改写为 "Agent Runtime Protocol — the AI OS protocol layer"；不再重复内容，作纯导航
- **`fcop-rules.mdc` / `fcop-protocol.mdc`**：顶部 description 字段加一句 "FCoP is the AI OS protocol layer"；正文不动（已经几乎全是 host-neutral runtime 内容）

### 决议 4：昨天 ADR 处理 = supersede（不删）

ADR 编号永不复用；新编号取代旧编号：

| 旧 | 新 | 处理 |
|---|---|---|
| ADR-0007（FCoP 1.0 Protocol Freeze Charter） | **ADR-0015**（FCoP 1.0 AI OS Protocol Charter） | Superseded by ADR-0015 |
| ADR-0008（JSON Schema spec） | **ADR-0016**（JSON Schema for 7 Core Abstractions，reframe） | Superseded by ADR-0016 |
| ADR-0009（REVIEW file type） | **ADR-0017**（REVIEW File Type，minimal v1.0 surface） | Superseded by ADR-0017 |
| ADR-0010（Agent.layer field） | **ADR-0020**（Agent Boundary & Capability，扩为 boundary） | Superseded by ADR-0020 |
| ADR-0011（Task.risk_level） | （延后） | Status: Deferred to v1.1+ |
| ADR-0012（Review.decision needs_human） | （延后） | Status: Deferred to v1.2+ |
| ADR-0013（Review.human_approval） | （延后） | Status: Deferred to v1.2+ |
| ADR-0014（Skill.tools[] risk metadata） | （延后） | Status: Deferred to v1.1+ |
| — | **ADR-0018**（Event Model） | 新增 |
| — | **ADR-0019**（Failure & Recovery Semantics） | 新增 |
| — | **ADR-0021**（Encoding Abstraction） | 新增 |

旧 ADR 文件**保留在仓里**——ADR 是隶点不可变原则；只在 Status 行注明 Superseded/Deferred 与指向。

### 决议 5：现在就按上面 4 项写 TASK-002（本文）→ 启动整改

不再做"Plan 模式细化"前置——上面 5 项已经把方向锁死，直接进入执行。

## 整改执行计划（13 步）

| # | 动作 | 输出文件 |
|---|---|---|
| 1 | 写 TASK-002（本文） | `docs/agents/tasks/TASK-20260509-002-ADMIN-to-ME.md` |
| 2 | commit + push TASK-002 | git |
| 3 | 写 ADR-0015 charter（重，~300 行）| `adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md` |
| 4 | 写 ADR-0016 / 0017 / 0020 草稿大纲（reframe 版）| 3 份 |
| 5 | 写 ADR-0018 / 0019 / 0021 草稿大纲（新增）| 3 份 |
| 6 | ADR-0007..0010 加 Status: Superseded；ADR-0011..0014 加 Status: Deferred；adr/README.md 索引同步 | 8 份小改 + 1 份索引 |
| 7 | 重写 docs/releases/1.0.0.md / 1.1.0.md 大纲（AI OS Protocol 叙事）| 2 份 |
| 8 | 创建 docs/getting-started.md（合并 standalone + primer 内容）| 1 份 |
| 9 | 删 fcop-standalone.md / fcop-standalone.en.md；归档 primer/fcop-primer.md | 文件操作 |
| 10 | README.md / README.zh.md framing 段改写 | 2 份 |
| 11 | docs/index.html homepage Hero/What 段改写 + EN/ZH 同步 | 1 份 |
| 12 | src/fcop/rules/_data/*.mdc 顶部 description 升级 + sync 到 .cursor/rules/ | 4 份（2 真本 + 2 副本）|
| 13 | 写 REPORT-002 + 归档 TASK-002 + final commit + push | git |

执行节奏：13 步可在多轮回复内完成；不强求一轮交付完。每个里程碑（步骤 6 / 9 / 12）独立 commit，便于 git 历史查阅。

## ADR-0015 charter 核心轮廓预览（执行步骤 3 的纲要）

| § | 内容 |
|---|---|
| Status | Accepted（ADMIN 当面拍板） |
| Context | 引 TASK-002 §背景 + 引朋友建议两段 + 引 §决议张力调和 |
| Decision | 5 项 ADMIN 决议固化 + 7 核心抽象表 + 4 层架构图 |
| Design Details | 4 层架构图 + 7 抽象逐项最小语义 + Reference Encoding 概念 + 跨语言契约（与 CodeFlow TS mirror）|
| Non-Goals | 不做 Kernel；不做完整 OS；不在 v1.0 做 needs_human / human_approval / Skill 等延后项 |
| Alternatives | A：维持 ADR-0007 路线（5 字段 schema），否决理由：Event/Failure 缺失致协议非真 Runtime；B：直接做 K8s 级完整 AI OS，否决理由：朋友警告"不做通用 AI OS"；C：4 层架构图 v1.0 直接到位，否决理由：over-engineering，2 层渐进更稳 |
| Consequences | Positive（POSIX 时刻、外部期望升级、CodeFlow §3.3.1.b 流程首例）、Negative（timeline 推到 D+42 ~ D+56、文档面 15+ 份要动、外部期望永久绑死）、Neutral（不影响 Zenodo DOI、不影响 fcop-rules 版本号）|
| Timeline | D+0 起步 → D+7 ADR-0015..0021 全部完整稿 → D+14 reference impl 开工 → **D+42 ~ D+56 fcop@1.0.0 上 PyPI** → 之后 v1.1 / v1.2 节奏由后续 ADR 决定 |
| Sign-off | ADMIN 已批准 |

## 验收标准

- [ ] 步骤 1：本 TASK 文件存在 ✅（写完即勾）
- [ ] 步骤 2：TASK-002 commit + push 成功
- [ ] 步骤 3：ADR-0015 charter 完整稿 Status: Accepted
- [ ] 步骤 4-5：ADR-0016..0021 共 6 份草稿大纲存在，全部 Status: Proposed
- [ ] 步骤 6：ADR-0007..0014 状态全部更新；adr/README.md 索引含 ADR-0015..0021
- [ ] 步骤 7：docs/releases/1.0.0.md / 1.1.0.md 重写大纲存在，narrative 升级为 AI OS Protocol
- [ ] 步骤 8：docs/getting-started.md 存在，内容覆盖 L0（30s framing）+ L1（5min 跑起来）
- [ ] 步骤 9：docs/fcop-standalone.md / fcop-standalone.en.md 已删；primer/fcop-primer.md 已归档
- [ ] 步骤 10：README.md / README.zh.md 第一段 framing 段含 "Agent Runtime Protocol" / "AI OS protocol layer"
- [ ] 步骤 11：docs/index.html Hero + What is FCoP 段含新 framing；EN/ZH 同步
- [ ] 步骤 12：4 份 mdc description 升级；.cursor/rules/ 副本与 _data/ 真本一致
- [ ] 步骤 13：REPORT-002 写完，TASK-002 归档到 log/tasks/，final commit + push

## 风险与边界

1. **scope creep**：朋友建议里有 11 条具体批评（layer 分离、Markdown 解耦、Event Model、Failure Model、Risk Model、Boundary、各种 enforce）—— v1.0 只接 ADR-0015..0021 这 7 份的内容；其余进 v1.x 排期。
2. **timeline 推迟**：v1.0 ship 从 D+14 推到 D+42 ~ D+56（28-42 天延期）。CodeFlow 那边的 S2-S6 sprint 可能等不起 → ADR-0015 §Consequences 必须有"interim option：CodeFlow 继续 pin `fcop>=0.7.2,<1.0`，1.0 ship 后再升"。
3. **外部期望永久绑死**：一旦 1.0 挂出 "AI OS Protocol" 招牌，向后兼容压力等同 POSIX。任何 1.x 内的 schema 变动都不能 break 1.0.0 用户。ADR-0015 必须明写这条不可逆性。
4. **ADR-0015 的"7 抽象最小语义"边界**：每个抽象到底冻结到多细？Event Model 是 5 个事件还是 8 个？Boundary 是 1 个 capability 字段还是 schema？这些细节必须在 ADR-0018/0019/0020 草稿大纲里**明示边界**，避免 v1.0 实现阶段超出。
5. **不动 Python 实现代码**（与 TASK-001 §风险 #5 一致）：本 TASK 仍然只产 charter / ADR / 文档，不动 src/。reference impl 由后续 ADR 各自的 PR 落地。
6. **昨天 8 份 ADR 不删**：必须以 Status: Superseded/Deferred 保留——ADR 隶点不可变原则；任何 contributor 应能看到"曾经计划做 X，因 Y 改方向 Z"的全过程。

## 与 CodeFlow §8.0 硬规则的对齐

- ✅ 本 TASK 100% 在 `D:\FCoP` 仓内发生（硬规则 #4）
- ✅ 不在 CodeFlow 仓动 schema（硬规则 #5 防内）
- ✅ AI OS framing 升级 → 必须在 Issue #2 上发后续 comment 通知 CodeFlow（这一步在 ADR-0015 完成后做，不是本 TASK 范围）
- ✅ ADR-0015 timeline 必须 honor §3.3.1.b 5 步流程

## 不属于本 TASK 的延后事项

| 项 | 延后到 |
|---|---|
| Issue #2 上发后续 comment 通知 CodeFlow framing 转向 | ADR-0015 ship 后单开 TASK |
| Mobile / Cloud host adapter 的具体设计 | v2+ |
| Event log 文件类型（EVENT-*.md）是否需要 | ADR-0018 草稿大纲讨论 |
| `risk_level` 在 ADR-0023（如果未来开）里如何 reframe 为 event tag | v1.1 |
| `fcop-rules.mdc` / `fcop-protocol.mdc` 正文是否需要按 7 抽象重组 | v1.1（v1.0 仅顶部 description 升级）|
| Skill schema 完整字段 | v1.1 |
| Session schema 完整实现 | v1.x（v1.0 仅在 ADR-0019 §Recovery 里给最小 hook） |
| `requires_rollback_plan` 字段 enforce | v1.2 |

## 审查者视角（提前预登记自检项）

REPORT-002 写完时，我必须三角度自验：

1. **提案者视角**：ADMIN 5 项决议是否每条都体现在 ADR-0015 §Decision？
2. **执行者视角**：13 步是否全部有交付物？timeline 是否诚实？
3. **审查者视角**：
   - 有没有把 charter 写成"无所不包的 AI OS 蓝图"（违反 min_kernel 决议）？
   - 有没有把 7 抽象的边界写松了（导致后续实现阶段 scope creep）？
   - 有没有动了 Python 实现代码（违反风险 #5）？
   - 有没有保留昨天 8 份 ADR（违反风险 #6）？
   - getting-started.md 是不是又变成了"看完还要去翻其他文档"的反例？

如果三角度任何一条 fail，TASK-002 不闭环。
