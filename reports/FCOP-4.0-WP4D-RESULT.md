# WP4D 勘误续作：RESULT — BLOCKED

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

## 本轮结果与下一步权限

```yaml
OLD_BLOCKER: RESOLVED_BY_AUTHORIZED_GUARD_FIX
NATIVE_FULL_REGRESSION: 1924/1924
NATIVE_FULL_FAILURES_ERRORS_SKIPS: 0/0/0
UBUNTU_CONTENT_FULL_REGRESSION: 1924/1924
UBUNTU_CONTENT_FAILURES_ERRORS_SKIPS: 0/0/0
NATIVE_DOC_AND_IDENTITY: 25/25
SOURCE_PUBLIC_CLIENTS: 2/2
MCP_SOURCE_SURFACE: 46/12/4
CONTENT_EXISTING_CI: 27/27
CONTENT_WINDOWS_CI: 8/8
RC_BUILD: FAILED_TWINE_METADATA_2_5
RC_REPRODUCIBILITY: NOT_RUN
RC_CONSUMER_MATRIX: NOT_RUN
INSTALLED_LEGACY_AND_SHADOW: NOT_RUN
FINAL_MANIFEST_RC_ACCEPTANCE: NOT_ACCEPTED
```

旧问题已经关闭；新问题由执行人在新增 workflow 中固定旧 Twine 6.2.0 导致。不得归咎于冻结 Core 或 Schema。按原任务书 §13.2，本轮保留 dd813868 候选与失败日志后停止内容修改，仅完成阻断证据和 Manifest 交付。请 ADMIN 对构建工具 pin 作定点续作裁定；Twine 7.0.0 的只读代码检查见诊断 JSON，但本轮没有替换或执行，不能预签通过。

## 命令、时间、计数与退出码

所有日期为 2026-09-09；下表起点来自完整 JUnit，结束为起点加 suite 耗时（精度毫秒），不是臆造进程日志。

| 检查 | 固定内容 / 环境 | 开始 → 结束 | pass/total | fail/error/skip | exit |
|---|---|---|---:|---|---:|
| guard 定向 | fad3a2d / Windows 10 build 19045, Python 3.12.9 | 2026-09-09T21:21:33.185582+08:00 → 2026-09-09T13:21:33.705Z | 1/1 | 0/0/0 | 0 |
| 身份/pin | fad3a2d / 同上 | 2026-09-09T21:21:34.787187+08:00 → 2026-09-09T13:21:34.924Z | 14/14 | 0/0/0 | 0 |
| 原生完整回归 | fad3a2d / 同上 | 2026-09-09T21:21:54.591334+08:00 → 2026-09-09T14:24:21.835Z | 1924/1924 | 0/0/0 | 0 |
| 文档/身份定向 | dd813868 内容提交前 / 同上 | 2026-09-09T22:25:47.346182+08:00 → 2026-09-09T14:25:47.743Z | 25/25 | 0/0/0 | 0 |
| Ubuntu 完整回归 | dd813868 / Ubuntu 24.04.5, Python 3.12.14 | 2026-09-09T14:27:49.684639+00:00 → 2026-09-09T14:29:44.717Z | 1924/1924 | 0/0/0 | 0 |

原生完整命令从 UTC 13:21:53.776 启动，终端结束观测 UTC 14:24:23；pytest 报 3747.49s，3 条既有 Traversable / RefResolver 弃用警告。未修复这些警告。

原生工作目录 `D:/FCoP-wp4d-rc-candidate`；只在源码检查中显式设置 PYTHONDONTWRITEBYTECODE=1 与 PYTHONPATH 为本工作树、src、mcp/src。未用其冒充安装态：

```text
python -B -m pytest tests/test_fcop/test_audit.py::test_scan_outdated_role_docs_far_behind -q -p no:cacheprovider --junitxml=<temp>/fcop-wp4d-resume-audit-01.xml
python -B -m pytest tests/test_fcop/test_pyproject_pins.py tests/test_fcop/test_wp4d_rc_identity.py -q -p no:cacheprovider --junitxml=<temp>/fcop-wp4d-resume-identity-01.xml
python -B -m pytest tests/test_fcop tests/conformance/v4 tests/test_fcop_mcp tests/conformance/rule_distribution_v4 -q -x -p no:cacheprovider --basetemp=D:/fcop-wp4d-resume-full-01 --junitxml=<temp>/fcop-wp4d-resume-full-01.xml
python -B -m pytest tests/test_fcop/test_install_prompt.py tests/test_fcop/test_pyproject_pins.py tests/test_fcop/test_wp4d_rc_identity.py -q -p no:cacheprovider --junitxml=<temp>/fcop-wp4d-resume-doc-identity-01.xml
python -B scripts/wp4d_source.py
python -B scripts/wp4d_verify_scope.py
```

