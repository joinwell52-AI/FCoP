---
title: "FCoP 4.0 WP4：机器合同、公共适配、规则分发与 RC 总任务书"
version: "1.0"
date: "2026-09-06"
document_role: "AUTHORIZED_MASTER_TASKBOOK"
authority: "ADMIN"
repository: "joinwell52-AI/FCoP"
program: "FCOP_4_0"
work_package: "WP4"
taskbook_branch: "taskbook/fcop-4.0-wp4-public-adapters-distribution"
parent_gate: "FCOP_4_CORE_IMPLEMENTATION_ACCEPTED"
parent_gate_commit: "fea48393be8c83f4dbb6e085f54bb4ce391ee2ed"
effective_core_head: "1d94b881e38cc0b98ca41c47d25c605431d5f9a7"
frozen_contract_commit: "aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6"
execution_authorized: true
authorized_scope: "WP4A_ONLY"
wp4b_wp4c_wp4d_status: "PLAN_ONLY_NOT_AUTHORIZED"
draft_pr_authorized: true
main_merge_authorized: false
release_authorized: false
pypi_publish_authorized: false
github_release_authorized: false
codeflowmu_change_authorized: false
workspace_migration_authorized: false
---

# FCoP 4.0 WP4：机器合同、公共适配、规则分发与 RC 总任务书

## 0. 给执行 Codex 的直接指令

FCoP 4.0 Core 已由 ADMIN 在提交
`fea48393be8c83f4dbb6e085f54bb4ce391ee2ed` 正式签署
`FCOP_4_CORE_IMPLEMENTATION_ACCEPTED`。

本任务书把 Core 之后尚未完成的公共交付工作统一纳入 WP4，消除旧规划中的编号冲突，并固定后续顺序。

本轮唯一允许执行：

> **WP4A：FCoP 4.0 机器可读合同与最小 Python 使用面。**

WP4B、WP4C、WP4D 只用于固定后续边界，不构成执行授权。WP4A 完成后必须通过 GitHub 固定 review 分支交付，停止，并请求：

```yaml
GATE: WP4A_MACHINE_CONTRACT_ACCEPTED
```

不得连续进入 MCP、规则包、Host 适配、RC、主分支合并或发布。

---

## 1. 为什么进入 WP4

WP3A–WP3E 已完成 FCoP 4.0 Core 的真实实现与收口：

- 工作区身份与四类正式信封；
- 五桶生命周期与七条合法迁移；
- attempt、REPORT head、Branch family 与显式汇合；
- Profile evaluator 信任边界和持久 Authorization；
- 创建幂等、迁移收据、恢复五态及冷导出；
- 冻结 v4 Conformance：119/119；
- v3 与 MCP 回归保持通过。

但“Core 实现通过”还不等于第三方已经能够稳定采用 FCoP 4.0。当前仍有四类公共交付缺口：

1. 现有 `spec/schemas/` 是 v1.x 的 8 份旧机器合同，不能代表 FCoP 4.0；
2. `fcop-mcp` 仍固定依赖 `fcop>=3.0.0,<4.0`，45 个工具与 11+3 资源尚未按 workspace version 分派；
3. `AGENTS.md`、`CLAUDE.md` 和 Cursor 规则仍是约 14 万字符的 3.x 整体副本，尚未形成 4.0 模块化规则包；
4. 还没有以打包制品、跨平台 CI 和最小第三方项目证明 4.0 可安装、可使用、可回滚。

因此 WP4 的目标不是增加新的 Core 能力，而是把已经接受的 Core 变成可验证、可装配、可供普通开发者使用的公共协议产品。

---

## 2. 编号与旧任务书处置

### 2.1 旧 WP3F 的正式处置

旧《WP3 实施总任务书》把“适配面：MCP、兼容与 RC”暂称为 WP3F。现在 WP3A–WP3E Core 已验收，该工作正式迁移为：

```yaml
OLD_NAME: WP3F
NEW_CONTAINER: WP4
DISPOSITION: SUPERSEDED_BY_THIS_TASKBOOK
BEHAVIORAL_SCOPE_LOST: false
EXECUTION_AUTHORITY_CARRIED_OVER: false
```

