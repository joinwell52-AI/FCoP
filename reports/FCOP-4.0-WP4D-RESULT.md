# WP4D RESULT — 候选 CI 通过；最终 Shadow 静默窗口受阻

## 当前增量回执：最终交付尚未完成

```yaml
WP4D_STATUS: BLOCKED
BLOCKER: CODEFLOWMU_CONCURRENT_WRITES_PREVENT_FINAL_ZERO_DRIFT_RECHECK
AUTHORIZED_SCOPE: WP4D_VERIFICATION_REPAIR_ENVELOPE_AND_CLOSEOUT
CANDIDATE_CONTENT_COMMIT: d1a86f32d87f000fe0aec444563decdc892dc142
CANDIDATE_CI: 42/42
WINDOWS_FULL: 1931/1931
UBUNTU_FULL: 1931/1931
RC_CONSUMERS: 12/12
INSTALLED_ORIGINS: 24/24
INITIAL_INSTALLED_SHADOW: 14/14
LATEST_SHADOW_INVENTORY_EQUALITY: FAIL
FINAL_MANIFEST_DELIVERY: NOT_COMPLETED
REQUESTED_GATE: NONE
CODEFLOWMU_WRITE_AUTHORIZED: false
MAIN_MERGE_AUTHORIZED: false
RC_PUBLISH_AUTHORIZED: false
```

初次安装态 Shadow 的 14/14 及前后全树一致证据真实保留。为补齐精确起止计时而进行的四次附加复验均发现读取窗口内下游变化，不能覆盖成 PASS，不能把初次通过冒充最新复验结果。这里只记录新的外部现场冲突，不修改生产代码、测试预期或任何 CodeFlowMu 文件/进程。

最新两次已定位差异（UTC）：

- 16:50:42.817716–16:51:36.749765：新增未跟踪文件 `research/evidence/changes/CFM-INDEPENDENT-UPDATER-20260910/runs/03-target.txt`。
- 16:52:35.678352–16:54:02.437892：未跟踪文件 `research/evidence/changes/CFM-INDEPENDENT-UPDATER-20260910/runs/05-shell-regression.txt` 的 SHA-256 从 `ffbd97cad9eacbef0057d7a44f505e832120c3509538035bd7db0b6fa026a656` 变为 `dfdddb5e03e12c7620089610e46f95ad7645573e7bb4f247513d1e21e95d6829`。

两次 tracked 文件均无变化，CodeFlowMu HEAD 均为 `cb590ce35686cb1980e3c89a7d68bd0cfbeb825a`；变化发生在其未跟踪验证证据中。诊断只在原脚本断言失败后读取 traceback 中原始 before/after，不 patch 任何方法或结果。失败、差异与执行时段保存在 `tests/rc/evidence/wp4d/socketpair-resume/shadow-*.json`。

需要 ADMIN 协调一个 CodeFlowMu 工作树约 2–3 分钟无写入的窗口，执行人再运行原样严格检查。此协调不等于请求修改、停止或升级 CodeFlowMu 的权限，执行人不会自行操作其进程。其它 WP4D 修复已完成，候选制品已重建、全部 CI 已通过；不需要新的协议/实现授权。

当前仅交付 RESULT 增量与证据，五份其余最终报告草稿保留在原独立工作树，未作为最终完成报告提交。没有创建新的阻断 PR，没有改写历史，也没有创建声称 COMPLETE 的新 Manifest。获得稳定窗口并通过检查后，继续原 PR #31 的最终证据/Manifest 与最终 HEAD 验证，不重做已授权功能、不扩大范围。

以下为已完成候选内容验证的详细记录；其中预期的最终 Manifest/回执步骤目前尚未执行。

---

# WP4D RESULT — 候选内容验证通过

## 收口结果与待完成的交付步骤

