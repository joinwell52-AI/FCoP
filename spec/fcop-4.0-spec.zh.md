# FCoP 4.0 候选规范（中文）

> **状态：Candidate · Not Implemented · Not Released**
>
> WP1 合同版本：`4.0.0-candidate.1`；基线 `68dbeb15f4e7f84e1d03f907be9fa66c2265843e`；WP0 证据 `c259bebdad77122d24dc18a6dd3f8fe191e4042f`。在 ADMIN 签署 `FCOP_4_CONTRACT_FROZEN` 并完成后续实现/发布前，FCoP 3.2.5 仍是现行协议。

## 0. 规范词义与权威

**F4.0.1** “必须/不得”（MUST/MUST NOT）是符合性要求；“应当/可以”（SHOULD/MAY）是建议或可选能力。

**F4.0.2** 英文 `spec/fcop-4.0-spec.md` 是候选规范主要权威文本；本中文版与其条款编号、对象、迁移、错误和不变量必须一致。差异必须阻止冻结/发布。

**F4.0.3** JSON Schema 只对其能表达的结构具有机器权威性。生命周期、授权、并发、恢复等行为以本规范为准；WP2 测试只能验证本规范，不得新增规则。

## 1. 定义、分层与 Core

**F4.1.1** FCoP 是文件原生的 Agent 行为治理协议：文件承载协议，路径表达当前状态，事件记录迁移历史。

**F4.1.2** FCoP 不执行任务，不拥有 LLM/tool 调用、Host、Session、Scheduler、数据库、UI、网络或进程管理。

| 层 | 合同 | Core |
|---|---|---:|
| Core | 跨实现必须一致的协议语义与不变量 | 是 |
| Specification | Core 的字段、状态、错误与可观察行为 | 权威表达 |
| Toolkit | 校验、查询、迁移、恢复和便利 API | 否 |
| Profile | 角色、签发权、组织和产品政策 | 否 |
| Runtime | Host/模型/Session/Scheduler/UI/DB/网络/进程 | 否 |

**F4.1.3** Core 仅含 C1–C8：工作区身份、四类信封、生命周期、四种关系、证据与收敛、持久授权、创建幂等、可恢复原子语义。

**F4.1.4** 固定角色、EVAL、Ledger 信封、Git branch/merge、CodeFlowMu 工作面、BCG、Relay 与在线升级不得进入 Core。

## 2. C1 · 工作区身份

**F4.2.1** 4.0 工作区的 Core 声明是 UTF-8 JSON 文件 `fcop/fcop.json`。它至少包含：

```json
{
  "protocol": "fcop",
  "protocol_version": "4.0",
  "workspace_id": "urn:uuid:00000000-0000-4000-8000-000000000000",
  "encoding": {"name": "fcop-filesystem", "version": "4.0"},
  "profiles": []
}
```

**F4.2.2** `workspace_id` 必须是小写规范 UUID URN，创建后稳定。每个 envelope 的 `workspace_id` 必须与声明相同，否则 `WORKSPACE_ID_MISMATCH`。

**F4.2.3** `profiles` 是已采用 Profile 标识符的有序数组；空数组表示无附加 Profile。团队、角色、leader 等 v3 字段可保留为 Profile 扩展，不得改变 Core 语义。

**F4.2.4** 备份或只读镜像可保留 ID。两个可写副本只有在外部保证单写者且共同表示同一逻辑工作区时才可保留 ID；任何独立 fork/派生可写工作区必须在第一次 4.0 写入前生成新 ID。无法证明时必须 `WORKSPACE_ID_CLONE_CONFLICT` 并 Fail Closed。

**F4.2.5** 不支持的 protocol/version/Encoding 分别返回 `UNSUPPORTED_PROTOCOL`、`UNSUPPORTED_WORKSPACE_VERSION`、`UNSUPPORTED_ENCODING`。

## 3. C2 · 四类正式信封

**F4.3.1** 正式业务信封严格限定为 `TASK`、`REPORT`、`ISSUE`、`REVIEW`。`shared/` 是知识面；operation receipt、锁和索引是 Encoding/Toolkit 内部事实，不是第五类信封。

