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
