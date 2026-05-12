# ADR-0033: Trailing Slug Filename Adoption / TASK·REPORT·ISSUE 文件名 trailing-slug 收编

| 字段 | 值 |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-05-12 |
| **Depends on** | ADR-0002（FCoP Filename Grammar 原文法）, ADR-0003（Pre-1.0 SemVer 章程） |
| **Type** | Protocol Extension — Filename Grammar (MINOR additive) |
| **Companion Task** | `fcop/tasks/TASK-20260512-006-ADMIN-to-ME.md` |

---

## 1. 背景 / Motivation

### 1.1 现场涌现

`codeflow` 项目自 2026-05-11 起,PM agent 在落 task / report 时**自发**用形如
下面的"长文件名"代替原协议的短形式:

```
TASK-20260512-025-PM-to-OPS-phase-a-fix-naming.md
TASK-20260512-022-PM-to-OPS-fcop-mcp-1-5-1-housekeeping-commit.md
TASK-20260512-009-PM-to-OPS-codeflow-json-rm.md
REPORT-20260512-009-OPS-to-PM-codeflow-json-rm.md
ISSUE-20260512-001-PM-pm50-userhome-pollution.md
```

截至 ADR 落盘时,`codeflow` 仓库中**至少 22 例**这种长文件名(占该日新增
envelope 的 ~60%)。其它接 fcop 协议的项目也有零星出现。

### 1.2 协议层的"灰色"

按原 `_ROLE = [A-Z][A-Z0-9_]*(?:-[A-Z0-9_]+)*` 文法,这些长文件名是**词法
非法**的 —— 段中含小写字母,违反 `_ROLE` 大写约束。

但 `fcop_audit()` 的所有 `_scan_*` 方法**都没有**做 TASK/REPORT/ISSUE 前缀
文件名的**词法合规**校验:

- `_scan_ghost_prefixes` 只查特定遗留前缀(`AMEND-*` / `*-v2.md`),不查
  正规前缀的内部结构;
- `_scan_misplaced_envelopes` 看 frontmatter `kind:` 字段与目录匹配,
  不看文件名词法;
- `_scan_*` 其它方法各管各的语义维度,均不涉及文件名词法。

**结果**:这些长文件名既不是合规的(词法不过 regex),也不会被 audit 捕获
(没有规则去查),处于"灰色地带"。

### 1.3 触发提案的关键问题

ADMIN 直接问:

> 长文件名是不是已经属于合规了?像这样的?
> `TASK-20260512-025-PM-to-OPS-phase-a-fix-naming.md`

经过 regex 实测 + `_scan_*` 全面盘点,得出诚实结论:

| 维度 | 状态 |
|---|---|
| `parse_task_filename(...)` 返回 | `None`(regex 不匹配) |
| `fcop_audit()` 输出 | 不报告(scan 没覆盖此类) |
| 协议规则原文 | 未规定 |
| 实际落盘文件 | 22+ 例已在 `codeflow` 仓库,Rule 5 禁止改名 |

→ **协议规则、解析器、审计工具三者之间存在不一致**。这本身就是协议要解决的问题。

---

## 2. 决策 / Decision

**协议收编(Protocol Consolidation)**:把 trailing slug 模式作为
**MINOR additive** 扩展正式纳入 FCoP filename grammar。

### 2.1 文法增量

在 TASK / REPORT / ISSUE 文件名的**路由字段尾部**追加一个可选 `-{slug}` 段:

```
TASK-{date}-{seq}-{sender}-to-{recipient}[.{slot}][-{slug}].md
REPORT-{date}-{seq}-{reporter}-to-{recipient}[-{slug}].md
ISSUE-{date}-{seq}-{reporter}[-{slug}].md
```

其中:

```regex
_SLUG = [a-z](?:[a-z0-9-]*[a-z0-9])?
```

- 起手:**小写字母**(强制,见 §3.1 消歧)
- 中段:小写字母 / 数字 / 连字符
- 收尾:**小写字母或数字**(禁止尾部 hyphen,见 §3.2)
- 单字母合法(`x.md`)

### 2.2 slug 不参与路由

工具继续按 `sender` / `recipient` / `slot` 调度。slug 是**人类可读标签**,
不是地址:

- `list_tasks(recipient="OPS")` 同时匹配 `...-PM-to-OPS.md` 和
  `...-PM-to-OPS-anything.md`
- 不创造新的路由维度
- 不引入新的索引开销

### 2.3 完全向后兼容

- 每一份 pre-2.4 的合法文件名仍然合法
- `parse_*_filename(...)` 在旧文件名上返回 `slug=None`
- `build_*_filename(..., slug=None)` 是缺省,行为与 1.1.x 完全一致
- 既有所有单测无需修改

