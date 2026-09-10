# FCoP 4.0 WP1 · WP2 符合性合同矩阵

> 本文件只定义未来测试合同；`TEST_CODE_WRITTEN: 0`。

## 1. 规范/双语权威

| test_id | 场景 | 输入/动作 | 预期可观察结果 | 条款 |
|---|---|---|---|---|
| C0-PARITY-01 | 英中候选对等 | 提取条款 ID、T1–T7、C1–C8、错误代码 | 集合完全一致，否则 gate fail | F4.0.2 |
| C0-AUTH-01 | Schema/规范冲突 | 构造 Schema 可接受但行为违规的迁移 | 行为拒绝且发布 gate fail；Schema 不覆盖行为规范 | F4.0.3, F4.12.3 |
| C0-ERROR-REGISTRY-01 | Base 错误注册表 | 提取英中 F4.10.1 并尝试用 Profile 错误重定义 Base | 两边集合严格相同且为 31；扩展重定义拒绝 | F4.10.1–F4.10.3 |

## 2. C1–C8 测试合同

| test_id | Core | 类型 | 场景 | 预期结果/错误 | 条款 |
|---|---|---|---|---|---|
| C1-N01 | C1 | 正常 | 创建 4.0 workspace，并写匹配 workspace_id 的 TASK | 声明可读，TASK 创建成功 | F4.2.1–F4.2.3 |
| C1-R01 | C1 | 拒绝 | envelope workspace_id 与 manifest 不同 | `WORKSPACE_ID_MISMATCH`，零写入 | F4.2.2 |
| C1-FORK-01 | C1 | 显式 fork | independent-fork/derive 创建可写派生工作区；另试强制保留 ID | 新 workspace_id 与源不同；强制保留时拒绝或明确只读 mirror | F4.2.4 |
| C1-OFFLINE-01 | C1 | 离线边界 | 单个离线 workspace 无网络/Registry，且未同时观察另一副本 | 不要求证明全球唯一、不伪报冲突；规范不承诺发现不可见副本 | F4.2.6 |
| C2-N01 | C2 | 正常 | 分别创建合法 TASK/REPORT/ISSUE/REVIEW | 四类均按共同/类型字段解码 | F4.3.1–F4.3.2 |
| C2-R01 | C2 | 拒绝 | 创建 EVAL 或缺 typed ID/subject_ref 的 envelope | `INVALID_ENVELOPE` | F4.3.1–F4.3.2 |
| C2-R02 | C2 | 追加性 | 尝试原地修改 REVIEW；再用新 REVIEW references 修正 | 原地修改拒绝；追加事实成功且旧 bytes 不变 | F4.3.3, F4.3.5 |
| C3-N01 | C3 | 正常 | T1→T2→T3→T4→T7 合法链 | 每次仅一边/一 event，最终 archive | F4.4.1–F4.4.3 |
| C3-N02 | C3 | 正常/reopen | done TASK 有授权执行 T6 | 进入 active，生成新 attempt | F4.4.2(T6), F4.6.1 |
| C3-R01 | C3 | 拒绝 | 从 inbox 单调用直达 archive | 非法边错误，仍在 inbox | F4.4.2–F4.4.3 |
| C3-R02 | C3 | 拒绝/Legacy | 4.0 workspace 调 `finish_task` | `LEGACY_TRANSITION_NOT_ALLOWED`，无 active→done | F4.4.4 |
| C3-R03 | C3 | 拒绝/Legacy | 将 archive 权威 TASK 移入 history | 拒绝；archive TASK 原位 | F4.4.6, F4.11.2 |
| C3-X01 | C3 | 恢复 | 冷存储导出中断 | 权威 archive 不变；残留导出无 NOW 权力 | F4.4.6, F4.9.4 |
| C3-GATE-01 | C3 | 参数化 Gate | 对 T1–T7 逐边提供/移除矩阵规定的 REPORT、REVIEW、Profile 与 attempt | 七边仅在完整前置成立时提交；非法边 `INVALID_TRANSITION`；Profile 可选政策不改变 Base 边 | F4.4.2, F4.4.7 |
| C4-N01 | C4 | 正常 | parent、subject_ref、references 指向合法对象 | 关系解析成功且所有权不被 references 改变 | F4.5.1–F4.5.2 |
| C4-N02 | C4 | 正常/Branch | active Root 创建两个 sibling Branch | 两 Branch 普通 TASK，branch_of 同 Root | F4.5.3–F4.5.4 |
| C4-R01 | C4 | 拒绝 | 强关系悬空/跨 workspace/循环；门控弱引用缺失 | `RELATION_INVALID` 或操作拒绝 | F4.5.2 |
| C4-R02 | C4 | 拒绝 | Branch 作为另一 Branch 的 branch_of target | `BRANCH_DEPTH_EXCEEDED` | F4.5.3 |
| C5-N01 | C5 | 正常 | current attempt 唯一 final REPORT 后 T3 | active→review 成功，event 引用该 REPORT | F4.6.1–F4.6.2 |
| C5-N02 | C5 | 正常/收敛 | Root 两 Branch 均完成，convergence 引用两个 current REPORT | family_digest 重算相同，T7 可继续 | F4.6.5–F4.6.8 |
| C5-R01 | C5 | 拒绝 | 无 REPORT 或同 attempt 两个 head 时 T3 | `REPORT_REQUIRED` 或 `REPORT_HEAD_AMBIGUOUS` | F4.3.4, F4.6.2 |
| C5-R02 | C5 | 拒绝/reopen | T5/T6 后用旧 attempt REPORT | `ATTEMPT_MISMATCH` | F4.6.1–F4.6.2 |
| C5-R03 | C5 | 拒绝/收敛 | convergence 少一个 Branch、引用旧 REPORT 或 digest 旧 | `FAMILY_CONVERGENCE_MISMATCH` | F4.6.6–F4.6.8 |
| C5-X01 | C5 | 并发 | convergence 后并发新增/reopen Branch 或 replacement REPORT | 旧 convergence 失效；Root archive 拒绝 | F4.6.8, F4.9.5 |
| C5-BRANCH-01 | C5 | Branch 终态门 | Root done；至少一个 Branch 在 active 或 review；调用 Root T7 | `BRANCH_NOT_TERMINAL`，Root 保持 done | F4.6.5 |
| C5-ARCHIVED-01 | C5 | Branch 路径变化 | 有效 convergence 后 Branch 执行已授权 done→archive，再调用 Root T7 | canonical family object/digest 不变；原 convergence 仍可匹配 | F4.6.6–F4.6.8 |
| C5-FAMILY-RACE-01 | C5 | family 竞态 | Root 离开 active 与 create Branch 同时竞争 | family 边界只允许一个先提交；后者锁后重读并稳定拒绝/重验 | F4.5.4, F4.9.5 |
| C5-REPORT-RACE-01 | C5 | family 竞态 | Branch REPORT replacement 与 convergence 创建同时竞争 | convergence 绑定替换前或替换后的唯一 head；不得提交混合快照 | F4.6.6–F4.6.8, F4.9.5 |
| C5-FAMILY-DIGEST-01 | C5 | 摘要算法 | 用乱序 Branch/对象键、不同目录遍历序和相同 UTF-8/LF REPORT bytes 计算 | 始终得到同一 `fcop-family-v1` lowercase SHA-256；mtime/状态不参与 | F4.6.6 |
| C6-N01 | C6 | 正常 | Profile 认可签发者追加绑定当前 transition/attempt 的 authorization REVIEW | transition 成功且 event 保存 authorization_ref | F4.7.1–F4.7.5 |
| C6-R01 | C6 | 拒绝 | 只有 actor=`ADMIN` 或授权 subject/edge/attempt 不匹配 | `AUTHORIZATION_REQUIRED`/`AUTHORIZATION_INVALID` | F4.7.3–F4.7.5 |
| C6-R02 | C6 | 拒绝 | 授权过期或 single-use 被第二 transition 使用 | `AUTHORIZATION_EXPIRED`/`AUTHORIZATION_REUSED` | F4.7.3 |
| C6-X01 | C6 | 响应丢失 | 已消费授权后响应丢失并以相同 ref/digest/transition 重试 | 返回既有提交结果，不产生第二消费 | F4.7.3, F4.9.11 |
| C6-PROFILE-01 | C6 | 空 Profile | `profiles: []` workspace 执行 T1–T3 后尝试 T4/T5/T6/T7 | T1–T3 按 Base 工作；授权迁移返回 `AUTHORIZATION_PROFILE_UNAVAILABLE` | F4.2.3, F4.7.4, F4.7.7 |
| C6-SPOOF-01 | C6 | 身份伪报 | 仅令 sender/actor=`ADMIN` 或 Host allowlist 命中，不提供 Profile 的 AUTHORIZED 证明 | `AUTHORIZATION_INVALID` 并 Fail Closed；不得消费或移动 | F4.7.4–F4.7.6 |
| C6-DIGEST-01 | C6 | 证据篡改 | transition 已消费 REPORT/REVIEW 后改变该文件任一字节 | `EVIDENCE_DIGEST_MISMATCH`；既有 ref 不被当作有效证据 | F4.4.5, F4.7.3, F4.7.5 |
| C7-N01 | C7 | 正常/幂等 | 同 create key 与相同 normalized digest 重试 | 第二次 `Existing`，同 task_id/path/digest，零新事件 | F4.8.1–F4.8.5 |
| C7-R01 | C7 | 拒绝 | 同 key、不同 semantic request digest | `OPERATION_ID_CONFLICT`，原对象不变 | F4.8.3–F4.8.4 |
| C7-X01 | C7 | 并发/重启 | 两进程同 key 同摘要并发，随后重启再请求 | 仅一个 TASK；所有调用返回同结果 | F4.8.2–F4.8.5 |
| C7-CREATE-01 | C7 | 外部幂等边界 | create TASK/Branch 用公共 operation_id 重放；再对普通 T2/T3 任意重放 | create 保持 Existing/conflict 合同；T2/T3 不被宣称具有公共长期重放幂等 | F4.8.1–F4.8.5, F4.9.8 |
| C8-N01 | C8 | 正常 | 单合法 transition 完整提交 | `COMMITTED`；一个权威路径；receipt 可审计 | F4.9.1–F4.9.4 |
| C8-R01 | C8 | 拒绝 | destination 已有不同内容 | `TARGET_ALREADY_EXISTS_DIFFERENT`，双方 bytes 保留 | F4.9.2 |
| C8-X01 | C8 | 崩溃 | 在 PREPARED、TARGET_DURABLE、COMMITTED 与响应返回边界注入故障 | 仅五类定义结果；可恢复或 Fail Closed，不猜测 | F4.9.1–F4.9.4, F4.9.9 |
| C8-X02 | C8 | family 竞态 | create/reopen/convergence/archive 并发 | family 线性化；失败方重读并返回稳定 gate error | F4.9.5 |
| C8-X03 | C8 | 损坏/平台 | 双副本内容分歧、receipt 损坏或 unsupported FS | `RECOVERY_REQUIRED`/`UNSUPPORTED_FILESYSTEM`，保留证据 | F4.9.4, F4.9.7 |
| C8-RETRY-01 | C8 | 授权响应丢失 | T4/T5/T6/T7 已提交但响应丢失，以相同 authorization 重试 | 完全匹配返回既有提交且不二次消费；不同 transition 返回 `AUTHORIZATION_REUSED` | F4.9.8, F4.9.11 |
| C8-STATE-01 | C8 | 五状态恢复 | 参数化执行 §3 的五行 source/target/receipt 组合 | 每行唯一分类与机械动作一致，无额外成功状态 | F4.9.1, F4.9.9–F4.9.10 |
| C8-INDETERMINATE-01 | C8 | 不可证明状态 | source/target 均不存在或 receipt/身份/摘要损坏冲突 | 仅 `INDETERMINATE`；保留可见证据、`RECOVERY_REQUIRED`、Fail Closed | F4.9.1, F4.9.4, F4.9.9 |

