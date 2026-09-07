# WP4C.3b delivery Manifest — FIXTURE + BLOCKER FACTS ONLY

## Status and authority

```yaml
WP4C_3B_FIXTURE_STATUS: COMPLETE
WP4C_3B_STATUS: BLOCKED
WP4C_3_STATUS: BLOCKED
AUTHORIZED_SCOPE: WP4C_3B_DIST_02_FIXTURE_ALIGNMENT_AND_WP4C_3_RESUME
TASKBOOK_COMMIT: 3a11498c0d4aff736628e781f34516950cb34be8
TASKBOOK_SHA256: 5c4cb2506a6d987dea705a2c5d1b28108b01a3d2b68cbf7b0047dbb8d3d4dbcb
TASKBOOK_BYTES: 13446
INPUT_HEAD: ec81dc5ed80ff2a4492fd0d1611aad234949bfb5
FIXTURE_COMMIT: 115751b4c24a1924062a81a21e0d655e8cb5fedc
CONTENT_COMMIT: 29ceaed54d63bbdff5057621b7dc0329535b1f98
MANIFEST_PARENT: 29ceaed54d63bbdff5057621b7dc0329535b1f98
REVIEW_BRANCH: review/fcop-4.0-wp4c.3b-development-fixture-and-rule-package
PR_BASE: taskbook/fcop-4.0-wp4c.3b-development-reference-fixture
BLOCKER: HISTORICAL_PUBLIC_METHOD_COUNT_NOT_SCOPED
DELIVERY_KIND: FIXTURE_AND_BLOCKER_FACTS_ONLY
IMPLEMENTATION_COMMITTED: false
IMPLEMENTATION_PUSHED: false
LOCAL_IMPLEMENTATION_FILES_PRESERVED: 31
LOCAL_WORKTREE_STATUS: DIRTY_PRESERVED
WP4C_3_RULE_PACKAGE_ACCEPTED: false
WP4C_4_STARTED: false
REQUESTED_GATE: NONE_BLOCKED
MAIN_MERGE_AUTHORIZED: false
RELEASE_AUTHORIZED: false
```

