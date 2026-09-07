---
document_role: ADMIN_SCOPE_CORRECTION
decision: WP4C_0B_REVOKED
date: 2026-09-07
supersedes_taskbook_commit: 95626bb6d599caf2893a3a4db0b9b3e6fbaa48ff
revocation_commit: b16ac400c6dd66ac836141938f85aa7db0218e16
wp4c_0_baseline_gate_remains_valid: true
wp4c_1_authorized: false
main_merge_authorized: false
release_authorized: false
---

# WP4C.0b 作用域纠正决定

## ADMIN 澄清

文件：

```text
Agent原生软件工程宪法-v1.0-rc.1.md
SHA-256: 87cf212d1cb75cefd0da6da7e5f0f4c7eaedbc231c784b985c3e2e51856abc4c
```

是为 **CodeFlowMu 当前开发**形成的过渡准入候选，只服务于 CodeFlowMu 在继续固定 FCoP 3.2.5 期间的开发治理。

它不是：

- FCoP 4.0 的协议文件；
- FCoP Rule Package 的组成部分；
- FCoP 仓库开发规则的既成权威来源；
- joinwell52-AI 全部项目的已冻结通用宪法；
- 可由 WP4C 自动提升为全局 v1.0 的候选。

## 处置

```yaml
WP4C_0_BASELINE_ACCEPTED: true
WP4C_0_BASELINE_GATE_COMMIT: 65ed07263de707d327e6e2c358aec2dd7c00a6df
WP4C_0B_TASKBOOK_STATUS: REVOKED_SCOPE_MISMATCH
WP4C_0B_EXECUTION_AUTHORIZED: false
CODEFLOWMU_RC1_CLASSIFICATION: CODEFLOWMU_TRANSITION_REVIEW_INPUT_ONLY
FCOP_CONSTITUTION_SOURCE_STATUS: UNRESOLVED
WP4C_1_AUTHORIZED: false
```

已提交到 FCoP 任务书分支的 RC 文件保留为审计历史，不得作为 FCoP 的 canonical、不得打包、不得生成规则、不得由 FCoP Host 投影加载。

## 后续边界

FCoP 的两类材料必须分开：

1. 普通业务 Agent 使用的 FCoP 4.0 Rule Package，只投影冻结协议；
2. 修改 FCoP 本体的开发 Agent 使用的工程规则，由 ADMIN 另行决定采用独立通用宪法，还是 FCoP 专属开发手册。

CodeFlowMu 的过渡 RC 不参与该选择。

在 ADMIN 固定 FCoP 开发治理来源，或明确将其从 WP4C.1 前置条件中移除以前，不得开始 WP4C.1。

本决定不撤销已经完成的 WP4C.0 基线审计 Gate，不修改任何产品、协议、规则、Host、main 或发布状态。
