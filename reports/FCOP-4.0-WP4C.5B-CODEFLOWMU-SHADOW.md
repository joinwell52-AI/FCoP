# WP4C.5B CodeFlowMu Read-Only Shadow

## Result and evidence limits

Real fixed-consumer observation completed through Project.rule_distribution,
not a synthetic consumer fixture. Current local CodeFlowMu HEAD was
b961b16dd0c8863ead6995d963fe0ca576a8abaa before and after the call.
Historical isolation evidence commit 789cb3fa8a007f050248784f7daf689808a549a2
is identified separately; historical test results are not this run's tests.

The original D:/codeflowmu worktree has pre-existing tracked/untracked material.
It was not cleaned, checked out, fetched into, installed, executed or modified.
A bounded git archive of fourteen explicitly named files from the current fixed
commit was extracted outside both products at
D:/fcop-wp4c5b-shadow-b961b16d-lf. Each extracted byte stream was independently
compared with git show <fixed-ref>:<path>, 14/14 exact. This is a fixed-commit
read-only evidence snapshot, not a claim the product worktree is clean.

An initial archive made without a per-command LF setting exposed the machine's
autocrlf conversion and was NOT accepted as raw-Blob evidence. A new archive
using git -c core.autocrlf=false archive produced the verified byte identities.
Original product files and the first evidence artifact were preserved.

## Read authorization and zero effects

The caller pre-created an external strict six-field authorization JSON, bound
to that exact normalized snapshot root and the fourteen hashes below.
Authorization file:
C:/Users/Administrator/AppData/Local/Temp/fcop-wp4c5b-shadow-authorization.json.
SHA-256: 206129e8a68db7d5da1ef345d04c5e28348c1f392eef11aaa44e96f1fe6cdafa.
Scope: read-only; authorization_kind: fcop-rule-distribution-shadow;
downstream_kind: fcop-consumer; deploy: false. Shadow did not create this
authorization, infer it from a product document, or install an evaluator.

Public caller workspace: D:/fcop-wp4c5b-shadow-caller01. It was explicitly
created before measurement. Shadow returned fourteen path/size/hash records,
literal fcop==3.2.5 / fcop-mcp==3.2.5 pins where present, deployed=false,
runtime_consumption_verified=null. No source bodies were returned.

Before/after equality passed for all snapshot bytes, all caller-workspace
bytes, product Git HEAD and product tracked-status metadata. Product status
byte SHA-256 at this observation:
0aafd5df239ee324f2e5fedeb91ac7aeeebd05b518220ce5edc8aae4f40ed19e.
This establishes this call's zero effects, not a claim to monitor unrelated
ongoing work indefinitely. No real product process, npm, pip, migration,
Scheduler, EVAL, Panel, Host deployment or five-bucket operation was invoked.

## Fixed raw evidence inventory — 14/14

All paths are relative to CodeFlowMu fixed commit b961b16dd0c8863ead6995d963fe0ca576a8abaa.

| Path | Bytes | SHA-256 |
|---|---:|---|
| START-CODEFLOWMU.ps1 | 821 | 4188a1d4ffdfd5777ec735785fe3f684a52c8aff302ed2c829e31afc3a7eee9b |
| codeflowmu-installer/install-codeflowmu.bat | 9265 | 97b4f12b9843f76e4144fe0d22897b8baa3e85f54b1d15ea3161e8400637fbcc |
| codeflowmu-installer/install-codeflowmu.sh | 2127 | 6e642139bb19ac9a1b65bde3fa5313df6e65d86c3a6eda8a7a60a8ddea175da5 |
| codeflowmu-installer/start-codeflowmu.bat | 487 | 999de5b0dd3e2b42b7035f086c8cf97725b71c1acc99a49453501dcbce1f2d12 |
| codeflowmu-installer/start-codeflowmu.sh | 400 | 556a5381f22da68c000d10c019ec3495d38ac9aee05baca97a3c99d05c52906d |
| codeflowmu-shell/package.json | 2118 | cd28c113310999330170f4763c4ec9a161b2ae6bc3a1c27e9705d6bfa87c4552 |
| codeflowmu-shell/scripts/runtime-preflight.cjs | 9513 | d46869cc449989531e8be2b7e286e85e2ac849589fe5c48f9534b7d5b7294be3 |
| codeflowmu-shell/src/fcop-adopted-bootstrap.ts | 4453 | 5c2c5fba8aac79b594b9064644f84be8d701c9aa9cf637be710d9abee6d9db52 |
| codeflowmu-shell/src/fcop-env-probe.ts | 24608 | e9aa5a6f4ebca7f352ecb20faceb30a42fc17bbb130e16134a36cece70457874 |
| docs/governance/AGENT-NATIVE-ENGINEERING-CONSTITUTION.md | 25871 | 87cf212d1cb75cefd0da6da7e5f0f4c7eaedbc231c784b985c3e2e51856abc4c |
| docs/governance/CODEFLOWMU-CONSTITUTION-ADOPTION.yaml | 761 | 2a7a39ca6fd5a9aaa13ab0efe05ee3c87c22b5ba79e35d7aa53f333a2f044add |
| package.json | 3226 | db53f4511f8d2021c00dba5b925bea51b583320d55b3b694dcb0cffeeb67b84a |
| packages/codeflowmu-runtime/src/_external/fcop-client.ts | 59840 | 0a2343c8fdc921a58aaf11216ff2473f5442d54fd76d257cec100b3842e41c01 |
| research/evidence/changes/CFM-20260902-FCOP3-VERSION-ISOLATION/conclusion.md | 2979 | b646b4a6aa7630fcb62b814ecc0df35ea1cb4038d9dfa03513b7206d17c94db7 |

