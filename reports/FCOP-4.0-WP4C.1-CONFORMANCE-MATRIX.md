# WP4C.1 Conformance Matrix — WP4C.1a contract closeout

## Previous blocked run

```yaml
PREVIOUS_STATUS: BLOCKED
PREVIOUS_STOP_CODE: TASKBOOK_RELATION_SET_CONFLICT
PREVIOUS_CONTENT_COMMIT: 741b1829283f6a7fc1023e0edd8176b58c63ded4
PREVIOUS_MANIFEST_COMMIT: d92c72620757cea455aa24b5d635cc12f1e8b16a
ADMIN_CORRECTION: WP4C.1a
```

PR #18 and both commits remain ancestors/history, unchanged. The stop was correct; WP4C.1a explicitly corrects the taskbook, not the frozen specification. Current status below supersedes the prior report's status, not its historical facts.

## Scope and evidence classes

Input: `7f973dc5f32bc6b9e1076184d1247c55a1349bd5`; authorized scope WP4C_1A_ONLY.
[EN contract](../docs/fcop-4.0/rule-distribution-contract.md), [ZH contract](../docs/fcop-4.0/rule-distribution-contract.zh.md), and [decision schedules](FCOP-4.0-WP4C.1-CONTRACT-DECISIONS.md) are the candidate authority being reviewed.
No production/conformance test files, global driver, rule source or generator is changed. Rows below are **future behavioral test obligations**, not tests executed or method/parameter probes. WP4C.2 alone may implement them after its own authorization. Passing current document checks does not satisfy future behavior.

## Future behavioral contract matrix

Each row defines distinct setup/action/postconditions, including rejection or failure cases. No existing frozen test_id is renamed or added to its denominator.

| Check | Contract | Arrange / Act | Required observable Assert | Implementation evidence owner |
| --- | --- | --- | --- | --- |
| DIST-01 | RD-01/02 | Valid package vs package claiming new Core role/state; validate/select | Valid trace accepted; invented authority rejected; no network/runtime service or lifecycle effect | WP4C.3 |
| DIST-02 | RD-03/19 | Ordinary and repository-development requests; add excluded RC or old draft as dependency | Ordinary has no development text; excluded RC rejected even for development; missing optional constitution does not substitute another source | WP4C.3 |
| DIST-03 | RD-04/05 | Complete clause schedule vs duplicate/missing owner/old relation alias | 73 unique IDs and nine domains; exactly four fields; aliases reject; common relations available without convergence | WP4C.3 |
| DIST-04 | RD-06 | Valid EN/ZH bytes vs same-label BOM/CR/control/invalid UTF8 or changed clause set | Valid bytes pass; malformed bytes/parity mismatch reject before any files/receipts | WP4C.3 |
| DIST-05 | RD-07 | Valid 18-artifact Manifest vs duplicate JSON key, unknown field/schema, missing language or embedded adoption state | Exact schema/fields pass; all malformed variants yield structured manifest error, zero effects | WP4C.3 |
| DIST-06 | RD-07/08 | Same version/hash-correct bytes vs altered bytes/size/path, symlink escape | Changed bytes or escaping source rejects; neither cache nor newline normalization hides drift | WP4C.3 |
| DIST-07 | RD-08 | Same selected inputs with permuted manifest records/directory order; cycle/missing dependency/conflict variants | Identical valid ordering; cycle/incomplete explicit selection reject without autoload | WP4C.3 |
| DIST-08 | RD-09 | No receipt but existing Host file; explicit valid adoption vs wrong workspace/version/broken previous hash | Existence never means adopted; only verified evidence selection passes; zero implicit migration or lifecycle authority | WP4C.4 |
| DIST-09 | RD-10 | Successful deploy, then inspect immutable receipt and hashed backup; induce before/after mismatch | Exact observed hashes/path chain recorded; old receipt bytes unchanged; mismatches never recorded as success | WP4C.4 |
| DIST-10 | RD-10 | Previous adopted snapshot available vs missing/modified backup or target; request rollback | Exact previous bytes restored with append-only evidence; drift rejects, no arbitrary label rollback or deletion | WP4C.4 |
| DIST-11 | RD-11/12 | Three static profiles vs unknown Host/caller evaluator/model probe request | Explicit selected profile only; unsupported typed-unavailable, no probing/adoption/issuer trust from text | WP4C.4 |
| DIST-12 | RD-11 | Independently supply support, adoption, generation and consumption evidence | Each remains independent; no inferred true/false from another field; unknown consumption stays unknown | WP4C.4 |
| DIST-13 | RD-12/13 | Existing unowned AGENTS/CLAUDE/legacy Cursor entry vs new empty eligible target | Unowned input survives byte-identically and operation rejects; new explicit target gets only selected profile entry | WP4C.4 |
| DIST-14 | RD-13 | Repeat plan from identical bytes in different absolute dirs/times | Byte-identical generated outputs and digests; no timestamps/absolute machine paths/random output | WP4C.4 |
| DIST-15 | RD-13 | User prefix/suffix, valid block vs nested/duplicate/missing markers; apply | Outside bytes exactly preserved; invalid markers reject with zero writes; full target size is counted | WP4C.4 |
| DIST-16 | RD-14 | Proven reference profile and immutable local snapshot vs missing, stale, relocated/escaping reference | Correct relative resolution/order/hash; invalid reference fails; never fetch remote latest or infer actual runtime consumption | WP4C.4 |
| DIST-17 | RD-15 | Bounded selected-language artifacts vs multi-language not adopted or over-cap result | Exact framing/ordered bytes; no translation/truncation/mode fallback; limit rejects all writes | WP4C.4 |
| DIST-18 | RD-16 | Snapshot workspace recursively; run dry-run for normal/conflicting targets | Identical file set/bytes afterward, including no mkdir/backups/receipts; complete diff/hash/size plan returned | WP4C.4 |
| DIST-19 | RD-16 | Make valid plan, edit target before commit; real two-process competing apply to same target | Revalidate under short coordination; stale contender rejects; no lost user edit or contradictory success receipts | WP4C.4 |
| DIST-20 | RD-16 | Inject failures before stage durability, between replacements and before success receipt | Prior targets/backups preserved; actual partial state explicit; no fake all-or-nothing/receipt success; explicit recovery only | WP4C.4 |
| DIST-21 | RD-17/18 | Adopt sequential, request Branch scope; explicitly adopt parallel separately | Sequential includes relations, excludes convergence and cannot silently activate Branch; parallel adds exactly convergence | WP4C.3 |
| DIST-22 | RD-19 | Repository-development fixed references vs ordinary default wheel/MCP guidance | Entry/manual/contracts/TASK authorization fixed; developer-only source never in ordinary response/package | WP4C.3 |
| DIST-23 | RD-20 | Existing v3 workspace and unversioned redeploy vs explicit v4 selection/no receipt | Legacy behavior remains; v4 never invokes legacy writer, auto-migrates or inflates old sources | WP4C.5 |
| DIST-24 | RD-21 | Read rules/protocol/guidance/team resources across workspace versions; Relay same reads | Correct typed object/version/digest or unavailable; zero writes/adoption/evaluator installation; delegate Toolkit logic | WP4C.5 |
| DIST-25 | RD-22 | Trigger each declared failure with safe operation/subject refs | Structured namespaced code matches condition, no text-only success/error inference and no Base-code redefinition | WP4C.3 |
| DIST-26 | RD-23 | Upgrade disk package while getter/index/process/Host snapshots remain old; inspect each layer | Distinct invalidation/adoption/consumption evidence; no all-layers-refresh claim from package version | WP4C.5 |
| DIST-27 | RD-23 | Build future authorized wheel/sdist on supported platforms; compare source/member bytes | All v4 Manifest/module hashes exactly match; CRLF diagnostics not success; no constitution/Host output bundle leakage | WP4C.6 |
| DIST-28 | RD-23 | Measure each assembly/Host and six historical surfaces, one language vs explicit multiple | Reproducible raw bytes and disclosed estimator; alternative Host duplication not actual session consumption; no silent deletion | WP4C.6 |
| DIST-29 | RD-23 | Authorized fixed CodeFlowMu read-only shadow vs requested deploy | Only permitted snapshot inspection; product ownership/pins preserved; RC not FCoP source and no files changed | WP4C.5 |
| DIST-30 | RD-24 | Missing next-stage authorization or unsatisfied Gate | Stop; no tests/implementation/autocontinuation/merge/release from this contract alone | WP4C.2 |

