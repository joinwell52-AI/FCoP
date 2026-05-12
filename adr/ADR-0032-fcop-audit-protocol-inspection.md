# ADR-0032: fcop_audit() — 协议状态编译器（三场景体检工具）

| 字段 | 值 |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-05-12 |
| **Depends on** | ADR-0029（行为治理协议）, ADR-0030（Capability Governance Boundary）, ADR-0031（GAL） |
| **Type** | Protocol Extension — Protocol Compiler / Remediation Documentation Generator |
| **Milestone** | fcop v1.3.0 |
| **Proposal** | `.fcop/proposals/legacy-project-onboarding-20260512.md` (v1.2, approved) |

> **一句话定位（TL;DR）**
>
> `fcop_audit()` is a **protocol-to-inspection compiler**: it translates FCoP compliance state into structured findings and suggested remediation plans.
>
> FCoP audit does not act. It does not execute. It only translates protocol state into structured remediation documentation.

### ADR 分工关系（三层不可混淆）

| ADR | 职责 | 产出 |
|---|---|---|
| **ADR-0030** | 定义能力边界（能不能做） | Capability schema / risk_level |
| **ADR-0031** | 产生治理信号（发生了什么） | Alert / drift signal |
| **ADR-0032** | 编译协议状态为检查报告（该怎么修的建议） | INSPECTION.md（结构化发现 + 整改建议） |

> ❗ `fcop_audit()` 是"文档生成器"，不是"执行引擎"。INSPECTION 报告是说明书，命令的执行由人或外部 agent 决定。

---

## 1. 背景 / Motivating Example

**实战触发（2026-05-12，D:\Bridgeflow）**：

> ADMIN 在审计一个运行 37 天的老 non-fcop 项目时发现，fcop 当前工具无法机械地告诉他"这个老项目和协议规范的差距是什么"——  
> 只能靠人肉逐条对照协议规则。

具体实证：4 类典型违规，现有工具 `fcop_check` 全部看不到：

| 违规类别 | 实证 | fcop_check 是否告警 |
|---|---|---|
| Rule 2 桶错位 | 99 份 `REPORT-*.md` 在 `fcop/tasks/` 而非 `fcop/reports/` | ❌ git tracked，不算 drift |
| Rule 4.5 三层文档 0% | `fcop/shared/` 空目录 | ❌ 仅显示"0 files"，不标违规 |
| Rule 0 协议规则缺失 | 6 份草根规则，无 `fcop-rules.mdc` | ❌ 不审计 `.cursor/rules/` |
| 草根角色书 + 双 manifest | `fcop/PM-01.md` 等 5 份 + `fcop/codeflow.json` | ❌ 不在任何检查路径 |

**根因**：`fcop_check()` 设计为**日常轻量自检**，只查 working-tree drift 和 session/role 冲突。它不覆盖"协议规范符合度"这个维度。

ADMIN 的洞察：

> "项目文件夹，如果是原来已经有的项目，引入 fcop，是不是更需要一个初始化？"

这个问题揭示了一个 **fcop 三场景模型**：

| 场景 | 起点 | 现有工具 | 缺口 |
|---|---|---|---|
| **new** | 0 文件，新项目 | `init_project()` / `init_solo()` | ✅ 无缺口 |
| **upgrade** | 已有 fcop 老版本 | `redeploy_rules()` + `deploy_role_templates()` | ✅ 无缺口 |
| **takeover** | 老 non-fcop 项目首次引入 | ❌ 无专用工具 | **本 ADR 要解决** |

---

## 2. 决策

引入 `fcop_audit()` 工具，作为**三场景通用的协议合规体检 + 整改文档生成器**。

### 核心原则

> **Inspection = Remediation Plan.**  
> `fcop_audit()` 产出的 INSPECTION 报告本身就是整改说明书——  
> 每条违规都附带**建议执行的命令**、执行人、时长估算、回滚方式和 Tier 优先级。

**关键语义**：Execution Block 里的命令是**建议语义（suggestion）**，不是**执行语义（execution）**。系统生成说明书，执行决策由人或外部 agent 做出。

### 三层内部架构

`fcop_audit()` 内部分三层，职责严格分离：

