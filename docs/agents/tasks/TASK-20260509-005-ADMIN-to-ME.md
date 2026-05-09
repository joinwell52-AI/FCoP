---
protocol: fcop
version: 1
type: TASK
sender: ADMIN
recipient: ME
date: 2026-05-09
priority: P0
status: in_progress
subject: Boundary 抽象端到端：layer + capability vocabulary 接进 reference impl
ref_charter: adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md
ref_adr: adr/ADR-0020-agent-boundary-and-capability.md
ref_predecessor: docs/agents/log/tasks/TASK-20260509-004-ADMIN-to-ME.md
acceptance_criteria_count: 11
---

# TASK-20260509-005-ADMIN-to-ME

> Solo 模式任务。v1.0 7 抽象 reference-impl wiring 第 **2/7**——第 1 个是
> TASK-004 的 REVIEW（Audit）。本任务把 ADR-0020 写在纸上的 layer +
> capability vocabulary 接进配置层 + 校验函数 + 写入路径，并在每写
> 一个 envelope 时**默认就检查 boundary**（事件留给 TASK-007 接收方
> 实现 BOUNDARY_VIOLATED 推送）。

---

## 1 · 为什么需要这个任务（why now）

ADR-0020 已经在 `boundary.schema.json` 里冻结了 10 个 capability token
词表 + 4 条 boundary 规则；但**没有任何代码消费它**。意思是：

- 任何 worker agent 现在仍可以 `Project.write_review`（应被 Rule
  `NO_WORKER_REVIEWS_GOVERNANCE` 拒）
- 任何 governance agent 现在仍可以 `Project.write_task` 给另一个
  governance（应被 `NO_GOVERNANCE_FISSION` 拒）
- `fcop.json` 添加 `layer: "admin"` 不会被运行时 reject（应被
  `NO_ADMIN_PROGRAMMATIC_CREATE` 拒）

→ Schema 是死字。本任务让它活。

---

## 2 · ADMIN 决议（针对本任务）

### 决议 1 · 不引入 `Role` dataclass，用 `_role_labels` extra 承载

ADR-0020 §design-details 原文写「`models.Role` dataclass 加字段」。
**修订**：v1.0 不引入 `Role` dataclass。理由：

- `TeamConfig.roles` 当前是 `tuple[str, ...]`——任何引入 dataclass
  替换的方案都会打破 ADR-0003 §additive-only（破坏 7+ 处 caller，包括
  fcop-mcp 包的 `init_project` adapter）。
- 实际数据已经能通过 `_extract_roles` 的 dict-form 分支落进
  `TeamConfig.extra["_role_labels"][code]`——已有 carrier，不需要新
  数据结构。
- 公开面 delta 最小：仅新增 `core/boundary.py` 模块的查询函数与
  `Project.boundary_violations()` 一个方法。

→ 本任务把 layer / can / cannot 字段约定为存在
`_role_labels[code]["layer"|"can"|"cannot"]` 路径下；新增
`fcop.core.boundary.lookup_capability(code, config)` 公开函数做
解析+default 填充；TASK-005-Phase-2（独立后续 TASK）再考虑是否
在 v1.1 引入 `Role` dataclass（届时 additive-only 路径：新加字段
`TeamConfig.role_capabilities: tuple[Role, ...] | None = None`）。

### 决议 2 · 新增 `core/boundary.py` 模块

公开 API（仅 import 一份就能用）：

- `LAYER_DEFAULTS: dict[str, LayerBundle]` —— 3 个 layer 的默认
  capability bundle（worker / governance / admin），与 ADR-0020
  §decision 表对齐
- `Capability` —— `@dataclass(frozen=True, slots=True)` 表示
  `(code, layer, can: tuple[str, ...], cannot: tuple[str, ...])`
- `lookup_capability(role_code: str, config: TeamConfig) -> Capability`
  —— 按 role code 查；若 fcop.json 显式声明了 layer/can/cannot 用
  显式值，否则回落 layer default = worker
- `validate_action(actor: Capability, action: str, *, target: Capability | None = None) -> list[BoundaryViolation]`
  —— 按 4 条 ADR-0020 规则 + capability 词表给出违规列表（空 = 允许）
- `BoundaryViolation` —— `@dataclass(frozen=True, slots=True)`：
  `(rule_id: str, actor: str, action: str, target: str | None, message: str)`
- `BOUNDARY_RULES: tuple[str, ...]` —— 4 条规则 id 常量

**不**走 fcop 顶层 `__all__`——按 ADR-0001 `core.*` 是 internal。
但 `BoundaryViolation` dataclass 通过 `Project.boundary_violations()`
等公开方法返回，所以从 `models.py` 重导出。

### 决议 3 · `Project.boundary_violations(actor_role)` 公开方法

不要把 boundary 检查偷偷塞进 write_*（那会让 0.7.x callers 无预警
开始挂）。本任务提供：

