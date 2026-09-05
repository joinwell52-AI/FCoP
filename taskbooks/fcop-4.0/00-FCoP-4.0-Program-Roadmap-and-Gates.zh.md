---
title: FCoP 4.0 统一项目路线图与阶段门
document_role: PROGRAM_ROADMAP
status: REVIEW_INPUT_ONLY
execution_authorized: false
authorized_scope: NONE
main_merge_authorized: false
release_authorized: false
roadmap_version: 1.0
roadmap_base_commit: 511039db227a23ae3e2d79aaae775a92ba392f5c
active_execution_taskbook_commit: 46c7d7522f020e85ad658a9e0147578d61fe908a
---

# FCoP 4.0 统一项目路线图与阶段门

## 0. 文档性质

本文只统一 FCoP 4.0 的阶段编号、依赖关系、交付位置和 ADMIN Gate。

本文不是执行任务书，不授权 Codex 修改代码、规范、Schema、MCP、PyPI、CodeFlowMu 或 main。任何阶段必须另有一份唯一执行任务书，并由 ADMIN 明确签署该阶段的授权范围。

## 1. 总原则

1. FCoP 4.0 只有一条顺序实施主线。
2. 同一时刻只允许一个会修改 FCoP 实现的工作包处于 ACTIVE。
3. 后续阶段必须从前一阶段已验收的 GitHub review head 顺序接出。
4. 总规划、候选设计和 review input 不能替代执行授权。
5. 每个工作包完成后必须推送 GitHub review 分支、回读验证、提交 Manifest，并停止等待 Gate。
6. 不通过聊天文本、未推送的本地提交或工作树状态作为唯一验收证据。
7. 不修改原始脏工作树；使用独立 git worktree。
8. CodeFlowMu 在 FCoP 4.0 发布前只作只读下游兼容性 shadow，继续固定使用 FCoP 3.2.5。
9. 不允许新增后台调度器、watcher、第二权威状态库或隐藏控制平面。
10. FCoP 4.0 的规范权威始终是冻结的 `spec/fcop-4.0-spec.md` 与 `spec/fcop-4.0-spec.zh.md`；规则包、Host 投影、MCP 和 PyPI 都是派生实现或发布载体。

## 2. 唯一阶段链

