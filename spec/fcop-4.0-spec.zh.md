# FCoP 4.0 候选规范（中文）

> **状态：Candidate · Not Implemented · Not Released**
>
> WP1.1 合同版本：`4.0.0-candidate.2`；基线 `68dbeb15f4e7f84e1d03f907be9fa66c2265843e`；WP0 证据 `c259bebdad77122d24dc18a6dd3f8fe191e4042f`；WP1 输入 `1b50f9e1fd4d2d21002bb1b98e14fd903a050f07`。在 ADMIN 签署 `FCOP_4_CONTRACT_FROZEN` 并完成后续实现/发布前，FCoP 3.2.5 仍是现行协议。

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

**F4.2.3** `profiles` 是以 JSON 数组表示的已采用 Profile 标识符集合。数组顺序不产生授权优先级或 Core 语义。`profiles: []` 合法，但该工作区只能执行不要求授权的 Base 操作。团队、角色、leader 等 v3 字段可保留为 Profile 扩展，不得改变 Core 语义。

**F4.2.4** `workspace_id` 是协议身份，不是全球在线锁。备份或只读镜像可保留 ID。显式创建独立可写 fork/派生工作区的生产者必须在首次写入前生成新 ID；调用者强制保留 ID 时，该操作必须以 `WORKSPACE_ID_CLONE_CONFLICT` 拒绝，或明确创建只读镜像。同一 Toolkit、Runtime 或导入操作同时观察到两个独立可写工作区使用同一 ID 时，可以返回 `WORKSPACE_ID_CLONE_CONFLICT` 并 Fail Closed。

**F4.2.5** 不支持的 protocol/version/Encoding 分别返回 `UNSUPPORTED_PROTOCOL`、`UNSUPPORTED_WORKSPACE_VERSION`、`UNSUPPORTED_ENCODING`。

**F4.2.6** 单个离线工作区无法证明不存在不可见副本，FCoP 不作这种保证。外部 single-writer、同步复制和网络冲突发现属于 Runtime/部署环境，不进入 Core。

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

**F4.3.5** REVIEW kind 至少包括 `assessment`、`acceptance`、`rejection`、`reopen`、`authorization`、`convergence`、`repair`。`mark_human_approved` 若保留，只能追加 REVIEW，不得改写原 REVIEW。

## 4. C3 · 单一权威路径、生命周期与事件

**F4.4.1** 权威 TASK 必须且只能位于以下一个路径；目录位置是 NOW 唯一真相：

```text
fcop/_lifecycle/{inbox,active,review,done,archive}/TASK-*.md
```

**F4.4.2** Base 合法迁移固定为七条，完整 Gate 矩阵如下：

| 迁移 | 前置状态 | 必需 REPORT | 必需 REVIEW | 必需 Authorization Profile | 新 attempt |
|---|---|---|---|---|---|
| T1 `None -> inbox` | TASK 不存在 | 否 | 否 | 否 | 否 |
| T2 `inbox -> active` | 唯一 inbox TASK | 否 | 否 | 否；Profile 可增加政策 | 是 |
| T3 `active -> review` | 唯一 active TASK | 当前 attempt 唯一有效 REPORT | 否 | 否；Profile 可增加政策 | 否 |
| T4 `review -> done` | 唯一 review TASK | T3 已绑定的当前 REPORT | acceptance REVIEW | 是 | 否 |
| T5 `review -> active` | 唯一 review TASK | 被拒绝的当前 REPORT | rejection REVIEW | 是 | 是 |
| T6 `done -> active` | 唯一 done TASK | 否 | reopen/authorization REVIEW | 是 | 是 |
| T7 `done -> archive` | 唯一 done TASK | 不新增；沿用已接受 attempt 证据 | archive authorization；有 Branch 时还需 convergence REVIEW | 是 | 否 |

**F4.4.3** 一次命令只能提交一条边并追加一条 transition。跨多边便利调用必须拆分；任一步失败不得伪造后续事件。

**F4.4.4** `active -> done` 不属于 4.0 Base。`finish_task` 是 3.x Legacy；在 4.0 workspace 必须拒绝并返回 `LEGACY_TRANSITION_NOT_ALLOWED`，不得绕过 T3/T4。