```yaml
AUTHORIZED_SCOPE: WP4D_VERIFICATION_REPAIR_ENVELOPE_AND_CLOSEOUT
CANDIDATE_CONTENT_VERIFICATION: PASS
CANDIDATE_CONTENT_COMMIT: d1a86f32d87f000fe0aec444563decdc892dc142
WINDOWS_FULL: 1931/1931
UBUNTU_FULL: 1931/1931
BASELINE_REGRESSION: 1912/1912
WP4D_TESTS: 19/19
FAILURES_ERRORS_SKIPS: 0/0/0
CONTENT_CI: 42/42
EXISTING_CI: 27/27
EXISTING_WINDOWS_CI: 8/8
RC_CONSUMERS: 12/12
INSTALLED_ORIGIN_PATHS: 24/24
TWINE_GROUPS: 2/2
REPRODUCIBILITY: 4/4
CODEFLOWMU_SHADOW: 14/14
MCP_SURFACE: 46/12/4
CANONICAL: 19/19
FROZEN_BYTES: 21/21
FINAL_MANIFEST_HEAD_CI: PENDING_AT_REPORT_COMMIT
FINAL_REMOTE_READBACK: PENDING_AT_REPORT_COMMIT
FCOP_4_RC_ACCEPTED: false
MAIN_MERGE_AUTHORIZED: false
RC_PUBLISH_AUTHORIZED: false
```

最终阶段只剩报告/evidence 提交、Manifest-only 提交、远端回读与最终 HEAD CI。完成后在 PR #31 发布绑定实际 HEAD 的 COMPLETE 回执并请求 FCOP_4_RC_ACCEPTED，然后立即停止；这些尚未发生的最终动作没有在本报告提前写为 PASS。

本轮修复均为执行人新增验证材料的问题，不归咎于 Core：socketpair 名称兼容改为 code identity；新测试补 -> None；Windows 全量及路径安全计数；候选/执行身份分离；consumer 浅克隆补完整父链。无生产语义、冻结断言、skip/xfail 或错误码变化。

## 固定身份与结论

本次由 `ba8830c1871f6516fec1e2779d21c09b9a5e96ea` 授权的验证层连续修复已完成；任务书 SHA-256 为 `badc8a597a01407dec012d1085a5cac5815f8608e8afec742688846beb11c625`（7652 bytes）。继承 socketpair 定点授权 `6c2793d2f91fe5c0c8d4edce4e8e0064f889c686`，不扩大到生产代码或发布。

- 最终候选内容提交：`d1a86f32d87f000fe0aec444563decdc892dc142`。
- 双包：`fcop==4.0.0rc1 / fcop-mcp==4.0.0rc1`；依赖：`fcop>=4.0.0rc1,<4.1.0`。
- 本报告记录候选内容 HEAD 的已完成验证，**不是提前宣称后续 Manifest HEAD CI 已通过**。最终 HEAD 的 CI、远端回读、自身摘要和 COMPLETE 回执必须在 PR #31 追加；只有全部通过后才请求 `FCOP_4_RC_ACCEPTED`。
- PR #31 仍 OPEN / Draft，分支 `feat/fcop-4.0-wp4d-rc-candidate`，base `task/fcop-4.0-wp4d-rc-candidate`。不合并、不创建 tag、不公开 RC，不触发任何发布。

## 已执行命令、时间与证据

以下均为 UTC。完整逐 Job 起止、平台、结论和 URL 在 `tests/rc/evidence/wp4d/final-content/ci-jobs.json`；测试 XML 保留自身时间和计数。没有把 queued、cancelled 或 skipped 算作 PASS。

