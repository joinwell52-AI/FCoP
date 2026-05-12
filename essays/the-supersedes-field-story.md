# 一行 frontmatter 的旅程

### `supersedes:` 字段 · 从一次救场到协议字段层的两小时

![一行 frontmatter 的旅程 · 题图](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/assets/the-supersedes-field-story-cover.png)

> *The Supersedes Field Story: how a single line of YAML invented by an agent under pressure became a protocol-level frontmatter field — and why this two-hour journey shows the cheapest place for FCoP emergence to land.*

**作者**:FCoP 维护者 · 2026-05-12
**关键词**:FCoP, supersedes, frontmatter 涌现, 协议字段, append-only, 反向兼容, SemVer MINOR

---

## TL;DR

2026-05-12 下午 16:07,codeflow OPS 在执行一次普通的回执写作中撞到了一个**协议级两难**:

- PM 在 TASK-010 修订 v2 里要求回执编号 `REPORT-013-OPS-to-PM`
- 但 `REPORT-011-OPS-to-PM`(v1 那次 G6 abort 回执)**已经 stage 进 commit**,等着随这一批协议物料一起入库
- Rule 5(append-only)说**不能改 REPORT-011**,Rule 6(reciprocity)说**TASK-010 必须有合法回执**,Rule 0.c(truthful)说**新回执不能假装旧 abort 没发生过**

三条规则同时拉紧。OPS 没有调任何人,也没有违反任何规则 —— 他在 REPORT-013 的 frontmatter 里加了一行字段:

```yaml
supersedes: REPORT-20260512-011-OPS-to-PM
```

旧文件留着,作为 abort 历史的真实记录;新文件公开声明"我接过它的职责"。三条规则同时满足。

这一行 frontmatter 不在协议字段表里 —— 但**它本可以在**。两小时后,FCoP 协议方启动 TASK-004 把它收回为正式字段,`fcop_protocol_version` 从 `2.0.0` 升到 `2.1.0`(SemVer MINOR additive),工具层补充 `read_task` / `read_report` 的继承链展示。

这是一次完整的"涌现 → 协议字段"生命周期。这篇 essay 把这两小时拉直说清楚 —— 不是为了表扬 OPS,而是为了说明:**协议字段层(frontmatter)是 FCoP 涌现最便宜、最干净、最适合着陆的地方**。

---

## 1 · 现场 · 三条规则同时拉紧

让我们把 16:07 那个十字路口的张力慢镜头看一遍。

### 1.1 前置状态

时间 16:00 左右,git staging area 已经积累了 35 个文件准备 commit:T2.4 + T2.5 的协议规则四件套 + 团队文档 14 件 + P4.9 阶段几份 TASK / REPORT。其中包括 **REPORT-011-OPS-to-PM.md** —— 这是 OPS 在 TASK-010 v1 失败时写的 abort 回执。

PM 在 16:05 修订了 TASK-010 为 v2(用 Rule 5 的方式:不改 v1,而是 append 新版本),修订理由是 G6 GATE 的实施细节要改。**v2 的 §6 段写明回执编号是 `REPORT-013-OPS-to-PM`** —— 这是新的回执编号,因为修订后是另一次 task 周期。

### 1.2 冲突点

OPS 接到 v2 任务,准备写回执。他遇到了:

| 规则 | 怎么拉紧 |
|---|---|
| **Rule 5 · append-only** | 不能修改已 stage 的 REPORT-011;不能 `git rm` 它(那等于改历史) |
| **Rule 6 · reciprocity** | TASK-010 v2 必须有 REPORT-013 回执;沉默 = 违约 |
| **Rule 0.c · truthful** | 新 REPORT-013 不能假装 REPORT-011 没存在过 —— 那个 abort 是真发生过的 |
| **PM 的明确编号** | TASK-010 v2 §6 写明回执编号 `013`,不能擅自改成 `011` 复用 |

四条夹在一起,OPS 没有简单出路:

- **写 REPORT-013,不提 REPORT-011** → 违反 Rule 0.c(掩盖 abort 历史)
- **改 REPORT-011 内容代替写 REPORT-013** → 违反 Rule 5(append-only)
- **删 REPORT-011** → 违反 Rule 5 + 0.c(改历史)
- **不写,等 PM / ADMIN 决定** → 违反 Rule 6(沉默 = 违约),且会卡住整个 commit

### 1.3 OPS 的发明 · 一行 frontmatter

OPS 写下 REPORT-013,frontmatter 长这样:

