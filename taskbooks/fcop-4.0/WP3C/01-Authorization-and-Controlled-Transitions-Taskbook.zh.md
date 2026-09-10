---
title: FCoP 4.0 WP3C 授权与受控生命周期迁移任务书
document_role: EXECUTION_TASKBOOK
status: AUTHORIZED_FOR_WP3C_ONLY
execution_authorized: true
authorized_scope: WP3C_ONLY
input_head: 511039db227a23ae3e2d79aaae775a92ba392f5c
taskbook_path: taskbooks/fcop-4.0/WP3C/01-Authorization-and-Controlled-Transitions-Taskbook.zh.md
taskbook_delivery_branch: task/fcop-4.0-wp3c-authorization-transitions
frozen_contract_commit: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
wp3b_accepted_review_head: 511039db227a23ae3e2d79aaae775a92ba392f5c
wp3b_lifecycle_accepted: true
wp3d_authorized: false
main_merge_authorized: false
release_authorized: false
requested_gate: WP3C_AUTHORIZATION_ACCEPTED
---

# FCoP 4.0 WP3C 授权与受控生命周期迁移任务书

## 0. 唯一执行授权

本文件是 WP3C 唯一具有执行授权的任务书。

Codex 只允许完成以下范围：

1. 将可信 Profile evaluator 从 `Project` 初始化边界接入 FCoP 4.0 私有实现；
2. 实现 Authorization REVIEW 的结构、绑定、三值裁决、摘要和 single-use 消费验证；
3. 实现 T4 `review → done`；
4. 实现 T5 `review → active`；
5. 实现 T6 `done → active`；
6. 使 T4/T5/T6 复用 WP3B 已验收的文件事务、收据、恢复和 Root-family 短锁；
7. 增加真实生产接口测试并交付 GitHub review 分支。

本轮明确不实现：

- T7 `done → archive`；
- `family_digest`；
- convergence REVIEW 的创建或验证；
- Root archive、Branch 终态门；
- MCP、Schema、迁移、发布或 CodeFlowMu 适配；
- 公共 recovery/fault-injection API；
- 任何固定 ADMIN、PM、QA、DEV、OPS、EVAL 角色规则。

本轮完成后必须停止并请求 ADMIN 审核：

```text
GATE: WP3C_AUTHORIZATION_ACCEPTED
```

执行者不得自行签署 Gate，不得继续 WP3D，不得合并 `main`，不得发布。

---

## 1. 已验收基线

```yaml
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
WP3B_1_CONTENT_COMMIT: b4648d223c2303997fe394c30feaa68e070264d2
WP3B_1_REVIEW_HEAD: 511039db227a23ae3e2d79aaae775a92ba392f5c
WP3B_LIFECYCLE_ACCEPTED: true
WP3C_AUTHORIZED: true
WP3D_AUTHORIZED: false
```

WP3B.1 已验收的事实不得回退：

- T2/T3 文件事务与五状态恢复；
- T3 收据按当前执行轮次选择；
- 历史收据保留但不阻塞后续轮次；
- 当前 attempt 只来自最后一个合法 active-entry transition；
- 顶层 `attempt_id` 不是事实源；
- REPORT replacement 在各生命周期状态保持 append-only；
- Branch create、REPORT、T2/T3 共用 Root-family 线性化边界；
- 不新增 Runtime、后台组件、权威数据库或公共重放承诺。

WP3C 必须在这些能力之上增加授权迁移，不能复制第二套生命周期、锁、收据或恢复系统。

---

## 2. 权威顺序

### 2.1 事实判断

```text
冻结合同 aec4c2b2…
> 已验收 review HEAD 511039db… 的真实代码
> 冻结 Conformance Test ID 与测试意图
> WP3B/WP3B.1 证明及 Manifest
> 本任务书
> 其他说明与历史材料
```

### 2.2 执行授权

