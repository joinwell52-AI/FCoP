---
document_role: ADMIN_CONTRACT_CLARIFICATION_AND_EXECUTION_TASKBOOK
title: FCoP 4.0 WP4B.1 T6 reopen_task MCP 映射与工具表面修正任务书
version: 1.0
status: AUTHORIZED_FOR_WP4B_RESUME_ONLY
execution_authorized: true
authorized_scope: WP4B_RESUME_ONLY
stop_code_resolved: MCP_T6_TOOL_MAPPING_UNDERDETERMINED
blocked_report_commit: 72e26fd214849922369e9135c8be0cb1fd260da8
resumes_taskbook_commit: b2453202686d08bd6584302072e0be814a059be4
parent_gate_commit: 982fcb24d9093e01c5ba4fdb87e710acd57e6d54
input_head: 72e26fd214849922369e9135c8be0cb1fd260da8
frozen_contract_commit: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
main_merge_authorized: false
release_authorized: false
wp4c_authorized: false
codeflowmu_change_authorized: false
---

# FCoP 4.0 WP4B.1：T6 `reopen_task` MCP 映射与工具表面修正任务书

## 0. ADMIN 裁决

ADMIN 接受 `72e26fd214849922369e9135c8be0cb1fd260da8` 所记录的阻断：冻结 FCoP 4.0 Core 已实现 T6，但 WP1 的 45 项历史 MCP disposition 没有为它指定公开 MCP 请求入口。

```yaml
BLOCKED_REPORT_ACCEPTED: true
STOP_CODE: MCP_T6_TOOL_MAPPING_UNDERDETERMINED
CORE_T6_IMPLEMENTED: true
MCP_T6_ENTRY_MISSING: true
```

现作最终裁决：

```yaml
T6_MCP_TOOL: reopen_task
T6_EDGE: done -> active
FCoP_4_CANONICAL_MCP_TOOLS: 46
NEW_FCoP_4_TOOL: reopen_task
close_issue_CANONICAL: false
claim_task_EXTENDED_TO_T6: false
reject_task_EXTENDED_TO_T6: false
```

本文件解决该阻断，并恢复原 WP4B 实施。除本文件以及 WP4B.0 已明确修正的条款外，原 WP4B 继续有效。

## 1. 为什么必须新增独立工具

真实生产代码 `src/fcop/v4/lifecycle.py` 已冻结以下 edge/tool 映射：

```text
inbox  -> active  : claim_task
active -> review  : submit_task
review -> done    : approve_task
review -> active  : reject_task
done   -> active  : reopen_task
done   -> archive : archive_task
```

所以：

- `claim_task` 只能表达 T2，不能根据 TASK 当前状态变成 T6；
- `reject_task` 只能表达 T5，不得通过隐藏状态推断变成 T6；
- `write_review` 只追加证据，不消费授权、不移动 TASK；
- `mark_human_approved` 只追加授权事实，不执行生命周期迁移；
- `finish_task` 在 v4 是被禁止的旧捷径；
- 通用 `transition` 工具会把底层生命周期细节和多种副作用重新暴露给 Agent，不采用。

新增一个单用途 `reopen_task`，比让旧工具根据状态或 selector 改变含义更小、更稳定，也与 Core transition event 中已经使用的 `tool: reopen_task` 完全一致。

## 2. 工具数量修正

### 2.1 历史与 4.0 表面分开计数

```yaml
FCoP_3_2_5_CANONICAL_TOOLS: 45
FCoP_4_0_CANONICAL_TOOLS: 46
ADDITIVE_DELTA: 1
ADDED_TOOL: reopen_task
REMOVED_TOOLS: 0
RENAMED_TOOLS: 0
```

WP0/WP1 的 `45/45` 报告继续作为 3.2.5 基线证据保留，不得篡改历史报告来假装当时已有 T6。

WP4B 必须新增一份 4.0 canonical disposition/snapshot，明确：

