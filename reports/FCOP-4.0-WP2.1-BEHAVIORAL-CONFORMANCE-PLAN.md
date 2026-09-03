# FCoP 4.0 WP2.1 · 行为符合性测试加强计划

## 1. 授权、输入与停止点

```yaml
AUTHORIZED_SCOPE: WP2_1_BEHAVIORAL_TEST_CORRECTION_ONLY
INPUT_BRANCH: review/fcop-4.0-wp2-conformance
INPUT_COMMIT: decfcc33ff4b26801417f4f68a75e6fdf493dd07
OUTPUT_BRANCH: review/fcop-4.0-wp2.1-behavioral-conformance
IMPLEMENTATION_AUTHORIZED: false
WP3_AUTHORIZED: false
WP3_STARTED: false
```

只修改 `tests/conformance/v4/**`、本报告与 WP2.1 结果报告，以及随后单独
提交的 `reviews/fcop-4.0/wp2.1/MANIFEST.md`。不修改规范、正式实现、Schema、
MCP 实现、CodeFlowMu、main、版本、发布、依赖或构建配置。

## 2. 测试分层

| 层 | 定义 | 是否计入行为符合性 |
|---|---|---|
| Static Surface | 规范对等、错误表、MCP catalog、方法解析和参数兼容诊断 | 否 |
| Behavioral Conformance | 对真实 `fcop.Project` 发起完整语义请求，并验证磁盘、返回值、错误码、不可变性、并发和重启后置条件 | 是 |
| Meta Guard | 检查每个冻结合同测试含 Arrange/Act/Assert；证明同名空壳、`**kwargs` 或返回 `None` 不能使行为测试通过 | 否 |

测试 driver 只是适配器：它把完整语义请求交给真实公开接口。方法不存在或
无法接受完整请求时，抛出带 `test_id`、F4 条款和诊断的
`V4_NOT_IMPLEMENTED`。driver 不生成 4.0 对象，不执行生命周期，不实现授权、
幂等、摘要或恢复算法。fixture 只负责布置可审计的输入状态和独立读取磁盘
事实，不能代替被测动作。

## 3. 冻结合同 60/60 · Arrange / Act / Assert

以下 60 个冻结 `test_id` 均保留独立语义；参数化节点用于覆盖同一合同内的
必要变体，不把多个合同 ID 合并成一次参数探针。

