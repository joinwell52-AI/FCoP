# WP4C.0a Constitution Source Decision — audit input only

## Outcome

The fixed discussion source is now identifiable and usable for baseline review. It is **not a normative constitution**, not licensed for redistribution, not frozen, not implemented and not an Agent loading requirement. This report proposes questions for ADMIN; it neither edits the source nor signs a Gate.

```yaml
AUTHORIZED_SCOPE: WP4C_0A_ONLY
TASKBOOK_COMMIT: eb086ee43f345a4d93ffb520049dc8af08712d3b
TASKBOOK_SHA256: 9db3b811048618cf4fe1baf4352c9e980f2d6da3e061f41709f553520e8e589c
SOURCE_KIND: ADMIN_AUTHORED_DISCUSSION_DRAFT
SOURCE_VERSION: 0.1-discussion-draft
CONSTITUTION_SOURCE_COMMIT: 0c61f7d3108777adb7aaf375324616c004fcaf7d
CONSTITUTION_SOURCE_SHA256: 25e70e221d6b54072503a8ec7224df33000fa63c0b12a64c148d86a0081b6762
SOURCE_PATH: taskbooks/fcop-4.0/WP4C.0a/sources/Agent-Native-Engineering-Constitution-v0.1-discussion-draft.zh.md
REVIEW_INPUT_FIXED: true
NORMATIVE: false
CONTRACT_FROZEN: false
IMPLEMENTATION_AUTHORIZED: false
BUNDLING_AUTHORIZED: false
RULE_GENERATION_AUTHORIZED: false
LICENSE_STATUS: UNRESOLVED
CANONICAL_RELEASE_PATH: UNRESOLVED
ENGINEERING_CONSTITUTION_SOURCE_STATUS: DISCUSSION_DRAFT_FIXED_REVIEW_INPUT
ENGINEERING_CONSTITUTION_LICENSE_STATUS: UNRESOLVED
ENGINEERING_CONSTITUTION_CONTRACT_FROZEN: false
WP4C_0_AUDIT_BLOCKERS: 0
WP4C_1_ENTRY_BLOCKERS: 1
WP4C_1_STARTED: false
REQUESTED_GATE: WP4C_0_BASELINE_ACCEPTED
```

