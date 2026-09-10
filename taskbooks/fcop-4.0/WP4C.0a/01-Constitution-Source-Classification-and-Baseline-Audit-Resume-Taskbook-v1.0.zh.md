---
title: "FCoP 4.0 WP4C.0a：宪法来源定级与分发基线审计恢复任务书"
document_id: "FCOP-4.0-WP4C.0A-TASKBOOK"
version: "1.0"
date: "2026-09-07"
status: "AUTHORIZED_FOR_WP4C_0A_ONLY"
document_role: "EXECUTION_TASKBOOK"
execution_authorized: true
authorized_scope: "WP4C_0A_ONLY"
implementation_authorized: false
main_merge_authorized: false
release_authorized: false
parent_blocked_head: "4420bf6cdd456e328230015bcffef4fdabf615a8"
parent_blocked_pr: 16
constitution_source_commit: "0c61f7d3108777adb7aaf375324616c004fcaf7d"
constitution_source_sha256: "25e70e221d6b54072503a8ec7224df33000fa63c0b12a64c148d86a0081b6762"
constitution_source_status: "DISCUSSION_DRAFT_REVIEW_INPUT_ONLY"
constitution_normative: false
constitution_contract_frozen: false
constitution_license_status: "UNRESOLVED"
---

# FCoP 4.0 WP4C.0a：宪法来源定级与分发基线审计恢复任务书

## 0. ADMIN 裁决

WP4C.0 因缺少《Agent 原生软件工程宪法》的固定来源而停止，停止行为正确，没有越权。

本任务书同时修正上一任务书的阶段门语义：

> “宪法尚未冻结”是 WP4C.0 必须记录的审计发现，是进入 WP4C.1 的前置阻断；它不是完成 WP4C.0 基线审计的前置条件。

因此：

- 不撤销、不覆盖 WP4C.0 的 BLOCKED 报告和提交；
- 不把讨论稿冒充正式宪法；
- 允许恢复并完成 WP4C.0 尚未完成的只读审计；
- WP4C.0 完成后只能请求 `WP4C_0_BASELINE_ACCEPTED`；
- 即使该 Gate 被签署，也不得自动进入 WP4C.1；
- WP4C.1 仍须先取得独立的“宪法来源与效力冻结”裁决及新的固定任务书。

## 1. 唯一固定输入

执行者必须从 ADMIN 下发的本任务书冻结提交创建独立 worktree。该提交必须包含本文、固定讨论稿，并在父链中包含下列两个提交。不得从本地目录、PR 浮动 HEAD、main 或其他分支猜测输入：

```yaml
REPOSITORY: joinwell52-AI/FCoP
TASKBOOK_COMMIT: <以 ADMIN 下发的固定 commit 为准>
CONSTITUTION_SOURCE_COMMIT: 0c61f7d3108777adb7aaf375324616c004fcaf7d
PARENT_BLOCKED_HEAD: 4420bf6cdd456e328230015bcffef4fdabf615a8
PARENT_PR: 16
AUTHORIZED_SCOPE: WP4C_0A_ONLY
```

执行开始前必须验证冻结任务书提交的父链同时包含 `0c61f7d3108777adb7aaf375324616c004fcaf7d` 与 `4420bf6cdd456e328230015bcffef4fdabf615a8`，并核验以下来源文件：

```text
taskbooks/fcop-4.0/WP4C.0a/sources/Agent-Native-Engineering-Constitution-v0.1-discussion-draft.zh.md
SHA-256: 25e70e221d6b54072503a8ec7224df33000fa63c0b12a64c148d86a0081b6762
```

如果提交、路径或 SHA-256 不匹配，必须以 `FIXED_INPUT_MISMATCH` 停止。

## 2. 来源文件的法律与协议地位

该文件只具有以下地位：

```yaml
SOURCE_KIND: ADMIN_AUTHORED_DISCUSSION_DRAFT
SOURCE_VERSION: 0.1-discussion-draft
REVIEW_INPUT_FIXED: true
NORMATIVE: false
CONTRACT_FROZEN: false
IMPLEMENTATION_AUTHORIZED: false
BUNDLING_AUTHORIZED: false
RULE_GENERATION_AUTHORIZED: false
LICENSE_STATUS: UNRESOLVED
CANONICAL_RELEASE_PATH: UNRESOLVED
```

禁止：

