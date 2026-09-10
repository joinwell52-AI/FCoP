# WP4C.5B Implementability Proof — pre-code record

## Authority and verified baseline

ME / solo executes ADMIN's fixed taskbook, not a self-signed Gate. Scope is WP4C_5B_ONLY, resuming FULL_WP4C_5. The fixed taskbooks are WP4C.5 at 3e48a344b3bf16c2ed45671a7fb458b14f50dd6e, WP4C.5a at c7986fb618b2f66c4ad2b157917f64a00bccf1c3, and WP4C.5b at a6f3ce278977b7121700de76ea6d832fe518533f. Their complete text and PR #27's two reports/Manifest have been read. Prior blocker documents are historical, not implementation results.

GitHub raw WP4C.5b Blob: 12749 bytes, SHA-256 f0501c7837e8e50668f8888d24e11b0929fafcf77ec2710d4c597deeb8fa5e2e, UTF-8/no BOM/LF. Commit API: direct parent c3ef6ccba14a93ac73935ae729b5f9b681693138, exactly one taskbook addition. New initially clean worktree D:/FCoP-wp4c5b-protocol-resume, branch review/fcop-4.0-wp4c.5b-protocol-resume, starts at that fixed taskbook.

Fixture-alignment commit 76ebfc6fedf9b55b436e866b7c80f532423cfd3c changes only the authorized condition in test_dist_21_24_assembly_compat_mcp.py. Pre-tree 1134d730e4c5ab23aa7b3ec91138da6981c2f009; post-tree 4f99c7261b63b6db81c500604a231defaca9f14b. Post-file: 6196 bytes, SHA-256 72b4c5a621775487b10b60dc789c27a67ecfd5a81eda28cc3563cbe6c878b572, Blob a3b831161d415a2aa7906688ceab9273b0dea090. Both inner assertions and all parameters remain. Two older authorized corrections remain, and no other frozen file may change.

## Measured red baseline and sole owners

Fresh Windows/Python 3.12.9 run, local src+mcp/src, PYTHONDONTWRITEBYTECODE=1, no pytest cache. Command: python -X utf8 -m pytest, selecting DIST-23/24/26/29 functions, tests/test_fcop_mcp/test_tool_surface.py and test_all_static_resources_and_disposition[v3], -q --tb=line -p no:cacheprovider --basetemp=D:/fcop-wp4c5b-baseline --junitxml=C:/Users/Administrator/AppData/Local/Temp/fcop-wp4c5b-baseline.xml. Result: 12 failed / 6 passed, 41.51 seconds; the 13 target nodes remain 1 passed / 12 failed, existing five MCP checks pass. Fixture alignment did not implement behavior or conceal red tests.

All following rows have one owner, WP4C.5, and public entry Project.rule_distribution. Writes below are the intended implementation boundary, not a claim of completed implementation.

| Node | Baseline | Action; reads | Allowed writes / rejection |
|---|---|---|---|
| DIST-23[unversioned-v3] | FAIL | redeploy; strict existing version classifier + legacy getters | existing legacy writer only, force=False; preserve every existing Host file |
| DIST-23[explicit-v4-on-v3] | FAIL | apply; workspace declaration only | none; RULE_ADOPTION_REQUIRED |
| DIST-23[v4-no-adoption] | PASS | existing apply/adoption receipt check | none; RULE_ADOPTION_REQUIRED |
| DIST-24[3.0-rules] | FAIL | read_resource; legacy rules getter | none |
| DIST-24[3.0-protocol] | FAIL | read_resource; legacy commentary getter | none; exact Markdown str |
| DIST-24[3.0-guidance/sequential/en] | FAIL | read_resource; same legacy rules source | none; no v4 assembly claim |
| DIST-24[3.0-team] | FAIL | read_resource; existing team catalog getter | none; no new store |
| DIST-24[4.0-rules] | FAIL | read_resource; strict Manifest + all 18 artifacts | none; manifest/artifact errors on drift |
| DIST-24[4.0-protocol] | FAIL | read_resource; frozen specification identity | none; artifact error on source drift |
| DIST-24[4.0-guidance/sequential/en] | FAIL | read_resource; validated Manifest and existing selection | none; selection/artifact errors |
| DIST-24[4.0-team] | FAIL | read_resource; typed unavailable | none; fixed reason, no fixed-role Core claim |
| DIST-26 | FAIL | inspect_layers; fresh package, adoption/deployment chain, snapshots and target bytes | none; structured chain/drift errors |
| DIST-29 | FAIL | shadow; validate external read authorization before downstream access | none; RULE_ADOPTION_REQUIRED before any downstream I/O |

## Version routing, resource surface and representation

Existing Project construction/binding owns workspace classification. Distribution reuses parse_json(classification=True), safe_path and _Creation.open_if_declared, never JSON last-key-wins. A current v3 declaration enters a distribution-local legacy action router: unversioned redeploy delegates Project.deploy_protocol_rules(force=False); read_resource delegates existing getters. Explicit v4-on-v3 rejects before writer. Current v4 stays behind _Creation's bound entry. Missing/ambiguous/changed declarations fail closed. No v3/v4 migration or second writer.

