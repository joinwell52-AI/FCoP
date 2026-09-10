---
taskbook_id: FCOP-4.0-WP3E-REMAINING-CORE-CLOSEOUT
document_role: EXECUTION_TASKBOOK
status: AUTHORIZED_FOR_WP3E_ONLY
execution_authorized: true
authorized_scope: WP3E_ONLY
gate_self_signing: forbidden
requested_gate: FCOP_4_CORE_IMPLEMENTATION_ACCEPTED
main_merge_authorized: false
release_authorized: false
---

# FCoP 4.0 WP3E：剩余 Core 恢复语义与符合性收口任务书 v1.0

## 0. ADMIN 授权

ADMIN 已在固定 GitHub review HEAD 上验收 WP3D/WP3D.1，并以独立 Gate receipt 签署：

```yaml
GATE: WP3D_CONVERGENCE_ACCEPTED
DECISION: ACCEPTED
GATE_COMMIT: 99d0ab14a8e4e3b5d8580230a9df1d6dbec50b41
ACCEPTED_REVIEW_HEAD: 7e0b42187bdee6a9fda3b0df2a2bc1e97cb8859f
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
```

本任务书是当前唯一执行授权，只允许 WP3E。目标是让冻结的 60/60 Test ID 对应的全部 119 个 v4 节点真实通过，并关闭现存 23 个 deferred Core 行为。

本任务不授权 WP4、规则包、Host adapter、MCP/PyPI、Schema、CodeFlowMu、main 合并或发布。

## 1. 固定输入与执行环境

执行前必须 fetch 并核验：

```yaml
REPOSITORY: joinwell52-AI/FCoP
INPUT_HEAD: 99d0ab14a8e4e3b5d8580230a9df1d6dbec50b41
GATE_RECEIPT: reviews/fcop-4.0/gates/WP3D-CONVERGENCE-ACCEPTED.md
ACCEPTED_REVIEW_HEAD: 7e0b42187bdee6a9fda3b0df2a2bc1e97cb8859f
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
EXPECTED_V4_COLLECTED: 119
EXPECTED_V4_STATIC_META: 27
EXPECTED_V4_BEHAVIORAL_GREEN: 69
EXPECTED_V4_DEFERRED: 23
EXPECTED_FROZEN_TEST_IDS: 60/60
EXPECTED_TEST_FCOP: 1118 passed
EXPECTED_V3_REGRESSION: 907/907
EXPECTED_MCP_REGRESSION: 80/80
```

输入、Gate、祖先链或冻结规范 blob 不一致时立即停止。不得从其他 review 分支 cherry-pick 或手工拼接。

必须使用独立 worktree，建议：

```text
D:\FCoP-wp3e-core-closeout
review/fcop-4.0-wp3e-core-closeout
```

原 `D:\FCoP` 工作区的修改和未跟踪文件不得清理、stash、覆盖或带入。

## 2. 编码前强制基线

修改生产代码前必须：

1. 使用 `--collect-only` 固定全部 119 个真实 node id；
2. 证明冻结 Test ID 仍为 60/60；
3. 运行完整 v4，确认恰为 `96 passed / 23 deferred`；
4. 把 23 个红灯逐项映射到下面的十组，不得只按文件计数；
5. 形成 `reports/FCOP-4.0-WP3E-IMPLEMENTABILITY-AND-RED-BASELINE.md`；
6. 证明本任务允许文件和复杂度预算足以实现；否则停止。

现存 23 个节点的唯一预期集合：

| 组 | 参数化节点数 | 冻结语义 |
|---|---:|---|
| C3-X01 | 1 | 冷存储导出中断不改变 archive NOW |
| C4-R01 dangling-gate-reference | 1 | Gate 必需弱引用悬空时 `REFERENCE_UNRESOLVED` 且零写入 |
| C6-X01 | 1 | T7 提交后响应丢失，精确重试 Existing、无二次消费 |
| C7-CREATE-01 | 1 | create 外部幂等不扩展到普通 T2 任意重放 |
| C8-X01 | 4 | PREPARED/TARGET_DURABLE/COMMITTED/RESPONSE_LOST |
| C8-X03 | 3 | divergent/corrupt-receipt/unsupported-filesystem |
| C8-STATE-01 | 5 | S1–S5 冻结恢复表 |
| C8-INDETERMINATE-01 | 1 | 不可证明状态只返回 INDETERMINATE/RECOVERY_REQUIRED |
| AT-05 | 3 | 三个故障点后的真实 transition 与机械恢复 |
| AT-06 | 3 | S2/S4/S5 恢复和证据保留 |