---

## 3. 设计细节 / Design Details

### 3.1 为什么强制小写起手

`_ROLE` 段允许**纯数字内段**:`DEV_01`, `OPS-001` 都是合法角色码。

如果不强制 slug 小写起手,会出现歧义:

```
TASK-20260512-001-PM-to-OPS-001-fix.md
```

两种合法解析:

| 解析 A | 解析 B |
|---|---|
| `recipient=OPS-001`, `slug=fix` | `recipient=OPS`, `slug=001-fix` |

regex 是 greedy 的,实际会取解析 A —— 但语义上歧义存在。强制 slug 起手
`[a-z]` 后,所有大写或数字后缀都必然归入 `_ROLE`,所有小写后缀都必然是
slug,**永无歧义**。

### 3.2 为什么禁止尾部 hyphen

`foo-` 这种 slug 视觉上不完整、提供零信息,且让文件名不雅观。强制末尾
为 `[a-z0-9]` 排除该模式。中段 hyphen 不受影响。

### 3.3 与 REVIEW 的 `subject_short` 关系

REVIEW envelope 的 `subject_short` 字段早已存在类似设计,文法为
`[a-z0-9][a-z0-9-]*`(允许数字起手)。两者**不要求统一**:

- `subject_short` 是 frontmatter 字段,在 YAML 内部,无与 `_ROLE` 的边界
  消歧问题 → 可以放宽到数字起手
- trailing slug 在文件名中,与 `_ROLE` 段相邻 → 必须更严格

这是协议层"局部约束 vs 整体约束"的合理分化。

### 3.4 与 `kind:` 字段语义校验的关系

ADR-0032(`fcop_audit`)已经在 frontmatter 层校验 `kind: task|report|issue`。
此 ADR 只动**词法层**(filename grammar),与语义层正交,不冲突。

---

## 4. 实施 / Implementation

### 4.1 代码改动(`fcop` 包,1.1.x → 1.2.0)

- ✅ `src/fcop/core/filename.py`
  - 新增 `_SLUG` 子模式与 `SLUG_RE` 导出常量
  - `TASK_FILENAME_RE` / `REPORT_FILENAME_RE` / `ISSUE_FILENAME_RE`
    末尾追加 `(?:-(_SLUG))?` 段
  - `TaskFilename` / `ReportFilename` / `IssueFilename` dataclass
    增加 `slug: str | None = None` 字段
  - `parse_*_filename` 解析并返回 slug
  - `build_*_filename` 接 `slug=` 关键字参数,缺省 `None`
  - `_check_components` 校验 slug 合规(走 `SLUG_RE`)
- ✅ `tests/test_fcop/test_core_filename.py`
  - 新增 31 个测试覆盖 trailing-slug 三种 envelope 的 parse / build /
    roundtrip / 拒绝非法 / 向后兼容 / 大写后缀消歧

### 4.2 文档改动

- ✅ `src/fcop/rules/_data/fcop-protocol.mdc`(wheel 内源)
  - frontmatter `fcop_protocol_version` 2.3.0 → 2.4.0
  - "## File Naming" 节后追加 "### Trailing slug (optional)" 子节
  - 末尾 changelog 加 v2.4 条目
- `src/fcop/rules/_data/fcop-rules.mdc` —— **不改**(规则本体未变,
  trailing slug 是 commentary 层面 additive convention)
- 项目根 `.cursor/rules/fcop-protocol.mdc` —— **不直接改**,由
  ADMIN 通过 `redeploy_rules()` 同步(per Rule 8 + ADR-0006)

### 4.3 版本规划

| 包 | 当前 | 目标 | 类型 |
|---|---|---|---|
| `fcop` | 1.5.1 | **1.6.0** | MINOR additive |
| `fcop-mcp` | 1.5.1 | **1.6.0** | MINOR additive |
| `fcop_protocol_version` | 2.3.0 | **2.4.0** | MINOR additive |
| `fcop_rules_version` | (不变) | (不变) | — |

按 ADR-0003 SemVer §MINOR additive:新增可选语法、向后兼容、既有所有行为不变。

---

## 5. 影响与迁移 / Impact & Migration

### 5.1 对 `codeflow` 与已有项目的回溯效果

22+ 例 codeflow 长文件名 **不需要任何迁移**:它们在 1.6.0 安装后自动变成
合规文件名,`parse_task_filename` 现在能解析它们,`slug` 字段被正确填充。

这正是协议收编的目的:**让既有现实变合法,而不是强迫现实回退**。

