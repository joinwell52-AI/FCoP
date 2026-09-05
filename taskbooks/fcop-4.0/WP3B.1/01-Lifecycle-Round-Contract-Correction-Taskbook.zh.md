---
title: FCoP 4.0 WP3B.1 生命周期轮次与合同一致性修订任务书
document_role: EXECUTION_TASKBOOK
status: AUTHORIZED_FOR_WP3B_1_ONLY
execution_authorized: true
authorized_scope: WP3B_1_ONLY
input_head: 297dc06ece87f1d4adf938875cb19e59be87def0
taskbook_path: taskbooks/fcop-4.0/WP3B.1/01-Lifecycle-Round-Contract-Correction-Taskbook.zh.md
taskbook_delivery_branch: task/fcop-4.0-wp3b.1-lifecycle-round-correction
wp3b_content_commit: 6bdde7038f124e2a6c0895166a2f76fad05fc860
frozen_contract_commit: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
wp3b_gate_signed: false
wp3c_authorized: false
main_merge_authorized: false
release_authorized: false
requested_gate: WP3B_LIFECYCLE_ACCEPTED
---

# FCoP 4.0 WP3B.1 生命周期轮次与合同一致性修订任务书

## 0. 唯一执行授权

本文件是本轮唯一具有执行授权的任务书。

Codex 只允许执行 **WP3B.1**：修正 WP3B 中已经确认的收据轮次识别、当前 attempt 事实源和 REPORT 写入边界问题，并补充相应回归测试。

本轮不得进入 WP3C，不得实现 T4、T5、T6、T7，不得修改 Authorization、Profile evaluator、family digest、convergence、MCP、Schema、CodeFlowMu、`main` 或发布流程。

执行者可以选择局部实现方法，但不得改变冻结合同、事实源、Gate、错误码集合或授权范围。

完成后必须推送 GitHub review 分支，生成 Manifest，停止并请求 ADMIN 重新审核：

```text
GATE: WP3B_LIFECYCLE_ACCEPTED
```

执行者不得自行签署 Gate，不得在同一轮开始 WP3C。

---

## 1. 背景与当前判定

WP3B 已在以下提交交付：

```yaml
INPUT_HEAD: d2d2e9518451d58d165e3705f13f1ceb24388571
CONTENT_COMMIT: 6bdde7038f124e2a6c0895166a2f76fad05fc860
REVIEW_HEAD: 297dc06ece87f1d4adf938875cb19e59be87def0
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
```

ADMIN 审核结论：

```yaml
DELIVERY_INTEGRITY: PASS
SCOPE_COMPLIANCE: PASS
T2_BASIC_IMPLEMENTATION: PASS
T3_FIRST_ATTEMPT_IMPLEMENTATION: PASS
ATOMICITY_DIRECTION: PASS

P0_OPEN: 2
P1_OPEN: 1
WP3B_LIFECYCLE_ACCEPTED: false
WP3C_AUTHORIZED: false
```

本轮不是重写 WP3B，也不是扩展生命周期，而是把已经实现的 T2/T3 修正为可支持完整七边生命周期的稳定基础。

---

## 2. 权威顺序

### 2.1 事实判断优先级

```text
冻结合同 aec4c2b2…
> GitHub review HEAD 297dc06e… 的真实代码
> 冻结 Conformance 的测试意图与 Test ID
> WP3B 审计报告和 Manifest
> 本任务书中的问题说明
```

若规范、测试夹具和代码发生冲突，不得通过增加生产兼容分支掩盖冲突。必须按照冻结合同修正测试构造或实现，并在报告中记录。

### 2.2 执行授权优先级

```text
ADMIN Gate
> 本任务书
> WP3B 原任务书中仍适用的边界
> 其他报告、计划和历史文件
```

报告、测试结果和执行者自己的判断都不能扩大授权。

---

## 3. 开始条件与工作区

### 3.1 Git 起点与任务书提交

本任务书通过以下固定路径和独立分支发布：

