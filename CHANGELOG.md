# Changelog

All notable changes to the `fcop` and `fcop-mcp` Python packages are recorded
here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and the project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This file tracks both packages together because they release in lockstep.
See [adr/ADR-0002](./adr/ADR-0002-package-split-and-migration.md) for the
versioning strategy.

## [1.5.1] — 2026-04-25

### fix(docs) — 版本字符串对齐补丁

**核心问题**：`v1.5.0` 发布后发现 `letter-to-admin.{zh,en}.md` 的摘要块停留在
`v1.5.0 摘要` 标注正确，但 `fcop-protocol.mdc` 版本引用写成了 `2.2.0`（实际
已升至 `2.3.0`），违反了发版前版本对齐必检项。同时 `test_server.py` 里的
断言也未随上一批文档修复同步。

**变更内容**（纯文档 / 测试修复，无功能变更）：

- `src/fcop/rules/_data/letter-to-admin.{zh,en}.md`：摘要块升至 `v1.5.1`；
  修正 `fcop-protocol.mdc 2.2.0` → `2.3.0`
- `src/fcop/_version.py`：1.5.0 → 1.5.1
- `src/fcop/rules/_data/fcop-rules.mdc`：2.4.0 changelog 条目注明 1.5.1 为 no-rule-change patch
- `src/fcop/rules/_data/fcop-protocol.mdc`：Protocol Version Log v2.3 条目注明 1.5.1 no commentary change
- `tests/test_fcop/test_rules.py` + `tests/test_fcop_mcp/test_server.py`：断言更新至 `v1.5.1 摘要`

**根因分析**：发版流程中 Phase 3-V（版本字符串全文对齐）检查项执行不到位，
`fcop-protocol.mdc` 版本在 v1.5.0 升至 2.3.0 但 letter 里的引用未同步。
已在 `RELEASE-CHECKLIST.md` 强化了该检查项，要求发版前逐项人工过一遍。

## [1.5.0] — 2026-05-12

### docs(P1) — 84 份角色/团队文档同步至 v1.4 协议

**核心问题**：v1.4.0 发布后，`fcop/shared/roles/` 里已部署的角色文档与团队模板
仍停留在 v1.1 内容层，不包含 REVIEW envelope / `risk_level` / `fcop_audit` /
`supersedes:` 等 v1.0~v1.4 引入的关键协议能力，新接手项目的 Agent 读取这些文档后
感知不到新功能（协议能力认知漂移 RULE_DOC_DRIFT）。

**变更内容**（涉及 58 个文件）：

- **非 leader 角色文档 × 20 份（中英双语）**：DEV / QA / OPS / WRITER / TESTER 等，
  新增"v1.0 ~ v1.4 协议更新速查"节，含 REVIEW envelope / `risk_level` /
  `fcop_audit` 与 INSPECTION / `supersedes:` 字段四小节
- **TEAM-ROLES × 10 份（5 团队 × 中英）**：新增"协议演进说明（v1.0 ~ v1.4）"表格
- **TEAM-OPERATING-RULES × 10 份（5 团队 × 中英）**：新增"协议演进补记"节，
  含高风险任务审批 / `fcop_audit` 整改处理 / write-side 绑定规则三段
- **team README × 10 份（5 团队 × 中英）**：新增"工具速查链接"表格
- **`docs/getting-started.{zh,en}.md`**：新增"fcop_audit 三场景体检"节
- **`src/fcop/rules/_data/agent-install-prompt.{zh,en}.md`**：装完即跑 `fcop_audit()` 提示

---

### feat(audit/P2) — `_scan_outdated_role_docs()` + RULE_DOC_DRIFT

**新增 `Project._scan_outdated_role_docs()` 扫描方法**（`scope=upgrade/takeover`）：

- 读取已安装 `fcop` 包版本（`major.minor`）
- Glob `fcop/shared/roles/*.md`，对每个文件用正则提取最高版本号引用
- 无版本引用，或版本 gap > 1 minor → 记入 `Violation(severity=P1, rule="RULE_DOC_DRIFT")`
- 整改建议：`deploy_role_templates(force=True)` 重新部署最新角色模板

**ADR-0032 同步更新**：新增 §4.7 `_scan_outdated_role_docs()` + `RULE_DOC_DRIFT` 违规类型

**测试**：`tests/test_fcop/test_audit.py` 新增 4 个测试用例（无 roles 目录 / 无版本引用 / 版本落后 / 当前版本）

---

### fix(ci) — Protocol v2.2 日志 + drop_suggestion 豁免

- `fcop-protocol.mdc` 正文补录 `v2.2` Protocol Version Log 条目（CI 测试验收）
- `mcp/src/fcop_mcp/server.py`：`drop_suggestion` 加入 `_INIT_TOOLS` 豁免，
  使其在项目初始化前也可向 `.fcop/proposals/` 写入建议文件（轻量级预初始化操作）

---

### docs — Essays 07-10 + essays/README.md

- **essay 07** `when-agents-learn-from-their-own-wreckage.md`：codeflow 一日 14 个涌现现场报告
- **essay 08** `why-the-protocol-stays-short.md`：协议为什么短，历史为什么长
- **essay 09** `gate-design-pitfalls-case-studies.md`：validator-validates-itself 案例分析
- **essay 10** `the-supersedes-field-story.md`：`supersedes:` 字段两小时旅程
- `essays/README.md`：10 篇文章完整索引 + 分类阅读建议
- `adr/README.md`：嵌入三层语义执行链模型图

---

## [1.4.0] — 2026-05-12

### fix(security) — P0 Write-side 工具显式绑定守门（PM #50 事件修复）

**核心问题**：`fcop-mcp 1.3.x` 的 write-side 工具在未显式绑定项目路径时，允许退化到
MCP Server 的 `cwd`（即 USER HOME），造成 `fcop-rules.mdc` 等文件污染系统目录。

**变更内容**（参见 `docs/releases/1.4.0.md`）：

- **D1 — 显式绑定守门**：15 个 write-side 工具在 cwd fallback 情况下直接抛出 `WriteRefused`
- **D2 — Protected Path 拒绝列表**：HOME / APPDATA / 驱动器根 / Unix 系统目录 全部硬拦截
- **D3 — `fcop_report()` 顶部告警**：检测到 protected path 或 cwd fallback 时显示 ⚠️ 警告
- **D4 — MCP Schema `binding_required` 标签**：`tools/list` 携带 `tags: ["binding_required"]`
- **D5 — 测试覆盖**：新增 `mcp/tests/test_write_guard.py`，11 通过 / 2 跳过（Unix 平台）
- **D6 — Release Notes**：`docs/releases/1.4.0.md` + 三种升级场景说明

**Breaking-ish**：原来依赖 cwd fallback 调用 write-side 工具的配置需要显式设置
`FCOP_PROJECT_DIR` 或调用 `set_project_dir()`，详见升级指南。

---

### feat(protocol) — `fcop_protocol_version 2.2.0`：`supersedes:` 字段 + GATE Design Pitfalls

**`fcop-protocol.mdc` 变更（2.1.0 → 2.2.0）**：

- **新增 `supersedes:` frontmatter 字段**（TASK-004）：  
  所有 envelope 类型（TASK / REPORT / ISSUE / REVIEW）新增可选字段，
  语义：本文件顶替 / 废止指定历史文件（Rule 5 append-only 修正模式）。  
  与 `parent:`（工作派生）/ `related:`（交叉引用）语义正交。  
  `ipc-envelope.schema.json` 同步加入 optional `supersedes` 字段。  
  `list_tasks` / `list_reports` 自动标注 `[supersedes X]` / `[superseded by X]`。

- **新增 `## GATE Design Pitfalls` 节**（TASK-003）：  
  Pitfall 1（GATE 描述自我命中）+ 语义化实证推荐姿势 + GATE 设计自查清单。  
  预留 `fcop_audit` D8 scan（`_scan_gate_self_collision()`）锚点，归 v1.5 认领。

---

## [1.3.1] — 2026-05-12

### fix(docs) — 协议文档同步至 v1.3.0（P0 整改批次）

**核心问题**：fcop v1.3.0 发布后，面向 Agent 的协议规则文件停留在 v1.1，导致 Agent 不知道 `fcop_audit()` / GAL / INSPECTION 的存在。

**变更内容**：

- **`fcop-rules.mdc` → 2.3.0**：新增 Rule 9.6（协议体检 / fcop_audit & INSPECTION）+ Rule 9.7（治理告警层 / GAL）
- **`fcop-protocol.mdc` → 2.1.0**：新增 9.6/9.7 Commentary 操作指南；`fcop/shared/` 目录表加入 `INSPECTION-` 行；新增批量整改授权模式规范
- **`letter-to-admin.{zh,en}.md`**：摘要段从 "0.6.4/0.6.5" 全面重写为 "v1.3.0 摘要"，涵盖 fcop_audit / GAL / risk_level / 工具总数
- **Leader 角色文档 × 10 份（中英各 5）**：PM / ME / LEAD-QA / MARKETER / PUBLISHER 均新增 "v1.3.0 工具速查" 段，包含 fcop_audit / fcop_list_alerts / write_task(risk_level) 等关键工具示例
- **`.cursor/rules/` + `AGENTS.md` + `CLAUDE.md`**：随源文件更新同步部署

**本次不包含**：P1（84 份团队模板深度）/ P2（`_scan_outdated_role_docs` 新增 scan）——推 1.4.0。

---

## [1.3.0] — 2026-05-12

### feat(audit) — ADR-0032 fcop_audit()：协议状态编译器（三场景体检工具）

**FCoP 第五支柱**：让协议合规缺口"成为可执行文档"。

**核心定位**：`fcop_audit()` is a protocol-to-inspection compiler — translates FCoP compliance state into structured findings and suggested remediation plans.

**新增 1 个 MCP 工具**（总数 34 → 35）：

- **`fcop_audit`** — 三场景协议体检工具；支持 `scope=new/upgrade/takeover/auto`；产出 `INSPECTION-{date}-{NNN}-{scope}.md`（含 P0/P1/P2 分档 + Execution Block 建议命令）

**新增 `fcop.inspection` 模块**：

- `RemediationStep` — 单条可复制整改命令（tier / executor / rollback / 双平台命令）
- `Violation` — 协议违规发现（evidence / impact / remediation 列表）
- `InspectionReport` — 完整体检报告，`to_markdown()`（L3 格式）+ `to_dict()`（机读 JSON）

**新增 `Project.audit()` Python API**（6 个 `scan_*` 扫描方法）：

| 扫描方法 | 检测范围 | 对应违规 |
|---|---|---|
| `_scan_cursor_rules()` | 协议规则缺失 / 草根规则混入 | Rule 0 P0/P2 |
| `_scan_shared_deployment()` | 三层团队文档部署完整度 | Rule 4.5 P0/P1 |
| `_scan_misplaced_envelopes()` | envelope 桶错位 | Rule 2 P1 |
| `_scan_legacy_role_docs()` | 草根角色书（无 kind: 字段） | Rule 1 P1 |
| `_scan_legacy_manifests()` | 非标准 JSON 双 manifest | Rule 0 P1 |
| `_scan_ghost_prefixes()` | 幽灵前缀文件（DRAFT/HANDOFF/AMEND） | Rule 5 P2 |

**L3 报告格式**（INSPECTION = Structured Findings + Suggested Remediation Plan）：

- YAML frontmatter（机读：inspection_id / overall_status / p0-p2 计数）
- P0 阻塞性 / P1 规范性 / P2 整洁性 分档展示
- **Execution Block**（核心创新）：按 Tier 1/2/3 分组的可复制整改命令建议，含回滚、执行人、时长估算
- append-only：同日同 scope 第二次跑产出 NNN+1，不覆盖

**新增核心规范文档**：`adr/FCoP-semantic-execution-chain.md`（三层语义执行链模型：Schema Layer / Signal Layer / Compiler Layer）

**测试**：新增 16 个 audit 单元测试，覆盖所有 scan_* 方法 + 三场景集成

---

### feat(gal) — ADR-0031 Governance Alert Layer：治理漂移检测与 ADMIN 告警

**FCoP 第四支柱**：让治理断层"自发光"（Governance Gaps Are Escalatable）。

