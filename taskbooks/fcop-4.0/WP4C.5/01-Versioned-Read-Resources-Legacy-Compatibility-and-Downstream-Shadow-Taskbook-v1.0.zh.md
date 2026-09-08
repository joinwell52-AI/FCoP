---
document_role: EXECUTION_TASKBOOK
status: AUTHORIZED_FOR_WP4C_5_ONLY
authority: ADMIN
execution_authorized: true
authorized_scope: WP4C_5_ONLY
accepted_wp4c_4_head: d29e4d41ad4e1fc74e6d3513faa6b95d97ba0dfb
wp4c_4_gate_commit: a9c810296aadf857438a1711b6a56fa63deaf4e9
frozen_fcop_contract: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
frozen_distribution_contract: f6831de12991010f22672fb6e776ce85ef1507ff
frozen_distribution_conformance: 1f4df9cc650f63b9e842d806340eb31b768f708e
taskbook_parent: a9c810296aadf857438a1711b6a56fa63deaf4e9
implementation_authorized: true
codeflowmu_write_authorized: false
main_merge_authorized: false
release_authorized: false
wp4c_6_authorized: false
requested_gate: WP4C_5_COMPATIBILITY_ACCEPTED
---

# FCoP 4.0 WP4C.5：版本化只读资源、3.x 隔离兼容与下游 Shadow 任务书 v1.0

## 0. 唯一授权与停止边界

只有本文件在固定 GitHub 提交中的完整原始字节具有执行授权。PR 评论、聊天摘要、旧总任务书、报告、Gate 和本地副本均不能扩大范围。

执行前必须从 GitHub 固定 ref 回读本文件并核对：

- commit 与本文件直接父提交；
- SHA-256、字节数、UTF-8、无 BOM、LF；
- `accepted_wp4c_4_head`、`wp4c_4_gate_commit` 与父链；
- 冻结 FCoP 4.0 合同、冻结规则分发合同及冻结 Conformance 的原始字节；
- 工作树来源和当前修改状态。

任一不一致立即停止，状态为 `INPUT_INTEGRITY_BLOCKED`，不得自行修正校验值、换基线或继续编码。

## 1. 任务目标

WP4C.5 只完成四件事：

1. 让 3.x 无版本调用继续走现有 legacy 路径，让显式 v4 请求绝不回落、迁移或覆盖 3.x；
2. 让规则、协议身份、已选择指导和 team 能力通过版本化只读资源获得，并由 MCP/Relay 薄适配层委托唯一 Toolkit/Project 实现；
3. 把 disk package、process/index、adoption、Host entry 与 Runtime consumption 五层事实分开报告，不把“包更新”等同于“Host 已消费”；
4. 建立严格授权、只读、零升级的下游 shadow；以 CodeFlowMu 作为真实兼容性观察对象，但不修改、迁移或升级 CodeFlowMu。

必须让冻结的 DIST-23、DIST-24、DIST-26、DIST-29 共 4 个 Test ID、13 个行为节点通过真实 `Project.rule_distribution` 入口。当前基线预计为 1 passed / 12 expected red；执行者必须先实测，不得把预计数写成事实。

本阶段不是 FCoP 4.0 发布，不是 CodeFlowMu 适配器，不是 Host 准入系统，不是远程规则服务，也不是缓存框架。

## 2. 必须坚持的 Unix 边界

实现形态固定为：

> 固定文件输入 → 显式版本选择 → 小型纯读取器／薄适配器 → 可核验输出

禁止增加：

- 数据库、Daemon、Watcher、Scheduler、后台线程、队列或后台重试；
- 网络更新器、远程规则源、自动下载、mutable latest、PATH 探测或 Host 能力发现；
- 全局规则 Registry、第二份 Manifest、第二套摘要算法或第二个分发状态机；
- 自动采用、自动部署、自动迁移、自动回滚或启动时写入；
- 通过“文件存在”推断采用、Host 加载或 Runtime consumption；
- 把 MCP、Relay、CodeFlowMu、Host Profile 或 `v1.0-rc.1` 变成 FCoP Core；
- 为通过测试复制 Project 的解析、选择、摘要或版本路由算法；
- 新公共 facade。唯一公共入口仍为 `Project.rule_distribution(*, action, request)`。

读资源、查层次和 shadow 都必须先完成全部准入检查，再触碰目标路径。拒绝路径必须零写入；DIST-29 缺授权时还必须零下游读取。

## 3. 固定输入与事实优先级

