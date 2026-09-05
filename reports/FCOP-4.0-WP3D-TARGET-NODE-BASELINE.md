# FCoP 4.0 WP3D Target Node Baseline

## 1. 执行环境

```yaml
WORKTREE: D:\FCoP-wp3d-convergence-t7
BRANCH: review/fcop-4.0-wp3d-convergence-t7
HEAD: e664fa39592b699637c1f0e6aeee229331b321e3
TARGET_NODE_COUNT: 15
BASELINE_RESULT: 0 passed / 15 failed
ELAPSED: 3.13s
WARNING_COUNT: 1
```

命令使用 Python 当前环境执行 15 个任务书固定 node id，参数为 `python -m pytest -q --tb=short <15 nodes>`。这是进入生产修改前的真实红灯基线。

## 2. 逐节点结果

| # | Node | 基线 |
|---:|---|---|
| 1 | `test_c3_lifecycle.py::test_c3_n01` | FAIL：T7 `OPERATION_NOT_IMPLEMENTED` |
| 2 | `test_c3_lifecycle.py::test_c3_gate_01[T7]` | FAIL：T7 `OPERATION_NOT_IMPLEMENTED` |
| 3 | `test_c5_convergence.py::test_c5_n02` | FAIL：T7 `OPERATION_NOT_IMPLEMENTED` |
| 4 | `test_c5_convergence.py::test_stale_convergence_rejected[C5-R03]` | FAIL：期望 `FAMILY_CONVERGENCE_MISMATCH`，实际 `OPERATION_NOT_IMPLEMENTED` |
| 5 | `test_c5_convergence.py::test_stale_convergence_rejected[C5-X01]` | FAIL：期望 `FAMILY_CONVERGENCE_MISMATCH`，实际 `OPERATION_NOT_IMPLEMENTED` |
| 6 | `test_c5_convergence.py::test_c5_branch_01` | FAIL：期望 `BRANCH_NOT_TERMINAL`，实际 `OPERATION_NOT_IMPLEMENTED` |
| 7 | `test_c5_convergence.py::test_c5_archived_01` | FAIL：`family_digest` 不存在 |
| 8 | `test_c5_convergence.py::test_c5_family_digest_01` | FAIL：`family_digest` 不存在 |
| 9 | `test_c5_convergence.py::test_c5_report_race_01` | FAIL：`family_digest` 不存在 |
| 10 | `test_c6_authorization.py::test_c6_r01[missing]` | FAIL：期望 `AUTHORIZATION_REQUIRED`，实际 `OPERATION_NOT_IMPLEMENTED` |
| 11 | `test_c6_authorization.py::test_c6_r01[actor-admin-only]` | FAIL：期望 `AUTHORIZATION_REQUIRED`，实际 `OPERATION_NOT_IMPLEMENTED` |
| 12 | `test_c6_authorization.py::test_c6_r01[wrong-subject]` | FAIL：期望 `AUTHORIZATION_INVALID`，实际 `OPERATION_NOT_IMPLEMENTED` |
| 13 | `test_c6_authorization.py::test_c6_r01[wrong-edge]` | FAIL：期望 `AUTHORIZATION_INVALID`，实际 `OPERATION_NOT_IMPLEMENTED` |
| 14 | `test_c6_authorization.py::test_c6_r01[wrong-attempt]` | FAIL：期望 `AUTHORIZATION_INVALID`，实际 `OPERATION_NOT_IMPLEMENTED` |
| 15 | `test_c8_recovery.py::test_c8_retry_01[T7]` | FAIL：T7 `OPERATION_NOT_IMPLEMENTED` |

## 3. 冻结合同/夹具冲突

### 3.1 规范事实

- `spec/fcop-4.0-spec.md:94` 将 T7 标为需要 Profile。
- `spec/fcop-4.0-spec.md:189` 规定 T4/T5/T6/T7 没有可用可信 Profile 时返回 `AUTHORIZATION_PROFILE_UNAVAILABLE`；只有 evaluator 的 `AUTHORIZED` 可以通过。
- `src/fcop/v4/authorization.py:179-187` 已按该合同先检查可用可信 Profile，再解析 authorization。
- `src/fcop/v4/authorization.py:262-278` 明确要求 Profile 已采用、可信 evaluator 可调用、issuer proof 被评为 `AUTHORIZED`。

### 3.2 夹具事实

- 默认 fixture 在 `tests/conformance/v4/conftest.py:23-25` 不传 `trusted_profiles`。
- driver 在 `tests/conformance/v4/driver.py:171-172` 因此构造无可信注册项的 `Project(root)`。
- `C3-GATE-01[T7]` 在 `tests/conformance/v4/test_c3_lifecycle.py:279-288` 未像 T4/T5/T6 那样构造 trusted driver。
- `C5-N02` 与 `C5-ARCHIVED-01` 分别在 `tests/conformance/v4/test_c5_convergence.py:64-88`、`:213-231` 使用默认 driver 并要求 T7 成功。

这些节点仅创建了带 `profile_ref: profile:test` 的 REVIEW；manifest 采用或 REVIEW 声明不能产生信任。它们缺少冻结合同要求的可信 evaluator 注册。

## 4. 判定

```yaml
RED_BASELINE_REPRODUCED: true
TARGET_IDS_LOCKED: 15/15
FROZEN_TEST_MUTATION_ALLOWED: false
CONFLICTING_SUCCESS_NODES: 3
CONFLICTING_NODES:
  - C3-GATE-01[T7]
  - C5-N02
  - C5-ARCHIVED-01
STOP_CODE: FROZEN_CONFORMANCE_CONTRACT_CONFLICT
```

不能通过弱化生产授权门来把红灯变绿；也不能在 WP3D_ONLY 内修改冻结夹具。故在生产编辑前停止。
