# FCoP 4.0 Gate — WP4C.4 Host Projection Accepted

```yaml
gate: WP4C_4_HOST_PROJECTION_ACCEPTED
status: ACCEPTED
authority: ADMIN
accepted_head: d29e4d41ad4e1fc74e6d3513faa6b95d97ba0dfb
content_commit: 90fd061e82d82ec5639a70c7964fdd5d24191886
manifest_commit: d29e4d41ad4e1fc74e6d3513faa6b95d97ba0dfb
accepted_delivery_paths: 17/17
wp4c_4_target_ids: 13/13
wp4c_4_target_nodes: 53/53
test_fcop: 1349/1349
v4_core_conformance: 119/119
mcp_regression: 134/134
rule_distribution_full: 144_passed_32_expected_future_failures
unexpected_failures: 0
delivery_sha256: 17/17
ci_status: NOT_TRIGGERED_BRANCH_FILTER
runtime_consumption_verified: UNKNOWN
wp4c_5_authorized_by_gate_alone: false
main_merge_authorized: false
release_authorized: false
```

## ADMIN decision

ADMIN 接受固定提交 `d29e4d41ad4e1fc74e6d3513faa6b95d97ba0dfb` 所承载的 WP4C.4 Host 薄投影、显式采用、部署、收据、验证、部分失败恢复与回滚实现。

验收依据是：任务书父链闭合；Content/Manifest 两提交职责分离；17 个交付路径与远端原始字节核验一致；DIST-08—DIST-20 的 13 个 Test ID、53 个节点全部通过；FCoP、v4 Core 与 MCP 回归无新增失败；冻结规范、冻结分发合同、冻结 Conformance、MCP、CodeFlowMu 与 `main` 均未被修改。

实现保持一个公共入口 `Project.rule_distribution`，新增模块均为职责受限的私有文件工具。它没有增加数据库、Daemon、Watcher、Scheduler、网络更新器、后台重试、第二权威 Store 或 Host 能力探测，也没有把 Host Profile 当作生命周期授权 Profile。

GitHub Actions 因 review 分支过滤没有运行，事实状态固定为 `NOT_TRIGGERED_BRANCH_FILTER`，不能解释为 CI PASS。Windows 原生结果已报告；Linux/macOS 原生验证仍属于 WP4C.6。Host 实际消费仍为 `UNKNOWN`，文件存在、部署成功和回执存在均不证明 Host 已加载内容。

本 Gate 只验收 WP4C.4，不自行授权 WP4C.5。WP4C.5 必须使用另行固定、直接接在本 Gate 后的任务书；也不授权修改 `main`、发布 FCoP 4.0、迁移工作区、升级 CodeFlowMu 的固定 FCoP 版本或将 FCoP 变为 Host Runtime。
