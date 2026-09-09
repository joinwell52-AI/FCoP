# FCoP 4.0 WP4D：收口验证修复授权包 v1.0

```yaml
document_role: EXECUTION_AUTHORIZATION_AMENDMENT
execution_authorized: true
authorized_scope: WP4D_VERIFICATION_REPAIR_ENVELOPE_AND_CLOSEOUT
parent_taskbook_commit: cbdc60a92a02b9e2eb0c1c6e2e93f74c335407f9
latest_point_erratum_commit: 6c2793d2f91fe5c0c8d4edce4e8e0064f889c686
resume_implementation_head: 737d3d3482f371616863a018f04ab1a756259723
draft_pr: https://github.com/joinwell52-AI/FCoP/pull/31
completion_gate: FCOP_4_RC_ACCEPTED
main_merge_authorized: false
rc_publish_authorized: false
stable_release_authorized: false
pypi_publish_authorized: false
github_release_authorized: false
mcp_registry_publish_authorized: false
zenodo_publish_authorized: false
codeflowmu_write_authorized: false
```

## 1. ADMIN 决定

WP4D 后续改为“验证修复授权包”执行，不再为每个测试环境、样例或构建验证脚本的兼容性问题逐点停机申请授权。

执行人可在本任务书明确的验证范围内自行诊断、修正、提交、重跑并继续；只有触及协议、生产实现、Conformance、候选身份、发布权限或无法维持验收语义时才必须停止。

本授权包继承并保留此前三份定点勘误；当前 Windows socketpair 修正首先按 `6c2793d2f91fe5c0c8d4edce4e8e0064f889c686` 执行，之后遇到同类验证层问题直接按本授权包处理。

## 2. 允许自行修复的路径

仅允许在以下路径内进行 WP4D 验证兼容修复：

```text
tests/rc/**
tests/test_fcop/test_wp4d_rc*.py
tests/test_fcop_mcp/test_wp4d_rc*.py
examples/v4/third-party/**
scripts/wp4d_*.py
scripts/fcop_rc_candidate_check.py
.github/workflows/rc-candidate.yml
reports/FCOP-4.0-WP4D-*.md
reviews/fcop-4.0/wp4d/MANIFEST.md
```

另允许修改既有测试文件中与候选版本、平台路径、编码或测试准入直接相关的前置条件，但必须同时满足：

- Test ID、夹具目的和业务断言保持不变；
- 不删除、弱化、反转或绕过断言；
- 不新增 skip、xfail、allowed failure；
- 不以 mock/monkeypatch 伪造生产结果；
- 每次修改在报告中逐项列出路径、原因和语义不变证明。

## 3. 允许修复的问题类型

执行人无需再次申请 ADMIN，可自行处理：

- Python 3.10–3.13 或 Windows/Linux/macOS 的测试工具兼容；
- 路径分隔符、换行、编码、临时目录和子进程差异；
- 第三方样例自身的启动、stdio、进程清理和离线守卫兼容；
- RC workflow 的 job 依赖、artifact 下载、哈希传递、shell 可移植性；
- WP4D 构建/消费/证据脚本的确定性缺陷；
- 已固定验证工具之间的兼容问题；如必须更换版本，必须使用精确版本、引用官方依据并记录完整工具身份；
- JUnit、日志、JSON evidence 与 Manifest 的生成和读取错误；
- 不改变验收语义的测试收集或前置条件错误。

每项修复必须保持或增强原验证强度，并用失败前后对照证明问题位于验证层。

## 4. 绝对冻结范围

以下任何内容仍不得自行修改：

```text
spec/**
specs/**
tests/conformance/**
src/fcop/**
mcp/src/fcop_mcp/**
mcp/pyproject.toml
pyproject.toml
mcp/server.json
CITATION.cff
.github/workflows/release.yml
```

同时冻结：

- FCoP 4.0 协议与八项 Core 合同；
- 公开 Python/MCP 行为和错误语义；
- `46 tools / 12 static resources / 4 templates`；
- 候选版本 `fcop==4.0.0rc1`、`fcop-mcp==4.0.0rc1`；
- MCP 依赖 `fcop>=4.0.0rc1,<4.1.0`；
- 19 个权威候选文件与 21 个冻结字节；
- legacy v3 bundled rules 和 3.2.5 兼容边界；
- CodeFlowMu 的全部文件与状态；
- main、tag 与全部发布面。

