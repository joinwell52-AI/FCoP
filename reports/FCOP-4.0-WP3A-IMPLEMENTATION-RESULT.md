# WP3A implementation result

## Outcome

WP3A local implementation verification passes. All 10 required behavior IDs
pass without changing the frozen specification or conformance suite. The
original 1225-test regression baseline is preserved, with 48 new implementation
tests added. This content commit does not claim a push that has not happened:
GitHub delivery is completed only by the subsequent Manifest commit, push,
fetch and exact hash/reachability receipt.

```yaml
AUTHORIZED_SCOPE: WP3A_ONLY
START_POINT: ffbfa0084f9b2758d95a09ecfbd89120b77b13cf
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
WORKTREE: D:/FCoP-wp3a-creation-plane
BRANCH: review/fcop-4.0-wp3a-creation-plane
WP3A_TARGET_IDS: 10/10
WP3A_TARGET_IDS_PASSED: 10/10
V3_REGRESSION: 1273 passed, 2 skipped (1225 baseline plus 48 new)
V3_NEW_FAILURES: 0
V4_STATIC_META: 27 passed
V4_BEHAVIORAL: 25 passed / 67 expected future-stage failures / 0 unexpected failures
V4_TOTAL: 52 passed, 67 failed
V4_COLLECT_ONLY: 119 collected
CONCURRENCY_IDEMPOTENCY: PASS
NEW_RUNTIME_DEPENDENCIES: 0
NEW_BACKGROUND_COMPONENTS: 0
NEW_AUTHORITATIVE_STORES: 0
FROZEN_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0
MAIN_MODIFIED: false
RELEASE_CREATED: false
WP3B_STARTED: false
REQUESTED_GATE: WP3A_IMPLEMENTATION_ACCEPTED
GATE_SELF_SIGNED: false
```

## Reproduction and actual results

Commands run from the independent worktree with `PYTHONPATH=mcp/src;src`
(use the platform path separator outside Windows). Native environment:
Windows, Python 3.12, local NTFS. Deprecation warnings are inherited from
`src/fcop/teams/__init__.py:31`; the two legacy-schema skips match input.

| Command | Actual result |
|---|---|
| `python -m pytest tests/test_fcop -q --tb=short` | 956 passed |
| `python -m pytest tests/test_fcop_mcp -q --tb=short` | 80 passed |
| `python -m pytest -q --ignore=tests/conformance/v4 --tb=short` | 1273 passed, 2 skipped |
| `python -m pytest tests/test_fcop/test_v4_creation.py -q --tb=short` | 48 passed |
| `python -m pytest tests/conformance/v4 -q --tb=no` | 52 passed, 67 failed; expected partial implementation |
| `python -m pytest tests/conformance/v4 --collect-only -q` | 119 collected; unchanged |
| Static/meta files: test_c0_contract_authority, test_mcp_surface_contract, test_meta_profile_boundary, test_meta_stub_guard, test_static_driver_surface | 27 passed |
| C1/C2/C7 files with `-k 'not test_at_01 and not test_c7_create_01'` | 10 passed, 2 deselected |
| `python -m mypy src/fcop` | PASS, 33 source files |
| Same mypy command with `--platform linux` / `--platform darwin` | PASS / PASS; type checking, not native execution |
| `python -m mypy --config-file mcp/pyproject.toml mcp/src/fcop_mcp` | PASS, 12 files |
| Same MCP configuration with `tests/test_fcop_mcp` | PASS, 5 files |
| Ruff on modified/new Python files | PASS |
| `python -m ruff check mcp/src tests/test_fcop_mcp` | PASS |
| `python -m ruff check src tests --output-format concise` | 21 inherited diagnostics, all in frozen conformance files; identical on input worktree |
| `git diff --check` | PASS |
| Strict UTF-8/LF validation of the 11 delivery content files | PASS; existing CRLF normalized mechanically only in authorized delivery files |
| Frozen spec/conformance/WP1 SHA-256 comparison | 48/48 match input Git blobs after accounting for Git checkout CRLF; frozen files themselves were not normalized or edited |

Full-root Ruff is explicitly **not** reported green. No configuration was
weakened and no frozen file was reformatted to hide those 21 diagnostics.
Existing CI triggers only main/feat pushes or PRs to main; this review-branch
delivery does not constitute a native three-OS CI run. No PR/workflow changes
were made to trigger extra work outside authorization.

## Required targets and behavioral evidence

Node names below are under `tests/conformance/v4/` and remain unchanged.

