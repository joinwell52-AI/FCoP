# WP4C.5 开工前核验与阻断证据

## 状态与唯一授权

```yaml
STATUS: INPUT_INTEGRITY_BLOCKED
AUTHORIZED_SCOPE: WP4C_5_ONLY
TASKBOOK_COMMIT: 3e48a344b3bf16c2ed45671a7fb458b14f50dd6e
TASKBOOK_SHA256: 6ebf0db70dcfe3d55ecbc0cfbe4b33d4d739057dac93a5f66801440fb2c144b4
TASKBOOK_BYTES: 22456
INPUT_HEAD: d29e4d41ad4e1fc74e6d3513faa6b95d97ba0dfb
WP4C_4_GATE_COMMIT: a9c810296aadf857438a1711b6a56fa63deaf4e9
DECLARED_FROZEN_CONFORMANCE: 1f4df9cc650f63b9e842d806340eb31b768f708e
CONFORMANCE_BASELINE_MISMATCH_FILES: 4
PRODUCTION_IMPLEMENTATION_STARTED: false
REQUESTED_GATE: NONE
WP4C_6_STARTED: false
```

执行角色为已交班的 ME / solo。ADMIN 固定任务书承载决策，本文件承载开工核验，不另行初始化或改动 dogfood 工作区。此文件是被输入阻断的 preflight，不是完成了任务书第 4 节全部 Implementability Proof 的声明。

