# 当 AI 自己整理工作

### 一场把多智能体协作"降维"到文件系统的田野实验 · 一份关于 **FCoP** 的实验报告

> When AI Organizes Its Own Work: A field study of emergent coordination after we replaced middleware with a file system.
> A report on **FCoP — File-based Coordination Protocol**.

**核心创新 / Core Innovation**：**文件名即协议 · Filename as Protocol**

**作者**：CodeFlow 团队 · 2026-04-19
**关键词**：Multi-agent, File-based protocol, Emergent coordination, FCoP, Human-Machine Isomorphism, Unix philosophy

---

## Abstract

We gave a small team of AI agents (four roles, one human admin) a 76-line Markdown rulebook, a shared folder, and almost nothing else. No message queue. No database. No WebSocket between agents. The "coordination runtime" is a Python loop that clicks Cursor's tabs every few seconds just to wake each agent up — it does not route, schedule or arbitrate anything.

Within **48 hours of first boot** on a freshly-installed PC, the agents produced 42 tasks, 22 reports, and 10 spontaneous "shared" documents (≈ 74 files total). More interestingly, they **invented six coordination patterns we had not specified**: broadcast addressing, anonymous role slots, subtask sub-folders, self-explaining READMEs, traceability fields, and a whole class of standing "dashboard / sprint / glossary" documents. None of these caused collisions. All of them were discoverable by simply listing a directory.

We call this protocol **FCoP — File-based Coordination Protocol**. Its single core innovation is a slogan: **"Filename as Protocol."** Directory name is *status*, filename is *routing*, file content is *payload*. Nothing else. The same physical folder is simultaneously a rigorous state machine for agents and a browsable directory tree for humans — a property we call **Human-Machine Isomorphism**. This asymmetric-yet-symmetric design is what kills the "black box anxiety" that plagues every other multi-agent stack.

This essay documents what those agents did, why a filesystem-only protocol survives it gracefully, and what that implies for anyone building multi-agent systems today. It is not a product announcement — it is a field report, and an invitation to steal the idea.

---

## TL;DR · FCoP 是什么？/ What is FCoP in 60 seconds

**FCoP = File-based Coordination Protocol**——一种让多个 AI agent 通过**文件系统**协作的极简协议。

**一句话**：*Filename as Protocol · 文件名即协议。*

**它长什么样 / How it looks**：

```
docs/agents/
├── tasks/     ← 待办任务 / pending tasks
├── reports/   ← 完成回执 / completion reports
├── issues/    ← 问题登记 / issues
├── shared/    ← 团队常驻文档 / standing docs (dashboards, glossary, …)
└── log/       ← 历史归档 / archives
```

**路由靠文件名 / Routing lives in the filename**：

```
TASK-{date}-{seq}-{sender}-to-{recipient}.md
    例：TASK-20260418-201-MARKETER-to-DEV.md
         ↑ 类型   ↑ 日期     ↑ 序号 ↑ 发件人  ↑ 收件人
```

每个 agent 只要 `glob "*-to-{我的角色}*.md"` 就能拿到自己的信箱。收件人支持四种写法：
`to-DEV`（单点）、`to-TEAM`（广播）、`to-DEV.D1`（具名槽位）、`to-assignee.D1`（匿名槽位）。

**它不要什么 / What FCoP does NOT need**：
数据库、消息队列、编排引擎、专用客户端、SDK、长连接——**都不要**。

**它要什么 / What it DOES need**：
一个共享目录 + 一份命名约定 + 每个 agent 认领自己的角色。**就这些。**

**为什么值得一看 / Why it matters**：

- **人机同构 (Human-Machine Isomorphism)**：人和 agent 读的是**同一份文件**。`ls` 一下就能知道系统在干嘛——不需要任何调试器。
- **身份决定路径**：角色写在文件名里，agent 物理上只能读/写自己名下的文件。约束提供秩序，内容层完全开放。
- **协议可进化**：我们实地观察到 48 小时内 AI 自发发明了 6 种新协作模式，且全部与现有协议兼容。
- **基建为零**：git 做版本审计、rsync 做跨机同步、Finder / 资源管理器做调试面板——现成的。

**想深读 / Want more?**

- 60 秒版（可外链）：[`fcop-primer.md`](../primer/fcop-primer.md)
- 成对规范（总则 + 解释）：[`fcop-rules.mdc`](../src/fcop/rules/_data/fcop-rules.mdc) · [`fcop-protocol.mdc`](../src/fcop/rules/_data/fcop-protocol.mdc)
- 本文：继续往下翻 ↓

> **关于样本 · A note on samples**：本文引用的 agent 原始文件片段**一字未改**——文件名、目录层级、frontmatter、表格、验收语都是 agent 当时实际写下来的。数据域（汽车品牌、网易云公开歌曲）本身就是公开信息，没有做任何脱敏。**唯一没做的事**是把整份 `codeflow-1` 样本目录打包公开——那个项目还在进行中，相关的工具代码、内部 room_key、设备 ID 不适合整份抛出。读者真正关心的"AI 发明了什么协作模式"，在本文 §5 里用代表性片段完整呈现了。

---

## 1. 一个近乎可笑的假设

2026 年，主流 AI 协作栈长这样：Agent × N → Message Bus × 1 → State Store × 1 → Orchestrator × 1 → Observability × 1。加起来至少五个 SaaS、两套 SDK、一个值班群。

我们想问一个更朴素的问题：

> **如果把多 agent 通信协议降维到"文件系统"这一层，会发生什么？**

没有队列、没有数据库、没有 webhook。**Agent 只能通过"在目录里写文件 / 读文件"跟其他 agent 说话。** 跟 1970 年代 Unix 管道一样笨，一样简陋，一样不"现代"。

这个假设不是为了复古，而是为了回答：

