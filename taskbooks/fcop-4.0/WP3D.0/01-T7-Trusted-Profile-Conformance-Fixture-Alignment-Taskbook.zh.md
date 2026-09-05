---
title: FCoP 4.0 WP3D.0 T7可信Profile符合性夹具对齐任务书
document_role: EXECUTION_TASKBOOK
status: AUTHORIZED_FOR_WP3D_0_ONLY
execution_authorized: true
authorized_scope: WP3D_0_ONLY
input_head: e664fa39592b699637c1f0e6aeee229331b321e3
frozen_contract_commit: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
blocked_local_commit: 5e6b14b493f7b98bd5754ea862e1b6525e186a5e
wp3d_implementation_suspended: true
production_change_authorized: false
main_merge_authorized: false
release_authorized: false
requested_gate: WP3D_FIXTURE_ALIGNMENT_ACCEPTED
---

# FCoP 4.0 WP3D.0 T7可信Profile符合性夹具对齐任务书

## 0. 唯一授权

本任务只允许修正三个冻结成功测试的可信Profile初始化夹具，并把WP3D阻断证据交付GitHub。

修正对象：

- `C3-GATE-01[T7]`
- `C5-N02`
- `C5-ARCHIVED-01`

本任务不实现T7、convergence或family digest，不修改任何生产代码、冻结规范、Schema、MCP或CodeFlowMu。

原WP3D执行任务书在本修订期间暂停。完成后必须停止并请求：

```text
GATE: WP3D_FIXTURE_ALIGNMENT_ACCEPTED
```

未取得该Gate和后续重新发布的WP3D任务书，不得恢复WP3D实现。

## 1. 已确认的真实冲突

远端 `e664fa39592b699637c1f0e6aeee229331b321e3` 的真实代码显示：

1. `tests/conformance/v4/conftest.py` 的默认 `v4_driver` 是 `V4ConformanceDriver(workspace.root)`，可信注册表为空；
2. `C3-GATE-01` 只为T4/T5/T6创建带 `profile:test` evaluator的driver，T7退回默认driver；
3. `C5-N02` 使用默认driver提交Root T7；
4. `C5-ARCHIVED-01` 使用默认driver提交Branch T7；
5. 三个测试使用的Authorization REVIEW均声明 `profile_ref: profile:test`，工作区manifest也采用该Profile，但没有在可信Project初始化边界注册evaluator；
6. 冻结F4.7.4规定T4/T5/T6/T7没有可用已采用Authorization Profile时必须返回 `AUTHORIZATION_PROFILE_UNAVAILABLE`；
7. manifest字符串、REVIEW自声明、sender或actor都不能替代可信evaluator。

因此，三个节点若继续作为成功测试，必须显式建立与T4/T5/T6相同的可信测试Profile边界。生产实现不得绕过F4.7.4。

## 2. 固定输入与工作区

```yaml
REPOSITORY: joinwell52-AI/FCoP
INPUT_HEAD: e664fa39592b699637c1f0e6aeee229331b321e3
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
BLOCKED_LOCAL_COMMIT: 5e6b14b493f7b98bd5754ea862e1b6525e186a5e
TASKBOOK_BRANCH: task/fcop-4.0-wp3d.0-profile-fixture-alignment
EXPECTED_REVIEW_BRANCH: review/fcop-4.0-wp3d.0-profile-fixture-alignment
```

Codex必须从包含本文件的Taskbook Commit创建独立worktree，不得继续在原WP3D worktree直接修改。

建议：

```text
WORKTREE: D:\FCoP-wp3d0-profile-fixtures
BRANCH: review/fcop-4.0-wp3d.0-profile-fixture-alignment
```

开始前必须验证Taskbook Commit、文件SHA-256、INPUT_HEAD祖先、冻结规范摘要及“INPUT_HEAD到Taskbook Commit只新增本任务书”。

中文Markdown使用UTF-8、LF；不得使用PowerShell修改中文文件。

## 3. 唯一允许的夹具修正

### 3.1 `C3-GATE-01[T7]`

文件：

```text
tests/conformance/v4/test_c3_lifecycle.py
```

只允许把T7纳入现有显式可信driver选择：

```python
if edge in {"T4", "T5", "T6", "T7"}
```

T7使用：

```python
V4ConformanceDriver(
    workspace.root,
    trusted_profiles={
        "profile:test": DeterministicProfileEvaluator("AUTHORIZED")
    },
    test_id="C3-GATE-01",
)
```

不得改变T1–T6夹具、GATE_CASES、Test ID、missing twin、错误码断言、状态断言或Authorization内容。

