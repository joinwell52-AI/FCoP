# FCoP 4.0 WP0 基线审计

> 审计日期：2026-09-03
> 审计范围：WP0 only
> 事实基线：`origin/main@68dbeb15f4e7f84e1d03f907be9fa66c2265843e`
> 执行依据：`02-FCoP-4.0-WP0-Baseline-and-Conflict-Audit-Taskbook.zh.md`
> 资料包：`FCoP-4.0-WP0-Audit-Package-v2.1`，声明 SHA-256 `a3e500887193faace109fddb2347bcbec8bd69c55b7487d28315f0c9ebc50c60`

## 1. 审计结论

当前 `origin/main` 是可复现、测试全绿的 FCoP 3.2.5 实现基线，但**不是已经冻结的 FCoP 4.0 合同**。WP0 已查清现有协议、实现、Schema、MCP、发行边界与 CodeFlowMu 下游样本之间的差异；共登记 30 项合同冲突，均未修复。

FCoP 4.0 的八项 Base Core 候选合同具有充分的 WP1 输入，但仍需 ADMIN 先签署 `BASELINE_VERIFIED`，再由 WP1 唯一化合同。七个架构概念是解释框架，不替代八项可测试合同。

## 2. 现场保护与可复现基线

| 项目 | 审计事实 | 证据 |
|---|---|---|
| 原工作区 | `D:\FCoP`，`main@da79dfefd99f597c9e422ce9edec22157f915a21`，含既有 modified/untracked、历史资料与 v2 dogfood | WP0 开始时的 `git status --short` 记录；未清理、未迁移、未切分支 |
| 远程 | `https://github.com/joinwell52-AI/FCoP.git` | `git remote -v` |
| 最新远程 main | `68dbeb15f4e7f84e1d03f907be9fa66c2265843e` | `git fetch --prune origin` 后 `git rev-parse origin/main` |
| 审计 worktree | `D:\FCoP-wp0-v2.1-audit`，分支 `codex/fcop-4.0-wp0-v2.1` | `git worktree add -b ... origin/main` |
| worktree 起始状态 | clean | 建立后 `git status --short` 无输出 |
| 原现场处置 | `DIRTY_PRESERVED` | 未执行 reset/clean/checkout/redeploy/migrate |
| CodeFlowMu 样本 | 只读 `D:\codeflowmu@21c1c8a215e407687cce69011f9038861ff935eb`；该 SHA 与远程 main 一致 | `git rev-parse HEAD`、`git ls-remote origin refs/heads/main`；未写入该仓库 |

资料包的 22 个提取文件已全文读取；五篇合集正文经逐篇比对为五篇文章的汇编。当前磁盘只有提取目录，没有与声明 SHA 对应的原始容器文件，因此本报告把该 SHA 记录为 ADMIN 提供的包身份，不把“提取目录的自定义拼接摘要”误报为容器哈希验证结果。

## 3. 权威事实层级

本次只描述现状，不提前冻结 WP1 合同。冲突时按以下证据层级审计：

1. `origin/main` 的真实路径、文件内容和测试可观察行为；
2. 当前入口规范 `spec/fcop-v3-spec.md` / `.zh.md`；
3. `spec/fcop-3.0-spec.md` / `.zh.md` 的冻结 3.0.0 基线；
4. accepted ADR、JSON Schema、bundled rules；
5. MCP canonical snapshot 与 server 注册链；
6. CodeFlowMu 只读样本仅作下游兼容证据，不反向定义 FCoP Core；
7. WP0 资料包是 4.0 候选与审计任务书，不是已冻结 4.0 规范。

## 4. 3.2.5 规范与文档基线

| 表面 | 现状 | 结论 |
|---|---|---|
| 包版本 | `src/fcop/_version.py` 与 `mcp/src/fcop_mcp/_version.py` 均为 `3.2.5` | 当前实现版本锚 |
| README | `README.md:117` 声称 current spec 覆盖 3.0→3.2.5；`README.md:401` 声明 current release 3.2.5 | 发布说明已到 3.2.5 |
| current spec | `spec/fcop-v3-spec.md:1-8` 和中文平行版仍写 3.2.4、rules 3.2.3 | 日常规范入口落后于实现与 bundled rules |
| frozen spec | `spec/fcop-3.0-spec.md:16` 明确只冻结 3.0.0，不含 v3.1 MCP 与 v3.2 history | 只能作为 3.0.0 兼容基线，不能代表 3.2.5 全貌 |
| bundled rules | `src/fcop/rules/_data/fcop-rules.mdc:4` 与 `fcop-protocol.mdc:4` 均为 3.2.5 | wheel 内规则与包版本对齐 |
| 原 dogfood 部署副本 | `D:\FCoP\AGENTS.md` 显示 rules/commentary 3.2.3 | 现场漂移只登记，不 redeploy |

