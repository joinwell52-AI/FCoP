# WP4C.5B Execution Result

## Current verification state

Implementation and local verification are complete. Final stable-byte serial
regression passed 1674/1674: FCoP 1397, v4 Core 119, MCP 158. The full distribution
suite has 156 passes and exactly twenty unchanged WP4C.6 future-owner reds;
all thirteen WP4C.5 targets pass. All twelve candidate code/test/CHANGELOG
byte streams still equal the preserved pre-run archive. No acceptance Gate is
signed by this report. This document records the pre-Content-commit checkpoint;
the subsequent Manifest and final PR receipt resolve commit identities and
remote readback. The first failed run is retained below, not relabeled green.

```yaml
WP4C_5B_STATUS: LOCAL_VERIFIED_DELIVERY_PENDING
REPORT_CHECKPOINT: PRE_CONTENT_COMMIT
AUTHORIZED_SCOPE: WP4C_5B_ONLY
RESUMED_SCOPE: FULL_WP4C_5
TASKBOOK_COMMIT: a6f3ce278977b7121700de76ea6d832fe518533f
TASKBOOK_SHA256: f0501c7837e8e50668f8888d24e11b0929fafcf77ec2710d4c597deeb8fa5e2e
TASKBOOK_BYTES: 12749
BLOCKED_DELIVERY_HEAD: c3ef6ccba14a93ac73935ae729b5f9b681693138
INPUT_HEAD: d29e4d41ad4e1fc74e6d3513faa6b95d97ba0dfb
WP4C_4_GATE_COMMIT: a9c810296aadf857438a1711b6a56fa63deaf4e9
FROZEN_DISTRIBUTION_CONTRACT: f6831de12991010f22672fb6e776ce85ef1507ff
PRE_CORRECTION_CONFORMANCE_TREE: 1134d730e4c5ab23aa7b3ec91138da6981c2f009
POST_CORRECTION_CONFORMANCE_TREE: 4f99c7261b63b6db81c500604a231defaca9f14b
FIXTURE_ALIGNMENT_COMMIT: 76ebfc6fedf9b55b436e866b7c80f532423cfd3c
FIXTURE_CORRECTION_FILES: 1/1
CONFORMANCE_FILES_MODIFIED_THIS_RUN: 1
FROZEN_TEST_IDS: 60/60
WP4C_5_TARGET_NODES: 13/13
DIST_23: 3/3
DIST_24: 8/8
DIST_26: 1/1
DIST_29: 1/1
TEST_FCOP: 1397/1397
V4_CORE_CONFORMANCE: 119/119
MCP_REGRESSION: 158/158
FINAL_COMBINED_REGRESSION: 1674/1674
RULE_DISTRIBUTION_FULL: 156_passed_20_expected_WP4C_6_red
UNEXPECTED_FAILURES_FINAL: 0
V3_PROTOCOL_PROJECT_SHAPE: LEGACY_MARKDOWN_STRING
V3_PROTOCOL_MCP_BYTES: PRESERVED
V3_PROTOCOL_MIME: text/markdown
V4_PROTOCOL_PROJECT_SHAPE: IDENTITY_OBJECT
V4_PROTOCOL_MCP_SHAPE: DETERMINISTIC_MARKDOWN
RESOURCE_READ_ZERO_WRITE: PASS
DIRECT_RELAY_PARITY: PASS
LAYER_SEPARATION: PASS
UNAUTHORIZED_SHADOW_ZERO_ACCESS: PASS
AUTHORIZED_SHADOW_ZERO_WRITE: PASS
MCP_ADAPTER_ALGORITHM_COPIES: 0
MCP_TOOLS: 46/46
MCP_STATIC_RESOURCES: 12/12
MCP_RESOURCE_TEMPLATES: 4/4
CODEFLOWMU_FIXED_BLOB_SHADOW: 14/14
CODEFLOWMU_FILES_MODIFIED: 0
RUNTIME_CONSUMPTION_CLAIM: UNKNOWN
NEW_RUNTIME_DEPENDENCIES: 0
NEW_BACKGROUND_COMPONENTS: 0
NEW_AUTHORITATIVE_STORES: 0
NEW_PUBLIC_FACADES: 0
CONTENT_COMMIT: NOT_COMMITTED
MANIFEST_COMMIT: NOT_COMMITTED
REMOTE_PUSHED: false
WP4C_5_COMPATIBILITY_ACCEPTED: false
WP4C_6_STARTED: false
MAIN_MODIFIED: false
RELEASE_CREATED: false
GATE_TO_REQUEST_AFTER_REMOTE_VERIFICATION: WP4C_5_COMPATIBILITY_ACCEPTED
```

