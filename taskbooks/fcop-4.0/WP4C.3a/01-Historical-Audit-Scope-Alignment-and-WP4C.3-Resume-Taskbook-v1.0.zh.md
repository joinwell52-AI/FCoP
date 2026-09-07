---
document_id: FCOP-4.0-WP4C.3A-TASKBOOK
title: FCoP 4.0 WP4C.3a 历史审计作用域修正与 WP4C.3 恢复任务书
version: 1.0
status: AUTHORIZED_FOR_WP4C_3A_AND_RESUME_WP4C_3_ONLY
authority: ADMIN
execution_authorized: true
authorized_scope: WP4C_3A_AUDIT_SCOPE_ALIGNMENT_AND_WP4C_3_RESUME
input_head: 78ea6b89a1ef0df0e504a3cfa34cecddeb7dda24
blocked_wp4c_3_taskbook_commit: de213ec0f74f8976283a24986d4eb7de77c67142
blocked_wp4c_3_taskbook_sha256: a4b782db3a984be9872d6c99428c5fc669a1cd3135468b33ef8eba7a6c1b57d2
wp4c_2_input_head: 921be62c32ccccece53be74e7e565b1b37731fbe
wp4c_2_accepted_head: 1f4df9cc650f63b9e842d806340eb31b768f708e
accepted_rule_contract_head: f6831de12991010f22672fb6e776ce85ef1507ff
frozen_fcop_contract_commit: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
parent_gate: WP4C_2_DISTRIBUTION_CONFORMANCE_ACCEPTED
parent_gate_comment: https://github.com/joinwell52-AI/FCoP/pull/20#issuecomment-5566832805
blocked_evidence_pr: https://github.com/joinwell52-AI/FCoP/pull/21
requested_gate: WP4C_3_RULE_PACKAGE_ACCEPTED
wp4c_4_authorized: false
main_merge_authorized: false
release_authorized: false
---

# FCoP 4.0 WP4C.3a：历史审计作用域修正与 WP4C.3 恢复任务书

## 0. ADMIN 裁决

ADMIN 确认 PR #21 的停止是正确的。阻断不是规则包实现失败，而是 WP4C.2 的两项审计断言把“WP4C.2 历史交付范围”错误地计算为“从 WP4C.2 输入提交到当前工作树的全部永久变化”，因此任何经过明确授权的后续任务书都会被旧 13 文件白名单拒绝。

正式裁决：

1. WP4C.2 的 13 文件白名单继续有效，不增加 WP4C.3、WP4C.4 或任何未来路径；
2. 该白名单只审计固定历史区间：
   `921be62c32ccccece53be74e7e565b1b37731fbe..1f4df9cc650f63b9e842d806340eb31b768f708e`；
3. 当前及未来阶段的修改范围，由该阶段固定任务书、执行分支、允许路径、Content commit 和 Manifest commit 独立审计；
4. 不得再用 WP4C.2 的历史白名单判断后续阶段是否可以存在；
5. DIST-30 仍证明 WP4C.2 当时没有自行越过 Gate，不得被改写成全仓库永久冻结器；
6. 本轮允许最小修正三处冻结 Conformance 文件；修正通过后，可在同一顺序提交链中恢复原 WP4C.3，不再增加一次中间 ADMIN Gate；
7. 原 WP4C.3 的 56 个目标节点、生产边界、禁止项及最终 Gate 全部不变。

这是一项审计边界修正，不是协议变更、测试放水或扩大产品范围。

---

## 1. 权威输入与提交链

执行前必须验证：

- 当前 HEAD 精确为 `78ea6b89a1ef0df0e504a3cfa34cecddeb7dda24`；
- 该 HEAD 是 PR #21 的事实报告 Manifest；
- 其直接父链包含：
  - Content：`0e89f94aa8df017817f76dadc8572c8bc5c0afdf`
  - 原 WP4C.3 固定任务书：`de213ec0f74f8976283a24986d4eb7de77c67142`
  - 已验收 WP4C.2：`1f4df9cc650f63b9e842d806340eb31b768f708e`
- 原 WP4C.3 任务书原始字节 SHA-256 仍为
  `a4b782db3a984be9872d6c99428c5fc669a1cd3135468b33ef8eba7a6c1b57d2`；
