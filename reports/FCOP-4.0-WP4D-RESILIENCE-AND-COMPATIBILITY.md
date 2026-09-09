# WP4D FCoP 候选收口 — RESILIENCE-AND-COMPATIBILITY

## 当前收口说明：撤回额外静默窗口要求

ADMIN 已明确：本轮只是升级 FCoP；CodeFlowMu 当前仅采用 FCoP <4.0，不是本轮升级、部署或验证现场协调的对象。执行人不再读取、协调、暂停或修改活动 CodeFlowMu，也不要求它为 FCoP 收口提供静默窗口。

执行人此前把附加计时复验遇到的外部文件变化提升成必须由 ADMIN 协调的阻断，判断不当，现撤回该升级判定。该说明不把失败改成 PASS：四次附加复验及旧 BLOCKED 回执完整保留为历史记录。固定候选 d1a86f3 的首次既有 14/14 证据及全树 MATCH 已从本地原始 3832169 bytes 证据再次核对摘要、结果和 inventory 摘要，候选内容自此没有改变；这里只复核已有 FCoP 证据，不重新访问 CodeFlowMu。

这是兼容性历史证明，不是 CodeFlowMu 采用、运行或升级为 4.0 的证明；runtime_consumption_verified 仍为 null，deployed=false。首次成功运行的精确起止时间没有单独采集，不补造计时；后续失败窗口的计时不能充当首次成功的计时。

本轮后续仅完成 FCoP 六份报告、证据、Manifest-only 提交、GitHub 回读及最终 HEAD CI。候选内容验证已通过；最终交付状态须以最终 HEAD 的追加回执为准，不能提前宣称其 CI 已通过。只请求 FCOP_4_RC_ACCEPTED，不自行签署，不合并或发布。

---

## 既有验证记录（后续陈旧状态以顶部收口说明为准）

# WP4D RESILIENCE-AND-COMPATIBILITY — 候选内容验证通过

## 恢复、幂等与兼容性

Python-only 在公开变更持久化之后由父进程 kill，随后新进程从磁盘 inspect；MCP 客户端在变更完成后丢弃响应，以相同操作身份重试，再关闭和新进程 reopen。全部 24 origin 的 exact_retry、disk_reopen、convergence 和零冲突效应通过；没有依赖进程内 monkeypatch 证明恢复。

Host 规则选择、缺失规则、digest 冲突、context overflow、deploy/rollback 及逐次拒绝零副作用由安装态样例中的完整快照断言执行，host_rollback 全部 true。固定旧版本生成的 3.2.5 fixture 在新包读取前后四文件 SHA-256 不变。

CodeFlowMu 固定消费者 ref 为 `b961b16dd0c8863ead6995d963fe0ca576a8abaa`，授权摘要 `206129e8a68db7d5da1ef345d04c5e28348c1f392eef11aaa44e96f1fe6cdafa`。真实安装态只读 shadow 为 14/14；检测到 fcop==3.2.5 / fcop-mcp==3.2.5，deploy=false，runtime_consumption_verified=null，不能声称 CodeFlowMu 已采用 RC。

首次本轮完整前后 inventory：tracked 14851、untracked 10406，canonical inventory SHA-256 `c2ef5998d3646e340dcd7196ff60c20c6986c92a233f43547e6434c8ef96e0ea`，零写入。首次精确起止时间未单独采集；附加计时复验的失败在 socketpair-resume/shadow-*.json 中保留，不覆盖第一次事实，不补造成功计时。

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

# WP4D 工具链勘误续作：RESILIENCE-AND-COMPATIBILITY — BLOCKED

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

## 恢复与零副作用证据的适用范围

十组成功 consumer 的 wheel/sdist 结果包含真实进程 kill/reopen、幂等重试、15 次迁移、Branch/convergence、Host 选择/拒绝/deploy/rollback、固定 legacy fixture 零漂移和包错配零副作用检查；逐组原始摘要见 consumer-results.json，不能用十组结果填补另外两组。

CodeFlowMu shadow 本轮尚未运行：已只读检查历史授权文件及历史报告以准备执行，但在安装矩阵失败后停止，未调用 shadow、运行产品、升级依赖或写 CodeFlowMu。因此本轮 14/14 为 NOT_RUN，不借用 WP4C.5B 结果。原历史 shadow 授权和快照未改。

Windows 本地完整回归启动于本次 b472be3 工作树，随后在新矩阵阻断确认后于 2026-09-09T23:09:34.2242519+08:00 停止了经命令行核验的本次 pytest 进程（PID 4620）。退出 1 为执行人终止，不是测试断言失败；未生成最终完整 JUnit，结果为 INTERRUPTED_NOT_ACCEPTED。原阻断 HEAD 的 1924/1924 不计本轮通过。

---

