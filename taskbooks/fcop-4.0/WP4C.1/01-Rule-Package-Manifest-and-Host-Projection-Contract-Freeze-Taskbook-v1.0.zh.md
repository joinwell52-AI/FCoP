---
title: "FCoP 4.0 WP4C.1：模块化规则包、Manifest 与 Host 薄投影合同冻结任务书"
document_id: "FCOP-4.0-WP4C.1-TASKBOOK"
version: "1.0"
date: "2026-09-07"
status: "AUTHORIZED_FOR_WP4C_1_ONLY"
document_role: "EXECUTION_TASKBOOK"
authority: "ADMIN"
execution_authorized: true
authorized_scope: "WP4C_1_ONLY"
implementation_authorized: false
conformance_implementation_authorized: false
main_merge_authorized: false
release_authorized: false
parent_gate: "WP4C_0_BASELINE_ACCEPTED"
parent_gate_commit: "65ed07263de707d327e6e2c358aec2dd7c00a6df"
wp4c_0a_head: "59a6654dbb5387201056004c06068f8afcafb9ed"
scope_correction_commit: "abc2dc06db227dbc81afbd554c372271c05e89da"
frozen_fcop_contract_commit: "aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6"
requested_gate: "WP4C_1_RULE_DISTRIBUTION_CONTRACT_FROZEN"
---

# FCoP 4.0 WP4C.1：模块化规则包、Manifest 与 Host 薄投影合同冻结任务书

## 0. 唯一执行授权

本文件是当前唯一允许执行的 WP4C.1 任务书。

本轮只允许根据已经完成的 WP4C.0/0a 审计，编写并冻结候选合同，不允许修改规则正文、生成器、Host 文件、Python、MCP、Schema、测试、CodeFlowMu 或 main。

完成后必须停止并请求：

```text
WP4C_1_RULE_DISTRIBUTION_CONTRACT_FROZEN
```

没有该 Gate，不得进入 WP4C.2。

## 1. 固定输入

执行者必须从 ADMIN 下发的本任务书固定提交创建独立 worktree。其父链必须包含：

```yaml
WP4C_0_BASELINE_GATE_COMMIT: 65ed07263de707d327e6e2c358aec2dd7c00a6df
WP4C_0A_AUDIT_HEAD: 59a6654dbb5387201056004c06068f8afcafb9ed
SCOPE_CORRECTION_COMMIT: abc2dc06db227dbc81afbd554c372271c05e89da
FROZEN_FCOP_4_CONTRACT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
```

必须完整读取：

```text
reports/FCOP-4.0-WP4C.0-DISTRIBUTION-BASELINE.md
reports/FCOP-4.0-WP4C.0-RULE-DISPOSITION.md
reports/FCOP-4.0-WP4C.0-HOST-CONSUMER-MATRIX.md
reports/FCOP-4.0-WP4C.0-CONTEXT-AND-COLLISION-AUDIT.md
reports/FCOP-4.0-WP4C.0A-CONSTITUTION-SOURCE-DECISION.md
reviews/fcop-4.0/wp4c.0/MANIFEST.md
reviews/fcop-4.0/gates/WP4C-0-BASELINE-ACCEPTED.md
reviews/fcop-4.0/decisions/WP4C-0B-SCOPE-CORRECTION.md
spec/fcop-4.0-spec.md
spec/fcop-4.0-spec.zh.md
```

如果父链、任务书摘要或冻结规范不匹配，以 `INPUT_REF_MISMATCH` 停止。

## 2. 作用域纠正：三个对象必须分开

### 2.1 FCoP 4.0 Rule Package

服务对象：使用 FCoP 协议完成工作的 Agent。

内容只能是冻结 FCoP 4.0 Specification 的可追溯、最小、可装配指导。它不得包含 CodeFlowMu 产品逻辑，也不得包含软件开发宪法全文。

### 2.2 FCoP repository development guidance

服务对象：修改 FCoP 仓库源码、规范、测试、打包或发布的开发 Agent。

它属于 FCoP 仓库自身的开发治理，不得进入普通业务 Agent 的最小规则包。WP4C.1 只冻结其隔离位置与引用边界，不重新编写其完整正文。

### 2.3 CodeFlowMu 过渡宪法候选

固定摘要为 `87cf212d…abc4c` 的 `Agent原生软件工程宪法-v1.0-rc.1` 仅用于 CodeFlowMu 当前开发过渡。

正式处置：

