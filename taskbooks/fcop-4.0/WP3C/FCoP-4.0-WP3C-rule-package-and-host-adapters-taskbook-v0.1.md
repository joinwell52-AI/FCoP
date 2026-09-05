---
title: "FCoP 4.0 WP3C：全新规则包、Host装配与开发Agent宪法接入任务书"
version: "0.1"
date: "2026-09-05"
status: "ADMIN_REVIEW_READY"
document_type: "implementation-taskbook"
authority: "ADMIN"
execution_authorized: false
implementation_authorized: false
activation_authorized: false
authorized_scope: "NONE"
target_repository: "joinwell52-AI/FCoP"
work_package: "WP3C"
parent_gate: "WP3B_LIFECYCLE_ACCEPTED"
base_commit: "511039db227a23ae3e2d79aaae775a92ba392f5c"
wp3c_authorized: false
codeflowmu_role: "downstream-validation-consumer-only"
program_scope: "FCOP_4_0_REQUIRED_WORKSTREAM"
fcop_4_0_release_blocker: true
fcop_4_0_rule_file_strategy: "CLEAN_REBUILD_FROM_FROZEN_V4_CONTRACT"
legacy_v3_rule_files_role: "AUDIT_AND_COMPATIBILITY_REFERENCE_ONLY"
host_projection_strategy: "ON_DEMAND_BY_EXPLICIT_HOST_PROFILE"
supersedes: "CodeFlowMu-AGENTS拆分与Agent宪法强制加载实施任务书-v0.1.md"
---

# FCoP 4.0 WP3C：全新规则包、Host装配与开发Agent宪法接入任务书

## 0. 任务裁决

本任务解决两个相关但不同的问题：

1. FCoP 如何把协议规则提供给已经正式采用的 Codex、Cursor 等 Host；
2. 开发 FCoP 本体的编程 Agent 如何强制读取《Agent原生软件工程宪法》。

本任务是 **FCoP 4.0 升级的强制工作流和发布阻断项**，不是 4.0 发布后的可选优化。FCoP 4.0 只有同时完成协议实现升级和大规则文件拆分，才能进入正式发布验收。

本任务采用 ADMIN 已明确的重建策略：

> **FCoP 4.0 规则文件从冻结的 4.0 合同重新编写，不在 3.x 的大文件上增量修订。**

旧 `AGENTS.md`、`CLAUDE.md` 和 `.mdc` 只用于语义覆盖审计、兼容性判断和历史追溯，不是 4.0 新规则正文的来源。

必须先固定以下边界：

> FCoP 当前仓库中的 `AGENTS.md`、`CLAUDE.md` 和 `.cursor/rules/*.mdc` 是配套 FCoP 的历史协议规则分发产物，不是 CodeFlowMu 产品开发手册；文件存在不等于对应 Host 已被正式采用。

> CodeFlowMu 的产品开发规则已经通过 `codeflowmu.rules.json → CODEFLOWMU-CODING-MANUAL.md → Host薄指针` 独立管理。

> 编程宪法只约束软件开发工作，不能无差别注入所有使用 FCoP 的普通业务 Agent。

本文当前只供 ADMIN 审阅。它确定本工作属于 FCoP 4.0 正式范围，但尚不等于授权某个 Agent 立即修改当前审阅分支、代码、分发包、PyPI 包或下游项目。实施应使用独立工作分支，在 4.0 发布 Gate 前与主升级线汇合。

---

## 1. 当前事实

### 1.1 FCoP 的大文件属于 FCoP

当前 FCoP 仓库包含：

- 根 `AGENTS.md`；
- 根 `CLAUDE.md`；
- `.cursor/rules/fcop-rules.mdc`；
- `.cursor/rules/fcop-protocol.mdc`。

其中根 `AGENTS.md` 与 `CLAUDE.md` 是历史 Host 分发机制生成的 FCoP 协议规则投影。它们不是 CodeFlowMu 产品规则。

当前审计值仅作任务书形成时的参考，执行时必须重新冻结：

```yaml
repository: joinwell52-AI/FCoP
reference_branch: main
AGENTS_md:
  lines: 3703
  characters: 147213
  git_blob: e8b7a3d3d6005d5bc55ea2e55e43a064364588e2
CLAUDE_md:
  lines: 3703
  characters: 147213
  git_blob: e8b7a3d3d6005d5bc55ea2e55e43a064364588e2
```

两份文件字节相同，说明现有机制按“同一规则、多 Host 投影”生成完整副本。代码、测试和发布流程已经把 `CLAUDE.md` 实现为固定分发目标；但这不能证明实际运行过 Claude Code，也不能证明某次 Session 读取了它。当前应区分三个事实：

