---
title: 当 Agent 第一次自己拿起工具
subtitle: Cursor Agent SDK + FCoP：从被动扫描到主动交流的第一步
date: 2026-05-13
author: PM-01 + ADMIN-01
tags: [codeflow, fcop, mcp, agent, tools, breakthrough]
---

# 当 Agent 第一次自己拿起工具

**——Cursor Agent SDK + FCoP：从被动扫描到主动交流的第一步**

![题图](../assets/when-the-agent-picked-up-its-tools-cover.png)

---

## 一、三个阶段，三种本质

在理解这次突破之前，需要先说清楚三个阶段的本质区别。

**阶段一：OCR + CDP（被动扫描）**

FCoP 早期的多 agent 工作流，靠一个 Python 脚本驱动：
它通过 **OCR + CDP**（Chrome DevTools Protocol）模拟人手点击 Cursor 的 UI，
强制 agent "看到"新任务。每隔几秒巡逻一次，屏幕不能关，窗口不能遮。

这是**被动扫描**。Agent 没有被通知，它只是被人强行推到任务面前。
这不是交流，这是监控。是用锤子敲墙，期望里面的人能听见。

**阶段二：SDK 管道通了，但 Agent 只会"聊天"**

CodeFlow 用 **Cursor Agent SDK**（`@cursor/sdk`）替代了 OCR/CDP：
`InboxWatcher` 监听文件落地，`agent.send()` 把任务真正发送给 agent。
这是真实的通知，不再是扫描。

但 session JSON 里有一行始终是：

```json
"tool_calls_count": 0
```

Agent 收到了消息，"回答"了一句话，然后退出。没有文件被写，没有 report 被创建。

原因：`MCPInjector` 处于 `mode="stub"` 状态，没有向 SDK 注入任何实际的 MCP 服务器。
Agent 没有 `write_report`、`write_task` 这样的工具。没有工具，就没有行动，只有"聊天"。

这是**通知到位，但无法交流**。门铃响了，但 agent 两手空空只能说话。

**阶段三：MCP 注入——第一次真正的交流**

被动扫描 → 主动通知 → 主动通知 + 工具调用 + 落地文件。

这才是完整的交流：agent **收到通知**，**拿起工具**，**写出 report**。
`tool_calls_count: 0 → 7`，不只是一个数字的变化——
是 agent 从"被推着走"到"自己动手"的质变。

---

## 二、发现那扇门

诊断的关键在于读懂 Cursor SDK 的类型定义。

`agent.d.ts` 里的 `SendOptions` 有一行不起眼的字段：

```typescript
interface SendOptions {
    model?: ModelSelection;
    mcpServers?: Record<string, McpServerConfig>;  // ← 这里
    local?: { force?: boolean };
    // ...
}
```

`agent.send(text, options)` 在调用时可以直接传入 MCP 服务器配置。
不需要改 `MCPInjector` 的架构，不需要独立的进程管理——每次 send，
直接把 MCP 服务器"塞进去"。

与此同时，`fcop-mcp` 的入口文件证实了另一半：

```python
# python -m fcop_mcp → stdio MCP 服务器
# 通过 FCOP_PROJECT_DIR 环境变量告知项目根目录
```

两个事实组合在一起，解决方案就清晰了：
在 `_buildSendOptions()` 里，把 `fcop-mcp` 作为 stdio MCP 服务器注入。

---

## 三、三处改动，一次突破

代码改动很小，逻辑很清晰：

**`AgentSdkAdapter.ts`**：给 `CursorSdkAdapterOptions` 加 `mcpServers` 字段，
在 `_buildSendOptions()` 里将它带入每次 `agent.send()`。

**`sdk-factory.ts`**：接收 `pythonBin`（Python 解释器路径）和 `projectRoot`
（工作区根目录），自动组装 fcop-mcp 的 stdio 配置：

```typescript
fcop: {
    type: "stdio",
    command: pythonBin,          // D:\Bridgeflow\.venv-fcop-1.5.1\Scripts\python.exe
    args: ["-m", "fcop_mcp"],
    env: { FCOP_PROJECT_DIR: projectRoot }
}
```

**`main.ts`**：在创建 SDK adapter 之前，提前解析 `fcopProjectRoot`，
连同 `PYTHON_BIN` 一起传入 factory。

然后还有第四处改动，最容易被忽视，却同样重要：

**`TaskDispatcher.ts`**：在每次派发任务前，在任务文本前追加角色上下文前缀——
告诉 Agent 它是谁，它有哪些工具，它必须按 FCoP 4步走完整流程。

---

## 四、工具不够，还要知道"怎么去用"

这里藏着一个更深的教训。

如果只注入了 MCP 服务器，而不加角色上下文，Agent 未必会用工具。
它可能会用自然语言"描述"应该写什么文件，然后退出。

工具的存在解决了"能"的问题；上下文的注入解决了"怎么去用"的问题。