```text
TASKBOOK_PATH: taskbooks/fcop-4.0/WP3B.1/01-Lifecycle-Round-Contract-Correction-Taskbook.zh.md
TASKBOOK_BRANCH: task/fcop-4.0-wp3b.1-lifecycle-round-correction
```

Codex 必须先读取 GitHub 上该路径的文件，并锁定用户提供或 GitHub 当前显示的 Taskbook Commit。聊天复制、下载副本和本地同名文件均不是执行权威。

代码基线必须是：

```text
297dc06ece87f1d4adf938875cb19e59be87def0
```

执行分支从 **Taskbook Commit** 创建；Taskbook Commit 的祖先必须包含上述代码基线，且代码基线到 Taskbook Commit 之间只能包含 `taskbooks/**` 文档。任务书本身随执行分支保留，不能在实现提交中改写。

建议使用独立 worktree 和分支：

```text
WORKTREE: D:\FCoP-wp3b1-round-correction
BRANCH: review/fcop-4.0-wp3b.1-lifecycle-round-correction
```

开始前必须确认：

1. `origin` 指向 `joinwell52-AI/FCoP`；
2. 起点提交远端可达；
3. Taskbook Commit 可达，且任务书 SHA-256 与最终发布回执一致；
4. `6bdde703…` 是 `297dc06e…` 的直接父提交；
5. 工作树干净；
6. 冻结合同文件与 `aec4c2b2…` 完全一致；
7. 原 `D:\FCoP` 和 CodeFlowMu 工作区不被修改。

工作树不干净时，不得在原工作树切换或覆盖用户改动；使用独立 worktree，无法安全隔离则停止并报告：

```text
BLOCKED: DIRTY_PRESERVED
```

### 3.2 编码与命令要求

- 中文 Markdown 使用 UTF-8、LF；
- 不使用 PowerShell 修改中文文件；
- 不执行自动升级、安装、发布或 `main` 合并；
- 不删除历史 receipt、临时故障证据或用户现场文件。

---

## 4. 本轮三个必须解决的问题

## 4.1 P0-A：T3 收据必须区分执行轮次

### 现状

当前 `matching_receipts()` 只按照以下字段选择收据：

```text
workspace_id + task_id + from_stage + to_stage
```

它没有使用 `attempt_id` 区分同一 TASK 的不同执行轮次，并把已经 `COMMITTED` 的历史 T3 收据继续当成当前调用的恢复候选。

因此合法流程：

```text
attempt A: active → review
T5/T6:     → active，生成 attempt B
attempt B: active → review
```

会被 attempt A 的旧 T3 receipt 阻塞，或错误进入旧操作恢复。

### 必须达到的合同结果

1. 每一次 T2/T3 文件事务都有独立、持久的内部操作身份；
2. T3 收据必须绑定其 `attempt_id`；
3. `COMMITTED` 历史收据保留为审计事实，但不得阻止新 attempt 的 T3；
4. 当前 attempt 存在未完成 T3 收据时，重试只能恢复这一轮，不得新建第二事件；
5. 当前 attempt 存在多个互相冲突的未完成收据时，返回 `RECOVERY_REQUIRED` 并保留全部证据；
6. 丢失响应后，同一轮重试返回已提交结果，不重复 TASK、不重复 event、不覆盖 target；
7. 收据选择不得依赖 mtime、目录顺序、最新文件名或进程内缓存；
8. 不得删除旧收据来“解决”冲突；
9. 不得为 T2/T3增加新的公共 `operation_id` 承诺；
10. 不得引入数据库、索引服务、后台恢复器或第二状态机。

### 允许的实现自由

Codex 可以自行设计私有选择器、收据索引字段或确定性分类步骤，但必须证明：

```text
历史已完成轮次
当前未完成轮次
当前已完成但响应丢失轮次
损坏或冲突轮次
```

能够仅依据持久文件事实确定性区分。

如果在不改变冻结合同的情况下无法做到，停止并报告：

```text
BLOCKED: RECEIPT_ROUND_IDENTITY_GAP
```

不得用删除收据、只保留最后一个收据或放宽 Fail Closed 解决。

---

## 4.2 P0-B：当前 attempt 只能来自 transition history

### 现状

