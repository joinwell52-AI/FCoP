# CLI v1 final validation manifest

STATUS: FINAL_VALIDATION_PENDING
REQUESTED_ADMIN_GATE: NONE
AUTHORITY: CLI-V1 v4 plus fixed ADMIN release-identity amendment
TASKBOOK_COMMIT: 8bedfd3e132b7cca38e017ca518807332abb4bc2
TASKBOOK_SHA256: 923480c9a6c4ffa7211cb0032f5497ba4089bb97339fe203978359cd97254e3f
AMENDMENT_COMMIT: a72fef39d772104f5129b1b4ed1c6feeda62e31c
AMENDMENT_SHA256: c21c094dd616bc4d216b1d3c7f57d9703ea11c18b84ad3afa4ea096c780465f5
BASELINE_HEAD: a72fef39d772104f5129b1b4ed1c6feeda62e31c
CONTENT_COMMIT: 1e44c4ed4137288e096dab9af2653551de3e6154
SPEC_IDENTITY_COMMIT: 5c27e1bc90dce799aa7fa89e6cc717e01d47693e
BRANCH: codex/fcop-4.0.2-cli-v1
PR: https://github.com/joinwell52-AI/FCoP/pull/40
VERSION: fcop==4.0.2 / fcop-mcp==4.0.2
CODEFLOWMU_MODIFIED: false
MAIN_MERGED_AT_MANIFEST_CREATION: false
TAG_CREATED_AT_MANIFEST_CREATION: false
PYPI_PUBLISHED_AT_MANIFEST_CREATION: false

This manifest-only commit follows the content commit without rewriting history.
Its own HEAD/hash, remote readback and final HEAD local/CI results are recorded
in PR #40, avoiding a self-referential hash and any unearned PASS claim.
All applicable local/remote release gates must pass before merge/tag/publication.
Once they pass, the fixed ADMIN amendment authorizes continuous release without
another Gate. Tag-built artifacts, public no-cache installation and both PyPI
description comparisons are recorded in the final release receipt in that PR.

## Historical holds

The initial inline-prompt mismatch and subsequent stable-identity scope hold
were resolved by explicit ADMIN authorization. Their original evidence remains
in prior commits and BASELINE.md / TEST-RESULTS.md. The old blocked manifest at
7ec09f1c26c25d0c1273b2d2ab0c5bb79c35b969 is preserved in Git history.
No historical WP1/WP1.1/WP2 Gate, report or candidate input was rewritten.

## Content inventory — 40 files

Hashes are exact committed UTF-8 Git blobs, not Windows CRLF working copies.
Only this Manifest is excluded from its own inventory. This is the complete
changed content set against the merged ADMIN amendment baseline.

