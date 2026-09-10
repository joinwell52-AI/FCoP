---
title: "FCoP 4.0 WP4C.2：规则分发符合性优先与红灯基线任务书"
document_id: "FCOP-4.0-WP4C.2-TASKBOOK"
version: "1.0"
date: "2026-09-07"
status: "AUTHORIZED_FOR_WP4C_2_ONLY"
document_role: "EXECUTION_TASKBOOK"
authority: "ADMIN"
execution_authorized: true
authorized_scope: "WP4C_2_ONLY"
implementation_authorized: false
conformance_implementation_authorized: true
main_merge_authorized: false
release_authorized: false
parent_gate: "WP4C_1_RULE_DISTRIBUTION_CONTRACT_FROZEN"
parent_gate_commit: "b5afdb8a2fb2e70620f15128bdeb772e071e7b43"
accepted_contract_head: "f6831de12991010f22672fb6e776ce85ef1507ff"
accepted_contract_content: "6122dca08e3eb093fc015a1b6e884bf2de0bd388"
frozen_fcop_contract_commit: "aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6"
requested_gate: "WP4C_2_DISTRIBUTION_CONFORMANCE_ACCEPTED"
---

# FCoP 4.0 WP4C.2：规则分发符合性优先与红灯基线任务书

## 0. 唯一执行授权

本文是当前唯一允许执行的 WP4C.2 任务书。

本轮只允许把已经冻结的规则分发合同变成先失败的、可执行的行为符合性测试，并形成真实红灯基线。

本轮不允许：

- 实现 v4 canonical rule modules；
- 实现 Distribution Manifest loader；
- 实现 Host projection、部署、receipt 或 rollback；
- 修改 FCoP 4.0 冻结规范或 WP4C.1 双语合同；
- 修改 Core、Toolkit、MCP、Schema、现有 Host 文件；
- 读取或修改 CodeFlowMu；
- 修改 main、Tag、Release 或 PyPI。

完成后必须停止并请求：

```text
WP4C_2_DISTRIBUTION_CONFORMANCE_ACCEPTED
```

没有该 Gate，不得进入 WP4C.3。

## 1. 固定输入与权威顺序

执行者必须从本任务书固定 GitHub commit 创建独立 worktree。

固定父链必须包含：

```yaml
WP4C_1_GATE_COMMIT: b5afdb8a2fb2e70620f15128bdeb772e071e7b43
ACCEPTED_CONTRACT_HEAD: f6831de12991010f22672fb6e776ce85ef1507ff
ACCEPTED_CONTRACT_CONTENT: 6122dca08e3eb093fc015a1b6e884bf2de0bd388
WP4C_1A_TASKBOOK: 7f973dc5f32bc6b9e1076184d1247c55a1349bd5
FROZEN_FCOP_4_SPEC: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
```

必须完整读取：

```text
reviews/fcop-4.0/gates/WP4C-1-RULE-DISTRIBUTION-CONTRACT-FROZEN.md
docs/fcop-4.0/rule-distribution-contract.md
docs/fcop-4.0/rule-distribution-contract.zh.md
reports/FCOP-4.0-WP4C.1-CONTRACT-DECISIONS.md
reports/FCOP-4.0-WP4C.1-CONFORMANCE-MATRIX.md
reports/FCOP-4.0-WP4C.1-RESULT.md
reviews/fcop-4.0/wp4c.1/MANIFEST.md
spec/fcop-4.0-spec.md
spec/fcop-4.0-spec.zh.md
tests/conformance/v4/conftest.py
tests/conformance/v4/driver.py
```

事实优先级：

```text
冻结 FCoP 4.0 Specification
> 已签署 WP4C.1 分发合同
> WP4C.1 Conformance Matrix
> 本任务书
> 旧 3.x 规则与实现
```

执行授权优先级：

```text
ADMIN Gate
> 本固定任务书
> 其他候选文档
```

父链、任务书摘要、Gate、合同文件或冻结规范字节不匹配时，以 `INPUT_REF_MISMATCH` 停止。

## 2. 本阶段真正要证明什么

WP4C.2 不证明功能已经实现。它只证明：

1. WP4C.1 中 DIST-01 至 DIST-30 每一项都有可执行测试；
2. 测试直接观察未来生产边界的输入、输出、文件效果和失败状态；
3. 当前缺失实现会产生真实红灯，而不是被 skip、xfail、mock 或空壳变绿；
4. 现有 FCoP 3.x、FCoP 4.0 Core 与 MCP 回归不被测试代码破坏；
5. 后续 WP4C.3–WP4C.6 可以按 Test ID 分阶段把红灯变绿。

