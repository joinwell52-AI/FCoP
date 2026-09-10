# FCoP 4.0 WP1 · 合同收口结果

## 1. 执行状态

```yaml
WP1_STATUS: COMPLETE
AUTHORIZED_SCOPE: WP1_CONTRACT_CONSOLIDATION_ONLY
BASELINE_HEAD: 68dbeb15f4e7f84e1d03f907be9fa66c2265843e
WP0_EVIDENCE_COMMIT: c259bebdad77122d24dc18a6dd3f8fe191e4042f
BASELINE_VERIFIED: true
WORKTREE: D:\FCoP-wp1-contract
BRANCH: codex/fcop-4.0-wp1-contract
FCOP_4_CONTRACT_FROZEN: false
IMPLEMENTATION_AUTHORIZED: false
WP2_AUTHORIZED: false
```

本 WP 仅形成候选合同与审计报告。`COMPLETE` 表示 WP1 任务书要求的候选材料已经完整，不表示合同已冻结、规范已发布或实现已获授权。

## 2. 输入与隔离核验

| 项目 | 结果 |
|---|---|
| WP1 任务书 | `FCoP-4.0-WP1-Contract-Consolidation-Taskbook.zh.md` |
| 任务书 SHA-256 | `2c6b511b9aadcdaf29d48024dffaa3dd55f2bcbbf220bdcd33cb36efe1858fc7` |
| 任务书行数/字节数 | `588` / `21412` |
| WP0 evidence commit | 存在；包含六份 WP0 审计报告 |
| WP0 baseline ancestry | `68dbeb15...` 是 `c259bebd...` 的祖先 |
| 起始 worktree 状态 | clean at `c259bebdad77122d24dc18a6dd3f8fe191e4042f` |
| 原工作区 `D:\FCoP` | 未清理、未切分支、未迁移、未重新部署规则、未写入 |
| WP0 worktree | 未修改 |
| CodeFlowMu | 未修改 |

未发现需要回写 WP0 报告的新事实错误；因此没有提出 WP0 勘误请求。

## 3. 交付物

仅新增/修改以下六个授权文件：

1. `spec/fcop-4.0-spec.md`
2. `spec/fcop-4.0-spec.zh.md`
3. `reports/FCOP-4.0-WP1-CONTRACT-DECISIONS.md`
4. `reports/FCOP-4.0-WP1-CONFORMANCE-MATRIX.md`
5. `reports/FCOP-4.0-WP1-COMPATIBILITY-AND-MCP.md`
6. `reports/FCOP-4.0-WP1-RESULT.md`

## 4. 合同收口结果

```yaml
CONTRACT_CONFLICTS_RESOLVED: 30/30
CORE_CONTRACTS: 8/8
SPEC_EN_ZH_PARITY: PASS
MCP_TOOL_MAPPING: 45/45
STATIC_RESOURCE_MAPPING: 11/11
RESOURCE_TEMPLATE_MAPPING: 3/3
DOWNSTREAM_CLOSE_ISSUE_EXCLUDED: 1/1
ATOMICITY_SCENARIOS_MAPPED: 6/6
P0_OPEN: 0
```

Core 严格限定为 C1–C8。候选规范没有把 EVAL、Ledger、固定角色、Git Branch、Relay、CodeFlowMu 或发布设施提升为 Core；没有引入第五类 envelope、Base `active -> done`、权威 `archive -> history`、`relation: branch` 或 `ref_task`。

## 5. 验证

```yaml
UTF8: PASS
SPEC_CLAUSE_PARITY: PASS
SPEC_ERROR_CODE_PARITY: PASS
CONFLICT_DECISION_COUNT: PASS_30_OF_30
CORE_COUNT: PASS_8_OF_8
MCP_TOOL_COUNT: PASS_45_OF_45
STATIC_RESOURCE_COUNT: PASS_11_OF_11
RESOURCE_TEMPLATE_COUNT: PASS_3_OF_3
ATOMICITY_SCENARIO_COUNT: PASS_6_OF_6
GIT_DIFF_CHECK: PASS
DOC_ONLY_ALLOWLIST: PASS
TESTS: NOT_RERUN_CONTRACT_ONLY
```

测试未重跑，符合任务书对纯合同 WP 的规定。提交 SHA 由提交完成后的标准回执报告；提交不能把自身最终 SHA 写入其内容而仍保持该 SHA 不变。

## 6. 变更边界

