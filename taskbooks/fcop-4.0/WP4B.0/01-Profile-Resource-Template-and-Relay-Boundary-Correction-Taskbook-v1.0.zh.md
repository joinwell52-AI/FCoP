---
document_role: ADMIN_CONTRACT_CLARIFICATION_AND_EXECUTION_TASKBOOK
title: FCoP 4.0 WP4B.0 Profile Resource Template 与 Relay 依赖边界修正任务书
version: 1.0
status: AUTHORIZED_FOR_WP4B_RESUME_ONLY
execution_authorized: true
authorized_scope: WP4B_RESUME_ONLY
blocked_report_commit: 9558a267333f245e5d4aa8c32aee4d1a90210639
resumes_taskbook_commit: 245d914e1f0aff48a19d8f0ba8432e6b4f008b68
parent_gate_commit: 982fcb24d9093e01c5ba4fdb87e710acd57e6d54
input_head: 9558a267333f245e5d4aa8c32aee4d1a90210639
frozen_contract_commit: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
main_merge_authorized: false
release_authorized: false
wp4c_authorized: false
codeflowmu_change_authorized: false
---

# FCoP 4.0 WP4B.0：Profile Resource Template 与 Relay 依赖边界修正任务书

## 0. ADMIN 裁决

ADMIN 接受 `reports/FCOP-4.0-WP4B-BLOCKED.md` 的停止行为与证据：

```yaml
BLOCKED_REPORT_ACCEPTED: true
STOP_CODE: MCP_TEMPLATE_CONTRACT_UNDERDETERMINED
BLOCKED_HEAD: 9558a267333f245e5d4aa8c32aee4d1a90210639
IMPLEMENTATION_BEFORE_STOP: false
```

阻断来自原 WP4B 任务书，而不是冻结 FCoP 4.0 Core：原任务书错误地要求三个只读 Team/Role Profile resource templates 生成 TASK、REPORT、ISSUE 或 REVIEW 业务信封；同时把“FCoP Relay 是可选能力”错误等同为“基础安装环境物理上不得出现 websockets 包”。

本文件对这两处歧义作最终裁决，并恢复原 WP4B 的实施授权。除本文件明确替换的条款外，原 WP4B 任务书继续有效。

```yaml
WP4B_RESUME_AUTHORIZED: true
AUTHORIZED_SCOPE: WP4B_RESUME_ONLY
START_FROM: 9558a267333f245e5d4aa8c32aee4d1a90210639
REQUESTED_GATE_ON_SUCCESS: WP4B_MCP_ADAPTER_ACCEPTED
```

## 1. 权威输入

- 原 WP4B 任务书：`taskbooks/fcop-4.0/WP4B/01-MCP-Thin-Adapter-and-Version-Routing-Taskbook-v1.0.zh.md`
- 原任务书提交：`245d914e1f0aff48a19d8f0ba8432e6b4f008b68`
- 阻断报告：`reports/FCOP-4.0-WP4B-BLOCKED.md`
- 阻断提交：`9558a267333f245e5d4aa8c32aee4d1a90210639`
- WP1 兼容合同：`reports/FCOP-4.0-WP1-COMPATIBILITY-AND-MCP.md`
- WP0 资源处置：`reports/MCP-RESOURCE-DISPOSITION-4.0.md`
- 冻结合同：`aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6`

如原 WP4B 与本文件冲突，以本文件为准；如本文件与冻结合同冲突，立即停止，不得修改冻结合同。

## 2. 裁决一：三个 Resource Templates 仍是只读 Profile 文档

### 2.1 固定合同

以下三个 canonical URI template 保持现有身份、参数和输出类别：

| URI template | 输入 | 输出 | 4.0 分类 |
|---|---|---|---|
| `fcop://teams/{team}` | `team` | 已注册 Team Profile 的只读 README | `PROFILE_RESOURCE` |
| `fcop://teams/{team}/{role}` | `team`, `role` | 已注册角色的中文只读 Profile 文档 | `PROFILE_RESOURCE` |
| `fcop://teams/{team}/{role}/en` | `team`, `role` | 已注册角色的英文只读 Profile 文档 | `PROFILE_RESOURCE` |

