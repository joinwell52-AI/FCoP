# WP4C.0 Rule Disposition — BLOCKED

- Repository: `joinwell52-AI/FCoP`
- Gate / audited tree: `aad88ae5f1112881545d30c9938739e83481516d`
- Taskbook commit: `962b67d89e137c26440291d3a48fc7aea1cfebb6`
- Taskbook: [fixed WP4C.0 authority](https://github.com/joinwell52-AI/FCoP/blob/962b67d89e137c26440291d3a48fc7aea1cfebb6/taskbooks/fcop-4.0/WP4C.0/01-Rule-Distribution-Host-Assembly-and-Development-Context-Baseline-Audit-Taskbook-v1.0.zh.md)
- Taskbook SHA-256: `c8c4cb26708a480a6793d88c21511b103f140021c3827c9977b076dfed748e55`
- Scope: `WP4C_0_ONLY`; report state: `BLOCKED`.

## Stop decision

`ENGINEERING_CONSTITUTION_SOURCE_UNRESOLVED` is one confirmed P0 blocker, not an exhaustive count of all possible conflicts. Taskbook sections 3 and 14 require an identifiable authority file, version, digest, license and acquisition method for 《Agent 原生软件工程宪法》. Those cannot be established from the supplied fixed inputs. Section 14 permits factual BLOCKED reports but prohibits requesting the acceptance Gate.

No replacement constitution is authored, downloaded or adopted. The audit stopped at this prerequisite; remaining audit obligations are explicitly incomplete. `REQUESTED_GATE: NONE`; WP4C.1 is not started.

## Coverage ledger

| Required mapping | Completed rows | Required denominator | Status |
|---|---:|---|---|
| Frozen EN clause → candidate semantic module, with ZH cross-check | 0 | NOT_ESTABLISHED | NOT_COMPLETED |
| Canonical 3.x active rule → disposition | 0 | NOT_ESTABLISHED | NOT_COMPLETED |
| Per-unit authority / normative / Host / downstream fields | 0 | NOT_ESTABLISHED | NOT_COMPLETED |

No new candidate module, normative rule, disposition or contract is proposed. In particular, no misc/other/temporary fallback module is introduced. Zero completed rows is not 0/0 coverage and is not evidence that the source contains no rules. The 42 search-hit lines in the Baseline report are authority-discovery evidence only, not a substitute denominator.

## Separation maintained

| Content class | Taskbook boundary | Audit conclusion |
|---|---|---|
| FCoP 4.0 protocol guidance | Traceable projection of the frozen specification; ordinary downstream use. | Clause mapping remains unperformed. |
| FCoP repository development manual | FCoP source-development audience only. | Full authority/content inventory remains unperformed. |
| Agent-native software engineering constitution | Independently fixed authority, digest and license; development only. | SOURCE_UNRESOLVED; no adopted artifact established. |
| Legacy team constitution | Existing team roles/operating-rules pattern. | Name similarity does not establish identity with the engineering constitution. |

## Section 9 contract-question register

These are outstanding questions, not WP4C.1 decisions.

| # | Subject | Result |
|---:|---|---|
| 1 | Reuse data directory versus v4 namespace | NOT_AUDITED |
| 2 | Package inventory versus workspace adoption receipt | NOT_AUDITED |
| 3 | Module identity / dependency / selection / ordering fields | NOT_AUDITED |
| 4 | Canonical module bytes and digest rules | NOT_AUDITED |
| 5 | Host-profile inputs and ADMIN adoption evidence | NOT_AUDITED |
| 6 | Pointer / embedding / compiled Host entry | NOT_AUDITED |
| 7 | Bounded projection for Hosts without references | NOT_AUDITED |
| 8 | Development versus downstream physical isolation | NOT_AUDITED |
| 9 | Constitution reference / snapshot / vendoring license and updates | BLOCKED: source, version, digest and license unresolved |
| 10 | Legacy redeploy compatibility and explicit v4 selection | NOT_AUDITED |
| 11 | Downstream-owned content conflict handling | NOT_AUDITED |
| 12 | Deployment staging / atomic replacement / receipt boundary | NOT_AUDITED |
| 13 | rules / protocol read-only resource object | NOT_AUDITED |
| 14 | Toolkit / Profile versus Rule Core boundary | NOT_AUDITED |
| 15 | P0 conflicts before WP4C.1 | One confirmed prerequisite blocker; full conflict audit incomplete |

No frozen specification or rule source was modified. Further mapping requires resolution of the taskbook hard stop, not an assumption that missing authority can be filled in by the executor.

---

# WP4C.0a resume — closed bidirectional classification

Input is `eb086ee43f345a4d93ffb520049dc8af08712d3b`. The BLOCKED record above remains verbatim history. This section completes its formerly unperformed mapping; labels below are audit candidates, NOT generated rules, a frozen module contract, or permission to implement WP4C.1.

## Units and count rules

- Forward denominator: all 73 distinct **F4.x.y** clause IDs in the frozen English specification, in order; Chinese file has the same 73 IDs in the same order and was read against it. Both blobs equal the fixed frozen commit. Tables/examples subordinate to each numbered clause are part of that clause, not extra test IDs.
- Reverse denominator: 147 **contiguous primary-source section units**: 51 in rules and 96 in commentary. Extract H2–H4 headings outside triple-backtick fences and the three bold 9.5.x headings; add preambles; split rules' unheaded version history at line 1170 and upgrade footer at line 1337. Each interval ends immediately before the next row. These intervals partition both entire texts without gaps. A section containing subordinate bullets carries them all; notes identify mixed semantics explicitly. Empty/container headings and bilingual repetitions are counted as structural units, not invented independent behavior contracts.
- `RULE_INVENTORY: 86/86` counts source/output *paths* in Distribution; `RULE_DISPOSITION: 147/147` counts section units here. Neither count means 147 executable Core requirements. No claim that headings equal atomic assertions.
- Four common role-injection variants are separately accounted below; 34 injected copies inherit those mappings, not 34 new Core rules. Profile biography/catalog files have path-level classifications in Distribution. Historical packaged specs are LEGACY; no new frozen contract is inferred from them.
- Every row has source path/anchor, normative claim, authority, category, module, disposition, Host-specific flag and downstream eligibility. `normative` here means the **old text presents guidance/policy as binding**, not that it has v4 Specification authority. `downstream_required` means semantic eligibility for future v4 guidance after replacement; NEVER load the legacy paragraph verbatim just because this flag is true.
- Source abbreviations: **R** = `src/fcop/rules/_data/fcop-rules.mdc`; **P** = `src/fcop/rules/_data/fcop-protocol.mdc`. Anchors are LF line numbers, not Python splitlines control-character counts. References resolve in the fixed input Git tree.
- Six exhaustive categories: CORE, CATEGORY_MODULE, HOST_ADAPTER, DEVELOPMENT_CONSTITUTION, LEGACY, REMOVE. DEVELOPMENT_CONSTITUTION classifies development-only intent, not adoption of the unlicensed discussion draft. REMOVE means exclude a placeholder from a future active projection, never delete history now. No misc/other fallback.

## Forward mapping — 73/73, EN/ZH parallel

Source for every row: `spec/fcop-4.0-spec.md` at `aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6`; counterpart `spec/fcop-4.0-spec.zh.md` same clause ID. authority=specification, host_specific=false. Candidate domains are semantic addresses only; physical directory, loading selection and digest contract remain ADMIN decisions.

| Clause ID | Candidate semantic domain | Boundary / subject | EN/ZH |
| --- | --- | --- | --- |
| F4.0.1 | core.authority | MUST/MUST NOT are conformance requirements; SHOULD/MAY are recommendations or optional capabilities. | MATCHED |
| F4.0.2 | core.authority | English `spec/fcop-4.0-spec.md` is the primary authority for this candidate. The Chinese parallel `spec/fcop-4.0-spec.zh.md` MUST have the same clause IDs, objects, … (full clause governs) | MATCHED |
| F4.0.3 | core.authority | JSON Schema has machine authority only for structure it can express. This specification governs lifecycle, authorization, concurrency, and recovery behavior. WP2 tes… (full clause governs) | MATCHED |
| F4.1.1 | core.scope | FCoP is a file-native agent behavior-governance protocol: files carry protocol, paths express current state, and events record transition history. | MATCHED |
| F4.1.2 | core.scope | FCoP does not execute work and does not own LLM/tool invocation, hosts, sessions, schedulers, databases, UI, networking, or process management. | MATCHED |
| F4.1.3 | core.scope | Core contains only C1–C8: workspace identity, four envelopes, lifecycle, four relations, evidence and convergence, durable authorization, create idempotency, and rec… (full clause governs) | MATCHED |
| F4.1.4 | core.scope | Fixed roles, EVAL, a Ledger envelope, Git branch/merge, CodeFlowMu work surfaces, BCG, Relay, and online upgrade MUST NOT enter Core. | MATCHED |
| F4.2.1 | core.workspace | The Core declaration of a 4.0 workspace is the UTF-8 JSON file `fcop/fcop.json`. It contains at least: | MATCHED |
| F4.2.2 | core.workspace | `workspace_id` MUST be a canonical lowercase UUID URN and remain stable after creation. Every envelope workspace_id MUST match it or return `WORKSPACE_ID_MISMATCH`. | MATCHED |
| F4.2.3 | core.workspace | `profiles` is a set of adopted Profile identifiers represented as a JSON array. Array order creates no authorization precedence or Core semantics. `profiles: []` is … (full clause governs) | MATCHED |
| F4.2.4 | core.workspace | `workspace_id` is protocol identity, not a global online lock. A backup or read-only mirror MAY retain the ID. The producer of an explicit independent writable fork/… (full clause governs) | MATCHED |
| F4.2.5 | core.workspace | Unsupported protocol, version, and Encoding return `UNSUPPORTED_PROTOCOL`, `UNSUPPORTED_WORKSPACE_VERSION`, and `UNSUPPORTED_ENCODING` respectively. | MATCHED |
| F4.2.6 | core.workspace | One offline workspace cannot prove that no invisible copy exists, and FCoP makes no such guarantee. External single-writer control, synchronized replication, and net… (full clause governs) | MATCHED |
| F4.3.1 | core.envelopes | Formal business envelopes are exactly `TASK`, `REPORT`, `ISSUE`, and `REVIEW`. `shared/` is a knowledge surface. Operation receipts, locks, and indexes are Encoding/… (full clause governs) | MATCHED |
| F4.3.2 | core.envelopes | Every envelope uses UTF-8, LF, YAML frontmatter plus Markdown body and contains `protocol: fcop`, `version: 4`, `type`, its typed ID, `workspace_id`, `sender`, `reci… (full clause governs) | MATCHED |
| F4.3.3 | core.envelopes | REPORT, ISSUE, and REVIEW are append-only facts: once landed they MUST NOT be edited in place or deleted. Corrections, replacements, and revocations create a new env… (full clause governs) | MATCHED |
| F4.3.4 | core.envelopes | A REPORT replacement chain uses `report_kind: final&#124;replacement`. A replacement MUST reference the current head for the same subject/attempt. The valid REPORT is the… (full clause governs) | MATCHED |
| F4.3.5 | core.envelopes | REVIEW kinds include at least `assessment`, `acceptance`, `rejection`, `reopen`, `authorization`, `convergence`, and `repair`. If retained, `mark_human_approved` may… (full clause governs) | MATCHED |
| F4.4.1 | core.lifecycle | An authoritative TASK MUST exist in exactly one of these paths; directory location is the sole NOW truth: | MATCHED |
| F4.4.2 | core.lifecycle | Base has exactly seven legal transitions and the following complete gate matrix: | MATCHED |
| F4.4.3 | core.lifecycle | One command may commit exactly one edge and append one transition. Multi-edge convenience calls MUST split the edges; failure at one edge MUST NOT fabricate later ev… (full clause governs) | MATCHED |
| F4.4.4 | core.lifecycle | `active -> done` is not in 4.0 Base. `finish_task` is 3.x Legacy; a 4.0 workspace MUST reject it with `LEGACY_TRANSITION_NOT_ALLOWED` and MUST NOT bypass T3/T4. | MATCHED |
| F4.4.5 | core.lifecycle | A transition contains `at/from/to/by/tool`; entry into active also contains a new `attempt_id`. For every REPORT or REVIEW consumed by a lifecycle gate, the transiti… (full clause governs) | MATCHED |
| F4.4.6 | core.lifecycle | Archive is terminal. An authoritative TASK MUST NOT move from archive to history or back into lifecycle. v3 history is read-only Legacy; a 4.0 Toolkit may only creat… (full clause governs) | MATCHED |
| F4.4.7 | core.lifecycle | A state edge not listed in §4.2 returns `INVALID_TRANSITION`. For T7, ordinary closure means only: the TASK is in the unique done path, its strong relations are vali… (full clause governs) | MATCHED |
| F4.5.1 | core.relations | Core relations are exactly `parent`, `branch_of`, `subject_ref`, and `references`. | MATCHED |
| F4.5.2 | core.relations | Missing, dangling, cross-workspace, cyclic, or non-unique strong relations return `RELATION_INVALID` and Fail Closed. An unresolved ordinary weak reference produces … (full clause governs) | MATCHED |
| F4.5.3 | core.relations | A Branch branch_of target has no branch_of of its own. A Branch cannot be a Branch Root. All Branches are siblings under one Root; violation returns `BRANCH_DEPTH_EX… (full clause governs) | MATCHED |
| F4.5.4 | core.relations | A Branch may be created only while its Root is unambiguous and active; otherwise return `ROOT_NOT_ACTIVE`. A done Root must first be reopened by authorized T6. | MATCHED |
| F4.5.5 | core.relations | `thread_key` is Profile/Legacy and does not alter the four Core relations. | MATCHED |
| F4.6.1 | core.evidence | Every entry into active (T2/T5/T6) generates a non-reusable `attempt_id` formatted as `urn:uuid:<uuid>` in that transition. The current attempt is the ID on the last… (full clause governs) | MATCHED |
| F4.6.2 | core.evidence | T3 references the unique valid REPORT. Its subject_ref is the TASK and its attempt_id equals the current attempt. A prior-attempt REPORT never satisfies the new gate… (full clause governs) | MATCHED |
| F4.6.3 | core.evidence | T4 references a REVIEW with `review_kind: acceptance` and `decision: approved`. Its subject_ref/attempt_id and referenced REPORT match current state, §7 authorizatio… (full clause governs) | MATCHED |
| F4.6.4 | core.evidence | Branch and ordinary TASK use the same lifecycle and evidence gates. There is no Branch-specific completion state. | MATCHED |
| F4.6.5 | core.evidence | If a Root has Branches, Root T7 executes within one family linearization boundary and verifies all of the following: Root is in the unique done path; Root has no `br… (full clause governs) | MATCHED |
| F4.6.6 | core.evidence | For each Branch, `report_digest` is lowercase SHA-256 of the complete current valid REPORT file bytes after UTF-8/LF validation. `family_digest` is lowercase SHA-256… (full clause governs) | MATCHED |
| F4.6.7 | core.evidence | Convergence references exactly every Branch current valid REPORT and may additionally reference Root's current REPORT. Missing/stale references, references to anothe… (full clause governs) | MATCHED |
| F4.6.8 | core.evidence | Creating a Branch, reopening a Branch, generating a new Branch attempt, or creating a valid replacement REPORT changes the canonical object or a report digest and in… (full clause governs) | MATCHED |
| F4.7.1 | core.authorization | Authorization is carried by an append-only REVIEW, not a fifth envelope. `review_kind: authorization` contains at least: | MATCHED |
| F4.7.2 | core.authorization | A T4 acceptance or T5 rejection REVIEW that contains every authorization binding, including `profile_ref`, and whose issuer proof is evaluated `AUTHORIZED` by that P… (full clause governs) | MATCHED |
| F4.7.3 | core.authorization | Core verifies: the object exists and is REVIEW; `profile_ref` names an adopted Profile; decision, subject, transition, attempt, family, time, reuse, evidence referen… (full clause governs) | MATCHED |
| F4.7.4 | core.authorization | The Profile named by `profile_ref` evaluates the issuer and its proof as exactly `AUTHORIZED`, `DENIED`, or `UNKNOWN`. Only `AUTHORIZED` passes; `DENIED` and `UNKNOW… (full clause governs) | MATCHED |
| F4.7.5 | core.authorization | A consuming transition persists `authorization_ref` and `authorization_digest`. A YAML `sender`, caller-supplied actor, Host allowlist, UI button, or REPORT conclusi… (full clause governs) | MATCHED |
| F4.7.6 | core.authorization | A Profile MAY use local single-user trust, OS ACLs, signatures, or another mechanism, but the mechanism is outside Core. FCoP is a governance and audit protocol and … (full clause governs) | MATCHED |
| F4.7.7 | core.authorization | `profiles: []` remains conformant for T1–T3 and other ungated Base operations. A minimally completable ordinary developer workspace MUST explicitly adopt at initiali… (full clause governs) | MATCHED |
| F4.8.1 | core.create-idempotency | Mandatory 4.0 idempotency is limited to create TASK, including Branch. The lookup key is: | MATCHED |
| F4.8.2 | core.create-idempotency | `operation_id` is 1–128 characters matching `[A-Za-z0-9][A-Za-z0-9._:-]*`. The implementation atomically reserves the lookup key; memory-only deduplication or an unl… (full clause governs) | MATCHED |
| F4.8.3 | core.create-idempotency | Same key/same digest returns `Existing` with original `task_id/path/digest` and creates no file/event. Same key/different digest returns `OPERATION_ID_CONFLICT`. Ope… (full clause governs) | MATCHED |
| F4.8.4 | core.create-idempotency | The create-task digest input is canonical JSON with: `contract="fcop-create-task-v1"`, workspace_id, operation_kind, operation_id, sender, recipient, subject, body, … (full clause governs) | MATCHED |
| F4.8.5 | core.create-idempotency | Physical layout of the durable operation fact is Encoding-defined, but it is auditable, survives restart, and is not a second NOW truth. The result TASK repeats oper… (full clause governs) | MATCHED |
| F4.9.1 | core.recovery | The specification does not claim cross-directory migration has no intermediate state. Every recovery observation is classified as exactly one of `NOT_COMMITTED`, `CO… (full clause governs) | MATCHED |
| F4.9.2 | core.recovery | Destination MUST NOT be silently overwritten. Create-TASK external idempotency may return `Existing` under §8.3. A lifecycle duplicate with matching receipt/digest f… (full clause governs) | MATCHED |
| F4.9.3 | core.recovery | If one TASK appears in multiple authoritative stages, readers return `STATE_AMBIGUOUS` and Fail Closed. They MUST NOT select NOW by mtime, directory order, or event … (full clause governs) | MATCHED |
| F4.9.4 | core.recovery | Internal recovery for every lifecycle transition uses a durable Toolkit/Encoding operation receipt containing operation identity, source/destination paths, normalize… (full clause governs) | MATCHED |
| F4.9.5 | core.recovery | One Root-family linearization boundary covers every write that changes Root lifecycle state, the Branch set, any Branch lifecycle state/current attempt/current REPOR… (full clause governs) | MATCHED |
| F4.9.6 | core.recovery | Lock/receipt/index paths are Encoding/Toolkit detail, not business envelopes. A stale lock MUST NOT be silently deleted by age; if safe release is unprovable, return… (full clause governs) | MATCHED |
| F4.9.7 | core.recovery | Base guarantees cover only supported NTFS/POSIX filesystems with reliable local semantics. Cross-device, network, distributed, or weakly consistent filesystems witho… (full clause governs) | MATCHED |
| F4.9.8 | core.recovery | Base distinguishes three guarantees: | MATCHED |
| F4.9.9 | core.recovery | Logical receipt stages are `PREPARED`, `TARGET_DURABLE`, and `COMMITTED`; physical file names are Encoding-defined. The Base filesystem recovery table is unique: | MATCHED |
| F4.9.10 | core.recovery | A mechanically proven `RECOVERABLE_DUPLICATE` appends/completes only the operation receipt and does not create a business REVIEW. Human disposition for `DIVERGENT_DU… (full clause governs) | MATCHED |
| F4.9.11 | core.recovery | After a lost response from T4/T5/T6/T7, retrying with the same authorization returns the existing committed result when `authorization_ref`, authorization digest, tr… (full clause governs) | MATCHED |
| F4.10.1 | core.errors | The Base 4.0 stable error registry contains exactly these 31 codes: | MATCHED |
| F4.10.2 | core.errors | Errors are machine-recognizable and include operation/subject references; free text is not the sole error contract. | MATCHED |
| F4.10.3 | core.errors | Profile and Toolkit extensions use an explicit namespace and MUST NOT replace, redefine, or change the meaning of any Base error code. | MATCHED |
| F4.11.1 | legacy.compatibility | A v3 workspace is read under v3 until explicit migration. No 4.0 write occurs without §2 declaration. This candidate does not authorize migration. | MATCHED |
| F4.11.2 | legacy.compatibility | `finish_task` and four history tools are `LEGACY_V3_ONLY`. A 4.0 workspace may read history through a Legacy Toolkit; moving an authoritative TASK to history is reje… (full clause governs) | MATCHED |
| F4.11.3 | legacy.compatibility | `fcop` is a reference Toolkit and `fcop-mcp` is an optional Adapter. The 45 existing tools, 11 static resources, and 3 templates are not Core. Retained names dispatc… (full clause governs) | MATCHED |
| F4.11.4 | legacy.compatibility | Branch is expressible as create TASK plus branch_of and requires no new MCP tool. `close_issue` is downstream catalog drift and is not official surface. | MATCHED |
| F4.11.5 | legacy.compatibility | Base MCP should be a thin stdio adapter. Relay is optional (candidate packaging `fcop-mcp[relay]`) and not Core. Upgrade/redeploy/GAL/workspace/session capabilities … (full clause governs) | MATCHED |
| F4.12.1 | development.conformance | Implementations validate workspace boundaries, reject path traversal, use UTF-8/LF, preserve unknown/failure evidence, and do not leak Profile/Runtime credentials. | MATCHED |
| F4.12.2 | development.conformance | WP2 verifies at least one normal, rejection, and applicable concurrency/recovery scenario for every C1–C8, including all six WP0 atomic/Branch scenarios and the WP1.… (full clause governs) | MATCHED |
| F4.12.3 | development.conformance | Conflict among Schema, specification, and tests blocks release; no source silently wins. Every 4.0-conformant implementation satisfies the same observable contract. | MATCHED |
| F4.12.4 | development.conformance | This file is Candidate until `FCOP_4_CONTRACT_FROZEN`; it does not authorize Schema, tests, implementation, migration, push, or release. | MATCHED |


F4.11.3's historical 45-tool baseline is not silently rewritten: ADMIN's accepted WP4B Gate records exactly 46 with reopen_task. It is a Toolkit surface addition, not ninth Core contract. F4.12.4 remains a historical candidate-stage authorization limit; actual Gates are separate signed receipts. English/ZH headings and evidence/authorization/family/recovery tables agree in their audited meaning; no frozen-text edit required.

## Reverse mapping — 147/147

Columns N/H/D respectively encode normative, host_specific, downstream_required as explicit booleans. Source intervals include their own heading and extend through listed end. Normative policy is never promoted solely because a row says true.

| Unit / source lines | Subject | Category | Authority | Candidate module | Disposition | N / H / D | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R-0001 R:1–21 | PREAMBLE / metadata | HOST_ADAPTER | guidance | host.entry | superseded | true / true / false | alwaysApply and v3 version header are legacy deployment metadata; v4 needs explicit selection. |
| R-0022 R:22–40 | 目的 / Purpose | CORE | guidance | core.scope | retained | true / false / true | Keep file-native collaboration intent; solo/team is optional Profile. |
| R-0041 R:41–42 | FCoP 的定位与七大核心概念 / Protocol Position & Seven Core Concepts | CORE | commentary | core.scope | commentary | false / false / true | Architecture introduction, not eight Core contracts. |
| R-0043 R:43–74 | 协议层定位 / Protocol Layer | CORE | commentary | core.scope | retained | false / false / true | Governance not scheduling: F4.1.1–F4.1.4. |
| R-0075 R:75–99 | 七大核心概念 / Seven Core Concepts | LEGACY | commentary | legacy.architecture | superseded | false / false / false | Seven explanatory concepts do not replace C1–C8; Failure/Event vocabulary is legacy. |
| R-0100 R:100–229 | 协议双图对偶 / Two-Diagram Duality | CATEGORY_MODULE | commentary | architecture.evolution | commentary | false / false / false | Preserve attribution and diagrams in optional explanation; no default full diagram injection. |
| R-0230 R:230–231 | Rule 0 · Root Principles / 根原则（三条） | CORE | commentary | core.scope | commentary | false / false / true | Container heading only; requirements are separately mapped below. |
| R-0232 R:232–243 | 0.a · Land it as a File / 必须落文件 | CORE | guidance | core.envelopes | retained | true / false / true | File-backed evidence maps F4.3; no requirement to install MCP. |
| R-0244 R:244–306 | 0.a.1 · 工作流硬约束（不允许"简单任务直接执行"软约束） | CORE | guidance | core.lifecycle | superseded | true / false / true | Use T1–T7 and stop for acceptance; raw shell bypass cannot omit Core validation. |
| R-0307 R:307–323 | 0.a.2 · Hot Path / Cold Path / 热路径与冷路径 | CATEGORY_MODULE | profile | profile.work-planning | profile | true / false / false | Hot/cold workflow useful; parent waits are Profile policy, not Base T7. |
| R-0324 R:324–336 | 0.a.3 · Lifecycle State Is Not Business Completion / 生命周期位置 ≠ 业务完成 | CORE | guidance | core.evidence | retained | true / false / true | Path state is not business success; acceptance requires evidence and authority. |
| R-0337 R:337–347 | 0.a.4 · Main Task / Subtask Governance / 主任务与子任务治理 | CATEGORY_MODULE | profile | profile.work-planning | profile | true / false / false | Parent/subtask policy must not substitute branch_of or create a Base child gate. |
| R-0348 R:348–359 | 0.a.5 · Archive Requires Authorization / 归档需授权 | CORE | guidance | core.authorization | superseded | true / false / true | Archive requires durable REVIEW and trusted adopted Profile, not role name or chat alone. |
| R-0360 R:360–370 | 0.a.6 · REPORT Is Stop Signal / REPORT 即停步信号 | CORE | guidance | core.evidence | retained | true / false / true | REPORT is self-report; no automatic acceptance or archive. |
| R-0371 R:371–388 | 0.b · No Single AI Does Decision-to-Execution Alone / 多角色制衡 | CATEGORY_MODULE | profile | profile.review-separation | profile | true / false / false | Solo proposer/reviewer governance is adopted policy; fixed roles not Core. |
| R-0389 R:389–421 | 0.c · Only Land True Things / 只落真话 | CORE | guidance | core.evidence | retained | true / false / true | Truth/citation principle retained; broader ethics/examples remain explanation. |
| R-0422 R:422–427 | Rule 1 · Two-Phase Startup: Initialize, then Assign / 两阶段启动：先初始化，再指派 | CATEGORY_MODULE | profile | profile.identity | profile | true / false / false | Two-phase role/session startup is not C1 workspace identity. |
| R-0428 R:428–453 | Phase 1 · 未初始化（`fcop/fcop.json` 不存在） | LEGACY | guidance | legacy.initialization | superseded | true / false / false | Five-bucket and automatic Host deploy promises are v1–v3, not v4 init. |
| R-0454 R:454–463 | Phase 2 · 已初始化但未指派（`fcop.json` 存在，本会话无角色） | CATEGORY_MODULE | profile | profile.identity | profile | true / false / false | Role binding policy only; cannot make authorization. |
| R-0464 R:464–501 | 贯穿两阶段的硬约束 | CATEGORY_MODULE | profile | profile.identity | profile | true / false / false | Historical ledger occupancy and subagent seat policy are not Base identity/authentication. |
| R-0502 R:502–532 | Phase 1 · Uninitialized (`fcop/fcop.json` missing) | LEGACY | guidance | legacy.initialization | superseded | true / false / false | EN parallel of phase 1; same legacy-only disposition. |
| R-0533 R:533–540 | Phase 2 · Initialized but unassigned (fcop.json present, no role) | CATEGORY_MODULE | profile | profile.identity | profile | true / false / false | EN parallel of phase 2, not independent Core. |
| R-0541 R:541–584 | Invariants across both phases | CATEGORY_MODULE | profile | profile.identity | profile | true / false / false | EN invariants parallel; no automatic seat/global lock guarantee. |
| R-0585 R:585–614 | Rule 2 · Files Are the Protocol, Folders Are the Organization / 文件即协议，文件夹即组织 | CORE | guidance | core.lifecycle | retained | true / false / true | Files/path principle retained; v4 exact authoritative TASK location F4.4.1. |
| R-0615 R:615–628 | Rule 3 · Metadata Integrity / 元数据完整 | CORE | guidance | core.envelopes | superseded | true / false / true | Four old required keys insufficient for F4.3.2; alias/version remain legacy. |
| R-0629 R:629–652 | Rule 4 · Role Routing / 角色链路 | CATEGORY_MODULE | profile | profile.role-routing | profile | true / false / false | Leader/ADMIN routing not Base. |
| R-0653 R:653–695 | Rule 4.5 · Team Docs Have Three Layers / 团队文档三层结构 | CATEGORY_MODULE | profile | profile.team-documents | profile | true / false / false | Three-layer template organization optional adoption; no fixed Core role roster. |
| R-0696 R:696–745 | Rule 4.6 · Internal vs External Documentation / 内外档案体系（non-mandatory） | CATEGORY_MODULE | commentary | knowledge.organization | commentary | false / false / false | Internal/external soft convention; do not enforce five legacy buckets for v4. |
| R-0746 R:746–770 | Rule 5 · Append-Only History / 历史只增不改 | CORE | guidance | core.append-facts | conflict | true / false / true | TASK transition append differs from blanket immutable TASK; REVIEW is fourth type; F4.3.3 corrections via references. |
| R-0771 R:771–781 | Rule 6 · Reciprocity / 互惠回执 | CATEGORY_MODULE | profile | profile.reply-routing | profile | true / false / false | Reply/thread convention not new Core relation. |
| R-0782 R:782–798 | Rule 7 · Destructive Operations / 破坏性操作 | DEVELOPMENT_CONSTITUTION | development | development.change-control | development | false / false / false | Destructive-operation approval advice; not v4 authorization carrier or frozen constitution. |
| R-0799 R:799–847 | Rule 7.5 · Workspace Convention / 工作区约定（soft convention） | DEVELOPMENT_CONSTITUTION | development | development.workspace | development | false / false / false | Business-code workspace cage cannot forbid FCoP src work; optional non-development workspace convention split. |
| R-0848 R:848–856 | Rule 8.v3 · _lifecycle/ Directory Structure / v3 生命周期目录结构 | LEGACY | guidance | legacy.lifecycle | superseded | true / false / false | v3 context only; v4 lifecycle has seven explicit edges. |
| R-0857 R:857–872 | v3 项目目录布局 / v3 Project Directory Layout | LEGACY | guidance | legacy.layout | superseded | true / false / false | Replace ambiguous project-root layout with F4.4.1 in future v4 guidance. |
| R-0873 R:873–892 | 生命周期状态机 / Lifecycle State Machine | LEGACY | guidance | legacy.lifecycle | conflict | true / false / false | finish/history conflict with v4 T3/T4 and terminal archive; preserve v3 text only. |
| R-0893 R:893–904 | 向后兼容 / Backward Compatibility | LEGACY | guidance | legacy.compatibility | retained | true / false / false | Explicit migration only; no rule deployment silently migrates workspace. |
| R-0905 R:905–915 | Rule 9 · v1.0 Capabilities / v1.0 新增能力（4 抽象） | LEGACY | commentary | legacy.capabilities | commentary | false / false / false | Historical capability container, not v4 Core expansion. |
| R-0916 R:916–948 | 9.1 · REVIEW envelope / 第四类 IPC（Audit 抽象） | CORE | guidance | core.reviews | superseded | true / false / true | Old decisions/human_approval in-place mutation replaced by append-only typed REVIEW. |
| R-0949 R:949–971 | 9.2 · Agent Boundary / Agent 能力边界（Boundary 抽象） | CATEGORY_MODULE | profile | profile.capabilities | profile | true / false / false | Worker/governance/admin tiers cannot supply Core authorization. |
| R-0972 R:972–994 | 9.3 · Failure & Recovery / 失败与恢复（Failure 抽象） | LEGACY | guidance | legacy.failure | superseded | true / false / false | Four failure types/five actions are not C8 five physical states. |
| R-0995 R:995–1015 | 9.4 · Event Model / 事件模型（Event 抽象） | LEGACY | guidance | legacy.events | conflict | true / false / false | In-memory notifications distinct from durable append-only TASK transition events. |
| R-1016 R:1016–1020 | 9.5 · v1.1 Additions / v1.1 新增能力（3 项） | CATEGORY_MODULE | commentary | profile.risk | commentary | false / false / false | Historical risk/skill container. |
| R-1021 R:1021–1038 | **9.5.1 · `Task.risk_level` / 任务风险等级**（per ADR-0024） | CATEGORY_MODULE | profile | profile.risk | profile | true / false / false | Risk tags Profile only and excluded from create digest. |
| R-1039 R:1039–1042 | **9.5.2 · `Review.decision = needs_human` + `human_approval`**（已收入 Rule 9.1） | LEGACY | guidance | legacy.approval | superseded | true / false / false | needs_human/human_approval not v4 trusted authorization. |
| R-1043 R:1043–1057 | **9.5.3 · `Skill.tools[]` 风险元数据**（per ADR-0027） | CATEGORY_MODULE | profile | profile.skills | profile | true / false / false | Tool risk metadata does not grant authority. |
| R-1058 R:1058–1100 | 9.6 · Protocol Inspection / 协议体检（fcop_audit & INSPECTION） | LEGACY | guidance | legacy.inspection | conflict | true / false / false | INSPECTION is diagnostic artifact, not fifth formal v4 envelope. |
| R-1101 R:1101–1140 | 9.7 · Governance Alert Layer / 治理告警层（GAL） | CATEGORY_MODULE | profile | profile.governance-alerts | profile | true / false / false | Independent signals useful, thresholds/runtime alerts outside Core. |
| R-1141 R:1141–1158 | Rule 8 · Rules Take Precedence / 规则优先级 | CORE | guidance | core.authority | conflict | true / false / true | v3 rule-file priority cannot override frozen English v4 spec/ADMIN fixed taskbooks. |
| R-1159 R:1159–1169 | Scope / 适用边界 | CORE | guidance | core.scope | retained | true / false / true | No prescribed model/framework/product architecture. |
| R-1170 R:1170–1336 | Version history (audit split) | LEGACY | history | legacy.rule-history | commentary | false / false / false | Version log is provenance, not a fresh executable instruction. |
| R-1337 R:1337–1359 | Upgrade footer (audit split) | HOST_ADAPTER | guidance | host.upgrade | superseded | true / true / false | Explicit upgrade/redeploy only; no auto-install or implicit migration. |
| P-0001 P:1–39 | PREAMBLE / metadata | HOST_ADAPTER | guidance | host.entry | superseded | true / true / false | BOM before frontmatter survives strip helper; broad host portability is a claim, not verified consumption. |
| P-0040 P:40–78 | Core Principle / 核心原则 | CORE | commentary | core.scope | commentary | false / false / true | File-native convenience philosophy retained; direct file operations must still obey locks, evidence, authorization and receipts. |
| P-0079 P:79–101 | Architectural Principle: Tools are a Convenience Layer / 架构原则：工具是便利层，不是真相层 | CORE | commentary | core.scope | commentary | false / false / true | File-native convenience philosophy retained; direct file operations must still obey locks, evidence, authorization and receipts. |
| P-0102 P:102–123 | Consequence 1 · Every tool decomposes into file operations / 每个工具都必须能拆解成文件操作 | CORE | commentary | core.scope | commentary | false / false / true | File-native convenience philosophy retained; direct file operations must still obey locks, evidence, authorization and receipts. |
| P-0124 P:124–136 | Consequence 2 · No-MCP participation must remain possible / 没装 MCP 的人必须也能参与 | CORE | commentary | core.scope | commentary | false / false / true | File-native convenience philosophy retained; direct file operations must still obey locks, evidence, authorization and receipts. |
| P-0137 P:137–147 | Consequence 3 · Protocol changes affect filename / directory / frontmatter; tool changes affect ergonomics / 协议改动影响命名/目录/frontmatter；工具改动只影响人机工效 | CORE | commentary | core.scope | commentary | false / false / true | File-native convenience philosophy retained; direct file operations must still obey locks, evidence, authorization and receipts. |
| P-0148 P:148–165 | 自校验清单 / Self-check | CORE | commentary | core.scope | commentary | false / false / true | File-native convenience philosophy retained; direct file operations must still obey locks, evidence, authorization and receipts. |
| P-0166 P:166–179 | Two-Diagram Duality / 双图对偶（执行 vs 演化） | CATEGORY_MODULE | commentary | architecture.evolution | commentary | false / false / false | Optional attributed architecture explanation, not eight Core contracts. |
| P-0180 P:180–199 | 为什么是两张图，不是一张 / Why Two Diagrams, Not One | CATEGORY_MODULE | commentary | architecture.evolution | commentary | false / false / false | Optional attributed architecture explanation, not eight Core contracts. |
| P-0200 P:200–227 | 七环节与 ADR-0034 章节映射 / Seven Stages × ADR Sections | CATEGORY_MODULE | commentary | architecture.evolution | commentary | false / false / false | Optional attributed architecture explanation, not eight Core contracts. |
| P-0228 P:228–243 | 引用与扩展 / Citations & Extensions | CATEGORY_MODULE | commentary | architecture.evolution | commentary | false / false / false | Optional attributed architecture explanation, not eight Core contracts. |
| P-0244 P:244–256 | How Rule 4.6 Applies: Internal vs External Document Convention / Rule 4.6 的展开：内外档案体系如何落地 | CATEGORY_MODULE | commentary | knowledge.organization | commentary | false / false / false | Soft internal documentation convention; P3 suggestion is not Base state or authorization. |
| P-0257 P:257–285 | 推荐目录布局 / Recommended Directory Layout | CATEGORY_MODULE | commentary | knowledge.organization | commentary | false / false / false | Soft internal documentation convention; P3 suggestion is not Base state or authorization. |
| P-0286 P:286–336 | `internal-only` 声明语法 v1 / Declaration Syntax v1 | CATEGORY_MODULE | commentary | knowledge.organization | commentary | false / false / false | Soft internal documentation convention; P3 suggestion is not Base state or authorization. |
| P-0337 P:337–364 | 与 Rule 7.5 的镜像关系 / Mirror with Rule 7.5 | CATEGORY_MODULE | commentary | knowledge.organization | commentary | false / false / false | Soft internal documentation convention; P3 suggestion is not Base state or authorization. |
| P-0365 P:365–383 | Audit 行为 / Audit Behaviour | CATEGORY_MODULE | commentary | knowledge.organization | commentary | false / false / false | Soft internal documentation convention; P3 suggestion is not Base state or authorization. |
| P-0384 P:384–391 | How Rule 0.c Applies: Truthfulness on Disk / Rule 0.c 的展开：落盘的必须是真话 | CORE | guidance | core.evidence | retained | true / false / true | Evidence/citation and incoming-file verification; solo reread does not manufacture authorization. |
| P-0392 P:392–411 | 引用格式 / Citation Formats | CORE | guidance | core.evidence | retained | true / false / true | Evidence/citation and incoming-file verification; solo reread does not manufacture authorization. |
| P-0412 P:412–439 | 读入信时的事实审查清单 / Reality Check for Incoming Files | CORE | guidance | core.evidence | retained | true / false / true | Evidence/citation and incoming-file verification; solo reread does not manufacture authorization. |
| P-0440 P:440–460 | Solo 模式下的特例 / Solo Mode Caveat | CORE | guidance | core.evidence | retained | true / false / true | Evidence/citation and incoming-file verification; solo reread does not manufacture authorization. |
| P-0461 P:461–466 | How Rule 0.a Applies: Collaboration Cycle (3.2.5) / Rule 0.a 的展开：协作闭环 | CORE | guidance | core.lifecycle | superseded | true / false / true | Use current attempt, REPORT and authorized acceptance; no self-archive default. |
| P-0467 P:467–479 | 协作闭环 / Collaboration cycle | CORE | guidance | core.lifecycle | superseded | true / false / true | Use current attempt, REPORT and authorized acceptance; no self-archive default. |
| P-0480 P:480–486 | Hot Path vs Cold Path（Rule 0.a.2） | CATEGORY_MODULE | profile | profile.work-planning | profile | true / false / false | Parent work breakdown is not Branch membership or a Base closure gate. |
| P-0487 P:487–492 | 生命周期 ≠ 业务完成（Rule 0.a.3） | CORE | guidance | core.lifecycle | superseded | true / false / true | Use current attempt, REPORT and authorized acceptance; no self-archive default. |
| P-0493 P:493–497 | 归档需授权（Rule 0.a.5） | CORE | guidance | core.authorization | superseded | true / false / true | Replace role-name permission with durable REVIEW plus trusted adopted evaluator. |
| P-0498 P:498–502 | REPORT 即停步（Rule 0.a.6） | CORE | guidance | core.lifecycle | superseded | true / false / true | Use current attempt, REPORT and authorized acceptance; no self-archive default. |
| P-0503 P:503–530 | MCP 工具 docstring 修改范围（3.2.5 / Tool docstring scope） | DEVELOPMENT_CONSTITUTION | development | development.adapter-docstrings | development | false / false / false | 3.2.5 maintainer editing checklist, not downstream business instructions. |
| P-0531 P:531–557 | How Rule 2 Scales: Files + Folders / Rule 2 的展开：文件 + 文件夹 | CORE | guidance | core.lifecycle | superseded | true / false / true | Keep file/path principle; v4 workspace namespace is explicit. |
| P-0558 P:558–639 | Session Startup — UNBOUND Protocol / 会话启动 · UNBOUND 协议 | CATEGORY_MODULE | guidance | profile.identity | conflict | true / false / false | Task-pickup self-binding wording conflicts with explicit assignment in Rule 1; resolve within Profile. |
| P-0640 P:640–649 | Setting / 场景 | CATEGORY_MODULE | profile | profile.identity | profile | true / false / false | Solo/team/roster examples; solo optional-task wording conflicts with Rule 0.a.1; not Core authorization. |
| P-0650 P:650–659 | Project Mode & Identity / 项目模式与身份 | CATEGORY_MODULE | profile | profile.identity | profile | true / false / false | Solo/team/roster examples; solo optional-task wording conflicts with Rule 0.a.1; not Core authorization. |
| P-0660 P:660–686 | `mode:` — Solo vs Team / 独模与团队模 | CATEGORY_MODULE | profile | profile.identity | profile | true / false / false | Solo/team/roster examples; solo optional-task wording conflicts with Rule 0.a.1; not Core authorization. |
| P-0687 P:687–732 | Example A · 4-role team (dev-team) / 四人团队示例 | CATEGORY_MODULE | profile | profile.identity | profile | true / false / false | Solo/team/roster examples; solo optional-task wording conflicts with Rule 0.a.1; not Core authorization. |
| P-0733 P:733–780 | Example B · Solo role (you yourself) / 单角色示例 | CATEGORY_MODULE | profile | profile.identity | profile | true / false / false | Solo/team/roster examples; solo optional-task wording conflicts with Rule 0.a.1; not Core authorization. |
| P-0781 P:781–792 | Solo → Team 迁移推荐做法 / Migrating Solo to Team (recommended recipe) | LEGACY | guidance | legacy.team-migration | superseded | true / false / false | Historical two-file team constitution and log archive recipe; not engineering constitution or authorized migration. |
| P-0793 P:793–850 | 1. 在 `shared/` 落两份团队宪法 / Land a two-file "team constitution" under `shared/` | LEGACY | guidance | legacy.team-migration | superseded | true / false / false | Historical two-file team constitution and log archive recipe; not engineering constitution or authorized migration. |
| P-0851 P:851–924 | 2. 归档旧 Solo 历史 / Archive the old Solo history | LEGACY | guidance | legacy.team-migration | superseded | true / false / false | Historical two-file team constitution and log archive recipe; not engineering constitution or authorized migration. |
| P-0925 P:925–935 | 3. `fcop.json` 不需要记"切换时间戳" / No need to timestamp the switch | LEGACY | guidance | legacy.team-migration | superseded | true / false / false | Historical two-file team constitution and log archive recipe; not engineering constitution or authorized migration. |
| P-0936 P:936–943 | Core Directories / 核心目录 | LEGACY | guidance | legacy.layout | superseded | true / false / false | v2/v3 paths only; no v4 history move. |
| P-0944 P:944–972 | v3 项目布局（当前标准）/ v3 Project Layout (current standard) | LEGACY | guidance | legacy.layout | superseded | true / false / false | v2/v3 paths only; no v4 history move. |
| P-0973 P:973–994 | v2 Legacy 布局（向后兼容）/ v2 Legacy Layout (backward-compatible) | LEGACY | guidance | legacy.layout | superseded | true / false / false | v2/v3 paths only; no v4 history move. |
| P-0995 P:995–1008 | File Naming / 文件命名 | LEGACY | guidance | legacy.naming | superseded | true / false / false | Legacy routing/slug syntax; four v4 types and workspace identity must be validated independently. |
| P-1009 P:1009–1030 | Recipient forms / 收件人的 4 种写法 | LEGACY | guidance | legacy.naming | superseded | true / false / false | Legacy routing/slug syntax; four v4 types and workspace identity must be validated independently. |
| P-1031 P:1031–1103 | Trailing slug (optional) / 可选的尾部 slug（ADR-0033） | LEGACY | guidance | legacy.naming | superseded | true / false / false | Legacy routing/slug syntax; four v4 types and workspace identity must be validated independently. |
| P-1104 P:1104–1159 | Task Format / 任务单格式 | CORE | guidance | core.envelopes | conflict | true / false / true | version 1/kind/related/supersedes examples and REPORT naming cannot serve as v4 envelopes. |
| P-1160 P:1160–1175 | About `protocol:` and `version:` / 关于 `protocol:` 和 `version:` | CORE | guidance | core.envelopes | conflict | true / false / true | version 1/kind/related/supersedes examples and REPORT naming cannot serve as v4 envelopes. |
| P-1176 P:1176–1200 | Subtask Batches / 分包任务 | CATEGORY_MODULE | profile | profile.work-planning | profile | true / false / false | Parent batches are not branch_of; no product workflow in Core. |
| P-1201 P:1201–1222 | Shared Documents / 团队共享知识 | CATEGORY_MODULE | commentary | knowledge.organization | commentary | false / false / false | Shared knowledge is not another envelope; avoid treating prefix conventions as Base. |
| P-1223 P:1223–1230 | Cross-scope Coordination / 跨域协作 | CATEGORY_MODULE | profile | profile.cross-scope | profile | true / false / false | Optional transport/routing policy; no hidden network consistency guarantee. |
| P-1231 P:1231–1259 | `inbox/` and `outbox/` / 收件箱与发件箱 | CATEGORY_MODULE | profile | profile.cross-scope | profile | true / false / false | Optional transport/routing policy; no hidden network consistency guarantee. |
| P-1260 P:1260–1282 | `fcop://` URI routing / URI 路由（可选） | CATEGORY_MODULE | profile | profile.cross-scope | profile | true / false / false | Optional transport/routing policy; no hidden network consistency guarantee. |
| P-1283 P:1283–1307 | Collaboration Rules / 协作规则 | CATEGORY_MODULE | profile | profile.reply-routing | profile | true / false / false | Single driver/thread and log workflow remain adopted/legacy policy. |
| P-1308 P:1308–1312 | GATE Design Pitfalls / GATE 设计陷阱 | DEVELOPMENT_CONSTITUTION | development | development.gate-design | development | false / false / false | Self-collision case and observable evidence checklist, not business Runtime or automatic acceptance. |
| P-1313 P:1313–1338 | Pitfall 1 · GATE 描述自我命中 / Self-collision | DEVELOPMENT_CONSTITUTION | development | development.gate-design | development | false / false / false | Self-collision case and observable evidence checklist, not business Runtime or automatic acceptance. |
| P-1339 P:1339–1342 | Pitfall 2 · TBD（留位） | REMOVE | guidance | development.placeholder | obsolete | true / false / false | TBD placeholder excluded from future active projection; retain original historical bytes. |
| P-1343 P:1343–1355 | GATE 设计自查清单 / GATE Design Self-check | DEVELOPMENT_CONSTITUTION | development | development.gate-design | development | false / false / false | Self-collision case and observable evidence checklist, not business Runtime or automatic acceptance. |
| P-1356 P:1356–1367 | Listing / Reading Tasks / 查询任务 | LEGACY | guidance | legacy.query | superseded | true / false / false | Legacy listing signatures; future v4 guidance must match accepted public APIs. |
| P-1368 P:1368–1401 | Agent Autonomy / Agent 自决权 | CATEGORY_MODULE | profile | profile.autonomy | profile | true / false / false | Within-task autonomy does not authorize role changes or destructive operations. |
| P-1402 P:1402–1814 | Protocol Version Log / 协议版本记录 | LEGACY | history | legacy.protocol-history | commentary | false / false / false | Version chronology preserved but excluded from default runtime context. |
| P-1815 P:1815–1821 | Auto-Patrol / 自动巡检 | CATEGORY_MODULE | profile | profile.patrol | profile | true / false / false | Optional prompted patrol; no new watcher or mandatory business acceptance. |
| P-1822 P:1822–1829 | Trigger / 触发条件 | CATEGORY_MODULE | profile | profile.patrol | profile | true / false / false | Optional prompted patrol; no new watcher or mandatory business acceptance. |
| P-1830 P:1830–1847 | Patrol Actions / 巡检动作 | CATEGORY_MODULE | profile | profile.patrol | profile | true / false / false | Optional prompted patrol; no new watcher or mandatory business acceptance. |
| P-1848 P:1848–1856 | Report Format / 汇报格式 | CATEGORY_MODULE | profile | profile.patrol | profile | true / false / false | Optional prompted patrol; no new watcher or mandatory business acceptance. |
| P-1857 P:1857–1867 | Patrol Rules / 巡检规则 | CATEGORY_MODULE | profile | profile.patrol | profile | true / false / false | Optional prompted patrol; no new watcher or mandatory business acceptance. |
| P-1868 P:1868–1876 | Rule 9 Commentary · v1.0 新增能力的协议解释 | LEGACY | commentary | legacy.capabilities | commentary | false / false / false | Historical v1 capability container. |
| P-1877 P:1877–1934 | 9.1 Commentary · REVIEW 文件命名与 Audit 链 | CORE | guidance | core.reviews | conflict | true / false / true | Old decision enums and in-place human_approval conflict with append-only v4 REVIEW. |
| P-1935 P:1935–1975 | 9.2 Commentary · Boundary 层级与能力检查清单 | CATEGORY_MODULE | profile | profile.capabilities | profile | true / false / false | Role/tier allowlist is not issuer proof. |
| P-1976 P:1976–2006 | 9.3 Commentary · Failure 检测与恢复操作指南 | LEGACY | guidance | legacy.failure | conflict | true / false / false | Old failure schema/action table; BOUNDARY_VIOLATED example also differs from stated four types. |
| P-2007 P:2007–2042 | 9.4 Commentary · Event 订阅与扫描操作指南 | LEGACY | guidance | legacy.events | superseded | true / false / false | EventBus/poll_once optional notifications, not lifecycle NOW or durable transition authority. |
| P-2043 P:2043–2044 | 9.5 Commentary · v1.1 新增能力操作指南 | CATEGORY_MODULE | profile | profile.risk | profile | true / false / false | Risk and skill policy optional; cannot create Core permission or affect create digest. |
| P-2045 P:2045–2069 | 9.5.1 · `Task.risk_level` 使用场景 | CATEGORY_MODULE | profile | profile.risk | profile | true / false / false | Risk and skill policy optional; cannot create Core permission or affect create digest. |
| P-2070 P:2070–2087 | 9.5.2 · `needs_human` + `mark_human_approved` 完整流程 | LEGACY | guidance | legacy.approval | conflict | true / false / false | In-place approval workflow must not be loaded for v4. |
| P-2088 P:2088–2107 | 9.5.3 · `Skill.tools[]` 风险元数据示例 | CATEGORY_MODULE | profile | profile.risk | profile | true / false / false | Risk and skill policy optional; cannot create Core permission or affect create digest. |
| P-2108 P:2108–2111 | 9.6 Commentary · 协议体检与 INSPECTION 报告操作指南 | LEGACY | guidance | legacy.inspection | superseded | true / false / false | INSPECTION file and old tool examples remain Toolkit diagnostic, never fifth envelope. |
| P-2112 P:2112–2122 | 9.6.1 · 三场景使用决策树 | LEGACY | guidance | legacy.inspection | superseded | true / false / false | INSPECTION file and old tool examples remain Toolkit diagnostic, never fifth envelope. |
| P-2123 P:2123–2140 | 9.6.2 · MCP 调用示例 | LEGACY | guidance | legacy.inspection | superseded | true / false / false | INSPECTION file and old tool examples remain Toolkit diagnostic, never fifth envelope. |
| P-2141 P:2141–2151 | 9.6.3 · INSPECTION 报告文件命名与归档 | LEGACY | guidance | legacy.inspection | superseded | true / false / false | INSPECTION file and old tool examples remain Toolkit diagnostic, never fifth envelope. |
| P-2152 P:2152–2157 | 9.6.4 · Execution Block 语义声明 | CATEGORY_MODULE | profile | profile.audit-response | profile | true / false / false | Execution blocks are recommendations, not commands; old audit P0 is not WP4C.0a Gate. |
| P-2158 P:2158–2167 | 9.6.5 · P0 violation 处置原则 | CATEGORY_MODULE | profile | profile.audit-response | profile | true / false / false | Execution blocks are recommendations, not commands; old audit P0 is not WP4C.0a Gate. |
| P-2168 P:2168–2171 | 9.7 Commentary · GAL 治理告警操作指南 | CATEGORY_MODULE | profile | profile.governance-alerts | profile | true / false / false | Self-report not independent evidence; GAL timers/outbox outside Core; decision=done example disagrees with REVIEW enum. |
| P-2172 P:2172–2180 | 9.7.1 · 告警查看流程 | CATEGORY_MODULE | profile | profile.governance-alerts | profile | true / false / false | Self-report not independent evidence; GAL timers/outbox outside Core; decision=done example disagrees with REVIEW enum. |
| P-2181 P:2181–2188 | 9.7.2 · 三类漂移信号触发条件 | CATEGORY_MODULE | profile | profile.governance-alerts | profile | true / false / false | Self-report not independent evidence; GAL timers/outbox outside Core; decision=done example disagrees with REVIEW enum. |
| P-2189 P:2189–2197 | 9.7.3 · FCoP-Rule-G1（协议公理） | CATEGORY_MODULE | profile | profile.governance-alerts | profile | true / false / false | Self-report not independent evidence; GAL timers/outbox outside Core; decision=done example disagrees with REVIEW enum. |
| P-2198 P:2198–2211 | 9.7.4 · 手动归档治理缺口 | CATEGORY_MODULE | profile | profile.governance-alerts | profile | true / false / false | Self-report not independent evidence; GAL timers/outbox outside Core; decision=done example disagrees with REVIEW enum. |
| P-2212 P:2212–2216 | 批量整改授权模式 · Batch Remediation Authorization | DEVELOPMENT_CONSTITUTION | development | development.batch-change | development | false / false / false | Explicit bounded file-list work authorization, not REVIEW-based lifecycle permission. |
| P-2217 P:2217–2222 | 背景 | DEVELOPMENT_CONSTITUTION | development | development.batch-change | development | false / false / false | Explicit bounded file-list work authorization, not REVIEW-based lifecycle permission. |
| P-2223 P:2223–2243 | 机制 | DEVELOPMENT_CONSTITUTION | development | development.batch-change | development | false / false / false | Explicit bounded file-list work authorization, not REVIEW-based lifecycle permission. |
| P-2244 P:2244–2253 | 约束 | DEVELOPMENT_CONSTITUTION | development | development.batch-change | development | false / false / false | Explicit bounded file-list work authorization, not REVIEW-based lifecycle permission. |
| P-2254 P:2254–2259 | Protocol Rule Distribution & Upgrade · 协议规则的分发与升级 | HOST_ADAPTER | guidance | host.distribution | superseded | true / true / false | Four whole-file outputs, no adopted-host selection or durable receipt; package update does not refresh cached process. |
| P-2260 P:2260–2282 | 三处部署，宿主中立 / Three deploy targets, host-neutral | HOST_ADAPTER | guidance | host.distribution | superseded | true / true / false | Four whole-file outputs, no adopted-host selection or durable receipt; package update does not refresh cached process. |
| P-2283 P:2283–2294 | 包升级不会自动改项目文件 / Package upgrade does not auto-upgrade project files | HOST_ADAPTER | guidance | host.distribution | superseded | true / true / false | Four whole-file outputs, no adopted-host selection or durable receipt; package update does not refresh cached process. |
| P-2295 P:2295–2306 | 升级路径 · ADMIN 显式调 / Upgrade path · ADMIN runs the tool explicitly | HOST_ADAPTER | guidance | host.distribution | superseded | true / true / false | Four whole-file outputs, no adopted-host selection or durable receipt; package update does not refresh cached process. |
| P-2307 P:2307–2324 | 版本告警 / Version drift warning | HOST_ADAPTER | guidance | host.distribution | superseded | true / true / false | Four whole-file outputs, no adopted-host selection or durable receipt; package update does not refresh cached process. |
| P-2325 P:2325–2336 | 工具改名历史 · `unbound_report` → `fcop_report` / Tool rename history | LEGACY | history | legacy.tool-history | obsolete | false / false / false | Removed alias history belongs in compatibility reference, not current API instructions. |
| P-2337 P:2337–2338 | 版本历史补记 / Version History Addendum | LEGACY | history | legacy.protocol-history | commentary | false / false / false | Version chronology preserved but excluded from default runtime context. |
| P-2339 P:2339–2356 | 2.2.0 变更（2026-05-12） | LEGACY | history | legacy.protocol-history | commentary | false / false / false | Version chronology preserved but excluded from default runtime context. |


## Common role block — four variants, 34 consumers

Source: `src/fcop/templates/roles/_COMMON-FCOP-3.2.5.md`; SHA-256 in Distribution. The injection script maps 16 team roles × two languages and one solo role × two languages. This source is itself included in the retained artifacts, in addition to the generated copies.

| Unit / source anchor | Category | Authority / normative | Disposition / domain | Host-specific / downstream-required | Finding |
| --- | --- | --- | --- | --- | --- |
| COMMON-TEAM-ZH / BEGIN_TEAM_ZH | CATEGORY_MODULE | profile / true | profile / profile.work-planning | false / false | References Rule 0.a; parent waiting, role routing, workspace cage and chat/task authorization are legacy Profile policy, not Base T7 authority. |
| COMMON-TEAM-EN / BEGIN_TEAM_EN | CATEGORY_MODULE | profile / true | profile / profile.work-planning | false / false | Same workflow intent; pure-Q&A exception requires explicit scope and recorded reason. Does not license silent task bypass. |
| COMMON-SOLO-ZH / BEGIN_SOLO_ZH | CATEGORY_MODULE | profile / true | profile / profile.work-planning | false / false | ME seat and self-reread are solo Profile; archive still needs formal v4 authorization if using v4. |
| COMMON-SOLO-EN / BEGIN_SOLO_EN | CATEGORY_MODULE | profile / true | profile / profile.work-planning | false / false | Same separation; no automatic role, implicit issuer trust or ordinary-child Base gate. |

## High-impact semantic splits, not new Core requirements

1. R-0075 architecture has seven concepts; frozen normative Core has eight contracts. Keep explanatory naming out of machine-Core counting.
2. R-0244/0307/0337 and COMMON: durable scope/report evidence belongs to v4; mandatory leader/subtask sequencing belongs to adopted Profile. Ordinary parent children/ISSUE closure cannot become hidden T7 gates (F4.4.7).
3. R-0348 and P-0493: explicit permission language is useful but role names/chat/task body are not authorization facts. F4.7 requires REVIEW, issuer proof and trusted adopted evaluator; profiles=[] allows T1–T3 only.
4. R-0464/0541/P-0558: session occupancy/handoff policy does not provide global workspace lock or Core identity; task pickup must not bypass explicit identity policy.
5. R-0615/P-1104: old frontmatter examples are not structurally valid v4. Four official envelopes, subject/attempt/workspace and timestamps must come from F4.3.2.
6. R-0746: append-only REPORT/ISSUE/REVIEW retained; blanket immutable TASK conflicts with append-only transitions and authoritative path movement. Corrections use references, not unrecognized AMEND prefixes or old supersedes alone.
7. R-0873/P-0851: archive stays terminal in v4; neither finish active→done nor authority-moving history archive is permitted.
8. R-0916/P-1877/P-2070: five old decision strings and in-place human_approval are not v4 REVIEW semantics; no same-file approval patch.
9. R-0972/P-1976: runtime failure categories are not C8 recovery states. R-0995/P-2007: notifications are not durable history and cannot determine NOW.
10. R-1058/P-2141: INSPECTION is not a fifth formal business envelope. GAL/ALERT and EVAL remain Toolkit/Profile/Runtime.
11. R-0799/P-0503/P-1308: maintainer coding/debugging/checklist content is development-only; does not enter generic business Agent context.
12. R-1141/P-0001: installed guidance and Host metadata cannot outrank frozen Specification, adopted trust boundary or fixed ADMIN taskbook.
13. P-2181's decision=done example conflicts with its own REVIEW enum; preserve history, exclude as current v4 example.
14. P-1339 is a literal TBD, not a rule to complete during this audit.
15. P-2254–2307: old whole-file distribution cannot be declared a safe, adopted, bounded v4 projection merely by changing version labels.

## WP4C.1 decision register — original 15/15 questions addressed

| # | Observed fact | Candidate decision for ADMIN (not frozen here) |
| --- | --- | --- |
| 1 | Existing _data mixes v3 rules and old specs. | Separate v4 namespace under package data; preserve legacy path/API behavior. |
| 2 | No module manifest or adoption receipt. | Separate immutable package inventory from explicit workspace adoption evidence. |
| 3 | Current version tags have no dependencies/selection. | Freeze minimal ID/version/digest/dependency/selection/order fields; no dynamic policy engine. |
| 4 | Git LF, archived CRLF and BOM differ. | Define exact UTF-8/no-BOM/LF module bytes and hash, including newline rule; fail closed on mismatch. |
| 5 | Four Host outputs generated indiscriminately. | Fixed static Host profile plus explicit ADMIN adoption reference, never evaluator installation via text. |
| 6 | Current files are full concatenations. | Short verified pointers where supported; deterministic bounded embeds otherwise. |
| 7 | No actual short-reference consumption proof. | Host-specific bounded projection and isolated later conformance proof, no duplicate authoring source. |
| 8 | Root development entry looks like downstream template. | Separate development-only entry/manual from general business context, with explicit audience. |
| 9 | Discussion source pinned; license/effect unresolved. | ADMIN source/effect/license freeze Gate before reference/snapshot/vendoring policy. |
| 10 | v3 redeploy public; v4 deployment unavailable. | Preserve v3, define explicit v4 adopted profile/hosts and real dry-run; no fallback. |
| 11 | Whole-file replacement can erase product blocks. | Ownership digest/conflict must fail closed before first write; no guessing managed region. |
| 12 | Archive then sequential write, no receipt. | Set bounded staging/atomic replacement/append receipt/rollback proof; avoid new Runtime/state machine. |
| 13 | rules/protocol typed unavailable in v4. | Freeze read-only object identity and version/digest; implement only later WP4C.4. |
| 14 | Roles, skills, patrol, GAL, deployment mixed with protocol. | Keep those optional Profile/Toolkit/development modules; Core remains C1–C8. |
| 15 | No frozen Core change needed to classify findings. | Audit can close; one WP4C.1 constitution freeze entry Gate remains, not implementation authorization. |

Counts: 73 forward clauses; 147 primary source sections (CORE 35, CATEGORY_MODULE 57, HOST_ADAPTER 8, DEVELOPMENT_CONSTITUTION 10, LEGACY 36, REMOVE 1); four separately listed common variants; 86 inventoried source/output paths. This is a classification audit, not a completed Rule Package or proof of Host consumption.