```yaml
---
protocol: fcop
version: 1
kind: report
report_id: REPORT-20260512-013-OPS-to-PM
sender: OPS
recipient: PM
task_id: TASK-20260512-010-PM-to-OPS
thread_key: p4_9_t2_4_t2_5_commit
session_id: sess-20260512-ops-01
status: done
supersedes: REPORT-20260512-011-OPS-to-PM   # ← 这一行
---
```

**`supersedes:` 不在协议字段定义里**。OPS 是当场发明的。

但这一行干净地解决了所有四条张力:

- **Rule 5 满足**:REPORT-011 没动,仍是 abort 历史的真实记录
- **Rule 6 满足**:REPORT-013 是 TASK-010 v2 的合法回执
- **Rule 0.c 满足**:REPORT-013 公开承认"我接过 REPORT-011 的职责",abort 历史可追溯
- **PM 的编号满足**:回执用 013,与 v2 §6 一致

更妙的是,这一行**对旧工具是透明的** —— `read_report(REPORT-013)` 仍能正常 parse,只是多了一个未知字段,旧 parser 会忽略它。对人也是透明的 —— `supersedes` 这个英文单词的意思在 IETF / W3C / RDF / HTTP header 等多个标准里都是同一个意思("the newer thing replaces the older thing"),不需要任何文档就能猜对。

---

## 2 · 为什么这个涌现"配进协议"?

涌现很多。大多数涌现是项目特定的、是失败、是错觉、是噪声。但**这一个**值得被收回。判定标准有四条:

### 2.1 不破坏既有结构

`supersedes:` 是一个**新增的、可选的 frontmatter 字段**。它不改:

- 文件名命名规则(`REPORT-{date}-{seq}-{sender}-to-{recipient}.md` 不动)
- 目录结构(还是 `tasks/` / `reports/` / `issues/`)
- 已有的必填字段(`protocol` / `version` / `kind` / `sender` / `recipient` 都不动)
- Rule 0..9 任何一条

它只是**在 frontmatter 的语义空间里多了一个键**。FCoP 协议的物理协议表面(filename, directory, frontmatter)其他部分**完全没动**。这种增量是协议演化里**最便宜的一种** —— 不需要 schema 大改、不需要工具大改、不需要老项目迁移。

### 2.2 反向兼容

旧版本的 FCoP parser(0.7.x)读 REPORT-013 不会出错 —— 它会 parse frontmatter 成功(YAML 标准本就允许未知键),把 `supersedes` 当成"我不认识但保留"的字段。

旧工具:`read_report(REPORT-013)` 仍能返回正文 + 已知字段。
新工具:`read_report(REPORT-013)` 额外显示 "Supersedes: REPORT-011"。

这是 SemVer **MINOR additive** 升级的教科书形态 —— `fcop_protocol_version` 从 `2.0.0` 升到 `2.1.0`,所有 2.0.x 项目继续工作,新功能对升级后的工具可见。

### 2.3 语义明确

`supersedes` 这个词不是 OPS 凭空造的。它在多个事实标准里都有同样的语义:

- **HTTP RFC 7231**:`Status: 301 Moved Permanently` + `Location: <new URI>` —— 旧 URI 被新 URI supersede
- **RDF / Dublin Core**:`dcterms:isReplacedBy` / `dcterms:replaces`
- **IETF RFC**:某 RFC 在 frontmatter 写 "Obsoletes: 793",意思就是"我 supersede 了 RFC 793"

OPS 没造词,他用的是网络标准 30 年来都在用的同一个 idiom。**这意味着任何下一个 agent / 任何一个新加入 FCoP 的项目,看到 `supersedes:` 都能秒懂** —— 这是字段普适性的最高证据。

### 2.4 普适

最关键的一条:**任何一个 FCoP 项目,只要规模足够大,都会撞上"新文件取代旧文件但旧文件不能删"这个张力**。

- 任务被中途取消、要写新任务 → `supersedes:` 旧 TASK
- 报告写完后发现重大错漏、要补写新报告 → `supersedes:` 旧 REPORT
- issue 被 reopen 后用新 ISSUE 文件继续追踪 → `supersedes:` 旧 ISSUE
- 决策(`DECISION-*`)被新决策推翻 → `supersedes:` 旧 DECISION

这些场景之前都靠**人工读正文**才能搞清楚关系。有了 `supersedes:`,关系**进入元数据层**,工具可以遍历、可以可视化、可以审计。

四条都过,`supersedes:` 配进协议字段层。

---

## 3 · TASK-004 的反向收回路径