[Fixed taskbook](https://github.com/joinwell52-AI/FCoP/blob/3a11498c0d4aff736628e781f34516950cb34be8/taskbooks/fcop-4.0/WP4C.3b/01-DIST-02-Development-Reference-Fixture-and-WP4C.3-Resume-Taskbook-v1.0.zh.md) and [ADMIN authorization](https://github.com/joinwell52-AI/FCoP/pull/22#issuecomment-5568219764) were verified from GitHub. PRs #21 and #22 remain unchanged historical blockers.

## Exact sequential commits

1. Taskbook 3a11498c0d4aff736628e781f34516950cb34be8, direct parent ec81dc5ed80ff2a4492fd0d1611aad234949bfb5.
2. Fixture 115751b4c24a1924062a81a21e0d655e8cb5fedc, direct child of taskbook: only test_dist_01_06_manifest.py; preserves ID/parameters/assertions and adds explicit local four-reference inputs.
3. Content 29ceaed54d63bbdff5057621b7dc0329535b1f98, direct child of Fixture: exactly the five reports listed below; NO implementation files.
4. This Manifest's commit is a direct child of Content and changes only reviews/fcop-4.0/wp4c.3/MANIFEST.md. Its actual HEAD/hash is established externally by the GitHub readback receipt, not self-embedded.

No merge, amend, force push, source cherry-pick or failed implementation commit is part of this chain.

## Six content/fixture raw identities

SHA-256 below hashes Git Blob bytes at the Content commit. Final readback compares these against GitHub at the Manifest HEAD and a fresh LF checkout. Manifest itself is the seventh changed file, hashed externally to avoid self-reference.

| Exact delivered path | Bytes | Raw SHA-256 |
| --- | ---: | --- |
| reports/FCOP-4.0-WP4C.3-CLAUSE-AND-ARTIFACT-MAPPING.md | 9925 | 7c28b4973525f2ea0e76639446dac7cb549224a56f70d4908de86490c0abfd7f |
| reports/FCOP-4.0-WP4C.3-CONFORMANCE-RESULT.md | 18861 | 58bc50ac03bcd9065312673e32b17db1310c3fb2755278ef4d641e7de0987a67 |
| reports/FCOP-4.0-WP4C.3-IMPLEMENTATION-PLAN.md | 14349 | 14e91d74e13eed7f6435945d689f4747528d7c94be4f47be09b0f7a2f220380f |
| reports/FCOP-4.0-WP4C.3-RESULT.md | 17312 | ca5e14fd8e8231264e4cbce3ba4466983c51fea092e17f9a5148eb754666b82f |
| reports/FCOP-4.0-WP4C.3B-DIST-02-FIXTURE-ALIGNMENT.md | 4669 | 82b2b41a33744afc5290e9cc6ba22bf47b193aef51991aa386190de8eb16ff64 |
| tests/conformance/rule_distribution_v4/test_dist_01_06_manifest.py | 10075 | dafac52d52a9c8568dd9d360b58cbba6676446cf62b3a498701a19cbb0697d78 |

The actual taskbook-to-final diff is exactly these six paths plus this Manifest. The inherited WP4C.3a audit-scope report and prior audit test corrections remain in the parent history, not modified or counted as new delivery files.

## Local implementation evidence — not remote capability claims

- Precise target run: 56/56 passed; full suite independently confirms 56 target, 33 Meta, 1 control passes.
- Full distribution: 99 passed / 77 failed. Future 86 nodes are 77 deferred reds plus 9 explained zero-write negative-preflight overlaps; reports enumerate all 86.
- Core: 119 passed. MCP: 134 passed. Full FCoP: 1296 passed / 1 failed; all 41 new unit nodes passed.
- Blocker: tests/test_fcop/test_v4_creation.py:839 computes the historical legacy set from all policies minus ten known v4-only methods. Adding the authorized rule_distribution yields 39 instead of 38. The sole set delta is that method. The existing test is outside this task's write set and has not been changed.
- Isolated blocker rerun: 1 failed, 1.48 s. Final Meta/control rerun: 34 passed, 13.26 s.
- Existing Project methods have identical ASTs; the candidate snapshot adds only rule_distribution. Legacy data bytes are 14/14 unchanged. Candidate package is 18 Markdown + 1 Manifest, 73 unique owners, eleven fields/record; wheel/sdist data inclusion is 19/19 (not WP4C.6 acceptance).
- The candidate implementation, package, new units, snapshot, package-data and CHANGELOG edits remain in D:/FCoP-wp4c3b-development-fixture-and-rule-package. The RESULT report lists all 31 local raw hashes. None is in this remote diff.
- No production or existing test change was made after the blocker was confirmed. No Host, MCP, CodeFlowMu, main, version or release mutation occurred.

The fixture-only committed tree still has no distribution public entry. Never use this report-only branch's CI, package file claims or local test counts as implementation acceptance.

## Remote verification procedure and stop

After push, refetch the exact review branch; require its HEAD to equal this Manifest commit. Validate every direct parent and exact per-commit file set. Read all seven changed files through GitHub's fixed-ref raw Contents API and compare complete bytes with local Git Blobs and a newly created LF checkout. Recheck local main and remote main against the observed baselines; preserve the dirty implementation worktree. Record final HEAD, 7/7 hashes, Draft PR URL and actual CI state in the external PR receipt.

Workflow filters target main/feat pushes and PRs to main; the prescribed review/base pair is outside them. If no run exists, report NOT_TRIGGERED_BRANCH_FILTER, not PASS. Do not change PR base or trigger release to manufacture green evidence.

Execution stops after factual delivery. ADMIN may authorize a narrow historical-test exclusion alignment, preserving the assertion of 38 original methods and all other compatibility checks. No such correction, WP4C.4 advance or Gate signature is performed here.
