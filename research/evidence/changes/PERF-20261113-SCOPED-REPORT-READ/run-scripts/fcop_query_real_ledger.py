from pathlib import Path
from statistics import median
import hashlib, json, sys, time

ROOT = Path('D:/codeflowmu/.cache/fcop-query-source-20261113')
PACKET = ROOT/'research/evidence/changes/PERF-20261113-SCOPED-REPORT-READ'
WORKSPACE = Path('D:/codeflowmu/projects/new-machine-dev-20261110')
sys.path[:0] = [str(ROOT/'src'), str(ROOT), 'D:/codeflowmu/packages/codeflowmu-v3/runtime']
import yaml
from fcop import Project
from fcop.v4 import reports
from report_parse_reuse import make_parser_dispatch, report_parsing_scope

yaml.load = make_parser_dispatch(yaml.load, yaml.SafeLoader)
candidate = reports.ReportQueries
namespace = {'__name__': 'fcop.v4.reports_baseline'}
exec(compile((PACKET/'baseline-source/reports.py').read_bytes(), 'baseline-reports.py', 'exec'), namespace)
baseline = namespace['ReportQueries']
project = Project(WORKSPACE)
task = 'TASK-44445de5b3ca4028ac14eedfd14ebde1'
report = 'REPORT-ff64cb0b701c4ce7abe30f753bcd5da3'
attempt = project.inspect_state(task_id=task)['current_attempt_id']

def snapshot():
    return {p.relative_to(WORKSPACE).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in (WORKSPACE/'fcop').rglob('*') if p.is_file()}

before = snapshot()
rows = []
for operation in ('read_report', 'scoped_heads'):
    expected = None
    for pair, order in enumerate(('AB', 'BA', 'AB'), 1):
        for label in order:
            reports.ReportQueries = baseline if label == 'A' else candidate
            try:
                with report_parsing_scope():
                    start = time.perf_counter()
                    if operation == 'read_report':
                        value = project.read_report(report)
                    else:
                        value = project.list_reports(subject_ref=task, attempt_id=attempt, head_only=True)
                    elapsed = (time.perf_counter()-start)*1000
            finally:
                reports.ReportQueries = candidate
            digest = hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
            if expected is None:
                expected = digest
            assert expected == digest, 'Result drift'
            assert snapshot() == before, 'Persisted ledger changed'
            rows.append(dict(operation=operation, pair=pair, order=order, variant=label,
                             elapsed_ms=elapsed, result_sha256=digest))
            with (PACKET/'runs/real-ledger-progress.json').open('w', encoding='utf-8') as stream:
                json.dump(dict(completed=False, rows=rows), stream, indent=2)
            print(json.dumps(rows[-1]), flush=True)
summaries = []
for operation in ('read_report', 'scoped_heads'):
    values = {v: median(r['elapsed_ms'] for r in rows if r['operation']==operation and r['variant']==v) for v in 'AB'}
    summaries.append(dict(operation=operation, baseline_median_ms=values['A'], candidate_median_ms=values['B'],
                          reduction_percent=(1-values['B']/values['A'])*100))
with (PACKET/'runs/real-ledger-01.json').open('x', encoding='utf-8') as stream:
    json.dump(dict(completed=True, source_origin=reports.__file__, workspace=str(WORKSPACE),
                   yaml_parse_reuse_enabled_in_both=True, unchanged_files=True, paired_result_parity=True,
                   live_sdk_modified=False, task_decisions=0, rows=rows, summaries=summaries), stream, indent=2)
print(json.dumps(dict(completed=True, summaries=summaries)), flush=True)
