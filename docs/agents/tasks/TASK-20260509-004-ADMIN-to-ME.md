---
protocol: fcop
version: 1
type: TASK
sender: ADMIN
recipient: ME
date: 2026-05-09
priority: P0
status: in_progress
subject: JSON Schema 校验器接入 reference impl + REVIEW（Audit 抽象）端到端落地
ref_charter: adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md
ref_predecessor: docs/agents/log/tasks/TASK-20260509-003-ADMIN-to-ME.md
acceptance_criteria_count: 10
---

# TASK-20260509-004-ADMIN-to-ME

> Solo 模式任务。**第一个动 `src/fcop/` 的任务**。TASK-003 把 schema 写在了纸上；本任务让 reference implementation 真正吃这份纸——端到端覆盖 7 个抽象里的 2 个：**Schema 校验基础设施（横切）** 和 **Audit / REVIEW（抽象 7）**。

---

## 1 · 为什么这样切 scope

REPORT-003 §6 列了 6 个剩余种子（TASK-004 ~ TASK-008）。最朴素的读法是「TASK-004 = `Project.write_review` + `subscribe_events` + `recover_session` + `report_failure` + dataclass 对齐 全做了」。但那等于动了**剩下 5 个抽象**，涉及 ~1000+ 行 src/ 改动——不是 atomic 任务，是 release。

本任务**故意收窄**到两块依赖关系最清晰、Project 公开面 delta 最小的：

1. **Schema 校验基础设施（横切）**：新增 `core/jsonschema_validator.py`，加载 7 份 `spec/schemas/*.schema.json`，对外暴露 `validate_envelope_frontmatter(frontmatter, envelope_type)` + `validate_record(record, schema_name)`。**仅 opt-in**——现有 caller 完全不变。同时把 ADR-0016 §tests-checklist 承诺的 `tests/test_schemas/` 全套测试落齐。

2. **REVIEW（Audit，抽象 7）**：[ADR-0017](../../adr/ADR-0017-review-file-type-minimal.md) 端到端实现——dataclass、文件名 grammar、frontmatter parser、4 个 `Project` 方法（`write_review` / `read_review` / `list_reviews` / `archive_review`）、`reviews/` 目录约定、回归测试、public surface snapshot 更新。

**Boundary（ADR-0020 enforce）、Event（ADR-0018 watcher）、Failure（ADR-0019 API）、migrate-workspace（ADR-0022 CLI）各开独立后续任务** —— 分别为 TASK-005 / 006 / 007 / 008。这样每个任务都 atomic 可审。

### 为什么这两块捆在一起做（而不是只做 schema）

Schema 校验器没有消费者就是死代码。REVIEW 是**最简单的消费者**：v1.0 全新引入，没有历史 frontmatter 要兼容、没有行为 compat 测要写——`write_review` 从第一天起就用 `review.schema.json` 校验。两块并入一个任务，让 R1 和 R2 共用一次 CI 循环 + 一次 snapshot bump。

---

## 2 · ADMIN 决议（针对本任务）

### 决议 1 · Schema 怎么打进 wheel

7 份 schema 在 `spec/schemas/*.schema.json`（TASK-003 落的）。Python 包运行时需要它们。考虑过三个方案：

| 方案 | 评判 |
|---|---|
| 写自定义 hatchling build hook 把 `spec/schemas/` 复制进 wheel | 太脆；source install 路径还要再写一遍 |
| 运行时按相对路径读 | 开发模式 OK，wheel 装好后 `spec/` 不在包里就坏 |
| ✅ **同步一份副本到 `src/fcop/_data/schemas/`，作为 wheel 内权威路径** | 简单稳；CI 测断言两份字节一致 |

采用方案 3。`src/fcop/_data/schemas/` 是**包内权威**；`spec/schemas/` 是**协议权威**。新增测试 `tests/test_schemas/test_bundled_schemas_in_sync.py` 强制两份相同——任何 commit 让两份漂移都会断 CI。

### 决议 2 · `core/jsonschema_validator.py` 是新模块

