---
stage: WP2.1b
delivery_role: NON_AUTHORITATIVE_REVIEW_MANIFEST
status: REVIEW_READY
authorized_scope: WP2_1B_PROFILE_TRUST_BOUNDARY_ONLY
branch: review/fcop-4.0-wp2.1b-profile-trust-boundary
input_commit: c3b2cabb2d703214185a982444abd95e3cc4e800
parent_commit: c3b2cabb2d703214185a982444abd95e3cc4e800
content_commit: 768b5f11fbd1943ee4cdeb767ac340be7132b03a
delivery_head: SELF
profile_trust_boundary_review: REQUESTED
implementation_authorized: false
wp3_authorized: false
requested_gate: IMPLEMENTATION_AUTHORIZED
---

# FCoP 4.0 WP2.1b GitHub Review Manifest

只提交 Profile 信任边界修订。三态 evaluator 移到可信 Project 初始化，正常
业务请求只携带引用；反向攻击直接调用生产方法，不能靠 driver 拦截获得
行为通过。Gate 和 P0 关闭由 ADMIN 裁定，本清单不自行签署。

## 内容文件摘要

摘要基于上述 content_commit 的 Git committed blob bytes，排除工作树换行
转换。Manifest 自身及自身 commit SHA 不循环嵌入；`delivery_head: SELF`
表示承载本文件的纯 Manifest 提交，其精确 SHA 在远端核验回执中返回。

| SHA-256 | 文件 |
|---|---|
| `9e9f80ab3f34a83d0658b3474e92534743549f9b3db625a71234d9e6e48d7f0c` | `reports/FCOP-4.0-WP2.1B-PROFILE-TRUST-BOUNDARY.md` |
| `74177d7533e7f7f2b40c581d6c433e964476ccf8da1ece38008024320195c651` | `tests/conformance/v4/driver.py` |
| `3e535968d32a5fee786d667a3d1dc37851564187ad95826c63ef1f92a382870c` | `tests/conformance/v4/test_c6_authorization.py` |
| `24882664edffe5b20a6e9af04a76a474f743045f3b7ee80932fd68c32f1d97cb` | `tests/conformance/v4/test_meta_profile_boundary.py` |

## 审核重点

1. `trusted_profiles` 仅通过 driver 构造进入生产 Project 显式初始化边界；
   driver 不执行 evaluator，不设置伪注册属性，不从业务请求获取裁判。
2. C6-N01/C6-R01 保留 AUTHORIZED、DENIED、UNKNOWN 三态；请求只有
   profile_ref、authorization_ref 和其他业务数据。
3. C6-SPOOF-01 先验证可信 DENIED，再绕过 driver 误用防护直接向生产接口
   发送四种夹带字段，最后再次验证可信 DENIED。
4. 攻击必须因生产签名拒绝或可信 DENIED 而失败；伪 evaluator 不得执行，
   注册项不能被替换，磁盘快照不变，无迁移、事件或二次消费。
5. 新 Meta Guard 只算静态/适配器证据，不计生产行为通过。

## 本轮实际测试结果

```yaml
V3_REGRESSION: 1225 passed, 2 skipped, 1 warning in 22.30s
V4_STATIC_META: 27 passed, 1 warning in 0.33s
V4_BEHAVIORAL: 92 failed, 1 warning in 4.27s
V4_COLLECT_ONLY: 119 tests collected in 0.20s
PROFILE_TARGETED: 7 failed, 11 deselected in 0.41s
BEHAVIORAL_PASSED: 0
BEHAVIORAL_SKIPPED: 0
BEHAVIORAL_XFAILED: 0
BEHAVIORAL_XPASSED: 0
COLLECTION_ERRORS: 0
FROZEN_TEST_ID_COVERAGE: 60/60
FROZEN_TEST_IDS_CHANGED: 0
BEHAVIORAL_UNIQUE_IDS: 54/54
```

Profile 定点红灯均为生产缺少 `trusted_profile_initialization`，不是宣称
生产三态/反向攻击已经通过。完整后置断言已经写好，供未来正式实现满足。

## 范围与停止点

```yaml
CONTENT_FILES: 4
TOTAL_CHANGED_FILES_WITH_MANIFEST: 5
SPEC_MODIFIED: false
SOURCE_IMPLEMENTATION_MODIFIED: false
SCHEMA_MODIFIED: false
MCP_IMPLEMENTATION_MODIFIED: false
CODEFLOWMU_MODIFIED: false
MAIN_MODIFIED: false
VERSION_DEPENDENCY_BUILD_RELEASE_MODIFIED: false
REMOTE_VERIFICATION: PERFORM_AFTER_PUSH_AND_FETCH
IMPLEMENTATION_AUTHORIZED: false
WP3_STARTED: false
REQUESTED_GATE: IMPLEMENTATION_AUTHORIZED
```

按内容提交 → 纯 Manifest 提交 → push review 分支 → fetch 远端 → 核验
HEAD/可达性/文件 SHA-256 的顺序交付，完成后停止。
