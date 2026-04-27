# FCoP MCP 工具与资源清单（fcop-mcp 0.6.x）

> 本页是 [`fcop-mcp`](https://pypi.org/project/fcop-mcp/) 暴露给 Cursor / Claude Desktop 等 MCP 客户端的**工具与资源**索引。**权威说明**仍在源码 docstring（[`mcp/src/fcop_mcp/server.py`](https://github.com/joinwell52-AI/FCoP/blob/main/mcp/src/fcop_mcp/server.py)）；本页是**导航与速查**，按类别分组、给出何时调用、参数要点。
>
> 稳定承诺：**整个 `0.6.x` 周期工具与资源「只增不改」**（[ADR-0003](../adr/ADR-0003-stability-charter.md)）。新增工具/参数允许；改名、删除、改语义不允许。

---

## 总览

- **工具（tools）26 个**（其中 `unbound_report` 自 0.6.3 起 **deprecated**，0.7.0 删除）：调用方主动触发，写盘或返回报告。
- **资源（resources）12 个**（9 个静态 URI + `fcop://teams/{team}` / `.../{role}` / `.../{role}/en` 三套模板）：只读 URI，常用于把规则/状态/职责模板以引用方式塞进上下文。

> **0.6.4 起新增** 2 个静态资源：`fcop://prompt/install`（中文）与
> `fcop://prompt/install/en`——agent 帮 ADMIN 装 fcop-mcp 的标准提示词，
> 装好以后随时可读。同时所有 `init_*` 工具新增 `force=True` 参数。
>
> **0.6.5 起**：`new_workspace` / `fcop_report` 在工具层落地
> [Rule 0.a.1](../src/fcop/rules/_data/fcop-rules.mdc) 四步循环
> （`write_task → 做 → write_report → archive_task`）——agent 跳步会被
> 即时提醒（**不阻塞**），具体见各工具说明。

> 看名字与参数清单（机器可读、CI 校验）：[`tests/test_fcop_mcp/snapshots/tool_surface.json`](../tests/test_fcop_mcp/snapshots/tool_surface.json)。  
> 看「为什么这么设计」：[`adr/ADR-0001`](../adr/ADR-0001-library-api.md)、[`adr/ADR-0003`](../adr/ADR-0003-stability-charter.md)。

---

## 1. 起手式（每次新会话先调）

| 工具 | 何时调 | 关键参数 |
|---|---|---|
| `fcop_report` | **每个新 MCP 会话的第一个调用**（FCoP Rule 0）。返回项目状态；**未初始化**时给出三选一初始化建议；**已初始化但本会话未认领角色**时输出 UNBOUND 报告，等 ADMIN 用「你是 \<ROLE\>」赋角色。报告头部含 `[版本] / [Versions]` 段，自动比对本地 `.cursor/rules/` 与 wheel 内捆绑版本，漂移时提示 ADMIN 调 `redeploy_rules`。**0.6.5 起**：已初始化分支末尾追加 Rule 0.a.1 四步循环模板（`write_task` → 做 → `write_report` → `archive_task`），中英双语，提醒 agent 跳步即违规。 | `lang`（`zh` / `en`） |
| `set_project_dir` | MCP 把项目根定位错了（典型：`fcop_report` 显示 `C:\Users\…` 不是你打开的工程）。**不改 `mcp.json`、不重启 Cursor**就能切到正确目录；UNBOUND 状态下也安全。 | `path`（绝对路径，目录须存在） |
| `unbound_report` | **deprecated**（0.6.3）。`fcop_report` 的别名，行为完全相同；调用即触发 `DeprecationWarning`，**0.7.0 移除**。把 system prompt / `LETTER-TO-ADMIN.md` 里的 `unbound_report` 改成 `fcop_report` 即可。 | `lang`（同上） |

---

## 2. 项目初始化（三选一）

| 工具 | 用途 | 关键参数 |
|---|---|---|
| `init_project` | 用**预设团队**模板初始化：`dev-team` / `media-team` / `mvp-team` / `qa-team`。建立 `docs/agents/` 五目录、写 `fcop.json`、把规则注入 `.cursor/rules/`、部署三层文档。**幂等**。 | `team`（默认 `dev-team`）、`lang` |
| `init_solo` | **Solo 模式**：单 AI 角色直接对 ADMIN，不做派发；Rule 0.b 仍生效（用文件做提议-审阅自审）。 | `role_code`（默认 `ME`）、`role_label`、`lang` |
| `create_custom_team` | **自定义角色**初始化。角色名进文件名、进权限。**强烈建议先 `validate_team_config` 干跑**。 | `team_name`、`roles`（逗号分隔）、`leader`、`lang` |
| `validate_team_config` | **不写盘**地校验自定义团队（中文字符、保留名、`leader` 不在 `roles` 等） | `roles`、`leader` |
| `get_available_teams` | 列出仓库内置团队及其 leader / 成员。`init_project` 前可先看一眼。 | `lang` |

---

## 3. 任务流（tasks/）

任务文件在 `docs/agents/tasks/`，命名 `TASK-YYYYMMDD-NNN-{SENDER}-to-{RECIPIENT}.md`。

| 工具 | 用途 | 关键参数 |
|---|---|---|
| `write_task` | 派一张任务单。库自动生成文件名与符合 FCoP v1.1 的 frontmatter。 | `sender`、`recipient`（支持 `ROLE.D1` 槽位 / `TEAM` 广播）、`subject`、`body`、`priority`（`P0`–`P3` 或别名）、`thread_key`、`references` |
| `read_task` | 读任务全文（含归档）。 | `filename`（文件名或纯 `TASK-…-NNN`） |
| `list_tasks` | 按发件人 / 收件人 / 状态 / 日期过滤；带分页。 | `sender`、`recipient`、`status`（`open` / `archived` / `all`）、`date`、`limit`、`offset` |
| `inspect_task` | **离线校验** schema 与「文件名↔frontmatter」一致性（典型：文件名说 `to-DEV` 但正文是 `recipient: QA`）。 | `filename` |
| `archive_task` | 把已完成任务（含同名报告）一起搬到 `docs/agents/log/`。 | `task_id` |

---

## 4. 报告流（reports/）

报告文件命名 `REPORT-<task_id>-{REPORTER}-to-{RECIPIENT}.md`，必须能反查源任务。

| 工具 | 用途 | 关键参数 |
|---|---|---|
| `write_report` | 写完成报告，回到指定收件人（通常是 leader/PM）。 | `task_id`、`reporter`、`recipient`、`body`、`status`（`done` / `in_progress` / `blocked`）、`priority` |
| `list_reports` | 过滤列出。 | `reporter`、`task_id`、`status`、`limit`、`offset` |
| `read_report` | 读报告全文。 | `filename`（或对应 `task_id`） |

---

## 5. 问题流（issues/）

| 工具 | 用途 | 关键参数 |
|---|---|---|
| `write_issue` | 上报问题：阻塞、规则不清、外部故障等。 | `reporter`、`summary`、`body`、`severity`（`critical` / `high` / `medium` / `low`，亦支持 `P0`–`P3` 别名） |
| `list_issues` | 过滤列出。 | `reporter`、`severity`、`limit`、`offset` |

> 没有 `read_issue` 是历史选择；如需逐条读，直接用编辑器/Project API。

---

## 6. 团队 / 共享文档 / 工作区

| 工具 | 用途 | 关键参数 |
|---|---|---|
| `get_team_status` | 项目状态快照：是否初始化、团队/leader、open task / report / issue 数、最近 5 条活动。 | `lang` |
| `deploy_role_templates` | 部署 / 刷新 `docs/agents/shared/` 里的 `TEAM-README` + `TEAM-ROLES` + `TEAM-OPERATING-RULES` 与角色档案。`force=True` 时**先归档**到 `.fcop/migrations/<时间戳>/` 再覆盖（可逆）。 | `team`、`lang`、`force`（默认 `True`） |
| `new_workspace` | 在 `workspace/<slug>/` 下建工作目录，**不要把代码写到项目根**。幂等，二次调用更新元数据。**0.6.5 起**：若当前没有任何开放 `TASK-*.md` 的 `subject` / `body` / `references` 提到这个 slug，工具返回头部会**预置一段 Rule 0.a.1 提醒**——建议先 `write_task` 把"要做什么"落文件，再开工作区动手。提醒不阻塞，工作区照常创建（合法的离线 / 实验流程不破坏）。 | `slug`（`^[a-z][a-z0-9-]*$`、≤ 40）、`title`、`description` |
| `list_workspaces` | 列出现有 `workspace/<slug>/`（含手动建的）。 | `lang` |

---

## 7. 协议泄压阀

| 工具 | 用途 | 关键参数 |
|---|---|---|
| `drop_suggestion` | **唯一**让 agent 对协议提反对意见的合法通道：写一份带时间戳的 markdown 到 `.fcop/proposals/`。**禁止**自己改 `fcop-rules.mdc` / `fcop-protocol.mdc`。 | `content`、`context` |

---

## 8. 维护（自检与升级）

| 工具 | 用途 | 关键参数 |
|---|---|---|
| `check_update` | 比对本地 `fcop-mcp` 与 PyPI 最新版（不写盘、不安装）。 | `lang` |
| `upgrade_fcop` | 打印**针对你的安装方式**（`pip` / `pipx` / `uvx`）的升级命令。**不**自动跑 pip——MCP 进程不能安全自升。 | `lang` |
| `redeploy_rules` | **ADMIN-only**（agent 不应主动调）。把 wheel 里的四份协议规则——`.cursor/rules/fcop-rules.mdc`、`.cursor/rules/fcop-protocol.mdc`、`AGENTS.md`、`CLAUDE.md`——host-neutral 地写到项目根。`force=True` 覆写，`archive=True` 先把旧文件归档到 `.fcop/migrations/<时间戳>/rules/`。何时调：`fcop_report` 显示版本漂移、或 ADMIN 在聊天框明确说"重部署规则"。背景：[ADR-0006](../adr/ADR-0006-host-neutral-rule-distribution.md)。 | `force`（默认 `True`）、`archive`（默认 `True`）、`lang` |

> 详细的升级流程（同环境升两包、重启 IDE、自检命令、协议规则文件升级）：[`docs/upgrade-fcop-mcp.md`](./upgrade-fcop-mcp.md)。

---

## 9. 资源（read-only URI）

资源是**只读上下文**——客户端可以把它们附到对话里。  

| URI | MIME | 内容 |
|---|---|---|
| `fcop://status` | `text/markdown` | 与 `get_team_status()` 一致的项目状态快照 |
| `fcop://config` | `application/json` | `docs/agents/fcop.json` 原文（未初始化返回 `{"initialized": false, …}`） |
| `fcop://rules` | `text/markdown` | 协议规则正文（`fcop-rules.mdc`） |
| `fcop://protocol` | `text/markdown` | 协议解释（`fcop-protocol.mdc`） |
| `fcop://letter/zh` | `text/markdown` | 《FCoP 致 ADMIN 的一封信》中文版 |
| `fcop://letter/en` | `text/markdown` | Letter to ADMIN — English |
| `fcop://prompt/install` | `text/markdown` | *(0.6.4)* "让 agent 帮我装 fcop-mcp" 标准提示词（中文） |
| `fcop://prompt/install/en` | `text/markdown` | *(0.6.4)* Same install prompt, English |
| `fcop://teams` | `application/json` | 内置团队索引（name / roles / leader） |
| `fcop://teams/{team}` | `text/markdown` | 指定团队的 `TEAM-README`（中文） |
| `fcop://teams/{team}/{role}` | `text/markdown` | 团队 + 角色档案（中文） |
| `fcop://teams/{team}/{role}/en` | `text/markdown` | 同上（英文） |

---

## 10. 一些常被问到的细节

**项目根是怎么找到的？**  
`set_project_dir` → `FCOP_PROJECT_DIR` → 历史变量 `CODEFLOW_PROJECT_DIR`（弃用警告）→ 向上找 `docs/agents/fcop.json` / `fcop-rules.mdc` / `docs/agents/tasks/` → 当前 cwd。  
详见 [`mcp/README.md`](../mcp/README.md) 与 [ADR-0003](../adr/ADR-0003-stability-charter.md)。

**ADMIN / leader / 角色谁是谁？**  
`ADMIN` = 你（真人，**不**进 `fcop.json.roles`）；`leader` 是 AI 端的对外接口；其它角色只对 leader。Solo 模式下 `leader = role_code` 仍是 AI，不是你。

**升级了 `fcop-mcp` 还要不要改 `mcp.json`？**  
**0.6.x 内不必改**——工具/资源 shape 是只增不改的。改 `mcp.json` 仅当**换了启动方式**（`uvx` ↔ 固定 venv 的 `python -m fcop_mcp`）。

---

*This page is a navigation index. Authoritative descriptions live in source docstrings; this list is auto-checked against `tool_surface.json` by CI.*
