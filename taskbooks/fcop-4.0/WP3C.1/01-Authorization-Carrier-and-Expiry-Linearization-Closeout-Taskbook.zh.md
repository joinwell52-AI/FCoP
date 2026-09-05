---
title: FCoP 4.0 WP3C.1 授权载体与过期线性化收口任务书
document_role: EXECUTION_TASKBOOK
status: AUTHORIZED_FOR_WP3C_1_ONLY
execution_authorized: true
authorized_scope: WP3C_1_ONLY
input_head: bd61efeb04d3cfe52b02c433226492e07a525fce
frozen_contract_commit: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
wp3c_authorization_accepted: false
wp3d_authorized: false
main_merge_authorized: false
release_authorized: false
requested_gate: WP3C_AUTHORIZATION_ACCEPTED
---

# FCoP 4.0 WP3C.1 授权载体与过期线性化收口任务书

## 0. 唯一执行授权

本文件只授权修正对 WP3C 远端交付 `bd61efeb04d3cfe52b02c433226492e07a525fce` 的三项审核发现：

1. Authorization REVIEW 类型与生命周期边的绑定过宽；
2. 授权过期只在 evaluator 调用前检查，不能证明消费线性化时仍有效；
3. 恢复时 receipt 的 `profile_ref` 尚未与其绑定的不可变 Authorization REVIEW 重新对齐。

不得进入 WP3D，不得实现 T7、Branch convergence、family digest、公共 recovery/fault API、Schema、MCP、PyPI、规则包、Host、CodeFlowMu、main 或发布。

完成后必须停止并重新请求：

```text
GATE: WP3C_AUTHORIZATION_ACCEPTED
```

## 1. 固定输入

```yaml
REPOSITORY: joinwell52-AI/FCoP
INPUT_HEAD: bd61efeb04d3cfe52b02c433226492e07a525fce
WP3C_CONTENT_COMMIT: 212bee4eebe47f760c36294d629a46a2caa5a8dc
WP3C_MANIFEST_COMMIT: bd61efeb04d3cfe52b02c433226492e07a525fce
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
TASKBOOK_BRANCH: task/fcop-4.0-wp3c.1-authorization-closeout
EXPECTED_REVIEW_BRANCH: review/fcop-4.0-wp3c.1-authorization-closeout
```

必须从 `INPUT_HEAD` 建立新的独立 worktree。不得在 `D:\FCoP` 或原 WP3C worktree 上继续修改。

若输入提交、冻结规范或远端文件摘要不匹配，停止并报告 `INPUT_IDENTITY_MISMATCH`。

## 2. 审核依据

冻结合同的授权载体矩阵：

| 生命周期边 | 可以同时作为 evidence 与 authorization 的 REVIEW | 独立 authorization_ref |
|---|---|---|
| T4 review→done | acceptance + approved，且携带完整授权绑定 | authorization + authorize |
| T5 review→active | rejection + rejected，且携带完整授权绑定 | authorization + authorize |
| T6 done→active | authorization + authorize 可以同时作为所需 REVIEW 与授权 | authorization + authorize |
| T6 done→active，review_ref 为 reopen | reopen + approved 只作所需 REVIEW证据 | 必须另有 authorization + authorize |

禁止行为：

- `reopen` REVIEW 直接充当 `authorization_ref`；
- acceptance REVIEW 为 T5/T6 授权；
- rejection REVIEW 为 T4/T6 授权；
- 任意 REVIEW 仅因包含 `profile_ref`、`issuer_proof` 或 `decision` 就获得跨边授权能力。

冻结依据是 F4.7.1–F4.7.6，尤其 F4.7.2 只给 T4 acceptance 与 T5 rejection 兼任授权的例外。

## 3. 必须修正 R1：Authorization kind-edge矩阵

当前 `src/fcop/v4/authorization.py` 对 authorization_ref 接受：

```text
authorization / acceptance / rejection / reopen
```

但没有把非 authorization 类型限定到对应生命周期边。

实现必须改成显式、封闭的矩阵：