**核心原则**：`Potential governance gaps must become ADMIN-visible within SLA.`  
GAL 不治理、不审批、不阻断——只做异常升级（Escalation）。

**新增 2 个 MCP 工具**（总数 32 → 34）：

- **`fcop_list_alerts`** — ADMIN 治理告警收件箱；读取 `fcop/alerts/ALERT-*.md`；支持按 `status` / `severity` 过滤；无需巡检，系统把异常送到 ADMIN 面前
- **`fcop_create_alert`** — 手动归档治理缺口；写入新 ALERT-*.md 文件

**新增 `gal/` 子包**（`fcop_mcp.gal`）：

- `create_alert` / `list_alerts` — ALERT-*.md append-only 文件操作
- `run_drift_scan` — 三类漂移信号扫描器（S1 / S3 / S4）

**三类漂移信号**：

- **S1 `critical_tool_unreviewed`**：24h 内有 CRITICAL_TAG 调用但无对应 Review → `severity: high`
- **S3 `missing_independent_verdict`（Solo Blindspot）**：执行窗口 > 6h 无任何治理事件 → `severity: high`
- **S4 `long_running_without_reconciliation`**：open Task 超 24h 未归档 → `severity: low`

**FCoP-Rule-G1（协议公理）**：

> `write_report / fcop_report` ∈ 执行域。自我叙述 ≠ 治理信号。不能重置 Solo Blindspot 窗口。  
> 只有 `write_review` / `mark_human_approved` / `fcop_check` 才构成独立治理视角。

**三域模型**（`skill_registry.yaml` 全量标注 `domain` 字段）：

| 域 | 工具示例 | 治理意义 |
|---|---|---|
| `execution` | write_task, write_report, fcop_report, delete_task | 自述，不重置治理窗口 |
| `governance` | write_review, mark_human_approved, fcop_check | 独立视角，重置 Solo Blindspot |
| `neutral` | list_tasks, read_task, list_reviews | 只读，无域效果 |

**实战案例 #24（2026-05-11）**：

> v0.3.0-alpha 含 8 commits，持续开发 ~8h，无独立 Review，无治理确认。  
> 若无 ADMIN 第二次介入，将以「无 QA sign-off」状态进入发版。  
> GAL S3（Solo Blindspot）信号会在 6h 时自动触发告警，无需 ADMIN 手动巡检。

**`fcop_check()` 整合 GAL Layer 3**：输出末段新增「治理告警扫描」摘要，命中漂移信号即实时写入 ALERT 文件。

---

## [1.2.1] — 2026-05-11

### chore — fcop 与 fcop-mcp 锁步对齐至 1.2.1（lockstep 恢复）

`fcop` 库从 `1.1.0` 空 patch 升至 `1.2.1`，与 `fcop-mcp 1.2.1` 严格对齐。此前 `fcop-mcp` 在 `1.1.1` / `1.2.0` / `1.2.0` 阶段手动发布，跳过了 CI `release.yml` 的 lockstep 检查；本 patch 恢复两包同版，后续所有发版均须通过 CI 一条龙（tag push → workflow → PyPI + GitHub Release）。

`fcop` 包本身无代码改动；`fcop-mcp` 功能与 `1.2.0` 完全相同，仅修正：

- `mcp/README.md`（PyPI 页面描述）工具数 30 → 32，补入 v1.2.0 治理工具说明
- `src/fcop/_version.py` 版本号对齐至 `1.2.1`

---

## [1.2.0] — 2026-05-11

### feat(mcp) — fcop-mcp 1.2.0：治理事件审计层（ADR-0030-bis Layer 1）

**新增 2 个 MCP 工具**（总数 30 → 32）：

- **`list_governance_events`** — 读取 `fcop_events.jsonl` append-only 治理日志；支持按 `risk`（Safe / Sensitive / Critical）和 `tag`（ALLOW / REVIEW_TAG / CRITICAL_TAG）过滤；每条显示 tool、risk、tag、args_hash、session_id、时间戳
- **`get_governance_summary`** — 汇总统计：总调用量 / 各风险层分布 / Top 10 工具 / CRITICAL_TAG 事件清单；快速健康检查入口

**新增 `governance/` 子包**（`fcop_mcp.governance`）：

- `FCoPGovernanceMiddleware` — FastMCP `on_call_tool` hook，每次工具调用自动执行：① Skill Resolver（tool_name → risk_level）→ ② Risk Tag（3 行静态映射）→ ③ Event Log（append-only `fcop_events.jsonl`）→ ④ call_next（不阻断）
- `skill_registry.yaml` — 产品化配置资产，定义全部 32 个内置工具的 risk 分类，用户可在项目级覆盖
- `resolve_skill` / `emit_event` — 可单独使用的工具函数

**`fcop_check()` 整合 Layer 3 审计**：输出末段新增「治理事件日志」摘要，显示 CRITICAL_TAG 操作清单（无对应 Task + Review 即为治理缺口）

**设计定位**（ADR-0030-bis SMB 原则）：

- 行为账本，不是防火墙；记录是强制的，阻断是可选的（v2.x 再加）
- stateless logging only，无 approval_token、无 policy engine、无状态机
- Authority Rule：风险分类决策在 MCP Interceptor，不在 Agent 执行层（ADR-0030 §四）

**测试**：新增 23 个 governance 单元测试（`mcp/tests/test_governance.py`），覆盖 Skill Resolver、Event Logger（线程安全）、Middleware on_call_tool 合约

**升级方式**：
```bash
pip install -U fcop-mcp
# 或
uvx --refresh fcop-mcp
```

---

## [1.1.1] — 2026-05-11

### fix(mcp) — 补发 fcop-mcp 1.1.1：Review 工具层（4 个工具）

**问题**：`fcop-mcp 1.1.0` PyPI wheel 发布时遗漏了 v1.1 新增的 4 个 Review MCP 工具，
导致 PyPI 版本（26 工具）与 GitHub main 源码（30 工具）不一致。

**本次修复**：`fcop-mcp` 版本从 `1.1.0` 升至 `1.1.1`，补入以下 4 个工具：

- **`write_review`** — 写入 REVIEW 文件（治理层决策，per ADR-0017/0025）
- **`list_reviews`** — 列出 REVIEW 文件，支持按 reviewer / subject / decision 过滤
- **`read_review`** — 读取单条 REVIEW 文件全文
- **`mark_human_approved`** — 为 `decision=needs_human` 的 REVIEW 落人工批准记录（per ADR-0026）

**变更范围**：仅 `fcop-mcp` 版本号 bump（`1.1.0` → `1.1.1`）；`fcop` 库版本不变（`1.1.0`）。
工具代码在 `1.1.0` 发布前已完整合入 `mcp/src/fcop_mcp/server.py`，本次为发布补丁。

**升级方式**：
```bash
pip install -U fcop-mcp
# 或
uvx --refresh fcop-mcp
```

---

## [1.1.0] — 2026-05-10

### feat — Agent Governance Layer, Task Risk Level, Human Approval, Skill Tools Risk Metadata

FCoP v1.1.0 是第一个 MINOR 版本，完全向后兼容 v1.0.x。5 个新字段对应 5 份 ADR：

**ADR-0023 — `Agent.layer` 形式化为协议字段**
- `agent.schema.json` 中 `layer: worker | governance | admin` 升格为有运行时合约的协议字段
- 运行时必须拒绝编程式创建 `layer: admin` agent
- `governance` agent 不得出现在 TASK/REPORT `recipient` 字段

**ADR-0024 — `Task.risk_level`**
- `ipc-envelope.schema.json` TASK 定义新增 `risk_level: low | medium | high | irreversible`（默认 `medium`）
- `models.py` 新增 `RiskLevel` 枚举
- `TaskFrontmatter.risk_level` 字段，默认 `RiskLevel.MEDIUM`
- `Project.write_task(risk_level=...)` 新增可选参数
- `fcop.core.schema.normalize_risk_level()` 公开 API

**ADR-0025 — `Review.decision = needs_human`**
- `review.schema.json` `decisionEnum` 从 4 值扩展至 5 值，新增 `needs_human`
- `ReviewDecision.NEEDS_HUMAN` 枚举值
- `write_review(decision="needs_human")` 不再被拒绝
- 移除 `test_review_no_v12_features.py`（ADR-0017 deferral 解除），新增 `test_review_v11_features.py`

**ADR-0026 — `Review.human_approval`**
- `review.schema.json` 新增 `human_approval` 属性（含 `humanApproval`、`humanApprovalEvidence` $defs）
- `models.py` 新增 `HumanApprovalChannel`、`HumanApprovalDecision`、`HumanApprovalEvidence`、`HumanApproval` dataclass
- `Review.human_approval: HumanApproval | None` 字段
- `Project.mark_human_approved(review_id, approver, decision, channel, ...)` 新增 API

**ADR-0027 — `Skill.tools[]` 风险元数据**
- 新增 `skill.schema.json`（`fcop://schemas/skill/v1.1.json`）
- `models.py` 新增 `SkillTool`、`Skill` dataclass
- `fcop.SCHEMA_NAMES` 从 7 个扩展到 8 个

---

## [1.0.1] — 2026-05-10

### feat(mcp) — 新增 `fcop://spec` / `fcop://spec/en` 资源（2026-05-10）

- **`fcop.rules.get_spec(lang)`**：新 API，从 wheel 内读取完整 FCoP v1.0 规范（中文 / 英文）
- **`fcop://spec`**：新 MCP 资源，返回 `spec/fcop-runtime-protocol-v1.0.zh.md`（中文，参考译文）
- **`fcop://spec/en`**：新 MCP 资源，返回 `spec/fcop-runtime-protocol-v1.0.md`（英文，权威版）
- 两份规范文件随 wheel 打包（`src/fcop/rules/_data/fcop-spec-v1.0.{zh,en}.md`）
- `docs/mcp-tools.md` 更新资源数量（12 → 14）并记录新条目
- 依赖两者 `pyproject.toml`：`Development Status :: 4 - Beta` → `5 - Production/Stable`
- `mcp/pyproject.toml` description：`fcop 0.7.x` → `fcop 1.x`
- `mcp/README.md` Stability 章节更新为 `1.x` + 升级提示指向 MIGRATION-1.0.md

### Docs — 全局路径迁移对齐（2026-05-10）

- **49 个文件** 完成 `docs/agents/` → `fcop/` 迁移——覆盖：
  模板文件（`letter-to-admin` × 2、`agent-install-prompt` × 2）、
  41 个团队角色模板（solo / dev / media / mvp / qa 全部中英双语）、
  essays 目录结构示例、`docs/mcp-tools.md`、`fcop-README.pypi.md`
- **历史性文件保留**（正确上下文）：CHANGELOG 历史条目、MIGRATION-1.0.md、
  旧版 release notes、`docs/agents/` 运行时日志

### Docs — AI OS 定位与七大核心概念写入运行时规则（2026-05-10）

- **`fcop-rules.mdc` → v2.1.0**：在 Purpose 节后新增双语小节
  "FCoP 的定位与七大核心概念 / Protocol Position & Seven Core Concepts"：
  - AI OS 协议栈三层图示（Application / FCoP / Host·LLM）
  - 七大核心概念对照表（Agent · IPC · Encoding · Event · Failure · Boundary · Audit）
  - 指向 `spec/fcop-runtime-protocol-v1.0.md` 的规范性引用
- **`fcop-protocol.mdc` → v1.9.0**：
  - 删除 v1.7.0 "Rule 9 commentary 待补" 占位 note
  - 新增 "Rule 9 Commentary" 完整节（9.1–9.4）：
    - 9.1 REVIEW 文件命名规范 + YAML frontmatter 必填字段
    - 9.2 Boundary 三层表 + `can`/`cannot` 示例 + agent 自查清单
    - 9.3 Failure 4 类触发场景 × 5 类恢复动作说明表 + SDK 示例
    - 9.4 Event 12 类型清单 + `subscribe_events` / `poll_once()` 使用模式
- **四个部署目标全部重新生成**（`AGENTS.md` / `CLAUDE.md` / `.cursor/rules/`）
  → rules 2.1.0 / protocol 1.9.0

### Docs — spec 入口与架构梳理（2026-05-10）

