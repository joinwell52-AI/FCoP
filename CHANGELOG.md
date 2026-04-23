# Changelog

All notable changes to the `fcop` and `fcop-mcp` Python packages are recorded
here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and the project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This file tracks both packages together because they release in lockstep.
See [adr/ADR-0002](./adr/ADR-0002-package-split-and-migration.md) for the
versioning strategy.

## [Unreleased]

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
- Zero third-party runtime dependencies. MCP and websocket deps moved
  entirely to `fcop-mcp`.
- Single source of truth for the version string at `src/fcop/_version.py`
  (read by `pyproject.toml` via hatchling's dynamic version).

### Added — fcop-mcp (MCP server)

- New package. Thin wrapper exposing `fcop.Project` / `fcop.teams` /
  `fcop.rules` as MCP tools and resources for Cursor / Claude Desktop.
- Depends on `fcop >= 0.6, < 0.7` and `fastmcp >= 3.2`.

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
