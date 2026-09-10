---
document_role: ADMIN_SCOPE_DECISION_AND_EXECUTION_TASKBOOK
title: FCoP 4.0 WP4B.3 公共授权事实追加边界与 WP4B 恢复任务书
version: 1.0
status: AUTHORIZED_FOR_WP4B_RESUME_ONLY
execution_authorized: true
authorized_scope: WP4B_RESUME_ONLY
stop_code_resolved: MCP_AUTHORIZATION_APPEND_VALIDATION_UNAVAILABLE
input_head: f98027dd3d7f4bbae5d3d7f3d0ed733afc9ffc05
resumes_taskbook_commit: ed8212cefeccf2e0d2a49b8802386758fd17475a
frozen_contract_commit: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
main_merge_authorized: false
release_authorized: false
wp4c_authorized: false
codeflowmu_change_authorized: false
---

# FCoP 4.0 WP4B.3：公共授权事实追加边界与 WP4B 恢复任务书

## 0. ADMIN 裁决

ADMIN 接受提交 `f98027dd3d7f4bbae5d3d7f3d0ed733afc9ffc05` 中记录的阻断及其真实入口复现：

```yaml
BLOCKED_REPORT_ACCEPTED: true
STOP_CODE: MCP_AUTHORIZATION_APPEND_VALIDATION_UNAVAILABLE
TRANSITION_AUTHORIZATION_BYPASS_FOUND: false
PUBLIC_AUTHORIZATION_APPEND_VALIDATION: MISSING
```

冻结合同与 WP1 disposition 要求 `mark_human_approved` 在 v4 中：

1. 不得修改旧 REVIEW；
2. 只能追加一个完整绑定的 `review_kind: authorization` REVIEW；
3. 使用 Project 初始化时注册的可信 Profile evaluator；
4. evaluator 返回 `DENIED`、`UNKNOWN` 或发生异常时，必须在发布前拒绝；
5. 绑定不足、Profile 不可用或过期时不得追加；
6. 写授权事实不等于消费授权，不得移动 TASK。

正式裁决：补齐现有 v4 `Project.mark_human_approved` 的公共授权事实追加边界。MCP 只调用该现有公共方法，不得自行判断 Profile、不得调用私有 `validate_gate`、不得先写后试迁移再回滚。

```yaml
V4_PUBLIC_METHOD_COMPLETED: Project.mark_human_approved
NEW_PUBLIC_METHOD_NAMES: 0
GENERAL_WRITE_REVIEW_SEMANTICS_CHANGED: false
NEW_CORE_RULES: 0
NEW_BASE_ERROR_CODES: 0
```

完成本边界及定向测试后，允许继续完成整个 WP4B，无需等待中间 Gate。

## 1. 权威输入

按以下优先级执行：

1. 冻结规范 `spec/fcop-4.0-spec.md`、`spec/fcop-4.0-spec.zh.md`，提交 `aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6`；
2. WP1 `reports/FCOP-4.0-WP1-COMPATIBILITY-AND-MCP.md` 中 `mark_human_approved` 与 `write_review` disposition；
3. 本 WP4B.3 裁决；
4. WP4B.2a，提交 `ed8212cefeccf2e0d2a49b8802386758fd17475a`；
5. WP4B.2、WP4B.1、WP4B.0 与原 WP4B 任务书；
6. 当前阻断报告，提交 `f98027dd3d7f4bbae5d3d7f3d0ed733afc9ffc05`。

本文件只补齐已冻结行为所需的公共实现边界，不修改冻结合同或 Schema 语义。

## 2. 两个阶段必须分开

### 2.1 追加授权事实

`Project.mark_human_approved` 负责：

```text
解析旧 REVIEW
→ 构造完整 authorization REVIEW 候选
→ 验证 subject/attempt/transition/time/Profile/issuer proof
→ 可信 evaluator 返回 AUTHORIZED
→ 原子追加新 REVIEW
```

它不得移动 TASK、消费授权、生成新 attempt 或追加 transition event。

### 2.2 消费授权

