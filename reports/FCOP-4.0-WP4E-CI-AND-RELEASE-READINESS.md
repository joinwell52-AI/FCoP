---
protocol: fcop
version: '4.0'
sender: ME
recipient: ADMIN
stage: WP4E_PHASE_A
taskbook_commit: 793b5eef808cecc55437c8c2dc43e737b56b1300
baseline: 64a24295d6c1fa53a182a819d39b295c2ba8d2d0
status: CONTENT_VERIFIED_FINAL_RECEIPT_REQUIRED
---

# WP4E CI and release readiness

## Evidence boundary

This is an executor report, not an ADMIN signature. The accepted WP4D parent is
`64a24295d6c1fa53a182a819d39b295c2ba8d2d0`, authenticated through
[OWNER Gate comment](https://github.com/joinwell52-AI/FCoP/pull/31#issuecomment-5610960987).
The remote Manifest was read as 34249 bytes with SHA-256
`21728890f757189cbc47e3ac131efcfb37d5ea0935de2b7467575de95f95314d`.
Taskbook: `793b5eef808cecc55437c8c2dc43e737b56b1300`, 13138 bytes, SHA-256
`05e39d231950917e56fef6cf63c9ee081316356058115a4942c47dffe3678bbc`.

Draft PR [#33](https://github.com/joinwell52-AI/FCoP/pull/33) targets main.
No main merge, tag, publication or CodeFlowMu operation is authorized or executed.
Final evidence/Manifest commits cannot substitute an earlier CI run for final HEAD CI.

## Acceptance matrix

Final HEAD requires: Windows and Ubuntu full regression with zero failures/errors/skips,
all applicable Core and MCP matrix/package jobs, both actual PR-only checks, RC source
parity, 12 installed consumers / 24 origins, 4 reproducible artifacts, 19 canonical and
21 authoritative identities, README parity/executable snippets, release dry-run and
all delivered GitHub blob hashes. An earlier taskbook-only or implementation run cannot
be reused as a final-head CI claim.

## Known intermediate runs

| Head | Workflow | Result at this report revision |
|---|---|---|
| 208ebb12e33518e7909dbcf4f6d0ad6c72c7e584 | 34426442905 RC | artifact-attribution failed; later cancelled by follow-up push |
| 208ebb12e33518e7909dbcf4f6d0ad6c72c7e584 | 34426442875 Core / 34426442874 MCP | both PR-only checks passed; full runs superseded/cancelled |
| 0b0da39d360952909305e0e20f4aad37cd8f8078 | 34426611345 RC | 15/15 jobs succeeded, including both full source platforms and 12 consumers |
| 0b0da39d360952909305e0e20f4aad37cd8f8078 | 34426611368 MCP | succeeded |
| 0b0da39d360952909305e0e20f4aad37cd8f8078 | 34426611357 Core | succeeded, preliminary 15/15 |

Jobs use the actual pull-request head rather than the synthetic merge checkout.
The PR still targets main so both existing PR-only checks execute with their original
snapshot/change-log requirements. Final aggregate counts and time-stamped evidence
will be appended after the last HEAD is verified.

## Local commands

- pytest test_install_prompt.py + initial WP4E tests: 46 passed, 0 failures; 109.46s.
- pytest -k metadata/readme after UTF-8 repair: 7 passed, 40 deselected (targeted, not full).
- Final six CI-guard cases + metadata case: 7 passed, 35 deselected; 0.09s.
- Full source parity command: python -B scripts/wp4d_source.py; returned SOURCE_ONLY
  Python and MCP success, the latter 24 transitions / 3 server processes / 2 real racers.
- Initial local full suite is preserved separately; its two missing-prompt-link failures
  are not relabeled as passing. Final new-head regressions are required.

Local timestamps not captured by an individual earlier command are not invented.
Final CI API started/completed times and JUnit counts provide the full auditable timing.

## Content verification closeout (not a self-signed Gate)

Fixed candidate content: `18f8d1ba3d0744bc4501e347312c3f97e2a4fede`.
Evidence observed at 2026-09-10T02:07:22.060075+00:00.
[Machine evidence](../tests/rc/evidence/wp4e/content-verification.json) retains
GitHub job/step timestamps, JUnit counts/hashes, every consumer result, build metadata,
dry-run result, 21 authoritative hashes and the 29/29 content-commit blob readback.

Windows and Ubuntu each passed 1973/1973 (1519 FCoP, 159 MCP, 295 frozen Conformance),
including 42/42 new WP4E tests; zero failures/errors/skips. 44/44 CI jobs and 2/2 actual
PR-only gates passed. Twelve consumers and 24 wheel/sdist origins passed the installed
MCP-only 24-transition / two-Branch / two-real-writer / three-process proof.
The separate release workflow dry-run passed its verification job; its publish job was
not applicable and was NOT counted as a passing job. Thus 45 applicable successful jobs.

Only the subsequent evidence and Manifest commits remain outside this verified content.
The executor must re-run all CI and release dry-run on the Manifest commit, read back all
final files, and post a fixed-head completion receipt on [PR #33](https://github.com/joinwell52-AI/FCoP/pull/33).
That later receipt is mandatory: these content-head results alone do not finish Phase A.
No source, test, example, workflow or README may be changed in the evidence suffix.

### Actual content-head Actions

| Workflow | Actions | Job outcome |
|---|---|---|
| .github/workflows/test-fcop-mcp.yml | [34427606981](https://github.com/joinwell52-AI/FCoP/actions/runs/34427606981) | 14 successful / 0 not applicable |
| .github/workflows/test-fcop.yml | [34427606898](https://github.com/joinwell52-AI/FCoP/actions/runs/34427606898) | 15 successful / 0 not applicable |
| .github/workflows/rc-candidate.yml | [34427606888](https://github.com/joinwell52-AI/FCoP/actions/runs/34427606888) | 15 successful / 0 not applicable |
| release-dry-run | [34427777738](https://github.com/joinwell52-AI/FCoP/actions/runs/34427777738) | 1 successful / 1 not applicable |

### Full regression commands and times (UTC)

Command on both platforms:
`python -B -m pytest tests/test_fcop tests/conformance/v4 tests/test_fcop_mcp tests/conformance/rule_distribution_v4 -q --junitxml="$RUNNER_TEMP/full.xml"`

| Platform | Step start | Step end | Exit | Tests | Fail / error / skip | JUnit seconds |
|---|---|---|---|---|---|---|---|
| ubuntu-latest / Python 3.12 | 2026-09-10T01:59:10Z | 2026-09-10T02:01:09Z | 0 | 1973 | 0 / 0 / 0 | 116.816 |
| windows-latest / Python 3.12 | 2026-09-10T01:59:50Z | 2026-09-10T02:04:32Z | 0 | 1973 | 0 / 0 / 0 | 278.816 |

Ruff: `python -m ruff check src tests`; mypy: `python -m mypy src/fcop`.
Local targeted invocation: `python -B -m pytest tests/test_fcop/test_wp4e_release_readiness.py -q`;
42 passed / 0 failed / 0 skipped, 85.96 seconds, exit 0. Exact earlier start/end not recorded.

### Installed consumer command and times (UTC)

Each runs `python -B scripts/wp4d_consume.py <four-artifacts> <manifest-sha>
<historical-3.2.5-fixture> <historical-sha> <external-evidence-dir> --stage WP4E`.
The arguments' actual values and hashes are in the uploaded result.json files.

| OS | Python | Start | End | Origins | Exit / status |
|---|---|---|---|---|---|
| Darwin | 3.10.11 | 2026-09-10T02:00:24.612961+00:00 | 2026-09-10T02:01:05.214013+00:00 | wheel + sdist | 0 / PASS |
| Darwin | 3.11.9 | 2026-09-10T02:01:16.537237+00:00 | 2026-09-10T02:01:51.698888+00:00 | wheel + sdist | 0 / PASS |
| Darwin | 3.12.10 | 2026-09-10T02:00:29.197195+00:00 | 2026-09-10T02:01:17.136981+00:00 | wheel + sdist | 0 / PASS |
| Darwin | 3.13.15 | 2026-09-10T02:01:26.392397+00:00 | 2026-09-10T02:02:28.078457+00:00 | wheel + sdist | 0 / PASS |
| Linux | 3.10.21 | 2026-09-10T02:01:12.151871+00:00 | 2026-09-10T02:02:12.891172+00:00 | wheel + sdist | 0 / PASS |
| Linux | 3.11.16 | 2026-09-10T01:59:52.728175+00:00 | 2026-09-10T02:00:56.271233+00:00 | wheel + sdist | 0 / PASS |
| Linux | 3.12.14 | 2026-09-10T02:00:58.504691+00:00 | 2026-09-10T02:02:08.784098+00:00 | wheel + sdist | 0 / PASS |
| Linux | 3.13.15 | 2026-09-10T02:00:03.313623+00:00 | 2026-09-10T02:01:00.582005+00:00 | wheel + sdist | 0 / PASS |
| Windows | 3.10.11 | 2026-09-10T02:01:04.348248+00:00 | 2026-09-10T02:03:10.889813+00:00 | wheel + sdist | 0 / PASS |
| Windows | 3.11.9 | 2026-09-10T02:01:16.735269+00:00 | 2026-09-10T02:03:46.197928+00:00 | wheel + sdist | 0 / PASS |
| Windows | 3.12.10 | 2026-09-10T02:01:20.242476+00:00 | 2026-09-10T02:03:30.330526+00:00 | wheel + sdist | 0 / PASS |
| Windows | 3.13.15 | 2026-09-10T02:00:04.575148+00:00 | 2026-09-10T02:02:47.509984+00:00 | wheel + sdist | 0 / PASS |

All are real installed-origin checks, not source imports; assertions cover metadata,
46/12/4 discovery, Branch convergence, T2–T7, retries, zero effects, legacy reads and
mixed-version rejection. Source-only checks are separately labelled, not double-counted.