它们不是业务信封模板，不创建、渲染或提交 TASK、REPORT、ISSUE、REVIEW，也不生成 `operation_id`、attempt、relation、evidence 或 authorization。

### 2.2 Profile 文档中的 `version`

现有 Profile 文档中的 `version: 1` 是 Profile 文档自身的格式/内容版本，不是 FCoP workspace protocol version。不得据此把工作区判断为 v1、v3 或 v4。

WP4B 不重写这些 Profile 文档，不把它们伪装成 FCoP 4.0 规则包。Profile 文档的模块化重写、Host 投影与采用机制属于 WP4C。

### 2.3 版本路由例外

原 WP4B 对“所有 tools/resources/templates 都必须按 workspace version 生成不同内容”的表述，在这三个 template 上撤销。

理由：它们是注册表内的只读 Profile catalog 文档，不是 workspace NOW、Core Schema、协议规范或授权事实。它们可以在未绑定业务工作区时被读取，但必须满足：

- 不把 Profile `version` 当 protocol version；
- 不把 team/role 文档当作 Core 身份或授权；
- 不因为读取文档而注册 evaluator；
- 不执行文档中的代码、路径或命令；
- 未知 team/role 明确失败，不回落到另一个模板；
- team/role 参数不得形成任意文件路径读取；
- 返回内容不得声称自身是冻结 FCoP 4.0 Specification。

### 2.4 Profile 与 Authorization 的隔离

读取上述资源永远不等于采用 Profile。T4–T7 仍只信任 MCP server/Project 在可信初始化边界预先注册的 evaluator。

以下攻击必须有真实生产入口测试：

- 调用 template 后再提交自报 `profile_ref`；
- 把返回文档写入 REVIEW 并声称获得授权；
- 用 `team`/`role` 参数夹带 evaluator 名、路径或代码；
- 用 Profile 文档里的 leader/role 绕过空可信 registry；
- 将 Profile 文档 `version: 1` 解释成 workspace version。

以上均必须拒绝或保持无授权效果。

## 3. 裁决二：业务信封合同由 MCP Tools 承担

原 WP4B 第 5.3 节与第 8.4 节中下列要求撤销：

```text
templates 必须按 workspace version 生成兼容信封
v4 template 不得产生旧 relation/version、缺失 operation_id 或可变 REVIEW
3 个 templates 分别生成 v3/v4 合法业务信封形状
```

替换为：

- `create_task` / `write_task` 验证并传递 TASK v3/v4 输入；
- `write_report` 验证并传递 REPORT v3/v4 输入；
- `write_issue` 验证并传递 ISSUE v3/v4 输入；
- `write_review` 验证并传递 REVIEW/Authorization v3/v4 输入；
- 生命周期 tools 只传递正式引用、摘要与授权材料给 `Project`；
- MCP 不在 Profile templates 中提供第二条业务信封生成路径。

业务信封输出必须由真实 `Project` 写入后返回的事实决定，不得仅靠 MCP 示例文本宣称符合 Schema。

## 4. 三个 Templates 的 WP4B 验收测试

WP4B 对 resource templates 的完成标准固定为：

```yaml
RESOURCE_TEMPLATE_COUNT: 3/3
RESOURCE_TEMPLATE_CLASSIFICATION: PROFILE_RESOURCE 3/3
READ_ONLY: 3/3
KNOWN_TEAM_ROLE_READS: PASS
UNKNOWN_TEAM_ROLE_FAILS_EXPLICITLY: PASS
PATH_TRAVERSAL: REJECTED
WORKSPACE_VERSION_INFERENCE: REJECTED
AUTHORIZATION_EFFECT: NONE
EVALUATOR_REGISTRATION_EFFECT: NONE
BUSINESS_ENVELOPE_GENERATION: NOT_APPLICABLE
```

可以更新 MCP descriptor/docstring/snapshot，以明确 `PROFILE_RESOURCE` 和非授权性质；除非测试证明现有正文会冒充 4.0 Specification，否则不得为了 WP4B 大规模改写 Team/Role 内容。

## 5. 裁决三：Relay 可选性是能力边界，不是环境纯度

### 5.1 已确认事实

