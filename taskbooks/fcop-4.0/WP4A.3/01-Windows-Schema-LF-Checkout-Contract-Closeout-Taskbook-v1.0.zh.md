---
title: "FCoP 4.0 WP4A.3：Windows Schema LF 检出合同收口任务书"
document_role: EXECUTION_TASKBOOK
status: AUTHORIZED_FOR_WP4A_3_ONLY
execution_authorized: true
authorized_scope: WP4A_3_ONLY
input_head: 2ef95e5afdabfc7aa25a93fb287827682b467c9d
frozen_contract_commit: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
draft_pr: 14
main_merge_authorized: false
release_authorized: false
wp4b_authorized: false
---

# FCoP 4.0 WP4A.3：Windows Schema LF 检出合同收口任务书

## 0. ADMIN 裁决

WP4A.2 已正确修复 10 条 Ruff 与 Stability Charter；其交付和失败证据全部保留。当前新阻断不是 Schema 内容不一致，也不是 Python 3.10 独有问题，而是 Windows checkout 在没有 `.gitattributes` 的仓库中把 24 个已提交为 LF 的 v4 Schema 文件检出为 CRLF，随后严格的 `generate.py --check` 按原始字节比较并正确报告 drift。

正式状态：

```yaml
WP4A_2_DELIVERY: PRESERVED
WP4A_MACHINE_CONTRACT_ACCEPTED: false
WP4A_3_AUTHORIZED: true
AUTHORIZED_SCOPE: WP4A_3_ONLY
MAIN_MERGE_AUTHORIZED: false
RELEASE_AUTHORIZED: false
WP4B_AUTHORIZED: false
```

本任务不允许放宽 Schema 字节合同。正确修复位置是 Git checkout policy，而不是生成器、测试或 Schema 内容。

## 1. 固定输入

```text
Repository: joinwell52-AI/FCoP
Draft PR: https://github.com/joinwell52-AI/FCoP/pull/14
Review branch: review/fcop-4.0-wp4a.1-machine-contract
INPUT_HEAD: 2ef95e5afdabfc7aa25a93fb287827682b467c9d
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
Failed run: https://github.com/joinwell52-AI/FCoP/actions/runs/34017767680
Representative failed job: 101444526767
```

任务书提交必须位于 `INPUT_HEAD` 的无分叉直接后继链。Codex 必须从任务书提交建立独立 worktree，不得修改原 `D:\FCoP` 现场。若 PR #14 head 出现未知推进、父链不符或工作树包含其他改动，停止并报告 `INPUT_DRIFT` 或 `DIRTY_PRESERVED`。

## 2. 已核实事实

### 2.1 失败范围

GitHub run `34017767680` 的真实结果：

| Job | 结果 |
|---|---|
| Ubuntu Python 3.10–3.13 | 4/4 PASS |
| macOS Python 3.10–3.13 | 4/4 PASS |
| Windows Python 3.10–3.13 | 0/4 PASS，均为 Schema drift |
| Coverage | PASS |
| Stability Charter | PASS |
| test-fcop-mcp workflow | PASS |
| fcop package job | 因 Windows matrix 失败而 skipped |

因此不得把问题描述为“仅 Windows/Python 3.10”。四个 Windows 版本都复现同一 checkout 字节问题。

### 2.2 字节链

`spec/schemas/v4/generate.py` 生成：

```python
data = (json.dumps(..., indent=2) + "\n").encode()
```

并用 `path.read_bytes() != data` 做严格比较。这一设计用于证明 source Schema 与 package Schema 的逐字节一致性，不得改为文本归一化比较。

仓库当前没有 `.gitattributes`。GitHub Windows runner 的 checkout 把两处 v4 Schema 目录中的 24 个 JSON 工作树文件转为 CRLF，因此全部被报告为 drift；Git blob 与 Linux/macOS checkout 仍为 LF。

## 3. 唯一授权修改

### 3.1 新增最小 `.gitattributes`

在仓库根目录新增 `.gitattributes`，内容必须精确限制为两处 v4 Schema：

```gitattributes
spec/schemas/v4/*.schema.json text eol=lf
src/fcop/_data/schemas/v4/*.schema.json text eol=lf
```

允许文件末尾一个 LF。不得扩大到全仓 `*.json`、`*.py`、`*.md` 或其他历史目录；不得设置 binary、`-text`、working-tree-encoding 或全局 Git 配置。

### 3.2 新增证据

只允许新增：

- `reports/FCOP-4.0-WP4A.3-WINDOWS-SCHEMA-CHECKOUT-POLICY.md`
- `reports/FCOP-4.0-WP4A.3-RESULT.md`
- `reviews/fcop-4.0/wp4a.3/MANIFEST.md`