执行者必须完整读取：

1. `spec/fcop-4.0-spec.md`、`spec/fcop-4.0-spec.zh.md`；
2. `docs/fcop-4.0/rule-distribution-contract.md`、`.zh.md`，重点 RD-20、RD-21、RD-23、RD-24；
3. `reports/FCOP-4.0-WP1-COMPATIBILITY-AND-MCP.md`；
4. `reports/MCP-RESOURCE-DISPOSITION-4.0.md`；
5. `reports/FCOP-4.0-WP4C.1-CONTRACT-DECISIONS.md` 与 Conformance Matrix；
6. WP4C.4 的 Manifest、四份报告及本 Gate；
7. `tests/conformance/rule_distribution_v4/test_dist_21_24_assembly_compat_mcp.py`；
8. `tests/conformance/rule_distribution_v4/test_dist_25_30_failures_artifacts_context_gates.py`；
9. 当前 `mcp/src/fcop_mcp/resources.py`、`server.py`、`disposition.py`、资源 snapshot 与隔离测试；
10. 当前 v3 `redeploy_rules`、规则 getter、Project workspace version routing、Relay 本地资源调用链；
11. CodeFlowMu 已公开的 FCoP 3.2.5 精确版本隔离证据提交 `789cb3fa8`，只作下游兼容性证据，不作为 FCoP 合同来源；
12. `v1.0-rc.1` 的固定来源、摘要与状态说明（若仓库中存在），只作 CodeFlowMu 开发期过渡资料。

事实优先级：冻结 FCoP 4.0 规范 > 冻结规则分发合同 > 冻结 Conformance > 本任务书范围控制 > 当前实现与历史报告 > 下游产品事实。

若前三者无法同时满足，输出 `FROZEN_COMPATIBILITY_CONTRACT_CONFLICT` 并停止；不得用实现或任务书隐式重写冻结合同。

## 4. 开工前 Implementability Proof

编码前生成 `reports/FCOP-4.0-WP4C.5-IMPLEMENTABILITY-PROOF.md`，至少包含：

- 13 个目标节点逐行红绿基线；
- 每个节点的唯一 owner、公共入口、读取路径、写入集合和预期错误；
- v3 无版本路由、v4 显式路由和拒绝路径调用图；
- 现有 46 tools、11 static resources、3 templates 的实测快照；
- 本任务书授权的资源面增量及其必要性证明；
- MCP direct、Relay in-process 和 Project reader 的单一算法归属；
- disk/index/adoption/Host/Runtime 五层事实来源；
- shadow 在鉴权前、鉴权后、读取中三处的路径和副作用边界；
- CodeFlowMu 当前精确 pin 与本阶段零写入证明计划；
- 现有工具可复用清单，以及明确不需要建立的缓存、Registry、服务和 Adapter 项目。

若目标只能靠修改冻结断言、skip/xfail、全局 driver 注入、调用者自报权限、真实 CodeFlowMu 写入或新增后台组件通过，立即停止。

## 5. 固定 action 面

本阶段只允许在既有 `Project.rule_distribution` 内新增或完成以下三个 action：

| action | 性质 | 固定效果 |
|---|---|---|
| `read_resource` | 只读 | 按 workspace/version/URI/显式选择返回唯一版本化资源结果 |
| `inspect_layers` | 只读 | 分别返回 disk、index/process、adoption、Host entry、Runtime consumption 事实 |
| `shadow` | 只读 | 缺授权先拒绝；有固定只读授权时只读取明确列出的下游证据并返回摘要事实 |

同时允许 `rule_distribution(action="redeploy")` 作为一个纯版本路由入口：3.x 无版本请求委托既有 legacy redeploy；显式 v4 请求不得使用它。不得新增第四个 action、公共方法或新的 legacy writer。

## 6. 3.x 与 4.0 严格隔离

### 6.1 无版本 legacy redeploy

目标 workspace 的权威 manifest 明确为 3.x，且请求未携带 v4 `protocol_version` 时：

- 只委托当前既有 v3 redeploy 实现；
- 返回明确 `protocol_version` 与真实 `written_paths`；
- 不创建 `fcop/internal/rule-distribution/**`；
- 不生成 v4 Manifest、Host Profile、Adoption/Deployment Receipt；
- 不改写用户拥有的 `AGENTS.md`、`CLAUDE.md` 或 Cursor 入口；
- 不读取或采用 `v1.0-rc.1` 为 FCoP 4.0 合同。