**F4.4.5** transition 事件必含 `at/from/to/by/tool`；进入 active 时必含新 `attempt_id`。生命周期 Gate 每消费一份 REPORT 或 REVIEW，transition 都必须在等长对齐的 `evidence_ref` 与 `evidence_digest` 数组中记录引用和摘要；适用授权时还必须记录 `authorization_ref` 与 `authorization_digest`。摘要固定为文件字节经 UTF-8、LF 验证后的完整内容之小写 SHA-256。后来字节不一致时返回 `EVIDENCE_DIGEST_MISMATCH`。事件只追加，不能推导 NOW。

**F4.4.6** archive 是终态。权威 TASK 不得从 archive 移入 history 或返回 lifecycle。v3 history 只读识别为 Legacy；4.0 Toolkit 只能生成非权威冷存储副本。

**F4.4.7** §4.2 未列出的状态边返回 `INVALID_TRANSITION`。T7 的普通 closure 仅表示：TASK 位于唯一 done 路径、强关系有效、授权有效。Base 不把普通 parent child 或 ISSUE 状态设为 T7 门；Profile 可以增加这些政策，但不得产生隐藏 Base 迁移。

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

**F4.6.3** T4 必须引用 `review_kind: acceptance`、`decision: approved` 的 REVIEW；其 subject_ref/attempt_id 和 references 中的 REPORT 必须匹配当前状态，满足 §7 授权，并由 transition 记录 §4.5 要求的 REPORT、REVIEW、授权引用及字节摘要。

**F4.6.4** Branch 与普通 TASK 使用同一生命周期与 evidence gate，不存在 Branch 专用完成状态。

**F4.6.5** Root 存在 Branch 时，Root T7 必须在同一个 family 线性化边界内验证：Root 位于唯一 done 路径；Root 的 `branch_of` 为空；所有指向 Root 的 Branch 均位于 done 或 archive；每个 Branch 当前 attempt 有唯一有效 REPORT；每个 Branch 的完成均已通过自己的 T3/T4 证据与授权门；convergence 精确引用这些当前 Branch REPORT；convergence 的 `family_digest` 等于提交点重算值；Root T7 authorization 绑定该当前摘要。任一 Branch 非终态时返回 `BRANCH_NOT_TERMINAL`。convergence REVIEW 结构为：

```yaml
review_kind: convergence
subject_ref: ROOT-TASK-ID
family_digest: <sha256-lower-hex>
references: [REPORT-ID-A, REPORT-ID-B]
```

**F4.6.6** 每个 Branch 的 `report_digest` 固定为当前唯一有效 REPORT 文件经过 UTF-8/LF 验证后的完整字节之小写 SHA-256。`family_digest` 是以下唯一 canonical object 的小写 SHA-256：

```json
{
  "contract": "fcop-family-v1",
  "root_task_id": "TASK-...",
  "branches": [
    {
      "branch_task_id": "TASK-...",
      "attempt_id": "urn:uuid:...",
      "report_id": "REPORT-...",
      "report_digest": "<lowercase-sha256>"
    }
  ]
}
```

只收集 `branch_of` 指向该 Root 的全部 TASK；每个 Branch 取当前 attempt 与唯一有效 REPORT head；`branches` 按 `branch_task_id` 的 Unicode code point 升序；所有对象键递归按 Unicode code point 升序；使用 UTF-8、无 BOM、无末尾换行、无多余空白的 JSON。Branch 的 done/archive 状态由 T7 单独验证，不进入摘要。mtime、目录遍历顺序、Runtime 计数器和进程内 generation 均不得作为摘要输入。

**F4.6.7** convergence references 必须恰好覆盖每个 Branch 当前有效 REPORT，可额外引用 Root 当前 REPORT；缺失、陈旧、引用其他 attempt 的报告或 canonical digest 不一致均返回 `FAMILY_CONVERGENCE_MISMATCH`。对收敛覆盖而言，done 和 archive 都是 Branch 完成状态。