### 3.2 `C5-N02`

文件：

```text
tests/conformance/v4/test_c5_convergence.py
```

为该测试创建局部可信driver，注册：

```python
{"profile:test": DeterministicProfileEvaluator("AUTHORIZED")}
```

该局部driver用于需要生产入口的本测试操作，尤其Root T7。可以继续用同一driver写convergence REVIEW，以减少混合对象，但不得改变测试的family、references、digest、Authorization或最终断言。

### 3.3 `C5-ARCHIVED-01`

在同一文件为该测试创建局部可信driver，注册同一确定性AUTHORIZED evaluator，并用于Branch T7以及该测试的family digest调用。

不得改变“Branch done→archive前后digest相同”的测试意图和断言。

### 3.4 导入

只允许在 `test_c5_convergence.py` 的既有fixtures导入中加入：

```python
DeterministicProfileEvaluator
```

不得新增另一种evaluator、修改 `fixtures.py` 或全局 `v4_driver` fixture。

## 4. 不得改变的合同与测试语义

- F4.7.4及中英文冻结规范不变；
- Profile evaluator仍只能通过 `Project(... trusted_profiles=...)` 初始化；
- 业务请求不得携带evaluator、resolver、registry或Host allowlist；
- Test ID仍为60/60，不改名、不复制；
- 不删断言、不放宽错误码、不增加skip/xfail；
- 不把默认 `v4_driver` 改成全局AUTHORIZED；
- 空Profile和无可信evaluator的负向测试必须继续Fail Closed；
- 三个节点在T7未实现期间仍可保持expected red；本任务不得伪造PASS；
- 修订的验收标准是“成功夹具已具备可信初始化条件”，不是“T7行为已经完成”。

## 5. 阻断证据的GitHub收口

本地提交 `5e6b14b493f7b98bd5754ea862e1b6525e186a5e` 仅作为待转存证据，不是执行基线。

若该提交在本机仍可读取，允许逐文件复制以下四份报告到新worktree；不得cherry-pick整个提交：

```text
reports/FCOP-4.0-WP3D-BLOCKED.md
reports/FCOP-4.0-WP3D-FAMILY-MODEL.md
reports/FCOP-4.0-WP3D-IMPLEMENTATION-PLAN.md
reports/FCOP-4.0-WP3D-TARGET-NODE-BASELINE.md
```

若本地提交不可读取，必须从INPUT_HEAD重新运行15节点基线并重新生成等价报告，注明 `LOCAL_BLOCKED_COMMIT_UNAVAILABLE_REPRODUCED`。

报告必须保留真实结论：

```yaml
WP3D_STATUS: BLOCKED
STOP_CODE: FROZEN_CONFORMANCE_CONTRACT_CONFLICT
PRODUCTION_CODE_CHANGED: false
WP3D_CONVERGENCE_ACCEPTED_REQUESTED: false
```

不得把WP3D.0夹具修正写成WP3D实现完成。

另新增：

```text
reports/FCOP-4.0-WP3D.0-FIXTURE-ALIGNMENT.md
reports/FCOP-4.0-WP3D.0-RESULT.md
```

## 6. 允许修改文件

仅允许：

```text
tests/conformance/v4/test_c3_lifecycle.py
tests/conformance/v4/test_c5_convergence.py

reports/FCOP-4.0-WP3D-BLOCKED.md
reports/FCOP-4.0-WP3D-FAMILY-MODEL.md
reports/FCOP-4.0-WP3D-IMPLEMENTATION-PLAN.md
reports/FCOP-4.0-WP3D-TARGET-NODE-BASELINE.md
reports/FCOP-4.0-WP3D.0-FIXTURE-ALIGNMENT.md
reports/FCOP-4.0-WP3D.0-RESULT.md

reviews/fcop-4.0/wp3d.0/MANIFEST.md
```

前四份WP3D报告只允许从本地阻断提交原样转存或重新生成，不得借机改写合同。

## 7. 明确禁止

禁止修改：

```text
src/**
mcp/**
schemas/**
spec/fcop-4.0-spec.md
spec/fcop-4.0-spec.zh.md
tests/conformance/v4/conftest.py
tests/conformance/v4/driver.py
tests/conformance/v4/fixtures.py
taskbooks/**
CodeFlowMu/**
```

同时禁止：

