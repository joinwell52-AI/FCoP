# FCoP 4.0 — idempotency

Audience: business-agent. Package: 4.0.0-candidate.1. Language: en.
Primary authority: frozen Core aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6, spec/fcop-4.0-spec.md.
This derived guidance grants no execution, adoption, Host or release authority.
Dependencies (explicit selection): workspace.

## F4.8.1

For ordinary and Branch TASK creation, key durable idempotency by workspace_id + operation_kind + operation_id and compare normalized_request_digest. Both use operation_kind=create_task; branch_of belongs in the digest, not another namespace.

## F4.8.2

Require operation_id to match [A-Za-z0-9][A-Za-z0-9._:-]* with length 1–128. Reserve the key atomically; memory-only deduplication or an unlocked scan is insufficient.

## F4.8.3

Same key/digest returns Existing with original task_id/path/digest and no file/event. Different digest returns OPERATION_ID_CONFLICT. Keep operation-kind namespaces separate and results available after restart.

## F4.8.4

Hash canonical fcop-create-task-v1 JSON containing workspace_id, operation_kind, operation_id, sender, recipient, subject, body, defaulted priority, parent, branch_of and references. Normalize strings to NFC, CRLF/CR to LF, body to one final LF; absent values become null, references deduplicate/sort by code point, keys sort with compact UTF-8 serialization. Use lowercase SHA-256. Exclude timestamps, allocated identity/path, thread_key, risk_level and Profile extensions; temporary validation switches are not request identity.

## F4.8.5

Keep the auditable operation fact durable in the Encoding-defined layout, not as a second NOW source. Repeat operation_id/kind/digest on TASK and reject duplicate or conflicting records.
