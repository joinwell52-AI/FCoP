---
document_role: EXECUTION_TASKBOOK
status: AUTHORIZED_FOR_WP4C_5B_ONLY
authority: ADMIN
execution_authorized: true
authorized_scope: WP4C_5B_ONLY
resumes_stage: WP4C.5
resumed_scope: FULL_WP4C_5
blocked_delivery_head: c3ef6ccba14a93ac73935ae729b5f9b681693138
accepted_wp4c_4_head: d29e4d41ad4e1fc74e6d3513faa6b95d97ba0dfb
wp4c_4_gate_commit: a9c810296aadf857438a1711b6a56fa63deaf4e9
original_wp4c_5_taskbook: 3e48a344b3bf16c2ed45671a7fb458b14f50dd6e
wp4c_5a_taskbook: c7986fb618b2f66c4ad2b157917f64a00bccf1c3
frozen_fcop_contract: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
frozen_distribution_contract: f6831de12991010f22672fb6e776ce85ef1507ff
pre_correction_conformance_tree: 1134d730e4c5ab23aa7b3ec91138da6981c2f009
post_correction_conformance_tree: 4f99c7261b63b6db81c500604a231defaca9f14b
fixture_correction_authorized: true
implementation_authorized: true
codeflowmu_write_authorized: false
main_merge_authorized: false
release_authorized: false
wp4c_6_authorized: false
requested_gate: WP4C_5_COMPATIBILITY_ACCEPTED
---

# FCoP 4.0 WP4C.5b：v3 Protocol 表示边界勘误与 WP4C.5 续作任务书 v1.0

## 0. ADMIN 裁定

PR #27 的停止有效。冲突不是生产实现缺陷，而是冻结 DIST-24 将 v4 `fcop://protocol` 的身份对象断言无条件施加给了 v3，同时 RD-21、WP0 资源处置、原 WP4C.5 任务书和现有 MCP 公共合同都要求 v3 保留原 Markdown 内容。

ADMIN 采用最小、向后兼容的裁定：

| 层 | v3 `fcop://protocol` | v4 `fcop://protocol` |
|---|---|---|
| `Project.rule_distribution(action="read_resource")` 的 `content` | 原 legacy Markdown `str` | `{path, revision, sha256}` typed identity object |
| MCP 公共资源 | 与既有 getter 完全相同的 Markdown 字节 | 将 Project 身份对象确定性渲染为 Markdown |
| MCP URI | `fcop://protocol` | `fcop://protocol` |
| MCP MIME | `text/markdown` | `text/markdown` |

因此：

1. v3 不改成 JSON，不增加隐藏 `.keys()`，不包装成伪字符串；
2. v4 的内部语义对象保持冻结测试要求；
3. MCP 只是表示层，不重新读取规范、不重新算规范身份、不复制版本路由；
4. “语义等价”不等于 Python 类型或传输字节完全相同；
5. 现有 URI 和 MIME 的 additive-only 承诺保持；
6. Relay 对同版本同 URI 返回与 MCP direct 完全相同的表示字节。

本裁定只修正一个错误适用范围，不重开 RD-21，不改变 v3 内容合同，也不增加新的协议层。

## 1. 唯一授权组合

完整执行授权由以下三份固定任务书共同组成：

1. WP4C.5 原任务书：功能范围与禁止项；
2. WP4C.5a：有效 Conformance 基线身份；
3. 本 WP4C.5b：DIST-24 单点 fixture 修正及 Project/MCP 表示边界。

仅以下内容以本文件为准：

- 原任务书 §7.2 中 v3 `fcop://protocol` 明确返回 legacy Markdown string；
- 原任务书 §7.3 的“JSON 对象确定性 JSON”不适用于既有 MIME 固定为 `text/markdown` 的 `fcop://rules` 和 `fcop://protocol` MCP 表示；
- 这两个 v4 MCP 资源必须由 Project typed result 确定性渲染为 Markdown；
- 允许第 2 节唯一 frozen fixture 修正。