## Completed checks and reproducible commands

All pytest runs use Python 3.12.9 on Windows, local source paths, no bytecode
or pytest cache writes, and unique external basetemp paths. Root pytest has
pythonpath=src; a prior-baseline comparison must override it and verify the
actually imported module, not merely set an environment path.

| Check | Measured result |
|---|---|
| Fixture-only baseline: 13 targets plus five MCP checks | 12 failed / 6 passed, 41.51 s |
| First implemented 13 targets plus four public surface checks | 17 passed, 37.71 s |
| Project/resource/Shadow suite plus initial MCP exact representation suite | 64 passed, 425.92 s; 49 Project tests plus 15 MCP tests |
| Final MCP whole suite including nine extra parameter-injection tests | 158 passed, 515.67 s; independent new MCP tests 24/24 |
| Rule Distribution full suite | 156 passed / 20 expected WP4C.6 failures / 0 skips, 1936.40 s; current targets 13/13 |
| Initial combined FCoP/Core/MCP run | 1660 passed / 2 failed, 2757.21 s; not final stable-byte evidence |
| Quiet unchanged lifecycle timing retest | 1 passed, 1.94 s total test run; original <2 s assertion intact |
| Final stable-byte serial combined run | 1674 passed / 0 failed / 0 skipped, 1507.43 s; FCoP 1397, Core 119, MCP 158 |
| Ruff: python -m ruff check src tests mcp/src | PASS |
| mypy src/fcop | PASS, 53 files |
| mypy --config-file mcp/pyproject.toml mcp/src/fcop_mcp tests/test_fcop_mcp | PASS, 29 files; MYPYPATH explicitly bound to this source tree |
| Fixed CodeFlowMu snapshot against raw Git blobs | 14/14, zero before/after effects |
| Final wheel/sdist canonical package raw bytes against source | 19/19 in both archives |
| Isolated installed wheels, real stdio resource and lifecycle probe | PASS, 46/12/4; five Project/resource parity checks; zero resource-read writes |
| Linux/macOS native execution | NOT_NATIVE_VERIFIED |

Full commands:

```text
python -X utf8 -m pytest tests/test_fcop tests/conformance/v4 tests/test_fcop_mcp -q --tb=short -p no:cacheprovider --basetemp=D:/fcop-wp4c5b-regression-01 --junitxml=C:/Users/Administrator/AppData/Local/Temp/fcop-wp4c5b-regression-01.xml
python -X utf8 -m pytest tests/test_fcop tests/conformance/v4 tests/test_fcop_mcp -q --tb=short -p no:cacheprovider --basetemp=D:/fcop-wp4c5b-regression-final04 --junitxml=C:/Users/Administrator/AppData/Local/Temp/fcop-wp4c5b-regression-final04.xml
python -X utf8 -m pytest tests/conformance/rule_distribution_v4 -q --tb=short -p no:cacheprovider --basetemp=D:/fcop-wp4c5b-distribution-01 --junitxml=C:/Users/Administrator/AppData/Local/Temp/fcop-wp4c5b-distribution-01.xml
python -X utf8 -m pytest tests/test_fcop/test_v4_rule_distribution_reads.py tests/test_fcop_mcp/test_wp4c5_resources.py -q --tb=short -p no:cacheprovider --basetemp=D:/fcop-wp4c5b-new-final01 --junitxml=C:/Users/Administrator/AppData/Local/Temp/fcop-wp4c5b-new-final01.xml
python -X utf8 -m pytest tests/test_fcop_mcp -q --tb=short -p no:cacheprovider --basetemp=D:/fcop-wp4c5b-mcp-full-final02 --junitxml=C:/Users/Administrator/AppData/Local/Temp/fcop-wp4c5b-mcp-full-final02.xml
D:/fcop-wp4c5b-wheel-venv01/Scripts/python.exe -I -B D:/FCoP-wp4c5b-protocol-resume/tests/test_fcop_mcp/artifact_probe.py base
```

