---
document_role: ADMIN_SCOPE_DECISION_AND_EXECUTION_TASKBOOK
title: FCoP 4.0 WP4B.2a REPORT 零 Head 错误码对齐与 WP4B 恢复任务书
version: 1.0
status: AUTHORIZED_FOR_WP4B_RESUME_ONLY
execution_authorized: true
authorized_scope: WP4B_RESUME_ONLY
stop_code_resolved: WP4B_2_INTERNAL_ERROR_CODE_CONFLICT
input_head: 535e85d88be80e943744287106cfed2908aa3307
amends_taskbook_commit: 9359de1f9268dd13c8c393ee403c8837130a0960
frozen_contract_commit: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
main_merge_authorized: false
release_authorized: false
wp4c_authorized: false
codeflowmu_change_authorized: false
---

# FCoP 4.0 WP4B.2a：REPORT 零 Head 错误码对齐与 WP4B 恢复任务书

## 0. ADMIN 裁决

ADMIN 接受提交 `535e85d88be80e943744287106cfed2908aa3307` 中记录的任务书内部冲突。

冻结合同 F4.3.4 是本次裁决的唯一语义权威：

```yaml
REPORT_HEAD_COUNT_0: REPORT_REQUIRED
REPORT_HEAD_COUNT_1: SUCCESS
REPORT_HEAD_COUNT_GT_1: REPORT_HEAD_AMBIGUOUS
```

当前实现把所有 `len(heads) != 1` 统一映射为 `REPORT_HEAD_AMBIGUOUS`，使 replacement 环形成零 head 时违反冻结合同。这是实现偏差，不是合同缺口。

因此，正式允许 WP4B.2 第 2.1 节存在一个且只有一个限定例外：

> 抽取共享 resolver 时，除“非空候选 REPORT 图最终计算为零 head”的错误码必须从 `REPORT_HEAD_AMBIGUOUS` 修正为 `REPORT_REQUIRED` 外，T3 的其他成功行为、失败行为和错误码全部保持不变。

本裁决不修改冻结规范，不增加错误码，不改变多 head 语义。

## 1. 权威输入与优先级

1. 冻结合同：`spec/fcop-4.0-spec.md`、`spec/fcop-4.0-spec.zh.md`，提交 `aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6`；
2. 本 WP4B.2a 裁决；
3. WP4B.2 任务书，提交 `9359de1f9268dd13c8c393ee403c8837130a0960`；
4. WP4B、WP4B.0、WP4B.1 的既有任务书；
5. 阻断报告，提交 `535e85d88be80e943744287106cfed2908aa3307`。

若 WP4B.2 第 2.1 节的“全部错误码保持不变”与本文件冲突，仅以本文件定义的零 head 例外为准。WP4B.2 其他条款继续有效。

## 2. 唯一获准的生产语义修改

共享 REPORT replacement/head resolver 必须显式区分：

```python
if not candidates:
    raise REPORT_REQUIRED

# 完成 replacement 图验证与 head 计算后
if len(heads) == 0:
    raise REPORT_REQUIRED
if len(heads) > 1:
    raise REPORT_HEAD_AMBIGUOUS
return heads[0]
```

伪代码只表达语义，不授权机械照抄，也不改变既有错误对象格式、上下文字段或异常类型。

必须满足：

- 无 REPORT 候选：继续返回 `REPORT_REQUIRED`；
- 有 REPORT 候选但有效 head 数为零：返回 `REPORT_REQUIRED`；
- 有两个或更多有效 head：继续返回 `REPORT_HEAD_AMBIGUOUS`；
- 唯一有效 head：返回该 head；
- replacement 自引用、缺失目标、跨 subject、跨 attempt、重复或无法证明的引用，继续按照冻结合同和既有明确规则 Fail Closed；不得借本裁决统一改写为 `REPORT_REQUIRED`；
- T3、`Project.list_reports`、`Project.read_report` 必须调用同一 resolver，不得在调用方转换错误码；
- MCP 必须原样传递公共 Project 边界的结构化错误，不得二次解释。

## 3. 不允许的扩大解释

本文件不授权：

- 修改 F4.3.4 或任何冻结规范；
- 修改 Schema 来迁就实现；
- 新增、删除或改名 Base 错误码；
- 将所有 replacement 图错误都改为 `REPORT_REQUIRED`；
- 保留 T3 的旧错误码、仅在 list/read 或 MCP 层映射；
- 在 MCP 中实现第二份 head/replacement 遍历；
- 新增第三个公共 REPORT head 方法；
- 新建数据库、索引账本、缓存 Store、后台进程、状态机或锁系统；
- 修改 CodeFlowMu；
- 进入 WP4C、合并 main 或发布。

## 4. 必须增加或固定的测试

### 4.1 Resolver 三分支

至少覆盖：