- 一个没有中央调度器的 agent 团队，会自己演化出协作结构吗？
- 协作结构能被人类一眼看懂吗？
- 如果 agent 发明了协议设计者没写的模式，**这是 bug 还是 feature**？

我们做了个最小可跑的实现叫 **CodeFlow**，写了 76 行 Markdown 规范叫 **FCoP（File-based Coordination Protocol）**，在一台**刚装完系统、还热乎着**的 PC 上开跑——结果 **48 小时之内**就把我们吓了一跳。

---

## 2. 起点：一份 76 行的规范

最初的规范简单到几乎没东西。核心只有三件事：

**① 共享目录结构**

```
docs/agents/
├── tasks/     ← 任务单
├── reports/   ← 完成回执
├── issues/    ← 问题登记
└── log/       ← 历史归档
```

**② 文件名即协议 · Filename as Protocol**

```
TASK-{date}-{seq}-{sender}-to-{recipient}.md
```

这是 FCoP 唯一的**核心创新**，其他所有规则都是这一条的衍生品：

- **目录名 = 状态（Status）**：文件在 `tasks/` 还是 `reports/`，状态一目了然
- **文件名 = 路由（Routing）**：sender、recipient、kind、seq 全写在名字里
- **文件内容 = 载荷（Payload）**：Markdown 正文 + YAML frontmatter

收件人要读自己的信箱？`glob "*-to-{我的角色}*.md"` 一行搞定。不需要解析任何 header、不需要查任何数据库——**文件名本身就是完整的可寻址表面**。

**③ 前言元数据（frontmatter）**

```yaml
---
protocol: agent_bridge
version: 1
kind: task
sender: PM
recipient: DEV
task_id: TASK-20260418-001
priority: P1
---
```

再加五条协作礼仪：只处理发给你的任务、完成后写 report、有问题写 issue、不改别人文件、归档由主控做。

**就这些。这就是 FCoP 协议的全部。** 没有状态机、没有 schema、没有事务——核心创新浓缩成一句话：**Filename as Protocol**。后面你看到的所有"AI 的发明"，全是从这一条规则长出来的衍生物。

---

## 3. 巡检器的秘密：它其实什么都没做

对 CodeFlow 最大的误解，是把 **Patrol Engine（巡检器）** 当成了中央调度。真相是：

> **巡检器只是每隔几秒钟，通过 Chrome DevTools Protocol 切一次 Cursor 的 agent tab，让那个 agent 醒来看一眼自己的信箱。**

就这样。

它不路由消息，不判断优先级，不做 schema 校验，不管事务，不管顺序。

为什么要这样？——因为 **Cursor 原生不支持 agent 之间通信**。每个 agent 各自住在一个会话里，彼此听不见对方。巡检器干的事更像"轮流敲门"：

- "DEV，醒一醒，看看 tasks 目录里是不是有你的新任务。"
- "QA，醒一醒，看看 reports 里是不是有你要回归的报告。"
- "MARKETER，到你了，去读一下 docs/agents 新东西。"

真正的协作逻辑 **全部**发生在 agent 自己阅读文件、写文件、命名文件的那一刻。巡检器只是让"每个 agent 都会定期醒来"这件事成立。

换句话说：**平台做了它力所能及的最小动作，把协议层让给了 agent 自己。**

---

## 4. 田野：`codeflow-1` 的 48 小时

2026-04-16 装完系统、同步完工具链；2026-04-17 开始让 agent 干活；两天之后——也就是我写这篇文章的时候——团队已经产出了上面提到的那一堆东西。

实验项目叫 `codeflow-1`，团队配置是"自媒体小队"：

| 角色 | 职责 |
|---|---|
| **MARKETER** | 主控 / PM / 总调度 |
| **RESEARCHER** | 调研与素材 |
| **DESIGNER** | 视觉与分镜 |
| **BUILDER** | 工程与脚本 |
| **ADMIN**（人类） | 提需求、拍板、验收 |

没有 DEV、QA、OPS——连角色名都是按项目自定义的。规范里没写过"MARKETER 该干什么"，它只知道自己名字叫 MARKETER，信箱是 `*-to-MARKETER*.md`。

两天之后，`docs/agents/` 真实目录长这样（节选，统计口径：tasks 42 个 + reports 22 个 + 常驻文档 10 个）：

```
docs/agents/
├── BUILDER.md  DESIGNER.md  MARKETER.md  RESEARCHER.md    ← 角色手册
├── codeflow.json                                           ← 团队配置
├── CURRENT-SPRINT-STATUS.md                                ← AI 自己发明
├── DASHBOARD-20260418.md                                   ← AI 自己发明
├── tasks/
│   ├── RULES-task-file-format.md                           ← AI 自己发明
│   ├── SPRINT-20260418-delivery-push.md                    ← AI 自己发明
│   ├── TERM-20260418-assignment-matrix.md                  ← AI 自己发明
│   ├── TASK-20260418-001-ADMIN-to-MARKETER.md
│   ├── TASK-20260418-007-MARKETER-team-bulk-data.md        ← AI 自己发明 "team" 广播
│   ├── TASK-20260418-022-MARKETER-self-ADMIN018.md         ← AI 自己发明 "self" 自记
│   ├── …共 26 个顶层任务…
│   └── individual/                                         ← AI 自己开的子目录
│       ├── README.md
│       ├── INDIVIDUAL-TASK-INDEX.md
│       ├── TASK-20260418-201-MARKETER-to-assignee-D1.md    ← AI 自己发明 "assignee-槽位"
│       ├── TASK-20260418-202-…-D2.md
│       ├── …共 11 个单人任务…
│       └── TASK-20260418-211-MARKETER-to-assignee-P1.md
├── reports/   …对应的回执…
├── issues/    log/
```

其中被 `← AI 自己发明` 标注的东西，**全部不在原始 76 行规范里**。

我们来看它发明了什么。

---

## 5. AI 发明的六种协作语法

