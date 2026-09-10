# WP4D FCoP 候选收口 — CI-AND-RELEASE-READINESS

## 当前收口说明：撤回额外静默窗口要求

ADMIN 已明确：本轮只是升级 FCoP；CodeFlowMu 当前仅采用 FCoP <4.0，不是本轮升级、部署或验证现场协调的对象。执行人不再读取、协调、暂停或修改活动 CodeFlowMu，也不要求它为 FCoP 收口提供静默窗口。

执行人此前把附加计时复验遇到的外部文件变化提升成必须由 ADMIN 协调的阻断，判断不当，现撤回该升级判定。该说明不把失败改成 PASS：四次附加复验及旧 BLOCKED 回执完整保留为历史记录。固定候选 d1a86f3 的首次既有 14/14 证据及全树 MATCH 已从本地原始 3832169 bytes 证据再次核对摘要、结果和 inventory 摘要，候选内容自此没有改变；这里只复核已有 FCoP 证据，不重新访问 CodeFlowMu。

这是兼容性历史证明，不是 CodeFlowMu 采用、运行或升级为 4.0 的证明；runtime_consumption_verified 仍为 null，deployed=false。首次成功运行的精确起止时间没有单独采集，不补造计时；后续失败窗口的计时不能充当首次成功的计时。

本轮后续仅完成 FCoP 六份报告、证据、Manifest-only 提交、GitHub 回读及最终 HEAD CI。候选内容验证已通过；最终交付状态须以最终 HEAD 的追加回执为准，不能提前宣称其 CI 已通过。只请求 FCOP_4_RC_ACCEPTED，不自行签署，不合并或发布。

---

## 既有验证记录（后续陈旧状态以顶部收口说明为准）

# WP4D CI-AND-RELEASE-READINESS — 候选内容验证通过

## 发布流程只读审计：尚不具备发布授权

只读取 `.github/workflows/release.yml`，没有触发它，也没有修改 workflow 字节。现流程匹配 v* tag，并允许 workflow_dispatch；PyPI 发布条件使用 push 或 dry_run=false；没有 ADMIN protected environment；工具版本未固定；它会自己重新 build，而不是绑定本次审核候选的四个原始字节；GitHub Release 创建未明确区分 RC/stable。

后续必须由独立任务书授权并硬化：精确 tag/版本一致性与受保护来源、RC 与 stable 分支/标识、ADMIN protected environment、绑定已审核同一四制品及摘要、发布后从 PyPI 回装核验、最小发布权限与完整可追踪性。现有流程没有执行这些后续动作，本次不通过实际发布来测试发布配置。公开 RC、stable、PyPI、GitHub Release、MCP Registry、Zenodo、tag、main 合并均为未授权/未运行，不记 PASS。

内容 CI 42/42 与最终 Manifest HEAD CI 是两次独立事实。最终完成回执只能在后者也全绿、远端文件全部回读后发布；这里的旧内容运行不能替代最终 CI。

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

# WP4D 工具链勘误续作：CI-AND-RELEASE-READINESS — BLOCKED

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

## 固定内容 CI 与发布边界

本次三个 workflow 已全部结束。Core 14 个适用 Job、MCP 13 个适用 Job 全部通过，既有 Windows 矩阵 8/8。RC source/build 两 Job 通过，consumer 10/12 通过、2/12 失败，无 consumer skip；Windows RC consumer 为 2/4，不能与既有 Windows 8/8 混写。

Ubuntu 本轮 full JUnit：1924 tests / 0 failures / 0 errors / 0 skipped，时间 103.370s；开始 UTC 15:05:18.595592，按 suite 耗时计算结束 15:07:01.965592。精确 Job 步骤起止时间和状态在 ci-jobs.json。Windows 本地 full 因停止条件中断，不满足最终 HEAD 要求。随后证据/Manifest 提交不继承候选内容的绿色声明。

release.yml、mcp/server.json、CITATION.cff 均未变，未执行发布命令；原报告记录的 tag 约束、RC/stable 区分、ADMIN protected environment、同制品发布和 PyPI 回装核验仍须独立授权。无 main、tag、registry、Release、Zenodo 或 CodeFlowMu 写入。

---

## 历史快照：截至 700e9e1 的原报告（全部保留）

以下包含前两次 BLOCKED 的事实，其状态仅适用于历史提交；当前状态以本报告顶部为准。

# WP4D 勘误续作：CI-AND-RELEASE-READINESS — BLOCKED

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

## 固定候选内容提交的 CI 结果

[完整 GitHub API 状态快照](../tests/rc/evidence/wp4d/content-ci-snapshot.json) 固定在 dd8138684006432c6bb62c952909a59cda20adaf，三个 run 均已结束。

| Workflow | 固定 Run | 结论 | 适用项 |
|---|---:|---|---|
| test-fcop | 34363703057 | SUCCESS | 14/14；含 12 矩阵、coverage、package |
| test-fcop-mcp | 34363702991 | SUCCESS | 13/13；含 12 矩阵、package |
| rc-candidate | 34363703047 | FAILURE | source 通过，build 失败，consumer 未运行 |

既有适用 Job 合计 27/27，Windows 8/8。两个 PR-only Job 被 skipped，是不适用，不计为通过。新增 RC consumer 因依赖失败而 skipped 是未完成强制项，**不属于不适用**。

