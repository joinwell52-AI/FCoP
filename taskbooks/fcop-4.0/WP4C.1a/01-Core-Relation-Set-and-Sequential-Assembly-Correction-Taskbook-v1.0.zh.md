---
title: "FCoP 4.0 WP4C.1a：Core 关系集合与装配边界修正及 WP4C.1 恢复任务书"
document_id: "FCOP-4.0-WP4C.1A-TASKBOOK"
version: "1.0"
date: "2026-09-07"
status: "AUTHORIZED_FOR_WP4C_1A_ONLY"
document_role: "EXECUTION_TASKBOOK"
authority: "ADMIN"
execution_authorized: true
authorized_scope: "WP4C_1A_ONLY"
implementation_authorized: false
conformance_implementation_authorized: false
main_merge_authorized: false
release_authorized: false
resumes_stage: "WP4C.1"
blocked_head: "d92c72620757cea455aa24b5d635cc12f1e8b16a"
blocked_stop_code: "TASKBOOK_RELATION_SET_CONFLICT"
superseded_taskbook_commit: "81d5cd416515d9d712db0250514f7011c346a07c"
parent_gate: "WP4C_0_BASELINE_ACCEPTED"
parent_gate_commit: "65ed07263de707d327e6e2c358aec2dd7c00a6df"
scope_correction_commit: "abc2dc06db227dbc81afbd554c372271c05e89da"
frozen_fcop_contract_commit: "aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6"
requested_gate: "WP4C_1_RULE_DISTRIBUTION_CONTRACT_FROZEN"
---

# FCoP 4.0 WP4C.1a：Core 关系集合与装配边界修正及 WP4C.1 恢复任务书

## 0. ADMIN 裁决

WP4C.1 的停止行为正确。冲突来自任务书，不来自冻结的 FCoP 4.0 合同。

ADMIN 现作出以下唯一裁决：

1. FCoP 4.0 Base Core 的正式关系集合严格为：

   ```text
   parent
   branch_of
   subject_ref
   references
   ```

2. `blocks`、`relates_to`、`supersedes` 不是 FCoP 4.0 Base Core 关系名，不得作为上述字段的别名、替代字段或隐式编码。
3. `relations` 是普通顺序任务和并行 Branch family 的共同基础模块。
4. `convergence` 才是并行 Branch family 相对顺序最小装配新增的模块。
5. 冻结规范不修改；原 WP4C.1 任务书仅第 4.1 节错误关系行及第 5.1/5.2 节相关装配表述被本文替代，其余要求继续有效。

## 1. 唯一执行授权

本文是当前唯一允许执行的 WP4C.1a 任务书。

本轮授权包含两部分，必须在同一受控阶段内完成：

1. 应用本文的关系集合与装配边界修正；
2. 从已交付的 WP4C.1 阻断 HEAD 恢复并完成原 WP4C.1 的双语合同、决策、矩阵和结果交付。

这不是实现授权。不得修改规则正文、规则生成器、Host 输出、Python、MCP、Schema、冻结 Conformance、CodeFlowMu 或 main。

完成后必须停止并请求：

```text
WP4C_1_RULE_DISTRIBUTION_CONTRACT_FROZEN
```

没有该 Gate，不得进入 WP4C.2。

## 2. 固定输入与执行起点

执行者必须从本任务书的固定 GitHub commit 创建独立 worktree，不得从本地漂移分支、PR 页面浮动 HEAD 或 main 猜测输入。

固定父链必须包含：

```yaml
WP4C_1_BLOCKED_HEAD: d92c72620757cea455aa24b5d635cc12f1e8b16a
WP4C_1_BLOCKED_CONTENT: 741b1829283f6a7fc1023e0edd8176b58c63ded4
SUPERSEDED_TASKBOOK: 81d5cd416515d9d712db0250514f7011c346a07c
WP4C_0_BASELINE_GATE: 65ed07263de707d327e6e2c358aec2dd7c00a6df
SCOPE_CORRECTION: abc2dc06db227dbc81afbd554c372271c05e89da
FROZEN_FCOP_4_CONTRACT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
```

必须完整读取：

