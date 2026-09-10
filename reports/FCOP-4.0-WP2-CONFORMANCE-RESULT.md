# FCoP 4.0 WP2 · Conformance-First 结果

## 1. 结论

```yaml
WP2_CONTENT_STATUS: READY_FOR_CONTENT_COMMIT
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
CONFORMANCE_MATRIX_COVERAGE: 60/60
WP1_1_REQUIRED_TEST_IDS: 14/14
WP0_ATOMICITY_SCENARIOS: 6/6
V3_REGRESSION_NEW_FAILURES: 0
V4_STATIC_CONTRACT_TESTS: PASS
V4_BEHAVIOR_COLLECTED: 54
V4_BEHAVIOR_PASSED: 1
V4_BEHAVIOR_FAILED: 53
V4_BEHAVIOR_SKIPPED: 0
V4_BEHAVIOR_XFAILED: 0
V4_BEHAVIOR_XPASSED: 0
V4_BEHAVIOR_COLLECTION_ERRORS: 0
FCOP_4_CONTRACT_FROZEN: true
IMPLEMENTATION_AUTHORIZED: false
WP3_STARTED: false
```

WP2 已得到预期的“静态绿灯 + 行为真实红灯”：冻结合同本身可被机械读取且
中英/MCP 计数一致，当前 3.2.5 尚未实现 4.0 行为。红灯未被 skip、xfail、
捕获或删除。

## 2. 环境与导入来源

```text
OS: Windows
PYTHON: C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe
PYTHON_VERSION: 3.12.9
PYTEST_VERSION: 9.0.3
WORKTREE: D:\FCoP-wp2-conformance
BRANCH: review/fcop-4.0-wp2-conformance
PARENT_DELIVERY_COMMIT: 501dfe7c8253e11bb1060768a45b7138d598c243
FCOP_IMPORT: D:\FCoP-wp2-conformance\src\fcop\__init__.py
FCOP_MCP_IMPORT: D:\FCoP-wp2-conformance\mcp\src\fcop_mcp\__init__.py
```

正式命令显式设置 `PYTHONPATH=<worktree>\mcp\src;<worktree>\src`，防止机器上
已安装的 `fcop_mcp` 抢先于 worktree 源码。

## 3. 三组测试的完整命令与结果

### A. 3.2.5 回归

正式命令：

```powershell
$env:PYTHONPATH=(Resolve-Path mcp\src).Path + [IO.Path]::PathSeparator + (Resolve-Path src).Path
python -m pytest -q --ignore=tests/conformance/v4
```

真实结果：

```text
1225 passed, 2 skipped, 1 warning in 341.89s
exit code: 0
V3_REGRESSION_NEW_FAILURES: 0
```

两个 skip 均来自 `tests/test_schemas/test_legacy_files_validate.py`：迁移后的
仓库不存在 legacy `docs/agents/log`，以及由此产生的空参数集。warning 是
Python 3.12 对 `importlib.abc.Traversable` 的既有弃用提示。

首次用未绑定 MCP 源码的根命令运行得到
`1 failed, 1224 passed, 2 skipped`；失败为
`tests/test_fcop_mcp/test_server.py::TestReportsAndIssues::test_report_lifecycle`。
证据显示它导入了 site-packages 的旧 `fcop_mcp`，其 `read_task` 输出缺少
`parent`；worktree 的 `mcp/src/fcop_mcp/server.py` 明确输出该字段。绑定
`mcp/src;src` 后该单点先通过，完整回归恢复为 1225/2。该污染运行不作为
回归裁定，也未通过修改代码规避。

### B. v4 静态合同

```powershell
python -m pytest -q tests/conformance/v4/test_c0_contract_authority.py tests/conformance/v4/test_mcp_surface_contract.py
```

```text
6 passed, 1 warning in 0.04s
exit code: 0
```

通过项：英中条款与 C1–C8/T1–T7 对等、31/31 Base 错误、规范相对 Schema
的行为权威、45 个工具、11 个静态资源、3 个 template、CodeFlowMu 额外
`close_issue` 排除、版本分派/Legacy/发布门。

### C. v4 行为 Conformance

```powershell
python -m pytest -q --tb=no tests/conformance/v4/test_c1_workspace.py tests/conformance/v4/test_c2_envelopes.py tests/conformance/v4/test_c3_lifecycle.py tests/conformance/v4/test_c4_relations.py tests/conformance/v4/test_c5_convergence.py tests/conformance/v4/test_c6_authorization.py tests/conformance/v4/test_c7_idempotency.py tests/conformance/v4/test_c8_recovery.py
```

```text
54 collected
1 passed
53 failed
0 skipped
0 xfailed
0 xpassed
0 collection errors
1 warning
exit code: 1 (expected red light)
```

## 4. 行为红灯逐项证据

