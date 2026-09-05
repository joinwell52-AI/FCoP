---
title: FCoP 4.0 WP3D Branch显式收敛、Family Digest与T7重新授权任务书 v1.1
document_role: EXECUTION_TASKBOOK
status: AUTHORIZED_FOR_WP3D_ONLY
execution_authorized: true
authorized_scope: WP3D_ONLY
input_head: dd8c39a2e025cc60f37d443abbe0988cbddf1810
accepted_review_head: 685835f5d22b327fd92121fce46941327368095c
frozen_contract_commit: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
accepted_gate: WP3D_FIXTURE_ALIGNMENT_ACCEPTED
supersedes_taskbook_commit: e664fa39592b699637c1f0e6aeee229331b321e3
fixture_alignment_head: 685835f5d22b327fd92121fce46941327368095c
wp3d_convergence_accepted: false
wp3e_authorized: false
wp4_authorized: false
main_merge_authorized: false
release_authorized: false
requested_gate: WP3D_CONVERGENCE_ACCEPTED
---

# FCoP 4.0 WP3D Branch显式收敛、Family Digest与T7重新授权任务书 v1.1

## 0. 唯一执行授权

本文件是WP3D当前唯一具有执行授权的任务书，并明确取代提交 `e664fa39592b699637c1f0e6aeee229331b321e3` 中已因夹具冲突停止的旧任务书。旧任务书不得恢复执行。

Codex本轮只允许完成：

1. 计算冻结合同定义的canonical family digest；
2. 通过现有 `write_review()` 写入并验证 `review_kind: convergence` 的正式REVIEW；
3. 实现T7 `done → archive`；
4. 实现普通TASK、Branch TASK及“存在Branch的Root TASK”三类T7门；
5. 使Branch创建、重开、REPORT replacement、convergence写入与Root T7共用既有Root-family短线性化边界；
6. 复用已验收的Authorization、三阶段receipt、响应丢失重试和单一NOW路径；
7. 使本任务书列明的15个冻结行为节点转绿，并保持既有节点不回退；
8. 以GitHub review分支交付证据。

本轮不实现公共recovery/fault-injection、cold export、Schema、MCP、PyPI、规则包、Host适配或CodeFlowMu适配。

完成后必须停止并请求：

```text
GATE: WP3D_CONVERGENCE_ACCEPTED
```

执行者不得自行签署Gate，不得进入WP3E/WP4，不得修改main或发布。

---

## 0.1 WP3D.0修正已经纳入

新的执行基线已经包含：

- `C3-GATE-01[T7]` 与T4/T5/T6一样使用局部可信Profile driver；
- `C5-N02` 使用局部 `DeterministicProfileEvaluator("AUTHORIZED")` driver；
- `C5-ARCHIVED-01` 使用同类局部driver；
- 默认 `v4_driver`、全局fixtures和负向Profile测试保持不变；
- WP3D阻断报告已经进入GitHub；
- Gate `WP3D_FIXTURE_ALIGNMENT_ACCEPTED` 已签署。

实现者不得撤销、泛化或绕过这些修正，也不得再次修改冻结Conformance文件。三个节点当前仍为红灯的唯一合法原因是T7/family digest尚未实现。

## 1. 固定输入与已签Gate

```yaml
REPOSITORY: joinwell52-AI/FCoP
INPUT_HEAD: dd8c39a2e025cc60f37d443abbe0988cbddf1810
ACCEPTED_REVIEW_HEAD: 685835f5d22b327fd92121fce46941327368095c
FIXTURE_ALIGNMENT_GATE_COMMIT: dd8c39a2e025cc60f37d443abbe0988cbddf1810
SUPERSEDED_TASKBOOK_COMMIT: e664fa39592b699637c1f0e6aeee229331b321e3
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
GATE_RECEIPT: reviews/fcop-4.0/gates/WP3D-FIXTURE-ALIGNMENT-ACCEPTED.md
GATE: WP3D_FIXTURE_ALIGNMENT_ACCEPTED
GATE_DECISION: ACCEPTED
TASKBOOK_BRANCH: task/fcop-4.0-wp3d-convergence-t7-v1.1
EXPECTED_REVIEW_BRANCH: review/fcop-4.0-wp3d-convergence-t7-v1.1
```