FCoP 3.x 的规范核心仍是：文件外化协议、路径定义 NOW、transition 记录 PAST；`ADR-0035` 冻结五阶段与七条边，`ADR-0036` 冻结 append-only transition，`ADR-0038` 排除 runtime/scheduler/executor，`ADR-0039` 要求真实 runtime pressure 才能演进，`ADR-0040` 固化教学/定义两层表述。FCoP 4.0 必须以明确的 superseding contract 处理这些冻结面，不能由实现细节暗改。

## 5. 当前生命周期与 history 调用链

### 5.1 权威路径

| 阶段/对象 | 路径 | 当前入口 | 当前语义 |
|---|---|---|---|
| inbox | `fcop/_lifecycle/inbox/` | `create_task` / `write_task` | created |
| active | `fcop/_lifecycle/active/` | `claim_task` | claimed |
| review | `fcop/_lifecycle/review/` | `submit_task` | pending confirmation |
| done | `fcop/_lifecycle/done/` | `approve_task` 或 `finish_task` | completed |
| archive | `fcop/_lifecycle/archive/` | `archive_task` | closed |
| history | `fcop/history/YYYY-MM-DD/<task-stem>/` | `archive_to_history` / bulk | `_lifecycle` 外的深归档 |
| REPORT | `fcop/reports/`，history 时可被移走 | `write_report` | 执行回执 |
| ISSUE | `fcop/issues/` | `write_issue` | 问题事实 |
| REVIEW | `fcop/reviews/` | `write_review` | 治理判断 |

七条显式边由 `src/fcop/lifecycle/transitions.py:69-76` 定义。没有 `done → active`。`finish_task` 在 `mcp/src/fcop_mcp/server.py:1685-1737` 直接执行 `active → done`，没有机械检查当前轮 REPORT 或授权引用。`submit_task` 同样允许没有 REPORT 的 `active → review`（`server.py:1627-1678`）。

`archive_task` 的公共签名没有 actor。`_v3_archive_chain` 在 `src/fcop/project.py:5162-5245` 用合成的 `archiver` 身份，把 inbox/active/review/done 自动走到 archive；因此它不仅是 `done → archive`，还可跨级触发 claim/finish/approve。它不检查当前轮 REPORT、正式 REVIEW、未闭合 ISSUE、子任务或 Branch 收敛。

### 5.2 四个 history 工具

| 工具 | 参数 | 调用目标 | 读写路径 | 当前测试事实 | WP0 判定 |
|---|---|---|---|---|---|
| `archive_to_history` | `task_id`, `done_date?` | `Project.archive_to_history` | `archive/TASK` 先移至 `history/date/stem`，再扫描/移动 REPORT | MCP 与 project tests 通过 | v3 legacy 冷存储；v4 权威模型待决 |
| `bulk_archive_to_history` | `done_date?` | 逐个调用上述方法 | 批量移动 archive 项 | tests 通过 | 同上，非第六状态合同 |
| `list_history` | `date?` | `Project.list_history` | 只读 history | tests 通过 | Toolkit read |
| `read_history_task` | `task_id`, `date?` | `Project.read_history_task` | 只读 history task | tests 通过 | Toolkit read |

`Project.archive_to_history` 在 `project.py:2917-2954` 先 `source.replace(target_task)`，随后逐份移动匹配 REPORT；中断可留下 TASK 已迁、REPORT 未迁的部分结果。REVIEW 不随之移动。history 的“只读”是约定，不是文件系统强制；权威 TASK 移出 archive 后，路径状态模型需要 WP1 在三种候选中唯一选择。

## 6. 四类信封、证据与授权