## 历史快照：截至 700e9e1 的原报告（全部保留）

以下包含前两次 BLOCKED 的事实，其状态仅适用于历史提交；当前状态以本报告顶部为准。

# WP4D 勘误续作：RESILIENCE-AND-COMPATIBILITY — BLOCKED

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

## 当前恢复与兼容证据边界

原生及 Ubuntu 源码样例通过以下真实调用：在已持久化边界外部 kill 进程，新进程从磁盘读取 TASK/transition/family digest/锁定规则上下文；响应丢失的创建请求返回 Existing，TASK 与事件不重复；不同摘要返回结构化 OPERATION_ID_CONFLICT 且整树快照不变。不是 parallel_surface_probe 或仅检查方法名。

Python 源码样例还通过临时目录内的 canonical 规则读取/选择、零写入计划、显式采用、Host deploy、精确 deploy retry、verify_deployment、rollback 与再次 rollback。版本冲突、规则缺失、字节 digest 冲突及 context overflow 分别拒绝且零副作用；runtime_consumption_verified 始终为 null。上述属于源码验证，日志、命令和起止时间见 THIRD-PARTY-ADOPTION/RESULT。

安装态仍未运行：四候选文件未通过 Twine，不能在本轮自行替换一组不同制品。3.2.5 固定历史 fixture producer、安装态双向版本错配、同一 wheel/sdist 的恢复/Host 证明和 14/14 CodeFlowMu shadow 均 NOT_RUN。没有修改、升级或部署 CodeFlowMu，也没有用父阶段 shadow 结果充当本轮结果。

固定内容提交本地及 Ubuntu scope guard 均通过：19/19 canonical 文件、21/21 规范/规则权威字节未变；Core Conformance tree 为 `24ab264c6bca9a3183ee270becb552f22a4c4f9e`，Distribution Conformance tree 为 `4f99c7261b63b6db81c500604a231defaca9f14b`。21 个 SHA-256 与下面历史权威字节表一致；两棵冻结测试树没有改写。

---

## 历史快照：原 BLOCKED 报告原文保留

以下原文固定在 893e5c55f9f7ea433c6c518c76534218a4cf9570；其中“未运行”和旧 skip 仅描述该历史提交，不是上述续作后的当前结论。

# WP4D 恢复与兼容性：守卫阻断，安装态验证未运行

修改前 1912 个现有节点完整通过，但未发布 RC 身份触发一个旧测试的提前 skip。不能把基线通过数移作候选恢复/兼容证据。

