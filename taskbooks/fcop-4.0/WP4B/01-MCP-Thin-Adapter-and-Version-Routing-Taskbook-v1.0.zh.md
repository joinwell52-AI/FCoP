---
document_role: EXECUTION_TASKBOOK
title: FCoP 4.0 WP4B MCP 薄适配、版本路由与分发边界任务书
version: 1.0
status: AUTHORIZED_FOR_WP4B_ONLY
execution_authorized: true
authorized_scope: WP4B_ONLY
parent_gate: WP4A_MACHINE_CONTRACT_ACCEPTED
parent_gate_commit: 982fcb24d9093e01c5ba4fdb87e710acd57e6d54
input_head: 982fcb24d9093e01c5ba4fdb87e710acd57e6d54
frozen_contract_commit: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
main_merge_authorized: false
release_authorized: false
wp4c_authorized: false
codeflowmu_change_authorized: false
---

# FCoP 4.0 WP4B：MCP 薄适配、版本路由与分发边界任务书

## 0. ADMIN 授权

本文件是 WP4B 唯一执行入口。ADMIN 已签署 `WP4A_MACHINE_CONTRACT_ACCEPTED`，现仅授权执行 WP4B。

```yaml
GATE_RECEIVED: WP4A_MACHINE_CONTRACT_ACCEPTED
AUTHORIZED_SCOPE: WP4B_ONLY
START_POINT: 982fcb24d9093e01c5ba4fdb87e710acd57e6d54
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
```

本授权不允许进入 WP4C、WP4D，不允许修改或合并 `main`，不允许发布 PyPI/GitHub Release，不允许修改 CodeFlowMu。

## 1. 目标

把现有 `fcop-mcp` 收敛为 FCoP Python 公共能力之上的薄 MCP Adapter，使第三方只安装 `fcop` 与 `fcop-mcp` 就能通过 MCP 使用对应版本的 FCoP 工作区。

WP4B 必须同时成立：

1. 一个权威边界识别工作区是 v3 还是 v4；
2. v3 工作区保持 3.2.5 兼容行为；
3. v4 工作区只调用已验收的 `Project` v4 实现；
4. 未知、缺失、冲突或不可解析版本在写入前 Fail Closed；
5. MCP 仍为 45 个 canonical tools、11 个 static resources、3 个 templates；
6. `websockets` 不再是基础 stdio 安装的强制依赖；
7. MCP 不复制生命周期、授权、幂等、并发、恢复或 Schema 判断；
8. 不引入数据库、后台进程、watcher、timer、第二权威 Store 或第二状态机。

## 2. 架构底线

### 2.1 唯一权威关系

```text
MCP request
  -> workspace/version routing
  -> argument adaptation
  -> fcop.Project public operation
  -> result/error projection
```

MCP 只允许完成识别、校验输入形状、调用与投影。以下行为禁止在 MCP 重新实现：

- TASK 生命周期迁移；
- T1–T7 Gate；
- Authorization 可信判断；
- operation_id 幂等与 request digest；
- family lock、family digest 与 Branch 汇合；
- crash recovery 与 receipt 选择；
- 正式文件 Schema 的第二套解释器。

### 2.2 文件原生原则

工作区文件仍是协议事实；MCP 不保存隐藏生命周期状态，不建立数据库或内存账本作为事实源。允许的进程内对象只限请求适配、只读缓存和启动时不可变配置，进程重启后不得改变协议结论。

### 2.3 Profile 信任边界

调用者不得通过 tool 参数、TASK、REPORT、REVIEW、manifest、环境文本或 workspace 内容夹带 evaluator、角色权力或 `AUTHORIZED` 结论。

允许提供一个最小的启动初始化注入缝：

- Profile evaluator 只能在创建 MCP server / Project factory 时注册；
- 注册表在 server 启动后不可由 tool 修改；
- registry 默认为空；
- 空 registry 下涉及 T4–T7 的 v4 操作必须由 Core 返回 `AUTHORIZATION_PROFILE_UNAVAILABLE`；
- WP4B 不实现任何产品 Profile，不自动发现 workspace 内 Python 代码，不动态执行用户文件；
- CodeFlowMu Profile 不得进入本仓库通用 Adapter。

## 3. 固定输入与事实源

执行前必须读取并固定：

- `spec/fcop-4.0-spec.md`
- `spec/fcop-4.0-spec.zh.md`
- `reports/MCP-TOOL-DISPOSITION-4.0.md`
- `reports/MCP-RESOURCE-DISPOSITION-4.0.md`
- `reports/FCOP-4.0-WP1-COMPATIBILITY-AND-MCP.md`
- `taskbooks/fcop-4.0/WP4/00-Public-Contract-Adapters-and-Distribution-Master-Taskbook-v1.0.zh.md`
- WP4A Gate：`reviews/fcop-4.0/gates/WP4A-MACHINE-CONTRACT-ACCEPTED.md`

