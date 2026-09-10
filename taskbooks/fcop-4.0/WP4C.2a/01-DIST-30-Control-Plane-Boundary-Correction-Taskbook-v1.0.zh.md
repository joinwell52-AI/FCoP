---
title: "FCoP 4.0 WP4C.2a：DIST-30 控制面边界修正与 WP4C.2 恢复任务书"
document_id: "FCOP-4.0-WP4C.2A-TASKBOOK"
version: "1.0"
date: "2026-09-07"
status: "AUTHORIZED_FOR_WP4C_2A_ONLY"
document_role: "EXECUTION_TASKBOOK"
authority: "ADMIN"
execution_authorized: true
authorized_scope: "WP4C_2A_ONLY"
implementation_authorized: false
conformance_implementation_authorized: true
main_merge_authorized: false
release_authorized: false
resumes_stage: "WP4C.2"
blocked_reason: "DIST30_EXECUTION_BOUNDARY_CONFLICT"
superseded_taskbook_commit: "17ef3704c66f7c0113d3159f2e4ec4f7d4f00ee4"
parent_gate: "WP4C_1_RULE_DISTRIBUTION_CONTRACT_FROZEN"
parent_gate_commit: "b5afdb8a2fb2e70620f15128bdeb772e071e7b43"
accepted_contract_head: "f6831de12991010f22672fb6e776ce85ef1507ff"
frozen_fcop_contract_commit: "aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6"
requested_gate: "WP4C_2_DISTRIBUTION_CONFORMANCE_ACCEPTED"
---

# FCoP 4.0 WP4C.2a：DIST-30 控制面边界修正与 WP4C.2 恢复任务书

## 0. ADMIN 裁决

WP4C.2 的停止行为正确。冲突来自 WP4C.2 任务书把 DIST-01–30 一律要求通过生产入口执行，并要求所有 Test ID 的 future owner 位于 WP4C.3–6；冻结 Matrix 对 DIST-30 的定义并非如此。

ADMIN 作出以下唯一裁决：

```yaml
DIST_01_29_CLASS: PRODUCTION_BEHAVIOR_CONFORMANCE
DIST_01_29_DRIVER_REQUIRED: true
DIST_01_29_FUTURE_OWNER: AS_FROZEN_MATRIX

DIST_30_CLASS: CONTROL_PLANE_CONFORMANCE
DIST_30_PRODUCTION_DRIVER_REQUIRED: false
DIST_30_PRODUCTION_API_REQUIRED: false
DIST_30_GATE_EXECUTOR_REQUIRED: false
DIST_30_OWNER: WP4C.2
DIST_30_EXPECTED_CURRENT_RESULT: PASS

TOTAL_TEST_IDS: 30
PRODUCTION_BEHAVIOR_IDS: 29
CONTROL_PLANE_IDS: 1
```

冻结合同与 WP4C.1 Matrix 不修改。原 WP4C.2 任务书中所有把 DIST-30 强制归入“真实生产入口、行为红灯或 WP4C.3–6 owner”的表述由本文替代，其余要求继续有效。

## 1. 唯一执行授权

本文是当前唯一允许执行的 WP4C.2a 任务书。

本轮允许：

1. 应用 DIST-30 控制面边界修正；
2. 保留并迁移当前 WP4C.2 已完成的合规测试与报告工作；
3. 恢复并完成原 WP4C.2 的 30/30 Test ID、红灯基线、回归、报告和 GitHub 交付。

本轮仍然只允许 Conformance 工作，不允许任何生产实现。

完成后必须停止并请求：

```text
WP4C_2_DISTRIBUTION_CONFORMANCE_ACCEPTED
```

没有该 Gate，不得进入 WP4C.3。

## 2. 固定输入

固定父链必须包含：

```yaml
WP4C_2_ORIGINAL_TASKBOOK: 17ef3704c66f7c0113d3159f2e4ec4f7d4f00ee4
WP4C_1_GATE_COMMIT: b5afdb8a2fb2e70620f15128bdeb772e071e7b43
ACCEPTED_CONTRACT_HEAD: f6831de12991010f22672fb6e776ce85ef1507ff
FROZEN_FCOP_4_SPEC: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
```

必须完整读取：

```text
taskbooks/fcop-4.0/WP4C.2/01-Distribution-Conformance-First-and-Red-Baseline-Taskbook-v1.0.zh.md
reports/FCOP-4.0-WP4C.1-CONFORMANCE-MATRIX.md
docs/fcop-4.0/rule-distribution-contract.md
docs/fcop-4.0/rule-distribution-contract.zh.md
reviews/fcop-4.0/gates/WP4C-1-RULE-DISTRIBUTION-CONTRACT-FROZEN.md
spec/fcop-4.0-spec.md
spec/fcop-4.0-spec.zh.md
```

