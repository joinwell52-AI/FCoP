---
protocol: fcop
version: 1
sender: ADMIN
recipient: ME
priority: P0
subject: FCoP 1.x roadmap — 响应 CodeFlow Issue #2 / 落地 5 类 schema + 5 governance 字段
---

## 背景

下游 CodeFlow v2（仓 `D:\Bridgeflow` / `joinwell52-AI/codeflow-pwa`）在
[`docs/design/codeflow-v2-on-fcop-sdk.md`](../../../../Bridgeflow/docs/design/codeflow-v2-on-fcop-sdk.md)
§3 把整套 Runtime Protocol 设计了出来——5 类 schema（Agent / Task /
Review / Session / Skill），并按 §3.3.1.b + §8.0 硬规则 #4 锁死「协议
演进唯一合法仓库 = `D:\FCoP`」。

CodeFlow 把 5 个最迫切的字段拎出来，作为 [Issue #2](https://github.com/joinwell52-AI/FCoP/issues/2)
正式提交给 FCoP 上游，状态 `pending-fcop-review`。

ME 已读完 Issue #2 全文 + CodeFlow 设计文档 §3 / §0.9.1 / §0.9.4 / §1.3
/ §3.3.1.b / §8.0，并探索了 FCoP 仓库现状（详见探索报告：
adr/README + ADR-0001..0006、`spec/fcop-spec-v1.0.3.md`、`src/fcop/`、
`mcp/`、`docs/releases/0.7.2.md`、`CHANGELOG.md`）。

### 关键发现（ME 的现状对账）

1. **Issue #2 比字面写的大得多**——CodeFlow §3 想要的是整套 5 类
   schema 升级（POSIX / OCI / CRD 类比），不只是 5 个字段。
2. **FCoP 当前没有 Review schema**——只有 `Report.status: 'done' \|
   'blocked' \| 'in_progress'`；Issue 假设的 `Review.decision:
   ['approve', 'reject']` enum 在仓里**不存在**。
3. **FCoP 当前没有 JSON Schema 文件**——`schema.py` 是 dataclass +
   手写 frozenset 校验。CodeFlow §3.1 第 1 条要求改。
4. **FCoP 当前没有 `REVIEW-*.md` 文件类型**——只有 TASK / REPORT /
   ISSUE 的 filename 正则。
5. **当前包版本 `0.7.2`**，Issue 默认目标 `1.1.0` 意味着先要发 `1.0.0`。
6. **CodeFlow §8.0 硬规则 #4 / §3.3.1.b** 锁死：协议任何演进必须
   先在本仓发生，CodeFlow 后镜像。

详细对账见后续 ADR-0007 (charter) 第 §Context。

## ADMIN 决议（2026-05-09 聊天对话锁定）

ADMIN 在 4 个关键岔口拍板，每条都从 `AskQuestion` 5 选项里明确选定：

| 决策点 | 选定方案 | 含义 |
|---|---|---|
| **升级 scope** | **Plan B · 中庸** | `0.7.2` → `1.0.0`（先 freeze）→ `1.1.0`（加 5 字段）。分两次发版，4-5 周 |
| **REVIEW 怎么落** | **新建 `REVIEW-*.md` 文件类型** | 与 TASK / REPORT / ISSUE 并列，配 `models.Review` + `Project.write_review`；REVIEW 是审 TASK / REPORT / role-switch 的独立事件 |
| **JSON Schema** | **`1.0.0` 就上** | `spec/schemas/{agent,task,review,session,skill}.schema.json` + `jsonschema` 库验证（CodeFlow §3.1 原则 #1） |
| **下一步动作** | **三件事都做** | 1) 先在 Issue #2 留方向 comment 让 CodeFlow 知道；2) 写 ADR-0007 charter；3) 切 Plan 模式细化 8 个 ADR |

### 8 ADR 大纲（ADMIN 已认可，细节由 Plan 模式后续补完）

| # | ADR 标题 | 落地版本 | PR scope（粗估）|
|---|---|---|---|
| 0007 | FCoP 1.0 Protocol Freeze Charter | 1.0.0 | 文档（charter + roadmap） |
| 0008 | JSON Schema as Machine-Readable Spec | 1.0.0 | `spec/schemas/*.schema.json` 5 份 + `tests/test_schemas/` + jsonschema 依赖 |
| 0009 | REVIEW-* File Type & Filename Grammar | 1.0.0 | `core/filename.py` 扩 + `models.Review` + `Project.write_review` + REVIEW frontmatter parser |
| 0010 | `Agent.layer` field (`worker` \| `governance` \| `admin`) | 1.1.0 | `TeamConfig.roles[i].layer` + 校验 + 默认 worker |
| 0011 | `Task.risk_level` field (`low` \| `medium` \| `high` \| `irreversible`) | 1.1.0 | `TaskFrontmatter._KNOWN_KEYS` 加 + 默认 medium |
| 0012 | `Review.decision = needs_human` enum extension | 1.1.0 | Review schema 加 enum + Reviewer 接口扩展 |
| 0013 | `Review.human_approval` sub-structure | 1.1.0 | Review schema 子对象 + `Project.mark_human_approved()` API + 校验：approver 必须是 `layer: admin` |
| 0014 | `Skill.tools[]` risk metadata | 1.1.0 | `spec/schemas/skill.schema.json` + `_data/skills/` 模板 + Skill loader |

