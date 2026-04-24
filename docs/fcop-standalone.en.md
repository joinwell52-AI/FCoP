# What FCoP is (standalone description)

**FCoP** — **F**ile-based **Co**ordination **P**rotocol — is an **open, product-agnostic** agreement: multiple AI agents (and humans) coordinate **only through files** in a shared working tree, without a message bus, an application database, a dedicated message broker, or a long-running coordinator.

This page documents **FCoP itself** (what it is, where the spec lives, what the tree looks like, how to adopt it). It is **not** a product manual, a genealogy essay, or field-report storytelling; for those, see `essays/` in this repository.

---

## The core idea (four points)

1. **Directories are state** — tasks, reports, issues, archives in separate buckets; moving a file is a state transition.  
2. **Filenames are routing** — e.g. `TASK-…-PM-to-DEV.md` encodes sender, recipient, type, and sequence.  
3. **Body is payload** — Markdown plus constrained YAML frontmatter; humans and agents read the same files.  
4. **The filesystem is the sync layer** — atomic `rename` on one mount; no distributed locks or consensus in the baseline story.

In one line: **the entire collaboration surface is on-disk, serialisable, and diffable.**

---

## Where the spec lives (normative)

| Role | Path | Note |
|------|------|------|
| **Charter (rules)** | [`src/fcop/rules/_data/fcop-rules.mdc`](../src/fcop/rules/_data/fcop-rules.mdc) | rule-level must-follow text |
| **Commentary (protocol)** | [`src/fcop/rules/_data/fcop-protocol.mdc`](../src/fcop/rules/_data/fcop-protocol.mdc) | how each rule applies in practice |
| **Human long spec** | [`spec/fcop-spec-v1.0.3.md`](../spec/fcop-spec-v1.0.3.md) | Chinese, versioned, non single-file “drop-in” |
| **Stable entry** | [`spec/fcop-spec.md`](../spec/fcop-spec.md) | navigation to the current release |

In Cursor, place **`fcop-rules.mdc` and `fcop-protocol.mdc` as a pair** under `.cursor/rules/`. If they disagree, **`fcop-rules.mdc` wins** (as `fcop-protocol` states).

> The path `spec/codeflow-core.mdc` in this repo is a **deprecation stub** for old URLs; it is **not** the 0.6+ normative body.

---

## Workspace shape

- **Root**: the project root you choose.  
- **Coordination root**: `docs/agents/` with `tasks/`, `reports/`, `issues/`, `shared/`, `log/`, … (created by `init` or by hand).  
- **Identity**: `docs/agents/fcop.json` is the **sole authority** for roles/leader; agents do not “pick a role in chat” over that file.

Finer details (naming, patrol, multi-team) are in **`fcop-rules` + `fcop-protocol`**.

---

## How to adopt (choose one or combine)

1. **Python** — `pip install fcop`, `Project(".").init()` (etc.) to create the tree and `fcop.json`.  
2. **Rules only** — copy `fcop-rules.mdc` + `fcop-protocol.mdc` to `.cursor/rules/`, and create `docs/agents/…` + `fcop.json` (minimal valid JSON per spec).  
3. **MCP** — `fcop-mcp` wires tools/IDE; **MCP is optional** and not required to use the protocol files.

---

## PyPI packages (optional)

- **`fcop`**: reference Python implementation.  
- **`fcop-mcp`**: exposes `fcop` over MCP.  

**The protocol is not tied to one language** — the filesystem contract is the portable part.

---

## Licence

[LICENSE](../LICENSE) in the repository root (MIT).

---

## Further reading (narrative, not normative)

- [60-second primer](../primer/fcop-primer.en.md)  
- [Spec entry point](../spec/fcop-spec.md)  
- [Essays / field reports](../essays/)  

To cite **FCoP without product or genealogy**, link this page; for **exact rules**, link `fcop-rules` / `fcop-protocol` and the versioned `fcop-spec-v*` documents.

---

- [简体中文](fcop-standalone.md)
