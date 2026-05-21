# `spec/archived/` — Historical FCoP Spec Drafts

> **🔒 These documents are SUPERSEDED.** They are retained verbatim for archaeology, citation continuity, and to honour the discovery-not-invention principle. **Do not** treat any normative statement (`MUST` / `SHOULD` / schema / contract) here as binding.
>
> **🔒 这些文档已被取代。** 保留逐字原文仅用于考古、引用连续性、以及尊重"发现而非发明"的原则。**不要**将此处的任何规范性陈述（`MUST` / `SHOULD` / schema / 契约）视为约束。

## Canonical source of truth / 单一真相源

- **Spec (canonical)**: [`../fcop-3.0-spec.md`](../fcop-3.0-spec.md) · [中文](../fcop-3.0-spec.zh.md)
- **RFC projection**: [`../fcop-3.0-rfc.md`](../fcop-3.0-rfc.md) · [中文](../fcop-3.0-rfc.zh.md)
- **Governance ADRs**: see [`../../adr/README.md`](../../adr/README.md)

## Contents / 目录内容

| File | Era | Role | Superseded by |
|---|---|---|---|
| `fcop-spec-v1.0.3.md` | 0.7.x | Legacy 0.7.x spec (pre-1.0 schema baseline) | FCoP 3.0 spec |
| `fcop-spec.md` | 1.0 | Spec index / entry point | `../README.md` of 3.0 era + ADR index |
| `fcop-runtime-protocol-v1.0.md` · `.zh.md` | 1.0 | First "runtime protocol" framing | FCoP 3.0 spec §1–§4 |
| `fcop-runtime-protocol-v1.1.md` · `.zh.md` | 1.1 | v1.1 Capability Governance additions | FCoP 3.0 spec §4 (Lifecycle) + ADR-0030-bis |

## Why these are kept / 为何保留

1. **Citation continuity** — external essays, downstream consumers, and academic references may link to these paths. Breaking the URLs would be a hostile act toward the historical record.
2. **Discovery audit** — FCoP 3.0 explicitly evolved *from* these documents through observed runtime pressure (see [ADR-0039](../../adr/ADR-0039-fcop-freeze-discipline-and-runtime-absorption-era.md)). Keeping the predecessors visible makes the evolution falsifiable.
3. **Comparative reading** — anyone wanting to understand *what changed and why* can diff these against the 3.0 spec.

## Why these are no longer canonical / 为何不再权威

FCoP 3.0 (2026-05-21) introduced a unified **State / Event** ontology that subsumed and reorganised everything in v1.0/v1.1:

- The v1.0 "7 abstractions" (Agent / IPC / Encoding / Event / Failure / Boundary / Audit) are now redistributed across spec §4 (Lifecycle = State), §5 (Event Layer), and §8 (Tool Tiers).
- The v1.1 governance fields (`risk_level` / `needs_human` / `human_approval` / `Skill.tools[*].risk`) are retained as `additionalFields` but the **state model** is now lifecycle-directory-based, not flag-based.
- A "Freeze Discipline" ([ADR-0039](../../adr/ADR-0039-fcop-freeze-discipline-and-runtime-absorption-era.md)) governs all post-3.0 evolution: changes must originate from real runtime pressure, not theoretical completeness.

If you arrived here from a link, please update your reference to [`../fcop-3.0-spec.md`](../fcop-3.0-spec.md).