| Path | Bytes | SHA-256 |
|---|---:|---|
| CHANGELOG.md | 135593 | 35cf1005ebdc507293cb091dc6cda4883377e4d08df47f0360e7230cf2127fef |
| README.md | 14978 | 24b5fb0646a511c42d98c6a525ca57422769157cebef0ac0a4684da9556cd340 |
| README.zh.md | 14108 | a82efb1022b77112c3f63657b585e333070f671b5e3b8cea2c4da0964acef258 |
| docs/cli.md | 4282 | ea226a15b26399b9a11183828f24c0d6b8ff9d736cb18fee48d5662baad6c673 |
| docs/cli.zh.md | 3564 | 2ef95d397f2084582f72fb384de11ca417414c7169b4f0366ff5cc345a61a4d6 |
| docs/mcp-tools.md | 20993 | fb89adee24369c10c875636d9e2fc8a43a63216cdbb9f669b70ddce836103fb0 |
| docs/pypi/README.md | 3366 | c1fb02b2397e090aa10f17977dd9bad84059577f4bc3459983b6063aff052df7 |
| fcop-README.pypi.md | 5389 | ca0931e849bd37101e9bd51745f38af09d84ffb8771e67857a620fa89a0dce2b |
| mcp/README.md | 5946 | 8aa7e299211fb3c7bda5c94592e2932f73122d3f3427a62e459f850ebd11e16c |
| mcp/pyproject.toml | 4871 | 6791668e5661eae393f99b68e68b0fcbec088f39370d1a5b9caa8add65af2ea9 |
| mcp/src/fcop_mcp/_specs.json | 98656 | 14b000e56217f39fc7a704b32882aaf95fd58502073cf2253f69c9b38df26cae |
| mcp/src/fcop_mcp/_version.py | 607 | 0c72a4f4c85dddd281c3c8ba429d4148a2809fcd66a65afa3497d5d5da6c1cbc |
| mcp/src/fcop_mcp/adapter.py | 13880 | 1d26ea295be02cb5162d39602cd11cc88a6bfb6aaaebbb5c55001dd971421c48 |
| mcp/src/fcop_mcp/catalog.py | 651 | fb21c8bad54c15294dc13da4a8ea55c46fca0576f8448c1fcaa26e7262ed4173 |
| mcp/src/fcop_mcp/disposition.py | 2986 | d053722d9a6e0cc01a6858fffadfe181e1be5c8d4c73e4ffd839b465771d96e8 |
| mcp/src/fcop_mcp/routing.py | 3820 | b02e6f2e5de5652cc5614683a1d7a99a87489083fe2415e98d9a966814e7a796 |
| reports/FCOP-4.0-CLI-V1-BASELINE.md | 2181 | f61c9b6d0e3624e64906efa6c5024dfbb5b46cfab38c8705b246e88c3b22478c |
| reports/FCOP-4.0-CLI-V1-CONTRACT.md | 3108 | 742c0b8ebf9de9f6f43fb91d5bbd110f77bb8263f2501126c9a2cf667a75729f |
| reviews/fcop-4.0/cli-v1/BASELINE.md | 5692 | 835602718386e133cb85256b219544cbe813cb657325e818f2213df9b2e5783e |
| reviews/fcop-4.0/cli-v1/CONTRACT.md | 1999 | 68570010a4d0ca9cde4119a803217a46836c93a008299fe427271d85ef489364 |
| reviews/fcop-4.0/cli-v1/MCP-CATALOG-PROOF.md | 1505 | fc80b9fb0fc1070bc391ee1be67c335b72eb1e1b514589087e208d7bd1805664 |
| reviews/fcop-4.0/cli-v1/PACKAGE-PROOF.md | 4423 | 5e8f646be2f49289601ce1477d2d198885e01d0db8cbe1f03452f75225adf0b4 |
| reviews/fcop-4.0/cli-v1/READONLY-PROOF.md | 1389 | 24201649c49cc0c4b3d502d0441bcc8ede518934961240b8cce339bcaf09dfa7 |
| reviews/fcop-4.0/cli-v1/TEST-RESULTS.md | 4573 | 301b0f052a24e9aa3111a5ad00f84c1ef3d42d524106a164ce06f88bced00957 |
| scripts/cli_v1_installed_probe.py | 6307 | c4d83ee5274f0d23acbd5a4b5e11b2ed0d6d42e30d906b2567c9bd4887c78e81 |
| spec/fcop-4.0-spec.md | 26397 | 9e6fd97ed4f3fa4bf9178babd54fd671fe4cc5f7bf7b8ee985d1726fb8c0e491 |
| spec/fcop-4.0-spec.zh.md | 24537 | babe6acad7ddcd41ae06a3e9b21334b191576111905012f752a3052d5951dcf9 |
| src/fcop/_version.py | 561 | 6f67ead43c6f75848e999f32da10f7dc2ffc3f708dc33cd94554a12778a5e683 |
| src/fcop/cli/_main.py | 2797 | 1b856eb96e935bd96382ceee9d840720dbeb7c96147fc20e7cd83a5b8b27fd7e |
| src/fcop/cli/_observe.py | 9355 | a018f37d4d5ec255d861279391f46a6657a4778fdf93398c78619914c345cf5d |
| src/fcop/observation.py | 9196 | e3910f4d1ed2f162e57f0d41e093c211dfe3ca6077b838568c206b26e2873068 |
| src/fcop/v4/rule_distribution/_read.py | 10645 | 0caf5b40c025fd20649834be722409267ef3534af697bcac02b3f9c6f481f872 |
| tests/conformance/rule_distribution_v4/test_dist_00_meta.py | 15280 | 61be4b5675b367166c48b0eddb8a33653ad07108dcfbef8235395dc403b549e7 |
| tests/test_fcop/test_cli_release_identity.py | 3093 | cb88c046b2a8809ad6aeb4a0a607851a2f26f708c0a9b7e4c49be7d928e67eb6 |
| tests/test_fcop/test_cli_v1.py | 9247 | df73ab30d6e7beac1d55b10eb6b81a5efe095d529c48d6e92d71733f571fada6 |
| tests/test_fcop/test_install_prompt.py | 7077 | cc8de577ecfed0ea59e4ad676f42b499a547276c7feda927cc39835de47194e6 |
| tests/test_fcop/test_v4_rule_distribution_reads.py | 14714 | fc6e1a74a072fb0fa3f7b2652228cb9e21ac21d2e6cc2460212a20b7952a7e85 |
| tests/test_fcop/test_wp4f_release_readiness.py | 14452 | 6f79f68cdea9f2e18ecc1ad14956c39b06ad0a1c82d9e8fe711a4821c5b6892c |
| tests/test_fcop_mcp/test_cli_catalog.py | 2008 | 8ee773aff6eb28182b43a9c41f4e04520a8992fbeaac3efb472021a7983099ac |
| tests/test_fcop_mcp/test_wp4f_release_pairs.py | 1047 | f2c6b5665ce3993bdf7ea303b6a6414271a6d29530df07bacdbdefa07018eb77 |