当前生产代码为了适配冻结测试夹具，允许：

```yaml
attempt_id: urn:uuid:...
transitions: []
```

并把顶层 `attempt_id` 当作当前轮次。

这与冻结合同冲突。冻结合同规定：

> 当前 attempt 是最后一次进入 active 的 transition 上的 `attempt_id`。

### 必须达到的合同结果

1. 生产 `current_attempt()` 只读取 transition history；
2. 顶层 `attempt_id` 不得成为 Core 的隐藏事实源；
3. 无合法进入 active 的 transition 时返回冻结错误，不得猜测；
4. 若同时存在顶层 `attempt_id` 与 transition attempt，以 transition 为唯一事实源；
5. 冻结 Test ID、测试目的和预期错误不得改变；
6. 测试 fixture 必须构造包含合法 active-entry event 的状态，不得要求生产代码识别“这是测试数据”；
7. 不得为 fixture 在生产接口中增加环境变量、测试模式、私有后门或路径识别。

### Conformance 夹具修订规则

允许修订 `tests/conformance/v4/fixtures.py` 以及确有必要的既有断言，使物化的 active/review/done/archive TASK 至少具有可证明的 active-entry attempt history。

但必须遵守：

- 60 个冻结 Test ID 不增、不减、不改名；
- 不删除断言；
- 不用 `skip`、`xfail`、mock driver 或硬编码 PASS；
- 不修改错误码期待来迎合实现；
- 不增加冻结合同不存在的规则；
- 所有修改逐项写入 `CONTRACT-TEST-ALIGNMENT` 报告；
- 若某个测试目的与冻结合同确实不可同时成立，停止并报告：

```text
BLOCKED: FROZEN_CONFORMANCE_CONTRACT_CONFLICT
```

---

## 4.3 P1-C：REPORT 写入不得增加未冻结的 active-only 策略

### 现状

当前 `write_report()` 对当前 attempt 增加了“TASK 必须处于 active”的限制。这不是冻结 Core 合同中的规则，并会阻断 review/done/archive 阶段追加 replacement REPORT。

### 必须达到的合同结果

1. REPORT 仍是 append-only 正式事实；
2. replacement 必须引用同一 subject、同一 attempt 的唯一当前 head；
3. 当前 head 的判断必须在 family lock 内重新读取；
4. TASK 不在 active 时，不能仅因状态而拒绝一个其他方面合法的 replacement；
5. replacement 不重写旧 REPORT，不回写旧 T3 event；
6. 后续 T4/T7 是否接受 replacement 后的新 head，由后续证据 Gate 判断，本轮不得提前实现；
7. final/replacement 的既有重复、分叉和旧 attempt 错误继续 Fail Closed；
8. 不得把 CodeFlowMu 角色、PM/QA 审批或产品策略放进 REPORT Core。

如果执行者认为 active-only 是冻结合同的必然推论，必须引用准确条款并形成阻断报告，不得静默保留。

---

## 5. 允许与禁止的代码范围

### 5.1 允许修改

在确有必要且保持最小改动时，允许：

```text
src/fcop/v4/lifecycle.py
src/fcop/v4/receipts.py
src/fcop/v4/creation.py
src/fcop/v4/linearization.py          # 仅当共享锁边界确需修正

tests/test_fcop/test_v4_lifecycle.py
tests/conformance/v4/fixtures.py
tests/conformance/v4/test_c3_lifecycle.py      # 仅合同夹具对齐所必需
tests/conformance/v4/test_c5_convergence.py    # 仅合同夹具对齐所必需
tests/conformance/v4/test_c8_recovery.py       # 仅合同夹具对齐所必需

reports/FCOP-4.0-WP3B.1-*.md
reviews/fcop-4.0/wp3b.1/MANIFEST.md
```

可以新增一个私有测试辅助模块，但必须说明为什么不能放入现有测试文件；不得新增生产层次、公共 facade 或依赖。

### 5.2 禁止修改

```text
spec/fcop-4.0-spec.md
spec/fcop-4.0-spec.zh.md
schemas/**
src/fcop/errors.py
src/fcop/project.py
src/fcop/v4/boundary.py
mcp/**
CodeFlowMu/**
```

