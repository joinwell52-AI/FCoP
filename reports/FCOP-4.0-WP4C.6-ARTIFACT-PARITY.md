# WP4C.6 artifact parity

Status: BLOCKED by the later historical ordinary-test absence assertion. Candidate artifact checks passed as recorded below; later install/native verification was not performed. No publication or Gate claim.

## Separate identities

The public `build_artifacts` action exports canonical rule data, not an install of the FCoP Toolkit. Each archive has exactly 19 canonical payload members below `fcop/rules/_data/v4/`: the original Manifest and all eighteen module/language files. The payload is read through the existing complete loader and retained as raw bytes, without serialization, newline conversion or implicit source discovery.

The data-only format carrier is named `fcop-rule-data`, with content-addressed local version `0+<manifest-sha256>`; this is private archive metadata, not a new FCoP project/release version or a change to Manifest.package_version. Wheel metadata includes METADATA/WHEEL/RECORD; the sdist contains PKG-INFO and a fixed, owned hatchling build declaration using the already-established build backend. Export never imports/runs that backend or reads caller/user build configuration. These metadata members are outside the 19 canonical payload members. No runtime code, dependency, workspace identity, Host output or receipt is exported.

Standard-library archive construction is in-memory. Member order, permissions, ownership and timestamps are fixed; wheel stores bytes without compression; sdist uses gzip with an empty filename and mtime zero. Format metadata includes no wall clock, host platform, absolute machine path or randomness. Existing output files/nonempty directories and unsafe/overlapping destinations reject before any write; creation is exclusive. A later I/O error is a failure, with partial output preserved for inspection, not a false group-atomic success claim.

## Observed candidate evidence

Frozen DIST-27: **2/2 passed**, within the combined 20-target run. JUnit: `C:/Users/Administrator/AppData/Local/Temp/fcop-wp4c6-target-01.xml`, SHA-256 `dbbfbb5f3e7a7ca7d630a143b1247f9baaa742a28691b2f9e24062cba87d1529`.

The first ordinary-unit run passed 59/59. Its real export test built wheel and sdist twice from the actual bundled package, into separate explicit output directories. Both repetitions had identical archive hashes and exact canonical member bytes; the caller workspace was unchanged. Source Manifest SHA-256: `7efb1ba14df4d1ffbe164b8ec85dbf4316e7da4c0f367f3a506c78e4e29862d4`.

| Export format | Archive bytes | Observed SHA-256 |
| --- | ---: | --- |
| wheel | 57438 | 152716140d60e435a040ba6e524deda46a8b80407521cb1d1015e87afbe003f2 |
| sdist | 18616 | ffc8ce654bde1049f69c87a466272f43038bc7772f5cc4d6117c8a2f998c4f87 |

These observations are from `D:/fcop-wp4c6-unit-01/test_exports_exact_bytes_repea0/{first,second}` on Windows Python 3.12. They prove same-platform repetition, not yet cross-platform whole-archive hash identity. Canonical byte identity must also pass native CI on Linux/macOS/Windows.

## Exact canonical input inventory

Read from the unchanged source package. The successful public export test compared every corresponding archive member with these actual source bytes; these are not installed/native-CI claims.

| Relative canonical member | Bytes | SHA-256 |
| --- | ---: | --- |
| authorization.en.md | 2128 | 96c1c18bab3a879b51a1e2d0041f1f08eeae685185ad9489f13ed0a999f9a00b |
| authorization.zh.md | 2033 | 13b82fdeb7c577a68a70d94303bf090eac42ce44c137c1a166b23f7014c1b854 |
| compatibility.en.md | 3521 | a65385a3a2e68d043c65f9b8c34c6ac311bb7f9b2ea1e9f4c162886f858a64d8 |
| compatibility.zh.md | 3024 | d6ce267c8216a2d6df2e5e601f4d237d941778a36687eae1d310616f6170585e |
| convergence.en.md | 2283 | ec3cf38b6dba4d3eb8447cc7cd25e947c06abed228c37c9d651f873662edc70e |
| convergence.zh.md | 2114 | 2b5c2a52c33bc38e8c3c85fdd75d5de3c837cc483a29941ec02a61a059c1701a |
| envelopes.en.md | 1743 | 0405885cbe3fe791c0e1a6c76da004d093d58cd55159ffeb3ca8c89e4ec045a3 |
| envelopes.zh.md | 1672 | 0a69c9196e95185cf9e98b71af8c564be5797e26a71c5a9b7dc32d0735a08fef |
| idempotency.en.md | 1720 | 1b100010d36342e6d98e9031429b3e11aad5657dfa953031e43bc4c99772a16a |
| idempotency.zh.md | 1591 | 51c53931e02b1f39950f4a2f16b5e8e9a5f9d10b77f5ea1ad6b07c3e96385f08 |
| lifecycle.en.md | 3041 | b6356c078ab00b893379f0b4f558616444ef4a4aa0e17432460719a9be362b2b |
| lifecycle.zh.md | 2787 | 26b338914cffe2ea076f0e88133fc69617c91ecb149b3e40217baeef708cffef |
| manifest.json | 11221 | 7efb1ba14df4d1ffbe164b8ec85dbf4316e7da4c0f367f3a506c78e4e29862d4 |
| recovery.en.md | 3534 | aad4861efa59df69742c4bf577d57a553cbb170f6f92d61f6df74ec3ec503908 |
| recovery.zh.md | 3099 | b19226071498f6414e11379b9d67cee36e4a79d65510fffefd14a021cd829000 |
| relations.en.md | 1106 | 1b706c4ff76efb6edad40ab7985a0693eb9466da483d7024eb1f29668e022789 |
| relations.zh.md | 1057 | fa51c77a568dae7f7cf41242b612ae2b2963075004aaebef533334a0466d3d42 |
| workspace.en.md | 1920 | 06d4a9604fbab50ade36369f8f1d2950f099a241d659613cc78f1dd7e93555b3 |
| workspace.zh.md | 1723 | 617009dc95cf4bedd252491334f45cf61fa1fe8ccf935f2127e2a1da9a49e30b |

## Remaining verification

Normal FCoP source wheel/sdist, clean-install 19-file parity and installed public export are separately checked by `tests/test_fcop/rule_distribution_artifact_probe.py`. The task requires these after full regression; they are not yet recorded as passed. Final native CI and remote delivery are also pending. Do not infer upload, installation, adoption or Runtime consumption from the export return value.
