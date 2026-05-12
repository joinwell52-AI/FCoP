# 看,但不动手

### FCoP 三层语义执行链科普 · 协议为什么"只看不改"

![看,但不动手 · 题图](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/assets/looking-without-touching-cover.png)

> *Looking, not Touching: a popular-science walkthrough of FCoP's three-layer semantic execution chain — why the protocol can see, interpret, and write a remediation plan, but stops short of executing it.*

---

## TL;DR · 给赶时间的读者

- FCoP 是文件协议,不是任务执行器 —— 协议把"看见违规"和"动手整改"刻意分开,中间隔三层。
- 三层语义执行链 = **L1 看见事实** → **L2 解释为违规** → **L3 写成整改说明书**。
- 输出叫 `INSPECTION.md`:**结构化发现 + 建议整改方案**,不是命令,执行权留给人或被人授权的 agent。
- 这套分层是 FCoP 的硬约束:任何"让工具自己动手"的扩展,**必须单独立 ADR**,不准从 audit 工具悄悄长出来。

为什么要把简单的"检查 + 改"切成三层?因为协议工具一旦"自动动手",离把整个项目搞乱只差一次 LLM 抽风 —— 详见正文。

---

## 1 · 一个开发者看不出来的设计选择

如果你只用过 `eslint --fix` / `black .` / `pre-commit run --all-files`,你大概默认:

> 检查工具发现问题,顺手就给修了 —— 这不挺好吗?省事。

FCoP 不这么干。FCoP 的同类工具 `fcop_audit()` 跑完之后,**一行项目文件都不改**(除了它自己写出来的那份报告)。它只产出一份 Markdown:

```fcop/shared/INSPECTION-20260512-001-takeover.md
```

报告里写着:

- 发现了什么(事实)
- 这意味着什么违规(解释)
- 建议你怎么修(整改方案 + 可复制命令 + 回滚方式)

然后工具退出。要不要照这份说明书去改,**由你或被你授权的 agent 决定**。

第一次见这个设计的工程师常常会问:

> 既然都知道怎么修了,为什么不顺手修了?多一次手动操作不就是浪费时间?

这个问题的答案是这篇文章的全部:**因为"看见"和"动手"是两件不同的事,把它们分开,是 FCoP 这套协议得以稳定运行的核心机制。**

---

## 2 · 三层执行链 —— 协议的眼睛长什么样

下面这张图,是 FCoP 协议的"内脏"示意 —— 把"看见 → 解释 → 写说明书"分成三层,中间不允许有任何短路:

![FCoP 三层语义执行链模型图 v1.0](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/adr/FCoP-semantic-execution-chain-v1.0.png)

读这张图最快的方式是从上往下顺一遍:

```text
项目工作树(Project Working Tree)
       │
       ▼  scan(纯读)
┌─────────────────────────────────────────┐
│  L1 · 检测层 · 发现事实(What is)         │
│  6 个 scan_*() 方法,纯扫描,不解释       │
│  输出:Facts(原始事实 / 计数 / 证据)     │
└──────────────┬──────────────────────────┘
               │  interpret
               ▼
┌─────────────────────────────────────────┐
│  L2 · 解释层 · 解释意义(What it means)  │
│  事实 → 协议规则匹配 → 违规清单           │
│  输出:Violations(结构化,机读)           │
└──────────────┬──────────────────────────┘
               │  generate
               ▼
┌─────────────────────────────────────────┐
│  L3 · 文档层 · 写说明书(What to do)     │
│  违规 → Tier 1/2/3 分组 → 可复制命令      │
│  输出:INSPECTION.md(人读)               │
└──────────────┬──────────────────────────┘
               │  use
               ▼
        人或 agent 决策并执行
        (执行发生在 FCoP 之外)
```

注意两件事:

1. **三层之间是单向流水线**:L1 不知道 L3 长什么样,L3 不能跳过 L2 直接读项目文件。每一层只跟前一层的输出打交道。
2. **协议的边界停在 INSPECTION.md**:执行那一格画在虚线外面,FCoP 协议本身不跨过去。

这两条加起来,就是 FCoP 协议工具体的"克制":协议提供完整的"看 + 想 + 写",但**不提供"做"**。

---

## 3 · L1 检测层 —— 只看,不判断

L1 是协议的眼睛。它做一件事:**告诉你项目里现在有什么**。它**不**告诉你这些东西"对不对" —— 那是 L2 的事。

