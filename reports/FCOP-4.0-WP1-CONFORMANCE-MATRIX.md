# FCoP 4.0 WP1 · WP2 符合性合同矩阵

> 本文件只定义未来测试合同；`TEST_CODE_WRITTEN: 0`。

## 1. 规范/双语权威

| test_id | 场景 | 输入/动作 | 预期可观察结果 | 条款 |
|---|---|---|---|---|
| C0-PARITY-01 | 英中候选对等 | 提取条款 ID、T1–T7、C1–C8、错误代码 | 集合完全一致，否则 gate fail | F4.0.2 |
| C0-AUTH-01 | Schema/规范冲突 | 构造 Schema 可接受但行为违规的迁移 | 行为拒绝且发布 gate fail；Schema 不覆盖行为规范 | F4.0.3, F4.12.3 |

## 2. C1–C8 测试合同

| test_id | Core | 类型 | 场景 | 预期结果/错误 | 条款 |
|---|---|---|---|---|---|
| C1-N01 | C1 | 正常 | 创建 4.0 workspace，并写匹配 workspace_id 的 TASK | 声明可读，TASK 创建成功 | F4.2.1–F4.2.3 |
| C1-R01 | C1 | 拒绝 | envelope workspace_id 与 manifest 不同 | `WORKSPACE_ID_MISMATCH`，零写入 | F4.2.2 |
| C1-X01 | C1 | 恢复/复制 | 两个独立可写 clone 保留同 ID 且无单写者证明 | `WORKSPACE_ID_CLONE_CONFLICT`，Fail Closed | F4.2.4 |
| C2-N01 | C2 | 正常 | 分别创建合法 TASK/REPORT/ISSUE/REVIEW | 四类均按共同/类型字段解码 | F4.3.1–F4.3.2 |
| C2-R01 | C2 | 拒绝 | 创建 EVAL 或缺 typed ID/subject_ref 的 envelope | `INVALID_ENVELOPE` | F4.3.1–F4.3.2 |
| C2-R02 | C2 | 追加性 | 尝试原地修改 REVIEW；再用新 REVIEW references 修正 | 原地修改拒绝；追加事实成功且旧 bytes 不变 | F4.3.3, F4.3.5 |
| C3-N01 | C3 | 正常 | T1→T2→T3→T4→T7 合法链 | 每次仅一边/一 event，最终 archive | F4.4.1–F4.4.3 |
| C3-N02 | C3 | 正常/reopen | done TASK 有授权执行 T6 | 进入 active，生成新 attempt | F4.4.2(T6), F4.6.1 |
| C3-R01 | C3 | 拒绝 | 从 inbox 单调用直达 archive | 非法边错误，仍在 inbox | F4.4.2–F4.4.3 |
| C3-R02 | C3 | 拒绝/Legacy | 4.0 workspace 调 `finish_task` | `LEGACY_TRANSITION_NOT_ALLOWED`，无 active→done | F4.4.4 |
| C3-R03 | C3 | 拒绝/Legacy | 将 archive 权威 TASK 移入 history | 拒绝；archive TASK 原位 | F4.4.6, F4.11.2 |
| C3-X01 | C3 | 恢复 | 冷存储导出中断 | 权威 archive 不变；残留导出无 NOW 权力 | F4.4.6, F4.9.4 |
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
| C6-N01 | C6 | 正常 | Profile 认可签发者追加绑定当前 transition/attempt 的 authorization REVIEW | transition 成功且 event 保存 authorization_ref | F4.7.1–F4.7.5 |
| C6-R01 | C6 | 拒绝 | 只有 actor=`ADMIN` 或授权 subject/edge/attempt 不匹配 | `AUTHORIZATION_REQUIRED`/`AUTHORIZATION_INVALID` | F4.7.3–F4.7.5 |
| C6-R02 | C6 | 拒绝 | 授权过期或 single-use 被第二 transition 使用 | `AUTHORIZATION_EXPIRED`/`AUTHORIZATION_REUSED` | F4.7.3 |
| C6-X01 | C6 | 响应丢失 | 已消费授权后响应丢失并重试同 transition | 返回既有提交结果，不产生第二消费 | F4.7.3, F4.9.4 |
| C7-N01 | C7 | 正常/幂等 | 同 create key 与相同 normalized digest 重试 | 第二次 `Existing`，同 task_id/path/digest，零新事件 | F4.8.1–F4.8.5 |
| C7-R01 | C7 | 拒绝 | 同 key、不同 semantic request digest | `OPERATION_ID_CONFLICT`，原对象不变 | F4.8.3–F4.8.4 |
| C7-X01 | C7 | 并发/重启 | 两进程同 key 同摘要并发，随后重启再请求 | 仅一个 TASK；所有调用返回同结果 | F4.8.2–F4.8.5 |
| C8-N01 | C8 | 正常 | 单合法 transition 完整提交 | `COMMITTED`；一个权威路径；receipt 可审计 | F4.9.1–F4.9.4 |
| C8-R01 | C8 | 拒绝 | destination 已有不同内容 | `TARGET_ALREADY_EXISTS_DIFFERENT`，双方 bytes 保留 | F4.9.2 |
| C8-X01 | C8 | 崩溃 | 在 temp/replace/unlink/response 各 kill point 重启 | 仅五类定义结果；可恢复或 Fail Closed，不猜测 | F4.9.1–F4.9.4 |
| C8-X02 | C8 | family 竞态 | create/reopen/convergence/archive 并发 | family 线性化；失败方重读并返回稳定 gate error | F4.9.5 |
| C8-X03 | C8 | 损坏/平台 | 双副本内容分歧、receipt 损坏或 unsupported FS | `RECOVERY_REQUIRED`/`UNSUPPORTED_FILESYSTEM`，保留证据 | F4.9.4, F4.9.7 |

