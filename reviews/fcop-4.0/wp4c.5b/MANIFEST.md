# WP4C.5b review Manifest

## Fixed authority and commit chain

```yaml
AUTHORIZED_SCOPE: WP4C_5B_ONLY
RESUMED_SCOPE: FULL_WP4C_5
TASKBOOK_COMMIT: a6f3ce278977b7121700de76ea6d832fe518533f
TASKBOOK_SHA256: f0501c7837e8e50668f8888d24e11b0929fafcf77ec2710d4c597deeb8fa5e2e
TASKBOOK_BYTES: 12749
TASKBOOK_DIRECT_PARENT: c3ef6ccba14a93ac73935ae729b5f9b681693138
INPUT_HEAD: d29e4d41ad4e1fc74e6d3513faa6b95d97ba0dfb
WP4C_4_GATE_COMMIT: a9c810296aadf857438a1711b6a56fa63deaf4e9
FIXTURE_ALIGNMENT_COMMIT: 76ebfc6fedf9b55b436e866b7c80f532423cfd3c
CONTENT_COMMIT: 4ed9fd6c1d2cfc3d235147ad3e923ea44c997b22
MANIFEST_PARENT: 4ed9fd6c1d2cfc3d235147ad3e923ea44c997b22
MANIFEST_COMMIT: THIS_FILE_CARRIER_COMMIT
FINAL_HEAD: THIS_FILE_CARRIER_COMMIT
REVIEW_BRANCH: review/fcop-4.0-wp4c.5b-protocol-resume
PR_BASE: taskbook/fcop-4.0-wp4c.5b-protocol-representation
PRE_CORRECTION_CONFORMANCE_TREE: 1134d730e4c5ab23aa7b3ec91138da6981c2f009
POST_CORRECTION_CONFORMANCE_TREE: 4f99c7261b63b6db81c500604a231defaca9f14b
CORE_CONFORMANCE_TREE: 24ab264c6bca9a3183ee270becb552f22a4c4f9e
FIXTURE_FILES: 1
CONTENT_FILES: 17
MANIFEST_FILES: 1
TOTAL_DELIVERY_FILES: 19
HASH_TABLE_FILES_EXCLUDING_MANIFEST: 18
```

The carrier is the single Manifest-only child of CONTENT_COMMIT. Its exact SHA
and this file's own SHA-256 are recorded in the final PR receipt after push and
remote readback; embedding a file's own digest or commit would be circular.
The first commit changes only the authorized version condition. Content changes
only twelve scoped candidate files and five reports. This last commit adds only
this Manifest. PR #26 and PR #27 remain immutable blocker history.

## Raw Git Blob inventory

Each row was read from CONTENT_COMMIT and compared byte-for-byte with the
verified local working file. All nineteen delivery files, including this
Manifest, must independently pass remote Contents/Blob readback and fresh LF
checkout verification before the final Gate request.

