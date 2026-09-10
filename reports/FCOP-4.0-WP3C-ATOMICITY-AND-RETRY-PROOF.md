# FCoP 4.0 WP3C Atomicity and Retry Proof

## 1. 结论

```yaml
T4_ATOMICITY: PASS
T5_ATOMICITY: PASS
T6_ATOMICITY: PASS
AUTHORIZATION_CONSUMPTION_COMMIT: SAME_TASK_EVENT
EXACT_RETRY: EXISTING
CROSS_TRANSITION_REUSE: AUTHORIZATION_REUSED
FIVE_STATE_TABLE_CHANGED: false
FAMILY_LOCK_REUSED: true
PUBLIC_OPERATION_ID_ADDED: false
WINDOWS_NATIVE_RACE: PASS
UNEXPECTED_FAILURES: 0
```

T4、T5、T6 沿用 WP3B 的同一 Root-family 短锁和三阶段 receipt。授权消费不是旁路表：`authorization_ref`、`authorization_digest`、证据引用/摘要及迁移边在同一个目标 TASK event 中发布，因此不存在“已消费但未移动”或“已移动后再补消费表”的第二提交。

## 2. 物理提交序列

| 阶段 | 可见事实 | 恢复动作 |
|---|---|---|
| PREPARED | source 存在；receipt 记录 source/target 摘要、完整 event、授权与证据摘要 | 从 source 和 receipt 重建目标；证据不一致即 Fail Closed |
| TARGET_DURABLE | source 与相同目标同时存在 | 验证双方字节及证据后删除 source，再把 receipt 标为 COMMITTED |
| COMMITTED | 仅 target 存在；receipt 为 COMMITTED | 验证目标与授权/证据后返回 Existing |
| RESPONSE_LOST | 物理状态等同 COMMITTED，调用者未收到响应 | 同一请求匹配 normalized digest，返回 Existing；不追加 event |
| 不可证明/冲突 | 双路径字节不同、receipt 损坏或证据摘要变化 | `RECOVERY_REQUIRED` 或 `EVIDENCE_DIGEST_MISMATCH`；不覆盖、不删除证据 |

T5/T6 receipt 分开记录 `source_attempt_id` 与 `target_attempt_id`；T4 两者相同。历史 receipt 保留，但当前轮次由 TASK 的 entry-to-active event 决定，不使用 mtime、文件名顺序或进程缓存选 winner。

## 3. 精确重试和 single-use

- 同一请求摘要匹配同一 receipt：按五状态恢复，最终 `existing: true`。
- 同一授权已出现在另一已提交 TASK transition event：返回 `AUTHORIZATION_REUSED`。
- 授权 REVIEW 从不重写、删除或原地标记 consumed。
- 任一授权或 gate evidence 文件字节改变：完整文件 SHA-256 不匹配，拒绝恢复。
- T4/T5 同时争用同一 review TASK：两个原生 Windows spawn 进程进入同一 family lock，实测最多一个迁移提交；NOW 只有一个 TASK 路径。

## 4. 实测矩阵

| 场景 | 覆盖 | 结果 |
|---|---:|---|
| T4 × PREPARED/TARGET_DURABLE/COMMITTED/RESPONSE_LOST | 4 | PASS |
| T5 × PREPARED/TARGET_DURABLE/COMMITTED/RESPONSE_LOST | 4 | PASS |
| T6 × PREPARED/TARGET_DURABLE/COMMITTED/RESPONSE_LOST | 4 | PASS |
| C8 exact retry T4/T5/T6 | 3 | PASS |
| T4/T5 Windows spawn race | 1 | PASS |
| 授权异边复用及零副作用 | 1 | PASS |
| 授权/证据字节改变 | 2 | PASS |
| T5/T6 历史 receipt 不阻塞新轮次 | 2 | PASS |

命令与结果：

```text
python -m pytest -q tests/test_fcop/test_v4_authorization.py
36 passed

python -m pytest -q tests/test_fcop/test_v4_authorization.py::test_t4_t5_race_commits_only_one_authorization \
  tests/conformance/v4/test_c8_recovery.py::test_c8_retry_01[T4] \
  tests/conformance/v4/test_c8_recovery.py::test_c8_retry_01[T5] \
  tests/conformance/v4/test_c8_recovery.py::test_c8_retry_01[T6]
4 passed
```

## 5. 边界

没有增加公共 fault injection、公共 recovery、公共 operation_id、数据库、消费表、后台组件或新状态机。公共恢复节点继续属于后续阶段；本轮只证明 T4/T5/T6 通过现有 transition 入口触发的私有 receipt 恢复。
