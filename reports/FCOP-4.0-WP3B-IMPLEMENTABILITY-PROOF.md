# FCoP 4.0 WP3B Implementability Proof

Status: **PASS**

Scope: WP3B T2/T3 only

Input: `d2d2e9518451d58d165e3705f13f1ceb24388571`

Frozen contract: `aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6`

## 1. Decision

The frozen F4.9.1–F4.9.10 five-state table covers every reachable physical
window of the proposed T2/T3 transaction. Coverage does not mean that every
window is mechanically completed: observations that cannot prove the required
ordering are uniquely classified as `INDETERMINATE`, return
`RECOVERY_REQUIRED`, and preserve all visible bytes.

The existing create operation lock can be nested under one deterministic
Root-family lock. Branch create, T2/T3, and current-attempt REPORT writes can
therefore share the boundary required by F4.9.5 without a second public facade,
global lock, lease, scheduler, or lock-age deletion.

## 2. Concrete transaction

Under one family lock the implementation performs these physical operations:

1. Open the retained family lock inode and acquire the kernel exclusive lock.
2. Re-read all authoritative TASK paths and all T2/T3 receipts relevant to the
   TASK/edge; validate receipt uniqueness and identity.
3. Parse and validate the source TASK and, for T3, recompute the current attempt
   and unique REPORT head from disk.
4. Build the exact target bytes by appending one event while preserving the
   TASK body and all non-transition fields; calculate source/target/evidence and
   normalized-transition SHA-256 values.
5. Write and fsync a same-directory temporary receipt, publish the canonical
   `PREPARED` receipt without replacement, and persist its directory entry.
6. Write and fsync a same-directory TASK temporary, publish the target with a
   kernel no-replace primitive, and persist the target directory entry.
7. Write and fsync a receipt-update temporary, atomically replace only the
   canonical receipt with `TARGET_DURABLE`, and persist the receipt directory.
8. Remove the authoritative source and persist its directory entry. POSIX uses
   `unlink` plus directory `fsync`; Windows first performs a write-through,
   no-replace rename to a non-authoritative tombstone before best-effort tombstone
   unlink, so the authoritative source-name removal has a durable boundary.
9. Atomically replace the receipt with `COMMITTED` and persist the receipt
   directory.
10. Return the committed path, attempt and receipt reference, then release the
    kernel lock. Lock files are retained and are never deleted by age.

Receipt stage replacement is a dedicated primitive. The existing no-overwrite
TASK publication primitive is not weakened.

## 3. Crash-window mapping

The table maps the ten boundaries before return. “Expected source” means its
bytes hash to `source_digest`; “expected target” means its different, planned
bytes hash to `target_digest`. A same transaction therefore does not require old
and new TASK bytes to be identical.

| Exit after | Observable durable facts | Frozen classification | Permitted action |
|---|---|---|---|
| 1 lock acquired | expected source only; no receipt/target | `NOT_COMMITTED` | Release-on-process-death; preserve source; a later call may plan anew. |
| 2 re-read | same as observed before validation | Determined by the existing fact combination | No write before full validation. |
| 3 validation | expected source only; no receipt/target | `NOT_COMMITTED` | Preserve source; retry may plan anew. |
| 4 target bytes computed in memory | expected source only; no receipt/target | `NOT_COMMITTED` | Memory is not evidence; preserve source. |
| 5 `PREPARED` durable | expected source, target absent, matching `PREPARED` receipt | `NOT_COMMITTED` | Reconstruct exact target from receipt event, verify its digest, and resume; abandoning is also safe. |
| 6 target durable | expected old source and expected new target, receipt still `PREPARED` | `INDETERMINATE` | Return `RECOVERY_REQUIRED`; preserve source, target, receipt and any temporary. The frozen mechanical-duplicate row requires `TARGET_DURABLE`. |
| 7 `TARGET_DURABLE` durable | expected old source and expected new target, matching receipt | `RECOVERABLE_DUPLICATE` | Verify both planned digests, remove source durably, then complete receipt. |
| 8 source removed durably | source absent, expected target, `TARGET_DURABLE` receipt | `COMMITTED` | Complete the receipt only; never republish target or append another event. |
| 9 `COMMITTED` durable | source absent, expected target, matching receipt | `COMMITTED` | Return result; do not repeat migration. |
| 10 response boundary | same as after 9 | `COMMITTED` | A response loss is recovered from the internal receipt, without claiming arbitrary-time public T2/T3 replay idempotency. |