T4–T7 的 `Project.transition` 仍负责：

```text
重新读取授权 REVIEW
→ 重新核验字节摘要、绑定、时效、Profile 与 issuer proof
→ 检查单次消费
→ 提交一条生命周期迁移
```

追加时通过不保证以后一定可以消费。若 Profile evaluator 的判断、证据字节、TASK 状态或时效在消费前改变，transition 必须继续 Fail Closed。

禁止把“追加时已验证”作为跳过 T4–T7 验证的缓存或凭证。

## 3. 唯一可信判断实现

允许在 `src/fcop/v4/authorization.py` 中抽取一个职责单一的内部 helper，供以下两个生产入口共用：

```text
Project.mark_human_approved append path
Project.transition T4–T7 consumption path
```

共享范围至少包括：

- `profile_ref` 已被 workspace manifest 采用；
- evaluator 来自 Project 初始化时的不可变 `trusted_profiles`；
- caller 请求中没有 evaluator、policy、registry 或预判结果；
- `issuer_proof` 存在；
- evaluator 只接收协议固定的 `profile_ref`、issuer、proof；
- 只有精确返回 `AUTHORIZED` 才通过；
- `DENIED`、`UNKNOWN`、其他值或 evaluator 异常均 Fail Closed。

不得在 MCP、`creation.py` 与 `authorization.py` 各复制一份相似判断。允许保留组装候选 REVIEW 与消费 transition 各自特有的验证。

## 4. v4 公共方法合同

### 4.1 复用已有方法

只允许完成现有名称：

```text
Project.mark_human_approved
```

不新增 `write_authorization`、`append_authorization`、`approve_authorization` 或其他公共同义方法。内部私有 helper 不计作公共 API。

v3 `Project.mark_human_approved` 的签名、原地兼容行为、返回类型与既有测试不得改变。v4 实例可通过现有 version boundary 提供独立的关键词参数合同；不得让 v4 签名污染 v3 反射面。

### 4.2 v4 正式请求字段

v4 公共方法与 MCP 投影必须能表达下列信息：

| 字段 | 要求 | 规则 |
|---|---:|---|
| `review_id` | 必填 | 被人工确认的旧 REVIEW；新事实必须引用它 |
| `approver` | 必填 | authorization REVIEW 的 issuer/sender；不是独立权限证明 |
| `decision` | 必填 | v4 只接受明确的肯定决定；保存时规范化为 `authorize` |
| `profile_ref` | 必填 | 已采用且在可信初始化边界注册的 Profile |
| `from_stage` | 必填 | 被授权迁移的源状态 |
| `to_stage` | 必填 | 被授权迁移的目标状态 |
| `attempt_id` | 按边要求 | 与旧 REVIEW、TASK 当前轮次及目标 edge 一致；允许冻结合同规定的 null 情形 |
| `family_digest` | 按边要求 | Root T7 等合同要求时必填；其他情形按冻结合同为 null/缺省 |
| `issued_at` | 必填 | 有时区的 date-time |
| `expires_at` | 必填可为 null | 非 null 时必须不早于 issued_at，发布点不得已过期 |
| `issuer_proof` | 必填 | 仅交给可信 Profile evaluator 判断 |
| `comment` | 可选 | 人类说明正文，不参与权限替代判断 |

适配器可将 `from_stage`、`to_stage` 组装为冻结 Encoding 的：

```yaml
transition:
  from: <from_stage>
  to: <to_stage>
```

下列字段由公共方法固定或从可信现有事实派生，不由调用者自由改写：

```yaml
review_kind: authorization
stored_decision: authorize
operation_kind: lifecycle_transition
authorization_scope: single_use
subject_ref: old REVIEW 的 subject_ref
references: [review_id]
recipient: old REVIEW 的 recipient 或现有规范化目标
workspace_id: bound Project manifest
```

如果原 WP4B 已为同一语义采用等价字段名，可保持向后兼容的 MCP 拼写，但生产 Project 候选必须落为上述冻结字段。

