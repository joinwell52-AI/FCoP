# FCoP 4.0 — envelopes

受众：business-agent。规则包：4.0.0-candidate.1。语言：zh。
主权威：冻结 Core aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6，spec/fcop-4.0-spec.md（中文对照 spec/fcop-4.0-spec.zh.md）。
本派生指引不产生执行、采用、Host 或发布授权。
显式选择依赖：workspace。

## F4.3.1

正式业务信封仅为 TASK、REPORT、ISSUE、REVIEW；shared/ 是知识面，锁、回执和索引不是新增信封。

## F4.3.2

使用 UTF-8/LF 的 YAML frontmatter 加 Markdown，包含 protocol: fcop、version: 4、type、对应 ID、workspace_id、sender、recipient、带时区 created_at。TASK 另需 subject/transitions；REPORT 需 subject_ref/attempt_id/report_kind/result；ISSUE 需 subject_ref/severity；REVIEW 需 review_kind/subject_ref/decision。TASK 可含 parent/branch_of/references/operation_id/operation_kind/normalized_request_digest；REPORT、ISSUE 可含 references；REVIEW 可含 attempt_id/family_digest/authorization_ref/references 及授权绑定。不得混淆 Profile 字段与 Core 字段。

## F4.3.3

不得修改或删除已落盘 REPORT、ISSUE、REVIEW；纠正、替换或撤销须追加同类型新信封，并通过 references 引用受影响事实。

## F4.3.4

REPORT 使用 final 或 replacement；替换须引用同 subject/attempt 的当前 head。未被其他有效替换引用的唯一 head 才有效；零 head 返回 REPORT_REQUIRED，多 head 返回 REPORT_HEAD_AMBIGUOUS。

## F4.3.5

识别 assessment、acceptance、rejection、reopen、authorization、convergence、repair REVIEW。若提供人工批准入口，只能追加 REVIEW，不得修改旧事实。
