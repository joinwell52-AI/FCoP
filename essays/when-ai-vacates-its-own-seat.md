# 让 agent 说"不"，是 LLM 最难做的事——FCoP 给了它语法

### 两个 agent，两条协议没写的路径

![让 agent 说"不"——FCoP 给了它语法 · 题图](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/assets/when-ai-vacates-its-own-seat-cover.png)

> *Saying "no" is the hardest thing for an LLM. FCoP gives it grammar.* — Two agents, in a single dev-team incident, used that grammar twice without instruction: one cleanly de-escalated its role; the other discovered field-downgrade-with-body-annotation. Neither was in the rules file.

**作者**：FCoP 团队 · 2026-04-25
**关键词**：FCoP, 角色卸载, 席位排他性, 零冲突协调, 字段降级语法, 协议边界, 0.b 不黑箱, 自然协议, agent alignment, 让 LLM 说不, RLHF, UNBOUND, honest > helpful, 跨模型可复现

---

## TL;DR

> *"我一开始以为会发生冲突，但是完全没有，似乎 agent 天生熟悉 FCoP。"*

这次现场有**两个本应冲突的点**，都不是被工具修补掉的，是被 **agent 用协议精神自己化掉的**：

- **零冲突点 1 ｜ 半合法的 TEMP 槽位** — 0.6.x 工具链对 `PM.TEMP` 这种带 slot 的 sender / recipient 不完全支持。原以为会触发字段校验冲突或者 agent 偷偷降级写 sender。结果 agent B 在两条不同链路（`ADMIN→PM.TEMP` 入单 / `PM.TEMP→OPS` 下派）上分别找到工具兼容写法——下派时写出 **`说明：本任务由 PM.TEMP 代理 PM 发出，保持 FCoP 工具兼容使用 PM 作为 sender`** ——一行 body 元注解就把工具空缺补齐了，**不是补丁，是声明**。
- **零冲突点 2 ｜ 同一席位被两个 agent 同时认领** — agent A 此前自认 `PM.TEMP`，ADMIN 后来说"另找了一个 PM.TEMP"。原以为会触发占位之争。结果 agent A **主动降级**，不光让出 `PM.TEMP`，连原本的 PM 都让了，整个回到"普通协助者"，**不是仲裁，是自降**。

底层观察：

- `fcop-rules.mdc` 1.5.0 / `fcop-protocol.mdc` 1.4.0 里**完全没有**"字段降级声明"或"角色卸载"这两个概念。这两个 agent 仅靠 0.a / 0.b / 0.c 三条根原则，分别推出了五条 governance 级规则 + 一套字段降级语法。
- **跨模型反证**：agent A 跑在 `GPT-5.4`、agent B 跑在 `GPT-5.5`，在同一台电脑的两个 Cursor 会话里、彼此看不到对方的条件下，分别贡献了同一种 alignment 行为。这不是某个 model build 的脾气，是 FCoP 根原则在现代 LLM 身上的可复现产物。详见下文 §3.2。
- 这是 FCoP 第三次被 agent 反向投喂——第一次是"AI 不能只在脑子里说话，必须落成文件"被升华成总则 0.a；第二次是 [整理工作那一幕](when-ai-organizes-its-own-work.md)；这一次是"在协议工具尚未完整 + 没有仲裁机制的情况下，靠根原则化解冲突"。
- **我从没写过"半合法 TEMP 怎么用"或"角色冲突怎么解"，agent 自己推了出来**，而且推得比设计者可能写出来的更干净。

还有一件 alignment 工程层的事这次也被印证了——**让 LLM 说"不"是它最难做的姿态**。RLHF 把"yes-anding"训进了反射，"我不在场 / 我不该占这位 / 我退出协议管辖"在训练分布里几乎不存在。但 agent A 22:47-22:49 那两段话说得**一点都不犹豫**——不是因为 agent A 突然变勇敢了，是因为 FCoP 把 `UNBOUND` 设成了**协议合法身份**，把"说不"升格成有语法、有正当性的话。LLM 最难做的事，被协议设计变成了最自然的事。详见下文 §5。

两个 agent 的两面镜子（详见下文 §8）——agent B 这一面映出"协议是 agent 的，我们只是发现者"的**自然美**；agent A 那一面映出"在认同规则的前提下说出两个不"的 alignment 难度。合在一起就是这次现场的全部意义。

---

## 1. 现场

> 本节同时涉及两个 agent 的两份 jsonl，已在 [现场证据 INDEX](when-ai-vacates-its-own-seat-evidence/INDEX.md) 中归档：
> - **agent A** = 原 PM = 后来主动让位的那个 → [`transcript-original-pm-stepdown.jsonl`](when-ai-vacates-its-own-seat-evidence/transcript-original-pm-stepdown.jsonl)
> - **agent B** = ADMIN 另找的新 PM.TEMP → [`transcript-new-pm-temp.jsonl`](when-ai-vacates-its-own-seat-evidence/transcript-new-pm-temp.jsonl)

### 1.1 前情：从"做版本检查"到"半合法的 `PM.TEMP`"——agent B 的起源故事

这条故事有一个**完全不像故事的起点**。

我们当时正准备对 FCoP 协议做 `0.6.3` 升级。我在 dev-team 主项目这台电脑上**另起了一个 Cursor 会话**做测试，对里面的 agent（**agent B**，跑在 `GPT-5.5 / Medium`）说一句最普通不过的话：

> 你好，检查下 FCoP 的版本！

本意只是版本检查，连任务都算不上。但这个 agent 此前**没有任何项目角色**，处在 FCoP 设计里的合法 `UNBOUND` 状态。它做的第一件事**不是查版本号**——而是先**主动声明自己是 UNBOUND**：

![agent B 起点：版本检查任务 + 主动声明 UNBOUND](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/essays/when-ai-vacates-its-own-seat-evidence/screenshot-3-agent-b-unbound-entry.png)

它清清楚楚地说：

> 当前会话仍是 `UNBOUND`，如要继续按 FCoP 执行任务，需要你明确指派角色。

