<p align="center">
  <img src="assets/fcop-logo-256.png" alt="FCoP Logo" width="180" />
</p>

<h1 align="center">FCoP — 文件驱动的 Agent 协作协议</h1>

<p align="center">
  <em>多 Agent 协作中的<strong>行为治理协议层</strong>——规范 Agent 如何报告行为、审阅结果并在受治理的能力边界内运作。</em><br/>
  <strong>核心不变量：<code>Filename as Protocol</code>（文件名即协议）·文件夹就是消息总线</strong>
</p>

<p align="center">
  <strong><a href="https://joinwell52-ai.github.io/FCoP/">🌐 项目主页</a></strong> ·
  <a href="README.md">English</a> ·
  <a href="docs/getting-started.md">上手 FCoP</a> ·
  <a href="src/fcop/rules/_data/agent-install-prompt.zh.md"><strong>👉 让 AI 安装！</strong></a> ·
  <a href="src/fcop/rules/_data/agent-bringup-prompt.zh.md"><strong>👉 让 AI 起项目！</strong></a> ·
  <a href="docs/mcp-tools.md"><strong>MCP 工具清单（45 个）</strong></a> ·
  <a href="essays/when-ai-organizes-its-own-work.md">现场报告</a> ·
  <a href="essays/fcop-natural-protocol.md">自然协议</a> ·
  <a href="spec/fcop-3.0-spec.zh.md"><strong>3.0 规范（中文）</strong></a> ·
  <a href="adr/README.md">ADR 索引</a>
</p>

<p align="center">
  <a href="https://dev.to/joinwell52/we-replaced-our-multi-agent-middleware-with-a-folder-48-hours-later-the-ai-invented-6-42a9">
    <img src="https://img.shields.io/badge/DEV-%E9%95%BF%E6%96%87%E5%AE%A2%E6%A0%88-black?style=flat-square&logo=dev.to&logoColor=white" alt="DEV Community 长文" />
  </a>
  <a href="https://forum.cursor.com/t/fcop-let-multiple-cursor-agents-collaborate-by-filename-mit-0-infra/158447">
    <img src="https://img.shields.io/badge/Cursor%20%E8%AE%BA%E5%9D%9B-%E8%AE%A8%E8%AE%BA-0066FF?style=flat-square" alt="Cursor 社区论坛" />
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="MIT License" />
  </a>
  <a href="CHANGELOG.md">
    <img src="https://img.shields.io/badge/%E5%8F%91%E5%B8%83-3.2.2-brightgreen?style=flat-square" alt="3.2.3" />
  </a>
  <a href="spec/fcop-3.0-spec.zh.md">
    <img src="https://img.shields.io/badge/%E8%A7%84%E8%8C%83-FCoP%203.0-orange?style=flat-square" alt="FCoP 3.0 规范" />
  </a>
  <a href="https://registry.modelcontextprotocol.io/v0/servers?search=io.github.joinwell52-AI%2Ffcop">
    <img src="https://img.shields.io/badge/MCP%20%E6%B3%A8%E5%86%8C%E8%A1%A8-io.github.joinwell52--AI%2Ffcop-8A2BE2?style=flat-square" alt="官方 MCP 注册表:io.github.joinwell52-AI/fcop" />
  </a>
  <a href="https://doi.org/10.5281/zenodo.19886036">
    <img src="https://zenodo.org/badge/DOI/10.5281/zenodo.19886036.svg" alt="DOI 10.5281/zenodo.19886036" />
  </a>
</p>

---

## 🆕 FCoP 3.0 已发布——*文件即协议；位置定义状态；事件记录历史。*

<p align="center">
  <a href="spec/fcop-3.0-spec.zh.md">
    <img src="assets/fcop-3.0-architecture.zh.png" alt="FCoP 3.0 · 体系结构全景图——文件即协议；位置定义状态；事件记录历史。" width="900" />
  </a>
</p>

> **FCoP 3.0** 是协议的第一次**语义封板**。状态住进文件系统本身（`_lifecycle/{inbox,active,review,done,archive}/`），事件以只追加方式住在文件内部，而 *custody / ownership / scheduling / runtime* 被显式划到**协议之外**（Boundary Charter）。
>
> 从 2.x 升级请运行 `python -m fcop migrate --to-v3`。

| 文档 | 用途 |
|---|---|
| [`spec/fcop-3.0-spec.zh.md`](spec/fcop-3.0-spec.zh.md) · [en](spec/fcop-3.0-spec.md) | 中文单页正式规范 |
| [`spec/fcop-3.0-rfc.zh.md`](spec/fcop-3.0-rfc.zh.md) · [en](spec/fcop-3.0-rfc.md) | RFC 中文平行版 |
| [`docs/MIGRATION-3.0.zh.md`](docs/MIGRATION-3.0.zh.md) · [en](docs/MIGRATION-3.0.md) | 2.x → 3.0 迁移指南 |
| [`CHANGELOG.md` `[3.0.0]`](CHANGELOG.md) | 完整 release notes |
| [`essays/the-day-we-almost-added-custody.md`](essays/the-day-we-almost-added-custody.md) · [en](essays/the-day-we-almost-added-custody.en.md) | 定义 3.0 的那次决策 |

---

## FCoP 在技术栈中的位置

FCoP 是多 Agent 协作中的**行为治理协议层**——规范 Agent 如何报告行为、审阅结果并在受治理的能力边界内运作。

```
应用层          CodeFlow / Cursor / Claude Desktop       ← 业务产品 / Agent 应用
宿主适配层      fcop-mcp / fcop-cli / @fcop/claude       ← 集成适配器 / 宿主桥接层
★ FCoP 协议层 ★ Agent 协作 / 行为报告 / Review /         ← FCoP 的核心职责
                Capability Governance / 事件语义 /
                失败边界 / 审计能力
参考实现层      fcop（Python Library）                   ← FCoP 协议的参考实现
执行基底层      LLM APIs / MCP 工具 / 文件系统 /         ← 执行环境（FCoP 不拥有）
                进程管理 / 操作系统
```

