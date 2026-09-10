# FCoP 4.0 Candidate Specification (English)

> **Status: Candidate · Not Implemented · Not Released**
>
> WP1.1 contract version: `4.0.0-candidate.2`; baseline `68dbeb15f4e7f84e1d03f907be9fa66c2265843e`; WP0 evidence `c259bebdad77122d24dc18a6dd3f8fe191e4042f`; WP1 input `1b50f9e1fd4d2d21002bb1b98e14fd903a050f07`. FCoP 3.2.5 remains the current protocol until ADMIN signs `FCOP_4_CONTRACT_FROZEN` and later implementation/release gates complete.

## 0. Normative language and authority

**F4.0.1** MUST/MUST NOT are conformance requirements; SHOULD/MAY are recommendations or optional capabilities.

**F4.0.2** English `spec/fcop-4.0-spec.md` is the primary authority for this candidate. The Chinese parallel `spec/fcop-4.0-spec.zh.md` MUST have the same clause IDs, objects, transitions, errors, and invariants. Any difference blocks freeze/release.

**F4.0.3** JSON Schema has machine authority only for structure it can express. This specification governs lifecycle, authorization, concurrency, and recovery behavior. WP2 tests may verify this specification but may not create rules.

## 1. Definition, layers, and Core

**F4.1.1** FCoP is a file-native agent behavior-governance protocol: files carry protocol, paths express current state, and events record transition history.

**F4.1.2** FCoP does not execute work and does not own LLM/tool invocation, hosts, sessions, schedulers, databases, UI, networking, or process management.

| Layer | Contract | Core |
|---|---|---:|
| Core | Semantics and invariants shared by every implementation | Yes |
| Specification | Core fields, states, errors, and observable behavior | Authoritative expression |
| Toolkit | Validation, query, migration, recovery, and convenience APIs | No |
| Profile | Roles, signing authority, organization, and product policy | No |
| Runtime | Host/model/session/scheduler/UI/DB/network/process | No |

**F4.1.3** Core contains only C1–C8: workspace identity, four envelopes, lifecycle, four relations, evidence and convergence, durable authorization, create idempotency, and recoverable atomic semantics.

**F4.1.4** Fixed roles, EVAL, a Ledger envelope, Git branch/merge, CodeFlowMu work surfaces, BCG, Relay, and online upgrade MUST NOT enter Core.

## 2. C1 · Workspace identity

**F4.2.1** The Core declaration of a 4.0 workspace is the UTF-8 JSON file `fcop/fcop.json`. It contains at least:

```json
{
  "protocol": "fcop",
  "protocol_version": "4.0",
  "workspace_id": "urn:uuid:00000000-0000-4000-8000-000000000000",
  "encoding": {"name": "fcop-filesystem", "version": "4.0"},
  "profiles": []
}
```

**F4.2.2** `workspace_id` MUST be a canonical lowercase UUID URN and remain stable after creation. Every envelope workspace_id MUST match it or return `WORKSPACE_ID_MISMATCH`.

**F4.2.3** `profiles` is a set of adopted Profile identifiers represented as a JSON array. Array order creates no authorization precedence or Core semantics. `profiles: []` is legal, but such a workspace can perform only Base operations that do not require authorization. v3 team, role, leader, and similar fields MAY remain Profile extensions and MUST NOT change Core semantics.

**F4.2.4** `workspace_id` is protocol identity, not a global online lock. A backup or read-only mirror MAY retain the ID. The producer of an explicit independent writable fork/derived workspace MUST generate a new ID before its first write. If the caller forces ID retention, that operation MUST reject with `WORKSPACE_ID_CLONE_CONFLICT` or explicitly create a read-only mirror. When one Toolkit, Runtime, or import operation simultaneously observes two independently writable workspaces with the same ID, it MAY return `WORKSPACE_ID_CLONE_CONFLICT` and Fail Closed.

