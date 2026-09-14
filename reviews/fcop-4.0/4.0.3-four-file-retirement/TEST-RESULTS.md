# 4.0.3 test results

Local environment: dedicated Windows Python 3.12 environment with editable fcop/fcop-mcp 4.0.3 and their test dependencies. No CodeFlowMu environment was used.

## Final local regression

`python -B -m pytest tests -q --tb=line --junitxml=<evidence>/fcop-403-retirement-full-5.xml`

**2320 passed / 0 failed / 0 errors / 2 existing skips** (323.10 seconds), on corrected test/implementation HEAD 5da0bbc127e272cd2492c2963db6441e6b2c46e3. Production/test files were unchanged during this final run; only evidence documents were being completed.

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

Raw JUnit SHA-256: `21e376409375515e05ac42ccd5fe367b794a814f6d689a047b4f5f6701a32217`. Local raw evidence: C:/Users/Administrator/.codex/tmp/fcop-403-retirement-full-5.xml. Earlier full-3 and full-4 results (also 2320 passed / 2 existing skips) remain preserved locally and in earlier evidence history.

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

The first delivery 7db5a24 had no CI checks because upstream PR #49 introduced a homepage merge conflict. A history-preserving merge b767e8f incorporated the upstream documentation, kept the CLI section visible and restored PR CI. It did not merge this PR into main.

Runs 34821714826 (Core) and 34821714874 (MCP) then exposed new-test defects: Windows non-venv console scripts live in sysconfig's scripts directory, not beside python.exe; MCP CI additionally type-checks its test tree, revealing 25 diagnostics in the two new ownership-test files. The corrections use sysconfig.get_path("scripts"), annotate tests, express existing runtime v4 method binding with Callable casts, and add structured-result/type narrowing assertions. No existing behavior assertion was removed, no skip/xfail added, no workflow or production code changed. Corrected test commit: 5da0bbc127e272cd2492c2963db6441e6b2c46e3. Directed 42/42 PASS; MCP test-tree mypy 16 source files PASS. Both package production mypy checks and Ruff remain PASS.

At corrected implementation HEAD 5da0bbc127e272cd2492c2963db6441e6b2c46e3, MCP run 34822242078 passed all 14 jobs; Core run 34822241976 was still running at evidence drafting. The final Manifest/PR receipt must bind completed CI for the actual final delivery HEAD, not substitute checkpoint or partial CI. This report is not a signed ADMIN Gate.
