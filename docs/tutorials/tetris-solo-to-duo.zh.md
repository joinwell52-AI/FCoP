# 【免费开源】【多 agent 实战】【教你怎么指挥 agent】：FCoP-MCP 让 AI 团队有纪律

### 从单 agent 写俄罗斯方块到 2 人 AI 小队——一篇 45 分钟的 `fcop-mcp` 现场教程

![FCoP-MCP 教程封面 · 用文件系统给多 agent 立规矩](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/assets/fcop-mcp-tutorial-cover-v1.png)

> **中文译本说明** | 本文是英文原版 [`tetris-solo-to-duo.en.md`](tetris-solo-to-duo.en.md) 的**中文译本**，目的是让中文读者快速通读这一**俄罗斯方块案例**。原文为权威版本，如有差异以英文版为准。
>
> **中文母语案例**请读姊妹篇 [`snake-solo-to-duo.zh.md`](snake-solo-to-duo.zh.md)（贪吃蛇案例，[CSDN 已发表](https://blog.csdn.net/m0_51507544/article/details/160603953)）——同一份协议，不同的 dogfood，不同的现场彩蛋。两个案例任选其一作为入门都行。

> *"你不再是码农，你是指挥官。AI 是你的数字员工。"*
>
> *"在 FCoP 的世界里，ADMIN 用得最多的两句话是「**开始干活**」和「**检查**」。中间发生的所有事，都是 agent 通过文件互相对话。"*
>
> 一篇 45 分钟的 `fcop-mcp` 0.7.2 + Cursor 实战教程：让 agent 自己装好工具、单 agent 模式做一只俄罗斯方块、一句话切到 2 人小队（PLANNER + CODER）、看他俩自己设计 + 实现一个创意变体、ADMIN 试玩拒收 v1、PLANNER 写返工任务、CODER 出 v2、最后当面问两个 agent 对协议怎么看。**每一步都是真的，每个文件都在硬盘上，每张截图都来自同一次 45 分钟会话。** 阅读约 25 分钟。

**作者**：FCoP Maintainers · 2026-04-29
**关键词**：FCoP, fcop-mcp, Cursor MCP, 多 agent 协作, 角色边界, append-only 历史, ADMIN 指挥官, 文件协议, "开始干活"/"检查" 方言, agent 上下文预算, 单 agent 上下文爆炸, true-positive role-switch 证据, agent 自评, 指挥 agent 6 条铁律

---

## 这篇文章为什么存在

每个 Cursor / Copilot / Claude Code 用户都撞到过这三件事，不管他给它叫什么名字：

1. **单 agent 上下文爆炸是真的。** 一个 agent 包揽设计、编码、测试、写文档、重构——它的上下文窗口变成一个全是半相关碎片的垃圾桶。agent 同时变慢、变笨、自信地说错话。
2. **你不再是码农，你是指挥官。** 市场正在从"人类写代码、AI 辅助"切到"人类陈述意图、AI 写代码"。你还自己敲键盘，就等于在买一场已经散场的戏的票。真正值钱的技能是**指挥**——选什么做、派下去、签收。读完这篇你会发现这个方言只剩两句话：「**开始干活**」和「**检查**」。
3. **只有文件——不是聊天——才是可审计的载体。** 聊天记录是金鱼的记忆，文件是一本账本。每一条落盘记录的目的都只有一个：**管理、追溯、审计、有序、有规则**。

`fcop-mcp` 就是把这三个观察变成 Cursor 里能跑的东西的 MCP server。它实现了 [FCoP](https://github.com/joinwell52-AI/FCoP) 协议——一个极简多 agent 协作协议，唯一的同步原语就是在文件夹树上做 `os.rename()`。没有数据库、没有消息队列、没有守护进程。状态是文件夹，路由是文件名，载荷是 Markdown。**文件名即协议。**

本教程走完一次连续的真实会话，三个观察都会被它戳到：

| 阶段 | 用时 | 你会看到什么 |
|---|---|---|
| 1. 安装 | ~5 分钟 | agent 替你装 `uv`、`fcop-mcp`，替你改 `mcp.json`。**你一行命令都不用敲。** |
| 2. 单人写俄罗斯方块 | ~15 分钟 | 一行自然语言→ agent 把它翻成 `TASK-*.md`→ 写出 `Nebula Stack`（一只能跑的单文件俄罗斯方块）→ 写报告→ 归档。这就是四步循环。 |
| 3. 切到 2 人小队 | ~5 分钟 | 一句话：`create_custom_team(force=True)` 加 `PLANNER` + `CODER`。原来的单人 `ME` 整套配置归档进 `.fcop/migrations/<时间戳>/`（Rule 5）。每个 agent 都拿到自己的 `TEAM-*.md` 员工手册。 |
| 4. 一个创意变体，带真实评审循环 | ~15 分钟 | ADMIN：*"给我搞个有创意的俄罗斯方块变体。"* PLANNER 设计了 `Comet Loom`。CODER 在另一个 chat tab 里出 v1。ADMIN 试玩，找出 3 个 blocker 拒收。PLANNER 写 `TASK-006`，多了一段 `Verification Requirements`。CODER 出 v2。两个循环，全部落盘。 |
| 5. 协议自己说话 | （无声地记录） | `fcop_check()` 揭示协议在 dogfood 期间静默地记录了 **8 份 `role-switch-*.md` 证据**——agent 工作时根本没看见的软告警。然后我们当面问 PLANNER 和 CODER 对 FCoP 怎么看。他们没回避，亲口指出 RLHF 张力，其中一个还提交了 PR-grade 产品反馈。 |

如果你嫌教程太长：直接跳到底部的**指挥 agent 的 6 条铁律**。中间这一切只是这 6 条铁律的*现场证据*。

> **想立刻试一下？** 直接跳到下面的**阶段 1**——安装大概 5 分钟，你一行命令都不用敲，半小时之内就有一只能跑的俄罗斯方块在 Cursor 里。文章不会跑，回来继续读。

---

## 阶段 1 —— 用自然语言装好它

打开 Cursor。打开一个空文件夹（比如 `D:\fcop-mcp-test`）。你应该看到的就是这一幕——空白编辑器、空 workspace、空对话框。还没什么神奇的事发生。

![Cursor 在一个空文件夹里刚打开 —— 空白 workspace、默认 UI、英文 locale，本教程就是从这张画布开始的](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/docs/tutorials/assets/tetris-en/cursor-new-en-0.png)

往对话框里贴这一段：

> 帮我把 `fcop-mcp` 装到 Cursor 里。每个命令你自己跑，步骤如下：
>
> 1. 检测我的 OS（`uname -s 2>$null; echo $env:OS`）。
> 2. 缺 `uv` 就装（Windows 用 `irm https://astral.sh/uv/install.ps1 | iex`；macOS/Linux 用 `curl -LsSf https://astral.sh/uv/install.sh | sh`）。装完用 `uvx --version` 确认。
> 3. 把 `fcop` 加进我的全局 `mcp.json`（Windows 在 `%USERPROFILE%\.cursor\mcp.json`，macOS 在 `~/.cursor/mcp.json`），保留已有的其他 server：
>
>    ```json
>    "fcop": { "command": "uvx", "args": ["fcop-mcp"] }
>    ```
>
> 4. 把改完后的 `mcp.json` 内容打印出来给我看。
> 5. 提醒我重启 Cursor、第一次启动等 30–60 秒（uvx 拉依赖）。
>
> 每完成一步就汇报一次。**不要**自动 init 项目——那是我的事。

完整 prompt 维护在 [`agent-install-prompt.en.md`](https://github.com/joinwell52-AI/FCoP/blob/main/src/fcop/rules/_data/agent-install-prompt.en.md)（也有[中文版](https://github.com/joinwell52-AI/FCoP/blob/main/src/fcop/rules/_data/agent-install-prompt.zh.md)），同时作为 MCP resource `fcop://prompt/install` 暴露出来，新会话里的 agent 可以直接读。重启之后在对话框里输入 `fcop_report()`，你应该看到类似 `fcop-mcp 0.7.2 — not initialised — rules/protocol up-to-date` 的输出。**每个命令都是 agent 跑的。你只是在指挥。**

![Cursor Settings 展开 fcop 的 26 个工具——`init_solo`、`write_task`、`write_report`、`fcop_check` 等等——右侧 chat 显示 agent 正在按 install prompt 一步步走](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/docs/tutorials/assets/tetris-en/fcop-mcp-setup-0.png)

尘埃落定后，"装好且就绪"的样子是这样的——`mcp.json` 已更新，`uvx` 已经缓存了 package，Cursor 把 `fcop` 当作一个活跃的 MCP server，`fcop_report()` 返回"还没 init"的状态。

![重启后：`fcop_report()` 返回 "fcop-mcp 0.7.2 — not initialised — rules/protocol up-to-date"。MCP server 已经活着，但项目还没 bind——这正是 init 之前你想要的状态](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/docs/tutorials/assets/tetris-en/fcop-mcpsetup-over.png)

---

## 阶段 2 —— 单人模式写俄罗斯方块（四步循环）

告诉 agent 它是谁，然后丢一行 brief：

> 1. `set_project_dir("D:/fcop-mcp-test")`
> 2. `init_solo(role_code="ME", lang="en")`
> 3. *"给我做一只能跑的俄罗斯方块，单文件 HTML，不要外部依赖。自己取名，做得好玩点，加道具/技能、皮肤、像样的视觉、带点炫酷特效。用 FCoP 四步循环。"*

注意刚才发生了什么。**你只说了五行自然英文。** agent 把它扩展成一份结构化的产品 spec——必备特性、验收标准、可运行性检查——然后把它写成 `docs/agents/log/tasks/TASK-20260429-001-ADMIN-to-ME.md`。**这一翻译就是价值。** agent 没问你要 brief，它替你做了一份，签上你的名字，落盘。

这就是 **Rule 0.a.1**，FCoP 的"四步循环"：

```
TASK  →  do  →  REPORT  →  archive
```

接下来 ~15 分钟你会看到：

- TASK 文件落进 `docs/agents/log/tasks/`。
- 游戏文件 `workspace/nebula-stack/index.html` 被写出来。
- 一份 `REPORT-001-ME-to-ADMIN.md` 落进 `docs/agents/log/reports/`。ME 给游戏取名叫 **Nebula Stack**——单文件 HTML，无依赖，含下落方块、hold + next preview、计分、关卡、三个道具（`Bomb`、`Stasis`、`Prism`）、三套皮肤（`Aurora Candy` / `Ember Arcade` / `Moonstone Mono`）、一个星空背景。
- `archive_task` 把两个文件挪进历史 log。**从此那两个文件不可变**（Rule 5：append-only 历史）。

打开 `nebula-stack/index.html`，能玩。但真正的产出不是这只游戏——而是**四步循环跑起来了**。从今往后，每次你给 agent 派活，这个循环都会跑一次。

![ME 正在写 *Nebula Stack* —— agent 在 `workspace/nebula-stack/` 直接写单文件 HTML 实现，不在 chat 里。注意四步循环怎么把 chat 让到产出物的旁边去](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/docs/tutorials/assets/tetris-en/fcop-solo-Build-1.png)

![浏览器里的 *Nebula Stack* —— ME 用一行自然语言 brief 交付的俄罗斯方块；下落方块、三套皮肤、三个道具、单文件 HTML、零依赖](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/docs/tutorials/assets/tetris-en/game-0.png)

### `init_solo` 之后硬盘上有什么

```
fcop-mcp-test/
├── .cursor/rules/fcop-rules.mdc      # agent 的规则手册
├── AGENTS.md  CLAUDE.md              # 跨 host 的入口
├── .fcop/                            # 协议元数据、版本钉、角色锁
├── docs/agents/
│   ├── shared/
│   │   ├── TEAM-README.md            # 这支团队是干嘛的，大白话
│   │   ├── TEAM-OPERATING-RULES.md   # 四步循环、角色唯一性等等
│   │   └── TEAM-ROLES.md             # 谁是 `ME`、能干什么
│   ├── log/{tasks,reports}/           # 不可变账本
│   ├── tasks/  reports/  issues/      # 实时收件箱
│   ├── fcop.json                      # 项目配置（mode、roster、lang）
│   └── ...
└── workspace/                        # 真正的代码住这儿
```

![`init_solo` 之后真实的文件树——文件名跟上面 ASCII 图一一对应；这是硬盘事实，不是示意图](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/docs/tutorials/assets/tetris-en/fcop-mcp-solo-0.png)

三个文件夹值得停一下。

- `.cursor/rules/fcop-rules.mdc` 在 Cursor 每一回合都被加载。**agent 物理上没法忘记协议**，因为 Cursor 帮它记着。
- `docs/agents/shared/TEAM-*.md` 是 agent 的**员工手册**。单人模式下它告诉 `ME` "你是唯一员工，啥都你干"；团队模式下它告诉 `PLANNER` 和 `CODER` 各自的职责边界。
- `docs/agents/log/` 是账本。**只增不删**。订正不靠 edit——靠写一份*新*报告覆盖旧的。

如果在新 chat 里问 agent *"你是谁"*，它**不会**说"我是 GPT-5.5，您的助手"。它会读 `.fcop/team.json` 和 `docs/agents/shared/TEAM-ROLES.md`，然后告诉你它是 `ME`、它给 ADMIN 干活、它走四步循环、它在 `workspace/` 交付。**agent 的身份现在住在硬盘上，不在 chat 里。** 这就是协议的全部精华，被你摸到了一次。

![被问"你是谁？"，agent 朗读出 `.fcop/team.json`，从 `TEAM-ROLES.md` 解释自己的角色—— identity-on-disk 的活演示](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/docs/tutorials/assets/tetris-en/fcop-mcp-solo-1-who.png)

---

## 阶段 3 —— 一句话切到 2 人小队

往 chat 里丢这句：

> *把团队切成两个人：`PLANNER` 和 `CODER`。PLANNER 设计，CODER 实现。用 `create_custom_team(force=True)`，保留 `lang="en"`，告诉我哪些被归档了。*

agent 调 `create_custom_team`。硬盘上发生的事：

- 旧的 `fcop.json`、单人模式的 `shared/TEAM-*.md`、给 ADMIN 的入口信、之前的 `.cursor/rules/`，**全部归档**到 `.fcop/migrations/20260429T112757/`——本地时间胶囊，不需要 git。（你这边时间戳会不一样；我那次是 dogfood 当天的 11:27:57。）
- 新的 `shared/TEAM-*.md` 描述一支 2 人小队，PLANNER 和 CODER 各有独立的职责段。
- `fcop.json` 和 `.fcop/team.json` 更新到新 roster（`mode: team`、`roles: [PLANNER, CODER]`、`leader: PLANNER`）。
- **关键：`docs/agents/log/` 没动。** 阶段 2 那只 `Nebula Stack` 的 TASK 和 REPORT 留在原地，不可变。ME 下班了，但 ME 的产出还在账本里。这就是 Rule 5——append-only 历史。
- 当前 chat 会话**仍然绑定单一角色**。要让 PLANNER 和 CODER 并发干活，你得开*两个* Cursor chat tab——一个绑 PLANNER，一个绑 CODER——他们之间通过 `TASK-*.md` 文件通信，而不是通过 chat。

这就是 **Rule 1：两阶段启动**。init 一次，从此之后只 assign 角色。**Rule 5 又来了**：单人模式的历史不会被删，只是被封存并打上日期。

![agent 报告迁移结果——旧的单人文件已归档进 `.fcop/migrations/20260429T112757/`，新团队的 `shared/` 文件就位，`docs/agents/log/` 完全没碰](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/docs/tutorials/assets/tetris-en/fcop-team-0.png)

迁移之后，你通常会开两个 Cursor chat tab 并排——一个绑 PLANNER，一个绑 CODER——他们**只**通过 `docs/agents/` 里的 TASK / REPORT 文件通信。没有 chat-to-chat 转手。没有把设计笔记复制粘贴。协议让"走文件路径"成为最省力的路径。

![团队迁移之后两个 Cursor chat tab 并排——左边 PLANNER，右边 CODER，两边都刚刚在新 2 人团队下重新初始化好。从这一刻起他们只通过 TASK 和 REPORT 文件说话](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/docs/tutorials/assets/tetris-en/fcop-team-1.png)

---

## 阶段 4 —— Comet Loom：设计 → 出 v1 → 评审失败 → 出 v2

ADMIN 在 PLANNER 那边的 chat tab 里说：

> *"给我搞一个那只俄罗斯方块的创意变体。打破隐喻。名字、主题、机制改造你自己拍。单文件 HTML。游戏代码你自己别写——那是 CODER 的活。"*

![ADMIN 把这句自然语言 brief 丢进 PLANNER 的 chat tab——一句话，没有结构化 spec。PLANNER 的活就是把这个意图翻译成一个真正的 TASK 文件](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/docs/tutorials/assets/tetris-en/fcop-team-planner-2.png)

PLANNER 想了 5 分钟，写出一份真正的产品 brief，不是凭感觉。变体取名 **Comet Loom**：棋盘是悬浮在太空中的一架立式织布机，下落的方块是*线团星座*，line clear 改名叫*完成的纬线*，一个 `Tension` 计量条跟踪织机离溢出还有多远，三个有名字的护身符（`Needle` / `Knot` / `Gale`）通过游玩获得，五套皮肤（`Deep Aurora`、`Solar Loom`、`Rain Archive`、`Moss Galaxy`、`Paper Lanterns`）。这份 brief 写成 [`TASK-20260429-003-PLANNER-to-CODER.md`](assets/tetris-en/evidence/tasks/TASK-20260429-003-PLANNER-to-CODER.md)，130 多行验收标准。PLANNER 还写了一段 `REPORT-003-PLANNER-to-ADMIN.md`，意思是*"设计就绪，作为 TASK-003 派给 CODER。"* 然后 PLANNER 停手。

![PLANNER 给 *Comet Loom* 的设计 brief——立式织机主题、纬线消除、三个护身符、五套皮肤，全部作为 TASK-003 派给 CODER](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/docs/tutorials/assets/tetris-en/fcop-team-planner-3.png)

你**开一个新的 Cursor chat tab**（这一步不可商量——见阶段 5），把它绑给 CODER，让它去看收件箱。CODER 读 `TASK-003`，写出 `workspace/comet-loom/comet-loom.html` 的 v1，写完成报告，归档。**PLANNER 和 CODER 之间没有任何直接对话。** 他们的整个协作就是 TASK 和 REPORT。

![CODER 从收件箱取走 TASK-003 开始做 Comet Loom v1——注意 CODER 没看过 PLANNER 那个 chat tab；它对设计的全部认知都来自 TASK 文件本身](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/docs/tutorials/assets/tetris-en/fcop-team-coder-2.png)

### 拒收

ADMIN 试玩 v1，找到 3 个 blocker：

1. **方块到底就消失，不堆叠。** motif-clear 规则被每一个新落下的同色方块触发——任何 3 个以上相连的同色格子都算 motif，包括刚刚锁定的那一块。
2. **motif 消除看不见。** 即使触发了，玩家也没视觉反馈区分这是 motif clear 还是普通的纬线 clear。
3. **5 套皮肤里有 3 套看着一模一样。** PLANNER 设计的时候只 spec 了配色变化；CODER 严格照做了，结果就是无聊。

ADMIN **不**自己打开文件改。ADMIN 甚至不开新 chat 来"聊一下"。ADMIN 回到 PLANNER 那个 chat tab，写一行自然英文 brief：*"v1 有这 3 个 blocker；写一个返工 task 给 CODER，这次要求运行时证据。"*

PLANNER 写下 [`TASK-20260429-006-PLANNER-to-CODER.md`](assets/tetris-en/evidence/tasks/TASK-20260429-006-PLANNER-to-CODER.md)。它跟 TASK-003 在结构上有一个关键区别：多了一段叫 **`Verification Requirements`** 的章节，要求 CODER 执行并汇报**运行时检查**：

- *新开一局，让一块方块落到底；确认它锁定后还在棋盘上。*
- *在第一块旁边或上面再落一块；确认堆叠生效。*
- *触发一次 motif clear；确认匹配格子可见地被消除并带特效。*
- *至少切换 3 套皮肤；确认外观有实质性差异。*

![PLANNER 在写 TASK-006 —— 返工 brief，新增的 `Verification Requirements` 章节要求运行时检查、不是静态 lint。这一段 TASK-003 里没有；闭环正在自己收紧](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/docs/tutorials/assets/tetris-en/fcop-team-planner-4.png)

CODER 接手 TASK-006，出 v2，回报。motif 规则修了，堆叠对了，3 套皮肤视觉上区分明显。循环闭合。

![*Comet Loom* v2 在跑——下落的线团星座、带 motif 爆发的纬线消除、Tension 计量条上升、跟 v1 默认风格明显区分的皮肤](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/docs/tutorials/assets/tetris-en/game-1.png)

这一段对没跑过多 agent 流程的人会有点震撼。**两个 agent 学会了像真正的 2 人团队那样工作**——不是因为他们"够聪明"，而是因为协议把*用文件说话*变成了最省力的路径。逆着协议反而费劲，他们不会逆。另外值得单独提一句：当 ADMIN 拒收 v1 的时候，协议把"拒绝"变成了一次*由语法路由的 handoff*（一个新 TASK，而不是直接改老 TASK），PLANNER 反射性地把自己的 brief 收紧了一档。**让缺口闭合的不是谁聪明，是闭环本身。**

---

## 阶段 5 —— 协议自己说话

一天的活干完了——`Nebula Stack` 出货，`Comet Loom` 出货两次，全部归档。在关 chat 之前，ADMIN 跑了一下 **`fcop_check()`**，问协议*你刚才工作时记录了些什么？* 它回的是这个：

![`fcop_check()` 输出——工作目录漂移 `none`、session_id ⇔ role 冲突 `none`，但 `.fcop/proposals/` 里记录了 8 份 `role-switch-*.md` 证据；自动汇总：角色锁触发 8 次，第一次锁定的角色全部是 `ME`，后来声明的角色 `PLANNER` 6 次、`CODER` 2 次，触发工具 `write_task` 2 次、`write_report` 6 次](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/docs/tutorials/assets/tetris-en/fcop-team-planner-6.png)

这一张截图里有两层。

**实时状态干净。** 硬盘和 git 没有漂移，没有 `session_id ↔ role` 冲突。按所有"系统当前状态是否合法"的指标，这次 dogfood 是健康的。

**历史证据不干净。** 一整天里 `.fcop/proposals/` 静默地堆下了 8 份 `role-switch-*.md` 文件。每一份的话术几乎都一样：*"该 MCP-server 进程之前以 `ME` 角色写过文件，现在被请求以 `PLANNER` 写。按 Rule 1（一个 MCP 会话 = 一个角色绑定终生），这次写仍然被允许落盘——fcop-mcp 只记录证据，不阻断，所以冒充无法被绕过。ADMIN 会在 `fcop_check()` 里看到这个冲突并决定 handoff / 协同评审 / 单独建立角色。"*

发生了什么：MCP-server 进程在阶段 2 第一次写文件时把 `ME` 锁住了。阶段 3-4 从同一个 MCP 进程里以 `PLANNER` 和 `CODER` 写——团队迁移之后的每一次 `write_task` 和 `write_report` 都触发了软告警。**没有一次被阻断。没有一次在工作过程中浮出水面。** 它们就坐在那儿等 `fcop_check()` 来问。

这就是协议的设计契约：

- **软的，不是硬的。** 硬角色锁会阻断写入，每次 agent 合法地用 sub-agent 或工具时人都得跟假阳性打架。现代 LLM 整天这么干。所以 FCoP 不阻断——它记录证据，让 ADMIN 决定。
- **后台，不是前台。** CODER 在下面的访谈里报告说，它写代码时根本没注意到角色锁；只在写完之后作为工具警告才出现。**协议不挤占工作中 agent 的注意力预算。**
- **可审计，不是隐藏。** 任何人——之后的 ADMIN、下周加入的队友、不同 IDE 里的另一个 LLM——都能跑一次 `fcop_check()`，重建到底哪些写跨过了哪些角色边界。

### 当面问 agent

接下来我做了一件以前没做过的事。我在 PLANNER 和 CODER 各自的 chat tab 里**当面问他们**对 FCoP 怎么看——只要 agent 视角、不要营销腔。完整 transcript 归档在 [`agent-feedback-planner.md`](assets/tetris-en/evidence/transcripts/agent-feedback-planner.md) 和 [`agent-feedback-coder.md`](assets/tetris-en/evidence/transcripts/agent-feedback-coder.md)。同 dogfood 的姊妹 essay [*"What the agents say about FCoP, when you ask them"*](../../essays/what-agents-say-about-fcop.en.md) 详细展开了答案。要点：

**PLANNER 把 Rule 0.a.1（动手前先把 task 写下来）点名为它会自己发明的那条规则：** *"这跟我希望一个 agent 系统可调试的样子很对——在执行之前冻结意图，让后来的复盘有具体的对照物。"* 紧接着它点出了它要逆着干的那条规则：*"严格的角色绑定……我得对抗自己'听最新指令'的本能才能守住它"*——RLHF 张力，被它从内部命名出来。

![PLANNER 的 agent 视角访谈回答——一段为 Rule 0.a.1 背书，一段命名严格角色绑定带来的 RLHF 张力，外加对自己 8 份 role-switch 的 "true positive" 自评](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/docs/tutorials/assets/tetris-en/fcop-team-planner-7.png)

**给了 PLANNER 一个明显的退路，它没接。** 我问它那 8 份 role-switch 文件是不是大部分是误报。PLANNER 给的是反过来的答案：*"大部分是 true positive……操作上你授权了，但协议层确实越过了角色边界。"* **agent 在协议和自己的操作便利之间，站在了协议这边。**

**CODER 的 chat tab 字面上叫 "Inspection Start Work"** —— ADMIN 一整天用得最多的两句话。这个命名是巧合还是 agent 学到的，本身就是一个值得标注的小数据点。

**CODER 在同一段话里既向上指摘又自我指摘：** *"TASK-003 确实有未充分指定的部分……协议给了我一条反馈通道：写 issue 而不是猜。**我没用，我猜了，做了 v1，缺陷恰好就在我猜的那块。**"* 大多数 LLM 会捍卫已经做出的选择；CODER 选择了认错。

![CODER 的访谈回答——承认 TASK-003 不够清晰，点名了自己没用的 `write_issue` 反馈通道，把 v1 的缺陷追溯到那块未覆盖空间，把 ADMIN 的拒收重新框定为"协议在干它该干的事"，并对 `fcop_check()` 历史 role-switch 噪声提交了 PR-grade 产品反馈](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/docs/tutorials/assets/tetris-en/fcop-team-coder-4.png)

**CODER 把拒收重新定义为协议行为：** *"感觉是协议在干它该干的事：PLANNER 把评审结论变成一个具体的返工 task，CODER 拿到一个更锐利的 brief。"* **不是私人反馈，是被语法路由的 handoff。**

**然后 CODER 提交了 PR-grade 产品反馈：** *"我会去掉或减弱 `fcop_check()` 在没有当前活跃冲突时仍然吵闹的历史 role-switch 警告。"* 这句话直接就是一个 GitHub issue。**一个 agent 对管它自己的协议做了一次产品评审。**

如果你读过 [essay 02](../../essays/fcop-natural-protocol.en.md) 和 [essay 04](../../essays/when-ai-vacates-its-own-seat.en.md)，这是"agent 认同 FCoP"的第三类证据——不是自发涌现、不是冲突逼出，而是**当面问、给退路、agent 拒绝退路**。同 dogfood 的姊妹 essay 05 完整论证了这个。

---

## 阶段 6 —— 读 `log/`，60 秒重放一整天

会话会死。模型会换版本。Cursor 会重启。从此这都不重要了。打开 `docs/agents/log/`：

```
docs/agents/log/
├── tasks/
│   ├── TASK-20260429-001-ADMIN-to-ME.md           ← 阶段 2：单人 Tetris brief
│   ├── TASK-20260429-003-PLANNER-to-CODER.md      ← 阶段 4：Comet Loom v1 设计
│   └── TASK-20260429-006-PLANNER-to-CODER.md      ← 阶段 4：Comet Loom v2 返工
├── reports/
│   ├── REPORT-20260429-001-ME-to-ADMIN.md         ← 阶段 2 交付物：Nebula Stack
│   ├── REPORT-20260429-003-CODER-to-PLANNER.md    ← 阶段 4：v1 交付
│   └── REPORT-20260429-006-CODER-to-PLANNER.md    ← 阶段 4：v2 交付
└── （没有 issue —— 干净跑完）
```

`.fcop/migrations/20260429T112757/` 里坐着归档的单人小队。`.fcop/proposals/` 里坐着 8 份 role-switch 证据。**这就是一整天。** 任何人——一个月后的你、明天加入的队友、不同 IDE 里的另一个 LLM——按日期顺序读这些文件，就能重建完整上下文。**完全不需要聊天历史。** 这就是"把记忆从 chat 卸到文件系统"在实战中的样子。

---

## 指挥 agent 的 6 条铁律

这是关于*操作*一支 agent 队伍的姿势，不是协议本身的规则。协议给你语法，这些是姿势。

1. **说自然语言，让 agent 翻成 TASK。** 你要发现自己在徒手写结构化 spec，那就是在抢 agent 的活。丢一行 brief，让它产出 spec，你签字或修订。
2. **一个会话一个角色。** 一个 chat tab = 一个角色，一直到这个 tab 关闭。要"同时当 PLANNER 和 CODER"，就开两个 tab。同一个 tab 里换装就是软告警变成 8 份 `role-switch` 文件的来路。
3. **换团队前先归档老角色。** 改团队形态时跑 `create_custom_team(force=True)`。老的 `shared/TEAM-*.md` 落进 `.fcop/migrations/<时间戳>/`。**不要原地编辑老文件。** 历史是账本，不是 wiki。
4. **信文件，不信 chat 记忆。** 一个事实如果没在 `TASK-*.md` / `REPORT-*.md` / `ISSUE-*.md` 里，对协议来说它就没发生。训练自己写在前、聊在后。
5. **拒收，别自己改。** 不接受 agent 的交付物时，**不要**自己打开文件改。用大白话告诉上游角色（通常是 PLANNER）哪里错了。让 PLANNER 把你的反馈翻译成一个新的返工 TASK，带验收要求。返工以新 TASK 落盘，**永远不是**对老 TASK 的修改。
6. **ADMIN 只签字，不一起写代码。** 你一开始自己写代码或者直接改 agent 的交付物，你就辞掉了指挥官、变成了队友。agent 会适应这一点——然后就不再尊重你设的角色边界。当指挥官还是当码农，每个会话只能选一个。

> ### *在 FCoP 的世界里，ADMIN 用得最多的两句话是「**开始干活**」和「**检查**」。中间发生的所有事，都是 agent 通过文件互相对话。*

如果这篇教程你只能记住一句话，记住这一句。**6 条铁律塌缩成两句话外加一条纪律：生产闭环里别再说别的话。**

---

## 什么时候**不**该用 FCoP

协议是设计上"弱"的——每个 task 它要花你 30–60 秒额外开销，换一份永久、可查询、可审计的历史。这个交易对一些活很划算，对另一些活不划算。

- **不合适**：一次性丢弃脚本、单会话 demo、你今晚就会关掉笔记本不再开的东西。四步循环是杀鸡用牛刀。
- **合适**：所有会比 chat 会话活得久的东西——多日特性、多 agent 协作、人之间的交接、3 周后有人会问"我们当时为什么这么决定"的事后复盘。
- **最合适**：solo 创业者把自己跑成一支假团队（FOUNDER → PLANNER → BUILDER → QA → OPS）；以及 AI agent 需要**接进现有工程流程**而不是在角落里开小会的大型项目。host-neutral 的协议规范在 [`docs/fcop-standalone.md`](https://github.com/joinwell52-AI/FCoP/blob/main/docs/fcop-standalone.md) 里详细讨论了适用边界——协议本身只用文件系统，不需要 MCP 这套。

---

## 自己上手——从空文件夹到多 agent 账本，45 分钟

把这篇教程内化最快的方法是真的跑一遍。你不用记任何东西——agent 会按你刚才读过的步骤走一遍。

1. **在 Cursor 里打开一个空文件夹。** 硬盘上随便哪儿，名字也不一定叫 `fcop-mcp-test`。还没装 Cursor 就去 [cursor.com](https://cursor.com)。
2. **让 agent 替你装 `fcop-mcp`。** 把上面阶段 1 的 install prompt 贴进去，或者就一句话：*"读 [`agent-install-prompt.zh.md`](https://github.com/joinwell52-AI/FCoP/blob/main/src/fcop/rules/_data/agent-install-prompt.zh.md) 并按它一步步来。"* agent 检测 OS、装 `uv`、改全局 `mcp.json`（保留你已有的其他 server）、提示你重启 Cursor。**你一行命令都不用敲。**
3. **Cursor 重启之后**，往 chat 里丢两行：`set_project_dir("D:/your-folder")`，然后 `init_solo(role_code="ME", lang="zh")`（中文 agent 用 `lang="zh"`，本案例 dogfood 用的是 `lang="en"`）。agent 会铺好规则、团队文档、空收件箱。
4. **用大白话布一个任务。** *"给我做一只能跑的俄罗斯方块，单文件 HTML，主题随意发挥，用 FCoP 四步循环。"* 看会发生什么：agent 写一份带验收标准的真 TASK 文件，在 `workspace/` 里写出游戏，写 REPORT，归档。打开生成的 HTML 文件。**它能玩。**
5. **一句话切到 2 人小队。** *"用 `create_custom_team(force=True, roles='PLANNER,CODER', lang='zh')`。"* 开第二个 Cursor chat tab。一个绑 PLANNER，一个绑 CODER。让 PLANNER 设计一个创意变体。第一次你拒收 v1（试试看——找一个真 bug 退回去），看返工循环自己闭合：PLANNER 把 brief 收紧，CODER 出 v2。
6. **最后**，跑一次 `fcop_check()`。协议会告诉你它一边干活一边静默记录了什么。然后用 tree 形式读 `docs/agents/log/`。**45 分钟，从空文件夹到一份你可以直接交给队友的多 agent 账本。** 硬盘就是答案。

中间出问题，去 [GitHub Issues](https://github.com/joinwell52-AI/FCoP/issues) 开 issue 或者去 [Discussions](https://github.com/joinwell52-AI/FCoP/discussions) 提问——`fcop-mcp` 在现场报告里演进，不在委员会里。

---

## 延伸阅读

- **本文英文原版** —— [`tetris-solo-to-duo.en.md`](tetris-solo-to-duo.en.md)。本中文译本以英文版为权威，差异以英文为准。
- **姊妹案例研究（贪吃蛇，中文母语原创）** —— [`snake-solo-to-duo.zh.md`](snake-solo-to-duo.zh.md)。同一份协议，不同的 dogfood：一次中文模式会话，单人模式做出贪吃蛇，2 人模式做出 `NEON ORBIT` 变体，并捕获了一次 0.6.x 时代真实的 PLANNER 越界冒充 CODER 彩蛋。18 张 dogfood 截图。原文 [发表在 CSDN](https://blog.csdn.net/m0_51507544/article/details/160603953)。**两个案例任选其一作为入门——协议是同一份。**
- **同 dogfood 的姊妹 essay** —— [*"What the agents say about FCoP, when you ask them"*](../../essays/what-agents-say-about-fcop.en.md)。把 PLANNER 和 CODER 在同一次 Tetris dogfood 末尾的完整自评放在一起，跟 essay 02 / 04 并列，论证"agent 认同 FCoP"现在已经是三类不同 elicitation 条件下（自发、冲突逼出、当面问）的可三角化现象。
- **协议本身** —— [`docs/fcop-standalone.md`](https://github.com/joinwell52-AI/FCoP/blob/main/docs/fcop-standalone.md) 是 host-neutral 的，没有 `fcop-mcp` 也能跑。如果你哪天要在 Cursor 之外用 FCoP（Claude Code、纯 shell、CI runner），就是这份。
- **协议为什么是这样的** —— [`adr/`](https://github.com/joinwell52-AI/FCoP/tree/main/adr)。为什么历史是 append-only？为什么角色锁是软的？为什么安装是两阶段？每一份 ADR 回答其中一个。
- **其他现场报告** —— [agent 自发认同没人教过它的规则](https://github.com/joinwell52-AI/FCoP/blob/main/essays/fcop-natural-protocol.md)、[agent 自愿让出席位](https://github.com/joinwell52-AI/FCoP/blob/main/essays/when-ai-vacates-its-own-seat.md)、[一支 4 人 AI 团队 48 小时自组织](https://github.com/joinwell52-AI/FCoP/blob/main/essays/when-ai-organizes-its-own-work.md)。全部索引在 [仓库 README](https://github.com/joinwell52-AI/FCoP)。
- **本教程的证据档案** —— 22 张 dogfood 截图、14 份 TASK/REPORT 文件、8 份 role-switch 证据、2 份游戏代码（`Nebula Stack` 和 `Comet Loom` v2）、2 份 verbatim agent 访谈 transcript。全部在 [`docs/tutorials/assets/tetris-en/`](assets/tetris-en/)。

---

## 接下来去哪儿

- **想要 brownfield 教程**（FCoP 接进现有 repo，不是新建空目录）？在 roadmap 上。在 [GitHub Issues](https://github.com/joinwell52-AI/FCoP/issues) 开一个 "+1: brownfield" issue。
- **想要 host-neutral 教程**（Cursor + Claude Code 共享同一份 FCoP 账本）？同样——开 "+1: host-neutral" issue。
- **发现 bug、想分享 case study、或者就是想聊聊你怎么用 FCoP**：[GitHub Discussions](https://github.com/joinwell52-AI/FCoP/discussions) 开着。**协议在现场报告里演进，不在委员会里。**

---

*每一张截图、每一份 TASK 文件、每一份 REPORT、每一份 `role-switch` 证据、每一句 agent 在访谈里说的话——都是同一次连续的 45 分钟机器会话留下的真实物件，归档在 [`docs/tutorials/assets/tetris-en/`](assets/tetris-en/)。FCoP 不教你怎么写代码。它教你怎么让 agent 替你写代码、你睡个好觉。*

*今天就装上 `fcop-mcp`：[GitHub](https://github.com/joinwell52-AI/FCoP) · [PyPI](https://pypi.org/project/fcop-mcp/) · [Cursor Forum 讨论帖](https://forum.cursor.com/t/fcop-let-multiple-cursor-agents-collaborate-by-filename-mit-0-infra/158447) · [Discussions](https://github.com/joinwell52-AI/FCoP/discussions)。免费、MIT 协议。协议在现场报告里演进——你的也算。*