| 层 | 名称 | 输入 | 输出 | 实现 |
|---|---|---|---|---|
| **L1** | Detection（检测层） | 项目文件系统 | `Violation` 列表 | 6 个 `scan_*()` 方法 |
| **L2** | Interpretation（解释层） | `Violation` | `severity` / `rule_violated` / `impact` | `_renumber_violations()` + schema |
| **L3** | Documentation Generation（文档生成层） | 结构化 `Violation` | INSPECTION.md（structured findings + suggested remediation plan） | `InspectionReport.to_markdown()` |

> L3 的输出是**文档**，不是**执行指令**。`command` 字段是"可复制的建议命令"，`fcop_audit()` 本身不运行它。

### 职责边界

`fcop_audit()` **做**：

- ✅ L1：扫描项目，发现协议违规（6 类盲区 + 基础合规项）
- ✅ L2：结构化事实建模（severity / rule / evidence / impact）
- ✅ L3：生成可执行说明书（含 Execution Block 建议命令）
- ✅ 产出 `INSPECTION-{date}-{seq}-{scope}.md`（落 `fcop/shared/`）
- ✅ 支持三场景（`new` / `upgrade` / `takeover` / `auto`）
- ✅ 零写盘（除 INSPECTION 文件本身），不影响项目工作树

`fcop_audit()` **不做**：

- ❌ **执行**整改命令（执行决策由 ADMIN/PM 做出，`fcop_audit` 只生成建议）
- ❌ 自动修改任何项目文件（纯读 + 写 INSPECTION）
- ❌ 修改 `fcop_check()` 现有行为
- ❌ 修改 frozen 4 类 envelope（task / report / issue / review）
- ❌ 强制项目跑 audit（推荐工具，非协议硬约束）

### fcop_check vs fcop_audit 定位

| | `fcop_check()` | `fcop_audit()` |
|---|---|---|
| **定位** | 日常轻量自检 | 一次性深度体检 |
| **频率** | 每次 session 开始 / 结束 | 引入 fcop / 大版本升级 / 专项审计 |
| **检查范围** | working-tree drift + session/role 冲突 | 协议合规度全量扫描 |
| **产出** | 控制台摘要 | INSPECTION-*.md（含整改方案） |
| **执行时长** | 秒级 | 秒～分钟级（取决于项目大小） |

---

## 3. 三场景规则集 / Scenario Rule Sets

`scope='auto'` 时，系统自动推断：有 `fcop.json` 且版本 < current → `upgrade`；有 `fcop.json` 且版本 ≥ current → `takeover` 风险最低；无 `fcop.json` 且无文件 → `new`；无 `fcop.json` 但有大量文件 → `takeover`。

### 3.1 `new` 场景规则集

触发条件：项目目录几乎为空（文件数 < 10，无 `fcop.json`）

| 检查项 | 期望状态 | Severity |
|---|---|---|
| `fcop.json` 存在 | ✅ | P0 |
| `.cursor/rules/fcop-rules.mdc` 存在 | ✅ | P0 |
| `.cursor/rules/fcop-protocol.mdc` 存在 | ✅ | P0 |
| `fcop/shared/` 下 ≥ 6 份团队文档 | ✅ | P1 |
| 四桶目录存在（tasks/reports/issues/log） | ✅ | P1 |

### 3.2 `upgrade` 场景规则集

触发条件：有 `fcop.json`，`protocol_version` < 当前包版本

| 检查项 | 期望状态 | Severity |
|---|---|---|
| `fcop-rules.mdc` 版本 = 最新 | ✅ | P0 |
| `fcop-protocol.mdc` 版本 = 最新 | ✅ | P0 |
| `fcop/shared/` Role 文档版本 ≥ 当前包 | ✅ | P1 |
| `fcop.json` `protocol_version` 字段已更新 | ✅ | P1 |
| 无 `DRAFT-` / `HANDOFF-` 幽灵前缀文件滞留 | ✅ | P2 |

### 3.3 `takeover` 场景规则集（最完整）

触发条件：有大量文件但 fcop 规范度不足，或无 `fcop.json` 但项目非空

**包含 new + upgrade 全部检查项，额外增加：**

