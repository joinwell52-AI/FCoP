# FCoP 4.0 原子性与 Branch 竞态审计

> 基线：`origin/main@68dbeb15f4e7f84e1d03f907be9fa66c2265843e`
> 范围：只读建模；未实现 Branch、锁、repair 或 fault injection

## A. 当前迁移实现

`src/fcop/lifecycle/atomic.py` 的 `commit()` 是事实入口。正常路径顺序固定为：校验 → 读源 → 内存追加 event → 目标目录 O_EXCL 创建临时文件 → write/flush/file-fsync → `os.replace(tmp,destination)` → `source.unlink(missing_ok=True)`。

| 项目 | 真实代码位置 | 当前行为 | 崩溃后磁盘事实 | 是否可自动判定 | 证据 |
|---|---|---|---|---|---|
| 源读取 | `atomic.py:167-182` | 检查 source exists，再 UTF-8 读取并在内存追加 event | 读取前/中退出时 source 通常仍在；非 UTF-8 直接失败 | 部分；可看 source，但无 operation receipt | `test_atomic.py:272-283` 只测 source missing |
| 目标临时写入 | `atomic.py:184-193` | destination 目录下随机 `.fcop-*.tmp`，O_EXCL；file flush+fsync | 受控异常会删 tmp；进程/机器崩溃可留 orphan tmp | 可扫描命名，但不能证明对应 operation | 成功后无 tmp 测试 `test_atomic.py:168-181` |
| 目标提交 | `atomic.py:195-199` | `os.replace(tmp,destination)` | 提交前：source + 可能 tmp；提交后：source + destination，直到 unlink | 路径可见，但无法判定哪个副本获胜/是否同请求 | happy-path tests；无 replace fault injection |
| 源删除 | `atomic.py:201-202` | 目标提交后单独 unlink source | 在 replace 后、unlink 前崩溃产生双副本 | 可发现重复 task_id，但当前 commit 不处理 | 无对应故障测试 |
| 目录/文件 fsync | `atomic.py:187-190` | 只 fsync 临时文件 | rename/unlink 的目录项持久化未显式保证 | 否；崩溃恢复无 durable receipt | 代码审计 |
| 重复检测 | `create:266-267` 仅预检 create target；`commit` 无 destination 预检 | create 重复报 FileExists；commit 的 replace 可覆盖目标 | 并发 TOCTOU 或已有目标可被覆盖 | 不比较内容/digest，不能安全判同/判异 | `test_atomic.py:120-132` 只覆盖 create 已存在 |
| 显式修复 | 全仓库未发现 lifecycle repair API | 审计/人工可看异常，但无稳定修复状态机 | tmp、双副本、部分 history 迁移需人工判断 | 否 | 代码和 45-tool snapshot 审计 |

### 当前声明与实现差异

`ADR-0036 §4.1` 把“tmp→destination rename”描述为前后没有中间状态，但其伪代码与实现都在 rename 后另行 unlink source。严格说，原子的是**目标目录项替换**，不是“一个 TASK 从源桶消失并在目标桶出现”的复合状态变更。当前 claim 为 `OVERSTATED`。

## B. 故障点

| 场景 | 前置磁盘状态 | 故障点 | 允许结果（4.0 候选） | 禁止结果 | 当前实现 | 4.0 候选合同 |
|---|---|---|---|---|---|---|
| 目标写入前退出 | source 唯一存在 | temp create/write 前 | 明确 NotCommitted；重试同 operation 安全 | event 已生效但无目标/receipt | source 保持；可能无 tmp | 查持久 operation record；相同摘要重试 |
| 目标写入后源删除前退出 | source 存在，tmp/目标正在提交 | replace 后、unlink 前 | Committed 或 RecoverableDuplicate，且能机械选 canonical | 两个位置都被当作 NOW | 会留下 source+destination | 以 transaction/operation evidence 判 winner，repair 幂等 |
| 源删除后响应丢失 | destination 唯一存在 | unlink 后、返回前 | 重试返回 Existing/Committed 同一 object | 创建第二对象或报不可恢复 missing source | 再次 commit 从旧 source 查找会 missing；上层无 operation lookup | lookup key 找到既有结果 |
| 目标已存在且相同 | source + 相同 destination | commit replace | 返回 Existing 并安全收敛为一个 canonical | 再追加重复 transition 或覆盖审计历史 | 会 replace 目标并可能重复事件 | 内容比较基于 normalized digest，不按字节猜测语义 |
| 目标已存在且不同 | source + 不同 destination | commit replace | 稳定 conflict，保留双方，不自动删 | 静默覆盖任一事实 | `os.replace` 覆盖 destination | fail closed，返回 stable conflict code |
| 源目标同时存在且相同 | duplicate | 进入恢复 | 依据 operation evidence 删冗余副本，重复 repair 无害 | 两副本持续作为两个 NOW | 无 repair | `RECOVERABLE_DUPLICATE_SAME` + durable receipt |
| 源目标同时存在且不同 | divergent duplicate | 进入恢复 | quarantine/fail closed，需显式授权选择 | 自动覆盖/删除造成证据丢失 | 下一次 commit 可能覆盖目标 | `DIVERGENT_DUPLICATE`，两份 hash/路径写入 ISSUE/repair fact |

