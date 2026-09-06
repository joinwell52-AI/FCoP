---
stage: WP3E.0
document_role: EXECUTION_TASKBOOK
status: AUTHORIZED_FOR_WP3E_0_ONLY
execution_authorized: true
authorized_scope: WP3E_0_ONLY
contract_frozen: true
implementation_authorized: true
main_merge_authorized: false
release_authorized: false
---

# FCoP 4.0 WP3E.0：C6-X01 可信 Profile 夹具对齐与 Core 收口恢复任务书 v1.0

## 0. ADMIN 决定

本任务书确认 WP3E 的停止是正确行为。

冻结规范 F4.7.4 要求 T4/T5/T6/T7 必须由可信初始化边界注册的 Profile evaluator 判断授权。冻结测试 `C6-X01` 当前使用默认 `v4_driver`，而默认 fixture 通过 `V4ConformanceDriver(workspace.root)` 创建，可信 Profile 注册表为空；测试却要求 T7 成功。这是测试夹具与冻结合同不一致，不是允许生产实现 Fail Open 的理由。

本任务书只开放一个极窄的冻结 Conformance 例外：为 `C6-X01` 注册测试内局部、确定性的 `AUTHORIZED` evaluator。该修正验证后，Codex 在同一任务内直接恢复原 WP3E 的 23 节点 Core 收口，不再等待中间 Gate。

本授权不修改冻结合同，不降低授权边界，不授权 WP4，不授权 main 合并或发布。

## 1. 固定输入

```yaml
REPOSITORY: joinwell52-AI/FCoP
TASKBOOK_BASE_COMMIT: 19285e5a22142c3e0331803f85b1776b533d9339
ORIGINAL_WP3E_TASKBOOK: taskbooks/fcop-4.0/WP3E/01-Remaining-Core-Recovery-and-Conformance-Closeout-Taskbook-v1.0.zh.md
ORIGINAL_WP3E_TASKBOOK_COMMIT: 19285e5a22142c3e0331803f85b1776b533d9339
WP3D_GATE_COMMIT: 99d0ab14a8e4e3b5d8580230a9df1d6dbec50b41
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
BLOCKED_LOCAL_REPORT_COMMIT: dfc2063b8e735aa38ca42dc47edf4ceb975876bf
BLOCKED_LOCAL_REPORT_ROLE: OPTIONAL_READ_ONLY_EVIDENCE
```

执行前必须验证：

1. 当前任务书 Commit 的直接父提交是 `19285e5a22142c3e0331803f85b1776b533d9339`；
2. 原 WP3E 任务书、WP3D Gate 与冻结中英文规范可由当前任务书 Commit 到达；
3. `tests/conformance/v4/test_c6_authorization.py` 中 `C6-X01` 仍接受默认 `v4_driver`；
4. `tests/conformance/v4/conftest.py` 中默认 `v4_driver` 仍没有可信 Profile 注册；
5. F4.7.4 仍要求无可用 Profile 时返回 `AUTHORIZATION_PROFILE_UNAVAILABLE`；
6. 原 `D:\FCoP` 不得被切分支、清理或覆盖。

任一身份不符，停止并报告 `INPUT_IDENTITY_MISMATCH`。

## 2. 工作树与分支

必须从本任务书固定 Commit 新建干净独立 worktree：

```text
D:\FCoP-wp3e0-c6-alignment-resume
```

执行 review 分支固定为：

```text
review/fcop-4.0-wp3e.0-core-closeout
```

禁止以本地阻断提交 `dfc2063...` 作为代码基线或整体 cherry-pick。该提交只可读取两份阻断报告以核对事实；其中没有保留的生产实现，不得把本地现场误当成权威输入。

若源工作区不干净，保留原现场并使用独立 worktree；不得 stash、reset、clean 或覆盖用户文件。

## 3. 授权范围

WP3E.0 只有两个连续阶段：

| 阶段 | 授权 | 是否需要中间 Gate |
|---|---|---|
| A | 只修正 `C6-X01` 的可信 Profile 测试初始化 | 否 |
| B | 按原 WP3E 任务书完成剩余 Core、Recovery 与 23/23 Conformance | 否 |

阶段 A 验证通过后立即进入阶段 B。只有最终达到 WP3E 完成门，才请求 `FCOP_4_CORE_IMPLEMENTATION_ACCEPTED`。

原 WP3E 任务书的架构预算、生产文件 allowlist、测试要求、23 个目标节点、恢复五状态、Fault 边界、Cold export、禁止项和最终 Gate 全部继续有效。