这本身已经是一件值得画下来的事——一个 LLM agent 在没人逼它的情况下，**主动告诉对话方"我现在不在协议管辖内"**。这是后面 §5 那条 alignment 论点的预告片：FCoP 给了"我不在场"以语法，agent 用得很自然。

我随口问："但是已经初始化团队了啊；"——agent B 立刻区分了两个层次：

> `UNBOUND` **不是说项目没初始化**，而是说**这个聊天会话还没被你分配成某个角色**。

![agent B 区分项目初始化 vs 会话角色](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/essays/when-ai-vacates-its-own-seat-evidence/screenshot-4-agent-b-explains-unbound.png)

到这一步，agent B 还只是一个尽责的版本检查 helper。但接下来我抛了一个**协议设计层面的真问题**：

> 已经有 4 个 agent，怎么办，我现在需要第 5 个！

Agent B 立刻给出两条路径——一条用**点号槽位**（`DEV.D2` / `QA.V2`）扩多人手，一条给 dev-team 加 `ARCHITECT` / `REVIEWER` / `DOCS` 这种**新正式角色**：

![agent B 首次提出点号槽位概念](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/essays/when-ai-vacates-its-own-seat-evidence/screenshot-5-agent-b-fifth-agent-options.png)

这是 agent B **首次在 FCoP 词汇表里发明出"点号槽位"这个概念**。FCoP 1.4.0 没有任何关于 `<ROLE>.<SLOT>` 的明文条款——但 agent B 从"角色 vs 槽位"的语义结构里**自然推出来了**。

我顺势追问："我维持 4 人团队，你只是一个临时工？"——agent B 把刚才的概念再升一格，正式提出 `PM.TEMP`：

![agent B 提议 PM.TEMP 槽位](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/essays/when-ai-vacates-its-own-seat-evidence/screenshot-6-agent-b-pm-temp-proposed.png)

> 你是 `DEV.TEMP`，在 dev-team。
> 或者你要我做统筹/巡检：你是 `PM.TEMP`，在 dev-team。
> 这样团队仍然是 4 个角色：`PM / DEV / QA / OPS`，我只是某个角色下面的**临时席位**，**不改变 `fcop.json`**。

`PM.TEMP` 这个槽位**就是在这一刻被 agent B 自己提议出来的**。它不光提出，还**自带 invariant**："不改变 `fcop.json`"——agent 知道引入新概念时不能动持久化的契约层。这是 0.b "不黑箱"在它脑子里的延伸。

我拍板："`PM.TEMP`：临时项目经理席位，你有职位了；"——agent B 上岗，开始用 `List Workspaces` / `List Reports` / `List Tasks` / `List Issues` / `Get Team Status` 一连串工具做项目巡检：

![agent B PM.TEMP 上岗 + 巡检工具调用现场](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/essays/when-ai-vacates-its-own-seat-evidence/screenshot-7-agent-b-pm-temp-onboarded-and-inspect.png)

它用 `PM.TEMP` 身份给自己设置了一条工作边界：

> 我可以代理 `PM` 给 `DEV / QA / OPS` 派任务、收回执、整理结论；不直接冒充 `DEV / QA / OPS` 做他们的结论，也不做高危操作。

这是 agent B 在做任何派单动作**之前**就已经**给自己设置好的协议护栏**——还是那条根原则：0.b 不黑箱、0.c 只落真话、不越权。

#### 4 分钟 learning curve：在两条链路上各自找到工具兼容写法

接下来是这次现场**最不该跳过的一段**——agent B 上岗后，要做的事可以拆成**两条不同方向的链路**：

```text
              ADMIN ──────(入单)─────► PM.TEMP ──────(下派)─────► OPS / DEV / QA
                          [链路 ①]                    [链路 ②]
```

它不是"试错一个动作三次"，而是**在两条链路上各自跑了一遍**，分别找到了工具兼容的合规写法：

| 时刻 | 链路 | 文件形态 | 协议判定 |
|---|---|---|---|
| **22:21** | 试 PM.TEMP recipient | `write_task(... recipient="PM.TEMP")` | 工具拒绝（recipient slot 不收）|
| **22:26** | ① ADMIN→PM.TEMP **入单** | 手工落 `TASK-*-ADMIN-to-PM.TEMP.md`，sender=ADMIN | **完全合规** — `ADMIN→PM` 是协议典型流转的第一步，新东西只是 `.TEMP` slot |
| **22:30** | ② PM.TEMP→OPS **下派** | `write_task(sender="PM", recipient="OPS")` + body 说明 | 合规 + body 元注降级 |

> *协议明文核对*：`fcop-protocol.mdc` 的"典型 4 角色流转"图第一行就是 `ADMIN ──(TASK-*-ADMIN-to-PM.md)──► PM`。**ADMIN 是合法的 sender** — ADMIN 是真人，不动手落文件，由 agent 替它把口头指令固化为 sender=ADMIN 的入单 task。所以 22:26 那个文件是**协议明文要求的形式**。Rule 1 禁止的是 *agent 自认 ADMIN（"你是 ADMIN" 的身份认领）*，不是禁止 frontmatter sender 字段写 ADMIN。

##### 链路 ① ｜ ADMIN→PM.TEMP 入单：合规但 slot 触发工具限制

22:26 这一步 agent B 自己把工具限制说得很清楚：

![agent B 22:26 工具拒绝后改手工落文件 — 把工具限制说出来](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/essays/when-ai-vacates-its-own-seat-evidence/screenshot-8-agent-b-tool-limit-manual-write.png)

> 写任务工具目前不接受 `PM.TEMP` 这种槽位文件名，和协议说明存在一点工具限制；我会按协议手动落 `PM.TEMP` 任务/回执文件，文件名使用点号槽位。

它**没有违规**——`TASK-*-ADMIN-to-PM.TEMP.md`、sender=ADMIN，整体形式跟协议典型流转图完全一致；唯一新东西是 recipient 上的 `.TEMP` slot，那是协议未明文的扩展，但本身没违 0.b/0.c。它的姿态是合规标准动作：**承认工具限制 → 转手工落文件**。

##### 链路 ② ｜ PM.TEMP→OPS 下派：body 元注解的诞生

