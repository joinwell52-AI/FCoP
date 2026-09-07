---
title: "FCoP 4.0 WP4C.0b：Agent 原生软件工程宪法 v1.0 收口与冻结候选任务书"
document_id: "FCOP-4.0-WP4C.0B-TASKBOOK"
version: "1.0"
date: "2026-09-07"
status: "REVOKED_SCOPE_MISMATCH"
document_role: "EXECUTION_TASKBOOK"
authority: "ADMIN"
execution_authorized: false
authorized_scope: "NONE"
implementation_authorized: false
rule_package_authorized: false
host_generation_authorized: false
main_merge_authorized: false
release_authorized: false
parent_gate: "WP4C_0_BASELINE_ACCEPTED"
parent_gate_commit: "65ed07263de707d327e6e2c358aec2dd7c00a6df"
wp4c_0a_head: "59a6654dbb5387201056004c06068f8afcafb9ed"
candidate_source_commit: "176ed6fa1b44a9c98528f06b08fd89899f914248"
candidate_source_sha256: "87cf212d1cb75cefd0da6da7e5f0f4c7eaedbc231c784b985c3e2e51856abc4c"
candidate_source_size_bytes: 25871
requested_gate: "NONE"
---

> **撤销通知（2026-09-07）**：本文执行权已由 ADMIN 撤销。固定的 `v1.0-rc.1` 文件仅用于 CodeFlowMu 当前开发的过渡准入，不是 FCoP 4.0、组织级或通用工程宪法的采用候选。任何执行者必须停止，不得依据本文生成双语 canonical 文本、采用回执或请求 Gate。文件保留仅用于审计历史。

# FCoP 4.0 WP4C.0b：Agent 原生软件工程宪法 v1.0 收口与冻结候选任务书

## 0. 唯一执行授权

本文件是 WP4C.0b 的唯一执行合同。

执行者只能把已固定的 `v1.0-rc.1` 候选收口为可供 ADMIN 冻结的 `v1.0` 文本、英文对照文本、采用候选记录和审核证据。不得进入 WP4C.1，不得修改规则包、Host 投影、Core、MCP、Schema、CodeFlowMu 或 main。

本任务不签署宪法 Gate。执行完成后必须停止并请求：

```text
ENGINEERING_CONSTITUTION_V1_FROZEN
```

## 1. 固定输入

执行者必须从 ADMIN 下发的本任务书固定提交创建独立 worktree。该提交父链必须同时包含：

```yaml
WP4C_0_BASELINE_GATE_COMMIT: 65ed07263de707d327e6e2c358aec2dd7c00a6df
WP4C_0A_AUDIT_HEAD: 59a6654dbb5387201056004c06068f8afcafb9ed
CANDIDATE_SOURCE_COMMIT: 176ed6fa1b44a9c98528f06b08fd89899f914248
```

唯一候选源：

```text
taskbooks/fcop-4.0/WP4C.0b/sources/Agent-Native-Engineering-Constitution-v1.0-rc.1.zh.md
size: 25871 bytes
SHA-256: 87cf212d1cb75cefd0da6da7e5f0f4c7eaedbc231c784b985c3e2e51856abc4c
encoding: UTF-8
terminal LF: required
license declared by source: MIT
```

执行前必须从 Git blob 原始字节重新计算摘要和字节数。任一不符，以 `CONSTITUTION_CANDIDATE_SOURCE_MISMATCH` 停止。

禁止从 `D:\downloads`、聊天记录、旧 0.1 讨论稿、本地同名文件或浮动分支替换固定输入。

## 2. ADMIN 已作出的收口裁决

### 2.1 身份与权威

候选最终身份固定为：

```yaml
NAME: Agent原生软件工程宪法
VERSION: "1.0"
AUTHORITY_OWNER: joinwell52-AI ADMIN
CANONICAL_REPOSITORY: joinwell52-AI/FCoP
CANONICAL_ZH_PATH: docs/governance/AGENT-NATIVE-ENGINEERING-CONSTITUTION.md
OFFICIAL_EN_PATH: docs/governance/AGENT-NATIVE-ENGINEERING-CONSTITUTION.en.md
LICENSE: MIT
DIGEST_ALGORITHM: sha256
ACTIVATION_SOURCE: external ADMIN Gate receipt
```

这里选择 FCoP 仓库作为当前唯一权威承载点，是因为 FCoP 4.0 的规则分发首先需要引用该文件；这不表示宪法依赖 FCoP，也不强迫其他项目采用 FCoP。

