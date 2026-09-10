---
document_role: EXECUTION_TASKBOOK
status: AUTHORIZED_FOR_WP4C_6_ONLY
authority: ADMIN
execution_authorized: true
authorized_scope: WP4C_6_ONLY
accepted_wp4c_5_head: 8a4e2b175938af8b28e2983161862b49e8650256
wp4c_5_gate_commit: b5c1e11a4fc05b4c659f69ddad09d3290840f86a
frozen_fcop_contract: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
frozen_distribution_contract: f6831de12991010f22672fb6e776ce85ef1507ff
frozen_distribution_test_tree: 4f99c7261b63b6db81c500604a231defaca9f14b
implementation_authorized: true
main_merge_authorized: false
release_authorized: false
codeflowmu_write_authorized: false
requested_gate: WP4C_RULE_DISTRIBUTION_ACCEPTED
---

# FCoP 4.0 WP4C.6：制品、上下文计量、跨平台与规则分发总收口任务书 v1.0

## 0. 任务结论

WP4C.5 已由 ADMIN 验收。本任务只完成规则分发合同 RD-23/RD-24 的最后二十个
既有红灯：`DIST-27` 两个制品节点与 `DIST-28` 十八个上下文计量节点，并完成
跨平台和整体闭合验证。

本阶段不是增加新产品能力的机会。禁止新增 Runtime、服务、数据库、Watcher、
Host 探测、在线更新器、通用构建系统或第二套规则解释器。允许的生产实现只有
两个窄动作及其私有小模块：

```text
Project.rule_distribution(action="build_artifacts")
Project.rule_distribution(action="measure_context")
```

二者仍通过既有 `Project.rule_distribution` 总线进入，不新增公共 facade。

## 1. 固定输入与开始条件

执行者必须从 GitHub 回读并核验：

1. 本任务书的固定 commit、SHA-256、字节数、UTF-8/no-BOM/LF；
2. 直接父提交必须是本任务书声明的 WP4C.5 Gate commit；
3. Gate 的直接父提交必须是 `8a4e2b175938af8b28e2983161862b49e8650256`；
4. Gate 必须签署 `WP4C_5_COMPATIBILITY_ACCEPTED`，且不得授权 merge/release；
5. Core 规范 `aec4c2b...`、分发合同 `f6831de...` 与冻结测试目录 tree
   `4f99c726...` 必须可达且字节不变；
6. `tests/conformance/rule_distribution_v4` 必须收集到既有节点，完整测试 ID 不得减少；
7. 初始完整分发结果应为 156 passed、恰好 20 个 WP4C.6 目标失败、0 skip/xfail、
   0 非预期失败；若集合不同立即停止。

从任务书固定提交建立独立 worktree：

```text
D:\FCoP-wp4c6-distribution-closeout
```

执行分支固定为：

```text
feat/fcop-4.0-wp4c.6-distribution-closeout
```

使用 `feat/**` 是为了让现有 GitHub Actions 对最终交付 HEAD 真正运行；不是 main
合并授权。不得修改 workflow 分支过滤器来制造绿灯。

原 `D:\FCoP`、既有 review 分支、PR #26–#28、CodeFlowMu 和 main 必须保持原样。
若原工作树有修改，不得切换或清理；只使用独立 worktree。

## 2. 唯一目标节点

目标集合必须精确等于：

- `DIST-27[wheel]`
- `DIST-27[sdist]`
- `DIST-28` 的 2 assemblies × 3 Hosts × 3 language selections，共 18 节点

不得把其他测试转绿解释为本阶段授权，不得新增/改名 Test ID，不得修改这两个
冻结测试函数、driver、全局 fixture 或任何冻结 Conformance 断言。

完成标准：上述 20/20 通过，完整分发测试 176/176 通过，且此前各阶段已通过的
156 个节点没有回退。

## 3. `build_artifacts` 最小合同

### 3.1 请求

在既有公共上下文字段之外，仅接受：

```yaml
output_directory: "绝对本地路径"
formats: [wheel] | [sdist] | [wheel, sdist]
offline: true
build_isolation: false
```

要求：

- `formats` 非空、无重复、只含 `wheel`/`sdist`；
- `offline` 必须显式为 `true`，`build_isolation` 必须显式为 `false`；
- 输出目录必须是调用方明确给出的本地普通路径，不得为 workspace、package 输入目录
  或它们的父目录，不得是 symlink/reparse/UNC/网络路径；