同时禁止：

- 实现 T4/T5/T6/T7；
- 实现 Authorization、Profile evaluator 或 authorization consumption；
- 实现 convergence REVIEW、family digest 或 Root archive；
- 暴露公共 recovery API；
- 新建 Runtime store、SQLite、缓存、队列、daemon、watcher、timer、scheduler；
- 新增运行时依赖；
- 修改 31 个冻结错误码；
- 修改 v3 方法签名或 v3 生命周期语义；
- 合并 `main`、建 tag、建 Release、上传 PyPI；
- 修改 CodeFlowMu。

如果修复必须越过允许范围，停止并请求 ADMIN，不得自行扩权。

---

## 6. 强制新增的回归场景

## 6.1 多轮 T3 与历史收据

至少覆盖：

1. attempt A 完成 T3，保留 `COMMITTED` receipt；
2. 通过测试夹具物化一次符合合同的 T5 或 T6 后状态，生成 attempt B；
3. attempt B 写入自己的 REPORT 并成功完成 T3；
4. 两轮 receipt 均保留，operation identity 不同；
5. TASK 中存在两个不同轮次的 T3 event，各自证据绑定正确；
6. attempt B 丢失响应后重试，返回 B 的已有结果，不返回 A；
7. attempt A 与 B 使用相同 actor、`report_ref=None` 时仍能正确区分；
8. 历史 `COMMITTED` receipt 与当前 `PREPARED` receipt 共存时，只恢复当前轮；
9. 同一当前 attempt 出现两个冲突未完成 receipt 时 Fail Closed；
10. 不通过删除任何历史 receipt 获得成功。

测试夹具可以物化 T5/T6 已完成后的文件事实，但不得调用或实现尚未授权的生产 T5/T6。

## 6.2 attempt 事实源

至少覆盖：

1. 顶层 `attempt_id`、空 transitions：生产读取返回 `ATTEMPT_MISMATCH`；
2. 顶层 attempt 与 transition attempt 不同：只认 transition；
3. 多次进入 active：只认最后一个合法 active-entry event；
4. 当前 attempt 的 REPORT 通过；
5. 旧 attempt REPORT 返回 `ATTEMPT_MISMATCH`；
6. Conformance fixture 不再依赖顶层 attempt fallback；
7. 60 个冻结 Test ID 保持不变。

## 6.3 REPORT append-only 与状态边界

至少覆盖：

1. active 状态 final REPORT 正常；
2. active 状态 replacement 与 T3 竞态仍可线性化；
3. review 状态合法 replacement 可以追加；
4. done 状态合法 replacement 可以追加；
5. archive 状态合法 replacement 可以追加；
6. replacement 必须引用唯一当前 head；
7. replacement 不修改旧文件和旧 transition event；
8. 两个并发 replacement 不得形成被静默接受的双 head；
9. 非当前 attempt、分叉 head、无有效 head继续返回冻结错误。

如果 archive 阶段 replacement 与冻结合同存在真实解释歧义，必须先报告，不得通过 Profile 策略或隐藏状态机裁决。

## 6.4 既有 WP3B 不回退

必须继续通过：

- WP3B 原 9/9 目标节点；
- T2 新 attempt；
- T3 当前 REPORT head 和完整字节 digest；
- Branch create / Root T3 竞态；
- REPORT write / T3 竞态；
- PREPARED、TARGET_DURABLE、COMMITTED 恢复；
- target-visible/PREPARED 为 `INDETERMINATE`；
- target-absent/TARGET_DURABLE 为 `INDETERMINATE`；
- response loss 不重复 event；
- receipt 相对 POSIX 路径；
- workspace relocation 后可恢复；
- 多路径 NOW 返回 `STATE_AMBIGUOUS`。

---

## 7. 实现约束

### 7.1 保持文件原生

权威事实仍然只能是：

```text
TASK/REPORT/ISSUE/REVIEW 文件
生命周期路径 NOW
TASK transitions PAST
私有 Encoding/Toolkit receipt
```

