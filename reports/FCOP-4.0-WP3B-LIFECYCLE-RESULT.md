# FCoP 4.0 WP3B Lifecycle Plane Result

## 1. Outcome

```yaml
WP3B_STATUS: COMPLETE
AUTHORIZED_SCOPE: WP3B_ONLY
INPUT_HEAD: d2d2e9518451d58d165e3705f13f1ceb24388571
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
IMPLEMENTABILITY_PROOF: PASS
PHYSICAL_CRASH_WINDOWS_MAPPED: 10/10
LINEARIZATION_PROOF: PASS
T2_STATUS: COMPLETE
T3_STATUS: COMPLETE
WP3B_TARGET_NODES: 9/9
WP3A_TARGET_IDS: 10/10
WP3A_1_REGRESSION: PASS
FROZEN_TEST_IDS: 60/60
REQUESTED_GATE: WP3B_LIFECYCLE_ACCEPTED
```

No Gate is self-signed. WP3C has not started.

## 2. Implemented behavior

- T2 moves one unique inbox TASK to active, appends exactly one event, creates a
  new UUID-URN attempt, and returns the same attempt with a durable receipt.
- T3 derives the active attempt, computes the unique final/replacement REPORT
  head under the family lock, hashes the complete validated REPORT bytes, and
  stores aligned evidence references/digests in its one event.
- Each transition persists PREPARED, TARGET_DURABLE and COMMITTED receipt stages
  through distinct no-overwrite and receipt-replace primitives. Recovery uses
  the frozen five-state classifications and never overwrites a target.
- Branch create, T2/T3 and current-attempt REPORT writes share one deterministic
  Root-family boundary. Branch creation rechecks Root state/depth after locking;
  REPORT writes recheck attempt/head after locking.
- `inspect_state(task_id=...)` reports path-derived NOW, complete-byte digest,
  last event and provable current attempt; multi-path state fails closed.
- T4–T7 remain unavailable with the existing Toolkit not-implemented code;
  `finish_task` remains forbidden for v4.

## 3. Final verification

All commands were run in `D:/FCoP-wp3b-lifecycle` on native Windows 11,
Python 3.12 and local NTFS. Commands involving MCP used
`PYTHONPATH=mcp/src;src`, matching the established review procedure so the
worktree packages—not older site-packages—were tested.

| Check | Actual result |
|---|---|
| `python -m pytest tests/test_fcop/test_v4_lifecycle.py -q` | 32 passed |
| WP3B nine frozen nodes | 9 passed |
| WP3A C1/C2/C7 target selection | 10 passed, 2 deselected |
| `test_v4_creation.py -k closeout` | 46 passed, 48 deselected |
| `python -m pytest tests/test_fcop -q` | 1034 passed |
| `python -m pytest tests/test_fcop_mcp -q` with bound worktree packages | 80 passed |
| `python -m pytest -q --ignore=tests/conformance/v4` with bound packages | 1351 passed, 2 skipped |
| Five frozen static/meta modules | 27 passed |
| Full frozen v4 suite | 62 passed, 57 expected later-stage failures |
| Frozen v4 collect-only | 119 collected |
| `python -m mypy src/fcop` | PASS, 36 source files |
| mypy `--platform linux` / `--platform darwin` | PASS / PASS (type checks only) |
| changed-file Ruff | PASS |
| whole `src tests` Ruff | 21 inherited frozen-test diagnostics; no 22nd diagnostic |
| `git diff --check` | PASS |

The input count `1319 passed, 2 skipped` is the complete non-conformance suite,
not `tests/test_fcop` alone. The latter input count is 1002. WP3B adds exactly
32 lifecycle tests: `1002 + 32 = 1034` and `1319 + 32 = 1351`, with zero new
v3/MCP failures.

An initial MCP invocation without a worktree `PYTHONPATH` loaded the machine's
older installed `fcop_mcp` and produced one known formatting failure. Module
paths proved that contamination (`site-packages/fcop_mcp` versus this
worktree's `mcp/src/fcop_mcp`). Re-running the same suite against the fixed
input/worktree packages passed 80/80; no source change was made for the
environmental mismatch.

Full v4 changed from 52/67 to 62/57. Nine new passes are the authorized WP3B
nodes. The tenth is `AT-03`, the frozen true-operation REPORT-write/T3 race that
WP3B §13.3 explicitly requires. It is evidence for the shared T3 boundary, not
a claim that WP3C, WP3D or WP3E is implemented. All remaining 57 failures are
preserved red lights for later lifecycle, authorization, convergence and public
recovery work.

## 4. Compatibility and complexity ledger

```yaml
NEW_RUNTIME_DEPENDENCIES: 0
NEW_BACKGROUND_COMPONENTS: 0
NEW_AUTHORITATIVE_STORES: 0
NEW_PUBLIC_APIS: 0
PUBLIC_APIS_REMOVED: 0
V3_METHOD_SIGNATURE_CHANGES: 0
NEW_BASE_ERROR_CODES: 0
FROZEN_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0
MAIN_MODIFIED: false
RELEASE_CREATED: false
WP3C_STARTED: false

NATIVE_WINDOWS_TESTED: true
LINUX_TYPE_CHECKED: true
MACOS_TYPE_CHECKED: true
NATIVE_LINUX_TESTED: false
NATIVE_MACOS_TESTED: false
```

The three new modules are private implementation boundaries, not public API:
`lifecycle.py` plans and commits T2/T3, `receipts.py` validates and classifies a
single file transaction, and `linearization.py` derives and holds a short family
lock. No scheduler, cache, database, registry, queue, daemon, watcher, timer,
network operation, role table, UI state, new dependency or second facade was
introduced.

## 5. Delivery state

This report precedes the required two-commit delivery. The final Content Commit,
Manifest Commit, remote HEAD, refetch verification and delivery blob SHA-256
values are recorded in `reviews/fcop-4.0/wp3b/MANIFEST.md`. The requested Gate
remains `WP3B_LIFECYCLE_ACCEPTED`; implementation stops after remote verification.