1. 空候选集合 → `REPORT_REQUIRED`；
2. 合法单 head → 成功；
3. 两个独立 final heads → `REPORT_HEAD_AMBIGUOUS`；
4. 两个 replacement heads → `REPORT_HEAD_AMBIGUOUS`；
5. 非空 replacement 环导致零 head → `REPORT_REQUIRED`；
6. 自引用 replacement → 既有 Fail Closed 错误保持；
7. 引用不存在 REPORT → 既有 Fail Closed 错误保持；
8. 跨 subject/attempt replacement → 既有 Fail Closed 错误保持。

### 4.2 三个消费者一致

对同一零 head fixture，必须通过真实生产入口证明：

```yaml
T3: REPORT_REQUIRED
Project.list_reports(head_only=true, exact_subject_attempt): REPORT_REQUIRED
Project.read_report(any_member_of_zero_head_group): REPORT_REQUIRED
MCP_list_reports: REPORT_REQUIRED
MCP_read_report: REPORT_REQUIRED
```

如果现有公共方法的精确参数命名与示意不同，以 WP4B.2 固定的公共接口为准，不另建旁路。

同一多 head fixture 必须在上述消费者中一致返回 `REPORT_HEAD_AMBIGUOUS`。

### 4.3 零写入与回归

错误路径必须验证完整工作区文件字节映射不变，并至少完成：

- 原 WP4B.2 公共查询定向测试；
- T3 生命周期回归；
- WP3E v4 单元测试；
- v4 frozen Conformance `119/119`；
- v3 `tests/test_fcop` 回归；
- 隔离 MCP 回归；
- FastMCP 真实 transport 错误传播测试；
- public-surface snapshot；
- Ruff、mypy、打包与最终 GitHub CI。

不得通过改 Test ID、删除断言、增加 skip/xfail 或放宽 fixture 使测试变绿。

## 5. 恢复执行规则

完成第 2–4 节并通过定向验证后，可继续执行 WP4B.2 已授权的恢复流程：

1. 核验未完成实现备份 SHA-256 与 14/14 entry hashes；
2. 在独立工作树内安全恢复；
3. 审查每一处恢复差异，不得覆盖本轮 resolver 修正；
4. 完成 WP4B、WP4B.0、WP4B.1、WP4B.2 的所有剩余实现与测试；
5. 仍使用固定分支 `review/fcop-4.0-wp4b-mcp-adapter` 和 Draft PR #15；
6. 最终实现必须以 Content/Manifest 两提交交付；
7. 远端回读所有交付文件并核验 SHA-256；
8. 等待最终 Manifest HEAD 的 required GitHub CI 全绿。

本轮 resolver 修正通过后不设置额外中间 Gate；应继续完成整个 WP4B，再停止请求最终 Gate。

## 6. 允许修改范围

除 WP4B.2 既有 allowlist 外，本修正本身只允许触及：

- 共享 REPORT resolver 所在或抽取后的内部模块；
- 调用该 resolver 的 T3 与 Project v4 只读边界；
- 针对零/一/多 head 和消费者一致性的测试；
- WP4B 结果报告、阻断报告追加段及最终 Manifest。

如发现必须修改冻结规范、Schema 基本语义、公开方法名或新建权威 Store，立即停止并报告新的阻断。

## 7. 完成回执新增字段

最终 WP4B 回执必须包含：

```yaml
WP4B_2A_DECISION_APPLIED: true
ZERO_HEAD_CONTRACT_CODE: REPORT_REQUIRED
MULTI_HEAD_CONTRACT_CODE: REPORT_HEAD_AMBIGUOUS
ZERO_HEAD_T3_CORRECTED: PASS
ZERO_HEAD_CONSUMER_PARITY: PASS
MULTI_HEAD_CONSUMER_PARITY: PASS
OTHER_T3_ERROR_CODE_DRIFT: 0
BASE_ERROR_CODES_ADDED: 0
REPORT_HEAD_RESOLVER_IMPLEMENTATIONS: 1
T3_AND_QUERY_RESOLVER_SHARED: PASS
QUERY_ZERO_WRITE: PASS
```

并继续满足 WP4B.2 规定的全部最终字段，包括：

```yaml
PUBLIC_REPORT_QUERY_METHODS: 2/2
NEW_PUBLIC_METHOD_NAMES: 0
V4_CANONICAL_MCP_TOOLS: 46/46
STATIC_RESOURCES: 11/11
RESOURCE_TEMPLATES: 3/3 READ_ONLY_PROFILE_RESOURCE
V4_CONFORMANCE: 119/119
UNEXPECTED_FAILURES: 0
GITHUB_CI_AT_FINAL_HEAD: PASS
MAIN_MODIFIED: false
CODEFLOWMU_FILES_MODIFIED: 0
RELEASE_CREATED: false
WP4C_STARTED: false
```

## 8. 停止点与 Gate

成功完成整个 WP4B 后停止，只能请求：

```yaml
REQUESTED_GATE: WP4B_MCP_ADAPTER_ACCEPTED
```

不得自行签署 Gate。

失败时必须撤回未完成生产实现或保持在独立工作树，追加阻断证据，并报告：

```yaml
WP4B_STATUS: BLOCKED
REQUESTED_GATE: NONE
```

## 9. 本任务书不授权

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