**F4.2.5** Unsupported protocol, version, and Encoding return `UNSUPPORTED_PROTOCOL`, `UNSUPPORTED_WORKSPACE_VERSION`, and `UNSUPPORTED_ENCODING` respectively.

**F4.2.6** One offline workspace cannot prove that no invisible copy exists, and FCoP makes no such guarantee. External single-writer control, synchronized replication, and network conflict discovery are Runtime/deployment concerns outside Core.

## 3. C2 · Four formal envelopes

**F4.3.1** Formal business envelopes are exactly `TASK`, `REPORT`, `ISSUE`, and `REVIEW`. `shared/` is a knowledge surface. Operation receipts, locks, and indexes are Encoding/Toolkit facts, not a fifth envelope.

**F4.3.2** Every envelope uses UTF-8, LF, YAML frontmatter plus Markdown body and contains `protocol: fcop`, `version: 4`, `type`, its typed ID, `workspace_id`, `sender`, `recipient`, and timezone-aware `created_at`.

| Type | Additional required fields | Optional Core fields |
|---|---|---|
| TASK | `task_id`, `subject`, `transitions` | `parent`, `branch_of`, `references`, `operation_id`, `operation_kind`, `normalized_request_digest` |
| REPORT | `report_id`, `subject_ref`, `attempt_id`, `report_kind`, `result` | `references` |
| ISSUE | `issue_id`, `subject_ref`, `severity` | `references` |
| REVIEW | `review_id`, `review_kind`, `subject_ref`, `decision` | `attempt_id`, `family_digest`, `authorization_ref`, `references`, and §7 authorization fields |

**F4.3.3** REPORT, ISSUE, and REVIEW are append-only facts: once landed they MUST NOT be edited in place or deleted. Corrections, replacements, and revocations create a new envelope of the same type and reference affected facts through `references`.

**F4.3.4** A REPORT replacement chain uses `report_kind: final|replacement`. A replacement MUST reference the current head for the same subject/attempt. The valid REPORT is the unique head not referenced by a valid replacement. Zero heads returns `REPORT_REQUIRED`; multiple heads returns `REPORT_HEAD_AMBIGUOUS`.

**F4.3.5** REVIEW kinds include at least `assessment`, `acceptance`, `rejection`, `reopen`, `authorization`, `convergence`, and `repair`. If retained, `mark_human_approved` may only append a REVIEW and MUST NOT edit the old REVIEW.

## 4. C3 · Single authoritative path, lifecycle, and events

**F4.4.1** An authoritative TASK MUST exist in exactly one of these paths; directory location is the sole NOW truth:

```text
fcop/_lifecycle/{inbox,active,review,done,archive}/TASK-*.md
```

**F4.4.2** Base has exactly seven legal transitions and the following complete gate matrix:

| Transition | Precondition | Required REPORT | Required REVIEW | Required Authorization Profile | New attempt |
|---|---|---|---|---|---|
| T1 `None -> inbox` | TASK does not exist | No | No | No | No |
| T2 `inbox -> active` | Unique inbox TASK | No | No | No; a Profile may add policy | Yes |
| T3 `active -> review` | Unique active TASK | Unique valid REPORT for current attempt | No | No; a Profile may add policy | No |
| T4 `review -> done` | Unique review TASK | Current REPORT bound by T3 | Acceptance REVIEW | Yes | No |
| T5 `review -> active` | Unique review TASK | Rejected current REPORT | Rejection REVIEW | Yes | Yes |
| T6 `done -> active` | Unique done TASK | No | Reopen/authorization REVIEW | Yes | Yes |
| T7 `done -> archive` | Unique done TASK | No new REPORT; reuse accepted-attempt evidence | Archive authorization; convergence REVIEW also required when Branches exist | Yes | No |

**F4.4.3** One command may commit exactly one edge and append one transition. Multi-edge convenience calls MUST split the edges; failure at one edge MUST NOT fabricate later events.