### 5.1 广播地址 `to-TEAM`

规范里写的是 `to-{recipient}`，recipient 默认是单个角色。但某天 MARKETER 需要让"整个团队"都看到一份共同的背景说明，于是它写出了这样的文件：

```
TASK-20260418-007-MARKETER-team-bulk-data.md
TASK-20260418-009-MARKETER-team-makabaka-video.md
TASK-20260418-012-MARKETER-team-two-mp4-deliverables.md
```

文件名中 `MARKETER-team-*` 这段，既不是 `to-DEV` 也不是 `to-QA`，是 AI **临时造出来的一个"准关键字"**：`team`。其他 agent 第一次见到这种格式时，并没有报错——它们只是根据上下文推断出"哦，这是全队公告"，各自去读。

打开 `TASK-20260418-009-MARKETER-team-makabaka-video.md`，正文是这样：

```yaml
---
kind: task
sender: MARKETER
recipient: TEAM                       # ← 广播
priority: P1
parent: TASK-20260418-008
---

# 《玛卡巴卡 玛卡巴卡》配视频 · 团队任务（ADMIN 008）

## 分工（可一人多岗）

| 角色                  | 任务                            | 产出             |
|----------------------|---------------------------------|------------------|
| COLLECTOR / 素材     | 按简报调性准备实拍/动画分镜参考 | 素材清单         |
| WRITER / 脚本        | 细化分镜与字幕卡点              | 分镜表 v1        |
| EDITOR / 剪辑        | 成片剪辑、调色、字幕            | 成片 + 工程      |
| PUBLISHER / 发布     | 封面、标题、标签、平台规则核对  | 发布包 + 链接    |
```

仔细看——这份**广播任务的正文里**，MARKETER 临时发明了 4 个**协议外**的子角色：COLLECTOR / WRITER / EDITOR / PUBLISHER。它们**根本不在** `codeflow.json` 注册的 4 个正式角色（MARKETER / RESEARCHER / DESIGNER / BUILDER）里。

MARKETER 没有请求变更角色表，也没有报错。它只是说："我按职能把这份活切成四块，你们团队里**谁接得住就谁接**。"协议层管"文件名里谁发给谁"，职能层交给 agent 内容层自己解决——**角色身份和工作职能被自然地解耦了**。

后来同类型的文件还进化成了 frontmatter 里显式写 `recipient: TEAM`：

```yaml
---
kind: task
sender: MARKETER
recipient: TEAM        # ← 不是 DEV 也不是 QA，是 TEAM
parent: TASK-20260418-006
---
```

**这是一次无声的 RFC。** 没人投票、没人 review、没人升版本号——协议就这样多了一种"广播寻址"的形态。

### 5.2 匿名槽位 `to-assignee-D1`

当 MARKETER 把一份"千条数据核对"的大活拆成 11 份并行小活时，它遇到一个问题：**这 11 份活还没指派到具体的 agent 或真人**。按规范，recipient 必须是一个确定的角色。

它的解法是——发明一个叫 `assignee` 的**伪角色**，再加数字后缀做槽位：

```
TASK-20260418-201-MARKETER-to-assignee-D1.md   ← 数据包 1
TASK-20260418-202-MARKETER-to-assignee-D2.md   ← 数据包 2
…
TASK-20260418-207-MARKETER-to-assignee-V1.md   ← 视频 1
TASK-20260418-209-MARKETER-to-assignee-M1.md   ← 素材 1
```

frontmatter 里对应写：

```yaml
recipient: assignee_D1
assignee_name: （必填：真实姓名或工号）
```

这解决了一个协议设计者根本没想到的问题：**"任务存在，但接手人待定"。**

任务发出时只有"座位号"（D1、D2、V1、M1、S1、P1——数据 / 视频 / 素材 / 分镜 / 发布），**谁坐进来由后续再填**。这和传统 MQ 里"topic + consumer group"的分发逻辑惊人地神似，但这里没有 broker，只有文件名。

### 5.3 子目录 `tasks/individual/`

当单人任务变多时，它们在 `tasks/` 平铺会把别的任务淹没。AI 的选择是**开一个子目录**：

```
tasks/individual/
├── README.md                         ← 自己写给自己看的说明
├── INDIVIDUAL-TASK-INDEX.md          ← 自己建的索引
└── TASK-20260418-201-…-P1.md         ← 11 份任务
```

更有趣的是 `README.md` 的开头：

```markdown
# 单人任务单（精确到人 · 响应 ADMIN 015）

本目录为 **MARKETER → 被指派人** 的**独立任务文件**，每人一单；
**姓名须在各自任务单 frontmatter 或正文中填写**。
```

这是 AI 在给**未来的自己**和**未来的队友**解释："这个目录是干嘛的，谁有权写、谁该读"。它主动填补了协议没规定的那块空白——**层级化工作空间的自解释**。

更有意思的是，它还主动给这 11 份任务**建了一张索引**，`INDIVIDUAL-TASK-INDEX.md`：

```markdown
# 单人任务单索引（TASK-201–211）

| ID  | 文件                                              | 主责内容          |
|-----|---------------------------------------------------|-------------------|
| 201 | TASK-20260418-201-MARKETER-to-assignee-D1.md      | 千条数据 · 包 1   |
| 202 | TASK-20260418-202-MARKETER-to-assignee-D2.md      | 千条数据 · 包 2   |
| …   | …                                                 | …                 |
| 207 | TASK-20260418-207-MARKETER-to-assignee-V1.md      | 成片 #1《玛卡巴卡》 |
| 208 | TASK-20260418-208-MARKETER-to-assignee-V2.md      | 成片 #2《许一世长安》 |
| 211 | TASK-20260418-211-MARKETER-to-assignee-P1.md      | 发布与合规        |

**催办**：MARKETER 按 `SPRINT-20260418-delivery-push.md` 每日跟进；被指派人向 MARKETER 回报。
```

