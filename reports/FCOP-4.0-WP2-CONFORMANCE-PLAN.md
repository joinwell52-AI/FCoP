# FCoP 4.0 WP2 · Conformance-First 计划

## 1. 授权、冻结输入与停止点

```yaml
AUTHORIZED_SCOPE: WP2_CONFORMANCE_FIRST_ONLY
TASKBOOK: FCoP-4.0-WP2-Conformance-First-Taskbook.zh.md
TASKBOOK_SHA256: 60849fad9c6c0c62591620192b4b24446dcbcf72a74c9b747491114215fb8ad2
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
FROZEN_CONTRACT_VERSION: 4.0.0-candidate.2
FCOP_4_CONTRACT_FROZEN: true
IMPLEMENTATION_AUTHORIZED: false
WP3_STARTED: false
```

本阶段只增加独立符合性测试和两份 WP2 报告；测试驱动只能调用或探测当前
3.2.5 公开接口，缺失能力必须返回 `V4_NOT_IMPLEMENTED` 红灯。测试不得在
`tests/` 中实现可工作的 4.0 替身。完成 GitHub review 交付后只请求
`IMPLEMENTATION_AUTHORIZED`，不得自行签署或进入 WP3。

## 2. 三组独立验证

| 组 | 命令范围 | WP2 期望 |
|---|---|---|
| A · v3 回归 | 全 `tests/`，显式忽略 `tests/conformance/v4`；`PYTHONPATH=mcp/src;src` 绑定 worktree | 3.2.5 基线 `1225 passed, 2 skipped`，新增失败 0 |
| B · v4 静态合同 | `test_c0_contract_authority.py`、`test_mcp_surface_contract.py` | 全绿；英中条款/31 错误、45+11+3 MCP、发布门 |
| C · v4 行为合同 | C1–C8 八个行为文件 | 收集错误 0、skip/xfail 0、真实非零红灯；每个红灯带 test_id 和条款 |

预计当前实现可偶然通过 `C3-R01`（既有非法边拒绝）。其余 53 个行为节点在
未实现 4.0 前应保持红灯；静态 6 个节点应通过。

## 3. 完整合同矩阵映射（60/60）

以下 node 均以 `tests/conformance/v4/` 为根。

