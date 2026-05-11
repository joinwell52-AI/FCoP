---
protocol: fcop
version: 1
sender: ME
recipient: ADMIN
priority: P1
references:
- TASK-20260427-002
status: done
---

# 0.7.0 一条龙交付——Rule 1 角色身份唯一性硬化

## 状态

`status=done`。本任务（TASK-20260427-002）的全部交付物已落盘。0.7.0
窗口正式开启时执行的实现总结见下。配套报告 REPORT-20260427-002 的
`status=in_progress` 是设计完成时的快照，本份是实现完成时的关闭回执。

## 交付清单（与 TASK-002 验收标准逐条对照）

| 验收项 | 落地证据 |
|---|---|
| `fcop_report()` UNBOUND 输出底部含「Role occupancy」段 | `mcp/src/fcop_mcp/server.py` `_compose_session_report` + 新增 `test_fcop_report_renders_role_occupancy_section` / `test_fcop_report_english_role_occupancy_section`（598 passed）|
| `fcop-rules.mdc` Rule 1「贯穿两阶段的硬约束」含「一角色一 agent」条款 | `src/fcop/rules/_data/fcop-rules.mdc`（中英各一份）+ `fcop_rules_version: 1.6.0 → 1.7.0` |
| `fcop-protocol.mdc` UNBOUND 节含 occupancy 自检步骤 + 三选一出口 | `src/fcop/rules/_data/fcop-protocol.mdc` 新 step 4 + `fcop_protocol_version: 1.4.0 → 1.5.0` |
| `letter-to-admin.{zh,en}.md` 含 ADMIN 双 bind 禁令 | 中英两份在「Standard opening lines」后新增「⚠️ 一个角色只能给一个 agent」节 |
| `fcop_protocol_version: 1.4.0 → 1.5.0`、`fcop_rules_version: 1.6.0 → 1.7.0` | 完成 |
| 包版本 0.6.5 → 0.7.0（minor bump） | `src/fcop/_version.py` + `mcp/src/fcop_mcp/_version.py` |
| 587 passed 基线不降 | 598 passed（净 +11；含 7 occupancy + 2 fcop_report 渲染 + 1 别名移除 + 3 seq 回归）|

零新工具，全靠现有 `fcop_report` occupancy + Rule 8 拒绝权 +
`.fcop/proposals/` 三件套——与 TASK-002 「0 个新工具」承诺一致。

## 实现的关键代码动作

- `src/fcop/models.py`：新 `RoleOccupancy` dataclass（status =
  UNUSED / ARCHIVED / ACTIVE，open & archived 计数，last_session_id，
  last_seen_at）。
- `src/fcop/project.py`：新 `Project.role_occupancy()` 方法 +
  `_parse_dir_files` / `_roles_in_parsed` / `_build_role_occupancy` /
  `_try_read_session_id` / `_RESERVED_ROLES` 五件助手。从磁盘账本
  推导，frontmatter-only 读取，UNBOUND 安全调用。
- `mcp/src/fcop_mcp/server.py`：`_compose_session_report` UNBOUND
  分支增加 Role occupancy 表 + 四行解读说明 + Rule 1 拒绝行为提示。
- 同时把 0.6.3 弃用的 `unbound_report()` 别名移除（ADR-0003
  允许 minor 边界破坏）—— 是"快进版本"时的清理动作。

## 与设计的偏差

零偏差。TASK-002 的修订清单逐项落地。设计阶段"0 个新工具、不引入
runtime lock、不改 frontmatter、不改 init_*"四条范围线全守住。

## 验证

```
.venv/Scripts/python.exe -m pytest tests/ -q
# 598 passed, 1 warning in 4.87s

.venv/Scripts/python.exe -m ruff check src mcp tests
# All checks passed!
```

## References

- 任务单：`TASK-20260427-002-ADMIN-to-ME.md`
- 配套 issue：`ISSUE-20260427-002-ME.md` (status=closed)
- 配套姊妹任务：`TASK-20260427-003-ADMIN-to-ME.md`（seq 修复）
- 发版说明：`docs/releases/0.7.0.md`
- 上游审查链路：REPORT-20260427-002（in_progress 设计快照）