**F4.4.4** `active -> done` is not in 4.0 Base. `finish_task` is 3.x Legacy; a 4.0 workspace MUST reject it with `LEGACY_TRANSITION_NOT_ALLOWED` and MUST NOT bypass T3/T4.

**F4.4.5** A transition contains `at/from/to/by/tool`; entry into active also contains a new `attempt_id`. For every REPORT or REVIEW consumed by a lifecycle gate, the transition stores aligned `evidence_ref` and `evidence_digest` arrays. When authorization applies, it also stores `authorization_ref` and `authorization_digest`. Each digest is lowercase SHA-256 of the complete file bytes after those bytes have been validated as UTF-8 with LF line endings. A later byte mismatch returns `EVIDENCE_DIGEST_MISMATCH`. Events are append-only and do not derive NOW.

**F4.4.6** Archive is terminal. An authoritative TASK MUST NOT move from archive to history or back into lifecycle. v3 history is read-only Legacy; a 4.0 Toolkit may only create non-authoritative cold-storage copies.

**F4.4.7** A state edge not listed in §4.2 returns `INVALID_TRANSITION`. For T7, ordinary closure means only: the TASK is in the unique done path, its strong relations are valid, and its authorization is valid. Base does not gate T7 on ordinary parent children or ISSUE state; a Profile MAY add those policies without creating a hidden Base transition.

## 5. C4 · Four relations

**F4.5.1** Core relations are exactly `parent`, `branch_of`, `subject_ref`, and `references`.

| Relation | Source→target | Strength | Meaning |
|---|---|---|---|
| parent | TASK→TASK | Strong | Delegation/hierarchy, not concurrent Branch |
| branch_of | TASK→Root TASK | Strong, at most one | Ordinary TASK is concurrent work for Root |
| subject_ref | REPORT/ISSUE/REVIEW→TASK or workspace | Strong, exactly one | Formal subject; workspace ISSUE uses `workspace:<workspace_id>` |
| references | Any envelope→existing envelope | Weak; mandatory when used by a gate | Citation, not ownership |

**F4.5.2** Missing, dangling, cross-workspace, cyclic, or non-unique strong relations return `RELATION_INVALID` and Fail Closed. An unresolved ordinary weak reference produces `REFERENCE_UNRESOLVED`; if used by a REPORT/REVIEW/authorization/convergence gate, the operation is rejected.

**F4.5.3** A Branch branch_of target has no branch_of of its own. A Branch cannot be a Branch Root. All Branches are siblings under one Root; violation returns `BRANCH_DEPTH_EXCEEDED`.

**F4.5.4** A Branch may be created only while its Root is unambiguous and active; otherwise return `ROOT_NOT_ACTIVE`. A done Root must first be reopened by authorized T6.

**F4.5.5** `thread_key` is Profile/Legacy and does not alter the four Core relations.

## 6. C5 · Attempt, REPORT, acceptance, and convergence

**F4.6.1** Every entry into active (T2/T5/T6) generates a non-reusable `attempt_id` formatted as `urn:uuid:<uuid>` in that transition. The current attempt is the ID on the last transition entering active.

**F4.6.2** T3 references the unique valid REPORT. Its subject_ref is the TASK and its attempt_id equals the current attempt. A prior-attempt REPORT never satisfies the new gate.

**F4.6.3** T4 references a REVIEW with `review_kind: acceptance` and `decision: approved`. Its subject_ref/attempt_id and referenced REPORT match current state, §7 authorization is satisfied, and the transition records the REPORT, REVIEW, authorization references, and byte digests required by §4.5.

**F4.6.4** Branch and ordinary TASK use the same lifecycle and evidence gates. There is no Branch-specific completion state.

**F4.6.5** If a Root has Branches, Root T7 executes within one family linearization boundary and verifies all of the following: Root is in the unique done path; Root has no `branch_of`; every Branch pointing to Root is in done or archive; every Branch current attempt has one valid REPORT; each Branch completion passed its own T3/T4 evidence and authorization gates; convergence references exactly those current Branch REPORTs; convergence `family_digest` equals the value recomputed at commit; and Root T7 authorization is bound to that current digest. Any non-terminal Branch returns `BRANCH_NOT_TERMINAL`. The convergence REVIEW shape is:

```yaml
review_kind: convergence
subject_ref: ROOT-TASK-ID
family_digest: <sha256-lower-hex>
references: [REPORT-ID-A, REPORT-ID-B]
```

**F4.6.6** For each Branch, `report_digest` is lowercase SHA-256 of the complete current valid REPORT file bytes after UTF-8/LF validation. `family_digest` is lowercase SHA-256 of this exact canonical object:

```json
{
  "contract": "fcop-family-v1",
  "root_task_id": "TASK-...",
  "branches": [
    {
      "branch_task_id": "TASK-...",
      "attempt_id": "urn:uuid:...",
      "report_id": "REPORT-...",
      "report_digest": "<lowercase-sha256>"
    }
  ]
}
```

Collect every TASK whose `branch_of` points to the Root; use each current attempt and unique valid REPORT head; sort `branches` by `branch_task_id` Unicode code point order; recursively sort object keys by Unicode code point order; serialize as UTF-8 without BOM, trailing newline, or extra whitespace. Branch done/archive state is verified separately by T7 and is not in the digest. mtime, directory enumeration order, Runtime counters, and in-memory generations are forbidden digest inputs.

**F4.6.7** Convergence references exactly every Branch current valid REPORT and may additionally reference Root's current REPORT. Missing/stale references, references to another attempt, or a canonical digest mismatch return `FAMILY_CONVERGENCE_MISMATCH`. For convergence coverage, done and archive are both completed Branch states.

**F4.6.8** Creating a Branch, reopening a Branch, generating a new Branch attempt, or creating a valid replacement REPORT changes the canonical object or a report digest and invalidates old convergence. A Branch T7 done→archive changes only its path and does not invalidate otherwise matching convergence. Root T7 recomputes the digest within the same family linearization boundary.

## 7. C6 · Durable authorization and trust boundary

**F4.7.1** Authorization is carried by an append-only REVIEW, not a fifth envelope. `review_kind: authorization` contains at least:

```yaml
subject_ref: TASK-ID
decision: authorize
operation_kind: lifecycle_transition
transition: {from: done, to: archive}
authorization_scope: single_use
issued_at: <date-time>
expires_at: <date-time-or-null>
attempt_id: <id-or-null>
family_digest: <digest-or-null>
references: []
profile_ref: <adopted-profile-id>
```

**F4.7.2** A T4 acceptance or T5 rejection REVIEW that contains every authorization binding, including `profile_ref`, and whose issuer proof is evaluated `AUTHORIZED` by that Profile MAY also be the authorization basis. Otherwise it references a separate authorization REVIEW. Convergence alone is not Root T7 authorization.

**F4.7.3** Core verifies: the object exists and is REVIEW; `profile_ref` names an adopted Profile; decision, subject, transition, attempt, family, time, reuse, evidence references, and stored byte digests match. Structural failures return `AUTHORIZATION_REQUIRED`, `AUTHORIZATION_INVALID`, `AUTHORIZATION_EXPIRED`, `AUTHORIZATION_REUSED`, or `EVIDENCE_DIGEST_MISMATCH` as applicable.

**F4.7.4** The Profile named by `profile_ref` evaluates the issuer and its proof as exactly `AUTHORIZED`, `DENIED`, or `UNKNOWN`. Only `AUTHORIZED` passes; `DENIED` and `UNKNOWN` return `AUTHORIZATION_INVALID` and Fail Closed. If T4/T5/T6/T7 has no usable adopted authorization Profile, return `AUTHORIZATION_PROFILE_UNAVAILABLE`. Core contains no ADMIN/PM/QA role table.

