---
document_role: EXECUTION_TASKBOOK
status: AUTHORIZED_FOR_WP4C_5A_ONLY
authority: ADMIN
execution_authorized: true
authorized_scope: WP4C_5A_ONLY
resumes_stage: WP4C.5
resumed_scope: FULL_WP4C_5
blocked_delivery_head: df395c7e221f850352d907933ccaab0937706c8f
accepted_wp4c_4_head: d29e4d41ad4e1fc74e6d3513faa6b95d97ba0dfb
wp4c_4_gate_commit: a9c810296aadf857438a1711b6a56fa63deaf4e9
original_wp4c_5_taskbook: 3e48a344b3bf16c2ed45671a7fb458b14f50dd6e
frozen_fcop_contract: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
frozen_distribution_contract: f6831de12991010f22672fb6e776ce85ef1507ff
origin_distribution_conformance: 1f4df9cc650f63b9e842d806340eb31b768f708e
effective_distribution_conformance_ref: d29e4d41ad4e1fc74e6d3513faa6b95d97ba0dfb
effective_distribution_conformance_tree: 1134d730e4c5ab23aa7b3ec91138da6981c2f009
authorized_conformance_corrections:
  - e1ed85e4ba5aba212ddf3cc4f880c0abecc2bfab
  - 115751b4c24a1924062a81a21e0d655e8cb5fedc
implementation_authorized: true
codeflowmu_write_authorized: false
main_merge_authorized: false
release_authorized: false
wp4c_6_authorized: false
requested_gate: WP4C_5_COMPATIBILITY_ACCEPTED
---

# FCoP 4.0 WP4C.5a：有效 Conformance 基线勘误与 WP4C.5 续作任务书 v1.0

## 0. ADMIN 裁定

PR #26 的 `INPUT_INTEGRITY_BLOCKED` 停止是正确行为。阻断证据确认：原 WP4C.5 任务书把 WP4C.2 的原始冻结提交 `1f4df9c…` 写成当前全部测试文件都必须逐字节相同的唯一身份，同时又指定已经包含两次获准测试修正的 WP4C.4 验收提交 `d29e4d4…` 为输入。这两个要求不能同时成立。

ADMIN 现作如下唯一裁定：

1. `1f4df9cc650f63b9e842d806340eb31b768f708e` 保留为 **origin frozen conformance**，不撤销、不改写；
2. `e1ed85e4ba5aba212ddf3cc4f880c0abecc2bfab` 与 `115751b4c24a1924062a81a21e0d655e8cb5fedc` 是已授权、已进入后续验收父链的 Conformance 修正；
3. WP4C.5 执行时的 **effective conformance** 固定为 `d29e4d41ad4e1fc74e6d3513faa6b95d97ba0dfb` 中 `tests/conformance/rule_distribution_v4/` 的完整 Git tree：`1134d730e4c5ab23aa7b3ec91138da6981c2f009`；
4. 不得回退四个修正文件，不得重做两次历史修正，也不得把本裁定解释为允许继续修改冻结 Conformance；
5. 除本节的基线身份勘误和第 8 节的续作交付命名外，原 WP4C.5 任务书全部范围、行为、禁止项、测试、MCP 资源面与停止条件继续有效。

本文件恢复完整 WP4C.5，而不是另开新产品功能。执行完成后请求的 Gate 仍是 `WP4C_5_COMPATIBILITY_ACCEPTED`。

## 1. 唯一授权组合

执行授权由以下固定文件组合构成：

1. 原 WP4C.5 任务书：
   `taskbooks/fcop-4.0/WP4C.5/01-Versioned-Read-Resources-Legacy-Compatibility-and-Downstream-Shadow-Taskbook-v1.0.zh.md`
2. 本 WP4C.5a 勘误与续作任务书。

冲突时仅以下两项以本文件为准：

- 原 frontmatter 的 `frozen_distribution_conformance` 改解释为 `origin_distribution_conformance`；
- 当前有效测试身份改用本文件的 `effective_distribution_conformance_ref + effective_distribution_conformance_tree`。

原任务书的功能设计、12+4 MCP 有界资源面、CodeFlowMu 零写入、Unix 边界、13 个目标节点及 WP4C.6 禁止项均不变。PR 评论、聊天摘要和阻断报告不扩大授权。

执行前必须从本文件固定 GitHub ref 回读并核对 commit、直接父提交、SHA-256、字节数、UTF-8、无 BOM、LF；任一不一致立即 `INPUT_INTEGRITY_BLOCKED`。

## 2. 有效测试树的精确身份

有效目录固定为：