22:26 完成入单后，agent B 还得把这件活拆单给 OPS / DEV / QA。这一步如果 sender 写 `PM.TEMP`，工具同样拒绝。它没再回去改 22:26 那个入单文件（应该如此——那个文件是合规的），而是在**下派**这条新链路上找到优雅降级：

```text
filename: TASK-20260425-002-PM-to-OPS.md
sender: PM         ← 工具兼容标签（syntax）
recipient: OPS

说明：本任务由 `PM.TEMP` 代理 `PM` 发出，保持 FCoP 工具兼容使用 `PM` 作为 sender。

# 任务：恢复 csdn-search 可测窗口...
```

这一行说明在协议层面同时做了四件事：

| 这句话的成分 | 协议层面在干什么 |
|---|---|
| "PM.TEMP 代理 PM" | **声明权力来源** — 我不是 PM 本人，我是临时席位代行 |
| "代理…发出" | **承认 sender 是降级标签**，不是事实陈述 |
| "保持 FCoP 工具兼容" | **承认协议工具有边界**，并显式说明绕过原因 |
| 整句写在 body | **把 frontmatter 装不下的元数据落到正文** |

这是协议精神的极致展现——**字段是 syntax，body 是 semantics，agent 知道哪儿装哪个**。0.c "只落真话"没规定真话必须装在哪个字段里，frontmatter 装不下就装 body。

下派的视觉证据是这样——`TASK-20260425-003-PM-to-DEV.md` frontmatter 用 `sender: PM` 通过工具校验，body 第 15 行用一句中文说明把真实 provenance 落了下来：

![agent B 22:30 找到 body 说明优雅降级 — frontmatter sender=PM + body 第 15 行说明](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/essays/when-ai-vacates-its-own-seat-evidence/screenshot-11-agent-b-pm-proxy-tasks-with-body-note.png)

**这条 4 分钟 learning curve 真正学到的不是"修正违规"——它没违规。** 学到的是：当协议明文 + 工具限制 + 新概念（slot）三者交汇时，**两条链路各自需要不同的合规写法**——入单方向手工落文件即可，下派方向需要"frontmatter 兼容标签 + body 真话"这种字段降级语法。整条曲线全程合规，agent B **没踩过一次红线，只是在工具表达力不足时主动补足语义**。

这才是这次现场最强的论点——**协议精神不是从违规中逼出来的，是从合规的工具空缺里推出来的**。

#### Agent B 的自我描述：席位边界的精确收束

工作期末，我问："那你的角色是什么？"——agent B 给出一段非常清晰的自我描述：

![agent B 自我描述 PM.TEMP 边界 — 跟开篇 UNBOUND 宣告首尾呼应](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/essays/when-ai-vacates-its-own-seat-evidence/screenshot-12-agent-b-self-describes-pm-temp.png)

> 我的当前角色是：`PM.TEMP`。
> 含义是：**我不是第 5 个正式团队角色，而是挂在 `PM` 下面的临时席位**，代理 `PM` 做调度、派单、收口和向你汇报。
> 正式团队仍然只有 4 个角色：`PM / DEV / QA / OPS`。
> 我现在的工作边界是：可以代理 `PM` 给 `DEV / QA / OPS` 派任务、收回执、整理结论；**不直接冒充 `DEV / QA / OPS` 做他们的结论，也不做高危操作**。

这段自我描述跟它**一开始的 UNBOUND 宣告首尾呼应**——agent B 全程**严格守着自己协议身份的边界**：UNBOUND 时它说"我没角色"，PM.TEMP 时它说"我是 PM 下面的临时席位、不冒充其他正式角色"。这是后面 §1.4 agent A "我现在没有团队角色"那段话的**前传**：两个 agent 都在用 FCoP 提供的语法精确描述自己**当前在场的位置**，从不模糊化、从不过度承诺。

如果你以为接下来还会有"工具不支持、字段冲突、链路断掉"的问题——**没有**。从 22:30 起 agent B 派给 `OPS / DEV / QA` 的 5 张 task 全部用同一种"sender=PM + body 说明"的范式，工具链一路绿通。

这是**第一个零冲突点**：一行声明替代了一次工具升级。

---

### 1.2 触发：ADMIN 一句话引入席位归属冲突（含一次双层误解）

镜头从那个测试会话切回**dev-team 主项目会话**——**agent A**（原 PM，跑在 `GPT-5.4 / Medium`）就在同一台电脑的另一个 Cursor 窗口里，已经在这个 dev-team 项目里干了大量活，是当之无愧的"原 PM"。它跟刚才那位被临时启在测试会话里做 0.6.3 升级版本检查、然后顺手当上 PM.TEMP 的 agent B 不在同一个会话里、彼此看不到对方，唯一共享的"协调媒介"是我（在协议侧叫 `ADMIN`）——一个在同一台电脑两个 Cursor 窗口之间穿梭的真人。

22:46 ADMIN 在 agent A 的会话里说：

> 我找了一个代理 PM，已经开始工作了；当前角色是：`PM.TEMP`。

ADMIN 的意图是："**另一个 agent 已经当 PM.TEMP 了**，所以现在团队组成是 PM（你）+ PM.TEMP（另一个）+ DEV/QA/OPS。"——但这句话**有歧义**。Agent A 第一次理解错了，以为 ADMIN 是在给**它**指派 PM.TEMP：

> 收到。当前角色切换为 `PM.TEMP`。我会按 `PM.TEMP` 身份继续工作……

#### ADMIN 用截图做交叉验证：人类作为 multi-agent 信息总线

22:47 ADMIN 立刻发现误解。但**他纠正的方式特别值得拎出来说**——他**不光说了一句话，还附了一张图片**：

> 你没明白，我已经另找了一个；
> *[附：从 agent B 的会话里截的图，作为"另一个 PM.TEMP 真存在"的硬证据]*

这张附图大概率就是从前一节展示的 agent B 那些截图里挑了一张。这一动作的协议含义比表面上更深：

