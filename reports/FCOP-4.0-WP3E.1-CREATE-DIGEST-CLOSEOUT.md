---
stage: WP3E.1
document_role: EXECUTION_RESULT
status: COMPLETE
authorized_scope: WP3E_1_ONLY
gate_self_signed: false
requested_gate: FCOP_4_CORE_IMPLEMENTATION_ACCEPTED
---

# FCoP 4.0 WP3E.1 · Create Digest 与 Gate 上下文收口

## 1. 结论

本轮只修复 `references_required_by_gate` 错误进入
`normalized_request_digest` 的冻结合同偏差。该字段仍由 `create_task()` 接受为
一次调用内的布尔校验上下文，但不再进入 normalized request、TASK、operation
fact 或 receipt。同一 F4.8.4 正式请求在携带或省略该临时开关时具有相同 digest
和持久幂等身份。

```yaml
WP3E_1_STATUS: COMPLETE
AUTHORIZED_SCOPE: WP3E_1_ONLY
CREATE_DIGEST_F4_8_4_EXACT: PASS
GATE_CONTEXT_TRANSIENT_ONLY: PASS
SAME_FORMAL_REQUEST_SAME_DIGEST: PASS
TASK_FIELD_DRIFT: 0
OPERATION_FACT_FIELD_DRIFT: 0
UNEXPECTED_FAILURES: 0
```

## 2. 输入身份

| 核验 | 结果 |
|---|---|
| Taskbook commit | `a2b32633708c22196a32f064d9850755634c25e7` |
| Taskbook SHA-256 | `8fd6854d97bce14a4d8098a295ba0170ff7d921631c4b860139f80d23749eeb9`，PASS |
| 直接父提交 | `a030eee3b20b7a0d1eef3535b7bf7554a622e1ce`，PASS |
| WP3E.0 Content/Manifest 祖先 | `c5a6de10…` / `a030eee3…`，PASS |
| 冻结合同祖先 | `aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6`，PASS |
| 中英文冻结规范 blob | 与冻结合同提交一致，PASS |
| WP3E.0 进入 remote main | 否，PASS |
| remote main 基线 | `68dbeb15f4e7f84e1d03f907be9fa66c2265843e` |

上述事实由 `git rev-parse`、`git merge-base --is-ancestor`、`git hash-object`
和重新 fetch `origin/main` 的输出核验。原 `D:\FCoP` 的未跟踪及历史现场未被
清理、迁移、切换分支或覆盖；执行发生在任务书指定的独立 worktree。

## 3. 修正与测试强度

生产修正仅删除 `_plan_create()` 中把临时 Gate 开关复制进 `normalized` 的两行。
以下行为保持不变：

- 非布尔开关返回结构化 `INVALID_ENVELOPE`；
- Gate 为 true 且 weak reference 未解析时返回 `REFERENCE_UNRESOLVED`；
- 上述拒绝路径零写入；
- Gate 为 true 且引用有效时正常创建。

新增真实生产入口回归覆盖两个顺序：先携带开关后省略，以及先省略后携带。
每个顺序均先创建可解析引用目标，再以同一 `operation_id` 和相同 F4.8.4 字段
重试；断言第二次 `existing=True`，两次 `task_id/path/digest` 完全一致，重试前后
工作区逐字节快照不变，并检查 TASK、operation fact/receipt 均无临时开关字段。
另加入非布尔开关拒绝断言，原 dangling-reference 零写入测试完整保留。

修复前红灯命令：

```text
python -m pytest tests/test_fcop/test_v4_creation.py -k "gate_context_does_not_change_create_digest_or_retry" -q
exit 1: 2 failed, 95 deselected
两个失败均为 OPERATION_ID_CONFLICT，分别覆盖两个调用顺序。
```

修复后定向命令：

```text
python -m pytest tests/test_fcop/test_v4_creation.py -k "gate_context_does_not_change_create_digest_or_retry or gate_required_weak_reference_rejects_without_writes or rejection_zero_writes" -q
exit 0: 15 passed, 83 deselected
```

## 4. 完整验证

| 命令/验证面 | 真实结果 |
|---|---|
| `pytest tests/test_fcop/test_v4_creation.py -q` | 98 passed |
| 全部 `tests/test_fcop/test_v4_*.py` | 235 passed |
| `pytest tests/test_fcop -q` | 1143 passed |
| `pytest tests/test_fcop -q -k "not v4"` | 908 passed / 235 deselected |
| 隔离 MCP，`PYTHONPATH=mcp/src;src` | 80 passed |
| v4 Static/Meta | 27 passed |
| v4 Behavioral | 92 passed |
| v4 完整 Conformance | 119 passed |
| v4 collect-only | 119 collected |
| public-surface snapshot | 4 passed；漂移 0 |
| `mypy src/fcop` | 39 source files，0 issues |
| Ruff：两个授权 Python 文件 | PASS |
| 全仓 Ruff | 10 个继承问题；授权文件新增问题 0 |

所有 pytest 运行只有既有的 `importlib.abc.Traversable` 弃用警告，无测试失败。
本机为 Windows 原生环境；Linux/macOS 未在本轮原生运行。

## 5. 范围与不变量

```yaml
WP3E_TARGET_NODES: 23/23
V4_STATIC_META: 27/27
V4_BEHAVIORAL: 92/92
V4_TOTAL: 119/119
TEST_FCOP: 1143/1143
V3_REGRESSION: 908 passed / 235 deselected
MCP_REGRESSION: 80/80

PRODUCTION_FILES_MODIFIED: 1
TEST_FILES_MODIFIED: 1
FROZEN_CONFORMANCE_FILES_MODIFIED: 0
PUBLIC_SURFACE_DRIFT: 0
NEW_PUBLIC_APIS: 0
NEW_PRODUCTION_MODULES: 0
NEW_RUNTIME_DEPENDENCIES: 0
NEW_BACKGROUND_COMPONENTS: 0
NEW_AUTHORITATIVE_STORES: 0
NEW_STATE_MACHINES: 0
NEW_LOCK_SYSTEMS: 0
NEW_BASE_ERROR_CODES: 0
FROZEN_SPEC_FILES_MODIFIED: 0
SCHEMA_FILES_MODIFIED: 0
MCP_IMPLEMENTATION_FILES_MODIFIED: 0
RULE_PACKAGE_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0
WP4_STARTED: false
MAIN_MODIFIED: false
RELEASE_CREATED: false
```

Content/Manifest 提交身份、四个交付文件的远端 SHA-256、远端 main 稳定性与
GitHub status contexts 由第二提交的
`reviews/fcop-4.0/wp3e.1/MANIFEST.md` 固定并在 push 后回读核验。本报告只请求
`FCOP_4_CORE_IMPLEMENTATION_ACCEPTED`，不自行签署 Gate。