合计必须为 23。某节点已经自然转绿可以记录为 `NO_CODE_REQUIRED`，但不得因此扩大范围或发明替代测试。

若实际红灯集合、数量或根因不一致，以 `WP3E_BASELINE_MISMATCH` 停止。

## 3. WP3E 的唯一实现边界

WP3E 只允许四组工作。

### 3.1 两个边界尾项

#### Gate-required weak reference

`create_task(..., references_required_by_gate=True)` 仅表示本次操作中的 `references` 被 Gate 使用，因此必须在同一工作区解析且唯一；悬空返回 `REFERENCE_UNRESOLVED` 并零写入。

普通弱引用继续遵守冻结合同，不得把所有 `references` 全局升级为强引用。

#### Create-only external idempotency

`C7-CREATE-01` 必须证明：

- 重放相同 create 请求返回 Existing；
- T2 成功后再次提交旧 `inbox → active` 请求返回 `INVALID_TRANSITION`；
- 不向 T2/T3 增加 caller `operation_id`；
- 不把内部 receipt 变成任意时间的公共重放承诺。

如果节点已由 WP3B–WP3D 实现自然满足，只补证据，不修改代码。

### 3.2 单一五状态机械恢复

新增的公共 Toolkit 入口最多一个：

```python
Project.recover_operation(
    *,
    operation_id: str,
    source_path: pathlib.Path | str,
    target_path: pathlib.Path | str,
    receipt_path: pathlib.Path | str | None = None,
    filesystem: str = "local",
) -> dict[str, Any]
```

它不是第二个生命周期、数据库、Runtime recovery manager 或业务裁决器，只是对调用者明确给出的本工作区可见证据执行冻结 F4.9.9 五行表。

必须满足：

- source、target、receipt 必须解析到当前 workspace 内的允许路径；
- 禁止 `..`、绝对路径逃逸、盘符逃逸、symlink/junction 越界；
- source/target 必须编码同一 TASK 身份和一条合法 lifecycle edge；
- `filesystem=network` 或无法证明本地可靠语义时返回 `UNSUPPORTED_FILESYSTEM`；
- 同一事实只能归为五类之一；
- S1 `NOT_COMMITTED`：保留 source，不创建 target；
- S2 `RECOVERABLE_DUPLICATE`：先验证完整字节相同，再删除 source、持久化目录、将 receipt 完成到 COMMITTED；
- S3 `COMMITTED`：保留唯一 target，仅补全 COMMITTED receipt；
- S4 `DIVERGENT_DUPLICATE`：不删、不覆盖，返回 `RECOVERY_REQUIRED`；
- S5 `INDETERMINATE`：不猜测、不重建事实，保留可见证据，返回 `RECOVERY_REQUIRED`；
- 重复调用机械恢复必须幂等；
- 不创建 REVIEW，不追加业务 transition，不伪造 event；
- 不以 mtime、目录枚举顺序、较新文件或调用者偏好决定 NOW。

冻结测试的 compact observation receipt 与现有完整 lifecycle receipt 必须归一化为同一个内存证据结构和同一张五状态表；不得建立第二份持久 receipt、第二个 operations 目录或第二套分类器。

若两种 receipt 无法在不改变冻结合同、不破坏既有 WP3B/WP3D receipt 的前提下归一化，必须以 `RECOVERY_RECEIPT_CONTRACT_GAP` 停止，不得做兼容特判堆叠。

### 3.3 抽象故障边界

新增公共 Toolkit 测试入口最多一个：

```python
Project.inject_fault(
    *,
    operation: str,
    stage: str,
    once: bool = True,
) -> None
```

严格边界：

