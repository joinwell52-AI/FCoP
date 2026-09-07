# FCoP 4.0 — recovery

Audience: business-agent. Package: 4.0.0-candidate.1. Language: en.
Primary authority: frozen Core aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6, spec/fcop-4.0-spec.md.
This derived guidance grants no execution, adoption, Host or release authority.
Dependencies (explicit selection): workspace.

## F4.9.1

Classify recovery as exactly NOT_COMMITTED, COMMITTED, RECOVERABLE_DUPLICATE, DIVERGENT_DUPLICATE or INDETERMINATE. Cross-directory operations can have intermediate physical states; INDETERMINATE never means success.

## F4.9.2

Never silently overwrite a target. Creation may return Existing under the idempotency module; matching lifecycle duplicates use recovery classification, not a general replay promise. Different target content returns TARGET_ALREADY_EXISTS_DIFFERENT.

## F4.9.3

Multiple authoritative TASK stages mean STATE_AMBIGUOUS. Do not select NOW by mtime, enumeration order or event replay.

## F4.9.4

Use a durable receipt for each lifecycle operation with identity, source/target paths, normalized/content digests and stage. Mechanical recovery creates neither a second TASK nor a second event or overwrite. Unprovable corruption/divergence returns RECOVERY_REQUIRED and preserves every copy.

## F4.9.5

Use one short Root-family linearization boundary for Branch creation, Root/Branch T2–T7, Branch REPORT create/replacement, convergence create/replacement and all Root archive conditions. Re-read Root state, Branch set, attempts, REPORT heads, digest and authorization after acquiring it. Never authorize from pre-lock caches; never hold this boundary across Agent work or unrelated ordinary TASKs.

## F4.9.6

Locks, receipts and indexes remain Toolkit/Encoding details. Never delete a lock merely because it is old; unprovable safe release returns LOCK_RECOVERY_REQUIRED.

## F4.9.7

Only supported local NTFS/POSIX semantics are covered. Unsupported cross-device, network, distributed or weakly consistent storage without an external consistency layer returns UNSUPPORTED_FILESYSTEM or fails closed.

## F4.9.8

Keep three guarantees separate: external create TASK/Branch idempotency uses operation_id; internal crash recovery for every transition uses its receipt; T4–T7 lost-response retry uses consumed authorization plus digest and edge. T2/T3 have no arbitrary-time external replay promise.

## F4.9.9

Apply the unique table: matching source/no target with no receipt or PREPARED => NOT_COMMITTED, preserve source; same-digest source+target with TARGET_DURABLE => RECOVERABLE_DUPLICATE, verify then remove source/persist directory/complete receipt; no source/matching target with TARGET_DURABLE or COMMITTED => COMMITTED, finish receipt without moving again; different source+target => DIVERGENT_DUPLICATE, preserve both for human disposition; both missing or damaged/conflicting receipt/identity/digest => INDETERMINATE, preserve evidence and fail closed. Logical stages are PREPARED, TARGET_DURABLE, COMMITTED.

## F4.9.10

Proven duplicate recovery completes only the receipt, not a business REVIEW. Human resolution of divergent/indeterminate states appends repair REVIEW. Receipt is neither envelope nor NOW nor Runtime database. Test abstract stages rather than incidental temporary filenames.

## F4.9.11

For lost-response T4–T7 retry, return the existing commit only when authorization_ref, authorization digest, edge and stored evidence digests all match. Use of consumed authority on a different edge returns AUTHORIZATION_REUSED; ambiguity fails closed.