history 另有独立部分提交窗口：`Project.archive_to_history` 在 `project.py:2917-2954` 先移动 TASK，再扫描并移动 REPORT。任一步失败都没有 rollback/receipt；同名 destination 已存在时 TASK `replace` 可覆盖，REPORT 则因 `if not dest.exists()` 被跳过，行为不一致。

## C. 六个必查并发/故障场景（6/6）

| # | 场景与前置状态 | 操作 A | 操作 B/故障 | 必须串行化对象 | 线性化点候选 | 允许结果 | 禁止结果 | 恢复证据 |
|---:|---|---|---|---|---|---|---|---|
| 1 | active Root；同一 `operation_id` 尚无 Branch | create-branch request 1 | 同 operation_id 的 create-branch request 2 | operation identity + Root family | 持久映射首次 create-if-absent 提交 | 同摘要两者返回同一 Branch；异摘要一方成功、一方 `OPERATION_ID_CONFLICT` | 两个不同 Branch | operation record 含 key、digest、result TASK id |
| 2 | active Root，尚无新 Branch | 创建 Branch | archive Root | TASK family | 对 family generation/revision 的 compare-and-commit | 一方先提交，另一方重读后拒绝或按新状态执行 | 已归档 Root 下事后出现 Branch；漏收敛归档 | family commit fact + root/branch path snapshot |
| 3 | active Branch 当前 attempt 尚无 REPORT | 写当前 attempt REPORT | Branch move-to-done/submit | Branch TASK + attempt | REPORT 文件 durable commit 后，transition CAS 验证引用 | REPORT 先提交，done 引用它；或 done 拒绝等待 | done Branch 无当前轮 REPORT；旧 REPORT 复用 | REPORT subject/attempt ref + transition ref |
| 4 | Root 有 N 个 Branch，尚无有效收敛 | 写 convergence REVIEW | archive Root；期间可能新增/重开 Branch | Root family generation | convergence 绑定 generation 和完整 branch/report set；archive CAS 同 generation | REVIEW 覆盖提交点全部 Branch 后 archive | 旧 REVIEW 覆盖 N-1；新增 Branch 后仍有效 | structured review_kind/subject/references + generation |
| 5 | 任一 TASK transition | 正常 temp/write/replace/unlink | 进程在提交点前或后崩溃/响应丢失 | operation identity + TASK | 需 WP1 定义 committed record 与目录项哪个先/后 | 重试可机械返回 NotCommitted/Existing/Recoverable | 重试产生新 TASK/event 或无法判定 | durable operation receipt、source/destination hash |
| 6 | source/target 可能双存或任一损坏 | recovery scan/repair | 并发重试/人工检查 | TASK identity + operation identity | 先 claim repair lease/lock，再基于证据单次提交 repair fact | same 可收敛；different/corrupt quarantine 并 fail closed | 以 mtime/路径猜测、静默删除/覆盖 | 两副本 bytes/hash、transaction record、repair REVIEW/ISSUE |

当前实现对六项均没有完整合同：场景 5 的正常路径有局部 primitives，场景 6 可由人工观察，但不存在 Base Core 级稳定结果。上述“线性化点候选”是 WP1 输入，不是已冻结设计。

## D. 稳定身份与摘要

### D.1 当前事实

