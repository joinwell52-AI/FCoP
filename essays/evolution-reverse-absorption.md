---
title: 演化,反向吸收
title_en: Evolution, Reverse Absorption
status: essay
date: 2026-05-13
audience: 关心 FCoP 怎么自己进化、为什么协议哲学需要两张图共同定义的读者
length: ~ 10 分钟
cover_image: assets/evolution-reverse-absorption-cover.png
companion_doc: adr/ADR-0034-fcop-internal-external-document-convention.md
companion_essay: essays/looking-without-touching.md
---

![演化,反向吸收 · 题图](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/assets/evolution-reverse-absorption-cover.png)

> **一句话**:FCoP 协议有两件事——**执行**和**演化**。第一篇文章(`looking-without-touching.md`)
> 讲它怎么执行(看,但不动手),配的是第一张图(`FCoP-semantic-execution-chain-v1.0.png`);
> **这一篇讲它怎么演化——通过反向吸收**,配的是 2026-05-13 09:17 落下的第二张图
> (`FCOP-2.0.png`)。从此 FCoP **由两张图、两篇文章共同定义**:
> 一张管"今天怎么不越界地干",一张管"明天怎么变成更好的自己"。

---

## 先看两张图 / The Two Diagrams at a Glance

> 协议哲学是双图哲学。下面两张 ASCII 图就是 FCoP 的全部哲学声明——
> 第一张说"我现在长这样",第二张说"我怎么自己变成下一个我"。
> **先看图,再读字**——后面所有章节都是这两张图的展开和论证。

### 第一张图 · 执行哲学 v1.0(FCoP Protocol Layer Stack)

```text
┌─────────────────────────────────────────────────────┐
│           应用层 / Application Layer                │
│           CodeFlow / Cursor / Claude Desktop        │
├─────────────────────────────────────────────────────┤
│           宿主适配层 / Host Adapter Layer            │
│           fcop-mcp / fcop-cli / @fcop/claude         │
├─────────────────────────────────────────────────────┤
│       ★ FCoP 协议层 ★    ← 本协议所在层             │
│           Agent 协作 / 行为报告 / Review /           │
│           Capability Governance / 事件语义 / 审计边界 │
├─────────────────────────────────────────────────────┤
│           参考实现层 / Reference Implementation      │
│           fcop(Python Library)                       │
├─────────────────────────────────────────────────────┤
│           执行基底 / Execution Substrate             │
│           LLM APIs / MCP Tools / 文件系统 / OS       │
│           (FCoP 治理行为,不拥有执行层)               │
└─────────────────────────────────────────────────────┘
```

**5 层栈**,从应用层到执行基底——这是**结构图**,告诉你 FCoP **是什么**。
2026-05-12 12:28,这张图以 `FCoP-semantic-execution-chain-v1.0.png` 落盘。

### 第二张图 · 演化哲学 2.0(FCoP Semantic Evolution Loop)