旧 WP3F 从未获得执行授权，因此不存在需要保留的实施结果。

### 2.2 规则包草案的正式处置

分支 `review/fcop-4.0-rule-package-taskbook` 中的：

```text
taskbooks/fcop-4.0/WP3C/
FCoP-4.0-WP3C-rule-package-and-host-adapters-taskbook-v0.1.md
```

方向必须纳入 FCoP 4.0，但其 `WP3C` 编号已被授权面占用，父提交也停留在旧 WP3B 阶段，不能原样执行。

正式处置：

```yaml
DOCUMENT_ROLE: REVIEW_INPUT_ONLY
OLD_WORK_PACKAGE: WP3C
NEW_WORK_PACKAGE: WP4C
PARENT_HEAD_REPLACED_BY: WP4B_ACCEPTED_HEAD
CORE_DIRECTION_RETAINED:
  - CLEAN_REBUILD_FROM_FROZEN_V4_CONTRACT
  - CORE_PLUS_MODULES_PLUS_MANIFEST
  - HOST_THIN_PROJECTIONS
  - ENGINEERING_CONSTITUTION_FOR_FCOP_DEVELOPMENT_ONLY
  - CODEFLOWMU_AS_READ_ONLY_COMPATIBILITY_SHADOW
EXECUTION_AUTHORIZED_BY_OLD_DOCUMENT: false
```

不得把旧草案直接 cherry-pick 后开始实现。WP4C 必须在 WP4B 通过后，由 ADMIN 依据真实代码另发固定任务书。

---

## 3. WP4 的四个小程序式工作包

| 阶段 | 单一职责 | 完成 Gate | 当前授权 |
|---|---|---|---:|
| WP4A | 机器可读合同、Schema registry、最小 Python 示例 | `WP4A_MACHINE_CONTRACT_ACCEPTED` | **已授权** |
| WP4B | MCP 薄适配、workspace version 分派、45/11/3 处置 | `WP4B_MCP_ADAPTER_ACCEPTED` | 未授权 |
| WP4C | 4.0 模块规则包、Manifest、Host 薄投影、开发宪法入口 | `WP4C_RULE_DISTRIBUTION_ACCEPTED` | 未授权 |
| WP4D | wheel/clean-room/跨平台/最小第三方项目/RC 收口 | `FCOP_4_RC_ACCEPTED` | 未授权 |

四个包不是四个 Runtime，也不允许产生新的控制中心。它们围绕同一份冻结规范、同一个 `Project` 公共入口和同一文件事实系统工作。

---

## 4. 全阶段不可改变的底线

1. 文件承载协议，路径表达 NOW，事件记录 PAST。
2. 不增加数据库、消息队列、daemon、timer、watcher、scheduler、session manager 或后台恢复服务。
3. 不建立第二套权威状态、第二个生命周期或第二个授权系统。
4. Schema、MCP、规则和 Host 入口只能表达或调用已接受的 Core，不得重新定义 Core。
5. 3.2.5 工作区继续走 3.x 路径；4.0 工作区必须显式声明版本。
6. 未知版本、未知 Encoding、无法证明的 Profile、歧义状态与摘要漂移一律 Fail Closed。
7. CodeFlowMu 保持 `fcop==3.2.5`、`fcop-mcp==3.2.5`；本 WP 不修改 CodeFlowMu。
8. 不自动迁移现有工作区，不自动更新包，不自动生成全部 Host 文件。
9. 不修改冻结规范或冻结 Conformance 来迁就实现。
10. 不以“让测试变绿”为理由删除断言、增加 skip/xfail 或建立测试旁路。
11. 不通过直接堆叠 `if version` 把 v4 逻辑散入全部 v3 文件；版本分派应停留在边界。
12. 新增公共能力必须有一个明确所有者，不允许同一逻辑在 Python、MCP、规则文件各实现一次。

---

## 5. 权威与固定输入

### 5.1 事实优先级