**F4.6.8** 新建 Branch、reopen Branch、生成新 Branch attempt 或产生合法 replacement REPORT 都会改变 canonical object 或 report digest，使旧 convergence 失效。Branch 的 T7 done→archive 只改变路径，不使其他方面仍匹配的 convergence 失效。Root T7 必须在同一 family 线性化边界内重新计算摘要。

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
profile_ref: <adopted-profile-id>
```

**F4.7.2** T4 acceptance 或 T5 rejection REVIEW 若包含包括 `profile_ref` 在内的全部授权绑定，且签发者证明被该 Profile 判定为 `AUTHORIZED`，可以同时作为授权依据；否则必须引用独立 authorization REVIEW。convergence 本身不能作为 Root T7 authorization。

**F4.7.3** Core 验证：对象存在且是 REVIEW；`profile_ref` 指向已采用 Profile；decision、subject、transition、attempt、family、时间、复用、证据引用和已存字节摘要均匹配。结构性失败按情况返回 `AUTHORIZATION_REQUIRED`、`AUTHORIZATION_INVALID`、`AUTHORIZATION_EXPIRED`、`AUTHORIZATION_REUSED` 或 `EVIDENCE_DIGEST_MISMATCH`。

**F4.7.4** `profile_ref` 指定的 Profile 必须把签发者及其证明判定为三值之一：`AUTHORIZED`、`DENIED`、`UNKNOWN`。只有 `AUTHORIZED` 通过；`DENIED` 与 `UNKNOWN` 均返回 `AUTHORIZATION_INVALID` 并 Fail Closed。T4/T5/T6/T7 没有可用的已采用授权 Profile 时返回 `AUTHORIZATION_PROFILE_UNAVAILABLE`。Core 不内置 ADMIN/PM/QA 等角色。

**F4.7.5** 消费授权的 transition 必须持久写 `authorization_ref` 与 `authorization_digest`。YAML `sender`、调用参数 `actor`、Host allowlist、UI 按钮或 REPORT 结论本身均不能证明签发权或替代授权事实。

**F4.7.6** Profile 可以采用本地单用户信任、OS ACL、签名或其他机制，但机制不进入 Core。FCoP 是治理与审计协议，不宣称仅凭可编辑文件提供密码学身份安全。

**F4.7.7** `profiles: []` 对 T1–T3 等无授权门的 Base 操作仍符合规范。普通开发者的最小可完成工作区必须在初始化时显式采用至少一个可用授权 Profile，但不得把任何固定角色变成 Core 要求。

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

**F4.9.1** 规范不宣称跨目录迁移没有中间状态。每个恢复观察必须唯一归类为 `NOT_COMMITTED`、`COMMITTED`、`RECOVERABLE_DUPLICATE`、`DIVERGENT_DUPLICATE` 或 `INDETERMINATE`；`INDETERMINATE` 绝不是成功兜底。

**F4.9.2** 不得静默覆盖 destination。创建 TASK 的外部幂等可按 §8.3 返回 `Existing`；生命周期迁移的同 receipt/digest 重复按 §9.9 恢复分类处理，不产生公共重放承诺；不同内容返回 `TARGET_ALREADY_EXISTS_DIFFERENT`。

**F4.9.3** 同一 TASK 在多个权威阶段出现时，读取者必须 `STATE_AMBIGUOUS` 并 Fail Closed，不得按 mtime、目录顺序或 event 回放猜测 NOW。

**F4.9.4** 每个生命周期迁移的内部恢复都使用持久 Toolkit/Encoding operation receipt，其中包含 operation identity、source/destination 路径、normalized/content digest 和阶段。机械恢复必须幂等，不得创建第二个 TASK、同一提交的第二条 event 或静默覆盖。分歧或不可证明的损坏返回 `RECOVERY_REQUIRED`，并保留每个可见副本。

**F4.9.5** 同一 Root family 中，所有会改变 Root 生命周期状态、Branch 集合、任一 Branch 生命周期状态/当前 attempt/当前 REPORT head、convergence REVIEW 或 Root archive 条件的写操作必须共享一个线性化边界。至少覆盖 Branch create、Root T2–T7、Branch T2–T7、Branch REPORT create/replacement、convergence REVIEW create/replacement 和 Root T7。每个操作取得边界后必须重新读取并验证 Root 状态、Branch 集合、attempt、REPORT head、摘要和授权，不得用加锁前缓存提交。边界只串行化短暂协议提交，不锁住 Agent 实际工作，也不串行化无 `branch_of` 的普通 TASK。

**F4.9.6** lock/receipt/index 的文件路径是 Encoding/Toolkit 细节，不是业务 envelope。遗留锁不得按年龄静默删除；无法证明安全释放时 `LOCK_RECOVERY_REQUIRED`。

**F4.9.7** Base 承诺仅覆盖具有可靠本地语义的受支持 NTFS/POSIX 文件系统。跨设备、网络盘、分布式/弱一致文件系统无外部一致性层时返回 `UNSUPPORTED_FILESYSTEM` 或 Fail Closed。

**F4.9.8** Base 区分三种保证：

| 保证 | 4.0 Base 范围 | 身份 |
|---|---|---|
| 外部请求幂等 | 创建 TASK/Branch | 调用者提供 `operation_id` |
| 内部崩溃恢复 | 所有生命周期迁移 | Toolkit/Encoding 持久 operation receipt |
| 授权迁移响应丢失重试 | T4/T5/T6/T7 | 已消费 `authorization_ref` + digest + transition |

普通 T2/T3 没有公共 `operation_id` 时不承诺任意时间后的外部请求重放；其内部崩溃恢复仍必须避免第二个 TASK、第二条同一提交 event 或覆盖。

**F4.9.9** 逻辑 receipt 阶段固定为 `PREPARED`、`TARGET_DURABLE`、`COMMITTED`，具体文件名由 Encoding 决定。Base filesystem 恢复状态表唯一如下：

| source | target | receipt/摘要 | 分类 | 允许机械动作 |
|---|---|---|---|---|
| 存在且匹配 | 不存在 | 无 receipt 或 PREPARED | `NOT_COMMITTED` | 保留 source；可安全放弃本次操作 |
| 存在且匹配 | 存在且同摘要 | TARGET_DURABLE | `RECOVERABLE_DUPLICATE` | 验证后删除 source、持久化目录、完成 receipt |
| 不存在 | 存在且匹配 | TARGET_DURABLE 或 COMMITTED | `COMMITTED` | 补全 COMMITTED receipt；不得重做迁移 |
| 存在 | 存在且摘要不同 | 任意 | `DIVERGENT_DUPLICATE` | 不删除、不覆盖；要求人工裁定 |
| 均不存在，或 receipt/身份/摘要损坏冲突 | 不可证明 | 任意 | `INDETERMINATE` | 保留全部可见证据并 Fail Closed |

**F4.9.10** 机械可证明的 `RECOVERABLE_DUPLICATE` 只追加/补全 operation receipt，不创建业务 REVIEW。`DIVERGENT_DUPLICATE` 或 `INDETERMINATE` 需要人工裁定时使用 `review_kind: repair` REVIEW。receipt 不是 envelope、NOW 真相或 Runtime 数据库。故障注入测试针对抽象阶段，不绑定 Python 函数或临时路径名。

**F4.9.11** T4/T5/T6/T7 响应丢失后，以相同授权重试时，若 `authorization_ref`、authorization digest、transition 和已存 evidence digest 全部匹配，则返回既有已提交结果；同一授权被不同 transition 消费时返回 `AUTHORIZATION_REUSED`；事实歧义时 Fail Closed。

## 10. 错误与 Fail Closed

**F4.10.1** Base 4.0 稳定错误注册表固定为以下 31 项：

| 域 | 稳定错误代码 |
|---|---|
| workspace | `WORKSPACE_ID_MISMATCH`, `WORKSPACE_ID_CLONE_CONFLICT`, `UNSUPPORTED_PROTOCOL`, `UNSUPPORTED_WORKSPACE_VERSION`, `UNSUPPORTED_ENCODING` |
| envelope/relation | `INVALID_ENVELOPE`, `RELATION_INVALID`, `REFERENCE_UNRESOLVED`, `BRANCH_DEPTH_EXCEEDED`, `ROOT_NOT_ACTIVE` |
| evidence | `REPORT_REQUIRED`, `REPORT_HEAD_AMBIGUOUS`, `ATTEMPT_MISMATCH`, `REVIEW_REQUIRED`, `FAMILY_CONVERGENCE_REQUIRED`, `FAMILY_CONVERGENCE_MISMATCH`, `EVIDENCE_DIGEST_MISMATCH` |
| authorization | `AUTHORIZATION_REQUIRED`, `AUTHORIZATION_INVALID`, `AUTHORIZATION_EXPIRED`, `AUTHORIZATION_REUSED`, `AUTHORIZATION_PROFILE_UNAVAILABLE` |
| idempotency | `OPERATION_ID_CONFLICT` |
| state/recovery | `INVALID_TRANSITION`, `BRANCH_NOT_TERMINAL`, `LEGACY_TRANSITION_NOT_ALLOWED`, `TARGET_ALREADY_EXISTS_DIFFERENT`, `STATE_AMBIGUOUS`, `RECOVERY_REQUIRED`, `LOCK_RECOVERY_REQUIRED`, `UNSUPPORTED_FILESYSTEM` |

**F4.10.2** 错误必须可机器识别并包含 operation/subject 引用；不得把自由文本当唯一错误合同。

**F4.10.3** Profile 与 Toolkit 扩展错误必须使用明确命名空间，不得替代、重定义或改变 Base 错误语义。

## 11. v3 兼容、Toolkit、MCP 与 Profile

**F4.11.1** v3 workspace 在显式迁移前仍按 v3 读取；4.0 写入不得在缺少 §2 声明时发生。迁移不在本候选规范中授权。

**F4.11.2** `finish_task` 与四个 history 工具是 `LEGACY_V3_ONLY`。4.0 workspace 的 history read 可作为 Legacy Toolkit；archive-to-history 移动权威 TASK 必须拒绝。

**F4.11.3** `fcop` 是参考 Toolkit，`fcop-mcp` 是可选 Adapter。45 个现有工具、11 个静态资源、3 个模板不构成 Core；保留名称的行为必须按 workspace version 分派并在不能安全兼容时 Fail Closed。

**F4.11.4** Branch 可由 create TASK + branch_of 表达，不要求新增 MCP 工具。`close_issue` 是下游 catalog 漂移，不属于官方表面。

**F4.11.5** MCP 基础适配应为薄 stdio；Relay 是可选扩展（候选包装 `fcop-mcp[relay]`），不进入 Core。upgrade/redeploy/GAL/workspace/session 等均为 Toolkit/Profile/Runtime。

## 12. 安全、符合性与发布门

**F4.12.1** 实现必须验证 workspace 边界、拒绝路径穿越、使用 UTF-8/LF、保留未知/失败证据并避免泄露 Profile/Runtime 凭据。

**F4.12.2** WP2 必须至少验证 C1–C8 各一项正常、拒绝以及适用的并发/恢复场景，并覆盖六个 WP0 原子/Branch 场景及 WP1.1 的 fork、Profile、证据摘要、family 竞态、幂等分层和五状态恢复合同。

**F4.12.3** Schema、规范和测试冲突时必须阻止发布；不得静默选择任一方。任何宣称 4.0 conformance 的实现必须通过同一可观察合同。

**F4.12.4** 本文件在 `FCOP_4_CONTRACT_FROZEN` 前仅为 Candidate；它不授权 Schema、测试、实现、迁移、push 或发布。

## 13. C1–C8 不变量摘要

| Core | 不变量 |
|---|---|
| C1 | 每个可写 workspace 有唯一稳定 ID；显式 fork 生成新 ID；不宣称可发现不可见离线副本 |
| C2 | 只有四类正式 envelope；REPORT/ISSUE/REVIEW 追加事实 |
| C3 | 路径是 NOW；只有七边；archive 终态；无 active→done |
| C4 | 只有四种关系；Branch sibling-only；强关系 Fail Closed |
| C5 | 每次 active 新 attempt；证据摘要；Branch 终态门；唯一 canonical family digest |
| C6 | 授权是持久 REVIEW+摘要；已采用 Profile 返回 AUTHORIZED/DENIED/UNKNOWN |
| C7 | create TASK 以固定 key+digest 持久幂等 |
| C8 | 三层幂等/恢复；五种恢复状态；不覆盖不猜测；完整 family 线性化 |
