---
document_role: ADMIN_RULING_AND_EXECUTION_TASKBOOK
status: AUTHORIZED_FOR_WP4C_6A_ONLY
authority: ADMIN
execution_authorized: true
authorized_scope: WP4C_6A_HISTORICAL_ASSERTION_ALIGNMENT_AND_WP4C_6_RESUME_ONLY
original_wp4c_6_taskbook_commit: dc4bd62d47c3c422c8e758b588369dd3ed089acd
blocked_delivery_head: 91e64fa0a0ee377335af3226263a1811e1a56c1d
accepted_wp4c_5_head: 8a4e2b175938af8b28e2983161862b49e8650256
wp4c_5_gate_commit: b5c1e11a4fc05b4c659f69ddad09d3290840f86a
frozen_distribution_test_tree: 4f99c7261b63b6db81c500604a231defaca9f14b
implementation_authorized: true
main_merge_authorized: false
release_authorized: false
codeflowmu_write_authorized: false
requested_gate_after_success: WP4C_RULE_DISTRIBUTION_ACCEPTED
---

# FCoP 4.0 WP4C.6a：旧“未实现”断言阶段对齐与 WP4C.6 恢复任务书 v1.0

## 0. ADMIN 裁定

PR #29 在旧 FCoP 回归失败后停止是正确行为。该失败不是生产实现违反冻结规则分发
合同，而是一个 **WP4C.6 之前有效、WP4C.6 实现开始后失效的阶段占位断言**：

```text
tests/test_fcop/test_v4_rule_distribution.py
test_future_positive_capability_is_absent[measure_context]
test_future_positive_capability_is_absent[build_artifacts]
```

原 WP4C.6 任务书明确授权实现 `measure_context` 和 `build_artifacts`，并要求对缺少
必需字段的请求做结构化 Fail Closed。继续要求这两个 v4 动作返回
`toolkit:OPERATION_NOT_IMPLEMENTED`，会把已授权能力伪装成“仍未实现”，与本阶段合同
直接冲突。

因此 ADMIN 裁定：

```yaml
BLOCKED_STOP_CORRECT: true
OLD_ASSERTION_CLASS: PRE_WP4C_6_STAGE_SENTINEL
OLD_ASSERTION_PERMANENT_COMPATIBILITY_CONTRACT: false
FROZEN_CONFORMANCE_CONFLICT: false
ORDINARY_TEST_ALIGNMENT_REQUIRED: true
WP4C_6A_HISTORICAL_ASSERTION_ALIGNMENT_AUTHORIZED: true
RESUMED_SCOPE: ORIGINAL_WP4C_6_ONLY
```

旧断言在 Git 提交历史和 PR #29 中继续作为阶段证据保留；它不再作为当前 v4 行为的
活动回归合同。不得在生产代码中增加兼容分支、feature flag 或特殊输入判断来返回
`OPERATION_NOT_IMPLEMENTED`。

## 1. 唯一允许的旧测试修正

只允许修改下列一个既有普通测试文件：

```text
tests/test_fcop/test_v4_rule_distribution.py
```

只允许把原函数替换为以下阶段对齐断言：

```python
@pytest.mark.parametrize("action", ["measure_context", "build_artifacts"])
def test_wp4c6_positive_capability_requires_complete_request(distribution, action):
    with pytest.raises(V4ProtocolError) as exc:
        call(distribution, action)
    assert exc.value.code == "toolkit:RULE_SELECTION_INVALID"
```

该修正的语义必须同时满足：

1. 两个参数节点仍然存在；
2. `call(...)` 的既有前后快照继续证明零副作用；
3. 缺少 WP4C.6 必需字段时，两个 v4 动作均返回
   `toolkit:RULE_SELECTION_INVALID`；
4. 不允许捕获宽泛异常、不允许接受多个错误码、不允许 skip/xfail；
5. 不允许修改 fixture、`call`、`snapshot` 或其他既有断言；
6. 本裁定显式允许且只允许上述函数名及其两个参数化 Test ID 随语义更新。

