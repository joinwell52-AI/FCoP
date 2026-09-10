# FCoP 4.0 — lifecycle

受众：business-agent。规则包：4.0.0-candidate.1。语言：zh。
主权威：冻结 Core aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6，spec/fcop-4.0-spec.md（中文对照 spec/fcop-4.0-spec.zh.md）。
本派生指引不产生执行、采用、Host 或发布授权。
显式选择依赖：workspace, envelopes, relations, authorization, idempotency, recovery。

## F4.4.1

权威 TASK 只能在一个 fcop/_lifecycle/{inbox,active,review,done,archive}/TASK-*.md 路径中；位置是唯一当前状态。

## F4.4.2

恰执行七个门：T1 None→inbox 要求 TASK 不存在；T2 inbox→active 要求唯一 inbox TASK 并开启 attempt；T3 active→review 要求唯一 active TASK 和当前有效 REPORT；T4 review→done 要求 T3 绑定 REPORT、acceptance REVIEW 和授权；T5 review→active 要求被拒当前 REPORT、rejection REVIEW 和授权，并开启 attempt；T6 done→active 要求 reopen/authorization REVIEW 和授权，不要求 REPORT，并开启 attempt；T7 done→archive 复用已接受证据，要求归档授权，有 Branch 时另需 convergence。T1–T3 无 Base 授权要求（Profile 可为 T2/T3 加策略）；T1/T3/T4/T7 不开新 attempt。汇合细节归 convergence，授权核验归 authorization。

## F4.4.3

一条命令只提交一条边并追加一个迁移；便捷链须拆分，前边失败不得制造后续事件。

## F4.4.4

以 LEGACY_TRANSITION_NOT_ALLOWED 拒绝 active→done 捷径；4.0 中 Legacy finish_task 不得绕过 T3/T4。

## F4.4.5

记录 at/from/to/by/tool，进入 active 时附新 attempt_id。为所有消费的 REPORT/REVIEW 保存对齐 evidence_ref/evidence_digest 数组，适用时另存 authorization_ref/authorization_digest。完整 UTF-8/LF 验证字节取小写 SHA-256；后续漂移为 EVIDENCE_DIGEST_MISMATCH。事件仅追加，不用于推导 NOW。

## F4.4.6

archive 为终态，权威文件不得移往 history 或回流；v3 history 只读 Legacy，cold export 只能产生非权威副本。

## F4.4.7

未列迁移返回 INVALID_TRANSITION。普通 T7 要求唯一 done、有效强关系和授权；普通 parent 子任务及 ISSUE 状态不是 Base 门，额外策略属于显式 Profile。

## F4.6.1

每次 T2/T5/T6 进入 active 创建不可复用的 urn:uuid attempt_id；最后一次 active 进入事件决定当前 attempt。

## F4.6.2

T3 消费本 TASK 当前 attempt 的唯一 REPORT；旧 attempt REPORT 不能满足门。

## F4.6.3

T4 acceptance REVIEW 的 decision 必须为 approved，绑定当前 subject、attempt、REPORT；按 authorization 模块核验，并依 F4.4.5 保存 REPORT/REVIEW/授权身份及字节摘要。

## F4.6.4

普通及 Branch TASK 使用相同生命周期和证据门，不设 Branch 专用完成状态。
