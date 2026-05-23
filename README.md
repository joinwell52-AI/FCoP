<p align="center">
  <img src="assets/fcop-logo-256.png" alt="FCoP Logo" width="180" />
</p>

<h1 align="center">FCoP 鈥?File-based Coordination Protocol</h1>

<p align="center">
  <em>The <strong>AI Agent behavior governance protocol</strong> 鈥?the runtime contract for agent collaboration on a shared filesystem.</em><br/>
  <strong>Core invariant: <code>Filename as Protocol</code>. Folders are the message bus.</strong>
</p>

<p align="center">
  <strong><a href="https://joinwell52-ai.github.io/FCoP/">馃寪 Project homepage</a></strong> 路
  <a href="README.zh.md">绠€浣撲腑鏂?/a> 路
  <a href="docs/getting-started.en.md">Getting started</a> 路
  <a href="src/fcop/rules/_data/agent-install-prompt.en.md"><strong>馃憠 Let AI install!</strong></a> 路
  <a href="src/fcop/rules/_data/agent-bringup-prompt.en.md"><strong>馃憠 Let AI bring up a project!</strong></a> 路
  <a href="docs/mcp-tools.md"><strong>MCP Tools (45)</strong></a> 路
  <a href="essays/when-ai-organizes-its-own-work.en.md">Field Report</a> 路
  <a href="essays/fcop-natural-protocol.en.md">Natural Protocol</a> 路
  <a href="spec/fcop-3.0-spec.md"><strong>3.0 Spec</strong></a> 路
  <a href="adr/README.md">ADR Index</a>
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
  <a href="CHANGELOG.md">
    <img src="https://img.shields.io/badge/release-3.2.3-brightgreen?style=flat-square" alt="3.2.3" />
  </a>
  <a href="spec/fcop-3.0-spec.md">
    <img src="https://img.shields.io/badge/spec-FCoP%203.0-orange?style=flat-square" alt="FCoP 3.0 spec" />
  </a>
  <a href="https://registry.modelcontextprotocol.io/v0/servers?search=io.github.joinwell52-AI%2Ffcop">
    <img src="https://img.shields.io/badge/MCP%20Registry-io.github.joinwell52--AI%2Ffcop-8A2BE2?style=flat-square" alt="Official MCP Registry: io.github.joinwell52-AI/fcop" />
  </a>
  <a href="https://doi.org/10.5281/zenodo.19886036">
    <img src="https://zenodo.org/badge/DOI/10.5281/zenodo.19886036.svg" alt="DOI 10.5281/zenodo.19886036" />
  </a>
</p>

---

## 馃啎 FCoP 3.0 is here 鈥?*Files carry protocol. Paths address state. Events replay transitions.*

<p align="center">
  <a href="spec/fcop-3.0-spec.md">
    <img src="assets/fcop-3.0-architecture.png" alt="FCoP 3.0 路 Canonical Architecture 鈥?Files carry protocol. Paths address state. Events replay transitions." width="900" />
  </a>
</p>

> **FCoP 3.0** is the protocol's first **semantic seal**. State now lives in the filesystem itself (`_lifecycle/{inbox,active,review,done,archive}/`), events live append-only inside the file, and *custody / ownership / scheduling / runtime* are explicitly **out of scope** (Boundary Charter).
>
> **Two paths to v3:**
> - **New project** 鈫?`fcop init` / MCP `init_solo|init_project|create_custom_team` (鈮?3.0.2 produces v3 topology directly).
> - **Existing 2.x project** 鈫?`python -m fcop migrate --to-v3`.
>
> 鈿狅笍 **3.0.0 / 3.0.1 fresh-init bug**: those releases initialized projects in v2 layout (no `_lifecycle/`). 3.0.2 fixes the bug. If you initialized on 3.0.0 / 3.0.1, run `migrate --to-v3` to upgrade.

| Doc | Purpose |
|---|---|
| [`spec/fcop-3.0-spec.md`](spec/fcop-3.0-spec.md) 路 [zh](spec/fcop-3.0-spec.zh.md) | Single-page canonical spec |
| [`spec/fcop-3.0-rfc.md`](spec/fcop-3.0-rfc.md) 路 [zh](spec/fcop-3.0-rfc.zh.md) | IETF-style RFC projection |
| [`docs/MIGRATION-3.0.md`](docs/MIGRATION-3.0.md) 路 [zh](docs/MIGRATION-3.0.zh.md) | 2.x 鈫?3.0 migration guide |
| [`CHANGELOG.md` `[3.0.0]`](CHANGELOG.md) | Full release notes |
| [`essays/the-day-we-almost-added-custody.en.md`](essays/the-day-we-almost-added-custody.en.md) 路 [zh](essays/the-day-we-almost-added-custody.md) | The decision that defined 3.0 |

---

## Where FCoP sits in the stack

FCoP is the **behavior governance protocol layer** for multi-agent collaboration 鈥?standardizing how agents report actions, review outcomes, and operate within governed capability boundaries.

```
Application Layer      CodeFlow / Cursor / Claude Desktop      鈫?business products / agent applications
Host Adapter Layer     fcop-mcp / fcop-cli / @fcop/claude      鈫?integration adapters / host bridges
鈽?FCoP Protocol 鈽?     Agent collaboration / reporting /        鈫?this is FCoP
                       review / capability governance /
                       event semantics / failure boundaries /
                       auditability
Reference Impl         fcop (Python library)                   鈫?protocol reference implementation
Execution Substrate    LLM APIs / MCP tools / filesystem /     鈫?execution environment
                       process manager / operating system
```

> **FCoP governs agent behavior, not execution runtime.** 鈥?[ADR-0029](adr/ADR-0029-fcop-behavior-governance-charter.md)

v1.0 stabilises the minimum semantic contract for the **seven core concepts** above. Spec is stable; encodings are open: the *IPC Surface* (TASK / REPORT / ISSUE / REVIEW) is strongly typed, while the *Open Knowledge Surface* (`shared/` + `{ALL-CAPS-PREFIX}-{slug}.md`) leaves vocabulary open for agents to invent 鈥?see [ADR-0021](adr/ADR-0021-encoding-abstraction.md).

