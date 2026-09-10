---
title: "FCoP 4.0 WP4A.1：Profile 扩展 Schema 策略裁决与 WP4A 恢复任务书"
version: "1.0"
date: "2026-09-06"
document_role: "AUTHORIZED_CORRECTION_AND_RESUME_TASKBOOK"
authority: "ADMIN"
repository: "joinwell52-AI/FCoP"
program: "FCOP_4_0"
work_package: "WP4A.1"
parent_taskbook_commit: "a789cf070cfc626d23034753b18e8679780b7d50"
parent_gate_commit: "fea48393be8c83f4dbb6e085f54bb4ce391ee2ed"
effective_core_head: "1d94b881e38cc0b98ca41c47d25c605431d5f9a7"
frozen_contract_commit: "aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6"
blocker: "SCHEMA_CONTRACT_UNDERDETERMINED"
blocker_disposition: "RESOLVED_BY_ADMIN_SCHEMA_BINDING"
execution_authorized: true
authorized_scope: "WP4A_1_ONLY"
resumes_full_wp4a: true
wp4b_started: false
main_merge_authorized: false
release_authorized: false
pypi_publish_authorized: false
codeflowmu_change_authorized: false
---

# FCoP 4.0 WP4A.1：Profile 扩展 Schema 策略裁决与 WP4A 恢复任务书

## 0. ADMIN 裁决

WP4A 在未修改代码的情况下以
`SCHEMA_CONTRACT_UNDERDETERMINED` 停止是正确行为。

阻断问题为：冻结合同允许 Profile 扩展，但没有把未知字段在 Base JSON Schema 中应如何处理写成唯一机械策略。执行者不得自行选择 `additionalProperties: true`、`false`、新增 `x-*` 命名规则或创建新的 `extensions` 容器。

ADMIN 现固定以下 Schema Binding：

```yaml
BASE_SCHEMA_ROOT_POLICY: OPEN_FOR_OPAQUE_PROFILE_FIELDS
OPEN_EXTENSION_POINTS:
  - fcop/fcop.json object root
  - TASK frontmatter object root
  - REPORT frontmatter object root
  - ISSUE frontmatter object root
  - REVIEW frontmatter object root
CORE_NESTED_OBJECT_POLICY: CLOSED_UNLESS_FROZEN_SPEC_EXPLICITLY_ALLOWS_EXTENSION
UNKNOWN_ROOT_FIELD_CORE_SEMANTICS: NONE
UNKNOWN_ROOT_FIELD_CAN_SATISFY_CORE_REQUIRED_FIELD: false
UNKNOWN_ROOT_FIELD_CAN_CHANGE_CORE_GATE: false
UNKNOWN_ROOT_FIELD_CAN_CHANGE_CORE_DIGEST: false
UNKNOWN_ROOT_FIELD_CAN_OVERRIDE_RESERVED_FIELD: false
NEW_X_PREFIX_RULE: false
NEW_EXTENSIONS_CONTAINER: false
PROFILE_REGISTRY_PROTOCOL_ADDED: false
```

这是一项 Schema 表达裁决，不修改冻结 Core，不新增第五类信封、不新增生命周期、不新增 Profile Runtime。

本任务书同时恢复原 WP4A 的完整授权。执行者无需再等待一份“恢复 WP4A”任务书。完成全部 WP4A 目标后请求原 Gate：

```yaml
GATE: WP4A_MACHINE_CONTRACT_ACCEPTED
```

WP4B、WP4C、WP4D 仍未授权。

---

## 1. 权威输入

必须读取并验证：

1. WP4 总任务书：
   `a789cf070cfc626d23034753b18e8679780b7d50`
2. Core Gate：
   `fea48393be8c83f4dbb6e085f54bb4ce391ee2ed`
3. Effective Core HEAD：
   `1d94b881e38cc0b98ca41c47d25c605431d5f9a7`
4. Frozen Contract：
   `aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6`