不要往 `core/schema.py` 上叠——按 ADR-0001 那个模块是**协议常量**模块，语义角色不同。开个兄弟模块。公开面 delta：

- `fcop.core.jsonschema_validator.validate_envelope_frontmatter(fm: dict, envelope_type: str) -> list[ValidationIssue]`
- `fcop.core.jsonschema_validator.validate_record(record: dict, schema_name: str) -> list[ValidationIssue]`
- 模块级常量：`BUNDLED_SCHEMA_DIR: Path`、`SCHEMA_REGISTRY`（`referencing.Registry` 实例）、`SCHEMA_NAMES: tuple[str, ...]`

这些**不进**顶层 `fcop.__all__` —— 按 ADR-0001 `core.*` 是 internal。它们由 `Project.write_review` 等内部使用；测试通过 `fcop.core.jsonschema_validator` 直接拿。

### 决议 3 · `Review` dataclass 形状

frozen + slotted（与 Task / Report / Issue 一致）。字段对齐 [ADR-0017 §design-details]：

```python
@dataclass(frozen=True, slots=True)
class Review:
    path: Path
    filename: str
    review_id: str          # REVIEW-{date}-{seq}-{reviewer}-on-{subject_short}
    date: str               # YYYYMMDD
    sequence: int           # 1..999
    subject_type: ReviewSubjectType   # task | report | role_switch | code_change
    subject_ref: str        # 文件路径 或 hash
    reviewer_role: str
    reviewer_agent: str | None
    decision: ReviewDecision  # approved | rejected | needs_changes | abstained
    rationale: str | None
    required_changes: tuple[str, ...]
    decided_at: datetime
    body: str
    is_archived: bool
    mtime: datetime
```

外加两个新枚举（在 `models.py`）：
- `ReviewDecision(str, Enum)`：APPROVED / REJECTED / NEEDS_CHANGES / ABSTAINED
- `ReviewSubjectType(str, Enum)`：TASK / REPORT / ROLE_SWITCH / CODE_CHANGE

### 决议 4 · `Project.write_review` 签名

```python
def write_review(
    self,
    *,
    reviewer_role: str,
    subject_type: str | ReviewSubjectType,
    subject_ref: str,
    decision: str | ReviewDecision,
    rationale: str | None = None,
    required_changes: Iterable[str] = (),
    reviewer_agent: str | None = None,
    body: str = "",
    date: str | None = None,            # 默认 = 今天 (YYYYMMDD)
) -> Review:
```

校验合约：
- `decision == NEEDS_CHANGES` 但 `required_changes` 为空 → 拒（对齐 review.schema.json 的 if/then）
- `decision` 不在 4 值枚举内 → 拒（防 `needs_human` 偷渡进来）
- `subject_type` 不在 4 值枚举内 → 拒
- `reviewer_role` 走现有 `validate_role_code(allow_reserved=True)`
- `reviews/` 子目录在第一次 write 时自动创建

### 决议 5 · 公开面 delta（ADR-0003 只进不出锁）

下列 4 方法 + 1 dataclass + 2 enum **新增**进公开面。snapshot `tests/test_fcop/snapshots/public_surface.json` 会在 R2 commit 一并更新：

- `Project.write_review`
- `Project.read_review`
- `Project.list_reviews`
- `Project.archive_review`
- `Review` dataclass
- `ReviewDecision` enum
- `ReviewSubjectType` enum

按 ADR-0003 §additive-only：每条都是新符号，没有任何已有签名被改。R3 commit 时同步加 CHANGELOG 条目。

### 决议 6 · v1.0 防御测试（防 v1.2 特性偷渡）

ADR-0017 明确 v1.0 REVIEW **不能**包含：
- `decision: needs_human` 枚举值
- `human_approval` 子对象
- `Project.mark_human_approved` API
- admin-layer manual_file_edit 守卫

新增测试 `tests/test_fcop/test_review_no_v12_features.py` 显式 ASSERT 它们不存在。任何 PR 想满足下游需求偷塞这些（绕过 charter ADR）都会被这个测试拦下。

