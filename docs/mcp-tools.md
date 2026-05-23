# FCoP MCP 工具清单（fcop-mcp 3.x）<!-- 45 tools — v3.2.2 release -->

> 本页是 [`fcop-mcp`](https://pypi.org/project/fcop-mcp/) 暴露给 Cursor / Claude Desktop 等 MCP 客户端的**工具**索引。**权威说明**仍在源码 docstring（[`mcp/src/fcop_mcp/server.py`](https://github.com/joinwell52-AI/FCoP/blob/main/mcp/src/fcop_mcp/server.py)）；本页是**导航与速查**，按类别分组。
>
> 稳定承诺：**整个 `3.x` 周期工具「只增不改」**。新增工具/参数允许；改名、删除、改语义不允许。

---

## 总览

**工具（tools）共 45 个**，按 Tier 分级：

| Tier | 含义 | 工具数 |
|------|------|--------|
| L0 | 只读/查询，无写盘 | 若干 |
| L1 | 写盘操作，需绑定角色（`binding_required`） | 大多数 |

**v3 新增（相对 v2/v1.x）：**

- **v3 任务生命周期**（5 个）：`claim_task` / `submit_task` / `finish_task` / `approve_task` / `reject_task`
- **历史深档案**（4 个）：`archive_to_history` / `bulk_archive_to_history` / `list_history` / `read_history_task`
- **v3 spec 对齐**（1 个）：`create_task`（`write_task` 的 v3 规范别名）

---

## 1. 起手式（每次新会话先调）

| 工具 | 何时调 | 关键参数 |
|------|--------|----------|
| `fcop_report` | **每个新 MCP 会话的第一个调用**（FCoP Rule 0）。返回项目状态；未初始化时给出三选一初始化建议；已初始化但本会话未认领角色时输出 UNBOUND 报告。报告头部含版本比对，漂移时提示 `redeploy_rules`。 | `lang`（`zh`/`en`） |
| `set_project_dir` | MCP 把项目根定位错了，不改 `mcp.json`、不重启 Cursor 就能切换。 | `path`（绝对路径） |
| `fcop_check` | 日常轻量自检：schema 合规、文件名一致性、frontmatter 完整性，含治理事件日志摘要。不写盘。 | `lang` |

---

## 2. 项目初始化（三选一）

| 工具 | 用途 | 关键参数 |
|------|------|----------|
| `init_project` | 用**预设团队**模板初始化：`dev-team` / `media-team` / `mvp-team` / `qa-team`。建立 `fcop/` 五目录 + `history/`，写 `fcop.json`，部署三层文档。**幂等**。 | `team`（默认 `dev-team`）、`lang` |
| `init_solo` | **Solo 模式**：单 AI 角色直接对 ADMIN，不做派发。 | `role_code`（默认 `ME`）、`role_label`、`lang` |
| `create_custom_team` | **自定义角色**初始化。强烈建议先 `validate_team_config` 干跑。 | `team_name`、`roles`（逗号分隔）、`leader`、`lang` |
| `validate_team_config` | **不写盘**地校验自定义团队配置。 | `roles`、`leader` |
| `get_available_teams` | 列出仓库内置团队及其 leader / 成员。 | `lang` |

---

## 3. 任务创建与查询

任务文件命名：`TASK-YYYYMMDD-NNN-{SENDER}-to-{RECIPIENT}.md`  
v3 项目任务落在 `_lifecycle/` 各阶段目录；v2 项目落在 `fcop/tasks/`。

| 工具 | 用途 | 关键参数 |
|------|------|----------|
| `create_task` | **v3 规范 §8 L1 入口**：创建任务，v3 项目落入 `_lifecycle/inbox/`，v2 落入 `fcop/tasks/`。与 `write_task` 功能完全相同，命名符合 spec。 | `sender`、`recipient`、`subject`、`body`、`priority`（`P0`–`P3`）、`thread_key`、`references`、`risk_level` |
| `write_task` | 同 `create_task`（v2 兼容名称，长期维护）。 | 同上 |
| `read_task` | 读任务全文（含各阶段目录）。 | `filename`（文件名或 `TASK-…-NNN`） |
| `list_tasks` | 按发件人 / 收件人 / 状态 / 日期过滤，带分页。 | `sender`、`recipient`、`status`、`date`、`limit`、`offset` |
| `inspect_task` | **离线校验** schema 与「文件名↔frontmatter」一致性，不写盘。 | `filename` |
| `archive_task` | 把 `done/` 里的已完成任务（含同名报告）搬到 `_lifecycle/archive/`（v3）或 `fcop/log/`（v2）。 | `task_id` |

> **`risk_level`**：`high` / `irreversible` 的任务按 ADR-0024 应配套 `write_review(decision="needs_human")`，由 ADMIN 用 `mark_human_approved` 闭合审批链。

---

## 4. v3 任务生命周期流转

> **仅 v3 项目有效**；v2 项目调用这些工具会返回提示性 no-op 消息。

v3 任务在 `_lifecycle/` 下按阶段流转：

```
inbox → active → review → done → archive → history/YYYY-MM-DD/<stem>/
              ↘ (直接完成，无需审核) ↗
```

| 工具 | 阶段流转 | 关键参数 |
|------|----------|----------|
| `claim_task` | `inbox` → `active`：agent 领取任务，开始执行。 | `task_id`、`actor`（领取者角色码） |
| `submit_task` | `active` → `review`：agent 提交工作，等待审核。 | `task_id`、`actor` |
| `finish_task` | `active` → `done`：agent 直接完成（无需审核路径）。 | `task_id`、`actor` |
| `approve_task` | `review` → `done`：ADMIN/治理角色审核通过。 | `task_id`、`actor`（默认 `ADMIN`）、`note` |
| `reject_task` | `review` → `active`：ADMIN 打回重做，task 退回 active 阶段供修改。 | `task_id`、`actor`、`note`（建议写明原因） |

---

## 5. 报告流（reports/）

| 工具 | 用途 | 关键参数 |
|------|------|----------|
| `write_report` | 写完成报告，回到指定收件人（通常是 leader/PM）。 | `task_id`、`reporter`、`recipient`、`body`、`status`（`done`/`in_progress`/`blocked`）、`priority` |
| `list_reports` | 过滤列出。 | `reporter`、`task_id`、`status`、`limit`、`offset` |
| `read_report` | 读报告全文。 | `filename`（或对应 `task_id`） |

---

## 6. 问题流（issues/）

| 工具 | 用途 | 关键参数 |
|------|------|----------|
| `write_issue` | 上报问题：阻塞、规则不清、外部故障等。 | `reporter`、`summary`、`body`、`severity`（`critical`/`high`/`medium`/`low`，亦支持 `P0`–`P3`） |
| `list_issues` | 过滤列出。 | `reporter`、`severity`、`limit`、`offset` |

---

## 7. 审核流（reviews/）

REVIEW 文件是治理层对制品的决策记录（ADR-0017）。

| 工具 | 用途 | 关键参数 |
|------|------|----------|
| `write_review` | 写一份 REVIEW（治理层决策）。 | `reviewer_role`、`subject_type`（`task`/`report`/`role_switch`/`code_change`）、`subject_ref`、`decision`（见下表）、`rationale`、`required_changes`（`needs_changes` 时必填）、`reviewer_agent`、`body`、`subject_short` |
| `list_reviews` | 过滤列出，标注 `[human_approval pending]` / `[human_approved]`。 | `reviewer_role`、`decision`、`subject_type`、`status`（`open`/`archived`/`all`）、`limit`、`offset` |
| `read_review` | 读 REVIEW 全文，含 `human_approval` 子结构展示。 | `filename`（文件名或 Review ID） |
| `mark_human_approved` | **关闭 `needs_human` 升级回路**（ADR-0026）。把 `human_approval` 事件写入已有 REVIEW frontmatter。approver 必须是 `layer: admin` 的角色。 | `review_id`、`approver`、`decision`（`approve`/`reject`）、`channel`、`comment` |

**`decision` 枚举（5 值）：**

| 值 | 含义 |
|----|------|
| `approved` | 制品通过，可以继续 |
| `rejected` | 制品被否决，不得继续 |
| `needs_changes` | 需要修改（必须配 `required_changes`） |
| `abstained` | 审核者回避 |
| `needs_human` | agent 主动上升人工——REVIEW 停留 pending，ADMIN 需调 `mark_human_approved` 闭合 |

---

## 8. 历史深档案（history/）— v3 新增

> **仅 v3 项目有效**。历史档案按日期分片存储在 `history/YYYY-MM-DD/<task-stem>/`，永不覆盖，适合长期回溯。

**典型归档流程（v3）：**

```
finish_task / approve_task
       ↓
   _lifecycle/done/
       ↓ archive_task
   _lifecycle/archive/
       ↓ archive_to_history（单个）或 bulk_archive_to_history（批量）
   history/2026-05-22/TASK-20260522-001-ME-to-ADMIN/
       ├── TASK-20260522-001-ME-to-ADMIN.md
       └── REPORT-20260522-001-ME-to-ADMIN.md
```

| 工具 | 用途 | 关键参数 |
|------|------|----------|
| `archive_to_history` | 把单个任务（及其关联报告）从 `_lifecycle/archive/` 移入 `history/YYYY-MM-DD/<stem>/`。**先调 `archive_task`，再调本工具**。 | `task_id`、`done_date`（覆盖日期分片，默认使用任务自身 `done_at`） |
| `bulk_archive_to_history` | 把 `_lifecycle/archive/` 里**所有**任务批量迁入历史档案。一次性迁移利器，适合升级后批量整理旧归档。 | `done_date`（为所有任务统一覆盖日期，留空则各自读 `done_at`） |
| `list_history` | 列出历史档案。不传 `date` 时列所有日期分片（最新在前）；传 `date` 时列该分片下所有任务。 | `date`（`YYYY-MM-DD`，可选） |
| `read_history_task` | 从历史档案读取指定任务全文。传 `date` 可限定分片范围，速度更快。 | `task_id`、`date`（可选） |

---

## 9. 团队 / 共享文档 / 工作区

| 工具 | 用途 | 关键参数 |
|------|------|----------|
| `get_team_status` | 项目状态快照：初始化状态、团队/leader、open task/report/issue/review 数、最近活动。 | `lang` |
| `deploy_role_templates` | 部署 / 刷新 `fcop/shared/` 里的团队文档与角色档案。`force=True` 时先归档再覆盖。 | `team`、`lang`、`force`（默认 `True`） |
| `new_workspace` | 在 `workspace/<slug>/` 下建工作目录，**不要把代码写到项目根**。幂等。 | `slug`（`^[a-z][a-z0-9-]*$`、≤ 40）、`title`、`description` |
| `list_workspaces` | 列出现有 `workspace/<slug>/`。 | `lang` |

---

## 10. 协议泄压阀

| 工具 | 用途 | 关键参数 |
|------|------|----------|
| `drop_suggestion` | **唯一**让 agent 对协议提反对意见的合法通道：写一份带时间戳的 markdown 到 `.fcop/proposals/`。**禁止**自己改 `fcop-rules.mdc`。 | `content`、`context` |

---

## 11. 维护（自检与升级）

| 工具 | 用途 | 关键参数 |
|------|------|----------|
| `check_update` | 比对本地 `fcop-mcp` 与 PyPI 最新版（不写盘、不安装）。 | `lang` |
| `upgrade_fcop` | 打印**针对你的安装方式**的升级命令。**不**自动跑 pip。 | `lang` |
| `redeploy_rules` | **ADMIN-only**。把 wheel 里四份规则文件写到项目根；`force=True` 覆写，`archive=True` 先归档旧文件。何时调：`fcop_report` 显示版本漂移。 | `force`（默认 `True`）、`archive`（默认 `True`）、`lang` |

---

## 12. 治理事件审计

> 基于 ADR-0030-bis Layer 1 MCP Middleware。每个工具调用自动打 `risk` 标签并写入 `fcop_events.jsonl`。

| 工具 | 用途 | 关键参数 |
|------|------|----------|
| `list_governance_events` | 读取 `fcop_events.jsonl`，列出最近 N 条治理事件（tool / risk / tag / session_id / 时间戳）。 | `last_n`（默认 50）、`risk`（过滤）、`tag`（过滤） |
| `get_governance_summary` | 汇总统计：总调用量 / 各风险层分布 / Top 10 工具 / CRITICAL_TAG 事件清单。 | 无 |

---

## 13. 治理告警（GAL — ADR-0031）

> `fcop_check()` 自动扫描治理漂移信号，命中则写入 `fcop/alerts/ALERT-*.md`。

| 工具 | 用途 | 关键参数 |
|------|------|----------|
| `fcop_list_alerts` | 读取告警收件箱，支持按 `status` / `severity` 过滤。 | `status`（`open`/`acknowledged`/`resolved`）、`severity`、`last_n`（默认 20） |
| `fcop_create_alert` | ADMIN / 治理观察者手动归档治理缺口。 | `severity`、`alert_type`、`summary`、`suggestion` |

**告警类型：**

| 类型 | 触发条件 | 严重度 |
|------|----------|--------|
| `critical_tool_unreviewed` | 24h 内有 CRITICAL_TAG 工具调用，但无对应 Review 文件 | high |
| `missing_independent_verdict` | 执行窗口 > 6h 无任何治理事件（Solo Blindspot，FCoP-Rule-G1） | high |
| `long_running_without_reconciliation` | open Task 超 24h 未归档 | low |

**FCoP-Rule-G1**：`write_report` / `fcop_report` ∈ 执行域，不构成治理信号。只有 `write_review` / `mark_human_approved` / `fcop_check` 才算独立治理视角。

---

## 14. 协议体检（fcop_audit）

> 一次性深度体检；`fcop_check` 是日常轻量自检，二者互补。

| 工具 | 用途 | 关键参数 |
|------|------|----------|
| `fcop_audit` | 三场景协议体检，发现 6 类合规盲区，产出 INSPECTION 报告（含 Execution Block 整改建议）。 | `scope`（`new`/`upgrade`/`takeover`/`auto`，默认 `auto`）、`output`（`file`/`stdout`/`both`）、`project_path` |

**三场景：**

| 场景 | 触发条件 | 扫描内容 |
|------|----------|----------|
| `new` | 新项目验收 | 协议文件是否完整部署 |
| `upgrade` | 版本升级后验收 | 规则/文档版本是否同步 |
| `takeover` | 老 non-fcop 项目首次引入 | 全量扫描（6 类盲区） |

---

## 附录：工具完整列表（45 个）

| # | 工具 | 分类 | Tier |
|---|------|------|------|
| 1 | `fcop_report` | 起手式 | L0 |
| 2 | `set_project_dir` | 起手式 | L1 |
| 3 | `fcop_check` | 起手式 | L0 |
| 4 | `init_project` | 初始化 | L1 |
| 5 | `init_solo` | 初始化 | L1 |
| 6 | `create_custom_team` | 初始化 | L1 |
| 7 | `validate_team_config` | 初始化 | L0 |
| 8 | `get_available_teams` | 初始化 | L0 |
| 9 | `create_task` | 任务 | L1 |
| 10 | `write_task` | 任务 | L1 |
| 11 | `read_task` | 任务 | L0 |
| 12 | `list_tasks` | 任务 | L0 |
| 13 | `inspect_task` | 任务 | L0 |
| 14 | `archive_task` | 任务 | L1 |
| 15 | `claim_task` | v3 生命周期 | L1 |
| 16 | `submit_task` | v3 生命周期 | L1 |
| 17 | `finish_task` | v3 生命周期 | L1 |
| 18 | `approve_task` | v3 生命周期 | L1 |
| 19 | `reject_task` | v3 生命周期 | L1 |
| 20 | `write_report` | 报告 | L1 |
| 21 | `list_reports` | 报告 | L0 |
| 22 | `read_report` | 报告 | L0 |
| 23 | `write_issue` | 问题 | L1 |
| 24 | `list_issues` | 问题 | L0 |
| 25 | `write_review` | 审核 | L1 |
| 26 | `list_reviews` | 审核 | L0 |
| 27 | `read_review` | 审核 | L0 |
| 28 | `mark_human_approved` | 审核 | L1 |
| 29 | `archive_to_history` | 历史档案 | L1 |
| 30 | `bulk_archive_to_history` | 历史档案 | L1 |
| 31 | `list_history` | 历史档案 | L0 |
| 32 | `read_history_task` | 历史档案 | L0 |
| 33 | `get_team_status` | 团队/工作区 | L0 |
| 34 | `deploy_role_templates` | 团队/工作区 | L1 |
| 35 | `new_workspace` | 团队/工作区 | L1 |
| 36 | `list_workspaces` | 团队/工作区 | L0 |
| 37 | `drop_suggestion` | 泄压阀 | L1 |
| 38 | `check_update` | 维护 | L0 |
| 39 | `upgrade_fcop` | 维护 | L0 |
| 40 | `redeploy_rules` | 维护 | L1 |
| 41 | `list_governance_events` | 治理审计 | L0 |
| 42 | `get_governance_summary` | 治理审计 | L0 |
| 43 | `fcop_list_alerts` | GAL | L0 |
| 44 | `fcop_create_alert` | GAL | L1 |
| 45 | `fcop_audit` | 体检 | L0 |

---

## 常见问题

**项目根是怎么找到的？**  
`set_project_dir` → `FCOP_PROJECT_DIR` → 向上找 `fcop/fcop.json` / `fcop-rules.mdc` / `fcop/tasks/` → 当前 cwd。

**`create_task` vs `write_task`？**  
功能完全相同。`create_task` 是 FCoP v3 规范 §8 的命名；`write_task` 是 v1/v2 兼容名称。两者长期并存。

**v3 生命周期工具在 v2 项目能用吗？**  
不能，但不会报错——会返回提示性 no-op 消息，说明当前是 v2 项目。

**`history/` 和 `_lifecycle/archive/` 有什么区别？**  
`_lifecycle/archive/` 是中间站（已完成但待深度归档）；`history/` 是最终归宿（按日期分片，永久只读）。`archive_to_history` 负责把任务从前者迁移到后者。

**`risk_level=high` 时必须 Review 吗？**  
协议层不强制阻塞，但 `high` / `irreversible` 的任务按 ADR-0024 应配套一个 `write_review`，且推荐 `decision="needs_human"` 由 ADMIN 用 `mark_human_approved` 闭合。

**升级了 `fcop-mcp` 还要不要改 `mcp.json`？**  
**3.x 内不必改**——工具 shape 是只增不改的。改 `mcp.json` 仅当换了启动方式（`uvx` ↔ 固定 venv 的 `python -m fcop_mcp`）。

---

*本页是导航索引，权威说明在源码 docstring；工具列表由 CI 对照 `tool_surface.json` 校验。*
