# FCoP 4.0 WP2.1a · Conformance Closeout

## 1. 授权与结论

```yaml
AUTHORIZED_SCOPE: WP2_1A_CONFORMANCE_CLOSEOUT_ONLY
INPUT_COMMIT: 07b525467a8e7639c64c0a06ec08d812247e4514
OUTPUT_BRANCH: review/fcop-4.0-wp2.1a-conformance-closeout
P0_RECEIVED: 3
P0_CLOSED_BY_TEST_CONTRACT: 3/3
FROZEN_SPEC_CHANGED: false
FROZEN_TEST_ID_SET: 60/60_UNCHANGED
IMPLEMENTATION_AUTHORIZED: false
WP3_STARTED: false
```

本轮只加强测试合同，不实现 FCoP 4.0。五个测试文件被定点修改；本文件是
唯一新增报告。规范、正式实现、Schema、MCP、CodeFlowMu、main、版本、依赖、
构建和发布均未修改。

## 2. P0-1 · 机器可识别错误码

`tests/conformance/v4/driver.py::error_code()` 已删除全部异常字符串 token
扫描，只接受异常对象上的非空结构化 `.code` 或 `.error_code` 字段。
`V4_NOT_IMPLEMENTED` 继续不能冒充合同拒绝。

`test_static_driver_surface.py::test_error_code_requires_a_machine_field`
构造两份显示文本相同的异常：

- `ValueError("AUTHORIZATION_INVALID")` 没有机器字段，必须触发
  `AssertionError`；
- 正式 `FcopError` 子类提供 `error_code="AUTHORIZATION_INVALID"`，可以稳定
  提取。

这使自由文本不再是错误合同，符合 F4.10.2。测试不会从异常消息、类名或
正则表达式猜测 Base code。

## 3. P0-2 · Profile evaluator 三态

新增测试边界 `DeterministicProfileEvaluator`。它只记录输入并返回指定三态，
不执行任何 Core 授权或迁移逻辑。生产 transition 必须真实调用该 evaluator，
并自行应用 F4.7.4：

| evaluator 结果 | 合同 ID / node | 预期 | 额外断言 |
|---|---|---|---|
| `AUTHORIZED` | `C6-N01` | T4 成功 | evaluator 被调用一次；传入 `profile:test`、issuer `ME` 与 issuer proof；event 持久绑定 authorization/evidence digest |
| `DENIED` | `C6-R01::test_c6_profile_evaluator_rejects[DENIED]` | `AUTHORIZATION_INVALID` | TASK 仍在 review；零移动、零事件、零消费 |
| `UNKNOWN` | `C6-R01::test_c6_profile_evaluator_rejects[UNKNOWN]` | `AUTHORIZATION_INVALID` | TASK 仍在 review；零移动、零事件、零消费 |

三种场景的 manifest 都采用 `profile:test`，authorization REVIEW 也都包含
该 `profile_ref`。因此仅凭 manifest membership 或 YAML 字段自动信任会被
DENIED/UNKNOWN 用例捕获；即使结果码碰巧正确，未调用 evaluator 也会因调用
记录为空而失败。

## 4. P0-3 · 授权响应丢失与跨迁移复用

`C8-RETRY-01` 继续参数化覆盖 T4/T5/T6/T7。每个节点现在执行三步：

1. 在 `RESPONSE_LOST` 边界提交首次受权迁移；
2. 使用相同 `authorization_ref`、摘要、transition 和证据重试，必须返回
   `Existing`；
3. 使用同一已消费授权请求另一条受权迁移，必须返回结构化
   `AUTHORIZATION_REUSED`。

不同迁移对照固定为：

| 首次迁移 | 同授权再次请求 |
|---|---|
| T4 `review→done` | T5 `review→active` |
| T5 `review→active` | T4 `review→done` |
| T6 `done→active` | T7 `done→archive` |
| T7 `done→archive` | T6 `done→active` |

跨迁移失败前后比较完整 workspace byte snapshot，并重新读取 TASK 权威阶段与
transition event：路径不移动、文件/receipt 不新增、引用该授权的 event 始终
恰好一条。因此同时证明零移动、零新增事件和零二次消费。

## 5. 冻结集合与节点计数

从 `reports/FCOP-4.0-WP1-CONFORMANCE-MATRIX.md` 机械提取仍得到 60 个唯一
冻结 test ID；逐一在测试源码中查找，缺失 0。没有修改规范或增删冻结 ID。
新增节点只是把 C6-N01/C6-R01 的既有合同展开为三态行为。

```yaml
FROZEN_TEST_ID_COVERAGE: 60/60
FROZEN_TEST_IDS_ADDED: 0
FROZEN_TEST_IDS_REMOVED: 0
BEHAVIORAL_UNIQUE_IDS: 54/54
BEHAVIORAL_NODES: 88
STATIC_AND_META_NODES: 13
TOTAL_V4_COLLECTED: 101
T1_T7_GATE_MATRIX: 7/7
RECOVERY_STATES: 5/5
WP0_ATOMICITY_SCENARIOS: 6/6
```

## 6. 最终测试证据

所有命令在 `D:\FCoP-wp2.1a-closeout` 执行，并显式把当前 worktree 的
`mcp/src`、`src` 置于 `PYTHONPATH`。

| 验证组 | 结果 | 判定 |
|---|---|---|
| v3 完整回归，忽略 v4 | `1225 passed, 2 skipped, 1 warning in 282.55s` | PASS，与冻结基线一致 |
| v4 Static/Meta | `13 passed, 1 warning in 2.88s` | PASS |
| v4 完整 Behavioral | `88 failed, 1 warning in 21.76s` | EXPECTED RED；0 pass/skip/xfail/collection error |
| v4 collect-only | `101 tests collected in 1.90s` | PASS |

唯一 warning 是既有 `importlib.abc.Traversable` 弃用提醒。两个 v3 skip 是
legacy log 目录已迁移和空参数集，与本轮修改无关。

## 7. 变更边界

```yaml
TEST_FILES_MODIFIED: 5
REPORT_FILES_ADDED: 1
SPEC_FILES_MODIFIED: 0
SOURCE_FILES_MODIFIED: 0
SCHEMA_FILES_MODIFIED: 0
MCP_IMPLEMENTATION_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0
DEPENDENCY_OR_BUILD_FILES_MODIFIED: 0
MAIN_MODIFIED: false
RELEASE_CREATED: false
```

测试文件：

- `tests/conformance/v4/driver.py`
- `tests/conformance/v4/fixtures.py`
- `tests/conformance/v4/test_c6_authorization.py`
- `tests/conformance/v4/test_c8_recovery.py`
- `tests/conformance/v4/test_static_driver_surface.py`

## 8. 提交、Gate 与停止点

```yaml
WP2_1A_CONTENT_COMMIT: SELF
WP2_1A_CONTENT_COMMIT_EXACT_SHA: RECORDED_BY_reviews/fcop-4.0/wp2.1a/MANIFEST.md
WP2_1A_MANIFEST_COMMIT_SHA: INTENTIONALLY_NOT_SELF_REFERENCED
REMOTE_VERIFICATION: PERFORM_AFTER_PUSH_FROM_REMOTE_OBJECTS
IMPLEMENTATION_AUTHORIZED: false
WP3_AUTHORIZED: false
WP3_STARTED: false
REQUESTED_GATE: IMPLEMENTATION_AUTHORIZED
```

完成内容提交、纯 Manifest 提交、push、fetch、远端 HEAD/提交可达性和 blob
SHA-256 回读核验后立即停止，不合并 main，不创建 Release，不进入 WP3。