## Verification failures retained, not erased

1. Fixture correction alone left all twelve implementation reds intact.
2. Newly written tests initially used the wrong v4 initializer and confused
   eleven artifact fields with four Manifest top-level fields. Those local
   test-writing errors were corrected before the exact behavior tests passed;
   no frozen assertion was changed beyond the single authorized condition.
3. FastMCP defaulted a template read to text/plain despite Markdown registration;
   an explicit framework ResourceContent fixes the MIME. A later probe found
   silent query/RPC-extra-field dropping. Small parameter guards now reject
   those requests before the framework discards fields; actual RPC tests pass.
4. An initial MCP mypy invocation resolved the installed legacy library. Explicit
   MYPYPATH fixes source selection; no type-ignore or threshold reduction was
   used. Initial no-isolation build failed because hatchling was absent;
   tooling was installed only in an isolated verification environment.
5. The first fixed-consumer archive used machine autocrlf and failed raw-Blob
   parity. A distinct LF archive passed 14/14. Product bytes were not normalized.
6. Initial full regression completed with 1660 passed and two failures.
   Its groups were FCoP 1393 passed / 1 failed, Core 119 passed, and MCP
   148 passed / 1 failed. Focused reproduction identified
   test_distinct_standalone_tasks_do_not_share_family_lock at
   tests/test_fcop/test_v4_lifecycle.py:399: elapsed 3.578 s versus <2 s.
   Verified actual WP4C.5a source reproduced 3.656 s versus <2 s. The first
   comparison attempt did not override root pytest pythonpath and is NOT
   counted as prior-baseline evidence. No timer, lifecycle implementation,
   assertion, skip or retry behavior has been changed to conceal this result.
   The initial full run's actual elapsed assertion was 2.015 s. With the other
   verification processes finished, the same unchanged test passed in a fresh
   isolated run (1.94 s total). This supports contention sensitivity; it does
   not prove an unconditional performance bound or erase the failed run.
7. The first combined process imported the MCP functions before the final
   parameter guards were added. Its later inspect.getsource call used old
   code-object line numbers against updated source, returning an unrelated
   module segment containing the pre-existing hashlib import. That failed
   source-owner check is retained. The final independent MCP run passes
   158/158, including that unchanged check. A subsequent frozen-byte serial
   combined run passes all 1674 nodes, including both initially failed nodes.
   Edits during a running verification process are not treated as reliable
   final-tree evidence. No assertion, threshold, skip or xfail was changed.

Evidence files are outside the repository:

| XML basename (under the local Temp directory) | Bytes | SHA-256 |
|---|---:|---|
| fcop-wp4c5b-regression-01.xml | 222920 | 9163cdfd9cbc52b6677d3377d50287aa88a6a901e2162e938576f7dad3801822 |
| fcop-wp4c5b-quiet-timing-final03.xml | 385 | e2a91e4ce5fd208e9ea0dcf5741967f6ec90ff1984c541a8e05f6784fd276781 |
| fcop-wp4c5b-regression-final04.xml | 223278 | 310be83058c98f8885d59df2797c968b4aa8b36c9d84cd8a979ff03de15f995a |