| 阶段 | 内容 | 当前状态 | 进入条件 | 完成 Gate |
|---|---|---|---|---|
| WP0 | 3.2.5 基线与冲突审计 | COMPLETE | WP0_ONLY | BASELINE_VERIFIED |
| WP1 / WP1.1 | 4.0 合同冻结与修订 | COMPLETE | BASELINE_VERIFIED | FCOP_4_CONTRACT_FROZEN |
| WP2 / WP2.1 / a / b | 静态与行为符合性测试、信任边界 | COMPLETE | FCOP_4_CONTRACT_FROZEN | IMPLEMENTATION_AUTHORIZED |
| WP3A / A.1 | 工作区与创建面 | COMPLETE | IMPLEMENTATION_AUTHORIZED | WP3A_IMPLEMENTATION_ACCEPTED |
| WP3B / B.1 | 生命周期、原子迁移与执行轮次 | COMPLETE | WP3A_IMPLEMENTATION_ACCEPTED | WP3B_LIFECYCLE_ACCEPTED |
| WP3C | Authorization 与受控迁移 T4/T5/T6 | COMPLETE_PENDING_CORRECTION | WP3B_LIFECYCLE_ACCEPTED | — |
| WP3C.1 | 授权载体矩阵、过期线性化与receipt绑定收口 | COMPLETE | WP3C_REMOTE_HEAD bd61efeb… | — |
| WP3C.2 | T6冻结符合性夹具与冻结合同对齐 | ACTIVE | WP3C.1_REMOTE_HEAD d0d9ec02… | WP3C_AUTHORIZATION_ACCEPTED |
| WP3D | Branch、显式收敛、family digest 与 T7 | NOT_AUTHORIZED | WP3C_AUTHORIZATION_ACCEPTED | WP3D_CONVERGENCE_ACCEPTED |
| WP3E | 剩余 Core 符合性收口；60/60 冻结测试全绿 | NOT_AUTHORIZED | WP3D_CONVERGENCE_ACCEPTED | FCOP_4_CORE_IMPLEMENTATION_ACCEPTED |
| WP4.0 | 规则大文件、Host入口、装配与发布现状只读审计 | NOT_AUTHORIZED | FCOP_4_CORE_IMPLEMENTATION_ACCEPTED | WP4_BASELINE_VERIFIED |
| WP4.1 | 冻结规则分层、Manifest、Host Profile 与宪法加载合同 | NOT_AUTHORIZED | WP4_BASELINE_VERIFIED | WP4_RULE_CONTRACT_FROZEN |
| WP4.2 | 先写失败的规则生成、漂移、Host装配与加载证据测试 | NOT_AUTHORIZED | WP4_RULE_CONTRACT_FROZEN | WP4_TESTS_ACCEPTED |
| WP4.3 | 实现 Core规则源＋分类模块＋Manifest＋生成器 | NOT_AUTHORIZED | WP4_TESTS_ACCEPTED | WP4_RULE_PACKAGE_ACCEPTED |
| WP4.4 | Codex、Cursor、Claude Code 等已采用 Host 的薄投影验证 | NOT_AUTHORIZED | WP4_RULE_PACKAGE_ACCEPTED | WP4_HOST_PROJECTIONS_ACCEPTED |
| WP4.5 | CodeFlowMu 3.2.5 固定版本下的非侵入兼容性 shadow | NOT_AUTHORIZED | WP4_HOST_PROJECTIONS_ACCEPTED | WP4_DOWNSTREAM_SHADOW_ACCEPTED |
| WP4.6 | 激活、回滚、摘要一致性与发布装配验收 | NOT_AUTHORIZED | WP4_DOWNSTREAM_SHADOW_ACCEPTED | WP4_RULE_DISTRIBUTION_ACCEPTED |
| WP5 | Schema、Toolkit、MCP薄适配与双PyPI制品收口 | NOT_AUTHORIZED | WP4_RULE_DISTRIBUTION_ACCEPTED | FCOP_4_DISTRIBUTION_ACCEPTED |
| WP6 | 跨平台RC、从公共PyPI回装、GitHub Release与最终发布审计 | NOT_AUTHORIZED | FCOP_4_DISTRIBUTION_ACCEPTED | FCOP_4_RELEASE_AUTHORIZED |

WP3E 只处理 WP3C、WP3D 完成后仍未通过的冻结 Core 测试，不预先发明新能力；如果届时 60/60 已全部通过，WP3E 仍须形成零实现收口报告，但不得借机扩展范围。

## 3. 当前唯一允许继续的工作

当前WP3C.1已交付远端审核头 `d0d9ec029516b4379dbf74f2167490f4867680c4`。三项生产修正通过代码审核，但冻结 `C3-GATE-01[T6]` 夹具仍把 reopen REVIEW 同时作为授权，和冻结F4.7.2冲突。当前Codex只能执行：

- Taskbook commit：`cc06603108db31d6c7e0c3b6ce5cf9e8769b6472`
- Taskbook path：`taskbooks/fcop-4.0/WP3C.2/01-T6-Frozen-Conformance-Fixture-Alignment-Taskbook.zh.md`
- Input head：`d0d9ec029516b4379dbf74f2167490f4867680c4`
- Authorized scope：`WP3C_2_ONLY`
- Required stop Gate：`WP3C_AUTHORIZATION_ACCEPTED`

WP3C.2只允许修正一个Conformance测试文件以及报告/Manifest；生产代码不得修改。

以下候选资料只能作为后续 WP4 的 review input，不得在 WP3C 中读取为执行授权：

- branch：`review/fcop-4.0-rule-package-taskbook`
- reviewed head：`587a461b9d6bff7a3ec3887ded2dae8b4d368143`
- original title：`FCoP-4.0-WP3C-rule-package-and-host-adapters-taskbook-v0.1.md`

该候选的思想被纳入 FCoP 4.0，但其 WP3C 编号和连续执行权被撤销。它必须改编为 WP4 总规划输入，并在 WP3D/WP3E 验收后的真实 accepted head 上重新核验。

## 4. WP3C.2 完成后的固定动作

