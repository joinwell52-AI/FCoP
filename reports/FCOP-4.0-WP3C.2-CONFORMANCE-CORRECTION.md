# FCoP 4.0 WP3C.2 Conformance Correction

## 1. 冲突结论

输入提交 `d0d9ec029516b4379dbf74f2167490f4867680c4` 中，冻结节点 `C3-GATE-01[T6]` 构造一份 `reopen + approved` REVIEW，并把同一个引用同时传给 `review_ref` 与 `authorization_ref`。

冻结 F4.7.1–F4.7.2 的合同边界是：

- `reopen + approved` 只可作为 T6 `done → active` 的必要 REVIEW 证据；
- T6 授权必须由独立的 `authorization + authorize` REVIEW 承载；
- 只有 T4 acceptance 与 T5 rejection 获得兼任 authorization 的例外。

因此，WP3C.1 生产实现返回 `AUTHORIZATION_INVALID` 是正确行为，冲突位于 Conformance 的 Arrange 夹具。

## 2. 编码前证据

编码前单独运行：

```text
python -m pytest -q "tests/conformance/v4/test_c3_lifecycle.py::test_c3_gate_01[T6]"
```

真实结果为 `1 failed`；结构化异常为 `AUTHORIZATION_INVALID`，失败位置是生产载体矩阵对 `reopen` 作为 `authorization_ref` 的拒绝。

## 3. 唯一修正

只修改 `tests/conformance/v4/test_c3_lifecycle.py` 的 Arrange：

1. 保留 `REVIEW-T6`：`review_kind: reopen`、`decision: approved`，作为 `review_ref`；
2. 用既有 `authorization_fixture()` 另建 `REVIEW-T6-AUTHORIZATION`：`review_kind: authorization`、`decision: authorize`；
3. 独立授权仍绑定当前 TASK、T6 `done → active`、当前 source attempt、`profile:test`、single-use scope 及既有可验证 issuer proof；
4. 将独立 REVIEW ID 传给 `authorization_ref`。

同时按任务书允许范围，仅澄清了 `C3-N02` 中关于 `authorization_fixture()` 生成物的注释；没有改变其行为。

## 4. 测试语义保持证明

```yaml
TEST_ID: C3-GATE-01
PARAMETER_ID_T6: PRESERVED
T6_COMPLETE_GATE: PASS
T6_MISSING_AUTHORIZATION: AUTHORIZATION_REQUIRED
MISSING_AUTHORIZATION_ZERO_WRITE_ASSERTION: PRESERVED
SOURCE_TARGET_ASSERTIONS: PRESERVED
ATTEMPT_ASSERTIONS: PRESERVED
TEST_IDS_RENAMED: 0
ASSERTIONS_REMOVED: 0
SKIP_XFAIL_ADDED: 0
DRIVER_SHORTCUTS_ADDED: 0
```

修改后的同一节点为 `1 passed`。整个 `test_c3_lifecycle.py` 为 `10 passed / 3 inherited deferred`；三个 deferred 仍分别属于未授权的 T7 与冷导出/fault surface，不由 WP3C.2 改变。

## 5. 冻结集合

Conformance 收集总数保持 `119`；冻结合同 Test ID 保持 `60/60`。Git diff 没有改变 `GATE_CASES`、参数 ID、测试函数名、Test ID 字符串或任何 Assert 段。除该测试文件外，没有修改其他 Conformance 文件。

## 6. 对齐结果

```yaml
C3_GATE_01_T6: PASS
FROZEN_TEST_IDS: 60/60
TASKBOOK_CORRECTED_EXPECTED_RED: 0
V4_STATIC_META: 27 passed
V4_BEHAVIORAL: 54 passed / 38 inherited deferred
V4_TOTAL: 81 passed / 38 deferred
UNEXPECTED_FAILURES: 0
```
