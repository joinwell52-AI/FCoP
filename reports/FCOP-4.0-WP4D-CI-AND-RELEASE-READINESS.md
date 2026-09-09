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