- 原 45 个名字全部保留；
- 第 46 项是 `reopen_task`；
- `close_issue` 仍是 CodeFlowMu 下游静态 catalog drift，不进入 FCoP；
- `reopen_task` 是 Core T6 的 MCP Adapter 映射，不是新 Core edge；
- 不通过删除一个 legacy 工具“腾位置”。

### 2.2 对原任务书的替换

原 WP4B 与 WP4B.0 中所有要求以下内容的条款：

```yaml
MCP_TOOLS: 45/45
TOOL_DISPOSITION: 45/45
canonical tool count unchanged: true
```

替换为：

```yaml
V3_BASELINE_TOOL_DISPOSITION: 45/45
V4_CANONICAL_MCP_TOOLS: 46/46
V4_ADDITIVE_TOOL: reopen_task 1/1
V4_REMOVED_TOOL_NAMES: 0
V4_RENAMED_TOOL_NAMES: 0
close_issue_PRESENT: false
```

## 3. `reopen_task` 固定公共请求合同

### 3.1 工具名与用途

```text
name: reopen_task
operation: consume T6 authorization and move exactly one TASK from done to active
```

一次调用只能请求 T6 一条边。不得附带创建 Branch、写 REPORT、归档、提交审查或执行下一轮工作的副作用。

### 3.2 显式参数

公开 MCP 参数固定为：

| 参数 | 类型 | 必填 | 含义 |
|---|---|---:|---|
| `task_id` | string | 是 | 当前唯一位于 `done` 的 TASK |
| `review_ref` | string | 是 | `review_kind: reopen`、`decision: approved` 的 T6 证据 REVIEW |
| `authorization_ref` | string | 是 | 独立、single-use、允许 `done -> active` 的 Authorization REVIEW |
| `profile_ref` | string | 是 | 已在可信 Project 初始化边界注册的 Profile 标识，必须与 Authorization 一致 |
| `actor` | string | 是 | 发起这次工具调用的审计主体；不是权限证明 |
| `lang` | string | 否 | 仅控制人类可读说明语言；不得影响业务结果，默认沿用 MCP 既有约定 |

禁止公开或接受：

- `from_stage`、`to_stage`、`tool` selector；它们由 `reopen_task` 固定为 `done`、`active`、`reopen_task`；
- `operation_id`；T6 响应丢失重试由已消费 Authorization 的稳定绑定处理；
- `internal_operation_id`；它只属于 Core 故障注入/恢复内部边界；
- `attempt_id`；Core 从当前 TASK 证明旧 attempt，并为 T6 生成新 attempt；
- `report_ref`；T6 不消费 REPORT；
- `family_digest`；冻结合同规定 T4–T6 不消费 family digest；
- caller 提供 evaluator、authorized/denied 结论、角色权限表或任意代码路径。

### 3.3 唯一调用映射

MCP Adapter 只能调用同一个已验收 `Project.transition()`：

```python
project.transition(
    task_id=task_id,
    from_stage="done",
    to_stage="active",
    tool="reopen_task",
    actor=actor,
    review_ref=review_ref,
    authorization_ref=authorization_ref,
    profile_ref=profile_ref,
)
```

上段是规范映射，不要求复制实现。Adapter 不得自行验证并替代 Core 的状态、Review、Authorization、Profile、摘要、单次消费、锁、receipt 或恢复判断。

## 4. T6 行为合同

成功必须同时满足：

1. TASK 在唯一 `done` 路径；
2. `review_ref` 是绑定该 TASK 与当前已接受 attempt 的合法 reopen REVIEW；
3. `authorization_ref` 是独立合法 Authorization REVIEW；
4. Authorization 绑定 T6、TASK、attempt、evidence digest 与 `profile_ref`；
5. `profile_ref` 已在可信初始化边界注册且 evaluator 返回 `AUTHORIZED`；
6. Authorization 未过期、未被其他 transition 消费；
7. Core 在 family linearization boundary 内只提交 `done -> active`；
8. 生成不可复用的新 `attempt_id`；
9. 旧 REPORT 不满足新 attempt；
10. Root 或 Branch 被 reopen 后，受影响的旧 convergence 失效；
11. transition event 记录 `tool: reopen_task`、authorization ref/digest 和新 attempt；
12. 响应丢失后，以完全相同的正式请求重试，返回已经提交的结果而不产生第二次 T6。