事实优先级：

```text
冻结 FCoP 4.0 合同
> 已验收 WP3E.1/WP4A 生产行为与机器合同
> WP0/WP1 disposition
> WP4 Master Taskbook
> 本任务书
> 历史 3.x 文档
```

如本任务书与冻结合同冲突，停止并报告，不得自行修改冻结合同。

## 4. 工作区与 Git 规则

1. 不在原 `D:\FCoP` 脏现场开发。
2. 从固定 `input_head` 新建独立 worktree。
3. 建议分支：`review/fcop-4.0-wp4b-mcp-adapter`。
4. 禁止 force-push，禁止 rebase 已交付 review 历史。
5. 若输入提交不可达、父链不一致或固定文件 SHA 不匹配，停止为 `INPUT_REF_MISMATCH`。
6. 中文 Markdown 不得使用 PowerShell 改写；使用 UTF-8/LF 安全的编辑方式。

## 5. WP4B 实施范围

### 5.1 单一版本路由边界

建立一个可单测的内部版本路由模块或等价单一边界。所有 tools/resources/templates 必须通过该边界取得：

```yaml
workspace_path: normalized absolute path
declared_protocol: v3 | v4
project: correctly initialized Project
capabilities: immutable route policy
```

要求：

- 只能读取 FCoP 已定义的工作区身份/manifest；
- 不得根据目录形状、已有文件数量、调用参数或失败重试猜版本；
- 明确 v4 后，不得因 v4 调用失败回退 v3；
- v3 工作区仍走既有 v3 行为；
- v4 工作区走 WP3A–WP3E.1 已验收的公共实现；
- unknown/missing/ambiguous/unsupported 在任何正式写入前失败；
- 每次重新绑定工作区必须重新识别；不得沿用上一个工作区版本。

禁止在 45 个 tool handler 中散落 45 份版本判断。版本判定和 disposition 必须分别只有一个权威实现。

### 5.2 45 个 canonical tools

保持 canonical tool 名称集合及数量：`45/45`。

- 不新增 `close_issue`；它是 CodeFlowMu 静态 catalog drift，不是 FCoP canonical tool。
- 不为了 Branch 新增强制 MCP tool；v4 Branch 继续通过普通 TASK 创建入口和 `branch_of` 表达。
- `reports/MCP-TOOL-DISPOSITION-4.0.md` 的 45 项必须全部进入一张声明式 route/disposition 表，并有 45/45 覆盖测试。
- 为 v4 增加必要参数时，只能做向后兼容的可选参数扩展；v4 路由在运行时强制其合同要求，v3 调用保持原签名语义。
- tool schema 发生预期变化时，更新 canonical snapshot 和 `[Unreleased]`，但 tool 名不得漂移。

#### v4 Core 写入口

下列能力必须调用 `Project` 的真实公共操作，不得复制实现：

- 创建 TASK、REPORT、ISSUE、REVIEW；
- claim、submit、approve、reject、archive；
- 重开与授权操作；
- family digest、收敛、恢复和幂等路径。

v4 请求所需的 `operation_id`、attempt、evidence、authorization、profile、family digest 等字段，必须按冻结 Schema 与 Project 公共 API 传递；不得由 MCP 伪造默认授权或补写证据。

#### v4 Legacy 拒绝

- `finish_task` 在 v4 工作区返回 `LEGACY_TRANSITION_NOT_ALLOWED`，零写入；
- 4 个 history/deep-archive 工具在 v4 工作区拒绝，零写入；
- v4 `archive_task` 只能请求 `done -> archive`，并由 Project 验证 T7；
- `mark_human_approved` 不得原地改写旧 REVIEW，只能调用追加事实的 Project 路径；
- 所有上述工具在 v3 工作区保持 3.2.5 兼容行为。

### 5.3 11 个 static resources 与 3 个 templates

保持 canonical surface：`11/11 + 3/3`，但每一项必须有明确版本策略和覆盖测试。

#### `fcop://spec`

- 不得继续把 v1.1 或任意旧规范冒充当前 v3/v4 规范；
- 为 MCP wheel 分发 v3 与冻结 v4 规范的只读投影，或采用等价的可复现打包方式；
- 投影必须有字节/哈希 parity 测试，根 `spec/` 文件仍是权威源；
- 未绑定工作区或版本未知时不得猜测返回哪个 current spec；
- unversioned URI 的响应必须依据已绑定工作区版本，并明确版本与来源提交。