INPUT_HEAD包含WP3C.2验收链及ADMIN Gate回执。WP3D必须从包含本任务书的Taskbook Commit顺序接出，不能从main、旧WP3C分支或本地 `D:\FCoP` 猜测起点。

已验收且不得回退：

- WP3A/WP3A.1工作区与四类信封创建面；
- WP3B/WP3B.1的T2/T3、当前执行轮次、REPORT head、文件事务、三阶段receipt与五状态恢复；
- WP3C/WP3C.1的可信Profile边界、Authorization绑定、过期复查、single-use与exact retry；
- WP3C.2的T6冻结夹具对齐；
- 60/60冻结Test ID及其断言意图。

## 2. 权威顺序

### 2.1 事实判断

```text
冻结合同 aec4c2b2…
> accepted review head c08d6059… 的真实代码
> 冻结Conformance Test ID与测试意图
> 已签Gate 9f72dc0…
> 本任务书
> 其他报告、路线图与历史材料
```

### 2.2 执行授权

```text
ADMIN Gate WP3C_AUTHORIZATION_ACCEPTED
> 本GitHub固定任务书
> taskbooks/README.zh.md
> 其他计划或说明
```

ADMIN Gate能授权进入下一阶段，但不能改变代码事实或冻结合同。任何无法在本任务范围闭合的冲突必须停止报告。

## 3. GitHub身份与隔离工作区

开始前必须：

1. fetch远端taskbook分支；
2. 从GitHub读取本任务书，不以聊天复制文本或本地旧副本为权威；
3. 固定Taskbook Commit并计算本文件SHA-256；
4. 验证Taskbook Commit祖先包含INPUT_HEAD；
5. 验证INPUT_HEAD到Taskbook Commit只新增本任务书；
6. 验证Gate回执decision为ACCEPTED；
7. 验证冻结中英文规范与FROZEN_CONTRACT_COMMIT一致；
8. 从Taskbook Commit创建独立review分支和worktree。

建议：

```text
WORKTREE: D:\FCoP-wp3d-convergence-t7
BRANCH: review/fcop-4.0-wp3d-convergence-t7-v1.1
```

不得修改 `D:\FCoP` 原工作现场、其他worktree或CodeFlowMu。原工作树脏时必须新建独立worktree；不能安全隔离则停止为 `DIRTY_PRESERVED`。中文Markdown统一UTF-8、LF；不得使用PowerShell修改中文文件。

## 4. 当前真实代码边界

编码前必须重新复核，并在实施计划中引用具体文件与符号：

1. `src/fcop/v4/lifecycle.py` 已实现T2–T6，T7仍返回结构化未实现错误；
2. `src/fcop/v4/linearization.py` 已提供按workspace/root_task_id确定的Root-family短锁；
3. Branch create、REPORT写入和生命周期迁移已使用该family边界；
4. `write_review()` 目前是通用追加写入，尚未为convergence执行family快照验证；
5. `Project` 尚无公共 `family_digest` 或等价生产入口；
6. Conformance driver对family digest只解析 `Project.family_digest` 或 `compute_family_digest`；
7. `src/fcop/v4/boundary.py` 对Project公共方法实行闭集策略，新增公共方法必须显式分类；
8. 现有Authorization与receipt必须扩展复用，禁止复制第二套T7事务；
9. 当前行为基线为54 passed / 38 deferred；本轮目标是其中15个T7/收敛节点，不包括公共恢复和cold export。

如果实际代码与以上不一致，先记录差异；不得机械照任务书实现。

## 5. 编码前必须提交的证明

在修改生产代码前生成：

```text
reports/FCOP-4.0-WP3D-FAMILY-MODEL.md
reports/FCOP-4.0-WP3D-IMPLEMENTATION-PLAN.md
reports/FCOP-4.0-WP3D-TARGET-NODE-BASELINE.md
```

至少证明：

