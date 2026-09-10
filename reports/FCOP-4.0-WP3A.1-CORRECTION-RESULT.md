# WP3A.1 correction result

## Outcome

All four closeout items pass local verification following ADMIN clarification
WP3A_1_MANIFEST_LINE_ENDING_COMPATIBILITY. No failed state is being submitted.
The earlier 11 v3 and four v4 regressions are restored. Completion of GitHub
delivery requires the subsequent Manifest commit, push, fetch and final receipt;
this content document does not claim a push before it happens.

```yaml
LOCAL_VERIFICATION: PASS
AUTHORIZED_SCOPE: WP3A_1_ONLY
INPUT_HEAD: 20b9fc25b66b6d52b9f7c761db5a18e1379794b8
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
WORKTREE: D:/FCoP-wp3a1-boundary-closeout
BRANCH: review/fcop-4.0-wp3a.1-boundary-initialization
AUTHORIZED_TASKBOOK_SHA256: 5f21440a88d90f5975a52db22fd37863595658b904eba3e3e1c03c408f69cb5f
P0_MANIFEST_FAIL_OPEN: RESOLVED
P0_WORKSPACE_PARTIAL_VISIBILITY: RESOLVED
P1_OPERATION_PATH_PORTABILITY: RESOLVED
P1_DESCRIPTOR_COMPATIBILITY: NARROWED
WP3A_TARGET_IDS: 10/10
WP3A_TARGET_IDS_PASSED: 10/10
WP3A_1_TESTS: 46 passed
V3_REGRESSION: 1319 passed, 2 skipped
V3_NEW_FAILURES: 0
MCP_REGRESSION: 80 passed
V4_STATIC_META: 27 passed
V4_BEHAVIORAL: 25 passed / 67 deferred failures / 0 new failures
V4_COLLECT_ONLY: 119
FROZEN_TEST_IDS: 60/60
NEW_RUNTIME_DEPENDENCIES: 0
NEW_BACKGROUND_COMPONENTS: 0
NEW_AUTHORITATIVE_STORES: 0
NEW_PUBLIC_APIS: 0
PUBLIC_APIS_REMOVED: 0
V3_METHOD_SIGNATURE_CHANGES: 0
FROZEN_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0
MAIN_MODIFIED: false
RELEASE_CREATED: false
WP3B_STARTED: false
NATIVE_WINDOWS_TESTED: true
LINUX_TYPE_CHECKED: true
MACOS_TYPE_CHECKED: true
NATIVE_LINUX_TESTED: false
NATIVE_MACOS_TESTED: false
REQUESTED_GATE_AFTER_DELIVERY: WP3A_IMPLEMENTATION_ACCEPTED
GATE_SELF_SIGNED: false
```

## Actual verification

Commands run from this independent worktree with `PYTHONPATH=mcp/src;src` on
Windows/Python 3.12/local NTFS. Native Linux/macOS execution is not claimed.

| Command / check | Final actual result |
|---|---|
| `python -m pytest tests/test_fcop -q --tb=short` | 1002 passed |
| `python -m pytest tests/test_fcop_mcp -q --tb=short` | 80 passed |
| `python -m pytest -q --ignore=tests/conformance/v4 --tb=short` | 1319 passed, 2 skipped |
| `python -m pytest tests/test_fcop/test_v4_creation.py -k closeout -q --tb=short` | 46 passed, original 48 deselected |
| Original creation-test source prefix vs input | Byte-equivalent text after checkout EOL normalization; all original 48 nodes retained |
| Post-LF `test_v4_creation.py` plus `test_public_surface.py` | 98 passed (94 creation + 4 public-surface checks) |
| C1/C2/C7 with `-k 'not test_at_01 and not test_c7_create_01'` | 10 passed, 2 deselected |
| Five static/meta modules from WP3A | 27 passed |
| `python -m pytest tests/conformance/v4 -q --tb=no` | 52 passed, 67 failed |
| `python -m pytest tests/conformance/v4 --collect-only -q` | 119 collected |
| WP1 matrix test IDs present in frozen suite | 60/60, no missing IDs |
| `python -m ruff check src tests --output-format concise` | 21 inherited diagnostics in frozen conformance; no new diagnostics |
| Ruff on changed Python files and separately MCP source/tests | PASS / PASS |
| `python -m mypy src/fcop` | PASS, 33 files |
| Same mypy command with `--platform linux` and `--platform darwin` | PASS / PASS, type checks only |
| `python -m mypy --config-file mcp/pyproject.toml mcp/src/fcop_mcp` | PASS, 12 files |
| Same MCP mypy configuration on tests/test_fcop_mcp | PASS, 5 files |
| Original Project method bodies/signatures/docs vs pre-WP3A ffbfa008 | 38/38 unchanged AST/docstrings |
| Frozen spec, WP1 reports and conformance files | 24/24 actual Git-blob hash matches after in-memory checkout EOL normalization |
| UTF-8/LF and git diff --check | PASS for all 8 content files / PASS |

The regression increase is exactly 46 tests: 1273 input + 46 = 1319. The two
legacy-schema skips and importlib deprecation warning are inherited. Root Ruff
is **not** reported green, and no configuration or frozen test was changed.
Full v4 returns to the original 25 behavioral passes and 67 deferred failures.
The same 15 incidental WP3A passes remain non-evidence for later-stage acceptance;
there are no new passes used to claim T2-T7, authorization, family or recovery.

