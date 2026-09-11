# CLI v1 delivery manifest

STATUS: BLOCKED
REQUESTED_ADMIN_GATE: NONE
AUTHORITY: CLI-V1 taskbook v4, 8bedfd3e132b7cca38e017ca518807332abb4bc2
TASKBOOK_SHA256: 923480c9a6c4ffa7211cb0032f5497ba4089bb97339fe203978359cd97254e3f
BASELINE_HEAD: 8bedfd3e132b7cca38e017ca518807332abb4bc2
CONTENT_COMMIT: 205d9fb20ba94998d66f331831c81681b29ab541
BRANCH: codex/fcop-4.0.2-cli-v1
VERSION_PROPOSED: fcop==4.0.2 / fcop-mcp==4.0.2
RELEASE_AUTHORIZED_CONDITION_MET: false
MAIN_MERGED: false
TAG_CREATED: false
PYPI_PUBLISHED: false
GITHUB_RELEASE_CREATED: false
CODEFLOWMU_MODIFIED: false

This manifest-only commit follows the content commit. Its own HEAD and SHA-256,
remote refetch/file verification and Draft PR link are recorded in the PR receipt
to avoid self-referential hashes. The table hashes exact UTF-8 Git blobs,
not Windows checkout line endings. No final CI success is claimed.

## Release blocker

C19 FAIL: the pre-existing MCP README inline-prompt assertion conflicts with the
current landing page. See BASELINE.md and TEST-RESULTS.md. Do not merge, tag or
publish this delivery. It preserves the implementation for ADMIN scope ruling.
Original full run: 2415 passed / 1 failed / 2 existing skips; newest targeted
CLI/catalog run: 88 passed. See the reports for source timing and limitations.

## Content inventory — 32 files

| Path | Bytes | SHA-256 |
|---|---:|---|
| CHANGELOG.md | 135323 | 0d23cf9c95cbee7a08cdf0f36ef97f3b96a1e28dc1ffee2757909c6c0a8b6dc8 |
| README.md | 14978 | 24b5fb0646a511c42d98c6a525ca57422769157cebef0ac0a4684da9556cd340 |
| README.zh.md | 14108 | a82efb1022b77112c3f63657b585e333070f671b5e3b8cea2c4da0964acef258 |
| docs/cli.md | 4282 | ea226a15b26399b9a11183828f24c0d6b8ff9d736cb18fee48d5662baad6c673 |
| docs/cli.zh.md | 3564 | 2ef95d397f2084582f72fb384de11ca417414c7169b4f0366ff5cc345a61a4d6 |
| docs/mcp-tools.md | 20993 | fb89adee24369c10c875636d9e2fc8a43a63216cdbb9f669b70ddce836103fb0 |
| docs/pypi/README.md | 2863 | 3c82fcf7a2145b28e9f731f14745c00cf29d17f9f3be6b506fc8dba79098a9fe |
| fcop-README.pypi.md | 4743 | cf6a615ebe0d0163d7100ad4789d2f2c6cff657c2cec670fe817c0c3d51d55d7 |
| mcp/README.md | 5458 | 5429133d720eeff47e3c957614449675d703b31288d65eca2f8208ded5655761 |
| mcp/pyproject.toml | 4871 | 6791668e5661eae393f99b68e68b0fcbec088f39370d1a5b9caa8add65af2ea9 |
| mcp/src/fcop_mcp/_version.py | 607 | 0c72a4f4c85dddd281c3c8ba429d4148a2809fcd66a65afa3497d5d5da6c1cbc |
| mcp/src/fcop_mcp/adapter.py | 13880 | 1d26ea295be02cb5162d39602cd11cc88a6bfb6aaaebbb5c55001dd971421c48 |
| mcp/src/fcop_mcp/catalog.py | 651 | fb21c8bad54c15294dc13da4a8ea55c46fca0576f8448c1fcaa26e7262ed4173 |
| mcp/src/fcop_mcp/disposition.py | 2986 | d053722d9a6e0cc01a6858fffadfe181e1be5c8d4c73e4ffd839b465771d96e8 |
| mcp/src/fcop_mcp/routing.py | 3820 | b02e6f2e5de5652cc5614683a1d7a99a87489083fe2415e98d9a966814e7a796 |
| reports/FCOP-4.0-CLI-V1-BASELINE.md | 2181 | f61c9b6d0e3624e64906efa6c5024dfbb5b46cfab38c8705b246e88c3b22478c |
| reports/FCOP-4.0-CLI-V1-CONTRACT.md | 3108 | 742c0b8ebf9de9f6f43fb91d5bbd110f77bb8263f2501126c9a2cf667a75729f |
| reviews/fcop-4.0/cli-v1/BASELINE.md | 1878 | e02024e1d9c035aba86cc984ad106ba1611b86bf1da9208eb2f83ee45a0be98c |
| reviews/fcop-4.0/cli-v1/CONTRACT.md | 1668 | e6b914ac742ddab647a1cbc99359aa22487fc0465acd2c3f632f7d711e749d5f |
| reviews/fcop-4.0/cli-v1/MCP-CATALOG-PROOF.md | 1109 | 2d8bb01dc016f785f60b14404f77f979aedc09f79da86b75dca3fcd2313cfe62 |
| reviews/fcop-4.0/cli-v1/PACKAGE-PROOF.md | 2503 | 4cebb56115e9b47b0e0526d610c6b237a8928cbfbe1ae71724fb21e244555472 |
| reviews/fcop-4.0/cli-v1/READONLY-PROOF.md | 1168 | 2a8ef472cb16af65fe466646b6f39985ae21d6bfbb572285ea3b55a8c6215a80 |
| reviews/fcop-4.0/cli-v1/TEST-RESULTS.md | 3147 | 5d8a9c3c5fab8847552c659c46648025813fabc30fa58110ad5f23e7a1af24f4 |
| scripts/cli_v1_installed_probe.py | 4110 | dc1fb60f7fb6671364785af7a27f4eacddb28f64b222fbff40f0399953df5f79 |
| src/fcop/_version.py | 561 | 6f67ead43c6f75848e999f32da10f7dc2ffc3f708dc33cd94554a12778a5e683 |
| src/fcop/cli/_main.py | 2797 | 1b856eb96e935bd96382ceee9d840720dbeb7c96147fc20e7cd83a5b8b27fd7e |
| src/fcop/cli/_observe.py | 9355 | a018f37d4d5ec255d861279391f46a6657a4778fdf93398c78619914c345cf5d |
| src/fcop/observation.py | 9196 | e3910f4d1ed2f162e57f0d41e093c211dfe3ca6077b838568c206b26e2873068 |
| tests/test_fcop/test_cli_v1.py | 9247 | df73ab30d6e7beac1d55b10eb6b81a5efe095d529c48d6e92d71733f571fada6 |
| tests/test_fcop/test_wp4f_release_readiness.py | 14452 | 6f79f68cdea9f2e18ecc1ad14956c39b06ad0a1c82d9e8fe711a4821c5b6892c |
| tests/test_fcop_mcp/test_cli_catalog.py | 2008 | 8ee773aff6eb28182b43a9c41f4e04520a8992fbeaac3efb472021a7983099ac |
| tests/test_fcop_mcp/test_wp4f_release_pairs.py | 1047 | f2c6b5665ce3993bdf7ea303b6a6414271a6d29530df07bacdbdefa07018eb77 |