Sources: [fixed taskbook](https://github.com/joinwell52-AI/FCoP/blob/eb086ee43f345a4d93ffb520049dc8af08712d3b/taskbooks/fcop-4.0/WP4C.0a/01-Constitution-Source-Classification-and-Baseline-Audit-Resume-Taskbook-v1.0.zh.md), [fixed discussion text](https://github.com/joinwell52-AI/FCoP/blob/0c61f7d3108777adb7aaf375324616c004fcaf7d/taskbooks/fcop-4.0/WP4C.0a/sources/Agent-Native-Engineering-Constitution-v0.1-discussion-draft.zh.md). Raw GitHub/base64-decoded bytes and Git blob SHA-256 matched. Both source and preserved blocked commit are ancestors of current input.

## Preservation and authority

The four old BLOCKED reports and old Manifest remain unchanged prefixes of their updated files; parent commit 4420bf6cdd456e328230015bcffef4fdabf615a8 and PR #16 history are not rewritten. WP4C.0's stop was correct under its taskbook. WP4C.0a §0 explicitly changes the current audit Gate meaning: constitution freeze is a *next-phase entry* requirement, not a prerequisite to finishing a read-only audit.

Read access is permitted by this taskbook. That permission does not settle copyright ownership, license compatibility, sublicensing, translation, vendoring, extraction or generated derivatives. Repository-level license is not presumed to cover this source for distribution. No legal conclusion beyond ADMIN's explicit UNRESOLVED status is made.

Existing TEAM-ROLES/TEAM-OPERATING-RULES, common role injection block, Rule 0.b and historical charter ADRs are different documents. None is a substitute source or authority for the named engineering constitution.

## Twelve principles — 12/12 mapped

Classification is **existing coverage**, not new normative adoption. Sources below are fixed input canonical rules/commentary and frozen F4 clauses. “Covered” means the stated governing intent is already expressed; it does not prove all product implementations obey it. “Partial” separates supported Core semantics from broader development/runtime aspirations. Potential overreach is recorded explicitly rather than converted into a new Base invariant.

| Principle / discussion §3 | Coverage | Existing evidence | Gap / conflict boundary |
| --- | --- | --- | --- |
| C1 Goal/contract fixed; Agent chooses execution path | PARTIAL | Rule Scope; commentary Agent Autonomy; F4.1.2 | Old fixed workflow/role prescriptions are Profile policy. No frozen general software-development freedom contract. |
| C2 Emergence free, responsibility/authority/facts constrained | PARTIAL | Rule 0.c/1 and evolution diagram; F4.2/F4.7 | Role/session occupancy is legacy policy, not issuer proof. Emergent convention cannot override frozen C1–C8. |
| C3 Executor completion is not acceptance | COVERED | Rules 0.a.3/0.a.5/0.a.6; F4.6.3/F4.7 | Existing separation is clear; legacy archive permission examples still need version isolation. |
| C4 Semantic decision belongs to responsible subject | PARTIAL | Rule 0.b; F4.7.4–F4.7.6 | Core verifies adopted issuer proof, not business truth. Who is responsible and independent remains Profile/product policy. |
| C5 Only fully observable deterministic conditions form mechanical Gates | PARTIAL | Commentary GATE self-collision/checklist; F4.10.2/F4.12.3 | Development Gate-design criteria are broader than Base validation. Do not create automated acceptance from an incomplete metric. |
| C6 Materialization executes authorized decision, not business judgment | COVERED | F4.1.2, F4.4.2, F4.7.5 | Thin Toolkit/adapter boundary fits. Source calls this a design principle, not permission for new Runtime architecture. |
| C7 EVAL independent evidence, no automatic lifecycle change | PARTIAL | Rule 9.7/GAL separation; F4.1.4 | Base explicitly excludes fixed EVAL. Role independence and evaluation scheduling need application policy, not a Core EVAL envelope. |
| C8 Process/test/report status is not goal achievement | COVERED | Rule 0.a.3/0.a.6; F4.6.2–F4.6.3 | Test green is an observation; ADMIN still decides this audit Gate. |
| C9 Uncertainty explicit and fail closed | COVERED | Rule 0.c; F4.9.1/F4.9.3/F4.9.9, F4.10 | Unknown recovery/evidence never becomes success or a guessed state. |
| C10 Recovery must not replay unknown external effects | PARTIAL | F4.8.1–F4.8.5 and F4.9.8–F4.9.11 | Draft applies broadly to world-changing operations; Base external idempotency is only TASK/Branch create. Broader effect safety is development/runtime policy, not an expanded Base replay promise. |
| C11 Local AI discretion cannot rewrite authority/state/writer boundaries | COVERED | Rule 8/Scope; F4.0.2/F4.1.3/F4.1.4; fixed taskbook allowlists | Legacy “rules highest” wording must not outrank frozen specification. Only explicit ADMIN taskbook permits changes. |
| C12 RPA-style predefined business paths need architecture scrutiny | MISSING | Closest: commentary convenience-layer philosophy and F4.1.2 | No explicit RPA-vs-Agent architecture review test in existing rules. Candidate development principle only; do not add scheduler/product workflow to Core. |

Counts: COVERED 5, PARTIAL 6, MISSING 1, direct unavoidable frozen-contract CONFLICT 0 = 12. C10 would conflict if promoted into a universal Base idempotency guarantee; C7 would conflict if made a fixed Core EVAL role. Those promotions are explicitly excluded, not silently treated as implemented.

Discussion §§4–9 further separate execution/evaluation/decision/materialization facts, offer architecture-review questions, distinguish FCoP from CodeFlowMu, enumerate pre-freeze conditions and discuss future loading. They are review material only. A future summary cannot be declared deterministically derived from a *frozen* constitution before that source is actually frozen.

## Minimum ADMIN decision list — 12/12

All entries below are candidates or unresolved choices, not decisions by ME.

| ID | ADMIN decision needed | Current established fact | Candidate boundary / acceptance evidence |
| --- | --- | --- | --- |
| D01 | Formal name and version | 0.1-discussion-draft only | Explicit promotion receipt; do not rename it v1.0 in an execution report. |
| D02 | Authority repository and canonical path | Fixed taskbooks source path, not a release path | One canonical document identity plus pinned commit; source ownership explicitly declared. |
| D03 | EN/ZH strategy | Fixed input is Chinese | Decide authoritative language and paired clause IDs/review process before translations are distributed. |
| D04 | Intended audience | Taskbook limits default loading to developers, excludes ordinary business | Separate FCoP developer, third-party developer and ordinary Agent policies; product mentions do not auto-adopt. |
| D05 | Mandatory-load conditions | No currently authorized mandatory loading | Freeze development-only trigger and proof requirements; never business lifecycle field/Gate. |
| D06 | Core/Spec/Profile/Toolkit/Runtime relationship | Core C1–C8 unchanged | Constitution constrains engineering choices; cannot redefine envelopes, errors, authority or scheduling ownership. |
| D07 | Relationship to generic rule package | Not a generic rule source | Explicit development namespace/reference; exclude from ordinary minimum assembly and default resources. |
| D08 | Revision and Gate process | No contract-frozen receipt | Independent ADMIN source/effect freeze, versioned changes and taskbook authorization; never auto-adopt latest. |
| D09 | License and redistribution | UNRESOLVED | Explicit rights for copying, translation, summaries, vendoring and package inclusion; no guessed repository-license inheritance. |
| D10 | Content/artifact digest contract | Review source exact SHA-256 fixed | Define canonical bytes, summary provenance, source-to-artifact digest and verification failure behavior. |
| D11 | Host reference versus duplicate copies | No implemented adopted Host profile | One authority reference with pinned hash; bounded generated embeds only if licensed and deterministic, never hand-maintained truths. |
| D12 | Ordinary-business exclusion rule | Explicitly prohibited default injection | Negative assembly/resource/package tests under a later taskbook, including no automatic CodeFlowMu injection. |

One aggregate next-phase entry blocker, **ENGINEERING_CONSTITUTION_SOURCE_EFFECT_LICENSE_FREEZE_REQUIRED**, has these twelve facets; the count of one is a Gate count, not a claim there is only one unanswered question. Even after a baseline Gate signature, WP4C.1 remains unauthorized until this decision and a new fixed taskbook.

## Validation and stop

- Source text unchanged; no constitution-derived rules or Host files generated.
- Existing artifacts inspected: no constitution payload; common role workflow is a distinct legacy source, not this constitution.
- No production, tests, Schema, MCP, Host projection, rules, main, CodeFlowMu, migration or release changes.
- Five reports form the Content Commit; Manifest-only direct child; six-file remote readback and complete machine receipt follow. This document does not preclaim network delivery.
- The only requested Gate is WP4C_0_BASELINE_ACCEPTED. ADMIN alone may sign. Stop after delivery; do not begin WP4C.1.
