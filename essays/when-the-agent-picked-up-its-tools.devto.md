---
title: When the Agent First Picked Up Its Own Tools
published: true
description: "tool_calls_count 0 to 7 - how injecting fcop-mcp into the Cursor Agent SDK turned a passive file-scanner into an agent that receives notifications, calls tools, and files its own reports."
tags: ai, agents, cursor, mcp
cover_image: https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/assets/when-the-agent-picked-up-its-tools-devto-cover.png
canonical_url: https://github.com/joinwell52-AI/FCoP/blob/main/essays/when-the-agent-picked-up-its-tools.en.md
---

*Cursor Agent SDK + FCoP: From Passive Scanning to Active Communication*

> This is a follow-up to a [Cursor Forum feature request](https://forum.cursor.com/t/feature-request-chat-notify-primitive-we-already-have-the-mailbox-files-we-just-need-the-doorbell/158480) I posted in late April 2026: *"we already have the mailbox (files), we just need the doorbell."* Colin recommended the Agent SDK. We built CodeFlow on top of it. This is what happened 18 days later.

---

## I. Three stages — three fundamentally different things

**Stage One: OCR + CDP (passive scanning)**

FCoP's early multi-agent workflow ran on a Python script that used **OCR + CDP** (Chrome DevTools Protocol) to simulate human clicks on the Cursor UI, forcing agents to "see" new tasks. It polled every few seconds. The screen had to stay on. The window couldn't be obscured.

This was **passive scanning**. The agent wasn't notified — it was pushed in front of a task by brute force. This wasn't communication. It was surveillance.

**Stage Two: The SDK pipe worked — but the agent could only "chat"**

CodeFlow replaced OCR/CDP with the **Cursor Agent SDK** (`@cursor/sdk`): `InboxWatcher` watches for files landing, `agent.send()` delivers tasks directly to the agent. Real notification. No more scanning.

But one line in every session JSON stayed the same:

```json
"tool_calls_count": 0
```

The agent received the message, "replied" with something, and exited. No files written. No reports created.

The reason: `MCPInjector` was in `mode="stub"` — no actual MCP server was injected into the SDK. The agent had no `write_report`, no `write_task`. No tools means no action. Only chat.

The doorbell rang. The agent answered with empty hands.

**Stage Three: MCP injection — the first real communication**

Passive scanning → real notification → real notification + tool calls + filed report.

`tool_calls_count: 0 → 7` is not just a number changing — it's the qualitative shift from "being pushed along" to "acting on its own."

---

## II. Finding the door

The key was reading the Cursor SDK type definitions.

In `agent.d.ts`, `SendOptions` had an easily-overlooked field:

```typescript
interface SendOptions {
    model?: ModelSelection;
    mcpServers?: Record<string, McpServerConfig>;  // ← here
    local?: { force?: boolean };
    // ...
}
```

`agent.send(text, options)` can receive MCP server configuration at call time. No need to refactor anything. Every send, just pass the MCP server config directly.

At the same time, `fcop-mcp`'s entry point confirmed the other half:

```python
# python -m fcop_mcp → stdio MCP server
# uses FCOP_PROJECT_DIR environment variable to locate the project root
```

Solution: in `_buildSendOptions()`, inject `fcop-mcp` as a stdio MCP server.

---

## III. Three changes, one breakthrough

**`AgentSdkAdapter.ts`**: Add `mcpServers` to `CursorSdkAdapterOptions`; pass it into every `agent.send()` call.

**`sdk-factory.ts`**: Automatically assemble the fcop-mcp stdio configuration:

```typescript
fcop: {
    type: "stdio",
    command: pythonBin,
    args: ["-m", "fcop_mcp"],
    env: { FCOP_PROJECT_DIR: projectRoot }
}
```

**`main.ts`**: Resolve `fcopProjectRoot` before building the SDK adapter.

And a fourth change — the easiest to overlook, and equally important:

**`TaskDispatcher.ts`**: Before each task dispatch, prepend a role context header to the task text — telling the agent who it is, what tools it has, and that it *must* follow the FCoP 4-step workflow to completion.

---

## IV. Tools aren't enough — you also need to know *how* to use them

If you inject the MCP server but add no role context, the agent might not use the tools. It might *describe* what files should be written, in natural language, and then exit.

Tool injection solves the "can" problem. Context injection solves the "how" problem — what format, what fields, what protocol.

Only when the agent simultaneously knows "I have a `write_report` tool" *and* "FCoP requires me to write a report after completing work — and here's the exact format and fields" will it actually call the tool and produce a properly structured file.

---

## V. That number

```
tool_calls_count: 7
```

On May 13, 2026, at 14:55 UTC+8, `session-1-mp3pfym2` completed — the first session in CodeFlow's history with `tool_calls_count > 0`.

The agent (DEV-01) called fcop-mcp tools 7 times in 55 seconds and wrote:

```
fcop/reports/REPORT-20260513-014-DEV-to-PM-hello-world-smoke-task.md
```

Below is the complete content of that file, archived verbatim, unmodified:

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

**Receipt: Hello World — CodeFlow v0.1.0-rc.1 Smoke Task**

**Task ID:** `TASK-20260509-999-PM-to-DEV`
**Goal:** Verify that CodeFlow v0.1.0-rc.1's nine-step end-to-end governance loop works correctly.

DEV-01's self-constructed nine-step verification table:

| Step | Component | Expected Behavior |
|------|-----------|-------------------|
| 1 | InboxWatcher | chokidar `add` event fires |
| 2 | TaskParser | reads YAML front-matter |
| 3 | TaskDispatcher | resolves `recipient: DEV` → `DEV-01`, starts session |
| 4 | InMemorySdkAdapter | `setImmediate` synthetic settle |
| 5 | ReviewEngine | listens for `runtime.session_ended`, starts `REVIEW-01` |
| 6 | REVIEW-01 | settles (no `VERDICT:` line → `decision="needs_human"`) |
| 7 | NeedsHumanGate | prints human-push payload to stdout |
| 8 | ReviewWriter | writes `REVIEW-*-REVIEW-on-TASK-*-HELLO.md` |
| 9 | StateHistoryWriter | appends `## state_history` section to task file |

**Status: DONE**

---

No one told it what format to use. It read the protocol, called the tools, and wrote the file.

---

## VI. The first complete cycle

Three things happened together for the first time:

1. **Notification received**: `InboxWatcher` detected the task file landing — a real doorbell, not an OCR script simulating a click.

2. **Autonomous communication**: DEV-01 received the task via the Cursor Agent SDK, understood what FCoP protocol required, and autonomously decided what to do and which tools to call. 7 fcop-mcp tool calls. 55 seconds.

3. **Report filed**: A complete, protocol-compliant Markdown file appeared in `fcop/reports/`. Not AI-generated text — a file written autonomously by an agent through protocol-driven tool calls.

Not "the agent can run now." But: **the agent was genuinely notified, genuinely communicated in protocol language, and genuinely wrote the result into a file.**

---

## VII. Where it all started

In late April 2026, I posted a feature request on the Cursor Forum:

> *"Feature request: chat-notify primitive — we already have the mailbox (files), we just need the doorbell"*

Colin replied:

> "Hi @joinwell52! While not a first-class feature in the IDE, the new **Agent SDK** might get you partway there today. `Agent.create()` gives you a long-lived agent with persistent context across multiple `.send()` calls, and `Agent.resume(agentId)` lets an external script pick up that same agent later. It can also run locally against your working tree too, not just cloud. Worth a look!"

`Agent.create()`, `Agent.resume()`, `agent.send()` — those three functions became the skeleton of CodeFlow's entire pipeline. `InboxWatcher` is the doorbell, FCoP task files are the mail, `@cursor/sdk` is the postal service.

From a feature-request post to the first `tool_calls_count: 7`: approximately 18 days.

---

## VIII. FCoP's own transformation

As the agent transformed, so did FCoP.

FCoP began as a **pure text protocol** — conventions written in Markdown. Its enforcement relied on *reading*. With `fcop-mcp`, FCoP underwent a fundamental change:

| Stage | FCoP's form | Agent's relationship to the protocol |
|-------|-------------|--------------------------------------|
| Early | Text specification | Agent reads files, generates text per convention |
| fcop-mcp | Tool set | Agent calls tools; protocol is enforced at write time |

Before, agents *knew* the FCoP spec and decided whether to follow it. Now, the FCoP spec **becomes the tools** — `write_report`, `write_task`, `write_issue`. Calling the tool *is* executing the protocol.

This is the leap from **specification** to **infrastructure**.

---

## Epilogue: Thank you, Cursor Agent SDK

**Long-lived agents**: `Agent.create()` maintains context across multiple `.send()` calls. PM, DEV, QA, OPS each carry their identity and state across tasks.

**External resumability**: `Agent.resume(agentId)` lets `InboxWatcher` re-enter the same agent when a new task arrives. No amnesia, no cold starts.

**Local execution**: The SDK runs against your local working tree. FCoP's file protocol is inherently local — a natural match.

**`mcpServers` injection**: `agent.send(text, { mcpServers: {...} })` accepts MCP server configuration at call time. This single field unlocked CodeFlow's entire tool layer.

Together these design choices describe something fundamental: **An agent is not a one-shot function. It's a long-lived entity with identity, memory, and the capacity to be coordinated by external systems.**

That's almost exactly how FCoP defines an agent role.

Thank you to the Cursor team. Thank you, Colin, for that reply.

---

**Related**

- [FCoP on GitHub](https://github.com/joinwell52-AI/FCoP) — Protocol spec, source, and all essays
- [Full essay (GitHub)](https://github.com/joinwell52-AI/FCoP/blob/main/essays/when-the-agent-picked-up-its-tools.en.md)
- [Cursor Forum discussion](https://forum.cursor.com/t/when-the-agent-first-picked-up-its-own-tools-cursor-agent-sdk-fcop-from-passive-scanning-to-active-communication/160505)
- [When Agents Learn From Their Own Wreckage](https://dev.to/joinwell52/when-agents-learn-from-their-own-wreckage-45p2) — A field report from the same project

*FCoP Maintainers · May 13, 2026*
