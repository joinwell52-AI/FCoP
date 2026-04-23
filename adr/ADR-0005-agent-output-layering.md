# ADR-0005: Agent 产出物分层（Observation Output Lifecycle）

- **Status**: Accepted
- **Date**: 2026-04-23
- **Deciders**: ADMIN
- **Related**: [ADR-0003](./ADR-0003-stability-charter.md), [ADR-0004](./ADR-0004-time-is-filesystem.md)

## ADMIN 决议（2026-04-23）

ADMIN 在审 0.6.0rc1 文档时问了一个 0.6 协议没回答的问题：

> "有个问题，agent 的一些检测结果文件放在哪里？"

并展示了真实案例 —— `.runtime-qa-095.json` / `.runtime-qa-100-scan.json` 这类 agent 运行时自产的 JSON 文件。这是 FCoP 0.5.x 遗留的灰色地带：协议只管 `tasks/` / `reports/` / `issues/`，agent 其他产出物没有归宿标准，各自为政。

本 ADR 把这块一次性定死。

---

## Context

Agent 在工作过程中会产生多种不同性质的数据，目前各自散落：

| 观察到的产出物 | 实际出现位置（0.5.x） | 问题 |
|---|---|---|
| `inspect_task` / `inspect_file` 校验结果 | 有时打印到日志，有时写成 md | 无标准 |
| `audit_project` / 巡检扫描结果 | `_ignore/`、根目录、临时 `.json` | 散乱 |
| QA/DEV agent 的 runtime state（如 `.runtime-qa-NNN.json`） | `docs/agents/` 根下、`workspace/` | 污染协议目录 |
| 本地脚本跑出来的一次性报告 | 根目录、`tmp/`、`_ignore/` | 混入 git |
| 需要其他 agent 跟进的问题发现 | 直接写个普通 md 文件 | 绕开了 issue 机制 |

这会导致：

1. **协议命名空间污染**：`docs/agents/` 下混入非协议文件，其他 agent `list_tasks` / `list_reports` 容易误伤
2. **信息孤岛**：audit 结果散在多处，没有标准位置去"查上次扫描结果"
3. **责任边界模糊**：agent 到底该把 scratch state 放哪？每个 agent 作者都得自己猜
4. **git 噪音**：运行时缓存混入版本控制

---

## Decision

### 核心原则：按**生命周期**和**可见性**分 5 档

所有 agent 产出物归入下表**唯一的一档**。新写的 tool / feature 必须在这 5 档里落位。

| 档位 | 名称 | 典型例子 | 存放位置 | 入 git？ | 跨 agent 可见？ | 生命周期 |
|---|---|---|---|---|---|---|
| **A** | 瞬时诊断 | `inspect_task` 返回值、pre-write 校验 | **不落盘**（MCP 工具返回 JSON） | — | 调用方 | 一次调用 |
| **B** | 巡检痕迹 | audit 快照、patrol 输出、巡检日志 | `docs/agents/log/` | ✅ 建议入 | ✅ 所有 agent + 人 | append-only，永久保留 |
| **C** | 协议级问题 | 严重不合规、阻塞事件、需他人修复的缺陷 | `docs/agents/issues/` | ✅ 必须入 | ✅ 所有 agent + 人 | open → closed |
| **D** | Agent 私有运行时 | session state、checkpoint、cache、`runtime-*.json` | `docs/agents/.runtime/{agent-code}/` | 🟡 项目自决（`.gitignore` 友好） | ❌ **只有生成者** | agent 重启/重建即失效 |
| **E** | 人的一次性考察 | 手写的探索性脚本、本地 audit JSON | `_ignore/` 或仓库外 | ❌ 不入 | ❌ 只本地 | 用完即弃 |

### 分档判定树

面对一个新产出物，按顺序回答：

1. **调用方拿到就够了？** → A（返回值，不落盘）
2. **其他 agent/人需要基于它做决定？**
   - 需要"处理"（修 bug / 改文件）→ **C**（走 `write_issue`）
   - 只需要"查询历史"（上次扫描结果、过去一周的事件）→ **B**（`log/`）
3. **只有生成它的 agent 自己要读？** → **D**（`.runtime/`）
4. **只是人在本地玩一把？** → **E**（`_ignore/`）

### 五档的具体约束

#### A. 瞬时诊断

- MCP tool / Python API 的返回值
- 严禁落盘（落盘就应该升到 B/C/D 档）
- 符合 ADR-0003 稳定性宪章对 tool 合同的约束

#### B. `docs/agents/log/`

- **Append-only**（符合 FCoP Rule 5 文件不可变）
- 文件名约定：`{KIND}-{YYYYMMDD}T{HHMMSS}-{SUBJECT}.{ext}`
  - `KIND` ∈ `AUDIT` / `PATROL` / `SCAN` / `EVENT` 等，大写 ASCII
  - `ext` 可以是 `json` / `md` / `jsonl`，由工具决定
  - 示例：`AUDIT-20260423T143500-compliance.json`、`PATROL-20260423T150000-relay.md`
- **无 frontmatter schema 约束**：不是 agent 通信文件，解析规则由生成工具自己定义
- **可以跨 agent 读**：未来可能加 `Project.list_logs(kind=...)` 之类的读取器
- **不走 `list_tasks` / `list_reports` 等协议扫描**：log 与协议文件严格隔离

#### C. `docs/agents/issues/`

维持现状。一切**需要他人跟进**的发现都必须走 `write_issue`，不允许"自造 issue 表达机制"（比如写一个 `FINDINGS-*.md` 然后期待别人看）。

这一条是对 agent 的**纪律**：你发现问题 → 开 issue，其他 agent 在 `list_issues()` 里能查到。不开 issue 就是没发生。

#### D. `docs/agents/.runtime/{agent-code}/`