- **opt-in 显式查询**：`Project.boundary_violations(actor_role: str, action: str, *, target_role: str | None = None) -> list[BoundaryViolation]`
- **opt-in 守门 wrapper**：`Project.assert_boundary(actor_role, action, *, target_role=None) -> None` —— 违规即 raise
  `BoundaryViolationError`（新异常，从 `fcop.errors` 公开）

write_review 在 R2 主动调 `assert_boundary(reviewer_role,
"review_decision", target_role=...)`——这是 v1.0 第一个**强制**接
boundary 的写入路径，它本身是 v1.0 新 API 没有 0.7.x 兼容包袱。
write_task / write_report / write_issue **不**接（保 0.7.x callers
不变）；它们将在 v1.1 通过新参数 `enforce_boundary=False`（默认）
逐步引入 opt-in 强制。

### 决议 4 · `admin` layer 在 `fcop.json.roles` 是否合法？

ADR-0020 Open Question 1 选 **不允许**。`Capability` 解析时若
`role_code` 来自 `fcop.json` 且 layer 显式设为 `"admin"`，
`lookup_capability` 抛 `BoundaryViolationError(rule="NO_ADMIN_PROGRAMMATIC_CREATE")`
—— 这一条本身就是 ADR-0020 校验的第 1 条规则。

但 ADMIN 仍可作为 `sender` / `recipient` 出现在 envelope frontmatter
（per `core/schema.validate_role_code(allow_reserved=True)`）—— 那
是「人在角色」语义，不是「config-driven agent」。两者不冲突。

### 决议 5 · 4 条规则的具体语义（编码进测试）

按 ADR-0020 §decision 表 + ADR-0015 §抽象 6：

| Rule id | 触发条件 | violations |
|---|---|---|
| `NO_ADMIN_PROGRAMMATIC_CREATE` | `lookup_capability(code, config)` 时 `_role_labels[code]["layer"] == "admin"` | actor=code, action="create", target=None |
| `NO_GOVERNANCE_FISSION` | actor.layer == governance AND action == "spawn_agent" AND target is None | actor=code, action="spawn_agent" |
| `NO_WORKER_REVIEWS_GOVERNANCE` | actor.layer == worker AND action == "review_decision" AND target.layer == governance | actor=actor.code, action="review_decision", target=target.code |
| `EXPLICIT_OVERRIDES_LAYER` | 显式 `cannot` 列表中含 action（无论 layer default 是否允许） | actor=code, action=action |

补充规则（ADR-0015 §抽象 6 提到但 ADR-0020 没列入 4 条）：
- 若 action **不在** 10 个 capability vocabulary 中 → 不视为 violation，
  但 `validate_action` 返回一条 `severity="warning"` 类型的
  BoundaryViolation 让 caller 知情（rule_id="UNKNOWN_CAPABILITY"）。这
  能兼容 v1.x 词表外的 caller。

### 决议 6 · v1.0 不实现的（独立 TASK）

- `BOUNDARY_VIOLATED` 事件触发 → **TASK-007**（Event Model 接收方）
- `fcop migrate-fcop-json` CLI 自动加 layer 字段 → **TASK-008** 已规划的 migrate-workspace 一并接
- write_task / write_report / write_issue 强制 boundary → **TASK-005-Phase-2**
- `fcop_report()` 显示 boundary 缺字段警告 → **TASK-005-Phase-2**
- 补充更多自定义 capability token 的注册机制 → v1.1，依用户反馈

---

## 3 · 验收标准（11 条）

| # | 标准 | 证据 |
|---|---|---|
| A1 | `core/boundary.py` 模块存在；export `LAYER_DEFAULTS` / `Capability` / `BoundaryViolation` / `BOUNDARY_RULES` / `lookup_capability` / `validate_action` | `from fcop.core.boundary import ...` |
| A2 | `LAYER_DEFAULTS` 含 3 个 layer × 与 boundary.schema.json 词表内 token 完全相符 | `test_layer_defaults_align_with_schema` |
| A3 | `lookup_capability` 对未声明 capability 的 role 回落 worker default；对显式 `layer: "admin"` 的 role 抛 `BoundaryViolationError(rule="NO_ADMIN_PROGRAMMATIC_CREATE")` | `test_lookup_capability` |
| A4 | `validate_action` 4 条规则各自至少 2 个 case（合法 + 违规）；显式 cannot 覆盖 layer default 单测 | `test_boundary_rules` ≥ 10 用例 |
| A5 | `BoundaryViolation` 与 `BoundaryViolationError` 通过 `models.py` / `errors.py` 公开导出，从顶层 `fcop` 包可 import | import smoketest |
| A6 | `Project.boundary_violations(actor_role, action, target_role=)` 端到端工作 | `test_project_boundary` |
| A7 | `Project.assert_boundary` 违规时 raise `BoundaryViolationError`，合法时静默返回 | `test_project_boundary` |
| A8 | `write_review` 写入前调 `assert_boundary(reviewer_role, "review_decision", target_role=...)`；worker reviewer 评 governance subject 时 raise | `test_review_boundary_enforce` |
| A9 | `_extract_roles` 在 dict-form 分支接受 `layer` / `can` / `cannot` 字段并保留进 `_role_labels`；round-trip serialize → load → 数据无丢失 | `test_core_config_role_capability` |
| A10 | snapshot `tests/test_fcop/snapshots/public_surface.json` 更新含 +5 项（2 dataclass + 1 异常 + 2 方法） | `test_public_surface` 通过 |
| A11 | REPORT-005 + 归档 + commit + push + CHANGELOG 加 Unreleased / Added 条目 + ADR-0020 状态从 Proposed → Accepted（含 Sign-off date） | git log + adr/ADR-0020 |