不得为了兼容测试复制旧 writer。若旧实现本身会违反上述边界，先报告真实冲突，不得偷偷另写一套 v3。

### 6.2 显式 v4 请求作用于 v3 workspace

必须在任何写入前返回 `toolkit:RULE_ADOPTION_REQUIRED`。不得：

- 回落 legacy writer；
- 修改 workspace 版本；
- 新建 v4 internal 目录；
- 改动 Host 入口；
- 将旧规则大文件解释为 v4 Manifest。

### 6.3 `v1.0-rc.1` 的固定身份

若该资料存在，其身份固定为：

```yaml
role: CODEFLOWMU_DEVELOPMENT_TRANSITION_REFERENCE
normative_fcop_4_contract: false
ordinary_business_agent_injection: false
release_identity: false
auto_adoptable: false
```

必须记录固定 path/revision/SHA-256/许可状态。它不得进入普通 sequential/parallel guidance、MCP 默认资源、FCoP 4.0 Manifest、wheel 默认业务包或 CodeFlowMu 自动升级路径。

## 7. 版本化只读资源合同

### 7.1 唯一读取实现

`read_resource` 是语义实现；MCP 与 Relay 只能做参数归一化和结果序列化。Manifest 解析、制品摘要、assembly 选择、规范身份和版本判断必须委托 Toolkit/Project，不能在 `mcp/` 再实现一份。

所有读取必须：

- 零 project 写入；
- 不采用、不部署、不写 receipt、不安装 evaluator、不迁移；
- 不读网络，不因 Relay 名称启动 WebSocket；
- direct `stdio-local` 与 `relay-inprocess + network=false` 返回相同语义内容、版本和摘要；
- 对版本不明、URI 不支持或制品漂移返回结构化 Toolkit 错误。

### 7.2 四类语义 URI

| URI | v3 | v4 |
|---|---|---|
| `fcop://rules` | 保持既有 legacy rules 资源合同 | 返回经校验的 v4 package Manifest typed object、Manifest SHA-256 与 `protocol_version=4.0` |
| `fcop://protocol` | 保持既有 legacy protocol 资源合同 | 返回冻结规范身份：repo-relative path、固定 revision、原始字节 SHA-256；不得包含 Host 生成状态 |
| `fcop://guidance/{assembly}/{language}` | `sequential/en` 返回既有 legacy rules 指导；不得声称 v3 原生具有 v4 assembly | 对 `sequential|parallel`、`en|zh` 读取经 Manifest 校验并按显式 assembly 选择的 canonical 模块；顺序和原始字节确定 |
| `fcop://team` | 只读映射到既有 `fcop://teams` 内容来源，不另建 team 数据源 | 返回 typed unavailable：`available=false` 与稳定 reason；固定角色不进入 FCoP 4.0 Core 或普通最小包 |

Project 内部 Python typed object 与 MCP 文本表示必须语义等价。MCP 对 JSON 对象使用确定性 UTF-8/LF JSON；不得用 `repr()`、Markdown 拼接或 Host 输出替代。

### 7.3 本阶段唯一允许的 MCP 资源面增量

WP0/WP1 的 `11 static + 3 templates` 是 3.2.5 基线事实；WP4B 接受面当前为 `46 tools + 11 static + 3 templates`。为实现冻结 RD-21/DIST-24，本任务书显式授权且只授权以下两个加法：

1. 新增静态资源 `fcop://team`；
2. 新增资源模板 `fcop://guidance/{assembly}/{language}`。

成功后的精确公开快照必须为：

```yaml
tools: 46
static_resources: 12
resource_templates: 4
```

原 11 个静态资源、3 个模板和 46 个工具的名称、顺序及既有 v3 语义不得删除、改名或借机重写。必须更新 canonical snapshot 与 MCP tests，并在 CHANGELOG 明确这是 WP4C.5 的有界 additive surface，不得回写历史报告中的 11+3 基线数字。

若 MCP 框架不能在不复制算法、不引入网络或不破坏 v3 的情况下实现这两个增量，输出 `MCP_RESOURCE_SURFACE_IMPLEMENTATION_BLOCKED` 并停止，不得改成新工具或隐藏写操作。

## 8. 五层事实与失效边界

`inspect_layers` 必须分别返回：