## 3. WP0 六个原子性/Branch 场景映射

| test_id | WP0 场景 | 线性化对象 | 允许结果 | 禁止结果 | 规范/主测试 |
|---|---|---|---|---|---|
| AT-01 | 同 operation_id create-branch/create-branch | operation key + family | 同摘要同 Branch；异摘要一成功一 conflict | 两个不同 Branch | F4.8, F4.9.5 / C7-X01 |
| AT-02 | create-branch/root-archive | Root family | 一方先提交，另一方重验后拒绝/继续 | archived Root 后出现新 Branch | F4.5.4, F4.9.5 / C8-X02 |
| AT-03 | branch-report/branch-done | Branch attempt | REPORT durable 后才 T3/T4 | 无 current REPORT 的 done | F4.6.2–F4.6.3 / C5-N01 |
| AT-04 | convergence-review/root-archive | Root family digest | 同 generation/digest 才 archive | 缺 Branch 的旧收敛通过 | F4.6.5–F4.6.8 / C5-X01 |
| AT-05 | 提交点前后崩溃/响应丢失 | operation + TASK | 五类结果之一、重试稳定 | 新对象/重复 event/不可解释成功 | F4.9.1–F4.9.4 / C8-X01 |
| AT-06 | 源/目标双副本和损坏 | TASK identity | same 可恢复；different/corrupt 保留并 fail closed | mtime 猜测、覆盖或删除 | F4.9.2–F4.9.4 / C8-X03 |

```text
ATOMICITY_SCENARIOS_MAPPED: 6/6
```

## 4. MCP、资源与发行符合性合同

| test_id | 场景 | 预期 |
|---|---|---|
| MCP-SURFACE-01 | canonical snapshot/server/CodeFlowMu catalog 集合比较 | FCoP 45；CodeFlowMu 仅额外 close_issue；官方不吸收 |
| MCP-PACKAGE-01 | 4.0 workspace 使用 retained/Legacy tool | adapter 按 workspace version 分派；unsafe behavior Fail Closed；Relay 非 Base 必装合同 |
| RELEASE-GATE-01 | spec/Schema/tests 任一不一致或未获后续 gate | build/publish/tag promotion 被阻断 |

## 5. 覆盖汇总

```text
CORE_CONTRACTS_WITH_NORMAL_CASE: 8/8
CORE_CONTRACTS_WITH_REJECTION_CASE: 8/8
CORE_CONTRACTS_WITH_RECOVERY_OR_PERSISTENCE_CASE: 8/8
ATOMICITY_SCENARIOS_MAPPED: 6/6
TEST_CODE_WRITTEN: 0
WP2_AUTHORIZED: false
```
