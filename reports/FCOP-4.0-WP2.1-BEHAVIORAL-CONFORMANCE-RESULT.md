# FCoP 4.0 WP2.1 · 行为符合性测试加强结果

## 1. 结论

```yaml
WP2_1_EXECUTION: COMPLETE
WP2_1_SCOPE_COMPLIANCE: PASS
BEHAVIORAL_CONFORMANCE_CORRECTION: PASS
FROZEN_TEST_ID_COVERAGE: 60/60
BEHAVIORAL_UNIQUE_IDS: 54/54
BEHAVIORAL_PYTEST_NODES: 86
STATIC_AND_META_NODES: 12
TOTAL_COLLECTED_NODES: 98
IMPLEMENTATION_AUTHORIZED: false
WP3_STARTED: false
```

WP2.1 已把 API 存在性/参数兼容性降级为 Static Surface，并将 C1–C8 与
AT-01–AT-06 改为完整语义请求及可观察后置断言。当前 3.2.5 实现下，86 个
行为节点全部保持真实红灯；没有 collection error、skip、xfail、xpass，也
没有行为节点因方法名、参数名或空返回值而变绿。

## 2. 三组最终测试证据

执行环境：`D:\FCoP-wp2.1-behavioral`；`PYTHONPATH` 按顺序显式绑定该
worktree 的 `mcp/src`、`src`。

| 组 | 结果 | 判定 |
|---|---|---|
| v3 完整回归，忽略 v4 目录 | `1225 passed, 2 skipped, 1 warning in 492.06s` | PASS；与冻结基线一致 |
| v4 Static Surface + Meta Guard | `12 passed, 1 warning in 0.20s` | PASS |
| v4 Behavioral Conformance | `86 failed, 1 warning in 23.71s` | EXPECTED RED；0 pass/skip/xfail/collection error |
| v4 全目录收集 | `98 tests collected in 0.06s` | PASS |

唯一 warning 是既有 `importlib.abc.Traversable` Python 3.14 弃用提醒；两项
既有 skip 是 legacy log 目录已迁移以及空参数集，与 WP2.1 无关。

## 3. 阻断意见逐项处置

| 原阻断 | WP2.1 处置 | 证据 |
|---|---|---|
| API/参数探针被算作行为覆盖 | 参数解析仅保留在 driver 的兼容诊断和 Static Surface；行为组只调用完整语义 operation | `driver.py`、`test_static_driver_surface.py` |
| C1-R01 未构造 workspace_id 不一致 | manifest 与请求使用两个确定不同 ID，前后比较全目录 bytes | `test_c1_workspace.py::test_c1_r01` |
| C2 两项共用 write_review 参数探针 | C2-R01 布置非法 EVAL 后调用生产 inspect；C2-R02 分别执行 replacement REPORT 与追加 REVIEW | `test_c2_envelopes.py` |
| C3-GATE-01 未执行 T1–T7 gate | 参数化执行七边，每边含完整正例与移除证据/授权的负例 | `test_c3_lifecycle.py::test_c3_gate_01[T1..T7]` |
| C4 关系语义不足 | 覆盖 parent/subject_ref/references/branch_of、强弱引用、跨 workspace、自环、不唯一和 Branch 深度 | `test_c4_relations.py` |
| C5 只探测 write_report/list_branches | 建立 Root、Branch、attempt、REPORT head、convergence REVIEW、授权和独立 family digest oracle | `test_c5_convergence.py` |
| C6 七项落到同一参数检查 | 分开验证缺失、过期、重复消费、响应丢失、空 Profile、issuer spoof 与 byte digest 改变 | `test_c6_authorization.py` |
| parallel_surface_probe 冒充竞态 | 删除该方法；多进程 worker 在同步屏障后执行真实 operation，并有禁止恢复的 meta assert | `driver.py`、`test_static_driver_surface.py` |
| C7 未使用同一 operation_id | C7-X01/AT-01 的并发请求显式共享同一 ID；分别覆盖同摘要与异摘要 | `test_c7_idempotency.py` |
| C7 缺少重启持久性 | 并发后创建新进程，用同 key/digest 查询/重试既有结果 | `test_c7_idempotency.py::test_c7_x01` |
| C8 未构造五种状态 | S1–S5 分别显式创建 source/target/receipt/摘要组合并核验分类、机械动作和证据保留 | `test_c8_recovery.py::test_c8_state_01` |
| race 没有真实操作 | C5 family/report race、C7 create race、C8 family race 与 AT-01–04 均由多个进程调用生产 operation | `test_c5_convergence.py`、`test_c7_idempotency.py`、`test_c8_recovery.py` |
| 空壳可使测试变绿 | 对同名 `**kwargs` 方法返回 `None` 的 create/transition/recover 三类空壳做反向验证 | `test_meta_stub_guard.py` |
| Normal/Rejection 输入同质 | 正常用完整合法对象并断言提交结果；拒绝用各自非法输入并断言稳定错误与零写入 | C1–C8 行为文件 |
| 60/60 只代表 ID 出现 | 报告分开记录 60 个唯一冻结 ID、54 个行为 ID、86 个行为节点、12 个静态/元节点 | 本报告与计划 §3 |