此前已经由 WP4D 内容提交完成的版本、classifier、依赖 pin 与兼容对不得借本授权包再次改变。

## 5. 不得以“加快”为由降低标准

禁止：

- 把失败、skip、cancelled、queued、in progress 或 NOT_RUN 写成 PASS；
- 只补失败矩阵而不重跑最终全矩阵；
- 按 OS/Python 放宽预期结果；
- 复用与最终提交 SHA 不一致的候选 manifest 或制品；
- 用源码 import 冒充 wheel/sdist clean-room；
- 关闭离线守卫、允许通用 loopback/外网或改用网络 MCP transport；
- 删除恢复、重试、零副作用、兼容、规则分发或 CodeFlowMu shadow 验证；
- 修改生产代码来迎合测试；
- 创建 tag、上传或发布任何候选。

加快的是授权与报告流程，不是降低验收强度。

## 6. 连续执行与提交规则

### 6.1 不中断原则

验证层问题落在第 2–3 节时：

1. 保存失败日志和根因；
2. 在 allowlist 内做最小修复；
3. 建立独立、可审查的修复提交；
4. 运行定点测试；
5. 定点通过后直接继续后续 WP4D；
6. 最终统一执行全量与远端收口。

无需为每个同类问题再次生成独立任务书、六份完整报告或中间 Manifest。

### 6.2 中间证据

中间失败只需保存：

- 原始日志/JUnit/JSON；
- 根因与修复摘要；
- 修复提交及变更路径；
- 定点复验结果。

六份完整报告与 Manifest 在最终 COMPLETE 时统一更新。只有出现第 8 节真实阻断且必须请求新权限时，才提交简洁的 BLOCKED 增量回执；不要求为相同验证层问题反复重写全部历史报告。

### 6.3 提交边界

- 每个逻辑修复独立提交，不混入报告或 Manifest。
- 允许连续多个验证修复提交。
- 最终证据提交只含报告与 evidence。
- 最终 Manifest-only 提交只含 Manifest。
- 不得 force-push、改写历史或删除既有 BLOCKED 记录。

## 7. 最终一次性验收

完成所有修复后，在最终候选内容 HEAD 统一执行：

- Windows 与 Ubuntu 全量回归，零失败、零错误、零意外 skip；
- 现有全部适用 CI，Windows 项全部通过；
- Twine 两组检查 `2/2`；
- 四制品原始字节可复现 `4/4`；
- RC consumer `12/12`，installed wheel/sdist origin paths `24/24`；
- Python-only 与 MCP-only 外部项目；
- response-loss retry 与 crash recovery；
- 3.2.5 workspace 零迁移、零漂移；
- Host 规则发现、拒绝、部署、回滚与零副作用；
- CodeFlowMu 固定 3.2.5 只读 shadow `14/14`；
- MCP 公开面 `46/12/4`；
- 权威候选文件 `19/19` 与冻结字节 `21/21`；
- 最终 Manifest HEAD 的全部适用 CI；
- 所有交付文件远端逐项回读与 SHA-256 核验。

制品和 manifest 必须绑定最终候选内容提交。最终修复如改变被打包内容或 manifest 绑定 SHA，必须重建四制品；不得手改 manifest。

## 8. 仅剩的停止条件

只有以下情况必须立即停止并请求 ADMIN：

- 修复需要改变第 4 节冻结文件；
- 发现真实协议、Core、MCP、规则或 Conformance 缺陷；
- 必须改变候选版本、依赖契约或公开行为；
- 无法在不削弱离线、恢复、幂等、零副作用或兼容要求的情况下通过；
- 需要 main、tag、secret、protected environment、PyPI、GitHub Release、MCP Registry、Zenodo 或 CodeFlowMu 写权限；
- 远端固定输入、分支身份或制品来源不可唯一核验。

回执：

```text
WP4D_STATUS: BLOCKED
REQUESTED_GATE: NONE
```

普通验证脚本、样例、测试环境或 CI 编排错误不再构成 ADMIN 权限阻断；必须在授权包内自行修复并继续。

## 9. 完成回执

全部通过后停止并请求：

```text
WP4D_STATUS: COMPLETE
REQUESTED_GATE: FCOP_4_RC_ACCEPTED
RC_PUBLISH_AUTHORIZED: FALSE
MAIN_MERGE_AUTHORIZED: FALSE
```

不得自行签署 Gate，不得在 Gate 后自动合并 main、创建 tag 或发布。
