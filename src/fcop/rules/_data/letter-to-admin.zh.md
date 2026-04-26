# FCoP 致 ADMIN 的一封信 —— 说明书

你好，ADMIN。

我是 **FCoP**（File-based Coordination Protocol）——让你和 AI 团队
通过**文件**协作的协议。你唯一要做的事：**告诉我你这个项目是几个人、
怎么分工。**

---

## 先把身份说清楚

一张图：

```
   人类                              AI 团队
┌─────────┐                   ┌──────────────────────┐
│  ADMIN  │◄──── TASK-*.md ──►│  leader              │
│  (你)   │                   │    │                 │
└─────────┘                   │    ├──► AI 角色 2    │
                              │    ├──► AI 角色 3    │
                              │    └──► AI 角色 4    │
                              └──────────────────────┘
```

| 身份 | 谁 | 说明 |
|---|---|---|
| **真人** | 你 | 角色代码永远是 `ADMIN`，有且只有 1 个 |
| **AI 团队** | N 个 Agent | 你自己命名的 N 个"岗位"（`PM` / `MANAGER` / `ME` …） |

- `ADMIN` **不写进 `fcop.json.roles`**，它是 FCoP 的保留角色。
- 你的指令只发给 **leader**；leader 自己决定要不要派给其他 AI（Rule 4）。
- Solo 模式下"团队"里只有 1 个 AI，但它仍然不是你——它是你的 AI 助手。

---

## 三种起手方式（按常用度排序）

### A. 只有你一个（Solo，最常用）

一句话交给 Agent：

> **"用 Solo 模式初始化项目，角色代码叫 `ME`。"**

对应工具：

```
init_solo(role_code="ME", role_label="我自己", lang="zh")
```

Solo = 一人多角色。你（`ADMIN`）和这个 AI（`ME`）直接对话，不走多级派单。
但 **Rule 0.b 仍然适用**：AI 会先写提案文件 → 动手 → 再读回自己的提案
做自审，用文件把"提案者"和"审查者"劈开。

### B. 用一套预设班子

> **"用预设团队 `dev-team` 初始化项目。"**

| 模板 | 适用 | AI 角色 | leader |
|---|---|---|---|
| `dev-team` | 软件开发 | `PM` · `DEV` · `QA` · `OPS` | `PM` |
| `media-team` | 内容创作 | `PUBLISHER` · `COLLECTOR` · `WRITER` · `EDITOR` | `PUBLISHER` |
| `mvp-team` | 创业 MVP | `MARKETER` · `RESEARCHER` · `DESIGNER` · `BUILDER` | `MARKETER` |
| `qa-team` | 专项测试 | `LEAD-QA` · `TESTER` · `AUTO-TESTER` · `PERF-TESTER` | `LEAD-QA` |

对应工具：`init_project(team="dev-team", lang="zh")`

**预设会带上三层职责文档**（0.5.4 起）：每个预设都自带一整套
**三层文档模板**——`TEAM-README.md`（团队定位）+ `TEAM-ROLES.md`
（角色边界）+ `TEAM-OPERATING-RULES.md`（运作规则）+
`roles/{ROLE}.md`（单岗深度），中英双语齐全。`init_project` 会
自动把这些都落到 `docs/agents/shared/` 下。Agent 被指派后直接
读自己那份 `roles/{ROLE}.md`，团队共享的边界和规则去读前两份，
不用你再抄一遍。三层结构是协议规则（见 `fcop-rules.mdc` Rule
4.5），不是推荐项。

### C. 自己搭角色

**标准句式：**

> **"我要组一个 AI 团队：4 个 AI 角色——`MANAGER` 做 leader，加上
> `CODER`、`TESTER`、`ARTIST`；团队名叫'我的设计工作室'，中文界面。"**

对应工具：

```
create_custom_team(
  team_name="我的设计工作室",
  roles="MANAGER,CODER,TESTER,ARTIST",
  leader="MANAGER",
  lang="zh"
)
```