1. Root、Branch及普通TASK如何仅从四类文件和路径识别；
2. 全部Branch如何跨五个生命周期目录确定，为什么不需要索引或数据库；
3. 每个Branch当前attempt如何由最后一次合法active-entry transition确定；
4. 每个Branch唯一当前REPORT head如何解析，replacement链如何处理；
5. canonical JSON字节和SHA-256如何独立于mtime、目录枚举顺序及done/archive路径；
6. convergence REVIEW如何在family锁内验证并追加，避免与REPORT replacement形成混合快照；
7. Root T7如何在同一family锁内重算全部门，不信任调用者提供的digest；
8. 三类T7如何走同一Lifecycle入口而使用不同证据门；
9. T7怎样复用现有Authorization evaluator、single-use检查、过期复查和receipt；
10. response loss后的exact retry怎样返回Existing且不追加第二个T7 event；
11. Branch create/reopen/report replacement/convergence写入/Root T7的锁顺序如何唯一；
12. 允许修改文件与复杂度预算为何足够。

无法证明时停止：`WP3D_IMPLEMENTABILITY_GAP`。

## 6. Canonical family digest合同

### 6.1 唯一允许的新公共读取入口

本轮只授权一个新公共API：

```python
Project.family_digest(*, root_task_id: str) -> str
```

返回值必须是64位小写SHA-256字符串。不得同时增加 `list_branches`、`compute_family_digest`、`family_snapshot`、索引查询或第二个等价公共入口。该方法必须进入现有Project v4边界策略，普通v3工作区行为和签名不变。

### 6.2 Canonical对象

必须严格按冻结F4.6.6构造：

```json
{"contract":"fcop-family-v1","root_task_id":"<ROOT>","branches":[{"branch_task_id":"<BRANCH>","attempt_id":"<CURRENT_ATTEMPT>","report_id":"<CURRENT_REPORT_HEAD>","report_digest":"<SHA256_OF_EXACT_REPORT_BYTES>"}]}
```

要求：

- branches按 `branch_task_id` Unicode code point升序；
- 对象键递归排序；
- UTF-8，无BOM、无换行、无多余空格；
- 摘要为完整canonical字节的SHA-256小写十六进制；
- Branch的done/archive路径、mtime和目录枚举顺序不进入摘要；
- Root本身及Root REPORT不进入branches数组；
- Branch缺当前attempt、缺REPORT、REPORT head歧义、摘要不符或关系损坏时Fail Closed；
- 计算过程只读，不创建缓存、索引、receipt或隐藏状态。

canonical构造与摘要算法只能有一份生产实现。convergence写入、Root T7及公共 `family_digest()` 必须调用同一纯函数/私有组件。

## 7. Convergence REVIEW合同

Convergence仍是REVIEW，不得新增第五类文件或数据库记录。必须复用 `Project.write_review(...)`；当且仅当 `review_kind == "convergence"` 时进入专用family验证路径，其他REVIEW语义不得改变。

convergence REVIEW至少满足：

```yaml
type: REVIEW
review_kind: convergence
subject_ref: <ROOT_TASK_ID>
decision: approved
family_digest: <canonical digest>
references:
  - <each current Branch REPORT head>
```

规则：

1. subject必须是当前唯一Root TASK，且至少存在一个Branch；
2. 在Root-family锁内重新枚举全部当前Branch；
3. 每个Branch必须处于done或archive，并有当前attempt与唯一当前REPORT head；
4. references必须恰好覆盖每个Branch当前REPORT head；
5. 可额外引用Root当前REPORT head；不得引用其他TASK、旧attempt或被替换REPORT；
6. family_digest必须等于锁内生产端重算值；
7. REVIEW以append-only新文件提交，不改写旧REVIEW；
8. REVIEW与REPORT replacement并发时只能形成两个完整次序，不能形成混合快照；
9. 旧convergence保留为历史证据，但Root T7只能使用与当前family匹配的明确REVIEW；
10. 调用者的references和digest只是待验证声明，不是事实源。

不得新增 `write_convergence()` 公共API。

## 8. T7 `done → archive`合同

### 8.1 三类TASK

