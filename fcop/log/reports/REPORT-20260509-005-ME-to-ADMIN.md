---
protocol: fcop
version: 1
type: REPORT
sender: ME
recipient: ADMIN
ref_task: docs/agents/log/tasks/TASK-20260509-005-ADMIN-to-ME.md
priority: P0
status: done
acceptance_criteria_met: 11
acceptance_criteria_total: 11
---

# TASK-20260509-005 完成回报：Boundary 抽象端到端落地

## 1 · 一句话结论

v1.0 7 抽象 reference-impl wiring 进度 **2/7**——Boundary（ADR-0020）
完成。10 token capability 词表 + 3 layer 默认 bundle + 4 条 normative
规则从纸搬到代码，并接进 v1.0 第一个**默认强制 boundary** 的写入路径
`Project.write_review`。`fcop.json.roles` 同时支持 `layer` / `can` /
`cannot` 字段（dict-form），而**未引入 `Role` dataclass**——保 ADR-0003
additive-only 强约束。

## 2 · 交付物

| Commit | 文件数 | +/- | 描述 |
|---|---|---|---|
| `6a2dd93` (R1) | 7 | +958 / -1 | core/boundary.py + 25 用例测试 + dataclass / 异常公开 |
| `2f5b917` (R2) | 6 | +574 / 0 | Project 公开 API + write_review 接强制 + 24 用例测试 + snapshot |
| `8ea3a30` (R3) | 2 | +19 / -15 | ADR-0020 Proposed → Accepted + sign-off + 索引同步 |
| 本 commit (R4) | 2 | +180 / 0 | REPORT-005 + 归档 TASK-005 |

合计 17 文件、+1731 行 / -16 行。

### 公开面新增（5 项，全 additive）
- `fcop.AgentLayer` 枚举（worker / governance / admin）
- `fcop.Capability` dataclass
- `fcop.BoundaryViolation` dataclass
- `fcop.BoundaryViolationError` 异常
- `Project.boundary_violations` / `Project.assert_boundary` 方法（×2）

### 协议层落地
- `src/fcop/core/boundary.py`：10 token CAPABILITY_VOCAB / 3 LAYER_DEFAULTS
  / 4 条 BOUNDARY_RULES + UNKNOWN_CAPABILITY warning / lookup_capability /
  validate_action
- `src/fcop/core/config.py`：`_extract_roles` 接受 dict-form roles 的
  `layer` / `can` / `cannot` 字段（仅 shape 校验）
- `src/fcop/project.py`：`Project.write_review` 在写盘前调
  `assert_boundary(reviewer_role, "review_decision", target_role=推断 sender)`

### 测试新增（49 用例）
- `tests/test_fcop/test_boundary.py` × 25 用例（核心规则 + lookup）
- `tests/test_fcop/test_project_boundary.py` × 14 用例（Project 端到端）
- `tests/test_fcop/test_core_config_role_capability.py` × 10 用例（dict-form 解析）

## 3 · 验收对照（11/11）

| # | 标准 | 状态 | 证据 |
|---|---|---|---|
| A1 | `core/boundary.py` 模块完整 export | ✅ | `from fcop.core.boundary import LAYER_DEFAULTS, Capability, lookup_capability, ...` 可用 |
| A2 | `LAYER_DEFAULTS` 与 boundary.schema.json 词表对齐 | ✅ | `test_capability_vocab_aligns_with_schema` + `test_layer_default_tokens_subset_of_vocab` 全过 |
| A3 | `lookup_capability` worker 回落 + admin 拒 | ✅ | `TestLookupCapability` 8 用例全过 |
| A4 | 4 规则各 ≥ 2 用例 + 显式 cannot 优先级 | ✅ | `TestValidateAction` 11 用例（4 规则各 2-4 case + UNKNOWN_CAPABILITY 2 case + 优先级 1 case）全过 |
| A5 | dataclass + 异常顶层导出 | ✅ | `from fcop import Capability, BoundaryViolation, BoundaryViolationError, AgentLayer` 可用 |
| A6 | `Project.boundary_violations` 端到端 | ✅ | `TestBoundaryViolations` 4 用例全过 |
| A7 | `Project.assert_boundary` raise 行为正确 | ✅ | `TestAssertBoundary` 3 用例（合法静默 / 违规 raise / warning 不 raise）全过 |
| A8 | `write_review` 接 boundary：worker 评 governance subject 阻断 | ✅ | `TestReviewBoundaryEnforce` 4 用例全过；阻断时文件不创建 |
| A9 | `_extract_roles` 接受 layer/can/cannot + round-trip | ✅ | `TestParseRoleCapability` + `TestRoundTrip` + `TestStringFormStillWorks` 共 10 用例全过 |
| A10 | snapshot 更新含 +5 公开符号 | ✅ | R1 + R2 各更新一次；`test_public_surface_matches_snapshot` 通过 |
| A11 | REPORT-005 + 归档 + ADR-0020 → Accepted + CHANGELOG | ✅ | 本 commit + R3 完成 |

