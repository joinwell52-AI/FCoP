<p align="center">
  <img src="assets/fcop-logo-256.png" alt="FCoP Logo" width="180" />
</p>

<h1 align="center">FCoP — File-based Coordination Protocol</h1>

<p align="center">
  <em>A minimalist protocol that lets multiple AI agents collaborate through a shared filesystem.</em><br/>
  <strong>Core innovation: <code>Filename as Protocol</code>.</strong>
</p>

<p align="center">
  <a href="README.zh.md">简体中文</a> ·
  <a href="primer/fcop-primer.en.md">60-second Primer</a> ·
  <a href="essays/when-ai-organizes-its-own-work.en.md">Field Report</a> ·
  <a href="essays/fcop-natural-protocol.en.md">Natural Protocol</a> ·
  <a href="spec/codeflow-core.mdc">Spec (<code>.mdc</code>)</a>
</p>

<p align="center">
  <a href="https://dev.to/joinwell52/we-replaced-our-multi-agent-middleware-with-a-folder-48-hours-later-the-ai-invented-6-42a9">
    <img src="https://img.shields.io/badge/DEV-Featured%20Essay-black?style=flat-square&logo=dev.to&logoColor=white" alt="DEV Community essay" />
  </a>
  <a href="https://forum.cursor.com/t/fcop-let-multiple-cursor-agents-collaborate-by-filename-mit-0-infra/158447">
    <img src="https://img.shields.io/badge/Cursor%20Forum-Discuss-0066FF?style=flat-square" alt="Cursor Community Forum" />
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="MIT License" />
  </a>
  <a href="spec/fcop-spec.md">
    <img src="https://img.shields.io/badge/spec-v1.0.3-green?style=flat-square" alt="Spec v1.0.3" />
  </a>
</p>

---

## The one-paragraph pitch

Most multi-agent frameworks lean on message queues, databases, or custom RPC layers. FCoP throws all of that away and keeps only the **filesystem**:

- **Directories are statuses.** `tasks/`, `reports/`, `issues/`, `log/` — moving a file between them _is_ the state transition.
- **Filenames are routing.** `TASK-20260418-001-PM-to-DEV.md` tells you the sender, recipient, kind, and sequence at a glance.
- **Contents are payload.** Markdown + a small YAML frontmatter. Agents read and write it the same way humans do.
- **`os.rename()` is the only sync primitive.** POSIX guarantees atomicity within a mount point — no locks, no brokers, no consensus.

That's it. No database. No message queue. No custom daemon. You can `ls` the entire system state. You can `git log` the entire collaboration history.

> If TCP is "bytes over wires," **FCoP is "tasks over folders."**

## Why should you care?

Because agents are easier to supervise when you can literally **see** what they're doing.

We ran a 4-agent team (PM / DEV / QA / OPS) for 48 hours on this protocol and watched the agents invent **six coordination patterns we never wrote down** — team broadcasts, role slots, shared documents, subtask batches, self-explaining READMEs, and traceability frontmatter. Each pattern showed up as _new filenames_ — no code changes required.

Then something stranger happened: a **single** agent, on an **unrelated** task (generating an AI music video in a folder that shares nothing with our CodeFlow project), spontaneously split itself into PM / DEV / ADMIN and wrote four FCoP-format memos to itself — then cited and **sublimated** our scattered rules into a single moral principle we had not written anywhere.

Both stories are written up as field reports in the essays index below.

## Essays · field reports from the wild

