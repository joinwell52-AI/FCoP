---
title: "FCoP 4.0 WP4C.3：Canonical 规则模块、Manifest Loader 与最小装配任务书"
version: "1.0"
date: "2026-09-07"
document_role: "AUTHORIZED_TASKBOOK"
authority: "ADMIN"
repository: "joinwell52-AI/FCoP"
program: "FCOP_4_0"
work_package: "WP4C.3"
taskbook_branch: "taskbook/fcop-4.0-wp4c.3-rule-package-core"
parent_gate: "WP4C_2_DISTRIBUTION_CONFORMANCE_ACCEPTED"
parent_gate_evidence_head: "1f4df9cc650f63b9e842d806340eb31b768f708e"
parent_gate_comment: "https://github.com/joinwell52-AI/FCoP/pull/20#issuecomment-5566832805"
accepted_rule_contract_head: "f6831de12991010f22672fb6e776ce85ef1507ff"
frozen_fcop_contract: "aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6"
execution_authorized: true
authorized_scope: "WP4C_3_ONLY"
wp4c_4_wp4c_5_wp4c_6_status: "NOT_AUTHORIZED"
main_merge_authorized: false
release_authorized: false
pypi_publish_authorized: false
codeflowmu_change_authorized: false
---

# FCoP 4.0 WP4C.3：Canonical 规则模块、Manifest Loader 与最小装配任务书

## 0. 给执行 Codex 的直接指令

ADMIN 已基于 Manifest HEAD `1f4df9cc650f63b9e842d806340eb31b768f708e` 签署：

```yaml
GATE: WP4C_2_DISTRIBUTION_CONFORMANCE_ACCEPTED
GATE_DECISION: SIGNED
```

本任务书是 WP4C.3 的唯一执行入口。本轮只允许实现：

1. 九个 FCoP 4.0 canonical guidance 模块及双语 18 个制品；
2. 严格离线的 Distribution Manifest loader；
3. `sequential`、`parallel`、`repository-development` 三种最小装配选择；
4. WP4C.3 所属的八种 namespaced Toolkit 失败；
5. 唯一公共入口 `Project.rule_distribution(action, request)` 的最小接线。

完成后必须停止并请求：

```yaml
GATE: WP4C_3_RULE_PACKAGE_ACCEPTED
```

不得进入 Host 投影、规则文件部署、adoption receipt、deployment receipt、回滚、MCP 接入、CodeFlowMu shadow、RC、main 合并或发布。

---

## 1. 固定权威与执行起点

### 1.1 事实权威

按以下顺序解释事实：

1. 冻结 FCoP 4.0 规范：
   - `spec/fcop-4.0-spec.md`
   - `spec/fcop-4.0-spec.zh.md`
   - commit `aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6`
2. 冻结规则分发合同：
   - `docs/fcop-4.0/rule-distribution-contract.md`
   - `docs/fcop-4.0/rule-distribution-contract.zh.md`
   - accepted head `f6831de12991010f22672fb6e776ce85ef1507ff`
3. WP4C.1 决策与矩阵：
   - `reports/FCOP-4.0-WP4C.1-CONTRACT-DECISIONS.md`
   - `reports/FCOP-4.0-WP4C.1-CONFORMANCE-MATRIX.md`
4. WP4C.2a 固定符合性测试和红灯基线：
   - accepted head `1f4df9cc650f63b9e842d806340eb31b768f708e`
5. FCoP 3.2.5 代码与旧规则只作为兼容事实，不是 4.0 正文来源。

规范决定协议；规则分发合同决定分发；测试验证合同。测试、旧 AGENTS/CLAUDE/MDC 文本或实现均不得反向增加规范。

### 1.2 固定起点

执行者必须：

1. fetch GitHub 远端；
2. 读取本任务书所在的不可变 commit；
3. 验证其直接父提交为 `1f4df9cc650f63b9e842d806340eb31b768f708e`；
4. 验证父链包含冻结合同和已签 Gate；
5. 计算本任务书原始字节 SHA-256，与 ADMIN 下发值完全一致；
6. 从任务书 commit 创建独立 worktree。