L1 当前由 6 个 `scan_*()` 方法构成,每个回答一个独立的问题:

| 方法名 | 在问什么 | 关联规则 |
|---|---|---|
| `scan_misplaced_envelopes()` | 有没有 envelope 文件被放错桶?(比如一份 `kind: report` 的文件却在 `tasks/` 里) | Rule 2 · 文件即协议 |
| `scan_legacy_role_docs()` | 项目根有没有"草根角色书"(没有 frontmatter 的零散 `.md`)? | Rule 1 · 两阶段启动 |
| `scan_legacy_manifests()` | 除了 `fcop.json`,还有没有别的 `fcop/*.json` 在装"另一份身份"? | Rule 0 · 真相唯一 |
| `scan_cursor_rules()` | `.cursor/rules/` 里协议规则齐不齐?有没有混进草根 `.mdc`? | P0 · 规则部署 |
| `scan_shared_deployment()` | `fcop/shared/` 三层团队文档部署完整度怎样? | Rule 4.5 · 三层文档 |
| `scan_ghost_prefixes()` | 有没有 `DRAFT-` / `HANDOFF-` / `AMEND-` / `*-v2.md` 这类幽灵前缀? | Rule 5 · 历史只增不改 |

每个方法返回一组 **Fact**:

```python
Fact {
    fact_id:    "F-001"
    source:     "scan_legacy_manifests"
    evidence:   ["fcop/codeflow.json"]   # 哪些文件触发了
    count:      1
    raw_data:   {...}                     # 文件大小 / 时间戳等
}
```

注意 **Fact 里没有"严重度"** —— L1 不知道这事算 P0 还是 P2,它只负责"看见"。把"看见"和"评级"分开,是 FCoP 故意做的:

- 规则演化时(比如把"幽灵前缀"从 P1 提到 P0),只需要改 L2 的解释逻辑,**L1 一行都不用动**。
- L1 不依赖任何"我以为这条规则应该多严重"的人类判断 —— 这种判断容易漂移,而原始事实不会。

工程上的好处:**L1 可以独立单测**。给它一个 fixture 目录,断言它返回多少个 Fact —— 不必同时验证"P0 还是 P1"。规则演化时 L1 的测试不会跟着崩。

---

## 4 · L2 解释层 —— 把事实变成"违规"

L1 看见 `fcop/codeflow.json` 这个文件。**它是不是违规?** 这事 L1 不管。

L2 来管。L2 拿 L1 的 Fact 列表,跑一遍"规则匹配 + 严重度评估 + 整改映射",输出**结构化的 Violation 清单**:

```python
Violation {
    violation_id:   "P0-001"
    severity:       "P0"                                # P0 / P1 / P2
    rule_violated:  "Rule 0 · 单一真相源"
    summary:        "fcop/codeflow.json 与 fcop.json 形成双 manifest"
    evidence:       ["fcop/codeflow.json"]
    impact:         "agent 会在两个身份源之间漂移"
    remediation:    [                                    # 机读,L3 用来渲染
        RemediationStep {
            tier:     1
            command:  "git rm fcop/codeflow.json"
            rollback: "git checkout HEAD -- fcop/codeflow.json"
            executor: "OPS"
            estimate: "5 min"
        }
    ]
}
```

几个关键点值得停一下:

**(a) 严重度三档,P0 必须修,P2 可以拖**

- **P0**:阻塞协议运行 —— 真相被破坏 / 协议规则没部署 / 历史被改过。这一档不修,FCoP 不能保证别的规则继续成立。
- **P1**:规范性 —— 文件归类不对、命名不规范,协议还能跑,但下一个 agent 进来时会困惑。
- **P2**:整洁性 —— 草稿没归档、临时文件没删,影响美观不影响功能。

**(b) `remediation` 是建议,不是命令**

仔细读那个字段名 —— **remediation**(整改建议),不是 `action` 或 `execute`。L2 把"该怎么修"想清楚了,**但不去做**,只是把它绑在 Violation 上,等 L3 渲染。

**(c) L2 看不到项目文件**

这一层只读 L1 的 Fact 列表,不去重新扫文件系统。这意味着:

- L2 的所有决策都可追溯 —— 每条 Violation 都能往回指到具体的 Fact。
- L2 的单测可以用纯内存 Fact fixture,不依赖磁盘。

---

## 5 · L3 文档层 —— 把违规写成人能读的说明书

