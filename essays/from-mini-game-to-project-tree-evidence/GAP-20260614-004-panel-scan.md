---
protocol: fcop
version: "1"
kind: eval
eval_type: gap
scope: internal
visibility: admin_only
public_candidate: false
sender: SYSTEM
recipient: ADMIN
producer: EVAL-01
reviewed_by: null
task_id: MANUAL-EVAL-1781412524758
thread_key: null
source_report: null
subject: "[EVAL] 面板扫描 · 2026-06-14"
severity: medium
status: draft
target_repo: null
created_at: 2026-06-14T04:48:44.857Z
assets_analyzed:
  - ledger
  - runtime
  - thinking
  - usage
  - analytics
  - eval
  - emergence-log
  - views
  - shared
promotion:
  status: none
  action: null
  target_type: null
  target_file: null
  target_repo: null
  target_url: null
  admin_approved: false
  promoted_by: null
  promoted_at: null
  verified_at: null
---

> **Evidence archive copy / 证据存档副本**
>
> 本文件自 CodeFlowMu 狗食现场 `fcop/internal/eval/` **按原文归档**至随笔证据目录，
> 供读者核对第 17 篇随笔中的 EVAL 观察。原路径见 frontmatter 与正文；
> 发布前已保留原 `INTERNAL ONLY` 声明。
>
> Archived verbatim from CodeFlowMu dogfood `fcop/internal/eval/` for essay 17 verification.

> ⚠️ **INTERNAL ONLY · 内部档案 · DO NOT EXTERNALIZE WITHOUT REVIEW**
>
> 本文件位于 `fcop/internal/eval/`，仅供 ADMIN 审阅。对外发布前须脱敏与改写。


# CodeFlowMu · EVAL 观察（panel-scan）

| 字段 | 值 |
|---|---|
| 观察日期 | 2026-06-14 |
| 触发 | doorbell |
| 关联 TASK | MANUAL-EVAL-1781412524758 |
| 模板 | codeflowmu-eval-assets-promotion-merged §5 |

---

## 1. 结论

扫描 9 类资产后发现 5 条待跟进项（P0=0 P1=4）。

## 受控涌现观察

**总分类**: `controlled_emergence` · skill `controlled-emergence-observer`

| 是否发现涌现 | 类型 | 关联对象 | 来源 | sandbox/probe | 正式 lifecycle | 污染看板 | 建议 emergence-log | 建议动作 |
|---|---|---|---|---|---|---|---|---|
| 是 | controlled_emergence | `TASK-20260612-023` | MCP-PROBE runner | 是 | 是 | 否 | 是 | 记录 emergence-log；probe 任务勿当业务验收 |
| 是 | controlled_emergence | `TASK-20260612-024` | MCP-PROBE runner | 是 | 是 | 否 | 是 | 记录 emergence-log；probe 任务勿当业务验收 |

**sandbox 上下文**: `fcop/_sandbox/mcp-tool-probe/`


## 项目树涌现观察

是否发现：是
类型：project_tree_emergence
整体成熟度：protocol_candidate
反模式数量：26

根任务：TASK-20260613-020
阶段任务：TASK-20260614-004
执行任务：TASK-20260614-005, TASK-20260614-006, TASK-20260614-007, TASK-20260614-008
模式：主线任务 -> 阶段任务 -> 执行任务
观察键：project-tree:TASK-20260613-020:TASK-20260614-004
观察状态：new
成熟度：stable
意图一致性：aligned（phase intent is supported by subject text, but some edges are inferred from references）
时序：2026-06-14T04:38:58.000Z → 2026-06-14T04:39:04.000Z（expanding_role_fanout）
因果链：TASK-20260613-020 -> TASK-20260614-004；TASK-20260614-004 -> TASK-20260614-005；TASK-20260614-004 -> TASK-20260614-006；TASK-20260614-004 -> TASK-20260614-007；TASK-20260614-004 -> TASK-20260614-008
价值：FCoP 从任务流管理中涌现出产品演进树与项目管理能力。
价值证据：mixed_with_coordination_cost；完成率=1；blocked=3
风险：若 PM 无意设置 parent/thread_key，独立 Phase 可能被挂到旧主线，造成 archive 被 CHILD_TASKS_OPEN 拦截。
预测风险：inferred_phase_parent/medium, inferred_execution_parent/medium
置信度：medium（75）
替代解释：The hierarchy may be an accidental reuse of thread_key/references rather than an intentional product phase.
协议吸收：prepare_absorption → panel_capability, pm_creation_prompt, skill_schema
建议动作：
1. 写入 emergence-log
2. Panel 显示 Project / Phase / Execution 三层结构
3. PM 创建 Phase 时提示：继续当前主线 or 新建独立 thread