**F4.7.5** A consuming transition persists `authorization_ref` and `authorization_digest`. A YAML `sender`, caller-supplied actor, Host allowlist, UI button, or REPORT conclusion alone cannot prove issuer authority or substitute for an authorization fact.

**F4.7.6** A Profile MAY use local single-user trust, OS ACLs, signatures, or another mechanism, but the mechanism is outside Core. FCoP is a governance and audit protocol and does not claim cryptographic identity security from editable files alone.

**F4.7.7** `profiles: []` remains conformant for T1–T3 and other ungated Base operations. A minimally completable ordinary developer workspace MUST explicitly adopt at initialization at least one usable authorization Profile, without making any fixed role a Core requirement.

## 8. C7 · Durable create-TASK idempotency

**F4.8.1** Mandatory 4.0 idempotency is limited to create TASK, including Branch. The lookup key is:

```text
workspace_id + operation_kind + operation_id
```

The stored comparison value is `normalized_request_digest`. `operation_kind` is `create_task` for ordinary and Branch tasks; branch_of is a digest field, not another namespace.

**F4.8.2** `operation_id` is 1–128 characters matching `[A-Za-z0-9][A-Za-z0-9._:-]*`. The implementation atomically reserves the lookup key; memory-only deduplication or an unlocked TASK scan is forbidden.

**F4.8.3** Same key/same digest returns `Existing` with original `task_id/path/digest` and creates no file/event. Same key/different digest returns `OPERATION_ID_CONFLICT`. Operation kinds do not share namespaces. Results survive restart.

**F4.8.4** The create-task digest input is canonical JSON with: `contract="fcop-create-task-v1"`, workspace_id, operation_kind, operation_id, sender, recipient, subject, body, priority after defaults, parent, branch_of, and references. Strings use Unicode NFC; CRLF/CR becomes LF; body ends with exactly one LF; absent values are JSON null; references are deduplicated and sorted by code point; object keys are sorted with no extra whitespace and encoded UTF-8; digest is lowercase SHA-256. Timestamps, allocated task_id/path, thread_key, risk_level, and Profile extensions are excluded.

**F4.8.5** Physical layout of the durable operation fact is Encoding-defined, but it is auditable, survives restart, and is not a second NOW truth. The result TASK repeats operation_id/kind/digest. Duplicate or conflicting records Fail Closed.

## 9. C8 · Atomic operations, duplicates, and recovery

**F4.9.1** The specification does not claim cross-directory migration has no intermediate state. Every recovery observation is classified as exactly one of `NOT_COMMITTED`, `COMMITTED`, `RECOVERABLE_DUPLICATE`, `DIVERGENT_DUPLICATE`, or `INDETERMINATE`; `INDETERMINATE` is never a successful fallback.

**F4.9.2** Destination MUST NOT be silently overwritten. Create-TASK external idempotency may return `Existing` under §8.3. A lifecycle duplicate with matching receipt/digest follows the recovery classification in §9.9 and does not create a public replay promise. Different content returns `TARGET_ALREADY_EXISTS_DIFFERENT`.

**F4.9.3** If one TASK appears in multiple authoritative stages, readers return `STATE_AMBIGUOUS` and Fail Closed. They MUST NOT select NOW by mtime, directory order, or event replay.

**F4.9.4** Internal recovery for every lifecycle transition uses a durable Toolkit/Encoding operation receipt containing operation identity, source/destination paths, normalized/content digests, and stage. Mechanical recovery is idempotent and MUST NOT create a second TASK, a second event for the same commit, or a silent overwrite. Divergence or unprovable corruption returns `RECOVERY_REQUIRED` and preserves every visible copy.

**F4.9.5** One Root-family linearization boundary covers every write that changes Root lifecycle state, the Branch set, any Branch lifecycle state/current attempt/current REPORT head, convergence REVIEW, or Root archive conditions. At minimum it covers Branch create, Root T2–T7, Branch T2–T7, Branch REPORT create/replacement, convergence REVIEW create/replacement, and Root T7. After acquiring the boundary, every operation re-reads and validates Root state, Branch set, attempts, REPORT heads, digest, and authorization; pre-lock caches cannot authorize commit. The boundary serializes only short protocol commits, never Agent work or unrelated TASKs without `branch_of`.