| test_id | pytest node |
|---|---|
| C0-PARITY-01 | `test_c0_contract_authority.py::test_c0_parity_01` |
| C0-AUTH-01 | `test_c0_contract_authority.py::test_c0_auth_01` |
| C0-ERROR-REGISTRY-01 | `test_c0_contract_authority.py::test_c0_error_registry_01` |
| C1-N01 | `test_c1_workspace.py::test_c1_contract[C1-N01]` |
| C1-R01 | `test_c1_workspace.py::test_c1_contract[C1-R01]` |
| C1-FORK-01 | `test_c1_workspace.py::test_c1_contract[C1-FORK-01]` |
| C1-OFFLINE-01 | `test_c1_workspace.py::test_c1_contract[C1-OFFLINE-01]` |
| C2-N01 | `test_c2_envelopes.py::test_c2_contract[C2-N01]` |
| C2-R01 | `test_c2_envelopes.py::test_c2_contract[C2-R01]` |
| C2-R02 | `test_c2_envelopes.py::test_c2_contract[C2-R02]` |
| C3-N01 | `test_c3_lifecycle.py::test_c3_n01` |
| C3-N02 | `test_c3_lifecycle.py::test_c3_n02` |
| C3-R01 | `test_c3_lifecycle.py::test_c3_r01` |
| C3-R02 | `test_c3_lifecycle.py::test_c3_r02` |
| C3-R03 | `test_c3_lifecycle.py::test_c3_r03` |
| C3-X01 | `test_c3_lifecycle.py::test_c3_x01` |
| C3-GATE-01 | `test_c3_lifecycle.py::test_c3_gate_01` |
| C4-N01 | `test_c4_relations.py::test_c4_contract[C4-N01]` |
| C4-N02 | `test_c4_relations.py::test_c4_contract[C4-N02]` |
| C4-R01 | `test_c4_relations.py::test_c4_contract[C4-R01]` |
| C4-R02 | `test_c4_relations.py::test_c4_contract[C4-R02]` |
| C5-N01 | `test_c5_convergence.py::test_c5_contract[C5-N01]` |
| C5-N02 | `test_c5_convergence.py::test_c5_contract[C5-N02]` |
| C5-R01 | `test_c5_convergence.py::test_c5_contract[C5-R01]` |
| C5-R02 | `test_c5_convergence.py::test_c5_contract[C5-R02]` |
| C5-R03 | `test_c5_convergence.py::test_c5_contract[C5-R03]` |
| C5-X01 | `test_c5_convergence.py::test_c5_contract[C5-X01]` |
| C5-BRANCH-01 | `test_c5_convergence.py::test_c5_contract[C5-BRANCH-01]` |
| C5-ARCHIVED-01 | `test_c5_convergence.py::test_c5_contract[C5-ARCHIVED-01]` |
| C5-FAMILY-DIGEST-01 | `test_c5_convergence.py::test_c5_contract[C5-FAMILY-DIGEST-01]` |
| C5-FAMILY-RACE-01 | `test_c5_convergence.py::test_c5_family_race_01` |
| C5-REPORT-RACE-01 | `test_c5_convergence.py::test_c5_report_race_01` |
| C6-N01 | `test_c6_authorization.py::test_c6_contract[C6-N01]` |
| C6-R01 | `test_c6_authorization.py::test_c6_contract[C6-R01]` |
| C6-R02 | `test_c6_authorization.py::test_c6_contract[C6-R02]` |
| C6-X01 | `test_c6_authorization.py::test_c6_contract[C6-X01]` |
| C6-PROFILE-01 | `test_c6_authorization.py::test_c6_contract[C6-PROFILE-01]` |
| C6-SPOOF-01 | `test_c6_authorization.py::test_c6_contract[C6-SPOOF-01]` |
| C6-DIGEST-01 | `test_c6_authorization.py::test_c6_contract[C6-DIGEST-01]` |
| C7-N01 | `test_c7_idempotency.py::test_c7_contract[C7-N01]` |
| C7-R01 | `test_c7_idempotency.py::test_c7_contract[C7-R01]` |
| C7-X01 | `test_c7_idempotency.py::test_c7_x01` |
| C7-CREATE-01 | `test_c7_idempotency.py::test_c7_contract[C7-CREATE-01]` |
| C8-N01 | `test_c8_recovery.py::test_c8_contract[C8-N01]` |
| C8-R01 | `test_c8_recovery.py::test_c8_contract[C8-R01]` |
| C8-X01 | `test_c8_recovery.py::test_c8_contract[C8-X01]` |
| C8-X02 | `test_c8_recovery.py::test_c8_contract[C8-X02]` |
| C8-X03 | `test_c8_recovery.py::test_c8_contract[C8-X03]` |
| C8-RETRY-01 | `test_c8_recovery.py::test_c8_contract[C8-RETRY-01]` |
| C8-STATE-01 | `test_c8_recovery.py::test_c8_contract[C8-STATE-01]` |
| C8-INDETERMINATE-01 | `test_c8_recovery.py::test_c8_contract[C8-INDETERMINATE-01]` |
| AT-01 | `test_c7_idempotency.py::test_at_01` |
| AT-02 | `test_c8_recovery.py::test_at_02` |
| AT-03 | `test_c5_convergence.py::test_at_03` |
| AT-04 | `test_c5_convergence.py::test_at_04` |
| AT-05 | `test_c8_recovery.py::test_at_05` |
| AT-06 | `test_c8_recovery.py::test_at_06` |
| MCP-SURFACE-01 | `test_mcp_surface_contract.py::test_mcp_surface_01` |
| MCP-PACKAGE-01 | `test_mcp_surface_contract.py::test_mcp_package_01` |
| RELEASE-GATE-01 | `test_mcp_surface_contract.py::test_release_gate_01` |