ADR-0007 / 0008 / 0009 是 1.0.0 地基；0010-0014 是 1.1.0 装修。

## 三步执行计划（这份 TASK 的可交付物）

### 步骤 1：在 Issue #2 留方向回复 comment

- 内容：现状对账（FCoP 当前现状 vs Issue #2 假设的差异表）+
  ADMIN 拍板的 Plan B 路径 + 8 ADR 大纲表 + 时间预期 + 5 步流程承诺
  （引 CodeFlow §3.3.1.b）。
- 让 CodeFlow 那边知道我们的方向、时间表、Issue 字段会按 1.1.0 落地、
  之前会先有 1.0.0 freeze。
- 工具：`gh issue comment 2 --body-file ...`，body 用 HEREDOC 走文件。
- 不关闭 Issue（5 个字段全部进 1.1.0 之后再关）。

### 步骤 2：写 `adr/ADR-0007-fcop-1.0-protocol-freeze-charter.md`

- 严格走 `adr/README.md` 模板：Status / Date / Deciders / Related →
  Context（含本 TASK §背景里的对账表） → Decision（Plan B 路径 + 8
  ADR roadmap） → Design Details（每个 ADR 的边界 + 依赖图） →
  Non-Goals → Alternatives Considered（A/C/D/E 4 个备选 + 否决理由）
  → Consequences（Positive/Negative/Neutral）→ Timeline。
- Status 起手 `Proposed`；本 TASK closed 后改 `Accepted`。
- 同步更新 `adr/README.md` 索引表加这一行。

### 步骤 3：切 Plan 模式细化 ADR-0008..0014

- 每个 ADR 各自起一份 `Status: Proposed` 的草稿 outline（不写正文，
  只写 Context / Decision 一句话 / Design Details 关键 bullet / Tests
  清单 / 兼容性说明）。
- 输出格式：`adr/ADR-NNNN-*.md` 的草稿大纲 + 1 份覆盖 1.0/1.1 两次
  发版的 release-notes 大纲（对位 `docs/releases/0.7.2.md` 的风格）。
- 这一步是**可视化 roadmap**，不写实现代码。
- 实现代码留给后续每个 ADR 单独的 TASK + PR。

## 验收标准

- [ ] 步骤 1：Issue #2 上有 ME 的方向 comment（gh CLI 留下，含
      现状对账表 + Plan B + 8 ADR 大纲）
- [ ] 步骤 2：`adr/ADR-0007-fcop-1.0-protocol-freeze-charter.md`
      存在，Status: Accepted（这次决议是 ADMIN 当面拍板的，直接
      Accepted；不走 Proposed→Accepted 两次提交）
- [ ] `adr/README.md` 索引表新增 ADR-0007 一行
- [ ] 步骤 3：`adr/ADR-0008..0014` 各有一份草稿大纲文件，Status:
      Proposed（待后续单独评审）
- [ ] 写 `REPORT-20260509-001-ME-to-ADMIN.md` 完整自查（含本 TASK
      四步全部勾掉的清单 + git commit 链）
- [ ] 把已过期的 `docs/agents/tasks/TASK-20260428-001-ADMIN-to-ME.md`
      （教程改版，2026-04-28 那次，早已完成但未归档）一并归档到
      `docs/agents/log/tasks/`，附一句"归档原因：内容已落地为
      tetris/snake 教程 + Essay 06，无悬挂工作"
- [ ] 全部 commit + push 到 main（这是 ADMIN 的 repo，无需 PR）

## 风险与边界

1. **scope creep**：8 个 ADR 写下来文字量很大；步骤 3 严格控制为
   "草稿大纲"（每份 ≤ 80 行），不展开实现细节，避免一口吃成胖子。
2. **跨语言契约**：1.0 freeze 后 CodeFlow TS 端要 mirror schema；
   ADR-0007 必须明写"FCoP 是 spec 权威"+ 5 步流程图（直接引 CodeFlow
   §3.3.1.b 全文，避免双仓自由解释）。
3. **`Report.status` 与 `Review.decision` 的语义切割**：1.0 freeze 后
   两者各管一段——Report.status = "我做完没"（worker 自报），
   Review.decision = "我审过了" (governance 审 worker)。ADR-0009 必须
   明写边界。
4. **JSON Schema vs dataclass 的双源真相风险**：避免 schema.json 和
   `core/schema.py` 漂移——ADR-0008 必须定一个"谁是 single source of
   truth"（建议 schema.json 是真相，dataclass 由 schema 生成或对照
   测试 enforce）。
5. **本 TASK 不动 Python 实现**——只产出文档与 roadmap。任何实现
   代码留给后续 TASK。

## 与 CodeFlow §8.0 硬规则的对齐

- 本 TASK 完全在 `D:\FCoP` 仓内发生 → ✅ 符合硬规则 #4。
- 不在 CodeFlow 仓动 schema → ✅ 符合硬规则 #5（防内）。
- 5 步流程的"FCoP 评审通过 → CodeFlow mirror"会在 ADR-0007 charter
  里以原话引用 CodeFlow §3.3.1.b → 双仓共识锁死。
