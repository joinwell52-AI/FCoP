---
document_id: FCOP-4.0-WP4C.3C-TASKBOOK
title: FCoP 4.0 WP4C.3c 历史公共方法集合对齐与 WP4C.3 收口任务书
version: 1.0
status: AUTHORIZED_FOR_WP4C_3C_AND_RESUME_WP4C_3_ONLY
authority: ADMIN
execution_authorized: true
authorized_scope: WP4C_3C_LEGACY_PUBLIC_METHOD_SET_ALIGNMENT_AND_WP4C_3_RESUME
input_head: c19808f4bc07948729bb841ec569627cb672fde7
prior_taskbook_commit: 3a11498c0d4aff736628e781f34516950cb34be8
fixture_commit: 115751b4c24a1924062a81a21e0d655e8cb5fedc
accepted_rule_contract_head: f6831de12991010f22672fb6e776ce85ef1507ff
frozen_fcop_contract_commit: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
blocked_evidence_pr: https://github.com/joinwell52-AI/FCoP/pull/23
requested_gate: WP4C_3_RULE_PACKAGE_ACCEPTED
wp4c_4_authorized: false
main_merge_authorized: false
release_authorized: false
---

# FCoP 4.0 WP4C.3c：历史公共方法集合对齐与 WP4C.3 收口任务书

## 0. ADMIN 裁决

ADMIN 接受 PR #23 的事实：

- WP4C.3b 的 DIST-02 夹具补齐已经完成；
- 本地候选实现的 WP4C.3 目标为 56/56 通过；
- v4 Core 119/119、MCP 134/134、41 个新增单元节点通过；
- 全量 FCoP 唯一失败位于 tests/test_fcop/test_v4_creation.py；
- 旧测试从 _METHOD_POLICIES 中排除10个 v4 专用方法后，断言历史方法恰好38个；
- WP4C.3 已明确授权新增 Project.rule_distribution，当前排除集合未包含它，因此得到39；
- 31个候选实现文件仍只存在于独立本地工作树，尚未提交或推送。

正式裁决：

1. 允许只修改 tests/test_fcop/test_v4_creation.py 中的 test_closeout_boundary_reflection_binding_and_subclass；
2. 将 rule_distribution 明确归类为 v4 专用公共方法；
3. 必须继续断言历史方法集合恰好38个；
4. 必须证明原38个方法没有删除、替换、改签名或隐藏；
5. 不允许简单把断言由38改成39；
6. 定点测试和完整回归通过后，允许恢复并提交已经核验的31文件候选实现；
7. 不授权 WP4C.4、MCP、Host、CodeFlowMu、main 合并或发布。

这是历史兼容性测试对已授权公共入口的范围对齐，不是扩大公共 API 数量，也不是放宽兼容性要求。

## 1. 固定输入与现场保护

执行前必须核验：

- 当前 Git HEAD 精确为 c19808f4bc07948729bb841ec569627cb672fde7；
- 它是 PR #23 的 Manifest commit；
- 父链包含 Content 29ceaed54d63bbdff5057621b7dc0329535b1f98、Fixture 115751b4c24a1924062a81a21e0d655e8cb5fedc、任务书 3a11498c0d4aff736628e781f34516950cb34be8；
- 旧测试文件原始 SHA-256 为 1397e4aaf9b0158c3491c4821fc13eb6dd38a608f9c88af4c68e2f7c15417012；
- 候选实现工作树为 D:\FCoP-wp4c3b-development-fixture-and-rule-package；
- 31个候选文件的路径、字节数与 SHA-256 全部匹配 PR #23 的 FCOP-4.0-WP4C.3-RESULT.md 清单；
- 除这31个已登记文件外没有其他修改或未跟踪文件；
- 原 D:\FCoP 工作区不变。

若候选文件少于或多于31、任一摘要变化、出现未知现场，立即停止并报告 LOCAL_CANDIDATE_DRIFT。

## 2. 固定任务书进入现有候选工作树

本任务书 commit 是输入 HEAD 的直接单文件子提交。为避免丢失已经核验的31个本地候选文件，允许在现有候选工作树中执行以下受控操作：

