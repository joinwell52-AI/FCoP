# FCoP 架构原理系列 · 五篇全文合集

[系列目录](README.md) · [返回 FCoP](../../README.zh.md)

原稿：2026-09-01 · 发布修订：2026-09-10 · 对齐 FCoP 4.0.0

本页汇集五篇已发布正文。可以连续阅读，也可以从目录跳转；修订时以各单篇为维护入口并同步本合集。

1. [Agent 没有操作系统：为什么 FCoP 选择把工作行为外化到文件系统](#article-1)
2. [FCoP Core 到底是什么：从工具箱中提炼最小工作内核](#article-2)
3. [FCoP 不等于它的工具：Core、Specification、Toolkit、Profile 与 Runtime 如何分层](#article-3)
4. [单机多 Agent 为什么不追求高并发：从共享写入到“多串行形成并行”](#article-4)
5. [从单机到联网：FCoP、MCP、A2A 与 CodeFlowMu 各自负责什么](#article-5)

---

<a id="article-1"></a>

## Agent 没有操作系统：为什么 FCoP 选择把工作行为外化到文件系统

[系列目录](README.md) · 第 1 / 5 篇 · [下一篇](02-minimal-core.zh.md) · [五篇合集](collected.zh.md)

原稿：2026-09-01 · 发布修订：2026-09-10 · 对齐 FCoP 4.0.0

> 本文解释架构取舍；字段、迁移与错误以 [4.0 契约](../../spec/fcop-4.0-spec.zh.md)为准，版本状态见 [4.0.0 发布说明](https://github.com/joinwell52-AI/FCoP/releases/tag/v4.0.0)。原始设计建议已按当前版本修订；示意流程不等于可直接执行的 API 示例。

今天的大模型可以写代码、查资料、调用工具、分析数据，甚至连续执行很长的任务。

但有一个很容易被忽略的问题：

> **Agent 并不拥有自己的操作系统。**

这里说“没有操作系统”，不是说 Agent 脱离 Windows、Linux 或其他 Host 运行。恰恰相反，Agent 的文件、进程、网络、时钟、权限和持久化能力，都来自 Host、Runtime 和操作系统。模型本身并不天然拥有这些能力。

Agent 可以说：

> “我接下这个任务。”

也可以说：

> “我已经完成。”

甚至可以说：

> “问题已经修复并通过验证。”

但如果这些行为只存在于模型上下文或聊天记录里，它们不会天然成为持续存在的工作事实。会话关闭、上下文压缩、Host 重启、模型切换，甚至一次响应丢失，都可能让“刚才到底发生了什么”重新变得模糊。

FCoP 最初真正要解决的，就是这个问题。

它没有选择给 Agent 再造一个操作系统，也没有首先建立数据库、消息队列或分布式控制平面，而是采取了一条更直接的路线：

> **把 Agent 的正式工作行为外化。**

在单机系统里，最自然的外化界面就是文件系统。

---

### 一、Agent 很强，但它没有天然持久的“工作世界”

一个 Agent 最基础的工作条件通常只有：

```text
模型
+
当前上下文
+
Host 暴露的工具
```

它自己并不天然拥有：

```text
持久文件系统
进程系统
系统时钟
事务机制
可靠状态机
用户权限系统
长期任务账本
```

这些能力属于操作系统和 Runtime。

因此：

```text
Agent:
“我已经接手 TASK-12”
```

首先只是一个语言行为。

如果没有外部状态承载：

```text
Agent Context
      ×
```

这项“接手”就可能和上下文一起消失。

这就是“Agent 能做事”与“Agent 能持续承担工作”之间的差别。

数字员工如果要真正承担岗位责任，工作状态不能依赖模型记得住。

---

### 二、为什么保存聊天还不够？

最简单的办法似乎是：把所有聊天记录保存下来。

但这仍然没有解决问题。

因为：

```text
“我准备开始。”
“应该快完成了。”
“我觉得这个版本没问题。”
```

这些都是语言表达，不等于正式工作行为。

FCoP 因此把少数具有明确工作意义的行为外化成正式对象：

```text
TASK
REPORT
ISSUE
REVIEW
```

例如：

```text
“请把 Windows 安装流程补齐”
```

只有被外化为 `TASK`，才成为正式委派。

执行者说：

```text
“我完成了。”
```

不会自动把任务变成成功，而是形成一个 `REPORT`：执行者正式提交了结果。

发现故障：

```text
ISSUE
```

独立检查：

```text
REVIEW
```

这一步的意义不是“把聊天换成 Markdown”。

真正发生的是：

```text
Agent 内部行为
        ↓
       外化
        ↓
操作系统中的持久工作对象
```

也就是说：

> **工作不再只活在模型上下文里。**

---

### 三、为什么是文件，而不是数据库？

FCoP 完全可以从一开始就选择数据库：

```text
tasks
reports
issues
reviews
```

也可以选择消息队列：

```text
Kafka
RabbitMQ
Redis Streams
```

甚至建立完整中心服务：

```text
Agent
  ↓
SDK
  ↓
API
  ↓
Workflow Service
  ↓
Database
```

这些方案可以针对高并发、事务和跨机器通信提供不同的工程能力；具体取舍仍要看负载与实现。本文没有进行吞吐量基准比较。

但 FCoP 面对的第一目标并不是高并发，而是：

> **怎样用最低复杂度，让单机里的多个 Agent 拥有一个脱离模型上下文的共同工作世界？**

文件在这个问题上有几个特殊优势。

第一，Agent 天然会读写文件。

第二，人也能直接阅读。

第三，IDE、脚本、Git、备份工具都能直接处理文件。

因此同一个工作对象可以同时服务于：

```text
Agent
人
IDE
脚本
Git
审计程序
```

这使文件成为一个非常低摩擦的共同表面。

FCoP 并不是在证明：

> “文件比数据库先进。”

它真正利用的是：

> **在单机 Agent 场景里，文件是行为外化成本最低、可观察性最高的公共界面之一。**

---

### 四、Filesystem as Behavioral Externalization Surface

过去常用一句话描述 FCoP：

> Filename as Protocol.

这仍然有意义。

但如果继续往底层追，FCoP 更核心的思想其实是：

> **Filesystem as Behavioral Externalization Surface.**

也就是：

> **文件系统是 Agent 正式工作行为的外化界面。**

以下路径省略了共同前缀 `fcop/_lifecycle/`，用于说明状态；它们不是手动搬动文件的操作教程。

例如：

```text
inbox/TASK-001.md
```

经过合法领取以后进入：

```text
active/TASK-001.md
```

这不是简单的文件整理。

它表达一个正式状态变化：

> TASK-001 已经从待领取进入执行状态。

提交以后进入：

```text
review/TASK-001.md
```

又表达：

> 执行者已经形成正式交付，现在等待审查。

目录不是装饰。

文件也不只是数据容器。

它们共同构成 Agent 工作行为在操作系统中的持续投影。

---

### 五、单机并不意味着“没有并行”

FCoP 的单机设计经常会引出一个问题：

> Windows 或普通文件系统又不是高并发任务平台，多 Agent 怎么并行？

答案不是让多个 Agent 同时竞争修改一个共享文件。

而是：

> **让多个独立工作串并行。**

例如：

```text
TASK-001 → DEV-01
TASK-002 → DEV-02
TASK-003 → QA
TASK-004 → OPS
```

这些工作可以同时进行。

这是：

> **工作级并行。**

但对于同一个正式对象：

```text
TASK-001
```

FCoP 并不追求：

```text
DEV-01 ─┐
DEV-02 ─┼→ 同时修改同一权威状态
PM     ─┤
QA     ─┘
```

更合理的模式是：

```text
一个正式对象
    ↓
明确工作归属
    ↓
经过校验的状态迁移
```

因此：

> **FCoP 支持多任务并行，但不以同一治理对象的多写者高并发为设计目标。**

---

### 六、一致性比 TPS 更重要

数据库和消息系统经常问：

> 每秒能处理多少请求？

数字员工面对的关键问题往往不同：

```text
任务有没有重复领取？
REPORT 是谁提交的？
失败之后有没有被误写成成功？
系统重启以后还能不能恢复？
当前状态为什么是合法的？
谁审查过这项交付？
```

这些问题的核心不是吞吐量，而是：

> **工作事实是否稳定。**

因此 FCoP 的设计优先级更接近：

```text
一致性
>
可恢复性
>
可检查性
>
可审计性
>
吞吐量
```

这不是说性能不重要。

而是明确：

> FCoP 优化的不是数据中心级高并发，而是单机多 Agent 正式工作的稳定性。

---

### 七、状态落到路径，正确提交还需要原子恢复

例如：

```text
inbox/TASK-001.md
        ↓
active/TASK-001.md
```

FCoP 使用操作系统文件语义，并不是为了构建一个高速消息队列。

它要获得的是一个非常简单但强的性质：

> **成功提交后，同一个工作对象应具有唯一可检查的正式生命周期位置。**

4.0 不承诺跨目录迁移永远没有中间状态。参考实现还使用持久操作回执、摘要校验和恢复分类。若同一个 TASK 同时出现在多个权威阶段，读取必须拒绝歧义，不能按修改时间猜测。单次 `rename` 不能替代这套协议提交与恢复条件（[规范 §9](../../spec/fcop-4.0-spec.zh.md)）。

这能让人和 Agent 直接检查：

```text
它现在在哪里？
```

而不必先向一个隐藏状态服务发起复杂查询。

对于单机工作系统，这是一种非常实用的取舍。

---

### 八、FCoP 不应该承担联网

当 FCoP 被理解为“单机 Agent 行为外化”，另一个边界也自然清楚了。

它没有必要继续扩张去承担：

```text
Agent discovery
OAuth
mTLS
跨机器路由
streaming
webhook
remote task
跨云互操作
```

这些问题属于网络互操作层。

A2A 更适合处理：

```text
Agent System A
       ↕
      A2A
       ↕
Agent System B
```

FCoP 则处理：

```text
一个 Agent 系统内部
Agent 行为
    ↓
正式工作对象
```

因此：

> **在本文提出的组合方式中，FCoP 保存本地工作事实，A2A 承担跨 Agent 系统交互。**

这是一种架构分工，不是已交付集成声明。A2A 本身也定义任务与产物语义；认证和通信策略仍需由实现者部署。第五篇具体讨论两者的映射边界。

---

### 九、FCoP 也不等于 Runtime

把行为写入文件还不等于数字员工已经可靠运行。

真正的 Runtime 还需要解决：

```text
Session
Attempt
Lease
Timer
Retry
Recovery
Host
Model
Tool execution
Crash recovery
```

这些是 CodeFlowMu 一类 Runtime 要处理的运行问题。这里的 Runtime attempt 与 FCoP 4.0 用来绑定交付证据的 `attempt_id` 是不同层次的身份，不应混用；协议文件提交的崩溃恢复仍属于 C8。

CodeFlowMu 的具体已实现功能和兼容版本以 [CodeflowMu-Distribution 发布说明](https://github.com/joinwell52-AI/CodeflowMu-Distribution/releases)为准。

所以可以分开理解：

```text
Agent
  ↓
FCoP
工作行为外化

CodeFlowMu Runtime
  ↓
持续执行与恢复
```

FCoP 不应该因为 Runtime 很重要，就把 Runtime 全部吸收到自己里面。

---

### 十、文件是载体，行为外化才是核心

如果未来 FCoP 出现：

```text
SQLite adapter
Object-store adapter
Database-backed implementation
```

它是否还可以被视为 FCoP？

这是一种未来的抽象方向，不是 4.0 已提供的存储适配能力。当前 Base 明确限定受支持、具有可靠本地语义的 NTFS/POSIX 文件系统。

将来讨论新的兼容编码时，判断不应只看 `.md`。

更重要的是它是否仍然保留：

```text
TASK 是正式委派
REPORT 是正式交付
ISSUE 是正式问题
REVIEW 是正式审查
状态迁移有明确含义
工作事实不依赖模型记忆存在
```

所以：

> **文件系统是 FCoP 今天的 reference carrier。**

而：

> **Agent 工作行为外化，是更底层的设计原则。**

但设计原则本身不足以授予 4.0 兼容性。其他存储需要明确编码、C1–C8 全部契约和相应符合性证据；仅保存四类对象还不够。

---

### 十一、单机不是落后，而是边界清楚

云原生时代很容易形成一种误解：

> 只有分布式才先进。

但一个软件开发数字员工一天可能只处理：

- 几个正式开发任务；
- 若干审查；
- 一轮测试；
- 几次故障恢复；
- 几份正式交付。

它真正需要的不是每秒十万次状态变更。

更重要的是：

> 明天重新打开系统以后，它还知不知道昨天做到哪里？

> 另一个 Agent 接手以后，能不能看懂之前发生了什么？

> 系统能不能区分“执行者说完成”和“真正被接受”？

> 出错以后，能不能根据外部事实恢复，而不是依赖模型回忆？

在这样的负载下：

> **低并发、强状态、强可观察、强恢复**

可以是一种非常合理的工程选择。

---

### 结语：即使模型离开了，工作依然在那里

FCoP 表面上看，是用文件组织多个 Agent。

继续往下推，它真正面对的是一个更基础的问题：

> **当 Agent 不拥有自己的操作系统、没有天然持久的工作事实时，工作怎样才能持续存在？**

FCoP 的回答很朴素：

> 借用单机操作系统最成熟的持久化界面，把 Agent 的正式工作行为外化出来。

它接受自己的边界：

```text
单机优先
受控并行
不承担联网
不承担完整 Runtime
不追求数据库级吞吐
```

换来的则是：

```text
可见
可读
可恢复
可追踪
可审查
可持续
```

因此，FCoP 不应该只被描述成“文件通信协议”。

更准确的理解是：

> **FCoP 是面向单机多 Agent 系统的工作行为外化机制：它把任务、交付、问题和审查从易失的模型上下文转化为持久、可检查的工作对象。**

数字员工真正成熟的标志，也许并不是模型能够完成越来越复杂的任务。

而是：

> **即使模型离开了，工作依然在那里。**

---

### 实现与延伸阅读

- [4.0 规范](../../spec/fcop-4.0-spec.zh.md)：核对 C1–C8、授权、幂等与恢复条款。
- [Python v4 实现](../../src/fcop/v4/)与[符合性测试](../../tests/conformance/)：核对契约的具体落点。
- [快速试用](../../README.zh.md#try-it) · [MCP 接入](../../README.zh.md#mcp) · [架构概览](../architecture.zh.md)。

[系列目录](README.md) · 第 1 / 5 篇 · [下一篇](02-minimal-core.zh.md) · [五篇合集](collected.zh.md)

---

<a id="article-2"></a>

## FCoP Core 到底是什么：从工具箱中提炼最小工作内核

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

### 一、Core 不是“所有已经实现的东西”

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

### 二、判断是不是 Core，只问一个问题

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

### 三、第一个 Core 原理：正式工作行为必须外化

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

### 四、TASK：正式委派

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

### 五、REPORT：正式交付

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

### 六、ISSUE：正式问题

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

### 七、REVIEW：正式审查

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

### 八、Actor 与 Attribution

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

### 九、Reference：工作对象必须能建立关系

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

### 十、Lifecycle：当前状态与历史

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

### 十一、Branch Relation 如何进入 Core

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

### 十二、Core 最重要的不变量

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

### 十三、哪些明确不是 Core？

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

### 十四、文件是不是 Core？

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

### 十五、4.0 将 Core 冻结为 C1–C8

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

### 十六、Core 小，并不意味着 FCoP 功能少

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

### 结语：先知道什么不能变

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

### 实现与延伸阅读

- [4.0 规范](../../spec/fcop-4.0-spec.zh.md)：核对 C1–C8、授权、幂等与恢复条款。
- [Python v4 实现](../../src/fcop/v4/)与[符合性测试](../../tests/conformance/)：核对契约的具体落点。
- [快速试用](../../README.zh.md#try-it) · [MCP 接入](../../README.zh.md#mcp) · [架构概览](../architecture.zh.md)。

[系列目录](README.md) · 第 2 / 5 篇 · [上一篇](01-work-beyond-context.zh.md) · [下一篇](03-architecture-layers.zh.md) · [五篇合集](collected.zh.md)

---

<a id="article-3"></a>

## FCoP 不等于它的工具：Core、Specification、Toolkit、Profile 与 Runtime 如何分层

[系列目录](README.md) · 第 3 / 5 篇 · [上一篇](02-minimal-core.zh.md) · [下一篇](04-parallel-work.zh.md) · [五篇合集](collected.zh.md)

原稿：2026-09-01 · 发布修订：2026-09-10 · 对齐 FCoP 4.0.0

> 本文解释架构取舍；字段、迁移与错误以 [4.0 契约](../../spec/fcop-4.0-spec.zh.md)为准，版本状态见 [4.0.0 发布说明](https://github.com/joinwell52-AI/FCoP/releases/tag/v4.0.0)。原始设计建议已按当前版本修订；示意流程不等于可直接执行的 API 示例。

当一个系统只有几个功能时，人们很少讨论分层。

但当它逐渐拥有：

```text
Library
MCP
Schema
Lifecycle
Audit
Migration
Validation
Branch
Merge
Recovery
```

问题就出现了：

> **这些东西是不是全部都属于 FCoP 本身？**

如果答案一直是“是”，FCoP 最终就会变成一个不断膨胀的整体。

这并不是功能太多的问题。

而是：

> **核心、合同、工具、组织配置和运行时没有被明确分开。**

---

### 一、Windows 给出的启示：平台不等于工具总和

Windows 拥有大量：

```text
API
SDK
PowerShell
CMD
Debugger
Sysinternals
Visual Studio
Management Tools
```

但开发者不会认为：

> PowerShell 就是 Windows Kernel。

因为它们处在不同层。

可以简化成：

```text
Windows Core
      ↓
Platform Contract / API
      ↓
SDK
      ↓
Tools
      ↓
Applications
```

一个开发者开发 Windows 软件，并不需要使用微软所有工具。

他真正必须遵守的是：

> Windows 对外提供的平台合同。

例如：

```text
文件有什么语义
进程如何创建
权限如何判断
API 的输入输出如何解释
```

至于使用 C++、Rust、Python、Visual Studio 还是其他工具，并不改变这一点。

FCoP 也需要同样的分层。

---

### 二、第一层：FCoP Core

最底层是：

```text
FCoP Core
```

Core 不应该包含某个具体 Python API，也不应该包含所有 MCP Tool。

它定义：

> **FCoP 工作世界里哪些概念具有稳定意义。**

例如：

```text
Actor
TASK
REPORT
ISSUE
REVIEW

Reference
Attribution
Branch

Lifecycle
Transition
History
```

以及最基本的原则：

> 正式 Agent 工作行为必须被外化。

以上是概念层的理解入口。正式 4.0 Core 为 C1–C8：工作区身份、四类信封、生命周期、关系、证据与汇合、持久授权、创建幂等和原子恢复。Core 应该小而稳定，但不能省去错误、授权和部分失败语义。

---

### 三、第二层：FCoP Specification

Core 定义必须共同遵守的语义与不变量。

要让别人可以独立实现，需要：

```text
Specification
```

Specification 回答：

```text
什么叫合法 TASK？
REPORT 如何引用 TASK？
哪些状态迁移合法？
当前状态怎样表达？
历史怎样保留？
Branch 与 Root 的关系如何表达？
```

它类似一个平台公开合同。

第三方真正需要遵守的是：

> **Specification。**

而不是复制官方 Python 源代码。

---

### 四、第三层：Conformance

如果只有规范，没有符合性测试，很容易出现：

```text
Python 认为合法
TypeScript 认为非法
第三方实现又有第三种解释
```

因此还需要：

```text
Conformance Suite
```

例如：

```text
TASK parsing              PASS
TASK lifecycle            PASS
REPORT reference          PASS
Illegal transition        PASS
Branch relation           PASS
History reconstruction    PASS
```

这样第三方才能真正回答：

> **我的实现是不是 FCoP-compatible？**

上面的 PASS 列表示意测试覆盖项，不是新增测试的运行结果。Conformance 是横跨实现的验证平面，而非每次操作必经的一层服务。成熟基础层需要可验证兼容；可从仓库的[符合性测试](../../tests/conformance/)核对具体证据。

---

### 五、第四层：FCoP Toolkit

再往上才是大量实际工具：

```text
FCoP Toolkit
```

以下是工具分类示例，包含可发展方向，不是当前版本的完整交付清单：

```text
Python SDK
MCP Server
CLI
Validator
Inspector
Migration
Audit
Branch helper
Merge helper
Recovery helper
```

Toolkit 的职责不是定义 FCoP 是什么。

而是：

> **让开发者更容易正确实现和使用 FCoP。**

例如 `Project.create_task(...)` 是 SDK 入口；这里省略必需参数，实际可运行代码见 [README 示例](../../README.zh.md#try-it)。

Core 要求的是：

> 最终产生的 TASK 符合规范。

所以：

```text
API 名称
≠
协议语义
```

---

### 六、第五层：Profile

再往上是：

```text
Profile
```

Profile 描述：

> 某个具体组织怎样使用 FCoP。

CodeFlowMu 可以定义：

```text
PM
DEV
QA
OPS
EVAL
ADMIN
```

以及：

```text
谁能创建 TASK
谁能提交 REPORT
谁负责 REVIEW
谁负责协调
谁只能观察
谁拥有人工最终权限
```

这些设计可以非常重要。

但它们属于：

> **CodeFlowMu 的组织 Profile。**

不是所有 FCoP 实现必须采用的角色结构。

其他系统完全可以定义：

```text
Lead
Researcher
Reviewer
Human
```

或者：

```text
Planner
Worker
Validator
```

但“声明谁有权限”与“权限被可信宿主验证”是两回事。4.0 工作区需显式采纳授权 Profile，由可信宿主注册签发者评估器；只有 `AUTHORIZED` 通过。角色名或请求中的 `profile_ref` 不能自行赋权，缺少可用 Profile 时 T4–T7 会拒绝执行。

---

### 七、第六层：Runtime

最后是：

```text
Runtime
```

Runtime 解决：

```text
Agent 什么时候启动？
使用哪个模型？
Session 怎么保持？
Worker 挂了怎么办？
Lease 怎么恢复？
Timer 怎么触发？
响应丢失以后怎么重试？
Host 怎么连接？
```

这些问题很重要。

但它们不是：

> “工作行为是什么意思？”

它们属于：

> **工作怎样真正运行。**

CodeFlowMu 的产品定位位于这一层。上述是 Runtime 职责分类，实际功能和版本支持应查看 [CodeflowMu-Distribution](https://github.com/joinwell52-AI/CodeflowMu-Distribution/releases)。

因此：

```text
FCoP
≠
CodeFlowMu
```

一个定义正式工作表达。

另一个让 Agent 真正持续执行这些工作。

---

### 八、完整结构

可以按依赖与职责理解，而不是把所有名字画成一条运行调用链：

```text
Runtime（模型、会话、调度、工具执行与界面）
    │ 使用
    ├── Toolkit（Python 实现、MCP 适配及工具）
    └── Profile（显式采纳的组织与授权策略）
              │ 必须遵守
Specification（字段、迁移、错误与可观察行为）
              │ 精确表达
Core C1–C8（跨实现不变量）

Conformance：横向验证实现是否满足规范
```

Profile 的授权判断参与指定迁移，但不能改变 Base 状态机。Conformance 检查契约，并不负责日常调度。这样每层可以独立增长，同时保持共同工作语义。

---

### 九、用这个分层重新看 Branch

Branch 很适合作为分层示例。

关系层可以用下面的省略示意表达：

```yaml
branch_of: ROOT
```

它表示：

> 这个 TASK 是某个 Root TASK 派生的独立工作线。

这是工作事实，4.0 在 C4 固定了 sibling-only 关系，在 C5/C8 固定了汇合和提交边界；并非只增加一个字段就完成全部语义。

而：

```text
create_task(..., branch_of=root_task_id)
```

只是 SDK API。

两者不应该混同。

---

### 十、复杂度评分属于 Toolkit 或 Policy

如果为了避免 Branch 失控，引入：

```text
branch_count
overlap_count
unresolved_count
```

这些客观事实可以成为工具输入。

但如果进一步定义：

```text
score = 某个权重公式
warn = 某个阈值
reject = 某个阈值
```

这已经是策略。

策略未来应该能够调整，而不需要修改 TASK、REPORT 或 REVIEW 的含义。

因此它更适合：

```text
Toolkit
或
CodeFlowMu Policy
```

而不是 Core。

---

### 十一、角色属于 Profile

如果某个实现规定：

```text
PM 负责协调
QA 负责审查
EVAL 只能观察
ADMIN 负责最终授权
```

这是一个具体组织设计。

FCoP Core 更应该表达：

```text
Actor
Authority
Attribution
```

然后 Profile 再映射：

```text
decision authority = PM
review authority = QA
observer = EVAL
human authority = ADMIN
```

这样 FCoP 才不会被某一种组织结构锁死。

---

### 十二、Merge 要区分“语义”和“参考实现”

“多个 Branch 最终必须形成可识别的收敛结果”可以是工作语义。

但：

```text
PREPARE
BUILD
VERIFY
COMMIT
MERGED
```

以及：

```text
Base
Candidate
checkpoint
AlreadyCommitted
Recovery
```

是原始架构讨论用来区分算法与语义的 Merge Toolkit 设计词汇，不是 4.0 新增的统一公开状态机。C8 自己规定的 receipt 阶段和恢复分类仍须遵守。

第三方可以实现另外一种可靠收敛方法，但这不允许更换 4.0 的授权、证据摘要或恢复合同。Root 有 Branch 时，归档必须校验各分支终态、当前 attempt 的 REPORT、准确的 convergence REVIEW、`family_digest` 和独立归档授权；Git 代码合并由应用负责。

这就是：

```text
Semantic Contract
≠
Reference Algorithm
```

---

### 十三、工具多不是问题，混层才是问题

如果所有 MCP Tool 都被解释为：

> FCoP 本身，

工具越多，FCoP 就越显得笨重。

但如果结构是：

```text
FCoP Core
少量稳定概念

FCoP Toolkit
大量可选工具
```

问题就完全不同了。

真正需要控制的是：

> **默认暴露给某一个 Agent 的工具表面有多大。**

普通 Worker 可能只需要：

```text
read task
claim
submit report
open issue
```

Reviewer 可能只需要：

```text
read report
review
```

宿主可以按需要设计工具选择策略；这不表示当前 MCP 适配器已提供按角色动态裁剪的功能。

---

### 十四、4.0 已经如何落实这条路线？

原始草稿提出先形成 Core 边界、再进行实现。现在可以直接核对 4.0 的成果：

1. [规范](../../spec/fcop-4.0-spec.zh.md)明确 C1–C8 及各层职责。
2. [v4 实现](../../src/fcop/v4/)将创建、生命周期、授权、汇合和恢复分开组织。
3. [符合性测试](../../tests/conformance/)提供可核对的行为证据。
4. [规则分发契约](../fcop-4.0/rule-distribution-contract.zh.md)区分采纳、部署和宿主投影。

原文建议的 `FCOP-CORE-BOUNDARY.md` 是当时拟议的文件名；当前实现者应以上述实际文档为入口。

---

### 十五、后续演进继续遵守契约优先

这条路线仍可作为后续演进方法，下面是设计流程，不是新的版本排期：

```text
现有 FCoP
   ↓
Core Extraction
   ↓
Core Boundary Freeze
   ↓
Specification
   ↓
Conformance
   ↓
Amendment 分类
   ↓
Toolkit Implementation
   ↓
Profile Integration
   ↓
Runtime Integration
```

而不是：

```text
发现新问题
   ↓
加规则
   ↓
加 Library API
   ↓
加 MCP Tool
   ↓
全部继续叫 FCoP Core
```

前者在建设平台。

后者只会产生越来越大的工具箱。

---

### 结语：强大的系统，核心通常很小

FCoP 不需要停止成长。

它真正需要的是：

> **让增长发生在正确的层。**

最终：

```text
Core
定义工作世界的基本规律

Specification
公开这些规律

Conformance
证明实现没有偏离

Toolkit
让这些规律容易使用

Profile
定义具体组织怎样工作

Runtime
让工作真正持续运行
```

当层次稳定以后，新的 Inspector、A2A 适配器或 Runtime 集成可以在各自边界内演进；如果确实改变 Core 的外部行为，则必须走规范变更和符合性验证，不能用“只是工具”掩盖语义变化。

> **Core 小而稳定，生态才能大而自由。**

---

### 实现与延伸阅读

- [4.0 规范](../../spec/fcop-4.0-spec.zh.md)：核对 C1–C8、授权、幂等与恢复条款。
- [Python v4 实现](../../src/fcop/v4/)与[符合性测试](../../tests/conformance/)：核对契约的具体落点。
- [快速试用](../../README.zh.md#try-it) · [MCP 接入](../../README.zh.md#mcp) · [架构概览](../architecture.zh.md)。

[系列目录](README.md) · 第 3 / 5 篇 · [上一篇](02-minimal-core.zh.md) · [下一篇](04-parallel-work.zh.md) · [五篇合集](collected.zh.md)

---

<a id="article-4"></a>

## 单机多 Agent 为什么不追求高并发：从共享写入到“多串行形成并行”

[系列目录](README.md) · 第 4 / 5 篇 · [上一篇](03-architecture-layers.zh.md) · [下一篇](05-mcp-a2a-runtime.zh.md) · [五篇合集](collected.zh.md)

原稿：2026-09-01 · 发布修订：2026-09-10 · 对齐 FCoP 4.0.0

> 本文解释架构取舍；字段、迁移与错误以 [4.0 契约](../../spec/fcop-4.0-spec.zh.md)为准，版本状态见 [4.0.0 发布说明](https://github.com/joinwell52-AI/FCoP/releases/tag/v4.0.0)。原始设计建议已按当前版本修订；示意流程不等于可直接执行的 API 示例。

多 Agent 系统一谈“并行”，很容易马上联想到：

```text
高并发
并发写
锁
事务
队列
分布式调度
```

但如果目标是一台工作机上的几个或十几个 Agent，这往往是把问题带错了方向。

FCoP 面向的不是一个每秒处理几十万事件的数据中心。

它面对的是：

```text
一个正式任务
多个不同职责 Agent
多个并行工作单元
最终形成一个可追踪结果
```

这两类系统需要的并行模型并不一样。

FCoP 更适合的原则是：

> **多串行形成并行。**

---

### 一、Windows 能并发，不等于 FCoP 应该追求共享写高并发

Windows 和 Linux 都能运行大量进程和线程。

文件系统也支持大量 I/O。

所以“单机”当然不等于“不支持并发”。

真正的问题是：

> **FCoP 是否应该把大量 Agent 同时修改同一个正式工作状态，当作主要工作模型？**

答案应该是否定的。

假设：

```text
TASK-001
```

同时被多个 Agent 改写：

```text
DEV-01 ─┐
DEV-02 ─┼→ TASK-001 / canonical result
QA     ─┤
OPS    ─┘
```

马上会出现：

```text
谁的写入最后生效？
另一个 Agent 基于哪个版本工作？
REVIEW 对应哪个结果？
ISSUE 是针对旧结果还是新结果？
系统崩溃时应该恢复哪一个版本？
```

这不是简单增加一个 lock 就能彻底解决的问题。

因为它同时牵涉：

> 工作身份、责任、版本、审查和收敛。

---

### 二、真正危险的是 shared mutable authority

多 Agent 协作最危险的不是：

> 同时运行。

而是：

> **同时修改同一个权威事实。**

这可以概括成：

```text
Parallel Execution
可以分开组织，但仍需资源与权限边界

Shared Mutable Authority
需要额外处理争用、证据与提交一致性
```

如果多个 Agent 同时执行不同工作：

```text
TASK-A → Agent A
TASK-B → Agent B
TASK-C → Agent C
```

可以分别组织；是否存在代码文件、外部资源或权限冲突，仍需 Runtime 和团队处理。

每个工作对象有自己的工作归属、状态和交付。TASK 分开不自动隔离代码工作区，必要时还应使用独立 checkout、worktree 或其他资源隔离。

真正应该避免的是：

```text
Agent A
Agent B
Agent C
    ↓
共同争抢一个 NOW
```

因此 FCoP 的并发原则应该围绕：

> **独立工作串。**

---

### 三、多个串行工作串可以天然形成并行

例如一个 Root TASK：

```text
发布 Windows 安装版
```

可能拆成：

```text
Root TASK
├─ 安装器构建
├─ 安装说明
├─ 升级验证
└─ 安全检查
```

每一个 Branch 都是独立正式 TASK：

```text
Branch A
TASK → work → REPORT

Branch B
TASK → work → REPORT

Branch C
TASK → work → REPORT
```

每条 Branch 内部保持清楚的单一工作序列。

但多条 Branch 可以同时推进。

于是得到：

```text
多个串行流
       ↓
整体并行
```

这就是：

> **多串行形成并行。**

---

### 四、为什么 Branch 比“共享文件一起改”更适合 Agent？

因为 Branch 把几个关键问题一起解决了。

#### 1. 工作归属明确

```text
Branch A → Agent A
Branch B → Agent B
```

系统很容易回答：

> 谁负责什么？

#### 2. 状态独立

一个 Branch 卡住，不会直接覆盖另一个 Branch 的正式状态。

#### 3. 交付独立

每个 Branch 可以产生自己的 REPORT。

#### 4. 问题独立

ISSUE 可以明确挂在某一条工作线上。

#### 5. 恢复独立

某个 Agent 会话丢失时，Runtime 可以依据该 Branch 的外部工作事实安排恢复；FCoP 不会自动重新启动该 Agent。

这种模式比多个 Agent 同时编辑一个“超级任务文档”清楚得多。

---

### 五、Branch 应该是普通 TASK，而不是第二套任务系统

Branch 如果成为一种全新的对象，会快速增加协议复杂度。

更好的设计是：

```text
Branch
=
普通 TASK
+
branch_of
```

例如：

```yaml
branch_of: "<Root 的稳定 task_id>"
```

这是关系字段示意，省略了合法 TASK 的其他必需字段。实际创建通过 `create_task(..., branch_of=root_task_id)`，Branch 同样需要工作区身份与创建幂等参数。

这样 Branch 仍然：

```text
进入正常生命周期
拥有自己的 Actor
拥有自己的 REPORT
可以产生 ISSUE
可以接受 REVIEW
```

协议只新增关系语义，而不是复制一套生命周期。

这正是 Core 应该追求的扩展方式：

> **新增最小关系，不新增第二世界。**

---

### 六、为什么不建议 Branch 再无限 Branch？

如果允许：

```text
Root
└─ A
   └─ A1
      └─ A1-1
         └─ ...
```

单机多 Agent 工作很快会变成一棵难以理解的动态树。

问题不只是数量。

更严重的是：

```text
责任向下扩散
审查关系复杂
最终收敛困难
根任务越来越难解释
```

因此 FCoP 4.0 明确采用扁平 sibling-only Branch：

```text
Root
├─ A
├─ B
├─ C
└─ D
```

Branch 不能再成为 Branch Root，否则拒绝为 `BRANCH_DEPTH_EXCEEDED`。需要进一步拆解时，可以在允许创建的 Root 下形成新的同级 Branch；已归档的 Root 不接受新 Branch。新增 Branch 后也必须重新评估原有汇合证据。

这不是“理论上绝对不能嵌套”，而是：

> **单机正式工作优先控制可理解性，而不是追求无限表达能力。**

---

### 七、并行之后必须收敛

Branch 的存在不能让系统长期保持多个“最终答案”。

临时分歧是允许的：

```text
Branch A → Result A
Branch B → Result B
Branch C → Result C
```

但正式 Root 工作最终必须能够回答：

> 当前权威结果是什么？

所以：

> **允许执行期间存在多个交付；带 Branch 的 Root 在正式归档前必须完成可核验的汇合。**

这是 Branch 模型真正重要的另一半。

没有显式收敛，Branch 只是任务拆分。

有了收敛，才形成一个完整的多 Agent 工作模式。

---

### 八、收敛语义与 Merge 工具不是一回事

这一点非常重要。

Core 可以规定：

> 多个 Branch 最终可以形成一个正式收敛结果。

但 Core 不要求复制某个 Git Merge Toolkit 的算法。以下阶段只是工具设计示意，并非 4.0 Base 生命周期：

```text
PREPARE
BUILD
VERIFY
COMMIT
```

也不必规定每一个实现必须有相同的：

```text
checkpoint
candidate
AlreadyCommitted
```

这些更像可靠 Merge Toolkit。

Core 需要稳定的是：

```text
哪些 Branch 被纳入
基于哪些工作产物
谁作出了收敛决定
当前工作结果与证据如何关联
原有来源关系不能被抹掉
```

4.0 将它落实为明确条件：Root 位于 done；所有 Branch 位于 done 或 archive，且各自经过 T3/T4；每个 Branch 当前 attempt 有唯一有效 REPORT；convergence REVIEW 精确覆盖这些报告；`family_digest` 匹配提交时重算值；另有绑定当前摘要的 Root 归档授权。

汇合记录不能替代归档授权。分支重开、新尝试或当前报告改变，会使旧汇合失效。这里汇合的是工作证据，并不自动生成或合并代码。

![多条 Branch 与当前证据汇合](../../assets/fcop-parallel-work.zh.svg)

相关边界见 [4.0 规范 §6、§7、§9](../../spec/fcop-4.0-spec.zh.md)。

---

### 九、并发复杂度可以计算，但不应该写死成 Core 公式

随着 Branch 增多，可以计算：

```text
active branch count
scope overlap
unresolved issues
merge surface
```

这些数据很有用。

但一个具体公式：

```text
score = aB + bO + cU ...
```

本质上属于：

> Policy / Toolkit。

因为真实使用以后，权重和阈值可能变化。

协议不应该因为某次实验调了一个阈值就升级 Core。

Core 只需要确保：

> 必要事实可以被外化和计算。

至于如何评分，是上层策略。

---

### 十、同一治理对象应该倾向单写者

FCoP 不需要承诺全局只有一个 Writer。

相反，它允许多个工作串同时存在。

但对于同一个正式治理对象，更合理的原则是：

> **同一正式对象的一次协议提交应具有明确、可校验的边界。**

“一个任务当前由谁执行”是组织和调度约定，不等于 Core 内置单一 owner 权限表。4.0 使用合法迁移、可信授权与提交协调保证正式状态，不能仅凭执行者标签判断写入合法。

例如：

```text
Branch A
→ Agent A 是当前正式执行者
```

其他 Agent 可以：

```text
观察
提出 ISSUE
提交 REVIEW
创建关联工作
```

但不应该无约束地同时改写 Branch A 的当前权威状态。

这使并行建立在：

```text
多个独立单写者工作串
```

之上，而不是：

```text
一个高争用共享对象
```

同一 Root family 中，涉及 Root/Branch 状态、当前 REPORT、汇合和归档条件的操作共享短暂线性化边界。取得边界后必须重读当前事实再提交；它不锁住 Agent 的整段执行时间，也不串行化无关的独立 TASK（[规范 F4.9.5](../../spec/fcop-4.0-spec.zh.md)）。

---

### 十一、这是一种更像真实组织的并行

真实团队也不是：

> 所有人同时在一张任务单上改最终结论。

更常见的是：

```text
工程负责工程
测试负责测试
运维负责部署
管理者负责协调
```

每个人形成自己的工作产物。

最后通过正式交付和审查形成收敛。

数字员工没有必要为了显得“并行”而采用一种比真实组织更难治理的共享写模式。

FCoP 的 Branch 反而更接近：

> **职责分离后的并行工作。**

---

### 十二、FCoP 为什么不需要追求极高 TPS？

数字员工的工作频率和数据系统不同。

一个 Agent 可能连续工作几十分钟，最后才产生一次 REPORT。

一个 REVIEW 可能需要重新执行测试。

一个 ISSUE 可能挂数小时才解决。

所以真正重要的指标不是：

```text
每秒创建多少 TASK
```

而是：

```text
有没有重复 TASK？
有没有丢 REPORT？
谁负责？
冲突有没有显式留下？
失败后能不能恢复？
最终结果来自哪些 Branch？
```

工作系统关注的是：

> **责任和状态质量。**

而不是单纯事务数量。

---

### 十三、如果真的需要高并发怎么办？

这也是边界问题。

如果未来场景变成：

```text
10000 agents
100000 events/sec
跨数据中心
大量共享状态
```

就需要重新评估存储、吞吐、通信与故障模型。下面的数字是负载假设，不是本项目已完成的基准；可考虑：

```text
数据库
消息队列
分布式协调
专用 Runtime
```

FCoP 的工作语义可以作为新架构的设计输入；但当前 4.0 Base 不能直接宣称支持这类跨数据中心负载，其他编码或一致性层仍需独立实现和验证。

但它没有必要亲自实现整个高并发数据平面。

这和操作系统、数据库、网络协议之间的分工一样：

> 每一层只解决自己最擅长的问题。

---

### 结语：并行不是同时修改同一个世界

多 Agent 系统真正需要避免的，是把：

> “并行”

误解为：

> “所有 Agent 同时修改同一个共享权威状态。”

对于单机数字员工，更稳健的方式是：

```text
独立工作对象
+
明确责任
+
各自串行推进
+
整体并行
+
显式收敛
```

也就是：

> **多串行形成并行。**

FCoP 的 Branch 价值不在于模仿 Git。

它更深层的意义是：

> **用多个外化、可归属、可恢复的独立工作串，替代不可治理的共享可变状态。**

这样，单机多 Agent 不需要先变成一个高并发分布式系统，也可以获得真正有用的并行能力。

---

### 实现与延伸阅读

- [4.0 规范](../../spec/fcop-4.0-spec.zh.md)：核对 C1–C8、授权、幂等与恢复条款。
- [Python v4 实现](../../src/fcop/v4/)与[符合性测试](../../tests/conformance/)：核对契约的具体落点。
- [快速试用](../../README.zh.md#try-it) · [MCP 接入](../../README.zh.md#mcp) · [架构概览](../architecture.zh.md)。

[系列目录](README.md) · 第 4 / 5 篇 · [上一篇](03-architecture-layers.zh.md) · [下一篇](05-mcp-a2a-runtime.zh.md) · [五篇合集](collected.zh.md)

---

<a id="article-5"></a>

## 从单机到联网：FCoP、MCP、A2A 与 CodeFlowMu 各自负责什么

[系列目录](README.md) · 第 5 / 5 篇 · [上一篇](04-parallel-work.zh.md) · [五篇合集](collected.zh.md)

原稿：2026-09-01 · 发布修订：2026-09-10 · 对齐 FCoP 4.0.0

> 本文解释架构取舍；字段、迁移与错误以 [4.0 契约](../../spec/fcop-4.0-spec.zh.md)为准，版本状态见 [4.0.0 发布说明](https://github.com/joinwell52-AI/FCoP/releases/tag/v4.0.0)。原始设计建议已按当前版本修订；示意流程不等于可直接执行的 API 示例。

Agent 技术快速发展以后，一个新的问题开始出现：

> 工具访问、Agent 协作、运行时、跨系统联网、工作治理，究竟应该由谁负责？

如果所有问题都交给一个框架，最后很容易得到：

```text
一个巨型 Agent 平台
```

它同时处理：

```text
工具
任务
网络
模型
身份
调度
审查
恢复
存储
治理
```

系统能力看起来很完整，但边界越来越模糊。

更健康的方式，是让不同基础设施承担不同职责。

对于本地优先的数字员工架构，可以先区分四个非常关键的层：

```text
MCP
FCoP
CodeFlowMu
A2A
```

它们解决的其实是四个不同问题。

---

### 一、MCP：Agent 怎样使用工具？

一个 Agent 要真正做事，必须能访问：

```text
文件
数据库
GitHub
浏览器
Shell
企业系统
外部 API
```

MCP 解决的是：

> **模型或 Agent 如何以标准方式访问 Tools、Resources 和其他上下文能力。**

最简单地说：

```text
Agent
   ↕
  MCP
   ↕
Tools / Resources
```

它关注的是：

```text
有哪些工具？
怎么描述？
参数是什么？
如何调用？
返回什么？
```

所以 MCP 的核心边界是：

> **Agent ↔ Tool。**

这只是本文关注的主要用途。MCP 也支持 Resources、Prompts、远程传输及长任务相关扩展；不能把“工具访问”理解为它完全没有网络或任务能力。它没有据此规定 FCoP 的组织验收语义。参见 [MCP 官方架构说明](https://modelcontextprotocol.io/docs/learn/architecture)。

---

### 二、FCoP：Agent 的正式工作行为怎样留下来？

FCoP 面对的是另一类问题。

Agent 调用了工具以后：

```text
谁接了任务？
谁提交了结果？
发现了什么问题？
谁做了审查？
任务现在处于什么状态？
```

这些不是 Tool Call 本身能表达的。

因此 FCoP 的边界是：

> **把单机 Agent 的正式工作行为外化成持续存在的工作对象。**

例如：

```text
TASK
REPORT
ISSUE
REVIEW
Lifecycle
Reference
History
```

最简单地说：

```text
Agent Behavior
      ↓
     FCoP
      ↓
Durable Work Facts
```

因此：

> **MCP 解决“Agent 怎么做”。**

> **FCoP 解决“Agent 做过什么正式工作”。**

二者关注点不同，可以组合使用。FCoP 4.0 已提供可选的 stdio `fcop-mcp` 适配器；Python 使用者也能直接调用同一实现，无需经过 MCP。

---

### 三、CodeFlowMu：Agent 怎样持续工作？

即使 Agent 的行为已经通过 FCoP 外化，系统仍然需要真正运行。

例如：

```text
哪个 Agent 被启动？
使用哪个 Host？
调用哪个模型？
Session 是否还活着？
Lease 是否过期？
失败以后怎么恢复？
Timer 什么时候触发？
响应丢失以后怎么重试？
```

这些属于 Runtime。

CodeFlowMu 的位置因此不是：

> FCoP 的另一个名字。

而是：

> **把 Agent、Host、模型、工具和外部工作事实组织成持续运行数字员工的 Runtime。**

可以理解成：

```text
       FCoP
  工作行为外化
       ↑
       │
CodeFlowMu Runtime
       │
       ↓
Model / Host / Tool
```

FCoP 可以独立存在。

CodeFlowMu 可以选择使用 FCoP 作为工作事实层。

这两者的职责不应该重新混同。这里描述 CodeFlowMu 的产品定位与 Runtime 需要承担的问题，具体版本能力请查看 [CodeflowMu-Distribution 发布说明](https://github.com/joinwell52-AI/CodeflowMu-Distribution/releases)，不能把职责列表当成当前产品已实现的逐项保证。

---

### 四、Windows 与 Linux 可以属于同一个数字员工运行边界

以下是部署设计示例，不代表 FCoP 4.0 已提供多机共享工作区或特定版本的 CodeFlowMu 已提供这一拓扑。一个产品的 Runtime 可以跨越多个物理节点。

例如一个数字员工可以由：

```text
Windows 工作电脑
+
Linux Server
```

共同组成。

Windows 可能承载：

```text
桌面环境
IDE
浏览器
本地应用
用户交互
Host
```

Linux Server 可能承载：

```text
Runtime service
持久调度
后台任务
API
长期服务
```

实现这样的 Runtime 时，可以由产品提供内部 API、RPC 或其他通信机制；具体方案需要定义认证、权限、失败恢复与持久边界。4.0 Base 的本地文件系统假设不能直接推广到网络共享盘。

关键点在于：

> **它们仍然可以属于同一个数字员工责任边界。**

因此，Windows ↔ Linux 并不必然需要 A2A。

A2A 不应该被当作内部组件通信的万能替代品。

---

### 五、A2A：不同 Agent 系统怎样联网？

A2A 解决的是：

> **一个独立 Agent 系统怎样与另一个独立 Agent 系统互操作。**

例如：

```text
Digital Worker A
       ↕
      A2A
       ↕
Digital Worker B
```

它需要处理：

```text
Agent discovery
Agent Card
Message
Task
Artifact
网络认证
远程交互
长任务
流式状态
异步通知
```

因此：

> **A2A 的核心边界是 Agent System ↔ Agent System。**

它关注跨系统交互，但 Task、Artifact 也带有自己的生命周期和语义，不能把 A2A 简化为纯传输管道。参见 [A2A 官方规范](https://a2a-protocol.org/latest/specification/)。

---

### 六、A2A 越成熟，FCoP 越不需要自己做联网

这其实是一件好事。

如果已经有专门协议解决：

```text
远程发现
跨组织通信
网络认证
streaming
webhook
remote task
```

FCoP 就没有必要继续扩张去复制这些能力。

FCoP 可以专注：

```text
TASK
REPORT
ISSUE
REVIEW
Attribution
Lifecycle
Branch relation
```

这反而让自己的 Core 更稳定。

所以：

> **A2A 不是 FCoP 的威胁，而是帮助 FCoP 收缩边界。**

---

### 七、数字员工之间可以 A2A，员工内部仍可 FCoP

例如一家公司未来有：

```text
软件开发数字员工
财务数字员工
销售数字员工
法务数字员工
```

不同数字员工之间：

```text
开发数字员工
      ↕
     A2A
      ↕
财务数字员工
```

A2A 负责跨系统交付远程 Task 与 Artifact。

下面是本文提出的映射设想，FCoP 4.0 尚未交付 A2A 适配器。财务数字员工收到任务后，可由适配层转换：

```text
A2A Task
    ↓
Local FCoP TASK
    ↓
Worker
    ↓
REPORT
    ↓
REVIEW
```

于是形成：

```text
A2A
负责系统之间

FCoP
负责系统内部正式工作
```

这是非常自然的两级结构。

---

### 八、一个完整数字员工内部可以是什么样？

例如：

```text
一个数字员工
────────────────────

        PM
     /  |  \\
   DEV  QA  OPS
        |
       EVAL

内部正式工作：
        FCoP

工具访问：
        MCP

执行、Session、恢复：
        CodeFlowMu Runtime
```

从外部看，它可能只是：

> 一个“软件开发数字员工”。

内部可以是一个职责分离的 Agent 团队。这组 PM/DEV/QA/OPS/EVAL 角色只是 Profile 示例，不是 FCoP Core 的必需角色。

这就是：

> **外部一个责任主体，内部多个工作角色。**

---

### 九、跨数字员工以后发生什么？

假设开发数字员工需要财务确认一项采购。

流程可以是：

```text
开发数字员工
内部 FCoP 形成正式请求
        ↓
A2A
        ↓
财务数字员工
        ↓
本地 FCoP TASK
        ↓
财务内部执行
        ↓
REPORT / REVIEW
        ↓
A2A Artifact
        ↓
返回开发数字员工
```

这里每一层都做自己最擅长的事情。

A2A 不需要知道财务数字员工内部有几个 Agent。

FCoP 也不需要知道对方系统在什么云上。

---

### 十、FCoP 与 A2A 的 Task 不是必须二选一

A2A 本身有 Task。

FCoP 也有 TASK。

这并不必然意味着冲突。

因为二者所处边界不同。

可以建立映射：

```text
A2A Task
    ↓
local FCoP TASK
```

A2A Task 是：

> 跨系统任务交互对象。

FCoP TASK 是：

> 本地正式工作对象。

同理：

```text
A2A Artifact
    ↓
local REPORT / evidence reference
```

适配层还必须定义远程与本地身份、重试幂等、状态映射、产物来源和权限验证。远端 A2A Task 完成或 Artifact 到达，不能自动转换为本地 FCoP 验收通过；本地仍需要匹配当前 attempt、REPORT、REVIEW 和可信授权。

---

### 十一、MCP 也不需要和 A2A 竞争

MCP 和 A2A 经常被同时讨论，但边界也很清楚：

```text
MCP:
Agent ↔ Tool

A2A:
Agent System ↔ Agent System
```

一个远程数字员工可以通过 A2A 接任务。

它内部某个 Agent 再通过 MCP：

```text
调用 GitHub
查询数据库
运行测试
读取文件
```

两者可以同时存在。这是一种组合方式，不要求所有远程 Agent 都只能通过 A2A 暴露，也不要求所有工具都只能经 MCP 接入。

---

### 十二、为什么不能让 CodeFlowMu 把一切都做掉？

理论上当然可以。

一个产品可以自己实现：

```text
工具协议
内部工作协议
网络协议
模型 Runtime
审计
身份
跨组织互操作
```

但这样会产生两个问题。

第一，系统越来越重。

第二，外部生态越来越难接入。

如果 MCP 已经成为工具接入层，A2A 已经承担跨系统互操作，那么 CodeFlowMu 更有价值的工作是：

> **成为一个高质量数字员工 Runtime。**

而不是重新发明所有基础协议。

---

### 十三、整个架构可以画成什么？

可以先用一个简单版本：

```text
                External Agent Systems
                         │
                        A2A
                         │
────────────────────────────────────────
                 Digital Worker
                         │
                  CodeFlowMu Runtime
                         │
          ┌──────────────┴─────────────┐
          │                            │
         FCoP                         MCP
  Work Behavior Externalization   Tool Access
          │                            │
     Work Facts                  External Tools
```

如果研究场景还采用 TMPA，可以增加治理解释视角；它不是 FCoP 4.0 的安装前置条件：

```text
                  Governance / TMPA
                         ↑
                         │
                       FCoP
                         ↑
                  CodeFlowMu Runtime
                  ↙               ↘
                MCP               A2A
                 ↓                 ↓
               Tools        Other Agent Systems
```

不同层的职责就不会互相挤压。

---

### 十四、四句话就可以描述整个体系

最终可以把边界压缩成：

> **MCP：Agent 如何使用工具。**

> **FCoP：单机 Agent 的正式工作行为如何外化。**

> **CodeFlowMu：Agent 如何持续运行、调度和恢复。**

> **A2A：不同 Agent 系统如何联网协作。**

如果再加治理层：

> **TMPA：为责任、审查与治理判断提供架构解释。**

治理判断仍需实际证据与审查，不能由架构名称自动证明成立。相关研究可从 [joinwell52 研究仓库](https://github.com/joinwell52-AI/joinwell52)继续阅读。

这五句话比“所有东西都是 Agent Framework”清楚得多。

---

### 十五、边界清楚以后，FCoP 反而可以更轻

在采用 A2A 的组合设计里，以下跨系统能力可交给网络集成层处理；这不是当前 FCoP 的新增工具清单：

```text
remote discovery
OAuth
mTLS
streaming
webhook
network routing
```

CodeFlowMu 负责 Runtime 以后，FCoP 不需要拥有：

```text
scheduler
session manager
lease
model selection
host recovery
```

MCP 负责工具以后，FCoP 也不需要定义：

```text
browser tool
GitHub tool
database tool
```

FCoP 最终可以安心停留在：

```text
正式工作行为
+
正式工作关系
+
正式工作状态
```

这正是它最有价值的位置。

---

### 结语：不要让每一层都变成“完整平台”

Agent 基础设施正在快速成熟。

这个阶段很容易出现一种冲动：

> 每一个项目都想解决所有问题。

但成熟架构往往来自相反的选择：

> **知道哪些问题不归自己解决。**

MCP 不需要成为工作治理系统。

A2A 不需要成为单机任务审查系统。

FCoP 不需要成为网络协议。

CodeFlowMu 不需要重造所有工具与网络标准。

每一层保持自己的边界，才能形成一个真正可组合的 Agent 技术栈。

最终：

```text
工具有工具的标准
工作有工作的事实
运行有运行的 Runtime
联网有联网的协议
治理有治理的判断
```

数字员工真正需要的，不是一个无所不包的超级框架。

而是一组边界清楚、可以长期组合的基础层。

---

### 实现与延伸阅读

- [4.0 规范](../../spec/fcop-4.0-spec.zh.md)：核对 C1–C8、授权、幂等与恢复条款。
- [Python v4 实现](../../src/fcop/v4/)与[符合性测试](../../tests/conformance/)：核对契约的具体落点。
- [快速试用](../../README.zh.md#try-it) · [MCP 接入](../../README.zh.md#mcp) · [架构概览](../architecture.zh.md)。

[系列目录](README.md) · 第 5 / 5 篇 · [上一篇](04-parallel-work.zh.md) · [五篇合集](collected.zh.md)
