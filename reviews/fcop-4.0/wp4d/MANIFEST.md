# WP4D Manifest — BLOCKED after authorized audit-guard resumption

## Current receipt

```yaml
WP4D_STATUS: BLOCKED
AUTHORIZED_SCOPE: WP4D_AUDIT_GUARD_ONLY_AND_WP4D_RESUME
BLOCKER: RC_TWINE_6_2_METADATA_2_5_REJECTION
BASE_COMMIT: 167c5fd4ca4c9603c392bae3a4a055963e7b7ed6
TASKBOOK_COMMIT: cbdc60a92a02b9e2eb0c1c6e2e93f74c335407f9
TASKBOOK_SHA256: bfc93f595800efe5185588ff92b612c9ca66e1622118e76c805d5fd908a1e290
ERRATUM_COMMIT: 22db1377163bb0b1e74c4b94fa1f594b3e762a9d
ERRATUM_SHA256: 0e8926c282516dd10e2c1506243ccf33ab7798a8cd0744bcbccf078d5f344767
ERRATUM_BYTES: 5642
RESUME_BASE: 893e5c55f9f7ea433c6c518c76534218a4cf9570
AUDIT_GUARD_FIX_COMMIT: fad3a2d2cdcee490f8a86ae3d1254439089d5427
CONTENT_COMMIT: dd8138684006432c6bb62c952909a59cda20adaf
EVIDENCE_COMMIT: b4edae38f070c9c65ffa92a9c8b287b60f188f34
MANIFEST_COMMIT: SELF
MANIFEST_PARENT: b4edae38f070c9c65ffa92a9c8b287b60f188f34
TARGET_FCOP: 4.0.0rc1
TARGET_FCOP_MCP: 4.0.0rc1
OLD_AUDIT_BLOCKER: RESOLVED
AUDIT_GUARD: 1/1
AUDIT_UNEXPECTED_SKIP: 0
AUDIT_TEST_ID_FIXTURE_ASSERTION: PRESERVED
NATIVE_FULL_REGRESSION: 1924/1924
UBUNTU_CONTENT_FULL_REGRESSION: 1924/1924
FULL_FAILURE_ERROR_SKIP: 0/0/0
NATIVE_DOC_AND_IDENTITY: 25/25
SOURCE_PUBLIC_CLIENTS: 2/2
SOURCE_MCP_SURFACE: 46/12/4
CONTENT_EXISTING_CI: 27/27
CONTENT_WINDOWS_CI: 8/8
CONTENT_PR_ONLY_JOBS: 2_NOT_APPLICABLE
RC_BUILD: FAILED
RC_REPRODUCIBILITY: NOT_RUN
RC_CONSUMER_MATRIX: NOT_RUN_0_OF_12_VALIDATED
INSTALLED_ADOPTION: NOT_RUN
INSTALLED_LEGACY_COMPATIBILITY: NOT_RUN
CODEFLOWMU_SHADOW: NOT_RUN
FINAL_MANIFEST_CI: NOT_CLAIMED_GREEN
CANONICAL_FILES: 19/19
AUTHORITATIVE_BYTES: 21/21
FROZEN_CORE_CONFORMANCE_TREE: 24ab264c6bca9a3183ee270becb552f22a4c4f9e
FROZEN_DISTRIBUTION_CONFORMANCE_TREE: 4f99c7261b63b6db81c500604a231defaca9f14b
CONTENT_EVIDENCE_REMOTE_READBACK: 48/48
CONTENT_EVIDENCE_READBACK_HEAD: b4edae38f070c9c65ffa92a9c8b287b60f188f34
CONTENT_EVIDENCE_READBACK_UTC: 2026-09-09T14:45:46.575619+00:00
DELIVERY_FILES_INCLUDING_MANIFEST: 49
FINAL_REMOTE_READBACK_RECEIPT: PR_31_COMMENT_AFTER_PUSH
DRAFT_PR: 31
PR_BASE: task/fcop-4.0-wp4d-rc-candidate
PR_HEAD: feat/fcop-4.0-wp4d-rc-candidate
MAIN_MERGE_AUTHORIZED: false
TAG_AUTHORIZED: false
RC_PUBLISH_AUTHORIZED: false
STABLE_RELEASE_AUTHORIZED: false
PYPI_PUBLISH_AUTHORIZED: false
GITHUB_RELEASE_AUTHORIZED: false
MCP_REGISTRY_PUBLISH_AUTHORIZED: false
ZENODO_PUBLISH_AUTHORIZED: false
CODEFLOWMU_WRITE_AUTHORIZED: false
REQUESTED_GATE: NONE
```

## Stop reason and evidence boundary

