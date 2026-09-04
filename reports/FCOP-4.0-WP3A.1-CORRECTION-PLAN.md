# WP3A.1 correction plan

## Task and pre-write review

ME (solo) executes ADMIN's four-item closeout only. This document records
the authorized task, proposal and re-read scope check before production edits;
the result report records execution. ADMIN alone accepts the Gate.

- Input: `20b9fc25b66b6d52b9f7c761db5a18e1379794b8`.
- Worktree: `D:/FCoP-wp3a1-boundary-closeout`.
- Branch: `review/fcop-4.0-wp3a.1-boundary-initialization`.
- Taskbook SHA-256: `5f21440a88d90f5975a52db22fd37863595658b904eba3e3e1c03c408f69cb5f`.
- Fetch confirmed the fixed WP3A remote HEAD; initial worktree clean;
  frozen contract and input ancestor checks passed.
- Main before delivery: `68dbeb15f4e7f84e1d03f907be9fa66c2265843e`.

## Input evidence

With `PYTHONPATH=mcp/src;src`, before any production edit:

| Command | Result |
|---|---|
| `python -m pytest -q --ignore=tests/conformance/v4 --tb=short` | 1273 passed, 2 skipped |
| `python -m pytest tests/conformance/v4 -q --tb=no` | 52 passed, 67 failed; 27 static/meta + 25 behavior passes |
| `python -m pytest tests/conformance/v4 --collect-only -q` | 119 collected |

The existing descriptor demonstrably loses function discovery: only the
classmethod validate_team appears in public `inspect.isfunction` discovery.
`create_autospec(Project).write_task` exposes the descriptor's generic
`(instance, *args, **kwargs)` instead of the legacy method signature.
This is evidence for a minimal boundary change, not a claim of compatibility.

## Exact planned inventory

Existing files:

1. `src/fcop/v4/creation.py`: strict classification, staged initialization,
   relative durable result paths and current-root API resolution.
2. `src/fcop/v4/encoding.py`: private no-overwrite directory publication primitive.
3. `src/fcop/v4/boundary.py`: replace catch-all custom descriptors with explicit
   method classification and ordinary function wrappers; retain one boundary.
4. `tests/test_fcop/test_v4_creation.py`: append new A-E acceptance evidence;
   retain all original 48 nodes and assertions.

New documents:

5. `reports/FCOP-4.0-WP3A.1-CORRECTION-PLAN.md`.
6. `reports/FCOP-4.0-WP3A.1-CORRECTION-RESULT.md`.
7. `reports/FCOP-4.0-WP3A.1-COMPATIBILITY-DECISION.md`.
8. `reviews/fcop-4.0/wp3a.1/MANIFEST.md` (separate delivery commit).

No project.py or public snapshot edit is currently needed. Any expansion
requires an appended decision before the additional edit.

## Four changes / test mapping

| Item | Minimal design | Acceptance evidence |
|---|---|---|
| Manifest | Use the same strict JSON reader before any version classification; invalid declaration keeps diagnostic construction but rejects writes | A: duplicate keys/order, malformed encoding/JSON and both public writer paths, unchanged snapshots |
| Initialization | Build complete unpredictable sibling staging, persist it, publish canonical directory with platform no-replace rename; preserve all failed staging | B/C: injected failures before/after each publication boundary, response loss, real spawned initialization race, existing destination and retained staging |
| Operation fact | Save canonical Project-relative POSIX path; validate it before safe resolution; return absolute API path derived at call time | D: move project directory and retry, unchanged identity/digest/bytes, tamper rejection |
| Compatibility | Explicit COMMON_SAFE/V4_HANDLER/V4_READ_UNAVAILABLE/V4_MUTATION_REJECTED/LEGACY_ONLY classifications, native function wrappers; reject unclassified future public members at class construction | E: original 38 signatures/metadata, discovery, binding, class calls, autospec, subclass/super, unsupported mutation rejection |

Initialization failures retain staging rather than auto-clean or merge it.
Pre-existing staging prevents a new attempt if canonical is absent, with
RECOVERY_REQUIRED; concurrent contenders that already passed this check still
compete via a kernel no-replace publication, never scan-then-overwrite.
No background recovery or lifecycle transition is added.

## Verification and stop

Run new tests first against input where meaningful, then all old/new creation
tests, 10 target IDs, regression and MCP, full frozen conformance and collect,
Ruff (record existing 21 diagnostics), mypy on Windows/Linux/macOS targets,
UTF-8/LF, frozen hashes and diff scope. Native Windows only unless another
native platform is actually run. Commit content then Manifest, push only the
new review branch, fetch and verify all remote blob hashes and ancestry.
Stop and request `WP3A_IMPLEMENTATION_ACCEPTED`; no WP3B execution.