“测试文件存在”不等于符合性完成；“异常被捕获”不等于通过；“未来会实现”不等于当前绿灯。

## 3. Test ID 与分组冻结

WP4C.1 Matrix 中以下 30 个 ID 全部进入本阶段：

| 文件 | 固定 Test ID |
|---|---|
| test_dist_01_06_manifest.py | DIST-01 … DIST-06 |
| test_dist_07_12_profiles.py | DIST-07 … DIST-12 |
| test_dist_13_20_projection.py | DIST-13 … DIST-20 |
| test_dist_21_24_assembly_compat_mcp.py | DIST-21 … DIST-24 |
| test_dist_25_30_failures_artifacts_context_gates.py | DIST-25 … DIST-30 |

要求：

- ID 集合必须精确为 DIST-01 至 DIST-30；
- 不得重命名、遗漏、重复或挪用现有 C0–C8 的 60 个冻结 Test ID；
- 每个 ID 至少对应一个真实 behavioral node；
- 参数化可以增加节点，但不得把多个不同 ID 合并成一个空泛断言；
- 每个测试 docstring 必须记录 Test ID、RD 条款和未来唯一负责阶段；
- Arrange、Act、Assert 必须与 Matrix 对应行的 subject、action、observable result 一致；
- Matrix 是最小要求，测试不得弱化其负例、竞态、零写入或恢复断言。

## 4. 测试目录与允许文件

仅允许新增：

```text
tests/conformance/rule_distribution_v4/__init__.py
tests/conformance/rule_distribution_v4/conftest.py
tests/conformance/rule_distribution_v4/driver.py
tests/conformance/rule_distribution_v4/test_dist_00_meta.py
tests/conformance/rule_distribution_v4/test_dist_01_06_manifest.py
tests/conformance/rule_distribution_v4/test_dist_07_12_profiles.py
tests/conformance/rule_distribution_v4/test_dist_13_20_projection.py
tests/conformance/rule_distribution_v4/test_dist_21_24_assembly_compat_mcp.py
tests/conformance/rule_distribution_v4/test_dist_25_30_failures_artifacts_context_gates.py
reports/FCOP-4.0-WP4C.2-CONFORMANCE-PLAN.md
reports/FCOP-4.0-WP4C.2-RED-BASELINE.md
reports/FCOP-4.0-WP4C.2-RESULT.md
reviews/fcop-4.0/wp4c.2/MANIFEST.md
```

Content commit 只能新增前十二项；Manifest commit 只能新增最后一项。

不得修改：

```text
spec/fcop-4.0-spec.md
spec/fcop-4.0-spec.zh.md
docs/fcop-4.0/rule-distribution-contract.md
docs/fcop-4.0/rule-distribution-contract.zh.md
tests/conformance/v4/**
src/**
mcp/**
spec/schemas/**
AGENTS.md
CLAUDE.md
.cursor/**
CodeFlowMu
```

若测试确实需要修改既有 fixture、workflow、配置或公共 driver，必须停止并报告，不得扩大 allowlist。

## 5. Test-only driver 边界

`RuleDistributionConformanceDriver` 只能做薄的测试适配：

- 解析一个明确的生产公开入口；
- 把完整语义请求原样传入；
- 返回未改写的生产结果；
- 读取测试工作区以验证实际文件效果；
- 在公开能力不存在时抛出结构化 `RULE_DISTRIBUTION_NOT_IMPLEMENTED` 测试错误，使测试保持红灯。

Driver 不得：

- 实现 Manifest 解析、依赖排序、摘要计算或模块选择；
- 生成 rule module、Host entry、adoption/deployment receipt；
- 模拟成功结果；
- 在测试侧替生产代码补默认值；
- 用 mock/monkeypatch 伪造生产行为；
- 捕获“未实现”并把它转换为 PASS；
- 根据函数名或参数签名本身给符合性分；
- 直接导入未来私有模块绕过公共入口；
- 复制 Core、Toolkit 或 MCP 业务算法。

测试侧的摘要只可用于独立计算 expected value，并必须与生产返回或磁盘事实比较；不得把 expected 写回生产结果。

公共生产 API 尚不存在是本阶段的预期红灯，不构成合同不确定，也不得因此修改生产代码。

## 6. Fixtures 与隔离

所有行为测试必须：