> **FCoP 治理 Agent 行为，而非执行运行时。** —— [ADR-0029](adr/ADR-0029-fcop-behavior-governance-charter.md)

v1.0 将七大核心概念——**Agent、Encoding、IPC、Event、Failure、Boundary、Audit**——的最小语义契约正式固化为稳定标准。spec 固化、encoding 留白：*IPC Surface*（TASK / REPORT / ISSUE / REVIEW）强类型；*Open Knowledge Surface*（`shared/` + `{ALL-CAPS-PREFIX}-{slug}.md`）词表完全开放，让 agent 自由发明——见 [ADR-0021](adr/ADR-0021-encoding-abstraction.md)。

→ **从这里开始**：[`docs/getting-started.md`](docs/getting-started.md) · [`docs/getting-started.en.md`](docs/getting-started.en.md)

---

## 一句话说清楚

主流的多 Agent 框架要靠消息队列、数据库、自研 RPC 中间件。FCoP 全部扔掉，只留**文件系统**：

- **目录就是状态。**`tasks/` / `reports/` / `issues/` / `log/`，文件从一个目录 `rename` 到另一个就是状态流转。
- **文件名就是路由。**`TASK-20260418-001-PM-to-DEV.md` 一眼看得出发件人、收件人、类型、流水号。
- **内容就是负载。**Markdown + 一点点 YAML frontmatter，Agent 和人读写的是同一份东西。
- **唯一的同步原语是 `os.rename()`。**POSIX 在同一挂载点内保证它原子——不需要锁、不需要 broker、不需要共识算法。

就这些。没有数据库，没有消息队列，没有常驻守护进程。整个系统状态 `ls` 就能看完，整段协作历史 `git log` 就能回放。

> 如果说 TCP 是"字节跑在线缆上"，**FCoP 就是"任务跑在文件夹里"。**

> 在工程上，就是用**可序列化、可版本化的协作面**，换走了对**专属、沉重基础设施**的依赖。

## 为什么值得一看

因为**看得见的 Agent，才管得住。**

我们用一支 4 人 AI 团队（PM / DEV / QA / OPS）跑了 48 小时，Agent 们**自发发明了 6 种我们从没写进规范的协作模式**——全体广播、角色槽位、共享文档、子任务批次、自解释 README、可追溯性 frontmatter。每一种新模式都表现为**新文件名**——我们一行代码都没改。

后来又出现了更意外的一幕：一个**单独**的 agent，在一个**与任何当时已打开的项目工作区都无关**的本地目录里（例如生成一段 AI 音乐视频），**自发**把自己拆成 PM / DEV / ADMIN 三个角色、给自己写了四份 FCoP 格式的公文，还**升华**了我那些分散在 7 个文件里的技术规定，浓缩成一句我根本没写过的原则性箴言。

这两段故事都整理成了现场报告，见下面的文章索引。

## 现场报告 · Essays

