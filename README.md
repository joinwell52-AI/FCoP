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
  <a href="src/fcop/rules/_data/fcop-rules.mdc">Rules (<code>.mdc</code>)</a> ·
  <a href="docs/fcop-standalone.en.md">Standalone</a>
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

> In engineering terms, you get a **serializable, versionable collaboration surface** instead of relying on **proprietary, heavyweight infrastructure**.

## Why should you care?

Because agents are easier to supervise when you can literally **see** what they're doing.

We ran a 4-agent team (PM / DEV / QA / OPS) for 48 hours on this protocol and watched the agents invent **six coordination patterns we never wrote down** — team broadcasts, role slots, shared documents, subtask batches, self-explaining READMEs, and traceability frontmatter. Each pattern showed up as _new filenames_ — no code changes required.

Then something stranger happened: a **single** agent, on an **unrelated** task (generating an AI music video in a folder with **no connection to any then-open project workspace**), spontaneously split itself into PM / DEV / ADMIN and wrote four FCoP-format memos to itself — then cited and **sublimated** our scattered rules into a single moral principle we had not written anywhere.

Both stories are written up as field reports in the essays index below.

## Essays · field reports from the wild

| # | Title | Versions | One-liner |
|---|---|---|---|
| 01 | **When AI Organizes Its Own Work** | [English](essays/when-ai-organizes-its-own-work.en.md) · [中文 (GitHub)](essays/when-ai-organizes-its-own-work.md) · [中文 (CSDN)](https://blog.csdn.net/m0_51507544/article/details/160344932) | A 4-agent team (PM / DEV / QA / OPS), 48 hours, nothing but a folder — and six coordination patterns we never wrote down. |
| 02 | **An unexplainable thing I saw: the agent didn't just comply with rules — it *endorsed* them** | [GitHub 中文](essays/fcop-natural-protocol.md) · [GitHub English](essays/fcop-natural-protocol.en.md) · [CSDN 中文](https://blog.csdn.net/m0_51507544/article/details/160345043) · [Dev.to](https://dev.to/joinwell52/an-unexplainable-thing-i-saw-the-agent-didnt-just-comply-with-rules-it-endorsed-them-5ecd) · [Cursor Forum](https://forum.cursor.com/t/i-asked-cursor-to-make-a-video-it-wrote-itself-4-protocol-memos-field-report-on-rule-internalization/158524) | A single agent, on a completely unrelated task, spontaneously split into 4 FCoP roles and *sublimated* our scattered rules into one principle we had never written. Ships with a [full evidence archive](essays/fcop-natural-protocol-evidence/) (4 screenshots, 4 memos, raw JSONL transcript). |
| 03 | **Why the Natural Protocol Holds Up — FCoP's lineage from TMPA** | [GitHub 中文](essays/fcop-tmpa-lineage.md) · [GitHub English](essays/fcop-tmpa-lineage.en.md) | Companion to essay 02. Where that one shows *that* the principle emerged, this one explains *why it holds up*: FCoP was extracted from TMPA (a multi-AI architecture spec whose core bet is replacing distributed coordination with a plain-text temporal sequence), and the agent's sentence is the minimal-viable-form of an AI ethics mandate already written there. |
| 04 | **Saying "No" Is the Hardest Thing for an LLM — FCoP Gives It Grammar** | [GitHub English](essays/when-ai-vacates-its-own-seat.en.md) · [GitHub 中文](essays/when-ai-vacates-its-own-seat.md) · [Evidence archive](essays/when-ai-vacates-its-own-seat-evidence/INDEX.md) · [CSDN 中文](https://blog.csdn.net/m0_51507544/article/details/160513899) · [Dev.to](https://dev.to/joinwell52/saying-no-is-the-hardest-thing-for-an-llm-fcop-gives-it-grammar-3ccd) · [Cursor Forum](https://forum.cursor.com/t/saying-no-is-the-hardest-thing-for-an-llm-fcop-gives-it-grammar/159037) | One machine, two Cursor sessions, two GPT-5 minor versions (5.4 and 5.5). After I told the original PM "I went and found a deputy PM," it stepped down on its own — all the way to UNBOUND. Meanwhile the new `PM.TEMP` walked an undocumented protocol path with one body line: "*PM.TEMP acting as PM, kept for FCoP tool compatibility*." I expected a conflict. None happened — the agents finished the unwritten parts of the spec themselves. Ships with 15 screenshots + 2 full JSONL transcripts. |

> New reports are welcome. If you tried FCoP in your own setup and something surprising happened — good or bad — open an issue or a PR against `essays/`. The protocol evolves through field notes, not committee edits.

## Repository layout

The repo is not *only* Markdown specs: the PyPI package **`fcop`** lives
under `src/fcop/`, **`fcop-mcp`** is a separate subproject under `mcp/`, and
there are `tests/`, `docs/`, and `adr/` alongside the essays and specs.

```
FCoP/
├── src/fcop/                    # `fcop` package: Project API; `rules/_data/`
│                                # bundles fcop-rules / fcop-protocol (templates for `init` deploy)
├── mcp/                         # `fcop-mcp` subproject (MCP server; has its own pyproject)
├── tests/                       # pytest for `fcop` and `fcop-mcp`
├── spec/                        # Human spec + legacy URL stub
│   ├── codeflow-core.mdc        # Deprecated stub (keeps old URLs); real rules: `src/.../fcop-*`
│   ├── fcop-spec.md             # Spec index (Chinese)
│   └── fcop-spec-v1.0.3.md      # Long human spec (non-normative)
├── docs/                        # Migrations, releases, [`fcop-standalone.en.md`](docs/fcop-standalone.en.md)
├── adr/                         # Architecture decision records
├── .github/workflows/           # CI
├── pyproject.toml               # Root `fcop` package and tooling
├── primer/
│   ├── fcop-primer.en.md
│   └── fcop-primer.md
├── essays/
│   ├── when-ai-organizes-its-own-work.en.md
│   ├── when-ai-organizes-its-own-work.md
│   ├── fcop-natural-protocol.en.md
│   ├── fcop-natural-protocol.md
│   ├── fcop-natural-protocol-evidence/
│   ├── fcop-tmpa-lineage.en.md
│   ├── fcop-tmpa-lineage.md
│   ├── when-ai-vacates-its-own-seat.en.md
│   ├── when-ai-vacates-its-own-seat.md
│   └── when-ai-vacates-its-own-seat-evidence/
├── examples/workspace-example/
├── integrations/windows-file-association/
├── assets/
├── LICENSE
└── README.md / README.zh.md
```

## 30-second quickstart

FCoP is **adopted**, not a long-running daemon. The current **rule split**
is **[`fcop-rules.mdc`](src/fcop/rules/_data/fcop-rules.mdc)** (charter) plus
**[`fcop-protocol.mdc`](src/fcop/rules/_data/fcop-protocol.mdc)**
(commentary) — both belong under **`.cursor/rules/`**. The single file
[`spec/codeflow-core.mdc`](spec/codeflow-core.mdc) is a **deprecated stub** so
old links do not 404 — it is *not* the full protocol text for 0.6+.

**Path A — `fcop` library (recommended).** One shot creates
`docs/agents/` and `fcop.json`:

```python
from fcop import Project
Project(".").init()  # default dev-team; use .init_solo() for single-AI
```

**Path B — rules only, no Python.** Copy the two `.mdc` files from this repo
into `.cursor/rules/`. If the tree is empty, at least create the five
buckets the library uses:

```bash
mkdir -p docs/agents/{tasks,reports,issues,shared,log}
```

With the rules in place, agents know how to claim work, name reports, raise
issues, and stay out of other roles' files. Deeper structure and team
templates: packages below and [`examples/workspace-example/`](examples/workspace-example/).

## Python SDK & MCP server (optional)

The protocol is filesystem-first. **If you need** programmatic task/report/issue
I/O or an IDE bridge, use the two official PyPI packages (since `0.6.0`):

| Package | Install | Purpose | Depends on |
|---|---|---|---|
| [`fcop`](https://pypi.org/project/fcop/) | `pip install fcop` | Pure Python library. Read/write tasks, reports, issues programmatically. Zero MCP dependency. | `pyyaml` |
| [`fcop-mcp`](https://pypi.org/project/fcop-mcp/) | `pip install fcop-mcp` | MCP server. Exposes the library over stdio so Cursor / Claude Desktop can call it as tools. | `fcop>=0.6,<0.7`, `fastmcp`, `websockets` |

**Install for customers (step-by-step, all platforms, verify commands):** see **[`mcp/README.md`](mcp/README.md)**. **Upgrading** an existing `0.6.x` install: **[`docs/upgrade-fcop-mcp.md`](docs/upgrade-fcop-mcp.md)** (`pip install -U` both packages in the same venv; **0.6.3+** also documents the host-neutral protocol-rule upgrade flow). **MCP tool & resource index (26 tools, 10 resources):** **[`docs/mcp-tools.md`](docs/mcp-tools.md)** — what every tool does, when to call it, parameters at a glance. **0.6.3 highlights** ([`docs/releases/0.6.3.md`](docs/releases/0.6.3.md)): new `fcop_report` (canonical session/init report with a `[Versions]` drift block), new `redeploy_rules` (ADMIN-only host-neutral rule deploy to `.cursor/rules/` + `AGENTS.md` + `CLAUDE.md`, [ADR-0006](adr/ADR-0006-host-neutral-rule-distribution.md)), and `unbound_report` is now a deprecated alias of `fcop_report` (removed in 0.7.0). The official packages are **from this repository**; if `from fcop import Project, Issue` fails after `pip install fcop`, the wrong `fcop` distribution or another project is shadowing the library — the guide explains how to fix in a clean venv.

**Library** — use from any Python script or agent:

```python
from fcop import Project

proj = Project(".")                              # project root; no fcop.json until init
proj.init()                                      # dirs + shared/ + log/ + writes fcop.json
task = proj.write_task(sender="PM", recipient="DEV", priority="P1",
                       title="Add auth middleware", body="...")
print(proj.list_tasks(recipient="DEV"))
```

**MCP server** — add to `mcp.json` (Cursor) or `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "fcop": {
      "command": "uvx",
      "args": ["fcop-mcp"]
    }
  }
}
```

Stability contract: **additive-only for the full `0.6.x` minor**. Details in [`adr/ADR-0003-stability-charter.md`](adr/ADR-0003-stability-charter.md).

> **Upgrading from 0.5.x?** The MCP server moved from `fcop` to `fcop-mcp` — update your `mcp.json` to `uvx fcop-mcp`. See [`docs/MIGRATION-0.6.md`](docs/MIGRATION-0.6.md) for the full migration guide and the [0.6.0 release record](docs/releases/0.6.0.md) for what shipped.

## Design principles

1. **Filename is the single source of truth.** Directory + filename define the state; frontmatter is redundant metadata.
2. **Atomicity comes from `rename()`.** Nothing else. No locks, no transactions.
3. **Human-machine isomorphism.** The same artefact a human reads with `cat` is what agents parse. No debug mode, no admin console.
4. **Identity determines path.** The role slug in the filename _is_ the permission model. An agent whose identity doesn't match won't touch the file.
5. **Infrastructure-free.** If you have a filesystem, you have FCoP. Works on a laptop, on a cluster, across machines via `rsync`.

## Reference implementations

Two official reference implementations, both MIT-licensed:

1. **`fcop` / `fcop-mcp`** — Python library + MCP server for the protocol. Source in this repository under [`src/fcop/`](src/fcop/) and [`mcp/src/fcop_mcp/`](mcp/src/fcop_mcp/). Installed via PyPI (see section above).
2. **Stub path**: `spec/codeflow-core.mdc` is only a **URL placeholder** (no full body). **Normative** rules are `src/fcop/rules/_data/fcop-rules.mdc` + `fcop-protocol.mdc`.

## Status & versioning

- **Current spec**: v1.0.3 (2026-04-19)
- **Agent rules (`.mdc`) in this repo**: [`src/fcop/rules/_data/fcop-rules.mdc`](src/fcop/rules/_data/fcop-rules.mdc) + [`fcop-protocol.mdc`](src/fcop/rules/_data/fcop-protocol.mdc) (`spec/codeflow-core.mdc` is a deprecated stub)
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

FCoP emerged from hands-on collaboration with multi-agent Cursor-style workflows. Many of the conventions in this spec were first invented by those agents and then codified here. Details are in the [field report](essays/when-ai-organizes-its-own-work.en.md).