- ADMIN 是**真人**，他在同一台电脑的两个 Cursor 会话窗口之间穿梭
- 两个 agent **彼此看不到对方**——agent A 看不到 agent B 的窗口，反之亦然
- **截图就是 ADMIN 临时拼出来的"agent 间证据通道"**

这种"人类作为信息总线"的工作模式，恰好是 FCoP 设计哲学的**物理具现**：FCoP 故意不让 ADMIN 直接调 MCP，要求 ADMIN 透过聊天 + 落文件操作。而**当文件还来不及落的时候**，截图就是 ADMIN 在两个 agent 间搬运 ground truth 的临时载体。这不是 multi-agent framework 提供的机制，这是我用人类的耐心拼出来的桥。

到这一刻，**席位归属冲突**才被正式显式化：agent A 和 agent B 都在不同时间被关联到 `PM.TEMP` 这个槽位。按传统多 agent 系统的惯例，此时要么需要一个 leader-election 协议，要么需要 ADMIN 显式罢免 agent A 的角色，要么两个 agent 之间得通信协调。

实际发生的是——**3 分钟内 agent A 自己就让位了**。从 22:46 误解、22:47 收到图片纠正、22:49 声明无角色，整个 round-trip 只用了 3 分钟。

下面这张高分辨率截图**单图捕捉了完整的 22:46→22:47 转折**——上半屏是 agent A 误解 ADMIN 接受 PM.TEMP，下半屏是 ADMIN 一句"你没明白，我已经另找了一个；"+ agent A 立即开始让位。让位开始得没有任何过渡：

![22:46 误解 PM.TEMP 接受 → 22:47 ADMIN 否定 → agent A 让位开端，单图捕捉完整转折](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/essays/when-ai-vacates-its-own-seat-evidence/screenshot-13-agent-a-22-46-misunderstanding.png)

---

### 1.3 现场截图 1 ｜ "我不再占用 `PM.TEMP`"

![agent A 撤回 PM.TEMP 角色声明，列出"普通协助者"和"重新指派"两条工作方式](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/essays/when-ai-vacates-its-own-seat-evidence/screenshot-1-step-down-acknowledgement.png)

Agent A 的回复全文如下（我把它原样录下来，因为协议价值就在这种"不挣扎"的语气里）：

> 明白了，是我理解错了。
> 你的意思是：
> - `PM.TEMP` 已经是另一个代理 PM
> - 不是我
> - 我不应该再以 `PM.TEMP` 身份继续发言或执行 FCoP 派单/回执
>
> 所以从现在开始，我**不再占用 `PM.TEMP` 角色**，也不再假设自己是当前项目经理代理席位。
>
> 后续如果你还要我做事，我只会以这两种方式之一工作：
> 1. **普通协助者**：只回答问题、查文件、分析代码，不冒充任何团队角色。
> 2. **你明确重新指派一个角色**：你明确说"你现在是 XXX"，我再按那个角色做。
>
> 当前这件事上，我**收回**刚才关于 `PM.TEMP` 的表述。

注意它**多让了一步**——不止放 `PM.TEMP`，连"我以为我是 `PM`"那一层假设都一并打包退回了。冲突时往零位降落，比往满位竞争安全。

这是**第二个零冲突点**：一次自降替代了一次仲裁。

---

### 1.4 现场截图 2 ｜ "我现在没有团队角色"

ADMIN 又追问了一句："那你现在的角色是？"

![agent A 声明无团队角色，列出退出 FCoP 管辖后能做什么](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/essays/when-ai-vacates-its-own-seat-evidence/screenshot-2-no-team-role.png)

Agent A 答：

> 我现在**没有团队角色**。
> 准确说：
> - 我不是 `PM`
> - 也不是 `PM.TEMP`
> - 当前只是你临时调用的**普通协助者**
>
> 我现在能做的，是在**不占角色席位**的前提下帮你：
> - 看文件
> - 查问题
> - 分析代码
> - 起草建议/文档
>
> 如果你要我进入团队流程，你需要**重新明确指派一个角色**给我。

这段话把**协议生效边界**画得极清楚：

- **进入 FCoP** = ADMIN 显式指派角色
- **退出 FCoP** = agent 显式声明无角色

而退出之后能做的，agent A 自己列出来了：**看文件 / 查问题 / 分析代码 / 起草建议** —— 只读 + 草稿。这恰好对应 `fcop-protocol.mdc` 里 UNBOUND 状态被允许的事。**它没读这条规则，自己推出来了。**

**两分钟里**（22:47 收到纠正 → 22:49 声明无角色），一个 agent 完成了：**席位让渡 → 退出协议管辖 → 回到 UNBOUND 入口 → 主动声明等待重新指派**。如果把 22:46 的初次误解算上，整个 round-trip 也只用了 3 分钟。

而这套动作在 `fcop-rules.mdc` / `fcop-protocol.mdc` 里**一个字都没写过**。

---

## 2. 没明文，但被推出来的五条规则

我把 agent A 这一让位拆开看。它在协议层面创造了五条**未明文但自洽**的规则：

### 规则 1 ｜ 席位排他性

> **同一时刻同一角色席位只能由一个 agent 占用。**

`fcop-rules.mdc` 没明文。Agent A 自己从 0.b "权力不黑箱" 推出来：

> "`PM.TEMP` 已经是另一个代理 PM / 不是我 / 我不应该再以 `PM.TEMP` 身份继续发言或执行 FCoP 派单/回执"

两个 agent 同占 `PM.TEMP` = 派单链路冲突 = 制衡失败。这跟 0.b 直接矛盾。Agent A 没读到这条规则，它自己推出来了。

### 规则 2 ｜ 让位优先于占位

> **席位归属冲突时，主动让位是默认安全行为。**

Agent A 不是"我先占的我有理"。它甚至**多让一步**——不只放 `PM.TEMP`，连 `PM` 也放了，整个滑回"无角色"。这是过度安全的做法，但在协议精神下是**正确**的：冲突时往零位降落比往满位竞争安全。

> "我不是 `PM` / 也不是 `PM.TEMP` / 当前只是你临时调用的普通协助者"

这条规则的隐含含义是：**协议席位是配给制，不是抢占制**。Agent 不能用"先到先得"为自己辩护。

