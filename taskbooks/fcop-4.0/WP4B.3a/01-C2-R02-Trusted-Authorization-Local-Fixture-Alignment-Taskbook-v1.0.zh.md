---
document_role: ADMIN_FIXTURE_ALIGNMENT_DECISION_AND_EXECUTION_TASKBOOK
title: FCoP 4.0 WP4B.3a C2-R02 可信授权局部夹具对齐任务书
version: 1.0
status: AUTHORIZED_FOR_FIXTURE_ALIGNMENT_AND_WP4B_RESUME
execution_authorized: true
authorized_scope: WP4B_RESUME_ONLY
input_head: 8a9312999788dd13c8c393ee403c8837130a0960
amends_taskbook_commit: 8a9312999788dd13c8c393ee403c8837130a0960
frozen_contract_commit: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
target_test_id: C2-R02
main_merge_authorized: false
release_authorized: false
wp4c_authorized: false
codeflowmu_change_authorized: false
---

# FCoP 4.0 WP4B.3a：C2-R02 可信授权局部夹具对齐任务书

## 0. ADMIN 裁决

允许补齐冻结 Conformance 测试 `C2-R02` 的局部夹具，使其满足 WP4B.3 已明确的授权事实追加前提：

```yaml
C2_R02_FIXTURE_ALIGNMENT_AUTHORIZED: true
TEST_ID_RENAME_AUTHORIZED: false
ASSERTION_REMOVAL_AUTHORIZED: false
GLOBAL_DRIVER_CHANGE_AUTHORIZED: false
PRODUCTION_BEHAVIOR_WEAKENING_AUTHORIZED: false
```

`C2-R02` 的原测试命题保持不变：

1. replacement REPORT 通过追加新事实纠正旧 REPORT；
2. 人工确认通过追加新 REVIEW 表达，不修改旧 REVIEW；
3. 新事实引用旧事实；
4. 旧 REPORT 与旧 REVIEW 的完整字节保持一致。

可信 Profile、授权迁移边、attempt、签发与失效时间、issuer proof 是授权追加成功的冻结前置条件。补齐这些输入属于测试安排修正，不是改变预期结果、弱化安全边界或修改冻结规范。

## 1. 唯一允许修改的既有测试

只允许修改承载 `C2-R02` 的测试文件中该测试函数的 Arrange/Act 局部夹具与输入。

必须保留：

- Test ID `C2-R02`；
- 原 clause 标识 `F4.3.3; F4.3.5`；
- 原 replacement REPORT 行为；
- 原 `mark_human_approved` 真实生产入口；
- 旧 REPORT 字节不变断言；
- 旧 REVIEW 字节不变断言；
- 新 REPORT ID 不等于旧 ID；
- 新 REVIEW ID 不等于旧 ID；
- 新 REPORT 引用旧 REPORT；
- 新 REVIEW 引用旧 REVIEW；
- 不得增加 skip、xfail、条件跳过或平台过滤。

只允许增加为满足 WP4B.3 所必需的局部安排和参数。

## 2. 局部可信 Profile

`C2-R02` 必须在测试函数内部或仅供该测试使用的局部 fixture 中创建：

```python
evaluator = DeterministicProfileEvaluator("AUTHORIZED")
local_driver = V4ConformanceDriver(
    workspace.root,
    trusted_profiles={"profile:test": evaluator},
    test_id="C2-R02",
)
```

以上为语义示意；可按现有测试工具的真实名称等价实现。

要求：

- Profile 必须已经存在于 workspace manifest 的 adopted `profiles`；
- evaluator 只能经 `Project(..., trusted_profiles=...)` 的可信初始化边界注册；
- 不得写入 TASK、REPORT、REVIEW、manifest 或工具参数；
- 不得修改全局 `v4_driver` fixture；
- 不得修改 `tests/conformance/v4/conftest.py` 的默认空 registry 行为；
- 不得修改 `V4ConformanceDriver` 让所有测试默认取得权限；
- 必须新增 evaluator 被生产入口真实调用且参数正确的断言。

## 3. 完整授权追加输入

对 `mark_human_approved` 的调用补齐 WP4B.3 固定的正式信息：

- 已采用 `profile_ref`；
- 合法且与测试 TASK/旧 REVIEW 一致的单条 T4–T7 授权边；
- 对应当前轮次的 `attempt_id`，或冻结合同明确允许的 null；
- `family_digest` 的有无符合所选 edge；
- 有时区 `issued_at`；
- 合法、尚未过期的 `expires_at`，或合同允许的 null；
- 有效 `issuer_proof`；
- 肯定 decision，保存后为 `review_kind: authorization`、`decision: authorize`；
- `review_id` 仍为原 `REVIEW-C2-OLD`。