其他仓库只能通过固定版本、提交和摘要引用或保存明确标记的只读快照，不能独立修改正文并冒充同一版本。

### 2.2 语言关系

- 中文文件是 v1.0 的规范性权威文本；
- 英文文件是官方对照文本；
- 两者必须使用相同的章节号、C1–C12 标识和义务强度；
- 英文文本不得新增中文不存在的权力、状态、角色、工具或产品规则；
- 中英文发生不可消除的解释差异时，以中文权威文本为准并停止后续装配；
- 后续修改必须形成新版本，不得只改一种语言。

### 2.3 生效方式

Canonical 文本本身不得写入自己的 SHA-256，也不得通过修改自身 `active: true` 形成自引用。

最终文本必须表达：

```yaml
DOCUMENT_VERSION: "1.0"
TEXT_STATUS: VERSIONED_CANONICAL_TEXT
NORMATIVE_WHEN_ADOPTED: true
ACTIVATION_AUTHORITY: EXTERNAL_ADMIN_GATE_RECEIPT
```

在 ADMIN 签署 `ENGINEERING_CONSTITUTION_V1_FROZEN` 前，候选文件仍不具有实际开发准入效力。Gate 签署后，产品还必须各自建立 adoption/load receipt；全局 Gate 不自动修改任何产品仓库或运行 Session。

### 2.4 适用边界

宪法只约束软件设计、编码、修改、修复、测试实现、发布实现、恢复实现和架构迁移。

它不应默认注入：

- 使用 FCoP 完成普通业务工作的 Agent；
- 普通研究、写作、客服、媒体或运营 Session；
- 仅仅读取 FCoP 文件的第三方应用；
- 不承担软件变更责任的 EVAL 或审阅活动。

开发 FCoP 本体时，装配顺序为：

```text
宪法
→ FCoP开发手册
→ 当前有效FCoP协议合同
→ 当前TASK、AcceptanceContract与授权
```

Host 入口只是指向上述权威文件的薄装配，不是新的宪法来源。

## 3. 必须保留的语义

v1.0 必须完整保留以下十二条原则的实质与编号：

1. 目标由合同确定，实现路径由 Agent 选择；
2. 路径可以涌现，责任与边界必须确定；
3. 执行者可以声明完成，但不能自行验收；
4. 语义裁决只能由承担责任的主体作出；
5. 确定性程序只判断能够完整观察的确定性事实；
6. 轨道物化授权决定，不产生业务决定；
7. EVAL 提供独立评价，不直接驱动生命周期；
8. 机器状态、模型输出和流程结束都不等于工作完成；
9. 不确定必须显式保留，不能被默认值改写成成功；
10. 恢复不得重复未知副作用；
11. AI 可以选择局部实现，不能自行改变事实源、权力和架构；
12. 任何把 Agent 重新变成工作流节点的设计都必须接受架构审查。

还必须保留：

- 执行事实、评价、决定、物化四层分离；
- 完整加载、固定来源、摘要验证与 Fail Closed；
- 高影响动作的授权、幂等、结果查询与未知副作用停止；
- Agent 自主范围与必须停止边界；
- RPA 退化检查；
- 宪法、产品手册、协议合同和当前任务互不替代；
- 修改、版本和 Adoption Receipt 机制；
- MIT License 全文和版权声明。

不得为了缩短文件删去限制条件、例外、失败语义或验收边界。

## 4. 必须移出全局宪法的产品快照

`v1.0-rc.1` 中的 `10.2.1 FCoP 4.0 发布前的 CodeFlowMu 过渡准入` 及其：

- CodeFlowMu 固定提交号；
- `fcop==3.2.5` / `fcop-mcp==3.2.5` 当前版本事实；
- CodeFlowMu 专用十条过渡规则；
- `PRE_FCOP4_COMPATIBILITY_RECEIPT`;

不得进入全局 v1.0 宪法。

原因不是这些内容错误，而是它们属于有时效的 CodeFlowMu 产品开发手册／Adoption Profile。把产品版本快照写进上位宪法会迫使每次产品升级都修改宪法，并与“宪法不规定具体产品状态”的自身边界冲突。

本任务不得修改 CodeFlowMu，也不得在 FCoP 仓库另建一份 CodeFlowMu 过渡规则。只在收口报告中记录：