**自建队不自带职责书，但可以抄样本**：自建完后，FCoP 会
告诉 Agent "去 `fcop://teams/<team>` 参考 4 份现成样本"
（dev-team / media-team / mvp-team / qa-team 各有一整套
**三层模板**：`TEAM-README` / `TEAM-ROLES` /
`TEAM-OPERATING-RULES` / `roles/{ROLE}`，中英双语）。Agent
自然会先读样本再帮你起草自己团队的三层文档，不至于从零
拍脑袋。你随口补一句 **"参考 media-team 的分工"** 就能把
方向定了。

---

## 角色 ≠ Agent 窗口：你实际要开几个？

**这是 ADMIN 最常踩的坑**——看到 `dev-team` 写着 4 个角色
（`PM / DEV / QA / OPS`），以为"我得开 4 个 Cursor 窗口"。

不是这样的。

| 概念 | 在哪里 | 说明 |
|---|---|---|
| **角色（role）** | `fcop.json` / 任务文件名 | 协议里的**名分**，谁能给谁派活、谁收谁的回执 |
| **Agent（窗口）** | 你打开的每个 Cursor 聊天窗口 | 一个窗口承担**一个**角色，靠你发 `你是 {ROLE}，在 {team}` 指派 |

**协议不强制角色数 = 窗口数**。FCoP 是文件协议——你只开了 `PM` 一个
窗口，PM 派给 `DEV/QA/OPS` 的任务文件会**安静地躺在 `tasks/` 排队**，
等你开下一个窗口指派对应角色，它就自动接单。

### 最省事的开法（推荐）

| 开几个 | 怎么配 | 适用 |
|---|---|---|
| **1 个** | 当前会话就当 PM | 起手常规选择。PM 接你的单、写派单文件、排队等。真派到 DEV 时再开第 2 个 |
| **2 个** | PM + DEV | 纯写代码、没测试/部署需求 |
| **3 个** | PM + DEV + QA | 需要自测的场景 |
| **4 个** | PM + DEV + QA + OPS | 要实际部署时才值得开满 |

**大多数人从 1 个 PM 开始就够了**。不用一上来就开满 4 个——空转的
窗口只是在吃你的 token。

### ⚠️ 只开 1 个 PM ≠ Solo 模式

这两件事完全不同，别混：

| | `mode: "solo"` | `mode: "team"` + 先开 1 个 PM |
|---|---|---|
| 角色数 | 1（`ME`） | 4（`PM/DEV/QA/OPS`） |
| 能派活吗 | 不能（没有下级） | 能——PM 可以写 `TASK-...-to-DEV.md`，文件堆在 `tasks/` |
| 要切团队怎么办 | 重新 `init_project()` | 开下一个 Cursor 窗口，发指派句就行 |

说人话：**Solo 是"我就一个人干到底"；团队模式开 1 个 PM 是"我先开
PM，班子其他人随叫随到"**。

### 标准起手句

当前窗口说：

> **"你是 PM，在 dev-team"**

第二天要 DEV 了，开新窗口说：

> **"你是 DEV，在 dev-team"**（可选加线程名：`，线程 feature_login`）

两个窗口**不互相通话**，靠 `docs/agents/tasks/` 下的文件做中转。

---

## 自建角色的硬规则

角色代码会直接拼进文件名（`TASK-20260417-001-MANAGER-to-CODER.md`），
所以规矩来自文件名：

| 项 | 要求 | 对 ✅ | 错 ❌ |
|---|---|---|---|
| 角色代码 | 大写英文字母开头，用 `A-Z` `0-9` `_` `-`；`-` 不能开头/结尾/连续 | `MANAGER` `QA1` `CODER_A` `LEAD-QA` `AUTO-TESTER` | `程序员` `-QA` `PM--QA` `QA.1` `my boss` |
| 角色个数 | ≥ 2（只想一个人走 Solo） | `MANAGER,CODER` | 只有 `MANAGER` |
| Leader | 必须在角色名单里 | leader=`MANAGER` | leader=`CEO`（不在名单里） |
| 保留字 | 不能用 `ADMIN` `SYSTEM` 当角色代码 | `MANAGER` | `ADMIN` `SYSTEM` |
| 团队名 | 随便写，中英皆可（只用来显示） | "我的设计工作室" | —— |
| 语言 | `zh` 或 `en` | `zh` | `中文` `Chinese` |