5. 本任务书所在固定提交及其 SHA-256。

本任务书只替换 WP4 总任务书第 6.3.4 节的不确定部分。原任务书其余范围、禁止项、测试、GitHub Draft PR、交付与停止要求继续全部生效。

---

## 2. Base Schema 与 Profile Schema 的分层

### 2.1 Base Schema 负责什么

Base Schema 只验证冻结 FCoP 4.0 Core 已定义的结构：

- 必填字段存在；
- 已知字段类型正确；
- 已知枚举正确；
- Core 内嵌对象结构正确；
- ID、时间、摘要和数组等可由 Schema 表达的格式正确。

Base Schema 不判断：

- 某个 Profile ID 是否已安装；
- Profile evaluator 是否可用；
- 签发者是否 `AUTHORIZED`；
- 未知扩展字段的业务含义；
- 文件路径是否是唯一 NOW；
- lifecycle、family、幂等或恢复行为是否成立。

这些继续由真实实现、Profile evaluator 与 Conformance 验证。

### 2.2 为什么根对象开放

冻结合同 F4.2.3 允许 v3 团队、角色等字段作为 Profile 扩展继续存在；F4.8.4 又明确 Profile 扩展不进入 create-task Core digest。

因此 Base Schema 必须允许工作区声明根和四类信封 frontmatter 根携带它不认识的 Profile 字段。允许解析不代表：

- FCoP Core 理解该字段；
- 该字段获得协议地位；
- 该字段可以授予权限；
- 该字段可以改变 Gate；
- 该字段可以替代正式字段；
- 所有实现都必须执行该字段。

未知根字段的唯一 Base 含义是：

> 可被保存和交给已采用的 Profile 层解释；Core 对其不作语义承诺。

### 2.3 为什么内嵌 Core 对象封闭

以下冻结结构必须拒绝未知成员，除非规范已明确允许扩展：

- `encoding`；
- transition 对象；
- authorization transition binding；
- receipt 中固定阶段和路径/摘要结构；
- family digest canonical object；
- 其他由冻结规范列出完整字段集合的 Core 子对象。

开放根对象不能扩散为“所有层级任意字段都接受”。否则拼写错误可能被当成无害扩展，削弱 Fail Closed。

### 2.4 Profile 专用验证

Base 包本轮不创建通用 Profile 注册协议，也不要求第三方 Profile 进入 FCoP Core Schema 目录。

Profile 可以提供自己的 Schema 或 evaluator，并采用分层验证：

```text
Base Schema
→ 已采用 Profile 自己的 Schema/evaluator
→ Core operation gate
```

Profile 层可以对它拥有的字段进一步要求、限制或拒绝，但不得：

- 放宽 Base 必填字段；
-改变 Base 字段类型；
- 重定义 Base 枚举；
- 覆盖 Base ID、workspace identity、路径状态或摘要；
- 把未知 Profile 字段直接解释为 Core Authorization。

Profile 不可用时，Base Schema 仍可完成结构读取；需要授权的 T4–T7 继续按冻结合同返回
`AUTHORIZATION_PROFILE_UNAVAILABLE` 或相应稳定错误。

---

## 3. 字段冲突与保留规则

### 3.1 不新增命名规范

FCoP 4.0 Base 本轮不新增：

- `x-*` 强制前缀；
- `extensions: {}` 容器；
- vendor namespace registry；
- 在线 Profile registry；
- 新的 Profile manifest 文件。

这些若未来需要，属于后续规范演进，不得借 Schema 实现偷偷加入。

### 3.2 重复与覆盖

- JSON/YAML 重复 key 必须在 Schema 前的严格解析阶段拒绝；
- 未知字段不能与一个已知 Base 字段“并存覆盖”，重复 key 直接失败；
- 大小写近似字段不替代 Base 字段；
- 未知字段不能满足缺失的 `protocol`、`version`、`type`、ID、`workspace_id` 等必填项；
- 已知字段存在但类型错误时，不能因为另有扩展字段而通过。