---

## 4 · 执行计划（4 commit）

| Round | 交付物 | Commit |
|---|---|---|
| R1 | `core/boundary.py` 模块（含 LAYER_DEFAULTS / dataclasses / lookup / validate_action）+ `models.py` 加 `BoundaryViolation` + `errors.py` 加 `BoundaryViolationError` + 全套 boundary 单测（≥ 15 用例） | `feat(core): boundary 词表与 4 条规则的 reference impl` |
| R2 | `_extract_roles` / `_collect_extra` 接受 layer/can/cannot；`Project.boundary_violations` + `assert_boundary` 公开方法；`write_review` 接进 boundary 强制；snapshot 更新；CHANGELOG | `feat(project): boundary 接 write_review + Project 公开 API` |
| R3 | ADR-0020 状态 Proposed → Accepted（加 Sign-off date 与 commit ref）；ADR-0010 superseded-by 行加 ADR-0020 link 校核；adr/README.md 索引同步 | `adr(0020): accept boundary ADR + 索引同步` |
| R4 | REPORT-005 + 归档 TASK-005 + push | `close TASK-20260509-005：boundary 抽象已发车` |

任何一轮 pytest 红 → 修完再 commit。**绝不 commit 红 pytest。**

---

## 5 · 风险登记

| 风险 | 缓解 |
|---|---|
| `_role_labels` 改 schema → 破坏 round-trip | 仅**追加** layer/can/cannot 三个 key 到既有 dict 内；序列化路径不变 |
| boundary 新规则在已有项目里突然挡掉合法操作 | write_review 是 v1.0 新 API（无历史 caller），write_task/report/issue **不接** —— 0.7.x 0% 影响 |
| `lookup_capability` 在 lookup 时 raise 影响热路径 | 仅 `layer: "admin"` 一条 raise；其他 default 路径无 raise |
| ADR-0020 状态从 Proposed 改 Accepted 需要 sign-off 流程 | solo 模式 ADMIN ≡ ME，本人 sign（在 ADR Sign-off 段加日期 + commit ref）|
| `Capability.can / cannot` 用 list vs tuple | 用 tuple（dataclass slots=True frozen，list 不 hashable）；`_role_labels` 反序列化时 list → tuple normalize |
| 公开面 +5 项触发 snapshot diff | R2 单独更新；diff 全部是 added 方向，符合 ADR-0003 |

---

## 6 · 三视角预飞

### Proposer
v1.0 7 抽象进度：1/7 完成（Audit/REVIEW），本任务推到 2/7
（Boundary）。**boundary 是 7 抽象里唯一同时影响 3 个其他抽象的——
Agent（layer 字段消费）、IPC（write_review enforcement）、Audit
（review 是 enforcement consumer）**。完成它解锁 v1.0 RC ship 路径
上 50% 的剩余风险。

### Executor
4 commit；R1 全新模块 + 新测试，无既有 src 修改；R2 触及
`core/config.py`（dict-form leftover 一处 additive）+ `project.py`
（一段 import + 一段 write_review hook + 2 个新方法）+ `models.py`
+ `errors.py`（各加一个符号）+ snapshot 更新；R3 / R4 文档与归档。
**0.7.x callers 0 影响**——boundary 是 opt-in API，强制路径仅 v1.0
新 API（write_review）。

### Reviewer
拒收预设：
- ❌ `TeamConfig.roles` 类型被改 → 触发立刻拆任务
- ❌ write_task / write_report / write_issue 自动接 boundary → 拒（v1.1 议题）
- ❌ ADR-0020 改文（除 Status 段）→ 拒（ADR immutable）
- ❌ 任何 boundary 规则新增（除 ADR-0020 列的 4 条 + UNKNOWN_CAPABILITY warning） → 拒（需新 ADR）
- ❌ `BoundaryViolation` 字段变更 → 拒（首发就 frozen）

---

## 7 · 签收

```
Sender:    ADMIN
Recipient: ME (solo 模式)
Status:    in_progress
Opened:    2026-05-09
Charter:   ADR-0015 §execution roadmap step 2（reference-impl wiring）
ADR:       ADR-0020 Agent Boundary & Capability（本任务接 R3 转 Accepted）
Touches:   src/fcop/core/boundary.py（新建）、core/config.py（additive）、
           project.py（additive）、models.py（additive）、errors.py（additive）
```

立即开始 R1。
