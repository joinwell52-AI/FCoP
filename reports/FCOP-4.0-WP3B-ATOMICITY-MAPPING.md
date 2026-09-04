# FCoP 4.0 WP3B Atomicity and Branch-Race Mapping

Status: **PASS**

Physical crash boundaries: **10/10 mapped**

Shared linearization boundary: **PASS**

## 1. Durable transaction map

| Boundary | Durable observation after restart | Classification | Production behavior | Test evidence |
|---|---|---|---|---|
| Before family lock | source is unchanged | `NOT_COMMITTED` | No protocol write | invalid-edge zero-write tests |
| After lock/re-read | pre-existing facts only | Existing fact classification | Validation only | head/relation rejection tests |
| After validation | source only | `NOT_COMMITTED` | May abandon | `test_failure_before_prepared_keeps_source` |
| After target calculation | source only; target exists only in memory | `NOT_COMMITTED` | May abandon | same pre-PREPARED injection |
| After durable PREPARED | source matches `source_digest`; target absent | `NOT_COMMITTED` | Rebuild exact target from stored event and resume after digest/head verification | `test_prepared_source_only_resumes_exact_transaction` |
| After no-overwrite target publish | old source and planned new target; receipt PREPARED | `INDETERMINATE` | `RECOVERY_REQUIRED`; preserve all | `test_failure_after_target_publish_preserves_indeterminate_evidence`, `test_target_visible_with_prepared_receipt_is_indeterminate` |
| After durable TARGET_DURABLE | old source and planned new target match their distinct receipt digests | `RECOVERABLE_DUPLICATE` | Remove source durably; update receipt only | `test_target_durable_duplicate_mechanically_converges` |
| After source removal | source absent; target matches; receipt TARGET_DURABLE | `COMMITTED` | Update receipt to COMMITTED; never append another event | `test_source_absent_target_durable_completes_receipt`, `test_response_loss_after_source_delete_does_not_repeat_event` |
| After durable COMMITTED | source absent; target and receipt match | `COMMITTED` | Return committed result | normal T2/T3 and two-process T2 tests |
| After return / response loss | same committed facts | `COMMITTED` | Read internal receipt; never duplicate TASK/event | response-loss and two-process tests |

Additional hostile observations are closed as follows:

| Observation | Classification/result | Byte preservation evidence |
|---|---|---|
| `TARGET_DURABLE` receipt but target absent | `INDETERMINATE` → `RECOVERY_REQUIRED` | `test_target_durable_without_target_is_indeterminate` |
| Both old/new paths present but either digest differs | `DIVERGENT_DUPLICATE` → `RECOVERY_REQUIRED` | `test_different_digest_duplicate_preserves_every_copy` |
| Both absent | `INDETERMINATE` → `RECOVERY_REQUIRED` | classifier branch plus proof table |
| Invalid JSON, path escape, duplicate/filename identity conflict | `INDETERMINATE` → `RECOVERY_REQUIRED` | three `test_receipt_damage_fails_closed_and_preserves_bytes` cases |
| No receipt and a different target already exists | `TARGET_ALREADY_EXISTS_DIFFERENT` | frozen `C8-R01` and local target-conflict test |
| Two authoritative paths without a provable receipt | `STATE_AMBIGUOUS`, except the explicit different-target collision above | `test_inspect_state_uses_path_now_and_rejects_ambiguity` |

`source_digest` hashes the complete pre-event TASK bytes and `target_digest`
hashes the complete post-event TASK bytes. These values intentionally differ.
The receipt uses both values to distinguish the planned old/new duplicate from
actual divergence; it never compares old and new TASKs as if they should be
byte-identical.

## 2. Physical primitives

- Initial receipt and TASK destination publication call the existing
  no-overwrite `publish()` primitive: fsync a same-directory temporary, then
  kernel no-replace publication and directory persistence.
- Receipt phase changes call the new private `replace_durable()` primitive.
  No business-envelope caller can use replacement through the public facade.
- POSIX authoritative-source removal is `unlink()` followed by directory
  `fsync()`.
- Windows authoritative-source removal first performs a same-directory,
  no-replace `MoveFileExW(..., MOVEFILE_WRITE_THROUGH)` into a filename that
  cannot match `TASK-*.md`. This durably removes the authoritative source name;
  best-effort deletion of the tombstone cannot change NOW. A failed delete
  leaves evidence, not a TASK.
- Replacement or publication temporaries are never selected as NOW and are not
  deleted by age.

## 3. Receipt integrity

The private receipt validator requires an exact contract/version and complete
field set; canonical UUID identities; canonical relative POSIX source/target
paths; the exact WP3B edge/tool; aligned evidence arrays; a timezone-aware event;
event/receipt identity agreement; a recomputed normalized request digest; and a
filename derived from the internal operation UUID. Invalid or conflicting facts
never fall back to event order, mtime, filenames, natural-language body, or the
last duplicate JSON key.

Receipts are stored under `fcop/operations/` but are neither envelopes nor NOW.
They contain no drive letter or absolute project path, and the relocation test
reopens and recovers the same fact after the entire project directory moves.

## 4. Family linearization map

| Race surface | Lock identity | Post-lock validation | Observed legal outcomes |
|---|---|---|---|
| Root/standalone T2/T3 | workspace ID + own TASK ID | path, relation, receipt, attempt, head/evidence | one edge/event or stable rejection |
| Branch T2/T3 | workspace ID + `branch_of` Root ID | Branch relation/path plus transition facts | serialized with Root-family changes |
| Branch create vs Root T3 | workspace ID + supplied Root ID | Root unique, active, not a Branch before nested create-op lock | Branch first: sibling exists and Root may then submit; T3 first: Branch gets `ROOT_NOT_ACTIVE` |
| REPORT replacement vs T3 | subject's Root-family identity | current attempt and current REPORT head | replacement first: T3 binds replacement; T3 first: current-attempt replacement is rejected |

The family lock is a retained kernel-lock file in the OS temporary lock area,
named by the complete SHA-256 family key. It is coordination only, not a project
fact or authoritative store; this also keeps zero-write rejections and receipt
counts truthful. It is never removed by age. Every operation holds at most one
family lock. Branch create alone nests its prior create-operation lock in the
fixed order `family -> create operation`. No inverse path exists.

True spawned-process evidence:

- concurrent same-request T2 returns the one internal committed result twice,
  with one TASK, one event, one attempt and one receipt;
- Branch create/Root T3 yields exactly one of the two serialized branch outcomes;
- REPORT replacement/T3 yields an evidence digest for the one head that won the
  linearization order;
- holding TASK A's family lock does not delay TASK B's T2, proving there is no
  unrelated global serialization.

## 5. Scope conclusion

The mapping implements private T2/T3 recovery only. It does not expose
`recover_operation`, `inject_fault`, public operation IDs for T2/T3, repair
REVIEWs, authorization retry, T4–T7 recovery, family digest, convergence, a
background worker, or another Runtime.