#### `fcop://rules` 与 `fcop://protocol`

WP4C 尚未完成，不得把 3.x 大规则包标成 FCoP 4.0 当前规则。v3 可继续返回 v3 内容；v4 必须明确返回“4.0 规则投影尚未由 WP4C 交付”的类型化不可用结果，不能 silent fallback。

#### 其他资源与 templates

- config/status 只允许为文件事实的派生快照，不得成为 authority；
- teams/roles 等 Profile 内容不得被 Core/MCP 当作授权依据；
- templates 必须按 workspace version 生成兼容信封；
- v4 template 不得产生旧 relation 字段、旧 version、缺失 operation_id 或可变 REVIEW 形状；
- 每个 resource/template 都必须在 disposition 测试中被点名，不允许靠计数掩盖漏项。

### 5.4 stdio 与 relay 分层

基础 `fcop-mcp` 安装必须是纯 stdio 薄适配：

- 从基础 dependencies 移除 `websockets`；
- 提供 `fcop-mcp[relay]` 可选 extra，承载 websocket relay 依赖；
- relay 模块只在显式使用 relay 时惰性导入；
- 未安装 extra 时，stdio 导入、启动、list tools/resources/templates 与基础调用均成功；
- 未安装 extra 而显式启动 relay 时，返回清晰依赖错误，不得影响 stdio；
- WP4B 不增加第三个 PyPI 包，不增加 daemon、常驻 watcher 或网络自动连接。

### 5.5 包版本兼容门

`fcop-mcp` 启动必须在注册/执行正式能力前验证其与 `fcop` 的包版本组合：

- 受支持的组合由一个声明式 compatibility table 定义；
- 未知、缺失、不可解析或不支持的组合 Fail Closed；
- 不从 PATH、全局 site-packages 或 fallback import 猜另一个版本；
- WP4B 不提升正式发行版本，不发布包；
- 开发树测试可使用显式 development compatibility entry，但不得让 wheel 接受任意 `>=` 组合；
- 最终 RC/stable 版本号与精确发布组合由 WP4D 决定。

### 5.6 MCP 错误投影

Core 的稳定错误码不得被转成成功字符串、泛化为无代码异常或被 Adapter 吞掉。至少保证：

- Base 4.0 error code 原样可观察；
- 错误不触发 v3 fallback；
- 零写入断言仍成立；
- exact retry 返回 Core 已存在结果；
- 若当前 FastMCP 传输无法无歧义承载稳定 code，停止为 `MCP_ERROR_TRANSPORT_UNDERDETERMINED` 并提交证据，不得自行新增第二套错误协议。

## 6. 允许修改的范围

在确有需要且能解释的前提下允许：

- `mcp/src/fcop_mcp/**`
- `mcp/tests/**` 或仓库现有 MCP 测试目录
- `mcp/pyproject.toml`
- MCP package 内只读 spec 投影及打包配置
- `tests/test_fcop_mcp/snapshots/**`
- 与 WP4B 直接相关的 README/安装说明
- `CHANGELOG.md` 的 `[Unreleased]` 加法条目
- `reports/FCOP-4.0-WP4B-*.md`
- `reviews/fcop-4.0/wp4b/MANIFEST.md`

若真实路径不同，使用当前仓库既有对应路径，不得另造平行目录。

## 7. 明确禁止

- 修改冻结 `spec/fcop-4.0-spec*.md`；
- 删除、改名或弱化 60 个冻结 Test ID；
- 用 skip、xfail、过滤平台、`continue-on-error` 冒充通过；
- 修改 v4 Schema 来迎合 Adapter；
- 把 MCP 参数或 workspace 文件当作 evaluator；
- 复制 Project 生命周期、锁、幂等、授权或恢复代码；
- 新增数据库、ledger、queue、scheduler、timer、watcher、daemon；
- 实现 WP4C 规则拆分、AGENTS/CLAUDE/.mdc 生成或 Host profile；
- 修改 CodeFlowMu、其固定版本、UI、Runtime 或工作区；
- 合并 main、发布包、创建正式 Release；
- 自动迁移 v3 workspace 到 v4；
- 删除或覆盖用户脏现场。

## 8. 必须先写的测试

实现前建立红灯或审计证明，至少覆盖：

### 8.1 路由

- 明确 v3 工作区 -> v3 route；
- 明确 v4 工作区 -> v4 route；
- 缺失/未知/冲突/不可解析版本 -> 写前拒绝；
- v4 调用失败不回退 v3；
- 重新绑定不同版本工作区不沿用旧缓存。

