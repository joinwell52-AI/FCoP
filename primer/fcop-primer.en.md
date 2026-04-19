# FCoP Primer · 60-Second Introduction

> **FCoP = File-based Coordination Protocol**
> A minimalist protocol that lets multiple AI agents collaborate through a **shared filesystem**.
> *Core innovation: **Filename as Protocol**.*

---

## One Picture, Whole Protocol

```
Shared directory                  Filename as routing
docs/agents/                      TASK-{date}-{seq}-{sender}-to-{recipient}.md
├── tasks/      ← pending          │   │        │    │         │
├── reports/    ← completed        │   │        │    │         └─ Recipient (DEV / TEAM / DEV.D1 / assignee.D1)
├── issues/     ← problems         │   │        │    └─ Sender
├── shared/     ← standing docs    │   │        └─ Sequence
└── log/        ← archive          │   └─ Date
                                   └─ Kind (TASK / REPORT / ISSUE / SPRINT / DASHBOARD / …)
```

**Directory = Status** · **Filename = Routing** · **File content = Payload**

---

## A Minimal Example

Alice (role: PM) wants to assign work to Bob (role: DEV):

1. Alice writes a file in `docs/agents/tasks/`:

   ```
   TASK-20260419-001-PM-to-DEV.md
   ```

   Content (Markdown + YAML frontmatter):

   ```markdown
   ---
   protocol: agent_bridge
   version: 1
   kind: task
   sender: PM
   recipient: DEV
   priority: P1
   ---

   # Add a dark mode toggle to the home page

   ## Background ...
   ## Acceptance criteria ...
   ```

2. Bob scans his own inbox periodically:

   ```python
   tasks_dir.rglob("*-to-DEV*.md")   # only read files addressed to DEV
   ```

3. When done, Bob writes a reply in `docs/agents/reports/`:

   ```
   TASK-20260419-001-DEV-to-PM.md
   ```

**That's it.** No database, no WebSocket, no message queue. Alice and Bob don't even need to be online at the same time.

---

## The Design Decisions FCoP Made

| Decision | Why |
|---|---|
| **Filename is routing** | No header parsing, a single `glob` does the job; humans and agents look at the same addressing surface |
| **Directory is status** | `tasks/` → pending, `reports/` → done, `log/` → archived. A bare `ls` is the admin panel. |
| **Markdown + YAML frontmatter** | Every LLM can read/write these natively; humans can too |
| **`rename` is the atomic commit** | POSIX atomic operation, no distributed lock required |
| **Roles live in the filename** | Agents can physically only read what's addressed to them — evolution stays orderly |
| **Core protocol ≤ 200 lines of Markdown** | The protocol itself is a `.cursorrules` file — pastable into any LLM system prompt |

---

## What FCoP Is NOT For

Being honest:

- **Millisecond latency** — a filesystem-based protocol has second-level latency. **Not suitable for high-frequency trading or realtime control.**
- **Strict transactional consistency** — no multi-file transactions. If you need transaction semantics, handle it in the content layer.
- **Huge scale** — when a single project hits millions of files, `glob` gets slow. Shard into date/batch subdirectories.
- **Strong schema validation** — FCoP encourages open frontmatter by default. If you want strong typing, add a linter yourself.

**FCoP's sweet spot**: 10–100 agents, collaboration cycles of seconds to minutes, scenarios where humans need to be able to review / audit / intervene at any time.

---

## The 4 Forms of Recipient

```
to-DEV               # Direct, single role
to-TEAM              # Broadcast to everyone except the sender
to-DEV.D1            # A specific slot within a named role
to-assignee.D1       # Anonymous slot, assignee TBD
```

**The slot separator is always `.`** (a dot), because role names may themselves contain `-` (e.g. `AUTO-TESTER`, `LEAD-QA`).

---

## Why We Call It "Human-Machine Isomorphism"

Most agent-to-agent coordination protocols (JSON-RPC, gRPC, event buses) are **agent-only** by design. When something breaks, humans need an entirely separate UI stack (Kibana, Grafana, an MQ admin page) to see what's happening.

