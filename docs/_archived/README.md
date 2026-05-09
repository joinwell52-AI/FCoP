# Archived docs

These files are kept for **history only**; they are not the current entry point and may not reflect current FCoP semantics.

## Contents

| File | Original location | Superseded by | Reason |
|---|---|---|---|
| `fcop-primer.md` / `.en.md` | `primer/fcop-primer.md` | [`docs/getting-started.md`](../getting-started.md) | v1.0 reframing: single L0+L1 entry point under "AI OS protocol layer" framing |
| `fcop-standalone.md` / `.en.md` | `docs/fcop-standalone.md` | [`docs/getting-started.md`](../getting-started.md) | Same — content merged into getting-started, plus `fcop/` workspace path migration ([ADR-0022](../../adr/ADR-0022-workspace-directory-convention.md)) |

## Why archived rather than deleted

- These were the entry-point docs for FCoP `0.x` and earlier `1.0` drafts.
- External links (essays, blog posts, GitHub issues) may still point at them.
- Deleting would break those links; archiving lets the URL keep resolving with a clear "look at the new entry" signal.

## What to read instead

- **L0+L1**: [`docs/getting-started.md`](../getting-started.md)
- **L2 protocol charter**: [`adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md`](../../adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md)
- **Workspace migration (`docs/agents/` → `fcop/`)**: [`adr/ADR-0022`](../../adr/ADR-0022-workspace-directory-convention.md)