建议：

```text
WORKTREE: D:\FCoP-wp4c3-rule-package-core
BRANCH: review/fcop-4.0-wp4c.3-rule-package-core
```

原 `D:\FCoP` 及此前 worktree 不得切换、清理、stash、reset、覆盖或吸收。若目标 worktree 已存在，先只读核验；不能证明归属时停止。

---

## 2. 单一目标和 Unix 边界

WP4C.3 的目标是把冻结合同表达成普通、可读、可校验、可装配的文件包：

```text
18 个 Markdown 制品 + 1 个 JSON Manifest
                  ↓
       小型离线 Loader / Selector
                  ↓
        明确选择后的字节与证据
```

坚持以下底线：

- 文件是规则事实，Manifest 只是索引和摘要证明；
- loader 是普通库函数，不是 Runtime；
- 不增加数据库、daemon、timer、watcher、scheduler、消息队列、远程规则服务或后台更新器；
- 不创建第二生命周期、第二授权系统、第二恢复系统；
- 不探测模型，不启动 Host，不访问网络，不自动安装规则；
- 不写工作区、不创建 receipt、不生成 AGENTS.md/CLAUDE.md/MDC；
- 不把 CodeFlowMu、PM/DEV/QA/OPS/EVAL、Session 或产品策略写进 FCoP 通用规则。

---

## 3. 本阶段唯一目标节点

WP4C.3 只负责冻结矩阵中以下 10 个 DIST ID、共 56 个行为节点：

| DIST | 节点数 | 合同 | 本阶段责任 |
| --- | ---: | --- | --- |
| DIST-01 | 2 | RD-01/02 | 权威、范围与新 Core 冒充拒绝 |
| DIST-02 | 4 | RD-03/19 | 普通业务与仓库开发输入隔离 |
| DIST-03 | 6 | RD-04/05 | 73 条款唯一主责与四关系精确集合 |
| DIST-04 | 11 | RD-06 | UTF-8/LF/BOM/C0/双语条款一致性 |
| DIST-05 | 9 | RD-07 | 严格 Manifest schema 与 18 制品 |
| DIST-06 | 6 | RD-07/08 | 原始字节、摘要、大小、路径与 symlink 边界 |
| DIST-07 | 4 | RD-08 | 无环依赖、显式选择与确定性排序 |
| DIST-21 | 2 | RD-17/18 | sequential 与 parallel 精确装配 |
| DIST-22 | 4 | RD-19 | repository-development 固定引用束 |
| DIST-25 | 8 | RD-22 | 八类 namespaced Toolkit 失败 |

验收目标：

```yaml
WP4C_3_TARGET_IDS: 10/10
WP4C_3_TARGET_NODES: 56/56
WP4C_3_TARGET_NODES_PASSED: 56/56
```

DIST-08–20 与 DIST-23–29 属于 WP4C.4–6，不得为了增加绿灯提前实现。DIST-30 已由 WP4C.2 关闭，仍应保持通过。

---

## 4. Canonical 模块与 Manifest

### 4.1 精确文件面

必须创建：

```text
src/fcop/rules/_data/v4/manifest.json

src/fcop/rules/_data/v4/workspace.en.md
src/fcop/rules/_data/v4/workspace.zh.md
src/fcop/rules/_data/v4/envelopes.en.md
src/fcop/rules/_data/v4/envelopes.zh.md
src/fcop/rules/_data/v4/relations.en.md
src/fcop/rules/_data/v4/relations.zh.md
src/fcop/rules/_data/v4/authorization.en.md
src/fcop/rules/_data/v4/authorization.zh.md
src/fcop/rules/_data/v4/idempotency.en.md
src/fcop/rules/_data/v4/idempotency.zh.md
src/fcop/rules/_data/v4/recovery.en.md
src/fcop/rules/_data/v4/recovery.zh.md
src/fcop/rules/_data/v4/lifecycle.en.md
src/fcop/rules/_data/v4/lifecycle.zh.md
src/fcop/rules/_data/v4/compatibility.en.md
src/fcop/rules/_data/v4/compatibility.zh.md
src/fcop/rules/_data/v4/convergence.en.md
src/fcop/rules/_data/v4/convergence.zh.md
```

