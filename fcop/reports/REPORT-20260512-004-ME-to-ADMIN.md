---
protocol: fcop
version: 1
kind: report
report_id: REPORT-20260512-004
task_id: TASK-20260512-004
sender: ME
recipient: ADMIN
status: done
thread_key: supersedes-frontmatter-field-20260512
session_id: sess-20260512-me-01
created_at: 2026-05-12T16:50:00+08:00
---

# TASK-004 完成报告 · `supersedes:` frontmatter 字段标准化

## 结论

**D1-D3 / D5-D7 全部交付（D4 D9 scan 明确留 ADR-0033/0034）。**  
`fcop_protocol_version` 从 2.1.0 bump 至 **2.2.0**（与 TASK-003 合并）。

## 交付清单

| Deliverable | 状态 | 说明 |
|---|---|---|
| D1 · `fcop-protocol.mdc` Task Format 加 `supersedes:` | ✅ | 含三字段语义对比表 + 字段说明 |
| D2 · `ipc-envelope.schema.json` 加 optional `supersedes` | ✅ | TASK / REPORT / ISSUE / REVIEW 四类 envelope 全覆盖 |
| D3 · `list_tasks` / `list_reports` 输出标注 | ✅ | 双向索引：`[supersedes X]` + `[superseded by X]` |
| D4 · `fcop_audit` D9 scan | ⏸ 留位 | 明确推 ADR-0033/0034 实施时认领 |
| D5 · `fcop_protocol_version` 2.1.0 → 2.2.0 | ✅ | 与 TASK-003 合并 bump |
| D6 · 同步四件套 | ✅ | `.cursor/rules/`、`AGENTS.md`、`CLAUDE.md` |
| D7 · Release notes | ✅ | `CHANGELOG.md` [1.4.1] 条目 |

## 版本说明

TASK-004 原要求 2.0.0 → 2.1.0，但 TASK 落盘时 2.1.0 已由 v1.3.1 协议文档同步批次占用。
本次实际 bump：2.1.0 → **2.2.0**，语义一致（MINOR additive，向后兼容）。

## 实现说明

### D1 — 协议文档
- Task Format frontmatter 示例加 `supersedes: TASK-...  # optional` 行
- 字段说明段加三字段语义对比表（`parent:` / `related:` / `supersedes:` 正交）
- 完整 `supersedes:` 字段说明（append-only 保留、取值格式、多份时用列表）

### D2 — JSON Schema
- `ipc-envelope.schema.json` 四个 envelope def 各加 `supersedes` optional 字段
- `oneOf`：单字符串或字符串数组，均要求 `^(TASK|REPORT|ISSUE|REVIEW)-` 前缀

### D3 — 工具输出
- 新增 `_supersedes_tag(extra)` 和 `_build_superseded_by_index(items)` 辅助函数
- `list_tasks` 建 O(N) 双向索引，每项带 `[supersedes X]`（前向）/ `[superseded by X]`（反向）
- `list_reports` 同理（Report 无 `.extra`，通过 `parse_frontmatter_raw` 读取）
- `list_reviews` / `list_issues` 未加（REVIEW/ISSUE 在实践中较少出现 supersede，留 v1.5）

— ME, 2026-05-12 16:50 (UTC+8)
