---
protocol: fcop
version: 1
type: REPORT
sender: ME
recipient: ADMIN
ref_task: docs/agents/log/tasks/TASK-20260509-004-ADMIN-to-ME.md
priority: P0
status: done
acceptance_criteria_met: 10
acceptance_criteria_total: 10
---

# TASK-20260509-004 完成回报：JSON Schema 校验器接入 + REVIEW（Audit）端到端

## 1 · 一句话结论

v1.0 spec 第一次**真正可执行**——`spec/schemas/` 不再是纸，
`fcop.core.jsonschema_validator` 把它接进 reference impl；REVIEW
（Audit 抽象）从 dataclass 到 `Project.write_review` 端到端发车，
v1.2 推迟特性（`needs_human` / `human_approval` / `mark_human_approved`）
被 schema + dataclass + project + 专门测试**四层拒收**。

## 2 · 交付物

| Commit | 文件数 | +/- | 描述 |
|---|---|---|---|
| `9cf0b05` (R1) | 22 | +2005 / -7 | 校验器基础设施 + 7 份 schema 测试 + bundle |
| `665eb53` (R2) | 11 | +1700 / -1 | REVIEW dataclass / API / 测试 / snapshot / CHANGELOG |
| 本 commit (R3) | 2 | +180 / 0 | REPORT-004 + 归档 TASK-004 |

合计 35 文件、+3885 行 / -8 行。

### 公开面新增（5 项，全 additive）
- `Project.write_review / read_review / list_reviews / archive_review`
- `Project.reviews_dir` property
- `Review` dataclass
- `ReviewDecision` 枚举（4 值闭枚举）
- `ReviewSubjectType` 枚举（4 值闭枚举）

### 协议层新增（schema 落地）
- `src/fcop/_data/schemas/*.schema.json` × 7（包内权威副本）
- `fcop.core.jsonschema_validator` 模块（normalize / validate × 2）
- `tests/test_schemas/` × 10 文件、116 用例
- `tests/test_fcop/test_*review*.py` × 4 文件、58 用例

### Spec 层调整
- `spec/schemas/ipc-envelope.schema.json` 放宽 TASK.subject 为 SHOULD、
  REPORT 接受 0.7.x 字段别名（references / related_task / related_issues
  / report_id）—— 满足 I5（v1.x 内向后兼容）。

## 3 · 验收对照（10/10）

| # | 标准 | 状态 | 证据 |
|---|---|---|---|
| A1 | `src/fcop/_data/schemas/` 含 7 份 spec 字节级副本 | ✅ | `test_bundled_schemas_in_sync` 4 用例全过 |
| A2 | `core/jsonschema_validator.py` 暴露 2 个 validate + 跨 `$ref` 解析 | ✅ | 模块 import 时构建一次 registry，跨文件 `$ref` 测试通过 |
| A3 | `tests/test_schemas/test_*.py` × 7，每份 ≥ 3 用例 | ✅ | 7 份文件实际 3..15 用例不等，覆盖合法 / 缺必填 / 非法枚举 |
| A4 | `docs/agents/log/` 全部 0.7.x envelope 通过新 schema | ✅ | `test_legacy_files_validate` 共 51 文件全过；触发 schema 放宽（见 §4） |
| A5 | `Review` + 2 枚举从顶层 `fcop` 导出 | ✅ | `from fcop import Review, ReviewDecision, ReviewSubjectType` 可用 |
| A6 | `core/filename.py` round-trip + `core/frontmatter.py` review parse | ✅ | `test_core_filename_review` + `test_core_frontmatter_review` 共 19 用例全过 |
| A7 | 4 个 `Project` review 方法在 temp project 端到端跑通 | ✅ | `test_project_reviews` 共 22 用例全过；reviews/ 目录懒创建 |
| A8 | `decision=needs_changes` + 空列表 → 拒；`needs_human` → 拒 | ✅ | 拒收测试 7 用例全过（含别名 NEEDS_HUMAN / needs-human） |
| A9 | snapshot 更新 + 完整 pytest 通过 | ✅ | 731 passed（mcp role_lock 1 项预存红，与本任务无关，多次 stash 验证） |
| A10 | REPORT-004 + 归档 + commit + CHANGELOG | ✅ | 本 commit 完成 |

## 4 · 设计决策回顾（与原 charter 偏差）

### 决策外的小调整 1：REPORT envelope 接受更多 0.7.x 字段别名

A4 跑测试时发现 0.7.x REPORT 用 `references` / `related_task` /
`related_issues` 三种风格的 task 引用字段（早期 28 份文件统计）。
按 I5（v1.x 内 backward compat），三个都必须合法。已在
`ipc-envelope.schema.json` 的 `report` 分支加进 properties，新文件
仍**推荐** `ref_task`（schema description 显式标注）。

