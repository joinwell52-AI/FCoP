# FCoP 4.0 WP3D.1 Public Surface 与 CHANGELOG 收口报告

## 1. 执行身份与范围

```yaml
WP3D_1_STATUS: COMPLETE_PENDING_GITHUB_DELIVERY
AUTHORIZED_SCOPE: WP3D_1_ONLY
TASKBOOK_PATH: taskbooks/fcop-4.0/WP3D.1/01-Public-Surface-Snapshot-and-Changelog-Closeout-Taskbook-v1.0.zh.md
TASKBOOK_COMMIT: 274797c1e7647f1831c2f9bb9a300981ec4cc3a7
TASKBOOK_SHA256: b7f9c6fe18cf36ef67e4ac6dc4f0a29817de05af3f4adf9ee126a4db909272f7
INPUT_HEAD: 639d8eb5be4d85303d8ac09e56bcef25c262d583
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
WORKTREE: D:\FCoP-wp3d1-public-surface-closeout
BRANCH: review/fcop-4.0-wp3d.1-public-surface-closeout
```

任务书 Git blob 为 9726 字节、295 行，SHA-256 与 ADMIN 固定值一致。祖先链为
`639d8eb5 → 1b398537 → 274797c1`；WP3D Content Commit
`51bbe443` 是 `639d8eb5` 的直接父提交，WP3D Taskbook Commit
`4e0d8c52` 是 `51bbe443` 的直接父提交。冻结合同提交是固定输入的祖先，且当前
中英文冻结规范与该提交的 Git blob 一致。

原 `D:\FCoP` 的已修改、未跟踪及历史文件未被清理、覆盖、迁移或带入本
worktree。

## 2. 更新前事实与精确漂移

更新前执行：

```text
python -m pytest -q tests/test_fcop/test_public_surface.py
```

结果为 `1 failed / 3 passed`。唯一失败是
`test_public_surface_matches_snapshot`，其唯一语义差异为：

```json
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
```

没有其他对象、方法、属性、参数、返回类型、dataclass、异常、顶层导出或
rules/teams 漂移。

## 3. 收口内容

`tests/test_fcop/snapshots/public_surface.json` 只新增上述 17 行
`Project.family_digest(*, root_task_id: str) -> str` 描述。生成命令按任务书使用
`--snapshot-update`，生成后的 Git diff 已人工复核；生成步骤自身的一个 skip
仅表示快照写入完成，普通验证没有 skip、xfail 或 expected-failure。

`CHANGELOG.md` 顶部新增唯一的 `## [Unreleased]` 节，登记：

- 该方法是 FCoP 4.0 declared workspace 的 canonical Root-family digest 公共读取入口；
- 该接口已由 WP3D 授权；
- 此记录不表示 FCoP 4.0 已发布；
- FCoP 3.2.5 行为、MCP surface 与 CodeFlowMu 固定版本不变。

历史发布记录和包版本均未改写。本轮没有新增或改变任何公共 API；只是把
WP3D 已实现的唯一 additive API 纳入快照与 CHANGELOG。

## 4. 验证结果

| 检查 | 真实结果 |
|---|---|
| 更新后 public-surface 普通验证 | 4 passed / 0 failed |
| `tests/test_fcop` | 1118 passed / 0 failed / 0 skipped / 0 xfailed |
| WP3D 固定目标节点 | 15/15 passed |
| v3/非 v4 回归（排除快照匹配节点） | 907 passed / 211 deselected |
| v4 Static/Meta 五文件 | 27/27 passed |
| 完整 v4 | 96 passed / 23 deferred |
| v4 Behavioral | 69 passed / 23 deferred / 0 unexpected |
| v4 collect-only | 119 collected；冻结 Test ID 60/60 |
| 隔离 MCP 回归，`PYTHONPATH=mcp/src;src` | 80/80 passed |
| `git diff --check` | PASS |

23 个 deferred 与 WP3D 已登记集合逐项相同：C3-X01 1、C4-R01 dangling gate
reference 1、C6-X01 1、C7-CREATE-01 1、C8-X01 4、C8-X03 3、
C8-STATE-01 5、C8-INDETERMINATE-01 1、AT-05 3、AT-06 3。它们不属于
WP3D.1 授权范围，本轮没有修改或隐藏。

## 5. 范围与不变量

```yaml
PUBLIC_SURFACE_DRIFT_BEFORE: 1
PUBLIC_SURFACE_DRIFT_AFTER: 0
PUBLIC_SURFACE_ADDITION: Project.family_digest
PUBLIC_SURFACE_SNAPSHOT: PASS
CHANGELOG_ADDITIVE_ENTRY: PASS
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
REMOTE_MAIN_BEFORE_DELIVERY: 68dbeb15f4e7f84e1d03f907be9fa66c2265843e
```

相对固定输入，任务书链只增加固定任务书；本轮内容改动严格限定为 snapshot、
CHANGELOG 与本报告。`src/**`、`mcp/**`、`schemas/**`、
`tests/conformance/v4/**`、测试逻辑、冻结规范、依赖与发布配置均无差异。

## 6. 停止状态

完成 Content Commit、Manifest-only Commit、push、重新 fetch 及逐文件 SHA-256
回读后立即停止。本报告不签署 Gate，不进入 WP3E/WP4，不修改 main，不创建
Release。

```yaml
WP3D_CONVERGENCE_ACCEPTED: false
WP3E_STARTED: false
WP4_STARTED: false
MAIN_MODIFIED: false
RELEASE_CREATED: false
REQUESTED_GATE: WP3D_CONVERGENCE_ACCEPTED
```