| 执行 | 起止或机器计时 | 平台 / 返回码 | 结果 |
|---|---|---|---|
| `python -B scripts/wp4d_build.py <new-output>`，内部两次 build 与 twine check | 2026-09-09 16:36:17.094948–16:36:21.777748 | Ubuntu / Python 3.12 / 0 | Twine 2/2 组（8/8 文件），可复现 4/4 |
| `python -B -m pytest tests/test_fcop tests/conformance/v4 tests/test_fcop_mcp tests/conformance/rule_distribution_v4 -q --junitxml=<full.xml>` | Ubuntu suite 起始 16:36:26.457821，102.848s；完整 Job 16:35:57–16:38:19 | Ubuntu / 0 | 1931/1931，失败/错误/skip 0/0/0 |
| 同一完整 pytest 命令 | Windows suite 起始 16:37:07.854159，270.586s；完整 Job 16:35:57–16:41:56 | 原生 Windows / 0 | 1931/1931，失败/错误/skip 0/0/0 |
| `python -B scripts/wp4d_source.py` | 上述两个 source Job 内，各自记录原始 SOURCE_ONLY 输出 | Ubuntu、Windows / 0 | 两种外部样例的源码 parity；不当作安装态证明 |
| `python -B scripts/wp4d_consume.py <first-set> <manifest-sha> <legacy-set> <legacy-sha> <evidence>` | 12 份 result.json 起止全集 16:37:15.908713–16:41:15.207947 | 3 OS × Python 3.10–3.13 / 全部 0 | consumer 12/12，wheel/sdist 24/24，失败/skip 0/0 |
| 既有 Core + MCP workflow | 16:35:57–16:41:23；逐 Job 见 JSON | 三平台 / 全部适用 Job success | 27/27；其中 Windows 8/8 |
| 候选身份与离线守卫定向 pytest | `targeted-7.xml`，24.630s | 本机 Windows / 0 | 7/7，零失败/错误/skip |
| `python -B scripts/wp4d_verify_scope.py` | 固定内容提交，输出 `scope.json` | 本机 Windows 及两个 CI source / 0 | 原业务断言、19/19 canonical、21/21 字节、两套冻结测试树保持 |

已有完整回归共 1912 项；新增 WP4D 测试 19 项，合计 1931。RC 新增 15 个 Job（build 1、完整 source 2、consumer 12）全部通过，加既有 27 个适用 Job，内容 HEAD 总计 **42/42**。两项仅 pull_request 执行的 Stability Charter / Tool Contract 在本 push 事件不适用，未计为通过。