不得增加第十个业务模块、catch-all 模块或产品模块。

### 4.2 正文生成原则

每个模块必须从冻结 4.0 条款重新编写 guidance，不得以 3.x 大规则文件为正文底稿做增量修补。

必须满足：

- 73 个完整冻结条款各有且只有一个 primary module；
- 模块内规范性段落引用其主责 F4 条款；
- 非规范示例显式标注，不能发明 Gate、角色或权限；
- 其他模块需要某条义务时只引用主责模块，不复制规范义务；
- `relations` 只承认 `parent`、`branch_of`、`subject_ref`、`references`；
- `sequential` 知道关系词汇但不启用 Branch family；
- `parallel` 相对 sequential 唯一增加 `convergence`；
- 中英文具有相同模块身份、条款集合、依赖、受众和行为含义；
- 不包含 Host 文件模板、CodeFlowMu 文本、外部工程宪法正文或旧 RC；
- 摘要 `87cf212d1cb75cefd0da6da7e5f0f4c7eaedbc231c784b985c3e2e51856abc4c` 的 CodeFlowMu `v1.0-rc.1` 必须被排除。

### 4.3 字节合同

所有 19 个文件必须：

- UTF-8；
- 任意位置无 BOM；
- 仅 LF；
- 结尾恰好一个 LF；
- 不含 TAB/LF 以外的 C0 控制字符和 DEL；
- Markdown 制品不包含 Host 投影保留标记；
- 摘要覆盖原始字节，不做换行归一化后比较。

### 4.4 Manifest 严格结构

`manifest.json` 必须严格实现 RD-07：

- 顶层仅 `manifest_schema`、`protocol_version`、`package_version`、`artifacts`；
- `manifest_schema = fcop-rule-distribution/v1`；
- `protocol_version = 4.0`；
- `package_version` 是精确候选版本，不得为 latest 或版本范围；
- artifacts 恰好 18 条；
- 每条仅包含合同规定的十个字段；
- 不包含 adoption、Host consumption、时间戳、绝对路径、进程或随机字段；
- JSON 重复键、未知字段、未知 schema 必须拒绝；
- Manifest 不自含自身摘要。

---

## 5. Loader 与选择器

### 5.1 公共入口

本阶段明确允许新增且只允许新增一个公共 Project 方法：

```python
Project.rule_distribution(*, action: str, request: Mapping[str, Any]) -> Mapping[str, Any]
```

实现可在 `src/fcop/v4/rule_distribution/**` 内自由拆分为小模块；`Project` 只做版本边界和转发。不得把算法堆入 `project.py`，不得建立第二 facade。

该入口只在明确的 FCoP 4.0 workspace 上可用。3.x Project 行为、签名和规则部署路径必须保持不变，不得自动转入 4.0。

### 5.2 本阶段可成功的 action

只有以下 action 可以完成成功结果：

| action | 成功责任 |
| --- | --- |
| `validate` | 严格验证 Manifest、18 制品、字节、条款主责和依赖图 |
| `select` | 按显式 assembly/languages/modules 生成确定性的只读选择结果 |
| `validate_operation_scope` | 验证所选装配是否完整指导某类操作，不授予生命周期权限 |

返回值必须是普通、稳定、可序列化的结构；不得包含当前时间、绝对机器路径、随机值或调用者未请求的隐式选择。

### 5.3 显式外部 Manifest

符合性测试会把候选 Manifest 放在临时目录。Loader 必须从 request 中的显式 `manifest_path` 读取，不得只信 bundled 路径，也不得把 filename/version 当成身份。

必须：

- 将 source_path 解析限制在 Manifest 所在目录；
- 拒绝绝对路径、`..` 逃逸及 symlink 逃逸；
- 先验证完整 Manifest 和全部 18 制品，再执行选择；
- 原始字节摘要和 size 同时匹配；
- 缓存如存在，必须由 Manifest/制品原始身份键控，不能只按版本键控；
- 不访问网络或可变 latest。

