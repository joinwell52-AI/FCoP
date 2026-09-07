# FCoP 4.0 — idempotency

受众：business-agent。规则包：4.0.0-candidate.1。语言：zh。
主权威：冻结 Core aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6，spec/fcop-4.0-spec.md（中文对照 spec/fcop-4.0-spec.zh.md）。
本派生指引不产生执行、采用、Host 或发布授权。
显式选择依赖：workspace。

## F4.8.1

普通及 Branch TASK 创建以 workspace_id + operation_kind + operation_id 为持久幂等键，比较 normalized_request_digest；两者 operation_kind 均为 create_task，branch_of 属于摘要而非新命名空间。

## F4.8.2

operation_id 长度 1–128，匹配 [A-Za-z0-9][A-Za-z0-9._:-]*；原子预留键，内存去重或无锁扫描不够。

## F4.8.3

同键同摘要返回含原 task_id/path/digest 的 Existing，不产生文件或事件；不同摘要返回 OPERATION_ID_CONFLICT。操作种类命名空间分离，结果重启后仍可用。

## F4.8.4

对 fcop-create-task-v1 规范 JSON 求摘要，字段为 workspace_id、operation_kind、operation_id、sender、recipient、subject、body、默认后 priority、parent、branch_of、references。字符串 NFC，CRLF/CR 转 LF，正文一个最终 LF；缺省为 null，references 去重并按码点排序，键排序并紧凑 UTF-8 序列化，取小写 SHA-256。排除时间戳、分配身份/路径、thread_key、risk_level、Profile 扩展；临时校验开关不是请求身份。

## F4.8.5

可审计操作事实按 Encoding 布局持久保存，不是第二 NOW 来源。TASK 重复记录 operation_id/kind/digest；重复或冲突记录须关闭失败。