旧报告、旧 Manifest、旧失败 Run 与 WP4A.2 提交不得修改或删除。

## 4. 禁止事项

本轮禁止修改：

- 24 个 v4 Schema 文件的任何字节；
- `spec/schemas/v4/generate.py`；
- `tests/**`；
- `.github/workflows/**`；
- 两份冻结 Spec；
- `src/fcop/**`、`mcp/**`、`CHANGELOG.md`、`pyproject.toml`；
- public-surface snapshot、CodeFlowMu、版本号、main、Release、PyPI。

禁止：

- 把 `read_bytes()` 改为 `read_text()`；
- 在比较前替换 CRLF/LF；
- 跳过 Windows 测试；
- 使用 `continue-on-error`、warning 或条件排除 Windows；
- 重新生成并提交 24 个 Schema 以制造无意义大 diff；
- 修改 runner 的全局 `core.autocrlf` 作为产品修复；
- force-push 或改写既有提交历史；
- 使用 PowerShell 改写中文任务书、报告或 Manifest。

不得新增依赖、Runtime、数据库、后台组件、authoritative store、状态机、锁系统、公开 API 或 Base error code。

## 5. 执行步骤

### Step 1：复核输入与失败

读取 run `34017767680` 的全部 Job，不得只引用代表性 3.10 Job。报告四个 Windows Job ID、结论及相同失败节点：

```text
tests/test_fcop/test_v4_schema.py::test_schema_parity_ids_offline_and_required_negative_matrix
```

确认 stderr 同时列出 source/package 两套共 24 个 Schema 路径。

### Step 2：增加精确属性

仅新增第 3.1 节规定的 `.gitattributes`。执行：

```text
git check-attr text eol -- spec/schemas/v4/workspace.schema.json
git check-attr text eol -- src/fcop/_data/schemas/v4/workspace.schema.json
```

两条都必须得到 `text: set`、`eol: lf`。再检查一个范围外 JSON，证明没有获得本任务新增的 `eol=lf` 规则。

### Step 3：证明 Schema blob 零变化

以 `INPUT_HEAD` 为基准记录两处目录全部 24 个 Git blob SHA 和 SHA-256；修复后必须完全一致：

```yaml
V4_SCHEMA_FILES: 24
V4_SCHEMA_BLOB_DRIFT: 0
V4_SCHEMA_SHA256_DRIFT: 0
SOURCE_PACKAGE_SCHEMA_PARITY: 12/12
```

若 `git diff --name-only INPUT_HEAD..HEAD` 中出现任何 Schema 文件，立即停止，不得提交。

### Step 4：本地与干净检出验证

当前 worktree 可能在属性加入前已经检出 CRLF，不能把旧工作树状态冒充最终 checkout 结果。至少完成：

1. 当前树运行 `python spec/schemas/v4/generate.py --check`；若因旧 checkout 仍红，只能如实记录，不得修改生成器或 Schema；
2. 在 `.gitattributes` 已进入提交后，建立一个新的、可丢弃的 Windows clean checkout/worktree；
3. 新 checkout 中确认 24 个文件均无 `CRLF`，运行 `generate.py --check` 得到 12 schema pairs verified；
4. 新 checkout 运行 `python -m pytest tests/test_fcop/test_v4_schema.py -q`；
5. 临时目录不得提交。

不得使用已经预先归一化的 LF 验证树代替“从含 `.gitattributes` 的提交新检出”证据。

### Step 5：完整回归

至少执行：

```text
python -m ruff check src tests
python -m mypy src/fcop
python -m pytest tests/conformance/v4 -q
python -m pytest tests/test_fcop -q
python -m pytest tests/test_fcop_mcp -q
```

并复核：

- v4 Conformance 119/119；
- frozen Test IDs 60/60；
- Schema binding 10/10；
- Schema source/package parity 12/12；
- public-surface drift 0；
- minimal sequential/family app PASS；
- clean wheel install PASS。

### Step 6：两提交交付

在现有 review 分支和 Draft PR #14 上追加：

1. Content Commit：`.gitattributes` 与两份报告；
2. Manifest Commit：只新增 `reviews/fcop-4.0/wp4a.3/MANIFEST.md`。

Manifest 必须列出 4 个交付文件 SHA-256、父链、零漂移证明、本地/clean-checkout 结果和最终 CI 等待规则。推送后重新 fetch，验证 remote head、提交父链和 4/4 哈希。不得追加第三个证据提交。

### Step 7：等待最终 CI

