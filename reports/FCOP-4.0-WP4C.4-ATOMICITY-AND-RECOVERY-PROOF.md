# WP4C.4 atomicity and explicit recovery proof

Status: local implementation and verification complete; see RESULT for final native runs and remaining limitations. No claim of multi-file atomicity, Host consumption or power-loss certification is made.

Authority: fixed taskbook 01c53355293c08f100b9f6e5aba0caea015d27cd, sections 8–13; frozen RD-09/10/16. Implementation: src/fcop/v4/rule_distribution/_deployment.py, _files.py, _receipts.py and _projection.py.

## Reused primitives and scope

Reuse Core encoding.canonical, safe_path, operation_lock, publish, sync_directory, supported_local and remove_authoritative without modifying them. No lifecycle/Authorization handler is invoked. The private _move performs same-directory single-file publication/replacement: Windows MoveFileExW WRITE_THROUGH (with REPLACE_EXISTING only for a verified existing target), POSIX replace or no-replace hard-link publication plus directory sync. Private staging is O_EXCL, explicit bytes, flush/fsync and byte comparison. Windows private extended-length I/O paths do not appear in logical targets, output bytes or receipt paths.

Coordination is the workspace-local distribution commit.lock, not a database, adoption registry, service, family lock or second Runtime. Cooperating apply/rollback callers serialize their validation and commit. Uncooperative external writers are checked immediately before replacement and after publication; no portable path API promises a filesystem-wide compare-and-swap against arbitrary hostile writers. The implementation rejects detected drift rather than guessing ownership.

The apply caller uses an explicit bounded 45-second acquisition wait; the reused Core primitive and its default are unchanged. A native two-process diagnostic showed that its default 15-second wait could expire while the other writer was genuinely completing file flushes. Waiting for that writer preserves the real winner/ownership-conflict result. Apply classifies pending intents only with the lock held, not while another writer may still be publishing them. The critical region contains bounded synchronous file work only, not Agent/model work, networking or background retries; this is not a hard real-time latency guarantee.

## Linearization and crash states

| Boundary / window | Durable authority and visible targets | Explicit handling |
| --- | --- | --- |
| plan / validation rejection | no new files, dirs or locks | return a structured rejection; no replay |
| adopt publication | one canonical content-addressed adoption receipt | same-byte retry returns same identity; no Host effect |
| before target staging | immutable attempt intent, possibly validated snapshots; before targets | inspect sees no changed target; explicit recovery may record unchanged restoration |
| before_stage_durable | intent plus possibly non-durable exclusive staging; target remains before | no success receipt; explicit inspect/rollback_partial |
| durable staged bytes, before backup | intent plus fsynced verified staging; before target | missing backup is allowed only while target is still provably before |
| backup durable, before target replacement | intent, verified old-byte backup, before target | check current before again; no inferred success |
| after one target replacement | its target matches recorded after, others remain before | proven_writes lists only observed changed identities |
| between_replacements | bounded two-target input has partial visible state | no global atomic claim; explicit restoration only |
| before_success_receipt | all target bytes verified, immutable evidence remains, no deployment success | existing intent blocks an unrelated new apply; inspect or explicit restore |
| success receipt published, response lost | verified receipt and after targets | same selection/time/preconditions/full supplied plan returns same receipt; no duplicate success |
| rollback after restoration, before success receipt | same attempt format records original deployed bytes as backup and desired restoration | inspect plus rollback_partial can restore the pre-rollback deployed bytes |
| partial recovery interrupted | original immutable intent/backups plus some restored before targets | re-inspect accepts only recorded before/after; explicit retry restores remaining changed targets |
| recovered fact published | original intent and append-only completion fact retained | no fabricated Deployment Receipt and no background work |

Deployment success linearizes at the immutable receipt publication after all requested target replacements have been verified. Each physical target replacement has its own filesystem linearization point. These are different claims. Intent publication is neither successful adoption of a new runtime nor a work queue. Plan has no linearization write.

`apply` and normal `rollback` share _commit_targets. Every replacing target follows same-directory stage → flush/fsync → verify staging → durable verified old backup → compare before → single-file atomic move → verify target. Deletion is limited to proven absent-before restoration and reuses the durable source-name removal primitive. All semantic validation, rollback timestamps, identity/chain/backup checks and planned receipt values precede target effects.

Normal rollback is restricted to the unique immediate deployment tail. It restores exact backup bytes and appends a new adoption/deployment pair referencing the previous facts. It does not select an arbitrary package label or rewrite history. Same rollback request after a lost response returns its existing rollback identity instead of toggling state. Full target drift, missing/tampered backup, broken history and arbitrary version selection are zero-further-write failures.

## Structured failure evidence

The private attempt carries schema, workspace identity, bounded known target set, before/after/managed digests, backup refs, same-directory staging identities, planned success refs, full plan digests and a private uniqueness nonce. The nonce does not enter plan or projected bytes. Immutable failure filename hashes cover full raw JSON bytes.

Successful attempts remain immutable evidence, not pending automatic jobs. Explicit inspection distinguishes changed targets from unchanged originals; it never claims staging or snapshot files are committed Host targets. A changed target requires the recorded verified backup where it previously existed. External drift that prevents proof fails closed. Safe exception details preserve failure_ref/proven_writes/requires_explicit_recovery, without source bodies or credentials. Partial restoration changes only the failure's proven paths and appends a completion fact; old failure/success/adoption evidence is not edited.

## Verification obligations

Frozen DIST-19 uses two real overlapping processes with the same absent-target precondition: at most one distinct success receipt, with the loser rejected for ownership or both returning the exact same identity. DIST-20 executes all three named physical windows through the production entry and explicitly inspects/restores the partial state.

Independent test_v4_rule_distribution_host.py supplements those tests with native junction rejection, complete-plan retry tampering, per-input plan drift, strict Profile bytes, invalid rollback times before effects, user-region restoration, owned-target failures, a real spawned process that exits immediately after actual replacement, and storage failure during rollback receipt publication. It never patches a successful result or supplies an evaluator to bypass a boundary. Test outcomes, failures during development and final commands are retained in RESULT.

Windows is the only native platform verified in this local execution. POSIX branches are reviewed/type-checked but Linux/macOS remain NOT_NATIVE_VERIFIED unless actual final GitHub runners execute them. Flush/write-through primitives do not warrant disk hardware, controller caches, sudden power-loss survival, adversarial external mutation or atomic replacement of a group of files.