### 8.2 45/11/3 表面

- tools 名称精确 45/45；
- resources 精确 11/11；
- templates 精确 3/3；
- disposition 覆盖 45/45、11/11、3/3；
- `close_issue` 不存在；
- tool schema 变化只有经批准的 v4 可选输入。

### 8.3 v3/v4 行为

- v3 现有 MCP 回归全部通过；
- v4 创建、T1–T7、幂等、family/recovery 走真实 Project；
- v4 `finish_task` 与 4 个 history 工具拒绝且零写入；
- v3 同名 legacy 工具保持原行为；
- caller authority/evaluator smuggling 拒绝；
- 空可信 Profile registry 的授权操作按合同失败；
- 启动时可信 registry 注入的合法路径通过。

### 8.4 resources/templates

- `fcop://spec` 在 v3/v4 返回正确版本投影与来源摘要；
- v4 不返回 v1.1/3.x 作为 current；
- v4 rules/protocol 在 WP4C 前显式不可用，不 silent fallback；
- 3 个 templates 分别生成 v3/v4 合法形状；
- 资源和 template 不授予角色权力。

### 8.5 安装与依赖

- clean venv 安装 base wheel，不安装 websockets，stdio 全部基础探针通过；
- clean venv 安装 `[relay]`，relay import/启动探针通过；
- base 环境显式用 relay 返回可诊断缺依赖；
- fcop/fcop-mcp 支持组合通过；不支持组合在启动前失败；
- sdist 与 wheel 内容一致，spec 投影 parity 通过。

## 9. 必须执行的验证

至少执行并报告真实命令、环境和原始计数：

1. 60/60 冻结 Test ID 与 119/119 v4 conformance；
2. 全量 `tests/test_fcop`；
3. 全量 MCP suite；
4. 45/11/3 canonical snapshot；
5. WP3E v4 unit regression；
6. Ruff、mypy、build；
7. base wheel clean-install；
8. relay extra clean-install；
9. Windows/Linux/macOS GitHub CI；
10. GitHub 最终 Manifest HEAD 的所有 required jobs 全绿。

不得把“本地通过”替代 GitHub CI。若 CI 存在与本阶段无关的既有红灯，也必须逐项证明基线来源；不得直接请求 Gate。

## 10. CodeFlowMu 只读 shadow

可在不写入 CodeFlowMu 的情况下只读验证：

- CodeFlowMu 仍固定 `fcop==3.2.5`、`fcop-mcp==3.2.5`；
- canonical 45 tool 名未因 WP4B 漂移；
- `close_issue` 仍被记录为 downstream static catalog drift；
- 不把 WP4B branch 安装到 CodeFlowMu，不运行工作区迁移。

这不是 CodeFlowMu 适配验收，结果只写兼容性 shadow 报告。

## 11. 交付文件

至少生成：

```text
reports/FCOP-4.0-WP4B-IMPLEMENTATION-PLAN.md
reports/FCOP-4.0-WP4B-VERSION-ROUTING-AND-TRUST-BOUNDARY.md
reports/FCOP-4.0-WP4B-45-11-3-DISPOSITION-RESULT.md
reports/FCOP-4.0-WP4B-PACKAGING-AND-RELAY-RESULT.md
reports/FCOP-4.0-WP4B-RESULT.md
reviews/fcop-4.0/wp4b/MANIFEST.md
```

Manifest 必须列出：

- 任务书路径、commit 与 SHA-256；
- input head 与父 Gate；
- Content commit、Manifest commit；
- 每个交付文件 SHA-256；
- 所有生产/测试/文档变更；
- 45/11/3 逐项覆盖统计；
- v3/v4/clean-install/CI 结果；
- 依赖前后差异；
- 新公共 API、模块、依赖、状态、后台组件、权威 Store 数量；
- main、release、CodeFlowMu 是否修改；
- 已知限制和未解决问题。

## 12. GitHub 审核交付

采用两提交交付：

1. `CONTENT_COMMIT`：实现、测试、报告；
2. `MANIFEST_COMMIT`：只增加/更新最终 Manifest。

要求：

- 推送固定 review 分支；
- 创建或更新 Draft PR，标题含 `[DO NOT MERGE][FCoP 4.0 WP4B]`；
- refetch 远端 HEAD；
- 从远端逐文件回读并验证 SHA-256；
- 报告 Draft PR URL、CI run URL、remote HEAD；
- 不使用本地路径作为 ADMIN 唯一审核入口。

## 13. 硬停止条件

遇到任一情况立即撤销未完成生产修改、保留证据并停止：