历史 Test ID 的变化必须在最终 RESULT 和 Manifest 中逐项列出。不得用删除测试、减少
参数、保留误导性函数名或只改错误消息的方式完成对齐。

## 2. 不得触碰的冻结边界

以下内容继续完全冻结：

- `tests/conformance/rule_distribution_v4/**` 的全部文件、176 个节点、fixture、driver、
  断言和 Test ID；
- Core 规范、规则分发合同、WP4C.5 Gate 和原 WP4C.6 任务书；
- v3 行为。两个 v4-only 动作在 v3 入口仍须 Fail Closed 且零输出；
- MCP 公共表面 46 tools、12 static resources、4 templates；
- Host profile、采用、部署、回滚、Shadow 和 Runtime consumption 语义；
- main、CodeFlowMu、版本号、PyPI、release workflow 和发布状态。

本裁定不是对“不得修改断言/Test ID”的普遍放宽，只对第 1 节准确列出的一个阶段
占位函数构成窄例外。任何第二个既有测试文件或第二处旧断言需要修改，立即停止并
提交新的事实报告。

## 3. 固定输入与本地候选恢复

恢复前必须从 GitHub 回读并核验：

1. 原 WP4C.6 任务书提交
   `dc4bd62d47c3c422c8e758b588369dd3ed089acd`；
2. PR #29 阻断交付 HEAD
   `91e64fa0a0ee377335af3226263a1811e1a56c1d`；
3. PR #29 恰好只有四份报告和一个 Manifest，没有实现文件；
4. 阻断 RESULT 中 11 个本地候选文件的路径、字节数和 SHA-256。

只有本地 `D:\FCoP-wp4c6-distribution-closeout` 中 11/11 候选文件逐字节匹配阻断
RESULT 的清单，且不存在未列出的候选修改时，才允许复用。任何一项不一致都不得
猜测、修补或从工作树现状重新定义候选；必须停止。

PR #29 保持 BLOCKED 历史，不得 force-push、改写、关闭后冒充成功交付或追加实现。
从本任务书固定提交建立新的独立 worktree：

```text
D:\FCoP-wp4c6a-distribution-resume
```

执行分支固定为：

```text
feat/fcop-4.0-wp4c.6a-distribution-resume
```

经 11/11 哈希复核后，将候选字节复制到新 worktree，并执行第 1 节唯一旧测试修正。
不得从 PR #29 的报告性 CI 推断候选实现通过。

## 4. 恢复后的实现范围

除第 1 节的窄例外外，继续逐字遵守原 WP4C.6 任务书
`dc4bd62d47c3c422c8e758b588369dd3ed089acd`。本任务不新增第三个动作，不新增公共
facade、Runtime 依赖、后台组件、权威存储、状态机、数据库、网络服务或通用构建系统。

候选代码仍只实现：

```text
Project.rule_distribution(action="build_artifacts")
Project.rule_distribution(action="measure_context")
```

第 1 节测试转绿只证明“不完整请求被正确拒绝”，不证明两个动作成功实现。成功路径
仍须由冻结 DIST-27/28、普通生产入口测试、制品字节核验和上下文矩阵共同证明。

## 5. 必须从头重跑的验证

在最终稳定候选字节上完整重跑原任务书第 7 节，不得复用阻断前结果代替最终结果：

1. 两个新阶段对齐节点：2/2；
2. DIST-27/28：20/20；
3. Rule Distribution：176/176，0 skip/xfail；
4. v4 Core：119/119；
5. `tests/test_fcop` 全量；
6. `tests/test_fcop_mcp` 隔离全量；
7. FCoP + Core + MCP 串行组合全量；
8. Ruff、mypy、公共表面、source/wheel/sdist/clean-install 19 字节一致性；
9. 安装后真实 stdio MCP 46/12/4；
10. CodeFlowMu 固定 ref 只读 Shadow，零写入；
11. Windows、Linux、macOS 原生矩阵；
12. 新 Draft PR 最终 Manifest HEAD 的全部适用 GitHub Actions 全绿；
13. 远端父链、全部交付文件 SHA-256、fresh LF checkout 和 main 未变。

