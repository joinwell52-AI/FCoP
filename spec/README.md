# `spec/` — FCoP Normative Specifications

> **TL;DR**: Read **[`fcop-v3-spec.md`](./fcop-v3-spec.md)** (EN) or **[`fcop-v3-spec.zh.md`](./fcop-v3-spec.zh.md)** (ZH).  
> Everything else is frozen baseline, RFC projection, or historical.

## Canonical (FCoP v3.2.x — current)

| File | Role |
|---|---|
| **[`fcop-v3-spec.md`](./fcop-v3-spec.md)** · [中文](./fcop-v3-spec.zh.md) | ★ **Current single-page spec** — `_lifecycle/` (3.0) + lifecycle MCP (3.1) + `history/` (3.2.0) + **governance `reviews/` / `needs_human`** (§5); aligned with **fcop@3.2.4** |
| [`fcop-3.0-spec.md`](./fcop-3.0-spec.md) · [中文](./fcop-3.0-spec.zh.md) | **Frozen 3.0.0 baseline** (2026-05-21). Retained for “FCoP 3.0.0 only” claims — **superseded** for day-to-day reading |
| [`fcop-3.0-rfc.md`](./fcop-3.0-rfc.md) · [中文](./fcop-3.0-rfc.zh.md) | IETF-style RFC projection of the **3.0.0** content |
| [`schemas/`](./schemas/) | Machine-readable JSON Schemas |

## Auxiliary

| File | Role |
|---|---|
| `codeflow-core.mdc` | Cursor Rules companion for downstream `codeflow` runtime; not part of FCoP itself |
| [`../docs/mcp-tools.md`](../docs/mcp-tools.md) | **45** MCP tools index (navigation; docstrings in `mcp/src/fcop_mcp/server.py` are authoritative) |

## Historical (superseded — do not treat as current)

See [`archived/README.md`](./archived/README.md) for the v1.0 / v1.1 / 0.7.x lineage.

## Governance & evolution

- [`../adr/README.md`](../adr/README.md) — ADR index
- [`../adr/ADR-0039-fcop-freeze-discipline-and-runtime-absorption-era.md`](../adr/ADR-0039-fcop-freeze-discipline-and-runtime-absorption-era.md) — post-3.0 change discipline
- [`../adr/ADR-0040-canonical-one-liner-two-layer-convention.md`](../adr/ADR-0040-canonical-one-liner-two-layer-convention.md) — canonical one-liners

## Version note

| What | Version |
|------|---------|
| This spec document | **v3.2.4** (implementation alignment) |
| `fcop_rules_version` / `fcop_protocol_version` in rules files | **3.2.3** |
| PyPI `fcop` / `fcop-mcp` | **3.2.4** (encoding fix; no new protocol semantics vs 3.2.3) |