```text
ADMIN 已签署 WP3B_LIFECYCLE_ACCEPTED
> 本 GitHub 固定任务书
> taskbooks/README.zh.md
> 其他报告、计划和历史任务书
```

规范、代码、测试或任务书若出现无法在授权范围内闭合的真实冲突，必须停止并报告；不得通过放宽验证、修改冻结规范或增加隐藏策略解决。

---

## 3. GitHub 身份与工作区

任务书固定位置：

```text
REPOSITORY: joinwell52-AI/FCoP
TASKBOOK_PATH: taskbooks/fcop-4.0/WP3C/01-Authorization-and-Controlled-Transitions-Taskbook.zh.md
TASKBOOK_BRANCH: task/fcop-4.0-wp3c-authorization-transitions
CODE_BASELINE: 511039db227a23ae3e2d79aaae775a92ba392f5c
```

Codex 开始前必须：

1. fetch 远端 taskbook 分支；
2. 读取 GitHub 上的任务书，不使用聊天复制文本或本地旧副本作为权威；
3. 验证用户提供的 Taskbook Commit；
4. 计算本文件 SHA-256，并与用户提供值完全一致；
5. 验证 Taskbook Commit 的祖先包含 `511039db…`；
6. 验证 `511039db…` 到 Taskbook Commit 之间仅新增本任务书；
7. 验证冻结中英文规范与 `aec4c2b2…` 一致；
8. 从 Taskbook Commit 创建独立 review 分支与 worktree。

建议：

```text
WORKTREE: D:\FCoP-wp3c-authorization
BRANCH: review/fcop-4.0-wp3c-authorization-transitions
```

原 `D:\FCoP` 工作区、其脏文件和 CodeFlowMu 必须保持不动。工作树无法安全隔离时停止：

```text
BLOCKED: DIRTY_PRESERVED
```

中文 Markdown 必须使用 UTF-8、LF；不得使用 PowerShell 修改中文文件。

---

## 4. 当前真实代码边界

WP3C 开始时必须先复核并在计划报告中引用实际代码：

1. `Project.__init__()` 已接受 `trusted_profiles`，并复制到只读映射，但当前 `_Creation`/`Lifecycle` 尚未消费它；
2. `creation._reject_caller_authority()` 已拒绝业务参数夹带 evaluator、resolver、registry 等裁判逻辑；
3. `Lifecycle.transition()` 当前只执行 T2/T3，对 T4–T7 返回未实现；
4. `write_review()` 已能追加 REVIEW；`mark_human_approved()` 在 v4 中追加新 REVIEW，不原地改写旧文件；
5. WP3B 的 receipt、`family_boundary()`、no-overwrite、目录持久化和响应丢失测试基础必须复用；
6. 当前尚无独立的 Authorization 生产模块，也没有 T4/T5/T6 生产实现。

若复核结果与以上不一致，先记录差异，不得机械照任务书改代码。

---

## 5. 实现前必须完成的证明

编码前生成：

```text
reports/FCOP-4.0-WP3C-AUTHORIZATION-MODEL.md
reports/FCOP-4.0-WP3C-IMPLEMENTATION-PLAN.md
```

至少回答：

1. 可信 evaluator 如何只在 `Project` 初始化时注册，如何以不可被调用请求替换的方式传入私有 v4 组件；
2. manifest 中已采用 `profiles` 与运行时可信 evaluator registry 如何分别承担“采用声明”和“裁决能力”；
3. `AUTHORIZED`、`DENIED`、`UNKNOWN`、无 evaluator、异常返回和 evaluator 抛错分别如何 Fail Closed；
4. Authorization REVIEW 的 subject、edge、attempt、time、scope、profile、issuer proof 和 references 如何验证；
5. T4/T5 的 acceptance/rejection REVIEW 何时可以同时作为 authorization，何时必须引用独立 authorization REVIEW；
6. single-use 消费事实存在哪里，为什么 transition 中的 `authorization_ref + authorization_digest` 足以审计；
7. 相同授权精确重试与不同迁移复用如何区分；
8. T5/T6 从旧 attempt 进入新 attempt 时，收据如何同时识别 source round 与 target round；
9. PREPARED、TARGET_DURABLE、COMMITTED 和 response-loss 各窗口如何避免重复消费、重复 event 和重复 attempt；
10. T4 与 T5 并发竞争时如何由同一个 family lock 只提交一条边；
11. 哪些文件需要修改，为什么每一项都属于 WP3C；
12. 复杂度预算是否满足第 11 节。