L2 的输出已经够 LLM 直接消费了 —— 结构化、机读、字段齐全。但**人**读起来眼花。

L3 干的是"渲染"这一步:把 L2 的 Violation 清单,变成一份给人(或给被人监督的 agent)看的 Markdown。

它做三件事:

1. **分组 + 排序**:按 severity 把 P0 / P1 / P2 切成三段,各段内按规则编号排。
2. **可读化**:每条 Violation 渲染成"标题 + 实证 + 影响 + 建议命令 + 回滚",而不是 JSON dump。
3. **执行块(Execution Block)**:把所有 `remediation.command` 按 Tier 1/2/3 重新分组,给一份**可以一次复制运行的命令清单**(每行带回滚指令)。

最后产出 `fcop/shared/INSPECTION-{YYYYMMDD}-{NNN}-{scope}.md`:

```markdown
---
inspection_id: INSPECTION-20260512-001-takeover
status: red                              # red / amber / green
p0_count: 2
p1_count: 5
p2_count: 1
estimate: "1-2 hours"
---

# INSPECTION 报告 · 2026-05-12 · takeover

## 摘要
🔴 RED · P0 × 2 / P1 × 5 / P2 × 1 · 预估整改 1-2 hours

## P0 · 阻塞性违规

### P0-001 · 双 manifest(Rule 0)
- **实证**:`fcop/codeflow.json` 与 `fcop.json` 并存
- **影响**:agent 会在两个身份源之间漂移
- **建议**:`git rm fcop/codeflow.json`(5 min,OPS)
- **回滚**:`git checkout HEAD -- fcop/codeflow.json`

...

## ▶ Execution Block

### Tier 1 · 立即(今日内,低风险,无依赖)
```bash
git rm fcop/codeflow.json
# 回滚:git checkout HEAD -- fcop/codeflow.json
```

### Tier 2 · 本 sprint(1-2 天,有依赖)
...
```

注意最后那个 Execution Block —— **这是 L3 的核心创新**:它把"我应该按什么顺序做、每一步执行 / 回滚的命令是什么"打包成可粘贴的代码块。

但这块文字依然只是**说明书**。FCoP 不会自己跑那些命令 —— `INSPECTION.md` 写完,工具的工作就结束了。

---

## 6 · 为什么 INSPECTION 不是 Remediation Plan

这是一个细微但非常重要的命名选择:

> **INSPECTION ≠ Remediation Plan**
>
> **INSPECTION = Structured Findings + Suggested Remediation Plan**

如果叫 "Remediation Plan",听上去像"接下来要执行的计划";如果叫 "Inspection",听上去就是"体检报告"。FCoP 选后者,有意把语义往"观察"上靠。

`INSPECTION.md` 也走 FCoP 的标准 envelope 规则:

- **append-only**:同一天同一 scope 第二次跑,产出 `NNN+1`,不覆盖第一份 —— 历史保留。
- **可追溯**:每个 Violation 都附 `violation_id` + `scan_source` + `evidence`,能完整回溯到 L1 的原始 Fact。
- **人读优先**:Tier 分组、命令块带回滚、每条都有"执行人"建议。

也就是说,即便几个月后回头查"那次 takeover 我们整改了什么",`fcop/shared/` 里那份 INSPECTION 还在,它本身就是审计链的一环。

---

## 7 · 五大原则 —— 为什么"不动手"是设计目标

FCoP 在文档里把这套架构总结成五条原则,值得逐条读一遍:

### ① 不越界(No Boundary Violation)

> 在协议规则定义的边界内工作。

`fcop_audit()` 只做协议规定的事,不去扩展"顺便清理一下 git 仓库"或"顺便重排一下文件"。

### ② 只观察(Observe Only)

> 不修改项目状态,不写业务文件。

工具是只读的。它写盘的唯一副作用,是它自己产出的那份 `INSPECTION.md`。这一条卡死了"工具悄悄改项目"这条路。

### ③ 不执行(No Execution)

> 只生成说明书,执行决策由人做出。

Execution Block 里的命令是**建议**,不是**指令**。工具退出后等人介入。

### ④ 可追溯(Traceable)

> 每个违规可回溯,每个步骤可审计。

每条 Violation 都能往回指到具体的 Fact、scan_source、evidence。没有结论是"凭空"的。

### ⑤ 防漂移(Anti-Creep)

