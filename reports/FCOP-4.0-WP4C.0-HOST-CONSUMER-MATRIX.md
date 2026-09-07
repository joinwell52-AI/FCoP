# WP4C.0 Host Consumer Matrix — BLOCKED

- Repository: `joinwell52-AI/FCoP`
- Gate / audited tree: `aad88ae5f1112881545d30c9938739e83481516d`
- Taskbook commit: `962b67d89e137c26440291d3a48fc7aea1cfebb6`
- Taskbook: [fixed WP4C.0 authority](https://github.com/joinwell52-AI/FCoP/blob/962b67d89e137c26440291d3a48fc7aea1cfebb6/taskbooks/fcop-4.0/WP4C.0/01-Rule-Distribution-Host-Assembly-and-Development-Context-Baseline-Audit-Taskbook-v1.0.zh.md)
- Taskbook SHA-256: `c8c4cb26708a480a6793d88c21511b103f140021c3827c9977b076dfed748e55`
- Scope: `WP4C_0_ONLY`; report state: `BLOCKED`.

## Stop decision

`ENGINEERING_CONSTITUTION_SOURCE_UNRESOLVED` is one confirmed P0 blocker, not an exhaustive count of all possible conflicts. Taskbook sections 3 and 14 require an identifiable authority file, version, digest, license and acquisition method for 《Agent 原生软件工程宪法》. Those cannot be established from the supplied fixed inputs. Section 14 permits factual BLOCKED reports but prohibits requesting the acceptance Gate.

No replacement constitution is authored, downloaded or adopted. The audit stopped at this prerequisite; remaining audit obligations are explicitly incomplete. `REQUESTED_GATE: NONE`; WP4C.1 is not started.

## Preliminary target register, not completed consumer verification

| Host | Tracked entry observed | Adapter implemented | ADMIN adopted | Generation provenance verified | File-reference support | Runtime consumption |
|---|---|---|---|---|---|---|
| Codex | `AGENTS.md` | NOT_AUDITED | unproven | No | unverified | unverified |
| Cursor | `.cursor/rules/fcop-rules.mdc`, `.cursor/rules/fcop-protocol.mdc` | NOT_AUDITED | unproven | No | unverified | unverified |
| Claude Code | `CLAUDE.md` | NOT_AUDITED | unproven | No | unverified | unverified |

The register has three required Host names and four observed tracked target paths. It is not a 3/3 completed Host audit. Additional Host inventory is incomplete; no total consumer denominator is asserted. The header also names other consumers (for example Devin); a header claim is not adapter or runtime proof.

The loader-declared candidate inputs are `src/fcop/rules/_data/fcop-rules.mdc` and `src/fcop/rules/_data/fcop-protocol.mdc`. A complete deployment trace from those inputs to each Host target has not been verified in this run.

`model_selection_effect: none` is the taskbook boundary, not a claim that a real Host's model configuration was probed. The existence of AGENTS.md in a Git tree does not prove adoption, generation in a current session, actual loading, compliance or model selection.

## Probe and consumer limits

No Host was installed or configured. No new login/credential probe or runtime smoke test was performed. No Host entry was generated, copied or redeployed. No ordinary task, parallel Branch task or development task assembly was executed.

CodeFlowMu shadow: `NOT_AVAILABLE` in this delivery because it was not attempted after the hard stop, not because access was tested and failed. No CodeFlowMu files were changed or used to infer FCoP authority.

Host support, adoption, generated entry and actual runtime consumption remain four separate facts. Completing this matrix is deferred until the prerequisite authority blocker is resolved by ADMIN.

---

# WP4C.0a resume — Host/consumer audit closed, consumption not assumed

Input: `eb086ee43f345a4d93ffb520049dc8af08712d3b`. No Host install, login, config mutation, projection generation, runtime probe or downstream upgrade. This appended section replaces the earlier *current* incomplete status without rewriting history.

## Host matrix — 12/12 named consumer classes

Inventory method: actual implemented four output targets plus named consumers in rules, ADR-0006, getting-started EN/ZH, ADR-0001 and tutorial references. Aliases grouped explicitly: Codex CLI→Codex; Claude Code CLI→Claude Code; generic CLI/raw API/SDK grouped as an unimplemented adapter class; CodeFlow/CodeFlowMu grouped downstream. Marketing/discovery/tutorial mentions are retained but do not count as working adapters. No claim to enumerate every commercial Host in existence.

Common fields for every row:
- `admin_adopted: unproven`: no fixed per-workspace adopted-host manifest in the audited code.
- `supports_file_reference: unverified`: existing long files and source comments are not a short-entry consumption test.
- `runtime_consumption_evidence: unverified`: task app presence or user screenshot does not prove reading the entire fixed current blob.
- `model_selection_effect: none`: FCoP outputs select no model.
- `v4_rule_adapter_implemented: false`: v4 rules/guidance remain unavailable.
- `canonical_inputs`: for actual legacy outputs, the two canonical mdc files; for MCP, versioned resource handlers; for unsupported mentions, none.
- `entry_generated_this_run: false` for all. Four entries observed in Git are not generated in this session.

| Host ID | adapter_implemented evidence / limit | generated_targets (existing or declared) | Fixed-tree evidence |
| --- | --- | --- | --- |
| Codex | true (legacy AGENTS) | AGENTS.md | Project:1393; ADR-0006:55/106 |
| Cursor | true (legacy mdc) | two .cursor/rules/*.mdc; AGENTS alternative | Project:1391–1393; getting-started:277 |
| Claude Code | true (legacy CLAUDE) | CLAUDE.md | Project:1394; server:3624 |
| Devin | generic AGENTS output only | AGENTS.md (same shared path) | ADR-0006:106/116 |
| Claude Desktop | MCP resource transport; no file adapter | none distinct; fcop://rules/protocol | ADR-0006:53; server:3780 |
| PulseMCP | false (discovery mention only) | none | getting-started.en.md:10 |
| Doubao | false (portability mention only) | none | canonical commentary:12 |
| CLI / raw LLM API / generic SDK | generic file access, no distinct Host profile | AGENTS claimed; no separate projection | canonical commentary:12/2268 |
| Gemini SDK / Gemini | false (library/downstream mention) | no FCoP-generated GEMINI.md | ADR-0001:36; tutorials/snake-solo-to-duo.zh.md:921 |
| Copilot | false (tutorial audience mention) | none | tutorials/tetris-solo-to-duo.en.md:26 |
| ChatGPT | false (tutorial audience mention) | none | tutorials/snake-solo-to-duo.zh.md:921 |
| CodeFlow / CodeFlowMu | downstream consumer, not FCoP Host adapter | downstream-owned composite files; shadow below | canonical rules:57; fixed downstream shadow |


Generated target map closes **4/4**: Cursor rules ← canonical rules; Cursor commentary ← canonical commentary; AGENTS and CLAUDE ← shared preamble + version banner + stripped-rule body + commentary. Actual checked-in copies drift from current source (Context report). Support/adoption/generation/consumption are separate columns of evidence; none implies the next.

A future short-entry profile must prove reference resolution, relative base paths, hash checking, truncation limits, load order and failure behavior in an authorized isolated Host test. If unsupported, freeze bounded deterministic embedded content rather than silent truncation. This report does not recommend installing or configuring a Host now.

## Non-Host consumer paths

| Consumer / entry | Inputs and behavior | Version / authority boundary |
| --- | --- | --- |
| fcop.rules getters | rules/_data mdc, install/bringup/letter/internal text and old spec snapshots | Cached package reads; no workspace adoption. |
| Project.deploy_protocol_rules | two mdc → four whole files | v3 legacy convenience; v4 boundary rejects mutation. |
| Project role-template deployment | teams/index.json → TEAM-README, TEAM-ROLES, TEAM-OPERATING-RULES and roles in shared/ | Five presets; no Profile evaluator installation by text. |
| MCP legacy redeploy_rules | _get_project_write → public Project | Explicit legacy deployment, no v4 fallback. |
| MCP fcop://config, fcop://status | selected workspace state, two resources | Read-only; not rules nor authorization. |
| MCP fcop://spec, fcop://spec/en | versioned _specs.json, two resources | Four source-matched v3/v4 EN/ZH payloads. |
| MCP fcop://rules, fcop://protocol | two resources | v4 typed V4_GUIDANCE_UNAVAILABLE, RULES_PENDING_WP4C. |
| MCP fcop://letter/zh, fcop://letter/en | two resources | v4 typed V4_GUIDANCE_UNAVAILABLE. |
| MCP fcop://prompt/install, fcop://prompt/install/en | two resources | v4 typed V4_GUIDANCE_UNAVAILABLE. |
| MCP fcop://teams | one catalog resource | Five presets; discovery is not adoption. |
| Three team resource templates | roles/TEAM-ROLES/TEAM-OPERATING-RULES lookups | Read-only Profile resources; no authorization power. |
| docs/getting-started*, upgrade and release SOP | operator-facing links/examples | Legacy/development documentation; not executable policy in this audit. |
| scripts/rule_encoding_guard.py and rule tests | read canonical/packaged text markers | Limited validation, not runtime-consumption evidence. |
| common role block injection script | common source → 34 role files | Maintenance generation, not run; not a second v4 source. |
| scripts/patch_rules_version.py | AGENTS/CLAUDE direct text edits | Historical manual drift path, not run or adopted. |

Static MCP count: 2 config/status + 2 spec + 2 rule + 2 letter + 2 install + 1 team = **11/11**; templates **3/3**. Current tests checked both versioned static-resource catalogs and spec parity (3 pytest cases). Prior WP4B 46 tools remain unchanged.

## Four audiences: loading boundaries

| Consumer | FCoP Core guidance | Role/Profile | Engineering constitution | Host thin adapter |
| --- | --- | --- | --- | --- |
| Ordinary FCoP business Agent | Required semantics | Only as explicitly adopted by application | NO default injection | Selected Host only |
| Agent developing FCoP | Required semantics | Per fixed development task | Candidate mandatory, but blocked until ADMIN freeze/license decision | Selected Host only |
| Third-party application developer | Required semantics | Application-owned | Not automatically injected | Selected Host only |
| CodeFlowMu | Compatibility shadow only this phase | Downstream-owned | No injection | No changes this phase |

The discussion draft's mention of other products is not permission to distribute it there. Normal business task completion must not require proof that a software-development constitution was loaded.

## CodeFlowMu fixed read-only shadow — PASS (inspection, not runtime acceptance)

Read `git show` at **c008d9db91a21136fc61a4f60314e22db395d5d2** from its local object store. Did not read mutable runtime ledgers, change files, fetch its branches, install dependencies or touch product state. This is a fixed local snapshot, not a claim of GitHub remote delivery of CodeFlowMu.

| Fixed downstream path | Bytes | SHA-256 | Ownership observation |
| --- | --- | --- | --- |
| AGENTS.md | 194526 | 9aacd2563e1c51394754a19cbd08b9c99fef7c12eac108a8a1c72074057ade0f | Product-owned prefix + FCoP body + product PM suffix |
| CLAUDE.md | 194234 | ef6261c2110f1e484412eb8dd52ecf50fff27cb6b5d26b3191739ebf6bbe89af | Product-owned prefix + FCoP body |
| .cursor/rules/fcop-rules.mdc | 75839 | 24f42cfe76063bd39358cdb03a59e8d4e6b391c36bc9749302185252a84d1686 | FCoP-origin legacy payload; matches canonical hash |
| .cursor/rules/fcop-protocol.mdc | 117608 | 8ac413b1c39238df82a175d108c166c58c27fbe833b202470e140755780250d3 | FCoP-origin legacy payload; matches canonical hash |
| .cursor/rules/codeflowmu-coding-manual.mdc | 782 | ff3eed062d0c493f7211f743958ed50d67567ff36577c12f4b5e17030840fc0a | Product-owned rules; never FCoP replacement target |
| .cursor/rules/codeflowmu-agent-skill-routing.mdc | 2515 | 9542238c79dab0336f9d22ead740988dcbfe8468915fb501a2353f58021408f6 | Product-owned rules; never FCoP replacement target |
| .cursor/rules/windows-encoding-safety.mdc | 1803 | 2d9490977f613e6dace471b928fffbc8538d5db26b81a6c7f481f89f49a62e0b | Product-owned rules; never FCoP replacement target |
| codeflowmu.rules.json | 578 | e2fe98ac17bc56538bbf0ceeb61c41d23e2ac984427980c8fe5d0788d2bcd364 | Product-owned source/Host mapping manifest |


`AGENTS.md:1` and `CLAUDE.md:1` point to the product coding manual via codeflowmu.rules.json. AGENTS additionally ends with CodeFlowMu PM planning policy. Neither region is a FCoP managed block; a sentinel heading alone is not machine-enforced ownership. Two downstream Cursor FCoP files match current canonical Git bytes, while the FCoP repository's own copies are stale; consumer freshness is not implied by parent project's version banner.

`codeflowmu.rules.json` also names GEMINI.md and a Runtime loader; these are downstream-owned Host/profile mechanisms, not new FCoP adapters. Three non-FCoP Cursor rule files are product-owned and outside the four FCoP deployment targets. General two-file root replacement would erase their root-equivalent policy even though distinct Cursor files survive.

Fixed downstream README:62/488/493 states `fcop==3.2.5` and `fcop-mcp==3.2.5`; version-history/changelog agree. This audit did not check installed runtime packages or reinterpret those pins as permission to deploy this review's development build.

## Closure and future boundary

12/12 Host classes, four outputs, 11 static resources and three templates are accounted; eight shadow paths are hashed. Unverified runtime/reference support is an explicit permitted result under original taskbook §8.6, not hidden evidence of success. No current audit gap is being relabeled as verified behavior. Only later authorized isolated consumer tests can change that status.

Stop after remote report delivery. Request WP4C_0_BASELINE_ACCEPTED only; WP4C.1 requires separate ADMIN source/effect/license freeze and taskbook.
