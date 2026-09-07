# FCoP 4.0 — authorization

Audience: business-agent. Package: 4.0.0-candidate.1. Language: en.
Primary authority: frozen Core aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6, spec/fcop-4.0-spec.md.
This derived guidance grants no execution, adoption, Host or release authority.
Dependencies (explicit selection): workspace, envelopes, relations.

## F4.7.1

Persist authority in an append-only authorization REVIEW: subject_ref, decision: authorize, operation_kind: lifecycle_transition, transition {from,to}, authorization_scope: single_use, issued_at, expires_at or null, attempt_id or null, family_digest or null, references and profile_ref. It is not a fifth envelope.

## F4.7.2

Only T4 acceptance or T5 rejection may also carry authority when every binding including profile_ref is present and trusted issuer evaluation is AUTHORIZED; otherwise cite a separate authorization REVIEW. Convergence alone never authorizes Root T7.

## F4.7.3

Check existing REVIEW type, adopted profile_ref, decision, subject, edge, attempt, family, validity time, reuse, evidence references and stored byte digests. Return AUTHORIZATION_REQUIRED/INVALID/EXPIRED/REUSED or EVIDENCE_DIGEST_MISMATCH as applicable; never accept partial matching.

## F4.7.4

Resolve issuer evaluation only through the adopted Profile's trusted registration. AUTHORIZED passes; DENIED and UNKNOWN both reject with AUTHORIZATION_INVALID. T4–T7 without a usable adopted Profile return AUTHORIZATION_PROFILE_UNAVAILABLE. Do not install caller-supplied judging logic or a Core role table.

## F4.7.5

Record authorization_ref and authorization_digest in the consuming transition. Sender, actor, Host allowlist, UI action or REPORT conclusion alone grants no authority.

## F4.7.6

Profile trust mechanisms such as local trust, OS ACLs or signatures stay outside Core. Editable files alone do not establish cryptographic identity security.

## F4.7.7

An empty Profile set is legal for T1–T3 and other ungated Base work. To complete an ordinary developer task, explicitly adopt a usable authorization Profile at initialization; no fixed role becomes mandatory Core.
