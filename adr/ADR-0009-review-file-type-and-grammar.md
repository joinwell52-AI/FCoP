# ADR-0009: REVIEW-* File Type & Filename Grammar

- **Status**: Superseded by [ADR-0017](./ADR-0017-review-file-type-minimal.md)（2026-05-09，同日；砍掉与 ADR-0012/0013 的 needs_human / human_approval 紧耦合，仅保留 v1.0 最小 surface）
- **Date**: 2026-05-09
- **Deciders**: ADMIN（待批准）
- **Related**: [ADR-0007](./ADR-0007-fcop-1.0-protocol-freeze-charter.md)（1.0 charter）；[ADR-0008](./ADR-0008-json-schema-as-machine-readable-spec.md)（review.schema.json）；下游字段：[ADR-0012](./ADR-0012-review-decision-needs-human.md) / [ADR-0013](./ADR-0013-review-human-approval.md)

## Context

FCoP `0.7.2` 仅识别三类协议文件名：TASK / REPORT / ISSUE。CodeFlow §3.4 + Issue #2 都基于"REVIEW 是独立事件"假设——审 TASK / REPORT / role-switch 的 governance 行为应该有自己的文件类型，不该混进 REPORT（worker 自报）的语义里。

REPORT vs REVIEW 的根本切割：

| | REPORT | REVIEW |
|---|---|---|
| 谁写 | worker（"我做完了 / 我卡了 / 我在做"） | governance（"我审过了"） |
| 关键字段 | `status` | `decision` |
| Trigger | TASK 完成 / 阻塞 / 进展 | 对 TASK / REPORT / role-switch 的事后审计 |

不切割 → REPORT 字段语义双重化 → 无法回应 Issue #2 字段 3-4。

## Decision

引入 `REVIEW-*.md` 作为协议正典文件类型（与 TASK / REPORT / ISSUE 并列）。

文件名 grammar：

```
REVIEW-{YYYYMMDD}-{NNN}-{REVIEWER_ROLE}-on-{SUBJECT_REF_SHORT}.md
```

例：`REVIEW-20260601-003-QA-on-TASK-20260601-001.md`

- `REVIEWER_ROLE` 与 fcop.json roles 中合法 role code 一致
- `SUBJECT_REF_SHORT` = 被审对象的核心 ID 段（如 `TASK-20260601-001`）
- 完整 `subject_ref` 在 frontmatter 里（含可选的 sender/recipient 段）

## Design Details

- `core/filename.py` 新增 `_REVIEW_FILENAME_RE` 与 `parse_review_filename()`
- `models.py` 新增 `Review` dataclass：`review_id`, `subject_type` (`task` \| `report` \| `role_switch` \| `code_change`), `subject_ref`, `reviewer_role`, `reviewer_agent`, `decision` (1.0 仅 `approved` \| `rejected` \| `needs_changes` \| `abstained`，1.1 由 ADR-0012 加 `needs_human`), `rationale`, `required_changes`, `decided_at`
- `project.py` 新增 `Project.write_review() / read_review() / list_reviews() / archive_review()`
- `core/frontmatter.py` 新增 `parse_review_frontmatter()` + `assemble_review_file()`
- `docs/agents/reviews/`：默认目录（与 `tasks/` `reports/` `issues/` 平级）；归档目录 `docs/agents/log/reviews/`
- 1.0 阶段 reviews/ 目录可选——只有当至少一个 REVIEW 存在时才创建

## Tests Checklist

- [ ] `tests/test_fcop/test_core_filename.py` 加 REVIEW 文件名正则 5 种 case
- [ ] `tests/test_fcop/test_core_frontmatter.py` 加 review parser 4 种 case
- [ ] `tests/test_fcop/test_project_reviews.py` 新文件：write / read / list / archive 全闭环
- [ ] `tests/test_schemas/test_review_schema.py`（与 ADR-0008）
- [ ] `tests/test_fcop/test_public_surface.py` 快照增加 4 个新公开方法

## Backwards Compatibility

- 加新文件类型、加新方法、加新目录 → 对 0.7.x 用户**完全透明**
- 旧 REPORT / ISSUE 不动；其语义不变
- `Project.write_review()` 是新公开方法，加入 ADR-0003 公开面只进不出锁
- 1.0 起，spec / docs / 教程必须明确 "REVIEW 与 REPORT 的分工"，避免老用户混淆

## Open Questions

1. REVIEW 是否需要 sender/recipient 字段？建议**不需要**——REVIEW 由 reviewer 写，subject_ref 已经表达了"审谁"
2. `decision: 'abstained'` 在 1.0 是否激活？建议激活（避免 1.1 再加一个 enum 值的 minor bump 心智负担）
3. `subject_type: 'role_switch'` 怎么 reference role-switch 文件？建议用文件名作为 ref
4. 是否在 MCP tool surface 新增 `write_review` tool？是（让 Cursor 内直接调）

## Sign-off

待 ADR-0007 charter 通过后，本 ADR 由 ADMIN 直接 sign 进入 Accepted。
