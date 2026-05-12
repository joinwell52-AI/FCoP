# FCoP MCP 工具与资源清单（fcop-mcp 1.x）<!-- 35 tools, 14 resources — v1.3.0 -->

> 本页是 [`fcop-mcp`](https://pypi.org/project/fcop-mcp/) 暴露给 Cursor / Claude Desktop 等 MCP 客户端的**工具与资源**索引。**权威说明**仍在源码 docstring（[`mcp/src/fcop_mcp/server.py`](https://github.com/joinwell52-AI/FCoP/blob/main/mcp/src/fcop_mcp/server.py)）；本页是**导航与速查**，按类别分组、给出何时调用、参数要点。
>
> 稳定承诺：**整个 `1.x` 周期工具与资源「只增不改」**（[ADR-0003](../adr/ADR-0003-stability-charter.md)）。新增工具/参数允许；改名、删除、改语义不允许。

---

## 总览

- **工具（tools）35 个**（v1.1 新增 4 个 Review 工具；v1.2.1 新增 2 个治理审计工具；v1.3.0 新增 3 个：2 个 GAL 告警工具 + 1 个协议体检工具）：调用方主动触发，写盘或返回报告。
- **资源（resources）14 个**（11 个静态 URI + `fcop://teams/{team}` / `.../{role}` / `.../{role}/en` 三套模板）：只读 URI，常用于把规则/状态/职责模板以引用方式塞进上下文。

> **v1.1.0 新增**：4 个 Review 工具（`write_review` / `list_reviews` / `read_review` / `mark_human_approved`）；`write_task` 新增 `risk_level` 参数；`fcop://spec` / `fcop://spec/en` 升级到 v1.1 spec。

> 看名字与参数清单（机器可读、CI 校验）：[`tests/test_fcop_mcp/snapshots/tool_surface.json`](../tests/test_fcop_mcp/snapshots/tool_surface.json)。  
> 看「为什么这么设计」：[`adr/ADR-0001`](../adr/ADR-0001-library-api.md)、[`adr/ADR-0003`](../adr/ADR-0003-stability-charter.md)。

---

## 1. 起手式（每次新会话先调）

| 工具 | 何时调 | 关键参数 |
|---|---|---|
| `fcop_report` | **每个新 MCP 会话的第一个调用**（FCoP Rule 0）。返回项目状态；**未初始化**时给出三选一初始化建议；**已初始化但本会话未认领角色**时输出 UNBOUND 报告，等 ADMIN 用「你是 \<ROLE\>」赋角色。报告头部含 `[版本] / [Versions]` 段，自动比对本地 `.cursor/rules/` 与 wheel 内捆绑版本，漂移时提示 ADMIN 调 `redeploy_rules`。 | `lang`（`zh` / `en`） |
| `set_project_dir` | MCP 把项目根定位错了。**不改 `mcp.json`、不重启 Cursor** 就能切到正确目录。 | `path`（绝对路径，目录须存在） |
| `fcop_check` | 项目自检：schema 合规、文件名一致性、frontmatter 完整性。不写盘。 | `lang` |

---

## 2. 项目初始化（三选一）

| 工具 | 用途 | 关键参数 |
|---|---|---|
| `init_project` | 用**预设团队**模板初始化：`dev-team` / `media-team` / `mvp-team` / `qa-team`。建立 `fcop/` 五目录、写 `fcop.json`、把规则注入 `.cursor/rules/`、部署三层文档。**幂等**。 | `team`（默认 `dev-team`）、`lang` |
| `init_solo` | **Solo 模式**：单 AI 角色直接对 ADMIN，不做派发。 | `role_code`（默认 `ME`）、`role_label`、`lang` |
| `create_custom_team` | **自定义角色**初始化。**强烈建议先 `validate_team_config` 干跑**。 | `team_name`、`roles`（逗号分隔）、`leader`、`lang` |
| `validate_team_config` | **不写盘**地校验自定义团队配置。 | `roles`、`leader` |
| `get_available_teams` | 列出仓库内置团队及其 leader / 成员。 | `lang` |

---

## 3. 任务流（tasks/）

任务文件在 `fcop/tasks/`，命名 `TASK-YYYYMMDD-NNN-{SENDER}-to-{RECIPIENT}.md`。

| 工具 | 用途 | 关键参数 |
|---|---|---|
| `write_task` | 派一张任务单。库自动生成文件名与符合 FCoP v1.1 的 frontmatter。 | `sender`、`recipient`（支持 `ROLE.D1` 槽位 / `TEAM` 广播）、`subject`、`body`、`priority`（`P0`–`P3`）、`thread_key`、`references`、**`risk_level`**（v1.1：`low`/`medium`/`high`/`irreversible`） |
| `read_task` | 读任务全文（含归档）。 | `filename`（文件名或纯 `TASK-…-NNN`） |
| `list_tasks` | 按发件人 / 收件人 / 状态 / 日期过滤；带分页。 | `sender`、`recipient`、`status`、`date`、`limit`、`offset` |
| `inspect_task` | **离线校验** schema 与「文件名↔frontmatter」一致性。 | `filename` |
| `archive_task` | 把已完成任务（含同名报告）一起搬到 `fcop/log/`。 | `task_id` |

> **v1.1 `risk_level`**：`high` / `irreversible` 会在报告里提示需要 `write_review(decision="needs_human")`，关键操作审批链才闭合。

---

## 4. 报告流（reports/）

| 工具 | 用途 | 关键参数 |
|---|---|---|
| `write_report` | 写完成报告，回到指定收件人（通常是 leader/PM）。 | `task_id`、`reporter`、`recipient`、`body`、`status`（`done` / `in_progress` / `blocked`）、`priority` |
| `list_reports` | 过滤列出。 | `reporter`、`task_id`、`status`、`limit`、`offset` |
| `read_report` | 读报告全文。 | `filename`（或对应 `task_id`） |

---

## 5. 问题流（issues/）

| 工具 | 用途 | 关键参数 |
|---|---|---|
| `write_issue` | 上报问题：阻塞、规则不清、外部故障等。 | `reporter`、`summary`、`body`、`severity`（`critical`/`high`/`medium`/`low`，亦支持 `P0`–`P3`） |
| `list_issues` | 过滤列出。 | `reporter`、`severity`、`limit`、`offset` |

---

## 6. 审核流（reviews/）— v1.1 新增

REVIEW 文件是治理层对某个制品的决策记录（[ADR-0017](../adr/ADR-0017-review-file-type-minimal.md)）。文件在 `fcop/reviews/`，命名 `REVIEW-YYYYMMDD-NNN-{REVIEWER}-on-{slug}.md`。

| 工具 | 用途 | 关键参数 |
|---|---|---|
| `write_review` | 写一份 REVIEW（治理层决策，per ADR-0017/0025）。 | `reviewer_role`、`subject_type`（`task`/`report`/`role_switch`/`code_change`）、`subject_ref`（被审对象路径）、`decision`（见下表）、`rationale`、`required_changes`（`needs_changes` 时必填）、`reviewer_agent`、`body`、`subject_short` |
| `list_reviews` | 过滤列出 REVIEW，标注 `[human_approval pending]` / `[human_approved]`。 | `reviewer_role`、`decision`、`subject_type`、`status`（`open`/`archived`/`all`）、`limit`、`offset` |
| `read_review` | 读 REVIEW 全文，含 `human_approval` 子结构展示。 | `filename`（文件名或 Review ID） |
| `mark_human_approved` | **关闭 `needs_human` 升级回路**（per ADR-0026）。把 `human_approval` 事件写入已有 REVIEW frontmatter。approver **必须**是 `layer: admin` 的角色（如 `ADMIN`）。 | `review_id`（REVIEW 文件名 stem）、`approver`、`decision`（`approve`/`reject`）、`channel`（`cli`/`mobile`/`web`/`manual_file_edit`）、`comment` |

**`decision` 枚举（v1.1 共 5 值）：**

| 值 | 含义 |
|---|---|
| `approved` | 制品通过，可以继续 |
| `rejected` | 制品被否决，不得继续 |
| `needs_changes` | 需要修改（必须配 `required_changes`） |
| `abstained` | 审核者回避 |
| `needs_human` | *(v1.1 ADR-0025)* agent 主动上升人工——REVIEW 停留 pending，ADMIN 需调 `mark_human_approved` 闭合 |

---

## 7. 团队 / 共享文档 / 工作区

| 工具 | 用途 | 关键参数 |
|---|---|---|
| `get_team_status` | 项目状态快照：初始化状态、团队/leader、open task/report/issue/review 数、最近活动。 | `lang` |
| `deploy_role_templates` | 部署 / 刷新 `fcop/shared/` 里的团队文档与角色档案。`force=True` 时先归档再覆盖。 | `team`、`lang`、`force`（默认 `True`） |
| `new_workspace` | 在 `workspace/<slug>/` 下建工作目录，**不要把代码写到项目根**。幂等。 | `slug`（`^[a-z][a-z0-9-]*$`、≤ 40）、`title`、`description` |
| `list_workspaces` | 列出现有 `workspace/<slug>/`。 | `lang` |

---

## 8. 协议泄压阀

| 工具 | 用途 | 关键参数 |
|---|---|---|
| `drop_suggestion` | **唯一**让 agent 对协议提反对意见的合法通道：写一份带时间戳的 markdown 到 `.fcop/proposals/`。**禁止**自己改 `fcop-rules.mdc`。 | `content`、`context` |

---

## 9. 维护（自检与升级）

| 工具 | 用途 | 关键参数 |
|---|---|---|
| `check_update` | 比对本地 `fcop-mcp` 与 PyPI 最新版（不写盘、不安装）。 | `lang` |
| `upgrade_fcop` | 打印**针对你的安装方式**的升级命令。**不**自动跑 pip。 | `lang` |
| `redeploy_rules` | **ADMIN-only**。把 wheel 里四份规则文件写到项目根；`force=True` 覆写，`archive=True` 先归档旧文件。何时调：`fcop_report` 显示版本漂移。背景：[ADR-0006](../adr/ADR-0006-host-neutral-rule-distribution.md)。 | `force`（默认 `True`）、`archive`（默认 `True`）、`lang` |

> 详细升级流程：[`docs/upgrade-fcop-mcp.md`](./upgrade-fcop-mcp.md)。

---

## 10. 治理事件审计（v1.2.1 新增）

> 基于 ADR-0030-bis Layer 1 MCP Middleware 的行为账本。每个工具调用都会被自动打上 `risk` 标签并写入 `fcop_events.jsonl`。

| 工具 | 用途 | 关键参数 |
|---|---|---|
| `list_governance_events` | 读取 `fcop_events.jsonl`，列出最近 N 条治理事件。每条包含：tool、risk（Safe / Sensitive / Critical）、tag（ALLOW / REVIEW_TAG / CRITICAL_TAG）、args_hash、session_id、时间戳。 | `last_n`（默认 50）、`risk`（过滤，空=全部）、`tag`（过滤） |
| `get_governance_summary` | 汇总统计：总调用量 / 各风险层分布 / Top 10 工具 / CRITICAL_TAG 事件清单。快速健康检查：CRITICAL_TAG 无对应 Task + Review 即为治理缺口。 | 无 |

> `fcop_check()` 已整合 Layer 3 审计：输出末段自动附上治理事件日志摘要，含 CRITICAL_TAG 操作清单。

---

## 11. 治理告警（GAL — ADR-0031，v1.3.0 新增）

> 基于 ADR-0031 Governance Alert Layer。`fcop_check()` 自动扫描治理漂移信号，命中则写入 `fcop/alerts/ALERT-*.md`。ADMIN 无需巡检，系统把异常送到 ADMIN 面前。

| 工具 | 用途 | 关键参数 |
|---|---|---|
| `fcop_list_alerts` | 读取 `fcop/alerts/` 下所有 ALERT 文件，输出 ADMIN 告警收件箱。支持按 `status` / `severity` 过滤。 | `status`（`open` / `acknowledged` / `resolved`，空=全部）、`severity`（`high` / `medium` / `low`）、`last_n`（默认 20） |
| `fcop_create_alert` | ADMIN / 治理观察者手动归档治理缺口，写入新 ALERT-*.md 文件。 | `severity`、`alert_type`、`summary`、`suggestion` |

**告警类型（`alert_type`）**：

| 类型 | 触发条件 | 严重度 |
|---|---|---|
| `critical_tool_unreviewed` | 24h 内有 CRITICAL_TAG 工具调用，但无对应 Review 文件 | high |
| `missing_independent_verdict` | 执行窗口 > 6h 无任何治理事件（Solo Blindspot，FCoP-Rule-G1） | high |
| `long_running_without_reconciliation` | open Task 超 24h 未归档 | low |

**FCoP-Rule-G1**：`write_report` / `fcop_report` ∈ 执行域，不构成治理信号，不能重置 Solo Blindspot 窗口。只有 `write_review` / `mark_human_approved` / `fcop_check` 才算独立治理视角。

**ADMIN 工作流**：
1. 运行 `fcop_check()` → 自动触发漂移扫描 → 输出新 ALERT 列表
2. 运行 `fcop_list_alerts(status="open")` → 查看待处理告警
3. 处理后直接编辑 ALERT-*.md 中的 `status` 字段（`open` → `acknowledged` → `resolved`）

---

## 12. 协议体检（fcop_audit）

> 一次性深度体检；`fcop_check` 是日常轻量自检，二者互补。

| 工具 | 用途 | 关键参数 |
|---|---|---|
| `fcop_audit` | 三场景协议体检，发现 6 类合规盲区，产出 INSPECTION 报告（含 Execution Block 整改建议） | `scope`（`new`/`upgrade`/`takeover`/`auto`，默认 `auto`）、`output`（`file`/`stdout`/`both`）、`project_path` |

**三场景**：

| 场景 | 触发条件 | 扫描内容 |
|---|---|---|
| `new` | 新项目验收 | 协议文件是否完整部署 |
| `upgrade` | 版本升级后验收 | 规则/文档版本是否同步 |
| `takeover` | 老 non-fcop 项目首次引入 | 全量扫描（6 类盲区） |

**INSPECTION 报告**（`fcop/shared/INSPECTION-{date}-{NNN}-{scope}.md`）：

- YAML frontmatter：inspection_id / overall_status / p0-p2 违规数 / 预估整改时长
- P0 阻塞性 / P1 规范性 / P2 整洁性 违规详情（含证据 + 影响）
- **Execution Block**：按 Tier 1/2/3 分组的可复制整改命令建议（含回滚、执行人）
- append-only：同日同 scope 第二次跑产出 NNN+1，不覆盖原报告

**语义定位**：INSPECTION ≠ 整改指令。命令是建议（suggestion），执行决策由 ADMIN/PM 做出。

**ADMIN 工作流**：
1. 首次引入 fcop 到已有项目：`fcop_audit(scope="takeover")`
2. 阅读 INSPECTION 报告，逐项执行 Execution Block
3. 整改后复检：`fcop_audit(scope="auto")` → 验证违规是否清零

---

## 13. 资源（read-only URI）

资源是**只读上下文**——客户端可以把它们附到对话里。

| URI | MIME | 内容 |
|---|---|---|
| `fcop://status` | `text/markdown` | 与 `get_team_status()` 一致的项目状态快照 |
| `fcop://config` | `application/json` | `fcop/fcop.json` 原文（未初始化返回 `{"initialized": false, …}`） |
| `fcop://rules` | `text/markdown` | 协议规则正文（`fcop-rules.mdc`） |
| `fcop://protocol` | `text/markdown` | 协议解释（`fcop-protocol.mdc`） |
| `fcop://spec` | `text/markdown` | *(v1.1)* FCoP v1.1 完整规范——中文版（参考译文），含七大核心概念 + v1.1 五个新字段详细契约 |
| `fcop://spec/en` | `text/markdown` | *(v1.1)* FCoP v1.1 完整规范——英文版（权威版） |
| `fcop://letter/zh` | `text/markdown` | 《FCoP 致 ADMIN 的一封信》中文版 |
| `fcop://letter/en` | `text/markdown` | Letter to ADMIN — English |
| `fcop://prompt/install` | `text/markdown` | "让 agent 帮我装 fcop-mcp" 标准提示词（中文） |
| `fcop://prompt/install/en` | `text/markdown` | Same install prompt, English |
| `fcop://teams` | `application/json` | 内置团队索引（name / roles / leader） |
| `fcop://teams/{team}` | `text/markdown` | 指定团队的 `TEAM-README`（中文） |
| `fcop://teams/{team}/{role}` | `text/markdown` | 团队 + 角色档案（中文） |
| `fcop://teams/{team}/{role}/en` | `text/markdown` | 同上（英文） |

---

## 12. 常见问题

**项目根是怎么找到的？**  
`set_project_dir` → `FCOP_PROJECT_DIR` → 向上找 `fcop/fcop.json` / `fcop-rules.mdc` / `fcop/tasks/` → 当前 cwd。  
详见 [`mcp/README.md`](../mcp/README.md)。

**ADMIN / leader / 角色谁是谁？**  
`ADMIN` = 你（真人，**不**进 `fcop.json.roles`）；`leader` 是 AI 端的对外接口；其它角色只对 leader。Solo 模式下 `leader = role_code` 仍是 AI，不是你。

**`risk_level=high` 时必须 Review 吗？**  
协议层不强制阻塞，但 `high` / `irreversible` 的任务按 ADR-0024 应配套一个 `write_review`，且推荐 `decision="needs_human"` 由 ADMIN 用 `mark_human_approved` 闭合。

**升级了 `fcop-mcp` 还要不要改 `mcp.json`？**  
**1.x 内不必改**——工具/资源 shape 是只增不改的。改 `mcp.json` 仅当**换了启动方式**（`uvx` ↔ 固定 venv 的 `python -m fcop_mcp`）。

---

*This page is a navigation index. Authoritative descriptions live in source docstrings; this list is auto-checked against `tool_surface.json` by CI.*

