# FCoP 4.0 — envelopes

Audience: business-agent. Package: 4.0.0-candidate.1. Language: en.
Primary authority: frozen Core aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6, spec/fcop-4.0-spec.md.
This derived guidance grants no execution, adoption, Host or release authority.
Dependencies (explicit selection): workspace.

## F4.3.1

Create only TASK, REPORT, ISSUE and REVIEW as formal business envelopes. shared/ holds knowledge; locks, receipts and indexes are not additional envelopes.

## F4.3.2

Use UTF-8/LF YAML frontmatter plus Markdown, with protocol: fcop, version: 4, type, typed ID, workspace_id, sender, recipient and timezone-aware created_at. TASK also needs subject/transitions; REPORT subject_ref/attempt_id/report_kind/result; ISSUE subject_ref/severity; REVIEW review_kind/subject_ref/decision. TASK may carry parent/branch_of/references/operation_id/operation_kind/normalized_request_digest; REPORT and ISSUE may carry references; REVIEW may carry attempt_id/family_digest/authorization_ref/references and authorization bindings. Do not confuse Profile fields with these Core fields.

## F4.3.3

Never edit or delete landed REPORT, ISSUE or REVIEW facts. Correction, replacement or revocation appends a new envelope of the same type citing affected facts through references.

## F4.3.4

Use final or replacement REPORT kinds. A replacement cites the current head of the same subject/attempt; the sole valid head is not referenced by another valid replacement. No head means REPORT_REQUIRED; multiple heads mean REPORT_HEAD_AMBIGUOUS.

## F4.3.5

Recognize assessment, acceptance, rejection, reopen, authorization, convergence and repair REVIEW kinds. Human approval, if exposed, appends REVIEW rather than modifying an old one.
