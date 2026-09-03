# FCoP 4.0 Candidate Specification (English)

> **Status: Candidate · Not Implemented · Not Released**
>
> WP1 contract version: `4.0.0-candidate.1`; baseline `68dbeb15f4e7f84e1d03f907be9fa66c2265843e`; WP0 evidence `c259bebdad77122d24dc18a6dd3f8fe191e4042f`. FCoP 3.2.5 remains the current protocol until ADMIN signs `FCOP_4_CONTRACT_FROZEN` and later implementation/release gates complete.

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

**F4.2.3** `profiles` is an ordered array of adopted Profile identifiers; an empty array means no additional Profile. v3 team, role, leader, and similar fields MAY remain Profile extensions and MUST NOT change Core semantics.

**F4.2.4** A backup or read-only mirror MAY retain the ID. Two writable copies may retain it only when external single-writer control makes them one logical workspace. Any independent fork/derived writable workspace MUST generate a new ID before its first 4.0 write. If this cannot be proven, return `WORKSPACE_ID_CLONE_CONFLICT` and Fail Closed.

**F4.2.5** Unsupported protocol, version, and Encoding return `UNSUPPORTED_PROTOCOL`, `UNSUPPORTED_WORKSPACE_VERSION`, and `UNSUPPORTED_ENCODING` respectively.

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

**F4.3.5** REVIEW kinds include at least `assessment`, `acceptance`, `rejection`, `authorization`, `convergence`, and `repair`. If retained, `mark_human_approved` may only append a REVIEW and MUST NOT edit the old REVIEW.

## 4. C3 · Single authoritative path, lifecycle, and events

**F4.4.1** An authoritative TASK MUST exist in exactly one of these paths; directory location is the sole NOW truth:

```text
fcop/_lifecycle/{inbox,active,review,done,archive}/TASK-*.md
```

**F4.4.2** Base has exactly seven legal transitions:

| # | from | to | Condition summary |
|---:|---|---|---|
| T1 | None | inbox | Idempotent create succeeds |
| T2 | inbox | active | Generate a new `attempt_id` |
| T3 | active | review | Current attempt has one valid REPORT |
| T4 | review | done | Current attempt has an acceptance REVIEW and valid authorization |
| T5 | review | active | Rejection/rework decision; generate a new attempt |
| T6 | done | active | Reopen authorization; generate a new attempt |
| T7 | done | archive | Closure, authorization, and family convergence gates pass |

**F4.4.3** One command may commit exactly one edge and append one transition. Multi-edge convenience calls MUST split the edges; failure at one edge MUST NOT fabricate later events.

**F4.4.4** `active -> done` is not in 4.0 Base. `finish_task` is 3.x Legacy; a 4.0 workspace MUST reject it with `LEGACY_TRANSITION_NOT_ALLOWED` and MUST NOT bypass T3/T4.

**F4.4.5** A transition contains `at/from/to/by/tool`; entry into active also contains a new `attempt_id`; transitions requiring evidence/authority contain `evidence_refs` and `authorization_ref`. Events are append-only and do not derive NOW.

**F4.4.6** Archive is terminal. An authoritative TASK MUST NOT move from archive to history or back into lifecycle. v3 history is read-only Legacy; a 4.0 Toolkit may only create non-authoritative cold-storage copies.

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

**F4.6.3** T4 references a REVIEW with `review_kind: acceptance` and `decision: approved`. Its subject_ref/attempt_id and referenced REPORT match current state, and §7 authorization is satisfied.

**F4.6.4** Branch and ordinary TASK use the same lifecycle and evidence gates. There is no Branch-specific completion state.

**F4.6.5** If a Root has Branches, T7 also references a valid convergence REVIEW:

```yaml
review_kind: convergence
subject_ref: ROOT-TASK-ID
family_digest: <sha256-lower-hex>
references: [REPORT-ID-A, REPORT-ID-B]
```

**F4.6.6** `family_digest` input is the Root ID plus every existing Branch tuple `(branch_task_id,current_attempt_id,current_report_id,current_report_digest)` at archive commit. Sort by branch_task_id, apply §8.4 canonical JSON, then SHA-256. Root is not a Branch, but its ID is in the digest domain.

**F4.6.7** Convergence references exactly every Branch current valid REPORT and may additionally reference Root's current REPORT. Missing/stale references or references to another attempt return `FAMILY_CONVERGENCE_MISMATCH`.

