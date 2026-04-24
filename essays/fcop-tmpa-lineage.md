# 自然协议为什么站得住：FCoP 从 TMPA 中抽出来的那条伦理

### 姊妹篇是"这件事发生了"，这篇是"它为什么站得住"

> **Companion essay** to [*"An Anomaly I Can't Fully Explain: AI Doesn't
> Just Obey Rules — It Endorses Them"*](fcop-natural-protocol.md):
> that one documents the **phenomenon** — with transcripts, screenshots,
> and the four memos an agent wrote to itself during a `D:\CloudMusic`
> video task, entirely unprompted. *This* essay answers the question
> that phenomenon raises: **why does the principle that fell out of the
> agent's pen actually hold up?** The answer is not in the agent. It is
> in what came before FCoP — a specification called **TMPA**.

**作者**：FCoP 维护者 · 2026-04-21
**关键词**：FCoP, TMPA, 多角色审核, AI 伦理强制, 自然协议

---

## TL;DR

- 姊妹篇《[一个无法完全解释的现象](fcop-natural-protocol.md)》记录了 FCoP 总则"AI 角色之间不能只在脑子里说话，必须落成文件"是怎么**被一个 agent 意外写下来**的——那是现象层。
- 这篇 essay 回答下一个问题：**它凭什么站得住？**
- **FCoP 不是凭空出现的协议，它是从 TMPA 规范里抽出来的文件协作骨架。** TMPA 规范里早就写着同一条铁律——"多角色审核是 AI 伦理强制"——只是 TMPA 用 7 个 AI 角色硬扛，FCoP 把同一条伦理压缩到"一人一文件"。
- TMPA 的工程立意更大：**用纯文本时序替代传统分布式协调**——消息队列 / 数据库 / RPC / 编排器全部退场，只留一条按时间戳排序的纯文本消息流。FCoP 只拿走了其中最外层"文件即消息、文件名即路由"的那一层。
- 所以"自然协议"这个说法不是浪漫主义修辞。它是说：**FCoP 不是实验室里的轻量协议设计，它是 TMPA 这条规范层伦理在最小工作单元上的投影。** 一个 agent 一台电脑，只要坚持把工作落成文件再读一遍，就已经在执行多角色审核。
- 文件是"多角色"的物理载体。没有文件，所谓多角色自审只是同一个声音的幻觉。

> **Short version**: The sister essay captures *that* the agent
> spontaneously wrote FCoP's core principle during an unrelated task.
> This essay explains *why* that principle holds up at all — not because
> the agent got lucky, but because it independently rediscovered a rule
> already written into **TMPA** (Text-Message Multi-AI Parallel
> Architecture), a draft specification whose core bet is *using a
> plain-text temporal sequence to replace traditional distributed
> coordination*. TMPA's ethic layer says: *"Multi-role review is an
> AI ethics mandate."* FCoP is that same ethic compressed to its
> smallest viable form — one agent, one file, one readback.

---

## 1. 姊妹篇交代完的事，这里不再重复

姊妹篇已经用原始 JSONL 转录、4 张截图、4 份 agent 自发写的 `TASK-*.md` 证据档，讲清楚了两件事：

1. agent 在**完全无关**的任务里（`D:\CloudMusic` 一个歌曲视频生成），自发把自己劈成 ADMIN / PM / DEV 四个角色，写了 4 份公文给自己，然后才去生成视频
2. 当被追问"你为什么这么做"时，它援引了一条**在我们规则文件里根本不存在**的话——"AI 角色之间不能只在脑子里说话，必须落成文件"

那篇文章的结论是：这不是复读，是**升华**——agent 把分散在 7 个规则文件里的 2~8 条技术规定，合并、抽象、拟人化，压成了一句可以当信条贴在墙上的话。我们随后把它反向收回为 FCoP 的总则。

这篇文章要讲的是那篇没展开的另一半：**那条被升华出来的话，之所以能"贴得住"，是因为它并不是凭空出现的哲学命题。它早就以另一种形式，写在 FCoP 诞生之前的一份规范里。**

---

## 2. FCoP 的真实出处

FCoP 本身不是凭空出现的协议。它是从 **TMPA** 这份规范里抽出来的文件协作骨架。

就维护者掌握的谱系而言，完整 TMPA 的**主稿**是长文《TMPA — 文本消息多AI并行架构规范》。需要事先说明：**截至本文写作时，该全文尚未公开发表**；本 FCoP 仓只讲从那份稿子里**抽象出来的**协作层（纯文本时序、命名路由、多角色等），不附带 TMPA 正文。若未来全文公开发布，**以维护者届时公布的正式渠道与文件名为准**，此处不构成对未公开正文的再分发。

**TMPA**（Text-Message Multi-AI Parallel Architecture，文本消息多 AI 并行架构规范）是一份多 AI 系统的**架构规范**。它的核心立意，在工程层面是一个非常大的赌注：

> **用纯文本时序替代传统分布式协调。**
>
> 多 AI 系统不需要消息队列、数据库、RPC、编排引擎。只要有一条按时间戳排序的纯文本消息流，加上一套关于"哪种消息由谁处理"的命名约定，就够了。

这是 TMPA 把"多 AI 协作"这个问题降维到极点的方案——不用分布式中间件，只用一条由文本消息构成的时间线。在这个赌注之上，TMPA 规范面向 **NL2SQL + BI 分析 + 知识库查询 + 自主 SQL 生成**这类**一步出错就不可逆**的高风险场景做了具体化，规定了 7 个固定角色：

| 角色 | 职责 |
|---|---|
| Dispatcher | 把用户请求分发到合适的专家链路 |
| Guardian | 安全边界守护 |
| Specialist | 领域专家（SQL 生成、分析规划等） |
| Analyst | 数据解读 |
| Auditor | **审计员**——审核 SQL、审核输出、审核幻觉 |
| Executor | 实际执行（aiomysql 异步落库） |
| Conductor | 全链路编排 |

> TMPA is an architecture **specification** for multi-AI systems. Its
> core bet: *a plain-text temporal sequence replaces traditional
> distributed coordination* — no queue, no database, no RPC, no
> orchestrator, just a timestamped plain-text message stream plus a
> naming convention. On top of this bet, the TMPA spec defines seven
> fixed roles (including a dedicated Auditor between Specialist and
> Executor) for high-risk paths like NL2SQL and BI analysis.

时间线是：**先有 TMPA 规范，后有 FCoP**。FCoP 是把 TMPA 规范里"文件即消息、文件名即路由、YAML 元数据"这一层**通用化**抽出来的结果——它不是一个独立设计的协议，是 TMPA 这份规范的一个**子集**。

这条族谱很重要，类比：
- Django 是一套完整的 Web 应用框架，WSGI 是从里面抽出来的可复用协议
- Kubernetes 是一套完整的容器编排平台，OCI Runtime Spec 是从里面抽出来的可复用规范
- **TMPA 是一份完整的多 AI 架构规范，FCoP 是从里面抽出来的可复用协议**

所以 FCoP 的一些设计选择看起来"恰到好处"——这不是运气，是因为 TMPA 规范已经替它在更大的场景下验证过一遍了。

---

## 3. TMPA 的核心伦理

TMPA 规范里写了一条**伦理级**的铁律：

> **多角色审核是 AI 伦理强制。**
> **任何 AI 都不得独自从"理解"走到"执行"。必须有另一个 AI 从不同 prompt 视角审查。**

在 SQL 执行路径上这条尤其硬：Specialist 生成的 SQL **不经过 Auditor 审计，禁止落库**。原因很直白——SQL 执行不可逆，一次幻觉性的 `DELETE` 就能毁掉数据。

TMPA 规范里的 7 角色流水线，不是"冗余"也不是"纵深防御"，是**规范层面的伦理强制**。它不是"最好有 Auditor"，而是"**没有 Auditor 的 SQL 不允许进系统**"。

> The TMPA spec carries a hard rule at the ethics layer: *no single AI
> may go from understanding to execution alone — another AI, with a
> different prompt, must review it.* In the SQL path this is
> non-negotiable, because SQL execution is irreversible and one
> hallucinated `DELETE` can destroy data. The seven-role pipeline is
> not redundancy; it is mandated multi-role review written into the
> specification itself.

**这就是姊妹篇那条被 agent 升华出来的话的"另一个身份"**——它在 TMPA 里是一条写给 7 个 AI 角色的伦理强制，在 FCoP 里被压缩成一句写给任何 agent 的日常准则。

---

## 4. agent 升华的那句话，是这条铁律的最小化重发现

姊妹篇里那个 agent 完全不知道 TMPA 规范的存在。但当它在一次无关任务里写下"不能只在脑子里说话，必须落成文件"时——它做的其实是**把这条规范级铁律重新压缩成最小可行形式**：

| 形式 | TMPA | FCoP |
|---|---|---|
| 多角色审核 | 7 个 AI 实例，不同 prompt，互相审 | 1 个 agent 足以，但必须通过**文件**把自己劈成多个视角 |
| 强度 | 硬约束 | 同等硬约束 |
| 载体 | 纯文本时序 + 命名约定路由 | 磁盘 Markdown 文件 + 文件名即路由 |
| 失败模式 | Specialist 直接 commit SQL 不过 Auditor → 数据被污染 | Agent 在脑子里自审自批 → 幻觉被合理化成"结论" |
| 防御机制 | 7 角色流水线 | 把每一步落成 `TASK-*` / `REPORT-*` 文件 |

**两种形式扛的是同一件事**，只是密度不同：

- TMPA：**"一个人不够，需要 7 个。"**
- FCoP：**"一个人也够，但必须通过文件把自己劈开。"**

所以姊妹篇里看到的那个 agent，它不是"模仿了一个它读过的规则"——它是**独立重新发现了一条它从未读过、但训练语料里无数次接触过的职业伦理的最小可行形式**。这也是为什么它"贴得住"——贴住的不是这 agent 一时的灵光，是这条伦理本身的重量。

---

## 5. 为什么"文件"是关键

文件是"多角色"的物理载体。

- **脑子里想**：提案人和审查者是同一个声音，review 只是更多合理化。你在审你自己，但你只有一个声音。
- **落成文件**：提案被**外化**成一个可被"另一个自己"冷眼读的对象。你回头去读那个文件时，你是**一个新的阅读者**——带着新的语境、新的关注点、新的批判视角。审查者那一刻才真正出生。

没有文件，所谓多角色审核就只是**同一个声音的幻觉**。

> A file is the physical substrate that lets "multi-role review" actually
> happen. In your head, the proposer and the reviewer share one voice —
> the "review" is just more rationalisation wearing a different hat. On
> disk, the proposal is externalised into an object that another reading
> of yourself can confront cold. *That* reading is a new reviewer.
> Without externalisation, multi-role review is a hallucination in a
> single voice.

这也解释了为什么 FCoP 能从 TMPA 独立出来：**TMPA 用 7 个不同 prompt 扛住这条伦理，FCoP 把同一条伦理压缩到一个 agent 身上，但要求它必须通过文件把自己劈开。** 两者扛的是同一个东西，只是形式密度不同。

---

## 6. 这给 FCoP 的立意带来什么

FCoP 不是"轻量协议设计"，它是**AI 伦理强制在最小工作单元上的投影**。

当一个 agent 按 FCoP 工作时——回头看姊妹篇里那个 `D:\CloudMusic` 任务——它做的事情其实都是这条伦理的具体落地：

- 写 `TASK-*-ADMIN-to-PM.md` ← 把"我要什么"落成可被另一个角色审查的对象
- 写 `TASK-*-PM-to-ADMIN.md` ← 把"我怎么理解你要的"落成可被 ADMIN 审查的对象
- 写 `TASK-*-PM-to-DEV.md` ← 把"执行计划"落成可被 DEV 自己审查的对象
- 写 `TASK-*-DEV-to-PM.md` ← 把"我做了什么"落成可被 PM 复核的对象

每一份 `TASK-*.md` 都不是"文档"，是**主动把自己劈开一个审查视角**。文件不是存档，文件是**让审查者这个角色能独立存在的物理条件**。

这也是为什么 FCoP 的配套工具箱（可选的 MCP 实现）里，**保险丝型扳手**这一类工具会存在——比如 `drop_suggestion`：

- 它不做任何"有用"的事
- 它存在的全部价值是**阻止 agent 绕过协议偷偷修改全局 Rules 文件**
- agent 对协议有意见？调它，把意见落成文件，继续干活
- 这恰好是总则"不能只在脑子里说话"在 agent 和协议之间的具体落地

> This is also why FCoP's optional toolbox includes *safety-fuse wrenches*
> like `drop_suggestion`: the tool itself does nothing useful. Its entire
> value is to prevent an agent from silently editing the rules file when
> it disagrees with the protocol. Disagreement, too, must land as a file.

---

## 7. 一句话收束

- TMPA 用 7 个 AI 硬扛"多角色审核是 AI 伦理强制"
- FCoP 把同一条伦理压缩到"一人一文件"
- 姊妹篇里那个 agent，是在没读过 TMPA 的情况下，把它最小化重新发现了一遍
- **这条原则之所以"自然"——不是因为它从天上掉下来，而是因为它在 AI 工程的最深处早就写好了，只是在这次被一个 agent 顺手翻到最表层**

这是姊妹篇和这篇合在一起要说的事：*现象* 是 agent 自己写下了这条原则，*原因* 是这条原则本来就在那儿。

---

## 相关 / Related

- 姊妹篇 · [一个无法完全解释的现象：AI 不止服从规则，它认同规则](fcop-natural-protocol.md) · [English version](fcop-natural-protocol.md) *(bilingual)*
- **Agent 侧规范（成对、缺一不可）**：[`fcop-rules.mdc`](../src/fcop/rules/_data/fcop-rules.mdc)（总则）· [`fcop-protocol.mdc`](../src/fcop/rules/_data/fcop-protocol.mdc)（解释）→ 部署到 `.cursor/rules/`
- 田野报告 · [当 AI 自己整理工作](when-ai-organizes-its-own-work.md) · [Field Report (EN)](when-ai-organizes-its-own-work.en.md)
- [English version / 英文版本](fcop-tmpa-lineage.en.md)

---

**License**: MIT (see `LICENSE` in repo root)
**署名**：这篇 essay 的写作本身就是 FCoP 主张的那种协作——agent 升华原则，人类识别并落成文件。文本由 **FCoP 维护者**修订、发布。