固定运行：[Core](https://github.com/joinwell52-AI/FCoP/actions/runs/34377729431)、[MCP](https://github.com/joinwell52-AI/FCoP/actions/runs/34377729147)、[RC](https://github.com/joinwell52-AI/FCoP/actions/runs/34377729223)。

## 远端第一组制品与来源

Actions artifact `10114578638`（`wp4d-candidates-first-set`），由 run `34377729223` 构建后下载逐字节核验。候选机器 Manifest SHA-256：`148915cde716d63284950ed46f9250e55b182885b23209cb56ac7d70d5b7dc8c`。两轮全新目录构建，不复用失败运行产物，不手改机器 Manifest。SOURCE_DATE_EPOCH=`1788940367`。

| 文件 | bytes | SHA-256 |
|---|---:|---|
| fcop-4.0.0rc1-py3-none-any.whl | 726280 | b539fdd496d52ea608b5f42abd270c2ed04e8f011242d932ddedac48f8d7cee9 |
| fcop-4.0.0rc1.tar.gz | 647881 | 43e4488af52bffac3e400c14f442136f955ee0477ddf0e94386481e6ec682bb4 |
| fcop_mcp-4.0.0rc1-py3-none-any.whl | 117937 | 20167b314de1a90093b74cf42c7039edceddc1458e1b37ce3e9e6f31697c773a |
| fcop_mcp-4.0.0rc1.tar.gz | 109420 | eefde60b6d156f5ef2184186f5f5a355837f0fc9e0244b3e2d8077dbed51000b |

工具身份全部精确校验：build 1.4.2、hatchling 1.32.0、setuptools 82.0.1、wheel 0.45.1、twine 7.0.0、packaging 26.3。四制品 Metadata-Version 均为合法 2.5，没有降级/伪造。

最终 Manifest HEAD 会重新构建上述**同一个候选内容提交**，并明确记录不同的 `execution_head`。只剥离连续、单父的 WP4D evidence/report/Manifest 提交；任何源文件、样例或测试变化都会改变候选身份。最终运行的机器 Manifest 含新的运行时间、run_id 和 execution_head，因此其自身摘要不能冒用这里的内容运行摘要；最终回读回执必须另列实际值并再次核验四制品及全部 12 consumer 的身份绑定。

## 证据解释与历史保留

主证据目录：`tests/rc/evidence/wp4d/final-content/`。机器 Manifest 保留下载字节；consumer-results 是 12 份原始 result.json 的无字段改写聚合；CI/artifact JSON 是 GitHub API 回读；JUnit 仅补最终 LF；日志摘录仅统一 LF、去 BOM/行尾空白，并标出来源 Job。源码 parity 与安装态证据明确分开。

本地 CodeFlowMu shadow 输出 `shadow.json` 保留固定 14 文件结果、安装路径、前后 inventory 相等结论及 inventory SHA-256；无关的全部下游文件名清单不上传，原始完整清单仍在该 JSON 标明的本地路径，记录其字节数与摘要。未执行 CodeFlowMu，未改它的 tracked/untracked 文件。

验证修复逐项与真实中间失败在 `tests/rc/evidence/wp4d/socketpair-resume/REPAIR-LEDGER.md`。以前的 BLOCKED 提交、报告和日志均保留；其状态仅适用于对应历史提交，不代表本次内容仍阻断。原 `D:/FCoP` 与 dogfood 未迁移、未重新部署。main、CodeFlowMu、发布状态未修改。


---

## 历史报告原文：以下 BLOCKED 状态仅属于历史提交

# WP4D 工具链勘误续作：RESULT — BLOCKED

## 当前裁定后的续作结果（2026-09-09；以下历史原文保持不动）

```yaml
WP4D_STATUS: BLOCKED
AUTHORIZED_SCOPE: WP4D_TWINE_METADATA_2_5_TOOLCHAIN_ONLY_AND_WP4D_RESUME
TOOLCHAIN_ERRATUM_COMMIT: 086c358f4c96e21aa31890d147eacae4a359a11a
TOOLCHAIN_ERRATUM_SHA256: 03da08ed72ffe438d49a65bb8f87e5b9b2e2e6a917fb8d9cfb945dade02eb2e4
TOOLCHAIN_ERRATUM_BYTES: 7224
TOOLCHAIN_RESUME_BASE: 700e9e1ecb3eb02e5860094175ba7f8099141695
TOOLCHAIN_FIX_COMMIT: b472be32a2623de77d0fb9b2c301960620383e27
TWINE_VERSION: 7.0.0
PACKAGING_VERSION: 26.3
METADATA_VERSION_OBSERVED: "2.5"
TWINE_CHECKS: 2/2
ARTIFACT_REPRODUCIBILITY: 4/4
FAILED_RUN_ARTIFACTS_REUSED: false
NEW_BLOCKER: WINDOWS_310_311_MCP_SAMPLE_OFFLINE_GUARD_REJECTS_STDLIB_SOCKETPAIR
RC_CONSUMER_MATRIX: 10 passed / 2 failed / 12 total
REQUESTED_GATE: NONE
```

任务书已从 GitHub 固定提交获取并核验字节和摘要；PR #31 的 [ADMIN 裁定](https://github.com/joinwell52-AI/FCoP/pull/31#issuecomment-5603988787) 与两文件范围一致。b472be3 是 RESUME_BASE 的直接子提交，只修改 workflow 的 Twine/packaging 精确 pin，以及 build 脚本工具身份记录列表；每文件各一行，无其他逻辑变化，Ruff 和 diff --check 通过。

Twine 阻断已关闭，新构建的四制品已上传 Actions artifact 并下载回读核验。两组各四次 Twine 检查均通过（2/2 组、8/8 文件检查）；六个工具身份精确匹配、合法 Metadata 2.5 未修改。新问题来自此前由执行人编写的第三方样例网络隔离守卫，不是 Twine 再次失败，也不能据此断言 FCoP Core 有缺陷。

Windows 3.10/3.11 的真实 stdio server 在 asyncio Proactor 建立内部 self-pipe 时，标准库 socket.socketpair 调用 socket.bind。样例 server.py:15 只放行 _fallback_socketpair，因函数名不匹配在第 17 行拒绝，尚未完成 MCP initialize。两份服务端 traceback 固定在 tests/rc/evidence/wp4d/toolchain-resume/。其余十组 wheel 和 sdist 安装态均通过，但两失败组的 sdist 路径没有执行，不能报 12/12。

按原任务书 §13.2 和本勘误 §8，发现适用矩阵失败后停止候选内容修改。未修改样例、网络守卫、Core/MCP、冻结 Conformance、Schema、规则或任何发布配置；未放宽网络边界。只收口报告、证据、Manifest。请求 ADMIN 对样例中标准库内部 socketpair 的跨 Python 兼容边界作定点裁定，继续保持真实网络访问禁用；本轮不执行该修正。

本轮固定内容 CI：[Core 34367862474](https://github.com/joinwell52-AI/FCoP/actions/runs/34367862474)、[MCP 34367862401](https://github.com/joinwell52-AI/FCoP/actions/runs/34367862401)、[RC 34367862396](https://github.com/joinwell52-AI/FCoP/actions/runs/34367862396)。27/27 既有适用 Job 与 8/8 既有 Windows Job 通过；两项 PR-only skipped 为不适用，不计通过。RC source/build 通过，但 2 个 consumer 失败，因此整体失败。上述结果均绑定 b472be3，不能冒充之后 Manifest HEAD 全绿。

## 完整回执与可复核证据

```yaml
TOOLCHAIN_CORRECTION: PASS
TOOLS_IDENTITY: 6/6
TWINE_CHECKS: 2/2
REPRODUCIBILITY: 4/4
UBUNTU_NEW_HEAD_FULL: 1924/1924
UBUNTU_FAILURE_ERROR_SKIP: 0/0/0
WINDOWS_LOCAL_NEW_HEAD_FULL: INTERRUPTED_NOT_ACCEPTED
EXISTING_CI: 27/27
EXISTING_WINDOWS_CI: 8/8
RC_CONSUMERS: 10/12
RC_CONSUMER_FAILURES: 2
RC_CONSUMER_SKIPS: 0
RC_WINDOWS_CONSUMERS: 2/4
INSTALLED_ORIGIN_PATHS_COMPLETE: 20/24
CODEFLOWMU_SHADOW: NOT_RUN
CANONICAL_FILES: 19/19
FROZEN_BYTES: 21/21
FROZEN_CONFORMANCE_MODIFIED: 0
FINAL_MANIFEST_CI: NOT_CLAIMED_GREEN
REQUESTED_GATE: NONE
```

命令与执行边界：
- python -m pip install build==1.4.2 hatchling==1.32.0 setuptools==82.0.1 wheel==0.45.1 twine==7.0.0 packaging==26.3：实际 build Job 成功。
- python -B scripts/wp4d_build.py "$RUNNER_TEMP/rc-build"：UTC 15:05:05.613250–15:05:10.914881，退出 0，2 组/4 制品可复现，8 次文件 Twine PASSED。
- python -B -m pytest tests/test_fcop tests/conformance/v4 tests/test_fcop_mcp tests/conformance/rule_distribution_v4 -q --junitxml="$RUNNER_TEMP/full.xml"：Ubuntu 1924/1924，无失败/错误/skip，suite 103.370s。
- python -B scripts/wp4d_consume.py <candidate-input> <manifest-sha> <historical-input> <historical-sha> <consumer-evidence>：12 组同制品执行；10 组退出 0，Windows 3.10/3.11 退出 1。各组实际命令、runner 版本和开始/结束在固定 Actions Job 与 ci-jobs.json；成功安装结果含自身 UTC 时间。
- 本地 Windows 命令使用相同四套测试路径，附 -x -p no:cacheprovider --basetemp=D:/fcop-wp4d-twine7-full-01 --junitxml=C:/Users/Administrator/AppData/Local/Temp/fcop-wp4d-twine7-full-01.xml。本次 full 在新阻断后停止，不宣称 1924 完成，不引用旧头的通过数。
- python -B -m ruff check scripts/wp4d_build.py、git diff --check 通过；最终提交范围只两文件各一行，旧 guard/assertions 未变。

| 制品 | bytes | 远端第一组 SHA-256 |
|---|---:|---|
| fcop-4.0.0rc1-py3-none-any.whl | 726280 | b539fdd496d52ea608b5f42abd270c2ed04e8f011242d932ddedac48f8d7cee9 |
| fcop-4.0.0rc1.tar.gz | 647881 | 43e4488af52bffac3e400c14f442136f955ee0477ddf0e94386481e6ec682bb4 |
| fcop_mcp-4.0.0rc1-py3-none-any.whl | 117937 | 20167b314de1a90093b74cf42c7039edceddc1458e1b37ce3e9e6f31697c773a |
| fcop_mcp-4.0.0rc1.tar.gz | 109420 | eefde60b6d156f5ef2184186f5f5a355837f0fc9e0244b3e2d8077dbed51000b |

| 证据副本 | bytes | SHA-256 |
|---|---:|---|
| tests/rc/evidence/wp4d/toolchain-resume/actions-artifacts.json | 14166 | 9d4072741abcbf095347af28416c509fe97a81021da836f1e72766ec3fd49bd3 |
| tests/rc/evidence/wp4d/toolchain-resume/build.log | 7097 | f377bbef5d3ae8a9797706ef883d476f1b2fdee14565df58d97ce45f324c496e |
| tests/rc/evidence/wp4d/toolchain-resume/candidate-manifest.json | 6782 | f8bdcdbd1d39278a8ab481ab6e41157525ddcd52bcb9c37ab4e91e5dac3c4ad5 |
| tests/rc/evidence/wp4d/toolchain-resume/ci-jobs.json | 167772 | 58a2c35758b5e659d47fcae357d82da4a6eb157f4cc52ad01d5ff077fa074ffc |
| tests/rc/evidence/wp4d/toolchain-resume/consumer-results.json | 67450 | 782a00cc2551d2114ec1517508ab6ec189ee29639de81537b4ab52e53d591707 |
| tests/rc/evidence/wp4d/toolchain-resume/ubuntu-full-1924.xml | 454732 | 9afb9d7742075450b09bfc5b7edd8a571a61d7a43c6e64eb90016db08c5bd92f |
| tests/rc/evidence/wp4d/toolchain-resume/windows-310-server.log | 2729 | de66e0b3a39e5535edcda3bc5fb22bbfcd7dc78f14573214cddc878a3a3d6daa |
| tests/rc/evidence/wp4d/toolchain-resume/windows-311-server.log | 2877 | 0314719025a2c91ff44c1e228fc26226d3ac432309ddab2fd8c9213dfe7ccc6e |

证据来源：GitHub run 34367862396 的 artifacts、GitHub Jobs API，以及本机读取到的固定下载字节。candidate-manifest.json 保持远端原始字节；consumer-results.json 是十份原始 result.json 的 JSON 数组汇总，字段和值未改；CI/artifact JSON 是 API 响应格式化。展示日志只统一 LF、去掉 BOM/行尾空格，错误内容未变；XML 仅补最终 LF。原下载均保留在 Temp/wp4d-b472be3-*，不删除旧失败证据。表中证据副本摘要将在 Manifest 最终远端逐项复核，制品摘要已由远端下载核验。

新阻断事实：Windows stdlib socket.py 的 socketpair 名称与样例只识别 _fallback_socketpair 不一致；见 windows-310-server.log、windows-311-server.log。已有源码/3.12 检查未覆盖旧 Python 的名称差异，这是执行人候选证明样例的跨版本缺口。没有认定生产协议错误，也不提议放行任意 loopback 流量。请 ADMIN 定点授权安全收窄的样例兼容修正后再恢复全部最终 HEAD 验收。

所有历史 BLOCKED 文本保留如下。原 D:/FCoP、旧 worktree、dogfood、main 及 CodeFlowMu 未修改。当前只交付证据与 Manifest，PR #31 保持 Draft；不请求或签署 Gate。

---

## 历史快照：截至 700e9e1 的原报告（全部保留）

以下包含前两次 BLOCKED 的事实，其状态仅适用于历史提交；当前状态以本报告顶部为准。

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