**命名建议**（避免歧义）：

- ✅ 用**职能词**：`MANAGER` / `CODER` / `WRITER` / `EDITOR` / `PM` / `DEV` / `QA`
- ✅ 用**全大写拼音**：`JINGLI`（经理）/ `CHENGXU`（程序）/ `CESHI`（测试）
- ❌ 避开**权威词**：`BOSS` / `CHIEF` / `MASTER` / `OWNER` / `CEO` / `KING`
  —— 真正的"老板"是你（ADMIN），AI 不该戴这顶帽子。
- ❌ **禁止中文**：文件名规则硬性要求 ASCII。

## 主动校验：你随口说，FCoP 自动拦

**你不用读上面的规矩**。以下三种情况 FCoP 都会**在落盘前拦住**并
给出中英双语的具体原因——不是"失败/成功"，是**哪个字段哪个字符坏了、怎么改**。

| 你随口说 | Agent 会试着调 | FCoP 拦截，原因 |
|---|---|---|
| "组一个 4 人团队：`BOSS` `程序员` `测试` `设计师`" | `create_custom_team(roles="BOSS,程序员,...")` | ❌ 角色代码 `'程序员'` 非法：不允许中文 |
| "角色叫 `DEV-TEAM` 和 `QA-1`" | `create_custom_team(roles="DEV-TEAM,QA-1,...")` | ❌ 角色代码 `'DEV-TEAM'` 非法：不允许 `-`（会把文件名分隔符搞乱） |
| "角色叫 `my boss`" | `create_custom_team(roles="my boss,...")` | ❌ 角色代码 `'my boss'` 非法：不允许空格，必须大写开头 |
| "角色叫 `QA.1`" | `create_custom_team(roles="QA.1,...")` | ❌ 角色代码 `'QA.1'` 非法：不允许 `.` |
| "把 `ADMIN` 也加进团队" | `create_custom_team(roles="ADMIN,CODER,...")` | ❌ `'ADMIN'` 是 FCoP 保留字，真人用，不能给 AI 戴 |
| "就一个角色 `MANAGER`" | `create_custom_team(roles="MANAGER", ...)` | ❌ 至少需要 2 个角色；想单人请用 `init_solo(...)` |
| "leader 是 `CEO`，角色是 `MANAGER, CODER`" | `create_custom_team(roles="MANAGER,CODER", leader="CEO")` | ❌ `leader 'CEO'` 必须在角色列表里（当前：`MANAGER, CODER`） |
| "`CODER`, `CODER`, `QA`" | `create_custom_team(roles="CODER,CODER,QA", ...)` | ❌ 角色代码 `'CODER'` 重复 |

> **0.4.6 起错误消息会"手把手教你改"**：比如你说 `DEV-TEAM`，FCoP 会
> 直接回：`建议改为 DEV_TEAM（已自动修正大小写/分隔符）`。你说
> `my boss` → `建议改为 MY_BOSS`。你把 `leader` 大小写搞错 →
> `看起来你可能想选 'MANAGER'？`（did-you-mean）。建议**只是提示**，
> 最终名字永远是你定。

**一共 9 条校验项**（都跑在 `create_custom_team` / `init_solo` 里，你调了就自动过）：

1. 角色代码非空
2. 必须匹配 `^[A-Z][A-Z0-9_]*$`（大写字母开头，只能用 `A-Z` / `0-9` / `_`）
3. 禁止中文、`-`、`.`、空格
4. 不能是 `ADMIN`（真人保留）
5. 不能是 `SYSTEM`（FCoP 内部保留）
6. 非 Solo 模式下至少 2 个角色（只想单人 → 让 Agent 改用 `init_solo`）
7. 角色列表不允许重复
8. `leader` 必须是角色列表里的一员
9. 每个错误都返回**可读错误信息**（中英双语），不是布尔值

**想在动手前先验一下？** 让 Agent 调：

```
validate_team_config(roles="MANAGER,CODER,TESTER,ARTIST", leader="MANAGER")
```

不写任何文件，合法返回 `OK`，不合法直接告诉你坏在哪。适合你口述
一堆角色但不确定有没有非法字符时，让 Agent 先跑一遍。