[固定未修改测试](https://github.com/joinwell52-AI/FCoP/blob/4160fc5d216f784bee6b35902b507fff8e0ba6f6/tests/test_fcop/test_audit.py#L242) 只读取版本第二段；`4.0.0rc1` 的 minor 为 0，因此在第 248 行 skip，未执行角色文档创建及最终 violations 断言。
[生产扫描逻辑](https://github.com/joinwell52-AI/FCoP/blob/4160fc5d216f784bee6b35902b507fff8e0ba6f6/src/fcop/project.py#L2422) 使用 major 与 minor 共同计算距离。源码阅读支持“旧测试前置条件忽略 major”的诊断，但没有执行被跳过的断言，故不据此宣称 RC 生产扫描已经通过。

没有修改旧测试、Core 扫描、Conformance、恢复或生命周期；需要 ADMIN 对该局部测试条件的明确裁定，不能在当前范围擅改。

| 安装态证明 | 状态 |
|---|---|
| response-loss 同身份重试与零重复效果 | NOT_RUN |
| 杀进程后磁盘恢复和锁定上下文 | NOT_RUN |
| 版本/缺失规则/digest/overflow 零副作用 | NOT_RUN |
| 固定 3.2.5 workspace 全树零漂移 | NOT_RUN |
| Host discover/select/deploy/rollback | NOT_RUN |
| CodeFlowMu 固定消费者 shadow 14/14 | NOT_RUN（0/14 已验证） |

这些项目无开始/结束、命令退出码或 Actions URL；均为 N/A，而非 PASS。没有运行 CodeFlowMu 或对其工作树写入，没有将旧 shadow 结果冒充本阶段。

## 冻结文件

17:24:29 +08:00，逐文件比较 `read_bytes()` 与 `git show 167c5fd4ca4c9603c392bae3a4a055963e7b7ed6:<path>`，21/21 字节不变，其中规则候选 19/19。Core Conformance tree 为 `24ab264c6bca9a3183ee270becb552f22a4c4f9e`；规则分发 Conformance tree 为 `4f99c7261b63b6db81c500604a231defaca9f14b`。

| 冻结文件 | SHA-256 |
|---|---|
| src/fcop/rules/_data/v4/authorization.en.md | 96c1c18bab3a879b51a1e2d0041f1f08eeae685185ad9489f13ed0a999f9a00b |
| src/fcop/rules/_data/v4/authorization.zh.md | 13b82fdeb7c577a68a70d94303bf090eac42ce44c137c1a166b23f7014c1b854 |
| src/fcop/rules/_data/v4/compatibility.en.md | a65385a3a2e68d043c65f9b8c34c6ac311bb7f9b2ea1e9f4c162886f858a64d8 |
| src/fcop/rules/_data/v4/compatibility.zh.md | d6ce267c8216a2d6df2e5e601f4d237d941778a36687eae1d310616f6170585e |
| src/fcop/rules/_data/v4/convergence.en.md | ec3cf38b6dba4d3eb8447cc7cd25e947c06abed228c37c9d651f873662edc70e |
| src/fcop/rules/_data/v4/convergence.zh.md | 2b5c2a52c33bc38e8c3c85fdd75d5de3c837cc483a29941ec02a61a059c1701a |
| src/fcop/rules/_data/v4/envelopes.en.md | 0405885cbe3fe791c0e1a6c76da004d093d58cd55159ffeb3ca8c89e4ec045a3 |
| src/fcop/rules/_data/v4/envelopes.zh.md | 0a69c9196e95185cf9e98b71af8c564be5797e26a71c5a9b7dc32d0735a08fef |
| src/fcop/rules/_data/v4/idempotency.en.md | 1b100010d36342e6d98e9031429b3e11aad5657dfa953031e43bc4c99772a16a |
| src/fcop/rules/_data/v4/idempotency.zh.md | 51c53931e02b1f39950f4a2f16b5e8e9a5f9d10b77f5ea1ad6b07c3e96385f08 |
| src/fcop/rules/_data/v4/lifecycle.en.md | b6356c078ab00b893379f0b4f558616444ef4a4aa0e17432460719a9be362b2b |
| src/fcop/rules/_data/v4/lifecycle.zh.md | 26b338914cffe2ea076f0e88133fc69617c91ecb149b3e40217baeef708cffef |
| src/fcop/rules/_data/v4/manifest.json | 7efb1ba14df4d1ffbe164b8ec85dbf4316e7da4c0f367f3a506c78e4e29862d4 |
| src/fcop/rules/_data/v4/recovery.en.md | aad4861efa59df69742c4bf577d57a553cbb170f6f92d61f6df74ec3ec503908 |
| src/fcop/rules/_data/v4/recovery.zh.md | b19226071498f6414e11379b9d67cee36e4a79d65510fffefd14a021cd829000 |
| src/fcop/rules/_data/v4/relations.en.md | 1b706c4ff76efb6edad40ab7985a0693eb9466da483d7024eb1f29668e022789 |
| src/fcop/rules/_data/v4/relations.zh.md | fa51c77a568dae7f7cf41242b612ae2b2963075004aaebef533334a0466d3d42 |
| src/fcop/rules/_data/v4/workspace.en.md | 06d4a9604fbab50ade36369f8f1d2950f099a241d659613cc78f1dd7e93555b3 |
| src/fcop/rules/_data/v4/workspace.zh.md | 617009dc95cf4bedd252491334f45cf61fa1fe8ccf935f2127e2a1da9a49e30b |
| spec/fcop-4.0-spec.md | 0c5005ec754ee71d735e02c9ea403adbc35e8dff9ce98c13d8a42040cacbc8e9 |
| spec/fcop-4.0-spec.zh.md | 7302983e8a6e2225470d3da8f2e768abd4dfcc1c7adbe17116a64dda7e357c19 |

## 执行身份与证据口径

- 唯一任务书：`cbdc60a92a02b9e2eb0c1c6e2e93f74c335407f9`，SHA-256 `bfc93f595800efe5185588ff92b612c9ca66e1622118e76c805d5fd908a1e290`，18471 bytes。
- 已验收实现基线：`167c5fd4ca4c9603c392bae3a4a055963e7b7ed6`；未发布候选内容提交：`4160fc5d216f784bee6b35902b507fff8e0ba6f6`。
- 环境：Windows 10 build 19045 / Python 3.12.9；时区 +08:00；独立工作树 `D:/FCoP-wp4d-rc-candidate`。
- Draft PR：[31](https://github.com/joinwell52-AI/FCoP/pull/31)，base 为 `task/fcop-4.0-wp4d-rc-candidate`，不指向 main。
- 本报告为 BLOCKED 证据，不是 RC 验收或发布证明。具体命令、起止时间、退出码、测试数、日志和哈希见 [RESULT](FCOP-4.0-WP4D-RESULT.md)。
- 尚未构建四个 RC 制品，故 artifact SHA-256 均为 NOT_GENERATED；安装态、12 组合和最终 HEAD CI 未验收，不能沿用父 Gate 的通过数。