| ID | Node | Evidence |
|---|---|---|
| C1-N01 | test_c1_workspace.py::test_c1_n01 | Real manifest, identity and TASK |
| C1-R01 | test_c1_workspace.py::test_c1_r01 | Mismatched workspace rejected, byte snapshot unchanged |
| C1-FORK-01 | test_c1_workspace.py::test_c1_fork_01 | New derived identity; retention refused |
| C1-OFFLINE-01 | test_c1_workspace.py::test_c1_offline_01 | No global registry or invisible-copy claim |
| C2-N01 | test_c2_envelopes.py::test_c2_n01 | Four actual typed envelopes |
| C2-R01 | test_c2_envelopes.py::test_c2_r01 | Invalid request rejected without writes; see supplemental parsing test below |
| C2-R02 | test_c2_envelopes.py::test_c2_r02 | Replacement REPORT/new REVIEW; old bytes unchanged |
| C7-N01 | test_c7_idempotency.py::test_c7_n01 | Existing, same ID/path/digest, no additional bytes |
| C7-R01 | test_c7_idempotency.py::test_c7_r01 | Conflicting digest rejected, original bytes unchanged |
| C7-X01 | test_c7_idempotency.py::test_c7_x01 | Synchronized spawned writers and fresh spawned restart |

The frozen C2-R01 passes an absolute envelope path. WP3A's taskbook rejects
absolute paths, so that node alone does not prove type parsing. The new
`test_inspect_really_parses_envelopes` first reads a valid relative-path TASK,
then independently rejects EVAL, mismatched IDs/workspace, missing timezone,
invalid UTF-8, CRLF and duplicate YAML keys. No frozen test was modified.

Additional implementation tests independently check the canonical SHA-256
object (including NFC/defaults/weak-reference warnings), all three append-only
fact types, constructor-only registry copying/freezing, caller-judge rejection,
unsupported manifests, legacy layout preservation, path escapes and both
instance/class-call rejection of out-of-stage mutators.

`test_spawn_same_key_and_restart[False]` executes two real same-digest writers;
`[True]` executes different digests at the same operation key and requires one
success and one OPERATION_ID_CONFLICT. Both repeat in a new spawned process
and require unchanged disk bytes. `test_kernel_lock_timeout_and_release`
holds the lock in another process, observes a bounded failure, then proves
release and reuse. No fork-only worker, mocked Project or surface probe is
used as concurrency evidence.

Creation failure tests preserve orphan/corrupt/duplicated operation facts,
changed result bytes and no-overwrite publication temporaries. They do not
expose a production fault-injection/recovery API or implement migration recovery.

## Fifteen incidental passes — not later-stage completion

| Node / ID | Why it passes | What is not implemented |
|---|---|---|
| C3-R01 | Illegal-edge refusal | Legal T2–T7 moves |
| C3-R02 | Ambiguous TASK reader refuses multiple paths | Recovery/repair |
| C3-R03 | Legacy finish is rejected | Evidence-gated completion |
| C3-GATE-01[T1] | Actual T1 creation | T2–T7 matrix |
| C4-N01 | Static relation parsing | Dynamic Branch policy |
| C4-N02 | Unresolved weak citation warning | Gate-strength evidence resolution |
| C4-R01[dangling-parent] | Static strong-reference rejection | Lifecycle gates |
| C4-R01[cross-workspace] | Referenced envelope identity validation | Cross-workspace routing |
| C4-R01[self-cycle] | Static cycle rejection | Family locking |
| C4-R01[nonunique-parent] | Reject non-single strong reference | Dynamic hierarchy policy |
| C5-FAMILY-RACE-01 | Branch create succeeds, T3 is unavailable; test permits this combination | Family linearization; this green is not proof of a real two-commit race |
| AT-04 | Append a convergence-shaped REVIEW; T7 is unavailable and Root stays done | Digest evaluation or Root archive gate; this green is not proof of convergence correctness |
| AT-01 | Create idempotency also covers branch_of as a digest field | Dynamic Root/Branch admission |
| C8-X02 | Ambiguous state read fails closed | Five-state recovery |
| AT-02 | Ambiguous state read fails closed | Mechanical duplicate repair |

The two permissive future-race nodes above are a **test-evidence limitation**,
not a reason to claim family/archive functionality or edit frozen tests. The
67 remaining behavioral failures are in deferred lifecycle, dynamic relation,
evidence/head, Profile authorization, family/convergence and recovery scopes.
There are no unexpected failures among the ten authorized target IDs or the
27 static/meta nodes.

## Scope and delivery

11 content files plus one Manifest are expected. The only existing production
files modified are project.py and errors.py; all other implementation is in
the private v4 package. The additional existing test snapshot is additive.
Spec, frozen conformance, WP1 reports, MCP, schemas, rules, versions, build,
dependencies and release workflow remain unchanged. D:/FCoP and prior
worktrees are preserved. The unrelated CodeFlowMu question was answered using
read-only inspection; no CodeFlowMu file was changed.

The Manifest records exact Git-blob SHA-256 hashes, avoiding Windows checkout
line-ending ambiguity. Its self commit is denoted SELF and resolved in the
final remote verification receipt rather than recursively embedded. Completion
requires that receipt; local content success alone does not sign the Gate.
After delivery, stop and request `WP3A_IMPLEMENTATION_ACCEPTED` only.