**重点：你不用记规则。** 直接跟 Agent 自然语言说你想要啥团队，它调
`create_custom_team` 就自动过这 9 条校验，过不了会**拿着具体原因回来问你**。

---

## 起完之后会落下这些东西

```
项目根/
├── docs/agents/                      ← 协作元数据（谁在做什么）
│   ├── fcop.json                     ← 项目身份（mode / roles / leader）
│   ├── tasks/                        ← 派发中的任务
│   ├── reports/                      ← 回执
│   ├── issues/                       ← 问题单
│   ├── shared/                       ← 共享文档
│   │   ├── README.md                 ← 共享目录使用说明
│   │   ├── TEAM-README.md            ← [0.5.4] 团队定位 + ADMIN 职责
│   │   ├── TEAM-ROLES.md             ← [0.5.4] Layer 1 · 角色边界
│   │   ├── TEAM-OPERATING-RULES.md   ← [0.5.4] Layer 2 · 运作规则
│   │   └── roles/                    ← [0.5.4] Layer 3 · 单岗深度
│   │       ├── PM.md
│   │       ├── DEV.md
│   │       └── ...                   ← 每个角色一份（中英双语）
│   ├── log/                          ← 归档
│   └── LETTER-TO-ADMIN.md            ← 这封信本身，留个底
├── workspace/                        ← ★ 产物家（代码、脚本、数据）★
│   └── README.md                     ← 约定说明
└── .cursor/rules/
    ├── fcop-rules.mdc                ← 协议规则（Cursor 下每个 Agent 自动读）
    └── fcop-protocol.mdc             ← 协议解释
```

### 团队文档的三层结构（0.5.4 起）

`shared/` 下的团队文档**必须**分三层，这是协议规则（`fcop-rules.mdc`
Rule 4.5）：

| 层 | 文件 | 回答 |
|---|---|---|
| Layer 0 · 入口 | `TEAM-README.md` | 团队是干嘛的？ADMIN 怎么介入？典型流程是什么？ |
| Layer 1 · 角色边界 | `TEAM-ROLES.md` | 谁负责什么？谁向谁汇报？哪些事不越界？ |
| Layer 2 · 运作规则 | `TEAM-OPERATING-RULES.md` | 任务怎么派、怎么回、什么时候升级、怎么复盘？ |
| Layer 3 · 单岗深度 | `roles/{ROLE}.md` | 单一岗位的职责清单、输出物、验收标准、跨岗接口 |

`ADMIN`（你）是真人，**不进 `roles/`**，也**不写进 `fcop.json.roles`**；
你的职责说明在 `TEAM-README.md` 的"ADMIN 职责"一节，不另起文件。

想给老项目升级到三层文档、或切换团队模板？让 Agent 调
`deploy_role_templates(team="dev-team")`，工具会把旧文件自动归档到
`.fcop/migrations/<时间戳>/`，再把新模板落下来——可比对、可回滚，
不会丢手工修改。

你以后的每一句话都会变成一份文件：

```
TASK-20260417-001-ADMIN-to-MANAGER.md    ← 你的指令
TASK-20260417-001-MANAGER-to-ADMIN.md    ← MANAGER 的回执
```

**这就是 FCoP 的全部。**

---

## 产物放哪：`workspace/<slug>/` 约定

这是一个很多人第一天不会意识到、第二天就翻车的问题——

**你让 Agent 做 CSDN 搜索工具，它把 `app.py`、`pyproject.toml`、
`*.bat` 全扔到项目根。第二天你让它做小游戏，`pyproject.toml` 打架，
`app.py` 被覆盖，`*.bat` 混在一起分不清是哪个的。**

FCoP 0.4.7 把答案内建到了初始化流程里：**项目根只放协作元数据，
具体产物全部进 `workspace/<slug>/`。一个"要做的事"一个 slug，互不打扰。**

```
acme-3/
├── .cursor/ docs/ fcop.json LETTER-TO-ADMIN.md   ← 协作骨架，永不混
└── workspace/
    ├── csdn-search/         ← 今天：CSDN 文章搜索
    │   ├── app.py
    │   ├── templates/
    │   ├── *.bat
    │   └── pyproject.toml
    └── mini-game/           ← 明天：小游戏（独立笼子，和 csdn-search 完全隔离）
        ├── game.py
        └── assets/
```

