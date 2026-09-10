# FCoP 架构原理系列：让 Agent 的工作站到模型之外

[返回 FCoP](../../README.zh.md) · [架构概览](../architecture.zh.md) · [English overview](../architecture.en.md) · **[五篇全文合集](collected.zh.md)**

**五篇全文已公开。** 原稿写于 2026-09-01，本次于 2026-09-10 修订发布，按 FCoP 4.0.0 的 C1–C8 契约核对。系列解释设计动机与工程取舍，供希望理解、使用或独立实现 FCoP 的读者阅读。

> **Agent 的正式工作怎样脱离模型上下文持续存在？**

## 五篇文章

| 顺序 | 全文 | 核心问题 |
|---|---|---|
| 01 | [Agent 没有操作系统：为什么 FCoP 选择把工作行为外化到文件系统](01-work-beyond-context.zh.md) | 为什么工作需要持久对象，为什么采用文件系统？ |
| 02 | [FCoP Core 到底是什么：从工具箱中提炼最小工作内核](02-minimal-core.zh.md) | 哪些跨实现语义必须一致，4.0 的 C1–C8 包含什么？ |
| 03 | [FCoP 不等于它的工具：Core、Specification、Toolkit、Profile 与 Runtime 如何分层](03-architecture-layers.zh.md) | 核心、规范、符合性、工具、策略与运行时如何分工？ |
| 04 | [单机多 Agent 为什么不追求高并发：从共享写入到“多串行形成并行”](04-parallel-work.zh.md) | 多条工作流如何并行，Root 如何核对当前交付并收尾？ |
| 05 | [从单机到联网：FCoP、MCP、A2A 与 CodeFlowMu 各自负责什么](05-mcp-a2a-runtime.zh.md) | 工具访问、工作事实、持续执行与跨系统通信如何组合？ |

可以从第一篇了解设计起点，也可以直接选择自己关心的问题。每篇都有前后导航；[五篇合集](collected.zh.md)适合连续阅读和保存。

## 从设计原则到 4.0 契约

```text
工作需要站到模型之外
  → 形成持久工作对象
  → 提炼 C1–C8 的共同语义
  → 分开规范、工具、策略与运行时
  → 各自执行，按当前证据汇合
  → 由适配层连接工具与外部 Agent 系统
```

| 契约 | 必须保持的工作语义 |
|---|---|
| C1 工作区身份 | 稳定 workspace ID，以及显式 fork 的身份边界。 |
| C2 四类信封 | TASK、REPORT、ISSUE、REVIEW 的结构、归属与追加事实。 |
| C3 生命周期 | 单一权威路径、七条合法迁移、追加事件；没有 active → done。 |
| C4 关系 | parent、branch_of、subject_ref、references；Branch 仅限同级。 |
| C5 证据与收敛 | 当前 attempt、有效 REPORT、验收证据及 Root 的汇合条件。 |
| C6 持久授权 | 绑定工作与证据的 REVIEW，由已采纳 Profile 判断签发权限。 |
| C7 创建幂等 | 创建 TASK/Branch 使用稳定 operation_id 和规范化请求摘要。 |
| C8 原子恢复 | 持久回执、明确恢复分类、拒绝歧义以及任务族的短暂提交边界。 |

## 这次发布修订了什么

- 保留五篇原文的完整论证与章节脉络，将“下一版提取 Core”的建议更新为已发布 4.0 的实际入口。
- 用 C1–C8 对齐原始概念枚举，补充创建幂等、持久授权和原子恢复，避免把它们全部归为可选工具。
- 明确 Branch 仅限同级、证据属于当前 attempt、Root 汇合与归档授权分开；短暂协议提交边界不锁住 Agent 整段工作。
- 其他存储、Windows/Linux 跨节点部署及 A2A 映射作为设计方向说明；当前 4.0 未据此宣称交付 A2A 适配器或多机共享工作区。

原始 WP0 草稿留在原归档中，本目录是经过修订的公开版。[清单](manifest.json)记录五篇文件与出版信息。合集由同一组单篇正文组成，单篇为维护入口。

## 规范、试用与产品入口

- **协议与实现：** [4.0 契约](../../spec/fcop-4.0-spec.zh.md)、[v4 源码](../../src/fcop/v4/)、[符合性测试](../../tests/conformance/)。契约文件保留形成时的候选标题，当前版本发布状态以 [v4.0.0 发布记录](https://github.com/joinwell52-AI/FCoP/releases/tag/v4.0.0)为准。
- **直接试用：** [Python 示例](../../README.zh.md#try-it)、[MCP 接入](../../README.zh.md#mcp)、[4.0 接入指南](../fcop-4.0-progress.md)。
- **研究传播：** [joinwell52](https://github.com/joinwell52-AI/joinwell52)。
- **产品体验：** [CodeflowMu-Distribution](https://github.com/joinwell52-AI/CodeflowMu-Distribution)，兼容范围以其发布说明为准。

如果这套设计对你的 Agent 工作有帮助，欢迎 [Star FCoP](https://github.com/joinwell52-AI/FCoP) 收藏，或通过 [Issues](https://github.com/joinwell52-AI/FCoP/issues)交流接入经验与可复现问题。
