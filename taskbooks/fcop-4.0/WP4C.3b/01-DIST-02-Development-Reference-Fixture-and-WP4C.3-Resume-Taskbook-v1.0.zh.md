---
document_id: FCOP-4.0-WP4C.3B-TASKBOOK
title: FCoP 4.0 WP4C.3b DIST-02 开发引用夹具补齐与 WP4C.3 恢复任务书
version: 1.0
status: AUTHORIZED_FOR_WP4C_3B_AND_RESUME_WP4C_3_ONLY
authority: ADMIN
execution_authorized: true
authorized_scope: WP4C_3B_DIST_02_FIXTURE_ALIGNMENT_AND_WP4C_3_RESUME
input_head: ec81dc5ed80ff2a4492fd0d1611aad234949bfb5
prior_taskbook_commit: 0559e0fdf5390aa830f98a38d83f96f1cd475ab1
prior_taskbook_sha256: 903c5f0f249598ab3b5aaf7e947af8ed36fbc23928eff9b5db11e305acb21ba6
audit_correction_commit: e1ed85e4ba5aba212ddf3cc4f880c0abecc2bfab
accepted_rule_contract_head: f6831de12991010f22672fb6e776ce85ef1507ff
frozen_fcop_contract_commit: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
blocked_evidence_pr: https://github.com/joinwell52-AI/FCoP/pull/22
requested_gate: WP4C_3_RULE_PACKAGE_ACCEPTED
wp4c_4_authorized: false
main_merge_authorized: false
release_authorized: false
---

# FCoP 4.0 WP4C.3b：DIST-02 开发引用夹具补齐与 WP4C.3 恢复任务书

## 0. ADMIN 裁决

ADMIN 接受 PR #22 的阻断事实：

- WP4C.3a 历史审计作用域修正已经完成；
- Meta 33/33 与 DIST-30 已通过；
- FCoP、v4 Core、MCP 回归通过；
- WP4C.3 尚未开始生产实现；
- DIST-02[development-no-constitution] 要求成功返回四项固定开发引用，但测试请求没有提供 development_references，临时工作区也没有对应文件；
- DIST-22 已提供同类完整、显式、本地、可摘要验证的输入范例。

正式裁决：

1. constitution_ref=None 只表示通用工程宪法允许缺席，不表示四项 FCoP 开发引用可以缺席；
2. 四项开发引用必须由调用方显式提供，生产实现不得猜测、联网获取、从 Git 当前分支推导或制造占位身份；
3. 允许仅修改 tests/conformance/rule_distribution_v4/test_dist_01_06_manifest.py，为 DIST-02[development-no-constitution] 补齐本地夹具；
4. 原 Test ID、参数、constitution_ref is None、四引用数量与字段完整性断言全部保留；
5. 不修改全局 Scenario、driver、DIST-22 或其他 Conformance 文件；
6. 局部夹具验证通过后，可在同一顺序提交链中恢复 WP4C.3；
7. 不授权 WP4C.4、Host 投影、MCP、CodeFlowMu、main 合并或发布。

这次是输入夹具对齐，不是规范变更，也不是允许生产实现提供隐式默认值。

## 1. 固定输入与前置验证

执行前必须核验：

- 输入 HEAD 精确为 ec81dc5ed80ff2a4492fd0d1611aad234949bfb5；
- 它是 PR #22 的 Manifest commit；
- 直接父链依次包含 Content 67bf7a08915024fa5d88b5e66eb6396b68d1c6c8、Audit correction e1ed85e4ba5aba212ddf3cc4f880c0abecc2bfab、WP4C.3a 任务书 0559e0fdf5390aa830f98a38d83f96f1cd475ab1；
- WP4C.3a 任务书摘要为 903c5f0f249598ab3b5aaf7e947af8ed36fbc23928eff9b5db11e305acb21ba6；
- 历史审计仍为 13/13 精确匹配；
- 工作树干净；
- 原 D:\FCoP 工作区不被修改或切换；
- 使用独立 worktree。

任一不满足，停止并报告 INPUT_DRIFT。

建议工作树与分支：

    D:\FCoP-wp4c3b-development-fixture-and-rule-package
    review/fcop-4.0-wp4c.3b-development-fixture-and-rule-package

必须从本任务书固定 commit 直接接出，不合并 PR #22，不从 main 重建，不 cherry-pick 其他实现。

## 2. 唯一获准的夹具修改

只允许修改：

    tests/conformance/rule_distribution_v4/test_dist_01_06_manifest.py

只允许影响：

    test_dist_02[development-no-constitution]

允许在该文件内增加一个仅安排本地输入的小函数，或在对应参数分支中直接安排输入。不得扩散到全局 fixture。

### 2.1 四项引用的精确类别

夹具必须创建并显式传入：

1. FCoP repository development entry；
2. FCoP development guidance/manual；
3. 固定 FCoP contract；
4. 当前 TASK、授权范围与 Gate。

每项必须有 path、revision、sha256。建议沿用 DIST-22 的局部命名 entry、manual、contracts、task-scope。

四份文件必须：