1. 冻结规范：
   - `spec/fcop-4.0-spec.md`
   - `spec/fcop-4.0-spec.zh.md`
   - 冻结提交 `aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6`
2. 已接受 Core 代码与测试：
   - 审核 HEAD `1d94b881e38cc0b98ca41c47d25c605431d5f9a7`
   - Gate `fea48393be8c83f4dbb6e085f54bb4ce391ee2ed`
3. WP1 决策、Conformance Matrix、MCP/兼容处置表。
4. FCoP 3.2.5 代码，仅作为兼容基线。
5. 架构文章、历史 Amendment 和旧任务书，仅作解释或来源。

Schema 不能改变规范，测试不能增加规范，MCP docstring 不能覆盖规范。

### 5.2 执行起点

WP4A 实施分支必须从**包含本任务书的固定提交**创建。执行者收到任务书地址后必须：

1. `git fetch origin`；
2. 取得任务书所在 commit；
3. 验证该 commit 的父链包含：
   - `fea48393be8c83f4dbb6e085f54bb4ce391ee2ed`
   - `1d94b881e38cc0b98ca41c47d25c605431d5f9a7`
   - `aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6`；
4. 计算任务书 SHA-256，与 ADMIN 下发值一致；
5. 从该任务书 commit 建立独立 worktree。

若任一条件不满足，停止并报告 `INPUT_REF_MISMATCH`。

建议：

```text
WORKTREE: D:\FCoP-wp4a-machine-contract
BRANCH: review/fcop-4.0-wp4a-machine-contract
```

不得在原 `D:\FCoP` 工作树切换、清理、stash、reset 或吸收用户未提交文件。

---

# 6. WP4A：机器可读合同与最小 Python 使用面

## 6.1 单一目标

让 FCoP 4.0 已接受的文件协议具备一套与冻结规范一致、随 `fcop` wheel 分发、可由第三方独立验证的机器合同，并提供不依赖 CodeFlowMu、不依赖 MCP 的最小 Python 示例。

WP4A 不增加协议语义，只完成：

```text
冻结规范
→ v4 JSON Schema / registry
→ Project真实产物验证
→ wheel内可发现
→ 最小Python示例
```

## 6.2 必须先核对的真实现状

编码前必须记录：

- `spec/schemas/` 当前 8 份 Schema 的文件名、`$id`、声明版本和用途；
- 已知基线数量为 `5×v1.0.0 + 3×v1.1.0`；
- IPC Envelope 与 Review 的历史 `version/$id` 不一致；
- `spec/schemas/README.md` 当前仍称其为 FCoP v1.0 SSOT；
- `pyproject.toml` 当前只打包 `src/fcop/_data/schemas/*.schema.json`；
- v4 真实写入、读取和错误路径位于 `src/fcop/v4/**`；
- 当前公共 surface snapshot 与 v4 Conformance 119 节点。

旧 8 份 Schema 不得删除、重命名或静默改写。它们属于 3.x/历史兼容面。

若事实不同，先写 `reports/FCOP-4.0-WP4A-INPUT-DRIFT.md` 并停止。

## 6.3 机器合同边界

### 6.3.1 必须覆盖

v4 Schema 集合必须覆盖冻结规范能以 JSON Schema 表达的结构，至少包括：

- `fcop/fcop.json` 工作区声明；
- TASK；
- REPORT；
- ISSUE；
- REVIEW，包括 authorization 与 convergence 的结构化字段；
- transition event；
- Toolkit operation/recovery receipt 中被声明为稳定的持久字段。

具体文件数量由“一个稳定结构一个 Schema”的原则决定，不得为了凑数复制旧七抽象模型。

### 6.3.2 不得伪装成 Schema 可证明的内容

以下行为必须由真实代码和 Conformance 验证，不能只靠 Schema 宣称完成：

- TASK 当前状态与单一权威路径；
- 合法迁移 T1–T7；
- Profile evaluator 的 `AUTHORIZED/DENIED/UNKNOWN`；
- Authorization 是否可用、过期或已消费；
- REPORT replacement head；
- family digest 覆盖完整性；
- operation_id 并发线性化；
- crash recovery 五态；
- 文件系统支持边界。