| 检查项 | 扫描方法（内部） | Severity |
|---|---|---|
| `REPORT-*.md` 物理位置（Rule 2 桶错位） | `_scan_misplaced_envelopes()` | P1 |
| 草根角色书（`fcop/*.md` 非协议文件） | `_scan_legacy_role_docs()` | P1 |
| 双 manifest（`fcop/*.json` 非 `fcop.json`） | `_scan_legacy_manifests()` | P1 |
| `.cursor/rules/` 协议规则缺失 / 草根规则混入 | `_scan_cursor_rules()` | P0 |
| `fcop/shared/` 三层团队文档部署度 | `_scan_shared_deployment()` | P1 |
| 幽灵前缀文件（`DRAFT-` / `HANDOFF-` / `AMEND-` / `*-v2.md`） | `_scan_ghost_prefixes()` | P2 |
| 已部署角色文档版本滞后（`fcop/shared/roles/*.md` 内容落后 > 1 个 minor 版本） | `_scan_outdated_role_docs()` | P1 |

---

## 4. 七类扫描方法规格 / _scan_* Specifications

> **实现说明**：以下六个方法均以 `_` 开头（`_scan_*`），是 `Project.audit()` 的**私有子程序**，不属于 `fcop` 的公开 API。
> 外部代码应调用 `project.audit()` 而非直接调用 `_scan_*` 方法。

所有 `_scan_*` 方法均为 **纯读操作**，返回 `list[Violation]`。

### 4.1 `_scan_misplaced_envelopes()`

**目的**：检测 `kind: report/task/issue/review` 文件物理路径与 frontmatter 声明不符（Rule 2）

```python
def scan_misplaced_envelopes(self) -> list[Violation]:
    """
    逻辑：
    1. 遍历 fcop/ 下所有 *.md（含子目录）
    2. 解析 frontmatter kind: 字段
    3. 检查物理路径是否在对应桶目录
       - kind: task   → 期望在 fcop/tasks/
       - kind: report → 期望在 fcop/reports/
       - kind: issue  → 期望在 fcop/issues/
       - kind: review → 期望在 fcop/reviews/
    4. 不符者 → Violation(severity=P1, rule="Rule 2")
    
    整改步骤：git mv {src} {dst} + git commit
    """
```

### 4.2 `_scan_legacy_role_docs()`

**目的**：检测老项目草根角色书（非协议标准文件，Rule 1 冲突风险）

```python
def scan_legacy_role_docs(self) -> list[Violation]:
    """
    逻辑：
    1. Glob fcop/*.md（只查根层，不递归）
    2. 排除：fcop.json、INSPECTION-*.md、SOP-*.md
    3. 排除：已知协议文件（fcop-rules.mdc 等不在此路径）
    4. 检查 frontmatter：若无 kind: 字段 → 草根文件
    5. 多份同角色文件（PM-01.md、PM-02.md）→ 双签风险
    
    整改建议：归档到 fcop/shared/roles/ 或 fcop/log/
    """
```

### 4.3 `_scan_legacy_manifests()`

**目的**：检测 `fcop/` 下非标准 JSON 文件（自创 manifest 会与 `fcop.json` 冲突）

```python
def scan_legacy_manifests(self) -> list[Violation]:
    """
    逻辑：
    1. Glob fcop/*.json
    2. 排除 fcop.json（合法）
    3. 剩余 *.json → Violation(severity=P1)
    
    整改建议：确认内容后删除或迁移到 fcop/shared/
    """
```

### 4.4 `_scan_cursor_rules()`

**目的**：审计 `.cursor/rules/` — 检测协议规则缺失 + 草根规则混入

```python
def scan_cursor_rules(self) -> list[Violation]:
    """
    逻辑（两个子检查）：
    
    SubCheck A — 协议规则缺失（P0）：
      期望文件列表：
        - .cursor/rules/fcop-rules.mdc
        - .cursor/rules/fcop-protocol.mdc
        - AGENTS.md（项目根）
        - CLAUDE.md（项目根）
      任一缺失 → Violation(severity=P0)
      整改：redeploy_rules()（ADMIN 执行）
    
    SubCheck B — 草根规则混入（P2）：
      Glob .cursor/rules/*.mdc
      排除 fcop-rules.mdc / fcop-protocol.mdc
      剩余 → Violation(severity=P2, "non-protocol rules detected")
      整改：ADMIN 审查后手动归档
    """
```