证明无法闭合时停止：

```text
BLOCKED: WP3C_IMPLEMENTABILITY_GAP
```

---

## 6. Authorization 信任边界

### 6.1 两个不同事实

必须严格区分：

```text
fcop.json profiles[]
  = 工作区声明已经采用哪些 Profile ID

Project(trusted_profiles=...)
  = 当前可信初始化边界为这些 Profile ID 注册的裁决实现
```

两者缺一不可。manifest 的字符串不能自己证明签发权；运行时 registry 中存在 evaluator，也不能绕过 manifest 的 adopted Profile 声明。

### 6.2 evaluator 调用

生产实现只允许从可信初始化 registry 取得 evaluator。业务 `transition()` 参数不得接受或传播：

```text
profile_evaluator
profile_resolver
trusted_profiles
profile_registry
authorization_evaluator
caller_judge
host_allowlist_match
```

以及任何等价的调用者裁判对象。

evaluator 的最小输入必须来自持久 Authorization REVIEW：

```yaml
profile_ref: <id>
issuer: <REVIEW sender>
proof: <REVIEW issuer_proof>
```

只有严格结果 `AUTHORIZED` 可以通过。`DENIED`、`UNKNOWN`、未知返回、异常、缺失 evaluator 或不可调用对象均不得授权迁移。不得把 `actor`、`sender: ADMIN`、Host allowlist、UI 按钮或调用成功当作授权证明。

### 6.3 错误语义

必须保持冻结错误语义：

- 工作区没有可用已采用 Profile：`AUTHORIZATION_PROFILE_UNAVAILABLE`；
- 需要授权但未提供 authorization：`AUTHORIZATION_REQUIRED`；
- Profile 未采用、绑定错误、裁决非 AUTHORIZED、调用者夹带裁判或结构不可信：`AUTHORIZATION_INVALID`；
- 已过期：`AUTHORIZATION_EXPIRED`；
- single-use 被不同迁移再次使用：`AUTHORIZATION_REUSED`；
- 已绑定证据字节变化：`EVIDENCE_DIGEST_MISMATCH`。

错误优先级必须在实现计划中列成表，并由测试固定。不得根据测试顺序偶然决定返回哪个错误。

---

## 7. Authorization REVIEW 验证

Authorization 仍是 REVIEW，不得新增第五类信封或数据库授权表。

验证至少包括：

```yaml
review_kind: authorization | acceptance | rejection
subject_ref: <current TASK>
decision: authorize | approved | rejected
transition:
  from: <source stage>
  to: <target stage>
authorization_scope: single_use
issued_at: <timezone-aware date-time>
expires_at: <timezone-aware date-time or null>
attempt_id: <source attempt or null according to frozen edge contract>
family_digest: null
references: [...]
profile_ref: <adopted Profile ID>
issuer_proof: <Profile-consumable proof>
```

要求：

1. REVIEW 文件必须存在、UTF-8/LF 合法、ID/路径/类型一致；
2. `subject_ref` 必须绑定当前 TASK；
3. `transition.from/to` 必须绑定本次边；
4. 需要 attempt 的边必须绑定 source TASK 的当前 attempt；
5. `profile_ref` 必须同时出现在 manifest 与可信 registry；
6. `expires_at` 不得早于消费提交时刻；
7. `authorization_scope` 首期只接受 `single_use`；
8. Authorization REVIEW 的完整文件字节摘要写入 transition；
9. 消费前必须扫描并验证既有 transition 中相同 `authorization_ref`；
10. 相同 ref、digest、edge、subject、evidence 的已提交精确重试返回 Existing；
11. 相同 ref 被不同 edge 或不同已提交事实消费返回 `AUTHORIZATION_REUSED`；
12. 不得原地标记 REVIEW 为 consumed，不得重写或删除 REVIEW。