| 层 | 权威来源 | 允许结论 |
|---|---|---|
| disk package | 当前 v4 Manifest 原始字节 | 当前磁盘包摘要 |
| process/index | 当前进程真实 getter/index 行为 | index 摘要及明确失效证据；若无缓存，如实报告 uncached/fresh-read |
| adoption | 已验证 Adoption Receipt | 被采用的 Manifest 摘要 |
| Host entry | Deployment Receipt + 当前目标完整字节 | 当前 Host 入口摘要与是否漂移 |
| Runtime consumption | 外部 Host/Runtime 可核验证据 | 本阶段固定为 `None/UNKNOWN`，除非后续独立合同定义证据 |

禁止为了满足 DIST-26 新造缓存。若当前实现没有 cache，直接返回当前读取值并提供 `uncached_current_read` 一类稳定失效说明；不得伪造 old cache。

磁盘 package 更新后：

- disk 摘要必须变化；
- index 摘要可以是旧或新，但必须给出真实 `index_invalidation_evidence`；
- adoption 与 Host entry 仍绑定旧收据/旧字节；
- Runtime consumption 仍为 `None`；
- 进程重建后仍不能把磁盘新版本推断为已采用或已部署；
- 该 action 全程零写入。

## 9. 下游只读 Shadow

### 9.1 鉴权前零访问

`shadow_authorization_ref` 缺失、无效、摘要不符、scope 非只读或未绑定目标路径时，必须在解析、枚举、stat/open 下游路径之前返回 `toolkit:RULE_ADOPTION_REQUIRED`。不得用“反正只读”绕过授权。

### 9.2 有授权时的最小行为

授权文件必须是调用者预先提供的本地普通 JSON 文件及 SHA-256，不由 `shadow` 创建。最小字段为：

```yaml
authorization_kind: fcop-rule-distribution-shadow
scope: read-only
downstream_kind: fcop-consumer
downstream_root: <normalized absolute path>
allowed_relative_paths: [<bounded exact paths>]
expected_sha256: {<path>: <sha256>}
```

要求：

- 严格 JSON、拒绝重复键/BOM/未知字段；
- 最多 16 个显式相对普通文件，禁止 glob、目录递归、symlink/junction、`..`、UNC/drive 逃逸；
- 请求 target 必须与授权字节逐字段绑定；
- 只读取 allowlist 文件并核验摘要，不返回凭据或原文正文；
- 只返回文件 path、size、sha、检测到的版本 pin 与兼容性事实；
- 不写下游、不写 FCoP workspace、不改版本、不安装包、不调用 npm/pip、不启动进程；
- `deploy` 必须为 false；true 直接拒绝；
- 不把下游静态 catalog、UI 或 RC 文档提升为 FCoP 权威事实。

该授权只控制工具对外部路径的读取，不是 F4.7 生命周期 authorization，也不安装 Profile evaluator。

### 9.3 CodeFlowMu 真实 shadow

在不修改 CodeFlowMu 的前提下，对可访问的固定 CodeFlowMu 提交或干净只读工作树进行一次兼容观察：

- 核实其 FCoP/FCoP-MCP 精确 pin 仍为 3.2.5；
- 核实 4.x、缺失、不可解析和非精确版本仍 Fail Closed；
- 核实启动路径不自动安装、升级或迁移 FCoP；
- 核实本轮没有改变其 Scheduler、EVAL、生命周期、Panel、Host 逻辑或五桶；
- 将 `close_issue` 等下游 catalog 漂移仅记为下游事实；
- 记录 `v1.0-rc.1` 仅供当前 CodeFlowMu 开发过渡，不把它当 FCoP 4.0 正式发布。

优先核对已知隔离证据提交 `789cb3fa8`；若远端或本地当前版本已推进，必须同时记录实际 ref，不能把旧提交冒充 current。若没有可核验 CodeFlowMu ref，报告 `CODEFLOWMU_SHADOW_NOT_AVAILABLE` 并停止请求 Gate；不得用合成 fixture 冒充真实使用者验证。

## 10. 实现允许范围

允许修改或新增：

- `src/fcop/v4/rule_distribution/**`；
- 仅为 action 接线所需的 `src/fcop/project.py`；
- 为 v3 无版本委托所必需的最小内部路由，但不得改变旧公共签名或另建 writer；
- `mcp/src/fcop_mcp/resources.py`、`server.py`、`disposition.py` 中只读资源薄适配与精确注册；
- MCP canonical resource snapshot 与相应资源测试，仅按 46/12/4 的有界增量更新；
- `tests/test_fcop/test_v4_rule_distribution*.py` 或新的同前缀单元测试；
- 本阶段只读 shadow 的测试 fixture（不得引用真实 CodeFlowMu 写路径）；
- public-surface snapshot（原则上零漂移）；
- `[Unreleased]` CHANGELOG 的准确增量；
- 本阶段五份报告和 `reviews/fcop-4.0/wp4c.5/MANIFEST.md`。

