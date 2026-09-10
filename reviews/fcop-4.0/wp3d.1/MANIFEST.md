---
stage: WP3D.1
delivery_role: NON_AUTHORITATIVE_REVIEW_MANIFEST
status: REVIEW_READY
authorized_scope: WP3D_1_ONLY
delivery_head: SELF
gate_self_signed: false
requested_gate: WP3D_CONVERGENCE_ACCEPTED
---

# FCoP 4.0 WP3D.1 Review Manifest

本交付只把 WP3D 已授权的 `Project.family_digest` 收录到 public-surface
snapshot 和 CHANGELOG，并提供审计报告。它不改变实现、测试逻辑、冻结合同、
MCP、CodeFlowMu 或 main；ADMIN 是 Gate 的唯一签署者。

## Delivery identity

```yaml
WP3D_1_STATUS: COMPLETE
AUTHORIZED_SCOPE: WP3D_1_ONLY
TASKBOOK_REPOSITORY: joinwell52-AI/FCoP
TASKBOOK_PATH: taskbooks/fcop-4.0/WP3D.1/01-Public-Surface-Snapshot-and-Changelog-Closeout-Taskbook-v1.0.zh.md
TASKBOOK_COMMIT: 274797c1e7647f1831c2f9bb9a300981ec4cc3a7
TASKBOOK_SHA256: b7f9c6fe18cf36ef67e4ac6dc4f0a29817de05af3f4adf9ee126a4db909272f7
INPUT_HEAD: 639d8eb5be4d85303d8ac09e56bcef25c262d583
WP3D_CONTENT_COMMIT: 51bbe4438aecaa5fb0081cd9cdd45f9054007d88
WP3D_MANIFEST_COMMIT: 639d8eb5be4d85303d8ac09e56bcef25c262d583
WP3D_TASKBOOK_COMMIT: 4e0d8c524020cc3b1b152d3d3a736f84a2f78a4e
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
WORKTREE: D:/FCoP-wp3d1-public-surface-closeout
BRANCH: review/fcop-4.0-wp3d.1-public-surface-closeout

PUBLIC_SURFACE_DRIFT_BEFORE: 1
PUBLIC_SURFACE_DRIFT_AFTER: 0
PUBLIC_SURFACE_ADDITION: Project.family_digest
PUBLIC_SURFACE_SNAPSHOT: PASS
CHANGELOG_ADDITIVE_ENTRY: PASS
WP3D_TARGET_NODES: 15/15
FROZEN_TEST_IDS: 60/60
TEST_FCOP: 1118 passed / 0 failed / 0 skipped / 0 xfailed
V3_REGRESSION: 907/907
MCP_REGRESSION: 80/80
V4_STATIC_META: 27/27
V4_BEHAVIORAL: 69 passed / 23 deferred / 0 unexpected
V4_TOTAL: 96 passed / 23 deferred
V4_COLLECT_ONLY: 119
UNEXPECTED_FAILURES: 0

PRODUCTION_FILES_MODIFIED: 0
TEST_LOGIC_FILES_MODIFIED: 0
FROZEN_FILES_MODIFIED: 0
MCP_IMPLEMENTATION_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0
NEW_PUBLIC_APIS_IN_WP3D_1: 0
NEW_RUNTIME_DEPENDENCIES: 0
NEW_BACKGROUND_COMPONENTS: 0
NEW_AUTHORITATIVE_STORES: 0
NEW_STATE_MACHINES: 0
NEW_LOCK_SYSTEMS: 0
NEW_BASE_ERROR_CODES: 0

CONTENT_COMMIT: 1a606e1e565c756ecf7f838d69fbf2b6febbf758
MANIFEST_COMMIT: SELF
REMOTE_HEAD: SELF_AFTER_PUSH
REMOTE_PUSHED: VERIFY_IN_FINAL_POST_FETCH_RECEIPT
REMOTE_REFETCH_VERIFIED: VERIFY_IN_FINAL_POST_FETCH_RECEIPT
COMMIT_REACHABILITY: REQUIRE_TASKBOOK_AND_CONTENT_ANCESTORS_OF_FETCHED_SELF
DELIVERY_FILES: 3 content files plus this Manifest
DELIVERY_SHA256: 3/3 CONTENT_BLOBS_LISTED_BELOW
REMOTE_MAIN_BEFORE_DELIVERY: 68dbeb15f4e7f84e1d03f907be9fa66c2265843e

WP3D_CONVERGENCE_ACCEPTED: false
WP3E_STARTED: false
WP4_STARTED: false
MAIN_MODIFIED: false
RELEASE_CREATED: false
REQUESTED_GATE: WP3D_CONVERGENCE_ACCEPTED
```