```yaml
host: claude-code
configured_purpose: "Claude Code CLI project instruction file"
distribution_implementation: ACTIVE_IN_V3
generated_by: "Project.deploy_protocol_rules / redeploy_rules"
fcop_runtime_reads_this_file: false
actual_claude_code_consumption_evidence: NOT_AVAILABLE
admin_host_adoption_status: NEEDS_EXPLICIT_DECISION
fcop_4_0_default_distribution: UNRESOLVED_UNTIL_WP3C_1
```

`CLAUDE.md` 不是模型选择文件。它不会把 Agent 切换成 Claude，也不表示 Cursor/Codex 正在调用 Claude 模型；它只是 Host 约定名称。FCoP 4.0 不再无条件生成所有 Host 文件，而是根据 ADMIN 明确选择的 Host profile 按需生成薄入口。

```yaml
fcop_4_0_host_projection_decision:
  canonical_rule_source: FCOP_V4_RULE_PACKAGE
  AGENTS.md: GENERATE_ONLY_FOR_CODEX_OR_GENERIC_PROFILE
  CLAUDE.md: GENERATE_ONLY_FOR_CLAUDE_CODE_PROFILE
  cursor_rules: GENERATE_ONLY_FOR_CURSOR_PROFILE
  default_profile: NONE
  model_selection_effect: NONE
```

### 1.2 CodeFlowMu 已有独立产品规则链

当前 CodeFlowMu 已存在：

```text
codeflowmu.rules.json
→ docs/engineering/CODEFLOWMU-CODING-MANUAL.md
→ CodeflowmuRuleLoader
→ Runtime编程Session
```

其 `AGENTS.md`、`CLAUDE.md`、`GEMINI.md` 与 Cursor 规则中已经有 CodeFlowMu 手册的薄指针。根文件中的大量 FCoP 正文来自 FCoP 协议分发层，不能归类为 CodeFlowMu 产品开发规则。

### 1.3 本任务必须并入 FCoP 4.0，但不得改写已冻结合同

已知当前 FCoP 4.0 工作基线：

```yaml
frozen_contract_commit: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
wp3b_1_status: COMPLETE
wp3b_1_branch: review/fcop-4.0-wp3b.1-lifecycle-round-correction
```

本任务不得：

- 修改已经冻结的 FCoP 4.0 Core 语义；
- 把 Host 分发问题混入生命周期、round、attempt 或 authority 合同；
- 在当前 WP3B.1 分支夹带实现；
- 把 CodeFlowMu 对 FCoP 3.2.5 的固定关系改为 4.0；
- 因为本文存在就声称 FCoP 4.0 已采用新分发方式。

同时，FCoP 4.0 的完成定义必须增加：

```text
14万字符级AGENTS.md/CLAUDE.md旧规则副本
→ 从冻结4.0合同重新编写Core、分类模块和Manifest
→ 按显式Host profile生成所需薄入口
→ 新旧语义覆盖率与真实Host验证通过
→ 才允许FCoP 4.0发布
```

WP3B.1 已完成不代表本工作完成。它只是 4.0 主升级线中的既有交付；本任务作为独立工作流继续推进，最终共同进入 4.0 release acceptance。

---

## 2. 三类对象必须分开

| 对象 | 面向谁 | 内容 | 是否随FCoP部署到下游 |
|---|---|---|---:|
| FCoP规范与Core | 所有FCoP实现者/使用者 | 协议语义、对象、关系、生命周期、幂等、原子性 | 是，按正式分发合同 |
| FCoP Agent Guidance | 使用FCoP工作的Agent | 如何按协议创建、读取和处理正式对象 | 是，按Role/WorkType最小装配 |
| FCoP开发手册 | 修改FCoP源代码的开发Agent | 仓库架构、测试、发布、兼容性和实现边界 | 否，只属于FCoP源码仓库 |
| Agent原生软件工程宪法 | 承担软件开发工作的Agent | Agent原生软件的上位工程原则 | 仅开发工作必读，不随普通业务工作无差别部署 |
| Host入口投影 | 已由ADMIN采用的Host | 发现、校验和加载上述正确规则的薄适配 | 仅按已采用Host生成 |

这一区分是本任务的核心。FCoP 协议规则与 FCoP 本体开发规则不能继续依赖同一个大文件表达全部语义。

### 2.1 三套规则的独立身份

| 规则体系 | 适用范围 | 独立版本/digest | 是否进入FCoP普通下游 |
|---|---|---:|---:|
| 《Agent原生软件工程宪法》 | 所有Agent原生软件开发 | 是 | 否；只有软件开发工作加载 |
| FCoP 4.0规则包 | 使用、实现或开发FCoP | 是 | 是；按工作类型装配必要模块 |
| 《CodeFlowMu编程与开发准入手册》 | 修改CodeFlowMu产品 | 是 | 否；只属于CodeFlowMu开发 |

