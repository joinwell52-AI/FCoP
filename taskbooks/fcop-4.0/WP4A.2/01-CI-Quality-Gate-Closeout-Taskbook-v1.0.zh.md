---
title: "FCoP 4.0 WP4A.2：CI 质量门禁正确性与 Machine Contract 收口任务书"
document_role: EXECUTION_TASKBOOK
status: AUTHORIZED_FOR_WP4A_2_ONLY
execution_authorized: true
authorized_scope: WP4A_2_ONLY
input_head: 6ff8f213313c1f802e3498d2196b8c3bd363ceb5
frozen_contract_commit: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
draft_pr: 14
main_merge_authorized: false
release_authorized: false
wp4b_authorized: false
---

# FCoP 4.0 WP4A.2：CI 质量门禁正确性与 Machine Contract 收口任务书

## 0. ADMIN 裁决

WP4A.1 的 Machine Contract、Schema、示例、离线制品与本地测试结果不因本任务被否定。当前阻断仅来自两类 CI 问题：

1. 冻结 Conformance 文件中 10 条静态 Ruff 诊断；
2. Stability Charter 的 `awk` 区间同时以 `## [Unreleased]` 作为开始和结束匹配，实际只截取标题首行，因而错误地看不到已经存在的 `### Added — fcop`。

因此：

```yaml
WP4A_1_DELIVERY: PRESERVED
WP4A_MACHINE_CONTRACT_ACCEPTED: false
WP4A_2_AUTHORIZED: true
AUTHORIZED_SCOPE: WP4A_2_ONLY
MAIN_MERGE_AUTHORIZED: false
RELEASE_AUTHORIZED: false
WP4B_AUTHORIZED: false
```

本任务只允许纠正 CI 门禁及其直接触发的静态问题，不允许修改 FCoP 4.0 行为、冻结合同、Schema 或产品边界。

## 1. 固定输入与执行入口

执行前必须核验：

```text
Repository: joinwell52-AI/FCoP
Draft PR: https://github.com/joinwell52-AI/FCoP/pull/14
Review branch: review/fcop-4.0-wp4a.1-machine-contract
INPUT_HEAD: 6ff8f213313c1f802e3498d2196b8c3bd363ceb5
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
Failed workflow run: https://github.com/joinwell52-AI/FCoP/actions/runs/34014373307
```

本任务书提交必须是 `INPUT_HEAD` 的直接后继或位于其无分叉后继链上。Codex 必须从本任务书所在提交建立独立 worktree；不得在原 `D:\FCoP` 脏工作区工作。

若远端 review 分支不再包含上述输入提交，或 PR #14 的 head 已被未知提交推进，立即停止并报告 `INPUT_DRIFT`。

## 2. 已核实的失败事实

### 2.1 Ruff：10 条，不是行为测试失败

GitHub Job `101435507343` 执行 `python -m ruff check src tests`，得到：

| 文件 | 诊断 |
|---|---|
| `tests/conformance/v4/driver.py` | `I001`、`UP035`、`N818` |
| `tests/conformance/v4/scenarios.py` | `UP035` |
| `tests/conformance/v4/test_c0_contract_authority.py` | `I001` |
| `tests/conformance/v4/test_c5_convergence.py` | `I001` |
| `tests/conformance/v4/test_c7_idempotency.py` | `I001`、`F401` |
| `tests/conformance/v4/test_mcp_surface_contract.py` | `I001` |
| `tests/conformance/v4/test_meta_profile_boundary.py` | `I001` |

其中 9 条可由 Ruff 安全修复；`N818` 对应测试专用异常类 `V4NotImplemented`。

### 2.2 Stability Charter：门禁提取算法错误

GitHub Job `101435507259` 已确认：

- `CHANGELOG.md` 存在 `## [Unreleased]`；
- 该节存在 `### Added — fcop`；
- 正则 `^### (Added|Changed|Deprecated|Removed)` 本可匹配该标题；
- 失败来自 `awk '/^## \[Unreleased\]/,/^## \[/' CHANGELOG.md`：开始行自身也匹配结束表达式，所以输出只有一行。

这不是 CHANGELOG 内容缺失，不得通过增加重复标题或改写已正确的变更记录来规避。

## 3. 唯一允许的修改

### 3.1 七个冻结 Conformance 文件的机械静态修正

只允许修改第 2.1 节列出的七个文件，并且只允许：