Ubuntu source 的合并回归为 1924/1924，零失败/错误/skip；源码样例也成功。RC build 的工具组合拒绝 Metadata 2.5，故不能请求 FCOP_4_RC_ACCEPTED。旧 package jobs 的成功不证明本轮固定四制品复现，更不代替安装态 consumer。

上述是候选内容 HEAD，不是未来 Manifest HEAD 全绿证明。后续证据/Manifest 提交不会修复未改变的 Twine pin，最终 RC 验收状态仍为 BLOCKED；不得重复绿色 CI 描述来掩盖该失败。

`release.yml` 本轮再次只读复核，未修改、未触发。下方历史发布差距表继续有效：v* tag 过滤、RC/stable 分流、ADMIN protected environment、精确采用已验收同制品、发布后回装核验仍需下一份独立授权。新 RC workflow 仅 contents:read，无发布 environment/secrets、tag 或 registry 上传；Actions artifact 不等于公开发布。

---

## 历史快照：原 BLOCKED 报告原文保留

以下原文固定在 893e5c55f9f7ea433c6c518c76534218a4cf9570；其中“未运行”和旧 skip 仅描述该历史提交，不是上述续作后的当前结论。

# WP4D CI 与发布准备：BLOCKED，未授权发布

现有分支 push CI 可以运行，但本次交付不是满足完整 WP4D 的候选。最终 Manifest HEAD 的 27/27、Windows 8/8 和新增 RC build/12 consumer 验收均未完成，不记为 PASS。未新增 RC workflow，未手动触发 release workflow。

[PR #31 checks](https://github.com/joinwell52-AI/FCoP/pull/31/checks) 是实时状态入口；它不是本报告声称通过的固定 CI 证据。后续任何绿色旧 CI 也不能消除旧测试 skip 或代替缺失的 RC workflow。

本地静态守卫在 2026-09-09 17:23:11–17:23:12 +08:00 执行：

```text
python -B -m ruff check --no-cache src tests scripts/fcop_rc_candidate_check.py
python -B -m ruff check --no-cache mcp/src tests/test_fcop_mcp
git diff cbdc60a92a02b9e2eb0c1c6e2e93f74c335407f9 --check
```

三项退出 0；静态检查不产生测试 pass/skip 计数。未发布制品 SHA-256 为 NOT_GENERATED。

## 只读 release workflow 审计

读取 [固定 release.yml](https://github.com/joinwell52-AI/FCoP/blob/4160fc5d216f784bee6b35902b507fff8e0ba6f6/.github/workflows/release.yml)，2026-09-09 17:21:29–17:21:31 +08:00，读取命令 `Get-Content .github/workflows/release.yml -Encoding UTF8` 退出 0，没有触发。

| 观察 | 后续独立授权所需工作 |
|---|---|
| push 匹配 v*，另有 workflow_dispatch；版本审计不能替代 ADMIN Gate | 精确 tag/候选提交/Gate 绑定和防误触发 |
| 发布任务没有区分 RC/stable 的明确策略，gh release create 无 prerelease 标记 | 明确 RC 与 stable 分流及公开标记 |
| 发布使用 PyPI token，无 ADMIN protected environment | 人工保护环境和发布授权门 |
| build job 重新从 checkout 构建，无本轮四制品哈希绑定 | 精确采用已验收的同一制品并验证全部哈希 |
| 构建工具未固定，artifact 保留 30 天 | 固定工具与可复现参数、artifact 到期处理 |
| smoke install 在上传前进行，没有公开 PyPI 下载后同制品回装比对 | 发布后独立回装与哈希核验 |
| release audit 会检查 server.json/CITATION 等发布面 | 与未发布 RC 保留 3.2.5 公共元数据的边界分开，不能为了运行发布流程提前重标 |

上述均为未来差距记录，不是当前允许修改的内容。release.yml、server.json、CITATION 保持原 Blob。main、tag、PyPI、GitHub Release、MCP Registry、Zenodo 和 CodeFlowMu 无变更授权；本次未执行这些操作。

## 执行身份与证据口径

- 唯一任务书：`cbdc60a92a02b9e2eb0c1c6e2e93f74c335407f9`，SHA-256 `bfc93f595800efe5185588ff92b612c9ca66e1622118e76c805d5fd908a1e290`，18471 bytes。
- 已验收实现基线：`167c5fd4ca4c9603c392bae3a4a055963e7b7ed6`；未发布候选内容提交：`4160fc5d216f784bee6b35902b507fff8e0ba6f6`。
- 环境：Windows 10 build 19045 / Python 3.12.9；时区 +08:00；独立工作树 `D:/FCoP-wp4d-rc-candidate`。
- Draft PR：[31](https://github.com/joinwell52-AI/FCoP/pull/31)，base 为 `task/fcop-4.0-wp4d-rc-candidate`，不指向 main。
- 本报告为 BLOCKED 证据，不是 RC 验收或发布证明。具体命令、起止时间、退出码、测试数、日志和哈希见 [RESULT](FCOP-4.0-WP4D-RESULT.md)。
- 尚未构建四个 RC 制品，故 artifact SHA-256 均为 NOT_GENERATED；安装态、12 组合和最终 HEAD CI 未验收，不能沿用父 Gate 的通过数。