Sub-step failures are covered as follows:

- A receipt/TASK temporary written but not published is non-authoritative
  evidence. It is retained. Canonical source/target/receipt facts still decide
  the state; a conflicting or unparsable canonical receipt is
  `INDETERMINATE`.
- If a receipt replacement has become visible but its directory persistence is
  uncertain, restart observes either the old or new complete receipt; atomic
  replacement never accepts partial JSON. The corresponding row is then
  selected from actual source/target bytes.
- A `TARGET_DURABLE` receipt with no target is impossible under the intended
  program order but remains physically observable after external corruption or
  unsupported storage behavior. It is `INDETERMINATE`, never success.
- A source deleted while the receipt is still `PREPARED` is likewise
  `INDETERMINATE`. Only `TARGET_DURABLE` or `COMMITTED` plus the exact target
  digest proves `COMMITTED` in the frozen table.
- Both absent is `INDETERMINATE`.
- Both present with `source_digest`/`target_digest` matching the planned old/new
  bytes is `RECOVERABLE_DUPLICATE` only when the canonical receipt is
  `TARGET_DURABLE`. Any other byte combination is `DIVERGENT_DUPLICATE`.
- A damaged receipt, multiple canonical JSON records claiming the same internal
  identity, a filename/identity mismatch, path escape, wrong workspace/TASK/
  edge, unsupported stage, or digest conflict is `INDETERMINATE`. No mtime,
  directory order, event replay, or “last JSON key wins” fallback is used.

The mapping has **10/10 physical boundaries covered**. The only mechanical
writes during recovery are: resume a matching `NOT_COMMITTED` receipt, finish a
matching `RECOVERABLE_DUPLICATE`, or complete a receipt for a proven
`COMMITTED` observation. Divergent and indeterminate observations preserve all
visible evidence and fail closed.

## 4. Shared linearization proof

The lock identity is a SHA-256 of canonical UTF-8 JSON containing the contract,
`workspace_id`, and `root_task_id`. It is stable across processes and project
relocation because no absolute path enters the key.

| Operation | Root-family identity chosen before locking | Required post-lock re-read |
|---|---|---|
| Standalone/potential Root T2/T3 | its own TASK ID | unique path, relation, stage, attempt, receipt; T3 also REPORT head/digest |
| Branch T2/T3 | its `branch_of` Root ID | Branch path/relation/stage/attempt plus receipt and REPORT head |
| `create_task(branch_of=ROOT)` | supplied Root ID | Root uniquely exists, is `active`, and has no `branch_of` |
| REPORT final/replacement | subject TASK's own ID or its `branch_of` Root ID | subject path/relation/stage/current attempt and current REPORT head |

Pre-lock reads only choose a lock. They never authorize a commit. After lock
acquisition, each writer re-resolves its relevant facts. If pre-lock and
post-lock family identity differ, the operation fails closed.

The only nested lock is Branch creation:

```text
family lock(ROOT) -> create operation lock(workspace_id, create_task, operation_id)
```

No code path acquires a family lock while holding a create-operation lock. T2,
T3, and REPORT writes hold one family lock only. Consequently there is no lock
cycle. Different standalone TASK IDs derive different locks, so unrelated work
is not globally serialized. Locks cover only disk re-read, validation and file
commit; no Agent work occurs inside them. Kernel locks release on process exit,
while the zero-byte lock inode remains and is never age-deleted.

Result: **LINEARIZATION_BOUNDARY_NOT_SHARED is not present**.

## 5. Evidence sources

- Frozen clauses: `spec/fcop-4.0-spec.md` F4.4–F4.9 at the fixed contract
  ancestor.
- Current primitives and routing: `src/fcop/v4/encoding.py`,
  `src/fcop/v4/creation.py`, and `src/fcop/v4/boundary.py` at the input HEAD.
- Windows no-replace/write-through move contract:
  <https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-movefileexw>.
- POSIX/Linux file and directory persistence:
  <https://man7.org/linux/man-pages/man2/fsync.2.html>.