- 目标文件已存在、目录非空、路径不安全或请求多余字段时，Fail Closed；
- 先完整验证 Manifest 和 18 个模块，再产生任何输出；验证失败零写入；
- 不访问网络，不下载包，不调用 shell，不读取用户配置，不写缓存或 workspace；
- 不把它扩展成 PyPI/GitHub Release 发布器。

### 3.2 内容

每个输出制品必须包含 `fcop/rules/_data/v4/` 下的精确 19 个文件：

- `manifest.json`；
- 九模块 × en/zh 的 18 个 Markdown 文件。

这些成员的路径集合、原始字节、字节数和 SHA-256 必须与已验证输入完全相等，
不得做换行转换、重新序列化、翻译或压缩前改写。不得包含：

- AGENTS.md、CLAUDE.md、`.cursor/rules/fcop-v4.mdc`；
- adoption/deployment/backup/operation receipts；
- CodeFlowMu `v1.0-rc.1` 或其他外部宪法；
- workspace 身份、Host 状态、绝对路径或凭据。

归档成员顺序和元数据必须确定，时间戳固定，不能使用当前时间或随机值。相同输入
在同平台重复构建应得到相同制品摘要；跨平台至少要求成员路径与成员原始字节完全
相同。若实现能保证完整 archive 摘要跨平台一致，应记录；不能保证时不得虚报。

该动作是离线 Toolkit 制品验证/导出，不是 Core、Runtime 或 Host 的职责。优先使用
Python 标准库和既有 package loader；不得增加 Runtime 依赖。允许在单一私有模块中
实现窄归档写入，不得创建通用 build framework。

### 3.3 返回值

至少返回：

```yaml
artifacts:
  wheel: "<实际绝对输出路径>"
  sdist: "<实际绝对输出路径>"
member_count: 19
manifest_sha256: "<已验证 Manifest 摘要>"
offline: true
```

只返回实际请求且成功产生的格式。不得声称上传、安装、采用或 Runtime 消费成功。

## 4. `measure_context` 最小合同

### 4.1 请求和输入边界

在既有显式 Manifest、Host profile、assembly、modules、languages 选择字段之外，只接受：

```yaml
historical_surfaces:
  - path: "绝对本地普通文件路径"
    sha256: "64位小写十六进制"
```

要求：

- 当前合同精确接受 6 个历史表面；不递归、不枚举目录；
- 每项只允许 `path`、`sha256`，路径唯一且摘要绑定精确原始字节；
- 拒绝 symlink/reparse/UNC、目录、缺失、变化中、重复或摘要不符的输入；
- 先验证完整 package、profile、selection 和全部历史输入，再返回；
- 纯只读，零 workspace/Host/receipt/output 写入，零网络、零缓存；
- 不能从 Host 名称猜模型窗口，不能探测 Host，不能删除或压缩历史材料。

### 4.2 计量语义

`projection_size_bytes` 必须调用或复用既有确定性 Host projection 结果，以最终完整
投影的 UTF-8 原始字节数计量，包含 framing、frontmatter、模块标记、空行和 final LF；
不得复制另一份 projection 算法。

固定披露：

```yaml
limit_unit: utf8_bytes
estimator:
  algorithm: exact-utf8-byte-count
  version: "1"
runtime_consumption_verified: null
```

每个历史表面只报告固定输入事实，至少包含 `path`、`sha256`、`size_bytes`。不得输出
文件正文，不得声称 token 精确值、上下文已注入或 Host 已消费。

返回的 `selected_modules`、`selected_languages` 必须与明确选择一致；顺序不得受目录、
平台或映射迭代影响。相同字节输入在 Windows/Linux/macOS 产生相同数值结果。

## 5. 代码范围

允许修改：

- `src/fcop/v4/rule_distribution/__init__.py`：仅接入两个动作；
- 最多两个新的私有小模块，例如 `_artifacts.py`、`_measurement.py`；
- 为复用既有纯 projection/loader 所必需的最小私有重构；
- 普通单元测试、打包/安装探针、CHANGELOG 的 additive `[Unreleased]` 条目；
- WP4C.6 报告和 Manifest。

