---
title: "FCoP 不等于它的工具：Core、Specification、Toolkit、Profile 与 Runtime 如何分层"
date: "2026-09-01"
series: "FCoP 架构原理系列：让 Agent 的工作站到模型之外"
series_no: 3
article_type: engineering-architecture
status: published
publication_authorized: true
published_at: "2026-09-10"
updated_at: "2026-09-10"
protocol_version: "4.0"
publication_revision: "1"
summary: "一个基础系统可以拥有大量 SDK、命令和工具，但这些并不等于它的内核。本文解释 FCoP 4.0 如何区分 Core、规范、符合性验证、工具、组织策略与 Runtime，使功能增长保持清楚的边界。"
---

# FCoP 不等于它的工具：Core、Specification、Toolkit、Profile 与 Runtime 如何分层

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

## 一、Windows 给出的启示：平台不等于工具总和

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

## 二、第一层：FCoP Core

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

## 三、第二层：FCoP Specification

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

## 四、第三层：Conformance

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

## 五、第四层：FCoP Toolkit

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

## 六、第五层：Profile

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

## 七、第六层：Runtime

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

## 八、完整结构

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

## 九、用这个分层重新看 Branch

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

## 十、复杂度评分属于 Toolkit 或 Policy

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

## 十一、角色属于 Profile

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

## 十二、Merge 要区分“语义”和“参考实现”

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

## 十三、工具多不是问题，混层才是问题

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

## 十四、4.0 已经如何落实这条路线？

原始草稿提出先形成 Core 边界、再进行实现。现在可以直接核对 4.0 的成果：

1. [规范](../../spec/fcop-4.0-spec.zh.md)明确 C1–C8 及各层职责。
2. [v4 实现](../../src/fcop/v4/)将创建、生命周期、授权、汇合和恢复分开组织。
3. [符合性测试](../../tests/conformance/)提供可核对的行为证据。
4. [规则分发契约](../fcop-4.0/rule-distribution-contract.zh.md)区分采纳、部署和宿主投影。

原文建议的 `FCOP-CORE-BOUNDARY.md` 是当时拟议的文件名；当前实现者应以上述实际文档为入口。

---

## 十五、后续演进继续遵守契约优先

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

## 结语：强大的系统，核心通常很小

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

## 实现与延伸阅读

- [4.0 规范](../../spec/fcop-4.0-spec.zh.md)：核对 C1–C8、授权、幂等与恢复条款。
- [Python v4 实现](../../src/fcop/v4/)与[符合性测试](../../tests/conformance/)：核对契约的具体落点。
- [快速试用](../../README.zh.md#try-it) · [MCP 接入](../../README.zh.md#mcp) · [架构概览](../architecture.zh.md)。

[系列目录](README.md) · 第 3 / 5 篇 · [上一篇](02-minimal-core.zh.md) · [下一篇](04-parallel-work.zh.md) · [五篇合集](collected.zh.md)
