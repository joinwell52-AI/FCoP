# Branch 合并：4.0.1 候选

尚未发布。`fcop` 和 `fcop-mcp` 均升级为 4.0.1 候选；MCP 依赖
`fcop>=4.0.1,<4.1.0`。原 4.0.0 制品、tag 保持不变。

新增三个薄工具：

- `create_branch`：复用 Core `create_task(branch_of=...)`，返回创建结果、
  Root/Branch ID、最新家族摘要和就绪原因。沿用原创建幂等语义。
- `inspect_family`：只读、稳定 TASK ID 顺序；返回 Root 状态、全部 Branch、
  精确 REPORT Head（ID、attempt、完整字节 SHA-256）、摘要、就绪原因和已有汇合。
- `merge_branches`：提交 Root、非空规范摘要、完整 Branch→REPORT ID 映射、
  调用者的合并结论及冲突处理说明、operation_id、sender/recipient/workspace_id。
  只调用 Core 同名原语，MCP 不加锁、不落 REVIEW、不维护幂等账本。

缺少 attempt 或 REPORT 时，摘要为 `null`，并返回结构化原因；不制造替代算法。
Branch 未终态返回 `BRANCH_NOT_TERMINAL`；Root 未 done 返回 `ROOT_NOT_DONE`。
任一前置条件未满足，`merge_ready` 为 false。摘要存在不等于允许合并。

Root 与两个 Branch 按正常生命周期和可信 Profile 授权完成后，先 inspect，
再将返回的摘要和每个 Branch 的精确 REPORT ID 提交给 merge。参数及 Python
示例见[英文合同](branch-merge.md)；真实 stdio 完整可运行示例位于
`tests/test_fcop_mcp/test_branch_merge_stdio.py`。

同一 operation_id 同请求返回原 REVIEW；异请求为 `OPERATION_ID_CONFLICT`。
不同 operation_id 同内容复用原 REVIEW；同 Root/摘要不同内容为
`FAMILY_CONVERGENCE_MISMATCH`，拒绝零副作用。等价内容包括身份、规范摘要、
排序后的引用、NFC/LF 正文及可选 REVIEW 字段；不同发件人不视为等价。
旧 `write_review(review_kind="convergence")` 也走同一路径，无 operation_id
时由 Core 从请求导出稳定标识。精确重试返回历史结果，不代表家族仍未变化。

Core 先取工作区合并操作锁，再取一次既有家族锁；REVIEW 的无覆盖原子发布是
线性化点。PREPARED 收据保存经过验证的完整 REVIEW 字节及身份。复用既有
fsync、原子发布、收据替换和故障注入机制；重启重试只恢复这一份结果。
已提交结果丢失、收据损坏或字节冲突时 Fail Closed，不生成第二份 REVIEW。
尚无目标的 PREPARED 恢复必须重新验证当前家族。只读检查不会触发恢复。

汇合本身不改变规范家族内容，因此返回的旧/新摘要相同。不自动归档 Root、
不消费生命周期授权、不替调用者判断语义优劣，也没有数据库或后台组件。
