# WP4A.2 CI gate diagnosis

## Authority, plan and input verification

Executor: ME (solo); ADMIN owns acceptance. The fixed taskbook is the decision file; this diagnosis and RESULT are execution evidence, not a self-signed Gate.

- Taskbook: `7e2dcd3cc45f043c7981e7e5b79a78505ec109e8:taskbooks/fcop-4.0/WP4A.2/01-CI-Quality-Gate-Closeout-Taskbook-v1.0.zh.md`.
- Verified raw Git blob SHA-256: `5caf02c25bd8a02989151066a801dfd83eef117d0342d3b01e5e7a885cd5adba`.
- Its direct parent is INPUT_HEAD `6ff8f213313c1f802e3498d2196b8c3bd363ceb5`; `git merge-base --is-ancestor` returned 0.
- `gh pr view 14 --repo joinwell52-AI/FCoP --json headRefOid,headRefName,isDraft` returned the taskbook SHA, `review/fcop-4.0-wp4a.1-machine-contract`, and `true` before modification.
- New execution worktree: `D:/FCoP-wp4a2-ci-closeout`. The previous clean WP4A.1 worktree was detached at its unchanged `6ff8f21` HEAD to release the branch; the branch then fast-forwarded to the taskbook commit. No old files or commits were rewritten.
- Plan reviewed against the allowlist before execution: mechanical import cleanup, the explicitly authorized exception rename, exactly one SECTION extraction line, two reports and one Manifest. No production, Schema, CHANGELOG or threshold change is authorized.

## Remote failure evidence

Preserved failing [library run 34014373307](https://github.com/joinwell52-AI/FCoP/actions/runs/34014373307) belongs to INPUT_HEAD, not the future WP4A.2 Manifest HEAD. GitHub readback reports twelve lint-failed matrix jobs, successful coverage, failed Stability Charter and skipped dependent packaging.

- Ruff example: [Ubuntu 3.12 job 101435507343](https://github.com/joinwell52-AI/FCoP/actions/runs/34014373307/job/101435507343).
- Charter: [job 101435507259](https://github.com/joinwell52-AI/FCoP/actions/runs/34014373307/job/101435507259).

`python -m ruff check src tests --output-format concise` on the unmodified taskbook tree reproduced exactly:

| File under tests/conformance/v4/ | Baseline line | Code | Diagnosis |
|---|---:|---|---|
| driver.py | 8 | I001 | Import ordering/format |
| driver.py | 16 | UP035 | Callable, Mapping, Sequence from collections.abc |
| driver.py | 59 | N818 | Test exception needs Error suffix |
| scenarios.py | 6 | UP035 | Mapping, Sequence from collections.abc |
| test_c0_contract_authority.py | 3 | I001 | Import block spacing |
| test_c5_convergence.py | 3 | I001 | Import ordering/format |
| test_c7_idempotency.py | 3 | I001 | Import ordering/format |
| test_c7_idempotency.py | 5 | F401 | Unused pathlib.Path |
| test_mcp_surface_contract.py | 3 | I001 | Import block spacing |
| test_meta_profile_boundary.py | 3 | I001 | Import ordering |

Nine safe fixes were requested only on these seven files. Ruff's iterative fixer printed `Found 13 errors (12 fixed, 1 remaining)` because transformed imports required subsequent formatting passes; this is not thirteen distinct baseline diagnostics. The baseline check had ten, the remaining diagnostic was the already-authorized N818, and the final full check has zero. Diff inspection confines every import change to the listed sorting, modernization and unused import removal.

`V4NotImplemented` became `V4NotImplementedError` at its definition and four local references in driver.py. Its base, structured code `V4_NOT_IMPLEMENTED`, constructor, message and control flow remain unchanged. Repository search found no other references requiring edits.

## Zero-behavior-change proof

Compared against the fixed taskbook Git blobs, Python ASTs are identical after removing Import/ImportFrom nodes and normalizing only the authorized exception ClassDef.name / Name.id. This retains full function bodies, signatures, decorators, fixtures, calls, constants, exception handlers, assertions and expected values. Import differences were independently inspected in `git diff`; this normalization is not permission for arbitrary imports.

| Changed file | Assert nodes before = after | Non-import normalized AST |
|---|---:|---|
| driver.py | 0 | Equal |
| scenarios.py | 8 | Equal |
| test_c0_contract_authority.py | 6 | Equal |
| test_c5_convergence.py | 37 | Equal |
| test_c7_idempotency.py | 24 | Equal |
| test_mcp_surface_contract.py | 10 | Equal |
| test_meta_profile_boundary.py | 5 | Equal |
| Total | 90 | 7/7 equal |

All other Conformance files remain Git-identical. `pytest tests/conformance/v4 --collect-only -q` produced exactly the same ordered list of 119 node IDs before and after. The contract-token set extracted from all Conformance Python sources is unchanged at 60/60 (C0-C8, AT, MCP and RELEASE IDs). Thus assertions removed = 0; skip/xfail added = 0; tests renamed = 0; behavior expectations changed = 0. Full behavioral execution is separately recorded in RESULT; ID coverage alone is not claimed as behavioral proof.

## Stability Charter cause and correction

The former awk range starts and ends on `## [Unreleased]` itself. The existing `### Added` entry was never included. CHANGELOG already documents the public additions and is unchanged.

Only the SECTION assignment in `.github/workflows/test-fcop.yml` changed:

```sh
SECTION=$(awk '/^## \[Unreleased\]$/ { capture=1; next } capture && /^## \[/ { exit } capture { print }' CHANGELOG.md | head -n 200)
```

The subsequent `^### (Added|Changed|Deprecated|Removed)` predicate, failure exits, job conditions and every other workflow line are unchanged. POSIX awk/grep were executed with three inputs (temporary pipe input, no committed fixtures):

| Input | Result |
|---|---|
| Actual `git show HEAD:CHANGELOG.md` bytes | PASS: current Added entry recognized |
| Unreleased section without qualifying third-level heading | Correctly rejected |
| Qualifying heading only in following version section | Correctly rejected |

## Local checkout caveat retained, not hidden

The machine's existing `core.autocrlf=true` checked out all twelve v4 Schema pairs with CRLF. The unchanged generator checks deterministic LF bytes, so the first complete library run in the execution tree returned **1189 passed / 1 failed** in 382.87s. The separate Schema/surface run returned **50 passed / 1 failed**. Both failures are `test_schema_parity_ids_offline_and_required_negative_matrix` at its generator subprocess, not protocol behavior failures.

Read-only byte comparisons proved each affected checkout file differs from its fixed Git blob solely by CRLF conversion; raw Git blobs are LF. Neither the generator nor Schema nor tests were changed to accommodate this environment.

A separate verification tree was created with `git -c core.autocrlf=false worktree add --detach D:/FCoP-wp4a2-lf-verification 7e2dcd3cc45f043c7981e7e5b79a78505ec109e8`. Only the same eight authorized edits were applied there. Its `git diff` is byte-identical to the execution tree's filtered diff. `python spec/schemas/v4/generate.py --check` then verified 12/12 pairs. No shared Git setting was changed, no original workspace was migrated, and the first failure is preserved here. Final local tests use this canonical-byte verification tree; native Windows CI still must pass independently.

## Scope and stop boundary

The content change is seven Conformance files, one workflow line and these two new reports. The following commit adds only the new WP4A.2 Manifest. Existing reports, failed runs and WP4A.1 delivery are preserved. No force-push, main change, release, WP4B work, or CodeFlowMu operation is authorized. Remote failure or missing final-HEAD checks means BLOCKED, never acceptance.