- 工作树干净；
- 不在原 `D:\FCoP` 脏工作区切换或开发；
- 使用独立 worktree。

任一不匹配，停止并报告 `INPUT_DRIFT`。

建议工作树与分支：

```text
D:\FCoP-wp4c3a-audit-scope-and-rule-package
review/fcop-4.0-wp4c.3a-audit-scope-and-rule-package
```

必须从本任务书固定 commit 直接接出，不合并 PR #20/#21，不从 main 重建，不 cherry-pick 未列入权威链的实现。

---

## 2. 第一阶段：仅修正历史审计作用域

### 2.1 唯一允许修改的 Conformance 文件

只允许修改：

```text
tests/conformance/rule_distribution_v4/conftest.py
tests/conformance/rule_distribution_v4/test_dist_00_meta.py
tests/conformance/rule_distribution_v4/test_dist_25_30_failures_artifacts_context_gates.py
```

不得修改其他 `tests/conformance/rule_distribution_v4/**` 文件，不得修改 Test ID，不得删除行为断言，不得增加 skip/xfail，不得更改 142 个行为节点的期望结果。

### 2.2 必须建立的固定历史边界

在 `conftest.py` 中保留现有 `INPUT_HEAD` 的测试输入含义，并增加明确的 WP4C.2 已验收交付 HEAD，例如：

```python
WP4C_2_INPUT_HEAD = "921be62c32ccccece53be74e7e565b1b37731fbe"
WP4C_2_ACCEPTED_HEAD = "1f4df9cc650f63b9e842d806340eb31b768f708e"
```

可以让 `INPUT_HEAD` 等于 `WP4C_2_INPUT_HEAD` 以保持现有 fixture 行为，但不得把 `INPUT_HEAD` 改成当前 HEAD、分支名或可变引用。

建立一个职责单一的历史交付路径计算函数。它必须：

- 精确计算 `WP4C_2_INPUT_HEAD..WP4C_2_ACCEPTED_HEAD`；
- 只使用 Git 已提交对象；
- 不读取当前 HEAD 的后续提交；
- 不拼入当前工作树未跟踪文件；
- 返回规范化仓库相对路径集合；
- 不接受调用方传入任意 end ref 来绕过固定证据。

### 2.3 Meta 断言的修正

保留 `test_meta_allowlist_and_no_stage_advance` 的 Test ID。

将其审计对象从：

```text
INPUT_HEAD → 当前 HEAD + 当前未跟踪文件
```

修正为：

```text
WP4C_2_INPUT_HEAD → WP4C_2_ACCEPTED_HEAD
```

并要求：

- 固定区间变化路径与 13 项 `ALLOWLIST` 精确相等，不只做宽松子集；
- 固定区间无 merge commit；
- `WP4C_2_ACCEPTED_HEAD` 是当前执行 HEAD 的祖先；
- 当前存在后续已授权任务书或报告，不改变上述历史结果；
- 原规范字节、测试源字节、anti-stub、断言计数与 33/33 Meta 其余检查全部保留。

不得将 WP4C.3 任务书、报告或未来目录加入 `ALLOWLIST`。

### 2.4 DIST-30 的修正

保留 DIST-30 的 Test ID、RD 归属、零写入断言及以下历史事实：

- 在 WP4C.2 的固定输入提交中，没有签署 `WP4C_2_DISTRIBUTION_CONFORMANCE_ACCEPTED`；
- 没有 `WP4C_3_ONLY` 执行授权；
- WP4C.2 任务书不能自动授权 WP4C.3；
- 合同冻结、测试授权、实现授权、合并授权、发布授权相互独立。

仅将末尾的变化范围与 merge 审计改为同一固定历史区间。DIST-30 不得扫描当前 HEAD 后续的合法 ADMIN 授权并把它误报成 WP4C.2 自动越权。

不得：

- 删除 Gate 检查；
- 把 DIST-30 改为无条件 PASS；
- mock Git 输出；
- 通过环境变量关闭审计；
- 允许未签署 Gate 自动推进；
- 信任测试调用者自报阶段状态。

### 2.5 必须新增的回归证明