**F4.3.2** 所有 envelope 都是 UTF-8、LF、YAML frontmatter + Markdown body，必含 `protocol: fcop`、`version: 4`、`type`、类型 ID、`workspace_id`、`sender`、`recipient`、带时区 `created_at`。

| 类型 | 额外必填 | 可选 Core 字段 |
|---|---|---|
| TASK | `task_id`, `subject`, `transitions` | `parent`, `branch_of`, `references`, `operation_id`, `operation_kind`, `normalized_request_digest` |
| REPORT | `report_id`, `subject_ref`, `attempt_id`, `report_kind`, `result` | `references` |
| ISSUE | `issue_id`, `subject_ref`, `severity` | `references` |
| REVIEW | `review_id`, `review_kind`, `subject_ref`, `decision` | `attempt_id`, `family_digest`, `authorization_ref`, `references` 及 §7 授权字段 |

**F4.3.3** REPORT/ISSUE/REVIEW 是追加事实：落盘后不得原地修改或删除。纠正、替换、撤销必须新建同类型事实，并在 `references` 中引用被影响事实。

**F4.3.4** REPORT 替换链使用 `report_kind: final|replacement`：replacement 必须引用同 subject/attempt 的当前 head。某 attempt 的有效 REPORT 是唯一未被合法 replacement 引用的 head；零个返回 `REPORT_REQUIRED`，多个返回 `REPORT_HEAD_AMBIGUOUS`。

**F4.3.5** REVIEW kind 至少包括 `assessment`、`acceptance`、`rejection`、`authorization`、`convergence`、`repair`。`mark_human_approved` 若保留，只能追加 REVIEW，不得改写原 REVIEW。

## 4. C3 · 单一权威路径、生命周期与事件

**F4.4.1** 权威 TASK 必须且只能位于以下一个路径；目录位置是 NOW 唯一真相：

```text
fcop/_lifecycle/{inbox,active,review,done,archive}/TASK-*.md
```

**F4.4.2** Base 合法迁移固定为七条：

| # | from | to | 条件摘要 |
|---:|---|---|---|
| T1 | None | inbox | 幂等创建成功 |
| T2 | inbox | active | 生成新 `attempt_id` |
| T3 | active | review | 当前 attempt 有唯一有效 REPORT |
| T4 | review | done | 当前 attempt 有 acceptance REVIEW 与有效授权 |
| T5 | review | active | rejection/返工决定；生成新 attempt |
| T6 | done | active | reopen 授权；生成新 attempt |
| T7 | done | archive | closure、授权与 family 收敛门通过 |

**F4.4.3** 一次命令只能提交一条边并追加一条 transition。跨多边便利调用必须拆分；任一步失败不得伪造后续事件。

**F4.4.4** `active -> done` 不属于 4.0 Base。`finish_task` 是 3.x Legacy；在 4.0 workspace 必须拒绝并返回 `LEGACY_TRANSITION_NOT_ALLOWED`，不得绕过 T3/T4。

**F4.4.5** transition 事件必含 `at/from/to/by/tool`；进入 active 时必含新 `attempt_id`；需要证据/授权时必含 `evidence_refs` 与 `authorization_ref`。事件只追加，不能推导 NOW。

**F4.4.6** archive 是终态。权威 TASK 不得从 archive 移入 history 或返回 lifecycle。v3 history 只读识别为 Legacy；4.0 Toolkit 只能生成非权威冷存储副本。

## 5. C4 · 四种关系

**F4.5.1** Core 关系只有 `parent`、`branch_of`、`subject_ref`、`references`。

| 关系 | 来源→目标 | 强度 | 语义 |
|---|---|---|---|
| parent | TASK→TASK | 强 | 委派/层级归属，不表示并发 Branch |
| branch_of | TASK→Root TASK | 强且最多一个 | 普通 TASK 是 Root 的并发工作分支 |
| subject_ref | REPORT/ISSUE/REVIEW→TASK 或 workspace | 强且唯一 | 正式主题；workspace ISSUE 使用 `workspace:<workspace_id>` |
| references | 任意 envelope→既有 envelope | 弱，门控使用时升级为必需证据 | 引用，不转移所有权 |