## 4. 红灯质量

行为 driver 对每个调用执行以下约束：

1. 将完整语义请求交给真实 `fcop.Project` 公开方法；
2. 缺方法或缺少完整请求所需参数时，抛出 `V4_NOT_IMPLEMENTED`；
3. 返回 `None`、缺必要结果字段或无法证明后置条件时，测试失败；
4. 预期拒绝用稳定错误码断言，`V4_NOT_IMPLEMENTED` 不能冒充合同拒绝；
5. 成功必须由返回字段和磁盘事实共同证明，不能仅凭“调用未抛错”；
6. 失败必须验证权威路径、bytes、receipt、事件或消费计数未发生非法变化。

因此 WP3 仅添加同名方法、宽泛参数或 `return None` 无法消除这些红灯。要让
测试变绿，正式实现必须实际满足对应 workspace、信封、生命周期、关系、
收敛、授权、幂等、原子恢复后置条件。

## 5. 关键覆盖计数

```yaml
CORE_C1_C8_NORMAL: 8/8
CORE_C1_C8_REJECTION: 8/8
T1_T7_GATE_MATRIX: 7/7
RELATION_KINDS: 4/4
WP1_1_REQUIRED_TEST_IDS: 14/14
FAMILY_LINEARIZATION_RACES: 4/4
WP0_ATOMICITY_SCENARIOS: 6/6
RECOVERY_STATES: 5/5
IDEMPOTENCY_LAYERS_SEPARATED: 3/3
EMPTY_STUB_GUARD_ACTIONS: 3/3
ARRANGE_ACT_ASSERT_META_AUDIT: PASS
```

WP1.1 旧回执中的 `13/13` 是文档计数漂移；本轮保留全部 14 个真实新增
test ID，不删除任何测试来迎合旧数字。

## 6. 变更边界

```yaml
SPEC_FILES_MODIFIED: 0
SOURCE_FILES_MODIFIED: 0
SCHEMA_FILES_MODIFIED: 0
MCP_IMPLEMENTATION_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0
DEPENDENCY_OR_BUILD_FILES_MODIFIED: 0
MAIN_MODIFIED: false
RELEASE_CREATED: false
```

内容提交只包含 `tests/conformance/v4/**` 和两份
`reports/FCOP-4.0-WP2.1-*.md`。精确内容提交 SHA、Manifest 提交 SHA、远端
HEAD 和每个交付文件 SHA-256 由第二个纯 Manifest 提交记录，以避免报告的
自引用哈希循环。

## 7. Gate 与停止点

```yaml
WP2_1_CONTENT_COMMIT: SELF
WP2_1_CONTENT_COMMIT_EXACT_SHA: RECORDED_BY_reviews/fcop-4.0/wp2.1/MANIFEST.md
WP2_1_MANIFEST_COMMIT_SHA: INTENTIONALLY_NOT_INCLUDED
REQUESTED_GATE: IMPLEMENTATION_AUTHORIZED
IMPLEMENTATION_AUTHORIZED: false
WP3_AUTHORIZED: false
WP3_STARTED: false
```

完成 review 分支 push、fetch 和 GitHub 远端回读核验后立即停止；不合并
main，不创建 Release，不进入 WP3。