```text
taskbooks/fcop-4.0/WP4C.1/01-Rule-Package-Manifest-and-Host-Projection-Contract-Freeze-Taskbook-v1.0.zh.md
reports/FCOP-4.0-WP4C.1-CONTRACT-DECISIONS.md
reports/FCOP-4.0-WP4C.1-CONFORMANCE-MATRIX.md
reports/FCOP-4.0-WP4C.1-RESULT.md
reviews/fcop-4.0/wp4c.1/MANIFEST.md
spec/fcop-4.0-spec.md
spec/fcop-4.0-spec.zh.md
reports/FCOP-4.0-WP4C.0-DISTRIBUTION-BASELINE.md
reports/FCOP-4.0-WP4C.0-RULE-DISPOSITION.md
reports/FCOP-4.0-WP4C.0-HOST-CONSUMER-MATRIX.md
reports/FCOP-4.0-WP4C.0-CONTEXT-AND-COLLISION-AUDIT.md
reviews/fcop-4.0/gates/WP4C-0-BASELINE-ACCEPTED.md
reviews/fcop-4.0/decisions/WP4C-0B-SCOPE-CORRECTION.md
```

任务书 SHA、父链、冻结规范或阻断证据不匹配时，以 `INPUT_REF_MISMATCH` 停止。

## 3. 修正后的关系模块合同

### 3.1 唯一正式集合

`relations` 模块只解释并约束冻结规范 F4.5 中的四种正式关系：

| 字段 | 来源 | 最小语义 |
|---|---|---|
| `parent` | TASK → TASK | 委派／层级关系；不等于并发 Branch |
| `branch_of` | TASK → Root TASK | 并行 Branch 归属；最多一个 Root |
| `subject_ref` | REPORT/ISSUE/REVIEW → TASK 或 workspace | 证据或问题的正式主体 |
| `references` | 任意正式信封 → 已存在正式信封 | 一般引用；被 Gate 使用时必须可解析 |

关系强弱、基数、目标类型、解析失败和 Gate 引用规则必须逐字追溯冻结 EN/ZH F4.5，不得由旧规则文件反向改写。

### 3.2 与 convergence 的唯一分工

`relations` 负责：

- 四字段词汇、方向、目标类型、强弱、基数与解析；
- 普通任务层级和正式证据归属；
- 被其他模块使用的关系完整性。

`convergence` 负责：

- Branch family 的创建准入、深度和 Root 约束；
- Branch REPORT head；
- family digest；
- Root 显式汇合和 T7 门；
- Branch 重新打开后旧汇合失效。

同一冻结条款只能有一个 primary module。交叉引用不得复制规范义务。若需细分 F4.5 子条款，必须在决策报告中给出唯一 primary mapping。

### 3.3 旧关系名处置

必须依据 WP4C.0 的 147/147 rule disposition 和真实 3.x 文件逐项记录 `blocks`、`relates_to`、`supersedes` 的来源与去向。允许的 disposition 仅为真实证据支持的：

```text
LEGACY_V3_ONLY
PROFILE
DOCUMENTARY
NOT_PRESENT
```

无论处置为何，均不得：

- 放入 v4 Base Core relations；
- 映射为四个 Core 字段的别名；
- 通过兼容解析静默获得 v4 Gate 语义；
- 写入 v4 canonical module 的规范性字段表。

## 4. 修正后的装配合同

### 4.1 普通顺序任务最小装配

普通顺序任务必须包含 `relations`，因为 `parent`、`subject_ref` 和 `references` 并非并发专属能力。

顺序装配不得包含 `convergence`，也不得因此启用 Branch family、family digest 或 T7 汇合。

`relations` 中存在 `branch_of` 的字段定义，仅表示协议词汇可验证；不代表顺序 profile 自动启用 Branch 操作。

### 4.2 并行 Branch family 最小装配

并行装配严格定义为：

```text
普通顺序任务最小装配
+ convergence
```

不得再写成“顺序最小集 + relations + convergence”，因为 `relations` 已属于共同基础。

### 4.3 FCoP 仓库开发装配

原 WP4C.1 第 5.3 节继续有效。CodeFlowMu 的 `Agent原生软件工程宪法-v1.0-rc.1` 仍是 CodeFlowMu 当前开发的过渡材料，不得进入 FCoP Rule Package、FCoP repository development guidance 或 Host projection。

## 5. 必须完成的原 WP4C.1 工作

除本文明确替代的两处内容外，必须完整执行原任务书第 2–14 节，包括：

- 双语 rule-distribution contract；
- 73/73 冻结规范条款唯一 primary module 映射；
- 147/147 legacy rule disposition；
- 86/86 路径 future owner；
- 12/12 Host/消费者策略；
- Manifest、workspace adoption receipt、Host profile 三类合同分离；
- 3/3 最小装配；
- 3.x/4.0 隔离；
- Host 薄投影和 MCP 只读边界；
- WP4C.2–WP4C.6 的单一职责与独立 Gate；
- CodeFlowMu 过渡 RC 排除。

不得用本次四字段裁决替代其余审计和合同工作。

## 6. 交付文件与阻断历史

只允许新增或修改：