禁止修改：

- `spec/fcop-4.0-spec*.md`、冻结 RD 合同/矩阵/决策；
- `tests/conformance/rule_distribution_v4/**`；
- FCoP Core 生命周期、Schema、Host Profile/投影/部署语义；
- legacy canonical rule bytes、现有 11 个资源和3个模板的 v3 内容来源；
- MCP tools 或工具计数、Relay 网络能力、packaging extras；
- CodeFlowMu 任何文件、分支、依赖、配置或工作区；
- workflow、版本号、`main`、release。

若必须改变共享组件，先证明唯一原因、最小 diff、v3/v4/MCP 全回归和公共表面不漂移；否则停止。

## 11. 必须通过的测试

### 11.1 WP4C.5 目标

- DIST-23：3/3 节点；
- DIST-24：8/8 节点；
- DIST-26：1/1 节点；
- DIST-29：1/1 节点；
- 合计 4/4 Test IDs、13/13 节点；
- 不得 skip、xfail、改名、删断言或修改冻结 fixture；
- 成功路径走真实 `Project.rule_distribution`；拒绝路径验证结构化错误和零副作用。

### 11.2 MCP 资源专项

必须新增/更新真实 MCP tests，至少证明：

- tools 46/46 不变；static resources 12/12；templates 4/4；
- 原 11+3 名称与 v3 内容行为不漂移；
- 新 `fcop://team` 与 guidance template 的注册、参数限制和序列化；
- v4 rules Manifest 原始摘要一致；protocol identity 固定；guidance 逐制品摘要一致；
- direct 与 Relay in-process/network=false 语义一致；
- 所有资源读取零写入、零 adoption、零 deployment、零 evaluator 安装；
- 不联网，不启动 Relay server；
- wheel/sdist 后 MCP 能读到相同的 packaged v4 canonical bytes；若完整制品验证属于 WP4C.6，只能记录当前可证明范围，不提前宣称跨平台发布验收。

### 11.3 回归

必须运行并记录：

- `tests/test_fcop` 全量；
- FCoP v4 Core Conformance 119/119；
- `tests/conformance/rule_distribution_v4` 全量；WP4C.5 完成后预计仅余 WP4C.6 的 20 个红灯，必须逐项按 owner 核验；
- MCP 隔离全量；
- 新增 unit/security tests；
- Ruff、mypy、public-surface snapshot；
- Windows 原生测试；Linux/macOS 无原生 runner 时只能写 `NOT_NATIVE_VERIFIED`。

## 12. 安全与故障专项

至少覆盖：

- workspace version 缺失、矛盾、3.x/v4 交叉请求；
- 资源 URI 编码、大小写、路径段、未知 assembly/language、重复参数；
- Manifest/module/spec identity 在读取前后漂移；
- MCP 资源请求带 adoption/deploy/evaluator/network 字段时拒绝；
- direct/Relay 结果不一致时 fail closed；
- index 无缓存与有缓存两种真实路径，不伪造命中；
- Adoption/Deployment Receipt 断链、Host target 漂移与 Runtime unknown；
- shadow 授权重复键、BOM、CRLF、摘要漂移、跨根、symlink/junction、glob、超16文件；
- shadow 未授权零 stat/open/scan，已授权只读 allowlist 且前后快照一致；
- CodeFlowMu 工作树和 Git HEAD 前后不变；
- 任何路径均不得访问凭据、环境变量秘密或把内容写进报告。

测试不能 monkeypatch 成功结果、复制生产算法到 driver 或使用真实 CodeFlowMu 作为可写 fixture。

## 13. 必须生成的报告

1. `reports/FCOP-4.0-WP4C.5-IMPLEMENTABILITY-PROOF.md`
2. `reports/FCOP-4.0-WP4C.5-VERSIONED-RESOURCE-MAPPING.md`
3. `reports/FCOP-4.0-WP4C.5-LEGACY-AND-LAYER-ISOLATION.md`
4. `reports/FCOP-4.0-WP4C.5-CODEFLOWMU-SHADOW.md`
5. `reports/FCOP-4.0-WP4C.5-RESULT.md`
6. `reviews/fcop-4.0/wp4c.5/MANIFEST.md`