[唯一任务书](https://github.com/joinwell52-AI/FCoP/blob/3e48a344b3bf16c2ed45671a7fb458b14f50dd6e/taskbooks/fcop-4.0/WP4C.5/01-Versioned-Read-Resources-Legacy-Compatibility-and-Downstream-Shadow-Taskbook-v1.0.zh.md)第 0 节明确要求核对冻结 Conformance 原始字节，任一不一致立即以 INPUT_INTEGRITY_BLOCKED 停止，不得自行修正校验值、换基线或继续编码。第 15 节重申固定输入不一致时只交付阻断报告，REQUESTED_GATE=NONE。

## 已通过的固定输入核验

- GitHub Contents API 固定 ref 原始 Blob 经 Base64 解码后，22456 字节、SHA-256 与用户给定一致；严格 UTF-8、无 BOM、仅 LF。再次核对本地 git show 原始字节相同。
- GitHub Commit API 确认任务书提交只改一个任务书文件，直接父提交是 a9c810296aadf857438a1711b6a56fa63deaf4e9；该 Gate 提交只新增 Gate 文件，直接父提交为 d29e4d41ad4e1fc74e6d3513faa6b95d97ba0dfb。
- [ADMIN Gate](https://github.com/joinwell52-AI/FCoP/blob/a9c810296aadf857438a1711b6a56fa63deaf4e9/reviews/fcop-4.0/gates/WP4C-4-HOST-PROJECTION-ACCEPTED.md)与[PR #25 ADMIN 回执](https://github.com/joinwell52-AI/FCoP/pull/25#issuecomment-5579183341)一致；回执作者为 joinwell52-AI。
- 独立工作树 D:/FCoP-wp4c5-compatibility 从任务书 SHA 创建，分支 review/fcop-4.0-wp4c.5-compatibility，初始 CLEAN；使用一次性的 core.autocrlf=false，不修改全局 Git 配置。
- 两份冻结 Core 规范与 aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6 无差异；两份 RD 合同、决策与矩阵与 f6831de12991010f22672fb6e776ce85ef1507ff 无差异。
- 任务书 HEAD 相对已验收输入只新增本 Gate 和任务书；生产代码和全部测试均原样继承已验收输入。

## 冻结测试身份的四处不一致

下表路径统一以 tests/conformance/rule_distribution_v4/ 为前缀。左侧来自任务书 frontmatter 所声明的冻结提交 1f4df9cc650f63b9e842d806340eb31b768f708e；右侧同时适用于已验收输入 d29e4d41ad4e1fc74e6d3513faa6b95d97ba0dfb 与任务书提交 3e48a344b3bf16c2ed45671a7fb458b14f50dd6e。

| 文件 | 声明冻结字节数 | 声明冻结 SHA-256 | 已验收/任务书字节数 | 已验收/任务书 SHA-256 |
| --- | ---: | --- | ---: | --- |
| conftest.py | 16323 | fe52ec983d2de2682c82f7bdef651dd9f9986ae1c92c51f15492f6df634585a6 | 16826 | e9571f4d0051e04cbc0e63ef9a8e2cdc9d5facd427afafb6c4934c305d835a67 |
| test_dist_00_meta.py | 12622 | b75643004972bf2f649471fd79ff42f91b67eca9dac2636226e1505d3f89fa6b | 14382 | 816d739dd4eed73c545ee75947c893eba44f5a9f944dbc37ef978b582746c9d6 |
| test_dist_01_06_manifest.py | 9081 | 1c06804bb2e09ac969dcb7c3ad3f36248f8240637c1c40958199b593c9d1bd5b | 10075 | dafac52d52a9c8568dd9d360b58cbba6676446cf62b3a498701a19cbb0697d78 |
| test_dist_25_30_failures_artifacts_context_gates.py | 13077 | d0bba1b41ad4a36030c7ba0c229da76c8de65aff127a04a16499a317c5acad19 | 13044 | be6a3fe99b19da82f1c14b964c96d02160812b169d5ad10b4d5cd5203a64839c |

不是 CRLF 展示差异：对每一文件分别从 GitHub 三个固定提交读取完整原始 Blob（共 12 份），与本地 git show 原始字节逐一相等；已验收输入=任务书 checkout，但两者均不等于声明的冻结身份。

可复核命令：

```text
git diff --name-status 1f4df9cc650f63b9e842d806340eb31b768f708e 3e48a344b3bf16c2ed45671a7fb458b14f50dd6e -- tests/conformance/rule_distribution_v4
git log --format="%H %s" 1f4df9cc650f63b9e842d806340eb31b768f708e..3e48a344b3bf16c2ed45671a7fb458b14f50dd6e -- tests/conformance/rule_distribution_v4
gh api repos/joinwell52-AI/FCoP/contents/<path>?ref=<fixed-sha>
```

差异归因仅有两次历史提交：

1. [e1ed85e4ba5aba212ddf3cc4f880c0abecc2bfab](https://github.com/joinwell52-AI/FCoP/commit/e1ed85e4ba5aba212ddf3cc4f880c0abecc2bfab)：WP4C.3a 将 WP4C.2 审计固定到历史区间，修改 conftest.py、test_dist_00_meta.py、test_dist_25_30_failures_artifacts_context_gates.py，63 增/9 删。
2. [115751b4c24a1924062a81a21e0d655e8cb5fedc](https://github.com/joinwell52-AI/FCoP/commit/115751b4c24a1924062a81a21e0d655e8cb5fedc)：WP4C.3b 给 DIST-02 增加固定开发引用，修改 test_dist_01_06_manifest.py，16 增/0 删。

这些是已验收父链中的已授权历史修正，不指控其未经授权，也不否定 WP4C.4 Gate。阻断点仅在于本任务书同时固定了旧测试身份和包含修正的新输入，却要求原始字节一致并禁止执行者自行换基线。

## 已运行的目标红灯基线

该只读审计/现有测试运行在生产编辑前启动，输入身份差异被完整确认后未继续实现或追加测试。结果为 **12 failed / 1 passed / 3 warnings，32.88 秒，exit 1**，无 skip/xfail。此为实际运行，不是把任务书预计数抄成事实。

```text
python -X utf8 -m pytest
 tests/conformance/rule_distribution_v4/test_dist_21_24_assembly_compat_mcp.py::test_dist_23
 tests/conformance/rule_distribution_v4/test_dist_21_24_assembly_compat_mcp.py::test_dist_24
 tests/conformance/rule_distribution_v4/test_dist_25_30_failures_artifacts_context_gates.py::test_dist_26
 tests/conformance/rule_distribution_v4/test_dist_25_30_failures_artifacts_context_gates.py::test_dist_29
 -q --tb=line -p no:cacheprovider
 --basetemp=D:/fcop-wp4c5-target-baseline
 --junitxml=C:/Users/Administrator/AppData/Local/Temp/fcop-wp4c5-target-baseline.xml
```

环境：Windows/Python 3.12.9；PYTHONDONTWRITEBYTECODE=1；PYTHONPATH 只指本独立工作树的 src、mcp/src、根目录。测试根是新建临时沙箱，没有删除或复用旧沙箱。JUnit 原始 SHA-256：28920cda4f6d0c1eb59271a0d18f964eb1462165ccbe272a3eed6a20019cabc1。

| 实际节点 | 结果 | 唯一 owner |
| --- | --- | --- |
| test_dist_23[unversioned-v3] | FAIL | WP4C.5 |
| test_dist_23[explicit-v4-on-v3] | FAIL | WP4C.5 |
| test_dist_23[v4-no-adoption] | PASS | WP4C.5 |
| test_dist_24[3.0-fcop://rules] | FAIL | WP4C.5 |
| test_dist_24[3.0-fcop://protocol] | FAIL | WP4C.5 |
| test_dist_24[3.0-fcop://guidance/sequential/en] | FAIL | WP4C.5 |
| test_dist_24[3.0-fcop://team] | FAIL | WP4C.5 |
| test_dist_24[4.0-fcop://rules] | FAIL | WP4C.5 |
| test_dist_24[4.0-fcop://protocol] | FAIL | WP4C.5 |
| test_dist_24[4.0-fcop://guidance/sequential/en] | FAIL | WP4C.5 |
| test_dist_24[4.0-fcop://team] | FAIL | WP4C.5 |
| test_dist_26 | FAIL | WP4C.5 |
| test_dist_29 | FAIL | WP4C.5 |

没有把当前红灯当成已完成实现；此前 WP4C.4 全量通过结果也不冒充本轮回归。完整 FCoP/Core/MCP 回归、13/13 实现验收、五层查询、资源注册增量与授权 Shadow 均未执行。

## 已观察到但未执行的后续设计入口

现有 Project.deploy_protocol_rules(force=False) 会保留存在的入口；force=True 默认可能覆盖，因此不能未经明确边界设计直接接线。当前 read_resource 尚不可用，MCP 资源仍使用 WP4B 的只读适配和 legacy 原来源。尚未完成所有安全证明，不能据此声称可实施。

CodeFlowMu 仅查询 Git 身份和文件路径/状态元数据：本地和远端 main 当时均为 b961b16dd0c8863ead6995d963fe0ca576a8abaa；已知隔离证据提交解析为 789cb3fa8a007f050248784f7daf689808a549a2。本地有既有未提交材料，未清理、切分支、fetch 到它的对象库、安装包、执行产品脚本或读取用户凭据。**未完成真实 Shadow，不声明精确 pin、安全路由或零写入 Shadow 测试已通过。**

## 请求 ADMIN 的最小裁定

请用新的固定任务书，或明确固定到 GitHub 的基线勘误，确认 frozen_distribution_conformance 指向已验收的修正后测试身份（例如明确采用 INPUT_HEAD 的 Conformance 树），或提供由旧冻结提交及两次已授权修正组成的精确 baseline 定义。不要回退四个测试文件来迎合旧字段，也不需要扩大 WP4C.5 功能范围。

在此之前仅保留并交付本阻断证据，不修改任务书、冻结测试、代码、资源 snapshot 或合同，不请求 WP4C_5_COMPATIBILITY_ACCEPTED。
