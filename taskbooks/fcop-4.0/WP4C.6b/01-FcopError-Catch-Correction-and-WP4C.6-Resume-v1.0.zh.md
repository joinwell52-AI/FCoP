---
document_role: ADMIN_ERRATUM_AND_RESUME_AUTHORIZATION
status: AUTHORIZED_FOR_WP4C_6B_ONLY
authority: ADMIN
execution_authorized: true
authorized_scope: WP4C_6B_EXCEPTION_CATCH_CORRECTION_AND_WP4C_6_RESUME_ONLY
original_wp4c_6_taskbook_commit: dc4bd62d47c3c422c8e758b588369dd3ed089acd
wp4c_6a_ruling_commit: cd0fe4df900c3ff0b34beca957097f87a8d4b150
blocked_pr: 30
blocked_delivery_head: 576bad0025038ee085fc53da46c125143d126bd3
implementation_authorized: true
main_merge_authorized: false
release_authorized: false
codeflowmu_write_authorized: false
requested_gate_after_success: WP4C_RULE_DISTRIBUTION_ACCEPTED
---

# FCoP 4.0 WP4C.6b：`FcopError` 捕获类型勘误与恢复授权 v1.0

## 0. ADMIN 裁定

PR #30 的停止正确。两个阶段对齐节点都已证明：

- `measure_context` 返回精确 `toolkit:RULE_SELECTION_INVALID`；
- `build_artifacts` 返回精确 `toolkit:RULE_SELECTION_INVALID`；
- 既有 `call(...)` 前后快照未失败，两个请求均为零副作用；
- 失败仅来自 WP4C.6a 固定代码片段错误地捕获 `V4ProtocolError`。

当前代码的既有公开错误层级为：

```text
FcopError
├── V4ProtocolError
└── _DistributionError
```

`_DistributionError` 是规则分发 Toolkit 的私有实现类型，直接继承公共基类
`FcopError`，不是 `V4ProtocolError` 的子类。测试不得导入或固定私有
`_DistributionError`；对公共入口应捕获 `FcopError`，再以精确 namespaced code
判断具体失败。

正式裁定：

```yaml
WP4C_6B_EXCEPTION_CATCH_CORRECTION_AUTHORIZED: true
PRODUCTION_BEHAVIOR_CHANGE_AUTHORIZED: false
ERROR_HIERARCHY_CHANGE_AUTHORIZED: false
EXPECTED_EXCEPTION_CLASS: FcopError
EXPECTED_ERROR_CODE: toolkit:RULE_SELECTION_INVALID
PARAMETER_NODES_REQUIRED: 2/2
ZERO_EFFECT_ASSERTION_REQUIRED: true
RESUMED_SCOPE: ORIGINAL_WP4C_6_ONLY
```

## 1. 唯一允许的修改

只允许在：

```text
tests/test_fcop/test_v4_rule_distribution.py
```

的现有函数：

```text
test_wp4c6_positive_capability_requires_complete_request
```

中作以下单行替换：

```diff
-    with pytest.raises(V4ProtocolError) as exc:
+    with pytest.raises(FcopError) as exc:
```

`FcopError` 已由该文件现有 import 提供，不允许因此修改 import、生产代码或错误层级。

必须原样保留：

```python
@pytest.mark.parametrize("action", ["measure_context", "build_artifacts"])
assert exc.value.code == "toolkit:RULE_SELECTION_INVALID"
```

以及既有 `call(...)`、`snapshot(...)` 和全部零副作用断言。不得改为
`Exception`、异常元组、多个可接受错误码、字符串包含判断、skip 或 xfail。

## 2. 固定恢复输入

恢复前必须同时核验：

1. PR #30 仍为 OPEN/Draft，远端 HEAD 精确为
   `576bad0025038ee085fc53da46c125143d126bd3`；
2. PR #30 仅含四份阻断报告和一个 Manifest，不含失败测试或候选实现；
3. 本地原候选与恢复候选继续 11/11 匹配 PR #29 RESULT 清单；
4. 当前失败对齐文件摘要仍为
   `b0a77d2b84d51e435a5dd7b171554e83005023ed1d8e7568fbd5d863a832ad3e`；
5. 除上述 11 个候选文件和该失败对齐文件外没有未列出的候选修改。

任何一项不一致，立即停止，不能从当前工作树重新定义输入。

## 3. PR #30 与提交方式

本次允许继续使用：

```text
D:\FCoP-wp4c6a-distribution-resume
feat/fcop-4.0-wp4c.6a-distribution-resume
Draft PR #30
```

不得重写、squash、force-push 或删除 PR #30 已存在的两份阻断交付提交；它们继续作为
真实历史。承载本勘误的 ADMIN 提交之后，执行者必须追加：

1. **Alignment-only commit**：只包含第 1 节单行测试修正；
2. **Content commit**：原 11 个候选文件与四份最终报告；
3. **Manifest-only commit**：只更新 `reviews/fcop-4.0/wp4c.6a/MANIFEST.md`。

最终 Manifest 必须记录本勘误提交、阻断 HEAD、失败对齐摘要、成功 Alignment commit、
Content commit、Manifest commit 和完整最终验证。

## 4. 恢复验证

先只运行两个阶段对齐节点，必须得到 2/2 通过、0 skip/xfail。随后必须在最终稳定
候选字节上从头执行 WP4C.6a 第 5 节和原 WP4C.6 第 7 节的全部验证，不得拿 PR #29、
PR #30 阻断前结果或 reports-only CI 代替最终证据。

冻结 Rule Distribution 必须继续 176/176，Core 必须继续 119/119；FCoP、MCP、组合
回归、制品/clean-install、真实 stdio 46/12/4、CodeFlowMu 固定 ref 只读 Shadow、
Windows/Linux/macOS 原生矩阵和最终 Manifest HEAD CI 均必须完成并通过。

## 5. 边界与停止条件

本勘误不允许修改：

- 任何 `tests/conformance/rule_distribution_v4/**` 文件、断言、fixture 或 Test ID；
- 生产代码、错误层级、错误码、Core 规范、规则分发合同或其他既有普通测试；
- MCP 公共表面、Host profile、采用/部署/回滚/Shadow 语义；
- main、CodeFlowMu、版本号、PyPI、Release 或发布流程。

单行修正后若两个节点仍非 2/2，或需要任何第二处修正，立即停止并设置：

```yaml
REQUESTED_GATE: NONE
```

全部完成后停止，只请求：

```yaml
WP4C_RULE_DISTRIBUTION_ACCEPTED: false
REQUESTED_GATE: WP4C_RULE_DISTRIBUTION_ACCEPTED
```

不得自行签署 Gate、合并 main、发布或开始 WP4D。
