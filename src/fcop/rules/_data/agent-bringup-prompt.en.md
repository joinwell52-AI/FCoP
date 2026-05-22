# Bring Up an FCoP Project Through an Agent (defensive prompt / en)

Send the block below to a **fresh agent session** — works for upgrading
fcop, creating a new FCoP project, or taking over a project on a new
machine.

This prompt is written for **weak models**: every step is spelled out,
no improvisation, must stop and report after each step. Strong models
should follow it too — a few extra steps beat a derailed run.

> Source of truth: this file lives in the fcop repo at
> `src/fcop/rules/_data/agent-bringup-prompt.en.md` and is also exposed
> as MCP resource `fcop://prompt/bringup/en`. It pairs with
> `agent-install-prompt.en.md` — that one covers "install fcop-mcp into
> Cursor"; this one covers "now bring the project up".

---

## First, figure out which path you're on

| Scenario | Meaning | Which prompt |
|---|---|---|
| **A · Install fcop-mcp** | fcop-mcp has never been installed on this machine / Cursor has no fcop entry | `agent-install-prompt.en.md` (do that first) |
| **B · New / upgrade FCoP project** | fcop-mcp is already wired into Cursor, you're creating a new empty dir or running latest in an existing one | **this prompt** |

**Only Scenario B applies here.** If fcop-mcp isn't installed yet, go
to the install prompt first.

---

## Copy the block below and send it to your agent

```
Bring up the FCoP project for me. Follow the six steps strictly,
report after each step before moving on — no skipping, no defaulting,
no API guessing.

═══════════════════════════════════════════════════════════════════
§1 · Environment check
═══════════════════════════════════════════════════════════════════

Run these two:

  python --version
  pip show fcop fcop-mcp

Requirements:
- Python ≥ 3.10
- If either fcop / fcop-mcp is missing, tell me "not installed"
- If both are installed, paste the version numbers back to me

Show the raw output. **Stop and wait for me to decide whether to
upgrade** — do not pip install before I say so.

═══════════════════════════════════════════════════════════════════
§2 · Upgrade to latest (no version pin)
═══════════════════════════════════════════════════════════════════

After I say upgrade, run:

  pip install --upgrade --no-cache-dir fcop fcop-mcp

Notes:
- **Do NOT** pin a version like ==X.Y.Z — pull whatever PyPI ships
- Same command for fresh install and upgrade — no scenario branching
- --no-cache-dir avoids stale local wheels

Confirm versions:

  python -c "import fcop, fcop_mcp; print('fcop:', fcop.__version__, '/ fcop-mcp:', fcop_mcp.__version__)"

Paste the version numbers back, **stop** and let me decide if it's
fresh enough.

═══════════════════════════════════════════════════════════════════
§3 · Boundary declaration (most important — read it twice)
═══════════════════════════════════════════════════════════════════

FCoP has TWO interfaces, **do NOT mix them**:

| Type | Names | How to call |
|---|---|---|
| **MCP tools** | fcop_report / init_solo / init_project / create_custom_team / fcop_audit / write_task / write_report / archive_task / ... | fcop-mcp wired into Cursor's mcp.json, **after Cursor restart** call directly in a fresh chat — NOT via Python import |
| **Python API** | from fcop import Project; Project('.').init(...) | Plain Python library, fallback when MCP isn't available |

**Key facts**:
- After `import fcop` you will **NOT find** fcop_report / init_solo as
  attributes — that's normal
- They are MCP tools, not Python functions
- Without fcop-mcp, the **only** legal Python fallback is
  Project('.').init(...)
- **Do NOT invent** function names like fcop.project.Project.init_project(...)

**Known anti-patterns (don't do these)**:
- ❌ init_project(team="ME") — ME is a role code, not a team name; for
   solo use init_solo(role_code="ME")
- ❌ fcop.fcop_report() — fcop_report is an MCP tool, not a Python function
- ❌ Using head / grep in PowerShell — they don't exist on Windows; use
   Select-Object -First / Select-String
- ❌ Inventing fcop.project.Project.init_project(...) when you can't find
   the API
- ❌ Calling init_solo() before ADMIN explicitly chose — init is ADMIN's
   choice, not your default
- ❌ Trusting "ok" from a tool — you MUST physically `ls` to verify the
   directory was actually created

**When unsure**:
- Read fcop/LETTER-TO-ADMIN.md in the project first
- Or docs/getting-started.md
- **Do NOT guess APIs** — stop and ask me

Nothing to execute here, just confirm you understood, then move to §4.

═══════════════════════════════════════════════════════════════════
§4 · Initialization (ADMIN's choice — agent never defaults)
═══════════════════════════════════════════════════════════════════

Call this MCP tool:

  fcop_report()

If the project is uninitialized (fcop/fcop.json missing), it returns
the Phase 1 initialization report listing **three options**:

  1) solo — single AI role
  2) preset team (dev-team / media-team / mvp-team / qa-team)
  3) custom team

Paste the report to me. **Stop** and wait for my pick. After I choose,
call the matching tool:

- solo → init_solo(role_code="ME"  or whatever name I give)
- preset → init_project(team="dev-team")  etc.
- custom → create_custom_team(team_name="...", roles=[...], leader="...")

**Do NOT pick for me.** "Let me bootstrap with dev-team" = Rule 1
violation.

═══════════════════════════════════════════════════════════════════
§5 · Physical verification (critical — tool "ok" is not enough)
═══════════════════════════════════════════════════════════════════

A tool returning "ok" does **NOT** mean the files were actually
created. v3.0.0 / v3.0.1 had exactly this bug — tool said success but
_lifecycle's five buckets were empty (fixed in v3.0.2). So you MUST
verify with ls.

> ⚠️ **v3.0.2 fresh init no longer creates `fcop/tasks/` or `fcop/log/`** —
> spec §6 retired them; they moved to `_lifecycle/inbox/` and
> `_lifecycle/archive/`. Their absence is **expected**, not a failure.
> Old v2 projects upgrade with `python -m fcop migrate --to-v3` —
> that is out of scope for this prompt.

Run (PowerShell):

  ls fcop/_lifecycle/
  ls fcop/
  ls workspace/
  ls .cursor/rules/

Expected layout (v3 topology):

  fcop/
  ├── fcop.json
  ├── LETTER-TO-ADMIN.md
  ├── _lifecycle/                    ← v3 five buckets (must check)
  │   ├── inbox/
  │   ├── active/
  │   ├── review/
  │   ├── done/
  │   └── archive/
  ├── shared/
  │   ├── TEAM-README.md
  │   ├── TEAM-ROLES.md
  │   ├── TEAM-OPERATING-RULES.md
  │   └── roles/{ROLE}.md
  ├── reports/                       ← reports (kept in v3)
  ├── issues/                        ← issues (kept in v3)
  └── reviews/                       ← reviews (kept in v3)

  workspace/
  └── README.md

  .cursor/rules/
  ├── fcop-rules.mdc
  └── fcop-protocol.mdc

  AGENTS.md
  CLAUDE.md

**Special check**:
- The five subdirs under fcop/_lifecycle/ MUST all exist
- Any missing = init didn't fully succeed, **stop** and report me
- Do NOT mkdir manually to "fix" it — that's an fcop library bug,
  escalate via Rule 8

Paste the raw ls output back to me.

═══════════════════════════════════════════════════════════════════
§6 · Health check (final step)
═══════════════════════════════════════════════════════════════════

Call this MCP tool:

  fcop_audit(scope="new")

(If you're taking over an existing project rather than creating new,
use scope="takeover" instead.)

The tool writes fcop/shared/INSPECTION-YYYYMMDD-NNN-new.md. Open it
and paste the **P0 / P1 / P2 counts** to me.

Decision rule:
- **P0 ≠ 0** → project is non-compliant, **stop** and let me decide,
  do NOT auto-remediate
- P1 / P2 are advisory, can wait until I look at them

Health check passed → bringup complete, await my next instruction.
```

