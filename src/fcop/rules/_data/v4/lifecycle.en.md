# FCoP 4.0 — lifecycle

Audience: business-agent. Package: 4.0.0-candidate.1. Language: en.
Primary authority: frozen Core aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6, spec/fcop-4.0-spec.md.
This derived guidance grants no execution, adoption, Host or release authority.
Dependencies (explicit selection): workspace, envelopes, relations, authorization, idempotency, recovery.

## F4.4.1

Locate the authoritative TASK in exactly one fcop/_lifecycle/{inbox,active,review,done,archive}/TASK-*.md path. This location alone is current state.

## F4.4.2

Apply exactly seven gates: T1 None→inbox requires absent TASK; T2 inbox→active requires unique inbox TASK and starts an attempt; T3 active→review requires unique active TASK and current valid REPORT; T4 review→done requires T3-bound REPORT, acceptance REVIEW and authorization; T5 review→active requires rejected current REPORT, rejection REVIEW and authorization, and starts an attempt; T6 done→active requires reopen/authorization REVIEW and authorization, no REPORT, and starts an attempt; T7 done→archive reuses accepted evidence and requires archive authorization, plus convergence when Branches exist. T1–T3 need no Base authorization (Profiles may add policy to T2/T3). T1/T3/T4/T7 start no attempt. Convergence details belong to convergence; authority validation belongs to authorization.

## F4.4.3

Commit one edge and append one transition per command. Split convenience chains; an earlier failure cannot fabricate later events.

## F4.4.4

Reject active→done shortcuts with LEGACY_TRANSITION_NOT_ALLOWED. Legacy finish_task cannot bypass T3/T4 in a 4.0 workspace.

## F4.4.5

Record at/from/to/by/tool, adding new attempt_id on active entry. Persist aligned evidence_ref/evidence_digest arrays for all consumed REPORT/REVIEW, plus authorization_ref/authorization_digest where applicable. Digest complete validated UTF-8/LF bytes with lowercase SHA-256; later drift means EVIDENCE_DIGEST_MISMATCH. Append events; never derive NOW from them.

## F4.4.6

Archive is terminal: no authoritative move to history or back. v3 history is read-only Legacy; cold export can only make non-authoritative copies.

## F4.4.7

Any unlisted edge returns INVALID_TRANSITION. Ordinary T7 requires unique done state, valid strong relations and valid authorization; ordinary parent children and ISSUE state add no Base gate. Extra policies belong to an explicit Profile.

## F4.6.1

Every T2/T5/T6 active entry creates a non-reusable urn:uuid attempt_id. The last active-entry transition supplies the current attempt.

## F4.6.2

T3 consumes the unique REPORT for this TASK and current attempt; an earlier attempt's REPORT cannot satisfy it.

## F4.6.3

T4 acceptance REVIEW must say approved and bind the current subject, attempt and REPORT. Apply the authorization module, and store REPORT/REVIEW/authorization identities and byte digests under F4.4.5.

## F4.6.4

Ordinary and Branch TASKs share these same lifecycle/evidence gates; there is no separate Branch completion state.
