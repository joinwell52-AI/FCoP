# Test Protocol

## Objective

Fix public Core read-query scope: list_reports(subject_ref, attempt_id) must resolve heads only for matching groups; read_report(ID) must first locate that exact envelope and query its task/attempt rather than validate every unrelated head group. Keep the one canonical report_head resolver used by lifecycle/writers.

## Scope

Only src/fcop/v4/reports.py and targeted tests. No CodeFlowMu, Runtime, Profile, Host, command/adjudication/authority changes in Core. No new persistent index or alternative head rule. The existing inventory/schema/freshness reads stay in place, so this first change reduces unrelated graph work but does not claim zero whole-directory metadata reads. Package source remains an unpublished change candidate; installed 18766 SDK files must not be edited.

## Environment

Official repository clone at f1aa3348a9a64475caba8036dcc23e83f5080c7c, current library 4.0.5. Windows Python 3.12.9, installed pytest/PyYAML/jsonschema, source selected explicitly through PYTHONPATH. Native tests use disposable FCoP workspaces. Optional real-ledger benchmark is read-only, in a separate process, and never changes installed package files or task state.

## Baseline

f1aa3348a9a64475caba8036dcc23e83f5080c7c, clean source clone. Save reports.py before modifications. Run existing tests/test_fcop/test_v4_report_queries.py as baseline. Preserve all failures and original outputs.

## Primary Metrics

Public return parity for valid target data; canonical target error codes, replacement/history metadata, stale/concurrent read checks unchanged; unscoped query still validates all groups. Count canonical resolver calls and query _scan calls for target versus all groups. Three paired AB/BA/AB queries in a fixed multi-task fixture, same result digests and no persisted fact changes. Querying an unrelated invalid head graph should not make a matching valid target query resolve that foreign graph; malformed inventory remains rejected under the preserved scan contract. A targeted query still uses canonical current-head checks.

## Planned Commands

Baseline pytest report-query tests. Candidate targeted scope tests plus existing report-query, v4 lifecycle/creation/authorization/convergence/linearization regressions. Compile touched Python and git diff --check; run available lint for changed files, record missing tooling honestly. Benchmark public Project.list_reports/read_report with original and candidate methods under identical fixtures. No PyPI upload, tag, Release, merge, installed SDK modification, model task approval or root lifecycle edit. Any wheel/release work requires a separate release gate and explicit publication authorization.

## Exclusion Rules

Do not claim the 92ms UI file view is the baseline for Core read_report; they have different contracts. Core read_report still returns canonical is_head/head_ref/head_digest/replacement metadata, while the UI text view is material-only. No user credential/configuration copies into evidence. Preserve all negative/slow samples; three pairs only support engineering observations. Full index design and zero unrelated-file reads are outside this bounded fix.