### 3.3 已知 Legacy/Profile 字段

`thread_key`、`risk_level`、团队和角色等字段：

- 若冻结规范已把它们列为 Profile/Legacy 字段，Base Schema 可以将其视为已知的非 Core 字段或普通未知根字段；
- 不得把它们提升为 Core；
- 不得加入 F4.8.4 create-task digest；
- 不得用它们改变 T1–T7、Authorization、family digest 或 recovery；
- 不要求 WP4A 为它们建立新的公共写入 API。

---

## 4. 写入、读取与持久化行为

1. v4 公共 API 只写它明确接受的字段；根对象开放不等于新增任意 kwargs API。
2. WP4A.1 不新增公共 `Project` 方法。
3. 生命周期移动现有信封时，不得因为 Base Schema 不理解扩展字段而删除或重写这些字段。
4. 若当前实现对扩展字段只能保持语义值、不能保证原始 YAML 排版字节不变，不得虚报 byte-preserving；transition 的正式证据摘要仍按冻结实现处理。
5. Core canonical digest 只使用冻结规范列出的字段。未知 Profile 字段不得自动进入：
   - create-task normalized request digest；
   - family digest；
   - authorization digest 以外的推导输入。
6. 对完整文件做证据摘要时，仍按冻结合同对完整文件字节计算；“扩展字段不进入 canonical request digest”不等于从文件 evidence digest 删除它。

第 5、6 项必须分别测试，不能混为一种摘要。

---

## 5. 必增测试

除原 WP4A 全部测试外，至少增加以下真实测试。

### SB-01 Base 根扩展接受

为 workspace、TASK、REPORT、ISSUE、REVIEW 各加入一个未知根字段，Base Schema 结构验证通过。

### SB-02 必填字段不可替代

删除每类对象的一个 Core 必填字段，同时加入名称近似扩展字段，必须失败。

### SB-03 已知字段类型不可覆盖

将已知 Base 字段改为错误类型，同时加入其他扩展字段，必须失败。

### SB-04 Core 子对象封闭

向 `encoding`、transition binding 等完整定义的 Core 子对象加入未知成员，必须失败。

### SB-05 重复 key 在 Schema 前失败

对 JSON 与 YAML frontmatter 的重复 key，严格 parser 必须拒绝；不得由“根对象开放”放过。

### SB-06 Core Gate 不读取未知字段

未知根字段不得改变 T1–T7 的结果、Profile 三态、Authorization 绑定或 family coverage。

### SB-07 create-task digest 不漂移

同一正式 F4.8.4 请求在仅 Profile 扩展上下文不同的情况下，Core request digest 不得变化。若公共 API 当前不接收扩展字段，只测试真实可达边界，不得新增测试专用参数。

### SB-08 完整文件 evidence digest 仍覆盖扩展字段

当一个已落盘正式证据文件的扩展字段字节改变时，完整文件 evidence digest 必须变化，既有绑定不得继续匹配。

### SB-09 Profile 层可收紧但不可放宽 Base

用局部测试 Profile 证明它可以拒绝自己的扩展字段，但不能让缺失/错误的 Base 字段通过。

### SB-10 v3 隔离

旧 8 份 Schema 和 v3 工作区行为保持不变；不得把本裁决反向写入 v1.x Schema。

---

## 6. 执行方式

### 6.1 工作树

原 `D:\FCoP-wp4a-machine-contract` 已有本地-only blocker commit。不得 reset、删除或覆盖它。

新建独立 worktree：

```text
WORKTREE: D:\FCoP-wp4a1-machine-contract
BRANCH: review/fcop-4.0-wp4a.1-machine-contract
START_POINT: 本任务书固定提交
```

原本地 blocker 报告应作为历史证据复制进新分支：

```text
reports/FCOP-4.0-WP4A-SCHEMA-CONTRACT-UNDERDETERMINED.md
```