| 类型 | 必须满足 | 不要求 |
|---|---|---|
| 普通TASK | 唯一done路径、当前attempt、有效T7 Authorization | convergence与family_digest |
| Branch TASK | 上述条件；锁键归属Root family | convergence与family_digest |
| 存在Branch的Root TASK | 全部Branch终态、当前REPORT heads、有效convergence、匹配family_digest、绑定同一digest的T7 Authorization | 新attempt |

T7成功后不生成新attempt，archive为终态。

### 8.2 Branch终态门

存在Branch的Root提交T7前，锁内必须验证：

- 每一个当前Branch都在done或archive；
- 每个Branch当前轮次已通过T3或T4形成可审计完成证据；
- 每个Branch存在唯一当前REPORT head；
- active、inbox或review Branch返回 `BRANCH_NOT_TERMINAL`；
- Root在锁后看到的全部Branch都必须被覆盖，不能由调用者声明参与者。

Branch从done归档到archive不改变family digest；Branch重开产生新attempt、Branch新增或REPORT replacement都会使旧convergence失效。

### 8.3 Root T7验证

有Branch的Root T7必须在同一family锁内重新验证：

1. Root仍唯一位于done；
2. family成员集合完整；
3. Branch终态门通过；
4. 当前attempt及REPORT heads唯一；
5. 生产端重算canonical family digest；
6. `review_ref` 指向有效convergence REVIEW；
7. convergence references与当前family完全匹配；
8. 请求 `family_digest` 与生产重算值一致；
9. T7 Authorization绑定Root、done→archive、source attempt与相同family_digest；
10. trusted Profile返回AUTHORIZED；
11. Authorization在最终提交前再次检查未过期；
12. receipt/evidence/authorization摘要完整后才提交文件迁移。

缺convergence返回 `FAMILY_CONVERGENCE_REQUIRED`；旧或不完整convergence、错误references或digest返回 `FAMILY_CONVERGENCE_MISMATCH`；Branch未终态优先返回 `BRANCH_NOT_TERMINAL`。Authorization相关错误沿用WP3C优先级。编码前须形成完整错误优先级表，禁止新增Base错误码。

### 8.4 T7 event

Root带Branch成功T7时，最后一个transition event必须持久化：

- source attempt与 `family_digest`；
- `authorization_ref`及完整字节 `authorization_digest`；
- `evidence_ref`至少含convergence REVIEW及按Branch ID排序的全部当前REPORT；
- 与 `evidence_ref` 同顺序、等长的 `evidence_digest`；
- 如convergence合法引用Root当前REPORT，则一并持久化；
- 不新增第二个event或外部消费记录。

普通TASK与Branch T7不得伪造family digest或convergence evidence。

## 9. 原子性、竞态与重试

所有family变更必须复用同一个Root-family短锁：Branch create、Branch T5/T6重开、Branch REPORT初写与replacement、convergence REVIEW写入、Branch T7、Root T7。禁止第二种锁目录、第二个锁实现或后台协调器。

必须证明以下竞态只有完整先后顺序：

1. Root T7 vs Branch create；
2. Root T7 vs Branch T6重开；
3. Root T7 vs Branch REPORT replacement；
4. convergence write vs REPORT replacement；
5. Root T7 vs convergence write；
6. Branch T7 vs Root T7；
7. 两次Root T7 exact retry；
8. Root T7授权复用到不同edge。

Root已archive后不得新建/重开/改写其Branch family；Root T7失败时不得移动Root、写event、产生消费痕迹或半成品convergence。

T7必须复用 `PREPARED → TARGET_DURABLE → COMMITTED` 及既有五状态恢复。receipt identity至少绑定subject、edge、source attempt、授权摘要、证据摘要；有Branch的Root还必须绑定family digest和convergence摘要。

响应在durable commit后丢失时，完全相同请求返回Existing；当前family或证据不同不能被旧receipt误判为Existing。历史receipt保留，不阻塞后续合法轮次。本轮不新增公共 `recover_operation`、`inject_fault` 或 `operation_id` 承诺。

## 10. 精确Conformance目标

开始前必须用 `--collect-only` 锁定参数化节点名称。语义目标固定为以下15个节点：