若 acceptance/rejection REVIEW 同时携带完整授权字段并通过 Profile 裁决，可以同时作为 evidence REVIEW 与 authorization REVIEW；否则必须使用独立 authorization REVIEW。

---

## 8. T4、T5、T6 合同

### 8.1 T4 `review → done`

必须在锁内重新验证：

- TASK 唯一位于 review；
- 当前 attempt 唯一；
- `report_ref` 是当前唯一有效 REPORT head；
- 最近 T3 event 确实绑定该 REPORT 及原始摘要；
- `review_ref` 是 `review_kind: acceptance`、`decision: approved`；
- acceptance REVIEW 的 subject/attempt/references 与当前 REPORT 匹配；
- authorization 完整、未过期、未被不同迁移消费且 Profile 返回 AUTHORIZED。

提交后仅追加一个 T4 event，事件必须持久记录：

```text
evidence_ref      = REPORT + acceptance REVIEW
evidence_digest   = 与引用等长、同顺序的完整字节 SHA-256
authorization_ref
authorization_digest
```

T4 不生成新 attempt。

### 8.2 T5 `review → active`

必须在锁内重新验证：

- 当前 REPORT 与最近 T3 绑定一致；
- `review_ref` 是 `review_kind: rejection`、`decision: rejected`；
- rejection REVIEW 引用被拒绝的当前 REPORT；
- authorization 绑定当前 source attempt 和 T5；
- Profile 返回 AUTHORIZED。

成功提交时必须生成全新、不可复用的 `attempt_id` 并写入 T5 event。旧 attempt 的 REPORT 永不满足新轮次 T3/T4/T5。

### 8.3 T6 `done → active`

必须使用 `review_kind: reopen` 或结构完整的 authorization REVIEW 作为所需 REVIEW，并通过独立或同一 Authorization 事实完成授权。成功提交时生成全新 attempt。

T6 不要求新增 REPORT，也不得重新采用旧 attempt REPORT。

### 8.4 明确保留 T7 阻断

T7 继续返回当前结构化未实现错误，不得出现部分 archive、部分 family 校验或“没有 Branch 就先支持”的特殊路径。

WP3C 的授权验证器可以设计为以后被 T7 复用，但不得在本轮实现 T7 行为、family digest、convergence 或 Branch 终态判断。

---

## 9. 原子性、轮次和恢复

T4/T5/T6 必须复用 WP3B 的三阶段 receipt：

```text
PREPARED → TARGET_DURABLE → COMMITTED
```

必须保持五状态恢复表不变，并满足：

1. source/target 不覆盖；
2. transition event 在目标 TASK 字节中一次提交；
3. Authorization REVIEW 不被修改；
4. authorization 消费事实与生命周期 event 是同一提交，不允许先消费后移动或先移动后另写消费表；
5. exact retry 返回已提交结果，不追加第二 event；
6. 不同 edge 复用相同授权稳定返回 `AUTHORIZATION_REUSED`；
7. T5/T6 receipt 必须明确记录 source attempt 与新 target attempt，不能用迁移后的 attempt 冒充授权绑定轮次；
8. 历史 T4/T5/T6 receipt 永久保留但不阻塞后续合法轮次；
9. 当前轮次出现互相冲突的 receipt 时 `RECOVERY_REQUIRED`；
10. target 可见但无法证明授权、证据或摘要一致时 Fail Closed；
11. 不按 mtime、目录顺序、文件名新旧或进程缓存选择收据；
12. 不新增公共 `operation_id` 承诺。