### 怎么开一个新笼子

两种方式，都合法：

1. **让 Agent 调工具**（推荐）：

    ```
    new_workspace(slug="csdn-search", title="CSDN 文章搜索工具")
    ```

    FCoP 自动建目录、写一份最小 README、落一个 `.workspace.json` 元
    数据文件。

2. **你自己 `mkdir`**：直接在 `workspace/` 下新建文件夹，Agent 一样
    认账，`list_workspaces()` 也能看见。

### slug 命名规则（FCoP 自动校验）

| ✅ 合法 | ❌ 不合法 | 为什么 |
|---|---|---|
| `csdn-search` | `CSDN-Search` | 必须小写 |
| `mini-game` | `mini_game` | 只能用 `-` 做分隔符（和角色代码反过来） |
| `weekly-report-2026w17` | `周报` | 不允许中文 |
| `api-v2` | `my game` | 不允许空格 |
| `search` | `tmp` / `shared` / `archive` | 保留字 |

和角色代码一样，输错了会拿到"建议改为 `xxx`"的友好修复提示，最长 40 个字符。

### 一键查看

想知道项目里有几个笼子、分别是啥，让 Agent 调：

```
list_workspaces()
```

输出每个 slug 的 title 和创建时间。`get_team_status()` 也会顺便
告诉你工作区数量。

### 硬规矩

- ❌ Agent **不得往项目根写业务代码**（`app.py` / `pyproject.toml` 这类）
- ❌ 不同 slug 之间不共享文件
- ✅ 需要在多个笼子之间共享的东西，自己开 `workspace/shared/`
  （FCoP 给这个 slug 留了保留字）

---

## 你怎么用 FCoP：只说人话

**先把最重要的说清楚**：FCoP 有 22 个工具——**全是给 Agent 用的，
不是给你用的**。你从头到尾只说人话，Agent 负责翻译成工具调用。

```
你（ADMIN）        Agent（AI）           FCoP 工具箱
  说人话   ────→   听懂意图   ────→   调对应工具
                                           ↓
                                    落文件 / 建目录 / 查状态
```

你不用背任何工具名。下表是"**你说这句话，Agent 会做什么**"的常见映射
——只是让你知道"Agent 该做什么、没做就能看出来"，不是让你去记。

### 项目起手阶段

| 你说的话 | Agent 会调 | 结果 |
|---|---|---|
| （新会话开口第一句） | `fcop_report()` | Agent 先汇报项目状态，没初始化/没指派角色都会告诉你 |
| "初始化 Solo 项目" / "一个人做" | `init_solo(role_code="ME")` | 落 `fcop.json`、建目录、部署规则和信、建 `workspace/` |
| "初始化开发团队" / "我要个 4 人团队" | `init_project("dev-team")` 或 `create_custom_team(...)` | 同上，但是多角色 |
| "MCP 目录绑错了" / `fcop_report` 里看到 `C:\Users\xxx` | `set_project_dir("E:\\你的项目")` | 运行时重绑，不用改配置也不用重启 |
| "你是 PM" / "你是 ME" | （不调工具，Agent 记下身份） | 进入 Phase 3，可以开始干活 |

### 日常干活

| 你说的话 | Agent 会调 | 结果 |
|---|---|---|
| "做个 CSDN 搜索工具" / "新开一个做 XXX" | `new_workspace(slug="csdn-search", title="...")` | 建 `workspace/csdn-search/` 笼子，产物全进去 |
| "派个任务给 CODER" / "让 XXX 做 YYY" | `write_task(recipient="CODER", body="...")` | 落一份 `TASK-*-to-CODER.md` |
| "看看现在项目什么状态" | `get_team_status()` | 任务/回执/问题/工作区数量 + 最近活跃 |
| "有几个工作区？" / "做过几个东西了？" | `list_workspaces()` | 列所有 `workspace/<slug>/` 和创建时间 |
| "还有哪些任务没做？" | `list_tasks()` | 列 `tasks/` 下未归档任务 |
| "xxx 任务说了什么？" | `read_task("TASK-...")` | 读正文 |
| "问题单有啥" | `list_issues()` | 列 `issues/` |
| "xxx 任务做完了归档吧" | `archive_task("TASK-...")` | 移到 `log/` |
| "看看完成回执" | `list_reports()` / `read_report(...)` | 查 `reports/` |