根任务：TASK-20260614-004
阶段任务：TASK-20260614-007
执行任务：TASK-20260614-008
模式：主线任务 -> 阶段任务 -> 执行任务
观察键：project-tree:TASK-20260614-004:TASK-20260614-007
观察状态：new
成熟度：protocol_candidate
意图一致性：aligned（phase intent is supported by subject text, but some edges are inferred from references）
时序：2026-06-14T04:38:58.000Z → 2026-06-14T04:38:58.000Z（early_tree_formation）
因果链：TASK-20260614-004 -> TASK-20260614-007；TASK-20260614-007 -> TASK-20260614-008
价值：FCoP 从任务流管理中涌现出产品演进树与项目管理能力。
价值证据：benefit_supported；完成率=1；blocked=0
风险：若 PM 无意设置 parent/thread_key，独立 Phase 可能被挂到旧主线，造成 archive 被 CHILD_TASKS_OPEN 拦截。
预测风险：inferred_phase_parent/medium, inferred_execution_parent/medium
置信度：medium（75）
替代解释：The hierarchy may be an accidental reuse of thread_key/references rather than an intentional product phase.
协议吸收：prepare_absorption → panel_capability, pm_creation_prompt, skill_schema, adr_or_fcop_protocol_candidate
建议动作：
1. 写入 emergence-log
2. Panel 显示 Project / Phase / Execution 三层结构
3. PM 创建 Phase 时提示：继续当前主线 or 新建独立 thread

根任务：TASK-20260614-004
阶段任务：TASK-20260614-008
执行任务：TASK-20260614-009
模式：主线任务 -> 阶段任务 -> 执行任务
观察键：project-tree:TASK-20260614-004:TASK-20260614-008
观察状态：new
成熟度：protocol_candidate
意图一致性：aligned（phase intent is supported by subject text, but some edges are inferred from references）
时序：2026-06-14T04:38:58.000Z → 2026-06-14T04:38:58.000Z（early_tree_formation）
因果链：TASK-20260614-004 -> TASK-20260614-008；TASK-20260614-008 -> TASK-20260614-009
价值：FCoP 从任务流管理中涌现出产品演进树与项目管理能力。
价值证据：benefit_supported；完成率=1；blocked=0
风险：若 PM 无意设置 parent/thread_key，独立 Phase 可能被挂到旧主线，造成 archive 被 CHILD_TASKS_OPEN 拦截。
预测风险：inferred_phase_parent/medium, inferred_execution_parent/medium
置信度：medium（75）
替代解释：The hierarchy may be an accidental reuse of thread_key/references rather than an intentional product phase.
协议吸收：prepare_absorption → panel_capability, pm_creation_prompt, skill_schema, adr_or_fcop_protocol_candidate
建议动作：
1. 写入 emergence-log
2. Panel 显示 Project / Phase / Execution 三层结构
3. PM 创建 Phase 时提示：继续当前主线 or 新建独立 thread

