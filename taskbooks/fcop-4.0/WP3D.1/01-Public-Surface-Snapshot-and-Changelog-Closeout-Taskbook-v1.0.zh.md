---
taskbook_id: FCOP-4.0-WP3D.1-PUBLIC-SURFACE-CLOSEOUT
document_role: EXECUTION_TASKBOOK
status: AUTHORIZED_FOR_WP3D_1_ONLY
execution_authorized: true
authorized_scope: WP3D_1_ONLY
gate_self_signing: forbidden
requested_gate: WP3D_CONVERGENCE_ACCEPTED
main_merge_authorized: false
release_authorized: false
---

# FCoP 4.0 WP3D.1：公共 API 快照与 CHANGELOG 收口任务书 v1.0

## 0. ADMIN 裁决

WP3D 的实现方向和限定范围通过技术审核，但当前不得签署 `WP3D_CONVERGENCE_ACCEPTED`。

原因不是 convergence/T7 实现失败，而是 WP3D 已授权并实际新增公共 API `Project.family_digest(*, root_task_id: str) -> str`，同时：

- `tests/test_fcop/test_public_surface.py` 仍有 1 项真实失败；
- `tests/test_fcop/snapshots/public_surface.json` 尚未收录该公共方法；
- `CHANGELOG.md` 尚未记录该 additive API surface change；
- WP3D v1.1 的允许写集漏掉了上述两个治理文件。

ADR-0003 明确要求：有意的附加性公共 API 变更必须更新 public-surface snapshot，并在 CHANGELOG 记录。失败测试不得改称 PASS，也不得以“预期漂移”代替收口。

因此下发本次极小修订。它只关闭交付/治理缺口，不重做 WP3D，不改变冻结合同，不增加能力。

```yaml
WP3D_GATE_DECISION: CHANGES_REQUIRED
WP3D_CONVERGENCE_ACCEPTED: false
AUTHORIZED_SCOPE: WP3D_1_ONLY
WP3E_AUTHORIZED: false
WP4_AUTHORIZED: false
MAIN_MERGE_AUTHORIZED: false
RELEASE_AUTHORIZED: false
```

## 1. 固定输入

执行前必须 fetch 并逐项核验：

```yaml
REPOSITORY: joinwell52-AI/FCoP
INPUT_HEAD: 639d8eb5be4d85303d8ac09e56bcef25c262d583
WP3D_CONTENT_COMMIT: 51bbe4438aecaa5fb0081cd9cdd45f9054007d88
WP3D_MANIFEST_COMMIT: 639d8eb5be4d85303d8ac09e56bcef25c262d583
WP3D_TASKBOOK_COMMIT: 4e0d8c524020cc3b1b152d3d3a736f84a2f78a4e
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
EXPECTED_INHERITED_PUBLIC_API: Project.family_digest
EXPECTED_SIGNATURE: "family_digest(self, *, root_task_id: str) -> str"
EXPECTED_INHERITED_TEST_STATE: "tests/test_fcop: 1117 passed + 1 public-surface snapshot failure"
```

输入 HEAD、任务书祖先链或冻结合同不一致时立即停止，不得从其他分支拼接。

## 2. 唯一目标

把已授权、已实现的 `Project.family_digest` 纳入现有公共 API 稳定性合同，使 `tests/test_fcop` 不再包含任何失败，同时在 CHANGELOG 如实登记这是 FCoP 4.0 候选实现阶段的 additive public API change。

本任务不修改 `family_digest` 的实现、签名或行为。

## 3. 执行方式

### 3.1 独立 worktree

不得在原 `D:\FCoP` 工作区直接开发。建议：

```text
worktree: D:\FCoP-wp3d1-public-surface-closeout
branch: review/fcop-4.0-wp3d.1-public-surface-closeout
base: 本任务书提交
```

若原工作区或目标 worktree 存在未知改动，保留现场并以 `DIRTY_PRESERVED` 停止；不得 stash、覆盖、清理或带入新分支。

### 3.2 更新 public-surface snapshot

允许运行：

```bash
pytest tests/test_fcop/test_public_surface.py --snapshot-update
```