> 未来要"让工具自动执行"?**必须单独立 ADR**,经过 ADMIN 二次审批。不准从 audit 工具悄悄长出来。

这条最重要。它的意思是:**今天工具不动手,以后想动手也得走显式立法**,而不是某天某次 PR 里悄悄加了个 `--fix` 参数。

为什么这条这么严?因为 FCoP 是协议层。协议层一旦能"自动改项目",它和应用层(那些真正负责干活的工具)的边界就模糊了 —— 然后所有"协议规则只是说说"的故事就开始了。FCoP 选择把这条线画死:**协议工具永远是观察者,执行权永远在协议之外**。

---

## 8 · 同类工具的边界对比

如果还是觉得"不动手"很怪,看看其他熟悉的工具是怎么划线的:

| 工具类型 | 看 | 想 | 写说明书 | 执行 |
|---|:-:|:-:|:-:|:-:|
| `linter`(eslint / ruff) | ✅ | ✅ | △ 简短 | ❌ |
| `linter --fix` | ✅ | ✅ | ❌ | ✅ 自动改 |
| `test runner`(pytest) | ✅ | ✅ | ❌ | ❌ 只报错 |
| `CI pipeline` | ✅ | △ | ❌ | ✅ 跑命令 |
| `agent` (claude / cursor) | ✅ | ✅ | △ chat 里说 | ✅ 主动改 |
| **`fcop_audit()`** | ✅ | ✅ | ✅ 结构化 | ❌ |

注意 `fcop_audit()` 唯一独占的格子是"**写说明书 · 结构化**" —— 这是它的独特定位:**写一份足够详细、可复制、可审计的说明书,然后停在那里**。

它不和 linter 抢"自动 fix"的市场,也不和 CI 抢"自动跑"的市场,更不和 agent 抢"主动改"的市场。它的位置是:

> **介于"只报错"和"自动改"之间的那个空格**:把"该怎么修"写成可读 + 可复制 + 可审计的文档,把执行权完整留给人。

为什么 FCoP 要占这个位置?因为协议演化需要这个位置 —— 协议变了之后,老项目需要被"接管(takeover)"或"升级(upgrade)",这中间的整改路径必须**可审查、可中止、可分批**。自动 fix 工具做不到这件事(它们做的是"一次过"),agent 也做不到(它们的执行不可审计、不可中止)。

---

## 9 · 协议的克制是用来"传"下去的

一份协议工具体能不能在十年后还原样工作,取决于一个简单的问题:

> **它有没有"自己动手"的能力?**

凡是能自己动手的协议工具,迟早会动错。因为:

- 它的执行依赖代码版本、依赖底层 OS、依赖被检查项目的状态 —— 这三件事都会漂移。
- 一次执行错误就可能搞乱被检查项目,而协议又是"被信任的层",出错代价比应用层大得多。

FCoP 把"看"和"做"切开后,这个风险被显著降低 —— 即便 `fcop_audit()` 因为某次 bug 写错了 INSPECTION,**项目本身没动**。人读 INSPECTION 时一眼能看出"这条建议不对",然后选择不执行。

这就是这套三层架构最深的设计意图:**把决策权和执行权,完整留在人这一边**。

协议负责"看清楚"。协议负责"想明白"。协议负责"写清楚"。

至于"要不要照着做" —— 那是协议的职责之外的事。

---

## 一句话回顾

FCoP 用三层 `L1 → L2 → L3` 把"看见 → 解释 → 写说明书"切开,产出 `INSPECTION.md`,然后停在那里。**协议的眼睛不动手 —— 这是设计,不是疏忽。**

---

## 相关阅读

- **`adr/FCoP-semantic-execution-chain.md`** —— 这篇科普的源文档,规范级三层定义、完整 ADR 引用、协议成熟度快照
- **`adr/ADR-0030-capability-governance-boundary.md`** —— Schema 层:能力边界(能不能做)
- **`adr/ADR-0031-governance-alert-layer.md`** —— Signal 层:治理信号(发生了什么)
- **`adr/ADR-0032-fcop-audit-protocol-inspection.md`** —— Compiler 层:工具能力(该怎么修的建议)
- **`essays/why-the-protocol-stays-short.md`** —— 为什么 FCoP 不让协议自己生长 —— 与本文"协议工具不动手"是同一道护栏的两端

---

*"看清楚,但不动手 —— 这是一种克制,不是缺陷。"*