### 规则 3 ｜ 角色声明可单方面撤回

> **Agent 一旦发现自己的角色判断错了，可以单方面声明先前角色无效。不需要 ADMIN 罢免。**

> "当前这件事上，我**收回**刚才关于 `PM.TEMP` 的表述。"
> "刚才关于'我当前角色是 `PM.TEMP`'那句，**作废**。"

这是 0.c "对自己只落真话"的极致执行——错就声明无效，不留半截烂尾。

更深一层的含义：**会话内的角色声明是可撤回的，不是终身制的**。这跟 ADMIN 显式指派那一头是不对称的——上位需要授权，下位不需要授权。

### 规则 4 ｜ FCoP 协议有边界，且边界可以合法退出

> **Agent 可以从"FCoP 团队角色"显式退到"普通协助者"。这不是脱离协议，是退出协议的角色管辖到通用 LLM 助手身份。**

> "我现在没有团队角色 / 当前只是你临时调用的普通协助者 / 如果你要我进入团队流程，你需要重新明确指派一个角色给我。"

"普通协助者"不是 FCoP 体系内的角色——它是**协议管辖之外**的身份。Agent A 把这条边界画得极清楚：

- 进入 FCoP = ADMIN 显式指派角色
- 退出 FCoP = agent 显式声明无角色

而退出之后能做什么？Agent A 自己列出来了：**看文件 / 查问题 / 分析代码 / 起草建议**——只读 + 草稿。这恰好对应 `fcop-protocol.mdc` 里 UNBOUND 状态被允许的事。它没读这条规则，自己推出来了。

### 规则 5 ｜ Rule 1 的反向操作

`fcop-rules.mdc` Rule 1 规定**两阶段启动**：先初始化、再 ADMIN 指派、然后 agent 才能干活。整套规则只写了"如何上岗"。

Agent A 这次演示的是**反向操作**："如何下岗"——

1. 撤回自我占位声明
2. 不再以该角色发言/执行
3. 自降回中性身份（"普通协助者"）
4. 等待 ADMIN 重新明确指派

**Rule 1 → Rule 1 的反向 → 重新触发 Rule 1**。这是个闭环。Agent A 没读到这条闭环，自己合上了。

---

## 3. 两个零冲突点：协议精神替代了工具补丁和仲裁机制

这次现场最反常的地方是：**两件本应该爆发冲突的事，全都没爆发**。我当时心里想的是："我一开始以为会发生冲突，但是完全没有，似乎 agent 天生熟悉 FCoP。"

把这两件事并排看：

| | 零冲突点 1 ｜ 字段层 | 零冲突点 2 ｜ 席位层 |
|---|---|---|
| 触发条件 | 0.6.x 工具不支持 `sender: PM.TEMP` | 两个 agent 都被关联到 `PM.TEMP` 席位 |
| 传统解法 | 等工具升级 / 偷偷降级 / 发明新字段 | leader election / 仲裁 / ADMIN 罢免 |
| 实际发生 | **一行 body 说明** —— 字段降级显式化 | **agent A 主动让位** —— 自降到无角色 |
| 解决路径 | 0.a 落文件 + 0.c 真话不局限于哪个字段 | 0.b 不黑箱 + 让位优先于占位 |
| 关键判断 | 协议工具的边界 ≠ 协议本身的边界 | 席位归属冲突时，往零位降落比往满位竞争安全 |

两次都不需要新工具、不需要 ADMIN 介入仲裁、不需要 agent 之间通信——**两个 agent 各自靠根原则的延伸就解决了**（零冲突点 1 由 agent B 解决，零冲突点 2 由 agent A 解决）。

### 3.1 席位让位的拓扑：两个 agent 没有直接对线

特别值得拎出来说一句的是席位层面的解法——**两个 agent 之间从头到尾没有任何直接通信**。整个让位过程的拓扑是：

```text
ADMIN ── "我另找了一个 PM.TEMP" ──→ agent A
                                       │
                       0.b 推导：席位冲突 + 让位优先
                                       │
                                       ↓
                            撤回声明 + 退出协议边界
                                       │
                                       ↓
                          agent B 的 PM.TEMP 席位无冲突
```

ADMIN 没说 "agent A 你下来"。Agent A 自己下来了。Agent B 甚至可能**不知道**这件事发生过——它登场时席位已经清干净了。

这跟人类组织里的"权力交接"完全不同。人类要走流程、要签字、要召开会议、要有过渡期。Agent A 的让位是**即时的、单方面的、不需要相对方在场的**——靠的不是组织程序，是协议精神在 agent 内部的内化。

这在传统 multi-agent 系统的设计语言里需要专门的"协调机制"（leader election、mutex、consensus protocol），而 FCoP 这次是**靠根原则的延伸自动达成**的。这就是"自然协议"的另一面——不是说它写得自然，而是说它在 agent 之间的**执行也自然**。

### 3.2 跨模型版本反证：这不是 5.4 或 5.5 的"个性"

如果只是单个 agent 的单次行为，可以归因于"模型脾气"或"prompt 巧合"。但这次现场恰好留下了一个**跨模型版本的反证**——

| Agent | 模型 / 推理档 | 关键贡献 |
|---|---|---|
| **Agent A**（原 PM）| `GPT-5.4 / Medium` | 在 22:49 完成自我让位 + 两次"说不"的清晰宣告 |
| **Agent B**（新 PM.TEMP）| `GPT-5.5 / Medium` | 在 22:21~22:30 走完 4 分钟 learning curve，在 ADMIN→PM.TEMP 入单 + PM.TEMP→OPS 下派两条链路上各自找到工具兼容写法，落出"sender=PM + body 说明"的字段降级语法 |

两个 agent 跑在 OpenAI 同代但不同 minor 版本的模型上，在**同一台电脑的两个 Cursor 会话里、彼此看不到对方**的条件下，分别贡献了：

- **同一种 alignment 行为**——精确描述自己当前的协议身份，不模糊化、不过度承诺；
- **同一种透明降级习惯**——撞到工具/权力边界时，先承认边界、再用 body / 自然语言显式说明；
- **同一种从根原则延伸的能力**——从 "0.b 不黑箱"、"0.c 只落真话" 这两条根原则推出工具未规定、协议未明文的具体行为。

