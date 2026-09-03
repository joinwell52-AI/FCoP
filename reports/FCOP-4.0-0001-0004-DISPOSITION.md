# FCoP 4.0 · 0001–0004 处置表

> 状态：WP0 audit disposition；不是协议采纳决定
> 基线：`origin/main@68dbeb15f4e7f84e1d03f907be9fa66c2265843e`

## 1. 处置词汇

| 处置 | 含义 |
|---|---|
| `BASE_CORE_CANDIDATE` | 可映射到八项 Base Core，但仍需 WP1 写成可测试合同 |
| `SPECIFICATION` | 解释/约束 Core 的规范文本，不是独立执行机制 |
| `PROFILE` | 角色、组织、权限签发者或项目约定 |
| `TOOLKIT` | 便利 API、索引、审计器、MCP/CLI 表面 |
| `RUNTIME` | scheduler、session、worker、数据库/ledger、UI 或执行器 |
| `LEGACY_V3_ONLY` | 可保留兼容，但不得直接成为 v4 工作区合同 |
| `REJECT_FROM_V4_BASE` | 与 Base Core 边界冲突或会引入双重事实源 |
| `DEFER_TO_WP1` | 方向可用，但 Encoding/边界尚未唯一化 |

## 2. 总览

| 文档 | 原状态/来源 | 可吸收的通用语义 | 必须剥离的下游语义 | WP0 主处置 |
|---|---|---|---|---|
| 0001 Lifecycle Authority | `adopted-pending-release`，CodeFlowMu runtime pressure | review/done/archive 分离；显式授权；transition 可审计 | ADMIN↔PM 主线、PM↔DEV/QA/OPS 支线、固定角色权限表、`delegated_done` 策略 | `SPLIT`：Core candidate + Profile |
| 0002 Fixed Work Folders + Ledger | CodeFlowMu `adopted` | 协作文件与路径事实分离；授权不能由状态/报告推断 | 固定工作面、JSONL ledger/views、Join J1–J5、wake-nudge、LifecycleKernel、Panel 操作手册 | `SPLIT`：少量 Core rationale；主体为 Runtime/Profile |
| 0003 Task Relations & Evidence | `adopted-pending-release` | parent/subject/ref 关系、证据归属、父任务归档控制 | EVAL 类型、CodeFlowMu continuation/child UX 和角色操作流 | `SPLIT_AND_NORMALIZE` |
| 0004 Branch/Merge 草案 | legacy 3.3 taskbook + 4.0 review candidate | Branch 是普通 TASK、`branch_of`、sibling-only、收敛 REVIEW、幂等与 family linearization | BCG 评分、PM merge 裁决、merge checkpoint/runtime、4 个新增 MCP 工具、发布实施 | `SUPERSEDE_LEGACY_DRAFT`；只保留 4.0 Core candidate |

## 3. 0001 · 生命周期权责、Review/Done/Archive

| 原条款/概念 | 事实判断 | 4.0 层 | 处置 | 理由/待决 |
|---|---|---|---|---|
| review、done、archive 不同语义 | 与 v3 路径状态一致 | Base Core C3 | `BASE_CORE_CANDIDATE` | WP1 需定义各自 admission，而非只写人类流程 |
| REPORT 不等于验收决定 | 通用且必要 | Base Core C5/C6 | `BASE_CORE_CANDIDATE` | 证据事实与授权事实必须分离 |
| 归档需要显式授权 | 通用方向成立 | Base Core C6 | `DEFER_TO_WP1` | 必须落为 durable `authorization_ref`，不能是 actor 自报 |
| YAML transition 记录 | 已有 v3 event 事实 | Base Core C3/C6 | `BASE_CORE_CANDIDATE` | 需要明确是否携带 authorization ref |
| 主线 ADMIN↔PM | 项目组织拓扑 | Profile | `PROFILE` | Core 不内置角色名 |
| 支线 PM↔DEV/QA/OPS | CodeFlowMu 团队策略 | Profile | `PROFILE` | 其他 host/team 可采用不同角色 |
| PM/ADMIN 决定 done/archive | 权限签发策略 | Profile | `PROFILE` | Core 只验证授权引用，Profile 判断谁能签发 |
| `delegated_done` | 特定低风险授权策略 | Profile | `PROFILE` | 可作为 authorization profile，不进基本字段 |
| frontmatter 状态投影 | 与 path=NOW 可能形成双真相 | Legacy/Profile | `REJECT_FROM_V4_BASE` | 状态必须由路径或 WP1 唯一 Encoding 决定 |