### 5.4 确定性排序

选择结果必须与 Manifest 数组顺序和目录枚举顺序无关：

1. 验证依赖与冲突；
2. 拒绝缺失依赖、环和不完整显式选择；
3. 模块按 `load_order`，再按 module_id Unicode code point 排序；
4. 语言按 request 中 `selected_languages` 的显式顺序；
5. `guidance` 必须由选中的原始模块字节确定性组合；
6. 相同输入在不同绝对目录和时间得到相同业务结果与摘要。

---

## 6. 三种最小装配

### 6.1 sequential

精确模块：

```json
["workspace","envelopes","relations","authorization","idempotency","recovery","lifecycle","compatibility"]
```

不包含 convergence。对 `create_branch` 等 Branch/family 操作，`validate_operation_scope` 必须返回 `toolkit:RULE_SELECTION_INVALID`，零写入。

### 6.2 parallel

精确模块为 sequential 加 `convergence`。它只能表示 guidance 完整：

```yaml
guidance_complete: true
lifecycle_authorized: false
```

不得创建 TASK、目录、授权、Profile evaluator 或生命周期效果。

### 6.3 repository-development

它不是第十个业务模块，也不返回业务 modules。只验证并返回四项固定引用：

1. FCoP 开发入口；
2. FCoP 开发指导；
3. 固定 FCoP 合同；
4. 当前 TASK/授权范围/Gate。

每项必须同时包含 path、revision、sha256。当前通用工程宪法允许缺席；不得用 CodeFlowMu RC 或旧讨论稿补位。普通 sequential/parallel 响应中不得出现 repository-development 正文或引用。

本阶段不编写完整开发手册，不获取外部宪法，不生成 Host 开发入口。

---

## 7. 八类 Toolkit 失败与未来动作边界

错误必须提供机器字段：

```yaml
code: toolkit:RULE_...
operation: <action>
subject_ref: <安全、非空引用>
details: <结构化且不泄露秘密>
```

八类错误精确为：

- `toolkit:RULE_MANIFEST_INVALID`
- `toolkit:RULE_ARTIFACT_MISMATCH`
- `toolkit:RULE_SELECTION_INVALID`
- `toolkit:RULE_HOST_UNAVAILABLE`
- `toolkit:RULE_PROJECTION_LIMIT`
- `toolkit:RULE_OWNERSHIP_CONFLICT`
- `toolkit:RULE_ADOPTION_REQUIRED`
- `toolkit:RULE_DEPLOYMENT_RECOVERY_REQUIRED`

不得加入冻结 Base Error 枚举，不得重解释 Core 错误。

为完成 DIST-25，允许 `inspect_profile`、`plan`、`apply`、`rollback` 进入统一的只读前置校验，但本阶段不得实现它们的成功副作用：

- 未知 Host/profile → `RULE_HOST_UNAVAILABLE`；
- 选择内容超限 → `RULE_PROJECTION_LIMIT`；
- 目标存在且无可证明所有权 → `RULE_OWNERSHIP_CONFLICT`；
- apply 缺少有效 adoption ref → `RULE_ADOPTION_REQUIRED`；
- rollback 缺少可验证 deployment/recovery ref → `RULE_DEPLOYMENT_RECOVERY_REQUIRED`。

若这些未来 action 的前置条件全部有效，本阶段必须明确返回 `toolkit:OPERATION_NOT_IMPLEMENTED` 或等价的既有“未授权阶段”错误，不能伪造成功、文件、计划、receipt 或 Gate。

所有写前拒绝必须对测试工作区零写入；错误详情不得回显 `secret-fixture-token` 等目标内容。

---

## 8. 明确禁止提前实现

WP4C.3 不得实现或修改：

- WP4C.4：Host profile 正向支持、plan/apply 成功、Host 文件投影、adoption/deployment receipt、回滚、部分写入恢复；
- WP4C.5：3.x/v4 MCP 资源路由、Relay、3.x 兼容重部署、缓存/进程层失效、CodeFlowMu shadow；
- WP4C.6：wheel/sdist 最终原始字节证明、跨平台完整矩阵、上下文字节测量和 RC 收口；
- AGENTS.md、CLAUDE.md、`.cursor/**`；
- MCP 工具与资源实现；
- CodeFlowMu；
- main、版本号、PyPI、GitHub Release。

