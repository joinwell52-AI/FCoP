---
stage: WP4A
document_role: BLOCKER_REPORT
status: BLOCKED
authorized_scope: WP4A_ONLY
blocker: SCHEMA_CONTRACT_UNDERDETERMINED
gate_self_signed: false
requested_gate: NONE
---

# FCoP 4.0 WP4A · Schema 合同未唯一化阻断报告

## 1. 正式结论

```yaml
WP4A_STATUS: BLOCKED
BLOCKER: SCHEMA_CONTRACT_UNDERDETERMINED
BLOCKING_SECTION: 6.3.4
IMPLEMENTATION_STARTED: false
SCHEMA_FILES_WRITTEN: 0
PRODUCTION_FILES_MODIFIED: 0
TEST_FILES_MODIFIED: 0
DRAFT_PR_CREATED: false
GITHUB_CI_REQUESTED: false
WP4A_MACHINE_CONTRACT_ACCEPTED_REQUESTED: false
```

WP4A 任务书要求 v4 Schema 对冻结 Core 与 Profile 扩展边界作机器表达，同时
明确禁止执行者自行选择“所有未知字段允许”“所有未知字段禁止”或新建 `x-*`
命名规则。冻结合同没有唯一规定 Profile 扩展的字段载体、命名空间、注册方式及
未知字段处置，因此无法在不增加协议语义的前提下确定根对象的
`additionalProperties`/`unevaluatedProperties` 合同。任务书 6.3.4 明确要求
在此情形报告 `SCHEMA_CONTRACT_UNDERDETERMINED` 并停止。

## 2. 固定输入核验

| 核验项 | 真实结果 |
|---|---|
| Taskbook commit | `a789cf070cfc626d23034753b18e8679780b7d50` |
| Taskbook SHA-256 | `f0b31843643216fd7c9448c0041fedaac7f904cd3e270425fb8dd50db11ed2d4`，PASS |
| Taskbook 直接父提交 | `fea48393be8c83f4dbb6e085f54bb4ce391ee2ed`，PASS |
| Effective Core 祖先 | `1d94b881e38cc0b98ca41c47d25c605431d5f9a7`，PASS |
| Frozen Contract 祖先 | `aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6`，PASS |
| 独立 worktree | `D:/FCoP-wp4a-machine-contract`，PASS |
| 固定执行分支 | `review/fcop-4.0-wp4a-machine-contract`，PASS |
| 原 `D:/FCoP` 脏现场 | 未清理、未切换、未 stash、未 reset，PASS |
| remote main | `68dbeb15f4e7f84e1d03f907be9fa66c2265843e`，未修改 |

## 3. 任务书 6.2 现状审计

输入事实全部符合任务书，不属于 `INPUT_DRIFT`：

1. `spec/schemas/` 有 8 份旧 Schema：
   `agent`、`boundary`、`encoding`、`event`、`failure`、`ipc-envelope`、
   `review`、`skill`。
2. 声明版本为 5 份 `1.0.0` 与 3 份 `1.1.0`。
3. `ipc-envelope.schema.json` 与 `review.schema.json` 均声明
   `version: 1.1.0`，但 `$id` 仍为 `/v1.0.json`；`skill` 的 1.1.0 与
   `/v1.1.json` 一致。
4. `spec/schemas/README.md` 仍把旧集合称为 FCoP v1.0 SSOT，并说明 IPC
   根对象使用 `additionalProperties: true` 保持 0.7.x 兼容。
5. `pyproject.toml` 仅收录
   `src/fcop/_data/schemas/*.schema.json`，未递归收录 v4 子目录。
6. v4 真实创建、读取、编码、授权、收敛与恢复实现位于
   `src/fcop/v4/**`，公共版本边界位于 `src/fcop/project.py`。
7. `tests/conformance/v4 --collect-only` 实际收集 119 个节点。

## 4. 冻结合同留下的精确空白

### 4.1 Workspace declaration

F4.2.1 使用“contains at least”，因此不能推出根对象必须封闭。F4.2.3 又明确
允许 team、role、leader 及“similar fields”作为 Profile 扩展保留，但没有定义：

- 扩展是根级字段、统一 `extensions` 容器，还是按 Profile ID 分区；
- 合法扩展字段的名称、类型、注册来源或离线解析方式；
- 未采用 Profile 的未知字段应拒绝、保留还是忽略；
- Profile 字段与 Core 字段碰撞时的机器判定规则。

### 4.2 Four envelopes

F4.3.2 冻结共同必填字段、类型必填字段和可选 Core 字段，但没有规定未列出的
根级 frontmatter key 是否有效。F4.5.5 只说明 `thread_key` 属于
Profile/Legacy 且不改变 Core 关系，没有规定其 Schema 载体，也没有给出
Profile 扩展的穷举集合。