```text
authorization + authorize:
  allowed on T4/T5/T6

acceptance + approved:
  allowed only on T4

rejection + rejected:
  allowed only on T5

reopen:
  never accepted as authorization_ref in WP3C.1
  may remain review_ref evidence for T6
```

未知类型、已知类型但错误边、错误decision全部返回：

```text
AUTHORIZATION_INVALID
```

所有拒绝必须发生在任何 receipt、TASK、REVIEW或其他文件写入之前。

## 4. 必须修正 R2：过期线性化

当前实现先比较 `expires_at`，再调用 trusted evaluator。若 evaluator 在授权有效时开始、在授权过期后返回，当前代码可能继续提交。

必须满足：

1. 首次执行必须在 trusted evaluator 返回之后、任何 PREPARED receipt 写入之前，再次以带时区UTC时钟检查 `expires_at`；
2. 若此时已经过期，返回 `AUTHORIZATION_EXPIRED`；
3. 不得写入 receipt、目标TASK或授权消费event；
4. 不得修改或删除 source TASK、REPORT、REVIEW；
5. 已经提交成功的精确重试不重新执行 evaluator，也不得因重试时授权已过期而否定既有事实；仍按冻结 F4.9.11 返回 Existing；
6. 不得引入公共 clock 参数、公共 API、后台计时器或Runtime状态。

允许增加私有可测试UTC时钟函数，但不得改变公共方法签名。

测试必须使用确定性时钟或同步屏障，不得依赖脆弱的毫秒 sleep 竞态。

## 5. 必须修正 R3：receipt Profile绑定

对带 authorization 的 T4/T5/T6 receipt，恢复验证必须重新解析 receipt 所绑定的 Authorization REVIEW，并证明：

- 文件完整字节摘要等于 `authorization_digest`；
- REVIEW ID等于 `authorization_ref`；
- REVIEW 中的 `profile_ref` 等于 receipt 的 `profile_ref`；
- 若不一致，Fail Closed，不删除 source，不覆盖 target，不补写业务event。

receipt 字段被修改但未改变Authorization REVIEW时，不得继续报告错误的信任来源。

使用现有 Base错误码；不得新增错误码。按现有恢复语义选择 `RECOVERY_REQUIRED` 或 `EVIDENCE_DIGEST_MISMATCH`，并在报告中说明选择依据。

## 6. 必须新增的测试

至少增加以下真实生产入口测试，不得只测driver或辅助函数：

| ID | 场景 | 期望 |
|---|---|---|
| WP3C1-KIND-01 | T6把reopen REVIEW同时作为review_ref和authorization_ref | AUTHORIZATION_INVALID，零写入 |
| WP3C1-KIND-02 | T5使用acceptance REVIEW作authorization_ref | AUTHORIZATION_INVALID，零写入 |
| WP3C1-KIND-03 | T4使用rejection REVIEW作authorization_ref | AUTHORIZATION_INVALID，零写入 |
| WP3C1-KIND-04 | T6使用reopen evidence＋独立authorization REVIEW | 成功 |
| WP3C1-EXP-01 | evaluator返回前有效、返回后已过期 | AUTHORIZATION_EXPIRED，零写入 |
| WP3C1-EXP-02 | 已提交结果在授权过期后精确重试 | Existing；不调用evaluator；不追加event |
| WP3C1-REC-01 | receipt profile_ref与不可变Authorization REVIEW不一致 | Fail Closed；保留全部证据 |
| WP3C1-REG-01 | T4 acceptance兼任授权 | 保持成功 |
| WP3C1-REG-02 | T5 rejection兼任授权 | 保持成功 |
| WP3C1-REG-03 | T6 authorization REVIEW兼任所需REVIEW与授权 | 保持成功 |

不得删除、重命名或放宽既有冻结 Test ID，不得增加 skip/xfail，不得把失败移入driver拦截。

## 7. 允许修改的文件

生产代码仅允许：

```text
src/fcop/v4/authorization.py
src/fcop/v4/lifecycle.py       # 仅在过期线性化需要最小接线时
src/fcop/v4/receipts.py        # 仅用于R3恢复绑定
```