不得修改冻结规范、冻结规则分发合同、WP4C.1 矩阵或 WP4C.2 符合性测试来迁就实现。不得删除断言、改 Test ID、增加 skip/xfail 或用测试专用成功后门。

---

## 9. 编码前必须完成的只读检查

先生成 `reports/FCOP-4.0-WP4C.3-IMPLEMENTATION-PLAN.md`，至少记录：

1. 任务书 commit、SHA-256、父链和 Gate；
2. 当前 `Project` v4 version boundary 与 handler 接线方式；
3. 当前 `src/fcop/rules/_data` 打包规则；
4. WP4C.2 的 56 个目标节点与其他 86 个未来节点；
5. 73 条款到九模块的唯一主责表；
6. 3.x 公共 surface 与规则文件字节基线；
7. 计划新增的生产文件及每个文件唯一职责；
8. 新公共方法签名和 public-surface snapshot 变更；
9. 为何不需要新依赖、Store、状态机、锁或后台组件。

若目标节点数、条款数、父链、合同或现有代码事实不一致，停止并报告 `INPUT_DRIFT`。

---

## 10. 允许修改范围

允许：

```text
src/fcop/rules/_data/v4/**                 # 精确 18 Markdown + 1 Manifest
src/fcop/v4/rule_distribution/**           # 新的私有小型 loader/selector
src/fcop/v4/creation.py                    # 仅 handler 注册
src/fcop/v4/boundary.py                    # 仅 Project 方法策略
src/fcop/project.py                        # 仅一个公共转发方法
pyproject.toml                             # 仅收录 v4 规则 package data
tests/test_fcop/test_v4_rule_distribution*.py
tests/test_fcop/snapshots/public_surface.json
CHANGELOG.md                               # 仅 [Unreleased] 增量记录
reports/FCOP-4.0-WP4C.3-*.md
reviews/fcop-4.0/wp4c.3/MANIFEST.md
```

若现有实现明确要求在 `src/fcop/v4/**` 的另一个既有文件做一行级公共接线，必须先在计划中解释并保持最小；不得借此修改 Core 生命周期、授权、幂等、恢复或汇合算法。

禁止：

```text
spec/fcop-4.0-spec*.md
docs/fcop-4.0/rule-distribution-contract*.md
reports/FCOP-4.0-WP4C.1-*.md
tests/conformance/rule_distribution_v4/**
tests/conformance/v4/**
mcp/**
AGENTS.md
CLAUDE.md
.cursor/**
.github/workflows/**
src/fcop/_version.py
CodeFlowMu任何文件
```

中文文件不得使用 PowerShell 重写或管道转换；必须保持原始 UTF-8/LF 字节合同。

---

## 11. 实现和验证顺序

### 11.1 先固定正文与 Manifest

1. 从冻结条款和 WP4C.1 ownership 表生成 18 个模块；
2. 完成双语义务核对；
3. 生成严格 Manifest；
4. 独立脚本核对 18/18、73/73、九模块、依赖无环和原始摘要；
5. 未通过前不得接公共 API。

### 11.2 再实现纯 Loader/Selector

1. 严格 JSON/UTF-8 读取；
2. 路径和 symlink containment；
3. 原始摘要、size、双语条款集合；
4. 图验证和确定性排序；
5. 三种装配；
6. Toolkit 错误；
7. Project 薄转发。

### 11.3 先跑定向目标

必须精确列出并运行 56 个 WP4C.3 节点。结果必须为 56/56 通过。

随后运行完整 Rule Distribution suite，并分类：

```yaml
META_STATIC: 33/33_PASS
WP4C_3_TARGET: 56/56_PASS
DIST_30_CONTROL: 1/1_PASS
FUTURE_OWNER_NODES: 86_EXPECTED_DEFERRED
UNEXPECTED_FAILURES: 0
UNEXPECTED_PASSES: 0
```

