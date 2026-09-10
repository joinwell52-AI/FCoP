---
title: "从单机到联网：FCoP、MCP、A2A 与 CodeFlowMu 各自负责什么"
date: "2026-09-01"
series: "FCoP 架构原理系列：让 Agent 的工作站到模型之外"
series_no: 5
article_type: engineering-architecture
status: published
publication_authorized: true
published_at: "2026-09-10"
updated_at: "2026-09-10"
protocol_version: "4.0"
publication_revision: "1"
summary: "MCP 提供工具与上下文访问，FCoP 保存正式工作事实，Runtime 组织执行，A2A 提供跨 Agent 系统交互。本文讨论四者的组合设计，区分 FCoP 4.0 已交付能力与尚需实现的网络映射。"
---

# 从单机到联网：FCoP、MCP、A2A 与 CodeFlowMu 各自负责什么

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

## 一、MCP：Agent 怎样使用工具？

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

## 二、FCoP：Agent 的正式工作行为怎样留下来？

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

## 三、CodeFlowMu：Agent 怎样持续工作？

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

## 四、Windows 与 Linux 可以属于同一个数字员工运行边界

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

## 五、A2A：不同 Agent 系统怎样联网？

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

## 六、A2A 越成熟，FCoP 越不需要自己做联网

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

## 七、数字员工之间可以 A2A，员工内部仍可 FCoP

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

## 八、一个完整数字员工内部可以是什么样？

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

## 九、跨数字员工以后发生什么？

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

## 十、FCoP 与 A2A 的 Task 不是必须二选一

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

## 十一、MCP 也不需要和 A2A 竞争

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

## 十二、为什么不能让 CodeFlowMu 把一切都做掉？

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

## 十三、整个架构可以画成什么？

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

## 十四、四句话就可以描述整个体系

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

## 十五、边界清楚以后，FCoP 反而可以更轻

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

## 结语：不要让每一层都变成“完整平台”

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

## 实现与延伸阅读

- [4.0 规范](../../spec/fcop-4.0-spec.zh.md)：核对 C1–C8、授权、幂等与恢复条款。
- [Python v4 实现](../../src/fcop/v4/)与[符合性测试](../../tests/conformance/)：核对契约的具体落点。
- [快速试用](../../README.zh.md#try-it) · [MCP 接入](../../README.zh.md#mcp) · [架构概览](../architecture.zh.md)。

[系列目录](README.md) · 第 5 / 5 篇 · [上一篇](04-parallel-work.zh.md) · [五篇合集](collected.zh.md)