The ADMIN-authorized guard correction now compares (major, minor) against (1, 2),
so 4.0.0rc1 no longer skips the existing audit assertion. The test ID, fixture,
binding and original final assertion are preserved. Six reports retain the old
BLOCKED reports verbatim below explicitly marked historical sections; the old
skip JUnit and [old Manifest](https://github.com/joinwell52-AI/FCoP/blob/893e5c55f9f7ea433c6c518c76534218a4cf9570/reviews/fcop-4.0/wp4d/MANIFEST.md)
remain historical evidence, not the current result.

The executor selected twine==6.2.0 in the newly added RC workflow. Its metadata
validation overrides the supported metadata versions through 2.4 and rejects
Metadata-Version 2.5 emitted by the pinned build stack. The exact first failure is
`InvalidDistribution: Invalid distribution metadata: '2.5' is not a valid metadata version`.
This is an executor tooling-pin defect, not a frozen Core/Schema failure or an
ADMIN taskbook error.

Original taskbook section 13.2 requires BLOCKED after an applicable CI failure.
No candidate content was changed after that failure. Only failure evidence,
reports and this Manifest were added. Twine 7.0.0 was inspected read-only as a
possible future pin, not installed or validated as a fix. Request ADMIN's
targeted tooling-pin resumption decision; do not request FCOP_4_RC_ACCEPTED.

## Fixed content CI

All following runs are tied to CONTENT_COMMIT, not SELF:

| Workflow | Run | Result |
|---|---|---|
| Core | [34363703057](https://github.com/joinwell52-AI/FCoP/actions/runs/34363703057) | 14 applicable jobs passed |
| MCP | [34363702991](https://github.com/joinwell52-AI/FCoP/actions/runs/34363702991) | 13 applicable jobs passed |
| RC candidate | [34363703047](https://github.com/joinwell52-AI/FCoP/actions/runs/34363703047) | Failed at Twine check; source job passed |

The existing Windows jobs passed 8/8. Two existing PR-only jobs were not
applicable to the push event and were not counted as passing. The RC consumer
dependency was skipped after its build failed: its 12 intended matrix cells
were NOT_RUN, not exempt and not passing. Ubuntu source full regression passed
1924/1924; native Windows full regression passed 1924/1924. Source-only public
Python and real stdio MCP samples passed, including process reopen, but do not
substitute for installed-artifact verification. Final Manifest HEAD CI is not
claimed green and cannot inherit RC acceptance from any earlier run.

## Candidate artifact identity — not delivered as validated artifacts

| Expected artifact | First build | Delivered candidate SHA-256 |
|---|---|---|
| fcop-4.0.0rc1-py3-none-any.whl | Built; validation failed | UNVERIFIED_NOT_UPLOADED |
| fcop-4.0.0rc1.tar.gz | Built; validation not accepted | UNVERIFIED_NOT_UPLOADED |
| fcop_mcp-4.0.0rc1-py3-none-any.whl | Built; validation not accepted | UNVERIFIED_NOT_UPLOADED |
| fcop_mcp-4.0.0rc1.tar.gz | Built; validation not accepted | UNVERIFIED_NOT_UPLOADED |

The second build, 4/4 reproducibility, canonical candidate hash manifest, wheel/
sdist installation, 12 consumer combinations and this stage's CodeFlowMu shadow
were not completed. Log artifact digests are not candidate artifact digests.
Full commands, timestamps, JUnit totals and log transformations are in
[RESULT](../../../../reports/FCOP-4.0-WP4D-RESULT.md); the five companion reports
appear in the hash table below.

## Additive commit chain

```text
167c5fd4ca4c9603c392bae3a4a055963e7b7ed6 accepted WP4C.6 content
 -> cbdc60a92a02b9e2eb0c1c6e2e93f74c335407f9 original WP4D taskbook
 -> f5a07a1c56dfc2a4bcd8bd258cd8db5d50b080d4 initial identity content
 -> 4160fc5d216f784bee6b35902b507fff8e0ba6f6 authorized-file LF correction
 -> 112a69b2fd9a3cdfdf3e72b7ea1e5ca9de208c07 original BLOCKED evidence
 -> 893e5c55f9f7ea433c6c518c76534218a4cf9570 original Manifest
 -> fad3a2d2cdcee490f8a86ae3d1254439089d5427 authorized audit guard only
 -> dd8138684006432c6bb62c952909a59cda20adaf candidate content
 -> b4edae38f070c9c65ffa92a9c8b287b60f188f34 six reports + eleven evidence files
 -> SELF Manifest only
```

Erratum 22db1377 is a fixed authority child of the original taskbook. It is not
merged into the implementation parent chain: its explicit RESUME_BASE is used.
No force push, main merge, tag, publication, workspace migration or CodeFlowMu
write was performed. The source scope guard preserves frozen Conformance,
19 canonical distribution files and 21 authoritative byte sequences.

## Delivery hashes

The following 48 files were individually re-read from GitHub Git Blob API at
EVIDENCE_COMMIT and byte-compared to their local committed blobs; every SHA-256
matched. Taskbook authority is listed separately above, not counted as a newly
delivered implementation file. SELF changes only this Manifest, preserving all
48 files. A final GitHub readback of all 49 files, parent chain and this
Manifest's own SHA-256 is recorded in PR #31 after pushing SELF, avoiding a
self-referential Manifest hash.

| File | Bytes | SHA-256 |
|---|---:|---|
| .github/workflows/rc-candidate.yml | 4883 | 3ebd90df68f4fe389765366effc08b64e6b851b20efaf7700c426f6b6ca4e854 |
| CHANGELOG.md | 132901 | 08d02ddc0509b723b51c58003fe11bf7a8cd45b25d64a57b1188b37fd2986f12 |
| docs/fcop-4.0/rc-candidate-boundary.md | 1469 | 8cf4906f96fc7b74096a77bba6b2bd4355e8ae72eb4d7fa64747ce514d3e06bb |
| docs/releases/4.0.0rc1.md | 1421 | fd4e62bc39d89c17701f6781bcffbf9b50a95e750689231053185c9563a5eef9 |
| examples/v4/third-party/mcp-only/README.md | 1615 | 83c82a93afee5da73c639bc8542a8b26a0016d7f66e142001c720e5cff8f2c8d |
| examples/v4/third-party/mcp-only/client.py | 9547 | 3675a4ab5c8351352fae27fd1a6353c389f8d3faa69be896e2f5a458a4d3d3f9 |
| examples/v4/third-party/mcp-only/server.py | 1033 | b566e175e853c97cb2a28c34ea9e9cf27d87c965821a3455c21eebd0d78687fa |
| examples/v4/third-party/python-only/README.md | 1707 | 94fe1a0a05808d5265e9646bed6c8b8c6c27c20a0ae49d2e58fd0234f2af957a |
| examples/v4/third-party/python-only/app.py | 12980 | c458bb0a4495b26791adfff10f82a853844ccddd9983b9cd0231ea3170b55902 |
| fcop-README.pypi.md | 2323 | 019dd8c11420e7d9b4e301dacdac42e45246169543bbae6fa785cc7e8b3dbf64 |
| mcp/README.md | 15929 | 2fa393329148df9079a35d17de345b8d43f653fc5d535eb67aa261b64eff57a8 |
| mcp/pyproject.toml | 4861 | 86628c2f21270758a51abac4fc375673d2c6a0c4c4806cf141fa270babff85c8 |
| mcp/src/fcop_mcp/_version.py | 610 | 310a8df396e097eeb5d3d8a0c83e3e2bc8803539ea94f7ecad7efad070a68339 |
| mcp/src/fcop_mcp/routing.py | 3760 | 6f054a99e2b2807b813d0e43e644e8b950a2f63c2d0159d519c6c89bb35fcb8b |
| pyproject.toml | 6077 | c9faa4f794b30ed52fdfc7093e0f0b30f7d8965ec8c8139c94f04eb732c346dc |
| reports/FCOP-4.0-WP4D-ARTIFACT-REPRODUCIBILITY.md | 6922 | 092fa24cc299ef81d0388dbfbdcdaafdbd0629f7b7093a610131c5fd43c78f49 |
| reports/FCOP-4.0-WP4D-CI-AND-RELEASE-READINESS.md | 7966 | 632b1f16e13879359eaaa598e2295b451e2eaed4539ab6745a6d44091789116f |
| reports/FCOP-4.0-WP4D-RC-IDENTITY-AND-VERSION.md | 7332 | 2d06437864803cd037a953f37b5d941fdf0acc1e892ebf2852b4cdd45ff9ff9c |
| reports/FCOP-4.0-WP4D-RESILIENCE-AND-COMPATIBILITY.md | 9719 | f1238a0830d2526448ba3d7219c7968068760e4aac485df97201f70c73a448d0 |
| reports/FCOP-4.0-WP4D-RESULT.md | 17432 | 29c329cb5c048ee76be8014d4beb636c98899e8133eebd436f61c3833e1a1f24 |
| reports/FCOP-4.0-WP4D-THIRD-PARTY-ADOPTION.md | 6752 | 55584c18082cfdfcebac187eb8ad58f64092e5a472b334d2c636f30e736e54d3 |
| scripts/fcop_rc_candidate_check.py | 3243 | 0a284ca78f5e36d46bbd73ef2113186d90194917a31c33a12a29818b4c8b144c |
| scripts/wp4d_build.py | 6643 | 6468447a61ffbf6bf75342c57dee3c395b25287de4e0c2eeb78aa24b1a347dd6 |
| scripts/wp4d_consume.py | 9066 | 6965a8c5878adf744bcacd6c9dfb451e3dca59159c1cf8e5059015859774ad72 |
| scripts/wp4d_legacy.py | 2191 | 4d3c824b87b19821a56e9579ca035af083ddf5277fb6c95d333abab227d579d1 |
| scripts/wp4d_shadow.py | 4569 | 8fd9ffebb6f1d69a60d44939bc0fc9f10ce3d1b4af9f5e627087a93642f8f0b6 |
| scripts/wp4d_source.py | 1193 | e2ad8fe4d54a6539b40b134fd15e71347274299bdc4280c85e91d7f40aac404b |
| scripts/wp4d_verify_scope.py | 3830 | 79a1f158a6d983f075145bdf4f696c5769bea26276d347cd625be7eb63079217 |
| src/fcop/_version.py | 564 | 14ffc70e19c78e318a2b65b2331dd21ccd3e84913493b1dca5a64079a6b0f3b9 |
| tests/rc/evidence/wp4d/baseline-1912.xml | 453008 | 54c07dd75b3208ee41bc51d2b0e1bf7ff4d6cadda0977042ad8ffbf3ccc48f33 |
| tests/rc/evidence/wp4d/content-ci-snapshot.json | 95357 | 51f1bd1cb6ee817530dfa8eb1e0f85c6c284a43be6d75e1f62c77cfb33deb478 |
| tests/rc/evidence/wp4d/identity-14.xml | 2293 | 4cfa47c3bdff3f4b7700872a1ed8ae2b51a5b4c731b1942ced3a425352b2a052 |
| tests/rc/evidence/wp4d/native-source-mcp.log | 276 | 6bc9c14ae833862c97a897050b4c1bca6b34f0e0d26ecba061faaf5b769b5a5d |
| tests/rc/evidence/wp4d/native-source-python.log | 249 | a874564d1776a3f1af5b37e094c3eccaf07f9f5b2de56d903e0cd90760f89a35 |
| tests/rc/evidence/wp4d/rc-audit-guard.xml | 596 | 6c03b6d5710cc90c1275b97d18e9b683f25bfff88c0c4777a9ca0af22f02934b |
| tests/rc/evidence/wp4d/rc-build-job.log | 43060 | 791dbf0506aaf6e6af5b6b155d040ff0be94182adce7a254524da019e6360893 |
| tests/rc/evidence/wp4d/rc-build-metadata-failure.log | 1634 | 8b9797bec3145685ed2c2589aa178f01c148f19529cd0dec586a82416c0d1e7d |
| tests/rc/evidence/wp4d/resume-audit-1.xml | 363 | 2a9c6a64553153a53f6f69e74be2062a41a57cef31a287fdec1a15329bafe3fd |
| tests/rc/evidence/wp4d/resume-doc-identity-25.xml | 4031 | 3049719aca165a1ab073893a4c8de366b1ddf092bc876d819b9e43e8b27ff323 |
| tests/rc/evidence/wp4d/resume-full-1924.xml | 454799 | d6b39e5a35e52bc0d2d03dd32206cbb7693aaeba0cdd9134d7f7a19ce0602474 |
| tests/rc/evidence/wp4d/resume-identity-14.xml | 2293 | 1e4633939df9206c6edeb9504aae94eb57dc88ec3bcc70acf91f4988cdd44d9d |
| tests/rc/evidence/wp4d/toolchain-diagnosis.json | 2105 | df2ff21f27f27c6343306ea90037a5e8f2606f7f3938896e0e6f55eab48f4f19 |
| tests/rc/evidence/wp4d/ubuntu-content-full-1924.xml | 454732 | 023552fc2549a3c340064a2e215bd898bbf0b3f11ca0304ed23e86bc9822b172 |
| tests/rc/installed_identity.py | 1109 | 6417053c91d55151b6c634fa6254c4e761d4076632141bcd5d7de81454cf2e03 |
| tests/rc/legacy_fixture.py | 3747 | 2971c5311994960e248d766054e8bc74f0c63aeed032bf80638f7f00c405b93c |
| tests/test_fcop/test_audit.py | 12271 | c5ee2802c01085ec6706aa99eec83b510e8a2871d489b0aed8e3ebeedc205c02 |
| tests/test_fcop/test_pyproject_pins.py | 1283 | 45cafdb7f125355d66cb503a3248c0b255e8826343e44894f98d4d1c3462cfc3 |
| tests/test_fcop/test_wp4d_rc_identity.py | 1586 | a5876542335a04a05d7ed315cfd239e14bf58986e90bf5bca479cc2b0a7473f8 |
