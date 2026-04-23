# Changelog

All notable changes to the `fcop` and `fcop-mcp` Python packages are recorded
here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and the project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This file tracks both packages together because they release in lockstep.
See [adr/ADR-0002](./adr/ADR-0002-package-split-and-migration.md) for the
versioning strategy.

## [Unreleased]

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