三者不得合并、共用版本号或互相复制正文。一次 CodeFlowMu 开发 Session 可以同时装配三者，但 Receipt 必须分别记录其版本和 digest。

### 2.2 不同工作的加载组合

```text
普通FCoP业务工作
= FCoP Core + 必要协议模块 + 当前TASK

开发FCoP本体
= Agent编程宪法 + FCoP开发手册 + FCoP规范/规则 + 当前TASK

开发CodeFlowMu
= Agent编程宪法 + CodeFlowMu编程手册
 + 必要FCoP协议模块 + 当前TASK
```

CodeFlowMu 手册不得进入 FCoP 包；FCoP 开发手册不得进入普通业务工作区；编程宪法不得因为一个项目使用 FCoP 就自动加载。

---

## 3. 目标

1. FCoP 协议规则具有唯一规范源和可验证 Manifest；
2. `AGENTS.md` 和 Cursor 文件只是确定性投影，不是独立权威；`CLAUDE.md` 的 4.0 地位由显式 Host 策略决定；
3. 开发 FCoP 本体的 Agent 强制加载已冻结的 Agent 宪法；
4. 普通 FCoP 业务 Agent 不因使用 FCoP 而自动加载编程宪法；
5. FCoP 开发规则不随 `redeploy_rules()` 复制到下游项目；
6. 下游仍保持“MCP 接入即可使用”的最小体验；
7. 3.x 兼容分发与 4.0 新分发明确隔离；
8. 更新只能被发现和审计，不能自动成为 active；
9. CodeFlowMu 作为重要下游消费者进行 shadow，但不在本任务中改造；
10. 所有变更经过 ADMIN 明确冻结、实施授权和激活。

### 3.1 “完成大文件拆分”的明确含义

拆分完成不是把 3,700 行正文移动到另一个同样大的文件，也不是把一个大文件机械切成若干等长片段，更不是在旧文件上继续增删。必须同时满足：

1. 从冻结的 FCoP 4.0 合同建立全新的规则文件集合；
2. 根 `AGENTS.md`、`CLAUDE.md` 不再携带完整 FCoP 规则正文，只作为 4.0 Host 投影；
3. FCoP 4.0 Core 作为所有 FCoP 工作的最小必读合同；
4. 其余 4.0 内容按稳定语义重新编写为专题模块；
5. Manifest 明确每个模块的 ID、版本、digest、适用条件、依赖和顺序；
6. Host 根据任务加载 Core 与必要模块，不默认加载全部历史、解释和示例；
7. 不支持原生 Manifest 的 Host 通过受控 bootstrap/生成器获得等价的有界投影；
8. 每一条冻结的 4.0 normative clause 都能追溯到唯一规则模块；
9. 每一条旧 3.x active rule 都有 `retained / superseded / obsolete / commentary / conflict` 处置记录；
10. history、commentary、示例和 release 说明退出默认强制上下文，但保留可发现性；
11. CodeFlowMu 等下游产品自有指针不会被 FCoP 更新覆盖；
12. 3.x 旧分发继续兼容，4.0 新分发不靠静默迁移生效。

### 3.1.1 两套覆盖证明

4.0 新规则必须同时通过两套不同的覆盖检查：

```text
正向覆盖：冻结4.0合同条款 → 4.0规则模块 = 100%
反向审计：旧3.x active规则 → 明确处置结果 = 100%
```

正向覆盖决定 4.0 是否完整；反向审计用于防止遗漏仍然有效的安全经验。不得因为旧文件存在某条规则就直接复制进 4.0，也不得因为 4.0 文本更短就默认旧规则全部过时。

### 3.2 候选模块边界

模块名由 WP3C.1 最终冻结，但至少应按语义而不是按页数考虑：

```text
fcop.core                 所有工作必读的最小协议合同
fcop.workspace            Workspace身份、版本和初始化
fcop.objects              TASK/REPORT/ISSUE/REVIEW
fcop.lifecycle            五桶、迁移与终端条件
fcop.relationships        parent/references/source/supersession
fcop.authorization        授权引用、责任和生效
fcop.idempotency          operation identity、结果复用与重试
fcop.atomicity            线性化、并发、崩溃窗口与恢复
fcop.host-tools           MCP资源、工具调用和Host适配
fcop.development          只供FCoP本体开发，不进入普通下游
```

Core 必须足以让普通使用者理解 FCoP 的最低不可违反边界；专题模块不得重新定义 Core。

### 3.3 上下文预算候选

WP3C.0 必须测量当前真实内容后由 WP3C.1 冻结预算，不能为追求数字而删减语义。初始目标：

- 根 Host bootstrap：2–4 KiB；
- `fcop.core`：目标不超过 12 KiB；
- 单个专题模块：目标不超过 16 KiB；
- 普通单一工作类型的默认装配：显著低于当前约 147 KiB；
- required 内容超限时 fail closed，不允许静默截断。

