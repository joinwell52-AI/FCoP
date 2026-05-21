---
protocol: fcop
version: 1
type: REVIEW
review_id: REVIEW-20260521-003-ADMIN-on-fcop-3-0-sealed
subject_type: code_change
subject_ref: spec/fcop-3.0-spec.md + spec/fcop-3.0-rfc.md + essays/the-day-we-almost-added-custody.md
reviewer_role: ADMIN
decision: approved
decided_at: "2026-05-21T18:30:00+08:00"
subject: FCoP 3.0 SEALED - canonical spec + RFC projection + immune-memory essay
---

# FCoP 3.0 · Final Sealing · Spec + RFC + Essay

## 1. Scope

本 REVIEW **封口 FCoP 3.0**。覆盖第二轮 RFC 评审之后的全部产物：

| Subject | Path | Role |
|---------|------|------|
| Single-page formal spec | `spec/fcop-3.0-spec.md` | Canonical normative |
| IETF-style RFC projection | `spec/fcop-3.0-rfc.md` | External stable surface |
| Immune-memory essay | `essays/the-day-we-almost-added-custody.md` | Community memory |
| Editorial patch archive | `.fcop/proposals/20260521-spec-editorial-patch-and-rfc-projection.md` | Process record |

---

## 2. Editorial Patches Accepted

第二轮 RFC 指出 3 个协议级风险点，全部已处理：

| # | 位置 | 处理 |
|---|------|------|
| R1 | spec §0 双句结构 | 合并为单句 canonical statement |
| R2 | spec §1.1.1 substrate assumption | 新增"FCoP 3.0 assumes a single-consistent filesystem boundary" |
| R3 | spec §2.4 event 历史性弱化 | 加 "event = transition itself, witnessed in writing" |

三处均为 Editorial PATCH（不 bump 版本号），符合 spec §10 的 PATCH 定义。

---

## 3. Decision

| 产物 | Decision | Action |
|------|----------|--------|
| spec 三处微调 | `approved` | 落入 3.0 范围内 editorial patch |
| RFC projection (`fcop-3.0-rfc.md`) | `approved` | 作为 spec 的外部稳定面同步发布 |
| Essay (`the-day-we-almost-added-custody.md`) | `approved` | 进入 essays/ 系列，与现有 14 篇 field report 并列 |
| Rules 同步（P2）| `deferred` | 等 fcop-mcp 3.0 实现稳定后再升级 |

**FCoP 3.0 SEALED.** 

---

## 4. 协议最终形态

```
┌───────────────────────────────────────────────────────────────────┐
│                        FCoP 3.0 Sealed                            │
├───────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Normative Documents（规范层）                                     │
│    spec/fcop-3.0-spec.md      (canonical, presentation-oriented) │
│    spec/fcop-3.0-rfc.md       (IETF-style, external-stable)      │
│                                                                   │
│  Justification（决策层）                                           │
│    adr/ADR-0035 · State Ontology       (Accepted & Frozen)       │
│    adr/ADR-0036 · Event Layer          (Accepted)                │
│    adr/ADR-0038 · Boundary Charter     (Accepted)                │
│    adr/NOTE-custody-is-not-a-layer     (Informative)             │
│                                                                   │
│  Process Records（演进证据）                                       │
│    .fcop/proposals/20260521-rfc-semantic-collapse...md            │
│    .fcop/proposals/20260521-spec-editorial-patch...md             │
│    fcop/reviews/REVIEW-20260521-001..003                          │
│                                                                   │
│  Community Memory（社区记忆）                                       │
│    essays/the-day-we-almost-added-custody.md                      │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

---

## 5. Canonical Statement

> **FCoP is a filesystem-native protocol where file location defines current state, and all historical and ownership semantics are derived from append-only transition traces.**

One-liner:

> **FCoP = file location is truth; everything else is trace.**

---

## 6. Post-Sealing Roadmap（不属于本 REVIEW 范围，仅记录）

| 优先级 | 动作 |
|--------|------|
| P0 | 实现 fcop-mcp 3.0（按 spec §C1-C10 + P1-P5 实现）|
| P0 | `fcop migrate --to-v3` 一键迁移脚本 |
| P1 | rules 升级（`.cursor/rules/fcop-rules.mdc` Rule 2 注入 canonical one-liner）|
| P1 | spec + RFC 双语版本（Chinese parallel）|
| P2 | Zenodo DOI 申请（fcop-3.0-spec.md + rfc 作为 research snapshot）|
| P2 | 社区发布（GitHub Release / Cursor Forum / Dev.to）|

任何后续 spec 变更必须经过 ADR-0038 §5 五问 + §5.1 豁免条款审查。

---

## 7. 一句话封口

> **2026-05-21，FCoP 完成了一次完整的协议级跃迁：从"文件组织协议"到"文件系统行为流转协议"，再到"文件系统在多 agent 环境中的状态物理学定义"。**
>
> **协议在三次拒绝之后停了下来。这是 protocol semantic sealing。**

---

*FCoP 3.0 · Final Sealing · ADMIN signed-off · 2026-05-21T18:30:00+08:00*
