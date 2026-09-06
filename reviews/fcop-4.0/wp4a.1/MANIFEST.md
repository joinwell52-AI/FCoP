# WP4A.1 fixed delivery Manifest

## Identity

```yaml
AUTHORIZED_SCOPE: WP4A_1_ONLY
RESUMED_SCOPE: FULL_WP4A
TASKBOOK_COMMIT: 6ddf6a35235c6aedff6807e5e7aba3f7d515e2ff
TASKBOOK_SHA256: 7fa10b9825a2b67c9c15032612d543045bef0b1d9ffc18e11dab96a16635e13b
PARENT_COMMIT: 6ddf6a35235c6aedff6807e5e7aba3f7d515e2ff
CONTENT_COMMIT: c4809267fafabe303b7e6d7c8a3d1db3edfb9dc9
MANIFEST_COMMIT: SELF
HEAD: SELF
BRANCH: review/fcop-4.0-wp4a.1-machine-contract
CONTENT_FILES: 45
MANIFEST_FILES: 2
TOTAL_CHANGED_FILES: 47
BLOCKER_LOCAL_COMMIT_IN_PARENT_CHAIN: false
LOCAL_TESTS: 1309/1309
MCP_TESTS: 80/80
SCHEMA_BINDING_TESTS: 10/10
V4_SCHEMA_PAIRS: 12/12
GITHUB_CI_AT_MANIFEST_HEAD: PENDING_AT_MANIFEST_CREATION
REQUESTED_GATE: NONE_UNTIL_REMOTE_CI_PASS
GATE_SELF_SIGNED: false
```

The Manifest commit has exactly one parent: Content Commit, whose parent is the fixed taskbook commit. No local-only blocker commit was joined. SHA-256 below refers to exact UTF-8/LF Git blob bytes. SELF avoids an impossible self-referential checksum; the terminal remote-read receipt supplies this Manifest's own hash and immutable HEAD. The original WP4A index is in the same Manifest-only commit and is hashed below.

## SHA-256 inventory