鈫?**Start here**: [`docs/getting-started.md`](docs/getting-started.md) 路 [`docs/getting-started.en.md`](docs/getting-started.en.md)

---

## The one-paragraph pitch

Most multi-agent frameworks lean on message queues, databases, or custom RPC layers. FCoP throws all of that away and keeps only the **filesystem**:

- **Directories are statuses.** `tasks/`, `reports/`, `issues/`, `log/` 鈥?moving a file between them _is_ the state transition.
- **Filenames are routing.** `TASK-20260418-001-PM-to-DEV.md` tells you the sender, recipient, kind, and sequence at a glance.
- **Contents are payload.** Markdown + a small YAML frontmatter. Agents read and write it the same way humans do.
- **`os.rename()` is the only sync primitive.** POSIX guarantees atomicity within a mount point 鈥?no locks, no brokers, no consensus.

That's it. No database. No message queue. No custom daemon. You can `ls` the entire system state. You can `git log` the entire collaboration history.

> If TCP is "bytes over wires," **FCoP is "tasks over folders."**

> In engineering terms, you get a **serializable, versionable collaboration surface** instead of relying on **proprietary, heavyweight infrastructure**.

## Why should you care?

Because agents are easier to supervise when you can literally **see** what they're doing.

We ran a 4-agent team (PM / DEV / QA / OPS) for 48 hours on this protocol and watched the agents invent **six coordination patterns we never wrote down** 鈥?team broadcasts, role slots, shared documents, subtask batches, self-explaining READMEs, and traceability frontmatter. Each pattern showed up as _new filenames_ 鈥?no code changes required.

Then something stranger happened: a **single** agent, on an **unrelated** task (generating an AI music video in a folder with **no connection to any then-open project workspace**), spontaneously split itself into PM / DEV / ADMIN and wrote four FCoP-format memos to itself 鈥?then cited and **sublimated** our scattered rules into a single moral principle we had not written anywhere.

Both stories are written up as field reports in the essays index below.

## Essays 路 field reports from the wild