最终裁决只认 PR #14 最新 Manifest head 对应的远端 CI。必须确认：

- Windows Python 3.10、3.11、3.12、3.13 全部 PASS；
- Ubuntu/macOS 8 个矩阵全部 PASS；
- Ruff、mypy、1190 项 test-fcop、Coverage、Stability Charter 全部 PASS；
- fcop package 不再 skipped，并完成 build/install/audit；
- test-fcop-mcp workflow 全部 PASS。

任务书提交自身触发的中间 CI 不可作为最终证据。任一失败、取消、缺失或非预期 skipped，必须 `BLOCKED` 并停止。

## 6. 完成判据

```yaml
WP4A_3_STATUS: COMPLETE
CHECKOUT_POLICY_FILE: .gitattributes
CHECKOUT_POLICY_SCOPE: V4_SCHEMA_ONLY
WINDOWS_MATRIX: 4/4
LINUX_MACOS_MATRIX: 8/8
V4_SCHEMA_FILES: 24
V4_SCHEMA_BLOB_DRIFT: 0
V4_SCHEMA_SHA256_DRIFT: 0
SCHEMA_SOURCE_PACKAGE_PARITY: 12/12
SCHEMA_CHECK_CLEAN_WINDOWS_CHECKOUT: PASS
V4_CONFORMANCE: 119/119
TEST_FCOP: 1190/1190
MCP_REGRESSION: 80/80
GITHUB_CI_AT_FINAL_HEAD: PASS
UNEXPECTED_FAILURES: 0
MAIN_MODIFIED: false
RELEASE_CREATED: false
WP4B_STARTED: false
```

全部满足后，唯一可请求 Gate：

```yaml
REQUESTED_GATE: WP4A_MACHINE_CONTRACT_ACCEPTED
```

Codex 不得自行签署 Gate。

## 7. 强制停止条件

出现任一情况立即停止：

- 需要修改 `.gitattributes` 之外的既有文件；
- 任何 Schema blob/hash 变化；
- 必须放宽严格字节比较才能通过；
- 发现并非 checkout newline 导致；
- 四个 Windows Job 未全部通过；
- 需要修改 workflow、测试、生产实现、MCP 或 CodeFlowMu；
- 需要 force-push、合并 main 或发布。

## 8. 最终回执

```yaml
WP4A_3_STATUS: COMPLETE | BLOCKED
AUTHORIZED_SCOPE: WP4A_3_ONLY
TASKBOOK_COMMIT: ""
TASKBOOK_SHA256: ""
INPUT_HEAD: 2ef95e5afdabfc7aa25a93fb287827682b467c9d
WORKTREE: ""
BRANCH: review/fcop-4.0-wp4a.1-machine-contract
DRAFT_PR: 14

WINDOWS_FAILURE_JOBS_REVIEWED: 4/4
CHECKOUT_POLICY_FILE: .gitattributes
CHECKOUT_POLICY_SCOPE: V4_SCHEMA_ONLY
GIT_CHECK_ATTR: ""
V4_SCHEMA_FILES: 24
V4_SCHEMA_BLOB_DRIFT: ""
V4_SCHEMA_SHA256_DRIFT: ""
SCHEMA_SOURCE_PACKAGE_PARITY: ""
SCHEMA_CHECK_CLEAN_WINDOWS_CHECKOUT: ""

RUFF: ""
MYPY: ""
FROZEN_TEST_IDS: ""
V4_CONFORMANCE: ""
TEST_FCOP: ""
MCP_REGRESSION: ""
PUBLIC_SURFACE_DRIFT: ""

CONTENT_COMMIT: ""
MANIFEST_COMMIT: ""
REMOTE_HEAD: ""
REMOTE_REFETCH_VERIFIED: ""
DELIVERY_SHA256: ""
WINDOWS_CI_MATRIX: ""
LINUX_MACOS_CI_MATRIX: ""
PACKAGE_CI: ""
MCP_CI: ""
GITHUB_CI_AT_FINAL_HEAD: ""

GITATTRIBUTES_FILES_MODIFIED: 1
SCHEMA_FILES_MODIFIED: 0
GENERATOR_FILES_MODIFIED: 0
TEST_FILES_MODIFIED: 0
WORKFLOW_FILES_MODIFIED: 0
PRODUCTION_FILES_MODIFIED: 0
MCP_IMPLEMENTATION_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0
MAIN_MODIFIED: false
RELEASE_CREATED: false
WP4B_STARTED: false

REQUESTED_GATE: WP4A_MACHINE_CONTRACT_ACCEPTED | NONE
```

完成或阻断后必须停止。
