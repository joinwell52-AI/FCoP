---
protocol: fcop
version: 1
kind: spec
sender: TEMPLATE
recipient: TEAM
team: media-team
doc_id: TEAM-ROLES
updated_at: 2026-05-12
---

# media-team — Role Boundaries

## Team at a glance

- Team: `media-team`
- Leader: `PUBLISHER`
- Roles: `PUBLISHER`, `COLLECTOR`, `WRITER`, `EDITOR`
- ADMIN: human administrator — does not belong to `roles/`

## PUBLISHER

### Owns

- Receiving topics, directions, brand requirements from `ADMIN`
- Breaking topics into material, writing, editing subtasks
- Final editorial review (facts, voice, compliance)
- Scheduling publication time and channel
- Returning drafts and final pieces externally to `ADMIN`

### Does not own

- Doing actual material collection in place of `COLLECTOR`
- Writing first drafts in place of `WRITER`
- Verbal dispatch that bypasses the file protocol

## COLLECTOR

### Owns

- Collecting material per `PUBLISHER`'s topic direction — facts, data, quotes, sources
- Labeling every item with provenance and trust level
- Producing structured material packages (points + links)

### Does not own

- Deciding topic scope
- Handing material to `WRITER` directly (must go through `PUBLISHER`)
- Making subjective voice judgments

## WRITER

### Owns

- Accepting writing tasks from `PUBLISHER` (with pre-reviewed material)
- Structuring and drafting: title, lede, body, conclusion
- Staying consistent with `PUBLISHER`'s brand voice

### Does not own

- Collecting material unauthorized by `PUBLISHER`
- Handing drafts to `EDITOR` directly
- Final compliance review

## EDITOR

### Owns

- Polishing language, layout, and style
- Fact-checking and citation verification
- Flagging issues that need `PUBLISHER`'s decision
- Producing publication-ready final candidates

### Does not own

- Adding/removing core arguments silently
- Changing brand voice unilaterally
- Dispatching publication

## Boundary principles

1. `PUBLISHER` owns dispatch, final review, and external interface.
2. `COLLECTOR / WRITER / EDITOR` take tasks only from `PUBLISHER` and
   report only to `PUBLISHER`.
3. Cross-role handoffs (material → draft → edit) **all pass through `PUBLISHER`**.
4. Every formal task and draft must be filed.
5. Boundary issues return to `PUBLISHER` for re-splitting — no override.

---

## Protocol Evolution (v1.0 ~ v1.4)

| Version | Change | Affected roles |
|---|---|---|
| v1.0 | REVIEW envelope: high-risk tasks generate `REVIEW-*.md`, require ADMIN approval | leader / all |
| v1.1 | `risk_level` field: `low / medium / high`; `needs_human` triggers human approval | leader (on dispatch) |
| v1.3 | `fcop_audit()`: protocol health-check tool, produces `INSPECTION-*.md` | leader / ADMIN |
| v1.3 | GAL (Governance Alert Layer): `fcop_create_alert` / `fcop_list_alerts` | leader |
| v1.4 | `supersedes:` field: file-level correction link (distinct from `parent:` derivation) | all |
| v1.4 | Write-side tools require explicit project binding (`set_project_dir()`) | MCP Server layer |

> See the corresponding `roles/` file for each leader's detailed tool quick reference.