```text
tests/conformance/rule_distribution_v4/
Git tree SHA-1: 1134d730e4c5ab23aa7b3ec91138da6981c2f009
Source ref: d29e4d41ad4e1fc74e6d3513faa6b95d97ba0dfb
```

目录共九个 tracked 文件：

| 文件 | Git blob | bytes |
|---|---|---:|
| `__init__.py` | `5668090502d28d2e9c388d9453137e4ed5fd0a31` | 81 |
| `conftest.py` | `24d10b24d91449c33171a125857e4f47b651edd1` | 16826 |
| `driver.py` | `f00e18c6420b8022e1e4d07ff3d43286ac966a3d` | 1227 |
| `test_dist_00_meta.py` | `3c74a7b43ea07469c9183e77b843a4ec6441792e` | 14382 |
| `test_dist_01_06_manifest.py` | `1442260e04943bd22a6fb26c23875d17727b43dc` | 10075 |
| `test_dist_07_12_profiles.py` | `2bff99c5aa73ccfdd33526d956941ebaf87abbf5` | 9595 |
| `test_dist_13_20_projection.py` | `c7b0f8ef75e94af164200551e5bbed9d299fa6b2` | 14006 |
| `test_dist_21_24_assembly_compat_mcp.py` | `ad7781c0a9fe417b3f750f2e3044891ca5f98fdb` | 6175 |
| `test_dist_25_30_failures_artifacts_context_gates.py` | `bbb5e10de63a5915e49a479ad560df5cb5d65de4` | 13044 |

其中四个相对 origin frozen conformance 有变化的文件，其完整原始字节 SHA-256 固定为：

| 文件 | effective SHA-256 | 合法来源 |
|---|---|---|
| `conftest.py` | `e9571f4d0051e04cbc0e63ef9a8e2cdc9d5facd427afafb6c4934c305d835a67` | `e1ed85e…` |
| `test_dist_00_meta.py` | `816d739dd4eed73c545ee75947c893eba44f5a9f944dbc37ef978b582746c9d6` | `e1ed85e…` |
| `test_dist_01_06_manifest.py` | `dafac52d52a9c8568dd9d360b58cbba6676446cf62b3a498701a19cbb0697d78` | `115751b…` |
| `test_dist_25_30_failures_artifacts_context_gates.py` | `be6a3fe99b19da82f1c14b964c96d02160812b169d5ad10b4d5cd5203a64839c` | `e1ed85e…` |

必须同时验证 Git tree、九个 blob、四个 SHA-256。不得只核对文件数量或当前 checkout 路径。

## 3. 两次修正的授权含义

### 3.1 `e1ed85e…`

该提交只把 WP4C.2 控制审计固定到其已接受的历史交付区间，避免后续合法任务书被历史 allowlist 错误拒绝。它修改：

- `conftest.py`
- `test_dist_00_meta.py`
- `test_dist_25_30_failures_artifacts_context_gates.py`

它没有改变 DIST-23/24/26/29 的业务期待，没有授权当前阶段继续改 Meta 或 DIST-30。

### 3.2 `115751b…`

该提交只为 `DIST-02[development-no-constitution]` 补齐四项固定开发引用，保留原 Test ID 和断言，并验证返回引用与请求完全一致。它没有把开发资料注入普通业务 Agent，也没有授权修改当前 WP4C.5 目标 fixture。

## 4. 续作起点与工作树

必须从本任务书固定提交新建独立 worktree：

```text
D:\FCoP-wp4c5a-compatibility-resume
review/fcop-4.0-wp4c.5a-compatibility-resume
```

新 worktree 将包含 PR #26 的三份阻断证据和本任务书，它们是历史事实，不是实现结果。原 `D:\FCoP`、WP4C.4 工作树、PR #26 工作树及 CodeFlowMu 工作树全部保留，不清理、不切换、不覆盖。

生产与测试实现基线仍是 `accepted_wp4c_4_head=d29e4d4…`。核对本任务书提交相对该基线的已有差异时，应只看到：WP4C.4 Gate、原 WP4C.5 任务书、PR #26 三份阻断证据和本任务书；不得出现未说明的生产、MCP 或测试改动。

## 5. 恢复执行步骤

1. 完整读取原任务书、本任务书、PR #26 两份报告和 Manifest；
2. 验证第 2 节完整测试树身份；
3. 重新运行 13 个目标节点，确认真实基线仍为 1 passed / 12 failed；若不同，先报告，不猜测；
4. 完成原任务书第 4 节 Implementability Proof，引用并保留 PR #26 已验证事实，不把 preflight 阻断报告冒充完整 Proof；
5. 严格按原任务书实现版本路由、只读资源、五层事实和授权 shadow；
6. 不修改 `tests/conformance/rule_distribution_v4/**`；
7. 完成全部定向、全量、安全、MCP snapshot、CodeFlowMu 只读 shadow 与远端交付验证；
8. 完成后停止并请求 `WP4C_5_COMPATIBILITY_ACCEPTED`。

