# FCoP 4.0 Rule Distribution Contract

Status: candidate for ADMIN freeze; version `1.0-candidate.1`; NOT implemented, adopted or released.

Authority: [WP4C.1a](https://github.com/joinwell52-AI/FCoP/blob/7f973dc5f32bc6b9e1076184d1247c55a1349bd5/taskbooks/fcop-4.0/WP4C.1a/01-Core-Relation-Set-and-Sequential-Assembly-Correction-Taskbook-v1.0.zh.md), resuming the unchanged requirements of WP4C.1. The [Chinese counterpart](rule-distribution-contract.zh.md) has identical clause IDs. Frozen [Core](../../spec/fcop-4.0-spec.md) at `aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6` is not amended. The [decisions and complete mappings](../../reports/FCOP-4.0-WP4C.1-CONTRACT-DECISIONS.md) are integral contract schedules; the [verification matrix](../../reports/FCOP-4.0-WP4C.1-CONFORMANCE-MATRIX.md) defines future observable checks, not implemented tests.

## Authority and audiences

### RD-01 — Authority

MUST/MUST NOT denote requirements of this distribution contract, not additions to Base C1–C8. English and Chinese MUST agree in obligation, field, error and Gate semantics. Conflict with frozen Specification MUST stop distribution and require ADMIN disposition; installed rules, Host entries, tests and legacy commentary cannot override it. This document becomes frozen only upon ADMIN signing `WP4C_1_RULE_DISTRIBUTION_CONTRACT_FROZEN`; it supplies no automatic next-stage execution, migration, merge or release authority.

### RD-02 — Scope

A Rule Package MUST contain only traceable guidance for using frozen FCoP. It MUST NOT execute work, decide business completion, grant lifecycle authority, select models, or own sessions/scheduling. Nine semantic modules, one editable artifact per module/language and thin derived Host outputs replace neither Core nor the Toolkit. No database, daemon, watcher, background updater, remote rule service or second Runtime is permitted. Files and short explicit operations are sufficient.

### RD-03 — Audience isolation

Ordinary business guidance, FCoP repository development guidance, and external engineering constitutions MUST be separate. Development guidance belongs under the reserved repository-only `docs/fcop-4.0/development/` namespace with an explicitly selected development entry; neither its body nor an external constitution enters ordinary assemblies, default wheel business guidance or default MCP responses. This namespace reservation does not create that manual now. A future independent constitution needs ADMIN-fixed identity, rights and adoption; absence is allowed and MUST NOT be filled by CodeFlowMu RC. The CodeFlowMu `v1.0-rc.1` digest `87cf212d1cb75cefd0da6da7e5f0f4c7eaedbc231c784b985c3e2e51856abc4c` is excluded as source, authority, dependency, copy, translation, bundle and projection. Earlier discussion-draft principle mappings are historical audit evidence, not a source for this contract.

## Canonical modules

### RD-04 — Identities and primary ownership

Reserve `src/fcop/rules/_data/v4/manifest.json` and `src/fcop/rules/_data/v4/{module_id}.{language}.md`, with `language` exactly `en` or `zh`. These are future package artifacts, not files created by WP4C.1a. Keep all nine modules; do not introduce a catch-all or product domain. The 73-row decision schedule assigns each whole frozen clause exactly one primary module, including its tables/examples. Secondary modules cite that owner instead of copying its obligation. Shared terms may be named without duplicating normative paragraphs. Every normative module paragraph MUST cite at least one owned frozen clause; nonnormative examples MUST be labelled and cannot invent gates.

| module_id | Unique responsibility | depends_on | load_order |
| --- | --- | --- | --- |
| workspace | Declaration, identity, path/encoding safety | [] | 10 |
| envelopes | Four formal files, append facts, ordinary REPORT heads | [workspace] | 20 |
| relations | Four relation fields, direction, strength, cardinality, resolution | [workspace,envelopes] | 30 |
| authorization | Durable authorization, trusted adopted Profile, single use | [workspace,envelopes,relations] | 40 |
| idempotency | Create TASK identity, normalized digest, durable retry | [workspace] | 50 |
| recovery | Atomicity, five recovery observations, receipts, family linearization | [workspace] | 60 |
| lifecycle | NOW/PAST, T1–T7, attempts and ordinary evidence gates | [workspace,envelopes,relations,authorization,idempotency,recovery] | 70 |
| compatibility | Authority/layer limits, errors, version isolation and conformance boundaries | [workspace] | 80 |
| convergence | Branch admission/depth, family REPORTs/digest, Root convergence/T7 | [workspace,envelopes,relations,authorization,idempotency,recovery,lifecycle,compatibility] | 90 |

`compatibility` owns F4.0, layer exclusions, F4.10, F4.11 and release/conformance boundary clauses because all prevent projecting a different contract into the selected version; it does not own development SOP. `recovery` owns F4.9.5 for shared physical linearization; `convergence` cross-references it. Ordinary REPORT head remains in `envelopes`; convergence cites it for Branch heads. This keeps the dependency graph acyclic without omitting common evidence.

### RD-05 — Exact relations

The machine-readable Core relation set is:

```json
["parent","branch_of","subject_ref","references"]
```

| Field | Source → target | Strength/cardinality | Normative source |
| --- | --- | --- | --- |
| parent | TASK → TASK | Strong delegation/hierarchy; not concurrent Branch | F4.5.1 |
| branch_of | TASK → Root TASK | Strong; at most one | F4.5.1 |
| subject_ref | REPORT/ISSUE/REVIEW → TASK or workspace | Strong; exactly one; workspace ISSUE uses workspace:<workspace_id> | F4.5.1 |
| references | Any envelope → existing envelope | Weak citation; mandatory when a gate uses it | F4.5.1–F4.5.2 |

Missing/dangling/cross-workspace/cyclic/non-unique strong relations Fail Closed with `RELATION_INVALID`; ordinary unresolved weak references produce `REFERENCE_UNRESOLVED`, and gate use rejects. No additional cardinality is invented for parent or references. F4.5.3–F4.5.4 are owned by convergence (sibling-only depth, unambiguous active Root admission), not duplicated in relations. F4.5.5 remains relations' boundary: thread_key is Profile/Legacy. `blocks`, `relates_to`, `supersedes` MUST NOT be Base relation names, aliases or implicit gate encodings. Their evidence-backed historical dispositions are in the decision schedule.

### RD-06 — Canonical bytes and bilingual artifacts

Each module artifact MUST be strict UTF-8, no BOM anywhere, LF only, exactly one final LF, and no C0 control characters except TAB/LF or DEL. Reserved projection-marker lines from RD-13 MUST NOT appear in artifact bodies. Hash exact bytes, never normalize before acceptance. Both languages share module_id, owned clause set, dependencies, audience and selection semantics; they have separate source paths, sizes and hashes. Distribution MUST NOT machine-translate, hand-patch a projection or use language fallback silently. Semantic parity is reviewed in addition to machine ID parity. Package version identifies fixed bytes; changed bytes require a new package version/Manifest and explicit adoption, never mutable latest.

## Distribution Manifest

### RD-07 — Shape and fields

Manifest is strict UTF-8/no-BOM/LF JSON; duplicate keys, unknown schema/fields and invalid types reject. Exact top-level shape is `manifest_schema`, `protocol_version`, `package_version`, `artifacts`; no rule text. `manifest_schema` is `fcop-rule-distribution/v1`; `protocol_version` is `4.0`; `package_version` is an exact nonempty version string (no ranges/latest); `artifacts` contains exactly 18 records, nine modules × two languages. Each record has exactly these fields:

| Field | Type / constraint |
| --- | --- |
| module_id | One of RD-04's nine IDs |
| source_path | Relative POSIX path from manifest directory, exactly module_id.language.md |
| language | en or zh |
| sha256 | 64 lowercase hex; entire artifact bytes |
| size_bytes | Nonnegative integer; exact byte count |
| normative_clause_refs | Unique F4 clause ID array; exactly the primary schedule for this module |
| depends_on | Unique module ID array; exactly RD-04 |
| load_order | Integer from RD-04, identical in both languages |
| audience | business-agent; never repository-developer text |
| required_when | common for eight base modules; branch-family for convergence |
| conflicts_with | Unique module ID array; [] for this nine-module version |

No adoption status, Host consumption, timestamp, absolute path, random value or running-process field is permitted. Exact Manifest bytes are hashed externally; Manifest MUST NOT contain its own hash. Git/package raw bytes MUST match; CRLF-normalized equality is diagnostic only.

### RD-08 — Validation and deterministic selection

Validate the entire Manifest and all artifact identities/parity, then resolve the explicit assembly/languages/profile. Reject missing/duplicate artifacts, unknown IDs, unsupported values, hash/size drift, paths outside the package, symlink escapes, cycles or conflicts before effects. A dependency absent from explicit selection is an error, not silent loading. Selected modules are dependency-valid and ordered by load_order then module_id by Unicode code point; language order follows the explicit selected_languages array. Artifact array order and directory enumeration MUST NOT affect outputs. Pure selection reads no network, executes no predicates or caller-supplied policy code and never installs an authorization evaluator.

## Workspace adoption and deployment evidence

### RD-09 — Adoption receipt

Adoption is an explicit ADMIN-authorized local selection, not an installation side effect. Reserve immutable `fcop/internal/rule-distribution/adoptions/<sha256>.json`, where the filename hashes complete receipt bytes. Receipt is a Toolkit distribution fact, not an envelope, Core operation receipt or NOW source. The exact minimal field contract is:

| Field | Type / meaning |
| --- | --- |
| receipt_schema | fcop-rule-adoption/v1 |
| workspace_id | Valid current workspace identity; binds this receipt |
| protocol_version | 4.0; must agree with workspace and Manifest |
| rule_package_version | Exact selected package version |
| rule_manifest_sha256 | Exact Manifest bytes identity |
| assembly_id | sequential or parallel; development uses RD-19's separate reference bundle |
| selected_modules | Unique ordered module IDs, exactly RD-17/RD-18 |
| selected_languages | [en] or [zh]; multiple only when the pinned Host profile explicitly allows |
| selected_host_profile | Object with host_id, profile_version, sha256 of exact static profile bytes |
| target_paths | Ordered unique workspace-relative POSIX paths matching profile |
| adopted_by | Reference to explicit ADMIN selection evidence; never proof by actor label alone |
| adopted_at | Timezone-aware adoption time; receipt only, never output input |
| previous_receipt_ref | null for first adoption, otherwise relative path plus sha256 of previous receipt |

Missing receipt MUST NOT turn existing Host files into adopted artifacts. Adoption evidence does not confer lifecycle authorization or prove successful deployment. An unresolved ADMIN decision, incompatible workspace version or invalid chain rejects; never migrate or relabel a v3 workspace during adoption. There is no mutable global adoption registry.

### RD-10 — Deployment receipt and rollback

After verified target writes, append an immutable distribution receipt under `fcop/internal/rule-distribution/deployments/<sha256>.json`. Required fields: `receipt_schema=fcop-rule-deployment/v1`, `adoption_receipt_ref` (path+hash), `manifest_sha256`, `host_profile_sha256`, `action` (deploy or rollback), `previous_deployment_ref` (null or path+hash), `targets` and timezone-aware `recorded_at`. Each target records `path`, `before_sha256` (null for absent), `after_sha256`, `managed_region_sha256`, and `backup_ref` (null only for previously absent target). Backups are immutable relative-path byte snapshots with hash; no credentials or absolute machine paths. This receipt records observed materialization, never Runtime consumption. Timestamp does not enter projection bytes.

Rollback MUST be explicitly requested, use the immediately previous adopted receipt with verified Manifest/profile/artifact/backup hashes, compare current targets to the last successful deployment, preserve user regions and restore exact recorded bytes (or remove only a proven newly created, unchanged managed-only target). Drift, missing backups or ambiguous history stop without deletion/overwrite. Rollback appends new adoption/deployment evidence referencing history; it does not rewrite old receipts, move lifecycle TASKs or restore an arbitrary version by label.

## Host profiles and deterministic output

### RD-11 — Static profile fields

A Host profile is a pinned static JSON input, not discovery or admission machinery. Fields are exactly:

| Field | Type / constraint |
| --- | --- |
| host_id | codex, cursor or claude-code |
| profile_version | Exact version string; any change requires a new version and adoption |
| supported_entry_kinds | Array of markdown and/or cursor-mdc |
| reference_mode | none or relative-path; latter only after isolated support evidence |
| projection_mode | reference or bounded_embed; reference requires relative-path |
| target_paths | Ordered unique relative paths from RD-12 |
| preserve_regions | Exact begin/end marker pairs, one managed block per target; outside bytes remain user-owned |
| max_projection_bytes | Positive integer cap on full resulting target bytes, including preserved bytes |
| encoding | UTF-8-no-BOM |
| newline | LF |
| languages | Explicit ordered en/zh array; candidate profiles select one language |

No model/subagent/binary/authentication/permission probing or arbitrary hooks. Separate observations `adapter_supported`, `admin_adopted`, `entry_generated`, `runtime_consumption_verified` MUST each carry their own evidence (or unknown); none implies another. A profile is not an authorization Profile evaluator. Hash pinning proves identity, not trust or actual Host consumption.

### RD-12 — Three candidate profiles

These are design targets, NOT existing support/consumption claims. Initial profile version `1.0-candidate.1` uses bounded_embed, reference_mode=none, one explicitly chosen language, and max_projection_bytes=65536. The cap is a contract safety limit, not a measured Host limit; overflow rejects and never removes obligations. Changing it requires reviewed profile revision, not a runtime override. A future reference profile has a distinct version, reference_mode=relative-path and cap=8192, and requires isolated evidence of resolution/order/integrity/failure before adoption. No reliable file-reference behavior is presumed for any of the three today.

| host_id | supported_entry_kinds | target_paths | Candidate policy |
| --- | --- | --- | --- |
| codex | [markdown] | [AGENTS.md] | One managed selected-language entry |
| cursor | [cursor-mdc] | [.cursor/rules/fcop-v4.mdc] | One selected-language entry; no AGENTS alternative simultaneously |
| claude-code | [markdown] | [CLAUDE.md] | One managed selected-language entry |

Unknown Host MUST return typed-unavailable without generation. These target paths never authorize replacing existing legacy or product-owned content. An occupied legacy root entry requires explicit separately authorized ownership/version transition; this contract authorizes no existing-workspace migration. Candidate Cursor profile cannot coexist as an adopted v4 profile with active legacy FCoP mdc inputs.

### RD-13 — Common deterministic framing

Projection is a pure function of exact Manifest, selected artifact bytes, static profile, explicit assembly/languages and existing preserved target bytes. Output MUST NOT contain generation time, absolute machine paths or randomness. UTF-8/no-BOM/LF validation precedes planning; invalid preserved bytes stop, not normalize silently. Begin/end markers are exactly `<!-- fcop:v4:begin -->` and `<!-- fcop:v4:end -->` on separate lines. Interior starts with one line `<!-- fcop:package=<package_version>;manifest=<sha256>;host=<host_id>@<profile_version>;assembly=<assembly_id>;language=<language> -->`. One LF follows every framing line. All inserted identifiers MUST reject control/markup delimiters. Package/profile identity is not supplied by untrusted rule prose.

New markdown file consists of this managed block and final LF. Existing marked file replaces only the inclusive managed block; every outside byte is preserved and included in the size/diff comparison. Missing/duplicate/nested markers or unowned content at an intended new target stop. New cursor-mdc starts with exact lines `---`, `description: FCoP 4.0 selected guidance`, `alwaysApply: true`, `---`, blank line, then the block; frontmatter is managed whole-file metadata and requires a matching previous receipt before update. Existing arbitrary Cursor frontmatter is not inferred owned. Selecting a profile explicitly is required before any alwaysApply output is materialized.

For an explicitly reviewed multi-language profile, the header language value is the comma-joined selected_languages array with no spaces; each artifact frame/link still names one language. Iterate modules first, languages second. The initial three profiles remain single-language. Static profile JSON rejects duplicate keys/unknown fields; preserving a region never licenses treating a marker alone as ownership proof: its prior receipt and managed-region digest must match.

### RD-14 — reference

Within the RD-13 block, reference mode writes one ordered Markdown link per selected artifact: `- [<module_id>:<language>](<relative-path>) sha256=<sha256>` followed by LF, then the end marker. Paths resolve from the target's containing directory to an immutable workspace-local snapshot `fcop/internal/rule-distribution/packages/<manifest-sha256>/` containing the exact Manifest and all 18 artifacts for complete identity validation; only selected artifacts are referenced or consumed. Links use POSIX separators; only the deterministic relative parents needed to reach that in-workspace directory are allowed, never an escape outside workspace. Snapshot bytes MUST be checked before deployment and each later explicit verification. No remote/download link, machine package-install path or unresolved reference is allowed. Loader/reference behavior and changes after deployment require separate Host evidence; entry creation itself proves no Runtime verification.

### RD-15 — bounded_embed

Within the common block, concatenate ordered selected artifacts. For each: write `<!-- fcop:module=<module_id>;language=<language>;sha256=<sha256> -->` plus LF, then its exact canonical bytes (already ending in exactly one LF), then one extra LF; finish with the end marker and LF. No summarization, translation, dropping history by heuristic, duplicated authoring or byte normalization occurs during projection. Relative source links MUST be authored against a declared packaged reference base and validated for the selected target; unresolved or relocated links stop, not silently point elsewhere. A future module author may use pinned authoritative links, but projection never invents content. Limit overflow in either mode returns an error, never an automatic mode switch, language switch or truncated module.

### RD-16 — Plan, ownership and partial failure

Every effectful operation MUST first offer a no-write dry-run listing exact selection, source/profile hashes, before/after target hashes, per-target diff, byte totals, ownership conflicts and planned backups/receipt. No mkdir, snapshot, backup or receipt in dry-run. Before first write validate all inputs/targets, ensure explicit adoption authorization, then recheck the plan's before hashes immediately before replacement; stale plans reject. Serialize only the short distribution commit for overlapping targets using local file coordination; do not lock Agent work or introduce a service.

Stage each target in its own directory, persist bytes, verify, then atomically replace; never archive-away before a durable replacement. Preserve verified old bytes before replacement. A set of files is NOT claimed atomically committed as a group. After any partial failure, preserve staged/backup/evidence bytes, do not append a success receipt, report exactly which writes are proven and stop for explicit inspection/rollback. Do not guess that missing receipt means no write occurred. No background replay or new lifecycle state machine; this is bounded Toolkit deployment failure handling, not reuse of Core authorization or NOW receipts. WP4C.4 must demonstrate failure at each materialization boundary.

## Assemblies and compatibility

### RD-17 — sequential

Exact ordered selected_modules:

```json
["workspace","envelopes","relations","authorization","idempotency","recovery","lifecycle","compatibility"]
```

This is the common ordinary-task guidance, including relations, ordinary attempts/REPORT heads, authorization and T1–T7. It MUST NOT load convergence or enable Branch family/digest/Root convergence operations. Knowing the branch_of vocabulary or mentioning a REVIEW kind grants no Branch capability. Applicable Core validation is never waived by context selection: a Branch/family operation in this assembly is unavailable until explicit parallel adoption; do not try the operation with partial guidance. Authorization Profile adoption is separate; profiles=[] does not become able to finish T4–T7 because guidance loaded. No development manual, constitution, fixed roster, GAL or scheduler enters this assembly.

### RD-18 — parallel

Exact ordered selected_modules:

```json
["workspace","envelopes","relations","authorization","idempotency","recovery","lifecycle","compatibility","convergence"]
```

The only increment over sequential is convergence. Explicit selection is required; installation never enables parallel work. Branch operations retain ordinary gates and authorization, then add frozen admission/depth/family digest/convergence/terminal checks. Core Branch is not Git branch/merge. No duplicated relation obligations or independent Branch state machine is permitted.

### RD-19 — repository-development

This assembly is a repository-only ordered reference bundle, not a tenth business module: (1) FCoP development entry; (2) independently maintained FCoP development guidance; (3) fixed current FCoP contracts; (4) current TASK and authorized scope/Gates. References MUST pin path, revision and hash; an optional independently ADMIN-adopted general constitution may precede them only after rights/source/adoption resolution. No current such constitution is assumed. If the development task also uses protocol collaboration it explicitly selects sequential or parallel as a separate business package; this does not inject development content into that package. No full new development manual, Host entry or implementation is written in this stage.

### RD-20 — Legacy isolation

Keep existing `src/fcop/rules/_data/` non-v4 sources and their APIs in Legacy scope. v4 modules cannot overwrite them or the four old Host outputs. Unversioned old redeploy calls retain 3.x behavior; explicit v4 workspace version, Manifest and adopted Host profile are required for v4 distribution, with no fallback to legacy writer. Existing workspaces are not automatically migrated, all Hosts are not automatically generated and no latest package is fetched. Reconstructible legacy outputs/compatibility tests remain a later acceptance requirement; historical body/version/CRLF differences MUST remain documented rather than called identical or repaired by inflating legacy files.

### RD-21 — MCP and Relay

Future version-selected `fcop://rules` returns package Manifest or typed-unavailable; `fcop://protocol` returns specification identity, not Host state. Selected read-only guidance reads validated modules by workspace version and explicit selection. Legacy resources retain their version contract. Resource reads MUST NOT adopt, deploy, write receipts, install Profile evaluators or migrate. MCP delegates parsing/hash/selection/write algorithms to Toolkit/Project without copies. Relay is optional transport with no rule authority/updater. Accepted WP4B implementations, 46 tools, 11 static resources and three templates are unchanged here; frozen F4.11.3's historical 45 is not silently edited.

### RD-22 — Typed failures

Distribution failures are Toolkit errors, not new Base errors. Reserve these explicit namespaced categories with structured `code`, `operation`, `subject_ref` and safe details: `toolkit:RULE_MANIFEST_INVALID`, `toolkit:RULE_ARTIFACT_MISMATCH`, `toolkit:RULE_SELECTION_INVALID`, `toolkit:RULE_HOST_UNAVAILABLE`, `toolkit:RULE_PROJECTION_LIMIT`, `toolkit:RULE_OWNERSHIP_CONFLICT`, `toolkit:RULE_ADOPTION_REQUIRED`, `toolkit:RULE_DEPLOYMENT_RECOVERY_REQUIRED`. They respectively cover malformed/unsupported schema or graph; missing/invalid/drifting bytes or references; unknown/conflicting/incomplete selection; unsupported/unproven Host mode; size overflow; target drift/ownership/markers; missing or invalid selection authority/receipt; uncertain partial write or rollback evidence. Errors MUST NOT substitute or reinterpret frozen Base errors if Core itself fails. Reject-before-write cases produce zero project writes. Failure reports expose no credentials; text alone is not a machine contract. Existing MCP typed-unavailable stays unchanged until separately authorized integration.

## Staged acceptance

### RD-23 — Evidence and future ownership

The decision schedules account for 73 clauses, 147 contiguous legacy units, 86 paths, 12 consumers, four outputs and all baseline collision/encoding/cache/artifact findings. A future owner is a single implementation/verification stage, not present permission to edit. Reconstructing 3.x and raw v4 package parity, process/getter/index/deployment/Host invalidation, context bytes and unknown Runtime consumption remain explicit future acceptance work. Reference Mode MUST NOT be accepted by a file-existence or API-surface-only test.

### RD-24 — Phase Gates and stop

| Stage | Sole responsibility | Gate requested after that separately authorized stage |
| --- | --- | --- |
| WP4C.2 | First-failing distribution/assembly/drift/conflict/rollback tests | WP4C_2_DISTRIBUTION_CONFORMANCE_ACCEPTED |
| WP4C.3 | Canonical v4 modules, Manifest loader and three minimal assemblies | WP4C_3_RULE_PACKAGE_ACCEPTED |
| WP4C.4 | Thin Host projection, explicit deployment, receipts and rollback | WP4C_4_HOST_PROJECTION_ACCEPTED |
| WP4C.5 | Read-only MCP guidance, 3.x compatibility, FCoP and CodeFlowMu read-only shadow | WP4C_5_COMPATIBILITY_ACCEPTED |
| WP4C.6 | Cross-platform/artifact/context and complete closure | WP4C_RULE_DISTRIBUTION_ACCEPTED |

These are candidate distribution-contract Gate identifiers, not existing signed receipts or taskbooks. Each stage needs its own fixed ADMIN authorization and previous acceptance; no automatic continuation. This stage only requests `WP4C_1_RULE_DISTRIBUTION_CONTRACT_FROZEN`. Any P0, source/spec conflict, unmapped primary clause, bilingual mismatch, requirement for out-of-scope modification or excluded authority MUST stop with factual reports, not a Gate request. No WP4C.2 work, main merge or publication is authorized here.