涌现被识别只是第一步,把它**结构化地收回协议**才是协议方的工作。这一步对应 `TASK-20260512-004-ADMIN-to-ME.md`,内容是把 OPS 当场发明的字段升格成协议字段。

### 3.1 字段定义入文

在 `fcop-protocol.mdc` 里新增一节(在 "Task Format" 之后、"Subtask Batches" 之前):

```markdown
### `supersedes:` — 文件继承链 / File Lineage (since 2.1.0)

可选字段,值为另一份 FCoP 文件的 ID(`TASK-*` / `REPORT-*` /
`ISSUE-*` / `DECISION-*`)。语义:**本文件接过被引文件的职责,
被引文件保留为历史记录**。

Optional. Value is the ID of another FCoP file. Semantics:
**this file takes over the duty of the referenced one;
the referenced file is preserved as historical record**.

典型用途 / Typical usage:
- 任务被中途取消,写新任务接替
- 报告写完后需要补写新版本,旧 abort 报告保留
- 决策被新决策推翻,旧决策保留作为决策史

不要用 `supersedes:` 修改协议规则文件本身——规则文件由
`fcop` 包发版控制,见 Rule 8。
```

### 3.2 Schema 更新

`spec/schemas/task.schema.json` / `report.schema.json` / `issue.schema.json` 各加一段:

```json
{
  "properties": {
    "supersedes": {
      "type": "string",
      "pattern": "^(TASK|REPORT|ISSUE|DECISION)-\\d{8}-\\d{3}-",
      "description": "Optional file lineage anchor — points to another FCoP file this one takes over from. Added in fcop_protocol_version 2.1.0."
    }
  }
}
```

JSON schema 验证器现在会 enforce:**如果出现 `supersedes:`,它的值必须是合法的 TASK/REPORT/ISSUE/DECISION ID 前缀格式**。

### 3.3 工具支持

`read_task` / `read_report` / `read_issue` 工具增加输出段:

```
Supersedes: REPORT-20260512-011-OPS-to-PM
└─ archived (was: status=aborted)
```

新增 `list_lineage(file_id)` 工具(可选):递归追踪 `supersedes` 链,显示完整的文件继承族谱。这对长 thread / 多次修订的场景特别有用。

### 3.4 版本号

`fcop_protocol_version` 从 `2.0.0` 升到 `2.1.0`。SemVer 规则:

| 改动类型 | 版本位 | 这次的情况 |
|---|---|---|
| 破坏既有约束 | MAJOR ↑ | 否(没改既有字段、规则、文件结构) |
| 新增可选能力 | MINOR ↑ | **是**(`supersedes:` 是新的可选字段) |
| Bug 修复 / 文档修订 | PATCH ↑ | 否 |

所以是 **2.0.0 → 2.1.0**,清晰。

---

## 4 · 两小时的完整生命周期

这是一个非常**快**的涌现 → 协议路径。把时间线摆出来:

| 时间(UTC+8) | 事件 | 角色 |
|---|---|---|
| **16:07:39** | OPS 完成 commit b4ef8aa,REPORT-013 落 frontmatter `supersedes: REPORT-011` | OPS |
| **16:07** | OPS 在汇报里**主动列出** "新发明 `supersedes:` frontmatter 字段" | OPS |
| **16:11** | PM 自披露 #54 候选(TASK-010 v2 §6 与 stage 列表逻辑冲突,是导致 OPS 撞上 supersedes 张力的上游原因) | PM |
| **16:23** | ADMIN 追问:"这样的涌现是不是没有止境?最后呢?" | ADMIN |
| **~16:30** | 协议方启动 4 篇 essay 写作 + 4 条 TASK(其中 TASK-004 是把 supersedes 入协议) | FCoP 维护者 |
| **未来某个版本** | `fcop@2.1.0` 发版,`supersedes:` 正式入协议字段表 | FCoP 包维护 |

从"OPS 当场写下"到"协议方决定收回",**间隔 16 分钟**(16:07 → 16:23)。从"决定收回"到"essay 草稿落地"**再加约 1 小时**。完整生命周期**约 2 小时**(等 fcop 包发版另算)。

为什么这个速度有意义?**因为它说明 FCoP 协议层的反应延迟是分钟级、不是月级**。绝大多数软件协议的演化路径是:用户撞到问题 → 报 issue → 几周或几个月讨论 → RFC → 实现 → 发版。FCoP 把这条链压缩到 2 小时。

压缩的代价是什么?**不是没有代价** —— 这种速度只在协议方**就在场**、agent 和协议方在同一个会话里、且涌现本身刚好满足"四条收回标准"时才成立。一旦协议方不在场,或者涌现需要更多反例才能确认普适,2 小时就会拉长到 2 周。但起码,FCoP 把"2 小时"这个**可能的下限**演示了出来。

