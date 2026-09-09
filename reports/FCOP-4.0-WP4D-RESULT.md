# WP4D 结果：BLOCKED，保留未发布候选与真实 skip

```yaml
WP4D_STATUS: BLOCKED
AUTHORIZED_SCOPE: WP4D_ONLY
REQUESTED_GATE: NONE
BLOCKER: LEGACY_AUDIT_MINOR_ONLY_GUARD_SKIPS_RC
BASELINE_REGRESSION: 1912/1912
NEW_WP4D_IDENTITY_TESTS: 12/12
AUTHORIZED_EXISTING_PIN_TESTS: 2/2
CANDIDATE_TARGETED_OLD_AUDIT: 0 passed / 0 failed / 1 skipped
CANDIDATE_FULL_REGRESSION: NOT_RUN_AFTER_BLOCKER
ARTIFACTS: NOT_GENERATED
RC_CONSUMER_MATRIX: NOT_RUN
CODEFLOWMU_SHADOW: NOT_RUN
```

## 1. 阻断事实与权限

旧节点 `tests/test_fcop/test_audit.py::test_scan_outdated_role_docs_far_behind` 在未修改的 3.2.5 基线中通过；候选版本下两次实测均因 minor=0 在第 248 行跳过。pytest 退出 0 不表示任务书验收通过：§10.2 要求原回归全通过及零意外 skip。

旧测试第 246–248 行只看 minor；生产实现考虑 major。可能需要修正旧测试前置条件，但 §3.1 只明确允许改 pin 测试，§4/§10.3 冻结其他旧回归语义。没有删除或改名节点、没有修改旧断言、没有新增 skip/xfail。按 §4/§13.2 停止后续实现，请 ADMIN 对这一处历史测试版本条件作定点裁定。未请求 FCOP_4_RC_ACCEPTED。

## 2. 固定运行记录