The 30 design rows are not 30 executed tests. WP4C.2 must create real behavioral arrangements and assertions (including actual competing operations), not greenable empty method stubs. Later taskbooks select exact tests/implementation write sets. Failure recovery for distribution remains separate from frozen Core five-state lifecycle conformance.

## Current read-only document checks

| Check | Required assertion | Current evidence class |
| --- | --- | --- |
| DOC-01 | GitHub fixed taskbook bytes equal declared SHA and local object | Executed input identity check |
| DOC-02 | Required Gate/blocked/scope/spec ancestors and blocked four-file identities | Executed Git parent/byte checks |
| DOC-03 | EN/ZH frozen bytes unchanged, complete read and ordered 73 clause IDs | Executed byte/ID check plus human semantic review |
| DOC-04 | EN/ZH RD-01 through RD-24 identical order; fields, enums, errors and Gates agree | Machine IDs/tokens/tables plus semantic review, not automatic translation proof |
| DOC-05 | Core relation arrays exactly four; module table has no legacy aliases | Machine contract extraction |
| DOC-06 | Sequential exact eight; parallel equals sequential plus convergence; dependencies acyclic and satisfied | Machine JSON/table checks |
| DOC-07 | Decision primary rows exactly equal all 73 frozen IDs, one owner each, zero relations/convergence overlap | Machine set/cardinality checks |
| DOC-08 | All 147 audit unit IDs and intervals exactly appear once with action/owner | Machine source-set comparison plus per-unit review |
| DOC-09 | All 86 audited paths appear once with one owner; source Git hashes match audit inventory | Machine set/hash checks |
| DOC-10 | Exactly 12 consumers/four prior outputs/three assemblies/nine modules; common variants 4/4 | Machine table counts plus policy review |
| DOC-11 | All three old names have actual-source dispositions; excluded RC absent from allowed source/module dependencies | Bounded source scan and contract exclusion review |
| DOC-12 | Manifest/adoption/Host fields separate; no timestamp/runtime field in package Manifest | Field-table checks plus semantic review |
| DOC-13 | Entire six-file delivery strict UTF8/LF/no BOM; table columns and Markdown links resolve; diff clean | Executed before commits; full results in final receipt |
| DOC-14 | Only five content paths, followed by Manifest-only child; fixed input direct parent; preserved history | Git tree/commit checks |
| DOC-15 | Remote HEAD/direct parents and six exact GitHub file hashes match local objects | Executed after push; final PR receipt contains actual SHAs |

Product tests: NOT_RUN. Rule generation: NOT_RUN. Host probes/deploys: NOT_RUN. Frozen conformance edits: 0. A document check PASS is not repair of the baseline or behavior conformance. The complete executed check summary and limitations are in RESULT; network-specific outcomes are recorded after delivery in the Draft PR receipt.