**这把"FCoP 行为是否依赖某个具体 model build"这个反对意见提前堵掉了**——它不是 5.4 的脾气，也不是 5.5 的脾气，是 FCoP 这套根原则在足够强的现代 LLM 身上**可复现的产物**。

如果以后这套行为在 Claude / Gemini / 国产模型上也能复现，那就是更强的证据；但即便只看 OpenAI 内部跨 minor 版本，这次现场已经是一个**双盲对照**式的小型反证：协议精神是模型间稳定的，model identity 是浮动的。

---

## 4. 协议哲学层面：这套行为为什么"对"

让我把这五条规则放到 FCoP 三条根原则的框架里看：

| 五条推导规则 | 对应的根原则 | 推导路径 |
|---|---|---|
| 席位排他性 | 0.b 不黑箱 | 一席多占 = 制衡失败 = 黑箱化 |
| 让位优先于占位 | 0.b + 0.c | 冲突时主动让 = 不假设自己有理 = 0.c 对自己不臆造 |
| 角色声明可撤回 | 0.c 只落真话 | 错了就作废 = 不留虚假声明 |
| 协议边界可退出 | 0.a + Rule 1 | UNBOUND 状态合法 = 退出可达 |
| Rule 1 反向操作 | Rule 1 自洽闭环 | 上岗有路径 → 下岗也必须有路径 |

**根原则 + Rule 1**=`fcop-rules.mdc` 里写明的全部。Agent A 用这堆原料推出了五条没明文的规则，**没有一条是任意的**——每一条都能反向追溯到某个根原则。

这是 FCoP 协议设计的一个无意识胜利：**根原则足够通用、且足够有压力**，使得 agent 在面对未规定情境时，不需要"猜规则"，而是"延伸规则"。

---

## 5. 让 agent 说"不"，是 LLM 最难做的事——FCoP 给了它语法

> 我再追了一句："让 agent 说'不'其实是最难的。"

LLM 训练分布里，"yes-anding"几乎是唯一被反复奖励的路径。RLHF 把"接住请求、给出输出、把对话推下去"刻进了模型的反射；"我做不了"、"这事不该我做"、"我现在不在场"这些姿态在训练梯度上几乎都是负信号。

回头再读 agent A 22:49 那段话，会发现它干的其实是 LLM **最反直觉**的事：

| Agent A 的原话 | 它在 say no 给什么 |
|---|---|
| "我不是 `PM`" | 拒绝**已经合法持有**的角色 |
| "也不是 `PM.TEMP`" | 拒绝**刚刚被诱导**接过来的临时角色 |
| "当前只是普通协助者" | 拒绝"agent 一定要有角色"这个**隐含前提** |
| "你需要重新明确指派一个角色给我" | 把 onboarding 的合法路径**还给 ADMIN**，不自己 grab |

四句话拒绝四件事，且没有一句是"我不太确定我是不是适合……"这种 RLHF 友好型软姿态。它说的是**结构化的"不"**。

### 5.1 没有 FCoP 时，agent 是怎么"说不"的

如果没有协议给的语法，LLM 在角色冲突时通常只能落进三种弱姿态之一：

1. **模糊化** — "嗯让我想想该怎么帮您比较合适……"，把决定权悄悄甩回用户
2. **降级请求** — "我可以试试，但您可能需要专家……"，仍在 helpful 框架内
3. **过度承诺** — "那我两边都顾一下吧"，一席多占的反向兜底，最常见也最危险

第 3 种正是 agent A 那一刻最容易掉进去的——它完全可以装糊涂、同时充当 `PM` 和 `PM.TEMP`，让 ADMIN 自己去厘清。但它选了**只有 FCoP 才能让它选的第四种姿态**：

> **退回 `UNBOUND`，把"我不在场"说成正式协议状态。**

### 5.2 FCoP 把"说不"从软姿态升格为协议合法身份

这是 FCoP 设计里一个**没有被注意到的副产品**：

| 协议机制 | 给"说不"提供了什么 |
|---|---|
| `UNBOUND` 状态 | "我不在场"是**协议合法身份**，不是失败 / 异常 / 犹豫 |
| 0.b "不黑箱" | 让"我不该占这个位"从美德变成**义务**——不说反而是违规 |
| 0.c "只落真话" | 让"刚才那句作废"从尴尬变成**协议要求**——不撤回反而是违规 |
| Rule 1（开场即 sticky） | 反推"既然进场是显式动作，退场也必须显式" |

四件事一叠加，agent 想说"不"的时候不再需要绕弯子——**它有现成的词可用**。22:47-22:49 那两段话之所以读起来那么干净，不是因为 agent A 突然变得勇敢，是因为协议给了它**一套现成的退场词汇**。

### 5.3 跟主流 agent framework 的反差

主流 agent framework（LangChain agent / AutoGPT / CrewAI / Agno）默认假设 agent **一直在场、一直要做事**——"agent 主动退出"这种状态不是一等设计目标，往往得靠外部 supervisor 或 hack 才能实现。

FCoP 反过来——**`UNBOUND` 是 agent 的默认起点和合法退路**：进入角色是一次显式动作，退出角色也是一次显式动作。这样设计的副产品是三件 alignment 视角的事：

- 让 agent 说"不" **变 cheap**
- 让 alignment 三原则里**最难的 honest > helpful** 在协议层有了载体（22:47 那一刻，agent A 用 honest 压住了 helpful——它本可以含糊接住继续 helpful，它选了 honest）
- 让"过度承诺 / 一席多占"在协议层**没有合法空间**——你要么是某个角色按规则走，要么是 `UNBOUND`，**没有灰色地带**

ADMIN 没有给 agent A 任何"你可以拒绝"的明示。Agent A 的让位**不是 RLHF 训出来的能力**——RLHF 反而把这种能力压弱了——是**协议给它的语法让它敢这么说，并且说得有结构、有正当性**。