- 只使用 pytest 临时目录；
- 不访问 `D:\FCoP`、用户工作区或 CodeFlowMu；
- 不依赖网络、当前时间、随机目录顺序或本机绝对路径；
- 固定 UTF-8/LF 原始字节；
- 固定 package Manifest、模块、Host profile、adoption receipt 和目标文件的最小测试 fixture；
- 对竞争测试使用真实独立进程和同步 barrier，不以单线程顺序调用冒充；
- 对崩溃窗口使用测试专用、公开的 fault seam；不存在时保持红灯，不修改生产实现；
- 对 Host 只测试静态 profile 和生成字节，不启动 Codex、Cursor、Claude Code；
- 对 MCP 只定义未来 read-only 映射的可观察合同，不修改或调用外部 Relay 网络；
- 对 CodeFlowMu 只验证“没有访问/没有写入”的边界，不读取其仓库内容。

Fixture 可以构造输入数据，但不能预先构造被测试的成功输出或 receipt。

## 7. 六组必须覆盖的行为

### 7.1 Manifest 与 canonical artifacts（DIST-01–06）

必须覆盖：

- Manifest schema、protocol/package identity；
- 九模块、十八个语言 artifact 的完整身份；
- 原始字节 SHA-256 与 size；
- 缺失、重复、未知、包外路径和符号链接逃逸；
- `depends_on` 无环、依赖闭包与确定性 load order；
- 明确语言选择和中英文 artifact 隔离；
- 相同输入产生相同选择结果；
- Manifest 不承载 workspace adoption 或 Runtime 状态。

### 7.2 Adoption、deployment 与 Host profile（DIST-07–12）

必须覆盖：

- package Manifest、workspace adoption receipt、deployment receipt、Host profile 四类字段不混用；
- 无 adoption receipt 时 Host 文件存在不等于已采用；
- adapter_supported、admin_adopted、entry_generated、runtime_consumption_verified 四事实不能互相推导；
- 未知 Host、未知 profile、未采用 profile Fail Closed；
- profile 字节上限、语言、换行、目标路径与 managed region；
- deployment receipt 只记录实际 effect，不获得生命周期 authority；
- rollback 只能指向上一条仍可验证的 adopted/deployed receipt。

### 7.3 Projection、所有权、竞态和恢复（DIST-13–20）

必须覆盖：

- `reference` 与 `bounded_embed` 的确定性字节；
- 不含时间戳、随机值、机器绝对路径；
- 超限直接拒绝，不截断、不换模式、不删规则；
- dry-run 零写入，包括不创建目录、备份或 receipt；
- 只写新文件或受管理区域；
- 下游非管理内容冲突停止；
- plan 后 target 漂移必须在写入前重验；
- 两个独立进程竞争同一 target，不得丢失用户修改或产生相互矛盾的成功 receipt；
- 阶段写入、替换中途和成功 receipt 之前的故障窗口；
- 不宣称多文件全局原子性；
- 部分结果必须显式，恢复必须由显式命令触发。

### 7.4 装配、Legacy 与 MCP（DIST-21–24）

必须覆盖：

- sequential 精确包含八个共同模块，其中有 `relations`、没有 `convergence`；
- parallel 等于 sequential 加且只加 `convergence`；
- 仅知道 `branch_of` 词汇不能启用 Branch；
- repository-development 是独立固定引用束，不是第十个业务模块；
- 普通业务指导不含开发治理或 CodeFlowMu RC；
- 无版本旧调用保持 3.x，显式 v4 不覆盖、不膨胀、不自动迁移 3.x；
- MCP resource read 零写入、零采用、零 evaluator 安装；
- Relay 只委托同一 read-only 能力，不成为第二规则权威。

### 7.5 类型化失败、缓存失效与制品（DIST-25–27）

必须覆盖八个 `toolkit:RULE_*` 错误分类与安全字段，且不重定义 31 个 Base error。

必须把以下事实分开验证：

- 磁盘 package；
- 进程内 Manifest/index；
- 已生成 Host entry；
- Runtime consumption evidence。

一个层级更新不得被测试解释为其余层已刷新。

制品测试必须离线、跨平台可收集，并为未来 wheel/sdist 的 Manifest/module 字节一致性设定真实断言；当前制品尚未包含 v4 modules 时应红，不得只检查文件名。

### 7.6 上下文、下游 shadow 与 Gate（DIST-28–30）

必须覆盖：