禁止修改：

- `spec/fcop-4.0-spec*.md`、分发合同和冻结 Gate；
- `tests/conformance/rule_distribution_v4/**`；
- Schema、MCP 公共工具/资源/模板数量与既有 46/12/4 表面；
- v3 行为、Host profile 字段、采用/部署/回滚/Shadow 语义；
- CodeFlowMu 及其 3.2.5 固定版本；
- project 版本号、PyPI 配置、release workflow、main；
- 新公共 API、新 Base 错误码、新状态机、新锁系统、新权威 store；
- 新 Runtime 依赖、后台线程/进程、daemon、watcher、registry、数据库或网络服务。

若两个动作无法在以上范围内实现，立即停止，不能用扩大架构来“完成测试”。

## 6. 必须新增的普通测试

除冻结 DIST-27/28 外，至少覆盖：

1. wheel/sdist 19 个成员路径、字节、摘要精确一致；
2. 同输入重复构建确定性；
3. 非法 format、联网/隔离请求、已占用输出、symlink/reparse、Manifest/模块漂移均拒绝；
4. 拒绝前 workspace 与输出位置零效果；
5. 制品不包含 Host 输出、receipt、外部宪法或 CodeFlowMu 内容；
6. `measure_context` 六项原始字节大小与摘要；
7. 三 Host、两 assembly、三 language selection 的 18 个结果与真实 projection 字节一致；
8. 缺失/重复/多余字段、摘要漂移、路径变化和 symlink/reparse 输入拒绝且零写入；
9. 计量实现不复制 projection 算法，不读取模型/Host 运行信息；
10. Windows/Linux/macOS 路径与换行差异不改变 canonical member bytes 或计量值；
11. v3 `Project.rule_distribution` 对两个 v4-only 动作 Fail Closed，不创建输出；
12. MCP 表面与 WP4C.5 的 46/12/4 snapshot 不漂移。

不得 mock 成功结果代替公共生产入口，不得加 sleep/retry 掩盖竞态，不得修改断言、
skip、xfail 或 Test ID。

## 7. 验证矩阵

在固定最终候选字节上按顺序执行并保存机器可复核输出：

1. `DIST-27/28`：20/20；
2. Rule Distribution 全套：176/176；
3. v4 Core Conformance：119/119；
4. `tests/test_fcop` 全量；
5. `tests/test_fcop_mcp` 隔离全量；
6. FCoP + Core + MCP 串行组合全量，0 failure/skip/xfail；
7. Ruff、mypy FCoP、mypy MCP；
8. public-surface snapshot：不得出现新 facade；
9. source → wheel/sdist → clean install 的 19 个 canonical rule-package byte parity；
10. 安装后真实 stdio MCP：46 tools、12 static resources、4 templates；
11. CodeFlowMu 固定 ref 只读 Shadow，零写入且仍固定 `fcop==3.2.5`、`fcop-mcp==3.2.5`；
12. fresh LF checkout 与全部交付文件远端 SHA-256；
13. 最终 Manifest HEAD 的 GitHub Actions。

跨平台最低要求：

- Windows：支持的 Python 矩阵；
- Linux：支持的 Python 矩阵；
- macOS：支持的 Python 矩阵；
- 每个平台实际运行 DIST-27/28、FCoP package 与 MCP package 的相关测试；
- 不得用“类型检查通过”代替 native tests；
- 最终 HEAD 所有适用 workflow/check 必须成功。未触发、pending、cancelled、skipped、
  neutral 或只在旧 commit 上成功，都不能写 `GITHUB_CI_AT_FINAL_HEAD: PASS`。

如果现有 workflow 不执行 WP4C.6 新测试，允许在本阶段对既有测试命令做最小 additive
接线，但不得放宽 branch protection、删除检查、改失败为 continue-on-error 或修改发布流程。

## 8. GitHub 交付

建立新的 Draft PR。base 为本任务书固定分支；执行分支使用第 1 节固定 `feat/**`。
禁止复用或改写 PR #28。

提交必须至少分为：

1. **Content commit**：实现、普通测试、必要的最小 CI 测试接线、CHANGELOG 和四份报告；
2. **Manifest-only commit**：只新增 `reviews/fcop-4.0/wp4c.6/MANIFEST.md`。

报告：