测试仅允许：

```text
tests/test_fcop/test_v4_authorization.py
```

报告与交付：

```text
reports/FCOP-4.0-WP3C.1-CORRECTION-RESULT.md
reports/FCOP-4.0-WP3C.1-AUTHORIZATION-MATRIX.md
reports/FCOP-4.0-WP3C.1-EXPIRY-AND-RECOVERY-PROOF.md
reviews/fcop-4.0/wp3c.1/MANIFEST.md
```

如确需修改其他文件，必须停止并报告，不得自行扩大allowlist。

## 8. 明确禁止

- 修改 `spec/fcop-4.0-spec.md` 或中文版；
- 修改任何Schema或冻结Conformance文件；
- 修改 `src/fcop/project.py`、`src/fcop/v4/creation.py`；
- 新增生产模块；
- 新增公共API、参数或错误码；
- 新增依赖、数据库、索引、watcher、daemon、timer或状态机；
- 修改MCP、CodeFlowMu、PyPI配置、构建与发布文件；
- 实现T7、family digest、convergence、Branch terminal gate；
- 修改main、打tag、发布Release；
- 把本任务扩展为WP3D或WP4。

## 9. 验证

必须从小到大运行并记录真实命令：

1. WP3C.1新增测试；
2. WP3C全部授权测试；
3. WP3B lifecycle与WP3A creation回归；
4. 冻结v4 static/meta与完整behavioral；
5. `tests/test_fcop`；
6. 绑定正确 `PYTHONPATH` 的完整非Conformance回归；
7. 隔离MCP回归；
8. changed-file Ruff、mypy、`git diff --check`；
9. 冻结规范、Schema、Conformance、MCP、CodeFlowMu未修改检查；
10. 原生Windows授权并发、过期边界及response-loss定向验证。

必须报告：

```yaml
WP3C_1_NEW_TESTS:
WP3C_TARGET_NODES:
FROZEN_TEST_IDS:
V3_REGRESSION:
MCP_REGRESSION:
V4_STATIC_META:
V4_BEHAVIORAL:
UNEXPECTED_FAILURES:
```

## 10. GitHub交付

交付必须使用两提交：

1. Content Commit：代码、测试和三份报告；
2. Manifest Commit：只添加 `reviews/fcop-4.0/wp3c.1/MANIFEST.md`。

推送后重新fetch远端分支并验证：

- remote HEAD等于Manifest Commit；
- Content是Manifest的直接父提交；
- `bd61efeb...`是Content祖先；
- 远端交付文件逐项SHA-256匹配；
- 远端main未修改；
- worktree干净。

## 11. 完成条件

只有同时满足以下条件，才可声明WP3C.1完成：

```yaml
AUTHORIZATION_KIND_EDGE_MATRIX: PASS
REOPEN_AS_AUTHORIZATION: REJECTED
POST_EVALUATOR_EXPIRY_CHECK: PASS
EXPIRED_ZERO_WRITE: PASS
EXPIRED_EXACT_RETRY: EXISTING
RECEIPT_PROFILE_BINDING: PASS
WP3C_REGRESSION: PASS
V3_NEW_FAILURES: 0
UNEXPECTED_FAILURES: 0
NEW_PUBLIC_APIS: 0
NEW_RUNTIME_DEPENDENCIES: 0
NEW_BACKGROUND_COMPONENTS: 0
NEW_AUTHORITATIVE_STORES: 0
NEW_STATE_MACHINES: 0
FROZEN_SPEC_FILES_MODIFIED: 0
SCHEMA_FILES_MODIFIED: 0
MCP_IMPLEMENTATION_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0
MAIN_MODIFIED: false
RELEASE_CREATED: false
WP3D_STARTED: false
```

## 12. 强制停止

完成并交付后必须停止，只请求：

```yaml
REQUESTED_GATE: WP3C_AUTHORIZATION_ACCEPTED
```

执行者不得自签Gate，不得进入WP3D或WP4。
