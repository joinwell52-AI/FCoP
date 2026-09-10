---
document_role: ADMIN_GATE_RECEIPT
gate: WP3D_CONVERGENCE_ACCEPTED
decision: ACCEPTED
issued_at: 2026-09-05
accepted_review_head: 7e0b42187bdee6a9fda3b0df2a2bc1e97cb8859f
wp3d_manifest_head: 639d8eb5be4d85303d8ac09e56bcef25c262d583
wp3d_1_manifest_head: 7e0b42187bdee6a9fda3b0df2a2bc1e97cb8859f
frozen_contract_commit: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
authorizes_wp3e_implementation: false
main_merge_authorized: false
release_authorized: false
---

# ADMIN Gate · WP3D_CONVERGENCE_ACCEPTED

## Decision

```yaml
GATE: WP3D_CONVERGENCE_ACCEPTED
DECISION: ACCEPTED
ACCEPTED_REVIEW_HEAD: 7e0b42187bdee6a9fda3b0df2a2bc1e97cb8859f
WP3D_IMPLEMENTATION: ACCEPTED
WP3D_1_PUBLIC_SURFACE_CLOSEOUT: ACCEPTED
WP3E_IMPLEMENTATION_AUTHORIZED_BY_THIS_GATE: false
MAIN_MERGE_AUTHORIZED: false
RELEASE_AUTHORIZED: false
```

本 Gate 接受 WP3D v1.1 的 canonical family digest、显式 convergence REVIEW、普通 TASK/Branch TASK/带 Branch Root 的 T7，以及 WP3D.1 对已授权公共 API 的 snapshot 与 CHANGELOG 收口。

本 Gate 不授权自动进入 WP3E。WP3E 必须另有一份从本 Gate Commit 顺序接出的固定执行任务书；它也不授权 WP4、main 合并、版本提升、tag、Release 或 PyPI 发布。

## Verified remote identity

| 项目 | 远端事实 |
|---|---|
| Frozen contract | `aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6` |
| WP3D taskbook | `4e0d8c524020cc3b1b152d3d3a736f84a2f78a4e` |
| WP3D content | `51bbe4438aecaa5fb0081cd9cdd45f9054007d88` |
| WP3D manifest/head | `639d8eb5be4d85303d8ac09e56bcef25c262d583` |
| WP3D.1 taskbook | `274797c1e7647f1831c2f9bb9a300981ec4cc3a7` |
| WP3D.1 content | `1a606e1e565c756ecf7f838d69fbf2b6febbf758` |
| WP3D.1 manifest / accepted head | `7e0b42187bdee6a9fda3b0df2a2bc1e97cb8859f` |
| WP3D.1 chain | Taskbook → Content → Manifest |
| WP3D.1 content files | 3 |
| WP3D.1 manifest files | 1 |
| WP3D.1 remote SHA-256 | 4/4 |

从 WP3D.1 最终 Taskbook Commit 到 accepted head 正好两次提交。Content Commit 只修改 `CHANGELOG.md`、`tests/test_fcop/snapshots/public_surface.json` 和收口报告；Manifest Commit 只新增 `reviews/fcop-4.0/wp3d.1/MANIFEST.md`。

## Accepted implementation evidence

```yaml
CANONICAL_FAMILY_DIGEST: PASS
CONVERGENCE_REVIEW: PASS
BRANCH_TERMINAL_GATE: PASS
ORDINARY_T7: PASS
BRANCH_T7: PASS
ROOT_WITH_BRANCHES_T7: PASS
T7_AUTHORIZATION_BINDING: PASS
T7_EXACT_RETRY: PASS
FAMILY_RACE_MATRIX: 8/8
WP3D_TARGET_NODES: 15/15
WP3D_NEW_TESTS: 23/23
FROZEN_TEST_IDS: 60/60
V4_STATIC_META: 27/27
V4_BEHAVIORAL: 69 passed / 23 deferred / 0 unexpected
V4_TOTAL: 96 passed / 23 deferred
V4_COLLECT_ONLY: 119
V3_REGRESSION: 907/907
MCP_REGRESSION: 80/80
UNEXPECTED_FAILURES: 0
```

关键实现复用既有 family lock、Lifecycle、可信 Profile evaluator、Authorization single-use 与三阶段 receipt；没有增加数据库、后台组件、第二权威存储、第二状态机、第二锁系统、依赖或 Base error code。唯一新生产模块为已授权的 `src/fcop/v4/convergence.py`，唯一新公共 API 为已授权的 `Project.family_digest(*, root_task_id: str) -> str`。

## Accepted WP3D.1 closeout

```yaml
PUBLIC_SURFACE_DRIFT_BEFORE: 1
PUBLIC_SURFACE_DRIFT_AFTER: 0
PUBLIC_SURFACE_ADDITION: Project.family_digest
PUBLIC_SURFACE_TESTS: 4/4
TEST_FCOP: 1118 passed / 0 failed / 0 skipped / 0 xfailed
CHANGELOG_UNRELEASED_ENTRY: PASS
PRODUCTION_FILES_MODIFIED_IN_WP3D_1: 0
TEST_LOGIC_FILES_MODIFIED_IN_WP3D_1: 0
FROZEN_FILES_MODIFIED_IN_WP3D_1: 0
```

Public-surface snapshot 只新增 `project.methods.family_digest`，其签名精确为 `family_digest(self, *, root_task_id: str) -> str`；没有其他公开对象、参数、返回类型、dataclass、异常、顶层导出或 rules/teams 漂移。

CHANGELOG 只新增 `[Unreleased]` additive API 条目，并明确不表示 FCoP 4.0 已发布，不改变 FCoP 3.2.5、MCP surface 或 CodeFlowMu 固定版本。

## Evidence limitations retained

- GitHub accepted head 的 combined commit status 没有上报 status contexts；本 Gate 不声称 GitHub Actions 已执行或通过。
- 本 Gate 接受的是 Manifest 记录的 Windows/本地与隔离回归证据，以及 ADMIN 对远端固定代码、差异、提交链和治理文件的复核。
- WP3D 已登记的 23 个 deferred Core 行为仍未实现；它们只能由后续 WP3E 固定任务书处理。
- Linux/macOS 原生并发与崩溃测试尚不能由本 Gate 推断为通过。
- WP3D.0 Gate 中记录的非隔离 `mcp/tests` HOME 拓扑敏感诊断仍保留；若后续触及 MCP 或工作区发现逻辑必须重新评估。

## Next-stage rule

WP3E 的固定任务书必须：

1. 以包含本 Gate receipt 的提交为唯一 `INPUT_HEAD`；
2. 只收口现存 23 个 deferred Core 行为和冻结 60 个 Test ID；
3. 编码前逐节点确认真实红灯与实现归属，不从测试文本发明新合同；
4. 优先复用现有 Encoding、Lifecycle、Authorization、receipt 与 family lock；
5. 不进入规则包、Host adapter、MCP/PyPI、Schema、CodeFlowMu 或发布工作；
6. 不增加后台进程、数据库、第二状态机、第二锁或隐藏恢复控制面；
7. 完成后停止并请求 `FCOP_4_CORE_IMPLEMENTATION_ACCEPTED`。

只有新的 WP3E 执行任务书可以授予 `WP3E_ONLY`，本 Gate 本身不授予实现权限。