CodeFlowMu shadow 报告只记录路径类别、commit、版本约束、文件摘要和判定；不得复制凭据、用户数据、大段产品源码或修改建议到 FCoP 正式合同。

## 14. GitHub 审核交付

使用新分支：`review/fcop-4.0-wp4c.5-compatibility`。

必须从本任务书固定提交创建独立 clean worktree。原 `D:\FCoP`、现有 review worktree 和 CodeFlowMu 工作区全部保留。

提交顺序固定为：

1. Content commit：实现、测试、snapshot、CHANGELOG、五份报告；
2. Manifest-only commit：只修改 WP4C.5 Manifest。

推送后必须从远端固定 Manifest HEAD 回读并核验：

- 父链与两提交文件集合；
- 全部交付文件原始字节、大小、SHA-256；
- 全新 LF checkout 与 tracked bytes；
- 工作树干净；
- remote main 未变；
- 真实 workflow run/check 状态。

建立新的 Draft PR，base 为本任务书分支；不得复用 PR #25，不得请求 reviewer、auto-merge、合并或发布。CI 若因分支过滤未触发，写 `NOT_TRIGGERED_BRANCH_FILTER`，不得写 PASS。

## 15. 强制停止条件

出现以下任一情况立即停止并只交付阻断报告：

- 固定输入、任务书 SHA/父链或工作树来源不一致；
- 冻结合同、冻结 Conformance 和本任务书无法同时满足；
- 需要修改冻结测试、Core、Schema、Host 部署合同或 CodeFlowMu；
- 需要新增 MCP tool、超过本任务书明确授权的 12+4 资源面、网络或后台组件；
- v3 无版本路由只能靠第二 legacy writer 或会自动迁移；
- MCP/Relay 不能委托唯一 Project 读取实现；
- 未授权 shadow 会触碰下游，或已授权 shadow 不能证明全程零写入；
- 无法获得真实 CodeFlowMu 固定 ref 的只读兼容证据；
- 任一 WP4C.5 目标节点未通过；
- v3/Core/MCP 出现新失败；
- 交付范围、远端回读、哈希或工作树核验不一致。

阻断时 `REQUESTED_GATE: NONE`，不得进入 WP4C.6。

## 16. 完成回执

成功后在 PR 评论中至少报告：

```yaml
WP4C_5_STATUS: COMPLETE
AUTHORIZED_SCOPE: WP4C_5_ONLY
TASKBOOK_COMMIT: ""
TASKBOOK_SHA256: ""
INPUT_HEAD: d29e4d41ad4e1fc74e6d3513faa6b95d97ba0dfb
WP4C_4_GATE_COMMIT: a9c810296aadf857438a1711b6a56fa63deaf4e9
FROZEN_DISTRIBUTION_CONTRACT: f6831de12991010f22672fb6e776ce85ef1507ff
DIST_23: 3/3
DIST_24: 8/8
DIST_26: 1/1
DIST_29: 1/1
WP4C_5_TARGET_NODES: 13/13
LEGACY_V3_ROUTING: PASS
V4_NO_FALLBACK_OR_MIGRATION: PASS
MCP_TOOLS: 46/46
MCP_STATIC_RESOURCES: 12/12
MCP_RESOURCE_TEMPLATES: 4/4
RESOURCE_READ_ZERO_WRITE: PASS
DIRECT_RELAY_PARITY: PASS
LAYER_SEPARATION: PASS
RUNTIME_CONSUMPTION_CLAIM: UNKNOWN
UNAUTHORIZED_SHADOW_ZERO_ACCESS: PASS
AUTHORIZED_SHADOW_ZERO_WRITE: PASS
CODEFLOWMU_SHADOW: PASS
CODEFLOWMU_PIN: fcop==3.2.5_fcop-mcp==3.2.5
CODEFLOWMU_FILES_MODIFIED: 0
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
CONTENT_COMMIT: ""
MANIFEST_COMMIT: ""
REMOTE_HEAD: ""
DELIVERY_SHA256: ""
CI_STATUS: ""
MAIN_MODIFIED: false
RELEASE_CREATED: false
WP4C_6_STARTED: false
WP4C_5_COMPATIBILITY_ACCEPTED: false
REQUESTED_GATE: WP4C_5_COMPATIBILITY_ACCEPTED
```

完成后必须停止。只有 ADMIN 审核并签署 `WP4C_5_COMPATIBILITY_ACCEPTED`，且另行下发固定 WP4C.6 任务书，才能继续。