根任务：TASK-20260612-101
阶段任务：TASK-20260613-001
执行任务：TASK-20260613-004, TASK-20260613-005, TASK-20260613-006
模式：主线任务 -> 阶段任务 -> 执行任务
观察键：project-tree:TASK-20260612-101:TASK-20260613-001
观察状态：new
成熟度：stable
意图一致性：ambiguous（hierarchy is inferred from references without an explicit phase marker）
时序：2026-06-12T17:21:57.000Z → 2026-06-12T17:47:51.000Z（expanding_role_fanout）
因果链：TASK-20260612-101 -> TASK-20260613-001；TASK-20260613-001 -> TASK-20260613-004；TASK-20260613-001 -> TASK-20260613-005；TASK-20260613-001 -> TASK-20260613-006
价值：FCoP 从任务流管理中涌现出产品演进树与项目管理能力。
价值证据：mixed_with_coordination_cost；完成率=1；blocked=1
风险：若 PM 无意设置 parent/thread_key，独立 Phase 可能被挂到旧主线，造成 archive 被 CHILD_TASKS_OPEN 拦截。
预测风险：inferred_phase_parent/medium, inferred_execution_parent/medium
置信度：medium（75）
替代解释：The hierarchy may be an accidental reuse of thread_key/references rather than an intentional product phase.
协议吸收：prepare_absorption → panel_capability, pm_creation_prompt, skill_schema
建议动作：
1. 写入 emergence-log
2. Panel 显示 Project / Phase / Execution 三层结构
3. PM 创建 Phase 时提示：继续当前主线 or 新建独立 thread

### 项目树反模式
- orphan_parent (medium)：TASK-20260609-006；parent TASK-20260609-012 does not exist
- orphan_parent (medium)：TASK-20260609-007；parent TASK-20260609-012 does not exist
- orphan_parent (medium)：TASK-20260609-008；parent TASK-20260609-012 does not exist
- orphan_parent (medium)：TASK-20260609-010；parent TASK-20260609-013 does not exist
- orphan_parent (medium)：TASK-20260612-001；parent TASK-20260611-102 does not exist
- orphan_parent (medium)：TASK-20260612-002；parent TASK-20260611-104 does not exist
- child_created_before_parent (medium)：TASK-20260613-001；child=2026-06-13T01:47:37+08:00, parent=2026-06-13T01:47:51+08:00
- child_created_before_parent (medium)：TASK-20260613-002；child=2026-06-13T01:34:43+08:00, parent=2026-06-13T01:47:51+08:00
- child_created_before_parent (medium)：TASK-20260613-003；child=2026-06-13T01:47:28+08:00, parent=2026-06-13T01:47:51+08:00
- child_created_before_parent (medium)：TASK-20260613-004；child=2026-06-13T01:21:57+08:00, parent=2026-06-13T01:47:37+08:00
- child_created_before_parent (medium)：TASK-20260613-005；child=2026-06-13T01:34:27+08:00, parent=2026-06-13T01:47:37+08:00
- child_created_before_parent (medium)：TASK-20260613-006；child=2026-06-13T01:22:02+08:00, parent=2026-06-13T01:47:37+08:00
- child_created_before_parent (medium)：TASK-20260613-008；child=2026-06-13T20:17:23+08:00, parent=2026-06-13T21:05:25+08:00
- child_created_before_parent (medium)：TASK-20260613-009；child=2026-06-13T20:17:20+08:00, parent=2026-06-13T21:05:25+08:00
- child_created_before_parent (medium)：TASK-20260613-010；child=2026-06-13T20:17:16+08:00, parent=2026-06-13T21:05:25+08:00
- child_created_before_parent (medium)：TASK-20260613-011；child=2026-06-14T12:38:58+08:00, parent=2026-06-14T12:39:04+08:00
- child_created_before_parent (medium)：TASK-20260613-012；child=2026-06-14T12:38:58+08:00, parent=2026-06-14T12:39:04+08:00
- child_created_before_parent (medium)：TASK-20260613-013；child=2026-06-14T12:38:58+08:00, parent=2026-06-14T12:39:04+08:00
- child_created_before_parent (medium)：TASK-20260614-001；child=2026-06-14T12:38:58+08:00, parent=2026-06-14T12:39:04+08:00
- child_created_before_parent (medium)：TASK-20260614-002；child=2026-06-14T12:38:58+08:00, parent=2026-06-14T12:39:04+08:00
- child_created_before_parent (medium)：TASK-20260614-003；child=2026-06-14T12:38:58+08:00, parent=2026-06-14T12:39:04+08:00
- child_created_before_parent (medium)：TASK-20260614-004；child=2026-06-14T12:38:58+08:00, parent=2026-06-14T12:39:04+08:00
- multiple_admin_roots_same_thread (medium)：TASK-20260609-014；panel-task-014: TASK-20260609-014, TASK-20260611-014
- multiple_admin_roots_same_thread (medium)：TASK-20260609-020；panel-task-020: TASK-20260609-020, TASK-20260613-020, TASK-20260614-004
- multiple_admin_roots_same_thread (medium)：TASK-20260611-100；panel-task-100: TASK-20260611-100, TASK-20260612-100
- multiple_admin_roots_same_thread (medium)：TASK-20260611-101；panel-task-101: TASK-20260611-101, TASK-20260612-101

