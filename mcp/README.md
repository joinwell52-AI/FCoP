# fcop-mcp

mcp-name: io.github.joinwell52-AI/fcop

> Unpublished WP4D candidate: both packages target `4.0.0rc1` (Beta).
> Candidate installation must use the exact WP4D Actions artifacts and hashes,
> in a fresh external venv. No PyPI, Registry, GitHub Release, main merge,
> existing-workspace upgrade or rule redeployment is authorized.
> The historical public-install instructions below are not candidate instructions.

**MCP (stdio) server** — the optional **IDE bridge** for the same FCoP stack. It
wraps the official [`fcop`](https://pypi.org/project/fcop/) library; it is **not**
a second “FCoP product” and does not replace the protocol text.

- **What FCoP is (protocol only, product-agnostic):** [`docs/getting-started.en.md`](../docs/getting-started.en.md) (中文 [`getting-started.md`](../docs/getting-started.md))  
- **Pure Python lib / `pip install fcop`:** filesystem + Project API, PyYAML and jsonschema — [PyPI `fcop`](https://pypi.org/project/fcop/) (see that package’s `description` and **Documentation**).
- **This package (`fcop-mcp`):** `pip install fcop-mcp` — stdio tools/resources for clients; same repo, folder `mcp/`.  
- **Source home:** [joinwell52-AI/FCoP](https://github.com/joinwell52-AI/FCoP)

**🎯 v3.2.4 — PyPI metadata & bundled protocol fix** (2026-05-27). Also: official MCP registry package, docs aligned with FCoP 3.0.  
`fcop-mcp` remains registered as `io.github.joinwell52-AI/fcop` in the [official MCP registry](https://registry.modelcontextprotocol.io/), and is discoverable from Claude Desktop / Cursor / PulseMCP and other MCP-compatible clients (`uvx fcop-mcp`). This release synchronizes team-template and rule-document references to the v3 `_lifecycle/` topology and keeps `fcop` / `fcop-mcp` lockstep semantics (ADR-0002).

**Upgrading from older lines (`0.6.x` / `0.7.x` / `1.x` / `2.x`)?** See [**`docs/upgrade-fcop-mcp.md`**](https://github.com/joinwell52-AI/FCoP/blob/main/docs/upgrade-fcop-mcp.md) — install in the MCP venv (`pip install -U fcop fcop-mcp`), restart IDE, then run `redeploy_rules()` once to refresh on-disk rule files.

**Surface:** the historical released 3.2.5 baseline has **45 tools**. This
unpublished candidate has **46 tools / 12 static resources / 4 templates**:
`reopen_task` is the sole additional tool; WP4C adds version-selected guidance
and team resources. Discovery is checked through stdio by the external sample.

### Unpublished 4.0.0rc1 v4 adapter

The candidate requires `fcop>=4.0.0rc1,<4.1.0` and accepts the exact installed
`4.0.0rc1 / 4.0.0rc1` pair. The historical `3.2.5 / 3.2.5` pair remains solely
for legacy/source compatibility checks; mixed installed pairs fail closed.
The copied stdio-only sample under `examples/v4/third-party/mcp-only/` has no
client-side FCoP imports and configures its educational Profile at trusted
server startup. It does not establish a production credential policy.

`fcop-mcp` defaults to stdio. `fcop-mcp --relay-url wss://<explicit-endpoint>`
selects a foreground standard-MCP JSON-RPC WebSocket transport; its direct
dependency is in `fcop-mcp[relay]`. FastMCP itself may install `websockets`
transitively. Presence of that package, `FCOP_ROOM_KEY` or `FCOP_RELAY_WS_URL`
does **not** enable FCoP Relay. No connection is made by base stdio startup.

Trusted application startup can use:

```python
from fcop_mcp.server import create_server

server = create_server(workspace_path, trusted_profiles={profile_ref: evaluator})
server.run(transport="stdio")
```

The registry is copied at construction and defaults to empty. It is never
populated by tool requests, manifest fields, Profile documents or actor names.
v4 T4–T7 without a trusted adopted evaluator fail in Core.

For v4, `init_solo` / `init_project` require explicit `protocol_version="4.0"`
to create a new workspace without legacy rule deployment. TASK creation requires
`workspace_id` and `operation_id`; Branch uses the optional `branch_of` field.
REPORT/ISSUE/REVIEW writers require the corresponding v4 fields, including
`workspace_id`, formal subject and (for REPORT) current `attempt_id`.
`write_review` appends evidence, not a transition.

In v4, `mark_human_approved` delegates exclusively to the existing public
Project method. Supply `review_id`, `approver`, affirmative `decision`,
`profile_ref`, `from_stage`, `to_stage`, the edge's `attempt_id` and (for a
Root T7 with Branches) `family_digest`, `issued_at`, explicit `expires_at`
(which may be null), and `issuer_proof`; `comment` is optional. The Project
derives workspace, subject, recipient and references from existing facts and
stores a new authorization REVIEW with decision `authorize`. A trusted
evaluator must authorize before publication. DENIED/UNKNOWN, invalid binding
or expiry fail with zero writes. The old REVIEW is never edited and no TASK
moves until a separate transition revalidates and consumes the authorization.
`approve`/`approved` are accepted affirmative spellings; rejection never
creates an authorization. v3 retains its original approve/reject behavior.

```json
{
  "name": "reopen_task",
  "arguments": {
    "task_id": "TASK-...",
    "review_ref": "REVIEW-reopen-...",
    "authorization_ref": "REVIEW-independent-authorization-...",
    "profile_ref": "profile:adopted-by-trusted-startup",
    "actor": "ME",
    "lang": "en"
  }
}
```

This requests only `done -> active`; Core validates evidence and single-use
authorization and creates the next attempt. An exact retry returns the existing
result. No `operation_id`, attempt, report, family digest, transition selector
or evaluator is accepted by `reopen_task`. The tool rejects v3 workspaces.

`list_reports(task_id=..., attempt_id=..., head_only=True)` and
`read_report(filename=...)` return the requested immutable facts with `is_head`,
`head_ref` and `head_digest`. All graph validation belongs to public Project
readers; pagination cannot hide an ambiguous group. `status="archived"` is
legacy-only, not v4 history authority. Base failures are standard MCP error
results (`isError=true`) with structured `code`, `operation_ref`, `subject_ref`.

`fcop://spec` and `/en` are version-routed projections with source SHA-256.
v4 rule Manifest and protocol identity objects are deterministically projected
as Markdown, and sequential/parallel guidance is read-only. Legacy v3 protocol
Markdown bytes and MIME remain unchanged. File projection does not prove Runtime
consumption; Host adoption/deployment remain explicit Project operations.
Profile resources remain read-only catalog documents and never grant authority.
Existing product-only rule deployment/GAL/governance extensions are not
relabelled as v4 Core; unsupported v4 projections return typed unavailability.

中文：本 review 版本尚未发布；历史 45 项工具保留，仅新增 T6 `reopen_task`，
合计 46 项。可信 Profile 只能在 server 初始化时注册。v4 查询委托公共
Project，零 head／多 head 分别返回 `REPORT_REQUIRED`／
`REPORT_HEAD_AMBIGUOUS`；旧 REPORT 可读取，但明确显示并非当前 head。
不得把历史安装说明中的升级、规则重部署步骤用于本轮现有工作区。

**0.6.3 ships [ADR-0006](https://github.com/joinwell52-AI/FCoP/blob/main/adr/ADR-0006-host-neutral-rule-distribution.md)** — host-neutral protocol-rule distribution. New tool **`fcop_report`** is now the canonical session/init report (its header carries a `[Versions]` block that flags drift between the wheel-bundled rules and the project-local `.cursor/rules/` copy). New ADMIN-only tool **`redeploy_rules`** writes the four protocol-rule targets — `.cursor/rules/fcop-rules.mdc`, `.cursor/rules/fcop-protocol.mdc`, `AGENTS.md`, `CLAUDE.md` — so Cursor, Claude Code CLI, and Codex CLI all see the same rules. Legacy **`unbound_report`** stays as a deprecated alias of `fcop_report` (emits `DeprecationWarning`, removed in 0.7.0). See [`docs/releases/0.6.3.md`](https://github.com/joinwell52-AI/FCoP/blob/main/docs/releases/0.6.3.md) for the full migration story.

> The **`fcop`** on PyPI **must** be the **FCoP library** (summary mentions *File-based Coordination Protocol*, `pyyaml`, no `fastmcp` inside `fcop`). If `pip show fcop` says *MCP toolbox* or `from fcop import Issue` fails, you have a **wrong** distribution — fix with a clean venv and reinstall (see *Verify* below).

---

## Historical published 3.x guide — not WP4D candidate installation

The following public-index and upgrade instructions describe the released line.
Do not execute them as part of WP4D or against an existing development workspace.

## TL;DR — Have an agent install fcop-mcp for you

Don't want to read the rest of this page? Open a fresh chat with any
shell-capable AI agent (Cursor with a new tab, Claude Code CLI, Codex
CLI…) and **paste this prompt verbatim**. The agent will detect your
OS, install `uv`, edit your `~/.cursor/mcp.json` (preserving every
other server you already have), and tell you when to restart.

```text
Install fcop-mcp into Cursor for me — you run the commands end to end.

1. Detect my OS first: in the terminal, run
   `uname -s 2>$null; echo $env:OS` to see whether this is Windows
   or macOS / Linux.

2. Install uv (if not already present). One-liner:
   - Windows PowerShell:
     powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   - macOS / Linux:
     curl -LsSf https://astral.sh/uv/install.sh | sh
   Then run `uvx --version` to confirm.

3. Add an fcop entry to the global mcp.json. **Preserve** existing
   mcpServers — do not overwrite them.
   - Windows path: %USERPROFILE%\.cursor\mcp.json
   - macOS / Linux path: ~/.cursor/mcp.json
   - Add this snippet inside the mcpServers object:
     "fcop": {
       "command": "uvx",
       "args": ["fcop-mcp"]
     }

4. Print the final mcp.json contents back to me.

5. Remind me to restart Cursor; on first launch fcop-mcp will pull
   dependencies, **wait 30 seconds to 1 minute**, do not close or
   reconnect early.

Report back after each step before moving on. **Do not** auto-init
a project after install — initialization is my (ADMIN's) choice; I
will pick solo / dev-team / custom myself.
```

中文版本 / Chinese version: see
[`agent-install-prompt.zh.md`](https://github.com/joinwell52-AI/FCoP/blob/main/src/fcop/rules/_data/agent-install-prompt.zh.md)
in the repo, or after install read the MCP resource
`fcop://prompt/install`.

> **Why the "do not auto-init" line?** Initialisation is ADMIN's
> three-way choice (`solo` / preset team / custom). 0.6.3 had agents
> defaulting to `init_project(team="dev-team")`, which silently
> overwrote ADMIN's intended Solo flow. 0.6.4 makes the prompt and
> the `fcop_report` Phase-1 message say the choice out loud and
> forbid the agent from picking on ADMIN's behalf.

---

## One-page install (what we recommend for customers)

**Goal:** a dedicated Python environment for MCP only, so no other project’s `.pth` or wrong `fcop` shadows the real library.

### A. Recommended: dedicated venv + `python -m fcop_mcp`

1. **Python 3.10+** on `PATH` (3.10–3.13 tested in CI; avoid very new 3.14 until CI covers it).
2. Create a venv (paths are examples — adjust if you like):

**Windows (PowerShell)**

```powershell
$v = "$env:USERPROFILE\.cursor\fcop_mcp_venv"
py -3.10 -m venv $v
& "$v\Scripts\pip.exe" install -U pip
& "$v\Scripts\pip.exe" install -U "fcop" "fcop-mcp"
```

**macOS / Linux**

```bash
VENV="$HOME/.cursor/fcop_mcp_venv"
python3 -m venv "$VENV"
"$VENV/bin/pip" install -U pip
"$VENV/bin/pip" install -U "fcop" "fcop-mcp"
```

3. **Cursor** user config — file:

- Windows: `%USERPROFILE%\.cursor\mcp.json`
- macOS / Linux: `~/.cursor/mcp.json`

Add or merge (use the **real** `python` path from step 2):

```json
{
  "mcpServers": {
    "fcop": {
      "command": "C:\\Users\\YOUR_USER\\.cursor\\fcop_mcp_venv\\Scripts\\python.exe",
      "args": ["-m", "fcop_mcp"]
    }
  }
}
```

On macOS, `command` is like `/Users/YOUR_USER/.cursor/fcop_mcp_venv/bin/python`.

4. **Fully restart Cursor** (or *Developer: Reload Window*), then open MCP and confirm `fcop` is connected.

**Why this path?** `uvx` (below) is convenient but **first run** can take a long time to download dependencies; some MCP hosts time out. A fixed venv avoids that and avoids **name conflicts** with other editable installs of `fcop` on the same machine.

---

### B. Alternative: `uvx fcop-mcp` (quickest to try, slower cold start)

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

Install [uv](https://docs.astral.sh/uv/) first. **First connection** may download many wheels — **wait** for it; don’t spam reconnect. If you see *Aborted* or timeouts, use **A** above.

---

## Verify (2 commands)

In the **same** venv you use for MCP:

```bash
python -c "from fcop import Issue, Project; print('fcop OK', Project)"
python -c "from fcop_mcp.server import mcp; print('fcop-mcp OK')"
```

If the first line fails, **`fcop` is not the FCoP library** — uninstall and reinstall in a **clean** venv (`fcop` / `fcop-mcp` from PyPI, **same version in lockstep** per [ADR-0002](https://github.com/joinwell52-AI/FCoP/blob/main/adr/ADR-0002-package-split-and-migration.md); e.g. `fcop 3.2.x` + `fcop-mcp 3.2.x`).

---

## Claude Desktop

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`  
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`  

Use the same `command` / `args` as Cursor (either **A** with your venv `python`, or **B** with `uvx`).

---

## Upgrading from `uvx` / `args: ["fcop"]` (0.5.x)

```json
"fcop": { "command": "uvx", "args": ["fcop-mcp"] }
```

The `mcpServers` key name can stay `"fcop"`. Full guide:  
[`docs/MIGRATION-0.6.md`](https://github.com/joinwell52-AI/FCoP/blob/main/docs/MIGRATION-0.6.md)

---

## Where the server looks for the project

Resolution order (see [ADR-0003](https://github.com/joinwell52-AI/FCoP/blob/main/adr/ADR-0003-stability-charter.md)):

1. Last `set_project_dir` in this MCP session  
2. `FCOP_PROJECT_DIR`  
3. Legacy 0.5.x env var `CODEFLOW_PROJECT_DIR` (still recognized with a deprecation warning — use `FCOP_PROJECT_DIR`)  
4. Walk up from cwd for any of these markers (first hit wins):
   - `.cursor/rules/fcop-rules.mdc` (present after `init_*` on v3 projects)
   - `docs/agents/fcop.json` or `docs/agents/tasks/` (legacy 0.7.x layout)
5. Current working directory (last resort)

Write guards additionally accept `fcop/fcop.json` (v1.0+ / v3 default workspace) or legacy `docs/agents/fcop.json`. v3 coordination files live under `fcop/_lifecycle/`; see [`docs/getting-started.en.md`](../docs/getting-started.en.md).

To pin a folder in config:

```json
"env": { "FCOP_PROJECT_DIR": "D:/path/to/your/repo" }
```

---

## Stability (3.x)

Within a single **MINOR** line (e.g. `3.2.x`), MCP tool/resource **shapes** stay **additive-only** ([stability charter, ADR-0003](https://github.com/joinwell52-AI/FCoP/blob/main/adr/ADR-0003-stability-charter.md)): no renames, no required-parameter tightening, no resource removal. Patch releases do not break existing tool calls.

`fcop` and `fcop-mcp` ship **lockstep** with the same version number ([ADR-0002](https://github.com/joinwell52-AI/FCoP/blob/main/adr/ADR-0002-package-split-and-migration.md)). Install both together, e.g. `pip install -U "fcop>=3.2.5,<3.3" "fcop-mcp>=3.2.5,<3.3"`. **Avoid PyPI 3.2.3** (bad bundled `fcop-protocol.mdc` encoding).

Upgrading from `0.6.x` / `0.7.x` / `1.x` / `2.x`? See [`docs/upgrade-fcop-mcp.md`](https://github.com/joinwell52-AI/FCoP/blob/main/docs/upgrade-fcop-mcp.md) and the release notes under [`docs/releases/`](../docs/releases/). v3.0.0 introduced the `_lifecycle/` topology — run `fcop_audit(scope="upgrade")` then `migrate_to_v3()` on unmigrated v2 workspaces.

---

## License

MIT — see [`LICENSE`](../LICENSE).
