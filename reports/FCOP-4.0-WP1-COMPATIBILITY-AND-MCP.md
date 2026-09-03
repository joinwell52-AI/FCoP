# FCoP 4.0 WP1 · 兼容性与 MCP 合同

- 状态：Candidate / Contract Only
- 基线：`68dbeb15f4e7f84e1d03f907be9fa66c2265843e`
- WP0 证据提交：`c259bebdad77122d24dc18a6dd3f8fe191e4042f`

## 1. 兼容总则

- v3 工作区继续按 v3 读取和写入；没有 `F4.2.1` 的 4.0 声明，不得执行 4.0 写入或静默迁移。
- 同名 MCP 工具必须先按 workspace version 分派。无法证明目标版本、Encoding、身份或安全语义时 Fail Closed，不得猜测或回落到另一版本写路径。
- `fcop` 是参考 Toolkit，`fcop-mcp` 是可选 Adapter；工具、资源和模板均不是 C1–C8 Core。
- 4.0 Branch 由普通 TASK 加 `branch_of` 表达，不新增强制专用工具。
- `finish_task` 与四个 history 工具属于 `LEGACY_V3_ONLY`；`close_issue` 是 CodeFlowMu 下游静态 catalog 漂移，不进入官方工具面。
- MCP 基础层是薄 stdio Adapter；联网 Relay 是可选扩展，候选包装名为 `fcop-mcp[relay]`，本 WP 不实施。

## 2. 官方 MCP 工具逐项映射（45/45）

表中“v3 旧语义”仅记录兼容输入，“4.0 候选语义”才是 4.0 workspace 的预期合同。所有 `v3/v4 分派` 行均要求显式 workspace version；不能安全分派时返回版本/Encoding 错误并保持磁盘不变。

