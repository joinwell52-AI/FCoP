# WP3A implementation plan

## Task / authority

ADMIN's WP3 master taskbook authorizes WP3A only. ME (solo) executes;
ADMIN retains acceptance authority. This plan records the task and pre-write
self-review; the result document records execution. No dogfood ledger, real
workspace, or rule deployment is changed.

- Taskbook: `D:/FCoP/docs/fcop-architecture-series/FCoP-4.0-WP3-Implementation-Master-Taskbook.zh.md`
- SHA-256: `2fdc907703fabb60c4ce89092588fbdc86bf821fb05007c9165a5b0593b2d99c`
- Input: `ffbfa0084f9b2758d95a09ecfbd89120b77b13cf`
- Worktree: `D:/FCoP-wp3a-creation-plane`
- Branch: `review/fcop-4.0-wp3a-creation-plane`
- Remote main observed: `68dbeb15f4e7f84e1d03f907be9fa66c2265843e`
- Frozen specification: `spec/fcop-4.0-spec.md`, F4.2–F4.5, F4.8,
  F4.10–F4.12. No specification or conformance edits are authorized.

## Input verification (before implementation)

With `PYTHONPATH=mcp/src;src`, actual commands produced:

| Command | Result |
|---|---|
| `python -m pytest tests/test_fcop -q` | 908 passed |
| `python -m pytest tests/test_fcop_mcp -q` | 80 passed |
| `python -m pytest -q --ignore=tests/conformance/v4` | 1225 passed, 2 skipped |
| `python -m pytest tests/conformance/v4 --collect-only -q` | 119 collected |
| `python -m pytest tests/conformance/v4 -q --tb=no` | 27 passed, 92 failed (expected unimplemented behavior) |

The two subset commands do not cover all regression directories; the full
regression command is recorded separately, not mislabeled as their sum.
Input and frozen-contract commits are reachable. Initial worktree was clean.
The supplied taskbook hash was truncated to 57 characters; all 57 match the
full local hash above. No input code or test-count drift was observed.

## Exact intended file inventory

Existing file changes:

1. `src/fcop/project.py`: trusted initialization and centralized version boundary.
2. `src/fcop/errors.py`: additive structured v4 error; preserve v3 exceptions.

New files:

3. `src/fcop/v4/__init__.py`: private package declaration.
4. `src/fcop/v4/boundary.py`: manifest-based, per-instance version dispatch;
   unsupported legacy business operations fail closed on v4.
5. `src/fcop/v4/encoding.py`: strict parsing, paths, durable no-overwrite writes,
   local cross-process locking and canonical request normalization.
6. `src/fcop/v4/creation.py`: private creation functions, four envelopes, T1,
   durable TASK operation fact, derive and append-only review correction.
7. `tests/test_fcop/test_v4_creation.py`: implementation-level coverage,
   including real spawn races and restart, failure preservation and v3 isolation.
8. `reports/FCOP-4.0-WP3A-IMPLEMENTATION-PLAN.md`: this task/plan.
9. `reports/FCOP-4.0-WP3A-IMPLEMENTATION-RESULT.md`: actual results and stop request.
10. `reports/FCOP-4.0-WP3A-ARCHITECTURE-DELTA.md`: architecture and scope evidence.
11. `reviews/fcop-4.0/wp3a/MANIFEST.md`: separate delivery commit and content hashes.

Any inventory expansion requires an appended decision here before editing.

## Design and self-review

Project remains the only public side-effect facade. A private descriptor at
the facade boundary selects the legacy bound method unchanged or a private
v4 creation method; direct class invocation must pass the same boundary.
Manifest detection happens once at construction; explicit fresh-workspace
creation establishes the new manifest and binding. Missing declarations never
select v4 from directory layout or ordinary request fields. Registry input is
copied into a read-only mapping and is never evaluated in WP3A.