```yaml
DISPOSITION: MOVE_TO_CODEFLOWMU_PRODUCT_MANUAL_BY_SEPARATE_TASK
CODEFLOWMU_CHANGE_AUTHORIZED: false
```

§10.2 可保留对 CodeFlowMu 的原则性说明，但只能说明：CodeFlowMu 通过自己的开发手册采用宪法，产品细节不进入宪法正文。

## 5. 不得进入宪法的内容

禁止在 v1.0 新增：

- FCoP TASK/REPORT/ISSUE/REVIEW 字段或生命周期编码；
- CodeFlowMu 五桶、PM/DEV/QA/OPS/EVAL 角色配置；
- Scheduler、Runtime、Session、Panel、数据库或日志设计；
- Codex、Cursor、Claude Code 的具体配置字段；
- Subagent、模型名单或 Host 能力准入逻辑；
- 某个仓库的临时 commit、包版本或发布状态；
- WP4C 的规则模块目录和 Manifest Schema；
- 任何把宪法变成操作系统或通用 Runtime 的机制。

允许用 FCoP、CodeFlowMu 作为解释性例子，但例子不得成为其他产品必须采用的协议合同。

## 6. D01–D12 必须闭合

必须在报告中逐项关闭 WP4C.0a 的十二项决定：

| ID | 固定裁决 |
|---|---|
| D01 | 正式名称为《Agent原生软件工程宪法》，版本 v1.0 |
| D02 | 当前唯一权威仓库为 joinwell52-AI/FCoP，中文路径见 §2.1 |
| D03 | 中文规范性权威，英文官方对照；编号与义务强度一致 |
| D04 | 适用于软件开发 Agent，不默认适用于普通业务 Agent |
| D05 | 只有被产品 Adoption 明确选中的正式软件开发 Session 强制加载 |
| D06 | 宪法约束工程边界，不重新定义 Core/Spec/Profile/Toolkit/Runtime |
| D07 | 宪法独立于通用 Rule Package，后者只能引用其固定身份 |
| D08 | 修改须独立修订、版本、摘要、审核与 ADMIN Gate |
| D09 | MIT；复制或派生时保留版权与许可文本 |
| D10 | 摘要以 canonical Git blob 原始字节计算，记录在外部 Gate/Manifest |
| D11 | Host 只引用同一固定身份；不手工维护多个正文真相 |
| D12 | 普通业务 Agent 默认不加载；后续必须有负向装配测试 |

如果正文无法与上述任一裁决一致，必须停止，不得自行改写裁决。

## 7. 允许修改的文件

只允许新增：

```text
docs/governance/AGENT-NATIVE-ENGINEERING-CONSTITUTION.md
docs/governance/AGENT-NATIVE-ENGINEERING-CONSTITUTION.en.md
reports/FCOP-4.0-WP4C.0B-CONSTITUTION-FREEZE-CANDIDATE.md
reviews/fcop-4.0/wp4c.0b/MANIFEST.md
```

固定候选源只读，不得修改。

禁止修改：

- `spec/`
- `src/`
- `mcp/`
- `tests/`
- AGENTS.md、CLAUDE.md、.cursor/
- 现有规则源、生成器与团队模板
- CodeFlowMu
- main、版本号、发布工作流与制品

如目标 canonical 文件已存在，必须先停止并报告 `CANONICAL_CONSTITUTION_PATH_COLLISION`，不得覆盖。

## 8. 文本收口规则

### 8.1 中文 canonical

以固定 RC 字节为唯一正文来源，只允许：

- 将版本身份从 `1.0-rc.1` 收口为 `1.0`；
- 将候选状态改成“由外部 Gate 激活的版本化 canonical 文本”；
- 应用 §4 的产品快照移出决定；
- 修正由上述两项产生的交叉引用；
- 将 Adoption 回执示例中的版本固定为 1.0；
- 修正明确的编号错误或同文自相矛盾；
- 保持 MIT License 与十二原则实质不变。

不得进行风格重写、扩写新原则或改变 MUST/MUST NOT/SHOULD/MAY 强度。

### 8.2 英文官方对照

英文必须逐节对应中文，不得摘要化。至少验证：

- 顶层章节编号一致；
- C1–C12 一一对应；
- 术语表条目一致；
- Fail Closed 错误码集合一致；
- 强制准入、停止条件和 RPA 审查项目计数一致；
- MIT License 文本一致；
- 没有新增产品专用快照。