**F4.9.6** Lock/receipt/index paths are Encoding/Toolkit detail, not business envelopes. A stale lock MUST NOT be silently deleted by age; if safe release is unprovable, return `LOCK_RECOVERY_REQUIRED`.

**F4.9.7** Base guarantees cover only supported NTFS/POSIX filesystems with reliable local semantics. Cross-device, network, distributed, or weakly consistent filesystems without an external consistency layer return `UNSUPPORTED_FILESYSTEM` or Fail Closed.

**F4.9.8** Base distinguishes three guarantees:

| Guarantee | 4.0 Base scope | Identity |
|---|---|---|
| External request idempotency | Create TASK/Branch only | Caller-provided `operation_id` |
| Internal crash recovery | Every lifecycle transition | Durable Toolkit/Encoding operation receipt |
| Lost-response retry for authorized transitions | T4/T5/T6/T7 | Consumed `authorization_ref` + digest + transition |

Ordinary T2/T3 without a public `operation_id` do not promise arbitrary-time external request replay, while their internal crash recovery still prevents a second TASK/event or overwrite.

**F4.9.9** Logical receipt stages are `PREPARED`, `TARGET_DURABLE`, and `COMMITTED`; physical file names are Encoding-defined. The Base filesystem recovery table is unique:

| source | target | receipt/digest | Classification | Permitted mechanical action |
|---|---|---|---|---|
| Present and matching | Absent | No receipt or PREPARED | `NOT_COMMITTED` | Preserve source; operation may be safely abandoned |
| Present and matching | Present with same digest | TARGET_DURABLE | `RECOVERABLE_DUPLICATE` | Verify, delete source, persist the directory, complete receipt |
| Absent | Present and matching | TARGET_DURABLE or COMMITTED | `COMMITTED` | Complete COMMITTED receipt; do not repeat migration |
| Present | Present with different digest | Any | `DIVERGENT_DUPLICATE` | Delete/overwrite nothing; require human disposition |
| Both absent, or receipt/identity/digest is damaged or conflicting | Unprovable | Any | `INDETERMINATE` | Preserve all visible evidence and Fail Closed |

**F4.9.10** A mechanically proven `RECOVERABLE_DUPLICATE` appends/completes only the operation receipt and does not create a business REVIEW. Human disposition for `DIVERGENT_DUPLICATE` or `INDETERMINATE` uses a `review_kind: repair` REVIEW. A receipt is not an envelope, NOW truth, or Runtime database. Fault injection tests target the abstract stages, not Python function or temporary-path names.

**F4.9.11** After a lost response from T4/T5/T6/T7, retrying with the same authorization returns the existing committed result when `authorization_ref`, authorization digest, transition, and stored evidence digests all match. Consumption by a different transition returns `AUTHORIZATION_REUSED`; ambiguous facts Fail Closed.

## 10. Errors and Fail Closed

**F4.10.1** The Base 4.0 stable error registry contains exactly these 31 codes:

| Domain | Stable error codes |
|---|---|
| workspace | `WORKSPACE_ID_MISMATCH`, `WORKSPACE_ID_CLONE_CONFLICT`, `UNSUPPORTED_PROTOCOL`, `UNSUPPORTED_WORKSPACE_VERSION`, `UNSUPPORTED_ENCODING` |
| envelope/relation | `INVALID_ENVELOPE`, `RELATION_INVALID`, `REFERENCE_UNRESOLVED`, `BRANCH_DEPTH_EXCEEDED`, `ROOT_NOT_ACTIVE` |
| evidence | `REPORT_REQUIRED`, `REPORT_HEAD_AMBIGUOUS`, `ATTEMPT_MISMATCH`, `REVIEW_REQUIRED`, `FAMILY_CONVERGENCE_REQUIRED`, `FAMILY_CONVERGENCE_MISMATCH`, `EVIDENCE_DIGEST_MISMATCH` |
| authorization | `AUTHORIZATION_REQUIRED`, `AUTHORIZATION_INVALID`, `AUTHORIZATION_EXPIRED`, `AUTHORIZATION_REUSED`, `AUTHORIZATION_PROFILE_UNAVAILABLE` |
| idempotency | `OPERATION_ID_CONFLICT` |
| state/recovery | `INVALID_TRANSITION`, `BRANCH_NOT_TERMINAL`, `LEGACY_TRANSITION_NOT_ALLOWED`, `TARGET_ALREADY_EXISTS_DIFFERENT`, `STATE_AMBIGUOUS`, `RECOVERY_REQUIRED`, `LOCK_RECOVERY_REQUIRED`, `UNSUPPORTED_FILESYSTEM` |

**F4.10.2** Errors are machine-recognizable and include operation/subject references; free text is not the sole error contract.

**F4.10.3** Profile and Toolkit extensions use an explicit namespace and MUST NOT replace, redefine, or change the meaning of any Base error code.

## 11. v3 compatibility, Toolkit, MCP, and Profile

**F4.11.1** A v3 workspace is read under v3 until explicit migration. No 4.0 write occurs without §2 declaration. This candidate does not authorize migration.

**F4.11.2** `finish_task` and four history tools are `LEGACY_V3_ONLY`. A 4.0 workspace may read history through a Legacy Toolkit; moving an authoritative TASK to history is rejected.

**F4.11.3** `fcop` is a reference Toolkit and `fcop-mcp` is an optional Adapter. The 45 existing tools, 11 static resources, and 3 templates are not Core. Retained names dispatch by workspace version and Fail Closed when safe compatibility is unavailable.

**F4.11.4** Branch is expressible as create TASK plus branch_of and requires no new MCP tool. `close_issue` is downstream catalog drift and is not official surface.

**F4.11.5** Base MCP should be a thin stdio adapter. Relay is optional (candidate packaging `fcop-mcp[relay]`) and not Core. Upgrade/redeploy/GAL/workspace/session capabilities are Toolkit/Profile/Runtime.

## 12. Security, conformance, and release gate

**F4.12.1** Implementations validate workspace boundaries, reject path traversal, use UTF-8/LF, preserve unknown/failure evidence, and do not leak Profile/Runtime credentials.

**F4.12.2** WP2 verifies at least one normal, rejection, and applicable concurrency/recovery scenario for every C1–C8, including all six WP0 atomic/Branch scenarios and the WP1.1 fork, Profile, evidence-digest, family-race, idempotency-layer, and five-state recovery contracts.

**F4.12.3** Conflict among Schema, specification, and tests blocks release; no source silently wins. Every 4.0-conformant implementation satisfies the same observable contract.

**F4.12.4** This file is Candidate until `FCOP_4_CONTRACT_FROZEN`; it does not authorize Schema, tests, implementation, migration, push, or release.

## 13. C1–C8 invariant summary

| Core | Invariant |
|---|---|
| C1 | Every writable workspace has one stable ID; explicit forks get a new ID; invisible offline copies are not claimed detectable |
| C2 | Exactly four formal envelopes; REPORT/ISSUE/REVIEW append facts |
| C3 | Path is NOW; exactly seven edges; archive terminal; no active→done |
| C4 | Exactly four relations; Branch sibling-only; strong relations Fail Closed |
| C5 | New attempt per active entry; evidence digests; terminal Branch gate; one canonical family digest |
| C6 | Authorization is a durable REVIEW+digest; adopted Profile returns AUTHORIZED/DENIED/UNKNOWN |
| C7 | create TASK is durably idempotent by fixed key+digest |
| C8 | Three idempotency/recovery layers; five recovery states; no overwrite/guessing; complete family linearization |