1. Ruff `I001` 导入排序与格式化；
2. Ruff `UP035` 将 `Callable`、`Mapping`、`Sequence` 移至 `collections.abc`，`Any` 保留在 `typing`；
3. 删除 `test_c7_idempotency.py` 未使用的 `pathlib.Path`；
4. 将 `driver.py` 内测试专用异常类 `V4NotImplemented` 精确重命名为 `V4NotImplementedError`，并仅在同一文件内同步其 4 处引用。

禁止使用 `# noqa`、全局 ignore、per-file ignore、修改 Ruff 配置或 workflow 跳过 Ruff。禁止改变测试 ID、测试函数名、fixture、参数、断言、marker、请求数据、预期错误码和生产入口。

修正前后必须证明：

```yaml
FROZEN_TEST_IDS: 60/60 unchanged
V4_COLLECTED_NODES: unchanged
ASSERTIONS_REMOVED: 0
SKIP_XFAIL_ADDED: 0
TESTS_RENAMED: 0
BEHAVIOR_EXPECTATION_CHANGED: 0
```

### 3.2 Stability Charter 的最小正确性修复

只允许修改 `.github/workflows/test-fcop.yml` 中 `SECTION` 提取语句。必须使其语义成为：

- 遇到精确的 `## [Unreleased]` 后开始采集；
- 不把开始标题本身当作结束标题；
- 遇到下一条 `## [...]` 时停止；
- 保留后续对 `Added|Changed|Deprecated|Removed` 的检查；
- 当前 `### Added — fcop` 必须被识别；
- 缺少上述三级标题的负例仍必须失败。

候选最小实现：

```sh
SECTION=$(awk '
  /^## \[Unreleased\]$/ { capture=1; next }
  capture && /^## \[/ { exit }
  capture { print }
' CHANGELOG.md | head -n 200)
```

允许在不扩大语义的前提下使用等价 POSIX `awk`。不得删除 Stability Charter Job，不得把失败改成 warning，不得无条件成功，不得降低 public-surface 检查。

必须用临时输入完成三项局部证明：

1. 当前 CHANGELOG：PASS；
2. 有 `[Unreleased]` 但无允许三级标题：FAIL；
3. 允许标题只出现在下一个版本节：FAIL。

临时文件不得提交。

### 3.3 证据文件

只允许新增：

- `reports/FCOP-4.0-WP4A.2-CI-GATE-DIAGNOSIS.md`
- `reports/FCOP-4.0-WP4A.2-RESULT.md`
- `reviews/fcop-4.0/wp4a.2/MANIFEST.md`

旧报告、旧 Manifest 和失败记录必须保留，不得重写历史。

## 4. 明确禁止

不得修改：

- 两份冻结 4.0 Spec；
- `spec/schemas/v4/**` 与 `src/fcop/_data/schemas/v4/**`；
- `src/fcop/**`、`mcp/**`、`CHANGELOG.md`、`pyproject.toml`；
- public-surface snapshot、CodeFlowMu、`main`、Release、PyPI、产品版本号。

不得新增依赖、后台组件、数据库、authoritative store、状态机、锁系统、公开 API 或 Base error code。

## 5. 执行顺序

### Step 1：保存输入证据

记录 PR #14 当前 head、任务书提交、失败 workflow run、两个失败 Job 的 URL/ID，以及修改前 Ruff 10 条完整清单。

### Step 2：修 Ruff 并证明语义未变

仅对七个白名单文件执行定向 Ruff 修复；手工完成唯一的异常类重命名。检查 Git diff，确认没有越出允许的 import/identifier 范围。

至少执行：

```text
python -m ruff check src tests
python -m pytest tests/conformance/v4 --collect-only -q
python -m pytest tests/conformance/v4 -q
python -m pytest tests/test_fcop -q
```

### Step 3：修 Stability Charter 提取

只改第 3.2 节所述一处。运行三项正负局部证明，并在诊断报告中保存命令、退出码和关键输出。

### Step 4：运行 WP4A 回归

至少运行 `python -m mypy src/fcop`、`python -m pytest tests/test_fcop -q`、`python -m pytest tests/test_fcop_mcp -q`，并按 WP4A.1 既有脚本复核：

- Schema source/package parity 12/12；
- Schema binding 10/10；
- v4 Conformance 119/119；
- minimal sequential app；
- minimal parallel family app；
- clean wheel install；
- public-surface drift = 0。

不得伪造 Linux/macOS 原生测试；跨平台结论只来自 GitHub Actions。

### Step 5：在 PR #14 上追加两提交交付

在现有 review 分支及 Draft PR #14 上顺序追加：