### 4.3 决定值

v4 `mark_human_approved` 是肯定授权入口。允许兼容现有肯定拼写 `approve`/`approved`，但必须规范化为 authorization REVIEW 的 `decision: authorize`。

`reject`、`rejected`、`deny`、`denied` 或其他非肯定值不得生成 authorization REVIEW，返回既有结构化错误并保证零写入。该规则不改变 v3 的人工拒绝兼容行为。

如果产品需要记录人工拒绝，应通过普通追加 REVIEW 表达，不得把拒绝伪装成授权。

## 5. 发布前验证

公共方法必须在任何新文件发布前验证：

1. workspace identity/version/encoding 有效；
2. `review_id` 唯一解析为旧 REVIEW；
3. 旧 REVIEW 字节不修改；
4. subject 是同 workspace 的合法 TASK；
5. edge 是冻结 T4/T5/T6/T7 中需要授权的合法单边；
6. attempt 绑定满足该 edge 的冻结规则；
7. family digest 的有无与值满足该 edge 的冻结规则；
8. operation kind 与 scope 固定正确；
9. 时间字段格式、顺序和发布点有效；
10. Profile 已采用并具有可信 evaluator；
11. issuer proof 存在；
12. evaluator 精确返回 `AUTHORIZED`；
13. 新 REVIEW 的 references 包含且只由该转换所需方式引用旧事实；
14. 完整候选通过 v4 REVIEW Schema 与关系验证。

若需要读取 TASK 当前状态、attempt 或 family，验证和新 REVIEW 发布必须使用现有 family linearization boundary，取得边界后重新读取；不得新建锁系统。Profile registry 在 Project 初始化后保持不可变。

## 6. 错误与零写入

使用既有 Base 错误，不新增同义错误码：

| 情况 | 错误 |
|---|---|
| 没有可用的已采用可信 Profile | `AUTHORIZATION_PROFILE_UNAVAILABLE` |
| Profile 未采用、proof 缺失、evaluator 返回 DENIED/UNKNOWN/其他值或抛错 | `AUTHORIZATION_INVALID` |
| binding、edge、subject、attempt、family 或时间顺序不合法 | `AUTHORIZATION_INVALID`，除非冻结合同已有更精确错误 |
| 发布点已经过期 | `AUTHORIZATION_EXPIRED` |
| 旧 REVIEW 不存在、类型错误或关系不可证 | 使用冻结合同已有关系/授权错误，不得新造码 |

所有失败必须验证：

```yaml
NEW_REVIEW_FILES: 0
OLD_REVIEW_BYTES_CHANGED: false
TASK_MOVES: 0
NEW_TRANSITIONS: 0
NEW_ATTEMPTS: 0
AUTHORIZATION_CONSUMPTIONS: 0
```

MCP 必须原样投影 Project 的结构化错误。

## 7. `write_review` 边界保持不变

通用 `Project.write_review` 仍是追加 typed REVIEW 事实的接口。本任务书不授权把它悄悄改造成：

- `mark_human_approved` 的替代入口；
- T4–T7 生命周期消费入口；
- 基于调用者字段自证授权的入口；
- 自动移动 TASK 的入口。

即使通用 `write_review` 落盘了结构上类似 authorization 的事实，后续 transition 仍必须完整验证，并可能拒绝。MCP 的 `mark_human_approved` 不得通过 `write_review` 绕过本任务书规定的公共 validated append path。

## 8. 必须先增加的测试

### 8.1 授权成功

- 可信 evaluator 返回 `AUTHORIZED`；
- evaluator 在追加阶段被真实调用一次；
- 只新增一个 `review_kind: authorization` REVIEW；
- 新 REVIEW 的 subject、transition、attempt、family、scope、time、profile、proof、references 完整；
- 旧 REVIEW 完整字节不变；
- TASK 仍在原状态；
- 新 authorization 通过真实 T4/T5/T6/T7 消费入口后才移动 TASK。

### 8.2 可信边界失败