复制前记录原文件 SHA-256；不得 cherry-pick 未推送的 blocker commit，也不得把该 local-only commit 当权威父提交。

### 6.2 实施范围

执行原 WP4A 的全部第 6 节，并使用本任务书第 2–5 节作为唯一 Schema 扩展策略。

仍只允许原 WP4A allowlist。额外允许新增：

```text
reports/FCOP-4.0-WP4A.1-SCHEMA-BINDING.md
reviews/fcop-4.0/wp4a.1/MANIFEST.md
```

不得修改冻结规范、冻结 Conformance、MCP、规则包、Host 入口、workflow、版本或 CodeFlowMu。

### 6.3 不得扩大为新系统

不得增加：

- Profile registry 服务；
- extension registry；
- schema server；
- 网络下载；
- background validator；
- schema cache 一致性层；
-数据库或索引；
- 第二套 Project；
- 动态插件加载框架。

离线 Schema registry 只能是小型、确定性的 package-data loader。

---

## 7. GitHub 交付与 CI

继续执行原 WP4A 两提交交付规则：

1. Content commit；
2. Manifest commit；
3. push `review/fcop-4.0-wp4a.1-machine-contract`；
4. 远端回读全部文件并核验 SHA-256；
5. 创建 Draft PR 到 `main`：
   `[DO NOT MERGE][FCoP 4.0 WP4A.1] Machine contract`；
6. 等待 Manifest HEAD 的真实 GitHub CI；
7. 不请求 reviewer、不启用 auto-merge、不合并。

CI 未运行或未全绿时，不得请求 Gate。不得修改 workflow 规避。

---

## 8. 验收条件

除原 WP4A 第 6.10 节全部条件外，新增：

- [ ] SB-01 至 SB-10 全部通过；
- [ ] 开放点仅限五个声明的根对象；
- [ ] 完整定义的 Core 子对象保持封闭；
- [ ] 未新增 `x-*` 或 `extensions` 规范；
- [ ] 未新增 Profile registry 协议；
- [ ] 未知字段对 Core gate 语义为 NONE；
- [ ] canonical request digest 与完整文件 evidence digest 的边界分别正确；
- [ ] 原 blocker 报告被保留并标记为已由 ADMIN 裁决；
- [ ] 原 local-only blocker commit 未进入父链；
- [ ] WP4A 全部机器合同、示例、制品和跨平台 CI 条件完成。

完成后请求：

```yaml
GATE: WP4A_MACHINE_CONTRACT_ACCEPTED
```

---

## 9. 回执格式

```yaml
WP4A_1_STATUS: COMPLETE | BLOCKED | FAILED
AUTHORIZED_SCOPE: WP4A_1_ONLY
RESUMED_SCOPE: FULL_WP4A

TASKBOOK_COMMIT: <sha>
TASKBOOK_SHA256: <sha256>
PARENT_TASKBOOK_COMMIT: a789cf070cfc626d23034753b18e8679780b7d50
INPUT_HEAD: fea48393be8c83f4dbb6e085f54bb4ce391ee2ed
EFFECTIVE_CORE_HEAD: 1d94b881e38cc0b98ca41c47d25c605431d5f9a7
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6

SCHEMA_BINDING_POLICY: PASS | FAIL
OPEN_ROOT_EXTENSION_POINTS: 5/5
CLOSED_CORE_NESTED_OBJECTS: PASS | FAIL
UNKNOWN_ROOT_FIELD_CORE_SEMANTICS: NONE
NEW_X_PREFIX_RULE: false
NEW_EXTENSIONS_CONTAINER: false
PROFILE_REGISTRY_PROTOCOL_ADDED: false
SCHEMA_BINDING_TESTS: 10/10

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

BLOCKER_REPORT_PRESERVED: true
BLOCKER_LOCAL_COMMIT_IN_PARENT_CHAIN: false
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

完成后强制停止。
