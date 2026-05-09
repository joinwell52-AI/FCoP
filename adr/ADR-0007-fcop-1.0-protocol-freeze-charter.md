# ADR-0007: FCoP 1.0 Protocol Freeze Charter

- **Status**: Superseded by [ADR-0015](./ADR-0015-fcop-1.0-ai-os-protocol-charter.md)（2026-05-09，同日；framing 升级为 AI OS Protocol，scope 收紧为 7 核心抽象的最小可运行内核）
- **Date**: 2026-05-09
- **Deciders**: ADMIN
- **Related**: [ADR-0001](./ADR-0001-library-api.md)（库 API 契约）、[ADR-0002](./ADR-0002-package-split-and-migration.md)（包拆分硬切）、[ADR-0003](./ADR-0003-stability-charter.md)（pre-1.0 稳定宪章）、[ADR-0006](./ADR-0006-host-neutral-rule-distribution.md)（规则分发）；下游触发：[Issue #2](https://github.com/joinwell52-AI/FCoP/issues/2)；外部参考：[CodeFlow v2 Design §3 / §3.3.1.b / §8.0 hard rule #4](https://github.com/joinwell52-AI/codeflow-pwa/blob/main/docs/design/codeflow-v2-on-fcop-sdk.md)

## ADMIN 决议（2026-05-09）

ADMIN 在 5/9 1:08-1:25 PM CST 的对话中，针对 CodeFlow Issue #2 给出 4 条拍板：

| 决策点 | 选定 | 含义 |
|---|---|---|
| 升级 scope | **Plan B · 中庸** | `0.7.2` → `1.0.0`（先 freeze）→ `1.1.0`（加 5 governance 字段） |
| REVIEW 怎么落 | **新建 `REVIEW-*.md` 文件类型** | 与 TASK / REPORT / ISSUE 并列；REVIEW 是审 TASK / REPORT / role-switch 的独立事件 |
| JSON Schema | **`1.0.0` 就上** | `spec/schemas/{agent,task,review,session,skill}.schema.json` + `jsonschema` 校验库 |
| 下一步 | **三件事都做** | 1) 先回 Issue #2；2) 写 ADR-0007 charter；3) 切 Plan 模式细化 8 ADR |

承上启下：本 ADR 把这 4 条决议固化为 1.x 的 release roadmap，并定义 8 个子 ADR 的边界与依赖。

ADR-0003 在 2026-04-23 留了一句话作为伏笔：

> 「0.7.x → 1.0.0：**终极对齐，允许一次清理**（仿 ADR-0002 的 0.5→0.6 硬切）。」

本 ADR 兑现这一句——它就是 1.0 的"终极对齐方案"。

---

## Context

### 触发事件