- 将其改名或声明为 v1.0 正式宪法；
- 擅自添加 MIT、Apache、CC 或其他许可；
- 将其加入 Python wheel、MCP 包、Host 规则包或发布制品；
- 据此生成或修改 AGENTS.md、CLAUDE.md、.mdc 或 Host profile；
- 将讨论稿中的解释性内容直接提升为 FCoP 4.0 Core 条款。

允许：

- 将其作为确定的审计输入；
- 识别与现有规则、Host 投影、FCoP 4.0 冻结合同之间的重合、冲突与缺口；
- 形成 WP4C.1 前必须由 ADMIN 决定的最小问题清单。

## 3. 本轮目标

WP4C.0a 只完成六项工作：

1. 复核父提交中四份 WP4C.0 报告与 Manifest，保留全部阻断历史。
2. 完成原 WP4C.0 尚未完成的规则来源、生成物、Host 消费者、上下文预算及碰撞审计。
3. 对讨论稿进行“来源—效力—许可—分发”定级，不对正文做规范性改写。
4. 将规则条目逐项映射到 `CORE / CATEGORY_MODULE / HOST_ADAPTER / DEVELOPMENT_CONSTITUTION / LEGACY / REMOVE`。
5. 明确普通 FCoP 业务 Agent 与“开发 FCoP 的 Agent”两种加载边界。
6. 形成 WP4C.1 的前置决策清单，并在强制停止点请求 Gate。

## 4. 必须回答的审计问题

### 4.1 权威源与生成物

必须区分：

- 可编辑权威规则源；
- 由 Manifest 装配的分类模块；
- Codex / Cursor / Claude Code 等 Host 投影；
- 兼容性输出；
- 历史大文件；
- 仅供审阅的开发宪法讨论稿。

任何生成物不得反向成为权威源。不得继续以手工同时修改 AGENTS.md、CLAUDE.md、.mdc 作为维护方式。

### 4.2 两类 Agent 的加载边界

必须形成明确矩阵：

| 消费者 | FCoP Core | 角色/Profile | 开发宪法 | Host 薄适配 |
|---|---:|---:|---:|---:|
| 普通 FCoP 业务 Agent | 必需 | 按应用采用 | 禁止默认注入 | 按 Host |
| 开发 FCoP 的 Agent | 必需 | 按任务 | 候选为强制，但须先冻结 | 按 Host |
| 第三方应用开发 Agent | 必需 | 自有 Profile | 不自动注入 | 按 Host |
| CodeFlowMu | 兼容性 shadow | 下游自有 | 不注入 | 本轮不修改 |

### 4.3 讨论稿的最小决策清单

报告至少列出：

- 正式名称与版本；
- 权威仓库及规范路径；
- 是否拆出中英文双语；
- 适用对象；
- 强制加载条件；
- 与 FCoP Core/Specification/Profile/Toolkit/Runtime 的关系；
- 与通用规则包的关系；
- 修订与 Gate 流程；
- 许可与再分发政策；
- 内容摘要或制品摘要；
- Host profile 如何引用而不复制出多个权威版本；
- 普通业务 Agent 的明确排除规则。

本轮只能提出候选，不得替 ADMIN 作最终决定。

## 5. 允许修改的文件

只允许修改或新增：

```text
reports/FCOP-4.0-WP4C.0-CONTEXT-AND-COLLISION-AUDIT.md
reports/FCOP-4.0-WP4C.0-DISTRIBUTION-BASELINE.md
reports/FCOP-4.0-WP4C.0-HOST-CONSUMER-MATRIX.md
reports/FCOP-4.0-WP4C.0-RULE-DISPOSITION.md
reports/FCOP-4.0-WP4C.0A-CONSTITUTION-SOURCE-DECISION.md
reviews/fcop-4.0/wp4c.0/MANIFEST.md
```

固定来源文件只读，不得修改。

禁止修改：

- `src/`
- `mcp/src/`
- `spec/`
- `tests/`
- `.github/workflows/`
- 现有正式规则文件和 Host 投影
- CodeFlowMu
- main
- 任何发布配置或版本号

## 6. 验证要求

至少完成：

- 固定输入提交、父链和来源 SHA-256；
- UTF-8/LF 与 `git diff --check`；
- 六文件 allowlist；
- 所有现存规则源、生成物与消费者的路径级清单；
- 规则 Disposition 表计数闭合；
- Host/消费者矩阵计数闭合；
- 上下文碰撞、重复、覆盖顺序与失效规则审计；
- 对讨论稿 12 条原则逐条标记：已被现有规则覆盖 / 部分覆盖 / 缺失 / 与冻结合同冲突；
- 确认未运行生成器、未写实现、未更改现有规则。

