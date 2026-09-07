# WP4C.0 Context and Collision Audit — BLOCKED

- Repository: `joinwell52-AI/FCoP`
- Gate / audited tree: `aad88ae5f1112881545d30c9938739e83481516d`
- Taskbook commit: `962b67d89e137c26440291d3a48fc7aea1cfebb6`
- Taskbook: [fixed WP4C.0 authority](https://github.com/joinwell52-AI/FCoP/blob/962b67d89e137c26440291d3a48fc7aea1cfebb6/taskbooks/fcop-4.0/WP4C.0/01-Rule-Distribution-Host-Assembly-and-Development-Context-Baseline-Audit-Taskbook-v1.0.zh.md)
- Taskbook SHA-256: `c8c4cb26708a480a6793d88c21511b103f140021c3827c9977b076dfed748e55`
- Scope: `WP4C_0_ONLY`; report state: `BLOCKED`.

## Stop decision

`ENGINEERING_CONSTITUTION_SOURCE_UNRESOLVED` is one confirmed P0 blocker, not an exhaustive count of all possible conflicts. Taskbook sections 3 and 14 require an identifiable authority file, version, digest, license and acquisition method for 《Agent 原生软件工程宪法》. Those cannot be established from the supplied fixed inputs. Section 14 permits factual BLOCKED reports but prohibits requesting the acceptance Gate.

No replacement constitution is authored, downloaded or adopted. The audit stopped at this prerequisite; remaining audit obligations are explicitly incomplete. `REQUESTED_GATE: NONE`; WP4C.1 is not started.

## Measured Git-blob identities

Method: `git show <Gate>:<path>` captured as raw bytes; SHA-256 over those bytes; strict UTF-8 decode; line count from `splitlines()`; absence of CR checked. These measurements concern committed blobs, not Windows working-tree checkout line endings or effective session context.

| Gate path | UTF-8 bytes | Lines | SHA-256 |
|---|---:|---:|---|
| `src/fcop/rules/_data/fcop-rules.mdc` | 75839 | 1359 | `24f42cfe76063bd39358cdb03a59e8d4e6b391c36bc9749302185252a84d1686` |
| `src/fcop/rules/_data/fcop-protocol.mdc` | 117608 | 2358 | `8ac413b1c39238df82a175d108c166c58c27fbe833b202470e140755780250d3` |
| `AGENTS.md` | 192003 | 3704 | `796281fea0c4d572d805c30f5e0651bc2aa72a8fd34738fcc7158354fc4cd5d2` |
| `CLAUDE.md` | 192003 | 3704 | `796281fea0c4d572d805c30f5e0651bc2aa72a8fd34738fcc7158354fc4cd5d2` |
| `.cursor/rules/fcop-rules.mdc` | 75764 | 1359 | `f38a204bde056e96aee06c4a0e418c3ac2eb6d89e74489b482ecc534a82fd6f2` |
| `.cursor/rules/fcop-protocol.mdc` | 116250 | 2330 | `32b621e0332000f6a78230a47ee715468a964e8e9d93e184acfce5f16805e9ff` |

All six measured blobs decode as strict UTF-8 and contain no CR. This is 6/6 for this bounded metadata set, not completion of the mandatory-input encoding audit or all context requirements.

## What the measurements do and do not prove

- AGENTS.md and CLAUDE.md are byte-identical at the Gate.
- The two Cursor files are not byte-identical to the corresponding loader-declared inputs.
- No semantic comparison establishes why those copies differ; no additional P0 is inferred from hash inequality alone.
- A six-file byte sum would double-count alternative Host surfaces. No effective per-session token total is claimed.
- Token estimator: NOT_USED. Normative fraction: NOT_MEASURED. Repeated-body ratio: NOT_MEASURED.
- Ordinary sequential-task, parallel-Branch and FCoP-development candidate minimal assemblies: all NOT_AUDITED.
- Deployment overwrite defaults, managed blocks, downstream ownership, partial writes, deterministic regeneration, rollback and receipt behavior: NOT_AUDITED.

## Confirmed authority collision risk

The fixed inputs name a development-only engineering constitution but do not fix its authority artifact, version, digest, license or acquisition. Treating the historical team-constitution wording as that engineering constitution would conflate different documents and audiences. No such adoption was made.

Known P0: one prerequisite blocker, `ENGINEERING_CONSTITUTION_SOURCE_UNRESOLVED`. The full collision audit remains incomplete. No claim of zero other risks is made.

## Encoding diagnostic limitation

An initial tree-wide search decoded as strict UTF-8 encountered an invalid byte sequence in a historical log. Search output was subsequently captured as bytes, with invalid sequences escaped for inspection. No log was edited or repaired. That diagnostic does not invalidate the six strict-UTF-8 measurements above and does not justify a repository-wide encoding PASS.

## Protection and continuation boundary

No content was shortened, no rule text was rewritten, and no arbitrary KiB/token budget was used to remove semantics. No CodeFlowMu, real downstream workspace or Host configuration was changed. The next required input is ADMIN's fixed constitution authority/licensing clarification; it is not authorization for WP4C.1 implementation.

---

# WP4C.0a resume — context and collision evidence

Input: `eb086ee43f345a4d93ffb520049dc8af08712d3b`. The earlier BLOCKED measurements/history stay intact; current measurements below use explicit LF line accounting.

## Six-file byte budget and duplication — 6/6

Raw Git bytes, strict UTF-8. LF lines = count(0x0A) plus one only for an unterminated last line. The old Python splitlines count additionally split two U+000C characters in commentary; the corrected LF counts are lower by two for commentary/combined copies. No file content was repaired.

Token estimate is **ceil(UTF-8 bytes / 4)**, a reproducible sizing heuristic, not a tokenizer result, maximum or model context guarantee. Mixed Chinese/English, box drawing and tables can differ materially by model. No token limit is used to delete semantics.

| Input path | Bytes | LF lines | Byte/4 estimate | Claimed-binding fraction | Repeated exact-line fraction | Canonical exact-line reuse |
| --- | --- | --- | --- | --- | --- | --- |
| src/fcop/rules/_data/fcop-rules.mdc | 75839 | 1359 | 18960 | 63.59% | 3.77% | 100% |
| src/fcop/rules/_data/fcop-protocol.mdc | 117608 | 2356 | 29402 | 55.41% | 0.84% | 100% |
| AGENTS.md | 192003 | 3702 | 48001 | 57.76% | 2.28% | 99.62% |
| CLAUDE.md | 192003 | 3702 | 48001 | 57.76% | 2.28% | 99.62% |
| .cursor/rules/fcop-rules.mdc | 75764 | 1359 | 18941 | 62.61% | 3.78% | 99.85% |
| .cursor/rules/fcop-protocol.mdc | 116250 | 2328 | 29063 | 55.13% | 0.84% | 100% |


Binding-fraction methodology: for canonical sources, sum raw LF-delimited bytes in Disposition intervals marked normative=true divided by full file bytes. It measures old **claimed guidance/Profile obligation** spans, including surrounding examples, not genuine v4 normative authority. For projections, sum nonblank line bytes exactly matching a line within those claimed-binding spans divided by full projection bytes (a conservative matching proxy, excluding LF bytes). Therefore primary-source and projection percentages use explicitly different denominators. Neither is a claim that those legacy paragraphs conform to v4. Only frozen Specification supplies v4 normative requirements.

Repeated fraction = sum over nonblank exact-line strings of UTF-8 line length × (occurrences−1), divided by sum of all nonblank line byte lengths. Canonical reuse fraction = fraction of nonblank line bytes whose entire line is present in either canonical input. Whitespace and bilingual paraphrases are not fuzzy-matched. These ratios undercount semantic repetition and overemphasize short repeated markers; they are not an effective model-context measurement.

AGENTS and CLAUDE are byte-identical alternatives: if a Host incorrectly loaded both, the second adds 192,003 duplicate bytes (50% of their combined bytes). No real session double-load was proven. Cursor's two files total 192,014 bytes; AGENTS adds another largely redundant 192,003 if also consumed. Actual Host load order is unverified and must not be inferred from these totals.

## Structural comparison, deterministic formula and invalidation

1. Canonical rules vs Cursor rules differ only in the historical 3.2.5 MCP-docstring change entry near source line 1183: current canonical describes nine required/five conditional tools; output retains an older short list.
2. Canonical commentary vs Cursor commentary differs by the missing 28-line development docstring checklist at source line 503. Both still advertise 3.2.5. Version-only drift detection misses this difference.
3. Existing AGENTS/CLAUDE reuse the older concatenated body and contain an embedded BOM before commentary; frontmatter keys appear around line 1377. Thus “frontmatter stripped” is not fully true for current legacy inputs.
4. Static generator formula is preamble → version banner → separator → stripped rules → separator → stripped commentary, independent of root path/time. No generator was invoked. Equal AGENTS/CLAUDE plus identified source differences establish structural provenance, not reproducible regeneration of the checked-in files.
5. Rule getter cache and team index cache persist through a running process. Package update, process restart, deployment, Host restart, and actual rule consumption are five separate events. None invalidates all other layers automatically.
6. Existing deployment order is Cursor rules → Cursor commentary → AGENTS → CLAUDE. Model prompt precedence across Host files/resources cannot be proven by that filesystem write order.

## Collision register — 12 findings, all classified

| ID | Evidence at fixed input | Consequence | Classification / future resolution |
| --- | --- | --- | --- |
| COL-01 | project.py:1450–1475; CodeFlowMu root prefixes/suffix | force replaces product-owned root policy along with FCoP text | Host ownership/explicit adoption; fail before writes on unowned content. |
| COL-02 | project.py:1461–1475 | Archive first, plain write after; partial four-target install possible | Toolkit deployment transaction/recovery proof, not Core lifecycle mutation. |
| COL-03 | project.py:5249/1463; test_project_deploy_protocol.py repeated-deploy test | Seconds-only archive key may collide; archive=False intentionally retains no backup | Legacy hazard recorded; future unique receipts/retention policy requires ADMIN contract. |
| COL-04 | rules source vs Cursor diffs above; local version reader | Same version but different body, no digest validation | Freeze exact module/entry digest and adoption identity later. |
| COL-05 | canonical commentary BOM, _strip_yaml_frontmatter | Frontmatter not removed, embedded BOM in combined markdown | Encoding contract required for future v4 guidance; no v3 byte repair here. |
| COL-06 | 107-file encoding scan; two U+000C in commentary | UTF-8 pass does not imply clean markdown/control characters or BOM-free text | Separate strict bytes, structural checks and semantic review. |
| COL-07 | rules Rule 1/4/9; frozen F4.1.4/F4.7 | Fixed roles/session/Host declarations can be mistaken for authorization | Profile boundary; trusted evaluator not caller-supplied text. |
| COL-08 | rules Rule 5/8.v3/9.1/9.6 | Mixed legacy immutability/finish/history/fifth-envelope semantics contradict v4 | Version-isolated superseded/conflict dispositions, not spec edits. |
| COL-09 | alwaysApply both files; combined copies; protocol history | Bilingual/history/dev bulk loaded with ordinary business context | Audience-scoped candidate modules; no arbitrary size-based deletion. |
| COL-10 | relative ../../spec links inside commentary; getting-started references | Same text moved to root resolves links differently; absent fcop-3.0-spec paths | Freeze reference base and pinned content; generated output cannot become authority. |
| COL-11 | release checklist manual copy/patch; release-process “byte-identical” | Maintenance procedure can create multiple hand-edited truths | Legacy development SOP, future source-only deterministic projection. |
| COL-12 | discussion draft license/effect unresolved; root entries generic | Development constitution could leak into business/runtime gates | One WP4C.1 source/effect/license freeze entry blocker; no injection or bundling. |

These are risk findings, not 12 unperformed audit tasks. WP4C.0a §7 permits closing the baseline once known hazards are documented; it does not bless deployment, automatically clear the next-phase entry Gate, or authorize their fixes.

## Encoding validation limits

107 explicitly bounded mandatory source/spec/code/doc/test/script blobs: strict UTF-8 **107/107**, no CR **107/107**, leading BOM **50/107**. All 86 inventory entries include their BOM flag. The common block and two maintenance scripts are no-BOM. Embedded BOM in AGENTS/CLAUDE is additional to this leading-BOM count. Commentaries have two U+000C each; LF remains intact.

`scripts/rule_encoding_guard.py` is a narrow regression guard: strict UTF-8, CJK count threshold, expected markers and four known mojibake sequences. It does not enforce no BOM/LF/exact hashes, parse every table or prove rule consistency. The 44 passing rule tests likewise do not prove all legacy text clean. No broad repair or generation ran.

Retained fcop archives: 131/144 package members differ from current Git only by CRLF; MCP: 11/21. Compare raw hashes for artifact identity and normalize solely to diagnose text parity, never to hide v4 schema/rule byte requirements. Do not reuse these package artifacts as a newly validated WP4C distribution build.

## Three candidate minimal assemblies — references only, not generated

Common semantic spine: authority/scope, workspace/version boundary, four envelopes and append facts, lifecycle/attempt evidence, four relations, trusted authorization, create idempotency, recovery/errors. Optional sections are available on demand; omission from initial prompt does not waive any applicable contract.

| Use case | Initial candidate semantic selection | Additional scoped inputs | Explicit exclusions |
| --- | --- | --- | --- |
| Ordinary sequential business task | C1–C8 common spine and ordinary T1–T7; no Branch-specific worked examples | Adopted authorization Profile as needed; chosen Host entry | Engineering constitution, maintainer SOP, GAL/runtime timers, historical logs, fixed product roles |
| Parallel Branch task | Common spine + Branch depth/root-active rules, terminal evidence, canonical family digest/convergence and family lock | Root/Branch task context and trusted Profile | Git branch/merge as Core, product scheduler, EVAL orchestration, automatic archive |
| FCoP source-development task | Common spine plus applicable Branch semantics; fixed taskbook/scope/Gate; repository development manual | Constitution only AFTER separate source/effect/license freeze; selected Host | Automatically distributing development rules to ordinary downstream workspaces |

Sizing reference, **not generated module sizes**: measuring frozen English clause blocks from each F4 ID to the next, sequential baseline excludes seven Branch-specific clauses F4.5.3/F4.5.4/F4.6.4–F4.6.8 and retains 66 blocks = 22,724 bytes (~5,681 byte/4 tokens). Full Branch reference is 73 blocks = 25,727 bytes (~6,432). Blocks include intervening headings/tables; this is an upper-content reference slice, not a proposed minimal instruction rewrite. General family-lock obligations still apply whenever operation scope requires them.

Development reference begins with the same 25,727 bytes; taskbook/manual/Host/Profile sizes depend on later adopted inputs and are **not yet budgeted**. The 7,517-byte common role workflow is not the engineering constitution. The constitution discussion source is not permitted to be appended to an execution prompt or installation during this audit. No final KiB target, model-specific tokenizer budget or safe truncation rule is frozen here.

## Resolution boundary

The underlying scope conflict is resolvable by classification and later version/audience-aware distribution, without changing C1–C8. Ordinary business Agents and developers have separate loading contracts. The baseline is now measured; Host consumption remains honestly unverified. After report delivery, stop and request only WP4C_0_BASELINE_ACCEPTED.
