# FCoP 4.0 WP4C.4：Host 薄投影、显式采用、部署收据与回滚任务书 v1.0

## 0. 文档身份与唯一授权

```yaml
document_role: EXECUTION_TASKBOOK
status: AUTHORIZED_FOR_WP4C_4_ONLY
execution_authorized: true
authorized_scope: WP4C_4_ONLY
accepted_wp4c_3_head: 4f56cfcf9754bb509b7bd353e830a8e4003810ea
wp4c_3_gate_commit: e24b16185dcd9b8746c26d08654c6ed285a2a8c7
frozen_fcop_contract: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
frozen_distribution_contract: f6831de12991010f22672fb6e776ce85ef1507ff
frozen_distribution_conformance: 1f4df9cc650f63b9e842d806340eb31b768f708e
taskbook_parent: e24b16185dcd9b8746c26d08654c6ed285a2a8c7
wp4c_5_authorized: false
main_merge_authorized: false
release_authorized: false
requested_gate_after_success: WP4C_4_HOST_PROJECTION_ACCEPTED
```

只有本文件在固定提交中的完整原始字节具有执行授权。PR 评论、摘要、旧 WP3C 总任务书、报告、聊天内容和 Gate 本身都不能扩大范围。执行前必须通过 GitHub 固定 ref 回读本文件，核对 commit、SHA-256、字节数、UTF-8、无 BOM、LF 和直接父提交；任一不一致立即停止。

## 1. 任务目标

在已验收的 WP4C.3 规则包之上，完成一个小而确定的文件工具层：

1. 校验固定静态 Host Profile；
2. 将已选择的 canonical guidance 确定性投影为 Host 入口字节；
3. 以 ADMIN 明确选择证据追加不可变 Adoption Receipt；
4. 提供严格零写入 `plan`；
5. 以短临界区、同目录暂存和原子替换执行 `apply`；
6. 追加 Deployment Receipt 和不可变备份；
7. 显式验证、失败检查和回滚；
8. 让冻结的 DIST-08—DIST-20 全部通过真实 `Project.rule_distribution` 入口。

本阶段不是 Host 准入系统，不是 Host Runtime，也不证明 Host 实际读取了文件。

## 2. 必须坚持的架构边界

实现必须保持：

> canonical 文件 + Manifest + 静态 Profile + 显式命令 → 确定性文件结果 + 追加收据

严禁新增：

- 数据库、Daemon、Watcher、Scheduler、后台线程、后台重试或自动恢复器；
- 网络请求、远程规则服务、自动下载、mutable latest 或包自动升级；
- Host 二进制发现、版本探测、模型探测、Subagent 探测、认证或权限探测；
- 全局 Adoption Registry、全局可变配置、第二 Runtime 或第二生命周期状态机；
- 自动采用、自动部署、自动回滚、启动时写入或文件存在即视为已采用；
- 修改 CodeFlowMu、当前 3.x 分发、MCP、Relay、FCoP Core 生命周期或冻结合同；
- 将 Host Profile 当作 F4.7 授权 evaluator；
- 新公共 facade。唯一公共入口仍是 `Project.rule_distribution(*, action, request)`。

允许增加少量私有模块，但每个模块必须只有一个职责。优先为：Profile/投影、Receipt、部署原子操作；不得建立通用框架或插件系统。

## 3. 固定输入与事实优先级

执行者必须完整读取：

1. `docs/fcop-4.0/rule-distribution-contract.md` 与 `.zh.md`；
2. `reports/FCOP-4.0-WP4C.1-CONFORMANCE-MATRIX.md`；
3. `reports/FCOP-4.0-WP4C.1-CONTRACT-DECISIONS.md`；
4. `tests/conformance/rule_distribution_v4/conftest.py`；
5. `test_dist_07_12_profiles.py`；
6. `test_dist_13_20_projection.py`；
7. WP4C.3 的实现、五份报告与 Manifest；
8. 当前既有原子写、锁、故障注入和路径安全工具，仅为复用审计，不得先假设适用。

事实优先级：冻结 FCoP 4.0 规范 > 冻结 RD 合同 > 冻结 Conformance > 本任务书的范围控制 > 既有实现与历史说明。

若前三者存在无法同时满足的语义冲突，必须先输出 `FROZEN_CONFORMANCE_CONTRACT_CONFLICT` 报告并停止；不得让实现偷偷决定合同。