- 没有 `operation_id` 参数、持久 lookup 表或 operation fact 文件；
- 没有 `normalized_request_digest`；
- TASK 序号与 O_EXCL 只防单个 canonical 文件名碰撞，进程重启后不能把重试关联到旧结果；
- 临时文件名是随机实现细节，不能作为协议身份。

### D.2 WP1 必须冻结的候选模型

```text
查找键：workspace_id + operation_kind + operation_id
保存比较值：normalized_request_digest
同键同摘要：Existing(existing_object_ref)
同键异摘要：OPERATION_ID_CONFLICT
```

`normalized_request_digest` 应只覆盖会改变语义结果的请求字段，例如目标 workspace、operation kind、sender/recipient、subject/body、规范化 relations 和显式 options；不得包含生成时间、随机 temp 名、分配后的 TASK 序号或响应时间。确切字段清单必须在 WP1 按 operation kind 冻结。

规范化候选要求：UTF-8、LF、Unicode normalization 形式、mapping key 确定排序、list 顺序语义逐字段定义、路径转 workspace-relative `/`、禁止 `..`/外部绝对路径；正文末尾换行与空白规则必须明确。不能简单对原始 JSON/YAML bytes 求 hash。

进程重启后必须从 workspace 内 durable、可审计且不充当第二 NOW 的 operation facts/index 查找既有结果。索引可派生，但 canonical operation fact 必须可恢复。临时锁/事务文件只表达进行中实现状态，不得成为 TASK/REPORT/REVIEW/ISSUE 之外的业务事实；遗留锁必须带 owner/expiry 或 repair 证据，并默认 fail closed，禁止只按年龄静默删除。

## E. 平台矩阵

| 平台/文件系统 | create | replace/rename | unlink | 锁机制候选 | 已有测试 | 风险 |
|---|---|---|---|---|---|---|
| Windows/NTFS | O_EXCL 可提供单路径排他创建 | `os.replace` 目标目录项替换；开放句柄/杀软可导致 PermissionError；不能把 replace+source unlink 视为一个原子操作 | 可能受共享模式/占用影响 | 同目录 lock file O_EXCL + durable operation fact；需 crash 测试 | 本次 1225 suite 在 Windows 通过；atomic tests 只有 happy path/invalid transition/create exists | 高：当前无 kill-point、双副本、占用文件、目录持久性测试 |
| Linux/local FS | O_EXCL；同 mount rename/replace 原子更新目录项 | 同 mount rename 原子，但 source unlink 仍是第二操作；断电持久性需目录 fsync | 单独系统调用 | O_EXCL/`flock` 仅作实现锁；canonical evidence 仍需文件事实 | 仓库有跨平台 CI 配置历史，但 WP0 未在 Linux fault-injection 实跑 | 高：当前合同把运行成功测试外推为崩溃原子性 |

distributed/network filesystem、跨挂载点、多 host concurrent writers 当前不应默认为安全。`spec/fcop-3.0-spec.md:86-93` 已要求外部一致性层；4.0 兼容声明需明确支持/排除的文件系统与 consistency model。

## F. 现有测试覆盖差距

`tests/test_lifecycle/test_atomic.py` 覆盖 create、target-exists(create only)、合法/非法边、source missing、happy path 和成功后无 tmp；没有对 `commit` 的 destination-existing、replace 后崩溃、unlink 失败、响应丢失、目录 fsync、并发、重启、repair、Windows open-handle 或 family race 做 fault injection。`test_project_v3_writes.py` 明确把 inbox 一键 archive full chain 当作当前行为测试，这证明现状，不证明它符合 4.0 候选。

## G. WP0 结论

```text
CURRENT_ATOMICITY_CLAIM: OVERSTATED
DUPLICATE_TASK_WINDOW: YES
TASK_FAMILY_LINEARIZATION_AVAILABLE: NO
RECOVERY_CONTRACT_READY_FOR_WP1: NO
ATOMICITY_SCENARIOS: 6/6
BLOCKERS: operation identity/digest; destination conflict semantics; compound-move commit point; directory durability; explicit repair; attempt binding; family generation/linearization; history authority model; platform support boundary
```

“不 ready”表示合同仍需 WP1 冻结，不阻断 WP0 作为事实审计完成；本轮没有创建测试、修改实现或模拟破坏性崩溃。