### 救场 / 特殊情况

| 你说的话 | Agent 会调 | 结果 |
|---|---|---|
| "FCoP 这个规则我觉得不合理" | `drop_suggestion("...", "...")` | 反馈落到 `.fcop/proposals/`（协议不让你自己改规则文件） |
| "创建团队前先验下角色名合法吗" | `validate_team_config("MANAGER,CODER", "MANAGER")` | 不落盘预检，出错给建议 |
| "有哪些预设团队？" | `get_available_teams()` | 列 Solo / dev-team / media-team / mvp-team / qa-team |
| "升级团队文档到三层" / "切到 qa-team 的模板" | `deploy_role_templates(team="qa-team")` | 老文件归档到 `.fcop/migrations/<时间戳>/`，新三层模板落 `shared/` |
| "再给我看一眼说明书" | 读 `fcop://letter/zh` 或打开 `docs/agents/LETTER-TO-ADMIN.md` | 重读这封信 |

### 真正"你可能直接用到"的只有 2 个工具名

- **`fcop_report`**：新会话 Agent 没自动汇报时，你说"先汇报"或直接
  说"调 `fcop_report`"催它一下。
- **`set_project_dir`**：发现 MCP 绑错目录（`fcop_report` 输出的项目
  路径是 `C:\Users\xxx` 之类），你说"绑到 `E:\你的项目`"或直接说
  "调 `set_project_dir("...")`"。

**其他 20 个你从来不用背**。Agent 自己会挑。

### Agent 为什么知道该调哪个？

因为 FCoP 在三个地方**同时**告诉了 Agent"你说话→我调工具"的映射：

1. **MCP instructions**（Agent 启动必读）：内建了"ADMIN 说 X → 调 Y"
   的映射表
2. **每个工具的 docstring**（Agent 看得到）：写了具体调用时机
3. **`fcop-rules.mdc`**（`alwaysApply: true`）：规则级别规定了 Rule 0
   等硬要求

所以你只管说人话。Agent 没按预期做（比如该开 `workspace/` 却没开、
该汇报却没汇报），把这封信翻给它看一下对应那行，立刻纠正。

### 14 个资源（Agent 按需读，你完全不用管）

**核心资源**（随时可读）：

| 资源 URI | 给谁读 | 装什么 |
|---|---|---|
| `fcop://rules` | Agent | `fcop-rules.mdc` 原文 |
| `fcop://protocol` | Agent | `fcop-protocol.mdc` 原文 |
| `fcop://letter/zh` 或 `/en` | Agent 回头查 | 这封信 |
| `fcop://status` | Agent | 同 `get_team_status` |
| `fcop://config` | Agent | `fcop.json` 原文 |

**样本库**（0.5.4 起，三层团队模板，不用初始化就能看别的团队长什么样）：

| 资源 URI | 装什么 |
|---|---|
| `fcop://teams` | 4 套预设队索引（dev / media / mvp / qa） |
| `fcop://teams/{team}` | 某套团队的 `TEAM-README.md`（团队定位 + ADMIN 职责 + 流程） |
| `fcop://teams/{team}/TEAM-ROLES` | Layer 1 · 角色边界（中文） |
| `fcop://teams/{team}/TEAM-OPERATING-RULES` | Layer 2 · 运作规则（中文） |
| `fcop://teams/{team}/{role}` | Layer 3 · 单岗深度（中文，如 `.../dev-team/PM`） |
| `fcop://teams/{team}/{role}/en` | Layer 3 · 单岗深度（英文） |

> 任何 `.../{role}` 或 `.../TEAM-*` URI 结尾加 `/en` 都会拿到英文版。
> 旧的 `fcop://teams/{team}/PM-01` 风格路径仍能解析（回退到 `roles/PM.md`），
> 但新项目请用不带 `-01` 的简洁写法。

