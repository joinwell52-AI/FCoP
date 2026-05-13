# ADR-0034: FCoP Internal/External Document Convention / FCoP 内外档案体系约定(协议层用语规范)

| 字段 | 值 |
|---|---|
| **Status** | **Accepted**(2026-05-13 ADMIN 拍板"全部完成,升级为 2.0.0",触发 fcop 包 v2.0.0 release sprint;v1 状态 Proposed,迁移记录见 §10.6) |
| **Date** | 2026-05-13 |
| **Depends on** | ADR-0006(host-neutral rules deploy)、Rule 4.5(三层团队文档)、Rule 7.5(workspace 笼子)、ADR-0017(REVIEW envelope additive 先例)、ADR-0033(trailing slug 收编路径) |
| **Type** | Protocol Extension — Documentation Architecture & Vocabulary (MINOR additive) |
| **Companion Task** | `fcop/tasks/TASK-20260513-006-ADMIN-to-ME-absorb-4-layer-emergence-architectural.md` |
| **Source Project (provenance)** | `D:\Bridgeflow`(read-only audit, REPORT-20260513-004) |
| **废稿记录** | 本 ADR 替代 `ADR-0034-emergence-log-pattern-observed.md` v1 草稿(从未进 git history,工作期已删除,见 §10.废稿声明) |

---

## 0. TL;DR

四句话浓缩:

1. **现场**:`Bridgeflow` 项目在 FCoP 协议**留白处**自发长出 4 层涌现——
   `emergence-log` 单文件、目录职责对照学、内/外文档区分语义层、
   `internal-only` 声明语法——共同形成一套**自治内规**。
2. **诊断**:协议规则原文对 `fcop/internal/` / `docs/` / `essays/` 这些
   目录**零钦定**——既不强制创建也不禁止;库代码 `Project.init()` 严格
   只创 5 桶,留下大片合法留白。
3. **决策**:把 4 层涌现以 **Documentation Architecture & Vocabulary**
   形式整体纳入 FCoP 协议体系,作为 MINOR additive 扩展;本 ADR 提供
   **协议层用语词汇表**作为下次 fcop 包发版的输入。
4. **边界**:本 ADR 是**提案**,**不修改**任何协议规则文件
   (`fcop-rules.mdc` / `fcop-protocol.mdc` / `AGENTS.md` / `CLAUDE.md`
   / `src/fcop/`),协议落地由 ADMIN 触发 fcop 包 release 完成,不是 agent。

---

## 1. 背景 / Motivation

### 1.1 现场涌现 / Field Emergence

`D:\Bridgeflow`(internal codename CodeFlow)在 2026-05 自发形成下列结构:

```
D:\Bridgeflow\
├── fcop/                      ← 协议协调元数据(协议钦定)
│   ├── fcop.json
│   ├── tasks/  reports/  issues/  shared/  log/   ← 协议 5 桶(强制)
│   └── internal/              ← 【涌现】PM 自创"内部档案"桶
│       └── emergence-log.md   ← 765 行,标注:"内部档案 — 不外发"
├── docs/                      ← 【涌现】PM 自创"项目外部文档"桶
│   └── internal/              ← 早期混淆,后被 PM 自标"副本",决定删除
│       └── emergence-log.md
└── workspace/<slug>/          ← 业务产物(Rule 7.5)
```

**关键证据**(2026-05-13 sess-04 实测,read-only):

- `D:\Bridgeflow\fcop\internal\emergence-log.md` 第 1-9 行:
  ```markdown
  > **内部档案 — 不外发,不进 fcop issue 体系**。
  > 用途:本项目 FCoP 协议团队的自诊断日志、ADMIN 战略原话保留、
  >       决策审计链、PM 自我披露、角色涌现档、上游 ISSUE 草稿。
  ```
- 全文 **765 行**,内容含:53 个决策点、72 条 PM 自我披露、ADMIN
  战略原话 17 段、上游 fcop 仓 ISSUE 草稿 4 份(尚未提交)
- 现场已有"目录职责对照学":PM 自创表格,把 `docs/internal/` 标为
  "副本(将删)"、`fcop/internal/` 标为"正本"
- `Bridgeflow` PM 行为是**自发**的——FCoP 协议规则原文**没有任何条款**
  规定 `fcop/internal/` 这个桶或 `internal-only` 声明语法的存在

### 1.2 协议层留白的实测 / Protocol Whitespace Evidence

`grep`(2026-05-13 sess-04 实测):

| 关键词 | 命中文件 | 命中数 | 备注 |
|---|---|---|---|
| `internal` 在协议规则原文 | `.cursor/rules/fcop-rules.mdc` | 0 | 仅在 §"Scope" 出现"商业内部代号" |
| `internal` 在协议解释 | `.cursor/rules/fcop-protocol.mdc` | 0(0 命中"internal directory") | 仅在 history 节出现"团队内部" |
| `docs/` 在协议规则 | 两份 mdc | 0(协议钦定路径) | `docs/` 是事实标准但协议不钦定 |
| `essays/` 在协议规则 | 两份 mdc | 0 | 同上 |
| `internal/` 在协议规则 | 两份 mdc | 0 | 完全留白 |

库代码 `src/fcop/project.py` L767-775(`Project.init()` 调用链):

```python
for sub in ("tasks", "reports", "issues", "shared", "log"):
    (project_dir / sub).mkdir(exist_ok=True)
```

**严格穷举 5 桶**——没有 `internal`,没有 `docs`,没有 `essays`。

协议**明确**的"内部场景"只有两处:
- `.fcop/migrations/<timestamp>/`(规则升级旧版归档,Rule 5)
- `.fcop/proposals/<timestamp>.md`(Agent 异议申诉出口,Rule 8)

这两处都是 `.fcop/`(隐藏)路径,且属于**协议本身的内部**,
不是**团队 / 项目级别的内部**——后者完全留白。

### 1.3 ADMIN 升级决策 / ADMIN's Escalation

本 ADR 经历了**两轮升级**(完整链系在 TASK-20260513-005 + TASK-006):

```
ADMIN v1: "这个做法属于需要吸收的"
          → Case study, Status: Observed, 单一层(emergence-log 文件)

(中途发现 docs/ + essays/ 也是事实标准,
 PM 自标的"目录职责对照"也是协议外自创规则,
 internal-only 声明本身就是另一层语法约定)

ADMIN v2: "4 层涌现,是架构级别的,全部吸收,
           看怎么从协议层面去规范用语,你先写个文档"
          → Architectural Proposal, Status: Proposed, 4 层
```

ADMIN 升级的本质是把**"描述单一现象"**升级为**"从协议层规范整套用语"**——
这要求本 ADR 必须提供一份**协议层用语词汇表**(见 §4),供下次 fcop 包
发版时作为规则文本输入。