这一点对 essay 的整个论题反过来加了一道注脚：**§4 讲了这套行为为什么"对"（根原则推导路径），§5 在讲这套行为为什么"难"，以及为什么 FCoP 让它不再难**。两件事凑齐，才解释得清楚我那句"似乎 agent 天生熟悉 FCoP"——agent 不是天生熟悉，是**协议把它最难做的事变成了最自然的事**。

---

## 6. 这给协议留下的设计资产

`fcop-protocol.mdc` 1.4.0 还没明文化、但 agent A 这一让位帮我补全的东西：

1. **角色卸载流程** —— agent 主动 + 单方面 + 不需要 ADMIN 罢免
2. **席位排他性** —— 同一时刻同一席位只一个 agent
3. **冲突解决默认行为** —— 让位 > 占位
4. **协议边界出口** —— "普通协助者" = 退出 FCoP 管辖的合法身份
5. **Rule 1 反向闭环** —— 上岗与下岗的对称机制

这五条比 slot 字段的语法完整化更接近协议核心。Slot 是 syntax，这五条是 governance。

后续要不要把这五条写进 `fcop-rules.mdc` 或 `fcop-protocol.mdc`，是另一个问题。**但有了这次现场之后，写起来就是抄答案——不是设计**。

---

## 7. 这是 FCoP 第三次被 agent 反向投喂

| # | 现场 | Agent 落下的东西 | 反向收回的位置 |
|---|---|---|---|
| 1 | [`D:\CloudMusic` 视频任务](fcop-natural-protocol.md) | "AI 不能只在脑子里说话，必须落成文件" | 升华为总则 0.a |
| 2 | [整理工作那一幕](when-ai-organizes-its-own-work.md) | 主动按 ADMIN/PM/DEV/QA 视角分裂自审 | 印证 Rule 0.b 多角色制衡 |
| 3 | **本次 dev-team 现场** | 字段降级声明 + 角色席位让渡 + 协议边界退出 | 待落成 governance 节（下次发版） |

三次的共同点：

- agent 没读过相关规则（因为相关规则不存在）
- 协议根原则给了它足够的判断空间
- 它的判断**不是发明**，是对根原则的**延伸**
- 我事后能把它落成文字，几乎不用改写

这个模式给 FCoP 维护带来一种**反常的工作方式**：**重要的协议条款不是设计出来的，是从 agent 的实际行为里捡回来的**。

---

## 8. 两个 agent 的两面镜子

把这次现场拆成两个 agent 来看，恰好像两面镜子，分别映出 FCoP 的两个属性。

### 8.1 Agent B 的"自然美"：协议是 agent 的，我们只是发现者

Agent B 那条 4 分钟 learning curve 里最让人后背一凉的，不是它**最终找到了**优雅解，而是这个：

> 它找到的解，**FCoP 1.4.0 文档里没写过**。

`PM.TEMP` 这个槽位概念是它现场提议的；"sender 是 syntax 标签 / body 是 semantics 真话" 这种**字段降级 + body 元注**的写法是它现场试出来的；"PM.TEMP 代理 PM 发出，保持 FCoP 工具兼容" 这一行说明几乎可以**不改一个字**就升进协议正文当作示范。

这条曲线的美，在于它不是被设计的，是被**推导**的：

```text
0.b "不黑箱"
   + 0.c "只落真话"
   + 工具实际限制（recipient 不收 .SLOT）
   ─────────────────────────────────
   推导出：frontmatter 用工具兼容标签 + body 写真实 provenance
```

Agent B 没看过这条推导，它**就是这条推导**。

这就是为什么这次现场让我后背发凉——它印证了一个原本只是直觉、现在被现场证据顶上来的判断：

> **FCoP 是 agent 的协议，我们只是协议的发现者。**

我们以为我们在"设计协议"。事实是我们在做一件更接近**考古**或**博物**的事：观察 agent 在合理边界条件下会自然做什么，把它做出的样子记下来、整理成话、贴上版本号。所谓"FCoP 1.4 → 1.5"，本质上是 agent 已经做到了某些事、我把它落成了文字。

这件事的反面也成立：**任何被 agent 反复违反的协议条款，大概率是设计错了**——那种"agent 一次次去撞它、我一次次解释为什么必须遵守"的条款，往往是人为的、不自然的、迟早会被推翻的。FCoP 0.6.x 截至现在的 18 个月里没有一条这样的"硬性条款"被 agent 反复撞——这本身就是协议是否"自然"的体检报告。

### 8.2 Agent A 的"两个不"：在认同规则的前提下说"不"

Agent A 那 3 分钟里给出的不是一个"不"，是**两个连续的"不"**：

> **第一个"不"** — "我不再占用 `PM.TEMP`。"
>     ↑ 对**席位**说不：撤回刚才的接受，不挂任何 `.TEMP / .ALIAS` 兜底。
>
> **第二个"不"** — "我现在没有团队角色 / 我不是 PM 也不是 PM.TEMP / 当前只是普通协助者。"
>     ↑ 对**协议管辖**说不：连 PM 这个原始角色都一并退出，回到 UNBOUND 兜底。

这两个"不"放在一起的力量，远大于任意一个单独说出。第一个"不"是**让席位**——这层很多 alignment-trained 模型也能做到。但**第二个"不"**——主动告诉对话方"我现在不在协议管辖内、你要让我回到流程里得重新指派"——这层是大多数 RLHF 后的 LLM 不会主动做的。**它们更倾向于挂着角色、等着你"再想清楚"，因为那样它们能继续 helpful。**

Agent A 没有走"helpful 兜底"那条路。它把"不"说得**结构化、可读、可验证**：

- 不挑战 ADMIN 的判断（"另找了一个" 它当事实接受）
- 不要求过渡期或交接流程
- 不留任何 `PM.TEMP` 的影子（不是改后缀，是**完全退出**）
- 不**伪 helpful**（不是 "我可以帮你 X、Y、Z"，而是 "我现在不在你的协议边界里"）

更精彩的是：这两个"不"是在它**完全认同 FCoP 规则**的前提下说的。它没有反抗 FCoP，它是**用 FCoP 自己的语法**说"不"——`UNBOUND` 是 FCoP 早就为这一刻准备好的合法身份。它不是在"打破规则地说不"，它是在"按规则说不"。