1. Content Commit：八个允许修改的既有文件，加两份新增报告；
2. Manifest Commit：只新增 WP4A.2 Manifest。

Manifest 必须记录全部交付文件 SHA-256、父链、测试结果、零越界统计、PR URL、Content Commit 与自身提交规则。推送后必须重新 fetch，并验证 remote head 与全部哈希。

不得 force-push，不得改写 WP4A.1 提交历史。

### Step 6：等待最终远端 CI

必须等待 PR #14 新 head 对应的全部 required checks 完成。至少确认：

- test-fcop：12 个 OS/Python matrix、Coverage、Stability Charter、package 全绿；
- test-fcop-mcp：全矩阵、tool contract、package 全绿。

本地通过不能代替 GitHub CI。任一失败、取消、缺失或非预期跳过，状态仍为 `BLOCKED`，不得请求 Gate。

## 6. 完成判据

```yaml
WP4A_2_STATUS: COMPLETE
RUFF_DIAGNOSTICS_BEFORE: 10
RUFF_DIAGNOSTICS_AFTER: 0
STABILITY_SECTION_EXTRACTION: CORRECTED
STABILITY_POSITIVE_CASE: PASS
STABILITY_NEGATIVE_CASES: 2/2 PASS
FROZEN_TEST_IDS: 60/60
V4_CONFORMANCE: 119/119
TEST_FCOP: PASS
MCP_REGRESSION: PASS
SCHEMA_SOURCE_PACKAGE_PARITY: 12/12
PUBLIC_SURFACE_DRIFT: 0
GITHUB_CI_AT_FINAL_HEAD: PASS
UNEXPECTED_FAILURES: 0
MAIN_MODIFIED: false
RELEASE_CREATED: false
WP4B_STARTED: false
```

完成后唯一可请求：`WP4A_MACHINE_CONTRACT_ACCEPTED`。Codex 不得自行签署 Gate。

## 7. 强制停止条件

遇到以下任一情况立即停止并报告，不得扩大修复：

- 10 条之外出现新的 Ruff 错误；
- Ruff 修复要求改变测试行为；
- Stability Charter 仍需修改 CHANGELOG 或放宽规则才能通过；
- frozen contract、Schema、生产代码、MCP 或 CodeFlowMu 需要修改；
- PR head/input parent chain 不一致；
- GitHub CI 非全绿；
- 需要 force-push、合并 main 或发布。

## 8. 最终回执格式

```yaml
WP4A_2_STATUS: COMPLETE | BLOCKED
AUTHORIZED_SCOPE: WP4A_2_ONLY
TASKBOOK_COMMIT: ""
TASKBOOK_SHA256: ""
INPUT_HEAD: 6ff8f213313c1f802e3498d2196b8c3bd363ceb5
WORKTREE: ""
BRANCH: review/fcop-4.0-wp4a.1-machine-contract
DRAFT_PR: 14

RUFF_DIAGNOSTICS_BEFORE: 10
RUFF_DIAGNOSTICS_AFTER: ""
RUFF_FILES_CHANGED: 7
FROZEN_TEST_IDS: ""
V4_COLLECTED_NODES: ""
ASSERTIONS_REMOVED: 0
SKIP_XFAIL_ADDED: 0
TESTS_RENAMED: 0
BEHAVIOR_EXPECTATION_CHANGED: 0

STABILITY_SECTION_EXTRACTION: ""
STABILITY_POSITIVE_CASE: ""
STABILITY_NEGATIVE_CASES: ""
V4_CONFORMANCE: ""
TEST_FCOP: ""
MCP_REGRESSION: ""
SCHEMA_SOURCE_PACKAGE_PARITY: ""
PUBLIC_SURFACE_DRIFT: ""

CONTENT_COMMIT: ""
MANIFEST_COMMIT: ""
REMOTE_HEAD: ""
REMOTE_REFETCH_VERIFIED: ""
DELIVERY_SHA256: ""
GITHUB_CI_AT_FINAL_HEAD: ""

FROZEN_SPEC_FILES_MODIFIED: 0
SCHEMA_FILES_MODIFIED: 0
PRODUCTION_FILES_MODIFIED: 0
MCP_IMPLEMENTATION_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0
WORKFLOW_FILES_MODIFIED: 1
CHANGELOG_FILES_MODIFIED: 0
MAIN_MODIFIED: false
RELEASE_CREATED: false
WP4B_STARTED: false
REQUESTED_GATE: WP4A_MACHINE_CONTRACT_ACCEPTED | NONE
```

完成或阻断后必须停止。
