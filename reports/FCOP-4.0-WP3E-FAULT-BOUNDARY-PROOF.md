# FCoP 4.0 WP3E · Fault Boundary Proof

`Project.inject_fault(operation, stage, once=True)` 的计划仅保存在当前 `_Creation`
实例内存，允许 operation 只有 `transition`、`export_archive`，允许 stage 只有
`PREPARED`、`TARGET_DURABLE`、`COMMITTED`、`RESPONSE_LOST`。`once=True` 在命中
时先移除计划再抛出既有 `RECOVERY_REQUIRED`，不增加错误码。

transition 触发点绑定既有 receipt 语义边界：PREPARED receipt durable 后、target
与 TARGET_DURABLE receipt durable 后、source 删除且 COMMITTED receipt durable
后、结果返回前。`RESPONSE_LOST` 因而只能发生在完成提交之后。

`internal_operation_id` 只有当前 Project 存在 transition fault plan 时才被接受，
仅决定同一 `fcop/operations/` 内可观察 receipt 文件名；无 fault plan 时返回
`INVALID_ENVELOPE`。普通 T2/T3 不获得外部幂等键，已授权 T4–T7 的既有 exact
retry 语义保持不变。

Windows 原生测试对四个 stage 逐项触发，并用公共 recovery 证明最终只有一个
TASK 和不超过一个 transition event。另有测试证明 fault 只消费一次、不落盘、
不跨 Project 实例，且没有 fault 时既有 1140 项库回归保持通过。

```yaml
FAULT_BOUNDARIES: 4/4
FAULT_OPERATION_SET: transition, export_archive
ONCE_CONSUMPTION: PASS
RESPONSE_LOST_AFTER_COMMIT: PASS
INTERNAL_OPERATION_ID_PUBLIC_REPLAY: REJECTED
NEW_BASE_ERROR_CODES: 0
WINDOWS_NATIVE: PASS
```