Schema README 必须清楚写明这个界限。

### 6.3.3 标识和版本

每份 v4 Schema 必须：

- 使用 JSON Schema 2020-12；
- 具有稳定、显式含 `v4` 或 `4.0` 的 `$id`；
- 不复用 v1.x `$id`；
- 具有与内容一致的 schema revision；
- 使用绝对 `$ref` 或一个可离线确定解析的 registry；
- 不假设 `fcop.dev` 网络地址一定可访问；
- UTF-8、LF、无重复 JSON key；
- 在 wheel 与源码树中使用同一字节内容，禁止两套人工维护副本。

若必须同时保留 `spec/` 可读副本与 package data，必须建立确定性同步/生成校验；不得靠人工记忆同步。

### 6.3.4 扩展字段

Schema 只能落实冻结规范已经允许的 Core 与 Profile 扩展边界。不得自行决定：

- 把所有未知字段一律允许；
- 把所有未知字段一律禁止；
- 为兼容旧角色字段改变 v4 Core；
- 新增 `x-*` 命名规则；
- 把 `thread_key`、`risk_level` 等 Profile/Legacy 字段提升为 Core。

若冻结规范不足以唯一决定某个 `additionalProperties` 行为，停止并报告
`SCHEMA_CONTRACT_UNDERDETERMINED`，不得修改冻结规范。

## 6.4 实现要求

1. 新建隔离的 v4 Schema 目录，优先使用：
   - `spec/schemas/v4/`
   - `src/fcop/_data/schemas/v4/`
2. 提供一个小型、无网络的 registry/loader；复用现有 `jsonschema` 依赖。
3. validator 必须验证真实 `Project` 创建的字节经严格解析得到的结构，而不是测试专用字典。
4. v4 写入前验证与读取验证必须复用同一个实现，不维护两个规则表。
5. 错误必须映射到冻结的 Base Error Code；不得新增 Base Error Code。
6. 不允许添加新的公共 `Project` 方法，除非现有 surface 无法完成第三方验证；若确需新增，必须先停止并请求 `PUBLIC_API_CHANGE_REQUIRED`，不得自行扩大。
7. 示例必须调用真实公共 API，不得 import 私有测试 driver。
8. 示例必须不依赖 CodeFlowMu、MCP、网络、数据库或后台服务。

## 6.5 最小第三方 Python 示例

必须提供至少两个可运行示例：

### 示例 A：最小顺序工作

证明普通开发者可以：

1. 创建 4.0 workspace；
2. 显式采用一个测试/示例 Profile evaluator；
3. 创建 TASK；
4. claim 进入 active；
5. 写当前 attempt REPORT；
6. submit、accept、archive；
7. 重启进程式重新打开 workspace；
8. 从文件与路径读取最终状态及 transition 证据。

示例不得把测试 evaluator 描述为生产身份安全方案。

### 示例 B：最小并行 family

证明：

1. Root active 时创建两个普通 TASK Branch；
2. 两个 Branch 各自完成并产生当前 REPORT；
3. 计算 family digest；
4. 追加 convergence REVIEW；
5. 使用独立 archive authorization 完成 Root T7；
6. 不使用 Git branch/merge，不启动 Runtime。

两个示例都必须可以在临时目录运行，不能写用户主目录、仓库根或 CodeFlowMu 工作区。

## 6.6 允许修改范围

仅允许：

```text
spec/schemas/v4/**
src/fcop/_data/schemas/v4/**
src/fcop/v4/**                         # 仅 Schema loader/validator 接线
src/fcop/project.py                    # 仅必要的既有入口接线
pyproject.toml                         # 仅 package-data 收录
tests/test_fcop/**                     # v4 Schema与示例测试
examples/v4/**
docs/fcop-4.0/schema-and-python-quickstart*.md
reports/FCOP-4.0-WP4A-*.md
reviews/fcop-4.0/wp4a/MANIFEST.md
```

禁止：