### 4.5 `_scan_shared_deployment()`

**目的**：检测 `fcop/shared/` 三层团队文档部署完整度（Rule 4.5）

```python
def scan_shared_deployment(self) -> list[Violation]:
    """
    逻辑：
    期望文件集（标准 dev-team，8 件）：
      fcop/shared/TEAM-README.md
      fcop/shared/TEAM-README.en.md
      fcop/shared/TEAM-ROLES.md
      fcop/shared/TEAM-ROLES.en.md
      fcop/shared/TEAM-OPERATING-RULES.md
      fcop/shared/TEAM-OPERATING-RULES.en.md
      fcop/shared/roles/{PM,DEV,QA,OPS}-01.md × 4
    
    计算缺失率：
      0%   → green（无 violation）
      1~49% → Violation(severity=P1)
      50%+ → Violation(severity=P0)
    
    整改：deploy_role_templates(team=..., force=True)（ADMIN 执行）
    """
```

### 4.6 `_scan_ghost_prefixes()`

**目的**：检测滞留的幽灵前缀文件（Rule 5）

```python
def scan_ghost_prefixes(self) -> list[Violation]:
    """
    逻辑：
    Glob fcop/**/{DRAFT,HANDOFF,AMEND}-*.md
    Glob fcop/**/*-v[0-9]*.md（如 TASK-001-v2.md）
    任何命中 → Violation(severity=P2)
    
    整改：
      DRAFT-   → 确认内容后重命名为 TASK- 或删除
      HANDOFF- → 确认交接完成后移入 fcop/log/archive/
      AMEND-   → 确认修订合并后删除
      *-v2.md  → 确认为同一 id 的重复版本后删除旧版
    """
```

---

### 4.7 `_scan_outdated_role_docs()`

**目的**：检测已部署角色文档内容滞后于已安装 `fcop` 版本（RULE_DOC_DRIFT）

**背景**：角色文档通过 `deploy_role_templates()` 一次性部署到 `fcop/shared/roles/`，
此后不会自动随 `fcop` 包升级而更新。若已安装的 `fcop` 新增了 REVIEW envelope /
`risk_level` / `supersedes:` 等能力，但角色文档仍停在旧版本，Agent 读取时不会感知
新协议功能，导致**协议能力认知漂移**（RULE_DOC_DRIFT）。

**适用范围**：`scope=upgrade` / `scope=takeover`

```python
def _scan_outdated_role_docs(self) -> list[Violation]:
    """
    逻辑：
    1. 读取已安装 fcop 包版本（major.minor）
    2. Glob fcop/shared/roles/*.md
    3. 对每个文件：用正则 r"v(\d+)\.(\d+)" 提取最高版本号
       - 无版本引用 → 记入 outdated 列表
       - 最高版本与已安装版本 gap > 1 minor → 记入 outdated 列表
    4. outdated 非空 → Violation(severity=P1, rule="RULE_DOC_DRIFT")

    违规类型：RULE_DOC_DRIFT（角色文档协议漂移）
    整改：deploy_role_templates(force=True)
    """
```

**违规类型字段**：`rule_violated = "RULE_DOC_DRIFT (角色文档协议漂移)"`

**整改建议**：调用 `deploy_role_templates(force=True)` 重新部署最新角色模板

---

## 5. 数据结构 / Data Classes

