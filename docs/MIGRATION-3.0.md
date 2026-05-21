# Migrating from FCoP 2.x to FCoP 3.0

> **TL;DR**: FCoP 3.0 introduces a new directory topology (`_lifecycle/`) as the canonical state truth. Run `python -m fcop migrate --to-v3` to perform a one-shot, git-aware migration.

---

## Why FCoP 3.0 is a breaking change

FCoP 1.x / 2.x treated directories as **type classification** (`tasks/`, `reports/`, `issues/`, `log/`). A task's current lifecycle state lived inside the file (in YAML frontmatter), not in the filesystem.

FCoP 3.0 elevates the directory itself to **state truth**:

```
fcop/
├── _lifecycle/        ← NEW: state lives here
│   ├── inbox/         ← created
│   ├── active/        ← claimed
│   ├── review/        ← pending confirmation
│   ├── done/          ← completed
│   └── archive/       ← closed (replaces fcop/log/tasks/)
├── reports/           ← unchanged (no longer archived)
├── issues/            ← unchanged (resolved field carries state)
└── shared/            ← unchanged
```

The canonical statement:

> **Files carry protocol. Paths address state. Events replay transitions.**
> *(Canonical one-liner per [ADR-0040](../adr/ADR-0040-canonical-one-liner-two-layer-convention.md); the v1 line "file location is truth; everything else is trace" is retained as historical epigraph in essays/reviews filed on or before 2026-05-21.)*

This change unlocks:

- **No-content state inspection**: `ls fcop/_lifecycle/active/` tells you everything in flight, without reading any file
- **Atomic claim semantics**: `claim_task` becomes a single `os.rename()`, eliminating the duplicate-dispatch class of bugs that plagued multi-agent setups
- **Audit-grade history**: every `mv` writes a `transitions:` event inside the file, providing a tamper-evident PAST trace

Full spec: [`spec/fcop-3.0-spec.md`](../spec/fcop-3.0-spec.md) · [`spec/fcop-3.0-rfc.md`](../spec/fcop-3.0-rfc.md)

---

## What you have to migrate

| 2.x location | 3.0 location | Notes |
|---|---|---|
| `fcop/tasks/*.md` | `fcop/_lifecycle/inbox/*.md` | All open tasks land in `inbox/` first |
| `fcop/log/tasks/*.md` | `fcop/_lifecycle/archive/*.md` | Closed tasks go straight to `archive/` |
| `fcop/log/reports/*.md` | `fcop/reports/*.md` | Reports are append-only; no archive concept |
| `fcop/log/issues/*.md` | `fcop/issues/*.md` | Resolved issues get `resolved: true` in frontmatter |
| `fcop/log/` (empty) | (removed) | Top-level `log/` no longer exists |
| `fcop/shared/*` | `fcop/shared/*` | Unchanged |

---

## One-shot migration

After upgrading packages (lockstep required, per ADR-0002):

```bash
pip install -U "fcop>=3.0,<4.0" "fcop-mcp>=3.0,<4.0"
```

Run the migrator from your project root:

```bash
python -m fcop migrate --to-v3
```

This will:

1. Create the 5 `_lifecycle/` subdirectories
2. Move every 2.x file to its 3.0 location per the table above
3. Append a **synthetic transition event** to every migrated file:
   ```yaml
   transitions:
     - at: <file-mtime>
       from: null
       to: <current-stage>
       by: migration
       tool: fcop_migrate_v3
   ```
4. Remove the empty `log/` directory
5. Print a per-file summary

The migration is **git-aware**: it uses `git mv` when the project is a git repo, so history is preserved.

---

## Verifying the migration

After migration, run:

```bash
python -m fcop status
```

You should see something like:

```
FCoP 3.0 project at <root>
  _lifecycle/inbox/    : 3 tasks
  _lifecycle/active/   : 2 tasks
  _lifecycle/review/   : 0 tasks
  _lifecycle/done/     : 12 tasks
  _lifecycle/archive/  : 47 tasks
  reports/             : 89 files
  issues/              : 14 files (3 unresolved)
```

Or use `fcop_audit()` (via the MCP server) to run a deep consistency check.

---

## What about files lacking `transitions:`?

Files that existed before migration and were not touched (rare edge cases) are treated as **legal historical artifacts**. They remain readable. But any new transition on them MUST start appending events.

The migrator adds a synthetic baseline event so most files won't need this fallback.

