---
stage: WP2.1
delivery_role: NON_AUTHORITATIVE_REVIEW_MANIFEST
status: REVIEW_READY
branch: review/fcop-4.0-wp2.1-behavioral-conformance
input_branch: review/fcop-4.0-wp2-conformance
input_commit: decfcc33ff4b26801417f4f68a75e6fdf493dd07
parent_commit: decfcc33ff4b26801417f4f68a75e6fdf493dd07
content_commit: 5325f0127a5987045228cb2e82a25755de71cf18
delivery_head: SELF
contract_frozen: true
implementation_authorized: false
wp3_authorized: false
release_authorized: false
codeflowmu_change_authorized: false
matrix_coverage: 60/60
behavioral_unique_ids: 54/54
behavioral_nodes: 86
wp1_1_required_test_ids: 14/14
wp0_atomicity_scenarios: 6/6
requested_gate: IMPLEMENTATION_AUTHORIZED
---

# FCoP 4.0 WP2.1 GitHub Review Manifest

本清单只交付 WP2.1 行为符合性测试修订证据，不签署 Gate，不授权 WP3、
实现、Schema、MCP、发布、迁移或 CodeFlowMu 变更。

`delivery_head: SELF` 表示本文件所在的 Manifest 提交就是交付 HEAD。提交 SHA
由本文件 bytes 决定，无法无穷自引用；精确 Manifest SHA 和远端 HEAD 在 push
后通过远端对象回读，并在标准回执中返回。

## 内容提交文件 SHA-256

SHA-256 基于 `content_commit` 中的 committed blob 字节计算，不使用可能受
Windows 换行转换影响的工作树副本。Manifest 不列自身摘要，避免自引用哈希
循环。

| SHA-256 | 文件 |
|---|---|
| `07f3f7b2c5f86772c20f21b3fce8563777eda353609aabe8db1e82d337e49b2b` | `reports/FCOP-4.0-WP2.1-BEHAVIORAL-CONFORMANCE-PLAN.md` |
| `38142aeb4b9233eed71d2b0e858984df3a3e5b3e0d1c4a264e51a8c719da341f` | `reports/FCOP-4.0-WP2.1-BEHAVIORAL-CONFORMANCE-RESULT.md` |
| `f76152a5267724195be038a8753786628e9ffb09fd357b704e210ea306203966` | `tests/conformance/v4/conftest.py` |
| `711469471a3ca1775fe716903da53cf41760a29c30e124b56fe03be0aa2921f0` | `tests/conformance/v4/driver.py` |
| `1ec22dc380989fcd086f0b378e4e11ab63ae0e3aa2e97d1e61a61a81cac53fc5` | `tests/conformance/v4/fixtures.py` |
| `6885d636fc5ddc15b4543a96d4c3f385e3b28bf3d570688ea1c2116de1c2e4ae` | `tests/conformance/v4/scenarios.py` |
| `b28dd5166e4351dad7d1e82b738a00875e098799451a13212eee6a70602d02de` | `tests/conformance/v4/test_c0_contract_authority.py` |
| `543ed48f60ac4daede7c380a5a3ac8c80fff6f2714a88f16527b3f46b93cfac6` | `tests/conformance/v4/test_c1_workspace.py` |
| `4791e184bea6f401b02e6d8c77170b1ecdbff03c39e50201c0d4156c0c6b9b46` | `tests/conformance/v4/test_c2_envelopes.py` |
| `4f51d39e7c02cda7d69917e4242fbe3ca0cb28789445911dbae67918e45af213` | `tests/conformance/v4/test_c3_lifecycle.py` |
| `d94c7885a140e07ba59e6697aa24c83a0ed40c17f5defbe4f56b2a2dc082b762` | `tests/conformance/v4/test_c4_relations.py` |
| `6da7e3b86c8ea91d51f7d16c1699a04074592cdae6f17bbe12aa340f8c3883b5` | `tests/conformance/v4/test_c5_convergence.py` |
| `63a1324ea88c279b3115084d177c5569a0ad0afba3245d928c5efaea93a8585b` | `tests/conformance/v4/test_c6_authorization.py` |
| `bc819a5db1daba58a97eaad3056e38a31e01e705357e4cad55ed0d8117125684` | `tests/conformance/v4/test_c7_idempotency.py` |
| `7050b8fcc21a50d3d48b295ad95e2af465e8fea5bcb40947bce2df00a6e512b3` | `tests/conformance/v4/test_c8_recovery.py` |
| `60b5f70c1ea2b588b58d7caec96ef712d956a0e146459845c91bd271d8deb1fa` | `tests/conformance/v4/test_mcp_surface_contract.py` |
| `28229ab929752f5c5d113d7dc0bedb5f4e7a992f448701a5a905b0c06d30592e` | `tests/conformance/v4/test_meta_stub_guard.py` |
| `22145567c8bdd496359f09558e1be144980c2fd083ef316e56ffe5c9d259345c` | `tests/conformance/v4/test_static_driver_surface.py` |