当前 `fcop-mcp` 依赖 `fastmcp>=3.2.0`。阻断报告已经证明 FastMCP 3.2.0/3.2.4 的发行元数据把 `websockets` 列为传递依赖。因此，仅移动 FCoP 自己的直接依赖，不能保证 clean environment 中完全不存在 `websockets` distribution。

WP4B 不得为了制造“环境无 websockets”而：

- `--no-deps` 安装 FastMCP；
- 安装后卸载其声明依赖；
- 篡改上游 wheel metadata；
- fork/vendor FastMCP；
- 仅为此目标降级、替换 MCP 框架；
- 把传递依赖存在错误宣称为 FCoP Relay 已启用。

### 5.2 固定边界

FCoP 的可选 Relay 定义为：

- base CLI 默认只启动 stdio；
- base 启动不读取 Relay URL、不建立 websocket 连接；
- 不因环境中存在 `websockets` 就注册、启用或自动运行 Relay；
- Relay 必须通过显式入口/配置启用；
- FCoP 自己直接用于 Relay 的依赖和使用说明归入 `fcop-mcp[relay]`；
- Relay 导入与连接代码不得进入普通 tool/resource 调用路径；
- stdio 与 Relay 共用同一个 MCP Adapter/Core 调用面，不复制业务逻辑。

`websockets` 可能作为 FastMCP 的传递依赖存在，这不改变上述能力边界。

### 5.3 替换验收项

撤销原 WP4B 的：

```yaml
BASE_STDIO_WITHOUT_WEBSOCKETS: PASS
```

替换为：

```yaml
FCOP_DIRECT_BASE_RELAY_DEPENDENCY: ABSENT
FASTMCP_TRANSITIVE_WEBSOCKETS: RECORDED_IF_PRESENT
BASE_STDIO_NO_RELAY_ACTIVATION: PASS
BASE_STDIO_NO_NETWORK_CONNECT: PASS
RELAY_REQUIRES_EXPLICIT_ENABLEMENT: PASS
RELAY_OPTIONAL_EXTRA_METADATA: PASS
STDIO_WITH_TRANSITIVE_WEBSOCKETS_PRESENT: PASS
```

### 5.4 必须测试

- 检查 `fcop-mcp` 自身的 direct dependency metadata；
- 检查 FastMCP 的 resolved dependency tree并如实报告；
- base CLI 启动只进入 stdio；
- 未配置 Relay 时不访问网络、不读取 Relay endpoint；
- 环境即使已经安装 websockets，也不会自动启用 Relay；
- 显式 Relay 入口在正确 extra/config 下工作；
- Relay 缺少其专属依赖时给出清晰错误，不影响 stdio；
- 不使用网络成功代替协议行为测试。

## 6. 原 WP4B 继续有效的范围

以下要求不变：

- 单一 v3/v4 workspace 路由边界；
- v3 3.2.5 行为兼容；
- v4 写操作委托同一 `Project` 实现；
- 45 tools / 11 static resources / 3 templates 名称与数量不漂移；
- 不增加 `close_issue`；
- `finish_task` 与四个 history 工具按 WP1 disposition；
- `fcop://spec[/en]` 不得继续把 v1.1 冒充 current v3/v4；
- `fcop://rules`、`fcop://protocol` 不得把 3.x 内容冒充 v4；
- caller 不得夹带 evaluator/authority；
- package compatibility Fail Closed；
- Core 稳定错误码可观察；
- 不增加数据库、后台服务、第二状态机、第二权威 Store；
- CodeFlowMu 只读 shadow，不修改、不升级、不迁移；
- GitHub Draft PR、两提交交付、远端回读与 CI 全绿；
- 完成后停止请求 `WP4B_MCP_ADAPTER_ACCEPTED`。

## 7. 实施顺序

1. 从 `9558a267333f245e5d4aa8c32aee4d1a90210639` 建立/恢复独立 WP4B worktree。
2. 先增加本文件第 4、5 节的合同测试。
3. 完成单一 workspace/version router。
4. 完成 45 tools 的声明式 disposition 与 v3/v4 delegation。
5. 完成 11 resources 的版本与权威边界。
6. 保留三个 Profile templates，完成非授权/路径安全测试。
7. 完成 stdio/Relay 能力分层与 dependency metadata。
8. 完成版本组合、错误投影、clean wheel 与跨平台测试。
9. 生成原 WP4B 要求的五份报告与最终 Manifest。
10. 更新 Draft PR #15，远端回读并等待全部 CI。
11. 全绿后停止并请求 Gate；任何阻断只报告，不继续 WP4C。