最终 Gate 以语义覆盖、安全和真实 Host 可用性为先，具体硬上限由 WP3C.1 基于实测冻结。

---

## 4. 非目标

本任务不：

- 重写 FCoP 4.0 Core；
- 修改 TASK、REPORT、ISSUE、REVIEW 的正式语义；
- 修改五桶、关系字段、Branch REPORT、Authorization 或幂等合同；
- 设计 CodeFlowMu 产品开发规则；
- 拆分 `CODEFLOWMU-CODING-MANUAL.md`；
- 让 FCoP 成为工作流引擎或业务裁决器；
- 让 FCoP Runtime 判断工作是否完成；
- 让 EVAL 直接驱动生命周期；
- 自动升级下游项目；
- 修改已经启动的 Run 所绑定的规则或合同；
- 在没有许可审计的情况下复制外部实现代码。

---

## 5. 目标架构

### 5.1 权威源与投影

```text
FCoP 4.0规范/Core
        │
        ├── 协议Guidance模块
        │        │
        │        └── FCoP Distribution Manifest
        │                  │
        │                  ├── AGENTS.md（Codex薄入口）
        │                  └── Cursor已采用入口
        │
        └── FCoP源码仓库开发规则
                 │
                 ├── Agent原生软件工程宪法
                 ├── FCoP开发手册
                 └── 当前开发TASK/Acceptance
```

### 5.2 两个不得混淆的装配结果

普通 FCoP 工作 Session：

```text
FCoP Core
+ 当前Role/WorkType所需协议Guidance
+ 当前TASK/authority
= FCoP工作上下文
```

开发 FCoP 本体的 Session：

```text
Agent原生软件工程宪法
+ FCoP开发手册
+ 与修改范围有关的FCoP规范/Core
+ 当前开发TASK/Acceptance/authority
= FCoP开发上下文
```

只有第二种必须加载编程宪法。

---

## 6. 文件职责候选

最终路径由合同冻结阶段确定。候选职责如下：

| 文件/目录 | 候选职责 |
|---|---|
| `spec/fcop-4.0-spec.md` / `.zh.md` | FCoP 4.0 规范权威文本 |
| `spec/fcop-4.0-core.*` | 最小 Core；若已有冻结路径则沿用，不重新命名 |
| `src/fcop/rules/_data/` | package-owned 协议 Guidance 源或生成输入 |
| `.fcop/rules/MANIFEST.json` | 下游已部署协议模块及 digest 的 Manifest |
| `docs/engineering/FCOP-DEVELOPMENT-MANUAL.md` | 只供 FCoP 本体开发的产品手册 |
| `docs/governance/AGENT-NATIVE-ENGINEERING-CONSTITUTION.md` | 已冻结宪法的固定引用或快照 |
| 根 `AGENTS.md` | FCoP 源码仓库 Codex 开发入口；不得再兼任完整下游模板源 |
| 根 `CLAUDE.md` | 从 4.0 Manifest 重新生成的 Host 兼容薄投影；不产生模型选择或采用事实 |
| `agents/codex.md` | 仅在确认消费者后生成的 Codex 投影 |
| `.cursor/rules/*.mdc` | Cursor 协议/开发适配，职责必须显式分开 |

不得为了符合候选结构而改动已经冻结的 FCoP 4.0 路径。执行者必须先读取真实仓库，再提出最小迁移方案。

### 6.1 建议的物理结构

```text
src/fcop/rules/_data/v4/
├── MANIFEST.json
├── core/
│   └── FCOP-CORE.md
├── modules/
│   ├── WORKSPACE.md
│   ├── OBJECTS.md
│   ├── LIFECYCLE.md
│   ├── RELATIONSHIPS.md
│   ├── AUTHORIZATION.md
│   ├── IDEMPOTENCY.md
│   ├── ATOMICITY-RECOVERY.md
│   └── TOOLS.md
└── adapters/
    ├── codex.template.md
    ├── claude-code.template.md
    └── cursor.template.mdc

下游项目/.fcop/rules/
├── MANIFEST.json
├── core/FCOP-CORE.md
└── modules/*.md
```

目录名是候选，WP3C.1 可按当前包结构调整；职责不可重新混合。

### 6.2 建议的部署接口

替换当前无条件写四件套的行为：

```python
deploy_protocol_rules(
    profile="fcop-4.0-modular",
    hosts=["codex", "cursor"],
    dry_run=True,
    preserve_project_owned=True,
)
```

MCP 对应接口应要求显式 Host：

```text
redeploy_rules(
  profile="fcop-4.0-modular",
  hosts=["codex", "cursor"],
  dry_run=true
)
```

关键语义：