所选 edge 必须与局部 TASK 当前状态和 attempt 一致。允许只在 `C2-R02` Arrange 中补齐该 TASK 的合法 source stage/transition history，以便生产入口证明绑定；不得减少旧事实不可变性断言，也不得通过直接写入目标 authorization REVIEW 绕过公共方法。

`workspace_id`、`subject_ref`、`references: [REVIEW-C2-OLD]`、`operation_kind: lifecycle_transition` 与 `authorization_scope: single_use` 应继续由 WP4B.3 的公共方法固定或从旧事实派生，不得在测试中夹带 evaluator 或预判结论。

## 4. 新增断言

在不删除任何原断言的基础上，至少增加：

```yaml
PROFILE_EVALUATOR_CALLS: 1
PROFILE_EVALUATOR_RESULT: AUTHORIZED
NEW_REVIEW_KIND: authorization
NEW_REVIEW_DECISION: authorize
NEW_REVIEW_PROFILE_REF: profile:test
NEW_REVIEW_TRANSITION_BINDING: MATCH
NEW_REVIEW_ATTEMPT_BINDING: MATCH
NEW_REVIEW_TIME_BINDING: VALID
NEW_REVIEW_REFERENCES_OLD: true
TASK_MOVED_BY_MARK: false
OLD_REPORT_BYTES_UNCHANGED: true
OLD_REVIEW_BYTES_UNCHANGED: true
```

本测试只验证授权事实追加与不可变性，不得把随后执行生命周期迁移加入 `C2-R02` 作为成功条件；消费时再次验证由 WP4B.3 的独立测试负责。

## 5. 禁止事项

- 改名或删除 `C2-R02`；
- 修改它的成功预期为拒绝；
- 删除或放宽任何旧字节、ID、引用断言；
- 使用 mock/monkeypatch 绕过生产 `Project.mark_human_approved`；
- 从业务请求传入 evaluator、registry、policy 或 `AUTHORIZED` 结论；
- 把 evaluator 注册进全局 driver；
- 让 `profiles: []` 自动拥有授权能力；
- 将 Profile `DENIED`/`UNKNOWN` 改为允许追加；
- 修改冻结规范、Schema、其他冻结 Test ID；
- 修改 CodeFlowMu、main 或发布。

## 6. 验证要求

修改后必须至少执行并报告：

1. `C2-R02` 单节点通过；
2. C2 文件全部节点通过；
3. WP4B.3 授权追加定向测试通过；
4. REPORT 查询 68 项回归继续通过；
5. v4 frozen Conformance `119/119`；
6. WP3E v4 单元测试；
7. 全量 `tests/test_fcop`；
8. 全量隔离 MCP；
9. FastMCP 真实 Client 授权追加与 T1–T7；
10. Ruff、mypy、打包、clean install；
11. 最终 Manifest HEAD 的 GitHub required CI 全绿。

必须报告：

```yaml
C2_R02_TEST_ID_UNCHANGED: true
C2_R02_ORIGINAL_ASSERTIONS_PRESERVED: PASS
C2_R02_TRUSTED_PROFILE_LOCAL_ONLY: PASS
GLOBAL_V4_DRIVER_MODIFIED: false
CALLER_AUTHORITY_FIELDS_ADDED: 0
SKIP_XFAIL_ADDED: 0
OTHER_FROZEN_TESTS_MODIFIED: 0
```

## 7. 正在运行的回归与脏工作树

本任务书发布时，WP4B 独立工作树可能仍在运行完整回归并保留未提交实现。不得为读取本文件中断已运行的安全只读测试，也不得 reset、checkout、clean 或覆盖工作树。

执行者应：

1. 先让当前回归完成并保存真实结果；
2. 直接从 GitHub 固定提交读取并核验本任务书；
3. 保存当前差异清单；
4. 仅追加本文件允许的局部 fixture 修正；
5. 在最终 Content Commit 前确保本任务书提交位于交付父链；
6. 重新运行受影响测试及第 6 节完整验证。

旧回归结果可以作为诊断证据，但不能替代修正后的最终验证。

## 8. GitHub 交付与停止点

继续使用：

- 分支：`review/fcop-4.0-wp4b-mcp-adapter`
- Draft PR：[PR #15](https://github.com/joinwell52-AI/FCoP/pull/15)

本修正不单独请求中间 Gate。完成局部夹具对齐后，继续完成 WP4B.3 及整个 WP4B。

最终成功后停止，只请求：

```yaml
REQUESTED_GATE: WP4B_MCP_ADAPTER_ACCEPTED
```

失败则保留证据并报告：

```yaml
WP4B_STATUS: BLOCKED
REQUESTED_GATE: NONE
```

## 9. 本任务书不授权

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