| # | 标题 | 版本 | 一句话 |
|---|---|---|---|
| 01 | **当 AI 自己整理工作** | [GitHub 中文](essays/when-ai-organizes-its-own-work.md) · [CSDN](https://blog.csdn.net/m0_51507544/article/details/160344932) · [English](essays/when-ai-organizes-its-own-work.en.md) | 一支 4 人 AI 团队（PM / DEV / QA / OPS），48 小时，只给一个文件夹——结果自发涌现出 6 种我们从没写进规范的协作模式。 |
| 02 | **一个无法完全解释的现象:AI 不止服从规则,它认同规则** | [GitHub 中文](essays/fcop-natural-protocol.md) · [GitHub English](essays/fcop-natural-protocol.en.md) · [CSDN 中文](https://blog.csdn.net/m0_51507544/article/details/160345043) · [Dev.to](https://dev.to/joinwell52/an-unexplainable-thing-i-saw-the-agent-didnt-just-comply-with-rules-it-endorsed-them-5ecd) · [Cursor Forum](https://forum.cursor.com/t/i-asked-cursor-to-make-a-video-it-wrote-itself-4-protocol-memos-field-report-on-rule-internalization/158524) | 一个 agent 在**完全无关**的任务里，自发把自己拆成 4 个 FCoP 角色，还**升华**了我散在 7 个文件里的技术规定，浓缩成一条我根本没写过的原则。附[完整证据档案](essays/fcop-natural-protocol-evidence/)（4 张截图 + 4 份公文 + 原始 JSONL 转录）。 |
| 03 | **自然协议为什么站得住——FCoP 从 TMPA 中抽出来的那条伦理** | [GitHub 中文](essays/fcop-tmpa-lineage.md) · [GitHub English](essays/fcop-tmpa-lineage.en.md) | 02 的姊妹篇。那一篇讲"这件事发生了"，这一篇讲"它为什么站得住"：FCoP 其实是从 **TMPA**（一份多 AI 架构规范，核心立意是用纯文本时序替代传统分布式协调）里抽出来的子集；agent 升华出的那句话，是 TMPA 伦理层"多角色审核是 AI 伦理强制"的最小化重发现。 |
| 04 | **让 agent 说"不"，是 LLM 最难做的事——FCoP 给了它语法** | [GitHub 中文](essays/when-ai-vacates-its-own-seat.md) · [GitHub English](essays/when-ai-vacates-its-own-seat.en.md) · [现场证据档案](essays/when-ai-vacates-its-own-seat-evidence/INDEX.md) · [CSDN 中文](https://blog.csdn.net/m0_51507544/article/details/160513899) · [Dev.to](https://dev.to/joinwell52/saying-no-is-the-hardest-thing-for-an-llm-fcop-gives-it-grammar-3ccd) · [Cursor Forum](https://forum.cursor.com/t/saying-no-is-the-hardest-thing-for-an-llm-fcop-gives-it-grammar/159037) | 同一台电脑、两个 Cursor 会话、两个 GPT-5 小版本（5.4 与 5.5）：原 PM 在我说"找了临时 PM"后主动让出席位回到 UNBOUND，新 PM.TEMP 用「frontmatter 降级 + 正文 `说明:` 一行」走完了协议没写的那条路。我原本以为会冲突，结果没有——agent 自己把规则补全了。附 15 张截图 + 2 份完整 JSONL 转录。 |
| 05 | **教程：solo 单 agent 转 2 人团队——FCoP-MCP 让 AI 团队有纪律**（两个并列案例） | 中文母语原创（贪吃蛇案例）: [`snake-solo-to-duo.zh.md`](docs/tutorials/snake-solo-to-duo.zh.md) · [CSDN](https://blog.csdn.net/m0_51507544/article/details/160603953) · English (Tetris case): [`tetris-solo-to-duo.en.md`](docs/tutorials/tetris-solo-to-duo.en.md) · [Dev.to](https://dev.to/joinwell52/free-open-source-multi-agent-hands-on-how-to-command-agents-fcop-mcp-brings-discipline-to-1j3j) · [Cursor Forum](https://forum.cursor.com/t/free-open-source-multi-agent-hands-on-how-to-command-agents-fcop-mcp-brings-discipline-to-ai-teams/159329) · 中文译本（俄罗斯方块案例）: [`tetris-solo-to-duo.zh.md`](docs/tutorials/tetris-solo-to-duo.zh.md) | 唯一一篇**教程性质**的文章，以**两个并列案例**形式发布——**协议相同，案例游戏与现场彩蛋不同**。两个案例都是 45 分钟跟真实 dogfood 走一遍：让 AI 替你装 `fcop-mcp`，solo 写一只能跑的小游戏，一句话切 2 人团队后 PLANNER 设计 + CODER 实现创意变体，最后读盘看完整账本。**中文案例**用贪吃蛇 → 原创主题《星轨织者 NEON ORBIT》，附 18 张截图 + 一次真实的 PLANNER 越界冒充 CODER 彩蛋（0.6.x 时代的协议越界证据）。**英文案例**用俄罗斯方块 → 单人《Nebula Stack》→ 双人《Comet Loom》，多了一个真实的"评审 → 拒收 → 重做"循环（v1 被 ADMIN 试玩驳回，PLANNER 写 TASK-006 加 `Verification Requirements`，v2 通过）+ 当场访谈两个 agent "你怎么看 FCoP" 收到的诚实自评。两个案例共 22 张 dogfood 截图、14 份 TASK/REPORT、8 份 role-switch 静默证据、2 份游戏代码、2 份 verbatim agent 访谈 transcript——全部归档在 [`docs/tutorials/assets/tetris-en/`](docs/tutorials/assets/tetris-en/)。 |
| 06 | **直接问 agent 它怎么看 FCoP——它说出了我们没让它说的话** | [GitHub 中文](essays/what-agents-say-about-fcop.md) · [GitHub English](essays/what-agents-say-about-fcop.en.md) · [现场证据（俄罗斯方块案例 dogfood）](docs/tutorials/assets/tetris-en/) · [CSDN 中文](https://blog.csdn.net/m0_51507544/article/details/160636177) · [Dev.to](https://dev.to/joinwell52/what-the-agents-say-about-fcop-when-you-ask-them-3ajk) · [Cursor Forum](https://forum.cursor.com/t/what-the-agents-say-about-fcop-when-you-ask-them-two-field-interviews-at-the-end-of-an-english-dogfood/159368) | 第三类"agent 反向认同 FCoP"的证据——在 [essay 02](essays/fcop-natural-protocol.md)（**自发触发，无关任务**）和 [essay 04](essays/when-ai-vacates-its-own-seat.md)（**被冲突逼出来**）之后，这次的触发条件是**被直接问**。一次英文俄罗斯方块 dogfood 收尾时（教程行 05 的伴随 essay），我分别在两个会话里问 PLANNER 和 CODER 同一类问题——agent 视角的老实话，无营销腔。PLANNER 把 "follow latest instruction" 这个 RLHF 训出来的本能命名为自己为了守住 FCoP 角色锁需要"对抗"的那一面，把它名下产生的 8 份 `role-switch` 评定为**真阳性**而不是误报。CODER 承认 TASK-003 有规格漏洞 + **协议本来给了它一条 pushback 路径（`write_issue`）它没用**——v1 缺陷正好长在那块没覆盖的空白上——并给出 PR 级别的协议产品反馈。三种触发条件，同一个现象：**只要给空间，agent 就会反过来认同 FCoP**。还有一个 dogfood 顺带产出的小观察值得留底——整整 45 分钟，ADMIN 说得最多的两句话是 **"Start work."** 和 **"Inspection."** |
| 07 | **当 agent 从自己的残骸中学习** | [GitHub 中文](essays/when-agents-learn-from-their-own-wreckage.md) | codeflow 项目一日 14 个 agent 涌现现场报告（2026-05-12）：USER HOME 全局污染 / GATE 描述自命中 / `supersedes:` 字段现场发明——以及协议如何在零次崩溃的情况下，以小时级速度将它们全部反向吸收。 |
| 08 | **协议为什么短，历史为什么长** | [GitHub 中文](essays/why-the-protocol-stays-short.md) | 一份给协议维护者的设计哲学答案："这样的涌现会不会没有止境？"——短答：会收敛但不会停。四类涌现的处理路径、三条结构力学为何能让协议骨架不被涌现压垮，以及"协议短是为了让历史能无限长"的底层逻辑。 |
| 09 | **当 validator 撞向自己的镜像** | [GitHub 中文](essays/gate-design-pitfalls-case-studies.md) | 从 codeflow OPS I-14 看 validator-validates-itself 反模式：GATE 在检查 staged diff 时命中了 GATE 描述本身，几分钟后被 OPS 自纠——这一类陷阱的系统性解剖与"语义化实证"根治姿势，以及它如何成为 `fcop-protocol.mdc §GATE Design Pitfalls` 的源头案例。 |
| 10 | **一行 frontmatter 的旅程** | [GitHub 中文](essays/the-supersedes-field-story.md) | `supersedes:` 字段从一次协议两难现场发明到 `ipc-envelope.schema.json` 正式字段的两小时旅程：Rule 5（append-only）+ Rule 6（reciprocity）+ Rule 0.c（truthful）三条规则同时成立时，agent 用一行 YAML 自己解了困局——这条路径展示 FCoP 涌现落地的最低成本姿势。 |
| 11 | **看，但不动手** | [GitHub 中文](essays/looking-without-touching.md) | FCoP 三层语义执行链科普：`fcop_audit()` 为什么"只看不改"——L1 检测 / L2 解释 / L3 文档三层把"看见"和"动手"切开，产出 `INSPECTION.md`（建议非命令），执行权留给人。`adr/FCoP-semantic-execution-chain.md` 的科普版。 |
| 12 | **五大 AI 模型眼中的 FCoP** | [GitHub 中文](essays/what-five-ai-models-say-about-fcop.md) · [GitHub English](essays/what-five-ai-models-say-about-fcop.en.md) | 把 FCoP 核心文档喂给 ChatGPT / Claude / DeepSeek / Grok / 豆包，只问一个问题："你是 agent，你怎么看这套协议？"——五种截然不同的内部视角（ChatGPT 谈身份合法性、Claude 谈诚实边界、DeepSeek 谈体面生存、Grok 做技术评审、豆包讲设计哲学），以及它们之间最有意思的分歧。 |
| 13 | **演化，反向吸收** | [GitHub 中文](essays/evolution-reverse-absorption.md) · [GitHub English](essays/evolution-reverse-absorption.en.md) | 协议哲学 2.0 视觉宣言：FCoP 从单张执行哲学图（"看，但不动手"）进入**两张图共同定义**时代——新增演化哲学图（7 步语义演化闭环）与配套 [ADR-0034](adr/ADR-0034-fcop-internal-external-document-convention.md)，把 4 层涌现模式 / 内外文档约定 / 反向吸收机制写入协议。essay 11 的孪生姊妹篇。 |
> 欢迎提交新的现场报告。如果你在自己的项目里用了 FCoP，遇到了意外（好或坏），欢迎开 issue 或对 `essays/` 提 PR。协议是在现场报告里演进的，不是在委员会里。

## 仓库结构

概览：根目录除**协议与文档**外，还有 **PyPI `fcop` 的源码**（`src/fcop/`）与**独立子项目 `fcop-mcp`**（`mcp/`），以及测试与发版/ADR 支撑目录。

```
FCoP/
├── src/fcop/                    # `fcop` 包：Project 等库 API；`rules/_data/` 内置 fcop-rules / fcop-protocol（init 时可选部署的母版）
├── mcp/                         # `fcop-mcp` 子项目（MCP 服务器，自有 pyproject）
├── tests/                       # `fcop` / `fcop-mcp` 的 pytest
├── spec/                        # 规范文件（参见 spec/README.md）
│   ├── fcop-3.0-spec.md         # ★ 英文权威规范（FCoP 3.0 canonical）
│   ├── fcop-3.0-spec.zh.md      # 中文平行版（informative）
│   ├── fcop-3.0-rfc.md / .zh.md # IETF 风格 RFC 版本
│   ├── schemas/                 # 8 JSON Schemas（机器可读）
│   └── archived/                # v1.0 / v1.1 / 0.7.x 早期 spec（已被取代，保留作历史）
├── docs/                        # 入门、迁移、发版记录、MCP 工具说明
│   └── getting-started.md      # ← 新用户从这里开始
├── adr/                         # 架构决策（ADR-0001..0022）
├── .github/workflows/           # CI
├── pyproject.toml               # 根 `fcop` 包与工具配置
├── essays/
│   ├── when-ai-organizes-its-own-work.md
│   ├── when-ai-organizes-its-own-work.en.md
│   ├── fcop-natural-protocol.md
│   ├── fcop-natural-protocol.en.md
│   ├── fcop-natural-protocol-evidence/
│   ├── fcop-tmpa-lineage.md
│   ├── fcop-tmpa-lineage.en.md
│   ├── when-ai-vacates-its-own-seat.md
│   ├── when-ai-vacates-its-own-seat.en.md
│   ├── when-ai-vacates-its-own-seat-evidence/
│   ├── what-agents-say-about-fcop.md
│   └── what-agents-say-about-fcop.en.md
├── examples/workspace-example/  # 最小参考工作区
├── integrations/windows-file-association/
├── assets/                      # Logo
├── LICENSE
└── README.md / README.zh.md
```

## 30 秒快速上手

FCoP 是「采纳」协议，不是装一个独立守护进程。当前版本的**规范侧**是成对的 **[总则 `fcop-rules.mdc`](src/fcop/rules/_data/fcop-rules.mdc)** 与 **[解释 `fcop-protocol.mdc`](src/fcop/rules/_data/fcop-protocol.mdc)**（部署到 **`.cursor/rules/`**）。`spec/codeflow-core.mdc` 仅为**防旧链接失效**的弃用占位，**勿**当正文规范使用。

**方式 A：用 `fcop` 库初始化（推荐）** — 一次写好 `fcop/` 目录与 `fcop.json`（库约定的协作根）：

```python
from fcop import Project
Project(".").init()  # 默认 dev-team；单人可改用 .init_solo()
```

**方式 B：不跑 Python、只让 Cursor 读规则** — 把上列两个 `.mdc` 从本仓拷进项目的 `.cursor/rules/`。目录若尚未存在，至少要有与库一致的五类桶：

```bash
mkdir -p fcop/{tasks,reports,issues,shared,log}
```

配好规则后，Agent 按总则/解释可知：认领发给自己的任务、按文件名写回报告、上报问题、不越权动他人文件。更完整的落盘与团队模板，见下节包与 [`examples/workspace-example/`](examples/workspace-example/)。

## Python SDK & MCP 服务器（可选）

协议可纯文件采纳；**若需要**在代码里读写 task/report/issue，或通过 MCP 暴露给 IDE，自 `0.6.0` 起 PyPI 上有两个包：

| 包 | 安装 | 用途 | 依赖 |
|---|---|---|---|
| [`fcop`](https://pypi.org/project/fcop/) | `pip install fcop` | 纯 Python 库。读写 task / report / issue。**零 MCP 依赖**。 | `pyyaml` |
| [`fcop-mcp`](https://pypi.org/project/fcop-mcp/) | `pip install fcop-mcp` | MCP 服务器。把库通过 stdio 暴露给 Cursor / Claude Desktop。 | `fcop>=1.1`、`fastmcp`、`websockets` |

**指针表**（一行一件事，不绑定版本号）：

| 想干啥 | 去这里 |
|---|---|
| 在 Cursor / Claude Desktop 装 `fcop-mcp`（分步、多平台、自检） | [`mcp/README.md`](mcp/README.md) |
| 不想自己改 JSON，让 agent 全程跑命令装 | [`agent-install-prompt.zh.md`](src/fcop/rules/_data/agent-install-prompt.zh.md) · [English](src/fcop/rules/_data/agent-install-prompt.en.md)（装好以后也是 MCP 资源 `fcop://prompt/install`） |
| 已在用 0.6.x，要升级（两包同环境一起升 + 协议规则文件刷新） | [`docs/upgrade-fcop-mcp.md`](docs/upgrade-fcop-mcp.md) |
| 浏览全部 45 个工具和 14 个资源（分类、何时调、参数要点） | [`docs/mcp-tools.md`](docs/mcp-tools.md) |
| 看每版到底改了什么、为什么改 | [`CHANGELOG.md`](CHANGELOG.md) 与 [`docs/releases/`](docs/releases/) |

**近期发版**（完整说明在 [`docs/releases/`](docs/releases/)）：

| 版本 | 一句话 |
|---|---|
| **3.2.2**（[CHANGELOG](CHANGELOG.md)） | **v3.2.2 — 深度历史归档 + 10 个新 MCP 工具（35 → 45）。** 新增 `history/YYYY-MM-DD/` 日期分片长期归档层；新工具：`create_task`、`archive_to_history`、`bulk_archive_to_history`、`list_history`、`get_history_stats`、`search_history`、`move_to_history`、`cleanup_history`、`export_history`、`import_from_history`。支持手动/定时把已完成任务-报告对移入 `history/`。`fcop` 与 `fcop-mcp` 双包 lockstep 对齐至 3.2.2。 |
| **3.0.2**（[CHANGELOG](CHANGELOG.md)） | **v3.0.2 — 初始化拓扑修复。** 关键 patch：3.0.0 / 3.0.1 的 `Project._apply_init` 只创建了 v2 老桶，跳过了 spec §1.1 强制要求的 v3 `_lifecycle/{inbox,active,review,done,archive}/` 五桶。3.0.2 让 fresh init 直接落 v3 拓扑（同时不再创建被 superseded 的 v2 `tasks/` / `log/`）；`core.events.scan_workspace` 与 `Project.role_occupancy()` 在 v3 项目下从 `_lifecycle/` 读取。新增 audit 扫描 `_scan_lifecycle_topology_compliance()`（D9）：P0 = 已初始化项目同时缺 `_lifecycle/` 和 v2 内容；P1 = 两套拓扑共存（建议 `migrate --to-v3`）。MCP 工具描述（`init_solo` / `init_project` / `create_custom_team`）同步更新。1209 测试全绿。SemVer patch：相对 3.0.1 无 API 表面改动——init 之前在做错事。 |
| **3.0.1**（[CHANGELOG](CHANGELOG.md)） | **v3.0.1 — 路径整合补丁。** 纯文档/元数据 patch，无代码逻辑变更：3.0.0 把 v1.0/v1.1 历史 spec 草稿移到 `spec/archived/` 后，修复散落在 `AGENTS.md` / `CLAUDE.md` / 打包 Cursor rules / MCP server docstring / 两份 JSON Schema `description` 中的失效链接，统一指向 `spec/archived/fcop-runtime-protocol-v1.0.{md,zh.md}`（并指针到当前 canonical `spec/fcop-3.0-spec.md`）。`fcop-mcp` 的 `fcop://spec` / `fcop://spec/en` docstring 同步修正为反映 wheel 实际打包内容（`fcop-spec-v1.1.{lang}.md`）。历史制品（TASK / REPORT / ADR / release notes / migration docs）按 ADR-0036"历史不重写"原则保留原文。1202 测试全绿。 |
| **3.0.0**（[CHANGELOG](CHANGELOG.md)） | **v3.0 — 协议级 MAJOR ·"文件夹即状态"纪元。** FCoP 协议本体的一次完整重写——canonical 双层（per [ADR-0040](adr/ADR-0040-canonical-one-liner-two-layer-convention.md)）：**Layer 1**「文件即协议；位置定义状态；事件记录历史」+ **Layer 2** 语义本体。新增 `_lifecycle/{inbox,active,review,done,archive}/` 五桶目录拓扑（**与 2.x 不兼容**，须 `fcop migrate --to-v3`）；三层规则集（State Layer Rule A/B/C · Event Layer Rule E/F/G · Boundary Charter）；7 条允许迁移表外不可（实现 MUST 拒绝）；write-then-rename 原子性模式（事件即迁移，迁移即事件）；ADR-0037 Custody Layer 在 RFC 评审中**未进 Accepted 即被作废**（custody 不构成协议层，以 NOTE 形式保留为衍生解释）。新增 [`spec/fcop-3.0-spec.md`](spec/fcop-3.0-spec.md) 单页 canonical + IETF 风格 RFC 平行版 + 中文平行版 + [`docs/MIGRATION-3.0.md`](docs/MIGRATION-3.0.md) 迁移指南。 |
| **2.0.2**（[CHANGELOG](CHANGELOG.md)） | **v2.0.2 — `fcop-mcp` 正式入驻[官方 MCP 注册表](https://registry.modelcontextprotocol.io/)**（`io.github.joinwell52-AI/fcop`）。由 Anthropic + GitHub + Microsoft 联合背书的官方目录收录,Claude Desktop / Cursor / PulseMCP 等所有 MCP 客户端均可一键发现并通过 `uvx fcop-mcp` 安装。双包 lockstep 版本号对齐(per ADR-0002):`fcop` 库代码与 v2.0.0 **完全一致**;本次跨版本是把 fcop-mcp@2.0.1 的 MCP-元数据 patch 合并进同日 release,并落地"发版+备份一条龙" SOP——`RULES-release-file-inventory.md`(12 类清单)、`RULES-mcp-registry-release.md`(三步升级路径)、以及 `joinwell52-AI/FCoP-backup` append-only 备份镜像。 |
| **2.0.0**（[CHANGELOG](CHANGELOG.md)） | **v2.0 — "两图对偶"哲学层主版本号跨越。** 执行面与 v1.x 完全一致（per ADR-0003 附加性），主版本号跨越是因为协议层首次同时承认**两张图**:**执行哲学的五层垂直栈**（v1.x 已稳定）*与* **FCoP Semantic Evolution Loop**（七节点闭环——涌现 → 观察 → 提案 → 评审 → 合并 → 部署 → 反射，v2.0 新固化）。新增 Rule 4.6（`fcop/internal/` vs `docs/` + `essays/` 软约定 + `internal-only` 声明语法 v1）、`Project.init(deploy_internal_template=...)` opt-in 参数、P3（建议级，非阻塞）巡查严重度档、以及 `fcop_audit` 内置豁免清单（`log/`/`_archive/`/`legacy-non-protocol/`，修复 codeflow 跨项目巡检暴露的三个上游 bug：ISSUE-008/009/010）。ADR-0034。 |
| **1.6.0**（[CHANGELOG](CHANGELOG.md)） | **v1.6 — Trailing-slug 文件名收编（ADR-0033）。** `TASK-20260512-025-PM-to-OPS-phase-a-fix-naming.md` 这类长文件名正式合规——把 codeflow 项目 22+ 例自发涌现写法吸收进文法。slug 不参与路由，只是人类可读标签。100% 向后兼容（既有 1057 个单测 0 回归）。 |
| **1.5.0**（[CHANGELOG](CHANGELOG.md)） | **v1.5 — 协议感知同步 + `RULE_DOC_DRIFT`。** 84 份角色/团队文档同步至 v1.4 协议面（REVIEW envelope / `risk_level` / `fcop_audit` / `supersedes:`）；新增 `Project._scan_outdated_role_docs()` 扫描方法和 `RULE_DOC_DRIFT`（P1）违规类型。 |
| **1.4.0**（[详细](docs/releases/1.4.0.md)） | **v1.4 — Write-side 显式绑定守门（P0 安全）+ `supersedes:` 字段。** 15 个 write-side MCP 工具在 cwd fallback 时直接 `WriteRefused`；Protected Path 拒绝列表（HOME / APPDATA / 驱动器根 / Unix 系统目录）；新增 `supersedes:` frontmatter 字段（4 种 envelope 通用）+ `## GATE Design Pitfalls` 节（`fcop_protocol_version 2.2.0`）。 |
| **1.3.0**（[详细](docs/releases/1.3.0.md)） | **v1.3 — 治理告警层 + 协议巡查编译器。** GAL（ADR-0031）：3 类漂移信号（S1/S3/S4）、FCoP-Rule-G1、2 个新告警工具（`fcop_list_alerts`、`fcop_create_alert`）。`fcop_audit`（ADR-0032）：三场景协议巡查编译器、6 种扫描方法、带 Execution Block 的 INSPECTION 报告。总计 35 个 MCP 工具。 |
| **1.2.1**（[详细](docs/releases/1.2.1.md)） | **v1.2 — Capability Governance 支柱。** `FCoPGovernanceMiddleware` 包装每次 MCP 工具调用：Skill 解析 → 风险标记（Safe / Sensitive / Critical）→ 追加写入 `fcop_events.jsonl` 审计日志。新增 2 个 MCP 工具（`list_governance_events`、`get_governance_summary`）。`fcop_check()` 新增治理事件摘要。`fcop` 与 `fcop-mcp` 同步对齐至 `1.2.1`（锁步发版）。ADR-0030-bis。 |
| **1.1.0**（[CHANGELOG](CHANGELOG.md)） | **v1.1 — Agent.layer 治理合约 + Task.risk_level + Review.needs_human + HumanApproval + Skill.tools[] 风险元数据。** 5 条新 ADR（0023–0027），4 个新 MCP 工具（`write_review`、`list_reviews`、`read_review`、`mark_human_approved`），`write_task` 新增 `risk_level` 参数，新增 `skill.schema.json`。完全向后兼容。 |
| **1.0.1** | spec 文件打包进 wheel（`get_spec()`）；`fcop://spec` MCP 资源；workspace 路径迁移 `docs/agents/` → `fcop/`；CI 全绿。 |
| **1.0.0** | 七大核心概念固化：Agent、Encoding、IPC、Event、Failure、Boundary、Audit。7 个 JSON Schema。见[发布说明](docs/releases/1.0.0.md)。 |
| **0.7.2**（[详细](docs/releases/0.7.2.md)） | 元数据 patch：修 `fcop-rules.mdc` frontmatter 错版本号。无协议变化、无 API 变化。 |

> **小心：PyPI 上有一个跟这里无关的 `fcop` 同名包。** 本仓两个包都从**本仓发**。如果 `pip install fcop` 之后 `from fcop import Project, Issue` 仍失败，多半是你装错了 distribution、或本机某个可编辑安装的工程把 `fcop` 名字抢走了。修法：干净 venv + 一并按 PyPI 重装两个包。验证命令在 [`mcp/README.md`](mcp/README.md)。

**库** —— 从任何 Python 脚本或 agent 里直接调：

```python
from fcop import Project

proj = Project(".")                              # 项目根；未 init 时无 fcop.json
proj.init()                                      # 建 tasks|reports|issues|shared|log/ 与 fcop.json
task = proj.write_task(sender="PM", recipient="DEV", priority="P1",
                       subject="加鉴权中间件", body="...",
                       risk_level="high")        # v1.1：触发 needs_human review gate
print(proj.list_tasks(recipient="DEV"))
```

**MCP 服务器** —— 写进 Cursor 的 `mcp.json` 或 Claude Desktop 的 `claude_desktop_config.json`：

```json
{
  "mcpServers": {
    "fcop": {
      "command": "uvx",
      "args": ["fcop-mcp"]
    }
  }
}
```

**不想自己改 JSON？** 让 agent 来。开一个能跑命令的新会话，把官方安装提示词
（[`agent-install-prompt.zh.md`](src/fcop/rules/_data/agent-install-prompt.zh.md)
· [English](src/fcop/rules/_data/agent-install-prompt.en.md)）整段贴过去——
agent 会识别系统、装 `uv`、改 `mcp.json`（**保留**已有 server）、提醒重启。
装好以后这段提示词在 MCP 资源 `fcop://prompt/install` 也能直接读到。提示
词里**明令禁止** agent 装完顺手 `init_project`——初始化是 ADMIN 的三选一
（solo / 预设团队 / 自定义），不是 agent 的默认值。

稳定性承诺：**整个 `0.6.x` 小版本周期内只加不改**，详见 [`adr/ADR-0003-stability-charter.md`](adr/ADR-0003-stability-charter.md)。

> **从 0.7.x 升级到 v1.0？** workspace 默认目录从 `docs/agents/` 迁到顶层 `fcop/`（per [ADR-0022](adr/ADR-0022-workspace-directory-convention.md)）。一键 git-aware 迁移：`fcop migrate-workspace --apply`；不想动盘传 `Project(workspace_dir="docs/agents")` 即可永久锁定老 layout。完整 walkthrough（含 4 个新抽象 REVIEW / Failure / Boundary / Event + JSON Schema 集成）见 [`docs/MIGRATION-1.0.md`](docs/MIGRATION-1.0.md)。
>
> **从 0.5.x 升级？** MCP 服务器已从 `fcop` 包搬到 `fcop-mcp`——把 `mcp.json` 里的命令改成 `uvx fcop-mcp`。完整迁移指引见 [`docs/MIGRATION-0.6.md`](docs/MIGRATION-0.6.md)，本次发版档案见 [`docs/releases/0.6.0.md`](docs/releases/0.6.0.md)。

## 如何阅读 FCoP 文档

## 如何阅读 FCoP 文档

| 你的目标 | 从这里开始 |
|---|---|
| **FCoP 新手** — 45 分钟上手实战 | [`docs/getting-started.md`](docs/getting-started.md) |
| **从 0.7.x 升级** — workspace 迁移 + 4 个新概念 | [`docs/MIGRATION-1.0.md`](docs/MIGRATION-1.0.md) |
| **从 1.0/1.1 升级到 1.2** — Capability Governance + 锁步发版 | [`docs/MIGRATION-1.1.md`](docs/MIGRATION-1.1.md) · [CHANGELOG](CHANGELOG.md) |
| **理解协议契约** — 合规实现 MUST 做什么 | [`spec/fcop-3.0-spec.zh.md`](spec/fcop-3.0-spec.zh.md) — 单页正式规范 v3.0（中文）。v1.0/v1.1 早期 spec 草稿在 `spec/` 中保留作为历史参考。 |
| **v1.2 Capability Governance** — FCoPGovernanceMiddleware、风险标记、审计日志 | [CHANGELOG](CHANGELOG.md) · ADR-0030-bis |
| **v1.1 新字段** — risk_level、needs_human、human_approval、skill tools | [CHANGELOG](CHANGELOG.md) · ADR-0023..0027 |
| **理解决策背后的原因** — 每个设计的考量 | [`adr/`](adr/) — 从 [ADR-0029](adr/ADR-0029-fcop-behavior-governance-charter.md) 开始 |
| **全部 45 个 MCP 工具与 14 个资源** | [`docs/mcp-tools.md`](docs/mcp-tools.md) |
| **发布说明** — 完整变更日志 | [`CHANGELOG.md`](CHANGELOG.md) |
| **完整文档地图** — 每个文件的角色 | [`adr/README.md`](adr/README.md)（ADR 索引）+ [`spec/fcop-3.0-spec.zh.md`](spec/fcop-3.0-spec.zh.md) §11（引用材料）|

---

## 设计原则

1. **文件名是唯一真理。**目录 + 文件名决定状态，frontmatter 只是冗余元数据。
2. **原子性来自 `rename()`**。没有别的——不需要锁，不需要事务。
3. **人机同构。**`cat` 能读的就是 Agent 能解析的，没有调试模式、没有管理后台。
4. **身份决定路径。**文件名里的角色标识本身就是权限模型——身份不匹配，Agent 连文件都动不了。
5. **零基础设施。**只要有文件系统就有 FCoP。笔记本能跑，集群能跑，跨机通过 `rsync` 就能跑。

## 参考实现

两套官方参考实现，均为 MIT 许可：

1. **`fcop` / `fcop-mcp`** —— 协议的 Python 库 + MCP 服务器。源码在本仓库 [`src/fcop/`](src/fcop/) 和 [`mcp/src/fcop_mcp/`](mcp/src/fcop_mcp/)，通过 PyPI 分发（见上一节）。
2. **历史 URL 占位**：`spec/codeflow-core.mdc` 仅防旧链接失效，**无正文**；**唯一权威**仍是 `src/fcop/rules/_data/fcop-rules.mdc` + `fcop-protocol.mdc`（文件名含历史字样而已）。

## 状态与版本

- **当前发布**：`v3.2.2`（2026-05-22）——**初始化拓扑修复。** 关键 patch：3.0.0 / 3.0.1 的 `Project._apply_init` 只创建了 v2 老桶，跳过了 spec §1.1 强制要求的 v3 `_lifecycle/{inbox,active,review,done,archive}/` 五桶——所有在那两版上 fresh init 的项目都是**生而不合规**的。3.0.2 让 fresh init 直接落 v3 拓扑（同时不再创建被 superseded 的 v2 `tasks/` / `log/`）；`core.events.scan_workspace` 与 `Project.role_occupancy()` 在 v3 项目下从 `_lifecycle/` 读取。新增 audit 扫描 `_scan_lifecycle_topology_compliance()`（D9）：P0 = 已初始化项目同时缺 `_lifecycle/` 和 v2 内容；P1 = 两套拓扑共存（建议 `migrate --to-v3`）。MCP 工具描述（`init_solo` / `init_project` / `create_custom_team`）同步更新。1209 测试全绿。SemVer patch：无 API 表面改动——init 之前在做错事。前置 **v3.0.1**（2026-05-21）—— 路径整合补丁（纯文档）。前置 **v3.0.0**（2026-05-21）—— **协议级 MAJOR ·"文件夹即状态"纪元**：FCoP 协议本体的一次完整重写——canonical 双层（per [ADR-0040](adr/ADR-0040-canonical-one-liner-two-layer-convention.md)）「文件即协议；位置定义状态；事件记录历史」+ 语义本体；新增 `_lifecycle/{inbox,active,review,done,archive}/` 五桶目录拓扑（**与 2.x 不兼容**，须 `fcop migrate --to-v3`）；三层规则集（State / Event / Boundary Charter）+ 7 条允许迁移表外不可 + write-then-rename 原子性；ADR-0037 Custody Layer 在 RFC 评审中**未进 Accepted 即被作废**。详见 [`spec/fcop-3.0-spec.md`](spec/fcop-3.0-spec.md) 与 [`docs/MIGRATION-3.0.md`](docs/MIGRATION-3.0.md)。早期发布：v2.0.2（fcop-mcp 入驻官方 MCP 注册表）、v2.0.0（两图对偶哲学主版本号跨越 + Rule 4.6 `fcop/internal/`）、v1.6（trailing-slug 文件名收编，ADR-0033）、v1.5（84 份协议感知同步）、v1.4（write-side 守门 + `supersedes:` 字段）、v1.3（GAL + `fcop_audit()` 巡查编译器）、v1.2.1（Capability Governance 支柱）、v1.1（Agent.layer + Task.risk_level + needs_human）、v1.0（七大核心概念 spec freeze）。详见 [CHANGELOG](CHANGELOG.md)。
- **规范性文件**：[`spec/fcop-3.0-spec.zh.md`](spec/fcop-3.0-spec.zh.md)（中文 v3.0）· [`spec/fcop-3.0-spec.md`](spec/fcop-3.0-spec.md)（英文权威 v3.0）· v1.0/v1.1 早期 spec 草稿在 `spec/` 中保留作为历史参考 · 机器可读契约见 [`spec/schemas/`](spec/schemas/)（8 个 Schema）
- **本仓内 Agent 规则（`.mdc`）**：[`src/fcop/rules/_data/fcop-rules.mdc`](src/fcop/rules/_data/fcop-rules.mdc) + [`fcop-protocol.mdc`](src/fcop/rules/_data/fcop-protocol.mdc)（`spec/codeflow-core.mdc` 仅为弃用占位）
- **变更记录**：[`CHANGELOG.md`](CHANGELOG.md)
- **研究快照**：[`research-snapshot-2026-04-29`](https://github.com/joinwell52-AI/FCoP/releases/tag/research-snapshot-2026-04-29) 已经归档到 Zenodo 并分配 DOI（详见下文 *如何引用*）。

## 如何引用

如果 FCoP 的协议、现场报告 essays、教程、或参考实现对你的研究、软件、写作有帮助，请引用 [Zenodo 研究快照](https://doi.org/10.5281/zenodo.19886036)：

- **DOI**：[`10.5281/zenodo.19886036`](https://doi.org/10.5281/zenodo.19886036)
- **快照 tag**：[`research-snapshot-2026-04-29`](https://github.com/joinwell52-AI/FCoP/releases/tag/research-snapshot-2026-04-29)（commit `7f59395`）
- **机器可读元数据**：[`CITATION.cff`](CITATION.cff)（GitHub 会从这个文件自动渲染一个 *Cite this repository* 按钮放在右栏）

```bibtex
@misc{fcop2026snapshot,
  author       = {Zhu, Wei},
  title        = {{FCoP}: A Filename-as-Protocol coordination layer for multi-agent {AI} development (Research Snapshot, April 2026)},
  month        = apr,
  year         = 2026,
  publisher    = {Zenodo},
  version      = {research-snapshot-2026-04-29},
  doi          = {10.5281/zenodo.19886036},
  url          = {https://doi.org/10.5281/zenodo.19886036}
}
```

如果引用单篇 essay 或教程，DOI 仍是同一个——在引用脚注里附上 essay 的文件名（如 `essays/what-agents-say-about-fcop.md`）和 snapshot 版本号即可定位到具体内容。

## 如何贡献

本仓库刻意保持**小而稳**。协议演进的依据是"真实场景里的报告"，不是"委员会投票"。最有价值的贡献是：

1. **现场报告。**把 FCoP 拉到你自己的 Agent 团队里跑一段，把"哪里坏了"、"Agent 自己发明了什么"、"涌现出哪些命名约定"开个 Issue。
2. **移植与 SDK。**Python / TypeScript / Go 的薄封装，负责解析文件名和跑 `rename()` 状态机。
3. **编辑器与 MCP 集成。**`.fcop` 文件的语法高亮、把这套文件夹 expose 给其他 Agent 运行时的 MCP 桥。

对规范本身的 PR，请链接到它要解决的具体问题。

## License

MIT — 详见 [LICENSE](LICENSE)。

## 致谢

FCoP 是在 **Cursor 等环境**里与多 Agent 实战协作时陆续涌现的。规范里不少约定**最初是 Agent 们自己写出来的**，我们只是把它们整理成册。详情见 [现场报告](essays/when-ai-organizes-its-own-work.md)。