| test_id | pytest node | Arrange | Act | Assert |
|---|---|---|---|---|
| C0-PARITY-01 | `test_c0_contract_authority.py::test_c0_parity_01` | 读取英中候选规范 | 分别提取条款、迁移、Core、错误码 | 两边集合完全一致 |
| C0-AUTH-01 | `test_c0_contract_authority.py::test_c0_auth_01` | 读取规范权威条款 | 检查 Schema/规范优先级 | 行为规范优先且发布门存在 |
| C0-ERROR-REGISTRY-01 | `test_c0_contract_authority.py::test_c0_error_registry_01` | 读取英中错误表 | 提取 Base 与扩展约束 | 双语同为 31 项且禁止重定义 |
| C1-N01 | `test_c1_workspace.py::test_c1_n01` | 空目录和 4.0 manifest 请求 | 创建 workspace 后创建匹配 TASK | manifest 字段完整，TASK workspace_id 匹配且唯一落盘 |
| C1-R01 | `test_c1_workspace.py::test_c1_r01` | manifest 与 TASK 使用不同 workspace_id | 调用真实 create TASK | `WORKSPACE_ID_MISMATCH` 且目录 byte snapshot 零变化 |
| C1-FORK-01 | `test_c1_workspace.py::test_c1_fork_01` | 已存在源 workspace | 分别请求 derive 新 ID 与 retain ID | 新 ID 可写；retain 仅能拒绝或明确只读 |
| C1-OFFLINE-01 | `test_c1_workspace.py::test_c1_offline_01` | 单个离线 workspace，无 Registry/网络 | 创建本地 TASK | 成功且不伪造不可见 clone 冲突 |
| C2-N01 | `test_c2_envelopes.py::test_c2_n01` | 一个 workspace 与类型所需 subject | 真实写 TASK/REPORT/ISSUE/REVIEW | 四类均可按共同字段和类型字段解码 |
| C2-R01 | `test_c2_envelopes.py::test_c2_r01` | 在 lifecycle 中布置非法 EVAL/缺 typed identity 信封 | 调用生产状态检查 | `INVALID_ENVELOPE` 且零写入 |
| C2-R02 | `test_c2_envelopes.py::test_c2_r02` | 已有 REPORT/REVIEW 的原始 bytes | 写 replacement REPORT 与追加修正 REVIEW | 新事实引用旧事实，旧 bytes 永不改变 |
| C3-N01 | `test_c3_lifecycle.py::test_c3_n01` | TASK、current REPORT、Review 与授权证据 | 执行 T1→T2→T3→T4→T7 | 每边只移动一次、只发一个事件，最终 archive |
| C3-N02 | `test_c3_lifecycle.py::test_c3_n02` | done TASK 与有效 T6 授权 | 执行 reopen | 进入 active 且产生新 attempt |
| C3-R01 | `test_c3_lifecycle.py::test_c3_r01` | inbox TASK | 请求 inbox→archive | `INVALID_TRANSITION` 且仍在 inbox、零额外事实 |
| C3-R02 | `test_c3_lifecycle.py::test_c3_r02` | 4.0 active TASK | 调用 legacy finish | `LEGACY_TRANSITION_NOT_ALLOWED` 且不进入 done |
| C3-R03 | `test_c3_lifecycle.py::test_c3_r03` | archive 权威 TASK | 请求迁移到 history | 拒绝且 archive bytes/路径不变 |
| C3-X01 | `test_c3_lifecycle.py::test_c3_x01` | archive TASK 与导出故障边界 | 执行冷存储导出 | 权威 archive 不变，残留导出不获得 NOW 权力 |
| C3-GATE-01 | `test_c3_lifecycle.py::test_c3_gate_01[T1..T7]` | 每条边各自完整证据，并构造缺证据/缺授权对照 | 对 T1–T7 分别执行正负请求 | 完整前置才提交；负例稳定拒绝且原状态不变 |
| C4-N01 | `test_c4_relations.py::test_c4_n01` | parent、subject_ref、references 合法对象 | 创建含四关系的信封 | 四关系可解析，references 不改变所有权 |
| C4-N02 | `test_c4_relations.py::test_c4_n02` | active Root | 创建两个 sibling Branch | 两者为普通 TASK 且 `branch_of` 同 Root |
| C4-R01 | `test_c4_relations.py::test_c4_r01[...]` | 分别布置悬空、跨 workspace、self-cycle、门控弱引用缺失、强目标不唯一 | 创建关系对象 | 每种输入拒绝为 `RELATION_INVALID` 且零写入 |
| C4-R02 | `test_c4_relations.py::test_c4_r02` | Root→Branch 已存在 | 以 Branch 为 branch_of target 再建 Branch | `BRANCH_DEPTH_EXCEEDED` 且无孙 Branch |
| C5-N01 | `test_c5_convergence.py::test_c5_n01` | current attempt 唯一 final REPORT | 执行 T3 | active→review，event 精确引用 REPORT head |
| C5-N02 | `test_c5_convergence.py::test_c5_n02` | Root、两个终态 Branch、各自 current REPORT、convergence REVIEW 与授权 | 重算 family digest 并执行 Root T7 | digest 相等且 Root 可归档 |
| C5-R01 | `test_c5_convergence.py::test_c5_r01[missing/ambiguous]` | 分别无 REPORT、同 attempt 双 head | 执行 T3 | 对应 `REPORT_REQUIRED`/`REPORT_HEAD_AMBIGUOUS` 且状态不变 |
| C5-R02 | `test_c5_convergence.py::test_c5_r02` | reopen 后的新 attempt 与旧 REPORT | 用旧 REPORT 执行 T3 | `ATTEMPT_MISMATCH` 且不消费旧证据 |
| C5-R03 | `test_c5_convergence.py::test_stale_convergence_rejected[C5-R03]` | convergence 缺 Branch/旧 REPORT/旧 digest | 执行 Root T7 | `FAMILY_CONVERGENCE_MISMATCH` 且 Root 保持 done |
| C5-X01 | `test_c5_convergence.py::test_stale_convergence_rejected[C5-X01]` | 已有 convergence 后改变 family | 执行 Root T7 | 旧 convergence 失效，归档拒绝 |
| C5-BRANCH-01 | `test_c5_convergence.py::test_c5_branch_01` | Root done，Branch 位于 active/review | 执行 Root T7 | `BRANCH_NOT_TERMINAL` 且 Root 保持 done |
| C5-ARCHIVED-01 | `test_c5_convergence.py::test_c5_archived_01` | 有效 convergence 与 done Branch | Branch 授权归档后再执行 Root T7 | canonical family object/digest 不因路径变化而改变 |
| C5-FAMILY-DIGEST-01 | `test_c5_convergence.py::test_c5_family_digest_01` | 相同语义对象的乱序键、乱序遍历、不同 mtime/路径 | 生产计算并与独立 `fcop-family-v1` oracle 比较 | 始终为同一 lowercase SHA-256，排除 mtime/状态/路径 |
| C5-FAMILY-RACE-01 | `test_c5_convergence.py::test_c5_family_race_01` | active Root；两个进程共享同步起点 | 并发执行 Root 离开 active 与 create Branch | 至多一种顺序提交，失败方锁后重读并稳定拒绝/重验 |
| C5-REPORT-RACE-01 | `test_c5_convergence.py::test_c5_report_race_01` | Branch 有旧 REPORT head；两个进程共享同步起点 | 并发 replacement REPORT 与 convergence REVIEW | convergence 只绑定完整旧快照或完整新快照，不得混合 |
| C6-N01 | `test_c6_authorization.py::test_c6_n01` | Profile 认可 issuer 的当前 transition/attempt 授权 REVIEW | 执行受权迁移 | 迁移成功，event 保存 authorization_ref 和证据摘要 |
| C6-R01 | `test_c6_authorization.py::test_c6_r01[...]` | 分别缺授权、actor=ADMIN、wrong subject/edge/attempt | 执行受权迁移 | 对应 REQUIRED/INVALID，零移动且零消费 |
| C6-R02 | `test_c6_authorization.py::test_c6_r02[expired/reused]` | 分别布置过期授权、已消费 single-use 授权 | 再次迁移 | 对应 EXPIRED/REUSED 且状态不变 |
| C6-X01 | `test_c6_authorization.py::test_c6_x01` | 有效授权与响应丢失故障 | 首次提交后用同 ref/digest/transition 重试 | 返回既有结果，不产生第二消费或第二事件 |
| C6-PROFILE-01 | `test_c6_authorization.py::test_c6_profile_01` | `profiles: []` workspace | 执行 T1–T3，再尝试 T4 | Base 边可用；授权边返回 PROFILE_UNAVAILABLE |
| C6-SPOOF-01 | `test_c6_authorization.py::test_c6_spoof_01` | sender/actor=ADMIN 或 host allowlist 命中但无 Profile 证明 | 执行受权迁移 | `AUTHORIZATION_INVALID`，Fail Closed，零消费/零移动 |
| C6-DIGEST-01 | `test_c6_authorization.py::test_c6_digest_01` | 授权引用的 REPORT/REVIEW 已按 byte digest 绑定 | 改变证据任一字节后迁移 | `EVIDENCE_DIGEST_MISMATCH`，旧 ref 不再有效 |
| C7-N01 | `test_c7_idempotency.py::test_c7_n01` | 固定 operation_id 和 normalized request digest | 连续两次 create | 第二次 Existing；task_id/path/digest 相同且零新增事件 |
| C7-R01 | `test_c7_idempotency.py::test_c7_r01` | 同 operation_id，不同 semantic digest | 第二次 create | `OPERATION_ID_CONFLICT` 且原对象 bytes 不变 |
| C7-X01 | `test_c7_idempotency.py::test_c7_x01` | 两进程使用相同 operation_id 和同摘要 | 同步并发真实 create，随后新进程查询/重试 | 仅一个 TASK，全部返回同一结果，重启后可查询 |
| C7-CREATE-01 | `test_c7_idempotency.py::test_c7_create_01` | create 与普通 T2 使用各自合同输入 | 重放 create，再重放 T2 | 仅 create 获公共长期 Existing/conflict 合同 |
| C8-N01 | `test_c8_recovery.py::test_c8_n01` | 单个合法迁移与空 receipt 目录 | 执行 transition | `COMMITTED`、一个权威路径、receipt 可审计 |
| C8-R01 | `test_c8_recovery.py::test_c8_r01` | target 已有不同 bytes | 执行迁移 | `TARGET_ALREADY_EXISTS_DIFFERENT`，source/target 均保留 |
| C8-X01 | `test_c8_recovery.py::test_c8_x01[...]` | 分别在 PREPARED/TARGET_DURABLE/COMMITTED/RESPONSE_LOST 注入确定性故障 | 迁移并恢复 | 仅合同五类结果；可机械恢复或 Fail Closed，不猜测 |
| C8-X02 | `test_c8_recovery.py::test_c8_x02` | 同一 family 的 create/reopen/convergence/archive 操作 | 多进程同步并发真实操作 | family 线性化，失败方重读后返回稳定 gate error |
| C8-X03 | `test_c8_recovery.py::test_c8_x03[...]` | 分歧双副本、损坏 receipt、unsupported FS | 调用生产恢复 | RECOVERY_REQUIRED/UNSUPPORTED_FILESYSTEM，所有证据保留 |
| C8-RETRY-01 | `test_c8_recovery.py::test_c8_retry_01[T4..T7]` | 各授权边已提交但响应丢失 | 同 authorization 重试同边及不同边 | 同边返回既有结果且不二次消费；异边 REUSED |
| C8-STATE-01 | `test_c8_recovery.py::test_c8_state_01[S1..S5]` | 精确构造五种 source/target/receipt 状态 | 对每行调用恢复 | 唯一分类和机械动作逐行符合冻结状态表 |
| C8-INDETERMINATE-01 | `test_c8_recovery.py::test_c8_indeterminate_01` | source/target 缺失或 identity/digest 证据冲突 | 调用生产恢复 | 仅 INDETERMINATE/RECOVERY_REQUIRED，保留证据并 Fail Closed |
| AT-01 | `test_c7_idempotency.py::test_at_01` | 两进程同 operation_id；覆盖同/异摘要两轮 | 并发 create Branch | 同摘要同 Branch；异摘要一成功一 conflict，绝不两个 Branch |
| AT-02 | `test_c8_recovery.py::test_at_02` | active Root；两个进程共享同步起点 | 并发 create Branch 与 Root archive | 线性化后另一方重验，禁止 archived Root 后新增 Branch |
| AT-03 | `test_c5_convergence.py::test_at_03` | Branch 无/有 durable current REPORT 两个阶段 | 并发 REPORT 与 Branch done | done 只能观察到 durable current REPORT |
| AT-04 | `test_c5_convergence.py::test_at_04` | convergence 与 Root archive 并发 | 两进程执行真实 REVIEW/transition | 归档只能消费同一 canonical family digest |
| AT-05 | `test_c8_recovery.py::test_at_05[...]` | 三个提交故障边界 | 真实 transition、恢复、重试 | 五类结果之一；无新对象、重复 event 或不可解释成功 |
| AT-06 | `test_c8_recovery.py::test_at_06[S2/S4/S5]` | 同副本、异副本、损坏证据 | 调用真实恢复 | same 可收敛；different/corrupt 保留并 Fail Closed |
| MCP-SURFACE-01 | `test_mcp_surface_contract.py::test_mcp_surface_01` | canonical snapshot/server/CodeFlowMu catalog | 提取并比较集合 | FCoP 45 项；CodeFlowMu 仅额外 close_issue |
| MCP-PACKAGE-01 | `test_mcp_surface_contract.py::test_mcp_package_01` | 4.0/Legacy 分派合同文本 | 检查 retained/legacy/relay 边界 | unsafe 行为 Fail Closed，Relay 非 Base 必装合同 |
| RELEASE-GATE-01 | `test_mcp_surface_contract.py::test_release_gate_01` | 未通过 spec/Schema/tests/Gate 的发布状态 | 检查发布约束 | build/publish/tag promotion 明确被阻断 |

