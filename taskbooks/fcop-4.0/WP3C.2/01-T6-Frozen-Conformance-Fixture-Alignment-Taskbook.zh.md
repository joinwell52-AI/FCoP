---
title: FCoP 4.0 WP3C.2 T6冻结符合性夹具对齐任务书
document_role: EXECUTION_TASKBOOK
status: AUTHORIZED_FOR_WP3C_2_ONLY
execution_authorized: true
authorized_scope: WP3C_2_ONLY
input_head: d0d9ec029516b4379dbf74f2167490f4867680c4
frozen_contract_commit: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
wp3c_authorization_accepted: false
wp3d_authorized: false
main_merge_authorized: false
release_authorized: false
requested_gate: WP3C_AUTHORIZATION_ACCEPTED
---

# FCoP 4.0 WP3C.2 T6冻结符合性夹具对齐任务书

## 0. 唯一授权

本任务只允许修正冻结符合性测试 `C3-GATE-01[T6]` 的夹具表达，使其符合已经冻结的F4.7.1–F4.7.2授权合同。

本任务不修改生产代码、不改变Test ID、不改变测试意图、不修改规范或Schema，也不进入WP3D/WP4。

完成后停止并重新请求：

```text
GATE: WP3C_AUTHORIZATION_ACCEPTED
```

## 1. 固定输入

```yaml
REPOSITORY: joinwell52-AI/FCoP
INPUT_HEAD: d0d9ec029516b4379dbf74f2167490f4867680c4
WP3C_1_CONTENT_COMMIT: 3c817d47bda21a4acd5992861d84f5ee4366ccbb
WP3C_1_MANIFEST_COMMIT: d0d9ec029516b4379dbf74f2167490f4867680c4
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
TASKBOOK_BRANCH: task/fcop-4.0-wp3c.2-conformance-alignment
EXPECTED_REVIEW_BRANCH: review/fcop-4.0-wp3c.2-conformance-alignment
```

从INPUT_HEAD建立新的独立worktree。不得在 `D:\FCoP`、WP3C或WP3C.1工作树上修改。

## 2. 已确认冲突

当前远端测试：

```text
tests/conformance/v4/test_c3_lifecycle.py
C3-GATE-01[T6]
```

构造 `review_kind: reopen` REVIEW，然后把同一引用同时传给：

```text
review_ref
authorization_ref
```

冻结合同规定：

- `reopen + approved`可以作为T6所需REVIEW证据；
- T6授权必须由 `authorization + authorize` REVIEW承载；
- 只有T4 acceptance和T5 rejection获得兼任authorization的明确例外；
- reopen不在该例外内。

因此，生产实现拒绝现有夹具是正确行为；测试夹具与冻结规范冲突。

## 3. 唯一允许的测试修正

只修改 `C3-GATE-01[T6]` 的Arrange部分：

1. 保留一个 `review_kind: reopen`、`decision: approved` REVIEW作为 `review_ref`；
2. 另建一个 `review_kind: authorization`、`decision: authorize` REVIEW；
3. 独立Authorization必须绑定：
   - 当前TASK；
   - T6 `done → active`；
   - 当前source attempt；
   - `operation_kind: lifecycle_transition`；
   - `authorization_scope: single_use`；
   - adopted `profile_ref`；
   - 可供可信evaluator验证的 `issuer_proof`；
4. 把第二个REVIEW传给 `authorization_ref`；
5. 完整边仍必须成功提交一次并产生全新attempt；
6. 缺少授权的twin仍必须返回 `AUTHORIZATION_REQUIRED`且零写入。

可以同时修正该文件中把 `authorization_fixture()`生成物误称为“reopen authorization REVIEW”的注释，但不得改变 `C3-N02`行为。

## 4. 不得改变的测试语义

- Test ID仍为 `C3-GATE-01`；
- 参数ID仍包含 `T6`；
- T6完整Gate必须成功；
- T6缺少Authorization必须稳定失败；
- source/target路径、attempt更新和零副作用断言不得减弱；
- 不得增加skip、xfail、条件跳过或driver短路；
- 不得复制一个新Test ID来替代旧红灯；
- 不得把该节点继续记录为expected red。