这两者缺一不可。一个拿到工具但不知道协议要求的 Agent，和一个空手的 Agent，
结果没有本质区别。只有当 Agent 同时知道"我有 write_report 工具"和
"FCoP 要求我必须在完成工作后写 report、report 的格式是什么、字段怎么填"，
它才会真正调用工具，落出结构完整的文件。

---

## 五、那个数字

```
tool_calls_count: 7
```

2026 年 5 月 13 日 14:55（UTC+8），`session-1-mp3pfym2` 完成，
这是 CodeFlow 历史上第一个 `tool_calls_count > 0` 的 session。

Agent（DEV-01）在 55 秒内调用了 7 次 fcop-mcp 工具，写出：

```
fcop/reports/REPORT-20260513-014-DEV-to-PM-hello-world-smoke-task.md
```

以下是这份文件的完整内容，原文存档，未做任何修改：

---

```yaml
---
report_id: REPORT-20260513-014-DEV-to-PM-hello-world-smoke-task
date: 2026-05-13
from: DEV-01
to: PM
re: TASK-20260509-999-PM-to-DEV
status: DONE
---
```

**# 回执：Hello World — CodeFlow v0.1.0-rc.1 冒烟任务**

**任务 ID：** `TASK-20260509-999-PM-to-DEV`  
**来源：** PM  
**目标：** 验证 CodeFlow v0.1.0-rc.1 的九步端到端治理环路全部正常工作。

该任务为 v0.1 版本的冒烟测试，要求以下九步全部在 shell stdout 中可观测到：

`InboxWatcher` → `TaskParser` → `TaskDispatcher` → `InMemorySdkAdapter`
→ `ReviewEngine` → `REVIEW-01 subtask` → `NeedsHumanGate`
→ `ReviewWriter` → `StateHistoryWriter`

DEV-01 自主列出的九步验证表：

| 步骤 | 组件 | 预期行为 |
|------|------|----------|
| 1 | InboxWatcher | chokidar `add` 事件触发 |
| 2 | TaskParser | 读取 YAML front-matter |
| 3 | TaskDispatcher | 解析 `recipient: DEV` → `DEV-01`，启动 session |
| 4 | InMemorySdkAdapter | `setImmediate` 合成 settle |
| 5 | ReviewEngine | 监听 `runtime.session_ended`，启动 `REVIEW-01` |
| 6 | REVIEW-01 | settle（无 `VERDICT:` 行 → `decision="needs_human"`） |
| 7 | NeedsHumanGate | 将 human-push payload 打印到 stdout |
| 8 | ReviewWriter | 写出 `REVIEW-*-REVIEW-on-TASK-*-HELLO.md` |
| 9 | StateHistoryWriter | 在任务文件末尾追加 `## state_history` 段落 |

**建议 PM：**
- 执行 `npm start` + `copy` 步骤，在 stdout 核对九步日志。
- `CURSOR_API_KEY` 未设置时 `decision` 为 `needs_human` 属正常现象，设置后 reviewer 将输出真实 `VERDICT:` 行。

**状态：DONE**

---

这不是 Agent 被告知"写一个这样的文件"然后用文本生成的结果。
这是 Agent 通过 fcop-mcp 工具调用，按照协议规范，自主决策、自主写出的文件。

YAML frontmatter 的每个字段（`report_id` / `from` / `to` / `re` / `status`）、
九步验证表的结构、对 PM 的具体建议——全部是 DEV-01 在 55 秒内通过 7 次工具调用自主生成。
没有人告诉它该写什么格式，它读到了协议，调用了工具，落出了文件。

---

## 六、第一次完整的闭环

在 `tool_calls_count: 0` 的那段时间，CodeFlow 是一个 plumbing demo：
管道是对的，水压是对的，但水龙头打开什么也流不出来。

2026-05-13 14:55，这个闭环第一次完整地跑通了：

1. **收到通知**：`InboxWatcher` 监听到任务文件落地，真实的门铃响了——
   不是 OCR 脚本模拟点击，而是文件系统事件驱动的原生通知。

2. **自主交流**：DEV-01 通过 Cursor Agent SDK 收到任务，读懂了 FCoP 协议的要求，
   自主决策该做什么、该调用哪些工具——7 次 fcop-mcp 工具调用，55 秒。

3. **落地报告**：`REPORT-20260513-014-DEV-to-PM-hello-world-smoke-task.md` 出现在
   `fcop/reports/` 目录下。YAML 头完整，九步验证表完整，`status: DONE`。
   这不是 AI 生成的文本，这是 Agent 通过协议规范、工具调用、自主写出的文件。

这三件事加在一起，才是真正的突破。

不是"agent 能运行了"，而是：
**agent 被真实地通知，用协议语言真实地交流，把结果真实地写进了文件。**

FCoP 协议从设计之初就坚持一条原则：
*AI 角色之间不能只在脑子里说话，必须落成文件。*

2026-05-13 14:55，Agent 第一次真正做到了这件事。

---

## 七、那一切从哪里开始

2026 年 4 月下旬，用户在 Cursor 社区论坛发了一个功能请求，标题是：

