---
document_role: ADMIN_SCOPE_DECISION_AND_EXECUTION_TASKBOOK
title: FCoP 4.0 WP4B.2 公共 REPORT Head 只读查询边界与 WP4B 恢复任务书
version: 1.0
status: AUTHORIZED_FOR_WP4B_RESUME_ONLY
execution_authorized: true
authorized_scope: WP4B_RESUME_ONLY
stop_code_resolved: MCP_PUBLIC_REPORT_HEAD_QUERY_UNAVAILABLE
blocked_report_commit: 1434d409925bec233d6b246ebb081bdf5bc12f08
resumes_taskbook_commit: e885135f4b074845944a7b8b799de879549fbc33
parent_gate_commit: 982fcb24d9093e01c5ba4fdb87e710acd57e6d54
input_head: 1434d409925bec233d6b246ebb081bdf5bc12f08
frozen_contract_commit: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
main_merge_authorized: false
release_authorized: false
wp4c_authorized: false
codeflowmu_change_authorized: false
---

# FCoP 4.0 WP4B.2：公共 REPORT Head 只读查询边界与 WP4B 恢复任务书

## 0. ADMIN 裁决

ADMIN 接受当前阻断及其可复现实验证据：

```yaml
BLOCKED_REPORT_ACCEPTED: true
STOP_CODE: MCP_PUBLIC_REPORT_HEAD_QUERY_UNAVAILABLE
BLOCKED_HEAD: 1434d409925bec233d6b246ebb081bdf5bc12f08
CORE_T3_HEAD_CHECK: WORKING
PUBLIC_REPORT_HEAD_QUERY: MISSING
MCP_MAY_DUPLICATE_HEAD_JUDGMENT: false
```

正式裁决：REPORT replacement/head 图的判断属于 FCoP Toolkit 的公共只读事实解析能力。MCP 只能调用该公共能力，不能自行重写算法、读取私有 `_Creation` 或调用 `fcop.v4.lifecycle.report_head` 私有实现。

本任务书授权补齐现有公共方法在 v4 工作区的行为：

```yaml
V4_PUBLIC_METHODS_ENABLED:
  - Project.list_reports
  - Project.read_report
NEW_PUBLIC_METHOD_NAMES: 0
NEW_CORE_RULES: 0
NEW_ERROR_CODES: 0
```

修复完成并通过定向测试后，允许恢复备份的未完成 WP4B 实现，继续完成原 WP4B、WP4B.0 与 WP4B.1；不需要在查询修复后再次等待中间 Gate。

## 1. 权威输入

- 冻结合同：`spec/fcop-4.0-spec.md`、`spec/fcop-4.0-spec.zh.md`，提交 `aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6`
- WP1 MCP 合同：`reports/FCOP-4.0-WP1-COMPATIBILITY-AND-MCP.md`
- 当前阻断：`reports/FCOP-4.0-WP4B-BLOCKED.md`，提交 `1434d409925bec233d6b246ebb081bdf5bc12f08`
- 原 WP4B 任务书：`245d914e1f0aff48a19d8f0ba8432e6b4f008b68`
- WP4B.0：`b2453202686d08bd6584302072e0be814a059be4`
- WP4B.1：`e885135f4b074845944a7b8b799de879549fbc33`

本文件仅补齐公共查询合同。若与冻结 Core 冲突，立即停止，不得修改规范或 Schema。

## 2. 设计边界

### 2.1 一份 Head 算法，三个消费者

REPORT head/replacement 图只能存在一份生产判断：

```text
shared internal REPORT graph resolver
  ├─ T3 lifecycle gate
  ├─ Project.list_reports (v4)
  └─ Project.read_report (v4)
```

允许把当前 `src/fcop/v4/lifecycle.py` 中已经通过 Conformance 的 `report_head` 算法抽取到一个职责单一的内部模块，例如 `src/fcop/v4/reports.py`；也允许采用不新增文件的等价共享方式。

要求：

- T3、list、read 必须调用同一实现；
- 抽取前后 T3 的所有成功/失败行为和错误码保持不变；
- 不允许复制三份相似算法；
- 不允许 MCP 直接 import 私有 resolver；
- 不把 resolver 公开为第三个 Project 方法；
- 不建立索引数据库、缓存账本或第二权威 Store。

### 2.2 只读性质

公共查询不得：