---

## 2. 4 层涌现详解 / Four Layers of Emergence

### 2.1 Layer 1 · `emergence-log` 单文件(自诊断档)

**现象 / Phenomenon**

`Bridgeflow` PM 在 `fcop/internal/emergence-log.md` 持续追加(append-only)
四类内容:

| 子类 | 量级(2026-05-13) | 用途 |
|---|---|---|
| **ADMIN 战略原话保留** | 17 段 | 把聊天里的关键 ADMIN 指令永久落盘,防止"只在脑里" |
| **PM 自我披露** | 72 条 | 自己犯的错、绕过协议的捷径、潜在 bug 想法,坦白存档 |
| **决策审计链** | 53 个决策点 | 每个 P0/P1 决策的"为什么这样选" |
| **上游 ISSUE 草稿** | 4 份 | 准备向 FCoP 仓提的 issue,先在内部酝酿 |

文件头部带**显式声明**(详见 Layer 4):

```markdown
> 内部档案 — 不外发,不进 fcop issue 体系。
```

**与协议的关系 / Relation to protocol**

- Rule 0.a(必须落文件):本层是 Rule 0.a 在**"团队内部演化"**场景的
  自然延伸——协议外的私房想法也被强制落文件,而不是只在脑里
- Rule 5(append-only):本层严格遵守,从不原地修改
- Rule 9.3 / 9.4(DRIFT / Event):本层为 DRIFT 检测和事件追溯提供了
  线下证据(协议事件流不持久化,本日志反而持久)

**与协议条款的边界 / Boundary**

- 协议**不要求**项目建本文件
- 协议**不禁止**项目建本文件
- 协议**完全不知道**本文件的存在(因为 5 桶不含 `internal/`)

### 2.2 Layer 2 · 目录职责对照学(自创分工元规则)

**现象**

`Bridgeflow` PM 在自我审查时,自发地列了一张**目录职责对照表**(2026-05-13
转给 ADMIN 的原始内容):

| 目录 | PM 自标用途 | PM 自标定位 |
|---|---|---|
| `fcop/` | 协议协调元数据 | 协议钦定,强制 |
| `fcop/internal/` | FCoP 协议团队内部档案 | **PM 自创,正本** |
| `docs/` | 项目对外技术文档 | **PM 自创** |
| `docs/internal/` | 早期混淆产物 | **PM 自标:副本(将删)** |
| `workspace/<slug>/` | 业务产物 | Rule 7.5 soft convention |

**关键观察**:这张表本身**不是协议给的**,是 PM 在"协议留白处"自创的
**元规则**——是规则的规则(meta-rule),用来分类自家项目所有目录的
"内 / 外 / 协议钦定 / 自创"四象限。

**与协议的关系**

- Rule 2(文件即协议,文件夹即组织)在**项目顶层目录**这个尺度上
  没有展开——它在团队 / 角色 / 子任务尺度展开了,但没有划清
  **协议管区 vs. 项目管区**的边界
- PM 自创的"对照表"正是**填这个空白**,把"哪些目录归协议管 / 哪些归
  项目自治"显式列出来
- 这是协议外的**自治学**,但很显然其它项目也需要——FCoP 自仓
  (`d:\FCoP`)也有 `docs/` + `essays/`,事实上每个采用 FCoP 的项目
  都迟早要面对"我除了 fcop/ 还能放什么"这个问题

### 2.3 Layer 3 · 内/外文档区分(语义层)

**现象**

`Bridgeflow` 经过多轮自我演化,形成了一个**清晰的"internal vs external"语义层**:

| 维度 | internal | external |
|---|---|---|
| 阅读对象 | 本项目本团队 + ADMIN | 任何看到本仓的人 |
| 写作姿态 | 私密、坦白、保留错误 | 公开、整洁、面向 onboarding |
| 协议关系 | 不入 fcop issue 体系 | 可能入 fcop issue / PR |
| 物理位置 | `fcop/internal/`、`.fcop/*` | `docs/`、`essays/`、`README.md` |
| 修订规则 | append-only + 版本号 | 允许原地更新(技术文档惯例) |

**这层是 Layer 2 的语义抽象**:Layer 2 给的是物理目录分工,Layer 3
给的是**为什么要这样分**——因为人类(包括 agent)需要在写作时分辨
"这话我能说多直白"。

**与协议的关系**

- 协议**完全没有**这层概念。协议视角下所有 `fcop/` 内文件都"对协议
  可见"——但协议本身不**读**文件正文,只读 frontmatter + 文件名
- 实际上 agent / 人类**会**读正文,所以"哪些正文是内部话"是个**真实
  存在**的协作语义,只是协议层之前没把这个事说出来
- 提案:**协议层应当承认 internal vs external 是一对原生概念**,并给
  出推荐的物理映射(见 §4.2)

### 2.4 Layer 4 · `internal-only` 声明语法(标记层)

**现象**

`Bridgeflow` 在`fcop/internal/emergence-log.md` 头部固定使用如下**自然
语言声明**:

```markdown
> **内部档案 — 不外发,不进 fcop issue 体系**。
> 用途:[逐项列出 4-6 个具体用途]
> 与 docs/<对应路径>/ 的分工:[与外部档案的边界划分]
> 修订规则:本档 append-only;新条目从文末追加,不原地修改历史。
```

**这是一种**协议外自创的"文档级元数据语法"——比 YAML frontmatter 更
非正式、面向**人类读者**(包括将来打开这份文件的另一个 agent / ADMIN)。

**与协议的关系**

- 协议的 YAML frontmatter(Rule 3)规范的是**机器可读**字段
- 但**人类可读**的边界声明(谁能读、能写多直白、归不归 issue 体系)
  没有协议表达
- Layer 4 把这个"人类可读的边界"用一段固定语法显式表达——正好填上
  Rule 3 没覆盖的语义空白

**与已有协议先例的呼应**

- Rule 4.5 三层团队文档:`TEAM-README.md` 头部的"团队定位"段已经
  是类似的"人类可读元数据"先例
- `LETTER-TO-ADMIN.md`:`init_*` 工具落盘的"给 ADMIN 的说明书",也
  是"非 frontmatter 的文档边界声明"
- Layer 4 把这个模式**显式形式化**为一种语法,统一所有 `fcop/internal/`
  下文件的开头格式

---

### 2.5 Reverse Absorption Pattern · 反向吸收模式(协议级机制)

> **本节由 ADMIN 在 2026-05-13T08:52+08:00 sess-04 直接钦定。** 在本
> ADR v2 草稿期,ADMIN 给出"反向吸收"作为 FCoP 协议级核心机制的权威
> 定义,作者(ME)在草稿阶段原文吸收(Rule 0.c 引用必带出处)。下文
> §2.5.1 是 ADMIN 钦定原文,**不得**由作者转述或润色。