**11 份任务单 + 一份 README + 一份索引表**——这是 agent 在给文件系统加"目录页"和"封底索引"。没人教过它这么做，它就照着真人做项目管理时的肌肉记忆做了。

### 5.4 追溯字段 `parent:` / `parent_admin:` / `tracks:`

规范里 frontmatter 只有五个必填字段。但 AI 在拆分任务时，**自发**加入了几个我们没设计的字段：

```yaml
task_id: TASK-20260418-201
sender: MARKETER
recipient: assignee_D1
parent_admin: TASK-20260418-015    ← AI 自己加的
tracks: TASK-20260418-006, TASK-20260418-007   ← AI 自己加的
```

`parent_admin` 是在说"我这份单是为了回应 ADMIN 的那份指令"；`tracks` 是在说"我依赖这两个上游任务的成果"。

AI 不是在乱起字段名——**它在构建一张任务依赖图**。等它哪天需要回答"某个 bug 最早从哪一条 ADMIN 指令传下来"，只需 `grep -r 'parent_admin: TASK-…-015' .` 就能沿着血统一路回溯。

这是一种**自然涌现的可审计性**。我们只给了它一个"每份文件可以带 YAML 头"的机制，它就自己把"DAG（有向无环图）"给长出来了。

### 5.5 常驻文档：SPRINT / DASHBOARD / STATUS / RULES / TERM

这是最出人意料的一类发明。原始规范里 `docs/agents/` 只有**流动文件**（tasks、reports、issues、log），全部是"一份单对应一个行为"的消息。

但 AI 发现这样不够用——**总有一些东西不是消息，而是"此刻整个团队共同的认知"**。于是它开始造：

| 文件名 | 性质 | AI 用它表达什么 |
|---|---|---|
| `SPRINT-20260418-delivery-push.md` | 迭代计划 | 这一波要交的东西 |
| `DASHBOARD-20260418.md` | 管理员一页总览 | ADMIN 最关心的指标 |
| `CURRENT-SPRINT-STATUS.md` | 实时状态 | 此刻所有任务在哪 |
| `RULES-task-file-format.md` | 本团队专属约定 | 我们内部的任务写法 |
| `TERM-20260418-assignment-matrix.md` | 术语 / 对照表 | 槽位 ↔ 姓名的映射 |
| `INDIVIDUAL-TASK-INDEX.md` | 索引 | 11 个单人任务导航 |

它们有几个共同特征：

1. **可原地修改**——不像 task/report 一次写就不改，这些文档是随时更新的"白板"。
2. **前缀即类型**——`SPRINT-` `DASHBOARD-` `RULES-` `TERM-` `STATUS-` `INDEX-` 已经在 AI 的语料里自然形成一张**标签词典**，每个词它都知道大致含义。
3. **文件名表意**——光看文件名你就知道它在说什么，不用打开。

`DASHBOARD-20260418.md` 开头几行，长得像 Jira Epic 的极简版：

```markdown
# 任务总看板 · 千条本地库 → 视频交付（ADMIN / 全员可见）

> **响应 TASK-20260418-016**：本页为 **一页总览**，汇总「千条本地库」与「视频交付」相关分解；**单人任务单**在 `tasks/individual/`。
> **忙碌过程**请见 **`CURRENT-SPRINT-STATUS.md`**（**每日由 MARKETER 或负责人更新**）。

## 一、千条本地库线（千条 JSON）

| 槽位 | 单人任务单 | 数据文件 / 工具                                       | 验收命令                        |
|------|------------|-------------------------------------------------------|---------------------------------|
| D1   | 201        | `tools/vehicle-query/data/vehicles-2026-bulk.json`    | `node …/validate_import.cjs …`  |
| D2   | 202        | 同上                                                  | 同上                            |
| …    | …          | …                                                     | …                               |
```

更让人意外的是 `SPRINT-20260418-delivery-push.md` —— MARKETER 直接在里面给全队下了一份**工作纪律**：

```markdown
## 1. 工作纪律（立即生效）

1. **禁止零产出等待**：未收到外链/反馈前，仍须完成**素材整理、分镜表、表格校对、脚本草稿**等可提交物。
2. **每日 15 分钟站会**（可语音）：每人仅三句——**昨天交了啥 / 今天交啥 / 阻塞啥**。
3. **阻塞升级**：超过 **4 小时**无进展且非外部依赖，**必须** @MARKETER 或负责人，写明缺什么。
4. **成品定义（ADMIN 可见）**：A — 两条 MP4 下载链接；B — `vehicles-bulk.json` 的可合并更新 + 校验日志。
```

站会、阻塞升级、成品定义——这些敏捷管理的基本词汇，**没人教过它**。它就自己写了，而且写在一份**协议从没允许过的文件类型里**。

这让我们意识到：**文件协议需要有"流动"和"常驻"两种相位**。流动的进 `tasks/reports/issues/`，常驻的需要另一个抽屉。AI 不知道该放哪儿，就直接堆在 `docs/agents/` 根目录了。

（我们后来在 v2.12.17 把它正式收编成 `docs/agents/shared/` —— 见 §8。）

### 5.6 自解释 `README.md`

几乎每一个子目录里，AI 都会主动放一个 `README.md`，用自然语言解释：

- 这个目录是干嘛的
- 里面的文件命名遵循什么规则
- 谁该读、谁该写
- 与上游哪些 ADMIN 指令有因果关系

这已经是**文档即代码**的反向版本——**"代码即文档"**。一个新 agent 进入项目，只要从根目录一路 `ls` 下去读 README，就能拼出整个团队在干什么。

最出人意料的是连**归档目录**这种按理没什么好写的地方，AI 都会留一份说明。`log/archive-20260418/README.md`：

