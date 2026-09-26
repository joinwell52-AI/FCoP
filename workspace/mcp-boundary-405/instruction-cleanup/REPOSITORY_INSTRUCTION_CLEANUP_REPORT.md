# REPOSITORY_INSTRUCTION_CLEANUP_REPORT

Scope: WP-1 / Repository Instruction Cleanup, added by the user's explicit correction on 2026-09-26.
The earlier WP1-WP11 work was paused and preserved. This document is a development audit, not an FCoP role-governance envelope.

## Gate

**PASS — REPOSITORY_INSTRUCTION_CLEANUP.** See [verification.json](verification.json): 122 tests passed (3 cleanup tests and 119 existing v4 conformance tests); relevant lint passed. Two existing jsonschema deprecation warnings remain.
This gate does not claim that the unfinished 4.0.5 refactor or release candidate is complete.

## Root instruction audit

- Before: **3732 lines**, 163 Markdown headings (including headings inside examples).
- Before SHA256: `ea9bfdbbb8642d0621e536e083a9ff19d45aff816906fbf205cc652cc085e902`.
- Exact inert backup: [AGENTS.before.txt](AGENTS.before.txt).
- Complete heading inventory with original line numbers: [audit.json](audit.json).
- After: **12 lines**, one repository-development heading.

The old file was a deployed combination of protocol rules and commentary, not a focused source-repository guide.
Categories overlap because a single rule could combine protocol, team and runtime responsibilities.

| Classification requested | Representative original lines | Finding and disposition |
|---|---|---|
| Source-repository development guidance | 1-20, 1877-1904 | Package source attribution and MCP docstring editing notes; no coherent build/test guide. Replaced with actual source, test and local build entrypoints. |
| Team / Solo / ME / role governance | 33-50, 241-399, 640-706, 1814-1904, 2024-2309, 2478-2681 | Role workflow, two-role/solo review, task/report loop, routing and team configuration. Removed from active repository instructions. |
| Session / seat / succession | 433-595, 1932-2013 | UNBOUND startup, fcop_report prerequisite, role assignment and session occupancy. Removed without replacement or developer onboarding gate. |
| v3 deployment rules | 859-915, 2310-2368, 3628-3710 | v3 layout, host projection, redeploy and version-warning rules. Removed from repository instructions; historical implementation is explicit compatibility. |
| Host / Runtime / CodeFlowMu-type governance | 960-1151, 3189-3241, 3309-3590 | Capability roles, session recovery, events, patrol and GAL. Not Base development policy. No CodeFlowMu files modified. |
| Still useful v4 development constraints | 400-432, 757-809, 1453-1539 | Truthful evidence, careful changes and separation of protocol authority from tools. Restated concisely as repository engineering guidance; no old protocol text retained. |

## Whole-repository search

Search uses `rg --hidden --no-ignore` over the repository, including ignored historical files.
Excludes `.git`, Python caches, installed dependency trees, node_modules and this evidence directory; binary files use ripgrep's default exclusion.
Results are **matching lines / distinct files**, not claims of active dependencies. Files and line numbers are recorded, without copying source text or secret values.
These counts describe the post-cleanup source tree; original root headings and bytes were captured before cleanup.

| Pattern | Matching lines | Files | Full path/line/category evidence |
|---|---:|---:|---|
| `AGENTS.md` | 711 | 215 | [AGENTS-md.json](AGENTS-md.json) |
| `CLAUDE.md` | 656 | 200 | [CLAUDE-md.json](CLAUDE-md.json) |
| `.cursor` | 1301 | 320 | [cursor.json](cursor.json) |
| `fcop_report` | 1946 | 216 | [fcop-report.json](fcop-report.json) |
| `solo` | 3277 | 263 | [solo.json](solo.json) |
| `ME` | 3348 | 486 | [ME.json](ME.json) |
| `seat/session/assignment` | 10493 | 404 | [seat-session-assignment.json](seat-session-assignment.json) |
| `redeploy_rules` | 715 | 185 | [redeploy-rules.json](redeploy-rules.json) |
| `deploy_role_templates` | 532 | 134 | [deploy-role-templates.json](deploy-role-templates.json) |
| `create_custom_team` | 745 | 133 | [create-custom-team.json](create-custom-team.json) |

Exact-name AGENTS file inventory: [instruction-file-inventory.json](instruction-file-inventory.json).
Historical `.fcop/migrations/.../rules/AGENTS.md` snapshots remain inactive archival material; they are not ancestors of source directories.

## Four separate ownership surfaces