---

## What if I have custom tools that wrote to `tasks/` directly?

Those tools were already breaking ADR-0035 Rule B (only L1 tools may move files between lifecycle directories). After migration:

- Update them to call L1 tools (`create_task`, `claim_task`, etc.) instead of writing files directly
- If they were L3/L4/L5 tools that only **read** files, they continue to work — just update the read paths from `tasks/` to `_lifecycle/<stage>/`

The L1 / L2 / L3 / L4 / L5 classification is described in [`spec/fcop-3.0-spec.md`](../spec/fcop-3.0-spec.md) §8.

---

## What about `risk_level`, `assignee`, custody fields?

These are **excluded** from FCoP 3.0 (see spec §3.2). If your 2.x files used them:

- `risk_level` may remain in frontmatter as a coordination hint, but it **MUST NOT** drive state transitions (use `finish_task(skip_review=true)` for direct paths)
- `assignee` / `owner` / `custodian` may exist as informational metadata, but **MUST NOT** be treated as protocol state (see `adr/NOTE-custody-is-not-a-layer.md`)

`fcop_audit()` will flag any code path that uses these fields to drive transitions.

---

## Rollback

The migrator does **not** write a reverse script. If you need to roll back:

1. `git checkout` to a commit before migration (if using git)
2. Or restore from backup

We deliberately do not provide a `fcop migrate --back-to-v2` because:

- Once `transitions:` events are appended, removing them violates Rule F (append-only)
- 2.x and 3.0 are conceptually different protocols (state-in-frontmatter vs state-in-path)
- The migration is fast (seconds for typical projects); re-running it after a 2.x downgrade is cheaper than maintaining a reverse path

---

## Cross-runtime / distributed setups

FCoP 3.0 assumes a **single-consistent filesystem boundary** per `_lifecycle/` root (spec §1.1.1). If your `fcop/` lives on:

- A distributed filesystem without strict POSIX semantics
- NFS with caching
- A shared git worktree synced across machines
- An S3-fuse mount

You MUST provide an external consistency layer (lock manager, single-writer gateway). FCoP itself does not handle distributed coordination.

---

## Common pitfalls

| Pitfall | Fix |
|---------|-----|
| Forgot lockstep upgrade (`fcop-mcp` still on 2.x while `fcop` on 3.0) | `pip install -U "fcop>=3.0,<4.0" "fcop-mcp>=3.0,<4.0"` |
| MCP server in Cursor still cached old tool list | Restart Cursor; `uvx` will fetch the new `fcop-mcp` |
| `_lifecycle/` not picked up by `.gitignore` | Add to git tracking explicitly; it is part of your project state |
| Custom audit tool reads `current_state` from frontmatter | Update to read from path (per Rule A); frontmatter status is no longer authoritative |
| `os.rename()` failing because `_lifecycle/` subdirs on different mounts | Move them to the same mount (spec §1.1 hard requirement) |

---

## Reading list

- [`spec/fcop-3.0-spec.md`](../spec/fcop-3.0-spec.md) — canonical single-page formal spec
- [`spec/fcop-3.0-rfc.md`](../spec/fcop-3.0-rfc.md) — IETF-style RFC projection
- [`adr/ADR-0035-lifecycle-directory-and-tool-layers.md`](../adr/ADR-0035-lifecycle-directory-and-tool-layers.md) — State Ontology decision record
- [`adr/ADR-0036-lifecycle-event-layer.md`](../adr/ADR-0036-lifecycle-event-layer.md) — Event Layer decision record
- [`adr/ADR-0038-fcop-boundary-charter.md`](../adr/ADR-0038-fcop-boundary-charter.md) — Boundary Charter
- [`adr/NOTE-custody-is-not-a-layer.md`](../adr/NOTE-custody-is-not-a-layer.md) — why custody is not a protocol field
- [`essays/the-day-we-almost-added-custody.en.md`](../essays/the-day-we-almost-added-custody.en.md) — field report on the decision

---

## Getting help

- File an issue: https://github.com/joinwell52-AI/FCoP/issues
- Read CHANGELOG: [`CHANGELOG.md`](../CHANGELOG.md) — [3.0.0] entry
- Chinese version of this guide: [`docs/MIGRATION-3.0.zh.md`](./MIGRATION-3.0.zh.md)

---

*FCoP 3.0 migration guide · 2026-05-21*