若未来节点意外通过，必须逐项证明未提前实现越权能力；不能证明则停止。

### 11.4 全量回归

至少执行：

- `tests/test_fcop` 全量；
- 冻结 `tests/conformance/v4` 119/119；
- `tests/test_fcop_mcp` 隔离回归；
- Rule Distribution Meta/Static 33/33；
- Rule Distribution 全量 collect-only 176；
- Ruff；
- mypy；
- public-surface snapshot；
- source/package-data 文件清单和原始字节核验；
- 构建 wheel/sdist并只检查 19 个 v4 规则文件是否被包含，不能把本阶段包装成 WP4C.6 制品验收。

3.x 新回归必须为 0。MCP 本阶段不得修改。

---

## 12. 必交付报告

必须生成：

```text
reports/FCOP-4.0-WP4C.3-IMPLEMENTATION-PLAN.md
reports/FCOP-4.0-WP4C.3-CLAUSE-AND-ARTIFACT-MAPPING.md
reports/FCOP-4.0-WP4C.3-CONFORMANCE-RESULT.md
reports/FCOP-4.0-WP4C.3-RESULT.md
reviews/fcop-4.0/wp4c.3/MANIFEST.md
```

映射报告必须逐项证明：

- 73/73 条款唯一主责；
- 18/18 制品及字节身份；
- 10/10 DIST ID、56/56 节点；
- 147 个 legacy 单元的既定 disposition 没有被正文机械回流；
- repository-development 与普通业务装配隔离；
- 当前缺席的通用宪法没有被其他来源替代。

---

## 13. 强制停止条件

出现以下任一情况立即停止，只提交事实报告，不请求 Gate：

- 任务书 SHA、父链或 Gate 不匹配；
- 冻结合同之间出现新的不可唯一解释冲突；
- 需要修改冻结规范、合同、矩阵或 WP4C.2 测试；
- 需要增加第十模块、第二公共 facade、数据库、后台组件或网络服务；
- 56 个目标节点无法在本阶段边界内完成；
- 需要实现 Host 投影、adoption、deployment、rollback、MCP 或 CodeFlowMu；
- 3.x 回归；
- 未来阶段节点出现无法解释的提前通过；
- 公共 surface 除 `Project.rule_distribution` 外发生漂移；
- 任何真实工作区出现非测试写入；
- 交付分支混入任务书以外来源或用户未提交文件。

---

## 14. GitHub 审核交付

执行分支：

```text
review/fcop-4.0-wp4c.3-rule-package-core
```

从固定任务书 commit 直接接出，不合并 PR #20，不 cherry-pick 未列入权威的分支。

交付采用两个提交：

1. Content commit：生产代码、19 个规则制品、单元测试和四份报告；
2. Manifest commit：仅 `reviews/fcop-4.0/wp4c.3/MANIFEST.md`。

Manifest 必须列出所有实际交付路径及其 Git blob 原始 SHA-256，不使用通配符代替文件清单。推送后：

1. 重新 fetch 远端 review ref；
2. 验证 Manifest → Content → taskbook 的直接父链；
3. 在固定 Manifest HEAD 从 GitHub 回读全部交付文件；
4. 逐文件比较远端、Git blob、本地工作字节 SHA-256；
5. 建立 Draft PR，base 为本 taskbook 分支；
6. 不修改 PR base 到 main 以制造 CI；
7. 若 CI 因分支过滤未触发，记录 `NOT_TRIGGERED_BRANCH_FILTER`，不得宣称全绿；
8. 不请求 reviewer、不启用 auto-merge、不合并。

完成后停止并请求 `WP4C_3_RULE_PACKAGE_ACCEPTED`。

---

## 15. 验收条件