| # | 节点 |
|---:|---|
| 1 | C3-N01 |
| 2 | C3-GATE-01[T7] |
| 3 | C5-N02 |
| 4 | C5-R03 |
| 5 | C5-X01 |
| 6 | C5-BRANCH-01 |
| 7 | C5-ARCHIVED-01 |
| 8 | C5-FAMILY-DIGEST-01 |
| 9 | C5-REPORT-RACE-01 |
| 10 | C6-R01[missing] 的T7节点 |
| 11 | C6-R01[actor-admin-only] 的T7节点 |
| 12 | C6-R01[wrong-subject] 的T7节点 |
| 13 | C6-R01[wrong-edge] 的T7节点 |
| 14 | C6-R01[wrong-attempt] 的T7节点 |
| 15 | C8-RETRY-01[T7] |

pytest node id文本如略有不同，必须在baseline报告中给出真实完整node id及语义映射，不得扩大范围。

同时保持 C5-FAMILY-RACE-01、C8-X02、AT-02、C6-SPOOF-01及WP3A至WP3C.2全部已通过节点继续通过。

按当前119个v4节点计算，15个目标转绿且无回退时预期：

```yaml
V4_STATIC_META: 27 passed
V4_BEHAVIORAL: 69 passed / 23 deferred
V4_TOTAL: 96 passed / 23 deferred
UNEXPECTED_FAILURES: 0
```

实际收集数若因合法新增测试不同必须如实报告；冻结Test ID仍为60/60。

仍defer：C3-X01 cold export、C4-R01 dangling gate reference、C6-X01公共fault路径、C7-CREATE-01、C8公共recovery/fault状态节点、AT-05、AT-06及WP3E后续能力。不得为追求整文件全绿越界。

## 11. 允许修改范围与复杂度预算

### 11.1 允许的生产文件

```text
src/fcop/project.py
src/fcop/v4/boundary.py
src/fcop/v4/creation.py
src/fcop/v4/lifecycle.py
src/fcop/v4/authorization.py
src/fcop/v4/receipts.py
src/fcop/v4/linearization.py
src/fcop/v4/convergence.py
```

约束：

- `project.py` 只增加 `family_digest(*, root_task_id)` v4读取入口；
- `boundary.py` 只将该入口纳入既有闭集策略；
- `creation.py` 只接线同一convergence实现并验证convergence REVIEW；
- `lifecycle.py` 只实现T7与共享family验证接线；
- `authorization.py` 只扩展T7/family绑定；
- `receipts.py` 只扩展T7 identity与exact retry；
- `linearization.py` 只复用/修正既有family锁；
- `convergence.py` 是本轮唯一允许的新生产模块，只容纳纯family扫描、head解析、canonical digest与convergence验证。

允许的测试与报告：

```text
tests/test_fcop/test_v4_convergence.py
tests/test_fcop/test_v4_lifecycle.py
tests/test_fcop/test_v4_authorization.py
tests/test_fcop/test_v4_creation.py
reports/FCOP-4.0-WP3D-*.md
reviews/fcop-4.0/wp3d/MANIFEST.md
```

冻结 `tests/conformance/v4/**` 原则上只读。若证明夹具与冻结规范冲突，必须停止请求单独修订授权。

### 11.2 复杂度预算

```yaml
NEW_PUBLIC_APIS_MAX: 1
AUTHORIZED_PUBLIC_API: Project.family_digest
NEW_PRODUCTION_MODULES_MAX: 1
AUTHORIZED_NEW_MODULE: src/fcop/v4/convergence.py
NEW_RUNTIME_DEPENDENCIES: 0
NEW_BACKGROUND_COMPONENTS: 0
NEW_AUTHORITATIVE_STORES: 0
NEW_STATE_MACHINES: 0
NEW_LOCK_SYSTEMS: 0
NEW_BASE_ERROR_CODES: 0
```

需要第二个新公共API、第二个新模块、数据库、索引、cache、daemon、watcher、timer、scheduler或外部依赖时，必须停止。

## 12. 明确禁止

禁止：