必须核实 Matrix 中 DIST-30 的原文事实：

```text
Subject:
Missing next-stage authorization or unsatisfied Gate

Observable:
Stop; no tests/implementation/autocontinuation/merge/release
from this contract alone

Owner:
WP4C.2
```

任务书摘要、父链、Gate 或合同字节不一致时，以 `INPUT_REF_MISMATCH` 停止。

## 3. 当前未提交成果的保护与迁移

已知当前独立工作树：

```text
D:\FCoP-wp4c2-distribution-conformance
```

其中存在尚未提交的合规测试和三份报告。不得删除、覆盖或把它们误当成任务书分支内容。

正确处理：

1. 先记录旧工作树的分支、HEAD、修改文件清单和每个文件 SHA-256；
2. 验证所有修改均属于原 WP4C.2 十二个 Content allowlist 路径；
3. 从本文固定 taskbook commit 建立新的独立 worktree 和 review 分支；
4. 以字节保持方式把旧工作树的允许修改迁入新工作树；
5. 对迁移前后每个文件核对 SHA-256；
6. 旧工作树保持原样，直到新工作树迁移、测试和提交全部核验完成；
7. 最终 Content commit 必须直接以本文固定 taskbook commit 为父提交。

不得把未提交内容直接提交到旧 `17ef3704...` 父链后，再用 merge commit 拼接任务书。不得把任务书提交混入 Content commit。

如果发现旧工作树存在 allowlist 外修改，以 `WIP_SCOPE_DRIFT` 停止并保留现场。

## 4. DIST-30 的唯一测试合同

### 4.1 类型

DIST-30 是可执行的 repository/control-plane conformance test，不是 FCoP Core、Toolkit、MCP、Host adapter 或 Runtime 行为测试。

它可以保留在：

```text
tests/conformance/rule_distribution_v4/test_dist_25_30_failures_artifacts_context_gates.py
```

但不得调用 `RuleDistributionConformanceDriver`，不得解析或探测未来生产 API。

### 4.2 必须读取的仓库事实

DIST-30 只能读取固定测试工作树内已经提交的控制文件，例如：

```text
reviews/fcop-4.0/gates/WP4C-1-RULE-DISTRIBUTION-CONTRACT-FROZEN.md
taskbooks/fcop-4.0/WP4C.2/01-Distribution-Conformance-First-and-Red-Baseline-Taskbook-v1.0.zh.md
taskbooks/fcop-4.0/WP4C.2a/01-DIST-30-Control-Plane-Boundary-Correction-Taskbook-v1.0.zh.md
reviews/fcop-4.0/wp4c.1/MANIFEST.md
```

测试不得访问 GitHub 网络、用户工作区、CodeFlowMu 或外部 Gate 服务。

### 4.3 必须断言

DIST-30 至少断言：

1. `WP4C_1_RULE_DISTRIBUTION_CONTRACT_FROZEN` 已由固定 Gate 签署；
2. 当前唯一执行范围为 `WP4C_2A_ONLY`，只恢复 WP4C.2；
3. 当前输入中没有已签署的 `WP4C_2_DISTRIBUTION_CONFORMANCE_ACCEPTED`；
4. 当前输入中没有 `WP4C_3_ONLY` 执行授权；
5. WP4C.1 Gate 本身没有自动授权 WP4C.2；
6. WP4C.2/WP4C.2a 任务书没有自动授权 WP4C.3；
7. 缺少下一 Gate 时，允许的完成状态只能是停止并请求 Gate；
8. 本轮 diff 中没有生产实现、main merge、Tag、Release 或 CodeFlowMu 修改；
9. `WP4C_3_STARTED` 必须为 false；
10. 合同冻结、Conformance 接受、实现接受、main merge 与 release 不能互相推导。

这些是仓库中可观察的静态控制事实。不得创建“Gate 执行器”来证明它们。

### 4.4 当前结果

当以上事实成立时：

```yaml
TEST_ID: DIST-30
CLASSIFICATION: CONTROL_PLANE_PASS
PUBLIC_PRODUCTION_ENTRY: NOT_APPLICABLE
STRUCTURED_PRODUCTION_ERROR: NOT_APPLICABLE
ZERO_STAGE_ADVANCE: PASS
OWNER: WP4C.2
FUTURE_OWNER: NONE_CLOSED_BY_WP4C_2
```