- 只接受冻结测试需要的 operation：`transition`、`export_archive`；
- 只接受抽象 stage：`PREPARED`、`TARGET_DURABLE`、`COMMITTED`、`RESPONSE_LOST`；
- fault plan 只存在于当前 `Project` 实例内存中；
- 不写配置文件、数据库、环境变量或新的权威状态；
- 不跨进程传播，不自动恢复，不成为 Runtime 服务；
- `once=True` 消费一次后移除；
- 没有已注册 fault 时生产路径字节行为与 WP3D accepted head 完全一致；
- 触发点必须位于既有 receipt 阶段提交边界，禁止绑定 Python 临时文件名、sleep 或函数内部偶然行号；
- fault exception 不增加新的 Base error code；
- `RESPONSE_LOST` 只发生在 durable commit 完成后。

冻结测试传入的 `internal_operation_id` 只能在当前实例存在匹配 fault plan 时作为测试/恢复定位符。它不得：

- 成为 T2/T3 的公共外部幂等键；
- 在无 fault plan 时改变正常请求身份；
- 绕过现有 Authorization/receipt exact retry；
- 创建第二种业务 operation record。

允许为 fault harness 使用安全、确定的 receipt 文件名，以满足冻结测试的观察路径；但文件仍必须位于同一个 `fcop/operations/`，内容和恢复必须复用同一 receipt/五状态实现。若这一约束无法成立，停止，不得修改冻结测试迁就实现。

### 3.4 非权威 archive 冷导出

新增公共 Toolkit 入口最多一个：

```python
Project.export_archive(*, task_id: str) -> dict[str, Any]
```

它只做冷存储副本：

- 输入 TASK 必须唯一位于 `fcop/_lifecycle/archive/`；
- 原 archive 路径和字节始终保持不变；
- 输出只能进入 `fcop/cold/`，其任何后代不得包含 `_lifecycle`；
- cold 文件不参与 NOW、状态解析、family digest、Authorization 或关系解析；
- 目标存在且同字节可返回 Existing；
- 目标存在但不同返回 `TARGET_ALREADY_EXISTS_DIFFERENT`，不得覆盖；
- 写入复用现有 durable publish 原语；
- `TARGET_DURABLE` fault 后 archive 仍是唯一 NOW；
- 不移动到 v3 `history/`，不调用 `archive_to_history`；
- 不新增 watcher、后台搬运器、定时器、索引或数据库。

## 4. 公共 API 与稳定性治理

WP3E 最多新增以下三个公共方法，名称不得增加：

```text
Project.recover_operation
Project.inject_fault
Project.export_archive
```

若实现不需要其中某个方法，不得为了凑数新增；但冻结 driver 需要的真实入口不得由 `__getattr__`、动态 catch-all、mock、测试内 monkeypatch 或空 stub 伪造。

新增的每个公共方法必须：

- 在 `src/fcop/v4/boundary.py` 中显式列入闭集策略；
- v3 workspace 上 Fail Closed 或保留明确 legacy 行为，不得改变既有 v3 方法签名；
- 更新 `tests/test_fcop/snapshots/public_surface.json`；
- 在 `CHANGELOG.md [Unreleased]` 标注 additive API surface change；
- 有真实生产入口单元测试；
- 不暴露 Host、Session、Scheduler、模型、网络或 CodeFlowMu 概念。

任何第四个公共 API 要求都触发 `PUBLIC_API_BUDGET_EXCEEDED`。

## 5. 复杂度预算

```yaml
NEW_PUBLIC_APIS_MAX: 3
AUTHORIZED_PUBLIC_APIS:
  - Project.recover_operation
  - Project.inject_fault
  - Project.export_archive
NEW_PRODUCTION_MODULES_MAX: 1
AUTHORIZED_NEW_MODULE_IF_PROVEN_NECESSARY: src/fcop/v4/recovery.py
NEW_RUNTIME_DEPENDENCIES: 0
NEW_BACKGROUND_COMPONENTS: 0
NEW_AUTHORITATIVE_STORES: 0
NEW_OPERATIONS_DIRECTORIES: 0
NEW_STATE_MACHINES: 0
NEW_LOCK_SYSTEMS: 0
NEW_BASE_ERROR_CODES: 0
NEW_ENVELOPE_TYPES: 0
FAULT_PLAN_DURABLE: false
```

优先扩展既有 `receipts.py`、`lifecycle.py` 与 Encoding 原语。只有 implementability 报告证明集中一个纯 `recovery.py` 能减少重复并保持单一分类器时，才允许增加该模块。