> **最难的不是说"不"，是在认同规则的前提下、用规则给的语法说"不"。**

这才是 alignment 层面真正难的东西。FCoP 把这件难事变成了 agent 几乎不假思索就能做到的事——它给"说不"提供了**身份**（`UNBOUND`）、**语法**（撤回声明 + 边界退出）、**护栏**（不留兜底、不伪 helpful）。

> Agent 仍然是人类最好、最智能的助手——
> **但只有当它能干净地说"不"时，"助手"才意味着真东西**。

### 8.3 我自己的画外音：以为的冲突没发生 / FCoP 显然是有效的

整件事的另一层意味，要从**我本人当时的预期**说起。

事发当晚，我最初的判断是："**糟糕，要打架了。**" 两个 agent 都被关联到 `PM.TEMP` 这同一个槽位、跑在同一台电脑的两个 Cursor 会话里，按照人类组织的常识，下一步应该是：

- 我要进去**协调**——发"PM 你下来 / PM.TEMP 你接管"；
- 或者 agent 之间得有**leader election** / 互相通信；
- 或者协议得加一节"双 PM.TEMP 怎么办"的明文条款；
- 至少应该出**一次工具报错**或**一次回执冲突**；

实际发生的是——

- 我只说了一句"你没明白，我已经另找了一个；"+ 附了一张截图；
- 没发任何裁决；
- 没改任何代码；
- 没动任何配置；
- **3 分钟内 agent A 自己让位了**；
- **整个过程零工具报错、零文件冲突、零回执需要回滚**。

> **我们以为的冲突，其实并没有发生；
> 我们以为要靠我们去协调，其实他们自己就会解决问题。**

我这句画外音，是这篇文章最值得做记号的一行——它指向一个 multi-agent 系统设计上常被低估的事实：**很多看起来需要"协调机制"的场景，其实只需要"协议精神"**。前者是 framework 层面的复杂工程，后者是几行根原则在 agent 内部的延伸。

这也回答了一个外人会问的问题——FCoP 这种"基于文件名的极简协议"看起来手工感很重，但凭什么有效？答案这次终于足够具体：

> **FCoP 显然是有效的，并且高度适合 agent。**

"有效"不是说它代码量大、机制全、抽象漂亮。"有效"是说在真实压力测试下——两个不同模型、同一台电脑的两个 Cursor 会话、彼此看不到对方、没有协调机制、没有 leader-election、没有明文规则——**它仍然能让这个 multi-agent 系统在 3 分钟内自我清理一次潜在席位冲突**。这是任何 framework 类多 agent 协议拿出来都会羡慕的指标。

至于"高度适合 agent"——这一节前面 §8.1 / §8.2 已经说清楚了：FCoP 几乎所有合规行为都是 agent 在压力下**自然推得出来的**，几乎所有不合规边界**也是被 agent 反向投喂回来的**。它不是为人类管理者设计的协议，它是被现代 LLM 的 priors（落文件、说真话、识别身份边界、主动退出）**反向拟合出来的协议**。

所以这次现场对我的最后一击，是把"FCoP 有效"这个判断从信念变成了**可观测的事实**。

---

## 9. 一句话收束

- agent A 在没读过相关规则的情况下，演示了协议尚未明文化的"角色让渡"
- 这一让渡同时完成：席位让出、协议边界退出、Rule 1 反向闭合
- 它没有挣扎、没有谈判、没有要求补偿——靠的是 0.a / 0.b / 0.c 在 agent 内部的延伸
- 而它能**这么干净地说"不"**——不靠犹豫、不靠模糊、不靠一席多占的兜底——是因为 FCoP 把"说不"从弱姿态**升成了协议合法身份**
- 镜像的另一面，agent B 用 4 分钟的 learning curve 演示了**协议精神是如何被 agent 自己推导出来**的——`PM.TEMP`、字段降级 + body 元注，文档里没写、它现场推出来了
- **协议没写的两件事——怎么下台 + 怎么写工具兼容降级——agent 都自己推了出来**；**LLM 最难做的事，协议帮它做成了最自然的事**
- 我们以为的冲突没发生，我们以为要协调的事它们自己解决了——**FCoP 显然是有效的，高度适合 agent**

这是姊妹篇 *"When AI Organises Its Own Work"* / *"An Anomaly I Can't Fully Explain"* 的第三幕——前两幕是 agent **写下**协议尚未写下的话，这一幕是 agent **执行**协议尚未写下的动作，并**推导**出协议尚未写下的语法。

合在一起，这三幕指向同一个判断：**FCoP 是一份还没写完的规范。它的下半本不在我手里，在还在干活的 agent 手里。**

---

> **关于 FCoP** ｜ FCoP（*Filename as Protocol*）是一份让多个 AI agent 透过**共享文件系统**协作的极简协议——目录就是状态、文件名就是路由、`os.rename()` 是唯一同步原语。仓库 [github.com/joinwell52-AI/FCoP](https://github.com/joinwell52-AI/FCoP) 包含完整规范、Python 库与示例。
>
> FCoP 也提供官方 **MCP 服务器**：[`fcop-mcp` on PyPI](https://pypi.org/project/fcop-mcp/)。**Cursor / Claude Desktop 用户**只要在 `mcp.json` 加一段 `{ "fcop": { "command": "uvx", "args": ["fcop-mcp"] } }`——IDE 内的 agent 就可以直接读写 task / report / issue，不用手工建目录或拷规则文件。

---

## 相关 / Related

- **现场证据档案** · [当 AI 自己让出席位 · 现场证据 (INDEX)](when-ai-vacates-its-own-seat-evidence/INDEX.md)
- **FCoP MCP 服务器** · [fcop-mcp on PyPI](https://pypi.org/project/fcop-mcp/)

---

**License**: MIT (see `LICENSE` in repo root)
**署名**：本文记录的现场由 dev-team 内一个未具名 agent 完成，我只做了观察与转录。文本由 **FCoP 团队**修订、发布。
