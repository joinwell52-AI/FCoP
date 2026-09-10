# FCoP 4.0 WP3D v1.1 Target Node Baseline

## 执行环境

```yaml
WORKTREE: D:\FCoP-wp3d-v1.1-convergence-t7
BRANCH: review/fcop-4.0-wp3d-convergence-t7-v1.1
HEAD: 4e0d8c524020cc3b1b152d3d3a736f84a2f78a4e
INPUT_HEAD: dd8c39a2e025cc60f37d443abbe0988cbddf1810
TARGET_NODE_COUNT: 15
BASELINE_RESULT: 0 passed / 15 failed
ELAPSED: 4.61s
```

命令为 `python -m pytest -q --tb=short <15 fixed node ids>`。所有失败均为预期红灯，且未出现收集错误。

| # | Node | 基线事实 |
|---:|---|---|
| 1 | `test_c3_lifecycle.py::test_c3_n01` | T7 未实现 |
| 2 | `test_c3_lifecycle.py::test_c3_gate_01[T7]` | T7 未实现 |
| 3 | `test_c5_convergence.py::test_c5_n02` | digest/T7 未实现 |
| 4 | `test_stale_convergence_rejected[C5-R03]` | 尚未返回 mismatch |
| 5 | `test_stale_convergence_rejected[C5-X01]` | 尚未返回 mismatch |
| 6 | `test_c5_branch_01` | 尚未返回 branch terminal 错误 |
| 7 | `test_c5_archived_01` | `family_digest` 缺失 |
| 8 | `test_c5_family_digest_01` | `family_digest` 缺失 |
| 9 | `test_c5_report_race_01` | `family_digest` 缺失 |
| 10 | `test_c6_r01[missing]` | T7 未实现 |
| 11 | `test_c6_r01[actor-admin-only]` | T7 未实现 |
| 12 | `test_c6_r01[wrong-subject]` | T7 未实现 |
| 13 | `test_c6_r01[wrong-edge]` | T7 未实现 |
| 14 | `test_c6_r01[wrong-attempt]` | T7 未实现 |
| 15 | `test_c8_retry_01[T7]` | T7 未实现 |

`reviews/fcop-4.0/gates/WP3D-FIXTURE-ALIGNMENT-ACCEPTED.md` 已关闭此前 T7 可信 Profile 夹具冲突；业务请求仍不携带 evaluator。

```yaml
RED_BASELINE_REPRODUCED: true
TARGET_IDS_LOCKED: 15/15
FROZEN_TEST_MUTATION_ALLOWED: false
PREVIOUS_FIXTURE_CONFLICT: CLOSED_BY_GATE
IMPLEMENTATION_MAY_BEGIN: true
```
