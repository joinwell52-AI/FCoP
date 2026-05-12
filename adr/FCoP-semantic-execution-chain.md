# FCoP 三层语义执行链模型图（v1.0）
# FCoP Three-Layer Semantic Execution Chain Model

**文档类型**：核心规范参考（Canonical Reference）  
**版本**：1.0  
**日期**：2026-05-12  
**依赖**：ADR-0030 · ADR-0031 · ADR-0032  
**模型图**：[FCoP-semantic-execution-chain-v1.0.png](./FCoP-semantic-execution-chain-v1.0.png)

![FCoP 三层语义执行链模型图 v1.0](./FCoP-semantic-execution-chain-v1.0.png)

---

> **FCoP 使命**：将协议状态（Protocol State）转化为可执行认知（Actionable Cognition），而非直接执行（Not Execution）

---

## 一、三层执行链总览

```
项目工作树（Project Working Tree）
         │
         ▼  scan（纯读）
┌─────────────────────────────────────────────────────┐
│  L1 检测层 · Detection Layer                         │
│  发现事实（What is）                                  │
│  纯扫描，不解释                                       │
│  输出：Facts（事实 / 元数据 / 证据）                   │
└────────────────────┬────────────────────────────────┘
                     │  interpret（语义解释）
                     ▼
┌─────────────────────────────────────────────────────┐
│  L2 解释层 · Interpretation Layer                    │
│  解释事实（What it means）                            │
│  结构化，赋予语义                                     │
│  输出：Violations（结构化违规清单）                    │
└────────────────────┬────────────────────────────────┘
                     │  generate（文档生成）
                     ▼
┌─────────────────────────────────────────────────────┐
│  L3 文档生成层 · Documentation Layer                  │
│  生成说明书（What to do）                             │
│  可读，可复制，不执行                                  │
│  输出：INSPECTION.md（结构化报告 + 建议整改方案）       │
└────────────────────┬────────────────────────────────┘
                     │  use（使用）
                     ▼
          人类 / Agent 决策并执行方案
          （执行在 FCoP 之外）
```

---

## 二、元数据级 ADR 分工

三个 ADR 各自负责三层中的一个维度，职责严格不重叠：

| ADR | 负责维度 | 核心定义 | 产出 | 直接产出物 |
|---|---|---|---|---|
| **ADR-0030** | 能力约束（Capability Boundary / Schema / Type System） | `risk_level` schema（irreversible / reversible / sensitive）；声明系统边界，不执行 | Capability Boundary | 无直接产出（定义约束，不产生日志） |
| **ADR-0031** | 防漂移规则（Governance Rules） | 定义何为漂移（Drift）；定义违规为何（Violation） | Alert / Drift Signal | 无直接产出（只产生信号，不生成文档） |
| **ADR-0032** | 工具能力定义（Tool Capability） | `fcop_audit()` 只读；不写盘（除报告本身）；不执行任何整改命令 | INSPECTION.md | 检查报告 + 建议整改方案 |

---

## 三、L1 检测层内部架构（六类扫描）

L1 的核心是**六类 `scan_*()` 方法**，每个方法回答"项目里发生了什么事实"。

```
L1 检测层 · Detection Layer Architecture

输入：项目工作树（Project Working Tree）
         │
         ├──► scan_misplaced_envelopes()   →  桶错位扫描（Rule 2）
         │      envelope 路径 ≠ kind: 声明
         │
         ├──► scan_legacy_role_docs()      →  草根角色书扫描（Rule 1 冲突风险）
         │      fcop/ 根目录无 kind: 字段的 .md
         │
         ├──► scan_legacy_manifests()      →  双 manifest 扫描（Rule 0 冲突）
         │      fcop/*.json ≠ fcop.json
         │
         ├──► scan_cursor_rules()          →  .cursor/rules/ 协议规则审计（P0）
         │      缺失协议 mdc + 草根 mdc 混入
         │
         ├──► scan_shared_deployment()     →  三层文档部署度（Rule 4.5）
         │      fcop/shared/ 完整度（P0 ≥ 50% 缺失 / P1 < 50%）
         │
         └──► scan_ghost_prefixes()        →  幽灵前缀扫描（Rule 5）
                DRAFT- / HANDOFF- / AMEND- / *-v2.md

输出：
  Facts（原始事实列表）
    ├─ 文件路径 / 计数 / 违规证据
    ├─ severity 初判（P0 / P1 / P2）
    └─ 关联规则（Rule 0 / 1 / 2 / 4.5 / 5）
```

