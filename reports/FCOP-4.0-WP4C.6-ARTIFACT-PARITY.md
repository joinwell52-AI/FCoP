# WP4C.6 artifact parity evidence

Authority: original WP4C.6 taskbook dc4bd62d47c3c422c8e758b588369dd3ed089acd, resumed by 6a/6b; final erratum 8162d6ae9a91b8b23a6698bfd292a2cb2a75194c. Artifact generation below is local verification/export only. No release, tag, upload, publication, workspace migration or adoption occurred.

## Canonical data identity

Source directory: src/fcop/rules/_data/v4. The nineteen files are unchanged from the accepted input. Raw UTF-8/no-BOM/LF module/Manifest bytes are copied, not reserialized or translated.

| Canonical member | Bytes | SHA-256 |
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

These paths occur beneath fcop/rules/_data/v4 inside both data export formats and the normal FCoP wheel/sdist. Carrier metadata is not counted as canonical rule members.

## Actual public offline exports

Public entry: Project.rule_distribution(action="build_artifacts"). Fresh frozen DIST-27 wheel/sdist nodes passed 2/2. The ordinary test test_exports_exact_bytes_repeat_and_no_workspace_effects exercised the real canonical package twice, independently opened the ZIP/TAR, verified member paths/raw bytes, excluded Host files/receipts/CodeFlowMu, compared full archive digests and checked unchanged workspace snapshots.

Actual outputs in D:/fcop-wp4c6b-fcop-01/test_exports_exact_bytes_repea0/{first,second}/:

| Format | Bytes per archive | First SHA-256 | Second SHA-256 |
| --- | ---: | --- | --- |
| Offline rule-data wheel | 57438 | 152716140d60e435a040ba6e524deda46a8b80407521cb1d1015e87afbe003f2 | 152716140d60e435a040ba6e524deda46a8b80407521cb1d1015e87afbe003f2 |
| Offline rule-data sdist | 18616 | ffc8ce654bde1049f69c87a466272f43038bc7772f5cc4d6117c8a2f998c4f87 | ffc8ce654bde1049f69c87a466272f43038bc7772f5cc4d6117c8a2f998c4f87 |

The content-addressed filename version 0+<Manifest SHA> identifies an offline fcop-rule-data carrier, not a new FCoP release. Standard-library archive construction has deterministic member order, ZIP epoch 1980-01-01 and TAR/GZIP time zero. No shell/build backend/network is called by this production action. Native cross-platform whole-archive digest equality is not claimed from this same-platform experiment.

Negative ordinary tests cover explicit offline/non-isolated requirements, malformed formats, extra fields, occupied/overlapping/indirect output, input drift and zero effects before refusal. No installed package, Host entry, receipt, absolute workspace path, credential or external constitution is inserted into the canonical data archive.

## Normal package builds

Commands used the existing build backend without isolation, changing no build/dependency/version configuration:

```text
D:/fcop-wp4c5b-wheel-venv01/Scripts/python.exe -B -m build --no-isolation --wheel --sdist --outdir D:/fcop-wp4c6b-artifacts-fcop .
D:/fcop-wp4c5b-wheel-venv01/Scripts/python.exe -B -m build --no-isolation --wheel --sdist --outdir D:/fcop-wp4c6b-artifacts-mcp ./mcp
```

| Local normal artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| D:/fcop-wp4c6b-artifacts-fcop/fcop-3.2.5-py3-none-any.whl | 725887 | b382282a76d93f0cfa08b898445e2614b3f8732f61e1fd74256003c74b441b28 |
| D:/fcop-wp4c6b-artifacts-fcop/fcop-3.2.5.tar.gz | 647334 | e72b1fd41e62664ce83b7342fb5b962b2df145cbb91eb389d9065e1f49fd2faf |
| D:/fcop-wp4c6b-artifacts-mcp/fcop_mcp-3.2.5-py3-none-any.whl | 117449 | 5e3ff514c1fca324bbd27a6597c44bc0db4189ea58705b866718f1102a0ba132 |
| D:/fcop-wp4c6b-artifacts-mcp/fcop_mcp-3.2.5.tar.gz | 108959 | 46b245d0d9ad686fe6daf25a97e28fef223d93febf0573d5412be07ddafd2756 |

Both normal distributions retain version 3.2.5. These normal package archives are distinct from the offline rule-data exports above.

## Clean-install status

CLEAN_INSTALL_PARITY: PASS_19_OF_19
INSTALLED_REAL_STDIO: PASS_46_12_4

The new non-system-site-packages environment D:/fcop-wp4c6b-clean-install01 installed the actual two local wheels and their declared dependencies. The initial installation was deliberately interrupted due to prolonged installation time; it was then force-reinstalled completely with --no-compile in this same task-created environment. This process interruption is not a successful install or a product test failure. The completed reinstall and pip check both passed; no existing environment was substituted.

After the combined regression, normal wheel/sdist builds were rerun and retained all four hashes above. Under -I -B, tests/test_fcop/rule_distribution_artifact_probe.py verified that FCoP imports from this environment, source/wheel/sdist/installed nineteen-member raw byte parity, and actual installed public export. The unchanged tests/test_fcop_mcp/artifact_probe.py base performed real installed stdio: exactly 46 tools, 12 static resources and 4 templates, successful create/exact retry/spec reads, structured rejection and five Project/MCP resource projections with zero effects. Its relay mode passed actual loopback initialize/tools-list and the controlled missing-extra diagnostic.

Resolved versions: fcop=3.2.5, fcop-mcp=3.2.5, fastmcp=3.2.4, mcp=1.30.0, websockets=17.1. Runtime dependency declarations were unchanged; test-environment resolution of existing transitive constraints is not a product dependency change.

## Historical and platform limits

PR #29 and PR #30 blocked reports remain preserved in commits 91e64fa0a0ee377335af3226263a1811e1a56c1d and 576bad0025038ee085fc53da46c125143d126bd3. Their then-NOT_RUN continuation states are not reused as current evidence. Fresh target and FCoP JUnit hashes/commands are in RESULT.

Final Manifest HEAD native Windows/Linux/macOS CI, package jobs and remote SHA readback remain independent mandatory checks. Local LF bytes or old reports-only green jobs do not establish default Windows checkout compatibility.

ARTIFACT_MEMBERS: 19/19
REPEAT_BUILD_DETERMINISM: PASS_SAME_PLATFORM
WP4C_RULE_DISTRIBUTION_ACCEPTED: false