不得用内存 generation、数据库行、后台索引、锁文件时间戳或 UI 状态替代。

### 7.2 保持单一写入边界

Branch create、T2/T3、REPORT final/replacement 继续使用同一个 Root-family 短锁语义。

允许调整锁内读取和收据筛选顺序，但必须保持：

```text
确定 family identity
→ 获取短锁
→ 重新读取持久事实
→ 验证当前路径/attempt/head/receipt
→ 单次提交
→ 释放短锁
```

不得持锁执行 Agent 工作、网络调用、模型调用或长时间计算。

### 7.3 保持恢复保守性

- target no-overwrite；
- receipt 初次发布 no-overwrite；
- 只有同一 receipt 的阶段更新允许专用原子 replace；
- divergence/indeterminate 不删除、不覆盖；
- 历史 receipt 永久保留；
- 不按时间清理 lock 或失败临时文件；
- 不自动创建 repair REVIEW。

---

## 8. 先证明、后修改

编码前必须生成：

```text
reports/FCOP-4.0-WP3B.1-CORRECTION-PLAN.md
```

至少说明：

1. 当前 receipt 为什么会阻塞第二轮 T3；
2. 新选择算法如何区分历史轮次和当前轮次；
3. 崩溃时只有 target、只有 source、两者并存时如何找到正确 receipt；
4. 为什么不会把旧 `COMMITTED` receipt 当作新 attempt；
5. fixture 哪些状态不符合 attempt 合同；
6. 哪些测试辅助文件需要改，为什么不是修改协议；
7. REPORT active-only 限制如何处理；
8. 精确修改文件清单；
9. 复杂度预算。

若证明不能闭合，停止，不得先写补丁。

---

## 9. 验证矩阵

必须依次运行并保存完整结果：

### 9.1 定向测试

```text
WP3B.1 新增 receipt-round 测试
WP3B.1 attempt-source 测试
WP3B.1 REPORT boundary 测试
WP3B 原 test_v4_lifecycle.py
受影响的 C3/C5/C8 Conformance
```

要求：

```text
NEW_TARGETS: 100% PASS
WP3B_TARGET_NODES: 9/9 PASS
UNEXPECTED_FAILURES: 0
SKIP/XFAIL_ADDED: 0
```

### 9.2 全量回归

至少运行：

```text
tests/test_fcop
tests/test_fcop_mcp（必须绑定当前 worktree 的 src 与 mcp/src）
全量非 Conformance 回归
完整 v4 static/meta
完整 v4 behavioral
v4 collect-only
mypy
changed-file Ruff
git diff --check
```

验收要求：

- v3 新失败为 0；
- MCP 新失败为 0；
- WP3A/WP3A.1/WP3B 已通过节点不得回红；
- 60/60 冻结 Test ID 不变；
- 剩余 deferred failures 只能减少，不能新增；
- 不得把 failure 改成 skip/xfail；
- 全仓既有 Ruff 基线可以如实保留，但 changed files 必须通过；
- Linux/macOS 未实际运行时，只能声明类型检查，不得宣称原生测试通过。

### 9.3 防空壳检查

必须证明：

- 新测试调用真实 `Project` 生产入口；
- 测试没有在 driver 中伪造返回值；
- fixture 只负责构造持久事实，不承担生产裁决；
- 不以 monkeypatch 绕过正常行为；
- 故障注入仅用于到达无法自然稳定复现的物理窗口。

---

## 10. 复杂度预算

最终报告必须逐项给出：

```yaml
NEW_RUNTIME_DEPENDENCIES: 0
NEW_BACKGROUND_COMPONENTS: 0
NEW_AUTHORITATIVE_STORES: 0
NEW_PUBLIC_APIS: 0
PUBLIC_APIS_REMOVED: 0
NEW_BASE_ERROR_CODES: 0
V3_METHOD_SIGNATURE_CHANGES: 0
FROZEN_SPEC_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0
```

建议限制：

- 不新增生产模块；
- 优先修改现有 `lifecycle.py`、`receipts.py`、`creation.py`；
- 不复制第二套 report-head、receipt-classification 或 family-lock 算法；
- 如果同一规则出现两份实现，必须收敛为一个私有函数；
- 不为未来 WP3C 预建抽象层。

