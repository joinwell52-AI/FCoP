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
