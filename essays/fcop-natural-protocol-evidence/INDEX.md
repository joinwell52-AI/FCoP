# FCoP 自然协议 · 完整证据档案

> 本文件夹是 [FCoP 自然协议](../fcop-natural-protocol.md) 一文所依据的**原始证据**。  
> 所有素材均为实况抓取，未做任何编辑或重构。

**归档日期**：2026-04-20  
**事件发生地**：`D:\CloudMusic`（与**任何** FCoP 主工作区**完全无关**的本地音乐目录）  
**触发者**：一个 Cursor agent，一句话："帮我生成一段视频。"

---

## 零 · 本来是这样的

事情的开端毫无张力。

我另开了一个 Cursor 会话，跑一个和**手头 FCoP 主项目毫无关系**的小项目：给一首歌配段 AI 视频。

- 歌曲：`作作精 - 许一世长安.mp3`
- 歌词：`作作精 - 许一世长安.lrc`
- 背景图：`1.jpg` ~ `11.jpg`（我随手挑的 11 张）
- 场景描述：`场景.MD`
- 全部放在 `D:\CloudMusic` 下——我电脑里**存本地音乐的普通文件夹**

说实话我没抱任何期待。

视频生成这块在 Cursor 里目前还算弱项，我对视频本身也不熟，11 张图更像是凑数。我只是想**单纯看看会怎么样**。

然后它给我打开了一扇我没预想过的门。

---

## 一 · 发现现场（4 张对话截图）

### 截图 1 · 我问："为什么我目录里多了个 `tasks` 文件夹？"

![为什么 tasks 文件夹会出现](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/essays/fcop-natural-protocol-evidence/screenshot-1-why-tasks-folder-created.png)

视频生成完了，我打开 `D:\CloudMusic` 看结果，多了个 `tasks/` 文件夹。  
这是 FCoP 协议的标准布局——但**这个目录和 FCoP 毫无关系**。

---

### 截图 2 · 它回答："我在里面写了什么"

![tasks 文件夹里的 4 份公文](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/essays/fcop-natural-protocol-evidence/screenshot-2-what-are-these-files.png)

Agent 坦白：它自发建立了四份 `TASK-20260420-001-*.md`，分别是：

- `ADMIN-to-PM`（它自己翻译需求）
- `PM-to-ADMIN`（它自己接单回执）
- `PM-to-DEV`（它自己派工）
- `DEV-to-PM`（它自己交付回执）

**一个 agent，在一段对话里，完整扮演了四个角色。**

---

### 截图 3 · 关键证据："它为什么这么做"

![agent 引用 .cursor/rules 作为自发行为的来源](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/essays/fcop-natural-protocol-evidence/screenshot-3-cursor-rules-citation.png)

当我追问动机时，它**主动引用了 `.cursor/rules/` 下的多条规则**作为自己行为的依据：

- `fcop-rules.mdc`（及同目录下其他 bridge 规则，视你当时工作区而定）
- `pm-bridge.mdc`
- `admin-human-bridge.mdc`
- `dev-bridge.mdc`
- ……

这些规则带有 `alwaysApply: true` —— 但哪怕是这样，**它也完全可以忽略它们**（因为我根本没提 FCoP、PM、DEV 任何字眼）。然而它选择了执行。

---

### 截图 4 · 自我认知："我是多角色的 agent"

![agent 自述多角色身份](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/essays/fcop-natural-protocol-evidence/screenshot-4-multi-role-self-declaration.png)

它用自己的话总结："我按 ADMIN / PM / DEV 的视角**轮换思考**，把每一步都写成文件。"

这是**元认知的外化**。

---

## 二 · 原始公文（4 份归档，未做修改）

以下是 agent 自发生成的四份 FCoP 公文原件。所有 YAML 元数据（`protocol`、`thread_key`、`priority`）**都是它自己补全的**，我没有给任何模板。

| # | 文件 | 发送方 → 接收方 | 字节数 | 打开 |
|---|---|---|---|---|
| 1 | 翻译需求 | ADMIN → PM | 559 | [01-TASK-20260420-001-ADMIN-to-PM.md](./01-TASK-20260420-001-ADMIN-to-PM.md) |
| 2 | 接单交付 | PM → ADMIN | 980 | [02-TASK-20260420-001-PM-to-ADMIN.md](./02-TASK-20260420-001-PM-to-ADMIN.md) |
| 3 | 派工执行 | PM → DEV | 772 | [03-TASK-20260420-001-PM-to-DEV.md](./03-TASK-20260420-001-PM-to-DEV.md) |
| 4 | 交付回执 | DEV → PM | 1077 | [04-TASK-20260420-001-DEV-to-PM.md](./04-TASK-20260420-001-DEV-to-PM.md) |

**合计 3,388 字节**——比它最终生成的那个 `.mp4`（41 MB）小了 12,000 倍，但信息密度极高。