```python
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Literal


@dataclass(frozen=True)
class RemediationStep:
    """单条整改操作，可直接复制执行。"""
    action: str                                      # 一句话描述
    command: str                                     # 可复制的 shell / MCP 调用
    command_unix: str | None = None                  # Unix 等价命令（PowerShell 主命令时填写）
    executor: Literal["ADMIN", "PM", "OPS", "mixed"] = "ADMIN"
    estimated_minutes: int = 5
    tier: Literal[1, 2, 3] = 1
    rollback: str | None = None                      # 回滚操作或说明
    precondition: str | None = None                  # 前置条件（若有）


@dataclass(frozen=True)
class Violation:
    """单条协议违规发现。"""
    violation_id: str                                # P0-001, P1-003, etc.
    severity: Literal["P0", "P1", "P2"]
    rule_violated: str                               # "Rule 2 (桶错位)"
    summary: str                                     # 一句话描述
    evidence: list[str]                              # 文件路径 / 计数 / 行号
    impact: str                                      # 业务影响说明
    remediation: list[RemediationStep]
    scan_source: str                                 # 产生此 violation 的 scan_* 方法名


@dataclass
class InspectionReport:
    """体检报告 = 违规清单 + 整改方案。"""
    inspection_id: str                               # INSPECTION-20260512-001
    scope: Literal["new", "upgrade", "takeover"]
    project_path: Path
    inspected_at: datetime
    fcop_version: str                                # fcop 包版本
    fcop_rules_version_local: str | None             # 项目本地 rules 版本
    fcop_rules_version_package: str                  # 当前包内 rules 版本
    overall_status: Literal["green", "needs_remediation", "blocked"]
    violations: list[Violation] = field(default_factory=list)

    # 计算属性（post_init 填充）
    p0_count: int = 0
    p1_count: int = 0
    p2_count: int = 0
    estimated_total_minutes: int = 0

    def __post_init__(self) -> None:
        self.p0_count = sum(1 for v in self.violations if v.severity == "P0")
        self.p1_count = sum(1 for v in self.violations if v.severity == "P1")
        self.p2_count = sum(1 for v in self.violations if v.severity == "P2")
        self.estimated_total_minutes = sum(
            s.estimated_minutes
            for v in self.violations
            for s in v.remediation
        )

    def to_markdown(self) -> str:
        """渲染为 L3 完整报告（含 YAML frontmatter + Execution Block）。"""
        ...

    def to_dict(self) -> dict[str, object]:
        """机读 JSON，供 fcop_remediate() 后续 ADR 消费。"""
        ...
```

---

## 6. INSPECTION 报告格式 / L3 Output Format

**协议级语义声明**：

> `INSPECTION` ≠ Remediation Plan  
> `INSPECTION` = Structured Findings + Suggested Remediation Plan

INSPECTION 是"结构化发现 + 整改建议"的复合体，不是"整改指令"。其中：
- **Structured Findings**：L1/L2 产出的客观事实（违规 ID / 规则 / 证据 / 影响）
- **Suggested Remediation Plan**：L3 基于发现生成的*建议*行动（Execution Block 里的命令是建议，不是指令）

INSPECTION 报告落点：`fcop/shared/INSPECTION-{YYYYMMDD}-{NNN}-{scope}.md`

- **append-only**：同一天同 scope 第二次跑产出 `NNN=002`，不覆盖
- **`kind: inspection`**：新 UPPERCASE prefix，不进 frozen 4 桶
- **双格式**：`to_markdown()` 给人读，YAML frontmatter 机读，`to_dict()` 给程序消费

### 6.1 报告结构

```
frontmatter (YAML)
  ├─ inspection_id / scope / project / inspector
  ├─ fcop_version / fcop_rules_version_*
  ├─ overall_status / p0_violations / p1_violations / p2_violations
  └─ estimated_total_minutes

## 摘要（状态图标 + 分档计数 + 预估时长）

## P0 · 阻塞性违规（N 项）
  └─ ### P0-001 · <规则名>
       ├─ 实证（文件路径 / 计数）
       ├─ 影响
       ├─ 整改命令（可复制 PowerShell + unix 注释）
       ├─ 执行人 / 预估时长
       └─ 回滚 / 前置条件

## P1 · 规范性违规（N 项）
  └─ （同 P0 结构）

## P2 · 整洁性违规（N 项）
  └─ （同 P0 结构）

## ▶ 执行块 · Execution Block（核心创新）
  ├─ ### Tier 1 · 立即（今日内，无前置，低风险）
  │    ├─ 步骤 1: <命令块（可直接复制）>
  │    ├─ 步骤 2: ...
  │    └─ 回滚方式
  ├─ ### Tier 2 · 本 sprint（1~2 day，有前置）
  └─ ### Tier 3 · 后续清理（next sprint，低优先）

## 复检建议
  └─ fcop_audit(scope="auto")   # 产出 INSPECTION-{date}-NNN+1-{scope}.md
```

