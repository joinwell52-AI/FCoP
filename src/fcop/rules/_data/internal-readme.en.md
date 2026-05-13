---
protocol: fcop
version: 1
kind: internal-archive
sender: SYSTEM
recipient: TEAM
internal_only: true
fcop_version: "{fcop_version}"
deployed_at: "{deployed_at}"
---

> ⚠️ **INTERNAL ONLY · DO NOT EXTERNALIZE WITHOUT REVIEW**
>
> This directory (`fcop/internal/`) is the **team-internal archive
> bucket**: for team self-audit / retrospective / decision trail
> only. **Must be reviewed and rewritten before any external
> publication** (strip raw quotes, sensitive persons, undisclosed
> decisions).

# fcop/internal/ — Team-Internal Archive Bucket

## What this is

This directory is deployed by
`Project.init(deploy_internal_template=True)` and corresponds to
**Rule 4.6** (fcop-rules.mdc v3.0.0+ / fcop@2.0.0+). It is an
**optional** sub-layer of `fcop/` (non-mandatory soft convention)
for **team-internal** archive material that is not directly
externalised:

- emergence-log (field-observed agent behaviour)
- self-disclosure (per-role retrospectives, PM diaries)
- decision-trail (ADMIN strategic quotes + which section absorbed them)
- upstream-issue drafts (before they go public on GitHub)
- ADMIN strategic raw quotes
- any draft material you don't want in git history yet, but want to
  preserve for future externalisation

## Boundaries with other directories

| Directory | Holds | Required? | Externally visible? |
|---|---|---|---|
| `fcop/{tasks,reports,...}` | coordination flow | yes (Rule 2) | yes |
| `fcop/internal/` (this bucket) | team-internal archive | **no** (Rule 4.6 soft) | optional, team's call |
| `docs/` | project external documentation | no | yes |
| `essays/` | public essays / philosophy | no | yes |
| `workspace/<slug>/` | task products (code / data) | no (Rule 7.5 soft) | yes |

## Recommended subdirectories

```
fcop/internal/
├── README.md              ← this file (carries internal-only declaration)
├── emergence-log/         ← field-observed emergence (e.g. codeflow / Bridgeflow)
├── self-disclosure/       ← per-role retrospectives, PM diaries
├── decision-trail/        ← ADMIN raw quotes + which section absorbed them
└── upstream-issues/       ← drafts before they go upstream
```

Subdirectories are not mandatory; create what you need.

## `internal-only` Declaration Syntax v1

Every `.md` file under `fcop/internal/` SHOULD carry a bilingual
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

Minimum requirements (per ADR-0034 §4.3):

1. Must be the **first block** after frontmatter (not buried mid-body).
2. Must contain the bilingual warning string `INTERNAL ONLY` /
   `内部档案` for greppability.
3. **Recommended**: pair with a frontmatter field
   `internal_only: true` for machine-readability (audit hooks honour
   this).

## Audit behaviour

`fcop_audit()` only emits **P3 (suggestion)** hints against this
bucket, never blocks:

- missing declaration block or `internal_only: true` field → P3 nudge
- carries `internal_only: true` but lives outside `fcop/internal/`
  → P3 misplaced-location flag

## Why this is a soft convention

Rule 4.6 mirrors Rule 7.5 (`workspace/` cage) in design pattern:
**prefer education over punishment** — hard rules sit only on Rules
0–4 / 5 / 7's destructive / truth red lines; directory organisation
and naming conventions live entirely under soft conventions, letting
the protocol grow **self-evolving muscle** rather than rigid bone.

## References

- Rule source: `fcop-rules.mdc` Rule 4.6 (v3.0.0+)
- Full commentary: `fcop-protocol.mdc` §How Rule 4.6 Applies (v3.0+)
- Design decision: ADR-0034 §4.3 "internal-only declaration syntax v1"
- Related essays:
  - `essays/evolution-reverse-absorption.md` (Reverse Absorption,
    Chinese)
  - `essays/evolution-reverse-absorption.en.md` (English)