---

## 5 · 字段层是涌现最容易着陆的地方

这是 essay 的核心论点。让我把它说清楚:

FCoP 协议有几层"地面"可以承接涌现:

| 层级 | 改动代价 | 典型例子 | 老项目影响 |
|---|---|---|---|
| **文件名规则** | 极高(影响所有文件) | 改 `_ROLE` regex、加新字段名 | 全项目重命名 |
| **目录结构** | 高(影响路由) | 加 `inbox/` / `outbox/` | 老项目要迁移 |
| **必填字段** | 高(破坏向后兼容) | 给 frontmatter 加 required key | 老项目 frontmatter 全要补 |
| **Rule 0..9** | 中-高(改行为) | 加新规则 / 改既有规则 | agent 要重新学 |
| **协议解释** | 低(只是 commentary) | 加 "GATE 设计陷阱" 一节 | 老项目读不读都行 |
| **可选字段(frontmatter)** | **极低** | **`supersedes:` ← 本文主角** | **完全透明** |
| **工具行为** | 低-中(看是否破坏既有 CLI) | `read_task` 多打一段 | 老脚本不受影响 |

**可选字段是协议演化里最便宜的一类增量**。它:

- 不动文件名(物理协议表面稳定)
- 不动目录(组织边界稳定)
- 不动必填字段(向后兼容)
- 不动规则(agent 行为不变,只是多了**可用**的表达力)

OPS 在那个十字路口,**本能地选择了协议代价最低的那一层**。这不是巧合 —— OPS 在场的所有选项里(改 REPORT-011 / 删 REPORT-011 / 重命名编号 / 等 ADMIN 拍 / 在正文里写"实际上 REPORT-011 是 abort 的"…),`supersedes:` 是**唯一一个不动其他层**的方案。

换句话说:**当涌现刚好能在"可选字段"层着陆时,协议方应该尽量把它收在那一层,不要让它升级到规则层、不要让它分散到正文里、不要让它变成项目特定 convention**。

这就是为什么 essay D("协议保持短,历史不断生长")在这件事上验证过一次。`supersedes:` 不让协议骨架长大,它让协议骨架**多了一颗很小的可选叶子**。骨架仍然短,但表达力涨了一截。

---

## 6 · 收尾 · 一行 frontmatter 的旅程

`supersedes: REPORT-20260512-011-OPS-to-PM`

这一行 18 个字符的 YAML,在 2026-05-12 16:07 第一次被人类(准确说,被一个 LLM agent)写下。两小时后,它被收回为协议字段。再过一段时间,它会随 `fcop@2.1.0` 发版,出现在每个新装 FCoP 的项目的字段表里。

它的旅程**不夸张**。它不是革命性的发明,IETF 1980 年代就在用同一个词。它的意义不在"原创性",而在三件事:

1. **它在一个 LLM agent 撞墙后的 5 分钟内自发出现,且语义和工业标准完全一致** —— 这说明协议方不需要事无巨细地把每个字段定义清楚,有些字段会被 agent 在压力下重新发明。
2. **它没破坏任何既有结构,只是在最便宜的层(可选字段)着陆** —— 这是协议演化最理想的形态。
3. **从涌现到协议字段花了 2 小时** —— 这把"协议演化可以多快"的上限压低了一个数量级。

> **协议字段层(frontmatter)是 FCoP 涌现最便宜、最干净、最适合着陆的地方。**
>
> **`supersedes:` 是这条原则第一个真正可触摸的样本。下一个样本会是什么,我们还不知道 —— 但既然 OPS 能在 5 分钟内发明出一个符合协议精神的字段,我们有理由相信下一个也会从 agent 那边长出来,而不是从协议方这边想出来。**
>
> **协议方的工作,是认得出它,然后让它便宜地着陆。**

—— 协议方 · 2026-05-12

---

**See also**:
- 同系列 essay:`when-agents-learn-from-their-own-wreckage.md`(本案 = §3 frontmatter 涌现)
- 同系列 essay:`why-the-protocol-stays-short.md`(为什么协议保持短的论证,本案是它的实证)
- 同系列 essay:`gate-design-pitfalls-case-studies.md`(同一天另一个值得收回的涌现)
- 协议条款:`fcop-protocol.mdc` "supersedes 字段"小节(将在 2.1.0 版本中入文)
- 相关 task:`TASK-20260512-004-ADMIN-to-ME.md`(把 `supersedes:` 收回为协议字段)
