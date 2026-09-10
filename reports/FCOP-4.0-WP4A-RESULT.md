# WP4A.1 execution result — local complete, remote CI gate pending

## Decision boundary

All local implementation, SB binding, application and artifact checks passed. This content commit does **not** claim remote delivery or CI success before those events occur. The mandatory next steps are Manifest-only commit, review-branch push/refetch/hash verification, Draft PR, and observation of its exact Manifest HEAD CI. No Gate is requested by this pre-CI report. Final remote HEAD/PR/job results are independently observable from the Manifest and GitHub checks and will be returned in the execution receipt.

The fixed workflow lints frozen Conformance files with ten pre-existing Ruff findings. They are outside this task's writable set; neither those files nor workflows were changed. If those findings block remote CI, status remains BLOCKED and the taskbook explicitly forbids requesting the Gate.

## Final local verification

Executed on Windows local NTFS / Python 3.12 in `D:/FCoP-wp4a1-machine-contract`:

| Command / measurement | Result |
|---|---|
| `python -m pytest tests/test_fcop tests/conformance/v4 -q --tb=short` | 1309 passed, 3 deprecation warnings, 342.79 s |
| test_fcop partition | 1190/1190 = v3/non-v4 908 + prior v4 units 235 + new schema/application nodes 47 |
| Frozen Conformance partition | 119/119, no fixture/test edits |
| SB-01–10 | 10/10 requirements, represented within 47 new nodes |
| `python -m pytest tests/test_fcop_mcp -q --tb=short` with current src and mcp/src on PYTHONPATH | 80/80, 33.26 s |
| `python -m pytest tests/test_fcop/test_public_surface.py -q` | 4/4, snapshot unchanged |
| `python -m mypy src/fcop` | PASS, 40 source files |
| `python -m ruff check src/fcop tests/test_fcop examples/v4 spec/schemas/v4/generate.py` | PASS |
| `python -m ruff check src tests` (workflow-equivalent broader scope) | FAIL, 10 pre-existing frozen Conformance findings |
| `python spec/schemas/v4/generate.py --check` | 12 schema pairs verified |
| Strict UTF-8/no BOM/LF, staged diff check | PASS for delivery content |
| Final wheel and sdist inventory | 20 schemas each: old 8 + new 12 |
| Source/wheel/sdist v4 schema byte parity | 12/12 each |
| Clean wheel install, external sequential/family applications, subprocess restart | PASS, network-disabled execution |

The full run was repeated after final schema and canonical-request wiring. A later LF-only normalization did not change Python logic; artifacts were rebuilt afterward and their smoke checks repeated. PACKAGE-PROOF records the final normalized artifact hashes.

## First remote observation and in-scope test correction

The first two-commit delivery ended at `12dde48babec00d38085332baafc115057618cbb`, was read back from GitHub 47/47, and opened Draft PR #14. Its immutable CI run [34014163412](https://github.com/joinwell52-AI/FCoP/actions/runs/34014163412) confirmed the ten inherited lint findings and the Stability charter failure: the cumulative PR snapshot change lacks a matching Added/Changed/Deprecated heading in the workflow's extracted Unreleased section. No frozen file, CHANGELOG or workflow was changed to bypass those failures.

That run also found one **new test-harness defect**, not an inherited problem: SB-10 invoked `git show` on the fixed taskbook ancestor, which is absent in CI's shallow checkout. Coverage had 1189 passed / 1 failed and reached 80.64% (above 80%). SB-10 now compares sixteen explicitly captured fixed-baseline Git-blob SHA-256 values after historical CRLF normalization; it performs no history lookup, fetch, network call, or skip. The targeted corrected test passed 1/1 locally. This is the only test change after the full 1309-pass local run; final CI reruns the corrected test within the complete 1190-node library suite. Production bytes and final artifact hashes are unchanged.

The first delivery remains reachable through local backup branch `codex/wp4a1-first-delivery-preserved`. The corrected delivery is rebuilt as exactly Content + Manifest commits from the same authorized taskbook parent; the review branch is updated only with an exact old-HEAD force-with-lease. Its new fixed Manifest HEAD and all 47 remote file hashes must be verified again. No third commit is appended to evade the two-commit contract, and no user-owned worktree history is reset.