```text
spec/fcop-4.0-spec*.md
tests/conformance/v4/**
mcp/**
src/fcop/rules/**
AGENTS.md
CLAUDE.md
.cursor/**
.github/workflows/**
src/fcop/_version.py
CodeFlowMu任何文件
```

## 6.7 强制测试

### A. Schema 自身

- 所有 Schema 可由 Draft 2020-12 validator 加载；
- `$id` 唯一且 registry 离线解析全部 `$ref`；
- source 与 wheel package data 字节一致；
- 重复 key、BOM、非 UTF-8、CRLF 等按冻结编码边界处理；
- 每类真实合法产物通过；
- 每个必填字段缺失、类型错误和冻结枚举错误被拒绝；
- Schema 不声称验证路径、授权或并发语义。

### B. 真实实现

- 两个示例均由测试在临时目录真实运行；
- v4 Conformance 保持 `119/119`；
- WP3E v4 unit tests 全绿；
- `tests/test_fcop` 全绿；
- v3 非-v4 回归新增失败为 0；
- public surface drift 为 0；
- MCP 回归保持全绿，尽管本轮不得修改 MCP。

### C. 构建制品

- 构建 `fcop` wheel 与 sdist；
- 解包清单证明 v4 Schema 被包含且旧 Schema 仍在；
- clean venv 从 wheel 安装；
- 在仓库外运行 Schema loader 和两个最小示例；
- 安装与运行不访问网络；
- wheel、sdist 和证据记录 SHA-256。

不得修改版本号，不得上传 PyPI。

## 6.8 GitHub CI 与交付

当前 workflow 的 push 触发只覆盖 `main` 与 `feat/**`，历史 `review/**` 分支因此可能没有 status contexts。WP4A 允许创建 Draft PR 以获得真实 `pull_request -> main` CI，但不允许合并。

交付顺序：

1. 从固定任务书 commit 创建 `review/fcop-4.0-wp4a-machine-contract`；
2. 完成实现与本地验证；
3. 创建 Content commit；
4. 创建 `reviews/fcop-4.0/wp4a/MANIFEST.md`，列出全部交付文件的 SHA-256；
5. 创建 Manifest commit；
6. push 固定 review 分支；
7. 远端重新 fetch，核对父链、HEAD 和全部哈希；
8. 创建 Draft PR，标题必须包含：
   `[DO NOT MERGE][FCoP 4.0 WP4A] Machine contract`；
9. 等待 Manifest HEAD 对应的 `test-fcop`、`test-fcop-mcp` 和 package jobs；
10. 记录每个 OS/Python job 的真实结论；
11. 不请求 reviewer，不启用 auto-merge，不合并。

若 GitHub CI 因配置或权限未运行：

- 不得修改 workflow 规避；
- 记录 `GITHUB_CI_NOT_OBSERVED`；
- 可以交付报告，但不得请求 `WP4A_MACHINE_CONTRACT_ACCEPTED`。

## 6.9 必交付文件

```text
spec/schemas/v4/**
src/fcop/_data/schemas/v4/**
examples/v4/**
docs/fcop-4.0/schema-and-python-quickstart.md
docs/fcop-4.0/schema-and-python-quickstart.zh.md
reports/FCOP-4.0-WP4A-SCHEMA-MAPPING.md
reports/FCOP-4.0-WP4A-MINIMAL-APPLICATION-PROOF.md
reports/FCOP-4.0-WP4A-PACKAGE-PROOF.md
reports/FCOP-4.0-WP4A-RESULT.md
reviews/fcop-4.0/wp4a/MANIFEST.md
```

Manifest 必须列出实际文件，而不是把通配符当作交付证明。

## 6.10 WP4A 验收条件

