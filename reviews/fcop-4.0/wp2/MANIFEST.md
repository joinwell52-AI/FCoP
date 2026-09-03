---
stage: WP2
delivery_role: NON_AUTHORITATIVE_REVIEW_MANIFEST
status: REVIEW_READY
branch: review/fcop-4.0-wp2-conformance
frozen_contract_commit: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
parent_delivery_commit: 501dfe7c8253e11bb1060768a45b7138d598c243
content_commit: 60554e1d6572385197740ba26671728636d3d6dc
contract_frozen: true
implementation_authorized: false
release_authorized: false
codeflowmu_change_authorized: false
matrix_coverage: 60/60
wp1_1_required_test_ids: 14/14
wp0_atomicity_scenarios: 6/6
requested_gate: IMPLEMENTATION_AUTHORIZED
---

# FCoP 4.0 WP2 GitHub Review Manifest

本清单只投递 WP2 conformance-first 证据，不签署 Gate，不授权实现、Schema、
MCP、发布、迁移或 CodeFlowMu 变更。

## 内容提交文件 SHA-256

SHA-256 基于 `content_commit` 中的 committed blob 字节计算，而不是工作树
换行转换后的副本。

| SHA-256 | 文件 |
|---|---|
| `1e21c6506d1aea5ea94d475cedddcdd094e1d5800f98fa661becef9d2814a5e7` | `reports/FCOP-4.0-WP2-CONFORMANCE-PLAN.md` |
| `f3c944be8002d6b1d906dc8a150ed818d98ef3c3c016de966a82b85c5414379c` | `reports/FCOP-4.0-WP2-CONFORMANCE-RESULT.md` |
| `03c3519f694c98abaf330d7f7fd715d6079613a285ba1b585a3b182cba3d5c4b` | `tests/conformance/v4/__init__.py` |
| `6c5dfd467fc254c044af69389818c98215e9d1351fff76cc8f1eeb6b3596b1f8` | `tests/conformance/v4/conftest.py` |
| `21f0913bb22fb5f63746d680c2e00f6f4b46b260547cb69c2e59e16a04afb062` | `tests/conformance/v4/driver.py` |
| `20fa1437609d72e70dbb268a3b359e6b57a736c26c0b6df5ba1c4a4c3b696b41` | `tests/conformance/v4/test_c0_contract_authority.py` |
| `9ec4ee391c31cdd33d08dbab993156aa4e3768ffac9448e4edbe9e9d791b75c0` | `tests/conformance/v4/test_c1_workspace.py` |
| `34049f4bd30253d23a6a22fcaefa11c8cf13559f672fbff9d20e937977ec53f3` | `tests/conformance/v4/test_c2_envelopes.py` |
| `e72c91a89e03ac4c16613bcf345439091ed77a9d195fa797b373d41a4cf38e93` | `tests/conformance/v4/test_c3_lifecycle.py` |
| `b0298b3d4ae5448d0986a73c8cb12cffbe848980284ee297167b17433a1c7093` | `tests/conformance/v4/test_c4_relations.py` |
| `d175fce0e79971846ba51b928fa1a3f47d1c980d2066fbc04e98fb74ed873dfb` | `tests/conformance/v4/test_c5_convergence.py` |
| `e2bd54ac5b7520661afba2f5e9cd0232a72936791b416b3f077d5974f056de84` | `tests/conformance/v4/test_c6_authorization.py` |
| `9cb4120375322648be550a81a853f4419d8df6dbdfec3a819a9524459d828c1a` | `tests/conformance/v4/test_c7_idempotency.py` |
| `7491f043d2805821910d5cc739a2b1d6700f69e08f7510dd0720b64e184bd18d` | `tests/conformance/v4/test_c8_recovery.py` |
| `41778a34818703c40b6be0afe0fac23f5775169ba8a52d36ddc9fa1902aa6e05` | `tests/conformance/v4/test_mcp_surface_contract.py` |

## 测试证据

```yaml
v3_regression: 1225 passed, 2 skipped, 1 warning
v3_regression_new_failures: 0
v4_static_contract: 6 passed, 1 warning
v4_behavior_collected: 54
v4_behavior_passed: 1
v4_behavior_failed: 53
v4_behavior_skipped: 0
v4_behavior_xfailed: 0
v4_behavior_xpassed: 0
v4_behavior_collection_errors: 0
incidental_pass_test_ids: [C3-R01]
```

`EXPECTED_FAILURE_TEST_IDS`：

```text
[C1-N01, C1-R01, C1-FORK-01, C1-OFFLINE-01,
 C2-N01, C2-R01, C2-R02,
 C3-N01, C3-N02, C3-R02, C3-R03, C3-X01, C3-GATE-01,
 C4-N01, C4-N02, C4-R01, C4-R02,
 C5-N01, C5-N02, C5-R01, C5-R02, C5-R03, C5-X01,
 C5-BRANCH-01, C5-ARCHIVED-01, C5-FAMILY-DIGEST-01,
 C5-FAMILY-RACE-01, C5-REPORT-RACE-01,
 C6-N01, C6-R01, C6-R02, C6-X01, C6-PROFILE-01, C6-SPOOF-01,
 C6-DIGEST-01,
 C7-N01, C7-R01, C7-CREATE-01, C7-X01,
 C8-N01, C8-R01, C8-X01, C8-X02, C8-X03, C8-RETRY-01,
 C8-STATE-01, C8-INDETERMINATE-01,
 AT-01, AT-02, AT-03, AT-04, AT-05, AT-06]
```

```yaml
UNEXPECTED_FAILURE_TEST_IDS: []
WP1_1_REQUIRED_TEST_ID_DECLARED: 13
WP1_1_REQUIRED_TEST_ID_OBSERVED: 14
CLASSIFICATION: DOCUMENT_COUNT_DRIFT
CONTRACT_SEMANTICS_AFFECTED: false
```

## 交付边界

```yaml
FROZEN_SPEC_FILES_MODIFIED: 0
SOURCE_FILES_MODIFIED: 0
SCHEMA_FILES_MODIFIED: 0
MCP_IMPLEMENTATION_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0
DEPENDENCY_OR_BUILD_FILES_MODIFIED: 0
REMOTE_VERIFICATION: PERFORM_AFTER_PUSH_FROM_REMOTE_OBJECTS
IMPLEMENTATION_AUTHORIZED: false
WP3_STARTED: false
REQUESTED_GATE: IMPLEMENTATION_AUTHORIZED
```