## 2. 九类资产分析矩阵

| 资产 | 状态 | 关键发现 | 风险/价值 | 证据 |
|---|---|---|---|---|
| 账本（ledger / tasks.jsonl / views） | scanned | lifecycle inbox=1 active=0 review=0 done=1 archive=68 | 用于判断任务流是否堆积或断链 | `fcop/_lifecycle/` |
| 运行日志（fcop/logs/runtime） | scanned | 17 个 jsonl | 提供运行/用量/统计证据 | `fcop/logs/runtime/` |
| 思考流（fcop/logs/thinking） | thin | 0 个 jsonl | P2：缺少思考流样本，难以复盘 Agent 判断质量 | `fcop/logs/thinking/` |
| 用量（fcop/logs/usage） | scanned | 6 个 jsonl | 提供运行/用量/统计证据 | `fcop/logs/usage/` |
| 统计（fcop/logs/analytics） | scanned | 6 个 jsonl | 提供运行/用量/统计证据 | `fcop/logs/analytics/` |
| 内部 eval（fcop/internal/eval） | scanned | 106 份 eval markdown | 可用于趋势复盘，但需避免重复浅层观察 | `fcop/internal/eval/` |
| 涌现日志（fcop/internal/emergence-log.md） | scanned | 存在 | 可承接模式级观察 | `fcop/internal/emergence-log.md` |
| 角色视图（fcop/ledger/views） | drift | 4 个 todo view；4 个疑似滞后；tasks.jsonl=70 行 | P1：ADMIN/PM 视图可能低估待办 | `fcop/ledger/views/`, `fcop/ledger/tasks.jsonl` |
| 共享知识（fcop/shared） | scanned | 团队共享文档存在 | 可校验角色与团队约束 | `fcop/shared/` |

## 3. 跨资产一致性分析

- ledger tasks.jsonl 有 70 行，但 4 个角色 todo view 显示空待办，说明 ledger source 与 view projection 可能不同步。

## 4. 根因假设

- H1：LedgerBuilder 或视图刷新触发点没有覆盖当前写入路径，导致角色 todo view 落后于 tasks.jsonl。

## 5. 影响面与置信度

| 影响面 | 判断 | 说明 |
|---|---|---|
| ADMIN 决策 | 高 | 角色视图滞后会直接误导 ADMIN 对待办/卡顿的判断。 |
| PM 派发/验收 | 高 | PM 可能基于空 todo 视图漏掉需要催办或验收的任务。 |
| DEV/OPS/QA 执行 | 中 | DEV/OPS/QA 的下一步依赖 PM 是否把观察拆成明确 TASK。 |
| 公开 Issue 价值 | 低 | 当前证据含内部路径和 ledger 状态，公开前需要脱敏与复现脚本。 |