Creation uses strict UTF-8/LF, same-directory flushed/fsynced temporary files,
atomic no-overwrite publication, and short per-operation OS locks. Durable
operation facts are immutable JSON, not lifecycle state. A partial creation
must preserve evidence and fail closed rather than fabricate success.
References are statically validated; unresolved weak citations are reported,
not elevated into gate evidence. No dynamic Branch/REPORT-head rules land.

T1 appends exactly one creation event. Existing returns original identity,
path and digest with no changed bytes. Conflict leaves all bytes unchanged.
T2–T7 and recovery remain unavailable; legacy finish/history mutation is
rejected on v4. No new runtime dependencies or schema files are needed.

## Verification / delivery plan

Run all 10 WP3A target IDs, implementation tests (spawn same/different digest,
restart), original v3 regression, unchanged v4 static/meta and full v4 suite,
collect-only, existing Ruff and mypy commands, UTF-8/LF and git diff checks.
Report incidental later-stage passes without claiming stage completion.
Commit content, then Manifest only; push the authorized review branch, fetch
it again and verify every content hash and commit reachability. Preserve main.
Stop and request `WP3A_IMPLEMENTATION_ACCEPTED`; never self-sign or start WP3B.

## Decision log 1 — first test run

The first target run passed all 10 target IDs and AT-01 incidentally;
C7-CREATE-01 remained red at T2. Full original regression found three
construction-time compatibility regressions for malformed legacy manifests
and one additive public-API snapshot difference. The former must be fixed;
the latter requires a reviewed additive snapshot update, not test weakening.

Additional intended existing file: `tests/test_fcop/snapshots/public_api.json`
(exact snapshot location verified before editing). Update only newly
authorized creation API/error entries; retain every old signature and result.
Add explicit unavailable transition/legacy-finish entry points so unsupported
v4 calls receive structured errors rather than Python AttributeError. These
entry points do not perform transitions. Typed error constants are centralized
in the already planned errors module. Original legacy identity/config tests
and the full regression suite remain the compatibility evidence.

Inventory clarification before snapshot edit: its verified exact path is
`tests/test_fcop/snapshots/public_surface.json`, not `public_api.json`.
No file at the latter path was created or changed. The snapshot update will
be additive; CHANGELOG is outside this package and remains untouched, with
the unreleased API delta documented in the required architecture report.

## Decision log 2 — verification and scope review

Implementation tests grew to 48 nodes, all under the planned test file.
Create request planning now completes before lock/file creation; a separate
commit function performs the short per-key write. Error codes are enum-backed.
Manifest errors preserve the legacy constructor/is_initialized/config contract
while refusing writes against unclassifiable declarations. Kernel-lock files
remain in place, with no age-based deletion. Native platform checks are local
only; no registry/network dependency was added.

Full Ruff reproduces the same 21 diagnostics in the frozen conformance files
at both the input worktree and this worktree. They are recorded, not repaired
or excluded through configuration. Changed-file Ruff and the existing MCP
lint command pass. Windows native tests and Windows/Linux/macOS mypy targets
pass; native Linux/macOS execution has not occurred on this Windows host.
Existing CI does not trigger on review-branch pushes; no workflow/PR change
is authorized or made to manufacture a matrix result.

No additional paths beyond the original inventory and the explicitly added
public_surface.json snapshot are required. All old snapshot entries were
compared unchanged before adding six Project methods and V4ProtocolError.

## Decision log 3 — line-ending verification

Windows checkout/local editing left CRLF in some authorized content files.
A UTF-8-strict mechanical LF normalization was applied with Node only to
the 11 planned delivery content files, without changing text. No PowerShell
text-writing path was used. The 48 frozen files retain their checkout bytes;
their normalized Git-blob SHA-256 values all match the fixed input. Comparing
them directly with another worktree's raw bytes initially exposed a checkout
EOL difference, not a frozen content change. Git diff for frozen paths is empty.