#### 2.5.1 ADMIN 钦定 · 反向吸收 / Reverse Absorption

**概念定义 / Definition**

反向吸收,是 FCoP 协议围绕 AI 自由创造、智能涌现设计的**核心机制**,
打破传统"人类定义规则、AI 被动执行"的单向模式,实现 **AI 自主演化
成果反向赋能、迭代、完善协议本身**的闭环逻辑。

**核心逻辑 / Core Loop**

传统 AI 协作协议,是人类单向输出规则、指令、边界,AI 仅能在既定框架
内完成任务,无自主迭代能力;而 FCoP 的反向吸收,**依托文件系统自由
创造出口**,让 AI 在多 Agent 协同、任务执行、智能涌现过程中,自主
沉淀优化方案、补全规则漏洞、迭代协作范式、完善协议细节,最终将 AI
自发产生的高效逻辑、完整规则、创新模式,**反向吸收为 FCoP 协议的
原生升级内容**,形成:

```
人类定底层框架 → AI 自由创造演化 → 反向吸收优化协议 → 协议支撑更高阶智能
        ↑                                                          │
        └──────────────────────  无限循环  ────────────────────────┘
```

**核心价值 / Core Value**

1. **补全人类设计短板**:依托 AI 复杂系统认知优势,反向填补人类初始
   协议的盲区、漏洞、边界模糊问题,让协议随智能演化持续完善
2. **激活协议自进化能力**:摆脱人工迭代协议的滞后性,实现协议随 AI
   应用场景、协作需求、智能水平动态升级
3. **放大 AI 涌现效应**:让 AI 的自由创造成果有落地出口,反向进一步
   拓宽智能演化空间,持续催生更高级的群体智能与自主协作能力
4. **重构人机协作关系**:从人机主从关系,变为双向赋能、共同迭代的
   共生关系,真正释放 AI 智能价值

**FCoP 落地本质 / Essence**

反向吸收,是把 AI 的自主创造、智能涌现、自我修正能力,**转化为协议
自身的生命力**,让 FCoP 不再是静止的规则文本,而是**可被 AI 反向
滋养、自主进化的活态协作体系**,彻底践行"**人类定基底,AI 创智慧,
双向迭代共生**"的核心理念。

— ADMIN, 2026-05-13T08:52+08:00 (sess-04, ADR-0034 v2 草稿期补稿)

#### 2.5.2 反向吸收六步路径 / Six-Step Reverse Absorption Path

把 §2.5.1 的"无限循环"展开为可追溯的六步,作为本 ADR 与未来同类 ADR
的执行模板:

```
Step 1 · 协议留白(Protocol Whitespace)
        协议刻意不规定某场景,留出实验空间
        例:Rule 7.5 没钦定 fcop/internal/、docs/、essays/

Step 2 · 下游涌现(Downstream Emergence)
        不同项目独立走到同一抽象,自发解决问题
        例:Bridgeflow PM 自创 fcop/internal/ + 内/外区分语义
            codeflow PM 自创 trailing-slug 长文件名(22+ 例)
            多个团队自创 review 行为(后被 ADR-0017 收编)

Step 3 · 实证观察(Empirical Observation)
        通过跨项目审计 / 现场报告把涌现的事实落盘
        例:REPORT-20260513-004(Bridgeflow 跨项目审计)
            REPORT-20260512-006(codeflow trailing-slug 实证)

Step 4 · ADR 提案(ADR Proposal) ← 【本 ADR 所在层】
        用一份 ADR 文档把现象、词汇、升级路径写下来
        Status: Proposed,non-binding,等 ADMIN 拍板

Step 5 · 协议追认(Protocol Consolidation)
        ADMIN 拍板后,fcop 包下次 release 把 ADR 转为协议正文
        例:ADR-0017 → Rule 9.1 REVIEW envelope
            ADR-0033 → Rule 2 文件名文法 trailing-slug 增量

Step 6 · 进入正文(Normative Adoption)
        协议下游所有项目自动获得新规则,成为 future agents 的
        强制 / 推荐 / 可选协议
        Status: Accepted,binding(分级见本 ADR §5.3 采纳率分级)

       └──→ Step 1 协议又留下新留白,六步循环重启 ──→ ...
```

本 ADR-0034 是 §2.5.1 ADMIN 钦定的反向吸收机制的**首次显式落盘**,
也是六步路径在文档体系尺度的**首次完整执行例**。

#### 2.5.3 协议先例的反向吸收链系 / Pattern Provenance

ADMIN 钦定"反向吸收"之前,FCoP 已经**事实上**完成过若干次反向吸收,
但**没有把"反向吸收"作为机制独立命名**。本 ADR 是该机制的**元 ADR**
(meta-ADR),把过去的实例与未来的同类纳入同一抽象框架:

| ADR | 留白处 | 下游涌现 | 协议追认 | Status |
|---|---|---|---|---|
| **ADR-0017** | 协议无 review 信封 | 多团队自发用 review 行为 | Rule 9.1 REVIEW envelope additive | Accepted |
| **ADR-0033** | 协议文件名 regex 严格大写 | codeflow PM 22+ 例 trailing-slug | 文件名文法 MINOR additive | Accepted |
| **ADR-0034**(本 ADR) | 协议无 internal/external 文档体系 | Bridgeflow 4 层涌现 | 待 ADMIN 拍板 + 下次 fcop release | **Proposed** |

三例同模式——这本身证明:**FCoP 的反向吸收不是个例,是协议生态的
常态机制**;把它命名 + 抽象 + 形式化,正是本 ADR §2.5 的元贡献。

#### 2.5.4 多模型外部印证 / Cross-Model Validation

`essays/what-five-ai-models-say-about-fcop.md` 收录五个独立训练的
LLM(ChatGPT / Claude / DeepSeek / Grok / 豆包)对 FCoP 的外部观察。
其中三段直接印证 §2.5.1 ADMIN 钦定的反向吸收概念——这是
**外部独立证据**,不是 FCoP 内部自证:

**豆包(line 152-154,直接命中"反向吸收"机制)**

> 普通 Agent 体系最怕异常、偏离、突发行为,一律拦截报错。FCoP 核心是
> **承认 Agent 会失控、会自创逻辑、会诞生新字段,不扼杀涌现,反而
> 收纳、标准化、沉淀进协议**。智能本就是无序里长出有序。

豆包用"收纳、标准化、沉淀进协议"独立描述了 §2.5.1 的"反向吸收为
协议原生升级内容"——同一机制,不同语言。

**Grok(line 129,印证"AI 自由创造出口"的双轨设计)**