- 写在 pytest tmp_path/Scenario sandbox 内；
- 使用 case.put；
- UTF-8/LF；
- 明确标识为非规范测试输入；
- sha256 由实际原始字节计算；
- path 指向真实文件；
- revision 为固定测试身份，不使用 HEAD、branch、tag、latest、当前时间或随机值。

### 2.2 请求构造

仅当 variant 等于 development-no-constitution 时：

- assembly_id 为 repository-development；
- constitution_ref 为 None；
- development_references 为上述四项显式引用。

ordinary、excluded-rc、old-draft 的输入和期望不得改变。

### 2.3 必须保留与加强的断言

原有断言全部保留：

- 排除摘要不出现在结果；
- constitution_ref is None；
- references 长度为 4；
- 每项至少含 path、revision、sha256。

允许增加：

- 返回 references 与显式输入完全相等且顺序稳定；
- 四个 path 均在夹具工作区；
- 每个摘要与文件原始字节一致；
- 没有第五项隐式引用；
- 普通业务装配不含 repository-development 引用。

不得删除、改名或降低任何已有断言。

## 3. 明确禁止的修法

不得：

- 让缺少 development_references 的生产请求自动成功；
- 在 Project、loader、selector 或 driver 中硬编码默认引用；
- 从 Git、任务书、分支、环境变量或网络自动发现引用；
- 用不存在路径、全零摘要、虚假 revision 或占位内容凑数；
- 把 CodeFlowMu v1.0-rc.1 或旧讨论稿作为缺省引用；
- 修改 conftest.py、全局 Scenario、driver.py 或 DIST-22；
- 修改冻结规范、规则分发合同或 WP4C.1 矩阵；
- 修改其他 Test ID、参数或行为期望；
- 增加 skip/xfail；
- 提前实现 WP4C.4–6。

## 4. 夹具修正验证与独立提交

先运行：

1. DIST-02 四个参数节点；
2. DIST-22 四个参数节点；
3. Rule Distribution Meta 33/33；
4. DIST-30；
5. Rule Distribution collect-only；
6. Rule Distribution 完整红灯基线；
7. tests/conformance/v4；
8. tests/test_fcop；
9. 隔离 tests/test_fcop_mcp；
10. Ruff 与 mypy。

生产实现仍不存在时，最低要求：

    DIST_02_FIXTURE_INPUTS: 4/4_PINNED
    DIST_02_TEST_ID: UNCHANGED
    DIST_02_ASSERTIONS_REMOVED: 0
    DIST_22_REGRESSION: PASS
    META_STATIC: 33/33_PASS
    DIST_30_CONTROL: 1/1_PASS
    RULE_DISTRIBUTION_COLLECT_ONLY: 176_UNCHANGED
    CURRENT_TARGET_BASELINE: 56_EXPECTED_RED
    FUTURE_OWNER_BASELINE: 86_EXPECTED_RED
    UNEXPECTED_FAILURES: 0
    SKIP_XFAIL_ADDED: 0

夹具补齐后，DIST-02 在生产实现不存在时仍应是缺能力红灯；这里证明输入完整，不要求它提前变绿。

通过后建立独立提交：

    test(fcop4): provide pinned development references to DIST-02

该提交只能包含 test_dist_01_06_manifest.py，不得与生产实现合并。如有节点数量漂移或非预期结果，停止，不进入生产实现。

## 5. 恢复 WP4C.3

只有第 4 节全部通过并完成 Fixture commit 后，才能恢复原 WP4C.3 任务书及 WP4C.3a 的历史审计修订。

本任务书只覆盖：

1. 原 Conformance 禁改条款对 test_dist_01_06_manifest.py 豁免一次，仅限 DIST-02 输入补齐；Fixture commit 后不得再改；
2. 输入改为本任务书及 Fixture commit 的顺序提交链。

其余 WP4C.3 合同全部不变：

- 九个 canonical 模块；
- 两种语言、18 个 Markdown；
- 一个严格 Manifest；
- 73 条款唯一主责；
- sequential、parallel、repository-development；
- 纯 loader/selector；
- Project.rule_distribution 为唯一新增公共 API；
- 八类 Toolkit 错误；
- 56 个本阶段节点全部转绿；
- DIST-30 保持通过；
- 86 个后续节点保持可解释预期红灯。

### 5.1 Manifest 字段数量勘误

原 WP4C.3 任务书写每条十个字段，但冻结 RD-07 双语合同、WP4C.1 矩阵和符合性夹具一致列出 11 个字段，包含 conflicts_with。

执行采用高优先级冻结合同：

    ARTIFACT_FIELDS: 11
    CONFLICTS_WITH_REQUIRED: true

不得删除 conflicts_with，也不得修改冻结合同或原任务书掩盖勘误。最终报告记录该事实优先级裁决。

## 6. 最终允许修改范围

本轮夹具：

    tests/conformance/rule_distribution_v4/test_dist_01_06_manifest.py

原 WP4C.3：

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
    reports/FCOP-4.0-WP4C.3B-*.md
    reviews/fcop-4.0/wp4c.3/MANIFEST.md