失败必须零业务写入，并原样投影 Core 稳定错误码。

## 5. v3 工作区行为

`reopen_task` 是 FCoP 4.0 新增 Adapter 能力。它可以出现在 fcop-mcp 4.x 的静态 tool list 中，但针对 v3 工作区调用时必须：

```yaml
RESULT: FAIL_CLOSED
ERROR_CODE: UNSUPPORTED_WORKSPACE_VERSION
BUSINESS_WRITES: 0
LIFECYCLE_MOVES: 0
REVIEWS_APPENDED: 0
```

不得把它回落为 v3 `claim_task`、`reject_task`、`finish_task` 或多边归档调用。原 45 个 v3 工具的既有行为不得因新增第 46 个名字而改变。

CodeFlowMu 当前固定使用 `fcop==3.2.5`、`fcop-mcp==3.2.5`，本次不修改其静态 catalog、Runtime 或安装依赖。

## 6. 必须增加的测试

### 6.1 Surface

- v3.2.5 历史 snapshot 仍证明 45 项；
- FCoP 4.0 canonical snapshot 精确 46 项；
- 差集精确为 `reopen_task`；
- 原 45 项无删除、无重命名；
- `close_issue` 不存在；
- `reopen_task` 参数表与本任务书一致；
- 不存在通用 `transition` MCP tool。

### 6.2 正常 T6

- Root TASK 合法 done→active；
- Branch TASK 合法 done→active；
- 新 attempt 与旧 attempt 不同；
- 旧 REPORT 不能通过新一轮 T3；
- reopen 后旧 convergence 失效；
- event 中 tool、授权和 attempt 字段正确；
- MCP 返回值与直接 Project 结果语义一致。

### 6.3 授权与证据失败

- 缺 `review_ref`；
- reopen REVIEW 类型/decision/subject/attempt 错误；
- 缺 `authorization_ref`；
- Authorization transition、subject、attempt、evidence digest、profile 错绑定；
- Authorization 过期、重复使用；
- Profile registry 为空；
- evaluator 返回 DENIED 或 UNKNOWN；
- caller 通过参数/文档/manifest 夹带权限；
- `actor` 冒充 ADMIN/PM/QA；
- 所有失败验证零移动、零新 attempt、零新 transition。

### 6.4 重试、恢复与竞态

- T6 成功响应丢失后 exact retry 返回既有结果；
- retry 不生成第二个 attempt/event/receipt；
- 同一 Authorization 被不同 TASK 或 transition 使用返回 `AUTHORIZATION_REUSED`；
- T6 与 Root archive/Branch create 的竞态继续由同一 family boundary 串行化；
- 崩溃点使用既有 Core receipt/recovery，不在 MCP 建第二套恢复状态。

### 6.5 非法工具复用

- `claim_task(done_task)` 仍为 `INVALID_TRANSITION`；
- `reject_task(done_task)` 不执行 T6；
- `write_review` 不移动 TASK；
- `mark_human_approved` 不移动 TASK；
- `finish_task` 在 v4 仍返回 `LEGACY_TRANSITION_NOT_ALLOWED`。

## 7. 文档与机器表面更新

WP4B 完成时必须同步：

- FCoP 4.0 MCP canonical tool snapshot：46 项；
- WP4B 45+1 disposition 结果；
- MCP README 中 `reopen_task` 用法；
- `[Unreleased]` 中记录 additive MCP tool；
- 安装后 list-tools 验证结果；
- clean wheel/sdist 中同样注册 46 项；
- 中英文用户说明若已有工具清单，必须同步且语义一致。