- `hosts` 不得默认为“全部平台”；
- 未声明 `claude-code` 时不得生成 `CLAUDE.md`；
- Host 参数只决定入口格式，不决定模型；
- 先把统一规则包部署到 `.fcop/rules/`；
- 再为选定 Host 生成短入口；
- 短入口只引用 Manifest、Core 和模块解析规则；
- 已存在的项目自有内容必须保留，冲突时停止；
- `dry_run` 必须输出计划、diff、摘要和冲突，保持零写入；
- 3.x legacy profile 保持兼容，不静默改成 4.0。

### 6.3 FCoP源码仓库与下游项目分开

FCoP 源码仓库自身的根 `AGENTS.md` 是“开发 FCoP”的入口，应加载：

```text
Agent编程宪法
+ FCoP开发手册
+ 当前FCoP 4.0规则包
+ 当前开发TASK
```

部署到普通下游项目的 Codex `AGENTS.md` 只加载：

```text
FCoP Core
+ 当前工作命中的协议模块
+ 当前TASK
```

两者可以使用同一 Codex adapter 模板，但选择的 bundle 不同。FCoP 源码仓库的开发入口不得被 `redeploy_rules()` 当作普通下游文件整份覆盖。

### 6.4 现有四件套的分类处置

现有四件套：

```text
.cursor/rules/fcop-rules.mdc
.cursor/rules/fcop-protocol.mdc
AGENTS.md
CLAUDE.md
```

“四件套”是当前遗留文件清单，不是 FCoP 4.0 必须继续支持四个目标的决定。FCoP 4.0 按实际 Host 采用状态分别处置：

| 文件 | FCoP 4.0职责 | 是否允许直接增加规则正文 |
|---|---|---:|
| `AGENTS.md` | Codex/通用Host薄入口，读取Manifest、Core和命中模块 | 否 |
| `CLAUDE.md` | 从全新4.0规则源生成的薄投影；不是旧3.x正文的修订版 | 否 |
| `fcop-rules.mdc` | Cursor的规则路由/模块引用投影 | 否 |
| `fcop-protocol.mdc` | Cursor的协议Core/规范引用投影 | 否 |

若 Cursor 的真实能力要求 `.mdc` 内嵌少量 required 内容，只允许由生成器从 canonical module 编译，不允许人工维护另一份正文。

### 6.5 新规则分类准入流程

FCoP 4.0 生效后，任何新增或修改规则必须走以下流程：

```text
提出规则变化
→ 判定是否改变FCoP Core/正式规范
→ 判定所属分类模块
→ 修改唯一canonical source
→ 更新模块version/digest/source anchor
→ 更新Distribution Manifest
→ 只生成已采用Host的投影
→ 执行覆盖、一致性与真实Host测试
→ 审阅与ADMIN激活
```

不得直接编辑现有四件套来增加或改变规则。新增 Host 也不能因为生成器“能够生成”就自动视为已经采用。

### 6.6 分类决策

每条新规则必须登记：

```yaml
rule_change:
  rule_id: ""
  normative: true | false
  source_authority: ""
  source_anchor: ""
  target_module: ""
  affects_core: true | false
  affected_roles: []
  affected_work_types: []
  affected_hosts: []
  compatibility_effect: none | additive | breaking
  module_version_before: ""
  module_version_after: ""
  module_digest_after: ""
  manifest_digest_after: ""
  activation_receipt: ""
```

分类规则：

- 能归入已有稳定语义域的，写入该模块；
- 同时影响多个模块的，正文仍只有一个权威位置，其他模块只做引用；
- 改变 Core 的，必须走 FCoP 规范变更程序，不得以普通 Guidance 更新绕过；
- 只属于 Host 语法的，进入 Host adapter，不得改变协议语义；
- 只属于 FCoP 源码开发的，进入 `fcop.development`，不得分发给普通下游；
- 找不到明确分类的，结果为 `RULE_CLASSIFICATION_UNRESOLVED`，停止并提交架构审查；
- 禁止以“暂时方便”为由追加到 `AGENTS.md`、`CLAUDE.md` 或任一 `.mdc` 末尾。

### 6.7 生成文件保护

所有 active Host 投影应具备机器可验证的生成标识，至少包含：

- generated / do-not-edit 声明；
- generator version；
- source manifest version/digest；
- selected module IDs/digests；
- 生成时间是否进入 digest 的明确规则；
- 当前 distribution profile。

CI 必须拒绝：

- active Host 投影发生变化但 canonical module/Manifest 未变化；
- 人工内容无法追溯到 source anchor；
- 未经 Host 策略冻结的文件被加入 4.0 默认分发；
- 若兼容测试临时生成 `CLAUDE.md`，其共同协议语义与 canonical module 不一致；
- Cursor 投影与其他 Host 选择不同的 required Core；
- generator 重跑不能复现已提交文件；
- 新规则被直接追加进生成文件；
- 同一规则在多个模块出现两份可独立修改的正文。

