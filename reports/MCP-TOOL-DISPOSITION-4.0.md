# FCoP 4.0 MCP 工具逐项处置

> Canonical source：`tests/test_fcop_mcp/snapshots/tool_surface.json`
> Registration source：`mcp/src/fcop_mcp/server.py`
> 基线：`origin/main@68dbeb15f4e7f84e1d03f907be9fa66c2265843e`

## 1. 口径与证据

- snapshot 导出 **45** 个唯一工具；server 的 `@mcp.tool` 注册链与 snapshot tests 一致。
- `CORE_MAPPING` 只表示工具映射到 Base Core 语义；MCP 工具本身仍是 Toolkit/adapter。
- “v4 行为”是 WP1 输入，不是本轮实现；名称保留不证明行为兼容。
- 证据简写：`S`=canonical snapshot；`R`=`server.py` 注册/调用链；`P`=`src/fcop/project.py`；`L`=`src/fcop/lifecycle/`；`T`=`tests/test_fcop_mcp`（80 passed）及全量测试（1225 passed）。

## 2. 45 个工具

| # | 当前工具名 | 当前参数（`?`=可选） | 当前调用目标 | 当前写入/移动 | 主 Disposition | v4 行为 | 兼容别名 | 风险 | 测试证据 | 决定理由 |
|---:|---|---|---|---|---|---|---|---|---|---|
| 1 | `approve_task` | actor?, note?, task_id | MCP 内构造 event → `atomic.commit` | review→done + event | `CORE_MAPPING` | 必须绑定当前 REVIEW/evidence 与授权引用 | 无 | critical | S/R/L/T | 映射 C3/C5/C6，当前 actor 自报不够 |
| 2 | `archive_task` | lang?, task_id | `Project.archive_task` | 当前可从多阶段链式移到 archive | `CORE_MAPPING` | 只接受合同允许的源态并检查 family/evidence/auth | 无 | critical | S/R/P/T | 映射 C3/C5/C6，但现有跨级行为不可直接继承 |
| 3 | `archive_to_history` | done_date?, task_id | `Project.archive_to_history` | archive TASK/REPORT→history | `LEGACY_V3_ONLY` | 取决于 WP1 的三选一 history 权威模型 | 无 | high | S/R/P/T | 当前移动非原子且改变权威路径 |
| 4 | `bulk_archive_to_history` | done_date? | `Project.bulk_archive_to_history` | 批量执行深归档 | `LEGACY_V3_ONLY` | 仅在选定 history 模型后保留 | 无 | high | S/R/P/T | 不是 Base 第六生命周期 |
| 5 | `check_update` | lang? | 包版本/PyPI 检查 | 网络读取，不写协议事实 | `TOOLKIT_CONVENIENCE` | 保持非规范性更新提示 | 无 | low | S/R/T | 与 Core 无关 |
| 6 | `claim_task` | actor?, task_id | MCP event → `atomic.commit` | inbox→active + event | `CORE_MAPPING` | 绑定 operation/attempt；actor 与授权分离 | 无 | high | S/R/L/T | 映射 C3/C5/C7/C8 |
| 7 | `create_custom_team` | force?, lang?, leader, roles, team_name | team config/init helpers | 写 workspace/profile/rules | `TOOLKIT_CONVENIENCE` | 生成 Profile，不定义 Core 角色 | 无 | high | S/R/P/T | 固定团队与角色在 Profile |
| 8 | `create_task` | body, parent?, priority?, recipient, references?, risk_level?, sender, subject, thread_key? | `Project.write_task` | 新建 inbox TASK | `CORE_MAPPING` | 支持稳定 operation identity/digest 与 v4 relations | `write_task`（语义别名） | critical | S/R/P/T | C2/C4/C7/C8 的创建入口 |
| 9 | `deploy_role_templates` | force?, lang?, team? | `Project.deploy_role_templates` | 覆盖/归档 Profile 文档 | `TOOLKIT_CONVENIENCE` | 仅 Profile；显式授权且不得改 Core | 无 | high | S/R/P/T | 部署便利层 |
| 10 | `drop_suggestion` | content, context? | proposal helper | 写 `.fcop/proposals/` | `OPTIONAL_EXTENSION` | 非规范 observation/proposal | 无 | low | S/R/T | 不属于四类正式 envelope |
| 11 | `fcop_audit` | output?, project_path?, scope? | audit compiler | 可只读或写 INSPECTION | `TOOLKIT_CONVENIENCE` | 只消费/报告 Core 事实 | 无 | medium | S/R/T | 审计工具不定义事实 |
| 12 | `fcop_check` | lang? | project/schema/drift checks | 只读 | `TOOLKIT_CONVENIENCE` | v4 conformance reader | 无 | low | S/R/T | 可重实现的检查器 |
| 13 | `fcop_create_alert` | alert_type, severity, suggestion?, summary | GAL alert store | 写 alert | `OPTIONAL_EXTENSION` | 保持 Toolkit/GAL，不进四 envelope Core | 无 | medium | S/R/T | 治理提醒不是 Base 文件类型 |
| 14 | `fcop_list_alerts` | last_n?, severity?, status? | GAL reader | 只读 alerts | `OPTIONAL_EXTENSION` | 同上 | 无 | low | S/R/T | 派生治理视图 |
| 15 | `fcop_report` | lang? | status/drift/report builder | 主要只读诊断 | `TOOLKIT_CONVENIENCE` | 启动报告，不定义 workspace 真相 | 无 | low | S/R/T | Host convenience |
| 16 | `finish_task` | actor?, task_id | MCP event → `atomic.commit` | active→done + event | `LEGACY_V3_ONLY` | 若保留必须有当前 REPORT + explicit auth；否则 v4 workspace 移除 | 无 | critical | S/R/L/T | 当前跳过 review 且无机械 gate |
| 17 | `get_available_teams` | lang? | bundled team catalog | 只读 templates | `TOOLKIT_CONVENIENCE` | Profile catalog | 无 | low | S/R/T | 非 Core |
| 18 | `get_governance_summary` | 无 | governance event summarizer | 只读派生摘要 | `OPTIONAL_EXTENSION` | 不得成为授权事实源 | 无 | low | S/R/T | GAL/治理观察 |
| 19 | `get_team_status` | lang? | `Project.status`/format | 只读 | `TOOLKIT_CONVENIENCE` | 由磁盘事实派生 | 无 | low | S/R/P/T | 状态视图 |
| 20 | `init_project` | force?, lang?, team? | `Project.init` + template deployment | 创建 workspace/profile/rules | `TOOLKIT_CONVENIENCE` | 写 v4 manifest/Encoding，但 team 为 Profile | 无 | critical | S/R/P/T | bootstrap 便利层，风险高 |
| 21 | `init_solo` | force?, lang?, role_code?, role_label? | `Project.init` | 创建 solo workspace/profile/rules | `TOOLKIT_CONVENIENCE` | solo 是 Profile，Core 身份不依赖角色名 | 无 | critical | S/R/P/T | 同上 |
| 22 | `inspect_task` | filename | `Project.inspect_task` | 只读校验 | `TOOLKIT_CONVENIENCE` | 校验 v4 envelope/path/relations | 无 | low | S/R/P/T | Core 的观察器 |
| 23 | `list_governance_events` | last_n?, risk?, tag? | governance log reader | 只读派生事件 | `OPTIONAL_EXTENSION` | 不得替代 REVIEW/authorization fact | 无 | low | S/R/T | GAL 视图 |
| 24 | `list_history` | date? | `Project.list_history` | 只读 history | `LEGACY_V3_ONLY` | 若 history 成为 v4 合法 Encoding，则转 Toolkit read | 无 | low | S/R/P/T | 依赖 history 决策 |
| 25 | `list_issues` | lang?, limit?, offset?, reporter?, severity? | `Project.list_issues` | 只读 issues | `TOOLKIT_CONVENIENCE` | 查询四类 envelope | 无 | low | S/R/P/T | 名称/分页非 Core |
| 26 | `list_reports` | limit?, offset?, reporter?, status?, task_id? | `Project.list_reports` | 只读 reports | `TOOLKIT_CONVENIENCE` | 支持 attempt/ref 查询但不定义其有效性 | 无 | low | S/R/P/T | 查询便利层 |
| 27 | `list_reviews` | decision?, limit?, offset?, reviewer_role?, status?, subject_type? | `Project.list_reviews` | 只读 reviews | `TOOLKIT_CONVENIENCE` | 支持 review_kind/subject/ref 查询 | 无 | low | S/R/P/T | 查询便利层 |
| 28 | `list_tasks` | date?, limit?, offset?, recipient?, sender?, status? | `Project.list_tasks` | 只读 lifecycle | `TOOLKIT_CONVENIENCE` | 从路径读 NOW；可按 relation 查询 | 无 | low | S/R/P/T | 查询便利层 |
| 29 | `list_workspaces` | lang? | workspace registry/discovery | 只读 registry | `TOOLKIT_CONVENIENCE` | discovery 不成为 workspace identity 真相 | 无 | low | S/R/T | Host convenience |
| 30 | `mark_human_approved` | approver, channel?, comment?, decision, review_id | `Project.mark_human_approved` | 当前原地改写 REVIEW | `CORE_MAPPING` | 改为追加独立 authorization/REVIEW fact，旧 REVIEW 不变 | 无 | critical | S/R/P/T | 映射 C6，当前行为必须改变 |
| 31 | `new_workspace` | description?, slug, title? | workspace creation helper | 创建目录/manifest/registry | `TOOLKIT_CONVENIENCE` | 原子创建 C1 manifest；registry 可重建 | 无 | critical | S/R/P/T | 创建器不是 Core 本身 |
| 32 | `read_history_task` | date?, task_id | `Project.read_history_task` | 只读 history | `LEGACY_V3_ONLY` | 取决于 history 模型 | 无 | low | S/R/P/T | v3 冷存储 reader |
| 33 | `read_report` | filename | `Project.read_report` | 只读 | `TOOLKIT_CONVENIENCE` | 读取正式 REPORT envelope | 无 | low | S/R/P/T | 查询便利层 |
| 34 | `read_review` | filename | `Project.read_review` | 只读 | `TOOLKIT_CONVENIENCE` | 读取正式 REVIEW/authorization fact | 无 | low | S/R/P/T | 查询便利层 |
| 35 | `read_task` | filename | `Project.read_task` | 只读 | `TOOLKIT_CONVENIENCE` | 读取 TASK，状态仍取路径 | 无 | low | S/R/P/T | 查询便利层 |
| 36 | `redeploy_rules` | archive?, force?, lang? | `Project.deploy_protocol_rules` | 覆盖规则副本并可归档旧文件 | `TOOLKIT_CONVENIENCE` | 仅显式 ADMIN/Profile 操作；不得暗改规范/行为 | 无 | critical | S/R/P/T | 高风险部署工具，不属 Core |
| 37 | `reject_task` | actor?, note?, task_id | MCP event → `atomic.commit` | review→active + event | `CORE_MAPPING` | 需 durable authorization；开始新 attempt 并使旧收敛失效 | 无 | high | S/R/L/T | C3/C5/C6 |
| 38 | `set_project_dir` | path | MCP 绑定状态 | 改进程内当前项目，不改协议文件 | `TOOLKIT_CONVENIENCE` | Host adapter binding | 无 | medium | S/R/T | 不得成为 workspace identity |
| 39 | `submit_task` | actor?, task_id | MCP event → `atomic.commit` | active→review + event | `CORE_MAPPING` | 对所有 TASK 强制当前 attempt REPORT | 无 | high | S/R/L/T | C3/C5 |
| 40 | `upgrade_fcop` | lang? | package-manager subprocess | 修改 Python 环境/可能影响部署 | `OPTIONAL_EXTENSION` | 与协议工作区分离；显式 ADMIN 授权 | 无 | critical | S/R/T | 更新器不是协议，且外部副作用大 |
| 41 | `validate_team_config` | leader, roles | team validation | 只读 | `TOOLKIT_CONVENIENCE` | Profile validator | 无 | low | S/R/T | 固定角色不进 Core |
| 42 | `write_issue` | body, reporter, severity?, summary | `Project.write_issue` | 新建 ISSUE | `CORE_MAPPING` | 四 envelope 之一；冻结 subject_ref 可选/必填规则 | 无 | high | S/R/P/T | C2/C4 |
| 43 | `write_report` | body, priority?, recipient, reporter, status?, task_id | `Project.write_report` | 新建 REPORT | `CORE_MAPPING` | 绑定当前 attempt/subject，append-only | 无 | high | S/R/P/T | C2/C5 |
| 44 | `write_review` | body?, decision, rationale?, required_changes?, reviewer_agent?, reviewer_role, subject_ref, subject_short?, subject_type | `Project.write_review` | 新建 REVIEW | `CORE_MAPPING` | 增加 review_kind/references；授权资格归 Profile | 无 | high | S/R/P/T | C2/C5/C6 |
| 45 | `write_task` | body, parent?, priority?, recipient, references?, risk_level?, sender, subject, thread_key? | `Project.write_task` | 新建 inbox TASK | `CORE_MAPPING` | 与 create_task 同一幂等实现；稳定 object identity | `create_task`（语义别名） | critical | S/R/P/T | 历史名称保留，但不得维护第二套逻辑 |