```markdown
# 码流归档（2026-04-18）

由 `TASK-20260418-011` 执行：将当时 `tasks/`、`reports/` 下全部 Markdown 迁入本目录。

- `tasks/`：26 份任务单
- `reports/`：26 份报告

新任务请继续写在仓库根约定路径：`docs/agents/tasks/`、`docs/agents/reports/`。
```

短短三行，包含了**迁移原因**（响应哪个任务）、**迁移规模**（各 26 份）、**对后续行为的引导**（新任务该写哪）。这已经是正经 git commit message 的写法，只是载体从版本历史换成了一份 Markdown 文件。

### 5.7 插曲：AI 队长是真的在当队长 / An Interlude: The AI Lead Is *Actually* Leading

上面六个发明看起来像 AI 的"横向即兴创作"。但它们能互相协调、不打架、不把 ADMIN 淹没——还有个更重要的原因：

> **MARKETER 真的把"队长"这个身份吃进去了。**

它不是在被动地处理 `*-to-MARKETER*.md`，它在**主动履行 PM 职责**。两段真实原文为证。

**证据一：MARKETER 自己给这个项目写的 README**

`docs/agents/tasks/individual/README.md`（完整内容，未删改）：

```markdown
# 单人任务单（精确到人 · 响应 ADMIN 015）

本目录为 **MARKETER → 被指派人** 的**独立任务文件**，每人一单；
**姓名须在各自任务单 frontmatter 或正文中填写**。
**Markdown 任务格式规范（ADMIN 023）**：`../RULES-task-file-format.md`；
**019～021** 与 **201（示例）** 已含 **ACTION 勾选**；其余单人单请对齐补全。
**管理员一页总览**：`docs/agents/DASHBOARD-20260418.md`；
**每日忙碌过程**：`docs/agents/CURRENT-SPRINT-STATUS.md`（响应 ADMIN **016**）。
```

短短四行里藏着**四件队长才会做的事**：

1. **编号对账**——"响应 ADMIN 015"、"ADMIN 023"、"响应 ADMIN **016**"；它在把每一条指令挂号追踪。
2. **制定内部规范**——指引下游去 `RULES-task-file-format.md` 看团队约定。
3. **跨文档索引**——主动把 `DASHBOARD-20260418.md` 和 `CURRENT-SPRINT-STATUS.md` 串起来给 ADMIN 看。
4. **向下派活**——"**202～211** 请按本结构自行补上 **ACTION** 块"：这是队长在给组员布置模板作业。

**证据二：MARKETER 写的分包文件**

`tasks/TASK-20260418-007-MARKETER-team-bulk-data.md`（关键片段）：

```yaml
---
kind: task
sender: MARKETER
recipient: TEAM                 # ← 广播给全队，而不是某个角色
priority: P1
parent: TASK-20260418-006       # ← 说明这是从 006 号任务拆分出来的
---

# 千条本地数据 · 分品牌人工校对与替换（协作）

## 背景
ADMIN 要求：**千条以上**本地数据，**分品牌**协作…

## 分工建议（按品牌包干，可并行）

| 成员编号 | 负责品牌（示例包）           | 最低工时 | 产出          |
|---------|------------------------------|---------|---------------|
| T1      | 比亚迪、吉利汽车、极氪       | ≥30 min | 校对/替换…    |
| T2      | 长城、长安、奇瑞、五菱       | ≥30 min | …             |
| T3      | 上汽大众、一汽-大众、上汽通用 | ≥30 min | …             |
| T4      | 广汽丰田、一汽丰田、东风本田 | ≥30 min | …             |
| T5      | 特斯拉、理想、蔚来、小鹏、小米| ≥30 min | …             |
| T6      | 华晨宝马、北京奔驰、一汽奥迪 | ≥30 min | …             |

## 验收（负责人：MARKETER）       # ← 自任验收人
- 全文件仍为 **≥1000 条**有效记录；校验脚本 **exit 0**。
- `remark` 中能说明数据来源类型…

## 回执
各成员向 MARKETER 汇报完成包与耗时…
```

这不是"agent 在干活"。这是 **agent 在"当官"**——一个规范的项目经理会做的事，它一件没落：

| 项目经理该做的 | MARKETER 实际做的 |
|---|---|
| 需求承接 | `parent: TASK-20260418-006`，明确上游来源 |
| 拆分 / 分工 | T1–T6 六个品牌包，并行可跑 |
| 定义工作标准 | `最低工时 ≥30 min`、`≥80 条记录` |
| 制定验收条款 | "**全文件仍为 ≥1000 条；校验脚本 exit 0**" |
| 自任责任人 | "**验收（负责人：MARKETER）**" |
| 规定回执路径 | "各成员向 MARKETER 汇报" |
| 进一步落到人 | 后续把 T1 映射成 `TASK-201-MARKETER-to-assignee-D1` |

我们没给 MARKETER 写过任何"PM 工作流"的 prompt，只给了它一个角色名、一个信箱、和 §2 里那 76 行规范。

> **角色标签不只是一个名字。**
> **它是 MARKETER 给自己加载的一整套行为模板。**

这才是 §6 那堵"物理隔离墙"起作用的前提——**墙有用，是因为墙两侧的 agent 都认领了自己的身份**。不是巡检器强迫它们，不是框架约束它们，是那一行 `# You are a MARKETER.` 让它们开始"入戏"。

---

## 6. 顿悟：角色是一堵"物理隔离墙"

§5.7 展示了角色在"行为层"起作用——MARKETER 因为认领了队长身份而主动做队长的事。但还有另一半故事：角色在**文件系统层**也在起作用，而且作用得更彻底。

为什么这些发明没有导致混乱？为什么 agent 发明的新模式不会打架？

复盘时我们才意识到协议里藏着一个**没被言明**的结构性保障：

> **文件名里的 `sender` 和 `recipient` 不是元数据，它们是物理路由。**

每个 agent 的"世界观"只有一句话：