---

## 11. 必须生成的报告

```text
reports/FCOP-4.0-WP3B.1-CORRECTION-PLAN.md
reports/FCOP-4.0-WP3B.1-RECEIPT-ROUND-PROOF.md
reports/FCOP-4.0-WP3B.1-CONTRACT-TEST-ALIGNMENT.md
reports/FCOP-4.0-WP3B.1-CORRECTION-RESULT.md
reviews/fcop-4.0/wp3b.1/MANIFEST.md
```

### 11.1 RECEIPT-ROUND-PROOF 必须包含

- 旧算法失败序列；
- 新收据相关性判定表；
- attempt A/B 两轮实例；
- lost-response 实例；
- 多收据冲突实例；
- 旧收据保留证明；
- 不使用 mtime/目录顺序证明。

### 11.2 CONTRACT-TEST-ALIGNMENT 必须包含

- 每个被改 fixture/test 文件；
- 修改前的不规范事实；
- 对应冻结条款；
- 修改后的持久文件形状；
- Test ID 和测试目的未变化证明；
- 生产 fallback 已删除证明。

### 11.3 CORRECTION-RESULT 必须包含

- 三个问题的最终状态；
- 精确文件清单；
- 测试命令和实际数字；
- deferred failure 清单变化；
- 复杂度预算；
- 已知限制；
- 未进入 WP3C 的声明。

---

## 12. GitHub 审核交付

继续采用两提交交付：

### 12.1 Content Commit

包含全部代码、测试和四份报告，不包含 Manifest。

建议提交信息：

```text
fix(fcop): align WP3B lifecycle rounds with frozen contract
```

### 12.2 Manifest Commit

第二次提交只能新增或更新：

```text
reviews/fcop-4.0/wp3b.1/MANIFEST.md
```

建议提交信息：

```text
docs(fcop): deliver WP3B.1 correction review manifest
```

### 12.3 Manifest 必须记录

```yaml
WP3B_1_STATUS:
AUTHORIZED_SCOPE: WP3B_1_ONLY
INPUT_HEAD: 297dc06ece87f1d4adf938875cb19e59be87def0
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6

RECEIPT_ROUND_IDENTITY: PASS | BLOCKED
HISTORICAL_RECEIPT_REUSE: PASS | BLOCKED
CURRENT_ATTEMPT_SOURCE: TRANSITION_ONLY | BLOCKED
TOP_LEVEL_ATTEMPT_FALLBACK: REMOVED | BLOCKED
CONFORMANCE_ALIGNMENT: PASS | BLOCKED
REPORT_STATE_POLICY: CONTRACT_ALIGNED | BLOCKED

WP3B_TARGET_NODES:
WP3B_1_NEW_TESTS:
FROZEN_TEST_IDS: 60/60
V3_REGRESSION:
MCP_REGRESSION:
V4_STATIC_META:
V4_BEHAVIORAL:
V4_COLLECT_ONLY:
UNEXPECTED_FAILURES:

NEW_RUNTIME_DEPENDENCIES: 0
NEW_BACKGROUND_COMPONENTS: 0
NEW_AUTHORITATIVE_STORES: 0
NEW_PUBLIC_APIS: 0
NEW_BASE_ERROR_CODES: 0
FROZEN_SPEC_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0
MAIN_MODIFIED: false
WP3C_STARTED: false

CONTENT_COMMIT:
MANIFEST_COMMIT: SELF
REMOTE_HEAD: SELF_AFTER_PUSH
REMOTE_PUSHED:
REMOTE_REFETCH_VERIFIED:
DELIVERY_SHA256:
REQUESTED_GATE: WP3B_LIFECYCLE_ACCEPTED
```

Manifest 必须列出每个交付文件的 Git blob 字节数和 SHA-256。Manifest 不计算自己的递归 SHA-256。

### 12.4 远端回读

推送后必须重新 fetch 并验证：

