# FCoP 4.0 — recovery

受众：business-agent。规则包：4.0.0-candidate.1。语言：zh。
主权威：冻结 Core aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6，spec/fcop-4.0-spec.md（中文对照 spec/fcop-4.0-spec.zh.md）。
本派生指引不产生执行、采用、Host 或发布授权。
显式选择依赖：workspace。

## F4.9.1

恢复分类恰为 NOT_COMMITTED、COMMITTED、RECOVERABLE_DUPLICATE、DIVERGENT_DUPLICATE、INDETERMINATE。跨目录操作可有物理中间态，INDETERMINATE 绝非成功兜底。

## F4.9.2

不得静默覆盖目标。创建按 idempotency 模块可返回 Existing；匹配的生命周期双副本走恢复分类，不承诺通用重放；目标内容不同返回 TARGET_ALREADY_EXISTS_DIFFERENT。

## F4.9.3

同一 TASK 出现在多个权威阶段即 STATE_AMBIGUOUS；不得按 mtime、枚举顺序或事件重放选 NOW。

## F4.9.4

每次生命周期操作使用含身份、源/目标路径、规范化/内容摘要和阶段的持久回执。机械恢复不产生第二 TASK、第二事件或覆盖；不可证明损坏/分歧返回 RECOVERY_REQUIRED，保留所有副本。

## F4.9.5

Branch 创建、Root/Branch T2–T7、Branch REPORT 创建/替换、convergence 创建/替换及所有 Root 归档条件共用一个短 family 线性化边界。取得边界后重新读取 Root 状态、Branch 集、attempt、REPORT head、摘要及授权；不得用锁前缓存授权，不得跨 Agent 工作或无关普通 TASK 持有该边界。

## F4.9.6

锁、回执、索引是 Toolkit/Encoding 细节；不得仅凭锁龄删除锁，无法证明安全释放时返回 LOCK_RECOVERY_REQUIRED。

## F4.9.7

保证仅覆盖受支持的本地 NTFS/POSIX 语义；无外部一致性层的不支持跨设备、网络、分布式或弱一致存储返回 UNSUPPORTED_FILESYSTEM 或关闭失败。

## F4.9.8

区分三种保证：TASK/Branch 外部创建幂等使用 operation_id；所有迁移内部崩溃恢复使用回执；T4–T7 响应丢失重试使用已消费授权、摘要和边。T2/T3 不承诺任意时间外部重放。

## F4.9.9

按唯一表分类：匹配源且无目标、无回执或 PREPARED => NOT_COMMITTED，保留源；同摘要源+目标且 TARGET_DURABLE => RECOVERABLE_DUPLICATE，核验后删源、持久目录、完成回执；无源且目标匹配、TARGET_DURABLE 或 COMMITTED => COMMITTED，仅补回执不再移动；源+目标内容不同 => DIVERGENT_DUPLICATE，保留双份交人工；两者皆无或回执/身份/摘要损坏冲突 => INDETERMINATE，保留证据关闭失败。逻辑阶段为 PREPARED、TARGET_DURABLE、COMMITTED。

## F4.9.10

已证明双副本的机械恢复只完成回执，不产生业务 REVIEW；分歧/不确定态的人工处置追加 repair REVIEW。回执不是信封、NOW 或 Runtime 数据库。测试抽象阶段，不依赖偶然临时文件名。

## F4.9.11

T4–T7 响应丢失重试仅在 authorization_ref、授权摘要、边及已存证据摘要全部匹配时返回既有提交。已消费授权用于不同边返回 AUTHORIZATION_REUSED；含糊时关闭失败。