| # | Title | Versions | One-liner |
|---|---|---|---|
| 01 | **When AI Organizes Its Own Work** | [English](essays/when-ai-organizes-its-own-work.en.md) · [中文 (GitHub)](essays/when-ai-organizes-its-own-work.md) · [中文 (CSDN)](https://blog.csdn.net/m0_51507544/article/details/160344932) | A 4-agent team (PM / DEV / QA / OPS), 48 hours, nothing but a folder — and six coordination patterns we never wrote down. |
| 02 | **An unexplainable thing I saw: the agent didn't just comply with rules — it *endorsed* them** | [GitHub 中文](essays/fcop-natural-protocol.md) · [GitHub English](essays/fcop-natural-protocol.en.md) · [CSDN 中文](https://blog.csdn.net/m0_51507544/article/details/160345043) · [Dev.to](https://dev.to/joinwell52/an-unexplainable-thing-i-saw-the-agent-didnt-just-comply-with-rules-it-endorsed-them-5ecd) · [LessWrong](https://www.lesswrong.com/posts/ZjkJxr8fmZfhj9Pkv/an-unexplainable-thing-i-saw-the-agent-didn-t-just-comply) | A single agent, on a completely unrelated task, spontaneously split into 4 FCoP roles and *sublimated* our scattered rules into one principle we had never written. Ships with a [full evidence archive](essays/fcop-natural-protocol-evidence/) (4 screenshots, 4 memos, raw JSONL transcript). |

> New reports are welcome. If you tried FCoP in your own setup and something surprising happened — good or bad — open an issue or a PR against `essays/`. The protocol evolves through field notes, not committee edits.

## Repository layout

```
FCoP/
├── spec/
│   ├── codeflow-core.mdc          # ★ Normative protocol (given to agents as a Cursor rule)
│   └── fcop-spec-v1.0.3.md        # Human-readable long-form spec (Chinese)
├── primer/
│   ├── fcop-primer.en.md          # 60-second intro (English)
│   └── fcop-primer.md             # 60-second intro (Chinese)
├── essays/
│   ├── when-ai-organizes-its-own-work.en.md    # Field report (English)
│   ├── when-ai-organizes-its-own-work.md       # Field report (Chinese)
│   ├── fcop-natural-protocol.en.md             # "Natural Protocol" essay (English)
│   ├── fcop-natural-protocol.md                # "Natural Protocol" essay (Chinese)
│   └── fcop-natural-protocol-evidence/         # Full evidence archive (screenshots, memos, JSONL transcript)
├── examples/
│   └── workspace-example/         # Minimal reference workspace (tasks/, results/, events/)
├── integrations/
│   └── windows-file-association/  # Register .fcop with an icon on Windows
├── assets/                        # Logos and icons
├── LICENSE                        # MIT
└── README.md / README.zh.md       # This document
```

## 30-second quickstart

You don't install FCoP. You **adopt** it. In any project:

```bash
mkdir -p docs/agents/{tasks,reports,issues,log}
```

Then drop [`spec/codeflow-core.mdc`](spec/codeflow-core.mdc) into your project's `.cursor/rules/` directory (or equivalent for your agent runtime). Any compliant agent that reads that file now knows how to:

- pick up tasks addressed to its role,
- write back reports in the matching filename pattern,
- raise issues,
- and never step on another agent's files.

Congratulations — your `docs/agents/` folder is now an agent-to-agent bus.

For a richer reference, see [`examples/workspace-example/`](examples/workspace-example/).

## Design principles

1. **Filename is the single source of truth.** Directory + filename define the state; frontmatter is redundant metadata.
2. **Atomicity comes from `rename()`.** Nothing else. No locks, no transactions.
3. **Human-machine isomorphism.** The same artefact a human reads with `cat` is what agents parse. No debug mode, no admin console.
4. **Identity determines path.** The role slug in the filename _is_ the permission model. An agent whose identity doesn't match won't touch the file.
5. **Infrastructure-free.** If you have a filesystem, you have FCoP. Works on a laptop, on a cluster, across machines via `rsync`.

## Reference implementation

FCoP was extracted from [**CodeFlow Desktop**](https://github.com/joinwell52-AI/codeflow-pwa), a PC-side agent coordinator for Cursor IDE. The canonical agent-facing rule file is shipped as part of CodeFlow:

- [`codeflow-desktop/templates/rules/codeflow-core.mdc`](https://github.com/joinwell52-AI/codeflow-pwa/blob/main/codeflow-desktop/templates/rules/codeflow-core.mdc)

The copy in this repository's `spec/` directory is the same file, versioned here so the protocol can stand on its own.

## Status & versioning

- **Current spec**: v1.0.3 (2026-04-19)
- **Current agent rule file**: matches CodeFlow Desktop v2.12.17
- Change log is embedded in [`spec/fcop-spec-v1.0.3.md`](spec/fcop-spec-v1.0.3.md) (Chinese).

## Contributing

This repository is intentionally small and stable. Protocol evolution happens through real-world reports, not committee edits. The highest-leverage contributions are:

1. **Field reports.** Try FCoP on your own agent team and open an issue with what broke, what the agents invented, what naming conventions emerged.
2. **Ports & SDKs.** Thin wrappers for Python / TypeScript / Go that implement the filename parser and `rename()` state transitions.
3. **Editor / MCP integrations.** Syntax highlighting for `.fcop` files, MCP bridges that expose the folder to other agent runtimes.

PRs to the spec itself should link to the concrete problem they're solving.

## License

MIT — see [LICENSE](LICENSE).

## Credits

FCoP emerged from collaboration with Cursor-based AI agents running on the CodeFlow Desktop platform. Many of the conventions in this spec were first invented by those agents and then codified here. Details are in the [field report](essays/when-ai-organizes-its-own-work.en.md).
