---
stage: WP3E.1
document_role: EXECUTION_TASKBOOK
status: AUTHORIZED_FOR_WP3E_1_ONLY
execution_authorized: true
authorized_scope: WP3E_1_ONLY
core_gate_signed: false
main_merge_authorized: false
release_authorized: false
---

# FCoP 4.0 WP3E.1：Create Digest 与 Gate 校验上下文收口任务书 v1.0

## 0. ADMIN 审核结论

WP3E.0 的提交身份、19 项 Content allowlist、Manifest-only 第二提交、20/20 远端文件以及主体实现边界已经通过审核：

- Recovery 复用唯一 `receipts.classify()` 五状态分类链；
- fault plan 只存在于当前 Project 实例内存；
- cold export 不改变 archive 的 NOW；
- `C6-X01` 只增加局部可信 Profile 初始化；
- 119/119 Conformance、v3 与 MCP 回归证据完整；
- 未增加依赖、后台组件、权威存储、状态机、锁系统或 Base error code。

但 Core Gate 暂不签署，因为发现一项确定的冻结合同偏差：

`src/fcop/v4/creation.py::_plan_create()` 将 Toolkit 临时输入
`references_required_by_gate` 写入 `normalized`，从而进入
`normalized_request_digest`。冻结规范 F4.8.4 明确列出 create-TASK digest
输入，并明确排除 Profile 扩展。这个临时校验开关不是 TASK Core 字段，也不得
改变同一正式请求的持久幂等身份。

本任务只修复这一项。不得重做 WP3E.0，不得扩大到规则包、MCP 或发布。

## 1. 固定输入

```yaml
REPOSITORY: joinwell52-AI/FCoP
INPUT_HEAD: a030eee3b20b7a0d1eef3535b7bf7554a622e1ce
WP3E_0_CONTENT_COMMIT: c5a6de102cd96e7291aa8b4572976571a6152268
WP3E_0_MANIFEST: reviews/fcop-4.0/wp3e.0/MANIFEST.md
WP3E_0_MANIFEST_SHA: a030eee3b20b7a0d1eef3535b7bf7554a622e1ce
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
CONTRACT_CLAUSE: F4.8.4
```

执行前必须确认：

1. 当前任务书 Commit 的直接父提交为 `a030eee3...`；
2. WP3E.0 Content 与 Manifest 是其祖先；
3. 中英文冻结规范仍与 `aec4c2b2...` 一致；
4. 当前 `_plan_create()` 仍包含：
   ```python
   if gate_required:
       normalized["references_required_by_gate"] = True
   ```
5. `references_required_by_gate` 当前没有写入最终 TASK fields；
6. remote main 未被 WP3E.0 修改。

任一事实不符，停止并报告 `INPUT_IDENTITY_MISMATCH`。

## 2. 工作树与 review 分支

从本任务书 Commit 创建干净独立 worktree：

```text
D:\FCoP-wp3e1-create-digest-closeout
```

review 分支固定为：

```text
review/fcop-4.0-wp3e.1-create-digest-closeout
```

不得修改、清理或切换原 `D:\FCoP`，不得 reset、clean、force push。

## 3. 唯一生产修正

唯一允许修改的生产文件：

```text
src/fcop/v4/creation.py
```

必须保持 `references_required_by_gate` 作为一次调用内的布尔校验上下文：

- 非 bool 仍返回 `INVALID_ENVELOPE`；
- 为 true 且 weak reference 未解析时，仍返回 `REFERENCE_UNRESOLVED`；
- 拒绝路径仍为零写入；
- 为 true 且引用有效时，创建行为正常。

必须删除它对持久请求身份的影响。语义上应成为：

```python
gate_required = request.get("references_required_by_gate", False)
if not isinstance(gate_required, bool):
    raise ...

normalized = {
    # 只含 F4.8.4 冻结字段
}

warnings = self._relations(normalized)
if gate_required and warnings:
    raise ...
```