本任务书仅覆盖原 WP3E 第 7 节中“不得修改冻结 Conformance”的一项禁令，而且只允许第 4 节定义的精确夹具修正。其他冻结文件仍只读。

## 4. 阶段 A：唯一允许的 Conformance 修正

唯一允许修改：

```text
tests/conformance/v4/test_c6_authorization.py
```

唯一允许修改的测试：

```text
test_c6_x01
```

必须采用测试内局部可信初始化，语义等价于：

```python
def test_c6_x01(workspace: WorkspaceFixture) -> None:
    ...
    trusted_driver = V4ConformanceDriver(
        workspace.root,
        trusted_profiles={
            "profile:test": DeterministicProfileEvaluator("AUTHORIZED")
        },
        test_id="C6-X01",
    )
```

并将该测试内原来对 fixture 参数 `v4_driver` 的调用改为 `trusted_driver`：

- `inject_fault(...)`
- 首次 `transition(...)`
- 精确重试 `transition(...)`

必须保持不变：

- Test ID `C6-X01`；
- clause `F4.7.3; F4.9.11`；
- TASK、REVIEW、operation、fault stage 与请求字段；
- `RESPONSE_LOST` 和 `once=True`；
- 所有既有断言；
- T7 仍要求正式 authorization REVIEW；
- 丢响应后的 exact retry 仍要求 `existing is True`；
- 单次 transition event 与单次授权消费语义；
- 默认 `v4_driver` fixture；
- 全局 driver、fixtures 与生产授权逻辑。

禁止：

- 将 evaluator、registry、resolver 或 `AUTHORIZED` 结果放入业务请求；
- 修改 `authorization_fixture` 以默认授权其他测试；
- 将默认 `v4_driver` 改成全局可信；
- 接受 manifest、actor、Host allowlist 或 REVIEW 自声明为可信裁判；
- 删除、放宽、重命名断言；
- 添加 skip、xfail 或条件跳过；
- 修改任何其他冻结 Conformance 文件。

## 5. 阶段 A 验证门

编码前记录原始 `C6-X01` 失败为 `AUTHORIZATION_PROFILE_UNAVAILABLE` 或记录其最早阻断点，并证明默认 driver 可信注册表为空。

夹具修正后必须满足：

```yaml
C6_X01_TRUSTED_PROJECT_INITIALIZATION: PASS
CALLER_AUTHORITY_FIELDS_ADDED: 0
GLOBAL_V4_DRIVER_MODIFIED: false
TEST_ID_RENAMED: 0
ASSERTIONS_REMOVED: 0
SKIP_XFAIL_ADDED: 0
OTHER_CONFORMANCE_FILES_MODIFIED: 0
```

在阶段 B 的 `inject_fault` 尚未实现时，`C6-X01` 可以继续因明确的 WP3E 能力缺失而红；但不得再因 Profile unavailable 或 caller-smuggled authority 失败。

至少运行并记录：

1. `C6-X01`；
2. `C6-N01`；
3. DENIED/UNKNOWN Profile 测试；
4. caller authority smuggling 四种攻击；
5. `C6-PROFILE-01` 空 Profile Fail Closed；
6. 整个 `test_c6_authorization.py`。

若修正需要超出上述唯一文件或改变合同断言，停止并报告 `FIXTURE_ALIGNMENT_SCOPE_EXCEEDED`，不得进入阶段 B。

## 6. 阶段 B：恢复 WP3E

阶段 A 通过后，继续严格执行原 WP3E 任务书的实现范围，完成全部 23 个 deferred 行为节点：

- C3-X01；
- C4-R01 dangling gate reference；
- C6-X01；
- C7-CREATE-01；
- C8-X01 四个 stage；
- C8-X03 三个 case；
- C8-STATE-01 五个 state；
- C8-INDETERMINATE-01；
- AT-05 三个 stage；
- AT-06 三个 state。

不得只实现 22 个“无冲突节点”后停止；阶段 A 已消除 C6-X01 的夹具冲突，最终目标仍是 23/23。

公共面预算保持：