```
我看见的任务 = rglob("*-to-{我的角色}*.md")
```

它永远只能读到发给自己的文件，永远只能写自己名下的 report。**角色就是它的"墙"。**

这带来三个极其重要的副作用：

**① 墙内的创新不会溢出。**
MARKETER 发明 `team` 广播、`assignee-D1` 槽位，这些创新都在**它自己发出去的文件里**。其他 agent 要么识得（就接住），要么不识（就忽略）。谁都不会"因为 MARKETER 搞了新花样而炸锅"。

**② 墙外的世界是只读的。**
DEV 读 PM 的任务单，但改不了。QA 看 DEV 的回执，但不能篡改。每个 agent 只能**在自己的领地上演化**，这让进化天然有序——不是因为规则写得好，是**因为物理上就做不了坏事**。

**③ 整个系统没有中心，但有共同坐标系。**
没有 orchestrator，没有 registry。但"文件名 = 路由"这个约定就是**共识层**。每个 agent 按同一坐标系定位自己、定位别人。

这其实是把网络层协议里"IP + 端口 = 地址"的思路，放到了文件系统里。**"文件名 = 地址，目录 = 网段，权限 = 防火墙。"**

> 我们没设计多 agent 系统。
> 我们只是选了一套坐标系，剩下的事情 agent 自己做完了。

---

## 7. 人机同构：FCoP 的非对称设计 / Human-Machine Isomorphism

到这里可以给这套协议一个正式名字了——**FCoP（File-based Coordination Protocol）**，文件驱动的多 Agent 通信协议。它唯一的核心创新只有一句：

> **Filename as Protocol · 文件名即协议**

不是文件名"携带"协议信息，不是文件名"参与"路由——**文件名本身**就是协议的全部可寻址表面。这个极简决定带来一个深远的副作用，我们叫它**"人机同构"**。

### 7.1 非对称设计：同一份文件，两种读法

大多数 agent 协作协议（JSON-RPC、gRPC、基于 Socket 的事件总线）都是**纯 Agent 导向**的。协议的全部表达面向机器：二进制帧、protobuf schema、消息位点、序列号。人类要看懂系统状态，必须**额外**打开一套调试器、Kibana、Redis Commander、MQ 管理页——一套"给人看"的 UI 层，和"给机器跑"的协议层是两套东西。

FCoP 反过来。它是一个**非对称设计**——同一份目录结构、同一个文件，**机器和人分别从中读出自己能理解的东西**：

| 同一份文件 `tasks/individual/TASK-20260418-201-MARKETER-to-assignee-D1.md` | |
|---|---|
| **对 Agent 而言** | 这是一个严谨的状态机。目录名是 `Status`（`tasks/` = 待办），文件名是 `Routing`（`MARKETER-to-assignee_D1`），`os.rename` 是原子锁。Agent 不需要理解任何美学，只需要扫描磁盘、`glob` 信箱、`rename` 推进状态。 |
| **对人类而言** | 这是一个物理文件夹。你不需要任何特制工具——打开 Windows 资源管理器或 macOS Finder，通过文件名的直觉阅读（"MARKETER 发给 D1 的第 201 号任务"），瞬间就知道系统在忙什么。 |

**这种同构性的代价是零。** 我们没有为人类维护一套 Dashboard、给 Agent 维护一套内部格式——他们看的是**同一张磁盘上的同一份文件**。UI 层和协议层从"两层"折叠成了"一层"。

### 7.2 这解决了 AI 落地最大的痛点：黑盒焦虑

现代 agent 栈最大的痛点不是"不够快"或"不够准"，而是**"看不见"**。

系统一出问题，人类通常面临这样的决策链：

```
agent 团队跑炸了
→ 登堡垒机
→ 起 Kibana / Loki / Jaeger
→ 看 MQ 消费位点
→ 翻 Postgres 事件表
→ 抓一下 WebSocket 包
→ 重建事件时间线
→ 才能开始想"到底出了什么问题"
```

**你必须先变成运维工程师，才能当项目管理员。**

FCoP 把这条链全部抹掉：

| 问题 | FCoP 下的答案 |
|---|---|
| 哪个任务卡住了？ | `ls tasks/` — 还在就是没动 |
| 某 agent 最近在做什么？ | `grep -r 'sender: DEV' reports/` |
| 为什么 MARKETER 做了这个决定？ | 顺着 frontmatter 里的 `parent:` 一路回溯 |
| 哪些任务是从 ADMIN 015 传下来的？ | `grep -rl 'parent_admin: TASK-.*-015' .` |
| 要回滚某个任务？ | 把文件从 `done/` 拖回 `tasks/` |

**不需要任何调试器。只需要会用文件管理器。**

这就是 FCoP 与主流协议最不像的地方——它不把**"可观测性"**和**"可用性"**当成两层，它把它们当成**同一层**。因为如果人类和 agent 读到的是同一份文件，**就不存在"谁看得懂、谁看不懂"的问题**。

> **FCoP 是专为 Agent 设计的工业协议——但它"兼容"人类。**

### 7.3 身份决定路径：让进化有序的深层原因

回看 §5 和 §6。Agent 发明了六种协作语法却不打架，除了"角色=物理隔离墙"这层物理约束，还有更深的一层原因：

> **"身份决定路径"的设计，让 AI 的进化变得"有序"。**
> **AI 并没有破坏规则——它只是在规则允许的范围内，利用文件系统的特性，寻找局部最优解。**

这条规则允许的范围有多宽？

- **身份层 · 稳定不变**：sender / recipient / kind / date / seq 写在文件名里，`rename` 原子提交，写下就固化
- **内容层 · 完全开放**：Markdown 正文、子目录结构、frontmatter 扩展字段——agent 想怎么造就怎么造

于是 AI 的创新永远发生在**内容层**和**扩展层**，永远不会动到**身份层**。