```yaml
CLASSIFICATION: CODEFLOWMU_TRANSITION_ONLY
FCOP_RULE_PACKAGE_INPUT: false
FCOP_DEVELOPMENT_AUTHORITY: false
BUNDLED_BY_FCOP: false
HOST_PROJECTED_BY_FCOP: false
WP4C_1_CONTRACT_SOURCE: false
```

不得复制、改写、翻译、采用或激活该文件。任务书分支中的历史副本只供审计，不是权威源。

## 3. Unix 架构底线

WP4C.1 合同必须保持：

1. 一个规则单元只承担一个稳定语义域；
2. 每段正文只有一个可编辑 canonical source；
3. Manifest 只描述文件、摘要、依赖、顺序和适用条件，不承载规则正文；
4. Host adapter 只把已选模块投影到 Host 支持的入口格式；
5. Host 文件是派生物，不是第二权威；
6. 无常驻服务、数据库、Watcher、Daemon、Scheduler、Session manager 或远程规则中心；
7. 不自动下载 latest，不自动采用新版本，不自动生成所有 Host；
8. 3.x 和 4.0 物理隔离、显式选择；
9. 下游自有内容不被静默覆盖；
10. 所有写入都必须可 dry-run、可比较、可拒绝、可恢复；
11. 缺失、摘要漂移、依赖冲突和未知 Host 一律 Fail Closed；
12. Rule Package 不判断业务完成，不获得生命周期 authority。

## 4. 必须冻结的五层合同

### 4.1 Canonical modules

候选物理命名空间固定为：

```text
src/fcop/rules/_data/v4/
```

WP4C.1 必须冻结模块清单与职责。至少包括以下稳定语义域，允许审计证明后合并，但不得新增产品域：

| 候选模块 | 唯一职责 |
|---|---|
| workspace | 协议版本、工作区身份、路径与编码 |
| envelopes | TASK/REPORT/ISSUE/REVIEW 正式文件 |
| lifecycle | T1–T7、NOW/PAST 与单步迁移 |
| relations | branch_of、blocks、relates_to、supersedes |
| convergence | Branch REPORT、head 与 Root 显式汇合 |
| authorization | 授权引用、可信 Profile 边界、单次消费 |
| idempotency | operation identity、请求摘要与重试 |
| recovery | 原子性、收据、恢复状态与未知停止 |
| compatibility | 3.x/4.0 隔离及 legacy 行为边界 |

每个冻结规范条款必须映射到且只映射到一个 primary module；交叉引用不得复制规范义务。

### 4.2 Distribution Manifest

必须冻结一个包内权威 Manifest，候选路径：

```text
src/fcop/rules/_data/v4/manifest.json
```

最小字段必须包括：

```yaml
manifest_schema
protocol_version
package_version
module_id
source_path
language
sha256
size_bytes
normative_clause_refs
depends_on
load_order
audience
required_when
conflicts_with
```

要求：

- 同一模块中英文为两个 artifact，共用 module_id 和 clause mapping；
- 摘要按 Git/package 原始字节计算；
- `depends_on` 必须无环；
- `load_order` 只解决确定性装配，不表达业务优先级；
- Manifest 不记录工作区采用状态；
- Manifest 不记录 Host 是否真的消费；
- 不加入时间戳、绝对路径、随机值或运行态字段。

### 4.3 Workspace adoption receipt

包内 Manifest 与工作区采用回执必须分开。

采用回执只记录某个工作区明确选择的：

```yaml
protocol_version
rule_package_version
rule_manifest_sha256
selected_modules
selected_languages
selected_host_profile
target_paths
adopted_by
adopted_at
previous_receipt_ref
```

本轮只冻结字段和语义，不实现 receipt。缺少采用回执时，不得把 Host 文件存在解释为已采用。

### 4.4 Host profile

Host profile 是静态装配输入，不是 Host 准入平台。最小字段：

```yaml
host_id
profile_version
supported_entry_kinds
reference_mode
projection_mode
target_paths
preserve_regions
max_projection_bytes
encoding
newline
```

必须区分四种事实：

```text
adapter_supported
admin_adopted
entry_generated
runtime_consumption_verified
```

任何一个都不能推导另一个。

WP4C.1 只冻结 Codex、Cursor、Claude Code 的候选静态 profile 合同；不得探测模型、Subagent、二进制、认证、权限或平台能力。未知 Host 默认不生成。

### 4.5 Deterministic projection

必须冻结两种模式：

- `reference`：Host 支持文件引用时，只生成短入口；
- `bounded_embed`：Host 不支持可靠引用时，按 Manifest 将明确选择的模块确定性拼接。