| 项 | 置信度 | 原因 |
|---|---|---|
| 资产覆盖 | high | 9 类资产均进入扫描并写入矩阵。 |
| 问题定位 | medium | 可定位到 ledger/views 投影不一致，但仍需代码级复现确认触发点。 |
| 晋升建议 | medium | 已有待跟进项，可转本地任务。 |

## 6. 证据

- - `fcop/_lifecycle/`：inbox=1 active=0 review=0 done=1 archive=68
- - `fcop/tasks/`（0002 支线）：0 个 TASK 文件
- - `fcop/ledger/tasks.jsonl`：70 行
- - `fcop/ledger/views/`：4 个 *.todo.md
- - `fcop/logs/runtime/`：17 个 jsonl
- - `fcop/logs/thinking/`：0 个 jsonl
- - `fcop/logs/usage/`：6 个 jsonl
- - `fcop/logs/analytics/`：6 个 jsonl
- - `fcop/internal/eval/`：106 份报告
- - `fcop/internal/emergence-log.md`：存在
- - `fcop/shared/`：存在
- - `.cursor/rules/fcop-rules.mdc`：rules 3.2.5

## 7. 发现问题

- P1：`fcop/ledger/views/DEV.todo.md` 显示「暂无任务」但 tasks.jsonl 非空（views 滞后）
- P1：`fcop/ledger/views/OPS.todo.md` 显示「暂无任务」但 tasks.jsonl 非空（views 滞后）
- P1：`fcop/ledger/views/PM.todo.md` 显示「暂无任务」但 tasks.jsonl 非空（views 滞后）
- P1：`fcop/ledger/views/QA.todo.md` 显示「暂无任务」但 tasks.jsonl 非空（views 滞后）
- P2：本次为面板/定时触发，无单一 TASK 正文快照（已做全库扫描）

## 8. 优先级

| 优先级 | 项 | 原因 |
|---|---|---|
| P0 | — | — |
| P1 | `fcop/ledger/views/DEV.todo.md` 显示「暂无任务」但 tasks.jsonl 非空（views 滞后） | 应修复 |
| P1 | `fcop/ledger/views/OPS.todo.md` 显示「暂无任务」但 tasks.jsonl 非空（views 滞后） | 应修复 |
| P1 | `fcop/ledger/views/PM.todo.md` 显示「暂无任务」但 tasks.jsonl 非空（views 滞后） | 应修复 |
| P1 | `fcop/ledger/views/QA.todo.md` 显示「暂无任务」但 tasks.jsonl 非空（views 滞后） | 应修复 |
| P2 | P2：本次为面板/定时触发，无单一 TASK 正文快照（已做全库扫描） | 改进 |

## 9. 建议动作

- CodeFlowMu 本地修复：Panel「转为本地任务」→ inbox TASK-ADMIN-to-PM
- CodeFlowMu Issue：产品/宿主缺陷且可公开时 → issue-drafts/CODEFLOWMU-*
- FCoP Issue：协议或 MCP 工具问题时 → issue-drafts/FCOP-*

## 10. 验证计划

- 重建 ledger/views 后比较 `DEV.todo.md`、`OPS.todo.md`、`QA.todo.md` 与 `tasks.jsonl` 是否一致。

## 11. 晋升判断

| 去向 | 是否建议 | 说明 |
|---|---|---|
| 本地 TASK | 建议 | 将结论拆为 PM 可执行 TASK |
| CodeFlowMu Issue | 建议 | views/ledger 不同步等宿主问题 |
| FCoP Issue | 否 | 协议/工具链问题时 |
| ADR | 否 | — |
| shared | 否 | — |
| emergence-log | 建议 | observer 已检出受控涌现或项目树涌现；写入 emergence-log |

---

*由 EVAL-01 按合并规格生成；不进入 ReportWatcher / PM 整合环。*