禁止修改冻结规范、规则分发合同、WP4C.1 矩阵、其他 Rule Distribution Conformance 文件、tests/conformance/v4、mcp、AGENTS.md、CLAUDE.md、.cursor、.github/workflows、CodeFlowMu、main、版本号、PyPI 或 GitHub Release。

中文文件不得使用 PowerShell 重写、拼接或管道转换；保持 UTF-8/LF 原始字节。

## 7. 报告与 GitHub 交付

新增：

    reports/FCOP-4.0-WP4C.3B-DIST-02-FIXTURE-ALIGNMENT.md

更新 WP4C.3 既有报告为当前实况，并保留、引用 PR #21 和 PR #22 的阻断历史。

最终至少三个顺序提交：

1. Fixture commit：只含 test_dist_01_06_manifest.py；
2. Content commit：WP4C.3 实现、单元测试、规则文件和报告；
3. Manifest commit：只含 reviews/fcop-4.0/wp4c.3/MANIFEST.md。

推送分支：

    review/fcop-4.0-wp4c.3b-development-fixture-and-rule-package

新建 Draft PR，base 为本任务书分支。PR #21、#22 保留为阻断历史。

最终从 GitHub 固定 Manifest HEAD 回读全部文件，核对 Taskbook → Fixture → Content → Manifest 父链、每个提交文件集合、远端/Git Blob/新鲜 LF checkout 三路 SHA-256、main 未变及实际 diff 允许面。CI 未触发时记录 NOT_TRIGGERED_BRANCH_FILTER，不得宣称绿色。

## 8. 强制停止条件

出现任一情况立即停止，只交付事实报告，不请求 Gate：

- 四项引用无法在局部 sandbox 中显式构造；
- 需要生产实现提供默认、猜测或联网引用；
- 需要修改第二个新的 Conformance 文件；
- 需要改动全局 Scenario、driver、DIST-22 或历史审计修正；
- 需要删除/改名 Test ID、断言或增加 skip/xfail；
- 176 节点、56/86 分类或 Meta 33 漂移；
- 11 字段合同仍有无法唯一执行的冲突；
- 56 个目标无法在原边界完成；
- 86 个未来节点无法解释地提前通过；
- 3.x、v4 Core 或 MCP 新回归；
- 需要修改 Host、MCP、CodeFlowMu、main、版本或发布；
- 父链、远端回读、文件清单或 SHA-256 不一致。

## 9. 验收条件

- [ ] DIST-02 四项引用均为真实本地文件、固定 revision 和真实摘要；
- [ ] constitution_ref=None 语义不变；
- [ ] 原 Test ID、参数及断言全部保留；
- [ ] 其他 DIST-02 参数和 DIST-22 无回归；
- [ ] Fixture commit 仅一个文件；
- [ ] 11 字段 RD-07 合同正确实现；
- [ ] 19/19 canonical 制品完成；
- [ ] 九模块、双语、73 条款主责一致；
- [ ] WP4C.3 56/56 通过，DIST-30 通过；
- [ ] 86 个未来节点保持预期红灯；
- [ ] FCoP、v4 Core、MCP、Ruff、mypy、public surface 通过；
- [ ] 无隐式开发引用、Host、网络、数据库、后台组件或第二状态机；
- [ ] GitHub 顺序提交、远端回读和哈希通过；
- [ ] 未进入 WP4C.4、main 或发布。

## 10. 最终回执格式

    WP4C_3B_STATUS: COMPLETE | BLOCKED | FAILED
    WP4C_3_STATUS: COMPLETE | BLOCKED | FAILED
    AUTHORIZED_SCOPE: WP4C_3B_DIST_02_FIXTURE_ALIGNMENT_AND_WP4C_3_RESUME
    TASKBOOK_COMMIT: <sha>
    TASKBOOK_SHA256: <sha256>
    INPUT_HEAD: ec81dc5ed80ff2a4492fd0d1611aad234949bfb5
    PRIOR_TASKBOOK: 0559e0fdf5390aa830f98a38d83f96f1cd475ab1
    AUDIT_CORRECTION_COMMIT: e1ed85e4ba5aba212ddf3cc4f880c0abecc2bfab
    DIST_02_FIXTURE: PASS
    DEVELOPMENT_REFERENCES: 4/4_PINNED
    CONSTITUTION_REF: ABSENT_AS_AUTHORIZED
    DIST_02_TEST_ID: UNCHANGED
    ASSERTIONS_REMOVED: 0
    SKIP_XFAIL_ADDED: 0
    OTHER_CONFORMANCE_FILES_MODIFIED: 0
    FIXTURE_COMMIT: <sha>
    ARTIFACT_FIELDS: 11/11
    CANONICAL_MODULES: 9/9
    CANONICAL_ARTIFACTS: 18/18
    MANIFEST_FILES: 1/1
    CLAUSE_OWNERSHIP: 73/73
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
    RUFF: PASS
    MYPY: PASS
    PUBLIC_SURFACE_DRIFT: 0_AFTER_AUTHORIZED_ADDITION
    PRODUCTION_IMPLICIT_REFERENCE_FALLBACKS: 0
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

完成后必须停止。任何既有 Gate、CI 或文件存在都不能自动授权 WP4C.4、合并 main 或发布。