投影必须满足：

- 相同输入字节产生相同输出字节；
- 不包含生成时间、机器路径或随机值；
- 输出包含来源版本与 Manifest digest；
- 不把多个语言同时塞入同一入口，除非 profile 明确选择；
- 超过 profile 上限时 Fail Closed，不自动删减规则；
- 生成前展示 diff；
- 只改受管理区域或新文件；
- 遇到未受管理的下游内容冲突必须停止；
- 写入采用临时同目录文件加原子替换；
- 生成后产生追加式 deployment receipt；
- 回滚只回到上一条已采用、摘要仍匹配的 receipt；
- 不建立后台更新器或第二状态机。

## 5. 三种最小装配

必须冻结：

### 5.1 普通顺序任务

只装配完成顺序 FCoP 工作所必需的模块，不加载 Branch convergence、FCoP 开发规则或 CodeFlowMu 宪法。

### 5.2 并行 Branch family

在顺序最小集上显式增加 relations 与 convergence；不得因为安装 FCoP 自动启用并行。

### 5.3 FCoP 仓库开发

```text
FCoP repository development entry
+ FCoP development guidance
+ 当前有效FCoP合同
+ 当前TASK与授权
```

未来若 ADMIN 另行采用通用开发宪法，只能作为独立固定引用插入最前面；当前没有该来源时，不得拿 CodeFlowMu RC 补位。

FCoP 开发装配不得进入普通业务 Agent、wheel 默认业务 guidance 或 MCP 默认资源响应。

## 6. 3.x 兼容与迁移边界

必须冻结：

- 现有 3.x canonical source 与 Host 输出保持 legacy namespace；
- v4 模块不得覆盖 3.x 文件；
- `redeploy_rules` 的无版本旧调用保持 3.x 行为；
- v4 必须由显式 workspace version、manifest 与 adopted Host profile 选择；
- 不自动迁移已有工作区；
- 不把 3.x 大文件继续修改成“兼容 4.0 的更大文件”；
- 4.0 实现完成后，3.x Host 输出仍可重建并与当前兼容测试对齐；
- legacy 文档漂移只能显式记录或版本化修复，不能静默归一化为“相同”。

## 7. MCP 边界

WP4C.1 只冻结后续 MCP 映射：

- `fcop://rules` 返回所选版本的包内 Manifest 或明确 typed-unavailable；
- `fcop://protocol` 返回所选版本的规范身份，不返回 Host 运行状态；
- read-only guidance 资源按 workspace version 与 selected modules 读取；
- 部署必须是显式 effectful 命令，不能由 resource read 触发；
- MCP 只调用 Toolkit/Project 的规则分发能力，不复制解析、摘要、选择或写入算法；
- Relay 不获得规则权威或自动更新能力。

不得在本轮修改 WP4B 已接受的工具和资源实现。

## 8. 必须处理的审计发现

合同决策报告必须逐项处置，不得遗漏：

- 86/86 路径清单；
- 147/147 规则单元；
- 73/73 冻结规范条款；
- 12/12 Host/消费者；
- 4/4 当前派生目标；
- 六文件上下文测量；
- AGENTS/CLAUDE 重复；
- Cursor 两项源/输出漂移；
- 50 个前导 BOM 与嵌入 BOM/控制字符；
- getter/index/进程/部署/Host 五种失效边界；
- wheel/sdist 的 CRLF-only 差异；
- 旧指南与发布文档的版本漂移；
- Host runtime consumption 未验证；
- CodeFlowMu 只读 shadow 边界；
- CodeFlowMu 过渡 RC 排除决定。

历史问题可以被安排到 WP4C.2–WP4C.6，但必须有唯一所有阶段和验收证据，不能写“以后处理”。

## 9. 本轮交付文件

只允许新增：

```text
docs/fcop-4.0/rule-distribution-contract.md
docs/fcop-4.0/rule-distribution-contract.zh.md
reports/FCOP-4.0-WP4C.1-CONTRACT-DECISIONS.md
reports/FCOP-4.0-WP4C.1-CONFORMANCE-MATRIX.md
reports/FCOP-4.0-WP4C.1-RESULT.md
reviews/fcop-4.0/wp4c.1/MANIFEST.md
```

不得修改冻结规范。英文/中文合同必须使用相同 clause ID；义务强度、字段、错误与阶段 Gate 必须一致。

## 10. 后续阶段划分

WP4C.1 必须冻结但不得执行：

