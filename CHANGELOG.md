# Changelog

All notable changes to the `fcop` and `fcop-mcp` Python packages are recorded
here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and the project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This file tracks both packages together because they release in lockstep.
See [adr/ADR-0002](./adr/ADR-0002-package-split-and-migration.md) for the
versioning strategy.

## [Unreleased]

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
