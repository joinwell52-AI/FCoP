# Changelog

All notable changes to the `fcop` and `fcop-mcp` Python packages are recorded
here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and the project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This file tracks both packages together because they release in lockstep.
See [adr/ADR-0002](./adr/ADR-0002-package-split-and-migration.md) for the
versioning strategy.

## [Unreleased]

### Documentation-only sync (destined for 0.6.6, no PyPI bump)

These edits are **docs-only**: `_version.py` for both `fcop` and
`fcop-mcp` stays at `0.6.5`, no PyPI upload, no behavior change. The
next package release (whatever number it takes) will carry the docs
forward. Pinned to a numbered release note for audit trail. See
[`docs/releases/0.6.6.md`](./docs/releases/0.6.6.md) for the
full rationale and verification commands.

- **`docs/mcp-tools.md` resource count**: corrected "资源（resources）
  **10 个**" → "**12 个**" (9 static + 3 templates, matches
  `tool_surface.json` truth). Added the two missing 0.6.4 resource
  rows for `fcop://prompt/install` (zh) and `fcop://prompt/install/en`.
  Appended one-liner 0.6.5 behaviour notes to the `fcop_report` and
  `new_workspace` rows.
- **`mcp/README.md` (PyPI `fcop-mcp` long description)**: appended a
  bilingual one-sentence summary of the 0.6.5 Rule 0.a.1 tripwires to
  the existing "What can the server actually do?" lede. Before this
  patch, PyPI users seeing `fcop-mcp 0.6.5` had no in-page explanation
  of why `new_workspace` started prepending a reminder.
- **`LETTER-TO-ADMIN.{zh,en}.md`**: added one bullet at the bottom of
  the top "0.6.4 摘要" / "0.6.4 in one block:" block describing the
  0.6.5 polish (`new_workspace` reminder + `fcop_report` four-step
  template). Heading text is preserved verbatim so existing letter-intro
  tests keep passing; both bullets land inside the slice that
  `get_letter_intro()` surfaces to ADMIN at init time.

## [0.6.5] - 2026-04-27

Hot-fix release wiring the **Rule 0.a.1 hard constraint** into the
tool layer. 0.6.4 shipped the four-step `task → do → report → archive`
hard constraint as text in 17 role charters and `fcop-rules.mdc`, but
the first real-world solo test (`init_solo` → ADMIN: "做个俄罗斯方块"
→ agent dove straight into code) showed the constraint never **bit**
in practice: the agent could recite the rule perfectly but skipped
Step 1 (`write_task`) anyway, because nothing in the actual tool
return path reminded it at the moment of action. The agent's own
post-mortem nailed the diagnosis: *"是我没有把刚建立的协议作为当前
工作流的硬约束执行到底"* (= "I didn't execute the just-established
protocol as a hard constraint on the current workflow"). 0.6.5 plants
two soft tripwires — non-blocking, additive, ADR-0003 compatible — at
the two moments where agents actually pivot between chat and
artifacts. See [`docs/releases/0.6.5.md`](./docs/releases/0.6.5.md).

### Fixed — Rule 0.a.1 enforcement gap

- **`new_workspace` tripwire (`fcop-mcp`).** When an agent calls
  `new_workspace(slug=...)` and **no open `TASK-*.md` mentions that
  slug** in its `subject` / `body` / `references`, the tool now
  prepends a bilingual Rule 0.a.1 reminder to the response,
  recommending `write_task(...)` as Step 1 *before* dropping
  artifacts. Workspace creation still succeeds (the tripwire is a
  reminder, not a block) so legitimate offline / experimental flows
  are not broken. New helper `_recent_task_mentions_slug()` does the
  scan over `docs/agents/tasks/` (open status only, body+subject+
  references substring match, IO/parse errors swallowed).
- **`fcop_report` four-step template (`fcop-mcp`).** The initialized
  branch of `_compose_session_report()` (a.k.a. the UNBOUND report
  every bound agent re-reads when it self-checks state) now ends with
  an explicit four-step cycle template — `write_task` →
  `new_workspace` → `write_report` → `archive_task` — plus the
  "skipping Step 1 or Step 3 violates Rule 0.a.1" callout. Both `zh`
  and `en` reports get the template; bilingual phrasing matches the
  bilingual rules block in `fcop-rules.mdc` Rule 0.a.1.

### Tests