## 3. 强制单列复核结论

| 工具/能力 | 真实结论 |
|---|---|
| 4 个 history 工具 | 当前是 v3.2 冷存储工具，不是 Base Core 第六生命周期；WP1 未选 history 权威模型前均 `LEGACY_V3_ONLY` |
| `finish_task` | 真实 `active→done`；不强制 REPORT，不含 authorization_ref；列为 v3 legacy |
| `archive_task` | 真实跨级；不检查 Branch REPORT/收敛 REVIEW/子任务/ISSUE；名称可映射 Core，行为不可直接兼容 |
| `mark_human_approved` | 原地改写旧 REVIEW；v4 必须改为追加事实 |
| `upgrade_fcop` | 执行包环境升级，可能随后影响工作区部署；是可选高风险 Toolkit，不属协议 |
| `redeploy_rules` | 覆盖规则副本并可归档；必须 Profile/ADMIN 显式授权 |
| GAL/governance | alert/event/summary 是 Optional Toolkit；不能取代正式 REVIEW/authorization |
| workspace 工具 | inspect/init/discovery/binding 属 Toolkit；runtime registry 不是 C1 真相 |
| relay/network | `websockets>=12.0` 当前为 MCP 必装依赖；4.0 候选应拆为可选 `fcop-mcp[relay]`，待 WP1/发行计划决定 |

