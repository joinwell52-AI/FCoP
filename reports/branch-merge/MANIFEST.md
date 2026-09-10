# FCoP 4.0.1 Branch merge review manifest

- PR: https://github.com/joinwell52-AI/FCoP/pull/37 (Draft; no merge/release authorization).
- Branch: codex/fcop-mcp-4.0.1-branch-merge.
- Baseline: ec7f415f84bfb93534ffccedaad873accd744095.
- Content HEAD: d3154b02503c201072bae7bd047fcbefbd7f8b43.
- Preserved blocker: 94d840bc7fdaa8988ddb316ab06b58d7e48a1c45.
- Canonical file SHA-256 below hashes Git blob bytes, not Windows CRLF materialization.
- Content files: 38/38.
- This manifest is excluded from its own hash list; its HEAD and hash are verified separately in the final PR receipt.
- Final CI and local full-regression results are bound to review HEAD by that receipt, not inferred from earlier green runs.
- Frozen Conformance, Schema, bundled rules, release workflows and CodeFlowMu are unchanged.

| File | SHA-256 |
| --- | --- |
| CHANGELOG.md | dc0baa4d78b71299ebb9e042aab67b6709ca8cf1ffd49b614dab0e77602f8d8b |
| README.md | 08a106b36c465209c81b29be368ed33ada8db92676ace031e4eca2342c35b3f3 |
| README.zh.md | dd200dfb316ce99820923bba0a85db3b8c9ca19a7d0c2012a38fe8ab42b17ca8 |
| docs/branch-merge.md | 94e9642bfb760308b8cec4bd1355087003f466e2a5d3ecb7b50bf7ce2ba84067 |
| docs/branch-merge.zh.md | d5ba92fb292828f37aa62e6fee5339d9441615acf89b2cee7a12d5440033badc |
| docs/mcp-tools.md | 608ffcfa69f11fbd0b0181ad60d8194f0e344ba908eef14fdf2d3dc5f696e2e0 |
| mcp/README.md | 5cbad1d3f49e7651abf51b14493a8277b46c4091d057d2c15398ccede1f24b82 |
| mcp/pyproject.toml | 19d1284b02725e100e1cd8bb53e1cb6550ba82ac5ce30862ee5339f08934ff7d |
| mcp/src/fcop_mcp/_version.py | bb7146dde9201eb15773bec4a4c69b8171bf521b0088a1dfef6e52c3c9b41195 |
| mcp/src/fcop_mcp/adapter.py | 3b438b6353fbdc947712e395623a9d9ba97882ab968d7bae260e0547a8b15720 |
| mcp/src/fcop_mcp/branches.py | bd80f3671ce377715a38b5221494d8fedc4238da716925b74c5872bb6cbd2d94 |
| mcp/src/fcop_mcp/routing.py | 4a178d496e12fe5e945f09e51463e2f88af616234d342b30a8f2f3f6cdbb7d12 |
| mcp/src/fcop_mcp/server.py | 897b9386c76f0785e7f46ab0ca096a9347496e0756909b957bbe88564e2b60ca |
| reports/branch-merge/DELIVERY.md | b96ddf7855a3e79fd4dfa9136231c16a49a1969beaec447f48fc8549aa05d5cc |
| reports/branch-merge/IMPLEMENTATION.md | 7bd590ecb44a3a3510a1eb43941ade795253b05ebf47b54c43268a890114f484 |
| reports/branch-merge/REPORT.md | 2dd0753cb728a17cd8babca392b59cd07773b74da0f1d7bb11fa6b1789f19408 |
| reports/branch-merge/TASK.md | bd9e557aeefbc46839574122aa7453ace3646d3d15183b860d20eff312d34d98 |
| reports/branch-merge/core_capability_probe.py | 3e853ae221e3a4a02258428e64d32a7e8937ceee82756b2e620a3a6dda716022 |
| reports/branch-merge/installed_probe.py | 3a04f710f2700311ba4950c7ac930d38cc16df0a9f5bca108d5f6a214ae8559e |
| src/fcop/_version.py | 30278235b075b0ff82e5736c03698a0c0965610dcebe60a0b6f5a58a99c61258 |
| src/fcop/project.py | b9a727216d8da37de5e07c248ae254bf245f22a060d5316fbb1cade50812a70b |
| src/fcop/v4/boundary.py | 73000d70b9c0f104895d6f3d8ca16aa3dcb2065693613c6004cf1d3b2897788f |
| src/fcop/v4/convergence.py | 4244245661aee8d64492fec26b0cf72bd13e3f9e6bc66e715bf2ff531e0cfcd6 |
| src/fcop/v4/creation.py | a0c24e6667d69611d959ce860f9c1245724cae1fd87f13ebf9abcb3752edddbd |
| src/fcop/v4/merge.py | 8f796c7ab86d2f7e8a0d794206755c277bda6b81d0c74b486589c561f122153c |
| tests/test_fcop/snapshots/public_surface.json | 06dc87e9781ee7389ac830a4f4396c3fc6fbe402156cfd780ed9a9f88286560a |
| tests/test_fcop/test_branch_merge.py | 2b94367a744435cd8d11a04d89d587e4a8a474f577871dd1e4db89d3e0adedec |
| tests/test_fcop/test_v4_creation.py | 0c7c3d6e4d0960ecc9f19a0bb340352007fecaf91ff778e477023c4390ff322f |
| tests/test_fcop/test_v4_rule_distribution_closeout.py | 7b95f34e8385a417b69635a7b7e908c814d1cc326907342789d2fdbdd30dfad2 |
| tests/test_fcop/test_wp4f_release_readiness.py | 633c755a69acbae7ef7b34741f70cb536ffe327856637dc8b795d6d17d45a03f |
| tests/test_fcop_mcp/artifact_probe.py | e733746baf5cd5b0723d59364c039f7fe297d28d0fc6a04a3f6651f9508fe156 |
| tests/test_fcop_mcp/snapshots/tool_surface_4_0_0.json | ab133b6018634ff0893e5039c7a31ae69a8612239eb75e0d99dd7f756ae378c4 |
| tests/test_fcop_mcp/snapshots/tool_surface_v4.json | 99ab4ab6f0026b1a9da2234eed05cfa3a94257aba02e05f05307890d9b492d6e |
| tests/test_fcop_mcp/test_branch_merge_stdio.py | af51a3184ca6ea46d07fce23d149c9e0778303d8398a064393d827809e9fdb6a |
| tests/test_fcop_mcp/test_wp4b_delivery.py | d25d9ce64fbe27029cff492530e3fc4b6ffe60f11d50fe97bc5bfdc70dcf2221 |
| tests/test_fcop_mcp/test_wp4b_resume.py | a8d2c485bf96e36ec19a36453cef42493d38a6d7291551403ea9d8ef479f4f9e |
| tests/test_fcop_mcp/test_wp4c5_resources.py | febd092f83e0881177d820091b927777f5aa9f7578b52c29f5d9e5ec458d845a |
| tests/test_fcop_mcp/test_wp4f_release_pairs.py | dda0098e2cd9fd47f45c1c840b5efe4b3487e3f2bc28010c134c05bc415cbdb8 |