在上述三个允许文件内，增加或加强最小测试，证明：

1. 固定历史区间恰好得到原 13 个路径；
2. WP4C.3 固定任务书存在于后续祖先链时，历史区间结果仍为原 13 个路径；
3. 若固定 WP4C.2 区间本身出现第 14 个路径，审计仍会失败；
4. 当前工作树的无关未跟踪文件不能改变历史事实，但必须仍由本任务书的执行前工作树检查和最终 Manifest 清单拒绝；
5. 三个固定 SHA 不可替换为 branch、tag、HEAD 或其他可变引用。

这里的第 4 项不是允许脏工作树执行。执行器仍必须在干净工作树开始、只修改授权文件，并在交付前恢复干净。

---

## 3. 第一阶段验证与独立提交

修正后先运行：

- `test_dist_00_meta.py` 全量；
- DIST-30 定向；
- Rule Distribution 全量 collect-only；
- Rule Distribution 全量行为基线；
- `tests/conformance/v4`；
- `tests/test_fcop`；
- 隔离 `tests/test_fcop_mcp`；
- Ruff；
- mypy。

最低要求：

```yaml
RULE_DISTRIBUTION_META: 33/33_OR_MORE_ALL_PASS
DIST_30_CONTROL: 1/1_PASS
RULE_DISTRIBUTION_COLLECT_ONLY: 176_UNCHANGED
WP4C_3_TARGET_BASELINE: 56_EXPECTED_RED
FUTURE_OWNER_BASELINE: 86_EXPECTED_RED
UNEXPECTED_FAILURES: 0
FROZEN_TEST_IDS: UNCHANGED
SKIP_XFAIL_ADDED: 0
```

如节点总数、Test ID、未来节点分类或既有回归发生漂移，立即停止，不进入生产实现。

通过后先建立一个独立提交：

```text
test(fcop4): pin WP4C.2 audit to its accepted historical range
```

该提交只包含上述三个 Conformance 文件。后续 WP4C.3 实现不得与这一提交压成一个提交。

---

## 4. 第二阶段：恢复原 WP4C.3

只有第一阶段全部通过且独立提交完成后，才恢复原任务书：

```text
taskbooks/fcop-4.0/WP4C.3/
01-Canonical-Rule-Package-Manifest-Loader-and-Assemblies-Taskbook-v1.0.zh.md
```

恢复时，原任务书的第 3–16 节继续有效，本任务书只作以下限定覆盖：

1. 输入 HEAD 改为本任务书提交链及第一阶段审计修正提交；
2. 原第 8、10、13 节对 `tests/conformance/rule_distribution_v4/**` 的绝对禁止，针对本轮已授权的三个审计文件仅豁免第一阶段一次；
3. 第一阶段提交之后，不得再次修改这三个文件；
4. PR #21 的 BLOCKED 报告必须保留在 Git 历史中；最终报告可更新同名 WP4C.3 报告为完成实况，但不得抹除或改写既有提交；
5. 原 56 个 WP4C.3 目标节点、86 个未来节点、19 个 canonical 文件、九模块、73 条款、一个公共 API、八类 Toolkit 错误及全部禁止项不变；
6. 不得借审计修正提前实现 WP4C.4–6。

WP4C.3 的唯一生产目标仍是：

- 18 个双语 canonical Markdown；
- 1 个严格 Manifest；
- 纯 loader/selector；
- sequential、parallel、repository-development 三种装配；
- `Project.rule_distribution` 唯一新增公共入口；
- 56/56 本阶段节点转绿；
- DIST-30 保持通过；
- 86 个未来节点保持有解释的预期红灯。

---

## 5. 最终允许修改范围

最终交付允许包含：

### 审计修正

```text
tests/conformance/rule_distribution_v4/conftest.py
tests/conformance/rule_distribution_v4/test_dist_00_meta.py
tests/conformance/rule_distribution_v4/test_dist_25_30_failures_artifacts_context_gates.py
```

### 原 WP4C.3 允许面