- `tests/test_fcop_mcp/test_server.py`:
  - `test_new_workspace_warns_when_no_open_task_mentions_slug` —
    fresh project, agent calls `new_workspace` with no matching task
    → response must contain `Rule 0.a.1`, `write_task`, and the
    "before editing any file" callout.
  - `test_new_workspace_silent_when_open_task_mentions_slug` —
    `write_task` first (subject/body mentions slug), then
    `new_workspace` → response must NOT contain the warning.
  - `test_fcop_report_initialized_includes_four_step_template_zh` /
    `_en` — both languages must list all four step verbs / tools and
    the "no `simple = skip`" callout.

### Compatibility / no breaking changes

- All edits are additive per ADR-0003: tool signatures unchanged,
  `tool_surface.json` snapshot unchanged, no new public API,
  `public_surface.json` snapshot unchanged. Existing callers see
  the same return-text *prefix* on the bound branches; only fresh
  scenarios with no matching task get extra prepended copy.

## [0.6.4] - 2026-04-26

Hot-fix release closing the **init-deposit gap** found while writing
the 0.6.3 customer tutorial: when ADMIN started fresh and asked an
agent to initialize an FCoP project, `init_*` was advertising files
(`LETTER-TO-ADMIN.md`, `workspace/`, `shared/` three-layer team
docs) that it never actually wrote. 0.6.4 makes every `init_*` land
its full promised set in a single transaction, ships a Solo template
bundle so single-AI projects no longer hit `TeamNotFoundError`, and
hardens the Phase-1 contract so agents stop defaulting to
`init_project(team="dev-team")` on ADMIN's behalf. All changes are
additive per ADR-0003. See
[`docs/releases/0.6.4.md`](./docs/releases/0.6.4.md).

### Fixed — initialization deposit gap (0.6.3 regression)

- **`init_solo` / `init_project` / `init_custom`** now deposit the
  full advertised set in one call: `docs/agents/fcop.json`,
  `docs/agents/LETTER-TO-ADMIN.md` (the ADMIN manual, picked from
  zh / en per the `lang` argument), `workspace/` cage with a starter
  `workspace/README.md`, the team's three-layer documentation under
  `docs/agents/shared/` (`TEAM-README.md` / `TEAM-ROLES.md` /
  `TEAM-OPERATING-RULES.md` / `roles/{ROLE}.md`, both zh and en),
  and the four host-neutral protocol-rule files
  (`.cursor/rules/*.mdc` + `AGENTS.md` + `CLAUDE.md`). 0.6.3 silently
  skipped the letter, the workspace cage, and the role charters.
- New `tests/test_fcop/test_init_promises.py` pins the deposit
  contract for all three init paths so this can never regress
  silently again.

### Added — fcop (library)

- **`teams/_data/solo/`** — first-class Solo team template bundle
  with the full three-layer documentation (`README.md` /
  `TEAM-ROLES.md` / `TEAM-OPERATING-RULES.md` + `roles/ME.md`), in
  zh and en. The `ME.md` charter contains a "workflow hard
  constraint" section that explicitly forbids the
  "simple-tasks-may-run-directly" soft-constraint pattern (the
  exact 0.6.3 mis-design that let agents bypass `task → do →
  report → archive`).
- **`Project.init` / `init_solo` / `init_custom` ↪ `deploy_role_templates=`**
  parameter (defaults: `True` for preset / solo, `False` for custom
  since custom teams have no bundled templates). Auto-deploys the
  three-layer docs at init time. Solo init no longer raises
  `TeamNotFoundError("solo")` on the role-template step.
- **`Project.init(team="solo")` is now rejected with `ValueError`**
  before any disk write, pointing callers at `init_solo()` so the
  saved config carries `mode="solo"` (not `mode="preset",
  team="solo"`).
- **`fcop.rules.get_install_prompt(lang)`** — returns the canonical
  "have an agent install fcop-mcp for you" prompt (the same text
  shipped to GitHub README / PyPI README / MCP resource
  `fcop://prompt/install`). 0.6.4 surfaces this prompt in three
  places at once so customers can always copy it from whichever
  one they happen to be reading.

### Added — fcop-mcp (MCP server)

- **`fcop://prompt/install`** + **`fcop://prompt/install/en`** —
  two new MCP resources exposing the agent-install prompt
  (zh / en). Total resource count: **10 → 12**.