本任务书不允许“只修输入字段后直接宣称完成”。全部 WP4C.5 行为、测试与证据仍须实际完成。

## 6. 强化停止条件

除原任务书第 15 节外，新增以下停止条件：

- 当前完整 Conformance tree 不等于 `1134d730…`；
- 四个修正文件任一字节不等于第 2 节摘要；
- 发现除 `e1ed85e…` 与 `115751b…` 外还有未登记的 Conformance 变化；
- 需要再次修改 frozen/effective Conformance 才能通过 WP4C.5；
- 执行者试图回退四文件到 `1f4df9c…`；
- 把本勘误解释为允许改变 Test ID、断言、fixture 或 owner；
- 将 PR #26 的阻断报告改写成“此前已完成实现”。

发生阻断时只提交新的事实报告，`REQUESTED_GATE: NONE`，不得进入 WP4C.6。

## 7. CodeFlowMu 边界重申

CodeFlowMu 当前真实 HEAD 已由阻断报告记录为 `b961b16dd0c8863ead6995d963fe0ca576a8abaa`；已知精确版本隔离证据提交完整身份为 `789cb3fa8a007f050248784f7daf689808a549a2`。续作必须核对实际 current ref，不能把旧证据冒充当前状态。

仍然只允许 Git 身份、明确 allowlist 文件及版本约束的只读检查。禁止：

- 修改或清理 CodeFlowMu dirty 现场；
- checkout、merge、安装、启动产品或运行会写入的脚本；
- 修改其 FCoP pin、Scheduler、EVAL、生命周期、Panel、Host 或五桶；
- 将 `v1.0-rc.1` 解释为 FCoP 4.0 正式规范、发布制品或普通业务规则。

## 8. 报告与 GitHub 交付

为保留 PR #26 的阻断历史，本轮不得覆盖其报告与 Manifest。成功续作必须生成：

1. `reports/FCOP-4.0-WP4C.5A-IMPLEMENTABILITY-PROOF.md`
2. `reports/FCOP-4.0-WP4C.5A-VERSIONED-RESOURCE-MAPPING.md`
3. `reports/FCOP-4.0-WP4C.5A-LEGACY-AND-LAYER-ISOLATION.md`
4. `reports/FCOP-4.0-WP4C.5A-CODEFLOWMU-SHADOW.md`
5. `reports/FCOP-4.0-WP4C.5A-RESULT.md`
6. `reviews/fcop-4.0/wp4c.5a/MANIFEST.md`

使用两个交付提交：

1. Content commit：实现、测试、snapshot、CHANGELOG、五份 WP4C.5A 报告；
2. Manifest-only commit：只新增 WP4C.5A Manifest。

创建新的 Draft PR，base 为本任务书固定分支。不得修改或复用 PR #26；PR #26 保持 BLOCKED 历史。远端回读、文件 SHA-256、fresh LF checkout、工作树、main 未变与真实 CI 状态全部按原任务书执行。

## 9. 完成回执补充字段

除原任务书第 16 节全部字段外，必须增加：

```yaml
WP4C_5A_STATUS: COMPLETE
AUTHORIZED_SCOPE: WP4C_5A_ONLY
RESUMED_SCOPE: FULL_WP4C_5
BLOCKED_DELIVERY_HEAD: df395c7e221f850352d907933ccaab0937706c8f
ORIGIN_CONFORMANCE_REF: 1f4df9cc650f63b9e842d806340eb31b768f708e
AUTHORIZED_CONFORMANCE_CORRECTIONS: 2/2
EFFECTIVE_CONFORMANCE_REF: d29e4d41ad4e1fc74e6d3513faa6b95d97ba0dfb
EFFECTIVE_CONFORMANCE_TREE: 1134d730e4c5ab23aa7b3ec91138da6981c2f009
EFFECTIVE_CONFORMANCE_FILES: 9/9
CONFORMANCE_FILES_MODIFIED_THIS_RUN: 0
PR26_BLOCKER_PRESERVED: true
WP4C_5_TARGET_NODES: 13/13
WP4C_5_COMPATIBILITY_ACCEPTED: false
WP4C_6_STARTED: false
REQUESTED_GATE: WP4C_5_COMPATIBILITY_ACCEPTED
```

完成后必须停止。不得自行签署 Gate、进入 WP4C.6、修改 main 或发布。