```text
docs/fcop-4.0/rule-distribution-contract.md
docs/fcop-4.0/rule-distribution-contract.zh.md
reports/FCOP-4.0-WP4C.1-CONTRACT-DECISIONS.md
reports/FCOP-4.0-WP4C.1-CONFORMANCE-MATRIX.md
reports/FCOP-4.0-WP4C.1-RESULT.md
reviews/fcop-4.0/wp4c.1/MANIFEST.md
```

既有 BLOCKED 交付不得从 Git 历史删除。三份报告和 Manifest 的最终版本必须保留“Previous blocked run”记录，至少列出：

```yaml
PREVIOUS_STATUS: BLOCKED
PREVIOUS_STOP_CODE: TASKBOOK_RELATION_SET_CONFLICT
PREVIOUS_CONTENT_COMMIT: 741b1829283f6a7fc1023e0edd8176b58c63ded4
PREVIOUS_MANIFEST_COMMIT: d92c72620757cea455aa24b5d635cc12f1e8b16a
ADMIN_CORRECTION: WP4C.1a
```

不得把原阻断改写为“从未发生”。

## 7. 验证要求

除原 WP4C.1 第 11 节外，必须增加以下机器可核验检查：

1. EN/ZH 合同的 Core relation set 均精确等于四字段集合；
2. 全部 v4 Base Core 模块表中不存在 `blocks`、`relates_to`、`supersedes`；
3. 三个旧名均有基于真实来源的 disposition；
4. 顺序装配包含 `relations` 且不包含 `convergence`；
5. 并行装配相对顺序装配只增加 `convergence`；
6. `relations` 与 `convergence` 的 primary clause mapping 无重复；
7. 73/73 条款仍恰好各有一个 primary module；
8. CodeFlowMu RC 排除状态保持不变；
9. UTF-8/LF、无 BOM、表格列数、链接、`git diff --check` 和六文件 allowlist 全部通过。

本轮仍不运行规则生成器，不修改测试，也不要求产品回归。

## 8. 强制停止条件

出现下列任一情况必须停止并只交付事实报告：

- 需要修改冻结 EN/ZH Specification；
- 四字段集合无法满足合同；
- 需要把旧关系名当作 v4 Core 别名；
- 顺序装配必须加载 convergence 才能成立；
- 某冻结条款无法获得唯一 primary module；
- 需要修改六文件以外内容；
- CodeFlowMu RC 被作为 FCoP 输入；
- 中英文合同无法语义对齐；
- 任何 P0 未关闭。

停止时不得请求 Gate，不得进入 WP4C.2。

## 9. GitHub-only 交付

使用新分支：

```text
review/fcop-4.0-wp4c.1a-rule-distribution-contract
```

创建新的 Draft PR；PR #18 作为阻断证据保留，不得改写或合并。

严格两提交：

1. Content commit：双语合同和三份报告；
2. Manifest commit：只更新 `reviews/fcop-4.0/wp4c.1/MANIFEST.md`。

随后必须 push、refetch，并在固定远端 Manifest HEAD 核验：

- 远端 HEAD；
- Content → 本任务书固定 commit 的直接父链；
- Manifest → Content 的直接父链；
- 6/6 文件 SHA-256；
- 工作树干净；
- main 未修改；
- CodeFlowMu 未修改。

聊天文本、本地路径、ZIP 或未推送 commit 均不构成交付。

## 10. 完成回执

```yaml
WP4C_1A_STATUS: COMPLETE | BLOCKED
AUTHORIZED_SCOPE: WP4C_1A_ONLY
TASKBOOK_COMMIT: ""
TASKBOOK_SHA256: ""
INPUT_HEAD: ""
PREVIOUS_BLOCKED_HEAD: d92c72620757cea455aa24b5d635cc12f1e8b16a
FROZEN_FCOP_CONTRACT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6

CORE_RELATION_SET: 4/4
LEGACY_RELATION_NAMES_DISPOSITION: 3/3
SEQUENTIAL_RELATIONS_INCLUDED: PASS
SEQUENTIAL_CONVERGENCE_EXCLUDED: PASS
PARALLEL_INCREMENT: CONVERGENCE_ONLY
RELATION_CONVERGENCE_PRIMARY_OVERLAP: 0

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
DIRECT_PARENT_CHAIN: PASS
DELIVERY_SHA256: 6/6
WORKTREE_STATUS: CLEAN

WP4C_1_RULE_DISTRIBUTION_CONTRACT_FROZEN: false
WP4C_2_STARTED: false
MAIN_MODIFIED: false
CODEFLOWMU_MODIFIED: false
REQUESTED_GATE: WP4C_1_RULE_DISTRIBUTION_CONTRACT_FROZEN
```

完成后强制停止。执行者不得自行签署 Gate。