- **`init_solo` / `init_project` / `create_custom_team`** all
  expose a new **`force: bool`** parameter (default `False`).
  When `True`, an already-initialized project is overwritten and
  the previous `fcop.json` / letter / workspace README / `shared/`
  files / protocol-rule quartet are archived under
  `.fcop/migrations/<timestamp>/`. This is the supported way for
  ADMIN to switch teams (e.g. solo → dev-team) without manually
  wiping the project.
- **`fcop_report` Phase-1 output** now (a) tells the agent
  explicitly that it MUST NOT pick an init mode on ADMIN's behalf,
  and (b) points ADMIN at `fcop://letter/zh|en` for the manual if
  the three-way choice (solo / preset / custom) is unfamiliar.

### Changed — protocol rules

- **`fcop-rules.mdc` 1.5.0 → 1.6.0**:
  - **Rule 0.a.1** new sub-section: workflow hard constraint.
    Every piece of work, no matter how trivial, must follow
    `task → do → report → archive`. Role documents are forbidden
    from softening this with "simple tasks may run directly" or
    equivalents — that pattern is itself a Rule 0.a violation.
  - **Rule 1 Phase 1** rewritten to (a) list the full set of
    files an `init_*` tool promises to deposit (so a partial
    deposit becomes a recognisable bug), and (b) explicitly
    forbid agents from defaulting to `dev-team` / `solo` /
    `custom` on ADMIN's behalf.

### Fixed — letter & install-prompt visibility

- **`init_project` / `init_solo` / `create_custom_team`** now splice
  the LETTER-TO-ADMIN intro slice (title + 0.6.4 summary block +
  ADMIN/AI-team identity diagram) into the post-init reply, with an
  explicit "paste this verbatim to ADMIN" instruction for the agent.
  0.6.3 deposited the letter to disk but never surfaced it in chat,
  so the manual was effectively invisible — customers in the
  tutorial all skipped opening `docs/agents/LETTER-TO-ADMIN.md`.
  The full letter remains available on disk and via the
  `fcop://letter/zh|en` MCP resource; the splice is just the
  intro so it doesn't drown the chat.
- **`fcop.rules.get_letter_intro(lang)`** new public accessor
  (used by the MCP layer above). Returns the verbatim prefix of
  the letter through the second `---` rule. Pinned by 7 new tests
  asserting it stays a strict prefix of `get_letter(lang)` and
  always carries the H1 + the "0.6.4 摘要" / "0.6.4 in one block"
  block.
- **`tests/test_fcop/test_install_prompt.py`** (11 new tests)
  pins the four-surface contract for the canonical install
  prompt: the bundled markdown file, `get_install_prompt(lang)`,
  the `fcop://prompt/install` MCP resource, and the verbatim
  embed inside `mcp/README.md` (PyPI-visible) all stay byte-for-
  byte aligned. Also asserts the non-negotiable safety clauses
  (preserve existing `mcpServers`, 30s–1min first-launch
  cooldown, do-not-auto-init) survive future copy edits in both
  languages.

### Fixed — role-template soft-constraint regression

- **All 17 bundled role charters** (`solo/ME`, `dev-team/PM` /
  `DEV` / `QA` / `OPS`, `media-team/PUBLISHER` / `COLLECTOR` /
  `WRITER` / `EDITOR`, `mvp-team/MARKETER` / `RESEARCHER` /
  `DESIGNER` / `BUILDER`, `qa-team/LEAD-QA` / `TESTER` /
  `AUTO-TESTER` / `PERF-TESTER`, both zh and en — 34 files total)
  now open with a "workflow hard constraint" section that
  translates Rule 0.a.1 onto the role side: every incoming piece
  of work, no matter how trivial, must follow the four-step
  cycle `task → do → report → archive`, with only a narrow
  ADMIN-explicit exception clause that itself requires a
  `drop_suggestion` trace. 0.6.3 charters scattered the
  workflow rules across "Responsibilities" / "Common mistakes"
  prose, which agents in the field softened to "simple tasks may
  run directly" — the exact pattern that let `ME` skip
  `task` / `report` and dump artefacts directly to the project
  root during the snake-game tutorial debug.
- New `tests/test_fcop/test_role_templates.py` (36 tests) pins
  the anchor across every bundled `roles/*.md` so a future
  contributor copy-pasting a role without the constraint will
  fail CI rather than silently regress.

