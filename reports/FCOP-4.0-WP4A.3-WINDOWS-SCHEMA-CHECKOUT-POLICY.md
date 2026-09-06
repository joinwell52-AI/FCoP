# WP4A.3 Windows Schema checkout policy

## Authority and solo execution review

Executor: ME; ADMIN retains Gate authority. The fixed taskbook is the decision document; this report records implementation evidence. Authorized scope is WP4A_3_ONLY.

- Fixed GitHub taskbook: `db4c99806e797a563541381e376c7c62e13f8da0:taskbooks/fcop-4.0/WP4A.3/01-Windows-Schema-LF-Checkout-Contract-Closeout-Taskbook-v1.0.zh.md`.
- Raw blob SHA-256 verified: `a1dac079f1744eb97ab15bcfa56088dac656b8843454dc49ae01ca36dbe045ee`.
- Direct input parent: `2ef95e5afdabfc7aa25a93fb287827682b467c9d`.
- GitHub PR #14 readback before work: HEAD exactly the fixed taskbook SHA, draft=true, branch `review/fcop-4.0-wp4a.1-machine-contract`.
- New execution tree: `D:/FCoP-wp4a3-checkout-policy`. Previous clean WP4A.2 tree was detached at its unchanged HEAD to release the branch, then the branch fast-forwarded to the taskbook. No previous file or delivery history was rewritten.
- Plan checked against the taskbook before editing: exactly two attribute rules, no existing file edits; preserve 24 schema blobs; test a newly checked-out committed policy with the machine's unchanged autocrlf setting; seal two reports, then a separate Manifest. Stop on any new failure.

## Four Windows failures, not a Python 3.10-only failure