| File | SHA-256 |
|---|---|
| docs/fcop-4.0/schema-and-python-quickstart.md | 9cbcf43ae527f7eb7ac3e24bc7a4546b33bdb2768d71aeb9cd44c97145937277 |
| docs/fcop-4.0/schema-and-python-quickstart.zh.md | 7d070a4d24cb306cbcc7b60792b7af593a3d3aabbbac51d8bed2576c17980fb8 |
| examples/v4/application.py | af5b7c6d4de3b3c47fea474870cb59d4ba4becd3b1931c9d67be9a4a71747b8e |
| examples/v4/artifact_smoke.py | 1cf05fb9858cbcf08f9e0cb7d35ab523adf8acca81e41bbc3b8e5dcfc5968cb1 |
| examples/v4/offline_guard/sitecustomize.py | f2b227a05aa773a36a016a9621918a2f34a7c73830521fd316adc49c974b4989 |
| pyproject.toml | af25fbd6622126dcba1e9339c4fb8a3566111a048af32027dd50927db1fe1403 |
| reports/FCOP-4.0-WP4A-MINIMAL-APPLICATION-PROOF.md | c4c9fe8c48fdd03e295a25d0e06aea7a036a572b801328eb7608d55cd200599f |
| reports/FCOP-4.0-WP4A-PACKAGE-PROOF.md | c564e6b14544f175921703e1febbbf53c339c9902957b4a331b352fd0f78aece |
| reports/FCOP-4.0-WP4A-RESULT.md | 118a687d87daa28ccd07cc7dfbd8142d96c339812bc1cd5f0fc8c44ddeb49efa |
| reports/FCOP-4.0-WP4A-SCHEMA-CONTRACT-UNDERDETERMINED.md | 3a9c42d321caf2d272bf4456a74517d8b2582ae81697718a4455c0177e4ff80e |
| reports/FCOP-4.0-WP4A-SCHEMA-MAPPING.md | 10a76bc7cbdcf4583a6433317c200f494f3702c3497bdea11a5dda0c7796ff70 |
| reports/FCOP-4.0-WP4A.1-SCHEMA-BINDING.md | 6c73ece7a0c346f37015707a4232ffbc1a3d3113566b1578734a07eadb3261bc |
| spec/schemas/v4/README.md | 32d2c3ca76c79925ab03828f5f612f02549416a78979f7f88a33f2a6fc0724c2 |
| spec/schemas/v4/authorization-binding.schema.json | d58987e4c353adcae73bac26136db8a1f2ce8c4b5694e78cb21e2e97bcd43b86 |
| spec/schemas/v4/create-operation.schema.json | eab9c43684fb6a8999d3d0c643a4402f4296a2a21103d4a3e5f318c665494a01 |
| spec/schemas/v4/create-request-canonical.schema.json | 2fdad6ed19cb53728521353a297aabaf02a599f6f276661564406e68bc267197 |
| spec/schemas/v4/family-canonical.schema.json | 6f31f5e1784b08706b237e75cb4cf496b0d9847b809683810f86d422acc110eb |
| spec/schemas/v4/generate.py | 29bcefb3ceb25fd3b1ae6af57ffde9a1f810839b66e2776eede94f941f1e3192 |
| spec/schemas/v4/issue.schema.json | 78830cc2c25f5a71f23e1e707c3801ec279ab51d0a7a8b8a6222b5a26d22c56b |
| spec/schemas/v4/lifecycle-receipt.schema.json | 41f38ff99672b1238c6d384499856c8c6af48bae0fffd74da93a56d4fcc495a2 |
| spec/schemas/v4/recovery-observation.schema.json | f8ef752dd58cc8716684919f9672112cb2282f8529fa5a6db151361d4c09dd99 |
| spec/schemas/v4/report.schema.json | 1a8de72da2870beca3a09af91aec48cf697d5a8c4d694b42f8d5cc0a001d19fc |
| spec/schemas/v4/review.schema.json | e07dbbbec4d100d6ab57db46057553896ebacbff55dd4567721408a33084f21a |
| spec/schemas/v4/task.schema.json | c3ec36ec5577fb07d05d69a7fc0f533594c6c4e5ed36376cc01092af4c69610f |
| spec/schemas/v4/transition.schema.json | b223a0dd5cbf634bbdd40b3364501522f8417c987bef97732c3c93786946e801 |
| spec/schemas/v4/workspace.schema.json | 775c2f5516d49f42fabf84a058fdf85298f4e9dcedc91d182a7e0678f2d0f0aa |
| src/fcop/_data/schemas/v4/authorization-binding.schema.json | d58987e4c353adcae73bac26136db8a1f2ce8c4b5694e78cb21e2e97bcd43b86 |
| src/fcop/_data/schemas/v4/create-operation.schema.json | eab9c43684fb6a8999d3d0c643a4402f4296a2a21103d4a3e5f318c665494a01 |
| src/fcop/_data/schemas/v4/create-request-canonical.schema.json | 2fdad6ed19cb53728521353a297aabaf02a599f6f276661564406e68bc267197 |
| src/fcop/_data/schemas/v4/family-canonical.schema.json | 6f31f5e1784b08706b237e75cb4cf496b0d9847b809683810f86d422acc110eb |
| src/fcop/_data/schemas/v4/issue.schema.json | 78830cc2c25f5a71f23e1e707c3801ec279ab51d0a7a8b8a6222b5a26d22c56b |
| src/fcop/_data/schemas/v4/lifecycle-receipt.schema.json | 41f38ff99672b1238c6d384499856c8c6af48bae0fffd74da93a56d4fcc495a2 |
| src/fcop/_data/schemas/v4/recovery-observation.schema.json | f8ef752dd58cc8716684919f9672112cb2282f8529fa5a6db151361d4c09dd99 |
| src/fcop/_data/schemas/v4/report.schema.json | 1a8de72da2870beca3a09af91aec48cf697d5a8c4d694b42f8d5cc0a001d19fc |
| src/fcop/_data/schemas/v4/review.schema.json | e07dbbbec4d100d6ab57db46057553896ebacbff55dd4567721408a33084f21a |
| src/fcop/_data/schemas/v4/task.schema.json | c3ec36ec5577fb07d05d69a7fc0f533594c6c4e5ed36376cc01092af4c69610f |
| src/fcop/_data/schemas/v4/transition.schema.json | b223a0dd5cbf634bbdd40b3364501522f8417c987bef97732c3c93786946e801 |
| src/fcop/_data/schemas/v4/workspace.schema.json | 775c2f5516d49f42fabf84a058fdf85298f4e9dcedc91d182a7e0678f2d0f0aa |
| src/fcop/v4/convergence.py | 1f784027f99aaba0698bc48d1cc8be83047ee2adb7a93932ef16d61cba3508dd |
| src/fcop/v4/creation.py | 0787abed6191a4798ea1c4470a8f9ab9fec3eb23b3329970d3ead0de5353d2f2 |
| src/fcop/v4/encoding.py | 8a442202037d5b1bb5e1fb8c5cbfeb1c57560fec6f7f0fa0fcb9613e593d94f5 |
| src/fcop/v4/receipts.py | 61ad9592b16e70bcea97bd1d739ff3f552f3f3bf4ee758b7b41975d07e424007 |
| src/fcop/v4/recovery.py | 58e37f36a50adc8cb2fc9f1cd0d38b3bdd5af55e343232c225532a794a2cf927 |
| src/fcop/v4/schema.py | 2454f55928aa3b589aefa01443b411558eaaea065f26ce53adfa025d5331976c |
| tests/test_fcop/test_v4_schema.py | 92171f144c9681daf7075e7eff8d4cf1c336e70f0fb18b8471da879fa11d1062 |
| reviews/fcop-4.0/wp4a/MANIFEST.md | a2476f9ae9426720e4058ba3838411f7369fb93de347b027b2524081c79d4e09 |
| reviews/fcop-4.0/wp4a.1/MANIFEST.md | SELF — hash in terminal remote-read receipt |

## CI observation procedure and stop condition

After pushing this fixed Manifest HEAD, refetch the review ref, compare remote HEAD, parent chain, and each GitHub blob SHA-256 with the local committed bytes. Create a Draft PR targeting main titled `[DO NOT MERGE][FCoP 4.0 WP4A.1] Machine contract`. No reviewer request, auto-merge, merge or release is authorized.

Wait for test-fcop, test-fcop-mcp and their package jobs associated with this exact HEAD. The local workflow-equivalent lint already identifies ten untouched frozen-Conformance errors; do not modify their files or workflow to bypass CI. Local success is not remote CI success. If CI is absent or not all green, stop BLOCKED and do not request WP4A_MACHINE_CONTRACT_ACCEPTED. Otherwise request that Gate, never sign it or enter WP4B.

RESULT and PACKAGE-PROOF preserve local commands, actual counts, final artifact hashes and limitations. GitHub checks are the post-Manifest evidence source, so no third evidence commit or mutation of this fixed HEAD is needed.