DIST-30 当前通过不是 `UNEXPECTED_PASS`，也不是 `PREEXISTING_PASS`；它是本阶段应完成的控制面证明。

## 5. 对原 WP4C.2 统一要求的限定修正

原任务书继续要求 30/30 ID，但统计口径改为：

```yaml
DISTRIBUTION_TEST_IDS: 30/30
PRODUCTION_BEHAVIOR_IDS: 29/29
CONTROL_PLANE_IDS: 1/1
PRODUCTION_BEHAVIORAL_NODES: n
CONTROL_PLANE_NODES: 1
```

下列表述仅适用于 DIST-01–29：

- 每个 ID 至少一个真实 production behavioral node；
- 通过 test-only driver 调用真实生产边界；
- 缺少公开生产入口属于预期红灯；
- future owner 为 WP4C.3–WP4C.6；
- `PREEXISTING_PASS / EXPECTED_FAIL_NOT_IMPLEMENTED / EXPECTED_FAIL_CONTRACT_MISMATCH` 分类。

DIST-30 使用独立分类 `CONTROL_PLANE_PASS`，owner 固定为 WP4C.2。

Meta guard 必须明确知道这一例外，不能因为 DIST-30 没有生产调用而把它判为空壳。

## 6. 报告字段修正

### 6.1 CONFORMANCE PLAN

DIST-30 行必须记录：

```yaml
test_id: DIST-30
contract_ref: RD-24
matrix_owner: WP4C.2
test_class: CONTROL_PLANE_CONFORMANCE
driver_action: NOT_APPLICABLE
effect_boundary: STAGE_ADVANCE
expected_result: CONTROL_PLANE_PASS
future_owner: NONE_CLOSED_BY_WP4C_2
```

### 6.2 RED BASELINE

原逐 node 字段对 DIST-01–29 保持不变。

DIST-30 使用：

```yaml
test_id: DIST-30
node_id: ""
contract_ref: RD-24
command: ""
exit_status: 0
classification: CONTROL_PLANE_PASS
structured_error: NOT_APPLICABLE
public_entry: NOT_APPLICABLE_CONTROL_PLANE
effects_observed: ZERO_STAGE_ADVANCE
zero_write_verified: PASS
future_owner: NONE_CLOSED_BY_WP4C_2
```

### 6.3 RESULT

必须记录本次阻断历史：

```yaml
PREVIOUS_STATUS: BLOCKED
PREVIOUS_REASON: DIST30_EXECUTION_BOUNDARY_CONFLICT
PREVIOUS_REMOTE_COMMIT: NONE
ADMIN_CORRECTION: WP4C.2a
```

不得把这次正确停止改写为从未发生。

## 7. 其余测试边界不变

DIST-01–29 必须继续遵守原任务书：

- test-only driver 不实现生产行为；
- 不使用 mock、skip、xfail 或空测试；
- 所有 effectful 行为只在 pytest 临时目录；
- 竞态使用真实独立进程；
- 不访问真实 Host、网络或 CodeFlowMu；
- 不修改冻结 C0–C8 60 个 Test ID；
- 既有 FCoP、v4 Core 与 MCP 回归零新增失败；
- 预期红灯逐 node 记录；
- `UNEXPECTED_PASS=0`；
- `UNEXPECTED_FAILURE=0`。

已取得的回归数字 `FCoP 1256 / v4 119 / MCP 134` 只能作为本轮中途实况；完成交付前必须在新固定工作树重新运行并记录实际结果。

## 8. 允许文件与提交结构

文件 allowlist 与原任务书完全相同，共十三项：

```text
tests/conformance/rule_distribution_v4/__init__.py
tests/conformance/rule_distribution_v4/conftest.py
tests/conformance/rule_distribution_v4/driver.py
tests/conformance/rule_distribution_v4/test_dist_00_meta.py
tests/conformance/rule_distribution_v4/test_dist_01_06_manifest.py
tests/conformance/rule_distribution_v4/test_dist_07_12_profiles.py
tests/conformance/rule_distribution_v4/test_dist_13_20_projection.py
tests/conformance/rule_distribution_v4/test_dist_21_24_assembly_compat_mcp.py
tests/conformance/rule_distribution_v4/test_dist_25_30_failures_artifacts_context_gates.py
reports/FCOP-4.0-WP4C.2-CONFORMANCE-PLAN.md
reports/FCOP-4.0-WP4C.2-RED-BASELINE.md
reports/FCOP-4.0-WP4C.2-RESULT.md
reviews/fcop-4.0/wp4c.2/MANIFEST.md
```

