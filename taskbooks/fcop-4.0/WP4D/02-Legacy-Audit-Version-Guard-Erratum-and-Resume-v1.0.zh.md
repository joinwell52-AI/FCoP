# FCoP 4.0 WP4D：旧审计测试版本前置条件定点勘误与恢复授权 v1.0

```yaml
document_role: EXECUTION_ERRATUM
execution_authorized: true
authorized_scope: WP4D_AUDIT_GUARD_ONLY_AND_WP4D_RESUME
parent_taskbook_commit: cbdc60a92a02b9e2eb0c1c6e2e93f74c335407f9
blocked_implementation_head: 893e5c55f9f7ea433c6c518c76534218a4cf9570
draft_pr: https://github.com/joinwell52-AI/FCoP/pull/31
blocker: LEGACY_AUDIT_MINOR_ONLY_GUARD_SKIPS_RC
completion_gate: FCOP_4_RC_ACCEPTED
main_merge_authorized: false
rc_publish_authorized: false
stable_release_authorized: false
pypi_publish_authorized: false
github_release_authorized: false
mcp_registry_publish_authorized: false
zenodo_publish_authorized: false
codeflowmu_write_authorized: false
```

## 1. ADMIN 裁定

确认授权定点修正：

```text
tests/test_fcop/test_audit.py::test_scan_outdated_role_docs_far_behind
```

当前前置条件只读取安装版本的 minor：`4.0.0rc1` 被解释为 minor `0`，从而在真正的回归断言之前错误 skip。该夹具引用 `v1.0`；相对 `4.0.0rc1` 已跨 major 落后，生产扫描器也按 major/minor 判断。因此这是测试准入条件未随候选版本升级而对齐，不是生产行为失败。

允许修正后恢复执行原 WP4D 任务书。此前 `WP4D_STATUS: BLOCKED` 与 `REQUESTED_GATE: NONE` 记录保持为历史事实，不得改写成当时已完成。

## 2. 唯一允许的非报告修改

只允许修改：

```text
tests/test_fcop/test_audit.py
```

且只允许修改上述 Test ID 内的版本前置条件，使其以 `(major, minor)` 判断安装版本是否达到 `1.2`。推荐等价实现：

```python
pkg_major, pkg_minor = (int(part) for part in pkg_ver.split(".")[:2])
if (pkg_major, pkg_minor) < (1, 2):
    pytest.skip("Installed fcop version < 1.2; gap cannot be > 1")
```

允许同步调整紧邻该判断、且只描述前置条件的注释或 skip message。不得引入新的运行时依赖。

## 3. 必须冻结的测试内容

以下内容必须保持不变：

- Test ID：`test_scan_outdated_role_docs_far_behind`
- fixture 参数：`tmp_path`
- 角色目录与文件名：`fcop/shared/roles/DEV.md`
- 夹具正文中的 `v1.0`
- `Project(tmp_path)` 调用
- `_scan_outdated_role_docs()` 调用
- 最终断言及其消息：

  ```python
  assert violations, "Role doc only referencing v1.0 should trigger RULE_DOC_DRIFT"
  ```

不得把测试改成仅验证“没有 skip”，不得 monkeypatch 生产扫描结果，不得调整生产扫描器，不得新增 xfail/skip/条件豁免。

## 4. 仍然冻结的范围

本勘误不授权修改：

- `src/**` 或 `mcp/src/**` 的任何生产行为；
- `specs/**`、Conformance、19 个权威候选文件或 21 个冻结文件；
- 其他既有测试、Test ID、夹具、阈值或断言；
- `.github/workflows/release.yml`、`mcp/server.json`、`CITATION.cff`；
- legacy v3 bundled rules、`AGENTS.md`、`CLAUDE.md`、`.cursor/**`；
- CodeFlowMu 的任何内容；
- `main`、tag、PyPI、GitHub Release、MCP Registry 或 Zenodo。

原 WP4D 任务书已授权的候选内容、测试、脚本、RC workflow、第三方示例、文档、报告和 Manifest 范围继续有效；本勘误只增加上述一个旧测试函数的定点修改权。

## 5. 恢复顺序

执行人必须在现有实现分支和 Draft PR #31 上续作，不得新开平行实现或丢弃阻断现场。

1. 从远端固定阻断 HEAD `893e5c55f9f7ea433c6c518c76534218a4cf9570` 验证父链和干净工作树。
2. 只提交第 2 节授权的定点测试修正。
3. 单独执行目标节点；必须为 `1 passed / 0 failed / 0 skipped`。
4. 重跑候选身份与依赖检查；必须保持 `14/14`。
5. 重跑全量回归；不得沿用修改前 `1912/1912` 作为修改后结果，且不得出现该节点 skip。
6. 全量成功后，继续完成原任务书尚未运行的四制品构建、`4/4` 可复现性、twine、wheel/sdist、12 组合 consumer、Python-only/MCP-only、response-loss、crash recovery、3.2.5 零漂移、Host 规则分发与 CodeFlowMu `14/14` 只读 shadow。
7. 在最终 Manifest HEAD 完成全部适用 CI；未运行、skip、queued、in progress、cancelled 均不得记为通过。
8. 更新六份报告、JUnit 和 Manifest，明确区分阻断前证据与恢复后重新执行证据。

## 6. 提交与远端证据

定点修正必须形成独立提交，提交中只能包含：

```text
tests/test_fcop/test_audit.py
```

后续候选内容、证据、Manifest 继续遵守原任务书的提交分层。若最终 Manifest 后再修改候选或测试内容，必须重新跑受影响的全部验证并重新收口。

最终回执必须新增：

```yaml
erratum_commit: <this-taskbook-commit>
resume_base: 893e5c55f9f7ea433c6c518c76534218a4cf9570
audit_guard_fix_commit: <single-file-commit>
audit_test_id_preserved: true
audit_fixture_preserved: true
audit_assertion_preserved: true
audit_target_node: 1/1
audit_target_skips: 0
```

所有最终交付文件必须从远端 Manifest HEAD 逐项回读并核验 SHA-256；不得用本地值代替远端值。

## 7. 停止条件

若定点修改后目标节点仍 skip/fail，或需要改变夹具、断言、生产代码、规范、Conformance、发布面、main 或 CodeFlowMu，立即停止：

```text
WP4D_STATUS: BLOCKED
REQUESTED_GATE: NONE
```

只有原 WP4D 全部验收项在新的最终固定 HEAD 上通过，才可停止并请求：

```text
WP4D_STATUS: COMPLETE
REQUESTED_GATE: FCOP_4_RC_ACCEPTED
RC_PUBLISH_AUTHORIZED: FALSE
MAIN_MERGE_AUTHORIZED: FALSE
```

执行人不得自行签署 Gate，不得在 Gate 后自动合并或发布。