## 4. 开工前 Implementability Proof

编码前先形成 `reports/FCOP-4.0-WP4C.4-IMPLEMENTABILITY-PROOF.md`，逐项证明：

- DIST-08—DIST-20 共 13 个 Test ID、53 个行为节点的现状；
- 当前已通过的 8 个负向节点与仍红的 45 个节点；
- 每个 action 到 RD 条款、错误码、读写路径和单一实现函数的映射；
- Adoption、plan、apply、verify、rollback 与失败恢复的线性化点；
- Windows/Linux/macOS 可用的文件原语与无法承诺的边界；
- 现有工具可复用清单，避免再造锁、JSON canonicalization 和安全路径逻辑；
- 所有物化窗口以及崩溃后的可证明状态。

Proof 中必须给出完整 53 行矩阵。若某节点只能靠修改冻结断言、跳过、xfail、信任调用者自声明或引入后台组件通过，立即停止。

## 5. 本阶段固定 action 面

仅允许在既有 `Project.rule_distribution` 内实现以下 action：

| action | 性质 | 允许效果 |
|---|---|---|
| `inspect_profile` | 只读 | 返回已校验静态 Profile 与独立事实字段 |
| `status` | 只读 | 分别报告 support/adoption/generated/consumption，不互相推导 |
| `adopt` | 写 | 只追加 Adoption Receipt |
| `plan` | 只读 | 返回确定性投影、diff、摘要、备份和回执计划 |
| `apply` | 写 | 按已验证计划部署并追加证据 |
| `verify_deployment` | 只读 | 验证目标、Profile、Manifest、快照和收据 |
| `rollback` | 写 | 只回滚紧邻已验证部署并追加回执 |
| `inspect_failure` | 只读 | 报告已持久化的部分失败事实，不重放 |
| `rollback_partial` | 写 | 对指定失败事实执行显式恢复 |

禁止再增加 action 或新的公开方法。`validate`、`select`、`validate_operation_scope` 必须保持 WP4C.3 行为不变。

### 5.1 错误边界裁决

`adopt` 的工作区身份、协议版本、ADMIN 选择证据、前序采用链或 Profile 不兼容，属于 RD-09 采用边界，必须按冻结测试返回 `toolkit:RULE_ADOPTION_REQUIRED` 且零写入。其他既有 Core/规则选择路径不得因此改写其 Base 错误。

该限定只解决 DIST-08 的既有成功合同，不授权全局捕获或重写 `WORKSPACE_ID_MISMATCH`、`UNSUPPORTED_WORKSPACE_VERSION`。

## 6. 静态 Host Profile

必须支持冻结的三个候选 Profile：

| host_id | target | entry kind | initial mode |
|---|---|---|---|
| `codex` | `AGENTS.md` | markdown | bounded_embed |
| `cursor` | `.cursor/rules/fcop-v4.mdc` | cursor-mdc | bounded_embed |
| `claude-code` | `CLAUDE.md` | markdown | bounded_embed |

初始版本严格为 `1.0-candidate.1`、单语言、65536 完整目标字节上限。Profile 是固定 JSON 字节输入；未知字段、重复键、未知 Host、调用者 evaluator、模型 probe 和未证明模式一律 `RULE_HOST_UNAVAILABLE`。

如增加 bundled Profile JSON，必须：

- 三份独立静态文件，原始字节有测试和 package-data 证明；
- 不进入 18 个业务 Artifact Manifest；
- 不被默认自动选择；
- 外部调用仍必须显式给出精确 Profile 身份；
- 不增加 profile 搜索、环境变量或 PATH fallback。

reference fixture 版本只在提供 RD-14 的固定本地支持证据时成立。它不升级三个初始 Profile，也不证明真实 Host 消费。

## 7. Adoption Receipt

`adopt` 必须按 RD-09 写入：

`fcop/internal/rule-distribution/adoptions/<receipt_sha256>.json`

要求：

- 严格字段集合、确定性 JSON、UTF-8/LF；
- 文件名摘要覆盖完整原始字节；
- `admin_selection_ref` 必须是显式本地普通文件引用和 SHA-256，不能用 `actor=ADMIN` 替代；
- `previous_receipt_ref` 必须验证完整链、工作区和前序字节；
- 精确重试返回同一既有回执；同一身份不同内容拒绝；
- 不修改 `fcop/fcop.json` 的 `profiles`；
- 不写 TASK/REPORT/REVIEW/ISSUE，不授予生命周期权限；
- 不使用全局注册表。