其他功能、12+4 MCP 资源面、CodeFlowMu 零写入、13 个目标节点、GitHub 交付和 WP4C.6 禁止项不变。

执行前必须从 GitHub 固定 ref 回读本文件，核对 commit、直接父提交、SHA-256、字节数、UTF-8、无 BOM、LF。任一不一致立即停止。

## 2. 唯一允许的冻结 fixture 修正

允许修改且只允许修改：

```text
tests/conformance/rule_distribution_v4/test_dist_21_24_assembly_compat_mcp.py
```

修改前 Git 身份：

```yaml
bytes: 6175
blob: ad7781c0a9fe417b3f750f2e3044891ca5f98fdb
directory_tree: 1134d730e4c5ab23aa7b3ec91138da6981c2f009
```

唯一允许的语义修改：

```diff
-    elif resource == "fcop://protocol":
+    elif version == "4.0" and resource == "fcop://protocol":
```

不得修改该分支内两条身份断言。v3 case 自动落入已有最终 `else`，继续断言内容非空；其精确 legacy Markdown 合同由 MCP/Project 专项回归锁定。

修改后原始文件身份必须精确为：

```yaml
bytes: 6196
sha256: 72b4c5a621775487b10b60dc789c27a67ecfd5a81eda28cc3563cbe6c878b572
blob: a3b831161d415a2aa7906688ceab9273b0dea090
directory_tree: 4f99c7261b63b6db81c500604a231defaca9f14b
```

要求：

- 原 Test ID `DIST-24`、8 个参数化节点、断言总意图全部保留；
- 不改 driver、全局 fixture、其他 frozen 文件；
- 不增加 skip、xfail、条件返回或只为测试制造的生产分支；
- 修正后必须先提交独立的 **Fixture-alignment commit**，该提交只能修改这一文件；
- 若 resulting blob/tree 不等于上述固定身份，立即停止，不得自行更新本任务书摘要。

## 3. Project 语义返回合同

`Project.rule_distribution(action="read_resource")` 必须返回一个稳定顶层结果，至少包含：

```yaml
resource_uri: fcop://protocol
protocol_version: "3.0 | 4.0"
content: "<version-specific typed content>"
sha256: "<source payload sha256>"
mime_type: text/markdown
```

版本规则：

- v3 `content` 必须是现有 `fcop.rules.get_protocol_commentary()` 的原 Markdown `str`，UTF-8 编码后的字节和 SHA-256 完全相同；
- v4 `content` 必须是 identity dict，精确包含或至少包含 `path`、`revision`、`sha256`，不得含 `entry_generated`、Host 状态或 Runtime consumption；
- v3/v4 都由 workspace 的明确协议版本选择；版本未知或矛盾时 Fail Closed；
- 同一版本的 `stdio-local` 与 `relay-inprocess/network=false` 顶层语义结果相同；
- 读取全程零写入、零采用、零部署、零 evaluator 安装和零迁移。

禁止为了统一类型，把 v3 Markdown 包进 identity dict，或把 v4 identity 降成无法机器解析的自由文本。

## 4. MCP 表示合同

现有 ADR 与测试已经把 `fcop://protocol` URI、`text/markdown` MIME 和非空文本固定为公共合同。MCP 适配必须保持：

### 4.1 v3

- 返回值与 `fcop.rules.get_protocol_commentary()` 完整文本相等；
- MIME 仍为 `text/markdown`；
- 不增加 JSON wrapper、额外 header、version banner 或尾部元数据；
- 原 117608 字节/既有摘要是 PR #27 的实测证据；执行时应重新核验当前固定 getter，不把报告数值硬编码进生产。

### 4.2 v4

- MCP 调用一次 Project `read_resource` 获取 identity object；
- 只做确定性 Markdown 表示，不重新读 spec 或计算 spec identity；
- 固定字段顺序为 `path`、`revision`、`sha256`；
- UTF-8、LF、无 BOM，不含绝对机器路径、当前时间、随机值、Host 状态；
- MIME 保持 `text/markdown`；
- 表示函数必须小且纯，只负责 typed-object → text，不成为第二协议解释器。