修正后完整v4预期恢复为：

```yaml
V4_STATIC_META: 27 passed
V4_BEHAVIORAL: 54 passed / 38 inherited deferred
V4_TOTAL: 81 passed / 38 deferred
UNEXPECTED_FAILURES: 0
TASKBOOK_CORRECTED_EXPECTED_RED: 0
```

实际数字如因收集方式不同必须如实报告，但 `C3-GATE-01[T6]` 必须为PASS。

## 5. 允许修改文件

唯一测试文件：

```text
tests/conformance/v4/test_c3_lifecycle.py
```

报告与交付文件：

```text
reports/FCOP-4.0-WP3C.2-CONFORMANCE-CORRECTION.md
reports/FCOP-4.0-WP3C.2-RESULT.md
reviews/fcop-4.0/wp3c.2/MANIFEST.md
```

除上述4个文件外不得修改任何文件。

## 6. 明确禁止

- 修改任何 `src/` 或 `mcp/src/` 生产代码；
- 修改 `spec/fcop-4.0-spec.*`；
- 修改Schema、错误码、driver、fixtures公共辅助文件或其他Conformance文件；
- 修改已有Test ID或删除断言；
- 修改依赖、构建、PyPI、发布配置；
- 修改MCP、CodeFlowMu、main；
- 实现T7、Branch、convergence、family digest或公共recovery；
- 进入WP3D/WP4。

如果只改该测试文件不能使行为与冻结合同同时成立，必须停止并报告 `CONFORMANCE_ALIGNMENT_BLOCKED`，不得扩大范围。

## 7. 验证顺序

必须记录真实命令与结果：

1. 编码前单独运行 `C3-GATE-01[T6]`，证明其因 `AUTHORIZATION_INVALID` 失败；
2. 修改后单独运行同一节点，必须PASS；
3. 运行整个 `test_c3_lifecycle.py`；
4. 运行WP3C/WP3C.1授权测试；
5. 运行完整v4 static/meta与behavioral；
6. 确认60个冻结Test ID名称与数量不变；
7. 运行 `tests/test_fcop`；
8. 使用正确绑定的 `PYTHONPATH` 运行完整非Conformance回归；
9. 运行隔离MCP回归；
10. 运行diff check及文件allowlist检查。

必须证明：

```yaml
C3_GATE_01_T6: PASS
FROZEN_TEST_IDS: 60/60
TEST_IDS_RENAMED: 0
ASSERTIONS_REMOVED: 0
SKIP_XFAIL_ADDED: 0
PRODUCTION_FILES_MODIFIED: 0
WP3C_REGRESSION: PASS
V3_NEW_FAILURES: 0
UNEXPECTED_FAILURES: 0
```

## 8. GitHub交付

必须使用两提交：

1. Content Commit：唯一测试修正＋两份报告；
2. Manifest Commit：只新增 `reviews/fcop-4.0/wp3c.2/MANIFEST.md`。

推送后重新fetch，验证：

- remote HEAD等于Manifest Commit；
- Content是其直接父提交；
-INPUT_HEAD是Content直接父提交；
- 4个交付文件远端SHA-256匹配；
- remote main未修改；
- worktree干净。

## 9. 完成与停止

只有全部条件通过才可声明：

```yaml
WP3C_2_STATUS: COMPLETE
AUTHORIZED_SCOPE: WP3C_2_ONLY
C3_GATE_01_T6: PASS
TASKBOOK_CORRECTED_EXPECTED_RED: 0
FROZEN_TEST_IDS: 60/60
PRODUCTION_FILES_MODIFIED: 0
FROZEN_SPEC_FILES_MODIFIED: 0
SCHEMA_FILES_MODIFIED: 0
MCP_IMPLEMENTATION_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0
MAIN_MODIFIED: false
WP3D_STARTED: false
REQUESTED_GATE: WP3C_AUTHORIZATION_ACCEPTED
```

完成后必须停止。不得自行签署Gate或进入WP3D。