T4 与 T5 同时竞争同一 review TASK 时必须共享同一 family lock：最多一条边提交；失败方锁后重读并返回稳定错误。不得出现 done 与 active 双副本，也不得双重消费两份授权。

---

## 10. 允许和禁止的修改范围

### 10.1 允许修改

仅在确有必要时允许：

```text
src/fcop/project.py                    # 只允许可信 registry 初始化接线，不改 v3 签名
src/fcop/v4/creation.py                # 私有 v4 上下文和 REVIEW/handler 接线
src/fcop/v4/lifecycle.py               # T4/T5/T6 及现有事务复用
src/fcop/v4/receipts.py                # 仅授权迁移 receipt 身份/恢复所需
src/fcop/v4/linearization.py           # 仅现有 family 锁复用/锁顺序所需
src/fcop/v4/authorization.py           # 最多新增这一份私有生产模块

tests/test_fcop/test_v4_authorization.py
tests/test_fcop/test_v4_lifecycle.py
tests/conformance/v4/test_c3_lifecycle.py
tests/conformance/v4/test_c6_authorization.py
tests/conformance/v4/test_c8_recovery.py
tests/conformance/v4/fixtures.py       # 仅真实合同夹具缺陷，必须逐项报告

reports/FCOP-4.0-WP3C-*.md
reviews/fcop-4.0/wp3c/MANIFEST.md
```

若无需修改某文件，不得为了“整理架构”而修改。

### 10.2 禁止修改

```text
spec/fcop-4.0-spec.md
spec/fcop-4.0-spec.zh.md
schemas/**
src/fcop/errors.py
mcp/**
taskbooks/**
CodeFlowMu/**
```

同时禁止：

- 修改 31 个冻结 Base 错误码；
- 修改冻结 Test ID、删断言、skip、xfail、空 stub 或硬编码 PASS；
- 修改 v3 公共签名或 v3 生命周期语义；
- 新增公共 API；
- 新增 Runtime、SQLite、授权数据库、事件总线、缓存服务、队列、daemon、watcher、timer 或 scheduler；
- 新增运行时依赖；
- 实现 T7、family digest、convergence、Root archive 或 Branch terminal gate；
- 让 evaluator、Profile 规则或角色权限进入业务请求；
- 自动修复、删除或覆盖损坏证据；
- 合并 `main`、建 tag、建 Release、上传 PyPI；
- 修改 CodeFlowMu 或 `D:\FCoP` 原工作现场。

超出允许范围时停止请求 ADMIN，不得自行扩权。

---

## 11. 复杂度预算

为避免 FCoP 再次演变成 Runtime，本轮强制：

```yaml
NEW_PUBLIC_APIS: 0
NEW_RUNTIME_DEPENDENCIES: 0
NEW_BACKGROUND_COMPONENTS: 0
NEW_AUTHORITATIVE_STORES: 0
NEW_STATE_MACHINES: 0
NEW_PRODUCTION_MODULES_MAX: 1
AUTHORIZED_NEW_MODULE: src/fcop/v4/authorization.py
```

设计必须优先使用纯函数验证、现有四类文件、现有 transition event、现有 receipt 和现有 family lock。

禁止为 WP3D 预建抽象框架。若 `authorization.py` 不需要，则不创建；若实现需要第二个新生产模块，必须停止并提交复杂度说明。

---

## 12. 强制测试场景

### 12.1 Profile 信任边界

至少覆盖：

1. manifest 已采用且初始化 registry 存在，AUTHORIZED 通过；
2. DENIED 与 UNKNOWN 均拒绝且零写入；
3. registry 缺失、Profile 未采用、Profile ID 不匹配；
4. evaluator 返回未知值、抛异常或不可调用时 Fail Closed；
5. 初始化后修改调用方原 registry，不得替换已绑定 evaluator；
6. 请求夹带 evaluator/resolver/registry/caller judge/Host allowlist 全部拒绝；
7. `actor=ADMIN` 或 REVIEW `sender=ADMIN` 不能单独授权；
8. evaluator 只接收持久 REVIEW 中的 issuer/proof，不接收调用者伪造值；
9. 空 `profiles: []` 下 T1–T3 仍可执行，T4/T5/T6 返回 `AUTHORIZATION_PROFILE_UNAVAILABLE`。