An initial MCP invocation loaded the globally installed `fcop_mcp` and returned 79 passed / 1 failed (`test_report_lifecycle`, missing parent display). `fcop_mcp.__file__` proved the wrong installed import. Re-running against this branch's unmodified `mcp/src` and `src` passed 80/80. No MCP correction was made or concealed.

## Inherited CI lint findings (not authorized to repair)

`tests/conformance/v4/driver.py`: I001, UP035, N818; `scenarios.py`: UP035; `test_c0_contract_authority.py`: I001; `test_c5_convergence.py`: I001; `test_c7_idempotency.py`: I001 and F401; `test_mcp_surface_contract.py`: I001; `test_meta_profile_boundary.py`: I001. All ten files/locations are untouched baseline content. The existing test-fcop workflow runs `ruff check src tests`; an actual remote result is still required, not inferred from this diagnostic.

## Scope and receipt at content creation

```yaml
WP4A_1_STATUS: BLOCKED
BLOCKER: MANIFEST_HEAD_GITHUB_CI_PENDING
LOCAL_IMPLEMENTATION_AND_VALIDATION: PASS
AUTHORIZED_SCOPE: WP4A_1_ONLY
RESUMED_SCOPE: FULL_WP4A
TASKBOOK_COMMIT: 6ddf6a35235c6aedff6807e5e7aba3f7d515e2ff
TASKBOOK_SHA256: 7fa10b9825a2b67c9c15032612d543045bef0b1d9ffc18e11dab96a16635e13b
PARENT_TASKBOOK_COMMIT: a789cf070cfc626d23034753b18e8679780b7d50
INPUT_HEAD: fea48393be8c83f4dbb6e085f54bb4ce391ee2ed
EFFECTIVE_CORE_HEAD: 1d94b881e38cc0b98ca41c47d25c605431d5f9a7
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
SCHEMA_BINDING_POLICY: PASS
OPEN_ROOT_EXTENSION_POINTS: 5/5
CLOSED_CORE_NESTED_OBJECTS: PASS
UNKNOWN_ROOT_FIELD_CORE_SEMANTICS: NONE
SCHEMA_BINDING_TESTS: 10/10
V4_SCHEMA_FILES: 12
V4_SCHEMA_STRUCTURAL_OBJECT_GROUP_MAPPING: 12/12
V4_SCHEMA_IDS_UNIQUE: PASS
OFFLINE_REF_RESOLUTION: PASS
SOURCE_PACKAGE_SCHEMA_PARITY: PASS
V4_CONFORMANCE: 119/119
WP3E_V4_UNIT_TESTS: 235/235
TEST_FCOP: 1190/1190
V3_NEW_FAILURES: 0
MCP_REGRESSION: 80/80
PUBLIC_SURFACE_DRIFT: 0
LOCAL_TEST_UNEXPECTED_FAILURES: 0
NEW_PUBLIC_APIS: 0
NEW_RUNTIME_DEPENDENCIES: 0
NEW_BACKGROUND_COMPONENTS: 0
NEW_AUTHORITATIVE_STORES: 0
NEW_STATE_MACHINES: 0
NEW_LOCK_SYSTEMS: 0
NEW_BASE_ERROR_CODES: 0
NEW_X_PREFIX_RULE: false
NEW_EXTENSIONS_CONTAINER: false
PROFILE_REGISTRY_PROTOCOL_ADDED: false
LEGACY_SCHEMA_FILES_MODIFIED: 0
FROZEN_SPEC_FILES_MODIFIED: 0
FROZEN_CONFORMANCE_FILES_MODIFIED: 0
MCP_FILES_MODIFIED: 0
RULE_PACKAGE_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0
BLOCKER_REPORT_PRESERVED: true
BLOCKER_LOCAL_COMMIT_IN_PARENT_CHAIN: false
GITHUB_CI_AT_MANIFEST_HEAD: PENDING
MAIN_MODIFIED: false
RELEASE_CREATED: false
WP4B_STARTED: false
REQUESTED_GATE: NONE_UNTIL_REMOTE_CI_PASS
```

The original dirty `D:/FCoP` was not switched, cleaned, reset, migrated or redeployed. Original blocker worktree remains at `73a7dd930de70819193a30264ca31ac6f9dd8e4a` clean; that local commit is not in this branch's parent chain. Remote main was read as `68dbeb15f4e7f84e1d03f907be9fa66c2265843e`, not modified. Completion of delivery is not self-signing acceptance and authorizes no WP4B work.