建议固定表示：标题加三行字段，具体标点可由实现选择一次后用 exact-byte unit test 锁定。不得将 JSON 文本伪装成 Markdown 合同，也不得改变静态资源注册 MIME。

### 4.3 `fcop://rules` 同类边界

为避免下一处相同冲突，本任务书同时明确：

- Project v4 `fcop://rules` 的 `content` 仍是 Manifest typed object，满足 DIST-24；
- MCP 既有 `fcop://rules` URI/MIME 保持 `text/markdown`；
- v3 返回旧 rules Markdown 原文；
- v4 将 Project Manifest 对象确定性、完整地渲染为 Markdown（可含 canonical JSON code block），不得重新读取或重算 Manifest；
- 渲染结果必须可无损恢复全部 Manifest 字段，并有 exact-byte test；
- 这不改变本阶段新增 `fcop://team` 与 `fcop://guidance/{assembly}/{language}` 的既定 MIME 选择。

## 5. 必须增加的非冻结测试

在原 WP4C.5 测试要求之外，必须新增或扩展普通 unit/MCP tests，证明：

1. v3 Project protocol `content` 是 `str`，与 legacy getter 完全相等；
2. v3 MCP protocol 文本、MIME、URI 与旧合同完全相等；
3. v4 Project protocol `content` 是 identity dict，三字段正确绑定冻结规范；
4. v4 MCP protocol 是确定性 Markdown，三字段与 Project object 一致；
5. v3/v4 rules 分别保持 legacy 原文和 Manifest typed object/确定性 Markdown 投影；
6. direct 与 Relay in-process 对每个版本返回相同 MCP 表示；
7. 所有资源读取前后 workspace snapshot 相等；
8. MCP adapter 不直接调用 spec/rules getter、Manifest loader 或摘要算法来绕过 Project；
9. `resources/list` 中旧 URI/MIME 不漂移；最终资源计数仍按原任务书为 46 tools、12 static、4 templates；
10. 未知版本和 v3/v4 交叉输入 Fail Closed。

不得用 mock 成功值代替生产入口，也不得复制 Project 算法到测试 oracle。

## 6. 续作步骤

1. 从本任务书固定提交创建独立 worktree：
   `D:\FCoP-wp4c5b-protocol-resume`；
2. 分支：`review/fcop-4.0-wp4c.5b-protocol-resume`；
3. 完整读取三份任务书、PR #27 两份报告和 Manifest；
4. 验证 pre-correction tree `1134d730…`；
5. 执行第 2 节唯一修改，提交独立 Fixture-alignment commit，并验证 post-correction tree `4f99c726…`；
6. 重跑 DIST-24 8 节点及现有 5 项 MCP 资源检查，确认 fixture 修正没有把未实现行为冒充完成；
7. 完成原 WP4C.5 的 Implementability Proof 和全部实现；
8. 跑完 13/13 目标、FCoP、v4 Core、MCP、分发全量、安全、Shadow、Ruff、mypy 与 public-surface 验证；
9. GitHub 三提交交付并停止，请求 `WP4C_5_COMPATIBILITY_ACCEPTED`。

## 7. 允许与禁止范围

除原 WP4C.5 允许范围外，本轮额外只允许：

- 第 2 节唯一 frozen test 条件修正；
- 为 v3/v4 Project/MCP 表示边界新增普通测试；
- 在 `mcp/src/fcop_mcp/resources.py` 或单一私有纯 renderer 中做最小表示接线。

继续禁止：

- 修改其他冻结测试、Core、Schema、RD 合同或 CodeFlowMu；
- 改旧 URI、旧 MIME、v3 Markdown 字节来源或 MCP tool 面；
- 新增协议 wrapper、通用序列化框架、缓存、Registry、数据库、网络或后台组件；
- 让 MCP 自己判定 workspace version、读取规范身份或计算 canonical digest；
- 修改 main、版本号、release 或进入 WP4C.6。

