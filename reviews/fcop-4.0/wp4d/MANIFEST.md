# WP4D Manifest — BLOCKED / unpublished candidate identity only

```yaml
wp4d_status: BLOCKED
authorized_scope: WP4D_ONLY
blocker: LEGACY_AUDIT_MINOR_ONLY_GUARD_SKIPS_RC
base_commit: 167c5fd4ca4c9603c392bae3a4a055963e7b7ed6
taskbook_commit: cbdc60a92a02b9e2eb0c1c6e2e93f74c335407f9
taskbook_sha256: bfc93f595800efe5185588ff92b612c9ca66e1622118e76c805d5fd908a1e290
initial_content_commit: f5a07a1c56dfc2a4bcd8bd258cd8db5d50b080d4
candidate_commit: 4160fc5d216f784bee6b35902b507fff8e0ba6f6
evidence_commit: 112a69b2fd9a3cdfdf3e72b7ea1e5ca9de208c07
manifest_commit: SELF
target_versions:
  fcop: 4.0.0rc1
  fcop-mcp: 4.0.0rc1
artifact_hashes:
  fcop-4.0.0rc1-py3-none-any.whl: NOT_GENERATED
  fcop-4.0.0rc1.tar.gz: NOT_GENERATED
  fcop_mcp-4.0.0rc1-py3-none-any.whl: NOT_GENERATED
  fcop_mcp-4.0.0rc1.tar.gz: NOT_GENERATED
artifact_reproducibility: NOT_RUN
baseline_regression_before_changes: 1912/1912
legacy_regression: NOT_RUN_FULL_ON_RC
candidate_existing_pin_tests: 2/2
candidate_targeted_old_audit: 0 passed / 0 failed / 1 skipped
wp4d_tests: 12/12
existing_ci_applicable: NOT_ACCEPTED_BLOCKED
windows_existing_ci: NOT_ACCEPTED_BLOCKED
rc_consumer_matrix: NOT_RUN
mcp_surface: NOT_REMEASURED_ON_INSTALLED_RC
parent_mcp_surface: 46/12/4
canonical_files: 19/19
frozen_bytes: 21/21
codeflowmu_shadow: NOT_RUN
main_merge_authorized: false
rc_publish_authorized: false
stable_release_authorized: false
pypi_publish_authorized: false
github_release_authorized: false
mcp_registry_publish_authorized: false
zenodo_publish_authorized: false
codeflowmu_write_authorized: false
requested_gate: NONE
draft_pr: 31
pr_base: task/fcop-4.0-wp4d-rc-candidate
pr_head: feat/fcop-4.0-wp4d-rc-candidate
content_evidence_remote_sha256: 18/18
content_evidence_readback_time: 2026-09-09T17:28:35.842206+08:00
```

## Stop reason

The unchanged historical test
`tests/test_fcop/test_audit.py::test_scan_outdated_role_docs_far_behind`
passed in the 1912-node baseline but skips with the required candidate version.
Its minor-only precondition sees 0 in 4.0.0rc1 and returns before the regression
assertion. The taskbook requires zero unexpected skips and does not authorize
changing this old test. No old test guard, assertion or production scanner was
changed. ADMIN must resolve that precise scope boundary before execution resumes.

The candidate identity/pin checks are not installation, reproducibility, adoption,
recovery, cross-platform or complete RC verification. The unexecuted checks above
are NOT_RUN, not successful zero-failure runs. Four artifact hashes do not exist.
No Gate is requested.

## Commit chain and scope

```text
167c5fd4ca4c9603c392bae3a4a055963e7b7ed6  accepted parent
  -> cbdc60a92a02b9e2eb0c1c6e2e93f74c335407f9  one-file taskbook
  -> f5a07a1c56dfc2a4bcd8bd258cd8db5d50b080d4  initial candidate identity
  -> 4160fc5d216f784bee6b35902b507fff8e0ba6f6  authorized-file LF correction
  -> 112a69b2fd9a3cdfdf3e72b7ea1e5ca9de208c07  six reports + three JUnit files only
  -> SELF  this Manifest only
```

The initial staging line-ending error and its additive correction are documented
in RESULT. History was not rewritten or force-pushed. The final net candidate
diff is nine authorized files; the compatibility module changes only the exact
package-pair constant. Frozen Core/Distribution Conformance, 21 authoritative
files, old audit test, main, public registry metadata and release workflow remain
unchanged. CodeFlowMu was not executed or written.

## Fixed remote delivery file hashes