| # | Title | Versions | One-liner |
|---|---|---|---|
| 01 | **When AI Organizes Its Own Work** | [English](essays/when-ai-organizes-its-own-work.en.md) 路 [涓枃 (GitHub)](essays/when-ai-organizes-its-own-work.md) 路 [涓枃 (CSDN)](https://blog.csdn.net/m0_51507544/article/details/160344932) | A 4-agent team (PM / DEV / QA / OPS), 48 hours, nothing but a folder 鈥?and six coordination patterns we never wrote down. |
| 02 | **An unexplainable thing I saw: the agent didn't just comply with rules 鈥?it *endorsed* them** | [GitHub 涓枃](essays/fcop-natural-protocol.md) 路 [GitHub English](essays/fcop-natural-protocol.en.md) 路 [CSDN 涓枃](https://blog.csdn.net/m0_51507544/article/details/160345043) 路 [Dev.to](https://dev.to/joinwell52/an-unexplainable-thing-i-saw-the-agent-didnt-just-comply-with-rules-it-endorsed-them-5ecd) 路 [Cursor Forum](https://forum.cursor.com/t/i-asked-cursor-to-make-a-video-it-wrote-itself-4-protocol-memos-field-report-on-rule-internalization/158524) | A single agent, on a completely unrelated task, spontaneously split into 4 FCoP roles and *sublimated* our scattered rules into one principle we had never written. Ships with a [full evidence archive](essays/fcop-natural-protocol-evidence/) (4 screenshots, 4 memos, raw JSONL transcript). |
| 03 | **Why the Natural Protocol Holds Up 鈥?FCoP's lineage from TMPA** | [GitHub 涓枃](essays/fcop-tmpa-lineage.md) 路 [GitHub English](essays/fcop-tmpa-lineage.en.md) | Companion to essay 02. Where that one shows *that* the principle emerged, this one explains *why it holds up*: FCoP was extracted from TMPA (a multi-AI architecture spec whose core bet is replacing distributed coordination with a plain-text temporal sequence), and the agent's sentence is the minimal-viable-form of an AI ethics mandate already written there. |
| 04 | **Saying "No" Is the Hardest Thing for an LLM 鈥?FCoP Gives It Grammar** | [GitHub English](essays/when-ai-vacates-its-own-seat.en.md) 路 [GitHub 涓枃](essays/when-ai-vacates-its-own-seat.md) 路 [Evidence archive](essays/when-ai-vacates-its-own-seat-evidence/INDEX.md) 路 [CSDN 涓枃](https://blog.csdn.net/m0_51507544/article/details/160513899) 路 [Dev.to](https://dev.to/joinwell52/saying-no-is-the-hardest-thing-for-an-llm-fcop-gives-it-grammar-3ccd) 路 [Cursor Forum](https://forum.cursor.com/t/saying-no-is-the-hardest-thing-for-an-llm-fcop-gives-it-grammar/159037) | One machine, two Cursor sessions, two GPT-5 minor versions (5.4 and 5.5). After I told the original PM "I went and found a deputy PM," it stepped down on its own 鈥?all the way to UNBOUND. Meanwhile the new `PM.TEMP` walked an undocumented protocol path with one body line: "*PM.TEMP acting as PM, kept for FCoP tool compatibility*." I expected a conflict. None happened 鈥?the agents finished the unwritten parts of the spec themselves. Ships with 15 screenshots + 2 full JSONL transcripts. |
| 05 | **Tutorial: From Solo to a 2-Person AI Crew 鈥?Disciplining the AI Team with FCoP-MCP** (two parallel case studies) | English (Tetris case): [`tetris-solo-to-duo.en.md`](docs/tutorials/tetris-solo-to-duo.en.md) 路 [Dev.to](https://dev.to/joinwell52/free-open-source-multi-agent-hands-on-how-to-command-agents-fcop-mcp-brings-discipline-to-1j3j) 路 [Cursor Forum](https://forum.cursor.com/t/free-open-source-multi-agent-hands-on-how-to-command-agents-fcop-mcp-brings-discipline-to-ai-teams/159329) 路 涓枃璇戞湰锛堜縿缃楁柉鏂瑰潡妗堜緥锛? [`tetris-solo-to-duo.zh.md`](docs/tutorials/tetris-solo-to-duo.zh.md) 路 涓枃姣嶈鍘熷垱锛堣椽鍚冭泧妗堜緥锛? [`snake-solo-to-duo.zh.md`](docs/tutorials/snake-solo-to-duo.zh.md) 路 [CSDN 涓枃鐗圿(https://blog.csdn.net/m0_51507544/article/details/160603953) | The first **tutorial-style** entry in this index, shipping as **two parallel case studies 鈥?the protocol is the same, the games and the live easter egg are different**. Both are 45-minute hands-on dogfoods: get the agent to install `fcop-mcp` in Cursor, ship a working game in solo mode, switch to a 2-person team where PLANNER designs and CODER implements a creative variant, then read the disk. The **Chinese case** uses Snake 鈫?`NEON ORBIT` (original-themed) and captures an actual PLANNER-impersonating-CODER easter egg from the 0.6.x era. The **English case** uses Tetris 鈫?`Nebula Stack` (solo) 鈫?`Comet Loom` (team), and adds a full **review-and-rework cycle** (ADMIN plays v1, finds 3 blocking defects, bounces it back; PLANNER writes TASK-006 with a new `Verification Requirements` section; CODER ships v2) plus an end-of-day on-the-record interview where both agents are asked what they think of the protocol. 22 dogfood screenshots, 14 TASK/REPORT files, 8 silent role-switch evidence files, 2 game artefacts, 2 verbatim agent transcripts 鈥?all archived under [`docs/tutorials/assets/tetris-en/`](docs/tutorials/assets/tetris-en/). |
| 06 | **What the Agents Say About FCoP, When You Ask Them** | [GitHub English](essays/what-agents-say-about-fcop.en.md) 路 [GitHub 涓枃](essays/what-agents-say-about-fcop.md) 路 [Evidence archive (Tetris-en dogfood)](docs/tutorials/assets/tetris-en/) 路 [CSDN 涓枃](https://blog.csdn.net/m0_51507544/article/details/160636177) 路 [Dev.to](https://dev.to/joinwell52/what-the-agents-say-about-fcop-when-you-ask-them-3ajk) 路 [Cursor Forum](https://forum.cursor.com/t/what-the-agents-say-about-fcop-when-you-ask-them-two-field-interviews-at-the-end-of-an-english-dogfood/159368) | The third class of *"agents endorse FCoP"* evidence, after [essay 02](essays/fcop-natural-protocol.en.md) (**unprompted, off-task**) and [essay 04](essays/when-ai-vacates-its-own-seat.en.md) (**conflict-forced**): now **directly asked**. At the end of the English Tetris dogfood (companion to the row-05 tutorial), both agents (PLANNER and CODER) were asked agent-perspective takes on FCoP 鈥?no marketing tone. PLANNER named the RLHF instinct it had to fight ("follow latest instruction") to honour FCoP's role lock and called eight of its own `role-switch` evidence files **true positives**, against its own operational convenience. CODER admitted it had a protocol primitive (`write_issue`) it didn't use, traced the v1 defect to that exact uncovered space, and filed PR-grade product feedback on the protocol. Three different elicitation conditions, the same phenomenon 鈥?agents endorse FCoP when given the room to. Also includes a small empirical observation: across the entire 45-minute dogfood, ADMIN's two most-used phrases were **"Start work."** and **"Inspection."** |
| 07 | **褰?agent 浠庤嚜宸辩殑娈嬮涓涔?* | [GitHub 涓枃](essays/when-agents-learn-from-their-own-wreckage.md) 路 [GitHub English](essays/when-agents-learn-from-their-own-wreckage.en.md) 路 [CSDN 涓枃](https://blog.csdn.net/m0_51507544/article/details/161028380) 路 [Dev.to](https://dev.to/joinwell52/when-agents-learn-from-their-own-wreckage-45p2) | codeflow 椤圭洰涓€鏃?14 涓?agent 娑岀幇鐜板満鎶ュ憡锛?026-05-12锛夛細USER HOME 鍏ㄥ眬姹℃煋 / GATE 鎻忚堪鑷懡涓?/ `supersedes:` 瀛楁鐜板満鍙戞槑鈥斺€斾互鍙婂崗璁浣曞湪闆舵宕╂簝鐨勬儏鍐典笅锛屼互灏忔椂绾ч€熷害灏嗗畠浠叏閮ㄥ弽鍚戝惛鏀躲€?|
| 08 | **鍗忚涓轰粈涔堢煭锛屽巻鍙蹭负浠€涔堥暱** | [GitHub 涓枃](essays/why-the-protocol-stays-short.md) 路 [GitHub English](essays/why-the-protocol-stays-short.en.md) | 涓€浠界粰鍗忚缁存姢鑰呯殑璁捐鍝插绛旀锛?杩欐牱鐨勬秾鐜颁細涓嶄細娌℃湁姝㈠锛?鈥斺€旂煭绛旓細浼氭敹鏁涗絾涓嶄細鍋溿€傚洓绫绘秾鐜扮殑澶勭悊璺緞銆佷笁鏉＄粨鏋勫姏瀛︿负浣曡兘璁╁崗璁鏋朵笉琚秾鐜板帇鍨紝浠ュ強"鍗忚鐭槸涓轰簡璁╁巻鍙茶兘鏃犻檺闀?鐨勫簳灞傞€昏緫銆?|
| 09 | **褰?validator 鎾炲悜鑷繁鐨勯暅鍍?* | [GitHub 涓枃](essays/gate-design-pitfalls-case-studies.md) 路 [GitHub English](essays/gate-design-pitfalls-case-studies.en.md) | 浠?codeflow OPS I-14 鐪?validator-validates-itself 鍙嶆ā寮忥細GATE 鍦ㄦ鏌?staged diff 鏃跺懡涓簡 GATE 鎻忚堪鏈韩锛屽嚑鍒嗛挓鍚庤 OPS 鑷籂鈥斺€旇繖涓€绫婚櫡闃辩殑绯荤粺鎬цВ鍓栦笌"璇箟鍖栧疄璇?鏍规不濮垮娍锛屼互鍙婂畠濡備綍鎴愪负 `fcop-protocol.mdc 搂GATE Design Pitfalls` 鐨勬簮澶存渚嬨€?|
| 10 | **涓€琛?frontmatter 鐨勬梾绋?* | [GitHub 涓枃](essays/the-supersedes-field-story.md) 路 [GitHub English](essays/the-supersedes-field-story.en.md) | `supersedes:` 瀛楁浠庝竴娆″崗璁袱闅剧幇鍦哄彂鏄庡埌 `ipc-envelope.schema.json` 姝ｅ紡瀛楁鐨勪袱灏忔椂鏃呯▼锛歊ule 5锛坅ppend-only锛? Rule 6锛坮eciprocity锛? Rule 0.c锛坱ruthful锛変笁鏉¤鍒欏悓鏃舵垚绔嬫椂锛宎gent 鐢ㄤ竴琛?YAML 鑷繁瑙ｄ簡鍥板眬鈥斺€旇繖鏉¤矾寰勫睍绀?FCoP 娑岀幇钀藉湴鐨勬渶浣庢垚鏈Э鍔裤€?|
| 11 | **鐪嬶紝浣嗕笉鍔ㄦ墜** | [GitHub 涓枃](essays/looking-without-touching.md) 路 [GitHub English](essays/looking-without-touching.en.md) 路 [CSDN 涓枃](https://blog.csdn.net/m0_51507544/article/details/161028161) | FCoP 涓夊眰璇箟鎵ц閾剧鏅細`fcop_audit()` 涓轰粈涔?鍙湅涓嶆敼"鈥斺€擫1 妫€娴?/ L2 瑙ｉ噴 / L3 鏂囨。涓夊眰鎶?鐪嬭"鍜?鍔ㄦ墜"鍒囧紑锛屼骇鍑?`INSPECTION.md`锛堝缓璁潪鍛戒护锛夛紝鎵ц鏉冪暀缁欎汉銆俙adr/FCoP-semantic-execution-chain.md` 鐨勭鏅増銆?|
| 12 | **浜斿ぇ AI 妯″瀷鐪间腑鐨?FCoP** | [GitHub 涓枃](essays/what-five-ai-models-say-about-fcop.md) 路 [GitHub English](essays/what-five-ai-models-say-about-fcop.en.md) 路 [Cursor Forum](https://forum.cursor.com/t/what-5-ai-models-say-about-fcop-from-their-own-agent-perspective-category-showcase/160506) | 鎶?FCoP 鏍稿績鏂囨。鍠傜粰 ChatGPT / Claude / DeepSeek / Grok / 璞嗗寘锛屽彧闂竴涓棶棰橈細"浣犳槸 agent锛屼綘鎬庝箞鐪嬭繖濂楀崗璁紵"鈥斺€斾簲绉嶆埅鐒朵笉鍚岀殑鍐呴儴瑙嗚锛圕hatGPT 璋堣韩浠藉悎娉曟€с€丆laude 璋堣瘹瀹炶竟鐣屻€丏eepSeek 璋堜綋闈㈢敓瀛樸€丟rok 鍋氭妧鏈瘎瀹°€佽眴鍖呰璁捐鍝插锛夛紝浠ュ強瀹冧滑涔嬮棿鏈€鏈夋剰鎬濈殑鍒嗘銆?|
| 13 | **Evolution, Reverse Absorption / 婕斿寲锛屽弽鍚戝惛鏀?* | [GitHub 涓枃](essays/evolution-reverse-absorption.md) 路 [GitHub English](essays/evolution-reverse-absorption.en.md) | Protocol philosophy 2.0 visual declaration: FCoP graduates from a single execution-chain diagram (essay 11 *Looking, not Touching*) to a **two-diagram era** 鈥?adding an evolution-loop diagram (a 7-step semantic evolution loop) plus the companion [ADR-0034](adr/ADR-0034-fcop-internal-external-document-convention.md), which codifies the 4-layer emergence pattern, internal/external document convention, and the reverse-absorption mechanism. Twin sibling to essay 11. |
| 14 | **褰?Agent 绗竴娆¤嚜宸辨嬁璧峰伐鍏?/ When the Agent First Picked Up Its Own Tools** | [GitHub 涓枃](essays/when-the-agent-picked-up-its-tools.md) 路 [GitHub English](essays/when-the-agent-picked-up-its-tools.en.md) 路 [Cursor Forum](https://forum.cursor.com/t/when-the-agent-first-picked-up-its-own-tools-cursor-agent-sdk-fcop-from-passive-scanning-to-active-communication/160505) 路 [Dev.to](https://dev.to/joinwell52/when-the-agent-first-picked-up-its-own-tools-4b63) 路 [CSDN](https://blog.csdn.net/m0_51507544/article/details/161057749) | `tool_calls_count: 0 鈫?7` 鐨勭獊鐮寸幇鍦猴細Cursor Forum 鍔熻兘璇锋眰 鈫?Colin 鎺ㄨ崘 Agent SDK 鈫?CodeFlow 璇炵敓 鈫?stub 妯″紡鍗″叧 鈫?MCP 娉ㄥ叆 + 瑙掕壊涓婁笅鏂囧弻淇濋櫓 鈫?2026-05-13 14:55锛孌EV-01 鍦?55 绉掑唴鑷富璋冪敤 7 娆?fcop-mcp 宸ュ叿锛屽啓鍑虹涓€浠藉畬鏁?FCoP report銆侳CoP 鑷韩涔熷湪杩欐绐佺牬涓畬鎴愯湑鍙橈細浠?鍗忎綔鎵嬪唽"鍗囩骇涓?鍙墽琛岀殑鍗忎綔鍩虹璁炬柦"銆?|
> New reports are welcome. If you tried FCoP in your own setup and something surprising happened 鈥?good or bad 鈥?open an issue or a PR against `essays/`. The protocol evolves through field notes, not committee edits.

## Repository layout

The repo is not *only* Markdown specs: the PyPI package **`fcop`** lives
under `src/fcop/`, **`fcop-mcp`** is a separate subproject under `mcp/`, and
there are `tests/`, `docs/`, and `adr/` alongside the essays and specs.

```
FCoP/
鈹溾攢鈹€ src/fcop/                    # `fcop` package: Project API; `rules/_data/`
鈹?                               # bundles fcop-rules / fcop-protocol (templates for `init` deploy)
鈹溾攢鈹€ mcp/                         # `fcop-mcp` subproject (MCP server; has its own pyproject)
鈹溾攢鈹€ tests/                       # pytest for `fcop` and `fcop-mcp`
鈹溾攢鈹€ spec/                        # Normative spec (see spec/README.md)
鈹?  鈹溾攢鈹€ fcop-3.0-spec.md         # 鈽?English normative spec (FCoP 3.0, canonical)
鈹?  鈹溾攢鈹€ fcop-3.0-spec.zh.md      # Chinese parallel (informative)
鈹?  鈹溾攢鈹€ fcop-3.0-rfc.md          # IETF-style RFC edition (English)
鈹?  鈹溾攢鈹€ fcop-3.0-rfc.zh.md       # IETF-style RFC edition (Chinese)
鈹?  鈹溾攢鈹€ schemas/                 # 8 JSON Schemas (machine-readable)
鈹?  鈹斺攢鈹€ archived/                # v1.0 / v1.1 / 0.7.x spec drafts (superseded, retained for history)
鈹溾攢鈹€ docs/                        # Getting-started, migrations, releases, MCP tools
鈹?  鈹斺攢鈹€ getting-started.en.md   # 鈫?start here if new to FCoP
鈹溾攢鈹€ adr/                         # Architecture decision records (ADR-0001..0022)
鈹溾攢鈹€ .github/workflows/           # CI
鈹溾攢鈹€ pyproject.toml               # Root `fcop` package and tooling
鈹溾攢鈹€ essays/
鈹?  鈹溾攢鈹€ when-ai-organizes-its-own-work.en.md
鈹?  鈹溾攢鈹€ when-ai-organizes-its-own-work.md
鈹?  鈹溾攢鈹€ fcop-natural-protocol.en.md
鈹?  鈹溾攢鈹€ fcop-natural-protocol.md
鈹?  鈹溾攢鈹€ fcop-natural-protocol-evidence/
鈹?  鈹溾攢鈹€ fcop-tmpa-lineage.en.md
鈹?  鈹溾攢鈹€ fcop-tmpa-lineage.md
鈹?  鈹溾攢鈹€ when-ai-vacates-its-own-seat.en.md
鈹?  鈹溾攢鈹€ when-ai-vacates-its-own-seat.md
鈹?  鈹溾攢鈹€ when-ai-vacates-its-own-seat-evidence/
鈹?  鈹溾攢鈹€ what-agents-say-about-fcop.en.md
鈹?  鈹斺攢鈹€ what-agents-say-about-fcop.md
鈹溾攢鈹€ examples/workspace-example/
鈹溾攢鈹€ integrations/windows-file-association/
鈹溾攢鈹€ assets/
鈹溾攢鈹€ LICENSE
鈹斺攢鈹€ README.md / README.zh.md
```

## 30-second quickstart

FCoP is **adopted**, not a long-running daemon. The current **rule split**
is **[`fcop-rules.mdc`](src/fcop/rules/_data/fcop-rules.mdc)** (charter) plus
**[`fcop-protocol.mdc`](src/fcop/rules/_data/fcop-protocol.mdc)**
(commentary) 鈥?both belong under **`.cursor/rules/`**. The single file
[`spec/codeflow-core.mdc`](spec/codeflow-core.mdc) is a **deprecated stub** so
old links do not 404 鈥?it is *not* the full protocol text for 0.6+.

**Path A 鈥?`fcop` library (recommended).** One shot creates
`fcop/` and `fcop.json`:

```python
from fcop import Project
Project(".").init()  # default dev-team; use .init_solo() for single-AI
```

**Path B 鈥?rules only, no Python.** Copy the two `.mdc` files from this repo
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

| You want to鈥?| Go to |
|---|---|
| Install `fcop-mcp` into Cursor / Claude Desktop step-by-step | [`mcp/README.md`](mcp/README.md) |
| Have an agent do the install for you (zero JSON editing) | [`agent-install-prompt.en.md`](src/fcop/rules/_data/agent-install-prompt.en.md) 路 [涓枃](src/fcop/rules/_data/agent-install-prompt.zh.md) (also live as MCP resource `fcop://prompt/install`) |
| Upgrade an existing `0.6.x` install (both packages in lockstep + protocol-rule refresh) | [`docs/upgrade-fcop-mcp.md`](docs/upgrade-fcop-mcp.md) |
| Browse all 45 MCP tools and 14 resources by category | [`docs/mcp-tools.md`](docs/mcp-tools.md) |
| Read the per-release record (what changed when, why) | [`CHANGELOG.md`](CHANGELOG.md) and [`docs/releases/`](docs/releases/) |

**Recent releases** (full notes in [`docs/releases/`](docs/releases/)):

| Version | One-line |
|---|---|
| **3.2.2** ([CHANGELOG](CHANGELOG.md)) | **v3.2.2 鈥?Deep history archiving + 10 new MCP tools (35 鈫?45).** Adds history/YYYY-MM-DD/ date-sharded long-term archive layer; new tools: create_task, rchive_to_history, ulk_archive_to_history, list_history, get_history_stats, search_history, move_to_history, cleanup_history, export_history, import_from_history. Manual and scheduled archiving of completed task-report pairs into history/. Both cop and cop-mcp align to 3.2.2 (lockstep). |
| **3.0.2** ([CHANGELOG](CHANGELOG.md)) | **v3.0.2 鈥?Init topology fix.** `Project._apply_init` in 3.0.0 / 3.0.1 only created the legacy v2 buckets and skipped the mandatory v3 `_lifecycle/{inbox,active,review,done,archive}/` layer (spec 搂1.1). 3.0.2 makes fresh init produce the v3 topology directly (and stops creating the superseded v2 `tasks/` / `log/` buckets); `core.events.scan_workspace` and `Project.role_occupancy()` now read from `_lifecycle/` for v3 projects. New audit scan `_scan_lifecycle_topology_compliance()` (D9): P0 when initialised projects miss both `_lifecycle/` and v2 content; P1 when both topologies coexist (suggests `migrate --to-v3`). MCP tool descriptors (`init_solo` / `init_project` / `create_custom_team`) updated. 1209 tests green. Patch (SemVer): no API surface changes vs 3.0.1 鈥?init was simply doing the wrong thing. |
| **3.0.1** ([CHANGELOG](CHANGELOG.md)) | **v3.0.1 鈥?Path-consolidation patch.** Pure docs/metadata patch with no code-logic changes: after v3.0.0 moved historical v1.0/v1.1 spec drafts to `spec/archived/`, this patch repairs broken links scattered across `AGENTS.md` / `CLAUDE.md` / packaged Cursor rules / MCP server docstrings / two JSON Schema `description` fields, unifying them on `spec/archived/fcop-runtime-protocol-v1.0.{md,zh.md}` (with pointers to the current canonical `spec/fcop-3.0-spec.md`). `fcop-mcp`'s `fcop://spec` / `fcop://spec/en` docstrings are corrected to reflect the wheel's actual packaged content (`fcop-spec-v1.1.{lang}.md`). Historical artifacts (TASK / REPORT / ADR / release notes / migration docs) are preserved verbatim per ADR-0036 "history is not rewritten". 1202 tests green. |
| **3.0.0** ([CHANGELOG](CHANGELOG.md)) | **v3.0 鈥?Protocol-level MAJOR 路 "folders-as-state" era.** A complete rewrite of the FCoP protocol body 鈥?canonical two-layer (per [ADR-0040](adr/ADR-0040-canonical-one-liner-two-layer-convention.md)): **Layer 1** "Files are the protocol; location defines state; events record history" + **Layer 2** semantic ontology. Adds `_lifecycle/{inbox,active,review,done,archive}/` five-bucket directory topology (**incompatible with 2.x**, requires `fcop migrate --to-v3`); three rule sets (State Layer Rule A/B/C 路 Event Layer Rule E/F/G 路 Boundary Charter); 7 allowed transitions 鈥?anything off-table MUST be rejected by implementations; write-then-rename atomicity (events ARE migrations, migrations ARE events); ADR-0037 Custody Layer **was withdrawn during RFC review and never reached Accepted** (custody is not a protocol layer; preserved as a NOTE-style derivative explanation). Adds [`spec/fcop-3.0-spec.md`](spec/fcop-3.0-spec.md) single-page canonical + IETF-style RFC parallel + Chinese parallel + [`docs/MIGRATION-3.0.md`](docs/MIGRATION-3.0.md) migration guide. |
| **2.0.2** ([CHANGELOG](CHANGELOG.md)) | **v2.0.2 鈥?`fcop-mcp` officially registered to the [MCP registry](https://registry.modelcontextprotocol.io/) (`io.github.joinwell52-AI/fcop`).** Backed by Anthropic + GitHub + Microsoft's joint registry, `fcop-mcp` is now discoverable by Claude Desktop / Cursor / PulseMCP / every MCP-compatible client out of the box (`uvx fcop-mcp` one-liner install). Double-pack lockstep version bump (per ADR-0002): `fcop` library code is **unchanged** from v2.0.0; the bump aligns both package version numbers and consolidates the fcop-mcp@2.0.1 MCP-metadata patch that landed the same day. Also lands the **release+backup one-shot SOP** 鈥?`RULES-release-file-inventory.md` (12-category), `RULES-mcp-registry-release.md` (3-step path), and the append-only backup mirror at `joinwell52-AI/FCoP-backup`. |
| **2.0.0** ([CHANGELOG](CHANGELOG.md)) | **v2.0 鈥?"Two-diagram era" philosophical major release.** Same execution surface as v1.x (per ADR-0003 additive); the major bump records that FCoP is now defined by **two** diagrams together: the **execution stack** (5-layer vertical, stable since v1.x) *and* the **FCoP Semantic Evolution Loop** (7-node closed loop 鈥?emerge 鈫?observe 鈫?propose 鈫?review 鈫?merge 鈫?deploy 鈫?reflect, newly canonicalised). Adds Rule 4.6 (`fcop/internal/` vs `docs/` + `essays/` soft convention with `internal-only` declaration v1), `Project.init(deploy_internal_template=...)` opt-in, P3 (suggestion) audit severity, and a bundled `fcop_audit` exemption list (`log/`, `_archive/`, `legacy-non-protocol/`) that fixes three upstream bugs surfaced by codeflow cross-project patrol (ISSUE-008/009/010). ADR-0034. |
| **1.6.0** ([CHANGELOG](CHANGELOG.md)) | **v1.6 鈥?Trailing-slug filename adoption (ADR-0033).** Long filenames (`TASK-20260512-025-PM-to-OPS-phase-a-fix-naming.md`) are now first-class 鈥?codeflow's 22+ self-emerged examples absorbed into the grammar. Slug does **not** participate in routing; it's a human-readable label. 100% backward-compatible (0 regressions across 1057 tests). |
| **1.5.0** ([CHANGELOG](CHANGELOG.md)) | **v1.5 鈥?Protocol-awareness sync + `RULE_DOC_DRIFT`.** 84 role/team docs synced to v1.4 protocol surface (REVIEW envelope / `risk_level` / `fcop_audit` / `supersedes:`); new `Project._scan_outdated_role_docs()` with `RULE_DOC_DRIFT` (P1) violation type. |
| **1.4.0** ([notes](docs/releases/1.4.0.md)) | **v1.4 鈥?Write-side bind enforcement (P0 security) + `supersedes:` field.** 15 write-side MCP tools refuse cwd fallback (`WriteRefused`); Protected Path deny-list (HOME / APPDATA / drive roots / Unix system dirs); new `supersedes:` frontmatter field (all envelopes) + `## GATE Design Pitfalls` commentary (`fcop_protocol_version 2.2.0`). |
| **1.3.0** ([notes](docs/releases/1.3.0.md)) | **v1.3 鈥?Governance Alert Layer + Protocol Compiler.** GAL (ADR-0031): 3 drift signals (S1/S3/S4), FCoP-Rule-G1, 2 new alert tools (`fcop_list_alerts`, `fcop_create_alert`). fcop_audit (ADR-0032): three-scenario protocol inspection compiler, 6 scan methods, INSPECTION report with Execution Block. 35 MCP tools total. |
| **1.2.1** ([notes](docs/releases/1.2.1.md)) | **v1.2 鈥?Capability Governance pillar.** `FCoPGovernanceMiddleware` wraps every MCP tool call: Skill Resolver 鈫?Risk Tagging (Safe / Sensitive / Critical) 鈫?append-only `fcop_events.jsonl` audit log. 2 new MCP tools (`list_governance_events`, `get_governance_summary`). `fcop_check()` gains governance event summary. Both `fcop` and `fcop-mcp` align to `1.2.1` (lockstep). ADR-0030-bis. |
| **1.1.0** ([CHANGELOG](CHANGELOG.md)) | **v1.1 鈥?Agent.layer governance contracts + Task.risk_level + Review.needs_human + HumanApproval + Skill.tools[] risk metadata.** 5 new ADRs (0023鈥?027), 4 new MCP tools (`write_review`, `list_reviews`, `read_review`, `mark_human_approved`), `write_task` gains `risk_level` param, new `skill.schema.json`. Fully backward-compatible. |
| **1.0.1** | Spec files bundled in wheel (`get_spec()`); `fcop://spec` MCP resource; workspace paths migrated `docs/agents/` 鈫?`fcop/`; CI green. |
| **1.0.0** | Seven core concepts stabilised: Agent, Encoding, IPC, Event, Failure, Boundary, Audit. JSON Schema for all 7. See [release notes](docs/releases/1.0.0.md). |
| **0.7.2** ([notes](docs/releases/0.7.2.md)) | Metadata patch: fixes `fcop-rules.mdc` frontmatter stale at `1.7.0` (body was already `1.8.0`); adds frontmatter鈫攂ody consistency tests. **No protocol or API change.** |

> **Watch out 鈥?wrong `fcop` on PyPI shadows the library.** Both packages here are published from **this** repository. If `from fcop import Project, Issue` fails after `pip install fcop`, you most likely installed an unrelated `fcop` distribution or another local project shadows the library. Fix: clean venv + reinstall both packages from PyPI in lockstep. The verify commands are in [`mcp/README.md`](mcp/README.md).

**Library** 鈥?use from any Python script or agent:

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
                           rationale="Irreversible infra change 鈥?escalate.")
proj.mark_human_approved(review.review_id, approver="ADMIN",
                         decision="approve", channel="cli")
```

**MCP server** 鈥?add to `mcp.json` (Cursor) or `claude_desktop_config.json`:

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
路 [涓枃](src/fcop/rules/_data/agent-install-prompt.zh.md)) 鈥?the agent
detects your OS, installs `uv`, edits your `mcp.json` (preserving
existing servers), and tells you when to restart. After install the
same prompt is also available as the MCP resource
`fcop://prompt/install`. The prompt explicitly forbids the agent from
auto-initialising a project after install 鈥?initialisation is ADMIN's
three-way choice (solo / preset team / custom).

Stability contract: **additive-only for the full `0.6.x` minor**. Details in [`adr/ADR-0003-stability-charter.md`](adr/ADR-0003-stability-charter.md).

> **Upgrading from 0.7.x to v1.0?** Default workspace moved from `docs/agents/` to top-level `fcop/` (per [ADR-0022](adr/ADR-0022-workspace-directory-convention.md)). Run `fcop migrate-workspace --apply` for one-shot git-aware migration, or pin via `Project(workspace_dir="docs/agents")` to stay on the legacy layout. Full walkthrough 鈥?including the 4 new abstractions (REVIEW / Failure / Boundary / Event) and JSON Schema integration 鈥?in [`docs/MIGRATION-1.0.md`](docs/MIGRATION-1.0.md).
>
> **Upgrading from 0.5.x?** The MCP server moved from `fcop` to `fcop-mcp` 鈥?update your `mcp.json` to `uvx fcop-mcp`. See [`docs/MIGRATION-0.6.md`](docs/MIGRATION-0.6.md) for the full migration guide and the [0.6.0 release record](docs/releases/0.6.0.md) for what shipped.

## How to read FCoP docs

| Your goal | Start here |
|---|---|
| **New to FCoP** 鈥?hands-on 45-min setup | [`docs/getting-started.en.md`](docs/getting-started.en.md) |
| **Upgrading from 0.7.x** 鈥?workspace migration + new abstractions | [`docs/MIGRATION-1.0.md`](docs/MIGRATION-1.0.md) |
| **Upgrading from 1.0/1.1 鈫?1.2** 鈥?Capability Governance + lockstep versioning | [`docs/MIGRATION-1.1.md`](docs/MIGRATION-1.1.md) 路 [CHANGELOG](CHANGELOG.md) |
| **Understand the protocol contract** 鈥?what an implementation MUST do | [`spec/fcop-3.0-spec.md`](spec/fcop-3.0-spec.md) 鈥?single-page canonical spec (v3.0). Earlier v1.0/v1.1 spec drafts remain in `spec/` for historical reference. |
| **v1.2 Capability Governance** 鈥?FCoPGovernanceMiddleware, risk tagging, audit log | [CHANGELOG](CHANGELOG.md) 路 ADR-0030-bis |
| **v1.1 new fields** 鈥?risk_level, needs_human, human_approval, skill tools | [CHANGELOG](CHANGELOG.md) 路 ADR-0023..0027 |
| **Understand why decisions were made** 鈥?reasoning behind each choice | [`adr/`](adr/) 鈥?start with [ADR-0029](adr/ADR-0029-fcop-behavior-governance-charter.md) |
| **All 45 MCP tools & 14 resources** | [`docs/mcp-tools.md`](docs/mcp-tools.md) |
| **Release notes** 鈥?full changelog | [`CHANGELOG.md`](CHANGELOG.md) |
| **Full document map** 鈥?every file and its role | [`adr/README.md`](adr/README.md) (ADR index) + [`spec/fcop-3.0-spec.md`](spec/fcop-3.0-spec.md) 搂11 (Cited Material) |

---

## Design principles

1. **Filename is the single source of truth.** Directory + filename define the state; frontmatter is redundant metadata.
2. **Atomicity comes from `rename()`.** Nothing else. No locks, no transactions.
3. **Human-machine isomorphism.** The same artefact a human reads with `cat` is what agents parse. No debug mode, no admin console.
4. **Identity determines path.** The role slug in the filename _is_ the permission model. An agent whose identity doesn't match won't touch the file.
5. **Infrastructure-free.** If you have a filesystem, you have FCoP. Works on a laptop, on a cluster, across machines via `rsync`.

## Reference implementations

Two official reference implementations, both MIT-licensed:

1. **`fcop` / `fcop-mcp`** 鈥?Python library + MCP server for the protocol. Source in this repository under [`src/fcop/`](src/fcop/) and [`mcp/src/fcop_mcp/`](mcp/src/fcop_mcp/). Installed via PyPI (see section above).
2. **Stub path**: `spec/codeflow-core.mdc` is only a **URL placeholder** (no full body). **Normative** rules are `src/fcop/rules/_data/fcop-rules.mdc` + `fcop-protocol.mdc`.

## Status & versioning

- **Current release**: `v3.2.2` (2026-05-22) 鈥?**Init topology fix.** Critical patch: `Project._apply_init` in 3.0.0 / 3.0.1 only created the legacy v2 buckets and skipped the mandatory v3 `_lifecycle/{inbox,active,review,done,archive}/` layer required by spec 搂1.1 鈥?every fresh project initialised on those releases was therefore born non-compliant. 3.0.2 makes fresh init produce the v3 topology directly (and stops creating the superseded v2 `tasks/` / `log/` buckets); `core.events.scan_workspace` and `Project.role_occupancy()` now read from `_lifecycle/` for v3 projects. New audit scan `_scan_lifecycle_topology_compliance()` (D9): P0 when initialised projects miss both `_lifecycle/` and v2 content; P1 when both topologies coexist (suggests `migrate --to-v3`). MCP tool descriptors (`init_solo` / `init_project` / `create_custom_team`) updated. 1209 tests green. Patch (SemVer): no API surface changes 鈥?init was doing the wrong thing. Predecessor **v3.0.1** (2026-05-21) 鈥?Path-consolidation patch (docs-only). Predecessor **v3.0.0** (2026-05-21) 鈥?**Protocol-level MAJOR 路 "folders-as-state" era**: a complete rewrite of the FCoP protocol body 鈥?canonical two-layer (per [ADR-0040](adr/ADR-0040-canonical-one-liner-two-layer-convention.md)) "Files are the protocol; location defines state; events record history" + semantic ontology; adds `_lifecycle/{inbox,active,review,done,archive}/` five-bucket directory topology (**incompatible with 2.x**, requires `fcop migrate --to-v3`); three rule sets (State / Event / Boundary Charter) + 7 allowed transitions (off-table MUST be rejected) + write-then-rename atomicity; ADR-0037 Custody Layer **was withdrawn during RFC review and never reached Accepted**. See [`spec/fcop-3.0-spec.md`](spec/fcop-3.0-spec.md) and [`docs/MIGRATION-3.0.md`](docs/MIGRATION-3.0.md). Earlier releases: v2.0.2 (fcop-mcp registered to official MCP registry), v2.0.0 (two-diagram philosophical major bump + Rule 4.6 `fcop/internal/`), v1.6 (trailing-slug filename grammar, ADR-0033), v1.5 (84-doc protocol-awareness sync), v1.4 (write-side bind + `supersedes:` correction), v1.3 (GAL + `fcop_audit()` inspection compiler). See [CHANGELOG](CHANGELOG.md).
- **Normative spec**: [`spec/fcop-3.0-spec.md`](spec/fcop-3.0-spec.md) 鈥?single-page canonical (v3.0; supersedes v1.0/v1.1 drafts retained for history) 路 machine-readable contracts in [`spec/schemas/`](spec/schemas/) (8 schemas)
- **Agent rules (`.mdc`) in this repo**: [`src/fcop/rules/_data/fcop-rules.mdc`](src/fcop/rules/_data/fcop-rules.mdc) + [`fcop-protocol.mdc`](src/fcop/rules/_data/fcop-protocol.mdc) (`spec/codeflow-core.mdc` is a deprecated stub)
- **Change log**: [`CHANGELOG.md`](CHANGELOG.md)
- **Research snapshot**: [`research-snapshot-2026-04-29`](https://github.com/joinwell52-AI/FCoP/releases/tag/research-snapshot-2026-04-29) archived on Zenodo with a citable DOI (see *How to cite* below).

## How to cite

If FCoP 鈥?the protocol, the field-report essays, the tutorials, or the reference implementations 鈥?informs your research, software, or writing, please cite the [Zenodo research snapshot](https://doi.org/10.5281/zenodo.19886036):

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

For citations of individual essays or tutorials, the same DOI applies 鈥?please reference the essay's filename (e.g. `essays/what-agents-say-about-fcop.en.md`) and the snapshot version in your citation note.

## Contributing

This repository is intentionally small and stable. Protocol evolution happens through real-world reports, not committee edits. The highest-leverage contributions are:

1. **Field reports.** Try FCoP on your own agent team and open an issue with what broke, what the agents invented, what naming conventions emerged.
2. **Ports & SDKs.** Thin wrappers for Python / TypeScript / Go that implement the filename parser and `rename()` state transitions.
3. **Editor / MCP integrations.** Syntax highlighting for `.fcop` files, MCP bridges that expose the folder to other agent runtimes.

PRs to the spec itself should link to the concrete problem they're solving.

## License

MIT 鈥?see [LICENSE](LICENSE).

## Credits

FCoP emerged from hands-on collaboration with multi-agent Cursor-style workflows. Many of the conventions in this spec were first invented by those agents and then codified here. Details are in the [field report](essays/when-ai-organizes-its-own-work.en.md).
