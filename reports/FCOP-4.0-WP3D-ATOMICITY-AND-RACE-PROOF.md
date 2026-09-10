# FCoP 4.0 WP3D v1.1 Atomicity and Race Proof

## 结论

```yaml
FAMILY_LINEARIZATION: PASS
FAMILY_RACE_MATRIX: 8/8
SECOND_LOCK_SYSTEM: false
PARTIAL_RECEIPT_OBSERVED: false
DOUBLE_AUTHORIZATION_CONSUMPTION: false
```

所有 family 变更复用 `src/fcop/v4/linearization.py::family_boundary()`。锁键仅由 `workspace_id + root_task_id` 的 canonical JSON 摘要确定；锁内重新读取路径、Branch 集合、attempt、REPORT head、convergence、Authorization 和 receipt，不使用进程内缓存授权提交。

## 八项竞态矩阵

| # | 竞争操作 | 证据 | 可观察结果 |
|---:|---|---|---|
| 1 | Root T7 vs Branch create | `test_root_t7_race_cannot_create_branch_below_done_root` | Root 归档；Branch 因 Root 非 active 被拒绝，无迟到 Branch |
| 2 | Root T7 vs Branch T6 | `test_root_t7_and_branch_reopen_have_one_cross_process_winner` | 恰一方提交；状态仅为 archive/done 或 done/active |
| 3 | Root T7 vs Branch REPORT replacement | `test_root_t7_and_branch_replacement_have_one_cross_process_winner` | 恰一方提交；无陈旧 convergence 批准新 head |
| 4 | convergence vs REPORT replacement | `test_replacement_and_convergence_are_cross_process_linearizable`、`C5-REPORT-RACE-01` | REVIEW 若落盘，只对应旧或新完整快照 |
| 5 | Root T7 vs convergence write | 冻结 `AT-04` | Root 只有看到明确匹配 REVIEW 才能归档，否则稳定拒绝 |
| 6 | Branch T7 vs Root T7 | `test_branch_t7_and_root_t7_both_commit_under_one_family_lock` | 两个短提交可串行完成；Branch done/archive 路径不改摘要 |
| 7 | 两次 Root T7 exact retry | `test_two_root_t7_calls_converge_on_one_receipt` | 两进程均得到结果，`existing=[false,true]`，仅一条 T7 event |
| 8 | T7 Authorization 复用于不同 edge | `test_t7_authorization_race_cannot_consume_a_different_edge`、`C8-RETRY-01[T7]` | 仅 T7 消费；另一 edge 为 invalid/reused，零二次 event |

这些测试均使用 Windows `spawn` 子进程和真实 `Project` 生产入口；同步依赖 `multiprocessing.Event`，没有用 sleep 作为判定 oracle。

## Receipt 与丢响应

T7 沿用 `PREPARED → TARGET_DURABLE → COMMITTED`。receipt 绑定 source/target 相对路径、source/target/request 摘要、source attempt、Authorization 引用及完整字节摘要、evidence 引用及逐项摘要；带 Branch Root 还绑定 `family_digest` 和 convergence REVIEW。精确重试在恢复前重新验证当前 family/convergence，防止 PREPARED 后 family 改变仍误判 Existing。

Root 归档后，Branch REPORT 写入/replacement 和 Branch reopen 均在同一 family lock 内被拒绝；Branch 自身 done→archive 仍可完成，因为该路径变化不改变 canonical digest。
