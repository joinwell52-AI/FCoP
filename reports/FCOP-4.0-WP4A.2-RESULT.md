# WP4A.2 result and delivery boundary

## Local result

Scope: `WP4A_2_ONLY`. Executor: ME (solo). ADMIN alone can sign `WP4A_MACHINE_CONTRACT_ACCEPTED`.

Taskbook commit `7e2dcd3cc45f043c7981e7e5b79a78505ec109e8`, verified SHA-256 `5caf02c25bd8a02989151066a801dfd83eef117d0342d3b01e5e7a885cd5adba`; input `6ff8f213313c1f802e3498d2196b8c3bd363ceb5`. Execution: `D:/FCoP-wp4a2-ci-closeout`, branch `review/fcop-4.0-wp4a.1-machine-contract`, existing [Draft PR #14](https://github.com/joinwell52-AI/FCoP/pull/14).

Seven Conformance files received only the taskbook's mechanical Ruff fixes. One workflow SECTION assignment was corrected without changing CHANGELOG or any gate threshold. See [diagnosis](FCOP-4.0-WP4A.2-CI-GATE-DIAGNOSIS.md) for the ten original diagnostics, old failed job URLs, 90 preserved assertions, exact AST comparison and the retained CRLF checkout failure.

Canonical-byte verification tree: `D:/FCoP-wp4a2-lf-verification`, same taskbook base and byte-identical filtered eight-file diff. Local platform is Windows / Python 3.12; these results do not stand in for native Linux/macOS CI.

| Command / proof | Observed result |
|---|---|
| `python -m ruff check src tests` | PASS, 10 original diagnostics to 0 |
| `python -m mypy src/fcop` | PASS, 40 source files |
| `python -m pytest tests/conformance/v4 --collect-only -q` | 119 nodes, exact ordered equality with baseline |
| `python -m pytest tests/conformance/v4 -q` | 119 passed, 0 skipped/xfail; LF verification rerun 60.56s |
| `python -m pytest tests/test_fcop -q` | 1190 passed, 3 existing warnings, 338.20s; canonical LF verification tree |
| `python -m pytest tests/test_fcop_mcp -q` | 80 passed, 38.40s |
| `python -m pytest tests/test_fcop/test_public_surface.py -q` | 4 passed, drift 0 |
| `python spec/schemas/v4/generate.py --check` | 12/12 pairs verified in LF tree |
| Schema Binding SB-01 through SB-10 | PASS, unchanged test_v4_schema.py: 47/47 within the complete 1190/1190 library run |
| Contract ID extraction vs fixed taskbook sources | 60/60 unchanged |
| Assertions removed / skip-xfail added / test names changed / expectations changed | 0 / 0 / 0 / 0 |
| Charter actual CHANGELOG / two negative cases | PASS / 2 of 2 correctly rejected |

MCP invocation set `PYTHONPATH=D:/FCoP-wp4a2-ci-closeout/src;D:/FCoP-wp4a2-ci-closeout/mcp/src` to test the authorized checkout rather than a previously installed adapter. Existing deprecation warnings for Traversable and RefResolver remain warnings; no ignore configuration was added.

## Minimal applications and artifact verification

Unchanged `examples/v4/application.py sequential` and `family` were run through the public Project API with source imports. Both Root tasks reached archive and were reopened in another interpreter with five lifecycle events. Only their own TemporaryDirectory workspaces were used.

A fresh clean venv was created under `D:/FCoP-wp4a2-artifact-proof/clean-env`. The preserved WP4A.1 wheel was first independently hashed and installed offline from the existing wheelhouse: its twelve Schema members matched canonical source bytes. Its forty Python modules matched fixed source after checkout newline normalization (34 retained historical CRLF), so this intermediate check is not claimed as raw byte identity for Python sources.

For the final proof, new artifacts were built directly from the canonical LF verification tree, with the authorized eight-file patch applied:

```text
D:/FCoP-wp4a1-artifact-proof/build-env/Scripts/python.exe -m build --no-isolation --outdir D:/FCoP-wp4a2-artifact-proof/dist
```

Build produced an sdist and then a wheel from that sdist. No build config, version or dependency was changed, and nothing was published.

| Fresh artifact | SHA-256 |
|---|---|
| fcop-3.2.5-py3-none-any.whl | be50090ca05d661f676d4f1f12832f3edb3c94b344ebc5ed8fb8c3d7a2a84818 |
| fcop-3.2.5.tar.gz | 05ffea6d853b4c4130adbaf36d23d060bd0388f2cf77a6bff83a5665de1c1b3f |

zipfile/tarfile byte comparisons verified all twelve v4 Schema files against canonical source and package copies in both artifacts. Every Python module in the fresh wheel exactly matches the LF verification tree; no newline normalization was used for this final equality check.

The fresh wheel was reinstalled in the isolated venv with `--no-index --no-deps --force-reinstall`. `PYTHONPATH` contained only the existing `examples/v4/offline_guard`, not src; cwd was the external artifact directory. The unchanged `artifact_smoke.py` checks an actual site-packages import, all twelve loaded validators and both restarted application modes under the network-blocking audit hook.

Final fresh-wheel smoke result: PASS. Import path was `D:/FCoP-wp4a2-artifact-proof/clean-env/Lib/site-packages/fcop/__init__.py`. All twelve validator hashes matched source/package bytes. Sequential task `TASK-078d8389a3644b77b9e3a585ac7c0049` reopened in archive with five events, SHA-256 `fe50b4bd5211834455d0cb61575486a654a841874e6fc290d3364ca1fbf840d0`. Family Root `TASK-2206e3e7391947fb8e407bc8a2467302` reopened in archive with five events, SHA-256 `b4cbbce64677a75f2d0504260f3a5d944665a06ec6867d7bbd9aa750d3e0635f`.

## Two-commit delivery and final CI receipt

Content Commit will contain only seven mechanical test files, one workflow and the two new reports (ten files). Its child Manifest Commit will add only `reviews/fcop-4.0/wp4a.2/MANIFEST.md` (eleven total delivery files). Exact commit values and ten content SHA-256 values are in that Manifest. The Manifest identifies its own containing commit as SELF; its own file hash is independently returned in the post-push receipt, avoiding self-reference.

At report sealing, remote final-HEAD CI has **not yet run**. This report deliberately does not claim remote PASS in advance. The final receipt must verify the pushed Manifest HEAD and all eleven files through GitHub blob readback, then use `gh run list --commit <Manifest SHA>` and the job records to determine the actual Gate request. Old CI success is not reused, nor is the PR merge-test SHA confused with the submitted head SHA.

Required final-HEAD checks: test-fcop twelve OS/Python jobs, Coverage, Stability Charter and package; test-fcop-mcp twelve OS/Python jobs, tool contract and package. Any failed, cancelled, missing or unexpectedly skipped check means BLOCKED and `REQUESTED_GATE: NONE`; no broader repair is authorized. Only all-green final CI plus verified delivery permits requesting `WP4A_MACHINE_CONTRACT_ACCEPTED`.

## Preserved boundaries

Frozen spec files modified: 0. Schema files modified: 0. Production files modified: 0. MCP implementation modified: 0. CodeFlowMu modified: 0. Workflow files modified: 1 (one line). CHANGELOG modified: 0. Test logic modified: 0. Main modified: false. Release created: false. WP4B started: false.

Original D:/FCoP and prior WP4A.1 file contents remain intact; no migration, redeploy, cleanup or force-push. Pre-delivery remote main was `68dbeb15f4e7f84e1d03f907be9fa66c2265843e`; only the designated review ref may be pushed. Existing reports and failed CI records remain preserved. On final CI success or a new blocker, stop and leave acceptance to ADMIN.