```text
src/fcop/rules/_data/v4/**
src/fcop/v4/rule_distribution/**
src/fcop/v4/creation.py
src/fcop/v4/boundary.py
src/fcop/project.py
pyproject.toml
tests/test_fcop/test_v4_rule_distribution*.py
tests/test_fcop/snapshots/public_surface.json
CHANGELOG.md
reports/FCOP-4.0-WP4C.3-*.md
reports/FCOP-4.0-WP4C.3A-*.md
reviews/fcop-4.0/wp4c.3/MANIFEST.md
```

若 `src/fcop/v4/**` 需要另一既有文件的一行级接线，仍须先在计划中证明最小性。

除以上精确路径外全部禁止，尤其禁止：

- `spec/fcop-4.0-spec*.md`；
- `docs/fcop-4.0/rule-distribution-contract*.md`；
- WP4C.1 冻结矩阵；
- 其他 Rule Distribution Conformance 文件；
- `tests/conformance/v4/**`；
- `mcp/**`；
- AGENTS.md、CLAUDE.md、`.cursor/**`；
- `.github/workflows/**`；
- CodeFlowMu；
- main、版本号、PyPI、GitHub Release。

中文文件不得使用 PowerShell 重写、拼接或管道转换；必须保持 UTF-8/LF 原始字节合同。

---

## 6. 新增报告要求

除原 WP4C.3 四份报告外，增加：

```text
reports/FCOP-4.0-WP4C.3A-AUDIT-SCOPE-CORRECTION.md
```

该报告必须逐项给出：

- 两个旧失败节点修正前后的真实输出；
- 原 13 路径清单及固定区间；
- 三处文件的逐项改动理由；
- 未删除的断言和新增的防回归证明；
- 为什么后续任务书不属于 WP4C.2 历史交付；
- 当前阶段如何由任务书和 Manifest 独立限制；
- 第一阶段提交 SHA；
- 第一阶段完整测试结果。

最终 `reviews/fcop-4.0/wp4c.3/MANIFEST.md` 必须列出本轮所有实际交付文件及原始 SHA-256，不得使用通配符。

---

## 7. 提交与 GitHub 交付

必须至少使用三个顺序提交：

1. Audit correction commit：只含三个获准 Conformance 文件；
2. Content commit：原 WP4C.3 生产实现、单元测试及全部报告；
3. Manifest commit：只含 `reviews/fcop-4.0/wp4c.3/MANIFEST.md`。

如需仅修报告中的客观错误，可增加受控 report-only 提交，但不得重写上述提交或 force-push 隐藏失败历史。

推送分支：

```text
review/fcop-4.0-wp4c.3a-audit-scope-and-rule-package
```

建立新的 Draft PR，base 为本任务书分支。不得复用 PR #21 冒充完整交付；PR #21 保留为阻断证据。

推送后必须：

1. fetch 远端 review ref；
2. 验证 Manifest → Content → Audit correction → taskbook 的父链；
3. 从 GitHub 固定最终 HEAD 回读所有交付文件；
4. 核对远端、Git blob、本地字节 SHA-256；
5. 核对实际 diff 全部落在本任务书允许面；
6. 核对 main 未变；
7. CI 未触发时如实写 `NOT_TRIGGERED_BRANCH_FILTER`，不得宣称绿色；
8. 不请求 reviewer、不启用 auto-merge、不合并。

---

## 8. 强制停止条件

出现任一情况立即停止，只交付事实报告，不请求 Gate：

- 不能用固定 `WP4C_2_INPUT_HEAD..WP4C_2_ACCEPTED_HEAD` 保留原审计语义；
- 需要把后续路径加入旧 13 文件白名单；
- 需要删除 Gate、零写入、anti-stub、Test ID 或行为断言；
- 第一阶段后 Meta/DIST-30 仍失败；
- 176 节点、56/86 分类或 33 Meta 发生不可解释漂移；
- 需要修改第四个 Rule Distribution Conformance 文件；
- 需要修改冻结规范、合同或矩阵；
- 需要放宽生产路径、Host、MCP、CodeFlowMu、main 或发布边界；
- WP4C.3 56 个目标不能在原范围内完成；
- 3.x/v4/MCP 出现新回归；
- 86 个未来节点出现无法解释的提前通过；
- 最终 diff、提交父链、远端回读或 SHA-256 不一致。

---

## 9. 验收条件