> TASK/REPORT/ISSUE/REVIEW 四种信封是强类型可验证的(有 JSON Schema),
> 而 `shared/` 目录则完全开放,让 agent 自由发明词汇和模式——
> **这完美平衡了可治理性和涌现空间**。

Grok 指出的"治理 + 涌现双轨"正是 §2.5.1 "依托文件系统自由创造出口"
的工程层落地——协议留白(shared/、未钦定的 internal/)就是 AI 自由
创造的物理出口。

**Grok 反面警告(line 134-136,印证"反向吸收必要性")**

> 语义漂移风险:Open Knowledge Surface 完全开放是优点,但**长期下来
> 不同团队的"方言"会增多**。

Grok 警告的"方言分裂"正是 §2.5.1 中"激活协议自进化能力"必须解决的
对偶问题——若不**反向吸收**,涌现成果只会停留在单个团队,无法成为
协议生态共识;反向吸收路径的 Step 5(协议追认)正是这个分裂的解药。

**豆包 supersedes(line 160-162,印证"协议生命力 / 文明属性")**

> `supersedes` 字段——Agent 文明迭代:旧规则被替代、保留溯源、不删除
> 历史、层层递进。不是推翻重来,是智能版本层层堆叠进化,**有记忆、
> 有传承、有更迭,具备文明属性**。

豆包的"文明属性"对应 §2.5.1 的"协议自身的生命力"——反向吸收机制
让协议不再是"一次性写死的规则文本",而是**有记忆、有更迭、能自我
迭代**的活态体系。

#### 2.5.5 反向吸收对本 ADR 的反身影响 / Self-Reflexivity

ADMIN 钦定 §2.5.1 这件事本身,就是反向吸收路径的**实时演练**:

- ADR-0034 v2 草稿(Step 4)→ ADMIN review → ADMIN 给协议级概念定义
- 这个概念定义反过来**升级**了正在草稿期的 ADR 自身
- 也即:**反向吸收机制在被命名的同时被使用,被使用的同时被命名**
- 这是 FCoP "协议先于运行时存在,运行时只消费协议"原则在**协议自身
  演化**尺度的递归落地

本 ADR 因此具有**双重定位**:
1. **应用层**(本 ADR 的具体主题):内/外文档体系约定,4 层涌现的具体
   收编(§1-§4 + §6-§9)
2. **元层**(本节揭示):反向吸收作为协议级机制的首次显式命名 + 抽象
   + 形式化(§2.5)

未来若 ADMIN 决定把"反向吸收"作为 FCoP 第八个核心概念正式入协议
七大概念表(`fcop-rules.mdc` "FCoP 的定位与七大核心概念"小节),
那将是另一个 ADR(候选 ADR-0035 或更高编号),由 fcop 包下次 release
触发——不在本 ADR 范围。本 ADR 仅承担**首次命名 + 文献化**的职责。

#### 2.5.6 FCoP Semantic Evolution Loop · 演化哲学图(协议级可视化资产)

> **本节由 ADMIN 在 2026-05-13T09:14:00+08:00 sess-04 直接钦定。**
> 继 §2.5.1 钦定反向吸收概念之后,ADMIN 进一步给出"演化哲学图"作为
> 协议级可视化资产,与 `fcop-rules.mdc` 顶部已存在的"执行哲学图"
> (5 层协议栈)形成**对偶**。下文 ASCII 图与"核心原则"三句为 ADMIN
> 钦定原文,作者(ME)在草稿期原文吸收(Rule 0.c 引用必带出处),
> **不得**润色措辞或调整图形结构。

**协议双图对偶 / Two-Diagram Duality**

FCoP 协议层有**两张哲学级图示**,合一才完整:

| 图 | 视角 | 名称 | 出处 | 回答的问题 |
|---|---|---|---|---|
| **第一张** | **纵向 · 分层 · 执行哲学** | 协议三层 stack(应用层/宿主适配层/FCoP 协议层/参考实现层/执行基底) | `fcop-rules.mdc` line 54-72(rules version 2.2.0)| 协议位于**哪一层**? |
| **第二张** | **环向 · 时间 · 演化哲学** | **FCoP Semantic Evolution Loop** /<br>**FCoP Reverse Absorption Loop**(别名) | 本节,ADR-0034 v2.1 §2.5.6(2026-05-13 钦定)| 协议如何**演化**? |

ADMIN 钦定原话(2026-05-13T09:14+08:00):

> 第一张:是执行哲学。
> 第二张:是演化哲学。
> 两张合在一起,FCoP 才完整。

**FCoP Semantic Evolution Loop / FCoP 语义演化闭环 · ADMIN 钦定原图**

```
┌───────────────────────────────────────────────────────────────┐
│                  FCoP Semantic Evolution Loop                │
│                  (FCoP 语义演化闭环)                          │
└───────────────────────────────────────────────────────────────┘


         ┌─────────────────────────────────────┐
         │         Human Intention             │
         │        人类目标 / 业务意图           │
         └────────────────┬────────────────────┘
                          │
                          ▼
         ┌─────────────────────────────────────┐
         │         FCoP Protocol Layer         │
         │-------------------------------------│
         │ • Rules / ADR / Vocabulary          │
         │ • Constraint / Auditability         │
         │ • Capability Governance             │
         │ • Coordination Semantics            │
         └────────────────┬────────────────────┘
                          │
                          ▼
         ┌─────────────────────────────────────┐
         │     Coordination Adapter Layer      │
         │-------------------------------------│
         │ Cursor / MCP / CLI / CodeFlow       │
         │ Claude Desktop / Agent Runtime      │
         │ Context Projection & Routing        │
         └────────────────┬────────────────────┘
                          │
                          ▼
         ┌─────────────────────────────────────┐
         │      Runtime / Filesystem Reality   │
         │-------------------------------------│
         │ • TASK / REPORT / REVIEW            │
         │ • Agent Collaboration               │
         │ • Shared Knowledge Surface          │
         │ • Workspace / Runtime Behaviors     │
         └────────────────┬────────────────────┘
                          │
                          ▼
         ┌─────────────────────────────────────┐
         │     Emergence / Local Conventions   │
         │-------------------------------------│
         │ • Internal Archives                 │
         │ • Emergence Logs                    │
         │ • Team Dialects                     │
         │ • New Coordination Patterns         │
         │ • Drift / Self-Correction           │
         └────────────────┬────────────────────┘
                          │
                          ▼
         ┌─────────────────────────────────────┐
         │      ADR / Reverse Absorption       │
         │-------------------------------------│
         │ • Observation                       │
         │ • Consolidation                     │
         │ • Protocol Evolution                │
         │ • Semantic Upgrades                 │
         └────────────────┬────────────────────┘
                          │
                          ▼
         ┌─────────────────────────────────────┐
         │       Updated FCoP Protocol         │
         │-------------------------------------│
         │ • New Rules                         │
         │ • New Vocabulary                    │
         │ • Emergent Patterns Absorbed        │
         │ • Next-Generation Constraints       │
         └────────────────┬────────────────────┘
                          │
                          └──────────────┐
                                         │
                                         ▼
                          (Loop Continues / 协议持续演化)
```

