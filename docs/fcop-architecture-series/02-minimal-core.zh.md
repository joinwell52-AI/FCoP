# FCoP Core 到底是什么：从工具箱中提炼最小工作内核

[系列目录](README.md) · 第 2 / 5 篇 · [上一篇](01-work-beyond-context.zh.md) · [下一篇](03-architecture-layers.zh.md) · [五篇合集](collected.zh.md)

原稿：2026-09-01 · 发布修订：2026-09-10 · 对齐 FCoP 4.0.0

> 本文解释架构取舍；字段、迁移与错误以 [4.0 契约](../../spec/fcop-4.0-spec.zh.md)为准，版本状态见 [4.0.0 发布说明](https://github.com/joinwell52-AI/FCoP/releases/tag/v4.0.0)。原始设计建议已按当前版本修订；示意流程不等于可直接执行的 API 示例。

FCoP 发展到今天，已经不再只有几份规则。

它有 Library，有 MCP，有生命周期，有审查，有历史，也有越来越多用于真实工程的工具。

问题随之出现：

> **哪些东西是 FCoP，哪些东西只是 FCoP 提供的工具？**

如果这个问题不解决，协议每增加一个能力，Core 就会跟着膨胀。

最后可能得到一个功能越来越丰富的工具箱，却越来越难回答：

> **FCoP 最本质的东西究竟是什么？**

4.0 已将这一方向落实为 C1–C8 契约。下面先解释提炼 Core 的理由，再把概念映射到当前版本的完整要求。

---

## 一、Core 不是“所有已经实现的东西”

一个基础系统通常同时拥有：

```text
核心语义
公开合同
SDK
工具
参考实现
产品
```

这些不能混成一层。

Windows 有大量 API、SDK、PowerShell 命令、调试器和管理工具，但它们的总和不等于 Windows Kernel。

同样：

```text
fcop Python Library
fcop-mcp
CLI
Validator
Migration
Audit
Merge Helper
```

都可以属于 FCoP 生态。

但它们不能自动成为 FCoP Core。

否则：

```text
新增一个 MCP Tool
=
协议增加一个核心概念
```

Core 最终一定会失控。

---

## 二、判断是不是 Core，只问一个问题

假设有一个第三方开发者：

- 不安装官方 `fcop` Python 包；
- 不使用 `fcop-mcp`；
- 不使用 CodeFlowMu；
- 只拿到 FCoP Specification。

然后他用 TypeScript、Go 或 Rust 自己实现。

这时候应该问：

> **为了让这个实现与官方实现表达相同的工作意义，他必须理解哪些概念？**

这些跨实现必须一致的语义才有资格进入 Core。4.0 的边界还包括持久授权、创建幂等和可恢复原子语义，不限于对象名称。

反过来，如果一个能力不用理解也能保持相同工作语义，它就不是 Core。

这是非常重要的分界线。

---

## 三、第一个 Core 原理：正式工作行为必须外化

FCoP 最底层的问题并不是任务管理。

而是：

> **Agent 的正式工作行为不能只存在于 Agent 上下文里。**

因此可以把 FCoP 的第一条核心不变量写成：

> **Formal agent work behavior must be externalized into durable, attributable and inspectable work facts.**

中文就是：

> **Agent 的正式工作行为必须外化为持久、可归属、可检查的工作事实。**

文件是当前 reference realization。

更底层的 Core 是：

```text
Behavior
   ↓
Externalization
   ↓
Work Fact
```

---

## 四、TASK：正式委派

第一个最小对象是：

```text
TASK
```

为什么它属于 Core？

因为：

```text
“你顺便把测试跑一下。”
```

与：

```text
TASK-xxx
```

不是同一类工作事实。

前者是语言。

后者意味着：

> 一个正式工作对象被创建并进入可追踪的工作世界。

Core 不要求第三方复制官方 Python 类的方法签名；但规范规定的逻辑操作名称、字段、摘要和错误语义必须保持一致。例如创建摘要中的 `operation_kind` 在 4.0 固定为 `create_task`。

它只需要规定：

> **什么条件下，一个对象在 FCoP 语义中构成正式 TASK。**

---

## 五、REPORT：正式交付

第二个对象是：

```text
REPORT
```

它解决：

> 执行者的“我做完了”如何成为正式交付？

因此：

```text
Message
≠
REPORT
```

同时：

```text
REPORT
≠
Accepted
```

REPORT 记录的交付主张是：

> 有一个 Actor 针对某项正式工作提交了结果。

记录中的 Actor 归属需要结合来源和授权证据检查，不能仅凭姓名字符串证明实际操作者。

它不自动证明：

> 结果是真的。

也不自动证明：

> 结果已被组织接受。

这个区分应该长期稳定，因此属于 Core。

---

## 六、ISSUE：正式问题

第三个对象：

```text
ISSUE
```

Agent 在聊天中说：

```text
“这里可能有问题。”
```

并不能保证后续工作持续记住这个风险。

ISSUE 的意义是：

> **把问题本身外化成独立工作事实。**

因此：

```text
Concern
  ↓
ISSUE
```

意味着：

> 即使提出问题的 Agent 离开，问题也不能静默消失。

---

## 七、REVIEW：正式审查

第四个对象：

```text
REVIEW
```

如果执行者：

```text
执行
↓
自己判断完成
↓
自己宣布通过
```

那么系统并没有真正表达“独立审查”。

REVIEW 的 Core 含义不是规定：

> 所有任务都必须由 QA 审查。

而是：

> **协议能够表达另一个工作主体对既有交付进行了正式审查。**

所以：

```text
REPORT
≠
REVIEW
```

4.0 中，REVIEW 还可以表达授权、退回、重开、归档、汇合等事实；不是所有 REVIEW 都只是内容审稿。验收需要绑定当前 attempt 与 REPORT，并通过已采纳 Profile 的可信签发者判断，单独写一个“approved”字段不够。

至于 Reviewer 叫：

```text
QA
PM
Human
Judge Agent
External Reviewer
```

属于 Profile，不属于 Core。

---

## 八、Actor 与 Attribution

既然 FCoP 外化的是工作行为，就必须回答：

> **谁做的？**

一个没有归属的报告只有内容，没有责任来源。

因此 Core 至少需要：

```text
Actor
Attribution
```

但 Core 不应该固定：

```text
PM
DEV
QA
OPS
EVAL
ADMIN
```

这些是某种组织模型。

Core 只要求：

> 正式工作行为能够归属到明确 Actor。

---

## 九、Reference：工作对象必须能建立关系

TASK、REPORT、ISSUE、REVIEW 如果彼此没有引用，只是一堆独立文件。

FCoP 必须能表达：

```text
REPORT 属于哪个 TASK？
ISSUE 针对什么工作？
REVIEW 审查什么交付？
一个 TASK 是否由另一个 TASK 派生？
```

因此：

```text
Reference
```

属于 Core。

它使工作不再是一系列孤立记录，而形成可以重建的工作关系。

---

## 十、Lifecycle：当前状态与历史

正式工作除了“是什么”，还必须表达：

```text
现在在哪里？
怎么来到这里？
```

因此 Core 需要：

```text
Lifecycle
Transition
History
```

当前文件实现可以使用路径表达 NOW、transition 记录历史。

但：

```text
claim_task()
submit_task()
archive_task()
```

这些 API 名称不是 Core。

它们是参考 SDK 的操作表面；其对应的逻辑迁移仍受规范约束。4.0 没有 `active → done` 直达边，进入 `active` 会生成新 attempt，提交与验收分别经过 T3/T4，archive 是终态。

---

## 十一、Branch Relation 如何进入 Core

当多个 Agent 参与同一个 Root 工作时，不应该让所有 Agent 同时修改一个共享权威对象。

更稳健的方法是：

```text
ROOT TASK
├─ TASK A
├─ TASK B
└─ TASK C
```

其中每条 Branch 仍然是普通 TASK，只增加来源关系：

```yaml
branch_of: ROOT
```

因此：

```text
Branch relation
```

在 4.0 中属于 C4。

Core 需要表达的是：

> **一个正式 TASK 可以由另一个 TASK 派生，并独立形成自己的工作串。**

4.0 只允许同一 Root 下的同级 Branch；Branch 不能再成为 Branch Root。Core 不规定复杂度评分或 Git 合并算法，但 C5/C8 明确约束汇合证据、Root 归档条件和短暂任务族提交边界。

---

## 十二、Core 最重要的不变量

把以上概念进一步压缩，可以形成一组帮助理解设计的原则。下面的十点不是完整的 4.0 符合性清单，完整边界见第十五节 C1–C8：

```text
1. 正式工作不能只依赖模型上下文存在。

2. TASK 与普通消息不同。

3. REPORT 与普通消息不同。

4. REPORT 不自动等于 Accepted。

5. ISSUE 一旦正式产生，不能被后续过程静默抹除。

6. REVIEW 与被审查的交付是不同工作事实。

7. 当前状态必须存在唯一可检查表达。

8. 状态迁移必须可追溯。

9. 正式行为必须可以归属到 Actor。

10. 派生工作必须保留来源关系。
```

这些比任何具体工具名都更接近 FCoP Core。

---

## 十三、哪些明确不是 Core？

一旦 Core 被提炼出来，大量功能就可以重新归类。

例如：

```text
复杂度评分公式
警告阈值
MCP 工具名
Python Project API
具体 checkpoint 格式
Runtime 的调度重试策略
Git merge 的具体算法
CodeFlowMu 的 PM/QA/EVAL 固定角色
轨道机
```

这些具体实现或政策可能非常重要，但不是每个兼容实现都必须复制的算法。需要区分：C7 的持久创建幂等、C8 的恢复行为与阶段、授权迁移丢失响应后的重试规则，仍然是 4.0 Core 要求，不能整体归入可选工具。

因此应该进入：

```text
Toolkit
Policy
Profile
Runtime
```

而不是继续塞入 Core。

---

## 十四、文件是不是 Core？

这是最需要谨慎的地方。

今天 FCoP 是 file-first 的。

文件的优势非常真实：

```text
Agent 能读
人能读
脚本能读
IDE 能读
Git 能追踪
```

因此文件系统应该继续作为：

> **FCoP 的 reference carrier。**

但如果把理论继续往下抽象，最不可丢失的并不是 `.md` 后缀。

而是：

> **正式工作行为必须被持久外化。**

未来可以研究 SQLite 或其他存储编码，但保持这些对象名称只是起点。4.0 Base 目前限定具有可靠本地语义的受支持文件系统；新编码还需逐项满足 C1–C8、定义可观察行为并提供符合性证据，不能仅凭概念一致宣称兼容。

所以：

> 文件是今天最重要的载体。

> 行为外化才是最底层 Core 原理。

---

## 十五、4.0 将 Core 冻结为 C1–C8

前面讨论的 Actor、对象、关系与状态提供了理解入口，正式实现还必须回答身份、证据、权限、重复请求和部分失败问题。4.0 用八项契约固定这些要求：

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

完整条款见 [4.0 规范 §2–§9、§13](../../spec/fcop-4.0-spec.zh.md)。对象语义、兼容性要求与 Python/MCP 工具目录分别维护，不能用工具数量替代契约覆盖。

---

## 十六、Core 小，并不意味着 FCoP 功能少

成熟基础系统通常是：

```text
Core
很小

Toolkit
很强
```

下面列出的是生态工具的分类方向，不是 4.0 安装包逐项交付清单：

```text
Python SDK
MCP Server
CLI
Inspector
Migration
Audit
Merge Helper
Branch Helper
Recovery Helper
Conformance Suite
Adapters
```

甚至工具数量继续增加也没有问题。

因为：

> **工具数量不再等于协议复杂度。**

真正需要多年保持稳定的，是 Core。

---

## 结语：先知道什么不能变

软件升级最容易做的是增加功能。

最难的是知道：

> **哪些东西不应该跟着功能一起变化？**

对于 FCoP，这个答案正在变得清楚。

它不是某一个 Python 类。

不是几十个 MCP Tool。

不是 PM、DEV、QA 的固定组织结构。

也不是某个复杂度算法。

它最底层的承诺是：

> **Agent 的正式工作行为必须脱离模型上下文，成为持久、可归属、可检查、可追溯的工作事实。**

TASK、REPORT、ISSUE、REVIEW、关系与生命周期构成理解这套工作语言的入口；4.0 还通过 C1–C8 约束身份、授权、证据、创建幂等和原子恢复。

工具可以变化。

Runtime 可以变化。

模型可以变化。

Host 可以变化。

但如果这些工作事实依然成立，FCoP 的 Core 就还在那里。

---

## 实现与延伸阅读

- [4.0 规范](../../spec/fcop-4.0-spec.zh.md)：核对 C1–C8、授权、幂等与恢复条款。
- [Python v4 实现](../../src/fcop/v4/)与[符合性测试](../../tests/conformance/)：核对契约的具体落点。
- [快速试用](../../README.zh.md#try-it) · [MCP 接入](../../README.zh.md#mcp) · [架构概览](../architecture.zh.md)。

[系列目录](README.md) · 第 2 / 5 篇 · [上一篇](01-work-beyond-context.zh.md) · [下一篇](03-architecture-layers.zh.md) · [五篇合集](collected.zh.md)
