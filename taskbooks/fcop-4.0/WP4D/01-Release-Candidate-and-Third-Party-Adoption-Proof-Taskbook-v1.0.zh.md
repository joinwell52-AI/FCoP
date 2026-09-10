# FCoP 4.0 WP4D：Release Candidate 与第三方采用证明执行任务书 v1.0

```yaml
document_role: EXECUTION_TASKBOOK
execution_authorized: true
authorized_scope: WP4D_ONLY
work_package: WP4D
target_candidate:
  fcop: 4.0.0rc1
  fcop-mcp: 4.0.0rc1
parent_gate: WP4C_RULE_DISTRIBUTION_ACCEPTED
parent_gate_commit: 167c5fd4ca4c9603c392bae3a4a055963e7b7ed6
parent_gate_evidence: https://github.com/joinwell52-AI/FCoP/pull/30#issuecomment-5597655457
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

## 0. 执行结论先行

本任务书授权执行 **WP4D 且仅限 WP4D**：把已由固定 Gate 验收的 FCoP 4.0 Core、MCP 与规则分发实现封装为未发布的 `4.0.0rc1` 候选制品，并用同一组候选制品完成可复现构建、跨平台 clean-room、最小第三方项目、恢复与兼容性证明。

本任务不授权合并 `main`，不授权创建 tag，不授权上传 PyPI，不授权 GitHub Release、MCP Registry 或 Zenodo，也不授权修改 CodeFlowMu。`FCOP_4_RC_ACCEPTED` 只表示固定候选提交及其固定制品通过验收；它不隐含任何发布或合并授权。

WP4D 不得新增、删除或改变 FCoP 4.0 协议行为。若证明过程中发现必须修改规范、Conformance、Core、MCP 公开行为或规则语义，必须阻断并停止。

## 1. 权威基线与阶段边界

### 1.1 唯一实现基线

- 仓库：`joinwell52-AI/FCoP`
- 固定提交：`167c5fd4ca4c9603c392bae3a4a055963e7b7ed6`
- Gate：`WP4C_RULE_DISTRIBUTION_ACCEPTED`
- Gate 只覆盖上述固定提交；不得把后续提交追认进该 Gate。
- `main` 当前未包含 WP4C；不得以 `main` 为本任务实现起点。

执行人必须先验证：

```powershell
git fetch origin --prune
git cat-file -e 167c5fd4ca4c9603c392bae3a4a055963e7b7ed6^{commit}
git show -s --format=%H 167c5fd4ca4c9603c392bae3a4a055963e7b7ed6
```

输出必须精确为固定提交。失败即停止，不得从近似分支或 `main` 继续。

### 1.2 已验收事实，不得在 WP4D 重开设计

- 本地合并回归：`1912/1912` 通过。
- 最终 HEAD CI：`27/27` 个适用 Job 通过，其中 Windows `8/8`。
- 两项仅限 PR 事件的检查未运行，不得记为通过。
- MCP 规范面：`46` 个 tools、`12` 个静态 resources、`4` 个 resource templates。
- FCoP 4.0 权威候选文件：`19/19` 完整。
- WP4C 权威文件字节冻结：`21/21` 未变。
- CodeFlowMu 仅作为固定 `3.2.5` 消费者进行只读 shadow；本任务无写权限。

这些数据是起跑线，不是允许删除回归、调低阈值或改变协议的理由。

### 1.3 版本与 Gate 对齐

本任务的唯一候选版本为：

```text
fcop==4.0.0rc1
fcop-mcp==4.0.0rc1
```

历史计划中的 `RELEASE_CANDIDATE_VERIFIED` 由当前 WP4 主任务书的 `FCOP_4_RC_ACCEPTED` 取代；不得请求或自行签署两个同义 Gate。稳定版 `4.0.0`、公开 RC、stable release 都属于后续独立授权。

## 2. 分支、worktree 与 PR

### 2.1 任务书分支

本任务书位于：

```text
task/fcop-4.0-wp4d-rc-candidate
```

任务书分支只能包含 `taskbooks/**`。

### 2.2 实现分支

执行人从本任务书分支的固定 HEAD 建立：

```text
feat/fcop-4.0-wp4d-rc-candidate
```

这里使用 `feat/**` 是为了命中仓库现有 push CI 分支过滤；它不授权修改功能语义。建议独立 worktree：

```text
D:\FCoP-wp4d-rc-candidate
```

禁止复用其他阶段的脏 worktree。创建后必须记录：任务书提交、实现起点、`git status --short`、Python 与平台版本。

### 2.3 Draft PR

实现 PR 必须：

- base：`task/fcop-4.0-wp4d-rc-candidate`
- head：`feat/fcop-4.0-wp4d-rc-candidate`
- 标题：`[DO NOT MERGE][FCoP 4.0 WP4D] RC candidate verification`
- Draft 状态保持到 ADMIN 明确处理。
- 不得改为以 `main` 为 base。
- 不得自行合并。

## 3. 本任务允许修改的内容

### 3.1 候选身份与依赖契约

必须完成以下精确修改：

1. `src/fcop/_version.py` → `4.0.0rc1`。
2. `mcp/src/fcop_mcp/_version.py` → `4.0.0rc1`。
3. `mcp/pyproject.toml` 中 FCoP 依赖精确为：

   ```text
   fcop>=4.0.0rc1,<4.1.0
   ```

4. `mcp/src/fcop_mcp/routing.py` 的包兼容集合加入精确候选对 `("4.0.0rc1", "4.0.0rc1")`。
5. 可保留历史 `("3.2.5", "3.2.5")` 对用于历史/source 测试，但安装态的错配组合必须 fail closed。
6. 不得提前加入 `("4.0.0", "4.0.0")`。
7. 两个 `pyproject.toml` 的开发状态 classifier 改为 Beta；不得宣称 Stable。
8. 修正根包元数据中“仅 library + PyYAML”之类与实际依赖不符的描述；只允许元数据纠错，不得改依赖行为。

必须修正现有版本约束检查，使其强制 **相同 major.minor**，并正确理解 pre-release 下界。`fcop>=4.0.0rc1,<5.0` 之类 major-wide 上界必须失败。允许修改：

- `tests/test_fcop/test_pyproject_pins.py`
- `scripts/release_audit.py` 中仅与该依赖契约相关的检查；或新增 `scripts/fcop_rc_candidate_check.py`

### 3.2 最小第三方项目与验证脚本

允许新增：

```text
examples/v4/third-party/python-only/**
examples/v4/third-party/mcp-only/**
tests/rc/**
tests/test_fcop/test_wp4d_rc*.py
tests/test_fcop_mcp/test_wp4d_rc*.py
scripts/fcop_rc_candidate_check.py
scripts/wp4d_*.py
```

脚本与示例只能消费公开接口，不得为测试方便导入内部私有实现。所有临时 workspace、规则目录与日志必须位于测试临时目录。

### 3.3 候选 CI

允许新增：

```text
.github/workflows/rc-candidate.yml
```

该 workflow 必须：

- `permissions: contents: read`；
- 不引用发布 secrets；
- 不配置发布 environment；
- 不上传到任何 registry；
- 在 `feat/fcop-4.0-wp4d-rc-candidate` push 上运行，可附加 `workflow_dispatch`；
- 构建候选制品一次并把同一制品分发给所有 consumer jobs；
- 上传候选制品与哈希 manifest 为 GitHub Actions artifact，建议保留 `90` 天；
- workflow artifact 不是公开发布。

### 3.4 文档与报告

允许更新或新增：

```text
CHANGELOG.md
fcop-README.pypi.md
mcp/README.md
docs/fcop-4.0/rc-candidate*.md
docs/releases/4.0.0rc1.md
reports/FCOP-4.0-WP4D-*.md
reviews/fcop-4.0/wp4d/MANIFEST.md
```

所有文字必须称其为“未发布候选”或同义明确表述。不得声称 PyPI、GitHub Release、Registry、Zenodo 或 `main` 已更新。

## 4. 冻结与禁止修改

下列内容在 WP4D 冻结：

- `specs/**`
- 全部 FCoP 4.0 Conformance 规范与 golden 数据
- 已验收的 19 个权威候选文件与 21 个冻结文件的字节
- Core 生产行为实现
- MCP tools/resources/templates/server 行为
- 规则发现、选择、锁定、部署、回滚的生产语义
- 现有回归阈值与断言语义
- `.github/workflows/release.yml`
- `mcp/server.json`
- `CITATION.cff`
- v3 bundled rules、`AGENTS.md`、`CLAUDE.md`、`.cursor/**`
- CodeFlowMu 仓库的全部内容

`mcp/server.json` 继续保留已公开的 `3.2.5` 信息；未发布候选不得冒充 Registry 已可获取。`CITATION.cff` 继续指向已公开版本/DOI。正式发布工作流的 hardened publish、tag、protected ADMIN environment 与同制品发布属于后续独立任务，WP4D 只审计并记录差距。

任何需要突破冻结区的情况都必须停止并报告：

```text
WP4D_STATUS: BLOCKED
REQUESTED_GATE: NONE
```

## 5. 候选制品的确定性构建

### 5.1 必须产出的四个文件

在 Ubuntu、Python 3.12 的隔离构建 job 中生成：

```text
fcop-4.0.0rc1-py3-none-any.whl
fcop-4.0.0rc1.tar.gz
fcop_mcp-4.0.0rc1-py3-none-any.whl
fcop_mcp-4.0.0rc1.tar.gz
```

必须设置并记录固定 `SOURCE_DATE_EPOCH`。同一提交在两个全新构建目录中各构建一遍，四个文件必须分别逐字节一致（`4/4` SHA-256 相同）。不得把第二次构建产生的混合文件替换进第一组。

对两组均执行 `python -m twine check`。检查 sdist 与 wheel 的成员清单、METADATA、版本、依赖约束；不得包含测试缓存、构建目录、秘密、绝对路径或未跟踪文件。

生成机器可读 JSON 哈希清单，至少包含：

- 仓库与候选提交 SHA
- Python、build、setuptools/wheel 版本
- `SOURCE_DATE_EPOCH`
- 四个制品的文件名、大小、SHA-256
- 构建时间与 workflow run ID

### 5.2 同一制品约束

后续所有 clean-room、跨平台、第三方采用和恢复测试必须下载并验证第一组固定四制品的哈希；不得在 consumer job 中重建。若任一 job 看到不同哈希，立即失败。

后续如 ADMIN 单独授权公开 RC，必须使用这组精确制品。若 artifact 已过期，只允许在独立授权下从固定提交复建且 `4/4` 哈希完全复现；否则必须重新走候选验收。

## 6. Clean-room 与跨平台矩阵

### 6.1 强制矩阵

对以下 `12` 个组合全部运行：

| OS | Python |
|---|---|
| Ubuntu | 3.10、3.11、3.12、3.13 |
| Windows | 3.10、3.11、3.12、3.13 |
| macOS | 3.10、3.11、3.12、3.13 |

每个 job 必须：

1. 下载固定候选 artifact 并核验 JSON manifest 与四个 SHA-256。
2. 在 checkout 目录之外创建全新 venv。
3. 只从固定 wheel/sdist 安装候选 `fcop` 与 `fcop-mcp`；不得 editable install。
4. 不设置指向仓库的 `PYTHONPATH`。
5. 证明 `fcop.__file__` 与 `fcop_mcp.__file__` 位于 venv 的 site-packages，而不是 checkout。
6. 对 wheel 与 sdist 安装路径分别验证；可拆 job，但最终必须覆盖两种来源。
7. 运行期间禁止应用访问网络；安装普通第三方依赖可使用包索引，但候选双包只能来自已核验 artifact。
8. 执行第 7、8、9 节的公共接口探针。

任何适用矩阵项被 skipped、cancelled 或 allowed failure 都不能计为通过。

### 6.2 安装态版本错配

至少验证：

- `4.0.0rc1 / 4.0.0rc1` 成功。
- 候选 MCP 与 `3.2.5` Core 错配时 fail closed。
- `3.2.5` MCP 与候选 Core 错配时 fail closed（若可在隔离 fixture 中构造）。
- 报错可诊断，且失败前无 workspace 或规则副作用。

## 7. 最小第三方采用证明

### 7.1 Python-only 项目

`examples/v4/third-party/python-only/` 必须是可复制到仓库外运行的最小项目：

- 只依赖安装态 `fcop`；
- 不读取仓库源码；
- 显式创建 4.0 workspace；
- 执行顺序流程；
- 执行一层 Branch 并显式 convergence；
- 关闭进程后在新进程 reopen，校验状态、事件与结果一致；
- 输出确定性的机器可读摘要。

### 7.2 MCP-only 项目

`examples/v4/third-party/mcp-only/` 必须模拟真正的外部 MCP 客户端：

- 客户端不得 import `fcop` 或 `fcop_mcp`；
- 通过 stdio JSON-RPC 启动安装态 `fcop-mcp`；
- 使用规范发现结果，而不是硬编码私有函数；
- 覆盖创建、顺序流程、一层 Branch、显式 convergence、关闭与新进程 reopen；
- 核验公开面精确为 `46 tools / 12 static resources / 4 templates`；
- 输出确定性的机器可读摘要。

两个项目必须在 12 组合矩阵中运行，不得只在源码 checkout 内演示。

## 8. 恢复、重试与零副作用证明

用安装态公共接口覆盖：

### 8.1 response-loss retry

- 服务端完成一次合法变更后模拟响应丢失。
- 客户端以相同幂等身份重试。
- 最终结果与首次结果一致。
- 事件、任务、结果与外部效应不得重复。
- 重新打开 workspace 后结论仍成立。

### 8.2 crash recovery

- 在明确的持久化边界后终止进程。
- 新进程从磁盘 reopen。
- 恢复后的状态、事件链、Branch/convergence 与锁定规则上下文一致。
- 不得依赖进程内 monkeypatch 状态来“证明”恢复。

### 8.3 失败零副作用

版本错配、规则缺失、digest 冲突、context overflow 等拒绝路径必须分别证明：

- 返回精确、稳定、可诊断的错误码；
- 不创建或改变 workspace 状态；
- 不写入目标规则目录；
- 不产生部分部署或重复外部效应。

## 9. 兼容性、规则分发与 CodeFlowMu

### 9.1 固定 3.2.5 workspace

必须使用由已验收 `3.2.5` 行为生成或固定保存的 workspace fixture，执行候选 `4.0.0rc1` 的只读兼容访问：

- 不迁移；
- 不重写；
- 不漂移；
- 执行前后整棵 fixture 文件树 SHA-256 完全一致；
- 证明 4.0 workspace 必须由显式 4.0 创建路径产生。

不得把 legacy v3 目录、bundled rules 或声明文件重标为 4.0。

### 9.2 Host 规则分发

在临时目录用安装态候选覆盖：

- 规则发现与选择；
- 缺失规则；
- digest 冲突；
- context overflow；
- deploy；
- rollback；
- 拒绝路径零副作用；
- deploy/rollback 后内容与哈希可核验。

### 9.3 CodeFlowMu 固定 shadow

在最终候选提交上重跑已定义的 CodeFlowMu `3.2.5` 固定消费者只读 shadow：

- 预期 `14/14`；
- 固定依赖和 fixture，不升级 CodeFlowMu；
- 运行前后 CodeFlowMu 工作树、tracked/untracked 清单与字节哈希一致；
- 不提交、不推送、不创建 PR。

## 10. 全量回归与静态守卫

### 10.1 修改前基线

从固定起点先重跑 `1912/1912`。如不能复现，停止；不得用候选版本修改掩盖基线失败。

### 10.2 修改后要求

最终 Manifest HEAD 必须满足：

- 原有全量回归全部通过，零失败、零意外 skip；
- 新增 WP4D 测试全部通过；
- 现有最终适用 CI `27/27` 通过，Windows `8/8`；
- 新 RC workflow 的构建、可复现与 12 组合 consumer 矩阵全部通过；
- MCP 公开面仍精确为 `46/12/4`；
- 权威候选文件 `19/19`；
- WP4C 冻结文件 `21/21` 字节未变；
- 双包版本、候选依赖 pin、兼容对完全一致；
- source checkout、wheel、sdist 的公开行为一致；
- 两个第三方项目、response-loss、crash recovery、3.2.5 零漂移、Host 规则矩阵与 CodeFlowMu shadow 全部通过。

### 10.3 禁止通过的方式

不得：

- 删除、跳过、xfail 或弱化旧测试；
- 修改断言以接受错误行为；
- 只在单一 OS 或单一 Python 上取样；
- 把未运行检查写成通过；
- 用源码 import 冒充已安装制品；
- 在各矩阵项分别重建并称为“同一制品”；
- 忽略 sdist 或只验证 wheel；
- 用发布动作验证发布配置。

## 11. 提交纪律

实现分支至少分为三类提交：

1. **候选内容提交**：版本/元数据、只限兼容表、测试、脚本、示例、RC workflow 与候选文档。
2. **证据提交**：只含报告与测试证据；不得再改候选内容。
3. **Manifest-only 提交**：只修改 `reviews/fcop-4.0/wp4d/MANIFEST.md`。

推送后不得 force-push。若 Manifest 后又改候选内容，原证据失效，必须重跑全部要求并生成新的证据提交和 Manifest-only 提交。

## 12. 必交报告

最终必须交付：

```text
reports/FCOP-4.0-WP4D-RC-IDENTITY-AND-VERSION.md
reports/FCOP-4.0-WP4D-ARTIFACT-REPRODUCIBILITY.md
reports/FCOP-4.0-WP4D-THIRD-PARTY-ADOPTION.md
reports/FCOP-4.0-WP4D-RESILIENCE-AND-COMPATIBILITY.md
reports/FCOP-4.0-WP4D-CI-AND-RELEASE-READINESS.md
reports/FCOP-4.0-WP4D-RESULT.md
reviews/fcop-4.0/wp4d/MANIFEST.md
```

每份报告必须给出命令、起止时间、平台、返回码、总数、失败数、skip 数、日志/Actions URL、固定提交、制品 SHA-256，并明确区分“通过”“未运行”“不适用”。

`CI-AND-RELEASE-READINESS` 必须审计但不得触发 `.github/workflows/release.yml`，并明确列出后续公开 RC/稳定发布尚需的独立授权与工作流硬化项，包括：tag 约束、RC/stable 区分、ADMIN protected environment、同一制品发布与 PyPI 回装核验。

### 12.1 Manifest 必含字段

```yaml
wp4d_status: COMPLETE | BLOCKED
base_commit: <sha>
candidate_commit: <sha>
evidence_commit: <sha>
manifest_commit: <sha-or-self-marker>
target_versions:
  fcop: 4.0.0rc1
  fcop-mcp: 4.0.0rc1
artifact_hashes: <four exact sha256 values>
artifact_reproducibility: 4/4
legacy_regression: <passed>/<total>
wp4d_tests: <passed>/<total>
existing_ci_applicable: <passed>/<applicable>
windows_existing_ci: <passed>/8
rc_consumer_matrix: <passed>/12
mcp_surface: 46/12/4
canonical_files: 19/19
frozen_bytes: 21/21
codeflowmu_shadow: 14/14
main_merge_authorized: false
rc_publish_authorized: false
stable_release_authorized: false
pypi_publish_authorized: false
github_release_authorized: false
mcp_registry_publish_authorized: false
zenodo_publish_authorized: false
codeflowmu_write_authorized: false
requested_gate: FCOP_4_RC_ACCEPTED | NONE
```

远端最终 HEAD 上必须回读全部交付文件并逐一核验 SHA-256。报告与 Manifest 中只记录远端值，不得仅引用本地文件。

## 13. 停止条件与回执格式

### 13.1 完成

只有第 5–12 节全部满足时，停止并请求：

```text
WP4D_STATUS: COMPLETE
REQUESTED_GATE: FCOP_4_RC_ACCEPTED
RC_PUBLISH_AUTHORIZED: FALSE
MAIN_MERGE_AUTHORIZED: FALSE
```

不得自行签署 Gate。不得继续发布、合并 `main` 或进入后续发布阶段。

### 13.2 阻断

发生以下任一情况即停止：

- 固定基线/Gate 不可核验；
- 必须改变冻结的规范、Conformance 或生产语义；
- 任一全量回归、适用 CI、矩阵、恢复、兼容或哈希检查失败；
- 四制品不可复现；
- 需要发布 secret、tag、registry、main 或 CodeFlowMu 写权限；
- 发现候选身份、依赖 pin 或安装态来源不唯一。

回执：

```text
WP4D_STATUS: BLOCKED
REQUESTED_GATE: NONE
```

必须保留现场、候选文件与日志，不得越权修复冻结区，不得把局部通过写成 WP4D 完成。

## 14. ADMIN 验收口径

ADMIN 只验收 Manifest 指向的固定远端 HEAD 与四个固定制品哈希。签署：

```text
FCOP_4_RC_ACCEPTED
```

其含义仅为：该固定提交的 `4.0.0rc1` 候选身份、制品、跨平台第三方采用、恢复与兼容证据被接受。它不授权：

- 合并 `main`
- 创建或推送 tag
- 发布公开 RC 或 stable
- 上传 PyPI
- 创建 GitHub Release
- 更新 MCP Registry
- 更新 Zenodo/DOI/CITATION
- 修改 CodeFlowMu

上述任何动作均需下一份独立授权任务书与对应 Gate。