| test_id | 条款 | 3.2.5 实际原因 |
|---|---|---|
| C1-N01 | F4.2.1–F4.2.3 | 真实 `fcop/fcop.json` 只有 v3 team/role 字段，无 protocol/version 4.0、workspace_id、encoding、profiles |
| C1-R01 | F4.2.2 | 无 4.0 workspace_id，不能执行 envelope/manifest ID mismatch 的零写入拒绝 |
| C1-FORK-01 | F4.2.4 | `Project.derive_workspace` 不存在 |
| C1-OFFLINE-01 | F4.2.6 | 无 4.0 workspace 声明，无法验证离线边界且不伪称全局唯一 |
| C2-N01 | F4.3.1–F4.3.2 | `write_report` 缺 subject_ref/attempt_id/report_kind/result/references |
| C2-R01 | F4.3.1–F4.3.2 | `write_review` 缺 review_kind/attempt/family/authorization/Profile/references |
| C2-R02 | F4.3.3, F4.3.5 | 无 typed append-only correction REVIEW 合同；现有 human approval 仍是 legacy 面 |
| C3-N01 | F4.4.1–F4.4.3 | 真实七边表包含 active→done、缺 done→active，与 4.0 集合不等 |
| C3-N02 | F4.4.2, F4.6.1 | done→active/T6 不在真实 transition table |
| C3-R02 | F4.4.4 | 真实 transition table 仍允许 active→done |
| C3-R03 | F4.4.6, F4.11.2 | 无 `Project.inspect_state` 4.0 唯一路径/terminal archive 检查面 |
| C3-X01 | F4.4.6, F4.9.4 | `atomic.commit` 无 receipt stage/fault injection 接口 |
| C3-GATE-01 | F4.4.2, F4.4.7 | 真实七边集合与冻结 T1–T7 不同，且无证据/Profile gate 矩阵 |
| C4-N01 | F4.5.1–F4.5.2 | `write_task` 缺 branch_of/operation 合同，四关系未实现 |
| C4-N02 | F4.5.3–F4.5.4 | `Project.list_branches` 不存在 |
| C4-R01 | F4.5.2 | 无 4.0 strong/weak relation validator surface |
| C4-R02 | F4.5.3 | 无 Branch family/depth surface |
| C5-N01 | F4.6.1–F4.6.2 | REPORT 不含 attempt/head 合同 |
| C5-N02 | F4.6.5–F4.6.8 | 无 family enumeration/convergence surface |
| C5-R01 | F4.3.4, F4.6.2 | 无 REPORT_REQUIRED/REPORT_HEAD_AMBIGUOUS head gate |
| C5-R02 | F4.6.1–F4.6.2 | REPORT 不绑定 current attempt |
| C5-R03 | F4.6.6–F4.6.8 | 无 canonical family/convergence validator |
| C5-X01 | F4.6.8, F4.9.5 | 无 family linearization surface |
| C5-BRANCH-01 | F4.6.5 | 无 Branch terminal gate |
| C5-ARCHIVED-01 | F4.6.6–F4.6.8 | 无 family digest，不能证明 Branch 路径变化不改摘要 |
| C5-FAMILY-DIGEST-01 | F4.6.6 | 无 `fcop-family-v1` canonical digest 实现面 |
| C5-FAMILY-RACE-01 | F4.5.4, F4.9.5 | 两同步进程均观察到 `list_branches`/family commit surface 缺失 |
| C5-REPORT-RACE-01 | F4.6.6–F4.6.8, F4.9.5 | 两同步进程观察到 REPORT API 缺 attempt_id/report_kind/references |
| AT-03 | F4.6.2–F4.6.3 | 两同步进程不能建立 attempt-bound REPORT durable-before-done gate |
| AT-04 | F4.6.5–F4.6.8 | 两同步进程观察到 REVIEW API 缺 review_kind/family_digest/references |
| C6-N01 | F4.7.1–F4.7.5 | REVIEW API 缺 Profile 与完整授权绑定 |
| C6-R01 | F4.7.3–F4.7.5 | actor/sender 与 durable Profile authorization 尚未分离 |
| C6-R02 | F4.7.3 | 无 expires/single-use authorization 消费合同 |
| C6-X01 | F4.7.3, F4.9.11 | 无 authorization ref/digest 丢响应稳定重试合同 |
| C6-PROFILE-01 | F4.2.3, F4.7.4, F4.7.7 | 无 profiles 声明和空 Profile 的 T1–T3/T4–T7 分界 |
| C6-SPOOF-01 | F4.7.4–F4.7.6 | 无 Profile 三态 issuer proof，无法关闭 ADMIN/allowlist 伪报 |
| C6-DIGEST-01 | F4.4.5, F4.7.3, F4.7.5 | transition 不保存/复核 evidence 与 authorization 完整字节摘要 |
| C7-N01 | F4.8.1–F4.8.5 | `write_task` 缺 operation_id/operation_kind/normalized digest |
| C7-R01 | F4.8.3–F4.8.4 | 无 durable operation key conflict 合同 |
| C7-CREATE-01 | F4.8.1–F4.8.5, F4.9.8 | 未分开 create 外部幂等、lifecycle 内部恢复、授权重试 |
| C7-X01 | F4.8.2–F4.8.5 | 两真实进程对同语义请求生成两个 TASK，而非同一 durable result |
| AT-01 | F4.8, F4.9.5 | 两真实进程对同语义 create 生成不同 TASK；无同 operation_id 收敛 |
| C8-N01 | F4.9.1–F4.9.4 | `Project.recover_operation` 不存在；legacy session recovery 非此合同 |
| C8-R01 | F4.9.2 | 无 receipt/digest 驱动的目标已存在不同内容分类 |
| C8-X01 | F4.9.1–F4.9.4, F4.9.9 | `atomic.commit` 无 PREPARED/TARGET_DURABLE/COMMITTED fault hook |
| C8-X02 | F4.9.5 | 无完整 family linearization/recovery surface |
| C8-X03 | F4.9.4, F4.9.7 | 无 divergent/corrupt/unsupported FS durable recovery surface |
| C8-RETRY-01 | F4.9.8, F4.9.11 | 无授权迁移的匹配重试与二次消费区分 |
| C8-STATE-01 | F4.9.1, F4.9.9–F4.9.10 | 无固定五状态 recovery classifier |
| C8-INDETERMINATE-01 | F4.9.1, F4.9.4, F4.9.9 | 无不可证明状态的 INDETERMINATE/保留证据 Fail Closed |
| AT-02 | F4.5.4, F4.9.5 | 两同步进程均观察到 Branch/Root family commit surface 缺失 |
| AT-05 | F4.9.1–F4.9.11 | 两同步进程均观察到 durable operation recovery surface 缺失 |
| AT-06 | F4.9.2–F4.9.4 | 无 source/target/receipt 摘要分类与保留证据恢复 |