### 决议 7 · 本任务**不**做的（每个走独立后续任务）

- `Role.layer / can / cannot` 字段 + 4 条 boundary 规则 + `BOUNDARY_VIOLATED` 事件 → **TASK-005**
- `Project.report_failure / recover_session` + `core/recovery.py` + Failure 事件 → **TASK-006**
- `Project.subscribe_events` + polling watcher + 12 个事件类型 → **TASK-007**
- `fcop migrate-workspace` CLI + `docs/agents/` detect+warn + `MIGRATION-1.0.md` → **TASK-008**
- 回 GitHub Issue #2 → **TASK-009**（原 REPORT-003 §6 的种子 4）
- `fcop deploy_rules` 重新 emit 让 mdc 引用新 schema → **TASK-010**
- v1.0.0 RC 打 tag + Zenodo DOI bump → **TASK-011**

REPORT-003 §6 的列表假设了 TASK-004 一锅端；这次收窄之后剩下的全部往后挪一格。

---

## 3 · 验收标准（10 条）

| # | 标准 | 证据 |
|---|---|---|
| A1 | `src/fcop/_data/schemas/` 含 7 份 `spec/schemas/*.schema.json` 的字节级副本 | `test_bundled_schemas_in_sync` |
| A2 | `core/jsonschema_validator.py` 暴露 `validate_envelope_frontmatter` + `validate_record`；import 时加载 7 份 schema；跨 `$ref` 用 `referencing.Registry` 解析 | 手动 import + `test_validator_loads_all` |
| A3 | `tests/test_schemas/test_*.py` × 7，每份 ≥ 3 用例（合法 / 缺必填 / 非法枚举），对齐 ADR-0016 | 文件数 + 每份用例数 |
| A4 | `docs/agents/log/` 下所有真实 0.7.x TASK / REPORT / ISSUE 文件全部通过 ipc-envelope schema（回归 / I5 见证） | `test_legacy_files_validate` |
| A5 | `Review` dataclass + `ReviewDecision` + `ReviewSubjectType` 在 `models.py`，从顶层 `fcop` 包导出 | import 测试 |
| A6 | `core/filename.py` 解析 `REVIEW-{date}-{seq}-{reviewer}-on-{subject}.md` round-trip；`core/frontmatter.py` parse/serialize review frontmatter | `test_core_filename_review` + `test_core_frontmatter_review` |
| A7 | `Project.write_review / read_review / list_reviews / archive_review` 在 temp project 上端到端跑通；`reviews/` 子目录自动创建 | `test_project_reviews` |
| A8 | `decision=needs_changes` 但 `required_changes` 为空 → 拒；`decision=needs_human`（v1.2 推迟值）→ 拒 | `test_project_reviews` + `test_review_no_v12_features` |
| A9 | `tests/test_fcop/snapshots/public_surface.json` 更新含 4 新方法 + 1 dataclass + 2 enum；完整 pytest 通过 | `pytest -q tests/test_fcop/test_public_surface.py` |
| A10 | REPORT-004 + TASK-004 归档 + commit + push，CHANGELOG 加一条 "Unreleased / Added" | `git log` + `CHANGELOG.md` |

---

## 4 · 执行计划（3 commit）

| Round | 交付物 | Commit 信息 |
|---|---|---|
| R1 | 把 schema 同步进 wheel + `core/jsonschema_validator.py` + 7 份 `tests/test_schemas/test_*.py` + 1 份 in-sync 测试 + 1 份 legacy-files 测试 | `feat(core): JSON Schema 校验器 + 7 抽象的测试套件` |
| R2 | `Review` dataclass + 枚举 + filename + frontmatter + 4 个 `Project` 方法 + 测试 + snapshot 更新 + CHANGELOG | `feat(review): REVIEW envelope 落地（ADR-0017 最小面）` |
| R3 | REPORT-004 + TASK-004 归档 + push | `close TASK-20260509-004：schema 校验器 + REVIEW 已发车` |