旧结果可以作为过程历史引用，但最终回执必须明确区分“阻断前证据”和“最终稳定
字节证据”。未触发、pending、cancelled、skipped、neutral 或旧 HEAD 的 CI 均不是 PASS。

## 6. GitHub 交付

新建 Draft PR，base 为承载本任务书的固定 taskbook 分支。不得复用 PR #29。

提交顺序固定为：

1. **Alignment-only commit**：只修改第 1 节的一个普通测试文件；
2. **Content commit**：候选实现、普通新增测试、必要的最小 CI 接线、CHANGELOG 和
   四份最终报告；
3. **Manifest-only commit**：只新增最终
   `reviews/fcop-4.0/wp4c.6a/MANIFEST.md`。

四份最终报告沿用原 WP4C.6 名称。最终 Manifest 必须同时记录原任务书、本裁定、
PR #29 阻断 HEAD、11/11 候选输入摘要、Alignment commit、Content commit、Manifest
commit、全部测试与三平台 CI。

## 7. 强制停止条件

除原 WP4C.6 任务书的停止条件外，出现任一情况立即停止，`REQUESTED_GATE: NONE`：

- 本任务书、PR #29 HEAD 或 11/11 候选摘要不一致；
- 需要修改第 1 节之外的既有普通测试或任何冻结 Conformance；
- 两个不完整 v4 请求不能以同一结构化
  `toolkit:RULE_SELECTION_INVALID` 零效果拒绝；
- 通过生产代码伪造 `OPERATION_NOT_IMPLEMENTED` 来满足历史断言；
- 旧测试回归、v3 行为、46/12/4 表面或既有 156 个分发节点发生回退；
- 任一支持平台未运行原生测试，或最终 Manifest HEAD CI 未全部通过；
- main、CodeFlowMu、发布状态或任何未授权边界发生变化。

## 8. 完成回执

完成后必须停止并提交：

```yaml
WP4C_6A_STATUS: COMPLETE
AUTHORIZED_SCOPE: WP4C_6A_HISTORICAL_ASSERTION_ALIGNMENT_AND_WP4C_6_RESUME_ONLY
ORIGINAL_TASKBOOK_COMMIT: dc4bd62d47c3c422c8e758b588369dd3ed089acd
RULING_TASKBOOK_COMMIT: ""
RULING_TASKBOOK_SHA256: ""
BLOCKED_DELIVERY_HEAD: 91e64fa0a0ee377335af3226263a1811e1a56c1d
CANDIDATE_INPUT_HASHES: 11/11
HISTORICAL_ASSERTION_ALIGNMENT: 2/2
ALIGNMENT_COMMIT: ""
DIST_27: 2/2
DIST_28: 18/18
RULE_DISTRIBUTION_FULL: 176/176
V4_CORE_CONFORMANCE: 119/119
TEST_FCOP: ""
MCP_REGRESSION: ""
COMBINED_REGRESSION: ""
ARTIFACT_MEMBERS: 19/19
ARTIFACT_RAW_BYTE_PARITY: PASS
CONTEXT_MATRIX: 18/18
WINDOWS_NATIVE: PASS
LINUX_NATIVE: PASS
MACOS_NATIVE: PASS
GITHUB_CI_AT_FINAL_HEAD: PASS
MCP_SURFACE: 46_tools_12_static_4_templates
CODEFLOWMU_FILES_MODIFIED: 0
CONTENT_COMMIT: ""
MANIFEST_COMMIT: ""
REMOTE_HEAD: ""
REMOTE_REFETCH_VERIFIED: PASS
DELIVERY_SHA256: ""
MAIN_MODIFIED: false
RELEASE_CREATED: false
WP4C_RULE_DISTRIBUTION_ACCEPTED: false
REQUESTED_GATE: WP4C_RULE_DISTRIBUTION_ACCEPTED
```

不得自行签署 `WP4C_RULE_DISTRIBUTION_ACCEPTED`，不得合并 main、发布或开始下游适配。