禁止把下列字段加入 `normalized`、operation fact、TASK frontmatter、transition
或 receipt：

```text
references_required_by_gate
```

不得修改 F4.8.4 已冻结的其他 digest 字段、NFC/LF 规范化、排序、默认值或
SHA-256 算法。

## 4. 强制回归测试

唯一允许修改的测试文件：

```text
tests/test_fcop/test_v4_creation.py
```

必须保留现有：

```text
test_gate_required_weak_reference_rejects_without_writes
```

并补充真实生产入口测试，至少证明：

1. 先创建一个可解析的引用目标；
2. 使用固定 `operation_id`、相同 F4.8.4 正式字段和
   `references_required_by_gate=True` 创建 TASK；
3. 再用同一正式请求、同一 `operation_id`，但不携带该临时开关；
4. 第二次返回 `existing=True`；
5. 两次 `task_id/path/digest` 完全相同；
6. 第二次调用前后工作区字节快照完全相同；
7. TASK frontmatter 不包含 `references_required_by_gate`；
8. operation fact/receipt 不包含该字段；
9. 反向顺序（先无开关、后 true）具有相同结果，或用参数化完整覆盖两个顺序；
10. dangling gate-required reference 仍为 `REFERENCE_UNRESOLVED` 且零写入。

该测试必须能在修复前暴露 digest identity 偏差，在修复后通过。不得通过删除
幂等断言、修改 frozen Conformance、skip 或 xfail 达标。

## 5. 允许文件

Content Commit 只允许：

```text
src/fcop/v4/creation.py
tests/test_fcop/test_v4_creation.py
reports/FCOP-4.0-WP3E.1-CREATE-DIGEST-CLOSEOUT.md
```

Manifest Commit 只允许新增：

```text
reviews/fcop-4.0/wp3e.1/MANIFEST.md
```

除上述四个路径外，任何文件变化都必须停止并报告。

## 6. 禁止范围

严格禁止：

- 修改中英文 FCoP 4.0 规范；
- 修改 `tests/conformance/v4/**`；
- 修改 Recovery、Lifecycle、Authorization、family、fault 或 cold export 实现；
- 修改 public-surface snapshot或增加/删除公共 API；
- 修改 Schema、MCP、45 tools、11 resources、3 templates；
- 修改规则包、Host profile、AGENTS.md、CLAUDE.md、.mdc；
- 修改 CodeFlowMu；
- 增加依赖、后台组件、权威存储、operation 目录、状态机、锁或错误码；
- 修改 main、PR merge、tag、Release、PyPI；
- 进入 WP4；
- 自行签署 `FCOP_4_CORE_IMPLEMENTATION_ACCEPTED`。

## 7. 验证要求

依次运行并记录真实命令、退出码与结果：

1. 新增定向 digest 测试修复前红灯证明；
2. `test_gate_required_weak_reference_rejects_without_writes`；
3. 完整 `tests/test_fcop/test_v4_creation.py`；
4. WP3E v4 单元测试；
5. 完整 `tests/test_fcop`；
6. v3/非-v4 回归；
7. 隔离 `tests/test_fcop_mcp`；
8. v4 Static/Meta；
9. v4 Behavioral 119/119；
10. public-surface snapshot；
11. mypy/type check；
12. 授权文件 Ruff 与全仓基线差异；
13. `git diff --check`、UTF-8、LF、无 BOM；
14. 冻结规范与 Conformance SHA 不变；
15. remote main 不变；
16. GitHub 远端回读和 SHA-256。

完成门：

```yaml
CREATE_DIGEST_F4_8_4_EXACT: PASS
GATE_CONTEXT_TRANSIENT_ONLY: PASS
SAME_FORMAL_REQUEST_SAME_DIGEST: PASS
TASK_FIELD_DRIFT: 0
OPERATION_FACT_FIELD_DRIFT: 0
WP3E_TARGET_NODES: 23/23
V4_TOTAL: 119/119
TEST_FCOP: ZERO_FAILURES
V3_NEW_FAILURES: 0
MCP_NEW_FAILURES: 0
UNEXPECTED_FAILURES: 0
PUBLIC_SURFACE_DRIFT: 0
```