| # | 工具 | v3 旧语义 | 4.0 候选语义 / 处置 | 适用工作区 | Fail Closed 行为 | 规范条款 |
|---:|---|---|---|---|---|---|
| 1 | `approve_task` | review→done，actor 自报 | T4；绑定当前 attempt、REPORT、acceptance REVIEW 与有效 authorization | v3/v4 分派 | 缺失/过期/复用/错绑定拒绝，无移动 | F4.4.2, F4.6.3, F4.7 |
| 2 | `archive_task` | 可跨多个阶段链式归档 | 仅 T7 done→archive；有 Branch 时验证 family convergence | v3/v4 分派 | 非 done、证据或授权不完整均拒绝 | F4.4.2–F4.4.3, F4.6.5–F4.6.8 |
| 3 | `archive_to_history` | archive TASK/REPORT 移入 history | 不得移动 4.0 权威 TASK；可选冷副本无 NOW 权力 | `LEGACY_V3_ONLY` | 4.0 权威移动返回 Legacy 错误 | F4.4.6, F4.11.2 |
| 4 | `bulk_archive_to_history` | 批量深归档 | 同上，不得批量改变 4.0 权威状态 | `LEGACY_V3_ONLY` | 4.0 写请求整体拒绝 | F4.4.6, F4.11.2 |
| 5 | `check_update` | 查询包版本/PyPI | 非规范更新提示，不改变协议事实 | Toolkit | 网络/版本不确定时报告未知，不写 workspace | F4.11.3, F4.11.5 |
| 6 | `claim_task` | inbox→active，actor 自报 | T2 并生成不可复用 attempt_id；原子记录 transition | v3/v4 分派 | 状态歧义、版本或提交不确定时拒绝 | F4.4.2, F4.6.1, F4.9 |
| 7 | `create_custom_team` | 初始化自定义 team/role | 只生成 Profile；不得定义 Core 角色或身份 | Toolkit/Profile | 未显式初始化授权或版本不明时拒绝 | F4.1.4, F4.2.3, F4.11.5 |
| 8 | `create_task` | 新建 inbox TASK；无 durable operation identity | 强制 operation_id/kind/digest；支持四关系与 Branch | v3/v4 分派 | 同键异摘要、关系非法或 Root 非 active 时拒绝 | F4.3, F4.5, F4.8 |
| 9 | `deploy_role_templates` | 部署/覆盖角色模板 | 仅显式 Profile 部署；不修改 Core 合同 | Toolkit/Profile | 缺授权、目标漂移或覆盖不安全时拒绝 | F4.1.4, F4.11.5 |
| 10 | `drop_suggestion` | 写 `.fcop/proposals/` | Optional observation；不是第五类 envelope | Optional Extension | 不得将结果当 TASK/REVIEW/authorization | F4.3.1, F4.11.3 |
| 11 | `fcop_audit` | 读取并可写 INSPECTION | 审计派生工具；只消费 Core 事实 | Toolkit | 事实歧义时显式报告，不替用户修复 | F4.9.3–F4.9.4, F4.11.3 |
| 12 | `fcop_check` | 工作区/Schema/drift 检查 | 4.0 conformance reader，不创造规范 | Toolkit | 规范/Schema/事实冲突时报错并阻断绿色结论 | F4.0.3, F4.12.3 |
| 13 | `fcop_create_alert` | 写 GAL alert | Optional/GAL，非四类业务 envelope | Optional Extension | 不得授予 transition 权限 | F4.3.1, F4.11.5 |
| 14 | `fcop_list_alerts` | 读取 GAL alerts | 只读派生视图 | Optional Extension | 不得将缺失/旧 alert 推断成 Core 事实 | F4.11.5 |
| 15 | `fcop_report` | 启动/状态/drift 报告 | Host convenience；workspace 真相仍来自声明与路径 | Toolkit | 读取冲突时报告不确定，不选择 NOW | F4.2, F4.4.1, F4.9.3 |
| 16 | `finish_task` | active→done，跳过 review | 4.0 Base 删除该边 | `LEGACY_V3_ONLY` / Deprecated | 4.0 返回 `LEGACY_TRANSITION_NOT_ALLOWED`，无副作用 | F4.4.4, F4.11.2 |
| 17 | `get_available_teams` | 枚举 bundled teams | Profile catalog，不进入 Core | Toolkit/Profile | 未知模板返回错误，不生成角色合同 | F4.1.4, F4.2.3 |
| 18 | `get_governance_summary` | 汇总治理事件 | Optional 派生摘要，不是授权源 | Optional Extension | 不得用摘要替代 REVIEW | F4.7, F4.11.5 |
| 19 | `get_team_status` | 扫描并格式化 team 状态 | 从 workspace 事实派生的 Profile 视图 | Toolkit/Profile | 重复 TASK/关系错误时标为歧义 | F4.2.3, F4.9.3 |
| 20 | `init_project` | 创建 workspace/team/rules | 仅在显式选择 4.0 时原子创建 C1 manifest；team 为 Profile | v3/v4 创建分派 | 不完整初始化、冲突 ID 或不支持 Encoding 时拒绝/可恢复 | F4.2, F4.9 |
| 21 | `init_solo` | 创建 solo workspace/rules | solo 仅 Profile；C1 身份不依赖角色码 | v3/v4 创建分派 | 同上，不静默采用默认版本 | F4.2, F4.11.1 |
| 22 | `inspect_task` | 只读单 TASK 校验 | 校验 envelope、唯一路径、关系、attempt 与 evidence | Toolkit | 多副本/强关系失败返回确定错误 | F4.3–F4.6, F4.9.3 |
| 23 | `list_governance_events` | 读取 governance log | Optional 派生事件；不替代 transition/REVIEW | Optional Extension | 事件缺失不得反推授权或 NOW | F4.4.5, F4.7, F4.11.5 |
| 24 | `list_history` | 列出 v3 history | 只读 Legacy history；不构成 4.0 第六生命周期 | `LEGACY_V3_ONLY` reader | 不从 history 选择 4.0 NOW | F4.4.6, F4.11.2 |
| 25 | `list_issues` | 查询 ISSUE | 查询正式 ISSUE envelope；状态非 Core | Toolkit | 非法 envelope 作为错误/无效项显式报告 | F4.3.2–F4.3.3 |
| 26 | `list_reports` | 查询 REPORT | 支持 subject/attempt/head 查询，不自行决定有效性 | Toolkit | 多 head 返回 `REPORT_HEAD_AMBIGUOUS` | F4.3.4, F4.6.2 |
| 27 | `list_reviews` | 查询 REVIEW | 支持 review_kind/subject/references/authorization 绑定 | Toolkit | 非法或歧义 REVIEW 不授予权限 | F4.3.5, F4.7 |
| 28 | `list_tasks` | 按 lifecycle 查询 TASK | 以五目录路径读取 NOW，并可按四关系查询 | Toolkit | 多权威副本返回 `STATE_AMBIGUOUS` | F4.4.1, F4.5, F4.9.3 |
| 29 | `list_workspaces` | 读取 Host registry | 仅发现 workspace；registry 不是 workspace identity | Toolkit/Runtime | registry 与 C1 冲突时以冲突停止，不重写 ID | F4.2, F4.11.5 |
| 30 | `mark_human_approved` | 原地修改既有 REVIEW | 只可追加新的 authorization REVIEW 并 references 旧事实 | v3/v4 分派；旧行为 Deprecated | 绝不改写旧 REVIEW；绑定不足则拒绝 | F4.3.3, F4.3.5, F4.7 |
| 31 | `new_workspace` | 创建目录、manifest、registry | 原子创建 C1 manifest；registry 可重建、非身份权威 | v3/v4 创建分派 | 路径/ID/版本冲突时拒绝并保留恢复证据 | F4.2, F4.9, F4.12.1 |
| 32 | `read_history_task` | 读取 v3 history TASK | 只读 Legacy 内容，不提升为 4.0 NOW | `LEGACY_V3_ONLY` reader | 不接受其作为 4.0 权威 lifecycle TASK | F4.4.6, F4.11.2 |
| 33 | `read_report` | 读取 REPORT | 读取 append-only REPORT 并暴露 attempt/head 元数据 | Toolkit | 非法/多 head 明确报错，不静默选取 | F4.3.3–F4.3.4, F4.6.2 |
| 34 | `read_review` | 读取 REVIEW | 读取 append-only REVIEW/authorization 事实 | Toolkit | 无效绑定不得被解释为授权 | F4.3.3, F4.3.5, F4.7 |
| 35 | `read_task` | 读取 TASK | 读取唯一权威路径 TASK；位置给出 NOW | Toolkit | 多副本返回 `STATE_AMBIGUOUS` | F4.4.1, F4.9.3 |
| 36 | `redeploy_rules` | 覆盖部署规则副本 | 显式 Profile/Toolkit 运维；不得暗改规范或 workspace 版本 | Toolkit/Profile | 未授权、版本错配或覆盖不安全时拒绝 | F4.0.3, F4.11.5, F4.12.3 |
| 37 | `reject_task` | review→active，actor 自报 | T5；有效 rejection/authorization，生成新 attempt | v3/v4 分派 | 错 attempt/过期/复用授权时拒绝 | F4.4.2, F4.6.1, F4.7 |
| 38 | `set_project_dir` | 改进程内当前项目 | Host binding；不能改变 C1 identity | Toolkit/Runtime | 目标无效/版本不支持时不绑定 | F4.2, F4.11.5 |
| 39 | `submit_task` | active→review，不强制 REPORT | T3；必须引用当前 attempt 唯一有效 REPORT | v3/v4 分派 | 缺 REPORT/旧 attempt/多 head 时拒绝 | F4.3.4, F4.4.2, F4.6.2 |
| 40 | `upgrade_fcop` | 修改 Python 环境 | Optional updater，协议工作区之外且需显式授权 | Optional Extension | 不得因升级自动迁移、重部署或改 workspace | F4.11.1, F4.11.5, F4.12.4 |
| 41 | `validate_team_config` | 校验 roles/leader | Profile validator，不定义 Core 角色表 | Toolkit/Profile | Profile 不完整时报错，不扩充 Core | F4.1.4, F4.2.3 |
| 42 | `write_issue` | 创建 ISSUE，当前缺统一 subject_ref | 创建 append-only ISSUE，subject_ref 必填且合法 | v3/v4 分派 | 关系/subject/workspace 错误时拒绝 | F4.3.2–F4.3.3, F4.5 |
| 43 | `write_report` | 创建 task_id REPORT | 创建 append-only REPORT，绑定 subject_ref/current attempt；replacement 成链 | v3/v4 分派 | 旧 attempt、非法 replacement 或多 head 时拒绝 | F4.3.3–F4.3.4, F4.6.2 |
| 44 | `write_review` | 创建通用 REVIEW | 创建 typed append-only REVIEW；授权资格由 Profile 判定 | v3/v4 分派 | kind/绑定/issuer 不可证时不能用于 gate | F4.3.5, F4.6.3, F4.7 |
| 45 | `write_task` | `create_task` 语义别名 | 与 `create_task` 共用同一幂等/关系实现，不维护第二状态机 | v3/v4 分派 | 与 #8 相同；别名不能绕过 gate | F4.5, F4.8, F4.9 |