## 4. Test-only driver action → 条款

| driver action | 冻结条款 | 真实探测面 |
|---|---|---|
| `create_workspace` | F4.2.1–F4.2.3 | 调用 `Project.init_solo` 并读取真实 `fcop/fcop.json` |
| `derive_workspace` | F4.2.4–F4.2.6 | 探测显式 writable derive/fork API |
| `create_task` | F4.3.1–F4.3.2, F4.8 | 检查 `write_task` 的 operation/branch 合同参数 |
| `read_task` | F4.4.1, F4.9.3 | 使用真实 reader 并要求唯一状态检查 |
| `transition` | F4.4.1–F4.4.7 | 读取真实不可变 `ALLOWED_TRANSITIONS` |
| `write_report` | F4.3.3–F4.3.4, F4.6.1–F4.6.2 | 检查 attempt/head/replacement 参数 |
| `write_review` | F4.3.3, F4.3.5, F4.7 | 检查 typed review、family、Profile 授权参数 |
| `replace_report` | F4.3.3–F4.3.4 | 复用真实 REPORT surface，不生成替身 |
| `inspect_state` | F4.4.1, F4.9.3 | 探测 fail-closed 多路径检查 API |
| `list_branches` | F4.5.3–F4.5.4, F4.6.5 | 探测 `branch_of` family 枚举 API |
| `recover_operation` | F4.9.1–F4.9.11 | 区分 v4 durable receipt 与 legacy session recovery |
| `inject_fault` | F4.9.4, F4.9.9–F4.9.10 | 探测抽象 receipt stage fault hook |

## 5. 并发与故障策略

- `C7-X01`、`AT-01` 使用 Windows `spawn` 的两个真实进程，借助
  `multiprocessing.Event` 同步起跑，并通过当前 `Project.write_task` 竞争同一
  语义请求；不使用线程或 `sleep`。
- `C5-FAMILY-RACE-01`、`C5-REPORT-RACE-01`、`AT-02`、`AT-03`、
  `AT-04`、`AT-05` 均启动两个同步真实进程探测相应 commit surface；缺失
  参数/API 直接产生条款绑定的红灯，不以 import/collection error 代替。
- `C3-X01`、`C8-X01` 探测 PREPARED/TARGET_DURABLE/COMMITTED 抽象故障
  注入入口；`C8-STATE-01` 固定检查五种恢复状态；不按临时文件名耦合。
- 所有写入仅发生在 pytest `tmp_path`，不接触 `D:\FCoP` dogfood 或用户工作区。

## 6. WP1.1 计数漂移

```yaml
WP1_1_REQUIRED_TEST_ID_DECLARED: 13
WP1_1_REQUIRED_TEST_ID_OBSERVED: 14
CLASSIFICATION: DOCUMENT_COUNT_DRIFT
CONTRACT_SEMANTICS_AFFECTED: false
WP2_REQUIRED_COVERAGE: 14/14
```

14 个 ID 是：`C1-FORK-01`、`C1-OFFLINE-01`、`C5-BRANCH-01`、
`C5-ARCHIVED-01`、`C5-FAMILY-RACE-01`、`C5-REPORT-RACE-01`、
`C5-FAMILY-DIGEST-01`、`C6-PROFILE-01`、`C6-SPOOF-01`、
`C6-DIGEST-01`、`C7-CREATE-01`、`C8-RETRY-01`、`C8-STATE-01`、
`C8-INDETERMINATE-01`。WP2 不删除任何一项来迎合旧数字。

## 7. 写入 allowlist

```text
tests/conformance/v4/**
reports/FCOP-4.0-WP2-CONFORMANCE-PLAN.md
reports/FCOP-4.0-WP2-CONFORMANCE-RESULT.md
reviews/fcop-4.0/wp2/MANIFEST.md
```

冻结规范、WP1/WP1.1 文档、`src/`、`mcp/src/`、Schema、构建配置、版本、
CodeFlowMu、main、Tag/Release/PR 均不在 allowlist。