- 写、改、移动或删除 TASK/REPORT/ISSUE/REVIEW；
- 创建 transition、receipt、authorization consumption 或 repair REVIEW；
- 自动选择两个冲突 head 中“较新”的一个；
- 自动修复 replacement chain；
- 把 malformed 文件静默跳过并仍返回绿色结论；
- 使用 mtime、目录顺序或文件名大小猜权威 head。

## 3. `Project.list_reports()` 的 v4 合同

### 3.1 v4 逻辑参数

v4 handler 接受以下语义参数；Adapter 可把旧 MCP 参数名映射到这些语义字段：

| 参数 | 类型 | 默认 | 规则 |
|---|---|---|---|
| `subject_ref` | `str | None` | `None` | 按正式 subject 过滤；MCP `task_id` 是兼容别名 |
| `attempt_id` | `str | None` | `None` | 按执行轮次过滤；指定时必须同时指定 `subject_ref` |
| `sender` | `str | None` | `None` | 按 REPORT sender 过滤；MCP `reporter` 是兼容别名 |
| `head_only` | `bool` | `False` | `True` 时每个 subject/attempt 只返回唯一有效 head |
| `limit` | `int | None` | `None` | 非负；在完整验证与确定性排序后分页 |
| `offset` | `int` | `0` | 非负；在完整验证与确定性排序后分页 |

v3 `Project.list_reports()` 的原签名与行为不得改变。v4 绑定实例可以使用现有 version boundary 的 handler 签名，不要求破坏类级 v3 反射。

### 3.2 查询行为

1. 读取正式 v4 REPORT 目录中的候选文件；
2. 对候选逐个执行已有 Encoding、Schema、关系和 workspace 身份验证；
3. 按 `(subject_ref, attempt_id)` 分组；
4. 对每组运行唯一共享 head resolver；
5. 任何组出现零 head、多个 head、非法 replacement、跨 subject/attempt replacement 或无法证明的引用，整次查询 Fail Closed；
6. `head_only=False` 返回组内全部合法不可变 REPORT，并附加 head 元数据；
7. `head_only=True` 每组只返回唯一当前 head；
8. 确定性排序后再分页，不能因 `limit`/`offset` 跳过尚未验证的冲突文件。

`attempt_id` 未同时提供 `subject_ref` 时返回既有 `INVALID_ENVELOPE`。若过滤后没有 REPORT，返回空列表；针对明确 subject/attempt 请求 current head 而零 head时，使用冻结合同的 `REPORT_REQUIRED`。

### 3.3 返回投影

每个 v4 结果至少包含：

```yaml
report_id: <id>
subject_ref: <id>
attempt_id: <urn:uuid>
report_kind: final | replacement
replaces: <report-id-or-null>
is_head: true | false
head_ref: <unique-current-head-id>
head_digest: <sha256-of-stored-head-bytes>
path: <workspace-relative-posix-path>
```

可以包含原 envelope 的其他只读字段，但不得把派生 `is_head/head_ref/head_digest` 写回 REPORT 文件。

## 4. `Project.read_report()` 的 v4 合同

### 4.1 输入

保持一个必填定位参数：

```text
filename_or_id: exact REPORT filename or exact REPORT id
```

禁止路径穿越、模糊前缀命中多个对象或从 history/临时目录猜测。MCP 的 `filename` 映射到该参数。

### 4.2 行为

1. 定位并严格验证请求的 REPORT；
2. 从其 `subject_ref` 与 `attempt_id` 确定 replacement group；
3. 在稳定读取边界内运行共享 head resolver；
4. 多 head 返回 `REPORT_HEAD_AMBIGUOUS`；
5. 零 head 返回 `REPORT_REQUIRED`；
6. 如果请求的是被合法 replacement 替代的旧 REPORT，允许读取，但必须返回 `is_head: false` 和唯一 `head_ref/head_digest`；
7. 如果请求的是当前 head，返回 `is_head: true`；
8. 不静默改为返回另一个 REPORT。

返回至少包含第 3.3 节的元数据和所请求 REPORT 的完整只读内容投影。

## 5. 一致性与并发边界

查询需要与现有 REPORT 写入、replacement 与 T3 使用相同的 family/subject 线性化边界或能证明等价稳定性的现有锁边界。

不得宣称整个 workspace 的跨 family 查询是一个全局事务快照。正确承诺是：