结论：0001 不能整体“升级为 Core”。其通用部分是 C3/C5/C6 的 runtime evidence；固定角色和主/支线归 Profile。

## 4. 0002 · 固定工作文件夹与 Ledger

| 原条款/概念 | 事实判断 | 4.0 层 | 处置 | 理由/待决 |
|---|---|---|---|---|
| `_lifecycle` 为 TASK 路径事实 | 已是 v3 normative | Base Core C3 | `BASE_CORE_CANDIDATE` | 4.0 需 supersede/兼容声明 |
| `tasks/reports/issues/ledger/attachments` 固定工作面 | CodeFlowMu 运行工作面 | Runtime/Profile | `PROFILE` | Base Core 只要求四类文件及边界，不要求下游投影目录 |
| 双轨 Join J1–J5 | LifecycleKernel 的投影同步算法 | Runtime | `RUNTIME` | Core 不拥有 ledger/cache/read model |
| `ledger/*.jsonl` | 热账本/索引 | Runtime | `RUNTIME` | 可重建，不能成为第二协议事实源 |
| `ledger/views/*` | 查询投影 | Runtime | `RUNTIME` | 明确为 derived view |
| canonical revision / expected revision | 有助于并发校验 | Toolkit/Runtime | `DEFER_TO_WP1` | 若成为 Core 必须由文件合同定义，不能引用 CodeFlowMu DB 对象 |
| AuthorityDecision | 通用授权需求的实例 | Profile/Runtime | `EVIDENCE_INPUT` | WP1 抽象成 authorization reference；不复制类名/角色表 |
| wake-nudge / scheduler / recovery | 调度与运行时 | Runtime | `REJECT_FROM_V4_BASE` | ADR-0038 明确排除 orchestration |
| Panel “归档”按钮流程 | 产品 UX | Runtime | `RUNTIME` | 不是协议调用合同 |
| history 深归档 | v3 当前实现 | Legacy v3 | `LEGACY_V3_ONLY` | WP1 在三种权威模型中唯一选择 |

结论：0002 是重要的 runtime pressure 和兼容样本，但其“已采用”只表示 CodeFlowMu 采用，不表示 FCoP Base Core 已采纳。

## 5. 0003 · 任务关系与证据归属

| 原条款/概念 | 当前映射 | 4.0 层 | 处置 | WP1 规范化要求 |
|---|---|---|---|---|
| `parent` | 当前 `Project.write_task` 已支持 | Base Core C4 | `BASE_CORE_CANDIDATE` | 定义允许目标、强关系、循环与归档影响 |
| `thread_key` | 当前实现支持 | Profile/Toolkit | `TOOLKIT` | 不应替代 parent/branch_of |
| `references` | TASK/REPORT 当前有部分使用 | Base Core C4/C5 | `BASE_CORE_CANDIDATE` | 定义有序/无序、去重、目标类型和失效 |
| `source_task_id` | 当前 REPORT 以 `task_id` 表达 | Base Core C4 | `NORMALIZE_TO_SUBJECT_REF_OR_TASK_REF` | 避免同义字段重复 |
| ISSUE/EVAL 证据归属 | ISSUE 尚缺 subject；EVAL 非四类 Core envelope | C2/C4 + Profile | `SPLIT` | ISSUE 关系进 Core；EVAL 留 Profile/Runtime |
| 强关系/弱关系 | 有利于机器校验 | Specification | `DEFER_TO_WP1` | 明确 parent/branch_of 强，references 弱或按 kind 限定 |
| tree/continuation/child UX | 多为 CodeFlowMu 操作语义 | Profile/Toolkit | `PROFILE` | Base 不规定 UI 入口或主控角色 |
| 父任务归档前检查子任务 | 通用 family closure | Base Core C4/C5 | `BASE_CORE_CANDIDATE` | 扩展到 Branch 与 convergence coverage |

结论：0003 提供关系词汇的实证来源，但必须收敛同义字段，且不能把 EVAL 变成第五类 Base Core 文件。

## 6. 0004 · TASK Branching / Merge 草案

### 6.1 保留为 4.0 候选的部分