[Issue #2](https://github.com/joinwell52-AI/FCoP/issues/2) 由下游 CodeFlow v2（仓 `joinwell52-AI/codeflow-pwa`）于 2026-05-09 提交。提案 5 个 governance 字段：

1. `Agent.layer: 'worker' | 'governance' | 'admin'`
2. `Task.risk_level: 'low' | 'medium' | 'high' | 'irreversible'`
3. `Review.decision = 'needs_human'`（enum 扩展）
4. `Review.human_approval`（子结构）
5. `Skill.tools[]` 风险元数据（`risk_level` / `irreversible` / `cost_sensitive`）

提案的 framing 是"5 个 additive 字段进 `fcop@1.1.0`"。

### 现状对账（Issue 假设 vs FCoP `0.7.2`）

ME 探索仓库后发现 Issue 的 framing 隐含着 5 个**它没意识到的前置缺口**：

| Issue 假设 | FCoP `0.7.2` 现状 | 缺口 |
|---|---|---|
| `Agent` 是 schema 概念 | `TeamConfig.roles: list[Role]`，无 `Agent` dataclass | 需要把 Agent 提升为一等公民 |
| `Review.decision` enum `['approve','reject']` 已存在 | **没有 Review schema**，只有 `Report.status: 'done' \| 'blocked' \| 'in_progress'` | 需要新建 `REVIEW-*.md` 文件类型 |
| `Skill.tools[]` 是已有 schema | **没有 Skill schema**；MCP 是 FastMCP 装饰器，无 `SKILL.md` parser | 需要建 Skill schema + loader |
| 协议有机器可读 schema | **零 JSON Schema**，`core/schema.py` 是 dataclass + frozenset | 需要 `spec/schemas/*.schema.json` 落地 |
| `REVIEW-*.md` 是合法文件名 | `core/filename.py` 只识别 TASK/REPORT/ISSUE | 需要扩文件名 grammar |
| 目标版本 `1.1.0` | 当前 `__version__ = "0.7.2"` | 中间隔着一个 `1.0.0` |

### CodeFlow §3 的更大图景

CodeFlow v2 设计文档 §3 把 Runtime Protocol 设计成**5 类完整 schema**（Agent / Task / Review / Session / Skill），明确对位 Linux POSIX / Docker OCI / Kubernetes CRD：

> "定义 Runtime Protocol —— 一旦协议稳定，生态会自己长出来。这其实就是 Linux 的 POSIX、Docker 的 OCI、Kubernetes 的 CRD。" —— CodeFlow §3 卷首

5 类 schema 中的每一类都比 Issue #2 单字段宽得多。Issue #2 是 §3 vision 的"5 个最迫切字段"切片，不是全部。

### CodeFlow §8.0 hard rule #4 + §3.3.1.b：协议演进唯一合法仓库

> 「协议演进唯一合法仓库 = `D:\FCoP` / `joinwell52-AI/FCoP`。任何"v2 想要但 FCoP 没有"的字段需求 → 必须先去 `D:\FCoP` 提 Issue / PR。任何"暂时在 v2 这边加个字段先用着"的捷径 → **不允许**。」

这条规则把 FCoP 仓推到了"协议权威"地位。Issue #2 是它的第一次正式行使。

### 约束

- **向后兼容是底线**：CodeFlow §3.1 原则 #3 + ADR-0003 都明文写：minor bump 只允许加字段，新字段对旧消费者透明。任何打破 `0.7.x` 用户既有代码 / 配置的改动都不能算 minor。
- **跨语言契约**：CodeFlow TS 端 `packages/codeflow-protocol/` 是 FCoP spec 的 TS 镜像；schema 跨语言必须等价。这意味着 1.0 的 spec 必须是机器可读的（不能是 markdown 散文）。
- **CI 已经 lock 住的不变量**：`tests/test_fcop/test_public_surface.py` + `tests/test_fcop_mcp/test_tool_surface.py` + `tests/test_fcop/test_pyproject_pins.py` + `tests/test_fcop/test_rules_metadata_consistency.py`。任何改动必须维护这些快照（必要时附 review 通过的 snapshot 更新）。
- **PROTOCOL_VERSION 这个整数变量**：`src/fcop/core/schema.py` 的 `PROTOCOL_VERSION: int = 1` 与 spec 文档版本号不是同一计数体系。1.0 / 1.1 升级**不会**bump 这个整数（它只在 frontmatter 的 on-disk format 真正破坏时才动）。

---

## Decision

### 核心决策（Plan B · 中庸路径）

**FCoP 走"先 freeze、后加字段"的两步 minor 路径**：

```
0.7.2 ──► 1.0.0 ──► 1.1.0
         ▲          ▲
         │          │
         │          └── 加 5 个 governance 字段（Issue #2 全部需求）
         │              一字段一 ADR，独立 PR；都是 additive
         │
         └── 协议 freeze：JSON Schema 形式化 + REVIEW 文件类型 + 公开面锁定
             不加任何业务功能，只把已有约定形式化、可机器校验、可跨语言 mirror
```

两次发版都严格遵守 ADR-0003 的稳定宪章——`1.0.0` 是 ADR-0003 「0.7→1.0 一次清理」窗口的兑现，`1.1.0` 进入 1.x 的"只进不出"模式。

### 8 ADR 路线图

| # | ADR 标题 | 落地版本 | 类型 | 主要触点 |
|---|---|---|---|---|
| **0007** | **FCoP 1.0 Protocol Freeze Charter**（本文） | 1.0.0 | 宪章 | 文档；不动代码 |
| 0008 | JSON Schema as Machine-Readable Spec | 1.0.0 | 规范 + 实现 | `spec/schemas/*.schema.json` × 5 + `tests/test_schemas/` + `jsonschema` 运行时依赖 + `core/schema.py` 内常量改为 schema 派生 |
| 0009 | `REVIEW-*.md` File Type & Filename Grammar | 1.0.0 | 规范 + 实现 | `core/filename.py` + `models.Review` + `Project.write_review` / `read_review` / `list_reviews` + `core/frontmatter.py` review parser |
| 0010 | `Agent.layer` field (`worker` / `governance` / `admin`) | 1.1.0 | 字段 | `TeamConfig.roles[i].layer` + 默认 `worker` + 校验（`governance` 不得 spawn agents；`admin` 不得 programmatic create） |
| 0011 | `Task.risk_level` field (`low` / `medium` / `high` / `irreversible`) | 1.1.0 | 字段 | `TaskFrontmatter._KNOWN_KEYS` + 默认 `medium` + `irreversible` 保留 `requires_rollback_plan` 字段名 |
| 0012 | `Review.decision = needs_human` enum extension | 1.1.0 | 字段 | Review schema enum 加值 + Reviewer 接口扩展 |
| 0013 | `Review.human_approval` sub-structure | 1.1.0 | 字段 | Review schema + `Project.mark_human_approved()` API + 校验：approver 必须是 `layer: admin` 角色；`channel: 'manual_file_edit'` 必须有 `device_id` 或 `channel_attestation` |
| 0014 | `Skill.tools[]` risk metadata | 1.1.0 | 字段 + schema | `spec/schemas/skill.schema.json` + `_data/skills/` 模板 + Skill loader 在 `fcop` 库一侧 |

ADR 编号一旦发出**不再变动**——即使后续顺序调整，编号保留作为历史指针。

### 落地节奏

| 时间窗 | 产出 | 责任人 |
|---|---|---|
| D0（今天 2026-05-09） | TASK-20260509-001 + Issue #2 reply + ADR-0007 + ADR-0008..0014 草稿大纲 | ADMIN + ME |
| D0 + 7 天 | ADR-0008 / 0009 完整稿 + 各自 PR 入库 | ME |
| **D0 + 14 天** | **`fcop@1.0.0` + `fcop-mcp@1.0.0` 上 PyPI** | ME |
| D0 + 14-21 天 | ADR-0010 / 0011 / 0014 完整稿 + PR | ME |
| D0 + 21-28 天 | ADR-0012 / 0013 完整稿 + PR | ME |
| **D0 + 35 天** | **`fcop@1.1.0` + `fcop-mcp@1.1.0` 上 PyPI** | ME |

每个 ADR 落地必须配 release notes 段落（`docs/releases/1.0.0.md` / `1.1.0.md`），仿 `0.7.2.md` 的格式。

---

## Design Details

### 1.0.0 的"四大冻结"

`fcop@1.0.0` 是个**纯结构化**版本——它不加业务能力，只把 0.7.x 既有的约定升级为机器可读、可 mirror、可 fuzz-test 的形式。冻结面有四块：

#### 冻结 #1：JSON Schema 作为唯一规范权威

`spec/schemas/` 下落 5 个文件：

```
spec/schemas/
├── agent.schema.json     # 现有 TeamConfig.roles[i] 字段的 schema
├── task.schema.json      # 现有 TaskFrontmatter 字段的 schema
├── review.schema.json    # 1.0 新增的 REVIEW-*.md frontmatter
├── session.schema.json   # 1.0 占位（v0.1 仅必填字段，实现留待 1.x 后续）
└── skill.schema.json     # 1.0 占位（同 session）
```

**single source of truth 原则**：`core/schema.py` 的 dataclass 字段集合**不**作为权威，反过来由 `spec/schemas/*.schema.json` 在 CI 阶段对照生成（或 enforce 等价）。这避免了双源真相漂移。具体机制由 ADR-0008 拍板。

#### 冻结 #2：REVIEW-*.md 进协议正典

filename grammar 增加：

```
REVIEW-{YYYYMMDD}-{NNN}-{REVIEWER_ROLE}-on-{SUBJECT_REF}.md
```

例：`REVIEW-20260601-003-QA-on-TASK-20260601-001.md`

`subject_ref` 可指向 TASK / REPORT / role-switch 文件名。`subject_type: 'task' | 'report' | 'role_switch' | 'code_change'`（直接对齐 CodeFlow §3.4 字段名，避免后续语义漂移）。

REVIEW 与 REPORT 的语义切割：

| | REPORT | REVIEW |
|---|---|---|
| 谁写 | worker（自报状态） | governance（外审） |
| 关键字段 | `status: done \| blocked \| in_progress` | `decision: approved \| rejected \| needs_changes \| abstained \| needs_human` |
| 触发 | TASK 完成 / 阻塞 / 进展 | 对 TASK / REPORT / role-switch 的事后审计 |
| 在 1.0 范围 | 不动（继续 0.7.x 约定） | 全新 |

#### 冻结 #3：公开 API 面 1.0 锁

ADR-0003 的「公开 API 面只进不出」原则在 1.0 边界做最后一次清理后，进入正式 1.x 锁。具体清理范围：

- 任何在 0.7.x 标过 `DeprecationWarning` 的 API：1.0 真删（这是 ADR-0003 deprecation cycle 的兑现窗口）
- 公开符号命名一致性（按 ADR-0001 的 API 契约 audit 一次）
- `models.*` dataclass 字段：1.0 之后只允许加新字段、加新 dataclass

清理列表由 ADR-0007 之外的"1.0.0 release notes" 文档单独维护（见 `docs/releases/1.0.0.md` 草稿）。

#### 冻结 #4：版本号语义重新定义

| 维度 | 0.x 含义 | 1.x 含义 |
|---|---|---|
| MAJOR (1.x → 2.x) | N/A | 协议级 breaking + 至少 6 个月共存 + 官方迁移脚本 |
| MINOR (1.0 → 1.1) | "新功能可能 break" | **只允许 additive**，新字段对旧 consumer 透明 |
| PATCH (1.0.0 → 1.0.1) | "bug fix" | **绝对零行为变化**，仅 bug fix |

`fcop` 与 `fcop-mcp` 继续 lockstep 同步 MINOR（如 `fcop@1.1.x` ↔ `fcop-mcp@1.1.x`），由 `tests/test_fcop/test_pyproject_pins.py` enforce。

### 1.1.0 的"五个加法"

每个字段一个 ADR、一个 PR、一段 release-notes。所有字段都遵守同一模板：

| 维度 | 约束 |
|---|---|
| 默认值 | 必须能让旧 consumer 完全无感（layer 默认 `worker`，risk_level 默认 `medium`，decision 不返回 `needs_human` 即旧行为） |
| Schema 版本 bump | 只 bump `spec/schemas/*.schema.json` 内的 `$schema`（如 `agent/v1.0` → `agent/v1.1`），**不**bump `core/schema.py` 的 `PROTOCOL_VERSION` 整数 |
| 测试 | 必须新增至少 3 个测试：(a) 字段缺省时旧文件可读；(b) 字段非法值被拒绝；(c) 字段合法值流转完整 |
| MCP 暴露 | 视字段而定。`Task.risk_level` 必须在 `write_task` MCP tool 加可选参数；`Agent.layer` 不直接 MCP 暴露（属配置层） |
| 文档 | release notes + `MIGRATION-1.1.md` 各加一段 |

### 跨语言契约（与 CodeFlow TS 镜像的协同）

CodeFlow TS 端 `packages/codeflow-protocol/` 是本仓 spec 的镜像：

```
本仓 (spec/schemas/*.schema.json) ──── single source of truth ────► CodeFlow TS schema
                                  ◄────── fuzz test enforce ──────
```

具体对接（由 ADR-0008 详细规定）：

1. 本仓发版 → CHANGELOG 列出所有 schema 变化
2. CodeFlow 那边同 minor 跟随（如 `@codeflow/protocol@1.0.0` ↔ `fcop@1.0.0`）
3. CodeFlow 仓 CI 跑跨语言 fuzz 测试，验证 TS schema 等价于本仓 JSON Schema
4. 任何 schema 偏离 → CodeFlow 侧 build fail，强制走 §3.3.1.b 5 步流程

CodeFlow §3.3.1.b 的 5 步流程在本 ADR 里以**链接**而非复制方式引用——避免双仓自由解释，以 CodeFlow 仓为准。

---

## Non-Goals

- **不**在 1.0 / 1.1 范围内引入 Session schema 完整实现（CodeFlow §3.5）。1.0 仅留 schema 占位文件，1.x 后续 minor 再实现。理由：Session 涉及 SDK 集成（OpenAI / Anthropic / Cursor），单独成版本叙事更清晰。
- **不**在本 ADR 内 enumerate 8 个子 ADR 的全部技术细节。每个子 ADR 自己负责。本 ADR 只锁路线、节奏、依赖、跨版本约束。
- **不**承诺 1.0 之前发任何 0.7.x patch。如发，仅限 ADR-0003 框定的"绝对兼容"补丁。
- **不**在 1.0 / 1.1 触碰 `PROTOCOL_VERSION` 整数（`src/fcop/core/schema.py` 第 56 行）。它只代表 frontmatter on-disk format 的破坏性升级，与 schema 字段加法无关。
- **不**承诺 CodeFlow TS 镜像在本仓 release 之前可用——TS 镜像由 CodeFlow 仓自行排期。
- **不**承诺 1.0 / 1.1 之外发个 0.8 / 0.9 中间版本。Plan B 直接 0.7.2 → 1.0.0 → 1.1.0，无中转站。

---

## Alternatives Considered

### Alt-A：极小切片（直接 0.7.2 → 0.8.0，5 字段一锅端）

只把 5 个字段加进现有 dataclass，复用 `Report.status` 充当 `Review.decision`，不建 REVIEW 文件类型，不做 JSON Schema。

**否决原因**：
- 违反 CodeFlow §3.1 原则 #3 ("minor bump 只允许加字段、新字段对旧 consumer 透明")——把 `Report.status` 重载成 `Review.decision` 是语义破坏，不是 additive
- 没有 JSON Schema → CodeFlow TS 端无法 mirror，§3.3.1.b 5 步流程跑不通
- "5 字段进 0.8.0" 的版本号语义错——这套字段是治理级别，配 1.x 才符合 semver 直觉
- 没有 1.0 锚点 → 后续 1.0 还要单独再做一次 freeze，等于做两遍

### Alt-C：一次性 1.0（freeze + 5 字段一锅烩）

把 1.0 freeze 与 5 字段都塞进 `1.0.0`。

**否决原因**：
- 风险大：1.0 必须 stable，但同 release 引入 5 个新字段就意味着 1.0 出版当天就有 5 个待 burn-in 的新字段——一旦发现字段设计需要调整，1.0 立刻被迫 1.0.1 / 1.0.2 修正，冻结力丧失
- 时间长：所有工作必须串到 1.0 发版前完成，估计 5-7 周——CodeFlow S2-S6 sprint 等不起
- 违反"一次决议一次 ADR"工程原则——1.0 要 freeze 决策本身已经是大议题，再叠加 5 个字段 = 6 件事一锅烩

### Alt-D：跳过 1.0 直接 1.1.0

按 Issue #2 字面，直接 0.7.2 → 1.1.0。

**否决原因**：
- 违反 semver——1.1 默认存在 1.0；CodeFlow §3.1 原则 #3 也假设 minor=1.x
- 1.0 freeze 是必须做的动作（JSON Schema、REVIEW 文件类型）；如果不发独立的 1.0，这些工作只能挤进 1.1.0 → 实际等价于 Alt-C
- 释放出错误信号——下游会以为 FCoP 不重视 stability charter（ADR-0003 的精神）

### Alt-E：仅改 spec 文档，不动 Python 实现

只在 `spec/fcop-spec.md` 加新章节描述 5 字段，让 CodeFlow TS 端"按 spec 实现"。

**否决原因**：
- CodeFlow §3.3.1.b 第 3-4 步明确要求"D:\FCoP 仓内：spec 文档 + Python 双包同步演进"——光改 spec 不动 Python 等于本仓没履行 spec 实施义务
- 本仓的 Python 双包是 FCoP 协议的"reference implementation"——它必须能跑过 5 字段相关的所有用例，否则 spec 是空文
- 跨语言 fuzz 测试（CodeFlow §3.8 v0.1→v1.0 criterion #4）需要 Python 端可执行行为作为 oracle

---

## Consequences

### Positive

- **CodeFlow 不会被卡死**：1.0.0 在 ~2 周内出，CodeFlow 那边可以立刻 mirror schema 文件 + 写 fuzz 测试；governance 字段在 ~5 周内全部就位
- **协议拿到 POSIX 时刻**：1.0 是 FCoP 第一次有"机器可读、跨语言可 mirror、被 fuzz test enforce"的 spec。这跟 Zenodo DOI 的学术资格双管齐下，让 FCoP 进入"可被引用、可被实现、可被信赖"三件套齐全的状态
- **Issue #2 不是孤儿**：8 ADR 的 roadmap 把 Issue 提议的 5 字段嵌进 FCoP 自己的演进叙事，不是单纯接外活
- **ADR-0003 的 0.7→1.0 清理窗口正式兑现**：早就预留的"一次性硬切"窗口落到具体动作上
- **下游协议演进路径有了模板**：以后任何"v2 想要但 FCoP 没有"的字段都按 §3.3.1.b 5 步流程走，本次是首例 reference

### Negative

- **比原计划多一个发版周期**：直接 1.1.0 vs 先 1.0 再 1.1，多 ~2 周。但收益（freeze 锚点、跨语言契约）远大于成本
- **JSON Schema 引入新依赖**：`jsonschema` 库进生产依赖，多一个 transitive 风险。由 ADR-0008 选具体 lib（候选：`jsonschema` / `fastjsonschema`，主要权衡是 dependency footprint vs validation 速度）
- **REVIEW 文件类型增加学习曲线**：对纯 0.7.x 用户，1.0 多了一类需要理解的文件。`MIGRATION-1.0.md` 必须把"REVIEW 是新概念，旧 TASK/REPORT/ISSUE 流程不受影响"写在最显眼位置
- **`spec/fcop-spec-v1.0.3.md` 与 `core/schema.py` 双源不一致的历史债**会在 1.0 暴露——必须一次性对齐（这是 freeze 的好处也是代价）

### Neutral

- **不影响 Zenodo DOI**：DOI 是 research snapshot 时点引用，1.0 / 1.1 发布会有新 GitHub Release，可以再发 DOI（可选，由后续 TASK 决定）
- **不影响 GitHub Pages 主页**：landing page 不绑特定版本号，里面的 `pipx install fcop-mcp` 仍然有效
- **不影响 `fcop-rules.mdc` 与 `fcop-protocol.mdc`**：这两份 host-neutral 规则文件由 ADR-0006 管理，1.0 / 1.1 是否 bump rules version 由各子 ADR 决定（多数情况：不 bump，rules 是宿主层规则，与协议字段升级解耦）

---

## Timeline

| 日期 | 里程碑 | 产出 |
|---|---|---|
| **2026-05-09** (D0) | 本 ADR 落定 + 子 ADR 草稿大纲 | TASK-20260509-001、Issue #2 reply、ADR-0007 (Accepted)、ADR-0008..0014 (Proposed 大纲) |
| 2026-05-12 (D+3) | ADR-0008 完整稿 + PR | spec/schemas 落 5 文件，jsonschema 集成 |
| 2026-05-16 (D+7) | ADR-0009 完整稿 + PR | REVIEW-* 文件类型上线 |
| **2026-05-23** (D+14) | `fcop@1.0.0` + `fcop-mcp@1.0.0` 上 PyPI | docs/releases/1.0.0.md、CHANGELOG `[1.0.0]`、`MIGRATION-1.0.md` |
| 2026-05-26 (D+17) | ADR-0010 + PR | Agent.layer 落地 |
| 2026-05-29 (D+20) | ADR-0011 + PR | Task.risk_level 落地 |
| 2026-06-02 (D+24) | ADR-0014 + PR | Skill.tools[] risk metadata 落地 |
| 2026-06-05 (D+27) | ADR-0012 + PR | Review.decision needs_human 落地 |
| 2026-06-09 (D+31) | ADR-0013 + PR | Review.human_approval 落地 |
| **2026-06-13** (D+35) | `fcop@1.1.0` + `fcop-mcp@1.1.0` 上 PyPI | docs/releases/1.1.0.md、CHANGELOG `[1.1.0]`、`MIGRATION-1.1.md`、Issue #2 关闭 |

每个里程碑允许 ±3 天浮动。任何超过 7 天的延期触发"重新评估"——由后续 TASK 决定调整路线还是延长 timeline。

---

## Sign-off

- **ADMIN**：已批准（2026-05-09，AskQuestion 4 选项明确）
- **ME**：负责执行；REPORT-20260509-001-ME-to-ADMIN.md 在三步全部完成后签字

---

_Last edited: 2026-05-09. Status changes go in the table at the top; body content is frozen per ADR convention._
