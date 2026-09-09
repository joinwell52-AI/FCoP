# WP4D 勘误续作：RC-IDENTITY-AND-VERSION — BLOCKED

## 当前续作结论（覆盖本报告的历史状态说明）

```yaml
WP4D_STATUS: BLOCKED
AUTHORIZED_SCOPE: WP4D_AUDIT_GUARD_ONLY_AND_WP4D_RESUME
ERRATUM_COMMIT: 22db1377163bb0b1e74c4b94fa1f594b3e762a9d
ERRATUM_SHA256: 0e8926c282516dd10e2c1506243ccf33ab7798a8cd0744bcbccf078d5f344767
RESUME_BASE: 893e5c55f9f7ea433c6c518c76534218a4cf9570
AUDIT_GUARD_FIX_COMMIT: fad3a2d2cdcee490f8a86ae3d1254439089d5427
CANDIDATE_CONTENT_COMMIT: dd8138684006432c6bb62c952909a59cda20adaf
AUDIT_GUARD_FIX: PASS
AUDIT_TEST_ID_FIXTURE_ASSERTION_PRESERVED: true
TARGETED_AUDIT: 1/1
TARGETED_AUDIT_SKIPPED: 0
NEW_BLOCKER: RC_TWINE_6_2_METADATA_2_5_REJECTION
REQUESTED_GATE: NONE
```

唯一原任务书为 `cbdc60a92a02b9e2eb0c1c6e2e93f74c335407f9` 的 WP4D 01 号任务书；本次 02 号勘误已按原始 Blob 核验 5642 bytes 与上列 SHA-256。勘误分支相对原任务书仅多一个文件提交；按其要求从 RESUME_BASE 继续同一独立工作树、原 feat 分支及 Draft PR #31，没有把任务书分支改写接入实现父链。

旧审计 guard 的真实 skip 已解除，不删除或追改原始 BLOCKED 事实。当前新阻断是执行人新增构建 workflow 中选择的旧 Twine pin；不是将旧问题归咎于 ADMIN 任务书。原任务书 §13.2 要求适用 CI 失败即停止，因此未在失败后擅自调整候选工具 pin、降级制品元数据或放宽检查。

当前制品身份仍为未发布 `fcop==4.0.0rc1 / fcop-mcp==4.0.0rc1`。四个首轮文件虽由构建器生成，但未通过 Twine、未计算并交付候选哈希清单；其 SHA-256 均为 **UNVERIFIED_NOT_UPLOADED**。第二轮构建、4/4 复现、wheel/sdist 安装态证明、12 组合 consumer 和本轮 CodeFlowMu shadow 均未验收。不得以源码成功、既有 package job 或旧 Gate 替代。

