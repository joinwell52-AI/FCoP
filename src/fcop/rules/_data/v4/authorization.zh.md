# FCoP 4.0 — authorization

受众：business-agent。规则包：4.0.0-candidate.1。语言：zh。
主权威：冻结 Core aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6，spec/fcop-4.0-spec.md（中文对照 spec/fcop-4.0-spec.zh.md）。
本派生指引不产生执行、采用、Host 或发布授权。
显式选择依赖：workspace, envelopes, relations。

## F4.7.1

授权落为追加不可变的 authorization REVIEW：subject_ref、decision: authorize、operation_kind: lifecycle_transition、transition {from,to}、authorization_scope: single_use、issued_at、expires_at 或 null、attempt_id 或 null、family_digest 或 null、references、profile_ref；不是第五类信封。

## F4.7.2

仅 T4 acceptance 或 T5 rejection 在具备含 profile_ref 的全部绑定且可信签发者评估为 AUTHORIZED 时可兼作授权；否则引用独立 authorization REVIEW。convergence 本身不能授权 Root T7。

## F4.7.3

核验既有 REVIEW 类型、已采用 profile_ref、decision、主题、迁移边、attempt、family、有效时间、复用、证据引用和存储字节摘要；按事实返回 AUTHORIZATION_REQUIRED/INVALID/EXPIRED/REUSED 或 EVIDENCE_DIGEST_MISMATCH，不得部分匹配即接受。

## F4.7.4

签发者评估只能经过已采用 Profile 的可信注册项；AUTHORIZED 通过，DENIED、UNKNOWN 均以 AUTHORIZATION_INVALID 拒绝。T4–T7 缺少可用已采用 Profile 时返回 AUTHORIZATION_PROFILE_UNAVAILABLE。不得安装调用者自带裁判逻辑或 Core 角色表。

## F4.7.5

消费迁移记录 authorization_ref 和 authorization_digest；sender、actor、Host 白名单、UI 操作或 REPORT 结论均不能单独产生授权。

## F4.7.6

本地信任、OS ACL、签名等 Profile 机制位于 Core 之外；可编辑文件本身不构成密码学身份安全。

## F4.7.7

空 Profile 集对 T1–T3 等无授权门 Base 操作合法；若要完成普通开发任务，应在初始化时显式采用可用授权 Profile，不使任何固定角色成为 Core 必填项。
