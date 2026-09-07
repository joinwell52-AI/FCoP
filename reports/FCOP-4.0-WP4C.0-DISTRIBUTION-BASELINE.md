# WP4C.0 Distribution Baseline — BLOCKED

- Repository: `joinwell52-AI/FCoP`
- Gate / audited tree: `aad88ae5f1112881545d30c9938739e83481516d`
- Taskbook commit: `962b67d89e137c26440291d3a48fc7aea1cfebb6`
- Taskbook: [fixed WP4C.0 authority](https://github.com/joinwell52-AI/FCoP/blob/962b67d89e137c26440291d3a48fc7aea1cfebb6/taskbooks/fcop-4.0/WP4C.0/01-Rule-Distribution-Host-Assembly-and-Development-Context-Baseline-Audit-Taskbook-v1.0.zh.md)
- Taskbook SHA-256: `c8c4cb26708a480a6793d88c21511b103f140021c3827c9977b076dfed748e55`
- Scope: `WP4C_0_ONLY`; report state: `BLOCKED`.

## Stop decision

`ENGINEERING_CONSTITUTION_SOURCE_UNRESOLVED` is one confirmed P0 blocker, not an exhaustive count of all possible conflicts. Taskbook sections 3 and 14 require an identifiable authority file, version, digest, license and acquisition method for 《Agent 原生软件工程宪法》. Those cannot be established from the supplied fixed inputs. Section 14 permits factual BLOCKED reports but prohibits requesting the acceptance Gate.

No replacement constitution is authored, downloaded or adopted. The audit stopped at this prerequisite; remaining audit obligations are explicitly incomplete. `REQUESTED_GATE: NONE`; WP4C.1 is not started.

## Reproducible authority evidence

All paths below refer to the fixed Gate tree, not a mutable checkout or the currently deployed user workspace.

| Evidence | Observed fact | Limit |
|---|---|---|
| `taskbooks/fcop-4.0/WP4/00-Public-Contract-Adapters-and-Distribution-Master-Taskbook-v1.0.zh.md:569` | Names 《Agent 原生软件工程宪法》 and limits its audience to FCoP developers. | Does not pin its text, version, digest, license or acquisition location. |
| Same master, lines 112 and 127 | Declares the development-only flag and future phase. | A roadmap flag/title is not an adopted authority artifact. |
| `reviews/fcop-4.0/gates/WP4B-MCP-ADAPTER-ACCEPTED.md:144` | Restricts the development constitution to development Agents. | Does not identify the constitution payload or fixed authority descriptor. |
| Taskbook commit versus its parent | Direct parent is the Gate; the sole changed file is the WP4C.0 taskbook. | No constitution payload is supplied by this commit. |
| Gate-tree `git grep` for the English/Chinese constitution terms | 42 matching lines, including legacy team-constitution mentions and the titles above. | These matches do not identify the requested engineering constitution; match count is not a normative-rule count. |
| Path inventory / named Git-log probes | No named engineering-constitution artifact established. | This is not a claim that no such document exists anywhere outside the supplied fixed inputs. |

The legacy two-file team constitution (`TEAM-ROLES.md` and `TEAM-OPERATING-RULES.md`) and ADR-0015's historical charter wording are not substitutes for the named engineering constitution. No repository-wide license is presumed to license an unidentified external text.

ADMIN resolution needed: supply a fixed authority file/URL, version, exact SHA-256, applicable license and acquisition/adoption instructions, or publish a fixed taskbook clarification. This report does not choose that policy.

## Baseline and protection

The audit worktree is `D:\FCoP-wp4c0-distribution-audit`, on `review/fcop-4.0-wp4c.0-distribution-audit`, initially clean at the Gate. The taskbook commit is verified separately; it is not inserted into the delivery parent chain. Existing `D:\FCoP` changes and dogfood files are preserved. No branch switch, stash, reset, cleanup, migration or rule redeployment was performed there.

## Source identities established before the stop

The fully read `src/fcop/rules/__init__.py` declares `fcop-rules.mdc` and `fcop-protocol.mdc` and loads them with `importlib.resources` from `fcop.rules/_data`, decoding UTF-8. `get_rules()` and `get_protocol_commentary()` return their text. Version readers extract the corresponding frontmatter version keys. This identifies the loader's declared inputs, not completion of the full canonical-authority audit.

The tracked Host header declares four deployment targets: AGENTS.md, CLAUDE.md and the two Cursor rule files. The six raw Git-blob identities are recorded in the Context report. No generation provenance or byte-reproducible regeneration has been proven in this run.

## Required verification accounting

| Requirement | Current evidence / status |
|---|---|
| Input Gate, taskbook parent, path, SHA-256 | Verified before audit. |
| Rule-related tests | NOT_RUN after prerequisite hard stop. |
| Canonical / four Host copies | Six raw-blob byte/line/hash measurements available; structural comparison incomplete. |
| wheel / sdist inventory | NOT_RUN; no fresh artifact built. |
| Project / MCP distribution call graph | NOT_COMPLETED; loader only read, not the complete call graph. |
| Mandatory inputs UTF-8/LF | Only six measured blobs verified; full inventory NOT_COMPLETED. |
| Normative and reverse-rule mapping | NOT_COMPLETED; denominators not established. |
| Report formatting / diff / allowlist | Delivery validation, recorded in Manifest and remote receipt. |
| Remote parent chain / five SHA-256 | To be measured after delivery; final PR receipt is the authority for that result. |

Full v3/v4/MCP regressions, dry-runs and deployment recovery probes were not run. Earlier WP4B results are historical inputs, not new test results. No production, test, Schema, rule, MCP or Host file was changed.

## Read coverage limitation

The WP4C.0 taskbook, WP4B Gate and rules loader were read in full. Searches and metadata extraction do not count as deep reading. The long Host text read was truncated and is not claimed complete. The remaining mandatory source/specification/history/report set, including the full WP4B evidence package, was not fully reviewed before the stop.

This is a preserved partial baseline and blocker delivery, not a completed WP4C.0 baseline.

---

# WP4C.0a resume — completed baseline audit

This appended record supersedes only the *current status* of the preserved WP4C.0 BLOCKED record above. It does not retract the earlier correct stop or claim those earlier unperformed checks ran then. Audit date: 2026-09-07. Executor: ME (solo); ADMIN's fixed taskbook is the decision carrier, these reports the execution evidence. No additional dogfood task/initialization/archival writes were made outside the six-file allowlist.

## Fixed authority and Gate distinction

- Input/taskbook: `eb086ee43f345a4d93ffb520049dc8af08712d3b`; SHA-256 `9db3b811048618cf4fe1baf4352c9e980f2d6da3e061f41709f553520e8e589c`.
- Source ancestor: `0c61f7d3108777adb7aaf375324616c004fcaf7d`; preserved blocked ancestor: `4420bf6cdd456e328230015bcffef4fdabf615a8`. Both verified with `git merge-base --is-ancestor`.
- Engineering discussion text SHA-256: `25e70e221d6b54072503a8ec7224df33000fa63c0b12a64c148d86a0081b6762`, verified against GitHub fixed bytes and local Git blob. It is NOT normative, NOT contract-frozen, NOT licensed for bundling.
- New worktree: `D:\FCoP-wp4c0a-baseline-resume`; branch `review/fcop-4.0-wp4c.0a-baseline-resume`; initially clean at input. Original workspaces are untouched.
- `git diff --quiet aad88ae5... HEAD -- src mcp/src spec tests .cursor/rules AGENTS.md CLAUDE.md` returned 0 before report edits. Audited production/rules remain identical to the accepted WP4B Gate tree.
- EN and ZH frozen specs each have 73 numbered F4 clauses, ordered IDs identical; each full file is byte-identical to `aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6`. The historical candidate banner is not an authorization to rewrite the frozen files.
- Taskbook §0/§7 corrects the old stop semantics. Legacy hazards and constitution freeze/licensing decisions are documented future entry requirements, not reasons to leave this read-only inventory unfinished. No frozen-Core change is necessary to classify them.

Current accounting: `WP4C_0_AUDIT_BLOCKERS: 0`; `WP4C_1_ENTRY_BLOCKERS: 1` (one unresolved ADMIN constitution-source/effect/license freeze Gate, with constituent questions). This is audit completeness, NOT a declaration that the old distribution system is safe for v4.

## Authority, source and consumer graph (static, not executed)

`src/fcop/rules/__init__.py` → cached UTF-8 `importlib.resources` readers → two bundled mdc inputs → `project.py:_plan_protocol_rules_deployment` → `Project.deploy_protocol_rules` → four whole-file Host outputs.

- Canonical editable v3 rules: `src/fcop/rules/_data/fcop-rules.mdc` (rules 3.2.5) and `fcop-protocol.mdc` (commentary 3.2.5). Root copies are outputs, never input authority.
- `src/fcop/templates/roles/_COMMON-FCOP-3.2.5.md` is a separate authoritative *injection block* for role workflow, not the engineering constitution. `scripts/inject_workflow_constraint.py:31` reads it and replaces anchored sections in 34 role files (17 roles × two languages). The 67 team data files comprise 64 Markdown documents plus two catalog README files and one index JSON; five indexed presets include solo. Body-level protocol overlaps are classified with Rule 0.a; role-specific duties are Profile material, not additional Base requirements.
- `fcop.teams` derives five presets from index.json, reads zh/en templates with importlib.resources, caches index data and returns text. Project role deployment maps README → TEAM-README, plus TEAM-ROLES, TEAM-OPERATING-RULES and roles into workspace shared/. This is a separate legacy Profile deployment path, not a v4 Rule Manifest.
- No v4 rule-module manifest, adopted Host selector, or thin entry generator exists in these paths. Candidate categories in the Disposition report are analysis labels, not implemented package IDs.
- `scripts/patch_rules_version.py` is a historical direct AGENTS/CLAUDE string-rewrite utility, not a canonical generator. It conflicts with the desired single-source maintenance model; not run.
- Generic `fcop.rules.get_spec()` defaults to old packaged v1.1 text. MCP's accepted versioned resources instead use `mcp/src/fcop_mcp/_specs.json`; do not confuse these authorities.
- MCP `server.py:4031–4033` installs version routes and resource replacements. v3 redeploy delegates Project; v4 PROFILE_DEPLOY is unavailable, and Project's explicit boundary marks `deploy_protocol_rules` V4_MUTATION_REJECTED. No fallback to legacy writing is permitted.
- For v4, six rules/guidance resources return typed `toolkit:V4_GUIDANCE_UNAVAILABLE`. Two specs, team catalog and three templates remain read-only. These are WP4C.4 closure points AFTER module/manifest contract and implementation, not invitations to return old guidance now.
- WP4B Gate, Manifest and all five reports were reviewed: accepted surface 46 tools (only additive reopen_task), 11 static resources, three read-only Profile templates; trusted evaluator belongs at server construction, never in resource text or business request parameters. Earlier 29/29 CI and 119/119 Conformance figures are historical evidence only.

## Deployment and invalidation facts

Source anchors: `src/fcop/project.py:1379–1483,5249–5258,6374–6464,6536–6580`; `src/fcop/v4/boundary.py:39`; MCP `server.py:3557–3653`.

| Question | Observed implementation / risk |
| --- | --- |
| Defaults/order | force=True, archive=True; Cursor rules → Cursor commentary → AGENTS → CLAUDE, always all four; no adopted-host filter. |
| Ownership | No managed blocks, content-owner digest or project-owned region detection. Existing target is either skipped or replaced wholesale. |
| force=False | Existing targets skipped, missing targets still generated; mkdir happens before the skip. Not a true dry-run or all-or-nothing plan. |
| Archive | Prior target is moved into .fcop/migrations/<local-second-stamp>/rules/<relative-path>. Timestamp precision is seconds; repeated writes in one second may reuse archive targets. No unique transaction directory guarantee. |
| Partial failure | Archive move precedes write_text. Failure can leave a missing/partial target or earlier outputs updated and later ones old. Source comment saying atomic-write is not implemented by plain write_text. |
| archive=False | Explicitly destroys previous target bytes without a backup. Existing test test_force_no_archive_overwrites_silently acknowledges this. No such operation ran here. |
| Repeatability | Static output formula contains packaged versions/text, no root path, randomness or timestamp. Archive paths and returned DeploymentReport are environment/time dependent. Whole deployment is not transactional. |
| Rollback/receipt | Archived files permit manual recovery when still available; no durable append receipt, staging transaction, verified automatic rollback, or crash-recovery proof. A returned dataclass is not a persistent receipt. |
| Cache/invalidation | Rules and team index cached per process. Package upgrade does not update a running process or existing Host files; restart and explicit deployment are separate. |
| Version check | Local reader examines only Cursor rules version, accepts legacy sentinel and ignores UTF-8 errors. Package version regex scans full text. No four-file digest reconciliation; equal versions can conceal body drift. |
| BOM | Commentary begins with BOM. _strip_yaml_frontmatter tests startswith('---\\n') and therefore leaves this frontmatter intact. Existing combined Host files contain embedded BOM and alwaysApply/version metadata. |
| Authority | Existing root files are FCoP's own development entry AND a deployed downstream-style payload, but NOT the generator input. A named development manual/constitution is not yet adopted there. |

These hazards are classified, not repaired. WP4C.0a §6 prohibits generator execution; therefore no isolated deployment smoke or fresh rule generation was run. Proposed staging/ownership/receipt semantics must be settled by a later fixed taskbook, not borrowed from Core lifecycle receipts without authorization.

## Actual retained artifact audit

Inspected existing fixed WP4B artifacts read-only at `D:\FCoP-wp4b3-artifact-proof`; did not build, install or publish. Rehashed archive bytes and compared every source-package member to the current input Git tree.

| Artifact relative path | Archive SHA-256 | Package members | Exact Git bytes | CRLF-only differences | Other differences |
| --- | --- | --- | --- | --- | --- |
| final-dist-fcop/fcop-3.2.5-py3-none-any.whl | 418e352fff133b1e58471da16d6bde7e6f79f8420419f5b82618ed46dad4a4bc | 144 | 13 | 131 | 0 |
| final-dist-fcop/fcop-3.2.5.tar.gz | 471ff35398f306fb0a01c8ce0abf821c057d83e77e553904cc0da564a54e69ad | 144 | 13 | 131 | 0 |
| accepted-dist-mcp/fcop_mcp-3.2.5-py3-none-any.whl | bd80cbbfe3446d5df4e0f2b0ab75807b2dcba5500281b2783b266b0a31670a89 | 21 | 10 | 11 | 0 |
| accepted-dist-mcp/fcop_mcp-3.2.5.tar.gz | 3b23b3b871c791abb59967e3613d79869ce78655797972fa2ae0ec2d1a733973 | 21 | 10 | 11 | 0 |

Both fcop artifacts carry 14 rule data files + 67 team files + the common role block = 82 rule/template source payloads, four old EN/ZH spec texts included in the 14. They also carry eight legacy and 12 v4 Schema payloads under fcop/_data/schemas; that is packaging evidence, not a change authorization. Both MCP artifacts carry no canonical rules or team templates, but do carry _specs.json containing v3/v4 EN/ZH specification payloads. The resource parity test checked all four against Git.

Path mapping: fcop wheel path = source path minus `src/`; fcop sdist path = `fcop-3.2.5/` + source path. MCP wheel path = source minus `mcp/src/`; sdist prefix `fcop_mcp-3.2.5/src/`. All 82 listed source payloads occur in both fcop archives. The four repository Host outputs are absent. The engineering constitution is absent. Archive contents have CRLF differences as explicitly counted above; text equality after newline normalization is NOT byte equality or a new build result. Existing package metadata remains 3.2.5 and is not a public 4.0 release.

Root and MCP pyproject package inclusion scopes confirm these paths. `taskbooks/**` is not included by the declared sdist source allowlists; no authority to vendor the discussion draft was inferred.

## Path-level rule/source/output inventory — 86/86

Two primary rule sources + twelve other bundled rule-data files + 67 Profile template/catalog files + one common injection source + four Host outputs. All entries have an explicit disposition class; full primary-text semantic disposition is in the companion report. A file is not counted as an independent normative rule merely because it is present. Common source and role copies must not both become authority for duplicated text.

| Path at input | Class / consumer | UTF-8 bytes | LF lines | BOM | SHA-256 |
| --- | --- | --- | --- | --- | --- |
| .cursor/rules/fcop-protocol.mdc | HOST_ADAPTER / generated legacy output | 116250 | 2328 | true | 32b621e0332000f6a78230a47ee715468a964e8e9d93e184acfce5f16805e9ff |
| .cursor/rules/fcop-rules.mdc | HOST_ADAPTER / generated legacy output | 75764 | 1359 | false | f38a204bde056e96aee06c4a0e418c3ac2eb6d89e74489b482ecc534a82fd6f2 |
| AGENTS.md | HOST_ADAPTER / generated legacy output | 192003 | 3702 | false | 796281fea0c4d572d805c30f5e0651bc2aa72a8fd34738fcc7158354fc4cd5d2 |
| CLAUDE.md | HOST_ADAPTER / generated legacy output | 192003 | 3702 | false | 796281fea0c4d572d805c30f5e0651bc2aa72a8fd34738fcc7158354fc4cd5d2 |
| src/fcop/rules/_data/agent-bringup-prompt.en.md | LEGACY / install, bringup or ADMIN guidance | 12347 | 287 | false | b519c83a588200d6af5d52fe2f0edec2f65a584b4f6f7261ddbf4e5dcf216837 |
| src/fcop/rules/_data/agent-bringup-prompt.zh.md | LEGACY / install, bringup or ADMIN guidance | 17911 | 361 | false | 1d0d26f827585b8f4bc3540dc0f5a5fe48ae00ce8f54b3a7ea5bbfaa3274fb7c |
| src/fcop/rules/_data/agent-install-prompt.en.md | LEGACY / install, bringup or ADMIN guidance | 2935 | 86 | false | e71c0eaa084bd75cf9ce7947eae25c0c4d126affe2e52fb069fafae70abdc496 |
| src/fcop/rules/_data/agent-install-prompt.zh.md | LEGACY / install, bringup or ADMIN guidance | 2771 | 76 | false | 92178af0a81acb4fdfe67ecca11d5a520bf3ed80a46df1b1493a591b2ab18d0e |
| src/fcop/rules/_data/fcop-protocol.mdc | LEGACY / canonical 3.2.5 source | 117608 | 2356 | true | 8ac413b1c39238df82a175d108c166c58c27fbe833b202470e140755780250d3 |
| src/fcop/rules/_data/fcop-rules.mdc | LEGACY / canonical 3.2.5 source | 75839 | 1359 | false | 24f42cfe76063bd39358cdb03a59e8d4e6b391c36bc9749302185252a84d1686 |
| src/fcop/rules/_data/fcop-spec-v1.0.en.md | LEGACY / historical specification | 34436 | 506 | false | 1c1feb55157fe3270e20bcdbe5363a04a5ecb68b8d2ed069d02a546f2e3349de |
| src/fcop/rules/_data/fcop-spec-v1.0.zh.md | LEGACY / historical specification | 32470 | 501 | false | f21a8231d72c99eaad97e77088876a19a70642040aafa27a31d8b9866893a9a8 |
| src/fcop/rules/_data/fcop-spec-v1.1.en.md | LEGACY / historical specification | 35723 | 520 | false | 13a4cae0db79d0094b796683a76bc40ef8fcd4ade3be739737fd3ecc52d1051c |
| src/fcop/rules/_data/fcop-spec-v1.1.zh.md | LEGACY / historical specification | 34693 | 523 | false | 987347c1ab1748cf1b124173dccf6833c324f23cae712aa2c9b6ccc18629e6fc |
| src/fcop/rules/_data/internal-readme.en.md | CATEGORY_MODULE / knowledge guidance | 3999 | 119 | false | e2a9491440f051dbc6d3c36fd54c474e985148ee28db911bf360b22f82d72936 |
| src/fcop/rules/_data/internal-readme.zh.md | CATEGORY_MODULE / knowledge guidance | 5391 | 135 | false | c9a9960b9db96145695f520fd2eef6b0d3177ff6cc8021be02b0a048f63ea61c |
| src/fcop/rules/_data/letter-to-admin.en.md | LEGACY / install, bringup or ADMIN guidance | 35788 | 772 | false | cd313d5963b644faf29fb42fce04eb66d104d77bd167ab26df4714d02458f6f0 |
| src/fcop/rules/_data/letter-to-admin.zh.md | LEGACY / install, bringup or ADMIN guidance | 34479 | 690 | false | e64a969ae5405fff4556fbf35a4f707793ea0a6778c31d98522e5a370b56fba7 |
| src/fcop/teams/_data/dev-team/README.en.md | CATEGORY_MODULE / adopted Profile templates | 3982 | 120 | false | 45e888022bafc0c1a377d4a4517698a7d6e57a18f628a45fdfae7ad12618f0e7 |
| src/fcop/teams/_data/dev-team/README.md | CATEGORY_MODULE / adopted Profile templates | 3603 | 106 | false | 2ec172c249b88d20bf399e0f4897221e66efb5d8bdacb2328686f978864a6b36 |
| src/fcop/teams/_data/dev-team/roles/DEV.en.md | CATEGORY_MODULE / adopted Profile templates | 7254 | 206 | true | a917d26cf679e84a98d1e388449be7f7689f2fa74773d6b52dbe46fe093a0315 |
| src/fcop/teams/_data/dev-team/roles/DEV.md | CATEGORY_MODULE / adopted Profile templates | 7656 | 199 | true | dcb5f95383c8156563ff8421e382ef7f35bb2602db49b5b794f7ad47989e73ac |
| src/fcop/teams/_data/dev-team/roles/OPS.en.md | CATEGORY_MODULE / adopted Profile templates | 7663 | 217 | true | c3917b1b1fc381fcd323bcf3bfb7a51493394937f1a8728cd6f22824e6dff374 |
| src/fcop/teams/_data/dev-team/roles/OPS.md | CATEGORY_MODULE / adopted Profile templates | 7847 | 208 | true | 82b34908482c8c682214b82e4eabe3da5ceb275ce4565ba1e4a654168ba9ab3f |
| src/fcop/teams/_data/dev-team/roles/PM.en.md | CATEGORY_MODULE / adopted Profile templates | 9620 | 262 | true | 040e20a26e438630ffa970060f2f9e37e47a80175a6832c58fa378a496fd6d6a |
| src/fcop/teams/_data/dev-team/roles/PM.md | CATEGORY_MODULE / adopted Profile templates | 10119 | 253 | true | 348978298f1a7e005126fcbcee54ea6a744ccf0ef95f2de16312f011180fab51 |
| src/fcop/teams/_data/dev-team/roles/QA.en.md | CATEGORY_MODULE / adopted Profile templates | 7351 | 216 | true | 4607972c94c3c8627d8572e43b2d0ec6c24e4d2afebaf8b75f414abf348f238b |
| src/fcop/teams/_data/dev-team/roles/QA.md | CATEGORY_MODULE / adopted Profile templates | 7766 | 209 | true | 69c8d17190075f519025721060caabf6bc3e601592b228be9fc2e0e65ee41e3e |
| src/fcop/teams/_data/dev-team/TEAM-OPERATING-RULES.en.md | CATEGORY_MODULE / adopted Profile templates | 5562 | 192 | true | 46290e5577458abc5c8fd1760101978c9bd3e998e49efbb8111bc15fa5143328 |
| src/fcop/teams/_data/dev-team/TEAM-OPERATING-RULES.md | CATEGORY_MODULE / adopted Profile templates | 5278 | 183 | true | e3838845a01db5e4eb06143e6d79feb16ccae54cd936c7795ff9d1131a31fa15 |
| src/fcop/teams/_data/dev-team/TEAM-ROLES.en.md | CATEGORY_MODULE / adopted Profile templates | 3307 | 104 | false | fc097e8a1111ad113d5c3bbc2d8d42038b92758f15fa11d8245927879a1c2091 |
| src/fcop/teams/_data/dev-team/TEAM-ROLES.md | CATEGORY_MODULE / adopted Profile templates | 2884 | 101 | false | d98c3189fb1512a3a9561d6d623c9314277c8d56b9eec18d21e40a54185ef1f2 |
| src/fcop/teams/_data/index.json | CATEGORY_MODULE / adopted Profile templates | 3430 | 89 | false | ac5a828c115f0e8ee92b5d5f2675db778c1d8c3751e837eed97e7791379f9e2f |
| src/fcop/teams/_data/media-team/README.en.md | CATEGORY_MODULE / adopted Profile templates | 3397 | 100 | false | 1d8a087229935e919dc1f5459f2bc8703f790544d3faf148171a55abde07c0bb |
| src/fcop/teams/_data/media-team/README.md | CATEGORY_MODULE / adopted Profile templates | 3372 | 93 | false | fc50cf9c0f0bf8d0c7fc2d603133525d65ba54997bcec32d2418f67c2345af83 |
| src/fcop/teams/_data/media-team/roles/COLLECTOR.en.md | CATEGORY_MODULE / adopted Profile templates | 7211 | 213 | true | 383358cd3ebdcb88a559864e89d1f6d6fac6d3f77b7683270c6a64bcbe8fbb21 |
| src/fcop/teams/_data/media-team/roles/COLLECTOR.md | CATEGORY_MODULE / adopted Profile templates | 7863 | 209 | true | 6613fe5ad37bf2d0d96f3e758e787bf23c036a060c18fd33959f3640fa728693 |
| src/fcop/teams/_data/media-team/roles/EDITOR.en.md | CATEGORY_MODULE / adopted Profile templates | 7215 | 203 | true | 37e07c2ab0788e2f838d5945e72bee37ec001b44f720fc7eda2b2d4d06541e54 |
| src/fcop/teams/_data/media-team/roles/EDITOR.md | CATEGORY_MODULE / adopted Profile templates | 7745 | 200 | true | 708a4096486a44dbcfec297fce2e7f6553c257b12cd6a83bacc80795b52f95aa |
| src/fcop/teams/_data/media-team/roles/PUBLISHER.en.md | CATEGORY_MODULE / adopted Profile templates | 8571 | 223 | true | de85f9185a4f1f300935edefd01c198c57c6392daf59e6171d69db523aa09fe5 |
| src/fcop/teams/_data/media-team/roles/PUBLISHER.md | CATEGORY_MODULE / adopted Profile templates | 9121 | 219 | true | 2831e3a32c55a33c6d722602601ad552a8c87c53431518fff97249d529affd56 |
| src/fcop/teams/_data/media-team/roles/WRITER.en.md | CATEGORY_MODULE / adopted Profile templates | 7118 | 203 | true | 424c9b66212dece1b029b64e47f62d4854b9e9c72b52f9654620800a162c39eb |
| src/fcop/teams/_data/media-team/roles/WRITER.md | CATEGORY_MODULE / adopted Profile templates | 7643 | 199 | true | 052441bc21b1ac8f7b5637e8e8c0e4c4cb90046ca73990004e32870cb62a5ccc |
| src/fcop/teams/_data/media-team/TEAM-OPERATING-RULES.en.md | CATEGORY_MODULE / adopted Profile templates | 5658 | 178 | true | 159489953a35f863d6e815a1d905f8dc68a2b50634efcb449f0952a2b726eef2 |
| src/fcop/teams/_data/media-team/TEAM-OPERATING-RULES.md | CATEGORY_MODULE / adopted Profile templates | 5523 | 166 | true | 960ea52dd3c3fdc3fc0b8e9ecd54d5a856b7669f22561df490f9cedf857088f8 |
| src/fcop/teams/_data/media-team/TEAM-ROLES.en.md | CATEGORY_MODULE / adopted Profile templates | 3059 | 102 | false | 76aed68e75c1cf187313eff9a039fd614f2529bc44c657e764972485cef4ee1d |
| src/fcop/teams/_data/media-team/TEAM-ROLES.md | CATEGORY_MODULE / adopted Profile templates | 3044 | 102 | false | 30ce2b9da56b645709c097e1720205b7327eccde31c844fc56210314550e08af |
| src/fcop/teams/_data/mvp-team/README.en.md | CATEGORY_MODULE / adopted Profile templates | 3534 | 103 | false | 5fdced44ef4203b062fa34085c99914ae9783bc097f2a17bfca7e986528af984 |
| src/fcop/teams/_data/mvp-team/README.md | CATEGORY_MODULE / adopted Profile templates | 3786 | 100 | false | a2ba6779e331edcd867ac8f0c67b02e3cb9d3e01e08a12e4245230e75bcb2f0e |
| src/fcop/teams/_data/mvp-team/roles/BUILDER.en.md | CATEGORY_MODULE / adopted Profile templates | 7547 | 216 | true | 73394bccee05eeeb0e63b51fd3bca13453db387cbbc6bc06e92cdbf7f1bb197d |
| src/fcop/teams/_data/mvp-team/roles/BUILDER.md | CATEGORY_MODULE / adopted Profile templates | 8115 | 213 | true | 6b42425ed5ac7aad36bc0ba4daa0874027529863ac787802bb734422ef052677 |
| src/fcop/teams/_data/mvp-team/roles/DESIGNER.en.md | CATEGORY_MODULE / adopted Profile templates | 7520 | 215 | true | 355fe8b6da5e1151dc91ab62fc0fa9579c1a6874ad9908635a3305d6923e65ef |
| src/fcop/teams/_data/mvp-team/roles/DESIGNER.md | CATEGORY_MODULE / adopted Profile templates | 8127 | 212 | true | af165a79ebd0fdbdb5f0fc3d1a3864279059942c7dde24c23747d4dd7a5e6274 |
| src/fcop/teams/_data/mvp-team/roles/MARKETER.en.md | CATEGORY_MODULE / adopted Profile templates | 8515 | 224 | true | 9ab0b421c75a2f899845f54f5ca012dfaa2fb0b08d656dea61c4d509b2aa7fb9 |
| src/fcop/teams/_data/mvp-team/roles/MARKETER.md | CATEGORY_MODULE / adopted Profile templates | 9145 | 220 | true | 99e14c5811b15674f84f69254fc4d88e84a76aa514cfa940d10a99125cf412c7 |
| src/fcop/teams/_data/mvp-team/roles/RESEARCHER.en.md | CATEGORY_MODULE / adopted Profile templates | 7530 | 214 | true | 0fb33f251476ac5242a6c2a51e2fba47ef8d89fb3b7f443fc8705c6184c22c58 |
| src/fcop/teams/_data/mvp-team/roles/RESEARCHER.md | CATEGORY_MODULE / adopted Profile templates | 8025 | 211 | true | 492fe03e8580d89f56e5a0d14e9894b40207b43d1a1d6cf791c2cbe98254e395 |
| src/fcop/teams/_data/mvp-team/TEAM-OPERATING-RULES.en.md | CATEGORY_MODULE / adopted Profile templates | 5504 | 173 | true | 61915593977e4589268e130a89f44dcec1a527c93742d63c4344b4e5c36a1831 |
| src/fcop/teams/_data/mvp-team/TEAM-OPERATING-RULES.md | CATEGORY_MODULE / adopted Profile templates | 5767 | 166 | true | 83a6effede7efc14957a79625db3af2ab56a1ff32ab55ebbd35c8d1c57351547 |
| src/fcop/teams/_data/mvp-team/TEAM-ROLES.en.md | CATEGORY_MODULE / adopted Profile templates | 3182 | 105 | false | 4838ae1edb5f620f9a04d53f3eef81128a6e483476381eac2b0603f1392b1c3a |
| src/fcop/teams/_data/mvp-team/TEAM-ROLES.md | CATEGORY_MODULE / adopted Profile templates | 3252 | 105 | false | 0597963c5dbe2acc016abcd66e87919747995de70791fe165af9e0105559808a |
| src/fcop/teams/_data/qa-team/README.en.md | CATEGORY_MODULE / adopted Profile templates | 3641 | 106 | false | d471ae236f2ef1da9da501920f2694ad1351c9c28e1a13a34695ba80178f77c2 |
| src/fcop/teams/_data/qa-team/README.md | CATEGORY_MODULE / adopted Profile templates | 3932 | 102 | false | 6be8d9968cd9f6d1a34a6da2f60955c04a050fe00ca49a44d271b499ca350520 |
| src/fcop/teams/_data/qa-team/roles/AUTO-TESTER.en.md | CATEGORY_MODULE / adopted Profile templates | 7313 | 206 | true | 3855035b08359f4ba74057428568806513868242ef4acbced0fe525a4ce2b696 |
| src/fcop/teams/_data/qa-team/roles/AUTO-TESTER.md | CATEGORY_MODULE / adopted Profile templates | 7885 | 202 | true | 89e208b097dee1c4107d4e008bd4fb618121846ed709b8baa5ca028fae8234c9 |
| src/fcop/teams/_data/qa-team/roles/LEAD-QA.en.md | CATEGORY_MODULE / adopted Profile templates | 8652 | 226 | true | afb26f01148b002ae99a05a30e19e359cbd51fad4a0d5bd0b25a9d04174d7e06 |
| src/fcop/teams/_data/qa-team/roles/LEAD-QA.md | CATEGORY_MODULE / adopted Profile templates | 9200 | 222 | true | af4ce0ad9dec4e6a936d1cd550a19bd99e60391b2b98909b574a0fa2876caf78 |
| src/fcop/teams/_data/qa-team/roles/PERF-TESTER.en.md | CATEGORY_MODULE / adopted Profile templates | 7857 | 218 | true | 1807f94b524621f8927f314e4bf88a75f00421cd89fb8d8b50fc84b58f03fb2f |
| src/fcop/teams/_data/qa-team/roles/PERF-TESTER.md | CATEGORY_MODULE / adopted Profile templates | 8203 | 215 | true | 0f68e285ace598003a488496f2d165dfd8ac9e90ce5c699c9dc0017f6963ec28 |
| src/fcop/teams/_data/qa-team/roles/TESTER.en.md | CATEGORY_MODULE / adopted Profile templates | 7054 | 205 | true | 642ffe1d6b079fcd6a558f0a0f95145487253d7d9e6fb826d9fe864845440705 |
| src/fcop/teams/_data/qa-team/roles/TESTER.md | CATEGORY_MODULE / adopted Profile templates | 7627 | 202 | true | 479a734e4d560466b58efba77b8d682d51af8f747ed0180ac1b0cdc37222f8e0 |
| src/fcop/teams/_data/qa-team/TEAM-OPERATING-RULES.en.md | CATEGORY_MODULE / adopted Profile templates | 5781 | 181 | true | 299a04b2e36f48e7161070c072dd0338d8d95c42ff56bdc833f877fddc3bed6e |
| src/fcop/teams/_data/qa-team/TEAM-OPERATING-RULES.md | CATEGORY_MODULE / adopted Profile templates | 5901 | 172 | true | 1e36c46c1ba7a29c5bf1cdf4bc9c9ea395fa9f8b622319097858e45fe14bf41c |
| src/fcop/teams/_data/qa-team/TEAM-ROLES.en.md | CATEGORY_MODULE / adopted Profile templates | 3297 | 107 | false | 0ec572dcfa6edeabb3cc9dd489dfe206aa351003ebc15a15339683e0ebf365b7 |
| src/fcop/teams/_data/qa-team/TEAM-ROLES.md | CATEGORY_MODULE / adopted Profile templates | 3222 | 104 | false | 34eecd9a120b402e1f6c5d874526fa499a29f719f1ccfecd5224fd90d2937484 |
| src/fcop/teams/_data/README.en.md | CATEGORY_MODULE / adopted Profile templates | 4868 | 118 | true | 96678f42654baea88276728d00953e0a7e60bc903a152f227e255eebf30ec889 |
| src/fcop/teams/_data/README.md | CATEGORY_MODULE / adopted Profile templates | 5645 | 105 | true | 9c601ca5419463436a0facf4805d3cf14569cad51c2e62375364a26d1e69c829 |
| src/fcop/teams/_data/solo/README.en.md | CATEGORY_MODULE / adopted Profile templates | 4488 | 120 | false | 2c66ae54e2a948333961446ff21c1d27f79e98eea7d97a1f8662fa9b013c71e2 |
| src/fcop/teams/_data/solo/README.md | CATEGORY_MODULE / adopted Profile templates | 4478 | 113 | false | a9da91c18beb1a1b02880725d95f10b1e7719064ac01e80f7e3ee0789839e6d7 |
| src/fcop/teams/_data/solo/roles/ME.en.md | CATEGORY_MODULE / adopted Profile templates | 11318 | 288 | true | 2c9082d10e9d442d672e74f98779db7fb858c3ace59f17ce25851027e62169b8 |
| src/fcop/teams/_data/solo/roles/ME.md | CATEGORY_MODULE / adopted Profile templates | 11468 | 259 | true | e3c4980a21d95c581a027e713fe77f0b3594c367269eec160b3a1ba04391d24a |
| src/fcop/teams/_data/solo/TEAM-OPERATING-RULES.en.md | CATEGORY_MODULE / adopted Profile templates | 7084 | 175 | true | 90336c1f1299786f522be078f5c2f283333c11e685cac30ad26ad6008b38a80d |
| src/fcop/teams/_data/solo/TEAM-OPERATING-RULES.md | CATEGORY_MODULE / adopted Profile templates | 6834 | 154 | true | a6f6ce00fc678b2dbf8703619c2cc54e30a1d6e49221a75eb2a4319f9e8a7e30 |
| src/fcop/teams/_data/solo/TEAM-ROLES.en.md | CATEGORY_MODULE / adopted Profile templates | 3757 | 96 | true | 52a9d7a7b2c6cd98735397a28c357c5d076142eed9e56fd18d8843261b88b8a7 |
| src/fcop/teams/_data/solo/TEAM-ROLES.md | CATEGORY_MODULE / adopted Profile templates | 3529 | 84 | true | 2c6e2cc9ddd30789cc83ccd435414a671f86a17f988e214189a6f4ad6c6c2706 |
| src/fcop/templates/roles/_COMMON-FCOP-3.2.5.md | CATEGORY_MODULE / role-block source | 7517 | 205 | false | cc1bba3351e3da0b48e607e026fe61c62d12157f5b5b30d95fb7a9f691282846 |


## Verification and read scope

- Current read-only pytest: 44 rule cases and three static-resource/spec-parity cases. Final combined rerun: 47 passed, three warnings in 3.87s, Python 3.12.9; warnings concern Traversable and jsonschema.RefResolver deprecations. No full v3/v4/MCP regression claim.
- Deployment test files were read as contracts, not executed: they call prohibited generators. Rule/data getters and resource tests do not run rule generation. Resource tests use isolated temporary workspaces, not existing dogfood.
- 104 mandatory rule/spec/code/doc/test blobs plus common source and two maintenance scripts = 107 strict UTF-8/LF Git-blob checks; 107/107 decode and contain no CR. 50 start with BOM. This is NOT a BOM-free or repository-wide encoding PASS. The Context report explains embedded BOM/control characters and narrower guard coverage.
- Primary canonical texts, EN/ZH frozen clauses, loader/deployment/route/resource functions, ADR-0006, getting-started EN/ZH, upgrade/release/checklist, rule tests, common block/injection scripts and prior reports/Gate/Manifest were read; package member enumeration is path/byte inspection, not a claim of line-by-line semantic review of every historical spec/team biography.
- History cross-checks: rule/Host release `9fb5fe1990b65b26b18888fc0c37df1d0da0fee4`; encoding repair `db18511770835629f39076c6b30b0cc095fddc0e`; Host ADR `a9d931d68c5f0811fb13ae5f7b9b7d5d2f7ecb83`; release SOP `f87de88a9bb861e9a975510e252cb51a31ba26b1`; MCP thin-adapter content `442de2748d0d5e657bfb3c8dc844457ca43d5114`. History is provenance, not a competing active instruction.
- Guides still contain old version-1 layout/examples and the absent spec/fcop-3.0-spec.md link. Upgrade prose overstates MCP wheel ownership of Host rules; actual data lives in fcop. Release checklist permits manual copying/patching and in-place ISSUE closure; release-process §E calls dissimilar combined outputs byte-identical to sources. Classify as version-scoped legacy/development documentation drift, not instructions to run now.
- The upstream blocked record remains a byte-for-byte prefix. No rules, Host files, Schema, production, tests, version, release configuration, main or CodeFlowMu changed.

See the other four current resume report sections for clause/section counts, Host evidence limits, context measurements and the 12/12 discussion-principle decision matrix. Final remote results belong in the Manifest and PR receipt; this report does not preclaim a push.