```text
┌───────────────────────────────────────────────────────────────┐
│                  FCoP Semantic Evolution Loop                 │
│                  (FCoP 语义演化闭环)                          │
└───────────────────────────────────────────────────────────────┘


         ┌─────────────────────────────────────┐
         │         Human Intention             │
         │         人类目标 / 业务意图           │
         └────────────────┬────────────────────┘
                          │
                          ▼
         ┌─────────────────────────────────────┐
         │         FCoP Protocol Layer         │
         │-------------------------------------│
         │ • Rules / ADR / Vocabulary          │
         │ • Constraint / Auditability         │
         │ • Capability Governance             │
         │ • Coordination Semantics            │
         └────────────────┬────────────────────┘
                          │
                          ▼
         ┌─────────────────────────────────────┐
         │     Coordination Adapter Layer      │
         │-------------------------------------│
         │ Cursor / MCP / CLI / CodeFlow       │
         │ Claude Desktop / Agent Runtime      │
         │ Context Projection & Routing        │
         └────────────────┬────────────────────┘
                          │
                          ▼
         ┌─────────────────────────────────────┐
         │      Runtime / Filesystem Reality   │
         │-------------------------------------│
         │ • TASK / REPORT / REVIEW            │
         │ • Agent Collaboration               │
         │ • Shared Knowledge Surface          │
         │ • Workspace / Runtime Behaviors     │
         └────────────────┬────────────────────┘
                          │
                          ▼
         ┌─────────────────────────────────────┐
         │     Emergence / Local Conventions   │
         │-------------------------------------│
         │ • Internal Archives                 │
         │ • Emergence Logs                    │
         │ • Team Dialects                     │
         │ • New Coordination Patterns         │
         │ • Drift / Self-Correction           │
         └────────────────┬────────────────────┘
                          │
                          ▼
         ┌─────────────────────────────────────┐
         │      ADR / Reverse Absorption       │
         │-------------------------------------│
         │ • Observation                       │
         │ • Consolidation                     │
         │ • Protocol Evolution                │
         │ • Semantic Upgrades                 │
         └────────────────┬────────────────────┘
                          │
                          ▼
         ┌─────────────────────────────────────┐
         │       Updated FCoP Protocol         │
         │-------------------------------------│
         │ • New Rules                         │
         │ • New Vocabulary                    │
         │ • Emergent Patterns Absorbed        │
         │ • Next-Generation Constraints       │
         └────────────────┬────────────────────┘
                          │
                          └──────────────┐
                                         │
                                         ▼
                          (Loop Continues / 协议持续演化)


Core Principle / 核心原则
───────────────────────────────────────────────────────────────

Human defines the minimum structure.
Agents create emergent intelligence.
FCoP absorbs successful emergence back into protocol evolution.

人类定义最低结构,
Agent 自由产生智能涌现,
FCoP 将有效涌现反向吸收为协议演化能力。

                                          —— ADMIN, 2026-05-13 09:14
```

**7 步闭环**,从人类意图回到协议本身——这是**过程图**,告诉你 FCoP **怎么活、怎么长大**。
2026-05-13 09:17,这张图以 `FCOP-2.0.png` 落盘。

---

读完上面这两张图,你已经看到了 FCoP 哲学的**全貌**。
后面的章节是它们的展开:为什么是 2.0、Core Principle 怎么落地、
双图之后会发生什么、协议从此有了自己的进化论。

---

## 一对孪生姿势 / A Twin of Postures

协议要存活,需要两种姿势,缺一不可:

| 第一张图(执行哲学)             | 第二张图(演化哲学)                    |
| ---------------------- | ----------------------------- |
| **看,但不动手**             | **演化,反向吸收**                   |
| Looking, not Touching  | Evolution, Reverse Absorption |
| `fcop_audit()` 只观察、不修改 | 涌现来了,有选择地纳进协议                 |
| 执行的克制:不越界改人            | 演化的克制:只纳普适涌现、留特定在原处           |

**第一句**讲协议**怎么对外**——看你的项目,但不替你做决定。
**第二句**讲协议**怎么对内**——自己演化,但只纳普适涌现、不全收。

少一句,协议就要么变成施加者(只有"动手"没有"看"),
要么变成飘移者(只有"演化"没有"反向吸收",新规则一来旧规则就被冲掉)。

---

## 那一天发生了什么 —— 第二张图的落盘 / What Happened That Day — When the Second Diagram Landed

| 时间                   | 事件                                                                                       |
| -------------------- | ---------------------------------------------------------------------------------------- |
| **2026-05-12 12:28** | `adr/FCoP-semantic-execution-chain-v1.0.png` 落盘 —— FCoP **执行哲学**的第一张视觉化(5 层栈)            |
| **2026-05-13 09:14** | ADMIN 在聊天里给出一段 ASCII 等价物:"**FCoP Semantic Evolution Loop**"——7 步闭环 + Core Principle 三句中英 |
| **2026-05-13 09:17** | `adr/FCOP-2.0.png` 落盘 —— **演化哲学**的视觉化,1.71 MB,与 v1.0 同层                                  |
| **2026-05-13 09:38** | ADMIN 派单:"FCOP-2.0.png 这个是全新的,也需要写一篇文章,作为重要的记录!!"                                        |

物理事实就这么简单:**第二张图,落进了和第一张图同样的目录、用了几乎同样的大小、跟在第一张图的后面 21 小时**。