- **`spec/fcop-spec.md`** 入口从旧 `fcop-spec-v1.0.3.md`（0.7.x 遗留）
  更新为 `fcop-runtime-protocol-v1.0.md`（v1.0 权威版）；
  明确版本历史：v1.0（当前正式版）vs v0.7.x（遗留参考）
- **`.mdc` 文件架构澄清**：在 spec Appendix B 中将 `fcop-rules.mdc` /
  `fcop-protocol.mdc` 归入 "B.2b Host Adapter Artefacts (Cursor)"，
  与核心协议文件明确分层
- **四个部署目标分工文档化**：
  `.cursor/rules/*.mdc`（Cursor）/ `AGENTS.md`（Codex/Devin）/
  `CLAUDE.md`（Claude Code CLI）

### Docs — 完善 v1.0.0 文档（2026-05-10）

- **术语统一**：全面将「冻结七个核心抽象」替换为「固化七大核心概念：Agent、Encoding、IPC、Event、Failure、Boundary、Audit」（5 个文件：spec / CHANGELOG / README.zh.md / 1.0.0.md / MIGRATION-1.0.md）
- **spec 英中分离**：`spec/fcop-runtime-protocol-v1.0.md` 清理为纯英文；
  新建 `spec/fcop-runtime-protocol-v1.0.zh.md` 作为完整中文平行版（informative）
- **spec §7.1** 节标题改为 "Stability of the seven core concepts (normative)"
- **spec Appendix B** 升级为 4 类分组文档地图（B.1 规范 / B.2 ADR / B.3 用户指南 / B.4 发布记录）
- **README.md + README.zh.md** 新增「How to read FCoP docs / 如何阅读 FCoP 文档」导航表
- **docs/releases/1.1.0.md** 刷新为 v1.0.0 final 之后的实际状态

## [1.0.0] — 2026-05-09 — AI OS Protocol Layer (final)

### 中文 TL;DR

`fcop@1.0.0` 是把 0.7.x 的"AI 协作规则"完整升级为 **AI OS 协议层 /
Agent Runtime Protocol** 的第一个稳定版。**协议表面与 `1.0.0-rc.1`
按位相同**——本 final 仅在 RC 之上增量交付 ADR-0022 Phase 2
（`Project.workspace_dir` 重构 + 4-detect + `workspace_layout`
introspection property）+ `docs/MIGRATION-1.0.md` 用户向迁移指南
+ release notes finalize。七大核心概念（Agent、Encoding、IPC、Event、Failure、Boundary、Audit）最小语义合约**已固化为稳定标准**，任何修改
协议的变更要求 MAJOR bump 到 v2.x。

### English TL;DR

`fcop@1.0.0` is the first stable release that promotes 0.7.x's
"AI collaboration rules" into a real **AI OS Protocol Layer /
Agent Runtime Protocol**. **Protocol surface is bit-identical to
`1.0.0-rc.1`** — this final ships only incremental deliverables
on top of the RC: ADR-0022 Phase 2 (`Project.workspace_dir`
refactor + 4-detect + `workspace_layout` introspection property),
`docs/MIGRATION-1.0.md` user-facing migration guide, and release
notes finalize. The minimum semantic contract of seven
abstractions is **frozen forever**; any protocol-breaking change
requires a MAJOR bump to v2.x.

> **Status**: Final release. Any project that ran on
> `1.0.0-rc.1` keeps running on `1.0.0` with zero changes; any
> 0.7.x project can opt into v1.0 with `pip install --upgrade
> fcop fcop-mcp` + an optional `fcop migrate-workspace --apply`
> run.
>
> Full release notes: [`docs/releases/1.0.0.md`](./docs/releases/1.0.0.md).

### Delta vs `1.0.0-rc.1`

Only the items below are new since RC. Everything else is identical.

#### Added — `fcop` library