All 60 unique C0-C8/AT/MCP/RELEASE identifiers in the unchanged WP1 matrix
remain present in the frozen Core test source. The Core test Git tree is
24ab264c6bca9a3183ee270becb552f22a4c4f9e; its worktree diff is empty.

## Exact future-owner red inventory

The completed distribution XML is 247951 bytes, SHA-256
0f607e1e907747020477d8a86d7ffc1ac9581b8ca4559ca211f27dd830ab0917.
Its failed-node set was compared for exact equality with the following twenty
nodes, all explicitly owned by WP4C.6 in the unchanged frozen test docstrings.
Every failure is the existing unavailable operation boundary, not an assertion
removed or converted to skip/xfail. All thirteen current-stage targets pass.

| Frozen node | Owner / intentionally unavailable action |
|---|---|
| test_dist_27[wheel] | WP4C.6 / build_artifacts |
| test_dist_27[sdist] | WP4C.6 / build_artifacts |
| test_dist_28[languages0-codex-sequential] | WP4C.6 / measure_context |
| test_dist_28[languages0-codex-parallel] | WP4C.6 / measure_context |
| test_dist_28[languages0-cursor-sequential] | WP4C.6 / measure_context |
| test_dist_28[languages0-cursor-parallel] | WP4C.6 / measure_context |
| test_dist_28[languages0-claude-code-sequential] | WP4C.6 / measure_context |
| test_dist_28[languages0-claude-code-parallel] | WP4C.6 / measure_context |
| test_dist_28[languages1-codex-sequential] | WP4C.6 / measure_context |
| test_dist_28[languages1-codex-parallel] | WP4C.6 / measure_context |
| test_dist_28[languages1-cursor-sequential] | WP4C.6 / measure_context |
| test_dist_28[languages1-cursor-parallel] | WP4C.6 / measure_context |
| test_dist_28[languages1-claude-code-sequential] | WP4C.6 / measure_context |
| test_dist_28[languages1-claude-code-parallel] | WP4C.6 / measure_context |
| test_dist_28[languages2-codex-sequential] | WP4C.6 / measure_context |
| test_dist_28[languages2-codex-parallel] | WP4C.6 / measure_context |
| test_dist_28[languages2-cursor-sequential] | WP4C.6 / measure_context |
| test_dist_28[languages2-cursor-parallel] | WP4C.6 / measure_context |
| test_dist_28[languages2-claude-code-sequential] | WP4C.6 / measure_context |
| test_dist_28[languages2-claude-code-parallel] | WP4C.6 / measure_context |

## Local verification artifacts, not releases

Both packages retain version 3.2.5. These are private test artifacts under
D:/fcop-wp4c5b-artifacts-final02, not uploads or published FCoP 4.0 products.
The installed-wheel environment imports both packages from its own prefix and
uses shared existing third-party dependencies; this is not a clean-room
dependency-resolution or cross-platform release qualification.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| fcop/fcop-3.2.5-py3-none-any.whl | 720900 | dadda8c231e3ad6a0fe9e228a722631dfad1e183e694ad7e9b252b73a95c3556 |
| fcop/fcop-3.2.5.tar.gz | 643622 | 54183971d12adac0112b52d545460f17bd76fe6a5f94e63e77259074181d1112 |
| mcp/fcop_mcp-3.2.5-py3-none-any.whl | 117449 | 5e3ff514c1fca324bbd27a6597c44bc0db4189ea58705b866718f1102a0ba132 |
| mcp/fcop_mcp-3.2.5.tar.gz | 108959 | 46b245d0d9ad686fe6daf25a97e28fef223d93febf0573d5412be07ddafd2756 |

## Scope and delivery boundary

The twelve candidate implementation/test/CHANGELOG files were frozen before
the final serial run and independently preserved without deleting originals:
D:/fcop-wp4c5b-candidate-preserved-01.tar, SHA-256
5ac2d342ab7cb6b60918d1f58640cda364f61ca8e4257f9d7e549af6d90ae7c7.
All twelve archived byte streams match the following working-tree identities.
This is a local preservation artifact, not a release or a second implementation.