### Documentation

- **`src/fcop/rules/_data/agent-install-prompt.zh.md`** +
  **`.en.md`** — the canonical install prompt, also packaged into
  the wheel and surfaced via the new MCP resource. Same text used
  in `mcp/README.md` and root `README.md` / `README.zh.md`.
- **`mcp/README.md`** opens with a "TL;DR — Have an agent install
  fcop-mcp for you" section visible on GitHub *and* PyPI.
- **Root `README.md` / `README.zh.md`** point at the install
  prompt + the new `fcop://prompt/install` resource so customers
  who land on either landing page can hand the prompt to an agent
  without reading the rest of the page.
- **`docs/agents/LETTER-TO-ADMIN.md`** (zh + en) gets a 0.6.4
  summary block at the top, the corrected tool / resource counts
  (26 / 12), the new `fcop://prompt/install` resource entry, and
  an explicit "agent must not default" warning on the three-way
  init choice.
- **`src/fcop/teams/_data/README.md`** + **`.en.md`** add the new
  `solo` team to the directory listing and the modes table, and
  pick up a "Custom teams" section pointing custom builds at the
  closest preset for inspiration.

## [0.6.3] - 2026-04-26

Lockstep release with two thrusts: (1) ratify **ADR-0006**, the
host-neutral protocol-rule distribution & upgrade contract, so
`fcop-mcp` finally writes the protocol rules to disk in a form every
MCP host can read (Cursor `.mdc`, plus `AGENTS.md` / `CLAUDE.md`); and
(2) rename `unbound_report` → `fcop_report` because the tool is the
canonical project-status report, not just the unbound-session
warning. All changes are additive per ADR-0003 (Pre-1.0 Stability
Charter); every removed-in-0.7.0 alias is shipped through one full
deprecation cycle. See [`docs/releases/0.6.3.md`](./docs/releases/0.6.3.md).

### Added — governance

- **ADR-0006 Host-Neutral Rule Distribution & Upgrade** ratified
  ([`adr/ADR-0006`](./adr/ADR-0006-host-neutral-rule-distribution.md)).
  Codifies that the protocol rule files (`fcop-rules.mdc`,
  `fcop-protocol.mdc`) must reach every supported host (Cursor,
  Claude Desktop, Claude Code CLI, Codex CLI, raw API scripts) and
  that there must be an explicit, ADMIN-controlled upgrade path when
  the wheel-bundled rules drift past the project-local copy.

### Added — fcop (library)

- **`fcop.rules.get_protocol_version()`** — returns the SemVer of the
  shipped commentary (`fcop-protocol.mdc`), symmetric to the existing
  `get_rules_version()`. The two documents version independently so a
  wording-only edit to the commentary doesn't force a rules bump and
  vice versa. Used by `Project.deploy_protocol_rules` and the MCP
  layer's `fcop_report` / `redeploy_rules` to detect drift.
- **`Project.deploy_protocol_rules(force=True, archive=True)`** — host-
  neutral redeploy of the four protocol-rule targets to the project
  root: `.cursor/rules/fcop-rules.mdc` + `.cursor/rules/fcop-protocol.mdc`
  (Cursor), plus YAML-frontmatter-stripped `AGENTS.md` (Codex CLI) and
  `CLAUDE.md` (Claude Code CLI). Stale targets are archived under
  `.fcop/migrations/<ts>/rules/` before being overwritten. Returns a
  `DeploymentReport` listing every file touched.
- **`Project.init(deploy_rules=True)`** — `deploy_rules` now wires
  through `deploy_protocol_rules` so a fresh project ships with the
  four rule targets already on disk. Existing call sites that don't
  pass the flag are unchanged.

### Added — fcop-mcp (MCP server)

- **`fcop_report(lang)`** — new canonical session-status / init report
  tool. Same body shape as the legacy `unbound_report` plus a
  `[Versions]` / `[版本]` block surfacing `fcop-mcp`, `fcop`, and
  the local-vs-bundled rules / protocol versions, with an `OUTDATED`
  / `本地偏旧` marker + `redeploy_rules` prompt when drift is
  detected. Replaces `unbound_report` for all new system prompts.