### 6.2 Execution Block 设计原则

Execution Block 是本 ADR 相对于传统体检报告的**核心创新**。

**语义声明**：Execution Block 是**建议性文档（suggestion document）**，不是系统指令。`fcop_audit()` 生成"可复制的命令建议"，执行决策由 ADMIN/PM 在阅读报告后做出。

1. **命令可直接复制（建议语义）**：每个步骤的 `command` 块是"建议执行的命令"，可粘贴到 shell 或 MCP 客户端，但**执行前须人工确认**
2. **双平台**：PowerShell 主命令块 + `# unix:` 注释行
3. **按 Tier 分组**：Tier 1 全部归在一起，方便 ADMIN 一次性跑完，再看 Tier 2
4. **回滚内嵌**：每个步骤下方直接给出回滚建议，不需要翻找
5. **状态感知**：`overall_status: blocked` 时，Execution Block 置顶警告

> 设计约束：Execution Block ≠ 执行引擎。未来若需"自动按报告执行"，应另立 `fcop_remediate()` ADR（见 §9.3）。

---

## 7. Python API + MCP 工具签名

### 7.1 Python API

```python
# src/fcop/project.py — Project 类新增方法
def audit(
    self,
    scope: Literal["new", "upgrade", "takeover", "auto"] = "auto",
    output: Literal["file", "stdout", "both"] = "file",
) -> InspectionReport:
    """三场景通用的协议体检 + 整改方案生成器。

    零写盘（除 INSPECTION 文件本身）。
    纯读操作序列：
      1. 推断 scope（若 auto）
      2. 按 scope 启用规则集，调对应 scan_*() 方法
      3. 为每条 Violation 生成 RemediationStep 列表
      4. 渲染 InspectionReport（to_markdown() + to_dict()）
      5. output='file' 时写 fcop/shared/INSPECTION-{date}-{seq}-{scope}.md
    """
```

### 7.2 MCP 工具

```python
# mcp/src/fcop_mcp/server.py
@mcp.tool
def fcop_audit(
    scope: str = "auto",        # "new" | "upgrade" | "takeover" | "auto"
    output: str = "file",       # "file" | "stdout" | "both"
    project_path: str = ".",
) -> str:
    """**协议体检工具**。扫描项目，发现协议合规缺口，产出"体检即整改方案"报告。

    产出物：fcop/shared/INSPECTION-{date}-{NNN}-{scope}.md

    三个 scope：
    - new      : 新项目验收（协议文件是否完整部署）
    - upgrade  : 版本升级后验收（规则版本 / 文档版本是否同步）
    - takeover : 老项目首次引入 fcop（全量合规扫描，含 6 类盲区）
    - auto     : 自动推断（推荐）

    报告含 Execution Block：每条违规附带可直接复制的整改命令、执行人、Tier 优先级和回滚方式。

    Note: fcop_audit 是一次性深扫，fcop_check 是日常轻量自检，二者互补。
    """
```

---

## 8. 实施路径 / Implementation Plan

| 阶段 | 内容 | 时长 | 负责人 |
|---|---|---|---|
| 0. 本 ADR 审议 | ADMIN 确认接受 | ✅ 已完成 | ADMIN |
| 1. 数据类实现 | `Violation` / `RemediationStep` / `InspectionReport` + `to_markdown()` | 2 day | 实现者 |
| 2. scan_* 实现 | 6 个扫描方法（§4） | 3 day | 实现者 |
| 3. `Project.audit()` 集成 | scope 推断逻辑 + 规则集路由 + 文件写入 | 1 day | 实现者 |
| 4. MCP `fcop_audit()` | server.py 注册 + 参数校验 + 错误处理 | 0.5 day | 实现者 |
| 5. 单元测试 | 三 scope fixture（空项目 / 老 fcop / Bridgeflow 样本） + 6 scan_* 单测 | 2 day | 实现者 |
| 6. Dogfood | D:\FCoP 自身 `scope='takeover'` + D:\Bridgeflow 现场跑 | 1 day | ADMIN + 实现者 |
| 7. 发版 | 合并 GAL（ADR-0031）+ fcop_audit（ADR-0032）→ fcop v1.3.0 | 0.5 day | ADMIN |