1. **Repository / Codex instructions:** root `AGENTS.md` is only a development guide. Root `CLAUDE.md` points to it. The two generated `.cursor/rules/fcop-*.mdc` files are removed from active discovery; their bytes are retained here as `.before.txt` audit copies.
2. **Product workspace facts:** canonical `fcop/fcop.json`, lifecycle directories and four envelope types are created by existing v4 Core. No host instruction file is a protocol input or initialization output. Explicit profile references remain data, never an injected instruction document.
3. **Legacy compatibility:** the complete old Project implementation is retained at `src/fcop/compatibility/v3/project.py`; the old server is at `mcp/src/fcop_mcp/compatibility/v3/server.py`. Historical workspace callers must select compatibility explicitly. Old published symbols other than Project are lazy compatibility access, not Base import dependencies.
4. **Host / Runtime / session governance:** the old GAL and governance modules remain historical code, outside canonical registration and imports. MCP transport sessions are SDK mechanics; they do not assign FCoP roles or seats.

## Before / after changes

| Surface | Before | After |
|---|---|---|
| AGENTS.md | 3,732 lines of old protocol/workflow rules | 12 lines of development guidance |
| CLAUDE.md | Full deployed protocol copy | Three-line pointer to repository guidance |
| Cursor protocol rules | Auto-discovered old rules and commentary | Removed from active location; inert audit backups |
| Default `fcop.Project` | Imports legacy Team/session machinery and exposes old deployment behavior | Canonical facade delegates to existing v4 Core; historical workspaces rejected with explicit compatibility guidance |
| Base imports | Eager legacy model/config/recovery/Project dependencies | Core Project and errors only; legacy symbols loaded only on explicit access |
| `_Creation` legacy classification | Eager Team parser import | Lazy import only on historical classification; Base rejects historical declarations before this route |
| v4 legacy rule redeploy helper | Imported helper from default Project module | Imports explicitly from compatibility only |
| New workspace | Existing canonical initialization already excluded host projections | Preserved and covered by import and file-access guards |

## Review of changes made before the pause

- **Preserved:** 49-tool baseline, 25-tool manifest/adapters, canonical registry/server entrypoint, workspace observation/validation, explicit Profile/Toolkit/CLI work, package version edits and historical MCP relocation. These implement the requested boundaries, not the old role workflow. They remain work in progress pending WP1-WP11 verification.
- **Reworked:** default Project/package imports were still carrying old role/config/recovery dependencies. The old implementation was relocated intact, and a canonical facade now delegates to the same existing v4 implementation without copying its algorithms.
- **Removed:** this execution's `fcop/tasks/TASK-20260926-001-ADMIN-to-ME.md` and `fcop/reviews/REVIEW-20260926-001-ME-on-task-20260926-001-admin-to-me.md`. They existed only to satisfy obsolete repository instructions. Deletion provenance and hashes are in [removed-current-run-governance.json](removed-current-run-governance.json).
- No implementation of new seat binding, role takeover or session governance was added. No prior user ledger, pre-existing shared team files or unrelated modifications were reverted.

## Remaining Legacy references and migration implications

- `src/fcop/compatibility/v3/project.py`: old initialization, role templates, host rule projection, audits, occupancy and recovery. Explicit historical import only.
- `mcp/src/fcop_mcp/compatibility/v3/server.py`: old 49-tool implementation. Not the default server.
- `src/fcop/core/config.py`, `core/recovery.py`, `models.py`: historical helpers/types still shipped for compatibility, but not imported by the tested Base path.
- `src/fcop/rules/_data/`, `src/fcop/teams/_data/`: old packaged rules/templates remain historical data. Canonical initialization does not read or deploy them. Explicit Profile discovery is outside Base.
- `mcp/src/fcop_mcp/adapter.py`, `disposition.py`, `resources.py`, `gal/`, `governance/`: existing historical routing/metadata/runtime helpers remain to be fully grouped by the original WP9 work. The default registry does not register or execute them.
- `fcop/`, `.fcop/migrations/`, archived specs, docs and fixtures retain historical references; a keyword hit alone is not an active workflow dependency.
- Existing legacy callers/tests using `from fcop import Project` for v3 must migrate to the explicit compatibility import. The full mixed-version test suite and public API migration documentation remain part of paused WP1-WP11; no full-suite success is claimed here.

## Default-path conclusion

The guarded Base Core + canonical MCP flow does not require Team, Solo, ME, role assignment, seats, succession or runtime session governance.
Its test denies imports of `fcop.teams`, `fcop.profiles`, `fcop.compatibility`, `fcop.core.config`, `fcop.core.recovery`, MCP compatibility, GAL and governance while performing real protocol operations.
It also denies reads/writes of `AGENTS.md`, `CLAUDE.md` and `.cursor` files, verifies pure and explicitly referenced-profile initialization, and checks inspect/validate preserve all existing bytes.

No PyPI upload, tag, Release, merge, deployment or CodeFlowMu modification was performed. WP1-WP11 may resume only after this gate passes.