## Decision log 1

The first new-test run reproduced 3 failures and 1 pass (both duplicate-key
orders were tested; one already failed closed incidentally). Explicit strict
classification fixes both orders. A later code read clarified validate_team
is a **staticmethod**, not the preliminary note's classmethod; it remains
COMMON_SAFE and unwrapped. No Project source or snapshot edit is needed.

The initial expanded suite passed 82 nodes (original 48 + 34 new). Two new
test-only import-order diagnostics were corrected without changing lint config.
Directory publication uses Windows MoveFileExW WRITE_THROUGH/no replace,
Linux renameat2 RENAME_NOREPLACE, or Darwin renamex_np RENAME_EXCL; no unsafe
plain rename fallback. Native POSIX results will not be inferred from mypy.

## Decision log 2 — stop for ADMIN clarification

Full regression exposed a literal taskbook conflict: section 5.2 rejects all
CRLF manifests, whereas the unchanged Windows v3 fixture at
`tests/test_fcop/test_project_boundary.py:41` writes CRLF and requires legal
REVIEW writes at lines 165 and 180. The allowed test edit inventory excludes
that fixture. No compatibility exception or fixture change is assumed.

The same full verification also exposed an implementation regression in the
new wrapper candidate: v4 bound methods advertise the legacy signature, so
the frozen driver rejects valid report requests. This is our unfinished
boundary change, **not** a contract contradiction or a reason to edit tests.
It must be corrected within the existing implementation scope upon resumption.

Production edits stop. The result and compatibility documents record BLOCKED,
all actual failures, and the narrow requested CRLF ruling. Nothing is committed
or pushed as a completed correction package; the independent worktree is kept.

## Decision log 3 — ADMIN clarification approved; resume WP3A.1 only

ADMIN_CLARIFICATION: WP3A_1_MANIFEST_LINE_ENDING_COMPATIBILITY.
DECISION: APPROVED. Legacy CRLF is allowed; v4 CRLF is rejected and LF required.
All version classification rejects duplicate JSON keys and invalid UTF-8;
request fields never select versions and ambiguous declarations never fall back.
This supersedes the taskbook's overbroad CRLF row, not the frozen specification.

Use two phases over the same bytes: strict UTF-8/unique-key JSON classification
without a CRLF restriction, then apply the selected version's Encoding. Confirmed
legacy retains its original behavior; v4 requires strict UTF-8/no BOM/LF.

Exact inventory expansion before editing: `src/fcop/project.py`, solely to
connect private instance-method binding after construction and successful
create_workspace. Class-level ordinary wrappers retain old signatures/autospec;
supported v4 methods get per-instance callables with the actual handler signature.
Binding does not replace subclass overrides or add a public API. The original
four new v4 failures must disappear without changing the frozen driver.

Append explicit legacy CRLF, v4 CRLF, duplicate classification, signature and
subclass tests. The earlier new `{CRLF}` invalid-input case will be changed to
an explicit v4 declaration in accordance with ADMIN's ruling; original WP3A
48 tests remain unchanged. No failed candidate may be committed or pushed.

## Decision log 4 — final verification after clarification

The final candidate passes 1319 regression tests (1273 input + 46 new), with
the same two skips; MCP passes 80; WP3A targets pass 10/10; Static/Meta passes
27. Full conformance is restored to 52 passed / 67 deferred failures and 119
collected. All 11 CRLF-triggered failures and all four wrapper-triggered failures
are closed. No new incidental conformance passes are introduced.

During resumption, checking old manifests through the modern TeamConfig parser
also exposed two historical v2 string-version fixtures. Classification now
recognizes their declared 1/2/3 semver strings without rewriting the manifest
or imposing newer config validation. The legacy is_initialized diagnostic still
uses its selected workspace, including explicit workspace_dir overrides.
These temporary regressions were repaired before the final full run.

The final boundary installs per-instance supported handler signatures only
after trusted initialization or successful creation, preserving subclass
overrides. Class-level wrappers retain legacy signatures and autospec. A probe
of whole-object v4 autospec encountered the pre-existing unsupported legacy
config property; the signature acceptance test therefore exercises v4 bound
method autospec and the required class/legacy-object autospec separately. No
new v4 config API or property semantics were introduced to bypass that limit.

Exact final inventory: five existing files (the four originally planned files
plus project.py), three reports, then one Manifest: 8 content files, 9 total.
The public snapshot is untouched. Original 38 legacy method AST bodies,
parameters and documentation match the pre-WP3A source. Frozen authoritative
spec/WP1/conformance file hash comparison covers 24 actual files; 60/60 matrix
IDs remain present. Original 48 creation-test source text is unchanged.
