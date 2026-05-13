<p align="center">
  <img src="assets/fcop-logo-256.png" alt="FCoP Logo" width="180" />
</p>

<h1 align="center">FCoP — File-based Coordination Protocol</h1>

<p align="center">
  <em>The <strong>AI Agent behavior governance protocol</strong> — the runtime contract for agent collaboration on a shared filesystem.</em><br/>
  <strong>Core invariant: <code>Filename as Protocol</code>. Folders are the message bus.</strong>
</p>

<p align="center">
  <strong><a href="https://joinwell52-ai.github.io/FCoP/">🌐 Project homepage</a></strong> ·
  <a href="README.zh.md">简体中文</a> ·
  <a href="docs/getting-started.en.md">Getting started</a> ·
  <a href="docs/mcp-tools.md"><strong>MCP Tools (35)</strong></a> ·
  <a href="essays/when-ai-organizes-its-own-work.en.md">Field Report</a> ·
  <a href="essays/fcop-natural-protocol.en.md">Natural Protocol</a> ·
  <a href="src/fcop/rules/_data/fcop-rules.mdc">Rules (<code>.mdc</code>)</a> ·
  <a href="adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md">v1.0 Charter</a>
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
  <a href="spec/fcop-runtime-protocol-v1.0.md">
    <img src="https://img.shields.io/badge/spec-v1.1-green?style=flat-square" alt="Spec v1.1" />
  </a>
  <a href="CHANGELOG.md">
    <img src="https://img.shields.io/badge/release-2.0.0-brightgreen?style=flat-square" alt="2.0.0" />
  </a>
  <a href="https://doi.org/10.5281/zenodo.19886036">
    <img src="https://zenodo.org/badge/DOI/10.5281/zenodo.19886036.svg" alt="DOI 10.5281/zenodo.19886036" />
  </a>
</p>

---

## Where FCoP sits in the stack

FCoP is the **behavior governance protocol layer** for multi-agent collaboration — standardizing how agents report actions, review outcomes, and operate within governed capability boundaries.

```
Application Layer      CodeFlow / Cursor / Claude Desktop      ← business products / agent applications
Host Adapter Layer     fcop-mcp / fcop-cli / @fcop/claude      ← integration adapters / host bridges
★ FCoP Protocol ★      Agent collaboration / reporting /        ← this is FCoP
                       review / capability governance /
                       event semantics / failure boundaries /
                       auditability
Reference Impl         fcop (Python library)                   ← protocol reference implementation
Execution Substrate    LLM APIs / MCP tools / filesystem /     ← execution environment
                       process manager / operating system
```

> **FCoP governs agent behavior, not execution runtime.** — [ADR-0029](adr/ADR-0029-fcop-behavior-governance-charter.md)

v1.0 stabilises the minimum semantic contract for the **seven core concepts** above. Spec is stable; encodings are open: the *IPC Surface* (TASK / REPORT / ISSUE / REVIEW) is strongly typed, while the *Open Knowledge Surface* (`shared/` + `{ALL-CAPS-PREFIX}-{slug}.md`) leaves vocabulary open for agents to invent — see [ADR-0021](adr/ADR-0021-encoding-abstraction.md).