Read all jobs from [preserved run 34017767680](https://github.com/joinwell52-AI/FCoP/actions/runs/34017767680), and separately read each of the four Windows job logs.

| Python | Job | Result | Test summary |
|---|---|---|---|
| 3.10 | [101444526767](https://github.com/joinwell52-AI/FCoP/actions/runs/34017767680/job/101444526767) | failure | 1189 passed / 1 failed, 60.67s |
| 3.11 | [101444526592](https://github.com/joinwell52-AI/FCoP/actions/runs/34017767680/job/101444526592) | failure | 1189 passed / 1 failed, 95.55s |
| 3.12 | [101444526626](https://github.com/joinwell52-AI/FCoP/actions/runs/34017767680/job/101444526626) | failure | 1189 passed / 1 failed, 114.60s |
| 3.13 | [101444526582](https://github.com/joinwell52-AI/FCoP/actions/runs/34017767680/job/101444526582) | failure | 1189 passed / 1 failed, 84.80s |

All four logs identify `tests/test_fcop/test_v4_schema.py::test_schema_parity_ids_offline_and_required_negative_matrix`. Each stderr lists precisely 24 paths: twelve under `spec/schemas/v4` and twelve under `src/fcop/_data/schemas/v4`. These counts were computed from each log's Schema drift line, not inferred from the representative job.

The eight Ubuntu/macOS matrix jobs, Coverage and Stability Charter succeeded. Library package job 101444865354 was skipped because of the failed matrix. [MCP run 34017767652](https://github.com/joinwell52-AI/FCoP/actions/runs/34017767652) succeeded. These are preserved baseline facts, not final-head CI evidence.

## Exact policy and boundary proof

The only product-side addition is `.gitattributes`, containing exactly:

```gitattributes
spec/schemas/v4/*.schema.json text eol=lf
src/fcop/_data/schemas/v4/*.schema.json text eol=lf
```

No blanket JSON/Python/Markdown rule, binary/-text flag, working-tree-encoding, or global Git setting was introduced.

`git check-attr text eol -- spec/schemas/v4/workspace.schema.json src/fcop/_data/schemas/v4/workspace.schema.json spec/schemas/agent.schema.json` returned:

| Path | text | eol |
|---|---|---|
| spec/schemas/v4/workspace.schema.json | set | lf |
| src/fcop/_data/schemas/v4/workspace.schema.json | set | lf |
| spec/schemas/agent.schema.json (outside scope) | unspecified | unspecified |

The strict generator remains unmodified: it encodes canonical JSON with final LF and compares raw `read_bytes()`. No normalization is added to the validator or tests.

## Fresh committed-policy checkout proof

Step 4's old-tree check was run after adding the attribute file. It still failed with the same 24 Schema drift paths because those files had already been checked out as CRLF. That result is retained and was not repaired in place.

To make clean-checkout evidence available before sealing the two reports, a **local-only verification snapshot commit** was created with Git write-tree/commit-tree from the staged attribute file:

```text
a15a0376c394f034031e3fa5580cc7ec32ac3225
parent: db4c99806e797a563541381e376c7c62e13f8da0
only added path: .gitattributes
```

Then the following fresh Windows checkout was created, without any autocrlf override:

```text
git worktree add --detach D:/FCoP-wp4a3-clean-windows a15a0376c394f034031e3fa5580cc7ec32ac3225
git config --get core.autocrlf
# true
python spec/schemas/v4/generate.py --check
# 12 schema pairs: verified
```

This is not the old pre-normalized WP4A.2 LF tree. The committed attribute rules performed the checkout. Before tests, all 24 fresh files had zero CRLF and exactly matched INPUT_HEAD Git blob bytes; all twelve source/package pairs were byte-identical. No schema generator write mode or manual conversion was run.

The snapshot is solely a local test fixture, retained by the detached verification worktree. It is not pushed, merged or used as a parent of the Content Commit. The two delivery commits descend directly from the fixed taskbook. Content differs from this validated policy tree only by the two new reports; the Manifest adds evidence only. This avoids either a third delivery commit or amending published history.

## Complete 24-file immutable inventory

The following Git blob IDs and SHA-256 values were captured from INPUT_HEAD. The local committed-policy snapshot has identical blob IDs and bytes. Final Content/Manifest and remote readback must retain every entry with zero drift.

| Repository path | Git blob ID | SHA-256 |
|---|---|---|
| `spec/schemas/v4/authorization-binding.schema.json` | `be3a4d44b8f112fa292404ca50acbede9b38dcc6` | `d58987e4c353adcae73bac26136db8a1f2ce8c4b5694e78cb21e2e97bcd43b86` |
| `spec/schemas/v4/create-operation.schema.json` | `cd8b90cf80c9f72380267d37be8b56fe010225e3` | `eab9c43684fb6a8999d3d0c643a4402f4296a2a21103d4a3e5f318c665494a01` |
| `spec/schemas/v4/create-request-canonical.schema.json` | `ab7083ca253e80bc04aafbbf83b7abc11f3e7ad3` | `2fdad6ed19cb53728521353a297aabaf02a599f6f276661564406e68bc267197` |
| `spec/schemas/v4/family-canonical.schema.json` | `8db381ecb33519abca4e87d4f003c0d3d3cfab66` | `6f31f5e1784b08706b237e75cb4cf496b0d9847b809683810f86d422acc110eb` |
| `spec/schemas/v4/issue.schema.json` | `9cc0ac3e4f4d19cb6925d8ad02a8211e9e9faab3` | `78830cc2c25f5a71f23e1e707c3801ec279ab51d0a7a8b8a6222b5a26d22c56b` |
| `spec/schemas/v4/lifecycle-receipt.schema.json` | `0bc3c115a4c2c7b168674acf682725165cb079b3` | `41f38ff99672b1238c6d384499856c8c6af48bae0fffd74da93a56d4fcc495a2` |
| `spec/schemas/v4/recovery-observation.schema.json` | `ab243c9b0a3dc705c96dd20efbc85370a66064de` | `f8ef752dd58cc8716684919f9672112cb2282f8529fa5a6db151361d4c09dd99` |
| `spec/schemas/v4/report.schema.json` | `eeccb337bc4c3d45ed65bae4adc2e2d7d3be15e4` | `1a8de72da2870beca3a09af91aec48cf697d5a8c4d694b42f8d5cc0a001d19fc` |
| `spec/schemas/v4/review.schema.json` | `2769a03a988ceb289a15c04563edb44bbecb4326` | `e07dbbbec4d100d6ab57db46057553896ebacbff55dd4567721408a33084f21a` |
| `spec/schemas/v4/task.schema.json` | `af80ddaf2af9479b59ec9928cab864512c16baa6` | `c3ec36ec5577fb07d05d69a7fc0f533594c6c4e5ed36376cc01092af4c69610f` |
| `spec/schemas/v4/transition.schema.json` | `430f9bc40cca9a56e0c4bcb4660e0c7341595bf5` | `b223a0dd5cbf634bbdd40b3364501522f8417c987bef97732c3c93786946e801` |
| `spec/schemas/v4/workspace.schema.json` | `7b02b87bf3b75d8cea719f559e6ddb14e4ac1596` | `775c2f5516d49f42fabf84a058fdf85298f4e9dcedc91d182a7e0678f2d0f0aa` |
| `src/fcop/_data/schemas/v4/authorization-binding.schema.json` | `be3a4d44b8f112fa292404ca50acbede9b38dcc6` | `d58987e4c353adcae73bac26136db8a1f2ce8c4b5694e78cb21e2e97bcd43b86` |
| `src/fcop/_data/schemas/v4/create-operation.schema.json` | `cd8b90cf80c9f72380267d37be8b56fe010225e3` | `eab9c43684fb6a8999d3d0c643a4402f4296a2a21103d4a3e5f318c665494a01` |
| `src/fcop/_data/schemas/v4/create-request-canonical.schema.json` | `ab7083ca253e80bc04aafbbf83b7abc11f3e7ad3` | `2fdad6ed19cb53728521353a297aabaf02a599f6f276661564406e68bc267197` |
| `src/fcop/_data/schemas/v4/family-canonical.schema.json` | `8db381ecb33519abca4e87d4f003c0d3d3cfab66` | `6f31f5e1784b08706b237e75cb4cf496b0d9847b809683810f86d422acc110eb` |
| `src/fcop/_data/schemas/v4/issue.schema.json` | `9cc0ac3e4f4d19cb6925d8ad02a8211e9e9faab3` | `78830cc2c25f5a71f23e1e707c3801ec279ab51d0a7a8b8a6222b5a26d22c56b` |
| `src/fcop/_data/schemas/v4/lifecycle-receipt.schema.json` | `0bc3c115a4c2c7b168674acf682725165cb079b3` | `41f38ff99672b1238c6d384499856c8c6af48bae0fffd74da93a56d4fcc495a2` |
| `src/fcop/_data/schemas/v4/recovery-observation.schema.json` | `ab243c9b0a3dc705c96dd20efbc85370a66064de` | `f8ef752dd58cc8716684919f9672112cb2282f8529fa5a6db151361d4c09dd99` |
| `src/fcop/_data/schemas/v4/report.schema.json` | `eeccb337bc4c3d45ed65bae4adc2e2d7d3be15e4` | `1a8de72da2870beca3a09af91aec48cf697d5a8c4d694b42f8d5cc0a001d19fc` |
| `src/fcop/_data/schemas/v4/review.schema.json` | `2769a03a988ceb289a15c04563edb44bbecb4326` | `e07dbbbec4d100d6ab57db46057553896ebacbff55dd4567721408a33084f21a` |
| `src/fcop/_data/schemas/v4/task.schema.json` | `af80ddaf2af9479b59ec9928cab864512c16baa6` | `c3ec36ec5577fb07d05d69a7fc0f533594c6c4e5ed36376cc01092af4c69610f` |
| `src/fcop/_data/schemas/v4/transition.schema.json` | `430f9bc40cca9a56e0c4bcb4660e0c7341595bf5` | `b223a0dd5cbf634bbdd40b3364501522f8417c987bef97732c3c93786946e801` |
| `src/fcop/_data/schemas/v4/workspace.schema.json` | `7b02b87bf3b75d8cea719f559e6ddb14e4ac1596` | `775c2f5516d49f42fabf84a058fdf85298f4e9dcedc91d182a7e0678f2d0f0aa` |

```yaml
V4_SCHEMA_FILES: 24
V4_SCHEMA_BLOB_DRIFT: 0
V4_SCHEMA_SHA256_DRIFT: 0
SOURCE_PACKAGE_SCHEMA_PARITY: 12/12
CLEAN_WINDOWS_CHECKOUT_CRLF_FILES: 0
```

## Verification and preservation

Commands and test results are in the companion RESULT. No Schema, generator, test, workflow, production, MCP, frozen spec, CHANGELOG, dependency, version, main or CodeFlowMu file was edited. The old WP4A.1/WP4A.2 reports and Manifest remain unchanged.

Final acceptance depends on all checks at the new Manifest HEAD: Windows 4/4, Ubuntu/macOS 8/8, Coverage, Stability Charter, the restored library package job, and the entire MCP workflow. The taskbook's intermediate CI is not reusable. A failure or unexpected skip requires BLOCKED; no further repair or WP4B work is authorized.