计数：`MCP_TOOL_MAPPING: 45/45`。

## 3. 静态资源逐项映射（11/11）

| # | URI | WP0 类别 | 4.0 候选处置 | 规范条款 |
|---:|---|---|---|---|
| 1 | `fcop://config` | `PROFILE_RESOURCE` | 只投影 C1/Profile；不得成为另一份身份权威 | F4.2, F4.11.3 |
| 2 | `fcop://letter/en` | `TOOLKIT_RESOURCE` | 非规范使用说明，必须标示适用版本 | F4.11.3, F4.12.3 |
| 3 | `fcop://letter/zh` | `TOOLKIT_RESOURCE` | 同上 | F4.11.3, F4.12.3 |
| 4 | `fcop://prompt/install` | `TOOLKIT_RESOURCE` | 安装提示不授权初始化、升级或迁移 | F4.11.1, F4.12.4 |
| 5 | `fcop://prompt/install/en` | `TOOLKIT_RESOURCE` | 同上 | F4.11.1, F4.12.4 |
| 6 | `fcop://protocol` | `PROFILE_RESOURCE` | 解释性投影，不能覆盖 frozen Specification | F4.0.3, F4.12.3 |
| 7 | `fcop://rules` | `PROFILE_RESOURCE` | Profile 规则投影；固定角色/Host 规则不得进入 Core | F4.1.4, F4.2.3 |
| 8 | `fcop://spec` | `SPEC_SNAPSHOT` | 必须绑定明确规范版本；当前无版本 v1.1 URI 不得冒充 4.0 | F4.0.2–F4.0.3, F4.11.3 |
| 9 | `fcop://spec/en` | `SPEC_SNAPSHOT` | 同上；中英 snapshot 版本不一致时 Fail Closed | F4.0.2–F4.0.3, F4.11.3 |
| 10 | `fcop://status` | `TOOLKIT_RESOURCE` | 只读派生视图；不产生 NOW 或 authorization | F4.4.1, F4.7, F4.11.3 |
| 11 | `fcop://teams` | `PROFILE_RESOURCE` | Profile catalog；角色集/leader 不进入 Base Core | F4.1.4, F4.2.3 |