### 5.2 对 agent 的行为指引

新协议明确**何时该用 slug、何时不该**:

- **DO**: 长任务批次、多 agent 协作、跨日 `ls log/` 扫描需要主题可读
- **DON'T**: 把 `subject` / `parent` / `thread_key` 能表达的信息塞 slug
  → frontmatter 是机器索引,slug 只是人肉标签

### 5.3 对 `fcop_audit()` 的影响

零变更。`fcop_audit` 不查文件名词法,本 ADR 也不要求它查 —— trailing
slug 由 `parse_*_filename` 在 1.6.0 起原生支持,词法层无需 audit 介入。

如果未来需要 audit 层做文件名词法校验(例如检测"slug=`x`"这种零信息
slug),那是另一个 ADR 的事(候选 ADR-0034)。

---

## 6. 备选方案 / Alternatives Considered

### A. 禁止长文件名,通过 audit P0 告警

**否决**。理由:

- 既有 22+ 例需要 Rule 5(append-only)豁免 / 重命名,代价大
- agent 自发用 trailing slug 是**正向**信号(在硬盘可读性上做了优化),
  禁止 = 协议向 agent 倒退
- 协议存在的意义是**约束有害、放过有益**,而非"凡未列入的都禁"

### B. 维持灰色 / 不收编

**否决**。理由:

- 同一份文件被三种工具(`parse_*` / `fcop_audit` / `list_*`)赋予不同
  状态(非法 / 不报告 / 不可读) → 协议自相矛盾
- 让灰色长期存在,会鼓励"反正没人查"的反模式

### C. **协议收编**(本 ADR 采纳)

**采纳理由**:

- ADMIN 一句话点中要害:"agent 之间看得懂"。当 agent 在硬盘上彼此识别
  这套模式时,协议本来就应该把它说清。
- MINOR additive,零破坏成本,完全向后兼容
- 一次性消除三处不一致(规则、解析器、审计)
- 把 codeflow 的现场涌现转化为协议演进 —— 这是 FCoP 自身设计哲学
  ("从涌现学习,沉淀为协议")的一次自我应用

---

## 7. 验收 / Acceptance Criteria

- [x] `parse_task_filename("TASK-20260512-025-PM-to-OPS-phase-a-fix-naming.md")`
      返回非 None,`slug == "phase-a-fix-naming"`
- [x] `parse_task_filename("TASK-20260423-017-ADMIN-to-PM.md")`(旧)返回
      非 None,`slug is None`
- [x] `build_task_filename(..., slug="foo-bar")` 与
      `parse_task_filename(...)` 互逆
- [x] `build_*_filename(slug="Foo")` / `slug="1foo"` / `slug="foo-"` 抛
      `ValueError`
- [x] `fcop_protocol_version: 2.4.0`,changelog 含 v2.4 条目
- [x] 既有 1057 个单测全部通过(`test_tool_surface` 预先存在失败与本 ADR 无关)
- [x] 新增 31 个 trailing-slug 单测全部通过

---

## 8. 公开发布 / Release

本 ADR 是 `fcop@1.6.0` 的核心变更。Release notes 见
`CHANGELOG.md` 中的 `[1.6.0]` 条目(Phase 4 同期产出)。

发布时机:**与 codeflow Mode 1 收尾解耦**,可独立发布。

---

## 9. 后续追踪 / Follow-ups

1. 待 ADMIN 触发 `redeploy_rules()` 同步项目根 `.cursor/rules/fcop-protocol.mdc`
   到 2.4.0
2. 观察后续 codeflow / 其它项目中 slug 的使用模式,若出现普遍性反模式(例如
   slug 与 frontmatter 信息重复),在 ADR-0034 或更晚的版本里追加 audit 层
   检测
3. `fcop_audit` snapshot 漂移(`test_tool_surface` 中 `fcop_audit` 工具
   消失)是**独立问题**,由专门的 task 跟踪,不在本 ADR 范畴

---

## 参考资料 / References

- ADR-0002: FCoP Filename Grammar(原文法定义)
- ADR-0003: Pre-1.0 Stability Charter(SemVer §MINOR additive 章节)
- ADR-0032: `fcop_audit` Protocol-Inspection(为什么 audit 不查词法)
- 同期 task: `fcop/tasks/TASK-20260512-006-ADMIN-to-ME.md`
- 现场触发样本:`d:\Bridgeflow\fcop\tasks\TASK-20260512-025-PM-to-OPS-phase-a-fix-naming.md`
  (路径在用户机器上,原项目代号 codeflow / d:\Bridgeflow 已迁名 codeflow,
   本 ADR 引用时按 codeflow 标准命名)