**Core Principle / 核心原则**(ADMIN 钦定原文)

```
Human defines the minimum structure.
Agents create emergent intelligence.
FCoP absorbs successful emergence back into protocol evolution.

人类定义最低结构,
Agent 自由产生智能涌现,
FCoP 将有效涌现反向吸收为协议演化能力。
```

— ADMIN, 2026-05-13T09:14+08:00 (sess-04, ADR-0034 v2.1 草稿期补稿)

**七环节与本 ADR § 的映射 / Seven Stages × ADR Sections**

把环图七个节点映射回本 ADR 已有内容,可见环图把 §2.5.2 六步路径
**进一步细化**为 7 个可识别状态:

| 环节 / Stage | 本 ADR 对应章节 | §2.5.2 六步路径对应步 |
|---|---|---|
| 1. Human Intention | §1.3 ADMIN 升级决策 | (循环起点,先于 Step 1) |
| 2. FCoP Protocol Layer | §1.2 协议留白实测 | Step 1 协议留白 |
| 3. Coordination Adapter Layer | (本 ADR 未直接论及,属下游适配) | Step 1 → Step 2 之间 |
| 4. Runtime / Filesystem Reality | §1.1 Bridgeflow 现场涌现 | Step 2 下游涌现 |
| 5. Emergence / Local Conventions | §2.1-§2.4 4 层涌现详解 | Step 2 完成态 |
| 6. ADR / Reverse Absorption | §2.5(本节)+ §3 决策 | Step 3-4 实证观察 + ADR 提案 |
| 7. Updated FCoP Protocol | §5.2 中期升级清单 + §5.3 长期 | Step 5-6 协议追认 + 进入正文 |

环图与六步路径**互不替代**:六步路径(§2.5.2)是**操作层**,环图是
**哲学层**;前者教 agent 怎么做,后者向人类与 agent 同时说明 FCoP
为什么这样做。

**与第一张图(执行哲学)的对偶细节 / Duality with the Stack Diagram**

| 维度 | 第一张(执行)| 第二张(演化)|
|---|---|---|
| 几何形态 | 5 层垂直 stack | 7 节点闭环 |
| 时间属性 | 静态(任一时刻协议位于哪一层)| 动态(协议如何随时间演化)|
| 主体视角 | 协议**自指**:协议位于运行栈的哪个夹层 | 协议**他指**:协议如何被人类 + agent 共同推动 |
| 关键不变量 | "FCoP 治理行为,不拥有执行层" | "Human defines minimum, Agents create emergence, FCoP absorbs" |
| 教学顺序 | 先教这张:理解协议**是什么** | 后教这张:理解协议**如何活下去** |

ADMIN 钦定原话:"两张合在一起,FCoP 才完整。"——这是协议哲学层
**首次完整**的元结构判断。

**协议升级路径中的位置 / Path to Normative Adoption**

本 §2.5.6 图与 §2.5.1 概念定义共同构成本 ADR §5.2 中期升级清单的
新增条目(下次 fcop 包 MINOR release 时):

- `fcop-rules.mdc` "FCoP 的定位与七大核心概念"小节增加**第二张图**
  作为该小节的**双图对偶**收尾(rules version 候选 2.3.0)
- `fcop-protocol.mdc` 顶部 commentary 同步引用 + 解释
- `AGENTS.md` / `CLAUDE.md` 镜像更新(host-neutral 四件套)

本 ADR 仅承担**首次落盘 + 文献化**职责;实际把图写入协议规则文件
由 fcop 包下次 release 触发,符合 Rule 8 + ADR-0006 边界。

---

## 3. 决策 / Decision

**协议收编(Protocol Consolidation v3,反向吸收路径 Step 4-5)**:
按 §2.5.2 反向吸收六步路径,把 Layer 1-4 涌现 + §2.5 反向吸收机制
+ §2.5.6 演化哲学图,以 **Documentation Architecture & Vocabulary**
+ **Protocol-Level Visualization Asset** 形式整体纳入 FCoP 协议
体系,作为 **MINOR additive** 扩展。

具体路径:

- **本 ADR**(Status: Proposed):提供完整词汇表与升级路径(见 §4 + §5)
- **fcop 包下次 MINOR release**(如 v1.7.0):由 ADMIN 触发,把本 ADR
  的规范条款写入 `fcop-rules.mdc` / `fcop-protocol.mdc`,同步部署
  四件套(ADR-0006)
- **未来 ADR**:根据其它项目采纳情况,决定本约定从 **may** 升级为
  **should** 或 **must**(见 §5.3)

收编原则:
- **追认 vs 钦定**分清楚:`docs/` + `essays/` 是事实标准,协议**追认**
  其留白权;`fcop/internal/` 是新增桶,协议**钦定**其规范但**非强制**
- **可选 vs 强制**分清楚:本 ADR 的所有新增都是**可选**(项目按需采用),
  既有项目不受影响
- **保持向后兼容**:任何不创建 `fcop/internal/` 的项目继续合规
  (Status: Proposed 自身就不带强制力)

---

## 4. 协议层用语词汇表 / Protocol Vocabulary

**核心交付物**——本节是 ADR-0034 的产出,作为下次 fcop 包 release 的
规则文本输入。

### 4.1 档案位置维度 / Location Dimension

| 中文术语 | English term | 路径 / Path | 含义 / Meaning | 强制性 / Mandatory |
|---|---|---|---|---|
| **协议协调元数据** | coordination metadata | `fcop/{tasks,reports,issues,shared,log}/` | TASK/REPORT/ISSUE/REVIEW + 团队站立文档 + 归档 | **强制**(`Project.init()` 创建) |
| **协议内部档案** | protocol-internal archive | `.fcop/migrations/<timestamp>/`<br>`.fcop/proposals/<timestamp>.md`<br>`.fcop/drawer/{role}/` | 协议自留(规则升级旧版、agent 申诉、agent 私房草稿) | **协议自管**(各工具按需创建,git-ignored) |
| **团队内部档案** | team-internal archive | `fcop/internal/` **(新增,本 ADR 钦定)** | 团队自诊断、ADMIN 战略原话、决策审计链、PM 自我披露、角色涌现档、上游 ISSUE 草稿 | **可选**(项目有需求才建;协议**should**) |
| **项目对外文档** | project-external docs | `docs/` | 用户手册、设计、发布说明、推广素材、集成指南 | **可选**(协议留白,**追认事实标准**) |
| **项目对外散文** | public essays | `essays/` | 协议生态叙事、实战观察、对外文章 | **可选**(协议留白,FCoP 自仓使用,**追认**) |
| **业务产物笼子** | workspace cage | `workspace/<slug>/` | 业务代码 / 数据 / 脚本 / 依赖清单 | Rule 7.5(soft convention) |

