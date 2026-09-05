# FCoP 4.0 WP3C Authorization Model

## 1. 权威与边界

- 唯一任务书：`taskbooks/fcop-4.0/WP3C/01-Authorization-and-Controlled-Transitions-Taskbook.zh.md`，提交 `46c7d7522f020e85ad658a9e0147578d61fe908a`，SHA-256 `9574b070cc9e850004954e9e5b1d3516c4f73bcaa5ea335da6dd226d31ff1340`。
- 代码基线：`511039db227a23ae3e2d79aaae775a92ba392f5c`。
- 冻结合同：`aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6`。
- 本轮只实现可信 Profile evaluator、Authorization REVIEW 以及 T4/T5/T6；T7、family digest、convergence、Branch 终态门保持未实现。

## 2. 信任边界

`Project(..., trusted_profiles={profile_ref: evaluator})` 是唯一可信注册入口。构造时复制调用方映射并以只读映射保存，再传入 v4 私有上下文；后续修改调用方原字典不得改变已绑定 registry。工作区 manifest 的 `profiles[]` 仅声明已采用 Profile，不提供裁决能力。

业务请求只允许携带 `profile_ref` 与 `authorization_ref` 等数据引用。请求中出现 callable，或 `profile_evaluator`、`profile_resolver`、`trusted_profiles`、`profile_registry`、`authorization_evaluator`、`caller_judge`、`host_allowlist_match` 等调用者裁判字段，必须在生产入口返回 `AUTHORIZATION_INVALID`，不得调用伪 evaluator。

Core 从已持久化 Authorization REVIEW 读取 `profile_ref`、`sender`（issuer）与 `issuer_proof`，并只将这三项交给可信 evaluator。只有精确字符串 `AUTHORIZED` 通过；`DENIED`、`UNKNOWN`、未知值、异常或不可调用对象一律 Fail Closed 为 `AUTHORIZATION_INVALID`。

## 3. Authorization REVIEW 验证顺序

在 family lock 内、任何 receipt 或目标文件写入前按稳定优先级验证：

1. 业务请求中的调用者裁判字段或 callable 先以 `AUTHORIZATION_INVALID` 拒绝；
2. TASK ID、边和 tool 先通过静态迁移面校验；T7 固定为 `OPERATION_NOT_IMPLEMENTED`；
3. 完全相同的 durable receipt 先按五状态表恢复；已提交精确重试返回 Existing，不重新执行 Profile；
4. 相同 authorization_ref 已存在于另一 durable transition fact 时返回 `AUTHORIZATION_REUSED`；
5. 当前 TASK 唯一、source stage 和当前 source attempt 可证明；
6. manifest 没有可用 adopted Profile 时返回 `AUTHORIZATION_PROFILE_UNAVAILABLE`；
7. authorization_ref 缺失时返回 `AUTHORIZATION_REQUIRED`；
8. REVIEW 文件、路径、类型、ID、UTF-8/LF 和完整结构；
9. subject、edge、source attempt、`operation_kind=lifecycle_transition`、family=null、scope=single_use、decision/review_kind；
10. profile_ref 同时存在于 manifest 与可信 registry；
11. issued_at/expires_at 为带时区时间，过期返回 `AUTHORIZATION_EXPIRED`；
12. evidence 引用与完整文件字节摘要；不一致返回 `EVIDENCE_DIGEST_MISMATCH`；
13. 调用可信 evaluator；非 AUTHORIZED 返回 `AUTHORIZATION_INVALID`。

第 3、4 项以已持久化事实优先：响应丢失后的结果不依赖重试时 Profile 是否仍在线；已经提交到 TASK event 的 single-use 消费也不能因 registry 后续变化而消失。

`sender=ADMIN`、调用者 `actor=ADMIN`、manifest membership、Host allowlist 或 UI 动作均不产生授权。

## 4. T4/T5/T6 证据模型

| 边 | evidence_ref | source attempt | target attempt | 额外验证 |
|---|---|---|---|---|
| T4 review→done | 当前 REPORT head、acceptance REVIEW | 当前 attempt | 与 source 相同 | 最近 T3 event 必须绑定同一 REPORT 和字节摘要；acceptance 为 approved |
| T5 review→active | 当前 REPORT head、rejection REVIEW | 当前 attempt | 新 UUID URN | 最近 T3 event 必须绑定当前 REPORT；rejection 为 rejected |
| T6 done→active | reopen REVIEW（或结构完整 authorization REVIEW） | 当前 accepted attempt | 新 UUID URN | 不要求新增 REPORT；不得采用旧 REPORT |

同一 REVIEW 可以同时作为 evidence 与 authorization，但 `evidence_digest` 与 `authorization_digest` 各自都记录完整文件字节 SHA-256。独立 evidence REVIEW 与 authorization REVIEW 时分别解析、验证和记录。

## 5. 单次消费与原子性

消费事实只存在于提交后的 TASK transition event：`authorization_ref` 与 `authorization_digest` 和状态迁移、evidence digests 在同一目标 TASK 字节中原子发布。不得重写 Authorization REVIEW，不得新增消费数据库或旁路状态。

T4/T5/T6 复用 WP3B 的 family lock 与三阶段 receipt：`PREPARED → TARGET_DURABLE → COMMITTED`。T5/T6 receipt 同时记录 source attempt 和 target attempt；`attempt_id` 表示提交后可见 attempt。响应丢失后的精确请求依据 receipt 与可见 TASK 返回 Existing，不追加事件、不二次消费；同一授权用于不同边或不同绑定返回 `AUTHORIZATION_REUSED`。

五状态恢复分类保持不变。target 可见但授权、证据或摘要不可证明时 Fail Closed 并保留全部证据。T4 与 T5 竞争同一 review TASK 时共用相同 family lock，最多一条边提交。

## 6. 错误码映射

| 条件 | Base code |
|---|---|
| 无可用 adopted Profile | `AUTHORIZATION_PROFILE_UNAVAILABLE` |
| 缺少 authorization_ref | `AUTHORIZATION_REQUIRED` |
| 结构/绑定/Profile/evaluator/调用者裁判失败 | `AUTHORIZATION_INVALID` |
| 授权已过期 | `AUTHORIZATION_EXPIRED` |
| 已消费授权用于不同迁移 | `AUTHORIZATION_REUSED` |
| 已绑定证据或授权文件字节变化 | `EVIDENCE_DIGEST_MISMATCH` |
| 收据冲突、损坏或恢复事实不可证明 | `RECOVERY_REQUIRED` |