1. fetch 本任务书远端 ref；
2. 确认 taskbook commit 相对 c19808f4 仅新增本任务书一个文件；
3. 使用 Git 的 fast-forward-only 操作把当前 review 分支推进到本任务书 commit；
4. 不 stash、不 reset、不 clean、不 checkout 覆盖候选文件；
5. fast-forward 前后分别核对31/31路径和原始 SHA-256完全一致；
6. Git 若拒绝快进或任何本地字节发生变化，立即停止。

这里对已知 dirty 现场的允许仅限 PR #23 登记的31个候选文件。它不是一般性的脏工作树豁免。

继续使用：

    WORKTREE: D:\FCoP-wp4c3b-development-fixture-and-rule-package
    BRANCH: review/fcop-4.0-wp4c.3c-public-method-closeout

可以在同一 worktree 将分支重命名为上述名称，但不得重写、删除或强推历史。

## 3. 唯一获准的历史测试修改

唯一允许新增修改的历史测试文件：

    tests/test_fcop/test_v4_creation.py

唯一允许修改的测试函数：

    test_closeout_boundary_reflection_binding_and_subclass

### 3.1 正确集合语义

将 v4 专用方法集合显式包含：

- create_workspace
- create_task
- derive_workspace
- inspect_state
- transition
- finish_task
- family_digest
- recover_operation
- inject_fault
- export_archive
- rule_distribution

从完整 _METHOD_POLICIES 集合排除这11个 v4 专用名称后，original_names 必须仍恰好为38。

必须新增或保留以下证明：

- len(original_names) == 38；
- rule_distribution 存在于 _METHOD_POLICIES；
- rule_distribution 不属于 original_names；
- v4 专用集合恰好为上述11项；
- 完整策略集合等于 original_names 与 v4 专用集合的不重叠并集；
- 除 rule_distribution 外，旧提交到候选实现之间没有第二个新增公共策略名。

可以通过固定旧提交读取旧名称集合，或通过已冻结的 public-surface snapshot 做独立比较；不得只依赖总数。

### 3.2 必须保留的旧断言

以下全部保留：

- validate_team 的 staticmethod 性质；
- Project 与实例调用结果；
- inspect.unwrap 后名称、文档和签名一致；
- 实例绑定关系；
- is_initialized；
- write_task/read_task 的真实行为；
- autospec 对未知参数的 TypeError；
- patch.object 的绑定调用断言。

不得删除断言、改 Test ID、增加 skip/xfail、放宽异常或 monkeypatch _METHOD_POLICIES。

### 3.3 禁止的修法

不得：

- 把38改成39；
- 从 _METHOD_POLICIES 删除任一旧方法；
- 隐藏 rule_distribution 以逃避反射；
-改变 __len__、迭代或 inspect 行为；
- 修改 Project 方法名称或签名；
- 把 rule_distribution 伪装成私有方法；
- 修改生产代码来迎合旧计数；
- 修改第二个既有测试文件；
- 修改 public-surface snapshot 以外的历史基线来掩盖漂移。

## 4. 定点修正提交

先只修改并提交上述一个测试文件。

提交信息：

    test(fcop4): exclude authorized rule_distribution from legacy method set

该提交必须只有一个文件。

提交前运行：

1. 该测试函数定向运行；
2. tests/test_fcop/test_v4_creation.py 全文件；
3. public-surface snapshot 定向测试；
4. 31个候选文件 SHA-256 再核对。

最低要求：

    LEGACY_METHODS: 38/38
    V4_ONLY_METHODS: 11/11
    AUTHORIZED_ADDITION: Project.rule_distribution
    OTHER_PUBLIC_METHOD_ADDITIONS: 0
    ORIGINAL_ASSERTIONS_REMOVED: 0
    TEST_ID_CHANGED: false
    TEST_FILES_MODIFIED: 1
    LOCAL_CANDIDATE_HASHES: 31/31_UNCHANGED

任一不满足，停止，不提交候选实现。

## 5. 恢复并收口 WP4C.3

定点提交通过后，恢复 WP4C.3 原任务书、WP4C.3a 审计修订与 WP4C.3b 夹具修订。

允许提交的候选实现必须严格等于 PR #23 报告中记录的31文件集合；如为完成本次测试修正而需要改变候选实现字节，必须逐项解释且仍限于原 WP4C.3 允许面。

WP4C.3 最终目标不变：