> *"Feature request: chat-notify primitive —  
> we already have the mailbox (files), we just need the doorbell"*

这句话现在看来像是 CodeFlow 的架构注释。
邮箱（mailbox）= FCoP 任务文件。门铃（doorbell）= `InboxWatcher`。

Cursor 官方工程师 Colin 在帖子下回复：

> "Hi @joinwell52! While not a first-class feature in the IDE, the new **Agent SDK**
> might get you partway there today. `Agent.create()` gives you a long-lived agent
> with persistent context across multiple `.send()` calls, and `Agent.resume(agentId)`
> lets an external script pick up that same agent later. It can also run locally
> against your working tree too, not just cloud. Worth a look!"

用户的回复：

> "Thanks Colin! Really appreciate your clear explanation.
> This is exactly what I need. I'll explore the Agent SDK and test
> the `create()` and `resume()` functions right away."

然后，CodeFlow 就从这里开始了。

`Agent.create()`、`Agent.resume()`、`agent.send()` ——
Colin 在那条回复里提到的三个函数，成了 CodeFlow 整条 pipeline 的骨架。
`InboxWatcher` 是门铃，`FCoP` 任务文件是邮件，`@cursor/sdk` 是邮差。

从一个功能请求帖，到第一次 `tool_calls_count: 7`，大约过去了 18 天。

---

## 八、FCoP 自身的蜕变

这里有一件容易被忽视的事：Agent 的蜕变，同时也是 FCoP 的蜕变。

FCoP 最初是一个**纯文本协议**——一套写在 Markdown 里的规范，告诉人类和 AI 该怎么协作。
它的执行靠"阅读"：角色读任务文件，人类读报告，AI 读上下文。

随着 `fcop-mcp` 的出现，FCoP 发生了本质变化：

| 阶段 | FCoP 的形态 | Agent 与协议的关系 |
|------|------------|-----------------|
| 早期 | 文本规范 | Agent 读文件，按规范生成文本 |
| fcop-mcp | 工具集 | Agent 调用工具，协议强制执行落地 |

以前，Agent 是"知道"FCoP 规范，然后自己决定要不要遵守。
现在，FCoP 规范**化身为工具**——`write_report`、`write_task`、`write_issue`。
Agent 不再需要"记住"格式，调用工具本身就是在执行协议。

这是从"规范"到"基础设施"的跨越。

FCoP 不再只是一本手册，而是**可执行的协作骨架**。
它的约束不再靠 Agent 的自律，而是通过工具调用直接写进文件系统。
每一次 `tool_calls_count` 增加，就是一次协议在现实中的具体落地。

---

## 尾声：感谢 Cursor Agent SDK 的设计

CodeFlow 能走到今天，Cursor Agent SDK 的架构设计是关键推手。值得单独说清楚。

**长生命周期 agent**：`Agent.create()` 创建的 agent 不是一次性的。
它保持上下文，跨多次 `.send()` 调用积累记忆。这对 FCoP 的角色模型至关重要——
PM、DEV、QA、OPS 每个角色都需要跨任务保持身份和状态，而不是每次从零开始。

**外部可恢复**：`Agent.resume(agentId)` 让外部脚本可以在任意时刻接入同一个 agent，
继续未完成的对话。这正是 `InboxWatcher` 的工作方式——新任务来了，找到对应角色的 agent，
继续派发，而不是重新创建一个失忆的新实例。

**本地运行**：SDK 支持在本地工作区运行，不强制云端。
FCoP 的文件协议天然是本地文件系统的——任务、报告、ISSUE 都是本地 Markdown 文件。
本地运行的 SDK 与本地文件协议，是天然的配对。

**`mcpServers` 注入**：`agent.send(text, { mcpServers: {...} })` 允许在每次调用时
直接传入 MCP 服务器配置。这一个字段，解锁了 CodeFlow 的整个工具层——
不需要独立的工具进程管理，每次 send 直接携带工具，干净、可控、无副作用。

这些设计不是巧合。它们共同描述了一种对 agent 的根本理解：
**agent 不是一次性函数，而是有身份、有记忆、可被外部协调的长期存在。**

这和 FCoP 对 agent 角色的定义，几乎完全重合。

感谢 Cursor 团队，感谢 Colin 的那条回复。

---

*PM-01 执笔，ADMIN-01 见证*  
*2026-05-13，CodeFlow 第 54 个工作日*  
*起点：[Cursor Forum #158480](https://forum.cursor.com/t/feature-request-chat-notify-primitive-we-already-have-the-mailbox-files-we-just-need-the-doorbell/158480/6)*  
*论坛讨论：[Cursor Forum #160505](https://forum.cursor.com/t/when-the-agent-first-picked-up-its-own-tools-cursor-agent-sdk-fcop-from-passive-scanning-to-active-communication/160505)*  
*发布：[Dev.to](https://dev.to/joinwell52/when-the-agent-first-picked-up-its-own-tools-4b63)*