## 8. 允许修改范围

沿用原 WP4B 允许范围。另明确允许：

- 更新原 WP4B 报告以记录本裁决；
- 更新 MCP resource template 描述与相应 snapshot/test；
- 更新 packaging metadata 以表达 base/relay 能力边界；
- 在 `[Unreleased]` 记录上述适配变化。

禁止修改冻结 spec、v4 Schema、60 个冻结 Test ID、CodeFlowMu、main 与发布配置。

## 9. 硬停止条件

除原 WP4B 第 13 节外，增加：

- 必须把 Profile template 改成业务信封生成器才能继续；
- 必须信任 Profile 文档才可通过 T4–T7；
- 必须 fork/patch FastMCP 才能声称 Relay 可选；
- 只能通过隐藏网络连接完成 stdio 测试；
- 传递依赖与 direct dependency 无法在报告中区分；
- 新增未获授权的第四个 template 或修改 canonical URI。

遇到阻断仍只提交阻断报告，`REQUESTED_GATE: NONE`。

## 10. 完成与回执修正

原 WP4B 完成标准中的：

```yaml
BASE_STDIO_WITHOUT_WEBSOCKETS: PASS
```

永久替换为：

```yaml
PROFILE_RESOURCE_TEMPLATES: 3/3 READ_ONLY
BUSINESS_ENVELOPE_TOOLS: CONTRACT_ALIGNED
FCOP_DIRECT_BASE_RELAY_DEPENDENCY: ABSENT
FASTMCP_TRANSITIVE_WEBSOCKETS: RECORDED_IF_PRESENT
BASE_STDIO_NO_RELAY_ACTIVATION: PASS
BASE_STDIO_NO_NETWORK_CONNECT: PASS
RELAY_REQUIRES_EXPLICIT_ENABLEMENT: PASS
RELAY_OPTIONAL_EXTRA_METADATA: PASS
```

最终回执必须增加：

```yaml
WP4B_STATUS: COMPLETE | BLOCKED
WP4B_0_DECISION_APPLIED: true
BLOCKED_INPUT_HEAD: 9558a267333f245e5d4aa8c32aee4d1a90210639
RESOURCE_TEMPLATE_COUNT: 3/3
RESOURCE_TEMPLATE_CLASSIFICATION: PROFILE_RESOURCE 3/3
RESOURCE_TEMPLATE_AUTHORIZATION_EFFECT: NONE
BUSINESS_ENVELOPE_GENERATION_BY_TEMPLATES: false
BUSINESS_ENVELOPE_TOOLS: CONTRACT_ALIGNED | FAIL
FCOP_DIRECT_BASE_RELAY_DEPENDENCY: ABSENT | PRESENT
FASTMCP_TRANSITIVE_WEBSOCKETS: RECORDED_IF_PRESENT | NOT_PRESENT
BASE_STDIO_NO_RELAY_ACTIVATION: PASS | FAIL
BASE_STDIO_NO_NETWORK_CONNECT: PASS | FAIL
RELAY_REQUIRES_EXPLICIT_ENABLEMENT: PASS | FAIL
RELAY_OPTIONAL_EXTRA_METADATA: PASS | FAIL
```

成功时唯一请求：

```yaml
REQUESTED_GATE: WP4B_MCP_ADAPTER_ACCEPTED
WP4C_STARTED: false
MAIN_MODIFIED: false
RELEASE_CREATED: false
CODEFLOWMU_FILES_MODIFIED: 0
```

## 11. 本任务书不授权

```yaml
WP4C_AUTHORIZED: false
WP4D_AUTHORIZED: false
MAIN_MERGE_AUTHORIZED: false
RELEASE_AUTHORIZED: false
PYPI_PUBLISH_AUTHORIZED: false
GITHUB_RELEASE_AUTHORIZED: false
CODEFLOWMU_CHANGE_AUTHORIZED: false
WORKSPACE_MIGRATION_AUTHORIZED: false
```