- [ ] 冻结规范可结构化部分到 v4 Schema 映射 100%；
- [ ] 旧 8 份 Schema 零修改；
- [ ] v4 `$id` 唯一，无 v1.x 标识复用；
- [ ] 离线 registry 可解析全部引用；
- [ ] 真实 Project 产物被验证；
- [ ] 写入与读取复用同一 validator；
- [ ] 示例 A、B 在仓库外 clean venv 运行通过；
- [ ] v4 119/119；
- [ ] v3 新回归 0；
- [ ] MCP 新回归 0；
- [ ] public surface drift 0；
- [ ] wheel/sdist 包含正确 Schema；
- [ ] 没有新依赖、后台组件、Store、状态机、锁系统或 Base Error；
- [ ] GitHub Draft PR CI 在固定 Manifest HEAD 全绿；
- [ ] 远端交付文件 SHA-256 全匹配；
- [ ] main、版本、PyPI、Release、CodeFlowMu 均未改变。

任一项不满足，不得请求 Gate。

## 6.11 回执格式

```yaml
WP4A_STATUS: COMPLETE | BLOCKED | FAILED
AUTHORIZED_SCOPE: WP4A_ONLY

TASKBOOK_COMMIT: <sha>
TASKBOOK_SHA256: <sha256>
INPUT_HEAD: fea48393be8c83f4dbb6e085f54bb4ce391ee2ed
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
EFFECTIVE_CORE_HEAD: 1d94b881e38cc0b98ca41c47d25c605431d5f9a7
WORKTREE: D:/FCoP-wp4a-machine-contract
BRANCH: review/fcop-4.0-wp4a-machine-contract

V4_SCHEMA_FILES: <n>
V4_SCHEMA_CLAUSE_MAPPING: <covered>/<applicable>
V4_SCHEMA_IDS_UNIQUE: PASS | FAIL
OFFLINE_REF_RESOLUTION: PASS | FAIL
SOURCE_PACKAGE_SCHEMA_PARITY: PASS | FAIL
LEGACY_SCHEMA_FILES_MODIFIED: 0

MINIMAL_SEQUENTIAL_APP: PASS | FAIL
MINIMAL_PARALLEL_FAMILY_APP: PASS | FAIL
CLEAN_WHEEL_INSTALL: PASS | FAIL
WHEEL_SHA256: <sha>
SDIST_SHA256: <sha>

V4_CONFORMANCE: 119/119
WP3E_V4_UNIT_TESTS: <actual>
TEST_FCOP: <actual>
V3_NEW_FAILURES: 0
MCP_REGRESSION: <actual>
PUBLIC_SURFACE_DRIFT: 0
UNEXPECTED_FAILURES: 0

NEW_PUBLIC_APIS: 0
NEW_RUNTIME_DEPENDENCIES: 0
NEW_BACKGROUND_COMPONENTS: 0
NEW_AUTHORITATIVE_STORES: 0
NEW_STATE_MACHINES: 0
NEW_LOCK_SYSTEMS: 0
NEW_BASE_ERROR_CODES: 0
FROZEN_SPEC_FILES_MODIFIED: 0
FROZEN_CONFORMANCE_FILES_MODIFIED: 0
MCP_FILES_MODIFIED: 0
RULE_PACKAGE_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0

CONTENT_COMMIT: <sha>
MANIFEST_COMMIT: <sha>
REMOTE_HEAD: <sha>
REMOTE_PUSHED: true
REMOTE_REFETCH_VERIFIED: PASS
DELIVERY_SHA256: <matched>/<total>
DRAFT_PR_URL: <url>
GITHUB_CI_AT_MANIFEST_HEAD: PASS
MAIN_MODIFIED: false
RELEASE_CREATED: false
WP4B_STARTED: false

REQUESTED_GATE: WP4A_MACHINE_CONTRACT_ACCEPTED
```

完成后停止。

---

# 7. 后续阶段的非执行性合同

## 7.1 WP4B：MCP 薄适配

只有 `WP4A_MACHINE_CONTRACT_ACCEPTED` 后才能另发任务书。

必须完成：