- 修改全局fixture使所有测试默认AUTHORIZED；
- 信任manifest、REVIEW sender、actor或自声明proof；
- 修改Authorization生产实现；
- 实现T7、family digest或convergence；
- 修改31个Base错误码；
- 新增公共API、生产模块、依赖、数据库、索引、锁或后台组件；
- 合并main、创建tag/Release或上传PyPI；
- 进入WP3D实现、WP3E或WP4。

如果只改两个测试文件不能消除夹具冲突，必须停止：`FIXTURE_ALIGNMENT_BLOCKED`。

## 8. 验证要求

必须记录真实命令和结果：

1. 对INPUT_HEAD运行15个WP3D目标节点，复现0 passed / 15 failed或如实记录差异；
2. 静态证明三个成功节点原先使用空可信registry；
3. 修改后证明三个节点都通过局部 `Project(trusted_profiles=...)` 初始化；
4. `C3-GATE-01[T4/T5/T6]`继续通过；
5. Profile unavailable、DENIED、UNKNOWN、caller-smuggling负向测试继续通过；
6. 三个T7节点若仍因T7未实现失败，必须记为 `EXPECTED_RED_IMPLEMENTATION_ABSENT`，不能算夹具修订失败；
7. 运行全部v4 static/meta与behavioral，除既有deferred外不得出现新失败；
8. 运行 `tests/test_fcop` 与隔离MCP回归；
9. 冻结Test ID数量和名称60/60不变；
10. `git diff --check`、UTF-8/LF及文件allowlist通过；
11. 生产文件、规范、Schema、MCP和CodeFlowMu修改数为0。

必须形成：

```yaml
CONFLICTING_SUCCESS_NODES: 3/3 ALIGNED
TRUSTED_PROFILE_LOCAL_FIXTURES: 3/3
GLOBAL_V4_DRIVER_MODIFIED: false
FROZEN_TEST_IDS: 60/60
ASSERTIONS_REMOVED: 0
SKIP_XFAIL_ADDED: 0
PRODUCTION_FILES_MODIFIED: 0
UNEXPECTED_FAILURES: 0
```

## 9. GitHub交付

必须使用两提交：

1. Content Commit：两个测试夹具修正、六份报告；
2. Manifest Commit：只新增 `reviews/fcop-4.0/wp3d.0/MANIFEST.md`。

提交链：

```text
Taskbook Commit → Content Commit → Manifest Commit
```

推送后重新fetch并验证：

- remote HEAD等于Manifest Commit；
- Content是Manifest直接父提交；
- Taskbook是Content直接父提交；
- Content不修改taskbooks；
- Manifest Commit只新增一个Manifest；
- 9个允许交付文件逐项SHA-256匹配；若四份阻断报告合并为更少文件，必须解释且总范围不得扩大；
- remote main未改变；
- worktree干净。

不force push，不自动开/合并PR。

## 10. 完成与停止

只有全部条件满足才可声明：

```yaml
WP3D_0_STATUS: COMPLETE
AUTHORIZED_SCOPE: WP3D_0_ONLY
INPUT_HEAD: e664fa39592b699637c1f0e6aeee229331b321e3
BLOCKED_LOCAL_COMMIT: 5e6b14b493f7b98bd5754ea862e1b6525e186a5e

CONFLICTING_SUCCESS_NODES: 3/3
TRUSTED_PROFILE_LOCAL_FIXTURES: 3/3
GLOBAL_V4_DRIVER_MODIFIED: false
FROZEN_TEST_IDS: 60/60
ASSERTIONS_REMOVED: 0
SKIP_XFAIL_ADDED: 0
PRODUCTION_FILES_MODIFIED: 0
FROZEN_SPEC_FILES_MODIFIED: 0
SCHEMA_FILES_MODIFIED: 0
MCP_IMPLEMENTATION_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0
UNEXPECTED_FAILURES: 0

CONTENT_COMMIT: <sha>
MANIFEST_COMMIT: <sha>
REMOTE_HEAD: <sha>
REMOTE_PUSHED: true | false
REMOTE_REFETCH_VERIFIED: PASS | FAIL
DELIVERY_SHA256: <matched>/<total>

WP3D_IMPLEMENTATION_SUSPENDED: true
WP3D_CONVERGENCE_ACCEPTED: false
WP3E_STARTED: false
WP4_STARTED: false
MAIN_MODIFIED: false
RELEASE_CREATED: false
REQUESTED_GATE: WP3D_FIXTURE_ALIGNMENT_ACCEPTED
```

完成后立即停止。ADMIN审核并签署 `WP3D_FIXTURE_ALIGNMENT_ACCEPTED` 后，必须另发以WP3D.0 remote head为输入的新WP3D执行任务书；不得直接恢复旧任务书。
