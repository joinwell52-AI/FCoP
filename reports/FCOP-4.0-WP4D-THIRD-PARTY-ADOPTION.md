# WP4D FCoP 候选收口 — THIRD-PARTY-ADOPTION

## 当前收口说明：撤回额外静默窗口要求

ADMIN 已明确：本轮只是升级 FCoP；CodeFlowMu 当前仅采用 FCoP <4.0，不是本轮升级、部署或验证现场协调的对象。执行人不再读取、协调、暂停或修改活动 CodeFlowMu，也不要求它为 FCoP 收口提供静默窗口。

执行人此前把附加计时复验遇到的外部文件变化提升成必须由 ADMIN 协调的阻断，判断不当，现撤回该升级判定。该说明不把失败改成 PASS：四次附加复验及旧 BLOCKED 回执完整保留为历史记录。固定候选 d1a86f3 的首次既有 14/14 证据及全树 MATCH 已从本地原始 3832169 bytes 证据再次核对摘要、结果和 inventory 摘要，候选内容自此没有改变；这里只复核已有 FCoP 证据，不重新访问 CodeFlowMu。

这是兼容性历史证明，不是 CodeFlowMu 采用、运行或升级为 4.0 的证明；runtime_consumption_verified 仍为 null，deployed=false。首次成功运行的精确起止时间没有单独采集，不补造计时；后续失败窗口的计时不能充当首次成功的计时。

本轮后续仅完成 FCoP 六份报告、证据、Manifest-only 提交、GitHub 回读及最终 HEAD CI。候选内容验证已通过；最终交付状态须以最终 HEAD 的追加回执为准，不能提前宣称其 CI 已通过。只请求 FCOP_4_RC_ACCEPTED，不自行签署，不合并或发布。

---

## 既有验证记录（后续陈旧状态以顶部收口说明为准）

# WP4D THIRD-PARTY-ADOPTION — 候选内容验证通过

## 真实第三方采用证明

12/12 组合全部完成 wheel 和 sdist 两条路径，共 24/24。安装后复制最小样例到仓库外目录：Python-only 只依赖安装态 Project；MCP-only 客户端不 import fcop/fcop_mcp，通过 stdio JSON-RPC 启动独立服务进程，先发现工具再调用。

每个 origin 都完成普通顺序任务、一层 Branch、显式 convergence、T7、进程关闭后 reopen。两类客户端最终状态一致：archive / archive / done / inbox，15 次迁移。MCP 运行两个独立服务进程、完整复验 46/12/4。安装身份与机器摘要来自 result.json，源码 parity 从未计作 clean-room 通过。

离线守卫只依赖预先捕获的 stdlib socketpair code object 身份。真实 socketpair 通过；普通 bind/connect/getaddrinfo/sendto 和伪造 stdlib 文件名/函数名均拒绝；守卫回归在三平台 12 个 Python Job 中逐项 PASSED（guard-matrix.json）。

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

# WP4D 工具链勘误续作：THIRD-PARTY-ADOPTION — BLOCKED

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

## 真实安装态的部分成功与失败

十个完整成功组合：Ubuntu 3.10/3.11/3.12/3.13、macOS 3.10/3.11/3.12/3.13、Windows 3.12/3.13。每组均从同一 manifest 的第一组文件安装 wheel 与 sdist，使用仓库外 venv，未设置源码 PYTHONPATH；两个样例输出、版本错配以及来源证明记录在 consumer-results.json。共 20 条成功安装来源路径，但不是 24/24。

Windows 3.10 与 3.11 组在 wheel 安装后的 MCP initialize 之前失败，未完成这一组的 MCP 采用、legacy/mismatch 后续检查和 sdist 分支。客户端报 Server exited 只是表象；server-1.log 的根异常是样例 offline 守卫拒绝 socket.bind。它拦截的是标准库建立事件循环的内部 self-pipe，不是任务操作请求；未用模拟返回或私有接口绕过。

需要修正的位置属于 examples/v4/third-party/mcp-only/server.py，不在本次两文件勘误白名单。没有实施修正，也没有扩大到 Core/MCP。

---

## 历史快照：截至 700e9e1 的原报告（全部保留）

以下包含前两次 BLOCKED 的事实，其状态仅适用于历史提交；当前状态以本报告顶部为准。

# WP4D 勘误续作：THIRD-PARTY-ADOPTION — BLOCKED

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

## 已验证的源码一致性与未运行的安装态

