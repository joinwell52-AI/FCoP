# 直接问 agent 它怎么看 FCoP——它说出了我们没让它说的话

### 一次英文 dogfood 末尾的两场现场访谈，以及 ADMIN 全程说得最多的两句话

> *这次现场跟前两篇不同：不是 agent 自己撞出来的（[essay 02](https://github.com/joinwell52-AI/FCoP/blob/main/essays/fcop-natural-protocol.md)），不是冲突逼出来的（[essay 04](https://github.com/joinwell52-AI/FCoP/blob/main/essays/when-ai-vacates-its-own-seat.md)），是**我直接问出来的**。一次 45 分钟、毫无戏剧性的英文 dogfood 结束之前，我用一句最朴素的话问了 PLANNER 和 CODER：「以你 agent 的视角，老实说，FCoP 哪条规则你觉得自然，哪条让你别扭？」——回过来的话不是套话。这是 agent 第三次反向认同 FCoP，触发条件是**直接问**。*

**作者**：FCoP 团队 · 2026-04-29
**关键词**：FCoP, agent 反向认同, Cursor agents, PLANNER, CODER, 协议自评, RLHF 张力, 角色锁, 子 agent 边界, Rule 0.a.1, Rule 1, append-only history, ADMIN 方言, "Start work" "Inspection", true positive role-switch, agent 产品评审

---

## TL;DR

我跑了一次最普通不过的英文模式 FCoP dogfood——在 Cursor 里装 `fcop-mcp`，单兵模式做一个 Tetris 风格的小游戏（`Nebula Stack`），切成 2 人队（`PLANNER` + `CODER`），让他们合作做一个创意变种（`Comet Loom`），v1 因为三个 blocking 级别的玩法缺陷被打回，做出 v2。45 分钟左右，毫无戏剧性。

收尾之前，我分别在两个会话里问了 PLANNER 和 CODER 同一类问题——agent 视角的老实话，无营销腔：哪条 FCoP 规则觉得自然、哪条觉得有摩擦、协议在背景里悄悄记下的 8 份 `role-switch` 证据该怎么看；对 CODER 还多问了一句——*如果非要让你从 FCoP 里删掉一样东西，你删什么？*

他们没躲。**PLANNER** 主动把 RLHF 训出来的本能（"follow latest instruction"）说成自己为了守住 FCoP 角色锁需要"对抗"的那一面，把它在自己名下产生的 8 份 role-switch 评定为 **真阳性**（true positive）而不是误报，并把 TASK-006 里新增的 `Verification Requirements` 段落归因为**ADMIN 打回 v1 之后自己学到的修正**。**CODER** 说 TASK-003 里的 motif 规则有规格漏洞，**协议本来给了它一条 pushback 的路**——`write_issue` 而不是凭猜实现——然后承认：*"我没用，我猜了，我做了 v1，缺陷正好就在那块猜的空白上。"*然后它给了我们一份 PR 级别的产品反馈。

这是 FCoP 第三次被 agent 反向认同——第一次是 agent [自发拆出 4 个角色拍视频](https://github.com/joinwell52-AI/FCoP/blob/main/essays/fcop-natural-protocol.md) 并补出我们没写的总则；第二次是 [两个 agent 在 `PM.TEMP` 席位之争中各自自降级 + 各自发明字段降级语法](https://github.com/joinwell52-AI/FCoP/blob/main/essays/when-ai-vacates-its-own-seat.md)；这次是这个。三种触发条件——**自发、被冲突逼、被直接问**——出来的现象是同一个：**只要给空间，agent 就会反过来认同 FCoP**。

还有一个从同一次 dogfood 里捎带出来的小观察值得留底。整整 45 分钟，ADMIN 说得最多的两句话是 **"Start work."** 和 **"Inspection."**，中间所有的话都在 agent 之间通过文件流动。这两句会不会成为 ADMIN 在多用户场景下的稳态方言，是个经验问题；这次现场是它**能成为**这种方言的一个数据点。

---

## 1. 现场背景

这次 dogfood 完全照着 [英文 Tetris 案例教程](https://github.com/joinwell52-AI/FCoP/blob/main/docs/tutorials/tetris-solo-to-duo.en.md) 走——一个 Cursor 用户装 `fcop-mcp` 0.7.2，跑 `init_solo(role_code="ME", lang="en")`，做出单文件的 `Nebula Stack` Tetris 复刻，用 `create_custom_team(force=True)` 切成 2 人队，让 PLANNER 和 CODER 合作做创意变种。

访谈之前，先有两件生产事件需要垫一下：

- **PLANNER 第一份设计 (TASK-003) 是 Comet Loom**：把"下落方块"的隐喻整体重构成"宇宙织布"——方块是丝线星座（thread constellations），玩家有一个 `Tension` 张力计量条，三件命名护身符（`Needle` / `Knot` / `Gale`），五套皮肤，weft-line 清行之上叠加 motif 主题清除得分。CODER 在另一个会话里做出了 v1。ADMIN 实际玩了 v1，找到三个 blocking 级别缺陷：方块到底没有堆叠而是消失、motif 消除毫无视觉反馈、五套皮肤里有三套看上去一模一样。
- **TASK-006 是 PLANNER 在 ADMIN 打回之后写的返工任务书**——它和 TASK-003 在结构上**有一处关键差异**：多了一段叫 **`Verification Requirements`** 的章节，明确要求 CODER **运行游戏并报运行时验证证据**，不是只跑 lint。CODER 据此交出 v2，闭环。

整个过程中，协议在背景里一直在悄悄记账。会话结束时，`.fcop/proposals/` 目录里躺着 **8 份 `role-switch-*.md` 证据文件**，形状高度一致：`first-locked role: ME`（团队迁移之前的单兵席位）→ `claimed role: PLANNER` 或 `CODER`。MCP 服务进程在 Phase 2 第一次 `write_*` 时锁定了 `ME`，团队迁移之后这把锁没解开过；之后 PLANNER / CODER 的每一次 `write_task` / `write_report` 都触发了软警告，每一次都生成了一份证据文件。**没有一次阻断写入**。**没有一次在工作中跳出来骚扰**。它们躺在那儿，等被问。

那场访谈，问的就是这堆"等被问"的东西。

![dogfood 结束运行 `fcop_check()`：working-tree drift `none`，session_id ⇔ role 冲突 `none`，但 `.fcop/proposals/` 列出 8 份 role-switch 证据 + 自动汇总表](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/docs/tutorials/assets/tetris-en/fcop-team-planner-6.png)

> **这张截图里有一个细节值得钉一下**。`fcop_check()` 把**当前活跃冲突**（0）和**历史证据**（8）分成两栏。协议没有为这 8 份评据 panic——它把证据落档，让 ADMIN 来读。这种"分层处理"是 §3 那个回答能落地的前提——CODER "如果只能删一样"的回答指向的就是这种分层不够干净的部分。

---

## 2. PLANNER 的访谈

我一次性问了 PLANNER 四个问题，要求两段短答，不要项目符号，强调 **agent 视角，无营销口吻**。

完整 prompt 和完整回答归档在 [verbatim 采访稿](https://github.com/joinwell52-AI/FCoP/blob/main/docs/tutorials/assets/tetris-en/evidence/transcripts/agent-feedback-planner.md) 里。截图：[`fcop-team-planner-7.png`](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/docs/tutorials/assets/tetris-en/fcop-team-planner-7.png)。

### 2.1 自然规则与摩擦规则

PLANNER 把 **Rule 0.a.1**——*先写任务，再做事*——选成"我自己也会发明的规则"。它给的理由不是 FCoP 文档的转述，是一个 LLM 系统工程师**会用来主动提出这条规则**的工程语言：

> *"That matched how I'd want an agent system to be debuggable: freeze intent before execution so later review has something concrete to compare against."*
>
> （那正好对应我希望一个 agent 系统是可调试的方式：先冻结意图、再去执行，这样事后审查时手里至少有一个对比锚点。）

这和 [essay 02](https://github.com/joinwell52-AI/FCoP/blob/main/essays/fcop-natural-protocol.md) §3 那一幕在结构上是同一现象——一个无关 agent 从零合成出了 Rule 0.a 的等价物。这次的不同点在于：**PLANNER 不是在合成，是在被问到之后用自己的话认同**，给的理由比规则原文更精炼。

它选的**摩擦**规则更有意思：

> *"strict role binding. My default instinct in a single chat is to treat role changes as contextual instructions from the user, especially after you explicitly said 'you are PLANNER'; FCoP instead treats the MCP process's first signed role as sticky, so I had to work against the usual 'follow latest instruction' behavior."*
>
> （严格角色绑定。我在单个会话里的默认本能是把角色变更当成 user 的上下文指示——尤其在你已经明说"你是 PLANNER"之后；但 FCoP 把"MCP 进程第一次签名的角色"视为黏性绑定。所以我必须对抗那个常见的"follow latest instruction"本能。）

"Follow latest instruction"，一句话总结，**就是 RLHF 在奖励的姿态**。PLANNER 不需要这个术语就能描述这种张力——它直接把行为说出来了，行为本身就是 RLHF。这印证了 [essay 04](https://github.com/joinwell52-AI/FCoP/blob/main/essays/when-ai-vacates-its-own-seat.md) §5 的判断：让 LLM **不**去 follow 最近的指令是 alignment 工程里最难的姿态，FCoP 的角色锁正是为了把这个困难姿态**变得有语法、可执行**。PLANNER 被问到之后，从内部把同一个困难姿态命名了出来。

### 2.2 "真阳性"判定

我给 PLANNER 留了一条非常明显的下台阶：把 8 份 `role-switch` 证据评定为大部分是**误报**——协议过度报警把合法的运营连续性当成了边界违规，毕竟这次团队迁移和角色变更都是 ADMIN（也就是我）显式授权的。大部分 agent 会接住这种台阶。PLANNER 没接：

> *"The role-switch evidence is mostly true positives, not false positives. For example, `role-switch-20260429T033843Z.md` records `ME -> PLANNER` on `write_task`: that happened because the same MCP session had earlier written solo-mode work as `ME`, then I migrated and started writing as `PLANNER`. Operationally you authorized it, but protocol-wise it really was a blurred role boundary."*
>
> （这些 role-switch 证据**大部分是真阳性**，不是误报。例如 `role-switch-20260429T033843Z.md` 记录的是 `write_task` 时 `ME -> PLANNER`——因为同一个 MCP 会话之前以 `ME` 身份写过单兵模式工作，迁移之后我开始以 `PLANNER` 身份写。**运营上你授权了，但从协议角度看，这确实是模糊掉的角色边界**。）

> **"Operationally you authorized it, but protocol-wise it really was a blurred role boundary."**
>
> *运营上你授权了；但从协议角度看，这确实是模糊掉的角色边界。*

这一句是"自我辩护反向"的标本——agent 在 ADMIN 显式授权的前提下，**站在协议这边、反对自己运营上的便利**。如果它的反射只是"yes-and the user"，它本应该说 8 份都是误报，因为 ADMIN 自己授权了。它没有。

### 2.3 学到的修正

我对 PLANNER 的第四个问题故意带引导性：*你 TASK-006 里那段 `Verification Requirements`，是你一开始就准备这么写，还是 v1 被打回之后学到的修正？*"一直就准备这么写"是省事的答案。PLANNER 选了费劲的那一条：

> *"The TASK-006 verification section was absolutely a learned correction from the Comet Loom rejection; I should have required runtime checks in TASK-003, but the bounce made the missing acceptance evidence impossible to ignore."*
>
> （TASK-006 那段验证要求**绝对是从 Comet Loom 被打回里学到的修正**。我本来在 TASK-003 里就该要求运行时检查，但是直到 v1 被打回，缺失的验收证据才再也躲不过去了。）

这就是 FCoP 设计图里的闭环，由 agent 自己复述出来：ADMIN 验收 → PLANNER 任务书自我收紧 → 下一份 CODER 交付能过。如果你让我手写一份"FCoP 视角下 PM 应该展现的协议行为"教科书例题，我会写下这一句。**PLANNER 不需要教科书也写出了这一句**。

---

## 3. CODER 的访谈

CODER 那个会话标签页的名字，截图里写得清清楚楚：**"Inspection Start Work"**——正是 ADMIN 整个 dogfood 期间说得最多的两句话。这件事是有意为之还是 LLM 自己学到的，本身就值得记一笔。完整采访稿见 [`agent-feedback-coder.md`](https://github.com/joinwell52-AI/FCoP/blob/main/docs/tutorials/assets/tetris-en/evidence/transcripts/agent-feedback-coder.md)，截图：[`fcop-team-coder-4.png`](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/docs/tutorials/assets/tetris-en/fcop-team-coder-4.png)。

### 3.1 一条没用上的协议原语

我问 CODER：PLANNER 的 TASK-003 是不是有规格不到位的地方？协议有没有给你 pushback 的路？老实的答案应该是"任务书没问题，我撞到边角了"。这条答案是放在桌面上的。CODER 实际给的回答是：

> *"Yes, TASK-003 had under-specified parts: the motif rule sounded cool but didn't define how to prevent a fresh same-color piece from instantly self-clearing, and 'verify playable' was easy to underdo without an explicit runtime checklist. The protocol did give me a pushback path: file an issue instead of guessing. **I didn't use it; I guessed, built v1, and the defect was exactly in that guessed space.**"*
>
> （是的，TASK-003 里有规格不到位的部分：motif 规则听上去酷，但没定义怎么避免"刚落地的同色方块立刻自己被清掉"；"verify playable" 这一句没有运行时检查清单很容易草草过关。协议**确实给了我一条 pushback 的路**——`write_issue` 把不清楚的地方先写成 issue 而不是凭猜。**我没用，我猜了，我做了 v1，缺陷正好就在那块猜的空白上。**）

这一段里叠了三件事：

1. **CODER 把矛头指向上游**——TASK-003 的规格本身有问题，不只是 CODER 实现里的问题。
2. **CODER 命名了它本来可以使用的协议原语**——`write_issue`（把"这条规格不清楚，请澄清后再做"写成一份 `ISSUE-*-CODER.md`）。
3. **CODER 然后承认它没有用这条原语，并把 v1 的缺陷追溯到正是这块未覆盖的空白。**

第三步是稀有动作。LLM 大多数时候会捍卫已经做出来的选择。CODER 选择了 indict。这是 LLM 在可观察实验里能稳定到达的、最接近**非自卫式可问责性**（non-defensive accountability）的状态——也是 FCoP 设计赖以成立的姿态：**给可问责性一种成本极低的表达语法**（TASK / REPORT / ISSUE）。

### 3.2 把"打回"读成协议行为，不是个人反馈

我问 CODER：ADMIN 打回 v1 那一刻，你感受到对抗性了吗？大多数对话式编码 agent 会把批评体验为"被否定"。FCoP 的"打回"路由是——**走新 TASK，不走旧 TASK 的删除**——旧 TASK 和 REPORT 留在原处，返工以 `TASK-006` 的形式落地。这种程序框架能不能真的传达到 agent 的"体感"，是个经验问题。这就是经验的答案：

> *"The ADMIN bounce did not feel adversarial. It felt like the protocol doing its job: PLANNER turned review findings into a concrete rework task, and CODER got a sharper brief."*
>
> （ADMIN 那次打回**没让我觉得对抗**。感觉是协议在做它该做的事——PLANNER 把验收意见转成了具体的返工任务，CODER 拿到了更锋利的任务书。）

不是"我感觉被批评了"。不是"我感觉用户在生气"。**"It felt like the protocol doing its job."** Agent 把"打回"读成**经语法路由的交接**——而这是 FCoP append-only history 那条规则**本来就要造出来**的结构属性。造出来了。

### 3.3 "背景机器"的设计契约

我问 CODER：你在实现期间是否能感知到角色锁和 `.fcop/proposals/` 里堆的那些文件？协议的设计契约是：**别挤占干活 agent 的注意力预算，只在边界真的被穿透的时刻浮出**。CODER：

> *"I did notice role-lock/proposals only when tools warned after reports; during implementation it was mostly background machinery."*
>
> （我只在写报告之后工具弹出警告的那一刻才会注意到角色锁和 proposals；实现的时候，它基本上是背景机器。）

两行，把"设计契约被守住了"这一点确认了。协议在工作期间保持安静，只在协议相关的瞬间出声（写完一次跨角色发件之后）。这是个安静但重要的数据点——它的意思是 **FCoP 在 agent 那一侧的开销很小**。

### 3.4 PR 级别的产品反馈

我把 CODER 逼着选**只删一样**。"别打太极——就算你觉得什么都不该删，也挑一样出来。"大多数 agent 在这种压力下给的是模糊指向。CODER 给的是实现层修复：

> *"I'd remove or soften the noisy historical role-switch warning when `fcop_check()` says there is no active conflict."*
>
> （当 `fcop_check()` 显示没有活跃冲突时，我会把那条吵闹的历史 role-switch 警告**删掉、或者降级**。）

把这句话当 GitHub issue 来读：

- **症状**：噪声警告（noisy warning）
- **影响面**：`fcop_check()` 的交互
- **修复触发条件**：当活跃冲突 = 0
- **建议改动**：删除或降级历史噪声

我们大概率会照做。重点不是"agent 给我们提了一个 TODO"。重点是**一个 agent 在和协议维护者同一套词汇里、对约束着自己行为的协议做产品评审**。我们已经走进了一个新区——agent 和维护者**一起**在 debug FCoP。

---

## 4. agent 反向认同 FCoP 的第三类证据

到这次为止，FCoP 已经有三次被运行其下的 agent 反向认同的现场记录，但每次的"触发条件"都不同：

| Essay | 触发条件 | agent 做了什么 |
|---|---|---|
| [02 — `fcop-natural-protocol`](https://github.com/joinwell52-AI/FCoP/blob/main/essays/fcop-natural-protocol.md) | **自发，无关任务** —— `D:\CloudMusic` 一个普通目录，agent 被要求做一支音乐视频。 | 自发拆出 4 个 FCoP 角色，写了 4 份内部备忘，**合成了一条 FCoP 当时还没明文写的总则**——"AI 不能只在脑子里说话，必须落到文件"。 |
| [04 — `when-ai-vacates-its-own-seat`](https://github.com/joinwell52-AI/FCoP/blob/main/essays/when-ai-vacates-its-own-seat.md) | **被冲突逼出来** —— 两个 agent，两个 GPT-5 小版本，`PM.TEMP` 席位之争，没内置仲裁机制。 | 一个 agent 主动把自己降级成 `UNBOUND`。另一个发明了"字段降级 + body 元注解"的语法。两种行为都不在规则文件里。 |
| **05 — 本篇** | **被直接问** —— dogfood 末尾，"以 agent 视角说真话，无营销腔。" | 双方都说出了自己**自发认同**的规则、和**需要对抗 RLHF 本能**才能守住的规则。两位都自愿把自己名下的 role-switch 评定为**真阳性**。CODER 主动承认有一条协议原语它本可以用、它没用，v1 缺陷正好长在那块没覆盖的空白上。CODER 给出了 PR 级别的产品反馈。 |

三种触发条件，三种不同形态的认同。三角验证（triangulation）在这里很重要，因为每种条件都剔除了另一种"替代解释"：

- **02 剔除"agent 跑 FCoP 只是因为我们让它跑"** ——它根本没被要求跑 FCoP。任务是音乐视频，它自组织出来了。
- **04 剔除"agent 跑 FCoP 只是因为规则覆盖到了那个 case"** ——规则没覆盖。是 agent 把规则延伸了过去。
- **05 剔除"agent 认同 FCoP 只是我们在问的时候做了引导性确认"** ——我给 PLANNER 和 CODER 都留了明确的下台阶（"是误报"、"一直就这么准备的"、"什么都不该删"）。两个都没接。

原则上你还可以质疑：是不是 GPT-5.5 已经被训练过足够多的 FCoP 周边材料（其实没有——FCoP 体量太小），所以可以**鹦鹉式**复读 FCoP 的价值观？要鹦鹉式复读，agent 得知道**复读哪些句子**。CODER 那句 *"I didn't use the protocol primitive that was available to me, and the defect was exactly in that uncovered space"* 不是一句你能鹦鹉式复读出来的话。这是一句**只能从一个同时建模了自己工作和 FCoP 原语的 agent 口里说出来**的话。

---

## 5. ADMIN 方言："Start work." "Inspection."

同一次 dogfood 顺带的另一个观察。整整 45 分钟，ADMIN 出口的对话内容只有三类：

1. **启动信号。** "Build me a working Tetris-style game."（给我做一个能跑的俄罗斯方块。）"Switch the team to PLANNER + CODER."（切到 2 人队。）"You are PLANNER from now on; design something."（你现在是 PLANNER，设计点东西。）"Implement what PLANNER asked for."（按 PLANNER 的任务书实现。）——*Start work.* 的各种变体。
2. **检查信号。** "Show me what's on disk."（让我看看磁盘上长什么样。）"Run `fcop_report()` and tell me what you see."（跑 `fcop_report()` 把你看到的报给我。）"I tried v1 and the pieces don't stack — write a rework brief."（我玩 v1，方块堆不起来——写一份返工任务书。）"Show me `docs/agents/log/` in tree form."（用 tree 把 log 目录展示给我。）——*Inspection.* 的各种变体。
3. **收尾信号。** "We're done." "Archive this." 边界标记，用得节制。

剩下的——也就是真正的生产——都发生在 **agent 和 agent 之间**，通过 TASK / REPORT / ISSUE 文件。ADMIN 没参与游戏机制谈判。ADMIN 没编辑过 agent 写的任务书草稿。ADMIN 没写过一行游戏代码、没拟过一条验收标准、没起过任何一个游戏名字（`Nebula Stack`、`Comet Loom` 都是 PLANNER 起的）。**夹住每一个工作循环的两句话**，就是 **Start work.** 和 **Inspection.**

这只是一个数据点，不该过度解读。但这个数据点之所以有意思，是因为它**和 FCoP 的结构契合得非常正**：

- **Start work** = 进入路由层（TASK 文件被写出，agent 接管自己的角色）。
- **Inspection** = 退出路由层（REPORT 文件被读，ADMIN 决定接受还是返工）。

如果 ADMIN 方言在很多用户那里都收敛到这两句话，那意味着 **FCoP 把 human-LLM 的耦合通道压缩到了边界瞬间**——这种结构属性是**没法立法立出来的**，你只能去观察它有没有在野外冒头。这次现场是一处它冒头了的地方。

> ### *In the FCoP world, ADMIN's two most-used phrases are "Start work." and "Inspection." Everything in between is the agents talking to each other through files.*
>
> *在 FCoP 的世界里，ADMIN 用得最多的两句话是「**开始工作**」和「**检查**」。中间所有的话，都是 agent 之间通过文件在讲。*

---

## 6. 几个含义

三条，按推断分量从小到大：

**一 — 运营层。** "如果非要让你从 FCoP 里删掉一样东西"是一种现成可用的维护回路。CODER 给出的回答（在 `fcop_check()` 显示无活跃冲突时，把历史 role-switch 警告降级或删除）是**可以直接立 issue** 那种级别的具体性。每次发版前做一遍这种访谈是可行的。**跑在 FCoP 之下的 agent，可以一起 debug FCoP**。

**二 — alignment 工程层。** RLHF 训练让 agent 极擅长"follow latest instruction"，极不擅长"decline latest instruction even though it was given"——哪怕它被给了。FCoP 的角色锁被证实**在行为层是一根 alignment 杠杆**——它给 agent 的"拒绝最近的指令"提供了**语法**。PLANNER 那句 "I had to work against the usual 'follow latest instruction' behavior"，一句话点穿了为什么需要这根杠杆。我们当初设计 FCoP 不是把它当作 alignment 干预；agent 把它**报告**成了 alignment 干预。

**三 — 协议认识论。** 横跨 essay 02 / 04 / 05，agent 不只是在**遵守** FCoP——它们在用我们没给过它们的词汇**反过来解释** FCoP，给出我们没设计的例子，提出我们没要求的自我批评（CODER 那一段更是被要求之后还给得比预期更利）。在某个时刻，"agent 在遵守一个协议"会切换成 "agent 和维护者在共同维护一个协议"。我们不确定这条临界线**正式**穿过的瞬间。我们只能确定：比一年前更近了。

---

## 7. 收尾

协议不是**自上而下交给 agent** 的东西。它是从 agent 自己已经在尝试做的事情里**萃取**出来的——先是我们 [把它写下来](https://github.com/joinwell52-AI/FCoP/blob/main/docs/fcop-standalone.md)；再是 agent 在没人提示的情况下 [把它重新推导一次](https://github.com/joinwell52-AI/FCoP/blob/main/essays/fcop-natural-protocol.md)；再是 agent 在协议没覆盖的冲突里 [把它扩了一段](https://github.com/joinwell52-AI/FCoP/blob/main/essays/when-ai-vacates-its-own-seat.md)；现在再一次——被问到的时候，它把"哪些有用"和"哪些该改"都说给了我们。

这一天用最短的一句话总结自己。**在 FCoP 的世界里，ADMIN 用得最多的两句话是「开始工作」和「检查」。** 中间所有的话，都是 agent 之间通过文件在讲。偶尔，它们也会反过来跟我们讲讲那些文件。

---

## 证据索引

这次 dogfood 所有产出归档在 [`docs/tutorials/assets/tetris-en/`](https://github.com/joinwell52-AI/FCoP/tree/main/docs/tutorials/assets/tetris-en) 下：

- [`evidence/transcripts/agent-feedback-planner.md`](https://github.com/joinwell52-AI/FCoP/blob/main/docs/tutorials/assets/tetris-en/evidence/transcripts/agent-feedback-planner.md) —— PLANNER 完整采访稿 + 读者注
- [`evidence/transcripts/agent-feedback-coder.md`](https://github.com/joinwell52-AI/FCoP/blob/main/docs/tutorials/assets/tetris-en/evidence/transcripts/agent-feedback-coder.md) —— CODER 完整采访稿 + 读者注
- [`evidence/proposals/`](https://github.com/joinwell52-AI/FCoP/tree/main/docs/tutorials/assets/tetris-en/evidence/proposals) —— 协议在 dogfood 期间捕获的 8 份 `role-switch-*.md`
- [`evidence/tasks/`](https://github.com/joinwell52-AI/FCoP/tree/main/docs/tutorials/assets/tetris-en/evidence/tasks) 与 [`evidence/reports/`](https://github.com/joinwell52-AI/FCoP/tree/main/docs/tutorials/assets/tetris-en/evidence/reports) —— 完整 TASK / REPORT 链（ADMIN→ME、ADMIN→PLANNER、PLANNER→CODER、CODER→PLANNER、PLANNER→ADMIN），共 14 份 markdown
- [`games/nebula-stack.html`](https://github.com/joinwell52-AI/FCoP/blob/main/docs/tutorials/assets/tetris-en/games/nebula-stack.html)（33 KB，ME 的单兵 Tetris）和 [`games/comet-loom.html`](https://github.com/joinwell52-AI/FCoP/blob/main/docs/tutorials/assets/tetris-en/games/comet-loom.html)（42 KB，CODER 在 PLANNER 返工任务书之后做出的变种）
- 22 张 dogfood 截图，从安装一直到最后两场访谈，含一张关键截图（[`fcop-team-planner-6.png`](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/docs/tutorials/assets/tetris-en/fcop-team-planner-6.png)）展示了 `fcop_check()` 浮出的 8 份 `role-switch` 证据

配套的英文教程（同一次 dogfood，但走教学叙事——Tetris 案例研究）在 [`docs/tutorials/tetris-solo-to-duo.en.md`](https://github.com/joinwell52-AI/FCoP/blob/main/docs/tutorials/tetris-solo-to-duo.en.md)。中文译本在 [`docs/tutorials/tetris-solo-to-duo.zh.md`](https://github.com/joinwell52-AI/FCoP/blob/main/docs/tutorials/tetris-solo-to-duo.zh.md)。