- 每个 assembly/Host projection 的原始 UTF-8 byte count；
- 单语言与显式多语言分开；
- estimator 必须公开算法，不能以 token 猜测替代 byte limit；
- 不因超限自动删减规范义务；
- CodeFlowMu shadow 为独立授权的只读未来动作；当前测试只能断言没有隐式读取、写入或版本提升；
- 缺少下一阶段 Gate 时，执行入口必须停止；
- 合同冻结、Conformance 接受、实现接受、main merge、release 五种状态不得互相推导。

## 8. Meta guard

`test_dist_00_meta.py` 必须独立通过并至少断言：

1. 30/30 Test ID 精确覆盖；
2. 无 skip、xfail 或条件性静默跳过；
3. 无 `pass`、空测试、无条件成功、只检查方法存在的测试；
4. Driver 不包含 Manifest/投影/receipt 的生产算法；
5. 测试只写 pytest 临时目录；
6. 冻结 C0–C8 的 60 个 ID 和文件 SHA 未变；
7. WP4C.1 双语合同、Gate 和 Manifest 字节未变；
8. 每个 DIST ID 有 RD 引用和唯一后续负责阶段；
9. 每个 effectful test 都检查成功效果或失败后的零写入/显式部分状态；
10. 未把 `RULE_DISTRIBUTION_NOT_IMPLEMENTED` 当作符合性成功。

Meta guard 通过不等于 30 个行为节点通过。

## 9. 预期红灯与结果分类

本阶段目标是可信红灯，不是人为追求“全红”。

结果必须分为：

```text
PREEXISTING_PASS
EXPECTED_FAIL_NOT_IMPLEMENTED
EXPECTED_FAIL_CONTRACT_MISMATCH
UNEXPECTED_PASS
UNEXPECTED_FAILURE
```

规则：

- 已有真实生产行为满足合同，可以记 `PREEXISTING_PASS`，但必须给出公开入口和文件效果证据；
- 缺公开能力属于 `EXPECTED_FAIL_NOT_IMPLEMENTED`；
- 已有行为与冻结合同不一致属于 `EXPECTED_FAIL_CONTRACT_MISMATCH`；
- mock、fixture 代做、旧 3.x 泄漏或仅检查文档造成的绿灯属于 `UNEXPECTED_PASS`，必须停止修正测试；
- 测试基础设施、收集、编码、平台或不相关回归失败属于 `UNEXPECTED_FAILURE`，必须停止。

不得添加：

```text
pytest.mark.skip
pytest.mark.xfail
pytest.skip
unittest.skip
try/except 后返回成功
环境变量关闭断言
空壳 NotImplemented 通过分支
```

目标完成条件不是“pytest 退出 0”，而是：

- Meta/static 全绿；
- 30/30 行为 ID 全部真实执行；
- 所有红灯均落入两个预期分类；
- `UNEXPECTED_PASS=0`；
- `UNEXPECTED_FAILURE=0`；
- 既有回归零新增失败。

## 10. 验证命令与证据

使用项目既有 Python 工具链，不增加运行依赖。

必须分别运行并记录完整命令、环境、退出码、收集数和结果：

1. 新规则分发 Meta 测试；
2. 新规则分发 30 个行为 ID；
3. `--collect-only`；
4. 现有 `tests/test_fcop`；
5. 现有 `tests/conformance/v4`；
6. 隔离的 MCP 回归；
7. Ruff 对本轮新增 Python 文件；
8. `git diff --check`；
9. UTF-8/LF/无 BOM；
10. allowlist、父链和冻结文件字节检查。

新行为测试允许预期非零退出码；报告必须列出每个失败 node 的 Test ID、结构化原因、负责阶段和是否产生磁盘效果。

不得把既有测试计数写死为任务书中的历史数字；记录本次实际结果，并证明零新增回归。

## 11. 报告要求

### 11.1 CONFORMANCE PLAN

必须包含：

- 30 个 ID 的 RD/Matrix 追踪；
- 每个 ID 的 Arrange/Act/Assert；
- test-only driver action；
- 真实 effect boundary；
- 预期当前分类；
- 后续唯一负责阶段 WP4C.3–WP4C.6。

### 11.2 RED BASELINE

必须逐 node 记录：

```yaml
test_id
node_id
contract_ref
command
exit_status
classification
structured_error
public_entry
effects_observed
zero_write_verified
future_owner
```

不得只给总数。

### 11.3 RESULT

必须清楚区分：