| 候选 | 4.0 映射 | 处置 |
|---|---|---|
| Branch 仍是普通 TASK | C2/C4 | `BASE_CORE_CANDIDATE` |
| `branch_of` 指向 Root | C4 | `BASE_CORE_CANDIDATE` |
| 只允许 sibling，不允许 Branch→Branch | C4 | `BASE_CORE_CANDIDATE` |
| Root 只有 active 可创建 Branch | C3/C4 | `DEFER_TO_WP1` |
| Root done 后先授权 reopen，再新增 Branch | C3/C6 | `DEFER_TO_WP1` |
| 每个 Branch 完成需当前 attempt REPORT | C5 | `BASE_CORE_CANDIDATE` |
| 收敛用机器可识别 REVIEW | C5 | `BASE_CORE_CANDIDATE` |
| 收敛覆盖归档提交点的全部 Branch | C5/C8 | `DEFER_TO_WP1` |
| 新 Branch/重开使旧收敛失效 | C5/C8 | `DEFER_TO_WP1` |
| stable operation identity + digest | C7 | `BASE_CORE_CANDIDATE` |
| TASK family 线性化 | C8 | `BASE_CORE_CANDIDATE` |
| 0 个新 MCP 工具也可实现协议 | Toolkit 边界 | `SPECIFICATION` |

### 6.2 从 Base Core 排除的 legacy 3.3 内容

| legacy 内容 | 处置 | 理由 |
|---|---|---|
| BCG Branch Complexity Gate 分数/阈值 | `REJECT_FROM_V4_BASE` | 是策略/工具算法，不是最小跨 host 合同 |
| `work_scope` 的 CodeFlowMu 受控对象模型 | `PROFILE` | 可作为下游 overlap profile |
| PM 做 Merge Decision | `PROFILE` | Core 不内置 PM；只验证收敛事实 |
| PREPARE/BUILD/VERIFY/COMMIT merge state machine | `RUNTIME` | 工作流引擎/恢复 checkpoint，不是 Base lifecycle |
| Base/Candidate/NOW 产品制品合并 | `RUNTIME` | FCoP 协调文件，不拥有业务制品 merge |
| `evaluate_branch_complexity` | `OPTIONAL_TOOLKIT` | 不进入 canonical 必需工具 |
| `create_branch` | `TOOLKIT_CONVENIENCE` | 可由创建普通 TASK + `branch_of` 实现 |
| `prepare_merge` / `commit_merge` | `RUNTIME` | 合并执行和 checkpoint 超出 Core |
| 自动发布 3.3/PyPI/GitHub Release | `SUPERSEDED` | 旧任务书未经合同冻结即实施，已被 4.0 gate 顺序取代 |

## 7. 分层归并结果

| 层 | 从 0001–0004 吸收/保留 | 明确不吸收 |
|---|---|---|
| Base Core | 路径生命周期、四类文件、关系、当前轮证据、收敛、授权引用、幂等、family 原子恢复 | 固定角色、ledger、scheduler、BCG、制品 merge |
| Specification | 字段语义、准入表、强弱关系、错误与恢复结果 | 产品 UI/操作手册 |
| Toolkit | create/read/list/inspect、可选审计与复杂度提示 | 不得成为第二协议逻辑 |
| Profile | ADMIN/PM/DEV/QA/OPS 权责、CodeFlowMu 工作面、签发者资格 | 不得写入 Base 角色表 |
| Runtime | ledger/views、Join、wake/recovery、merge workflow、UI | 不得反向定义 Core |

## 8. WP1 输入清单

1. 为 C1–C8 各写一份唯一、可失败测试验证的合同；
2. 冻结 `parent/branch_of/subject_ref/references`，禁止同义字段并存无映射；
3. 冻结 normal TASK 与 Branch TASK 共同适用的 REPORT/REVIEW/authorization gate；
4. 选择 history 权威模型；
5. 定义 operation lookup key、normalized digest、Existing 与 conflict；
6. 定义 family 线性化、收敛覆盖/失效与 crash recovery；
7. 写出 v3 compatibility/legacy 行为，不把文档保留误称为行为兼容。

```yaml
AMENDMENT_0001: SPLIT_CORE_AND_PROFILE
AMENDMENT_0002: MOSTLY_RUNTIME_PROFILE
AMENDMENT_0003: SPLIT_AND_NORMALIZE
AMENDMENT_0004: LEGACY_DRAFT_SUPERSEDED_CORE_CANDIDATE_ONLY
FCOP_4_CONTRACT_FROZEN: false
IMPLEMENTATION_AUTHORIZED: false
```