`SELF` 表示包含本 Manifest 的提交，以避免自引用哈希。最终 post-fetch 回执
解析 `SELF`，并核验远端 Manifest 字节、两提交直接父链、三个 Content blob、
远端 main 稳定性与干净工作树。

## Public-surface 精确差异

更新前唯一失败为 `test_public_surface_matches_snapshot`。snapshot 的唯一新增
语义是 `project.methods.family_digest`：

```yaml
signature: family_digest(self, *, root_task_id: str) -> str
self.kind: POSITIONAL_OR_KEYWORD
self.annotation: null
self.has_default: false
root_task_id.kind: KEYWORD_ONLY
root_task_id.annotation: str
root_task_id.has_default: false
return: str
```

除此之外无对象、方法、属性、参数、返回类型、dataclass、异常、顶层导出或
rules/teams 漂移。更新后的普通快照验证为 4/4 通过；完整 `tests/test_fcop`
为 1118/1118 通过。

## CHANGELOG 条目

`CHANGELOG.md` 顶部新增一个 `## [Unreleased]` 节，只记录
`Project.family_digest(*, root_task_id: str) -> str` 是 FCoP 4.0 declared
workspace 的 canonical Root-family digest 公共读取入口和 WP3D 已授权的
additive API。本条明确不表示 4.0 已发布，不改变 3.2.5 行为、MCP surface
或 CodeFlowMu 固定版本；历史版本记录与包版本未修改。

## Content blob hashes

下列 SHA-256 与字节数覆盖 Content Commit
`1a606e1e565c756ecf7f838d69fbf2b6febbf758` 的精确 Git blob。三份文件均为
严格 UTF-8、LF、无 BOM；Manifest 不进入自身递归哈希表。

| SHA-256 | Bytes | File |
|---|---:|---|
| `67a7dfd6bef4df731f5aa55649dc879c5f84bcae96ea5828d367a58bc824f29b` | 128221 | `CHANGELOG.md` |
| `e339355339f620c74126f1f754f82ad7e7a3c0bdac4aeea2d5eeba5b33653ca5` | 4847 | `reports/FCOP-4.0-WP3D.1-PUBLIC-SURFACE-CLOSEOUT.md` |
| `ff15f73776ce0da8a0bdc3ae9c54031b8ba33a07ed8d4ade817de6f1c8ddfc3b` | 51907 | `tests/test_fcop/snapshots/public_surface.json` |

## 验证与范围证明

23 个 deferred 与 WP3D 既有登记逐项相同；没有将其误报为本轮失败，也没有
修改冻结 60 个 Test ID。Content Commit 的直接父提交是 Taskbook Commit，且
只包含 snapshot、CHANGELOG 和本报告。Manifest Commit 只允许新增本文件。

`src/**`、`mcp/**`、`schemas/**`、`tests/conformance/v4/**`、测试逻辑、冻结
规范、依赖与发布配置相对固定输入均无本轮变化。`git diff --check`、allowlist
和冻结中英文规范 blob 核验通过。

## Required post-push verification

无 force push 推送后重新 fetch 本 review 分支。要求 fetched HEAD 等于本
Manifest Commit；Content 为其直接父提交，Taskbook Commit 为 Content 的直接
父提交；Manifest Commit 只新增本文件；远端四个交付文件与本地 Git blob
逐项一致；远端 main 仍为
`68dbeb15f4e7f84e1d03f907be9fa66c2265843e`；worktree 干净。完成后停止并请求
`WP3D_CONVERGENCE_ACCEPTED`。
