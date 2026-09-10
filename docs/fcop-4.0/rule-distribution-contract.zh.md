# FCoP 4.0 规则分发合同

状态：待 ADMIN 冻结的候选合同；版本 `1.0-candidate.1`；未实现、未采用、未发布。

权威：[WP4C.1a](https://github.com/joinwell52-AI/FCoP/blob/7f973dc5f32bc6b9e1076184d1247c55a1349bd5/taskbooks/fcop-4.0/WP4C.1a/01-Core-Relation-Set-and-Sequential-Assembly-Correction-Taskbook-v1.0.zh.md)，恢复 WP4C.1 未被替代的要求。[英文版](rule-distribution-contract.md)使用相同条款编号。固定于 `aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6` 的[Core 规范](../../spec/fcop-4.0-spec.zh.md)不修改。[决策与完整映射](../../reports/FCOP-4.0-WP4C.1-CONTRACT-DECISIONS.md)是本合同的组成附表；[验证矩阵](../../reports/FCOP-4.0-WP4C.1-CONFORMANCE-MATRIX.md)定义未来可观察检查，并非已经实现的测试。

## 权威和服务对象

### RD-01 — 权威

“必须／不得”表示本分发合同的要求，不是新增 Base C1–C8。中英文的义务、字段、错误和 Gate 语义必须一致。与冻结规范冲突时必须停止分发并请求 ADMIN 裁决；已安装规则、Host 入口、测试或旧解释不能覆盖冻结规范。只有 ADMIN 签署 `WP4C_1_RULE_DISTRIBUTION_CONTRACT_FROZEN` 后本合同才冻结；它不自动授权下一阶段执行、迁移、合并或发布。

### RD-02 — 范围

Rule Package 只能包含可追溯的冻结 FCoP 使用指导，不得执行工作、判定业务完成、授予生命周期权限、选择模型或管理会话／调度。九个语义模块、每模块每语言一份可编辑制品以及派生的薄 Host 输出，不替代 Core 或 Toolkit。禁止数据库、Daemon、Watcher、后台更新器、远程规则服务和第二 Runtime；文件与短暂显式操作即可完成分发。

### RD-03 — 服务对象隔离

普通业务指导、FCoP 仓库开发指导与外部工程宪法必须分开。开发指导保留在仅仓库使用的 `docs/fcop-4.0/development/` 命名空间，通过显式选择的开发入口引用；其正文或外部宪法均不得进入普通装配、wheel 默认业务指导或 MCP 默认响应。本轮保留路径，不创建该手册。未来独立宪法需要 ADMIN 固定身份、权利和采用；允许当前缺席，不得用 CodeFlowMu RC 补位。摘要为 `87cf212d1cb75cefd0da6da7e5f0f4c7eaedbc231c784b985c3e2e51856abc4c` 的 CodeFlowMu `v1.0-rc.1` 不得作为来源、权威、依赖、复制、翻译、打包或投影对象。旧讨论稿原则映射只是历史审计证据，不是本合同来源。

## Canonical 模块

### RD-04 — 身份与唯一主责

保留 `src/fcop/rules/_data/v4/manifest.json` 和 `src/fcop/rules/_data/v4/{module_id}.{language}.md`；language 仅为 `en` 或 `zh`。这些是未来包制品，不是 WP4C.1a 创建的文件。保留九个模块，不增加兜底模块或产品域。决策附表的 73 行将每个完整冻结条款（含表格／示例）分配给唯一 primary module；其他模块引用主责，不复制义务。可以提到共享术语，但不能复制规范段落。模块每个规范段落必须引用至少一个归属自己的冻结条款；非规范示例必须标记且不能发明 Gate。

| module_id | 唯一职责 | depends_on | load_order |
| --- | --- | --- | --- |
| workspace | 声明、身份、路径／编码安全 | [] | 10 |
| envelopes | 四类正式文件、追加事实、普通 REPORT head | [workspace] | 20 |
| relations | 四关系字段、方向、强弱、基数、解析 | [workspace,envelopes] | 30 |
| authorization | 持久授权、可信已采用 Profile、单次消费 | [workspace,envelopes,relations] | 40 |
| idempotency | 创建 TASK 身份、规范摘要、持久重试 | [workspace] | 50 |
| recovery | 原子性、五种恢复观察、receipt、family 线性化 | [workspace] | 60 |
| lifecycle | NOW/PAST、T1–T7、attempt 和普通证据门 | [workspace,envelopes,relations,authorization,idempotency,recovery] | 70 |
| compatibility | 权威／层边界、错误、版本隔离、符合性边界 | [workspace] | 80 |
| convergence | Branch 准入／深度、family REPORT／digest、Root 汇合／T7 | [workspace,envelopes,relations,authorization,idempotency,recovery,lifecycle,compatibility] | 90 |

`compatibility` 主责 F4.0、层排除、F4.10、F4.11 及发布／符合性边界条款，因为它们防止把不同合同投影到所选版本；它不承载开发 SOP。`recovery` 主责共享物理线性化 F4.9.5，`convergence` 引用它。普通 REPORT head 归 `envelopes`，汇合模块引用它处理 Branch head。这使依赖无环且不遗漏公共证据。

### RD-05 — 精确关系集合

机器可读的 Core 关系集合：

```json
["parent","branch_of","subject_ref","references"]
```

| 字段 | 来源 → 目标 | 强弱／基数 | 规范来源 |
| --- | --- | --- | --- |
| parent | TASK → TASK | 强委派／层级关系；不是并发 Branch | F4.5.1 |
| branch_of | TASK → Root TASK | 强；最多一个 | F4.5.1 |
| subject_ref | REPORT/ISSUE/REVIEW → TASK 或 workspace | 强；唯一；workspace ISSUE 使用 workspace:<workspace_id> | F4.5.1 |
| references | 任意 envelope → 既有 envelope | 弱引用；Gate 使用时必需 | F4.5.1–F4.5.2 |

强关系缺失、悬空、跨工作区、循环或不唯一，以 `RELATION_INVALID` Fail Closed；普通弱引用无法解析产生 `REFERENCE_UNRESOLVED`，用于 Gate 则拒绝。不为 parent 或 references 发明额外基数。F4.5.3–F4.5.4 由 convergence 主责（同级 Branch 深度、唯一 active Root 准入），不在 relations 重复。F4.5.5 仍归 relations：thread_key 属于 Profile/Legacy。`blocks`、`relates_to`、`supersedes` 不得作为 Base 关系名、别名或隐式 Gate 编码；决策附表给出有证据的历史处置。

### RD-06 — Canonical 字节与双语制品

每份模块必须严格 UTF-8、任何位置无 BOM、仅 LF、结尾恰好一个 LF，禁止除 TAB/LF 外的 C0 控制字符及 DEL。制品正文不得出现 RD-13 的保留投影标记行。摘要覆盖原始字节，不得先归一化再验收。两语言共用 module_id、主责条款集、依赖、受众和选择语义，路径／大小／摘要分别记录。分发不得自动翻译、手改投影或静默回退语言。机器 ID 一致外还需语义审查。package_version 固定字节；字节变化必须形成新包版本／Manifest 并显式采用，不得使用可变 latest。

## Distribution Manifest

### RD-07 — 结构与字段

Manifest 是严格 UTF-8／无 BOM／LF JSON；重复键、未知 schema／字段和类型错误均拒绝。顶层字段严格为 `manifest_schema`、`protocol_version`、`package_version`、`artifacts`，不承载规则正文。manifest_schema=`fcop-rule-distribution/v1`；protocol_version=`4.0`；package_version 是精确非空版本字符串（无范围／latest）；artifacts 恰好 18 条，即九模块 × 两语言。每条记录严格包含：

| 字段 | 类型／约束 |
| --- | --- |
| module_id | RD-04 的九个 ID 之一 |
| source_path | 相对 Manifest 目录的 POSIX 路径，精确为 module_id.language.md |
| language | en 或 zh |
| sha256 | 64 位小写十六进制，覆盖完整制品字节 |
| size_bytes | 非负整数，精确字节数 |
| normative_clause_refs | 不重复的 F4 条款 ID 数组，与该模块主责附表完全相同 |
| depends_on | 不重复模块 ID 数组，与 RD-04 相同 |
| load_order | RD-04 整数，两语言一致 |
| audience | business-agent；不得包含 repository-developer 正文 |
| required_when | 八基础模块为 common；convergence 为 branch-family |
| conflicts_with | 不重复模块 ID 数组；本九模块版本为 [] |

不得包含采用状态、Host 消费状态、时间戳、绝对路径、随机值或运行进程字段。完整 Manifest 字节在外部计算摘要，不能自含自身摘要。Git／package 原始字节必须相同；CRLF 归一化相等只用于诊断。

### RD-08 — 校验与确定性选择

先验证完整 Manifest、所有制品身份／双语一致性，再解析显式装配／语言／profile。缺失／重复制品、未知 ID、非法值、摘要／大小漂移、包外路径、符号链接逃逸、依赖环或冲突，必须在产生效果前拒绝。显式选择缺失依赖时返回错误，不得静默加载。所选模块依赖有效，按 load_order、然后 module_id Unicode code point 排序；语言按显式 selected_languages 顺序。制品数组顺序、目录枚举不影响输出。纯选择不访问网络、不执行谓词或调用者提供的政策代码，也不安装授权 evaluator。

## 工作区采用与部署证据

### RD-09 — Adoption receipt

采用是 ADMIN 明确授权的本地选择，不是安装副作用。保留不可变路径 `fcop/internal/rule-distribution/adoptions/<sha256>.json`，文件名摘要覆盖完整回执字节。它是 Toolkit 分发事实，不是 envelope、Core operation receipt 或 NOW 来源。精确最小字段合同：

| 字段 | 类型／含义 |
| --- | --- |
| receipt_schema | fcop-rule-adoption/v1 |
| workspace_id | 当前合法工作区身份，绑定该回执 |
| protocol_version | 4.0；与工作区及 Manifest 一致 |
| rule_package_version | 精确选择的包版本 |
| rule_manifest_sha256 | 完整 Manifest 字节身份 |
| assembly_id | sequential 或 parallel；开发采用 RD-19 独立引用束 |
| selected_modules | 不重复有序模块 ID，精确符合 RD-17/RD-18 |
| selected_languages | [en] 或 [zh]；仅固定 Host profile 明确允许时可多语言 |
| selected_host_profile | 含 host_id、profile_version、静态 profile 原始字节 sha256 的对象 |
| target_paths | 有序、不重复、相对工作区的 POSIX 路径，与 profile 一致 |
| adopted_by | ADMIN 显式选择证据引用；actor 标签本身不证明权威 |
| adopted_at | 带时区的采用时间；只在回执，不进入输出输入 |
| previous_receipt_ref | 首次为 null，否则是旧回执相对路径和 sha256 |

缺少回执，不得把现有 Host 文件解释为已采用。采用证据不授予生命周期授权，也不证明部署成功。ADMIN 决策未确定、工作区版本不兼容或链无效时拒绝；不得在采用过程中迁移或重标 v3 工作区。不建立可变全局采用注册中心。

### RD-10 — Deployment receipt 与回滚

目标写入并验证后，在 `fcop/internal/rule-distribution/deployments/<sha256>.json` 追加不可变分发回执。必需字段：`receipt_schema=fcop-rule-deployment/v1`、`adoption_receipt_ref`（路径＋摘要）、`manifest_sha256`、`host_profile_sha256`、`action`（deploy 或 rollback）、`previous_deployment_ref`（null 或路径＋摘要）、`targets`、带时区 `recorded_at`。每个目标记录 `path`、`before_sha256`（原文件不存在则 null）、`after_sha256`、`managed_region_sha256`、`backup_ref`（仅原文件不存在可 null）。备份为不可变相对路径字节快照及摘要，不含凭据或机器绝对路径。回执记录已观察到的物化，不证明 Runtime 消费；时间不进入投影字节。

回滚必须显式请求，只使用紧邻的前一条已采用回执，校验 Manifest／profile／制品／备份摘要，比较当前目标与上次成功部署，保留用户区域并恢复已记录的精确字节（或只移除可证明新建、未改变且全受管理的目标）。漂移、备份缺失或历史歧义时停止，不删除／覆盖。回滚追加引用历史的新采用／部署证据，不改旧回执、不移动生命周期 TASK、不按版本标签任意恢复。

## Host profile 与确定性输出

### RD-11 — 静态 profile 字段

Host profile 是固定的静态 JSON 输入，不是发现或准入机制。字段严格为：

| 字段 | 类型／约束 |
| --- | --- |
| host_id | codex、cursor 或 claude-code |
| profile_version | 精确版本字符串；任何变更需新版本和采用 |
| supported_entry_kinds | markdown 和／或 cursor-mdc 数组 |
| reference_mode | none 或 relative-path；后者先有隔离支持证据 |
| projection_mode | reference 或 bounded_embed；reference 要求 relative-path |
| target_paths | RD-12 的有序唯一相对路径 |
| preserve_regions | 精确 begin/end 标记对，每目标一个受管理块；块外字节归用户 |
| max_projection_bytes | 正整数；限制包括保留字节的完整结果目标大小 |
| encoding | UTF-8-no-BOM |
| newline | LF |
| languages | 显式有序 en/zh 数组；候选 profile 只选择一种语言 |

不得探测模型／Subagent／二进制／认证／权限，不得任意挂钩。`adapter_supported`、`admin_adopted`、`entry_generated`、`runtime_consumption_verified` 必须分别拥有证据（或 unknown），互不推导。此 profile 不是授权 Profile evaluator。摘要固定只能证明身份，不证明信任或实际 Host 消费。

### RD-12 — 三种候选 profile

以下是设计目标，不是现有支持／消费声明。初始版本 `1.0-candidate.1` 使用 bounded_embed、reference_mode=none、显式单一语言及 max_projection_bytes=65536。此上限是合同安全限制，不是测得的 Host 限制；溢出拒绝，不删义务。修改上限需审查后的 profile 版本，不能运行时覆盖。未来 reference profile 使用独立版本、reference_mode=relative-path、上限 8192，并在采用前提供解析／顺序／完整性／失败的隔离证据。目前不假定这三个 Host 中任何一个具备可靠文件引用行为。

| host_id | supported_entry_kinds | target_paths | 候选政策 |
| --- | --- | --- | --- |
| codex | [markdown] | [AGENTS.md] | 一个所选语言受管理入口 |
| cursor | [cursor-mdc] | [.cursor/rules/fcop-v4.mdc] | 单一语言入口；不同时使用 AGENTS 替代入口 |
| claude-code | [markdown] | [CLAUDE.md] | 一个所选语言受管理入口 |

未知 Host 返回 typed-unavailable，不生成。上述目标路径不授权替换现有 legacy 或产品内容。已有 legacy 根入口需要另行明确授权的所有权／版本切换；本合同不授权现有工作区迁移。已采用的 v4 Cursor profile 不得与活动 legacy FCoP mdc 输入并存。

### RD-13 — 共同确定性格式

投影是精确 Manifest、所选制品字节、静态 profile、显式装配／语言和现有保留目标字节的纯函数。输出不得含生成时间、机器绝对路径或随机值。规划前验证 UTF-8／无 BOM／LF；保留区域字节非法时停止，不静默归一化。独立行上的起止标记严格为 `<!-- fcop:v4:begin -->` 和 `<!-- fcop:v4:end -->`。内部首行严格为 `<!-- fcop:package=<package_version>;manifest=<sha256>;host=<host_id>@<profile_version>;assembly=<assembly_id>;language=<language> -->`。每个格式行后一个 LF；插入标识符拒绝控制字符／标记分隔符。包／profile 身份不从不可信规则正文获取。

新 markdown 文件由该受管理块和末尾 LF 组成。已有带标记文件只替换包含起止标记的整个受管理块；块外每个字节保留并参与大小／diff 比较。标记缺失／重复／嵌套或预期新目标存在不受管理内容时停止。新 cursor-mdc 先写精确行 `---`、`description: FCoP 4.0 selected guidance`、`alwaysApply: true`、`---`、空行，再写块；frontmatter 是受管理的全文件元数据，更新前必须匹配旧回执。不得推断任意现有 Cursor frontmatter 属于 FCoP。任何 alwaysApply 输出物化前都必须显式选择 profile。

如显式审查后采用多语言 profile，头部 language 值为 selected_languages 数组按逗号连接、无空格；每个制品格式行／链接仍只标记一种语言。先遍历模块，再遍历语言。初始三个 profile 仍为单语言。静态 profile JSON 拒绝重复键／未知字段；保留区域不代表标记本身就是所有权证明：旧回执和受管理区域摘要必须匹配。

### RD-14 — reference

在 RD-13 块内为所选制品逐个写有序 Markdown 链接：`- [<module_id>:<language>](<relative-path>) sha256=<sha256>`，后跟 LF，最后结束标记。路径从目标所在目录解析到不可变工作区本地快照 `fcop/internal/rule-distribution/packages/<manifest-sha256>/`，其中含精确 Manifest 和全部 18 份制品以完整验证身份；只引用或消费所选制品。链接使用 POSIX 分隔符；只允许到达该工作区内目录所需的确定性相对父目录，不得逃逸工作区。部署前及以后每次显式核验都必须验证快照字节。不允许远程／下载链接、机器包安装路径或未解析引用。Loader／引用行为及部署后变化需要独立 Host 证据，生成入口本身不证明 Runtime 核验。

### RD-15 — bounded_embed

共同块内按顺序拼接所选制品。每个制品先写 `<!-- fcop:module=<module_id>;language=<language>;sha256=<sha256> -->` 和 LF，然后原样写入 canonical 字节（本已恰好一个末尾 LF），再加一个 LF；最后结束标记及 LF。投影不摘要、不翻译、不按启发式删历史、不重复维护正文、不归一化字节。源内相对链接必须按声明的包内引用基准编写，并针对所选目标验证；未解析或错位链接停止，不静默指向其他位置。未来模块作者可使用固定权威链接，但投影不发明内容。任一模式超限均报错，不自动换模式、换语言或截断模块。

### RD-16 — 规划、所有权和部分失败

每个有副作用操作必须先提供零写入 dry-run：精确选择、来源／profile 摘要、目标前后摘要、逐目标 diff、字节合计、所有权冲突、备份／回执计划。dry-run 不创建目录、快照、备份或回执。首次写入前验证全部输入／目标并确认显式采用授权；每次替换前立即重查规划中的 before 摘要，陈旧计划拒绝。对重叠目标使用本地文件协调，仅串行化短暂分发提交，不锁 Agent 工作、不引入服务。

各目标在同目录暂存，持久化字节并校验，然后原子替换；不得先归档移走旧目标再准备持久替代。替换前保留经校验旧字节。不宣称多文件整体原子提交。部分失败后保留暂存／备份／证据，不追加成功回执，明确报告可证明的写入并停止，等待显式检查／回滚。不得把缺少回执猜成从未写入。无后台重放、新生命周期状态机；这是有限 Toolkit 部署失败处理，不复用 Core 授权或 NOW 回执。WP4C.4 必须证明每个物化边界的失败行为。

## 装配与兼容

### RD-17 — sequential

精确有序 selected_modules：

```json
["workspace","envelopes","relations","authorization","idempotency","recovery","lifecycle","compatibility"]
```

这是普通任务公共指导，包含 relations、普通 attempt／REPORT head、授权及 T1–T7，不加载 convergence，也不启用 Branch family／digest／Root 汇合操作。知道 branch_of 词汇或 REVIEW kind 不授予 Branch 能力。上下文选择不得豁免适用 Core 校验：本装配的 Branch／family 操作在显式采用 parallel 前不可用，不得用残缺指导尝试。授权 Profile 采用独立进行；profiles=[] 不因加载指导就能完成 T4–T7。本装配不包含开发手册、宪法、固定角色表、GAL 或调度器。

### RD-18 — parallel

精确有序 selected_modules：

```json
["workspace","envelopes","relations","authorization","idempotency","recovery","lifecycle","compatibility","convergence"]
```

相对 sequential 唯一增量是 convergence，必须显式选择，安装不自动启用并行。Branch 操作保留普通门和授权，再加冻结的准入／深度／family digest／汇合／终态检查。Core Branch 不是 Git branch／merge；不得重复关系义务或设独立 Branch 状态机。

### RD-19 — repository-development

这是仅仓库使用的有序引用束，不是第十个业务模块：(1) FCoP 开发入口；(2) 独立维护的 FCoP 开发指导；(3) 固定的当前 FCoP 合同；(4) 当前 TASK 及授权范围／Gate。引用必须固定路径、revision 和摘要；独立 ADMIN 采用的通用宪法只有在权利／来源／采用已明确后才可选地放在最前。目前不假定存在这种宪法。开发任务如使用协议协作，另行显式选择 sequential 或 parallel 业务包，不把开发内容注入业务包。本阶段不写完整新开发手册、Host 入口或实现。

### RD-20 — Legacy 隔离

保留 `src/fcop/rules/_data/` 非 v4 来源及 API 的 Legacy 范围；v4 模块不覆盖它们或四份旧 Host 输出。无版本旧 redeploy 调用保留 3.x 行为；v4 分发必须有明确 v4 工作区版本、Manifest 和已采用 Host profile，不得回退 legacy writer。不自动迁移现有工作区、不自动生成所有 Host、不拉取 latest。可重建 legacy 输出／兼容测试仍是后续验收要求；历史正文／版本／CRLF 差异必须明确记录，不能宣称相同或靠扩大旧文件修复。

### RD-21 — MCP 与 Relay

未来按版本选择的 `fcop://rules` 返回包 Manifest 或 typed-unavailable；`fcop://protocol` 返回规范身份而非 Host 状态。只读指导按工作区版本和显式选择读取已校验模块；legacy 资源保留版本合同。资源读取不得采用、部署、写回执、安装 Profile evaluator 或迁移。MCP 委托 Toolkit／Project 完成解析／摘要／选择／写入算法，不复制算法。Relay 只作可选传输，无规则权威／更新器。本轮不改已接受 WP4B 实现、46 个工具、11 个静态资源、三个模板；不静默修改冻结 F4.11.3 中历史数字 45。

### RD-22 — 类型化失败

分发失败属于 Toolkit，不是新 Base 错误。保留明确命名空间分类，并提供结构化 `code`、`operation`、`subject_ref` 及安全详情：`toolkit:RULE_MANIFEST_INVALID`、`toolkit:RULE_ARTIFACT_MISMATCH`、`toolkit:RULE_SELECTION_INVALID`、`toolkit:RULE_HOST_UNAVAILABLE`、`toolkit:RULE_PROJECTION_LIMIT`、`toolkit:RULE_OWNERSHIP_CONFLICT`、`toolkit:RULE_ADOPTION_REQUIRED`、`toolkit:RULE_DEPLOYMENT_RECOVERY_REQUIRED`。分别覆盖：非法／不支持的 schema 或图；缺失／非法／漂移字节或引用；未知／冲突／不完整选择；不支持／未证明的 Host 模式；超限；目标漂移／所有权／标记；缺失或无效的选择权威／回执；不确定部分写入或回滚证据。Core 本身失败时不得以此替代或重解释冻结 Base 错误。写前拒绝必须产生零项目写入。失败报告不泄露凭据，纯文字不是机器合同。现有 MCP typed-unavailable 在另行授权接入前保持不变。

## 分阶段验收

### RD-23 — 证据与后续所有权

决策附表覆盖 73 条款、147 个连续 legacy 单元、86 路径、12 消费者、四输出及全部基线冲突／编码／缓存／制品问题。future owner 是唯一实现／验证阶段，不是当前编辑许可。3.x 重建、v4 包原始字节一致性、进程／getter／index／部署／Host 失效边界、上下文字节及未知 Runtime 消费都保留为明确未来验收工作。reference 模式不得仅凭文件存在或 API 表面测试验收。

### RD-24 — 阶段 Gate 与停止

| 阶段 | 唯一职责 | 该阶段独立授权后请求的 Gate |
| --- | --- | --- |
| WP4C.2 | 先失败的分发／装配／漂移／冲突／回滚测试 | WP4C_2_DISTRIBUTION_CONFORMANCE_ACCEPTED |
| WP4C.3 | v4 canonical 模块、Manifest loader、三种最小装配 | WP4C_3_RULE_PACKAGE_ACCEPTED |
| WP4C.4 | Host 薄投影、显式部署、回执和回滚 | WP4C_4_HOST_PROJECTION_ACCEPTED |
| WP4C.5 | MCP 只读指导、3.x 兼容、FCoP 与 CodeFlowMu 只读 shadow | WP4C_5_COMPATIBILITY_ACCEPTED |
| WP4C.6 | 跨平台／制品／上下文与完整收口 | WP4C_RULE_DISTRIBUTION_ACCEPTED |

这些是分发候选合同的 Gate 标识，不是已签回执或任务书。每阶段需要独立固定 ADMIN 授权及前一阶段验收，不自动继续。本阶段只请求 `WP4C_1_RULE_DISTRIBUTION_CONTRACT_FROZEN`。任何 P0、来源／规范冲突、无法唯一映射的条款、双语差异、越权修改需要或被排除权威，都必须停止并提交事实报告，不请求 Gate。本轮不授权 WP4C.2、main 合并或发布。
