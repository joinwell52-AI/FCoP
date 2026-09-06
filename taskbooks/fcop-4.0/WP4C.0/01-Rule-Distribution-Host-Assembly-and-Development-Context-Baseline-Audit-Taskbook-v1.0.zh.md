---
title: "FCoP 4.0 WP4C.0：规则分发、Host薄装配与开发上下文基线审计任务书"
version: "1.0"
date: "2026-09-06"
status: "AUTHORIZED_FOR_WP4C_0_ONLY"
document_role: "EXECUTION_TASKBOOK"
authority: "ADMIN"
execution_authorized: true
implementation_authorized: false
activation_authorized: false
authorized_scope: "WP4C_0_ONLY"
target_repository: "joinwell52-AI/FCoP"
program: "FCOP_4_0"
work_package: "WP4C.0"
parent_gate: "WP4B_MCP_ADAPTER_ACCEPTED"
parent_gate_commit: "aad88ae5f1112881545d30c9938739e83481516d"
effective_input_head: "aad88ae5f1112881545d30c9938739e83481516d"
frozen_contract_commit: "aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6"
main_merge_authorized: false
release_authorized: false
codeflowmu_change_authorized: false
workspace_migration_authorized: false
network_write_authorized: false
---

# FCoP 4.0 WP4C.0：规则分发、Host 薄装配与开发上下文基线审计任务书

## 0. 唯一执行授权

本文件是当前唯一允许执行的 WP4C 文件。执行者只能完成 **WP4C.0 只读审计与报告交付**，不得进入规则重写、生成器、MCP 资源实现、Host 投影生成或下游部署。

本次正式接续点是 ADMIN Gate：

```yaml
GATE: WP4B_MCP_ADAPTER_ACCEPTED
GATE_COMMIT: aad88ae5f1112881545d30c9938739e83481516d
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
```

执行者必须从该 Gate 提交建立独立 worktree 和 review 分支。若父提交、任务书字节或 GitHub 固定分支与本文不一致，必须以 `INPUT_REF_MISMATCH` 停止。

本任务书取代旧候选文件：

```text
taskbooks/fcop-4.0/WP3C/
FCoP-4.0-WP3C-rule-package-and-host-adapters-taskbook-v0.1.md
```

旧文件只作为审计输入；不得按其旧 WP3C 编号、旧父提交或连续执行授权开展工作。

## 1. 本阶段裁决

FCoP 4.0 的后续规则工作正式归入 **WP4C**，不是独立产品线，也不是 CodeFlowMu 改造。

FCoP 的分层保持：

| 层 | 权威内容 | WP4C 是否可改变 |
|---|---|---:|
| Specification | FCoP 4.0 规范条款 | 否 |
| Core implementation | 文件、生命周期、授权、幂等、恢复 | 否 |
| Rule package | 规范到 Agent 可执行指导的最小投影 | 后续阶段可实现 |
| Toolkit / MCP | 查询、部署与 Host 接入便利面 | 后续阶段仅薄适配 |
| Profile | 角色、组织与产品策略 | 只识别边界，不进入 Core |
| Runtime / product | 调度、Session、UI、数字员工 | 不属于本任务 |

规则包不是新的协议权威。它只能引用和投影冻结 Specification，不得反向定义 Core。

## 2. 必须坚持的 Unix 底线

WP4C 所有阶段必须遵守以下底线：

1. 文件承载协议，路径与 Manifest 提供可检查的寻址；
2. 每个模块只做好一件事，正文只有一个权威来源；
3. 小程序或薄适配器通过稳定文件与参数组合，不共享隐藏状态；
4. Host 入口只是装配插槽，不是协议、Runtime 或权限裁判；
5. 缺失、冲突、摘要错误一律 fail closed，不猜测、不静默补全；
6. 3.x 与 4.0 显式隔离，现有工作区不自动迁移；
7. 不增加数据库、Watcher、后台服务、第二套状态机或第二个更新器；
8. 不把所有规则塞入 AGENTS.md、CLAUDE.md 或 .mdc；
9. 不用一个新的“大规则平台”替代旧大文件；
10. 能由纯文件、确定性生成和命令完成的，不引入常驻 Runtime。

