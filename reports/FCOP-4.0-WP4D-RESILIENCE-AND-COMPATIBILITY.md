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