1. 远端 HEAD 等于本地 Manifest Commit；
2. Input HEAD 是 Content Commit 祖先；
3. Content Commit 是 Manifest Commit 直接父提交；
4. 两提交之间唯一差异是 Manifest；
5. 每个交付文件的远端字节和 SHA-256 匹配；
6. 冻结规范未变；
7. `origin/main` 未变；
8. 没有 tag、Release 或 merge；
9. 工作树干净。

不得 force push。

---

## 13. 停止条件

发生以下任一情况必须停止：

```text
RECEIPT_ROUND_IDENTITY_GAP
FROZEN_CONFORMANCE_CONTRACT_CONFLICT
REPORT_STATE_CONTRACT_AMBIGUITY
FROZEN_SPEC_CHANGE_REQUIRED
NEW_ERROR_CODE_REQUIRED
PUBLIC_API_CHANGE_REQUIRED
WP3C_CODE_REQUIRED
V3_REGRESSION
MCP_REGRESSION
DIRTY_PRESERVED
REMOTE_DELIVERY_MISMATCH
```

停止时只提交阻断报告；不得自行改变合同、测试目标或授权范围。

---

## 14. 完成标准

只有全部满足才允许声明 WP3B.1 完成：

1. 历史 T3 receipt 不阻塞新 attempt；
2. 同一当前 attempt 的故障重试不产生第二事件；
3. 多轮 T3 测试通过；
4. `current_attempt` 只以 transition history 为事实源；
5. 测试 fixture 不再迫使生产代码识别顶层 attempt；
6. REPORT 写入不再包含未冻结的 active-only Core 策略；
7. WP3B 原 9/9 节点继续通过；
8. v3/MCP 无新回归；
9. 60 个冻结 Test ID 不变；
10. 无新依赖、后台组件、权威 store、公共 API 或错误码；
11. GitHub 两提交交付与远端回读通过；
12. 未进入 WP3C，未修改 main，未发布。

---

## 15. 最终回执模板

```yaml
WP3B_1_STATUS: COMPLETE | BLOCKED
AUTHORIZED_SCOPE: WP3B_1_ONLY
INPUT_HEAD: 297dc06ece87f1d4adf938875cb19e59be87def0
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
WORKTREE:
BRANCH: review/fcop-4.0-wp3b.1-lifecycle-round-correction

RECEIPT_ROUND_IDENTITY:
MULTI_ATTEMPT_T3:
LOST_RESPONSE_CURRENT_ROUND:
HISTORICAL_RECEIPTS_PRESERVED:
CURRENT_ATTEMPT_SOURCE:
TOP_LEVEL_ATTEMPT_FALLBACK:
CONFORMANCE_ALIGNMENT:
REPORT_STATE_POLICY:

WP3B_TARGET_NODES:
WP3B_1_NEW_TESTS:
FROZEN_TEST_IDS: 60/60
V3_REGRESSION:
MCP_REGRESSION:
V4_STATIC_META:
V4_BEHAVIORAL:
V4_COLLECT_ONLY:
UNEXPECTED_FAILURES:

FILES_MODIFIED:
FROZEN_SPEC_FILES_MODIFIED: 0
SCHEMA_FILES_MODIFIED: 0
MCP_IMPLEMENTATION_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0
NEW_RUNTIME_DEPENDENCIES: 0
NEW_BACKGROUND_COMPONENTS: 0
NEW_AUTHORITATIVE_STORES: 0
NEW_PUBLIC_APIS: 0
NEW_BASE_ERROR_CODES: 0

CONTENT_COMMIT:
MANIFEST_COMMIT:
REMOTE_HEAD:
REMOTE_PUSHED:
REMOTE_REFETCH_VERIFIED:
DELIVERY_SHA256:
COMMIT_REACHABILITY:

WP3B_LIFECYCLE_ACCEPTED: false
WP3C_STARTED: false
MAIN_MODIFIED: false
RELEASE_CREATED: false
REQUESTED_GATE: WP3B_LIFECYCLE_ACCEPTED
```

完成后停止，等待 ADMIN 审核。没有 ADMIN 签署的 `WP3B_LIFECYCLE_ACCEPTED`，不得开始 WP3C。
