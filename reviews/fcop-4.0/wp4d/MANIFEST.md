# WP4D Manifest — FCoP 4.0.0rc1 候选收口

## 使用本清单的前提

本清单固定已通过验证的候选内容和全部交付文件。下面的 COMPLETE 是**完成回执声明，仅在本清单 SELF 实际提交完成最终 CI 与远端回读、并在 PR #31 追加绑定该 HEAD 的回执后生效**。写入本清单时，不宣称尚未发生的 SELF CI 已成功；没有追加回执，不能据此验收。最终回执必须同时列实际 Manifest commit、自身 SHA-256、三个运行 ID 和最终运行的机器候选 Manifest SHA-256，避免自引用提交循环。

所有 Gate 均由 ADMIN 签署；本文件只请求，不签署。先前 BLOCKED 文本及失败日志均保留在下方历史区或 evidence 目录，当前解释以本节及六份报告顶部为准。

## 固定候选完成回执（最终 HEAD 核验后生效）

```yaml
wp4d_status: COMPLETE
status_activation: FINAL_HEAD_CI_AND_REMOTE_READBACK_RECEIPT_REQUIRED
authorized_scope: WP4D_VERIFICATION_REPAIR_ENVELOPE_AND_CLOSEOUT
base_commit: 167c5fd4ca4c9603c392bae3a4a055963e7b7ed6
taskbook_commit: cbdc60a92a02b9e2eb0c1c6e2e93f74c335407f9
taskbook_sha256: bfc93f595800efe5185588ff92b612c9ca66e1622118e76c805d5fd908a1e290
verification_repair_taskbook_commit: ba8830c1871f6516fec1e2779d21c09b9a5e96ea
verification_repair_taskbook_sha256: badc8a597a01407dec012d1085a5cac5815f8608e8afec742688846beb11c625
verification_repair_taskbook_bytes: 7652
socketpair_erratum_commit: 6c2793d2f91fe5c0c8d4edce4e8e0064f889c686
socketpair_erratum_sha256: 29a43ba7a5646a38a89e509c4e8f0b5c03d2f7b8a31d4bee9dc76b10a41eaa2e
resume_implementation_head: 737d3d3482f371616863a018f04ab1a756259723
candidate_commit: d1a86f32d87f000fe0aec444563decdc892dc142
historical_evidence_commit: a584e02ba4166d2dcdae8dab84f36d5a2c43d222
evidence_commit: 6549a639574d4587a7fa9ffc5f96f4f156b336ba
manifest_commit: SELF
manifest_parent: 6549a639574d4587a7fa9ffc5f96f4f156b336ba
target_versions:
  fcop: 4.0.0rc1
  fcop-mcp: 4.0.0rc1
mcp_dependency: "fcop>=4.0.0rc1,<4.1.0"
artifact_hashes:
  fcop-4.0.0rc1-py3-none-any.whl: b539fdd496d52ea608b5f42abd270c2ed04e8f011242d932ddedac48f8d7cee9
  fcop-4.0.0rc1.tar.gz: 43e4488af52bffac3e400c14f442136f955ee0477ddf0e94386481e6ec682bb4
  fcop_mcp-4.0.0rc1-py3-none-any.whl: 20167b314de1a90093b74cf42c7039edceddc1458e1b37ce3e9e6f31697c773a
  fcop_mcp-4.0.0rc1.tar.gz: eefde60b6d156f5ef2184186f5f5a355837f0fc9e0244b3e2d8077dbed51000b
artifact_reproducibility: 4/4
twine_checks: 2/2
twine_version: 7.0.0
packaging_version: 26.3
metadata_version: "2.5"
source_date_epoch: 1788940367
candidate_content_machine_manifest_sha256: 148915cde716d63284950ed46f9250e55b182885b23209cb56ac7d70d5b7dc8c
candidate_content_actions_run: 34377729223
candidate_content_artifact_id: 10114578638
legacy_regression: 1912/1912
wp4d_tests: 19/19
ubuntu_full: 1931/1931
windows_full: 1931/1931
failures_errors_unexpected_skips: 0/0/0
existing_ci_applicable: 27/27
windows_existing_ci: 8/8
rc_workflow_applicable: 15/15
candidate_content_total_ci: 42/42
pr_only_jobs: 2_NOT_APPLICABLE_NOT_COUNTED_AS_PASS
rc_consumer_matrix: 12/12
installed_wheel_sdist_origins: 24/24
mcp_surface: 46/12/4
canonical_files: 19/19
frozen_bytes: 21/21
frozen_core_conformance_tree: 24ab264c6bca9a3183ee270becb552f22a4c4f9e
frozen_distribution_conformance_tree: 4f99c7261b63b6db81c500604a231defaca9f14b
codeflowmu_shadow: 14/14
shadow_proof: EXISTING_FIXED_CANDIDATE_EVIDENCE_VERIFIED
supplemental_shadow_rechecks: FAILED_EXTERNAL_CHANGES_PRESERVED_NOT_RELABELED
quiet_window_escalation: WITHDRAWN_EXECUTOR_JUDGMENT_ERROR
codeflowmu_adoption_policy: "<4.0"
codeflowmu_upgrade: false
codeflowmu_runtime_consumption_verified: null
further_live_codeflowmu_access: false
content_evidence_remote_readback: 86/86
content_evidence_readback_head: 6549a639574d4587a7fa9ffc5f96f4f156b336ba
content_evidence_readback_utc: 2026-09-09T17:32:11.061939+00:00
delivery_files_including_manifest: 87
final_manifest_head_ci: POST_PUSH_RECEIPT_REQUIRED_NOT_PRECLAIMED
final_head_remote_readback: POST_PUSH_RECEIPT_REQUIRED_NOT_PRECLAIMED
final_run_machine_manifest_sha256: POST_PUSH_RECEIPT_REQUIRED
draft_pr: 31
pr_base: task/fcop-4.0-wp4d-rc-candidate
pr_head: feat/fcop-4.0-wp4d-rc-candidate
main_merge_authorized: false
tag_authorized: false
rc_publish_authorized: false
stable_release_authorized: false
pypi_publish_authorized: false
github_release_authorized: false
mcp_registry_publish_authorized: false
zenodo_publish_authorized: false
codeflowmu_write_authorized: false
requested_gate: FCOP_4_RC_ACCEPTED
gate_signed: false
```