## 3. 三类内容必须分开

| 内容 | 面向对象 | 是否进入普通 FCoP 下游 | 权威来源候选 |
|---|---|---:|---|
| FCoP 4.0 protocol guidance | 使用 FCoP 的 Agent | 是，按需最小装配 | 冻结规范的可追溯投影 |
| FCoP repository development manual | 修改 FCoP 源码的开发 Agent | 否 | FCoP 仓库开发规则 |
| Agent 原生软件工程宪法 | 从事软件开发的 Agent | 否，只有开发工作加载 | 独立版本与 digest 的外部/仓内权威文件 |

普通 FCoP 业务 Agent 不得因为使用 FCoP 而自动加载编程宪法。开发 FCoP 本体的 Agent 必须能证明加载了宪法和 FCoP 开发手册，但这个证明不能成为普通业务协议字段或生命周期 Gate。

WP4C.0 必须查明宪法的真实权威文件、版本、digest、许可和获取方式。若不存在可固定来源，只报告 `ENGINEERING_CONSTITUTION_SOURCE_UNRESOLVED`，不得自行编写一份冒充已采用宪法。

## 4. Host 边界

FCoP 4.0 只定义最小 Host 装配合同：

```text
canonical rule modules
→ distribution manifest
→ adopted host profile
→ deterministic thin entry
```

必须区分：

| 事实 | 含义 |
|---|---|
| Adapter supported | 生成器知道该 Host 的文件格式 |
| Host adopted | ADMIN 明确选择该 Host profile |
| Entry generated | 对某工作区生成了入口文件 |
| Runtime consumption verified | 真实 Host 已读取并遵循该入口 |

四者不能互相替代。文件存在不代表 Host 已采用；Host 已采用不代表某次 Session 已读取；Host 名称不选择模型。

本 WP4C 不实现通用 Host 准入平台。模型清单、Subagent、工具权限、二进制哈希、升级采用和 Session 隔离属于 Runtime/Profile 或可选外部插件。FCoP 只消费 ADMIN 固定的 Host profile，并确定性生成薄入口。

## 5. WP4C 总路线（仅路线，不授权后续阶段）

| 阶段 | 目标 | 本任务是否授权 |
|---|---|---:|
| WP4C.0 | 真实基线、消费者、覆盖与冲突审计 | 是 |
| WP4C.1 | 冻结 Rule Package、Manifest、模块和 Host 投影合同 | 否 |
| WP4C.2 | 先写失败的分发符合性测试 | 否 |
| WP4C.3 | 实现分类模块、Manifest、确定性生成器和薄入口 | 否 |
| WP4C.4 | MCP read-only 资源、显式部署命令与 3.x 兼容 | 否 |
| WP4C.5 | FCoP 自身与下游 shadow、回滚、跨平台验证 | 否 |
| WP4C.6 | 收口验收；请求 WP4C_RULE_PACKAGE_ACCEPTED | 否 |

每一阶段必须有独立固定任务书、输入提交、SHA-256、review 分支和 ADMIN Gate。不得因本总路线存在而连续执行。

## 6. WP4C.0 工作目标

只读查明以下事实，不提前设计实现：

