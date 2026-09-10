# WP3A architecture delta

## Outcome and scope

This package implements only the 4.0 creation plane behind `fcop.Project`.
It is an unreleased implementation candidate, not full FCoP 4.0 conformance.
ADMIN acceptance and all later stage gates remain external decisions.
The task/authority and exact file inventory are in
`reports/FCOP-4.0-WP3A-IMPLEMENTATION-PLAN.md`.

```yaml
NEW_RUNTIME_DEPENDENCIES: 0
NEW_BACKGROUND_COMPONENTS: 0
NEW_AUTHORITATIVE_STORES: 0
PUBLIC_API_ADDITIONS:
  - Project.trusted_profiles constructor argument
  - Project.create_workspace
  - Project.derive_workspace
  - Project.create_task
  - Project.inspect_state
  - Project.transition (rejection boundary only)
  - Project.finish_task (rejection boundary only)
  - fcop.errors.V4ProtocolError
V3_PATHS_TOUCHED:
  - src/fcop/project.py
  - src/fcop/errors.py
  - tests/test_fcop/snapshots/public_surface.json
MCP_IMPLEMENTATION_MODIFIED: false
SCHEMA_MODIFIED: false
FROZEN_FILES_MODIFIED: 0
VERSION_RELEASE_DEPENDENCY_CONFIG_MODIFIED: false
WP3B_STARTED: false
```

## Module responsibilities

| Module | Responsibility | Core relationship |
|---|---|---|
| `src/fcop/v4/boundary.py` | One descriptor-based Project boundary; native legacy binding or private v4 handler | C1 version isolation; C6 trust surface only |
| `src/fcop/v4/encoding.py` | Strict UTF-8/LF, unique mapping keys, safe paths, canonical JSON, local filesystem capabilities, no-overwrite publication, kernel key locks | C1/C2 encoding; C7 durable creation |
| `src/fcop/v4/creation.py` | Private creation context, workspace identity, envelope validation/append, T1 request plan and commit | C1/C2/C7; C4 static references only |
| `src/fcop/v4/__init__.py` | Private package declaration; no second public facade | No new protocol object |
| `src/fcop/errors.py` | Additive FcopError subtype and centralized code enum | F4.10 machine errors |
| `tests/test_fcop/test_v4_creation.py` | 48 production-API/encoding tests, including spawned process races | Implementation evidence, not replacement conformance |

No database, server, background worker, global authority registry, new role,
or fifth envelope exists. The private `_Creation` object is reached through
Project and is not a public V4Project/Runtime product surface.

## Version and compatibility boundary

`Project.__init__` reads a declaration once. Directory shape and business
arguments never select v4. An explicitly declared 4.0 manifest is validated;
unsupported protocol/version/encoding fails closed. Each v4 operation checks
the current manifest against its original binding rather than silently
switching versions. Explicit `create_workspace` is the sole empty-project
exception: it establishes the declaration and the instance binding together.

The class descriptor returns the original native bound function on legacy
instances. Class-style calls also traverse the same boundary; they cannot
bypass it into an old mutator. Unsupported public methods fail closed on v4.
The existing 38 Project method signatures and all existing properties,
dataclasses, exports and exception names are preserved. The public-surface
snapshot change is purely additive; its old entries were compared structurally
before updating. Existing method bodies are not copied or rewritten.

Malformed legacy manifests retain the old read-only construction,
`is_initialized` and `config` behavior. Writes against an unclassifiable
manifest are refused. A legacy/overridden workspace directory cannot be
silently converted by calling `create_workspace`. No source workspace,
dogfood, or deployed rule file was changed to exercise this behavior.

The trusted Profile mapping is copied and wrapped read-only at Project
construction. No evaluator runs in this package. Business requests reject
judging fields/callables; no setter or runtime registration API is exposed.
An approval-shaped REVIEW is an appended claim, never an authorization decision.

## Authority, durability and failure evidence

| Artifact | Meaning | Not its meaning |
|---|---|---|
| `fcop/fcop.json` | Workspace identity/declaration | Global uniqueness registry |
| Lifecycle TASK path | Authoritative current position | Cached status or event replay |
| `transitions[0]` | One T1 historical event | Second current-state field |
| REPORT / ISSUE / REVIEW | Append-only facts | In-place correction or implicit authorization |
| `operations/create-<key-hash>.json` | Durable immutable creation result/digests | Second lifecycle state machine |
| `operations/create-<key-hash>.lock` | Retained inode for a short kernel lock | Permanent owner lease, scheduler, or age-based stale record |
| `.fcop-create-*.tmp` | Incomplete publication evidence | Successful operation fact |

The operation key hashes workspace_id/kind/operation_id, separate from the
canonical request digest. The request digest follows F4.8.4 including NFC,
newline/body normalization, default priority, null optional relations and
sorted/deduplicated references. Timestamps, allocated identities and Profile
thread/risk extensions are excluded. The result TASK repeats the public key
fields and request digest. The operation fact stores the original result and
content digest, not a Runtime counter or mutable NOW field.

Planning and validation precede writes. A per-key OS lock linearizes the
commit; a fresh Project/process reads the durable fact, not memory. Existing
returns the same result without new bytes. A conflict never calls publication.
Corrupt/copied facts, an orphan authoritative TASK, or changed result bytes
fail closed and preserve evidence. This is creation-failure detection, not
automatic repair or the five-state lifecycle recovery implementation.

Publication writes a same-directory temporary, flushes and fsyncs it, then
uses no-overwrite publication. Windows uses MoveFileExW WRITE_THROUGH without
REPLACE_EXISTING. POSIX uses hard-link publication, directory fsync, then
removes only its own successful temporary. A failure leaves the temporary
and existing destination intact. Kernel locks release on process exit;
timeouts return LOCK_RECOVERY_REQUIRED and never delete a lock by age.

Paths reject traversal, absolute envelope paths, symlinks and Windows reparse
points. The layout must be present and on one device. Local NTFS and supported
local POSIX filesystem checks fail closed for unknown/network capabilities.
The macOS probe follows Apple's [public statfs ABI](https://github.com/apple-oss-distributions/xnu/blob/main/bsd/sys/mount.h).
These checks are not cryptographic protection against an external actor
rewriting files or racing directory permissions; OS/deployment control remains
outside Core. Native Windows is verified; Linux/macOS code is type-checked,
but no native POSIX execution is claimed in this receipt.

## Deliberate non-implementation

- T2–T7 return a namespaced unavailable error; illegal edges return
  INVALID_TRANSITION. Legacy finish/history mutation is rejected on v4.
- Strong/weak relationships are parsed and statically checked. No dynamic
  Branch admission, family lock, REPORT-head selection or family digest exists.
- `write_review` can store a convergence-shaped fact but does not certify its
  digest or authorize archive. T7 never executes in WP3A.
- Derivation creates a new empty workspace with adopted Profile identifiers
  and a new identity. It does not copy/rewrite historical envelopes, perform
  a migration, copy Runtime policy or claim invisible-clone detection.
- No migration receipt/recovery engine, fault injection API, cold export,
  MCP routing, role policy or release work is implemented.

## Later integration, without changing this package's contract

After ADMIN accepts WP3A and separately authorizes WP3B, the private handler
table can route T2/T3 into lifecycle-specific functions. No new public Runtime
or replacement Project is needed. New migration evidence must distinguish a
legitimate changed TASK from corruption before creation-result verification
can accept post-transition bytes; creation operation facts remain immutable.
WP3D, not this package, must add the family linearization/evidence semantics.
Incidental green tests are detailed in the result report and confer no later
stage completion or Gate.
