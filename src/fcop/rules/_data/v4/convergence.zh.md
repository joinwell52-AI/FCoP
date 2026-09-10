# FCoP 4.0 — convergence

受众：business-agent。规则包：4.0.0-candidate.1。语言：zh。
主权威：冻结 Core aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6，spec/fcop-4.0-spec.md（中文对照 spec/fcop-4.0-spec.zh.md）。
本派生指引不产生执行、采用、Host 或发布授权。
显式选择依赖：workspace, envelopes, relations, authorization, idempotency, recovery, lifecycle, compatibility。

## F4.5.3

Branch 指向无 branch_of 的 Root，自身不能再作 Branch Root；所有 Branch 同级，更深嵌套返回 BRANCH_DEPTH_EXCEEDED。

## F4.5.4

仅当 Root 唯一且 active 时创建 Branch，否则 ROOT_NOT_ACTIVE；done Root 开新并行工作前须经授权 T6。

## F4.6.5

在同一 family 边界内，Root T7 要求唯一 done 且非 Branch 的 Root、全部 Branch done/archive、各当前 attempt 唯一有效 REPORT、各 Branch 自身 T3/T4 完成、汇合精确覆盖当前 REPORT、现算 family_digest 一致及绑定该摘要的 Root 授权。非终态 Branch 返回 BRANCH_NOT_TERMINAL。convergence REVIEW 包含 subject_ref=Root、family_digest、Branch REPORT references；它本身不产生归档授权。

## F4.6.6

对紧凑 UTF-8 规范 JSON {contract:fcop-family-v1,root_task_id,branches:[{branch_task_id,attempt_id,report_id,report_digest}]} 求小写 SHA-256。收集所有指向 Root 的 TASK，使用当前 attempt 及唯一 head；report_digest 取完整已验证 UTF-8/LF REPORT 字节摘要。Branch 按 branch_task_id、所有对象键按 Unicode 码点排序，无 BOM、尾 LF 或额外空白；排除阶段、mtime、枚举顺序、Runtime 计数及内存代次。

## F4.6.7

convergence 精确引用每个当前 Branch REPORT，可另引 Root 当前 REPORT；缺失、过期、异 attempt 引用或摘要不一致返回 FAMILY_CONVERGENCE_MISMATCH。done、archive 均为已完成 Branch 状态。

## F4.6.8

Branch 创建/重开/新 attempt 或有效替换 REPORT 改变规范对象/字节，使旧汇合失效。仅 Branch done→archive 不改变摘要。Root T7 在同一 family 边界内重算，不使用锁前过期值授权。