新增两个可复制外部样例及隔离构建/消费脚本，已作为候选内容提交保留：
- Python-only：只使用公共 Project API；顺序任务、一层 Branch、显式 convergence、T7、真实进程终止/重开、相同 operation_id 的 Existing 重试。
- MCP-only：客户端不 import fcop/fcop_mcp，以 stdio JSON-RPC 连接可信启动配置的服务进程；发现 46 tools / 12 resources / 4 templates；两个真实服务进程覆盖同样的流程与响应丢失重试。
- Profile evaluator 仅在可信 Project/Toolkit 初始化处注册。示例的固定 proof 是教学夹具，不是生产身份验证方案；业务请求不能携带裁判。
- 两个样例的确定性语义摘要均为阶段 `archive, archive, done, inbox` 与 15 个 transition；文件路径等来源字段随测试临时目录变化，不能把它们宣称为跨运行字节相同的整个输出。

原生 Windows 执行 `python -B scripts/wp4d_source.py`，副本位于 `C:/Users/Administrator/AppData/Local/Temp/wp4d-source-jq0ayhjn`；目录创建 UTC 14:25:08.896629，Python 日志完成 14:25:44.910230，MCP 日志完成 14:26:09.371575，命令退出 0。这是提交前与 dd813868 内容相同的源码候选验证，明确使用 SOURCE_ONLY。日志：[Python](../tests/rc/evidence/wp4d/native-source-python.log)、[MCP](../tests/rc/evidence/wp4d/native-source-mcp.log)。

固定内容提交的 Ubuntu [源码 Job](https://github.com/joinwell52-AI/FCoP/actions/runs/34363703047/job/102506904899) 再执行同一命令，UTC 14:29:46–14:29:53，步骤成功；不将此计为 clean-room。

`scripts/wp4d_consume.py` 的安装态代码和 12 组合 workflow 已保留，但构建上游失败，consumer 依赖 Job 被 skipped，没有实际启动 12 个单元。因此 wheel/sdist 两来源、安装包 site-packages 来源证明、安装态错配、三平台最小项目均为 NOT_RUN。严禁把两个源码样例 PASS 写成 12/12。

---

## 历史快照：原 BLOCKED 报告原文保留

以下原文固定在 893e5c55f9f7ea433c6c518c76534218a4cf9570；其中“未运行”和旧 skip 仅描述该历史提交，不是上述续作后的当前结论。

# WP4D 第三方采用：NOT_RUN

未发布候选尚无通过验收的四制品，Python-only、MCP-only 与 12 组合 consumer 未执行，不能用源码测试替代安装态采用证明。

| 证明 | 结果 | 已完成/要求 |
|---|---|---|
| 仓库外 Python-only 顺序/Branch/convergence/reopen | NOT_RUN | 0/12 |
| 外部 stdio JSON-RPC MCP-only 项目 | NOT_RUN | 0/12 |
| wheel/sdist 新 venv 来源核验 | NOT_RUN | 0/12 |
| 12 组合应用禁网与确定性摘要 | NOT_RUN | 0/12 |
| 候选安装态 MCP 46/12/4 发现 | NOT_RUN | 未测 |

这些探针无实际命令启动，起止时间、退出码、失败/skip 数及 Actions URL 均 N/A（未运行，不是零失败通过）；制品 SHA-256 为 NOT_GENERATED。
源码身份检查使用显式 PYTHONPATH，已经明确标为 SOURCE_ONLY，不符合 clean-room 条件。没有提交或声称第三方项目已完成。

## 执行身份与证据口径

- 唯一任务书：`cbdc60a92a02b9e2eb0c1c6e2e93f74c335407f9`，SHA-256 `bfc93f595800efe5185588ff92b612c9ca66e1622118e76c805d5fd908a1e290`，18471 bytes。
- 已验收实现基线：`167c5fd4ca4c9603c392bae3a4a055963e7b7ed6`；未发布候选内容提交：`4160fc5d216f784bee6b35902b507fff8e0ba6f6`。
- 环境：Windows 10 build 19045 / Python 3.12.9；时区 +08:00；独立工作树 `D:/FCoP-wp4d-rc-candidate`。
- Draft PR：[31](https://github.com/joinwell52-AI/FCoP/pull/31)，base 为 `task/fcop-4.0-wp4d-rc-candidate`，不指向 main。
- 本报告为 BLOCKED 证据，不是 RC 验收或发布证明。具体命令、起止时间、退出码、测试数、日志和哈希见 [RESULT](FCOP-4.0-WP4D-RESULT.md)。
- 尚未构建四个 RC 制品，故 artifact SHA-256 均为 NOT_GENERATED；安装态、12 组合和最终 HEAD CI 未验收，不能沿用父 Gate 的通过数。