所有上表 driver 红灯均包含 `test_id`、F4 条款、expected/actual 和
`code=V4_NOT_IMPLEMENTED`；`C3-N01`/`C3-GATE-01` 是真实表集合差异断言，
不是 import 或 collection failure。

## 5. 3.2.5 偶然满足与 WP3 缺口

`C3-R01` 偶然通过：3.2.5 已拒绝 inbox→archive 这一非法边。该单项通过不
表示 C3 合同完成；4.0 仍需移除 active→done、增加 done→active、落实
T1–T7 的 REPORT/REVIEW/Profile/attempt gate。

WP3 若获授权，需要由正式实现分别补齐：C1 4.0 workspace 身份与 fork；C2
四类 typed append-only envelope；C3 唯一路径与七边 gate；C4 四关系与
Branch；C5 attempt/report head/family convergence；C6 durable Profile
authorization；C7 create operation record；C8 receipt、五状态恢复和完整
family linearization。WP2 不实现这些内容。

## 6. 覆盖与计数漂移

机械提取冻结矩阵得到 60 个唯一 test_id；测试源码逐项出现 60 个，缺失 0。

```yaml
CONFORMANCE_MATRIX_COVERAGE: 60/60
WP1_1_REQUIRED_TEST_ID_DECLARED: 13
WP1_1_REQUIRED_TEST_ID_OBSERVED: 14
CLASSIFICATION: DOCUMENT_COUNT_DRIFT
CONTRACT_SEMANTICS_AFFECTED: false
WP1_1_REQUIRED_TEST_IDS: 14/14
WP0_ATOMICITY_SCENARIOS: 6/6
```

## 7. 测试基础设施问题

`ROOT_PYTEST_IMPORT_AMBIGUITY` 仍是环境注意项：根 `pyproject.toml` 只把
`src` 加入 pytest 路径，没有把 `mcp/src` 加入，因此已安装的旧
`fcop_mcp` 可能污染根级 MCP 测试。WP2 没有权限修改构建/pytest 配置；
正式命令用显式 `PYTHONPATH` 完全规避并验证了 worktree 导入来源。除此之外
没有 collection、spawn、临时目录或网络问题。

## 8. 变更边界与提交标识

```yaml
FROZEN_SPEC_FILES_MODIFIED: 0
SOURCE_FILES_MODIFIED: 0
SCHEMA_FILES_MODIFIED: 0
MCP_IMPLEMENTATION_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0
DEPENDENCY_OR_BUILD_FILES_MODIFIED: 0
WP2_CONTENT_COMMIT: SELF
WP2_CONTENT_COMMIT_EXACT_SHA: RECORDED_BY_reviews/fcop-4.0/wp2/MANIFEST.md
WP2_MANIFEST_COMMIT_SHA: INTENTIONALLY_NOT_INCLUDED
```

`SELF` 表示本报告与测试、计划共同属于内容提交。Git commit SHA 依赖本报告
字节，无法在不改变自身 SHA 的情况下把最终 SHA 写回同一提交；因此精确
内容提交 SHA 按两提交协议外置到随后唯一的 Manifest 提交和最终回执。这
避免伪造、自引用循环或让 Manifest 提交夹带结果报告修改。

## 9. Gate 与停止点

内容与 Manifest 提交、远端 push/fetch/回读尚由后续交付步骤完成。完成后仅
请求：

```yaml
REQUESTED_GATE: IMPLEMENTATION_AUTHORIZED
IMPLEMENTATION_AUTHORIZED: false
WP3_STARTED: false
```