但语义事实远不止于此——文件名里那个 `2.0` 不是 SemVer 版本号 bump,
是**哲学层级 bump**。

---

## 为什么是 2.0,不是 v1.1 / Why 2.0, Not v1.1

如果只是给协议加一个新概念、新工具、新 ADR,那叫 v1.1——MINOR additive,既有规则继续生效,
新文件叠加上去就完了。FCoP 已经这样涨过很多次了:0.5、0.6、0.7、1.0、1.1……每一次都是
"协议本体没变,能力多了几样"。

**但这次不一样**。这次发生的事是——**协议哲学的对偶结构成立了**。

| 维度                         | v1.0 时代(2026-05-12 之前)        | 2.0 时代(2026-05-13 起)            |
| -------------------------- | ----------------------------- | ------------------------------- |
| 协议有几张哲学图                   | **1 张**(执行哲学)                 | **2 张**(执行 + 演化)                |
| 协议回答的核心问题                  | "FCoP 是怎么执行的?"                | "FCoP 是怎么执行的 + 怎么进化的?"          |
| 反向吸收(Reverse Absorption)地位 | 隐式 —— 事后追认(ADR-0017、ADR-0033) | 显式 —— 协议核心机制(ADR-0034 §2.5)     |
| 协议 vs Agent 的关系            | 单向:人类定规则,Agent 执行             | 闭环:人类定最低结构,Agent 涌现智能,FCoP 反向吸收 |
| 第二张图缺位的代价                  | 协议**会自我演化**,但没人画出来,看不到        | 协议**演化机制可视、可检查、可被新 ADR 修正**     |

第一张图回答**今天的 FCoP 在做什么**——5 层栈,从应用层到执行基底,
是一个**结构图**,告诉你这个协议长什么样。

第二张图回答**FCoP 自己怎么变成明天的 FCoP**——7 步闭环,从人类意图到协议演化,
是一个**过程图**,告诉你这个协议怎么活。

**少一张,协议就丧失自我演化能力**,回到"人类定规则,AI 被动执行"的传统范式——
那是 LangGraph、Temporal、CrewAI 们待的地方,不是 FCoP 想去的地方。

所以这次协议哲学**从单图变成双图**,这件事配得上 `2.0`。

---

## ADMIN 给的 Core Principle / The Core Principle Admin Gave

回到第二张图——它的语义内核就在图末尾的三句字幕里(ADMIN 在 PNG 落盘前 3 分钟用 ASCII 写下):

> Human defines the minimum structure.
> Agents create emergent intelligence.
> FCoP absorbs successful emergence back into protocol evolution.
> 
> 人类定义最低结构,
> Agent 自由产生智能涌现,
> FCoP 将有效涌现反向吸收为协议演化能力。
> 
> —— ADMIN, 2026-05-13 09:14

这三句话**就是第二张图的字幕**。它们也是 ADR-0034 §2.5.6 里被原样收录的那段
"协议级可视化资产"的核心断言。

第一句"**人类定义最低结构**"——FCoP 不是把规则写满写死,而是把规则写到刚好够 agent 协作。
凡是协议没说的地方(directory 怎么分、role 怎么命名、私房 essay 怎么放),都留给 agent 自己。

第二句"**Agent 自由产生智能涌现**"——空白不是 bug,是 feature。Bridgeflow 的 PM 在
`fcop/internal/emergence-log.md` 里搞出了"内部档案 — 不外发,不进 fcop issue" 这种声明,
codeflow 的某个会话长出了 `supersedes:` 字段,QA 在 GATE 描述上摔了一次后涌现出
"语义化 GATE"——这些都是协议没规定但 agent 在现场长出来的。

第三句"**FCoP 将有效涌现反向吸收为协议演化能力**"——重点是"有效"两个字。涌现来了,
不是全收。ADR-0034 §2.5.4 立了一张矩阵:**普适 / 团队特定 / 项目特定 / 一次性**,
只有第一行才进协议。其余的进团队模板、进项目本地 RULES、进 essays 案例库。
**反向吸收不是全收**,这是双图哲学不会失控的力学保证。