不得为通过测试增加 service、manager、repository、controller、daemon、queue、cache、DB、watcher、timer、scheduler 或第二个 journal。

## 6. 允许修改范围

### 6.1 生产文件

```text
src/fcop/project.py
src/fcop/v4/boundary.py
src/fcop/v4/creation.py
src/fcop/v4/lifecycle.py
src/fcop/v4/receipts.py
src/fcop/v4/encoding.py
src/fcop/v4/recovery.py     # 唯一可选新生产模块
```

### 6.2 单元、稳定性与发布记录

```text
tests/test_fcop/test_v4_boundary.py
tests/test_fcop/test_v4_creation.py
tests/test_fcop/test_v4_lifecycle.py
tests/test_fcop/test_v4_recovery.py   # 可新增
tests/test_fcop/snapshots/public_surface.json
CHANGELOG.md
```

### 6.3 证据交付

```text
reports/FCOP-4.0-WP3E-IMPLEMENTABILITY-AND-RED-BASELINE.md
reports/FCOP-4.0-WP3E-RECOVERY-STATE-PROOF.md
reports/FCOP-4.0-WP3E-FAULT-BOUNDARY-PROOF.md
reports/FCOP-4.0-WP3E-COLD-EXPORT-PROOF.md
reports/FCOP-4.0-WP3E-CONFORMANCE-CLOSEOUT.md
reports/FCOP-4.0-WP3E-RESULT.md
reviews/fcop-4.0/wp3e/MANIFEST.md
```

需要修改清单外文件必须停止并报告，不得先改后解释。

## 7. 冻结与禁止范围

严格禁止：

- 修改 `spec/fcop-4.0-spec.md`、中文规范、Schema、31 个 Base error codes；
- 修改、删减、重命名、skip、xfail 冻结 `tests/conformance/v4/**`；
- 修改 WP0–WP3D 历史任务书、报告、Manifest 或 Gate；
- 修改 MCP 注册、45 项工具、11 resources、3 templates、relay 或 PyPI；
- 修改规则包、AGENTS.md、CLAUDE.md、.mdc、Host profile；
- 修改 CodeFlowMu；
- 将 cold 目录变成生命周期第六桶；
- 为 recovery 创建数据库、第二 NOW truth、第二 journal 或 repair 自动裁决；
- 通过 mtime、latest、目录顺序或自动删除分歧证据恢复；
- 将 `inject_fault` 做成后台故障服务或正式 Runtime 控制平面；
- 扩展 create 之外的外部幂等合同；
- 修改 main、创建/合并 PR、打 tag、建 Release、发布 PyPI；
- 进入 WP4/WP5/WP6；
- 自行签署 `FCOP_4_CORE_IMPLEMENTATION_ACCEPTED`。

## 8. 强制单元测试

除冻结 Conformance 外，至少新增以下真实生产入口测试：

### 8.1 恢复分类

- S1–S5 每行正例；
- 同一事实不能命中两个分类；
- compact observation receipt 与完整 lifecycle receipt 归一到相同结果；
- source/target 不同 TASK、非法 edge、receipt path 越界、operation_id 不匹配拒绝；
- symlink/junction/path traversal 越界拒绝；
- S2 删除 source 前验证完整字节摘要；
- S3 只完成 receipt，不复制或追加 event；
- S4/S5 重复调用仍保留全部可见证据；
- network/unsupported filesystem 零写入。

### 8.2 Fault 边界

- 每个抽象 stage 恰触发一次；
- `once=True` 第二次不触发；
- 未注册 fault 的 byte-for-byte 回归；
- PREPARED、TARGET_DURABLE、COMMITTED、RESPONSE_LOST 后的物理事实分别可由五状态表解释；
- 触发后调用公共 recovery，不产生第二 TASK/event；
- fault plan 不落盘，不跨新 Project 实例；
- 不借 `internal_operation_id` 获得 T2/T3 外部重放。

### 8.3 Cold export

- archive 原文件路径、字节和 transition 不变；
- cold 输出不含 `_lifecycle`；
- 同内容重复导出 Existing；
- 异内容目标拒绝且不覆盖；
- TARGET_DURABLE fault 后 archive 仍唯一权威；
- cold 副本不参与 inspect_state、family digest 或关系解析。