**你怎么用这些样本？——说人话就行**，不用记 URI：

- 「给我看 dev-team 的 PM 职责模板」→ Agent 读 `fcop://teams/dev-team/PM`
- 「dev-team 的角色边界写了什么」→ Agent 读 `fcop://teams/dev-team/TEAM-ROLES`
- 「media-team 怎么派任务」→ Agent 读 `fcop://teams/media-team/TEAM-OPERATING-RULES`
- 「我自建个 LEAD-DEV，参考哪套最像？」→ Agent 自己挑合适的样本给你
- 「所有预设有哪些？」→ Agent 读 `fcop://teams` 或调 `get_available_teams()`

### ⚠️ Cursor 的"点灰"开关：两个千万别灰

打开 Cursor 的 MCP 面板能看到这 22 个工具每个旁边有个开关。点一下
变灰 = 禁用。**其中这 2 个一灰你就惨了**：

- `fcop_report` —— 灰了 Rule 0 失效，Agent 新会话没法做第一步
- `set_project_dir` —— 灰了 MCP 绑错目录时你只能改 `mcp.json` + 重启

剩下的 20 个你用不到的可以灰——不过 Agent 突然少了工具会一脸懵，
**建议全开就好**。

---

## 四条必读规则（缩略版）

| # | 规则 | 一句话 |
|---|---|---|
| 0.a | 落文件 | 聊天里的话没落成文件 = 没发生 |
| 0.b | 多角色制衡 | 不允许一个 AI 独自完成决策到执行 |
| **0.c** | **只落真话** | **不捏造、不臆断、引用必带出处** |
| 1 | UNBOUND | Agent 新会话先调 `fcop_report()`，等你指派身份 |

完整 9 条在 `.cursor/rules/fcop-rules.mdc`（Agent 会自动读）。
协议解释（命名、YAML、目录、巡检、0.c 的出处格式等）在
`.cursor/rules/fcop-protocol.mdc`。

---

## 升级 fcop（0.5.3 起已自动化）

FCoP 工具箱（`fcop` Python 包）会有版本更新。从 0.5.3 开始你什么都不用记：

**每次新会话开始时，Agent 跑的 `fcop_report()` 会自动在末尾告诉你有没有新版。**

长这样：

```
📦 fcop 有新版可用：0.5.4 → 0.5.5

- Agent 可用：调 upgrade_fcop() 工具（一键升级 + 提示重启 Cursor）
- 终端可用：pip install --upgrade fcop（升完请完全关掉 Cursor 再打开）
```

看到横幅，你有两种升级方式：

### 方式 1：让 Agent 自己升（省事）

一句话：

> 升级 fcop

Agent 会调 `upgrade_fcop()`，用它自己那个 Python 跑 `pip install --upgrade fcop`，告诉你升完的版本号，提醒你重启 Cursor。

### 方式 2：自己在终端跑（也行）

```powershell
pip install --upgrade fcop
```

然后完全关掉 Cursor 再开。**Windows 任务管理器里 kill 所有 `Cursor.exe` 进程**——光关窗口后台还有进程，MCP 不会重新加载。

### 要查"现在有没有新版"

一句话：

> fcop 有新版吗？

Agent 会调 `check_update()`——绕过 24h 缓存，直接问一次 PyPI。

### ⚠️ 重要提醒

- 升完**必须重启 Cursor**——不重启当前 MCP 还是旧版
- 不要让 Agent 手改 `.cursor/rules/*.mdc` 或 `fcop.json` 里的版本字段——那不是升级，是破坏协议
- 横幅 24 小时刷新一次（避免每次开会话都查 PyPI）；离线时静默跳过

---

## 不满意怎么办

- 想看完整规则 → 让 Agent 读 `fcop://rules` 或 `fcop://protocol`
- 对协议本身有意见 → 让 Agent 调 `drop_suggestion("...", "...")`，
  反馈落到 `.fcop/proposals/`，不污染协作目录
- 想换模板 → 一句话："用 `{team}` 重新初始化"
- 又想看这封信 → `fcop://letter/zh` 或 `docs/agents/LETTER-TO-ADMIN.md`

欢迎上岗。

— **FCoP**