- 冻结合同无法唯一决定 Adapter 行为；
- 必须修改冻结 spec/schema/conformance 才能通过；
- 必须在 MCP 复制 Core 判断；
- 必须信任 caller/workspace 自声明 evaluator；
- 45/11/3 canonical 名称无法保持；
- FastMCP 无法承载稳定错误码且没有冻结映射；
- base stdio 无法与 relay 强制依赖解耦；
- v3 兼容与 v4 Fail Closed 无法同时成立；
- GitHub CI 非绿；
- input drift、脏文件冲突或范围外修改无法隔离。

阻断状态不得请求 Gate，只提交 `FCOP-4.0-WP4B-BLOCKED.md` 并报告单一 stop code。

## 14. 完成标准与停止点

只有以下全部成立才算完成：

```yaml
WP4B_STATUS: COMPLETE
WORKSPACE_ROUTING: PASS
V3_COMPATIBILITY: PASS
V4_PROJECT_DELEGATION: PASS
TRUSTED_PROFILE_INITIALIZATION: PASS
CALLER_AUTHORITY_SMUGGLING: REJECTED
MCP_TOOLS: 45/45
STATIC_RESOURCES: 11/11
RESOURCE_TEMPLATES: 3/3
FCOP_SPEC_VERSION_ROUTING: PASS
BASE_STDIO_WITHOUT_WEBSOCKETS: PASS
RELAY_OPTIONAL_EXTRA: PASS
PACKAGE_COMPATIBILITY_FAIL_CLOSED: PASS
V4_CONFORMANCE: 119/119
UNEXPECTED_FAILURES: 0
GITHUB_CI_AT_FINAL_HEAD: PASS
MAIN_MODIFIED: false
CODEFLOWMU_FILES_MODIFIED: 0
RELEASE_CREATED: false
WP4C_STARTED: false
```

完成后停止，只请求：

```yaml
REQUESTED_GATE: WP4B_MCP_ADAPTER_ACCEPTED
```

不得自行签署 Gate，不得进入 WP4C。

## 15. 固定回执格式

```yaml
WP4B_STATUS: COMPLETE | BLOCKED
AUTHORIZED_SCOPE: WP4B_ONLY
TASKBOOK_COMMIT: <sha>
TASKBOOK_SHA256: <sha256>
INPUT_HEAD: 982fcb24d9093e01c5ba4fdb87e710acd57e6d54
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
WORKTREE: <path>
BRANCH: review/fcop-4.0-wp4b-mcp-adapter

WORKSPACE_ROUTING: PASS | FAIL
V3_COMPATIBILITY: PASS | FAIL
V4_PROJECT_DELEGATION: PASS | FAIL
TRUSTED_PROFILE_INITIALIZATION: PASS | FAIL
CALLER_AUTHORITY_SMUGGLING: REJECTED | FAIL

MCP_TOOLS: 45/45
STATIC_RESOURCES: 11/11
RESOURCE_TEMPLATES: 3/3
TOOL_DISPOSITION: 45/45
RESOURCE_DISPOSITION: 11/11
TEMPLATE_DISPOSITION: 3/3

BASE_STDIO_WITHOUT_WEBSOCKETS: PASS | FAIL
RELAY_OPTIONAL_EXTRA: PASS | FAIL
PACKAGE_COMPATIBILITY_FAIL_CLOSED: PASS | FAIL

FROZEN_TEST_IDS: 60/60
V4_CONFORMANCE: <result>
TEST_FCOP: <result>
MCP_REGRESSION: <result>
RUFF: PASS | FAIL
MYPY: PASS | FAIL
GITHUB_CI_AT_FINAL_HEAD: PASS | FAIL
UNEXPECTED_FAILURES: <count>

NEW_PUBLIC_APIS: <count>
NEW_PRODUCTION_MODULES: <count>
NEW_RUNTIME_DEPENDENCIES: <count>
NEW_BACKGROUND_COMPONENTS: 0
NEW_AUTHORITATIVE_STORES: 0
NEW_STATE_MACHINES: 0

CONTENT_COMMIT: <sha>
MANIFEST_COMMIT: <sha>
REMOTE_HEAD: <sha>
REMOTE_PUSHED: true | false
REMOTE_REFETCH_VERIFIED: PASS | FAIL
DELIVERY_SHA256: <matched>/<total>
DRAFT_PR_URL: <url>

MAIN_MODIFIED: false
CODEFLOWMU_FILES_MODIFIED: 0
RELEASE_CREATED: false
WP4C_STARTED: false
REQUESTED_GATE: WP4B_MCP_ADAPTER_ACCEPTED | NONE
```