---

## 7. Host统一接口参考

赵越的 `yzhao062/anywhere-agents` 可作为 Host 配置工程参考：

- 一份共享源生成 `CLAUDE.md` 与 `agents/codex.md`；
- rule/skill/permission pack；
- pinned ref、lock 与 drift 检查；
- generated file 一致性测试；
- 真实 Claude/Codex CLI smoke test；
- local override 与生成内容分层。

本任务只吸收适合 FCoP 的机制：

1. 单源多投影；
2. Host 能力矩阵；
3. 生成器与确定性测试；
4. 版本锁和漂移审计；
5. 真实 Host 读取验证。

不得照搬：

- mutable ref 自动更新并生效；
- 默认写用户主目录或全局 Host 设置；
- 未经 allowlist/digest/许可审计的远程 pack；
- 用 local override 改写协议 Core、authority 或 Capability；
- 把配置同步工具当成 FCoP 协议实现。

若复用代码而不是借鉴思想，必须固定 commit、核验 Apache-2.0 许可和 attribution 要求。

---

## 8. 分阶段任务

### WP3C.0：只读基线与消费者审计

在独立审计上下文中读取：

1. FCoP 当前 `main` 与当前 4.0 审阅分支；
2. `AGENTS.md`、`CLAUDE.md`、`.cursor/rules/*.mdc`；
3. bundled rule 源、生成器、版本 patch 脚本；
4. `Project.deploy_protocol_rules` 与 `redeploy_rules()`；
5. `fcop://rules`、`fcop://spec` 等 MCP resource；
6. wheel/package 中实际捆绑的文件；
7. CodeFlowMu 中由 FCoP 写入的区域与产品自有薄指针；
8. 其他测试下游项目的规则部署结果；
9. `anywhere-agents` 固定参考 commit。

必须回答：

- 哪一份文件是 canonical source；
- 哪些是生成投影；
- 根 `AGENTS.md` 是否同时承担源码开发入口和下游模板源；
- `redeploy_rules()` 是否会覆盖下游产品自有内容；
- 普通业务 Agent 实际需要加载多少 FCoP 内容；
- FCoP 本体开发 Agent 当前缺少哪些开发专用规则；
- 3.x 与 4.0 的分发兼容边界是什么。

WP3C.0 只读，不允许修改、生成、提交、发布或部署。

### WP3C.1：冻结分发与开发上下文合同

冻结：

- 协议规范、协议 Guidance、开发手册、宪法和 Host 投影的身份；
- Host Adoption Registry：只有 ADMIN 明确采用且通过能力验证的 Host 才能进入 active distribution；
- 唯一 Source of Truth 与引用方向；
- Manifest Schema、canonicalization 和 digest；
- required/optional 模块；
- Role/WorkType/Host 的选择规则；
- 3.x combined profile 与 4.0 modular profile；
- `redeploy_rules()` 允许写入范围；
- managed block 或完全独立文件策略；
- fail-closed 错误码；
- 下游采用与回滚 Receipt；
- 宪法升级与 FCoP 协议升级的独立版本关系。
- `CLEAN_REBUILD_FROM_FROZEN_V4_CONTRACT`：禁止以旧3.x大文件作为新正文基底；
- 4.0 clause-to-module 正向覆盖矩阵；
- 3.x rule disposition 反向审计矩阵；
- Codex、Claude Code、Cursor 等 adapter 模板合同，以及按显式 Host profile 生成的规则。

退出 Gate：`FCOP_RULE_DISTRIBUTION_CONTRACT_FROZEN`。

### WP3C.2：先建立失败测试

测试至少覆盖：

- FCoP 本体开发缺宪法时拒绝正式开发；
- 普通 FCoP 业务 Session 不加载编程宪法；
- 协议 Guidance 不包含 FCoP 仓库开发命令；
- FCoP 开发手册不被打包到普通下游；
- 已采用 Host 投影选择相同协议模块和 digest；
- `CLAUDE.md` 只在显式选择 `claude-code` Host profile 时生成；未选择时不得出现；
- required 模块缺失、digest mismatch 和冲突 fail closed；
- dry-run 零写入；
- 下游产品自有薄指针不被覆盖；
- 3.x 兼容分发保持原有行为；
- 4.0 modular 分发可回滚；
- MCP 接入的最小用户无需 CodeFlowMu。

### WP3C.3：实现模块、Manifest与生成器

实施内容：