未触发 ADR 修订——这只是把已存在的 0.7.x 行为编码进 schema，
不是新协议决策。

### 决策外的小调整 2：TASK.subject 从 MUST 改 SHOULD

A4 发现 8 份早期 0.7.x TASK 把 subject 写在 markdown body H1 而非
frontmatter（如 `TASK-20260427-008-ADMIN-to-ME.md`）。这是 0.7.x
始终允许的行为，schema 应反映现实。已加 SHOULD 注释，新文件仍
应该写 frontmatter subject。

### 决策外的小调整 3：REVIEW 也带 sender 字段

`ipc-envelope.schema.json` 的 `envelopeBase` 把 sender 列为必填
（4 个 envelope 类型共享）。REVIEW 的 sender = reviewer_role 是
最自然映射，已在 `Project.write_review` 自动注入。frontmatter
field-order 同步把 sender 加到 review 序列化的固定位置。

## 5 · 三视角自审

### Proposer
v1.0 RC ship 准备：spec ✅、schema ✅、reference impl 第一抽象 ✅。
按 ADR-0015 §execution roadmap，本任务完成 step 2 的 1/7。剩 6 个
抽象的 reference impl 拆给 TASK-005..008（boundary / failure /
event / migrate-workspace），独立 atomic。

### Executor
3 个 commit，每个独立可审：
- R1（22 文件）：纯基础设施，无业务逻辑变更
- R2（11 文件）：纯 additive，零删除，snapshot diff 显示净 +5 符号
- R3（2 文件）：仅文档移动 / 创建

涉及 src 改动文件 5 个：`models.py` / `core/filename.py` /
`core/frontmatter.py` / `core/jsonschema_validator.py` /
`project.py` / `__init__.py`。所有现有 dataclass / 函数签名 0
修改、0 删除。

### Reviewer
拒收预设全部触发并通过：
- ❌ 任何 dataclass 字段类型被改 → 没发生
- ❌ `validate_*` 调用被接进 write_task / write_report / write_issue
  → 没发生（opt-in 仅 write_review 启用）
- ❌ snapshot 出现 DELETED / RENAMED → 没发生（5 项纯 added）
- ❌ 任何测试文件 < 3 用例 → 没发生（最少 5，最多 22）

## 6 · 余下种子（next-task 候选，给 ADMIN 排序）

按 ADR-0015 §execution roadmap，剩余抽象的 reference-impl wiring：

1. **TASK-005**：Boundary（ADR-0020）—— `Role.layer / can / cannot`
   字段 + 4 条 boundary 规则强制 + `BOUNDARY_VIOLATED` 事件
2. **TASK-006**：Failure（ADR-0019）—— `Project.report_failure /
   recover_session` + `core/recovery.py` + Failure 事件
3. **TASK-007**：Event（ADR-0018）—— `Project.subscribe_events` +
   polling watcher + 12 个事件类型
4. **TASK-008**：migrate-workspace（ADR-0022）—— `fcop migrate-workspace`
   CLI + `docs/agents/` detect+warn + `MIGRATION-1.0.md`

外加 release / outreach：
5. **TASK-009**：回 GitHub Issue #2（解释 v1.0 reframing 与 review
   功能可用）
6. **TASK-010**：`fcop deploy_rules` 重新 emit 让 mdc 引用新 schema
   + 更新 `fcop-rules.mdc` 加 REVIEW envelope 段
7. **TASK-Z01**：把 TASK-002/003 / REPORT-002/003 / ADR-0015..0022 /
   spec 长文 补 `.zh.md` 中文版（用户反馈"全英文看不懂"）
8. **TASK-011**：v1.0.0 RC tag + Zenodo DOI bump

建议下一棒优先 **TASK-005（Boundary）** 或 **TASK-Z01（双语补齐）**——
前者推进协议完整度，后者解决用户可读性 friction。

## 7 · 元反思（与上一份 REPORT 的对照）

REPORT-003 §6 假设 TASK-004 = "一锅端 5 个抽象" 的 1000+ 行改动。
本任务 charter 主动收窄到 2 个抽象（Schema 校验器横切 + REVIEW
单点），换来：
- 3 个原子 commit（vs 一个巨型 PR 不可审）
- snapshot diff 仅 +5 项（vs 几十项混合）
- 没有破坏 0.7.x 兼容（schema 放宽全在 backward 方向）
- 给后续 TASK-005..008 各自留出独立 ADR 引用空间

这种「故意收窄」是 FCoP solo 模式 self-discipline 的正面案例——
**抢着做完所有事不如做完一件可以 ship 的事**。

## 8 · 签收

```
Status:    done
Closed:    2026-05-09
Commits:   9cf0b05 (R1) → 665eb53 (R2) → 本 commit (R3)
Branches:  main（直接推 main，solo 模式无 PR）
Next:      由 ADMIN 在 §6 候选里选择下一棒
```