时间只取显式 `recorded_at` 并写作 `adopted_at`，不得读取系统当前时间参与确定性结果。必须验证带时区格式。

## 8. 确定性投影与 plan

### 8.1 bounded_embed

严格实现 RD-13/RD-15 的头、模块标记、原始 canonical 字节、空行、结束标记和 Cursor frontmatter。禁止重新渲染 Markdown、翻译、摘要正文、截断或切换模式。

### 8.2 reference

仅在固定支持证据通过后使用。创建不可变工作区快照：

`fcop/internal/rule-distribution/packages/<manifest_sha256>/`

快照包含 Manifest 和全部 18 份 canonical 制品；Host 输出只引用所选制品。链接必须是从目标目录出发的 POSIX 相对路径，解析后仍在工作区内，并逐项验证摘要。禁止网络 URL、安装包绝对路径、目录逃逸和静默 relocation。

### 8.3 所有权与大小

- 新目标必须不存在；已存在但没有已验证旧 Deployment Receipt/managed block 所有权时拒绝；
- 已拥有目标只能替换唯一、非嵌套、非重复的 begin/end 块；
- 块外所有字节逐字节保留；
- Cursor frontmatter 必须由旧收据证明属于本工具；
- 完整目标字节（含用户区域）计算 65536 上限；
- source 内相对链接必须可解析，否则 `RULE_ARTIFACT_MISMATCH`；
- 冲突、标记不完整、目标漂移返回 `RULE_OWNERSHIP_CONFLICT`。

### 8.4 `plan` 零写入

`plan` 不得创建目录、快照、lock、temp、backup、receipt 或日志。必须返回：

- 固定选择、Manifest/Profile 摘要；
- 每个目标的 path、before/after SHA-256、after_bytes、size_bytes 和确定性 diff；
- planned_backups 与 planned_receipt；
- 不含绝对机器路径、当前时间、随机值。

相同输入字节在不同目录和不同请求时间下，输出目标字节与摘要必须一致。

## 9. apply、并发与部分失败

`apply` 首次写入前必须重新校验 Manifest、全部 18 制品、Profile、Adoption、目标、旧回执和计划。每个目标替换前再次比对 before 摘要。

物理过程必须为：

1. 在目标同目录创建唯一暂存；
2. 写入并 flush/fsync 可用的字节；
3. 校验暂存摘要；
4. 持久化并校验旧字节备份；
5. 在短本地协调区内再次检查 before；
6. 原子替换单一目标；
7. 校验目标；
8. 全部目标完成后才追加成功 Deployment Receipt。

不得宣称多文件整体原子。两个进程对同一 absent-target 前提并发 apply：允许一个成功、另一个 `RULE_OWNERSHIP_CONFLICT`；若两个都返回成功，必须是同一结果和同一 receipt，且磁盘只能有一个成功收据。

`adopt_if_authorized=true` 只允许在 apply 请求同时携带完整、可验证的 `admin_selection_ref` 时先完成同一选择的 Adoption；它不是默认自动采用。普通缺 receipt 的 apply 仍必须拒绝。

冻结 DIST-20 的 `deployments` 是有界多目标故障验证输入：只允许三个已知 Host Profile、目标不得重复、每个子请求必须有完整显式 ADMIN 选择。它不是第四 Host、队列或批处理服务。

`test_fault` 仅允许冻结测试中的三个值：

- `before_stage_durable`
- `between_replacements`
- `before_success_receipt`

并要求 `raise_after_observation=true`。未知值拒绝。该 seam 只能触发确定性失败并持久化最小失败事实；不能执行调用者代码、sleep、随机终止或影响其他工作区。

部分失败必须返回 `RULE_DEPLOYMENT_RECOVERY_REQUIRED`，details 只含安全的 failure_ref、proven_writes、requires_explicit_recovery 等结构化事实。不追加成功 Deployment Receipt，不后台重放。

## 10. Deployment Receipt、验证与回滚

成功部署回执路径：

`fcop/internal/rule-distribution/deployments/<sha256>.json`

严格实现 RD-10 全字段。备份必须位于工作区内部不可变命名空间，使用相对路径和摘要；不得写凭据或机器绝对路径。

`verify_deployment` 必须验证：