中文专有名词可以保留并提供英文解释，不得通过翻译改变权力关系。

## 9. 验证要求

至少完成：

1. 固定输入 commit、父链、25871 bytes 与 SHA-256；
2. 四个交付文件严格 UTF-8、LF、无 BOM；
3. 中文 canonical 与 RC 的允许差异逐 hunk 解释；
4. 中文 C1–C12 存在且各出现一次；
5. 英文 C1–C12 存在且各出现一次；
6. 中英文顶层章节、规范性关键词和错误码集合对齐；
7. CodeFlowMu commit、`fcop==3.2.5`、`PRE_FCOP4_COMPATIBILITY_RECEIPT` 不存在于 canonical 双语文本；
8. 两份 canonical 文本均不写自身 SHA-256；
9. License 为 MIT，版权主体与年份一致；
10. 普通业务 Agent 排除规则在双语文本中明确；
11. 未修改 frozen FCoP 4.0 Specification/Core/Schema/Conformance；
12. 未修改规则、Host、MCP、CodeFlowMu、main；
13. `git diff --check` 与四文件 allowlist 通过。

允许使用一次性只读检查命令；不得为了本阶段新增生产验证器、Schema 或 Runtime。

## 10. GitHub 交付

使用独立 review 分支，建议：

```text
review/fcop-4.0-wp4c.0b-constitution-freeze-candidate
```

必须采用两提交：

1. Content commit：双语 canonical 文本和收口报告；
2. Manifest commit：只新增 Manifest，记录三份 Content 文件和自身的远端 SHA-256、父链及验证结果。

随后：

- push；
- refetch；
- 验证远端 HEAD、直接父链和 4/4 文件 SHA-256；
- 创建 Draft PR；
- 留完整机器可读回执；
- 停止。

不得把任务书分支合并 main，不得合并 Draft PR。

## 11. 强制停止条件

以下任一出现必须停止：

- 固定候选源摘要或字节数不匹配；
- canonical 路径已有未授权文件；
- 无法在不改变 C1–C12 实质的情况下移出产品快照；
- 中英文义务强度或条款结构无法对齐；
- 需要修改 FCoP 4.0 冻结合同；
- 需要修改规则、Host、MCP、CodeFlowMu 或测试；
- 需要发明新的宪法原则或产品架构；
- 需要把普通业务 Agent 纳入默认强制加载；
- 交付范围超出四个文件；
- 无法证明远端文件摘要与本地 Git blob 一致。

停止时只允许提交事实报告，不得请求 Gate。

## 12. 完成回执

```yaml
WP4C_0B_STATUS: COMPLETE | BLOCKED
AUTHORIZED_SCOPE: WP4C_0B_ONLY
TASKBOOK_COMMIT: ""
TASKBOOK_SHA256: ""
INPUT_HEAD: ""
PARENT_GATE_COMMIT: 65ed07263de707d327e6e2c358aec2dd7c00a6df
CANDIDATE_SOURCE_COMMIT: 176ed6fa1b44a9c98528f06b08fd89899f914248
CANDIDATE_SOURCE_SIZE: 25871
CANDIDATE_SOURCE_SHA256: 87cf212d1cb75cefd0da6da7e5f0f4c7eaedbc231c784b985c3e2e51856abc4c
D01_D12_DECISIONS: 12/12
ZH_CANONICAL_STATUS: VERSIONED_TEXT_PENDING_GATE
EN_PARITY: PASS | FAIL
C1_C12_ZH: 12/12
C1_C12_EN: 12/12
PRODUCT_SNAPSHOT_REMOVED: PASS
MIT_LICENSE: PASS
UTF8_LF_NO_BOM: 4/4
FILES_WRITTEN: 4/4
CONTENT_COMMIT: ""
MANIFEST_COMMIT: ""
REMOTE_HEAD: ""
REMOTE_PUSHED: true
REMOTE_REFETCH_VERIFIED: PASS
DELIVERY_SHA256: 4/4
ENGINEERING_CONSTITUTION_V1_FROZEN: false
WP4C_1_STARTED: false
MAIN_MODIFIED: false
CODEFLOWMU_MODIFIED: false
REQUESTED_GATE: ENGINEERING_CONSTITUTION_V1_FROZEN
```

本任务书不签署 Gate。执行者完成后必须停止，等待 ADMIN 逐条审核 v1.0 文本。