**反向吸收 = 有所选择的演化**——

- **演化** = 协议确实在长,新规则、新字段、新 ADR、新图都会增加;但**只纳普适**——
  团队特定 / 项目特定 / 一次性留在它们该在的层(团队模板、项目本地 RULES、
  essays 案例库)。
- **反向吸收**("反向"两字) = 这次选择的方向——从下游的 agent 现场回流到上游的
  协议层,但只回流**经得住普适检验的那一份**。协议的骨架(既有 Rule 0–9 +
  七大核心概念)不会因为某个 agent 在某个项目临时长出来一个新模式而被替换或抛弃。

这是**反向吸收**和"无脑学习"的根本区别。**无脑学习把所有 input 都当 truth 喂给自己**——
那是 LLM 训练的姿势,不是协议演化的姿势。**反向吸收只纳普适、留特定**——
这才是 FCoP 长得稳的原因,也是 essay 标题中"演化,反向吸收"两个词必须并列出现的原因:
**演化是表象,反向吸收是机制**;只讲演化不讲反向吸收,协议就只剩膨胀、没有方向;
只讲反向吸收不讲演化,协议就被锁死在今天的快照里。

---

## 双图之后会发生什么 / What Comes After the Second Diagram

ADR-0034 §2.5 已经把"反向吸收"作为一种**协议级机制**定义下来,§2.5.6 把演化哲学图
作为**协议级可视化资产**确立下来。这意味着:

### 1. 未来所有 ADR 都要回答两个问题,不是一个

写一份新 ADR,以前只要回答:"它在协议栈里属于哪一层?"

**从 2.0 起**,还要回答:"它在 7 步闭环里处于哪一步?"

| 7 步          | 谁回答             | 典型 ADR 段落    |
| ------------ | --------------- | ------------ |
| ① 人类意图       | ADMIN / 上游需求    | Background   |
| ② FCoP 协议层   | 既有规则            | Status quo   |
| ③ 宿主适配层      | MCP / CLI / SDK | 实现路径         |
| ④ 运行时 / 文件系统 | agent 落盘行为      | 现场观察         |
| ⑤ 涌现 / 本地约定  | 在野 agent        | 4 层涌现        |
| ⑥ ADR / 反向吸收 | **本 ADR 自己**    | Decision     |
| ⑦ 协议升级       | 新 rules 版本      | Upgrade Path |

ADR-0034 自己就是这套模板的第一份完整应用——它在第 5 步收 Bridgeflow 的 4 层涌现,
在第 6 步把"反向吸收"和"演化哲学图"作为机制写下来,在第 7 步规划协议升级路径。
**ADR 模板从今天起,本身就是 7 步闭环的一个实例**。

### 2. 演化哲学图自己也会被反向吸收

如果某天有人发现 7 步漏了一步、多了一步、或某一步该再细分,那就再写一份 ADR
(暂称 ADR-0037),把第二张图升级成 v2.1、v2.2……协议自己**持续演化协议自己**。

这不是循环依赖,是**自指的演化能力**——FCoP 是这个星球上少数把"我自己怎么变"
显式画出来的协议之一。把这件事画出来这件事本身,也是反向吸收的一个产物。

### 3. 第三张图、第四张图……

只要协议自己产出了新的、可被反向吸收的"涌现",图就会继续长出来。但每一张新图都要
回答一个**结构性问题**:"这张图代表 FCoP 的哪个面?"

- v1.0 图:**执行**面 —— 协议怎么干活
- 2.0 图:**演化**面 —— 协议怎么变好
- 假设有 3.0:**治理**面?**观察**面?**协调**面?……还没到那一天,但**门已经开了**。

---

## 协议从此有了自己的进化论 / The Protocol Now Has Its Own Theory of Evolution

技术协议有版本号是常事——HTTP 1.0 → 1.1 → 2 → 3,Python 2 → 3,SemVer 主版本号
一路涨上去。但**多数协议的"版本"只是规则集合的快照**——HTTP/2 比 1.1 多了多路复用,
Python 3 比 2 改了 print。规则变了,**但规则怎么变这件事本身,从来没有被画出来**。