- 收据文件名、原始字节和摘要；
- Adoption、Manifest、Profile 及 package snapshot；
- target 当前完整字节和 managed region；
- reference 链接解析、顺序与摘要；
- 历史收据字节未变。

返回的 `runtime_consumption_verified` 必须为 `None/unknown`。不得因文件存在、生成成功或调用者提交 consumption 文件而变为 true。

`rollback` 只接受紧邻 `previous_deployment_ref`，恢复精确备份字节；仅对“此前不存在、当前未漂移、全文件受管理”的目标允许删除。任意版本标签、缺失/修改备份、修改目标、断链一律 `RULE_DEPLOYMENT_RECOVERY_REQUIRED`，且零进一步写入。

`inspect_failure` 只读；`rollback_partial` 只操作 failure_ref 中已证明的路径。恢复后追加或保留明确恢复事实，但不得伪造成功部署收据、修改旧事实或猜测未记录状态。

## 11. 实现允许范围

允许修改或新增：

- `src/fcop/v4/rule_distribution/**`
- 为唯一 facade 做最小接线所必需的 `src/fcop/project.py`、`src/fcop/v4/boundary.py`、`src/fcop/v4/creation.py`
- 可复用且不改变 Core 行为的现有内部原子/路径工具；若必须改共享工具，先证明 v3/v4 回归和公共表面不漂移
- `src/fcop/rules/_data/v4/host-profiles/**`（仅三份静态候选 Profile）
- `pyproject.toml` 中对应 package-data 条目
- `tests/test_fcop/test_v4_rule_distribution*.py` 或新的同前缀单元测试
- public-surface snapshot（仅既有 `Project.rule_distribution` 内部 action 不改变签名时原则上应零漂移）
- 本阶段四份报告和 `reviews/fcop-4.0/wp4c.4/MANIFEST.md`
- `[Unreleased]` CHANGELOG 的准确增量条目

禁止修改：

- `spec/fcop-4.0-spec*.md`、WP4C.1 冻结合同/矩阵/决策；
- `tests/conformance/rule_distribution_v4/**`；
- Schema、MCP/Relay、Host 实际仓库入口文件、CodeFlowMu；
- legacy rule data、AGENTS.md、CLAUDE.md、`.cursor/rules/*.mdc` 的仓库真实文件；
- workflow、版本号、main、release。

若冻结 Conformance 本身阻止合同正确实现，只能报告，不能定点修改。

## 12. 必须通过的测试

### 12.1 WP4C.4 目标

- DIST-08—DIST-20：13/13 Test IDs、53/53 行为节点；
- 其中所有成功路径必须走真实公共入口；
- 所有拒绝路径必须验证结构化错误和零非预期写入；
- 不得 skip、xfail、改名、删断言或通过全局 driver 注入实现。

### 12.2 回归

必须运行并记录：

- `tests/test_fcop` 全量；
- FCoP v4 Core Conformance 119/119；
- `tests/conformance/rule_distribution_v4` 全量，按 owner 解释 WP4C.5/6 尚红节点；
- MCP 隔离回归；
- 新增私有单元测试；
- Ruff、mypy、public-surface snapshot；
- wheel/sdist 中 v4 模块与可选静态 Profile 原始字节检查；
- Windows 原生为当前必需；Linux/macOS 若无原生 runner，只能记 `NOT_NATIVE_VERIFIED`，不得用类型检查替代。

完整分发套件允许 WP4C.5/6 所属节点继续预期红，但不得有 WP4C.4 红灯或非预期失败。必须列出每个剩余红灯的唯一 future owner。

## 13. 安全与失败注入专项

至少新增/保留单元测试覆盖：

- symlink/junction、`..`、绝对目标、Windows drive/UNC、NUL、保留设备名；
- 重复 JSON key、BOM、CRLF、控制字符、非有限值、非法时间；
- receipt 文件名与内容摘要不一致、链循环、跨 workspace、重用；
- manifest/profile/source/target/backup/receipt 在 plan 后漂移；
- managed block 缺失、重复、嵌套、伪标记、用户前后缀；
- full-target byte cap 与 diff 确定性；
- 两进程 absent target 竞争；
- 三个物理失败窗口；
- exact retry、lost response 后重试和历史事实不可变；
- 任意请求都不能安装 evaluator、改变生命周期、访问网络或写出工作区。

测试不能 monkeypatch 成功结果或把生产算法复制进 driver。