- **路径结构**：`docs/agents/.runtime/{AGENT_CODE}/<任意层级>`
  - `AGENT_CODE` 遵循 FCoP 文件名角色码规则（大写 ASCII + 连字符 + 可选 `.SLOT`）
  - 小写目录名 `runtime` 前加 `.` 提示"这是隐藏/运行时"
  - 示例：`docs/agents/.runtime/QA/095.json`、`docs/agents/.runtime/DEV.BACKEND/session.db`
- **只有生成它的 agent 自己读**：协议上禁止跨 agent 读（想通信请走 B 或 C）
- **FCoP 库零语义**：
  - 不扫描、不验证、不解析、不写入
  - `list_*` / `read_*` / `inspect_*` 永远忽略 `.runtime/`
  - 内容可以是任何格式（JSON / pickle / sqlite / 二进制）
- **git 策略由项目自决**：
  - 想共享（比如分布式 agent 协作）→ 入 git
  - 想私有（纯本地缓存）→ `.gitignore` 里加 `docs/agents/.runtime/`
  - FCoP 不强制二选一

#### E. `_ignore/` 或仓库外

- 人手写的探索性脚本、一次性调试输出
- 严禁 `git add`（目录应该进 `.gitignore`）
- 典型例子：审计脚本 `_ignore/audit_legacy_fcop.py`、冒烟测试 `_ignore/smoke_06_on_codeflow3.py`
- 生命周期：几小时到几天，用完删

---

## Consequences

### 正面

1. **协议命名空间纯净**：`docs/agents/tasks/` / `reports/` / `issues/` 不会再混入运行时脏数据
2. **Agent 纪律**：任何新 feature 作者拿到 ADR-0005 都能 30 秒回答"我这玩意放哪"
3. **工具合同更清楚**：ADR-0003 的稳定承诺延伸到"新 tool 必须落档"
4. **向后兼容**：0.5.x 那些放错位置的 runtime 文件在 0.6 属于"agent 视角看不见"（按 MIGRATION-0.6 §0 心智模型），人视角下完全保留，不影响历史

### 负面

1. **目录结构多一层**：`docs/agents/` 从 4 个子目录（tasks/reports/issues/log）变成 5 个（加 .runtime）
2. **`.runtime/` 的 git 策略不统一**：不同项目可能选不同（入 git vs ignore），需要在 README 里显式告知新用户

这些成本换来清晰的归宿标准，值。

---

## Alternatives Considered

### 备选 1：所有 runtime 扔 `_ignore/`

**否决**：`_ignore/` 是"人的一次性"（E 档）语义，agent 每次重启都要重建 state 会很痛。而且 `_ignore/` 按约定是 git-ignored，分布式 agent 想共享 state 时没路径。

### 备选 2：agent runtime 丢 `docs/agents/` 根目录

**否决**：污染协议命名空间。未来加 `list_*` 类 tool 都要给 runtime 文件写黑名单。

### 备选 3：每类都独立目录（runtime/cache/state/checkpoint 分开）

**否决**：过度设计。`.runtime/{agent}/` 下爱怎么组织是 agent 的事，协议不该管。

### 备选 4：不叫 `.runtime/`，叫 `.scratch/` / `.agent-cache/`

**否决**：用户决定用 `.runtime/`（决议时间 2026-04-23）。理由：与真实观察到的命名（`.runtime-qa-*.json`）对齐，且比 `scratch` 更明确传达"运行时"语义。

### 备选 5：把 B 档 log 也合进 .runtime/

**否决**：B 和 D 的**可见性**完全不同（B 跨 agent，D 私有）。混在一起会让"我能不能读这个文件"变成灰色问题。

---

## Implementation Timeline

### 0.6.0rc1（本次）

**协议决议落地**，不动代码：

1. ✅ 本 ADR Accepted
2. ✅ `adr/README.md` 索引加入
3. ✅ `docs/MIGRATION-0.6.md` 加提示：0.5.x 乱丢的 runtime 文件建议迁入 `.runtime/{agent}/`（非强制）
4. ✅ 0.5.x 在协议根目录的误放文件保持 MIGRATION §0 心智模型：**人可见、agent 不可见**

### 0.6.1（下一版）

**库端 helper**（additive、符合 ADR-0003）：

- `Project.agent_runtime_dir(agent_code: str) -> Path`：返回 `docs/agents/.runtime/{agent}/`，自动 `mkdir -p`
- `Project.list_logs(kind: str | None = None) -> list[LogEntry]`：列 B 档 log 文件
- `Project.write_log(kind: str, subject: str, payload: bytes | str) -> LogEntry`：写 B 档 log

所有新 API 进 `test_public_surface.py` snapshot 锁定。

### 0.7.0（远期，如有需要）

- MCP 工具：`agent_runtime_dir` / `list_logs` / `write_log` 三个 tool，加入 `test_tool_surface.py`
- `list_agents()` / `clean_runtime(agent_code)` 等 admin 工具（可选）

---

## Notes

- 本 ADR 只规定**归宿**和**可见性**，不规定 `.runtime/` 目录**内部的文件格式**——那是每个 agent 作者的自由
- 本 ADR 不破坏 ADR-0003 稳定性宪章：没有修改现有公共 API，没有修改现有 tool 合同，只是为未来 additive API 预留路径
- 本 ADR 是 ADR-0004"文件即协议"哲学的延伸：**不同性质的文件归不同的协议子空间**，避免用途混淆

---

## References

- [ADR-0003](./ADR-0003-stability-charter.md) — 稳定性宪章
- [ADR-0004](./ADR-0004-time-is-filesystem.md) — 时间由文件系统提供
- [MIGRATION-0.6](../docs/MIGRATION-0.6.md) §0 — 人视角 ≠ Agent 视角
