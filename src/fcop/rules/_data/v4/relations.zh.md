# FCoP 4.0 — relations

受众：business-agent。规则包：4.0.0-candidate.1。语言：zh。
主权威：冻结 Core aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6，spec/fcop-4.0-spec.md（中文对照 spec/fcop-4.0-spec.zh.md）。
本派生指引不产生执行、采用、Host 或发布授权。
显式选择依赖：workspace, envelopes。

## F4.5.1

只使用 parent、branch_of、subject_ref、references。parent 是强 TASK 层级而非并行；branch_of 是至多一个强 Root 链接；subject_ref 是唯一强 TASK/工作区主题（工作区 ISSUE 为 workspace:<workspace_id>）；references 是弱的既有信封引用，被门消费时必须可解析。

## F4.5.2

强关系缺失、悬空、跨工作区、成环或不唯一时以 RELATION_INVALID 关闭失败。普通弱引用未解析时给出 REFERENCE_UNRESOLVED；门使用的引用无法解析则拒绝操作。

## F4.5.5

thread_key 仅为 Profile/Legacy 元数据，不得新增、改名或改变 Core 关系。Branch 深度和 Root active 要求由 convergence 模块负责。