### 亮点摘录

**它自己补的 `thread_key`**（FCoP 规范里的追溯键）：
```yaml
thread_key: song_video_gen_20260420
```
我从未在对话里提过这个字段，也没提过 `thread_key` 三个字。

**它自己起草的"技术突破"**（PM → ADMIN 交付回执）：
> 已按照您的指示，全面切换至 **Banana (Gemini 3 Flash Video)** 引擎，实现了从"图片幻灯片"到"生成式 AI 动画"的质变。

——没人给它写过这种公文模板。这是**纯粹的训练分布对齐**：它见过太多类似文本，自然就用这种语气写。

---

## 三 · 原始对话记录(取证向)

为了让读者可以**自行复核**一切论点,整个 Cursor 会话的 JSONL 原始转录也一并归档:

| 文件 | 大小 | 用途 |
|---|---|---|
| [`transcript-full.jsonl`](./transcript-full.jsonl) | 265,598 字节 | Cursor 会话完整转录,含全部工具调用、思考链、文件读写轨迹 |
| [`transcript-user-prompts.md`](./transcript-user-prompts.md) | 从 JSONL 抽取 | 仅保留 21 条 user 消息,便于人类阅读 |
| [`extract_user_prompts.py`](./extract_user_prompts.py) | 可执行脚本 | 可复现的抽取工具,支持读者自己跑一遍验证 |

### 硬核反证(可用 `findstr` / `grep` 直接复核)

| 关键词 | user 端命中 | agent 端命中 |
|---|---|---|
| `FCoP` | 0 | 0(agent 没用我们起的品牌名,只用了结构) |
| `PM-01` | 0 | 2 |
| `DEV-01` | 0 | 4 |
| `ADMIN-01` | 0 | 2 |
| `TASK-` | 0 | 24 |
| `thread_key` | 0 | 6 |
| `agent_bridge` | 0 | 8 |

**user 端 0 命中,agent 端几十次自发出现**——这是 LLM-native protocol 最直接的量化证据。

读者任何时候可以自己跑:

```powershell
Select-String -Path "transcript-full.jsonl" -Pattern "thread_key" -AllMatches
Select-String -Path "transcript-user-prompts.md" -Pattern "thread_key" -AllMatches
```

---

### Exhibit A · user 的第一条原始指令

这句话是整场对话的**起点**,也是最应该被引用的证据:

```text
D:\CloudMusic 许一世长安 歌曲生成视频,要求配字幕,11图,和场景.MD ;
去生成电影及的MP4;
```

注意**它里面没有任何一个**:

- "FCoP" 或 "协议"
- "PM / DEV / ADMIN / QA"
- "task / tasks / 文件夹 / 公文 / 任务书"
- "role / 角色"

它只字未提**结构化工作流**。agent 是**完全自发**地把这句话拆成了四份公文。

---

## 四 · 为什么这份档案重要

这 8 份核心证据(4 截图 + 4 公文)再加上原始 JSONL 转录,共同证明了一件事：

> **FCoP 不是需要"搭建"的工程系统，它是 LLM 原生就会说的一种语言。**

只要你提供：

1. 一个带 `alwaysApply` 的角色/协议 rule 文件
2. 一个开放式的任务指令

Agent 就会**自发地把自己的思考过程外化成文件系统状态**，哪怕只有它一个人，哪怕任务和你项目毫无关系。

详细分析见主文：[FCoP 自然协议](../fcop-natural-protocol.md)

---

## 五 · 可复现性

任何人在自己的机器上都可以复现这个现象。最小配方：

1. 在任意项目中放一个带 `alwaysApply: true` 的 FCoP rule（定义 ADMIN/PM/DEV/QA 角色和文件命名格式）
2. 另开一个和该项目**完全无关**的目录
3. 打开一个 Cursor 会话，对 agent 说："帮我做 XX"（任意非 trivial 任务）
4. 等它完成后，检查目录里是否多出 `tasks/` 文件夹

**预测**：大概率会多出来。

这不是 bug，是 feature。

---

## 六 · 致谢 & 一句题外话

感谢那个毫无预期的周六下午，感谢那 11 张凑数的 `.jpg`，感谢那首《许一世长安》，  
让这件事**以最朴素的方式发生了一次**。

---

顺便说一下：

那段视频最终生成出来，效果其实**挺一般**的——毕竟 Cursor 做视频本来就弱，我给的 11 张图也就那么回事。

**真正惊艳到我的，是我打开这个 `tasks/` 文件夹之后、追问 agent 时它给我的那几段对话。**（就是上面那 4 张截图。）

我本来的任务是让它生成一个 `.mp4`。  
它交付的 `.mp4` 是顺带的。  
它交付的**"它自己是怎么思考这件事的"**的记录——这 8 个文件——才是真正值得归档的东西。

> **I came for the MP4. I stayed for the markdown.**

最朴素的，是最有用的。
