# WP4C.4 pre-code implementability proof

## Fixed task and role separation

Executor: ME, solo. ADMIN's fixed taskbook is the decision carrier; this file records execution preflight and review before any production edit. No dogfood TASK/archive or deployed Host file is changed.

Taskbook: 01c53355293c08f100b9f6e5aba0caea015d27cd; raw SHA-256 c8d91d0c0d24804f8b06bb3dde9d07f14febc1d75411778fd74f6272398b0d78; 18707 bytes, strict UTF-8/no BOM/LF. GitHub raw bytes, fetched Git Blob and direct parent e24b16185dcd9b8746c26d08654c6ed285a2a8c7 were checked before creating D:/FCoP-wp4c4-host-projection, branch review/fcop-4.0-wp4c.4-host-projection. Initial checkout CLEAN. Parent Gate accepts implementation 4f56cfcf9754bb509b7bd353e830a8e4003810ea.

Authority: [fixed taskbook](https://github.com/joinwell52-AI/FCoP/blob/01c53355293c08f100b9f6e5aba0caea015d27cd/taskbooks/fcop-4.0/WP4C.4/01-Host-Projection-Adoption-Deployment-and-Rollback-Taskbook-v1.0.zh.md), [Gate](https://github.com/joinwell52-AI/FCoP/blob/e24b16185dcd9b8746c26d08654c6ed285a2a8c7/reviews/fcop-4.0/gates/WP4C-3-RULE-PACKAGE-ACCEPTED.md), [ADMIN receipt](https://github.com/joinwell52-AI/FCoP/pull/24#issuecomment-5577821094).

Read both RD contract languages, integral decision schedule/matrix, complete conftest/driver and both target test files, five accepted WP4C.3 reports and Manifest, private loader/selector/dispatch/table/error implementation, boundary and handler wiring, v4 Encoding/linearization and legacy lifecycle atomic primitives. Historical report statements are evidence, not current authorization.

## Actual baseline, not implementation acceptance

Native Windows / Python 3.12.9. Standard python -B -m pytest, -q -p no:cacheprovider --tb=line; source-root PYTHONPATH and PYTHONDONTWRITEBYTECODE=1. Exact file::function selection for test_dist_08 through test_dist_12 in test_dist_07_12_profiles.py, plus all test_dist_13_20_projection.py. Result: **45 failed, 8 passed, 3 warnings, 130.93 seconds**, exit 1. No skips or xfails. JUnit: C:/Users/Administrator/AppData/Local/Temp/fcop-wp4c4-target-baseline.xml; raw SHA-256 f042ba79dc905d9d02c9a67ca51c60c9058a74bc7f19badf40e553dcdc61c54c.

Every row below is an actual collected node. PASS_NEGATIVE means only an existing rejection, not a later positive capability. RED is expected missing WP4C.4 behavior on the accepted WP4C.3 implementation.

| Frozen node | Baseline | Contract | Required action | Observable obligation |
| --- | --- | --- | --- | --- |
| test_dist_08[valid] | RED | RD-09 | adopt/status | receipt identity; no migration or implicit adoption |
| test_dist_08[file-without-adoption] | RED | RD-09 | adopt/status | receipt identity; no migration or implicit adoption |
| test_dist_08[wrong-workspace] | RED | RD-09 | adopt/status | receipt identity; no migration or implicit adoption |
| test_dist_08[v3] | RED | RD-09 | adopt/status | receipt identity; no migration or implicit adoption |
| test_dist_08[broken-previous] | RED | RD-09 | adopt/status | receipt identity; no migration or implicit adoption |
| test_dist_08[actor-only] | RED | RD-09 | adopt/status | receipt identity; no migration or implicit adoption |
| test_dist_09[success] | RED | RD-10 | verify_deployment | raw receipt and full target identity |
| test_dist_09[before-drift] | RED | RD-10 | verify_deployment | raw receipt and full target identity |
| test_dist_09[receipt-tamper] | RED | RD-10 | verify_deployment | raw receipt and full target identity |
| test_dist_10[success] | RED | RD-10 | rollback | immediate verified history; exact bytes or zero-write rejection |
| test_dist_10[missing-backup] | RED | RD-10 | rollback | immediate verified history; exact bytes or zero-write rejection |
| test_dist_10[modified-backup] | RED | RD-10 | rollback | immediate verified history; exact bytes or zero-write rejection |
| test_dist_10[modified-target] | RED | RD-10 | rollback | immediate verified history; exact bytes or zero-write rejection |
| test_dist_10[arbitrary-version] | RED | RD-10 | rollback | immediate verified history; exact bytes or zero-write rejection |
| test_dist_11[codex] | RED | RD-11/12 | inspect_profile | known pinned static profile; no evaluator/probe |
| test_dist_11[cursor] | RED | RD-11/12 | inspect_profile | known pinned static profile; no evaluator/probe |
| test_dist_11[claude-code] | RED | RD-11/12 | inspect_profile | known pinned static profile; no evaluator/probe |
| test_dist_11[unknown-host] | PASS_NEGATIVE | RD-11/12 | inspect_profile | known pinned static profile; no evaluator/probe |
| test_dist_11[unknown-profile] | PASS_NEGATIVE | RD-11/12 | inspect_profile | known pinned static profile; no evaluator/probe |
| test_dist_11[evaluator] | PASS_NEGATIVE | RD-11/12 | inspect_profile | known pinned static profile; no evaluator/probe |
| test_dist_11[model-probe] | PASS_NEGATIVE | RD-11/12 | inspect_profile | known pinned static profile; no evaluator/probe |
| test_dist_11[duplicate-key] | PASS_NEGATIVE | RD-11/12 | inspect_profile | known pinned static profile; no evaluator/probe |
| test_dist_12[support-only] | RED | RD-11 | status | four independent facts; consumption unknown |
| test_dist_12[adoption-only] | RED | RD-11 | status | four independent facts; consumption unknown |
| test_dist_12[generated] | RED | RD-11 | status | four independent facts; consumption unknown |
| test_dist_12[consumption-only] | RED | RD-11 | status | four independent facts; consumption unknown |
| test_dist_13[False-codex] | RED | RD-12/13 | apply | exact selected target; preserve unowned entries |
| test_dist_13[False-cursor] | RED | RD-12/13 | apply | exact selected target; preserve unowned entries |
| test_dist_13[False-claude-code] | RED | RD-12/13 | apply | exact selected target; preserve unowned entries |
| test_dist_13[True-codex] | RED | RD-12/13 | apply | exact selected target; preserve unowned entries |
| test_dist_13[True-cursor] | RED | RD-12/13 | apply | exact selected target; preserve unowned entries |
| test_dist_13[True-claude-code] | RED | RD-12/13 | apply | exact selected target; preserve unowned entries |
| test_dist_14 | RED | RD-13 | plan | relocation/time-independent bytes; zero writes |
| test_dist_15[preserve] | RED | RD-13 | plan/apply | owned block matches; outside bytes preserved; full byte cap |
| test_dist_15[nested] | RED | RD-13 | plan/apply | owned block matches; outside bytes preserved; full byte cap |
| test_dist_15[duplicate] | RED | RD-13 | plan/apply | owned block matches; outside bytes preserved; full byte cap |
| test_dist_15[missing] | RED | RD-13 | plan/apply | owned block matches; outside bytes preserved; full byte cap |
| test_dist_15[oversized-user-region] | RED | RD-13 | plan/apply | owned block matches; outside bytes preserved; full byte cap |
| test_dist_16[reference] | RED | RD-14 | adopt/apply/verify_deployment | local support before adoption; immutable 19-file snapshot |
| test_dist_16[stale-snapshot] | RED | RD-14 | adopt/apply/verify_deployment | local support before adoption; immutable 19-file snapshot |
| test_dist_16[missing-snapshot] | RED | RD-14 | adopt/apply/verify_deployment | local support before adoption; immutable 19-file snapshot |
| test_dist_16[escaping-reference] | RED | RD-14 | adopt/apply/verify_deployment | local support before adoption; immutable 19-file snapshot |
| test_dist_17[exact] | RED | RD-15 | plan | exact raw framing; no fallback/truncation/unresolved link |
| test_dist_17[unadopted-multilingual] | PASS_NEGATIVE | RD-15 | plan | exact raw framing; no fallback/truncation/unresolved link |
| test_dist_17[overflow] | PASS_NEGATIVE | RD-15 | plan | exact raw framing; no fallback/truncation/unresolved link |
| test_dist_17[broken-source-link] | RED | RD-15 | plan | exact raw framing; no fallback/truncation/unresolved link |
| test_dist_18[False] | RED | RD-16 | plan | recursive zero writes; complete deterministic diff |
| test_dist_18[True] | PASS_NEGATIVE | RD-16 | plan | recursive zero writes; complete deterministic diff |
| test_dist_19[stale-plan] | RED | RD-16 | apply | fresh preconditions; real two-process single commit |
| test_dist_19[two-processes] | RED | RD-16 | apply | fresh preconditions; real two-process single commit |
| test_dist_20[before_stage_durable] | RED | RD-16 | apply/inspect_failure/rollback_partial | three physical windows; explicit verified recovery only |
| test_dist_20[between_replacements] | RED | RD-16 | apply/inspect_failure/rollback_partial | three physical windows; explicit verified recovery only |
| test_dist_20[before_success_receipt] | RED | RD-16 | apply/inspect_failure/rollback_partial | three physical windows; explicit verified recovery only |

## Planned single-responsibility implementation mapping

These are proposed private functions, not capabilities already delivered. Only the existing public facade remains. Existing validate/select/validate_operation_scope behavior stays unchanged.

| Action | Private owner | Reads | Permitted writes | Principal rejection |
| --- | --- | --- | --- | --- |
| inspect_profile | _projection.inspect_profile | explicit static profile | none | RULE_HOST_UNAVAILABLE |
| status | _receipts.status | profile and explicit verified adoption/deployment refs | none | corresponding identity error |
| adopt | _receipts.adopt | workspace, package, profile, ADMIN file, complete predecessor chain | immutable adoption receipt only | RULE_ADOPTION_REQUIRED; narrow taskbook 5.1 exception |
| plan | _projection.plan | package/profile/selection, history and current target | none, including no lock/temp/directories | RULE_OWNERSHIP_CONFLICT / RULE_PROJECTION_LIMIT / RULE_ARTIFACT_MISMATCH |
| apply | _deployment.apply | full fresh inputs and plan, adoption, current history | bounded package/profile snapshots, staging, backups, coordination, deployment/failure evidence and selected targets | fresh validation error, or RULE_DEPLOYMENT_RECOVERY_REQUIRED after effects |
| verify_deployment | _receipts.verify_deployment | full receipt chain, snapshots, target bytes | none | RULE_OWNERSHIP_CONFLICT / RULE_ARTIFACT_MISMATCH / RULE_DEPLOYMENT_RECOVERY_REQUIRED |
| rollback | _deployment.rollback | unique immediate predecessor, exact current target and verified backup | exact restored target, append rollback evidence | RULE_DEPLOYMENT_RECOVERY_REQUIRED |
| inspect_failure | _deployment.inspect_failure | fixed durable failure/intent ref and physical observations | none | RULE_DEPLOYMENT_RECOVERY_REQUIRED |
| rollback_partial | _deployment.rollback_partial | failure proof, before/after/backup identities | only proven target restoration and append recovery evidence | RULE_DEPLOYMENT_RECOVERY_REQUIRED |

## Reuse audit and linearization design

- Reuse v4.encoding.canonical for deterministic JSON plus one final LF; strict distribution parse for received raw JSON. Reject before serialization rather than map arbitrary Core errors globally.
- Reuse safe_path plus distribution-specific POSIX/device/control validation, checking all components including reparse points. Existing contained requires an existing source and is insufficient for a new target; do not relax the Core helper.
- Reuse operation_lock's retained inode/kernel lock, not an age-based lease. Distribution coordination must live inside its own internal namespace, never family_boundary's external temporary directory. Pure plan/status/verification never call it.
- Reuse publish for immutable byte-addressed evidence, no replacement of historical receipt names. Existing replace_durable is explicitly receipt-only and does not expose the required staged-hash/before-comparison boundary; do not repurpose it for Host targets or alter Core behavior.
- Host replacement needs a small distribution-local staged-file commit: same-directory exclusive temp, flush/fsync, hash verify, durable backup, short coordinated before comparison, atomic single-file rename/replace and target verification. Use native write-through rename on Windows and replace plus directory fsync on POSIX, matching the existing platform strategy without lifecycle coupling.
- Do not reuse legacy lifecycle.atomic.commit/create: they validate/mutate lifecycle and remove temporary evidence on errors. Do not reuse Core fault plans/operation receipts; distribution test_fault is its own fixed literal observation seam.
- Adoption publication is the single immutable receipt-name linearization point. Same canonical byte identity can be returned Existing; prior hashes and workspace bindings are validated, no registry.
- Commit serialization is short and local to overlapping distribution targets, not Agent work. Revalidate before any effects; revalidate before replacement under coordination. An absent-target contender cannot silently replace another result. Returning Existing requires exact complete success evidence, not merely equal target bytes.
- Durable prepared intent precedes target mutation and records before/after/backup identities. Each observed replacement and final success has immutable evidence. An unfinished intent blocks overlapping mutation until explicit inspection/recovery; no startup replay.
- Rollback validates the entire immediate chain/current bytes/backups before its first mutation. A retained proof records each restoration; partial or unprovable states preserve evidence. No arbitrary package label, mtime ordering, stale-lock deletion or inferred history.

## Materialization windows and recoverable observations

| Window | Observable durable fact | Allowed interpretation / recovery |
| --- | --- | --- |
| Before validation | no new file | rejection; zero writes |
| After validation, before target staging | adoption/intent/coordination may exist; targets original | preserve internal evidence; do not claim target writes |
| Stage created, not durable | possible partial temp, original target | before_stage_durable reports only proven files, preserves temp; explicit recovery never deletes user bytes |
| Stage durable, before backup | verified proposed bytes, original target | no target commit; preserve evidence |
| Backup durable, before replacement | complete original snapshot and intent | safe original target; no success receipt |
| Replacement completed, observation not yet appended | intent plus target after-hash; lock released on process exit | inspect exact bytes against intent; ambiguity rejects, never assume missing receipt means no write |
| Between replacements | subset of targets matches after, others before | enumerate proven writes; no all-or-nothing claim; explicit rollback only |
| All targets replaced, before success receipt | all after identities and pending intent | before_success_receipt returns recovery-required, no success receipt |
| Success durable, response lost | full immutable receipt and exact current bytes | exact retry returns same result; no new success history |
| During explicit rollback | predecessor backup plus restoration proof | verify current before/after per target; retry only proven steps, preserve uncertainty |

The three test seams are controlled exceptions, not proof of every possible power failure. Hardware durability guarantees remain bounded by supported local filesystem/kernel behavior. Windows native validation is required; Linux/macOS remain NOT_NATIVE_VERIFIED without actual native runners. No group atomicity or remote-filesystem guarantee.

## Interpretation review before coding

RD-13 distinguishes owned managed-region identity from user-owned outside bytes. Updates can preserve a new prefix/suffix when the old receipt proves the unchanged managed region. RD-10 explicit verification still compares the complete last-deployment target and reports full-file drift; it must not silently accept a newly edited suffix.

Reference support is validated before adoption, separately from runtime consumption. Adopt writes only its exact receipt fields; later use must validate the bound adopted profile identity and cannot accept caller evaluator code. Package/profile byte snapshots are an apply effect, never a plan/adopt side effect. Ordinary and reference output identity are reproducible across installation paths.

All rejection validation paths must stay zero-write. Failure after authorized effects must be explicitly distinguished, retain proof, and never be laundered as a reject-before-write. Unknown state cannot be repaired by a guessed write. Security/unit verification and a final semantic review remain mandatory; this pre-code design is not a PASS claim.

STATUS: PRE_CODE_REVIEW_COMPLETE_IMPLEMENTATION_UNVERIFIED
REQUESTED_GATE: NONE
WP4C_5_STARTED: false

## Post-implementation review (append-only conclusion)

The status immediately above records the original pre-code checkpoint; it is not overwritten. Final implementation uses the ownership map in HOST-PROJECTION-MAPPING, including _profiles.inspect_profile and _deployment.dispatch for status, rather than treating proposed function locations as binding new APIs.

Final native verification: all 53 target nodes pass, all 56 prior-stage nodes pass, full FCoP 1349/1349, Core 119/119 and MCP 134/134. The full distribution suite has 144 passes and 32 explicitly owned WP4C.5/6 failures, with zero unexpected failures. The 52 new Host units are included in FCoP, including real process exit after replacement, interrupted rollback, native junctions and evidence tampering. Exact commands, raw JUnit identities, all 32 future owners and retained intermediate failures are in RESULT.

Implementation review reconciled staging-before-backup ordering, normal rollback's durable attempt, exact retry versus legitimate user-region updates, and bounded two-process lock acquisition. The ATOMICITY-AND-RECOVERY-PROOF documents these actual paths and platform limits. No Core primitive, frozen Conformance, rule body, Schema, MCP, real Host entry or CodeFlowMu file changed. Local validation is complete; the Manifest and external PR receipt carry subsequent remote delivery evidence. ADMIN alone may sign the requested Gate; WP4C.5 remains unauthorized.