- `reports/FCOP-4.0-WP4C.6-IMPLEMENTABILITY-PROOF.md`
- `reports/FCOP-4.0-WP4C.6-ARTIFACT-PARITY.md`
- `reports/FCOP-4.0-WP4C.6-CONTEXT-MEASUREMENT.md`
- `reports/FCOP-4.0-WP4C.6-RESULT.md`
- `reviews/fcop-4.0/wp4c.6/MANIFEST.md`

Manifest 必须列出固定输入、实际修改文件、测试节点、平台矩阵、制品成员/摘要、交付
文件 byte/hash、Content/Manifest 提交和真实 CI。推送后重新 fetch，核对父链、远端
原始字节、所有交付 SHA-256、fresh checkout、工作树干净、main 未变。

不得 auto-merge、retarget main、发布 tag/release/PyPI 或创建 CodeFlowMu 任务。

## 9. 强制停止条件

出现任一情况立即停止，提交事实报告；`REQUESTED_GATE: NONE`：

- 固定输入/Gate/taskbook/hash/tree 不一致；
- 初始 20 红灯集合或 156 既有通过节点不一致；
- 需要修改冻结测试、规范、分发合同、Schema 或 MCP 公共面；
- 需要新增 Runtime 依赖、服务、数据库、网络、后台组件、公共 facade 或状态机；
- 制品成员字节发生换行/序列化漂移，或包含被禁止的内容；
- 计量需要复制 projection 算法或探测 Host/model；
- 任一旧测试回退、出现非预期失败或 v3 行为漂移；
- 任一支持平台没有实际 native tests；
- 最终 Manifest HEAD CI 未触发或不是全绿；
- CodeFlowMu 被写入、main 改变或发布动作发生。

阻断报告可推送到当前 Draft PR，但不得请求验收 Gate。

## 10. 完成回执

完成后必须提供：

```yaml
WP4C_6_STATUS: COMPLETE
AUTHORIZED_SCOPE: WP4C_6_ONLY
TASKBOOK_COMMIT: ""
TASKBOOK_SHA256: ""
INPUT_HEAD: 8a4e2b175938af8b28e2983161862b49e8650256
WP4C_5_GATE_COMMIT: ""
FROZEN_DISTRIBUTION_CONTRACT: f6831de12991010f22672fb6e776ce85ef1507ff
FROZEN_DISTRIBUTION_TEST_TREE: 4f99c7261b63b6db81c500604a231defaca9f14b
DIST_27: 2/2
DIST_28: 18/18
RULE_DISTRIBUTION_FULL: 176/176
V4_CORE_CONFORMANCE: 119/119
TEST_FCOP: ""
MCP_REGRESSION: ""
COMBINED_REGRESSION: ""
ARTIFACT_MEMBERS: 19/19
ARTIFACT_RAW_BYTE_PARITY: PASS
REPEAT_BUILD_DETERMINISM: PASS
CONTEXT_MATRIX: 18/18
CONTEXT_ESTIMATOR: exact-utf8-byte-count/v1
RUNTIME_CONSUMPTION_VERIFIED: null
WINDOWS_NATIVE: PASS
LINUX_NATIVE: PASS
MACOS_NATIVE: PASS
GITHUB_CI_AT_FINAL_HEAD: PASS
NEW_PUBLIC_APIS: 0
NEW_RUNTIME_DEPENDENCIES: 0
NEW_BACKGROUND_COMPONENTS: 0
NEW_AUTHORITATIVE_STORES: 0
NEW_STATE_MACHINES: 0
MCP_SURFACE: 46_tools_12_static_4_templates
CODEFLOWMU_FILES_MODIFIED: 0
CONTENT_COMMIT: ""
MANIFEST_COMMIT: ""
REMOTE_HEAD: ""
REMOTE_REFETCH_VERIFIED: PASS
DELIVERY_SHA256: ""
WORKTREE_STATUS: CLEAN
MAIN_MODIFIED: false
RELEASE_CREATED: false
WP4C_RULE_DISTRIBUTION_ACCEPTED: false
REQUESTED_GATE: WP4C_RULE_DISTRIBUTION_ACCEPTED
```

完成后必须停止。不得自行签署总 Gate、合并 main、发布 FCoP 4.0 或开始任何下游适配。