## 4. 外部可见差异

| 环境 | 可见数量 | 额外/缺失 | 来源证据 | 官方 snapshot | 处理 |
|---|---:|---|---|---|---|
| FCoP canonical snapshot | 45 | 无 | `tests/test_fcop_mcp/snapshots/tool_surface.json` | 是 | 基线 |
| FCoP MCP server | 45 | 无 | `server.py` 注册链 + snapshot tests | 是 | 交叉验证 |
| CodeFlowMu 静态 catalog | 46 | 额外 `close_issue` | `D:\codeflowmu@21c1c8a.../codeflowmu-shell/src/fcop-mcp-catalog.ts` | 否 | `DOWNSTREAM_CATALOG_DRIFT`；只报告 |
| CodeFlowMu filter | 45 基线 | 无 canonical 增项 | `fcop-mcp-filter.ts` 明确上游返回 45，运行时按 allowlist 过滤 | 下游处理 | 不修改 |
| CodeFlowMu SDK | 45 基线 | 无 canonical 增项 | `sdk-factory.ts` 以 45 作为 admin/all-tools 总数 | 下游处理 | 不修改 |

通过只读脚本把 CodeFlowMu catalog 的顶层键与 FCoP snapshot 名称集合比较：`catalog_count=46`、`upstream_count=45`、`extra=[close_issue]`、`missing=[]`。CodeFlowMu HEAD 与远程 main 同为 `21c1c8a215e407687cce69011f9038861ff935eb`。

## 5. 完成状态

```text
CANONICAL_TOOL_COUNT: 45
SERVER_REGISTERED_COUNT: 45
DISPOSITION_COMPLETED: 45/45
DUPLICATE_TOOL_NAMES: 0
UNRESOLVED_DISPOSITIONS: 0
V4_BEHAVIOR_DECISIONS_DEFERRED_TO_WP1: YES
```