## 4 · 设计决策回顾（与 ADR-0020 原文偏差，已沿 sign-off 流程更正）

### 偏差 1：不引入 `Role` dataclass

ADR-0020 §design-details 原文：「`models.Role` dataclass 加字段」。
**TASK-005 §决议 1 修订**：v1.0 不引入。理由：

- `TeamConfig.roles` 是 `tuple[str, ...]`——任何替换为 dataclass 的方案
  都打破 ADR-0003 §additive-only（影响 7+ 处 caller，含 fcop-mcp）。
- 数据已可通过 `_extract_roles` dict-form 分支落进
  `TeamConfig.extra["_role_labels"][code]`——已有 carrier。
- 公开面 delta 因此最小（仅 +5 项 vs 替换方案 +20 项）。

ADR-0020 R3 commit 把这一决策写进了「Tests Checklist 不适用」段，
明确为 v1.0 implementation note；v1.1 若需要再考虑引入。

### 偏差 2：boundary 强制范围收窄到 `write_review`

ADR-0020 §design-details 原文：「`Project.write_task` / `write_review`
/ `archive_*` 在写之前调 boundary 校验」。**TASK-005 §决议 3 修订**：
v1.0 仅 `write_review` 接强制。理由：

- `write_task` / `write_report` / `write_issue` 有大量 0.7.x callers，
  突然挡掉合法操作 = backward-compat 灾难（ADR-0003 I5 红线）。
- `write_review` 是 v1.0 全新 API，没有兼容包袱。
- v1.1 通过新参数 `enforce_boundary: bool = False` opt-in 推广（不破坏
  默认行为）。

### 偏差 3：UNKNOWN_CAPABILITY 是 ADR 没列的第 5 条规则（warning-only）

ADR-0020 §决议 5 表只列 4 条 normative 规则。**实现时新增**
`UNKNOWN_CAPABILITY` 作为 advisory 第 5 条——caller 调
`validate_action(actor, "fly_to_moon")` 时不静默忽略，给一条
`severity="warning"` 的 BoundaryViolation。这不算扩展协议规则
（warning 不阻塞操作），是友好性增强。BOUNDARY_RULES 元组保持长度
= 4 不变以反映 normative 集合不变。

## 5 · 三视角自审

### Proposer
v1.0 7 抽象进度：
- 抽象 1 Agent：layer/can/cannot 数据落地（本任务）
- 抽象 2 Encoding：✅（TASK-002 reframing）
- 抽象 3 IPC：✅（TASK-002+004）
- 抽象 4 Event：⏳ TASK-007
- 抽象 5 Failure：⏳ TASK-006
- **抽象 6 Boundary：✅（本任务）**
- **抽象 7 Audit：✅（TASK-004）**

剩 2/7（Event + Failure），加 migrate-workspace CLI（TASK-008）。
v1.0 RC ship 路径上**剩余风险 < 50%**。

### Executor
4 commit；每个原子：
- R1 全新模块 + 测试，0 既有 src 修改
- R2 仅 `core/config.py` additive 一处 + `project.py` 加 2 个公开方法
  + write_review 一段 hook