- **`redeploy_rules(force=True, archive=True, lang)`** — ADMIN-only
  thin wrapper over `Project.deploy_protocol_rules`. Agents must not
  invoke directly (the docstring says so), but the MCP surface stays
  symmetric with `deploy_role_templates` so ADMIN can call it from
  the chat box. The 24-tool count is now **26** with these two
  additions; the snapshot
  (`tests/test_fcop_mcp/snapshots/tool_surface.json`) is updated
  accordingly per ADR-0003 commitment #2.

### Deprecated — fcop-mcp

- **`unbound_report`** is now a thin alias of `fcop_report` and emits
  `DeprecationWarning("unbound_report is deprecated; use fcop_report
  instead. This alias will be removed in fcop-mcp 0.7.0. See ADR-0006
  for the rationale.")` on every call. The tool stays in the public
  surface for one full minor (per ADR-0003 deprecation cycle); 0.7.0
  removes the name. Migration is purely lexical: replace every
  `unbound_report` in your system prompts with `fcop_report`.

### Tests

- **15 new tests** for `fcop`: `tests/test_fcop/test_rules.py` adds
  `TestGetProtocolVersion`; new file
  `tests/test_fcop/test_project_deploy_protocol.py` covers the four
  deployment targets, byte-exactness of `.mdc`, frontmatter stripping
  for `AGENTS.md` / `CLAUDE.md`, idempotency, archival, and the
  `Project.init(deploy_rules=True)` integration path. Public-surface
  snapshot regenerated for the additive `Project.deploy_protocol_rules`
  + `fcop.rules.get_protocol_version` exports.
- **9 new tests** for `fcop-mcp`:
  `tests/test_fcop_mcp/test_server.py::TestSessionReportAndRedeploy`
  covers `fcop_report` (uninitialized / initialized / `[Versions]`
  block / English variant / drift warning), the `unbound_report`
  alias (still works + `DeprecationWarning` is emitted), and
  `redeploy_rules` (writes four targets + archives stale files).
  Tool-surface snapshot regenerated for the additive
  `fcop_report` / `redeploy_rules` registrations.

### CI

- **`.github/workflows/release.yml`**: `verify` 步骤改为只从
  `^__version__ =` 行解析版本；不再用「文件中首段双引号内文字」，避免
  匹配到 `src/fcop/_version.py` 里 **`"semver 承诺"`** 导致 tag 发版
  在 verify 即失败。行为与发版后用户升级无直接关系。

## [0.6.2] - 2026-04-25

### Documentation (PyPI + repo)

- **Project metadata** (`pyproject.toml`): one-line `description` and
  `project.urls` for both packages. **`fcop`**: long description is
  [`fcop-README.pypi.md`](./fcop-README.pypi.md) (pure library; fixes wrong
  historical “MCP toolbox” text on PyPI). **`fcop-mcp`**: `description` / links;
  install story in [`mcp/README.md`](./mcp/README.md).
  No library or server code change; **ADR-0003** tool/resource surface unchanged.
- **`fcop-mcp`**: customer-facing install guide in [`mcp/README.md`](./mcp/README.md) — one **recommended** path (dedicated venv + `python -m fcop_mcp`), **alternatives** (`uvx fcop-mcp` with cold-start note), **Windows / macOS** `mcp.json` examples, **verify** commands (`from fcop import Issue, Project` / `fcop_mcp.server`), and a short warning when the wrong `fcop` distribution is on `PYTHONPATH`.
- **Root `README` / `README.zh`**: pointer to the full install doc for IDE users; behaviour of the two packages is unchanged.
- **Lockstep**: `fcop` **0.6.2** and **`fcop-mcp` 0.6.2** together — **no** public library API or compat-CLI code change in `fcop` vs 0.6.1; version bump aligns both wheels and refreshes long-form docs on PyPI (cannot replace 0.6.1 files in place).

See [`docs/releases/0.6.2.md`](./docs/releases/0.6.2.md).

## [0.6.1] - 2026-04-23

### Added

- **`fcop` compat CLI shim** — the `fcop` wheel now ships a `fcop`
  console script that prints a friendly migration message and exits
  with status `1`. This closes the `0.5.x → 0.6.x` gap where users who
  ran `uvx fcop` or `pip install fcop && fcop` would have gotten a bare
  "command not found" after upgrading. Pure additive per ADR-0003 (no
  library API change). See [`docs/releases/0.6.0.md`](./docs/releases/0.6.0.md)
  §5.3 for background.

## [0.6.0] - 2026-04-23