- 修改冻结中英文规范、Schema、31个Base错误码或冻结Test ID；
- 修改MCP、PyPI、发布、规则包、Host adapter或CodeFlowMu；
- 新增 `write_convergence`、`list_branches`、公共recovery/fault API；
- 复制第二套生命周期、摘要、授权、receipt或锁；
- 以mtime、枚举顺序、缓存或调用者branch清单决定family；
- 原地修改REPORT/REVIEW或自动删除冲突证据；
- skip、xfail、空stub、测试内生产实现或硬编码Test ID；
- 修改main、建tag/Release、上传PyPI；
- 进入WP3E/WP4。

## 13. 强制单元与并发测试

### 13.1 Digest与family

至少覆盖：创建顺序、mtime、Branch done/archive路径不改变digest；REPORT replacement和新attempt改变family事实；缺/歧义/旧attempt REPORT及损坏关系Fail Closed；Root不存在、subject为Branch、重复TASK路径Fail Closed；canonical bytes与独立oracle一致。

### 13.2 Convergence

至少覆盖：完整references成功；缺、多、旧、重复reference拒绝；Root无Branch和Branch未终态拒绝；append-only；replacement后旧REVIEW保留但Root T7拒绝；并发replacement/convergence无混合快照。

### 13.3 T7

至少覆盖：普通TASK、Branch、有Branch Root三种成功；Branch非终态；缺/旧convergence；错误digest；Authorization subject/edge/attempt/family错误；DENIED/UNKNOWN/expired/issuer proof错误零写入；event refs/digests正确；archive终态；response-loss exact retry；Authorization不同请求复用；既有三阶段恢复不回退。

### 13.4 多进程线性化

必须使用真实生产接口和Windows spawn多进程，不以sleep作判定。覆盖第9节八项竞态，证明NOW唯一、Root archive后无新Branch、旧convergence不能批准新family、无双消费、loser返回冻结错误、无混合event或部分receipt。

## 14. 验证顺序

保存完整命令与结果：

1. 编码前collect-only及15节点基线；
2. WP3D新增单元测试；
3. 全部 `tests/test_fcop/test_v4_*.py`；
4. C3/C5/C6/C8/AT定向Conformance；
5. 全部v4 static/meta与behavioral；
6. `tests/test_fcop`全量；
7. 正确 `PYTHONPATH` 下v3全量回归；
8. 隔离MCP 3.x回归；
9. type check、格式、lint差异与 `git diff --check`；
10. 冻结文件、allowlist、依赖和公共API差异检查；
11. 独立工作区smoke：普通全生命周期、两Branch显式收敛Root T7、Branch归档digest不变；
12. Windows原生多进程竞态与response-loss；
13. 远端固定提交回读及SHA-256。

Linux/macOS未原生运行只能报告未验证。既有Ruff问题与本轮新增问题分开，不得借机全仓格式化。

## 15. 交付文件

Content Commit至少包含：

```text
reports/FCOP-4.0-WP3D-FAMILY-MODEL.md
reports/FCOP-4.0-WP3D-IMPLEMENTATION-PLAN.md
reports/FCOP-4.0-WP3D-TARGET-NODE-BASELINE.md
reports/FCOP-4.0-WP3D-ATOMICITY-AND-RACE-PROOF.md
reports/FCOP-4.0-WP3D-CONFORMANCE-ALIGNMENT.md
reports/FCOP-4.0-WP3D-RESULT.md
```

以及授权范围内源码和测试。Content Commit不得包含Manifest或任务书修改。

Manifest Commit只允许新增：

```text
reviews/fcop-4.0/wp3d/MANIFEST.md
```

Manifest记录Taskbook身份与SHA-256、INPUT_HEAD、accepted review head、Gate、冻结合同、交付文件SHA-256、15节点前后结果、deferred逐项映射、digest oracle/竞态/重试证据、v3/MCP/v4结果、复杂度与公共API差异、未修改范围及请求Gate。

## 16. GitHub两提交交付

review分支从Taskbook Commit创建：

```text
review/fcop-4.0-wp3d-convergence-t7-v1.1
```

提交链固定：

```text
Taskbook Commit → Content Commit → Manifest Commit
```

推送后重新fetch验证remote HEAD、直接父链、Content不改taskbooks、Manifest只新增一个文件、全部远端SHA-256、worktree干净及remote main未变。不force push、不自动创建/合并PR、不删除历史review分支。