### 12.2 Authorization 绑定与消费

至少覆盖：

1. subject、edge、attempt、profile、scope、decision、review kind 分别错误；
2. authorization 缺失与过期；
3. Authorization REVIEW 任一字节在验证前改变；
4. REPORT/acceptance/rejection/reopen REVIEW 任一字节改变；
5. 同一 authorization 精确响应丢失重试返回 Existing；
6. 同一 authorization 用于不同 edge 返回 `AUTHORIZATION_REUSED`；
7. 同一 REVIEW 同时作为 evidence 与 authorization 时，两个摘要字段均正确；
8. 独立 evidence REVIEW + authorization REVIEW 时，两者分别验证；
9. failed/denied/unknown/expired 请求不产生 receipt、target、event 或消费痕迹。

### 12.3 T4/T5/T6

至少覆盖：

1. T4 正常提交，REPORT、acceptance REVIEW、authorization 全部入 event；
2. T4 REPORT 不是 T3 已绑定 head 时拒绝；
3. T5 正常提交并生成新 attempt；
4. T5 后旧 attempt REPORT 不能满足新门；
5. T6 正常提交并生成新 attempt；
6. T6 不错误要求新 REPORT；
7. T4/T5/T6 tool、source、target 任一不匹配时拒绝；
8. T4 与 T5 并发最多一个成功，NOW 仍唯一；
9. T5/T6 多轮运行时历史 receipt 不阻塞当前轮；
10. T4/T5/T6 各自 PREPARED、TARGET_DURABLE、COMMITTED 和 RESPONSE_LOST 恢复；
11. source/target 不同摘要、收据损坏和多路径 NOW 保留证据并 Fail Closed；
12. T7 仍未实现且不产生任何写入。

### 12.4 回归

必须继续通过：

- WP3A、WP3A.1 创建面测试；
- WP3B、WP3B.1 全部生命周期与轮次测试；
- v3 全量回归；
- MCP 3.x 回归；
- v4 static/meta；
- 冻结 Test ID `60/60` 不变；
- 任务书开始点已有通过节点不得回退。

---

## 13. Conformance 目标与防伪

编码前必须先运行 `--collect-only` 并形成 WP3C 节点清单。至少包括语义上属于以下范围的参数化节点：

```text
C3-N02
C3-GATE-01[T4]
C3-GATE-01[T5]
C3-GATE-01[T6]

C6-N01
C6-R01 中基于 T4/T5/T6 可验证的节点
C6-R02 中 T6 expiry/reuse 节点
C6-PROFILE-01
C6-DIGEST-01
WP2.1b 的 Profile evaluator 与 caller-smuggling 节点

C8-RETRY-01[T4]
C8-RETRY-01[T5]
C8-RETRY-01[T6]
```

测试文件中混有 T7 的 Test ID 时，只允许本阶段对应的 T4/T5/T6 参数节点转绿；不得为了追求整文件全绿而实现 T7。

实现前报告必须记录：

```text
WP3C_TARGET_NODE_IDS
BASELINE_PASS
BASELINE_EXPECTED_FAIL
BASELINE_UNEXPECTED_FAIL
```

实现后要求：

```text
WP3C_TARGETS: 100% PASS
WP3B_REGRESSION: PASS
UNEXPECTED_FAILURES: 0
FROZEN_TEST_IDS: 60/60
```

其余仍失败节点必须逐项映射到未授权的 T7、convergence/family、公共恢复、MCP/Schema 或后续阶段能力。不能笼统写“expected deferred”。

不得通过 driver 拦截冒充生产拒绝；信任边界、授权裁决、迁移、响应丢失和复用测试必须实际调用 `Project` 生产接口。