```yaml
CODE_FILES_MODIFIED: 0
SCHEMA_FILES_MODIFIED: 0
TEST_FILES_MODIFIED: 0
BUILD_RELEASE_DEPENDENCY_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0
WORKSPACE_MIGRATIONS_RUN: 0
REMOTE_PUSHED: false
COMMIT_REACHABILITY: LOCAL_ONLY
```

## 7. Gate 请求与停止点

```yaml
REQUESTED_GATE: FCOP_4_CONTRACT_FROZEN
GATE_SIGNED_BY_CODEX: false
NEXT_WP_STARTED: false
```

请求 ADMIN 审阅候选合同并决定是否签署 `FCOP_4_CONTRACT_FROZEN`。在该 Gate 明确签署且另行下发 WP2 任务书前，不进入 WP2，不编写符合性测试，不修改 Schema、Core、Lifecycle、MCP 实现或 CodeFlowMu，不发布 RC。

## 8. WP1.1 合同修订回执

本节追加记录 Gate review 要求的 WP1.1 修订；以上 WP1 原始执行事实保留，不被重写。候选合同版本由 `4.0.0-candidate.1` 修订为 `4.0.0-candidate.2`，状态仍为 Candidate / Not Implemented / Not Released。

### 8.1 输入与授权

```yaml
WP1_1_STATUS: COMPLETE
AUTHORIZED_SCOPE: WP1_CORRECTION_ONLY
TASKBOOK: FCoP-4.0-WP1.1-Contract-Correction-Taskbook.zh.md
TASKBOOK_LINES: 556
TASKBOOK_BYTES: 20551
TASKBOOK_SHA256: 66b43ee8f7d5b783011ee24a2f29275c7eaf66a9596bedaa8dc8e2b3a6bcc234
INPUT_COMMIT: 1b50f9e1fd4d2d21002bb1b98e14fd903a050f07
BASELINE_HEAD: 68dbeb15f4e7f84e1d03f907be9fa66c2265843e
WP0_EVIDENCE_COMMIT: c259bebdad77122d24dc18a6dd3f8fe191e4042f
WORKTREE: D:\FCoP-wp1-contract
BRANCH: codex/fcop-4.0-wp1-contract
```

### 8.2 修订完成度

```yaml
WP1_1_CORRECTIONS: 8/8
T1_T7_GATE_MATRIX: 7/7
BASE_ERROR_CODES: 31/31
SPEC_EN_ZH_PARITY: PASS
AUTHORIZATION_TRUST_BOUNDARY: CLOSED
EMPTY_PROFILE_BEHAVIOR: DEFINED
BRANCH_TERMINAL_GATE: DEFINED
FAMILY_LINEARIZATION_SCOPE: DEFINED
WORKSPACE_FORK_BOUNDARY: DEFINED
FAMILY_DIGEST_ALGORITHM: DEFINED
RECOVERY_STATE_TABLE: 5/5
IDEMPOTENCY_LAYERS: 3/3
```

R1–R8 已作为对原 30 项裁决的精化逐项映射，没有伪造为 38 项新冲突。T1–T7 现在各自唯一说明前置状态、REPORT、REVIEW、Authorization Profile 与新 attempt；`family_digest` 使用固定 `fcop-family-v1` canonical object；恢复只使用五种分类，并区分外部 create 幂等、所有 lifecycle 内部恢复、T4/T5/T6/T7 授权响应丢失重试。

### 8.3 修改与验证边界

```yaml
FILES_MODIFIED: 6/6_AUTHORIZED_WP1_FILES
CODE_FILES_MODIFIED: 0
SCHEMA_FILES_MODIFIED: 0
TEST_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0
UTF8_LF: PASS
CLAUSE_ID_PARITY: PASS
T1_T7_SEMANTIC_PARITY: PASS
BASE_ERROR_SET_PARITY: PASS_31_OF_31
R1_R8_MAPPING: PASS_8_OF_8
RECOVERY_STATE_TABLE: PASS_5_OF_5
GIT_DIFF_CHECK: PASS
DOC_ONLY_ALLOWLIST: PASS
TESTS: NOT_RERUN_CONTRACT_ONLY
COMMIT_REACHABILITY: LOCAL_ONLY
REMOTE_PUSHED: false
```

最终 WP1.1 commit SHA 由提交后的标准回执报告，避免自引用改变提交 SHA。

### 8.4 Gate 与停止点

```yaml
FCOP_4_CONTRACT_FROZEN: false
WP2_STARTED: false
REQUESTED_GATE: FCOP_4_CONTRACT_FROZEN
```

Codex 仅重新请求 ADMIN 审阅并签署 Gate，不代签，不进入 WP2，不修改实现、Schema、测试、MCP、发布流程或 CodeFlowMu。
