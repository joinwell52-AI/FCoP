# FCoP 4.0 — convergence

Audience: business-agent. Package: 4.0.0-candidate.1. Language: en.
Primary authority: frozen Core aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6, spec/fcop-4.0-spec.md.
This derived guidance grants no execution, adoption, Host or release authority.
Dependencies (explicit selection): workspace, envelopes, relations, authorization, idempotency, recovery, lifecycle, compatibility.

## F4.5.3

A Branch points to a Root with no branch_of; it cannot itself be a Branch Root. All Branches are siblings. Reject deeper nesting with BRANCH_DEPTH_EXCEEDED.

## F4.5.4

Create Branches only while the Root is unique and active; otherwise ROOT_NOT_ACTIVE. A done Root needs authorized T6 before new parallel work.

## F4.6.5

Inside one family boundary, Root T7 requires a unique done non-Branch Root, every Branch done/archive, one valid REPORT for each current Branch attempt, each Branch's own T3/T4 completion, exact current REPORT convergence coverage, freshly matching family_digest and Root authorization bound to it. Nonterminal Branch means BRANCH_NOT_TERMINAL. Use convergence REVIEW with subject_ref=Root, family_digest and references to Branch REPORTs; this REVIEW does not itself supply archive authority.

## F4.6.6

Compute lowercase SHA-256 of compact UTF-8 canonical JSON {contract:fcop-family-v1,root_task_id,branches:[{branch_task_id,attempt_id,report_id,report_digest}]}. Collect all TASKs pointing to Root; use current attempts and unique heads; report_digest hashes full validated UTF-8/LF REPORT bytes. Sort branches by branch_task_id and every object's keys by Unicode code point; no BOM, trailing LF or whitespace. Exclude stage, mtime, enumeration order, Runtime counters and in-memory generations.

## F4.6.7

Convergence references exactly every current Branch REPORT and optionally Root's current REPORT. Missing/stale/other-attempt coverage or digest mismatch returns FAMILY_CONVERGENCE_MISMATCH. Both done and archive count as completed Branch states.

## F4.6.8

Branch creation/reopen/new attempt or valid replacement REPORT invalidates old convergence by changing the canonical object/bytes. Branch done→archive alone changes no digest. Root T7 recomputes under the same family boundary; never authorize with a stale pre-lock value.