- registry 为空；
- profile 未采用；
- profile 已采用但 evaluator 未注册；
- evaluator 返回 `DENIED`；
- evaluator 返回 `UNKNOWN`；
- evaluator 返回任意其他值；
- evaluator 抛出异常；
- issuer proof 缺失；
- caller 在顶层或嵌套字段夹带 evaluator/policy/registry/`AUTHORIZED` 结果。

每项必须断言 evaluator 调用次数符合预期及完整工作区字节映射不变。

### 8.3 Binding 失败

- review_id 不存在或不是 REVIEW；
- subject 不一致；
- 非法 edge；
- attempt 缺失、错误或旧轮次；
- family digest 缺失、错误或不应出现；
- operation kind/scope 试图漂移；
- issued_at/expires_at 非法或已过期；
- 非肯定 decision；
- 试图覆盖 references、subject、workspace 或 stored decision。

全部零写入。

### 8.4 再次消费验证

- append 时 `AUTHORIZED`、consume 时仍 `AUTHORIZED` → 合法迁移；
- append 时 `AUTHORIZED`、consume 时变为 `DENIED`/`UNKNOWN` → transition 拒绝且零迁移；
- append 后授权 REVIEW 字节变化 → 摘要/授权拒绝；
- append 后过期 → `AUTHORIZATION_EXPIRED`；
- 成功消费后 exact transition retry 仍遵循既有 receipt/单次消费合同；
- 同一 authorization 被其他 TASK/edge 消费仍拒绝。

### 8.5 MCP 与版本兼容

- FastMCP Client 通过 `mark_human_approved` 调用公共 Project 方法；
- MCP 中不存在 evaluator、Profile 角色表或私有 Core import；
- DENIED/UNKNOWN 在 MCP 返回结构化错误且零写入；
- v4 肯定决定追加 authorization REVIEW，不追加 assessment；
- v4 非肯定决定不追加 authorization；
- v3 原方法、MCP 参数与人工 approve/reject 行为保持 3.2.5 回归；
- v4 扩展字段对 v3 schema 为向后兼容可选参数，但不得改变 v3 执行语义。

## 9. 允许修改范围

沿用 WP4B.2a 及既有 WP4B allowlist，并为本阻断明确允许：

- `src/fcop/v4/authorization.py`：抽取/复用内部 Profile issuer 校验；
- `src/fcop/v4/creation.py`：完成 v4 `mark_human_approved` 公共追加路径；
- `src/fcop/v4/boundary.py` 与 public-surface snapshot：仅在保持 v3 签名隔离所必需时调整；
- MCP `mark_human_approved` handler/schema/文档：只做版本路由与公共 Project 委托；
- 与本边界直接对应的单元、Conformance 补充、FastMCP transport、回归测试；
- WP4B 报告、CHANGELOG、snapshot 与最终 Manifest。

不允许修改冻结 spec、冻结 60 个 Test ID 或 Schema 基本语义。

## 10. 不允许的实现

- MCP 直接 import `_Creation`、`validate_gate` 或其他私有 Core；
- MCP 自己调用 evaluator；
- 把 evaluator 或 `AUTHORIZED` 结论作为工具参数；
- 先追加授权，再调用 transition 试错，失败后删除授权；
- 先迁移再回滚；
- 用 UI/Host/角色名/`approver=ADMIN` 代替 Profile evaluator；
- 修改旧 REVIEW；
- 将 `mark_human_approved` 同时做成授权追加和 TASK 迁移；
- 让 append-time 验证替代 consume-time 验证；
- 新增数据库、授权 ledger、缓存权威、后台组件、状态机或锁系统；
- 修改 CodeFlowMu。

## 11. 恢复与完整验证

本任务书提交后，从当前 review 分支 HEAD 建立或恢复独立工作树。现有未提交实现已经保留在独立工作树时：

1. 先保存并核验当前差异清单；
2. 不得用 reset/checkout 覆盖未完成工作；
3. 先实现并验证本公共授权追加边界；
4. 再审查并继续原 WP4B 未完成实现；
5. 重新运行此前仅部分执行的完整测试，旧的局部绿色记录不能替代最终结果。

