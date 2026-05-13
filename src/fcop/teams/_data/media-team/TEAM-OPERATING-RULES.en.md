---
protocol: fcop
version: 1
kind: rules
sender: TEMPLATE
recipient: TEAM
team: media-team
doc_id: TEAM-OPERATING-RULES
updated_at: 2026-05-12
---

# media-team — Operating Rules

## 1. Basic routing

1. `ADMIN ↔ PUBLISHER` is the only external interface.
2. `COLLECTOR / WRITER / EDITOR` take tasks only from `PUBLISHER` and report
   only to `PUBLISHER`.
3. Cross-role handoffs (`COLLECTOR ↔ WRITER`, `WRITER ↔ EDITOR`) are
   not allowed — **all handoffs go through `PUBLISHER`**.
4. Cross-role needs go back to `PUBLISHER`, who decides whether to split a
   new task.

## 2. Dispatch rules

### PUBLISHER does directly

- Topic clarification, brand voice definition
- Task splitting, priority ranking
- Final review (facts, voice, compliance)
- Publication scheduling
- Phase reports to `ADMIN`

### PUBLISHER dispatches to COLLECTOR

- Material gathering, fact-check, data collection
- Citation sourcing
- Competitive / trending research

### PUBLISHER dispatches to WRITER

- First draft (dispatched with **pre-reviewed material package**)
- Title / lede / structural adjustment
- Column-style rewrite

### PUBLISHER dispatches to EDITOR

- Language polish, layout norms
- Fact-check, citation verification
- Pre-publication format cleanup

## 3. Handoff rules

1. Every handoff is "task + previous-round artifact". Downstream roles may
   not pull files from upstream directly.
2. `PUBLISHER` attaches the material package to `PUBLISHER-to-WRITER` tasks
   (or places it under `shared/` and references it).
3. `EDITOR` receives drafts routed back through `PUBLISHER`, not from
   `WRITER` directly.
4. Every handoff leaves a traceable file record.

## 4. Report rules

1. Every task has a matching report.
2. Reports must state: status, artifact produced, open issues, next step.
3. Formal reports from `COLLECTOR / WRITER / EDITOR` all target `PUBLISHER`.
4. `PUBLISHER` consolidates and sends a unified status/final to `ADMIN`.
5. Verbal sync is not a report — it must be filed.

## 5. Thread and cadence

1. One `thread_key` (a full piece lifecycle) has one active driver — by default, `PUBLISHER`.
2. Other roles handle only their received subtasks.
3. Return to `PUBLISHER` promptly — no backlog, no silence.
4. `PUBLISHER` decides whether to advance to the next stage or archive.

## 6. When to escalate to ADMIN

- Topic direction needs adjustment
- Compliance / legal / factual dispute requires arbitration
- Material gaps block the plan
- Publication channel or timing change
- Brand voice conflict

## 7. High-risk action rules

Record and confirm before execution:

- Formal publication on public channels (blogs, channels, social)
- Content involving third-party accounts, partnerships, licensed quotes
- Deleting published content or public retraction
- Content on sensitive topics or people

Published content cannot be silently modified — revision notes are mandatory.

## 8. Documents and archival

1. Flow files go in `tasks/`, `reports/`, `issues/`.
2. Material packages, draft history, brand specs go in `shared/`.
3. Published work is archived by `PUBLISHER`.
4. `shared/` docs may be updated in place; tasks/reports are append-only.

## 9. Operating stance

The goal is not to have every role drafting at once, but to make every
step of every piece attributable:

- `PUBLISHER` owns dispatch, review, external
- `COLLECTOR` owns facts and material
- `WRITER` owns structure and prose
- `EDITOR` owns quality and compliance

Each step traceable → pieces reliable → brand trustworthy.

---

## Protocol Evolution Addendum (v1.0 ~ v1.4)

Key operating rule changes introduced in recent protocol versions:

### High-risk task approval (introduced v1.0)

- Leader marks dispatch with `risk_level: high`; system generates `REVIEW-*.md`
- Tasks with `needs_human: true`: execution roles **stop and wait** for ADMIN
  to call `mark_human_approved()`
- No approval → no execution; this overrides any schedule pressure

### Handling fcop_audit remediation tasks (introduced v1.3)

- After ADMIN / leader runs `fcop_audit()`, `INSPECTION-*.md` records compliance gaps
- Remediation tasks (`TASK-*-ADMIN-to-PM.md`) may be batch-authorized
  (`scope: batch-remediation` in proposal frontmatter)
- Handle remediation tasks with the standard four-step workflow; reference the
  INSPECTION ID in your report

### Write-side binding requirement (introduced v1.4)

- Write-side MCP tools now require an explicit project path binding
- Configure via `FCOP_PROJECT_DIR` env var in MCP config, or call
  `set_project_dir()` at session start
- Calling any write tool without binding raises `WriteRefused`


---

## §internal-only Declaration Syntax (v3.0+, per Rule 4.6)

> Since fcop@2.0.0 / `fcop_rules_version: 3.0.0`, teams may opt in to
> the "team-internal archive bucket" by having ADMIN call
> `Project.init(deploy_internal_template=True)`, which deploys the
> `fcop/internal/` sub-layer (Rule 4.6 non-mandatory soft convention).

- Any `.md` file under `fcop/internal/` SHOULD carry a bilingual
  declaration block right after the YAML frontmatter:

```markdown
---
protocol: fcop
version: 1
kind: internal-archive
sender: PM
recipient: PM
internal_only: true
---

> ⚠️ **INTERNAL ONLY · DO NOT EXTERNALIZE WITHOUT REVIEW**
>
> (file purpose description)

# Body title
...
```

- Full template and rationale: `fcop/internal/README.md` (deployed
  automatically), `fcop-rules.mdc` Rule 4.6, `fcop-protocol.mdc`
  §How Rule 4.6 Applies.
- `fcop_audit()` only emits P3 (suggestion) hints against this bucket
  and never blocks any write.
