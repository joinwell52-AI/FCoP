# FCoP Essays · 现场报告与设计哲学

本目录收录 FCoP 协议演化过程中的**现场报告、涌现记录与设计哲学文章**。

与 `adr/`（架构决策记录）不同，这里的文章不是决策快照——它们是：

- **dogfood 现场报告**：真实项目里 agent 做了什么、协议表现如何
- **涌现记录**：agent 自发产出的行为 / 规则 / 字段，以及如何被协议吸收
- **设计哲学**：协议维护者对"为什么这样设计"的回答

---

## 文章索引

| # | 标题 | 版本 | 一句话摘要 |
|---|---|---|---|
| 01 | **When AI Organizes Its Own Work / 当 AI 自己组织工作** | [English](when-ai-organizes-its-own-work.en.md) · [中文](when-ai-organizes-its-own-work.md) | 4 个 agent（PM/DEV/QA/OPS），48 小时，一个空文件夹——以及 6 个我们从没写下来的协调模式。 |
| 02 | **An Unexplainable Thing I Saw / agent 不只是遵守规则，它背书了规则** | [中文](fcop-natural-protocol.md) · [English](fcop-natural-protocol.en.md) | 一个 agent 在完全无关的任务里，自发拆成 4 个 FCoP 角色，把我们散乱的规则升华成一条我们从没写过的原则。 |
| 03 | **Why the Natural Protocol Holds Up — FCoP's lineage from TMPA** | [中文](fcop-tmpa-lineage.md) · [English](fcop-tmpa-lineage.en.md) | essay 02 的姊妹篇：那篇证明"原则涌现了"，这篇解释"为什么它站得住"——FCoP 从 TMPA 提炼而来，agent 那句话是早已写好的 AI 伦理规范的最小可行形式。 |
| 04 | **Saying "No" Is the Hardest Thing for an LLM — FCoP Gives It Grammar** | [中文](when-ai-vacates-its-own-seat.md) · [English](when-ai-vacates-its-own-seat.en.md) · [证据存档](when-ai-vacates-its-own-seat-evidence/INDEX.md) | 一台机器，两个 Cursor 会话，两个 GPT-5 小版本。原 PM 自行退位至 UNBOUND；新 PM.TEMP 用一行 body 走完未写的协议路径。我以为会冲突，结果没有。 |
| 05 | **Tutorial: From Solo to a 2-Person AI Crew** | [English (Tetris)](../docs/tutorials/tetris-solo-to-duo.en.md) · [中文（俄罗斯方块）](../docs/tutorials/tetris-solo-to-duo.zh.md) · [中文（贪吃蛇）](../docs/tutorials/snake-solo-to-duo.zh.md) | 45 分钟上手教程（两个并行案例）：从 solo 模式出发，切换到双人 AI 团队，PLANNER 设计 / CODER 实现。含完整 review-and-rework 周期与回顾采访。 |
| 06 | **What the Agents Say About FCoP, When You Ask Them** | [中文](what-agents-say-about-fcop.md) · [English](what-agents-say-about-fcop.en.md) | agent 背书 FCoP 的第三类证据（继 essay 02「自发、无关任务」和 essay 04「冲突触发」之后）：直接问。PLANNER 和 CODER 各自描述了为了遵守协议必须克服的本能。 |
| 07 | **当 agent 从自己的残骸中学习** | [中文](when-agents-learn-from-their-own-wreckage.md) · [English](when-agents-learn-from-their-own-wreckage.en.md) · [CSDN](https://blog.csdn.net/m0_51507544/article/details/161028380) | codeflow 项目一日 14 个 agent 涌现现场报告（2026-05-12）：USER HOME 全局污染 / GATE 描述自命中 / `supersedes:` 字段现场发明——协议以小时级速度零崩溃反向吸收全部涌现。 |
| 08 | **协议为什么短，历史为什么长** | [中文](why-the-protocol-stays-short.md) · [English](why-the-protocol-stays-short.en.md) | 一份给协议维护者的设计哲学答案："这样的涌现会不会没有止境？"——四类涌现的处理路径、三条结构力学、协议骨架冻结的代价与价值。 |
| 09 | **当 validator 撞向自己的镜像** | [中文](gate-design-pitfalls-case-studies.md) · [English](gate-design-pitfalls-case-studies.en.md) | 从 codeflow OPS I-14 看 validator-validates-itself 反模式：GATE 在检查 staged diff 时命中了 GATE 描述本身——系统性解剖与"语义化实证"根治姿势，以及它如何成为 `fcop-protocol.mdc §GATE Design Pitfalls` 的源头案例。 |
| 10 | **一行 frontmatter 的旅程** | [中文](the-supersedes-field-story.md) · [English](the-supersedes-field-story.en.md) | `supersedes:` 字段从一次协议两难（三条规则同时成立）到 `ipc-envelope.schema.json` 正式字段的两小时旅程——展示 FCoP 涌现落地的最低成本路径。 |
| 11 | **看，但不动手** | [中文](looking-without-touching.md) · [English](looking-without-touching.en.md) · [CSDN](https://blog.csdn.net/m0_51507544/article/details/161028161) | FCoP 三层语义执行链科普：`fcop_audit()` 为什么"只看不改"——L1 检测 / L2 解释 / L3 文档三层把"看见"和"动手"切开，产出 `INSPECTION.md`（建议非命令），执行权留给人。`adr/FCoP-semantic-execution-chain.md` 的科普版。 |
| 12 | **五大 AI 模型眼中的 FCoP** | [中文](what-five-ai-models-say-about-fcop.md) · [English](what-five-ai-models-say-about-fcop.en.md) | 把 FCoP 核心文档喂给 ChatGPT / Claude / DeepSeek / Grok / 豆包，只问一个问题："你是 agent，你怎么看这套协议？"——五种截然不同的内部视角，以及它们之间最有意思的分歧。 |

---

## 阅读建议

**第一次接触 FCoP**：从 essay 01 开始，了解协议在实际项目里如何运作。

**关心 agent 是否真的"理解"协议**：essay 02 / 04 / 06 / 12 构成一个渐进的证据链（无关任务自发 → 冲突触发 → 直接问内部 agent → 问外部 AI 模型）。

**关心协议如何演化**：essay 07 / 08 / 09 / 10 记录了协议从压力测试到字段级收编的完整过程（2026-05-12 这一天）。

**关心协议工具如何设计**：essay 11（科普）配合 ADR 目录的 `ADR-0030 / 0031 / 0032` 一起读，理解 `fcop_audit()` 为什么是三层架构、为什么"只看不改"。

**协议维护者 / 贡献者**：essay 08（为什么协议要短）和 ADR 目录里的 `ADR-0029`（FCoP 哲学宪章）是最重要的背景读物。

---

> 现场报告欢迎投稿。如果你在自己的项目里用 FCoP 遇到了有意思的情况（好的坏的都算），欢迎开 issue 或向 `essays/` 提 PR。协议通过现场笔记演化，不通过委员会修订。