- 每个 `(subject_ref, attempt_id)` 分组在自己的既有线性化边界内得到可证明结果；
- 查询中发生并发变化而无法证明一致时 Fail Closed；
- 多组按稳定 key 顺序处理，一次只持有必要的一个 family boundary，避免建立新锁系统或多锁死锁；
- 查询结束后不得留下锁、receipt 或临时权威文件。

## 6. MCP 映射

### 6.1 `list_reports`

保留现有工具名。允许增加向后兼容可选参数：

```yaml
existing:
  reporter: ""
  task_id: ""
  status: open
  limit: 0
  offset: 0
additive_v4:
  attempt_id: ""
  head_only: false
```

映射：

- `task_id` -> v4 `subject_ref`；
- `reporter` -> v4 `sender`；
- `attempt_id`、`head_only` 原样传递；
- `limit=0` -> `None`；
- v4 `status=archived` 不得读取 legacy history 作为权威 REPORT；按既有 WP1 legacy disposition Fail Closed；
- `status=open|all` 在 v4 只指向同一正式 append-only REPORT 面，不创造第二种状态。

MCP 不得扫描 REPORT 后自行计算 head。

### 6.2 `read_report`

保留现有 MCP 参数 `filename`，调用 `Project.read_report(filename_or_id=filename)` 的 v4 handler。格式化层必须显示：

- `report_id`、`subject_ref`、`attempt_id`、`report_kind`；
- `is_head` 与 `head_ref`；
- Core 错误码原样可观察。

不得在公共查询不可用时回退本地文件扫描。

## 7. 必须增加的测试

### 7.1 Public Project 正常路径

- 单个 final REPORT：list/read 均 `is_head=true`；
- final -> replacement：旧 REPORT 可读但 `is_head=false`，两者指向同一 current head；
- `head_only=true` 只返回 replacement head；
- subject、attempt、sender 过滤正确；
- attempt 不带 subject 被拒绝；
- 排序和分页在验证之后执行；
- 查询前后 workspace 全文件字节图不变。

### 7.2 异常图

- 两个 final heads -> `REPORT_HEAD_AMBIGUOUS`；
- 两个 replacement heads -> `REPORT_HEAD_AMBIGUOUS`；
- replacement 环/cycle 导致零 head -> `REPORT_REQUIRED`；
- replacement 指向不存在 REPORT；
- replacement 跨 subject；
- replacement 跨 attempt；
- malformed/非 UTF-8/Schema 非法 REPORT；
- exact ID 与 filename 冲突或路径穿越；
- 所有失败零写入。

### 7.3 与 Core T3 对齐

针对同一 fixture，必须证明：

- 公共查询与 T3 对合法 unique head 得到同一 `head_ref/head_digest`；
- 公共查询与 T3 对多 head 返回同一 `REPORT_HEAD_AMBIGUOUS`；
- 公共查询与 T3 对零 head 返回同一 `REPORT_REQUIRED`；
- replacement/attempt 规则不存在查询版和生命周期版两种解释。

### 7.4 并发

- list/read 与 concurrent replacement；
- list/read 与 concurrent second head corruption fixture；
- 查询不得返回两个对象都标为 head；
- 无法取得稳定分组时 Fail Closed；
- 不新增全局锁或后台协调器。

### 7.5 MCP 真实入口

- v4 `list_reports` unique/multiple/zero head；
- v4 `read_report` current/replaced/ambiguous；
- 稳定错误码通过 FastMCP transport 可观察；
- v3 原 list/read 回归不变；
- Adapter 没有 import `fcop.v4.*` 私有 resolver；
- Adapter 没有第二份 replacement traversal 实现。

## 8. 允许修改范围

仅为实现上述公共读边界允许：

- `src/fcop/project.py`：必要的 v4 公共方法占位/文档对齐，但不得改变 v3 行为；
- `src/fcop/v4/boundary.py`：把 `list_reports`、`read_report` 明确分类为 `V4_HANDLER`；
- `src/fcop/v4/lifecycle.py`：抽取后改为调用共享 resolver；
- `src/fcop/v4/creation.py` 或真实 handler registry：注册两个 v4 handler；
- `src/fcop/v4/reports.py` 或一个等价的单职责内部模块；
- 对应 `tests/test_fcop/**`、MCP 测试和 public-surface snapshot；
- MCP `list_reports/read_report` 的薄参数映射、格式化和 snapshot；
- WP4B 报告、Manifest 与 `[Unreleased]` 说明。