---

## 14. 验证顺序

至少依次执行并保存完整命令和结果：

1. WP3C 新增定向单元测试；
2. `tests/test_fcop/test_v4_lifecycle.py`；
3. `tests/test_fcop/test_v4_creation.py`；
4. C3/C6/C8 定向 Conformance；
5. 全部 v4 static/meta/behavioral；
6. `tests/test_fcop` 全量；
7. 正确 `PYTHONPATH` 下 v3 全量回归；
8. `mcp` 正确隔离环境回归；
9. type check、格式和 `git diff --check`；
10. 冻结文件、允许文件和依赖差异检查；
11. 独立临时工作区 smoke：T1→T2→REPORT→T3→T4，以及 T5/T6 新轮次；
12. Windows 原生文件系统并发与 response-loss 测试。

不得把仅在错误 `PYTHONPATH`、全局安装包或缓存环境中的结果声明为通过。Linux/macOS 未实际运行时，只能如实写未验证。

仓库已有 Ruff 基线问题必须与本轮新增问题分开；本轮不得增加新的 lint 问题，也不得借机全仓格式化。

---

## 15. 交付文件

### 15.1 Content Commit

至少包含：

```text
reports/FCOP-4.0-WP3C-AUTHORIZATION-MODEL.md
reports/FCOP-4.0-WP3C-IMPLEMENTATION-PLAN.md
reports/FCOP-4.0-WP3C-ATOMICITY-AND-RETRY-PROOF.md
reports/FCOP-4.0-WP3C-CONFORMANCE-ALIGNMENT.md
reports/FCOP-4.0-WP3C-RESULT.md
```

以及实际授权范围内修改的源码和测试。

Content Commit 不得包含 Manifest。

### 15.2 Manifest Commit

第二个提交只允许新增：

```text
reviews/fcop-4.0/wp3c/MANIFEST.md
```

Manifest 必须记录：

- Repository、Taskbook path/branch/commit/SHA-256；
- Code baseline 与 Frozen Contract Commit；
- `WP3B_LIFECYCLE_ACCEPTED: true`；
- Content Commit 与 Manifest Commit；
- 精确文件清单和每个交付文件 SHA-256；
- 远端 refetch 后 HEAD 与哈希复核；
- WP3C target node 清单和结果；
- v3、MCP、v4 static/meta/behavioral 测试结果；
- 仍 deferred 节点逐项原因；
- 复杂度预算实测；
- 冻结文件、Schema、MCP、CodeFlowMu、main 未修改；
- `WP3D_AUTHORIZED: false`；
- `MAIN_MERGE_AUTHORIZED: false`；
- `RELEASE_AUTHORIZED: false`；
- `REQUESTED_GATE: WP3C_AUTHORIZATION_ACCEPTED`。

---

## 16. GitHub 两提交交付

实现 review 分支必须从 Taskbook Commit 创建：

```text
review/fcop-4.0-wp3c-authorization-transitions
```

交付结构固定：

```text
Taskbook Commit
  → Content Commit
  → Manifest Commit
```

推送后必须重新 fetch 远端，并验证：

1. 远端 HEAD 等于 Manifest Commit；
2. Content Commit 是 Manifest Commit 的直接父提交；
3. Taskbook Commit 是 Content Commit 的直接父提交；
4. Taskbook Commit 与 Content Commit 之间没有额外提交；
5. Content Commit 不修改 `taskbooks/**`；
6. Manifest Commit 只修改一个 Manifest 文件；
7. 从 GitHub 固定提交重新读取每个交付文件；
8. 重新计算的 SHA-256 与 Manifest 全部一致；
9. `main` 未改变。

不 force push，不创建 Release，不自动开合并 PR，不删除历史 review 分支。

---

## 17. 停止条件

遇到以下任一情况必须停止：