- 在一个边界识别 workspace 3.x/4.0；
- 维持 canonical 45 个名称，不吸收 CodeFlowMu 静态 catalog 的 `close_issue`；
- 45/45 工具逐项落实 `CORE_MAPPING / TOOLKIT / PROFILE / LEGACY_V3_ONLY / OPTIONAL_EXTENSION`；
- 11 static resources 与 3 templates 逐项版本绑定；
- `fcop://spec` 不再把 v1.1 快照冒充当前规范；
- `finish_task`、history 深归档在 v4 workspace 明确拒绝；
- v4 写操作调用同一个 `Project` 实现，不复制生命周期、授权、幂等或恢复逻辑；
- stdio 是基础 MCP；Relay 从基础依赖移到可选 `fcop-mcp[relay]`；
- `fcop-mcp` 与 `fcop` 版本组合 Fail Closed；
- 普通开发者仅安装 `fcop-mcp` 即可使用，不依赖 CodeFlowMu。

WP4B 不处理规则大文件，也不发布。

## 7.2 WP4C：模块化规则包与 Host 薄入口

只有 `WP4B_MCP_ADAPTER_ACCEPTED` 后才能另发任务书。

必须吸收旧规则包草案的有效方向：

```text
冻结4.0合同
→ 全新Core Guidance与分类模块
→ Distribution Manifest
→ ADMIN明确采用的Host薄投影
```

必须满足：

- 不以 3.x 大文件作为 4.0 正文基底；
- 正向覆盖：冻结 4.0 条款 → 唯一模块 = 100%；
- 反向审计：3.x active rule → retained/superseded/obsolete/commentary/conflict = 100%；
- 根 `AGENTS.md`、`CLAUDE.md`、Cursor `.mdc` 不再成为独立规则源；
- 新规则只能修改对应 canonical module；
- Host 文件存在、生成能力、ADMIN adoption、模型选择、真实 Host 消费是四种不同事实；
- Codex、Cursor、Claude Code 等只按已采用 Host profile 生成；
- 《Agent 原生软件工程宪法》只强制用于开发 FCoP 本体的 Agent，不注入普通 FCoP 业务 Agent；
- FCoP 开发手册不进入普通下游包；
- CodeFlowMu 只做只读兼容 shadow，固定 3.2.5；
- 不新增远程规则服务、自动更新器或运行时规则热切换。

## 7.3 WP4D：RC 与第三方采用证明

只有 `WP4C_RULE_DISTRIBUTION_ACCEPTED` 后才能另发任务书。

至少验证：

- `fcop` 与 `fcop-mcp` 构建制品组合；
- Windows、Linux、macOS 和 Python 3.10–3.13；
- Python-only 最小项目；
- MCP-only 最小项目；
- 一层并发 Branch 与显式汇合；
- 崩溃恢复与响应丢失重试；
- 3.2.5 工作区不迁移、不漂移；
- 4.0 新工作区显式创建；
- Host 规则发现、缺失、摘要冲突、上下文超限与回滚；
- CodeFlowMu 固定 3.2.5 shadow；
- 相同 artifact 贯穿 clean-room、GitHub Release candidate 与后续发布批准。

WP4D 只形成 RC 候选，不自动授权 main merge、PyPI 或正式 Release。

---

## 8. 独立的后续 Gate

以下决定互不替代：

```yaml
WP4A_MACHINE_CONTRACT_ACCEPTED: false
WP4B_MCP_ADAPTER_ACCEPTED: false
WP4C_RULE_DISTRIBUTION_ACCEPTED: false
FCOP_4_RC_ACCEPTED: false
MAIN_MERGE_AUTHORIZED: false
RELEASE_AUTHORIZED: false
PYPI_PUBLISH_AUTHORIZED: false
CODEFLOWMU_ADOPTION_AUTHORIZED: false
```

任何一个较早 Gate 通过，都不能推导后面的 Gate 自动通过。

---

## 9. 最终完成定义

FCoP 4.0 只有满足以下链条，才可以进入独立发布裁决：

```text
Core实现已接受
+ 机器合同与Python最小应用通过
+ MCP薄适配与45/11/3版本分派通过
+ 模块规则包与Host投影通过
+ 跨平台制品与第三方最小项目通过
= FCoP 4.0 RC候选
```

即使 RC 通过，也仍需 ADMIN 单独决定主线合并和正式发布。