若审计脚本只读且仓库已有，可运行；不得为了本轮新写生产脚本。

## 7. Gate 语义

允许请求：

```text
WP4C_0_BASELINE_ACCEPTED
```

该 Gate 仅表示“分发与规则现状已经审计清楚”，不表示：

- 宪法已冻结；
- WP4C.1 已授权；
- 规则包结构已实施；
- Host adapter 已实施；
- main 可合并；
- FCoP 4.0 可发布。

Manifest 必须同时记录：

```yaml
WP4C_0_AUDIT_BLOCKERS: 0
WP4C_1_ENTRY_BLOCKERS: 1
ENGINEERING_CONSTITUTION_SOURCE_STATUS: DISCUSSION_DRAFT_FIXED_REVIEW_INPUT
ENGINEERING_CONSTITUTION_LICENSE_STATUS: UNRESOLVED
ENGINEERING_CONSTITUTION_CONTRACT_FROZEN: false
WP4C_1_STARTED: false
```

若除宪法冻结之外仍存在任何未完成的 WP4C.0 审计项，不得请求 Gate。

## 8. GitHub 两提交交付

使用独立 review 分支。不得修改 PR #16 的历史提交。

交付必须为：

1. Content commit：五份报告内容；
2. Manifest commit：只更新 `reviews/fcop-4.0/wp4c.0/MANIFEST.md`，记录全部交付文件 SHA-256、父提交、测试/审计结果及停止状态。

随后：

- push review 分支；
- refetch 远端；
- 验证远端 HEAD、父链和 6/6 文件 SHA-256；
- 更新 Draft PR #16 或新建仅针对该恢复分支的 Draft PR；
- 在 PR 留完整机器可读回执；
- 停止。

不得合并 PR，不得删除旧分支或旧报告。

## 9. 强制停止条件

遇到以下任一情况必须停止：

- 固定输入或来源 SHA 不匹配；
- 需要修改冻结规范才能完成审计；
- 需要为讨论稿擅自确定许可或正式效力；
- 需要修改现有规则、生成器、Host 投影或产品代码；
- 无法闭合规则清单或消费者清单；
- 除“宪法待冻结”外仍有 WP4C.0 审计缺口；
- 发现工作树污染且无法通过独立 worktree 隔离。

停止时只允许提交报告，不得请求 Gate。

## 10. 完成回执

```yaml
WP4C_0A_STATUS: COMPLETE | BLOCKED
AUTHORIZED_SCOPE: WP4C_0A_ONLY
TASKBOOK_COMMIT: ""
INPUT_HEAD: ""
CONSTITUTION_SOURCE_COMMIT: 0c61f7d3108777adb7aaf375324616c004fcaf7d
PARENT_BLOCKED_HEAD: 4420bf6cdd456e328230015bcffef4fdabf615a8
CONSTITUTION_SOURCE_SHA256: 25e70e221d6b54072503a8ec7224df33000fa63c0b12a64c148d86a0081b6762
CONSTITUTION_SOURCE_STATUS: DISCUSSION_DRAFT_FIXED_REVIEW_INPUT
CONSTITUTION_LICENSE_STATUS: UNRESOLVED
CONSTITUTION_CONTRACT_FROZEN: false
RULE_INVENTORY: n/n
RULE_DISPOSITION: n/n
HOST_CONSUMER_MATRIX: n/n
CONSTITUTION_PRINCIPLE_MAPPING: 12/12
WP4C_0_AUDIT_BLOCKERS: 0
WP4C_1_ENTRY_BLOCKERS: 1
FILES_MODIFIED: 6/6
CONTENT_COMMIT: ""
MANIFEST_COMMIT: ""
REMOTE_HEAD: ""
REMOTE_PUSHED: true
REMOTE_REFETCH_VERIFIED: PASS
DELIVERY_SHA256: 6/6
MAIN_MODIFIED: false
CODEFLOWMU_MODIFIED: false
WP4C_1_STARTED: false
REQUESTED_GATE: WP4C_0_BASELINE_ACCEPTED
```

本任务书不签署任何 Gate。执行者完成后必须停止，等待 ADMIN 审核。