随后必须人工核对 Git diff。相对输入 HEAD，snapshot 唯一允许的语义变化是：

```json
{
  "project": {
    "methods": {
      "family_digest": {
        "params": [
          {
            "annotation": null,
            "has_default": false,
            "kind": "POSITIONAL_OR_KEYWORD",
            "name": "self"
          },
          {
            "annotation": "str",
            "has_default": false,
            "kind": "KEYWORD_ONLY",
            "name": "root_task_id"
          }
        ],
        "return": "str"
      }
    }
  }
}
```

不得接受排序噪声之外的其他对象、方法、属性、参数、返回类型、dataclass、异常、顶层导出或 rules/teams 变化。出现额外语义 drift 时，以 `PUBLIC_SURFACE_UNEXPECTED_DRIFT` 停止。

更新后重新运行普通快照测试，禁止保留 skip/xfail/expected-failure：

```bash
pytest -q tests/test_fcop/test_public_surface.py
```

### 3.3 更新 CHANGELOG

在 `CHANGELOG.md` 顶部既有版本记录之前增加 `## [Unreleased]`（若固定输入已存在该节则复用，不得重复），记录一条明确的 additive API surface change：

- 新增 `Project.family_digest(*, root_task_id: str) -> str`；
- 用于 FCoP 4.0 declared workspace 的 canonical Root-family digest；
- 这是 WP3D 已授权的公共读取入口；
- 不表示 FCoP 4.0 已发布；
- 不改变 FCoP 3.2.5 的行为、MCP surface 或 CodeFlowMu 固定版本。

不得改写历史发布记录，不得提升包版本。

## 4. 允许修改范围

Content Commit 只允许：

```text
tests/test_fcop/snapshots/public_surface.json
CHANGELOG.md
reports/FCOP-4.0-WP3D.1-PUBLIC-SURFACE-CLOSEOUT.md
```

Manifest Commit 只允许新增：

```text
reviews/fcop-4.0/wp3d.1/MANIFEST.md
```

本任务书文件来自 ADMIN 固定提交，不得在执行分支修改。

## 5. 明确禁止

禁止：

- 修改任何 `src/**`、`mcp/**` 生产代码；
- 修改 `tests/test_fcop/test_public_surface.py` 或任何测试逻辑；
- 修改 `tests/conformance/v4/**`、冻结规范、Schema、Base error codes；
- 删除、改名、放宽 `Project.family_digest`；
- 通过 skip、xfail、条件绕过、mock 或 expected-failure 隐藏快照失败；
- 增加第二个公共 API、依赖、后台组件、权威存储、状态机、锁或错误码；
- 修改 CodeFlowMu；
- 修改 main、创建/合并 PR、建 tag/Release、上传 PyPI；
- 进入 WP3E/WP4；
- 自行签署 `WP3D_CONVERGENCE_ACCEPTED`。

任何生产代码或测试逻辑被证明必须修改时，以 `UNAUTHORIZED_FILE_REQUIRED` 停止并报告。

## 6. 强制验证

按顺序保存命令、退出码与结果：

1. 输入 HEAD、任务书提交、直接祖先和冻结合同核验；
2. 更新前复现唯一 public-surface drift，并保存精确 diff；
3. snapshot 更新后的语义 diff 审核：只新增上述 `family_digest` 条目；
4. `pytest -q tests/test_fcop/test_public_surface.py`：全部通过；
5. `pytest -q tests/test_fcop`：零失败、零新增 skip/xfail；
6. WP3D 15 个目标节点：15/15；
7. 全部 v4 Static/Meta 与 Behavioral：不得低于 `27 passed`、`69 passed / 23 deferred / 0 unexpected`；
8. v3 回归：不得低于输入证据 `907/907`，实际收集数如实报告；
9. 隔离 MCP 回归：`80/80`；
10. `git diff --check`、UTF-8/LF/BOM、allowlist 检查；
11. 确认 public API 相对 WP3D 输入仍只有一个新增项；
12. 确认生产代码、冻结文件、MCP、CodeFlowMu 与 remote main 未变；
13. 推送后重新 fetch，核验远端 HEAD、父链和全部交付文件 SHA-256。

