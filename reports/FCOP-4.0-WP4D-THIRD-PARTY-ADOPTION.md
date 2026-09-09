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