- canonical 模块9/9；
-双语 Markdown 18/18；
- Manifest 1/1；
- RD-07 artifact 字段11/11，包含 conflicts_with；
- F4条款主责73/73；
- sequential、parallel、repository-development 三装配；
- Project.rule_distribution 为唯一新增公共 API；
- 56/56 本阶段节点通过；
- DIST-30 通过；
- 86个未来节点保持可解释的后续状态；
- 3.x 公共行为无回归。

不得借本次测试修正增加第二个公共 API 或提前实现 WP4C.4–6。

## 6. 允许修改范围

本轮新增授权：

    tests/test_fcop/test_v4_creation.py
    reports/FCOP-4.0-WP4C.3C-PUBLIC-METHOD-SET-ALIGNMENT.md

原 WP4C.3 已登记候选范围：

    CHANGELOG.md
    pyproject.toml
    src/fcop/project.py
    src/fcop/rules/_data/v4/**
    src/fcop/v4/boundary.py
    src/fcop/v4/creation.py
    src/fcop/v4/rule_distribution/**
    tests/test_fcop/test_v4_rule_distribution*.py
    tests/test_fcop/snapshots/public_surface.json
    reports/FCOP-4.0-WP4C.3-*.md
    reports/FCOP-4.0-WP4C.3A-*.md
    reports/FCOP-4.0-WP4C.3B-*.md
    reports/FCOP-4.0-WP4C.3C-*.md
    reviews/fcop-4.0/wp4c.3/MANIFEST.md

先前已验收且必须保持不变：

    tests/conformance/rule_distribution_v4/conftest.py
    tests/conformance/rule_distribution_v4/test_dist_00_meta.py
    tests/conformance/rule_distribution_v4/test_dist_01_06_manifest.py
    tests/conformance/rule_distribution_v4/test_dist_25_30_failures_artifacts_context_gates.py

禁止修改其他 tests/conformance、冻结规范、规则分发合同、WP4C.1矩阵、mcp、Host入口、AGENTS.md、CLAUDE.md、.cursor、.github/workflows、CodeFlowMu、版本号、main、PyPI或GitHub Release。

中文文件不得使用 PowerShell 重写、拼接或管道转换；必须保持 UTF-8/LF 原始字节。

## 7. 完整验证

至少执行：

- 定点历史测试；
- tests/test_fcop 全量；
- tests/conformance/v4 119/119；
- 隔离 tests/test_fcop_mcp；
- Rule Distribution Meta 33/33；
- Rule Distribution collect-only 176；
- WP4C.3 目标56/56；
- Rule Distribution完整行为；
- 41个新增单元节点；
- Ruff；
- mypy；
- public-surface snapshot；
- 19个规则制品源码/包内路径与摘要；
- wheel/sdist 包含性检查。

验收要求：

    TEST_FCOP: ALL_PASS
    V4_CORE_CONFORMANCE: 119/119
    MCP_REGRESSION: 134/134_OR_ACTUAL_ALL_PASS
    RULE_DISTRIBUTION_META: 33/33
    RULE_DISTRIBUTION_COLLECT_ONLY: 176
    WP4C_3_TARGET_NODES: 56/56
    NEW_UNIT_NODES: 41/41_OR_ACTUAL_ALL_PASS
    LEGACY_METHODS: 38/38
    V4_ONLY_METHODS: 11/11
    PUBLIC_API_ADDITIONS: 1
    PUBLIC_API_ADDITION: Project.rule_distribution
    UNEXPECTED_FAILURES: 0
    RUFF: PASS
    MYPY: PASS

未来节点中的负向零写入重叠通过，不等于提前完成后续正向能力；最终报告必须继续逐项区分。

## 8. 提交与 GitHub 交付

至少形成：

1. Test-alignment commit：仅 test_v4_creation.py；
2. Content commit：31文件候选实现、单元测试、规则制品和报告；
3. Manifest commit：仅 reviews/fcop-4.0/wp4c.3/MANIFEST.md。

如果31文件候选在导入 taskbook 前后发生任何字节变化，必须在报告中给出前后摘要和原因。禁止丢弃后重写成无历史来源的新实现。

推送分支：

    review/fcop-4.0-wp4c.3c-public-method-closeout

建立新的 Draft PR，base 为本任务书分支。PR #21、#22、#23 保留为历史阻断证据，不复用、不重写。

推送后：

1. fetch 远端 review ref；
2. 验证 Taskbook → Test alignment → Content → Manifest 直接父链；
3. 验证每个提交的精确文件集合；
4. 从最终 Manifest HEAD 回读全部文件；
5. 比较 GitHub、Git Blob、新鲜 LF checkout 三路 SHA-256；
6. 核对 main 未变；
7. 核对实际 diff 均在允许范围；
8. CI 未触发则记录 NOT_TRIGGERED_BRANCH_FILTER，不得宣称全绿；
9. 不请求 reviewer、不启用 auto-merge、不合并。

## 9. 强制停止条件

出现任一情况立即停止，只交付事实报告，不请求 Gate：

- 旧38个方法集合无法保持；
- 除 rule_distribution 外发现其他公共入口变化；
- 需要修改第二个历史测试文件；
- 需要修改生产代码来绕过反射或计数；
- 31文件候选现场与 PR #23 清单不一致；
- fast-forward 改变候选文件字节；
- 56个目标、119 Core 或 MCP 出现新失败；
- 需要修改冻结规范、合同、Conformance、Host、MCP或CodeFlowMu；
- 需要进入 WP4C.4、main、版本或发布；
- 远端父链、文件集合、回读或摘要不一致。

## 10. 最终报告

新增：

    reports/FCOP-4.0-WP4C.3C-PUBLIC-METHOD-SET-ALIGNMENT.md

必须记录：

- 修正前39与38冲突；
- 11项 v4 专用集合；
- 38项历史集合保持证明；
- rule_distribution 为唯一新增公共方法；
- 旧测试全部保留的断言；
- 31文件候选导入前后摘要；
- 完整测试结果；
- PR #21至#23的阻断历史引用。

最终回执：

    WP4C_3C_STATUS: COMPLETE | BLOCKED | FAILED
    WP4C_3_STATUS: COMPLETE | BLOCKED | FAILED
    AUTHORIZED_SCOPE: WP4C_3C_LEGACY_PUBLIC_METHOD_SET_ALIGNMENT_AND_WP4C_3_RESUME
    TASKBOOK_COMMIT: <sha>
    TASKBOOK_SHA256: <sha256>
    INPUT_HEAD: c19808f4bc07948729bb841ec569627cb672fde7
    TEST_ALIGNMENT_COMMIT: <sha>
    HISTORICAL_TEST_FILES_MODIFIED: 1
    LEGACY_METHODS: 38/38
    V4_ONLY_METHODS: 11/11
    PUBLIC_API_ADDITIONS: 1
    PUBLIC_API_ADDITION: Project.rule_distribution
    ORIGINAL_ASSERTIONS_REMOVED: 0
    LOCAL_CANDIDATE_FILES: 31/31
    CANONICAL_MODULES: 9/9
    CANONICAL_ARTIFACTS: 18/18
    MANIFEST_FILES: 1/1
    ARTIFACT_FIELDS: 11/11
    CLAUSE_OWNERSHIP: 73/73
    WP4C_3_TARGET_NODES: 56/56
    DIST_30_CONTROL: 1/1
    TEST_FCOP: <actual>
    V4_CORE_CONFORMANCE: 119/119
    MCP_REGRESSION: <actual>
    RULE_DISTRIBUTION_META: 33/33
    RULE_DISTRIBUTION_COLLECT_ONLY: 176
    UNEXPECTED_FAILURES: 0
    RUFF: PASS
    MYPY: PASS
    CONTENT_COMMIT: <sha>
    MANIFEST_COMMIT: <sha>
    REMOTE_HEAD: <sha>
    REMOTE_PUSHED: true
    REMOTE_REFETCH_VERIFIED: PASS
    DELIVERY_SHA256: <matched>/<total>
    DRAFT_PR_URL: <url>
    WORKTREE_STATUS: CLEAN
    MCP_FILES_MODIFIED: 0
    CODEFLOWMU_FILES_MODIFIED: 0
    MAIN_MODIFIED: false
    RELEASE_CREATED: false
    WP4C_3_RULE_PACKAGE_ACCEPTED: false
    WP4C_4_STARTED: false
    REQUESTED_GATE: WP4C_3_RULE_PACKAGE_ACCEPTED

完成后必须停止。任何测试通过、既有 Gate 或本地候选文件都不能自动授权 WP4C.4、main 合并或发布。