Existing measured FastMCP registrations: 46 tools, 11 static resources, 3 templates (PR #27 real runtime listing, unchanged input; five current snapshot/resource checks also pass). Keep every tool, old static URI/MIME and old template. Only additions: fcop://team (application/json), fcop://guidance/{assembly}/{language} (text/markdown), giving 46/12/4. The historical 45/11/3 snapshot is immutable history; only the current v4 snapshot changes additively.

Project is the sole semantic reader. MCP calls it once for a requested rules/protocol/team/guidance resource; Relay's in-process session uses the same FastMCP handlers and no network. No adapter Manifest loader, module selection or source-digest implementation. Existing unrelated spec/profile resources retain their accepted behavior.

WP4C.5b resolves representation: v3 rules/protocol text is byte-identical to getters, no banner; v4 protocol remains a machine identity dict in Project, rendered by a small pure MCP function in path/revision/sha256 order. v4 rules is the full Manifest dict in Project and lossless deterministic Markdown with a canonical JSON code block in MCP. No MIME changes. Direct/Relay exact-byte tests lock representation; typed metadata remains separate from Runtime consumption.

Strict read requests validate action fields, URI spelling/segments, explicit language/assembly, no executable fields or network effects. Frozen fixture administrative metadata is inert input, never authority or a trigger to adopt. Guidance selection reuses existing select and its closed module/language validation; an internal language-only selection binding is not a Host Profile adoption. Package reads use existing offline loader/raw SHA, with repeated raw-input comparison for observable drift and no cache. Fixed specification identity is bound to aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6, spec/fcop-4.0-spec.md, SHA-256 0c5005ec754ee71d735e02c9ea403adbc35e8dff9ce98c13d8a42040cacbc8e9 (26218 raw bytes). Packaged identity is a citation, not a duplicate specification or registry; source checkout verification must detect changed bytes without requiring a network/spec download in wheels.

## Five independent facts

Disk/index: current strict package read, returning the same hash and uncached_current_read evidence, not invented old cache. Adoption: adoption_chain's verified receipt and ADMIN selection reference, independently of current disk version. Host: deployment_chain/verify_history/recorded_inputs and current target bytes; explicit drift fact, no implicit redeploy. Runtime: always None. Disk changes do not mutate old adoption/deployment snapshots; restart reads identical immutable evidence. Reuse accepted receipt validators, do not alter Host projection, apply or rollback semantics. No new authoritative store.

## Shadow boundary and actual consumer plan

Before downstream access: require deploy=False and a complete external authorization ref; strict JSON UTF-8/no BOM/LF, duplicate/unknown-field rejection, raw SHA, exact scope/kind/root/allowlist binding. Lexical root/relative-path validation must not call stat/resolve/open on downstream. Reject an authorization file inside its downstream target before reading it. No caller evaluator.

After admission: at most 16 explicit ordinary relative files, no glob, traversal, UNC, devices, symlink/junction or directory scan. Reuse distribution external_file/path safety, verify each full-file expected digest, and reread authorized bytes to detect observable changes. Return only bounded path/size/hash and literal version-pin facts, never file bodies or arbitrary matches. Authorization governs filesystem reading only, not F4.7 authority. No subprocess/install/start/deploy in shadow.

Real CodeFlowMu current local fixed ref is b961b16dd0c8863ead6995d963fe0ca576a8abaa; historical isolation evidence ref 789cb3fa8a007f050248784f7daf689808a549a2. Read-only source inspection of packages/codeflowmu-runtime/src/_external/fcop-client.ts:57 onward confirms literal adopted versions 3.2.5/3.2.5, exact policy, missing/unparseable/nonmatching rejection. Historical conclusion is evidence, not this run's test result. Plan: bind a small explicit allowlist to fixed Git Blob SHA values, verify present allowlisted bytes equal that fixed ref, run public shadow under an external fixed authorization, and compare before/after identities. Existing dirty product files outside the allowlist remain untouched; no product execution, checkout, installation or broad data traversal. Independently inspect bounded startup/version source and historical evidence for no automatic upgrade. Report current and historical refs separately; do not claim whole dirty tree is clean. Excluded v1.0-rc.1 stays development-transition-only, never ordinary guidance, manifest, default package or FCoP contract.

## Reuse and implementation review

Reuse: strict Encoding/classification, offline Manifest loader and sha, selection, external path safety, receipt chains/snapshots, legacy rule/team getters and legacy writer, existing Project facade, existing FastMCP registration/session transport. Planned private additions are small read/resource and shadow helpers plus an MCP renderer; no dependencies, database, cache framework, registry, second Runtime, background component, updater, new public facade or lifecycle state machine.

This pre-code review finds the previous representation and baseline conflicts resolved by ADMIN. Implementation can proceed within this scope. It does not sign an acceptance Gate. Verification and any discovered failures will be recorded in RESULT before three-commit delivery; a new out-of-scope contract need still stops execution.