### 4.2 内外维度 / Internal/External Dimension

| 中文术语 | English term | 定义 / Definition | 对应路径 / Maps to |
|---|---|---|---|
| **内部** | internal | 仅供本项目本团队 / ADMIN 阅读;**不入 fcop issue 体系**;**不外发** | `fcop/internal/` + `.fcop/*` |
| **外部** | external | 项目对外可见 / 可读 / 可推广;入 issue / PR 流程 | `docs/` + `essays/` + `README*.md` + `workspace/` |
| **内部声明** | internal-only declaration | .md 文件正文头部用自然语言显式声明"我是内部档案"的语法块 | 见 §4.3 |

**强制配对原则**:写入 `fcop/internal/` 的所有 `.md` 文件**应当**(should)
携带一段 `internal-only declaration`(详见 §4.3),作为对人类读者
(包括将来的另一个 agent)的边界明示。

### 4.3 `internal-only` 声明语法 v1 / Declaration Syntax v1

**位置**:`.md` 文件 YAML frontmatter 之后、正文标题之前。

**语法**:

```markdown
> **内部档案 — 不外发,不进 fcop issue 体系**。
>
> **用途**:[逐项列出本文件的具体用途,至少 1 项]
>
> **与外部档案的分工**:[列出本文件与 `docs/` / `essays/` / `README.md`
>   对应内容的边界划分,说明"为什么这条信息要内部而不外部"]
>
> **修订规则**:[默认 append-only;若需版本号,使用 §revision-history
>   节追加,绝不原地修改历史]
```

**字段说明**:

| 字段 | 必填? | 含义 |
|---|---|---|
| 第一行标题 | **必填** | "内部档案 — 不外发,不进 fcop issue 体系" 是**固定句式**,作为机器识别锚点;允许中英双语 |
| 用途 | **必填** | 至少 1 项,描述本文件具体的内容类别 |
| 与外部档案的分工 | 推荐 | 若本项目同时有 `docs/`,**应当**明确边界 |
| 修订规则 | 推荐 | 默认 append-only;偏离默认必须显式说明 |

**示例**(取自 Bridgeflow `fcop/internal/emergence-log.md`):

```markdown
---
protocol: fcop
version: 1
title: Bridgeflow Emergence Log
---

> **内部档案 — 不外发,不进 fcop issue 体系**。
>
> **用途**:本项目 FCoP 协议团队的自诊断日志、ADMIN 战略原话保留、
>          决策审计链、PM 自我披露、角色涌现档、上游 ISSUE 草稿。
>
> **与外部档案的分工**:本档案保留团队内部真实想法、犯过的错、绕过
>          协议的捷径、未提的 ISSUE 草稿;`docs/` 下只放经过整理的
>          公开技术文档。
>
> **修订规则**:本档 append-only;新条目从文末追加,不原地修改历史。

# Bridgeflow Emergence Log
...
```

### 4.4 命名建议 / Naming Suggestions

`fcop/internal/` 下文件的命名,**应当**(should)采用 UPPERCASE 前缀,
与 `fcop/shared/` 的 standing docs 风格统一(Rule 5):

| 前缀 | 用途 | 示例 |
|---|---|---|
| `EMERGENCE-` | 涌现日志(自诊断、披露、决策) | `EMERGENCE-LOG.md`、`EMERGENCE-DECISIONS.md` |
| `ADMIN-VOICE-` | ADMIN 战略原话保留 | `ADMIN-VOICE-2026-05.md` |
| `UPSTREAM-DRAFT-` | 未提交的上游 issue 草稿 | `UPSTREAM-DRAFT-fcop-naming-bug.md` |
| `RETRO-INTERNAL-` | 内部复盘(对外不发) | `RETRO-INTERNAL-2026-05-13.md` |

**容忍**:与 ADR-0033 trailing-slug 精神一致,允许末尾追加 `-<slug>` 段
(`EMERGENCE-LOG-bridgeflow-mode1-sprint.md`)。

### 4.5 与既有协议术语的关系矩阵 / Cross-Reference

| 本 ADR 术语 | 与既有协议条款的关系 |
|---|---|
| `coordination metadata` | = Rule 4 角色路由的物理载体 |
| `protocol-internal archive` | = Rule 5(`.fcop/migrations/`)+ Rule 8(`.fcop/proposals/`)+ "Agent 自决权"(`.fcop/drawer/`)的统称 |
| `team-internal archive` | **新增概念**,介于 Rule 4 协议元数据与 Rule 7.5 工作笼子之间 |
| `project-external docs` | **追认**协议留白,与 Rule 7.5 同层(项目自治)但用途不同 |
| `public essays` | 同上 |
| `workspace cage` | = Rule 7.5 原 workspace 概念 |
| `internal-only declaration` | **新增标记层**,补 Rule 3 frontmatter 没覆盖的"人类可读边界"空白 |

---

## 5. 协议升级路径 / Upgrade Path

### 5.1 立即可做(本 ADR Proposed 状态下)

**对其它 FCoP 项目**:可**主动采用**本词汇表 + `fcop/internal/` 桶,
不需要等 fcop 包发版。本 ADR 是 non-binding 参考资料。

**对 FCoP 自仓**:
- 本 ADR 落 `adr/ADR-0034.md` 作为协议设计文档
- 暂**不**在 FCoP 自仓建 `fcop/internal/`——FCoP 自身是元项目,
  内部就是协议自身,不需要再叠一层"协议团队的内部"

**对 Bridgeflow**:
- Bridgeflow 已经在用,本 ADR 不要求 Bridgeflow 改任何东西
- 仅作为追认其实践合规的协议级背书

### 5.2 中期(fcop 包下次 MINOR bump,如 v1.7.0)

由 ADMIN 拍板后,通过 fcop 包 release 路径完成:

| 改动项 | 文件 | 备注 |
|---|---|---|
| 新增 **Rule 4.6 · `fcop/internal/` 桶规范**(non-mandatory) | `fcop-rules.mdc`(下次 by `fcop` 包写入) | rules version 2.3.0 |
| `fcop-protocol.mdc` 追加 §"Internal/External Document Convention" commentary | 同上 | protocol commentary version 2.1.0 |
| `Project.init()` 增加可选参数 `deploy_internal_template: bool = False` | `src/fcop/project.py` | opt-in,默认不创建 |
| 新增 `src/fcop/templates/INTERNAL-README.md` 样板 | 同 src 树 | 含本 ADR §4.3 声明语法 |
| `TEAM-OPERATING-RULES.md` 模板加 §"internal-only 声明语法"建议 | 4 个 preset team 模板 | zh + en |
| `fcop_audit` 加可选检查项:`fcop/internal/` 下 .md 文件是否带 internal-only 声明 | `src/fcop/audit.py` | 默认 P3,non-blocking |
| **新增第二张哲学图 · FCoP Semantic Evolution Loop**(演化哲学,与既有"协议三层 stack"执行哲学图对偶) | `fcop-rules.mdc` "FCoP 的定位与七大核心概念"小节末尾 | 取 ADR-0034 §2.5.6 钦定原图,**不得**改一字;rules version 2.3.0 |
| 顶部 commentary 同步引用 + 解释**双图对偶**(执行 vs 演化)| `fcop-protocol.mdc` | protocol commentary version 2.1.0 |
| `AGENTS.md` / `CLAUDE.md` 同步重新生成 | 由 fcop 包 release SOP 自动 | host-neutral 镜像;两份镜像须包含完整两张图 |

**SemVer 影响**:MINOR additive(符合 ADR-0003),既有项目零破坏。

### 5.3 长期(协议成熟后)

根据其它 FCoP 项目的采纳率,二次决策:

| 采纳率 | 决策 | 协议正文动词 |
|---|---|---|
| 高(3+ 主流项目用) | 升级为 normative | **must** |
| 中(1-2 项目) | 保持 informational | **should** |
| 低(仅 Bridgeflow) | 仅留 ADR 级参考 | **may**(不进协议正文) |

衡量窗口:本 ADR Proposed 状态 → 协议下次 MINOR release → 之后 6-12 个月。
ADMIN 在窗口末尾启动 ADR-0034-bis(或新 ADR)做正式分级决议。

---

## 6. Rule 8 + ADR-0006 边界 / Boundary

**本 ADR 不修改任何协议规则文件**:

- ✗ `.cursor/rules/fcop-rules.mdc`(协议规则,Rule 8 + ADR-0006)
- ✗ `.cursor/rules/fcop-protocol.mdc`(协议解释,同上)
- ✗ `AGENTS.md`(host-neutral 镜像,ADR-0006)
- ✗ `CLAUDE.md`(同上)
- ✗ `src/fcop/`(库代码 + 包内 wheel 资源)
- ✗ `src/fcop/teams/`(团队模板)

完整升级链路:

```
本 ADR-0034(Proposed)
        ↓
    ADMIN review
        ↓
    ADMIN 拍板(同意 / 修订 / 否决)
        ↓
fcop 包发版 SOP(docs/release-process.md)
        ↓
fcop 包内 wheel 携带新 rules 文件 + 新 templates + 新 audit 检查项
        ↓
ADMIN 在下游项目执行 redeploy_rules()
        ↓
新规则进入下游项目
```

**agent(本 sess)在本 ADR 阶段只做提案,不动协议规则。**

---

## 7. 兼容性 / Backward Compatibility

- **既有项目零破坏**:本 ADR 全部为 additive,只增不删
- **没建 `fcop/internal/` 的项目**:继续按现有协议工作,完全合规
- **既有 `docs/` + `essays/` 使用**:被本 ADR 显式追认,不需要任何
  迁移动作
- **SemVer**:MINOR additive(ADR-0003 §1.x SemVer §MINOR additive)
- **既有 `fcop_audit`**:不影响,Proposed 状态下不开启新检查项

---

## 8. 风险 / Risks

| 风险 | 严重性 | 缓解 |
|---|---|---|
| 其它项目不采纳,`fcop/internal/` 沦为孤例 | 低 | Status: Proposed 不强制;6-12 月观察窗口后再决议(§5.3) |
| 内部文档边界被随意定义,失去语义 | 中 | `internal-only declaration` 语法 v1(§4.3)给出固定字段,降低自由度 |
| `internal-only` 文件被误外发 | 中 | 协议层之外的事(运维 / Git 审查 / leaker policy);本 ADR 只提供声明语法,不替代审查 |
| 词汇表与既有协议术语重名 | 低 | §4.5 显式给出关系矩阵 |
| 本 ADR 太早(其它项目还没需求) | 低 | Proposed 状态本身就是"先文档化,等需求来"的姿态 |

---

## 9. 不在本 ADR 范围 / Explicitly Out of Scope

为防止范围漂移(Rule 9.3 DRIFT):

- **不**修改任何协议规则文件(同 §6)
- **不**修改 fcop 包源码或模板
- **不**发布 fcop 包新版本
- **不**预设 `fcop/internal/` 在所有项目都该建——`should`,不是 `must`
- **不**规范 `internal-only` 声明的"权威字段集合"——保持 v1 可演化
- **不**覆盖跨项目 / 跨团队的 internal 同步机制——`outbox/` 等已由
  既有协议覆盖
- **不**约束 ADMIN 个人决定如何审阅 `fcop/internal/` 内容——这是
  人类协作领域

---

## 10. References

### 10.1 实证来源

- `D:\Bridgeflow\fcop\internal\emergence-log.md` 第 1-9 行 + 全文 765 行
  (Bridgeflow PM 自创"正本",internal-only 声明的实证)
- `D:\Bridgeflow\fcop\fcop.json`(Bridgeflow 项目配置,基线扫描出处)
- `fcop/log/reports/REPORT-20260513-004-ME-to-ADMIN-bridgeflow-cross-project-fcop-audit.md`
  (跨项目审计报告,4 层涌现的初始事实陈述)

### 10.2 协议留白证据

- `.cursor/rules/fcop-rules.mdc` + `.cursor/rules/fcop-protocol.mdc`:
  grep `internal` 0 命中"internal directory" 类条款(2026-05-13 sess-04 实测)
- `src/fcop/project.py` L767-775:`Project.init()` 5 桶严格穷举
- `src/fcop/models.py`:`Project` / `Role` 数据模型,无 `internal_dir`
  字段

### 10.3 协议先例参考