Read from GitHub raw contents at evidence commit `112a69b2fd9a3cdfdf3e72b7ea1e5ca9de208c07`,
not inferred only from local files. Each byte sequence matched the local file.
The final Manifest HEAD must preserve these exact 18 files; the Manifest itself
is the nineteenth delivery file and is hashed separately in the final PR receipt
to avoid a self-referential hash. SELF resolves to the commit adding this file.

| File | Bytes | Remote SHA-256 |
|---|---:|---|
| docs/fcop-4.0/rc-candidate-boundary.md | 1469 | 8cf4906f96fc7b74096a77bba6b2bd4355e8ae72eb4d7fa64747ce514d3e06bb |
| mcp/pyproject.toml | 4861 | 86628c2f21270758a51abac4fc375673d2c6a0c4c4806cf141fa270babff85c8 |
| mcp/src/fcop_mcp/_version.py | 610 | 310a8df396e097eeb5d3d8a0c83e3e2bc8803539ea94f7ecad7efad070a68339 |
| mcp/src/fcop_mcp/routing.py | 3760 | 6f054a99e2b2807b813d0e43e644e8b950a2f63c2d0159d519c6c89bb35fcb8b |
| pyproject.toml | 6077 | c9faa4f794b30ed52fdfc7093e0f0b30f7d8965ec8c8139c94f04eb732c346dc |
| reports/FCOP-4.0-WP4D-ARTIFACT-REPRODUCIBILITY.md | 1873 | 0961adb69702af33f8a7805ff668211d3cb1afc218e99c24248790fa0ee33908 |
| reports/FCOP-4.0-WP4D-CI-AND-RELEASE-READINESS.md | 3409 | 8677a432e1de753f71b1955de176725702aace51664f836e7720173098f9df9c |
| reports/FCOP-4.0-WP4D-RC-IDENTITY-AND-VERSION.md | 3144 | 9a7469b71420e8bcf74ec9e0035073111f830ff69542bf366638edbfe16aa235 |
| reports/FCOP-4.0-WP4D-RESILIENCE-AND-COMPATIBILITY.md | 5212 | 7199a995cb1bd62e4b8fab771baa97ea3288265293ba87b3d2ed209b8dc0806d |
| reports/FCOP-4.0-WP4D-RESULT.md | 6436 | cac539041e7eb3d718eb9916928188c4b13d54d5b205dffe367644509985bef4 |
| reports/FCOP-4.0-WP4D-THIRD-PARTY-ADOPTION.md | 1814 | b40a12d643e3cc4a9d0bcf07b92909ddad4d1a712a795cbd5188543721a906bf |
| scripts/fcop_rc_candidate_check.py | 3243 | 0a284ca78f5e36d46bbd73ef2113186d90194917a31c33a12a29818b4c8b144c |
| src/fcop/_version.py | 564 | 14ffc70e19c78e318a2b65b2331dd21ccd3e84913493b1dca5a64079a6b0f3b9 |
| tests/rc/evidence/wp4d/baseline-1912.xml | 453008 | 54c07dd75b3208ee41bc51d2b0e1bf7ff4d6cadda0977042ad8ffbf3ccc48f33 |
| tests/rc/evidence/wp4d/identity-14.xml | 2293 | 4cfa47c3bdff3f4b7700872a1ed8ae2b51a5b4c731b1942ced3a425352b2a052 |
| tests/rc/evidence/wp4d/rc-audit-guard.xml | 596 | 6c03b6d5710cc90c1275b97d18e9b683f25bfff88c0c4777a9ca0af22f02934b |
| tests/test_fcop/test_pyproject_pins.py | 1283 | 45cafdb7f125355d66cb503a3248c0b255e8826343e44894f98d4d1c3462cfc3 |
| tests/test_fcop/test_wp4d_rc_identity.py | 1586 | a5876542335a04a05d7ed315cfd239e14bf58986e90bf5bca479cc2b0a7473f8 |

## Evidence and review

- [Result and reproducible commands](../../../../reports/FCOP-4.0-WP4D-RESULT.md)
- [Baseline JUnit: 1912 pass / 0 skip](../../../../tests/rc/evidence/wp4d/baseline-1912.xml)
- [Candidate identity JUnit: 14 pass](../../../../tests/rc/evidence/wp4d/identity-14.xml)
- [Real candidate guard JUnit: 1 skip](../../../../tests/rc/evidence/wp4d/rc-audit-guard.xml)
- [Draft PR #31](https://github.com/joinwell52-AI/FCoP/pull/31)

Report links and JUnit copies are pinned by this commit and the hashes above.
No release, tag, merge or public candidate distribution occurred. Final CI is
not claimed green; even if existing branch CI later turns green it cannot stand
in for the missing RC workflow and cannot waive the regression skip.