- [ ] 任务书与父 Gate 验证通过；
- [ ] 19/19 canonical 文件存在；
- [ ] 九模块、两语言、73 条款唯一主责全部匹配；
- [ ] 严格字节、Manifest、路径、摘要和图验证完成；
- [ ] sequential、parallel、repository-development 精确；
- [ ] 八类 Toolkit 错误结构化且零写入；
- [ ] 唯一新增公共 API 为 `Project.rule_distribution`；
- [ ] WP4C.3 目标 56/56 通过；
- [ ] DIST-30 继续通过；
- [ ] 其他 86 节点保持有解释的后续红灯；
- [ ] FCoP/v4/MCP 回归全绿；
- [ ] 3.x 新回归 0；
- [ ] 无新依赖、Store、状态机、锁、后台组件或网络访问；
- [ ] 无 Host、MCP、CodeFlowMu、main、版本或发布变更；
- [ ] GitHub 两提交、直接父链及全部文件哈希核验通过。

---

## 16. 最终回执格式

```yaml
WP4C_3_STATUS: COMPLETE | BLOCKED | FAILED
AUTHORIZED_SCOPE: WP4C_3_ONLY

TASKBOOK_COMMIT: <sha>
TASKBOOK_SHA256: <sha256>
INPUT_HEAD: 1f4df9cc650f63b9e842d806340eb31b768f708e
PARENT_GATE: WP4C_2_DISTRIBUTION_CONFORMANCE_ACCEPTED
PARENT_GATE_COMMENT: https://github.com/joinwell52-AI/FCoP/pull/20#issuecomment-5566832805
ACCEPTED_RULE_CONTRACT_HEAD: f6831de12991010f22672fb6e776ce85ef1507ff
FROZEN_FCOP_CONTRACT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6

WORKTREE: D:/FCoP-wp4c3-rule-package-core
BRANCH: review/fcop-4.0-wp4c.3-rule-package-core

CANONICAL_MODULES: 9/9
CANONICAL_ARTIFACTS: 18/18
MANIFEST_FILES: 1/1
CLAUSE_OWNERSHIP: 73/73
SPEC_EN_ZH_PARITY: PASS
RAW_BYTE_VALIDATION: PASS
MANIFEST_GRAPH_VALIDATION: PASS

PUBLIC_ENTRY: Project.rule_distribution
NEW_PUBLIC_APIS: 1
WP4C_3_TARGET_IDS: 10/10
WP4C_3_TARGET_NODES: 56/56
DIST_30_CONTROL: 1/1
FUTURE_OWNER_NODES: 86_EXPECTED_DEFERRED
UNEXPECTED_FAILURES: 0
UNEXPECTED_PASSES: 0

TEST_FCOP: <actual>
V4_CORE_CONFORMANCE: 119/119
MCP_REGRESSION: <actual>
RULE_DISTRIBUTION_META: 33/33
RULE_DISTRIBUTION_COLLECT_ONLY: 176
V3_NEW_FAILURES: 0
RUFF: PASS
MYPY: PASS
PUBLIC_SURFACE_DRIFT: 0_AFTER_AUTHORIZED_ADDITION

NEW_RUNTIME_DEPENDENCIES: 0
NEW_BACKGROUND_COMPONENTS: 0
NEW_AUTHORITATIVE_STORES: 0
NEW_STATE_MACHINES: 0
NEW_LOCK_SYSTEMS: 0
NEW_BASE_ERROR_CODES: 0
HOST_PROJECTION_IMPLEMENTED: false
ADOPTION_DEPLOYMENT_IMPLEMENTED: false
MCP_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0
FROZEN_FILES_MODIFIED: 0

CONTENT_COMMIT: <sha>
MANIFEST_COMMIT: <sha>
REMOTE_HEAD: <sha>
REMOTE_PUSHED: true
REMOTE_REFETCH_VERIFIED: PASS
DELIVERY_SHA256: <matched>/<total>
DRAFT_PR_URL: <url>
CI_STATUS: PASS | NOT_TRIGGERED_BRANCH_FILTER
WORKTREE_STATUS: CLEAN

WP4C_3_RULE_PACKAGE_ACCEPTED: false
WP4C_4_STARTED: false
MAIN_MODIFIED: false
RELEASE_CREATED: false
REQUESTED_GATE: WP4C_3_RULE_PACKAGE_ACCEPTED
```

执行完成后必须停止。较早 Gate、测试通过或文件存在均不能自动授权 WP4C.4。