**总周期**：~10 day（实现阶段 1~4 可重叠）

---

## 9. 范围与边界 / Scope & Boundary

### 9.1 本 ADR 要做

- `fcop_audit()` Python API + MCP 工具（§7）
- `InspectionReport` / `Violation` / `RemediationStep` 数据类（§5）
- 六类 `scan_*` 扫描方法（§4）
- L3 INSPECTION 报告格式含 Execution Block（§6）
- 三场景规则集（§3）
- `INSPECTION-` 新 UPPERCASE prefix（落 `fcop/shared/`）
- 工具快照 `tool_surface.json` 更新（`fcop_audit` 登记）

### 9.2 本 ADR 不做

- **不做整改自动化**：`fcop_audit()` 产出 plan，执行由人触发（留给 `fcop_remediate()` 后续 ADR）
- **不改 `fcop_check()` 行为**：两者职责互补，独立存在
- **不改 frozen 4 类 envelope**：`INSPECTION-` 是第 5 种 UPPERCASE prefix，走 `fcop/shared/`
- **不强制集成到 `init_project()` hook**：`fcop_audit` 是手工调的一次性工具

### 9.3 后续可选（后续 ADR 候选）

- `fcop_remediate(inspection_id)` — 按 INSPECTION 报告自动执行 Tier 1（需 ADMIN 二次确认，对应 fcop 9.5.1 risk_level=irreversible）
- `INSPECTION-` 升格为 frozen 第 5 类 envelope — 让 inspection 进入 audit chain

---

## 10. 风险与对策

| 风险 | 概率 | 对策 |
|---|---|---|
| 三场景规则集设计偏差，漏掉盲区 | 中 | Dogfood 阶段 D:\FCoP + D:\Bridgeflow 真实样本补缺 |
| INSPECTION 报告字段项目间偏差 | 低 | 数据类 frozen，Markdown 渲染按固定模板 |
| PowerShell / bash 命令不兼容 | 中 | 默认 PowerShell + `# unix:` 注释双版本 |
| `fcop_check` vs `fcop_audit` 用户混淆 | 中 | docstring 明示；§2 对照表写入协议文档 |
| scope='auto' 推断错误（把 new 项目推断为 takeover） | 低 | 推断逻辑保守：宁可多扫，规则集取并集 |
| Dogfood 发现严重设计缺陷 | 低 | Dogfood 在 RC 阶段，发现问题可在 1.3.0 正式版修复 |

---

## 11. 非目标 / Non-Goals

`fcop_audit()` 明确**不是**：

- ❌ **执行引擎**：工具生成命令建议，不执行命令（执行由人或 `fcop_remediate()` 决定）
- ❌ **Orchestration Layer**：`fcop_audit()` 不调度任何 agent 行为
- ❌ **自动治理系统**：不会因为发现违规而自动修复或阻塞流程
- ❌ 安全扫描工具（漏洞 / 密钥泄露不在范围）
- ❌ 代码质量检查（linting / coverage 不在范围）
- ❌ 项目管理工具（进度 / 里程碑不在范围）

> 防漂移声明：若未来出现"让 `fcop_audit` 自动执行整改"的需求，必须单独立 ADR，不得悄然扩展本工具的职责边界。这是 FCoP 避免"从治理协议滑向 orchestration layer"的硬约束。

---

## 12. 参考

- `src/fcop/project.py` — `Project.audit_drift()` 现有实现（盲区起点）
- `mcp/src/fcop_mcp/server.py` — `fcop_check()` 工具（日常自检对照）
- `adr/ADR-0030-capability-governance-boundary.md` — risk_level 分级模型
- `adr/ADR-0031-governance-alert-layer.md` — GAL 漂移信号（fcop_audit 扫描结果可触发 GAL）
- `.fcop/proposals/legacy-project-onboarding-20260512.md` — 提案 v1.2（本 ADR 的需求来源）
- `D:\Bridgeflow` — 触发本 ADR 的真实案例项目
