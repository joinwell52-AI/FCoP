# WP4D 工具链勘误续作：ARTIFACT-REPRODUCIBILITY — BLOCKED

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

## 本次全新制品，不继承旧失败产物

构建 UTC 2026-09-09T15:05:05.613250+00:00 至 15:05:10.914881+00:00，Ubuntu/Python 3.12.14，命令 python -B scripts/wp4d_build.py "$RUNNER_TEMP/rc-build"，退出 0。两个全新 Git archive source 目录，分别构建双包 wheel/sdist；两组 twine check 均退出 0。raw_reproducibility=4/4。没有调整元数据、检查或构建逻辑。

| 制品 | bytes | 远端第一组 SHA-256 |
|---|---:|---|
| fcop-4.0.0rc1-py3-none-any.whl | 726280 | b539fdd496d52ea608b5f42abd270c2ed04e8f011242d932ddedac48f8d7cee9 |
| fcop-4.0.0rc1.tar.gz | 647881 | 43e4488af52bffac3e400c14f442136f955ee0477ddf0e94386481e6ec682bb4 |
| fcop_mcp-4.0.0rc1-py3-none-any.whl | 117937 | 20167b314de1a90093b74cf42c7039edceddc1458e1b37ce3e9e6f31697c773a |
| fcop_mcp-4.0.0rc1.tar.gz | 109420 | eefde60b6d156f5ef2184186f5f5a355837f0fc9e0244b3e2d8077dbed51000b |

[第一组 Actions artifact](https://github.com/joinwell52-AI/FCoP/actions/runs/34367862396/artifacts/10110629085) 的 ZIP digest 为 334c8b7293c22857e258075766228733394029833e949e01b192fb4b831ca8f9，过期时间 2026-12-08T15:04:47Z。它是候选验证附件，不是 GitHub Release 或公开 RC。ZIP digest 不等于四个制品摘要。下载目录为 C:/Users/Administrator/AppData/Local/Temp/wp4d-b472be3-candidates，4/4 文件及候选清单已重新核验。最终安装矩阵失败，不构成制品验收 Gate。

---

## 历史快照：截至 700e9e1 的原报告（全部保留）

以下包含前两次 BLOCKED 的事实，其状态仅适用于历史提交；当前状态以本报告顶部为准。

# WP4D 勘误续作：ARTIFACT-REPRODUCIBILITY — BLOCKED

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

## 首轮构建的真实失败

[失败 Job 102506905065](https://github.com/joinwell52-AI/FCoP/actions/runs/34363703047/job/102506905065) 在 Ubuntu / Python 3.12.14，UTC 2026-09-09 14:27:20–14:27:35 运行。固定工具安装步骤通过；实际安装含 build 1.4.2、hatchling 1.32.0、setuptools 82.0.1、wheel 0.45.1、twine 6.2.0、packaging 26.3。固定 SOURCE_DATE_EPOCH 为 1788940367。

执行命令：

```text
python -B scripts/wp4d_build.py "$RUNNER_TEMP/rc-build"
python -m build --no-isolation --wheel --sdist --outdir <artifacts-1> <source-1>
python -m build --no-isolation --wheel --sdist --outdir <artifacts-1> <source-1/mcp>
python -m twine check <first-set-four-files>
```

构建步骤日志 UTC 14:27:30–14:27:32：双包 wheel/sdist 首轮生成成功；首个 wheel 的 Twine 检查退出 1，脚本随 CalledProcessError 退出 1。错误为 `InvalidDistribution: Invalid distribution metadata: '2.5' is not a valid metadata version`。其余首轮文件未完成 Twine 检查；第二轮与独立复现比较根本未执行。没有生成候选 JSON hash manifest，没有上传四候选文件 artifact，不能填 4/4、不能凭文件名推测哈希。

只读诊断记录：[toolchain-diagnosis.json](../tests/rc/evidence/wp4d/toolchain-diagnosis.json)。从 PyPI 固定 wheel 读取代码并核验其发布 SHA-256：Twine 6.2.0 的 `twine/package.py:32` 覆盖 packaging 的元数据白名单，只列至 2.4；已安装 packaging 26.3 本身支持 2.5/2.6。Twine 7.0.0 同文件不再有该覆盖，是可供 ADMIN 后续裁定的待验证工具版本，**本轮未切换、未执行其制品检查，不声称修复通过**。不得修改生产包元数据来迎合旧验证器，也不得忽略错误。

GitHub 保留的 build-logs artifact ID 为 10108917968，digest 为 `sha256:0d08b29a3302243ca93bbb75abedd58c55adfa5a78eba1b59fe559dcaf35ab65`，只含失败日志，不是 RC 制品。完整命令输出已转存 [rc-build-job.log](../tests/rc/evidence/wp4d/rc-build-job.log) 和 [rc-build-metadata-failure.log](../tests/rc/evidence/wp4d/rc-build-metadata-failure.log)。

---

## 历史快照：原 BLOCKED 报告原文保留

以下原文固定在 893e5c55f9f7ea433c6c518c76534218a4cf9570；其中“未运行”和旧 skip 仅描述该历史提交，不是上述续作后的当前结论。

# WP4D 制品可复现性：NOT_RUN

阶段在源码回归守卫处阻断；没有生成、上传或混用候选制品。

| 必需制品 | 构建/两次比对/twine | SHA-256 |
|---|---|---|
| fcop-4.0.0rc1-py3-none-any.whl | NOT_RUN | NOT_GENERATED |
| fcop-4.0.0rc1.tar.gz | NOT_RUN | NOT_GENERATED |
| fcop_mcp-4.0.0rc1-py3-none-any.whl | NOT_RUN | NOT_GENERATED |
| fcop_mcp-4.0.0rc1.tar.gz | NOT_RUN | NOT_GENERATED |

预定命令类别为 Ubuntu/Python 3.12 下两次全新目录 `python -m build` 与两组 `python -m twine check`；均未执行，开始/结束、退出码、测试数和 Actions artifact URL 均 N/A（不是通过）。SOURCE_DATE_EPOCH 未进入实际构建记录。0/4 已验证，不得记成 4/4。

内存中曾拟定构建/consumer 脚本草案，但没有落入交付内容，也未作为已实现、已运行或可用制品报告。后续续作必须在明确解除阻断后按任务书重新建立完整证据。

## 执行身份与证据口径

- 唯一任务书：`cbdc60a92a02b9e2eb0c1c6e2e93f74c335407f9`，SHA-256 `bfc93f595800efe5185588ff92b612c9ca66e1622118e76c805d5fd908a1e290`，18471 bytes。
- 已验收实现基线：`167c5fd4ca4c9603c392bae3a4a055963e7b7ed6`；未发布候选内容提交：`4160fc5d216f784bee6b35902b507fff8e0ba6f6`。
- 环境：Windows 10 build 19045 / Python 3.12.9；时区 +08:00；独立工作树 `D:/FCoP-wp4d-rc-candidate`。
- Draft PR：[31](https://github.com/joinwell52-AI/FCoP/pull/31)，base 为 `task/fcop-4.0-wp4d-rc-candidate`，不指向 main。
- 本报告为 BLOCKED 证据，不是 RC 验收或发布证明。具体命令、起止时间、退出码、测试数、日志和哈希见 [RESULT](FCOP-4.0-WP4D-RESULT.md)。
- 尚未构建四个 RC 制品，故 artifact SHA-256 均为 NOT_GENERATED；安装态、12 组合和最终 HEAD CI 未验收，不能沿用父 Gate 的通过数。
