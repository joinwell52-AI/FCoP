# FCoP 4.0.3 implementation delivery Manifest

Status: LOCAL_VERIFICATION_PASS_REMOTE_CI_PENDING. This supersedes the earlier BLOCKED checkpoint status, not its historical evidence. No ADMIN Gate is signed here.

- Execution-start base: `157acaeb0cbd11bbf0ce54fba18c2a7d0d980efb`
- Current-main integration / inventory base: `aa970936f19b875720c4b17608bb3c17b7fb195c`; merged into this review branch only, preserving PR #49 handoff material.
- Taskbook: `8ec8658c15f2aa148bd42e3d6e6bb916921e4b0b`
- Spec source: `1f91d53c51f040b1f4bd306d72d7e31ce35c7084`
- Implementation: `009d6abdadcde1fc97c440e04970434e2e0c9459`
- Candidate build source: `b767e8f46ede33d405a96ba568dc38b4e733b3ec`
- Corrected test HEAD: `5da0bbc127e272cd2492c2963db6441e6b2c46e3`
- Evidence/content HEAD: `bbc207e6dd4479840a379271fdb19670ba632dc3`
- Branch: `review/fcop-4.0.3-four-file-retirement`
- Draft PR: https://github.com/joinwell52-AI/FCoP/pull/48
- Delivery HEAD: the commit containing this Manifest; exact SHA, remote hash readback and CI results are bound by the final PR receipt. A Manifest cannot contain its own commit SHA or own byte hash without a circular dependency.
- Packages: fcop 4.0.3 / fcop-mcp 4.0.3; dependency fcop>=4.0.3,<4.1.0.
- MCP surface: 49/12/4, original signatures preserved.
- Full local tests: 2320 passed, 0 failures, 2 existing Legacy empty-sample skips.
- Installed behavior: 36/36; clean Core/pair wheel/sdist probes: 4/4.
- Frozen Core Conformance: 18 files unchanged, 60 IDs / 119 nodes PASS.
- Active rule-distribution suite: 101 nodes PASS; Host-only retirement explicitly itemized in TEST-RETIREMENT.md.
- Candidate reproducibility: 4/4; strict Twine: 8/8; actual description bytes: 4/4.
- Public release / Registry / Pages: NOT_PUBLISHED by this task; subsequent ADMIN authorization required.
- Requested ADMIN Gate after final remote verification: `FCOP_4_0_3_FOUR_FILE_RETIREMENT_ACCEPTED`.

## Candidate artifacts

- `fcop-4.0.3-py3-none-any.whl` — 721754 bytes — SHA-256 `a974ff981cb829ab2af2ceb1b5fa82c275ffe7c8492a0642c215c3817bff244d`
- `fcop-4.0.3.tar.gz` — 628433 bytes — SHA-256 `2323147d5d740cc671f9a8219826b642bb37d997e02059819033c3842d1378db`
- `fcop_mcp-4.0.3-py3-none-any.whl` — 116598 bytes — SHA-256 `6264ec0fb08ac8aa46780c0dc165e13e07571da2524480fdedcebe23e4d38897`
- `fcop_mcp-4.0.3.tar.gz` — 107434 bytes — SHA-256 `8f2dea3e5b7d4a47099cae9b2d6cfd859dadad17bc400e59dd88dcbdd400aced`

## Changed-file byte inventory

Hashes cover canonical Git blobs at the content HEAD above relative to the current-main integration base, not Windows CRLF checkout bytes. The original execution-start base remains recorded separately. There are 99 changed files: 91 present including this Manifest and 8 deleted. Upstream's three newly added handoff files are inherited unchanged, not claimed as this task's additions. DELETED means absent in the delivery tree; previous bytes remain in Git history. This Manifest is excluded from its own inventory and separately checked during remote readback.