**F4.5.2** 强关系缺失、悬空、跨 workspace、循环或不唯一时返回 `RELATION_INVALID` 并 Fail Closed。普通弱引用缺失产生 `REFERENCE_UNRESOLVED` 审计结果；若该引用用于 REPORT/REVIEW/authorization/convergence 门，则操作必须拒绝。

**F4.5.3** Branch 的 `branch_of` 必须指向没有 `branch_of` 的 Root；Branch 不能成为 Branch Root。所有 Branch 必须是同一 Root 的兄弟；违反时 `BRANCH_DEPTH_EXCEEDED`。

**F4.5.4** 仅当 Root 在 active 且无歧义时可创建 Branch；其他阶段返回 `ROOT_NOT_ACTIVE`。done Root 必须先经 T6 授权 reopen，再创建 Branch。

**F4.5.5** `thread_key` 是 Profile/Legacy 字段，不改变四种 Core 关系。

## 6. C5 · Attempt、REPORT、接受与收敛

**F4.6.1** 每次进入 active（T2/T5/T6）必须生成不可复用的 `attempt_id`，格式 `urn:uuid:<uuid>`，写入该 transition。当前 attempt 是路径历史中最后一次进入 active 的事件所载 ID。

**F4.6.2** T3 必须引用唯一有效 REPORT；该 REPORT 的 subject_ref 必须是 TASK、attempt_id 必须等于当前 attempt。旧 attempt REPORT 永不满足新门。

**F4.6.3** T4 必须引用 `review_kind: acceptance`、`decision: approved` 的 REVIEW；其 subject_ref/attempt_id 和 references 中的 REPORT 必须匹配当前状态，并满足 §7 授权。

**F4.6.4** Branch 与普通 TASK 使用同一生命周期与 evidence gate，不存在 Branch 专用完成状态。

**F4.6.5** Root 存在 Branch 时，T7 还必须引用有效 convergence REVIEW：

```yaml
review_kind: convergence
subject_ref: ROOT-TASK-ID
family_digest: <sha256-lower-hex>
references: [REPORT-ID-A, REPORT-ID-B]
```

**F4.6.6** `family_digest` 的输入是归档提交点的 Root ID，以及全部现存 Branch 的 `(branch_task_id,current_attempt_id,current_report_id,current_report_digest)`；按 branch_task_id 升序，使用 §8.4 canonical JSON 后 SHA-256。Root 自身不是 Branch，但其 ID 必须进入摘要域。

**F4.6.7** convergence references 必须恰好覆盖每个 Branch 当前有效 REPORT，可额外引用 Root 当前 REPORT；缺失、陈旧或额外引用其他 attempt 的报告均返回 `FAMILY_CONVERGENCE_MISMATCH`。

**F4.6.8** 新建 Branch、T5/T6 reopen Branch、或产生合法 replacement REPORT 都改变 family digest，旧 convergence 自动失效。T7 必须在同一 family 线性化边界内重新计算。

## 7. C6 · 持久授权与信任边界

**F4.7.1** Authorization 由追加式 REVIEW 承载，不是第五类信封。`review_kind: authorization` 至少包含：

```yaml
subject_ref: TASK-ID
decision: authorize
operation_kind: lifecycle_transition
transition: {from: done, to: archive}
authorization_scope: single_use
issued_at: <date-time>
expires_at: <date-time-or-null>
attempt_id: <id-or-null>
family_digest: <digest-or-null>
references: []
```

**F4.7.2** acceptance/rejection/convergence REVIEW 若包含同等绑定字段并由 Profile 认可的签发者生成，可同时作为授权依据；否则必须引用独立 authorization REVIEW。

**F4.7.3** Core 只验证：对象存在且是 REVIEW、decision 有效、subject/transition/attempt/family 绑定匹配、时间有效、single-use 未被其他 transition 消费。失败分别返回 `AUTHORIZATION_REQUIRED`、`AUTHORIZATION_INVALID`、`AUTHORIZATION_EXPIRED`、`AUTHORIZATION_REUSED`。

**F4.7.4** Profile 判断 sender 是否有签发权。Profile 缺失或不能证明权力时 Fail Closed；Core 不内置 ADMIN/PM/QA 等角色。