**L1 设计原则**：纯读操作，不修改任何文件，不做语义判断——只回答"目前项目里有什么"。

---

## 四、L2 解释层内部架构（语义解释）

L2 将 L1 的原始事实解释为**结构化协议违规**，是"发现"到"理解"的桥梁。

```
L2 解释层 · Interpretation Layer Architecture

输入：L1 Facts（原始事实）
         │
         ▼
┌─────────────────────────────────────────────────────┐
│  解释引擎 · Interpretation Engine                    │
│  事实 → 协议规则（ADR-0030）                          │
└──────────────┬──────────────────────────────────────┘
               │
     ┌─────────┼─────────┐
     ▼         ▼         ▼
  规则匹配   违规判定   影响评估
  Rule       Violation  Impact
  Matching   Judgment   Assessment
  是/否     P0/P1/P2   对项目的实际影响
                       风险级别
               │
               ▼
          整改映射 · Remediation Mapping
          映射到可执行建议（不执行！）
               │
               ▼
输出：Violation List（结构化违规清单）
  Violation {
    violation_id:  P0-001 / P1-003 ...
    severity:      P0 / P1 / P2
    rule_violated: "Rule 2 (桶错位)"
    summary:       一句话描述
    evidence:      [文件路径 / 计数]
    impact:        业务影响
    remediation:   [RemediationStep 列表]（机读）
  }
```

---

## 五、L3 文档生成层内部架构（说明书生成）

L3 将结构化违规转化为**人可读 + 可操作的整改说明书**。

```
L3 文档生成层 · Documentation Layer Architecture

输入：L2 Violations（结构化违规清单）
         │
         ▼
┌─────────────────────────────────────────────────────┐
│  文档生成器 · Documentation Generator                │
└──────────────────────────┬──────────────────────────┘
               ┌───────────┼───────────┐
               ▼           ▼           ▼
           分组排序      建议生成      渲染文档
           Grouping &   Suggestion   Markdown
           Sorting      Generation   Rendering
           severity/    为每条违规   INSPECTION.md
           tier 分组    生成           (L3 格式)
                        RemediationStep
                        列表
                             │
                             ▼
                        执行块生成
                        Execution Block
                        Tier 1/2/3 分组
                        可复制命令

最终产出：INSPECTION.md
  ├─ YAML frontmatter（机读：inspection_id / overall_status / p0-p2 计数）
  ├─ 摘要（状态图标 + 分档计数 + 预估时长）
  ├─ P0 阻塞性违规（每条含：实证 / 影响 / 建议命令 / 执行人 / 回滚）
  ├─ P1 规范性违规（同上）
  ├─ P2 整洁性违规（同上）
  └─ ▶ Execution Block（核心创新）
       ├─ Tier 1 · 立即（今日内，低风险，无依赖）→ 可复制命令
       ├─ Tier 2 · 本 sprint（1-2 天，有依赖）
       └─ Tier 3 · 后续清理（低优先）
```

---

## 六、端到端数据流（End-to-End Data Flow）

```
项目工作树
Project Working Tree
    │
    │  scan（6 个 scan_* 方法，纯读）
    ▼
L1 Facts
（事实 / 元数据 / 证据）
    │
    │  interpret（L2 解释引擎）
    ▼
L2 Violations
（结构化违规清单，机读）
    │
    │  generate（L3 文档生成器）
    ▼
L3 INSPECTION.md
（建议整改方案，人读）
    │
    │  use（由人 / Agent 决策）
    ▼
人类 / Agent 执行方案
（执行在 FCoP 之外）
```

---

## 七、最终产出物 INSPECTION.md

`INSPECTION.md` 是**结构化发现 + 整改建议**的复合体：

> **INSPECTION ≠ Remediation Plan**  
> **INSPECTION = Structured Findings + Suggested Remediation Plan**

| 组成部分 | 内容 | 性质 |
|---|---|---|
| **Structured Findings** | L1/L2 产出的客观事实（违规 ID / 规则 / 证据 / 影响） | 客观描述 |
| **Suggested Remediation Plan** | L3 基于发现生成的建议行动（Execution Block） | 建议，不是指令 |

**文件命名**：`fcop/shared/INSPECTION-{YYYYMMDD}-{NNN}-{scope}.md`  
**append-only**：同日同 scope 第二次跑产出 NNN+1，不覆盖原报告  
**human-readable**：Tier 1/2/3 分组，每步含可复制命令 + 回滚方式

---

## 八、核心原则（Core Principles）

