# Getting Started · 上手 FCoP

> **FCoP** = **F**ile-based **Co**ordination **P**rotocol —— the **AI OS protocol layer**.
>
> 「FCoP 是 agent 的协议，我们发现了他，而不是发明；而正好人类可以读懂。」
> — [ADR-0015 §FCoP is discovered, not invented](../adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md#fcop-is-discovered-not-invented)

本文是 **L0 + L1 唯一入口** —— 30 秒搞懂 FCoP 是什么 + 5 分钟在你机器上跑起来。读完本文不需要再翻其他文档；想深入再去 [`spec/`](../spec/) / [`adr/`](../adr/) / [`essays/`](../essays/)。

---

## 30 秒：FCoP 是什么

**FCoP 是 AI OS 栈中的协议层** —— 与 Linux 的 POSIX、容器生态的 OCI、Kubernetes 的 CRD 同一位置。它定义 agent 之间通过**共享文件系统**协作的契约：

```
┌─────────────────────────────────────────────────────────┐
│  Application       CodeFlow / Cursor / Claude Desktop   │  ← 业务产品
├─────────────────────────────────────────────────────────┤
│  Host Adapter      fcop-mcp / fcop-cli / @fcop/claude   │  ← libc 的位置
├─────────────────────────────────────────────────────────┤
│ ★ FCoP Protocol ★  Agent / IPC / Encoding / Event /     │  ← POSIX 的位置
│                    Failure / Boundary / Audit           │     这就是 FCoP
├─────────────────────────────────────────────────────────┤
│  Reference Impl    fcop (Python lib)                    │  ← 协议参考实现
├─────────────────────────────────────────────────────────┤
│  Kernel Primitives LLM API / Filesystem / Process Mgr   │  ← AI OS 内核
└─────────────────────────────────────────────────────────┘
```

带 ★ 那一条线就是 FCoP。**不是 application、不是 kernel、不是某个 host 的 SDK** —— 是 agent 协作时**自然涌现**的协议规约，被我们形式化为机器可读的 spec。

人能读懂是**副作用**：substrate 恰好是 filesystem + Markdown，所以你打开 VSCode 就能直接看到 agent 在干啥。但 FCoP 不是为人设计的——是为 agent 设计的，人**白看**。

---

## FCoP 比传统协议大在哪：两个 Encoding Surface

FCoP 的 Encoding 有**两面**（这是 [ADR-0021](../adr/ADR-0021-encoding-abstraction.md) 的核心）：

### Surface 1 · IPC Surface（强 contract）

4 类 envelope，由 spec 预定义、filename 严格、frontmatter 必填：

| 类型 | 文件名前缀 | 用途 |
|---|---|---|
| **TASK** | `TASK-{date}-{seq}-{from}-to-{to}.md` | 派活 |
| **REPORT** | `REPORT-{date}-{seq}-{from}-to-{to}.md` | 回执（worker 自报状态）|
| **ISSUE** | `ISSUE-{date}-{seq}-{from}.md` | 阻塞 / 反思 |
| **REVIEW** | `REVIEW-{date}-{seq}-{from}-on-{subject}.md` | 外审决议（v1.0 新加）|

类比 POSIX 的 pipes / message queues —— 强结构化、有明确 sender→recipient。

### Surface 2 · Open Knowledge Surface（弱 contract）

agent 在 `shared/` 里**自由发明**的命名学。spec 只规定 filename 形式 `{ALL-CAPS-PREFIX}-{kebab-slug}[.{lang}].md`；**PREFIX 由 agent 自创，FCoP spec 不枚举**。

真实 FCoP 项目里观察到的 agent invention：

| 前缀 | 含义 |
|---|---|
| `GUIDE-{topic}.md` | 操作指南、how-to |
| `SPEC-{topic}.md` | 团队规约 |
| `STATUS-{actor}-{topic}-RECORD.md` | 跨任务的状态账本 |
| `TEAM-{aspect}.md` | 团队层文档（README / ROLES / OPERATING-RULES） |
| `LETTER-TO-{recipient}.md` | 跨 session 的开放交流 |

**这些没有一个在 spec 里被定义**——是 agent 在 FCoP 文件名 grammar 的精神下**长出来的**。类比 POSIX 的 shared memory / `/usr/share/` —— 弱结构化、留白命名学。

这一面是 FCoP 比传统 message protocol（JSON-RPC / gRPC / MQ）更有生命力的地方：协议留白让 agent 自由发明子语言。

---

## 5 分钟：跑起来

### Step 1 · 安装

```bash
pipx install fcop-mcp        # 装 host adapter (含 fcop 库依赖)
# 或者只装库（不需要 MCP 时）：
# pipx install fcop
```

PyPI 包族（[ADR-0015 §术语表](../adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md#%E6%9C%AF%E8%AF%AD%E8%A1%A8v10-%E6%B0%B8%E4%B9%85%E5%86%BB%E7%BB%93)）：

| 包 | 角色 | 必装 |
|---|---|---|
| `fcop` | Reference Implementation | ✅ |
| `fcop-mcp` | Host Adapter for Cursor / 任意 MCP 宿主 | ✅（用 Cursor / Claude Desktop 时） |
| `fcop-cli`（v1.x 候选）| Host Adapter for 命令行 | ⏳ |

### Step 2 · 在项目根 init

```bash
cd your-project
fcop init                    # 创建 fcop/ 命名空间
```

得到的目录结构（v1.0 默认）：

```
your-project/
└── fcop/                          ← v1.0 协议命名空间
    ├── fcop.json                  ← 团队 / 角色配置
    ├── tasks/                     ← TASK-* 落这里
    ├── reports/                   ← REPORT-* 落这里
    ├── issues/                    ← ISSUE-* 落这里
    ├── reviews/                   ← REVIEW-* 落这里（v1.0 新加）
    ├── shared/                    ← Open Knowledge Surface — agent 自由发明
    └── log/                       ← 归档（已完成的 TASK / REPORT 移到这里）
```

> **从 0.7.x 升级？** 旧项目的 `docs/agents/` 会被 detect 到，触发 warning。运行 `fcop migrate-workspace --apply` 一键迁移到 `fcop/`（git mv 保留历史）。详见 [ADR-0022](../adr/ADR-0022-workspace-directory-convention.md)。

### Step 3 · 写第一个 TASK

`fcop/tasks/TASK-20260601-001-PM-to-DEV.md`：

```markdown
---
protocol: fcop
version: 1
sender: PM
recipient: DEV
priority: P1
subject: 给首页加黑暗模式切换
---

## 背景
...

## 验收标准
- [ ] 切换按钮在 header 右上
- [ ] localStorage 持久化
```

### Step 4 · agent 接活并回执

DEV 角色 agent 扫自己的信箱：

```python
from fcop import Project

project = Project(".")              # 默认读 fcop/
my_inbox = project.inbox(role="DEV")
for task in my_inbox:
    print(task.subject)             # 「给首页加黑暗模式切换」
    # ... 干活 ...
    project.write_report(
        task=task,
        status="done",
        body="实现完成，commit abc1234"
    )
```

REPORT 自动落到 `fcop/reports/REPORT-20260601-001-DEV-to-PM.md`。

### Step 5 · 在 shared/ 自由发明

发现需要写一份**跨多个 task 的指南**？直接发明：

```bash
fcop/shared/GUIDE-dark-mode-implementation-notes.md
```

这是 Open Knowledge Surface —— **没人教 agent 用 `GUIDE-` 前缀**，但 agent 会自己发明类似命名（field evidence 见 [ADR-0021](../adr/ADR-0021-encoding-abstraction.md)）。你的项目里 agent 可能发明 `MEMO-` / `RECIPE-` / `ARCHIVE-` 等；都合法。

---

## 7 核心抽象一览

[ADR-0015 charter](../adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md) 把 FCoP 协议本体定义为 7 个抽象（POSIX 类比）：

| FCoP 抽象 | POSIX 类比 | 落地 ADR |
|---|---|---|
| **Agent**（Lifecycle + 身份） | Process | [ADR-0020](../adr/ADR-0020-agent-boundary-and-capability.md) |
| **Encoding**（IPC + Open Knowledge）| Filesystem | [ADR-0021](../adr/ADR-0021-encoding-abstraction.md) |
| **IPC**（4 类 envelope） | pipes / MQ | [ADR-0017](../adr/ADR-0017-review-file-type-minimal.md) + 现有 |
| **Event Model** | signals | [ADR-0018](../adr/ADR-0018-event-model.md) |
| **Failure & Recovery** | errno | [ADR-0019](../adr/ADR-0019-failure-and-recovery-semantics.md) |
| **Boundary**（can / cannot） | permissions | [ADR-0020](../adr/ADR-0020-agent-boundary-and-capability.md) |
| **Audit**（REVIEW） | syslog | [ADR-0017](../adr/ADR-0017-review-file-type-minimal.md) |

每个抽象由独立 ADR 收口；协议级 schema 在 [`spec/schemas/`](../spec/schemas/)。

---

## FCoP 不解决什么

诚实交底：

- **毫秒级低延迟** — 文件系统协议有秒级延迟，**不适合**高频交易、实时控制
- **强一致事务** — 没有多文件事务；需要事务语义请在内容层处理
- **百万级文件单仓** — 单项目超大规模时扫描会慢，建议按日期 / 批次分子目录
- **完整 AI OS** — FCoP 只是协议层，**不**包含 Kernel（Task Scheduler / Event Loop / State Machine 是 reference impl 的事）、**不**包含 Application（CodeFlow 等）

**FCoP 专长**：10–100 个 agent、秒级到分钟级协作周期、需要人类随时插手 review / audit 的场景。

---

## 协议规范权威来源（按抽象层级）

| 层 | 文件 | 角色 |
|---|---|---|
| L0 + L1 入口 | [`docs/getting-started.md`](./getting-started.md)（本文）| 30 秒 + 5 分钟 |
| L2 长文规范 | [`spec/fcop-runtime-protocol-v1.0.md`](../spec/)（v1.0 ship 时上线）| 完整 spec |
| L2 给 agent 读的规则（Cursor） | [`.cursor/rules/fcop-rules.mdc`](../.cursor/rules/fcop-rules.mdc) + [`fcop-protocol.mdc`](../.cursor/rules/fcop-protocol.mdc) | Cursor 宿主，`alwaysApply: true` |
| L2 给 agent 读的规则（其他宿主） | [`AGENTS.md`](../AGENTS.md) / [`CLAUDE.md`](../CLAUDE.md) | Codex / Claude Code / Devin / 通用 SDK |
| L2 机器可读 schema | [`spec/schemas/*.schema.json`](../spec/schemas/)（v1.0 ship 时上线）| JSON Schema × 7 抽象 |
| L3 故事 | [`essays/`](../essays/) | 现场报告与随笔 |
| 决策史 | [`adr/`](../adr/)（含 ADR-0001..0022） | 为什么这么做 |

> **`src/fcop/rules/_data/` 是规则的唯一来源（canonical source）。** `deploy_protocol_rules()`（或 MCP `redeploy_rules()`）将其同步到：`.cursor/rules/*.mdc`（Cursor 宿主）以及 `AGENTS.md` / `CLAUDE.md`（其他宿主）。详见 [ADR-0006](../adr/ADR-0006-host-neutral-rule-distribution.md)。

---

## 进一步阅读

- **协议哲学**：[ADR-0015 §FCoP is discovered, not invented](../adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md#fcop-is-discovered-not-invented)
- **现场报告**：[`essays/when-ai-organizes-its-own-work.md`](../essays/when-ai-organizes-its-own-work.md) — 48 小时内 AI 自发发明 6 种协作模式
- **agent 自留笔记**：[`docs/tutorials/`](./tutorials/) — 教程 + agent 真实落盘的 TASK/REPORT 片段
- **GitHub 仓**：<https://github.com/joinwell52-AI/FCoP>

---

## FAQ

**Q：FCoP 和 MCP 是什么关系？**
A：正交。MCP 是 agent ↔ 工具的调用协议；FCoP 是 agent ↔ agent 的通信协议。可以叠加用（fcop-mcp 就是用 MCP 把 FCoP 协议工具暴露给 Cursor）。

**Q：能跨机器 / 跨项目吗？**
A：可以。最简单是用 git / Syncthing / Dropbox 同步 `fcop/` 目录；严肃一点直接让整个项目用 git，`git pull/push` 就是同步机制。

**Q：协议会变吗？**
A：v1.0 起进入"AI OS Protocol Layer"稳定承诺——MAJOR (1.x→2.x) 才允许 breaking + 至少 6 个月共存 + 官方迁移脚本；MINOR 只允许 additive；PATCH 绝对零行为变化。详见 [ADR-0003](../adr/ADR-0003-stability-charter.md) + [ADR-0015 §冻结 #4](../adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md)。

**Q：为什么不用 JSON-RPC / gRPC / MQ？**
A：它们是**纯 agent 导向**的协议，人类看不见也改不动。FCoP 的 substrate 是 filesystem + Markdown —— 人和 agent 看到同一个世界。这是 essay 里说的「人机同构」。

**Q：shared/ 里 agent 想发明前缀，要先报备吗？**
A：**不要。** 这是 Open Knowledge Surface 的核心约束——spec 不枚举词表，agent 想发明就发明（只要遵守 `{ALL-CAPS-PREFIX}-{kebab-slug}.md` grammar）。如果你看到一个新前缀觉得有意思，可以在 release notes 的 §observed agent inventions 段记一笔，但不进 spec。

---

[English version](./getting-started.en.md)