| 对象 | 创建入口 | 更新入口 | 删除入口 | 4.0 审计结论 |
|---|---|---|---|---|
| TASK | `write_task` / `create_task` | L1 移动会重写 frontmatter 并追加 transition | 无通用删除；archive/history 为移动 | 已有路径身份，但无持久 operation identity/digest |
| REPORT | `write_report` | 无正式更新；新文件表达新事实 | 无正式删除；history 可移动 | 只带 task 引用，未绑定当前 attempt |
| ISSUE | `write_issue` | 上游 canonical 45 无 `close_issue` | 无正式删除 | FCoP 无 close 入口；CodeFlowMu catalog 多出一项 |
| REVIEW | `write_review` | `mark_human_approved` 原地改写旧文件 | 无正式删除 | 违反 4.0 append-facts 候选，需要 WP1 定义替代事实 |

`TransitionEvent` 只要求 `at/from/to/by/tool`，可选 `note/supersedes`（`src/fcop/lifecycle/events.py:61-128`）。`by` 来自 MCP 调用参数，当前没有持久 `authorization_ref`，也不校验授权是否绑定当前 TASK、transition 和执行轮次。Profile/Host 的角色 allowlist、MCP `binding_required` 与 docstring 约束不是 Core 机械保证。

`Project.write_report` 的参数为 task_id/reporter/recipient/body/status/priority；`write_issue` 没有 subject_ref；`write_review` 有 subject_ref，但没有 `review_kind` 与 `references`。`mark_human_approved` 在 `project.py:3985-4003` 把 `human_approval` 写回同一个 REVIEW，且使用普通 `write_text`。

## 7. Schema 基线

`spec/schemas/README.md` 自称 FCoP v1.0 machine-readable single source of truth，但仓库当前实际有 8 个 schema：**5 个** `version: 1.0.0`（Agent、Boundary、Encoding、Event、Failure），**3 个** `version: 1.1.0`（IPC Envelope、Review、Skill）。其中 `ipc-envelope.schema.json` 与 `review.schema.json` 的顶层 `version` 已是 `1.1.0`，但 `$id` 仍分别为 `https://fcop.dev/schemas/ipc-envelope/v1.0.json` 与 `https://fcop.dev/schemas/review/v1.0.json`；两者存在明确的 `version` / `$id` 不一致。Skill 的 `version: 1.1.0` 与 `$id: https://fcop.dev/schemas/skill/v1.1.json` 一致。它们没有冻结 v3 的五阶段、history、transition 当前约束，也没有 4.0 的 workspace identity、branch_of、attempt、authorization_ref、operation identity/digest、convergence encoding。

IPC root `additionalProperties: true` 保留兼容扩展，却使未建模字段可被接受；“schema wins”与 current v3 实现/规范之间不存在完整、单一、机器可执行的一致面。这是 WP1 必须解决的规范/Schema 权威冲突，不是 WP0 可修复事项。

## 8. 原子性基线

`src/fcop/lifecycle/atomic.py:181-202` 的真实顺序为：读取 source → 在内存追加事件 → destination 目录创建临时文件 → flush + file fsync → `os.replace(tmp,destination)` → `source.unlink()`。

这保证的是目标文件替换动作本身的单路径原子性，不保证“源消失 + 目标出现”这一复合迁移严格原子：进程若在 replace 后、unlink 前崩溃，会有双副本。代码没有 directory fsync、目标内容冲突比较、operation_id 持久索引、跨进程 family lock 或显式 repair API；`os.replace` 还会覆盖已存在目标。完整故障/竞态矩阵见 `ATOMICITY-AND-BRANCH-RACE-AUDIT.md`。

## 9. MCP 与下游基线

| 面 | 数量/版本 | 结论 |
|---|---|---|
| canonical tools | 45 | snapshot 与 server 注册链一致；逐项见工具处置报告 |
| static resources | 11 | 全部来源已定位 |
| resource templates | 3 | 全部来源已定位 |
| CodeFlowMu catalog | 46 | 唯一多出 `close_issue`，`DOWNSTREAM_CATALOG_DRIFT` |
| CodeFlowMu filter/SDK | 45 基线 | 文件注释和计数仍以上游 45 为总数；没有把 `close_issue` 变成 FCoP canonical |
| MCP dependency | `fcop>=3.0.0,<4.0`, `fastmcp>=3.2.0`, `websockets>=12.0` | relay websockets 当前是必装依赖，不是 extra |

工具名保留不等于行为兼容。特别是 archive、finish、human approval、history 与 init/upgrade 类工具，4.0 必须按合同重新判定行为。

## 10. 发行与仓库治理边界（2026-09-03 只读快照）

