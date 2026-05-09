# ADR-0017: REVIEW File Type — Minimal v1.0 Surface

- **Status**: Proposed
- **Date**: 2026-05-09
- **Deciders**: ADMIN（待批准）
- **Supersedes**: [ADR-0009](./ADR-0009-review-file-type-and-grammar.md)（含 needs_human / human_approval 紧耦合的版本）
- **Related**: [ADR-0015](./ADR-0015-fcop-1.0-ai-os-protocol-charter.md) §抽象 7 Audit；[ADR-0016](./ADR-0016-json-schema-for-7-abstractions.md)

## Context

ADR-0009 把 REVIEW 引入并立刻定义了 `decision: needs_human` + `human_approval` 子结构 + admin layer 校验 + manual_file_edit 防 backdoor 等等——这是**膨胀方向**，外部反馈说"Review 正在变成神角色"。

ADR-0015 charter 决议 2（min_kernel）+ Non-Goals 明确：v1.0 REVIEW 只做最小 surface；needs_human / human_approval 推 v1.2+；mark_human_approved API 推 v1.2+。

REVIEW 与 REPORT 的根本切割（保留 ADR-0009 的核心洞察）：

| | REPORT | REVIEW |
|---|---|---|
| 谁写 | worker（自报） | governance（外审） |
| 关键字段 | `status` | `decision` |
| Trigger | TASK 完成 / 阻塞 / 进展 | 对 TASK / REPORT / role-switch 的事后审计 |

## Decision

引入 `REVIEW-*.md` 作为协议正典文件类型（与 TASK / REPORT / ISSUE 并列），**仅 minimal surface**：

```
REVIEW-{YYYYMMDD}-{NNN}-{REVIEWER_ROLE}-on-{SUBJECT_REF_SHORT}.md
```

`decision` enum 仅 4 值：`approved` | `rejected` | `needs_changes` | `abstained`。

**v1.0 不含**：
- `needs_human` enum 值（推 v1.2，由后续 ADR）
- `human_approval` 子结构（推 v1.2）
- `Project.mark_human_approved()` API（推 v1.2）
- admin layer 校验、manual_file_edit 防 backdoor 等 enforce（推 v1.2）

## Design Details

- `core/filename.py` 新增 `_REVIEW_FILENAME_RE` + `parse_review_filename()`
- `models.py` 新增 `Review` dataclass：`review_id`, `subject_type` (`task` | `report` | `role_switch` | `code_change`), `subject_ref`, `reviewer_role`, `reviewer_agent`, `decision` (4 值), `rationale`, `required_changes`, `decided_at`
- `project.py` 新增 `Project.write_review() / read_review() / list_reviews() / archive_review()` 共 4 个公开 API
- `core/frontmatter.py` 新增 `parse_review_frontmatter()` + `assemble_review_file()`
- `docs/agents/reviews/` 默认目录；归档目录 `docs/agents/log/reviews/`
- 1.0 阶段 reviews/ 可选——仅当至少一个 REVIEW 存在时创建

## Tests Checklist

- [ ] `tests/test_fcop/test_core_filename.py` 加 REVIEW 文件名正则 5 种 case
- [ ] `tests/test_fcop/test_core_frontmatter.py` 加 review parser 4 种 case
- [ ] `tests/test_fcop/test_project_reviews.py` 新文件：write/read/list/archive 全闭环
- [ ] `tests/test_schemas/test_review_schema.py`（与 ADR-0016）
- [ ] `tests/test_fcop/test_public_surface.py` 快照增加 4 个新公开方法
- [ ] `tests/test_fcop/test_review_no_human_approval.py` 显式 enforce v1.0 不含 needs_human / human_approval（防止下游 PR 滑入）

## Backwards Compatibility

- 加新文件类型、加新方法、加新目录 → 对 0.7.x 用户**完全透明**
- 旧 REPORT / ISSUE 不动；其语义不变
- 4 个新公开 API 进 ADR-0003 公开面只进不出锁
- v1.0 reviews 文件 v1.2 加 needs_human 时仍合法（v1.2 是 superset）

## Open Questions

1. `decision: 'abstained'` 在 v1.0 是否激活？**建议激活**（避免 v1.2 加一个 enum 值的额外认知负担）
2. REVIEW 是否需要 sender/recipient？建议**不需要**——subject_ref 已表达"审谁"
3. `subject_type: 'role_switch'` 怎么 reference？建议用文件名作为 ref
4. MCP tool surface 是否新增 `write_review` tool？是（让 Cursor 内直接调）

## Sign-off

待 ADR-0015 charter 通过后，本 ADR 由 ADMIN 直接 sign 进入 Accepted。