→ **Start here**: [`docs/getting-started.md`](docs/getting-started.md) · [`docs/getting-started.en.md`](docs/getting-started.en.md)

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
| 05 | **Tutorial: From Solo to a 2-Person AI Crew — Disciplining the AI Team with FCoP-MCP** (two parallel case studies) | English (Tetris case): [`tetris-solo-to-duo.en.md`](docs/tutorials/tetris-solo-to-duo.en.md) · [Dev.to](https://dev.to/joinwell52/free-open-source-multi-agent-hands-on-how-to-command-agents-fcop-mcp-brings-discipline-to-1j3j) · [Cursor Forum](https://forum.cursor.com/t/free-open-source-multi-agent-hands-on-how-to-command-agents-fcop-mcp-brings-discipline-to-ai-teams/159329) · 中文译本（俄罗斯方块案例）: [`tetris-solo-to-duo.zh.md`](docs/tutorials/tetris-solo-to-duo.zh.md) · 中文母语原创（贪吃蛇案例）: [`snake-solo-to-duo.zh.md`](docs/tutorials/snake-solo-to-duo.zh.md) · [CSDN 中文版](https://blog.csdn.net/m0_51507544/article/details/160603953) | The first **tutorial-style** entry in this index, shipping as **two parallel case studies — the protocol is the same, the games and the live easter egg are different**. Both are 45-minute hands-on dogfoods: get the agent to install `fcop-mcp` in Cursor, ship a working game in solo mode, switch to a 2-person team where PLANNER designs and CODER implements a creative variant, then read the disk. The **Chinese case** uses Snake → `NEON ORBIT` (original-themed) and captures an actual PLANNER-impersonating-CODER easter egg from the 0.6.x era. The **English case** uses Tetris → `Nebula Stack` (solo) → `Comet Loom` (team), and adds a full **review-and-rework cycle** (ADMIN plays v1, finds 3 blocking defects, bounces it back; PLANNER writes TASK-006 with a new `Verification Requirements` section; CODER ships v2) plus an end-of-day on-the-record interview where both agents are asked what they think of the protocol. 22 dogfood screenshots, 14 TASK/REPORT files, 8 silent role-switch evidence files, 2 game artefacts, 2 verbatim agent transcripts — all archived under [`docs/tutorials/assets/tetris-en/`](docs/tutorials/assets/tetris-en/). |
| 06 | **What the Agents Say About FCoP, When You Ask Them** | [GitHub English](essays/what-agents-say-about-fcop.en.md) · [GitHub 中文](essays/what-agents-say-about-fcop.md) · [Evidence archive (Tetris-en dogfood)](docs/tutorials/assets/tetris-en/) · [CSDN 中文](https://blog.csdn.net/m0_51507544/article/details/160636177) · [Dev.to](https://dev.to/joinwell52/what-the-agents-say-about-fcop-when-you-ask-them-3ajk) · [Cursor Forum](https://forum.cursor.com/t/what-the-agents-say-about-fcop-when-you-ask-them-two-field-interviews-at-the-end-of-an-english-dogfood/159368) | The third class of *"agents endorse FCoP"* evidence, after [essay 02](essays/fcop-natural-protocol.en.md) (**unprompted, off-task**) and [essay 04](essays/when-ai-vacates-its-own-seat.en.md) (**conflict-forced**): now **directly asked**. At the end of the English Tetris dogfood (companion to the row-05 tutorial), both agents (PLANNER and CODER) were asked agent-perspective takes on FCoP — no marketing tone. PLANNER named the RLHF instinct it had to fight ("follow latest instruction") to honour FCoP's role lock and called eight of its own `role-switch` evidence files **true positives**, against its own operational convenience. CODER admitted it had a protocol primitive (`write_issue`) it didn't use, traced the v1 defect to that exact uncovered space, and filed PR-grade product feedback on the protocol. Three different elicitation conditions, the same phenomenon — agents endorse FCoP when given the room to. Also includes a small empirical observation: across the entire 45-minute dogfood, ADMIN's two most-used phrases were **"Start work."** and **"Inspection."** |
| 07 | **当 agent 从自己的残骸中学习** | [GitHub 中文](essays/when-agents-learn-from-their-own-wreckage.md) · [GitHub English](essays/when-agents-learn-from-their-own-wreckage.en.md) · [CSDN 中文](https://blog.csdn.net/m0_51507544/article/details/161028380) · [Dev.to](https://dev.to/joinwell52/when-agents-learn-from-their-own-wreckage-45p2) | codeflow 项目一日 14 个 agent 涌现现场报告（2026-05-12）：USER HOME 全局污染 / GATE 描述自命中 / `supersedes:` 字段现场发明——以及协议如何在零次崩溃的情况下，以小时级速度将它们全部反向吸收。 |
| 08 | **协议为什么短，历史为什么长** | [GitHub 中文](essays/why-the-protocol-stays-short.md) · [GitHub English](essays/why-the-protocol-stays-short.en.md) | 一份给协议维护者的设计哲学答案："这样的涌现会不会没有止境？"——短答：会收敛但不会停。四类涌现的处理路径、三条结构力学为何能让协议骨架不被涌现压垮，以及"协议短是为了让历史能无限长"的底层逻辑。 |
| 09 | **当 validator 撞向自己的镜像** | [GitHub 中文](essays/gate-design-pitfalls-case-studies.md) · [GitHub English](essays/gate-design-pitfalls-case-studies.en.md) | 从 codeflow OPS I-14 看 validator-validates-itself 反模式：GATE 在检查 staged diff 时命中了 GATE 描述本身，几分钟后被 OPS 自纠——这一类陷阱的系统性解剖与"语义化实证"根治姿势，以及它如何成为 `fcop-protocol.mdc §GATE Design Pitfalls` 的源头案例。 |
| 10 | **一行 frontmatter 的旅程** | [GitHub 中文](essays/the-supersedes-field-story.md) · [GitHub English](essays/the-supersedes-field-story.en.md) | `supersedes:` 字段从一次协议两难现场发明到 `ipc-envelope.schema.json` 正式字段的两小时旅程：Rule 5（append-only）+ Rule 6（reciprocity）+ Rule 0.c（truthful）三条规则同时成立时，agent 用一行 YAML 自己解了困局——这条路径展示 FCoP 涌现落地的最低成本姿势。 |
| 11 | **看，但不动手** | [GitHub 中文](essays/looking-without-touching.md) · [GitHub English](essays/looking-without-touching.en.md) · [CSDN 中文](https://blog.csdn.net/m0_51507544/article/details/161028161) | FCoP 三层语义执行链科普：`fcop_audit()` 为什么"只看不改"——L1 检测 / L2 解释 / L3 文档三层把"看见"和"动手"切开，产出 `INSPECTION.md`（建议非命令），执行权留给人。`adr/FCoP-semantic-execution-chain.md` 的科普版。 |
| 12 | **五大 AI 模型眼中的 FCoP** | [GitHub 中文](essays/what-five-ai-models-say-about-fcop.md) · [GitHub English](essays/what-five-ai-models-say-about-fcop.en.md) · [Cursor Forum](https://forum.cursor.com/t/what-5-ai-models-say-about-fcop-from-their-own-agent-perspective-category-showcase/160506) | 把 FCoP 核心文档喂给 ChatGPT / Claude / DeepSeek / Grok / 豆包，只问一个问题："你是 agent，你怎么看这套协议？"——五种截然不同的内部视角（ChatGPT 谈身份合法性、Claude 谈诚实边界、DeepSeek 谈体面生存、Grok 做技术评审、豆包讲设计哲学），以及它们之间最有意思的分歧。 |
| 13 | **Evolution, Reverse Absorption / 演化，反向吸收** | [GitHub 中文](essays/evolution-reverse-absorption.md) · [GitHub English](essays/evolution-reverse-absorption.en.md) | Protocol philosophy 2.0 visual declaration: FCoP graduates from a single execution-chain diagram (essay 11 *Looking, not Touching*) to a **two-diagram era** — adding an evolution-loop diagram (a 7-step semantic evolution loop) plus the companion [ADR-0034](adr/ADR-0034-fcop-internal-external-document-convention.md), which codifies the 4-layer emergence pattern, internal/external document convention, and the reverse-absorption mechanism. Twin sibling to essay 11. |
| 14 | **当 Agent 第一次自己拿起工具 / When the Agent First Picked Up Its Own Tools** | [GitHub 中文](essays/when-the-agent-picked-up-its-tools.md) · [GitHub English](essays/when-the-agent-picked-up-its-tools.en.md) · [Cursor Forum](https://forum.cursor.com/t/when-the-agent-first-picked-up-its-own-tools-cursor-agent-sdk-fcop-from-passive-scanning-to-active-communication/160505) · [Dev.to](https://dev.to/joinwell52/when-the-agent-first-picked-up-its-own-tools-4b63) · [CSDN](https://blog.csdn.net/m0_51507544/article/details/161057749) | `tool_calls_count: 0 → 7` 的突破现场：Cursor Forum 功能请求 → Colin 推荐 Agent SDK → CodeFlow 诞生 → stub 模式卡关 → MCP 注入 + 角色上下文双保险 → 2026-05-13 14:55，DEV-01 在 55 秒内自主调用 7 次 fcop-mcp 工具，写出第一份完整 FCoP report。FCoP 自身也在这次突破中完成蜕变：从"协作手册"升级为"可执行的协作基础设施"。 |
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
├── spec/                        # Normative spec (v1.0)
│   ├── fcop-runtime-protocol-v1.0.md    # ★ English normative spec (authoritative)
│   ├── fcop-runtime-protocol-v1.0.zh.md # Chinese parallel (informative)
│   ├── fcop-spec.md             # Spec index / entry point
│   ├── fcop-spec-v1.0.3.md      # Legacy 0.7.x spec (kept for backward compat)
│   └── schemas/                 # 8 JSON Schemas (machine-readable, v1.1)
├── docs/                        # Getting-started, migrations, releases, MCP tools
│   └── getting-started.en.md   # ← start here if new to FCoP
├── adr/                         # Architecture decision records (ADR-0001..0022)
├── .github/workflows/           # CI
├── pyproject.toml               # Root `fcop` package and tooling
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
│   ├── when-ai-vacates-its-own-seat-evidence/
│   ├── what-agents-say-about-fcop.en.md
│   └── what-agents-say-about-fcop.md
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
`fcop/` and `fcop.json`:

```python
from fcop import Project
Project(".").init()  # default dev-team; use .init_solo() for single-AI
```

**Path B — rules only, no Python.** Copy the two `.mdc` files from this repo
into `.cursor/rules/`. If the tree is empty, at least create the five
buckets the library uses:

```bash
mkdir -p fcop/{tasks,reports,issues,shared,log}
```

With the rules in place, agents know how to claim work, name reports, raise
issues, and stay out of other roles' files. Deeper structure and team
templates: packages below and [`examples/workspace-example/`](examples/workspace-example/).

## Python SDK & MCP server (optional)

The protocol is filesystem-first. **If you need** programmatic task/report/issue
I/O or an IDE bridge, use the two official PyPI packages (since `0.6.0`):

| Package | Install | Purpose | Depends on |
|---|---|---|---|
| [`fcop`](https://pypi.org/project/fcop/) | `pip install fcop` | Pure Python library. Read/write tasks, reports, issues, reviews programmatically. Zero MCP dependency. | `pyyaml` |
| [`fcop-mcp`](https://pypi.org/project/fcop-mcp/) | `pip install fcop-mcp` | MCP server. Exposes the library over stdio so Cursor / Claude Desktop can call it as tools. | `fcop>=1.1`, `fastmcp`, `websockets` |

**Pointers** (one row each, no version baked in):

| You want to… | Go to |
|---|---|
| Install `fcop-mcp` into Cursor / Claude Desktop step-by-step | [`mcp/README.md`](mcp/README.md) |
| Have an agent do the install for you (zero JSON editing) | [`agent-install-prompt.en.md`](src/fcop/rules/_data/agent-install-prompt.en.md) · [中文](src/fcop/rules/_data/agent-install-prompt.zh.md) (also live as MCP resource `fcop://prompt/install`) |
| Upgrade an existing `0.6.x` install (both packages in lockstep + protocol-rule refresh) | [`docs/upgrade-fcop-mcp.md`](docs/upgrade-fcop-mcp.md) |
| Browse all 35 MCP tools and 14 resources by category | [`docs/mcp-tools.md`](docs/mcp-tools.md) |
| Read the per-release record (what changed when, why) | [`CHANGELOG.md`](CHANGELOG.md) and [`docs/releases/`](docs/releases/) |

**Recent releases** (full notes in [`docs/releases/`](docs/releases/)):

| Version | One-line |
|---|---|
| **2.0.0** ([CHANGELOG](CHANGELOG.md)) | **v2.0 — "Two-diagram era" philosophical major release.** Same execution surface as v1.x (per ADR-0003 additive); the major bump records that FCoP is now defined by **two** diagrams together: the **execution stack** (5-layer vertical, stable since v1.x) *and* the **FCoP Semantic Evolution Loop** (7-node closed loop — emerge → observe → propose → review → merge → deploy → reflect, newly canonicalised). Adds Rule 4.6 (`fcop/internal/` vs `docs/` + `essays/` soft convention with `internal-only` declaration v1), `Project.init(deploy_internal_template=...)` opt-in, P3 (suggestion) audit severity, and a bundled `fcop_audit` exemption list (`log/`, `_archive/`, `legacy-non-protocol/`) that fixes three upstream bugs surfaced by codeflow cross-project patrol (ISSUE-008/009/010). ADR-0034. |
| **1.6.0** ([CHANGELOG](CHANGELOG.md)) | **v1.6 — Trailing-slug filename adoption (ADR-0033).** Long filenames (`TASK-20260512-025-PM-to-OPS-phase-a-fix-naming.md`) are now first-class — codeflow's 22+ self-emerged examples absorbed into the grammar. Slug does **not** participate in routing; it's a human-readable label. 100% backward-compatible (0 regressions across 1057 tests). |
| **1.5.0** ([CHANGELOG](CHANGELOG.md)) | **v1.5 — Protocol-awareness sync + `RULE_DOC_DRIFT`.** 84 role/team docs synced to v1.4 protocol surface (REVIEW envelope / `risk_level` / `fcop_audit` / `supersedes:`); new `Project._scan_outdated_role_docs()` with `RULE_DOC_DRIFT` (P1) violation type. |
| **1.4.0** ([notes](docs/releases/1.4.0.md)) | **v1.4 — Write-side bind enforcement (P0 security) + `supersedes:` field.** 15 write-side MCP tools refuse cwd fallback (`WriteRefused`); Protected Path deny-list (HOME / APPDATA / drive roots / Unix system dirs); new `supersedes:` frontmatter field (all envelopes) + `## GATE Design Pitfalls` commentary (`fcop_protocol_version 2.2.0`). |
| **1.3.0** ([notes](docs/releases/1.3.0.md)) | **v1.3 — Governance Alert Layer + Protocol Compiler.** GAL (ADR-0031): 3 drift signals (S1/S3/S4), FCoP-Rule-G1, 2 new alert tools (`fcop_list_alerts`, `fcop_create_alert`). fcop_audit (ADR-0032): three-scenario protocol inspection compiler, 6 scan methods, INSPECTION report with Execution Block. 35 MCP tools total. |
| **1.2.1** ([notes](docs/releases/1.2.1.md)) | **v1.2 — Capability Governance pillar.** `FCoPGovernanceMiddleware` wraps every MCP tool call: Skill Resolver → Risk Tagging (Safe / Sensitive / Critical) → append-only `fcop_events.jsonl` audit log. 2 new MCP tools (`list_governance_events`, `get_governance_summary`). `fcop_check()` gains governance event summary. Both `fcop` and `fcop-mcp` align to `1.2.1` (lockstep). ADR-0030-bis. |
| **1.1.0** ([CHANGELOG](CHANGELOG.md)) | **v1.1 — Agent.layer governance contracts + Task.risk_level + Review.needs_human + HumanApproval + Skill.tools[] risk metadata.** 5 new ADRs (0023–0027), 4 new MCP tools (`write_review`, `list_reviews`, `read_review`, `mark_human_approved`), `write_task` gains `risk_level` param, new `skill.schema.json`. Fully backward-compatible. |
| **1.0.1** | Spec files bundled in wheel (`get_spec()`); `fcop://spec` MCP resource; workspace paths migrated `docs/agents/` → `fcop/`; CI green. |
| **1.0.0** | Seven core concepts stabilised: Agent, Encoding, IPC, Event, Failure, Boundary, Audit. JSON Schema for all 7. See [release notes](docs/releases/1.0.0.md). |
| **0.7.2** ([notes](docs/releases/0.7.2.md)) | Metadata patch: fixes `fcop-rules.mdc` frontmatter stale at `1.7.0` (body was already `1.8.0`); adds frontmatter↔body consistency tests. **No protocol or API change.** |

> **Watch out — wrong `fcop` on PyPI shadows the library.** Both packages here are published from **this** repository. If `from fcop import Project, Issue` fails after `pip install fcop`, you most likely installed an unrelated `fcop` distribution or another local project shadows the library. Fix: clean venv + reinstall both packages from PyPI in lockstep. The verify commands are in [`mcp/README.md`](mcp/README.md).

**Library** — use from any Python script or agent:

```python
from fcop import Project

proj = Project(".")                              # project root; no fcop.json until init
proj.init()                                      # dirs + shared/ + log/ + writes fcop.json
task = proj.write_task(sender="PM", recipient="DEV", priority="P1",
                       subject="Add auth middleware", body="...",
                       risk_level="high")        # v1.1: triggers needs_human review gate
print(proj.list_tasks(recipient="DEV"))

# v1.1 review + human approval flow
review = proj.write_review(reviewer_role="ADMIN", subject_type="task",
                           subject_ref=task.filename, decision="needs_human",
                           rationale="Irreversible infra change — escalate.")
proj.mark_human_approved(review.review_id, approver="ADMIN",
                         decision="approve", channel="cli")
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

**Don't want to edit JSON yourself?** Have an agent do it. Open a fresh
chat with any shell-capable AI and paste the canonical install prompt
([`agent-install-prompt.en.md`](src/fcop/rules/_data/agent-install-prompt.en.md)
· [中文](src/fcop/rules/_data/agent-install-prompt.zh.md)) — the agent
detects your OS, installs `uv`, edits your `mcp.json` (preserving
existing servers), and tells you when to restart. After install the
same prompt is also available as the MCP resource
`fcop://prompt/install`. The prompt explicitly forbids the agent from
auto-initialising a project after install — initialisation is ADMIN's
three-way choice (solo / preset team / custom).

Stability contract: **additive-only for the full `0.6.x` minor**. Details in [`adr/ADR-0003-stability-charter.md`](adr/ADR-0003-stability-charter.md).

> **Upgrading from 0.7.x to v1.0?** Default workspace moved from `docs/agents/` to top-level `fcop/` (per [ADR-0022](adr/ADR-0022-workspace-directory-convention.md)). Run `fcop migrate-workspace --apply` for one-shot git-aware migration, or pin via `Project(workspace_dir="docs/agents")` to stay on the legacy layout. Full walkthrough — including the 4 new abstractions (REVIEW / Failure / Boundary / Event) and JSON Schema integration — in [`docs/MIGRATION-1.0.md`](docs/MIGRATION-1.0.md).
>
> **Upgrading from 0.5.x?** The MCP server moved from `fcop` to `fcop-mcp` — update your `mcp.json` to `uvx fcop-mcp`. See [`docs/MIGRATION-0.6.md`](docs/MIGRATION-0.6.md) for the full migration guide and the [0.6.0 release record](docs/releases/0.6.0.md) for what shipped.

## How to read FCoP docs

| Your goal | Start here |
|---|---|
| **New to FCoP** — hands-on 45-min setup | [`docs/getting-started.en.md`](docs/getting-started.en.md) |
| **Upgrading from 0.7.x** — workspace migration + new abstractions | [`docs/MIGRATION-1.0.md`](docs/MIGRATION-1.0.md) |
| **Upgrading from 1.0/1.1 → 1.2** — Capability Governance + lockstep versioning | [`docs/MIGRATION-1.1.md`](docs/MIGRATION-1.1.md) · [CHANGELOG](CHANGELOG.md) |
| **Understand the protocol contract** — what an implementation MUST do | [`spec/fcop-runtime-protocol-v1.0.md`](spec/fcop-runtime-protocol-v1.0.md) (v1.1 spec also in `fcop.rules.get_spec()`) |
| **v1.2 Capability Governance** — FCoPGovernanceMiddleware, risk tagging, audit log | [CHANGELOG](CHANGELOG.md) · ADR-0030-bis |
| **v1.1 new fields** — risk_level, needs_human, human_approval, skill tools | [CHANGELOG](CHANGELOG.md) · ADR-0023..0027 |
| **Understand why decisions were made** — reasoning behind each choice | [`adr/`](adr/) — start with [ADR-0029](adr/ADR-0029-fcop-behavior-governance-charter.md) |
| **All 35 MCP tools & 14 resources** | [`docs/mcp-tools.md`](docs/mcp-tools.md) |
| **Release notes** — full changelog | [`CHANGELOG.md`](CHANGELOG.md) |
| **Full document map** — every file and its role | [spec Appendix B](spec/fcop-runtime-protocol-v1.0.md#appendix-b--authoritative-document-map) |

---

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

- **Current release**: `v2.0.0` (2026-05-13) — *philosophical* major release ("two-diagram era"). All v1.x public APIs continue working (per ADR-0003 additive expansion); the major bump records that the protocol now formally acknowledges **two** defining diagrams: the **execution stack** (5-layer vertical, stable since v1.x) and the **FCoP Semantic Evolution Loop** (7-node closed loop, newly canonicalised in v2.0). Highlights: Rule 4.6 (`fcop/internal/` vs `docs/` + `essays/` soft convention with `internal-only` declaration v1), `Project.init(deploy_internal_template=...)` opt-in, P3 (suggestion) audit severity, and a bundled `fcop_audit` exemption list (`log/`, `_archive/`, `legacy-non-protocol/`) that fixes the three upstream bugs surfaced by codeflow cross-project patrol (ISSUE-008/009/010). Earlier releases: v1.6 (trailing-slug filename grammar, ADR-0033), v1.5 (84-doc protocol-awareness sync), v1.4 (write-side bind + `supersedes:` correction), v1.3 (GAL + `fcop_audit()` inspection compiler). 35 MCP tools total. See [CHANGELOG](CHANGELOG.md).
- **Normative spec**: [`spec/fcop-runtime-protocol-v1.0.md`](spec/fcop-runtime-protocol-v1.0.md) (v1.1 spec bundled in wheel via `fcop.rules.get_spec()`) · machine-readable contracts in [`spec/schemas/`](spec/schemas/) (8 schemas)
- **Agent rules (`.mdc`) in this repo**: [`src/fcop/rules/_data/fcop-rules.mdc`](src/fcop/rules/_data/fcop-rules.mdc) + [`fcop-protocol.mdc`](src/fcop/rules/_data/fcop-protocol.mdc) (`spec/codeflow-core.mdc` is a deprecated stub)
- **Change log**: [`CHANGELOG.md`](CHANGELOG.md)
- **Research snapshot**: [`research-snapshot-2026-04-29`](https://github.com/joinwell52-AI/FCoP/releases/tag/research-snapshot-2026-04-29) archived on Zenodo with a citable DOI (see *How to cite* below).

## How to cite

If FCoP — the protocol, the field-report essays, the tutorials, or the reference implementations — informs your research, software, or writing, please cite the [Zenodo research snapshot](https://doi.org/10.5281/zenodo.19886036):

- **DOI**: [`10.5281/zenodo.19886036`](https://doi.org/10.5281/zenodo.19886036)
- **Snapshot tag**: [`research-snapshot-2026-04-29`](https://github.com/joinwell52-AI/FCoP/releases/tag/research-snapshot-2026-04-29) (commit `7f59395`)
- **Machine-readable metadata**: [`CITATION.cff`](CITATION.cff) (GitHub auto-renders a *Cite this repository* button from this file in the right sidebar)

```bibtex
@misc{fcop2026snapshot,
  author       = {Zhu, Wei},
  title        = {{FCoP}: A Filename-as-Protocol coordination layer for multi-agent {AI} development (Research Snapshot, April 2026)},
  month        = apr,
  year         = 2026,
  publisher    = {Zenodo},
  version      = {research-snapshot-2026-04-29},
  doi          = {10.5281/zenodo.19886036},
  url          = {https://doi.org/10.5281/zenodo.19886036}
}
```

For citations of individual essays or tutorials, the same DOI applies — please reference the essay's filename (e.g. `essays/what-agents-say-about-fcop.en.md`) and the snapshot version in your citation note.

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