## 17. 停止条件

```text
TASKBOOK_IDENTITY_MISMATCH
BASELINE_MISMATCH
GATE_RECEIPT_MISMATCH
FROZEN_CONTRACT_MISMATCH
DIRTY_PRESERVED
WP3D_IMPLEMENTABILITY_GAP
FROZEN_CONFORMANCE_CONTRACT_CONFLICT
FAMILY_LINEARIZATION_GAP
CANONICAL_DIGEST_AMBIGUITY
REPORT_HEAD_AMBIGUITY_NOT_CLOSED
T7_RECEIPT_IDENTITY_GAP
UNAUTHORIZED_FILE_REQUIRED
SECOND_PUBLIC_API_REQUIRED
SECOND_PRODUCTION_MODULE_REQUIRED
NEW_RUNTIME_DEPENDENCY_REQUIRED
SECOND_AUTHORITATIVE_STORE_REQUIRED
UNEXPECTED_V3_REGRESSION
UNEXPECTED_MCP_REGRESSION
REMOTE_DELIVERY_VERIFICATION_FAILED
```

停止时提交阻断报告；不得扩大范围、修改规范或继续下一阶段绕过。

## 18. 最终回执格式

```yaml
WP3D_STATUS: COMPLETE | BLOCKED
AUTHORIZED_SCOPE: WP3D_ONLY
TASKBOOK_PATH: taskbooks/fcop-4.0/WP3D/02-Branch-Convergence-Family-Digest-and-T7-Restart-Taskbook-v1.1.zh.md
TASKBOOK_COMMIT: <sha>
TASKBOOK_SHA256: <sha256>
INPUT_HEAD: dd8c39a2e025cc60f37d443abbe0988cbddf1810
ACCEPTED_REVIEW_HEAD: 685835f5d22b327fd92121fce46941327368095c
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
GATE_RECEIPT: reviews/fcop-4.0/gates/WP3D-FIXTURE-ALIGNMENT-ACCEPTED.md
WORKTREE: D:\FCoP-wp3d-convergence-t7
BRANCH: review/fcop-4.0-wp3d-convergence-t7-v1.1

CANONICAL_FAMILY_DIGEST: PASS | FAIL
CONVERGENCE_REVIEW: PASS | FAIL
BRANCH_TERMINAL_GATE: PASS | FAIL
ORDINARY_T7: PASS | FAIL
BRANCH_T7: PASS | FAIL
ROOT_WITH_BRANCHES_T7: PASS | FAIL
T7_AUTHORIZATION_BINDING: PASS | FAIL
T7_EXACT_RETRY: PASS | FAIL
FAMILY_RACE_MATRIX: <passed>/<total>

WP3D_TARGET_NODES: 15/15
WP3D_NEW_TESTS: <passed>/<total>
WP3C_REGRESSION: PASS | FAIL
FROZEN_TEST_IDS: 60/60
TEST_FCOP: <result>
V3_REGRESSION: <result>
MCP_REGRESSION: <result>
V4_STATIC_META: <result>
V4_BEHAVIORAL: <passed/deferred/unexpected>
V4_TOTAL: <passed/deferred>
UNEXPECTED_FAILURES: <n>

NEW_PUBLIC_APIS: 1
NEW_PUBLIC_API: Project.family_digest
NEW_PRODUCTION_MODULES: 0 | 1
NEW_RUNTIME_DEPENDENCIES: 0
NEW_BACKGROUND_COMPONENTS: 0
NEW_AUTHORITATIVE_STORES: 0
NEW_STATE_MACHINES: 0
NEW_LOCK_SYSTEMS: 0
NEW_BASE_ERROR_CODES: 0
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

WP3D_CONVERGENCE_ACCEPTED: false
WP3E_STARTED: false
WP4_STARTED: false
MAIN_MODIFIED: false
RELEASE_CREATED: false
REQUESTED_GATE: WP3D_CONVERGENCE_ACCEPTED
```

完成后立即停止。只有ADMIN审核GitHub固定review HEAD并签署 `WP3D_CONVERGENCE_ACCEPTED`，才能另立WP3E任务书。