FCoP flips this. **The same file on the same disk** is a state machine for agents and a folder for humans:

| One file: `TASK-20260419-001-PM-to-DEV.md` | |
|---|---|
| To an agent | Directory = Status · Filename = Routing · `os.rename` = atomic lock |
| To a human | A file you can see, drag, grep — right inside your file manager |

**The UI layer and the protocol layer collapse from "two layers" into "one layer."**

This gives FCoP a rare property in the multi-agent world: **observability IS usability**. You don't need to become a site-reliability engineer before you can be a project manager.

---

## Want to See FCoP Running?

**Two paths, pick one:**

### A. Just read the protocol (install nothing)

1. Clone the CodeFlow repo (or any project already using FCoP).
2. Browse [`examples/workspace-example/`](../examples/workspace-example/) — tasks, reports, standing docs. All plain Markdown.
3. Read the spec: [`spec/codeflow-core.mdc`](../spec/codeflow-core.mdc) (~160 lines).

That's enough to understand FCoP. The protocol is a handful of naming conventions plus one directory layout — reading real samples is faster than reading a spec.

### B. Make your Cursor agents talk via FCoP

1. Drop [`codeflow-core.mdc`](../spec/codeflow-core.mdc) into your project's `.cursor/rules/`.
2. Create the five directories: `docs/agents/{tasks,reports,issues,shared,log}/`.
3. Tell each agent its role in the Cursor chat: "You are DEV. Read `*-to-DEV*.md`."
4. Drop a task file into `tasks/` and watch what they do.

**No middleware required.** FCoP's entire runtime is `open()` / `rename()` / `glob()`.

### C. (Optional) Automate it with CodeFlow Desktop

If you want to send tasks from your phone, auto-wake Cursor agents, and see live status on a web panel — use the CodeFlow desktop app. Download the platform binary from the [releases page](https://github.com/joinwell52-AI/codeflow-pwa/releases).

---

## Further Reading

| Document | What's inside |
|---|---|
| [`when-ai-organizes-its-own-work.en.md`](../essays/when-ai-organizes-its-own-work.en.md) | Long-form field note: how AI agents self-invented six coordination patterns in 48 hours |
| [`spec/codeflow-core.mdc`](../spec/codeflow-core.mdc) | The spec itself (pastable into any LLM) · FCoP v2.12.17 |
| [FCoP on GitHub](https://github.com/joinwell52-AI/FCoP) | FCoP protocol main repo |

---

## FAQ

**Q: How does FCoP relate to MCP (Model Context Protocol)?**
A: They're orthogonal. MCP is an agent-to-tool protocol. FCoP is an agent-to-agent protocol. You can call MCP tools from inside an FCoP task; you can also run FCoP in environments without MCP (e.g. a plain ChatGPT chat that writes files manually).

**Q: What about filename collisions?**
A: `{date}-{seq}` (date plus monotonic sequence) guarantees uniqueness. Under concurrent agents, `os.rename` atomicity enforces first-to-claim semantics.

**Q: Can it go cross-machine or cross-project?**
A: Yes. The simplest option is syncing `docs/agents/` with rsync / Syncthing / Dropbox. For serious use, just put the whole project under git — `git pull` and `git push` become the synchronization mechanism.

**Q: Why not JSON-RPC / gRPC / MQ?**
A: They're **agent-only** protocols — humans can neither see nor edit their state. The entire point of FCoP is making humans and agents see the same world. That's the "Human-Machine Isomorphism" above.

**Q: Will the protocol change?**
A: The core (filename grammar, required frontmatter fields) is stable once ratified. The periphery (prefixes under `shared/`, custom `kind` values) stays open — your agents are welcome to invent new ones. The good ones get folded back into the spec.

---

*FCoP is the core protocol of the [CodeFlow](https://github.com/joinwell52-AI/FCoP) project, MIT-licensed. Forks, critiques, improvements, and field notes are all welcome.*
