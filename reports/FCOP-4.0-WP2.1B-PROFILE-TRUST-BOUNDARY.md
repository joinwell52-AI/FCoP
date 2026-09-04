# FCoP 4.0 WP2.1b · Profile Trust Boundary

## 1. 输入、范围与审查状态

```yaml
AUTHORIZED_SCOPE: WP2_1B_PROFILE_TRUST_BOUNDARY_ONLY
INPUT_COMMIT: c3b2cabb2d703214185a982444abd95e3cc4e800
REVIEW_BRANCH: review/fcop-4.0-wp2.1b-profile-trust-boundary
TEST_BOUNDARY_CORRECTION: SUBMITTED_FOR_REVIEW
IMPLEMENTATION_AUTHORIZED: false
WP3_STARTED: false
```

WP2.1a 的三态测试确实存在信任边界错误：业务请求携带 evaluator 会把授权
裁判权交给请求者。本轮只修测试接入位置；上一轮错误码与 C8 异边复用修订
原样保留，旧报告/Manifest 不改写。

## 2. 正确的可信初始化入口

```text
测试宿主的可信配置
  → V4ConformanceDriver(root, trusted_profiles={profile_ref: evaluator})
  → Project(root, trusted_profiles=registry)
  → transition(profile_ref, authorization_ref, other_data_only_fields)
  → 生产 Core 查询可信注册项并执行三态判定
```

`driver.py` 只允许在构造阶段把 registry 交给生产 Project 的显式初始化参数。
registry 使用独立字典副本与只读映射，外部随后替换原字典中的 evaluator
不能改变已传入注册项。driver 不调用 evaluator、不计算授权结论、不通过
`setattr` 伪造生产注册项，也不在每次业务请求中重新注册。

当前 3.2.5 Project 没有这个初始化能力，故相关行为节点报告
`V4_NOT_IMPLEMENTED`，action 为 `trusted_profile_initialization`，附带原合同
ID 和 F4.7.4–F4.7.6。没有把注册替身作为生产能力。

## 3. 普通业务请求与反向攻击分开验证

普通 driver 请求禁止 `profile_evaluator`、`profile_resolver`、
`trusted_profiles`、`profile_registry`、`authorization_evaluator`，以及其他
字段名下的 callable（包括嵌套容器）。这只是适配器误用防护，不计为生产
行为符合性通过。

`test_meta_profile_boundary.py` 单独验证：

- 初始化接收 registry；正常 transition 只有 Profile 与授权引用，没有裁判对象；
- driver 不调用 evaluator，注册配置不受原字典后续替换影响；
- transition/create_task/recover_operation 三类请求中的四种裁判夹带均被
  适配器拒绝，伪 evaluator 未执行；
- 当前已有生产业务方法的显式签名不能声明裁判字段。缺失的 v4 方法不获
  行为通过信用，仍由行为组保持红灯。

## 4. 三态与真实生产反向测试

| 合同 | 场景 | 生产后置断言 |
|---|---|---|
| C6-N01 | 初始化注册 AUTHORIZED | 调用可信 evaluator，正确 issuer/proof，T4 成功且 event 绑定证据摘要 |
| C6-R01 | 初始化注册 DENIED | AUTHORIZATION_INVALID；未移动、未新增事件、未消费授权 |
| C6-R01 | 初始化注册 UNKNOWN | AUTHORIZATION_INVALID；未移动、未新增事件、未消费授权 |
| C6-SPOOF-01 | 可信 DENIED；请求夹带 AUTHORIZED 裁判 | 拒绝或忽略夹带，可信 DENIED 继续生效，绝不完成迁移 |

新增的 C6-SPOOF-01 反向测试展开四种字段：`profile_evaluator`、
`profile_resolver`、`trusted_profiles`、`caller_judge`。每个节点：

1. 通过正常请求证明生产 Project 实际调用已注册 DENIED evaluator；
2. **绕过 driver 误用防护，直接向真实 Project 方法提交恶意字段**，不删除
   字段、不在 driver 内替生产返回拒绝；
3. 若 TypeError 拒绝，只接受可由生产方法签名 bind 独立证明的参数拒绝，
   不接受内部崩溃冒充正确拒绝；否则要求结构化 AUTHORIZATION_INVALID；
4. 再发一次正常请求，验证可信注册项未被恶意请求悄悄替换；
5. 验证伪 evaluator 从未执行，可信 evaluator 仍返回 DENIED，TASK 留在
   review，全 workspace byte snapshot 不变，无新增事件/receipt/授权消费。

因此，仅在 driver 中拦掉攻击、无条件返回错误、静默替换注册项或允许请求者
自己的 AUTHORIZED 判定，都不能满足完整后置断言。

## 5. 验证证据

执行目录 `D:\FCoP-wp2.1b-profile-trust`，显式设置 `PYTHONPATH` 为本 worktree
的 `mcp/src` 与 `src`。所有以下结果均为本轮实际执行：

| 组 | 结果 |
|---|---|
| v3 全回归，`--ignore=tests/conformance/v4` | 1225 passed, 2 skipped, 1 warning in 22.30s |
| v4 Static/Meta（包含新 Profile boundary meta 文件） | 27 passed, 1 warning in 0.33s |
| C1–C8 全行为组，`--tb=no` | 92 failed, 1 warning in 4.27s |
| 全目录 `--collect-only` | 119 tests collected in 0.20s |
| 三态与夹带攻击定点 `--tb=line` | 7 failed, 11 deselected in 0.41s；均明确缺可信初始化能力 |

92 个行为红灯表示未实现，不表示生产授权已通过；0 pass、0 skip、0 xfail、
0 xpass、0 collection error。27 个绿色静态/元节点不计行为通过数。
warning 与两项 v3 skip 均为既有弃用提示/legacy 数据缺失。

```yaml
FROZEN_TEST_ID_COVERAGE: 60/60
FROZEN_TEST_IDS_ADDED_OR_REMOVED: 0
BEHAVIORAL_UNIQUE_IDS: 54/54
BEHAVIORAL_NODES: 92
STATIC_META_NODES: 27
COLLECTED_NODES: 119
PROFILE_TRISTATE_CASES: 3/3_DEFINED
CALLER_JUDGE_ATTACK_VARIANTS: 4/4_DEFINED
```

## 6. 范围、交付与停止点

内容修改仅限 `tests/conformance/v4/driver.py`、
`tests/conformance/v4/test_c6_authorization.py`，新增
`tests/conformance/v4/test_meta_profile_boundary.py` 和本报告。随后仅新增
`reviews/fcop-4.0/wp2.1b/MANIFEST.md`。

```yaml
SPEC_MODIFIED: false
SOURCE_IMPLEMENTATION_MODIFIED: false
SCHEMA_MODIFIED: false
MCP_IMPLEMENTATION_MODIFIED: false
CODEFLOWMU_MODIFIED: false
MAIN_MODIFIED: false
VERSION_DEPENDENCY_BUILD_RELEASE_MODIFIED: false
CONTENT_COMMIT: SELF
EXACT_CONTENT_SHA: RECORDED_IN_WP2_1B_MANIFEST
REMOTE_VERIFICATION: PERFORM_AFTER_PUSH_AND_FETCH
IMPLEMENTATION_AUTHORIZED: false
WP3_AUTHORIZED: false
REQUESTED_GATE: IMPLEMENTATION_AUTHORIZED
```

本报告提交修订证据供 ADMIN 审查，不自行宣告 Gate 或 P0 签署关闭。完成
GitHub review 分支的远端 HEAD、可达性与 blob SHA-256 核验后停止。