1. 当前规则 canonical source 的准确文件、版本和 digest；
2. AGENTS.md、CLAUDE.md、.cursor/rules/*.mdc 的真实来源及生成关系；
3. Project.deploy_protocol_rules、MCP redeploy_rules、规则版本读取与归档路径；
4. wheel/sdist 实际携带的规则、模板、规范和资源；
5. 根 Host 文件是否同时承担 FCoP 源码开发入口和下游模板源；
6. 当前大文件包含哪些 normative、commentary、历史、开发、Profile 和产品内容；
7. 冻结 4.0 规范的每条条款未来应映射到哪个稳定语义域；
8. 3.x active rule 的逐条处置需求；
9. CodeFlowMu 或其他下游中哪些区域由 FCoP 管理，哪些由产品自身管理；
10. 当前 Host 能否消费“短入口 + 文件引用”，以及不能时需要什么有界投影；
11. WP4B 的 fcop://rules、fcop://protocol 和 guidance typed-unavailable 点应由 WP4C 哪个阶段闭合；
12. 是否存在无法在不改变冻结 Core 的前提下完成的冲突。

## 7. 强制审计对象

至少审查以下固定输入及其 Git 历史：

```text
spec/fcop-4.0-spec.md
spec/fcop-4.0-spec.zh.md
src/fcop/rules/__init__.py
src/fcop/rules/_data/**
src/fcop/project.py
mcp/src/fcop_mcp/server.py
mcp/src/fcop_mcp/disposition.py
mcp/src/fcop_mcp/resources.py
scripts/rule_encoding_guard.py
AGENTS.md
CLAUDE.md
.cursor/rules/**
docs/getting-started.md
docs/getting-started.en.md
docs/upgrade-fcop-mcp.md
docs/release-process.md
docs/releases/RELEASE-CHECKLIST.md
adr/ADR-0006-host-neutral-rule-distribution.md
tests/test_fcop/**rule**
tests/test_fcop_mcp/**rule**
```

还必须读取 WP4B Gate、WP4B Manifest 和五份报告，以免重新发明已经冻结的 MCP 边界。

CodeFlowMu 只允许只读 shadow：优先使用 GitHub 固定提交或独立只读副本。不得在 `D:\codeflowmu` 中生成、覆盖、安装、升级或清理文件。

## 8. 审计方法

### 8.1 工作区保护

- 若 `D:\FCoP` 不干净，不得切分支、stash、reset 或清理；
- 从固定 Gate 提交新建独立 worktree；
- 审计可以运行只读命令、构建临时 wheel 和在临时目录执行 dry-run；
- 临时目录不得指向任何真实下游工作区；
- 不得调用会部署规则的命令，除非目标是新建临时目录且已证明确为 dry-run/隔离验证；
- 不得修改 main、PR #15、CodeFlowMu 或用户现有工作区。

### 8.2 双向覆盖

形成两张机器可核对的映射，不要求本轮写新规则：

```text
正向：FCoP 4.0 normative clause → 候选语义模块
反向：3.x active rule → retained | superseded | obsolete | commentary | profile | development | conflict
```

正向覆盖必须以冻结英文规范为条款身份来源，并核对中英文平行；反向审计必须以真实 3.x canonical source 为来源，不能只扫描根投影副本。

### 8.3 内容分类

每个独立规则单元至少记录：

```yaml
rule_id: ""
source_path: ""
source_anchor: ""
normative: true | false
authority: specification | guidance | profile | development | history | commentary
candidate_module: ""
disposition: retained | superseded | obsolete | commentary | profile | development | conflict
host_specific: false
downstream_required: false
notes: ""
```

若无法稳定分类，标记 `RULE_CLASSIFICATION_UNRESOLVED`，不得创建 misc/other/temporary 兜底模块。

### 8.4 生成与覆盖风险

必须用真实代码回答：

- force/archive 默认值是什么；
- 哪些文件被整文件覆盖；
- 项目自有内容如何识别；
- 是否有 managed block；
- 失败时是否可能部分写入；
- 生成时间、绝对路径或随机值是否破坏可重复性；
- 3.x 与 4.0 如何区分；
- 未选 Host 是否仍被生成；
- 回滚依据和 Receipt 是否真实存在。

### 8.5 上下文测量

对 canonical source 和各投影记录：

- UTF-8 字节数；
- 行数；
- 估算 token 数时使用的方法；
- normative 内容比例；
- 重复正文比例；
- 普通顺序任务、并行 Branch 任务、FCoP 开发任务三种候选最小装配。

本轮不得为满足任意 KiB 目标删减语义。预算只作为 WP4C.1 的合同输入。

### 8.6 Host 事实审计

对 Codex、Cursor、Claude Code 及仓库中实际出现的其他 Host 逐项登记：

```yaml
host_id: ""
adapter_implemented: true | false
admin_adopted: true | false | unproven
generated_targets: []
canonical_inputs: []
supports_file_reference: true | false | unverified
runtime_consumption_evidence: verified | unverified | unavailable
model_selection_effect: none
```

WP4C.0 不安装 Host、不修改 Host 配置、不运行需要新登录或凭据的探针。已有 CLI 可做只读版本/帮助/隔离 smoke；无法证明时如实写 unverified。

## 9. 必须回答的合同问题

WP4C.0 报告必须给 WP4C.1 明确列出事实与待裁决项：

1. v4 Rule Package 的物理目录是否可以复用 `src/fcop/rules/_data/`，还是需要其下的 `v4/` 命名空间；
2. Manifest 是包内权威清单还是工作区采用回执，两者是否必须分开；
3. 模块 ID、版本、digest、依赖、选择条件和顺序的最小字段；
4. 模块正文的 canonicalization 与 SHA-256 字节规则；
5. Host profile 的最小静态输入及 ADMIN adoption 证据如何引用；
6. AGENTS.md、CLAUDE.md 和 .mdc 是短指针、受控嵌入还是编译产物；
7. 不支持跨文件引用的 Host 如何获得有界、可重现且不形成第二真相的投影；
8. FCoP 源码仓库开发入口与普通下游入口如何物理隔离；
9. 工程宪法只读引用、固定快照或 vendored 文本的许可与更新策略；
10. redeploy_rules 如何保持 3.x 行为，同时让 v4 显式选择 profile/hosts/dry-run；
11. 下游自有内容冲突时如何 fail closed；
12. 部署是否需要 staging、原子替换和追加 Receipt，且如何避免新状态机；
13. fcop://rules 与 fcop://protocol 应返回哪个只读对象；
14. 哪些能力只是 Toolkit/Profile，不得进入 Rule Core；
15. WP4C.1 前是否存在 P0 合同冲突。

## 10. 禁止项

WP4C.0 禁止：

1. 修改规范、Core、Schema、MCP、规则源、生成器、Host 投影或测试；
2. 新建正式 Rule Package、Manifest Schema 或生产目录；
3. 修改 AGENTS.md、CLAUDE.md 或任何 .mdc；
4. 运行 redeploy_rules 或 deploy_protocol_rules 写入真实工作区；
5. 设计或实现通用 Host 准入 Runtime；
6. 引入数据库、日志服务、Watcher、Daemon、Scheduler、Session 管理或 UI；
7. 把工程宪法塞入普通业务 Agent；
8. 把 CodeFlowMu 角色、EVAL、Host policy 或产品手册复制进 FCoP；
9. 修改 CodeFlowMu 固定的 fcop==3.2.5 / fcop-mcp==3.2.5；
10. 自动下载或采用 mutable 远程规则包；
11. 以测试通过代替真实代码与字节审计；
12. 修改 main、合并 PR、发布包或创建 Release；
13. 进入 WP4C.1–WP4C.6。

## 11. 交付文件

只允许新增以下五个文件：

```text
reports/FCOP-4.0-WP4C.0-DISTRIBUTION-BASELINE.md
reports/FCOP-4.0-WP4C.0-RULE-DISPOSITION.md
reports/FCOP-4.0-WP4C.0-HOST-CONSUMER-MATRIX.md
reports/FCOP-4.0-WP4C.0-CONTEXT-AND-COLLISION-AUDIT.md
reviews/fcop-4.0/wp4c.0/MANIFEST.md
```

其中：

- Distribution Baseline：真实 source、生成器、部署、打包、版本与恢复事实；
- Rule Disposition：4.0 clause 正向映射和 3.x active rule 反向处置；
- Host Consumer Matrix：Host 支持/采用/生成/真实消费四类事实；
- Context and Collision Audit：上下文体积、重复、开发/业务隔离、下游覆盖风险；
- Manifest：固定输入、文件 SHA-256、审计命令、限制和请求 Gate。

不得借报告路径夹带实现文件、规范候选、测试或生成产物。

## 12. 验证要求

至少完成：

1. 输入 Gate、父链、任务书路径和任务书 SHA-256；
2. 现有全仓规则相关测试的只读基线；
3. 3.x canonical source 与四个投影的字节/结构比较；
4. wheel 与 sdist 规则文件 inventory；
5. Project 与 MCP 分发入口的静态调用图；
6. 强制审计对象 UTF-8/LF 检查；
7. 报告内表格计数和双向覆盖计数；
8. `git diff --check`；
9. 交付 allowlist；
10. GitHub 远端回读与五文件 SHA-256。

如果完整 v3/v4 回归耗时过大，本轮只需运行规则分发相关测试和静态审计；必须如实报告未运行的套件，不得复用旧绿灯冒充本轮结果。

## 13. GitHub 审核交付规则

1. 分支名固定为：`review/fcop-4.0-wp4c.0-distribution-audit`；
2. 从 Gate commit `aad88ae5f1112881545d30c9938739e83481516d` 建立独立 worktree；
3. Content Commit 只含四份 reports；
4. Manifest Commit 是 Content Commit 的唯一直接子提交，只新增 Manifest；
5. 推送 review 分支并创建/更新 Draft PR；
6. 从 GitHub 重新 fetch 分支 HEAD；
7. 验证父链、五文件路径及 SHA-256；
8. PR 正文或最终评论写远端回执；
9. 不改 main，不 force-push，不把本地路径作为唯一审核入口。

若 GitHub 写入权限不可用，必须停止并报告 `GITHUB_DELIVERY_UNAVAILABLE`；不得用 ZIP、聊天附件或用户手工搬运替代正式交付。

## 14. 停止条件

出现以下任一情况立即停止：

- 输入提交或任务书 SHA 不一致；
- 需要修改冻结规范/Core 才能建立规则投影；
- canonical source 无法唯一确定；
- 发现现有部署会不可恢复地覆盖下游内容；
- 工程宪法来源、许可或 digest 无法确定；
- 规则单元无法分类且只能放入兜底模块；
- 需要新增 Runtime、数据库、后台服务或第二状态机；
- 必须修改 CodeFlowMu 或真实下游工作区；
- 交付 diff 超出五文件 allowlist。

停止时仍可提交事实报告，但必须标为 BLOCKED，不得请求后续 Gate。

## 15. 完成回执

完成后只允许请求：

```yaml
WP4C_0_STATUS: COMPLETE | BLOCKED
AUTHORIZED_SCOPE: WP4C_0_ONLY
PARENT_GATE_COMMIT: aad88ae5f1112881545d30c9938739e83481516d
TASKBOOK_COMMIT: ""
TASKBOOK_SHA256: ""
WORKTREE: ""
BRANCH: review/fcop-4.0-wp4c.0-distribution-audit

CANONICAL_SOURCE_IDENTIFIED: true | false
GENERATED_TARGETS_MAPPED: n/n
V4_CLAUSE_MAPPING: n/n
V3_ACTIVE_RULE_DISPOSITION: n/n
HOST_CONSUMER_MATRIX: n/n
CONTEXT_MEASUREMENTS: n/n
CODEFLOWMU_SHADOW: PASS | GAP | NOT_AVAILABLE
P0_CONTRACT_CONFLICTS: n

FILES_WRITTEN: 5/5
CODE_FILES_MODIFIED: 0
SPEC_FILES_MODIFIED: 0
SCHEMA_FILES_MODIFIED: 0
MCP_FILES_MODIFIED: 0
RULE_FILES_MODIFIED: 0
HOST_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0

CONTENT_COMMIT: ""
MANIFEST_COMMIT: ""
REMOTE_PUSHED: true | false
REMOTE_REFETCH_VERIFIED: PASS | FAIL
DELIVERY_SHA256: 5/5 | n/5
MAIN_MODIFIED: false
RELEASE_CREATED: false
WP4C_1_STARTED: false

REQUESTED_GATE: WP4C_0_BASELINE_ACCEPTED | NONE
```

只有 `P0_CONTRACT_CONFLICTS: 0` 且所有事实映射完成时，才可请求 `WP4C_0_BASELINE_ACCEPTED`。完成后必须停止，等待 ADMIN 另行固定 WP4C.1 合同任务书。