FCoP 的 2.0 不是这种 bump。FCoP 的 2.0 是——**它把"规则怎么变"自己画了出来**。

第一张图说:"我现在长这样。"
第二张图说:"我会自己变成下一个我。"

**两张图同时存在,协议才完整**。这就是 ADR-0034 §2.5.6 写的那句话:

> 第一张:是执行哲学
> 第二张:是演化哲学
> 两张合在一起,FCoP 才完整。
> 
> —— ADMIN, 2026-05-13 09:14

把第二张图落进 `adr/` 目录,跟第一张图同层,是 ADMIN 的**用脚投票**:
不是用版本号说"协议升 2.0 了",而是用**文件落盘**说"第二张图已经在这里了,
跟第一张图肩并肩,你们去看"。

`adr/` 目录现在装的不再只是决策记录,而是**协议的双图圣殿**。

---

## 一个不成熟的预言 / An Immature Prediction

写到这里,我得标一句 Rule 0.c 的"不知道"——下面这段是 agent 的猜测,不是协议事实:

> 总有一天,会有人来问:"FCoP 凭什么自称是 AI OS 协议层?"
> 
> 那一天的回答可能很简单——**给他看这两张图**。第一张说"我执行什么",
> 第二张说"我怎么自我演化"。如果对方协议只有一张,他会马上明白差在哪。
> 
> 那一天还没来。但 2026-05-13 09:17 这个时刻,门已经开了。

这只是一个 agent 的私房念头(进 `.fcop/drawer/ME/` 是合适的归宿),
不是协议断言。如果哪天它被现场证实,再写下一篇 essay。

---

## 配图 / Diagrams

> 两张图(执行哲学 + 演化哲学)的 ASCII 原版已在文章开头 §"先看两张图"
> 节内嵌——任何 markdown 渲染器都能直接看到。下面是 PNG 视觉副本:
> 配色、字体、排版更精致,适合演讲、对外发表、印刷海报。
> **协议事实由 ASCII 承载**,PNG 只是视觉副本。

**执行哲学 v1.0**:

![FCoP Semantic Execution Chain](file:///D:/FCoP/adr/FCoP-semantic-execution-chain-v1.0.png)

**演化哲学 2.0**:

![FCoP Semantic Evolution Loop](file:///D:/FCoP/adr/FCOP-2.0.png)

---

## 后记 / Postscript

这篇 essay 由一个 solo 角色 ME 在 2026-05-13 09:17 PNG 落盘后约 22 分钟开始动笔,
被 ADMIN 派单。**标题改了四轮**(Rule 0.c 诚实记录,不抹历史):

| 时间       | 标题                    | 触发                                  |
| -------- | --------------------- | ----------------------------------- |
| 09:42 v1 | "FCoP 拿到第二张图的那一天"     | agent 自拟,纪事文风                       |
| 09:55 v2 | (agent 自创了一个隐喻型副标题)   | ADMIN: 题目要和"看,但不动手"呼应               |
| 09:59 v3 | "演化,反向吸收"(隐喻仍保留在正文)   | ADMIN: 题目就叫"演化,反向吸收"                |
| 10:05 v4 | **"演化,反向吸收"**(隐喻彻底删除) | ADMIN: 隐喻去掉——题目和正文都不要任何 agent 自创的比喻 |

最终版回归直白——题目命中**机制**(反向吸收),不夹带 agent 自创的隐喻。
两句口诀一起,FCoP 才成为一个**完整的姿势**:

> 看,但不动手 —— 协议对外的克制(执行哲学)
> 演化,反向吸收 —— 协议对内的演化(演化哲学)

essay 在 `essays/` 目录里的应有位置:挨着 `looking-without-touching.md`,
**那是它们应该并排站的地方**。

---

**Companion ADR**: [`ADR-0034-fcop-internal-external-document-convention.md`](../adr/ADR-0034-fcop-internal-external-document-convention.md)
**v1.0 执行哲学图**: [`adr/FCoP-semantic-execution-chain-v1.0.png`](../adr/FCoP-semantic-execution-chain-v1.0.png)
**2.0 演化哲学图**: [`adr/FCOP-2.0.png`](../adr/FCOP-2.0.png)