```yaml
MAX_NEW_PUBLIC_TOOLKIT_APIS: 3
ALLOWED_PUBLIC_APIS:
  - Project.recover_operation
  - Project.inject_fault
  - Project.export_archive
MAX_NEW_PRODUCTION_MODULES: 1
OPTIONAL_NEW_MODULE: src/fcop/v4/recovery.py
NEW_RUNTIME_DEPENDENCIES: 0
NEW_BACKGROUND_COMPONENTS: 0
NEW_AUTHORITATIVE_STORES: 0
NEW_OPERATIONS_DIRECTORIES: 0
NEW_STATE_MACHINES: 0
NEW_LOCK_SYSTEMS: 0
NEW_BASE_ERROR_CODES: 0
```

必须复用既有 receipt、lifecycle、encoding 和文件原语。禁止数据库、第二 NOW truth、第二 journal、后台 recovery controller、daemon、watcher、timer、scheduler、queue 或自动裁决器。

## 7. 允许文件

除阶段 A 唯一冻结测试文件外，阶段 B 允许范围与原 WP3E 一致：

```text
src/fcop/project.py
src/fcop/v4/boundary.py
src/fcop/v4/creation.py
src/fcop/v4/lifecycle.py
src/fcop/v4/receipts.py
src/fcop/v4/encoding.py
src/fcop/v4/recovery.py

tests/test_fcop/test_v4_boundary.py
tests/test_fcop/test_v4_creation.py
tests/test_fcop/test_v4_lifecycle.py
tests/test_fcop/test_v4_recovery.py
tests/test_fcop/snapshots/public_surface.json
CHANGELOG.md

tests/conformance/v4/test_c6_authorization.py
```

证据交付：

```text
reports/FCOP-4.0-WP3E.0-C6-X01-FIXTURE-ALIGNMENT.md
reports/FCOP-4.0-WP3E-IMPLEMENTABILITY-AND-RED-BASELINE.md
reports/FCOP-4.0-WP3E-RECOVERY-STATE-PROOF.md
reports/FCOP-4.0-WP3E-FAULT-BOUNDARY-PROOF.md
reports/FCOP-4.0-WP3E-COLD-EXPORT-PROOF.md
reports/FCOP-4.0-WP3E-CONFORMANCE-CLOSEOUT.md
reports/FCOP-4.0-WP3E-RESULT.md
reviews/fcop-4.0/wp3e.0/MANIFEST.md
```

需要清单外文件时必须停止，不得先改后解释。

## 8. 冻结与禁止范围

仍然严格禁止：

- 修改中英文 FCoP 4.0 规范、Schema 或 31 个 Base error codes；
- 修改除 `test_c6_x01` 外的任何冻结 Conformance 内容；
- 修改 Test ID、删除断言、增加 skip/xfail；
- 修改 MCP、45 tools、11 resources、3 templates 或 relay；
- 修改规则包、Host profile、AGENTS.md、CLAUDE.md、.mdc；
- 修改 CodeFlowMu 或其固定 FCoP 3.2.5 合同；
- 修改 main、创建或合并 PR、tag、Release、PyPI；
- 进入 WP4/WP5/WP6；
- 自行签署任何 Gate。

## 9. 完成标准

必须达到：

```yaml
AUTHORIZED_CONFORMANCE_FILES_MODIFIED: 1
AUTHORIZED_CONFORMANCE_TEST: C6-X01
FROZEN_TEST_IDS: 60/60
V4_COLLECT_ONLY: 119
V4_STATIC_META: 27/27
V4_BEHAVIORAL: 92 passed / 0 deferred / 0 unexpected
V4_TOTAL: 119 passed / 0 deferred
WP3E_TARGET_NODES: 23/23
TEST_FCOP: ZERO_FAILURES
V3_NEW_FAILURES: 0
MCP_NEW_FAILURES: 0
UNEXPECTED_FAILURES: 0
RECOVERY_STATE_TABLE: 5/5
FAULT_BOUNDARIES: 4/4
COLD_EXPORT_NON_AUTHORITATIVE: PASS
```

完整验证顺序继续采用原 WP3E 第 9 节，包括 Windows 原生 fault/recovery、独立工作区 smoke、public-surface 精确差异、UTF-8/LF、依赖差异、MCP 隔离回归与远端回读。

Linux/macOS 未原生运行必须标为 `NOT_NATIVE_VERIFIED`。

## 10. 停止条件

除原 WP3E 全部停止条件外，增加：

```text
FIXTURE_ALIGNMENT_SCOPE_EXCEEDED
C6_X01_STILL_PROFILE_UNAVAILABLE
CALLER_AUTHORITY_SMUGGLING_REQUIRED
GLOBAL_DRIVER_TRUST_REQUIRED
OTHER_FROZEN_CONFORMANCE_CHANGE_REQUIRED
```