- [ ] 历史审计固定为 WP4C.2 的两个 immutable SHA；
- [ ] 旧 13 路径白名单未增加；
- [ ] Meta 与 DIST-30 不再读取当前 HEAD 后续路径作为 WP4C.2 事实；
- [ ] 三处修正有独立提交和回归证明；
- [ ] 其他冻结 Conformance 文件 0 修改；
- [ ] WP4C.3 19 个 canonical 文件完成；
- [ ] 九模块、双语和 73 条款主责一致；
- [ ] WP4C.3 56/56 通过；
- [ ] DIST-30 通过；
- [ ] 86 个未来节点保持预期红灯；
- [ ] FCoP/v4/MCP、Ruff、mypy 和 public surface 通过；
- [ ] 无新增依赖、数据库、daemon、timer、watcher、scheduler、网络服务或第二状态机；
- [ ] 无 Host 投影、MCP、CodeFlowMu、main 或发布变更；
- [ ] GitHub 三提交以上顺序、远端回读与全部哈希通过。

---

## 10. 最终回执格式

```yaml
WP4C_3A_STATUS: COMPLETE | BLOCKED | FAILED
WP4C_3_STATUS: COMPLETE | BLOCKED | FAILED
AUTHORIZED_SCOPE: WP4C_3A_AUDIT_SCOPE_ALIGNMENT_AND_WP4C_3_RESUME

TASKBOOK_COMMIT: <sha>
TASKBOOK_SHA256: <sha256>
INPUT_HEAD: 78ea6b89a1ef0df0e504a3cfa34cecddeb7dda24
WP4C_2_INPUT_HEAD: 921be62c32ccccece53be74e7e565b1b37731fbe
WP4C_2_ACCEPTED_HEAD: 1f4df9cc650f63b9e842d806340eb31b768f708e
ORIGINAL_WP4C_3_TASKBOOK: de213ec0f74f8976283a24986d4eb7de77c67142
FROZEN_FCOP_CONTRACT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6

HISTORICAL_ALLOWLIST: 13/13_EXACT
AUDIT_SCOPE_CORRECTION: PASS
META_STATIC: <actual>/ALL_PASS
DIST_30_CONTROL: 1/1_PASS
FROZEN_TEST_IDS: UNCHANGED
ASSERTIONS_REMOVED: 0
SKIP_XFAIL_ADDED: 0
AUDIT_CORRECTION_COMMIT: <sha>

CANONICAL_MODULES: 9/9
CANONICAL_ARTIFACTS: 18/18
MANIFEST_FILES: 1/1
CLAUSE_OWNERSHIP: 73/73
WP4C_3_TARGET_IDS: 10/10
WP4C_3_TARGET_NODES: 56/56
FUTURE_OWNER_NODES: 86_EXPECTED_DEFERRED
UNEXPECTED_FAILURES: 0
UNEXPECTED_PASSES: 0

TEST_FCOP: <actual>
V4_CORE_CONFORMANCE: 119/119
MCP_REGRESSION: <actual>
RULE_DISTRIBUTION_COLLECT_ONLY: 176
RUFF: PASS
MYPY: PASS
PUBLIC_SURFACE_DRIFT: 0_AFTER_AUTHORIZED_ADDITION

FROZEN_SPEC_FILES_MODIFIED: 0
OTHER_RULE_DISTRIBUTION_CONFORMANCE_FILES_MODIFIED: 0
MCP_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0
MAIN_MODIFIED: false
RELEASE_CREATED: false

CONTENT_COMMIT: <sha>
MANIFEST_COMMIT: <sha>
REMOTE_HEAD: <sha>
REMOTE_PUSHED: true
REMOTE_REFETCH_VERIFIED: PASS
DELIVERY_SHA256: <matched>/<total>
DRAFT_PR_URL: <url>
WORKTREE_STATUS: CLEAN

WP4C_3_RULE_PACKAGE_ACCEPTED: false
WP4C_4_STARTED: false
REQUESTED_GATE: WP4C_3_RULE_PACKAGE_ACCEPTED
```

完成后必须停止。此前任何 Gate、CI 或文件存在都不能自动授权 WP4C.4、合并 main 或发布。
