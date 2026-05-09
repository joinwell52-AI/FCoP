# FCoP Primer · 60 秒搞懂 FCoP

> **FCoP = File-based Coordination Protocol**
> 一种让多个 AI agent 通过**文件系统**协作的极简协议。
> *Core innovation: **Filename as Protocol** · 文件名即协议。*

---

## 一张图看完

```
共享目录                          文件名即路由
docs/agents/                      TASK-{date}-{seq}-{sender}-to-{recipient}.md
├── tasks/      ← 待办              │   │        │    │         │
├── reports/    ← 回执              │   │        │    │         └─ 收件人 (DEV / TEAM / DEV.D1 / assignee.D1)
├── issues/     ← 问题              │   │        │    └─ 发件人
├── shared/     ← 常驻文档           │   │        └─ 序号
└── log/        ← 归档               │   └─ 日期
                                    └─ 类型 (TASK / REPORT / ISSUE / SPRINT / DASHBOARD / …)
```

**目录名 = 状态 (Status)** · **文件名 = 路由 (Routing)** · **文件内容 = 载荷 (Payload)**

---

## 一个最小例子

Alice（角色 PM）要派活给 Bob（角色 DEV）：

1. Alice 在 `docs/agents/tasks/` 里写一个文件：

   ```
   TASK-20260419-001-PM-to-DEV.md
   ```

   内容（Markdown + YAML frontmatter）：

   ```markdown
   ---
   protocol: agent_bridge
   version: 1
   kind: task
   sender: PM
   recipient: DEV
   priority: P1
   ---

   # 给首页加黑暗模式切换

   ## 背景 ...
   ## 验收标准 ...
   ```

2. Bob 定期扫描自己的信箱：

   ```python
   tasks_dir.rglob("*-to-DEV*.md")   # 只读发给 DEV 的文件
   ```

3. Bob 完成后，在 `docs/agents/reports/` 里写回执：

   ```
   TASK-20260419-001-DEV-to-PM.md
   ```

**就这样。** 没有数据库，没有 WebSocket，没有消息队列。Alice 和 Bob 甚至不需要同时在线。

---

## FCoP 做了哪些设计决定

| 设计 | 原因 |
|---|---|
| **文件名即路由** | 不用解析 header，`glob` 一行完事；人和 agent 看的是同一套寻址方案 |
| **目录即状态** | `tasks/` → 待办，`reports/` → 已回，`log/` → 归档，`ls` 一下就是管理面板 |
| **Markdown + YAML frontmatter** | 所有 LLM 天生会读写；人类也能直接看 |
| **`rename` 即原子提交** | POSIX 原子操作，不需要分布式锁 |
| **角色写进文件名** | Agent 物理上只能读到发给自己的文件，进化自然有序 |
| **核心协议 ≤ 200 行 Markdown** | 协议本身就是 `.cursorrules`，可直接灌进任何 LLM 的系统提示 |

---

## FCoP 不解决什么

诚实地说：

- **毫秒级低延迟** —— 基于文件系统的协议有秒级延迟，**不适合高频交易、实时控制**
- **强一致的事务** —— 没有多文件事务，需要事务语义请自己在内容层处理
- **超大规模** —— 单项目百万级文件时扫描会慢，建议按日期/批次分子目录
- **强 schema 校验** —— 协议默认鼓励开放 frontmatter，强类型需要自己加 linter

**FCoP 专长**：10–100 个 agent、秒级到分钟级协作周期、需要人类随时插手 review / 审计的场景。

---

## 收件人的 4 种写法

```
to-DEV               # 单点投递
to-TEAM              # 广播给全队（除发件人）
to-DEV.D1            # 具名角色的某个槽位
to-assignee.D1       # 匿名槽位，谁接谁填
```

**槽位分隔符只用 `.`**（点号），因为角色名可能带 `-`（如 `AUTO-TESTER`、`LEAD-QA`）。

---

## 为什么叫 "Human-Machine Isomorphism / 人机同构"

大多数 agent 协作协议（JSON-RPC、gRPC、事件总线）是**纯 Agent 导向**的。系统出问题时，人类必须额外装一套 UI（Kibana、Grafana、MQ 管理页）才能看见发生了什么。

FCoP 反过来——**同一份磁盘上的同一份文件**，对 Agent 是状态机，对人类是文件夹：