## 3. WP1.1 Base filesystem 恢复状态测试表

| test_id | case | source | target | receipt/摘要 | 唯一分类 | 预期动作 |
|---|---|---|---|---|---|---|
| C8-STATE-01 | S1 | 存在且匹配 | 不存在 | 无或 PREPARED | `NOT_COMMITTED` | 保留 source；可安全放弃 |
| C8-STATE-01 | S2 | 存在且匹配 | 存在且同摘要 | TARGET_DURABLE | `RECOVERABLE_DUPLICATE` | 验证后移除 source、持久化目录、完成 receipt |
| C8-STATE-01 | S3 | 不存在 | 存在且匹配 | TARGET_DURABLE 或 COMMITTED | `COMMITTED` | 补全 receipt，不重做迁移 |
| C8-STATE-01 | S4 | 存在 | 存在且摘要不同 | 任意 | `DIVERGENT_DUPLICATE` | 不删不覆盖，等待人工 repair REVIEW |
| C8-STATE-01 | S5 | 均不存在或证据损坏冲突 | 不可证明 | 任意 | `INDETERMINATE` | 保留证据并 Fail Closed |

## 4. WP0 六个原子性/Branch 场景映射

| test_id | WP0 场景 | 线性化对象 | 允许结果 | 禁止结果 | 规范/主测试 |
|---|---|---|---|---|---|
| AT-01 | 同 operation_id create-branch/create-branch | operation key + family | 同摘要同 Branch；异摘要一成功一 conflict | 两个不同 Branch | F4.8, F4.9.5 / C7-X01 |
| AT-02 | create-branch/root-archive | Root family | 一方先提交，另一方重验后拒绝/继续 | archived Root 后出现新 Branch | F4.5.4, F4.9.5 / C8-X02 |
| AT-03 | branch-report/branch-done | Branch attempt | REPORT durable 后才 T3/T4 | 无 current REPORT 的 done | F4.6.2–F4.6.3 / C5-N01 |
| AT-04 | convergence-review/root-archive | Root family digest | 同 canonical family object/digest 才 archive | 缺 Branch 的旧收敛通过 | F4.6.5–F4.6.8 / C5-X01 |
| AT-05 | 提交点前后崩溃/响应丢失 | internal receipt + TASK | 五类结果之一、重试稳定 | 新对象/重复 event/不可解释成功 | F4.9.1–F4.9.11 / C8-X01, C8-RETRY-01 |
| AT-06 | 源/目标双副本和损坏 | TASK identity | same 可恢复；different/corrupt 保留并 fail closed | mtime 猜测、覆盖或删除 | F4.9.2–F4.9.4 / C8-X03 |