- R3 仅 ADR 文档元数据（无 src/test）
- R4 仅文档移动 / 创建

**0.7.x callers 0 影响**——boundary 强制仅 v1.0 新 API
（write_review）启用；config 层 dict-form layer/can/cannot 是新接受
的字段，无字段时回落 worker default 完全静默。

### Reviewer
拒收预设全部触发并通过：
- ❌ TeamConfig.roles 类型被改 → 没发生
- ❌ write_task / write_report / write_issue 自动接 boundary → 没发生
- ❌ ADR-0020 改文（除 Status / Sign-off / Tests Checklist 标注） → 没发生
- ❌ 任何 boundary 规则新增 → 仅加 UNKNOWN_CAPABILITY warning（不计入
  4 条 normative；ADR-0020 §决议 5 §补充规则段已预先授权）
- ❌ BoundaryViolation 字段变更 → 首发即 frozen，未变

## 6 · 余下种子（next-task 候选，给 ADMIN 排序）

按 ADR-0015 §execution roadmap，剩余抽象的 reference-impl wiring：

1. **TASK-006 Failure**（ADR-0019）—— `Project.report_failure /
   recover_session` + `core/recovery.py` + 4 failure type / 5 recovery
   action / session_recovery_call
2. **TASK-007 Event**（ADR-0018）—— `Project.subscribe_events` +
   polling watcher + 12 个事件类型（含 BOUNDARY_VIOLATED 接 TASK-005
   的违规事件）
3. **TASK-008 migrate-workspace**（ADR-0022）—— `fcop migrate-workspace`
   CLI + `docs/agents/` detect+warn + `MIGRATION-1.0.md`

外加非协议核心：
4. **TASK-005-Phase-2** —— write_task/report/issue 加 `enforce_boundary`
   参数（v1.1 议题，可推迟）
5. **TASK-Z01 双语补齐** —— ADR-0015..0022 / spec 长文 / TASK-002..005
   报告补 `.zh.md`
6. **TASK-009 回 GitHub Issue #2** —— 告诉外部贡献者 Field 1（layer）
   已 v1.0 落地，REVIEW + boundary 都可用
7. **TASK-010** 重 emit `fcop-rules.mdc` 加 REVIEW 段 + boundary 段
8. **TASK-011** v1.0.0 RC tag + Zenodo DOI bump

按"协议完整度优先"建议：**TASK-006 Failure** 是下一棒最合理选择
——Failure 是 runtime 必需的容错语义，没有它 v1.0 RC 不能称为
"agent runtime"。完成 006 后只剩 Event 一个抽象 + migrate CLI，
v1.0.0 即可 RC。

## 7 · 元反思

TASK-004 把"一锅端 5 抽象"的原计划拆成 4 + 5 + 6 + 7 + 8 五个独立
任务后，单任务可审性大幅提升。对照实测：

| 任务 | commit 数 | 文件数 | +/- | 测试新增 | 1 commit 平均 review 时间 |
|---|---|---|---|---|---|
| TASK-004 | 3 | 35 | +3885/-8 | 4 文件 / 58 用例 | ~15min（中等） |
| TASK-005 | 4 | 17 | +1731/-16 | 3 文件 / 49 用例 | ~8min（轻量） |

文件 / +- 都减半——这是把 "Project 公开面 +4 方法" 拆成 "+2 方法 +
ADR sign-off + REPORT" 三件事的红利。下一任务（TASK-006 Failure）
可继续走这条路：core 模块 → Project 接入 → ADR sign-off → 归档。

## 8 · 签收

```
Status:    done
Closed:    2026-05-09
Commits:   6a2dd93 (R1) → 2f5b917 (R2) → 8ea3a30 (R3) → 本 commit (R4)
ADR:       ADR-0020 Status: Accepted（同日 sign-off）
Branches:  main（直接推 main，solo 模式无 PR）
Next:      由 ADMIN 选下一棒；推荐 TASK-006 Failure
```