- Test 合同完成；
- 当前实现未完成；
- 既有回归状态；
- 未执行的 Host Runtime、CodeFlowMu shadow、跨平台原生行为；
- 本轮没有获得 WP4C.3 实现授权。

## 12. 强制停止条件

出现任一情况必须停止并交付事实报告，不请求 Gate：

- 需要修改 WP4C.1 已冻结合同；
- 某 DIST 行无法从合同和 Matrix 得出明确 observable；
- 需要修改生产代码、Schema、MCP、现有 Core conformance 或测试配置；
- 需要 mock、skip、xfail 或测试侧实现行为；
- Test ID 无法保持 30/30；
- 出现 `UNEXPECTED_PASS` 或 `UNEXPECTED_FAILURE`；
- 既有回归出现新增失败；
- 测试触碰真实工作区、Host 或 CodeFlowMu；
- 需要网络或新运行依赖；
- Content/Manifest 两提交范围无法保持；
- 任何 P0 未关闭。

公开生产入口不存在不是停止条件，而是预期红灯。

## 13. GitHub-only 交付

使用新 review 分支：

```text
review/fcop-4.0-wp4c.2-distribution-conformance
```

创建 Draft PR，base 为本任务书固定分支。不得修改、合并或关闭 PR #18、PR #19。

严格两提交：

1. Content commit：九个测试文件和三份报告，共十二项；
2. Manifest commit：只新增 `reviews/fcop-4.0/wp4c.2/MANIFEST.md`。

push 后必须 refetch，并在固定远端 Manifest HEAD 核验：

- Manifest → Content → 本任务书固定 commit 的直接父链；
- 13/13 交付文件 SHA-256；
- PR changed paths 精确 13 项；
- 远端 HEAD 等于 Manifest commit；
- 工作树干净；
- main、冻结合同、生产源码、MCP、Schema、Host 和 CodeFlowMu 未修改。

GitHub CI 因新行为红灯而失败不等于 `UNEXPECTED_FAILURE`；但必须证明失败只来自已登记的预期 DIST nodes，其他 job 不得出现基础设施或回归失败。

## 14. 完成回执

```yaml
WP4C_2_STATUS: COMPLETE | BLOCKED
AUTHORIZED_SCOPE: WP4C_2_ONLY
TASKBOOK_COMMIT: ""
TASKBOOK_SHA256: ""
INPUT_HEAD: ""
PARENT_GATE_COMMIT: b5afdb8a2fb2e70620f15128bdeb772e071e7b43
ACCEPTED_CONTRACT_HEAD: f6831de12991010f22672fb6e776ce85ef1507ff
FROZEN_FCOP_CONTRACT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6

DISTRIBUTION_TEST_IDS: 30/30
BEHAVIORAL_NODES: n
META_TESTS: n/n
PREEXISTING_PASS: n
EXPECTED_FAIL_NOT_IMPLEMENTED: n
EXPECTED_FAIL_CONTRACT_MISMATCH: n
UNEXPECTED_PASS: 0
UNEXPECTED_FAILURE: 0
SKIP_XFAIL: 0
EMPTY_STUB_GUARD: PASS

FROZEN_CORE_TEST_IDS: 60/60_UNCHANGED
TEST_FCOP_REGRESSION: PASS
V4_CORE_CONFORMANCE: PASS
MCP_REGRESSION: PASS
NEW_RUNTIME_DEPENDENCIES: 0
PRODUCTION_FILES_MODIFIED: 0
SCHEMA_FILES_MODIFIED: 0
MCP_FILES_MODIFIED: 0
FROZEN_CONTRACT_FILES_MODIFIED: 0
EXISTING_CORE_CONFORMANCE_MODIFIED: 0
HOST_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0

CONTENT_FILES: 12/12
TOTAL_DELIVERY_FILES: 13/13
CONTENT_COMMIT: ""
MANIFEST_COMMIT: ""
REMOTE_HEAD: ""
REMOTE_PUSHED: true
REMOTE_REFETCH_VERIFIED: PASS
DIRECT_PARENT_CHAIN: PASS
DELIVERY_SHA256: 13/13
WORKTREE_STATUS: CLEAN

WP4C_2_DISTRIBUTION_CONFORMANCE_ACCEPTED: false
WP4C_3_STARTED: false
MAIN_MODIFIED: false
RELEASE_CREATED: false
REQUESTED_GATE: WP4C_2_DISTRIBUTION_CONFORMANCE_ACCEPTED
```

完成后强制停止。执行者不得自行签署 Gate，不得进入 WP4C.3。