### 不越界 · No Boundary Violation
> 在 ADR-0030 定义边界内工作

`fcop_audit()` 只扫描，不干预；只读操作，写副作用仅限 INSPECTION.md 本身。

### 只观察 · Observe Only
> 不修改项目状态，不写业务文件

`fcop_audit()` 是纯观察工具，不改变项目的任何业务文件，仅产出 INSPECTION 报告。

### 不执行 · No Execution
> 只生成说明书，执行决策由人做出

Execution Block 里的命令是**建议（suggestion）**，不是**指令（command to system）**。每次运行结束后所有操作等待人类确认。

### 可追溯 · Traceable
> 每个违规可回溯，每个步骤可审计

每条 Violation 含 `violation_id`、`scan_source`、`evidence` 列表，所有结论有据可查。

### 防漂移 · Anti-Creep
> 未来自动执行需求，必须单独 ADR

❗ 若未来出现"让 `fcop_audit` 自动执行整改"或"让 FCoP 调度 agent"的需求，**必须单独立 ADR**（如 `fcop_remediate()`），经 ADMIN 明确审批后才能实施。不得悄然扩展本工具职责边界。

---

## 九、三层职责总对照表

| 维度 | L1 检测层 | L2 解释层 | L3 文档生成层 |
|---|---|---|---|
| **核心问题** | 发生了什么事实？ | 这意味着什么？ | 该怎么修（建议）？ |
| **输入** | 项目文件系统 | L1 Facts | L2 Violations |
| **输出** | 原始事实 / 证据 | 结构化违规 | INSPECTION.md |
| **是否判断** | ❌ 不判断 | ✅ 规则匹配 | ✅ 建议生成 |
| **是否执行** | ❌ | ❌ | ❌ |
| **是否写盘** | ❌ | ❌ | ✅（INSPECTION 文件） |
| **人可读** | ❌（原始数据） | △（机读为主） | ✅ |
| **对应实现** | `scan_*()` 方法 | `_renumber_violations()` + Violation schema | `InspectionReport.to_markdown()` |

---

## 十、与 ADR 三层关系（元数据级）

```
ADR-0030 · Schema Layer
  定义：能力边界（能不能做）
  产出：risk_level schema · MCP Interceptor policy
  → L1 扫描时参考协议规则边界定义

ADR-0031 · Signal Layer
  定义：治理信号（发生了什么）
  产出：Alert · Drift Signal（S1/S3/S4）
  → L2 解释时参考"何为违规"的治理定义

ADR-0032 · Compiler Layer（本文档主角）
  定义：工具能力（该怎么修的建议）
  产出：INSPECTION.md
  → L3 生成可操作说明书
```

**重要**：ADR-0030 和 ADR-0031 对 L1/L2 的作用是**规则参考**，不是运行时依赖。`fcop_audit()` 在扫描时读取协议规则判断违规，但不调用 GAL API 或 MCP Interceptor——三层均为**静态分析**。

---

## 十一、协议成熟度快照（2026-05-12）

| 层 | ADR | 状态 | 实现 |
|---|---|---|---|
| Schema Layer | ADR-0030 | ✅ Accepted | ✅ risk_level · MCP Interceptor |
| Signal Layer | ADR-0031 | ✅ Accepted | ✅ GAL · fcop_list_alerts · S1/S3/S4 |
| Compiler Layer | ADR-0032 | ✅ Accepted | ✅ fcop_audit · 6 scan_* · INSPECTION.md |

**待定候选**（均需独立 ADR）：

| 候选 | 说明 |
|---|---|
| `fcop_remediate(inspection_id)` | 按 INSPECTION 报告半自动执行 Tier 1（需 ADMIN 二次确认） |
| `INSPECTION-` 升格为第 5 类 frozen envelope | 让 inspection 进入正式 audit chain |
| Codeflow 适配接口规范 | 三层模型对 Codeflow 的对接协议 |

---

## 参考

- `adr/ADR-0030-capability-governance-boundary.md`
- `adr/ADR-0031-governance-alert-layer.md`
- `adr/ADR-0032-fcop-audit-protocol-inspection.md`
- `src/fcop/inspection.py` — L2/L3 数据类实现（Violation / InspectionReport）
- `src/fcop/project.py` — L1 实现（`scan_*()` 方法）+ `Project.audit()` 编排
- `mcp/src/fcop_mcp/server.py` — `fcop_audit()` MCP 工具入口
- `tests/test_fcop/test_audit.py` — 16 个 audit 单元测试