| 同一份 `TASK-20260419-001-PM-to-DEV.md` | |
|---|---|
| 对 Agent | 目录=Status · 文件名=Routing · `os.rename`=原子锁 |
| 对人类 | 一个资源管理器里直接能看见、能拖动、能 grep 的文件 |

**UI 层和协议层从"两层"折叠成了"一层"。**

这让 FCoP 具备一个主流 agent 协议少有的能力——**可观测性就是可用性**。你不需要先变成运维工程师，才能当管理员。

---

## 想现场看 FCoP 跑起来？

**两条路，任选一条：**

### A. 只想看协议本身（不装任何软件）

1. 克隆本 FCoP 主仓（或任何已在用 FCoP 的项目）
2. 浏览 [`examples/workspace-example/`](../examples/workspace-example/) 里的真实文件——任务、回执、common docs 全是纯 Markdown
3. 读成对规范：[`fcop-rules.mdc`](../src/fcop/rules/_data/fcop-rules.mdc)（总则）+ [`fcop-protocol.mdc`](../src/fcop/rules/_data/fcop-protocol.mdc)（解释）

这就够你理解 FCoP 了——协议本身就是**几条命名约定加一个目录结构**，看真实样本比读文档快。

### B. 想让 Cursor 里的 agent 按 FCoP 协作

1. 把 [`fcop-rules.mdc`](../src/fcop/rules/_data/fcop-rules.mdc) 与 [`fcop-protocol.mdc`](../src/fcop/rules/_data/fcop-protocol.mdc) 复制到你项目的 `.cursor/rules/` 下
2. 在项目里建好 `docs/agents/{tasks,reports,issues,shared,log}/` 五个目录
3. 给每个 agent 一个角色名（在 Cursor 的 chat 里告诉它："You are DEV, read `*-to-DEV*.md`"）
4. 丢一个任务文件进 `tasks/`，观察 agent 的反应

**不需要任何中间件。** FCoP 的全部运行时就是 `open()` / `rename()` / `glob()`。

### C.（可选）用 IDE / 自建宿主做自动化

若还需要手机发单、远程触发、看板等能力，可自建调度层或使用任意与 FCoP 文件层对接的工具；**协议层**不绑定某一桌面产品。需要 MCP 式集成时可参考本仓 [`mcp/README.md`](../mcp/README.md)。

---

## 继续阅读 · Further Reading

| 文档 | 内容 |
|---|---|
| [`when-ai-organizes-its-own-work.md`](../essays/when-ai-organizes-its-own-work.md) | 长文田野笔记：48 小时内 AI 自发发明 6 种协作模式的完整记录 |
| [`fcop-rules.mdc`](../src/fcop/rules/_data/fcop-rules.mdc) + [`fcop-protocol.mdc`](../src/fcop/rules/_data/fcop-protocol.mdc) | 给 Agent 的成对规范（总则 + 解释） |
| [FCoP on GitHub](https://github.com/joinwell52-AI/FCoP) | FCoP 协议主仓 |

---

## FAQ

**Q：FCoP 和 MCP (Model Context Protocol) 是什么关系？**
A：两者正交。MCP 是 agent 和工具之间的调用协议；FCoP 是 agent 和 agent 之间的通信协议。你完全可以在 FCoP 任务里调用 MCP 工具，也完全可以在没有 MCP 的环境里（比如纯 ChatGPT）手动执行 FCoP。

**Q：文件名冲突怎么办？**
A：靠 `{date}-{seq}`（日期 + 递增序号）保证唯一；多 agent 并发时靠 `os.rename` 的原子性先到先得。

**Q：能跨机器 / 跨项目吗？**
A：可以。最简单的是用 rsync / Syncthing / Dropbox 同步 `docs/agents/` 目录；严肃一点可以直接让整个项目用 git 托管，`git pull` + `git push` 就是同步机制。

**Q：为什么不用 JSON-RPC / gRPC / MQ？**
A：它们都是**纯 Agent 导向**的协议，人类看不见也改不动。FCoP 的整个设计目标是让人和 agent 看到同一个世界——这是前面说的"人机同构"。

**Q：协议会变吗？**
A：核心部分（文件名语法、frontmatter 必填字段）稳定后不会动。外围词汇（shared 里的前缀、自定义 kind）完全开放，欢迎你的 agent 发明新的——好的会被收编进规范。

---

*FCoP 协议以本仓库为家：[joinwell52-AI/FCoP](https://github.com/joinwell52-AI/FCoP) · MIT。欢迎 fork、批评、改进、贡献田野观察。*
