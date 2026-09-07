# FCoP 4.0 — compatibility

受众：business-agent。规则包：4.0.0-candidate.1。语言：zh。
主权威：冻结 Core aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6，spec/fcop-4.0-spec.md（中文对照 spec/fcop-4.0-spec.zh.md）。
本派生指引不产生执行、采用、Host 或发布授权。
显式选择依赖：workspace。

## F4.0.1

MUST/MUST NOT 为规范要求，SHOULD/MAY 为建议或许可；规则指引不能削弱规范要求。

## F4.0.2

冻结英文 Core 为主权威；中文条款、对象、边、错误及不变量必须等价，语言冲突阻断冻结/发布。

## F4.0.3

Schema 管可表达结构，规范管行为，测试验证而非发明规则。

## F4.1.2

FCoP 治理行为但不执行 Agent 工作、模型、工具、Host、会话、调度、数据库、UI、网络或进程；区分 Core、其 Specification、便捷 Toolkit、策略 Profile 与执行 Runtime。

## F4.1.3

Core 仅限 C1–C8：工作区身份、四信封、生命周期、四关系、证据/汇合、持久授权、创建幂等、可恢复原子语义。

## F4.1.4

不得把固定角色、EVAL、Ledger 信封、Git 分支/合并、CodeFlowMu 工作面、BCG、Relay、在线升级提升为 Core。

## F4.10.1

使用冻结的 31 项 Base 错误表，不由规则另建：workspace 5、envelope/relation 5、evidence 7、authorization 5、idempotency 1、state/recovery 8；精确拼写查 F4.10.1，各模块引用适用码，不新增 Base 码。

## F4.10.2

消费含操作及主题引用的结构化机器错误，不得仅从异常文字推测稳定错误码。

## F4.10.3

Toolkit/Profile 错误显式带命名空间，不替换或改释 Base 错误码。

## F4.11.1

v3 工作区在显式迁移前继续按 v3 读取；规则选择不是迁移或声明，不授予 4.0 写权限。

## F4.11.2

finish_task 及四个 history 工具为 LEGACY_V3_ONLY；4.0 Legacy 查询可读 history，不得将权威 TASK 移入。

## F4.11.3

fcop 是参考 Toolkit，fcop-mcp 是可选适配器；工具/资源目录不是 Core。保留名称按工作区版本路由，无法安全兼容时关闭失败；冻结条款中的历史数量不是新的分发目录。

## F4.11.4

Branch 是带 branch_of 的 TASK 创建，不要求新增 MCP 工具；下游目录漂移不会使 close_issue 成为官方表面。

## F4.11.5

Base MCP 保持薄的 stdio 适配；可选 Relay 及 upgrade/redeploy/GAL/workspace/session 能力属于 Toolkit/Profile/Runtime，不是 Core。

## F4.12.2

符合性证据须覆盖 C1–C8 正常、拒绝及适用竞态/恢复，包括六个 WP0 场景和冻结派生、Profile、字节摘要、family 竞态、幂等分层及五态恢复合同；仅有指引不证明符合性。

## F4.12.3

Schema、规范或测试冲突时停止发布，不允许静默覆盖；所有符合实现须满足相同可观察合同。

## F4.12.4

候选文档或规则包不授权实现、迁移、推送或发布；核对独立签署 Gate 和当前显式任务范围，不自动推进阶段。