## 测试证据

```yaml
v3_regression: 1225 passed, 2 skipped, 1 warning in 492.06s
v3_regression_new_failures: 0
v4_static_and_meta: 12 passed, 1 warning in 0.20s
v4_behavior_collected: 86
v4_behavior_passed: 0
v4_behavior_failed: 86
v4_behavior_skipped: 0
v4_behavior_xfailed: 0
v4_behavior_xpassed: 0
v4_behavior_collection_errors: 0
v4_all_collected: 98
behavioral_unique_test_ids: 54/54
frozen_test_id_coverage: 60/60
```

`EXPECTED_RED_TEST_IDS`：

```text
[C1-N01, C1-R01, C1-FORK-01, C1-OFFLINE-01,
 C2-N01, C2-R01, C2-R02,
 C3-N01, C3-N02, C3-R01, C3-R02, C3-R03, C3-X01, C3-GATE-01,
 C4-N01, C4-N02, C4-R01, C4-R02,
 C5-N01, C5-N02, C5-R01, C5-R02, C5-R03, C5-X01,
 C5-BRANCH-01, C5-ARCHIVED-01, C5-FAMILY-DIGEST-01,
 C5-FAMILY-RACE-01, C5-REPORT-RACE-01,
 C6-N01, C6-R01, C6-R02, C6-X01, C6-PROFILE-01, C6-SPOOF-01,
 C6-DIGEST-01,
 C7-N01, C7-R01, C7-X01, C7-CREATE-01,
 C8-N01, C8-R01, C8-X01, C8-X02, C8-X03, C8-RETRY-01,
 C8-STATE-01, C8-INDETERMINATE-01,
 AT-01, AT-02, AT-03, AT-04, AT-05, AT-06]
```

```yaml
UNEXPECTED_GREEN_BEHAVIOR_IDS: []
UNEXPECTED_FAILURE_IDS: []
WP1_1_REQUIRED_TEST_ID_DECLARED_IN_OLD_RECEIPT: 13
WP1_1_REQUIRED_TEST_ID_OBSERVED: 14
CLASSIFICATION: DOCUMENT_COUNT_DRIFT
CONTRACT_SEMANTICS_AFFECTED: false
```

## 行为强度证据

- 60 个冻结 ID 均在计划中逐项记录 Arrange、Act、Assert。
- 54 个行为 ID 展开为 86 个执行节点；Normal 与 Rejection 使用不同输入和
  不同后置条件。
- `V4_NOT_IMPLEMENTED` 只表示正式实现缺失，不能作为合同拒绝错误通过测试。
- 成功结果必须同时满足返回字段与磁盘事实；`None`、缺字段或同名空壳失败。
- C3-GATE-01 展开 T1–T7 七边；C8-STATE-01 展开 S1–S5 五状态。
- race 使用多进程同步执行真实 operation；C7/AT-01 使用相同 operation_id，
  并在新进程中验证重启后既有结果。
- `parallel_surface_probe` 已移除，并有 meta guard 防止回归。

## 交付边界

```yaml
SPEC_FILES_MODIFIED: 0
SOURCE_FILES_MODIFIED: 0
SCHEMA_FILES_MODIFIED: 0
MCP_IMPLEMENTATION_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0
DEPENDENCY_OR_BUILD_FILES_MODIFIED: 0
MAIN_MODIFIED: false
RELEASE_CREATED: false
REMOTE_VERIFICATION: PERFORM_AFTER_PUSH_FROM_REMOTE_OBJECTS
IMPLEMENTATION_AUTHORIZED: false
WP3_AUTHORIZED: false
WP3_STARTED: false
REQUESTED_GATE: IMPLEMENTATION_AUTHORIZED
```