| 阶段 | 单一职责 |
|---|---|
| WP4C.2 | 先写失败的分发、装配、漂移、冲突与回滚符合性测试 |
| WP4C.3 | 实现 v4 canonical modules、Manifest loader 与三种最小装配 |
| WP4C.4 | 实现 Host 薄投影、显式部署、receipt 与回滚 |
| WP4C.5 | MCP read-only guidance、3.x兼容、FCoP自身及CodeFlowMu只读shadow验证 |
| WP4C.6 | 跨平台、制品、上下文与完整收口，申请 WP4C_RULE_DISTRIBUTION_ACCEPTED |

任何阶段不得连续自动执行。

## 11. 验证要求

至少完成：

- 六份输入报告、Gate、纠正决定与冻结规范全部读取；
- 合同中英文 clause parity；
- 73 条规范逐条映射到唯一 primary module；
- 147 条 legacy rule 全部获得冻结 disposition；
- 86 个路径全部获得 future owner；
- 12 个消费者全部获得生成／读取／不支持策略；
- Manifest、adoption receipt、Host profile 三类字段无混用；
- 三种最小装配无 CodeFlowMu RC；
- 普通业务装配无 FCoP 开发治理；
- 不存在数据库、Daemon、Watcher、Scheduler、Session 或远程规则中心；
- UTF-8/LF、无 BOM、`git diff --check`；
- 六文件 allowlist；
- 所有决定能追溯到冻结规范或 WP4C.0 证据。

本阶段不运行生成器、不改测试，也不要求全量产品回归。可运行只读文档一致性检查。

## 12. 强制停止条件

以下任一出现必须停止：

- 需要修改 FCoP 4.0 冻结规范；
- 无法将某条规范映射到唯一 primary module；
- 需要把 CodeFlowMu RC 当作 FCoP 权威来源；
- 需要把 FCoP 开发治理放进普通业务 Rule Package；
- 需要引入常驻 Runtime、数据库或自动更新；
- Manifest 同时承担包清单和工作区采用状态；
- Host profile 被用来证明 Runtime 已消费；
- 为满足上下文限制需要自动删减规则；
- 3.x 兼容只能通过扩大旧大文件实现；
- 中英文合同无法对齐；
- 六文件以外的修改成为必要条件。

停止时只提交事实报告，不得请求 Gate。

## 13. GitHub 交付

使用独立 review 分支。两提交交付：

1. Content commit：双语合同和三份报告；
2. Manifest commit：只新增 Manifest。

然后 push、refetch，核验远端 HEAD、直接父链与 6/6 SHA-256，创建 Draft PR 并留下完整回执。

不得修改或合并 PR #17；不得合并 main。

## 14. 完成回执

```yaml
WP4C_1_STATUS: COMPLETE | BLOCKED
AUTHORIZED_SCOPE: WP4C_1_ONLY
TASKBOOK_COMMIT: ""
TASKBOOK_SHA256: ""
INPUT_HEAD: ""
PARENT_GATE_COMMIT: 65ed07263de707d327e6e2c358aec2dd7c00a6df
SCOPE_CORRECTION_COMMIT: abc2dc06db227dbc81afbd554c372271c05e89da
FROZEN_FCOP_CONTRACT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
CONTRACT_CLAUSE_PARITY: n/n
V4_CLAUSE_PRIMARY_MAPPING: 73/73
LEGACY_RULE_DISPOSITION: 147/147
PATH_FUTURE_OWNER: 86/86
HOST_CONSUMER_MAPPING: 12/12
MODULE_CONTRACTS: n/n
MANIFEST_CONTRACT: PASS
ADOPTION_RECEIPT_CONTRACT: PASS
HOST_PROFILE_CONTRACT: PASS
ASSEMBLY_PROFILES: 3/3
CODEFLOWMU_RC_EXCLUDED: PASS
P0_OPEN: 0
FILES_WRITTEN: 6/6
CONTENT_COMMIT: ""
MANIFEST_COMMIT: ""
REMOTE_HEAD: ""
REMOTE_PUSHED: true
REMOTE_REFETCH_VERIFIED: PASS
DELIVERY_SHA256: 6/6
WP4C_1_RULE_DISTRIBUTION_CONTRACT_FROZEN: false
WP4C_2_STARTED: false
MAIN_MODIFIED: false
CODEFLOWMU_MODIFIED: false
REQUESTED_GATE: WP4C_1_RULE_DISTRIBUTION_CONTRACT_FROZEN
```

完成后强制停止。执行者不得自行签署 Gate。