**F4.7.5** 消费授权的 transition 必须持久写 `authorization_ref`。调用参数 `actor`、Host allowlist、UI 按钮或 REPORT 结论均不能替代授权事实。

## 8. C7 · 创建 TASK 的持久幂等

**F4.8.1** 4.0 首版强制幂等范围仅为创建 TASK（含 Branch）。查找键固定为：

```text
workspace_id + operation_kind + operation_id
```

比较值固定为 `normalized_request_digest`。`operation_kind` 对普通/Branch 创建均为 `create_task`；branch_of 是摘要字段，不另设命名空间。

**F4.8.2** `operation_id` 是 1–128 字符 `[A-Za-z0-9][A-Za-z0-9._:-]*`。实现必须原子保留查找键；不得只靠内存或无并发保护地扫描 TASK。

**F4.8.3** 同键同摘要返回 `Existing` 与原 `task_id/path/digest`，不得新建文件/事件；同键异摘要返回 `OPERATION_ID_CONFLICT`；不同 operation kind 互不冲突。重启后结果相同。

**F4.8.4** create-task 摘要输入固定为 canonical JSON 对象：`contract="fcop-create-task-v1"`、workspace_id、operation_kind、operation_id、sender、recipient、subject、body、priority（应用默认后）、parent、branch_of、references。字符串 Unicode NFC；CRLF/CR 转 LF；body 末尾规范为恰好一个 LF；空值为 JSON null；references 去重后按代码点升序；对象键升序、无多余空白、UTF-8 编码；摘要为小写 SHA-256。时间戳、分配后的 task_id/path、thread_key、risk_level 和 Profile 扩展不进入摘要。

**F4.8.5** durable operation fact 的物理布局由 Encoding 决定，但必须可审计、可在重启后查找且不成为 NOW 第二真相。结果 TASK 必须复写 operation_id/kind/digest，重复或冲突记录必须 Fail Closed。

## 9. C8 · 原子操作、重复与恢复

**F4.9.1** 规范不宣称跨目录迁移没有中间状态。实现必须将可观察结果归类为：`NOT_COMMITTED`、`COMMITTED`、`RECOVERABLE_DUPLICATE`、`DIVERGENT_DUPLICATE`、`INDETERMINATE`。

**F4.9.2** 不得静默覆盖 destination。存在相同 canonical 内容且有同 operation evidence 时可返回 Existing/Recoverable；不同内容返回 `TARGET_ALREADY_EXISTS_DIFFERENT`。

**F4.9.3** 同一 TASK 在多个权威阶段出现时，读取者必须 `STATE_AMBIGUOUS` 并 Fail Closed，不得按 mtime、目录顺序或 event 回放猜测 NOW。

**F4.9.4** 恢复判断必须使用持久 operation identity、normalized/content digest、source/destination 路径和追加式 receipt。修复必须幂等并追加 repair REVIEW 或等价可审计 receipt；分歧/损坏时返回 `RECOVERY_REQUIRED`，保留所有副本。

**F4.9.5** Branch 创建、Branch T5/T6、convergence 创建和 Root T7 必须共享 Root family 级线性化边界。每个提交点都重新验证 Root stage、Branch 集合、attempt/report heads、family digest 和 authorization。

**F4.9.6** lock/receipt/index 的文件路径是 Encoding/Toolkit 细节，不是业务 envelope。遗留锁不得按年龄静默删除；无法证明安全释放时 `LOCK_RECOVERY_REQUIRED`。

**F4.9.7** Base 承诺仅覆盖具有可靠本地语义的受支持 NTFS/POSIX 文件系统。跨设备、网络盘、分布式/弱一致文件系统无外部一致性层时返回 `UNSUPPORTED_FILESYSTEM` 或 Fail Closed。

## 10. 错误与 Fail Closed

**F4.10.1** 规范错误代码至少包括：

