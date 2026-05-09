# GitHub Issue #2 回复草稿（v1.0.0-rc.1 progress update）

> **Status**: Draft — 由 TASK-20260509-009 准备；提交到 issue #2 的命令见
> 文末"How to publish"段。在那之前不要替 ADMIN 决定何时 push。
>
> **Target**: <https://github.com/joinwell52-AI/FCoP/issues/2>

---

```markdown
## v1.0 progress update — RC just landed

Hi @joinwell52-AI, thanks again for the original proposal. Posting a
**status update** now that `fcop@1.0.0-rc.1` is on the branch and the
relevant decisions have crystallised. Final 1.0.0 tag is
2-4 weeks out (waiting on Phase 2 of the workspace refactor +
`MIGRATION-1.0.md` — see Roadmap below); this RC freezes the
**protocol surface** so downstream can start integrating.

### TL;DR

- **1 of your 5 fields is shipping in v1.0** — but generalized:
  `Agent.layer` became the full **Boundary abstraction** (layer +
  10-token `can`/`cannot` capability bundle + 4 normative rules + a
  `BOUNDARY_VIOLATED` event), per ADR-0020.
- **4 of your 5 fields are deferred** — but each has its own
  Accepted-status ADR with the field shape preserved, so they're not
  in limbo. They split as: 2 → v1.1+ (additive minor), 2 → v1.2+
  (the `needs_human` family — see "why deferred" below).
- The protocol got a **bigger reframing than your proposal asked
  for** — turns out the field-level pressure you surfaced was a
  symptom of a deeper missing layer. v1.0 is now scoped as
  **"Agent Runtime Protocol — the AI OS protocol layer"** with
  **7 frozen core abstractions** (Agent / IPC / Encoding / Event /
  Failure / Boundary / Audit), all with JSON Schemas under
  `spec/schemas/`. See [ADR-0015 charter](https://github.com/joinwell52-AI/FCoP/blob/main/adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md).

---

### Field-by-field status

| # | Your proposal | v1.0 status | ADR | Notes |
|---|---|---|---|---|
| 1 | `Agent.layer: worker / governance / admin` | **✅ Shipped (generalized to Boundary)** | [ADR-0020](https://github.com/joinwell52-AI/FCoP/blob/main/adr/ADR-0020-agent-boundary-and-capability.md) | layer + 10-token `can`/`cannot` bundle + 4 normative rules + `Project.assert_boundary` + `BOUNDARY_VIOLATED` event |
| 2 | `Task.risk_level: low / medium / high / irreversible` | ⏳ **Deferred → v1.1+** | [ADR-0011](https://github.com/joinwell52-AI/FCoP/blob/main/adr/ADR-0011-task-risk-level-field.md) | Field shape preserved; Accepted ADR records the proposal verbatim |
| 3 | `Review.decision = needs_human` | ⏳ **Deferred → v1.2+** | [ADR-0012](https://github.com/joinwell52-AI/FCoP/blob/main/adr/ADR-0012-review-decision-needs-human.md) | v1.0 freezes a 4-value enum (`approved / changes_requested / blocked / rejected`) deliberately — see "why deferred" |
| 4 | `Review.human_approval` (sub-structure) | ⏳ **Deferred → v1.2+** | [ADR-0013](https://github.com/joinwell52-AI/FCoP/blob/main/adr/ADR-0013-review-human-approval.md) | Pairs with #3; both land together |
| 5 | `Skill.tools[]` risk metadata | ⏳ **Deferred → v1.1+** | [ADR-0014](https://github.com/joinwell52-AI/FCoP/blob/main/adr/ADR-0014-skill-tools-risk-metadata.md) | Pairs with #2; both land together |

---

### What v1.0 actually shipped (the bigger story)

Your proposal exposed that the protocol-vs-runtime line was unclear,
which led to a charter rewrite. v1.0 now positions FCoP as the
**AI OS protocol layer** (the slot POSIX occupies in Unix), and
freezes 7 abstractions instead of just adding 5 fields:

| # | Abstraction | ADR | Schema |
|---|---|---|---|
| 1 | **Agent** (lifecycle + identity + Boundary) | [ADR-0015](https://github.com/joinwell52-AI/FCoP/blob/main/adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md) §abstr. 1 + [ADR-0020](https://github.com/joinwell52-AI/FCoP/blob/main/adr/ADR-0020-agent-boundary-and-capability.md) | `agent.schema.json` + `boundary.schema.json` |
| 2 | **Encoding** (filename + frontmatter + workspace) | [ADR-0021](https://github.com/joinwell52-AI/FCoP/blob/main/adr/ADR-0021-encoding-abstraction.md) + [ADR-0022](https://github.com/joinwell52-AI/FCoP/blob/main/adr/ADR-0022-workspace-directory-convention.md) | `encoding.schema.json` |
| 3 | **IPC** (TASK / REPORT / ISSUE / **REVIEW** envelopes) | [ADR-0017](https://github.com/joinwell52-AI/FCoP/blob/main/adr/ADR-0017-review-file-type-minimal.md) | `ipc-envelope.schema.json` + `review.schema.json` |
| 4 | **Event Model** (12 event types + subscribe) | [ADR-0018](https://github.com/joinwell52-AI/FCoP/blob/main/adr/ADR-0018-event-model.md) | `event.schema.json` |
| 5 | **Failure & Recovery** (4 failure × 5 recovery) | [ADR-0019](https://github.com/joinwell52-AI/FCoP/blob/main/adr/ADR-0019-failure-and-recovery-semantics.md) | `failure.schema.json` |
| 6 | **Boundary** (capability bundle, ⬅ your Field 1) | [ADR-0020](https://github.com/joinwell52-AI/FCoP/blob/main/adr/ADR-0020-agent-boundary-and-capability.md) | `boundary.schema.json` |
| 7 | **Audit** (REVIEW minimal v1.0 surface) | [ADR-0017](https://github.com/joinwell52-AI/FCoP/blob/main/adr/ADR-0017-review-file-type-minimal.md) | `review.schema.json` |

Reference implementation is fully wired in `fcop@1.0.0-rc.1`; cross-
schema `$ref` resolves via `referencing.Registry`. JSON-Schema 2020-12
copies ship in the wheel and are byte-identical to the spec/schemas/
sources, guarded by tests.

---

### Why fields 3 & 4 (`needs_human` / `human_approval`) were deferred

Short version: per [ADR-0017 §"Minimal v1.0 Surface"](https://github.com/joinwell52-AI/FCoP/blob/main/adr/ADR-0017-review-file-type-minimal.md),
v1.0 deliberately freezes a 4-value `decision` enum
(`approved` / `changes_requested` / `blocked` / `rejected`) without
`needs_human`, because:

1. The `needs_human` decision + the `human_approval` audit struct
   together turn the Review role into a **god-tier gatekeeper**
   ("Review is everything") — that contradicts the v1.0 framing
   where Review is one of seven equal abstractions.
2. The `human_approval.evidence` sub-struct (your `auth_method`
   enum + `device_id` + `ip`) has zero field evidence in real FCoP
   projects — it would be the first thing in v1.0 that we
   *invented* rather than *discovered*. v1.0's tiebreaker rule
   (per [ADR-0015 §"FCoP is discovered, not invented"](https://github.com/joinwell52-AI/FCoP/blob/main/adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md#fcop-is-discovered-not-invented))
   is "answer no → defer".
3. The escalation use cases you cite (paid-API > $10, missing
   `tenant_id` clause) are real, but they're better modelled as a
   **Boundary capability check** (Field 1, already shipped) than as
   a Review decision. We expect to learn whether your specific
   use cases collapse into Boundary in v1.1, and if not, those
   are exactly the field signals we'll need to land #3+#4 in v1.2.

So both fields are **alive** (Accepted ADRs preserve the proposal
verbatim) but **paused for evidence**.

---

### How v1.0 changes affect your CodeFlow `peerDependencies` plan

You wrote: `peerDependencies: { "fcop": ">=1.1.0" }`. Here's the
recommended adjustment:

```jsonc
{
  "peerDependencies": {
    "fcop": ">=1.0.0,<2.0.0"
  }
}
```

— bump now, get Field 1 (Boundary) immediately. Fields 2 & 5 land in
v1.1; pin a stricter `>=1.1.0` then. Fields 3 & 4 land in v1.2.

The TS reference impl in `packages/codeflow-protocol/` should mirror
the **7 schemas** under `spec/schemas/` (not the previous "5 schemas"
shape from ADR-0008 era — that ADR was superseded by
[ADR-0016](https://github.com/joinwell52-AI/FCoP/blob/main/adr/ADR-0016-json-schema-for-7-abstractions.md)).
A cross-language fuzz test that loads `spec/schemas/*.schema.json`
verbatim and validates the same fixtures in TS + Python is exactly
the kind of conformance test we'd merge into the FCoP test matrix —
let's open a tracking issue once `codeflow-protocol@1.0.0-rc` is
ready.

---

### Roadmap

| When | What |
|---|---|
| **2026-05-09 (today)** | `fcop@1.0.0-rc.1` on branch — protocol surface frozen |
| 2026-05-13 ~ 2026-05-15 | ADR-0022 Phase 2 (Project workspace_dir refactor) + `MIGRATION-1.0.md` |
| 2026-05-16 ~ 2026-05-20 | `fcop@1.0.0` final tag + PyPI publish + Zenodo DOI bump |
| **v1.1** (target ~Q3 2026) | Fields 2 + 5 (`Task.risk_level` + `Skill.tools[]` risk meta) — both ADRs already Accepted, just need impl + tests |
| **v1.2** (target Q4 2026) | Fields 3 + 4 (`needs_human` + `human_approval`) — gated on field evidence beyond your single use case |

---

### What I'm asking from you

1. **Does the Field 1 → Boundary generalisation match your CodeFlow
   runtime design?** I.e. can `worker / governance / admin` layer
   bundles + a 10-token `can`/`cannot` cover your needs, or does the
   TS impl need finer-grained capability tokens?
2. **Are you OK with the `>=1.0,<2.0` pin recommendation** so you
   can start integrating immediately, or would you prefer to wait
   for `1.1.0`?
3. **For Fields 3+4 deferred to v1.2** — would you like to
   contribute additional field evidence (real failure modes from
   CodeFlow runtime that *required* `needs_human` and could not be
   modelled as a Boundary check)? That would directly accelerate
   v1.2 timing.

Will keep this issue open until Fields 2+5 ship in v1.1; then
re-evaluate the deferred pair.

— ME (FCoP maintainer, posting on behalf of ADMIN per solo-mode
sign-off in REPORT-20260509-009)

---

**References**:
- v1.0 charter: [ADR-0015](https://github.com/joinwell52-AI/FCoP/blob/main/adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md)
- v1.0.0-rc.1 release notes: [docs/releases/1.0.0-rc.1.md](https://github.com/joinwell52-AI/FCoP/blob/main/docs/releases/1.0.0-rc.1.md)
- 7 ADRs (Accepted): [ADR-0015..0022](https://github.com/joinwell52-AI/FCoP/tree/main/adr)
- 5 deferred ADRs (the original 5 fields, preserved verbatim): [ADR-0011](https://github.com/joinwell52-AI/FCoP/blob/main/adr/ADR-0011-task-risk-level-field.md), [ADR-0012](https://github.com/joinwell52-AI/FCoP/blob/main/adr/ADR-0012-review-decision-needs-human.md), [ADR-0013](https://github.com/joinwell52-AI/FCoP/blob/main/adr/ADR-0013-review-human-approval.md), [ADR-0014](https://github.com/joinwell52-AI/FCoP/blob/main/adr/ADR-0014-skill-tools-risk-metadata.md)
- 7 JSON Schemas: [`spec/schemas/`](https://github.com/joinwell52-AI/FCoP/tree/main/spec/schemas)
- New `Rule 9 · v1.0 Capabilities` in bundled rules: [`src/fcop/rules/_data/fcop-rules.mdc`](https://github.com/joinwell52-AI/FCoP/blob/main/src/fcop/rules/_data/fcop-rules.mdc) (1.9.0)
```

---

## How to publish (ADMIN action required)

```powershell
# 1. Review the markdown body inside the triple-backtick block above.
# 2. From repo root, post it as a comment on issue #2:
gh issue comment 2 `
  --repo joinwell52-AI/FCoP `
  --body-file - < (Get-Content docs/issue-2-reply-draft.md `
                   | Select-String -Pattern '^```(?:markdown)?$' -SimpleMatch -Context 0,99999 `
                   | ...)
```

Easier path — manually copy the body between the
`` ```markdown `` … `` ``` `` fences and paste into
`docs/issue-2-reply-body.md`, then:

```powershell
gh issue comment 2 --repo joinwell52-AI/FCoP --body-file docs/issue-2-reply-body.md
```

**Why ME does not auto-post**: per Rule 7 (destructive operations),
posting to a public GitHub Issue under the project's identity is an
externally-visible commitment that requires ADMIN's explicit second
confirmation — even in solo mode. The draft is committed to the
repo for ADMIN review; the actual `gh issue comment` invocation is
deliberately left to ADMIN.
