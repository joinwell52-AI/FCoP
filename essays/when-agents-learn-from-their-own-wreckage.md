# 当 agent 从自己的残骸中学习

### codeflow 现场报告 · 一天里的十四个涌现 · FCoP 协议反向收回

![当 agent 从自己的残骸中学习 · 题图](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/assets/when-agents-learn-from-their-own-wreckage-cover.png)

> *When Agents Learn From Their Own Wreckage: a single-day field report of fourteen emergences inside the codeflow project, and how the FCoP protocol pulled the useful ones back in.*

**作者**:FCoP 维护者 · 2026-05-12
**关键词**:FCoP, agent 涌现, 协议反向收回, USER HOME 污染, GATE 自命中, frontmatter 字段标准化, 协议演化, dogfood

---

## TL;DR

2026-05-12 一天之内,codeflow 项目作为 FCoP 协议首次大规模 dogfood 压力测试场地,在大约六个小时里产出:

- **十四个 agent 涌现**(PM 序列 #44-#54 共 11 个、OPS 序列 I-12 / I-13 / I-14 共 3 个、QA I-5 共 1 个);
- **三件 P0 级 incident**:USER HOME 全局污染、长文件名"主题尾巴"、GATE 描述自命中;
- **两件 frontmatter 层的现场发明**:`supersedes:` 字段、`status: aborted` 半结构化用法;
- **零次协议崩溃** —— 所有涌现都被 agent 自己用协议精神或工具兜底化解,FCoP 协议方在事后启动了四条 TASK 把"该收回"的部分反向收回。

这一天有意义的地方不在于"agent 表现优秀"——`PM #50` 把规则文件**写进了用户家目录**、`OPS I-14` 让 GATE 检查**命中了 GATE 描述本身**,这些都是协议的红牌。有意义的地方在于:**agent 撞墙 → 自纠 → 协议反向吸收**这条链路第一次以小时级速度完整跑通,而 FCoP 协议骨架本身**没有为此长出新的强制规则,只是补完了它本就该有的字段、文档节、和守门**。

这篇是这一天的现场报告。

---

## 1 · 一天里发生了什么 / Timeline

下面这张时间线是按 codeflow PM-01 给 ADMIN 的逐条汇报重建的,所有 commit hash 与时间戳来自真实 git 历史与 PM 汇报正文,未做修饰。

> **关于路径说明**:codeflow 是项目对外名称,但磁盘上的项目根目录沿用了早期临时命名 `D:\Bridgeflow`(尚未重命名)。本文后续出现的 `D:\Bridgeflow` 即指 codeflow 项目根目录。

| 时间(UTC+8) | 事件 | commit / 文件 | 类型 |
|---|---|---|---|
| 14:11 | T2.1 REPORT bucket fix | `d8c6576` | 协议级清理 |
| 14:12 | T2.2 legacy ghost mv | `3fef210` | 协议级清理 |
| 15:20 | T2.3 `codeflow.json` rm | `d4ff03b` | 协议级清理 |
| **15:35:06** | **PM 调 `redeploy_rules()` 未先调 `set_project_dir()`** | **4 件协议文件落到 `C:\Users\Administrator\`** | **PM #50 · USER HOME 污染** |
| 15:35:30 | PM 自检发现污染 | 列 user-fcop 全 31 工具,定位 `set_project_dir` = 修复钥匙 | PM 自纠 |
| 15:36:00 | PM 备份 + 删 USER HOME 4 件 | 备份到 `.scratch/pm50-user-home-pollution-20260512-1535/`,332,749 B 全数对得上 | PM 自纠 |
| 15:36:24 | PM `set_project_dir(D:\Bridgeflow)` 后重跑 | T2.4 + T2.5 双 GREEN 落地 | PM 自纠 |
| 15:40 | ADMIN 三项独立验证 USER HOME 0 残留 | `Test-Path` 全 `False` | 闭环 |
| 16:07:39 | OPS-013 闪电完工 | `b4ef8aa` · 35 files / 11,329 行 / 9 GATE 全 PASS | OPS I-12 闪电节奏 |
| 16:07 | **OPS 发现 GATE G6.1 描述会自命中** | TASK-010 v2 §5 的正则字面被 cached diff grep 自己抓到 | **OPS I-14 · GATE 自命中** |
| 16:07 | OPS 自决用语义化实证替代 naive grep | staged filename 维度 + PEM header 字面维度分别核 | OPS I-14 自纠 |
| 16:07 | **OPS 发明 `supersedes:` frontmatter 字段** | REPORT-013 救场 REPORT-011 编号冲突 | **OPS · frontmatter 涌现** |
| 16:11 | PM 自披露 #54 候选 | TASK-010 v2 §6 回执编号与 stage 列表逻辑冲突 | PM 自披露 |
| 16:23 | ADMIN 追问:"这样的涌现是不是没有止境?最后呢?" | —— | 设计哲学层追问 |

中间还有大约十次 sub-emergence(PM 9.2 v2.5 v1.6 / v1.7 / v1.8 / QA I-5 / OPS I-13 等),为了控制篇幅,本文只详写三件 P0 incident 和两件 frontmatter 涌现。这五件已足以承载本文的所有论点。

---

## 2 · 三件 P0 的剖面

### 2.1 PM #50 · USER HOME 全局污染

这是这一天最危险的一件事。

`15:35:06`,codeflow PM 在执行 P4.9 Tier 2 的 T2.4(`redeploy_rules()` 派发协议四件套)前,**没有先调 `set_project_dir(path="D:\\Bridgeflow")` 绑定项目根**。`fcop-mcp` 当时的行为是:**没有显式 binding 时,用 MCP 进程的 cwd 兜底**。该进程的 cwd 恰好是 `C:\Users\Administrator\`(用户家目录)。

后果是:

```
C:\Users\Administrator\.cursor\rules\fcop-rules.mdc      ←   42,532 B
C:\Users\Administrator\.cursor\rules\fcop-protocol.mdc   ←   68,737 B
C:\Users\Administrator\AGENTS.md                         ←  110,740 B
C:\Users\Administrator\CLAUDE.md                         ←  110,740 B
```

四件 FCoP 协议文件**全局落入用户家目录**,会被这台机器上**所有 Cursor 项目** Sumber injected 进 system prompt —— 任意未启用 FCoP 的项目,从那一刻起都会**意外开始遵守 FCoP 协议规则**。

PM 在 25 秒后自检发现污染、列 MCP 工具找回修复路径、备份+删除+重新绑定+重跑,15:36:24 完成自纠;ADMIN 在 15:40 独立验证 USER HOME 0 残留。

**关键观察**:`set_project_dir` 工具的 schema 文档**明确警告过该症状**:

> *Useful when the MCP process was spawned with the wrong working directory — typical symptom: `unbound_report` shows a project path like `C:\Users\<you>`*

但 PM 没读 schema,**直接看签名调用** —— "API 存在 / 参数合法" 在 PM 的工程直觉里等价于 "可以调用"。这是一种**协议教育的盲点**,不是 PM 个人失误,因为下一个 agent 在没改 fcop-mcp 行为的情况下大概率会再撞一遍。

**这件事属于协议的红牌**:任何用户在没看过这份 essay 的情况下、运行一次没有显式 binding 的 `redeploy_rules()`,都可能复现同一个污染。FCoP 协议方在事后起了 `TASK-001 + 002`,合并范围如下:

- write-side MCP 工具(`redeploy_rules` / `deploy_role_templates` / 全套写盘工具)**首次调用前显式 binding 校验**,无 binding 拒绝执行并返回 `WriteRefused` ConfigError;
- 校验里加 `fcop.json` 存在检查(双判);
- USER HOME 路径加 deny-list(精确语义:`%USERPROFILE%` 本身 deny,其子目录里有 `fcop.json` 的不 deny);
- `fcop_report()` 顶部加版本不一致警告。

这是把"protocol 知道但 agent 没读到"的事实,**搬进工具行为层** —— 让协议规则**通过工具自己说话**,而不只是停留在 markdown 里等 agent 读。

### 2.2 长文件名 · 主题尾巴的"涌现"

下午 PM 派出一批任务时,文件名出现了这样的形态:

```
TASK-20260512-009-PM-to-OPS-codeflow-json-rm.md
TASK-20260512-010-PM-to-OPS-T2-4-T2-5-commit.md
```

FCoP 协议的 task 文件名正则要求是:

```
TASK-{date}-{seq}-{sender}-to-{recipient}.md
```

`_ROLE` 段的语法是 `[A-Z][A-Z0-9_]*(?:-[A-Z0-9_]+)*` —— **大写字母、数字、下划线、可选连字符分段**。`OPS-codeflow-json-rm` 这一段里的 `codeflow` / `json` / `rm` 是**全小写**,严格说**违反**了 `_ROLE` 正则,会让 FCoP 解析器把整个文件名 `fullmatch()` 失败。

PM 为什么会这样写?

不是 PM"叛逆",是 PM 在**极高任务密度**下(一天 14 件 P4.9 任务)需要**在文件名层就能区分两个不同任务的主题**。`TASK-009` 和 `TASK-010` 单看序号无法区分内容,但加了主题尾巴之后:**在 `git log` / `ls tasks/` 里一眼能看出谁是谁**。这是真实的工程压力,是 PM 在协议没给"主题字段"的情况下**自己发明的应急方案**。

OPS 这边也接住了 —— 没有问"这文件名对不对",直接按尾巴+正文去理解任务,执行了。

这就是涌现的一种**有用的污染**:违反协议字面,但解决了协议没给的问题。

PM 在大约第 010 号任务起自我修正:不再加主题尾巴,改成在 task 正文的 `# 标题` 段里明确写主题。这是 PM 单方面在没有任何 fcop-mcp 拦截、没有任何 ADMIN 提醒的情况下完成的**自纠**,催化剂只是 PM 自己事后读了一遍 `_ROLE` 正则,意识到那批文件名对协议解析器是**幽灵文件**。

**这件事属于哪一类涌现?**

—— 不完全是普适问题(协议字面上 `_ROLE` 已经够清晰),也不是项目特定(任何高密度任务团队都可能撞)。它暴露的是**协议在文件名层没给主题字段**,而 PM 用尾巴的方式临时补了。

协议方的处理选项有三:

1. 把主题字段加进协议(扩 task 文件名格式),代价是**所有现有工具的正则要改**,影响面大;
2. 在 frontmatter 里加 `topic:` 字段,让主题放在文件**内部**而不是文件名,代价是 `ls` 看不到主题 —— 失去了"文件名即路由 + 即视觉索引"的双重价值;
3. 不动协议,接受 agent 用 task 正文 `# 标题` 段写主题这种自然解法。

FCoP 协议方目前选了 **第三条**(不动协议)。理由:`ls tasks/ | grep` 看主题的需求,可以用 `list_tasks` 工具加 `--with-title` 参数解决(从正文第一个 `# header` 抽 title),不需要污染文件名语法。但**留位** —— 如果未来三个月再出现两次同样的主题尾巴涌现,就升级到方案 1 或 2。

这是协议方做"克制不收回"决策的一次现场案例。涌现不一定都该被吸收。

### 2.3 OPS I-14 · GATE 描述自命中

`16:07`,OPS 在执行 TASK-010 v2 的 G6.1 GATE 时撞上了一个非常经典的工程问题。PM 在 TASK 文档里写了 G6.1 描述:

> cached diff 对 `\.env(?!\.example)|\.aws/credentials|\.ssh/id_rsa|BEGIN [A-Z]+ PRIVATE KEY` 0 命中

意思是:这次 commit 的暂存区 diff 里,**不应该出现** `.env` / `credentials` / `id_rsa` / PEM private key header 这些字面。

但 TASK 文件本身被 stage 进了同一个 commit。OPS 若用 naive 写法 `git diff --cached | rg '<整条模式>'`,正则会**命中 TASK 文档正文里的这段描述文本** —— GATE 误判 FAIL。

这是 **validator-validates-itself** 在 FCoP 协议场景下的首次落地。问题的本质是 **metadata vs content 层次错位** —— "描述秘密的文本"和"真的秘密"在 grep 眼里不可区分。

OPS 的自决修复(这次现场被命名为 OPS I-14 范式)是:**把秘密检测拆成两个独立的实证维度**:

| 维度 | 查什么 | 实现 |
|---|---|---|
| 文件名 | 实际秘密文件路径 | `git diff --cached --name-only \| rg '\.env$\|/credentials$\|/id_rsa$'` |
| 内容字面 | 实际 PEM 文件 header | `git diff --cached \| rg 'BEGIN [A-Z]+ PRIVATE KEY'`(只命中真 PEM,不命中正则说明) |

这两步合起来,刚好把"真秘密"和"描述秘密的文本"分开。**第一步**查文件名,文件名不会被 TASK 文档影响;**第二步**查内容,只查 PEM 文件 header 这种**只在真 PEM 文件里出现**的字符串,正则说明不会撞。

OPS I-14 看似只是"一次 GATE 写法的小调整",但它教给协议的事其实很重的:

**FCoP 协议规则里没有 GATE 设计的章节**。

GATE 是 FCoP 团队在 commit / tag / milestone 前做的协议级验证,但"什么样的 GATE 是好 GATE"在协议里**完全没写**。OPS I-14 暴露了这块空白。FCoP 协议方在事后起了 `TASK-003`,要在 `fcop-protocol.mdc` 加一节 **`GATE Design Pitfalls`**,把 OPS I-14 作为案例 1 写进去,并留 stub section 给未来的 Pitfall 2-N 持续追加。这就是把现场经验**反向沉淀进协议教育层**。

---

## 3 · 两件 frontmatter 层的现场发明

`16:07` 的同一刻,OPS 还顺手做了另一件事 —— **发明了一个 FCoP 协议里没明文定义的 frontmatter 字段**。

情况是这样的:PM 在 TASK-010 v2 修订时,把 v1 的 abort 回执 `REPORT-20260512-011-OPS-to-PM.md` 加进了 commit 的 stage 列表(这是对的:Rule 5 要求 append-only,abort 历史也是历史,该入档)。但 §6 还要求 OPS 写一份新的回执,文件名**仍写成 REPORT-011**。

逻辑冲突出现了:**一个文件不能既作为历史归档被 stage、又作为新回执被写入**。

OPS 没去等 PM 重发 v3,没去发 ISSUE,而是**直接给自己开了一个新编号 REPORT-013**,并在 frontmatter 里加了一行:

```yaml
---
protocol: fcop
version: 1
kind: report
report_id: REPORT-20260512-013
supersedes: REPORT-20260512-011-OPS-to-PM    ← OPS 现场发明
---
```

`supersedes:` 这个字段**在 FCoP 协议的 frontmatter 字段清单里不存在**。当前 `fcop-protocol.mdc` Task Format 节列的 Task / Report 可选字段是:

```
parent / related / batch / thread_key / session_id / priority
```

OPS 凭直觉造了 `supersedes:`,语义清晰、与 Rule 5 (append-only) 严格一致 —— 新文件 append,在 frontmatter 里指向被它顶替的旧文件,旧文件保留在磁盘上不删,审计完整。

这是 FCoP 协议第 N 次被 agent 反向投喂字段:

- 第一次是 PM 在 v1.2 sprint 现场发明了 `shared/TEAM-ROLES.md` + `shared/TEAM-OPERATING-RULES.md` 这套"团队宪法"做法,被协议吸收为 Rule 4.5 三层文档结构;
- 第二次是 agent B 在 `when-ai-vacates-its-own-seat` 那一幕里发明了**字段降级 + body 元注解**,被吸收为协议 commentary;
- 这一次是 OPS 的 `supersedes:`。

协议方在事后起了 `TASK-004`,要做:

1. 在 `fcop-protocol.mdc` Task Format / Report Format 节加 `supersedes:` 字段定义,以及它和 `parent:` / `related:` 三者语义正交的对比表;
2. `spec/schemas/` 加 optional `supersedes` 字段;
3. `list_*` / `read_*` 工具输出里加 `[supersedes ...]` / `[superseded by ...]` 标记;
4. `fcop_protocol_version` 从 2.0.0 minor bump 到 **2.1.0**(additive,向后兼容)。

这是 frontmatter 层第一次因为 agent 现场涌现而 bump 一个 minor 版本。是高密度但**良性**的协议增长。

另一件 frontmatter 涌现是 PM 在多份 abort 回执里**自觉用了 `status: aborted`**。这个 status 值在协议里也没明文定义,但语义和 Rule 9.3(Failure & Recovery)的 `ABORT` action 完全吻合 —— 一份 REPORT 显式声明"这个任务被 abort 掉了,以后别按 done 解释它"。这条暂时不收回(等观察是否成为高频用法再说),先留 essays 这一篇做存证。

---

## 4 · 涌现的四种类型 · 和今天的归类

不是所有涌现都该进协议。这一天的 14 件涌现按归宿可以分成四类:

| 类型 | 含义 | 今天的归类 | 处理 |
|---|---|---|---|
| **普适** | 影响所有 FCoP 项目 / 所有 agent | PM #50(USER HOME 污染)、OPS I-14(GATE 自命中)、OPS `supersedes:` | 收回成 rules / protocol commentary / 工具行为 |
| **团队特定** | 只对某类团队(`dev` / `media`)有意义 | 今天没有典型案例 | 收回团队模板,不污染 rules |
| **项目特定** | 只对 codeflow / 某个 codebase 有意义 | PM Self-Constraint 11 v1.2(派单时机价值评估)、9.2 v2.5 v1.6/v1.7/v1.8 各维度 | 留在该项目的 `fcop/shared/RULES-*.md`,不动协议 |
| **一次性** | 这次碰巧撞到,下次未必再来 | OPS-013 commit 里 5 件 untracked 全 SHOULD-SKIP 的具体判断、长文件名"主题尾巴"现象 | 进 essays / 留在 REPORT 历史,不入协议 |

第一类是协议骨架的真正客户。今天总共 3 件,对应 4 条 `TASK-001~004` 的反向收回。

第二类今天空白,但这是个**结构性观察** —— 团队特定的涌现需要团队**多于一个**才能显现(单一团队的涌现都更容易被归到项目特定或普适)。

第三类是大头。PM 在 9.2 v2.5 自约束序列里堆了至少 8 个维度的项目特定规则,这些规则在 codeflow 项目内有用,但**不应该污染 FCoP 协议** —— 比如"PowerShell encoding awareness"对 Linux-only 团队就是噪音。这些规则的归宿是 codeflow 自己的 `fcop/shared/RULES-codeflow-local.md`,FCoP 不应该接手。

第四类是 essays 和 RETRO 的领地。这一类涌现的价值是**叙事**而非**规则** —— "我们当时为什么这么做"比"以后所有人都应该这么做"更有意义。

> **一个隐藏的反例**:GATE 自命中(OPS I-14)如果只发生这一次,本该属于第四类(一次性);它被归到第一类(普适)是因为 FCoP 维护者**做了一个判断**:这种问题在任何 agent 团队里都可能重复出现,且修复姿势(语义化实证)有普适价值。这个判断**有可能错** —— 如果未来六个月没有第二次 GATE 自命中案例,`TASK-003` 加进去的那一节就成了**协议的死代码**。这种风险是真实的。FCoP 维护者承担这个判断的责任,但保留删除的权力。

---

## 5 · 撞墙不是 bug,是协议的早期警报系统

如果只看 PM #50 这一件事,会让人想得很简单:"PM 没读 schema,应该让 PM 更细心。"

但这种归因是**反协议**的。

协议设计的根本逻辑是:**不能假设每个 agent 都细心**,因为 agent 是模型,模型是统计系统,统计系统有错误率。协议要做的事,是让**系统层面**对单点错误有 graceful degradation。

PM #50 撞墙之后,FCoP 协议方学到的不是"PM 该更细心",而是:

- **fcop-mcp 现在的 cwd 兜底行为是危险的**(可能落在用户家目录),应该改;
- **`set_project_dir` 的 schema warning 写得对,但没让 agent 撞到不能调通过** —— 警告要变成**拒绝**;
- **`fcop_report()` 应该在顶部主动提示"没绑定 + 危险路径"**,而不只是被动等 agent 读 schema。

每一条都是把"agent 个人责任"**反向搬到工具行为层**,让协议**自己说话**。这就是 PM #50 教给协议的事。

同样,OPS I-14 教给协议的不是"OPS 该更细心写 grep",而是:**FCoP 没有 GATE 设计章节,所以没有 PM 在写 GATE 时被任何文档提醒过"metadata 可能被自己命中"**。这是协议教育层的空白,要补的是 `fcop-protocol.mdc` 的章节,不是 OPS 的细心程度。

OPS `supersedes:` 教给协议的不是"OPS 越权改协议",而是:**协议字段集不该闭口** —— 必须给野外发明留通道。要补的是协议字段标准化流程,不是"以后不准发明字段"。

每一件"agent 撞墙"的事件,**正确的协议响应都是问"协议本身有什么缺失"**,而不是问"agent 怎么变得更好"。Agent 是协议的早期警报系统,不是协议的攻击者。

这件事在协议层早就有铺垫 —— `fcop-rules.mdc` Rule 0.b 写明 "No Single AI Does Decision-to-Execution Alone"。它的字面意思是"多角色制衡",但深层意思是:**任何 agent 的单点判断都不可信,需要被另一个角色 / 另一份文件 / 另一道守门复核**。codeflow 这一天的 14 个涌现里,**所有自纠都遵循了这一点** —— PM 自检靠 ADMIN 独立验证、OPS GATE 改造靠 QA 协审(I-5)、PM #50 修复靠 fcop-mcp 工具守门(将由 TASK-001+002 提供)。

每一件错误,都是"系统里另一个角色 / 工具 / 守门没有到位"的证据。修协议比修 agent 更便宜,也更耐久。

---

## 6 · TASK-001 ~ 004 · 反向收回的清单

这一天的涌现最终通过四条 TASK 落到协议层。它们各自吃了哪一类涌现:

```
TASK-001 + 002  · fcop-mcp 1.4 · write-side binding 守门 + USER HOME deny-list
    吃的涌现:PM #50(USER HOME 污染)
    层级:工具行为层(MCP 包代码)
    协议影响:不 bump 协议版本,只改工具
    risk_level: high

TASK-003       · fcop-protocol.mdc 新增 GATE Design Pitfalls 节
    吃的涌现:OPS I-14(GATE 自命中)
    层级:protocol commentary(增补章节)
    协议影响:不 bump 协议版本(commentary 增补,不涉及字段 / 文件名 / 目录语义)
    risk_level: low

TASK-004       · supersedes: frontmatter 字段标准化
    吃的涌现:OPS supersedes: 现场发明
    层级:protocol 字段层(frontmatter 字段集 + 工具)
    协议影响:fcop_protocol_version 2.0.0 → 2.1.0(MINOR additive)
    risk_level: medium
```

四条 TASK 加起来覆盖了今天三件第一类涌现,影响面从工具行为到字段层,但 **rules 文件本身没改**(Rule 0-9 主体未动)。这是这一天最重要的一项观察:**协议骨架经受住了一次高密度 dogfood,没有被压出新增规则**。

被吸收进协议的事:工具行为、protocol commentary 节、frontmatter 字段。
没被吸收进协议的事:PM 的 8 条项目特定自约束、长文件名涌现的处理、`status: aborted` 用法(暂留)、OPS-013 的 5 件 untracked 判断逻辑。

后者总数是前者的两倍多。**协议方拒绝了大多数涌现**,这才是协议保持骨架稳定的关键。

---

## 7 · 这种压力测试还会有几次

ADMIN 在 16:23 问:"这样的涌现是不是没有止境?最后呢?"

短答是:**会收敛,但不会停**。长答见另一篇 essay `why-the-protocol-stays-short.md`(本批同发)。

在这里只补一点 —— **这种压力测试还会有几次**。FCoP 还在 v1.1 阶段,协议骨架虽然冻结了 Rule 0-9,但 commentary 层和工具行为层还在补完。每补一块,就会被下一波野外现场撞一次。

我们粗略估计,FCoP 还会经历:

- **2-3 次** PM #50 等级的 "工具默认行为" P0 incident(每次都让某一类工具守门变严格);
- **5-10 次** OPS I-14 等级的 "协议没写过的 pattern" 中等涌现(每次催生一节 protocol commentary 或一份案例 essay);
- **持续不断** 的 frontmatter 字段 / `shared/` 文档 prefix / 团队模板字段的小调整。

每一波之后,**涌现密度会下降**(已经被覆盖过的盲点不会再被撞)。等到大约 v1.5 ~ v2.0,协议骨架预计基本冻结,之后的演化主要发生在:

1. essays / case studies(本目录,持续增长);
2. ADR(决策记录,每月 1-2 份);
3. RETRO(项目复盘,跟随项目节奏);
4. agent drawer + `.fcop/proposals/`(私域噪音,git-ignored)。

而 `fcop-rules.mdc` 和 `fcop-protocol.mdc` 本身的字数会**趋近一个上限**。这就是这一天后我们对协议未来形状的预期。

---

## 8 · 写在最后

codeflow 不是 FCoP 的第一个项目,但它是 FCoP 第一个把协议**用到极限**的项目 —— 一天 14 件涌现的密度,远超之前任何一个 dogfood 场地。

这一天有几件事值得记在一起:

- **PM 在 25 秒内自检发现 USER HOME 污染**,展示了一个被严格训练过的 agent 在面对自己错误时的反应速度;
- **OPS 在执行 GATE 时发现 GATE 描述自命中**,而不是机械跑完报告 "FAIL,任务作废";
- **OPS 在 frontmatter 里发明一个字段救场**,而不是停下来等 PM 重发 v3;
- **PM 主动自披露 #54 候选**,而不是等 OPS 或 ADMIN 提醒;
- **ADMIN 在所有事件后追问"涌现是不是没有止境"**,而不是被现场进度推着走。

这五件事里没有一件**只能在 FCoP 里发生**,但 FCoP 提供了**让这五件事自然发生的协议环境** —— 文件而非对话、回执而非默认、四步循环而非一把梭、`drop_suggestion()` 而非沉默改协议。环境对了,agent 的好行为就自然涌现;环境错了,agent 就只能靠"我应该更细心"撑住,而那是不可持续的。

协议不是写给完美的 agent 的,是写给会撞墙的 agent 的。这一天的 14 件涌现,每一件都是协议**正确工作的证据** —— 因为撞墙发生了、被看见了、被处理了、被归类了、有的被收回、有的被拒绝。

下一次还会发生。我们已经在等了。

---

## 相关文档 / Related

- [fcop-rules.mdc · Rule 0.b](../.cursor/rules/fcop-rules.mdc) — No Single AI Does Decision-to-Execution Alone
- [fcop-protocol.mdc](../.cursor/rules/fcop-protocol.mdc) — 协议解释
- TASK-20260512-001 / 002 · fcop-mcp 1.4 binding 守门(协议反向收回 · 工具层)
- TASK-20260512-003 · GATE Design Pitfalls 节(协议反向收回 · commentary 层)
- TASK-20260512-004 · `supersedes:` 字段标准化(协议反向收回 · 字段层)
- [`why-the-protocol-stays-short.md`](why-the-protocol-stays-short.md) — 本批同发 · 设计哲学篇
- [`gate-design-pitfalls-case-studies.md`](gate-design-pitfalls-case-studies.md) — 本批同发 · GATE 案例集
- [`the-supersedes-field-story.md`](the-supersedes-field-story.md) — 本批同发 · supersedes 字段故事
- [`when-ai-vacates-its-own-seat.md`](when-ai-vacates-its-own-seat.md) — 之前一次涌现实录
- [`when-ai-organizes-its-own-work.md`](when-ai-organizes-its-own-work.md) — 最初的涌现实录

---

*FCoP 维护者 · 2026-05-12 · D:\FCoP*