GitHub 没有状态检查上下文时必须如实报告
`GITHUB_STATUS_CONTEXTS: NONE`，不得把本地测试冒充云端 CI。

## 8. GitHub 两提交交付

提交链固定：

```text
Taskbook Commit
  → Content Commit
  → Manifest Commit
```

Content Commit 只含三个授权文件。Manifest Commit 只新增一个 Manifest。

推送后重新 fetch，核对：

- 两提交直接父链；
- Taskbook、WP3E.0、WP3D Gate 与冻结合同祖先关系；
- 文件 allowlist；
- 四个交付文件远端字节 SHA-256；
- remote main 未变；
- worktree clean；
- 未使用 force push。

## 9. 停止条件

```text
INPUT_IDENTITY_MISMATCH
DIGEST_FIX_REQUIRES_CONTRACT_CHANGE
FROZEN_CONFORMANCE_CHANGE_REQUIRED
PUBLIC_SURFACE_CHANGE_REQUIRED
RECOVERY_OR_LIFECYCLE_CHANGE_REQUIRED
UNAUTHORIZED_FILE_REQUIRED
UNEXPECTED_V3_REGRESSION
UNEXPECTED_V4_REGRESSION
UNEXPECTED_MCP_REGRESSION
REMOTE_DELIVERY_VERIFICATION_FAILED
```

出现任一条件立即提交阻断报告并停止。

## 10. 最终回执

```yaml
WP3E_1_STATUS: COMPLETE | BLOCKED
AUTHORIZED_SCOPE: WP3E_1_ONLY
TASKBOOK_PATH: taskbooks/fcop-4.0/WP3E.1/01-Create-Digest-Gate-Context-Closeout-Taskbook-v1.0.zh.md
TASKBOOK_COMMIT: <sha>
TASKBOOK_SHA256: <sha256>
INPUT_HEAD: a030eee3b20b7a0d1eef3535b7bf7554a622e1ce
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
WORKTREE: D:\FCoP-wp3e1-create-digest-closeout
BRANCH: review/fcop-4.0-wp3e.1-create-digest-closeout

CREATE_DIGEST_F4_8_4_EXACT: PASS | FAIL
GATE_CONTEXT_TRANSIENT_ONLY: PASS | FAIL
SAME_FORMAL_REQUEST_SAME_DIGEST: PASS | FAIL
TASK_FIELD_DRIFT: 0
OPERATION_FACT_FIELD_DRIFT: 0
PRODUCTION_FILES_MODIFIED: 1
TEST_FILES_MODIFIED: 1
FROZEN_CONFORMANCE_FILES_MODIFIED: 0
PUBLIC_SURFACE_DRIFT: 0

WP3E_TARGET_NODES: 23/23
V4_STATIC_META: 27/27
V4_BEHAVIORAL: 92/92
V4_TOTAL: 119/119
TEST_FCOP: <result>
V3_REGRESSION: <result>
MCP_REGRESSION: <result>
UNEXPECTED_FAILURES: 0

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

CONTENT_COMMIT: <sha>
MANIFEST_COMMIT: <sha>
REMOTE_HEAD: <sha>
REMOTE_PUSHED: true | false
REMOTE_REFETCH_VERIFIED: PASS | FAIL
DELIVERY_SHA256: <matched>/<total>
REMOTE_MAIN_UNCHANGED: true | false
WORKTREE_STATUS: CLEAN | DIRTY_PRESERVED
GITHUB_STATUS_CONTEXTS: <count | NONE>

FCOP_4_CORE_IMPLEMENTATION_ACCEPTED: false
WP4_STARTED: false
MAIN_MODIFIED: false
RELEASE_CREATED: false
REQUESTED_GATE: FCOP_4_CORE_IMPLEMENTATION_ACCEPTED
```

完成远端交付后停止。不得自行进入 WP4。
