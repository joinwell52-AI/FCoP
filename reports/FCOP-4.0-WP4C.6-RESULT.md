# WP4C.6c Windows materialization closeout result

## WP4C.6c continuation (supersedes status, preserves all history below)

ADMIN taskbook: commit `7b61d4ce1a1f5c4f69bca77dfea959d06e3c763c`,
`taskbooks/fcop-4.0/WP4C.6c/01-Windows-LF-Materialization-Policy-and-WP4C.6-Resume-v1.0.zh.md`.
GitHub Contents API raw Blob: 5202 bytes; SHA-256
`b9063ec71228fcfd3dfd59e920ce56f0e5b21bdd55096ee05773f096f7e60698`.
The full taskbook was read before editing. Its parent is the preserved blocked final
implementation HEAD `34841330604e32c473a538afb634a81334eca8ad`.

The old final-HEAD runs remain failed historical evidence:
FCoP [34310336551](https://github.com/joinwell52-AI/FCoP/actions/runs/34310336551)
and MCP [34310336555](https://github.com/joinwell52-AI/FCoP/actions/runs/34310336555).
Their eight Windows failures and skipped downstream package jobs were not relabelled
or used to request a Gate. ADMIN authorized only the materialization policy correction.

Policy-only commit `a46a51b4cf6b2711ab0c1e526019c6d7ea284fad` has the taskbook
as its sole parent and changes only `.gitattributes`: the existing two Schema lines
are retained and exactly the four taskbook lines appended. No source, test, workflow,
Schema, frozen specification, canonical rule text, dependency or release file changed.
The previous FcopError alignment is retained. No renormalization, configuration change,
force push, main merge or CodeFlowMu write was performed.

### Native Windows checkout proof

Command: `git worktree add --detach D:/FCoP-wp4c6c-windows-policy-readback HEAD`
from the policy commit. No `-c core.autocrlf=false`, checkout override, global or local
Git configuration change was used. `git config --show-origin --get core.autocrlf`
returned `file:D:/Git/etc/gitconfig true`. Windows Python is 3.12.9.

For every path below, `git check-attr text eol -- <path>` returned `text: set` and
`eol: lf`. Direct `Path.read_bytes()` equals both the policy HEAD's `git show HEAD:path`
and the blocked baseline's raw Git Blob. All 21 files are strict UTF-8 without BOM or
CR, with unchanged SHA-256 and byte length. The fresh checkout was clean after this check.

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| spec/fcop-4.0-spec.md | 26218 | 0c5005ec754ee71d735e02c9ea403adbc35e8dff9ce98c13d8a42040cacbc8e9 |
| spec/fcop-4.0-spec.zh.md | 24341 | 7302983e8a6e2225470d3da8f2e768abd4dfcc1c7adbe17116a64dda7e357c19 |
| src/fcop/rules/_data/v4/authorization.en.md | 2128 | 96c1c18bab3a879b51a1e2d0041f1f08eeae685185ad9489f13ed0a999f9a00b |
| src/fcop/rules/_data/v4/authorization.zh.md | 2033 | 13b82fdeb7c577a68a70d94303bf090eac42ce44c137c1a166b23f7014c1b854 |
| src/fcop/rules/_data/v4/compatibility.en.md | 3521 | a65385a3a2e68d043c65f9b8c34c6ac311bb7f9b2ea1e9f4c162886f858a64d8 |
| src/fcop/rules/_data/v4/compatibility.zh.md | 3024 | d6ce267c8216a2d6df2e5e601f4d237d941778a36687eae1d310616f6170585e |
| src/fcop/rules/_data/v4/convergence.en.md | 2283 | ec3cf38b6dba4d3eb8447cc7cd25e947c06abed228c37c9d651f873662edc70e |
| src/fcop/rules/_data/v4/convergence.zh.md | 2114 | 2b5c2a52c33bc38e8c3c85fdd75d5de3c837cc483a29941ec02a61a059c1701a |
| src/fcop/rules/_data/v4/envelopes.en.md | 1743 | 0405885cbe3fe791c0e1a6c76da004d093d58cd55159ffeb3ca8c89e4ec045a3 |
| src/fcop/rules/_data/v4/envelopes.zh.md | 1672 | 0a69c9196e95185cf9e98b71af8c564be5797e26a71c5a9b7dc32d0735a08fef |
| src/fcop/rules/_data/v4/idempotency.en.md | 1720 | 1b100010d36342e6d98e9031429b3e11aad5657dfa953031e43bc4c99772a16a |
| src/fcop/rules/_data/v4/idempotency.zh.md | 1591 | 51c53931e02b1f39950f4a2f16b5e8e9a5f9d10b77f5ea1ad6b07c3e96385f08 |
| src/fcop/rules/_data/v4/lifecycle.en.md | 3041 | b6356c078ab00b893379f0b4f558616444ef4a4aa0e17432460719a9be362b2b |
| src/fcop/rules/_data/v4/lifecycle.zh.md | 2787 | 26b338914cffe2ea076f0e88133fc69617c91ecb149b3e40217baeef708cffef |
| src/fcop/rules/_data/v4/manifest.json | 11221 | 7efb1ba14df4d1ffbe164b8ec85dbf4316e7da4c0f367f3a506c78e4e29862d4 |
| src/fcop/rules/_data/v4/recovery.en.md | 3534 | aad4861efa59df69742c4bf577d57a553cbb170f6f92d61f6df74ec3ec503908 |
| src/fcop/rules/_data/v4/recovery.zh.md | 3099 | b19226071498f6414e11379b9d67cee36e4a79d65510fffefd14a021cd829000 |
| src/fcop/rules/_data/v4/relations.en.md | 1106 | 1b706c4ff76efb6edad40ab7985a0693eb9466da483d7024eb1f29668e022789 |
| src/fcop/rules/_data/v4/relations.zh.md | 1057 | fa51c77a568dae7f7cf41242b612ae2b2963075004aaebef533334a0466d3d42 |
| src/fcop/rules/_data/v4/workspace.en.md | 1920 | 06d4a9604fbab50ade36369f8f1d2950f099a241d659613cc78f1dd7e93555b3 |
| src/fcop/rules/_data/v4/workspace.zh.md | 1723 | 617009dc95cf4bedd252491334f45cf61fa1fe8ccf935f2127e2a1da9a49e30b |

Only these authoritative inputs and the existing Schema paths acquire the targeted LF
policy. Unrelated checkout files can still materialize as CRLF; that is not described
as raw LF parity. Normal wheel/sdist hashes may consequently differ from the previous
all-LF checkout, while canonical member bytes must remain exactly equal.

### WP4C.6c validation evidence

Validation is running in the fresh default Windows checkout, not the earlier all-LF
execution worktree. `PYTHONDONTWRITEBYTECODE=1`; PYTHONPATH explicitly points to that
checkout, its src and mcp/src. Alignment passed 2/2. The single full native run selects
`tests/conformance/rule_distribution_v4 tests/test_fcop tests/conformance/v4 tests/test_fcop_mcp`
with `-q -x -p no:cacheprovider`, fresh basetemp `D:/fcop-wp4c6c-full-native-01`, and
JUnit `C:/Users/Administrator/AppData/Local/Temp/fcop-wp4c6c-full-native-01.xml`.
It includes all 176 Distribution nodes (including the 20 targets), 119 Core nodes,
1459 FCoP nodes and 158 MCP nodes; its completion is not preclaimed here.

Both canonical Ruff commands passed. Mypy passed for FCoP source (55 files), MCP
source (18), and MCP tests (11). Frozen Core and Distribution tree identities remain
`24ab264c6bca9a3183ee270becb552f22a4c4f9e` and
`4f99c7261b63b6db81c500604a231defaca9f14b` respectively.

Native source builds completed using the existing build environment and unchanged
`python -B -m build --no-isolation --wheel --sdist` commands. They are local validation
artifacts, not published packages; development versions remain 3.2.5.

| Native checkout artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| fcop-3.2.5-py3-none-any.whl | 730867 | b1ddb309828feef995a42bb71ef4ae48d0b71663c94483aa2219f9ab0ef8cd71 |
| fcop-3.2.5.tar.gz | 651800 | 05995816e102fd93ed39eed56c01eae1c03a1a5ca277fac7411e291884932714 |
| fcop_mcp-3.2.5-py3-none-any.whl | 117966 | e490041d80b8f82e07bd1fd8f5e2f6d0c96bfb92921387328353e7e5192e14a9 |
| fcop_mcp-3.2.5.tar.gz | 110043 | 8a7d9d2c6ba521d1af443a833e476a2ffd4dbe39f3b3cbd467f9b41049e10720 |

A new isolated environment `D:/fcop-wp4c6c-clean-install01` was created with
`include-system-site-packages=false`; installation uses the two newly built wheels
and the existing relay extra without changing dependency constraints. Installation
completed and `pip --python <new-env-python> check` reported no broken requirements.
The unchanged installed artifact probe passed raw source/wheel/sdist/install parity
19/19 and the real installed public export. `artifact_probe.py base` passed real
stdio 46/12/4, create/retry/spec/structured-error and versioned resource parity with
zero writes 5/5. `artifact_probe.py relay` passed initialization/tool listing and the
missing-dependency diagnostic. Imports were verified inside the new isolated environment.

The actual public fixed-ref read-only Shadow passed 14/14 and zero effects again.
Authorized ref and authorization hash are unchanged from the historical report below.
This invocation observed CodeFlowMu HEAD `cb590ce35686cb1980e3c89a7d68bd0cfbeb825a`,
tracked-status SHA-256 `acbc2da1fb5d105b4d8b97a2bdcbac1b67624af7801f59242b3cc28253082ec9`;
its own before/after caller, snapshot, authorization, product HEAD and tracked status
matched. No live downstream execution or write occurred.

Policy HEAD CI completed successfully in both workflows: FCoP
[34313100034](https://github.com/joinwell52-AI/FCoP/actions/runs/34313100034)
and MCP [34313099999](https://github.com/joinwell52-AI/FCoP/actions/runs/34313099999).
All eight Windows matrix items and sixteen Ubuntu/macOS matrix items passed;
Coverage and both downstream package jobs actually ran and passed (27 applicable jobs).
The two pull-request-event-only charter jobs were skipped by their unchanged event
conditions on this push; they are disclosed as NOT_RUN_EVENT_INAPPLICABLE, not PASS.
This intermediate evidence demonstrates the four-line policy correction but does not
replace the mandatory repeat CI at final Manifest HEAD.

Final Manifest HEAD, pending full local run, and final CI conclusions must be recorded in the post-push receipt.
The policy commit's intermediate CI is not final delivery acceptance. Pending, skipped,
cancelled and untriggered jobs are not PASS. Gate remains unsigned and unrequested
until all applicable final-head checks complete.

## Preserved WP4C.6b result (historical)

Execution role: ME / solo. ADMIN owns authorization and Gate signature. This report records current stable candidate evidence; it does not self-sign acceptance.

## Status at content preparation

```yaml
WP4C_6B_STATUS: LOCAL_VERIFIED_AWAITING_REMOTE_CI
AUTHORIZED_SCOPE: WP4C_6B_EXCEPTION_CATCH_CORRECTION_AND_WP4C_6_RESUME_ONLY
ORIGINAL_TASKBOOK_COMMIT: dc4bd62d47c3c422c8e758b588369dd3ed089acd
ORIGINAL_TASKBOOK_SHA256: 457ec98aecaad481b68879069771c954d8e4069352ccdbe19838e92ddc61e06e
WP4C_6A_RULING: cd0fe4df900c3ff0b34beca957097f87a8d4b150
ERRATUM_COMMIT: 8162d6ae9a91b8b23a6698bfd292a2cb2a75194c
ERRATUM_SHA256: 4fbf32c198f4ee624d55bd149c4152e3382894623c638b1001f943849900e306
ERRATUM_BYTES: 5334
INPUT_HEAD: 8a4e2b175938af8b28e2983161862b49e8650256
WP4C_5_GATE_COMMIT: b5c1e11a4fc05b4c659f69ddad09d3290840f86a
FROZEN_DISTRIBUTION_CONTRACT: f6831de12991010f22672fb6e776ce85ef1507ff
FROZEN_DISTRIBUTION_TEST_TREE: 4f99c7261b63b6db81c500604a231defaca9f14b
FROZEN_CORE_TEST_TREE: 24ab264c6bca9a3183ee270becb552f22a4c4f9e
BLOCKED_PR_29_HEAD: 91e64fa0a0ee377335af3226263a1811e1a56c1d
BLOCKED_PR_30_HEAD: 576bad0025038ee085fc53da46c125143d126bd3
CANDIDATE_INPUT_HASHES: 11/11
HISTORICAL_ASSERTION_ALIGNMENT: 2/2
ALIGNMENT_COMMIT: 22e2f558d3980d5647a1669e9455e4dacb60bc85
DIST_27: 2/2
DIST_28: 18/18
RULE_DISTRIBUTION_FULL: 176/176
V4_CORE_CONFORMANCE: 119/119
TEST_FCOP: 1459/1459
MCP_REGRESSION: 158/158
COMBINED_REGRESSION: 1736/1736
CLEAN_INSTALL_PARITY: PASS_19_OF_19
INSTALLED_REAL_STDIO: PASS_46_12_4
CONTEXT_MATRIX: 18/18
CONTEXT_ESTIMATOR: exact-utf8-byte-count/v1
RUNTIME_CONSUMPTION_VERIFIED: null
GITHUB_CI_AT_FINAL_HEAD: NOT_YET_RUN
ARTIFACT_MEMBERS: 19/19
ARTIFACT_RAW_BYTE_PARITY: PASS
REPEAT_BUILD_DETERMINISM: PASS_SAME_PLATFORM
PUBLIC_SURFACE: 4/4_UNCHANGED
NEW_PUBLIC_APIS: 0
NEW_RUNTIME_DEPENDENCIES: 0
NEW_BACKGROUND_COMPONENTS: 0
NEW_AUTHORITATIVE_STORES: 0
NEW_STATE_MACHINES: 0
WINDOWS_NATIVE_MATRIX: PENDING_FINAL_HEAD
LINUX_NATIVE_MATRIX: PENDING_FINAL_HEAD
MACOS_NATIVE_MATRIX: PENDING_FINAL_HEAD
MCP_SURFACE: 46_tools_12_static_4_templates
CODEFLOWMU_FILES_MODIFIED: 0
MAIN_MODIFIED: false
RELEASE_CREATED: false
WP4C_RULE_DISTRIBUTION_ACCEPTED: false
REQUESTED_GATE: NONE
```

Worktree: D:/FCoP-wp4c6a-distribution-resume. Branch: feat/fcop-4.0-wp4c.6a-distribution-resume. Draft PR #30, base taskbook/fcop-4.0-wp4c.6-closeout. PR #29 is not reused or modified. No main merge, retarget, tag, Release or PyPI action is authorized.

## Fixed input and preserved history

The fixed GitHub erratum was decoded from its raw Blob, verified at 5334 bytes with the stated SHA-256, strict UTF-8/no-BOM/LF, and parent 576bad0025038ee085fc53da46c125143d126bd3. The user's latest clarification explicitly identifies 8162d6ae... as the updated remote PR HEAD; section 2's previous blocked HEAD remains the historical checkpoint.

The original eleven candidates and the recovered eleven copies matched the PR #29 inventory before resumption. The failed local alignment matched b0a77d2b84d51e435a5dd7b171554e83005023ed1d8e7568fbd5d863a832ad3e. No unlisted candidate was accepted. The erratum was fast-forwarded without cleaning or overwriting candidate files. The original D:/FCoP workspace and D:/FCoP-wp4c6-distribution-closeout were preserved.

The historical failures remain true and visible:

- PR #29: original FCoP run stopped at 1240 passed / 1 failed on the pre-WP4C.6 missing-capability sentinel.
- WP4C.6a / PR #30: exact ADMIN replacement produced 0 passed / 2 failed, 38 deselected. Structured toolkit:RULE_SELECTION_INVALID and zero effects were correct, but sibling _DistributionError was not caught by V4ProtocolError. Historical JUnit SHA-256 12e38db40788e457a6183666b011d9f583836eee5925fba73691aa67228cf436.
- WP4C.6b: only the local catch changed to public FcopError; both nodes freshly passed. No exception import/hierarchy, private public API or alternate accepted code was introduced.

Commit 22e2f558... has three line replacements relative to its Git parent because the two authorized WP4C.6a replacements were previously local-only. Relative to the verified failed local file, only the single 6b catch changed. It contains one test file and no implementation. Successful test-file SHA-256: 1905cc752c455b41d77defb41a4dd7a21d1fba3a1d51850dd74d7390e0b97bc2.

| Historical ordinary ID | Authorized active ordinary ID |
| --- | --- |
| test_future_positive_capability_is_absent[measure_context] | test_wp4c6_positive_capability_requires_complete_request[measure_context] |
| test_future_positive_capability_is_absent[build_artifacts] | test_wp4c6_positive_capability_requires_complete_request[build_artifacts] |

All frozen IDs/assertions/fixtures/drivers remain unchanged. Imports, call/snapshot and both parameter values in the aligned ordinary test are unchanged.

## Eleven approved candidate inputs

The following source/recovered hashes were rechecked after testing had started, without modifying any implementation bytes:

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| .github/workflows/test-fcop.yml | 12763 | caa2d77983c52530049d9e171b19258df0724aaa484374e289d77e12cfeeb1f1 |
| .github/workflows/test-fcop-mcp.yml | 9106 | f709b11b870012aac468fde079b3a6b0f2a3a599fbc5dbd3cc59c31d14fbb067 |
| CHANGELOG.md | 132298 | 886207904c7d42caaf822f509ca2c65c911efa652ea81f22dcacf743c9f44318 |
| src/fcop/v4/rule_distribution/__init__.py | 5595 | 9566f6deac89bafed304957150d4585e8ed8ac9838e2fae28b0cebb19d6c398d |
| src/fcop/v4/rule_distribution/_artifacts.py | 7902 | 405aaac145415302326bb68762a7861a162c81211cf9e9f4622dbf6054b52e0e |
| src/fcop/v4/rule_distribution/_measurement.py | 3672 | 5da4ba521c8ea07b0a584dcf1323c3ecc3ec76d3046711025bc7ecd03700391a |
| src/fcop/v4/rule_distribution/_profiles.py | 3232 | c999662959d5dd94518711db3ec007333943a5101608973cb096d36af3b37784 |
| src/fcop/v4/rule_distribution/_projection.py | 6467 | b24ebd30e563d24f3947ca8b9f0b46becc5eea9d53ce1bc0ec085aeb45b33ffd |
| src/fcop/v4/rule_distribution/_selection.py | 6736 | 16b6ce8025f265c76a86b62c15451a83a656608c3c7a00aaab2b3a20bcc1f056 |
| tests/test_fcop/rule_distribution_artifact_probe.py | 3092 | 3bb3ce4f5bef9d1881a198efa118cbf3f61a07de5a0113e51a0099a1a611fbfc |
| tests/test_fcop/test_v4_rule_distribution_closeout.py | 12883 | e2bbff2de538b06faa8c41b333ec9e6afd86c44dbd18bf67b6fdd661cf06fc9d |

Content delivery adds these eleven candidates and the four existing final-report paths. No further production correction was made under the erratum.

## Fresh validation commands and machine evidence

Working directory: the resumed worktree. Interpreter: Windows Python 3.12.9. PYTHONDONTWRITEBYTECODE=1; PYTHONPATH includes this checkout's src, mcp/src and repository root. Tests use -B, -q -x -p no:cacheprovider, separate fresh --basetemp directories under D:/fcop-wp4c6b-*, and --junitxml paths below. Test suite order is alignment, targets, distribution, Core, FCoP, isolated MCP, combined.

| Suite | Pytest selection |
| --- | --- |
| Alignment | tests/test_fcop/test_v4_rule_distribution.py -k test_wp4c6_positive_capability_requires_complete_request |
| Targets | tests/conformance/rule_distribution_v4/test_dist_25_30_failures_artifacts_context_gates.py -k "test_dist_27 or test_dist_28" |
| Distribution | tests/conformance/rule_distribution_v4 |
| Core | tests/conformance/v4 |
| FCoP | tests/test_fcop |
| MCP | tests/test_fcop_mcp |
| Combined | tests/test_fcop tests/conformance/v4 tests/test_fcop_mcp |

JUnit files are retained outside the repository at C:/Users/Administrator/AppData/Local/Temp/. Each listed suite has zero failures, errors and skips; seconds below are the JUnit suite time (terminal summary timing can differ slightly).

| JUnit file (under the Temp directory above) | Passed | Seconds | Raw SHA-256 |
| --- | ---: | ---: | --- |
| fcop-wp4c6b-alignment-01.xml | 2 | 4.955 | e89a7963e20226941b96d746c68eb9b3ed373bad9b6ca08801e327ddb64acd33 |
| fcop-wp4c6b-combined-01.xml | 1736 | 3174.433 | ca3e6458932974121ff059226e6aa715e2878c67ce5104dc0eb09cf3ed952862 |
| fcop-wp4c6b-core-01.xml | 119 | 85.213 | 02811b8737a326a78df34ee803f71ce0b43a89796b9ecb5336b52f3e16fa349a |
| fcop-wp4c6b-distribution-01.xml | 176 | 960.610 | 3e5434fe42f79c365a56b797933b53f666774662b5176c72c683beff706ba904 |
| fcop-wp4c6b-fcop-01.xml | 1459 | 2104.988 | fa02fbfc1bbccef7c3d5e1a4bee0a5e913b9c424742fa7437a1ba4c8e5f32b76 |
| fcop-wp4c6b-mcp-01.xml | 158 | 260.161 | 70ace931ce85f02d89e1db64d428caa9cb6d11f242cbd3538bcb47e23eff68cd |
| fcop-wp4c6b-surface-01.xml | 4 | 0.273 | 2b2d48dc1912a5869980b024f270bf37f61f91eb8ce871c16620a354083e5294 |
| fcop-wp4c6b-target-01.xml | 20 | 135.286 | f4a8796f1e587e71a4042d7704f734eff1cb84352b9a3697873627d3e86310d7 |

The root FCoP run includes 62 new ordinary closeout nodes and the unchanged public-surface snapshot. Existing DeprecationWarnings concerning Traversable/jsonschema.RefResolver are disclosed; they are not hidden failures.

Supplementary checks performed while the serial combined suite ran: canonical CI Ruff commands passed; mypy src/fcop passed (55 files), MCP source passed (18 files) and MCP tests passed (11 files), using MYPYPATH for this checkout rather than an installed older package. The extra diagnostic invocation forcing MCP's Ruff config from the root reported four existing import-order differences; it was not the workflow command. The actual workflow command without that override passed, and no import was changed. Formal post-combined reruns of both Ruff commands and all three mypy commands passed with the same file counts. Explicit public-surface rerun passed 4/4 without snapshot-update. Normal FCoP/MCP builds passed again with identical artifact hashes. Isolated installed parity and real stdio/Relay probes passed, followed by a fresh read-only Shadow. These are completed results, not planned checks.

## Artifact and context evidence

See ARTIFACT-PARITY for the exact nineteen-member inventory, normal wheel/sdist hashes, real public export repeat hashes and clean-install status. See CONTEXT-MEASUREMENT for all eighteen actual canonical-package byte counts and zero-effect checks. These are fresh 6b runs on unchanged candidate bytes, not pre-blocker evidence.

Installed probe commands (both exit zero) used D:/fcop-wp4c6b-clean-install01/Scripts/python.exe -I -B followed by tests/test_fcop/rule_distribution_artifact_probe.py <checkout> D:/fcop-wp4c6b-artifacts-fcop --installed and tests/test_fcop_mcp/artifact_probe.py base / relay. Exact terminal facts: REAL_STDIO: 46/12/4; create/retry/spec/structured-error PASS; WP4C5_PACKAGED_RESOURCE_PROJECT_STDIO_PARITY_ZERO_WRITE: 5/5; INSTALLED_RELAY_INITIALIZE_AND_TOOL_LIST: PASS; RELAY_MISSING_DEPENDENCY_DIAGNOSTIC: PASS. pip check: No broken requirements found. The initial prolonged pip installation was deliberately interrupted and completely force-reinstalled using --no-compile; only the task-created environment was affected. No dependency constraint changed.

## Fixed-ref downstream Shadow

Read-only authorization file C:/Users/Administrator/AppData/Local/Temp/fcop-wp4c5b-shadow-authorization.json retained SHA-256 206129e8a68db7d5da1ef345d04c5e28348c1f392eef11aaa44e96f1fe6cdafa. All fourteen allowed snapshot files at D:/fcop-wp4c5b-shadow-b961b16d-lf matched the fixed b961b16dd0c8863ead6995d963fe0ca576a8abaa raw Git Blobs. The actual public shadow action returned read-only, deployed=false, fourteen files, both fcop==3.2.5 and fcop-mcp==3.2.5 pins, and runtime_consumption_verified=null.

Before/after caller tree, snapshot bytes, authorization bytes, actual downstream HEAD and tracked status matched. Observed current downstream HEAD was b2c402e2c647e158c852c42f1e52a6ad8b1e38d4, not falsely asserted to equal the historical snapshot ref. Tracked-status SHA-256 was 90fc7d541b5b51c093f99e70a7c2c017705d4d5cb5ed2f6fd8c506b161294ead. No CodeFlowMu checkout/install/run/upgrade or write occurred. Its excluded v1.0-rc.1 document remains audit input only, not a canonical source or archive member.

The required post-combined Shadow repeated the fourteen fixed-Blob and zero-effect checks successfully. It observed actual downstream HEAD 9a14c6d1be0eb50cd4398fbee325e62ec7144b53 and tracked-status SHA-256 4f7ae536aa81f4060b3332377bd82ae9a6b1ae5fa8252b875dfc1d88073d244e. The independently active downstream changed between the two observation times, but each probe's own before/after identities matched. The fixed authorized snapshot did not change, and this FCoP task made zero CodeFlowMu writes.

## Native CI risk and non-claims

Read-only inspection of erratum-only HEAD 8162d6ae... found a pre-existing Windows failure pattern: test-fcop run 34302231513 and test-fcop-mcp run 34302231581 had four Windows matrix failures each; eight Ubuntu/macOS matrix jobs each passed. FCoP Windows 3.12 job 102311391448 reported 49 failed / 1348 passed, with Invalid raw Encoding and Frozen specification source drift. Package jobs were skipped. This HEAD contains no candidate implementation; its results cannot establish final implementation PASS or FAIL.

The current .gitattributes pins LF only for the two v4 Schema paths. Rule-data/Manifest and frozen spec raw bytes are not covered. This is a documented checkout-risk hypothesis supported by the old logs, not permission to change attributes, rules, frozen files, loaders or CI thresholds. No such repair was made. Final implementation HEAD CI must supply the actual disposition; pending, skipped applicable jobs, cancelled and old-head success are never reported PASS.

## Delivery control

Local verification is complete; remote final-HEAD CI has not yet run when this content report is committed. REQUESTED_GATE remains NONE until the post-push receipt establishes all applicable checks. This timing is intentional: a report cannot contain the future commit's CI conclusion without a circular/repeated delivery.

Before delivery, remote main remained 68dbeb15f4e7f84e1d03f907be9fa66c2265843e, original D:/FCoP HEAD remained da79dfefd99f597c9e422ce9edec22157f915a21, and PR #30 remained Open/Draft at the erratum. Content commit contains eleven approved candidates plus four reports; the following Manifest-only commit updates reviews/fcop-4.0/wp4c.6a/MANIFEST.md. Exact commit hashes, seventeen agent-delivered file hashes (including alignment and Manifest), remote parent/readback, fresh LF checkout and final CI conclusions belong to the Manifest and post-push receipt. The ADMIN erratum taskbook is a separate upstream file, not an agent implementation edit.

No self-signature, main merge, release or WP4D advance is permitted. If a final check needs any additional unauthorized correction, preserve the evidence and stop with REQUESTED_GATE: NONE.