计数：`STATIC_RESOURCE_MAPPING: 11/11`。

## 4. Resource template 逐项映射（3/3）

| # | URI template | WP0 类别 | 4.0 候选处置 | 规范条款 |
|---:|---|---|---|---|
| 1 | `fcop://teams/{team}` | `PROFILE_RESOURCE` | 只读已注册 team Profile；未知 team 拒绝 | F4.1.4, F4.2.3 |
| 2 | `fcop://teams/{team}/{role}` | `PROFILE_RESOURCE` | 中文角色 Profile；不得定义 Core 授权表 | F4.2.3, F4.7.4 |
| 3 | `fcop://teams/{team}/{role}/en` | `PROFILE_RESOURCE` | 英文角色 Profile；与中文版本漂移时不得推导 Core 权限 | F4.0.2, F4.7.4 |

计数：`RESOURCE_TEMPLATE_MAPPING: 3/3`。

## 5. 下游额外项与包装边界

| 项目 | 数量 | 裁定 |
|---|---:|---|
| CodeFlowMu `close_issue` | 1/1 | 下游静态 catalog 漂移；不在 FCoP 45 工具 snapshot 中，明确排除，不修改 CodeFlowMu |
| `finish_task` | 1/1 | `LEGACY_V3_ONLY` / Deprecated；4.0 返回 `LEGACY_TRANSITION_NOT_ALLOWED` |
| History 工具 | 4/4 | `archive_to_history`、`bulk_archive_to_history`、`list_history`、`read_history_task` 均为 `LEGACY_V3_ONLY`；4.0 只允许 Legacy 只读/非权威副本 |
| Branch 专用工具 | 0 required | 不新增；使用 create TASK + `branch_of` |
| Relay | optional | Candidate 包装 `fcop-mcp[relay]`；不属于 Base MCP/Core，本 WP 不修改 packaging |

## 6. 兼容裁定

4.0 兼容策略是“显式版本分派 + 不静默迁移 + 失败关闭”，而不是让 4.0 合同迁就 v3 的跨边、原地改写、actor 自报或 history 权威移动。官方 MCP 计数保持 45；资源保持 11+3；下游额外 `close_issue` 保持排除。该裁定只冻结候选可观察语义，不授权实现、Schema、测试、包装、发布或 CodeFlowMu 修改。
