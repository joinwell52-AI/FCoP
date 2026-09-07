# WP4C.3 implementation plan — WP4C.3c authorized closeout

## WP4C.3c governing continuation

Fixed taskbook ec2e43cd87ce264da1b77365558a182736ccb24f (13805 bytes, SHA-256 c81c883c6ccf4f132ed12f511684eed93fc455fc37125b85ed4c15d8fbaeee80) and [ADMIN approval](https://github.com/joinwell52-AI/FCoP/pull/23#issuecomment-5572037831) now authorize the exact historical method-set correction and reuse of all 31 preserved candidate files. Scope is WP4C_3C_LEGACY_PUBLIC_METHOD_SET_ALIGNMENT_AND_WP4C_3_RESUME, not WP4C.4.

The fixed taskbook is a direct single-file child of c19808f4bc07948729bb841ec569627cb672fde7. The authorized dirty-worktree fast-forward preserved 31/31 raw identities and no unknown files were present. No candidate implementation change was needed. Branch is now review/fcop-4.0-wp4c.3c-public-method-closeout in the same independent worktree. Original D:/FCoP and PRs #21/#22/#23 remain untouched.

Alignment commit 96ad2ae812c60a6362d9c360dbb815621a0cbe1a changes only the authorized function in test_v4_creation.py. It pins the historical 38-name identity, explicitly separates eleven v4-only names, proves a disjoint exhaustive union and the sole rule_distribution addition, and retains all twelve original assertions. All 110 pre-existing Project method ASTs and all original policy values remain unchanged. The exact function passes; the full creation/public-surface test run passes 102/102. See FCOP-4.0-WP4C.3C-PUBLIC-METHOD-SET-ALIGNMENT.md for independent identity and assertion evidence.

Closeout sequence: full FCoP/Core/MCP and distribution validation; verify all future nodes and package inclusion; Content commit of exactly the preserved 31 candidates plus current reports; Manifest-only commit; new Draft PR with taskbook/fcop-4.0-wp4c.3c-public-method-set as base; fixed-HEAD GitHub/Git/fresh-LF readback. Absent branch-filtered CI is NOT_TRIGGERED_BRANCH_FILTER, not a pass. Only after actual completion request WP4C_3_RULE_PACKAGE_ACCEPTED and stop. Test results and delivery outcome are maintained in the current CONFORMANCE-RESULT and RESULT, not inferred from this plan.

## Preserved WP4C.3b stop and pre-code plan (historical)

Historical WP4C.3b status: BLOCKED at the existing historical public-method count assertion in tests/test_fcop/test_v4_creation.py:839 (39 vs 38, sole addition rule_distribution). That file was outside the then-authorized write set. Production changes and candidate data were preserved LOCAL_ONLY, not committed with the factual report delivery. See the RESULT report for the retained evidence and inventory; WP4C.3c above records the subsequent ADMIN authorization. No implementation changes followed confirmation of that blocker.

## Current authority and pre-code decision

The historical blocker below is preserved, now resolved by ADMIN's WP4C.3b taskbook `3a11498c0d4aff736628e781f34516950cb34be8` (13446 raw bytes, SHA-256 `5c4cb2506a6d987dea705a2c5d1b28108b01a3d2b68cbf7b0047dbb8d3d4dbcb`) and [PR #22 approval](https://github.com/joinwell52-AI/FCoP/pull/22#issuecomment-5568219764). GitHub raw Blob and fetched Git Blob were equal. The direct parent is `ec81dc5ed80ff2a4492fd0d1611aad234949bfb5`.

Fixture commit `115751b4c24a1924062a81a21e0d655e8cb5fedc` changes only DIST-02's development variant in one file; six original assertions remain, with three added assertion statements. No subsequent Conformance edits are authorized. Pre-code validation: FCoP 1256 passed; Core 119 passed; MCP 134 passed; Meta 33 and control 1 passed; collect 176; behavioral 142 expected missing-capability failures (56 current, 86 future), no unexpected error; Ruff and mypy passed. A transient Ruff UP012 on the fixture's redundant encoding argument was corrected before the isolated commit, without byte-semantic change.

Execution directory: `D:\FCoP-wp4c3b-development-fixture-and-rule-package`; review branch: `review/fcop-4.0-wp4c.3b-development-fixture-and-rule-package`. Original workspace and historical PRs #21/#22 are preserved. Scope remains WP4C.3b fixture alignment plus WP4C.3 only.

### Implementation sequence and budget

1. Author exactly nine new business modules in English and Chinese, plus one Manifest. Use the 73-row primary ownership schedule in the mapping report; EN/ZH have identical primary IDs, graph and audience. Verify raw UTF-8/LF, exactly one final LF, 18 identities, all hashes/sizes, 73 unique owners and bilingual parity before wiring any public entry.
2. Add a small private package under `src/fcop/v4/rule_distribution/`: fixed contract tables, structured errors, strict offline loader, explicit selector, and thin dispatch/read-only preflight. No persistent cache, dependency framework, network, database, lock or second state machine.
3. Add only `Project.rule_distribution(*, action: str, request: Mapping[str, Any]) -> Mapping[str, Any]`; register one handler and one version policy. Legacy calls reject without migration. The private binder reuses `_manifest`, `read_json` and `safe_path` to revalidate the declaration and cached workspace identity. It deliberately does not call `_Creation._check`, whose mutation-layout prerequisites require lifecycle directories: pure package reads need only the valid declaration and must never create those directories. Existing Core algorithms remain unchanged.
4. Only validate/select/validate_operation_scope may succeed. Future inspect_profile/plan/apply/rollback perform negative, read-only preflight where facts prove a typed failure; otherwise return existing toolkit:OPERATION_NOT_IMPLEMENTED. No projection bytes, Host writes, adoption, receipts, deployment or rollback success.
5. Add only v4 data patterns to package inclusion, focused unit tests, the single-method public snapshot addition and an additive Unreleased entry. Run all 56 target nodes, Meta/control, classify all 86 future nodes, regress FCoP/Core/MCP, Ruff/mypy, public surface, wheel/sdist inclusion and raw legacy byte comparison.

Manifest records contain all ELEVEN RD-07 fields, including conflicts_with; package identity is a candidate data version, not a library version bump. All artifacts are validated on every request before selection; no cache keyed only by version. Development selection requires four explicit fixed local references under the reserved namespace, checks real raw hashes and returns the same ordered identities; no defaults, Git discovery, network or business-content substitution. Constitution remains absent.

The production file budget is five small private modules initially; a sixth is permitted only to keep preflight distinct from positive selection. Existing-file edits are confined to project.py's thin entry, creation.py's registry, boundary.py's policy, package-data patterns, public snapshot and CHANGELOG. No source outside the taskbook allowlist is needed. The 14 legacy data hashes and pre-addition public snapshot baseline below remain the comparison authority.

Delivery sequence is fixed Taskbook -> Fixture -> Content -> Manifest, with the last commit containing only the delivery Manifest. New Draft PR targets the taskbook branch. Final remote Blob/Git/fresh LF checkout parity is required; branch-filtered absent CI must be reported honestly. Only ADMIN may sign WP4C_3_RULE_PACKAGE_ACCEPTED.

## Preserved WP4C.3a preflight record

Taskbook: `0559e0fdf5390aa830f98a38d83f96f1cd475ab1`, path `taskbooks/fcop-4.0/WP4C.3a/01-Historical-Audit-Scope-Alignment-and-WP4C.3-Resume-Taskbook-v1.0.zh.md`.
Raw bytes: 15954; SHA-256: `903c5f0f249598ab3b5aaf7e947af8ed36fbc23928eff9b5db11e305acb21ba6`.
[ADMIN authorization](https://github.com/joinwell52-AI/FCoP/pull/21#issuecomment-5567383721) and [hash erratum](https://github.com/joinwell52-AI/FCoP/pull/21#issuecomment-5567650164) were read back. The revoked `a61c4159...` is NOT an accepted identity.
Direct parent: `78ea6b89a1ef0df0e504a3cfa34cecddeb7dda24`; original WP4C.3 taskbook: `de213ec0f74f8976283a24986d4eb7de77c67142` (SHA-256 `a4b782db3a984be9872d6c99428c5fc669a1cd3135468b33ef8eba7a6c1b57d2`).
Audit correction commit: `e1ed85e4ba5aba212ddf3cc4f880c0abecc2bfab`, direct child of the corrected-identity taskbook.
Scope: `WP4C_3A_AUDIT_SCOPE_ALIGNMENT_AND_WP4C_3_RESUME`.

## New pre-implementation blocker: missing mandatory development inputs

`DIST-02[development-no-constitution]` in `tests/conformance/rule_distribution_v4/test_dist_01_06_manifest.py:40` calls `select` with `assembly_id=repository-development` and `constitution_ref=None`, then requires four references with path/revision/sha256 (lines 71-75).

Its actual inputs do NOT contain the four development references:
- `conftest.py:166-230`: Scenario creates only `fcop/fcop.json` in the workspace. The package contains the 18 business fixtures and their Manifest; the input directory contains a Host profile and the generic ADMIN-selection fixture.
- `conftest.py:243-263`: request has no `development_references`, development entry identity, development manual identity, or current development TASK/Gate reference bundle.
- `driver.py:22-36`: the driver only constructs Project(root) and forwards the request; it supplies no trusted reference registry or defaults.
- `git ls-tree -r --name-only 0559e0fdf5390aa830f98a38d83f96f1cd475ab1 docs/fcop-4.0/development` returns no paths. The fixture workspace also has no such directory.

Read-only inspection plus execution of the existing Scenario setup in an isolated temporary sandbox produced:

```json
{
  "development_references_present": false,
  "constitution_ref": null,
  "workspace_files": ["fcop/fcop.json"],
  "development_namespace_exists": false,
  "manifest_fields": ["artifacts", "manifest_schema", "package_version", "protocol_version"],
  "artifact_record_field_count": 11
}
```

This is a fixture-input finding, NOT a claim that a production implementation was run and failed. The production entry is still absent. Ordinary baseline red alone would not establish this finding; the explicit request and filesystem evidence above do.

Frozen RD-03 reserves repository-only development guidance separately; RD-19 requires four pinned references, with only the independent constitution optional. Original taskbook section 6.3 requires validating and returning those four fixed references; section 5.2 forbids caller-unrequested implicit selection. A rule package cannot invent the current development TASK/Gate, substitute business artifacts for a development manual, return placeholder paths/hashes, or bake this executor's own taskbook into every user's request.

By contrast, `test_dist_21_24_assembly_compat_mcp.py:43-79` (DIST-22) constructs four local reference files and passes `development_references`. This is an available example of complete local inputs, not authority to edit DIST-02.

The narrow likely correction is to supply the same categories of complete, pinned local inputs to the DIST-02 success fixture, preserving its ID, all assertions, and optional-constitution absence. ADMIN must decide and authorize that correction. It resides in a FOURTH frozen Conformance file, outside WP4C.3a's exception. No test edit or synthetic production fallback was made.

Stop basis: WP4C.3a section 8 (fourth Conformance file / 56 targets cannot be completed within scope); original WP4C.3 sections 8, 10 and 13. No Gate is requested.

## Read-only implementation preparation

Both frozen Core languages, both rule distribution contracts, the complete WP4C.1 decision schedule and matrix, original taskbook and WP4C.3a taskbook were read. The 73-clause ownership plan is reproduced in [the mapping report](FCOP-4.0-WP4C.3-CLAUSE-AND-ARTIFACT-MAPPING.md); it is not authored artifact coverage.

| Surface | Baseline fact / conditional implementation plan |
| --- | --- |
| Public boundary | src/fcop/v4/boundary.py has an exhaustive method-policy map; only one new rule_distribution policy would be allowed |
| Public entry | Project.rule_distribution is absent; authorized signature is Project.rule_distribution(*, action: str, request: Mapping[str, Any]) -> Mapping[str, Any] |
| Handler wiring | src/fcop/v4/creation.py:241 registers bound v4 handlers; only handler registration would change |
| Project | src/fcop/project.py would have one thin version-routed entry, no selection algorithms |
| Private code | Only src/fcop/v4/rule_distribution/** for pure parser/loader/selection and structured Toolkit failures; final decomposition is not implemented |
| Data | Exactly 18 newly authored module Markdown files + manifest.json under src/fcop/rules/_data/v4; not copies of legacy rules |
| Packaging | pyproject.toml currently includes legacy rules by explicit patterns; only v4 data inclusion would be added |
| Scope | No Store, database, extra lifecycle, locks, background, network, Host output, evaluator registration or dependencies are needed for pure reads |

Only validate/select/validate_operation_scope could succeed. Future actions would be restricted to typed read-only preflight rejection. Existing 3.x writers/signatures/bytes must remain untouched. No public entry, candidate data, packaging change or implementation file was created because the blocker precedes coding.

## Manifest field-count observation (not a second blocker)

Original taskbook section 4.4 says ten artifact fields but explicitly requires strict RD-07. The higher-priority frozen RD-07 EN/ZH table and actual fixture each enumerate ELEVEN fields (including conflicts_with). Any eventual implementation must retain the complete RD-07 field set; no field may be removed to satisfy the prose count. Neither document was edited.

## Target plan

| DIST ID | Nodes | Final pre-implementation classification |
| --- | ---: | --- |
| DIST-01 | 2 | Expected red |
| DIST-02 | 4 | Expected red; success-fixture input defect requires ADMIN |
| DIST-03 | 6 | Expected red |
| DIST-04 | 11 | Expected red |
| DIST-05 | 9 | Expected red |
| DIST-06 | 6 | Expected red |
| DIST-07 | 4 | Expected red |
| DIST-21 | 2 | Expected red |
| DIST-22 | 4 | Expected red |
| DIST-25 | 8 | Expected red |
| Current total | 56 | Not implemented |
| Future owners | 86 | Expected red |
| DIST-30 | 1 | PASS |

## Legacy byte baseline at fixed taskbook

These are SHA-256 of immutable Git blob bytes, not CRLF-normalized comparisons. No listed source or snapshot was modified.

| Baseline path | Git blob SHA-256 |
| --- | --- |
| src/fcop/rules/_data/agent-bringup-prompt.en.md | b519c83a588200d6af5d52fe2f0edec2f65a584b4f6f7261ddbf4e5dcf216837 |
| src/fcop/rules/_data/agent-bringup-prompt.zh.md | 1d0d26f827585b8f4bc3540dc0f5a5fe48ae00ce8f54b3a7ea5bbfaa3274fb7c |
| src/fcop/rules/_data/agent-install-prompt.en.md | e71c0eaa084bd75cf9ce7947eae25c0c4d126affe2e52fb069fafae70abdc496 |
| src/fcop/rules/_data/agent-install-prompt.zh.md | 92178af0a81acb4fdfe67ecca11d5a520bf3ed80a46df1b1493a591b2ab18d0e |
| src/fcop/rules/_data/fcop-protocol.mdc | 8ac413b1c39238df82a175d108c166c58c27fbe833b202470e140755780250d3 |
| src/fcop/rules/_data/fcop-rules.mdc | 24f42cfe76063bd39358cdb03a59e8d4e6b391c36bc9749302185252a84d1686 |
| src/fcop/rules/_data/fcop-spec-v1.0.en.md | 1c1feb55157fe3270e20bcdbe5363a04a5ecb68b8d2ed069d02a546f2e3349de |
| src/fcop/rules/_data/fcop-spec-v1.0.zh.md | f21a8231d72c99eaad97e77088876a19a70642040aafa27a31d8b9866893a9a8 |
| src/fcop/rules/_data/fcop-spec-v1.1.en.md | 13a4cae0db79d0094b796683a76bc40ef8fcd4ade3be739737fd3ecc52d1051c |
| src/fcop/rules/_data/fcop-spec-v1.1.zh.md | 987347c1ab1748cf1b124173dccf6833c324f23cae712aa2c9b6ccc18629e6fc |
| src/fcop/rules/_data/internal-readme.en.md | e2a9491440f051dbc6d3c36fd54c474e985148ee28db911bf360b22f82d72936 |
| src/fcop/rules/_data/internal-readme.zh.md | c9a9960b9db96145695f520fd2eef6b0d3177ff6cc8021be02b0a048f63ea61c |
| src/fcop/rules/_data/letter-to-admin.en.md | cd313d5963b644faf29fb42fce04eb66d104d77bd167ab26df4714d02458f6f0 |
| src/fcop/rules/_data/letter-to-admin.zh.md | e64a969ae5405fff4556fbf35a4f707793ea0a6778c31d98522e5a370b56fba7 |
| tests/test_fcop/snapshots/public_surface.json | 8ccbea8a628e94eec25467dfbb04a29e6a4843bf3822c8810360d2bb7a9a2fb3 |

## Preserved history

PR #21 remains an OPEN Draft at `78ea6b89a1ef0df0e504a3cfa34cecddeb7dda24`; it was not rewritten, merged or repurposed. Its Content `0e89f94aa8df017817f76dadc8572c8bc5c0afdf` and Manifest remain ancestors. The prior 32/33 Meta and DIST-30 failure is an accepted historical blocker, now resolved by the separate audit commit. This report updates current facts; it does not erase that history.