恢复原 WP4B 未完成实现时，继续沿用 WP4B/WP4B.0/WP4B.1 原允许范围。

## 9. 备份恢复规则

阻断报告记录的 14 文件 ZIP 只能作为未完成工作的恢复来源：

```text
D:/FCoP-wp4b-evidence/wp4b1-unfinished-e246ecc148534c73a1eae34b3ae3b628.zip
SHA-256: 27d636ec70dc675bf90e533b2951e679e9adb62abbf892b5efb1fc40271e1d87
```

恢复前必须：

1. 验证 ZIP SHA-256；
2. 列出并验证 14/14 entry hash；
3. 拒绝绝对路径、`..`、symlink 和任务范围外文件；
4. 只恢复到独立 WP4B worktree；
5. 恢复后以当前任务书 HEAD 为基线逐文件审查，不把 ZIP 当权威提交；
6. 原 `D:/FCoP` 现场保持不动。

## 10. 禁止事项

- MCP 自己实现 REPORT head/replacement 算法；
- MCP import `project._v4_creation` 或私有 `report_head`；
- 新增 `Project.resolve_report_head` 等第三个公共方法；
- 修改 F4.3.4、REPORT Schema 或冻结 Conformance；
- 通过跳过 malformed/ambiguous 文件让查询成功；
- 用 `family_digest` 冒充普通 Root REPORT 查询；
- 用 T3 写操作作为只读查询；
- 写索引文件、数据库、缓存账本或 repair REVIEW；
- 修改 CodeFlowMu、main，进入 WP4C/WP4D 或发布。

## 11. 硬停止条件

出现以下任一项立即停止并只更新阻断报告：

- T3 与公共查询无法共用同一 resolver；
- 必须改变冻结 head 算法才能提供查询；
- existing `Project.list_reports/read_report` 无法承载 v4 handler 且必须新增公共方法名；
- 稳定读取必须引入第二锁系统或数据库；
- v3 list/read 行为发生破坏；
- FastMCP 无法传递 `REPORT_HEAD_AMBIGUOUS`；
- 恢复 ZIP hash/entry/scope 不匹配；
- 最终 CI 非绿。

阻断时：

```yaml
WP4B_STATUS: BLOCKED
REQUESTED_GATE: NONE
```

## 12. 完成标准

WP4B 最终回执除既有字段外，必须增加：

```yaml
WP4B_2_DECISION_APPLIED: true
PUBLIC_REPORT_QUERY_METHODS: 2/2
NEW_PUBLIC_METHOD_NAMES: 0
REPORT_HEAD_RESOLVER_IMPLEMENTATIONS: 1
T3_AND_QUERY_RESOLVER_SHARED: PASS
LIST_REPORTS_V4: PASS
READ_REPORT_V4: PASS
REPORT_HEAD_UNIQUE: PASS
REPORT_HEAD_AMBIGUOUS: PASS
REPORT_HEAD_ZERO: PASS
REPLACED_REPORT_METADATA: PASS
QUERY_ZERO_WRITE: PASS
QUERY_CONCURRENCY: PASS
V3_REPORT_QUERY_REGRESSION: PASS
MCP_REPORT_QUERY_DELEGATION: PASS
MCP_PRIVATE_V4_IMPORTS: 0
```

并且原 WP4B、WP4B.0、WP4B.1 的全部完成条件仍须满足，包括：

```yaml
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

成功后停止，只请求：

```yaml
REQUESTED_GATE: WP4B_MCP_ADAPTER_ACCEPTED
```

不得自行签署 Gate。

## 13. GitHub 交付

继续使用 [Draft PR #15](https://github.com/joinwell52-AI/FCoP/pull/15) 和固定分支 `review/fcop-4.0-wp4b-mcp-adapter`。

交付仍为：

1. `CONTENT_COMMIT`：公共查询、恢复的 WP4B 实现、测试与报告；
2. `MANIFEST_COMMIT`：最终 Manifest；
3. refetch 远端 HEAD；
4. 从远端逐文件回读 SHA-256；
5. 等最终实现 HEAD 的全部 required GitHub CI 真实执行全绿。

任务书提交或阻断报告提交的绿色 CI 不得替代最终实现验收。

## 14. 本任务书不授权

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