不得把 WP3D 原有 23 个明确 deferred 项误报为本轮失败，也不得减少、改名或跳过冻结 60 个 Test ID。

## 7. 交付与提交链

分支从本任务书提交创建：

```text
review/fcop-4.0-wp3d.1-public-surface-closeout
```

提交链固定：

```text
Taskbook Commit
  → Content Commit
  → Manifest Commit
```

Content Commit 包含第 4 节前三个文件；Manifest Commit 只新增 Manifest。不得 force push。

Manifest 至少记录：

- 任务书路径、提交与 SHA-256；
- 固定输入与冻结合同；
- snapshot 更新前后的精确公共面差异；
- CHANGELOG 新增条目；
- 全部测试结果；
- allowlist、复杂度预算和未修改范围；
- Content/Manifest commit；
- 远端回读及文件 SHA-256；
- Gate 尚未自行签署。

## 8. 停止条件

```text
TASKBOOK_IDENTITY_MISMATCH
BASELINE_MISMATCH
FROZEN_CONTRACT_MISMATCH
DIRTY_PRESERVED
PUBLIC_SURFACE_UNEXPECTED_DRIFT
PUBLIC_SURFACE_TEST_NOT_GREEN
CHANGELOG_SCOPE_EXPANSION
UNAUTHORIZED_FILE_REQUIRED
UNEXPECTED_V3_REGRESSION
UNEXPECTED_V4_REGRESSION
UNEXPECTED_MCP_REGRESSION
REMOTE_DELIVERY_VERIFICATION_FAILED
```

遇到任一条件，提交阻断报告并停止；不得扩大范围。

## 9. 完成回执

```yaml
WP3D_1_STATUS: COMPLETE | BLOCKED
AUTHORIZED_SCOPE: WP3D_1_ONLY
TASKBOOK_PATH: taskbooks/fcop-4.0/WP3D.1/01-Public-Surface-Snapshot-and-Changelog-Closeout-Taskbook-v1.0.zh.md
TASKBOOK_COMMIT: <sha>
TASKBOOK_SHA256: <sha256>
INPUT_HEAD: 639d8eb5be4d85303d8ac09e56bcef25c262d583
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
WORKTREE: D:\FCoP-wp3d1-public-surface-closeout
BRANCH: review/fcop-4.0-wp3d.1-public-surface-closeout

PUBLIC_SURFACE_DRIFT_BEFORE: 1
PUBLIC_SURFACE_DRIFT_AFTER: 0
PUBLIC_SURFACE_ADDITION: Project.family_digest
PUBLIC_SURFACE_SNAPSHOT: PASS | FAIL
CHANGELOG_ADDITIVE_ENTRY: PASS | FAIL
WP3D_TARGET_NODES: 15/15
FROZEN_TEST_IDS: 60/60
TEST_FCOP: <result>
V3_REGRESSION: <result>
MCP_REGRESSION: <result>
V4_STATIC_META: <result>
V4_BEHAVIORAL: <passed/deferred/unexpected>
UNEXPECTED_FAILURES: <n>

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

CONTENT_COMMIT: <sha>
MANIFEST_COMMIT: <sha>
REMOTE_HEAD: <sha>
REMOTE_PUSHED: true | false
REMOTE_REFETCH_VERIFIED: PASS | FAIL
DELIVERY_SHA256: <matched>/<total>
REMOTE_MAIN_UNCHANGED: true | false
WORKTREE_STATUS: CLEAN | DIRTY_PRESERVED

WP3D_CONVERGENCE_ACCEPTED: false
WP3E_STARTED: false
WP4_STARTED: false
MAIN_MODIFIED: false
RELEASE_CREATED: false
REQUESTED_GATE: WP3D_CONVERGENCE_ACCEPTED
```

完成并远端核验后立即停止，重新请求 ADMIN 审核。只有 ADMIN 在固定 GitHub review HEAD 上签署 `WP3D_CONVERGENCE_ACCEPTED`，才可另立 WP3E 任务书。