| Status | File | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| DELETED | `.cursor/rules/fcop-protocol.mdc` | — | — |
| DELETED | `.cursor/rules/fcop-rules.mdc` | — | — |
| M | `AGENTS.md` | 926 | `5c920c9c949a14af02140907700e40d224e12a7a058a1cc199663a54d50bb395` |
| M | `CHANGELOG.md` | 136846 | `4e8233c86ce931601fcc934b043832e901fa0da3254edf8f94b8ca29e151ec8d` |
| DELETED | `CLAUDE.md` | — | — |
| M | `README.md` | 17617 | `d19388ef8f5b9c81f4440711636eccd6f2cf275466216b78118fb567f4c68844` |
| M | `README.zh.md` | 16610 | `ec3f43796f1e157cde253c1f0f60476949d7905297a98f49f4a3e84cc60989ad` |
| M | `docs/ai-install.md` | 9018 | `dbaa55f2ca08b7a1eab3ba59b7aa5301f28ae3e6ca03228ad50cd4972a40e2bb` |
| M | `docs/cli.md` | 4282 | `9defc268bafce63818e7961a24178dc61922fc33196934a4c8a5b5cc9384841f` |
| M | `docs/cli.zh.md` | 3564 | `79fced88c3500cb07c716e1515c2e42ce5577f2bbe2e2d0a007715bacba4de84` |
| M | `docs/fcop-4.0-progress.md` | 8437 | `4c103273e8b939e5954cfed34f5b9a987cbcaf20611b6fcb9fbc21ab246f22a7` |
| M | `docs/getting-started.en.md` | 17312 | `2271bcfea25009be9597d8f6a4a6af47dc874f0e1c950b307e03fd5b142816e2` |
| M | `docs/getting-started.md` | 17735 | `7e71eb0ec63894f3b4c2e6e48eeb542613f148905f7d4c3c89c2658e3fc20004` |
| M | `docs/index.html` | 42864 | `4fe65b0425f14ba0a35a42124af54b37c3d7207f634eaea21301245b3215c67c` |
| M | `docs/mcp-tools.md` | 21057 | `d77ffbffc4a690ee6baf9391438f806c395b8585b6ba0bdcc09307672579d58d` |
| M | `docs/pypi/README.md` | 3366 | `524e8eb754ea58113a786fa2d68ef8f365d40d58551ff7de80e43f699ee35cae` |
| M | `docs/release-process.md` | 33002 | `79f6622a2eb4a4aa68c3f2ca387d0d64e859e17b49ff5fae751b6f35aa1b8a4f` |
| A | `docs/rule-resources.md` | 4667 | `470285a7829bfe1a7909d8887152126acfedbf9576f832762f56ee0086d14642` |
| M | `docs/site-assets/site.css` | 18369 | `88698bf69e622ac7b117fb57eeb3a069ed465ada2ac2ebc0ee5bcef3b63b97da` |
| M | `docs/upgrade-fcop-mcp.md` | 8084 | `c13bc065c0c981e0d418f867a8126fe0155eb095d3e27ad6925c25631a3a9678` |
| M | `fcop-README.pypi.md` | 6064 | `04e389fc9aff843f7b23662ed6d12e0e2ee4f1a6ececfa228627d89c96b3fa76` |
| M | `mcp/README.md` | 8027 | `df6b8389505855c413993f3f09e0fd5ba6edd7df2b956480577ab70978e32e2e` |
| M | `mcp/pyproject.toml` | 4871 | `b1c28ceb4e3f9a8cc160a225ca3bf34ad4f1b71bfc5da4bfae08ffab8a7fd7c5` |
| M | `mcp/server.json` | 860 | `6da63ec8bf1b9622874788cddb5cc266686c391c0e3fa2de88edbae1349bc66a` |
| M | `mcp/src/fcop_mcp/_specs.json` | 99433 | `3a601a42aa032c3710cd1b893710d214720ab372637c9576281795d1ef81455a` |
| M | `mcp/src/fcop_mcp/_version.py` | 607 | `e3db43c59a2b9954f92d02441520e62d0eeb67acb79b5beee67012d83eb2fcf7` |
| M | `mcp/src/fcop_mcp/disposition.py` | 2990 | `346522bbcc2547133579844c4cbd513e1171f54aa673d09588e6d885ecff5de3` |
| M | `mcp/src/fcop_mcp/projection.py` | 8383 | `80ae0cf3fe1d82c47894b6a6ea7602e735936c9f1ffadb4d8396eba307d8ecb4` |
| M | `mcp/src/fcop_mcp/routing.py` | 3840 | `0af9df67f6302c93e36319d9532da83fbe8a2251521406ff0c9e6376a4596754` |
| M | `mcp/src/fcop_mcp/server.py` | 160639 | `26bf2882875dcb79fe6133f614d97bb1e640655ea709c4972fa388788086944e` |
| A | `reviews/fcop-4.0/4.0.3-four-file-retirement/BASELINE.md` | 5298 | `bdef6b330380e1db28239105637c78b6f076cb604abc80c45132f2b334af0ed6` |
| A | `reviews/fcop-4.0/4.0.3-four-file-retirement/BLOCKED-INITIALIZATION-BOUNDARY.md` | 7106 | `ddec2a6fd0f3a370fb7e1b06093e3754b10366f050da2672fc2d3c110f0bf361` |
| A | `reviews/fcop-4.0/4.0.3-four-file-retirement/MCP-SURFACE.md` | 1497 | `97e189f76a6b61775bdccb17f751fb8c75df9f0aecba5f0a6814ecaf15b2d587` |
| A | `reviews/fcop-4.0/4.0.3-four-file-retirement/OWNERSHIP-BOUNDARY.md` | 2904 | `a3d86c15b671f732dc74b301e861de68f0a7e83815311305217eec7c60878e76` |
| A | `reviews/fcop-4.0/4.0.3-four-file-retirement/PACKAGE-PROOF.md` | 2407 | `5fb9e229aeb49be34fd013cccd2b2601ba3952443f1f6194b3aa7ef72f5a9442` |
| A | `reviews/fcop-4.0/4.0.3-four-file-retirement/PYPI-DESCRIPTION-PROOF.md` | 937 | `5ed9a3cc6569e57569938c53cc98f46db4500b591018da2f077eb6275220e199` |
| A | `reviews/fcop-4.0/4.0.3-four-file-retirement/RELEASE-PLAN.md` | 1159 | `7e7bd1606743deace31d06fc7c3cc46089b13a20db2b84c57f1cfb34ad16020b` |
| A | `reviews/fcop-4.0/4.0.3-four-file-retirement/RESUME-PLAN.md` | 2201 | `9abcffd058663a6cefda0e8ca129038d4f86ca56ec02bab9b1d5287fe04a3c8e` |
| A | `reviews/fcop-4.0/4.0.3-four-file-retirement/ROOT-BYTE-PRESERVATION.md` | 1445 | `4496c773f1b97f5988017616c4c83ace545252a257a3438e6fed07b7696681c1` |
| A | `reviews/fcop-4.0/4.0.3-four-file-retirement/TEST-RESULTS.md` | 4506 | `4dd292398222b427b03add9b0ccd1f26c3846d818f9b83b22d6c58698b72eb53` |
| A | `reviews/fcop-4.0/4.0.3-four-file-retirement/TEST-RETIREMENT.md` | 3586 | `a257e118eedc8f307a9c7d90e31ec1a51ccd49e9915de8cbd757d408c349420c` |
| A | `reviews/fcop-4.0/4.0.3-four-file-retirement/WEBSITE-PROOF.md` | 2301 | `cb348591cadb257f7eeb7edb53ab834da2186ddc98a03c3fcd2ccc082172e3d1` |
| A | `reviews/fcop-4.0/4.0.3-four-file-retirement/initialization-boundary-repro.py` | 2241 | `404ebc67b031a205e2a9446cfed76a2a9ba213908eae16f2b92fe64bacb08a99` |
| A | `reviews/fcop-4.0/4.0.3-four-file-retirement/package-proof.json` | 1868 | `286366aee70fc797840fe55df0c8bbd7bac31a7ea1e59e9afd4e199ec5b8fabf` |
| M | `scripts/cli_v1_installed_probe.py` | 6307 | `0b6051b8bdca9be9378d5fb7c8ff648323ec352d61bebc858f7b00a923e14fb4` |
| A | `scripts/fcop_403_package_proof.py` | 6031 | `fa461212644815abd4b7fd8f33e7dbcf452c378610769785cb9e0984e341bed7` |
| M | `scripts/pages/build.py` | 9731 | `250c88873e32052166e0ae3e87ee57be97235e93edd831f3eacb6fd667e5b472` |
| M | `scripts/pages/index.template.html` | 37198 | `a16a1102ae92ea3d18078f9db197f2440c5583b8a355f39efb7c1364105adaf5` |
| M | `spec/fcop-4.0-spec.md` | 26792 | `8fba4ee790f380e71c50de0d841beb61d67ea9209cd4b77315d5523debe90140` |
| M | `spec/fcop-4.0-spec.zh.md` | 24911 | `4cfe5696b85b8f26399719b8f74dc7593f3fb796e886a9040881961bf8ff910a` |
| M | `src/fcop/_version.py` | 561 | `b64f31c0116e27baa5f05cac297e3722785edb60b9aa13e7ddd2920167792cb4` |
| M | `src/fcop/rules/_data/agent-install-prompt.en.md` | 2829 | `f3c17ca809cf11f0cf22e628e72150af79533db2a1e33f35dd67fba5e952e146` |
| M | `src/fcop/rules/_data/agent-install-prompt.zh.md` | 2660 | `6d5ee062b6b6114239afce9829e607aa7126baa48cfbb3040be83cc00a97288c` |
| M | `src/fcop/rules/_data/v4/authorization.en.md` | 2116 | `206aef3f8bf23cbaab73fcaa73c0fe070e53ee6c55fc0127d382de1d9fea28db` |
| M | `src/fcop/rules/_data/v4/authorization.zh.md` | 2021 | `e51381642cae47558089bc1ac17a9e73f818a8e189fa62c4353273117b8bf01b` |
| M | `src/fcop/rules/_data/v4/compatibility.en.md` | 3912 | `9a381dd57a36401db215fbf2579b0eb9715a5d068046ede6dbf34165d58e232f` |
| M | `src/fcop/rules/_data/v4/compatibility.zh.md` | 3371 | `ce6d4aad15d7d1a4f858eaeeeb77f0be3a6a0bc75a3d69dec0d1bc6a3946000d` |
| M | `src/fcop/rules/_data/v4/convergence.en.md` | 2271 | `ba4e1e80f7dfcdbe7369d96c009caf92702a0067d9755eac15a100bbb93c96c9` |
| M | `src/fcop/rules/_data/v4/convergence.zh.md` | 2102 | `dae8e0f95c798530e5b644ffb8d6b889c0fc377c610a4490cbd3da49a5768d65` |
| M | `src/fcop/rules/_data/v4/envelopes.en.md` | 1731 | `daa674ee84e2ca0776dbc8efbd072571df25ba49036e6613989e2ed25d728a58` |
| M | `src/fcop/rules/_data/v4/envelopes.zh.md` | 1660 | `92a23f813bf46de64d428b5fb994a32c28b2a88eb8ca3077baac3fcb5bd9033b` |
| M | `src/fcop/rules/_data/v4/idempotency.en.md` | 1708 | `ed6fb259fd88586db79b8195e2532646df2b475483d42f0ef60ee0060cd07ff2` |
| M | `src/fcop/rules/_data/v4/idempotency.zh.md` | 1579 | `8b207caecfccf62fe64d28482f8cd03d2b8587b3af7431f1822aac70e0ef20e5` |
| M | `src/fcop/rules/_data/v4/lifecycle.en.md` | 3029 | `ec20246e998dbd351d34e3771a6fd76cc58ad00eef5740eae192361b33e8b4e7` |
| M | `src/fcop/rules/_data/v4/lifecycle.zh.md` | 2775 | `2bf22c4d2aac616b769854320395c2c364d4ba4600a56f24f8ac495d4388b9f8` |
| M | `src/fcop/rules/_data/v4/manifest.json` | 11209 | `ed114353960785da42434b265f6c4f91ab43d6fc9362b41a3b181f7c4ebd14d1` |
| M | `src/fcop/rules/_data/v4/recovery.en.md` | 3522 | `ffa5141531bb3ca8207ce716825cd2a4629e5d286d172f102e7e92e607877885` |
| M | `src/fcop/rules/_data/v4/recovery.zh.md` | 3087 | `04d6031b1dcd2749c45c7b816c63db2675388dc267780c6aa8156d8317f07084` |
| M | `src/fcop/rules/_data/v4/relations.en.md` | 1094 | `cd4f9e90082b8084c08d195005a65cf088c77158deedd8a31e526aa4332d4232` |
| M | `src/fcop/rules/_data/v4/relations.zh.md` | 1045 | `1497d2c34d368a69c3b1559c394edb92fc70d938320d009dc75927035806d38a` |
| M | `src/fcop/rules/_data/v4/workspace.en.md` | 1908 | `beda65ea376061a87c17710ff44a594c55f277b9ffe4834ca47836ab421e35d9` |
| M | `src/fcop/rules/_data/v4/workspace.zh.md` | 1711 | `9e79cceb2a36504e296d8c435c82729c812f7bbba5500de00a5400782f3a2fe4` |
| M | `src/fcop/v4/rule_distribution/__init__.py` | 3880 | `a3c33ef6320313fa777722944a61af47b7c881291c1f11eea4424c6ed405e0af` |
| DELETED | `src/fcop/v4/rule_distribution/_deployment.py` | — | — |
| DELETED | `src/fcop/v4/rule_distribution/_measurement.py` | — | — |
| DELETED | `src/fcop/v4/rule_distribution/_profiles.py` | — | — |
| DELETED | `src/fcop/v4/rule_distribution/_projection.py` | — | — |
| M | `src/fcop/v4/rule_distribution/_read.py` | 9371 | `75a6ccf1ab2702cbd0de87169d78b9d555696143cf2cf6e49044e5e5d637a0e4` |
| DELETED | `src/fcop/v4/rule_distribution/_receipts.py` | — | — |
| A | `src/fcop/v4/rule_distribution/_request.py` | 998 | `6a6df22e40a425b82101e990dfbb68fc2df7cefb9966f7883e32ed4b51e448be` |
| M | `src/fcop/v4/rule_distribution/_selection.py` | 5350 | `4b30b3dd6569cf13f5687054fcc4fa8d3498523b7246ceea0ae90e73a1336d0c` |
| A | `taskbooks/fcop-4.0/4.0.3/01-Legacy-Four-File-Rule-Distribution-Retirement-and-4.0.3-Release-Taskbook-v1.0.zh.md` | 16312 | `1fccdeca2e7332cc5e5e397847409e9a4f86d32c81ada64dcce4d88bc7a1f70d` |
| M | `tests/conformance/rule_distribution_v4/test_dist_00_meta.py` | 15502 | `506aa20a224ba843a761e6f146ac8bf6a9e5473a379bc647a05d5b3258128554` |
| M | `tests/conformance/rule_distribution_v4/test_dist_07_12_profiles.py` | 1211 | `295f3537bbe0702198642ca50a0c8f987abaf591292442f14873a4b89b5a8571` |
| M | `tests/conformance/rule_distribution_v4/test_dist_13_20_projection.py` | 253 | `68e0a4db19c6a11aa8c46ab71f03d80741fc39c4e3fadef47497bb666f8b4c0e` |
| M | `tests/conformance/rule_distribution_v4/test_dist_21_24_assembly_compat_mcp.py` | 6739 | `1d4b36d3b170464f3bed17e4ef7d97961604568630e969546aa97f450d68ac80` |
| M | `tests/conformance/rule_distribution_v4/test_dist_25_30_failures_artifacts_context_gates.py` | 10356 | `6112f40d83432fbdc2814161450ea75b651dd4bdf4477a6208894d8545e7408d` |
| A | `tests/test_fcop/test_403_cli_entrypoints.py` | 4396 | `d8a7418dae61d69cf5dcad4459b80944e10fd4b6a1f225e1777253face4188aa` |
| A | `tests/test_fcop/test_403_root_ownership.py` | 5583 | `50d5ab1f0546af7ed751690f2cb79a3ff11c5f15538a0b53264bfc8c9b65ebbb` |
| M | `tests/test_fcop/test_cli_release_identity.py` | 4142 | `8519279573bee4ad0325293976ca5ce572c16833f08d1b005b07582c00e2dd74` |
| M | `tests/test_fcop/test_public_docs_release_identity.py` | 2984 | `0675da799685540a0fb0e5698b8d477569ce06b8a750b5b60404dd0ec1f21d83` |
| M | `tests/test_fcop/test_v4_rule_distribution.py` | 8551 | `d86a775e2270d3ccc0316b081f8086e497e494c9b3afb94d7c32dc97f088f1bb` |
| M | `tests/test_fcop/test_v4_rule_distribution_closeout.py` | 8045 | `6add2902df834ad4ef2f77a82d865fc7c45cd6553b18628979581e8690a7b317` |
| M | `tests/test_fcop/test_v4_rule_distribution_host.py` | 2720 | `4e16629d23faff37cfe18c698d8107fbc7620c3ff2364dd0de381cbfed063c7e` |
| M | `tests/test_fcop/test_v4_rule_distribution_reads.py` | 14779 | `4eea1aaa7da67a0b215f58ebb3226dd6f5e816d9fcb7f7a42be663f723dfb3c4` |
| M | `tests/test_fcop/test_wp4f_release_readiness.py` | 15013 | `2d2f464723fd6798d25f32a61ca49e4d263a16c3d65c8c2142fddd69c0f8a581` |
| A | `tests/test_fcop_mcp/test_403_mcp_root_ownership.py` | 2617 | `3ea8a9a5e057b9b657d2b7b27527c0352b1cde70ec1f2eb05255aea086b09ee6` |
| M | `tests/test_fcop_mcp/test_wp4f_release_pairs.py` | 1067 | `9d126d3a2e454fa2da5e674d69b6c3951d3d05da17fea5761703ee0ae56b09d9` |

## Qualification and stop boundary

The atomic initializer's pre-existing `.fcop-init-*` staging/failure evidence remains unchanged; see OWNERSHIP-BOUNDARY.md and the preserved checkpoint reproduction. This delivery does not falsely claim failed initialization has zero writes outside fcop/. Normal successful workspace state and customer Host byte preservation were tested.

No unresolved product-test failure is known locally. Remote CI remains pending at this commit and is not counted as PASS. Failed intermediate tests/builds are documented; 2 historical skips remain distinct from passing tests. No main merge, tag, publication, actual MCP service upgrade, customer migration or CodeFlowMu change is included.