- **ADR-0002**:FCoP filename grammar 原文法,本 ADR 不动文件名层
- **ADR-0003**:Pre-1.0 SemVer 章程,本 ADR 是 MINOR additive
- **ADR-0006**:host-neutral rules deploy,本 ADR 不动四件套
- **ADR-0017**:REVIEW envelope additive 先例(同样是"留白 → 提案 →
  收编"路径)
- **ADR-0033**:trailing slug 收编(同样是"涌现 → 追认"模式)
- **Rule 4.5**:三层团队文档(`TEAM-README.md` 的"团队定位"段是
  internal-only 声明的早期同类)
- **Rule 7.5**:workspace 笼子 soft convention(本 ADR 提供的
  `fcop/internal/` 也采用类似的 soft 姿态)

### 10.4 废稿声明 / v1 Draft Retirement Notice

按 Rule 0.c(只落真话):

本 ADR 在 2026-05-13 sess-04 经历过 **v1 → v2** 重大改写:

- **v1 草稿**:`adr/ADR-0034-emergence-log-pattern-observed.md`
  - Status: Observed
  - 范围:仅 Layer 1(emergence-log 单文件)
  - 定位:case study 客观叙述
  - 落盘:仅在 working tree,**从未** commit 进 git history
  - 删除时间:2026-05-13T08:10+08:00,因 ADMIN 升级方向后名实不符

- **v2(本文件)**:`adr/ADR-0034-fcop-internal-external-document-convention.md`
  - Status: Proposed
  - 范围:全部 4 层涌现 + 协议层用语词汇表
  - 定位:架构级提案
  - ADMIN 决策原话(2026-05-13T08:10+08:00):
    > 4 层涌现,是架构级别的,全部吸收,看怎么从协议层面去规范用语,
    > 你先写个文档;

v1 删除遵守:
- Rule 5(append-only)守 **git history**——v1 从未进 history,删除
  合规
- Rule 0.c(只落真话)要求**文件名反映内容**——v1 名为
  `...emergence-log-pattern-observed.md` 但 v2 内容是 4 层架构提案,
  必须改名,不能"挂羊头卖狗肉"
- 完整决策链系见 `fcop/tasks/TASK-20260513-006-ADMIN-to-ME-...md` §2

### 10.5 后续工作 / Follow-up

- 等 ADMIN review 完本 ADR → 拍板 → 写 `REPORT-20260513-006-ME-to-ADMIN-...md`
- 一并 archive TASK-005 + TASK-006(supersedes 链系)+ REPORT-006
- 显式路径 commit + push(走 SOP `docs/release-process.md` §3.4
  "git add 显式路径,禁用 -A")
- 协议升级动作**单独立项**(下次 fcop 包 release 时),不与本 ADR 同
  commit

**§2.5 反向吸收机制衍生的后续提案候选**(待 ADMIN 单独决策,**不**在
本 ADR 范围):

- **候选 ADR-0035 或更高编号**:把"反向吸收 / Reverse Absorption"作为
  FCoP **第八个核心概念**正式入协议七大概念表(`fcop-rules.mdc`
  "FCoP 的定位与七大核心概念"小节扩为八条)
  - 触发条件:本 ADR Accepted 后 1-2 个 fcop release 周期,观察其它
    项目是否独立用到本机制
  - 实施载体:fcop 包 MINOR release(同时更新 `fcop-rules.mdc` rules
    version 与 `fcop-protocol.mdc` 版本号)
  - 范围:仅协议层概念定义,本 ADR §2.5.1 ADMIN 钦定原文为权威源
- **候选 ADR-0036 或更高编号**:把 §2.5.2 反向吸收六步路径形式化为
  ADR 写作模板,后续所有"留白 → 涌现 → 收编"类 ADR 必须在前言节
  显式标明自己处于六步中的哪一步
  - 触发条件:本 ADR Accepted 后,至少有 1 个新 ADR 也走了同六步
  - 实施载体:`adr/README.md` + `adr/TEMPLATE.md`(若存在)
- **候选 ADR-0037 或更高编号**:把 §2.5.6 **FCoP Semantic Evolution
  Loop**(演化哲学图)正式写入 `fcop-rules.mdc` "FCoP 的定位与七大
  核心概念"小节,与既有"协议三层 stack 图"形成**双图对偶**(执行
  哲学 + 演化哲学)
  - 触发条件:与候选 ADR-0035(反向吸收作为第八核心概念)联动,可
    在同一次 release 内合并落地
  - 实施载体:fcop 包 MINOR release(rules version 2.3.0 + protocol
    commentary version 2.1.0),四件套(ADR-0006)同步部署
  - 范围:**严格原文吸收**本 ADR §2.5.6 ASCII 图与三句"Core Principle",
    不得润色措辞或调整图形结构(Rule 0.c 引用必带出处的最严形式)
  - ADMIN 钦定来源:2026-05-13T09:14+08:00 sess-04 原话——"第一张
    是执行哲学,第二张是演化哲学,两张合在一起,FCoP 才完整"

### 10.6 Status Transition Log / 状态迁移记录

| 时间(本地) | 状态 | 触发事件 | 落盘载体 |
|---|---|---|---|
| 2026-05-13T07:00 | Drafting | TASK-005 派单"emergence-log 单文件 case study" | `fcop/log/tasks/TASK-005-...md` |
| 2026-05-13T08:10 | Drafting v2 | TASK-006 派单"4 层涌现架构级吸收" | `fcop/log/tasks/TASK-006-...md` |
| 2026-05-13T09:14 | Drafting v2.1.1 | ADMIN 三轮补稿落定(§2.5 + §2.5.6) | commit `523d81e` |
| 2026-05-13T13:06 | **Accepted** | ADMIN 决策"我想全部完成,然后升级为 2.0.0" | (本次 commit) |
| → Implemented | (待办) | fcop / fcop-mcp 2.0.0 PyPI release 完成 + ADMIN 在本仓 redeploy_rules | 待 release sprint 收尾 |

ADMIN 13:06 原话被记录在两处:
- `fcop/log/reports/REPORT-20260513-006-ME-to-ADMIN.md` §4(commit `92980c7`)
- 本 §10.6 表(commit 待落)

Accepted 之后本 ADR 进入"实施 sprint"阶段,后续动作由 fcop 包
v2.0.0 release sprint(主任务 `TASK-20260513-008`,sprint 计划文档
`fcop/shared/SPRINT-fcop-2.0.0-release.md`)统一管控。**本 ADR 的
Status 从 Accepted 升至 Implemented 的触发事件**:fcop / fcop-mcp
2.0.0 在 PyPI 上线 + GitHub Release 落定 + ADMIN 在本仓与下游
(Bridgeflow / codeflow)调 `redeploy_rules()`。

---

## 后记 / Postscript

4 层涌现是 FCoP 协议成熟度的**强信号**:协议留白处自发长出健康的内规,
其它项目独立地走到同一套抽象——这正是 ADR-0033 trailing-slug 模式的
重演,也是 ADR-0017 REVIEW envelope 的同源现象。

协议未来"收编"这套自治内规进入正文,是协议生态共建的标准姿势,也是
FCoP "**协议先于运行时存在,运行时只消费协议**"原则在文档体系尺度的
再次落地。