## 证据与判定边界

- 候选内容 C=`d1a86f3`；其后的 `a584e02` 与 E=`6549a63` 都只有报告/evidence，本 M 只改 Manifest。任何后续内容变化都会产生新的 C 并使本证明失效。
- 内容 C 的真实运行：[Core 34377729431](https://github.com/joinwell52-AI/FCoP/actions/runs/34377729431)、[MCP 34377729147](https://github.com/joinwell52-AI/FCoP/actions/runs/34377729147)、[RC 34377729223](https://github.com/joinwell52-AI/FCoP/actions/runs/34377729223)。这些已通过，但不得代替 M 的新运行。
- 最终 M 的 RC build 会重新从 C 导出两份独立源目录并检查原始 4/4；其机器 JSON 同时记录 commit=C、execution_head=M。M 的所有 12 consumer 必须使用该运行同一第一组，校验 M 的机器 Manifest 新摘要。不得把内容运行 JSON 的旧摘要当成最终运行摘要。
- 首次 Shadow 原始证据 SHA-256 `d0e293c19bd5297659cd67f71ae32dc607d2172fee08e447108788d834b8a6f8`（3832169 bytes），完整 inventory 摘要 `c2ef5998d3646e340dcd7196ff60c20c6986c92a233f43547e6434c8ef96e0ea`；固定候选没有改变。首次精确计时未单独采集，不补造。后续附加复验失败不隐藏，也不倒算成 FCoP 修改了其他项目。
- 用户已明确这里只升级 FCoP，CodeFlowMu 仅采用 <4.0。不再把额外活动工作区复验或静默窗口当作 FCoP 收口前置条件；不再访问或协调该项目。已有兼容性证据绝不代表该项目采用了 RC。
- 离线守卫 12/12 跨平台回归保留真实 code object 身份放行；普通网络及伪造文件名/函数名均拒绝。没有放宽生产语义或 frozen assertions。
- 发布 workflow 只读审计见 CI-AND-RELEASE-READINESS。tag、RC/stable、protected environment、同一制品发布与 PyPI 回装等后续硬化与发布动作仍需独立授权。本 Gate 请求不是发布请求。

## 六份报告

- [RC-IDENTITY-AND-VERSION](https://github.com/joinwell52-AI/FCoP/blob/6549a639574d4587a7fa9ffc5f96f4f156b336ba/reports/FCOP-4.0-WP4D-RC-IDENTITY-AND-VERSION.md)
- [ARTIFACT-REPRODUCIBILITY](https://github.com/joinwell52-AI/FCoP/blob/6549a639574d4587a7fa9ffc5f96f4f156b336ba/reports/FCOP-4.0-WP4D-ARTIFACT-REPRODUCIBILITY.md)
- [THIRD-PARTY-ADOPTION](https://github.com/joinwell52-AI/FCoP/blob/6549a639574d4587a7fa9ffc5f96f4f156b336ba/reports/FCOP-4.0-WP4D-THIRD-PARTY-ADOPTION.md)
- [RESILIENCE-AND-COMPATIBILITY](https://github.com/joinwell52-AI/FCoP/blob/6549a639574d4587a7fa9ffc5f96f4f156b336ba/reports/FCOP-4.0-WP4D-RESILIENCE-AND-COMPATIBILITY.md)
- [CI-AND-RELEASE-READINESS](https://github.com/joinwell52-AI/FCoP/blob/6549a639574d4587a7fa9ffc5f96f4f156b336ba/reports/FCOP-4.0-WP4D-CI-AND-RELEASE-READINESS.md)
- [RESULT](https://github.com/joinwell52-AI/FCoP/blob/6549a639574d4587a7fa9ffc5f96f4f156b336ba/reports/FCOP-4.0-WP4D-RESULT.md)

报告中的已完成命令、平台、UTC 时间、计数和制品摘要均指明所属 C。后续 M 的 CI 时序只能由推送后的回执提供；该时序限制没有被手改时间或自引用 SHA 掩盖。

## GitHub 实际 Blob 回读表（E，86/86）

下列 SHA-256 直接来自 GitHub Git blob 解码后的原始字节，逐一与固定 E 的 Git blob 比较；不是工作树推测值。M 不改变这 86 个文件，推送后必须再次核验，另加本 Manifest 自身 1 个文件，共 87/87。原任务书也纳入本表；主工作树与历史资料不在写集内。

| 文件 | bytes | GitHub SHA-256 |
|---|---:|---|
| .github/workflows/rc-candidate.yml | 5136 | 5b391585a27d650df8997f54d48150cfafe66ac23295e8097b987e3a356797aa |
| CHANGELOG.md | 132901 | 08d02ddc0509b723b51c58003fe11bf7a8cd45b25d64a57b1188b37fd2986f12 |
| docs/fcop-4.0/rc-candidate-boundary.md | 1469 | 8cf4906f96fc7b74096a77bba6b2bd4355e8ae72eb4d7fa64747ce514d3e06bb |
| docs/releases/4.0.0rc1.md | 1421 | fd4e62bc39d89c17701f6781bcffbf9b50a95e750689231053185c9563a5eef9 |
| examples/v4/third-party/mcp-only/README.md | 1615 | 83c82a93afee5da73c639bc8542a8b26a0016d7f66e142001c720e5cff8f2c8d |
| examples/v4/third-party/mcp-only/client.py | 9547 | 3675a4ab5c8351352fae27fd1a6353c389f8d3faa69be896e2f5a458a4d3d3f9 |
| examples/v4/third-party/mcp-only/server.py | 1192 | a86c374839944b44d87a157bfa9aea950540a0c5dab2bc14e952057191bf1579 |
| examples/v4/third-party/python-only/README.md | 1707 | 94fe1a0a05808d5265e9646bed6c8b8c6c27c20a0ae49d2e58fd0234f2af957a |
| examples/v4/third-party/python-only/app.py | 12980 | c458bb0a4495b26791adfff10f82a853844ccddd9983b9cd0231ea3170b55902 |
| fcop-README.pypi.md | 2323 | 019dd8c11420e7d9b4e301dacdac42e45246169543bbae6fa785cc7e8b3dbf64 |
| mcp/README.md | 15929 | 2fa393329148df9079a35d17de345b8d43f653fc5d535eb67aa261b64eff57a8 |
| mcp/pyproject.toml | 4861 | 86628c2f21270758a51abac4fc375673d2c6a0c4c4806cf141fa270babff85c8 |
| mcp/src/fcop_mcp/_version.py | 610 | 310a8df396e097eeb5d3d8a0c83e3e2bc8803539ea94f7ecad7efad070a68339 |
| mcp/src/fcop_mcp/routing.py | 3760 | 6f054a99e2b2807b813d0e43e644e8b950a2f63c2d0159d519c6c89bb35fcb8b |
| pyproject.toml | 6077 | c9faa4f794b30ed52fdfc7093e0f0b30f7d8965ec8c8139c94f04eb732c346dc |
| reports/FCOP-4.0-WP4D-ARTIFACT-REPRODUCIBILITY.md | 20117 | fdbb8ad72eef0110b5d966d5885a92d5b9c01d198402c9d8aa6044167e010c7a |
| reports/FCOP-4.0-WP4D-CI-AND-RELEASE-READINESS.md | 21182 | 14d79774b80b29985364bc0683cffacd136192f813b6196062fd184cb6e6d1f4 |
| reports/FCOP-4.0-WP4D-RC-IDENTITY-AND-VERSION.md | 19827 | 2752d43ad62ea95d9d44c6a79661256891610f9e24db61cb66cdc6d4cbb39caa |
| reports/FCOP-4.0-WP4D-RESILIENCE-AND-COMPATIBILITY.md | 23210 | 77cf984b30fc274ea0990b47b287f0fcf7b36910295f0f056b1c3ac36cef0a73 |
| reports/FCOP-4.0-WP4D-RESULT.md | 37404 | f9999862abd167bf87876faa51e5b22eb22c91ec6d4d6272ee0542fdb876e482 |
| reports/FCOP-4.0-WP4D-THIRD-PARTY-ADOPTION.md | 19752 | d6340b0afd3cfeb17a3588e885624686dcfea9a48804aabfe444259231919607 |
| scripts/fcop_rc_candidate_check.py | 3243 | 0a284ca78f5e36d46bbd73ef2113186d90194917a31c33a12a29818b4c8b144c |
| scripts/wp4d_build.py | 7023 | 24264dc82bb9bc44866702d3a48b4294b7d4bab1e6f3f3353eea8bb91ea85483 |
| scripts/wp4d_candidate_ref.py | 1086 | 1205d8a9e960fb7cf5a3347b8f01d508147f6a854004845d6d2ed2b53d836357 |
| scripts/wp4d_consume.py | 9240 | fb6ecfb62b0f7f794f2c792ea21c1e4590a6f0177eb9f4ac05a1a18ca6a1dafe |
| scripts/wp4d_legacy.py | 2191 | 4d3c824b87b19821a56e9579ca035af083ddf5277fb6c95d333abab227d579d1 |
| scripts/wp4d_shadow.py | 4569 | 8fd9ffebb6f1d69a60d44939bc0fc9f10ce3d1b4af9f5e627087a93642f8f0b6 |
| scripts/wp4d_source.py | 1193 | e2ad8fe4d54a6539b40b134fd15e71347274299bdc4280c85e91d7f40aac404b |
| scripts/wp4d_verify_scope.py | 3830 | 79a1f158a6d983f075145bdf4f696c5769bea26276d347cd625be7eb63079217 |
| src/fcop/_version.py | 564 | 14ffc70e19c78e318a2b65b2331dd21ccd3e84913493b1dca5a64079a6b0f3b9 |
| taskbooks/fcop-4.0/WP4D/01-Release-Candidate-and-Third-Party-Adoption-Proof-Taskbook-v1.0.zh.md | 18471 | bfc93f595800efe5185588ff92b612c9ca66e1622118e76c805d5fd908a1e290 |
| tests/rc/evidence/wp4d/baseline-1912.xml | 453008 | 54c07dd75b3208ee41bc51d2b0e1bf7ff4d6cadda0977042ad8ffbf3ccc48f33 |
| tests/rc/evidence/wp4d/content-ci-snapshot.json | 95357 | 51f1bd1cb6ee817530dfa8eb1e0f85c6c284a43be6d75e1f62c77cfb33deb478 |
| tests/rc/evidence/wp4d/final-content/actions-artifacts.json | 15069 | 580e151b26b0724efd2bfb9c8f60122f0556a7b43ddcc0278ef3c9702acaa651 |
| tests/rc/evidence/wp4d/final-content/build.log | 7205 | c57a96946ad3215dc87d7fa421b3509534f84dbd9f8a51911c1a32b53c3c1b2e |
| tests/rc/evidence/wp4d/final-content/candidate-manifest.json | 6978 | 148915cde716d63284950ed46f9250e55b182885b23209cb56ac7d70d5b7dc8c |
| tests/rc/evidence/wp4d/final-content/ci-jobs.json | 172074 | 1f3664865203e368c39c376f91c1d8d12f466d9947dfb1f2dc5a426f2cd0a13a |
| tests/rc/evidence/wp4d/final-content/consumer-results.json | 81829 | b4b849e1f240ede656cece29d287c30a5b43ca8539250cfc20f3e433d8f82bdc |
| tests/rc/evidence/wp4d/final-content/content-remote-readback.json | 10759 | db0b2ef2d2b2e6d927bbea2dceb04cf649504fc92d2aac362e1f185ada56a833 |
| tests/rc/evidence/wp4d/final-content/guard-matrix.json | 3243 | 2a4a080bbf3e50f3a44b7b402cc6117bfacb5cd4afde3b5bb7077690b8ce36d4 |
| tests/rc/evidence/wp4d/final-content/scope.json | 2802 | 88c53c9e5f77eefbebb7018b5f14dcd375b002e6e40592f54353e0a85e0e0f24 |
| tests/rc/evidence/wp4d/final-content/shadow-evidence-review.json | 908 | d7af09778a7246cabc85c5ca55b170a9c35c9e4bc1eed1b0d3ad08e74b8d04b9 |
| tests/rc/evidence/wp4d/final-content/shadow.json | 4681 | e52fbdc6848fc80cb652c23af4b43d37fceb2afd61ced595555b30849fe9252a |
| tests/rc/evidence/wp4d/final-content/source-parity.json | 1791 | 24e3b424616073c8a129dfe2f035c823554bb0e57c58d9fca5ffd72772046016 |
| tests/rc/evidence/wp4d/final-content/targeted-7.xml | 1506 | 042b751c4b02e9d6b82c464a0b46ab2ab22cf6b03255a4178f616bfaa886a419 |
| tests/rc/evidence/wp4d/final-content/ubuntu-full-1931.xml | 455985 | 9e193730e15763ab6423f543198b9b483c89280186374d9ae6666df2c8698fb1 |
| tests/rc/evidence/wp4d/final-content/windows-full-1931.xml | 455985 | 3063c0c684c6d3c3d0895780dbf0a7b7a8ed6adeea61333a283115faa18f39c9 |
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
| tests/rc/evidence/wp4d/socketpair-resume/REPAIR-LEDGER.md | 4606 | d3b645dd825c94c8632981f14aa81d1525b3887cea57b34f109583b82b05f7dd |
| tests/rc/evidence/wp4d/socketpair-resume/build.log | 7097 | bb6c8360b7510a327cbf8b0ba8783f9870863083e45d6e45a01134af61e72ebf |
| tests/rc/evidence/wp4d/socketpair-resume/candidate-manifest.json | 6782 | 2d24d63a9e1bc833053b543adb016dc7801716514fc4fa20a859c7a488252eb6 |
| tests/rc/evidence/wp4d/socketpair-resume/guard-first-count-failure.xml | 4460 | fc889acb560f175105bdd27b59320949f43c069d9edf940e57a604b8641654fd |
| tests/rc/evidence/wp4d/socketpair-resume/guard-local-pass.xml | 406 | 1810ff03fa6d49713847bbeea72e2fec6ab1fdeb5e696639d6f0dbee876a37dc |
| tests/rc/evidence/wp4d/socketpair-resume/mypy-failures.json | 6415 | eb89d5c3cae6c54eec60de78bd1667edf7b85299826321a7be3fa57ca7865d79 |
| tests/rc/evidence/wp4d/socketpair-resume/shadow-change-diagnosis.json | 803 | ca99d5e5f1b88fbd505ef6df3f453e64a8d0f857dbb3598b625f1910acdc0149 |
| tests/rc/evidence/wp4d/socketpair-resume/shadow-final-recheck-failure.json | 1902 | 10a20e0d3f4dba4bc3a412b10667a5c8be3a937f3eb037d4a0f1fec6539c1466 |
| tests/rc/evidence/wp4d/socketpair-resume/shadow-recheck-02-failure.json | 417 | e2111a54e17379f0db46ba0c7f17fd75e6fcfd09183670b8abc296434a93d8f3 |
| tests/rc/evidence/wp4d/socketpair-resume/shadow-recheck-failure.json | 475 | ea2703f690b60b962408cb8646315ec62cd4cf3d8c62c38e4b396e77f6a54361 |
| tests/rc/evidence/wp4d/socketpair-resume/shallow-checkout-failure.log | 1565 | f83a9c56398ff08520f77495132fed2019b933283d5a6a8bd7021025cb930a4c |
| tests/rc/evidence/wp4d/socketpair-resume/ubuntu-full-1925.xml | 454886 | 82169451401613ecb0f8aa6db3d8c9f56fe55033dd1ab575ba491c4d1ccf3863 |
| tests/rc/evidence/wp4d/toolchain-diagnosis.json | 2105 | df2ff21f27f27c6343306ea90037a5e8f2606f7f3938896e0e6f55eab48f4f19 |
| tests/rc/evidence/wp4d/toolchain-resume/actions-artifacts.json | 14166 | 9d4072741abcbf095347af28416c509fe97a81021da836f1e72766ec3fd49bd3 |
| tests/rc/evidence/wp4d/toolchain-resume/build.log | 7097 | f377bbef5d3ae8a9797706ef883d476f1b2fdee14565df58d97ce45f324c496e |
| tests/rc/evidence/wp4d/toolchain-resume/candidate-manifest.json | 6782 | f8bdcdbd1d39278a8ab481ab6e41157525ddcd52bcb9c37ab4e91e5dac3c4ad5 |
| tests/rc/evidence/wp4d/toolchain-resume/ci-jobs.json | 167772 | 58a2c35758b5e659d47fcae357d82da4a6eb157f4cc52ad01d5ff077fa074ffc |
| tests/rc/evidence/wp4d/toolchain-resume/consumer-results.json | 67450 | 782a00cc2551d2114ec1517508ab6ec189ee29639de81537b4ab52e53d591707 |
| tests/rc/evidence/wp4d/toolchain-resume/ubuntu-full-1924.xml | 454732 | 9afb9d7742075450b09bfc5b7edd8a571a61d7a43c6e64eb90016db08c5bd92f |
| tests/rc/evidence/wp4d/toolchain-resume/windows-310-server.log | 2729 | de66e0b3a39e5535edcda3bc5fb22bbfcd7dc78f14573214cddc878a3a3d6daa |
| tests/rc/evidence/wp4d/toolchain-resume/windows-311-server.log | 2877 | 0314719025a2c91ff44c1e228fc26226d3ac432309ddab2fd8c9213dfe7ccc6e |
| tests/rc/evidence/wp4d/ubuntu-content-full-1924.xml | 454732 | 023552fc2549a3c340064a2e215bd898bbf0b3f11ca0304ed23e86bc9822b172 |
| tests/rc/installed_identity.py | 1109 | 6417053c91d55151b6c634fa6254c4e761d4076632141bcd5d7de81454cf2e03 |
| tests/rc/legacy_fixture.py | 3747 | 2971c5311994960e248d766054e8bc74f0c63aeed032bf80638f7f00c405b93c |
| tests/test_fcop/test_audit.py | 12271 | c5ee2802c01085ec6706aa99eec83b510e8a2871d489b0aed8e3ebeedc205c02 |
| tests/test_fcop/test_pyproject_pins.py | 1283 | 45cafdb7f125355d66cb503a3248c0b255e8826343e44894f98d4d1c3462cfc3 |
| tests/test_fcop/test_wp4d_rc_candidate_ref.py | 1928 | 9fff409545b2c4dcb77df3fe9bc12baf057ff4ecd64977d6a1ad65d94401224e |
| tests/test_fcop/test_wp4d_rc_identity.py | 1586 | a5876542335a04a05d7ed315cfd239e14bf58986e90bf5bca479cc2b0a7473f8 |
| tests/test_fcop_mcp/test_wp4d_rc_offline_guard.py | 3092 | 0553db016440ac5ba1bf7dcd88ad6ae9b1782167b6e7dd6636093a20cd902a62 |

---

## 历史 Manifest 原文（旧 BLOCKED 状态不作为当前结论）

# WP4D Manifest — toolchain resumed; Windows sample boundary BLOCKED

## Current receipt

```yaml
wp4d_status: BLOCKED
authorized_scope: WP4D_TWINE_METADATA_2_5_TOOLCHAIN_ONLY_AND_WP4D_RESUME
blocker: WINDOWS_310_311_MCP_SAMPLE_OFFLINE_GUARD_REJECTS_STDLIB_SOCKETPAIR
base_commit: 167c5fd4ca4c9603c392bae3a4a055963e7b7ed6
taskbook_commit: cbdc60a92a02b9e2eb0c1c6e2e93f74c335407f9
taskbook_sha256: bfc93f595800efe5185588ff92b612c9ca66e1622118e76c805d5fd908a1e290
prior_erratum_commit: 22db1377163bb0b1e74c4b94fa1f594b3e762a9d
toolchain_erratum_commit: 086c358f4c96e21aa31890d147eacae4a359a11a
toolchain_erratum_sha256: 03da08ed72ffe438d49a65bb8f87e5b9b2e2e6a917fb8d9cfb945dade02eb2e4
toolchain_erratum_bytes: 7224
toolchain_resume_base: 700e9e1ecb3eb02e5860094175ba7f8099141695
toolchain_fix_commit: b472be32a2623de77d0fb9b2c301960620383e27
candidate_commit: b472be32a2623de77d0fb9b2c301960620383e27
evidence_commit: bbc43524b62046d5c3bb181b4233579bb08cac57
manifest_commit: SELF
manifest_parent: bbc43524b62046d5c3bb181b4233579bb08cac57
target_versions:
  fcop: 4.0.0rc1
  fcop-mcp: 4.0.0rc1
twine_version: 7.0.0
packaging_version: 26.3
metadata_version_observed: "2.5"
twine_checks: 2/2
artifact_reproducibility: 4/4
failed_run_artifacts_reused: false
candidate_manifest_sha256: f8bdcdbd1d39278a8ab481ab6e41157525ddcd52bcb9c37ab4e91e5dac3c4ad5
candidate_actions_run: 34367862396
candidate_artifact_id: 10110629085
source_date_epoch: 1788940367
ubuntu_candidate_full_regression: 1924/1924
ubuntu_failures_errors_skips: 0/0/0
windows_candidate_local_full_regression: INTERRUPTED_NOT_ACCEPTED
legacy_regression: NOT_ACCEPTED_FULL_STAGE
wp4d_tests: INCLUDED_IN_1924_UBUNTU_FULL
existing_ci_applicable: 27/27_AT_CANDIDATE_COMMIT
windows_existing_ci: 8/8_AT_CANDIDATE_COMMIT
pr_only_jobs: 2_NOT_APPLICABLE_NOT_PASSED
rc_consumer_matrix: 10/12
rc_consumer_failures: 2
rc_consumer_skips: 0
rc_windows_consumer_matrix: 2/4
completed_installed_origin_paths: 20/24
mcp_surface: 46/12/4_IN_TEN_SUCCESSFUL_MATRIX_CELLS
canonical_files: 19/19
frozen_bytes: 21/21
frozen_core_conformance_tree: 24ab264c6bca9a3183ee270becb552f22a4c4f9e
frozen_distribution_conformance_tree: 4f99c7261b63b6db81c500604a231defaca9f14b
codeflowmu_shadow: NOT_RUN_THIS_RESUMPTION
final_manifest_head_ci: NOT_CLAIMED_GREEN
content_evidence_remote_readback: 56/56
content_evidence_readback_head: bbc43524b62046d5c3bb181b4233579bb08cac57
content_evidence_readback_utc: 2026-09-09T15:15:41.799061+00:00
delivery_files_including_manifest: 57
final_head_readback_receipt: PR_31_COMMENT_AFTER_PUSH
draft_pr: 31
pr_base: task/fcop-4.0-wp4d-rc-candidate
pr_head: feat/fcop-4.0-wp4d-rc-candidate
main_merge_authorized: false
tag_authorized: false
rc_publish_authorized: false
stable_release_authorized: false
pypi_publish_authorized: false
github_release_authorized: false
mcp_registry_publish_authorized: false
zenodo_publish_authorized: false
codeflowmu_write_authorized: false
requested_gate: NONE
```

## Stop reason

The two-file toolchain correction succeeded: two fresh build directories each
produced four artifacts; Twine passed both sets and all four raw SHA-256 pairs
matched. The downloaded manifest records six exact tool identities including
Twine 7.0.0 and packaging 26.3. Core wheel metadata is valid version 2.5.
No failed-run artifact was reused and no metadata or validation was weakened.

The next failure is in the executor-written MCP adoption sample's offline
audit hook. On Windows Python 3.10 and 3.11, asyncio creates its internal
Proactor self-pipe using stdlib socket.socketpair. That implementation calls
socket.bind from a function named socketpair, while the sample server only
exempts _fallback_socketpair at examples/v4/third-party/mcp-only/server.py:15.
The hook raises at line 17 before MCP initialize completes. This evidence
identifies a sample cross-version isolation boundary defect, not a demonstrated
Core/MCP protocol failure.

The original taskbook section 13.2 and current erratum section 8 require
stopping on an applicable matrix failure or a change outside the two-file
allowlist. No sample/network-guard fix was made, no Core/MCP/Conformance/Schema
was modified, and network access was not relaxed. Request ADMIN's targeted
ruling for a narrowly safe standard-library socketpair compatibility fix.
Do not sign or request FCOP_4_RC_ACCEPTED.

## Fixed results and limitations

| Workflow at candidate commit | Result |
|---|---|
| [Core 34367862474](https://github.com/joinwell52-AI/FCoP/actions/runs/34367862474) | 14 applicable jobs passed |
| [MCP 34367862401](https://github.com/joinwell52-AI/FCoP/actions/runs/34367862401) | 13 applicable jobs passed |
| [RC 34367862396](https://github.com/joinwell52-AI/FCoP/actions/runs/34367862396) | Build/source passed; consumers 10 passed, 2 failed |

Ubuntu full JUnit records 1924 tests, zero failures/errors/skips, 103.370 seconds
starting 2026-09-09T15:05:18.595592+00:00. Both public source clients also passed.
The 27 existing applicable jobs and 8 existing Windows jobs are results of the
new candidate commit, not the old blocked head and not SELF. Two PR-only skips
are N/A, never counted as passed.

The ten complete consumer cells cover all four Ubuntu versions, all four macOS
versions, and Windows 3.12/3.13. Each ran both wheel and sdist installation
outside checkout, both public clients, process reopen/retry, Host operations,
legacy zero-drift and mismatch checks against identical first-set artifacts.
Their twenty origin paths are complete. Windows 3.10/3.11 fail in wheel MCP
startup; downstream checks and sdist paths in those cells were not completed.
Do not infer 24/24 from 20/24.

Native Windows full regression was started against b472be3, then the verified
pytest process was stopped at 2026-09-09T23:09:34.2242519+08:00 after the matrix
blocker. Exit 1 was executor termination, not an observed assertion failure.
No final full JUnit was produced; previous blocked-head 1924/1924 is not reused.
This resumption's CodeFlowMu shadow was not executed. All these incomplete
requirements remain explicit. Final Manifest HEAD CI is not claimed green.

## Verified first-set artifacts

Build Python 3.12.14, Ubuntu; build interval
2026-09-09T15:05:05.613250+00:00 to 2026-09-09T15:05:10.914881+00:00.
Tools: build 1.4.2, hatchling 1.32.0, setuptools 82.0.1, wheel 0.45.1,
twine 7.0.0, packaging 26.3. Both Twine groups exit 0; raw equality 4/4.

| File | Bytes | Remote first-set SHA-256 |
|---|---:|---|
| fcop-4.0.0rc1-py3-none-any.whl | 726280 | b539fdd496d52ea608b5f42abd270c2ed04e8f011242d932ddedac48f8d7cee9 |
| fcop-4.0.0rc1.tar.gz | 647881 | 43e4488af52bffac3e400c14f442136f955ee0477ddf0e94386481e6ec682bb4 |
| fcop_mcp-4.0.0rc1-py3-none-any.whl | 117937 | 20167b314de1a90093b74cf42c7039edceddc1458e1b37ce3e9e6f31697c773a |
| fcop_mcp-4.0.0rc1.tar.gz | 109420 | eefde60b6d156f5ef2184186f5f5a355837f0fc9e0244b3e2d8077dbed51000b |

[Actions candidate artifact](https://github.com/joinwell52-AI/FCoP/actions/runs/34367862396/artifacts/10110629085)
ZIP digest: 334c8b7293c22857e258075766228733394029833e949e01b192fb4b831ca8f9.
Expires 2026-12-08T15:04:47Z. This validation attachment is not a Release or
public RC. The ZIP digest is not a substitute for the four hashes above.

## Additive chain and preserved history

The [previous Manifest at 700e9e1](https://github.com/joinwell52-AI/FCoP/blob/700e9e1ecb3eb02e5860094175ba7f8099141695/reviews/fcop-4.0/wp4d/MANIFEST.md)
preserves the full earlier chain and both historical blocker facts.

```text
700e9e1ecb3eb02e5860094175ba7f8099141695 previous blocked delivery
 -> b472be32a2623de77d0fb9b2c301960620383e27 two-file toolchain fix only
 -> bbc43524b62046d5c3bb181b4233579bb08cac57 six reports + eight evidence files
 -> SELF Manifest only
```

The fixed erratum is authority, not a merged implementation branch. No history
was rewritten. All six prior reports are retained verbatim under history
headings, including old JUnit, Twine failure and original audit-guard blocker.
The original D:/FCoP worktree, existing workspaces, main and CodeFlowMu were not
modified; no tag, registry upload or release action was performed.

## Remote delivery hashes

The following 56 files were individually read via GitHub Git Blob API at
evidence commit bbc43524b62046d5c3bb181b4233579bb08cac57. Their complete bytes
matched local committed blobs; these are the observed remote SHA-256 values.
The authority taskbook is listed above and not counted as candidate delivery.
SELF changes only this Manifest. After push, all 57 files, parent chain and
Manifest self-hash are verified again at final HEAD and recorded in PR #31.
The six reports provide detailed commands, timestamps and evidence sources.

| File | Bytes | Remote SHA-256 |
|---|---:|---|
| .github/workflows/rc-candidate.yml | 4899 | f1f8982697e955d4d8eaca9ca004e41b1522c58ad88af008bc9a7ca819af29f4 |
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
| reports/FCOP-4.0-WP4D-ARTIFACT-REPRODUCIBILITY.md | 11648 | 896ea1110b84b58ab2891cefaf8cf9ae54b8100c63c258aa7dfca794d9c40461 |
| reports/FCOP-4.0-WP4D-CI-AND-RELEASE-READINESS.md | 12251 | 0009a8b9d29947c0fd1b1526a80293fa4a4573ebba1145bec4612eccca6d0e85 |
| reports/FCOP-4.0-WP4D-RC-IDENTITY-AND-VERSION.md | 11445 | cdf1b11104e53fd8a8a2f0211f86e7716fd1e5bbac7398b44ed082a70139c3ce |
| reports/FCOP-4.0-WP4D-RESILIENCE-AND-COMPATIBILITY.md | 14076 | 77ae52dfa90ac03da8422cf366647bdabb91af7de5661b6060cd476fc5beac04 |
| reports/FCOP-4.0-WP4D-RESULT.md | 25524 | b8e5bfc59c5727c9a51579b9f8e8c32744fb0ec1f05037b116a4fcfc026f03ce |
| reports/FCOP-4.0-WP4D-THIRD-PARTY-ADOPTION.md | 11034 | f7055ced07a008d873518fe9a619e1a46d94a6a63911dd33ebbd9d68f18e4ca2 |
| scripts/fcop_rc_candidate_check.py | 3243 | 0a284ca78f5e36d46bbd73ef2113186d90194917a31c33a12a29818b4c8b144c |
| scripts/wp4d_build.py | 6656 | 061217a3690ffec52da90f6168744b4d6a9112583e7032cfa7d892be91c22a29 |
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
| tests/rc/evidence/wp4d/toolchain-resume/actions-artifacts.json | 14166 | 9d4072741abcbf095347af28416c509fe97a81021da836f1e72766ec3fd49bd3 |
| tests/rc/evidence/wp4d/toolchain-resume/build.log | 7097 | f377bbef5d3ae8a9797706ef883d476f1b2fdee14565df58d97ce45f324c496e |
| tests/rc/evidence/wp4d/toolchain-resume/candidate-manifest.json | 6782 | f8bdcdbd1d39278a8ab481ab6e41157525ddcd52bcb9c37ab4e91e5dac3c4ad5 |
| tests/rc/evidence/wp4d/toolchain-resume/ci-jobs.json | 167772 | 58a2c35758b5e659d47fcae357d82da4a6eb157f4cc52ad01d5ff077fa074ffc |
| tests/rc/evidence/wp4d/toolchain-resume/consumer-results.json | 67450 | 782a00cc2551d2114ec1517508ab6ec189ee29639de81537b4ab52e53d591707 |
| tests/rc/evidence/wp4d/toolchain-resume/ubuntu-full-1924.xml | 454732 | 9afb9d7742075450b09bfc5b7edd8a571a61d7a43c6e64eb90016db08c5bd92f |
| tests/rc/evidence/wp4d/toolchain-resume/windows-310-server.log | 2729 | de66e0b3a39e5535edcda3bc5fb22bbfcd7dc78f14573214cddc878a3a3d6daa |
| tests/rc/evidence/wp4d/toolchain-resume/windows-311-server.log | 2877 | 0314719025a2c91ff44c1e228fc26226d3ac432309ddab2fd8c9213dfe7ccc6e |
| tests/rc/evidence/wp4d/ubuntu-content-full-1924.xml | 454732 | 023552fc2549a3c340064a2e215bd898bbf0b3f11ca0304ed23e86bc9822b172 |
| tests/rc/installed_identity.py | 1109 | 6417053c91d55151b6c634fa6254c4e761d4076632141bcd5d7de81454cf2e03 |
| tests/rc/legacy_fixture.py | 3747 | 2971c5311994960e248d766054e8bc74f0c63aeed032bf80638f7f00c405b93c |
| tests/test_fcop/test_audit.py | 12271 | c5ee2802c01085ec6706aa99eec83b510e8a2871d489b0aed8e3ebeedc205c02 |
| tests/test_fcop/test_pyproject_pins.py | 1283 | 45cafdb7f125355d66cb503a3248c0b255e8826343e44894f98d4d1c3462cfc3 |
| tests/test_fcop/test_wp4d_rc_identity.py | 1586 | a5876542335a04a05d7ed315cfd239e14bf58986e90bf5bca479cc2b0a7473f8 |