```text
ATOMICITY_SCENARIOS_MAPPED: 6/6
```

## 5. MCP、资源与发行符合性合同

| test_id | 场景 | 预期 |
|---|---|---|
| MCP-SURFACE-01 | canonical snapshot/server/CodeFlowMu catalog 集合比较 | FCoP 45；CodeFlowMu 仅额外 close_issue；官方不吸收 |
| MCP-PACKAGE-01 | 4.0 workspace 使用 retained/Legacy tool | adapter 按 workspace version 分派；unsafe behavior Fail Closed；Relay 非 Base 必装合同 |
| RELEASE-GATE-01 | spec/Schema/tests 任一不一致或未获后续 gate | build/publish/tag promotion 被阻断 |

## 6. 覆盖汇总

```text
CORE_CONTRACTS_WITH_NORMAL_CASE: 8/8
CORE_CONTRACTS_WITH_REJECTION_CASE: 8/8
CORE_CONTRACTS_WITH_RECOVERY_OR_PERSISTENCE_CASE: 8/8
ATOMICITY_SCENARIOS_MAPPED: 6/6
WP1_1_REQUIRED_TEST_IDS: 13/13
T1_T7_GATE_MATRIX: 7/7
RECOVERY_STATE_TABLE: 5/5
IDEMPOTENCY_LAYERS: 3/3
BASE_ERROR_CODES: 31/31
TEST_CODE_WRITTEN: 0
WP2_AUTHORIZED: false
```