| Path | Bytes | SHA-256 |
|---|---:|---|
| [CHANGELOG.md](https://github.com/joinwell52-AI/FCoP/blob/4ed9fd6c1d2cfc3d235147ad3e923ea44c997b22/CHANGELOG.md) | 131915 | df50cc2dba48d81ddba6e6ad834b70920ec6111bdd7fb379f6bacdc45e355d65 |
| [mcp/src/fcop_mcp/disposition.py](https://github.com/joinwell52-AI/FCoP/blob/4ed9fd6c1d2cfc3d235147ad3e923ea44c997b22/mcp/src/fcop_mcp/disposition.py) | 2825 | e0c749c0e9009a68f231c59eb6b0369b3d6602597a8b4b781045c38cea29a1e1 |
| [mcp/src/fcop_mcp/resources.py](https://github.com/joinwell52-AI/FCoP/blob/4ed9fd6c1d2cfc3d235147ad3e923ea44c997b22/mcp/src/fcop_mcp/resources.py) | 7434 | 2e830503f7eac73445be7a2015b5a82426e1dffdc5875952447e179df62d739a |
| [reports/FCOP-4.0-WP4C.5B-CODEFLOWMU-SHADOW.md](https://github.com/joinwell52-AI/FCoP/blob/4ed9fd6c1d2cfc3d235147ad3e923ea44c997b22/reports/FCOP-4.0-WP4C.5B-CODEFLOWMU-SHADOW.md) | 7867 | 87f7eee15a21f9351bb0cff54407b10f03ba0c096d16a9d0e4447d56b818ac7c |
| [reports/FCOP-4.0-WP4C.5B-IMPLEMENTABILITY-PROOF.md](https://github.com/joinwell52-AI/FCoP/blob/4ed9fd6c1d2cfc3d235147ad3e923ea44c997b22/reports/FCOP-4.0-WP4C.5B-IMPLEMENTABILITY-PROOF.md) | 10198 | fbe3dd2d5c7b8706c947cefb938ef160889d4d6c8d52fda495e969d10e9dba89 |
| [reports/FCOP-4.0-WP4C.5B-LEGACY-AND-LAYER-ISOLATION.md](https://github.com/joinwell52-AI/FCoP/blob/4ed9fd6c1d2cfc3d235147ad3e923ea44c997b22/reports/FCOP-4.0-WP4C.5B-LEGACY-AND-LAYER-ISOLATION.md) | 3631 | be8dd1c7a578b3d0bb3ccbcbbd578ce4eda39c6ff4e2dcf7bfc935fd91e6ffc9 |
| [reports/FCOP-4.0-WP4C.5B-RESULT.md](https://github.com/joinwell52-AI/FCoP/blob/4ed9fd6c1d2cfc3d235147ad3e923ea44c997b22/reports/FCOP-4.0-WP4C.5B-RESULT.md) | 16013 | eeea967a14b6115546c337c363180bd80be0dbb8c5db0904a6af6a4b07f55a05 |
| [reports/FCOP-4.0-WP4C.5B-VERSIONED-RESOURCE-MAPPING.md](https://github.com/joinwell52-AI/FCoP/blob/4ed9fd6c1d2cfc3d235147ad3e923ea44c997b22/reports/FCOP-4.0-WP4C.5B-VERSIONED-RESOURCE-MAPPING.md) | 5408 | d77c9bb276ce97481d71d52b2e2a33093abb0c211d8fc10a0120232498e769c4 |
| [src/fcop/project.py](https://github.com/joinwell52-AI/FCoP/blob/4ed9fd6c1d2cfc3d235147ad3e923ea44c997b22/src/fcop/project.py) | 265728 | 6f602991b036289f3955a9eda1abf93fc95e5ab25349dd9f42795a367eade1c3 |
| [src/fcop/v4/rule_distribution/__init__.py](https://github.com/joinwell52-AI/FCoP/blob/4ed9fd6c1d2cfc3d235147ad3e923ea44c997b22/src/fcop/v4/rule_distribution/__init__.py) | 5331 | 4fa74f36fca5fa0786691fa3d98ba8433ee53f490eef9cacddc348d4ca9dc534 |
| [src/fcop/v4/rule_distribution/_read.py](https://github.com/joinwell52-AI/FCoP/blob/4ed9fd6c1d2cfc3d235147ad3e923ea44c997b22/src/fcop/v4/rule_distribution/_read.py) | 10645 | 0e0ca53a5cc48feea4d4f72fb51cfd57792894e1159be87f543354895d044473 |
| [src/fcop/v4/rule_distribution/_shadow.py](https://github.com/joinwell52-AI/FCoP/blob/4ed9fd6c1d2cfc3d235147ad3e923ea44c997b22/src/fcop/v4/rule_distribution/_shadow.py) | 5206 | 1f494f16bb2142d311ed383858d34493f08ae14c7f880e116fcc94ac10cfd773 |
| [tests/conformance/rule_distribution_v4/test_dist_21_24_assembly_compat_mcp.py](https://github.com/joinwell52-AI/FCoP/blob/4ed9fd6c1d2cfc3d235147ad3e923ea44c997b22/tests/conformance/rule_distribution_v4/test_dist_21_24_assembly_compat_mcp.py) | 6196 | 72b4c5a621775487b10b60dc789c27a67ecfd5a81eda28cc3563cbe6c878b572 |
| [tests/test_fcop/test_v4_rule_distribution.py](https://github.com/joinwell52-AI/FCoP/blob/4ed9fd6c1d2cfc3d235147ad3e923ea44c997b22/tests/test_fcop/test_v4_rule_distribution.py) | 9592 | 4c9ef609091dcc26b86fadca9dc6a19ee9fa835ef8ca6c63f3477a6de5031752 |
| [tests/test_fcop/test_v4_rule_distribution_reads.py](https://github.com/joinwell52-AI/FCoP/blob/4ed9fd6c1d2cfc3d235147ad3e923ea44c997b22/tests/test_fcop/test_v4_rule_distribution_reads.py) | 14714 | f44dd65808cf2315943f15259a669f48f35621e85018c31628db929609529768 |
| [tests/test_fcop_mcp/artifact_probe.py](https://github.com/joinwell52-AI/FCoP/blob/4ed9fd6c1d2cfc3d235147ad3e923ea44c997b22/tests/test_fcop_mcp/artifact_probe.py) | 7060 | 8053447e28c87b4ede044a94c95e49c9e19501e572ef12dc585c7c6ad44fd4eb |
| [tests/test_fcop_mcp/snapshots/tool_surface_v4.json](https://github.com/joinwell52-AI/FCoP/blob/4ed9fd6c1d2cfc3d235147ad3e923ea44c997b22/tests/test_fcop_mcp/snapshots/tool_surface_v4.json) | 27301 | ab133b6018634ff0893e5039c7a31ae69a8612239eb75e0d99dd7f756ae378c4 |
| [tests/test_fcop_mcp/test_wp4c5_resources.py](https://github.com/joinwell52-AI/FCoP/blob/4ed9fd6c1d2cfc3d235147ad3e923ea44c997b22/tests/test_fcop_mcp/test_wp4c5_resources.py) | 9214 | 955c7fe4f33412d1b2d7cbab15549d92c7523fed387a245e237e73c92f1a71f9 |

## Local verification, completed before Content commit

```yaml
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
FROZEN_TEST_IDS: 60/60
MCP_SURFACE: 46_tools_12_static_4_templates
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
CODEFLOWMU_FIXED_BLOB_SHADOW: 14/14
RUNTIME_CONSUMPTION_CLAIM: UNKNOWN
RUFF: PASS
MYPY_FCOP: 53_files_PASS
MYPY_MCP: 29_files_PASS
PACKAGED_CANONICAL_BYTES: 19/19_wheel_and_sdist
INSTALLED_WHEEL_REAL_STDIO: PASS
NEW_RUNTIME_DEPENDENCIES: 0
NEW_BACKGROUND_COMPONENTS: 0
NEW_AUTHORITATIVE_STORES: 0
NEW_PUBLIC_FACADES: 0
CONFORMANCE_FILES_MODIFIED_THIS_RUN: 1
CODEFLOWMU_FILES_MODIFIED: 0
MAIN_MODIFIED: false
RELEASE_CREATED: false
WP4C_6_STARTED: false
WP4C_5_COMPATIBILITY_ACCEPTED: false
NEXT_GATE_AFTER_REMOTE_VERIFICATION: WP4C_5_COMPATIBILITY_ACCEPTED
```

Final combined XML: 223278 bytes, SHA-256
310be83058c98f8885d59df2797c968b4aa8b36c9d84cd8a979ff03de15f995a,
1674 passed, zero failed/skipped, 1507.43 seconds. Candidate code/test bytes
were stable for this final serial run. The earlier 1660-pass/two-failure run
is retained with its timing and source-line evidence in RESULT; no assertion,
timer, skip, xfail or frozen behavior was weakened to pass.

The twenty distribution reds are exactly DIST-27's two artifact cases and
DIST-28's eighteen context cases, explicitly owned by WP4C.6. RESULT lists
every node. They are real failed tests, not new skips or a completed WP4C.6.

## Remote verification contract

Re-fetch only the authorized review branch, verify the three-parent sequence,
and compare all nineteen raw remote byte streams with local committed Blobs.
Create a fresh detached checkout with per-command core.autocrlf=false; compare
tracked raw byte identities and confirm clean status. Record exact remote main
before/after (observed before push: 68dbeb15f4e7f84e1d03f907be9fa66c2265843e).

Observe actual Actions runs, check-runs and status contexts at the final carrier
HEAD. Existing workflows trigger push only for main/feat/** and PR only for
main; this authorized review/taskbook pair is excluded. An empty observation
must be NOT_TRIGGERED_BRANCH_FILTER, not PASS. No retargeting, dispatching
release workflows or changing workflow filters is authorized.

The final receipt in the new Draft PR records those completed observations,
exact Manifest HEAD/hash and the Gate request. This Manifest does not self-sign
a Gate. Stop after delivery; no WP4C.6, main merge, release or downstream writes.