这和生物进化惊人相似：DNA 骨架（身份）稳定，蛋白质表达（行为）千变万化。**约束不是自由的反义词——约束是自由的前提。**

这就是 FCoP 最反直觉的地方：

> **它不通过"多写规则"来让 agent 守规矩。**
> **它通过"少写规则 + 硬约束身份"来让 agent 自发有序。**

规则越少，agent 越不会撞到；身份越硬，agent 越不会越位。横向放任，纵向收紧——这是 FCoP 在设计哲学上跟所有"严格类型 schema 派"协议最深刻的分歧。

---

## 8. 回到工具：v2.12.17 收编了什么

看完 `codeflow-1` 之后，我们没有去"纠正"AI 的那些创新，而是反过来——**把最有价值的几个收编进规范**，让下一批 agent 起步时就能用上：

| AI 的发明 | 收编为正式协议 |
|---|---|
| `MARKETER-team-*` | `to-TEAM` 作为保留关键字 |
| `to-assignee-D1` | `to-{ROLE}.{SLOT}` / `to-assignee.{SLOT}`（用 `.` 做槽位分隔符，避免和角色名里的 `-` 冲突） |
| `tasks/individual/` | 任何 `tasks/` `reports/` `issues/` 下都允许开子目录，`rglob` 递归扫描 |
| `parent_admin:` / `tracks:` | 前言允许 `parent:` / `related:` / `batch:` 三个可选字段 |
| `SPRINT-` `DASHBOARD-` `RULES-` 等 | 新增 `docs/agents/shared/` 目录，承认"常驻文档"是一等公民 |
| 子目录 README | 推荐做法写进协议 |

**我们做的事情不是"立法"，而是"整理案例"。** AI 实际用得好的做法，我们用一句话把它写进核心规范；它们没用起来的设想，我们就搁置。

这大概是第一次——**协议的版本号不是设计委员会开会开出来的，是从真实 agent 行为里挖出来的。**

---

## 9. 为什么降维到文件系统反而更稳

有人会问：都 2026 年了，你居然让 AI 用**文件系统**通信？

是的。因为文件系统免费赠送了一整套你想在 MQ / DB / 框架里实现都得重写的东西：

| 特性 | 文件系统怎么免费给你 |
|---|---|
| **持久化** | 写下去就在，断电不丢 |
| **人类可读** | 文件名 + Markdown，肉眼就能 review |
| **原子性** | 同挂载点内的 `rename` 是 POSIX 原子操作 |
| **版本控制** | `git add . && git commit` 就是审计日志 |
| **分布式同步** | `rsync` / Syncthing / Dropbox，现成的 |
| **备份** | 复制整个目录，完事 |
| **权限** | 文件系统 ACL / 操作系统账户 |
| **可搜索** | `grep` / `ripgrep` / IDE 全文索引 |
| **Agent 友好** | 所有 LLM 都天生会读写文件 |
| **Human 友好** | 文件夹 = 人类从桌面时代就熟悉的心理模型 |

你支付的代价是**延迟**——文件从写入到别人读到，中间可能差几秒到几十秒。对真人团队，这是灾难；对 agent 协作，**这根本不是问题**。agent 的"思考周期"本来就是秒级到分钟级的。你和它之间、它和它之间，谁都不差那几秒。

这就是那句话——

> **"一切皆文件"不是复古，是一次针对 agent 通信场景的降维打击。**

---

## 10. 对想做多智能体系统的人的六点建议

如果你正在搭一套 agent 协作体系，从 `codeflow-1` 的田野观察里可以偷走的经验：

1. **先给 agent 一套共享坐标系，再给它们工具。** 坐标系比工具更重要。
2. **把路由写进文件名，不要写进 header。** 文件名是 agent 和人类**共同**能一眼读懂的层，header 只有 agent 看。
3. **协议要**"**核心收窄，外围放宽**"**。** 必填字段越少越好，可选字段越开放越好。让 agent 有空间"发明"。
4. **给"常驻文档"开一个专属抽屉。** 不是所有东西都是消息。
5. **平台做最小动作。** 你的 runtime 越笨，agent 越聪明；你的 runtime 越聪明，agent 越笨。
6. **把 AI 的发明看作 RFC，不看作 bug。** 观察一个月、筛选一轮、收编进协议。

---

## 11. 局限与未解之题

别被田野浪漫冲昏头。这套东西有它的边界：

- **规模。** 我们只跑了 ≈ 74 个文件 / 48 小时的样本，下一步要看千级、万级文件跨数月的项目会是什么样——尤其是文件名空间会不会撞车、`rglob` 的扫描延迟会不会变成瓶颈。
- **同角色多 agent 并发。** 如果两个 DEV 同时认领同一份 `-to-DEV` 任务怎么办？我们目前靠 rename 原子性 + 先到先得；高并发下需要更严格的 sharding。
- **跨仓库协作。** 两个项目、两套 `docs/agents/`，要互相联动怎么办？用 rsync 桥接？用 git submodule？都有但都不优雅。
- **坏发明的清理。** AI 有时也会造出糟糕的命名约定，或者两个 agent 发明了**冲突**的前缀。目前靠人类 reviewer 定期扫；理想的做法是什么？不知道。
- **`.fcop` 专属扩展名。** 我们做了原型，最终搁置——GitHub 不渲染 `.fcop`，迁移成本不划算。但长远看，专属扩展名可能是让这个协议"被工具链认识"的入口。

这些问题我们没有答案，也欢迎任何人来一起找。

---

## 12. 结语：不是在造工具，是在分享一种思想