| Candidate path | Bytes | SHA-256 |
|---|---:|---|
| CHANGELOG.md | 131915 | df50cc2dba48d81ddba6e6ad834b70920ec6111bdd7fb379f6bacdc45e355d65 |
| mcp/src/fcop_mcp/disposition.py | 2825 | e0c749c0e9009a68f231c59eb6b0369b3d6602597a8b4b781045c38cea29a1e1 |
| mcp/src/fcop_mcp/resources.py | 7434 | 2e830503f7eac73445be7a2015b5a82426e1dffdc5875952447e179df62d739a |
| src/fcop/project.py | 265728 | 6f602991b036289f3955a9eda1abf93fc95e5ab25349dd9f42795a367eade1c3 |
| src/fcop/v4/rule_distribution/__init__.py | 5331 | 4fa74f36fca5fa0786691fa3d98ba8433ee53f490eef9cacddc348d4ca9dc534 |
| src/fcop/v4/rule_distribution/_read.py | 10645 | 0e0ca53a5cc48feea4d4f72fb51cfd57792894e1159be87f543354895d044473 |
| src/fcop/v4/rule_distribution/_shadow.py | 5206 | 1f494f16bb2142d311ed383858d34493f08ae14c7f880e116fcc94ac10cfd773 |
| tests/test_fcop/test_v4_rule_distribution.py | 9592 | 4c9ef609091dcc26b86fadca9dc6a19ee9fa835ef8ca6c63f3477a6de5031752 |
| tests/test_fcop/test_v4_rule_distribution_reads.py | 14714 | f44dd65808cf2315943f15259a669f48f35621e85018c31628db929609529768 |
| tests/test_fcop_mcp/artifact_probe.py | 7060 | 8053447e28c87b4ede044a94c95e49c9e19501e572ef12dc585c7c6ad44fd4eb |
| tests/test_fcop_mcp/snapshots/tool_surface_v4.json | 27301 | ab133b6018634ff0893e5039c7a31ae69a8612239eb75e0d99dd7f756ae378c4 |
| tests/test_fcop_mcp/test_wp4c5_resources.py | 9214 | 955c7fe4f33412d1b2d7cbab15549d92c7523fed387a245e237e73c92f1a71f9 |

The current Conformance tree is exactly the authorized post-correction tree;
frozen Core tests, normative contracts, Schema, canonical rule bytes, Host
deployment implementation and the historical MCP snapshot have no drift.
No new public API, Runtime dependency, authoritative store, cache, background
component, network update, MCP tool, downstream modification or release exists.
New read-only helpers live behind the existing Project entry. WP4C.6 build and
context-measurement actions remain unavailable.

PR #26 remains at df395c7e221f850352d907933ccaab0937706c8f and PR #27 remains
at c3ef6ccba14a93ac73935ae729b5f9b681693138, both OPEN/DRAFT. They are immutable
blocker history. At this report checkpoint no candidate implementation has
yet been committed or pushed. The next steps are the authorized Content commit
(twelve candidate files and these five reports), Manifest-only commit, new
Draft PR, remote raw-byte readback, and fresh LF checkout. Manifest includes
the fixture plus all seventeen Content files; its own digest is verified and
reported externally to avoid a self-referential hash.

The fixed review base is taskbook/fcop-4.0-wp4c.5b-protocol-representation.
test-fcop.yml:17-24 and test-fcop-mcp.yml:26-33 trigger pushes only on main/feat/**
and pull requests only against main. The authorized review/taskbook branch pair
is excluded. Final remote run/check observations must say
NOT_TRIGGERED_BRANCH_FILTER if empty, never PASS. No workflow is altered,
release workflow dispatched, or PR retargeted to main to bypass this boundary.
The final PR receipt, not this pre-commit checkpoint, records the actual
remote HEAD, all nineteen delivery hashes, clean checkout and Gate request.