**F4.6.8** Creating a Branch, T5/T6 reopening a Branch, or creating a valid replacement REPORT changes family_digest and automatically invalidates old convergence. T7 recomputes it within the same family linearization boundary.

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
```

**F4.7.2** An acceptance/rejection/convergence REVIEW with equivalent bindings and a Profile-recognized issuer may also be the authorization basis; otherwise it references a separate authorization REVIEW.

**F4.7.3** Core verifies only: object exists and is REVIEW, decision is valid, subject/transition/attempt/family bindings match, time is valid, and single-use was not consumed by another transition. Failures return `AUTHORIZATION_REQUIRED`, `AUTHORIZATION_INVALID`, `AUTHORIZATION_EXPIRED`, or `AUTHORIZATION_REUSED`.

**F4.7.4** Profile decides whether sender may issue the authorization. Missing or unprovable signing authority Fails Closed. Core contains no ADMIN/PM/QA role table.

**F4.7.5** A consuming transition persists `authorization_ref`. A caller-supplied actor, Host allowlist, UI button, or REPORT conclusion cannot substitute for authorization fact.

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

**F4.9.1** The specification does not claim cross-directory migration has no intermediate state. Observable outcomes are classified as `NOT_COMMITTED`, `COMMITTED`, `RECOVERABLE_DUPLICATE`, `DIVERGENT_DUPLICATE`, or `INDETERMINATE`.

**F4.9.2** Destination MUST NOT be silently overwritten. Same canonical content with the same operation evidence may return Existing/Recoverable; different content returns `TARGET_ALREADY_EXISTS_DIFFERENT`.

**F4.9.3** If one TASK appears in multiple authoritative stages, readers return `STATE_AMBIGUOUS` and Fail Closed. They MUST NOT select NOW by mtime, directory order, or event replay.

**F4.9.4** Recovery uses durable operation identity, normalized/content digest, source/destination paths, and append-only receipt. Repair is idempotent and appends a repair REVIEW or equivalent auditable receipt. Divergence/corruption returns `RECOVERY_REQUIRED` and preserves every copy.

**F4.9.5** Branch creation, Branch T5/T6, convergence creation, and Root T7 share a Root-family linearization boundary. Each commit revalidates Root stage, Branch set, attempt/report heads, family digest, and authorization.

**F4.9.6** Lock/receipt/index paths are Encoding/Toolkit detail, not business envelopes. A stale lock MUST NOT be silently deleted by age; if safe release is unprovable, return `LOCK_RECOVERY_REQUIRED`.

**F4.9.7** Base guarantees cover only supported NTFS/POSIX filesystems with reliable local semantics. Cross-device, network, distributed, or weakly consistent filesystems without an external consistency layer return `UNSUPPORTED_FILESYSTEM` or Fail Closed.

## 10. Errors and Fail Closed

**F4.10.1** Stable error codes include at least:

| Domain | Stable error codes |
|---|---|
| workspace | `WORKSPACE_ID_MISMATCH`, `WORKSPACE_ID_CLONE_CONFLICT`, `UNSUPPORTED_PROTOCOL`, `UNSUPPORTED_WORKSPACE_VERSION`, `UNSUPPORTED_ENCODING` |
| envelope/relation | `INVALID_ENVELOPE`, `RELATION_INVALID`, `REFERENCE_UNRESOLVED`, `BRANCH_DEPTH_EXCEEDED`, `ROOT_NOT_ACTIVE` |
| evidence | `REPORT_REQUIRED`, `REPORT_HEAD_AMBIGUOUS`, `ATTEMPT_MISMATCH`, `REVIEW_REQUIRED`, `FAMILY_CONVERGENCE_REQUIRED`, `FAMILY_CONVERGENCE_MISMATCH` |
| authorization | `AUTHORIZATION_REQUIRED`, `AUTHORIZATION_INVALID`, `AUTHORIZATION_EXPIRED`, `AUTHORIZATION_REUSED` |
| idempotency | `OPERATION_ID_CONFLICT` |
| state/recovery | `LEGACY_TRANSITION_NOT_ALLOWED`, `TARGET_ALREADY_EXISTS_DIFFERENT`, `STATE_AMBIGUOUS`, `RECOVERY_REQUIRED`, `LOCK_RECOVERY_REQUIRED`, `UNSUPPORTED_FILESYSTEM` |

**F4.10.2** Errors are machine-recognizable and include operation/subject references; free text is not the sole error contract.

## 11. v3 compatibility, Toolkit, MCP, and Profile

**F4.11.1** A v3 workspace is read under v3 until explicit migration. No 4.0 write occurs without §2 declaration. This candidate does not authorize migration.

**F4.11.2** `finish_task` and four history tools are `LEGACY_V3_ONLY`. A 4.0 workspace may read history through a Legacy Toolkit; moving an authoritative TASK to history is rejected.

**F4.11.3** `fcop` is a reference Toolkit and `fcop-mcp` is an optional Adapter. The 45 existing tools, 11 static resources, and 3 templates are not Core. Retained names dispatch by workspace version and Fail Closed when safe compatibility is unavailable.

**F4.11.4** Branch is expressible as create TASK plus branch_of and requires no new MCP tool. `close_issue` is downstream catalog drift and is not official surface.

**F4.11.5** Base MCP should be a thin stdio adapter. Relay is optional (candidate packaging `fcop-mcp[relay]`) and not Core. Upgrade/redeploy/GAL/workspace/session capabilities are Toolkit/Profile/Runtime.

## 12. Security, conformance, and release gate

**F4.12.1** Implementations validate workspace boundaries, reject path traversal, use UTF-8/LF, preserve unknown/failure evidence, and do not leak Profile/Runtime credentials.

**F4.12.2** WP2 verifies at least one normal, rejection, and applicable concurrency/recovery scenario for every C1–C8, including all six WP0 atomic/Branch scenarios.

**F4.12.3** Conflict among Schema, specification, and tests blocks release; no source silently wins. Every 4.0-conformant implementation satisfies the same observable contract.

**F4.12.4** This file is Candidate until `FCOP_4_CONTRACT_FROZEN`; it does not authorize Schema, tests, implementation, migration, push, or release.

## 13. C1–C8 invariant summary

| Core | Invariant |
|---|---|
| C1 | Every writable workspace has one stable ID and explicit protocol/Encoding/Profile |
| C2 | Exactly four formal envelopes; REPORT/ISSUE/REVIEW append facts |
| C3 | Path is NOW; exactly seven edges; archive terminal; no active→done |
| C4 | Exactly four relations; Branch sibling-only; strong relations Fail Closed |
| C5 | New attempt per active entry; current REPORT/acceptance; verifiable family convergence |
| C6 | Authorization is a durable REVIEW reference; Core checks binding, Profile checks issuer |
| C7 | create TASK is durably idempotent by fixed key+digest |
| C8 | No overwrite or guessing; duplicates classified; evidence-based recovery; family linearization |