## 8. GitHub 交付

PR #27 保持 BLOCKED 历史，不修改、不复用。新 Draft PR 的 base 为本任务书固定分支。

提交顺序固定为三笔：

1. Fixture-alignment commit：仅一个 frozen test 文件；
2. Content commit：实现、普通测试、snapshot、CHANGELOG、五份新的 WP4C.5B 报告；
3. Manifest-only commit：只新增 `reviews/fcop-4.0/wp4c.5b/MANIFEST.md`。

报告路径：

1. `reports/FCOP-4.0-WP4C.5B-IMPLEMENTABILITY-PROOF.md`
2. `reports/FCOP-4.0-WP4C.5B-VERSIONED-RESOURCE-MAPPING.md`
3. `reports/FCOP-4.0-WP4C.5B-LEGACY-AND-LAYER-ISOLATION.md`
4. `reports/FCOP-4.0-WP4C.5B-CODEFLOWMU-SHADOW.md`
5. `reports/FCOP-4.0-WP4C.5B-RESULT.md`
6. `reviews/fcop-4.0/wp4c.5b/MANIFEST.md`

远端回读、全部交付 SHA-256、fresh LF checkout、工作树干净、main 未变和真实 CI 状态按原任务书执行。CI 未触发不得写 PASS。

## 9. 强制停止条件

除前两份任务书停止条件外，出现以下任一情况立即停止：

- 单点修正后的文件 blob 或目录 tree 不等于固定值；
- 需要第二处 frozen test 修改；
- v3 protocol/rules 原 Markdown 字节或 MIME 漂移；
- v4 Project identity/Manifest object 只能靠 MCP 重新计算；
- MCP renderer 需要网络、缓存、全局状态或新公共 facade；
- direct 与 Relay 表示不一致；
- 任何资源读取产生 workspace 写入；
- PR #27 阻断历史被覆盖；
- 任一 WP4C.5 目标未通过或出现新回归。

阻断时 `REQUESTED_GATE: NONE`，不得进入 WP4C.6。

## 10. 完成回执补充字段

除原 WP4C.5 第 16 节字段外，必须增加：

```yaml
WP4C_5B_STATUS: COMPLETE
AUTHORIZED_SCOPE: WP4C_5B_ONLY
RESUMED_SCOPE: FULL_WP4C_5
BLOCKED_DELIVERY_HEAD: c3ef6ccba14a93ac73935ae729b5f9b681693138
PRE_CORRECTION_CONFORMANCE_TREE: 1134d730e4c5ab23aa7b3ec91138da6981c2f009
POST_CORRECTION_CONFORMANCE_TREE: 4f99c7261b63b6db81c500604a231defaca9f14b
FIXTURE_CORRECTION_FILES: 1/1
FROZEN_TEST_IDS: 60/60
V3_PROTOCOL_PROJECT_SHAPE: LEGACY_MARKDOWN_STRING
V3_PROTOCOL_MCP_BYTES: PRESERVED
V3_PROTOCOL_MIME: text/markdown
V4_PROTOCOL_PROJECT_SHAPE: IDENTITY_OBJECT
V4_PROTOCOL_MCP_SHAPE: DETERMINISTIC_MARKDOWN
MCP_ADAPTER_ALGORITHM_COPIES: 0
WP4C_5_TARGET_NODES: 13/13
CONFORMANCE_FILES_MODIFIED_THIS_RUN: 1
PR27_BLOCKER_PRESERVED: true
WP4C_5_COMPATIBILITY_ACCEPTED: false
WP4C_6_STARTED: false
REQUESTED_GATE: WP4C_5_COMPATIBILITY_ACCEPTED
```

完成后必须停止。不得自行签署 Gate、进入 WP4C.6、合并 main 或发布。