工作目录 `D:/FCoP-wp4d-rc-candidate`。以下源码检查均显式使用：

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONPATH='D:/FCoP-wp4d-rc-candidate;D:/FCoP-wp4d-rc-candidate/src;D:/FCoP-wp4d-rc-candidate/mcp/src'
```

B0 修改前：

```text
python -B -m pytest tests/conformance/rule_distribution_v4 tests/test_fcop tests/conformance/v4 tests/test_fcop_mcp -q -x -p no:cacheprovider --basetemp=D:/fcop-wp4d-baseline-01 --junitxml=C:/Users/Administrator/AppData/Local/Temp/fcop-wp4d-baseline-01.xml
```

B1 固定候选身份：

```text
python -B scripts/fcop_rc_candidate_check.py
python -B -m pytest tests/test_fcop/test_pyproject_pins.py tests/test_fcop/test_wp4d_rc_identity.py -q -p no:cacheprovider --junitxml=C:/Users/Administrator/AppData/Local/Temp/fcop-wp4d-identity-02.xml
```

B2 固定候选旧节点：

```text
python -B -m pytest tests/test_fcop/test_audit.py::test_scan_outdated_role_docs_far_behind -q -rs -p no:cacheprovider --junitxml=C:/Users/Administrator/AppData/Local/Temp/fcop-wp4d-rc-audit-guard-02.xml
```

| 运行 | 固定内容 | JUnit 开始 +08:00 | JUnit 耗时 s | 通过/总数 | 失败/错误/skip | 退出码 |
|---|---|---|---:|---|---|---:|
| B0 | cbdc60a92a02b9e2eb0c1c6e2e93f74c335407f9 | 16:14:19.500917 | 3865.801 | 1912/1912 | 0/0/0 | 0 |
| B1 | 4160fc5d216f784bee6b35902b507fff8e0ba6f6 | 17:23:08.292338 | 0.131 | 14/14 | 0/0/0 | 0 |
| B2 | 4160fc5d216f784bee6b35902b507fff8e0ba6f6 | 17:23:09.180088 | 0.383 | 0/1 | 0/0/1 | 0（验收 BLOCKED） |

日期均为 2026-09-09；JUnit 起点加耗时为 suite 结束时间。B0 终端报告 3866.20s、1912 passed、3 warnings；B1/B2 包围命令的墙钟区间为 17:23:07.573642–17:23:11.202684。3 个 warning 为既有 Traversable/RefResolver 弃用提醒，不是失败。

首次 B1/B2 在 17:21:08–17:21:12 +08:00 得到相同 14 pass / 1 skip；原始 identity-01、rc-audit-guard-01 日志仍保留。随后内容文件 LF 修正完成后，在固定候选提交重跑得到以上 B1/B2；没有用旧版本或 monkeypatch 伪造候选身份。

## 3. 原始日志与交付日志

原始日志在 `C:/Users/Administrator/AppData/Local/Temp/` 保留，未改写：

| 文件 | 原始 SHA-256 |
|---|---|
| fcop-wp4d-baseline-01.xml | 69cee51b8e4c8305836658e094fe75e1d98b7d38118792b1815ee3dc7cf839c5 |
| fcop-wp4d-identity-02.xml | bc8323be3653865a76954d36bf4b9e949925f51c09e61de124ca20d82f3beedf |
| fcop-wp4d-rc-audit-guard-02.xml | fcdebab0a7063dd904a77a1e546e11c6de825ebbb3b0d0d8b1a98f6d35f3a36c |

交付完整 JUnit 于 `tests/rc/evidence/wp4d/`，仅在原始 XML 末尾补一个 LF（不是改测试记录）；最终远端哈希由 Manifest 及回读回执固定。不是节选、人工重造计数或通过日志覆盖失败日志。

| 交付日志 | tests / failures / errors / skips |
|---|---|
| [baseline-1912.xml](../tests/rc/evidence/wp4d/baseline-1912.xml) | 1912 / 0 / 0 / 0 |
| [identity-14.xml](../tests/rc/evidence/wp4d/identity-14.xml) | 14 / 0 / 0 / 0 |
| [rc-audit-guard.xml](../tests/rc/evidence/wp4d/rc-audit-guard.xml) | 1 / 0 / 0 / 1 |

## 4. 保留范围及提交纪律

候选内容仅 9 个获准文件。首次内容提交 `f5a07a1c56dfc2a4bcd8bd258cd8db5d50b080d4` 误将 Windows 混合行尾原样暂存，diff --check 报行尾问题；命令序列未及时阻止提交。随后追加 `4160fc5d216f784bee6b35902b507fff8e0ba6f6`，仅恢复 5 个获准文件的 LF，净内容 diff --check 与双 Ruff 全通过。首次错误如实保留；未 amend、未 force-push。

后续证据提交仅含本组六报告和三个完整 JUnit；最后 Manifest-only 提交。候选内容与证据提交 SHA 由 Manifest 固定。需要复现时使用最终候选内容提交，而不是第一次带行尾噪音的提交。

原 `D:/FCoP` 的 main 和未提交/未跟踪/历史/dogfood 文件保留；未在原工作树切分支。远端 main 读取值仍为 `68dbeb15f4e7f84e1d03f907be9fa66c2265843e`；未推送 main。没有改 CodeFlowMu、冻结测试、21 个权威文件、发布内容。

尚未执行完整候选回归、安装态错配、可复现构建、第三方采用、恢复、12 组合、CodeFlowMu shadow、最终 CI 验收。这些结果均为 NOT_RUN，不是 0 失败通过。完整工作不宣称完成。

## 执行身份与证据口径

- 唯一任务书：`cbdc60a92a02b9e2eb0c1c6e2e93f74c335407f9`，SHA-256 `bfc93f595800efe5185588ff92b612c9ca66e1622118e76c805d5fd908a1e290`，18471 bytes。
- 已验收实现基线：`167c5fd4ca4c9603c392bae3a4a055963e7b7ed6`；未发布候选内容提交：`4160fc5d216f784bee6b35902b507fff8e0ba6f6`。
- 环境：Windows 10 build 19045 / Python 3.12.9；时区 +08:00；独立工作树 `D:/FCoP-wp4d-rc-candidate`。
- Draft PR：[31](https://github.com/joinwell52-AI/FCoP/pull/31)，base 为 `task/fcop-4.0-wp4d-rc-candidate`，不指向 main。
- 本报告为 BLOCKED 证据，不是 RC 验收或发布证明。具体命令、起止时间、退出码、测试数、日志和哈希见 [RESULT](FCOP-4.0-WP4D-RESULT.md)。
- 尚未构建四个 RC 制品，故 artifact SHA-256 均为 NOT_GENERATED；安装态、12 组合和最终 HEAD CI 未验收，不能沿用父 Gate 的通过数。