---

## Behavioral constraints (recap — repeated above, here as one list)

- After each step you **must** report results, **never** auto-advance.
- When unsure, read project docs (`LETTER-TO-ADMIN.md` /
  `getting-started.md`) — **do not guess**.
- Any `init_*` is ADMIN's choice; agent never defaults for ADMIN.
- Tool "ok" ≠ success — verify with physical `ls`.
- Health check P0 ≠ 0 → stop and report ADMIN, no auto-remediation.

---

## Why a separate bringup prompt

After v3.0.2 shipped, ADMIN ran a fresh-install verification on
another machine (with a weaker-model agent). The agent treated
`fcop_report()` (an MCP tool) as a Python API, couldn't find it, then
started inventing names like `fcop.project.Project.init_project(team="ME")`
(non-existent function), and ran `head` / `grep` in PowerShell —
multiple derailments in one session.

Root cause: the existing `agent-install-prompt.en.md` only covers
"install fcop-mcp into Cursor". The path **after install — how to
bring the project up** — was never frozen in protocol docs. Strong
models infer it; weak models can't.

This prompt freezes the six steps (env check → upgrade → boundary
declaration → init → physical verification → health check) at a
density weak models can follow. It's a live instance of FCoP Rule 4
(Semantic Evolution Loop): observed derailment in the wild gets
absorbed back as a defensive doc.

For deeper protocol context, read `fcop/LETTER-TO-ADMIN.md` —
fcop's complete manual for ADMIN.