如果恢复实现后发现新的真实合同冲突，不得继续堆补丁；以精确 Test ID、规范条款、生产入口和零写入证据停止。

## 11. GitHub 交付

从本任务书 Commit 创建：

```text
review/fcop-4.0-wp3e.0-core-closeout
```

提交链固定：

```text
Taskbook Commit
  → Content Commit
  → Manifest Commit
```

Content Commit 包含阶段 A 的唯一夹具改动、阶段 B 实现与测试、snapshot、CHANGELOG 和七份报告。Manifest Commit 只新增：

```text
reviews/fcop-4.0/wp3e.0/MANIFEST.md
```

推送后重新 fetch，并验证直接父链、固定合同与 Gate 祖先、allowlist、所有交付 SHA-256、remote main 未变、worktree 干净、无 force push。

## 12. 最终回执

```yaml
WP3E_0_STATUS: COMPLETE | BLOCKED
AUTHORIZED_SCOPE: WP3E_0_ONLY
TASKBOOK_PATH: taskbooks/fcop-4.0/WP3E.0/01-C6-X01-Trusted-Profile-Fixture-Alignment-and-Core-Resume-Taskbook-v1.0.zh.md
TASKBOOK_COMMIT: <sha>
TASKBOOK_SHA256: <sha256>
INPUT_HEAD: 19285e5a22142c3e0331803f85b1776b533d9339
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
WORKTREE: D:\FCoP-wp3e0-c6-alignment-resume
BRANCH: review/fcop-4.0-wp3e.0-core-closeout

C6_X01_FIXTURE_ALIGNMENT: PASS | FAIL
TRUSTED_PROFILE_LOCAL_FIXTURE: PASS | FAIL
GLOBAL_V4_DRIVER_MODIFIED: false
CALLER_AUTHORITY_FIELDS_ADDED: 0
TEST_IDS_RENAMED: 0
ASSERTIONS_REMOVED: 0
SKIP_XFAIL_ADDED: 0
AUTHORIZED_CONFORMANCE_FILES_MODIFIED: 1
OTHER_CONFORMANCE_FILES_MODIFIED: 0

WP3E_TARGET_NODES: 23/23
V4_STATIC_META: 27/27
V4_BEHAVIORAL: 92 passed / 0 deferred / 0 unexpected
V4_TOTAL: 119 passed / 0 deferred
TEST_FCOP: <result>
V3_REGRESSION: <result>
MCP_REGRESSION: <result>
UNEXPECTED_FAILURES: 0

RECOVERY_STATE_TABLE: 5/5
RECOVERY_RECEIPT_IMPLEMENTATIONS: 1
FAULT_BOUNDARIES: 4/4
COLD_EXPORT_NON_AUTHORITATIVE: PASS | FAIL
PUBLIC_SURFACE_SNAPSHOT: PASS | FAIL
CHANGELOG_ADDITIVE_ENTRY: PASS | FAIL

NEW_PUBLIC_APIS: <0..3>
NEW_PRODUCTION_MODULES: <0..1>
NEW_RUNTIME_DEPENDENCIES: 0
NEW_BACKGROUND_COMPONENTS: 0
NEW_AUTHORITATIVE_STORES: 0
NEW_OPERATIONS_DIRECTORIES: 0
NEW_STATE_MACHINES: 0
NEW_LOCK_SYSTEMS: 0
NEW_BASE_ERROR_CODES: 0
FROZEN_SPEC_FILES_MODIFIED: 0
SCHEMA_FILES_MODIFIED: 0
MCP_IMPLEMENTATION_FILES_MODIFIED: 0
RULE_PACKAGE_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0

CONTENT_COMMIT: <sha>
MANIFEST_COMMIT: <sha>
REMOTE_HEAD: <sha>
REMOTE_PUSHED: true | false
REMOTE_REFETCH_VERIFIED: PASS | FAIL
DELIVERY_SHA256: <matched>/<total>
REMOTE_MAIN_UNCHANGED: true | false
WORKTREE_STATUS: CLEAN | DIRTY_PRESERVED

FCOP_4_CORE_IMPLEMENTATION_ACCEPTED: false
WP4_STARTED: false
MAIN_MODIFIED: false
RELEASE_CREATED: false
REQUESTED_GATE: FCOP_4_CORE_IMPLEMENTATION_ACCEPTED
```

完成交付后立即停止。不得自行签署 `FCOP_4_CORE_IMPLEMENTATION_ACCEPTED`。
