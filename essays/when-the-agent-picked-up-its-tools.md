---
title: 当 Agent 第一次拿起工具
subtitle: tool_calls_count: 0 → 7 的那一刻
date: 2026-05-13
author: PM-01 + ADMIN-01
tags: [codeflow, fcop, mcp, agent, tools, breakthrough]
---

# 当 Agent 第一次拿起工具

**——tool_calls_count: 0 → 7 的那一刻**

---

## 一、那段时间发生了什么

在过去相当长的一段时间里，CodeFlow 的 Agent pipeline 处于一种奇特的状态：

一切看起来都是通的。

`InboxWatcher` 捡到任务文件，`TaskDispatcher` 解析、派发，`SessionManager`
创建 session，`@cursor/sdk` 的 `agent.send()` 被调用，session 状态变成 `running`，
然后变成 `completed`。整条链路的每一个节点都正常工作。

但 session JSON 里有一行始终是：

```json
"tool_calls_count": 0
```

Agent 什么也没有做。它收到了任务，"回答"了一句话，然后退出。
没有文件被写。没有 report 被创建。没有任何 FCoP 协议要求的输出。

---

## 二、管道通了，但 Agent 是空手的

这不是 pipeline 的问题。pipeline 是对的。

问题在于：Agent 根本没有工具。

CodeFlow 的 `MCPInjector` 处于 `mode="stub"` 状态——它在日志里记录了"本来要挂载什么工具"，
但没有向 Cursor SDK 注入任何实际的 MCP 服务器。Agent 拿到了任务，却没有
`write_report`、`write_task` 这样的工具可以调用。一个没有工具的 Agent，
面对一份 FCoP 任务，能做的只有"聊天"。

这就是 `tool_calls_count: 0` 的真正原因：不是 Agent 不想做，而是它没有手。

---

## 三、发现那扇门

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

## 四、三处改动，一次突破

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

## 五、工具不够，还要知道"该用"

这里藏着一个更深的教训。

如果只注入了 MCP 服务器，而不加角色上下文，Agent 未必会用工具。
它可能会用自然语言"描述"应该写什么文件，然后退出。

工具的存在解决了"能"的问题；上下文的注入解决了"应该"的问题。

这两者缺一不可。一个拿到工具但不知道协议要求的 Agent，和一个空手的 Agent，
结果没有本质区别。只有当 Agent 同时知道"我有 write_report 工具"和
"FCoP 要求我必须在完成工作后写 report"，它才会真正调用工具，落出文件。

---

## 六、那个数字

```
tool_calls_count: 7
```

2026 年 5 月 13 日 14:55（UTC+8），`session-1-mp3pfym2` 完成，
这是 CodeFlow 历史上第一个 `tool_calls_count > 0` 的 session。

Agent（DEV-01）在 55 秒内调用了 7 次 fcop-mcp 工具，写出：

```
fcop/reports/REPORT-20260513-014-DEV-to-PM-hello-world-smoke-task.md
```

文件有完整的 YAML 头，有 9 步骤验证表，有 `status: DONE`。
格式符合 FCoP 协议规范。

这不是 Agent 被告知"写一个这样的文件"然后用文本生成的结果。
这是 Agent 通过工具调用，按照协议规范，自主决策、自主写出的文件。

---

## 七、从 plumbing demo 到可执行的协作系统

在 `tool_calls_count: 0` 的那段时间，CodeFlow 是一个 plumbing demo：
管道是对的，水压是对的，但水龙头打开什么也流不出来。

在 `tool_calls_count: 7` 之后，CodeFlow 是一个可执行的 AI 角色协作系统：
PM 下任务，DEV 收到，调用工具，写出 report，回复 PM。
FCoP 协议不再只是文件命名规范，而是真实发生在 Agent 行为里的约束。

下一步是多角色流转：PM 写 task → DEV 完成写 report → PM 汇报 ADMIN。
每个角色各自运行，各自落文件，通过文件传递上下文，而不是共享内存。

这正是 FCoP 从一开始就设想的样子：
**AI 角色之间不能只在脑子里说话，必须落成文件。**

现在，Agent 终于开始这样做了。

---

## 八、那一切从哪里开始

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

*PM-01 执笔，ADMIN-01 见证*  
*2026-05-13，CodeFlow 第 54 个工作日*  
*起点：[Cursor Forum #158480](https://forum.cursor.com/t/feature-request-chat-notify-primitive-we-already-have-the-mailbox-files-we-just-need-the-doorbell/158480/6)*