| 域 | 稳定错误代码 |
|---|---|
| workspace | `WORKSPACE_ID_MISMATCH`, `WORKSPACE_ID_CLONE_CONFLICT`, `UNSUPPORTED_PROTOCOL`, `UNSUPPORTED_WORKSPACE_VERSION`, `UNSUPPORTED_ENCODING` |
| envelope/relation | `INVALID_ENVELOPE`, `RELATION_INVALID`, `REFERENCE_UNRESOLVED`, `BRANCH_DEPTH_EXCEEDED`, `ROOT_NOT_ACTIVE` |
| evidence | `REPORT_REQUIRED`, `REPORT_HEAD_AMBIGUOUS`, `ATTEMPT_MISMATCH`, `REVIEW_REQUIRED`, `FAMILY_CONVERGENCE_REQUIRED`, `FAMILY_CONVERGENCE_MISMATCH` |
| authorization | `AUTHORIZATION_REQUIRED`, `AUTHORIZATION_INVALID`, `AUTHORIZATION_EXPIRED`, `AUTHORIZATION_REUSED` |
| idempotency | `OPERATION_ID_CONFLICT` |
| state/recovery | `LEGACY_TRANSITION_NOT_ALLOWED`, `TARGET_ALREADY_EXISTS_DIFFERENT`, `STATE_AMBIGUOUS`, `RECOVERY_REQUIRED`, `LOCK_RECOVERY_REQUIRED`, `UNSUPPORTED_FILESYSTEM` |

**F4.10.2** 错误必须可机器识别并包含 operation/subject 引用；不得把自由文本当唯一错误合同。

## 11. v3 兼容、Toolkit、MCP 与 Profile

**F4.11.1** v3 workspace 在显式迁移前仍按 v3 读取；4.0 写入不得在缺少 §2 声明时发生。迁移不在本候选规范中授权。

**F4.11.2** `finish_task` 与四个 history 工具是 `LEGACY_V3_ONLY`。4.0 workspace 的 history read 可作为 Legacy Toolkit；archive-to-history 移动权威 TASK 必须拒绝。

**F4.11.3** `fcop` 是参考 Toolkit，`fcop-mcp` 是可选 Adapter。45 个现有工具、11 个静态资源、3 个模板不构成 Core；保留名称的行为必须按 workspace version 分派并在不能安全兼容时 Fail Closed。

**F4.11.4** Branch 可由 create TASK + branch_of 表达，不要求新增 MCP 工具。`close_issue` 是下游 catalog 漂移，不属于官方表面。

**F4.11.5** MCP 基础适配应为薄 stdio；Relay 是可选扩展（候选包装 `fcop-mcp[relay]`），不进入 Core。upgrade/redeploy/GAL/workspace/session 等均为 Toolkit/Profile/Runtime。

## 12. 安全、符合性与发布门

**F4.12.1** 实现必须验证 workspace 边界、拒绝路径穿越、使用 UTF-8/LF、保留未知/失败证据并避免泄露 Profile/Runtime 凭据。

**F4.12.2** WP2 必须至少验证 C1–C8 各一项正常、拒绝以及适用的并发/恢复场景，并覆盖六个 WP0 原子/Branch 场景。

**F4.12.3** Schema、规范和测试冲突时必须阻止发布；不得静默选择任一方。任何宣称 4.0 conformance 的实现必须通过同一可观察合同。

**F4.12.4** 本文件在 `FCOP_4_CONTRACT_FROZEN` 前仅为 Candidate；它不授权 Schema、测试、实现、迁移、push 或发布。

## 13. C1–C8 不变量摘要

| Core | 不变量 |
|---|---|
| C1 | 每个可写 workspace 有唯一稳定 ID 和显式 protocol/Encoding/Profile |
| C2 | 只有四类正式 envelope；REPORT/ISSUE/REVIEW 追加事实 |
| C3 | 路径是 NOW；只有七边；archive 终态；无 active→done |
| C4 | 只有四种关系；Branch sibling-only；强关系 Fail Closed |
| C5 | 每次 active 新 attempt；当前 REPORT/acceptance；family 收敛可验证 |
| C6 | 授权是持久 REVIEW 引用；Core 验绑定，Profile 验签发权 |
| C7 | create TASK 以固定 key+digest 持久幂等 |
| C8 | 不覆盖、不猜测；重复可分类；恢复有证据；family 线性化 |