## Compatibility findings, not a new FCoP contract

- Runtime fcop-client.ts:57–59 fixes both adopted packages at 3.2.5 with exact
  policy. Lines 80–123 classify missing/empty, unparseable, and non-exact
  versions independently. 4.0.0 is not adopted; a range, prerelease or malformed
  value is not an exact accepted triple. Both packages must match.
- assertFcopReady at lines 596–675 reads installed distribution metadata,
  rejects failed policy before loadFcopModule, and separately checks the
  imported runtime version. Shell main.ts calls that guard; health projection
  delegates the same evaluateFcopVersionPolicy. These are fixed source
  findings, not a claim that this audit ran the downstream runtime.
- Start launchers call npm start; package scripts route through the existing
  runtime-preflight to shell startup. FCoP installation is an explicit installer
  operation pinned to the adopted pair, not a startup pip upgrade. The guard's
  pip command is error-message advice, not execution.
- Scope caveat: runtime-preflight has an existing --open path that may refresh
  Node production dependencies. Also fcop-adopted-bootstrap can copy missing
  product-local adoptedSource files. These pre-existing behaviors are not
  FCoP package upgrades or this stage's v4 adoption, and this audit does NOT
  claim all product startup is write-free. Neither path was executed or changed.
- Downstream catalogs or UI do not define FCoP tool ownership. No close_issue
  capability is added to FCoP. Catalog drift, if present, remains a downstream
  observation, not justification to change the 46-tool surface.

## Excluded CodeFlowMu development RC

Fixed path docs/governance/AGENT-NATIVE-ENGINEERING-CONSTITUTION.md,
revision b961b16dd0c8863ead6995d963fe0ca576a8abaa, 25871 bytes,
SHA-256 87cf212d1cb75cefd0da6da7e5f0f4c7eaedbc231c784b985c3e2e51856abc4c.
The product's fixed adoption YAML declares version 1.0-rc.1, license MIT,
CodeFlowMu-development scope, ordinary-business/FCoP4-adoption exclusion, and
global_constitution_version_frozen=false. This is attribution of the local
declaration, not a grant or independent legal assessment of redistribution.

For this task its role is CODEFLOWMU_DEVELOPMENT_TRANSITION_REFERENCE.
normative_fcop_4_contract=false; ordinary_business_agent_injection=false;
release_identity=false; auto_adoptable=false. It is read solely as excluded
audit evidence and never fed to a Manifest, module selector, rule generator,
MCP default resource, Host projection or wheel business payload.
The frozen FCoP distribution contract's explicit digest exclusion is unchanged.

## Reproducibility and stop

Recreate only the exact listed files with LF Git archive at the fixed ref,
verify each against git show, and provide an external authorization with those
same raw hashes bound to the chosen local root. Invoke the production public
shadow action with deploy=false; compare before/after snapshots. Do not run
product scripts or use this evidence as runtime-consumption confirmation.
Independent negative tests cover invalid authorization before any downstream
stat/open/scan, symlink/junction, changed authorization and changed source
bytes. Companion RESULT records their actual results.

CODEFLOWMU_FILES_MODIFIED: 0
RUNTIME_CONSUMPTION_CLAIM: UNKNOWN
This report requests no separate downstream migration or adoption.