1. Codex推送WP3C.2 review分支和Manifest。
2. Codex远端回读并验证交付文件摘要。
3. Codex停止，不进入 WP3D。
4. ADMIN审核WP3C.2测试对齐、WP3C.1生产修正和WP3C整体回归。
5. 只有WP3C.2通过且符合性红灯恢复为既有38项，并签署 `WP3C_AUTHORIZATION_ACCEPTED` 后，才能编制并授权WP3D执行任务书。
6. WP3D任务书必须引用WP3C.2已验收的remote head，不得继续从 `511039db...` 或规则包旧分支接出。

## 5. WP4 的正式边界

WP4 是 FCoP 4.0 正式工作包和发布阻断项，不是独立产品线。

WP4必须实现：

- 规则规范源按分类拆分；
- 单一 Manifest 与确定性生成；
- 禁止直接维护生成后的 AGENTS.md、CLAUDE.md 和 .mdc；
- 仅为 ADMIN 已采用的 Host Profile 生成薄入口；
- Agent原生软件工程宪法强制用于“开发 FCoP 的 Agent”；
- 普通 FCoP 业务 Agent 不注入开发宪法；
- wheel、PyPI、MCP资源、GitHub Release 使用同一规则制品摘要；
- 可验证激活与显式回滚。

WP4不得形成：

- 第二份 FCoP Core 规范；
- 第五种正式信封；
- 新 Runtime 数据库；
- watcher、自动更新器或后台Host控制面；
- CodeFlowMu产品逻辑；
- 对 CodeFlowMu 的4.0升级或工作区迁移；
- 对冻结45项MCP工具面的未授权改变。

## 6. GitHub任务与交付规则

### 6.1 任务书

- 分支：`task/fcop-4.0-<stage>-<topic>`
- 目录：`taskbooks/fcop-4.0/<STAGE>/`
- review input：`execution_authorized: false`、`authorized_scope: NONE`
- 唯一执行书：`document_role: EXECUTION_TASKBOOK`，且只允许一个阶段范围
- 每份任务书必须固定 input commit、允许文件、禁止文件、测试命令、交付清单和停止 Gate

### 6.2 开发交付

- 分支：`review/fcop-4.0-<stage>-<topic>`
- Manifest：`reviews/fcop-4.0/<stage>/MANIFEST.md`
- 报告：`reports/FCOP-4.0-<STAGE>-*.md`
- 必须包含 content commit 与 manifest commit
- 必须验证 remote refetch、提交可达性、文件清单和 SHA-256
- 不得修改 main、打tag或创建Release

### 6.3 阶段串接

下一阶段的 `INPUT_HEAD` 必须等于上一阶段 ADMIN 验收的 `REMOTE_HEAD`。禁止从旧基线并行开发后再手工拼接。

## 7. 发布总门

只有同时满足以下条件，ADMIN才可以考虑 `FCOP_4_RELEASE_AUTHORIZED`：

- 冻结合同未被修改；
- Core符合性测试60/60通过；
- 3.x回归无新增失败；
- Schema与规范一致；
- MCP disposition全部落实；
- 两个PyPI包来自同一已验证制品链；
- 规则Manifest、wheel、MCP资源与GitHub Release摘要一致；
- Host薄投影至少完成已采用Host的真实加载验证；
- CodeFlowMu 3.2.5 shadow无回归且未被升级；
- Windows、Linux、macOS RC证据完整；
- 公共PyPI回装验证通过；
- rollback材料存在并已验证；
- ADMIN显式签署发布Gate。

## 8. 当前状态回执

```yaml
PROGRAM: FCoP 4.0
ROADMAP_VERSION: 1.0
ACTIVE_STAGE: WP3C.2
ACTIVE_EXECUTION_COMMIT: cc06603108db31d6c7e0c3b6ce5cf9e8769b6472
PARALLEL_IMPLEMENTATION_ALLOWED: false
WP3D_AUTHORIZED: false
WP4_INCLUDED_IN_FCOP_4: true
WP4_RELEASE_BLOCKER: true
WP4_AUTHORIZED: false
MAIN_MERGE_AUTHORIZED: false
RELEASE_AUTHORIZED: false
NEXT_DECISION: REVIEW_WP3C_2_RESULT
```
