# FCoP 4.0 WP3C.1 Expiry and Recovery Proof

## 1. 过期线性化

首次授权迁移按以下顺序执行：

```text
解析并绑定 Authorization REVIEW
→ 第一次 UTC 过期检查
→ 调用可信 Profile evaluator
→ 第二次 UTC 过期检查
→ PREPARED receipt
→ 目标 TASK / event / COMMITTED receipt
```

第二次检查位于 evaluator 返回 `AUTHORIZED` 之后、任何 PREPARED receipt 写入之前。使用私有 `_utc_now()`，未改变 `Project` 或 `transition()` 的公共签名，也未引入 timer、后台组件或 Runtime 状态。

`WP3C1-EXP-01` 用确定性双时刻替换私有时钟：第一次检查时授权有效，evaluator 返回后的第二次检查时已经过期。生产入口返回 `AUTHORIZATION_EXPIRED`；完整目录树快照与调用前一致，证明 receipt、目标 TASK、授权消费 event 以及原始证据均为零变化。

## 2. 已提交精确重试

精确重试先按 operation fact/receipt 恢复既有已提交结果，再进入新的授权验证。因此，授权在成功提交后过期不会推翻既有事实。

`WP3C1-EXP-02` 先在有效期内提交，再把时钟推进到过期后，并注册一个若被调用即失败的 evaluator。重试结果为 `existing: true`，evaluator 调用次数为 0，授权迁移 event 仍只有 1 条，整个目录树没有追加或改写。

## 3. 恢复时的 Profile 绑定

带授权的 T4/T5/T6 receipt 在恢复路径重新解析其不可变 Authorization REVIEW，并依次验证：

1. REVIEW 完整字节 SHA-256 等于 receipt 的 `authorization_digest`；
2. REVIEW 的 `review_id` 等于 receipt 的 `authorization_ref`；
3. REVIEW 的 `profile_ref` 等于 receipt 的 `profile_ref`。

任何不一致都在恢复业务写入前 Fail Closed，不删除 source，不覆盖 target，不补写 event。

## 4. 现有错误码选择

- Authorization REVIEW 字节发生变化或引用无法解析：`EVIDENCE_DIGEST_MISMATCH`。这是不可变证据本身无法通过摘要证明。
- REVIEW 字节摘要仍正确，但 receipt 的 `profile_ref` 或 `authorization_ref` 与该 REVIEW 不一致：`RECOVERY_REQUIRED`。这是恢复证明元数据与完整证据的绑定损坏，而不是证据字节发生变化。

没有新增 Base 错误码。`WP3C1-REC-01` 只篡改 receipt 的 `profile_ref`，保留 Authorization REVIEW 不变，生产重试返回 `RECOVERY_REQUIRED`，且失败前后目录树完全一致。

## 5. Windows 定向证明

原生 Windows 定向运行覆盖：evaluator 前后过期边界、过期后的精确重试、receipt Profile 不匹配、既有 T4/T5 授权竞态，以及 T4/T5/T6 response-loss 重试。结果为 7 passed；没有依赖毫秒 sleep。