完整命令、UTC 时间、退出码、计数、日志及交付字节说明集中列于本轮 [RESULT](FCOP-4.0-WP4D-RESULT.md)。候选内容提交的固定远端运行是 [Core CI](https://github.com/joinwell52-AI/FCoP/actions/runs/34363703057)、[MCP CI](https://github.com/joinwell52-AI/FCoP/actions/runs/34363702991) 和 [RC CI（FAIL）](https://github.com/joinwell52-AI/FCoP/actions/runs/34363703047)。所有证据必须按这里的提交读取；后续 Manifest HEAD 不能凭这些结果声称全绿。

main 合并、tag、公开 RC、PyPI、GitHub Release、MCP Registry、Zenodo 及 CodeFlowMu 写入仍未授权，均未执行。新证据提交只包含这六份报告与测试证据，最后另作 Manifest-only 提交；内容、证据、Manifest 父链及远端逐文件 SHA-256 由 Manifest 和远端回读回执固定。

## 本轮身份与 guard 复核

- 首先仅修改旧测试的前置版本判断：比较 `(major, minor) < (1, 2)`；单文件提交 `fad3a2d…`。未改变 DEV.md/v1.0 夹具、Project 调用、审计调用或最终断言。
- AST 比较删除双方仅有的旧/新 guard 两个节点后，整份 `test_audit.py` 的 AST 相等；原 Test ID、fixture 和断言保留。
- 原生 Windows 定向 guard 为 1 passed / 0 skipped；身份及 pin 为 14 passed；候选文档与相关节点为 25 passed（均含 12 个新增身份节点、2 个既有 pin 节点）。
- 双版本为 4.0.0rc1；MCP pin 为 `fcop>=4.0.0rc1,<4.1.0`；候选精确对与历史 3.2.5 对保留，未加入稳定版 4.0.0 对，Beta classifier 保持。
- 新增的验证脚本没有导入私有 FCoP 生产接口；`Project`、`FcopError` 和可信 `create_server` 启动边界用于样例。没有新增公共 API 或运行时依赖。
- `scripts/wp4d_verify_scope.py` 在内容提交上通过：routing 除兼容集合以外、两个版本模块除版本赋值以外，AST 均与固定基线相等；21/21 权威字节、19/19 canonical 文件与两棵冻结 Conformance tree 一致。

本文件的身份通过不等于制品/安装态验收，当前 REQUESTED_GATE 仍为 NONE。

---

## 历史快照：原 BLOCKED 报告原文保留

以下原文固定在 893e5c55f9f7ea433c6c518c76534218a4cf9570；其中“未运行”和旧 skip 仅描述该历史提交，不是上述续作后的当前结论。

# WP4D RC 身份与版本：局部通过，阶段阻断

双包源码身份为未发布 `4.0.0rc1`，两处 classifier 为 Beta。
MCP 下界精确为 `fcop>=4.0.0rc1,<4.1.0`；兼容集合仅增加同版本 RC 对，保留历史 3.2.5 对，不加入稳定 4.0.0。
根包依赖描述已纠正；PyYAML/jsonschema、FastMCP、Relay 的原依赖行为未改变。

任务书 §3.1 明确允许修正原有两个 pin 测试：保留 Test ID，强制相同 MAJOR.MINOR 和精确 prerelease 下界。新增测试 12 个，含 8 种错误 pin 拒绝；合计 14/14 通过、0 失败、0 skip。

这仅证明源码声明和静态依赖契约，不证明安装态元数据或真实错配组合。源 import 实测路径为 `D:/FCoP-wp4d-rc-candidate/src/fcop/__init__.py`，不冒充 site-packages。

## 固定远端内容回读

2026-09-09 17:24:29 +08:00，从 GitHub Contents API 按候选提交逐项读取原始 Blob，9/9 与本地文件及 Git Blob 相同：

| 文件 | bytes | GitHub SHA-256 |
|---|---:|---|
| docs/fcop-4.0/rc-candidate-boundary.md | 1469 | 8cf4906f96fc7b74096a77bba6b2bd4355e8ae72eb4d7fa64747ce514d3e06bb |
| mcp/pyproject.toml | 4861 | 86628c2f21270758a51abac4fc375673d2c6a0c4c4806cf141fa270babff85c8 |
| mcp/src/fcop_mcp/_version.py | 610 | 310a8df396e097eeb5d3d8a0c83e3e2bc8803539ea94f7ecad7efad070a68339 |
| mcp/src/fcop_mcp/routing.py | 3760 | 6f054a99e2b2807b813d0e43e644e8b950a2f63c2d0159d519c6c89bb35fcb8b |
| pyproject.toml | 6077 | c9faa4f794b30ed52fdfc7093e0f0b30f7d8965ec8c8139c94f04eb732c346dc |
| scripts/fcop_rc_candidate_check.py | 3243 | 0a284ca78f5e36d46bbd73ef2113186d90194917a31c33a12a29818b4c8b144c |
| src/fcop/_version.py | 564 | 14ffc70e19c78e318a2b65b2331dd21ccd3e84913493b1dca5a64079a6b0f3b9 |
| tests/test_fcop/test_pyproject_pins.py | 1283 | 45cafdb7f125355d66cb503a3248c0b255e8826343e44894f98d4d1c3462cfc3 |
| tests/test_fcop/test_wp4d_rc_identity.py | 1586 | a5876542335a04a05d7ed315cfd239e14bf58986e90bf5bca479cc2b0a7473f8 |

命令：`python -B scripts/fcop_rc_candidate_check.py`；17:23:07–17:23:08 +08:00，退出 0，输出双包候选身份、精确 pin、stable_pair=false、published=false。
候选身份测试命令、JUnit 及 14/14 明细见 RESULT。

## 执行身份与证据口径

- 唯一任务书：`cbdc60a92a02b9e2eb0c1c6e2e93f74c335407f9`，SHA-256 `bfc93f595800efe5185588ff92b612c9ca66e1622118e76c805d5fd908a1e290`，18471 bytes。
- 已验收实现基线：`167c5fd4ca4c9603c392bae3a4a055963e7b7ed6`；未发布候选内容提交：`4160fc5d216f784bee6b35902b507fff8e0ba6f6`。
- 环境：Windows 10 build 19045 / Python 3.12.9；时区 +08:00；独立工作树 `D:/FCoP-wp4d-rc-candidate`。
- Draft PR：[31](https://github.com/joinwell52-AI/FCoP/pull/31)，base 为 `task/fcop-4.0-wp4d-rc-candidate`，不指向 main。
- 本报告为 BLOCKED 证据，不是 RC 验收或发布证明。具体命令、起止时间、退出码、测试数、日志和哈希见 [RESULT](FCOP-4.0-WP4D-RESULT.md)。
- 尚未构建四个 RC 制品，故 artifact SHA-256 均为 NOT_GENERATED；安装态、12 组合和最终 HEAD CI 未验收，不能沿用父 Gate 的通过数。
