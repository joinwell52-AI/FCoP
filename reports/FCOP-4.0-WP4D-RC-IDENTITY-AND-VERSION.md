# WP4D FCoP 候选收口 — RC-IDENTITY-AND-VERSION

## 当前收口说明：撤回额外静默窗口要求

ADMIN 已明确：本轮只是升级 FCoP；CodeFlowMu 当前仅采用 FCoP <4.0，不是本轮升级、部署或验证现场协调的对象。执行人不再读取、协调、暂停或修改活动 CodeFlowMu，也不要求它为 FCoP 收口提供静默窗口。

执行人此前把附加计时复验遇到的外部文件变化提升成必须由 ADMIN 协调的阻断，判断不当，现撤回该升级判定。该说明不把失败改成 PASS：四次附加复验及旧 BLOCKED 回执完整保留为历史记录。固定候选 d1a86f3 的首次既有 14/14 证据及全树 MATCH 已从本地原始 3832169 bytes 证据再次核对摘要、结果和 inventory 摘要，候选内容自此没有改变；这里只复核已有 FCoP 证据，不重新访问 CodeFlowMu。

这是兼容性历史证明，不是 CodeFlowMu 采用、运行或升级为 4.0 的证明；runtime_consumption_verified 仍为 null，deployed=false。首次成功运行的精确起止时间没有单独采集，不补造计时；后续失败窗口的计时不能充当首次成功的计时。

本轮后续仅完成 FCoP 六份报告、证据、Manifest-only 提交、GitHub 回读及最终 HEAD CI。候选内容验证已通过；最终交付状态须以最终 HEAD 的追加回执为准，不能提前宣称其 CI 已通过。只请求 FCOP_4_RC_ACCEPTED，不自行签署，不合并或发布。

---

## 既有验证记录（后续陈旧状态以顶部收口说明为准）

# WP4D RC-IDENTITY-AND-VERSION — 候选内容验证通过

## 身份与公共面核验

24 个安装路径全部在各自临时 venv 的 site-packages，module.__version__ 与安装元数据一致，没有 PYTHONPATH 或 editable 源码代替。每个 origin 完成双向 3.2.5/4.0.0rc1 错配拒绝，精确错误 `toolkit:MCP_PACKAGE_INCOMPATIBLE` 且 workspace 零创建；恢复后再次检查正确双包身份。

MCP 公开面 46 tools / 12 static resources / 4 templates，在全部 24 个真实 stdio 客户端运行中一致；RC 标签/classifier 仍 Beta，未冒充 stable。版本、依赖 pin、生产兼容表在本次授权包内零变化。

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

# WP4D 工具链勘误续作：RC-IDENTITY-AND-VERSION — BLOCKED

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

## 身份边界

候选身份仍为 fcop==4.0.0rc1 / fcop-mcp==4.0.0rc1，没有改变双包版本或依赖合同。原审计 guard 修正没有回退，Ubuntu 完整回归重新覆盖该节点且无 skip。安装态成功的十组均记录 venv/site-packages 导入身份、两种安装来源及双向错配拒绝，见 consumer-results.json；失败组不以发现包版本正确冒充完整采用成功。

构建清单绑定提交 b472be32a2623de77d0fb9b2c301960620383e27，Python 3.12.14，SOURCE_DATE_EPOCH=1788940367，tools={build:1.4.2,hatchling:1.32.0,setuptools:82.0.1,wheel:0.45.1,twine:7.0.0,packaging:26.3}。下载后逐项断言身份与四个原始文件摘要，全通过。candidate-manifest.json 的原始远端 SHA-256 为 f8bdcdbd1d39278a8ab481ab6e41157525ddcd52bcb9c37ab4e91e5dac3c4ad5。

---

## 历史快照：截至 700e9e1 的原报告（全部保留）

以下包含前两次 BLOCKED 的事实，其状态仅适用于历史提交；当前状态以本报告顶部为准。

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
