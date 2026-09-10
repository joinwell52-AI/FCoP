---
stage: WP2.1a
delivery_role: NON_AUTHORITATIVE_REVIEW_MANIFEST
status: REVIEW_READY
branch: review/fcop-4.0-wp2.1a-conformance-closeout
input_commit: 07b525467a8e7639c64c0a06ec08d812247e4514
parent_commit: 07b525467a8e7639c64c0a06ec08d812247e4514
content_commit: 0bde7ff920d25987bfdb5b9052facb9f31284491
delivery_head: SELF
p0_closed_by_test_contract: 3/3
contract_frozen: true
frozen_test_id_coverage: 60/60
implementation_authorized: false
wp3_authorized: false
release_authorized: false
codeflowmu_change_authorized: false
requested_gate: IMPLEMENTATION_AUTHORIZED
---

# FCoP 4.0 WP2.1a GitHub Review Manifest

本清单只交付 WP2.1a 三项行为符合性收口，不签署 Gate，不授权 WP3、实现、
Schema、MCP、发布、迁移或 CodeFlowMu 变更。

`delivery_head: SELF` 表示本文件所在的 Manifest 提交就是交付 HEAD。提交 SHA
由本文件自身 bytes 决定，无法在文件中无穷自引用；精确 Manifest SHA 和
GitHub 远端 HEAD 在 push/fetch 后通过远端对象回读并写入标准回执。

## 内容提交文件 SHA-256

以下 SHA-256 基于 `content_commit` 中的 committed blob bytes 计算，不使用
可能受 Windows 换行转换影响的工作树副本。Manifest 不列自身摘要，避免
自引用哈希循环。

| SHA-256 | 文件 |
|---|---|
| `c7d8ae2f6940a9669ac4f8aa23ccef5c4d19fb8d4ee64990dc0ab5963f10dd36` | `reports/FCOP-4.0-WP2.1A-CONFORMANCE-CLOSEOUT.md` |
| `426dee06477e22da114793210c5028491bf35d3ade3a653eb92f08946b66d721` | `tests/conformance/v4/driver.py` |
| `f531e24dd7fcfad2585645541e36f57c22a1d99ef3a71d5113fc3222f0edf217` | `tests/conformance/v4/fixtures.py` |
| `f8da65a82b2cc857e05bff453a09d42aea6910c7fde48a2d98ab338b5ca37344` | `tests/conformance/v4/test_c6_authorization.py` |
| `dcb0897087b686521f4336480b4ee8f831ca88297fb25179eadffc996c18c364` | `tests/conformance/v4/test_c8_recovery.py` |
| `214734dcf63a6db8424ae3f0f2bf0c5777afcc5a1ef5a97ed1b5d4d38981e443` | `tests/conformance/v4/test_static_driver_surface.py` |

## 三项 P0 收口

| P0 | 交付结论 | 防弱化证据 |
|---|---|---|
| 错误码不得从文字猜测 | CLOSED | `error_code()` 只读取 `.code`/`.error_code`；`ValueError("AUTHORIZATION_INVALID")` 必须失败 |
| Profile evaluator 三态 | CLOSED | AUTHORIZED 允许；DENIED/UNKNOWN 均 INVALID；三态都必须真实调用 evaluator，manifest membership 不构成授权 |
| 授权跨迁移复用 | CLOSED | T4–T7 同边丢响应重试 Existing；同授权换另一迁移 REUSED；完整 byte snapshot 与 event count 证明零副作用 |

## 测试证据

```yaml
v3_regression: 1225 passed, 2 skipped, 1 warning in 282.55s
v3_regression_new_failures: 0
v4_static_and_meta: 13 passed, 1 warning in 2.88s
v4_behavior_collected: 88
v4_behavior_passed: 0
v4_behavior_failed: 88
v4_behavior_skipped: 0
v4_behavior_xfailed: 0
v4_behavior_xpassed: 0
v4_behavior_collection_errors: 0
v4_all_collected: 101
behavioral_unique_test_ids: 54/54
frozen_test_id_coverage: 60/60
frozen_test_ids_added: 0
frozen_test_ids_removed: 0
```

## 交付边界

```yaml
TEST_FILES_MODIFIED: 5
REPORT_FILES_ADDED: 1
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