- **`Project.workspace_dir` Phase 2 改造 — ADR-0022 第二阶段全量
  落地**（TASK-20260509-012，commit `861713b`，per
  [ADR-0022 §Implementation §Phase 2](./adr/ADR-0022-workspace-directory-convention.md#implementation)）。
  RC 阶段以 `fcop migrate-workspace` CLI（Phase 1，TASK-008）独立
  交付；本阶段把 `Project` 类的 workspace 路径决议从 hard-coded
  `docs/agents/` 升级为可配置 + 自动 detect。
  - **新构造参数**：`Project(path, *, strict=True, workspace_dir=None)`。
    `workspace_dir=None`（默认）触发 4 种 detect：
    1. `<root>/fcop/` 存在  → use it（v1.0 默认，无 warning）
    2. 仅 `<root>/docs/agents/` 存在 → use it + `DeprecationWarning`
       指向 `fcop migrate-workspace`
    3. 两者并存                → `ConfigError` ABORT，提示用 explicit
       override 消歧
    4. 两者均不存在            → 默认 `<root>/fcop/`（v1.0 fresh init）
  - 显式 `workspace_dir="docs/agents"` / 任意相对/绝对路径 → 永远合
    法，永不 warn（escape hatch 永久保留）
  - **新公开 property**：`Project.workspace_layout` →
    `"v1"` / `"legacy"` / `"explicit"`，便于下游工具识别项目状态
  - **路径 derivation 收敛**：8 个公开路径 properties（`tasks_dir` /
    `reports_dir` / `issues_dir` / `shared_dir` / `log_dir` /
    `reviews_dir` / `config_path` / `workspace_dir`）+
    `LETTER-TO-ADMIN.md` deposit 路径 + drift parser ledger
    prefixes 全部从 `self._workspace_root` 派生，单 Project 实例
    对应单 workspace
  - **MCP 端协同**：`init_project` / `init_solo` / `create_custom_team`
    reply 以及 `_letter_handover_block` 中 `LETTER-TO-ADMIN.md`
    引用路径动态化（基于 `project.workspace_dir.relative_to
    (project.path)`），确保 ADMIN 看到的路径与文件实际落地处一致
  - **测试**：`tests/test_fcop/test_project_workspace_dir.py`
    （新建，15 用例：`TestAutoDetect`(4) + `TestExplicitOverride`(4)
    + `TestPathPropertiesFollowWorkspace`(3 parametrize) +
    `TestIsInitializedHonoursWorkspace`(3) +
    `TestInitUnderExplicitWorkspace`(1)）
  - **既有测试 swap**：9 个 fcop test 文件 + 1 个 mcp test 文件
    53 处 hard-coded `docs/agents/` 期望批量改为 `fcop/`；
    `test_migrate_workspace.py` / `test_legacy_files_validate.py` /
    `test_encoding_schema.py` / `test_audit_drift.py` 故意保留
    （migration tool / legacy fixture / raw schema 用例）
  - **public_surface snapshot bump**：`Project.__init__` 新增
    `workspace_dir` kwarg + 新 property `workspace_layout` 进
    `tests/test_fcop/snapshots/public_surface.json`
  - **回归数据**：971 passed, 1 failed（pre-existing date-pinned
    mcp test 与本改动无关；从 Phase 2 改造前的 954 passed 上涨
    +17）

#### Added — docs

- **`docs/MIGRATION-1.0.md` 用户向 0.7.x → 1.0 迁移指南**
  （TASK-20260509-013，per ADR-0022 §"Tests Checklist" 最后一项）。
  覆盖 8 章节：TL;DR / 心智模型（3 个独立 breaking 维度）/ 协议
  framing 升级 / workspace 目录迁移 3 选项 + auto-detect 矩阵 +
  完全 rollback / 4 新抽象 walkthrough（REVIEW / Failure /
  Boundary / Event）/ JSON Schema 形式化 / 6 类常见踩坑 / 估时表
  + 进一步阅读链接。
- **README.md / README.zh.md 头部加 v1.0 升级 callout**，与既有
  0.5.x → 0.6 callout 并列；指向 `docs/MIGRATION-1.0.md` +
  ADR-0022。
- **`docs/releases/1.0.0.md` finalize**（commit `03810f4`）：去
  DRAFT marker，重写为 final canonical release notes（双语 TL;DR
  + 7-step release commands + annotated tag message template +
  RC-issue 回链）。

#### Changed — `fcop-mcp` server

- **init reply LETTER 路径动态化**（同 TASK-012，commit `861713b`）：
  `init_project` / `init_solo` / `create_custom_team` 三处 reply
  + `_letter_handover_block` 不再硬编码 `docs/agents/LETTER-TO-ADMIN.md`，
  改为从 `project.workspace_dir.relative_to(project.path)` 动态拼装。
  v1.0 default 项目看到 `fcop/LETTER-TO-ADMIN.md`，0.7.x legacy 项目
  仍看到 `docs/agents/LETTER-TO-ADMIN.md`，explicit override 项目
  看到自定义路径。

#### Release plumbing

- **Version bump**：`1.0.0rc1` → `1.0.0`
  （`src/fcop/_version.py` + `mcp/src/fcop_mcp/_version.py`）
- **`fcop-mcp` pin relax**：`fcop>=1.0.0rc1,<2.0` → `fcop>=1.0,<2.0`
  （`mcp/pyproject.toml`），允许 v1.x MINOR 漂移
- **CHANGELOG fold**：`[Unreleased]` → `[1.0.0]`，本段以下 RC delta
  归档于此

## [1.0.0-rc.1] — 2026-05-09 — AI OS Protocol Layer release candidate

### 中文 TL;DR

把 0.7.x 的 "AI 协作规则" 升级为 **AI OS 协议层 / Agent Runtime
Protocol**。7 抽象（Agent / IPC / Encoding / Event / Failure / Boundary
/ Audit）最小语义合约 frozen + reference impl 全部 wiring 完成 +
新增 `fcop migrate-workspace` CLI（per ADR-0022）。0.7.x 文件 100%
向后兼容；v1.x 之后不再允许 workspace 默认迁移。

### English TL;DR

Promotes 0.7.x's "AI collaboration rules" to a real **AI OS protocol
layer / Agent Runtime Protocol**. Seven abstractions (Agent / IPC /
Encoding / Event / Failure / Boundary / Audit) frozen at a
minimum-semantic-contract level + reference implementation fully
wired + new `fcop migrate-workspace` CLI (per ADR-0022). All 0.7.x
files remain 100% backward compatible; no further workspace default
migrations after v1.x.

> **Status**: Release candidate. Protocol surface frozen; only bug fixes
> + non-protocol release tooling will land before final `1.0.0`.
>
> 7 抽象 reference-impl wiring **100% 完成**。这是 `fcop@1.x` 系列的
> 第一个候选发车版本——把 0.7.x 的"AI 协作规则"完整升级为
> **AI OS Protocol Layer / Agent Runtime Protocol**。

### Highlights

- **协议本体重 framing**：FCoP 不再是"协作规则"，而是 **AI OS 的 POSIX
  层** —— 7 核心抽象（Agent / IPC / Encoding / Event / Failure /
  Boundary / Audit）的最小语义合约（per ADR-0015）。
- **7 份 JSON Schema** v1.0 frozen 在 `spec/schemas/`，作为协议唯一
  真相（per ADR-0016）。schemas 通过 `referencing.Registry` 跨文件
  解析 `$ref`；wheel 内副本 byte-identical 守门。
- **4 类 IPC envelope** 全落地：TASK / REPORT / ISSUE / **REVIEW**
  （新增 v1.0 Audit 抽象，per ADR-0017；4 值 decision，
  `needs_human` 刻意推迟 v1.2）。
- **Failure & Recovery 语义**（per ADR-0019）：4 类失败枚举（TIMEOUT
  / CRASH / DEADLOCK / DRIFT）+ 5 类恢复枚举（RETRY / RESUME /
  ROLLBACK / ABORT / ESCALATE）+ Session 恢复 hook。RETRY/RESUME/
  ROLLBACK 是 plan-only（不引入 git 依赖）；ABORT/ESCALATE 实际写盘。
- **Boundary 抽象**（per ADR-0020）：10 token capability 词表 +
  3 layer 默认 bundle（worker / governance / admin）+ 4 条 normative
  规则（NO_ADMIN_PROGRAMMATIC_CREATE / NO_GOVERNANCE_FISSION /
  NO_WORKER_REVIEWS_GOVERNANCE / EXPLICIT_OVERRIDES_LAYER）。
- **Event Model**（per ADR-0018）：12 事件枚举 + polling watcher
  reference impl（pure functions，不引入后台线程；caller 显式调
  `Project.poll_once`）+ 同步 callback 触发。事件不持久化，仅在
  订阅瞬间发出。
- **公开 API 增量约 30 项**，全 additive：从 `fcop` 顶层可 import
  `Review` / `Failure` / `Recovery` / `Event` / `EventSubscription`
  / `BoundaryViolation` / 12 个 Action/Type enum / `Project` 方法
  `write_review` / `report_failure` / `apply_recovery` /
  `recover_session` / `assert_boundary` / `subscribe_events` /
  `poll_once` 等。详细清单见上一段每个 TASK 的子 section。
- **0.7.x 100% 兼容**：所有 0.7.x TASK / REPORT / ISSUE 文件不动可用；
  `Project(workspace_dir="docs/agents/")` 显式传永远合法（escape
  hatch 永久保留，per ADR-0022）；既有公开 API 全部不变；
  `_emit_event_stub` 设计为 bridge，TASK-006 22 个测试零修改通过。
- **测试规模**：从 0.7.2 的约 600 用例增长到 871（仅 fcop 库；
  fcop-mcp 65 个）。

### Stats — 7 抽象 reference-impl wiring 集成总账

| 任务 | commits | 文件次 | +/- | 测试用例 |
|---|---|---|---|---|
| TASK-002（reframing） | 6 | ~30 | ~+3500 / ~-150 | 文档 |
| TASK-003（schema 物化） | 2 | ~20 | ~+1500 / 0 | 116 |
| TASK-004（schema 校验器 + REVIEW） | 3 | 35 | +3885 / -8 | 58 |
| TASK-005（Boundary） | 4 | 17 | +1731 / -16 | 49 |
| TASK-006（Failure） | 4 | 15 | +2476 / -23 | 46 |
| TASK-007（Event） | 4 | 17 | +2277 / -54 | 43 |

详细每一段的子条目见下面（按 TASK 时间倒序）。

### Changed — bundled rules / 协议规则文件

- **`fcop-rules.mdc` 1.8.0 → 1.9.0**（TASK-20260509-010，per
  [ADR-0015](./adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md)
  §execution roadmap）：
  - 新增 **Rule 9 · v1.0 Capabilities**（4 子段对应 v1.0 reframing
    新增的 4 抽象，纯 additive 不改 Rule 0..8）：
    - 9.1 REVIEW envelope（第 4 类 IPC，per ADR-0017）
    - 9.2 Agent Boundary（layer + can/cannot capability，per ADR-0020）
    - 9.3 Failure & Recovery（4 failure × 5 recovery，per ADR-0019）
    - 9.4 Event Model（12 事件 + subscribe_events 显式 poll，per ADR-0018）
  - frontmatter `fcop_rules_version` 1.8.0 → 1.9.0；body changelog
    顶部加 1.9.0 段
- **`fcop-protocol.mdc` 1.6.0 → 1.7.0**：
  - 顶部加 "v1.0 Capabilities pointer" callout，指向
    `spec/schemas/`、ADR-0017..0020、`docs/getting-started.md` 速查
    （Rule 9 的详细 commentary 留 v1.0 final 之前的独立 task）
  - Protocol Version Log 顶部加 v1.7 双语条目
  - 顶部 nav "Rule 0–8" → "Rule 0–9"
- **既有 Rule 0..8 主体不变**——v1.0 是 additive expansion of contract
  （per ADR-0003 §1.x SemVer §MINOR additive），所有既有规则继续生效

### Added — `fcop` CLI

- **`fcop migrate-workspace` 子命令 — 0.7.x → v1.0 workspace 迁移工具**
  （TASK-20260509-008，per [ADR-0022](./adr/ADR-0022-workspace-directory-convention.md)）：

  把 `docs/agents/` 迁到 `fcop/`（顶层协议命名空间），保留 git 历史。
  RC 阶段先交付 CLI 本身；`Project` 默认目录改造留 v1.0 final。

  - **`fcop` console-script entry point bump**：从
    `fcop._compat_cli:main` 升级为 `fcop.cli._main:main`——subcommand
    派发器；`fcop`（无参）仍打印 0.5→0.6 MCP 迁移信息以兼容历史
    用户（per ADR-0002 §0.6 入站契约）
  - **`fcop migrate-workspace`**：
    - 默认 dry-run；`--apply` 才真改盘
    - git-aware：在 git 工作树 + path 已 tracked 时自动 `git mv`，
      否则 fallback `shutil.move`，附 warning
    - 幂等：已迁移的 tree 上 `--apply` 是 no-op，退出 0
    - both-exist 防呆：若 `docs/agents/` 与 `fcop/` 同时存在则 ABORT
      （退出 2），绝不自动合并（per ADR-0022 §"启动时 detect 行为"）
    - 留痕：迁移成功后写 `fcop/MIGRATED_FROM_DOCS_AGENTS.md`
      含时间戳、源路径、目标路径、CLI 版本号
    - 顾问扫描：列出 `.gitignore` / `.cursor/rules/*.mdc` /
      `AGENTS.md` / `CLAUDE.md` / `README*.md` 中 `docs/agents`
      字符串引用——**仅列出，不自动改写**（避免误伤用户文档；
      per ADR-0022 §"Design Details" item 3）
    - 选项：`--apply` / `--target=path` / `--source=path` /
      `--project-root=path`
  - **新增模块**：
    - `src/fcop/cli/__init__.py`（CLI namespace 占位 + docstring）
    - `src/fcop/cli/_main.py`（subcommand 派发器；63 行）
    - `src/fcop/cli/migrate_workspace.py`（plan/apply/render_summary
      + argparse glue；~340 行）
  - **测试**：`tests/test_fcop/test_migrate_workspace.py` 共 25 用例：
    - `TestPlan`（7）：canonical / already_migrated / source_missing /
      conflict / advisory hits / 自定义 source 与 target / surprise
      entry note
    - `TestApply`（6）：shutil fallback / git mv 保留历史 / 幂等 /
      conflict raises / source-missing no-op / breadcrumb 内容
    - `TestRenderSummary`（3）：dry-run hint / applied 不带 hint /
      advisory 显示
    - `TestCli`（6）：dry-run / apply / conflict 退 2 / 自定义 target /
      bare `fcop` 走 legacy / `--help` 退 0
    - `TestRunStandalone`（2）：standalone `mw.run()` 入口 dry-run /
      apply
  - **测试调整**：
    - `tests/test_fcop/test_compat_cli.py` ::
      `test_console_script_resolves_to_cli_main`：放宽接受
      `fcop.cli._main:main`（v1.0+） 或 `fcop._compat_cli:main`
      （未 reinstall 的老 editable install），加历史说明 docstring
  - **Phase 2 已落地**（RC 之后、final 之前；TASK-20260509-012，
    commit `861713b`）：
    - `Project()` 构造加 `workspace_dir=` 参数 + 4 detect 场景
      （`fcop/` / 仅 `docs/agents/` / 都有 / 都无）+ 公开
      `workspace_layout` property（`"v1"` / `"legacy"` /
      `"explicit"`）
    - 检测到 `docs/agents/` 时打 `DeprecationWarning` 指向
      `fcop migrate-workspace`；两者并存时 `ConfigError` ABORT
    - `Project` 内 8 个 `*_dir` / `config_path` properties + drift
      parser ledger prefixes + `LETTER-TO-ADMIN.md` deposit 全部
      derive from `self._workspace_root`
    - MCP server `init_project` / `init_solo` / `create_custom_team`
      reply 中 LETTER 路径动态化
    - `tests/test_fcop/test_project_workspace_dir.py` 新建 15 用例；
      9 个 fcop test 文件 + 1 个 mcp test 文件 53 处 hard-coded
      `docs/agents/` 期望批量 swap 为 `fcop/`
    - 详见 [ADR-0022 §Implementation §Phase 2](./adr/ADR-0022-workspace-directory-convention.md#implementation)
  - **仍 deferred 到 v1.0 final**：`MIGRATION-1.0.md` 用户向迁移
    指南（拆到 TASK-013）

### Added — `fcop` library

- **Event 抽象端到端 — v1.0 7 抽象闭合最后一环**（TASK-20260509-007
  R1+R2，per ADR-0018 + ADR-0019）。reference-impl wiring 进度
  **4/7**——Event 落地后 v1.0.0 RC 候选条件全达成。
  - 新模块 `fcop.core.events` 暴露 polling watcher 的纯函数 reference
    impl：`scan_workspace(workspace_dir, project_root)` /
    `compute_diff(prev, curr)` / `make_event` / `make_event_id` +
    `WatcherState` / `FileSnapshot` dataclass + `WATCHER_ID` 常量。
  - 公开 5 个新符号（4 dataclass/enum + 1 Subscription）：`Event` /
    `EventSource` / `EventSourceKind` / `EventType`（12 值，与
    `event.schema.json` 词表对齐）+ `EventSubscription` 句柄。
  - `Project.subscribe_events(types, callback)` 注册订阅；返回
    `EventSubscription`，调 `unsubscribe()` 取消。`types=None` 表示
    订阅所有 12 类；字符串自动 coerce 为 `EventType`。
  - `Project.poll_once()` 显式跑一次 polling 周期：scan + diff +
    dispatch + 缓存当前 state。**v1.0 不引入后台线程**（per TASK-007
    §决议 3 + 7），caller 负责调度。
  - `Project.workspace_dir` property —— v1.0 显式 accessor，
    `tasks_dir.parent` 的等价别名。
  - 12 类事件中 8 类（TASK_CREATED / TASK_ACCEPTED / TASK_BLOCKED /
    TASK_COMPLETED / REPORT_FILED / REVIEW_DECIDED / ROLE_SWITCHED +
    部分 BOUNDARY_VIOLATED）由 polling 派生；剩 4-5 类
    （FAILURE_DETECTED / RECOVERY_INITIATED / RECOVERY_COMPLETED /
    SESSION_LOST / 同步 BOUNDARY_VIOLATED）由 Project 内部代码
    同步触发。
  - **接住 TASK-005/006 的 stub 钩子**：`Project.assert_boundary` 现
    在 raise 之前 emit `BOUNDARY_VIOLATED`；`apply_recovery` 头尾
    emit `RECOVERY_INITIATED` / `RECOVERY_COMPLETED`；
    `recover_session` session_not_found 时 emit `SESSION_LOST`。
    `_emit_event_stub` 改为 bridge——既保留 TASK-006 测试观察的
    legacy log（`_emit_event_stub_calls`），又派发到真实事件总线。
  - 测试套件：`test_core_events.py`（23 用例）+
    `test_project_events.py`（20 用例）。
- **Failure & Recovery 抽象端到端**（TASK-20260509-006 R1+R2，
  per ADR-0019）。v1.0 7 抽象 reference-impl wiring 进度
  **3/7**——Failure 落地。
  - 新模块 `fcop.core.recovery` 暴露 5 类 RecoveryAction 的 pure
    reference-impl 函数：`make_retry_plan` / `make_resume_payload` /
    `make_rollback_plan` / `make_abort_artifact` /
    `make_escalate_artifact` + `parse_session_id`（接受
    `TASK-...:agent` 与 0.7.x `sess-YYYYMMDD-...` 两种形状）+
    `build_recovery_record` 工厂。
  - 公开 13 个新符号：`Failure` / `Recovery` / `RetryPlan` /
    `ResumePayload` / `RollbackPlan` / `RecoveryOutcome` /
    `SessionRecoveryResult` / `FailureReceipt`（8 dataclass）+
    `FailureType` / `RecoveryAction` / `SessionRecoveryAction`
    （3 enum）+ `Project.report_failure` / `Project.apply_recovery`
    / `Project.recover_session`（3 方法）。
  - `Project.report_failure(failure)` 触发 stub 事件
    `FAILURE_DETECTED`（TASK-007 接事件后换成真实推送）+ 返回
    `FailureReceipt`，**不写盘**。
  - `Project.apply_recovery(failure, action=None, ...)` 把 5 类
    Recovery 映射到 reference impl：RETRY/RESUME/ROLLBACK 是 plan-only
    （per TASK-006 §决议 3，v1.0 不引入 git 依赖；ROLLBACK
    `executed=False` 永远）；ABORT 写一份 `status: aborted` REPORT；
    ESCALATE 写一份 ISSUE 给 leader。
  - `Project.recover_session(session_id, action, ...)` action 仅 3 值
    `resume` / `rollback` / `abort`（RETRY / ESCALATE 不是 session
    级，会被拒）。
  - 测试套件：`test_core_recovery.py`（24 用例）+
    `test_project_failure.py`（22 用例）。
- **JSON Schema 校验基础设施**（TASK-20260509-004 R1）。新增模块
  `fcop.core.jsonschema_validator` 暴露
  `validate_envelope_frontmatter(fm, type)` /
  `validate_record(record, schema_name)` /
  `normalize_for_json(value)` 三个函数，以及模块级 `SCHEMA_REGISTRY` /
  `SCHEMA_NAMES` / `ENVELOPE_TYPES` / `BUNDLED_SCHEMA_DIR` 常量。7 份
  v1.0 协议 schema（`spec/schemas/*.schema.json`）随 wheel 打包到
  `src/fcop/_data/schemas/`，跨文件 `$ref` 通过 `referencing.Registry`
  按 `$id` 解析。**opt-in**：现有 `write_task` / `write_report` /
  `write_issue` 路径完全不变，仅 `write_review` 启用了校验。
- **`Project.write_review` / `read_review` / `list_reviews` /
  `archive_review`**（TASK-20260509-004 R2，per ADR-0017）。FCoP v1.0
  引入的第四种 IPC envelope —— Audit 抽象的端到端实现。文件落在
  `docs/agents/reviews/`，归档到 `log/reviews/`。
- **`Project.reviews_dir` property**（v1.0）。指向
  `<project>/docs/agents/reviews/`。
- **`Review` dataclass + `ReviewDecision` / `ReviewSubjectType` enums**
  从顶层 `fcop` 包导出。`ReviewDecision` 为 4 值闭枚举
  （`approved` / `rejected` / `needs_changes` / `abstained`）；
  `needs_human` **刻意推迟到 v1.2**（per ADR-0017），schema 与
  dataclass 双层拒。
- **`fcop.core.filename` 新增 REVIEW 文件名 grammar**：
  `REVIEW_FILENAME_PREFIX` / `REVIEW_FILENAME_RE` /
  `REVIEW_SUBJECT_SHORT_RE` / `ReviewFilename` /
  `parse_review_filename` / `build_review_filename`，并把
  `FilenameKind` 加 `"review"` 选项。
- **`fcop.core.frontmatter` 新增 REVIEW 序列化**：
  `parse_review_frontmatter` / `serialize_review_frontmatter` /
  `assemble_review_file`。
- **`tests/test_schemas/` 测试套件**（10 份文件，116 用例）。每份
  schema ≥ 3 用例（合法/缺必填/非法枚举），加横切的 in-sync 守门
  与全部 0.7.x envelope 文件回归（I5 见证）。
- **`tests/test_fcop/test_project_reviews.py` + 关联的 filename /
  frontmatter / no-v12-features 测试**（共 4 份，58 用例）。

### Changed — `fcop` library

- **`Project.write_report` 接受 `status="aborted"`**（TASK-20260509-006
  R2）。原 Literal `"done" | "blocked" | "in_progress"` 扩展为四值，
  追上 `ipc-envelope.schema.json` 已 frozen 的 `aborted` enum。这是
  ABORT recovery 写盘前提；纯 additive，不影响现有 callers。
  `models.Report.status` Literal 同步扩展。


- **`spec/schemas/ipc-envelope.schema.json` 放宽以满足 I5**（TASK-004
  R1）：`TASK.subject` 改 SHOULD（0.7.x 常把 subject 写在 markdown
  H1）；REPORT 接受 `references` / `related_task` / `related_issues` /
  `report_id`（0.7.x 字段别名），仍推荐新文件用 `ref_task`；新增
  `task_id` / `session_id` 为已知可选字段。

### Added — `fcop` library（TASK-005 / Boundary 抽象）

- **`fcop.core.boundary` 模块**（per ADR-0020）。10 token v1.0
  capability 词表、3 layer × 默认 bundle、4 条 normative boundary
  规则（NO_ADMIN_PROGRAMMATIC_CREATE / NO_GOVERNANCE_FISSION /
  NO_WORKER_REVIEWS_GOVERNANCE / EXPLICIT_OVERRIDES_LAYER）+ 1 条
  advisory（UNKNOWN_CAPABILITY warning）+ `lookup_capability(role,
  config)` / `validate_action(actor, action, target=)` 公开函数。
- **`Project.boundary_violations` / `Project.assert_boundary` 公开
  方法**。前者返回 `BoundaryViolation` 列表（永不 raise），后者
  违规即 raise `BoundaryViolationError`。warning 级别（如
  UNKNOWN_CAPABILITY）不进 raise。
- **`AgentLayer` / `Capability` / `BoundaryViolation` dataclasses +
  `BoundaryViolationError` 异常**从顶层 `fcop` 包导出。
- **`Project.write_review` 接进 boundary 强制**——reviewer →
  `review_decision` → 推断的 subject sender role 走 `assert_boundary`，
  违规即 raise，文件不创建。这是 v1.0 第一个**默认强制 boundary**
  的写入路径；write_task / write_report / write_issue **不**接
  （0.7.x 兼容性，留给 v1.1 通过 `enforce_boundary` 参数 opt-in）。
- **`fcop.json.roles` 接受 dict-form `layer` / `can` / `cannot` 字段**。
  解析后落进 `TeamConfig.extra["_role_labels"][code]`，
  `lookup_capability` 从这条路径读。`layer` 类型必须 string，
  `can` / `cannot` 必须 list[str] 或 null。**不引入 `Role` dataclass
  以保 ADR-0003 additive-only**（per TASK-005 §决议 1）。
- **`tests/test_fcop/test_boundary.py` × 25 用例**：词表对齐 schema、
  4 规则各 ≥ 2 用例、layer 默认与 ADR §decision 表对照、
  EXPLICIT_OVERRIDES_LAYER 优先级、UNKNOWN_CAPABILITY warning。
- **`tests/test_fcop/test_project_boundary.py` × 14 用例**：
  Project.boundary_violations / assert_boundary / write_review 端到端
  + admin layer 拒收。
- **`tests/test_fcop/test_core_config_role_capability.py` × 10 用例**：
  dict-form roles 的 layer/can/cannot 解析 / round-trip / 类型校验
  / string-form backward compat。

### Added — packaging

- `pyproject.toml` `tool.hatch.build.targets.wheel` `include` glob 加
  `src/fcop/_data/schemas/*.schema.json`，确保 wheel 内含 7 份 v1.0
  协议 schema。

### Internal

- 中文为主、英文括注的内部文档约定从 `TASK-20260509-004` 起恢复
  （此前 TASK-002 / TASK-003 / 多份 ADR 临时全英文）。

## [0.7.2] - 2026-04-27

Metadata-only patch release. **No behaviour change**, no new APIs,
no new MCP tools, no protocol bump. Sole purpose: close
`ISSUE-20260427-007` (rules.mdc frontmatter version stale at
`1.7.0` while body changelog and content are `1.8.0`) and harden
the build against the *class* of bug it represents — the third
"multi-line edit, one edit dropped" incident in the 0.7.x cycle
(after `ISSUE-20260427-006` dependency pin and the REPORT-005
"yank" wording drift, both fixed in 0.7.1). See
[`docs/releases/0.7.2.md`](./docs/releases/0.7.2.md) for the
post-mortem.

### Fixed — `fcop` library

- **`fcop-rules.mdc` frontmatter version (`ISSUE-20260427-007`).**
  `src/fcop/rules/_data/fcop-rules.mdc` shipped in 0.7.1 with
  `fcop_rules_version: 1.7.0` in its frontmatter while the body
  changelog and rule text were already `1.8.0` (sub-agent
  identity clause in Rule 1, `AMEND-*` / `-v2` removal in Rule 5,
  Rule 0.a.1 applicability clarification). `fcop_report()`
  therefore reported `rules: 1.7.0`, masking the fact that the
  bundled rules already behaved as 1.8.0. Frontmatter is now
  `1.8.0`, in lockstep with the body.

### Added — `fcop` library tests (regression guard)

- **`tests/test_fcop/test_rules_metadata_consistency.py`.**
  Three new tests that read both `fcop-rules.mdc` and
  `fcop-protocol.mdc` and assert the frontmatter
  `fcop_rules_version` / `fcop_protocol_version` fields equal the
  highest version listed in the body changelog (`**X.Y.Z changes
  ...**` for rules, `- **vX.Y** (date)` for protocol). This makes
  the *class* of bug behind ISSUE-007 — and equally behind
  ISSUE-006 (multi-line edit, one edit dropped) — unshippable: a
  PR that bumps body but forgets frontmatter (or vice versa) now
  fails the test suite before the wheel is built.

### Documentation

- `README.md` / `README.zh.md`: extended the **Recent releases**
  table with `0.7.0`, `0.7.1`, `0.7.2`. The previous entries
  stopped at `0.6.5`, so users following the table never saw the
  `RoleOccupancy` (0.7.0) or the role-uniqueness protocol bump
  (0.7.1) on the landing page.
- `mcp/README.md`: "Already on `0.6.x`" / "**Stability (0.6.x)**"
  upgraded to also speak about `0.7.x` (without dropping the
  0.6.x → 0.7.x migration anchor — that lives in
  [`docs/upgrade-fcop-mcp.md`](./docs/upgrade-fcop-mcp.md)).

### Operational

- No PyPI yank for `fcop-mcp 0.7.1` (mirrors the 0.7.0 decision).
  `0.7.2` is the higher version on PyPI, so any unpinned
  `pip install -U fcop-mcp` / `uvx --refresh fcop-mcp`
  automatically picks it up. Same rationale as 0.7.1 applies; see
  [`docs/releases/0.7.2.md`](./docs/releases/0.7.2.md) for the
  short version.

## [0.7.1] - 2026-04-27

Hotfix release rolling up the `fcop-mcp 0.7.0` dependency-pin
incident together with three protocol clarifications discovered
during dogfooding the same afternoon. See
[`docs/releases/0.7.1.md`](./docs/releases/0.7.1.md) for the
post-mortem on `ISSUE-20260427-006` and the rationale for closing
`ISSUE-20260427-001 / -004 / -005`.

### Fixed — `fcop-mcp` (release blocker)

- **`fcop-mcp 0.7.0` dependency pin (`ISSUE-20260427-006`).**
  `mcp/pyproject.toml` was published with the stale pin
  `"fcop>=0.6,<0.7"`, which made `uvx fcop-mcp` resolve `fcop 0.6.5`
  even though `fcop-mcp 0.7.0` imports symbols introduced in
  `fcop 0.7.0` (`RoleOccupancy`, `Project.role_occupancy()`,
  `OccupancyState`). Fresh installs hit `ImportError` on
  `fcop_report()` until `uv cache clean` was run by hand. The pin is
  now `"fcop>=0.7,<0.8"` and a regression test
  (`tests/test_fcop/test_pyproject_pins.py`) reads
  `mcp/pyproject.toml` and asserts that the `fcop` lower bound
  matches `fcop-mcp`'s minor — see ADR-0002 "Lockstep pin rule" for
  the formal rule. `fcop-mcp 0.7.0` stays on PyPI, **not yanked**:
  the dominant install path (`uvx fcop-mcp` / `pip install fcop-mcp`
  without a pin) already resolves to 0.7.1, so yank would not
  repair anyone currently broken — only `pip install -U` /
  `uvx --refresh` does. Yank is kept as a reversible fallback;
  rationale recorded in `docs/releases/0.7.1.md`.

### Protocol — `fcop_protocol_version: 1.6.0` / `fcop_rules_version: 1.8.0`

- **Rule 1 — sub-agent identity inheritance (`fcop`).** Rule 1 now
  explicitly states that sub-agents and worker subprocesses
  **inherit the parent session's bound role** and must not
  self-assign a different role code, even temporarily, to satisfy
  task language like "ME completes, COMMS reviews". A single
  agent driving multiple subprocesses is one role, not many.
  Detection now exists at audit time: `fcop_check()` flags any
  `session_id` that signs files under more than one role. Closes
  `ISSUE-20260427-004` and answers the AMEND-20260427-011 dogfood
  case where a parent session let a sub-process write a `REPORT-*`
  under a peer role. Source: `src/fcop/rules/_data/fcop-rules.mdc`.
- **Rule 0.a.1 — tripwire applies to all write paths (`fcop`).**
  Clarifies that the `task → do → report → archive` cycle binds
  every write path, not just MCP tools — raw shell, `git commit`,
  IDE-side edits, and external scripts are all in scope. The
  protocol cannot prevent these channels from running; what it
  guarantees is that the next `fcop_report()` / `fcop_check()`
  surfaces the drift loud and unmissable. Closes
  `ISSUE-20260427-001`. Source:
  `src/fcop/rules/_data/fcop-rules.mdc`.
- **Rule 5 — sequential corrections, no `AMEND-*` / `-v2` (`fcop`).**
  Rule 5's allowed-correction examples drop the `AMEND-*` and `-v2`
  filename patterns, which the `fcop` library never parsed. Append-
  only history is now expressed by allocating the next
  `REPORT-NNN` / `TASK-NNN` sequence number and cross-referencing
  the prior file in frontmatter — no special filename grammar
  required. Closes `ISSUE-20260427-005`. Source:
  `src/fcop/rules/_data/fcop-rules.mdc`.
- **`LETTER-TO-ADMIN.{zh,en}.md` — sub-agent warning.** The "one
  role, one agent" warning gains a sibling section, "a sub-agent is
  not an extra role", that tells ADMIN how to spot impersonation
  via subprocesses and points at `fcop_check()` for evidence.

### Added — `fcop`

- **`Project.audit_drift()` and `DriftReport` model.** New read-only
  API returning two independent audit streams: (1) working-tree
  drift detected by parsing `git status --porcelain -z` and
  removing every entry that lives under
  `docs/agents/{tasks,reports,issues,log}` — whatever remains is
  by definition work that bypassed the four-step cycle; (2)
  `session_id ↔ role` conflicts detected by walking every
  `TASK-*.md` / `REPORT-*.md` / `ISSUE-*.md` and grouping
  frontmatter `session_id` by role code. The result is a frozen
  `DriftReport(entries, session_role_conflicts, git_available)`,
  with new dataclasses `DriftEntry` and `SessionRoleConflict` in
  `fcop.models`. Detection-only by design — the protocol cannot
  prevent an agent from spawning a subprocess and writing
  arbitrary files; what FCoP guarantees is that the audit is
  loud. Source: `src/fcop/project.py`,
  `src/fcop/models.py`.

### Added — `fcop-mcp`

- **`fcop_check()` MCP tool.** New tool that wraps
  `Project.audit_drift()` and renders both audit streams in human-
  readable form. ADMIN now has a "is the ledger clean?" button.
  Source: `mcp/src/fcop_mcp/server.py`.
- **Per-MCP-process role lock for `write_*` tools.** `write_task`,
  `write_report`, and `write_issue` remember the first `sender`
  role observed in the current MCP process. If a later call uses a
  different role, the tool drops a Rule-1 evidence file under
  `.fcop/proposals/role-switch-*.md` and appends a warning to its
  return value. This is **soft enforcement** by design — the agent
  is not blocked, but the impersonation attempt is recorded
  alongside the body it would have written. Source:
  `mcp/src/fcop_mcp/server.py`.
- **`fcop_report()` shows audit summary.** When the session is
  UNBOUND, the report now folds in a one-screen
  `audit_drift()` summary so ADMIN sees pre-existing drift
  before assigning roles.

### Documentation

- **ADR-0002 — Lockstep pin rule.** The package-split ADR gains a
  formal section requiring `fcop-mcp X.Y.Z` to depend on
  `fcop>=X.Y,<X.(Y+1)` while pre-1.0, and a "发版前 lockstep 检查
  表" pre-release checklist. References `ISSUE-20260427-006`.
- **`docs/releases/RELEASE-CHECKLIST.md`** (new). Eight-phase release
  checklist born from the 0.7.0 incident. Every future release must
  walk through it.

## [0.7.0] - 2026-04-27

Tightens the protocol around **role-identity uniqueness** and fixes the
sequence-collision bug spotted live during 0.6.6 documentation work.
Carries forward all 0.6.6 documentation-only edits that never made it
to PyPI. See [`docs/releases/0.7.0.md`](./docs/releases/0.7.0.md) for
the full rationale, the "two ME" thought experiment that motivated the
protocol changes, and the dogfood incident reports
(`ISSUE-20260427-002` and `ISSUE-20260427-003`).

### Protocol — `fcop_protocol_version: 1.5.0` / `fcop_rules_version: 1.7.0`

- **Rule 1 — role-identity uniqueness (`fcop`).** Rule 1's
  "Invariants across both phases" section now explicitly forbids the
  same non-`ADMIN` / non-`SYSTEM` role code being bound to multiple
  agents simultaneously, declares the on-disk ledger
  (`docs/agents/{tasks,reports,issues,log}/`) as the **single
  authority** on occupancy, and binds ADMIN symmetrically — ADMIN
  must not assign the same role code to multiple agents either. The
  rule is the dual of the existing "ADMIN cannot be assigned to an
  agent" clause: the former protects the human seat, the latter
  protects every AI seat. Agents that detect a double-bind during
  the UNBOUND → BOUND transition must refuse under Rule 8 and
  surface three options (handoff / co-review / distinct role) to
  ADMIN; "temporarily filling in" is not a legal state.
  Source: `src/fcop/rules/_data/fcop-rules.mdc`.
- **UNBOUND step 4 — disk-based occupancy self-check (`fcop`).** The
  UNBOUND protocol in `fcop-protocol.mdc` adds a fourth step: before
  transitioning to BOUND, cross-check the assigned role against the
  new "Role occupancy" section of `fcop_report()` and reject the
  transition when another `session_id` is already driving the role.
  Source: `src/fcop/rules/_data/fcop-protocol.mdc`.
- **`LETTER-TO-ADMIN.{zh,en}.md` — ADMIN's symmetric duty.** The
  "Standard opening lines" section gains an explicit "one role, one
  agent" warning so ADMIN learns the constraint at the moment they
  type "you are PM". Includes the three escape options when the
  constraint is hit.

### Added — `fcop`

- **`Project.role_occupancy()` and `RoleOccupancy` model.** New
  read-only API returning per-role status (`UNUSED` / `ARCHIVED` /
  `ACTIVE`), open / archived counts across `tasks/`, `reports/`,
  `issues/`, `log/`, plus the most recent `session_id` and `mtime`.
  Computed from filename parses + frontmatter-only reads, so it is
  safe to call from an UNBOUND session (Rule 1 still forbids body
  reads). Roles in the on-disk ledger that are not declared in
  `fcop.json` are surfaced as "ghost" rows so ADMIN can spot stale
  team layouts.

### Added — `fcop-mcp`

- **`fcop_report()` "Role occupancy" section.** UNBOUND output now
  renders the new `Project.role_occupancy()` data as a fixed-width
  table (role / status / open & archived counts / `last_session_id`
  / `last_seen_at`). The output also gains a four-line guide on how
  to read the table and when to refuse a BOUND transition. Drives
  the agent-side enforcement of Rule 1's role uniqueness clause.

### Fixed — `fcop`

- **`write_task` / `write_report` / `write_issue` sequence collision
  after archive (`ISSUE-20260427-003`).** All three writers used to
  scan only their active directory (`tasks/` / `reports/` /
  `issues/`) when computing the next sequence number, ignoring
  `log/<type>/`. After `archive_task` moved a file out, the next
  same-day write reused the just-vacated sequence and produced a
  basename that collided with its archived ancestor in `git log` /
  cross-history grep. Fix: extracted shared helper
  `_existing_filenames_for_seq(*dirs)` that yields basenames across
  every passed directory; all three writers now union active and
  archive paths. Three regression tests added (one per writer) under
  the name `test_seq_skips_archived_basename`. Spotted live during
  the dogfood session that produced `TASK-20260427-002` and
  `REPORT-20260427-002`, both of which had to be hand-renamed.

### Removed — `fcop-mcp`

- **`unbound_report()` deprecated alias.** The 0.6.3 deprecation
  cycle promised removal in 0.7.0; `fcop_report()` is now the only
  way to produce the session report. Existing system prompts and
  documentation that still call `unbound_report` must switch.
  References to the alias in `fcop-protocol.mdc` were rewritten as
  history. **Surface-breaking change** under ADR-0003 — explicitly
  permitted at minor boundaries (0.6.x → 0.7.0).

### Documentation

- **Carries forward all 0.6.6 docs-only edits** that never shipped
  to PyPI: `docs/mcp-tools.md` resource count, `mcp/README.md` 0.6.5
  summary, `LETTER-TO-ADMIN.{zh,en}.md` 0.6.5 bullet, and the root
  README "Recent releases" table.

## [0.6.5] - 2026-04-27

Hot-fix release wiring the **Rule 0.a.1 hard constraint** into the
tool layer. 0.6.4 shipped the four-step `task → do → report → archive`
hard constraint as text in 17 role charters and `fcop-rules.mdc`, but
the first real-world solo test (`init_solo` → ADMIN: "做个俄罗斯方块"
→ agent dove straight into code) showed the constraint never **bit**
in practice: the agent could recite the rule perfectly but skipped
Step 1 (`write_task`) anyway, because nothing in the actual tool
return path reminded it at the moment of action. The agent's own
post-mortem nailed the diagnosis: *"是我没有把刚建立的协议作为当前
工作流的硬约束执行到底"* (= "I didn't execute the just-established
protocol as a hard constraint on the current workflow"). 0.6.5 plants
two soft tripwires — non-blocking, additive, ADR-0003 compatible — at
the two moments where agents actually pivot between chat and
artifacts. See [`docs/releases/0.6.5.md`](./docs/releases/0.6.5.md).

### Fixed — Rule 0.a.1 enforcement gap

- **`new_workspace` tripwire (`fcop-mcp`).** When an agent calls
  `new_workspace(slug=...)` and **no open `TASK-*.md` mentions that
  slug** in its `subject` / `body` / `references`, the tool now
  prepends a bilingual Rule 0.a.1 reminder to the response,
  recommending `write_task(...)` as Step 1 *before* dropping
  artifacts. Workspace creation still succeeds (the tripwire is a
  reminder, not a block) so legitimate offline / experimental flows
  are not broken. New helper `_recent_task_mentions_slug()` does the
  scan over `docs/agents/tasks/` (open status only, body+subject+
  references substring match, IO/parse errors swallowed).
- **`fcop_report` four-step template (`fcop-mcp`).** The initialized
  branch of `_compose_session_report()` (a.k.a. the UNBOUND report
  every bound agent re-reads when it self-checks state) now ends with
  an explicit four-step cycle template — `write_task` →
  `new_workspace` → `write_report` → `archive_task` — plus the
  "skipping Step 1 or Step 3 violates Rule 0.a.1" callout. Both `zh`
  and `en` reports get the template; bilingual phrasing matches the
  bilingual rules block in `fcop-rules.mdc` Rule 0.a.1.

### Tests

- `tests/test_fcop_mcp/test_server.py`:
  - `test_new_workspace_warns_when_no_open_task_mentions_slug` —
    fresh project, agent calls `new_workspace` with no matching task
    → response must contain `Rule 0.a.1`, `write_task`, and the
    "before editing any file" callout.
  - `test_new_workspace_silent_when_open_task_mentions_slug` —
    `write_task` first (subject/body mentions slug), then
    `new_workspace` → response must NOT contain the warning.
  - `test_fcop_report_initialized_includes_four_step_template_zh` /
    `_en` — both languages must list all four step verbs / tools and
    the "no `simple = skip`" callout.

### Compatibility / no breaking changes

- All edits are additive per ADR-0003: tool signatures unchanged,
  `tool_surface.json` snapshot unchanged, no new public API,
  `public_surface.json` snapshot unchanged. Existing callers see
  the same return-text *prefix* on the bound branches; only fresh
  scenarios with no matching task get extra prepended copy.

## [0.6.4] - 2026-04-26

Hot-fix release closing the **init-deposit gap** found while writing
the 0.6.3 customer tutorial: when ADMIN started fresh and asked an
agent to initialize an FCoP project, `init_*` was advertising files
(`LETTER-TO-ADMIN.md`, `workspace/`, `shared/` three-layer team
docs) that it never actually wrote. 0.6.4 makes every `init_*` land
its full promised set in a single transaction, ships a Solo template
bundle so single-AI projects no longer hit `TeamNotFoundError`, and
hardens the Phase-1 contract so agents stop defaulting to
`init_project(team="dev-team")` on ADMIN's behalf. All changes are
additive per ADR-0003. See
[`docs/releases/0.6.4.md`](./docs/releases/0.6.4.md).

### Fixed — initialization deposit gap (0.6.3 regression)

- **`init_solo` / `init_project` / `init_custom`** now deposit the
  full advertised set in one call: `docs/agents/fcop.json`,
  `docs/agents/LETTER-TO-ADMIN.md` (the ADMIN manual, picked from
  zh / en per the `lang` argument), `workspace/` cage with a starter
  `workspace/README.md`, the team's three-layer documentation under
  `docs/agents/shared/` (`TEAM-README.md` / `TEAM-ROLES.md` /
  `TEAM-OPERATING-RULES.md` / `roles/{ROLE}.md`, both zh and en),
  and the four host-neutral protocol-rule files
  (`.cursor/rules/*.mdc` + `AGENTS.md` + `CLAUDE.md`). 0.6.3 silently
  skipped the letter, the workspace cage, and the role charters.
- New `tests/test_fcop/test_init_promises.py` pins the deposit
  contract for all three init paths so this can never regress
  silently again.

### Added — fcop (library)

- **`teams/_data/solo/`** — first-class Solo team template bundle
  with the full three-layer documentation (`README.md` /
  `TEAM-ROLES.md` / `TEAM-OPERATING-RULES.md` + `roles/ME.md`), in
  zh and en. The `ME.md` charter contains a "workflow hard
  constraint" section that explicitly forbids the
  "simple-tasks-may-run-directly" soft-constraint pattern (the
  exact 0.6.3 mis-design that let agents bypass `task → do →
  report → archive`).
- **`Project.init` / `init_solo` / `init_custom` ↪ `deploy_role_templates=`**
  parameter (defaults: `True` for preset / solo, `False` for custom
  since custom teams have no bundled templates). Auto-deploys the
  three-layer docs at init time. Solo init no longer raises
  `TeamNotFoundError("solo")` on the role-template step.
- **`Project.init(team="solo")` is now rejected with `ValueError`**
  before any disk write, pointing callers at `init_solo()` so the
  saved config carries `mode="solo"` (not `mode="preset",
  team="solo"`).
- **`fcop.rules.get_install_prompt(lang)`** — returns the canonical
  "have an agent install fcop-mcp for you" prompt (the same text
  shipped to GitHub README / PyPI README / MCP resource
  `fcop://prompt/install`). 0.6.4 surfaces this prompt in three
  places at once so customers can always copy it from whichever
  one they happen to be reading.

### Added — fcop-mcp (MCP server)

- **`fcop://prompt/install`** + **`fcop://prompt/install/en`** —
  two new MCP resources exposing the agent-install prompt
  (zh / en). Total resource count: **10 → 12**.
- **`init_solo` / `init_project` / `create_custom_team`** all
  expose a new **`force: bool`** parameter (default `False`).
  When `True`, an already-initialized project is overwritten and
  the previous `fcop.json` / letter / workspace README / `shared/`
  files / protocol-rule quartet are archived under
  `.fcop/migrations/<timestamp>/`. This is the supported way for
  ADMIN to switch teams (e.g. solo → dev-team) without manually
  wiping the project.
- **`fcop_report` Phase-1 output** now (a) tells the agent
  explicitly that it MUST NOT pick an init mode on ADMIN's behalf,
  and (b) points ADMIN at `fcop://letter/zh|en` for the manual if
  the three-way choice (solo / preset / custom) is unfamiliar.

### Changed — protocol rules

- **`fcop-rules.mdc` 1.5.0 → 1.6.0**:
  - **Rule 0.a.1** new sub-section: workflow hard constraint.
    Every piece of work, no matter how trivial, must follow
    `task → do → report → archive`. Role documents are forbidden
    from softening this with "simple tasks may run directly" or
    equivalents — that pattern is itself a Rule 0.a violation.
  - **Rule 1 Phase 1** rewritten to (a) list the full set of
    files an `init_*` tool promises to deposit (so a partial
    deposit becomes a recognisable bug), and (b) explicitly
    forbid agents from defaulting to `dev-team` / `solo` /
    `custom` on ADMIN's behalf.

### Fixed — letter & install-prompt visibility

- **`init_project` / `init_solo` / `create_custom_team`** now splice
  the LETTER-TO-ADMIN intro slice (title + 0.6.4 summary block +
  ADMIN/AI-team identity diagram) into the post-init reply, with an
  explicit "paste this verbatim to ADMIN" instruction for the agent.
  0.6.3 deposited the letter to disk but never surfaced it in chat,
  so the manual was effectively invisible — customers in the
  tutorial all skipped opening `docs/agents/LETTER-TO-ADMIN.md`.
  The full letter remains available on disk and via the
  `fcop://letter/zh|en` MCP resource; the splice is just the
  intro so it doesn't drown the chat.
- **`fcop.rules.get_letter_intro(lang)`** new public accessor
  (used by the MCP layer above). Returns the verbatim prefix of
  the letter through the second `---` rule. Pinned by 7 new tests
  asserting it stays a strict prefix of `get_letter(lang)` and
  always carries the H1 + the "0.6.4 摘要" / "0.6.4 in one block"
  block.
- **`tests/test_fcop/test_install_prompt.py`** (11 new tests)
  pins the four-surface contract for the canonical install
  prompt: the bundled markdown file, `get_install_prompt(lang)`,
  the `fcop://prompt/install` MCP resource, and the verbatim
  embed inside `mcp/README.md` (PyPI-visible) all stay byte-for-
  byte aligned. Also asserts the non-negotiable safety clauses
  (preserve existing `mcpServers`, 30s–1min first-launch
  cooldown, do-not-auto-init) survive future copy edits in both
  languages.

### Fixed — role-template soft-constraint regression

- **All 17 bundled role charters** (`solo/ME`, `dev-team/PM` /
  `DEV` / `QA` / `OPS`, `media-team/PUBLISHER` / `COLLECTOR` /
  `WRITER` / `EDITOR`, `mvp-team/MARKETER` / `RESEARCHER` /
  `DESIGNER` / `BUILDER`, `qa-team/LEAD-QA` / `TESTER` /
  `AUTO-TESTER` / `PERF-TESTER`, both zh and en — 34 files total)
  now open with a "workflow hard constraint" section that
  translates Rule 0.a.1 onto the role side: every incoming piece
  of work, no matter how trivial, must follow the four-step
  cycle `task → do → report → archive`, with only a narrow
  ADMIN-explicit exception clause that itself requires a
  `drop_suggestion` trace. 0.6.3 charters scattered the
  workflow rules across "Responsibilities" / "Common mistakes"
  prose, which agents in the field softened to "simple tasks may
  run directly" — the exact pattern that let `ME` skip
  `task` / `report` and dump artefacts directly to the project
  root during the snake-game tutorial debug.
- New `tests/test_fcop/test_role_templates.py` (36 tests) pins
  the anchor across every bundled `roles/*.md` so a future
  contributor copy-pasting a role without the constraint will
  fail CI rather than silently regress.

### Documentation

- **`src/fcop/rules/_data/agent-install-prompt.zh.md`** +
  **`.en.md`** — the canonical install prompt, also packaged into
  the wheel and surfaced via the new MCP resource. Same text used
  in `mcp/README.md` and root `README.md` / `README.zh.md`.
- **`mcp/README.md`** opens with a "TL;DR — Have an agent install
  fcop-mcp for you" section visible on GitHub *and* PyPI.
- **Root `README.md` / `README.zh.md`** point at the install
  prompt + the new `fcop://prompt/install` resource so customers
  who land on either landing page can hand the prompt to an agent
  without reading the rest of the page.
- **`docs/agents/LETTER-TO-ADMIN.md`** (zh + en) gets a 0.6.4
  summary block at the top, the corrected tool / resource counts
  (26 / 12), the new `fcop://prompt/install` resource entry, and
  an explicit "agent must not default" warning on the three-way
  init choice.
- **`src/fcop/teams/_data/README.md`** + **`.en.md`** add the new
  `solo` team to the directory listing and the modes table, and
  pick up a "Custom teams" section pointing custom builds at the
  closest preset for inspiration.

## [0.6.3] - 2026-04-26

Lockstep release with two thrusts: (1) ratify **ADR-0006**, the
host-neutral protocol-rule distribution & upgrade contract, so
`fcop-mcp` finally writes the protocol rules to disk in a form every
MCP host can read (Cursor `.mdc`, plus `AGENTS.md` / `CLAUDE.md`); and
(2) rename `unbound_report` → `fcop_report` because the tool is the
canonical project-status report, not just the unbound-session
warning. All changes are additive per ADR-0003 (Pre-1.0 Stability
Charter); every removed-in-0.7.0 alias is shipped through one full
deprecation cycle. See [`docs/releases/0.6.3.md`](./docs/releases/0.6.3.md).

### Added — governance

- **ADR-0006 Host-Neutral Rule Distribution & Upgrade** ratified
  ([`adr/ADR-0006`](./adr/ADR-0006-host-neutral-rule-distribution.md)).
  Codifies that the protocol rule files (`fcop-rules.mdc`,
  `fcop-protocol.mdc`) must reach every supported host (Cursor,
  Claude Desktop, Claude Code CLI, Codex CLI, raw API scripts) and
  that there must be an explicit, ADMIN-controlled upgrade path when
  the wheel-bundled rules drift past the project-local copy.

### Added — fcop (library)

- **`fcop.rules.get_protocol_version()`** — returns the SemVer of the
  shipped commentary (`fcop-protocol.mdc`), symmetric to the existing
  `get_rules_version()`. The two documents version independently so a
  wording-only edit to the commentary doesn't force a rules bump and
  vice versa. Used by `Project.deploy_protocol_rules` and the MCP
  layer's `fcop_report` / `redeploy_rules` to detect drift.
- **`Project.deploy_protocol_rules(force=True, archive=True)`** — host-
  neutral redeploy of the four protocol-rule targets to the project
  root: `.cursor/rules/fcop-rules.mdc` + `.cursor/rules/fcop-protocol.mdc`
  (Cursor), plus YAML-frontmatter-stripped `AGENTS.md` (Codex CLI) and
  `CLAUDE.md` (Claude Code CLI). Stale targets are archived under
  `.fcop/migrations/<ts>/rules/` before being overwritten. Returns a
  `DeploymentReport` listing every file touched.
- **`Project.init(deploy_rules=True)`** — `deploy_rules` now wires
  through `deploy_protocol_rules` so a fresh project ships with the
  four rule targets already on disk. Existing call sites that don't
  pass the flag are unchanged.

### Added — fcop-mcp (MCP server)

- **`fcop_report(lang)`** — new canonical session-status / init report
  tool. Same body shape as the legacy `unbound_report` plus a
  `[Versions]` / `[版本]` block surfacing `fcop-mcp`, `fcop`, and
  the local-vs-bundled rules / protocol versions, with an `OUTDATED`
  / `本地偏旧` marker + `redeploy_rules` prompt when drift is
  detected. Replaces `unbound_report` for all new system prompts.
- **`redeploy_rules(force=True, archive=True, lang)`** — ADMIN-only
  thin wrapper over `Project.deploy_protocol_rules`. Agents must not
  invoke directly (the docstring says so), but the MCP surface stays
  symmetric with `deploy_role_templates` so ADMIN can call it from
  the chat box. The 24-tool count is now **26** with these two
  additions; the snapshot
  (`tests/test_fcop_mcp/snapshots/tool_surface.json`) is updated
  accordingly per ADR-0003 commitment #2.

### Deprecated — fcop-mcp

- **`unbound_report`** is now a thin alias of `fcop_report` and emits
  `DeprecationWarning("unbound_report is deprecated; use fcop_report
  instead. This alias will be removed in fcop-mcp 0.7.0. See ADR-0006
  for the rationale.")` on every call. The tool stays in the public
  surface for one full minor (per ADR-0003 deprecation cycle); 0.7.0
  removes the name. Migration is purely lexical: replace every
  `unbound_report` in your system prompts with `fcop_report`.

### Tests

- **15 new tests** for `fcop`: `tests/test_fcop/test_rules.py` adds
  `TestGetProtocolVersion`; new file
  `tests/test_fcop/test_project_deploy_protocol.py` covers the four
  deployment targets, byte-exactness of `.mdc`, frontmatter stripping
  for `AGENTS.md` / `CLAUDE.md`, idempotency, archival, and the
  `Project.init(deploy_rules=True)` integration path. Public-surface
  snapshot regenerated for the additive `Project.deploy_protocol_rules`
  + `fcop.rules.get_protocol_version` exports.
- **9 new tests** for `fcop-mcp`:
  `tests/test_fcop_mcp/test_server.py::TestSessionReportAndRedeploy`
  covers `fcop_report` (uninitialized / initialized / `[Versions]`
  block / English variant / drift warning), the `unbound_report`
  alias (still works + `DeprecationWarning` is emitted), and
  `redeploy_rules` (writes four targets + archives stale files).
  Tool-surface snapshot regenerated for the additive
  `fcop_report` / `redeploy_rules` registrations.

### CI

- **`.github/workflows/release.yml`**: `verify` 步骤改为只从
  `^__version__ =` 行解析版本；不再用「文件中首段双引号内文字」，避免
  匹配到 `src/fcop/_version.py` 里 **`"semver 承诺"`** 导致 tag 发版
  在 verify 即失败。行为与发版后用户升级无直接关系。

## [0.6.2] - 2026-04-25

### Documentation (PyPI + repo)

- **Project metadata** (`pyproject.toml`): one-line `description` and
  `project.urls` for both packages. **`fcop`**: long description is
  [`fcop-README.pypi.md`](./fcop-README.pypi.md) (pure library; fixes wrong
  historical “MCP toolbox” text on PyPI). **`fcop-mcp`**: `description` / links;
  install story in [`mcp/README.md`](./mcp/README.md).
  No library or server code change; **ADR-0003** tool/resource surface unchanged.
- **`fcop-mcp`**: customer-facing install guide in [`mcp/README.md`](./mcp/README.md) — one **recommended** path (dedicated venv + `python -m fcop_mcp`), **alternatives** (`uvx fcop-mcp` with cold-start note), **Windows / macOS** `mcp.json` examples, **verify** commands (`from fcop import Issue, Project` / `fcop_mcp.server`), and a short warning when the wrong `fcop` distribution is on `PYTHONPATH`.
- **Root `README` / `README.zh`**: pointer to the full install doc for IDE users; behaviour of the two packages is unchanged.
- **Lockstep**: `fcop` **0.6.2** and **`fcop-mcp` 0.6.2** together — **no** public library API or compat-CLI code change in `fcop` vs 0.6.1; version bump aligns both wheels and refreshes long-form docs on PyPI (cannot replace 0.6.1 files in place).

See [`docs/releases/0.6.2.md`](./docs/releases/0.6.2.md).

## [0.6.1] - 2026-04-23

### Added

- **`fcop` compat CLI shim** — the `fcop` wheel now ships a `fcop`
  console script that prints a friendly migration message and exits
  with status `1`. This closes the `0.5.x → 0.6.x` gap where users who
  ran `uvx fcop` or `pip install fcop && fcop` would have gotten a bare
  "command not found" after upgrading. Pure additive per ADR-0003 (no
  library API change). See [`docs/releases/0.6.0.md`](./docs/releases/0.6.0.md)
  §5.3 for background.

## [0.6.0] - 2026-04-23

### Added — project governance

- **ADR-0003 Pre-1.0 Stability Charter** ratified
  ([`adr/ADR-0003`](./adr/ADR-0003-stability-charter.md)). Starting with
  `0.6.0`, the four public-API surfaces (`fcop.__all__`, `Project`
  methods/properties, `fcop.models` dataclass fields,
  `fcop.teams` / `fcop.rules` exports) are **additive-only** within a
  minor version; breaking changes require a deprecation cycle spanning
  at least one minor version.
- New snapshot test
  `tests/test_fcop/test_public_surface.py` freezes the observed surface
  to `tests/test_fcop/snapshots/public_surface.json`. Update the
  snapshot with `pytest --snapshot-update` when adding public API and
  announce it in this CHANGELOG.
- New CI job `surface-check` verifies that any PR modifying the snapshot
  file also updates the `[Unreleased]` section of this CHANGELOG.
- **`fcop-mcp` tool contract frozen** (ADR-0003 commitment #2). New
  snapshot test `tests/test_fcop_mcp/test_tool_surface.py` captures
  every tool name, parameter name + JSON type + required-ness, and
  every `fcop://` resource URI into
  `tests/test_fcop_mcp/snapshots/tool_surface.json`. Regenerate with
  `pytest tests/test_fcop_mcp --snapshot-update` when adding public
  MCP surface (always additive within 0.6.x).
- New smoke suite `tests/test_fcop_mcp/test_server.py` (39 tests)
  exercises every registered tool and resource end-to-end via
  `mcp.call_tool` / `mcp.read_resource`, so a broken MCP handler
  fails CI instead of surfacing only in a user's editor.
- New GitHub Actions workflow `test-fcop-mcp.yml` — 3-OS × 4-Python
  matrix, ruff + mypy (strict) + pytest for the MCP contract and
  smoke suite, a PR-only `tool-surface` gate mirroring the library's
  `surface-check` job, and a clean-venv smoke install of the built
  wheel so the `fcop-mcp` console script packaging is verified
  every commit.
- **ADR-0004 Time Is Filesystem's Job** ratified
  ([`adr/ADR-0004`](./adr/ADR-0004-time-is-filesystem.md)). Single
  source of truth for time: task / report files **do not** carry
  `created_at` in frontmatter (Git history + filesystem `mtime` are
  authoritative). Issue files **do** carry `created_at` because
  Issue is the one FCoP file kind that allows legal editing
  (`open → closed` monotonic append), so `mtime` is no longer
  equivalent to creation time.
- **ADR-0005 Agent Output Layering** ratified
  ([`adr/ADR-0005`](./adr/ADR-0005-agent-output-layering.md)).
  Every agent-produced artifact now falls into exactly one of five
  lifecycle tiers: (A) tool return values — no file, (B) audit /
  patrol traces → `docs/agents/log/`, (C) cross-agent findings →
  `docs/agents/issues/` via `write_issue`, (D) agent-private runtime
  state (`runtime-*.json`, cache, checkpoint) → **new**
  `docs/agents/.runtime/{AGENT_CODE}/`, (E) local one-shot human
  scripts → `_ignore/`. 0.6.0 is a protocol-level decision only; the
  library helpers (`Project.agent_runtime_dir`, `write_log`,
  `list_logs`) ship in 0.6.1 as additive API per ADR-0003.

### Changed — fcop (library)

- **BREAKING**: `fcop` is now a pure Python library, not an MCP server.
  Users who were running `uvx fcop` or `pip install fcop` expecting an
  MCP server should install `fcop-mcp` instead.
- New `Project` facade as the main entry point; see
  [adr/ADR-0001](./adr/ADR-0001-library-api.md) for the full API contract.
- Structured data returns: methods now return frozen dataclasses
  (`Task`, `Report`, `Issue`, `TeamConfig`, `ProjectStatus`, ...) instead
  of pre-formatted strings.
- Typed exception hierarchy: every failure mode has a dedicated subclass
  of `FcopError`.
- Runtime dependency reduced to just `pyyaml` (YAML is part of the
  FCoP file format). MCP and websocket deps moved entirely to `fcop-mcp`.
- Single source of truth for the version string at `src/fcop/_version.py`
  (read by `pyproject.toml` via hatchling's dynamic version).
- **Preset rosters realigned** with the authoritative `_data/teams/index.json`
  (ported from `codeflow-plugin 0.5.x`):
  - `mvp-team`: now `MARKETER` (leader) / `RESEARCHER` / `DESIGNER` /
    `BUILDER`. Was `PM` / `BUILDER` / `SELLER` in a pre-0.6 snapshot of
    `fcop.teams`.
  - `media-team`: adds `EDITOR` as the fourth role.
  - `dev-team` and `qa-team` unchanged.
  `Project.init(team=...)` will generate the new rosters from 0.6.0
  onward.
- `fcop.rules` now returns real content (the protocol rule docs and
  the Letter-to-ADMIN user manual). Previously raised
  `NotImplementedError`. `get_rules_version()` parses the bundled
  rules document's frontmatter — today `"1.4.0"`.
- `fcop.teams.get_template()` implemented. Returns a `TeamTemplate`
  dataclass with `readme` + `team_roles` + `operating_rules` + a
  per-role `roles` dict, all as UTF-8 text. Previously raised
  `NotImplementedError`.
- `Project.write_issue` now emits two additional canonical
  frontmatter fields: `status: open` and `created_at` (ISO 8601,
  second precision). Existing issue files missing these fields are
  still readable — the new fields are additive, see ADR-0004
  Grandfather clause.
- Issue file canonical frontmatter order is now
  `protocol, version, reporter, severity, status, summary,
  created_at [, closed_at, closed_by, resolution]` with unknown
  keys sorted alphabetically below; `closed_*` / `resolution` slots
  are reserved for the 0.6.1 issue state-machine follow-up.

### Added — fcop-mcp (MCP server)

- New package. Thin wrapper exposing `fcop.Project` / `fcop.teams` /
  `fcop.rules` as MCP tools and resources for Cursor / Claude Desktop.
- Depends on `fcop >= 0.6, < 0.7` and `fastmcp >= 3.2`.
- **24 MCP tools** registered, mirroring the 0.5.4 surface so existing
  clients keep working after the rename (`fcop` → `fcop-mcp`). Groups:
  project path (`set_project_dir`), init (`init_project`, `init_solo`,
  `create_custom_team`, `validate_team_config`),
  tasks (`write_task` / `read_task` / `list_tasks` / `inspect_task` /
  `archive_task`), reports (`write_report` / `list_reports` /
  `read_report`), issues (`write_issue` / `list_issues`),
  team & workspace (`get_available_teams`, `get_team_status`,
  `deploy_role_templates`, `new_workspace`, `list_workspaces`),
  suggestions (`drop_suggestion`), and meta (`unbound_report`,
  `check_update`, `upgrade_fcop`).
- **10 MCP resources** under the `fcop://` URI scheme: `status`,
  `config`, `rules`, `protocol`, `letter/{zh,en}`, `teams`,
  `teams/{team}`, `teams/{team}/{role}`, `teams/{team}/{role}/en`.
  All returns route through the `fcop` library, so the contract
  remains single-sourced.

### Removed — fcop (library)

- `fcop.server` module (moved to `fcop-mcp`).
- `fcop` console script (the CLI returns in a later release as a
  separate ADR).
- Global module state (`PROJECT_DIR`, `TASKS_DIR`, ...); all state now
  flows through `Project` instances.

### Migration

If you were using `fcop 0.5.x`:

- MCP server users → `pip install fcop-mcp` and update your MCP client
  config to call `fcop-mcp` instead of `fcop`.
- Python library users → upgrade to `fcop 0.6.0` and switch from
  `from fcop.server import ...` (unofficial) to the new public API
  `from fcop import Project`.

See [`docs/MIGRATION-0.6.md`](./docs/MIGRATION-0.6.md) for the step-by-step
guide (coming before the 0.6.0 final release).

---

## Pre-history (before joinwell52-AI/FCoP existed)

Prior to 0.6.0, the package was developed inside the
[`joinwell52-AI/codeflow-pwa`](https://github.com/joinwell52-AI/codeflow-pwa)
monorepo under the `codeflow-plugin/` subdirectory. That history is
preserved in place and is not ported into this repository.

The last `fcop 0.5.x` release
([`fcop 0.5.4`](https://pypi.org/project/fcop/0.5.4/)) was built from
commit
[`e651139`](https://github.com/joinwell52-AI/codeflow-pwa/commit/e651139).
Anything older should be read from that repository's `git log`.