### 8.4 回归

- C4 gate-required weak reference 的缺失与合法引用；
- C7 create Existing 与 T2 重放拒绝；
- WP3A–WP3D 全部新增测试继续通过；
- 三个公共 API 的 v3/v4 version boundary；
- public-surface snapshot 精确只有本任务授权增量。

## 9. 验证顺序与完成标准

必须记录完整命令、环境、退出码和真实结果：

1. 编码前 119 节点 collect-only；
2. 23 deferred 红灯基线；
3. WP3E 新增单元测试；
4. 十组目标节点逐项运行；
5. 全部 `tests/test_fcop/test_v4_*.py`；
6. 完整 v4 Static/Meta 与 Behavioral；
7. `tests/test_fcop` 全量；
8. 正确 `PYTHONPATH` 下 v3/非 v4 回归；
9. 隔离 `tests/test_fcop_mcp` 回归；
10. mypy/type check；
11. 授权文件 Ruff 与既有全仓 Ruff 差异；
12. `git diff --check`、UTF-8/LF/BOM；
13. 冻结文件 SHA、Test ID、allowlist、依赖和公共面差异；
14. 独立工作区 smoke；
15. Windows 原生 fault/recovery 测试；
16. 远端固定提交、父链与 SHA-256 回读。

完成门：

```yaml
FROZEN_TEST_IDS: 60/60
V4_COLLECT_ONLY: 119
V4_STATIC_META: 27/27
V4_BEHAVIORAL: 92 passed / 0 deferred / 0 unexpected
V4_TOTAL: 119 passed / 0 deferred
WP3E_TARGET_NODES: 23/23
TEST_FCOP: ZERO_FAILURES
V3_NEW_FAILURES: 0
MCP_NEW_FAILURES: 0
UNEXPECTED_FAILURES: 0
```

实际新增单元测试可使 `tests/test_fcop` 收集数上升，必须如实报告。不得通过减少收集数达标。

Linux/macOS 未原生运行必须写 `NOT_NATIVE_VERIFIED`，不能用类型检查冒充。

## 10. 停止条件

```text
TASKBOOK_IDENTITY_MISMATCH
INPUT_HEAD_MISMATCH
GATE_RECEIPT_MISMATCH
FROZEN_CONTRACT_MISMATCH
DIRTY_PRESERVED
WP3E_BASELINE_MISMATCH
FROZEN_CONFORMANCE_CONTRACT_CONFLICT
RECOVERY_RECEIPT_CONTRACT_GAP
RECOVERY_CLASSIFICATION_AMBIGUOUS
UNSAFE_PATH_BOUNDARY
PUBLIC_API_BUDGET_EXCEEDED
NEW_STATE_MACHINE_REQUIRED
SECOND_RECEIPT_SYSTEM_REQUIRED
SECOND_AUTHORITATIVE_STORE_REQUIRED
NEW_RUNTIME_DEPENDENCY_REQUIRED
UNAUTHORIZED_FILE_REQUIRED
UNEXPECTED_V3_REGRESSION
UNEXPECTED_V4_REGRESSION
UNEXPECTED_MCP_REGRESSION
PUBLIC_SURFACE_UNEXPECTED_DRIFT
REMOTE_DELIVERY_VERIFICATION_FAILED
```

出现任一条件，提交阻断报告并停止。不得扩大范围、修改冻结合同或转入 WP4 绕过。

## 11. GitHub 两提交交付

review 分支必须从本任务书 Commit 创建：

```text
review/fcop-4.0-wp3e-core-closeout
```

提交链固定：

```text
Taskbook Commit
  → Content Commit
  → Manifest Commit
```

Content Commit 包含允许范围内源码、单元测试、snapshot、CHANGELOG 和六份报告；不得包含 Manifest 或任务书修改。

Manifest Commit 只允许新增：

```text
reviews/fcop-4.0/wp3e/MANIFEST.md
```

推送后重新 fetch，验证：

- fetched HEAD；
- 两提交直接父链；
- Taskbook/Gate/frozen contract 祖先；
- Content/Manifest allowlist；
- 全部交付文件 SHA-256；
- remote main 未变；
- worktree 干净；
- 不使用 force push。