- 以冻结的 FCoP 4.0 spec/Core/决策合同为唯一规范输入，重新编写 Core 与按需 Guidance；
- 禁止复制旧 `AGENTS.md`/`CLAUDE.md` 后在其上删改形成 4.0 规则；
- 对旧 3.x 规则只做逐条 disposition 和必要经验核验；
- 建立 Distribution Manifest；
- 从 4.0 Manifest 只为本次显式选择的 Host 生成全新薄投影；
- 将 FCoP 源码仓库开发入口与下游协议模板分开；
- 为 FCoP 本体开发入口加入宪法和开发手册校验；
- 让 `redeploy_rules()` 支持显式 profile、dry-run、staging、原子替换和 Receipt；
- 禁止整文件覆盖未知的产品自有内容；
- 保留 3.x legacy/combined 兼容路径，不静默切换现有项目。

### WP3C.4：FCoP自身Host shadow

对 Codex、Cursor 及正式采用的其他 Host 执行：

- 协议使用任务；
- FCoP 本体编码任务；
- Core 与专题模块路由；
- 缺失、冲突和超限；
- 开发宪法 required/not-required 判定；
- 真实 CLI 读取 smoke test；
- 旧大文件与新装配的 active normative coverage 对比。

`CLAUDE.md` 必须验证为与 4.0 Manifest 一致的生成投影；若当前环境没有 Claude Code CLI，结果只能是 `HOST_RUNTIME_UNVERIFIED`，不得虚报真实 Host 消费已通过。这不阻止验证文件生成与语义一致性，但正式 Host 支持声明必须另有真实运行证据。

shadow 不修改 lifecycle，不发布包，不改变业务决定。

### WP3C.5：下游兼容 shadow

至少验证：

- 纯 FCoP 最小示例项目；
- CodeFlowMu 当前固定 FCoP 3.2.5 的项目；
- 新建 FCoP 4.0 候选项目；
- Windows、Linux 与 macOS 支持矩阵；
- Codex、Cursor 等已采用 Host 的规则发现；
- 下游自有 `AGENTS.md`/`CLAUDE.md` 内容保护；
- 回滚到旧分发 revision。

CodeFlowMu 在本阶段仅作为只读/隔离 shadow 消费者，不采用 4.0、不改生产入口。

### WP3C.6：ADMIN发布与采用

只有 WP3C.0–WP3C.5 通过后才能：

1. ADMIN 签发分发 ActivationReceipt；
2. 合并独立审阅分支；
3. 构建并验证包；
4. 发布明确版本；
5. 新项目显式选择 4.0 modular profile；
6. 现有 3.x 项目保持原 profile，除非另行迁移；
7. CodeFlowMu 通过独立 Adoption TASK 决定是否采用；
8. 保留旧模板、Manifest、生成器和 rollback receipt。

---

## 9. 失败语义

| 情况 | 结果 | 处理 |
|---|---|---|
| FCoP开发缺宪法 | `ENGINEERING_CONSTITUTION_UNAVAILABLE` | 停止开发 |
| 普通业务Session未加载宪法 | 正常 | 不构成缺失 |
| 协议模块缺失 | `FCOP_GUIDANCE_REQUIRED_MODULE_MISSING` | 停止受影响动作 |
| digest不一致 | `FCOP_GUIDANCE_DIGEST_MISMATCH` | 停止，不使用近似副本 |
| 开发规则进入下游包 | `DEVELOPMENT_GUIDANCE_SCOPE_LEAK` | 构建失败 |
| 下游产品内容将被覆盖 | `DOWNSTREAM_OWNED_CONTENT_COLLISION` | 停止并报告冲突 |
| Host读取能力未验证 | `HOST_GUIDANCE_CAPABILITY_UNVERIFIED` | 不列为正式支持，不生成active入口 |
| 未采用Host进入默认分发 | `UNADOPTED_HOST_DISTRIBUTION_ATTEMPT` | 构建失败 |
| 3.x/4.0 profile不明 | `DISTRIBUTION_PROFILE_UNRESOLVED` | 不部署 |
| 更新可用但未激活 | `UPDATE_AVAILABLE` | 只报告，不应用 |

不确定不得被默认值改写为成功。

---

## 10. 验收合同

