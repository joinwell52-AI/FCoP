# FCoP 4.0 合同冲突登记

> 基线：`origin/main@68dbeb15f4e7f84e1d03f907be9fa66c2265843e`
> 状态：WP0 evidence only；不得在本轮修复
> 冲突总数：**30**

## 判定口径

“冲突”表示当前规范、Schema、实现、MCP、发行边界或候选合同之间存在不一致/未定义面；不等于已确定修复方案。所有处置均为 WP1 待决，`FCOP_4_CONTRACT_FROZEN=false`。

严重度：P0 会阻断可验证的 4.0 Core 或安全发布；P1 会造成兼容、审计或恢复歧义；P2 为分层/文档一致性问题。

## 冲突表

| # | 严重度 | 冲突 | 当前证据 | 影响合同 | WP1 必须唯一化的问题 |
|---:|---|---|---|---|---|
| 1 | P1 | current spec 版本落后 | `spec/fcop-v3-spec.md:1-8` 仍为 3.2.4/rules 3.2.3；包和 bundled rules 已是 3.2.5 | Specification | 3.2.5 事实由哪个规范文件完整定义，4.0 supersede 起点是什么 |
| 2 | P0 | Schema “唯一真相”与当前协议脱节 | `spec/schemas/README.md` 声称 v1.0 SSOT；8 个 schema 实际混合 1.0/1.1，未编码 v3 lifecycle/history | C2/C3/C4/C6 | 4.0 Schema、正文规范、参考实现的优先级与同版本发布规则 |
| 3 | P0 | Workspace 无稳定协议身份 | 当前主要靠项目路径与 `fcop.json`；没有规范化 `workspace_id` | C1/C7 | workspace manifest 的必填字段、编码版本、迁移与复制语义 |
| 4 | P0 | 四类 envelope 的 Schema/模型不闭合 | IPC schema 开放扩展；TASK/REPORT/ISSUE/REVIEW 当前字段各自演进 | C2 | 四类正式文件的最小必填字段和未知字段兼容策略 |
| 5 | P0 | 关系词汇未统一 | TASK 当前有 `parent/thread_key/references`；候选需要 `parent/branch_of/subject_ref/references`；Schema 未覆盖完整语义 | C4 | 强关系、弱关系、方向、合法目标与循环检测 |
| 6 | P0 | history 与“路径定义状态”冲突 | `spec/fcop-v3-spec.md:150-188` 把 history 置于 lifecycle 外；权威 TASK 会移出 archive | C3/C8 | history 是导出副本、archive 分片 Encoding，还是 v4 禁用 |
| 7 | P0 | history 迁移不是 task+evidence 原子提交 | `project.py:2917-2954` 先移 TASK，再逐份移 REPORT；REVIEW 不移动 | C5/C8 | 配对集合、提交点、失败结果与恢复凭据 |
| 8 | P1 | history “不可变”仅为约定 | `read_history_*` 只读，但普通文件仍可被外部/代码改写；无 hash/freeze enforcement | C6/C8 | Core 要保证逻辑不可变还是只规定合法 API 不得改写 |
| 9 | P0 | `archive_task` 跨级 | `_v3_archive_chain` 可从 inbox/active/review 自动经过多条边至 archive（`project.py:5202-5219`） | C3/C5/C6 | archive 是否只能接受 done，旧一键语义如何兼容 |
| 10 | P0 | Branch 候选需要 `done → active`，当前无此边 | 当前七边见 `transitions.py:69-76` | C3/C4 | 是否加入受授权 reopen；旧 REPORT/REVIEW 如何失效 |
| 11 | P0 | `active → review` 不强制当前轮 REPORT | `submit_task` 只校验 stage 并 commit（`server.py:1627-1678`） | C5 | 所有 TASK 的 submit gate 与 REPORT attempt 绑定 |
| 12 | P0 | `active → done` 不强制 REPORT | `finish_task` 直接 commit（`server.py:1685-1737`） | C5 | 是否保留该边；若保留，最低 evidence gate |
| 13 | P0 | `active → done` 无持久授权 | `finish_task(actor=...)` 只有自报 actor | C6 | 明确 `authorization_ref`、绑定范围、复用规则与 Profile 验签 |
| 14 | P0 | approve/reject 的授权只是调用参数 | 默认 actor=`ADMIN`，Core 不验证签发事实（`server.py:1744-1804`） | C6 | transition authorization 文件/字段、主体与防冒用规则 |
| 15 | P0 | archive 没有 actor/授权引用 | `Project.archive_task(filename_or_id)` 无 actor；helper 写 `by: archiver`（`project.py:5170-5177,5230-5238`） | C6 | archive authority 的 durable evidence 与调用接口 |
| 16 | P0 | archive 不检查闭合条件 | 无当前轮 REPORT、正式 REVIEW、open ISSUE、child/branch/convergence gate | C3/C4/C5/C6 | 普通 TASK 与 family archive admission |
| 17 | P0 | REPORT 未绑定当前执行轮次 | `write_report` 仅以 `task_id` 关联；reject/reopen 后旧报告仍可被找到 | C5 | `attempt_id` 或 transition ref、最新轮判定、历史报告失效 |
| 18 | P0 | 收敛 REVIEW 缺机器可识别结构 | `write_review` 有 subject_ref，但无 `review_kind` 与 `references` | C4/C5 | convergence 最小 Encoding、branch 覆盖证明和引用集合 |
| 19 | P1 | ISSUE 缺标准 subject_ref | `Project.write_issue` 只有 reporter/summary/body/severity | C2/C4 | ISSUE 是否必须绑定 TASK/REPORT/REVIEW 或允许 workspace 级问题 |
| 20 | P0 | `mark_human_approved` 改写历史 REVIEW | `project.py:3985-4003` 原地重写同一文件 | C6 | 人工决定必须落新 REVIEW/authorization fact；旧文件保持字节不变 |
| 21 | P0 | transition 没有授权引用 | event 只含 `at/from/to/by/tool` + note/supersedes（`events.py:102-128`） | C6 | `authorization_ref` 放在 event 还是独立事实；完整性检查方式 |
| 22 | P0 | create 没有持久 operation identity | 当前 O_EXCL/递增序号只能避免单次文件碰撞 | C7 | 查找键 `workspace_id+operation_kind+operation_id` 的持久位置 |
| 23 | P0 | 没有 request digest/稳定冲突结果 | 无 normalized digest、Existing 返回或 `OPERATION_ID_CONFLICT` | C7 | 规范化字段、路径/换行/顺序/时间处理与错误对象 |
| 24 | P0 | 迁移存在双副本崩溃窗口 | `atomic.py:196-202` 目标 replace 后才 unlink source | C8 | 成功/失败/可恢复的允许磁盘状态与恢复判定 |
| 25 | P0 | 目标存在时可能被静默覆盖 | `commit` 未预检/比较 destination，使用 `os.replace` | C7/C8 | 相同内容返回 Existing；不同内容 fail closed；禁止覆盖 |
| 26 | P0 | 持久性与修复合同缺失 | 只 fsync 文件，不 fsync 目录；进程崩溃可遗留 tmp；无显式 repair API | C8 | Windows/NTFS、Linux/local FS 的承诺范围、锁遗留与 repair |
| 27 | P0 | Branch 身份与创建准入未实现 | 无 `branch_of`、active-root gate、sibling-only/深度检查 | C3/C4/C7 | 各 root stage 的准入表与 create-branch 幂等合同 |
| 28 | P0 | TASK family 无线性化与收敛失效 | 无 family lock、覆盖快照、branch 新增/重开后旧 convergence 失效规则 | C5/C7/C8 | family 串行对象、提交点、generation/revision 与恢复证据 |
| 29 | P1 | MCP 下游 catalog 漂移 | FCoP snapshot/server 45；CodeFlowMu `fcop-mcp-catalog.ts` 46，唯一额外 `close_issue`；filter/SDK 仍标称 45 | Toolkit/Profile | `close_issue` 明确为 `DOWNSTREAM_CATALOG_DRIFT`，不得反向进入 canonical |
| 30 | P0 | v4 发布/适配边界未设门 | MCP 依赖 `fcop>=3,<4` 且 relay websockets 必装；任意 `v*` tag 触发 token 发布；无 tag ruleset、required checks、PyPI environment 或 Trusted Publishing | Toolkit/Release | v4 lockstep/兼容范围、relay extra、签名 tag/gate、OIDC/environment/required checks |

## 交叉冲突关系

- #6–#8 共同说明：history 不是简单的“第六桶”，而是权威路径、证据集合和恢复语义的联合决定。
- #9–#16 共同说明：当前工具文案中的治理建议没有被 Core 机械执行，不能作为 4.0 合同证据。
- #17–#21 共同说明：存在文件并不等于当前轮证据有效，actor 字符串也不等于授权。
- #22–#28 共同说明：Branch 不能只加字段；它依赖持久幂等、family 线性化、可判定恢复和收敛失效。
- #29–#30 属于适配/发行面，不应被吸收到 Base Core，但必须在 4.0 兼容与发布计划中有显式处置。

## Gate 判定

```yaml
CONTRACT_CONFLICTS: 30
UNRESOLVED_IN_WP0: 30
WP0_BLOCKED_BY_CONFLICTS: false
WP1_DECISIONS_REQUIRED: true
FCOP_4_CONTRACT_FROZEN: false
IMPLEMENTATION_AUTHORIZED: false
```

这些冲突是 WP0 的预期产物，不阻断 `BASELINE_VERIFIED` 对“审计完整性”的确认；它们会阻断任何未经 WP1 冻结的实现。