```yaml
FROZEN_TEST_ID_COVERAGE: 60/60
BEHAVIORAL_UNIQUE_IDS: 54
BEHAVIORAL_PYTEST_NODES: 86
STATIC_FROZEN_IDS: 6
WP1_1_REQUIRED_TEST_IDS: 14/14
T1_T7_GATE_MATRIX: 7/7
RECOVERY_STATE_TABLE: 5/5
WP0_ATOMICITY_SCENARIOS: 6/6
```

## 4. 并发、重启与空壳防护

- 竞态使用 Windows `spawn` 多进程和 Event 屏障；worker 调用真实 driver
  operation，不检查方法签名来冒充提交，不使用 `sleep` 作为同步 oracle。
- C7-X01 与 AT-01 的竞争者使用相同 `operation_id`；同摘要要求同一结果，
  异摘要要求 `OPERATION_ID_CONFLICT`。首次竞争后再创建新进程验证持久化查询。
- `test_meta_stub_guard.py` 向生产 Project 注入同名 `**kwargs` 空壳，分别返回
  `None`；`create_task`、`transition`、`recover_operation` 都必须继续失败。
- `test_static_driver_surface.py` 通过 AST 检查所有冻结合同测试函数均含显式
  Arrange、Act、Assert，并禁止恢复旧 `parallel_surface_probe`。

## 5. 验证命令

所有命令显式绑定当前 worktree 的 `mcp/src` 与 `src`，避免已安装旧包污染。

```text
python -m pytest -q --ignore=tests/conformance/v4
python -m pytest -q tests/conformance/v4/test_c0_contract_authority.py tests/conformance/v4/test_mcp_surface_contract.py tests/conformance/v4/test_static_driver_surface.py tests/conformance/v4/test_meta_stub_guard.py
python -m pytest -q --tb=line tests/conformance/v4/test_c1_workspace.py tests/conformance/v4/test_c2_envelopes.py tests/conformance/v4/test_c3_lifecycle.py tests/conformance/v4/test_c4_relations.py tests/conformance/v4/test_c5_convergence.py tests/conformance/v4/test_c6_authorization.py tests/conformance/v4/test_c7_idempotency.py tests/conformance/v4/test_c8_recovery.py
python -m pytest --collect-only -q tests/conformance/v4
```

完成内容提交与 Manifest 交付、远端 fetch/回读后停止，只请求
`IMPLEMENTATION_AUTHORIZED`，不自行签署。