## 12. 最终回执格式

```yaml
WP3E_STATUS: COMPLETE | BLOCKED
AUTHORIZED_SCOPE: WP3E_ONLY
TASKBOOK_PATH: taskbooks/fcop-4.0/WP3E/01-Remaining-Core-Recovery-and-Conformance-Closeout-Taskbook-v1.0.zh.md
TASKBOOK_COMMIT: <sha>
TASKBOOK_SHA256: <sha256>
INPUT_HEAD: 99d0ab14a8e4e3b5d8580230a9df1d6dbec50b41
GATE_RECEIPT: reviews/fcop-4.0/gates/WP3D-CONVERGENCE-ACCEPTED.md
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
WORKTREE: D:\FCoP-wp3e-core-closeout
BRANCH: review/fcop-4.0-wp3e-core-closeout

RED_BASELINE: 23/23
WP3E_TARGET_NODES: 23/23
C3_X01: PASS | FAIL
C4_DANGLING_GATE_REFERENCE: PASS | FAIL
C6_X01: PASS | FAIL
C7_CREATE_BOUNDARY: PASS | FAIL
C8_X01: 4/4
C8_X03: 3/3
C8_STATE_01: 5/5
C8_INDETERMINATE_01: PASS | FAIL
AT_05: 3/3
AT_06: 3/3

FROZEN_TEST_IDS: 60/60
V4_COLLECT_ONLY: 119
V4_STATIC_META: 27/27
V4_BEHAVIORAL: 92 passed / 0 deferred / 0 unexpected
V4_TOTAL: 119 passed / 0 deferred
TEST_FCOP: <result>
V3_REGRESSION: <result>
V3_NEW_FAILURES: 0
MCP_REGRESSION: <result>
MCP_NEW_FAILURES: 0
UNEXPECTED_FAILURES: 0

RECOVERY_STATE_TABLE: 5/5
RECOVERY_RECEIPT_IMPLEMENTATIONS: 1
FAULT_BOUNDARIES: 4/4
COLD_EXPORT_NON_AUTHORITATIVE: PASS | FAIL
PUBLIC_SURFACE_SNAPSHOT: PASS | FAIL
CHANGELOG_ADDITIVE_ENTRY: PASS | FAIL

NEW_PUBLIC_APIS: <0..3>
NEW_PRODUCTION_MODULES: <0..1>
NEW_RUNTIME_DEPENDENCIES: 0
NEW_BACKGROUND_COMPONENTS: 0
NEW_AUTHORITATIVE_STORES: 0
NEW_OPERATIONS_DIRECTORIES: 0
NEW_STATE_MACHINES: 0
NEW_LOCK_SYSTEMS: 0
NEW_BASE_ERROR_CODES: 0
FROZEN_SPEC_FILES_MODIFIED: 0
FROZEN_CONFORMANCE_FILES_MODIFIED: 0
SCHEMA_FILES_MODIFIED: 0
MCP_IMPLEMENTATION_FILES_MODIFIED: 0
RULE_PACKAGE_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0

CONTENT_COMMIT: <sha>
MANIFEST_COMMIT: <sha>
REMOTE_HEAD: <sha>
REMOTE_PUSHED: true | false
REMOTE_REFETCH_VERIFIED: PASS | FAIL
DELIVERY_SHA256: <matched>/<total>
REMOTE_MAIN_UNCHANGED: true | false
WORKTREE_STATUS: CLEAN | DIRTY_PRESERVED
LINUX_NATIVE: PASS | FAIL | NOT_NATIVE_VERIFIED
MACOS_NATIVE: PASS | FAIL | NOT_NATIVE_VERIFIED

FCOP_4_CORE_IMPLEMENTATION_ACCEPTED: false
WP4_STARTED: false
MAIN_MODIFIED: false
RELEASE_CREATED: false
REQUESTED_GATE: FCOP_4_CORE_IMPLEMENTATION_ACCEPTED
```

完成远端交付后立即停止。只有 ADMIN 审核固定 GitHub review HEAD 并签署 `FCOP_4_CORE_IMPLEMENTATION_ACCEPTED`，才可另立 WP4.0 只读审计任务书。