最终至少必须通过：

- 本任务书授权追加定向测试；
- 已通过的 REPORT 查询 68 项定向回归；
- WP3E v4 单元测试；
- v4 frozen Conformance `119/119`；
- 全量 `tests/test_fcop`；
- 全量隔离 MCP suite；
- FastMCP 真实 Client T1–T7 与授权追加；
- v3/v4 public-surface 与工具 snapshot；
- 46/46 v4 MCP disposition；
- 11/11 static resources；
- 3/3 read-only Profile templates；
- Ruff、mypy、wheel/sdist、clean install；
- Windows/Linux/macOS GitHub required CI。

## 12. GitHub 交付

继续使用固定分支 `review/fcop-4.0-wp4b-mcp-adapter` 与 [Draft PR #15](https://github.com/joinwell52-AI/FCoP/pull/15)。

成功交付必须包含：

1. `CONTENT_COMMIT`：完整 WP4B 实现、测试、文档和结果报告；
2. `MANIFEST_COMMIT`：最终清单与逐文件 SHA-256；
3. refetch 远端 HEAD 和父链；
4. 从远端逐文件回读并核验哈希；
5. 最终 Manifest HEAD 的 required GitHub CI 全绿。

任务书提交或阻断报告提交的绿色 CI 不得替代实现验收。

## 13. 完成回执新增字段

最终 WP4B 回执必须增加：

```yaml
WP4B_3_DECISION_APPLIED: true
PUBLIC_AUTHORIZATION_APPEND_METHODS: 1/1
PUBLIC_AUTHORIZATION_APPEND_METHOD: Project.mark_human_approved
NEW_PUBLIC_METHOD_NAMES: 0
AUTHORIZATION_PROFILE_VALIDATOR_IMPLEMENTATIONS: 1
APPEND_AND_CONSUME_PROFILE_VALIDATOR_SHARED: PASS
APPEND_AUTHORIZED: PASS
APPEND_DENIED_ZERO_WRITE: PASS
APPEND_UNKNOWN_ZERO_WRITE: PASS
APPEND_PROFILE_UNAVAILABLE_ZERO_WRITE: PASS
APPEND_INVALID_BINDING_ZERO_WRITE: PASS
APPEND_EXPIRED_ZERO_WRITE: PASS
OLD_REVIEW_IMMUTABLE: PASS
AUTHORIZATION_REVIEW_APPENDED: PASS
TASK_MOVED_DURING_APPEND: false
CONSUME_REVALIDATION: PASS
GENERAL_WRITE_REVIEW_SEMANTICS_CHANGED: false
V3_MARK_HUMAN_APPROVED_REGRESSION: PASS
MCP_MARK_HUMAN_APPROVED_PROJECT_DELEGATION: PASS
MCP_PRIVATE_AUTHORIZATION_IMPORTS: 0
```

并继续满足 WP4B.2a、WP4B.2、WP4B.1、WP4B.0 与原 WP4B 的全部完成条件。

## 14. 停止点与 Gate

成功完成整个 WP4B 后停止，只请求：

```yaml
REQUESTED_GATE: WP4B_MCP_ADAPTER_ACCEPTED
```

不得自行签署 Gate，不得进入 WP4C。

若发现必须修改冻结合同/Schema、增加公共方法名、改变通用 `write_review` 或建立第二套授权系统，立即停止并追加阻断报告：

```yaml
WP4B_STATUS: BLOCKED
REQUESTED_GATE: NONE
```

## 15. 本任务书不授权

```yaml
WP4C_AUTHORIZED: false
WP4D_AUTHORIZED: false
MAIN_MERGE_AUTHORIZED: false
RELEASE_AUTHORIZED: false
PYPI_PUBLISH_AUTHORIZED: false
GITHUB_RELEASE_AUTHORIZED: false
CODEFLOWMU_CHANGE_AUTHORIZED: false
WORKSPACE_MIGRATION_AUTHORIZED: false
```