```text
TASKBOOK_IDENTITY_MISMATCH
BASELINE_MISMATCH
FROZEN_CONTRACT_MISMATCH
DIRTY_PRESERVED
WP3C_IMPLEMENTABILITY_GAP
FROZEN_CONFORMANCE_CONTRACT_CONFLICT
AUTHORIZATION_TRUST_BOUNDARY_GAP
RECEIPT_ROUND_IDENTITY_GAP
UNAUTHORIZED_FILE_REQUIRED
NEW_RUNTIME_DEPENDENCY_REQUIRED
SECOND_AUTHORITATIVE_STORE_REQUIRED
T7_OR_CONVERGENCE_REQUIRED
UNEXPECTED_V3_REGRESSION
UNEXPECTED_MCP_REGRESSION
REMOTE_DELIVERY_VERIFICATION_FAILED
```

停止时应提交阻断报告；不得通过扩大范围、修改规范、跳过测试或继续下一阶段绕过。

---

## 18. 最终回执格式

```yaml
WP3C_STATUS: COMPLETE | BLOCKED
AUTHORIZED_SCOPE: WP3C_ONLY
TASKBOOK_PATH: taskbooks/fcop-4.0/WP3C/01-Authorization-and-Controlled-Transitions-Taskbook.zh.md
TASKBOOK_COMMIT: <sha>
TASKBOOK_SHA256: <sha256>
INPUT_HEAD: 511039db227a23ae3e2d79aaae775a92ba392f5c
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
WORKTREE: D:\FCoP-wp3c-authorization
BRANCH: review/fcop-4.0-wp3c-authorization-transitions

TRUSTED_PROFILE_INITIALIZATION: PASS | FAIL
CALLER_AUTHORITY_SMUGGLING: REJECTED | FAIL
AUTHORIZATION_BINDING: PASS | FAIL
AUTHORIZATION_SINGLE_USE: PASS | FAIL
AUTHORIZATION_EXACT_RETRY: PASS | FAIL
T4_STATUS: COMPLETE | BLOCKED
T5_STATUS: COMPLETE | BLOCKED
T6_STATUS: COMPLETE | BLOCKED
T7_STATUS: NOT_AUTHORIZED

WP3C_TARGET_NODES: <n>/<n>
WP3C_NEW_TESTS: <n>/<n>
WP3B_REGRESSION: PASS | FAIL
FROZEN_TEST_IDS: 60/60
TEST_FCOP: <result>
V3_REGRESSION: <result>
MCP_REGRESSION: <result>
V4_STATIC_META: <result>
V4_BEHAVIORAL: <passed/deferred/unexpected>
UNEXPECTED_FAILURES: <n>

NEW_PUBLIC_APIS: 0
NEW_RUNTIME_DEPENDENCIES: 0
NEW_BACKGROUND_COMPONENTS: 0
NEW_AUTHORITATIVE_STORES: 0
NEW_STATE_MACHINES: 0
NEW_PRODUCTION_MODULES: 0 | 1
FROZEN_SPEC_FILES_MODIFIED: 0
SCHEMA_FILES_MODIFIED: 0
MCP_IMPLEMENTATION_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0

CONTENT_COMMIT: <sha>
MANIFEST_COMMIT: <sha>
REMOTE_HEAD: <sha>
REMOTE_PUSHED: true | false
REMOTE_REFETCH_VERIFIED: PASS | FAIL
DELIVERY_SHA256: <matched>/<total>
COMMIT_REACHABILITY: REMOTE_REVIEW_BRANCH | LOCAL_ONLY

WP3C_AUTHORIZATION_ACCEPTED: false
WP3D_STARTED: false
MAIN_MODIFIED: false
RELEASE_CREATED: false
REQUESTED_GATE: WP3C_AUTHORIZATION_ACCEPTED
```

完成后立即停止。只有 ADMIN 审核 GitHub 固定 review HEAD 并签署 `WP3C_AUTHORIZATION_ACCEPTED`，才能另立 WP3D 任务书。