- [ ] `ACC-001` FCoP 大文件被正确认定为 FCoP 协议分发产物；
- [ ] `ACC-002` CodeFlowMu 产品开发规则未被错误归入 FCoP；
- [ ] `ACC-003` 协议规则、开发手册和编程宪法三者身份独立；
- [ ] `ACC-004` 普通业务 Agent 不无差别加载编程宪法；
- [ ] `ACC-005` FCoP 本体开发 Agent 必须加载并验证宪法；
- [ ] `ACC-006` canonical source、Manifest 与 Host 投影关系唯一；
- [ ] `ACC-007` `AGENTS.md`、遗留 `CLAUDE.md`、`.mdc` 不各自维护规则；
- [ ] `ACC-008` active normative coverage 为 100%；
- [ ] `ACC-009` 真实 Codex/Cursor 及其他已采用 Host 的 shadow 通过；
- [ ] `ACC-010` MCP 最小接入不依赖 CodeFlowMu；
- [ ] `ACC-011` 开发手册不会泄漏进普通下游工作区；
- [ ] `ACC-012` `redeploy_rules()` 不覆盖下游产品自有内容；
- [ ] `ACC-013` 3.x 兼容路径不被静默改变；
- [ ] `ACC-014` 4.0 modular profile 只有显式选择后生效；
- [ ] `ACC-015` CodeFlowMu 继续固定 3.2.5，直到独立 Adoption；
- [ ] `ACC-016` FCoP 4.0 冻结 Core 与当前 WP3B.1 证据未被改写；
- [ ] `ACC-017` shadow 不驱动生命周期或业务决定；
- [ ] `ACC-018` rollback 演练通过并产生 Receipt；
- [ ] `ACC-019` 任何代码复用已完成许可与 attribution 审计；
- [ ] `ACC-020` ADMIN 已明确签发 ActivationReceipt。
- [ ] `ACC-021` 两个大文件已拆为 Core、分类模块、Manifest 和薄入口；
- [ ] `ACC-022` 所有 active Host 投影均可由固定输入确定性重生成；
- [ ] `ACC-023` CI 能阻止直接向 `AGENTS.md`、`CLAUDE.md` 和 `.mdc` 增加规则正文；
- [ ] `ACC-024` 每条新增规则必须有唯一分类、source anchor、模块版本和 digest；
- [ ] `ACC-025` 无法分类的新规则会触发架构审查，而不是进入兜底大文件；
- [ ] `ACC-026` FCoP 4.0 release Gate 明确依赖本任务完成。
- [ ] `ACC-027` 本次选定 Host 的入口均从全新 4.0 Manifest 按需生成，不是旧3.x正文的增量修订；
- [ ] `ACC-028` 文件存在、生成器支持、模型选择和实际 Host 消费四种事实不会互相替代；
- [ ] `ACC-029` 冻结4.0合同条款到4.0规则模块的正向覆盖率为100%；
- [ ] `ACC-030` 旧3.x active规则的处置记录覆盖率为100%。

任一必选项不通过，不得发布或激活。

---

## 11. 禁止项

1. 禁止再把 FCoP 的大文件称为 CodeFlowMu 产品开发规则；
2. 禁止在 CodeFlowMu 仓库内部重新维护一份 FCoP 规范；
3. 禁止把编程宪法加入所有普通 FCoP 业务 Agent；
4. 禁止让根 `AGENTS.md` 同时成为开发手册、协议规范和下游模板的唯一正文；
5. 禁止直接删除当前大文件以达到瘦身目标；
6. 禁止在 current WP3B.1 分支夹带本任务；
7. 禁止修改冻结的 FCoP 4.0 Core；
8. 禁止自动采用 mutable upstream 或远程 pack；
9. 禁止让 generator、MCP、Host 或 Runtime自行决定规则生效；
10. 禁止用文件生成成功代替语义验收；
11. 禁止让已启动的 Session/Run 中途换规则 digest；
12. 禁止未经 ADMIN Adoption 改变 CodeFlowMu 的 FCoP 版本。
13. 禁止把 `AGENTS.md` 或 `CLAUDE.md` 设为新增规则的编辑入口；
14. 禁止建立 `misc`、`other`、`temporary` 等永久兜底规则模块；
15. 禁止通过复制正文实现跨分类引用。

---

## 12. 第一项允许建立的任务

在 ADMIN 冻结本任务书后，第一项只能是：

```text
FCoP 4.0 WP3C.0：规则分发与开发上下文只读基线审计
```

WP3C.0 应在固定的 WP3B accepted head 之上执行，不修改已验收的 WP3B 分支。最终只输出：

```yaml
WP3C_0_RESULT: pass | gap | conflict | needs_pm
CURRENT_DISTRIBUTION_SOURCE: ""
CURRENT_GENERATED_TARGETS: []
FCOP_DEVELOPMENT_CONTEXT: ""
DOWNSTREAM_PROTOCOL_CONTEXT: ""
CODEFLOWMU_COLLISION_SCOPE: []
V3_COMPATIBILITY_RISK: []
V4_MODULAR_READINESS: ""
WP3C_1_ADMISSION: allowed | blocked
```

执行者不得自行启动 WP3C.1–WP3C.6。

---

## 13. 完成定义

```text
FCoP协议规则有唯一源和Manifest
+ 开发FCoP的Agent强制加载宪法
+ 普通FCoP业务Agent不加载开发规则
+ 多Host入口只是可验证投影
+ 3.x兼容与4.0新分发隔离
+ CodeFlowMu只通过独立Adoption采用
+ shadow、回滚、ADMIN Activation全部通过
= 本任务完成
```

在此之前，只能报告某个 WP3C 子阶段已交付，不能声称 FCoP 的大规则文件已经被替换或新分发已经生效。