## A. Manifest: classify strictly, then apply the selected Encoding

Both phases operate on the same captured manifest bytes. Classification decodes
strict UTF-8 and rejects duplicate keys, including nested keys, before routing.
CRLF is permitted in this first phase. Recognized old declarations retain legacy
behavior; exact v4 applies no-BOM/LF validation. Unknown/malformed versions and
unclassifiable objects do not reach a legacy writer. Business request fields
cannot change binding. Existing v4 instances recheck strict manifest bytes.

New tests cover both duplicate-version orders, CRLF plus a duplicate version,
duplicate identity/encoding/unknown/nested fields, bad UTF-8/BOM/JSON, NaN,
unknown versions, v4 CRLF against reopened and existing Project objects, and
legacy CRLF with real successful REVIEW writing. Failure assertions compare the
whole filesystem tree (files and directories), not just returned exceptions.
The original taskbook hash is unchanged; the ADMIN ruling is appended to both
CORRECTION-PLAN and COMPATIBILITY-DECISION.

## B/C. Workspace publication and concurrent initialization

Initialization validates first, builds a complete unpredictable sibling staging
directory, persists its manifest and minimum directory tree, then publishes it
to canonical fcop/ with a no-replace OS directory operation. Failed staging is
retained as evidence; an earlier unresolved staging blocks a new attempt when
canonical is absent. No cleanup service or automatic recovery was introduced.

`test_closeout_initialization_faults` covers before staging, before manifest,
partial directory construction, complete staging before publication, actual
no-replace publication failure, and response loss after successful publication.
At each point canonical is absent or complete. The publication-failure case
redirects the internal seam to an already existing empty test directory to prove
that the actual OS primitive will not replace even an empty destination.
Separate existing-canonical and retained-staging tests assert unchanged bytes.

`test_closeout_spawn_initialization_no_overwrite` uses two independent spawned
processes, both fully staged before a barrier releases real public create calls
into OS publication. Exactly one wins; the loser gets a structured collision,
cannot change the winner's tree, and retains its staging. The original spawned
TASK idempotency/restart and kernel-lock tests remain unchanged and pass.
Fault seams are private monkeypatches, not public production fault-injection APIs.

## D. Portable operation facts

The durable path is relative to Project root and serialized with POSIX separators:
`fcop/_lifecycle/inbox/<task_id>.md`. It is checked for canonical form and bound
through safe_path on use. No original drive/root is persisted. First and Existing
API results remain absolute paths derived from the **current** Project root.

Moving an entire temporary project and reopening it returns the same task_id and
digest at the new absolute path with no added/changed facts or second TASK.
Traversal, absolute, drive-qualified, another-workspace, backslash, empty/dot
segment and non-string fact paths fail closed with unchanged tree snapshots.

The immutable operation key identifies workspace_id/kind/operation_id; task_id
and echoed request digest identify its result. Initial path and content digest
are creation snapshots, not NOW authority. WP3B will need to prove later legal
TASK transitions by identity/evidence without rewriting this fact. In WP3A.1,
unprovable changed/migrated TASK contents return RECOVERY_REQUIRED, never a second
create. No migration or old candidate-format converter was added.

## E. Version binding and compatibility

The blanket custom descriptor is replaced with an explicit immutable policy table
and ordinary function wrappers. The safe staticmethod is not wrapped. Unknown
future public methods require an explicit policy at class construction.
Original class signatures and autospec are preserved. A private connection in
Project construction/create_workspace binds supported v4 instance callables with
their actual handler signature. They still call through the class boundary;
class-style calls cannot bypass it. Inherited behavior and super calls pass;
normal subclass overrides are not overwritten or treated as a security boundary.

Current compatibility evidence covers original 38 method metadata/body/signature
parity, real legacy and v4 calls, class/legacy-object autospec, bound v4 method
autospec, patch.object, subclass behavior and all rejected legacy mutators.
Whole-object autospec on v4 still encounters the pre-existing unsupported legacy
config property; no new config API is implemented. This observable limitation
is documented rather than changing v3 property semantics outside this task.

## Historical failed iterations — not final delivery status

The first closeout candidate followed the original overbroad CRLF rule and
produced 11 v3 failures. Its initial ordinary wrapper also advertised v3 signatures
on v4 instances, causing four new conformance failures (C2-N01, C2-R02, C4-N01,
AT-04). It was stopped, reported and never committed or pushed. ADMIN then
approved the two-phase interpretation and explicitly authorized continued repair.
Both defects are closed by the final runs above. A subsequent exploratory legacy
classification check exposed semver-string and explicit-workspace diagnostic
compatibility; those were repaired without changing any original regression test.
CORRECTION-PLAN retains the chronological decisions and authorized file expansion.

## Scope, delivery and stop

Eight content files plus a separate Manifest (nine total). Production changes
are only project.py and the three private v4 modules; the only test edit appends
implementation-level acceptance tests to test_v4_creation.py. No snapshot,
specification, frozen conformance, WP1 report, lifecycle module, errors/model,
MCP, dependency, version, build, release or CodeFlowMu file is modified.

After the content commit, add the Manifest alone, push only
`review/fcop-4.0-wp3a.1-boundary-initialization`, fetch and read remote objects,
verify all eight content hashes and exact parent/HEAD ancestry, preserve main,
then issue the final receipt requesting WP3A_IMPLEMENTATION_ACCEPTED and stop.
This package does not authorize WP3B or sign ADMIN's Gate.