此处 `<temp>` 为 `C:/Users/Administrator/AppData/Local/Temp`。Ubuntu full 使用相同四套测试路径，命令固定在新增 workflow，见 [source Job](https://github.com/joinwell52-AI/FCoP/actions/runs/34363703047/job/102506904899)。

原生样例证据边界 UTC 14:25:08.896629–14:26:09.371575（目录创建至最后日志写入），退出 0，2/2 源码样例；Ubuntu 同命令步骤 UTC 14:29:46–14:29:53，成功。两者都使用真实进程终止/重开，不是安装态。

静态检查：新增 Python 文件 AST/Ruff、两包 Ruff、workflow 12 矩阵/contents:read/无发布 environment 检查通过；`git -c core.autocrlf=false diff --check` 通过。首次新 README 修改行保留了 Markdown 双空格而被 diff --check 提醒，提交前已去除该一处尾随空格；未改变测试或生产行为。候选提交后 scope guard 再次通过（UTC 14:27 前后，准确运行日志由 CI 同一守卫补强）。

## 新 CI 阻断与证据

RC build UTC 14:27:20–14:27:35；双包首轮构建结束后，Twine 检查 UTC 14:27:30–14:27:32 退出 1。新 RC run 为 FAILURE，consumer 依赖 Job 为 skipped，没有 12 个单元结果。详见 ARTIFACT-REPRODUCIBILITY 报告和完整日志，四候选 SHA-256 为 UNVERIFIED_NOT_UPLOADED；不得把 Twine 自身或日志 artifact 的哈希当作候选制品哈希。

原生与 Ubuntu 完整 JUnit 全量转存，每份只在原始 XML 后补一个 LF；原始文件保留。源码小日志在转存时仅 CRLF 归一为 LF；两个 build 日志为展示副本，按行转存并去除共四行的尾随空格，以通过 git diff --check。失败消息、计数及退出状态未改变；GitHub 原日志和本地下载原件未修改。日志 artifact 与仓库展示副本的容器/文件 SHA 不混用，表中均为交付文件 SHA-256，最终逐项远端回读。

| 交付证据 | bytes | SHA-256 |
|---|---:|---|
| [baseline-1912.xml](../tests/rc/evidence/wp4d/baseline-1912.xml) | 453008 | `54c07dd75b3208ee41bc51d2b0e1bf7ff4d6cadda0977042ad8ffbf3ccc48f33` |
| [content-ci-snapshot.json](../tests/rc/evidence/wp4d/content-ci-snapshot.json) | 95357 | `51f1bd1cb6ee817530dfa8eb1e0f85c6c284a43be6d75e1f62c77cfb33deb478` |
| [identity-14.xml](../tests/rc/evidence/wp4d/identity-14.xml) | 2293 | `4cfa47c3bdff3f4b7700872a1ed8ae2b51a5b4c731b1942ced3a425352b2a052` |
| [native-source-mcp.log](../tests/rc/evidence/wp4d/native-source-mcp.log) | 276 | `6bc9c14ae833862c97a897050b4c1bca6b34f0e0d26ecba061faaf5b769b5a5d` |
| [native-source-python.log](../tests/rc/evidence/wp4d/native-source-python.log) | 249 | `a874564d1776a3f1af5b37e094c3eccaf07f9f5b2de56d903e0cd90760f89a35` |
| [rc-audit-guard.xml](../tests/rc/evidence/wp4d/rc-audit-guard.xml) | 596 | `6c03b6d5710cc90c1275b97d18e9b683f25bfff88c0c4777a9ca0af22f02934b` |
| [rc-build-job.log](../tests/rc/evidence/wp4d/rc-build-job.log) | 43060 | `791dbf0506aaf6e6af5b6b155d040ff0be94182adce7a254524da019e6360893` |
| [rc-build-metadata-failure.log](../tests/rc/evidence/wp4d/rc-build-metadata-failure.log) | 1634 | `8b9797bec3145685ed2c2589aa178f01c148f19529cd0dec586a82416c0d1e7d` |
| [resume-audit-1.xml](../tests/rc/evidence/wp4d/resume-audit-1.xml) | 363 | `2a9c6a64553153a53f6f69e74be2062a41a57cef31a287fdec1a15329bafe3fd` |
| [resume-doc-identity-25.xml](../tests/rc/evidence/wp4d/resume-doc-identity-25.xml) | 4031 | `3049719aca165a1ab073893a4c8de366b1ddf092bc876d819b9e43e8b27ff323` |
| [resume-full-1924.xml](../tests/rc/evidence/wp4d/resume-full-1924.xml) | 454799 | `d6b39e5a35e52bc0d2d03dd32206cbb7693aaeba0cdd9134d7f7a19ce0602474` |
| [resume-identity-14.xml](../tests/rc/evidence/wp4d/resume-identity-14.xml) | 2293 | `1e4633939df9206c6edeb9504aae94eb57dc88ec3bcc70acf91f4988cdd44d9d` |
| [toolchain-diagnosis.json](../tests/rc/evidence/wp4d/toolchain-diagnosis.json) | 2105 | `df2ff21f27f27c6343306ea90037a5e8f2606f7f3938896e0e6f55eab48f4f19` |
| [ubuntu-content-full-1924.xml](../tests/rc/evidence/wp4d/ubuntu-content-full-1924.xml) | 454732 | `023552fc2549a3c340064a2e215bd898bbf0b3f11ca0304ed23e86bc9822b172` |

## 保留现场与停止

证据交付检查另发现 build job 下载文本带 UTF-8 BOM；仅从仓库展示副本移除该 3 字节 BOM，原始下载和 GitHub 日志保持不动。以上表格已使用最终展示副本的摘要。

候选内容、旧 BLOCKED 原文及旧 skip JUnit 均保留。未改 Core/MCP 生产行为、冻结测试、21 个权威字节、Schema、legacy rules、release.yml/server.json/CITATION、CodeFlowMu 或 main。原 D:/FCoP 工作树、未跟踪资料及 dogfood 没有迁移或重新部署。

最终仅提交六报告与证据、再提交 Manifest 并远端回读；不 force-push。PR #31 继续 Draft，base 仍为 task/fcop-4.0-wp4d-rc-candidate。本次 **REQUESTED_GATE: NONE**，不请求或自行签署 FCOP_4_RC_ACCEPTED。

---

## 历史快照：原 BLOCKED 报告原文保留

以下原文固定在 893e5c55f9f7ea433c6c518c76534218a4cf9570；其中“未运行”和旧 skip 仅描述该历史提交，不是上述续作后的当前结论。

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
