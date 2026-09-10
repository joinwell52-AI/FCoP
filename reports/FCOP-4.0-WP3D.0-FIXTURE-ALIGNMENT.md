# FCoP 4.0 WP3D.0 Fixture Alignment

## 1. 执行身份

```yaml
WP3D_0_STATUS: COMPLETE
AUTHORIZED_SCOPE: WP3D_0_ONLY
TASKBOOK_COMMIT: e06e059dce3c8bbe55d0dbcf78a36b2c3a024cc6
TASKBOOK_SHA256: e34ca748a426fbcf0ee82c577d626cc88f092a76535da1275c08b7a769fb1364
INPUT_HEAD: e664fa39592b699637c1f0e6aeee229331b321e3
BLOCKED_LOCAL_COMMIT: 5e6b14b493f7b98bd5754ea862e1b6525e186a5e
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
WORKTREE: D:\FCoP-wp3d0-profile-fixtures
BRANCH: review/fcop-4.0-wp3d.0-profile-fixture-alignment
```

## 2. 输入与冲突复现

任务书固定身份验证结果：

- 任务书为 UTF-8、LF、无 BOM，328 行、10,468 bytes；SHA-256 与任务书声明一致；
- Taskbook Commit 的直接父提交是 INPUT_HEAD；两者间只新增本任务书；
- 中英文冻结规范与 `aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6` 一致；
- 本地阻断提交可读取，四份报告可逐文件原样转存。

在未修改夹具的代码基线上重新执行 15 个 WP3D 固定目标节点，结果为：

```yaml
WP3D_TARGET_BASELINE: 0 passed / 15 failed
ELAPSED: 4.34s
EXPECTED_IMPLEMENTATION_GAPS: 15
```

静态核对确认三个成功节点原先都把生产操作交给空可信注册表的默认 driver：`C3-GATE-01[T7]` 未纳入 T4/T5/T6 的局部 trusted driver 分支，`C5-N02` 与 `C5-ARCHIVED-01` 直接使用默认 `v4_driver`。

## 3. 唯一夹具修正

### 3.1 C3-GATE-01[T7]

`tests/conformance/v4/test_c3_lifecycle.py` 仅将 T7 纳入现有选择条件：

```python
if edge in {"T4", "T5", "T6", "T7"}
```

因此 T7 与既有 T4/T5/T6 一样，通过：

```python
V4ConformanceDriver(
    workspace.root,
    trusted_profiles={
        "profile:test": DeterministicProfileEvaluator("AUTHORIZED")
    },
    test_id="C3-GATE-01",
)
```

T1–T6、GATE_CASES、完整/缺失 twin、Authorization 内容、错误码和状态断言均未改变。

### 3.2 C5-N02

`tests/conformance/v4/test_c5_convergence.py` 在该测试内部创建同样的确定性可信 driver。convergence REVIEW 写入和 Root T7 都改由该局部 driver 调用；family、references、digest、Authorization 与最终断言未改变。

### 3.3 C5-ARCHIVED-01

同一文件在该测试内部创建局部可信 driver，并将 T7 前后的 `family_digest()` 和 Branch T7 都交给该 driver。Branch `done → archive` 前后 digest 相同的测试意图与断言未改变。

### 3.4 信任边界

`DeterministicProfileEvaluator` 只从既有 `fixtures.py` 导入，并且只通过 `V4ConformanceDriver(..., trusted_profiles=...)` 进入 `Project` 可信初始化边界。业务请求没有新增 evaluator、resolver、registry 或 Host allowlist；默认 `v4_driver` 完全未修改。

## 4. 定向验证

```yaml
CONFLICTING_SUCCESS_NODES: 3/3 ALIGNED
TRUSTED_PROFILE_LOCAL_FIXTURES: 3/3
C3_GATE_T4_T5_T6: 3 passed
PROFILE_NEGATIVE_AND_BOUNDARY: 21 passed
FOCUSED_GREEN_TOTAL: 24 passed
T7_SUCCESS_NODES: 3 EXPECTED_RED_IMPLEMENTATION_ABSENT
```

三个 T7 节点修改后仍失败，但失败原因均为生产能力尚未实现：

- `C3-GATE-01[T7]`：结构化 T7 `OPERATION_NOT_IMPLEMENTED`；
- `C5-N02`：结构化 T7 `OPERATION_NOT_IMPLEMENTED`；
- `C5-ARCHIVED-01`：公共 `family_digest` 尚不存在。

它们不再依赖空可信注册表完成预期成功路径。T4/T5/T6、Profile unavailable、DENIED、UNKNOWN、四类 caller-smuggling 以及 Profile boundary Meta 测试共 24 项全部通过。

## 5. 不变量

```yaml
GLOBAL_V4_DRIVER_MODIFIED: false
FROZEN_TEST_IDS: 60/60
ASSERTIONS_REMOVED: 0
SKIP_XFAIL_ADDED: 0
PRODUCTION_FILES_MODIFIED: 0
FROZEN_SPEC_FILES_MODIFIED: 0
SCHEMA_FILES_MODIFIED: 0
MCP_IMPLEMENTATION_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0
WP3D_IMPLEMENTATION_SUSPENDED: true
```
