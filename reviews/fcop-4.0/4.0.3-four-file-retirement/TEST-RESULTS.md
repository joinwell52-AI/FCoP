# 4.0.3 test results

Local environment: dedicated Windows Python 3.12 environment with editable fcop/fcop-mcp 4.0.3 and their test dependencies. No CodeFlowMu environment was used.

## Final local regression

`python -B -m pytest tests -q --tb=line --junitxml=<evidence>/fcop-403-retirement-full-3.xml`

**2320 passed / 0 failed / 0 errors / 2 existing skips** (349.37 seconds).

| Group | Collected | Result |
| --- | ---: | --- |
| Core package tests | 1691 | all passed |
| MCP package tests | 172 | all passed |
| Frozen Core Conformance | 119 | all passed; 60 test IDs retained |
| Current rule distribution | 101 | all passed; 16 retained DIST IDs plus Meta tests |
| v3 topology | 7 | all passed |
| Lifecycle | 142 | all passed |
| Schema | 90 | 88 passed; 2 historical empty-sample skips |

The two skips are unmodified tests/test_schemas/test_legacy_files_validate.py: absent historical docs/agents/log and empty fixture parameterization. No skip/xfail was added. Existing Traversable/RefResolver deprecation warnings remain.

Raw JUnit SHA-256: `30c408f4e5fb55a1f108fb5145b708dbc0a636948b8703775750eb03e6c2bea5`. Local raw evidence: C:/Users/Administrator/.codex/tmp/fcop-403-retirement-full-3.xml.

- Ruff: src, tests, mcp/src and current proof scripts PASS.
- mypy Core: 54 source files PASS; MCP: 20 source files PASS.
- Pages generator: 14 text files + logo parity PASS.
- Installed wheel runtime ownership/real stdio/Branch/restart: 36/36 PASS, imports asserted under the isolated environment's site-packages.
- Clean Core/pair wheel/sdist CLI probes: 4/4 PASS.
- Two builds: 4/4 raw artifact reproducibility, 8/8 strict Twine checks.
- 18 frozen Core Conformance files and all Schema bytes match the development base. Public tool/API snapshots unchanged. Core creation/Encoding/lifecycle/authorization/convergence code unchanged.

## Intermediate failures preserved

The initial development diagnostic had 155 failures while retirement edits were in flight; it is not an immutable baseline. A later fixed test run had 2317 passes and three failures: Registry publication expectation, missing updated Chinese spec payload and missing 4.0.3 pair expectation. All were fixed and full regression rerun. Directed stages: 271 PASS; CLI/install/readme 85 PASS; specific closeout 37 PASS.

New type checking also caught a missing static list narrowing in rule selection, corrected by a cast without changing accepted inputs. New CLI test initially invoked unsupported python -m fcop; corrected to the actual installed fcop console script, not by changing production.

The first build proof detected Windows Git export CRLF versus metadata LF. The proof exporter now requests canonical Git bytes; exact metadata comparison remains enforced. The failed build is not a release candidate.

## Remote verification

GitHub CI for the delivery HEAD is pending at this evidence commit. It must not be reported as PASS until the actual jobs complete; the final Manifest/PR receipt will bind the observed HEAD and results. This report is not a signed ADMIN Gate.