### Added — project governance

- **ADR-0003 Pre-1.0 Stability Charter** ratified
  ([`adr/ADR-0003`](./adr/ADR-0003-stability-charter.md)). Starting with
  `0.6.0`, the four public-API surfaces (`fcop.__all__`, `Project`
  methods/properties, `fcop.models` dataclass fields,
  `fcop.teams` / `fcop.rules` exports) are **additive-only** within a
  minor version; breaking changes require a deprecation cycle spanning
  at least one minor version.
- New snapshot test
  `tests/test_fcop/test_public_surface.py` freezes the observed surface
  to `tests/test_fcop/snapshots/public_surface.json`. Update the
  snapshot with `pytest --snapshot-update` when adding public API and
  announce it in this CHANGELOG.
- New CI job `surface-check` verifies that any PR modifying the snapshot
  file also updates the `[Unreleased]` section of this CHANGELOG.
- **`fcop-mcp` tool contract frozen** (ADR-0003 commitment #2). New
  snapshot test `tests/test_fcop_mcp/test_tool_surface.py` captures
  every tool name, parameter name + JSON type + required-ness, and
  every `fcop://` resource URI into
  `tests/test_fcop_mcp/snapshots/tool_surface.json`. Regenerate with
  `pytest tests/test_fcop_mcp --snapshot-update` when adding public
  MCP surface (always additive within 0.6.x).
- New smoke suite `tests/test_fcop_mcp/test_server.py` (39 tests)
  exercises every registered tool and resource end-to-end via
  `mcp.call_tool` / `mcp.read_resource`, so a broken MCP handler
  fails CI instead of surfacing only in a user's editor.
- New GitHub Actions workflow `test-fcop-mcp.yml` — 3-OS × 4-Python
  matrix, ruff + mypy (strict) + pytest for the MCP contract and
  smoke suite, a PR-only `tool-surface` gate mirroring the library's
  `surface-check` job, and a clean-venv smoke install of the built
  wheel so the `fcop-mcp` console script packaging is verified
  every commit.
- **ADR-0004 Time Is Filesystem's Job** ratified
  ([`adr/ADR-0004`](./adr/ADR-0004-time-is-filesystem.md)). Single
  source of truth for time: task / report files **do not** carry
  `created_at` in frontmatter (Git history + filesystem `mtime` are
  authoritative). Issue files **do** carry `created_at` because
  Issue is the one FCoP file kind that allows legal editing
  (`open → closed` monotonic append), so `mtime` is no longer
  equivalent to creation time.
- **ADR-0005 Agent Output Layering** ratified
  ([`adr/ADR-0005`](./adr/ADR-0005-agent-output-layering.md)).
  Every agent-produced artifact now falls into exactly one of five
  lifecycle tiers: (A) tool return values — no file, (B) audit /
  patrol traces → `docs/agents/log/`, (C) cross-agent findings →
  `docs/agents/issues/` via `write_issue`, (D) agent-private runtime
  state (`runtime-*.json`, cache, checkpoint) → **new**
  `docs/agents/.runtime/{AGENT_CODE}/`, (E) local one-shot human
  scripts → `_ignore/`. 0.6.0 is a protocol-level decision only; the
  library helpers (`Project.agent_runtime_dir`, `write_log`,
  `list_logs`) ship in 0.6.1 as additive API per ADR-0003.

### Changed — fcop (library)

- **BREAKING**: `fcop` is now a pure Python library, not an MCP server.
  Users who were running `uvx fcop` or `pip install fcop` expecting an
  MCP server should install `fcop-mcp` instead.
- New `Project` facade as the main entry point; see
  [adr/ADR-0001](./adr/ADR-0001-library-api.md) for the full API contract.
- Structured data returns: methods now return frozen dataclasses
  (`Task`, `Report`, `Issue`, `TeamConfig`, `ProjectStatus`, ...) instead
  of pre-formatted strings.
- Typed exception hierarchy: every failure mode has a dedicated subclass
  of `FcopError`.
- Runtime dependency reduced to just `pyyaml` (YAML is part of the
  FCoP file format). MCP and websocket deps moved entirely to `fcop-mcp`.
- Single source of truth for the version string at `src/fcop/_version.py`
  (read by `pyproject.toml` via hatchling's dynamic version).
- **Preset rosters realigned** with the authoritative `_data/teams/index.json`
  (ported from `codeflow-plugin 0.5.x`):
  - `mvp-team`: now `MARKETER` (leader) / `RESEARCHER` / `DESIGNER` /
    `BUILDER`. Was `PM` / `BUILDER` / `SELLER` in a pre-0.6 snapshot of
    `fcop.teams`.
  - `media-team`: adds `EDITOR` as the fourth role.
  - `dev-team` and `qa-team` unchanged.
  `Project.init(team=...)` will generate the new rosters from 0.6.0
  onward.
- `fcop.rules` now returns real content (the protocol rule docs and
  the Letter-to-ADMIN user manual). Previously raised
  `NotImplementedError`. `get_rules_version()` parses the bundled
  rules document's frontmatter — today `"1.4.0"`.
- `fcop.teams.get_template()` implemented. Returns a `TeamTemplate`
  dataclass with `readme` + `team_roles` + `operating_rules` + a
  per-role `roles` dict, all as UTF-8 text. Previously raised
  `NotImplementedError`.
- `Project.write_issue` now emits two additional canonical
  frontmatter fields: `status: open` and `created_at` (ISO 8601,
  second precision). Existing issue files missing these fields are
  still readable — the new fields are additive, see ADR-0004
  Grandfather clause.
- Issue file canonical frontmatter order is now
  `protocol, version, reporter, severity, status, summary,
  created_at [, closed_at, closed_by, resolution]` with unknown
  keys sorted alphabetically below; `closed_*` / `resolution` slots
  are reserved for the 0.6.1 issue state-machine follow-up.

### Added — fcop-mcp (MCP server)

- New package. Thin wrapper exposing `fcop.Project` / `fcop.teams` /
  `fcop.rules` as MCP tools and resources for Cursor / Claude Desktop.
- Depends on `fcop >= 0.6, < 0.7` and `fastmcp >= 3.2`.
- **24 MCP tools** registered, mirroring the 0.5.4 surface so existing
  clients keep working after the rename (`fcop` → `fcop-mcp`). Groups:
  project path (`set_project_dir`), init (`init_project`, `init_solo`,
  `create_custom_team`, `validate_team_config`),
  tasks (`write_task` / `read_task` / `list_tasks` / `inspect_task` /
  `archive_task`), reports (`write_report` / `list_reports` /
  `read_report`), issues (`write_issue` / `list_issues`),
  team & workspace (`get_available_teams`, `get_team_status`,
  `deploy_role_templates`, `new_workspace`, `list_workspaces`),
  suggestions (`drop_suggestion`), and meta (`unbound_report`,
  `check_update`, `upgrade_fcop`).
- **10 MCP resources** under the `fcop://` URI scheme: `status`,
  `config`, `rules`, `protocol`, `letter/{zh,en}`, `teams`,
  `teams/{team}`, `teams/{team}/{role}`, `teams/{team}/{role}/en`.
  All returns route through the `fcop` library, so the contract
  remains single-sourced.

### Removed — fcop (library)

- `fcop.server` module (moved to `fcop-mcp`).
- `fcop` console script (the CLI returns in a later release as a
  separate ADR).
- Global module state (`PROJECT_DIR`, `TASKS_DIR`, ...); all state now
  flows through `Project` instances.

### Migration

If you were using `fcop 0.5.x`:

- MCP server users → `pip install fcop-mcp` and update your MCP client
  config to call `fcop-mcp` instead of `fcop`.
- Python library users → upgrade to `fcop 0.6.0` and switch from
  `from fcop.server import ...` (unofficial) to the new public API
  `from fcop import Project`.

See [`docs/MIGRATION-0.6.md`](./docs/MIGRATION-0.6.md) for the step-by-step
guide (coming before the 0.6.0 final release).

---

## Pre-history (before joinwell52-AI/FCoP existed)

Prior to 0.6.0, the package was developed inside the
[`joinwell52-AI/codeflow-pwa`](https://github.com/joinwell52-AI/codeflow-pwa)
monorepo under the `codeflow-plugin/` subdirectory. That history is
preserved in place and is not ported into this repository.

The last `fcop 0.5.x` release
([`fcop 0.5.4`](https://pypi.org/project/fcop/0.5.4/)) was built from
commit
[`e651139`](https://github.com/joinwell52-AI/codeflow-pwa/commit/e651139).
Anything older should be read from that repository's `git log`.