| 项目 | 当前事实 | 风险/Disposition |
|---|---|---|
| release trigger | `.github/workflows/release.yml` 接受任意 `v*` tag 与 manual dispatch | 无 v4 专用合同门 |
| package order | build 双包 → publish fcop → publish fcop-mcp → GitHub Release | 顺序明确 |
| PyPI auth | 仓库 secrets `PYPI_TOKEN_FCOP`、`PYPI_TOKEN_FCOP_MCP` | 未使用 Trusted Publishing/OIDC |
| branch ruleset | `main-protection` active，实际条件为 `~ALL` branches；禁止删除/非快进，要求 PR thread resolution，0 个必需批准 | 无 required status checks；RepositoryRole 可 always bypass |
| classic branch protection | main 返回 404 | 保护由 ruleset 承载 |
| tag ruleset/protection | 未发现 tag target ruleset | 任意 `v*` tag 可触发真实发布，是 P0 发布边界缺口 |
| environments | 只有 `github-pages` | PyPI jobs 无受保护 environment/审批 |
| Actions | enabled，allowed actions=all，第三方 action 不要求 SHA pin | 供应链边界宽 |
| workflow token | default read；release workflow 显式 `contents: write` | GitHub Release 所需，但需 WP1/WP2 明确 gate |

以上来自登录态 `gh api` 的只读查询；没有改变仓库设置。

## 11. 八项 Base Core 合同审计

| 合同 | 当前能力 | 缺口 | WP1 待决 |
|---|---|---|---|
| C1 Workspace identity | `fcop.json` 与路径可定位项目 | 无规范化 `workspace_id` 与编码版本合同 | manifest 最小字段、迁移与冲突规则 |
| C2 四类正式文件 | TASK/REPORT/ISSUE/REVIEW 已存在 | Schema/实现字段不一致；ISSUE 缺 subject；REVIEW 缺 convergence kind/refs | 四类 envelope 的唯一 Encoding |
| C3 生命周期 | 五阶段、七边、路径 NOW 已实现 | archive 跨级；done→active 缺失；history 身份含混 | v4 边表与合法准入 |
| C4 关系 | `parent/thread_key/references` 已有部分实现 | 无 `branch_of`；关系方向和强弱未统一 | parent/branch_of/subject_ref/references |
| C5 证据/收敛 | REPORT/REVIEW 文件存在 | 无 attempt 绑定、覆盖证明、失效规则 | current-attempt gate 与 convergence encoding |
| C6 授权/只追加 | REVIEW、transition actor 存在 | actor 自报；无 authorization_ref；旧 REVIEW 被改写 | Core 验引用，Profile 验签发权，新增事实不改历史 |
| C7 幂等 | 文件名 O_EXCL/sequence 避免单次碰撞 | 无查找键、digest、跨重启 existing/conflict | `workspace_id+kind+operation_id` 与保存摘要 |
| C8 原子恢复 | temp+fsync+replace 正常路径 | 双副本窗口、覆盖、无目录 fsync/repair/family lock | 可观察结果、线性化点、恢复合同与平台范围 |

## 12. 测试证据

所有测试均在独立 worktree、显式本地 `src`/`mcp/src` PYTHONPATH 下运行：

| 命令范围 | 结果 |
|---|---|
| `tests/test_fcop` | `908 passed, 1 warning in 213.62s` |
| `tests/test_fcop_mcp` | `80 passed, 1 warning in 71.82s` |
| 全量 `python -m pytest -q` | `1225 passed, 2 skipped, 1 warning in 261.10s` |

唯一 warning 为 `src/fcop/teams/__init__.py:31` 的 `importlib.abc.Traversable` Python 3.14 弃用提示。两个 skip 是已迁移项目不存在旧 `docs/agents/log` 样本与空参数集；均原样记录，未修改测试环境或代码。

## 13. WP0 状态

```yaml
WP0_PACKAGE_READY: true
WP0_AUDIT_COMPLETE: true
FCOP_4_CONTRACT_FROZEN: false
IMPLEMENTATION_AUTHORIZED: false
CODEFLOWMU_CHANGE_AUTHORIZED: false
CONTRACT_CONFLICTS: 30
COMMIT_REACHABILITY: LOCAL_ONLY
REMOTE_PUSHED: false
NEXT_GATE_REQUEST: BASELINE_VERIFIED
```

WP0 只证明“现场已经查清”，不证明 4.0 合同已经决定，更不授权实现。