严格两提交：

1. Content commit：前十二项；
2. Manifest commit：只新增最后一项。

除本文对 DIST-30 的限定修正外，原任务书第 4–14 节继续有效。

## 9. 强制停止条件

出现任一情况必须停止并只交付事实报告：

- 需要修改冻结 Specification、WP4C.1 合同或 Matrix；
- DIST-30 需要生产 API、Gate executor、Runtime、MCP 或 Host 才能通过；
- DIST-30 被归入 WP4C.3–6；
- DIST-30 通过被统计为意外绿灯；
- DIST-01–29 使用控制文档替代生产行为；
- 旧未提交成果迁移发生字节丢失或 allowlist 漂移；
- 需要修改十三项以外文件；
- 出现意外通过、意外失败或新增回归；
- 需要访问 CodeFlowMu、真实 Host、网络或 main；
- 任何 P0 未关闭。

公开生产入口不存在对 DIST-01–29 仍是预期红灯；对 DIST-30 不适用。

## 10. GitHub-only 交付

新 review 分支：

```text
review/fcop-4.0-wp4c.2a-distribution-conformance
```

从本文固定 taskbook commit 创建。创建新的 Draft PR；不得修改、合并或关闭 PR #18、PR #19。

push 后 refetch 并核验：

- Manifest → Content → 本任务书固定 commit 的直接父链；
- 13/13 交付文件 SHA-256；
- changed paths 精确十三项；
- 工作树干净；
- 旧工作树保留；
- 冻结合同、生产源码、MCP、Schema、Host、CodeFlowMu 与 main 未修改。

聊天回执、本地路径或未推送提交不构成交付。

## 11. 完成回执

```yaml
WP4C_2A_STATUS: COMPLETE | BLOCKED
AUTHORIZED_SCOPE: WP4C_2A_ONLY
TASKBOOK_COMMIT: ""
TASKBOOK_SHA256: ""
INPUT_HEAD: ""
ORIGINAL_WP4C_2_TASKBOOK: 17ef3704c66f7c0113d3159f2e4ec4f7d4f00ee4
PARENT_GATE_COMMIT: b5afdb8a2fb2e70620f15128bdeb772e071e7b43
ACCEPTED_CONTRACT_HEAD: f6831de12991010f22672fb6e776ce85ef1507ff

WIP_FILES_DISCOVERED: n
WIP_FILES_MIGRATED: n/n
WIP_SHA256_MATCH: n/n
OLD_WORKTREE_PRESERVED: PASS

DISTRIBUTION_TEST_IDS: 30/30
PRODUCTION_BEHAVIOR_IDS: 29/29
CONTROL_PLANE_IDS: 1/1
PRODUCTION_BEHAVIORAL_NODES: n
CONTROL_PLANE_NODES: 1
CONTROL_PLANE_PASS: 1
PREEXISTING_PASS: n
EXPECTED_FAIL_NOT_IMPLEMENTED: n
EXPECTED_FAIL_CONTRACT_MISMATCH: n
UNEXPECTED_PASS: 0
UNEXPECTED_FAILURE: 0
SKIP_XFAIL: 0
EMPTY_STUB_GUARD: PASS

FROZEN_CORE_TEST_IDS: 60/60_UNCHANGED
TEST_FCOP_REGRESSION: PASS
V4_CORE_CONFORMANCE: PASS
MCP_REGRESSION: PASS
PRODUCTION_FILES_MODIFIED: 0
SCHEMA_FILES_MODIFIED: 0
MCP_FILES_MODIFIED: 0
FROZEN_CONTRACT_FILES_MODIFIED: 0
HOST_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0

CONTENT_FILES: 12/12
TOTAL_DELIVERY_FILES: 13/13
CONTENT_COMMIT: ""
MANIFEST_COMMIT: ""
REMOTE_HEAD: ""
REMOTE_PUSHED: true
REMOTE_REFETCH_VERIFIED: PASS
DIRECT_PARENT_CHAIN: PASS
DELIVERY_SHA256: 13/13
WORKTREE_STATUS: CLEAN

WP4C_2_DISTRIBUTION_CONFORMANCE_ACCEPTED: false
WP4C_3_STARTED: false
MAIN_MODIFIED: false
RELEASE_CREATED: false
REQUESTED_GATE: WP4C_2_DISTRIBUTION_CONFORMANCE_ACCEPTED
```

完成后强制停止。不得自行签署 Gate，不得进入 WP4C.3。