F4.8.4 把 Profile 扩展排除在 create digest 之外，只决定幂等摘要输入，不能
推导哪些扩展字段可持久化或 Schema 应如何识别它们。F4.10.3 只要求 Profile /
Toolkit **错误码**使用明确命名空间，不能作为数据字段命名规则。

### 4.3 WP1 冲突裁决不足以补齐该点

WP0 冲突 #4 明确要求 WP1 唯一化“四类正式文件的最小必填字段和未知字段兼容
策略”。WP1 决策 #4 冻结了四类 envelope、共同/类型字段与 append-only 规则，
但没有给出未知字段兼容策略或 `additionalProperties` 行为。执行者不能把这项
遗漏用实现偏好补齐。

## 5. 为什么所有可选实现都越权

| Schema 选择 | 实际语义 | 越权原因 |
|---|---|---|
| 省略 `additionalProperties` | Draft 2020-12 默认允许全部未知字段 | 等价于任务书禁止的“所有未知字段一律允许” |
| `additionalProperties: true` | 明确允许全部未知字段 | 同上，并会把拼写错误与未采用扩展一并接受 |
| `additionalProperties: false` | 拒绝所有未列字段 | 违反 F4.2.3 允许 Profile 扩展保留的边界 |
| 穷举 team/role/leader/thread_key 等 | 把例示集合当成封闭集合 | “similar fields”并非穷举，且字段类型未冻结 |
| 新建 `x-*`、`profile:*` 或扩展容器 | 创建新字段协议与命名空间 | 任务书明确禁止自行新增该规则 |
| 只投影 Core 子集后再校验 | 不对真实解析后的完整 Project 产物校验 | 违反 6.4.3 的真实产物要求，并隐藏未知字段决定 |

## 6. 当前实现不能替代规范决定

`src/fcop/v4/creation.py::_manifest()` 验证必填身份后返回原 dict；
`_Creation._validate()` 验证四类 envelope 的必填结构但不要求字段集合完全相等。
这说明当前读取实现可以保留额外字段。相反，业务写入口 `_request()` 又使用
显式 allowlist 拒绝未知调用参数；生命周期 receipt 则在
`src/fcop/v4/receipts.py::validate_receipt()` 中要求精确字段集合。

这些差异是各对象当前实现事实，不是冻结 Schema 的未知字段总规则。F4.0.3 与
任务书均禁止用当前实现反向增加规范。直接照抄任一现状会使 Schema 获得未被
冻结合同授予的机器权威。

## 7. 阻断影响与所需裁决

在 ADMIN/合同维护者补齐以下最小决定前，无法合法开始 WP4A：

1. 分别确定 workspace、TASK、REPORT、ISSUE、REVIEW 的扩展载体；
2. 规定每类根对象对未识别字段的 accept/reject/preserve 行为；
3. 规定扩展的离线注册或命名空间，以及与 Core 字段的碰撞规则；
4. 明确 `thread_key`、team/role/leader 等例示字段是否有稳定机器结构；
5. 明确上述扩展在写入、读取及 create digest 排除中的一致处理。

裁决必须来自新的固定合同修正或 ADMIN 固定任务书，不能由 WP4A 执行者自行
选择。因为 Schema 根对象边界尚未唯一，Schema 映射、共享 validator 接线、
示例、wheel/sdist 证明和固定 Manifest HEAD CI 均不得继续。

## 8. 停止回执

```yaml
WP4A_STATUS: BLOCKED
AUTHORIZED_SCOPE: WP4A_ONLY
BLOCKER: SCHEMA_CONTRACT_UNDERDETERMINED
INPUT_REF_MISMATCH: false
INPUT_DRIFT: false

V4_SCHEMA_FILES: 0
V4_SCHEMA_CLAUSE_MAPPING: NOT_STARTED
LEGACY_SCHEMA_FILES_MODIFIED: 0
PRODUCTION_FILES_MODIFIED: 0
TEST_FILES_MODIFIED: 0
FROZEN_SPEC_FILES_MODIFIED: 0
FROZEN_CONFORMANCE_FILES_MODIFIED: 0
MCP_FILES_MODIFIED: 0
RULE_PACKAGE_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0

CONTENT_COMMIT: NOT_CREATED
MANIFEST_COMMIT: NOT_CREATED
BLOCKER_REPORT_COMMIT: SELF
COMMIT_REACHABILITY: LOCAL_ONLY
REMOTE_PUSHED: false
DRAFT_PR_URL: NOT_CREATED
GITHUB_CI_AT_MANIFEST_HEAD: NOT_RUN
MAIN_MODIFIED: false
RELEASE_CREATED: false
WP4B_STARTED: false

WP4A_MACHINE_CONTRACT_ACCEPTED: false
REQUESTED_GATE: NONE
NEXT_REQUIRED_ACTION: FREEZE_PROFILE_EXTENSION_AND_UNKNOWN_FIELD_SCHEMA_POLICY
```
