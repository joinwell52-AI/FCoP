# WP4A.1 artifact proof

## Final artifacts (not published)

Build directory: `D:/FCoP-wp4a1-artifact-proof/final-lf-dist`. Package version deliberately remains 3.2.5; schema revision 4.0.0 is not a package release.

| Artifact | SHA-256 |
|---|---|
| fcop-3.2.5-py3-none-any.whl | 6fa453ec502f6c52e0754ae7527ae3e03cf5885542ed9cb1ef6b7592755ade2b |
| fcop-3.2.5.tar.gz | b8df886de41c37f2f19e237382d1917139ff45e01e6f052b57e421df529f3f21 |

Command: `D:/FCoP-wp4a1-artifact-proof/build-env/Scripts/python.exe -m build --no-isolation --outdir D:/FCoP-wp4a1-artifact-proof/final-lf-dist` from the independent worktree. build 1.6.0 / hatchling 1.32.0 successfully built sdist and then wheel from that sdist. Earlier development artifacts remain separate under `dist` and `final-dist`; they are not delivery artifacts. Final source LF normalization caused a rebuild so these hashes describe delivery bytes.

## Inventory and byte proof

Both archives contain 20 schema files: the unchanged eight historical schemas plus twelve v4 schemas. Wheel prefix: `fcop/_data/schemas/`; sdist prefix: `fcop-3.2.5/src/fcop/_data/schemas/`.

| Historical names | v4 names (under v4/) |
|---|---|
| agent.schema.json | authorization-binding.schema.json |
| boundary.schema.json | create-operation.schema.json |
| encoding.schema.json | create-request-canonical.schema.json |
| event.schema.json | family-canonical.schema.json |
| failure.schema.json | issue.schema.json |
| ipc-envelope.schema.json | lifecycle-receipt.schema.json |
| review.schema.json | recovery-observation.schema.json |
| skill.schema.json | report.schema.json |
| — | review.schema.json |
| — | task.schema.json |
| — | transition.schema.json |
| — | workspace.schema.json |

Python zipfile/tarfile reads asserted count 20 in each artifact and compared all twelve v4 members byte-for-byte with `src/fcop/_data/schemas/v4`. Result: wheel 12/12, sdist 12/12. Deterministic generation also compares package copies with spec copies. Final installed hashes:

| v4 basename | SHA-256 |
|---|---|
| authorization-binding | d58987e4c353adcae73bac26136db8a1f2ce8c4b5694e78cb21e2e97bcd43b86 |
| create-operation | eab9c43684fb6a8999d3d0c643a4402f4296a2a21103d4a3e5f318c665494a01 |
| create-request-canonical | 2fdad6ed19cb53728521353a297aabaf02a599f6f276661564406e68bc267197 |
| family-canonical | 6f31f5e1784b08706b237e75cb4cf496b0d9847b809683810f86d422acc110eb |
| issue | 78830cc2c25f5a71f23e1e707c3801ec279ab51d0a7a8b8a6222b5a26d22c56b |
| lifecycle-receipt | 41f38ff99672b1238c6d384499856c8c6af48bae0fffd74da93a56d4fcc495a2 |
| recovery-observation | f8ef752dd58cc8716684919f9672112cb2282f8529fa5a6db151361d4c09dd99 |
| report | 1a8de72da2870beca3a09af91aec48cf697d5a8c4d694b42f8d5cc0a001d19fc |
| review | e07dbbbec4d100d6ab57db46057553896ebacbff55dd4567721408a33084f21a |
| task | c3ec36ec5577fb07d05d69a7fc0f533594c6c4e5ed36376cc01092af4c69610f |
| transition | b223a0dd5cbf634bbdd40b3364501522f8417c987bef97732c3c93786946e801 |
| workspace | 775c2f5516d49f42fabf84a058fdf85298f4e9dcedc91d182a7e0678f2d0f0aa |

## Clean offline installation and external applications

Dependencies were downloaded into a wheelhouse in a separate preparation step (network used **only in preparation**, not claimed offline). A new clean venv then used:

```text
python -m pip install --no-index --find-links D:/FCoP-wp4a1-artifact-proof/wheelhouse D:/FCoP-wp4a1-artifact-proof/final-dist/fcop-3.2.5-py3-none-any.whl
python -m pip install --no-index --no-deps --force-reinstall D:/FCoP-wp4a1-artifact-proof/final-lf-dist/fcop-3.2.5-py3-none-any.whl
python D:/FCoP-wp4a1-machine-contract/examples/v4/artifact_smoke.py
```

Both commands used `D:/FCoP-wp4a1-artifact-proof/clean-env/Scripts/python.exe`, cwd `D:/FCoP-wp4a1-artifact-proof`, and PYTHONPATH containing **only** `examples/v4/offline_guard`. That sitecustomize audit hook rejects network connects and DNS in all descendant interpreters. fcop imported from `D:/FCoP-wp4a1-artifact-proof/clean-env/Lib/site-packages/fcop/__init__.py`, not the checkout. No source-tree fallback or system-site-packages was used.

Installed runtime: fcop 3.2.5, PyYAML 6.0.3, jsonschema 4.26.0, attrs 26.1.0, jsonschema-specifications 2025.9.1, referencing 0.37.0, rpds-py 2026.6.3, typing-extensions 4.16.0. These resolve the existing two runtime requirements; none was added to project dependencies.

Loader discovered all twelve schemas after the final LF-normalized wheel was reinstalled into the isolated environment. Sequential result: TASK-69625216af5e4a339d7299acac8205e9, archive, 5 events, file SHA-256 `6c8e4524f40ce8aeaed83223148524816502fa2f560d9c490024bb6eb2a7c313`. Family Root: TASK-e85f9637ba8740a4a329f95eccac05fa, archive, 5 events, SHA-256 `0f78a9f335431d1f7beddcc1a1a057b774f06af66212b1d43bfbbe615c7589d8`. Both restarted in separate interpreters and passed.

These are local Windows/Python 3.12 artifact proofs, not a substitute for remote multi-platform CI. Artifact/venv directories are outside both user workspaces and remain available for inspection. Example temporary workspaces were removed by their own TemporaryDirectory context; no user data was removed. Nothing was uploaded to PyPI or released.