不得回写 WP0/WP1 历史报告的原始 45/45 统计；新的 WP4B 报告负责记录从 45 到 46 的正式演进。

## 8. WP4B.0 与其他 WP4B 工作继续执行

以下既有要求继续有效：

- WP4B.0 对三个 Profile Resource Templates 的裁决；
- WP4B.0 对 FastMCP `websockets` 传递依赖和 Relay 能力边界的裁决；
- 单一 v3/v4 workspace router；
- 11 static resources / 3 read-only Profile templates；
- v4 操作只委托 `Project`；
- package compatibility Fail Closed；
- Base stdio 不自动启用 Relay；
- 冻结 119/119 v4 conformance；
- 全量 fcop/MCP/打包/跨平台 CI；
- GitHub 两提交与远端 SHA-256 交付；
- 不修改 CodeFlowMu、main，不发布，不进入 WP4C。

## 9. 允许修改范围

沿用原 WP4B 和 WP4B.0 的允许范围，并明确允许：

- 新增 `reopen_task` MCP handler；
- 增加它所需的向后兼容 Adapter 参数/测试/文档；
- 将 FCoP 4.0 MCP snapshot 从 45 更新为 46；
- 新增 45+1 disposition 结果；
- 更新 Draft PR #15 的标题与说明，删除“当前仍被 T6 mapping 阻断”的陈旧状态。

不允许修改冻结 Core spec、Schema、60 个冻结 Test ID 或已验收的 `Project.transition()` T6 语义。

## 10. 硬停止条件

除既有停止条件外，出现以下任一项立即停止：

- 必须改动 Core T6 才能实现 MCP 映射；
- `reopen_task` 需要第二套授权、锁、receipt 或恢复；
- 必须让 reopen REVIEW 自己兼任 Authorization 才能通过；
- 必须暴露 `internal_operation_id`、caller evaluator 或通用 transition selector；
- 第 46 项不是 `reopen_task` 或意外加入 `close_issue`；
- 原 45 个工具出现删除/重命名；
- v3 调用产生任何 T6 副作用；
- GitHub 最终 CI 非绿。

阻断时只更新阻断报告，`REQUESTED_GATE: NONE`。

## 11. 完成回执修正

最终 WP4B 回执必须使用：

```yaml
WP4B_STATUS: COMPLETE | BLOCKED
WP4B_0_DECISION_APPLIED: true
WP4B_1_DECISION_APPLIED: true

T6_MCP_TOOL: reopen_task
T6_MCP_MAPPING: PASS | FAIL
T6_EXPLICIT_PARAMETERS: 6/6
T6_PROJECT_DELEGATION: PASS | FAIL
T6_EXACT_RETRY: PASS | FAIL
T6_NEW_ATTEMPT: PASS | FAIL
T6_OLD_REPORT_REJECTED: PASS | FAIL
T6_CONVERGENCE_INVALIDATION: PASS | FAIL
T6_CALLER_AUTHORITY_SMUGGLING: REJECTED | FAIL

V3_BASELINE_TOOL_DISPOSITION: 45/45
V4_CANONICAL_MCP_TOOLS: 46/46
V4_ADDITIVE_TOOL: reopen_task 1/1
V4_REMOVED_TOOL_NAMES: 0
V4_RENAMED_TOOL_NAMES: 0
close_issue_PRESENT: false

STATIC_RESOURCES: 11/11
RESOURCE_TEMPLATES: 3/3 READ_ONLY_PROFILE_RESOURCE
V4_CONFORMANCE: 119/119
UNEXPECTED_FAILURES: 0

MAIN_MODIFIED: false
CODEFLOWMU_FILES_MODIFIED: 0
RELEASE_CREATED: false
WP4C_STARTED: false
REQUESTED_GATE: WP4B_MCP_ADAPTER_ACCEPTED | NONE
```

成功后必须停止，不得自行签署 Gate。

## 12. 本任务书不授权

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