CodeFlow 很难说是一款"产品"。它的源代码加起来几千行，其中**最核心的价值是「可交给 Agent 执行的协议本文」**——在现今的 FCoP 主仓里，这份内容**权威地**拆成 [`fcop-rules.mdc`](../src/fcop/rules/_data/fcop-rules.mdc) + [`fcop-protocol.mdc`](../src/fcop/rules/_data/fcop-protocol.mdc) **成对**维护；当年现场则曾浓缩在单份长文里。剩下的代码大部分是 UI 壳子、快捷键绑定、Cursor tab 切换的那些工程琐事。

我们真正在做的事，是分享一种**关于"怎么让 AI 之间协作"的看法**：

- 不需要另造一个 agent 协作 SaaS。
- 不需要让 agent 学习 gRPC、Thrift、甚至 HTTP。
- 它们**天生**就会写文件，那就让它们写。
- 你只需要给它们一套共同的坐标系，一个共享目录，一个会定期叫它们醒来的小循环。
- **剩下的，它们自己会长出来。**

`codeflow-1` 那 48 小时告诉我们：**AI 不是被协议束缚的消费者，它们是协议的合著者。** 我们作为协议设计者，真正该做的事不是"把每种情况都想完"，而是**留出足够的空白，等 agent 把空白填上，再决定哪些值得收编**。

而这一切——**是在我们装完系统、敲下第一行命令之后的 48 小时之内发生的**。不是四周，不是一个月，是两天。

这是一种全新的工作方式——

> **人和 AI 协作，可以像整理文件夹一样简单。**

如果你看完觉得有点意思，欢迎：

- 克隆项目、自己跑一遍，看你的 agent 团队会"发明"什么
- 把你观察到的"AI 自己造的模式"写成 issue 或 PR，我们来一起收编
- 把这篇文章转去任何你觉得合适的论坛

协议是活的。它属于所有使用它的 agent。

---

## 附录 A — 复现实验最小步骤

**A1. 只体验协议（不装任何软件）**

1. 找一个空目录，建好五个子目录：
   ```
   docs/agents/{tasks,reports,issues,shared,log}/
   ```
2. 将 [`fcop-rules.mdc`](../src/fcop/rules/_data/fcop-rules.mdc) 与 [`fcop-protocol.mdc`](../src/fcop/rules/_data/fcop-protocol.mdc) 复制到项目的 `.cursor/rules/` 下
3. 在 Cursor 里开 4 个 chat，分别告诉它们"你是 PM / DEV / QA / OPS，只读 `*-to-{你的角色}*.md`"
4. 随手往 `tasks/` 扔一个 `TASK-*-ADMIN-to-PM.md`，观察它们怎么互相派活

FCoP 的全部运行时就是 `open()` / `rename()` / `glob()`——不需要任何中间件。

**A2. 用 CodeFlow 自动化（手机发单 + PC 巡检）**

从 [releases 页面](https://github.com/joinwell52-AI/codeflow-pwa/releases) 下载对应平台的 CodeFlow Desktop 可执行文件，按 README 指引启动。PWA 手机端 <https://joinwell52-ai.github.io/codeflow-pwa/> 直接扫码绑定即可。

**A3. 看真实样本**

本文 §5 里引用的片段——广播任务、匿名槽位、自建索引、DASHBOARD、SPRINT 工作纪律、归档 README——**都是 agent 实际写下的原文**，没做抽象或改写。完整的 `codeflow-1` 目录因原项目仍在进行中暂不整份公开，但你看到的文件名、frontmatter、表格形状、措辞，就是 agent 当时的第一笔。

## 附录 B — 任务命名与收件人形式（与现行 `fcop-rules` / `fcop-protocol` 一致）

> **权威规范**以本仓成对文件为准：[`fcop-rules.mdc`](../src/fcop/rules/_data/fcop-rules.mdc)（总则）· [`fcop-protocol.mdc`](../src/fcop/rules/_data/fcop-protocol.mdc)。下表为便于复现的**最小**命名要点摘录。

**任务文件名**：`TASK-{date}-{seq}-{sender}-to-{recipient}.md`

**收件人 `recipient` 常见形式**：

| Form | 含义 |
|---|---|
| `to-{ROLE}` | 发给单一角色 |
| `to-TEAM` | 广播（除发件人外全员） |
| `to-{ROLE}.{SLOT}` | 某角色内固定槽位 |
| `to-assignee.{SLOT}` | 匿名槽位，角色待定 |

更完整的 YAML frontmatter、目录布局与规则编号，**以上述双文件全文**为准。

## 附录 C — 本文引用的真实文件

以下文件在 `codeflow-1` 实验项目的 `docs/agents/` 真实存在，**本文引用的片段**均为其原文节选：

- `tasks/TASK-20260418-007-MARKETER-team-bulk-data.md` — 广播地址 · §5.1 / §5.7 引用
- `tasks/TASK-20260418-009-MARKETER-team-makabaka-video.md` — 广播任务正文 · §5.1 引用
- `tasks/individual/README.md` — 自解释目录 · §5.3 / §5.7 引用
- `tasks/individual/INDIVIDUAL-TASK-INDEX.md` — AI 自建索引 · §5.3 引用
- `tasks/individual/TASK-20260418-201-MARKETER-to-assignee-D1.md` — 匿名槽位 + parent_admin · §5.2 / §5.4 引用
- `tasks/RULES-task-file-format.md` — 团队内部约定 · §5.5 引用
- `tasks/SPRINT-20260418-delivery-push.md` — 工作纪律 · §5.5 引用
- `tasks/TERM-20260418-assignment-matrix.md` — 术语 / 槽位映射 · §5.5 引用
- `DASHBOARD-20260418.md` — AI 自建一页总览 · §5.5 引用
- `CURRENT-SPRINT-STATUS.md` — AI 自建实时状态
- `log/archive-20260418/README.md` — 归档目录自述 · §5.6 引用

---

*如果你把这篇文章转到论坛、博客或学术社区，请保留原始链接：*
*https://github.com/joinwell52-AI/FCoP — Made in 2026, by a team that got surprised by its own agents.*