## 14. 报告和 GitHub 交付

必须生成：

1. `reports/FCOP-4.0-WP4C.4-IMPLEMENTABILITY-PROOF.md`
2. `reports/FCOP-4.0-WP4C.4-HOST-PROJECTION-MAPPING.md`
3. `reports/FCOP-4.0-WP4C.4-ATOMICITY-AND-RECOVERY-PROOF.md`
4. `reports/FCOP-4.0-WP4C.4-RESULT.md`
5. `reviews/fcop-4.0/wp4c.4/MANIFEST.md`

使用新分支：`review/fcop-4.0-wp4c.4-host-projection`。

提交顺序必须是：

1. Content commit：实现、单元测试、package data、CHANGELOG、四份报告；
2. Manifest-only commit：只修改 WP4C.4 Manifest。

推送后从远端固定 Manifest HEAD 回读：

- 直接父链和每提交文件集合；
- 所有交付文件完整原始字节、大小、SHA-256；
- 新 detached LF checkout 对照；
- 工作树干净；
- remote main 未变；
- 真实 workflow run/check 状态。

建立新的 Draft PR，base 为本任务书所在固定分支，不得把旧 PR #24 改作 WP4C.4，不得请求 reviewer、auto-merge 或切到 main。若 CI 因分支过滤未触发，写 `NOT_TRIGGERED_BRANCH_FILTER`，不得写 PASS。

## 15. 强制停止条件

出现以下任一情况立即停止并只交付阻断报告：

- 固定输入、任务书 SHA/父链或工作树来源不一致；
- RD 合同与冻结测试不能同时满足；
- 需要修改冻结 Conformance、FCoP Core、MCP、Schema、Host 真实入口或 CodeFlowMu；
- 需要数据库、后台服务、网络、自动采用或新 public facade；
- 无法证明并发线性化、零写入 plan、用户字节保护或回滚唯一性；
- 任一 WP4C.4 节点未通过；
- v3/Core/MCP 出现新失败；
- 交付范围、远端回读或哈希不一致。

阻断时 `REQUESTED_GATE: NONE`，不得进入 WP4C.5。

## 16. 完成回执

成功后在 PR 评论中至少报告：

```yaml
WP4C_4_STATUS: COMPLETE
AUTHORIZED_SCOPE: WP4C_4_ONLY
TASKBOOK_COMMIT: ""
TASKBOOK_SHA256: ""
INPUT_HEAD: 4f56cfcf9754bb509b7bd353e830a8e4003810ea
WP4C_3_GATE_COMMIT: ""
FROZEN_DISTRIBUTION_CONTRACT: f6831de12991010f22672fb6e776ce85ef1507ff
DIST_08_20_IDS: 13/13
WP4C_4_TARGET_NODES: 53/53
ADOPTION_RECEIPTS: PASS
HOST_PROFILES: 3/3
DETERMINISTIC_PROJECTION: PASS
PLAN_ZERO_WRITE: PASS
DEPLOYMENT_RECEIPTS: PASS
ROLLBACK: PASS
PARTIAL_FAILURE_WINDOWS: 3/3
TWO_PROCESS_LINEARIZATION: PASS
RUNTIME_CONSUMPTION_CLAIM: UNKNOWN
TEST_FCOP: ""
V4_CORE_CONFORMANCE: 119/119
MCP_REGRESSION: ""
RULE_DISTRIBUTION_FULL: ""
UNEXPECTED_FAILURES: 0
NEW_RUNTIME_DEPENDENCIES: 0
NEW_BACKGROUND_COMPONENTS: 0
NEW_AUTHORITATIVE_STORES: 0
NEW_PUBLIC_FACADES: 0
FROZEN_FILES_MODIFIED: 0
MCP_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0
CONTENT_COMMIT: ""
MANIFEST_COMMIT: ""
REMOTE_HEAD: ""
DELIVERY_SHA256: ""
CI_STATUS: ""
MAIN_MODIFIED: false
RELEASE_CREATED: false
WP4C_5_STARTED: false
WP4C_4_HOST_PROJECTION_ACCEPTED: false
REQUESTED_GATE: WP4C_4_HOST_PROJECTION_ACCEPTED
```

完成后必须停止。只有 ADMIN 审核并签署 `WP4C_4_HOST_PROJECTION_ACCEPTED`，且另行下发固定 WP4C.5 任务书，才能继续。
