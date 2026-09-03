# FCoP 4.0 WP1 · 30 项合同冲突裁决

> 输入：`reports/FCOP-4.0-CONTRACT-CONFLICTS.md`（30/30）
>
> 状态含义：`RESOLVED` 表示候选规范已有唯一决定；不表示 ADMIN 已签署合同冻结。

| conflict_id | baseline_fact | v4_decision | normative_clause | compatibility | wp2_test_id | status |
|---:|---|---|---|---|---|---|
| 1 | current v3 spec 写 3.2.4/rules 3.2.3，包为 3.2.5 | 4.0 使用独立双语 Candidate，明确 3.2.5 仍 current，冻结前不得冒充发布规范 | F4.0.2, F4.12.4 | 转换 | C0-PARITY-01 | RESOLVED |
| 2 | v1.x Schema 自称 SSOT，却未编码 v3 行为且版本混合 | Schema 仅对可表达结构有机器权威；行为由规范定义；任一冲突阻断发布 | F4.0.3, F4.12.3 | 转换 | C0-AUTH-01 | RESOLVED |
| 3 | workspace 依赖路径/fcop.json，无稳定 ID | `fcop/fcop.json` 必含 protocol/version/workspace_id/encoding/profiles；clone/fork 规则唯一化 | F4.2.1–F4.2.5 | 转换 | C1-N01, C1-R01, C1-X01 | RESOLVED |
| 4 | 四类 envelope 字段演进且 Schema 开放 | 正式 envelope 仅四类，冻结共同字段、类型字段与 append-only 规则 | F4.3.1–F4.3.5 | 转换 | C2-N01, C2-R01 | RESOLVED |
| 5 | parent/thread_key/references 与候选词汇不统一 | Core 只保留 parent/branch_of/subject_ref/references；thread_key 降 Profile/Legacy | F4.5.1–F4.5.5 | 转换 | C4-N01, C4-R01 | RESOLVED |
| 6 | history 把权威 TASK 移出 path-NOW lifecycle | archive 是终态；4.0 禁止权威 archive→history；Legacy history 只读，冷存储仅非权威副本 | F4.4.6, F4.11.2 | Legacy | C3-R03, C3-X01 | RESOLVED |
| 7 | history 先移 TASK 再逐个 REPORT，可能部分提交 | 4.0 不执行该权威移动；若 Toolkit 导出副本，失败不得改变 archive 权威事实 | F4.4.6, F4.9.1–F4.9.4 | Legacy | C3-X01, C8-X03 | RESOLVED |
| 8 | history 不可变仅靠约定 | v3 history 只读 Legacy；4.0 权威 archive 不动，导出副本无 NOW 权力 | F4.4.6, F4.11.2 | Legacy | C3-R03 | RESOLVED |
| 9 | archive_task 可从 inbox/active/review 跨多边 | 一次命令一条边；4.0 archive 仅 T7 done→archive；跨边调用拒绝 | F4.4.2–F4.4.3 | 转换 | C3-R01, C3-R02 | RESOLVED |
| 10 | 当前无 done→active | 4.0 T6 加入受授权 reopen，并生成新 attempt | F4.4.2(T6), F4.6.1, F4.7 | 转换 | C3-N02, C5-R02 | RESOLVED |
| 11 | active→review 不机械要求 REPORT | T3 必须引用当前 attempt 唯一有效 REPORT | F4.4.2(T3), F4.6.2 | 转换 | C5-N01, C5-R01 | RESOLVED |
| 12 | finish_task active→done 不要求 REPORT | active→done 从 Base 删除；4.0 workspace 返回 `LEGACY_TRANSITION_NOT_ALLOWED` | F4.4.4 | Legacy/Deprecated | C3-R02 | RESOLVED |
| 13 | finish_task 只有 actor，无授权 | 同上；Legacy 名称不能在 4.0 绕过 T3/T4 | F4.4.4, F4.11.2 | Legacy/Deprecated | C3-R02 | RESOLVED |
| 14 | approve/reject actor 为调用者自报 | transition 必须引用 durable REVIEW authorization；Profile 验签发权 | F4.7.1–F4.7.5 | 转换 | C6-N01, C6-R01 | RESOLVED |
| 15 | archive 无 actor/ref，事件使用 `archiver` | T7 必须持久保存 authorization_ref；自报 actor/合成 actor 无授权力 | F4.4.2(T7), F4.7.5 | 转换 | C6-R01, C6-X01 | RESOLVED |
| 16 | archive 不检查 REPORT/REVIEW/ISSUE/child/Branch | T7 校验普通 closure；有 Branch 时还需 current REPORT 集与有效 convergence/family digest | F4.4.2(T7), F4.6.5–F4.6.8, F4.9.5 | 转换 | C5-N02, C5-R03, C8-X02 | RESOLVED |
| 17 | REPORT 只绑定 task_id，不绑定执行轮次 | 每次 active 新 attempt；REPORT 必含 subject_ref+attempt_id；旧轮次永不复用 | F4.6.1–F4.6.2 | 转换 | C5-N01, C5-R02 | RESOLVED |
| 18 | REVIEW 无 review_kind/references，收敛不可机读 | convergence REVIEW 固定 kind/subject/family_digest/references，并精确覆盖 Branch current heads | F4.6.5–F4.6.8 | 转换 | C5-N02, C5-R03 | RESOLVED |
| 19 | ISSUE 无 subject_ref | ISSUE 必有 subject_ref；workspace 级用 `workspace:<workspace_id>` | F4.3.2, F4.5.1 | 转换 | C2-N01, C4-R01 | RESOLVED |
| 20 | mark_human_approved 原地改写 REVIEW | REVIEW 追加事实；兼容入口只能新建 REVIEW 并 references 原事实 | F4.3.3, F4.3.5 | 转换/Deprecated old behavior | C2-R02, C6-N01 | RESOLVED |
| 21 | transition 无 authorization_ref | 有授权门的 event 必含 authorization_ref；Core 验绑定/时效/复用 | F4.4.5, F4.7.3–F4.7.5 | 转换 | C6-N01, C6-R01 | RESOLVED |
| 22 | create 只有 O_EXCL/序号，无 durable operation identity | 创建 TASK/Branch 强制固定 lookup key，原子保留并跨重启 | F4.8.1–F4.8.3 | 转换 | C7-N01, C7-X01 | RESOLVED |
| 23 | 无 normalized digest/Existing/conflict | 冻结 create digest 字段和 canonicalization；同键同摘要 Existing，异摘要稳定 conflict | F4.8.3–F4.8.5 | 转换 | C7-N01, C7-R01 | RESOLVED |
| 24 | replace 后 unlink 前崩溃可双副本 | 明确五类结果；重复时 reader Fail Closed，恢复凭 operation/digest/receipt | F4.9.1, F4.9.3–F4.9.4 | 转换 | C8-X01, AT-05, AT-06 | RESOLVED |
| 25 | commit 使用 replace 静默覆盖目标 | 禁止覆盖；同证据同内容 Existing/Recoverable，不同内容稳定错误 | F4.9.2 | 转换 | C8-R01, AT-06 | RESOLVED |
| 26 | 无目录 fsync、crash cleanup/repair 合同 | durable receipt + 显式幂等 repair；遗留锁不能按年龄静默删；平台范围明确 | F4.9.4, F4.9.6–F4.9.7 | 转换 | C8-X01, C8-X03, AT-05, AT-06 | RESOLVED |
| 27 | 无 branch_of/active-root/sibling-only 准入 | Branch 是普通 TASK；Root 必须 active；branch_of 不得指向 Branch | F4.5.3–F4.5.4 | 新增 Core | C4-N02, C4-R02, AT-01, AT-02 | RESOLVED |
| 28 | 无 family lock、覆盖快照和收敛失效 | family digest 绑定全部 Branch 当前 attempt/report；相关操作共享 family 线性化边界 | F4.6.6–F4.6.8, F4.9.5 | 新增 Core | C5-X01, C8-X02, AT-02–AT-04 | RESOLVED |
| 29 | FCoP 45 tools；CodeFlowMu catalog 独多 close_issue | 官方仍按 45 映射；close_issue 明确排除为 downstream drift | F4.11.3–F4.11.4 | 拒绝进入官方表面 | MCP-SURFACE-01 | RESOLVED |
| 30 | MCP relay 必装、fcop<4；发布缺 v4 gate/tag/environment hardening | Core 排除 Relay/发布；候选规定 Relay 可选与版本分派；4.0 发布必须等规范/Schema/测试一致和后续 Gate | F4.11.3, F4.11.5, F4.12.3–F4.12.4 | Toolkit/Release 转换 | MCP-PACKAGE-01, RELEASE-GATE-01 | RESOLVED |

## 数量与开放项

```text
CONTRACT_CONFLICTS_RESOLVED: 30/30
P0_TBD: 0
P0_OPEN: 0
BLOCKED: 0
```

所有决定均落到 `spec/fcop-4.0-spec.md` / `.zh.md` 的可观察条款；没有通过引入 Runtime、第五类信封或 CodeFlowMu 私有状态来“解决”冲突。