任何一轮测试第一次没通过 → 修完再 commit。**绝不 commit 红 pytest。**

---

## 5 · 风险登记

| 风险 | 缓解 |
|---|---|
| Schema 打包破坏 wheel build | 用 `src/fcop/_data/schemas/` 简单复制 + hatchling `include` glob（rules `_data/` 已经这么用），不写自定义 hook |
| 0.7.x 文件验证失败 | A4 在 commit 前抓；如果挂了，那是 schema 写错了（I5 禁止破 0.7.x） |
| 测试时 `referencing` 库不可用 | 已经是 `jsonschema>=4.0` 的 transitive dep（TASK-003 R1 / commit 3c35e0e 加的）—— 任务开始前已确认 |
| `Review` dataclass 字段与 `Task.task_id` 风格冲突 | 用 `review_id`（对齐 schema），与 Issue/Task 命名风格一致 |
| 公开面 snapshot diff 太大 | R2 一个 commit 单独更新；CI diff 显示 7 条 net 增加，全是 added 方向 |
| REVIEW 文件 body 与 REPORT body 约定冲突 | 没有冲突——REVIEW body 同其他 envelope 一样是自由 Markdown，rationale 在 frontmatter，body 是补充 |

---

## 6 · 三视角预飞检查

### Proposer（这件事是否让 v1.0 离 ship 更近？）
是。v1.0.0 RC 需要：(a) schema 存在 [TASK-003 已做]，(b) reference impl 按 spec 读写 [本任务起步]，(c) 新 envelope（REVIEW）可发货 [本任务发]。完成 TASK-004，协议**第一次**可端到端使用——而且把原 Issue #2 的头号请求 REVIEW 发出来了。

### Executor（工作是否有界？）
3 个 commit。触及 `src/fcop/_data/schemas/`（新建）、`src/fcop/core/jsonschema_validator.py`（新建）、`src/fcop/models.py`（additive）、`src/fcop/core/filename.py`（additive）、`src/fcop/core/frontmatter.py`（additive）、`src/fcop/project.py`（additive）、`src/fcop/__init__.py`（additive）、`tests/`（仅新文件）。**零删除。** pyproject 已经在 TASK-003 加了 jsonschema 依赖。

### Reviewer（如果是同事提的，我会拒吗？）
需要在执行中盯的拒收条件：
- 任何测试文件 < 3 用例 → 拒
- 任何已有 dataclass 字段类型被改 → 拒（破坏性变更）
- 任何 `validate_*` 调用被接进 `write_task / write_report / write_issue` 路径 → **停下来拆分**（legacy 文件可能挂、回归风险高；那块工作要单开「校验强制化」任务，带 opt-in flag）
- 公开面 snapshot 出现任何 DELETED 或 RENAMED 条目 → 拒

---

## 7 · 签收

```
Sender:    ADMIN
Recipient: ME (solo 模式)
Status:    in_progress
Opened:    2026-05-09
Charter:   ADR-0015 §execution roadmap step 2（reference-impl wiring）
Touches:   src/fcop/（v1.0 reframing 链条上第一个动 src 的任务）
```

立即开始 R1。

---

## 8 · 备注：本任务起恢复中文为主

ADMIN 反馈：之前 TASK-002 / TASK-003 / REPORT-002 / REPORT-003 / ADR-0015..0022 / spec/fcop-runtime-protocol-v1.0.md 大量纯英文，可读性差。

新约定（自本任务起）：
- **内部管理文档**（TASK / REPORT / 草拟 ADR / 草拟 release notes）→ **中文为主**，关键术语带英文括注
- **协议对外文档**（spec / 长文 ADR / README / homepage / getting-started）→ **中英双语并出**
- 已写好的英文文档暂时保留；是否回头补 `.zh.md` 由 ADMIN 单开 TASK 安排（候选：TASK-Z01 文档双语化补齐）

本 charter 已用中文重写覆盖。R2/R3 commit 信息同样中文为主、关键术语带英文。
